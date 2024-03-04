# Pomodoro-Telegram-Bot
This telegram bot helps you manage your time by setting up timers to stay focused on your tasks

## How to run
* Install and run Docker
* Change the [config.ini](config.ini) file with you value: `BOT_TOKEN`
* Build Docker image using `docker build --tag pomodorobot .`
* Run Docker container using `docker-compose up`
* Once the container is running go to Telegram and send the `/start` command to your bot

## What this bot can do?
* Sets timer from 5 to 120 minutes
* Shows how much time is left, notifies the user when time is up
* Stops current timer
* Repeats last timer
