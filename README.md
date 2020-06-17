# Roam Research offline graph backup

This tool backs up one or few **local** [Roam Research](https://roamresearch.com) graphs. You can 
run it periodically using cron etc. to perform regular backups of your graph.

Since it's a version 0.1, it assumes that you are using Google Chrome on Mac OS. It should be
fairly trivial to make it more generic, but I have neither desire nor ability to test it in 
multiple configurations, although patches are welcome.

## Usage

```
python3 roam_backup.py local-graph local-backup-dir
``` 
where 
- `local-graph` is the name of the local graph
- `backup_destination` is a directory where the backup copy should be placed

## Installation

1. Download roam_backup.py and place it somewhere nice
1. Install Selenium Chrome driver with `brew cask install chromedriver`
1. Install `selenium` python package with `pip install selenium`
