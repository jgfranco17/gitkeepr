"""Gitkeepr exceptions."""
from typing import Final


class ExitCode:
    """Class for Gitkeepr Exit Codes."""

    SUCCESS: Final[int] = 0
    RUNTIME_ERROR: Final[int] = 1
    INPUT_ERROR: Final[int] = 2


class GitkeeprBaseError(Exception):
    """A base Gitkeepr Error class.

    Contains a message, exit_code and help text show to the user

    exit_code should be a member of ExitCode
    """

    def __init__(self, message: str, exit_code: int):
        """Init an Gitkeepr Error."""
        self.message = message
        self.exit_code = exit_code
        super().__init__(self.message)


class GitkeeprRuntimeError(GitkeeprBaseError):
    """General Gitkeepr CLI Error class."""

    def __init__(self, message: str):
        """Init an Gitkeepr CLI Error."""
        self.message = message
        super().__init__(self.message, ExitCode.RUNTIME_ERROR)


class GitkeeprInputError(GitkeeprBaseError):
    """Gitkeepr User Input Error class."""

    def __init__(self, message: str):
        """Init an Gitkeepr Input Error."""
        self.message = message
        super().__init__(self.message, ExitCode.INPUT_ERROR)
