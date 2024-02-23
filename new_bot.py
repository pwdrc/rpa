import os
import requests as rq
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

excelFile = r"C:\Users\tolvo\Desktop\desafio\challenge.xlsx"
if not os.path.exists(excelFile):
    response = rq.get('https://rpachallenge.com/assets/downloadFiles/challenge.xlsx')
    with open(excelFile, 'wb') as file:
        file.write(response.content)
dataFrame = pd.read_excel(excelFile)
#dataFrame.info()

url = 'https://rpachallenge.com/'
driver = webdriver.Chrome()
driver.get(url)
startButton = driver.find_element(By.XPATH, '/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/button')
startButton.click()

#for index, row in dataFrame.iterrows():
#print(dataFrame.columns)
for _, row in dataFrame.iterrows():
    name = row['First Name']
    surname = row['Last Name ']
    company = row['Company Name']
    role = row['Role in Company']
    address = row['Address']
    email = row['Email']
    phone = row['Phone Number']

    nameForm = driver.find_element(By.XPATH, '//*[@ng-reflect-name="labelFirstName"]')
    nameForm.send_keys(name)

    surnameForm = driver.find_element(By.XPATH, '//*[@ng-reflect-name="labelLastName"]')
    surnameForm.send_keys(surname)

    companyForm = driver.find_element(By.XPATH, '//*[@ng-reflect-name="labelCompanyName"]')
    companyForm.send_keys(company)

    roleForm = driver.find_element(By.XPATH, '//*[@ng-reflect-name="labelRole"]')
    roleForm.send_keys(role)

    addressForm = driver.find_element(By.XPATH, '//*[@ng-reflect-name="labelAddress"]')
    addressForm.send_keys(address)

    emailForm = driver.find_element(By.XPATH, '//*[@ng-reflect-name="labelEmail"]')
    emailForm.send_keys(email)

    phoneForm = driver.find_element(By.XPATH, '//*[@ng-reflect-name="labelPhone"]')
    phoneForm.send_keys(phone)

    submitButton = driver.find_element(By.XPATH, '/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/input')
    submitButton.click()
    #print(f'{name} {surname} {company} {role} {address} {email} {phone}')

message = driver.find_element(By.XPATH, '/html/body/app-root/div[2]/app-rpa1/div/div[2]')
print(message.text)

driver.quit()
