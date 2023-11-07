import os
import sys
from pathlib import Path

import click
from ruamel.yaml import safe_dump
from ruamel.yaml import safe_load


DEFAULT_CONFIG = {
    "engine": "auto",
    "viewer": "auto",
    "data_dir": "default",
    "image": "quay.io/redhatqe/selenium-standalone",
    "name": "miqsel_container",
    "network": "default",
    "server_port": 4444,
    "vnc_port": 5999,
}
CONTAINER_ENGINES = ["podman", "docker"]
VNC_VIEWERS = ["vncviewer", "vinagre", "xdg-open"]


class Configuration:
    """read write conf yaml files"""

    def __init__(self, conf_file=None):
        self.conf_file = conf_file

    @property
    def config_path(self):
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME")

        if xdg_config_home:
            config_home = Path(xdg_config_home)
        else:
            config_home = Path.home().joinpath(".config")

        conf_dir = config_home.joinpath("miqsel")

        if not conf_dir.exists():
            conf_dir.mkdir()

        return conf_dir.joinpath("config.yaml")

    def read(self):
        if self.config_path.exists():
            with open(self.config_path) as ymlfile:
                return safe_load(ymlfile)
        else:
            self.write(DEFAULT_CONFIG)
            return DEFAULT_CONFIG

    def write(self, cfg):
        with open(self.config_path, "w") as ymlfile:
            return safe_dump(cfg, ymlfile, default_flow_style=True)


@click.command(help="Configure Selenium Server")
@click.option("--reset", is_flag=True, help="Reset configuration to default.")
def config(reset):
    """Config command"""

    conf = Configuration()

    if reset:
        confirm = click.confirm("Are you sure you want to rest configuration?")
        if confirm:
            conf.write(DEFAULT_CONFIG)
            click.echo("Configuration reset to default.")
        sys.exit(0)

    cfg = conf.read()
    clients = ["auto"] + CONTAINER_ENGINES
    cfg["engine"] = click.prompt(
        "Container Engine", type=click.Choice(clients), default=cfg["engine"]
    )
    cfg["image"] = click.prompt("Selenium container image", default=cfg["image"])
    viewers = ["auto"] + VNC_VIEWERS
    cfg["viewer"] = click.prompt("VNC viewer", type=click.Choice(viewers), default=cfg["viewer"])
    cfg["server_port"] = click.prompt(
        "Selenium server running on port?", default=cfg["server_port"]
    )
    cfg["vnc_port"] = click.prompt("VNC running on port?", default=cfg["vnc_port"])
    cfg["name"] = click.prompt("Container name", default=cfg["name"])
    cfg["network"] = click.prompt("Container network", default=cfg["network"])
    cfg["data_dir"] = click.prompt(
        "Testing data mount to directory '/data'", default=cfg["data_dir"]
    )

    conf.write(cfg=cfg)
    click.echo("Configuration saved successfully...")


_config = Configuration().read()
