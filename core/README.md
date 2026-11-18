# core — платформа, спільна для всіх сайтів

Усе, що не знає про ігри чи лекції: вхід, люди, бот, активність, помилки, методичка, оформлення. Сайт — тонка тека поруч: `app/` (python), `sites/ods/`. Чому так — [T163](../.dev/platform/.t/T163-P--core-and-sites.md), як виносили — [T167](../.dev/platform/.t/T167--core-extract/report.md).

- `api/` — Python-пакет `core`; сайт бере його залежністю за шляхом.
- `ui/` — вихідні файли Vue; сайт бачить їх через alias `@core`.

## Три правила

1. Ядро не знає про сайти: жодного `if site == 'ods'`. Відмінність — параметр, слот або код сайту.
2. Що не знає про предмет сайту (ігри, лекції) і може знадобитись іншому сайтові — живе в ядрі одразу (рішення 2026-11-19, [T352](../.dev/platform/.t/T352--shared-to-core/plan.md)); у сайті лишається лише своє. Зшите з предметом сайту — лишається в сайті, доки його не розшито.
3. Перед пушем проходять смоук-тести всіх сайтів: платформні — `api/tests/`, з теки кожного сайту.
4. Сторінку ядра сайт підключає тим самим шляхом і з тією самою метою, що й сусідній сайт: пункт меню — тим самим словом.

Залежність іде в один бік: сайт імпортує ядро, ядро сайт — ніколи.

## Що всередині

