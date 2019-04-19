import os
from subprocess import PIPE, Popen

import pytest
from tests import miqsel_cmd


@pytest.fixture(scope="module")
def config():
    """Configured miqsel"""
    if not os.path.isdir("conf"):
        os.mkdir("conf")
    path = os.path.join(os.getcwd(), "conf")
    proc = Popen(["miqsel", "config"], stdin=PIPE, stdout=PIPE)
    input = str.encode("{}\n\n\n\n\n".format(path))
    proc.communicate(input=input)
    yield
    if os.path.isdir("conf"):
        os.rmdir("conf")


@pytest.fixture(scope="module")
def ensure_stopped(config):
    out, _, _ = miqsel_cmd("miqsel status")
    if out.strip() == "running":
        miqsel_cmd("miqsel stop")


@pytest.fixture(scope="module")
def ensure_running(config):
    out, _, _ = miqsel_cmd("miqsel status")
    if out.strip() != "running":
        miqsel_cmd("miqsel start")
