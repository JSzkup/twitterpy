# Scrape Twitter for certain keywords i.e Suffolk Run/COVID19
# then determine if the posts are threatening/bad or are useful to police
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
# TODO when everything is done import only needed things from tkinter
from tkinter import *

# connecting/writing to database
import pyodbc

# pause program so it doesnt work faster than the driver can update
# Twitter bot etiquette states you should have at least 1 second in between requests
import time
import datetime
from datetime import datetime

# regular expressions to parse text
import re


# opens a headless/invisible automated version of chrome
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(
        executable_path=r'chromedriver.exe', options=chrome_options)

    return driver


# compiling regex query early as dictionary, once for optimization
def init_regex():
    regex = {
        # Needs to find the FIRST one per line
        "name": re.compile(r'(?P<name>[a-zA-Z0-9 _.]{,50})'),
        "username": re.compile(r'(?P<username>@[a-zA-Z_0-9]{,15})'),
        # TODO hacky nonetext fix by increading character count to 1000 in text
        "text": re.compile(r'((?P<before>(\d(s|m|h|d))|(>@[a-zA-Z_0-9]{,15})|(and \d others))(?P<text>.{,1000}))', re.DOTALL | re.MULTILINE)
    }
    # https://stackoverflow.com/questions/41805522/can-a-python-dictionary-use-re-compile-as-a-key

    return regex


# opens twitter explore page in the browser
def login_twitter(driver):

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


# types in keywords defined by the user in the ui
# selects whether latest tweets are searched for
def search_twitter(driver, keywords, latest):

    # checks for the presence of the search box before typing in search query
    box = driver.wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[aria-label='Search query']")))
    driver.find_element_by_css_selector(
        "input[aria-label='Search query']").clear()
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


# finds the tweet on page, then copies its content to a variable
# scrolls the page to copy more tweets until no more new tweets are found
def pull_tweets(driver, regex, search):
    wait = WebDriverWait(driver, 10)

    try:
        # wait until the first search result is found Search results will be
        # tweets which are html list items and have the class='data-item-id'
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[aria-label=\"Timeline: Search timeline\"]")))

        # scroll down to the last tweet until there are no more tweets
        while True:

            # extract all the tweets
            tweets = driver.find_elements_by_css_selector(
                "article[role='article']")

            # find number of visible tweets
            number_of_tweets = len(tweets)

            for i in tweets:
                parse_tweets(i.text, regex, search)

            # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
            # https://stackoverflow.com/questions/27003423/staleelementreferenceexception-on-python-selenium
            # TODO limit scrolling to x amount of pages/tweets
            # TODO stops automatically when tweets are found faster than the page can update instead of giving TimeoutException
            # twitter limits scrolling in timeline/favorites to around 3200 tweets
            # scroll after finding a set of tweets so the next set appears
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", tweets[-1])

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

    print("Done Searching Tweets")

    return tweets


# puts the current tweet in a database
# each query is a new table titled after the search/time search was done
# def databasing(name, username, text, search):
    # TODO only connect to sql database once, write everything to it, then close after no tweets are found (cnxn.close())

    # cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
    # r"Server=JON\SQLEXPRESS;"
    # "Database=twitterpy;"
    # "Trusted_Connection=yes")
##
    ##cursor = cnxn.cursor()
##
    ##search = ''.join([str(elem) for elem in search])
    ##search = str(search.replace(" ", "_"))
##
    ##currently = datetime.today()
    ##currently = str(currently).replace(" ", "_")
    ##currently = currently.strip()
##
    ##currently = currently.replace("-", "_")
    ##currently = currently.replace(":", "_")
    ##currently = currently.replace(".", "_")
##
    # TODO cut off trailing milliseconds from datetime
    ##search = (search + currently)
##
    ##text = text.replace(",", "(comma)")
##
    ##print("Search/Table Name: " + search)
    ##print("Tweet Name: " + name)
    ##print("Tweet Username: " + username)
    ##print("Tweet text: " + text)
##
    # TODO incorrect syntax on table title
    # https://doc.4d.com/4Dv15/4D/15.6/Rules-for-naming-tables-and-fields.300-3836655.en.html
    # cursor.execute(f"""CREATE TABLE {search} (
    # tweet_name NVARCHAR(60) NOT NULL,
    # tweet_user NVARCHAR(20) NOT NULL,
    # tweet_text NVARCHAR(1000) NOT NULL);""")
    # cnxn.commit()
##
    # cursor.execute(f"""INSERT INTO {search}
    ##                    (tweet_name, tweet_user, tweet_text)
    # VALUES
    # ('{name}'),
    # ('{username[1:]}'),
    # ('{text}');""")
    # cnxn.commit()
    # cnxn.close()
    # return search


# object representing each tweet
class TweetObject:
    def __init__(self, name, username, text):
        self.name = ""
        self.username = ""
        self.text = ""


