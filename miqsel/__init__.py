import click

from miqsel.config import config
from miqsel.env import appliance, browser
from miqsel.server import executor, start, status, stop, viewer, vnc


@click.version_option()
@click.group()
def main():
    """Miq Selenium Server"""
    pass


# config command
main.add_command(config)

# server management command
main.add_command(status)
main.add_command(start)
main.add_command(stop)
main.add_command(viewer)
main.add_command(vnc)
main.add_command(executor)

# Env management command
main.add_command(appliance)
main.add_command(browser)

if __name__ == "__main__":
    main()
