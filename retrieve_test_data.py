import os
import json
import requests
import sys

# Define file paths
json_file = 'config.json'
tests_to_run_file = sys.argv[1]
output_folder = '/data/input_data'

# Create the folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Read the JSON file
try:
    with open(json_file, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {json_file} does not exist.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Could not parse JSON. {e}")
    exit(1)

# Read the tests_to_run.txt file
try:
    with open(tests_to_run_file, 'r') as file:
        tests_to_run = {line.strip() for line in file if line.strip()}
except FileNotFoundError:
    print(f"Error: The file {tests_to_run_file} does not exist.")
    exit(1)

# Process each unique entry listed in tests_to_run.txt
for test_name in tests_to_run:
    config = data.get(test_name)
    if not config:
        print(f"Warning: Test name {test_name} not found in JSON configuration.")
        continue

    input_files = config.get("input_files", [])
    for input_file in input_files:
        # Build the download link
        download_url = f"http://evolution6.i3s.up.pt/static/pegi3s/dockerfiles/input_test_data/{input_file}"
        output_path = os.path.join(output_folder, input_file)

        # Download the file
        if not os.path.exists(f"/data/input_data/{input_file}"):
            print(f"File {input_file} will be downloaded.", flush=True)
            try:
                response = requests.get(download_url)
                response.raise_for_status()  # Raise an exception for HTTP errors

                # Write the content to the file
                with open(output_path, 'wb') as output_file:
                    output_file.write(response.content)
            except requests.RequestException as e:
                print(f"Error downloading {input_file} for {test_name}: {e}")
        else:
            print(f"File {input_file} is already available.", flush=True)
