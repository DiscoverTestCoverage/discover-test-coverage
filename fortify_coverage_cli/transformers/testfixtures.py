"""Instrument an application for function coverage using libCST."""

from fortify_coverage_cli import output
from fortify_coverage_cli import transform
from fortify_coverage_cli import codegenerator

from datetime import datetime

import libcst as cst

from libcst import Expr
from libcst import SimpleStatementLine
from libcst import SimpleString


def detect_module_docstring(node: cst.Module) -> bool:
    """Determine if a specific module node has a docstring or not."""
    # assume that the module does not have a docstring and prove otherwise
    has_module_docstring = False
    n = node.body[0]
    if isinstance(n, SimpleStatementLine):
        n = n.body[0]
        if isinstance(n, Expr):
            if len(n.children) == 1 and isinstance(n.children[0], SimpleString):
                has_module_docstring = True
    return has_module_docstring


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
        import_statement_type = codegenerator.InstrumentationTypeSourceCode.TEST_SESSION_DOCSTRONG
        instrumentation_type_generator = codegenerator.InstrumentedSourceCodeGenerator(import_statement_type)
        import_statement = instrumentation_type_generator.generate()
        # determine whether or not the module has a docstring
        module_has_docstring = detect_module_docstring(original_node)
        if module_has_docstring:
            body_modified = (
                *updated_node.body[0:1],
                import_statement,
                *updated_node.body[1:],
            )
            output.logger.debug(f"length of body modified: {len(body_modified)}")
            updated_node = updated_node.with_changes(body=body_modified)
        else:
            body_modified = (
                import_statement,
                *updated_node.body,
            )
            output.logger.debug(f"length of body modified: {len(body_modified)}")
            updated_node = updated_node.with_changes(body=body_modified)
        return updated_node
