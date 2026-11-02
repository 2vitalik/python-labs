# T252 · Деплой ods: чекліст команд крок за кроком

`2026-11-02` · 🔆 clarification

Контекст:
- запит Vitalik (чат, 2026-11-02): «склади дуже короткий, лаконічний і конкретний план щодо деплою: які команди мені потрібно запустити та що зробити… щоб я міг просто виконати інструкцію крок за кроком і задеплоїти сайт та бота»;
- це стиснутий [T250](T250-P--ods-deploy-go.md) «Порядок» + runbook vps-infra [T76](../../../../My/vps-infra/.dev/apps/ods-labs/.t/T76--ods-labs/plan.md) (логи 00–07 — там «Чекаємо», відкати, «якщо пішло не так»); вибори [T251](T251-Q--ods-deploy-go-choices.md) — усе за «a» (мовчання);
- машини: 💻 ноутбук (python-labs / vps-infra), 🖥 сесія `ssh vv3`, 🌐 браузер. Зупинка після будь-якого блоку безпечна; до блоку 5 зовні нічого не видно.

## Блок 0 · 💻 Підготовка (≈15 хв, без сервера)

0. *(необовʼязково, T251 Q2)* Колізія `/api/labs` → `/api/deadlines`: скажи мені «так» — виправлю й прогоню смоуки **до** пушу в 0.4.
1. 🌐 BotFather: `/newbot` → назва `ODS Labs` → нік `ods_nure_bot` (зайнятий — `ods_labs_nure_bot`). Токен — одразу в 1Password, у `.env` ноутбука не класти.
2. 🌐 Google Cloud Console → проєкт python-labs → APIs & Services → Credentials → Create credentials → OAuth client ID → Web application → назва `ods-labs prod` → Authorized redirect URI рівно `https://ods.labs.in.ua/api/auth/callback`. Client ID + secret — у 1Password.
3. 1Password — чотири записи: `vv3 mongo ods_labs` (пароль 30 символів, літери+цифри, без спецсимволів) · `ods-labs TG_BOT_TOKEN (prod)` · `ods-labs Google OAuth (prod)` · `ods-labs AGENT_TOKENS (prod)` = `claude:<вивід openssl rand -hex 32>`.
4. Гілки `ods` + `www-ods` (хук `pre-push` сам збере статику; python отримає T248/T249 і задеплоїться сам):

```sh
cd "$HOME/Main Dropbox/Dev/Dev.v4/Nure/python-labs"
git push origin main main:ods
git ls-remote --heads origin        # чекаємо: main www ods www-ods
```

5. Seed-база (локальна `ods` не чіпається):

```sh
mongosh ods --quiet <<'JS'
const seed = "ods_seed";
db.getSiblingDB(seed).dropDatabase();
db.guide.aggregate([{ $out: { db: seed, coll: "guide" } }]);
db.media.aggregate([{ $out: { db: seed, coll: "media" } }]);
const s = db.getSiblingDB(seed);
print("guide", s.guide.countDocuments(), "media", s.media.countDocuments());
JS
```

Чекаємо: `guide 20 media 123`.

## Блок 1 · 💻→🖥 vps-infra: 4e + маніфест ods на машину

1. 💻 Два коміти і push (меседжі — у чаті 2026-11-02 / нижче):

```sh
cd "$HOME/Main Dropbox/Dev/Dev.v4/My/vps-infra"
git add vv/ apps/python-labs/ .dev/vv/README.md .dev/apps/python-labs/README.md \
  .dev/vv/.t/T58--vv-phase2/log/4e-env-secrets.md .dev/vv/.t/T74-C--env-step-answers.md .dev/vv/.t/T75-Q--env-conf-followup.md
git commit -m "feat(vv): env.conf, env edit without secrets, env set, t58,74-75"   # + тіло з чату
git add -A
git commit -m "feat: ods-labs manifest and runbook, KIND=job proposal, t76-77"    # + тіло з чату
git push
```

2. 🖥 `ssh vv3`:

```sh
sudo vv self-update                      # чекаємо: [~] env.py conf.py cli.py …, [+] ×4 /etc/vv/apps/ods-labs/
sudo vv check python-labs                # чекаємо: ok env ключі (12), без warn
sudo vv env edit python-labs             # у редакторі лише заглушки #! замість секретів → вийти без змін
sudo vv unit apply python-labs           # diff 256M → 384M, Записати? → y
sudo systemctl restart python-labs-bot
sudo vv check python-labs                # усе ok, restarts 0
sudo etckeeper commit "vv: unit apply python-labs"
sudo vv apps                             # ods-labs planned /srv/ods-labs, два юніти
sudo vv check --all                      # python-labs ok, ods-labs skip
```

## Блок 2 · 🖥 Тенант

```sh
sudo vv tenant add ods-labs
sudo vv repo init ods-labs               # код 77 + публічний ключ — це норма
```

