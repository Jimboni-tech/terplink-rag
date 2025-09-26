from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.window import WindowTypes
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
        sleep(0.5) 
        try:
            load_button = driver.find_element(By.XPATH, "//div[@class='outlinedButton']/button")
            load_button.click()

        except Exception:
            break
def collect_org_info() -> list:
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
        name = driver.find_element(By.TAG_NAME, "h1").text
    except Exception:
        name = None
    
    try: 
        desc = driver.find_element(By.CLASS_NAME, "bodyText-large.userSupplied").text
    except Exception:
        name = None
    
    # collects mission statement and cleans it
    try:

        additional_info["mission_statement"] =  ((driver.find_element(By.XPATH, "//strong[contains(text(), 'Mission Statement')]")).find_element(By.XPATH, "./parent::div").find_element(By.XPATH, "./parent::div")).text
        additional_info["mission_statement"] = additional_info["mission_statement"].replace("Mission Statement\nAn organization's mission statement should provide a description of the group's purpose.\n", "")
        
        if additional_info["mission_statement"].strip() == "No Response":
            additional_info["mission_statement"] = None
    except Exception:
        additional_info["mission_statement"] = None
    

    # collects membership requirements and cleans it
    try: 
        additional_info["membership_requirements"] = ((driver.find_element(By.XPATH, "//strong[contains(text(), 'Membership Requirements')]")).find_element(By.XPATH, "./parent::div").find_element(By.XPATH, "./parent::div")).text
        additional_info["membership_requirements"] = additional_info["membership_requirements"].replace("Membership Requirements\nPlease list information about the organizations selection process and include membership requirements if applicable.\n", "")
        if additional_info["membership_requirements"].strip() == "No Response":
            additional_info["membership_requirements"] = None
    except Exception:
        additional_info["membership_requirements"] = None


    # collects how to get involved and cleans it
    try:
        additional_info["how_to_get_involved"] = ((driver.find_element(By.XPATH, "//strong[contains(text(), 'How would a student get involved in your organization?')]")).find_element(By.XPATH, "./parent::div").find_element(By.XPATH, "./parent::div")).text
        additional_info["how_to_get_involved"] = additional_info["how_to_get_involved"].replace('How would a student get involved in your organization?\nIncluding, but not limited to, "show up to our meetings!" or "you must apply and applications are available," or "email us and let us know you want to be involved!"\n', "")
        if additional_info["how_to_get_involved"].strip() == "No Response":
            additional_info["how_to_get_involved"] = None
    except Exception:
        additional_info["how_to_get_involved"] = None


    # collects general meeting information and when general meetings are and cleans it 
    try:
        additional_info["general_meeting_information"] = ((driver.find_element(By.XPATH, "//strong[contains(text(), 'Does your organization have general body meetings that are open for potential new members to attend?')]")).find_element(By.XPATH, "./parent::div").find_element(By.XPATH, "./parent::div")).text
        additional_info["general_meeting_information"] = additional_info["general_meeting_information"].replace("Does your organization have general body meetings that are open for potential new members to attend?\n", "")
        if additional_info["general_meeting_information"].strip() == "No Response":
            additional_info["general_meeting_information"] = ""

    except Exception:
        additional_info["general_meeting_information"] = ""
    try:
        temp = ((driver.find_element(By.XPATH, "//strong[contains(text(), 'How often does your organization have general body meetings?')]")).find_element(By.XPATH, "./parent::div").find_element(By.XPATH, "./parent::div")).text.strip()
        temp = temp.replace("How often does your organization have general body meetings?\n", "")
        if temp != "No Response":
            additional_info["general_meeting_information"] += temp
        
    except Exception:
        additional_info["general_meeting_information"] += ""
    
    if additional_info["general_meeting_information"] == "":
        additional_info["general_meeting_information"] = None


    # collects expected time commitment and cleans it 
    try: 
        additional_info["expected_time_commitment"] = ((driver.find_element(By.XPATH, "//strong[contains(text(), 'How would you rate the time commitment level to be a member of your organization?')]")).find_element(By.XPATH, "./parent::div").find_element(By.XPATH, "./parent::div")).text
        additional_info["expected_time_commitment"] = additional_info["expected_time_commitment"].replace("How would you rate the time commitment level to be a member of your organization? \n", "")
        if additional_info["expected_time_commitment"].strip() == "No Response":
            additional_info["expected_time_commitment"] = None
    except Exception:
        additional_info["expected_time_commitment"] = None

    # collects meeting schedule and cleans it
    try:
        additional_info["meeting_schedule"] = ((driver.find_element(By.XPATH, "//strong[contains(text(), 'When are most of the commitments')]")).find_element(By.XPATH, "./parent::div").find_element(By.XPATH, "./parent::div")).text
        additional_info["meeting_schedule"] = additional_info["meeting_schedule"].replace("When are most of the commitments (meetings, events, office hours, etc.) for your organization? (check all that apply)\n", "")
        if additional_info["meeting_schedule"].strip() == "No Response":
            additional_info["meeting_schedule"] = None
    except Exception:
        additional_info["expected_time_commitment"] = None
    return [name, desc, additional_info]



def collect_orgs() -> pd.DataFrame:
    df = pd.DataFrame(columns=['Name', 'Description', 'Additional Information']) # , 'Public Events', 'News', 'Documents'
    # creates a list containing all orgs
    orgs = driver.find_elements(By.CLASS_NAME, "MuiCard-root")
    links = []
    # gather link for each org
    for org in orgs:
        try:
            links.append(org.find_element(By.XPATH, "./parent::a").get_attribute("href"))
        except Exception:
            print(Exception)


    original_window = driver.current_window_handle
    for link in links:
        driver.switch_to.new_window(WindowTypes.TAB)
        driver.get(link)
        sleep(.2)
        temp = collect_org_info()
        df.loc[len(df)] = temp
        driver.close()
        driver.switch_to.window(original_window)
        sleep(.2)
        
    return df


    




if __name__ == '__main__':
    url = "https://terplink.umd.edu/organizations"
    driver = init_driver(url)
    # user_sign_in(driver) # user signs in
    # waits until load button is available
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class='outlinedButton']/button")))
    load_orgs() # presses load more button until all orgs are loaded
    df = collect_orgs() # navigates through each orgs page and collects information
    driver.quit()
