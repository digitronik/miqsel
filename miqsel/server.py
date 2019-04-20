import time
from subprocess import PIPE, Popen

import click
import docker

from miqsel.config import Configuration
from miqsel.env import LocalEnv


class Server(object):
    """Selenium Server Management"""

    def __init__(self):
        self.client = docker.from_env(version="auto")
        self.cfg = Configuration().read()

    @property
    def container(self):
        """
        Get running selenium container
        :return: if container running return container object else None
        """

        try:
            return self.client.containers.get(self.cfg["container"]["name"])
        except docker.errors.NotFound:
            return None

    @property
    def hostname(self):
        """
        Get ip allocated to container
        :return: If container running return ip else None
        """

        return self.container.attrs["NetworkSettings"]["IPAddress"] if self.container else None

    @property
    def executor(self):
        """
        Get executor url
        :return: If container running return executor url else None
        """

        return (
            "http://{host}:{port}/wd/hub".format(
                host=self.hostname, port=self.cfg["container"]["server_port"]
            )
            if self.hostname
            else None
        )

    @property
    def vnc(self):
        """
        Get vnc url
        :return: If container running return vnc url else None
        """

        return (
            "{host}:{port}".format(host=self.hostname, port=self.cfg["container"]["vnc_port"])
            if self.hostname
            else None
        )

    def start(self):
        """Start selenium container"""

        img = self.cfg["container"]["image"]
        name = self.cfg["container"]["name"]

        if not self.container:
            if not self.client.images.list(name=img):
                click.echo("Pulling docker images...")
                click.echo("It will take some time; Please wait...")

            self.client.containers.run(img, name=name, detach=True, auto_remove=True)
            time.sleep(5)

            t0 = time.time()
            while True:
                if self.hostname:
                    break
                elif time.time() > (t0 + 30):
                    click.echo("Timeout: Fail to get hostname. Check for selenium server status")
                    exit(0)

        elif getattr(self.container, "status", None) == "exited":
            self.container.start()
        else:
            click.echo("Need to check container status...")

    def stop(self):
        """Stop selenium container if running"""

        if getattr(self.container, "status", None) == "running":
            self.container.stop()

    @property
    def status(self):
        """
        Get status of selenium container
        :return: container status if running else stopped
        """

        if self.container:
            return self.container.status
        else:
            return "stopped"


@click.command(help="Status of Selenium Server")
def status():
    """status command"""

    miq = Server()
    click.echo(miq.status)


@click.command(help="Start Selenium Server")
@click.pass_context
def start(ctx):
    """start command"""

    miq = Server()
    if miq.status == "stopped":
        try:
            miq.start()
            click.echo("Selenium Server started")
        except Exception:
            click.echo("Fail to start Selenium Server")
            raise

        env = LocalEnv()
        env.executor = miq.executor
        ctx.invoke(viewer)
    else:
        click.echo("Server in running state")


@click.command(help="Stop Selenium Server")
def stop():
    """stop command"""

    miq = Server()
    if miq.status == "running":
        miq.stop()
        click.echo("Selenium Server stopped")
    else:
        click.echo("Server not running...")


@click.command(help="Selenium executor URL")
def executor():
    """executor url command"""

    miq = Server()
    if miq.status == "running":
        click.echo(miq.executor)
    else:
        click.echo("Server not running...")


@click.command(help="VNC URL")
def vnc():
    """vnc url command"""

    miq = Server()
    if miq.status == "running":
        click.echo(miq.vnc)
    else:
        click.echo("Server not running...")


@click.command(help="VNC viewer")
@click.option("-u", "--url", default=None, help="Server url with port <hostname:port>")
def viewer(url):
    """vnc viewer command

    :param url: Server url with port <hostname:port>
    """

    url = url if url else Server().vnc
    if url:
        try:
            Popen(["vncviewer", url], stdout=PIPE)
        except FileNotFoundError:
            click.echo("Need vnc viewer... Check README")
    else:
        click.echo("Server not running...")
