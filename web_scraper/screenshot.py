from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# URL of the webpage to screenshot
url = "example.com"  # Replace with your actual URL

# Set up Chrome options
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--window-size=1920,1080")  # Set initial window size

# Set up ChromeDriver using WebDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Open the webpage
    driver.get(url)

    # Wait for the cookie dialog and click "Allow All Cookies" if it appears
    try:
        allow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Allow All Cookies')]"))
        )
        allow_button.click()
        print("Clicked 'Allow All Cookies'")
    except Exception as e:
        print("No 'Allow All Cookies' button found or timed out:", e)

    # Wait briefly after clicking the cookie dialog button
    time.sleep(2)

    # Slowly scroll down the page to load all dynamic content
    scroll_pause_time = 1  # Pause between scrolls
    scroll_increment = 300  # Pixels to scroll at each step

    last_height = driver.execute_script("return document.body.scrollHeight")
    current_scroll_position = 0

    while current_scroll_position < last_height:
        # Scroll down by the increment
        driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
        time.sleep(scroll_pause_time)  # Wait to allow content to load
        current_scroll_position += scroll_increment

        # Update last_height to the new scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height > last_height:
            last_height = new_height

    # After scrolling, take the full-page screenshot
    full_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1920, full_height)  # Adjust width as needed

    # Save the screenshot
    screenshot_path = "full_page_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"Full-page screenshot with dynamic content saved as {screenshot_path}")

finally:
    # Close the driver
    driver.quit()