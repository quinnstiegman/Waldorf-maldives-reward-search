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
import sys


route_code = sys.argv[1]
days_list = [330,331]
# Set up WebDriver (replace with the path to your driver executable)
driver = Driver(uc=True,headless=True, disable_gpu=True)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})

# Set up the CSV file
csv_file_path = 'scrape_results.csv'
csv_headers = ['Date', 'Route','Price', 'Timestamp']

for days in days_list:
    future_date = datetime.now() + timedelta(days=days)
    formatted_date = future_date.strftime('%Y-%m-%d')
    print(datetime.now())
    print(formatted_date)
    if route_code == '1':
        try:
            with open(csv_file_path, mode='a', newline='') as file:
                csv_writer = csv.writer(file)
                if os.stat(csv_file_path).st_size == 0:
                    csv_writer.writerow(csv_headers)
                print('PPT --> LAX')
                route = 'PPT --> LAX'
                print('-------------------------------')
                # Define the target URL, gift card number, and list of PIN numbers
                url = f"https://www.alaskaair.com/search/results?A=1&O=PPT&D=LA5&OD={formatted_date}&OT=Anytime&RT=false&UPG=none&ShoppingMethod=onlineaward&awardType=MilesOnly"  # Replace with the actual URL

                # Navigate to the original page for each PIN attempt
                driver.get(url)

                # Wait for the element to be present
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='valuetile-0-2']"))
                )
                csv_writer.writerow([formatted_date, route, element.text, datetime.now()])
                print(element.text)

        except:
            print('Day not availiable yet')

    if route_code == '2':
        try:
            with open(csv_file_path, mode='a', newline='') as file:
                csv_writer = csv.writer(file)
                if os.stat(csv_file_path).st_size == 0:
                    csv_writer.writerow(csv_headers)
                print('')
                print('LAX --> PPT')
                route = 'LAX --> PPT'
                print('-------------------------------')
                # Define the target URL, gift card number, and list of PIN numbers
                url = f"https://www.alaskaair.com/search/results?A=1&O=LA5&D=PPT&OD={formatted_date}&OT=Anytime&RT=false&UPG=none&ShoppingMethod=onlineaward&awardType=MilesOnly"  # Replace with the actual URL

                # Navigate to the original page for each PIN attempt
                driver.get(url)

                # Wait for the element to be present
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='valuetile-0-2']"))
                )
                csv_writer.writerow([formatted_date, route, element.text, datetime.now()])
                print(element.text)
        except:
            print('Day not availiable yet')





