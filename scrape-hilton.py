from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

url = 'https://www.hilton.com/en/book/reservation/flexibledates/?ctyhocn=MLEONWA&arrivalDate=2024-04-20&departureDate=2024-04-21&redeemPts=true&room1NumAdults=1&displayCurrency=USD'  # Replace with the actual URL

# Set up a headless Chrome browser
options = Options()
options.add_argument('--disable-gpu')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Navigate to the webpage
driver.get(url)

# Wait for dynamic content to load (adjust the sleep time accordingly)
time.sleep(25)

# Get the updated page source after JavaScript execution
page_source = driver.page_source

# Save the page source to a file
with open('output_page_source.html', 'w', encoding='utf-8') as file:
    file.write(page_source)
# Use Beautiful Soup to parse the HTML
soup = BeautifulSoup(page_source, 'html.parser')

# Step 5: Find all elements with the specified data-testid
date_and_price_elements = soup.find_all('button', attrs={"data-testid": True})

# Extract and print the date and price information
for element in date_and_price_elements:
    date = element['data-testid'].replace('arrival-', '')  # Extract date from data-testid attribute
    price_element = element.find(attrs={"data-testid": "flexDatesRoomRate"})

    # Check if the price element exists
    if price_element:
        price = price_element.text.strip()
        print(f"Date: {date}, Price: {price} Points")

# Quit the browser
driver.quit()