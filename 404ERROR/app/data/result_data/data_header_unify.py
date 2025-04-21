import csv

def change_headers(file_path, changes, output_file=None):
    if output_file is None:
        output_file = file_path  

    
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)

    headers = rows[0]
    new_headers = [changes.get(col, col) for col in headers]
  
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(new_headers)
        writer.writerows(rows[1:])

    print(f"{file_path} -> {output_file} test")

change_headers(
    'SHS_population.csv',
    {'자치구명': '자치구'}
)

change_headers(
    'LHK_bus.csv',
    {'사용일자': '일시', '행정구': '자치구'}
)
