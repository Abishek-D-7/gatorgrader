"""Test cases for the run module."""

import platform

from gator import run

# define the operating systems on which to run processes
LINUX = "Linux"
MAC = "Darwin"
WINDOWS = "Windows"


class DistinctStr(str):
    """Equal to a str but never the same object."""


def expected_echo_output(system_name):
    """Return the output that echo makes on the given operating system."""
    # running an "echo" will have a trailing newline
    if system_name in (LINUX, MAC):
        return b"Hello!\n"
    # running an "echo" will have a carriage return and then trailing newline
    if system_name == WINDOWS:
        return b'"Hello!"\r\n'
    return None


def test_run_working_command_returns_message():
    """Check that a single line is returned from command ."""
    output, error, code = run.run_command('echo "Hello!"')
    assert error == b""
    assert output == expected_echo_output(platform.system())
    assert code == 0


def test_expected_echo_output_uses_value_comparison():
    """Match operating system names that are equal but distinct objects."""
    linux = DistinctStr(LINUX)
    windows = DistinctStr(WINDOWS)
    assert linux == LINUX
    assert linux is not LINUX
    assert expected_echo_output(linux) == b"Hello!\n"
    assert expected_echo_output(windows) == b'"Hello!"\r\n'


def test_run_broken_command_returns_nonzero():
    """Check that a single line is returned from command ."""
    output, error, code = run.run_command("willnotwork")
    assert output == b""
    assert error != b""
    assert code != 0


def test_run_command_grab_output_as_string_correct_command(tmpdir):
    """Check that invocation of command produces correct captured output."""
    tmpdir.mkdir("Hello1")
    tmpdir.mkdir("Hello2")
    tmpdir.mkdir("Hello3")
    assert len(tmpdir.listdir()) == 3
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/"
    # note that this test case passes even when run in AppVeyor CI
    # thus suggesting that the ls command is supported on Windows
    output = run.specified_command_get_output("ls " + directory)
    assert "Hello1" in output
    assert "Hello2" in output
    assert "Hello3" in output


def test_run_command_grab_output_as_string_incorrect_command(tmpdir):
    """Check that invocation of command produces correct captured output."""
    tmpdir.mkdir("Hello1")
    tmpdir.mkdir("Hello2")
    tmpdir.mkdir("Hello3")
    assert len(tmpdir.listdir()) == 3
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/"
    # this command will not work correctly because it does not exist
    # this means that it should not produce any output
    output = run.specified_command_get_output("gus " + directory)
    assert output == ""


def test_run_invalid_output():
    """Check that invalid unicode bytestrings are handled correctly."""
    invalid_byte_sequence = b"\x80\x81"
    output = run.get_actual_output(invalid_byte_sequence)
    assert invalid_byte_sequence in output


def test_run_invalid_output_str():
    """Check that ouputs that are already strings are handled correctly."""
    randomString = "Hello"
    output = run.get_actual_output(randomString)
    assert randomString in output
