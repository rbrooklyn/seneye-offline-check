#!/usr/bin/python
import json, requests, calendar, time
from pushbullet import Pushbullet

# User configured parts:
username = os.environ['SENEYE_USERNAME']
password = os.environ['SENEYE_PASSWORD']
offlineAlertTime = os.environ['OFFLINE_ALERT_MINUTES']
pbAPI = os.environ['PUSHBULLET_API_KEY']

# def which sends pushbullet alert if needed:
def alertUserToOfflineState(tankName , timeOffline):
    pb = Pushbullet(pbAPI)
    my_channel = pb.channels[0]
    pb.push_note("SENEYE OFFLINE WARNING", ("%s has been offline for %d minutes now!" % (tankName, timeOffline)))
    print('Sent pushbullet warning: %s has been offline for %d minutes now!' % (tankName, timeOffline))

url = ('https://api.seneye.com/v1/devices?user=%s&pwd=%s' % (username , password))

# Grab seneye information
seneye = requests.get(url)

# Go through each tank and check we have been online within the last X minutes (X defined by offlineAlertTime):
for tank in seneye.json():
    url=('https://api.seneye.com/v1/devices/%s?IncludeState=1&user=%s&pwd=%s' % (tank["id"], username, password))
    tankinfo = requests.get(url)
    timeDiff = calendar.timegm(time.gmtime()) - int(tankinfo.json()['status']['last_experiment'])
    if (timeDiff/60) >= offlineAlertTime:
        alertUserToOfflineState(tankinfo.json()['description'] , (timeDiff/60))
    else:
        print('Last update was %d minutes ago. We are not panicking just yet :)' % ((timeDiff/60)))
