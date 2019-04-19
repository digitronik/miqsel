from tests import miqsel_cmd


def test_miqsel_start(ensure_stopped):
    """Check start of miqsel"""

    out, err, returncode = miqsel_cmd("miqsel start")
    assert "miq_sel container started" in out
    out, err, returncode = miqsel_cmd("miqsel status")
    assert out.strip() == "running"


def test_miqsel_stop(ensure_running):
    """Check stop of miqsel"""

    miqsel_cmd("miqsel stop")
    out, _, _ = miqsel_cmd("miqsel status")
    assert out.strip() == "Not running..."
