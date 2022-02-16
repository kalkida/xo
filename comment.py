import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

#browser = webdriver.chrome('./chromedriver')


def youtube_login(email, password):
    # Browser
    driver = webdriver.Chrome('./chromedriver')
    driver.set_window_size(1080,1920)
    driver.get('https://accounts.google.com/ServiceLogin?hl=en&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fhl%3Den%26feature%3Dsign_in_button%26app%3Ddesktop%26action_handle_signin%3Dtrue%26next%3D%252F&uilel=3&passive=true&service=youtube#identifier')

    # log in
    driver.find_element(By.CSS_SELECTOR,'input[type=email]').send_keys(email)
    driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()
    waite = WebDriverWait(driver, 30)
    elements = waite.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
    elements.send_keys(password)
    wait = WebDriverWait(driver, 30)
    #driver.find_element(By.CSS_SELECTOR,"button").click()
    element = wait.until(EC.presence_of_element_located((By.ID, "passwordNext")))
    element.click()

    return driver


def comment_page(driver, urls, comment):
    # Check if there still urls
    if len(urls) == 0:
        print('Youtube Comment Bot: Finished!')
        return []

    # Pop a URL from the array
    url = urls.pop()

    # Visite the page
    driver.get(url)
    driver.implicitly_wait(1)

    # Is video avaliable (deleted,private) ?
    if not check_exists_by_xpath(driver, '//*[@id="movie_player"]'):
        return comment_page(driver, urls, random_comment())

    # Scroll, wait for load comment box
    driver.execute_script("window.scrollTo(0, 500);")

    # Comments are disabled?
    if check_exists_by_xpath(driver, '//*[@id="comments-disabled-message"]/div/span'):
        return comment_page(driver, urls, random_comment())

    # Lets wait for comment box
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-comment-simplebox-renderer")))

    # Activate box for comments
    driver.find_element(By.CSS_SELECTOR,"ytd-comment-simplebox-renderer").click()

    # Send comment and post
    driver.implicitly_wait(5)
    wait = WebDriverWait(driver, 30)
    ele = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[id = 'contenteditable-root'")))
    ele.send_keys(comment)
   # wait = WebDriverWait(driver, 30)
    #sending = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ytd-comment-simplebox-renderer')))
    ele.send_keys(Keys.ENTER + Keys.ENTER)

    # Is post ready to be clicked?
    post = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, 'submit-button'))
    )
    post.click()

    # Lets wait a bit
    r = np.random.randint(2, 5)
    time.sleep(r)

    # Recursive
    return comment_page(driver, urls, random_comment())


def random_comment():
    messages = [
        '#No More African people can solve their own conflict by standing together',
        '#No More Donot put your nose in any ones business this is Neo colonialism we say no more',
        '#no more'
    ]

    r = np.random.randint(0, len(messages))

    return messages[r]


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False

    return True


if __name__ == '__main__':
    # Credentials
    email = 'andrewsein123@gmail.com'
    password = 'K@lep@55'

    # List of Urls
    urls = []

    with open('url.txt') as f:
        for line in f:
            inner_list = [elt.strip() for elt in line.split(',')]
            urls_new.append(inner_list)

    # You can add in a file and import from there
    '''
    inp = open ("urls.txt","r")
    for line in inp.readlines():
            urls.append(line.split())
      '''
    # Login in youtube

    driver = youtube_login(email, password)

    # Random comment
    comment_page(driver, urls, random_comment())