"""Transfer files."""

import shutil
from pathlib import Path
from typing import Callable

from rich.progress import BarColumn
from rich.progress import Progress
from rich.progress import TextColumn
from rich.table import Column

from discover_test_coverage import file
from discover_test_coverage import output


def transfer_files(
    project_directory_path: Path,
    program_directory: Path,
    file_finder: Callable,
) -> int:
    """Transfer a directory of files to a hidden directory derived from existing directory."""
    # create the fully qualified directory that contains the program's source code
    fully_qualified_program_directory = project_directory_path / program_directory
    output.logger.debug(fully_qualified_program_directory)
    # find all of the Python source code files for instrumentation
    program_files_list = file_finder(fully_qualified_program_directory)
    # configure a progress bar for visual display in the terminal window
    text_column = TextColumn("{task.description}", table_column=Column(ratio=1))
    bar_column = BarColumn(bar_width=None, table_column=Column(ratio=2))
    progress = Progress(text_column, bar_column, expand=True)
    # create a hidden directory that can store the instrumented files
    hidden_program_directory = file.get_hidden_directory(
        project_directory_path, project_directory_path / program_directory
    )
    # copy each of the individual files in the specified directory,
    # updating progress bar after each one of the transfers
    if len(program_files_list) > 0:
        with Progress() as progress:
            # create the task label for the progress bar
            task = progress.add_task(
                ":sparkles: Copy test files",
                total=len(program_files_list),
            )
            # iteratively transfer the source code for each file
            for program_file in program_files_list:
                progress.console.print(f"Copying {file.elide_path(program_file)}")
                # create a new pathlib Path object for the module in the hidden directory
                instrumented_file = Path(hidden_program_directory / program_file.name)
                # copy the existing file to the "instrumented" one in hidden directory
                shutil.copy(program_file, instrumented_file)
                # indicate that the current task is finished to advance progress bar
                progress.advance(task)
    return len(program_files_list)
