# Docker + Telegram Bot Template

aiogram 3 asosidagi Telegram bot, Docker konteynerda ishlaydi.

## Imkoniyatlar

- `/start` — salomlashish va asosiy menyu
- `/help` yoki "ℹ️ Yordam" tugmasi — yordam
- "👤 Men haqimda" — foydalanuvchi ma'lumotlari
- Boshqa matnlarni qaytaradi (echo)

## Docker bilan ishga tushirish

```bash
cp .env.example .env
```

`.env` ichiga bot tokenini yozing:

```bash
docker compose up --build -d
docker compose logs -f bot
```

To'xtatish:

```bash
docker compose down
```

Bot `restart: unless-stopped` bilan ishlaydi, ya'ni xato bo'lsa yoki server qayta yonsa o'zi qayta ishga tushadi.

## Testlar

```bash
pip install -r requirements.txt
pytest
```
