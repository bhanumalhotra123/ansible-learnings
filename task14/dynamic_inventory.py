#!/usr/bin/env python            what env to run in

import json

# Define your dynamic inventory data
dynamic_inventory = {
    "db_server": {
        "ansible_host": "192.168.1.1",
    },
    "web_server": {
        "ansible_host": "192.168.1.2",
    }
}

if __name__ == "__main__":
    # Print the dynamic inventory in JSON format
    print(json.dumps(dynamic_inventory))
