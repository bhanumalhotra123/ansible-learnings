#!/usr/bin/env python

import json
import requests

# Replace with the actual URL of your CMDB API
cmdb_api_url = "https://your-cmdb-api-url.com/api/data"

# Define your CMDB API credentials or authentication tokens if required
api_credentials = {
    "username": "your_username",
    "password": "your_password"
}

# Make a request to the CMDB API
try:
    response = requests.get(cmdb_api_url, auth=(api_credentials["username"], api_credentials["password"]))

    # Check if the request was successful
    if response.status_code == 200:
        cmdb_data = response.json()

        # Process and format the CMDB data as needed
        dynamic_inventory = {}

        for item in cmdb_data:
            hostname = item.get("hostname")
            ip_address = item.get("ip_address")

            if hostname and ip_address:
                dynamic_inventory[hostname] = {
                    "ansible_host": ip_address
                }

        # Print the dynamic inventory in JSON format
        print(json.dumps(dynamic_inventory))

    else:
        print(f"Failed to fetch data from the CMDB API. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")
