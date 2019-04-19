import os

from tests import miqsel_cmd


def test_miqsel_help():
    """Check Status of miqsel"""
    out, err, returncode = miqsel_cmd("miqsel")
    assert returncode == 0
    assert "Usage: miqsel [OPTIONS] COMMAND [ARGS]" in out


def test_miqsel_unconfigured():
    """Check Status of unconfigured miqsel"""
    os.system("rm -rf ~/.config/miqsel/conf.yml")
    out, err, returncode = miqsel_cmd("miqsel status")
    assert returncode == 0
    assert (
        out.strip()
        == "Please run command from project directory or set project directory with config"
    )


def test_miqsel_configured(ensure_stopped):
    out, err, returncode = miqsel_cmd("miqsel status")
    assert returncode == 0
    assert out.strip() == "Not running..."
