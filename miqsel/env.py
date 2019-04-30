import os

import click
from ruamel.yaml import safe_load, safe_dump

from miqsel.config import Configuration


class LocalEnv(object):
    """Local env file management"""

    def __init__(self):
        self.cfg = Configuration().read()

    @property
    def project(self):
        """ Project directory

        :return: project directory
        """
        return self.cfg["container"]["project"]

    @property
    def env_file(self):
        """ Environment file

        :return: environment file if not None
        """
        if os.path.isdir("conf"):
            # First check miqsel running from project dir
            return os.path.join("conf", "env.local.yaml")
        elif self.project:
            # Second check miqsel project path set or not
            return os.path.join(self.project, "conf", "env.local.yaml")
        else:
            return os.path.join("tmp", "env.local.yaml")

    @property
    def in_env(self):
        """ Check we are in env or not.
        :return: return bool
        """
        proj_dir = os.path.dirname(self.env_file)
        return os.path.isdir(proj_dir)

    def read(self):
        """Read Environment file

        :return: dict
        """
        with open(self.env_file, "r") as ymlfile:
            return safe_load(ymlfile)

    def write(self, cfg):
        """ Write Environment file

        :param cfg: dict to write
        """
        if self.in_env:
            with open(self.env_file, "w") as ymlfile:
                return safe_dump(cfg, ymlfile, default_flow_style=False)
        else:
            click.echo(
                "Project directory need set or run from Project directory; 'env.yaml' not updated"
            )

    @property
    def env(self):
        """Read environment
        :return: if env file exist return else sample conf
        """
        return self.read() if os.path.isfile(self.env_file) else self.cfg["miq"]

    @property
    def appliance(self):
        """appliance from env

        :return: return current appliance
        """
        return self.env["appliances"][0]["hostname"]

    @appliance.setter
    def appliance(self, value):
        """Setter for appliance

        :param value: appliance
        """
        if self.appliance != value:
            cfg = self.env
            cfg["appliances"][0]["hostname"] = value
            self.write(cfg)

    @property
    def executor(self):
        """Executor form env

        :return: executor url
        """
        return self.env["browser"]["webdriver_options"]["command_executor"]

    @executor.setter
    def executor(self, value):
        """Setter for executor

        :param value: executor url
        """
        if self.browser != value:
            cfg = self.env
            cfg["browser"]["webdriver_options"]["command_executor"] = value
            self.write(cfg)

    @property
    def browser(self):
        """Browser from env"""
        return self.env["browser"]["webdriver_options"]["desired_capabilities"]["browserName"]

    @browser.setter
    def browser(self, value):
        """Setter for browser

        :param value: browser (chrome/ firefox)
        """
        if self.browser != value:
            cfg = self.env
            cfg["browser"]["webdriver_options"]["desired_capabilities"]["browserName"] = value
            self.write(cfg)


@click.command(help="Set Browser")
@click.option("-c", "--chrome", "browser", flag_value="chrome", help="Chrome")
@click.option("-f", "--firefox", "browser", flag_value="firefox", help="Firefox")
def browser(browser):
    """Browser command

    :param browser: --chrome[-c] or --firefox[-f]
    """

    env = LocalEnv()

    if browser:
        click.echo("Browser set to {}".format(browser))
        env.browser = browser
    else:
        click.echo(env.browser)


@click.command(help="Set Appliance")
@click.option("-s", "--set", "app", default=None, help="Set Appliance")
def appliance(app):
    """Appliance command

    :param app: --set[-s]
    """

    env = LocalEnv()

    if app:
        click.echo("Appliance set to {}".format(app))
        env.appliance = app
    else:
        click.echo(env.appliance)
