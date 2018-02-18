#!/usr/bin/python2 
#TODO Testing full program and getting message:

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException  
from selenium.common.exceptions import UnexpectedAlertPresentException 
from selenium.webdriver.support.ui import Select   
    
import re
import time
import os
import shutil
import pypandoc
import sys

dataDir = "/home/user1/Projects/Downloads"

from dataScraper import *

# Open Browser and navigate to assignments  ------------
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/home/user1/.config/google-chrome") #Path to your chrome profile
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
#options.binary_location = "/usr/bin/chromium-browser"
options.binary_location = "/usr/bin/google-chrome"
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://usma.blackboard.com')
## TODO put new login here
enterFullGradeCenter(driver)
openFirstAssignment(driver) #switches web page

assingmentsOfInterest= ["_48980_1","_48985_1","_48996_1","_48997_1", "_48998_1", "_49000_1", "_48992_1", "_48989_1"]
#assingmentsOfInterest= [ "_48992_1", "_48989_1"]
for colVal in assingmentsOfInterest:
    selectEvent(driver, colVal)
    selectUser(driver, colVal)  
    selectAssignment(driver)
    # Click the Jump to Button to move to next assignment
    link = driver.find_element_by_id('jumpToButton')    
    link.click()
    #leaves us off at top of column to pulldown
    saveTextAnswers(driver)
    # While content ont the page pull it down
    done=False
    while (not done):
        saveTextAnswers(driver)
        downLoadFiles(driver) 
        if(check_exists_by_id(driver,'bottom_saveAndNextButton')):
            link = driver.find_element_by_id('bottom_saveAndNextButton')
            link.click()
        else:
            done=True #TODO should we be stopping here?



uname=""
pwd=""
with open("log_in.txt", 'r') as outFile:    
    uname=outFile.readline()
    pwd=outFile.readline()
    
    
print uname,pwd







assingmentsOfInterest= ["_48980_1","_48985_1","_48996_1","_48997_1", "_48998_1", "_49000_1", "_48992_1", "_48989_1"]
#assingmentsOfInterest= [ "_48992_1", "_48989_1"]
for colVal in assingmentsOfInterest:
print("WORKING ON: %s" % colVal)

colVal="_48980_1"
selectEvent(driver, colVal)
selectUser(driver, colVal)  
selectAssignment(driver)

link = driver.find_element_by_id('jumpToButton')    
link.click()

saveTextAnswers(driver)
downLoadFiles(driver) 



fileLink = driver.find_element_by_xpath(".//a[@href[contains(.,'uploaded_filename')]]")








done=False
while (not done):
    saveTextAnswers(driver)
    downLoadFiles(driver) 
    if(check_exists_by_id(driver,'bottom_saveAndNextButton')):
        link = driver.find_element_by_id('bottom_saveAndNextButton')
        link.click()
    else:
        done=True












'''
actions = ActionChains(driver)
actions.move_to_element(fileLink)
actions.context_click(fileLink)
actions.send_keys('k')
actions.send_keys(Keys.ENTER)
actions.perform()

actions = ActionChains(driver)
actions.move_to_element(fileLinks)
actions.context_click(fileLinks)
actions.send_keys('k')
actions.send_keys(Keys.ENTER)
actions.perform()



actions = ActionChains(driver)
actions.move_to_element(fileLinks[0])
actions.context_click(fileLinks[0])
actions.key_down(Keys.CONTROL)
actions.send_keys('s')
actions.key_up(Keys.CONTROL)
actions.perform()



driver = webdriver.Chrome()
actionChains = ActionChains(driver)

actionChains.context_click(your_link).perform()
actionChains.context_click(fileLinks).key_down(Keys.CONTROL).key_down(Keys.CONTROL).key_down(Keys.CONTROL).key_enter(Keys.CONTROL).build().perform()
key_down(Keys.CONTROL)

actionChains.key_down(Keys.ENTER).perform()
'''

