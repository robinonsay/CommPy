from commpy import gui, cli
import argparse

parser = argparse.ArgumentParser('CommPy', description="CommPy: Wireless Communication Simulation Python Library")
parser.add_argument('--cli', help='Use Command Line Interface', action='store_true')
args = parser.parse_args()

try:
    if args.cli:
        cli.main()
    else:
        gui.main()
except KeyboardInterrupt:
    pass
