---
title: Dota Underlords
slug: dota-underlords
aka: [Underlords]
family: tower-lanes
also: [tactics]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: online
  info: partial
  random: runtime
  goal: survive
year: 2019
platforms: [PC (Windows, macOS, Linux), iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dota_Underlords", best: true, note: "8×8, 8 гравців, фази раунду, золото/XP, 3 копії → сильніша, альянси, предмети, Лорд після 10-го раунду, HP 100, режими"}
  - {kind: steam, url: "https://store.steampowered.com/app/1046930/Dota_Underlords/", note: "режими Standard/Knockout/Duos, офлайн з AI на 4 рівнях, City Crawl, 4 Underlords, crossplay, battle pass"}
  - {kind: official, url: "https://underlords.com/", note: "офіційний сайт (сторінка без тексту)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Auto_battler", note: "жанр; Underlords — standalone-версія від Valve"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dota+underlords+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [round-currency, shop-catalog, shop-buyback, tile-merge, inventory-items, inventory-limit, drag-drop-piece, hp-damage, chase-greedy, melee-vs-ranged, ai-opponent, ai-greedy, difficulty-levels, online-multiplayer, rating-system, mode-select, move-timer, replay-window, lobby-window, level-bank, +auto-battle, +bench-and-board, +star-up-merge, +trait-synergy, +shared-unit-pool, +interest-economy, +commander-unit, +shared-hp-duo, +survivor-count-damage, +puzzle-board-challenges, +cross-device-session, +seasonal-rotation]
proposes: ["+trigger:round_lost", "+effect:reroll", "+effect:interest", "+effect:sell", "+role:unit", "+role:bench", "+role:commander", "+ui:synergy-panel", "+ui:shop-bar", "+ui:player-list", "+window:campaign-map", "+feature:spectator-lobby", "+feature:cross-device-continue"]
author: opus
date: 2026-11-09
---

# Dota Underlords — Valve-версія Auto Chess: та сама 8×8 дошка, плюс Лорд-командир на полі, кампанія-пазли й кооп удвох

## Суть
Standalone-автобатлер Valve (ранній доступ — червень 2019, реліз — лютий 2020), що виріс з моду [dota-auto-chess](dota-auto-chess.md). Ядро те саме: купуєш героїв, тримаєш у запасі або ставиш на квадратну дошку 8×8, три однакові зливаються в сильнішого, альянси дають бонуси, бій іде сам. Цей файл описує **відмінності**: після 10-го раунду обираєш одного з 4 **Лордів** — юніт-командира, що бʼється разом із загоном; урон за програш дорівнює кількості живих героїв переможця; є кампанія City Crawl з пазл-челенджами, режими Knockout і Duos (спільні HP і XP) та офлайн-гра з AI.

## Поле і час
- Квадратна дошка 8×8; свої — нижня половина (?), бій на спільній дошці з загоном суперника.
- Раунд: **підготовка** (купівля, перестановка, нові герої; таймер) → **бій** (автоматично, без вводу).
- Запас (inventory) — герої, куплені, але не поставлені; кількість героїв на дошці обмежена рівнем.
- 8 гравців онлайн у дуелях 1×1 за раунд; останній живий перемагає.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | 100 HP, золото, XP/рівень | програв бій → −HP |
| Герой | ally (`+role:unit`) | ціна, рівень злиття, альянси (1+), HP, атака, дальність, здібність | у бою сам іде до цілі, бʼє, кастує |
| Запас | zone (`+role:bench`) | слоти | куплені, не поставлені герої |
| Клітина дошки | zone | — | одна фігура |
| Лорд (Underlord) | ally (`+role:commander`) | 1 з 4, власні перки й здібності | зʼявляється після 10-го раунду, бʼється разом із загоном |
| Магазин | spawner | слоти, оновлення | пропонує героїв (?) зі спільного пулу |
| Альянс | zone | пороги | ≥2 героїв одного альянсу → бонус усім членам |
| Предмет | pickup | ефект | видається після певних раундів; вішається на героя |
| Нейтральні крипи | enemy | — | PvE-раунди (?) |
| Напарник у Duos | ally | — | спільні з тобою HP і XP |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(prep)` → ТО `currency(+income)`; `custom: «відсотки за накопичене і стріки, як у DAC»` (?).
- КОЛИ `input(buy, hero)` → ЯКЩО `has(gold, cost)` and `custom: «є місце в запасі»` → ТО `currency(-cost)`, `place(hero, bench)`.
- КОЛИ `input(buy_xp)` → ЯКЩО `has(gold, cost)` → ТО `counter(xp, +n)`; КОЛИ `counter(xp, >=, need)` → ТО `custom: «рівень +1: +1 герой на дошці»`.
- КОЛИ `custom: «3 однакові герої одного рівня»` → ТО `merge(3 → 1)` — сильніша версія з новими здібностями.
- КОЛИ `input(drag, hero, cell)` → ЯКЩО `free(cell)` and `count(heroes_on_board, <, level)` → ТО `move(hero, cell)`; `occupied` → `swap`.
- КОЛИ `input(sell, hero)` → ТО `currency(+value)`, `disappear(hero)`.
- КОЛИ `custom: «на дошці ≥2 героїв одного альянсу»` → ТО `set_state(alliance_members, bonus)`.
- КОЛИ `counter(round, ==, 10)` → ТО `choose(1 з 4 Лордів)`, `spawn(underlord, board)`.
- КОЛИ `custom: «раунд нагородження предметом»` → ТО `choose(item)` (?), `give(player, item)`; КОЛИ `input(drag, item, hero)` → ТО `custom: «підсилення або спецефект»`.
- КОЛИ `phase_start(battle)` → ТО герої й Лорд `custom: «автобій: рух до цілі, атака, здібності»`.
- КОЛИ `all_gone(units, side)` → ТО раунд завершено; КОЛИ `custom: «trigger round_lost»` → ТО `hp(player, −кількість живих героїв переможця)`.
- КОЛИ `mode(duos)` → ТО `custom: «HP і XP спільні для пари»`.
- КОЛИ `mode(knockout)` → ТО `custom: «прискорений розвиток, коротший матч»`.
- КОЛИ `hp_zero(player)` → ТО `custom: «вибуває, місце 8…2»`; останній живий — `win`.
- Перемога: останній з 8 (у Duos — остання пара) · Поразка: HP = 0 · Рахунок: місце, рейтинг (ranked).

## Керування і ввід
- Миша/тач: клік по слоту магазину — купити; drag героя запас ↔ дошка; drag предмета на героя; кнопки оновлення магазину й купівлі XP (?).
- Однаковий інтерфейс для ПК і мобільного; матч можна почати на одному пристрої й закінчити на іншому.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Standard / Knockout / Duos / офлайн проти AI / City Crawl.
- `difficulty-select`: 4 рівні AI в офлайні.
- `lobby-window`: ranked, приватні лобі з глядачами.
- `game-screen`: дошка 8×8, запас, `+ui:shop-bar`, `coins`, рівень/XP, `+ui:synergy-panel` (альянси з порогами), `+ui:player-list` (HP суперників), `timer-countdown` фази.
- `character-select` — вибір Лорда після 10-го раунду.
- `+window:campaign-map` — City Crawl: місто White Spire по районах, пазл-челенджі й «вуличні бійки» (`level-bank`).
- `replay-window` — перегляд матчів · `end-screen` з місцем · battle pass (`shop-window`).

## Фічі поза полем
- `mode-coop` (Duos) · `ai-opponent-levels` (офлайн, 4 рівні) · `rank-tiers` (ranked matchmaking) · `+feature:spectator-lobby` (приватні лобі з глядачами).
- `+feature:cross-device-continue` — профіль спільний на всіх пристроях, crossplay ПК ↔ мобільні.
- `daily-puzzle` / щоденні челенджі й нагороди; replay system.
- Сезони: ротація предметів (частину прибирають щосезону); battle pass без ігрової переваги.
- City Crawl: кампанія з пазлами на фіксованій дошці, нагороди — косметика й титули.

## Варіації й родичі
- [dota-auto-chess](dota-auto-chess.md) — першоджерело (домашні/виїзні бої, кур'єр, реліквії); [teamfight-tactics](teamfight-tactics.md) — гекси, карусель, аугменти; Hearthstone Battlegrounds — ряд без поля; [super-auto-pets](super-auto-pets.md); [mechabellum](mechabellum.md).
- **Що Underlords додав до осі жанру**: командир на полі (Лорд), урон = кількість живих героїв переможця, пазл-кампанія на тому ж двіжку, спільні HP/XP у парі, сезонна ротація предметів.

## Цікавинки для курсу
- Пазл-челендж на двіжку автобатлера: дана дошка й запас — розстав, щоб виграти бій — 🥈 (детермінований автобій + перевірка результату).
- Урон = кількість живих героїв переможця — 🌱.
- Лорд — юніт-командир, обраний один раз за матч — 📎.
- Duos: два гравці з одним HP і XP — 🥉 (спільний стан, два вводи).
- Продовження матчу на іншому пристрої — 🥇 (серверний стан сесії).

## Мапа на каталог
- Є: `round-currency` · `shop-catalog` + `shop-buyback` · `tile-merge` ↔ 3 → 1 · `inventory-items` + `inventory-limit` ↔ предмети, запас · `drag-drop-piece` · `hp-damage` · `chase-greedy` + `melee-vs-ranged` ↔ автобій · `ai-opponent` + `ai-greedy` + `difficulty-levels` ↔ офлайн AI · `online-multiplayer` · `rating-system` · `mode-select` · `move-timer` ↔ таймер підготовки · `replay-window` · `lobby-window` · `level-bank` ↔ челенджі City Crawl.
- **Нема** → пропозиції карток:
  - `+auto-battle`, `+bench-and-board`, `+star-up-merge`, `+trait-synergy`, `+shared-unit-pool`, `+interest-economy` — уже пропоновані сімʼєю (DAC, TFT).
  - `+commander-unit` «Юніт-командир, обраний раз за матч» · entities/state · 📎.
  - `+shared-hp-duo` «Спільні HP і ресурс пари» · game-logic/opponent · 🥉.
  - `+survivor-count-damage` «Урон = кількість живих юнітів переможця» · game-logic/lose · 🌱.
  - `+puzzle-board-challenges` «Пазл-челенджі на двіжку основної гри» · levels/bank · 🥈.
  - `+cross-device-session` «Продовжити партію на іншому пристрої» · code/architecture · 🥇.
  - `+seasonal-rotation` «Сезонна ротація пулу предметів» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+trigger:round_lost`, `+effect:reroll`, `+effect:interest`, `+effect:sell`, `+role:unit`, `+role:bench`, `+ui:synergy-panel`, `+ui:shop-bar`, `+ui:player-list` — підтвердження з DAC/TFT.
- `+role:commander` — юніт-лідер з перками, що бʼється разом із загоном (Лорд).
- `+window:campaign-map` — мапа кампанії з районами-челенджами (City Crawl).
- `+feature:spectator-lobby` — приватне лобі з глядачами.
- `+feature:cross-device-continue` — спільний профіль і продовження матчу на іншому пристрої.

## Джерела
- ⭐ [Wikipedia: Dota Underlords](https://en.wikipedia.org/wiki/Dota_Underlords) — 8×8, 8 гравців, фази, золото/XP, злиття трьох, альянси, предмети, Лорди після 10-го раунду, HP 100 і урон за живих, Classical/Knockout/Duos, ранній доступ і реліз.
- [Steam](https://store.steampowered.com/app/1046930/Dota_Underlords/) — режими, офлайн-AI 4 рівнів, ranked і приватні лобі з глядачами, City Crawl, 4 Underlords, сезонна ротація предметів, battle pass, crossplay і продовження на іншому пристрої.
- [Wikipedia: Auto battler](https://en.wikipedia.org/wiki/Auto_battler) — жанр і місце Underlords у ньому.

## Непевне
- (?) Чи бій іде проти копії армії суперника (кожен на своїй дошці), чи на одній дошці «вдома/на виїзді» — джерела не уточнюють.
- (?) Предмети: вибір з кількох варіантів чи випадковий дроп; у яких саме раундах.
- (?) Розмір магазину, ціни оновлення й XP, відсотки й стріки — не перевірено (у DAC є).
- (?) Чи є PvE-раунди з крипами, як у DAC.
- (?) Режим Free for All і подальша доля гри після 2020 (припинення оновлень) — не перевірено.
