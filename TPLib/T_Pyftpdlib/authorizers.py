import os
import warnings


__all__ = [
    'DummyAuthorizer',
    # 'BaseUnixAuthorizer', 'UnixAuthorizer',
    # 'BaseWindowsAuthorizer', 'WindowsAuthorizer',
]

class AuthorizerError(Exception):
    pass


class AuthenticationFailed(Exception):
    pass


class DummyAuthorizer:
    read_perms = "elr"
    write_perms = "adfmwMT"
    def __init__(self):
        self.user_table = {}
    def add_user(
        self,
        username,
        password,
        homedir,
        perm='elr',
        msg_login="Login successful.",
        msg_quit="Goodbye.",
    ):
        if self.has_user(username):
            raise ValueError(f'user {username!r} already exists')
        if not os.path.isdir(homedir):
            raise ValueError(f'no such directory: {homedir!r}')
        homedir = os.path.realpath(homedir)
        self._check_permissions(username, perm)
        dic = {
            'pwd': str(password),
            'home': homedir,
            'perm': perm,
            'operms': {},
            'msg_login': str(msg_login),
            'msg_quit': str(msg_quit),
        }
        self.user_table[username] = dic

    def add_anonymous(self, homedir, **kwargs):
        DummyAuthorizer.add_user(self, 'anonymous', '', homedir, **kwargs)

    def remove_user(self, username):
        del self.user_table[username]

    def override_perm(self, username, directory, perm, recursive=False):
        self._check_permissions(username, perm)
        if not os.path.isdir(directory):
            raise ValueError(f'no such directory: {directory!r}')
        directory = os.path.normcase(os.path.realpath(directory))
        home = os.path.normcase(self.get_home_dir(username))
        if directory == home:
            raise ValueError("can't override home directory permissions")
        if not self._issubpath(directory, home):
            raise ValueError("path escapes user home directory")
        self.user_table[username]['operms'][directory] = perm, recursive

    def validate_authentication(self, username, password, handler):
        msg = "Authentication failed."
        if not self.has_user(username):
            if username == 'anonymous':
                msg = "Anonymous access not allowed."
            raise AuthenticationFailed(msg)
        if username != 'anonymous':
            if self.user_table[username]['pwd'] != password:
                raise AuthenticationFailed(msg)

    def get_home_dir(self, username):
        return self.user_table[username]['home']

    def impersonate_user(self, username, password):
        pass

    def terminate_impersonation(self, username):
        pass

    def has_user(self, username):
        return username in self.user_table

    def has_perm(self, username, perm, path=None):
        if path is None:
            return perm in self.user_table[username]['perm']

        path = os.path.normcase(path)
        for dir in self.user_table[username]['operms']:
            operm, recursive = self.user_table[username]['operms'][dir]
            if self._issubpath(path, dir):
                if recursive:
                    return perm in operm
                if path == dir or (
                    os.path.dirname(path) == dir and not os.path.isdir(path)
                ):
                    return perm in operm

        return perm in self.user_table[username]['perm']

    def get_perms(self, username):
        return self.user_table[username]['perm']

    def get_msg_login(self, username):
        return self.user_table[username]['msg_login']

    def get_msg_quit(self, username):
        try:
            return self.user_table[username]['msg_quit']
        except KeyError:
            return "Goodbye."

    def _check_permissions(self, username, perm):
        warned = 0
        for p in perm:
            if p not in self.read_perms + self.write_perms:
                raise ValueError(f'no such permission {p!r}')
            if (
                username == 'anonymous'
                and p in self.write_perms
                and not warned
            ):
                warnings.warn(
                    "write permissions assigned to anonymous user.",
                    RuntimeWarning,
                    stacklevel=2,
                )
                warned = 1

    def _issubpath(self, a, b):
        p1 = a.rstrip(os.sep).split(os.sep)
        p2 = b.rstrip(os.sep).split(os.sep)
        return p1[: len(p2)] == p2


def replace_anonymous(callable):
    def wrapper(self, username, *args, **kwargs):
        if username == 'anonymous':
            username = self.anonymous_user or username
        return callable(self, username, *args, **kwargs)

    return wrapper


# ===================================================================
# --- platform specific authorizers
# ===================================================================


