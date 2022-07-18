"""Run commands to execute commands of a subject."""

from fortify_coverage_cli import output

import os
import subprocess

from enum import Enum
from pathlib import Path


class TestRunCommand(str, Enum):
    """The predefined commands for running a test suite."""

    TEST = "poetry run pytest"
    TEST_FAIL_FAST = "poetry run pytest -x"


def run_test_suite(
    project_directory: Path, program_directory: Path, test_run_command: str
) -> None:
    """Run the test suite with a provided command."""
    output.logger.debug(f"Change into the project directory: {project_directory}")
    initial_current_working_directory = Path.cwd()
    os.chdir(project_directory)
    output.print_test_start()
    subprocess.run(test_run_command, shell=True)
    output.print_test_finish()
    os.chdir(initial_current_working_directory)
