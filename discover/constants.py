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

# define the logger constants
logger = create_constants(
    "logger",
    Richlog="discover-richlog",
    Syslog="discover-syslog",
)

# define the constants for the discover tool
discover = create_constants(
    "discover",
    Emoji=":shield:",
    Https="https://",
    Name="discover.py",
    Separator="/",
    Tagline="discover.py: Discover the effectiveness of your test coverage!",
    Website="https://github.com/DiscoverTestCoverage/discover.py",
)

# define the constants for markers
markers = create_constants(
    "markers",
    Empty=b"",
    Ellipse="...",
    Dot=".",
    Hidden=".",
    Indent="   ",
    Newline="\n",
    Nothing="",
    Space=" ",
    Tab="\t",
    Underscore="_",
)

# define the constants for output
output = create_constants(
    "output",
    Syslog=":sparkles: Syslog server for receiving debugging information",
    Test_Start=":sparkles: Start to run test suite for the specified program",
)

# define the constants for syslog server
server = create_constants(
    "server",
    Localhost="127.0.0.1",
    Log_File=".discover.log",
    Port=2525,
)

# define the constants for syslog server
tests = create_constants(
    "tests",
    Backup="-backup",
)

# define the wildcards constants
wildcards = create_constants(
    "wildcards",
    All_Python="*.py",
)
