"""Define constants for use in tea."""

import collections
import itertools


def create_constants(name, *args, **kwargs):
    """Create a namedtuple of constants."""
    # the constants are created such that:
    # the name is the name of the namedtuple
    # for *args with "Constant_Name" or **kwargs with Constant_Name = "AnyConstantName"
    # note that this creates a constant that will
    # throw an AttributeError when attempting to redefine
    new_constants = collections.namedtuple(name, itertools.chain(args, kwargs.keys()))
    return new_constants(*itertools.chain(args, kwargs.values()))


# The defined logging levels, in order of increasing severity, are as follows:
#
# DEBUG
# INFO
# WARNING
# ERROR
# CRITICAL

# define the logging constants
logging = create_constants(
    "logging",
    Debug="DEBUG",
    Info="INFO",
    Warning="WARNING",
    Error="ERROR",
    Critical="CRITICAL",
    Console_Logging_Destination="CONSOLE",
    Syslog_Logging_Destination="SYLOG",
    Default_Logging_Destination="CONSOLE",
    Default_Logging_Level="ERROR",
    Format="%(message)s",
    Rich="Rich",
)

# define the constants for the fortify tool
fortify = create_constants(
    "fortify",
    Emoji=":flexed_biceps:",
    Https="https://",
    Name="fortify-coverage",
    Separator="/",
    Tagline="Fortify-Coverage: Give Vitamins to Your Coverage Criteria!",
    Website="https://github.com/FortifiedTestCoverage/fortify-coverage-cli",
)

# define the constants for markers
markers = create_constants(
    "markers",
    Empty=b"",
    Hidden=".",
    Indent="   ",
    Newline="\n",
    Nothing="",
    Space=" ",
    Tab="\t",
    Underscore="_",
)

# define the wildcards constants
wildcards = create_constants(
    "wildcards",
    All_Python="*.py",
)
