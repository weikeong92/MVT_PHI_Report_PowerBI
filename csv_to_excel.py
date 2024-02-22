import pandas as pd
import os

csv_folder = 'O:\\yield_report\\LatestData\\LatestData\\2024\\WW05\\data'
xlsx_folder = 'O:\\yield_report\\_excel_to_db_'

os.makedirs(xlsx_folder, exist_ok=True)

for file in os.listdir(csv_folder):
    if file.endswith('.csv'):
        df = pd.read_csv(os.path.join(csv_folder, file))
        output_filename = os.path.splitext(file)[0] + '.xlsx'
        df.to_excel(os.path.join(xlsx_folder, output_filename), index=False)