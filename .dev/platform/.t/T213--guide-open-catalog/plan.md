# T213 · Ігри й таски відкриті всім, каталог без чернеток — план

`2026-10-13` · ⚙️ задача · запит Vitalik у чаті · замок — [T136](../../../.t/T136--guide-hidden/report.md) + [T159](../T159--guide-closed-again/report.md) · заглушка каталогу — [T116](../../../.t/T116-Q--guide-questions.md) Q13 · звіт — [report.md](report.md)

Запит (чат, 2026-10-13): «Давай зробимо видимою методичку: ігри й таски. Думаю, це можна зробити видимим не тільки для студентів, а й загалом відкритий доступ. Там же інакше немає нічого секретного? А також давай приберемо статус чернетки з усіх ігор і тасків. Усе одно насправді всі-всі вони поки що чернетки.»

## Як є

- Уся методичка — лише адміну й агенту: `hidden` у `router.js`, `GUIDE_READERS=admin` (T136, T159).
- `/games` і `/tasks` — текст розділу був би всім, каталог усередині — `v-if="admin"` із заглушкою «🚧 відкриється незабаром» (T116 Q13).
- `GET /api/games`, `GET /api/tasks` — уже відкриті гостю (`viewer`), не-адмін бачить лише `active`.
- Чернетки в каталозі: 8 ігор із 17, 135 тасків із 209 — однаково в деві, на сервері й у знімку `data/catalog/`.

## Рішення

- Відкрити всім, і гостю: `/games`, `/games/<slug>`, `/tasks` — текст розділу й каталог. Решта методички — як була.
- Текст розділів гостю — через нове налаштування ядра `GUIDE_PUBLIC` (slug-и, відкриті всім, без чернеток); `GUIDE_READERS` не чіпати.
- Усі чернетки каталогу → `active` на сервері через `bin/catalog` (кожна правка в історії), знімок у git — із сервера, дев — імпортом знімку. Статус `draft` у механіці лишається: нова картка народжується чернеткою.

## Кроки

- [x] Ядро: `guide_public` у `config.py`, `page_reader` у `routes/guide.py`; `site.env`: `GUIDE_PUBLIC=game,tasks`; `core/README.md`.
- [x] Фронт: `router.js`, `GamesPage.vue`, `TasksPage.vue`, `GamePage.vue`, `GuideHead.vue`, `StartSteps.vue`, `crumbs.js`.
- [x] Каталог: `bin/catalog pull` → статуси → `push` (143) → `snap`; дев — `catalog_io.py import`.
- [x] Смоуки (`smoke_guide`, `smoke_agent`, `smoke_games`), `npm run build`, стенд у headless Chrome гостем і адміном.
- [x] Доки: README platform / games / tasks / кореневий, `app/README.md`, `data/guide/README.md`, `data/catalog/README.md`, CHANGELOG, STATUS.