| Частина | Бекенд `api/core/` | Фронт `ui/` |
|:--------|:-------------------|:------------|
| Вхід, сесія, ролі, «очима студента», токен агента | `routes/auth.py`, `routes/me.py`, `routes/view_as.py`, `deps.py` | `user.js`, `router.js`, `pages/LoginPage.vue`, `ViewBar.vue` |
| Профіль і студенти | `models/user.py`, `routes/profile.py`, `routes/students.py` | `pages/ProfilePage.vue`, `pages/Student*.vue`, `studentFilter.js`, `studentSearch.js` |
| Бот | `bot/` | — |
| Активність, події, помилки | `activity_*.py`, `routes/activity.py`, `routes/front_errors.py`, `models/` | `pages/ActivityPage.vue`, `activity.js`, `problem.js`, `http.js` |
| Історія правок | `models/history.py` | `diff.js`, `components/Diff.vue` |
| Методичка | `models/guide.py`, `routes/guide.py`, `guide_io.py`, `guide_mirror.py` (дзеркало з іншого сайту: `bin/guide dump` → `python -m core.guide_mirror apply`), `drafts.py` | `pages/GuidePage.vue`, `MethodPage.vue`, `HistoryPage.vue`, `components/Guide*.vue` (`GuideHead` — текст розділу над каталогом сайту: згортається, переноситься вниз), `md.js`, `guide.js` (`labPages()` — лаби серед сторінок) |
| Домашня: «Перші кроки» | — | `components/StartSteps.vue`: увійти, привʼязати бота; тиждень і свій рядок — з паспорта (`site.start`) |
| Опитування в Telegram | `models/poll.py`, `poll_send.py`, `vote.py`, `polls_*.py`, `routes/poll*.py`, `bot/polls.py`, `bot/chats.py` | `pages/Poll*.vue`, `components/Poll*.vue`, `TagInput.vue`, `polls.js` |
| Тиждень студента | `models/week.py`, `week_marks.py`, `routes/my_week.py`, `routes/weeks.py`, `bot/week.py` | `pages/MyWeekPage.vue`, `WeekPage.vue`, `components/Week*.vue`, `CopyNicks.vue`, `week*.js`, `autosave.js` |
| Лаби: дедлайни, репозиторії, звіти агента | `models/deadline.py`, `models/repo.py`, `labs.py`, `lab_marks.py`, `repos.py`, `routes/labs.py`, `routes/student_labs.py`, `bot/due.py` | `pages/DeadlinesPage.vue`, `components/Lab*.vue`, `DeadlineForm.vue`, `StudentLabs.vue`, `labs.js` |
| Таблиця студентів: види, свої поля | `models/field.py`, `models/view.py`, `table.py`, `fields.py`, `routes/table.py`, `routes/fields.py`, `routes/views.py` | `pages/TablePage.vue`, `components/Table*.vue`, `Fields*.vue`, `table.js`, `tableCols.js`, `tableViews.js` |
| Оформлення | — | `App.vue`, `NavBar.vue`, `Crumbs.vue`, `theme.js`, `style.css`, `dark.css` |
| Мова дій: один колір — одна дія (T270 §1) | — | `components/Icon.vue` (лінійні SVG: `<Icon name="plus" />`), `Pop.vue` (спливна панель біля свого елемента), `DelButton.vue` (кошик з підтвердженням), `Lightbox.vue` + `lightbox.js` (картинка поверх сторінки); `Tip.vue` + `tips.js` (пояснення в єдиному оформленні: `<Tip id="…">` — читач може сховати, лишається «ⓘ»), `HashLink.vue` («#» біля заголовка блоку: посилання на це місце сторінки); у `style.css` — `btn-add` (додати — фіолетовий), `iact` / `iact del` / `iact add` (іконка-дія), `soft-input`, `<mark>`, `editing` / `editing new` (рамка відкритої форми), `more-field` (тихе «＋ нотатка»); зберегти — `btn-success`, скасувати — `btn-outline-secondary`; `SaveCancel.vue` (пара «✕ ✓» під формою), `MoreFields.vue` (тихий ряд «⊕ поле» рідких полів) |
| Текст і вибір | — | `search.js` (`norm` — пошук без огляду на регістр і «и / і», `hl`, `markHtml` — підсвітка знайденого), `components/Md.vue` (Markdown з підсвіткою), `MdField.vue` (текст у формі: клік — джерело на місці), `InlineMd.vue` (те саме без форми: зберігає сам), `Picker.vue` + `pick.js` (один список-вибір із пошуком: рядок каже, чому знайшовся; `tag` — тихе слово біля назви), `shortLink.js` (посилання, як його читають) |
| Сторінка, що згортається | — | `fold.js` (памʼять «розгорнуто · коротко · згорнуто» за місцем сторінки, «усе одразу»), `jump.js` («покажи де»: згорнуте саме відкривається, сторінка їде до місця, місце спалахує) |

## Сайт на ядрі: бекенд

Тека сайту — та, з якої запускається все: там `.env`, `main.py`, `bot/`.

| Файл сайту | Що в ньому |
|:-----------|:-----------|
| `pyproject.toml` | залежність `labs-core` за шляхом, editable |
| `site.env` | сталі сайту, в git: `SITE_NAME`, `DB_NAME`, `SITE_URL`, `GUIDE_DIR`; за потреби `GUIDE_READERS`, `SESSION_COOKIE`, `WEEK_HOURS`, `WEEK_DAYS`, `LABS` |
| `.env` | секрети й значення цієї машини; читається після `site.env` |
| `db.py` | `MODELS` — власні документи, `init_db()` |
| `main.py` | `app = create_app(models=MODELS, routers=[…])` |
| `bot/__init__.py` | власні види алертів: `notify.add({...}, after="login")` |
| `bot/__main__.py` | `run(init_db)`; запуск — `python -m bot` |

- Налаштування — один екземпляр `core.config.settings`. Власні модулі сайту лишаються пласкими: `from models.game import Game`.
- Рядок студента в списку `/api/students` сайт доповнює через `students.EXTRAS` (бачить кожен, хто бачить рядок: гра на python) або `students.TEACHER` (лише викладач і `/table`: бали, нотатки, посилання — картки лаб на ods). Адмін отримує всіх, із поштою/GitHub/Telegram; студент — лише студентів (`can_see`: без викладачів, pending і тестових, крім себе) як `person()`-рядки. Тим самим `can_see` сайт закриває й `/students/<нік>`.
- `GUIDE_READERS`: `admin` — методичку читають лише адміни й агенти; `active` — і студенти (ods); `all` — будь-хто, і гість (python). Не-адмін отримує текст без чернеток.
- `SESSION_COOKIE`: назва cookie сесії. Другий сайт у деві ставить свою: браузер не розрізняє cookie за портом.
- Сторінка `/students/<нік>` — за сайтом: на неї ведуть алерти бота й крихти.
- `WEEK_HOURS` (`15-23`) і `WEEK_DAYS` (`6`, від понеділка) — сітка «Мій тиждень»: сторінки малюють те, що віддає API, своїх годин у них нема.
- `LABS` (`5`) — скільки лаб у курсі: колонки `/deadlines`, що приймають `/due` і звіти; сайт реєструє маршрут `/deadlines` і пункт меню, назви лаб бере з `site.guide` (`n`; де номер мають і інші сторінки, лаби позначає `kind: 'labs'`). `/api/labs` — шлях ядра: своє про лаби сайт тримає під іншим (ods — `/api/variants`). Репозиторії студентів на диск тягне `bin/repos` (python), сайт лише зберігає факти (`PUT /api/repos`).
- `/table` (T240) — рядок студента з усіх джерел одним читанням (`core/table.py`: профіль, `labs.Index`, `Repo`, останній голос у кожному опитуванні, свої поля, `students.EXTRAS`); свої поля й збережені види — `fields`, `field_values`, `views`; усе для адміна й агента (`editor_user`), опитування (`GET`) — теж. Заводські види («Усе», «Старт», «Лаба N», «Дедлайн N») ядро створює само; їхні колонки й «для чого» — сталі `core/views_seed.py` (`ALL_COLS`, `START_COLS`, `START_ABOUT`, `LAB_COLS`, `LAB_ABOUT`), які сайт замінює у своєму `table_seed.py`; уже створений вид лишається, яким є.

## Сайт на ядрі: фронт

| Файл сайту | Що в ньому |
|:-----------|:-----------|
| `vite.config.js` | alias `@core`, `dedupe`, `fs.allow` — як у `app/vue` |
| `src/site.js` | паспорт сайту: назва, меню, сторінки методички, власні колонки студентів |
| `src/router.js` | усі маршрути явним списком, сторінки ядра серед них: `makeRouter([…])` |
| `src/main.js` | `start(site, router)` |
| `src/api.js` | власні виклики API |

- Поля паспорта описано в `ui/site.js`. Групу (`students`, `table`, `start`, `profile`) сайт пише лише тим, що в нього своє: решта лишається за замовчуванням. Пункт меню з третім елементом (`['/students', 'Студи', 'admin']`) — вужчий за сторінку: сторінка відкрита студентам, пункт — ні. Пʼятий елемент — значок: ним стає слово, коли меню тісно й читач обрав «меню значками» (`navFit.js`).
- `/students` студентові — та сама сторінка під назвою з `students.asStudent` (`{ title, crumbs }`; корінь крихт і назву дають `ui/students.js`), чіпи груп і пошук за початком слова (`studentSearch.js`), таблиця без пошти/GitHub/Telegram, імʼя веде на `/students/<нік>`; `students.inGallery` звужує галерею (python: лише з грою) — числа в заголовку й на чіпах ідуть за режимом.
- Мета маршруту, яку читає ядро: `title`; `access` — `'admin'` · `'active'` · нема = усім; `filters` — зміна `?запиту` не гортає вгору; `stay` — інший параметр тієї самої сторінки теж (`/week/3` → `/week/4`); `wide` — `true`: сторінку можна розгорнути на все вікно (`wide.js`: `wide`, `toggleWide` — одна памʼять на таблиці й каталог), слово (`'game'`) — окрема памʼять `wideOf('game')`, `'admin'`: викладачу завжди на все вікно. Частину широкої сторінки тримає в колонці клас `.in-column`.
- `site.table.cols` — власні колонки `/table`: `{ key, type, title, short, get: (row) => …, link? }` (python: гра, заявки, монетки з `game.coins`); фасети `students.facets` стають колонками-чекмарками самі. Колонка з ключем `lab<N>.<слово>` і полями `group`, `cat: 'Лаба'`, `lab: N` стоїть у смузі своєї лаби, а вид каже про неї «ця лаба» — `lab.<слово>` (ods: `sites/ods/vue/src/labCols.js`).
- Зміст сторінки — `<Toc :items>` (`[{ id, text, depth }]`, `{ label }` між групами, `quiet` — місце поза списком): збоку від колонки, а де не вміщається чи `side` вимкнено — у «☰» з `PageJump`. Ядро саме позначає розділ на екрані й показує під меню рядок «де я» (`TocBar`); сторінка з власними прилиплими заголовками вимикає його властивістю `bar`.
- Картка під мишкою — директива `v-peek="{ kind, id }"` і `<PeekHost />` на сторінці; вигляд картки за видом реєструє сайт: `registerPeeks({ kind: Component })`. Згадка всередині картки відкриває наступну.
- `site` заповнюється в `start()`. Ядро читає його у функціях і компонентах, а не на верхньому рівні модуля: там він ще порожній.
- `public/` у кожного сайту своя: іконки й `theme-boot.js`.
- Свій синтаксис Markdown — `useMd(ext)` з `md.js` у `main.js` сайту, до `start()`: так ods додає формули.
- Коментар `<!-- слайд N -->` — не чернетка: межа слайда, на сторінці невидима. Решта `<!-- … -->` — чернетки.

## Сайт на ядрі: деплой

На сервері сайт — окремий застосунок зі своїм маніфестом у vps-infra. У цьому репо йому належать дві гілки.

| Сайт | Гілка деплою | Гілка статики |
|:-----|:-------------|:--------------|
| python | `main` | `www` |
| ods | `ods` | `www-ods` |

- `bin/www <сайт> [коміт]` збирає фронт сайту й пушить гілку статики; тека фронта й назва гілки — на початку скрипта.
- `bin/hooks/pre-push` викликає його на push гілки деплою; відповідність «гілка → сайт» — у хуку.
- Ті самі назви стоять у маніфесті сайту: `BRANCH` і `WWW`.
- Оновити ods: `git push origin main:ods`. Сам ods ще не на сервері — план у [T180](../.dev/ods/.t/T180-P--ods-deploy-plan.md).
- Новий сайт — рядок у `bin/www`, рядок у хуку, маніфест у vps-infra.

## Перевірка

- Смоуки платформи — `api/tests/` ([README](api/tests/README.md)): той самий файл запускається з теки `api` кожного сайту й проходить на обох. Смоуки сайтів — `app/api/tests/` (ігри, каталог, захисти, ШІ), `sites/ods/api/tests/` (лекції, варіанти лаб, колонки «Зводу»).
- Без `uv run` поза `app/api`: venv у деві спільний із запущеними серверами — `~/.venvs/python-labs/bin/python <смоук>`.
- Після правки ядра — смоуки обох сайтів і збірка обох фронтів: `npm run build` в `app/vue` і `sites/ods/vue`.
