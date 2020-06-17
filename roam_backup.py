#! /usr/local/bin/python3

import argparse
import getpass
import glob
import os.path
import tempfile
import time
import shutil
import sys

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


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

    time.sleep(3)
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


def move_roam_exports_since(start, backup_dir, username, local_graph):
    """Move all Roam-Export-*.zip files created after start into dst_dir"""
    paths = [p for p in glob.glob(f"/Users/{username}/Downloads/Roam-Export-*.zip")
             if os.path.getctime(p) >= start]
    for p in paths:
        base = os.path.splitext(os.path.basename(p))[0][len("Roam-Export-"):]
        fmt_time = time.strftime("%Y-%m-%d-%H%M%S", time.localtime(float(base)/1000))
        shutil.move(p, os.path.join(backup_dir, f"{local_graph}-{fmt_time}.zip"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Backup local Roam database.')
    parser.add_argument("local_graph", help="name of the local graph")
    parser.add_argument("backup_dir", help="folder to place backup files")
    args = parser.parse_args()

    username = getpass.getuser()
    tmp = tempfile.TemporaryDirectory()
    user_data_dir = tmp.name + "/chrome"

    clone_chrome_user_data(username, user_data_dir)

    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--disable-extensions")  # to avoid  nasty side effects
    driver = Chrome(options=chrome_options)

    start = time.time()
    download_local_graph(driver, args.local_graph)
    move_roam_exports_since(start, args.backup_dir, username, args.local_graph)

    driver.quit()
