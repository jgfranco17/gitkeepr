import os
from pathlib import Path
from typing import Dict, List, Optional

from click.testing import CliRunner, Result

from gitkeepr.main import cli


def run_cli_command(
    cli_args: List[str], custom_envs: Optional[Dict[str, str]] = None
) -> Result:
    """Run the Gitkeepr CLI with envs set."""
    env = {
        "GITHUB_USERNAME": "test-user",
        "GITHUB_API_TOKEN": "my-github-api-token",  # pragma: allowlist secret
    }
    if custom_envs:
        env.update(custom_envs)

    runner = CliRunner(mix_stderr=False)
    return runner.invoke(cli, cli_args, env=env)


def assert_generated_files(
    directory: str,
    files: List[str],
) -> None:
    """Assert that the expected files to be generated are created."""
    for file in files:
        full_path = Path(os.path.join(directory, file))
        assert full_path.exists(), f"Templated file '{file}' was not created"
