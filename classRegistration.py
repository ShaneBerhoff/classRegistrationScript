#!/usr/bin/env python3
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
import datetime

# Username and password for login
username = "student-username"
password = "student-password"

def open_and_reload(reload_hour, reload_minute):
    # url currently set to emory class shopping cart
    url = "https://saprod.emory.edu/psc/saprod_8/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_MD_SP_FL.GBL?Action=U&MD=Y&GMenu=SSR_STUDENT_FL&GComp=SSR_START_PAGE_FL&GPage=SSR_START_PAGE_FL&scname=CS_SSR_MANAGE_CLASSES_NAV"
    
    # This opens browser and URL
    try:
        driver = webdriver.Firefox()  # can also use .Chrome or .Safari here
        driver.get(url)
        print("Connected to page")
        
        # Find the username and password fields and input the credentials
        username_field = driver.find_element(By.ID, "userid")
        password_field = driver.find_element(By.ID, "pwd")
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Find and click the login button
        login_button = driver.find_element(By.XPATH, "//input[@value='Login']")
        login_button.click()
        print("User logged in")
        
        # waits for the shopping cart to load then clicks it
        if element_ready(driver, "SCC_LO_FL_WRK_SCC_VIEW_BTN$3"):
            shopping_cart_element = driver.find_element(By.ID, "SCC_LO_FL_WRK_SCC_VIEW_BTN$3")
            shopping_cart_element.click()
            print("Entering shopping cart")
        else:
            print("Shopping cart not ready")
            sys.exit(1)
    except WebDriverException as error: #catches any issues
            print(f"There was an error: {error}")
            sys.exit(1)

    try:
        # calculates the reload time delay based on inputs and current time
        now = datetime.datetime.now()
        reload_time_today = datetime.datetime(now.year, now.month, now.day, reload_hour, reload_minute)
        if now > reload_time_today:
            reload_time_today += datetime.timedelta(days=1)
        delay = (reload_time_today - now).total_seconds()

        # waits
        print("Waiting for enrollment time")
        time.sleep(delay)

        # reload page
        # renaviagion to current url so that browser treats it as a GET request instead of
        # another POST request which it would for driver.refresh() causing a popup warning
        driver.get(driver.current_url)
        print("Page reloaded")
    except TimeoutException as error:
        print(f"Timeout: {error}")
        sys.exit(1)
    except Exception as error:
        print(f"An unknown error occured: {error}")
        sys.exit(1)
    
    # Wait for the first checkbox to be ready
    if element_ready(driver, "DERIVED_REGFRM1_SSR_SELECT$0"):
        # Now select all checkboxes
        checkboxes = driver.find_elements(By.CLASS_NAME, "ps-checkbox")
        print("Selecting classes")
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                checkbox.click()
    else:
        print("First checkbox not ready")
        sys.exit(1)
    
    # Find and click the Enroll button
    enroll_button = driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_ENROLL_FL")
    enroll_button.click()
    print("Enrollment requested")

    try:
        # Wait for the Yes button to be present in the DOM
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='#ICYes']"))
        )

        # Wait for the Yes button to be clickable
        yes_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='#ICYes']"))
        )

        yes_button.click()
        
    except TimeoutException:
        print("Yes button not ready or not found")
        sys.exit(1)
    
    print("Enjoy your classes!")

# Function to check if an element is visible
def element_ready(driver, element_id, timeout=10):
    try:
        # Wait for element to be present in DOM and visible
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, element_id))
        )

        end_time = time.time() + timeout
        while time.time() < end_time:
            if not is_element_obscured(driver, element):
                return True
            time.sleep(1) # time interval for obstruction check
    except WebDriverException as e:
        print(f"WebDriverException occurred: {e}")
    return False

# function to check for obstruction
def is_element_obscured(driver, element):
    return driver.execute_script(
        "var elem = arguments[0], box = elem.getBoundingClientRect(), "
        "cx = box.left + box.width / 2, cy = box.top + box.height / 2, "
        "e = document.elementFromPoint(cx, cy); "
        "return (e !== elem && !elem.contains(e));",
        element
    )

#main
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 classRegistration.py [Hour (24 format)] [Minute]")
        sys.exit(1)

    reload_hour = int(sys.argv[1])
    reload_minute = int(sys.argv[2])

    open_and_reload(reload_hour, reload_minute)
