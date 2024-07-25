import argparse
import os
from . import data


def init(args):
    data.init()
    print(f"Initilalized an empty mygit repository in {os.getcwd()}/{data.GIT_DIR}")


def parse_args():
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest="command")
    commands.required = True

    init_parser = commands.add_parser("init")
    init_parser.set_defaults(func=init)

    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)
