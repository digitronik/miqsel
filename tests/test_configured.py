import os

import pytest

from tests import miqsel_cmd

DATA = {
    "start": {"status": "running", "msg": "Selenium Server started"},
    "stop": {"status": "stopped", "msg": "Selenium Server stopped"},
}


@pytest.mark.parametrize("state", DATA)
def test_miqsel(state, proj_dir, ensure_stopped):
    """Check start and stop of unconfigured miqsel but run from project"""

    cmd = "miqsel {}".format(state)
    out, _, returncode = miqsel_cmd(cmd)
    assert returncode == 0
    assert DATA[state]["msg"] in out

    if state == "start":
        # For unconfigured miqsel evm.local.yaml will not update
        env_path = os.path.join(proj_dir, "env.local.yaml")
        assert "'env.yaml' not updated" not in out

        # env.local.yaml will create in conf
        assert os.path.isfile(path=env_path)

        with open(env_path, "r") as f:
            assert "command_executor: http://172" in f.read()

    out, _, returncode = miqsel_cmd("miqsel status")
    assert returncode == 0
    assert out.strip() == DATA[state]["status"]


def test_appliance(proj_dir, ensure_stopped):
    """Check appliance set"""
    miqsel_cmd("miqsel start")

    # without appliance set
    out, _, returncode = miqsel_cmd("miqsel appliance")
    assert returncode == 0
    assert out.strip() == ""

    # with appliance set
    app = "192.168.1.1"
    out, _, returncode = miqsel_cmd("miqsel appliance -s {}".format(app))
    assert returncode == 0
    assert out.strip() == "Appliance set to {}".format(app)
    out, _, returncode = miqsel_cmd("miqsel appliance")
    assert out.strip() == app


def test_browser(proj_dir, ensure_stopped):
    """Check browser set"""
    miqsel_cmd("miqsel start")

    # without browser set
    out, _, returncode = miqsel_cmd("miqsel browser")
    assert returncode == 0
    assert out.strip() == "chrome"

    # with browser set
    out, _, returncode = miqsel_cmd("miqsel browser -f")
    assert returncode == 0
    assert out.strip() == "Browser set to firefox"
    out, _, returncode = miqsel_cmd("miqsel browser")
    assert out.strip() == "firefox"


def test_executor_url(proj_dir, ensure_stopped):
    """test executor pointing to"""

    miqsel_cmd("miqsel start")
    out, _, returncode = miqsel_cmd("miqsel executor")
    assert returncode == 0
    assert out.strip() == "http://172.17.0.2:4444/wd/hub"


def test_vnc_url(proj_dir, ensure_stopped):
    """test vnc pointing to"""

    miqsel_cmd("miqsel start")
    out, _, returncode = miqsel_cmd("miqsel vnc")
    assert returncode == 0
    assert out.strip() == "172.17.0.2:5999"
