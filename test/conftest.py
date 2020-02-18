"""PyTest fixtures."""

import logging
import os
from shutil import copyfile

import pytest


@pytest.fixture(autouse=True)
def run_around_tests():
    """Clear logging cache before each test."""
    logging.Logger.manager.loggerDict.clear()
    yield


@pytest.fixture(scope="session")
def cfgdir(tmpdir_factory):
    """Prepare configuration directory for cloudselect."""
    tmp = tmpdir_factory.mktemp("cloudselect")
    src = os.path.join(os.path.dirname(__file__), "fixture", "cloud.json")
    dst = os.path.join(str(tmp), "cloud.json")
    copyfile(src, dst)
    return tmp