🌐 github.com/2vitalik/python-labs → Settings → Deploy keys → Add deploy key: Title `vv3 deploy ods-labs`, Key — з екрана, **Allow write access — вимкнено**.

```sh
sudo vv repo init ods-labs               # чекаємо: repo/ = origin/ods
sudo vv venv sync ods-labs               # Installed 64 packages
sudo vv check ods-labs                   # ok user dir repo venv; решта fail — попереду
```

## Блок 3 · 🖥 + 💻 Дані

```sh
sudo vv db add ods-labs                  # пароль admin (1Password vv3 mongo admin), пароль ods_labs (vv3 mongo ods_labs)
sudo vv env edit ods-labs
```

У редакторі заповнити лише: `GOOGLE_CLIENT_ID` · `ADMIN_EMAILS` (твоя пошта) · `TG_BOT_NAME` (нік без `@`); `FAKE_USER_EMAIL` — лишити порожнім; `DB_NAME`/`SITE_URL`/`SESSION_SECRET`/`MONGO_URI` не чіпати. Зберегти, вийти → команда спитає прихованим вводом `GOOGLE_CLIENT_SECRET`, `TG_BOT_TOKEN`, `AGENT_TOKENS` (`claude:<hex>`). Чекаємо: `ключі (12)` без `бракує`/`порожні`.

```sh
sudo vv check ods-labs | grep -E 'env|db' # ok env, ok db ods_labs@ods_labs
```

💻 з ноутбука (спитає passphrase ключа і пароль sudo):

```sh
cd "$HOME/Main Dropbox/Dev/Dev.v4/My/vps-infra"
./vv/bin/vv db push ods-labs vv3 --from ods_seed   # чекаємо: 143 document(s) restored successfully
```

## Блок 4 · 🖥 Юніти й старт (бот оживає тут)

```sh
free -m                                  # запамʼятати available (якщо < 400M — стоп, вивід мені)
sudo vv unit apply ods-labs              # Записати? → y
sudo vv start ods-labs --kill-test       # ok active ×2, polling as @<нік>, ok health → 200
sudo etckeeper commit "vv: unit apply + start ods-labs"
sudo vv check ods-labs                   # ok … active active health; fail caddy — норма
```

Через хвилину:

```sh
free -m
sudo vv check --all | grep -E 'mem|restarts|^[a-z-]+ (ok|fail|warn)'
```

Гейт: `available` > 250M і своп не зріс → далі. Інакше `sudo systemctl stop ods-labs-bot` (сайт лишається), вивід мені.

## Блок 5 · 🖥 + 💻 Caddy (домен стає публічним)

```sh
sudo vv site apply ods-labs              # чекаємо: TLS ok · HTTP 404
sudo etckeeper commit "vv: site apply ods-labs"
sudo vv check ods-labs | grep caddy      # ok caddy
```

💻 смоук:

```sh
curl -sI https://ods.labs.in.ua/ | head -1                              # HTTP/2 404 (www/ ще порожній)
curl -sI https://ods.labs.in.ua/api/me | grep -iE '^(HTTP|server)'       # 200, server: uvicorn
curl -sI https://python.labs.in.ua/ | head -1                           # 200 — сусід живий
```

## Блок 6 · 💻→🖥→🌐 Перший деплой і автодеплой

1. 💻 У `vps-infra/apps/ods-labs/app.conf` прибрати рядок `STATE=planned` і коментар про нього → `git commit -am "chore: ods-labs goes live, t76"` → `git push`.
2. 🖥:

```sh
sudo vv self-update                      # [~] /etc/vv/apps/ods-labs/app.conf
sudo deploy ods-labs                     # none → <sha> … ok <sha>; на FAILED: curl → sudo deploy ods-labs --force
sudo vv check ods-labs | grep -E 'deploy|health|active'
```

3. 🌐 `https://ods.labs.in.ua/` — домашня; вхід Google поштою з `ADMIN_EMAILS`; лекція з формулами (`lec05`) — формули, картинки, слайди; приватне вікно — лекції гостю закриті.
4. 🖥:

```sh
sudo vv timer on ods-labs                # Записати? → y
sudo vv check --all                      # ods-labs ok, python-labs ok
free -m
```

## Блок 7 · Після

- Бот: у профілі на ods «Привʼязати бота» → Start у чаті; `/here` там, куди мають іти алерти адміна.
- Студенти: імпорт груп на `/students` до оголошення (лекції бачить лише підтверджений).
- Агент з ноутбука — у python-labs `.site/.env`: `ODS_URL=https://ods.labs.in.ua`, `ODS_TOKEN=<hex без claude:>`; перевірка `bin/guide -t ods ls` → 20.
- Нові тексти лаб 1–5 — `bin/guide -t ods push` або `content_io.py` (T238 Q5).

## Як жити після

Оновити ods — `git push origin main:ods`; обидва сайти — `git push origin main main:ods`; стан — `sudo vv check ods-labs`; журнал деплою — `sudo journalctl -u deploy@ods-labs.service -n 20 -o cat`.

## Твої думки та питання

> 
