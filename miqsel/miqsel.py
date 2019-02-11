import os
import time

import click
import docker
import yaml


class Connection(object):
    def __init__(self):
        self.client = None
        self.container = None
        self.conf = None


connection = click.make_pass_decorator(Connection, ensure=True)
home = os.environ["HOME"]


@click.version_option()
@click.group()
@connection
def cli(connection):
    try:
        connection.client = docker.from_env()
    except Exception:
        click.echo("Fail to connect docker")
        exit(1)
    conf = Configuration()
    connection.conf = conf.read()
    proj_dir = connection.conf.get("project_dir")

    if proj_dir == "":
        if not os.path.isdir("conf"):
            click.echo(
                "Please run command from project directory or set project directory with config"
            )
            exit(0)


class Configuration(object):
    """Configure miqsel"""

    def __init__(self):
        self.conf_file = "{home}/.config/miqsel/conf.yml".format(home=home)
        dir_path = os.path.dirname(self.conf_file)

        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        if not os.path.isfile(self.conf_file):
            raw_cfg = {
                "project_dir": "",
                "container_name": "miq_sel",
                "image": "cfmeqe/cfme_sel_stable:latest",
                "vnc_port": 5999,
                "server_port": 4444,
            }
            self.write(raw_cfg)

    def read(self):
        with open(self.conf_file, "r") as ymlfile:
            return yaml.load(ymlfile)

    def write(self, cfg):
        with open(self.conf_file, "w") as ymlfile:
            return yaml.safe_dump(cfg, ymlfile, default_flow_style=False)


def set_env(hostname=None, browser=None):
    conf = Configuration().read()
    proj_dir = conf.get("project_dir")
    port = conf.get("server_port")

    if proj_dir != "":
        path = os.path.join(proj_dir, "conf/env.local.yaml")
    else:
        path = "conf/env.local.yaml"

    raw_cfg = {
        "browser": {
            "webdriver": "Remote",
            "webdriver_options": {
                "keep_alive": True,
                "desired_capabilities": {
                    "browserName": "chrome",
                    "platform": "LINUX",
                    "unexpectedAlertBehaviour": "ignore",
                    "acceptInsecureCerts": True,
                    "acceptSslCerts": True,
                },
            },
        }
    }

    try:
        with open(path, "r") as ymlfile:
            env_yaml = yaml.safe_load(ymlfile)
    except IOError:
        env_yaml = {}

    env_yaml = env_yaml if env_yaml else raw_cfg
    if hostname:
        url = "http://{host}:{port}/wd/hub".format(host=hostname, port=port)
        env_yaml["browser"]["webdriver_options"]["command_executor"] = url
    if browser:
        env_yaml["browser"]["webdriver_options"]["desired_capabilities"]["browserName"] = browser
    with open(path, "w") as ymlfile:
        yaml.safe_dump(env_yaml, ymlfile, default_flow_style=False)


@cli.command(help="Configure Miq Selenium webdriver")
def config():
    conf = Configuration()
    cfg = conf.read()

    cfg["project_dir"] = click.prompt("Miq project working dir", default=cfg.get("project_dir"))
    cfg["container_name"] = click.prompt("Container name", default=cfg.get("container_name"))
    cfg["image"] = click.prompt("Docker selenium driver image", default=cfg.get("image"))
    cfg["vnc_port"] = click.prompt("VNC running on port?", default=cfg.get("vnc_port"))
    cfg["server_port"] = click.prompt(
        "Selenium server running on port?", default=cfg["server_port"]
    )
    conf.write(cfg=cfg)
    click.echo("Configuration saved successfully...")


@connection
def get_container(connection):
    try:
        return connection.client.containers.get(connection.conf.get("container_name"))
    except docker.errors.NotFound:
        return None


@cli.command(help="Miq Selenium Server Hostname")
def hostname():
    container = get_container()
    host = container.attrs["NetworkSettings"]["IPAddress"] if container else None
    click.echo(host)
    return host


@cli.command(help="VNC viewer")
@click.option("-u", "--url", default=None, help="Server url with port <hostname:port>")
@connection
@click.pass_context
def viewer(ctx, connection, url):
    if not url:
        host = ctx.invoke(hostname)
        if host:
            url = "{hostname}:{port}".format(hostname=host, port=connection.conf.get("vnc_port"))
        else:
            click.echo("Selenium server not running...")
            exit(0)
    os.system("vncviewer {url}&".format(url=url))


@cli.command(help="VNC and Command Executor URL's")
@click.pass_context
def urls(ctx):
    host = ctx.invoke(hostname)
    conf = Configuration().read()

    click.echo(
        "Command Executor: http://{host}:{port}/wd/hub".format(
            host=host, port=conf.get("server_port")
        )
    )
    click.echo("VNC: {host}:{port}".format(host=host, port=conf.get("vnc_port")))


@cli.command(help="Start Miq Selenium Server")
@connection
@click.pass_context
def start(ctx, connection):
    container = get_container()
    img = connection.conf.get("image")
    name = connection.conf.get("container_name")

    if not container:
        if not connection.client.images.list(name=img):
            click.echo("Pulling docker images...")
            click.echo("It will take some time; Please wait...")

        connection.client.containers.run(img, name=name, detach=True, auto_remove=True)
        click.echo("{} container started".format(name))
        time.sleep(5)

        t0 = time.time()
        while True:
            host = ctx.invoke(hostname)
            if host:
                break
            elif time.time() > (t0 + 20):
                click.echo("Timeout: Fail to get hostname. Check for selenium server status")
                exit(0)

        set_env(hostname=host)
        ctx.invoke(viewer)

    elif getattr(container, "status", None) == "exited":
        container.start()
        click.echo("{} container started".format(name))
    else:
        click.echo("Container in {} state".format(container.status))


@cli.command(help="Stop Miq Selenium Server")
def stop():
    container = get_container()

    if getattr(container, "status", None) == "running":
        container.stop()
    else:
        click.echo("Nothing to stop")


@cli.command(help="Status of Miq Selenium Server")
def status():
    container = get_container()
    if container:
        click.echo(container.status)
    else:
        click.echo("Not running...")


@cli.command(help="Set Browser")
@click.option("-c", "--chrome", "browser", flag_value="chrome", default=True, help="Chrome")
@click.option("-f", "--firefox", "browser", flag_value="firefox", help="Firefox")
def browser(browser):
    set_env(browser=browser)
