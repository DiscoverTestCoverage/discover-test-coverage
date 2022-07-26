# flake8: noqa
# type: ignore

"""Instrument an application for function coverage using libCST."""

from typing import List
from typing import Optional
from typing import Tuple

import libcst as cst

from discover_test_coverage import constants
from discover_test_coverage import output
from discover_test_coverage import transform


class FunctionCoverageTransformer(cst.CSTTransformer):
    """Transform program source code to collect fortified function coverage."""

    def __init__(self):  # noqa
        # stack for storing the canonical name of the current function
        self.stack: List[Tuple[str, ...]] = []
        # construct a fully qualified name of the TestFixtureTransformer
        self.name = str(
            self.__module__ + constants.markers.Dot + type(self).__qualname__
        )

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:  # noqa
        self.stack.append(node.name.value)  # type: ignore

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.CSTNode:  # noqa
        self.stack.pop()
        return updated_node

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:  # noqa
        self.stack.append(node.name.value)  # type:ignore
        return False

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.CSTNode:  # noqa
        # key = tuple(self.stack)
        self.stack.pop()
        output.logger.debug(
            f"current function definition node's name: {original_node.name}"
        )
        output.logger.debug(f"contents of the stack after the pop() call: {self.stack}")
        return updated_node.with_changes(decorators=[cst.Decorator(cst.Name("sample"))])

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.CSTNode:  # noqa
        output.logger.debug("start --->")
        output.logger.debug(f"current module node's header: {original_node.header}")
        output.logger.debug("---> end")
        # TODO: Add in correct location and add correct import to a
        # module that exists inside of the fortify-coverage package
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
