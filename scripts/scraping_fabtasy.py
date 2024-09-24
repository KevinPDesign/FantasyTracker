from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Iniciate WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

df = pd.DataFrame(columns=["name", "position", "opponent", "points_proj", "points_made"])

def data_scrapp():
    url = 'https://fantasy.nfl.com/league/9616457/team/8?statCategory=projectedStats&statSeason=2024&statType=weekProjectedStats&statWeek=5&week=5'

    #Open URL
    driver.get(url)

    #Loading time
    time.sleep(5)

    rows = driver.find_elements(By.XPATH, '//table[@class="tableType-player hasGroups"]/tbody/tr')
    for row in rows:
        #Extract each row with the correspondig class
        position = row.find_element(By.CLASS_NAME, 'teamPosition.first').text
        name = row.find_element(By.CLASS_NAME, 'playerNameAndInfo').text
        opponent = row.find_element(By.CLASS_NAME, 'playerOpponent').text
        points_made = row.find_element(By.CLASS_NAME, 'stat.statTotal.numeric.last').text
        points_proj = None #This value is in another table, for now we'll leave it as this.

        #add the values to the DataFrame
        df = df.append({
            "name": name,
            "position": position,
            "opponent": opponent,
            "points_proj": points_proj, #We'll add this value later
            "points_made": points_made
        }, ignore_index=True)

    print(df)

data_scrapp()

driver.quit()