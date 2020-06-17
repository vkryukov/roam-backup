#! /usr/local/bin/python3

import getpass
import glob
import tempfile
import time
import shutil
import sys
import subprocess

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


#https://stackoverflow.com/questions/48263317/selenium-python-waiting-for-a-download-process-to-complete-using-chrome-web
def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    # return driver.execute_script("""
    #         var items = downloads.Manager.get().items_;
    #         if (items.every(e => e.state === "COMPLETE"))
    #             return items.map(e => e.fileUrl || e.file_url);
    #         """)
    return driver.execute_script("""
        return document.querySelector('downloads-manager')
        .shadowRoot.querySelector('#downloadsList')
        .items.filter(e => e.state === 'COMPLETE')
        .map(e => e.filePath || e.file_path || e.fileUrl || e.file_url);
        """)


def download_local_graph(driver, name):
    """Download a local graph with given name to ~/Downloads"""
    print(f"Downloading local graph `{name}`...", end="")
    driver.get("https://roamresearch.com/#/offline/" + name)
    for css_selector in (
            ".bp3-icon-more",
            "li:nth-child(2) .bp3-text-overflow-ellipsis",
            ".bp3-button-text",
            ".bp3-text-overflow-ellipsis",
            ".bp3-intent-primary"
    ):
        el = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR, css_selector))
        time.sleep(0.1)
        el.click()

    # time.sleep(0.1)
    # el = driver.find_element_by_xpath("//div[contains(text(), 'Export All')]")
    # time.sleep(0.1)
    # el.click()
    #
    # for css_selector in (
    #         ".bp3-button-text",
    #         ".bp3-text-overflow-ellipsis",
    #         ".bp3-intent-primary"
    # ):
    #     el = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR, css_selector))
    #     el.click()

    # Give it some time to finish the download
    time.sleep(3)
    # WebDriverWait(driver, 10).until(every_downloads_chrome)
    print("done.")


def clone_chrome_user_data(username, dst_dir):
    """Copy Chrome settings folder to dst_dir"""
    print("Cloning chrome user data...", end="")
    src_dir = f"/Users/{username}/Library/Application Support/Google/Chrome"
    # subprocess.check_call(["cp", "-R", src_dir, dst_dir])
    try:
        shutil.copytree(src_dir, dst_dir)
    except shutil.Error:
        pass
    print("done.")


if __name__ == "__main__":
    username = getpass.getuser()
    tmp = tempfile.TemporaryDirectory()
    user_data_dir = tmp.name + "/chrome"

    clone_chrome_user_data(username, user_data_dir)

    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument("--profile-directory=Default")
    driver = Chrome(options=chrome_options)

    download_local_graph(driver, sys.argv[1])

    driver.quit()
