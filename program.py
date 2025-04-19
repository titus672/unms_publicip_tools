#!/usr/bin/env python

from googleapiclient.errors import HttpError
from connectors import nms_connector
from unms_devices import Device
from sheets import Sheet, find_value_in_sheet
from misc_tools import Debug
import time
import os
import argparse


def main():
    # change cwd so relative paths work
    cwd = os.path.dirname(__file__)
    os.chdir(cwd)
    print(os.getcwd())
    # Parse arguments
    parser = argparse.ArgumentParser(
        prog="IP Updater",
        description="Updates a spreadsheet with public ip's"
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-c", "--clear", action="store_true")
    args = parser.parse_args()
    # initialize debug
    debug = Debug(args)
    # get UISP Devices
    devices = []
    d = nms_connector("devices?withInterfaces=True&authorized=True")
    for device in d:
        devices.append(Device(device))
    # Initialize sheet
    sheet = Sheet()
    values = sheet.get_range(sheet.range)
    if args.clear:
        debug.debug(sheet.config.range_to_clear)
        sheet.clear_ranges()

    # list of tuples with the index, ip_address and device name
    indexes = []
    for d in devices:
        for address in d.addresses:
            index = find_value_in_sheet(values, address)
            if index:
                indexes.append((index, address, d.name))
    for index in indexes:
        range = f"{sheet.page}!{index[0]}"
        address = index[1]
        name = index[2]
        try:
            sheet.update_range(range, name)
            debug.debug(f"{range}, {address}, {name}")
            time.sleep(1)
            debug.debug("sleeping 1s")
        except HttpError as e:
            print("Too many requests, waiting for 60s")
            wait_time = 60
            while True:
                if wait_time >= 1:
                    time.sleep(1)
                    wait_time -= 1
                else:
                    sheet.update_range(range, name)
                    debug.debug(f"{range}, {address}, {name}")
                    debug.debug("sleeping 1s")


if __name__ == "__main__":
    main()
