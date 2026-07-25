# T45 · Каркас мікро-MVP: файли і зміст

`2026-07-25` · 💡 proposal

Контекст:
- план задачі — [T44](T44--auth-mvp/plan.md); рішення з чату 2026-07-25: теки `api`/`vue` (замість backend/frontend), правило дрібних файлів;
- уточнення до [T44](T44--auth-mvp/plan.md): `.env` живе в `app/api/.env` (в [T43](T43-C--gcp-oauth-setup.md) згадувався `app/backend/.env` — тека перейменована).

## Дерево

```
app/
├─ README.md               # запуск: 3 команди (mongod вже є, uv, npm)
├─ api/                    # FastAPI-бекенд (uv-проєкт)
│  ├─ pyproject.toml       # deps: fastapi[standard], beanie, authlib, pydantic-settings, itsdangerous
│  ├─ .env.example         # шаблон: усі змінні з коментарями
│  ├─ .env                 # секрети (git-ignored)
│  ├─ main.py              # створення app: SessionMiddleware, lifespan (init_db), підключення роутерів
│  ├─ config.py            # Settings (pydantic-settings): mongo_uri, db_name, google_*, session_secret, admin_emails
│  ├─ db.py                # init_db(): async-клієнт PyMongo + ініціалізація Beanie з моделями
│  ├─ deps.py              # current_user: дістає юзера з сесії (для /api/me і майбутніх роутів)
│  ├─ models/
│  │  └─ user.py           # Status (enum: pending/student/admin) + User(Document)
│  └─ routes/
│     ├─ auth.py           # /api/auth/login · /api/auth/callback · /api/auth/logout
│     └─ me.py             # /api/me → юзер або null
└─ vue/                    # Vue 3 SPA (Vite)
   ├─ package.json         # deps: vue, vue-router, bootstrap
   ├─ vite.config.js       # plugin vue + proxy /api → http://localhost:8000
   ├─ index.html
   └─ src/
      ├─ main.js           # createApp + router + імпорт bootstrap css
      ├─ App.vue           # <NavBar/> + <RouterView/>
      ├─ router.js         # маршрути: / → HomePage (майбутні сторінки додаються сюди)
      ├─ api.js            # fetch-обгортка: getMe(), logout()
      ├─ user.js           # composable useUser(): ref поточного юзера + load()
      ├─ components/
      │  └─ NavBar.vue     # назва-лінк + «Увійти з Google» / аватар, імʼя, «Вийти»
      └─ pages/
         └─ HomePage.vue   # анонім: текст-заглушка + заклик увійти; залогінений: статус
```

Орієнтир: жоден файл не більший за ~60–80 рядків; api — 9 файлів, vue — 9.

## Ключові файли — що всередині

- **`config.py`** — один клас `Settings`, все з `.env`; `admin_emails` — список через кому. Жодних інших джерел конфігурації.
- **`models/user.py`** — `User(Document)`: `email` (Indexed, unique), `name`, `picture`, `status: Status = pending`, `created_at`. Уся «схема БД» проєкту — цей файл.
- **`routes/auth.py`** — серце задачі (~50 рядків): `login` → redirect на Google (Authlib, `hd=nure.ua` як підказка); `callback` → перевірка `email_verified` і (`hd == nure.ua` або email в `admin_emails`) → upsert User (адмін-email одразу отримує `status=admin`) → email у сесію-cookie → redirect на `/`; не-nure.ua → redirect на `/?error=domain`; `logout` → чистить сесію.
- **`routes/me.py`** — віддає юзера з сесії або `null`; фронт цим визначає стан.
- **`NavBar.vue`** — Bootstrap navbar: зліва назва, справа «Увійти з Google» (звичайний `<a href="/api/auth/login">`) або аватар + імʼя + «Вийти».
- **`HomePage.vue`** — анонім: «Це майбутня система для лабораторних… Щоб отримати доступ, авторизуйтесь поштою @nure.ua»; `?error=domain` → підказка «лише пошта nure.ua»; залогінений `pending`: «Ти в списку; доступ надає викладач»; `student`/`admin` — поки просто бейдж статусу.
- **`CLAUDE.md` (корінь репо)** — правила для агентів, чернетка:
  - код лаконічний і максимально зрозумілий, «ніби писав сам Vitalik»: мінімум шарів, магії та залежностей;
  - дрібні файли: один файл — одна відповідальність, орієнтир ≤ ~80 рядків; виріс — розбити;
  - код/ідентифікатори/коментарі — EN; UI-тексти — UA; відповіді в чаті — UA;
  - коментарі лише там, де код сам не пояснює «чому»;
  - робоча памʼять проєкту — `.dev/` (спека, тікети, статус).

## Запуск у PyCharm

- Відкрити коренем **весь репо** (`.dev/` поруч із кодом — зручно для тікетів).
- Інтерпретатор: uv-середовище з `app/api` (PyCharm ≥2024.2 підтримує uv нативно: Add Interpreter → uv).
- Run-конфігурації:
  - **api**: у Pro є готовий тип «FastAPI» (вказати `app/api/main.py`); універсально — конфігурація module `uvicorn`, параметри `main:app --reload --port 8000`, working dir `app/api`. `.env` підхоплює pydantic-settings — окремий EnvFile-плагін не потрібен;
  - **vue**: npm-конфігурація `dev` з `app/vue/package.json` (у Community JS-підтримки нема — тоді `npm run dev` у вбудованому терміналі);
  - **Compound «app»**: api + vue разом — одна кнопка ▶ запускає все (mongod і так висить сервісом).

## Без секретів

- Весь код пишеться і працює без Google-секретів; реальний вхід — єдине, що не перевірити.
- Опційно (питання в [T46](T46-Q--pre-code-questions.md)): dev-вхід без Google — `FAKE_USER_EMAIL` у `.env` вмикає кнопку «Dev-вхід» (~5 рядків у auth.py, працює лише локально, у проді змінна відсутня). Дає розробку UI, не чекаючи GCP.

## Твої думки та питання

> 
