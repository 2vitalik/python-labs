---
title: Patternsight
slug: patternsight
aka: ["Patternsight: read the living world"]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: setup
  goal: territory
year: 2026
platforms: [web]
links:
  - {kind: itch, url: "https://programersi.itch.io/patternsight", best: true, note: "грати в браузері; опис: патерни Life як ферми, стіни, істоти, снаряди; режими Settle / Rival / Trio / Sandbox"}
  - {kind: other, url: "https://programersi.itch.io/patternsight/devlog/1610731/settle-a-world-made-of-conways-life-win-by-seeing-what-it-becomes", note: "девлог 2026-07-31: ресурси, мета — 8 гравців на одній дошці"}
  - {kind: play, url: "https://html-classic.itch.zone/html/17732424-2264560/index.html", note: "HTML5-збірка; у ній вбудована вікі гри (Basics / Mechanics / Life forms / Settings)"}
  - {kind: other, url: "https://itch.io/t/6768896/nice-niche-more-please", note: "відгук гравця і відповідь розробника"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Patternsight+game+of+life+strategy", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cell-click, hover-highlight, cursor-place, piece-rotate-flip, keyboard-controls, game-loop, game-pause, round-currency, spawner-entity, wrap-edges, ai-opponent, realtime-ai, online-multiplayer, lobby-window, mode-select, help-window, codex-window, game-screen, settings-window, achievements-window, end-screen, stats-window, code-editor-window, message-log, objective-text, status-panel, field-scaling, player-camera, replay, share-result, seed-share, state-as-data, +cellular-automaton-rule, +pattern-library, +territory-capture, +territory-by-presence, +pattern-as-unit, +death-yield-mining, +taming-by-territory, +bot-scripting]
proposes: ["+cond:owned_by", "+trigger:covered_by", "+ui:event-arrows", "+ui:size-filter", "+feature:restricted-sets", "+feature:spawn-bot-faction", "+card:pattern-as-unit", "+card:death-yield-mining", "+card:taming-by-territory", "+card:bot-scripting", "+card:deterministic-lockstep"]
author: opus
date: 2026-11-09
---

# Patternsight — стратегія на території, де вся біологія — Life B3/S23: став патерни як будівлі й істот, клейми землю, стріляй глайдерами

## Суть
Інопланетний світ, що вже живе за правилом Конвея (B3/S23): дикі осцилятори дрейфують, на мапі камені й рудні жили. Гравець-поселенець з палітри ставить **патерни Life** як будівлі й юнітів: натюрморти — стіни й «ферми», осцилятори — робоча сила, що заробляє й клеймить землю, глайдери й кораблі — розвідка і снаряди, гармати-«фабрики» — турелі, матусалеми — «бомби». Кожен патерн має ціну в біомасі, відбиток і стадію відкриття; мета — тримати заданий відсоток світу проти AI-поселень. Головна навичка, за назвою гри, — «бачити наперед», у що перетвориться конфігурація.

## Поле і час
- Квадратна сітка, сусідство Мура-8, правило B3/S23 (у налаштуваннях можна інше правило — «експериментально», застосовується після рестарту).
- Розміри сценаріїв: Settle і Trio — 1024×1024, Rival — 768×768, Sandbox — 1024×1024; форма світу — тор (wrap-around) або обмежений стінами.
- Шари клітини: живий/мертвий · фракція · ідентифікатор патерна · камінь · власник території (бітове поле в одному числі).
- Час — покоління-тіки в реальному часі з паузою: «Paused · place & build anytime · press play to run»; темп Glacial / Slow / Normal / Fast / Frantic; крок на одне покоління.
- Камера: пан і зум великої мапи; стрілки на краю екрана показують події поза видом.
- Детермінований двіжок на Rust/WebAssembly; світ засівається за seed (дика екосистема, кластери каменів).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Жива клітина | tile | фракція, патерн | B3/S23; на своїй дозрілій території приносить біомасу |
| Структура (натюрморт: Habitat Block, Storage Hive, Granary Loaf…) | static | ціна 10·клітин | не змінюється; якорить територію, стіна |
| Їдець (Fishhook Eater, Greater Eater) | static | — | «зʼїдає» вторгнення, сам відновлюється |
| Істота (осцилятор: Pulse Grazer, Toad Beast, Pulsar Colossus, Clock…) | ally | ціна 35·клітин − 10 | пульсує вічно; заробляє, клеймить землю навколо |
| Корабель (Scout Glider, Skiff/Middleweight/Heavyweight Cruiser, Copperhead, Sir Robin…) | projectile | ціна 100 + 24·клітин | летить; таранить структури й істот; у польоті не заробляє |
| Турель-фабрика (Glider Foundry, Twin Foundry, AK-94 Gun…) | spawner | ціна 1750 + 50·клітин | безперервно випускає глайдери |
| Насіння (T-Seed, Switch Engine, Noah's Ark, Spacefiller II, Sawtooth 262) | spawner | ціна 126·клітин − 280 | росте/залишає слід (паффери, наповнювачі) |
| Бомба-матусалем (R-Seed, Acorn Bloom, Diehard, Herschel, Lidka…) | object | ціна 2000 + клітин; потребує заліза | хаотичний вибух росту на чужій землі |
| Гліф (0–9, A–Z) | object | — | декоративні патерни-літери |
| Дика істота | neutral | бурштиновий колір | дрейфує; на твоїй землі переходить до тебе |
| Камінь | static | — | непрохідний для життя |
| Рудна жила | resource | запас | клітина, що вмирає на краю жили, дає 1 залізо |
| Територія | zone | власник, «дозрілість» | дає дохід і місце для будівництва; вигасає без утримання |
| Бот-поселення | enemy | heuristic-v2, рішення раз на 50–100 тіків | будує, розширює кордон, бомбить при загрозі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `cell(x, dead)` and `adjacent_count(x, live, ==, 3)` → ТО `set_cell(x, live)`; ЯКЩО `cell(x, live)` and `adjacent_count(x, live, in, {2,3})` → лишається; інакше `set_cell(x, dead)`.
- КОЛИ `input(place, pattern)` → ЯКЩО `counter(biomass, >=, cost)` and `in_range(footprint, own_territory, 14)` and `not cell(footprint, enemy_territory)` and `custom: «стадія патерна відкрита»` → ТО `place(player, pattern)`, `currency(-cost)`, `paint(footprint + halo, player)` (гало — 3 клітини).
- … інакше `message("Not enough biomass.")` / `message("Too far from your territory.")` / `message("Cannot build on another faction’s territory.")`.
- Ціна: `custom: «max(4, round(base + mult · кількість_клітин)) за категорією»` — структура 0 + 10, істота −10 + 35, корабель 100 + 24, турель 1750 + 50, насіння −280 + 126, бомба 2000 + 1.
- КОЛИ `input(rotate, Q|E)` → ТО `rotate(ghost, ±90)` до розміщення.
- КОЛИ `timer(income_interval)` → ЯКЩО `cell(x, live)` and `custom: «клітина стоїть на власній дозрілій території»` → ТО `currency(+rate)`; вищі стадії патернів платять більше за клітину; щойно заклеймлена земля не платить, доки не «дозріє».
- КОЛИ `tick` → ЯКЩО `custom: «жива істота фракції»` → ТО `paint(cells_around, faction)` — живе продовжує клеймити сусідні клітини.
- КОЛИ `timer(spread_interval)` → ЯКЩО `custom: «кордон утримується достатньо довго»` → ТО `custom: «кордон розквітає назовні в дику землю»`.
- КОЛИ `custom: «клітину території ніщо не утримує»` → ТО `paint(cell, wild)` — земля повільно повертається до дикої.
- КОЛИ `died(cell)` → ЯКЩО `adjacent_count(cell, ore_vein, >=, 1)` → ТО `counter(iron, +1)` — залізо не копають, його «перемелює» життя на краю жили.
- КОЛИ `custom: «твоя територія накрила дику істоту»` → ТО `set_side(creature, player)` (бурштин → зелений), істота починає платити біомасу.
- КОЛИ `input(harvest, cell)` → ЯКЩО `custom: «вистачає заліза»` → ТО `clear(3×3)`, `currency(+burst)` — разовий урожай з живих клітин.
- КОЛИ `contact(ship, structure|creature)` → ТО `custom: «звичайна Life-реакція: корабель і ціль руйнуються чи перетворюються»`; КОЛИ `contact(ship, eater)` → ТО `disappear_a` (їдець лишається).
- Турель: КОЛИ `custom: «період гармати»` → ТО `spawn(glider)` — не правило гри, а властивість патерна.
- КОЛИ `input(unlock, n)` → ЯКЩО `counter(biomass, >=, B_n)` and `counter(iron, >=, I_n)` → ТО `unlock(stage_n)`: 2 Builder — 300 + 15 заліза, 3 Engineer — 2000 + 40, 4 Combatant — 5000 + 120, 5 Pufferfish — 15000 + 300 (1 — Settler).
- КОЛИ `timer(60)` → ЯКЩО `counter(territory_pct, >=, goal)` → ТО `win` (Settle — 17 %, Rival і Trio — 22 %); якщо поріг узяв бот → `lose`.
- Інші умови в коді: «Last standing» — КОЛИ `all_gone(rival_settlement)` → ТО `win`; «Score» — `counter(score, >=, n)`.
- Виклик: КОЛИ `counter(gen, >=, deadline)` → ЯКЩО `counter(territory_pct, <, goal)` → ТО `lose` («Time’s up»); набори-обмеження «No Ships», «Structures Only», «Methuselahs Only»… забороняють категорії.
- Перемога: частка світу · Поразка: поріг узяв суперник / вичерпано час виклику · Рахунок: покоління, коли досягнуто мети («Best: gen N»).

## Керування і ввід
- Миша: клік по дошці — поставити вибраний патерн (з «привидом» під курсором); Q / E або кнопки — поворот привида; Harvest — клік по клітині; Pencil — малювати окремі живі клітини (дотик: один палець малює, два — рухають дошку).
- Space — Play / Pause; кнопка кроку на одне покоління; перемикач темпу.
- Палітра патернів: категорії Structures / Creatures / Ships / Turrets / Seeds / Bombs / Glyphs / Tools і фільтр розміру (≤5, 6–12, 13–30, 30+); вибір кольору патерна.
- Sandbox: Iron Vein (поставити скелю з 1–4 жилами), виклик бот-фракції в точку (очищає 30×30 і ставить стартовий набір).
- Bot Lab: бот — JS-модуль з `config`, `onMatchStart`, `onScan`; API на кшталт `ctx.settle()`, `ctx.expandFrontier()`, `ctx.defendWithBomb()`; бюджет обчислень на хід.

## Вікна, меню, HUD
- `main-menu` («Xenosurvey · Living-World Protocol»): картки режимів Settle / Rival / Trio / Sandbox / Multiplayer / Bot Lab → `mode-select`.
- `custom-window` вибору виклику: Free Play або Challenge («Claim N % by gen T») × Pattern Set; прогрес «sets mastered».
- `game-screen`: дошка; HUD — `custom: «Gen»`, Biomass, Iron, Territory (`progress-bar`-подібно), `objective-text` («Control 22 % of the world»); панелі Growth (відкрити стадію) / Build (палітра) / Time (крок, play, темп); `event-arrows` до подій поза видом (червоні — твої втрати, зелені — суперника).
- `log-window`-подібна панель Events: Placements / Network («{actor} placed {pattern}», «Match started», «Match over»).
- `help-window` / `codex-window`: вбудована вікі з розділами Basics · Mechanics · Life forms · Settings і живими міні-дошками до кожної теми (Reading Life, Placing patterns, Territory, Biomass, Iron, Creatures & structures, Wild & taming, Gliders, Turrets…).
- `settings-window` з вкладками: Field (Recordings, налаштування партії: seed, розмір, форма світу, правило; Reset / Export / Import), Trophies, Effects (звук, музика, шари відображення), Notes (кредити, встановити як застосунок).
- `achievements-window` (Trophies): полиця пройдених викликів з карткою для поширення.
- `end-screen`: Victory / Defeated / Draw · «Keep exploring» · «Review stats».
- `stats-window` («Survey summary» / Field Log): покоління, поставлено патернів, зібрано, зароблено біомаси, видобуто заліза, пік території й живих клітин, найчастіший патерн, «You vs rivals».
- `replay-window` (Recordings): до 100 записів — Replay / Load / Share-посилання, значок «may desync».
- `lobby-window` (Xenosurvey Network): адреса релея, позивний, код каналу, список відкритих партій, spectate, «Confirm Presence», зворотний відлік.
- `code-editor-window` (Bot Lab): Run / Save / New / My Bots / Examples / Reference / Fork, журнал бота по тіках.

## Фічі поза полем
- Режими: `mode-classic` (Settle — проти дикої екосистеми), `mode-versus` проти AI (Rival — один бот, Trio — троє), `mode-sandbox` (безмежні ресурси, усі патерни), мультиплеєр (рання стадія, детермінований через релей), Bot Lab (у веб-збірці — «Available in the local build for now»).
- Прогресія в партії — 5 стадій Growth за біомасу й залізо; поза партією — виклики з наборами-обмеженнями і трофеї.
- `replay` + `share-code` (посилання на повтор), `export-import` партії, `autosave` записів, `seed-input` у налаштуваннях партії.
- `custom-rules` (правило B/S, тор / стіни, розмір), `speed-control`, `step-mode`, `tutorial` (інтерактивна вікі), `sound-toggle` / `music-toggle`, `animation-toggle`-подібні перемикачі ефектів.
- `share-result`: картка колонії з QR «Scan to settle your own world»; встановлення як PWA.

## Варіації й родичі
- Задум автора — до 8 людей на одній дошці; поки одиночна гра з ботами (девлог).
- **Осі варіацій** «Life як RTS»: що є юнітом (готовий патерн з ціною / вільне малювання клітин) · як рахується власність (територія з гало й вигасанням / колір клітини, як у Immigration) · ресурс (біомаса з землі, залізо з «смертей» біля жил) · мета (частка світу / останній вижилий / очки).
- Родичі в корпусі: [game-of-life](game-of-life.md) (двіжок і патерни), [cell-machine](cell-machine.md), [brians-brain-seeds](brians-brain-seeds.md); у `tower-lanes` — турелі як «фабрики глайдерів»; гравець порівнює з Abstractia Worlds (ітч-відгук).
- Immigration / QuadLife (фракції-кольори в Life) — ідейні предки PvP-автоматів (див. «Варіації» в game-of-life).

## Цікавинки для курсу
- Палітра патернів з RLE, «привид» з поворотом Q/E і перевіркою «в радіусі своєї території, не на чужій» — 🥉.
- Ціна за формулою base + mult · клітин і стадії відкриття за категорією й розміром — 🌱.
- Шар території: клейм відбитку + гало, клеймлення навколо живих, вигасання без утримання, «дозрівання» для доходу — 🥈.
- Залізо з клітин, що вмирають біля жили, і приручення диких істот накриттям територією — 📎 кожне.
- Детермінований тік + запис лише дій гравців → повтор і посилання-реплей; «may desync» при іншій логіці ботів — 🥈.
- Евристичний бот (settle / expand frontier / defend with bomb) і пісочниця для ботів студентів з бюджетом обчислень — 🥇.
- Виклики «N % до покоління T» з наборами-заборонами категорій — 📎.

## Мапа на каталог
- Є: `cell-click` + `hover-highlight` + `cursor-place` ↔ розміщення · `piece-rotate-flip` ↔ Q/E · `keyboard-controls` · `game-loop` + `game-pause` · `round-currency` ↔ біомаса · `spawner-entity` ↔ турелі · `wrap-edges` ↔ тор · `ai-opponent` + `realtime-ai` ↔ боти · `online-multiplayer` + `lobby-window` · `mode-select` · `help-window` + `codex-window` ↔ вікі «Life forms» · `settings-window` · `achievements-window` ↔ Trophies · `end-screen` · `stats-window` · `code-editor-window` ↔ Bot Lab · `message-log` ↔ Events · `objective-text` · `status-panel` · `field-scaling` + `player-camera` · `replay` · `share-result` · `seed-share` · `state-as-data`.
- **Нема** → пропозиції карток:
  - `+pattern-as-unit` «Патерн автомата як юніт/будівля з ціною, відбитком і стадією» · entities · 🥉 · слоти {category, cost_formula}.
  - `+death-yield-mining` «Ресурс з клітин, що вмирають біля жили» · game-logic/economy · 📎.
  - `+taming-by-territory` «Нейтральна сутність переходить до того, чия територія її накрила» · entities/interact · 📎.
  - `+bot-scripting` «Користувацькі боти: API, бюджет обчислень, журнал» · game-logic/opponent · 🥇.
  - `+deterministic-lockstep` «Детермінований тік: мультиплеєр і повтор через лише дії» · code/architecture · 🥈.
  - Перевикористано: `+cellular-automaton-rule`, `+pattern-library`, `+territory-capture`, `+territory-by-presence`.

## Пропозиції до словників
- `+cond:owned_by` — клітина/сутність на території сторони (шар власника окремо від типу клітини: дохід, розміщення, приручення).
- `+trigger:covered_by` — зона сторони накрила сутність (приручення дикої істоти).
- `+ui:event-arrows` — стрілки на краю вʼюпорта до подій поза видом, колір за наслідком.
- `+ui:size-filter` — фільтр палітри за розміром патерна.
- `+feature:restricted-sets` — виклики з забороненими категоріями («Structures Only», «No Ships»).
- `+feature:spawn-bot-faction` — у пісочниці поставити бота-суперника в точку мапи.
- `+card:pattern-as-unit`, `+card:death-yield-mining`, `+card:taming-by-territory`, `+card:bot-scripting`, `+card:deterministic-lockstep` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch.io: Patternsight](https://programersi.itch.io/patternsight) — опис, ролі патернів (натюрморти — ферми й стіни, осцилятори — істоти й двигуни, глайдери — снаряди й розвідка), режими Settle / Rival / Trio / Sandbox, ввід клавіатура/миша/тач, MIT-код, AI-асистований код.
- [Девлог 2026-07-31](https://programersi.itch.io/patternsight/devlog/1610731/settle-a-world-made-of-conways-life-win-by-seeing-what-it-becomes) — одиночна збірка для фідбеку, мета — 8 людей на дошці, ресурси «focus, biomass, iron».
- [HTML5-збірка](https://html-classic.itch.zone/html/17732424-2264560/index.html) — прочитано як текст (не запускав): вбудована вікі, рядки інтерфейсу, конфіги сценаріїв (розміри, пороги 17/22 %, стартові 600 біомаси), формула ціни, вартості стадій, категорії й назви патернів, API ботів.
- [Відгук «Nice Niche, More Please»](https://itch.io/t/6768896/nice-niche-more-please) — програш першої партії одному боту, порівняння з Abstractia Worlds.

## Непевне
- (?) Ресурс «focus» з девлогу в поточній збірці не знайдено (HUD: Gen, Biomass, Iron, Territory) — можливо, прибраний.
- (?) Кому належить клітина, що народилась між патернами різних фракцій, і як саме працює «розквіт» кордону — у тексті збірки лише параметри.
- (?) Скільки заліза коштує Harvest і бомби — у конфігу є `ironPerHarvest: 20`, але неясно, витрата це чи дохід.
- (?) Числа (розміри, пороги, ціни) — з конфігу збірки станом на листопад 2026; гра в розробці, можуть змінитись.
- (?) Bot Lab у веб-версії, схоже, вимкнений («local build»); мультиплеєр — «not open to the public yet» в одному з рядків.
