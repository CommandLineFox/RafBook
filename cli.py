import click
from tcp.node import Node

node = None


@click.group()
def cli():
    pass


@cli.command()
@click.argument('config_path')
@click.argument('port', type=int)
def login(config_path, port):
    global node
    if node:
        click.echo("Error: Already logged in. Please stop the current node first.")
        return
    try:
        node = Node(config_path, port)
        click.echo(f"Logged in and node created with config {config_path} and port {port}")
    except ConnectionRefusedError:
        click.echo(f"Error: Cannot connect to bootstrap node")


@cli.command()
@click.argument('address')
@click.argument('port', type=int)
def add_friend(address, port):
    global node
    if not node:
        click.echo("Error: You need to login first")
        return
    node.add_friend(address, port)


@cli.command()
@click.argument('path')
@click.argument('visibility')
def add_file(path, visibility):
    global node
    if not node:
        click.echo("Error: You need to login first")
        return
    node.add_file(path, visibility)


@cli.command()
@click.argument('address')
@click.argument('port', type=int)
def view_files(address, port):
    global node
    if not node:
        click.echo("Error: You need to login first")
        return
    node.view_files(address, port)


@cli.command()
@click.argument('filename')
def remove_file(filename):
    global node
    if not node:
        click.echo("Error: You need to login first")
        return
    node.remove_file(filename)


@cli.command()
def stop():
    global node
    if not node:
        click.echo("Error: You need to login first")
        return
    node.stop()
    node = None


@click.command()
@click.pass_context
def interactive(ctx):
    """Run in interactive mode."""
    while True:
        try:
            command = input("> ")
            ctx.invoke(cli, command)
        except (EOFError, KeyboardInterrupt):
            print("Exiting interactive mode")
            break


if __name__ == '__main__':
    cli.add_command(interactive)
    cli()
