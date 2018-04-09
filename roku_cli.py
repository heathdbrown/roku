import roku.ecp
import argparse

# Simple Arguments pulling ip Addresses or File
parser = argparse.ArgumentParser(description="Interact with Roku")
parser.add_argument('roku_ip', help='Roku IP address')
parser.add_argument('--channels', action='store_true', help='List channels on Roku')
args = parser.parse_args()

if args.channels:
    roku_channels = roku.ecp.ECP(args.roku_ip)
    print('{}'.format(roku_channels.query_apps()))
    roku_apps = dict(roku_channels.query_apps())
    print(type(roku_apps))
