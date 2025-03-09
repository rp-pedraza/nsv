#!/usr/bin/env python3

# Usage: [python] ./process-data.py [source_data_dir [output_data_dir]]
#
# Default source_dir is '../data'.  Default output_dir is '(source_dir).processed'.

from datetime import datetime
from pathlib import Path
import glob
import json
import os
import sys

def die(message, *extra_args):
    print(message, *extra_args, file=sys.stderr)
    sys.exit(1)

default_data_dir = os.path.join(Path(__file__).parent, '..', 'data')
source_dir = sys.argv[1] if len(sys.argv) > 1 else default_data_dir
output_dir = sys.argv[2] if len(sys.argv) > 2 else source_dir + '.processed'

if not os.path.isdir(source_dir):
	die(f"Data directory '{source_dir}' doesn't exist.")

os.makedirs(output_dir, exist_ok=True)

files = glob.glob(os.path.join(source_dir, '*.json'))

if len(files) == 0:
	die("No data file found in '{source_dir}'")

for file_path in files:
    print(f"Processing {file_path}.")

    with open(file_path, 'r') as f:
        hash_data = json.load(f)

    # Add identity based on the data file's name so we can have something
    # to use for uniquely identifying the entries.
    hash_data['identity'] = os.path.basename(file_path).split('_')[0]

    # Convert 'datetime' values to floating-point.
    dt = datetime.strptime(hash_data['datetime'], '%Y-%m-%d %H:%M:%S.%f')
    hash_data['datetime'] = float(dt.strftime('%s.%f'))

    new_json_str = json.dumps(hash_data, separators=(',', ':'))
    new_file_path = os.path.join(output_dir, os.path.basename(file_path))

    print(f"Saving data to {new_file_path}.")
    with open(new_file_path, 'w') as f:
        f.write(new_json_str)

print("Done.")
