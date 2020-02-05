# Scrape Twitter for certain keywords i.e Suffolk Run and determine if the posts are threatening/bad
# Create an admin ui to select different keywords/see info

# import selenium for use with Chrome automation
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# error handling
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

# parse HTML tweets
from bs4 import BeautifulSoup as bs

# pause program so it doesnt work faster than the driver can update
# Twitter bot etiquette states you should have at least 1 second in between requests
import time
import datetime

### organizing info
##import numpy
##import pandas

# regular expressions to parse text
import re

def init_driver():
    #Chrome 79
    driver = webdriver.Chrome(r'C:\PythonFiles\TwitterScraper\chromedriver.exe')
    driver.wait = WebDriverWait(driver, 5) 

    return driver

def login_twitter(driver):
 
    #TODO Look into https://twitter.com/search-advanced / Making a UI for these inputs specifically

    # open the web page in the browser:
    driver.get("https://twitter.com/explore")
    WebDriverWait(driver,1)
 
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
 
    box = driver.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"react-root\"]/div/div/div[2]/header/div[2]/div[1]/div[1]/div/div[2]/div/div/div/form/div[1]/div/div/div[2]/input")))
    driver.find_element_by_xpath("//*[@id=\"react-root\"]/div/div/div[2]/header/div[2]/div[1]/div[1]/div/div[2]/div/div/div/form/div[1]/div/div/div[2]/input").clear()
    # your typed keywords is typed in
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

    try:
        # wait until the first search result is found. Search results will be tweets, which are html list items and have the class='data-item-id'
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[aria-label=\"Timeline: Search timeline\"]")))
 
        # scroll down to the last tweet until there are no more tweets
        while True:
 
            # extract all the tweets
            tweets = driver.find_elements_by_css_selector("article[role='article']")

            #print tweets to
            for i in tweets:
                print(i.text)
                print("\n\n")
 
            # find number of visible tweets
            number_of_tweets = len(tweets)
 
            # keep scrolling
            driver.execute_script("arguments[0].scrollIntoView(true);", tweets[-1])
            driver.implicitly_wait(1)
 
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
 
    return tweets

class Tweet(object):
    def __init__(self, tweet_id, tweet_name, tweet_handle, text, comments, retweets, likes):
        self.tweet_id = ""
        self.tweet_name = ""
        self.tweet_handle = ""
        self.text = ""
        self.comments = 0
        self.retweets = 0
        self.likes = 0


def parse_tweets(tweets):
    
    parsedText = []

    #for i in tweets:
    #    text = i.text
 




        ##tweet = {
        ##    'tweet_id': li['data-item-id'],
        ##    'text': None,
        ##    'user_id': None,
        ##    'user_screen_name': None,
        ##    'user_name': None,
        ##    'created_at': None,
        ##    'retweets': 0,
        ##    'likes': 0,
        ##    'replies': 0
        ##}
 
    return parsedText


def close_driver(driver):
    driver.close()

if __name__ == "__main__":
 
    # start a driver for a web browser
    driver = init_driver()
 
    # log in to twitter (replace username/password with your own)
    login_twitter(driver)
 
    # What is written in the twitter searchbar 
    # TODO look into advanced search
    keywords = "Suffolk County"
    search_twitter(driver, keywords)

    tweets = pull_tweets(driver)
 
    # extract info from the search results
    finalTweets = parse_tweets(tweets)


    # close the driver:
    close_driver(driver)


""" 
Might be a better Idea to use scrapy or Tweepy with the Twitter API
Tweepy would make pulling info from tweets easier but I need API keys
scrapy would make organizing the data after scraping easier
"""
