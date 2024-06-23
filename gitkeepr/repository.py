import logging
import os
import subprocess
from typing import Optional, Tuple

import click

from .client import GithubClient
from .errors import GitkeeprInputError, GitkeeprRuntimeError
from .output import print_error, print_success

logger = logging.getLogger(__name__)


@click.group("repo")
def repo() -> None:
    """Interact with repositories."""
    pass


def __validate_directory(ctx: click.Context, param: click.Parameter, value: str) -> str:
    if value and not os.path.isdir(value):
        raise click.BadParameter(
            f"The directory '{value}' does not exist or is not a directory."
        )
    return value


def __run_git(cmd: str, *args) -> str:
    accepted_git_commands = ["clone", "status"]
    if cmd not in accepted_git_commands:
        raise GitkeeprInputError(f"Invalid git command '{cmd}' called.")

    git_cmd = ["git", cmd, *args]
    result = subprocess.run(git_cmd, capture_output=True, text=True)
    if result.exit_code != 0:
        raise GitkeeprRuntimeError(
            f"Git returned non-zero exit code {result.exit_code}: {result.stderr}"
        )
    return result.stdout


@click.command("create")
@click.argument("name")
@click.option("--private", is_flag=True, help="Create a private repository")
def create(name: str, private: Optional[bool] = True):
    """Create a new GitHub repository."""
    github = GithubClient()
    result = github.create_repo(name, private)
    click.echo(result)


@click.command("get")
@click.option(
    "--show-url", is_flag=True, default=False, help="Only fetch public repositories."
)
def get(show_url: bool):
    """List all repositories of a user."""
    try:
        github = GithubClient()
        repos = github.list_repos()
        if repo_count := len(repos):
            for index, repo in enumerate(repos, start=1):
                output = f"[{index:0{len(str(repo_count))}d}] {repo.name}"
                if show_url:
                    output += f": {repo.url}"
                click.echo(output)
        else:
            print_error(f"No repositories found for user {github.username}!")

    except GitkeeprInputError as err:
        print_error(f"Failed to get repositories: {err}")


@click.command("clone")
@click.argument("url")
@click.option(
    "--directory",
    type=click.STRING,
    callback=__validate_directory,
    help="Optional directory path.",
)
def clone(url: str, destination: str):
    """Clone a repository to a local directory.

    Args:
        url (str): Github repository URL
        destination (str): _description_

    Raises:
        GitkeeprInputError: _description_
    """
    if "github" not in url or not url.endswith(".git"):
        raise GitkeeprInputError(f"Invalid GitHub URL: {url}")

    git_cmd = __run_git("clone", url, destination)
    result = subprocess.run(git_cmd, capture_output=True, text=True)
    click.echo(result.stdout)
    if result.stderr:
        click.echo(result.stderr, err=True)


@click.command("new")
@click.option(
    "--name",
    type=str,
    required=True,
    help="Create a new basic repo-ready project directory.",
    prompt="Enter the name of the repository directory to create",
    default="new-project",
)
def new(name: str):
    """Initialize a template repository directory."""
    try:
        # Create project directory if it doesn't exist
        project_dir_path = os.path.join(os.getcwd(), name)
        if os.path.exists(project_dir_path):
            raise GitkeeprInputError(
                f"Repository directory already exists: {project_dir_path}"
            )
        os.makedirs(project_dir_path, exist_ok=False)
        logger.info(f"Creating project directory: {project_dir_path}")

        # Create basic repository files
        github_dir = os.path.join(project_dir_path, ".github")
        os.makedirs(github_dir, exist_ok=True)
        readme_content = "# Welcome to My Repository\n\nThis is a template repository."
        with open(os.path.join(project_dir_path, "README.md"), "w") as readme_file:
            readme_file.write(readme_content)
        print_success(f"Template repository initialized: {project_dir_path}")

    except Exception as e:
        print_error(f"Failed to create a new project directory: {e}")


repo.add_command(get)
repo.add_command(clone)
repo.add_command(create)
repo.add_command(new)
