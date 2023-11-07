# SPDX-FileCopyrightText: 2023-present Heath Brown <heathd.brown@gmail.com>
#
# SPDX-License-Identifier: MIT
import click
import json

from roku.api import query_device_info
from roku.api import query_apps
from roku.models.roku import RokuDevice

from ..__about__ import __version__


@click.group(context_settings={'help_option_names': ['-h', '--help']}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name='roku-hatch')
@click.pass_context
def cli(ctx: click.Context):
    pass

@cli.command()
@click.argument("ip")
@click.pass_context
def device(ctx:click.Context, ip):
    """Shows Device information from IP
    
    IP is the address of the Roku
    """
    device = RokuDevice(**query_device_info(ip))
    print(f"Connected to Roku: {device.friendly_device_name}")
    print(f"Model Name: {device.model_name}")
    print(f"Model Number: {device.model_number}")
    print(f"Software Version: {device.software_version}")

@cli.command()
@click.argument("ip")
@click.pass_context
def apps(ctx: click.Context, ip):
    """Show the apps from IP
    
    IP is the address of the Roku
    """
    device = RokuDevice(**query_device_info(ip))
    print(f"Connected to Roku: {device.friendly_device_name}")

    apps = query_apps(ip)
    print("Application Found: ")
    for app in apps:
        print(f"              {app}")
