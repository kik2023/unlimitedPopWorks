"""
===================================
===================================
AUTO UPDATER FOR CHROME WEB DRIVER
THIS SCRIPT CAN BE USED AS LIBRARY
OR
PACKAGE AS STANDALONE EXECUTABLE
===================================
NOTE:
When using as standalone executable, the script will
automatically search for the webdriver from
"{location of the itself during execution}/webdriver"
===================================
"""
import os
import sys
import shutil
import logging
import requests
import zipfile

from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import SessionNotCreatedException

def updateDriver(webDriverDirectory, osType='win32'):
    """Params: Directory of your webdriver, the OS you using."""
    logging.info(f"Checking if driver is up to date!")
    try:
        webDriverWithPath = f"{webDriverDirectory}chromedriver"
        try:
            driver = webdriver.Chrome(str(webDriverWithPath))
        except FileNotFoundError:
            os.mkdir(webDriverDirectory)
            driver = webdriver.Chrome(str(webDriverWithPath))
        driver.close()
        logging.info("Version check passed!")
        return True
    except SessionNotCreatedException as e:
        errorMessage = str(e)
        if "This version of ChromeDriver only supports Chrome version" in errorMessage:
            logging.info("Starting update for chrome web driver...")
            url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_'
            url_file = 'https://chromedriver.storage.googleapis.com/'
            file_name = f"chromedriver_{osType}.zip"

            logging.info(errorMessage)
            formattedMessage = errorMessage.split('\n')
            currentVersion = formattedMessage[0].split("supports Chrome version")[1].strip()
            browserVersion = formattedMessage[1].split("Current browser version is")[1].split('.', 1)[0].strip()

            version_response = requests.get(url + browserVersion)
            logging.info(f"The latest release for version {browserVersion} is {version_response.text}")
            if version_response.text:
                logging.info("Downloading the latest web driver...")
                file = requests.get(f"{url_file}{version_response.text}/{file_name}")
                if file.status_code == 404:
                    logging.info("Unable to download the driver!")
                    return False
                with open(file_name, "wb") as code:
                    code.write(file.content)
                    logging.info(f"Latest web driver downloaded!")
                downloadedFile = f"chromedriver_{osType}.zip"
                destination = webDriverDirectory
                shutil.move(file_name, destination + file_name)
                try:
                    shutil.move(f"{webDriverWithPath}.exe",f"{webDriverDirectory}Archive/chromedriver_v{currentVersion}.exe")
                    logging.info("Old webdriver is moved to archive and labeled with version number")
                except FileNotFoundError as e:
                    os.mkdir(webDriverDirectory + "Archive")
                    shutil.move(f"{webDriverWithPath,webDriverDirectory}.exe",
                                webDriverDirectory + f"Archive/chromewebdriver{currentVersion}.exe")
                    logging.info("Old webdriver is moved to archive and labeled with version number")

                logging.info("Extracting new driver from the zip file...")
                with zipfile.ZipFile(destination + file_name, 'r') as zip_ref:
                    zip_ref.extractall(destination)
                logging.info("File extracted!")

                logging.info("Verifying web driver after update...")
                try:
                    webDriverWithPath = f"{webDriverDirectory}chromedriver"
                    driver = webdriver.Chrome(str(webDriverWithPath))
                    driver.close()
                    logging.info("Version check passed! Auto update completed!"
                          f" Current driver version: {version_response.text}")
                    return True
                except SessionNotCreatedException:
                    logging.info("Session creation fail after update! Please reach your respective SME to report about this issue!")
                    return False


