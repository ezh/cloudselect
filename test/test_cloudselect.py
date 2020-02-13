# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""This module is used for testing CloudSelect class."""
import logging
import os

import dependency_injector.providers as providers
import pytest

import cloudselect
from cloudselect.cloudselect import CloudSelect
from cloudselect.discovery import DiscoveryService, DiscoveryServiceProvider
from cloudselect.discovery.aws import AWS
from cloudselect.discovery.local import Local
from cloudselect.discovery.stub import Stub as DiscoveryStub
from cloudselect.group import GroupServiceProvider
from cloudselect.group.simple import Simple
from cloudselect.group.stub import Stub as GroupStub
from cloudselect.pathfinder import PathFinderServiceProvider
from cloudselect.pathfinder.bastion import Bastion
from cloudselect.pathfinder.stub import Stub as PathFinderStub
from cloudselect.report import ReportServiceProvider
from cloudselect.report.json import Json
from cloudselect.report.stub import Stub as ReportStub


def test_cli_incorrect_configuration(script_runner):
    """Testing cloudselect invocation with non existing profile."""
    ret = script_runner.run("cloudselect", "something_that_does_not_exist")
    assert not ret.success
    assert ret.stdout == ""
    assert ret.stderr == 'Error: Profile "something_that_does_not_exist" not found\n'


def test_cli_version(tmpdir, script_runner):
    """Testing that cloudselect has expected version."""
    ret = script_runner.run("cloudselect", "--version")
    assert ret.success
    assert ret.stdout == "cloudselect version {}\n".format(cloudselect.__version__)
    assert ret.stderr == ""

    with pytest.raises(SystemExit):
        cloud = CloudSelect(tmpdir)
        cloud.parse_args(["--version"])


def test_cli_verbose(tmpdir):
    """Testing cloudselect verbose behavior."""
    cloud = CloudSelect(tmpdir)
    if os.environ.get("CLOUDSELECT_VERBOSE"):
        del os.environ["CLOUDSELECT_VERBOSE"]
    args = cloud.parse_args("-v".split(" "))
    assert args.verbose == 1
    args = cloud.parse_args("-vv".split(" "))
    assert args.verbose == 2
    args = cloud.parse_args([])
    assert args.verbose is None
    os.environ["CLOUDSELECT_VERBOSE"] = "1"
    args = cloud.parse_args([])
    assert args.verbose == 1
    os.environ["CLOUDSELECT_VERBOSE"] = "2"
    args = cloud.parse_args([])
    assert args.verbose == 2


def test_cli_query(tmpdir):
    """Testing query option."""
    cloud = CloudSelect(tmpdir)
    args = cloud.parse_args([])
    assert args.query == ""
    args = cloud.parse_args("-q test".split(" "))
    assert args.query == "test"


def test_cli_profile():
    """Testing profile option."""
    cloud = CloudSelect()
    assert cloud.configpath.endswith("cloudselect")
    args = cloud.parse_args([""])
    assert args.profile == ""
    args = cloud.parse_args("test".split(" "))
    assert args.profile == "test"


def test_cli_configuration_read(tmpdir):
    """Testing initial configuration."""
    initial_config = {
        "log": {
            "version": 1,
            "formatters": {
                "f": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
            },
            "handlers": {
                "h": {
                    "class": "logging.StreamHandler",
                    "formatter": "f",
                    "level": logging.DEBUG,
                },
            },
            "root": {"handlers": ["h"], "level": logging.ERROR},
        },
        "plugin": {
            "discovery": {
                "aws": "cloudselect.discovery.aws",
                "local": "cloudselect.discovery.local",
            },
            "group": {"simple": "cloudselect.group.simple"},
            "pathfinder": {"bastion": "cloudselect.pathfinder.bastion"},
            "report": {
                "json": "cloudselect.report.json",
                "json_pp": "cloudselect.report.json_pp",
                "yaml": "cloudselect.report.yaml",
            },
        },
    }
    cloud = CloudSelect(tmpdir)
    configuration = cloud.configuration_read()
    assert configuration == initial_config


def test_resolve(tmpdir):
    """Testing resolve behavior."""
    cloud = CloudSelect(tmpdir)
    discovery = cloud.resolve("cloudselect.discovery.aws", DiscoveryService)
    discovery_instance = discovery()
    assert discovery_instance.__class__.__name__ == "AWS"


def test_factory_load_plugin(tmpdir):
    """Testing factory_load_plugin behavior."""
    # fmt off
    class BrokenServiceProvider(providers.Singleton):
        """Broken provider."""

    cloud = CloudSelect(tmpdir)
    configuration = {}
    discovery = cloud.fabric_load_plugin(
        configuration, "discovery", DiscoveryServiceProvider, DiscoveryStub,
    )
    assert isinstance(discovery, DiscoveryServiceProvider)
    assert isinstance(discovery(), DiscoveryStub)
    assert discovery() == discovery()

    # pass ServiceProvider without specialization
    with pytest.raises(AssertionError):
        cloud.fabric_load_plugin(
            configuration, "discovery", BrokenServiceProvider, DiscoveryStub,
        )

    configuration = {"discovery": {"type": "unknown"}}
    with pytest.raises(ValueError):
        cloud.fabric_load_plugin(
            configuration, "discovery", DiscoveryServiceProvider, DiscoveryStub,
        )

    configuration = {
        "discovery": {"type": "aws"},
        "plugin": {"discovery": {"aws": "cloudselect.discovery.aws"}},
    }
    discovery = cloud.fabric_load_plugin(
        configuration, "discovery", DiscoveryServiceProvider, DiscoveryStub,
    )
    assert isinstance(discovery(), AWS)


def test_factory_load_discovery(tmpdir):
    """Testing that factory is able to load AWS discovery plugin."""
    cloud = CloudSelect(tmpdir)
    configuration = cloud.configuration_read()

    configuration["discovery"] = {"type": "aws"}
    plugin = cloud.fabric_load_plugin(
        configuration, "discovery", DiscoveryServiceProvider, DiscoveryStub,
    )
    assert isinstance(plugin(), AWS)

    configuration["discovery"] = {"type": "local"}
    plugin = cloud.fabric_load_plugin(
        configuration, "discovery", DiscoveryServiceProvider, DiscoveryStub,
    )
    assert isinstance(plugin(), Local)


def test_factory_load_group(tmpdir):
    """Testing that factory is able to load simple group plugin."""
    cloud = CloudSelect(tmpdir)
    configuration = cloud.configuration_read()

    configuration["group"] = {"type": "simple"}
    plugin = cloud.fabric_load_plugin(
        configuration, "group", GroupServiceProvider, GroupStub,
    )
    assert isinstance(plugin(), Simple)


def test_factory_load_pathfinder(tmpdir):
    """Testing that factory is able to load bastion pathfinder plugin."""
    cloud = CloudSelect(tmpdir)
    configuration = cloud.configuration_read()

    configuration["pathfinder"] = {"type": "bastion"}
    plugin = cloud.fabric_load_plugin(
        configuration, "pathfinder", PathFinderServiceProvider, PathFinderStub,
    )
    assert isinstance(plugin(), Bastion)


def test_factory_load_report(tmpdir):
    """Testing that factory is able to load json report plugin."""
    cloud = CloudSelect(tmpdir)
    configuration = cloud.configuration_read()

    configuration["report"] = {"type": "json"}
    plugin = cloud.fabric_load_plugin(
        configuration, "report", ReportServiceProvider, ReportStub,
    )
    assert isinstance(plugin(), Json)
