"""Perform file operations."""

from pathlib import Path
from pathlib import PurePath
from shutil import rmtree
from typing import List

from discover_test_coverage import constants
from discover_test_coverage import output


def find_python_files(directory: Path) -> List[Path]:
    """Find all of the Python files in a specified directory."""
    # note that this function works for both test cases and
    # program files as long as the directory is specified;
    # with that said, this works by a convention that a developer
    # may not follow (i.e., tests could be inside program directories)
    all_python_files = sorted(directory.rglob(constants.wildcards.All_Python))
    return all_python_files


def find_python_files_not_conftest(directory: Path) -> List[Path]:
    """Find all of the Python files that are not a conftest.py file."""
    # create a list to store Python files that are not conftest.py
    not_conftest_file_list = []
    # find all of the Python files in the specified directory
    python_file_list = find_python_files(directory)
    # add to the not_conftest_file_list all files that
    # are not conftest.py according to their name
    for python_file in python_file_list:
        if python_file.name != "conftest.py":
            not_conftest_file_list.append(python_file)
    return not_conftest_file_list


def find_conftest_files(directory: Path) -> List[Path]:
    """Find all of the Python files that are a conftest.py file."""
    # create a list of all the conftest.py files
    conftest_file_list = []
    # find all of the Python files in the specified directory
    python_file_list = find_python_files(directory)
    # add to the conftest_file_list all files that are
    # conftest.py according to their name
    for python_file in python_file_list:
        if python_file.name == "conftest.py":
            conftest_file_list.append(python_file)
    return conftest_file_list


def elide_path(path, maximum_parts: int = 4, include_up_to: int = 5):
    """Elide a path so that it supports compact display."""
    parts = list(PurePath(path).parts)
    # if the path is too long (i.e., has more than maximum_parts parts),
    # then "elide" it by omitting details from the "middle" of the path,
    # starting at the part of the path at include_up_to, going up to but
    # not including the name of the file that should always display
    if len(parts) >= maximum_parts:
        parts[include_up_to:-1] = [constants.markers.Ellipse]
    return PurePath(*parts)


def create_hidden_directory(
    containing_directory: Path, directory: Path, delete_path: bool = True
) -> Path:
    """Create a hidden directory."""
    output.logger.debug(f"Hiding in containing directory: {containing_directory}")
    output.logger.debug(f"Hiding the directory with name: {directory.name}")
    # create a hidden directory (i.e., a directory with name "program" will
    # lead to creation of a hidden directory called ".program")
    hidden_directory = Path(
        containing_directory / Path(constants.markers.Hidden + str(directory.name))
    )
    # delete the hidden directory if it already exists
    if hidden_directory.exists() and hidden_directory.is_dir() and delete_path:
        rmtree(hidden_directory)
    # create the hidden directory for storing instrumentation
    # note that mkdir throws an exception if the directory exists;
    # since it was already deleted, the exception should not occur
    hidden_directory.mkdir(parents=True)
    output.logger.debug(f"Created the hidden directory: {hidden_directory}")
    return hidden_directory


def get_hidden_directory(
    containing_directory: Path,
    directory: Path,
) -> Path:
    """Create a hidden directory."""
    output.logger.debug(f"Hiding in containing directory: {containing_directory}")
    output.logger.debug(f"Hiding the directory with name: {directory.name}")
    # access a hidden directory (i.e., a directory with name "program" will
    # lead to creation of a hidden directory called ".program")
    hidden_directory = Path(
        containing_directory / Path(constants.markers.Hidden + str(directory.name))
    )
    output.logger.debug(f"Accessing the hidden directory: {hidden_directory}")
    return hidden_directory
