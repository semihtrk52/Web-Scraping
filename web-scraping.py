from bs4 import BeautifulSoup
import requests

job_url = 'https://www.kariyer.net/is-ilanlari/stajyer?lpst=8'
html_text = requests.get(job_url).text
soup = BeautifulSoup(html_text, 'lxml')

page_numbers = soup.find('div', class_='ad-pagination bg-white d-md-block d-none')
pagenumber_max = page_numbers.find('li', class_='page-item bv-d-xs-down-none tiny-padding')
button = pagenumber_max.find('button', class_='page-link')
max_page = int(button.get('aria-setsize'))

all_page_links = []

job_url = 'https://www.kariyer.net/is-ilanlari/stajyer?lpst=8'
html_text = requests.get(job_url).text
soup = BeautifulSoup(html_text, 'lxml')

all_links = soup.find_all('div', class_='list-items')
for link in all_links:
    link_address = link.find('a')['href']
    all_page_links.append(link_address)

for i in range(2, max_page + 1):
    job_url = f'https://www.kariyer.net/is-ilanlari/stajyer-{i}?lpst=8&cp={i}'
    html_text = requests.get(job_url).text
    soup = BeautifulSoup(html_text, 'lxml')
    all_links = soup.find_all('div', class_='list-items')
    for link in all_links:
        link_address = link.find('a')['href']
        all_page_links.append(link_address)

avr_links = []
asya_links = []
for link in all_page_links:
    new_link = "https://www.kariyer.net" + link
    html_text = requests.get(new_link).text
    soup = BeautifulSoup(html_text, 'lxml')
    location = soup.find('div', class_ = 'company-location')
    new_location = location.find('span').text.strip()
    if "İstanbul(Asya)" in new_location:
        asya_links.append(new_link)
    elif "İstanbul(Avr.)" in new_location:
        avr_links.append(new_link)
    

filtered_links = avr_links + asya_links
university_links = []
for link in filtered_links:
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    education_sections = soup.find_all('div', class_='aligment-container-section')
    
    for education in education_sections:
        h3_tags = education.find('h3').text
        
        if "Eğitim Seviyesi" in h3_tags:
            egitim_labels = education.find('span').text.strip()
            if not "Lise(Öğrenci)" in egitim_labels:
                university_links.append(link)

engineering_links = []
my_search_list = []

for link in university_links:
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    
    job_detail = soup.find('div', class_ = 'job-detail-qualifications').text
    search_words = ["bilgisayar mühendisliği", "yazılım mühendisliği", "python", "elektrik-elektronik", "c#", "sql", "javascript"] # değişmesi lazım
    for n in search_words:
        if link not in my_search_list:
            if n in job_detail.lower():
                my_search_list.append(link)
                print(link)
                