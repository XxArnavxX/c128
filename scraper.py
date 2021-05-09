import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests

START_URL = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("./chromedriver")
browser.get(START_URL)
time.sleep(7)
headers = ["name", "light_yearsPfromPearth", "planet_mass", "stella_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius"]
planet_list = []
newplanetdata = []
def scrape():
    for i in range(439):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            empt = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    empt.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        empt.append(li_tag.contents[0])
                    except: 
                        empt.append("")
        hyperlink_li_tag = li_tags[0]
        empt.append("https://exoplanets.nasa.gov" + hyperlink_li_tag.find_all("a", href = True)[0]["href"])
        planet_list.append(empt)
    browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    
def scrapmoredata(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parcel")
        for tr_tag in soup.find_all("tr", attrs = {"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
            temp_list = []
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs{"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
        newplanetdata.append(temp_list)
    except:
        time.sleep(1)
        scrapmoredata()

scrape()
for index, data in enumerate(planet_list):
    scrapmoredata(data[5])

finalplanetdata = []

for index, data in enumerate(planet_list):
    newplanetdata_element = newplanetdata[index]
    newplanetdata_element = [elem.replace("\n", "") for elem in newplanetdata_element] 
    newplanetdata_element = newplanetdata_element[:7]
    finalplanetdata.append(data+newplanetdata_element)
with open('data.csv', "w") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(finalplanetdata)
