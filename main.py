# Scrape Twitter for certain keywords i.e Suffolk Run and determine if the posts are threatening/bad
# Create an admin ui to select different keywords/see info

# import selenium for use with Chrome automation
import selenium
from selenium import webdriver
# inputting keyboard keys into chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# chrome wait for element, change chrome options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options  
# error handling
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

# lets you search twitter by entered location
import geocoder

# GUI creation
from tkinter import *
#TODO https://www.reddit.com/r/learnpython/comments/6tw5ve/tkinter_entry_box_how_to_declare_a_light_grey/
#TODO https://stackoverflow.com/questions/30491721/how-to-insert-a-temporary-text-in-a-tkinter-entry-widget/39677021#39677021

# pause program so it doesnt work faster than the driver can update
# Twitter bot etiquette states you should have at least 1 second in between requests
import time
import datetime

# regular expressions to parse text
import re

def visual_search(root):
    #TODO display where things are beingsearched visually
    geoLabel = Label(root, text="Search Using GeoLocation:")
    #TODO put a greyed out example in the text box
    geoInput = Entry(root, width=40)
    geoEnter = Button(root, text="Enter", padx=10, pady=2)


    geoLabel.grid(row=0, column=0)
    geoInput.grid(row=1, column=0, columnspan=2)
    geoEnter.grid(row=1, column=2)

    allLabel = Label(root, text="All of these words:")
    allInput = Entry(root, width=40)
    allEnter = Button(root, text="Enter", padx=10, pady=2)

    allLabel.grid(row=2, column=0)
    allInput.grid(row=3, column=0, columnspan=2)
    allEnter.grid(row=3, column=2)

    exactLabel = Label(root, text="Exactly this phrase:")
    exactInput = Entry(root, width=40)
    exactEnter = Button(root, text="Enter", padx=10, pady=2)

    exactLabel.grid(row=4, column=0)
    exactInput.grid(row=5, column=0, columnspan=2)
    exactEnter.grid(row=5, column=2)

    orLabel = Label(root, text="Any of these words:")
    orInput = Entry(root, width=40)
    orEnter = Button(root, text="Enter", padx=10, pady=2)

    orLabel.grid(row=6, column=0)
    orInput.grid(row=7, column=0, columnspan=2)
    orEnter.grid(row=7, column=2)

    notLabel = Label(root, text="None of these words:")
    notInput = Entry(root, width=40)
    notEnter = Button(root, text="Enter", padx=10, pady=2)

    notLabel.grid(row=8, column=0)
    notInput.grid(row=9, column=0, columnspan=2)
    notEnter.grid(row=9, column=2)

    hashLabel = Label(root, text="These hashtags (starts with #):")
    hashInput = Entry(root, width=40)
    hashEnter = Button(root, text="Enter", padx=10, pady=2)

    hashLabel.grid(row=10, column=0)
    hashInput.grid(row=11, column=0, columnspan=2)
    hashEnter.grid(row=11, column=2)

    hashLabel = Label(root, text="These hashtags:")
    hashInput = Entry(root, width=40)
    hashEnter = Button(root, text="Enter", padx=10, pady=2)

    hashLabel.grid(row=12, column=0)
    hashInput.grid(row=13, column=0, columnspan=2)
    hashEnter.grid(row=13, column=2)

    mentLabel = Label(root, text="Mentioning these accounts (starts with @):")
    mentInput = Entry(root, width=40)
    mentEnter = Button(root, text="Enter", padx=10, pady=2)

    mentLabel.grid(row=14, column=0)
    mentInput.grid(row=15, column=0, columnspan=2)
    mentEnter.grid(row=15, column=2)

    #TODO tkcalendar might work here instead of text input
    sincLabel = Label(root, text="Since this date:")
    sincInput = Entry(root, width=40)
    sincEnter = Button(root, text="Enter", padx=10, pady=2)

    sincLabel.grid(row=16, column=0)
    sincInput.grid(row=17, column=0, columnspan=2)
    sincEnter.grid(row=17, column=2)

    untLabel = Label(root, text="Until this date:")
    untInput = Entry(root, width=40)
    untEnter = Button(root, text="Enter", padx=10, pady=2)

    untLabel.grid(row=18, column=0)
    untInput.grid(row=19, column=0, columnspan=2)
    untEnter.grid(row=19, column=2)

    latLabel = Label(root, text="Check for the latest tweets:")
    latButton = Button(root, text="Latest", padx=10, pady=5)

    latLabel.grid(row=20, column=0)
    latButton.grid(row=20, column=1)


