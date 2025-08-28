import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Sample test data
test_data = [
    ("Admin", "admin123", "success"),
    ("user", "wrongpass", "fail"),
    ("", "noUser", "fail"),
]

@pytest.fixture
def driver():
    # Setup
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    yield driver, wait
    # Teardown (runs after test ends, pass or fail)
    driver.quit()

@pytest.mark.parametrize("username, password, expected", test_data)
def test_login(driver, username, password, expected):
    driver, wait = driver  # unpack fixture values

    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    # Input credentials
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Validation
    if expected == "success":
        wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']")))
        assert "Dashboard" in driver.page_source
    else:
        wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'Invalid credentials')]")))
        assert "Invalid credentials" in driver.page_source
