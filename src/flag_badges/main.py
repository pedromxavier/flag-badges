import argparse
from pathlib import Path

from .list import list_cmd
from .generate import generate_cmd

def main():
    parser = argparse.ArgumentParser()
    
    subparsers = parser.add_subparsers(dest='command')

    list_parser = subparsers.add_parser("list", help="Lists available countries and their codes")
    list_parser.set_defaults(callback=list_cmd)

    generate_parser = subparsers.add_parser("generate", help="Generates badges and a README file")
    generate_parser.add_argument("path", type=Path, help="Root directory")
    generate_parser.set_defaults(callback=generate_cmd)

    args = parser.parse_args()
    args.callback(args)

    return None