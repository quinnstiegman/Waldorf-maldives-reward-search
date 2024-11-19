import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
import pandas as pd
import os
from seleniumbase import Driver

# Set up WebDriver (replace with the path to your driver executable)
driver = Driver(uc=True, headless=True, disable_gpu=True)

try:
    # Define the target URL, gift card number, and list of PIN numbers
    url = "https://www.alaskaair.com/search/results?A=1&O=PPT&D=LA5&OD=2025-10-15&OT=Anytime&RT=false&UPG=none&ShoppingMethod=onlineaward&awardType=MilesOnly"  # Replace with the actual URL

    # Navigate to the original page for each PIN attempt
    driver.get(url)

    # Wait for the element to be present
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "valuetile partner-business"))
    )
    print(element.text)

finally:
    # Close the WebDriver
    driver.quit()
