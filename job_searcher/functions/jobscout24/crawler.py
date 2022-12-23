import requests
from bs4 import BeautifulSoup
from langdetect import detect


def find_job_urls_per_page(search_term_url, main_url):
        jobs_data = []
    
        reqs = requests.get(search_term_url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        soup_articles = soup.find_all("li", {"class": "job-list-item"})
        page = search_term_url.split('=')[-1]
        
        for soup_article in soup_articles:

            job_dic = {}
            index_id = str(soup_article).index('data-job-id')
            data_id = str(soup_article)[index_id + len('data-job-id='):].split('"')[1]
            job_url = f'{main_url}?jobId={data_id}'
            job_dic['joblisting_url'] = job_url
            job_dic['page'] = page
            job_dic['joblisting_id'] = data_id
            job_dic['job_site'] = "Jobscout24"
            jobs_data.append(job_dic)
    
        return jobs_data

def find_job_urls_on_first_x_pages(number_of_pages, search_term_url, main_url):    
    
    all_jobs_data = []
    for page in range(number_of_pages):
        next_page_url = f'{search_term_url}?p={page+1}'
        all_jobs_data += find_job_urls_per_page(next_page_url, main_url)
        
    return all_jobs_data

def find_jobsites(number_of_pages, search_term):
    main_url = 'https://www.jobscout24.ch/de/jobs/'
    list_jobs_data = []

    search_term_reworked = search_term.replace(' ', '%20').lower()
    search_term_url = f'{main_url}/{search_term_reworked}/'
    jobs_data = find_job_urls_on_first_x_pages(number_of_pages, search_term_url, main_url)

    for job_data in jobs_data:
        job_data['search_term'] = search_term
    
        list_jobs_data.append(job_data)

    return list_jobs_data

class Crawler:

    def __init__(self, job_url):

        self.job_url = job_url
        self.main_url = 'https://www.jobscout24.ch/de/jobs/'
        self.job_description, self.job_title, self.company_title, self.job_location, self.job_description_soup, self.language  = self.crawl_url()

    def crawl_url(self):

        reqs = requests.get(self.job_url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        job_description_soup = soup.find('div', {'class': 'job-description'})
        job_title_soup = soup.find('div', {'class': 'title-left-part'})
        company_title_soup = soup.find('h2', {'class': 'company-title'})
        job_location_soup = soup.find(['a', 'span'], {'class': 'company-location'})        
            
        try:
            job_description = job_description_soup.get_text().lower()
        except:
            job_description = None
            
        try:
            language = detect(job_description)
        except:
            language = None

        try:
            job_title = job_title_soup.get_text()
        except:
            job_title = None
            
        try:
            company_title = company_title_soup.get_text()
        except:
            company_title = None 
            
        try:
            job_location = job_location_soup.get_text()
        except:
            job_location = None
            
        
        return job_description, job_title, company_title, job_location, str(job_description_soup), language
