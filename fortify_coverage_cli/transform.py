"""Instrument an application and its test suite using libCST transformers."""

from fortify_coverage_cli.transformers import functioncoverage
from fortify_coverage_cli.transformers import testfixtures

from fortify_coverage_cli import file
from fortify_coverage_cli import instrumentation
from fortify_coverage_cli import output

from pathlib import Path

import difflib

from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn

import libcst as cst
from libcst import Module

# global configuration of the source tree
# that libCST creates through initial parse;
# declared here so that it can be accessed
# by various visit or leave methods after
# the initial construction of CAST
source_tree_configuration = None


# TODO: move the instrumentationtype?
class InstrumentationTypeGenerator(object):
    def __init__(self, type) -> None:
        self.type = type

    def generate(self, *args, **kwgs) -> cst.CSTTransformer:
        return getattr(self, "generate_transformer_{}".format(self.type))(*args, **kwgs)

    def generate_transformer_function(self) -> cst.CSTTransformer:
        transformer = functioncoverage.FortifiedFunctionCoverageTransformer()
        return transformer

    def generate_transformer_branch(self) -> None:
        print("TODO: branch transformer")

    def generate_transformer_fixture(self) -> cst.CSTTransformer:
        transformer = testfixtures.TestFixtureTransformer()
        return transformer


def create_libcst_transformer(
    instrumentation_type: instrumentation.InstrumentationType,
) -> cst.CSTTransformer:
    """Create the correct transformer based on the requested type of instrumentation.."""
    instrumentation_type_generator = InstrumentationTypeGenerator(instrumentation_type)
    libcst_transformer = instrumentation_type_generator.generate()
    output.logger.debug(libcst_transformer)
    output.logger.debug(type(libcst_transformer))
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
    single_file_text = program_file.read_text()
    output.logger.debug(single_file_text)
    source_tree = cst.parse_module(single_file_text)
    # TODO: check the coverage_type variable and run the
    # requested type of coverage transformation
    # transformer = functioncoverage.FortifiedFunctionCoverageTransformer()
    # transformer = testfixtures.TestFixtureTransformer()
    transformer = create_libcst_transformer(instrumentation_type)
    create_libcst_transformer(instrumentation_type)
    source_tree_configuration = source_tree.config_for_parsing
    modified_tree = source_tree.visit(transformer)
    # modified_modified_tree = modified_tree.with_changes(
    #     body=(
    #         cst.parse_statement(
    #             "from fortify import sample # instrument_file",
    #             config=modified_tree.config_for_parsing,
    #         ),
    #         *modified_tree.body,
    #     ),
    # )
    # output.logger.debug("Entire modified source code:")
    # output.logger.debug(modified_modified_tree.code)
    output.logger.debug("Diff of the modified source code:")
    output.logger.debug(
        "".join(
            difflib.unified_diff(
                single_file_text.splitlines(1), modified_tree.code.splitlines(1)
            )
        )
    )
    output.logger.debug(f"Type: {type(modified_tree)}")
    return modified_tree
