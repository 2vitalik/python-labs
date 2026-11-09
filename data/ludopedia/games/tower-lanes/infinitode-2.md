---
title: Infinitode 2
slug: infinitode-2
aka: [Infinitode 2 - Infinite Tower Defense, Infinitode]
family: tower-lanes
also: [build-sim]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: survive
year: 2021
platforms: [PC, Linux, Android, iOS]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/937310", best: true, note: "майнери ресурсів на будь-якому рівні, 15+ веж до рівня 10 з XP і вміннями, модифікатори, 400+ досліджень, редактор, endless"}
  - {kind: other, url: "https://steamcommunity.com/app/937310/guides/", note: "гайди спільноти: прогресія, ресурси, bit dust, рівень 6.1"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=infinitode+2+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [enemy-waves, spawn-schedule, spawn-points, enemy-reached-base, tower-placement, tower-range, coverage-area, unit-xp-skills, round-currency, in-round-upgrades, shop-buyback, shop-catalog, projectile-shot, shoot-cooldown, explode-area, status-effects, hp-damage, speed-per-type, in-game-editor, editor-palette, editor-playtest, level-select, level-unlock, save-progress, leaderboard, game-pause, status-panel, +aura-buff, +resource-miner, +miner-cost-escalation, +research-tree, +endless-research, +ability-cast, +boss-per-stage, +trophy-bonuses, +cross-platform-save]
proposes: ["+effect:sell", "+effect:upgrade", "+effect:mine", "+effect:buff", "+role:tower", "+role:miner", "+role:modifier", "+ui:range-circle", "+ui:ability-bar", "+window:research-tree", "+feature:research-tree"]
author: opus
date: 2026-11-09
---

# Infinitode 2 — мінімалістичний TD на плитках, де між хвилями ще й копаєш ресурси на дослідження

## Суть
Абстрактна «ШІ-тренувальна» тайлова мапа: вороги йдуть дорогою до бази, гравець ставить вежі на вільні плитки. Поверх звичного TD — три шари: **майнери** на плитках-джерелах добувають ресурси (Scalar, Vector, Matrix, Tensor, Infiar) для дерева з 400+ досліджень; **модифікатори** — будівлі, що підсилюють сусідні вежі чи пришвидшують видобуток; вежі набирають **досвід** і на рівнях отримують вибір вмінь. Відмінність від Desktop TD і Fieldrunners: шлях заданий плитками, а ціна клітини визначається тим, що поруч (джерело, сусіди-вежі).

## Поле і час
- Квадратна сітка плиток: дорога, платформи під вежі/модифікатори, джерела ресурсів, точки спавну, база (ціль) (?).
- Сусідство важливе: модифікатор діє на суміжні клітини; майнер — лише на плитці-джерелі.
- Real-time з хвилями; є прискорення й пауза (?); кампанія — 6 стадій, 50+ рівнів, бос наприкінці кожної стадії; після кампанії — нескінченна гра.
- Повна інформація; генерація — лише в нескінченних рівнях (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дорога | terrain | — | вороги йдуть по ній |
| Платформа | terrain | — | сюди ставлять вежі й модифікатори |
| Джерело ресурсу | resource | тип, щільність | майнер на ньому добуває ресурс |
| Спавн | spawner | — | хвилі виходять сюди |
| База | static | HP / життя (?) | ворог дійшов → втрата |
| Вежа (15+ типів) | tower | рівень 1–10, XP | стріляє; росте досвідом; на рівнях — вибір унікального вміння |
| Майнер | custom | тип ресурсу, швидкість | добуває ресурс зі швидкістю × щільність джерела; встановлення займає час |
| Модифікатор | custom | тип | підсилює сусідні вежі (шкода, темп тощо), або пришвидшує майнери, або інші бонуси |
| Вороги | enemy | HP, швидкість, тип | ідуть до бази; різні типи (?) |
| Бос стадії | boss | — | у кінці кожної стадії |
| Вміння (abilities) | custom | заряди/вартість (?) | активні удари гравця по мапі (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, tower, cell)` → ЯКЩО `cell(cell, platform)` and `free(cell)` and `has(player, coins)` → ТО `place(player, tower)`, `currency(-cost)`; інакше `block`.
- КОЛИ `input(place, miner, cell)` → ЯКЩО `cell(cell, source)` and `has(player, coins)` → ТО `place(player, miner)`, `currency(-cost)`, `timer(install)`.
- КОЛИ `input(place, miner)` → ТО `custom: «наступний майнер того ж типу дорожчий на 60 % (множенням)»`.
- КОЛИ `tick` → ЯКЩО `state(miner, installed)` → ТО `counter(resource, +speed × density)`.
- КОЛИ `input(place, modifier, cell)` → ЯКЩО `cell(cell, platform)` and `free(cell)` → ТО `place(player, modifier)`; КОЛИ `adjacent(modifier, tower)` → ТО `custom: «effect buff: підсилення сусідньої вежі»`.
- КОЛИ `schedule(waves)` → ТО `spawn_at(enemies, spawn)`.
- КОЛИ `tick` → ворог `move(a, next_on_road)` до бази.
- КОЛИ `in_range(tower, enemy, r)` → ТО `spawn(projectile)` з періодом `shoot-cooldown`.
- КОЛИ `contact(projectile, enemy)` → ТО `damage(n)`; частина веж — `explode(area, n)` або `set_state(enemy, slow|poison, dur)` (?).
- КОЛИ `hp_zero(enemy)` → ТО `disappear(enemy)`, `currency(+bounty)`, `custom: «XP вежі, що вбила/влучала»`.
- КОЛИ `counter(tower_xp, >=, n)` → ТО `custom: «рівень вежі +1»`, на окремих рівнях `choose(options)` — унікальне вміння вежі.
- КОЛИ `input(upgrade, tower)` → ЯКЩО `has(player, coins)` → ТО `custom: «effect upgrade»` (до рівня 10).
- КОЛИ `input(cast, ability, area)` → ТО `custom: «активне вміння по області»` (?).
- КОЛИ `reach(enemy, base)` → ТО `lives(-n)` (?), `disappear(enemy)`.
- КОЛИ `counter(lives, ==, 0)` → ТО `lose`.
- КОЛИ `wave_cleared` → ЯКЩО `custom: «остання хвиля рівня»` → ТО `win`, ресурси майнерів зараховуються в загальний запас для досліджень.
- КОЛИ `input(research, node)` → ЯКЩО `has(player, resources)` → ТО `unlock(node)` — нові вежі, вміння, бонуси до характеристик.
- Перемога: пройти всі хвилі рівня · Поразка: база знищена · Рахунок: у нескінченному режимі — хвилі/очки в таблиці.

## Керування і ввід
- Миша/тач: вибір вежі, майнера чи модифікатора з меню → клік по плитці.
- Клік по вежі — панель: рівень, XP, апгрейд, вибір вміння, продаж.
- Кнопки: виклик хвилі, прискорення, пауза (?); активні вміння — панель знизу (?).
- Редактор: палітра плиток і обʼєктів, тест рівня.

## Вікна, меню, HUD
- `main-menu` → `level-select` (6 стадій, 50+ рівнів, мапа стадій) / `+window:research-tree` (400+ вузлів, нескінченна частина) / `editor-window` / `leaderboard` / `achievements-window` (36+ трофеїв, що дають бонуси) / `settings-window`.
- `game-screen`: мапа плиток, `coins`, `lives`/HP бази, `wave-counter`, лічильники ресурсів майнерів, `+ui:range-circle`, `+ui:ability-bar`.
- Панель вежі: XP, рівень, вміння.
- `end-screen` — результат рівня й зібрані ресурси.

## Фічі поза полем
- `+feature:research-tree` — 400+ досліджень за ресурси з майнерів + нескінченне дерево (`meta-progression`).
- `level-editor` — власні рівні; майнити ресурси можна й на кастомних рівнях.
- `mode-endless` — гра після кампанії з таблицею лідерів і призами.
- `achievements` — трофеї з бонусами до гри.
- `cloud-save` — синхронізація сейвів між PC, Android і iOS.
- Free-to-play з внутрішніми покупками.

## Варіації й родичі
- Попередник — Infinitode (мобільний, ?). Родичі: `gemcraft` (мана й самоцвіти — інша економіка на полі), `creeper-world` (ресурс і поле), `dungeon-warfare`; з `build-sim` — видобуток на клітинах-джерелах (Factorio, Mindustry).
- **Осі варіацій**: на що йде клітина — вежа / економіка / підсилювач · економіка — лише нагорода за вбивства / видобуток на полі · прогрес вежі — апгрейд за гроші / досвід у бою / обидва · мета-прогрес — нема / дерево досліджень.

## Цікавинки для курсу
- Модифікатор, що підсилює всі суміжні вежі — 📎 (сусідство на сітці + модифікатори).
- Майнер на плитці-джерелі: швидкість × щільність, ціна наступного ×1.6 — 📎.
- Вежа з XP і вибором вміння на рівні — 🥉.
- Редактор плиткових мап з плейтестом — 🥈.
- Дерево досліджень з передумовами як граф — 🥉.

## Мапа на каталог
- Є: `enemy-waves` + `spawn-schedule` + `spawn-points` · `enemy-reached-base` · `tower-placement` + `tower-range` · `coverage-area` ↔ модифікатори · `unit-xp-skills` ↔ XP і вміння веж · `round-currency` · `in-round-upgrades` · `shop-buyback` · `shop-catalog` · `projectile-shot` + `shoot-cooldown` · `explode-area` · `status-effects` · `hp-damage` · `speed-per-type` · `in-game-editor` + `editor-palette` + `editor-playtest` · `level-select` + `level-unlock` · `save-progress` · `leaderboard` · `game-pause` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+resource-miner` «Видобувач на клітині-джерелі» · game-logic/economy · 📎 · слоти {speed, density}.
  - `+miner-cost-escalation` «Кожен наступний дорожчий» · game-logic/economy · 🌱 · слот {factor}.
  - `+research-tree` «Дерево досліджень» · game-logic/progression · 🥉.
  - `+endless-research` «Нескінченні дослідження» · game-logic/progression · 📎.
  - `+ability-cast` «Активне вміння гравця по області» · entities/combat · 📎.
  - `+boss-per-stage` «Бос наприкінці стадії» · game-logic/waves · 🌱.
  - `+trophy-bonuses` «Досягнення дають бонуси в грі» · game-logic/progression · 🌱.
  - `+cross-platform-save` «Сейв між платформами» · game-logic/save · 🥈.
  - `+aura-buff` — див. desktop-tower-defense.

## Пропозиції до словників
- `+effect:sell`, `+effect:upgrade`, `+effect:buff`, `+role:tower`, `+ui:range-circle` — підтвердження з родини.
- `+effect:mine` — сутність щотіку додає ресурс з клітини.
- `+role:miner` — будівля-видобувач на клітині-ресурсі.
- `+role:modifier` — будівля без атаки, що змінює сусідів.
- `+ui:ability-bar` — панель активних умінь із зарядами.
- `+window:research-tree` — дерево досліджень (`editor-window` уже ⏳).
- `+feature:research-tree` — дерево досліджень як фіча (поруч із ⏳ `meta-progression`, `mode-endless`, `cloud-save`, які вже є).

## Джерела
- ⭐ [Steam: Infinitode 2](https://store.steampowered.com/app/937310) — майнінг на всіх рівнях (і кастомних), 15+ веж, XP і вибір умінь, рівень 10, модифікатори (сусіди, швидкість видобутку), 400+ досліджень, нескінченне дерево, 6 стадій, 50+ рівнів, боси, редактор, 36+ трофеїв, хмарні сейви з Android/iOS, реліз 30.04.2021, Prineside.
- [Steam Community: гайди](https://steamcommunity.com/app/937310/guides/) — список гайдів (прогресія, bit dust, рівень 6.1 з механікою руйнування самоцвітів).
- Пошуковий сніпет fandom-вікі (сторінка Miners; сама вікі віддає 402): майнери Scalar/Vector/Matrix/Tensor/Infiar на плитках-джерелах, швидкість × щільність, +60 % за кожен наступний, +25 % до апгрейду, встановлення 1:00.
- YouTube: пошук «infinitode 2 gameplay».

## Непевне
- (?) Повний перелік типів плиток (дорога, платформа, джерело, спавн, база; чи є портали/брами).
- (?) Чи можна будувати на дорозі / чи вороги шукають шлях по кількох дорогах (вибір найкоротшого).
- (?) Назви веж (Basic, Sniper, Cannon, Freezing, Venom, Splash, Blast, Multishot, Minigun, Air, Tesla, Missile, Flamethrower, Laser, Gauss, Crusher — з памʼяті) і модифікаторів.
- (?) Типи ворогів, вміння гравця (Fireball, Blizzard тощо — з памʼяті), життя бази й прискорення.
- (?) Рік: Steam — 2021, мобільна версія, імовірно, раніше.
- (?) Чи «ресурси майнерів» лише для досліджень, чи також у рівні (сніпет каже: «required for Research»).
