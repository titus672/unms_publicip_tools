#!/usr/bin/env python
from connectors import test_nms_connector
from misc_tools import pprint
from unms_devices import Device
import sys

def search_uisp_id(id):
    d = test_nms_connector()
    device_list = []
    for device in d:
        device_list.append(Device(device))
    for device in device_list:
        if device.data["identification"]["id"] == id:
            pprint(device.data["identification"]["site"])
def main():
    search_uisp_id(sys.argv[1])

if __name__ == "__main__":
    main()
