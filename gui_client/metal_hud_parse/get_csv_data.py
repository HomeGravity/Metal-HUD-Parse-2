import csv

def get_csv_data(file_name:str):
    if str(file_name).endswith(".csv"):
        with open(file_name, 'r', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        return data
    
    else:
        print("*.csv 파일이 아닙니다.")
        return None
