---
title: Championship Lode Runner і Lode Runner Legacy
slug: lode-runner-sequels
aka: [Championship Lode Runner, チャンピオンシップロードランナー, Lode Runner Legacy]
family: grid-platformer
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: collect
year: 1984
platforms: [Apple II, C64, IBM PC, Atari 8-bit, Famicom, SG-1000, MSX, Windows (Steam, 2017)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Championship_Lode_Runner", best: true, note: "50 рівнів строго по черзі, без редактора, відновлення сейву коштує життя, сертифікат, паролі на Famicom"}
  - {kind: steam, url: "https://store.steampowered.com/app/628660/Lode_Runner_Legacy/", note: "Legacy 2017: режими Adventure, Puzzle (без ворогів), Classic 150, Extra, кооп, Craft, World Levels, Workshop"}
  - {kind: other, url: "https://mocagh.org/broderbund/masksun-loderunner-loderunner-manual.pdf", note: "мануал Championship: клавіші, Ctrl-команди, очки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Championship+Lode+Runner+gameplay", note: "пошук; геймплей"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lode+Runner+Legacy+gameplay", note: "пошук; геймплей Legacy"}
stage: v1
coverage: 50
mechanics: [sequential-levels, level-unlock, level-password, save-game, save-single-slot, level-select, mode-select, in-game-editor, editor-palette, level-exchange, leaderboard, avatar-picker, +save-costs-life, +completion-certificate, +puzzle-mode-no-enemies, +voxel-asset-editor, +local-coop-versus, +dig-hole, +hole-refill]
proposes: ["+feature:save-costs-life", "+feature:completion-certificate", "+feature:asset-editor", "+card:save-costs-life", "+card:puzzle-mode-no-enemies", "+card:voxel-asset-editor"]
author: opus
date: 2026-11-09
---

# Championship Lode Runner і Lode Runner Legacy — що два сиквели додають до правил Lode Runner: жорсткі рівні з ціною сейву і сучасний набір режимів з редактором персонажів

## Суть
Обидві гри грають за правилами [lode-runner](lode-runner.md): бігун, копання ям убік-униз, ями заростають, вартові, золото, драбина-вихід. **Championship Lode Runner** (Broderbund, 1984) міняє лише контент і метагру: 50 значно важчих рівнів строго по черзі, без редактора, сейв, відновлення якого коштує життя, і сертифікат за проходження. **Lode Runner Legacy** (Tozai Games, 2017) — воксельний ремейк, який розкладає ту саму механіку на режими: класичні 150 рівнів, пригода, головоломки без ворогів, нові вороги з іншим рухом, кооп на двох і Craft — редактор рівнів, персонажів і предметів з обміном.

## Поле і час
- Як у [lode-runner](lode-runner.md): один екран-сітка, клітинна гравітація, real-time.
- Legacy: розмір рівня змінний («varying level sizes»); воксельна 3D-подача тієї самої 2D-сітки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бігун, цегла, бетон, драбина, перекладина, пастка, золото, вартовий | — | — | без змін — див. [lode-runner](lode-runner.md) |
| Нові вороги (Legacy, Extra) | enemy | — | «нові патерни руху» (?) |
| Другий бігун (Legacy) | player | лише Two Player Mode | кооп на одному екрані |
| Створені персонажі й предмети (Legacy, Craft) | player / pickup | вокселі | користувацький вигляд (?) і поведінка (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- Усі правила поля — як у [lode-runner](lode-runner.md).
- КОЛИ `contact(runner, guard)` → ТО `lose`, `lives(-1)`, `custom: «втрачено все зібране на рівні золото»` — Championship (за Wikipedia).
- КОЛИ `custom: «рівень пройдено»` → ТО `next_level`; ЯКЩО `level(==, 50)` → ТО `win`, `custom: «сертифікат чемпіона»` — Championship.
- КОЛИ `input(save)` → ТО `custom: «запис стану в слот»`; КОЛИ `input(restore)` → ТО `lives(-1)`, `custom: «стан із слота»` — Championship.
- КОЛИ `input(password)` → ЯКЩО `custom: «пароль правильний»` → ТО `unlock(level)` — Championship на Famicom; старт з будь-якого з рівнів 1–10.
- КОЛИ `level_start` → ЯКЩО `mode(puzzle)` → ТО `custom: «ворогів нема — чиста задача копання й маршруту»` — Legacy.
- КОЛИ `level_end` → ТО `custom: «результат іде в онлайн-рейтинг»` — Legacy.

## Керування і ввід
- Championship: як Lode Runner — IJKL рух, U/O копання, Ctrl-команди (Ctrl-S — збереження) за мануалом.
- Legacy: клавіатура або геймпад; Two Player Mode вимагає контролер.

## Вікна, меню, HUD
- Championship: `game-screen` як в оригіналі; `level-password` і вибір рівня 1–10 (Famicom); `end-screen` з сертифікатом (Apple II, Famicom).
- Legacy: `main-menu` → `mode-select`: Adventure · Two Player · Extra · Puzzle · Classic · World Levels · Craft; `editor-window` (Craft) для рівнів, персонажів і предметів; `leaderboard` (онлайн); `achievements-window`.
- Переходи (Legacy): Craft → публікація → World Levels → гра чужого рівня.

## Фічі поза полем
- Championship: `levels-sequential` без пропуску, `save-slots` з ціною (−1 життя за відновлення), сертифікат за фініш (реєстрація у видавця (?)), без `level-editor`.
- Legacy: `mode-classic` (150 рівнів у 3D), `mode-puzzle`, `mode-coop` (локально на двох), `level-editor` + редактор персонажів і предметів, `level-sharing` / `user-levels-browser` (World Levels, Steam Workshop), `leaderboard-online`, `achievements`.

## Варіації й родичі
- Предок: [lode-runner](lode-runner.md); паралельна гілка: [lode-runner-the-legend-returns](lode-runner-the-legend-returns.md) (пристрої, ченці, нічні рівні).
- Між ними: Lode Runner 2009 (Xbox Live Arcade, Tozai/Southend) — 3D, шість нових типів блоків, кооп і змагання, онлайн-рейтинги (за Wikipedia: Lode Runner).
- Осі: **де складність** (у рівнях / у нових сутностях); **ціна збереження** (безкоштовно / −1 життя / нема); **чистий пазл** (з ворогами / без ворогів — ті самі правила копання як головоломка).

## Цікавинки для курсу
- Сейв, відновлення якого коштує життя — 🌱 (одне правило поверх `save-game`).
- Режим «без ворогів»: Lode Runner як детермінований пазл, де можна шукати розвʼязок BFS по станам (поле + ями з таймерами) — 🥇.
- Паролі рівнів поверх послідовної прогресії — 🌱.
- Редактор персонажів і предметів (вокселі) поряд з редактором рівнів — 🥈.
- Обмін рівнями й каталог чужих рівнів (World Levels) — 🥈.

## Мапа на каталог
- Є: `sequential-levels` · `level-unlock` · `level-password` · `save-game` · `save-single-slot` (?) · `level-select` (1–10) · `mode-select` · `in-game-editor` · `editor-palette` · `level-exchange` · `leaderboard` · `avatar-picker` (персонажі Craft (?)).
- **Нема** → пропозиції карток:
  - `+save-costs-life` «Відновлення сейву коштує життя» · game-logic/progress · 🌱.
  - `+completion-certificate` «Нагорода поза грою за проходження» · interface/menus · 🌱.
  - `+puzzle-mode-no-enemies` «Той самий рушій без ворогів як пазл-режим» · game-logic/modes · 📎.
  - `+voxel-asset-editor` «Редактор вигляду персонажів і предметів» · interface/editor · 🥈.
  - `+local-coop-versus`, `+dig-hole`, `+hole-refill` — як у lode-runner / lode-runner-the-legend-returns.

## Пропозиції до словників
- `+feature:save-costs-life` — збереження з ціною при відновленні.
- `+feature:completion-certificate` — сертифікат/нагорода від видавця за фініш.
- `+feature:asset-editor` — редактор персонажів і предметів (не лише рівнів).
- `+card:save-costs-life`, `+card:puzzle-mode-no-enemies`, `+card:voxel-asset-editor` — див. вище.

## Джерела
- ⭐ [Wikipedia: Championship Lode Runner](https://en.wikipedia.org/wiki/Championship_Lode_Runner) — 50 рівнів по черзі, набагато важчі, без редактора, сейв з ціною життя, дотик вартового — життя і все золото, Famicom: старт з 1–10 і паролі, сертифікат, платформи.
- [Steam: Lode Runner Legacy](https://store.steampowered.com/app/628660/Lode_Runner_Legacy/) — режими, Craft, World Levels, Workshop, кооп з контролером, онлайн-рейтинги, змінний розмір рівнів, Tozai / O-TWO / ESQUADRA, 13.07.2017.
- [Мануал Championship Lode Runner](https://mocagh.org/broderbund/masksun-loderunner-loderunner-manual.pdf) — клавіші й Ctrl-команди (посилання з lode-runner.md; тут не перевідкривав).
- [Wikipedia: Lode Runner](https://en.wikipedia.org/wiki/Lode_Runner) — Lode Runner 2009 і три версії Legacy (класична, нова, кооп).
- YouTube: пошуки «Championship Lode Runner gameplay», «Lode Runner Legacy gameplay».

## Непевне
- (?) Черга називала Championship «рівнями-задачами на точну послідовність ходів» — Wikipedia підтверджує лише «набагато важчі»; характер задач не перевірено.
- (?) «Втрата життя і всього золота» в Championship — дослівно з Wikipedia; чи золото повертається на поле — не ясно.
- (?) Реєстрація сертифіката у Broderbund і чи вона ще діє — не перевірено.
- (?) Legacy: які саме нові вороги й «technical bonuses», кількість рівнів Adventure / Puzzle / Extra — Steam не каже.
- (?) Legacy на Switch / PS4 / macOS / Linux — так у Wikipedia (Lode Runner), Steam показує лише Windows.
- Лінк черги `store.steampowered.com/app/560040` веде на іншу гру — правильний `app/628660`; `en.wikipedia.org/wiki/Lode_Runner_Legacy` — редирект на статтю Lode Runner.
