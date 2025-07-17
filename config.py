#!/usr/bin/env python
import json

# Config class to handle all config options such as api_keys etc...


class CONFIG:
    def __init__(self):
        try:
            with open("config.json", "r") as c:
                config = json.load(c)
                self.unms_url = config.get("unms_url", "unms.example.com")
                self.unms_api_key = config.get("unms_api_key", "example_key")
                self.spreadsheet_id = config.get("spreadsheet_id", "sample_id")
                self.range = config.get("range", "sample_range")
                self.page = self.range.split("!")[0]
                self.range_to_clear = config.get(
                    "range_to_clear", "sample_range")
                self.discord_webhook = config.get("discord_webhook", "https://example.com")
        except FileNotFoundError:
            print("config file not found exiting NOW")
            exit(1)

    def __str__(self):
        return f"url = {self.unms_url},\napi_key = {self.unms_api_key},\npage = {self.page}"


# test function to print config
def main():
    config = CONFIG()
    print(config)


if __name__ == "__main__":
    main()
