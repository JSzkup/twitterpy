# Scrape Twitter for certain keywords i.e Suffolk Run and determine if the posts are threatening/bad
# Create an admin ui to select different keywords/see info

# import selenium for use with Chrome automation
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options  

# error handling
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

# parse HTML tweets
import pandas as pd

# Read xml
from bs4 import BeautifulSoup as bs

#TODO implement TKinter for writing search terms and selecting whether or not to use the latest search terms/geolocation

#TODO recheck requirements.txt and cleanup unused imports

# pause program so it doesnt work faster than the driver can update
# Twitter bot etiquette states you should have at least 1 second in between requests
import time
import datetime

# regular expressions to parse text
import re

# Custom search query is entered before the browser starts up
#TODO geocodes to search for tweets geocode:45.523452,-122.676207,10km
# https://geocoder.readthedocs.io/
def query():

    search_query = []

    # Example: what’s happening · contains both “what’s” and “happening”
    print("All of These words: ", end = '')
    allW = input()
    if allW == "":
        pass
    else:
        search_query.append(allW)
        search_query.append(" ")
    print("")

    ### Example: happy hour · contains the exact phrase “happy hour”
    ##print("This Exact Phrase: ", end = '')
    ##exactW = input()
    ##if exactW == "":
    ##    pass
    ##else:
    ##    search_query.append("\"" + exactW +"\"")
    ##    search_query.append(" ")
    ##print("")
##
    ### Example: cats dogs · contains either “cats” or “dogs” (or both)
    ##print("Any of these words: ", end = '')
    ##anyW = input()
    ##if anyW == "":
    ##    pass
    ##else:
    ##    search_query.append(anyW.replace(" ", " OR "))
    ##    search_query.append(" ")
    ##print("")
##
    ### Example: cats dogs · does not contain “cats” and does not contain “dogs”
    ##print("None of these Words: ", end = '')
    ##noneW = input()
    ##if noneW == "":
    ##    pass
    ##else:
    ##    search_query.append("-" + noneW.replace(" ", " -"))
    ##    search_query.append(" ")
    ##print("")
##
    ### Example: #ThrowbackThursday · contains the hashtag #ThrowbackThursday
    ##print("These hashtags (starts with #): ", end = '')
    ##hashW = input()
    ##if hashW == "":
    ##    pass
    ##else:
    ##    search_query.append(hashW)
    ##    search_query.append(" ")
    ##print("")
##
    ### Example: @SFBART @Caltrain · mentions @SFBART or mentions @Caltrain
    ##print("Mentioning these accounts (starts with @): ", end = '')
    ##mentW = input()
    ##if mentW == "":
    ##    pass
    ##else:
    ##    search_query.append(mentW)
    ##    search_query.append(" ")
    ##print("")

    #TODO date selection    

    for i in search_query:
        print(i)


    #result = [" "] * (len(search_query) * 2 - 1)
    #result[0::2] = search_query

    #print(str(result))
    
    return search_query

def init_driver():
    # opens a headless/invisible automated version of chrome
    #TODO temporarily gave Chrome a head again
    #chrome_options = Options()  
    #chrome_options.add_argument("--headless")  

    driver = webdriver.Chrome(executable_path=r'C:\PythonFiles\TwitterScraper\chromedriver.exe')#, options = chrome_options)  

    return driver

def login_twitter(driver):
 
    # open the web page in the browser:
    driver.get("https://twitter.com/explore")
    driver.wait = WebDriverWait(driver, 1)
 
    return

# scrolls the page/waits for more elements to be visible to scroll again
class WaitForMoreThanNElementsToBePresent(object):
    def __init__(self, locator, count):
        self.locator = locator
        self.count = count
 
    def __call__(self, driver):
        try:
            elements = EC._find_elements(driver, self.locator)
            return len(elements) > self.count
        except selenium.common.exceptions.StaleElementReferenceException:
            return False


