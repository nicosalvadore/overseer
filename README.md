# Overseer

## Description

This is a Public IP address checker.

This quick script gets my public IP address using an online service (several can be defined for redundancy).
If the returned public IP is different from the one kept in a local file, it sends me an email using Sendgrid API.

## Prerequisites
- Sendgrid account (free is enough), with an API key.
- Verified sender domain on Sendgrid
- python3

## Installation
    pip3 install -r requirements.txt
    cp .env.example .env

Fill required fields in `.env`

## Usage
`python3 main.py`

On the first run, as the local `ip.log` file isn't available, the script will create it, add the current public IP address to it, and send an email.

On subsequent runs, the script will get the current IP address and compare it with the one stored in `ip.log`. If they are different, it will replace the one in the file with the new one and send an email. If they're identical, nothing happens.

## Logging
`app.log` logs all steps of the script during execution, the log file is created in the same directory. A rotating schedule is set to keep 3 months of logs in `app.log.1-2-3`