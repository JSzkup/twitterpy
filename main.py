# Scrape Twitter for certain keywords i.e Suffolk Run and determine if the posts are threatening/bad
#Create an admin ui to select different keywords/see info

# Import selenium for use with Chrome automation
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

#Pause program so it doesnt work faster than the driver can update
import time
import datetime

#Ordering info
import numpy
import pandas

USERNAME = "lorem"
PASSWORD = "Ipsum"

def init_driver():
    #Chrome 79
    driver = webdriver.Chrome(r'C:\PythonFiles\TwitterScraper\chromedriver.exe')
    driver.wait = WebDriverWait(driver, 5) 

    return driver

def login_twitter(driver, USERNAME, PASSWORD):
 
    # open the web page in the browser:
    driver.get("https://twitter.com/login")
 
    # find the boxes for username and password
    username_field = driver.find_element_by_class_name("js-username-field")
    password_field = driver.find_element_by_class_name("js-password-field")
 
    # enter credentials
    username_field.send_keys(USERNAME)
    driver.implicitly_wait(1)
    password_field.send_keys(PASSWORD)
    driver.implicitly_wait(1)
 
    # click the "Log In" button:
    driver.find_element_by_class_name("EdgeButtom--medium").click()
 
    return



def close_driver(driver):
    driver.close()


""" Reference
https://selenium-python.readthedocs.io/
https://towardsdatascience.com/web-scrape-twitter-by-python-selenium-part-1-b3e2db29051d
https://towardsdatascience.com/selenium-tweepy-to-scrap-tweets-from-tweeter-and-analysing-sentiments-1804db3478ac
"""