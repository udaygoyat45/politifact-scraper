import pandas as pd
from inspect import getfile
from os.path import exists, getsize
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome('./chromedriver.exe')

FILENAME = "people.tsv"

existing_people = set()
with open(FILENAME) as fin:
    fin.readline()
    for line in fin:
        existing_people.add(line.strip().split('\t')[2])

driver.get("https://www.politifact.com/personalities/")
people = driver.find_elements(By.CLASS_NAME, 'c-chyron')
people_data = []

fout = open(FILENAME, "a")

for i, person in enumerate(people):
    try:
        link = person.find_element(By.XPATH, 'div/a')
        if link.get_attribute('href') in existing_people:
            print("Skipped:", (i + 1) / len(people), link.text,"                ", end='\r')
            continue
        
        party = person.find_element(By.CLASS_NAME, 'c-chyron__subline')
        fout.write(f"{link.text}\t{party.text}\t{link.get_attribute('href')}\n")
        print("Loading People: ", (i + 1) / len(people))

    except NoSuchElementException:
        print("Couldn't find the child elements :( Skipping...")

fout.close()