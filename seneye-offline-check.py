#!/usr/bin/python
import json, requests, calendar, time
from pushbullet import Pushbullet

## Settings: Change these:
## Username and password, obviously:
username = 'me@myemail.com'
password = 'myPassword'
## How many minutes until you want an offline alert:
## You may want to set this to 1 or something to test the script before setting it to a higher value.
offlineAlertTime = 240
## Pushbullet API key
## THIS IS REQUIRED. DO NOT LEAVE THIS AS IS OTHERWISE NOTHING WILL WORK!
## Go here: https://www.pushbullet.com/#settings/account (you will need to sign up for a pushbullet account)
## Scroll down to "Access Tokens" then "Create Access Token" copy and paste the resulting code below,
## remembering to keep within the quotes.
## For example (don't use this, it won't work):
## pbAPI = 'o.1234789gbh31byiu3r79'
pbAPI = 'WhateverPushbulletGaveMe'
## Ensure you have the pushbullet app installed on your phone and it's logged in.
## Stop editing now!

def alertUserToOfflineState(tankName , timeOffline):
    pb = Pushbullet(pbAPI)
    my_channel = pb.channels[0]
    pb.push_note("SENEYE OFFLINE WARNING", ("%s has been offline for %d minutes now!" % (tankName, timeOffline)))
    print('Sent pushbullet warning: %s has been offline for %d minutes now!' % (tankName, timeOffline))

url = ('https://api.seneye.com/v1/devices?user=%s&pwd=%s' % (username , password))

# Grab seneye information
seneye = requests.get(url)

# Go through each tank and check we have been online within the last two hours:
for tank in seneye.json():
    url=('https://api.seneye.com/v1/devices/%s?IncludeState=1&user=%s&pwd=%s' % (tank["id"], username, password))
    tankinfo = requests.get(url)
    timeDiff = calendar.timegm(time.gmtime()) - int(tankinfo.json()['status']['last_experiment'])
    if (timeDiff/60) >= offlineAlertTime:
        alertUserToOfflineState(tankinfo.json()['description'] , (timeDiff/60))
    else:
        print('Last update was %d minutes ago. We are not panicking just yet :)' % ((timeDiff/60)))
