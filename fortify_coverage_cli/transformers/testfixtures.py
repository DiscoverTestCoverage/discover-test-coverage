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
    """Transform test suite source code to collect information about test execution."""

    def __init__(self):
        """Construct a TestFixtureTransformer and give it a name."""
        self.name = "TestFixtureTransformer"

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.CSTNode:
        """Instrument the starting source code in the module to add test fixture import."""
        output.logger.debug(
            f"Modifying source code body with starting length: {len(updated_node.body)}"
        )
        # determine whether or not the module has a docstring
        module_has_docstring = detect_module_docstring(original_node)
        # the module has a docstring and thus the import statement should
        # be inserted after the docstring and before any other imports
        if module_has_docstring:
            # generate the correct type of import statement for a module with a docstring
            import_statement_type = (
                codegenerator.InstrumentationTypeSourceCode.TEST_SESSION_DOCSTRONG
            )
            instrumentation_type_generator = codegenerator.InstrumentedSourceCodeGenerator(
                import_statement_type
            )
            import_statement = instrumentation_type_generator.generate()
            # insert the import statement between the docstring and the rest of the code
            body_modified = (
                *updated_node.body[0:1],
                import_statement,
                *updated_node.body[1:],
            )
            updated_node = updated_node.with_changes(body=body_modified)
        # the module does not have a docstring and thus the import statement
        # should be imported as the first line inside of the module's body
        else:
            import_statement_type = (
                codegenerator.InstrumentationTypeSourceCode.TEST_SESSION_DOCSTRONG
            )
            instrumentation_type_generator = codegenerator.InstrumentedSourceCodeGenerator(
                import_statement_type
            )
            import_statement = instrumentation_type_generator.generate()
            body_modified = (
                import_statement,
                *updated_node.body,
            )
            output.logger.debug(f"Modified source code body to have length: {len(body_modified)}")
            updated_node = updated_node.with_changes(body=body_modified)
        return updated_node
