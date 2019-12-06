# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
import logging

import dependency_injector.providers as providers
import pytest

import cloudselect
from cloudselect.cloudselect import CloudSelect
from cloudselect.discovery import DiscoveryService, DiscoveryServiceProvider
from cloudselect.discovery.aws import AWS
from cloudselect.discovery.local import Local
from cloudselect.discovery.stub import Stub as DiscoveryStub
from cloudselect.group import GroupServiceProvider
from cloudselect.group.simple import Simple as Simple
from cloudselect.group.stub import Stub as GroupStub
from cloudselect.pathfinder import PathFinderServiceProvider
from cloudselect.pathfinder.bastion import Bastion
from cloudselect.pathfinder.stub import Stub as PathFinderStub
from cloudselect.report import ReportServiceProvider
from cloudselect.report.json import Json
from cloudselect.report.stub import Stub as ReportStub


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
        plugin={
            "discovery": {
                "aws": "cloudselect.discovery.aws",
                "local": "cloudselect.discovery.local",
            },
            "group": {"simple": "cloudselect.group.simple"},
            "pathfinder": {"bastion": "cloudselect.pathfinder.bastion"},
            "report": {"json": "cloudselect.report.json"},
        },
    )
    cloud = CloudSelect()
    configuration = cloud.read_configuration()
    assert configuration == initial_config


def test_resolve():
    cloud = CloudSelect()
    discovery = cloud.resolve("cloudselect.discovery.aws", DiscoveryService)
    discovery_instance = discovery()
    assert discovery_instance.__class__.__name__ == "AWS"


def test_factory_load_plugin():
    class BrokenServiceProvider(providers.Singleton):
        pass

    cloud = CloudSelect()
    configuration = {}
    discovery = cloud.fabric_load_plugin(
        configuration, "discovery", DiscoveryServiceProvider, DiscoveryStub
    )
    assert type(discovery) == DiscoveryServiceProvider
    assert type(discovery()) == DiscoveryStub
    assert discovery() == discovery()

    # pass ServiceProvider without specialization
    with pytest.raises(AssertionError):
        cloud.fabric_load_plugin(
            configuration, "discovery", BrokenServiceProvider, DiscoveryStub
        )

    configuration = {"discovery": {"type": "unknown"}}
    with pytest.raises(ValueError):
        cloud.fabric_load_plugin(
            configuration, "discovery", DiscoveryServiceProvider, DiscoveryStub
        )

    configuration = {
        "discovery": {"type": "aws"},
        "plugin": {"discovery": {"aws": "cloudselect.discovery.aws"}},
    }
    discovery = cloud.fabric_load_plugin(
        configuration, "discovery", DiscoveryServiceProvider, DiscoveryStub
    )
    assert type(discovery()) == AWS


def test_factory_load_discovery():
    cloud = CloudSelect()
    configuration = cloud.read_configuration()

    configuration["discovery"] = {"type": "aws"}
    plugin = cloud.fabric_load_plugin(
        configuration, "discovery", DiscoveryServiceProvider, DiscoveryStub
    )
    assert type(plugin()) == AWS

    configuration["discovery"] = {"type": "local"}
    plugin = cloud.fabric_load_plugin(
        configuration, "discovery", DiscoveryServiceProvider, DiscoveryStub
    )
    assert type(plugin()) == Local


def test_factory_load_group():
    cloud = CloudSelect()
    configuration = cloud.read_configuration()

    configuration["group"] = {"type": "simple"}
    plugin = cloud.fabric_load_plugin(
        configuration, "group", GroupServiceProvider, GroupStub
    )
    assert type(plugin()) == Simple


def test_factory_load_pathfinder():
    cloud = CloudSelect()
    configuration = cloud.read_configuration()

    configuration["pathfinder"] = {"type": "bastion"}
    plugin = cloud.fabric_load_plugin(
        configuration, "pathfinder", PathFinderServiceProvider, PathFinderStub
    )
    assert type(plugin()) == Bastion


def test_factory_load_report():
    cloud = CloudSelect()
    configuration = cloud.read_configuration()

    configuration["report"] = {"type": "json"}
    plugin = cloud.fabric_load_plugin(
        configuration, "report", ReportServiceProvider, ReportStub
    )
    assert type(plugin()) == Json
