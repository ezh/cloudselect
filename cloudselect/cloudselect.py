# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
import argparse
import inspect
import json
import logging
import os
import sys
from logging.config import dictConfig

import appdirs
import dependency_injector.providers as providers
import pkg_resources

import cloudselect
from cloudselect import Container
from cloudselect.discovery import DiscoveryService, DiscoveryServiceProvider
from cloudselect.discovery.stub import Stub as DiscoveryStub
from cloudselect.filter import FilterService, FilterServiceProvider
from cloudselect.filter.stub import Stub as FilterStub
from cloudselect.pathfinder import PathFinderService, PathFinderServiceProvider
from cloudselect.pathfinder.stub import Stub as PathFinderStub
from cloudselect.report import ReportService, ReportServiceProvider
from cloudselect.report.stub import Stub as ReportStub
from cloudselect.selector import Selector


class CloudSelect:
    configpath = appdirs.user_config_dir("cloudselect")
    extension = "cloud.json"
    importer = staticmethod(__import__)
    logger = None

    def fabric(self, configuration, args):
        if args.verbose:
            if args.verbose == 1:
                configuration.get("log", {}).get("root", {})["level"] = logging.INFO
            elif args.verbose > 1:
                configuration.get("log", {}).get("root", {})["level"] = logging.DEBUG
        dictConfig(configuration.get("log", {}))
        self.logger = logging.getLogger("cloudselect.CloudSelect")
        self.logger.debug("Logging is initialized")
        self.logger.debug(
            "Configuration:\n{}".format(
                json.dumps(
                    configuration, sort_keys=True, indent=4, separators=(",", ": ")
                )
            )
        )
        Container.args = providers.Object(args)
        Container.config = providers.Configuration(name="config", default=configuration)
        Container.configpath = providers.Object(self.configpath)
        Container.selector = providers.Singleton(Selector)
        Container.extension = providers.Object(self.extension)

        Container.discovery = self.fabric_load_plugin(
            configuration, "discovery", DiscoveryServiceProvider, DiscoveryStub
        )
        Container.filter = self.fabric_load_plugin(
            configuration, "filter", FilterServiceProvider, FilterStub
        )
        Container.pathfinder = self.fabric_load_plugin(
            configuration, "pathfinder", PathFinderServiceProvider, PathFinderStub
        )
        Container.report = self.fabric_load_plugin(
            configuration, "report", ReportServiceProvider, ReportStub
        )

        return Container.selector()

    def fabric_load_plugin(
        self, configuration, plugin_type, service_provider, service_stub
    ):
        if configuration.get(plugin_type, {}).get("type"):
            plugin = configuration.get("plugin", {}).get(
                configuration[plugin_type]["type"]
            )
            if plugin is None:
                raise ValueError(
                    "Unable to find class for {}: {}".format(
                        plugin_type, configuration[plugin_type]["type"]
                    )
                )
            return self.plugin(plugin, service_provider)
        else:
            return self.plugin(service_stub, service_provider)

    def merge(self, a, b, path=None):
        """ Merge two dictioraries """
        if path is None:
            path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self.merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass  # same leaf value
                else:
                    raise Exception("Conflict at %s" % ".".join(path + [str(key)]))
            else:
                a[key] = b[key]
        return a

    def parse_args(self, args):
        parser = argparse.ArgumentParser(prog="cloudselect")
        parser.add_argument(
            "--version",
            action="version",
            version="%(prog)s version {}".format(cloudselect.__version__,),
        )
        parser.add_argument(
            "--verbose", "-v", action="count", help="maximum verbosity: -vv"
        )
        parser.add_argument("--query", "-q", nargs="?", default="")
        parser.add_argument(
            "--edit",
            "-e",
            nargs="?",
            default=False,
            help="edit configuration or profile",
        )
        parser.add_argument("profile", nargs="?")
        return parser.parse_args(args)

    def plugin(self, plugin_class, service_provider):
        assert service_provider.provided_type, "{} lost provided_type value".format(
            service_provider
        )
        if isinstance(plugin_class, str):
            plugin_class_object = self.resolve(
                plugin_class, service_provider.provided_type
            )
            return service_provider(plugin_class_object)
        else:
            return service_provider(plugin_class)

    def read_configuration(self, name=None):
        """
        Read json configuration from configpath
        Copy initial configuration from cloud.json.dist to cloud.json if needed
        """
        file_name = ".".join(filter(None, [name, self.extension]))
        full_path = os.path.join(self.configpath, file_name)
        try:
            if name is None and not os.path.isfile(full_path):
                if not os.path.exists(self.configpath):
                    os.mkdir(self.configpath)
                source = pkg_resources.resource_stream(
                    __name__, "{}.dist".format(self.extension)
                )
                with open(full_path, "w") as f:
                    json.dump(
                        json.load(source),
                        f,
                        sort_keys=True,
                        indent=4,
                        separators=(",", ": "),
                    )
            with open(full_path, "r") as f:
                return json.load(f)
        except Exception as e:
            message = "Unable to read configuration {}: {}".format(file_name, str(e))
            if self.logger:
                self.logger.error(message)
            else:
                print(message)

    def resolve(self, s, base):
        """
        Resolve strings to objects using standard import and attribute
        syntax.
        """
        name = s.split(".")
        used = name.pop(0)
        try:
            found = self.importer(used)
            for frag in name:
                used += "." + frag
                try:
                    found = getattr(found, frag)
                except AttributeError:
                    self.importer(used)
                    found = getattr(found, frag)
            for cls in dir(found):
                cls = getattr(found, cls)
                if (
                    inspect.isclass(cls)
                    and inspect.getmodule(cls) == found
                    and issubclass(cls, base)
                ):
                    return cls
            raise ImportError("Unable to find plugin in {}".format(found))
        except ImportError:
            e, tb = sys.exc_info()[1:]
            v = ValueError("Cannot resolve %r: %s" % (s, e))
            v.__cause__, v.__traceback__ = e, tb
            raise v


def main():
    cloud = CloudSelect()
    args = cloud.parse_args(sys.argv[1:])
    # Read shared part
    profile = cloud.read_configuration()
    if args.profile:
        # Read part with profile information
        profile = cloud.merge(profile, cloud.read_configuration(args.profile))
    cloud.fabric(profile, args).select()
