import csv
import openpyxl
import pathlib

def write_csv(horse_lst, owner_id, header, path):
    """
    Input: 
        horse_lst - list
        owner_id - integer
        header - list
        path - pathlib object
    """
    file_path = path.joinpath((str(owner_id) + '.csv'))

    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in horse_lst:
            for j in i['races']:
                writer.writerow([i['horse_name'],
                            i['horse_url'],
                            j['race_url'],
                            j['race_date'],
                            j['owner'],
                            j['prize'],
                            j['currency']])


def write_xlsx(horse_lst, owner_id, header, path):
    """
    Input: 
        horse_lst - list
        owner_id - integer
        header - list
        path - pathlib object
    """
    file_path = path.joinpath((str(owner_id) + '.xlsx'))

    workbook = openpyxl.Workbook()
    
    worksheet = workbook.active
    worksheet.title = 'Owner ID ' + str(owner_id)

    worksheet.append(item for item in header)
    for i in horse_lst:
        for j in i['races']:
            worksheet.append([i['horse_name'],
                            i['horse_url'],
                            j['race_url'],
                            j['race_date'],
                            j['owner'],
                            j['prize'],
                            j['currency']])
            
    workbook.save(filename=file_path)