# T93 · Plan: етап C — перейменування за T92 + фронт «Моєї гри»

`2026-08-16` · рішення [T92](../T92-Q--naming-urls.md) — відповіді в чаті: **всі «a»** + «кошик» для файлів; дизайн — [T90](../T90-P--my-game-v1-design.md).

## Рішення T92 (зафіксовано)

- Q1a: гра студента = **`Game`** (колекція `student_games`), каталожний клас → **`BaseGame`** (колекція `games` і роути без змін).
- Q2a: обʼєкт вікно/меню = **`Part`** (колекція `game_parts`); поле заявки `object` → `part` — узгодження мови.
- Q3a: **`Claim`** лишається.
- Q4a: сторінки — `/my/game` (редактор), `/students` (галерея карток + адмін-таблиця перемикачем), `/students/<nick>` (паспорт гри; nick = пошта до `@`), `/students/<nick>/edit` (адмін); API — `/api/my/game…`, `/api/my/claims`, `/api/students…`.
- Бонус (чат): видалення файлів → **кошик** `uploads.trash/` замість unlink — ніщо не зникає назавжди.

## Кроки

1. **Бекенд**: `models/base_game.py` (BaseGame) · `models/game.py` (Game/Part/Claim, жива база порожня — без міграцій) · роути `my_game.py` / `my_parts.py` / `my_claims.py` / `student_games.py` (галерея з role-shaped полями + паспорт по nick) · `students.py` — get/put по nick · `User.nick` + `by_nick()` · кошик в `uploads.py` · `main.py`/`db.py`/`.gitignore`.
2. **Смоук**: переписати під нові шляхи (`tests/smoke_games.py` замість `smoke_works.py`) + нові перевірки: кошик, галерея (адмін бачить pending і пошти, студент — ні), nick-лукап.
3. **Фронт**: `api.js` (+upload-хелпер) · router/NavBar («Студенти» всім активним, «Моя гра») · `/my/game` — редактор (гра, вікна з типами/скриншотами/чіпами заявок, меню з пунктами, заявки рівня гри, автопідказки пар volume-control→sound-volume, music-toggle→background-music) · `/students` — галерея+таблиця · `/students/<nick>` — паспорт · edit по nick; `GameForm.vue` → `BaseGameForm.vue`.
4. `npm run build` чистий, смоук зелений; report, живі доки, коміт-меседж.
