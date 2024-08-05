#!/usr/bin/env python
from connectors import nms_connector, test_nms_connector
from misc_tools import pprint

class Device:
    def __init__(self, device):
        self.data = device
        self.name = device["identification"].get("name", "no name set")
        self.addresses = []
        for interface in device["interfaces"]:
            for a in interface["addresses"]:
                if a["version"] == "v4" and a["cidr"].split("/")[0] not in self.addresses:
                    self.addresses.append(a["cidr"].split("/")[0])
        

def main():
    devices = []
    d = test_nms_connector()
    #d = nms_connector("devices?withInterfaces=True&authorized=True")
    for device in d:
        devices.append(Device(device))
    for d in devices:
        print(d.addresses)
        pprint(d.name)
    
    


if __name__ == "__main__":
    main()
