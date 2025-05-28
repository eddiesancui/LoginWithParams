import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Create directory for screenshots if it doesn't exist
os.makedirs("screenshots", exist_ok=True)

# Sample test data
test_data = [
    ("Admin", "admin123", "success"),
    ("user", "wrongpass", "fail"),
    ("", "noUser", "fail"),
]

@pytest.mark.parametrize("username, password, expected", test_data)
def test_login(username, password, expected):
    # Setup WebDriver
    service = Service()
    driver = webdriver.Chrome(service=service)
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    wait = WebDriverWait(driver, 10)

    # Input credentials
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Wait and validate result
    try:
        if expected == "success":
            wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']")))
            assert "Dashboard" in driver.page_source
        else:
            wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'Invalid credentials')]")))
            assert "Invalid credentials" in driver.page_source
    finally:
        # Take screenshot regardless of test result
        safe_username = username if username else "empty_user"
        screenshot_name = f"screenshots/login_{safe_username}_{expected}.png"
        driver.save_screenshot(screenshot_name)

        driver.quit()
