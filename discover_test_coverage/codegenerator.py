"""Generate concrete abstract syntax trees based on source code strings."""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Union

import libcst as cst
from libcst import CSTNode
from libcst._nodes.statement import BaseCompoundStatement
from libcst._nodes.statement import SimpleStatementLine

from discover_test_coverage import constants
from discover_test_coverage import transform


class InstrumentationTypeSourceCode(str, Enum):
    """The predefined levels for source code based on instrumentation type."""

    TEST_SESSION_DOCSTRONG = "test_session_docstring"
    TEST_SESSION_NO_DOCSTRONG = "test_session_no_docstring"
    EMPTY_LINE = "empty_line"


def get_discover_comment_code(name) -> str:
    """Return the standard comment that goes along with fortify's instrumentation."""
    # define the standard code comment to include the name of the
    # module that added the instrumentation and full date-time details
    discover_comment_code = (
        "# discover-test-coverage instrumentation generated on"
        f" {datetime.now().strftime('%m/%d/%Y at %H:%M:%S')} by {name}\n"
    )
    return discover_comment_code


def get_testfixture_start_import() -> str:
    """Return the import statement for the test session fixture."""
    # define the import statement for all of the test fixtures
    return "from libdtc.testfixture import *\n"


def create_instrumented_conftest_file(
    project_directory: Path, test_directory: Path
) -> None:
    """Create an instrumented conftest.py file in specified directory."""
    # create a pathlib Path object for the conftest.py file that will
    # be stored in the main test directory for the project
    conftest_path = Path(constants.tests.Conftest)
    initial_conftest_file = Path(project_directory / test_directory / conftest_path)
    # create a fully qualified name of this function in this module
    # so that this detail can be displayed in the generated comment
    comment_name = (
        str(__name__)
        + constants.markers.Dot
        + str(create_instrumented_conftest_file.__qualname__)
    )
    # create the entire text string that will be written to the
    # conftest.py file; there are two lines in this string
    # Line 1: comment explaining the instrumentation
    # Line 2: the import for all of the test fixtures
    full_code_text = (
        get_discover_comment_code(comment_name)
        + constants.markers.Newline
        + get_testfixture_start_import()
    )
    initial_conftest_file.write_text(full_code_text)


def delete_instrumented_conftest_file(
    project_directory: Path, test_directory: Path
) -> None:
    """Delete an instrumented conftest.py file in specified directory."""
    # create a pathlib Path object for the conftest.py file
    conftest_path = Path(constants.tests.Conftest)
    # create a fully qualified conftest.py file in the test directory of project
    initial_conftest_file = Path(project_directory / test_directory / conftest_path)
    # unlink the file, which causes the file to be removed from directory
    initial_conftest_file.unlink()


class InstrumentedSourceCodeGenerator(object):
    """Use a form of single dispatch to generate concrete abstract syntax trees."""

    def __init__(self, code_type, name) -> None:
        """Construct a new TransformerGenerator with the requested type of transformer."""
        self.code_type = code_type
        self.name = name

    @staticmethod
    def create_parsed_statement(import_statement):
        """Create a parsed statement out of the provided Python source code."""
        import_statement = cst.parse_statement(
            import_statement,
            config=transform.source_tree_configuration,
        )
        return import_statement

    def generate(
        self, *args, **kwgs
    ) -> Union[CSTNode, SimpleStatementLine, BaseCompoundStatement]:
        """Generate by dispatch a concrete abstract syntax tree by needed instrumentation."""
        # call the function with the name that starts with the word "generate"
        # and then finishes with the specific type of source code needed
        return getattr(self, "generate_{}".format(self.code_type))(*args, **kwgs)

    def generate_test_session_no_docstring(
        self,
    ) -> Union[CSTNode, SimpleStatementLine, BaseCompoundStatement]:
        """Generate a concrete abstract syntax tree for importing test fixture when no docstring."""
        # construct the import statement that will import the test fixtures:
        # -- session_setup_teardown: initializes coverage tracking and saves it
        # construct the source code as a string
        #         - line 1: comment showing when instrumentation was generated and by what
        #         - line 2: import the session_setup_teardown from discover_test_coverage module
        # Note: discover_test_coverage package is not part of the discover package;
        # it is a separate package on which discover and a subject program depends
        multiple_line_import_statement_str = (
            get_discover_comment_code(self.name) + get_testfixture_start_import()
        )
        return InstrumentedSourceCodeGenerator.create_parsed_statement(
            multiple_line_import_statement_str
        )

    def generate_test_session_docstring(
        self,
    ) -> Union[CSTNode, SimpleStatementLine, BaseCompoundStatement]:
        """Generate a concrete abstract syntax tree for importing test fixture when docstring."""
        # construct the import statement that will import the test fixtures:
        # -- session_setup_teardown: initializes coverage tracking and saves it
        # construct the source code as a string
        #         - line 0: an extra newline before the other generated code
        #         - line 1: comment showing when instrumentation was generated and by what
        #         - line 2: import the session_setup_teardown from discover_test_coverage module
        # Note: discover_test_coverage package is not part of the discover package;
        # it is a separate package on which discover and a subject program depends
        multiple_line_import_statement_str = (
            "\n" + get_discover_comment_code(self.name) + get_testfixture_start_import()
        )
        return InstrumentedSourceCodeGenerator.create_parsed_statement(
            multiple_line_import_statement_str
        )

    def generate_empty_line(
        self,
    ) -> Union[CSTNode, SimpleStatementLine, BaseCompoundStatement]:
        """Generate a concrete abstract syntax tree for an empty line."""
        # construct an empty line in the libcst format
        empty_line = cst.EmptyLine()
        return empty_line
