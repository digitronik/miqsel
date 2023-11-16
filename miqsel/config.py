import json
import os
import sys
from pathlib import Path

import click


DEFAULT_CONFIG = {
    "engine": "auto",
    "viewer": "auto",
    "data_dir": "default",
    "image": "quay.io/redhatqe/selenium-standalone",
    "name": "miqsel_container",
    "network": "default",
    "server_port": 4444,
    "vnc_port": 5999,
    "shm_size": "2g",
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

        conf_path = config_home.joinpath("miqsel").joinpath("config.json")
        conf_path.parent.mkdir(parents=True, exist_ok=True)
        return conf_path

    def read(self):
        if self.config_path.exists():
            return json.loads(self.config_path.read_text(encoding="utf-8"))
        else:
            self.write(DEFAULT_CONFIG)
            return DEFAULT_CONFIG

    def write(self, cfg: dict):
        self.config_path.write_text(json.dumps(cfg), encoding="utf-8")


@click.command(help="Set Configuration")
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
    cfg["name"] = click.prompt("Selenium container name", default=cfg["name"])
    cfg["network"] = click.prompt("Selenium container network", default=cfg["network"])
    cfg["shm_size"] = click.prompt("Selenium container shared Memory", default=cfg["shm_size"])
    cfg["data_dir"] = click.prompt(
        "Testing data mount to directory '/data'", default=cfg["data_dir"]
    )

    conf.write(cfg=cfg)
    click.echo("Configuration saved successfully...")


_config = Configuration().read()
