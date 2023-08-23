import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time 
import sys
import os
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import glob
from datetime import datetime, timedelta
import string
from tiktok_uploader import send_keys

COOKIE_PATH = "e:/aless/AppData/chrome/"

def generate_password(length):
    # Define character sets for letters, numbers, and special characters
    letters = string.ascii_letters
    digits = string.digits
    special_characters = "!@#$&?"

    # Ensure at least one character from each set is included
    password = random.choice(letters) + random.choice(digits) + random.choice(special_characters)
    # Fill the remaining characters with a random selection from all character sets
    all_characters = letters + digits + special_characters
    remaining_length = length - 3  # Subtract 3 for the characters already chosen
    password += ''.join(random.choice(all_characters) for _ in range(remaining_length))

    # Shuffle the password to randomize the character order
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)
    return password

def random_date():
    # Get the current date
    current_date = datetime.now()

    # Calculate the maximum and minimum birth dates
    min_birth_date = current_date - timedelta(days=365 * 40)  # 100 years ago
    max_birth_date = current_date - timedelta(days=365 * 21)   # 21 years ago

    # Generate a random birth date within the specified range
    random_birth_date = min_birth_date + timedelta(days=random.randint(0, (max_birth_date - min_birth_date).days))

    # Store the components in a table-like format
    return [random_birth_date.month, random_birth_date.day, random_birth_date.year]    

def create_credentials():
    date = random_date()
    mail = "test@gmail.com"
    password = generate_password(random.randint(14, 19))
    return (date, mail, password)

def input_date(driver, string, date):
    time.sleep(random.uniform(0.1, 0.5))
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//div[@aria-label='{string}. Double-tap for more options']"))).click()
    time.sleep(random.uniform(0.1, 0.5))
    if string == "Year":
        date = (datetime.now().year) - date
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//div[@id='{string}-options-item-{date - 1}']")))
    time.sleep(random.uniform(0.1, 0.5))
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(random.uniform(0.1, 0.5))
    element.click()

def retreive_code(driver):
    button = driver.find_elements(By.XPATH, '//button')
    time.sleep(1)
    button[-2].click()
    code = "123456"
    send_keys(WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter 6-digit code']"))), code)
    time.sleep(random.uniform(0.1, 0.5))

def input_data(driver, date, mail, password):
    # select month
    input_date(driver, "Month", date[0])
    # select day
    input_date(driver, "Day", date[1])
    # select year
    input_date(driver, "Year", date[2])
    # input mail
    send_keys(WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email address']"))), mail)
    # input password
    send_keys(WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']"))), password)
    # send code
    retreive_code(driver)
    # Next button
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))).click()

def new_account():
    # Set True if you have any saved cookies
    auto_login = False
    option = webdriver.ChromeOptions()
    #option.add_argument("--headless")
    option.add_argument("--disable-gpu")
    option.add_argument("--profile-directory=Default")
    option.add_argument("--ignore-certificate-errors")
    option.add_argument("--log-level=3")
    #option.add_argument(f"--user-data-dir={COOKIE_PATH}")
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("window-size=1920,1400")
    #optional : option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")
    
    # Initialize the webdriver (replace 'chromedriver' with the path to your WebDriver)
    driver = webdriver.Chrome(options=option)
    #Open a webpage
    driver.get('https://www.tiktok.com/signup/phone-or-email/email')
    time.sleep(1)
    date, mail, password = create_credentials()
    print(f'date : {date} | mail : {mail} | password : {password}')
    input_data(driver, date, mail, password)
    # Close the browser window
    time.sleep(15)
    driver.quit()

def main():
    new_account()

if __name__ == "__main__":
    main()