## ملف: scraper/parse.py
from bs4 import BeautifulSoup

def extract_jobs(html):
    soup = BeautifulSoup(html, 'lxml')

    job_titles = soup.find_all('h2', {'class': 'css-m604qf'})
    company_names = soup.find_all('a', {'class': 'css-17s97q8'})
    locations = soup.find_all('span', {'class': 'css-5wys0k'})
    skills = soup.find_all('div', {'class': 'css-y4udm8'})

    jobs = []
    for i in range(len(job_titles)):
        title = job_titles[i].text.strip()
        company = company_names[i].text.strip()
        location = locations[i].text.strip()
        skill = skills[i].text.strip()

        jobs.append([title, company, location, skill])

    return jobs