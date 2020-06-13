#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import time


# In[2]:

#Dictionary to store all scrape data
mars_scrape_data = {}

def init_browser():

    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


    # # NASA Mars News Articles

    # In[3]:
def scrape():
    browser = init_browser()

    #Collect News urls
    news_url="https://mars.nasa.gov/news/"

    browser.visit(news_url)
    time.sleep(1)


    # In[4]:


    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')


    # In[5]:


    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_='bottom_gradient').find('div').find('h3').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Save scrapped data 
    mars_scrape_data['news_title'] = news_title
    mars_scrape_data['news_p'] = news_p


    # ### JPL Mars Space Images - Featured Image

    # In[6]:


    #Collect pic urls
    pic_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(pic_url)
    time.sleep(2)


    # In[7]:


    # HTML Object 
    image = browser.html

    # Parse HTML with Beautiful Soup
    soup_img = bs(image, 'html.parser')

    # Retrieve background-image url from style tag 
    featured_image_url  = soup_img.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Concatenate website url with scrapped route
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url

    # Save full link to featured image

    mars_scrape_data['featured_image_url'] = featured_image_url


    # # Mars Weather

    # In[17]:


    #Collect twitter url
    twitter = "https://twitter.com/marswxreport?lang=en"

    browser.visit(twitter)
    time.sleep(2)


    # In[56]:


    # HTML Object 
    weather = browser.html

    # Parse HTML with Beautiful Soup
    soup_weather = bs(weather, 'html.parser')

    # Retrieve mars weather 
    weather_tweet  = soup_weather.find_all('div', class_='css-1dbjc4n')
    #'css-1dbjc4n r-18u37iz r-thb0q2')

    # Look for entries that display weather related words to exclude non weather related tweets 
    for tweet in weather_tweet: 
        node1 = tweet.find('div')
        if node1 is not None:
            node2 = node1.find('span')
            if node2 is not None:
                mars_weather = node2.text
                if 'sol' and 'pressure' in mars_weather:
                    #Print Mars Weather
                    print(mars_weather)
                    break
                else: 
                    continue

    # Save MARS weather
    mars_scrape_data['mars_weather'] = mars_weather
    # # Mars Facts

    # In[40]:


    #Collect MARS facts url
    facts = "https://space-facts.com/mars/"

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts)

    #Save facts to df
    mars_facts_df=mars_facts[0]

    mars_facts_df.columns = ['Description', 'Value']

    #Replace colons
    mars_facts_df['Description']=mars_facts_df['Description'].replace(':','', regex=True)

    # Save html code 
    mars_facts_html=mars_facts_df.to_html(classes='table table-striped',header=['Description','Value'],index=False,border='', justify='unset')

    #Save MARS fact html string

    mars_scrape_data['mars_facts_html'] = mars_facts_html

    # ### Mars Hemispheres

    # In[11]:


    # Visit hemispheres website
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    time.sleep(3)


    # In[12]:
    
    # Create empty list for hemisphere urls 
    hemispheres_main_urls = []

    # HTML Object
    hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    hem_soup = bs(hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    images = hem_soup.find_all('div', class_='item')

    
    # Loop through the items previously stored
    for i in images: 
        # Store title
        title = i.find('h3').text

        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']

        # Visit the link that contains the full image website 
        browser.visit('https://astrogeology.usgs.gov' + partial_img_url)
        time.sleep(1)

        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html

        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup_1 = bs( partial_img_html, 'html.parser')

        # Retrieve full image source 
        img_url = 'https://astrogeology.usgs.gov' + soup_1.find('img', class_='wide-image')['src']

        # Append the retreived information into a list of dictionaries 
        hemispheres_main_urls.append({"title" : title, "img_url" : img_url})


    # Save hemisphere_image_urls

    mars_scrape_data['mars_hemispheres'] = hemispheres_main_urls

    browser.quit()
    return mars_scrape_data