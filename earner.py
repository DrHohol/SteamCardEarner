from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

driver = webdriver.Chrome()

mode = "manual"

def read_data():
	account_data = open('accs.txt','r').read().split('\n')
	print(account_data)
	for account in account_data:
		account_login = account.split(':')[0]
		account_pwd = account.split(':')[1]
		if mode == "auto":
			guards = open(account_login + ".txt",'r').read().split(',')
			guard = guards[0]
			guards.remove(guard)
			with open(account_login + ".txt",'w') as guardsfile:
				for i in guards:
					guardsfile.write(i + ',')
			login(account_login,account_pwd,guard)
		else: login(account_login,account_pwd,None)
		

def login(login,password,guard):
	print(login + ' ' + password)
	driver.get("https://steamcommunity.com/login/home/?goto=")
	username = driver.find_element_by_name("username").send_keys(login)
	password_field = driver.find_element_by_name("password").send_keys(password)
	driver.find_element_by_id("SteamLogin").send_keys(Keys.RETURN)
	if mode == "auto":
		driver.implicitly_wait(10)
		driver.find_element_by_id("twofactorcode_entry").send_keys(guard)
		driver.find_element_by_class_name("auth_button leftbtn").click()
	else: pass
	driver.implicitly_wait(10)
	if len(driver.find_elements_by_class_name('persona_name')) > 0:
		driver.get_cookies()
		explore()
	else: exit()

def explore():
	radius = 3
	for i in range(radius):
		driver.get("https://store.steampowered.com/explore")
		try:
			driver.find_element_by_id("discovery_queue_start_link").click()
		except:
			driver.find_element_by_id("refresh_queue_btn").click()
		driver.implicitly_wait(10)
		try:
			for i in range (12):
				driver.find_element_by_class_name('next_in_queue_content').click()
				sleep(1)
		except:
			radius -= 1 
			explore()
read_data()

