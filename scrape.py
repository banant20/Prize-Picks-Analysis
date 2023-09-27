import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import pandas as pd

options = uc.ChromeOptions()
options.headless = False
driver = uc.Chrome(options = options)

# Scrape PrizePicks
driver.get("https://app.prizepicks.com/")
time.sleep(3)

# Closes initial tutorial popup that appears
driver.find_element(By.CLASS_NAME, value = "close").click()
time.sleep(3)


# Creating tables for players
ppPlayers = []

driver.find_element(By.XPATH, "//div[@class='name'][normalize-space()='NFL']").click()
time.sleep(5)

# Waits until stat container element is fully viewable
stat_container = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "stat-container")))

# Getting each prop type in the stat container
categories = driver.find_element(By.CSS_SELECTOR, ".stat-container").text.split('\n')

# Get all the players and their props for each prop type
for category in categories:
    driver.find_element(By.XPATH, f"//div[text()='{category}']").click()

    projectionsPP = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".projection")))

    for projections in projectionsPP:
        names = projections.find_element(By.CLASS_NAME, "name").text
        team = projections.find_element(By.CLASS_NAME, "team-position").get_attribute('innerHTML')
        value = projections.find_element(By.CLASS_NAME, "presale-score").get_attribute('innerHTML')
        proptype = projections.find_element(By.CLASS_NAME, "text").get_attribute('innerHTML')

        players = {
            'Player': names,
            'Team-Position': team,
            'Line': value,
            'PropType': proptype.replace("<wbr>", "")
        }
        ppPlayers.append(players)

dfProps = pd.DataFrame(ppPlayers)
dfProps.to_excel('lines.xlsx', engine='openpyxl', index=False)