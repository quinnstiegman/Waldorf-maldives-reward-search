import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

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


# Set up a headless Chrome browser
options = Options()
options.add_argument('--disable-gpu')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Save the results to a CSV file
previous_prices = {}
csv_file_path = 'output_results.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Iterate through different variations of the URL by changing a small part
    dates = ['2024-11', '2024-10', '2024-12' , '2025-01' , '2025-02' ]
    for date in dates:  # Change the range or logic as needed
        # Create the complete URL
        url = f'https://www.hilton.com/en/book/reservation/flexibledates/?ctyhocn=MLEONWA&arrivalDate={date}-20&departureDate={date}-21&redeemPts=true&room1NumAdults=1&displayCurrency=USD'

        # Set up the Chrome driver
        driver = webdriver.Chrome(options=options)
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

# Read the CSV file
with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

# Initialize variables
consecutive_count = 0
target_value = '150k'

# Iterate through the rows starting from the second row
for i in range(1, len(rows) - 4):
    date = rows[i][0]
    value = rows[i][1]

    # Check if the value is equal to the target value
    if value == str(target_value):
        # Check the next 4 consecutive dates
        if all(rows[i + j][1] == str(target_value) for j in range(1, 5)):
            consecutive_count += 1

            # If 5 consecutive dates are found, print the result and break the loop
            if consecutive_count == 2:
                print(f"Found 5 consecutive dates with a value of {target_value} starting from {date}")
                break
        else:
            consecutive_count = 0
    else:
        consecutive_count = 0

# If no consecutive dates are found, print a message
if consecutive_count < 5:
    print(f"No 5 consecutive dates with a value of {target_value} found.")

