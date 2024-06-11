import click
from tcp.node import Node

node = None


@click.group()
def cli():
    pass


@cli.command()
@click.argument('port', type=int)
def login(port):
    global node
    if node:
        click.echo("Error: Already logged in. Please stop the current node first.")
        return
    node = Node(port=port)
    click.echo(f"Logged in and node created with port {port}")


@cli.command()
@click.argument('message')
def send(message):
    global node
    if not node:
        click.echo("Error: You need to login first")
        return
    node.send_message(message)


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
            command = input("> ").strip()
            if not command:
                continue
            args = command.split()
            cmd_name = args[0]
            cmd_args = args[1:]
            cmd = cli.get_command(ctx, cmd_name)
            if cmd:
                ctx.forward(cmd, *cmd_args)
            else:
                click.echo(f"Unknown command: {cmd_name}")
        except (EOFError, KeyboardInterrupt):
            print("Exiting interactive mode")
            break


if __name__ == '__main__':
    cli.add_command(interactive)
    cli()
