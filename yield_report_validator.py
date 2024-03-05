import os
import shutil
import gzip
import csv
import re
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime, timedelta, date

today = date.today()
iso_week = today.isocalendar()[1]
work_week = iso_week - 1 if today.isoweekday == 7 else iso_week
date_today = datetime.today()
formatted_timedate = date_today.strftime("%m/%d/%Y %H:%M:%S")

expected_odm = {'Azurewave', 'Gemtek', 'Gemtektw', 'GemtekVN', 'Syrma', 'BrazilFlex'}
encountered_odm = set()
missing_odms_acc = set()

def replace_header(csv_file):
    try:
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

            for row_idx, row in enumerate(rows[1:], start=1):
                try:
                    for col_idx in [13, 16, 17]:
                        if row[col_idx] == '#DIV/0!':
                            row[col_idx] = '0'
                except IndexError:
                    #print(f"Error: Index out of range in row column {col_idx}")
                    continue
                
                try:
                    for col in [0, 5, 10, 11, 13, 14, 18, 23]:
                        odm_idx = header.index('ODM')
                        if row[odm_idx].strip() == "GemTek":
                            row[odm_idx] = "Gemtek"

                        input_idx = header.index('Input')
                        if row[input_idx].strip() == '-' or row[input_idx].strip() == "NO PRF":
                            row[input_idx] = '0'

                        pareto_idx = header.index('Pareto')
                        if row[pareto_idx].strip() == '0':
                            row[pareto_idx] = 'NA'

                        qty_idx = header.index('Qty')
                        if row[qty_idx].strip().startswith('-') or row[qty_idx].strip() == "#VALUE!":
                            row[qty_idx] = '0'

                        yield_idx = header.index('Yield')
                        if row[yield_idx].strip() == "#VALUE!" or row[yield_idx].strip() == "#DIV/0!":
                            row[yield_idx] = '0.00%'
                        elif row[yield_idx].strip().startswith('-'):
                            row[yield_idx] = '0.00%'

                        alpha_idx = header.index('Alpha')
                        if row[alpha_idx].strip() == "#DIV/0!":
                            row[alpha_idx] = '0.00%'

                        ndfdpm_idx = header.index('NDF dpm')
                        if row[ndfdpm_idx].strip() == "#DIV/0!":
                            row[ndfdpm_idx] = '0'
                    
                        test_time_idx = header.index('Test Time')
                        row[test_time_idx] = row[test_time_idx].replace('S', '')

                except ValueError:
                    print(f"Error: {col} column not found in row {row_idx}")

        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
            
    except Exception as e:
        print(f"Error processing {csv_file}: {e}")

# def process_folder(folder_path):
#     for foldername, subfolders, filenames in os.walk(folder_path):
#         for filename in filenames:
#             if filename.endswith('.csv'):
#                 csv_file = os.path.join(foldername, filename)
#                 replace_header(csv_file)
                
def send_email(odm, ww):
    sender_email = "wei.keong.tan@intel.com"
    #receiver_email = "wei.keong.tan@intel.com, kent.yen.keong@intel.com, guanx.yi.lim@intel.com"
    receiver_email = "wei.keong.tan@intel.com"
    pwd = "Elon@369"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Test Alert! No New Yield Report Receive from ODM This Week\n Please check with ODM to request them to upload the latest yield report!"

    body = f"Missing Yield Report from {odm} this work week {ww}"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtpauth.intel.com', 587)
    server.starttls()
    server.login(sender_email, pwd)
    server.sendmail(sender_email, [receiver_email], msg.as_string())
    server.quit()
    #print("successfully sent email to %s\n" % (msg['To']))

def upload_file_2sharepoint():
    ps_script_path = "C:\\ScheduleTask\\MVT_PHI_HVM_PBI\\upload_data.ps1"
    print("\nPowerShell Running...")
    result = subprocess.run(["pwsh.exe", "-File", ps_script_path], capture_output=True, text=True)
     
    print("PowerShell Output: \n", result.stdout)
     
    if result.returncode != 0:
        print(f"{formatted_timedate}, PowerShell script failed with return code:  '{result.returncode}'\n")

def find_and_copy_recent_gz(src_dir, dest_dir):
    #data_log_file = "C:\\temp\\yield_report_data_log"
    data_log_file = r"C:\\ScheduleTask\\MVT_PHI_HVM_PBI\\_log_\\yield_report_log.txt"
    
    if not os.path.exists(src_dir):
        print(f"Source directory '{src_dir}' does not exist.")
        return

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    max_age_seconds = 2 * 24 * 60 * 60

    current_time = datetime.now()

    for foldername, subfolders, filenames in os.walk(src_dir):
        for filename in filenames:
            if filename.endswith('.gz'):
                src_path = os.path.join(foldername, filename)

                file_modification_time = os.path.getmtime(src_path)
                file_age_seconds = current_time.timestamp() - file_modification_time

                if file_age_seconds <= max_age_seconds:

                    filename_yp = os.path.splitext(os.path.splitext(filename)[0])[0]
                    parts = filename_yp.split('_')
                    odm = parts[0]

                    encountered_odm.add(odm)

                    for part in parts:
                        if re.match(r'ww\d{2}', part):
                            ww = part[2:]
                            if ww[0] == '0':
                                ww = ww[1:]
                            #if (str(ww) == str(work_week-1) or str(ww) == str(work_week-2)):
                                # how to modify the code to check and ensure if odm only get certain expected_odm, it will send email?
                                # send_email(odm, ww)

                    with open(data_log_file, 'r') as file:
                        for line in file:
                            if filename_yp in line:
                                break
                        else:
                            dest_path = os.path.join(dest_dir, filename)

                            shutil.copy2(src_path, dest_path)
                            print(f"\nCopied '{filename}' to '{dest_dir}'.")

                            with gzip.open(dest_path, 'rb') as f_in:
                                with open(dest_path[:-3], 'wb') as f_out:
                                    shutil.copyfileobj(f_in, f_out)
                                    print(f"Extracted contents from '{filename}'.")

                            os.remove(dest_path)

                            csv_file_path = dest_path[:-3]

                            replace_header(csv_file_path)
                            print(f"Header replaced in {csv_file_path}")

                            #Move the file to the destination directory
                            destination_path = os.path.join(destination_directory, os.path.basename(csv_file_path))
                            shutil.move(csv_file_path, destination_path)
                            print(f"Moved '{os.path.basename(csv_file_path)}' to '{destination_directory}'.")

                            yield_report_file = os.path.basename(os.path.splitext(csv_file_path)[0])
                            with open(data_log_file, 'a') as file:
                                file.write(yield_report_file+"\n")

if __name__ == "__main__":
    source_directories = [
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//CB//MVT-YieldSummary",
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//CX//MVT-YieldSummary",
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//FS//MVT-YieldSummary",
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//PL//MVT-YieldSummary",
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//RL//MVT-YieldSummary",
        "//EBS-PG-MVT3.cps.intel.com//it_mvtarchive//prod//ebsarchive//WZ/MVT-YieldSummary"
    ]

    destination_directory = r"C:\\ScheduleTask\\MVT_PHI_HVM_PBI\\data"

    for source_directory in source_directories:
        find_and_copy_recent_gz(source_directory, destination_directory)
    
    missing_odms_acc = expected_odm - encountered_odm
    if missing_odms_acc:
        for missing_odm in missing_odms_acc:
            print(missing_odm)
    upload_file_2sharepoint()