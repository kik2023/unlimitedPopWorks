import os, sys

from selenium import webdriver

if getattr(sys, 'frozen', False):
    path = os.path.dirname(sys.executable)
elif __file__:
    path = os.path.dirname(__file__)

try:
    driver = webdriver.Chrome(f"{path}/webdriver/chromedriver")
    driver.get('https://popcat.click/')
    driver.set_window_size(1280, 720)

    stop = False
    cat = driver.find_element_by_xpath('//*[@id="app"]/div')
    print("Unlimited Pop Jutsu!"
          "Want to spam more? Run more!"
          "To exit, simply close this window")
    while stop is False:
        cat.click()
except Exception:
    print("Please create a folder called 'webdriver' and place it beside your exe, then google for chromedriver and download it, put it inside the folder."
          "Close and restart this application once done")
    input()



