# T141 · SESSION_SECRET і UPLOADS_DIR: навіщо і звідки на VPS

`2026-09-26` · 🔆 clarification

Контекст: питання Vitalik у чаті перед заповненням `/srv/python-labs/shared/env` на vv3 (vps-infra [T61](../../../../../My/vps-infra/.dev/apps/python-labs/.t/T61--python-labs/plan.md), крок 3). Обидві змінні — з `app/api/config.py`; повний список ключів проду — `ENV_KEYS` у маніфесті vv (11 ключів, [T58](../../../../../My/vps-infra/.dev/vv/.t/T58--vv-phase2/log/4c-env-edit.md) 4c).

## SESSION_SECRET

- **Навіщо.** Ключ, яким Starlette `SessionMiddleware` підписує session-cookie (`app/api/main.py`). У сесії лежить `email` залогіненого і `next` для повернення після Google-редиректу (`routes/auth.py`). Без підпису cookie можна підробити і зайти під будь-якою поштою, включно з адмінською.
- **Обовʼязковий.** Поле в `Settings` без дефолту → без нього застосунок не стартує; локально в `.env` — з [T44](T44--auth-mvp/report.md).
- **Генерує Vitalik руками** — на сервері його ніхто не створює: `vv env edit python-labs` дописує лише порожній рядок `SESSION_SECRET=`, `vv check` скаже «порожні». За T61 (log/00-local, log/03-data):
  - `openssl rand -hex 32` (де запускати — байдуже; план каже «на ноутбуці», щоб значення одразу лягло в 1Password);
  - **новий, не той, що в локальному `.env`** — дев і прод не ділять секрет;
  - запис 1Password `python-labs SESSION_SECRET (prod)` → вставити в `shared/env`.
- Зміна секрету пізніше розлогінює всіх (cookie з чужим підписом не читаються) — при першому деплої неістотно.

## UPLOADS_DIR

- **Що це.** Тека скриншотів студентських ігор («Моя гра», [T90](T90-P--my-game-v1-design.md) / [T91](T91--my-game-backend/report.md)): `uploads.py` кладе файли `<тека>/<game-id>/<uuid>.<ext>` (png/jpg/webp/gif, ≤ 8 МБ), `main.py` роздає їх `StaticFiles` на `/api/uploads`. Видалені не зникають, а переїжджають у сусідню `<тека>.trash/` — код виводить її сам із `UPLOADS_DIR` (`ROOT.parent / (ROOT.name + ".trash")`), окремо задавати не треба.
- **У коді необовʼязковий:** порожньо = `app/api/uploads/` поруч із кодом (git-ignored). Локально не потрібен; лише смоуки ставлять `UPLOADS_DIR=/tmp/pl-smoke`, щоб не смітити в робочій теці.
- **На VPS обовʼязковий і потрібен:**
  - код на сервері живе в релізному чекауті, який деплой замінює → файли поруч із кодом зникли б після наступного релізу; тому `shared/` поза релізами;
  - маніфест vv тримає `UPLOADS_DIR` в `ENV_KEYS` без `?` → порожнє значення = помилка `vv check`;
  - `RW_PATHS` дає сервісу право писати лише в `shared/uploads` і `shared/uploads.trash` (systemd-пісочниця, решта read-only);
  - бекап скриншотів — поруч із mongodump у тому ж `shared/` (README платформи, блок «Моя гра»).
- Значення проду: `UPLOADS_DIR=/srv/python-labs/shared/uploads`.

## Твої думки та питання

> 
