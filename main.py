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
    # opens automated version of chrome
    driver = webdriver.Chrome(r'C:\PythonFiles\TwitterScraper\chromedriver.exe') #Chrome 79
    driver.wait = WebDriverWait(driver, 5) 

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


#TODO create own queries instead of using twitters advanced search tool
# geocode:45.523452,-122.676207,10km
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

# TODO switch to mobile twitter
def pull_tweets(driver):
    wait = WebDriverWait(driver, 10)

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


            unparsed = open("Unorganized.txt", "a", encoding='utf-8')
            for i in tweets:
                unparsed.writelines("\n" + i.text +  "\n")
            unparsed.close()
 
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
 
    return tweets

class Tweet(object):
    def __init__(self, tweet_id, tweet_name, tweet_handle, text, comments, retweets, likes):
        self.tweet_id = "" # tweet.id
        self.tweet_name = ""
        self.tweet_handle = ""
        self.text = ""
        self.comments = 0
        self.retweets = 0
        self.likes = 0


def parse_tweets(tweets): #TODO Tweet Object wont pass into function
    
    #TODO account for non english characters, different fonts, and emojis sanitize

    tweetText = []
    tweetText = tweets.text
    splitTweets = (tweetText.splitlines())

            
    parsed = open("Organized.txt", "a", encoding='utf-8')
    for i in splitTweets:
        parsed.writelines(i +  "\n") #TODO removed first newline added to i
    parsed.close()
 
    return splitTweets #TODO make an actual ending function


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


