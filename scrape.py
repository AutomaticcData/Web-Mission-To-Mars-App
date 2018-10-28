
# coding: utf-8

# In[1]:


#import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

import time
#from datetime import datetime, timedelta

from bs4 import BeautifulSoup as bs

from splinter import Browser
#from splinter.exceptions import ElementDoesNotExist, ElementNotVisibleException
from flask import Flask, render_template, jsonify

def scrape_mars():

    # In[2]:



    #deal with ChromeDriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #had issues with chrome driver, added it to my environment variable pathing using %USERPROFILE%\AppData\Roaming\webdrivers
    #which fixed the issue

    #create a dictionary to hold values for our db list
    mars_data = {}


    # In[3]:

    #visit the url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    
    # In[4]:
    
    
    #create beautiful soup instance and parse using html (not xlml)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    
    # ### NASA Mars News
    # 
    # * Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    # 
    # ```python
    # # Example:
    # news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
    # 
    # news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."
    
    # In[5]:
    
    
    #declare our main variables to hold title and paragraph
    news_title = soup.find('div', 'content_title', 'a').text
    news_paragraph = soup.find('div', 'rollover_description_inner').text
    
    #========MONGODB==================================>>>>>>>>>>>>>>>>>>>>>>>>
    mars_data["mars_news_headline"] = news_title
    mars_data["mars_news_paragraph"] = news_paragraph
    #========MONGODB==================================>>>>>>>>>>>>>>>>>>>>>>>>
    
    #print(f"Title: {news_title}")
    #print(f"Paragraph: {news_paragraph}")
    
    
    # ### JPL Mars Space Images - Featured Image
    # 
    # * Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    # 
    # * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
    # 
    # * Make sure to find the image url to the full size `.jpg` image.
    # 
    # * Make sure to save a complete url string for this image.
    # 
    # ```python
    # # Example:
    # featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
    
    # In[6]:
    
    
    #visit the url
    #url = 'https://mars.nasa.gov/news/'
    featured_home_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    featured_image_url = "https://www.jpl.nasa.gov"
    browser.visit(featured_home_url)
    
    
    # In[7]:
    
    
    #create beautiful soup instance and parse using html (not xlml)
    fi_html = browser.html
    fi_soup = bs(fi_html, 'html.parser')
    
    
    # In[8]:
    
    
    fi_items = fi_soup.find("div",{"class":"carousel_items"}).find("article")
    #https://stackoverflow.com/questions/8825788/use-of-slice-command-with-split-command
    fi_image = fi_items['style'].split(':')[1].split('\'')[1]
    
    #https://stackoverflow.com/questions/1185524/how-do-i-trim-whitespace
    #fi_title = fi_items.find("h1",{"class":"media_feature_title"}).text.rstrip().lstrip()
    
    #print(fi_items['style'].split(':')[1].split('\'')[1])
    #print(fi_image)
    #print(fi_title)
    
    fi_image_link = featured_image_url + fi_image
    #print(fi_image_link)
    #========MONGODB==================================>>>>>>>>>>>>>>>>>>>>>>>>
    mars_data["mars_news_featured_image_src"] = fi_image_link
    #========MONGODB==================================>>>>>>>>>>>>>>>>>>>>>>>>
    
    
    # ### Mars Weather
    # 
    # * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
    # 
    # ```python
    # # Example:
    # mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
    
    # In[9]:
    
    
    #deal with ChromeDriver
    #executable_path = {'executable_path': 'chromedriver.exe'}
    #browser = Browser('chrome', **executable_path, headless=False)
    
    
    # In[10]:
    
    
    weather_home_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_home_url)
    
    
    # In[11]:
    
    
    weather_html = browser.html
    weather_soup = bs(weather_html, "html.parser")
    
    weather_mars = weather_soup.find("ol",{"id":"stream-items-id"}).find("li").find("p").text
    #print(weather_mars)
    #========MONGODB==================================>>>>>>>>>>>>>>>>>>>>>>>>
    mars_data["mars_news_weather"] = weather_mars
    #========MONGODB==================================>>>>>>>>>>>>>>>>>>>>>>>>
    
    # ### Mars Facts
    # 
    # * Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # 
    # * Use Pandas to convert the data to a HTML table string.
    
    # In[12]:
    
    
    # Mars Facts URL
    mars_url = "https://space-facts.com/mars/"
    browser.visit(mars_url)
    
    
    # In[13]:
    
    
    mars_html = browser.html
    mars_soup = bs(mars_html, "html.parser")
    
    
    # In[14]:
    
    
    #mars_info = mars_soup.find("div",{"id":"facts"}).find("li").find("strong").text
    #print(mars_info)
    
    
    # In[ ]:
    
    
    """
    SEARCH THROUGH THE TABLE
    """
    
    # In[15]:
    
    
    mars_table = mars_soup.find('table', class_='tablepress tablepress-id-mars')
    column_name = mars_table.find_all('td', class_='column-1')
    column_value = mars_table.find_all('td', class_='column-2')
    
    column_names = []
    column_values = []
    
    for row in column_name:
        column = row.text.strip()
        column_names.append(column)
        
    for row in column_value:
        value = row.text.strip()
        column_values.append(value)
        
    mars_facts_df = pd.DataFrame({
        "Column":column_names,
        "Value":column_values
        })
    
    mars_facts_df
    
    #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.pivot.html
    #mars_facts_df.pivot(index=None, columns='Column', values='Value')
    
    
    # In[16]:
    
    
    #mars_facts_df.describe()
    
    
    # In[17]:
    
    
    #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_html.html
    #http://wesmckinney.com/blog/formatting-dataframe-as-html/
    #https://stackoverflow.com/questions/32430009/python-pandas-data-frame-save-as-html-page
    
    mars_facts_html_table_string = mars_facts_df.to_html(header=False, index=False)
    #mars_facts_html_table_string
    #========MONGODB==================================>>>>>>>>>>>>>>>>>>>>>>>>
    mars_data["mars_news_facts_table"] = mars_facts_html_table_string
    #========MONGODB==================================>>>>>>>>>>>>>>>>>>>>>>>>
    
    
    # In[18]:
    
    
    #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_html.html
    #mars_table = pd.read_html(mars_url)
    #mars_table
    
    
    # ---
    # ## Mars Hemispheres
    # 
    # * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
    # 
    # * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # 
    # * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    # 
    # * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
    # 
    # ```python
    # # Example:
    # hemisphere_image_urls = [
    #     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #     {"title": "Cerberus Hemisphere", "img_url": "..."},
    #     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    # ]
    # ```
    # 
    # - - -
    
    # In[19]:
    
    
    hs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hs_url)
    
    
    # In[20]:
    
    
    hs_soup = bs(browser.html,"html.parser")
    hs_items = hs_soup.find("div",{"id":"product-section"}).find_all("div",{"class":"item"})
    #hemisphere_data = []
    
    
    # In[21]:
    
    
    #https://stackoverflow.com/questions/35616434/how-can-i-get-the-base-of-a-url-in-python
    #https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse
    hs_home_base_url = hs_url.rsplit('/', 2)[0]
    hs_home_base_url
    
    
    # In[22]:
    
    
    """
    <div class="item"><a class="itemLink product-item" href="/search/map/Mars/Viking/cerberus_enhanced"><img alt="Cerberus Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/dfaf3849e74bf973b59eb50dab52b583_cerberus_enhanced.tif_thumb.png"/></a><div class="description"><a class="itemLink product-item" href="/search/map/Mars/Viking/cerberus_enhanced"><h3>Cerberus Hemisphere Enhanced</h3></a><span class="subtitle" style="float:left">image/tiff 21 MB</span><span class="pubDate" style="float:right"></span><br/><p>Mosaic of the Cerberus hemisphere of Mars projected into point perspective, a view similar to that which one would see from a spacecraft. This mosaic is composed of 104 Viking Orbiter images acquired…</p></div> <!-- end description --></div>
    """
    
    
    # In[23]:
    
    
    #https://stackoverflow.com/questions/1424005/in-python-how-do-i-create-a-string-of-n-characters-in-one-line-of-code
    
    hs_list = []
    
    timecounter = 0
    for hsitem in hs_items:
        #print(hsitem)
        
        #get the base url and make a complete url
        hs_image_base_url = hsitem.find("a")["href"]
        hs_image_main_url = hs_home_base_url + hs_image_base_url
           
        print(f'Base URL: {hs_image_base_url}')
        print(f'Main URL: {hs_image_main_url}')
        
        #find the title of the image
        hs_image_title = hsitem.find("div",{"class":"description"}).find("a").find("h3").text
        
        print(f'Image Title: {hs_image_title}')
        
        #go to the image search page-----------------------------
        browser.visit(hs_image_main_url)
        
        hs_image_soup = bs(browser.html,"html.parser")
        hs_download_items = hs_image_soup.find("div",{"class":"downloads"})
        hs_full_image_url = hs_download_items.find("li").find("a")["href"]
        print(f'Full URL: {hs_full_image_url}')
        
        #add to dictionary
        hs_dict = {"title": hs_image_title, "img_url": hs_full_image_url}
        
        #append to list
        hs_list.append(hs_dict)
        
        #got a timeout error or high latency?
        #adding a sleep just account for the above
        time.sleep(2)
        print("**" * timecounter)
        
        timecounter +=1
        
    #========MONGODB==================================>>>>>>>>>>>>>>>>>>>>>>>>
        mars_data["mars_news_hemisphere_images"] = hs_list
    #========MONGODB==================================>>>>>>>>>>>>>>>>>>>>>>>>
    # In[24]:
    
    
    #print(hs_image_base_url)

    # In[25]:
    
    """ 
   TESTING
    hs_image_df = pd.DataFrame(hs_list)
    hs_image_df
    
    
    # In[26]:
    
    
    #reorganize for better readability
    hs_image_df = hs_image_df[['title','img_url']]
    hs_image_df
    
    mars_data = [{"Test":"This is a Test 0"}
                ,{"Test":"This is a Test 1"}
                ,{"Test":"This is a Test 2"}
                ,{"Test":"This is a Test 3"}]
        """
    
    browser.quit()
    
    
    #=====testing
    #return "mars_news_headline"
    return mars_data
    
    


