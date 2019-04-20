import click

from miqsel.config import config
from miqsel.server import start, status, stop, urls, viewer


@click.version_option()
@click.group()
def main():
    """Entry point for miqsel"""
    pass


# config command
main.add_command(config)

# server management command
main.add_command(status)
main.add_command(start)
main.add_command(stop)
main.add_command(urls)
main.add_command(viewer)


if __name__ == "__main__":
    main()
