# core — платформа, спільна для всіх сайтів

Усе, що не знає про ігри чи лекції: вхід, люди, бот, активність, помилки, методичка, оформлення. Сайт — тонка тека поруч: `app/` (python), `sites/ods/`. Чому так — [T163](../.dev/platform/.t/T163-P--core-and-sites.md), як виносили — [T167](../.dev/platform/.t/T167--core-extract/report.md).

- `api/` — Python-пакет `core`; сайт бере його залежністю за шляхом.
- `ui/` — вихідні файли Vue; сайт бачить їх через alias `@core`.

## Три правила

1. Ядро не знає про сайти: жодного `if site == 'ods'`. Відмінність — параметр, слот або код сайту.
2. Є сумнів — код лишається в сайті. У ядро переїжджає те, що знадобилося вдруге.
3. Перед пушем проходять смоук-тести всіх сайтів.

Залежність іде в один бік: сайт імпортує ядро, ядро сайт — ніколи.

## Що всередині

| Частина | Бекенд `api/core/` | Фронт `ui/` |
|:--------|:-------------------|:------------|
| Вхід, сесія, ролі, «очима студента», токен агента | `routes/auth.py`, `routes/me.py`, `routes/view_as.py`, `deps.py` | `user.js`, `router.js`, `pages/LoginPage.vue`, `ViewBar.vue` |
| Профіль і студенти | `models/user.py`, `routes/profile.py`, `routes/students.py` | `pages/ProfilePage.vue`, `pages/Student*.vue`, `studentFilter.js` |
| Бот | `bot/` | — |
| Активність, події, помилки | `activity_*.py`, `routes/activity.py`, `routes/front_errors.py`, `models/` | `pages/ActivityPage.vue`, `activity.js`, `problem.js`, `http.js` |
| Історія правок | `models/history.py` | `diff.js`, `components/Diff.vue` |
| Методичка | `models/guide.py`, `routes/guide.py`, `guide_io.py`, `drafts.py` | `pages/GuidePage.vue`, `MethodPage.vue`, `HistoryPage.vue`, `components/Guide*.vue`, `md.js` |
| Опитування в Telegram | `models/poll.py`, `poll_send.py`, `vote.py`, `polls_*.py`, `routes/poll*.py`, `bot/polls.py`, `bot/chats.py` | `pages/Poll*.vue`, `components/Poll*.vue`, `TagInput.vue`, `polls.js` |
| Тиждень студента | `models/week.py`, `week_marks.py`, `routes/my_week.py`, `routes/weeks.py`, `bot/week.py` | `pages/MyWeekPage.vue`, `WeekPage.vue`, `components/Week*.vue`, `CopyNicks.vue`, `week*.js`, `autosave.js` |
| Оформлення | — | `App.vue`, `NavBar.vue`, `Crumbs.vue`, `theme.js`, `style.css`, `dark.css` |

## Сайт на ядрі: бекенд

Тека сайту — та, з якої запускається все: там `.env`, `main.py`, `bot/`.

| Файл сайту | Що в ньому |
|:-----------|:-----------|
| `pyproject.toml` | залежність `labs-core` за шляхом, editable |
| `site.env` | сталі сайту, в git: `SITE_NAME`, `DB_NAME`, `SITE_URL`, `GUIDE_DIR`; за потреби `GUIDE_READERS`, `SESSION_COOKIE`, `WEEK_HOURS`, `WEEK_DAYS` |
| `.env` | секрети й значення цієї машини; читається після `site.env` |
| `db.py` | `MODELS` — власні документи, `init_db()` |
| `main.py` | `app = create_app(models=MODELS, routers=[…])` |
| `bot/__init__.py` | власні види алертів: `notify.add({...}, after="login")` |
| `bot/__main__.py` | `run(init_db)`; запуск — `python -m bot` |

- Налаштування — один екземпляр `core.config.settings`. Власні модулі сайту лишаються пласкими: `from models.game import Game`.
- Рядок студента в списку `/api/students` сайт доповнює через `students.EXTRAS`.
- `GUIDE_READERS`: `admin` — методичку читають лише адміни й агенти (python, поки методичка не готова); `active` — і студенти, без чернеток (ods).
- `SESSION_COOKIE`: назва cookie сесії. Другий сайт у деві ставить свою: браузер не розрізняє cookie за портом.
- Сторінка `/students/<нік>` — за сайтом: на неї ведуть алерти бота й крихти.
- `WEEK_HOURS` (`15-23`) і `WEEK_DAYS` (`6`, від понеділка) — сітка «Мій тиждень»: сторінки малюють те, що віддає API, своїх годин у них нема.

## Сайт на ядрі: фронт

| Файл сайту | Що в ньому |
|:-----------|:-----------|
| `vite.config.js` | alias `@core`, `dedupe`, `fs.allow` — як у `app/vue` |
| `src/site.js` | паспорт сайту: назва, меню, сторінки методички, власні колонки студентів |
| `src/router.js` | усі маршрути явним списком, сторінки ядра серед них: `makeRouter([…])` |
| `src/main.js` | `start(site, router)` |
| `src/api.js` | власні виклики API |

- Поля паспорта описано в `ui/site.js`.
- `site` заповнюється в `start()`. Ядро читає його у функціях і компонентах, а не на верхньому рівні модуля: там він ще порожній.
- `public/` у кожного сайту своя: іконки й `theme-boot.js`.
- Свій синтаксис Markdown — `useMd(ext)` з `md.js` у `main.js` сайту, до `start()`: так ods додає формули.
- Коментар `<!-- слайд N -->` — не чернетка: межа слайда, на сторінці невидима. Решта `<!-- … -->` — чернетки.

## Перевірка

- Смоуки платформи поки лежать у `app/api/tests/`: більшість перевіряє платформу разом з іграми. У ods — `sites/ods/api/tests/`.
- Після правки ядра — смоуки обох сайтів і збірка обох фронтів: `npm run build` в `app/vue` і `sites/ods/vue`.
