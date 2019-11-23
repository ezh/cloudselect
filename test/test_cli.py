import pytest

import awselect
from awselect.cli import Cli


def test_cli_version(script_runner):
    ret = script_runner.run("awselect", "--version")
    assert ret.success
    assert ret.stdout == "awselect version {}\n".format(awselect.__version__)
    assert ret.stderr == ""

    with pytest.raises(SystemExit):
        cli = Cli()
        cli.parse_args(["--version"])


def test_cli_verbose():
    cli = Cli()
    args = cli.parse_args("-v".split(" "))
    assert args.verbose == 1
    args = cli.parse_args("-vv".split(" "))
    assert args.verbose == 2


def test_cli_query():
    cli = Cli()
    args = cli.parse_args([])
    assert args.query == ""
    args = cli.parse_args("-q test".split(" "))
    assert args.query == "test"


def test_cli_profile():
    cli = Cli()
    args = cli.parse_args([""])
    assert args.profile == ""
    args = cli.parse_args("test".split(" "))
    assert args.profile == "test"
