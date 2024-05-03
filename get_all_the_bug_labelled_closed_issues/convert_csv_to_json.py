import json
import csv
import sys

csv.field_size_limit(sys.maxsize)

def csv_to_json(csv_file_path, json_file_path):
    # Read CSV file and convert to a list of dictionaries
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)

    # Write JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)


csv_to_json('dataset/issue_dataset.csv', 'dataset/issue_dataset.json')
