"""Command-line interface for fortified coverage calculation."""

from fortify_coverage import coverage
from fortify_coverage_cli import debug
from fortify_coverage_cli import output
from fortify_coverage_cli import run
from fortify_coverage_cli import server
from fortify_coverage_cli import transform

from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def instrument_program(
    project_directory: Path = typer.Option(...),
    program_directory: Path = typer.Option(...),
    coverage_type: coverage.CoverageType = typer.Option(
        coverage.CoverageType.FUNCTION.value
    ),
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
    output.logger.debug(f"Adding instrumentation for {coverage_type}")
    # display the header
    output.print_header()
    # instrument all of the files in a program
    transform.transform_files_using_libcst(
        project_directory, program_directory, coverage_type
    )
    # display the footer
    output.print_footer()


@app.command()
def test(
    project_directory: Path = typer.Option(...),
    program_directory: Path = typer.Option(...),
    test_run_command: str = typer.Option(
        run.TestRunCommand.TEST.value, "--test-run-cmd"
    ),
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
    run.run_test_suite(project_directory, program_directory, test_run_command)


@app.command()
def log_server():
    """Run the logging server."""
    # display the header
    output.print_header()
    # display details about the server
    output.print_server()
    # run the server; note that this
    # syslog server receives debugging
    # information from fortify and must
    # be started in a separate process
    # before running any sub-command
    # of the fortify tool
    server.run_syslog_server()
