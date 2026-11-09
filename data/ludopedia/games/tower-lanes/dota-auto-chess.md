---
title: Dota Auto Chess
slug: dota-auto-chess
aka: [Auto Chess, DAC]
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
platforms: [PC (Dota 2 custom game), Android, iOS, PS4]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dota_Auto_Chess", best: true, note: "8 гравців, кур'єр, фази раунду, відсотки, лава 8, 3 копії → зірка, раси/класи, спільний пул, крипи й предмети"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Auto_battler", note: "жанр, що виріс з моду: Underlords, TFT, Battlegrounds"}
  - {kind: other, url: "https://blog.gamesight.io/auto-battlers-have-arrived-teamfight-tactics-vs-dota-underlords-vs-auto-chess/", note: "порівняння трьох автобатлерів (з черги; не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dota+auto+chess+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [round-currency, shop-catalog, shop-buyback, tile-merge, inventory-items, inventory-limit, drag-drop-piece, hp-damage, chase-greedy, melee-vs-ranged, ai-opponent, enemy-waves, move-timer, online-multiplayer, run-relics, leaderboard, +auto-battle, +bench-and-board, +interest-economy, +streak-bonus, +shop-reroll, +star-up-merge, +trait-synergy, +item-combine, +shared-unit-pool, +home-away-board, +streak-breaker-bonus]
proposes: ["+role:unit", "+role:bench", "+trigger:round_lost", "+cond:count_unique", "+effect:reroll", "+effect:interest", "+effect:sell", "+ui:synergy-panel", "+ui:shop-bar", "+ui:player-list", "+window:lobby-window", "+axis:time"]
author: opus
date: 2026-11-09
---

# Dota Auto Chess — першоджерело автобатлерів: купуй фігури, збирай трійки, став на шахівницю — бій іде сам

## Суть
Мод для Dota 2 (Drodo Studio, січень 2019), з якого виріс жанр auto battler. Вісім гравців паралельно купують «шахові фігури» — героїв Dota — у магазині, тримають на лаві або ставлять на свої ряди шахівниці; бій між загонами йде **без участі гравця**. Три однакові фігури зливаються в 2★, три 2★ — у 3★; раси й класи дають синергії за кількістю. Програш раунду знімає HP кур'єра, виживає останній. Від [teamfight-tactics](teamfight-tactics.md) відрізняється квадратною дошкою, домашніми/виїзними боями, бонусом за перерваний стрік і реліквіями з крипів.

## Поле і час
- Квадратна шахівниця; свої — перші 4 ряди, у бою — дві половини разом. Бій вдома (на своїй дошці) або на виїзді (на дошці суперника).
- Лава — до 8 слотів поза дошкою.
- Раунд = **дохід** → **підготовка** (купівля, розстановка, предмети; таймер) → **бій** (real-time, без вводу). Кілька десятків раундів.
- Частина раундів — проти нейтральних крипів (PvE); інформація: видно дошки інших, випадковість — магазин, лут, пари суперників.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кур'єр | player | HP, золото (показане як мана), рівень досвіду | аватар гравця; програш раунду → −HP; збирає лут |
| Фігура (герой) | ally (`+role:unit`) | ціна, зірки 1–3, раса (≥1), клас, HP, атака, дальність, здібність | у бою сама йде до цілі, бʼє, кастує |
| Лава | zone (`+role:bench`) | 8 слотів | запас фігур поза боєм |
| Клітина дошки | zone | — | одна фігура; кількість фігур на дошці ≤ рівень |
| Магазин | spawner | слоти, реролл | пропонує фігури зі **спільного пулу** за шансами рівня |
| Золото | resource | — | дохід + відсотки + стріки + перемога |
| Досвід / рівень | resource | — | ліміт фігур на дошці, шанси дорогих фігур |
| Раса / клас | zone | пороги | N фігур раси/класу на дошці → ярусний баф (свої), дебаф (ворог) або спец-ефект |
| Нейтральний крип | enemy | — | у PvE-раундах; дропає предмети |
| Предмет | pickup | стати | вішається на фігуру; деякі збираються в сильніші |
| Реліквія | pickup | нейтральний предмет | за вдалий бій у кожному 10-му раунді; змінює правила на користь |
| Candies / кур'єри | neutral | косметика | валюта топ-рангу; кур'єри комбінуються |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(income)` → ТО `currency(+base)`, `custom: «+1 за кожні 10 золота в банку, з капом»`, `custom: «стрік ≥5 перемог/поразок → бонус»`.
- КОЛИ `custom: «гравець перервав чужий стрік»` → ТО `currency(+bonus)`; КОЛИ `custom: «допоміг вибити гравця»` → ТО `give(player, gold|item)`.
- КОЛИ `custom: «перемога в раунді»` → ТО `currency(+1)` до розрахунку відсотків.
- КОЛИ `input(buy, slot)` → ЯКЩО `has(gold, cost)` and `count(bench, <, 8)` → ТО `currency(-cost)`, `spawn(unit, bench)`.
- КОЛИ `custom: «3 однакові фігури з однаковими зірками на лаві+дошці»` → ТО `merge(3 → 1, stars+1)`; 3 × 2★ → 3★.
- КОЛИ `input(reroll)` → ЯКЩО `has(gold, cost)` → ТО `custom: «effect reroll: нові фігури з пулу»`.
- КОЛИ `input(buy_xp)` → ЯКЩО `has(gold, cost)` → ТО `counter(xp, +n)`; КОЛИ `counter(xp, >=, need)` → ТО `custom: «рівень +1: +1 фігура на дошці, кращі шанси»`.
- КОЛИ `input(sell, unit)` → ТО `currency(+value)`, `custom: «фігура повертається в спільний пул»` (?).
- КОЛИ `input(drag, unit, cell)` → ЯКЩО `custom: «клітина в перших 4 рядах»` and `count(units_on_board, <, level)` → ТО `move(unit, cell)`; `occupied` → `swap`.
- КОЛИ `custom: «змінився склад дошки»` → ЯКЩО `custom: «різних фігур раси/класу ≥ поріг яруса»` → ТО `set_state(units, synergy_bonus)` або `set_state(enemies, debuff)`.
- КОЛИ `phase_start(battle)` → ТО `custom: «home/away: бій на дошці одного з двох»`; фігури `chase-greedy` → `in_range(a, target, range)` → `damage`; повна мана → здібність.
- КОЛИ `all_gone(units, side)` → ТО раунд завершено; КОЛИ `custom: «trigger round_lost»` → ТО `hp(courier, -f(живі фігури переможця))`.
- КОЛИ `died(creep)` → ТО `spawn(item)`; КОЛИ `custom: «кожен 10-й раунд виграно»` → ТО `give(courier, relic)`.
- КОЛИ `input(drag, item, unit)` → ТО `custom: «вішається; деякі пари збираються в сильніший»` (`merge`).
- КОЛИ `hp_zero(courier)` → ТО `custom: «вибув на місце 8…2»`; останній — `win`; КОЛИ топ-ранг → ТО `give(candies)`.
- Перемога: останній живий з 8 · Поразка: HP кур'єра = 0 · Рахунок: місце, ранг (шахові звання (?)).

## Керування і ввід
- Миша: клік по слоту магазину — купити; drag фігури лава ↔ дошка, на магазин — продати; drag предмета на фігуру.
- ПКМ — рух кур'єра (збір луту); гарячі клавіші Dota-клієнта для рероллу й XP (?).

## Вікна, меню, HUD
- `lobby-window` — пошук гри в клієнті Dota 2 (Arcade), рангові/звичайні матчі.
- `game-screen`: шахівниця, лава, кур'єр; `+ui:shop-bar` (фігури з ціною, расою/класом, Reroll, XP, Lock), `coins` (як мана кур'єра), рівень/XP, `+ui:synergy-panel` (раси/класи з порогами), `+ui:player-list` (HP усіх 8), `timer-countdown` фази, номер раунду, `tooltip`.
- `end-screen` — місце, зміна рангу; `shop-window` кур'єрів за candies (косметика).
- Переходи: lobby → завантаження → game-screen (раунди) → end-screen.

## Фічі поза полем
- `mode-versus` на 8 гравців; рангова драбина `rank-tiers`; `leaderboard-online`.
- Косметика: кур'єри, ефекти за candies (`unlockables`).
- Окремий standalone Auto Chess (Drodo, мобільні/PC/PS4) і спін-офи — див. варіації.

## Варіації й родичі
- Спадкоємці: Auto Chess (standalone, Drodo), Dota Underlords (Valve), [teamfight-tactics](teamfight-tactics.md) (Riot; гекси, карусель, аугменти), Hearthstone Battlegrounds (ряд без поля), [super-auto-pets](super-auto-pets.md) (асинхронний 1D-ряд), [mechabellum](mechabellum.md) (автобій загонів).
- Родичі-попередники: [legion-td](legion-td.md) (розставив захисників — далі бій сам).
- **Осі варіацій**: дошка — квадрати (DAC) / гекси (TFT) / ряд (SAP) · бій — вдома/на виїзді · бонуси — відсотки, стріки, перерваний стрік · пул копій — спільний / особистий.

## Цікавинки для курсу
- Спільний скінченний пул копій і шанси магазину за рівнем — 🥈.
- Злиття 3 → 2★, 9 → 3★ з урахуванням лави й дошки (каскад) — 🥉.
- Синергії рас і класів: одна фігура в кількох лічильниках, пороги — 🥉.
- Економіка: відсотки з капом + стріки + бонус за перерваний стрік — 📎.
- Автобій на квадратній сітці: найближча ціль, рух, атака, мана — 🥈.

## Мапа на каталог
- Є: `round-currency` ↔ золото · `shop-catalog` ↔ магазин · `shop-buyback` ↔ продаж · `tile-merge` ↔ 3 копії · `inventory-items` + `inventory-limit` ↔ предмети, лава 8 · `drag-drop-piece` ↔ розстановка · `hp-damage` · `chase-greedy` · `melee-vs-ranged` · `ai-opponent` + `enemy-waves` ↔ крипи · `move-timer` ↔ таймер фази · `online-multiplayer` · `run-relics` ↔ реліквії · `leaderboard`.
- **Нема** → пропозиції карток (більшість уже запропоновані в teamfight-tactics):
  - `+auto-battle` · `+bench-and-board` · `+interest-economy` · `+streak-bonus` · `+shop-reroll` · `+star-up-merge` · `+trait-synergy` · `+item-combine` · `+shared-unit-pool`.
  - `+home-away-board` «Бій на дошці одного з суперників» · game-logic/opponent · 🌱.
  - `+streak-breaker-bonus` «Нагорода за перерваний чужий стрік» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+role:unit` — бойовий юніт загону; `+role:bench` — зона запасу поза полем.
- `+trigger:round_lost` — сторона програла раунд.
- `+cond:count_unique` — кількість різних сутностей з ознакою (раса/клас).
- `+effect:reroll` — оновити вітрину; `+effect:interest` — дохід від накопиченого; `+effect:sell` — продати сутність за частину ціни.
- `+ui:synergy-panel` — список рас/класів з лічильниками; `+ui:shop-bar`; `+ui:player-list`.
- `+window:lobby-window` — лобі в клієнті-хості (Dota 2 Arcade).
- `+axis:time` — значення `phased` (планування + автобій).

## Джерела
- ⭐ [Wikipedia: Dota Auto Chess](https://en.wikipedia.org/wiki/Dota_Auto_Chess) — 8 гравців, кур'єр (HP, золото-мана, рівень), фази income/preparation/battle, +1 за 10 золота, стріки ≥5, перерваний стрік, лава 8, 3 копії → 2★, 3 × 2★ → 3★, раси/класи, спільний пул, home/away, крипи → предмети, реліквія кожен 10-й раунд, candies; Drodo Studio, 4.01.2019.
- [Wikipedia: Auto battler](https://en.wikipedia.org/wiki/Auto_battler) — жанр і спадкоємці (з черги; не відкривав окремо).
- [Gamesight: порівняння автобатлерів](https://blog.gamesight.io/auto-battlers-have-arrived-teamfight-tactics-vs-dota-underlords-vs-auto-chess/) — з черги; не відкривав.

## Непевне
- (?) Розмір дошки 8×8 — за назвою «шахи» й черги; Wikipedia каже лише «перші 4 ряди — для розстановки».
- (?) Кап відсотків (Wikipedia-витяг каже «capped at 40 gold» — неоднозначно: +4 чи кап банку), розміри бонусів за стрік.
- (?) Формула шкоди кур'єру, вартість рероллу й XP, кількість слотів магазину (у TFT — 5).
- (?) Чи повертається продана фігура в пул; назви рангів (Pawn, Knight, Bishop, Rook, King, Queen — з памʼяті).
