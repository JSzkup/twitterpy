# Scrape Twitter for certain keywords i.e Suffolk Run and determine if the posts are threatening/bad
# Create an admin ui to select different keywords/see info

# import selenium for use with Chrome automation
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

# parse HTML tweets
from bs4 import BeautifulSoup as bs

# pause program so it doesnt work faster than the driver can update
import time
import datetime

# ordering info
import numpy
import pandas

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
 
    # wait until the search box has loaded to search within it
    wait = WebDriverWait(driver, 10)
    box = driver.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"react-root\"]/div/div/div[2]/header/div[2]/div[1]/div[1]/div/div[2]/div/div/div/form/div[1]/div/div/div[2]/input")))
    driver.find_element_by_xpath("//*[@id=\"react-root\"]/div/div/div[2]/header/div[2]/div[1]/div[1]/div/div[2]/div/div/div/form/div[1]/div/div/div[2]/input").clear()
    # your typed keywords is typed in
    box.send_keys(keywords)
    box.submit()

    # initial wait for the search results to load
    driver.implicitly_wait(1)
 
    driver.find_element_by_link_text("Latest").click()
    driver.wait = WebDriverWait(driver, 1) 

    try:
        # wait until the first search result is found. Search results will be tweets, which are html list items and have the class='data-item-id'
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "data-testid=\"tweet\"")))
 
        # scroll down to the last tweet until there are no more tweets
        while True:
 
            # extract all the tweets
            tweets = driver.find_elements_by_css_selector("data-testid=\"tweet\"")
 
            # find number of visible tweets
            number_of_tweets = len(tweets)
 
            # keep scrolling
            driver.execute_script("arguments[0].scrollIntoView();", tweets[-1])
 
            try:
                # wait for more tweets to be visible
                wait.until(WaitForMoreThanNElementsToBePresent(
                    (By.CSS_SELECTOR, "data-testid=\"tweet\""), number_of_tweets))
 
            except TimeoutException:
                # if no more are visible the "wait.until" call will timeout. Catch the exception and exit the while loop
                break
 
        # extract the html for the whole lot
        page_source = driver.page_source
 
    except TimeoutException:
 
        # if there are no search results then the "wait.until" call in the first "try" statement will never happen and it will time out. So we catch that exception and return no html
        page_source=None #TODO Throws errors at bs4 when NONE
 
    return page_source

def extract_tweets(page_source):
 
    soup = bs(page_source,'lxml')
 
    tweets = []
    for li in soup.find_all("li", class_='js-stream-item'):
 
        # If our li doesn't have a tweet-id, we skip it as it's not going to be a tweet.
        if 'data-item-id' not in li.attrs:
            continue
 
        else:
            tweet = {
                'tweet_id': li['data-item-id'],
                'text': None,
                'user_id': None,
                'user_screen_name': None,
                'user_name': None,
                'created_at': None,
                'retweets': 0,
                'likes': 0,
                'replies': 0
            }
 
            # Tweet Text
            text_p = li.find("p", class_="tweet-text")
            if text_p is not None:
                tweet['text'] = text_p.get_text()
 
            # Tweet User ID, User Screen Name, User Name
            user_details_div = li.find("div", class_="tweet")
            if user_details_div is not None:
                tweet['user_id'] = user_details_div['data-user-id']
                tweet['user_screen_name'] = user_details_div['data-screen-name']
                tweet['user_name'] = user_details_div['data-name']
 
            # Tweet date
            date_span = li.find("span", class_="_timestamp")
            if date_span is not None:
                tweet['created_at'] = float(date_span['data-time-ms'])
 
            # Tweet Retweets
            retweet_span = li.select("span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount")
            if retweet_span is not None and len(retweet_span) > 0:
                tweet['retweets'] = int(retweet_span[0]['data-tweet-stat-count'])
 
            # Tweet Likes
            like_span = li.select("span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount")
            if like_span is not None and len(like_span) > 0:
                tweet['likes'] = int(like_span[0]['data-tweet-stat-count'])
 
            # Tweet Replies
            reply_span = li.select("span.ProfileTweet-action--reply > span.ProfileTweet-actionCount")
            if reply_span is not None and len(reply_span) > 0:
                tweet['replies'] = int(reply_span[0]['data-tweet-stat-count'])
 
            tweets.append(tweet)
 
    return tweets


def close_driver(driver):
    driver.close()

if __name__ == "__main__":
 
    # start a driver for a web browser
    driver = init_driver()
 
    # log in to twitter (replace username/password with your own)
    login_twitter(driver)
 
    # What is written in the twitter searchbar
    #TODO Should I be querying for hashtages or strictly keywords
    keywords = "Suffolk County"
    page_source = search_twitter(driver, keywords)
 
    # extract info from the search results
    tweets = extract_tweets(page_source)

 
    # close the driver:
    close_driver(driver)


""" 
Might be a better Idea to use scrapy or Tweepy with the Twitter API
Tweepy would make pulling info from tweets easier but I need API keys
scrapy would make organizing the data after scraping easier
"""

""" Reference
https://twitter.com/robots.txt
https://selenium-python.readthedocs.io/
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
https://towardsdatascience.com/web-scrape-twitter-by-python-selenium-part-1-b3e2db29051d
https://towardsdatascience.com/selenium-tweepy-to-scrap-tweets-from-tweeter-and-analysing-sentiments-1804db3478ac
https://towardsdatascience.com/hands-on-web-scraping-building-your-own-twitter-dataset-with-python-and-scrapy-8823fb7d0598
"""