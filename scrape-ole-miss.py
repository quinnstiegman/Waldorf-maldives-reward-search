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

TARGET_ARRIVAL = '2025-09-10'
TARGET_DEPARTURE = '2025-09-11'

# Function to wait for the presence of either price or rate_not_available element
def wait_for_elements(driver):
    try:
        WebDriverWait(driver, 30).until(
            EC.any_of(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, '[data-testid="flexDatesRoomRate"]'), ','),
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="rateNotAvailable"]')),     
            )
        )

    except TimeoutException:
        print("Neither element appeared within 30 seconds. Moving on.")

# Function to get the price for a specific date
def get_price_for_date(date):
    # Filter the DataFrame for the specific date
    filtered_data = data[data['date'] == date]
    
    # Check if the date exists in the DataFrame
    if not filtered_data.empty:
        # Retrieve the price for the date
        price = filtered_data['price'].values[0]
        return price, filtered_data
    else:
        return None



# grab env vars
api_token = os.environ.get("API_KEY")
user_key = os.environ.get("USER_KEY")
# Set up a headless Chrome browser
# options = uc.ChromeOptions()
# options.add_argument('--disable-gpu')
# options.add_argument("--disable-extensions")
# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
# options.add_argument(f'user-agent={user_agent}')
driver = Driver(uc=True, headless=True, disable_gpu=True)
# options.add_argument('--headless')
# driver = uc.Chrome(options=options, version_main=122)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})
# Save the results to a CSV file
previous_prices = {}
csv_file_path = 'output_results.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['date', 'price', 'timestamp', 'hotel_name'])
    # Create the complete URL
    url1 = f'https://www.hilton.com/en/book/reservation/flexibledates/?ctyhocn=TUPGOGU&arrivalDate={TARGET_ARRIVAL}&departureDate={TARGET_DEPARTURE}&redeemPts=true&room1NumAdults=1&displayCurrency=USD'
    hotel_name = "Graduate Oxford"
    driver.get(url1)
    
        # Wait for either element to be present
    wait_for_elements(driver)

    # Get the updated page source after JavaScript execution
    page_source = driver.page_source

    # Use Beautiful Soup to parse the HTML
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all elements with the specified data-testid
    date_and_price_elements = soup.find_all('button', attrs={"data-testid": True})

    # Extract and write the date and price information
    for element in date_and_price_elements:
        date = element['data-testid'].replace('arrival-', '')  # Extract date from data-testid attribute
        price_element = element.find(attrs={"data-testid": "flexDatesRoomRate"})
        rate_not_available_element = element.find(attrs={"data-testid": "rateNotAvailable"})

        # # Check if the price element exists
        if price_element:
            price = price_element.text.strip()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            csv_writer.writerow([date, price, timestamp, hotel_name])

        if rate_not_available_element:
            reason = rate_not_available_element.text.strip()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            csv_writer.writerow([date,reason, timestamp, hotel_name])

    # Create the complete URL
    url2 = f'https://www.hilton.com/en/book/reservation/flexibledates/?ctyhocn=TUPRURU&arrivalDate={TARGET_ARRIVAL}&departureDate={TARGET_DEPARTURE}&redeemPts=true&room1NumAdults=1&displayCurrency=USD'
    hotel_name = "Tru Oxford"
    driver.get(url2)
    
        # Wait for either element to be present
    wait_for_elements(driver)

    # Get the updated page source after JavaScript execution
    page_source = driver.page_source

    # Use Beautiful Soup to parse the HTML
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all elements with the specified data-testid
    date_and_price_elements = soup.find_all('button', attrs={"data-testid": True})

    # Extract and write the date and price information
    for element in date_and_price_elements:
        date = element['data-testid'].replace('arrival-', '')  # Extract date from data-testid attribute
        price_element = element.find(attrs={"data-testid": "flexDatesRoomRate"})
        rate_not_available_element = element.find(attrs={"data-testid": "rateNotAvailable"})

        # # Check if the price element exists
        if price_element:
            price = price_element.text.strip()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            csv_writer.writerow([date, price, timestamp, hotel_name])

        if rate_not_available_element:
            reason = rate_not_available_element.text.strip()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            csv_writer.writerow([date,reason, timestamp, hotel_name])

# Quit the browser
driver.quit()

# check for 5 consectuve nights

# Read the CSV file into a Pandas DataFrame
data = pd.read_csv(csv_file_path)

prices, filtered_data = get_price_for_date(TARGET_ARRIVAL)

print(price)

print(filtered_data)

condition_value = "false"

value_to_exclude = ['2 night stay unavailable', 'Sold out']

eligible_dates = filtered_data[~filtered_data['price'].isin(value_to_exclude)]

print(eligible_dates)
result_string = ""
if len(eligible_dates) > 0:
    for index, row in eligible_dates.iterrows():
        date = row['date']
        price = row['price']
        timestamp = row['timestamp']
        hotel_name = row['hotel_name']
        result_string += f"Date: {date}\n\nPrice: {price}\n\nHotel Name: {hotel_name}"
    condition_value = "true"
    result_string += f"\nGraduate URL: {url1}\n Tru URL: {url2}"
print(result_string)

with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    print(f'condition_value={condition_value}', file=fh)
    print(f'result_string={result_string}', file=fh)
