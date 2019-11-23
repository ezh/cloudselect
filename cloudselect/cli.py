import argparse
import logging
import sys
from logging.config import dictConfig

import cloudselect
from cloudselect import cloudselect as abc


class Cli:
    logger = None
    logging_config = dict(
        version=1,
        formatters={
            "f": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"}
        },
        handlers={
            "h": {
                "class": "logging.StreamHandler",
                "formatter": "f",
                "level": logging.DEBUG,
            }
        },
        root={"handlers": ["h"], "level": logging.ERROR},
    )

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
            "--edit", "-e", nargs="?", default=False, help="edit configuration or profile"
        )
        parser.add_argument("profile", nargs="?")
        return parser.parse_args(args)

    def logging(self, level):
        if level == 1:
            self.logging_config["root"]["level"] = logging.INFO
        elif level and level > 1:
            self.logging_config["root"]["level"] = logging.DEBUG
        dictConfig(self.logging_config)
        self.logger = logging.getLogger("cloudselect.Cli")
        self.logger.debug("Logging is initialized")


def main():
    cli = Cli()
    args = cli.parse_args(sys.argv[1:])
    cli.logging(args.verbose)
    abc.CloudSelect().run(args)
