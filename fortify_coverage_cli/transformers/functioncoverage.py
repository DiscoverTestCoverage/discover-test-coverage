"""Instrument an application for function coverage using libCST."""

from fortify_coverage_cli import output
from fortify_coverage_cli import transform

from typing import List
from typing import Optional
from typing import Tuple

import libcst as cst



class FortifiedFunctionCoverageTransformer(cst.CSTTransformer):
    """Transform program source code to collect fortified function coverage."""

    def __init__(self):
        # stack for storing the canonical name of the current function
        self.stack: List[Tuple[str, ...]] = []

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        self.stack.append(node.name.value)

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.CSTNode:
        self.stack.pop()
        return updated_node

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        self.stack.append(node.name.value)
        return False

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.CSTNode:
        key = tuple(self.stack)
        self.stack.pop()
        output.logger.debug(
            f"current function definition node's name: {original_node.name}"
        )
        output.logger.debug(f"contents of the stack after the pop() call: {self.stack}")
        return updated_node.with_changes(decorators=[cst.Decorator(cst.Name("sample"))])

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.CSTNode:
        output.logger.debug("start --->")
        output.logger.debug(f"current module node's header: {original_node.header}")
        output.logger.debug("---> end")
        updated_node = updated_node.with_changes(
            header=(
                cst.parse_statement(
                    "from fortify import sample # leave_Module",
                    config=transform.source_tree_configuration,
                ),
                *updated_node.header,
            )
        )
        return updated_node
