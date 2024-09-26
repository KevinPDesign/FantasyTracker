from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json
import time

# Setting Chrome options to ignore SSL errors
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the NFL Fantasy login page
driver.get('https://www.nfl.com/account/sign-in')
time.sleep(2)  # Give the page a moment to load

# Wait for the email input to be visible and enter the email
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'email-input-field')))
email_input = driver.find_element(By.ID, 'email-input-field')
email_input.send_keys('dekevines.laweb@gmail.com')

# Wait for the "Continue" button to be enabled and click it
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@value="Continue"]')))
continue_button = driver.find_element(By.XPATH, '//button[@value="Continue"]')
continue_button.click()

# Wait for the password input to be visible and enter the password
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'password-input-field')))
password_input = driver.find_element(By.ID, 'password-input-field')
password_input.send_keys('DJkevo0116?')

# Wait for the "Sign In" button to be enabled and click it
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@value="Sign In"]')))
sign_in_button = driver.find_element(By.XPATH, '//button[@value="Sign In"]')
sign_in_button.click()

# Create a list to store rows and later build the DataFrame
data = []

# Function to scrape fantasy data
def data_scrapp():
    url = 'https://fantasy.nfl.com/league/9616457/team/8'

    # Open the URL
    driver.get(url)

    # Wait for the table inside 'tablewrap' to be visible (increase wait time)
    WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.ID, 'tableWrap-O'))
    )

    # Locate the table inside the div
    # table = driver.find_element(By.XPATH, '//div[@id="tableWrap-O"]//table[@class="tableType-player hasGroups"]')
    # print(table.get_attribute('outerHTML'))  # Print the table's HTML content

    # Locate rows within the table
    # rows = driver.find_elements(By.XPATH, './tbody/tr')
    # rows = table.find_elements(By.XPATH, './tbody/tr')
    # print(f"Number of rows found: {len(rows)}")  # Print the number of rows found
    rows = driver.find_elements(By.XPATH, '//div[@id="tableWrap-O"]//table[@class="tableType-player hasGroups"]/tbody/tr')


    # Loop through each row and extract the necessary information
    for row in rows:
        try:
            # Try to extract data from each column
            position = row.find_element(By.XPATH, './/td[@class="teamPosition first"]/span').text
            name = row.find_element(By.XPATH, './/td[@class="playerNameAndInfo"]//a').text
            opponent = row.find_element(By.XPATH, './/td[@class="playerOpponent"]//a').text
            points_made = row.find_element(By.XPATH, './/td[@class="stat statTotal numeric last"]//span').text
            points_proj = None  # Placeholder for projected points from another table

            # Append the extracted data to the list
            data.append({
                "name": name,
                "position": position,
                "opponent": opponent,
                "points_proj": points_proj,
                "points_made": points_made
            })
        except Exception as e:
            print(f"Error extracting data: {e}")


    # Convert the list to a DataFrame at the end of the loop
    df = pd.DataFrame(data)
    print(df)

# Call the scraping function
data_scrapp()

# Quit the WebDriver
driver.quit()
