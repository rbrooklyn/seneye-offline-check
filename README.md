# seneye-offline-check
This is a small python script to check if your Seneye tank monitoring system hasn't uploaded readings in a while
This is a small simple python script that will check if your Seneye has not uploaded a reading for a while, and will alert you, via PushBullet, if the latest reading is more than X minutes old.
## Background - What is Seneye and how this script helps:
The Seneye is a aquarium monitor solution that will test your aquarium's water quality, and upload those results to Seneye's servers. This works in both freshwater and saltwater aquariums, heated and unheated. When the water parameters go outside a 'safe' range, the Seneye system will warn you with an email and/or text messages to your phone to allow you to take remedial action. You can find more about the Seneye system here: https://www.seneye.com/

However, a problem exists where the Seneye aquarium 'dongle' may fail in some fashion, the Seneye uploading software may crash, freeze, or otherwise fail, or the host PC or 'Seneye bridge' device may also fail in some fashion. In this state, Seneye's systems may no longer receive updated data, so a degradation of the water conditions may go unnoticed. This script is an attempt to help mitigate that issue.

PushBullet is a service which allows you to synchronise messages between devices (text messages between your phone and your tablet, for example), and also allows you to send messages to yourself with the built in API, which this script takes advantage of. This script requires that you have a PushBullet account set up, and that PushBullet is installed and configured on whatever devices you want to have the alerts sent to. There is a paid ‘pro’ tier, but the free tier should be more than sufficient for our needs. You can learn more about PushBullet here: https://www.pushbullet.com/

This script will ask Seneye's servers directly the state of the latest batch of data that they hold about your aquarium. Seneye's servers will reply with all the data about the aquariums that are known to it, including, crucially, the latest date and time of the information it holds. The script will then check if the data is X minutes old (you define whatever X is) and will send a PushBullet notification to your mobile device, warning you to check the Seneye computer/dongle/software to ensure that new readings are being uploaded.

You do not have to run the script on the same machine as the Seneye is running from. In fact it’s recommended that you do not. In fact, you can even run it from a server or machine that is nowhere near your network if you prefer, as it contacts the Seneye servers directly for it’s information. You can use a cloud provider such as RackSpace, or Amazon’s AWS service (which is free for the first year) to run this on if you prefer.

## Background
After a incident where I lost some livestock, of course some bad luck my Seneye had not been uploading for four days, I created this script.

After the incident, I complained to Seneye that the device and/or software obviously should never have broken in the first place,  Seneye suggested that "some times a router can crash or change configuration which throws it off", which in my case was untrue, and it actually required the Seneye dongle to be physically removed from the machine, even rebooting it didn't fix the issue. I have also experienced several failures where the software simply stops uploading test data to Seneye for seemingly no reason.

Never again. So I wrote this script.

I also complained to Seneye support that this is a huge flaw in the design of their systems; that a system can fail, even if it’s not Seneye’s fault, and the user may be blissfully unaware of the situation. Seneye have informed me that they are working on such a feature, but unforuntately only for the 'web server' product, which is something I do not need and refuse to pay for, for what I consider should be a feature for all their customers. I have feedback my feelings but I'm not expecting a change in policy.

As usual, the Seneye and this script are not a replacement for good aquarium maintenance. This is just another tool in the good fish-keeper's arsenal, and should be treated as such; it’s not a silver bullet and it should never be considered to be one.

## Installation and usage

The Dockerfile can be used to build a image for a docker installation.

The following environment settings need to be provided:

SENEYE_USERNAME - This is probably your email address. Required.

SENEYE_PASSWORD - Whatever your password is to login to the seneye.me website. Required.

OFFLINE_ALERT_MINUTES - How many minutes where no update has been seen before sending pushbullet notification. Optional, defaults to 240 (4 hours)

PUSHBULLET_API_KEY - The API key from the pushbullet website. Required.

The script will run every 4 hours: at midnight, 4am, 8am, 12pm, 4pm, 8pm. If the script, at that exact point, sees that your Seneye's latest readings are over the value given in OFFLINE_ALERT_MINUTES (set above), then a pushbullet notification will be sent, warning of the situation.

As the script checks every 4 hours, it might be some time before a notification is sent. This is to prevent constant notifications being sent throughout the day if something does go wrong and using up all the pushbullet notifications on the free tier. This can be adjusted by using your own crontab file, and setting the OFFLINE_ALERT_MINUTES setting to a lower value. Just be careful if you're planning to do this.

The Dockerfile will automatically download the seneye-offline-check.py and crontab files from my Github. There is a comment in the file which you can remove in order to use local files instead if this is desired. If you do this, remember to comment out the wget lines as well.

## Errors:

The script is very small and basic, and doesn't have great error reporting at this stage.

If you get the following:

```
Traceback (most recent call last):                                                                                                                          
  File "./seneye-online.py", line 36, in <module>                                                                                                           
    url=('https://api.seneye.com/v1/devices/%s?IncludeState=1&user=%s&pwd=%s' % (tank["id"], username, password))                                           
TypeError: string indices must be integers
```

Your username and/or password is wrong.

If you get this:

```
Traceback (most recent call last):
  File "seneye-online.py", line 40, in <module>
    alertUserToOfflineState(tankinfo.json()['description'] , (timeDiff/60))
  File "seneye-online.py", line 24, in alertUserToOfflineState
    pb = Pushbullet(pbAPI)
  File "/usr/local/lib/python3.5/dist-packages/pushbullet/pushbullet.py", line 29, in __init__
    self.refresh()
  File "/usr/local/lib/python3.5/dist-packages/pushbullet/pushbullet.py", line 288, in refresh
    self._load_devices()
  File "/usr/local/lib/python3.5/dist-packages/pushbullet/pushbullet.py", line 42, in _load_devices
    resp_dict = self._get_data(self.DEVICES_URL)
  File "/usr/local/lib/python3.5/dist-packages/pushbullet/pushbullet.py", line 35, in _get_data
    raise InvalidKeyError()
pushbullet.errors.InvalidKeyError
```

Your pbAPI value is incorrect.

## Changing how the script works, for python programmers and advanced users that want to change the script.
This script is open source, licenced under the GPL version 3. You are free to edit the script as you see fit.

The portion that decides what should happen when the user should be alerted can be found in the “alertUserToOfflineState” def. You can maybe change this to send a email, or a text message, maybe remotely reboot the Seneye managing machine, whatever you like.
