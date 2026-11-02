# T250 · Деплой ods через місяць: що змінилося, репетиція на HEAD, порядок дій

`2026-11-01` · 💡 proposal

Контекст:
- запит Vitalik (чат, 2026-11-01): «Давай задеплоїмо ODS-сайт. Досліди, що для цього потрібно… я досі чомусь боюся цього кроку. Та його треба зробити. Проєкт VPS Infra також треба дослідити… ідеї, як зробити це ще зручніше та швидше й не боятися… Задеплоїти, мабуть, треба і сайт, і окремого бота»;
- план місячної давнини — [T180](T180-P--ods-deploy-plan.md) (2026-10-01), вибори без відповідей — [T181](T181-Q--ods-deploy-choices.md) (план іде за «a»); тут — що з того часу змінилося, що перевірено сьогодні заново, і що ще заважає;
- vps-infra читав і **дописав**: маніфест `apps/ods-labs/`, картка, задача [T76](../../../../../My/vps-infra/.dev/apps/ods-labs/.t/T76--ods-labs/plan.md) з логами блоків 0–7 — повний runbook команд для сесії `ssh vv3`; код `vv`/`deploy` не чіпав;
- нові вибори — [T251](T251-Q--ods-deploy-go-choices.md), мовчання = «a».

## Коротко

- План T180 чинний: `vv` і `deploy` міняти не треба, ods — ще одна тека маніфесту. Сервера так ніхто й не торкався; гілок `ods`/`www-ods` на GitHub нема; vps-infra лежить із незакоміченим кроком 4e (`env.conf`) **з 2026-09-27** — це перший камінь.
- Сьогодні на HEAD `6581fc7` повторено репетицію T180: чистий клон → venv 3.12 → старт без `.env` і без `sites/ods/data` → health 200; смоуки; збірка; маніфест через актуальний `vv`. Усе проходить, крім відомої колізії `/api/labs` (26/28), яка лекцій не стосується.
- Усе, що не сервер, зроблено або розписано. Лишаються твої дії поза кодом (бот, OAuth, 1Password, два пуші) і одна сесія `ssh vv3` на 40–60 хвилин, яку можна різати на будь-якому блоці.
- Чого боятись не треба: python-labs ods не чіпає ні на одному кроці, крім двох спільних речей — коду `vv` при `self-update` (а `deploy` — bash і від `vv` не залежить) і файла Caddy при `site apply` (валідація на копії, самовідкат). Єдиний справжній спільний ресурс — памʼять машини, і на неї в блоці 4 стоїть гейт.

## Перевірено сьогодні (ноутбук, HEAD `6581fc7`)

| Що | Як | Результат |
|:---|:---|:----------|
| venv як на сервері | чистий `git clone` у скретч, `uv sync --frozen --project sites/ods/api --python 3.12 --no-dev`, свій `UV_PROJECT_ENVIRONMENT` | 64 пакети (як у T180), 1.6 с з кешу; `uv.lock` ods досі дорівнює lock python по пакетах — залежності ядра з 2026-09-29 не мінялись |
| старт без диска | `env -i` з `MONGO_URI DB_NAME SESSION_SECRET SITE_URL FAKE_USER_EMAIL=` — без `.env`, без `sites/ods/data` | `/api/health` → `{"ok": true}` через **17 с** (перший старт: компіляція байткоду; на vv3 python-labs піднімається за ≈11 с); гість `/api/me` 200; `/api/auth/login` з заголовками Caddy → `redirect_uri=https://ods.labs.in.ua/api/auth/callback` |
| смоуки | `DB_NAME=ods_smoke uv run --frozen python tests/smoke_ods.py` і `smoke_labs.py` у `sites/ods/api` | **10/10**; **26/28** — два падіння `GET /api/labs → 403 Forbidden`: роутер дедлайнів ядра (T235) має той самий префікс і включається раніше ([T238](T238-Q--ods-labs-2-5-questions.md) Q6) |
| статика | `npm run build` у `sites/ods/vue` | 0.8 с, `dist/` 1.9 МБ (один чанк 547 КБ — попередження Vite, не помилка) |
| маніфест | копія vps-infra (з незакоміченим 4e) + `apps/ods-labs/` з T180 → `./vv/bin/vv apps`, `show`, `render unit\|caddy\|tmpfiles\|sysusers` | без помилок: `WORKDIR=/srv/ods-labs/repo/sites/ods/api`, Caddy → `127.0.0.1:8035`, секція `# env.conf` з `DB_NAME=ods_labs`, `SITE_URL=https://ods.labs.in.ua` |
| DNS / зовні | `dig`, `curl` | `ods.labs.in.ua → 185.65.245.199` (wildcard); HTTPS ще нема — очікувано; `python.labs.in.ua` → 200 |
| GitHub | `git ls-remote --heads origin` | лише `main`, `www`; локальний `main` на 2 коміти попереду (T248/T249, твої) |
| хук | `git config core.hooksPath` | `bin/hooks` — pre-push збере `www-ods` при пуші в `ods` |
| база | `mongosh ods` | `guide` 20 (`lec01…lec15` + `lab1…lab5` — **старі** тексти лаб), `media` 123 (7.5 МБ), `users` 1 — `dev@nure.ua` зі статусом admin, `activity` 1048, `history` 22, `variants` 0 |

Сервера не торкався: ключ vv3 під `v6u` — `~/.ssh/id_ed25519_vps_56429` з passphrase і `AddKeysToAgent 1m` (vps-infra T46 виконано) — з моєї сесії без твоєї `ssh vv3`/`ssh-add` вхід `Permission denied`; це задумано.

## Що змінилося з T180

1. **vps-infra так і не закомічено.** Крок 4e (`env.conf`, `env edit` без секретів у редакторі, `env set`) — 18 файлів, +360/−73, симуляція 40 кейсів 2026-09-27, на vv3 не їздив; плюс два незапушені docs-коміти. На машині `vv` досі зі старим `ENV_KEYS`, бот python з лімітом 256M. Маніфест ods у T180 — у форматі `env.conf`, тобто **4e має доїхати першим** (або ods переписати на `ENV_KEYS` — T251 Q1).
2. **Колізія `/api/labs`** (з 2026-10-25): ядро `core/api/core/routes/labs.py` (дедлайни, адмін) і ods `routes/labs.py` (лаби студента) — один префікс, ядро виграє, студент отримує 403. Сайт лекцій не чіпає; сторінку «Моя лаба» ламає. Виправлення — префікс ядра → `/api/deadlines` (1 файл API + 3 рядки `core/ui/api.js`); T238 Q6 казав «у тій сесії» — вона не жива, конфліктів у дереві нема (T251 Q2).
3. **Ядро виросло** (заняття, Zoom, дедлайни, таблиця, репозиторії — 20 комітів у `core/`), але залежності ті самі: lock ods актуальний, venv-рецепт T180 без змін.
4. **Лаби:** на сайті (у базі) — старі пʼять текстів; нові 1–5 ([T234](T234--ods-labs-2-5-ready/report.md)) — на диску, імпорт — T238 Q5. Деплой цього не чекає: `GUIDE_READERS=active`, активних студентів на ods ще нема (T251 Q3).
5. **Доступ агента до сервера** з-під `v6u` існує, але у вікні `ssh-add` і без `sudo` (T251 Q6).
6. `bin/guide snap` для цілі не `prod` без `--to` писав би лекції ods у `data/guide/` (git) — **закрито цією сесією**: відмовляє, поки не вказано `--to` (T180 блок 7, T181 Q5 a).

## Що заважає — і що з цим робити

| # | Перешкода | Дія | Хто |
|---|---|---|---|
| 1 | 4e на vv3 нема | коміт незакомічених змін vps-infra (+ `AGENT_TOKENS!` у `apps/python-labs/env.conf`) → push → `sudo vv self-update` → перевірка за log/4e | ти (коміт, сесія); runbook — T76 log/01 |
| 2 | гілок `ods`/`www-ods` нема | `git push origin main main:ods` або `origin/main:refs/heads/ods` — хук збирає статику | ти — T76 log/00 §0.5, T251 Q5 |
| 3 | бот, OAuth, 1Password | BotFather, Cloud Console (той самий проєкт, consent screen уже production), пʼять записів | ти — T76 log/00 §0.2–0.4 |
| 4 | dev-адмін у локальній базі | seed-копія `ods_seed` з `guide` + `media` → `db push --from ods_seed`; локальну `ods` не чіпати | ти — log/00 §0.6 (команда готова), T251 Q4 |
| 5 | колізія `/api/labs` | префікс ядра → `/api/deadlines`, смоуки обох сайтів | я, на твоє «так» (T251 Q2) |
| 6 | памʼять vv3 | `free -m` до/після старту ods, гейт `available` > 250M, інакше бот стоп до рішення | ти — log/04, T251 Q7 |

## Ризики — що може піти не так і що тоді

- **Памʼять.** 1.9 GiB; зараз ≈ 4 боти × 165–200M + web 200M + Mongo (кеш 0.25 GiB уже обрізано) ≈ 1.3–1.4 GiB; ods додає ≈ 375M. Своп 2 GiB не дасть OOM, але одноядерна машина у свопі — повільна для всіх. Гейт у блоці 4; запасні ходи — бот ods пізніше або тариф з 4 GiB.
- **Health на першому деплої.** `deploy` чекає ≈ 35 с (`sleep 5` + `curl --retry 10 --retry-delay 3`); перший старт на ноутбуці — 17 с, python на vv3 — 11 с. Якщо не вкладеться — `FAILED: curl`, маркер `failed`, і `sudo deploy ods-labs --force` з другої спроби (байткод уже скомпільовано). Не ламає нічого.
- **`self-update` з 4e.** Міняє CLI `vv` і дзеркало `/etc/vv/apps`; не міняє `deploy` (bash зі своїми дефолтами), юніти, Caddy, `shared/env`. Відкат — `git revert` → `self-update`. Автодеплой python живе своїм життям увесь час.
- **`site apply`.** Валідація копії, самовідкат при помилці; у найгіршому разі — `rm` файла сайту + `reload`.
- **OAuth.** `redirect_uri_mismatch` → адреса в клієнті не точна; `403 access_denied` → consent screen не production (він production — python-labs блок 6). `hd=nure.ua`; твоя пошта — через `ADMIN_EMAILS`.
- **409 бота** — лише якщо локальний `python -m bot` запустити на прод-токені; токен у `.env` ноутбука не класти.
- **`AGENT_TOKENS!`** — `env edit` не пропустить порожнього; токен — `openssl rand -hex 32`.
- **Deploy key.** Другий ключ на той самий репо — норма; без гілки `ods` на GitHub `repo init` дасть підказку про ключ, яка збиває з пантелику.
- **Контент.** Після першої правки на сайті md на диску стає архівом; бекапу Mongo поза сервером нема ні в python, ні в ods (vps-infra T36/Q11) — після go-live це питання стає гострішим: лекції живуть лише на vv3.

## Щоб швидше, зручніше й не боятись

- **Усе поза сервером — готове.** Маніфест (перевірений), картка, план і сім логів із командами ≤70 символів, «Чекаємо» і «Якщо пішло не так» на кожен блок, відкат кожного блоку. Твоя робота — вставляти команди й читати, чи збігається екран з «Чекаємо».
- **Блоки незалежні, зупинка безпечна.** До блоку 5 зовні нічого не видно; до блоку 6 код не запускається таймером (`STATE=planned` — `deploy` відмовляє); бот після блоку 4 уже живий, але це лише `🚀 Бот запустився` тобі. Можна зробити 1–3 одного вечора (ніщо не працює, нічого публічного), 4–6 — іншого.
- **Гейт після кожного блоку** — `sudo vv check --all`: рядок `python-labs ok` має лишатись. Якщо ні — зупиняємось, вивід мені.
- **Seed замість чистки:** `ods_seed` з двох колекцій — повторювано, локальна база жива, dev-адмін на сервер не потрапляє фізично.
- **Мій доступ на час сесії** (T251 Q6): `ssh-add -t 2h ~/.ssh/id_ed25519_vps_56429` — і я сам читаю `free -m`, `systemctl is-active`, health з `127.0.0.1:8035`, роблю зовнішній смоук; `sudo`-команди лишаються твоїми. Менше копіювання туди-сюди.
- **Після ods — `vv up`** (vps-infra T58 крок 8): два повні комплекти логів (python-labs, ods-labs) — це і є специфікація однієї команди; третій сайт (oop наступного року) — одна команда замість семи блоків.
- **Сповіщення деплоїв у Telegram** (vps-infra T37) — щоб бачити «доїхало» без `ssh`; окрема коротка сесія у vps-infra.

## Порядок (деталі — vps-infra T76)

0. Ноутбук (≈15 хв): бот, OAuth, 1Password, `git push origin main main:ods`, `ods_seed` → [log/00](../../../../../My/vps-infra/.dev/apps/ods-labs/.t/T76--ods-labs/log/00-local.md).
1. vps-infra: два коміти (4e; ods-labs) → push → `ssh vv3`: `self-update`, `check` → [log/01](../../../../../My/vps-infra/.dev/apps/ods-labs/.t/T76--ods-labs/log/01-manifest.md).
2. `tenant add` → `repo init` ×2 (Deploy key) → `venv sync` → [log/02](../../../../../My/vps-infra/.dev/apps/ods-labs/.t/T76--ods-labs/log/02-tenant.md).
3. `db add` → `env edit` → `db push --from ods_seed` (ноутбук) → [log/03](../../../../../My/vps-infra/.dev/apps/ods-labs/.t/T76--ods-labs/log/03-data.md).
4. `free -m` → `unit apply` → `start --kill-test` → `free -m` → гейт → [log/04](../../../../../My/vps-infra/.dev/apps/ods-labs/.t/T76--ods-labs/log/04-units.md).
5. `site apply` → смоук ззовні → [log/05](../../../../../My/vps-infra/.dev/apps/ods-labs/.t/T76--ods-labs/log/05-caddy.md).
6. `STATE` → live → push → `self-update` → `deploy` → вхід, лекція, слайди → `timer on` → `check --all` → [log/06](../../../../../My/vps-infra/.dev/apps/ods-labs/.t/T76--ods-labs/log/06-autodeploy.md).
7. Бот `/here`, студенти, `ODS_URL`/`ODS_TOKEN` у `.site/.env`, доки → [log/07](../../../../../My/vps-infra/.dev/apps/ods-labs/.t/T76--ods-labs/log/07-operate.md).

«Як жити після» — таблиця в T180 чинна без змін: оновити ods — `git push origin main:ods`, обидва — `git push origin main main:ods`, стан — `sudo vv check ods-labs`.

## Зроблено цієї сесії (код і доки)

- `bin/guide`: `snap` з `-t` не `prod` вимагає `--to`; `--to` без дефолту в аргументах, `data/guide/` — лише для `prod` (push на prod, як і раніше, закінчується знімком).
- vps-infra: `apps/ods-labs/*` (4 файли), `apps/python-labs/env.conf` + `AGENT_TOKENS!`, вузол `.dev/apps/ods-labs/` (картка, T76 план, 8 логів), рядок реєстру, CHANGELOG.
- python-labs: цей тікет, T251, README ods, CHANGELOG. Коміти — твої, меседжі в чаті.

## Твої думки та питання

> 
