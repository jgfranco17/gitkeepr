"""Gitkeepr exceptions."""
import logging
import sys
from typing import Any, Final, Optional

import click

from .output import print_warning

logger = logging.getLogger(__name__)


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

    def __init__(self, message: str, exit_code: int, help_text: Optional[str]):
        """Init an Gitkeepr Error."""
        self.message = message
        self.exit_code = exit_code
        if help_text is None:
            help_text = "Help is available with --help. Use the -v flag to increase output verbosity."
        self.help_text = help_text
        super().__init__(self.message)


class GitkeeprRuntimeError(GitkeeprBaseError):
    """General Gitkeepr CLI Error class."""

    def __init__(
        self,
        message: str,
        help_text: Optional[str] = None,
    ) -> None:
        """Init an Gitkeepr CLI Error."""
        self.message = message
        super().__init__(self.message, ExitCode.RUNTIME_ERROR, help_text)


class GitkeeprInputError(GitkeeprBaseError):
    """Gitkeepr User Input Error class."""

    def __init__(
        self,
        message: str,
        help_text: Optional[str] = None,
    ) -> None:
        """Init an Gitkeepr Input Error."""
        self.message = message
        super().__init__(self.message, ExitCode.INPUT_ERROR, help_text)


class ErrorHandler(click.Group):
    """A wrapped around CLI invocation that handles related errors."""

    def invoke(self, ctx: click.Context) -> Any:
        """Invoke the CLI and catch, log and exit for any raised errors."""
        try:
            return super().invoke(ctx)

        except GitkeeprBaseError as err:
            logger.exception(err)
            logger.error(f"{err.message}\n")
            print_warning(f"{err.help_text}")
            sys.exit(err.exit_code)

        except click.UsageError as err:
            err.show()
            sys.exit(ExitCode.RUNTIME_ERROR)
