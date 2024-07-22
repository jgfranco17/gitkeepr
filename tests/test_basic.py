from pathlib import Path

from pytest import LogCaptureFixture, MonkeyPatch

from tests.helpers import run_cli_command


def test_help_message_sane(
    tmp_path: Path, monkeypatch: MonkeyPatch, caplog: LogCaptureFixture
) -> None:
    """Test a sane basic help call."""
    monkeypatch.chdir(tmp_path)
    result = run_cli_command(["--help"])
    assert result.exit_code == 0
    assert (
        "Gitkeepr: CLI tool for managing Github repositories from local"
        in result.output
    )
