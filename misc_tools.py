#!/usr/bin/env python
import json
import requests


def pprint(j):
    print(json.dumps(j, indent=4))


def index_to_column(index):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
    return alphabet[index]


class Debug:
    def __init__(self, args):
        self.verbose = args.verbose

    def debug(self, message):
        if self.verbose:
            print(message)


def message_discord(message):
    ...


def main():
    debug = Debug()
    debug.debug("verbose is enabled")


if __name__ == "__main__":
    main()
