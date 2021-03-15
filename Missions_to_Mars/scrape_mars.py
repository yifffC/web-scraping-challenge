from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    slides = soup.find_all('li', class_='slide')
    content_title = slides[0].find('div', class_ = 'content_title')
    latest_news_title = content_title.text.strip()
    
    article_teaser_body = slides[0].find('div', class_ = 'article_teaser_body')
    latest_news_paragraph = article_teaser_body.text.strip()

    # JPL Mars Space Images - Featured Image
    base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    url = base_url + 'index.html'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    relative_image_path = soup.find('img', class_='headerimage fade-in')["src"]
    featured_image_url = base_url + relative_image_path

    # Mars Facts
    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    mars_facts_df = tables[0]
    mars_facts_df.columns = ["Mars Property", "Value"]
    mars_facts_df.set_index("Mars Property", inplace=True)

    mars_facts_html = mars_facts_df.to_html().replace('\n', '')

    # Mars Hemispheres
    base_url = 'https://astrogeology.usgs.gov'
    url = base_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_items = soup.find_all('div', class_='item')
    image_page_urls = []
    title = []
    for item in image_items:
        image_page_urls.append(base_url + item.find('a')['href'])
        title.append(item.find('h3').text.strip())
    
    img_urls = []
    image_url = image_page_urls[0]
    for image_url in image_page_urls:
        browser.visit(image_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image_url = base_url + soup.find('img',class_='wide-image')['src']
        img_urls.append(image_url)
    
    hemisphere_image_urls = []

    for i in range(len(img_urls)):
        hemisphere_image_urls.append({'title':title[i],'img_url':img_urls[i]})
    
    # return one Python dictionary containing all of the scraped data
    marsdata = {}
    marsdata["latest_news_title"] = latest_news_title
    marsdata["latest_news_paragraph"] = latest_news_paragraph
    marsdata["featured_image_url"] = featured_image_url
    marsdata["mars_facts_html"] = mars_facts_html
    marsdata["hemisphere_image_urls"] = hemisphere_image_urls



    # Close the browser after scraping
    browser.quit()

    # Return results
    return marsdata
