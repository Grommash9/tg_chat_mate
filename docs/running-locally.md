---
layout: default
title: Running Locally
---

## Description
For development we are able to run it locally without any changes.
You should have docker installed locally!
You should not use `.install.sh` locally because it's only for server deploy really (installing docker and issue ssl certs)

## Install
1. Get and run ngrok
https://ngrok.com/
Dowload and run ngrok it will create external https url for your local bot, so you will be able to run telegram bot on webhook.
You should run it like
```
ngrok http 80
```
Put the domain from ngrok into `DOMAIN` variable.
After ngrok reloading url could be changed and you should change `DOMAIN` variable and rebuild nginx container
```
docker compose up --build nginx -d
```
2. Fill `.env` variables from `.sample.env` example
3. Run it 
```
docker compose up -d
```
4. Rebuild
After making some changes you are able to rebuild only single container using the command
```
docker compose up --build --no-deps -d bot
```
or
```
docker compose up --build --no-deps -d typescript-app
```