import os
import shutil
from subprocess import PIPE, Popen

import pytest

from tests import miqsel_cmd


@pytest.fixture(scope="module")
def config():
    """Configured miqsel"""
    if not os.path.isdir("conf"):
        os.mkdir("conf")
    proc = Popen(["miqsel", "config"], stdin=PIPE, stdout=PIPE)
    input = str.encode("{}\n\n\n\n\n".format(os.getcwd()))
    proc.communicate(input=input)
    yield
    if os.path.isdir("conf"):
        shutil.rmtree("conf")


@pytest.fixture(scope="module")
def proj_dir():
    """Create Project dir"""

    # `conf` is identity that you are in project where we create evm.local.yaml
    if not os.path.isdir("conf"):
        os.mkdir("conf")
    yield "conf"
    if os.path.isdir("conf"):
        shutil.rmtree("conf")


@pytest.fixture(scope="module")
def ensure_stopped():
    out, _, _ = miqsel_cmd("miqsel status")
    if out.strip() == "running":
        miqsel_cmd("miqsel stop")


@pytest.fixture(scope="module")
def ensure_running():
    out, _, _ = miqsel_cmd("miqsel status")
    if out.strip() != "running":
        miqsel_cmd("miqsel start")
