from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


terplink_url = "https://terplink.umd.edu/organizations"
driver = webdriver.Chrome()
driver.get(terplink_url)


while True: # loads all organizations
    try:
        load_button = driver.find_element(By.XPATH, "//div[@class='outlinedButton']/button")
        load_button.click()
        sleep(0.5) 
    except Exception:
        break




orgs = driver.find_elements(By.CLASS_NAME, "MuiCard-root")
print(len(orgs))



driver.quit()
