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


# define the constants for the discover tool
code = create_constants(
    "code",
    Comment="#",
    Discover_Comment="# discover-test-coverage instrumentation generated on",
)

# define the constants for the discover tool
discover = create_constants(
    "discover",
    Emoji=":shield: ",
    Https="https://",
    Name="discover-test-coverage",
    Separator="/",
    Server_Shutdown=":person_shrugging: Shut down discover's sylog server",
    Tagline="discover-test-coverage: Disabling code to discover test effectiveness",
    Website="https://github.com/DiscoverTestCoverage/discover-test-coverage",
)

# define the constants for the discover tool
generator = create_constants(
    "generator",
    Function_Prefix="generate_{}",
)

# define the logger constants
logger = create_constants(
    "logger",
    Richlog="discover-richlog",
    Syslog="discover-syslog",
)

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
    Syslog_Logging_Destination="syslog",
    Default_Logging_Destination="console",
    Default_Logging_Level="ERROR",
    Format="%(message)s",
    Rich="Rich",
)

# define the constants for markers
markers = create_constants(
    "markers",
    Bad_Fifteen="<15>",
    Bad_Zero_Zero="",
    Empty_Bytes=b"",
    Empty="",
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
    Backup_Count=1,
    Localhost="127.0.0.1",
    Log_File=".discover.log",
    Max_Log_Size=1048576,
    Poll_Interval=0.5,
    Port=2525,
    Utf8_Encoding="utf-8",
)

# define the constants for syslog server
tests = create_constants(
    "tests",
    Backup="-backup",
    Conftest="conftest.py",
)

# define the wildcards constants
wildcards = create_constants(
    "wildcards",
    All_Python="*.py",
)
