# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
import logging
import os
import subprocess

from cloudselect import Container


class Selector:
    logger = None

    def __init__(self):
        self.logger = logging.getLogger("cloudselect.Selector")

    def complete(self, cline, cpoint):
        configpath = Container.configpath()
        extension = Container.extension()

        prefix = cline[0:cpoint].partition(" ")[-1]
        self.logger.debug(
            "Complete line {}, point {}, prefix".format(cline, cpoint, prefix)
        )
        for file in os.listdir(configpath):
            if file.endswith(".{}".format(extension)):
                name = file.replace(".{}".format(extension), "")
                if name.startswith(prefix):
                    print(name)

    def edit(self, file):
        self.logger.debug("Edit '{}'".format(file))
        if not os.path.isfile(file):
            self.logger.info("{} does not exists".format(file))
        editor = self.get_editor()
        os.execvp(editor, [editor, file])

    def execute(self, program, args, **kwargs):
        """Executes a command in a subprocess and returns its standard output."""
        return (
            subprocess.run([program, *args], stdout=subprocess.PIPE, **kwargs)
            .stdout.decode()
            .strip()
        )

    def fzf_select(self, instances):
        fzf_options = Container.config.fzf() or ["-m", "--with-nth", "2.."]

        def find(instance_id):
            return next(x for x in instances if x.id == instance_id)

        fzf_input = "\n".join("\t".join(i.representation) for i in instances).encode()
        selected = self.execute("fzf", fzf_options, input=fzf_input)
        assert (
            "\t" in selected
        ), "There should be at least 2 fields in instance representation: id and something meaningful"
        return [find(i.split("\t", 1)[0]) for i in selected.split("\n")]

    def get_editor(self):
        config = Container.config
        if config.editor():
            return config.editor()
        for key in "VISUAL", "EDITOR":
            rv = os.environ.get(key)
            if rv:
                return rv
        for editor in "vim", "nano":
            if os.system("which %s >/dev/null 2>&1" % editor) == 0:
                return editor
        return "vi"

    def profile_list(self):
        configpath = Container.configpath()
        extension = Container.extension()

        self.logger.debug("List all available profiles from {}".format(configpath))
        empty = True
        print("CloudSelect profiles:")
        for file in os.listdir(configpath):
            if file.endswith(".{}".format(extension)):
                empty = False
                print("- {}".format(file.replace(".{}".format(extension), "")))
        if empty:
            print("- NO PROFILES -")

    def profile_process(self):
        discovery = Container.discovery()
        profile_name = Container.args().profile
        report = Container.report()

        self.logger.debug("Process profile '{}'".format(profile_name))
        instances = discovery.run()
        selected = self.fzf_select(instances)
        report.run(selected)

    def select(self):
        args = Container.args()
        configpath = Container.configpath()
        extension = Container.extension()

        if args.edit is None or args.edit:
            if args.edit is None:
                configuration = os.path.join(configpath, "{}".format(extension))
                self.edit(configuration)
            else:
                profile = os.path.join(configpath, "{}.{}".format(args.edit, extension))
                self.edit(profile)
        if not args.profile:
            self.profile_list()
        else:
            self.profile_process()
