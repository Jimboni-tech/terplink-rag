from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
load_dotenv()
import pandas as pd

def init_driver(url: str) -> webdriver:
    driver = webdriver.Chrome()
    driver.get(url)
    return driver
# user must sign into terplink
def user_sign_in() -> None:
    shadow_host = driver.find_element(By.ID, "parent-root")
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadow_host)
    header = driver.execute_script("return arguments[0].querySelector('header')", shadow_root)
    sign_in_button = driver.execute_script(
        "return arguments[0].querySelector('a.MuiButton-containedPrimary')", header
    )
    sign_in_button.click()

# loads all organizations
def load_orgs():
    while True: 
        try:
            load_button = driver.find_element(By.XPATH, "//div[@class='outlinedButton']/button")
            load_button.click()
            sleep(0.5) 
        except Exception:
            break

def collect_orgs() -> pd.DataFrame:
    df = pd.DataFrame(columns=['Name', 'Description', 'Additional Information', 'Public Events', 'News', 'Documents'])
    # creates a list containing all orgs
    orgs = driver.find_elements(By.CLASS_NAME, "MuiCard-root")
    # gather information about each org
    for org in orgs:
        pass
    return df

def org_info() -> dict:
    name = ""
    desc = ""
    additional_info = {
        "mission_statement": "", 
        "membership_requirements": "",
        "how_to_get_involved": "",
        "general_meeting_information": "",
        "expected_time_commitment": "",
        "meeting_schedule": ""
    }
    public_events = ""
    news = ""
    docs = ""
    try: 
        name = driver.find_element(By.TAG_NAME, "h1")
    except Exception:
        name = None
    
    try: 
        desc = driver.find_element(By.CLASS_NAME, "bodyText-large.userSupplied")
    except Exception:
        name = None
    
    additional_info["mission_statement"] =  ((driver.find_element(By.XPATH, "//strong[contains(text(), 'Mission Statement')]")).find_element(By.XPATH, "./parent::div").find_element(By.XPATH, "./parent::div")).text

    additional_info["membership_requirements"] = ((driver.find_element(By.XPATH, "//strong[contains(text(), 'Membership Requirements')]")).find_element(By.XPATH, "./parent::div").find_element(By.XPATH, "./parent::div")).text

    additional_info["how_to_get_involved"] = ((driver.find_element(By.XPATH, "//strong[contains(text(), 'How would a student get involved in your organization?')]")).find_element(By.XPATH, "./parent::div").find_element(By.XPATH, "./parent::div")).text

    additional_info["general_meeting_information"] = ((driver.find_element(By.XPATH, "//strong[contains(text(), 'Does your organization have general body meetings that are open for potential new members to attend?')]")).find_element(By.XPATH, "./parent::div").find_element(By.XPATH, "./parent::div")).text + ((driver.find_element(By.XPATH, "//strong[contains(text(), 'How often does your organization have general body meetings?')]")).find_element(By.XPATH, "./parent::div").find_element(By.XPATH, "./parent::div")).text

    additional_info["expected_time_commitment"] = ((driver.find_element(By.XPATH, "//strong[contains(text(), 'How would you rate the time commitment level to be a member of your organization?')]")).find_element(By.XPATH, "./parent::div").find_element(By.XPATH, "./parent::div")).text

    additional_info["meeting_schedule"] = ((driver.find_element(By.XPATH, "//strong[contains(text(), 'When are most of the commitments')]")).find_element(By.XPATH, "./parent::div").find_element(By.XPATH, "./parent::div")).text

    print(additional_info)
    




if __name__ == '__main__':
    '''terplink_url = "https://terplink.umd.edu/organizations"
    driver = init_driver(terplink_url)
    # user_sign_in(driver) # user signs in
    # waits until load button is available
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class='outlinedButton']/button")))
    load_orgs(driver) # presses load more button until all orgs are loaded
    collect_orgs(driver) # navigates through each orgs page'''
    
    driver = init_driver("https://terplink.umd.edu/organization/salvation-and-praise")
    org_info()
    
    driver.quit()
