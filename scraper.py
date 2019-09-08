#declare dependencies
from bs4 import BeautifulSoup as bs
from splinter.exceptions import ElementDoesNotExist
from splinter import Browser
import pandas as pd
import requests
import time
import requests as req


# Initialize browser
#executable path to driver
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# Defining scrape & dictionary



################################################h
#NASA Mars Website

def scrape():
    Final_Mars_Dictionary = {}
    
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    output = [news_title, news_p]

    Final_Mars_Dictionary["mars_news"] = output[0]
    Final_Mars_Dictionary["mars_paragraph"] = output[1]
## JPL Mars Space Images - Featured Image
# def mars_image():
    #Mars Image: Website Link Provided
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)

    #HTML object
    html = browser.html

    #Parse image with Beautiful Soup
    soup = bs(html, 'html.parser')

    #Retrieve background-image url from style tag 
    featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    #website url
    main_url = 'https://www.jpl.nasa.gov'

    #munge website & image url
    final_image = main_url + featured_image_url

    Final_Mars_Dictionary["mars_image"] = final_image

# # ## Mars Weather
# # # def mars_weather():
    weather_mars = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_mars)
    time.sleep(5)
    #HTML Object
    html_weather = browser.html

    #Parse with Beautiful Soup
    soup = bs(html_weather, 'html.parser')

    #find elements that contain tweets
    twitterverse = soup.find_all('div', class_ = 'js-tweet-text-container')

    #loop through the twitterverse for martian weather
    #find the key terms in weather tweets vs non-weather tweets
    for tweet in twitterverse:
        red_rock_weather = tweet.find('p').text
        if 'Sol' and 'pressure' in red_rock_weather:
            print(red_rock_weather)
            break
        else:
            pass

    Final_Mars_Dictionary["mars_weather"] = red_rock_weather

# # ## Mars Facts
# # def mars_facts():
    # Mars Facts URL
     
    facts = 'https://space-facts.com/mars/'
    browser.visit(facts)    
    time.sleep(8)
    # Use Panda's `read_html` to parse the url
    
    table = pd.read_html(facts)
    mars_df = table[0]
    # Find the mars facts DataFrame in the list of DataFrames
    mars_df = pd.DataFrame(mars_df[0])
    mars_df.columns = ['Description', 'Value']
    html_table = mars_df.set_index('Description', inplace = True)
    f_html_table = html_table.to_html
    #f_html_table.replace('\n', '')
    browser.quit()
    Final_Mars_Dictionary["mars_facts"] = f_html_table
    
    
# ## Mars Hemispheres

# # # def mars_hemispheres():
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        dictionary = {"title": title, "img_url": image_url}
        mars_hemisphere.append(dictionary)
    
    Final_Mars_Dictionary["mars_hemisphere"] = mars_hemisphere

    return Final_Mars_Dictionary
    