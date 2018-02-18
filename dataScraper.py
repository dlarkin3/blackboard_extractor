#!/usr/bin/python2 

from __future__ import print_function
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

# Variables that may need to change for different computers
dataDir = "/home/user1/Projects/Downloads" # directory this code moves or saves all data into
sourcePath="/home/user1/Downloads/" # location that chrome downloads files in. should be empty before running this.
chromeProfile = "user-data-dir=/home/user1/.config/google-chrome" # location of default profile for chrome

# Variables that may need to change for different coursess
filesToDownload = (".pdf",".doc",".docx",".ino",".zip",".txt") # only download this file extensions ignore all else.
# User and assignment values are pulled by inspecting the web html code.
assingmentsOfInterest= ["_48980_1","_48985_1","_48996_1","_48997_1", "_48998_1", "_49000_1", "_48992_1", "_48989_1"]
userValues=['_256771_1', '_256776_1', '_256784_1', '_256770_1', '_256777_1', '_256782_1', '_256775_1', '_256781_1', '_256773_1', '_256783_1', '_256779_1', '_256772_1', '_256774_1', '_256778_1', '_256780_1']

#  Log on
def logOntoBlackBoard(page, user, passw):
    username = page.find_element_by_id('user_id')
    password = page.find_element_by_id('password')
    username.send_keys(user)
    password.send_keys(passw)
    page.find_element_by_name("login").submit()
    time.sleep(3)
    
def enterFullGradeCenter(page):    
    success=False
    for i in range(3):
        try:
            link = page.find_element_by_partial_link_text('MECHATRONICS')
            link.click()
            time.sleep(1)
            link = page.find_element_by_id('menuPuller')
            link.click()
            time.sleep(1)
            link = page.find_element_by_partial_link_text('Grade Center')
            link.click()
            time.f(1)
            link = page.find_element_by_partial_link_text('Full Grade Center')
            link.click()
            time.sleep(1) 
            success=True
            break
        except:
            print ("Failed to enter full grade center trying again.")
    if not success:
        print("Exiting because we could not enter the FULL GRADE CENTER.")
        sys.exit(0)
    

# clicking to open the first assignment page used to start navigating.f
def openFirstAssignment(page):
    time.sleep(1)
    table=page.find_element_by_id("table1")
    row = table.find_elements_by_tag_name("tr")[0]
    cell = row.find_elements_by_tag_name("td")[1]
    element = cell.find_element_by_xpath(".//a[@title='Click for more options']")
    page.execute_script("arguments[0].click();" , element)
    time.sleep(1)     
    assignmentLink = page.find_element_by_xpath(".//a[@title[starts-with(.,'Attempt ')]]").click()

# extract paragraphs and write them to a text file
def saveTextAnswers(page):
    time.sleep(1)
    title=page.find_element_by_id("pageTitleText").text
    sName=page.find_element_by_class_name('students-pager').find_element_by_tag_name('h3').text
    sfName=sName.split()
    sfName=sfName[0]+sfName[1]    
    assignment = page.find_element_by_id("dataCollectionContainer")
    parags = assignment.find_elements_by_tag_name("p")
    fName=re.sub("[^a-zA-Z0-9]+", "", title.split(":")[1])+sfName+".txt"
    fDirName=os.path.join(dataDir,fName)
    with open(fDirName, 'w') as outFile:
        print("Extracted TXT answers from: %s -- %s" % ( title, sName))
        outFile.write(title+" -- "+sName+"\n") 
        outFile.write("FileName is:"+fName+"\n\n\n")     
        for parag in parags:
            if parag.text.startswith("out of "):
                outFile.write("\n")
            else:
                outFile.write(parag.text+"\n")


