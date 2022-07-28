"""Command-line interface for fortified coverage calculation."""

from pathlib import Path

import typer

from discover_test_coverage import debug
from discover_test_coverage import file
from discover_test_coverage import instrumentation
from discover_test_coverage import output
from discover_test_coverage import run
from discover_test_coverage import server
from discover_test_coverage import transfer
from discover_test_coverage import transform

# create a typer object
# for command-line interface
app = typer.Typer()


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
        project_directory,
        program_directory,
        instrumentation_type,
        file.find_python_files,
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
    # instrument all of the conftest.py files in a program; note
    # that these are normally in the tests/ directory but can,
    # in fact, be at any location in a project
    transformed_file_count = transform.transform_files_using_libcst(
        project_directory,
        tests_directory,
        instrumentation_type,
        file.find_conftest_files
    )
    # there were no conftest.py files that were found and then
    # instrumented and thus one needs to be created and then
    # copied to the hidden directory location for the tests
    if transformed_file_count == 0:
        print("need to copy one over!")
    # add a blank line between the status outputs in the console
    # for the two different types of tasks
    output.console.print()
    # transfer the test from the program's test directory to
    # the hidden directory that contains the instrumented conftest.py
    # file (and any other instrumented tests that were needed)
    transformed_file_count = transfer.transfer_files(
        project_directory,
        tests_directory,
        file.find_python_files_not_conftest
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
    # run the test suite using Pytest without collect coverage information;
    # this run will not use instrumented program and/or test source code
    run.run_test_suite_with_optional_coverage(
        project_directory, tests_directory, test_run_command, False
    )


@app.command()
def test_coverage(
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
    """Run the program's test suite and collect code coverage."""
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
    # run the test suite using Pytest without collect coverage information;
    # this run will not use instrumented program and/or test source code
    run.run_test_suite_with_optional_coverage(
        project_directory, tests_directory, test_run_command, True
    )


@app.command()
def start_log_server():
    """Start the logging server."""
    # display the header
    output.print_header()
    # display details about the server
    output.print_server()
    # run the server; note that this
    # syslog server receives debugging
    # information from discover-test-coverage
    # and must be started in a separate process
    # before running any sub-command
    # of the discover-test-coverage tool
    server.start_syslog_server()