def search_twitter(driver, keywords):
 
    #TODO Twitter changed its searchbox XPATH, check to see what/if has been changed on twitters end
    box = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search query']")))
    driver.find_element_by_css_selector("input[aria-label='Search query']").clear()
    # your typed keywords is typed in and entered
    box.send_keys(keywords)
    box.submit()

    # initial wait for the search results to load
    driver.implicitly_wait(1)
 
    # clicks "Latest" tab to get most recent tweets
    driver.find_element_by_link_text("Latest").click()
    driver.wait = WebDriverWait(driver, 1) 

    return

def pull_tweets(driver):
    wait = WebDriverWait(driver, 10)

    # pulls xml from current opened page
    page_source = driver.page_source
    soup = bs(page_source,'lxml')
    # writes xml to an xml file in main dir (overwrites itself on run)
    xmltest = open("xmlTest.xml", "w", encoding='utf-8')
    xmltest.writelines(str(soup))
    xmltest.close()

    try:
        # wait until the first search result is found. Search results will be tweets, which are html list items and have the class='data-item-id'
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[aria-label=\"Timeline: Search timeline\"]")))
 
        # scroll down to the last tweet until there are no more tweets
        while True:
 
            # extract all the tweets
            tweets = driver.find_elements_by_css_selector("article[role='article']")

            ### print tweets to console
            ##for i in tweets:
            ##    print(i.text)
            ##    print("\n\n")
 
            # find number of visible tweets
            number_of_tweets = len(tweets)

            #TODO add the rest of Regextest Here or in another function for clarity

            #key, match = parse_tweets(tweets)

            for i in tweets:
                parse_tweets(i.text)
 
            # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
            # https://stackoverflow.com/questions/27003423/staleelementreferenceexception-on-python-selenium
            #TODO limit scrolling to x amount of pages/tweets
            #TODO stops automatically when tweets are found faster than the page can update instead of giving TimeoutException
            # twitter limits scrolling in timeline/favorites to around 3200 tweets
            # scroll after finding a set of tweets so the next set appears
            driver.execute_script("arguments[0].scrollIntoView(true);", tweets[-1])
            # Twitter kindly asks to wait at least a second between requests
            time.sleep(1)
            #driver.implicitly_wait(1)
 
            try:
                # wait for more tweets to be visible
                wait.until(WaitForMoreThanNElementsToBePresent(
                    (By.CSS_SELECTOR, "article[role='article']"), number_of_tweets))
 
            except TimeoutException:
                # if no more are visible the "wait.until" call will timeout. Catch the exception and exit the while loop
                break
 
    except TimeoutException:
 
        # if there are no search results then the "wait.until" call in the first "try" statement will never happen and it will time out. So we catch that exception and return no html
        tweets = None

    #TODO create an sql db for storing tweets (mySQL / NoSQL / MongoDB)
 
    return tweets

#TODO create a tweet object and have parse tweets create a new object instance per tweet then add name/use/text to it


#TODO part of the loop when finding the tweets should be parsing it piece by piece, then storing it somewhere LOG/DATABASE
def parse_tweets(tweets):
    
    tweet_dict = {
        "name": re.compile(r'(?P<name>[a-zA-z0-9 _.]{,50})'), #Needs to find the FIRST one per line
        "username": re.compile(r'(?P<username>@[a-zA-Z_0-9]{,15})'),
        "text": re.compile(r'(?P<before>(\d(s|m|h|d))|(>@[a-zA-Z_0-9]{,15})|(and \d others))(?P<text>.{,280})'),
    }

    for key, tweet in tweet_dict.items():
        match = tweet.search(tweets)
        match = match.group(0)
        if match:
            print(f"{key.upper()}: {match}")
            return key, match
        else:
            print (f"{key.upper()}: NO {key.upper()}")
            return key, None
    print("")

def close_driver(driver):
    driver.close()

if __name__ == "__main__":
    # creating the advanced search tool
    search = query()
  
    # start a driver for a web browser
    driver = init_driver()
 
    # log in to twitter (replace username/password with your own)
    login_twitter(driver)

    # the advanced search to be performed
    search_twitter(driver, search)

    # TODO create an actual limit to how many tweets are pulled/can be pulled
    # grabs the tweets from the twitter search
    tweets = pull_tweets(driver)
 
    # extract info from the search results
    finalTweets = parse_tweets(tweets)

    # close the driver:
    close_driver(driver)


