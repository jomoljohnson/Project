# Test 1: Login test

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
chrome_driver_path = 'c:\\Users\\jomol\\OneDrive\\Desktop\\project\\chromedriver.exe'

class LoginformTest(LiveServerTestCase):

    def testloginpage(self):
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/login/')
        time.sleep(5)
        username_input = driver.find_element(By.NAME, 'email')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
        username_input.send_keys('jomolmariya432@gmail.com')
        password_input.send_keys('Jomol@123')
        login_button.send_keys(Keys.RETURN)

        assert 'Job Card Application' in driver.page_source