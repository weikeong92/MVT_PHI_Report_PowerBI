import os
import csv

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

        for row in rows[1:]:
            for col_idx in [13, 16, 17]:
                if row[col_idx] == '#DIV/0!':
                    row[col_idx] = '0'

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
            if row[qty_idx].strip() == '-' or row[qty_idx].strip() == "#VALUE!":
                row[qty_idx] = '0'

            yield_idx = header.index('Yield')
            if row[yield_idx].strip() == "#VALUE!" or row[yield_idx].strip() == "#DIV/0!":
                row[yield_idx] = '0%'

            alpha_idx = header.index('Alpha')
            if row[alpha_idx].strip() == "#DIV/0!":
                row[alpha_idx] = '0%'

            ndfdpm_idx = header.index('NDF dpm')
            if row[ndfdpm_idx].strip() == "#DIV/0!":
                row[ndfdpm_idx] = '0'
            
            test_time_idx = header.index('Test Time')
            row[test_time_idx] = row[test_time_idx].replace('S', '')

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

def main():
    #folder_path = "C:\\Users\\tanweike\\OneDrive - Intel Corporation\\Desktop\\Dev\\MVT_PHI_Report_PowerBI\\validator"
    folder_path = "O:\\yield_report\\2023\\Syrma\\csv"

    process_folder(folder_path)

    # for filename in os.listdir(folder_path):
    #     if filename.endswith('.csv'):
    #         csv_file = os.path.join(folder_path, filename)
    #         replace_header(csv_file)
    #         print(f"Header replaced in {filename}")

if __name__ == "__main__":
    main()