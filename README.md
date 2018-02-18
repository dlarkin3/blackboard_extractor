# Downloads files from Blackboard Mechatronics course

## Extract data from Blackboard. 
This downloads all files that end with: (".pdf",".doc",".docx",".ino",".zip",".txt") and copies all text entries into a file.
This code is written for Python2.7

## Dependencies (probably not all)
- `sudo apt-get install selenium`
- `sudo pip install -U selenium`
- `sudo apt-get install pandoc`
- `sudo pip install pypandoc`
- `sudo apt-get install chromium-chromedriver*`

## Required: 
1. Change the default settings to make chrome download a pdf if it is a link instead of opening it in a viewer.
I used this site to find the option then enabled "Download PDF files ... ": `https://support.google.com/chrome/answer/6213030?hl=en`
2. The code must use the users chrome default settings. The code assumes they are located at: `/home/user1/.config/google-chrome`. 
To change this modify only the path part of the variable called `chromeProfile` found around line 32 in the code. 
3. The code assumes that chrome downloads files to the `/home/user1/Downloads/` directory. To change this modify the variable `sourcePath`
found around line 31 in the code.
    - WARNING WARNING: The download directory should be empty before running the code. This code moves all files from this directory
    to the specified data directory.
4. If you receive an error saying that chromium driver must be in your path then run these commands in the terminal: 
    - `PATH=$PATH:/usr/lib/chromium-browser`
5. Most variables that need to change for different courses and different computers can be found starting around line 30 in the code

## STEP 1: Run web scraper script
1. Create a text file with the Blackboard user name on one line and the password on the next.
2. Run the program `./dataScraper.py filename_of_passwored_file.txt`
3. This file puts the downloaded files and text files in the directory: /home/user1/Projects/Downloads this can be changed 
in the code by changing the `dataDir` variable found around line 30.

## STEP 2: Extract pdf files from any ZIP files
1. Run the command:
 - `./zipToPdf.py`

## STEP 3: Parse the pdf files
1. Run the command:
 - `./pdf_parser.py`

## STEP 4: Parse the txt files
1. Run the command:
 - `./txt_parser.py`
 
