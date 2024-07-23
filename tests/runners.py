import os
from pathlib import Path
from typing import Any, List, Tuple

from click.testing import CliRunner, Result

from gitkeepr.main import cli


class TestRunner:
    def __init__(self, working_dir: str):
        self.env = {
            "GITHUB_USERNAME": "test-user",
            "GITHUB_API_TOKEN": "my-github-api-token",  # pragma: allowlist secret
        }
        self.__working_dir = working_dir
        self.__runner = CliRunner(mix_stderr=False)

    @property
    def directory(self) -> str:
        return self.__working_dir

    def get_test_resource(self, *args: Tuple[Any]) -> Path:
        return Path(self.__working_dir, *args)

    def run_cli(self, cli_args: List[str]) -> Result:
        """Run the Gitkeepr CLI with envs set."""
        env = self.env.copy()
        return self.__runner.invoke(cli, cli_args, env=env)

    def verify_generated_files(self, directory: str, files: List[str]) -> None:
        """Assert that the expected files to be generated are created."""
        for file in files:
            full_path = Path(os.path.join(directory, file))
            assert (
                full_path.exists()
            ), f"Templated file '{str(full_path)}' was not created"
