# Scrape Twitter for certain keywords i.e Suffolk Run and determine if the posts are threatening/bad
#Create an admin ui to select different keywords/see info

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import numpy
import pandas

browser = webdriver.Chrome(r'C:\PythonFiles\TwitterScraper\chromedriver.exe')

browser.get("http://www.twitter.com")

time.sleep(2)

browser.close()
