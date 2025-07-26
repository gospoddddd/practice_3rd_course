# practice_3rd_course

**RU | EN below**

## Цель
Демо-проект «программно‑аппаратного комплекса» на Windows (Docker Desktop + WSL2) с упором на **CI/CD в Jenkins**.  
Data Quality сведён к заглушке (Great Expectations + Postgres). Всё — в коде и в репозитории: Docker Compose, Jenkins (JCasC), пайплайн, приложение.

## Что внутри
- Jenkins в Docker, конфигурация через **JCasC** (админ, URL, seed‑job, плагины).
- Пайплайн `Jenkinsfile`: checkout → lint/test → GE‑заглушка → build/push образа в **локальный Registry** → **ручной апрув** → deploy в `docker-compose.prod.yml`.
- **Telegram**: установлен плагин `telegram-notifications`; в пайплайне используется `telegramSend` (если плагин сконфигурирован) и **fallback** через Telegram Bot API (curl).
- Приложение (`app/`): Python ETL → Postgres. Образ собирается и деплоится.
- Секреты: **.env (локально, не коммитим)**; пример — `.env.example`.

## Быстрый старт (Windows 10/11)
1. Установите Docker Desktop (WSL2).
2. Склонируйте репозиторий и создайте `.env`:
   ```powershell
   copy .env.example .env
   notepad .env   # укажите GIT_REPO_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
   ```
3. Запустите всё одной командой:
   ```powershell
   .\scripts\start.ps1
   ```
4. Откройте Jenkins: http://localhost:8080  
   Логин/пароль — из `.env` (по умолчанию admin/admin123). Seed‑job **practice_3rd_course** уже создан (JCasC).
5. Запустите job вручную. На шаге **Approval** подтвердите деплой.

### Замечания по Telegram
- Плагин **Telegram Bot** (`telegram-notifications`) установлен. Глобальная конфигурация плагина через JCasC не документирована официально, поэтому по умолчанию пайплайн шлёт уведомления через **curl** (Bot API) с использованием переменных `TELEGRAM_*` из `.env`.
- Если настроите плагин вручную в Jenkins (Manage Jenkins → Configure System), шаг `telegramSend` начнёт работать без fallback.
- У плагина отмечена проблема хранения токена в открытом виде (см. страницу плагина). Храните токен только в `.env` и не коммитьте его.

## Секреты и переменные
- Храните реальные значения в `.env` (не коммитим). В репозитории есть `.env.example`.
- Пример значений:
  ```env
  JENKINS_ADMIN_ID=admin
  JENKINS_ADMIN_PASSWORD=admin123
  JENKINS_URL=http://localhost:8080
  GIT_REPO_URL=https://github.com/<you>/practice_3rd_course.git
  GIT_BRANCH=main
  TELEGRAM_BOT_TOKEN=xxxx
  TELEGRAM_CHAT_ID=123456789
  REGISTRY_HOST_FROM_JENKINS=host.docker.internal:5000
  REGISTRY_HOST_FROM_HOST=localhost:5000
  POSTGRES_DB=demo
  POSTGRES_USER=demo
  POSTGRES_PASSWORD=demo123
  POSTGRES_PORT=5432
  APP_DB_TABLE=demo_data
  ```

## Как это работает
- **docker-compose.yml** поднимает: `jenkins`, `postgres`, `registry`.
- Jenkins запускается с JCasC (`jenkins/casc/jenkins.yaml`), создаёт job `practice_3rd_course`, указывающий на ваш GitHub‑репозиторий и `Jenkinsfile`.
- Пайплайн строит образ `localhost:5000/practice_3rd_course/app:<git-sha>` и пушит его в локальный реестр.
  - Из Jenkins (в контейнере) реестр доступен как `host.docker.internal:5000`.
  - Из вашего хоста — как `localhost:5000`.
- На деплое запускается `docker-compose.prod.yml` c переменной `APP_IMAGE=...`.

## Проверка DQ (минимальная заглушка)
Скрипт `app/dq/check_ge.py` извлекает до 1000 строк из таблицы и проверяет простые ожидания (наличие колонки, число строк > 0) через **Great Expectations (legacy API)**. Любые ошибки в заглушке **не валят** пайплайн.

## Частые проблемы
- **Плагин Telegram**: если не сконфигурирован — будет использоваться fallback через curl.
- **Недоступен Docker из Jenkins**: проверьте, что смонтирован `/var/run/docker.sock` и установлен `docker.io` в образе Jenkins.
- **GIT_REPO_URL**: укажите ваш URL после пуша репозитория на GitHub.

---

## EN

### Goal
Windows‑friendly demo of a CI/CD system (Jenkins + Docker Desktop) with a tiny data‑quality placeholder (GE + Postgres). Everything is code: Docker Compose, JCasC, pipeline, app.

### What’s included
- Jenkins configured via **JCasC** (admin, URL, seed job, plugins).
- Pipeline: checkout → lint/test → GE placeholder → build/push to local **Registry** → **manual approval** → deploy with `docker-compose.prod.yml`.
- **Telegram** notifications: plugin installed; pipeline uses `telegramSend` if available and falls back to Bot API via `curl`.
- Secrets in local `.env` (kept out of Git).

### Quick start
```
copy .env.example .env
# fill .env (GIT_REPO_URL, TELEGRAM_*)
.\scripts\start.ps1
# Open http://localhost:8080 and run the job
```

### Secrets
Use `.env` locally. See `.env.example` for fields.

### Notes
- This repo is optimized for **Windows + Docker Desktop**.
- The Telegram plugin stores token in plaintext in its global config; keep your token only in `.env` if you use the curl fallback.
