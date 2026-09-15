# Docker Telegram Bot Template

A minimal, Dockerized [aiogram 3](https://docs.aiogram.dev/) Telegram bot template.

## Structure

```
├── bot/
│   ├── config.py          # loads BOT_TOKEN from .env
│   ├── dispatcher.py      # aiogram Dispatcher instance
│   └── handlers/
│       ├── __init__.py    # registers handler modules
│       └── main.py        # /start handler
├── main.py                # entrypoint, starts polling
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Setup

1. Copy `.env.example` to `.env` and set your bot token (get one from [@BotFather](https://t.me/BotFather)):

   ```
   BOT_TOKEN=your-token-here
   ```

2. Run it:

   ```
   docker compose up --build
   ```

## Adding handlers

Add a new module under `bot/handlers/`, import it in `bot/handlers/__init__.py`, and register handlers on the shared `dp` from `bot/dispatcher.py`.
