"""Interface for default modules os and json"""

# Standard modules
import json
import os
from logging import Logger
from typing import IO


def open_file(path: str, mode: str, logger: Logger = None, *, create: bool = True, encoding: str = None) -> IO:
    """Open a file

    path: the path of the file
    mode: the mode to use to open the file
    logger: the logger to log information and warnings
    create: do create directories and file, if not existent
    encoding: the encoding to use for the file
    """

    if create and not exists(directory(path)) and not directory(path) == "":
        if logger:
            logger.info(f"Doesn't found directory '{directory(path)}'! Create directory ...")
        os.makedirs(directory(path))

    try:

        if logger:
            logger.debug(f"Open file '{path}' with mode '{mode}' ...")
        return open(path, mode, encoding=encoding)

    except OSError:

        if create:
            if logger:
                logger.info(f"Failed to open file '{path}'! Create and try to load it again ...")
            open(path, "w", encoding=encoding).close()
            return open_file(path, mode, logger, create=False)
        else:
            if logger:
                logger.warning(f"Failed to open file '{path}'! Raise error ...")
            raise


def open_utf8(path: str, mode: str, logger: Logger = None, *, create: bool = True) -> IO:
    """Open a file with UTF-8 encoding

    path: the path of the file
    mode: the mode to use to open the file
    logger: the logger to log information and warnings
    create: do create directories and file, if not existent
    """

    return open_file(path, mode, logger, create=create, encoding="utf-8")


def load_json(path: str, logger: Logger = None, *, create: bool = True) -> dict:
    """Load a json file to a dictionary

    path: the path of the file
    logger: the logger to log information and warnings
    create: do create directories and file, if not existent
    """

    if not create and not exists(path):
        logger.warning(f"Doesn't found file '{path}'! Continue with empty dictionary ...")
        return {}

    try:

        with open_utf8(path, "r", logger) as f:
            return json.load(f)

    except json.JSONDecodeError:

        logger.warning(f"Failed to decode file '{path}' to json! Continue with empty dictionary ...")
        return {}


def save_json(path: str, data: dict, logger: Logger = None) -> None:
    """Load a json file to a dictionary

    path: the path of the file
    data: the dictionary to save
    logger: the logger to log information and warnings
    """

    with open_utf8(path, "w", logger) as f:
        json.dump(data, f, indent=4, separators=(', ', ': '))


def delete(path: str, logger: Logger = None, *, ignore_error: bool = False) -> None:
    """Delete a file"""

    if logger:
        logger.debug(f"Delete file '{path}' ...")

    try:
        os.remove(path)
    except OSError:
        if not ignore_error:
            if logger:
                logger.warning(f"Failed to delete file '{path}'! Raise error ...")
            raise
        if logger:
            logger.info(f"Failed to delete file '{path}'!")


def make_dir(path: str, logger: Logger = None, *, parent: bool = True, ignore_error: bool = False) -> None:
    """Make a directory"""

    if logger:
        logger.debug(f"Make directory at '{path}' ...")

    try:
        if parent:
            os.makedirs(path, exist_ok=True)
        else:
            os.mkdir(path)
    except OSError:
        if not ignore_error:
            if logger:
                logger.warning(f"Failed to make directory at '{path}'! Raise error ...")
            raise
        if logger:
            logger.info(f"Failed to make directory at '{path}'!")


def remove_dir(path: str, logger: Logger = None, *, parent: bool = False, ignore_error: bool = False) -> None:
    """Remove a directory"""

    if logger:
        logger.debug(f"Delete directory at '{path}' ...")

    try:
        if parent:
            os.removedirs(path)
        else:
            os.rmdir(path)
    except OSError:
        if not ignore_error:
            if logger:
                logger.warning(f"Failed to remove directory at '{path}'! Raise error ...")
            raise
        if logger:
            logger.info(f"Failed to remove directory at '{path}'!")


def exists(path: str) -> bool:
    """Check file existence"""

    return os.path.exists(path)


def name(path: str) -> str:
    """Get the basename of a path"""

    return os.path.basename(path)


def directory(path: str) -> str:
    """Get the directory of a path"""

    return os.path.dirname(path)


def file_type(path: str) -> str:
    """Get the type of a file"""

    return name(path).split(".")[-1]


def file_name(path: str) -> str:
    """Get the name of a file without file extension"""

    return ".".join(name(path).split(".")[0:-2]) if len(name(path)) > 1 else ""


def is_file(path: str) -> bool:
    """Is file"""

    return os.path.isfile(path)


def is_dir(path: str) -> bool:
    """Is directory"""

    return os.path.isdir(path)


def join(dir_path: str, filename: str) -> str:
    """Join a directory path with a filename"""

    return os.path.join(dir_path, filename)


def rename(old_path: str, new_path: str, logger: Logger = None) -> None:
    """Rename a file or path"""

    if logger:
        logger.debug(f"Rename '{old_path}' to '{new_path}' ...")

    os.rename(old_path, new_path)


def dir_size(path: str, logger: Logger = None) -> int:
    """Get the size of a directory"""

    size = 0

    try:

        if logger:
            logger.debug(f"Get the size of '{path}' ...")

        for entry in os.scandir(path):

            if entry.is_file():
                size += file_size(entry.path)
            elif entry.is_dir():
                size += dir_size(entry.path, logger)

    except PermissionError:
        if logger:
            logger.info(f"Failed to get the size of '{path}'! Unresolved permission! Continue with 0 ...")
        return 0
    except OSError:
        if logger:
            logger.warning(f"Failed to get the size of '{path}'! Unexpected error! Continue with 0 ...")
        return 0

    return size


def file_size(path: str) -> int:
    """Get the size of a file"""

    return os.path.getsize(path)


def format_size_1000(size: int) -> str:
    """Format a size with a factor of 1000"""

    for i in ["", "K", "M", "G", "T", "P"]:

        if size < 1000:
            return f"{size:.2f}{i}B"

        size /= 1000

    return f"{size:.2f}EB"


def format_size_1024(size: int) -> str:
    """Format a size with a factor of 1024"""

    for i in ["", "Ki", "Mi", "Gi", "Ti", "Pi"]:

        if size < 1024:
            return f"{size:.2f}{i}B"

        size /= 1024

    return f"{size:.2f}EiB"
