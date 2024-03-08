# Pomodoro-Telegram-Bot
This telegram bot helps you manage your time by setting up timers to stay focused on your tasks

* [How to run](#how-to-run)
* [How to run without Docker](#how-to-run-without-docker)
* [What this bot can do?](#what-this-bot-can-do)

## How to run
* Clone git repository
* Change the [config.ini](config.ini) file with you value: `BOT_TOKEN`
* Install and run [Docker](https://www.docker.com/)
* Build Docker image and run Docker container using those commands
```
docker build --tag pomodorobot .
docker-compose up
```
* Once the container is running go to Telegram and send the `/start` command to your bot

## How to run without Docker
* Create the virtual environment
* Run those commands
```
pip install -r requirements.txt
python main.py
```

## What this bot can do?
* Sets timer from 5 to 120 minutes
* Shows how much time is left, notifies the user when time is up
* Stops current timer
* Repeats last timer
