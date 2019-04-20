import click

from miqsel.config import config


@click.version_option()
@click.group()
def main():
    """Entry point for miqsel"""
    pass


# config command
main.add_command(config)


if __name__ == "__main__":
    main()
