import requests
import json

# URL of the file to download
url = "https://raw.githubusercontent.com/pegi3s/dockerfiles/master/metadata/metadata.json"

# Download the file
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Error downloading the file: {e}")
    exit(1)

# Parse the downloaded JSON
try:
    data = response.json()
except json.JSONDecodeError as e:
    print(f"Error decoding the JSON: {e}")
    exit(1)

# Extract "auto_tests" and organize them by the "name" field
organized_auto_tests = {}

if isinstance(data, list):
    for item in data:
        if isinstance(item, dict) and "auto_tests" in item and item["auto_tests"]:
            name = item.get("name", "unknown")
            organized_auto_tests[name] = item["auto_tests"][0]
else:
    print("The JSON structure is not as expected (not a list at the root).")
    exit(1)

# Save the organized data to a new JSON file
output_file = "config.json"
try:
    with open(output_file, "w") as file:
        json.dump(organized_auto_tests, file, indent=4)
except IOError as e:
    print(f"Error saving the JSON file: {e}")
    exit(1)
