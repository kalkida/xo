from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import csv
import pymongo
import pandas as pd
import os
import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client["youtube"]
Collection =db["youtube_data"]

commenter = []
dataset = []

def get_video_info(url):

    try:
        session = HTMLSession()
        response = session.get(url)
        # execute Javascript
        response.html.render(sleep=2)
        # create beautiful soup object to parse HTML
        soup = bs(response.html.html, "html.parser")
        soup.find_all("meta")
        # open("index.html", "w").write(response.html.html)
        # initialize the result
        result = {}
        results ={}
        result['url'] = url
        result['title'] = soup.find("meta", itemprop="name")['content']
        result['views'] = soup.find("meta", itemprop="interactionCount")['content']
        results= soup.find_all("meta")
        text_yt_formatted_strings = soup.find_all("yt-formatted-string",
                                                  {"id": "text", "class": "ytd-toggle-button-renderer"})
        result['likes'] =''.join([c for c in text_yt_formatted_strings[0].attrs.get("aria-label") if c.isdigit()])
        #result["\'likes\'"] = 0 if result['likes'] == '' else int(result['likes'])
        channel_tag = soup.find("yt-formatted-string", {"class": "ytd-channel-name"}).find("a")
        # channel name
        channel_name = channel_tag.text
        # channel URL
        channel_url = f"https://www.youtube.com{channel_tag['href']}"
        # number of subscribers as str
        channel_subscribers = soup.find("yt-formatted-string", {"id": "owner-sub-count"}).text.strip()
        result['channel'] = {'channel_name': channel_name, 'channel_url':  channel_url, 'subscribers': channel_subscribers}
        result['comments'] = commenter
        with open("textbooks.json", "w") as writeJSON:
            json.dump(result, writeJSON, ensure_ascii=False)
        return result

    except:
        print("Invalid link")



def comment(url):
    try:
        driver = webdriver.Chrome('./chromedriver')
        driver.get(url)
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
    print(commenter)
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
    # with open("textbooks.json", "w") as writeJSON:
    #     json.dump(, writeJSON, ensure_ascii=False)

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
        get_video_info(urls)
        print(get_video_info(urls))
        comment(urls)
        
     with open('textbooks.json') as f:
        file_data = json.load(f)
        
     collection.insert_many(file_data)
     client.close()





    # request_url = 'http://127.0.0.1:3000/posts'
    # r = requests.request("POST", request_url, data=get_video_info(url))




