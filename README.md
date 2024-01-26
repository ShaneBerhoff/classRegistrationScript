# README for Class Registration Script

## Description

This script automates the process of registering for classes at Emory University through OPUS. It utilizes Selenium WebDriver for browser automation. The script logs into the student portal, waits until a specified time, and then attempts to enroll in the classes added to the shopping cart.

## Requirements

- Python 3
- Selenium WebDriver
- A web driver compatible with your browser (e.g., geckodriver for Firefox)

## Setup

1. **Install Python 3:** Ensure Python 3 is installed on your system.
2. **Install Selenium:** Install Selenium library using pip:
   ```
   pip install selenium
   ```
3. **Web Driver:** Download and set up the appropriate web driver for your browser:
   - Firefox: [geckodriver](https://github.com/mozilla/geckodriver/releases)
   - Chrome: [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
   - Safari: Safari comes with its driver.
4. **Script Location:**
   - **Accessible Path:** Place the script in a directory that is accessible via your system's PATH environment variable. This allows you to run the script from any location in your command line interface.
   - **Updating PATH:** If you're not sure about your PATH, you can either add the script's directory to your PATH or navigate to the script's directory in the command line before running it.
   - **Permissions:** Ensure that the script file has executable permissions. On Unix-like systems, you can set this with `chmod +x classRegistration.py`.

## Usage

1. **Edit Script:** Open the script in a text editor and replace `student-username` and `student-password` with your actual Emory OPUS login credentials.
2. **Run the Script:** Execute the script from the command line with the hour and minute you want the script to start enrolling in classes. This should be the time that registration opens. Use 24-hour format for the time.
   ```
   classRegistration.py [Hour] [Minute]
   ```
   Example if class registration is at 5:30 PM:
   ```
   classRegistration.py 17 30
   ```
   This command will run the script, login to OPUS, and wait for a 5:30 PM enrollment time.
   So in this example it would be essential to run the script a few minutes before 5:30 PM so that it can login and load up.

## How It Works

1. **Open Browser:** The script opens a browser and navigates to the Emory class registration page.
2. **Login:** It logs in using the provided credentials.
3. **Shopping Cart:** Navigates to the shopping cart.
4. **Wait for Enrollment Time:** Waits until the specified time.
5. **Enroll in Classes:** Automatically selects all classes in the shopping cart and attempts to enroll.

## Important Notes

- **Class Validation:** Ensure that classes are validated before running the script, as unvalidated classes may lead to unsuccessful enrollment.
- **Shopping Cart Handling:**
   - If the script logs in but fails to automatically navigate to the shopping cart, you may manually click on the shopping cart tab. The script will still function correctly after this manual intervention; simply allow it to continue running uninterrupted.
   - It's important to note that the script is designed to work with only one shopping cart. If multiple shopping carts are present, the script will not navigate correctly. You need to manually select the correct shopping cart; then allow it to continue running and it will do the rest correctly
- **Timing:** Ensure the computer's time is synchronized correctly.
- **Internet Connection:** A stable internet connection is required.
- **Browser Compatibility:** Make sure the script is using the correct web driver for your browser.
- **Error Handling:** The script has basic error handling for timeouts and web driver exceptions.
- **Functionality:** The script was functional as of 1/25/2024. Changes to Emory's registration page may have broken parts of it, but it should easily be fixable.

## Disclaimer

This script is intended for educational purposes. Be aware of Emory University's policies on automated systems for class registration. Use at your own risk.
