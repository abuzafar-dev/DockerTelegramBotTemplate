.PHONY: help install run test down logs admin env

help:
	@echo "make run      — Docker'da ishga tushirish: bot + API + PostgreSQL"
	@echo "make admin    — admin panel uchun superuser (http://127.0.0.1:8002/admin/)"
	@echo "make down     — to'xtatish"
	@echo "make logs     — loglar"
	@echo "make test     — testlar (Docker'siz)"

env:
	@python3 scripts/sync_env.py

run: env
	@grep -q '^BOT_TOKEN=.\+' .env || { echo "XATO: .env faylida BOT_TOKEN bo'sh. @BotFather'dan token olib yozing."; exit 1; }
	@echo "==> admin: http://127.0.0.1:8002/admin/   statistika: http://127.0.0.1:8002/api/feedback/stats/"
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

admin:
	docker compose exec web python manage.py createsuperuser

PY := .venv/bin/python

.venv/bin/python:
	@if command -v uv >/dev/null 2>&1; then uv venv -q --python 3.12 .venv; else python3 -m venv .venv; fi

.venv/.installed: requirements.txt | .venv/bin/python
	@echo "==> kutubxonalar o'rnatilmoqda"
	@if command -v uv >/dev/null 2>&1; then uv pip install -q -p $(PY) -r requirements.txt; else $(PY) -m pip install -q -r requirements.txt; fi
	@touch $@

install: .venv/.installed

test: install
	@POSTGRES_DB= bash scripts/ci.sh
