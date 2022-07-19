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

    def __init__(self, type) -> None:
        """Construct a new TransformerGenerator with requested type of transformer."""
        self.type = type

    def generate(
        self, *args, **kwgs
    ) -> Union[SimpleStatementLine, BaseCompoundStatement]:
        """Generate a concrete abstract syntax tree based on type of instrumentation needed."""
        return getattr(self, "generate_{}".format(self.type))(*args, **kwgs)

    def generate_test_session_docstring(
        self,
    ) -> Union[SimpleStatementLine, BaseCompoundStatement]:
        """Generate a concrete abstract syntax tree for importing test fixture when docstring."""
        # construct the import statement that will import the test fixtures:
        # -- session_setup_teardown: initializes coverage tracking and saves it
        multiple_line_import_statement_str = (
            f"\n# fortify-coverage instrumentation generated on {datetime.now().strftime('%m/%d/%Y at %H:%M:%S')}\n"
            "from fortify_coverage.fixture import session_setup_teardown"
        )
        import_statement = cst.parse_statement(
            multiple_line_import_statement_str,
            config=transform.source_tree_configuration,
        )
        return import_statement
