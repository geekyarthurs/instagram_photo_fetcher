import bs4
from time import sleep
import sys, os
import requests
import random, string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

if len(sys.argv) != 2:
    print("Please pass the username of the user.")
    exit()

url = "https://www.instagram.com/{}/".format(sys.argv[1])

username = input("Enter your username or email or phone number: ")
password = input("Enter Password: ")

#Getting Page Source 
try:
    browser = webdriver.Firefox()
except:
    print("Please install Firefox to proceed.")



browser.get("https://www.instagram.com/accounts/login/")
sleep(1)
print("Entering Username..")
usernameInput = browser.find_element_by_name("username")
usernameInput.send_keys(username)
sleep(1)
print("Entering Password..")
passwordInput = browser.find_element_by_name("password")
passwordInput.send_keys(password)
sleep(1)
print("Submitting the form..")
submitButton = browser.find_element_by_css_selector("button[type=submit]")
submitButton.click()
sleep(1)

print("Logged In")


browser.get(url)
sleep(1)
SCROLL_PAUSE_TIME = 1

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


html = browser.page_source
browser.quit()

#Webscraping for images src and alt attribute.
soup = bs4.BeautifulSoup(html, 'lxml')
images = soup.find_all('img')
username  = soup.select("h1")[0].text.strip()
full_name = soup.select("h1")[1].text.strip()
print("Full Name: {} \nUsername: {}".format(full_name,username) )
imageUrls = []
for image in images:
    fileUrl = image['src']
    imageUrls.append((username + randomString(10),fileUrl))

print("Image Found: {}".format(len(imageUrls)))
#downloading the photos. 
for index,url in enumerate(imageUrls):
    print("Downloading : {}".format(index + 1))
    # url = (alt, src)
    if not os.path.exists('images'):
        print("Making directory images.")
        os.makedirs('images')
    fileName = "images/{}.jpg".format(url[0]) 
    fileUrl = url[1] #src
    req = requests.get(fileUrl)
    file = open(fileName, 'wb') 
    for chunk in req.iter_content(100000):
        file.write(chunk)
    file.close()
