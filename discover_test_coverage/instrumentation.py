"""Types of instrumentation."""

from enum import Enum


class InstrumentationType(str, Enum):
    """The predefined levels for instrumentation."""

    FIXTURE = "fixture"
    FUNCTION = "function"
    BRANCH = "branch"
