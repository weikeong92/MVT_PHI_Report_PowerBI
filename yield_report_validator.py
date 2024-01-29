import os
import shutil
import gzip
import csv
from datetime import datetime, timedelta

def replace_header(csv_file):
    header = [
        "ODM", "Prodname", "Year", "Workweek", "Station", "Input", "1A fail", "2A fail",
        "Test result", "Indicator", "Pareto", "Qty", "1A PASS", "Yield", "Alpha",
        "Si fail QTY", "NDF QTY", "Si fail dpm", "NDF dpm", "Remarks", "Yield GOAL",
        "Alpha Goal", "notes", "Test Time", "Test time1"
    ]

    header = [col.strip() for col in header]

    with open(csv_file, 'r', newline='') as file:
        rows = list(csv.reader(file))
        rows[0] = header

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def process_folder(folder_path):
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.csv'):
                csv_file = os.path.join(foldername, filename)
                replace_header(csv_file)
                print(f"Header replaced in {csv_file}")

def find_and_copy_recent_gz(src_dir, dest_dir):
    if not os.path.exists(src_dir):
        print(f"Source directory '{src_dir}' does not exist.")
        return

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    max_age_seconds = 7 * 24 * 60 * 60

    current_time = datetime.now()

    for foldername, subfolders, filenames in os.walk(src_dir):
        for filename in filenames:
            if filename.endswith('.gz'):
                src_path = os.path.join(foldername, filename)

                file_modification_time = os.path.getmtime(src_path)
                file_age_seconds = current_time.timestamp() - file_modification_time

                if file_age_seconds <= max_age_seconds:

                    dest_path = os.path.join(dest_dir, filename)

                    shutil.copy2(src_path, dest_path)
                    print(f"Copied '{filename}' to '{dest_dir}'.")

                    with gzip.open(dest_path, 'rb') as f_in:
                        with open(dest_path[:-3], 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                            print(f"Extracted contents from '{filename}'.")

                    os.remove(dest_path)

                    # Get the path to the extracted CSV file
                    csv_file_path = dest_path[:-3]

                    # Replace the header in the CSV file
                    replace_header(csv_file_path)
                    print(f"Header replaced in '{csv_file_path}'.")

                    # Move the file to the destination directory
                    destination_path = os.path.join(destination_directory, os.path.basename(csv_file_path))
                    shutil.move(csv_file_path, destination_path)
                    print(f"Moved '{os.path.basename(csv_file_path)}' to '{destination_directory}'.")

if __name__ == "__main__":
    source_directories = [
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//CB//MVT-YieldSummary",
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//CX//MVT-YieldSummary",
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//FS//MVT-YieldSummary",
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//PL//MVT-YieldSummary",
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//RL//MVT-YieldSummary",
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//WZ/MVT-YieldSummary"
    ]

    destination_directory = "//PGGAPP3001//ToWeiKeong//data"

    for source_directory in source_directories:
        find_and_copy_recent_gz(source_directory, destination_directory)