# Roam Research offline graph backup

This tool backs up one or few **local** [Roam Research](https://roamresearch.com) graphs. You can 
run it periodically using cron etc. to perform regular backups of your graph.

Since it's a version 0.1, it assumes that you are using Google Chrome on Mac OS. It should be
fairly trivial to make it more generic, but I have neither desire nor ability to test it in 
multiple configurations, although patches are welcome.

## Installation

1. Download roam_backup.py and place it somewhere by navigating to the desired folder and executing the following 
command: 
    ```
    curl -O https://raw.githubusercontent.com/vkryukov/roam-backup/master/roam_backup.py
    ```
1. Install Selenium Chrome driver with `brew cask install chromedriver`
1. Install `selenium` python package with `pip3 install selenium --user`
1. Run `python3 roam_backup.py -h` to see the help message.

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

## Scheduling backup

To schedule backups on macOS, you can use a [launchd.plist generator](http://launched.zerowidth.com/). E.g.
if you put the script in `/Users/vkryukov`, and want to backup a local database `test` into 
`/Users/vkryukov/roam-backups` every 15 minutes, you should populate the following fields:

- Name: `Roam offline backup`
- Command: `/usr/local/bin/python3 /Users/vkryukov/roam_backup.py test /Users/vkryukov/roam-backup`
- Minute: `*/15`

Leave all the other fields blank.
