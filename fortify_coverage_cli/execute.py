"""DEPRECATED: Execute external applications and test suites."""

import pytest

from pathlib import Path


def run_test_suite_with_pytest(tests_directory: Path) -> None:
    """Execute the test suite a single time using Pytest."""
    pytest.main(["--trace-config"])
    pytest.main([str(tests_directory), "-s"])


# def run_test_suite_with_test_command(tests_directory: Path, test_command: str): -> None:
#     """Execute the test suite with a specified test command."""


def repeatedly_run_test_suite_with_pytest(
    tests_directory: Path, number_runs: int
) -> None:
    """Repeatedly execute the test suite a single time using Pytest."""
    run_count = 0
    while run_count < number_runs:
        run_test_suite_with_pytest(tests_directory)
