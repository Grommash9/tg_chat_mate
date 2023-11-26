## Anonymous Support Bot

<a href="https://www.buymeacoffee.com/andreevich0" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

<a href="https://wakatime.com/badge/github/Grommash9/anonymous_support_bot"><img src="https://wakatime.com/badge/github/Grommash9/anonymous_support_bot.svg" alt="wakatime"></a>

## Project Description

Anonymous Support Bot - це комплексне рішення техн підтримки, яке використовує Docker Compose для безперебійної роботи набору сервісів, включаючи MongoDB, Redis, Nginx, бота в Telegram, створеного з Aiogram 3, та веб-інтерфейс на основі TypeScript. Цей проєкт спрощує процес інтеграції бота техн підтримки, дозволяючи клієнтам надсилати повідомлення безпосередньо до бота в Telegram. Повідомлення можна моніторити та відповідати на них через веб-інтерфейс.

The Anonymous Support Bot is a comprehensive support solution that leverages Docker Compose to seamlessly run a suite of services including MongoDB, Redis, Nginx, a Telegram bot built with Aiogram 3, and a TypeScript-based web UI service. This project simplifies the process of integrating a support bot into your server, allowing customers to send messages directly to the Telegram bot. The messages can be monitored and responded to through a web-based UI interface.


## Installation Guide
To install the Anonymous Support Bot, follow these steps:
1. Clone the repository:
```
git clone https://github.com/Grommash9/anonymous_support_bot
```
2. Navigate to the cloned directory:
```
cd anonymous_support_bot
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

