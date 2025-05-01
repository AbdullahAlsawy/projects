## ملف: main.py
from scraper.fetch import get_page
from scraper.parse import extract_jobs
from scraper.save import save_to_csv

if __name__ == "__main__":
    html = get_page()
    jobs = extract_jobs(html)
    save_to_csv(jobs)