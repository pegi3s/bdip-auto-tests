import os
import json
import subprocess
import time
import sys
from datetime import datetime

# Function for checking if the Docker image exists in the host
def docker_image_exists(image_name):
    try:
        result = subprocess.run(f"docker images -q {image_name}", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError:
        return False

print(f"Running tests", flush=True)

# Define file paths
json_file = 'config.json'
tests_to_run_file = sys.argv[1]
config_file = '/data/' + sys.argv[2]

# Read the path information from the config file
try:
    with open(config_file, 'r') as file:
        for line in file:
            if line.strip().startswith("dir="):
                path_info = line.strip().split("=", 1)[1] 
                break
        else:
            raise ValueError("The config file does not contain a valid 'dir=' entry.")
except FileNotFoundError:
    print(f"Error: The file {config_file} does not exist.")
    exit(1)
except ValueError as e:
    print(f"Error: {e}")
    exit(1)

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

# Read the tests to run
try:
    with open(tests_to_run_file, 'r') as file:
        tests_to_run = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print(f"Error: The file {tests_to_run_file} does not exist.")
    exit(1)

# Process each unique entry
for test_name in tests_to_run:
    config = data.get(test_name)
    if not config:
        print(f"Warning: Test name {test_name} not found in JSON configuration.")
        continue

    # Extract configuration details
    docker_image = config.get("docker_image")
    commands = config.get("commands", "")
    output_dir = config.get("output_dir", "")
    output_file = config.get("output_file", "")
    
    # Check if the Docker image exists and if true remove it
    if docker_image_exists(docker_image):
        try:
            subprocess.run(f"docker rmi {docker_image}", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(f"Error removing Docker image {docker_image}: {e}")

    # Extract the image name without "pegi3s/" prefix
    image_name = docker_image.split('/')[-1]

    # Construct the output directory path
    output_dir_path = os.path.join("/data/output_folder", output_dir)

    # Ensure the output directory exists
    os.makedirs(output_dir_path, exist_ok=True)

    # Construct the full path to the output file
    output_file_path = os.path.join(output_dir_path, output_file)

    # Construct the Docker command
    if output_file:  # Check if output_file is not empty
        docker_command = f'docker run --rm -v {path_info}:/data {docker_image} {commands}'
    else:
        # Ensure DISPLAY is set
        if "DISPLAY" not in os.environ:
            os.environ["DISPLAY"] = ":0"
        docker_command = f'docker run --rm {commands}'
   
    # Get the current date in day/month/year format
    current_date = datetime.now().strftime("%d/%m/%Y")
    
    # Start measuring execution time
    start_time = time.time()  

    # Check if the output file exists and is not empty
    if output_file:
        try:
            subprocess.run(docker_command, shell=True, check=True)
            elapsed_time = time.time() - start_time
        except subprocess.CalledProcessError as e:
            print(f"Error executing Docker command for {test_name}: {e}")
            continue
        log_file_path = "/data/log"
        if not os.path.exists(output_file_path) or os.path.getsize(output_file_path) == 0:
            print(f"Execution of pegi3s/{image_name} failed.", flush=True)
            with open(log_file_path, "a") as log_file:
                log_file.write(f"Execution of pegi3s/{image_name} failed.\n")

        else:
            print(f"On the {current_date}, it took {elapsed_time:.2f} seconds to successfully execute pegi3s/{image_name}.", flush=True)
            with open(log_file_path, "a") as log_file:
                log_file.write(f"On the {current_date}, it took {elapsed_time:.2f} seconds to successfully execute pegi3s/{image_name}.\n")
    else:
        process = subprocess.run(docker_command, shell=True, capture_output=True, text=True)

        # Check the return code to determine if the Docker command was successful
        if process.returncode == 0:
            # Get the container ID for the running container
            container_id_process = subprocess.run(['docker', 'ps', '-q', '--filter', f'ancestor={docker_image}'], capture_output=True, text=True)
            container_id = container_id_process.stdout.strip()
            time.sleep(5)
            if container_id:
                # Stop the running container
                subprocess.run(['docker', 'stop', container_id], capture_output=True, text=True)
                elapsed_time = time.time() - start_time
                print(f"On the {current_date}, it took {elapsed_time:.2f} seconds to successfully execute pegi3s/{image_name}.", flush=True)
                with open("log", "a") as log_file:
                    log_file.write(f"On the {current_date}, it took {elapsed_time:.2f} seconds to successfully execute pegi3s/{image_name}.\n")
            else:
                print(f"Execution of pegi3s/{image_name} failed.", flush=True)
                with open("log", "a") as log_file:
                  log_file.write(f"Execution of pegi3s/{image_name} failed.\n")

        else:
            print(f"Execution of pegi3s/{image_name} failed.", flush=True)
            with open("log", "a") as log_file:
                  log_file.write(f"Execution of pegi3s/{image_name} failed.\n")
            print(process.stderr)

    # Remove again the tested Docker image
    try:
        subprocess.run(f"docker rmi {docker_image}", shell=True, check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Error removing Docker image {docker_image}: {e}")
