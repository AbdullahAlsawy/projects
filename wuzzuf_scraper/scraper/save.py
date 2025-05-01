## ملف: scraper/save.py
import csv
from itertools import zip_longest

def save_to_csv(data, filename='wuzzuf_jobs.csv'):
    headers = ['job_title', 'company_name', 'location', 'skills']

    # zip_longest إذا كانت البيانات عبارة عن أعمدة منفصلة
    if isinstance(data[0], str):
        data = zip_longest(*data)

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)