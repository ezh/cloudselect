import logging

import pytest

import cloudselect
from cloudselect.cloudselect import CloudSelect
from cloudselect.discovery import DiscoveryService


def test_cli_version(script_runner):
    ret = script_runner.run("cloudselect", "--version")
    assert ret.success
    assert ret.stdout == "cloudselect version {}\n".format(cloudselect.__version__)
    assert ret.stderr == ""

    with pytest.raises(SystemExit):
        cloud = CloudSelect()
        cloud.parse_args(["--version"])


def test_cli_verbose():
    cloud = CloudSelect()
    args = cloud.parse_args("-v".split(" "))
    assert args.verbose == 1
    args = cloud.parse_args("-vv".split(" "))
    assert args.verbose == 2


def test_cli_query():
    cloud = CloudSelect()
    args = cloud.parse_args([])
    assert args.query == ""
    args = cloud.parse_args("-q test".split(" "))
    assert args.query == "test"


def test_cli_profile():
    cloud = CloudSelect()
    assert cloud.configpath.endswith("cloudselect")
    args = cloud.parse_args([""])
    assert args.profile == ""
    args = cloud.parse_args("test".split(" "))
    assert args.profile == "test"


def test_cli_read_configuration():
    initial_config = dict(
        log={
            "version": 1,
            "formatters": {
                "f": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"}
            },
            "handlers": {
                "h": {
                    "class": "logging.StreamHandler",
                    "formatter": "f",
                    "level": logging.DEBUG,
                }
            },
            "root": {"handlers": ["h"], "level": logging.ERROR},
        },
    )
    cloud = CloudSelect()
    configuration = cloud.read_configuration()
    assert configuration == initial_config


def test_resolve():
    cloud = CloudSelect()
    discovery = cloud.resolve("discovery.aws", DiscoveryService)
    discovery_instance = discovery()
    assert discovery_instance.__class__.__name__ == "AWS"
