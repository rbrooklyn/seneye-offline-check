# seneye-offline-check
This is a small python script to check if your Seneye tank monitoring system hasn't uploaded readings in a while
This is a small simple python script that will check if your Seneye has not uploaded a reading for a while, and will alert you, via PushBullet, if the latest reading is more than X minutes old.
## Background - What is Seneye and how this script helps:
The Seneye is a aquarium monitor solution that will test your aquarium's water quality, and upload those results to Seneye's servers. This works in both freshwater and saltwater aquariums, heated and unheated. When the water parameters go outside a 'safe' range, the Seneye system will warn you with an email and/or text messages to your phone to allow you to take remedial action. You can find more about the Seneye system here: https://www.seneye.com/

However, a problem exists where the Seneye aquarium 'dongle' may fail in some fashion, the Seneye uploading software may crash, freeze, or otherwise fail, or the host PC or 'Seneye bridge' device may also fail in some fashion. In this state, Seneye's systems may no longer receive updated data, so a degradation of the water conditions may go unnoticed. This script is an attempt to help mitigate that issue.

PushBullet is a service which allows you to synchronise messages between devices (text messages between your phone and your tablet, for example), and also allows you to send messages to yourself with the built in API, which this script takes advantage of. This script requires that you have a PushBullet account set up, and that PushBullet is installed and configured on whatever devices you want to have the alerts sent to. There is a paid ‘pro’ tier, but the free tier should be more than sufficient for our needs. You can learn more about PushBullet here: https://www.pushbullet.com/

This script will ask Seneye's servers directly the state of the latest batch of data that they hold about your aquarium. Seneye's servers will reply with all the data about the aquariums that are known to it, including, crucially, the latest date and time of the information it holds. The script will then check if the data is X minutes old (you define whatever X is) and will send a PushBullet notification to your mobile device, warning you to check the Seneye computer/dongle/software to ensure that new readings are being uploaded.

You do not have to run the script on the same machine as the Seneye is running from. In fact it’s recommended that you do not. In fact, you can even run it from a server or machine that is nowhere near your network if you prefer, as it contacts the Seneye servers directly for it’s information. You can use a cloud provider such as RackSpace, or Amazon’s AWS service (which is free for the first year) to run this on if you prefer.

## Background and why this script is a temporary solution
After a incident where I lost some livestock, of course some bad luck my Seneye had not been uploading for four days, I created this script.

After the incident, I complained to Seneye that the device and/or software obviously should never have broken in the first place,  Seneye suggested that "some times a router can crash or change configuration which throws it off", which in my case was untrue, and it actually required the Seneye dongle to be physically removed from the machine, even rebooting it didn't fix the issue.

Never again. So I wrote this script.

I also complained to Seneye support that this is a huge flaw in the design of their systems; that a system can fail, even if it’s not Seneye’s fault, and the user may be blissfully unaware of the situation. Seneye have informed me that they are working on such a feature. So this script is nothing more than a temporary solution to the problem.

As usual, the Seneye and this script are not a replacement for good aquarium maintenance. This is just another tool in the good fish-keeper's arsenal, and should be treated as such; it’s not a silver bullet and it should never be considered to be one.

## Installation and usage

This is a fairly basic python script. So you need to have a python environment set up to use it. I have not tested this on Windows, and I am unsure how to set up a python environment on Windows systems. The only Windows machine I have running is managing my Seneye, and installing this script on the same machine is a bad idea. I welcome instructions for Windows users if anybody is able to write them.

The script is tested on a Ubuntu 16.04 and Raspbian 7 (wheezy) (although I’d suggest a newer version of Raspbian if possible, as installation is difficult on this platform due it to using older libraries).

I strongly recommend that you run this script on a different psychical machine to the one that is running on Seneye. As if the the machine managing the Seneye fails for some reason, you will never get notified.

The script will check the Seneye's systems “there and then” in the moment that it is run. It will not run in the background constantly checking the Seneye for you. You will have to use whatever task scheduling solution is provided by your operating system to run the script every hour or so.

Instructions to install on a fresh Ubuntu 16.04 machine are below. The instructions will be similar on Debian and other Linux based systems. In the terminal:

Install dependencies in the terminal that are provided by Ubuntu:

`sudo apt install python3 python3-requests python3-pip`

And install the dependencies not provided by Ubuntu, but provided by pip. Sudo is not required here:

`pip3 install pushbullet.py`

Now get the seneye-offline-check.py into your machine if you haven’t already:

`wget https://raw.githubusercontent.com/ribs85/seneye-offline-check/master/seneye-offline-check.py`

Make it executable (optional):

`chmod +x seneye-offline-check.py`

And now configure it. This is not optional, you MUST configure this script otherwise it will not work.

graphical editor:

`gedit seneye-offline-check.py`

or terminal editor:

`nano -w seneye-offline-check.py`

If you’ve never used nano before, a basic guide is here: https://wiki.gentoo.org/wiki/Nano/Basics_Guide

You need to edit the username, password, offlineAlertTime and pbAPI:

username is the username that you use to sign into the Seneye website

password is the password that you use to sign into the Seneye website

offlineAlertTime is the amount of minutes that the script will allow before warning you that the data is stale. If you are testing the script, set this to one. Once you have verified the script is working, set it to something at least 31 (preferably at least 60 minutes), as the Seneye uploads every 30 minutes or so.

pbAPI is the PushBullet API key. You can get this from your PushBullet account by going to the settings link here: then click “Create Access Token”, you have to copy and paste this string exactly as the website gives it to you into the file. An error here or skipping this step will render the script useless.

Your final edits should look something like this, I have removed the comments (lines beginning with a #) from the file for brevity:

```username = 'me@myemail.com' 
password = 'myPassword' 
offlineAlertTime = 0 
pbAPI = 'o.WhateverPushbulletGaveMe' ```

Notice offlineAlertTime is 0, this is for testing only.

Now we test the script:
If you made it executable earlier:

`./seneye-offline-check.py`

or if you didn’t:

`python3 seneye-offline-check.py`

You should then get a warning for each tank you own:
Sent PushBullet warning: TANKNAME has been offline for 24 minutes now!

And you should get a warning on your mobile device as well:

SENEYE OFFLINE WARNING
TANKNAME has been offline for 24 minutes now!

Don’t keep running the script too often, as you will use up all of your PushBullet messages on the free tier. You only get 100 a month at the time of writing. Running too often may upset Seneye as well.

Once your are convinced this is working, you can change the  offlineAlertTime to a more sane value. I use 240 minutes, which is four hours. This gives Seneye a chance to fix whatever is happening in case it’s just a temporary outage:

offlineAlertTime = 240

Test again:
Last update was 25 minutes ago. We are not panicking just yet :)

## Schedule the script to run.

You may have noticed the script only checks that one time. This isn’t much help as you need it to keep checking Seneye’s systems regularly. To do this, we’ll ask Ubuntu to run this script every hour for us.

Edit your user’s cron:

`crontab -e`

It may ask you to select a editor, I suggest using 2, which is nano. If you’ve never used nano before, a basic guide is here: https://wiki.gentoo.org/wiki/Nano/Basics_Guide

The file is well commented to explain it’s format. At the end of the file, you can add the following line if you made it executable:

`0 * * * * /home/YOURUSERNAME/seneye-offline-check.py`

or 

`0 * * * * python3 /home/YOURUSERNAME/seneye-offline-check.py`

if you didn’t.

Obviously replace /home/YOURUSERNAME/seneye-offline.check.py with the actual path of the script.

You may want to change offlineAlertTime to 0 again, and waiting for the beginning of the new hour, just as one last check to ensure it’s all working, then change it back.

Installation is complete at this stage.

## Errors:

The script is very small and basic, and doesn't have great error reporting at this stage.

If you get the following:

```Traceback (most recent call last):                                                                                                                          
  File "./seneye-online.py", line 36, in <module>                                                                                                           
    url=('https://api.seneye.com/v1/devices/%s?IncludeState=1&user=%s&pwd=%s' % (tank["id"], username, password))                                           
TypeError: string indices must be integers```

Your username and/or password is wrong.

If you get this:

```Traceback (most recent call last):
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
pushbullet.errors.InvalidKeyError```

Your pbAPI value is incorrect.

## Changing how the script works, for python programmers and advanced users that want to change the script.
This script is open source, licenced under the GPL version 3. You are free to edit the script as you see fit.

The portion that decides what should happen when the user should be alerted can be found in the “alertUserToOfflineState” def. You can maybe change this to send a email, or a text message, maybe remotely reboot the Seneye managing machine, whatever you like.
