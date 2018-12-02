FROM ubuntu:bionic
LABEL Description="Send pushbullet notification if Seneye data is out of date" Version="1.0"
ENV SENEYE_USERNAME x
ENV SENEYE_PASSWORD x
ENV OFFLINE_ALERT_MINUTES 240
ENV PUSHBULLET_API_KEY x
ADD . /seneye
WORKDIR /seneye
RUN apt update
RUN apt dist-upgrade -y
RUN apt install -y --no-install-recommends python3-minimal python3-requests python3-pip wget cron
RUN pip3 install pushbullet.py

## Uncomment to use local files:
#COPY seneye-offline-check.py /seneye/seneye-offline-check.py
#COPY crontab /etc/cron.d/seneye

## Uncomment to use github files:
RUN wget https://raw.githubusercontent.com/rbrooklyn/seneye-offline-check/master/seneye-offline-check.py -O /seneye/seneye-offline-check.py
RUN wget https://raw.githubusercontent.com/rbrooklyn/seneye-offline-check/master/crontab -O /etc/cron.d/seneye

RUN chmod 0644 /etc/cron.d/seneye

CMD ["cron","-f"]
