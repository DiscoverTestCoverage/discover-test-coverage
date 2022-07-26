"""Command-line interface for fortified coverage calculation."""

from pathlib import Path

import typer

from discover import debug
from discover import instrumentation
from discover import output
from discover import run
from discover import server
from discover import transform


def instrument_program(
    project_directory: Path = typer.Option(...),
    program_directory: Path = typer.Option(...),
    instrumentation_type: instrumentation.InstrumentationType = typer.Option(
        instrumentation.InstrumentationType.FUNCTION.value
    ),
    verbose: bool = typer.Option(False),
    debug_level: debug.DebugLevel = typer.Option(debug.DebugLevel.ERROR.value),
    debug_destination: debug.DebugDestination = typer.Option(
        debug.DebugDestination.CONSOLE.value, "--debug-dest"
    ),
):
    """Modify code of application and test suite."""
    # setup the console and the logger through output module
    output.setup(debug_level, debug_destination)
    output.logger.debug(f"Instrumenting the project in {project_directory}")
    output.logger.debug(f"Instrumenting program modules in {program_directory}")
    output.logger.debug(f"Adding instrumentation for {instrumentation_type}")
    # display the header
    output.print_header()
    # display details about configuration as
    # long as verbose output was requested
    output.print_diagnostics(
        verbose,
        debug_level=debug_level,
        debug_destination=debug_destination,
        instrumentation_type=instrumentation_type,
        project_directory=project_directory,
        program_directory=program_directory,
    )
    # instrument all of the files in a program
    transform.transform_files_using_libcst(
        project_directory, program_directory, instrumentation_type
    )
    # display the footer
    output.print_footer()


@app.command()
def instrument_tests(
    project_directory: Path = typer.Option(...),
    tests_directory: Path = typer.Option(...),
    instrumentation_type: instrumentation.InstrumentationType = typer.Option(
        instrumentation.InstrumentationType.FIXTURE.value
    ),
    verbose: bool = typer.Option(False),
    debug_level: debug.DebugLevel = typer.Option(debug.DebugLevel.ERROR.value),
    debug_destination: debug.DebugDestination = typer.Option(
        debug.DebugDestination.CONSOLE.value, "--debug-dest"
    ),
):
    """Modify code of application and test suite."""
    # setup the console and the logger through output module
    output.setup(debug_level, debug_destination)
    output.logger.debug(f"Instrumenting the project in {project_directory}")
    output.logger.debug(f"Instrumenting test files in {tests_directory}")
    output.logger.debug(f"Adding instrumentation for {instrumentation_type}")
    # display the header
    output.print_header()
    # display details about configuration as
    # long as verbose output was requested
    output.print_diagnostics(
        verbose,
        debug_level=debug_level,
        debug_destination=debug_destination,
        instrumentation_type=instrumentation_type,
        project_directory=project_directory,
        program_directory=tests_directory,
    )
    # instrument all of the files in a program
    transform.transform_files_using_libcst(
        project_directory, tests_directory, instrumentation_type
    )
    # display the footer
    output.print_footer()


@app.command()
def test(
    project_directory: Path = typer.Option(...),
    program_directory: Path = typer.Option(...),
    tests_directory: Path = typer.Option(...),
    test_run_command: str = typer.Option(
        run.TestRunCommand.TEST.value, "--test-run-cmd"
    ),
    verbose: bool = typer.Option(False),
    debug_level: debug.DebugLevel = typer.Option(debug.DebugLevel.ERROR.value),
    debug_destination: debug.DebugDestination = typer.Option(
        debug.DebugDestination.CONSOLE.value, "--debug-dest"
    ),
):
    """Run the program's test suite."""
    # setup the console and the logger through output module
    output.setup(debug_level, debug_destination)
    output.logger.debug(f"Testing the project in {project_directory}")
    output.logger.debug(f"Testing program modules in {program_directory}")
    # display the header
    output.print_header()
    # display details about configuration as
    # long as verbose output was requested
    output.print_diagnostics(
        verbose,
        debug_level=debug_level,
        debug_destination=debug_destination,
        test_run_command=test_run_command,
        project_directory=project_directory,
        program_directory=program_directory,
    )
    # run the test suite using Pytest
    run.run_test_suite(project_directory, tests_directory, test_run_command)


@app.command()
def log_server():
    """Run the logging server."""
    # display the header
    output.print_header()
    # display details about the server
    output.print_server()
    # run the server; note that this
    # syslog server receives debugging
    # information from discover.py and must
    # be started in a separate process
    # before running any sub-command
    # of the discover.py tool
    server.run_syslog_server()
