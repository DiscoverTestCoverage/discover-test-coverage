"""Generate different subclasses of CSTTransformer depending on requested instrumentation."""

from fortify_coverage_cli.transformers import functioncoverage
from fortify_coverage_cli.transformers import testfixtures

import libcst as cst


class TransformerGenerator(object):
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
