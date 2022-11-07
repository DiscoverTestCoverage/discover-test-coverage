"""Configure logging and console output."""

import json
import logging
import logging.config
import logging.handlers
import os
import sys
from enum import Enum
from pathlib import Path

from rich.logging import RichHandler
from rich.traceback import install

from discover_test_coverage import constants


class Configuration(str, Enum):
    """The predefined values for the configuration file."""

    HOME = Path.home()
    DIRECTORY = ".discover/"
    FILE = "discover.ini"
    SEPARATOR = os.sep


def save_configuration(**configurations) -> None:
    """Save the configuration in the specified directory."""
    print("these are the configurations")
    print(configurations)
    # extract the string that contains the discover directory
    discover_dir = configurations["discover_dir"]
    discover_dir.mkdir(parents=True, exist_ok=True)
    discover_json_file_path = Path(discover_dir / "discover.json")
    discover_dir_str = str(discover_dir)
    configurations["discover_dir"] = discover_dir_str
    print("discover_dir")
    print(type(discover_dir))
    print(discover_dir)
    # save details about the coverage report inside of the
    # configurations dictionary so that the test coverage
    # monitoring instrumentation can pick it up and use it
    configurations["coverage_file"] = str(discover_dir) + "/coveragereport.json"
    configurations_str = json.dumps(configurations, indent=2)
    discover_json_file_path.touch()
    discover_json_file_path.write_text(configurations_str)


def configure_tracebacks() -> None:
    """Configure stack tracebacks arising from a crash to use rich."""
    install()


def configure_logging(
    debug_level: str = constants.logging.Default_Logging_Level,
    debug_dest: str = constants.logging.Default_Logging_Destination,
) -> logging.Logger:
    """Configure standard Python logging package."""
    # use the specified logger with the specified destination
    # by dynamically constructing the function to call and then
    # invoking it with the provided debug_dest parameter
    function_name = constants.logger.Function_Prefix + debug_dest
    configure_module = sys.modules[__name__]
    return getattr(configure_module, function_name)(debug_level)


def configure_logging_console(
    debug_level: str = constants.logging.Default_Logging_Level,
) -> logging.Logger:
    """Configure standard Python logging package to use rich."""
    # use the RichHandler to provide formatted
    # debugging output in the console
    logging.basicConfig(
        level=debug_level,
        format=constants.logging.Format,
        datefmt="[%X]",
        handlers=[RichHandler()],
    )
    # create a logger and then return it
    logger = logging.getLogger()
    return logger


def configure_logging_syslog(
    debug_level: str = constants.logging.Default_Logging_Level,
) -> logging.Logger:
    """Configure standard Python logging package to use syslog."""
    # use the SysLogHandler to send output to a localhost on a port
    syslog_handler = logging.handlers.SysLogHandler(
        address=(constants.server.Localhost, constants.server.Port)
    )
    logging.basicConfig(
        level=debug_level,
        format=constants.logging.Format,
        datefmt="[%X]",
        handlers=[syslog_handler],
    )
    # create a logger and then return it
    logger = logging.getLogger()
    return logger
