import mysql.connector
from mysql.connector import Error
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to create a connection to the MySQL database
def create_connection():
    connection = None
    try:
        # Establish connection to MySQL database
        connection = mysql.connector.connect(
            host="127.0.0.1",  # Adjust based on your server
            user="root",       # Use your MySQL username
            password="DJkevo0116",  # Use your MySQL password
            database="fantasy_tracker"    # The name of the database you created
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"Error: '{e}' occurred while connecting to MySQL")
    return connection

# Function to insert data into the 'players' table
def insert_player(connection, name):
    cursor = connection.cursor()
    query = """
    INSERT INTO players (name) 
    VALUES (%s)
    ON DUPLICATE KEY UPDATE name = name;
    """
    cursor.execute(query, (name,))
    connection.commit()
    return cursor.lastrowid # Return player_id for future use

# Function to insert weekly points into 'weekly_points' table
def insert_weekly_points(connection, player_id, week_number, opponent, points_proj, points_made):
    cursor = connection.cursor()
    query = """
    INSERT INTO weekly_points (player_id, week_number, opponent, points_proj, points_made)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE points_made = VALUES(points_made), points_proj = VALUES(points_proj), opponent = VALUES(opponent);
    """
    cursor.execute(query, (player_id, week_number, opponent, points_proj, points_made))
    connection.commit()

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
def data_scrapp(week_number):
    connection = create_connection()  # Create connection to MySQL
    url = 'https://fantasy.nfl.com/league/9616457/team/8'

    # Open the URL
    driver.get(url)

    # Wait for the dropdown menu to be visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'week-nav-dropdown-wrap'))
    )

    # Select the correct week
    try:
        # Look for the week link using the week_number
        week_link = driver.find_element(By.XPATH, f'//a[contains(@href, "statWeek={week_number}")]')
        week_link.click()  # Click on the link for the corresponding week
        time.sleep(3)  # Give the page some time to load
        print(f"Week {week_number} selected successfully.")
    except Exception as e:
        print(f"Error selecting week {week_number}: {e}")

    # Wait for the table inside 'tablewrap' to be visible (increase wait time)
    WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.ID, 'tableWrap-O'))
    )

    rows = driver.find_elements(By.XPATH, '//div[@id="tableWrap-O"]//table[@class="tableType-player hasGroups"]/tbody/tr')


    # Loop through each row and extract the necessary information
    for row in rows:
        try:
            # Try to extract data from each column
            #position = row.find_element(By.XPATH, './/td[@class="teamPosition first"]/span[@class="final"]').text
            name = row.find_element(By.CSS_SELECTOR, 'td.playerNameAndInfo a').text
            opponent = row.find_element(By.XPATH, './/td[@class="playerOpponent"]//a').text
            points_made = row.find_element(By.XPATH, './/td[@class="stat statTotal numeric last"]//span').text
            points_proj = None  # Placeholder for projected points from another table

            # Insert player data and get the player_id
            player_id = insert_player(connection, name)
            # Insert weekly points data
            insert_weekly_points(connection, player_id, week_number, opponent, points_proj, points_made)

        except Exception as e:
            print(f"Error extracting data: {e}")

    if connection:
        connection.close()  # Close the connection to MySQL when done


# Call the scraping function
data_scrapp(1)

# Quit the WebDriver
driver.quit()
