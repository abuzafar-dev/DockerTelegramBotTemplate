# Docker + Telegram Bot Template

aiogram 3 bot + Django API + PostgreSQL, uchalasi Docker Compose'da ishlaydi. Bot foydalanuvchidan baho va izoh oladi va uni API orqali bazaga saqlaydi. Natijalarni admin panelda ko'rish mumkin.

## Quick start

```bash
make run     # .env ni to'ldiradi, db + web + bot ni ko'taradi
make admin   # admin panel uchun superuser
make test    # checks + tests (Docker'siz)
```

`.env` dagi `BOT_TOKEN` ga @BotFather'dan olingan tokenni yozing. `SECRET_KEY` va `API_TOKEN` avtomatik yaratiladi.

## Servislar

| Servis | Vazifasi |
|---|---|
| `db` | PostgreSQL 16 |
| `web` | Django API (gunicorn): `POST /api/feedback/`, `GET /api/feedback/stats/`, `/admin/` |
| `bot` | aiogram 3, long polling. Bahoni `http://web:8000/api/feedback/` ga yuboradi |

- Admin: http://127.0.0.1:8002/admin/ (Fikrlar bo'limi)
- Statistika: http://127.0.0.1:8002/api/feedback/stats/

API `X-Api-Token` sarlavhasini tekshiradi: bot va web bitta `API_TOKEN` dan foydalanadi.

## Bot imkoniyatlari

- `/start` — salomlashish va asosiy menyu
- `/help` yoki "ℹ️ Yordam" tugmasi — yordam
- "👤 Men haqimda" — foydalanuvchi ma'lumotlari
- "⭐ Baho berish" yoki `/feedback` — **FSM**: 1–5 yulduz → izoh (yoki o'tkazib yuborish) → bazaga saqlash
- Deep-link / QR: `https://t.me/<bot>?start=filial_3` — `filial_3` manba sifatida saqlanadi
- `/cancel` — har qanday holatdan chiqish
- Boshqa matnlarni qaytaradi (echo)

## Boshqarish

```bash
make logs    # loglar
make down    # to'xtatish
```

Servislar `restart: unless-stopped` bilan ishlaydi.

## Testlar

```bash
make test
```

Django API testlari (`feedbacks/tests.py`) va bot testlari (`tests/`, pytest) ikkalasi ham ishlaydi.
