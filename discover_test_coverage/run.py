"""Run commands to execute commands of a subject."""

import os
import subprocess
from enum import Enum
from pathlib import Path
from shutil import copytree
from shutil import rmtree

from discover_test_coverage import constants
from discover_test_coverage import output


class TestRunCommand(str, Enum):
    """The predefined commands for running a test suite."""

    TEST = "poetry run pytest"
    TEST_OUTPUT = "poetry run pytest -s"
    TEST_FAIL_FAST = "poetry run pytest -x"
    TEST_FAIL_FAST_OUTPUT = "poetry run pytest -x -s"


def copytree_overwrite(from_path: Path, to_path: Path) -> None:
    """Copy from a path to a path, allowing an overwrite to occur if needed."""
    # note that this function is needed because copytree will, by default,
    # fail if you ask it to copy from_path to to_path and to_path exists
    # the path already exists and thus it needs to be removed before using copytree
    if os.path.exists(to_path):
        rmtree(to_path)
    # run the copytree to perform the directory copy
    copytree(from_path, to_path)


def run_test_suite(
    project_directory: Path,
    test_directory: Path,
    test_run_command: str,
    use_coverage_or_not: str,
) -> None:
    """Run the test suite with a provided command."""
    locals()["run_test_suite" + use_coverage_or_not]


def run_test_suite_without_coverage(
    project_directory: Path,
    test_directory: Path,
    test_run_command: str,
) -> None:
    """Run the test suite with a provided command with coverage monitoring."""
    output.logger.debug(f"Change into the project directory: {project_directory}")
    output.logger.debug(f"Preparing to run the test command: {test_run_command}")
    initial_current_working_directory = Path.cwd()
    # change into the directory for the specified project
    os.chdir(project_directory)
    # display a label in standard output about running the test suite
    output.print_test_start()
    # create the directory where tests are stored by default
    test_directory = Path(project_directory / test_directory)
    # run the test suite with the provided test execution command
    subprocess.run(test_run_command, shell=True)
    # display a label in standard output about finishing the test suite run
    output.print_test_finish()
    # return to the main working directory for the program
    os.chdir(initial_current_working_directory)


def prepare_for_coverage_monitoring(
    project_directory: Path, test_directory: Path
) -> Path:
    """Prepare to run the test suite with coverage monitoring."""
    # create the directory where tests are stored by default
    test_directory = Path(project_directory / test_directory)
    # create a backup directory for the original tests;
    # it is a hidden directory that ends with a label like "-backup"
    test_directory_backup = Path(
        project_directory
        / (constants.markers.Hidden + test_directory.name + constants.tests.Backup)
    )
    # create a hidden directory that will store the instrumented tests
    test_directory_instrumented = Path(
        project_directory / (constants.markers.Hidden + test_directory.name)
    )
    # copy the original test directory to the backup directory; this will
    # ensure that original test cases are not deleted during test execution
    copytree_overwrite(test_directory, test_directory_backup)
    # recursively remove the test directory and all of its contents
    rmtree(test_directory)
    # recursively copy the instrumented tests into the original test directory
    copytree_overwrite(test_directory_instrumented, test_directory)
    return test_directory_backup


def finalize_coverage_monitoring(test_directory: Path, test_directory_backup: Path) -> None:
    """Finalize the system after running test coverage monitoring."""
    # delete the test directory that contains the instrumented tests
    rmtree(test_directory)
    # return the original tests to the testing directory
    copytree_overwrite(test_directory_backup, test_directory)
    # delete the backup directory for the original tests
    rmtree(test_directory_backup)


def run_test_suite_with_coverage(
    project_directory: Path,
    test_directory: Path,
    test_run_command: str,
) -> None:
    """Run the test suite with a provided command and collect coverage."""
    output.logger.debug(f"Change into the project directory: {project_directory}")
    output.logger.debug(f"Preparing to run the test command: {test_run_command}")
    initial_current_working_directory = Path.cwd()
    # change into the directory for the specified project
    os.chdir(project_directory)
    # display a label in standard output about running the test suite
    output.print_test_start()
    test_directory_backup = prepare_for_coverage_monitoring(
        project_directory, test_directory
    )
    # run the test suite with the provided test execution command
    subprocess.run(test_run_command, shell=True)
    # display a label in standard output about finishing the test suite run
    output.print_test_finish()
    finalize_coverage_monitoring(test_directory, test_directory_backup)
    # return to the main working directory for the program
    os.chdir(initial_current_working_directory)
