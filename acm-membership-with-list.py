#!/usr/bin/env python
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


driver = webdriver.Firefox()

f = open("demofile.txt", "r")
o_f = open("output.txt", "w")

for membership_number_from_file in f:
	print(membership_number_from_file)
	if membership_number_from_file == "":
		break


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

	o_f.write("membership_no = " + membership_number_from_file[:-1] + "\t")	
	time.sleep(10)
	membership_no = driver.find_element_by_id("clientNo")
	membership_no.send_keys(membership_number_from_file)

	retrieve_info = driver.find_element_by_name('submit_form')
	retrieve_info.send_keys(Keys.RETURN)

	time.sleep(5)

	# label = driver.find_element_by_css_selector("label[for='firstName']")
	# print(label.text)

	# first name of the membership id
	firstName = driver.find_element_by_name('firstName')
	print(firstName.get_attribute('value'))
	o_f.write("first name = " + firstName.get_attribute('value') + "\t")

	email = driver.find_element_by_name('Email')
	print(email.get_attribute('value'))
	o_f.write("email = " + email.get_attribute('value') + "\t")


	try:
		# if this line is True, membership is expired
		renew_member = driver.find_element_by_link_text('Renew Membership')
		print(renew_member is not None)
		o_f.write("membership expired = " + str(renew_member is not None) + "\n")
	except NoSuchElementException:
		print(False)
		o_f.write("membership expired = " + str(False) + "\n")

	driver.refresh()
	# membership_no = driver.find_element_by_id("clientNo")
	# membership_no.send_keys("9983515")
f.close()
o_f.close()