import click
import main
import json


token = None

@click.group()
def cli():
    """Unofficial CAME Connect CLI."""
    # Fetch a token for the CLI duration
    # TODO: Don't fetch if you're calling --help
    global token
    token = main.fetch_token()

@cli.group()
def devices():
    """Manage Devices."""

@cli.group()
def site():
    """Manages Sites."""

@site.command("read")
def sites_read():
    """Read sites"""
    sites = main.fetch_sites(token)
    click.echo(json.dumps(sites, indent=2))

@devices.command("read")
def devices_read():
    """Read Devices"""
    devices = main.fetch_devices(token)
    click.echo(json.dumps(devices, indent=2))

@devices.command("status")
def devices_status():
    """Read Device Statuses"""
    statuses = main.fetch_device_statuses(token)
    click.echo(json.dumps(statuses, indent=2))

@devices.command("commands")
@click.argument("device_id", type=int)
def device_commands(device_id):
    """Read Device Commands"""
    commands = main.fetch_commands_for_device(token, device_id)
    click.echo(json.dumps(commands, indent=2))

@devices.command("run_command")
@click.argument("device_id", type=int)
@click.argument("command_id", type=int)
def device_run_command(device_id, command_id):
    """Run a Device Command"""
    run = main.run_command_for_device(token, device_id, command_id)
    click.echo(json.dumps(run, indent=2))


if __name__ == '__main__':
    cli()
