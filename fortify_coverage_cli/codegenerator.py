"""Generate concrete abstract syntax trees based on source code strings."""

from fortify_coverage_cli import transform

from datetime import datetime

from enum import Enum

from typing import Union

import libcst as cst
from libcst import CSTNode
from libcst._nodes.statement import BaseCompoundStatement
from libcst._nodes.statement import SimpleStatementLine


class InstrumentationTypeSourceCode(str, Enum):
    """The predefined levels for source code based on instrumentation type."""

    TEST_SESSION_DOCSTRONG = "test_session_docstring"
    TEST_SESSION_NO_DOCSTRONG = "test_session_no_docstring"
    EMPTY_LINE = "empty_line"


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

    def get_fortify_comment_code(self) -> str:
        """Return the standard comment that goes along with fortify's instrumentation."""
        # define the standard code comment to include the name of the
        # module that added the instrumentation and full date-time details
        fortify_comment_code = (
            "# fortify-coverage instrumentation generated on"
            f" {datetime.now().strftime('%m/%d/%Y at %H:%M:%S')} by {self.name}\n"
        )
        return fortify_comment_code

    def get_fortify_import_test_session_fixture(self) -> str:
        """Return the import statement for the test session fixture."""
        # define the import statement for the session_setup_teardown fixture
        return "from fortify_coverage.fixture import session_setup_teardown\n\n"

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
        #         - line 2: import the session_setup_teardown from fortify_coverage module
        # Note: fortify_coverage package is not part of the fortify_coverage_cli package;
        # it is a separate package on which fortify_coverage_cli and a subject program depends
        multiple_line_import_statement_str = (
            self.get_fortify_comment_code()
            + self.get_fortify_import_test_session_fixture()
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
        #         - line 2: import the session_setup_teardown from fortify_coverage module
        # Note: fortify_coverage package is not part of the fortify_coverage_cli package;
        # it is a separate package on which fortify_coverage_cli and a subject program depends
        multiple_line_import_statement_str = (
            "\n" + self.get_fortify_comment_code()
            + self.get_fortify_import_test_session_fixture()
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