class _Base:
    msg_no_such_user = "Authentication failed."
    msg_wrong_password = "Authentication failed."
    msg_anon_not_allowed = "Anonymous access not allowed."
    msg_invalid_shell = "User %s doesn't have a valid shell."
    msg_rejected_user = "User %s is not allowed to login."
    def __init__(self):
        if self.rejected_users and self.allowed_users:
            raise AuthorizerError(
                "rejected_users and allowed_users options "
                "are mutually exclusive"
            )
        users = self._get_system_users()
        for user in self.allowed_users or self.rejected_users:
            if user == 'anonymous':
                raise AuthorizerError('invalid username "anonymous"')
            if user not in users:
                raise AuthorizerError(f'unknown user {user}')

        if self.anonymous_user is not None:
            if not self.has_user(self.anonymous_user):
                raise AuthorizerError(f'no such user {self.anonymous_user}')
            home = self.get_home_dir(self.anonymous_user)
            if not os.path.isdir(home):
                raise AuthorizerError(
                    f'no valid home set for user {self.anonymous_user}'
                )
    def override_user(
        self,
        username,
        password=None,
        homedir=None,
        perm=None,
        msg_login=None,
        msg_quit=None,
    ):
        if (
            not password
            and not homedir
            and not perm
            and not msg_login
            and not msg_quit
        ):
            raise AuthorizerError(
                "at least one keyword argument must be specified"
            )
        if self.allowed_users and username not in self.allowed_users:
            raise AuthorizerError(f'{username} is not an allowed user')
        if self.rejected_users and username in self.rejected_users:
            raise AuthorizerError(f'{username} is not an allowed user')
        if username == "anonymous" and password:
            raise AuthorizerError("can't assign password to anonymous user")
        if not self.has_user(username):
            raise AuthorizerError(f'no such user {username}')

        if username in self._dummy_authorizer.user_table:
            # re-set parameters
            del self._dummy_authorizer.user_table[username]
        self._dummy_authorizer.add_user(
            username,
            password or "",
            homedir or os.getcwd(),
            perm or "",
            msg_login or "",
            msg_quit or "",
        )
        if homedir is None:
            self._dummy_authorizer.user_table[username]['home'] = ""

    def get_msg_login(self, username):
        return self._get_key(username, 'msg_login') or self.msg_login

    def get_msg_quit(self, username):
        return self._get_key(username, 'msg_quit') or self.msg_quit

    def get_perms(self, username):
        overridden_perms = self._get_key(username, 'perm')
        if overridden_perms:
            return overridden_perms
        if username == 'anonymous':
            return 'elr'
        return self.global_perm

    def has_perm(self, username, perm, path=None):
        return perm in self.get_perms(username)

    def _get_key(self, username, key):
        if self._dummy_authorizer.has_user(username):
            return self._dummy_authorizer.user_table[username][key]

    def _is_rejected_user(self, username):
        if self.allowed_users and username not in self.allowed_users:
            return True
        return bool(self.rejected_users and username in self.rejected_users)


# ===================================================================
# --- UNIX
# ===================================================================

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import crypt
        import pwd
        import spwd
except ImportError:
    pass
