import shutil
import subprocess
from pathlib import Path


def test_check_command_reports_invalid_metadata_in_subprocess(tmp_path: Path) -> None:
    adr_path = tmp_path / "0001-invalid.md"
    adr_path.write_text(
        "---\n"
        "id: not-a-uuid\n"
        "ordinal: 1\n"
        "title: Invalid\n"
        "status: proposed\n"
        "date: '2026-08-25'\n"
        "tags: []\n"
        "supersedes: []\n"
        "superseded_by: null\n"
        "---\n\n# Invalid\n"
    )

    result = subprocess.run(
        [shutil.which("adr") or "adr", "check", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "0001-invalid.md" in result.stdout
    assert "valid UUID" in result.stdout