def query():

    search_query = []

    #TODO break all the search inputs into different functions for use in the GUI

    ### Example: geocode:45.523452,-122.676207,10km
    ### Open Street Map used for geolocation https://operations.osmfoundation.org/policies/nominatim/
    ##print("In this Location ('Mountain View, CA'): ", end = '')
    ##area = input()
    ##geoLoc = geocoder.osm(area)
    ##if geoLoc == "":
    ##    pass
    ##else:
    ##    search_query.append("geocode:" + str(geoLoc.lat) + "," + str(geoLoc.lng) + ",138km,") # 138km is the length of suffolk county
    ##    search_query.append(" ")
    ##print("")

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

    ### Example: “since:yyyy-mm-dd” “until:yyyy-mm-dd”
    ##print("Since, Until these dates (either or both) ", end = '')
    ##print("Since this date (yyyy-mm-dd): ", end = '')
    ##since = input()
    ##print("Until this date (yyyy-mm-dd): ", end = '')
    ##until = input()
    ##if since == "":
    ##    pass
    ##elif until == "":
    ##    pass
    ##else:
    ##    if since:
    ##        search_query.append("since:" + since)
    ##    elif until:
    ##        search_query.append("until:" + until)
    ##search_query.append(" ")
    ##print("")

    for i in search_query:
        print(i)
    
    return search_query

def init_driver():
    # opens a headless/invisible automated version of chrome
    #TODO Headless Chrome off for debugging
    #chrome_options = Options()  
    #chrome_options.add_argument("--headless")  

    driver = webdriver.Chrome(executable_path=r'C:\PythonFiles\TwitterScraper\chromedriver.exe')#, options = chrome_options)  

    return driver

def init_regex():
    # compiling regex query early, once for optimization
    regex = {
        "name": re.compile(r'(?P<name>[a-zA-z0-9 _.]{,50})'), #Needs to find the FIRST one per line
        "username": re.compile(r'(?P<username>@[a-zA-Z_0-9]{,15})'),
        #TODO works with (?s) for no apparent reason, gives a deprecation warning, tweets are supposed to only be 280 chars +- handles/usernames (but not hashtags)
        "text": re.compile(r'((?P<before>(\d(s|m|h|d))|(>@[a-zA-Z_0-9]{,15})|(and \d others))(?P<text>(?s).{,500}))')
    }
    # https://stackoverflow.com/questions/41805522/can-a-python-dictionary-use-re-compile-as-a-key

    return regex

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
 
    # checks for the presence of the search box before typing in search query
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

def pull_tweets(driver, regex):
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

            #key, match = parse_tweets(tweets)

            for i in tweets:
                parse_tweets(i.text, regex)

                #TODO store the tweets/tweet objects somewhere within this loop
 
            # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
            # https://stackoverflow.com/questions/27003423/staleelementreferenceexception-on-python-selenium
            #TODO limit scrolling to x amount of pages/tweets
            #TODO stops automatically when tweets are found faster than the page can update instead of giving TimeoutException
            # twitter limits scrolling in timeline/favorites to around 3200 tweets
            # scroll after finding a set of tweets so the next set appears
            driver.execute_script("arguments[0].scrollIntoView(true);", tweets[-1])

            # waiting a second to adhere to twitters bot rules
            time.sleep(2)
 
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

class TweetObject:
    def __init__(self, name, username, text):
        self.name = ""
        self.username = ""
        self.text = ""

def parse_tweets(unparsedtweet, regexDict):

    f = open("Unorganized.txt", "a", encoding="utf-8", newline='')
    f.write(unparsedtweet.replace("\n", "\\n"))
    f.write("\n")
    f.close()
    
    # Separates each part of a tweet and putting them into respective variables
    for key, tweet in regexDict.items():
        match = tweet.search(unparsedtweet)
        match = match.group(0)
            
        if match:
            print(f"{key.upper()}: {match}")
            if key == 'name':
                name = match
            elif key == 'username':
                username = match
            elif key == 'text':
                text = match
        else:
            print (f"{key.upper()}: NO {key.upper()}")
            if key == 'name':
                name = "NO NAME"
            elif key == 'username':
                username = "NO USERNAME"
            elif key == 'text':
                text = "NO TEXT"

    finalTweet = TweetObject(name, username, text)

    print (finalTweet.name)
    print (finalTweet.username)
    print (finalTweet.text)
    print("")

    return finalTweet


def close_driver(driver):
    # closes chrome web browser
    driver.close()

if __name__ == "__main__":
    #TODO gui creation here
    # initializing Gui
    root = Tk()
    visual_search(root)

    # creating the advanced search tool
    search = query()
  
    # start a driver for a web browser/compiles regex for parsing tweets
    driver = init_driver()
    regex = init_regex()
 
    # log in to twitter (replace username/password with your own)
    login_twitter(driver)

    # the advanced search to be performed
    search_twitter(driver, search)

    # TODO create an actual limit to how many tweets are pulled/can be pulled
    # grabs the tweets from the twitter search
    tweets = pull_tweets(driver, regex)

    # close the driver:
    close_driver(driver)

    root.mainloop()
