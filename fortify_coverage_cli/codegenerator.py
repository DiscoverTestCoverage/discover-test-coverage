"""Generate concrete abstract syntax trees based on source code strings."""

from fortify_coverage_cli import transform

from datetime import datetime

from enum import Enum

from typing import Union

import libcst as cst
from libcst._nodes.statement import BaseCompoundStatement, SimpleStatementLine


class InstrumentationTypeSourceCode(str, Enum):
    """The predefined levels for source code based on instrumentation type."""

    TEST_SESSION_DOCSTRONG = "test_session_docstring"
    TEST_SESSION_NO_DOCSTRONG = "test_session_no_docstring"


class InstrumentedSourceCodeGenerator(object):
    """Use a form of single dispatch to generate concrete abstract syntax trees."""

    def __init__(self, code_type, name) -> None:
        """Construct a new TransformerGenerator with the requested type of transformer."""
        self.code_type = code_type
        self.name = name

    def generate(
        self, *args, **kwgs
    ) -> Union[SimpleStatementLine, BaseCompoundStatement]:
        """Generate a concrete abstract syntax tree based on type of instrumentation needed."""
        return getattr(self, "generate_{}".format(self.code_type))(*args, **kwgs)

    def generate_test_session_docstring(
        self,
    ) -> Union[SimpleStatementLine, BaseCompoundStatement]:
        """Generate a concrete abstract syntax tree for importing test fixture when docstring."""
        # construct the import statement that will import the test fixtures:
        # -- session_setup_teardown: initializes coverage tracking and saves it
        # Step 1: construct the source code as a string
        #         - line 1: comment showing when instrumentation was generated and by what
        #         - line 2: import the session_setup_teardown from fortify_coverage module
        # Note: fortify_coverage package is not part of the fortify_coverage_cli package;
        # it is a separate package on which fortify_coverage_cli and a subject program depends
        multiple_line_import_statement_str = (
            "\n# fortify-coverage instrumentation generated on"
            f" {datetime.now().strftime('%m/%d/%Y at %H:%M:%S')} by {self.name}\n"
            "from fortify_coverage.fixture import session_setup_teardown"
        )
        # Step 2: use libcst to construct a concrete abstract syntax tree out of the source code
        import_statement = cst.parse_statement(
            multiple_line_import_statement_str,
            config=transform.source_tree_configuration,
        )
        return import_statement
