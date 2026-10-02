import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import ShellEmulator


def test_parse_command_with_arguments():
    command, arguments = ShellEmulator.parse_command("ls file.txt test.txt")
    assert command == "ls"
    assert arguments == ["file.txt", "test.txt"]


def test_parse_cd_command():
    command, arguments = ShellEmulator.parse_command("cd documents")
    assert command == "cd"
    assert arguments == ["documents"]


def test_parse_empty_command():
    command, arguments = ShellEmulator.parse_command("")
    assert command is None
    assert arguments == []


def test_parse_multiple_spaces():
    command, arguments = ShellEmulator.parse_command("  ls   one   two  ")
    assert command == "ls"
    assert arguments == ["one", "two"]
