---
layout: default
title: Deploy
---

## Description
Main target is to make deploy as simple as it possible for devs

We have all services needed packed in docker compose, for commands for installing docker and docker compose are packed in `install.sh` also if 
you need to issue SSL certificate there it will be issues by code in `install.sh` automatically

## Preparation
1. Getting server
We should use at least 1 CPU 1 RAM. We are storing media files locally so if you are expecting a lot of it make sure you get enough of storage.
2. Domain setting up
If you want to use `Cloudflare` and it will provide you SSL you should just put domain into `DOMAIN` variable in the next step and `ISSUE_SSL` should be false
You are also able to use certbot and domain or even external server ip without domain at all, in both options turn on `ISSUE_SSL`
3. If you are using domain please make sure it is pointing on your server
You can use https://www.nslookup.io/ for it

## Deploy Guide
To install the Tg Chat Mate, follow these steps:
1. Clone the repository:
```
git clone https://github.com/Grommash9/tg_chat_mate
```
2. Navigate to the cloned directory:
```
cd tg_chat_mate
```
3. Create a `.env` file based on the provided example:
```
nano .env
```
Add the environment variables as shown in `.env.example`.

4. Make the `install.sh` script executable and run it:
```
chmod +x install.sh
./install.sh
```

After running these commands, the services should be set up and you can start using the bot.
