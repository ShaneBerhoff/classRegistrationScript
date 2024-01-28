#!/usr/bin/env python3
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
import datetime

# Select Browser
browser = "Firefox"
#browser = "Chrome"
#browser = "Safari"

# Username and password for login
username = "student-username"
password = "student-password"

# url currently set to emory course enrollment
url = "https://saprod.emory.edu/psc/saprod_8/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_MD_SP_FL.GBL?Action=U&MD=Y&GMenu=SSR_STUDENT_FL&GComp=SSR_START_PAGE_FL&GPage=SSR_START_PAGE_FL&scname=CS_SSR_MANAGE_CLASSES_NAV"
# page elements
cart_id = "SCC_LO_FL_WRK_SCC_VIEW_BTN$3"
first_checkbox_id = "DERIVED_REGFRM1_SSR_SELECT$0"
checkbox_class = "ps-checkbox"
enroll_id = "DERIVED_SSR_FL_SSR_ENROLL_FL"

def open_and_reload(reload_hour, reload_minute):
    
    try: # Open browser and URL
        if browser == "Firefox":
            driver = webdriver.Firefox()
        elif browser == "Chrome":
            driver = webdriver.Chrome()
        elif browser == "Safari":
            driver = webdriver.Safari()
        else:
            raise WebDriverException("Invalid browser selected")
        
        driver.maximize_window()
        driver.get(url)
        print("Connected to page")
    except WebDriverException as error: #catches any issues
        print(f"There was an error loading the page: {error}")
        sys.exit(1)
    
    try: # User login
        # Find the username and password fields and inputs the credentials
        username_field = driver.find_element(By.ID, "userid")
        password_field = driver.find_element(By.ID, "pwd")
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Find and click the login button
        login_button = driver.find_element(By.XPATH, "//input[@value='Login']")
        login_button.click()
        print("User logged in")
    except WebDriverException as error:
        print(f"Failure to login: {error}")
        sys.exit(1)
    
    # wait for the shopping cart then click it
    if wait_for_element(driver, cart_id):
        driver.find_element(By.ID, cart_id).click()
        print("Navigated to shopping cart")
    else:
        print("Failed to navigate to shopping cart tab")

    try: # reload time
        # calculates the reload time delay based on inputs and current time
        now = datetime.datetime.now()
        reload_time = datetime.datetime(now.year, now.month, now.day, reload_hour, reload_minute)
        if now > reload_time:
            raise Exception("Selected time already passed for today")
        delay = (reload_time - now).total_seconds()

        # waits
        print("Waiting for enrollment time")
        time.sleep(delay)

        # reload page
        # renaviagion to current url so that browser treats it as a GET request instead of
        # another POST request which it would for driver.refresh() causing a popup warning
        driver.get(driver.current_url)
        print(f"Page reloaded sucessfully at {reload_hour}:{reload_minute}")
    except TimeoutException as error:
        print(f"Timeout: {error}")
        sys.exit(1)
    except Exception as error:
        print(f"An error occured: {error}")
        sys.exit(1)
    
    # Wait for the first checkbox to be ready
    if wait_for_element(driver, first_checkbox_id):
        # Now select all checkboxes
        checkboxes = driver.find_elements(By.CLASS_NAME, checkbox_class)
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                checkbox.click()
        print("Classes selected")
    else:
        print("First checkbox not ready")
        sys.exit(1)
    
    try: # enroll
        # Find and click the Enroll button
        enroll_button = driver.find_element(By.ID, enroll_id)
        enroll_button.click()
        print("Enrollment requested")
    except:
        print("Could not find enrollment button")
        sys.exit(1)

    try: # yes
        # Wait for the Yes button to be present in the DOM
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='#ICYes']"))
        )

        # Wait for the Yes button to be clickable
        yes_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='#ICYes']"))
        )

        # Click
        yes_button.click()
        print("Enjoy your classes!")
    except TimeoutException:
        print("Yes button not ready or not found")
        sys.exit(1)

    # Stops Safari and Chrome from imediatly closing
    if browser=="Safari" or browser=="Chrome":
        print("Browser will automatically close in 1 minute.")
        time.sleep(60)

# Function to wait for an element to exist and be unobstructed
def wait_for_element(driver, element_id, timeout=10):
    try:
        # Wait for the element to be present in DOM and visible
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, element_id))
        )

        # Retrieve the element by ID
        element = driver.find_element(By.ID, element_id)

        # Wait until the element is unobstructed
        WebDriverWait(driver, timeout).until(
            lambda d: not d.execute_script(
                "var elem = arguments[0], box = elem.getBoundingClientRect(), "
                "cx = box.left + box.width / 2, cy = box.top + box.height / 2, "
                "e = document.elementFromPoint(cx, cy); "
                "return (e !== elem && !elem.contains(e));",
                element
            )
        )
        
        # Wait until the element is clickable
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, element_id))
        )
    except TimeoutException:
        print(f"Timeout waiting for element with ID '{element_id}' to be ready.")
        return False
    except Exception as error:
        print(f"Error when waiting for element with ID '{element_id}': {error}")
        return False
    return True

#main
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: classRegistration.py [Hour (24 format)] [Minute]")
        sys.exit(1)

    reload_hour = int(sys.argv[1])
    reload_minute = int(sys.argv[2])

    open_and_reload(reload_hour, reload_minute)