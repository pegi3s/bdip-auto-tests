import subprocess
import sys
import os
import shutil

# Ensure at least one argument is provided
if len(sys.argv) < 3:
    print("Usage: script.py <source_file> <config_file>")
    sys.exit(1)

# Get the file name from the first argument
file_name = sys.argv[1]
file_name_2 = sys.argv[2]

print("Copying the needed files", flush=True)

# Define file paths
source_file = os.path.join("/data", file_name)
destination_dir = "/opt"
destination_file = os.path.join(destination_dir, file_name)

# Copy the file
try:
    os.makedirs(destination_dir, exist_ok=True)
    shutil.copy(source_file, destination_file)
except FileNotFoundError:
    print(f"Source file {source_file} does not exist.")
    exit(1)
except PermissionError:
    print("Permission denied. Ensure you have the required privileges.")
    exit(1)
except Exception as e:
    print(f"An error occurred while copying the file: {e}")
    exit(1)

scripts = [
    ["get_json.py"],
    ["retrieve_test_data.py", file_name],
    ["run_docker.py", file_name, file_name_2]
]

# Run the scripts sequentially
for script in scripts:
    try:
        subprocess.run(["python3"] + script, check=True)
    except FileNotFoundError:
        print(f"Script {script[0]} not found. Ensure the file exists in the current directory.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error while executing {script[0]}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while running {script[0]}: {e}")
        sys.exit(1)
