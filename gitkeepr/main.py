import logging

import click
import colorama

from . import __version__
from .collborator import collaborator
from .constants import LoggerFormats
from .output import ColorHandler
from .repository import repo

colorama.init(autoreset=True)


def __get_log_level(verbosity: int) -> int:
    levels = {0: logging.WARN, 1: logging.INFO, 2: logging.DEBUG}
    return levels.get(verbosity, logging.DEBUG)


def __set_logger(level: int):
    logger = logging.getLogger(__package__)
    log_level = __get_log_level(level)
    logger.setLevel(log_level)
    handler = ColorHandler()
    handler.setLevel(log_level)
    formatter = logging.Formatter(
        LoggerFormats.MESSAGE_FORMAT, datefmt=LoggerFormats.DATE_FORMAT
    )
    handler.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(handler)


@click.group()
@click.version_option(version=__version__)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Increase verbosity. Use multiple times for more detail (e.g., -vv for debug).",
)
def cli(verbose: int):
    """Gitkeepr: CLI tool for managing Github repositories from local"""
    __set_logger(verbose)


cli.add_command(repo)
cli.add_command(collaborator)
