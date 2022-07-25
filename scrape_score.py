from h11 import Data
import pandas as pd
from inspect import getfile
from os.path import exists, getsize
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome('./chromedriver.exe')

PEOPLE_FILE = "people.tsv"
DATA_FILE = "politifact.tsv"

def extract_factuality(name, party, url):
    global driver

    checks = {
        "name": name,
        "party": party
    }

    driver.get(url)
    scorecard = driver.find_elements(By.CLASS_NAME, "m-scorecard__item")

    for score in scorecard:
        tag = score.find_element(By.XPATH, 'h4').text
        number = score.find_element(By.XPATH, 'div/p/a').text
        checks[tag.lower()] = int(number.split(' ')[0]) 
    
    return checks

existing_people = set()
with open(DATA_FILE) as fin:
    fin.readline()
    for line in fin:
        existing_people.add(line.strip().split('\t')[0])


fin = open(PEOPLE_FILE, "r")
fout = open(DATA_FILE, "a")

fin.readline()

i = 0
for line in fin:
    name, party, link = line.strip().split('\t')

    if name in existing_people:
        print("Skipped:", name)
        continue

    print("Processing:", name)
    f = extract_factuality(name, party, link)
    fout.write(f"{name}\t{party}\t{f['true']}\t{f['mostly true']}\t{f['half true']}\t{f['mostly false']}\t{f['false']}\t{f['pants on fire']}\n")
    
    i += 1


fin.close()
fout.close()