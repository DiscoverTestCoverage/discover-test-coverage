"""Perform logging and/or console output."""

from fortify_coverage_cli import configure
from fortify_coverage_cli import debug
from fortify_coverage_cli import constants

from rich.console import Console

logger = None
console = Console()


def setup(
    debug_level: debug.DebugLevel, debug_destination: debug.DebugDestination
) -> None:
    """Perform the setup steps and return a Console for terminal-based display."""
    global logger
    # configure the use of rich for improved terminal output:
    # --> rich-based tracebacks to enable better debugging on program crash
    configure.configure_tracebacks()
    # --> logging to keep track of key events during program execution;
    # pass in the actual values as strings instead of using class enums
    logger = configure.configure_logging(debug_level.value, debug_destination.value)


def print_diagnostics(verbose, **configurations) -> None:
    """Display all variables input to the function."""
    global console
    # display diagnostic information for each configuration keyword argument
    if verbose:
        console.print(":sparkles: Configured with these parameters:")
        # iterate through each of the configuration keyword arguments
        for configuration in configurations:
            # print the name and the value of the keyword argument
            console.print(
                f"{constants.markers.Indent}{configuration} = {configurations[configuration]}"
            )
        console.print()


def print_header() -> None:
    """Display tool details in the header."""
    global console
    console.print()
    console.print(
        constants.fortify.Emoji + constants.markers.Space + constants.fortify.Tagline
    )
    console.print(constants.fortify.Website)
    console.print()


def print_server() -> None:
    """Display server details in the header."""
    global console
    console.print(constants.output.Syslog)
    console.print()


def print_test_start() -> None:
    """Display details about the test run."""
    global console
    console.print(constants.output.Test_Start)
    console.print()


def print_test_finish() -> None:
    """Display details about the test run."""
    global console
    console.print()
    console.print(":sparkles: Finish running test suite for the specified program")
    console.print()


def print_footer() -> None:
    """Display concluding details in the footer."""
    global console
    console.print()
