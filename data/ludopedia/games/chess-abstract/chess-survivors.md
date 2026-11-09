---
title: Chess Survivors
slug: chess-survivors
aka: []
family: chess-abstract
also: [roguelike]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: survive
year: 2022
platforms: [PC, macOS, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2065000", best: true, note: "grid-based quick-turn roguelike; орда шахових ворогів, здібності + апгрейди + реліквії; EA 10.11.2022, реліз 31.08.2023"}
  - {kind: other, url: "https://www.keengamer.com/articles/reviews/pc-reviews/chess-survivors-review-a-smashing-challenge/", note: "огляд: персонажі замість фігур, вороги ходять як шахові, еліти, вижити N ходів, 3 світи, gambit mode"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=3224122851", note: "гайд Gambit 20: назви здібностей, апгрейди level-up, нагороди скринь"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Chess+Survivors+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [piece-move-patterns, chase-player, enemy-waves, progress-acceleration, hp-damage, status-effects, in-round-upgrades, run-relics, unit-xp-skills, permadeath, sequential-levels, difficulty-levels, character-select, keyboard-controls, cell-click, game-screen, main-menu, end-screen, achievements-window, +auto-attack-abilities, +xp-level-up-choice, +survive-turns, +elite-enemies, +enemy-buff-items]
proposes: ["+ui:xp-bar", "+ui:ability-cooldowns", "+trigger:level_up", "+card:auto-attack-abilities", "+card:xp-level-up-choice", "+card:survive-turns"]
author: opus
date: 2026-11-09
---

# Chess Survivors — Vampire Survivors на шахівниці: герой ходить клітинами, автозброя б'є, а орда шахових фігур насувається хвилями

## Суть
Покроковий «survivors»-роглайт Aarimous: гравець керує **героєм** (не шаховою фігурою) на сітці, а вороги — пішаки, коні, королі тощо — ходять за шаховими патернами й тиснуть числом. Здібності героя здебільшого спрацьовують самі або від руху, тож мета ходу — позиціювання: де стати, щоб автоатаки накрили більше, а шахові вороги не дістали. Набираєш досвід → на кожному рівні обираєш апгрейд; виживи задану кількість ходів у кожному з трьох світів.

## Поле і час
- Квадратна сітка (шахова розмітка), вид згори, піксель-арт; поле більше за екран (?).
- «Quick-turn»: хід героя → вороги роблять свої шахові ходи; темп близький до безперервного, але час іде ходами (KeenGamer: «вижити певну кількість ходів»).
- Ворогів більшає з кожним ходом рівня; ближче до кінця забігу темп різко зростає.
- Три рівні-світи з власним лімітом ходів, зростаючою складністю й ворогами; планування рівнів однакове.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP, досвід, рівень, патерн ходу, стартовий набір | ходить на клітину за своїм патерном; несе здібності-автозброю |
| «Real knight» | player | melee splash, лікування від удару | персонаж, що ходить конем (?) — рекомендований гайдом |
| Вороги-фігури | enemy | HP, шкода | ходять як шахові: пішак, кінь, слон, тура, ферзь (?), король |
| Пішак-ворог | enemy | HP і шкода ростуть з рівнем Gambit | масовий; з Gambit 6 різко сильніший |
| Король-ворог | enemy | — | повільний (?), «Gift for Someone» сповільнює саме пішаків і королів |
| Еліта | enemy | більший розмір, більше HP і шкоди | посилена фігура |
| Здібність | — | шкода, cooldown, кількість, площа, тривалість, pierce | спрацьовує автоматично або від руху |
| Bouncy Ball | projectile | count | самонавідний відскок |
| Bubble | projectile | cooldown | багато снарядів, висока частота |
| Bulleye | projectile | — | висока частота; добре з ходом коня |
| Marble | projectile | cooldown | «не марнує шкоду» |
| Yo-Yo | projectile | count, area, duration | повертається (?) |
| Shield | — | — | блокує шкоду |
| Snowman Minion | ally | freeze duration | заморожує ворогів, мала шкода |
| Скриня | container | — | нагорода: +шкода, cooldown, range, pierce, AoE, HP, heal, броня, реліквії |
| Реліквії | pickup | — | Ever Sharp Dagger (+1 хід), Staff of Chaos (пастки шкодять ворогам), Wandering Bot, The Game Developer |
| Пастки | hazard | — | шкодять; зі Staff of Chaos — і ворогам |
| Досвід | pickup | — | з убитих ворогів (?) → рівень |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, hero, to)` → ЯКЩО `free(to)` і `custom: «to в патерні ходу персонажа»` → ТО `move(hero, to)`, `end_turn`.
- КОЛИ `turn_end(hero)` → ТО `custom: «кожна здібність з готовим cooldown атакує сама»`; `damage(n)` ворогам у зоні.
- КОЛИ `input(move, hero, to)` → ЯКЩО `custom: «здібність спрацьовує від руху»` → ТО `damage(n)` (melee splash, Bulleye тощо).
- КОЛИ `turn_end(hero)` → ТО `custom: «кожен ворог робить шаховий хід до героя»` (`move(enemy, to)`).
- КОЛИ `contact(enemy, hero)` → ТО `damage(n)` героєві; `custom: «real knight: удар лікує»` — `heal(hero, n)`.
- КОЛИ `hp_zero(enemy)` → ТО `disappear_a`, `spawn(xp)` (?).
- КОЛИ `counter(xp, >=, threshold)` → ТО `choose(upgrades)` (`+trigger:level_up`): нова здібність / апгрейд здібності / +melee / +ability damage / +HP.
- КОЛИ `contact(hero, chest)` → ТО `choose(rewards)` або `give(hero, relic)` (?).
- КОЛИ `picked(hero, ever_sharp_dagger)` → ТО `extra_move` (додатковий хід).
- КОЛИ `contact(snowman, enemy)` → ТО `freeze(enemy, n)`.
- КОЛИ `schedule(turns)` → ТО `spawn_at(enemy, edge)`; `custom: «щільність хвиль росте до кінця рівня»`.
- Деякі предмети посилюють ворогів — опційна складність посеред забігу; деякі апгрейди шкодять герою.
- КОЛИ `custom: «лічильник ходів рівня досяг ліміту»` → ТО `next_level`; після третього — `win`.
- КОЛИ `hp_zero(hero)` → ТО `lose` (забіг закінчено).
- Перемога: пережити ліміт ходів усіх трьох рівнів · Поразка: HP героя = 0 · Рахунок: — (Gambit-рівень складності як рекорд).

## Керування і ввід
- Миша (рекомендовано для точності), клавіатура або геймпад: вибір клітини для ходу героя.
- Цілитися не треба — атаки автоматичні або прив'язані до руху.
- Level-up: клік по одній з карток апгрейдів.

## Вікна, меню, HUD
- `main-menu`: Грати → `character-select`; Gambit → `difficulty-select`; досягнення; налаштування.
- `character-select`: персонажі з різним ходом, сильними/слабкими сторонами, стартовим набором і силами; частина — заблокована.
- `game-screen`: сітка, герой, орда; зліва вгорі — HP, досвід (`+ui:xp-bar`), набір здібностей (`+ui:ability-cooldowns`).
- `upgrade-window`: вибір апгрейда на level-up; окремо — нагороди скрині.
- `end-screen`: смерть («герой розсипається») або перемога забігу; розблоковане.
- Переходи: main-menu → character-select → game-screen ⇄ upgrade-window → (ліміт ходів) наступний світ → end-screen.

## Фічі поза полем
- `meta-progression`: розблокування персонажів, косметики й реліквій.
- `difficulty-presets`: **Gambit**-рівні (досягнення Gambit 20) — зростаючі модифікатори складності.
- `achievements`, `cloud-save`, `localization` (8 мов).
- «Gambit mode» — головна варіація петлі (KeenGamer, без деталей).

## Варіації й родичі
- Родичі в корпусі: `shotgun-king.md` (король проти білої армії, постріл замість автоатак, таймери ходів ворогів), `roguelike/pawnbarian.md` (герой ходить картами-фігурами, позначки шкоди на клітинах), `really-bad-chess.md` (випадкові армії).
- **Відмінність від Shotgun King**: там ворог — армія з королем-ціллю й матом як поразкою; тут — нескінченна орда, мета — протриматись N ходів, атаки самі, герой не шахова фігура.
- **Відмінність від Pawnbarian**: там патерн ходу дає карта в руці, а шкода — від червоних позначок; тут патерн — властивість персонажа, а шкода — від контакту й орди.
- Жанрові предки поза сімʼєю: Vampire Survivors (автоатаки + level-up вибір, realtime).
- Осі варіацій: **час** (realtime survivors / покроковий quick-turn) · **патерн героя** (король / кінь / свій) · **атака** (авто / від руху / ручна) · **мета рівня** (вижити N ходів / вбити боса).

## Цікавинки для курсу
- Орда шахових фігур, кожна жадібно йде до героя своїм патерном (BFS по ходах коня, промені тури) — 🥉.
- Автозброя з cooldown-ами, що атакує в кінці ходу: черга подій на тік — 📎.
- Level-up вибір з 3 карток, вага рідкості й «не пропонувати те, що вже на максимумі» — 🥉.
- Хвилі з густиною, що росте від номера ходу (`spawn-schedule` + `progress-acceleration`) — 📎.
- Самонавідний снаряд з відскоками на сітці (Bouncy Ball) — 🥉.
- Gambit-рівні як стос модифікаторів складності (HP/шкода ворогів ×k) — 🌱.

## Мапа на каталог
- Є в каталозі: `piece-move-patterns` ↔ вороги-фігури й хід героя · `chase-player` ↔ орда · `enemy-waves`, `progress-acceleration` · `hp-damage`, `status-effects` ↔ заморозка · `in-round-upgrades` ↔ level-up · `run-relics` ↔ реліквії скринь · `unit-xp-skills` ↔ досвід · `permadeath` · `sequential-levels` ↔ три світи · `difficulty-levels` ↔ Gambit · `character-select` · `keyboard-controls`, `cell-click` · `game-screen`, `main-menu`, `end-screen`, `achievements-window`.
- **Нема** → пропозиції карток:
  - `+auto-attack-abilities` «Автозброя з cooldown» · entities/combat · 🥉 · слоти {trigger: turn|move, cooldown, count, area}.
  - `+xp-level-up-choice` «Level-up: вибір 1 з N апгрейдів» · game-logic/economy · 🥉 · слоти {n, rarity}.
  - `+survive-turns` «Вижити N ходів» · game-logic/win · 🌱 · слоти {turns}.
  - `+elite-enemies` «Елітний варіант ворога» · entities/enemies · 📎 — більший, більше HP/шкоди.
  - `+enemy-buff-items` «Предмет, що посилює ворогів за нагороду» · game-logic/economy · 📎.

## Пропозиції до словників
- `+trigger:level_up` — досвід досяг порогу рівня (зручніше, ніж `counter(xp, >=, n)` з порогом, що росте).
- `+ui:xp-bar` — смуга досвіду до наступного рівня; `+ui:ability-cooldowns` — іконки здібностей з таймерами.
- `+card:auto-attack-abilities`, `+card:xp-level-up-choice`, `+card:survive-turns` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Chess Survivors](https://store.steampowered.com/app/2065000) — «grid based, quick-turn, roguelike», орда шахових ворогів, комбінації здібностей/апгрейдів/реліквій, «Die, Learn, Repeat»; дати EA і релізу, платформи, 8 мов.
- [KeenGamer: огляд](https://www.keengamer.com/articles/reviews/pc-reviews/chess-survivors-review-a-smashing-challenge/) — персонажі зі своїм рухом і силами, вороги ходять як шахові, еліти, предмети-посилення ворогів, вижити N ходів, 3 світи, HUD зліва вгорі, gambit mode.
- [Steam-гайд «How to Reach Gambit 20»](https://steamcommunity.com/sharedfiles/filedetails/?id=3224122851) — real knight, здібності (Bouncy Ball, Bubble, Bulleye, Marble, Shield, Snowman Minion, Yo-Yo), пріоритети level-up, нагороди скринь (Ever Sharp Dagger +1 хід, Staff of Chaos). Сторінка позначена Steam як видалена.

## Непевне
- (?) Як саме чергуються ходи: усі вороги після кожного ходу героя чи за власним темпом; теги Steam суперечать (Turn-Based vs Real Time Tactics).
- (?) Набір персонажів і їхні патерни ходу (чи «real knight» ходить конем — лише натяк гайда).
- (?) Ліміти ходів рівнів, кількість Gambit-рівнів (≥20), що саме змінює кожен.
- (?) Чи є боси наприкінці світу; звідки досвід (кристали з убитих?).
- (?) Розмір поля і чи камера йде за героєм.
