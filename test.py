# # Test 1: Login test

# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By

# class LoginformTest(LiveServerTestCase):

#     def testloginpage(self):
#         driver = webdriver.Chrome()

#         driver.get('http://127.0.0.1:8000/login.html')
#         time.sleep(5)
#         username_input = driver.find_element(By.NAME, 'email')
#         password_input = driver.find_element(By.NAME, 'password')
#         login_button = driver.find_element(By.NAME, 'submit')
#         username_input.send_keys('jomolmariya432@gmail.com')
#         password_input.send_keys('Jomol@123')
#         login_button.send_keys(Keys.RETURN)

#         assert 'Job Card Application' in driver.page_source

# # #TEST 2: Working day selection
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select

# class WorkingDayTest(LiveServerTestCase):

#     def setUp(self):
#         self.username = 'jomolmariya432@gmail.com'
#         self.password = 'Jomol@123'

#         self.driver = webdriver.Chrome()

#     def tearDown(self):
#         self.driver.quit()

#     def login(self):
#         self.driver.get('http://127.0.0.1:8000/login.html')
#         time.sleep(3)
#         username_input = self.driver.find_element(By.NAME, 'email')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.NAME, 'submit')
#         username_input.send_keys(self.username)
#         password_input.send_keys(self.password)
#         login_button.send_keys(Keys.RETURN)
#         time.sleep(3)  

#     def test_working_day(self):
#         # Step 1: Login
#         self.login()

#         # Step 2: Navigate to the patient dashboard
#         self.driver.get('http://127.0.0.1:8000/dashuser')
#         time.sleep(3)  

#         # Step 3: Click on "View Doctors" link/button
#         view = self.driver.find_element(By.LINK_TEXT, 'Working Days Selection')
#         view.click()
#         time.sleep(3)  


#        # Step 5: Select slot from the dropdown
#         select = Select(self.driver.find_element(By.NAME, 'job_id'))
#         select.select_by_index(2)  
#         time.sleep(3)

#         date_input = self.driver.find_element(By.ID, 'start_date')
#         date_input.clear()  
#         date_input.send_keys('13-04-2024')
#         time.sleep(3)

#         date_input = self.driver.find_element(By.ID, 'end_date')
#         date_input.clear()  
#         date_input.send_keys('15-04-2024')
#         time.sleep(3)

#         # Step 6: Click on "Proceed" button
#         proceed_button = self.driver.find_element(By.XPATH, '//button[@type="submit" and text()="Submit"]')
#         proceed_button.click()
#         time.sleep(3)
#         # Step 7: Verify if "Proceed" button is present on the booking page
#         proceed_button = self.driver.find_element(By.LINK_TEXT, 'View Working Days')
#         self.assertIsNotNone(proceed_button)



# #TEST 3: Accept Job
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select

# class AcceptJobTest(LiveServerTestCase):

#     def setUp(self):
#         self.username = 'jomonjohnson@gmail.com'
#         self.password = 'Jomon@123'

#         self.driver = webdriver.Chrome()

#     def tearDown(self):
#         self.driver.quit()

#     def login(self):
#         self.driver.get('http://127.0.0.1:8000/login.html')
#         time.sleep(3)
#         username_input = self.driver.find_element(By.NAME, 'email')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.NAME, 'submit')
#         username_input.send_keys(self.username)
#         password_input.send_keys(self.password)
#         login_button.send_keys(Keys.RETURN)
#         time.sleep(3)  

#     def test_working_day(self):
#         # Step 1: Login
#         self.login()

#         # Step 2: Navigate to the patient dashboard
#         self.driver.get('http://127.0.0.1:8000/dashworker')
#         time.sleep(3)  

#         # Step 3: Click on "View jobs" link/button
#         view = self.driver.find_element(By.LINK_TEXT, 'Jobs')
#         view.click()
#         time.sleep(3)  

#         # Step 7: Verify if "Proceed" button is present on the booking page
#         proceed_button = self.driver.find_element(By.XPATH, '//button[@type="submit" and text()="Accept"]')
#         proceed_button.click()
#         time.sleep(3)

#         button = self.driver.find_element(By.LINK_TEXT, 'Accepted Jobs')
#         self.assertIsNotNone(button)



# #Test4: User Job mentor
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select

# class UserJobTest(LiveServerTestCase):

#     def setUp(self):
#         self.username = 'panchayath01@gmail.com'
#         self.password = 'Panchayath@123'

#         self.driver = webdriver.Chrome()

#     def tearDown(self):
#         self.driver.quit()

#     def login(self):
#         self.driver.get('http://127.0.0.1:8000/login.html')
#         time.sleep(3)
#         username_input = self.driver.find_element(By.NAME, 'email')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.NAME, 'submit')
#         username_input.send_keys(self.username)
#         password_input.send_keys(self.password)
#         login_button.send_keys(Keys.RETURN)
#         time.sleep(3)  

#     def test_doctor_booking(self):
#         # Step 1: Login
#         self.login()

#         # Step 2: Navigate to the patient dashboard
#         self.driver.get('http://127.0.0.1:8000/admindashboard')
#         time.sleep(3)  

#         # Step 3: Click on "View Doctors" link/button
#         view_doctors_button = self.driver.find_element(By.LINK_TEXT, 'User Jobs')
#         view_doctors_button.click()
#         time.sleep(3)  


#         # Step 6: Click on "Proceed" button
#         proceed_button = self.driver.find_element(By.XPATH, '//button[@type="submit" and text()="Reject"]')
#         proceed_button.click()
#         time.sleep(3)
#         # Step 7: Verify if "Proceed" button is present on the booking page
#         proceed_button = self.driver.find_element(By.LINK_TEXT, 'User Jobs')
#         self.assertIsNotNone(proceed_button)

#Test 5:job approval
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class JobApprovalTest(LiveServerTestCase):

    def setUp(self):
        self.username = 'panchayath01@gmail.com'
        self.password = 'Panchayath@123'

        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def login(self):
        self.driver.get('http://127.0.0.1:8000/login.html')
        time.sleep(3)
        username_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.NAME, 'submit')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button.send_keys(Keys.RETURN)
        time.sleep(3)  

    def test_doctor_booking(self):
        # Step 1: Login
        self.login()

        # Step 2: Navigate to the patient dashboard
        self.driver.get('http://127.0.0.1:8000/admindashboard')
        time.sleep(3)  

        # Step 3: Click on "View Doctors" link/button
        view_doctors_button = self.driver.find_element(By.LINK_TEXT, 'view User job Card')
        view_doctors_button.click()
        time.sleep(3)  


        # Step 6: Click on "Proceed" button
        proceed_button = self.driver.find_element(By.XPATH, '//button[@type="submit" and text()="Approve"]')
        proceed_button.click()
        time.sleep(5)
        # Step 7: Verify if "Proceed" button is present on the booking page
        proceed_button = self.driver.find_element(By.LINK_TEXT, 'view User job Card')
        self.assertIsNotNone(proceed_button)
