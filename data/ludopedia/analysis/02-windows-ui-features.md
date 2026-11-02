# 02 · Вікна, HUD, фічі поза полем — каталог з корпусу

`2026-11-02` · корпус: **169 ігор** · числа — з [index/harvest.md](../index/harvest.md) (секції «Вікна, меню, HUD» і «Фічі поза полем»; автоген, свіжіший за цей файл). Питання, на яке відповідає зведення: **які вікна, елементи інтерфейсу й «фічі поза полем» справді трапляються в іграх і як часто** — щоб каталог завдань (interface/*, game-logic/save, levels/progression) і типи вікон для «Моєї гри» спирались на корпус, а не на здогад.

## Вікна — частоти (зі 169 ігор)

| Ранг | Вікно | Ігор | Статус у каталозі | Коментар |
|---|---|---|---|---|
| 1 | `game-screen` | 169 | ✅ | завжди |
| 2 | `end-screen` | 125 | ✅ | перемога/поразка/результат раунду — у 3/4 ігор; варто сімʼю win/lose (T88 хвіст) |
| 3 | `main-menu` | 100 | ✅ | |
| 4 | `settings-window` | 81 | ✅ | |
| 5 | `help-window` | 58 | ✅ | правила/довідка — частіше, ніж здається |
| 6 | `splash-screen` | 49 | ✅ | |
| 7 | `leaderboard` | 44 | ✅ | |
| 8 | `custom-window` | 42 | ✅ | «своє вікно» просять 1/4 ігор — ознака, що типів бракує (див. кандидати нижче) |
| 9 | `pause-menu` | 33 | ✅ | |
| 10 | `level-select` | 29 | ✅ | |
| 11 | `editor-window` | 22 | ⏳ | редактор рівнів як окремий екран |
| 12 | `shop-window` | 21 | ✅ | |
| 13 | `stats-window` | 20 | ⏳ | статистика гравця |
| 14 | `mode-select` | 19 | ⏳ | вибір режиму |
| 15 | `map-window` | 18 | ⏳ | карта світу/підземелля на весь екран |
| 16 | `lobby-window` · `difficulty-select` · `puzzle-select` | 17 | ⏳ | мультиплеєр · складність · сітка пазлів з позначками |
| 19 | `tutorial-window` · `replay-window` | 13 | ⏳ | |
| 21 | `codex-window` | 12 | ⏳ | бестіарій/енциклопедія елементів — прямий аналог «паспорта гри» |
| 22 | `confirm-dialog` | 11 | ✅ | |
| 23 | `achievements-window` · `character-select` · `game-over-continue` | 10 | ⏳ | |
| 26 | `save-slots` · `dialogue-window` | 9 | ⏳ | |
| 28 | `upgrade-window` · `inventory-window` | 8 | ⏳ | |
| 30 | `match-setup` · `skin-select` · `hints-window` | 7 | ⏳ | налаштування партії (гравці/раунди/арена) |
| 33 | `log-window` · `about-window` · `profile-window` · `daily-window` · `level-password` | 6 | about ✅, решта ⏳ | |

Висновки для каталогу типів вікон (тег `window`, зараз 13):
- **Додати як картки** (≥10 ігор, нема в каталозі): `editor-window` 🥈 (редактор — екран, окремо від підзони levels/editor з інструментами), `stats-window` 🌱, `mode-select` 🌱, `map-window` 📎, `difficulty-select` 🌱, `puzzle-select` 📎 (сітка рівнів зі статусом — для класу пазлів це головне меню), `lobby-window` 📎, `tutorial-window` 📎, `replay-window` 📎, `codex-window` 📎, `achievements-window` 🌱, `character-select` 🌱, `game-over-continue` 🌱.
- `end-screen` варто розщепити на сімʼю: `win-screen` · `lose-screen` · `round-summary` (у настолках і versus — зведення раунду, не перемога) — відповідає хвосту T88.
- `custom-window` ×42 — переглянути тексти в файлах: більшість — це `codex`, `round-summary`, `match-setup`, `placement-screen` (розставити кораблі/фігури до партії — Battleship, Stratego, Khet), `pass-device` (hot-seat «передай пристрій»), `attract-demo` (аркадний demo-режим), `code-editor` (program-robots), `chapter-select`, `variant-select` (вибір варіанту правил — lichess, Tatham), `placement-screen`. Це кандидати другого кола.

## HUD-елементи — частоти

Топ-30 зі 169 ігор: `score` 48 · `level-number` 27 · `lives` 26 · `turn-indicator` 21 · `remaining-counter` 20 · `timer-countdown` 20 · `legal-move-highlight` 18 · `undo-button` 18 · `coins` 17 · `hi-score` 16 · `timer-elapsed` 14 · `conflict-highlight` 12 · `restart-button` 11 · `move-counter` 10 · `hp-bar` 10 · `inventory-bar` 10 · `turn-counter` 9 · `selection-highlight` 8 · `minimap` 8 · `player-clock` 8 · `move-list` 8 · `objective-text` 8 · `message-log` 8 · `tooltip` 7 · `last-move-highlight` 7 · `popup-text` 6 · `drag-ghost` 6 · `wave-counter` 6 · `hint-button` 6 · `score-preview` 5.

Що це каже про підзону interface/hud (зараз у каталозі — жменька карток):
- **Ядро HUD, яке є майже в усіх класах**: лічильники (`score`, `lives`, `level-number`, `remaining-counter`, `timer`), кнопки керування ходом (`undo`, `restart`, `pause`, `hint`) — це кандидати в сімʼю `hud-counters` (батько 📎, діти 🌱 кожен) і сімʼю `game-controls`.
- **Підсвітки** — окрема сімʼя для класів `figure`/`puzzle`/`cursor`: `legal-move-highlight` 18, `conflict-highlight` 12, `selection-highlight` 8, `last-move-highlight` 7, `reachable-highlight`, `threat-range`, `telegraph-marker`, `path-preview`. У каталозі є лише `legal-move-highlight` [chess]. Пропозиція: сімʼя `highlights` з 6–8 дітьми 🌱/📎.
- **Текстові панелі**: `objective-text`, `message-log` (роглайки), `tooltip`, `popup-text`, `toast` — сімʼя `feedback-text`.
- **Специфічні для сімей**: `next-piece-preview`/`hold-slot`/`ghost-piece`/`garbage-meter` (падаючі), `player-clock`/`move-list`/`captured-pieces`/`pocket` (фігурні), `pencil-marks`/`mistake-counter`/`check-button` (пазли), `wave-counter`/`range-circle` (TD), `instruction-highlight`/`code-editor` (програмування). Це аргумент тримати в каталозі теги класу/сімʼї на картках HUD.

## Фічі поза полем — частоти

Топ зі 169 ігор: `undo` 54 · `levels-sequential` 40 · `online-multiplayer` 38 · `custom-rules` 37 · `ai-opponent-levels` 35 · `stats` 33 · `difficulty-presets` 32 · `autosave` 32 · `level-editor` 32 · `puzzle-bank` 31 · `hotseat` 30 · `leaderboard-online` 29 · `achievements` 28 · `leaderboard-local` 27 · `replay` 26 · `restart-level` 26 · `custom-difficulty` 25 · `tutorial` 23 · `level-unlock` 23 · `export-import` 20 · `seed-input` 20 · `unlockables` 19 · `share-code` 19 · `redo` 19 · `turn-timer` 18 · `save-slots` 18 · `hint` 18 · `daily-puzzle` 18 · `meta-progression` 17 · `theme-select` 16 · `level-sharing` 15 · `mode-daily` 14 · `cloud-save` 14 · `local-multiplayer` 14 · `mode-versus` 14 · `pause` 13 · `auto-check` 12.

Висновки:
- **`undo` — у третині ігор** (54) і жодної картки в каталозі (лише `editor-undo`). Разом із `redo` 19 і `rewind` 6 це сімʼя `undo-redo`: `undo-step` 📎 · `undo-unlimited` 🥉 · `redo` 🌱 · `rewind-continuous` 🥈 (Catrap, Braid-подібне) · `reset-level` 🌱. Найбільша прогалина корпусу.
- **`custom-rules` ×37** — конструктор варіантів правил (розмір поля, кількість мін, набір правил Tatham, варіанти lichess, Life B/S) — у каталозі є лише `difficulty-levels`. Пропозиція: картка `rule-variants` 🥉 зі слотом {what: text} + дитина `variant-select` вікно.
- **`seed-input`/`seed-display`/`share-code` (20/6/19)** — відтворюваність і обмін: картка `seed-share` 📎 (показати/ввести seed, код рівня) — важлива для пазлів і роглайків, дешева.
- **`puzzle-bank` ×31, `daily-puzzle` ×18** — для класу `puzzle` це основа прогресії (є картки `level-bank`, `daily-puzzle` ✅).
- **`auto-check` ×12, `hint` ×18, `auto-solve` ×8** — «помічники розвʼязання» для пазлів: сімʼя `solver-aids`: `auto-check` 📎 · `hint-cell` 🥉 · `auto-solve` 🥇 · `mistake-limit` 🌱 — частково є (`level-solver`, `hint`).
- **Режими** (`mode-*` разом ≈60 згадок): `versus` 14 · `daily` 14 · `coop` 9 · `hardcore` 8 · `endless` 8 · `classic` 7 · `zen` 6 · `puzzle` 6 · `time-attack` 6 — картка `game-modes` 📎 зі слотом {modes: text} або сімʼя з дітьми 🌱.
- **Мультиплеєр**: `online` 38 · `hotseat` 30 · `local` 14 · `ai-opponent-levels` 35 · `turn-timer` 18 — підзона game-logic/opponent має `hot-seat`, `ai-opponent`, `move-timer`; бракує `online-multiplayer` 🥇/👑 і `async-multiplayer` (ходи поштою — Letterpress, Words With Friends) 🥈.
- **Доступність** (`colorblind-palette` 6, `remap-controls` 7, `speed-control` 7, `font-scale`, `assist-mode`): рідко описані в джерелах, але це сильна тема для курсу — сімʼя `accessibility` (controls-remap уже є).
- Слова поза словником, які агенти вживали ≥4 рази: `level-select`, `rating`, `save-progress`, `save-game`, `score-records`, `level-password`, `progress-acceleration`, `permadeath`, `roster-carryover`, `run-relics` — перші шість просто дублюють slug-и каталогу (агенти брали картки замість слів словника — нормально), **нові**: `permadeath` ×4 (одне життя, сейв стирається — роглайки, Fire Emblem), `roster-carryover` ×4 (загін переходить між місіями), `run-relics` ×4 (реліквії забігу — роглайти).

## Типові набори по класах (що описувати студентові як «мінімум»)

- `avatar` (аркади, пазли-штовхання): game-screen + HUD (lives/score/level/timer) · main-menu · end-screen · pause · level-select або password · settings (звук) · help.
- `cursor` (match/TD/сапер): game-screen + лічильники (remaining, moves, coins) · mode/difficulty-select · settings · leaderboard · end/round-summary.
- `figure` (шахи/тактики): game-screen + turn-indicator, player-clock, move-list, legal-move-highlight · match-setup (сторони, AI, час) · end-screen (результат + причина) · replay/analysis · lobby (онлайн).
- `puzzle` (паперові): game-screen + pencil-marks, conflict-highlight, check/hint buttons, timer · puzzle-select/bank · difficulty · settings (auto-check, помітки) · stats/streaks · daily.

Ці чотири набори — готовий «стартовий чек-ліст вікон» для «Моєї гри» за класом (меню для студента з T98 «еталон = меню»).
