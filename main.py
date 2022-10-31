from audioop import avg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import numpy as np
import re

filename = 'keywords.csv'
filetowrite = open('prices.csv', 'a', newline='')

options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver",options=options)

def CleanPrice(price):
    price = re.sub("\.", "", price)
    price = re.sub(",", ".", price)
    price = re.sub(" ", "", price)
    price = re.sub("€", "", price)
    price = re.findall(r"[-+]?(?:\d*\.\d+|\d+)|$", price)
    price = float(price[0])
    return price

def GetProducts(url):
        
    driver.get(url)
    results = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "sh-dgr__content")))
    rowstowrite=[]

    for i in range(0,10):
        price=results[i].find_element(By.CLASS_NAME, "kHxwFf").text
        seller=results[i].find_element(By.CSS_SELECTOR, ".aULzUe.IuHnof").text
        title=results[i].find_element(By.CSS_SELECTOR, ".EI11Pd").text
        link=results[i].find_element(By.CSS_SELECTOR, ".aULzUe.IuHnof").get_attribute("data-href")
        rowtowrite=[title,CleanPrice(price.partition('\n')[0]),seller,link]
        rowstowrite.append(rowtowrite)
        print(rowtowrite)
        
    return rowstowrite


        
driver.get("https://www.google.com/search?tbm=shop&q=asd")
consentbutton=WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#yDmH0d > c-wiz > div > div > div > div.NIoIEf > div.G4njw > div.AIC7ge > div.CxJub > div.VtwTSb > form:nth-child(1) > div > div > button > span")))
consentbutton.click()

with open(filename, 'r') as keywordfile:
    datareader = csv.reader(keywordfile)
    writer = csv.writer(filetowrite)
    for row in datareader:
        url="https://www.google.com/search?tbm=shop&q="+row[0]+" spare"
        writer.writerows(GetProducts(url))
driver.quit



