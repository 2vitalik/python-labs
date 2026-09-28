# app — Python Labs (мікро-MVP)

- `api/` — FastAPI-бекенд (uv, MongoDB/Beanie, Google OAuth)
- `vue/` — Vue 3 SPA (Vite, Bootstrap 5)

## Перший запуск

1. локальний `mongod` має працювати;
2. `cd app/api && cp .env.example .env` — вписати Google-креди ([інструкція](../.dev/platform/.t/T43-C--gcp-oauth-setup.md)), `SESSION_SECRET` (`openssl rand -hex 32`) і свою пошту в `ADMIN_EMAILS`;
3. `cd app/api && uv sync`;
4. `cd app/vue && npm install`.

## Дев-запуск

Порти — №3 у крос-проєктній схемі (`dev-md-rules/DEV.md`): API 8030, фронт 5030.

- бекенд: `cd app/api && uv run fastapi dev --port 8030` → http://localhost:8030
- фронт: `cd app/vue && npm run dev` → **http://localhost:5030** (відкривати цю адресу)
- дев-вхід без Google: кнопка «Dev-вхід» у шапці (працює, якщо в `.env` заданий `FAKE_USER_EMAIL`); закрита сторінка без входу веде на `/login?next=…` і повертає туди після входу
- «Очима студента»: студент із галочкою «Тестовий студент» (`/students/<нік>/edit`) отримує кнопку 👁 — адмін дивиться сайт як він, «Повернутись» у жовтій смужці; на сервері це заміна dev-входу
- смоуки API (без Google): `cd app/api && DB_NAME=python_labs_smoke uv run python tests/smoke_auth.py` (вхід, `?next=`, 401/403), `… UPLOADS_DIR=/tmp/pl-smoke uv run python tests/smoke_games.py` (гра, заявки, знахідки), `… tests/smoke_guide.py` (методичка: читання без чернеток, PUT/409, історія, чернетка «Що змінилось», export/import, ідеї), `… tests/smoke_activity.py` (сторінка активності: стрічка, люди, журнал подій, рядок 500), `… tests/smoke_view_as.py` («Очима студента»: хто може, чиї права, чий слід), `… tests/smoke_errors.py` (колекція `errors`: API, бот, помилки фронту з лімітами, стрічка)

У PyCharm (Pro): run-конфігурація FastAPI (`app/api/main.py`, в Uvicorn options — `--port 8030`) + npm-конфігурація `dev` (`app/vue/package.json`) + Compound «app» — запуск обох однією кнопкою.

## Методичка

Публічні сторінки для студентів (`/labs` + `/labs/1…5`, `/score`, `/howto`, `/method` — усе однією сторінкою; `/games` і `/tasks` — текст розділу всім, каталог поки лише адміну) рендерять Markdown із Mongo-колекції `guide` через `GET /api/guide/{slug}`; домашня — лід + «Як влаштований курс». **Правка — на сайті** (адмін: ✏️ біля заголовка або «✏️ сторінку», нотатка «що змінив» → чернетка на `/changes`, історія з diff і відкатом — `/method/history`; [T128](../.dev/platform/.t/T128--guide-editor-v1/report.md)); файли `data/guide/*.md` ([конвенції](../data/guide/README.md)) — seed при першому старті і знімок: `cd api && uv run python guide_io.py export|import`. **Чернетки** ([T157](../.dev/platform/.t/T157--guide-drafts/report.md)): `<!-- … -->` у тексті — те, чого студенти не отримують; вирізає сервер (`api/drafts.py`), адмін бачить чернетки виділеними й перемикає «👁 з чернетками / 🙈 як у студентів» (`vue/src/drafts.js`); сторінка з самих чернеток студентові порожня і в меню її розділу нема; `bin/guide close` — усі сторінки цілком у чернетки. Якорі `{#id}` → `/score#79`: «🔗» біля заголовка копіює лінк, ціль підсвічується. Список розділів і маршрути — `vue/src/guide.js`; рендер — `md.js`, скрол/спалах — `anchors.js`. Звіт — [T117](../.dev/.t/T117--guide-v1/report.md).

