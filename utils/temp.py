import os
import sys


class PathNotFound(Exception):
    pass


class PathNotExist(Exception):
    pass


def get_temp_path() -> str:
    platform = sys.platform

    if platform.startswith("linux"):
        # TODO
        temp_path = "/tmp"
    elif platform.startswith("win32"):
        temp_path = os.getenv("TEMP")
    elif platform.startswith("darwin"):
        temp_path = os.getenv("TMPDIR")
    else:
        raise PathNotFound("Not found temp path on platform '{0}'".format(platform))

    if not os.path.exists(temp_path):
        raise PathNotExist("Not exist {0}".format(temp_path))

    return temp_path
