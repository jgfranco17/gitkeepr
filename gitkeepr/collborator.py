import logging

import click

from .client import GithubClient

logger = logging.getLogger(__name__)


@click.group("collaborator")
def collaborator() -> None:
    """Manage repository collborators."""
    pass


@click.command("add")
@click.argument("repo")
@click.argument("username")
@click.option(
    "--permission",
    default="push",
    type=click.Choice(
        [
            "pull",
            "push",
            "admin",
        ],
        case_sensitive=False,
    ),
    help="Permission level: pull, push, or admin",
)
def add_collaborator(repo: str, username: str, permission: str):
    """Add a collaborator to a repository."""
    github = GithubClient()
    result = github.add_collaborator(repo, username, permission)
    click.echo(result)


@click.command("remove")
@click.argument("repo")
@click.argument("username")
def remove_collaborator(repo: str, username: str):
    """Remove a collaborator from a repository."""
    github = GithubClient()
    result = github.remove_collaborator(repo, username)
    click.echo(result)


collaborator.add_command(add_collaborator)
collaborator.add_command(remove_collaborator)
