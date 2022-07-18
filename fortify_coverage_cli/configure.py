"""Configure logging and console output."""

from fortify_coverage_cli import constants

import logging
import logging.config
import logging.handlers

from rich.logging import RichHandler
from rich.traceback import install


def configure_tracebacks() -> None:
    """Configure stack tracebacks arising from a crash to use rich."""
    install()


def configure_logging(
    debug_level: str = constants.logging.Default_Logging_Level,
    debug_dest: str = constants.logging.Default_Logging_Destination,
) -> logging.Logger:
    """Configure standard Python logging package."""
    if debug_dest == constants.logging.Console_Logging_Destination:
        return configure_logging_rich(debug_level)
    return configure_logging_syslog(debug_level)


def configure_logging_rich(
    debug_level: str = constants.logging.Default_Logging_Level,
) -> logging.Logger:
    """Configure standard Python logging package to use rich."""
    logging.basicConfig(
        level=debug_level,
        format=constants.logging.Format,
        datefmt="[%X]",
        handlers=[RichHandler()],
    )
    # create a logger and then return it
    logger = logging.getLogger("fortify-richlog")
    return logger


def configure_logging_syslog(
    debug_level: str = constants.logging.Default_Logging_Level,
) -> logging.Logger:
    """Configure standard Python logging package to use syslog."""
    syslog_handler = logging.handlers.SysLogHandler(address=("127.0.0.1", 2525))
    logging.basicConfig(
        level=debug_level,
        format=constants.logging.Format,
        datefmt="[%X]",
        handlers=[syslog_handler],
    )
    # create a logger and then return it
    logger = logging.getLogger("fortify-syslog")
    return logger
