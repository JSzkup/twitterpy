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

# pause program so it doesnt work faster than the driver can update
# Twitter bot etiquette states you should have at least 1 second in between requests
import time
import datetime

# regular expressions to parse text
import re

def init_driver():
    # opens a headless/invisible automated version of chrome
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  

    driver = webdriver.Chrome(executable_path=r'C:\PythonFiles\TwitterScraper\chromedriver.exe', options = chrome_options)  

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


def search_twitter(driver, keywords, latest):
 
    # checks for the presence of the search box before typing in search query
    box = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search query']")))
    driver.find_element_by_css_selector("input[aria-label='Search query']").clear()
    # your typed keywords is typed in and entered
    box.send_keys(keywords)
    box.submit()

    # initial wait for the search results to load
    driver.implicitly_wait(1)
 
    if latest == 1:
        # clicks "Latest" tab to get most recent tweets
        driver.find_element_by_link_text("Latest").click()
        driver.wait = WebDriverWait(driver, 1) 
    else:
        pass

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
                #TODO place parced tweets into database here as they come through
 
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
        if match == None:
            text = "NO TEXT"
            pass
        else:
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

def make_form(root, fields):

    entries = {}

    # for every field, create a row in the form for entry
    for field in fields:
        row = Frame(root)
        # Each field gets labeled with its field name
        lab = Label(row, width=28, text=field+": ", anchor='w')
        ent = Entry(row, width=30)

        row.pack(side = TOP, fill = X, padx = 10 , pady = 5)
        lab.pack(side = LEFT)
        ent.pack(side = RIGHT, expand = YES, fill = X)

        entries[field] = ent

    return entries

def build_query(entries):

    # final advanced search query put into twitter
    search_query = []

    locWords = str(entries['At this location'].get())
    # uses the entered text to pull specific geolocation from open street maps
    geoLoc = geocoder.osm(locWords)
    if locWords == "":
        pass
    else:
        geoLoc = ("geocode:" + str(geoLoc.lat) + "," + str(geoLoc.lng) + ",138km,") #TODO things are searched 85 miles from the geo point
        search_query.append(geoLoc)
        search_query.append(" ")
    
    allWords = str(entries['All of these words'].get())
    if allWords == "":
        pass
    else:
        search_query.append(allWords)
        search_query.append(" ")

    exaWords = str(entries['This exact phrase'].get())
    if exaWords == "":
        pass
    else:
        exaWords = ("\"" + exaWords +"\"")
        search_query.append(exaWords)
        search_query.append(" ")

    anyWords = str(entries['Any of these words'].get())
    if anyWords == "":
        pass
    else:
        anyWords = (anyWords.replace(" ", " OR "))
        search_query.append(anyWords)
        search_query.append(" ")

    nonWords = str(entries['None of these words'].get())
    if nonWords == "":
        pass
    else:
        nonWords = ("-" + nonWords.replace(" ", " -"))
        search_query.append(nonWords)
        search_query.append(" ")

    hasWords = str(entries['These hashtags'].get())
    if hasWords == "":
        pass
    else:
        search_query.append(hasWords)
        search_query.append(" ")

    menWords = str(entries['Mentioning these accounts'].get())
    if menWords == "":
        pass
    else:
        search_query.append(menWords)
        search_query.append(" ")

    sinWords = str(entries['Since this date (yyyy-mm-dd)'].get())
    if sinWords == "":
        pass
    else:
        search_query.append("since:" + sinWords)
        search_query.append(" ")

    untWords = str(entries['Until this date (yyyy-mm-dd)'].get())
    if untWords == "":
        pass
    else:
        search_query.append("until:" + untWords)
        search_query.append(" ")
        
    for i in search_query:
        print(i)

    return search_query

# twitter and browser functions moved here for UI consistency
def twitter_func(root, search, latest): 
  
    # start a driver for a web browser/compiles regex for parsing tweets
    driver = init_driver()
    regex = init_regex()
 
    # log in to twitter (replace username/password with your own)
    login_twitter(driver)

    # the advanced search to be performed
    search_twitter(driver, search, latest)

    # grabs the tweets from the twitter search
    tweets = pull_tweets(driver, regex)

    # close the driver:
    close_driver(driver)

#TODO loop this every hour ( time.sleep(3600) )
#TODO create UI portion for letting a user decide how far away from the geolocation point things are searched
if __name__ == "__main__":
    # initializing Gui
    root = Tk()
    root.title("Twitter Advanced Search Scraper")

    # creates the form based off the fields in the fields tuple
    fields = ('At this location', 'All of these words', 'This exact phrase', 'Any of these words', 'None of these words', 'These hashtags', 'Mentioning these accounts', 'Since this date (yyyy-mm-dd)', 'Until this date (yyyy-mm-dd)')
    ents = make_form(root, fields)

    # binds the enter key to the submit button
    root.bind('<Return>', (lambda event, e = ents: twitter_func(root, build_query(e), var1.get())))

    # checkbox to allow for showing of only the latest tweets (OFF by default)
    var1 = IntVar()
    checkBox = Checkbutton(root, text="Show the Latest Tweets only?", variable=var1)
    checkBox.pack(side = LEFT, padx = 5, pady = 5)

    submitBtn = Button(root, text = 'Search', bg="light green",
       command=(lambda e = ents: twitter_func(root, build_query(e), var1.get())))
    submitBtn.pack(side = RIGHT, padx = 5, pady = 5)

    #quitBtn = Button(root, text = 'Quit', command = root.quit)
    #quitBtn.pack(side = RIGHT, padx = 10, pady = 10)

    root.mainloop()
    