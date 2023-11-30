## Anonymous Support Bot

<a href="https://wakatime.com/badge/github/Grommash9/anonymous_support_bot"><img src="https://wakatime.com/badge/github/Grommash9/anonymous_support_bot.svg" alt="wakatime"></a>

## Project Description
🇺🇦🇺🇦🇺🇦
Anonymous Support Bot - це комплексне рішення техн підтримки. Цей проєкт спрощує процес інтеграції бота техн підтримки, дозволяючи клієнтам надсилати повідомлення безпосередньо до бота в Telegram. Повідомлення можна моніторити та відповідати на них через веб-інтерфейс.
Хоча код доступний публічно, ми пропонуємо преміальні консультаційні та інсталяційні послуги для підприємств, які шукають персоналізовану підтримку. Для отримання додаткової інформації щодо наших комерційних послуг, будь ласка, зв'яжіться з [PydevTeam](https://t.me/PydevTeam)

🇬🇧🇬🇧🇬🇧
The Anonymous Support Bot is a comprehensive support solution that leverages Docker Compose to seamlessly run a suite of services including MongoDB, Redis, Nginx, a Telegram bot built with Aiogram 3, and a TypeScript-based web UI service. This project simplifies the process of integrating a support bot into your server, allowing customers to send messages directly to the Telegram bot. The messages can be monitored and responded to through a web-based UI interface.
While the source code is freely available, we offer premium consulting and installation services for businesses seeking personalized support. For more information on our commercial services, please contact [PydevTeam](https://t.me/PydevTeam)

## Installation Guide
To install the Anonymous Support Bot, follow these steps:
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

