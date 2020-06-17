# Roam Research offline graph backup

This tool backs up one or few **local** [Roam Research](https://roamresearch.com) graphs. You can 
run it periodically using cron etc. to perform regular backups of your graph.

Since it's a version 0.1, it assumes that you are using Google Chrome on Mac OS. It should be
fairly trivial to make it more generic, but I have neither desire nor ability to test it in 
multiple configurations, although patches are welcome.

## Usage

```
usage: roam_backup.py [-h] local_graph backup_dir

Backup local Roam database.

positional arguments:
  local_graph  name of the local graph
  backup_dir   folder to place backup files

optional arguments:
  -h, --help   show this help message and exit

```

## Installation

1. Download roam_backup.py and place it somewhere nice
1. Install Selenium Chrome driver with `brew cask install chromedriver`
1. Install `selenium` python package with `pip install selenium`
