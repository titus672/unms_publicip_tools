#!/usr/bin/env python
import json
import argparse
def pprint(j):
    print(json.dumps(j, indent=4))

def index_to_column(index):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
    return alphabet[index]

class Debug:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="IP Updater",
            description="Updates a spreadsheet with public ip's"
        )
        parser.add_argument("-v", "--verbose", action="store_true")
        self.args = parser.parse_args()
        self.verbose = self.args.verbose
    def debug(self, message):
        if self.verbose:
            print(message)
def main():
    debug = Debug()
    debug.debug("verbose is enabled")

if __name__ == "__main__":
    main()
    
