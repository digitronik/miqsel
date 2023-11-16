from tests import miqsel_cmd


def test_help():
    """Check Status of miqsel"""

    out, _, returncode = miqsel_cmd("miqsel")
    assert returncode == 0
    assert "Usage: miqsel [OPTIONS] COMMAND [ARGS]" in out


def test_config():
    pass


def test_executor(ensure_running):
    out, _, returncode = miqsel_cmd("miqsel executor")
    assert returncode == 0
    assert "http://localhost:4444/wd/hub" in out


def test_vnc(ensure_running):
    out, _, returncode = miqsel_cmd("miqsel vnc")
    assert returncode == 0
    assert "localhost:5999" in out


def test_start(ensure_stopped):
    out, _, returncode = miqsel_cmd("miqsel start --no-viewer")
    assert returncode == 0
    assert "Selenium Server started" in out


def test_status(ensure_stopped):
    out, _, returncode = miqsel_cmd("miqsel status")
    assert returncode == 0
    assert "stopped" in out
    miqsel_cmd("miqsel start --no-viewer")
    out, _, returncode = miqsel_cmd("miqsel status")
    assert returncode == 0
    assert "running" in out


def test_stop(ensure_running):
    out, _, returncode = miqsel_cmd("miqsel stop")
    assert returncode == 0
    assert "Selenium Server stopped" in out


def test_viewer():
    pass
