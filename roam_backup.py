#! /usr/local/bin/python3

import argparse
import getpass
import glob
import os.path
import tempfile
import time
import shutil

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

SLEEP_BETWEEN_ACTIONS = 0.1  # Sleep time between consecutive browser actions

def download_local_graph(driver, name, timeout):
    """Download a local graph with given name to ~/Downloads"""
    print(f"Downloading local graph `{name}`...", end="")
    driver.get("https://roamresearch.com/#/offline/" + name)
    for css_selector in (
            ".bp3-icon-more",
            "li:nth-child(3) .bp3-text-overflow-ellipsis",
            ".bp3-button-text",
            ".bp3-text-overflow-ellipsis",
            ".bp3-intent-primary"
    ):
        try:
            el = WebDriverWait(driver, timeout=timeout).until(lambda d: d.find_element(By.CSS_SELECTOR, css_selector))
            time.sleep(SLEEP_BETWEEN_ACTIONS)
            el.click()
        except TimeoutException as e:
            print(f"Timeout of {timeout} seconds exceeded while finding selector {css_selector}. Exiting...")
            raise e

    time.sleep(timeout)
    print("done.")


def clone_chrome_user_data(username, dst_dir):
    """Copy Chrome settings folder to dst_dir"""
    print("Cloning chrome user data...", end="")
    src_dir = f"/Users/{username}/Library/Application Support/Google/Chrome"
    try:
        shutil.copytree(src_dir, dst_dir)
    except shutil.Error:
        pass
    print("done.")


def move_roam_exports_since(start, backup_dir, username, local_graph):
    """Move all Roam-Export-*.zip files created after start into dst_dir"""
    paths = [p for p in glob.glob(f"Roam-Export-*.zip")
             if os.path.getctime(p) >= start]
    for p in paths:
        base = os.path.splitext(os.path.basename(p))[0][len("Roam-Export-"):]
        fmt_time = time.strftime("%Y-%m-%d-%H%M%S", time.localtime(float(base) / 1000))
        target = os.path.join(backup_dir, f"{local_graph}-{fmt_time}.zip")
        print(f"Moving {p} to {target}...", end="")
        shutil.move(p, target)
        print("done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Backup local Roam database.')
    parser.add_argument("local_graph", help="name of the local graph")
    parser.add_argument("backup_dir", help="folder to place backup files")
    parser.add_argument("--debug", help="show the browser and pause after each step", action="store_true")
    parser.add_argument("--timeout", help="max timeout for each action", type=float, default=30)
    args = parser.parse_args()

    username = getpass.getuser()
    tmp = tempfile.TemporaryDirectory()
    user_data_dir = tmp.name + "/chrome"

    clone_chrome_user_data(username, user_data_dir)

    print("Launching headless chrome...", end="")
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--disable-extensions")
    if args.debug:
        SLEEP_BETWEEN_ACTIONS = 1.0
    else:
        chrome_options.add_argument("--headless")

    driver = Chrome("/usr/local/bin/chromedriver", options=chrome_options)
    print("done.")

    start = time.time()
    download_local_graph(driver, args.local_graph, args.timeout)
    move_roam_exports_since(start, args.backup_dir, username, args.local_graph)

    driver.quit()
