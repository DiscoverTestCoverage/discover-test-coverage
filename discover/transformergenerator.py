"""Generate different subclasses of CSTTransformer depending on requested instrumentation."""

from fortify_coverage_cli.transformers import functioncoverage
from fortify_coverage_cli.transformers import testfixtures

import libcst as cst


class TransformerGenerator(object):
    """Use a form of single dispatch to generate requested subclass of CSTTransformer."""

    def __init__(self, type) -> None:
        """Construct a new TransformerGenerator with requested type of transformer."""
        self.type = type

    def generate(self, *args, **kwgs) -> cst.CSTTransformer:
        """Generate a transformer based on type of instrumentation needed."""
        return getattr(self, "generate_transformer_{}".format(self.type))(*args, **kwgs)

    def generate_transformer_function(self) -> cst.CSTTransformer:
        """Generate a fortified function coverage transformer to create an instrumented program."""
        transformer = functioncoverage.FortifiedFunctionCoverageTransformer()
        return transformer

    def generate_transformer_branch(self) -> None:
        """Generate a fortified branch coverage transformer to create an instrumented program."""
        print("TODO: branch transformer")

    def generate_transformer_fixture(self) -> cst.CSTTransformer:
        """Generate a test fixture transformer to create an instrumented test suite."""
        transformer = testfixtures.TestFixtureTransformer()
        return transformer
