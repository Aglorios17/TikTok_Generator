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

# Load the environment variables from the .env file
load_dotenv()
# Access the environment variables
USERNAME = os.getenv("MAIL")
PASSWORD = os.getenv("PASSWORD")
COOKIE_PATH = "e:/aless/AppData/chrome/"

def send_keys(element, data):
    for i in data:
        element.send_keys(i)
        time.sleep(random.uniform(0.1, 0.4))
        
def send_hashtag(element, data):
    element.send_keys(" ")
    time.sleep(random.uniform(0.1, 0.4))
    element.send_keys('|#')
    time.sleep(random.uniform(0.1, 0.4))
    for i in data:
        element.send_keys(i)
        time.sleep(random.uniform(0.1, 0.4))
    time.sleep(1)
    element.send_keys(" ")

def login(driver):
    send_keys(WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email or username']"))), USERNAME)
    time.sleep(1)
    send_keys(WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']"))), PASSWORD)
    time.sleep(1)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))).click()

def televerser(driver, path_video):
    time.sleep(6)
    driver.get("https://www.tiktok.com/creator#/upload?scene=creator_center")
    time.sleep(2)
    print(path_video)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))).send_keys(path_video)

def title_and_hashtag(driver, title, hashtag):
    first_letter = title[0]
    rest_letter = title[1:]
    time.sleep(2)
    br = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//br[@data-text="true"]')))
    time.sleep(1)
    send_keys(br, first_letter)
    time.sleep(1)
    span = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//span[@data-text="true"]')))
    send_keys(span, rest_letter)
    if hashtag:
        list_hashtag = hashtag.split(" ")
        for word in list_hashtag:
            send_hashtag(span, word)

def post_button(driver, basename):
    time.sleep(2)
    print(basename)
    while True:
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//div[@title="{basename}"]')))
            time.sleep(10)
            buttons = driver.find_elements(By.XPATH, '//button')
            if buttons:
                # Find the last button in the list
                last_button = buttons[-1]
                last_button.click()
            break
        except:
            print("video is loading")
            time.sleep(5)
    while True:
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="tiktok-modal__modal-title"]')))
            print("video is uploaded !")
            break
        except:
            print("video is uploading")
            time.sleep(5)

            
            

def uploader(path_video, title, hashtag):
    if os.path.exists("sources/chromedriver.exe"):
        print("driver exist")
    
    # absolut path
    #path_video = os.path.join(os.getcwd(), path_video)
    # Options
    option = webdriver.ChromeOptions()
    option.add_argument("--profile-directory=Default")
    option.add_argument(f"--user-data-dir={COOKIE_PATH}")
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("window-size=1920,1000")
    #optional : option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")
    
    # Initialize the webdriver (replace 'chromedriver' with the path to your WebDriver)
    driver = webdriver.Chrome(options=option)
    #Open a webpage
    driver.get('https://www.tiktok.com/login/phone-or-email/email')
    time.sleep(1)
    # Getting the list of directories
    dir = os.listdir(COOKIE_PATH)
    # Checking if the list is empty or not
    if len(dir) == 0:
        print("try to login")
        login(driver)
    televerser(driver, path_video)
    title_and_hashtag(driver, title, hashtag)
    post_button(driver, os.path.basename(path_video))
    # Close the browser window
    driver.quit()

# video / titre / hashtag
def main():
    uploader(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()
  
