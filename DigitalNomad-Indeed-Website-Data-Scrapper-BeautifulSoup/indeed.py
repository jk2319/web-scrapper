import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = "https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def get_last_page():
  #get html_doc
  result = requests.get(URL)

  #create a soup, extract the data from the HTML
  soup = BeautifulSoup(result.text, "html.parser")

  #look for div class named 'pagination'
  pagination = soup.find("div", {"class":"pagination"})

  #find the anchors
  links = pagination.find_all('a')
  pages = []
  for link in links[:-1]:
      #extract the string in relation to span, .find('span') can be inc middle
      pages.append(int(link.string))
  max_page=pages[-1]
  return max_page

def extract_job(html):
  title = (html.find("h2",{"class":"title"})).find("a")["title"]
  #get variable "title" inside the anchor which contains the job titles
  #anchor = title.find("a")["title"]
  #able to combine above commands as well
  company = html.find("span", {"class":"company"})
  company_anchor = company.find("a")
  if company_anchor is not None:
    company = str(company_anchor.string)
  else:
    company = str(company.string)
  company = company.strip()
  location = html.find("div", {"class":"recJobLoc"})["data-rc-loc"]
  job_id = html["data-jk"]
  return {
      'title':title,
      'company': company, 
      'location': location,
      'link': f"https://www.indeed.com/viewjob?jk={job_id}"
  }

def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page}")
    #result is the html
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    #'find_all' gives everything you find and 'find' just gives the first one
    results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs