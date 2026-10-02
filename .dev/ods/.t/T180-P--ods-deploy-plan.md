# T180 · Деплой ods: що готово, що пофіксити, план

`2026-10-01` · 💡 proposal

Контекст:
- запит Vitalik (чат, 2026-10-01): «що треба зробити, щоб задеплоїти сайт ods.labs.in.ua та відповідного бота… Чи треба якісь моменти спочатку пофіксити? Наприклад, www генерацію, окремі гілки для деплою різних сайтів, якісь відповідні налаштування тут і там»; vps-infra не чіпати — там незакомічені зміни; у python-labs правити можна, якщо впевнений;
- рішення, на яких стоїть план: один репо й гілка деплою на сайт — [T164](../../.rounds/.t/T164-R--ods-kickoff.md), [T163](../../platform/.t/T163-P--core-and-sites.md); бот одразу — [T168](../../.rounds/.t/T168-R--ods-base-decisions.md) Q6; контент лише в Mongo — [README](../README.md);
- vps-infra читав, не правив: код `vv/` і `deploy`, маніфест і [картка python-labs](../../../../../My/vps-infra/.dev/apps/python-labs/README.md), контракт гілки статики ([T59](../../../../../My/vps-infra/.dev/vv/.t/T59-P--ci-www-branch.md), [T63](../../../../../My/vps-infra/.dev/vv/.t/T63--www-hook/report.md));
- вибори — [T181](T181-Q--ods-deploy-choices.md); план нижче йде за рекомендаціями «a».

## Коротко

- Код `vv` і `deploy` міняти не треба. Другий сайт з того самого репо — це ще одна тека маніфесту `apps/ods-labs/`: свій користувач, клон, venv, база, порт, таймер.
- У python-labs бракувало одного: `bin/www` і хук знали лише сайт python. Зроблено цієї сесії.
- Лишаються дії поза кодом: бот у BotFather, адреса в Google OAuth, гілки `ods` і `www-ods` на GitHub, маніфест у vps-infra, команди `vv` на сервері.
- Два місця, де легко помилитись: дев-користувач у локальній базі `ods` і памʼять сервера.

## Що перевірено

| Що | Як | Результат |
|:---|:---|:----------|
| DNS | `dig` | `ods.labs.in.ua` → `185.65.245.199` (vv3) за wildcard `*.labs.in.ua`; запис додавати не треба |
| Маніфест | чернетка нижче + справжній `vv` на копії в тимчасовій теці | `vv apps`, `vv show`, `vv render unit\|caddy\|tmpfiles\|sysusers` — без помилок; юніти з `WorkingDirectory=/srv/ods-labs/repo/sites/ods/api`, Caddy → `127.0.0.1:8035` |
| Пара гілок | клон-«сервер»: `fetch ods www-ods`, порівняння, `git archive` | `deploy` звіряє subject гілки `WWW` із sha `origin/BRANCH`, назви — з маніфесту; пара `ods`/`www-ods` працює як `main`/`www`. Закриває «не перевірено» з T163 |
| venv | `uv sync --frozen --project sites/ods/api --python 3.12 --no-dev` у чистому клоні | 64 пакети; ядро ставиться залежністю за шляхом |
| Старт як на сервері | uvicorn на Python 3.12 із самих змінних оточення: без `.env`, без `sites/ods/data` | `/api/health` → `{"ok": true}` за ~3 с; гість — 401; порожній `FAKE_USER_EMAIL` не пускає; теки `GUIDE_DIR` на сервері нема — старту не заважає |
| Смоук ods | той самий клон, Python 3.12 | 10/10 |
| Адреса для Google | `/api/auth/login` із заголовками, які ставить Caddy | `redirect_uri=https://ods.labs.in.ua/api/auth/callback`, cookie `ods_session` |
| База | локальна `ods` | 20 сторінок, 123 картинки, архів `mongodump --gzip` — 7.1 МБ |

Сервер не чіпав і не міряв: усе вище — ноутбук.

## Зроблено цієї сесії

- `bin/www <сайт> [коміт]`:
  - `python` — `app/vue` → гілка `www`;
  - `ods` — `sites/ods/vue` → гілка `www-ods`;
  - без сайту — рядок `usage`.
- `bin/hooks/pre-push`: push у `main` → `bin/www python`, push в `ods` → `bin/www ods`, решта гілок — нічого.
- Перевірено на окремому клоні з локальним «GitHub» — bare-репо в тимчасовій теці; справжній GitHub не чіпався:
  - дерево `www` для `0ada5a0` — `24806f1`, те саме, що в нинішньої `origin/www`: статика python не змінилась;
  - `www-ods` — один коміт без батька, subject = sha, 64 файли (59 з них — шрифти формул);
  - `git push origin main` збирає лише `www`, `git push origin main:ods` — лише `www-ods`, обидві разом — обидві;
  - коміт, старший за `core/`, для python збирається; коміт без `sites/ods/vue` для ods падає з `pathspec … did not match`.
- Команда з картки python-labs у vps-infra «гілка `www` відстала» тепер пишеться `bin/www python origin/main`.

## Що пофіксити до деплою

1. **vps-infra: довезти незакомічене на vv3.** Чернетка маніфесту — у форматі `env.conf`, а він на сервер ще не приїхав. Спершу коміт і push наявних змін, `sudo vv self-update`, `sudo vv check --all`.
2. **Дев-користувач у локальній базі `ods`.**
   - У базі один користувач — дев-вхід (`FAKE_USER_EMAIL`, адреса на `nure.ua`), статус `admin`.
   - `vv db push` переносить базу цілком.
   - Рядок зі статусом `admin` лишається адміном і без `ADMIN_EMAILS`: вхід виставляє статус тим, хто у списку, решті не чіпає.
   - Якщо така скринька в NURE існує, її власник увійде на ods адміном.
   - Тому перед переносом — прибрати користувача й дев-шум (985 рядків `activity`); команди — у блоці 3.
   - У python такого нема: у локальній `python_labs` один адмін, і він зі списку.
3. **Памʼять vv3.** 1.9 GiB RAM, 2 GiB свопу, одне ядро. Юніти python-labs тримають ≈ 200M (web) і ≈ 175M (бот); ods додасть стільки ж. Виміряти до й після: `free -m`, рядки `mem` у `sudo vv check --all`.
4. **Гілка `ods` має бути на GitHub до `vv repo init`.** Без неї `repo init` скаже «GitHub ще не знає цей ключ» — підказка не про те.

## Маніфест

Чернетка для `vps-infra/apps/ods-labs/`. Перевірена `vv`; значень секретів у ній нема.

`app.conf`:

```sh
# ods-labs — ods.labs.in.ua + бот: другий сайт репо python-labs (sites/ods), той самий стек, свій venv і база.
# BRANCH — гілка деплою сайту, WWW — гілка його статики: обидві пушить python-labs (pre-push → bin/www ods).
REPO=git@github.com:2vitalik/python-labs.git
BRANCH=ods
PYTHON=/usr/bin/python3.12
PROJECT_DIR=sites/ods/api
DB=ods_labs
WWW=www-ods
```

`env.conf`:

```sh
MONGO_URI!                  # пише vv db add
DB_NAME={DB}
GOOGLE_CLIENT_ID            # Cloud Console → клієнт ods
GOOGLE_CLIENT_SECRET!       # Cloud Console → клієнт ods
SESSION_SECRET*             # підпис сесій; ротація — vv env set --random
ADMIN_EMAILS                # через кому без пробілів
FAKE_USER_EMAIL?            # порожньо = dev-вхід без Google вимкнено
TG_BOT_NAME                 # без @
TG_BOT_TOKEN!               # BotFather
AGENT_TOKENS!               # імʼя:токен для bin/guide -t ods
SITE_URL=https://{DOMAIN}
```

`units/ods-labs-web.conf`:

```sh
# Без CSP/HSTS на старті, як python-labs; на диск не пише — картинки лекцій у Mongo.
KIND=web
EXEC="venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8035 --workers 1"
ENV_EXTRA="PYTHONUNBUFFERED=1"
MEMORY_MAX=384M
PORT=8035
DOMAIN=ods.labs.in.ua
HEALTH=/api/health
```

`units/ods-labs-bot.conf`:

```sh
# Long polling; на диск не пише; sys.exit без TG_BOT_TOKEN.
KIND=bot
EXEC="venv/bin/python -m bot"
ENV_EXTRA="PYTHONUNBUFFERED=1"
RESTART_SEC=15s
STOP_TIMEOUT=30
MEMORY_MAX=384M
```

- `AGENT_TOKENS!` — за T181 Q5 «a»; за «b» рядок прибрати: `!` не дозволяє порожнього значення.
- `UPLOADS_DIR` і `RW_PATHS` не потрібні: ods файлів на диск не кладе.
- Порт 8035 — запас проєкту №3, як у деві; на vv3 вільний (зайняті 8010, 8030, план — 8040).
- Розкладка з перервами — `STATE=planned` у першому коміті маніфесту, прибрати перед блоком 6, як було в python-labs.

## План

Блоки 1–6 — робота сесії у vps-infra: там зʼявляться своя задача, логи й картка `apps/ods-labs`, цей тікет для неї — вхідний матеріал. Команди сервера — у сесії `ssh vv3`.

**Блок 0 — локально, python-labs**

1. Коміт `bin/www` і хука, `git push`. Перевірка: рядок `www: origin/www ← …`, python задеплоївся як завжди.
2. BotFather: новий бот → нік і токен у 1Password.
3. Google Cloud Console, той самий проєкт: OAuth-клієнт для ods з адресою `https://ods.labs.in.ua/api/auth/callback` → ID і secret у 1Password. Consent screen уже в production.
4. Гілки:

```sh
git push origin main:ods
git ls-remote --heads origin
```

Чекаємо: у списку `ods` і `www-ods`.

**Блок 1 — маніфест (vps-infra)**

1. Коміт і push наявних змін → `sudo vv self-update` → `sudo vv check --all`.
2. `apps/ods-labs/` з чернетки, картка, рядок реєстру → коміт, push → `sudo vv self-update` → `vv apps`.

**Блок 2 — тенант**

```sh
sudo vv tenant add ods-labs
sudo vv repo init ods-labs
```

Перший `repo init` друкує pub-ключ і виходить з кодом 77. Ключ — у GitHub: репо python-labs → Settings → Deploy keys, без write, назва `vv3 ods-labs`. Ключ `vv3`, що там уже є, — від застосунку python-labs; у кожного застосунку свій. Потім:

```sh
sudo vv repo init ods-labs
sudo vv venv sync ods-labs
sudo vv check ods-labs
```

**Блок 3 — дані**

```sh
sudo vv db add ods-labs
sudo vv env edit ods-labs
```

У редакторі: `GOOGLE_CLIENT_ID`, `ADMIN_EMAILS`, `TG_BOT_NAME`; `FAKE_USER_EMAIL` порожній. Секрети команда спитає прихованим вводом: `GOOGLE_CLIENT_SECRET`, `TG_BOT_TOKEN`, `AGENT_TOKENS` — у вигляді `claude:<токен>`, токен — `openssl rand -hex 32`.

На ноутбуці, `mongosh ods` — прибрати дев-користувача й шум:

```js
db.users.drop()
db.activity.drop()
db.events.drop()
db.history.deleteMany({ coll: "users" })
```

На ноутбуці, з теки vps-infra:

```sh
./vv/bin/vv db push ods-labs vv3 --from ods
```

До `start`: порожня база приймає без `--drop`. Після переносу локально — звичайний dev-вхід, користувач створиться знову.

**Блок 4 — юніти**

```sh
free -m
sudo vv unit apply ods-labs
sudo vv start ods-labs --kill-test
free -m
```

**Блок 5 — Caddy**

```sh
sudo vv site apply ods-labs
```

Чекаємо: `TLS ok · HTTP 404` — `www/` порожній до першого деплою.

**Блок 6 — перший деплой і таймер**

```sh
sudo deploy ods-labs
```

Перевірка в браузері: вхід Google, лекція з формулами й картинками, слайди. Потім:

```sh
sudo vv timer on ods-labs
sudo vv check --all
```

**Блок 7 — після**

- Бот: «Привʼязати бота» у власному профілі, `/here` — куди йдуть алерти.
- Студенти: імпорт списків груп на `/students` до оголошення; лекції бачать лише підтверджені.
- Агент: `ODS_URL` і `ODS_TOKEN` у `.site/.env` → `bin/guide -t ods ls`. Перед цим закрити в `bin/guide` команду `snap` для цілі не `prod`: без `--to` вона пише в `data/guide/`, тобто в git.
- Доки: README ods, картка у vps-infra.

## Як жити після

| Дія | Команда |
|:----|:--------|
| оновити python | `git push` |
| оновити ods | `git push origin main:ods` |
| оновити обидва | `git push origin main main:ods` |
| статика відстала | `bin/www python origin/main` · `bin/www ods origin/ods` |
| відкотити ods | `git revert <sha>`, потім `git push origin main:ods` |
| стан на сервері | `sudo vv check ods-labs` |
| журнали | `sudo journalctl -u ods-labs-web -n 50 -o cat` · `-u ods-labs-bot` |

- Правка ядра їде на python з кожним push у `main`, на ods — коли пересунуто гілку `ods`. Версії ядра на сайтах можуть на якийсь час розійтись; бази в них окремі.
- Після першої правки на сайті md у `sites/ods/data/` — архів: повторний `content_io.py` у базу сервера затер би правки.
- Бекапу бази поза сервером ще нема (vps-infra T36/Q11). Після запуску тексти лекцій живуть у Mongo сервера.

## Побічні знахідки

Не блокують ods.

- **Страховий файл опитувань на сервері не пишеться.** Бот кладе копію кожного апдейта опитування в `logs/poll_updates.jsonl` у теці запуску. На сервері це `repo/app/api/`: тека належить root, юніт бота працює з `ProtectSystem=strict` і без `RW_PATHS`. Запис падає, помилка йде в журнал, голос у Mongo доходить. Звіт [T176](../../tgbot/.t/T176--polls-v1/report.md) чекає на сервері файл, якого не буде. Варіанти — T181 Q6.
- **`AGENT_TOKENS` у маніфесті python-labs.** У незакоміченому `apps/python-labs/env.conf` ключа нема, а на сервері він, судячи з `.site/prod/`, є. Після `self-update` він стане «поза env.conf»: у редакторі схований, а `vv env set python-labs AGENT_TOKENS` відмовить. Додати рядок `AGENT_TOKENS!` тим самим комітом.
- **Cookie сесії без `Secure`** на обох сайтах. Caddy переводить http на https, HSTS вимкнено. Дрібниця ядра на потім.

## Твої думки та питання

> 