else:
    __all__ += ['BaseUnixAuthorizer', 'UnixAuthorizer']

    # the uid/gid the server runs under
    PROCESS_UID = os.getuid()
    PROCESS_GID = os.getgid()

    class BaseUnixAuthorizer:
        def __init__(self, anonymous_user=None):
            if os.geteuid() != 0 or not spwd.getspall():
                raise AuthorizerError("super user privileges are required")
            self.anonymous_user = anonymous_user

            if self.anonymous_user is not None:
                try:
                    pwd.getpwnam(self.anonymous_user).pw_dir  # noqa
                except KeyError:
                    raise AuthorizerError(f'no such user {anonymous_user}')
        def validate_authentication(self, username, password, handler):
            if username == "anonymous":
                if self.anonymous_user is None:
                    raise AuthenticationFailed(self.msg_anon_not_allowed)
            else:
                try:
                    pw1 = spwd.getspnam(username).sp_pwd
                    pw2 = crypt.crypt(password, pw1)
                except KeyError:  # no such username
                    raise AuthenticationFailed(self.msg_no_such_user)
                else:
                    if pw1 != pw2:
                        raise AuthenticationFailed(self.msg_wrong_password)

        @replace_anonymous
        def impersonate_user(self, username, password):
            try:
                pwdstruct = pwd.getpwnam(username)
            except KeyError:
                raise AuthorizerError(self.msg_no_such_user)
            else:
                os.setegid(pwdstruct.pw_gid)
                os.seteuid(pwdstruct.pw_uid)

        def terminate_impersonation(self, username):
            os.setegid(PROCESS_GID)
            os.seteuid(PROCESS_UID)

        @replace_anonymous
        def has_user(self, username):
            return username in self._get_system_users()

        @replace_anonymous
        def get_home_dir(self, username):
            try:
                return pwd.getpwnam(username).pw_dir
            except KeyError:
                raise AuthorizerError(self.msg_no_such_user)

        @staticmethod
        def _get_system_users():
            return [entry.pw_name for entry in pwd.getpwall()]

        def get_msg_login(self, username):
            return "Login successful."

        def get_msg_quit(self, username):
            return "Goodbye."

        def get_perms(self, username):
            return "elradfmwMT"

        def has_perm(self, username, perm, path=None):
            return perm in self.get_perms(username)

    class UnixAuthorizer(_Base, BaseUnixAuthorizer):
        def __init__(
            self,
            global_perm="elradfmwMT",
            allowed_users=None,
            rejected_users=None,
            require_valid_shell=True,
            anonymous_user=None,
            msg_login="Login successful.",
            msg_quit="Goodbye.",
        ):
            BaseUnixAuthorizer.__init__(self, anonymous_user)
            if allowed_users is None:
                allowed_users = []
            if rejected_users is None:
                rejected_users = []
            self.global_perm = global_perm
            self.allowed_users = allowed_users
            self.rejected_users = rejected_users
            self.anonymous_user = anonymous_user
            self.require_valid_shell = require_valid_shell
            self.msg_login = msg_login
            self.msg_quit = msg_quit

            self._dummy_authorizer = DummyAuthorizer()
            self._dummy_authorizer._check_permissions('', global_perm)
            _Base.__init__(self)
            if require_valid_shell:
                for username in self.allowed_users:
                    if not self._has_valid_shell(username):
                        raise AuthorizerError(
                            f"user {username} has not a valid shell"
                        )

        def override_user(
            self,
            username,
            password=None,
            homedir=None,
            perm=None,
            msg_login=None,
            msg_quit=None,
        ):
            if self.require_valid_shell and username != 'anonymous':
                if not self._has_valid_shell(username):
                    raise AuthorizerError(self.msg_invalid_shell % username)
            _Base.override_user(
                self, username, password, homedir, perm, msg_login, msg_quit
            )
        def validate_authentication(self, username, password, handler):
            if username == "anonymous":
                if self.anonymous_user is None:
                    raise AuthenticationFailed(self.msg_anon_not_allowed)
                return
            if self._is_rejected_user(username):
                raise AuthenticationFailed(self.msg_rejected_user % username)
            overridden_password = self._get_key(username, 'pwd')
            if overridden_password:
                if overridden_password != password:
                    raise AuthenticationFailed(self.msg_wrong_password)
            else:
                BaseUnixAuthorizer.validate_authentication(
                    self, username, password, handler
                )
            if self.require_valid_shell and username != 'anonymous':
                if not self._has_valid_shell(username):
                    raise AuthenticationFailed(
                        self.msg_invalid_shell % username
                    )

        @replace_anonymous
        def has_user(self, username):
            if self._is_rejected_user(username):
                return False
            return username in self._get_system_users()

        @replace_anonymous
        def get_home_dir(self, username):
            overridden_home = self._get_key(username, 'home')
            if overridden_home:
                return overridden_home
            return BaseUnixAuthorizer.get_home_dir(self, username)

        @staticmethod
        def _has_valid_shell(username):
            try:
                file = open('/etc/shells')
            except FileNotFoundError:
                return True
            else:
                with file:
                    try:
                        shell = pwd.getpwnam(username).pw_shell
                    except KeyError:  # invalid user
                        return False
                    for line in file:
                        if line.startswith('#'):
                            continue
                        line = line.strip()
                        if line == shell:
                            return True
                    return False

try:
    import pywintypes
    import win32api
    import win32con
    import win32net
    import win32security
except ImportError:
    pass
