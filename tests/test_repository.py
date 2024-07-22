import os
from pathlib import Path

from pytest import LogCaptureFixture, MonkeyPatch

from tests.helpers import assert_generated_files, run_cli_command


def test_template_new_repo_success(
    tmp_path: Path, monkeypatch: MonkeyPatch, caplog: LogCaptureFixture
) -> None:
    monkeypatch.chdir(tmp_path)
    test_repo_name = "my-test-repo"
    expected_repo_path = os.path.join(str(tmp_path), test_repo_name)
    expected_files = [
        "README.md",
        ".gitignore",
        ".github/PULL_REQUEST_TEMPLATE.md",
    ]

    result = run_cli_command(["-vv", "repo", "new", "--name", test_repo_name])

    assert result.exit_code == 0
    assert_generated_files(expected_repo_path, files=expected_files)
    expected_logs = [
        "Validated environment variable 'GITHUB_USERNAME'",
        f"Generated 4 files in '{expected_repo_path}'",
    ]
    for log_msg in expected_logs:
        assert log_msg in caplog.text, f"Missing log message: {log_msg}"
