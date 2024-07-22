import os
from pathlib import Path

from pytest import LogCaptureFixture, MonkeyPatch

from tests.conftest import CommandRunner


def test_template_new_repo_success(
    runner: CommandRunner, caplog: LogCaptureFixture
) -> None:
    test_repo_name = "my-test-repo"
    expected_repo_path = os.path.join(runner.directory, test_repo_name)
    expected_files = [
        "README.md",
        ".gitignore",
        ".github/PULL_REQUEST_TEMPLATE.md",
    ]

    result = runner.run(["-vv", "repo", "new", "--name", test_repo_name])

    assert result.exit_code == 0
    runner.verify_generated_files(expected_repo_path, files=expected_files)
    expected_logs = [
        "Validated environment variable 'GITHUB_USERNAME'",
        f"Generated 4 files in '{expected_repo_path}'",
    ]
    for log_msg in expected_logs:
        assert log_msg in caplog.text, f"Missing log message: {log_msg}"
