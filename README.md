## Anonymous Support Bot

<a href="https://wakatime.com/badge/user/d26cd398-7251-4fd1-a726-fb1f96747ca6/project/018bc4dd-87f2-49e0-82d6-3e44d5bd0ee3"><img src="https://wakatime.com/badge/user/d26cd398-7251-4fd1-a726-fb1f96747ca6/project/018bc4dd-87f2-49e0-82d6-3e44d5bd0ee3.svg" alt="wakatime"></a>

## Project Description

Anonymous Support Bot - це комплексне рішення техн підтримки, яке використовує Docker Compose для безперебійної роботи набору сервісів, включаючи MongoDB, Redis, Nginx, бота в Telegram, створеного з Aiogram 3, та веб-інтерфейс на основі TypeScript. Цей проєкт спрощує процес інтеграції бота техн підтримки, дозволяючи клієнтам надсилати повідомлення безпосередньо до бота в Telegram. Повідомлення можна моніторити та відповідати на них через веб-інтерфейс.

The Anonymous Support Bot is a comprehensive support solution that leverages Docker Compose to seamlessly run a suite of services including MongoDB, Redis, Nginx, a Telegram bot built with Aiogram 3, and a TypeScript-based web UI service. This project simplifies the process of integrating a support bot into your server, allowing customers to send messages directly to the Telegram bot. The messages can be monitored and responded to through a web-based UI interface.


## Technical Debt

- Refactor Cloudflare Nginx logic.
- Create scripts for dumping and loading data for MongoDB.
- Implement lazy loading for new messages and chats upon scrolling instead of loading all at once.
- Establish a testing strategy and framework.

## Next Steps

- Implement authentication mechanisms for manager and root roles within the UI.
- Enhance media storage in MongoDB within the messages collection.
  - Add logic for handling different Telegram media types for sending and receiving.
  - Integrate storage of customer photos in the MongoDB users collection and display them in the UI.
- Create a mobile-responsive version of the UI.
- Allow root users to create manager accounts through the UI.
  - Set up tracking of managers' working hours.
  - Link managers' accounts to their Telegram accounts for receiving notifications about new messages.
  - Consider automatic assignment of managers to new chats.
- Add a mass messaging feature accessible from the bot, the UI, or both.
- Capture `start_param` from the bot initiation and store it in the MongoDB user collection as an extra field, e.g., `{"start_param": "facebook"}`.
- Implement search functionality for chat names, chat messages, and user custom fields.
- Design a pre-conversation questionnaire for customers on Telegram with optional storage of responses in user collection extra fields, e.g., `{"phone": "+4407308483234"}`.


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

