# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module that invoke FZF on list of discovered instances.

This module is invoked by CloudSelect when all data is prepared:
-   configuration is loaded;
-   plugins are resolved and loaded;
-   arguments are parsed.

The entry point is select function.
"""

import logging
import os
import subprocess
import sys

from cloudselect import Container


class Selector:
    """Selector class that selects cloud instances."""

    logger = None

    def __init__(self):
        """Class constructor."""
        self.logger = logging.getLogger("cloudselect.Selector")

    def complete(self, cline, cpoint):
        """List profiles for shell completion."""
        configpath = Container.configpath()
        extension = Container.extension()

        prefix = cline[0:cpoint].partition(" ")[-1]
        self.logger.debug(
            "Complete line %s, point %s, prefix %s", cline, cpoint, prefix,
        )
        for profile in os.listdir(configpath):
            if profile.endswith(".{}".format(extension)):
                name = profile.replace(".{}".format(extension), "")
                if name.startswith(prefix):
                    print(name)

    def edit(self, configuration):
        """Edit profile or shared configuration file if file is None."""
        self.logger.debug("Edit '%s'", configuration)
        if not os.path.isfile(configuration):
            self.logger.info("%s does not exists", configuration)
        editor = self.get_editor()
        os.execvp(editor, [editor, configuration])

    @staticmethod
    def execute(program, args, **kwargs):
        """Execute a command in a subprocess and returns its standard output."""
        return (
            subprocess.run(
                [program] + args, stdout=subprocess.PIPE, check=False, **kwargs
            )
            .stdout.decode()
            .strip()
        )

    def fzf_select(self, instances):
        """Invoke FZF with list of instances and return selected."""
        fzf_options = Container.config.fzf() or ["-1", "-m", "--with-nth", "2.."]

        def find(instance_id):
            return next(x for x in instances if x.id == instance_id)

        fzf_input = "\n".join("\t".join(i.representation) for i in instances).encode()
        selected = self.execute("fzf", fzf_options, input=fzf_input)
        if not selected:
            sys.exit("Error: No instances selected")
        if "\t" not in selected:
            raise AssertionError(
                "There should be at least 2 fields in instance representation: id and something meaningful",
            )
        return [find(i.split("\t", 1)[0]) for i in selected.split("\n")]

    def get_editor(self):
        """Get editor path."""
        config = Container.config
        if config.editor():
            return config.editor()
        for key in "VISUAL", "EDITOR":
            rv = os.environ.get(key)
            if rv:
                return rv
        for editor in "vim", "nano":
            try:
                return subprocess.check_output(  # noqa: DUO116
                    "which {} >/dev/null 2>&1".format(editor), shell=False,
                )
            except subprocess.CalledProcessError as exc:
                self.logger.warning("Unable to fild editor: %s", str(exc))
        return "vi"

    def profile_list(self):
        """List available profiles."""
        configpath = Container.configpath()
        extension = Container.extension()

        self.logger.debug("List all available profiles from %s", configpath)
        empty = True
        print("CloudSelect profiles:")
        for profile in os.listdir(configpath):
            if profile.endswith(".{}".format(extension)):
                empty = False
                print("- {}".format(profile.replace(".{}".format(extension), "")))
        if empty:
            print("- NO PROFILES -")

    def profile_process(self):
        """Run selection process for the specific profile."""
        discovery = Container.discovery()
        pathfinder = Container.pathfinder()
        profile_name = Container.args().profile
        report = Container.report()

        self.logger.debug("Process profile '%s'", profile_name)
        instances = discovery.run()
        if not instances:
            sys.exit("Error: No instances found")
        selected = self.fzf_select(instances)
        selected = [pathfinder.run(i, instances) for i in selected]
        return report.run(selected)

    @staticmethod
    def reporter_list():
        """List available reporters."""
        empty = True
        print("CloudSelect reporters:")
        for reporter in sorted(
            Container.config().get("plugin", {}).get("report", {}).keys(),
        ):
            empty = False
            print("- {}".format(reporter))
        if empty:
            print("- NO REPORTERS -")

    def select(self):
        """Entry point. Select instances."""
        args = Container.args()
        configpath = Container.configpath()
        extension = Container.extension()

        if args.edit is None or args.edit:
            if args.edit is None:
                configuration = os.path.join(configpath, "{}".format(extension))
                return self.edit(configuration)
            profile = os.path.join(configpath, "{}.{}".format(args.edit, extension))
            return self.edit(profile)
        if args.reporter is None:
            return self.reporter_list()
        if not args.profile:
            return self.profile_list()
        return self.profile_process()
