import os

def convert(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    with open(file_path, 'w', encoding='utf-8-sig') as f:
        f.write(content)

csv_files = [
    'CARD_SUBWAY_MONTH_2020.csv'
    #'LHK_bus.csv',
    #'SHS_population.csv',
    #'SHS_weather.csv'
]

for file in csv_files:
    if os.path.exists(file):
        convert(file)
        print(f"{file} success")
    else:
        print(f"{file} fail")