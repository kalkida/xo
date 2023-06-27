from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
import chromedriver_autoinstaller
import asyncio
import youtube_dl
from selenium.webdriver.common.keys import Keys
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import csv
import pymongo
import pandas as pd
import os
import json
import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.scheduler import Scheduler
from pymongo import MongoClient

chromedriver_autoinstaller.install()

client = MongoClient('localhost', 27017)
db = client["youtube-data"]
Collection =db["youtube"]

commenter = []
dataset = []

def get_video_info(url):

    driver = webdriver.Chrome()  # Replace with appropriate webdriver (e.g., Firefox, Edge, etc.)
    driver.get(url)

    try:
        # session = HTMLSession()
        # response = session.get(url)
        # # execute Javascript
        # response.html.render(sleep=2)
        # # create beautiful soup object to parse HTML
        # soup = bs(response.html, "html.parser")
        # soup.find_all("meta")
        # open("index.html", "w").write(response.html.html)
        # initialize the result
        result = {}
        results ={}
        result['url'] = url
        # result['title'] = soup.find("meta", itemprop="name")['content']
        # result['views'] = soup.find("meta", itemprop="interactionCount")['content']
        # results= soup.find_all("meta")
        # text_yt_formatted_strings = soup.find_all("yt-formatted-string",
        #                                           {"id": "text", "class": "ytd-toggle-button-renderer"})
        # result['likes'] =''.join([c for c in text_yt_formatted_strings[0].attrs.get("aria-label") if c.isdigit()])
        # #result["\'likes\'"] = 0 if result['likes'] == '' else int(result['likes'])
        # channel_tag = soup.find("yt-formatted-string", {"class": "ytd-channel-name"}).find("a")
        # channel name
        # channel_name = channel_tag.text
        # # channel URL
        # channel_url = f"https://www.youtube.com{channel_tag['href']}"
        # # number of subscribers as str
        # channel_subscribers = soup.find("yt-formatted-string", {"id": "owner-sub-count"}).text.strip()
        
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        
        # Extract video information
        video_title = driver.find_element(By.TAG_NAME, "h1").text
        video_duration = driver.find_element(By.CSS_SELECTOR, ".ytp-time-duration").text
        # video_views = driver.find_element(By.CSS_SELECTOR, ".view-count").text
        video_likes = driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/div[1]/ytd-segmented-like-dislike-button-renderer/yt-smartimation/div/div[1]/ytd-toggle-button-renderer/yt-button-shape/button").text
        channel_name = driver.find_element(By.CSS_SELECTOR, "#text > a").text
        channel_subscribers = driver.find_element(By.CSS_SELECTOR, "#owner-sub-count").text
        channel_url = driver.find_element(By.CSS_SELECTOR, "#text > a").get_attribute("href")

        result["title"]= video_title
        result["duration"]=video_duration
        result["duration_seconds"]=video_duration
        # result["Views"]=video_views
        result["likes"]=video_likes

        print("Video Title:", video_title)
        print("Duration:", video_duration)
        # print("Views:", video_views)

        result['channel'] = {'channel_name': channel_name, 'channel_url':  channel_url, 'subscribers': channel_subscribers}
        result['comments'] = commenter
        with open("textbooks.json", "w+") as writeJSON:
            json.dump(result, writeJSON, ensure_ascii=False)
        return result
        

    except Exception as EE:
        print("An error occurred:", str(EE))

        print(EE)
        print("Invalid link")



def comment(url):
    try:
        #service_object = Service('/usr/local/share/chromedriver')
        #driver = webdriver.Chrome(service=service_object)
        driver = webdriver.Chrome()
        driver.get(url)
        driver.manage().timeouts().implicitlyWait(60, SCROLL_PAUSE_TIME)

    except:
        print("didn't open a chrome tab")

    SCROLL_PAUSE_TIME = 2
    CYCLES = 100

    time.sleep(5)
    html = driver.find_elements(By.TAG_NAME,'html')

    html[0].send_keys(Keys.PAGE_DOWN)
    html[0].send_keys(Keys.PAGE_DOWN)
    time.sleep(SCROLL_PAUSE_TIME * 3)
    for i in range(CYCLES):
        html[0].send_keys(Keys.END)
        time.sleep(SCROLL_PAUSE_TIME)

    comments= driver.find_elements(By.XPATH,'//*[@id="content-text"]')

    name = driver.find_elements(By.XPATH,'//*[@id="author-text"]')
    links = [elem.get_attribute('href') for elem in name]
    time.sleep(10)
    print("second")

    common=("comments")

    # with open("textbooks.json", "a") as writeJSON:
    #     writeJSON.seek(0)
    #     json.dump(common, writeJSON, ensure_ascii=False)
    number_of_items= len(name)

    # print("comments" + ":" + "[")
    for i in range(number_of_items):
        commenter.append({"comment_id": links[i], "comment_name": name[i].text, "comment": comments[i].text})
        # print("{")
        # print("\"comment_id\""+":"+"\""+links[i]+"\""+",")
        # print("\"comment_name\""+":"+"\""+name[i].text+"\""+",")
        # print("\"comment\""+":"+"\""+comments[i].text+"\"")
        # print("},")
    # print(commenter)
    with open("textbooks.json", 'r+',) as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["comments"].append(commenter)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)
    # with open("textbooks.json", "a", encoding="utf-8") as writeJSON:
    #     writeJSON.seek(0)
    #     json.dump(commenter, writeJSON, ensure_ascii=False)

    # print("]")
        # with open("textbooks.json", "w+") as writeJSON:
        #     json.dump(commenter, writeJSON, ensure_ascii=False)

    driver.quit()

if __name__ =="__main__":

    # with open('textbooks.json') as file:
    #     file_data = json.load(file)
    #
    # db.Collection.insert_one(file_data)
    lines = []
    with open('url.txt') as f:
        for line in f:
            inner_list = [elt.strip() for elt in line.split(',')]
            lines.append(inner_list)
        print(lines[0])
        urls = lines[0].pop()
        print(urls)
        
        # get_video_info(urls)
        # comment(urls)
        # print(get_video_info(urls))
        # comment(urls)
    async def first_function():
    # Perform tasks for the first function
        await asyncio.sleep(1)
        get_video_info(urls)
        print("First function completed")
    async def second_function():
    # Perform tasks for the second function
        await asyncio.sleep(2)
        comment(urls)
        print("Second function completed")

    async def main():
    # Call the first function and wait for its completion
        await first_function()

    # Call the second function after the first function has completed
        await second_function()

# Running the event loop
    asyncio.run(main())

    with open('textbooks.json') as f:
        file_data = json.load(f)
        
    Collection.insert_one(file_data)
    client.close()

    sched = BackgroundScheduler(standalone=True , coalesce = True)
    sched.add_cron_job(main(), 'interval', minutes=360)
    sched.start()
        
 
 





    # request_url = 'http://127.0.0.1:3000/posts'
    # r = requests.request("POST", request_url, data=get_video_info(url))




