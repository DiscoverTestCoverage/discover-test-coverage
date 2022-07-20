"""Run commands to execute commands of a subject."""

from fortify_coverage_cli import output

import os
import subprocess

from enum import Enum
from pathlib import Path
from shutil import copytree
from shutil import rmtree


class TestRunCommand(str, Enum):
    """The predefined commands for running a test suite."""

    TEST = "poetry run pytest"
    TEST_FAIL_FAST = "poetry run pytest -x"


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
) -> None:
    """Run the test suite with a provided command."""
    output.logger.debug(f"Change into the project directory: {project_directory}")
    initial_current_working_directory = Path.cwd()
    os.chdir(project_directory)
    output.print_test_start()
    test_directory = Path(project_directory / test_directory)
    test_directory_backup = Path(
        project_directory / ("." + test_directory.name + "-backup")
    )
    test_directory_instrumented = Path(project_directory / ("." + test_directory.name))
    copytree_overwrite(test_directory, test_directory_backup)
    rmtree(test_directory)
    copytree_overwrite(test_directory_instrumented, test_directory)
    subprocess.run(test_run_command, shell=True)
    output.print_test_finish()
    rmtree(test_directory)
    copytree_overwrite(test_directory_backup, test_directory)
    rmtree(test_directory_backup)
    os.chdir(initial_current_working_directory)
