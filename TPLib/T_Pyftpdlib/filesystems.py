# Copyright (C) 2007 Giampaolo Rodola' <g.rodola@gmail.com>.
# Use of this source code is governed by MIT license that can be
# found in the LICENSE file.

import os
import stat
import tempfile
import time


try:
    import grp
    import pwd
except ImportError:
    pwd = grp = None


__all__ = ['AbstractedFS', 'FilesystemError']


_months_map = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec',
}


def _memoize(fun):
    def wrapper(*args, **kwargs):
        key = (args, frozenset(sorted(kwargs.items())))
        try:
            return cache[key]
        except KeyError:
            ret = cache[key] = fun(*args, **kwargs)
            return ret

    cache = {}
    return wrapper

class FilesystemError(Exception):
    pass

class AbstractedFS:
    def __init__(self, root, cmd_channel, encoding="utf8"):
        self._cwd = '/'
        self._root = root
        self.cmd_channel = cmd_channel
        self.__encoding = encoding

    @property
    def root(self):
        return self._root

    @property
    def cwd(self):
        return self._cwd

    @property
    def encoding(self):
        return self.__encoding

    @encoding.setter
    def encoding(self,value):
        self.__encoding = value

    @root.setter
    def root(self, path):
        self._root = path

    @cwd.setter
    def cwd(self, path):
        self._cwd = path

    @staticmethod
    def _isabs(path, _windows=os.name == "nt"):
        if _windows and path.startswith("/"):
            return True
        return os.path.isabs(path)

    def ftpnorm(self, ftppath):
        if self._isabs(ftppath):
            p = os.path.normpath(ftppath)
        else:
            p = os.path.normpath(os.path.join(self.cwd, ftppath))
        if os.sep == "\\":
            p = p.replace("\\", "/")
        while p[:2] == '//':
            p = p[1:]
        if not self._isabs(p):
            p = "/"
        return p

    def ftp2fs(self, ftppath):
        if os.path.normpath(self.root) == os.sep:
            return os.path.normpath(self.ftpnorm(ftppath))
        else:
            p = self.ftpnorm(ftppath)[1:]
            return os.path.normpath(os.path.join(self.root, p))

    def fs2ftp(self, fspath):
        if self._isabs(fspath):
            p = os.path.normpath(fspath)
        else:
            p = os.path.normpath(os.path.join(self.root, fspath))
        if not self.validpath(p):
            return '/'
        p = p.replace(os.sep, "/")
        p = p[len(self.root) :]
        if not p.startswith('/'):
            p = '/' + p
        return p

    def validpath(self, path):
        root = self.realpath(self.root)
        path = self.realpath(path)
        if not root.endswith(os.sep):
            root += os.sep
        if not path.endswith(os.sep):
            path += os.sep
        return path[0 : len(root)] == root

    # --- Wrapper methods around open() and tempfile.mkstemp

    def open(self, filename, mode):
        return open(filename, mode)

    def mkstemp(self, suffix='', prefix='', dir=None, mode='wb'):
        class FileWrapper:
            def __init__(self, fd, name):
                self.file = fd
                self.name = name
            def __getattr__(self, attr):
                return getattr(self.file, attr)
        text = 'b' not in mode
        tempfile.TMP_MAX = 50
        fd, name = tempfile.mkstemp(suffix, prefix, dir, text=text)
        file = os.fdopen(fd, mode)
        return FileWrapper(file, name)

    def chdir(self, path):
        os.chdir(path)
        self.cwd = self.fs2ftp(path)

    def mkdir(self, path):
        os.mkdir(path)

    def listdir(self, path):
        return os.listdir(path)

    def listdirinfo(self, path):
        return os.listdir(path)

    def rmdir(self, path):
        os.rmdir(path)

    def remove(self, path):
        os.remove(path)

    def rename(self, src, dst):
        os.rename(src, dst)

    def chmod(self, path, mode):
        if not hasattr(os, 'chmod'):
            raise NotImplementedError
        os.chmod(path, mode)

    def stat(self, path):
        return os.stat(path)

    def utime(self, path, timeval):
        return os.utime(path, (timeval, timeval))

    if hasattr(os, 'lstat'):
        def lstat(self, path):
            return os.lstat(path)

    else:
        lstat = stat

    if hasattr(os, 'readlink'):
        def readlink(self, path):
            return os.readlink(path)

    # --- Wrapper methods around os.path.* calls

    def isfile(self, path):
        return os.path.isfile(path)

    def islink(self, path):
        return os.path.islink(path)

    def isdir(self, path):
        return os.path.isdir(path)

    def getsize(self, path):
        return os.path.getsize(path)

    def getmtime(self, path):
        return os.path.getmtime(path)

    def realpath(self, path):
        return os.path.realpath(path)

    def lexists(self, path):
        return os.path.lexists(path)

    if pwd is not None:

        def get_user_by_uid(self, uid):
            try:
                return pwd.getpwuid(uid).pw_name
            except KeyError:
                return uid

    else:

        def get_user_by_uid(self, uid):
            return "owner"

    if grp is not None:

        def get_group_by_gid(self, gid):
            try:
                return grp.getgrgid(gid).gr_name
            except KeyError:
                return gid

    else:

        def get_group_by_gid(self, gid):
            return "group"

    def format_list(self, basedir, listing, ignore_err=True):

        @_memoize
        def get_user_by_uid(uid):
            return self.get_user_by_uid(uid)

        @_memoize
        def get_group_by_gid(gid):
            return self.get_group_by_gid(gid)

        if self.cmd_channel.use_gmt_times:
            timefunc = time.gmtime
        else:
            timefunc = time.localtime
        SIX_MONTHS = 180 * 24 * 60 * 60
        readlink = getattr(self, 'readlink', None)
        now = time.time()
        for basename in listing:
            file = os.path.join(basedir, basename)
            try:
                st = self.lstat(file)
            except (OSError, FilesystemError):
                if ignore_err:
                    continue
                raise

            perms = stat.filemode(st.st_mode)
            nlinks = st.st_nlink
            if not nlinks:
                nlinks = 1
            size = st.st_size
            uname = get_user_by_uid(st.st_uid)
            gname = get_group_by_gid(st.st_gid)
            _st_mtime=st.st_mtime
            if _st_mtime < 0: _st_mtime = -_st_mtime
            mtime = timefunc(_st_mtime)
            fmtstr = '%d  %Y' if now - st.st_mtime > SIX_MONTHS else '%d %H:%M'
            try:
                mtimestr = "%s %s" % (
                    _months_map[mtime.tm_mon],
                    time.strftime(fmtstr, mtime),
                )
            except ValueError:
                mtime = timefunc()
                mtimestr = "%s %s" % (
                    _months_map[mtime.tm_mon],
                    time.strftime("%d %H:%M", mtime),
                )

            islink = (st.st_mode & 61440) == stat.S_IFLNK
            if islink and readlink is not None:
                try:
                    basename = basename + " -> " + readlink(file)
                except (OSError, FilesystemError):
                    if not ignore_err:
                        raise

            line = "%s %3s %-8s %-8s %8s %s %s\r\n" % (
                perms,
                nlinks,
                uname,
                gname,
                size,
                mtimestr,
                basename,
            )
            yield line.encode(
                self.cmd_channel.encoding, self.cmd_channel.unicode_errors
            )

    def format_mlsx(self, basedir, listing, perms, facts, ignore_err=True):
        if self.cmd_channel.use_gmt_times:
            timefunc = time.gmtime
        else:
            timefunc = time.localtime
        permdir = ''.join([x for x in perms if x not in 'arw'])
        permfile = ''.join([x for x in perms if x not in 'celmp'])
        if ('w' in perms) or ('a' in perms) or ('f' in perms):
            permdir += 'c'
        if 'd' in perms:
            permdir += 'p'
        show_type = 'type' in facts
        show_perm = 'perm' in facts
        show_size = 'size' in facts
        show_modify = 'modify' in facts
        show_create = 'create' in facts
        show_mode = 'unix.mode' in facts
        show_uid = 'unix.uid' in facts
        show_gid = 'unix.gid' in facts
        show_unique = 'unique' in facts
        for basename in listing:
            retfacts = {}
            file = os.path.join(basedir, basename)
            try:
                st = self.stat(file)
            except (OSError, FilesystemError):
                if ignore_err:
                    continue
                raise
            isdir = (st.st_mode & 61440) == stat.S_IFDIR
            if isdir:
                if show_type:
                    if basename == '.':
                        retfacts['type'] = 'cdir'
                    elif basename == '..':
                        retfacts['type'] = 'pdir'
                    else:
                        retfacts['type'] = 'dir'
                if show_perm:
                    retfacts['perm'] = permdir
            else:
                if show_type:
                    retfacts['type'] = 'file'
                if show_perm:
                    retfacts['perm'] = permfile
            _st_mtime=st.st_mtime
            if _st_mtime < 0: _st_mtime = -_st_mtime
            _st_ctime=st.st_ctime
            if _st_ctime < 0: _st_ctime = -_st_ctime
            if show_size:
                retfacts['size'] = st.st_size
            if show_modify:
                try:
                    retfacts['modify'] = time.strftime(
                        "%Y%m%d%H%M%S", timefunc(_st_mtime)
                    )
                except ValueError:
                    pass
            if show_create:
                try:
                    retfacts['create'] = time.strftime(
                        "%Y%m%d%H%M%S", timefunc(_st_ctime)
                    )
                except ValueError:
                    pass
            if show_mode:
                retfacts['unix.mode'] = oct(st.st_mode & 511)
            if show_uid:
                retfacts['unix.uid'] = st.st_uid
            if show_gid:
                retfacts['unix.gid'] = st.st_gid
            if show_unique:
                retfacts['unique'] = f"{st.st_dev:x}g{st.st_ino:x}"
            factstring = "".join(
                [f"{x}={retfacts[x]};" for x in sorted(retfacts.keys())]
            )
            line = f"{factstring} {basename}\r\n"
            yield line.encode(
                self.cmd_channel.encoding, self.cmd_channel.unicode_errors
            )

if os.name == 'posix':
    __all__ += ['UnixFilesystem']

    class UnixFilesystem(AbstractedFS):
        def __init__(self, root, cmd_channel):
            AbstractedFS.__init__(self, root, cmd_channel)
            self.cwd = root

        def ftp2fs(self, ftppath):
            return self.ftpnorm(ftppath)

        def fs2ftp(self, fspath):
            return fspath

        def validpath(self, path):
            return True
