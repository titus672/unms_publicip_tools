#!/usr/bin/env python
import requests
from config import CONFIG


def discord_webhook(url, data):
    contents = {"content": str(data)}
    requests.post(url, json=contents)


def nms_connector(endpoint, action="get"):
    config = CONFIG()
    url = f"https://{config.unms_url}/nms/api/v2.1/{endpoint}"
    headers = {"x-auth-token": config.unms_api_key, "accept": "application/json"}
    request = requests.request(action, url, headers=headers)
    return request.json()


def test_nms_connector():
    import os
    import json
    if os.path.exists("device.json"):
        with open("device.json", "r") as device:
            print("reading data from file")
            return json.load(device)
    else:
        data = nms_connector("devices?withInterfaces=True&authorized=True")
        with open("device.json", "w") as f:
            json.dump(data, f, indent=4)
        print("writing data to file")
        return data


def main():
    # test connections
    import json
    try:
        devices = nms_connector("devices")
        print(json.dumps(devices, indent=4))
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
