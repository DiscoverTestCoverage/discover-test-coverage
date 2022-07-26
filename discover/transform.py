"""Instrument an application and its test suite using libCST transformers."""

import difflib
from pathlib import Path

import libcst as cst
from libcst import Module
from rich.progress import BarColumn
from rich.progress import Progress
from rich.progress import TextColumn
from rich.table import Column

from discover import file
from discover import instrumentation
from discover import output
from discover import transformergenerator

# global configuration of the source tree
# that libCST creates through initial parse;
# declared here so that it can be accessed
# by various visit or leave methods after
# the initial construction of CAST
source_tree_configuration = None


def create_libcst_transformer(
    instrumentation_type: instrumentation.InstrumentationType,
) -> cst.CSTTransformer:
    """Create the correct transformer based on the requested type of instrumentation.."""
    # create a TransformerGenerator that knows how to create a transformer subclass
    # based on the type on the requested type of instrumentation
    instrumentation_type_generator = transformergenerator.TransformerGenerator(
        instrumentation_type
    )
    # generate the requested type of transformer
    libcst_transformer = instrumentation_type_generator.generate()
    output.logger.debug(f"Created the transformer: {type(libcst_transformer)}")
    return libcst_transformer


def transform_files_using_libcst(
    project_directory_path: Path,
    program_directory: Path,
    instrumentation_type: instrumentation.InstrumentationType,
) -> None:
    """Transform directory of files by adding instrumentation."""
    global progress
    # create the fully qualified directory that contains the program's source code
    fully_qualified_program_directory = project_directory_path / program_directory
    output.logger.debug(fully_qualified_program_directory)
    # find all of the Python source code files for instrumentation
    program_files_list = file.find_python_files(fully_qualified_program_directory)
    # configure a progress bar for visual display in the terminal window
    text_column = TextColumn("{task.description}", table_column=Column(ratio=1))
    bar_column = BarColumn(bar_width=None, table_column=Column(ratio=2))
    progress = Progress(text_column, bar_column, expand=True)
    # create a hidden directory that can store the instrumented files
    hidden_program_directory = file.create_hidden_directory(
        project_directory_path, project_directory_path / program_directory
    )
    # instrument each of the individual files in the program, updating progress bar
    with Progress() as progress:
        # create the instrumentation task label for the progress bar
        task = progress.add_task(
            f":sparkles: Add {instrumentation_type} instrumentation",
            total=len(program_files_list),
        )
        # iteratively transform the source code for each of the program files
        for program_file in program_files_list:
            progress.console.print(f"Instrumenting {file.elide_path(program_file)}")
            # instrument the current program file for the specific coverage type
            instrumented_module = transform_file_using_libcst(
                program_file, instrumentation_type
            )
            # create a new pathlib Path object for the instrumented module
            instrumented_file = Path(hidden_program_directory / program_file.name)
            instrumented_file.write_text(instrumented_module.code)
            # indicate that the current task is finished to advance progress bar
            progress.advance(task)


def transform_file_using_libcst(
    program_file: Path,
    instrumentation_type: instrumentation.InstrumentationType,
) -> Module:
    """Transform specified file by adding instrumentation for fortified coverage."""
    global source_tree_configuration
    # extract the source code from the file so that it can be instrumented
    single_file_text = program_file.read_text()
    # use libcst to parse the source code of the file
    source_tree = cst.parse_module(single_file_text)
    # use the helper function to create the correct type of transformer
    # that uses libcst to instrumented the program file
    transformer = create_libcst_transformer(instrumentation_type)
    source_tree_configuration = source_tree.config_for_parsing
    # visit the source code using the constructed transformer
    # so that the instrumentation exists in the modified tree
    modified_tree = source_tree.visit(transformer)
    output.logger.debug("Diff of the modified source code:")
    output.logger.debug(
        "".join(
            difflib.unified_diff(
                single_file_text.splitlines(1), modified_tree.code.splitlines(1)  # type: ignore
            )
        )
    )
    return modified_tree
