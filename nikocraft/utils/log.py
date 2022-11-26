"""Interface for standard module logging"""

# Standard modules
import logging
import os
import sys

# Local modules
from . import file


def setup_log_directory(path: str, file_limit: int = 10) -> None:
    """Make the log directory and delete old log files

    path: the log directory path
    file_limit: how many old log files to keep
    """

    # Make the directory
    file.make_dir(path)

    # Delete old log files
    log_files = []
    for entry in os.listdir(path):
        if file.is_file(file.join(path, entry)):
            if file.file_type(entry) == "log":
                log_files.append(entry)
    if len(log_files) > file_limit:
        for i in range(file_limit, len(log_files)):
            os.remove(file.join(path, log_files[i - file_limit]))


def setup_log_file(path: str, head: str, print_head: bool = True) -> None:
    """Create the log file and write the head (additionally print the head to console)

    path: the log file path
    head: a head of the application (for example for a description, version, author ...)
    print_head: print the head to console
    """

    # Print the head
    if print_head:
        print(head)

    # Create and open the file to write the head
    with file.open_utf8(path, "w") as f:
        f.write(head + "\n")


def create_logger(path: str, name: str, level: int, *, log_date: bool = True, log_thread: bool = False, log_custom: str = "", log_custom_date: str = "") -> logging.Logger:
    """Create the logger

    path: the log file path
    name: the name of the logger
    level: the minimum level of the logs to show
    log_date: show the date (if no custom format)
    log_thread: show the thread name (if no custom format)
    log_custom: custom format (default format if empty string)
    log_custom_date: custom date format (default date format if empty string)
    """

    # Define format
    log_format = logging.Formatter(f"[%(asctime)s] [%(name)s{' - %(threadName)s' if log_thread else ''}] [%(levelname)s] %(message)s" if log_custom == "" else log_custom,
                                   datefmt=('%d/%b/%y %H:%M:%S' if log_date else '%H:%M:%S') if log_custom_date == "" else log_custom_date)

    # Setup handler
    log_handler_file = logging.FileHandler(path, encoding="utf-8")
    log_handler_console = logging.StreamHandler(sys.stdout)
    log_handler_file.setFormatter(log_format)
    log_handler_console.setFormatter(log_format)

    # Create logger
    logger = logging.Logger(name, level)
    logger.addHandler(log_handler_file)
    logger.addHandler(log_handler_console)

    # Return logger
    return logger
