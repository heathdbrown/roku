# SPDX-FileCopyrightText: 2023-present Heath Brown <heathd.brown@gmail.com>
#
# SPDX-License-Identifier: MIT
import asyncio
import time

import click
from pygments import formatters, highlight
from ssdp import messages, network
from ssdp.aio import SSDP
from ssdp.lexers import SSDPLexer

from roku.api import query_device_info
from roku.api import query_apps
from roku.models.roku import RokuDevice

from ..__about__ import __version__


class ConsoleMessageProcessor:
    """Print SSDP messages to stdout."""

    def request_received(self, request: messages.SSDPRequest, addr: tuple):
        self.pprint(request, addr)

    def response_received(self, response: messages.SSDPResponse, addr: tuple):
        self.pprint(response, addr)

    @staticmethod
    def pprint(msg, addr):
        """Pretty print the message."""
        host = f"[{addr[0]}]" if ":" in addr[0] else addr[0]
        host = click.style(host, fg="green", bold=True)
        port = click.style(str(addr[1]), fg="yellow", bold=True)
        pretty_msg = highlight(str(msg), SSDPLexer(), formatters.TerminalFormatter())
        click.echo("%s:%s - - [%s] %s" % (host, port, time.asctime(), pretty_msg))


class PrintSSDMessageProtocol(ConsoleMessageProcessor, SSDP):
    pass


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

@cli.command()
@click.option(
    "--bind",
    "-b",
    help="Specify alternate bind address [default: all interfaces]",
)
@click.option(
    "--search-target",
    "--st",
    default="ssdp:all",
    help="Search target [default: ssdp:all]",
)
@click.option(
    "--max-wait",
    "--mx",
    default=5,
    help="Maximum wait time in seconds [default: 5]",
)
def discover(bind, search_target, max_wait):
    """Send out an M-SEARCH request and listening for responses."""
    family, addr = network.get_best_family(bind, network.PORT)
    loop = asyncio.get_event_loop()

    connect = loop.create_datagram_endpoint(PrintSSDMessageProtocol, family=family, local_addr=(bind, 6666))
    transport, protocol = loop.run_until_complete(connect)

    target = network.MULTICAST_ADDRESS_IPV4, network.PORT

    search_request = messages.SSDPRequest(
        "M-SEARCH",
        headers={
            "HOST": "%s:%d" % target,
            "MAN": '"ssdp:discover"',
            "MX": str(max_wait),  # seconds to delay response [1..5]
            "ST": search_target,
        },
    )

    target = network.MULTICAST_ADDRESS_IPV4, network.PORT

    search_request.sendto(transport, target)

    PrintSSDMessageProtocol.pprint(search_request, addr[:2])
    try:
        loop.run_until_complete(asyncio.sleep(4))
    finally:
        transport.close()
