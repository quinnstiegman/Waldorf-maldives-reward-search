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

def get_months(n):
    future_date = datetime.now() + timedelta(days=304)  
    months_list = []

    for i in range(n):
        # Adding 'i' months to the future date
        target_date = future_date + timedelta(days=future_date.day - 1)  # Go to the last day of the month
        target_date = target_date.replace(month=future_date.month + i)
        months_list.append(target_date.strftime('%Y-%m'))

    return months_list

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
    csv_writer.writerow(['date', 'price', 'timestamp'])
    # Iterate through different variations of the URL by changing a small part
    dates = get_months(4)
    for date in dates:  # Change the range or logic as needed
        # Create the complete URL
        url = f'https://www.hilton.com/en/book/reservation/flexibledates/?ctyhocn=MLEONWA&arrivalDate={date}-20&departureDate={date}-21&redeemPts=true&room1NumAdults=1&displayCurrency=USD'

        driver.get(url)
        
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
                csv_writer.writerow([date, price, timestamp])

            if rate_not_available_element:
                reason = rate_not_available_element.text.strip()
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                csv_writer.writerow([date,reason, timestamp])

# Quit the browser
driver.quit()

# check for 5 consectuve nights

# Read the CSV file into a Pandas DataFrame
data = pd.read_csv(csv_file_path)

# Check for two consecutive dates with the value '150k'
two_consecutive_150k_start = None
for i in range(len(data) - 1):
    if data['price'][i] == '150,000' and data['price'][i + 1] == '150,000':
        two_consecutive_150k_start = data['date'][i]
        break

# Check for five consecutive dates with the value '150k'
five_consecutive_150k_start = None
for i in range(len(data) - 4):
    if data['price'][i] == '150,000' and \
       data['price'][i + 1] == '150,000' and \
       data['price'][i + 2] == '150,000' and \
       data['price'][i + 3] == '150,000' and \
       data['price'][i + 4] == '150,000':
        five_consecutive_150k_start = data['date'][i]
        break
condition_value = "false"

five_consecutive_150k_starts_list = []
consecutive_count = 0

for i in range(len(data) - 4):
    if (
        data['price'][i] == '150,000'
        and data['price'][i + 1] == '150,000'
        and data['price'][i + 2] == '150,000'
        and data['price'][i + 3] == '150,000'
        and data['price'][i + 4] == '150,000'
    ):
        five_consecutive_150k_starts_list.append(data['date'][i])
        consecutive_count += 1

# Print or use the list of start dates
if consecutive_count > 0:
    print("Found", consecutive_count, "sets of 5 consecutive dates:")
    for start_date in five_consecutive_150k_starts_list:
        print(start_date)
else:
    print("No sets of 5 consecutive dates found.")

# Print the results
if two_consecutive_150k_start:
    print(f'There are two consecutive dates with the value of "150k". Starting date: {two_consecutive_150k_start}')
    # message = 'test message'
    # data = {
    # 'token': api_token,
    # 'user': user_key,
    # 'message': message,
    # }

    # response = requests.post(url, data=data)

    # if response.status_code == 200:
    #     print('Message sent successfully')
    # else:
    #     print(f'Failed to send message. Status code: {response.status_code}, Response: {response.text}')
else:
    print('There are no two consecutive dates with the value of "150k".')

if five_consecutive_150k_start:
    print(f'There are five consecutive dates with the value of "150k". Starting date: {five_consecutive_150k_start}')
    condition_value = "true" 
else:
    print('There are no five consecutive dates with the value of "150k".')

with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    print(f'condition_value={condition_value}', file=fh)
    print(f'start_date={five_consecutive_150k_start}', file=fh)
    print(f'url={url}', file=fh)
    print(f'start_date_list={five_consecutive_150k_starts_list}', file=fh)


