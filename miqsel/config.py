import os

import click
from ruamel.yaml import safe_load, safe_dump


class Configuration(object):
    """read write conf yaml files"""

    def __init__(self, conf_file=None):
        self.conf_file = (
            conf_file if conf_file else os.path.join(os.path.dirname(__file__), "conf.yaml")
        )

    def read(self):
        with open(self.conf_file, "r") as ymlfile:
            return safe_load(ymlfile)

    def write(self, cfg):
        with open(self.conf_file, "w") as ymlfile:
            return safe_dump(cfg, ymlfile, default_flow_style=False)


@click.command(help="Configure Miq Selenium Server")
def config():
    """Config command"""

    conf = Configuration()
    cfg = conf.read()

    cfg["container"]["project"] = click.prompt(
        "Miq project working dir", default=cfg["container"]["project"]
    )
    cfg["container"]["name"] = click.prompt("Container name", default=cfg["container"]["name"])
    cfg["container"]["image"] = click.prompt(
        "Docker selenium driver image", default=cfg["container"]["image"]
    )
    cfg["container"]["vnc_port"] = click.prompt(
        "VNC running on port?", default=cfg["container"]["vnc_port"]
    )
    cfg["container"]["server_port"] = click.prompt(
        "Selenium server running on port?", default=cfg["container"]["server_port"]
    )
    conf.write(cfg=cfg)
    click.echo("Configuration saved successfully...")