**Правка агентом** ([T153](../.dev/platform/.t/T153--agent-guide-access/report.md), [T155](../.dev/platform/.t/T155--agent-catalog-snapshot/report.md)): ШІ-агент править сторінки методички й картки каталогу через те саме API, вхід — токен у заголовку `Authorization: Bearer …`; токени — `AGENT_TOKENS=claude:<токен>,codex:<токен>` в `api/.env`, імʼя — автор в історії. Решту сайту токен не відкриває. Скрипти без залежностей: `bin/guide` (`ls` · `pull [slug…]` · `push <slug> -m "що змінив" [-s "Розділ"]` · `snap` · `close`) і `bin/catalog` (`ls tasks|games [текст]` · `pull` · `push [tasks/<slug> …]` · `snap`); без `-t` — сервер, `-t dev` — дев; адреси й токени — `.site/.env`, робочі копії — `.site/<ціль>/` (поза git). `snap` знімає сайт у `data/guide/` і `data/catalog/` — це знімок для git; після `push` на сервер він робиться сам. Смоук: `… tests/smoke_agent.py`.

**Історія тасків та ігор** ([T156](../.dev/platform/.t/T156--card-history/report.md)): `/tasks/history` і `/games/history` (адмін) — кожна правка з «було → стало» по полях і відкатом ↩; `?slug=` — один запис. Бек — `api/routes/card_history.py`, фронт — `vue/src/pages/CardHistoryPage.vue`, `components/CardChange.vue`, `cardFields.js`. Імпорт із YAML теж пише в історію. Смоук: `… tests/smoke_card_history.py`.

## Активність

`/activity` (меню «Актив», лише адмін) — усе, що збирають сайт і бот: стрічка входів, переглядів, змін даних, Telegram, нотаток і збоїв (чіпи джерел, «і викладачі», `?user=<нік>` — одна людина) та вкладка «Люди» з лічильниками за період і стовпчиками за 14 днів. Оновлюється сама. Бек — `api/activity_feed.py` (злиття журналів), `api/activity_people.py` (лічильники), `api/routes/activity.py`; фронт — `vue/src/pages/ActivityPage.vue`, `components/Activity*.vue`, `activity.js`. Звіт — [T146](../.dev/platform/.t/T146--activity-page/report.md).

Telegram-рядки й нотатки, записані до привʼязки бота, не мають пошти — людину за Telegram id знаходить читання (`api/activity_link.py`), у базі нічого не дописується. Звіт — [T150](../.dev/platform/.t/T150--tg-link-on-read/report.md).

## Помилки

- Відповідь API розбирає `vue/src/http.js`: помилка несе `status` і людський текст; нема відповіді — `status = 0` і прапорець `down` → банер `DownBar.vue`.
- Помилку, яку сторінка не зловила, бере `report()` у `vue/src/problem.js`: 404 → сторінка 404 замість відкритої, решта → блок `Oops.vue` над нею. Тому завантаження даних у сторінці — без `try`: ловити варто лише те, для чого є свій текст поруч із кнопкою.
- Необроблені помилки API, бота і фронту лягають у колекцію `errors` (`api/models/error.py`) з повним traceback і йдуть алертом `error`; фронт шле свої на `POST /api/errors` (`api/routes/front_errors.py`). Дивитись — `/activity`, чіп «💥 Помилки».
- Звіт — [T149](../.dev/platform/.t/T149--errors-pack/report.md).

## Telegram-бот

Живе в `app/api/bot/` — та сама база, моделі й `.env`, що й API (тому не окремий пакет). Інструкція користування — [api/bot/README.md](api/bot/README.md). Уміє: `/start` + привʼязка акаунта deep link-ом з профілю; адмін-алерти (профілі, перші входи, заявки, гра студента, повідомлення боту, помилки сайту/API/бота; кожен спершу лягає в колекцію `events`, тож лишається в базі, навіть коли Telegram його не отримав) — без налаштувань особисто адмінам, що привʼязали бота, або в групу/гілку форуму після `/here change` там (`/here` — статус із ключами видів, `/here all`, `/here off`, `/mute game` — вимкнути вид). Алерти шле сам API (той самий `TG_BOT_TOKEN`), запущений бот потрібен лише для `/here` і ранкового дайджесту профілів (09:00 Київ).

- токен від BotFather → `TG_BOT_TOKEN` у `app/api/.env`;
- запуск: `cd app/api && uv run python -m bot` (long polling, вебхук не потрібен);
- смоуки без Telegram: `DB_NAME=python_labs_smoke uv run python tests/smoke_bot.py` (привʼязка), `… tests/smoke_notify.py` (алерти профілю, `/here`, `/mute`), `… tests/smoke_events.py` (заявки, гра, помилки, дайджест, перший вхід).