# download all files with the specified file extensions to the browser down load location then move them
# to the desired location.
#TODO Find a way of avoiding the move step, do a direct download to folder.
def downLoadFiles(page):
    time.sleep(1)
    title=page.find_element_by_id("pageTitleText").text
    sName=page.find_element_by_class_name('students-pager').find_element_by_tag_name('h3').text
    sfName=sName.split()
    sfName=sfName[0]+sfName[1] 
    fName=re.sub("[^a-zA-Z0-9]+", "", title.split(":")[1])+sfName
    fileLinks = page.find_elements_by_xpath(".//a[@href[contains(.,'uploaded_filename')]]")
    print("File Links found: %d" %len(fileLinks))
    for fileLink in fileLinks:
        print(fName,fileLink.text, end='')
        if (fileLink.get_attribute("href").endswith(filesToDownload)):
            page.execute_script("arguments[0].click();" , fileLink)

    time.sleep(10) # delay allow all to download before attempting to move
    # Move files in download dir and construct File name  
    source = os.listdir(sourcePath)
    for sfile in source:
        pathAndNameFile=os.path.join(sourcePath,sfile)
        if os.path.isfile(pathAndNameFile):
            if sfile.endswith((".docx",".doc")):
                newSfile=sfile.split(".")[0]+".pdf"
                try:
                    pypandoc.convert_file(pathAndNameFile, 'pdf', outputfile=os.path.join(sourcePath, newSfile))
                    shutil.move(os.path.join(sourcePath,newSfile),os.path.join(dataDir,(fName+newSfile[32:]))) 
                except:
                    print("Failed to convert %s to %s" % (pathAndNameFile,fName+newSfile[32:]))               
            #print sfile,"\n"
            shutil.move(os.path.join(sourcePath,sfile),os.path.join(dataDir,(fName+sfile[32:])))
            print("Moved the file: %s" % os.path.join(dataDir,(fName+sfile[32:])))

# Helper function to gracefully find if element exists in a page
def check_exists_by_id(page, e_id):
    try:
        page.find_element_by_id(e_id)
    except NoSuchElementException:
        return False
    return True

# Select event to grade
def selectEvent(page, column):
    element = page.find_element_by_id('itemSelect')
    if not element.is_displayed(): # If the Jump to menu is not displayed the display it
        page.find_element_by_xpath(".//a[@title='Jump to...']").click()
    select = Select(element)  
    select.select_by_value(column)


# Select first student to start grading, the others are found by select the next button    
def selectUser(page, event):
    select = Select(page.find_element_by_id('userSelect'))

    for user in userValues: # Finds the first student with an assignment to grade
        try:
            select.select_by_value(user)
            print("WORKING ON EVENT: %s for: %s" % (event,user))
            return
        except:
            print("Exception, user value not on list. Trying Again")
            pass

# Select the assisgnment to grade     
def selectAssignment(page):    
    select = Select(page.find_element_by_id('attemptSelect'))
    select.select_by_index(len(select.options)-1)


if __name__ == "__main__": 
    if len(sys.argv)==2: 
        pwdFile=sys.argv[1]
    else: 
        pwdFile="log_in.txt"
    
    # Open Browser and navigate to assignments  ------------
    options = webdriver.ChromeOptions()
    options.add_argument(chromeProfile) #Path to your chrome profile
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    #options.binary_location = "/usr/bin/chromium-browser"
    options.binary_location = "/usr/bin/google-chrome"
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://usma.blackboard.com')
    with open(pwdFile, 'r') as outFile:    
        logOntoBlackBoard(driver,outFile.readline().strip(),outFile.readline().strip())        
    enterFullGradeCenter(driver)
    openFirstAssignment(driver) #switches web page

    # Begin Navigating to assignement and student pages pulling relevant data.
    for colVal in assingmentsOfInterest:
        try:         
            selectEvent(driver, colVal)
            selectUser(driver, colVal)  
            selectAssignment(driver)
            # Click the Jump to Button to move to next assignment
            link = driver.find_element_by_id('jumpToButton')    
            link.click()
            time.sleep(1)
            title=driver.find_element_by_id("pageTitleText") # This will trigger the exception if an alert popups
        except UnexpectedAlertPresentException:
            # If an alert box appears, click accept and move on
            print("Alert handled by exception")
            driver.switch_to.alert.accept()             
            
        # While content not the page pull it down
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
        except:
            print "Unexpected error:", sys.exc_info()[0]
            print "Moving to next assignment or person."
'''


'''
value="_48992_1">Final Project Paper (Test)
value="_48980_1">Lab #1 (Test)
value="_48985_1">Lab 2 (Test)
value="_50856_1">Lab 3 - Interim (Individual) Deliverables - NEW (Test)
value="_48996_1">Lab 3 - Report and Documentation (Test)
value="_48997_1">Lab 4 - Group Report (Test)
value="_51887_1">Lab 4 - Individual Assignment (Test)
value="_48998_1">Lab 5 - Group Report (Test)
value="_48987_1">Lab 5 - Individual Assignment (Test)
value="_49000_1">Lab 6 - Group Report (Test)
value="_48988_1">Lab 6 - Individual Assignment (Test)
value="_48991_1">Project Paper Outline (Test)
value="_48989_1">Related Work Assignment (Test)
value="_48986_1">WPR 1 scrap (Test)
value="_48999_1">WPR 2 (Test)
'''
              
