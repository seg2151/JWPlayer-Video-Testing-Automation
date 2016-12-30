# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 14:21:33 2016

@author: SGarcia
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from URL_List1 import URL_list

class AnyEc:
    """ Use with WebdriverWait to combine expected_conditions in an OR"""
    def __init__(self, *args):
        self.ecs = args
    def __call__(self, driver):
        for fn in self.ecs:
            try:
                if fn(driver): return True
            except:
                pass

#read from text file


options = Options()
options.add_argument('--user-data-dir=C:\\Users\\Sgarcia\\AppData\\Local\\Google\\Chrome\\User Data') #add chrome user profile to chrome driver
driver = webdriver.Chrome(chrome_options=options) # inititate driver with options

driver.get('http://demo.jwplayer.com/ad-tester/') #navigate to the video tester

elem = driver.find_element_by_id('theTag') #space to type in URL
load = driver.find_element_by_name("load") #load button
html = driver.find_element_by_id('radio2') #HTML5 button

ERRORS_list = [] #initiate list to track errors

def run():
    """ Function to fully run arbitrary number of URLs on the video tester"""
    
    for URL in URL_list:
        length = len(URL)
        print(length)
        elem.clear() #clear elem of any characters
        for i in range(0,length, 100): #send URLs in chunks of size 100 (vector limit is ~110)
            elem.send_keys(URL[i:i+100])
        load.click() #click load button
        #wait
        wait = WebDriverWait(driver, 20) #initiate driver wait object with timeout at 20 seconds
        element = wait.until(AnyEc(EC.text_to_be_present_in_element(
                                                                    (By.ID, 'impression'),'The ad impression was fired.'), 
                                   EC.text_to_be_present_in_element(
                                                                    (By.ID, 'anError'),'There was an ad error.') )) #look if text populates the impression fired field OR the ad error field
        error = driver.find_element_by_id('anError') #element that stores error text
        if error.text == 'There was an ad error.':
            ERRORS_list.append(1) 
        else:
            ERRORS_list.append(0)

run()
print('Flash Errors:',ERRORS_list)
ERRORS_list = []
html.click()
run()
print('HTML Errors:', ERRORS_list)

#driver.quit()