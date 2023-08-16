import sys
import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from tkinter import Tk, filedialog
from webdriver_manager.chrome import ChromeDriverManager


from flask import  send_file

option=sys.argv[2]
# specify the URL of the web page
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = input("Enter the URL: ")

# specify the path of the ChromeDriver executable
chrome_driver_path = "/path/to/chromedriver"

# create a new Chrome driver service
service = Service(chrome_driver_path)

# create a new Chrome driver service
service = Service(ChromeDriverManager().install())

# create a new Chrome browser instance
download_dir = '.'

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    'plugins.always_open_pdf_externally': True,
    'download.default_directory': download_dir,
    'download.prompt_for_download': True,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
})
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=service, options=options)
# navigate to the web page
driver.get(url)
# ask the user to select the CSV file
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
root.destroy()
# read the student details from the CSV file
with open(file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    total_steps = sum(1 for row in reader) # count the number of students
    csvfile.seek(0) # reset the file cursor to the beginning
    next(reader) # skip the header row
    for i, row in enumerate(reader):
        if option == "pg":
            reg_num = row['regno']
            dob = row['dob']
            # Enter the register number and DOB
            reg_num_field = driver.find_element(By.NAME, 'regno')
            dob_field = driver.find_element(By.NAME, 'dob')
            reg_num_field.clear()
            dob_field.clear()
            reg_num_field.send_keys(reg_num)
            dob_field.send_keys(dob)
        elif option=="ug":
            reg_num = row['regno']
            dob = row['aadhaar']
            # Enter the register number and DOB
            reg_num_field = driver.find_element(By.NAME, 'regno')
            dob_field = driver.find_element(By.NAME, 'aadhaar')
            reg_num_field.clear()
            dob_field.clear()
            reg_num_field.send_keys(reg_num)
            dob_field.send_keys(dob)
        # submit the web form
        submit_button = driver.find_element(By.XPATH, "//input[@value='SUBMIT']")
        submit_button.click()

        try:
            # wait for the download button to appear and click on it
            download_button = WebDriverWait(driver, 0.1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="Download"]'))
            )
            download_button.click()

        except TimeoutException:
            os.rename("file.pdf", f"{reg_num}.pdf")
            #progress_bar(i+1, total_steps)

        finally:
            # go back to the previous page
            driver.back()

            # close the current browser window
            driver.close()

                        # reopen the browser for the next student
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(url)
print('Downloaded')
# close the final browser
driver.quit()
