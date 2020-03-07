#!/usr/bin/env python
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


driver = webdriver.Firefox()
driver.get('https://services.acm.org/public/chapters/AutoChap/')

elem = driver.find_element_by_name("chapterName")
elem.send_keys("testing")

email = driver.find_element_by_id("Email")
email.send_keys("abc@def.ghi")


el = driver.find_element_by_name('chapter_type')
for option in el.find_elements_by_tag_name('option'):
    if option.text == 'Student':
        option.click() # select() in earlier versions of webdriver
        break

el = driver.find_element_by_name('chapter_sub_type')
for option in el.find_elements_by_tag_name('option'):
    if option.text == 'University':
        option.click() # select() in earlier versions of webdriver
        break

submit = driver.find_element_by_id("submit")
submit.send_keys(Keys.RETURN)

membership_no = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "clientNo")))



membership_no.send_keys("9983515")

retrieve_info = driver.find_element_by_name('submit_form')
retrieve_info.send_keys(Keys.RETURN)

time.sleep(5)

# label = driver.find_element_by_css_selector("label[for='firstName']")
# print(label.text)

firstName = driver.find_element_by_name('firstName')

# first name of the membership id
print(firstName.get_attribute('value'))

# if this line is false, membership is expired
renew_member = driver.find_element_by_link_text('Renew Membership')
print(renew_member is None)

email = driver.find_element_by_name('Email')
print(email.get_attribute('value'))

# membership_no = driver.find_element_by_id("clientNo")
# membership_no.send_keys("9983515")
