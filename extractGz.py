import os
import shutil
import gzip
from datetime import datetime, timedelta

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

if __name__ == "__main__":
    source_directories = [
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//CB//MVT-YieldSummary",
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//CX//MVT-YieldSummary",
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//FS//MVT-YieldSummary",
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//PL//MVT-YieldSummary",
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//RL//MVT-YieldSummary",
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//WZ/MVT-YieldSummary"
    ]

    #source_directory = "G:\\WZ\\MVT-YieldSummary\\2022"
    destination_directory = "//PGGAPP3001//ToWeiKeong//LatestData"

    for source_directory in source_directories:
        find_and_copy_recent_gz(source_directory, destination_directory)

    #find_and_copy_gz(source_directory, destination_directory)