# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""CloudSelect module loads configuration, plugins and invokes Select module."""
import argparse
import inspect
import json
import logging
import os
import sys
import traceback
from logging.config import dictConfig

import appdirs
import chardet
import dependency_injector.providers as providers
import pkg_resources

import cloudselect
from cloudselect import Container
from cloudselect.discovery import DiscoveryServiceProvider
from cloudselect.discovery.stub import Stub as DiscoveryStub
from cloudselect.group import GroupServiceProvider
from cloudselect.group.stub import Stub as GroupStub
from cloudselect.pathfinder import PathFinderServiceProvider
from cloudselect.pathfinder.stub import Stub as PathFinderStub
from cloudselect.report import ReportServiceProvider
from cloudselect.report.stub import Stub as ReportStub
from cloudselect.selector import Selector


class CloudSelect:
    """CloudSelect class that bootstraps application.

    Attributes:
       configpath     The path to the user configuration directory ~/.config/cloudselect.
       extension      CloudSelect files extension 'cloud.json'.

    """

    extension = "cloud.json"
    importer = staticmethod(__import__)

    def __init__(self):
        """Class constructor."""
        self.configpath = appdirs.user_config_dir("cloudselect")
        self.logger = None

    def configuration_exists(self, name):
        """Check if configuration/profile exists."""
        if os.path.isfile(name):
            return True
        else:
            file_name = ".".join(filter(None, [name, self.extension]))
            full_path = os.path.join(self.configpath, file_name)
            return os.path.isfile(full_path)

    def configuration_read(self, name=None):
        """Read configuration/profile."""
        """
        Read json configuration from configpath
        Copy initial configuration from cloud.json.dist to cloud.json if needed
        """  # pylint: disable=W0105
        full_path = name
        if name and os.path.isfile(name):
            full_path = os.path.abspath(name)
            name = os.path.basename(name).replace(".{}".format(self.extension), "")
        else:
            file_name = ".".join(filter(None, [name, self.extension]))
            full_path = os.path.join(self.configpath, file_name)

        try:
            if name is None and not os.path.isfile(full_path):
                if not os.path.exists(self.configpath):
                    os.mkdir(self.configpath)
                source = pkg_resources.resource_string(
                    __name__, "{}.dist".format(self.extension),
                )
                with open(full_path, "w") as f:
                    data = json.loads(source.decode())
                    json.dump(
                        data, f, sort_keys=True, indent=4, separators=(",", ": "),
                    )
            charenc = chardet.detect(open(full_path, "rb").read())["encoding"]
            with open(full_path, "r", encoding=charenc) as f:
                return json.load(f)
        except Exception as e:
            message = "Unable to read configuration {}: {}".format(full_path, str(e))
            if self.logger:
                self.logger.debug(traceback.format_exc())
                self.logger.error(message)
            else:
                traceback.print_exc()
                print(message)

    def fabric(self, configuration, args):
        """Load discovery, group, pathfinder, report plugins."""
        if args.verbose:
            if args.verbose == 1:
                configuration.get("log", {}).get("root", {})["level"] = logging.INFO
            elif args.verbose > 1:
                configuration.get("log", {}).get("root", {})["level"] = logging.DEBUG
        dictConfig(configuration.get("log", {}))
        self.logger = logging.getLogger("cloudselect.CloudSelect")
        self.logger.debug("Logging is initialized")
        self.logger.debug(
            "Configuration:\n%s",
            json.dumps(configuration, sort_keys=True, indent=4, separators=(",", ": ")),
        )
        Container.args = providers.Object(args)
        Container.config = providers.Configuration(name="config", default=configuration)
        Container.configpath = providers.Object(self.configpath)
        Container.extension = providers.Object(self.extension)
        Container.options = providers.Callable(self.options)
        Container.selector = providers.Singleton(Selector)

        Container.discovery = self.fabric_load_plugin(
            configuration, "discovery", DiscoveryServiceProvider, DiscoveryStub,
        )
        Container.group = self.fabric_load_plugin(
            configuration, "group", GroupServiceProvider, GroupStub,
        )
        Container.pathfinder = self.fabric_load_plugin(
            configuration, "pathfinder", PathFinderServiceProvider, PathFinderStub,
        )
        Container.report = self.fabric_load_plugin(
            configuration, "report", ReportServiceProvider, ReportStub, args.reporter,
        )

        return Container.selector()

    def fabric_load_plugin(
        self,
        configuration,
        plugin_type,
        service_provider,
        service_stub,
        plugin_name=None,
    ):
        """Load plugins."""
        if configuration.get(plugin_type, {}).get("type"):
            if not plugin_name:
                plugin_name = configuration[plugin_type]["type"]
            plugin = (
                configuration.get("plugin", {}).get(plugin_type, {}).get(plugin_name)
            )
            if plugin is None:
                raise ValueError(
                    "Unable to find class for {}: {}".format(
                        plugin_type, configuration[plugin_type]["type"],
                    ),
                )
            return self.plugin(plugin, service_provider)
        return self.plugin(service_stub, service_provider)

    @staticmethod
    def merge(dict1, dict2, path=None):
        """Merge two dictioraries."""
        if path is None:
            path = []
        if dict2 is None:
            return dict1
        if dict1 is None:
            return dict2
        for key in dict2:
            if key in dict1:
                if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                    CloudSelect.merge(dict1[key], dict2[key], path + [str(key)])
                elif dict1[key] == dict2[key]:
                    pass  # same leaf value
                else:
                    logging.debug(
                        "Conflict at %s; overwrite", ".".join(path + [str(key)]),
                    )
                    dict1[key] = dict2[key]
            else:
                dict1[key] = dict2[key]
        return dict1

    def options(self, name, metadata=None):
        """Get plugin/block options."""
        group = Container.group()
        base = Container.config().get(name, {})
        override = group.run(name, metadata)
        return self.merge(base, override)

    @staticmethod
    def parse_args(args):
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(prog="cloudselect")
        parser.add_argument(
            "--version",
            action="version",
            version="%(prog)s version {}".format(cloudselect.__version__,),
        )
        parser.add_argument(
            "--verbose", "-v", action="count", help="maximum verbosity: -vv",
        )
        parser.add_argument("--query", "-q", nargs="?", default="")
        parser.add_argument(
            "--edit",
            "-e",
            nargs="?",
            default=False,
            help="edit configuration or profile",
        )
        parser.add_argument(
            "--reporter", nargs="?", default="", help="change Cloud Select output",
        )
        if (
            os.environ.get("CLOUDSELECT_VERBOSE")
            and "-v" not in args
            and "-vv" not in args
        ):
            if os.environ["CLOUDSELECT_VERBOSE"] == "1":
                args.append("-v")
            else:
                args.append("-vv")
        parser.add_argument("profile", nargs="?")
        result = parser.parse_args(args)
        return result

    def plugin(self, plugin_class, service_provider):
        """Return service provider."""
        if not service_provider.provided_type:
            raise AssertionError(
                "{} lost provided_type value".format(service_provider,),
            )
        if isinstance(plugin_class, str):
            plugin_class_object = self.resolve(
                plugin_class, service_provider.provided_type,
            )
            return service_provider(plugin_class_object)
        else:
            return service_provider(plugin_class)

    def resolve(self, reference, base):
        """Resolve strings to objects using standard import and attribute syntax."""
        name = reference.split(".")
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
            verror = ValueError("Cannot resolve %r: %s" % (reference, e))
            verror.__cause__, verror.__traceback__ = e, tb
            raise verror


def complete():
    """Show completion list."""
    # bash exports COMP_LINE and COMP_POINT, tcsh COMMAND_LINE only
    cline = os.environ.get("COMP_LINE") or os.environ.get("COMMAND_LINE") or ""
    cpoint = int(os.environ.get("COMP_POINT") or len(cline))
    try:
        cloud = CloudSelect()
        profile = cloud.configuration_read()
        args = cloud.parse_args([])
        cloud.fabric(profile, args).complete(cline, cpoint)
    except KeyboardInterrupt:
        # If the user hits Ctrl+C, we don't want to print
        # a traceback to the user.
        pass


def main():
    """Run CloudSelect."""
    cloud = CloudSelect()
    configuration = cloud.configuration_read()

    args = cloud.parse_args(sys.argv[1:])
    if args.profile and not cloud.configuration_exists(args.profile):
        sys.exit('Error: Profile "{}" not found'.format(args.profile))

    # Read configuration part with profile information
    if args.profile:
        configuration = cloud.merge(
            configuration, cloud.configuration_read(args.profile),
        )

    cloud.fabric(configuration, args).select()