# appends tweet to a text file
# using the regex dict, the tweet block is separated into name/user/text
# tweets are then sent to be databased
def parse_tweets(unparsedtweet, regexDict, search):
    f = open("foundTweets.txt", "a", encoding="utf-8", newline="\n")
    # TODO more clearly separate tweets within the text file
    f.write("\n" + unparsedtweet + r"\n")
    f.close()

    # Separates each part of a tweet and putting them into respective variables
    for key, tweet in regexDict.items():
        match = tweet.search(unparsedtweet)
        if match is None:
            # TODO text=notext is hacky, leaves 0 text a lot of the time instead of just preventing None Error
            text = "TEXT CANNOT BE FOUND"
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
            print(f"{key.upper()}: NO {key.upper()}")
            if key == 'name':
                name = "NO NAME"
            elif key == 'username':
                username = "NO USERNAME"
            elif key == 'text':
                text = "NO TEXT"

    finalTweet = TweetObject(name, username, text)

    # f.write(unparsedtweet)

    name = finalTweet.name
    username = finalTweet.username
    text = finalTweet.text

    #databasing(name, username, text, search)

    ##print (finalTweet.name)
    ##print (finalTweet.username)
    ##print (finalTweet.text)
    print("")


# closes chrome web browser until next query
def close_driver(driver):
    driver.close()


# builds the form UI using fields supplied in __main__
def make_form(root, FIELDS):

    entries = {}

    # TODO greyed out examples in input fields

    # for every field, create a row in the form for entry
    for field in FIELDS:
        row = Frame(root)
        # Each field gets labeled with its field name
        lab = Label(row, width=28, text=field+": ", anchor='w')
        ent = Entry(row, width=30)

        row.pack(side=TOP, fill=X, padx=10, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)

        entries[field] = ent

    return entries


# grabs input from the user in the UI and formats it so twitter can
# perform advanced search queries
def build_query(entries):

    # final advanced search query put into twitter
    search_query = []

    locWords = str(entries['At this location'].get())
    # uses the entered text to pull specific geolocation from open street maps
    geoLoc = geocoder.osm(locWords)
    if locWords == "":
        pass
    else:
        # things are searched 85 miles from the geo point
        geoLoc = ("geocode:" + str(geoLoc.lat) +
                  "," + str(geoLoc.lng) + ",138km,")
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
        exaWords = ("\"" + exaWords + "\"")
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

    listToStr = ''.join([str(elem) for elem in search_query])
    print(listToStr)

    return search_query


# twitter and browser functions moved here for UI consistency
def twitter_func(root, search, latest, loop):

    while loop in (0, 1):
        # start a driver for a web browser/compiles regex for parsing tweets
        driver = init_driver()
        regex = init_regex()

        # log in to twitter (replace username/password with your own)
        login_twitter(driver)

        # the advanced search to be performed
        search_twitter(driver, search, latest)

        # grabs the tweets from the twitter search
        tweets = pull_tweets(driver, regex, search)

        # close the driver:
        close_driver(driver)

        if loop == 1:
            time.sleep(3600)
        else:
            break


# TODO create UI portion for letting a user decide how far away from the geolocation point things are searched
# TODO show tweets in the GUI
# TODO add consolve view to bottom of gui to show tweets in gui
if __name__ == "__main__":
    # initializing Gui
    root = Tk()

    # adds a title and an icon to the window
    root.title("Twitter Advanced Search Scraper")
    root.wm_iconbitmap('twitterIcon.ico')

    # creates the form based off the fields in the fields tuple
    FIELDS = ('At this location', 'All of these words', 'This exact phrase', 'Any of these words', 'None of these words',
              'These hashtags', 'Mentioning these accounts', 'Since this date (yyyy-mm-dd)', 'Until this date (yyyy-mm-dd)')
    ents = make_form(root, FIELDS)

    # binds the enter key to the submit button
    root.bind('<Return>', (lambda event, e=ents: twitter_func(
        root, build_query(e), var1.get(), var2.get())))

    # frame created to separate options from text input and output
    options = Frame(root)

    # checkbox to allow for showing of only the latest tweets (OFF by default)
    var1 = IntVar()
    checkBox = Checkbutton(
        options, text="Show the Latest Tweets only?", variable=var1)
    checkBox.pack(side=LEFT, padx=5, pady=5)

    var2 = IntVar()
    checkBox = Checkbutton(options, text="Run Hourly?", variable=var2)
    checkBox.pack(side=LEFT, padx=5, pady=5)

    padding = Label(options)
    padding.pack(side=LEFT, padx=140)

    submitBtn = Button(options, text='Search', bg="light green",
                       command=(lambda e=ents: twitter_func(root, build_query(e), var1.get(), var2.get())))
    submitBtn.pack(side=RIGHT, padx=5, pady=5)

    options.pack()

    # adds scrollbae ro outputBox
    scroll = Scrollbar(root)
    scroll.pack(side=RIGHT, fill=Y)

    # TODO maybe put this in a frame and have it only appear after a search to keep the UI simple
    # TODO pack it after search is pressed/enter key
    # Large text box to show tweets in GUI once they are pulled
    outputBox = Text(root, bg="white", height=20,
                     wrap=NONE, yscrollcommand=scroll.set)
    outputBox.pack(side=BOTTOM, padx=5, pady=5, fill=X)

    root.mainloop()