else:  # pragma: no cover
    import winreg

    __all__ += ['BaseWindowsAuthorizer', 'WindowsAuthorizer']

    class BaseWindowsAuthorizer:
        def __init__(self, anonymous_user=None, anonymous_password=None):
            self.anonymous_user = anonymous_user
            self.anonymous_password = anonymous_password
            if self.anonymous_user is not None:
                self.impersonate_user(
                    self.anonymous_user, self.anonymous_password
                )
                self.terminate_impersonation(None)

        def validate_authentication(self, username, password, handler):
            if username == "anonymous":
                if self.anonymous_user is None:
                    raise AuthenticationFailed(self.msg_anon_not_allowed)
                return
            try:
                win32security.LogonUser(
                    username,
                    None,
                    password,
                    win32con.LOGON32_LOGON_INTERACTIVE,
                    win32con.LOGON32_PROVIDER_DEFAULT,
                )
            except pywintypes.error:
                raise AuthenticationFailed(self.msg_wrong_password)

        @replace_anonymous
        def impersonate_user(self, username, password):
            handler = win32security.LogonUser(
                username,
                None,
                password,
                win32con.LOGON32_LOGON_INTERACTIVE,
                win32con.LOGON32_PROVIDER_DEFAULT,
            )
            win32security.ImpersonateLoggedOnUser(handler)
            handler.Close()

        def terminate_impersonation(self, username):
            win32security.RevertToSelf()

        @replace_anonymous
        def has_user(self, username):
            return username in self._get_system_users()

        @replace_anonymous
        def get_home_dir(self, username):
            try:
                sid = win32security.ConvertSidToStringSid(
                    win32security.LookupAccountName(None, username)[0]
                )
            except pywintypes.error as err:
                raise AuthorizerError(err)
            path = r"SOFTWARE\Microsoft\Windows NT"
            path += r"\CurrentVersion\ProfileList" + "\\" + sid
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
            except OSError:
                raise AuthorizerError(
                    f"No profile directory defined for user {username}"
                )
            value = winreg.QueryValueEx(key, "ProfileImagePath")[0]
            home = win32api.ExpandEnvironmentStrings(value)
            return home

        @classmethod
        def _get_system_users(cls):
            return [
                entry['name'] for entry in win32net.NetUserEnum(None, 0)[0]
            ]

        def get_msg_login(self, username):
            return "Login successful."

        def get_msg_quit(self, username):
            return "Goodbye."

        def get_perms(self, username):
            return "elradfmwMT"

        def has_perm(self, username, perm, path=None):
            return perm in self.get_perms(username)

    class WindowsAuthorizer(_Base, BaseWindowsAuthorizer):
        def __init__(
            self,
            global_perm="elradfmwMT",
            allowed_users=None,
            rejected_users=None,
            anonymous_user=None,
            anonymous_password=None,
            msg_login="Login successful.",
            msg_quit="Goodbye.",
        ):
            if allowed_users is None:
                allowed_users = []
            if rejected_users is None:
                rejected_users = []
            self.global_perm = global_perm
            self.allowed_users = allowed_users
            self.rejected_users = rejected_users
            self.anonymous_user = anonymous_user
            self.anonymous_password = anonymous_password
            self.msg_login = msg_login
            self.msg_quit = msg_quit
            self._dummy_authorizer = DummyAuthorizer()
            self._dummy_authorizer._check_permissions('', global_perm)
            _Base.__init__(self)
            # actually try to impersonate the user
            if self.anonymous_user is not None:
                self.impersonate_user(
                    self.anonymous_user, self.anonymous_password
                )
                self.terminate_impersonation(None)

        def override_user(
            self,
            username,
            password=None,
            homedir=None,
            perm=None,
            msg_login=None,
            msg_quit=None,
        ):
            _Base.override_user(
                self, username, password, homedir, perm, msg_login, msg_quit
            )
        def validate_authentication(self, username, password, handler):
            if username == "anonymous":
                if self.anonymous_user is None:
                    raise AuthenticationFailed(self.msg_anon_not_allowed)
                return
            if self.allowed_users and username not in self.allowed_users:
                raise AuthenticationFailed(self.msg_rejected_user % username)
            if self.rejected_users and username in self.rejected_users:
                raise AuthenticationFailed(self.msg_rejected_user % username)

            overridden_password = self._get_key(username, 'pwd')
            if overridden_password:
                if overridden_password != password:
                    raise AuthenticationFailed(self.msg_wrong_password)
            else:
                BaseWindowsAuthorizer.validate_authentication(
                    self, username, password, handler
                )

        def impersonate_user(self, username, password):
            if username == "anonymous":
                username = self.anonymous_user or ""
                password = self.anonymous_password or ""
            BaseWindowsAuthorizer.impersonate_user(self, username, password)

        @replace_anonymous
        def has_user(self, username):
            if self._is_rejected_user(username):
                return False
            return username in self._get_system_users()

        @replace_anonymous
        def get_home_dir(self, username):
            overridden_home = self._get_key(username, 'home')
            if overridden_home:
                home = overridden_home
            else:
                home = BaseWindowsAuthorizer.get_home_dir(self, username)
            return home
