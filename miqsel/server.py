import shutil
import subprocess
import sys
import time

import click

from miqsel.config import _config
from miqsel.config import CONTAINER_ENGINES
from miqsel.config import VNC_VIEWERS


class SeleniumContainer:
    """Selenium Server Management"""

    def __init__(
        self,
        image=None,
        name=None,
        server_port=None,
        vnc_port=None,
        data_dir=None,
        network=None,
        shm_size=None,
        viewer=None,
    ):
        self.cfg = _config
        self.image = image or self.cfg["image"]
        self.name = name or self.cfg["name"]
        self.server_port = server_port or self.cfg["server_port"]
        self.vnc_port = vnc_port or self.cfg["vnc_port"]
        self.data_dir = data_dir or self.cfg["data_dir"]
        self.network = network or self.cfg["network"]
        self.shm_size = shm_size or self.cfg["shm_size"]
        self.viewer = viewer or self.cfg["viewer"]

    @property
    def client(self):
        _client = self.cfg["engine"]

        if _client == "auto":
            try:
                _client = next(c for c in CONTAINER_ENGINES if shutil.which(c))
            except StopIteration:
                click.echo(
                    f"No container engine found on machine. "
                    f"Install one of {CONTAINER_ENGINES}"
                )
        if shutil.which(_client):
            return _client
        else:
            click.echo(f"Container client {_client} not found")

    @property
    def is_running(self):
        cmd = subprocess.run([self.client, "ps"], stdout=subprocess.PIPE)
        return self.name in cmd.stdout.decode()

    @property
    def is_stale(self):
        cmd = subprocess.run([self.client, "ps", "-a"], stdout=subprocess.PIPE)
        return self.name in cmd.stdout.decode() and not self.is_running

    @property
    def executor(self):
        """
        Get executor url
        :return: If container running return executor url else None
        """

        return f"http://localhost:{self.server_port}/wd/hub"

    @property
    def vnc(self):
        """
        Get vnc url
        :return: If container running return vnc url else None
        """

        return f"localhost:{self.vnc_port}"

    def start(self, **kwargs):
        """Start selenium container"""
        if self.is_stale:
            cmd = [self.client, "rm", self.name]
            subprocess.run(cmd)

        if not self.is_running:
            cmd = [
                self.client,
                "run",
                "-d",
                "--rm",
                f"--shm-size={self.shm_size}",
                "--expose",
                str(self.vnc_port),
                "--expose",
                str(self.server_port),
                "-p",
                f"{self.vnc_port}:{self.vnc_port}",
                "-p",
                f"{self.server_port}:{self.server_port}",
                "-e",
                "SE_VNC_NO_PASSWORD=1",
                "--name",
                self.name,
            ]
            if self.network != "default":
                cmd.extend(["--network", self.network])
            if self.data_dir != "default":
                cmd.extend(["-v", f"{self.data_dir}:/data:z"])
            cmd.append(self.image)
            subprocess.run(cmd)
            # hack some time to stable
            time.sleep(2)

    def stop(self):
        """Stop selenium container if running"""
        subprocess.run([self.client, "stop", self.name])

    @property
    def status(self):
        """
        Get status of selenium container
        :return: container status if running else stopped
        """
        return "running" if self.is_running else "stopped"


@click.command(help="Status of Selenium Server")
def status():
    """status command"""

    miq = SeleniumContainer()
    click.echo(miq.status)


@click.command(help="Start Selenium Server")
@click.option("--viewer/--no-viewer", default=True)
@click.pass_context
def start(ctx, viewer):
    """start command"""

    miq = SeleniumContainer()
    if not miq.is_running:
        try:
            miq.start()
            click.echo("Selenium Server started")
            if viewer:
                ctx.invoke(viewer_cmd)

        except Exception:
            click.echo("Fail to start Selenium Server")
            raise
        # ctx.invoke(viewer)
    else:
        click.echo("Server in running state")


@click.command(help="Stop Selenium Server")
def stop():
    """stop command"""

    miq = SeleniumContainer()
    if miq.is_running:
        miq.stop()
        click.echo("Selenium Server stopped")
    else:
        click.echo("Server not running...")


@click.command(help="Selenium executor URL")
def executor():
    """executor url command"""

    miq = SeleniumContainer()
    if miq.status == "running":
        click.echo(miq.executor)
    else:
        click.echo("Server not running...")


@click.command(help="VNC URL")
def vnc():
    """vnc url command"""

    miq = SeleniumContainer()
    if miq.status == "running":
        click.echo(miq.vnc)
    else:
        click.echo("Server not running...")


@click.command("viewer", help="VNC viewer")
@click.option(
    "-u", "--url", default=None, help="Server url with port <hostname:port>"
)
def viewer_cmd(url):
    """vnc viewer command

    :param url: Server url with port <hostname:port>
    """
    miq = SeleniumContainer()

    if not miq.is_running:
        click.echo("Server not running...")
        sys.exit(1)

    url = url if url else miq.vnc

    try:
        _viewer = next(v for v in VNC_VIEWERS if shutil.which(v))
    except StopIteration:
        click.echo(f"No vnc viewer found. Install one of {VNC_VIEWERS}")

    subprocess.Popen([_viewer, url], stdout=subprocess.PIPE)
