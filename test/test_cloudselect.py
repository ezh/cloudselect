import argparse
from unittest import mock

from cloudselect.cli import Cli


@mock.patch(
    "argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(version=True)
)
def test_ok(mock_args):
    print("ok")
