import os
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def init_browser():
    driverpath = os.environ.get('GOOGLE_CHROME_BIN')
    driverpath2 = os.environ.get('GOOGLE_CHROME_SHIM')
    print(driverpath)
    print(driverpath2)

    # old path: '/app/.chromedriver/bin/chromedriver'
    executable_path = {'executable_path': '/app/.chromedriver/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars = {}

    # Retrieve Latest News Article
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(random.random()*1)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    listTextLabelElem = news_soup.find('div', class_='content_title')
    mars["news_title"] = listTextLabelElem.find('a').get_text()
    mars["news_paragraph"] = news_soup.find('div', class_='article_teaser_body').get_text()

    # Retrieve JPL Mars Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(random.random()*1)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    time.sleep(random.random()*2)
    full_image_elem.click()

    # Find the more info button and click that
    more_info_elem = browser.find_link_by_partial_text('more info')
    time.sleep(random.random()*3)
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    # find the relative image url
    img_url_rel = img_soup.find('figure', class_='lede').find('img')['src']

    # Set featured_image
    mars["featured_image"] = f'https://www.jpl.nasa.gov{img_url_rel}'

    # Retrieve Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(random.random()*1)

    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')

    # First, find a tweet with the data-name `Mars Weather`
    mars_weather_tweet = weather_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})

    # Set weather
    mars["weather"] = mars_weather_tweet.find('p', 'tweet-text').get_text()

    # Retrieve Mars Hemisphere Data
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(random.random()*1)

    # List for hemisphere image links
    hemisphere_image_urls = []

    # We have to find the elements on each loop to avoid a stale element exception
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    links = soup.find_all('a', class_='itemLink')

    for i in links[1::2]:
        hemisphere = {}
        browser.visit('https://astrogeology.usgs.gov'+i['href'])
        # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']

        # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text

        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)

        # Finally, we navigate backwards
        browser.back()
        time.sleep(random.random()*1)

    # Set hemispheres
    mars["hemispheres"] = hemisphere_image_urls

    df = pd.read_html('http://space-facts.com/mars/')[0]
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)

    table = df.to_html()
    table = table.replace('\n', '')

    mars['facts'] = table

    browser.quit()

    return mars
