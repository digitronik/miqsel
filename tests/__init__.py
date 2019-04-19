import subprocess


def miqsel_cmd(cmd):
    """
    Runs a miqsel shell command, and returns the output, err, returncode
    """
    ret = subprocess.Popen(
        cmd,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
    )
    out, err = ret.communicate()
    returncode = ret.returncode
    return out.decode(), err.decode(), returncode
