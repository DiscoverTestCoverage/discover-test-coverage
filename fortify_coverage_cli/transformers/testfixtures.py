"""Instrument an application for function coverage using libCST."""

from fortify_coverage_cli import output
from fortify_coverage_cli import transform

from datetime import datetime

import libcst as cst

from libcst import Expr
from libcst import SimpleStatementLine
from libcst import SimpleString


class TestFixtureTransformer(cst.CSTTransformer):
    """Transform program source code to collect information about test execution."""

    def __init__(self):
        self.name = "TestFixtureTransformer"

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.CSTNode:
        output.logger.debug("start --->")
        output.logger.debug(f"current module node's header: {original_node.header}")
        output.logger.debug(
            f"current module node's body first: {original_node.body[0]}"
        )
        output.logger.debug(
            f"length of current module node's body: {len(original_node.body)}"
        )
        output.logger.debug("---> end")
        output.logger.debug(
            f"Does the module have a docstring? {self.has_module_docstring(original_node)}"
        )
        output.logger.debug(f"Node header: {updated_node.header}")
        output.logger.debug(f"Node body: {updated_node.body}")
        multiple_line_import_statement_str = (
            f"\n# fortify-coverage instrumentation generated on {datetime.now().strftime('%m/%d/%Y at %H:%M:%S')}\n"
            "from fortify_coverage.fixture import session_setup_teardown"
        )
        import_statement = cst.parse_statement(
            multiple_line_import_statement_str,
            config=transform.source_tree_configuration,
        )
        body_modified = (
            *updated_node.body[0:1],
            import_statement,
            *updated_node.body[1:],
        )
        output.logger.debug(f"length of body modified: {len(body_modified)}")
        updated_node = updated_node.with_changes(body=body_modified)
        return updated_node

    @staticmethod
    def has_module_docstring(node):
        has_module_docstring = False
        n = node.body[0]
        if isinstance(n, SimpleStatementLine):
            n = n.body[0]
            if isinstance(n, Expr):
                if len(n.children) == 1 and isinstance(n.children[0], SimpleString):
                    has_module_docstring = True
        return has_module_docstring
