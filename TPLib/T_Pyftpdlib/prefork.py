import os
import random
import sys
import time
from binascii import hexlify

try:
    import multiprocessing
except ImportError:
    multiprocessing = None

from .log import logger


_task_id = None


def cpu_count():
    if multiprocessing is None:
        return 1
    try:
        return multiprocessing.cpu_count()
    except NotImplementedError:
        pass
    try:
        return os.sysconf("SC_NPROCESSORS_CONF")
    except (AttributeError, ValueError):
        pass
    return 1


def _reseed_random():
    try:
        seed = int(hexlify(os.urandom(16)), 16)
    except NotImplementedError:
        seed = int(time.time() * 1000) ^ os.getpid()
    random.seed(seed)


def fork_processes(number, max_restarts=100):
    assert _task_id is None
    if number is None or number <= 0:
        number = cpu_count()
    logger.info("starting %d pre-fork processes", number)
    children = {}

    def start_child(i):
        pid = os.fork()
        if pid == 0:
            # child process
            _reseed_random()
            global _task_id
            _task_id = i
            return i
        else:
            children[pid] = i
            return None

    for i in range(number):
        id = start_child(i)
        if id is not None:
            return id
    num_restarts = 0
    while children:
        try:
            pid, status = os.wait()
        except InterruptedError:
            continue
        if pid not in children:
            continue
        id = children.pop(pid)
        if os.WIFSIGNALED(status):
            logger.warning(
                "child %d (pid %d) killed by signal %d, restarting",
                id,
                pid,
                os.WTERMSIG(status),
            )
        elif os.WEXITSTATUS(status) != 0:
            logger.warning(
                "child %d (pid %d) exited with status %d, restarting",
                id,
                pid,
                os.WEXITSTATUS(status),
            )
        else:
            logger.info("child %d (pid %d) exited normally", id, pid)
            continue
        num_restarts += 1
        if num_restarts > max_restarts:
            raise RuntimeError("Too many child restarts, giving up")
        new_id = start_child(id)
        if new_id is not None:
            return new_id
    sys.exit(0)
