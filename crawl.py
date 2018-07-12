import sys
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

site_url = 'http://animeheaven.eu/'

episode_list = []

# Each show URL in 'page-list' file is a show to be scraped
with open('page-list', 'r') as inputFile:
    for url in inputFile:
        # print(url)

        # Req web-page for the show
        uShowPage = uReq(url)
        page_html = uShowPage.read()
        uShowPage.close()

        # Soup the web-page
        page_soup = soup(page_html, 'html.parser')

        # Loop through each 
        containers = page_soup.findAll('a',{'class':'infovan'})
        for container in containers:
            episode_list.append("{}".format(site_url + container['href']))

episode_list.reverse()
download_count = 0

from selenium import webdriver
import time

force_xPath = '//*[@id="main"]/div[9]/div/a[2]/div[2]'

for ep_url in episode_list:
    # setup selenium webdriver
    driver = webdriver.Chrome('./webdrivers/chromedriver')
    driver.set_window_position(0, 0)
    driver.set_window_size(512, 512)
    # Open episode page
    driver.get(ep_url)
    # Locate download button and click it
    forceButtonElement = webdriver.support.ui.WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(force_xPath))
    forceButtonElement.click()
    download_count += 1

    # wait for download to complete before quitting
    download_wait = True
    while download_wait is True:
        time.sleep(5)
        download_wait = False
        li = os.listdir('/Users/james/Downloads')
        for x in li:
            if x.endswith('.crdownload'):
                download_wait = True
    # Quit because at this point Ads are everywhere
    driver.quit()
    # Only wait when there are more shows to download
    if download_count != len(episode_list):
        time.sleep(600)