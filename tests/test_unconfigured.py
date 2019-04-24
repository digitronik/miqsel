import pytest

from tests import miqsel_cmd

DATA = {
    "start": {"status": "running", "msg": "Selenium Server started"},
    "stop": {"status": "stopped", "msg": "Selenium Server stopped"},
}


def test_miqsel_help():
    """Check Status of miqsel"""

    out, _, returncode = miqsel_cmd("miqsel")
    assert returncode == 0
    assert "Usage: miqsel [OPTIONS] COMMAND [ARGS]" in out


@pytest.mark.parametrize("state", DATA)
def test_miqsel_status(state, ensure_stopped):
    """Check Status of unconfigured miqsel"""

    cmd = "miqsel {}".format(state)
    miqsel_cmd(cmd)
    out, _, returncode = miqsel_cmd("miqsel status")
    assert returncode == 0
    assert out.strip() == DATA[state]["status"]


@pytest.mark.parametrize("state", DATA)
def test_miqsel(state, ensure_stopped):
    """Check start and stop of unconfigured miqsel"""
    cmd = "miqsel {}".format(state)
    out, _, returncode = miqsel_cmd(cmd)
    assert returncode == 0

    assert DATA[state]["msg"] in out

    if state == "start" and DATA[state]["status"] == "running":
        # For unconfigured miqsel evm.yaml will not update
        assert "'env.yaml' not updated" in out

    out, _, returncode = miqsel_cmd("miqsel status")
    assert returncode == 0
    assert out.strip() == DATA[state]["status"]


def test_appliance_browser(ensure_running):
    """Check appliance and browser"""
    out, _, returncode = miqsel_cmd("miqsel browser")
    assert returncode == 0
    assert out.strip() == "chrome"

    out, _, returncode = miqsel_cmd("miqsel appliance")
    assert returncode == 0
    assert out.strip() == ""
