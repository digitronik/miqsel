import click

from miqsel.config import config
from miqsel.server import executor
from miqsel.server import start
from miqsel.server import status
from miqsel.server import stop
from miqsel.server import viewer_cmd
from miqsel.server import vnc


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
main.add_command(viewer_cmd)
main.add_command(vnc)
main.add_command(executor)


if __name__ == "__main__":
    main()
