import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

# Setting up the driver
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=/Users/victor/Library/Application Support/Google/Chrome")
# chrome_options.add_argument("--profile-directory=Default")
driver = Chrome(options=chrome_options)

# Navigating to web page

driver.get("https://roamresearch.com/#/offline/test")

# Locating and clicking import menu
for css_selector in (
        ".bp3-icon-more",
        "li:nth-child(2) .bp3-text-overflow-ellipsis",
        ".bp3-button-text",
        ".bp3-text-overflow-ellipsis",
        ".bp3-intent-primary"
):
    el = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR, css_selector))
    el.click()

time.sleep(5)
driver.quit()
