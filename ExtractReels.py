from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import requests
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Update this section with details for login 
# Download Chrome driver, 
username = ""
password = ""
account_id = "_.theukiyostore" # username for business account 
section = "reels" # reels to download videos, posts for posts sections
PATH = r"chromedriver.exe"


driver = webdriver.Chrome(executable_path=PATH)
driver.get("https://www.instagram.com/")

# login
time.sleep(5)
try:
	elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
finally:
	account_id = driver.find_element(By.CSS_SELECTOR( "input[name='username']"))
	password = driver.find_element(By.CSS_SELECTOR( "input[name='password']"))

account_id.clear()
password.clear()

account_id.send_keys(username)
password.send_keys(password)
login = driver.find_element(By.CSS_SELECTOR( "button[type='submit']")).click()

# save your login info deny
# todo: wait for login page to finish loading by waiting for an element on the page - this should be done for every section where we are adding time.sleep()
# note: time.sleep added so page can load properly before actions are triggered. 
time.sleep(10)
login_dont_save = driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
# turn on notifications deny
time.sleep(10)
notifications_turn_off = driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()


driver.get("https://www.instagram.com/" + account_id + "/" + section)
time.sleep(10)

# scroll
scroll_down = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
match = False
while (match == False):
    last_count = scroll_down
    time.sleep(3)
    scroll_down = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    if last_count == scroll_down:
        match = True

# posts
posts = []
links = driver.find_elements_by_tag_name('a')
for link in links:
    post = link.get_attribute('href')
    if '/p/' in post or 'reel' in post:
      posts.append(post)

print(posts)
post_df = pd.DataFrame(posts)
post_df.to_csv("Data1.csv")

dataset = []
# get videos and images
download_url = ''
for post in posts:
	driver.get(post)
	short_code = driver.current_url.split("/")[-2]
	time.sleep(7)
		
	if(section == "reels"):
		# todo: get links to the urls for reels 
		# download_url = driver.find_element(By.TAG_NAME("video")).get_attribute('src')
		# urllib.request.urlretrieve(download_url, '{}.mp4'.format(short_code))
		 # Get the URL of the video
		download_url = driver.find_element(By.TAG_NAME, "video").get_attribute('src')
        # Get the caption
        caption_elem = driver.find_element(By.CSS_SELECTOR, "div.C4VMK > span")
        caption = caption_elem.text if caption_elem else ""
        urllib.request.urlretrieve(download_url, '{}.mp4'.format(short_code))
    
	else:
		caption = ""
		if driver.find_element(By.CSS_SELECTOR( "img[style='object-fit: cover;']")) is not None:
			download_url = driver.find_element(By.CSS_SELECTOR( 
				"img[style='object-fit: cover;']")).get_attribute('src')
			urllib.request.urlretrieve(download_url, '{}.jpg'.format(short_code))
		else:
			download_url = driver.find_element(By.CSS_SELECTOR( 
				"video[type='video/mp4']")).get_attribute('src')
			urllib.request.urlretrieve(download_url, '{}.mp4'.format(short_code))
		
	details = {}
	details["url"] = driver.current_url
	details["short_code"] = short_code
	details["description"] = driver.find_elements(By.TAG_NAME("header"))[1] 
	details["pinned_comment"] = driver.find_elements(By.TAG_NAME("h1"))[1]
	details["caption"] = caption
	print(details)
	dataset.append(details)
	time.sleep(5)
print(dataset)    