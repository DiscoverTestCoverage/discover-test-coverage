"""Perform file operations."""

from fortify_coverage_cli import constants
from fortify_coverage_cli import output

from pathlib import Path
from pathlib import PurePath

from typing import List


def find_python_files(program_directory: Path) -> List[Path]:
    """Find all of the Python files in a specified directory."""
    all_python_files = sorted(program_directory.rglob(constants.wildcards.All_Python))
    return all_python_files


def elide_path(path, maximum_parts: int = 4, include_up_to: int = 5):
    parts = list(PurePath(path).parts)
    # if the path is too long (i.e., has more than maximum_parts parts),
    # then "elide" it by omitting details from the "middle" of the path,
    # starting at the part of the path at include_up_to, going up to but
    # not including the name of the file that should always display
    if len(parts) >= maximum_parts:
        parts[include_up_to:-1] = ["..."]
    return PurePath(*parts)


def create_hidden_directory(containing_directory: Path, directory: Path) -> Path:
    """Create a hidden directory."""
    output.logger.debug(f"Hiding in containing directory: {containing_directory}")
    output.logger.debug(f"Hiding the directory with name: {directory.name}")
    # create a hidden directory (i.e., a directory with name "program" will
    # lead to creation of a hidden directory called ".program")
    hidden_directory = Path(
        containing_directory / Path(constants.markers.Hidden + str(directory.name))
    )
    hidden_directory.mkdir(parents=True, exist_ok=True)
    output.logger.debug(f"Created the hidden directory: {hidden_directory}")
    return hidden_directory
