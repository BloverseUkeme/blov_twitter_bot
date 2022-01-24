# from pymongo import MongoClient
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from time import sleep
# from selenium.webdriver.chrome.options import Options

# options=Options()
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--disable-gpu')

# from ordered_set import OrderedSet



# def open_browser(topic_url):
#     """
#         This starts the chrome browser and opens the url
#     """
#     ## windows
#     PATH = 'C://Users/hp/Desktop/Chrome Driver/chromedriver.exe'

#     ## linux
# #     PATH = "/usr/lib/chromium-browser/chromedriver"

#     try:
#         driver = webdriver.Chrome(PATH, options=options)
# #         driver.maximize_window()
#         sleep(2)

#         driver.get(topic_url)
#         sleep(5)
#     except Exception as e:
#         print(e)

#     return driver


# def scroll_down_twitter(driver):
#     """
#         This implements an infinite scroll on twitter and stops at the end of the page
#     """
#     # Get scroll height

#     try:
#         driver.execute_script("window.scrollTo(0, 0);")
#         sleep(4)
#         last_height = driver.execute_script("return document.body.scrollHeight")

#         new_height = 10

#         tweet_urls = []
        
#         while True:

#             driver.execute_script(f"window.scrollTo(0, {new_height});")
#             sleep(5)
            
#             tag_sections = driver.find_elements_by_tag_name("a")

#             tags = [item.get_attribute('href') for item in tag_sections]
#             ids = [item for item in tags if "status" in item and ("photo" not in item) and ("retweets" not in item) and ('likes' not in item) and ("dhaboy01") in item]
#             sleep(3)
            
#             tweet_urls.append(ids)
            

#             # Calculate new scroll height and compare with last scroll height
#             new_height = driver.execute_script(f"return {new_height+1000}")
#             print(new_height)
#             if new_height > last_height:
#                 break
#     except Exception as e:
#         print(e)
        
#     return tweet_urls


# def format_tweet_data(tweet_urls):
#     """
#         This splits a list of list into a single ordered list 
#     """
#     try:
#         tweet_urls = [a for b in tweet_urls for a in b]
#         tweet_urls = list(OrderedSet(tweet_urls))
#     except Exception as e:
#         print(e)
#     return  tweet_urls


# def start_selenium_process(tweet_url):
#     driver = open_browser(tweet_url)
#     tweet_urls = scroll_down_twitter(driver)
#     tweet_urls = format_tweet_data(tweet_urls)
    
#     return tweet_urls