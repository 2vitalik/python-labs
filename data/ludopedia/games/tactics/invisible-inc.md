---
title: Invisible, Inc.
slug: invisible-inc
aka: [Invisible Inc, Incognita]
family: tactics
also: [roguelike]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2015
platforms: [PC, Mac, Linux, PS4, iOS, Switch]
links:
  - {kind: other, url: "https://gamedeveloper.com/design/game-design-deep-dive-alarm-systems-in-klei-s-i-invisible-inc-i-", best: true, note: "deep dive від розробників: тривога 0–6 по 5 поділок, що її піднімає, рівні 2 і 3, чому так"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Invisible,_Inc.", note: "огляд: AP агентів, Incognita і PWR, 3 дні кампанії, смерть агента, процедурні місії, DLC, платформи"}
  - {kind: other, url: "https://www.gamedeveloper.com/design/lesson-the-problems-of-modern-stealth-design-and-how-invisible-inc-solves-them", note: "поведінка охорони: підозра, пошук, укриття лише затримує, крик у кімнаті, звук"}
  - {kind: steam, url: "https://store.steampowered.com/app/243970/Invisible_Inc/", note: "10 агентів + 6 варіантів, 6 стартових програм, аугменти, 5 режимів, кастомна генерація"}
  - {kind: other, url: "https://steamcommunity.com/app/243970/discussions/0/617336568086845807", note: "форум: укриття і зір, периферійний зір"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Invisible+Inc+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [fog-of-war, enemy-patrol, chase-bfs, key-and-door, reach-exit, permadeath, hp-damage, status-effects, temporary-modes, inventory, inventory-items, inventory-limit, round-currency, shop-between-levels, shop-catalog, in-round-upgrades, run-relics, path-preview, threat-range, legal-move-highlight, hover-highlight, button-toggle, reinforcements, spawn-schedule, dungeon-generation, difficulty-levels, game-settings, map-window, character-select, mode-select, save-autosave, game-screen, main-menu, end-screen, +vision-cone, +peek, +alarm-clock, +action-points, +overwatch, +ko-and-pin, +hacking-layer, +noise-lure, +campaign-time-budget, +meta-unlocks]
proposes: ["+trigger:seen", "+trigger:noticed", "+trigger:alarm_level", "+cond:in_vision", "+cond:in_cover", "+effect:alert", "+effect:investigate", "+effect:hack", "+effect:ko", "+role:device", "+role:camera", "+ui:vision-cone", "+ui:alarm-dial", "+ui:pwr-counter", "+window:mainframe-view", "+window:agency-screen", "+window:destination-map", "+feature:custom-generation"]
author: opus
date: 2026-11-09
---

# Invisible, Inc. — покроковий шпигунський стелс: конуси зору, тривога, що росте щоходу, і хакерський шар над кожним пристроєм

## Суть
Гравець — куратор агентів, що проникають у корпоративні будівлі. Кожен агент має очки дії (AP) на хід: рух клітинами, двері, тихе знешкодження охоронця, взаємодія з терміналами. Охорона бачить **конусами зору**, і будь-яка помилка коштує дорого; але головний ворог — **тривога (Security Level)**: вона росте наприкінці кожного ходу й приносить нові патрулі, камери, вогнестіни. Паралельно діє друга дошка — мейнфрейм: ШІ Incognita витрачає PWR, щоб зламати камери, дверні замки, сейфи й турелі. Місія: забрати ціль і вийти через ліфт, поки будівля не стала смертельною.

## Поле і час
- Квадратна сітка кімнат і коридорів, ізометричний рендер; стіни, двері (відчинені/зачинені), укриття (столи, шафи), пристрої.
- Туман: агенти бачать лише свої лінії; невідвідані кімнати сховані; двері блокують лінію, підглядання (peek) показує, що за дверима/рогом.
- Хід гравця: усі агенти витрачають AP у будь-якому порядку → кінець ходу → хід охорони (патруль, пошук, атака) → тривога +1 поділка.
- Тривога 0–6, кожен рівень має 5 поділок; ефект настає, лише коли заповнились усі 5 (gamedeveloper).
- Мета-час кампанії: 3 ігрових дні до фінальної місії; переліт і місії зʼїдають цей запас (Wikipedia).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Агент | piece | AP на хід, HP (?), інвентар, аугменти | рух, двері, peek, takeout, взаємодія; загиблий лежить до медкіта або виносу до виходу |
| Incognita (ШІ) | player | PWR, програми | мейнфрейм-дія: ламає вогнестіни пристроїв за PWR |
| Охоронець | enemy | конус зору, периферійний зір | патрулює; підозрілий — сходить з маршруту й шукає; побачив — кричить і стріляє (?) |
| Elite Enforcer | enemy | — | викликається тривогою / подіями; сканувальні гранати бачать крізь укриття (форум) |
| Дрон / робот-охорона (?) | enemy | — | механічний: не вирубується нейро-шокером (?) |
| Камера | enemy | конус, вогнестіна | бачить агентів → тривога / охорона на місце; хакінгом вимикається |
| Турель (?) | enemy | вогнестіна | стріляє у видимого агента; хакнута стріляє по охороні (?) |
| Консоль | resource | — | захоплення → +PWR |
| Сейф | container | вогнестіна / замок | гроші (credits) або предмет; відкрити — PWR |
| Пристрій з daemon | hazard | прихований daemon | злам запускає шкідливий ефект проти гравця |
| Двері | gate | відчинені/зачинені | блокують зір; відкриття коштує AP; камера чи охорона з того боку може помітити |
| Замок / лазерна сітка (?) | gate | вогнестіна | прохід після злому |
| Укриття | static | — | присівши за ним, агент схований від зору; охоронець може підійти й зазирнути |
| Тіло / вирубаний охоронець | object | таймер KO | приходить до тями; притиснутий агентом на тій самій клітині — ні |
| Ціль місії (vault, в'язень, детектив...) | object | — | залежить від типу обʼєкта; в'язень = новий агент |
| Ліфт виходу | static | — | евакуація: агенти на клітинах ліфта — місію закінчено |
| Точка входу | static | — | старт агентів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, agent, cell)` → ЯКЩО `has(agent, ap, path_len)` → ТО `move(agent, cell)`, `counter(ap, -path_len)`.
- КОЛИ `input(peek, agent, door)` → ТО `reveal(cells_behind)` без відчинення (?) — ціна 1 AP (?).
- КОЛИ `input(open, door)` → ТО `set_cell(door, open)`, `counter(ap, -1)`; ЯКЩО `line_of_sight(guard|camera, agent)` → ТО агента помічено.
- КОЛИ `input(takeout, agent, guard)` → ЯКЩО `adjacent(agent, guard) and has(agent, charged_melee)` → ТО `custom: «KO на N ходів»`, `set_state(weapon, recharging)`.
- КОЛИ `turn_start(enemy)` → ЯКЩО `state(guard, ko) and occupied(cell, agent)` → ТО KO триває (pin); інакше `counter(ko_timer, -1)` → при 0 `clear_state(ko)` і охоронець прокидається насторожений (?).
- КОЛИ `input(kill, guard)` → ТО `disappear_b`, `counter(alarm, +1)` (вбивство піднімає тривогу).
- КОЛИ `custom: «агент у периферійному зорі»` → ТО `set_state(guard, noticed)`: повертається / йде перевірити.
- КОЛИ `line_of_sight(guard, agent)` → ЯКЩО `not custom: «агент у укритті»` → ТО `set_state(guard, alerted)`: конус ~180°, кричить — охорона **в тій самій кімнаті** розвертається; наступного ходу стріляє (?).
- КОЛИ `custom: «охоронець бачить тіло»` → ТО `counter(alarm, +1)`, `set_state(guard, searching)`.
- КОЛИ `state_on(guard, suspicious)` → ТО `custom: «сходить з маршруту й шукає»` (`chase-bfs` до останньої відомої точки); укриття лише затримує — він може підійти й зазирнути.
- КОЛИ `custom: «шум»` → ТО охорона `custom: «завжди йде перевірити»` (noise lure).
- КОЛИ `input(ambush, agent)` → ТО `set_state(agent, ambush)`: охоронець, що зайде в сусідню клітину, отримує KO без витрати AP (?).
- КОЛИ `input(overwatch, agent)` → ТО `set_state(agent, overwatch)`: постріл у першого ворога в лінії (?).
- КОЛИ `input(hack, device)` → ЯКЩО `has(incognita, pwr, cost)` → ТО `counter(firewall, -n)`; КОЛИ `counter(firewall, ==, 0)` → ТО `set_side(device, player)` (камера вимкнена, сейф відкритий, консоль дає PWR).
- КОЛИ `after(hack, device_with_daemon)` → ТО `custom: «daemon: негативний ефект»` (+тривога, +вогнестіни, −PWR тощо (?)).
- КОЛИ `turn_end(player)` → ТО `counter(alarm, +1)` (поділка); КОЛИ `counter(alarm_ticks, ==, 5)` → ТО `counter(alarm_level, +1)` і ефект рівня.
- КОЛИ `counter(alarm_level, ==, 2)` → ТО `custom: «усі вогнестіни будівлі +1»`.
- КОЛИ `counter(alarm_level, ==, 3)` → ТО `spawn_at(patrol, entry)` (новий патруль); вищі рівні — нові камери, Enforcer-и (?).
- КОЛИ `hp_zero(agent)` → ТО `set_state(agent, down)`; ЯКЩО `custom: «медкіт»` → ТО `heal(agent)`; ЯКЩО `custom: «тіло винесли до ліфта»` → ТО агент вцілів; інакше втрачений до кінця забігу.
- КОЛИ `all_on(agents, exit)` → ТО `custom: «евакуація»` → `window(end-screen)`; ціль може бути не виконана — місія все одно закінчена.
- КОЛИ `custom: «загинули всі агенти»` → ТО `lose` (кінець кампанії).
- КОЛИ `counter(days_left, ==, 0)` → ТО `custom: «фінальна місія»`; її успіх → `win`.
- Перемога: пройти фінальну місію після 3 днів · Поразка: усі агенти втрачені · Рахунок: зібрані credits, предмети, вцілілі агенти.

## Керування і ввід
- Миша: клік по агенту → клік по клітині з превʼю шляху і ціни AP (`path-preview`); наведення на клітину показує, чи вона під зором.
- Перемикання на мейнфрейм (окремий режим відображення) → клік по пристрою → вибір програми злому.
- Дії агента — кнопки (peek, takeout, ambush, overwatch, предмети); кінець ходу — кнопка.
- Ресурс для передбачення руху охорони (?) — шпигунські дії/програми показують, куди піде охоронець (gamedeveloper «Lesson»).

## Вікна, меню, HUD
- `main-menu`: Продовжити · Нова гра → `mode-select` (режими складності, кастомна генерація) → `character-select` (пара агентів і стартові програми) · Налаштування · Вихід.
- `map-window` — карта світу з цілями місій (тип обʼєкта, ризик, переліт у годинах).
- `game-screen`: ізометрична мапа; `fog-overlay`; конуси зору охорони (червоний / світліший периферійний); `action-points` агента; `hp-bar`; `inventory-bar`; PWR Incognita; диск тривоги з 5 поділками і `tooltip` «що буде на наступному рівні»; `path-preview`; `end-turn-button`.
- `custom-window` «Mainframe» — той самий план, але видно пристрої, вогнестіни, daemon-позначки, програми.
- `shop-window` — магазин на станціях / у місії (?): предмети, аугменти, програми за credits.
- `upgrade-window` — агентство між місіями: прокачка характеристик агентів, аугменти (?).
- `end-screen` — підсумок місії; кінець кампанії.
- `confirm-dialog`, `pause-menu`.

## Фічі поза полем
- Кампанія: 3 дні часу, вибір місій на карті світу, фінальна місія; процедурні рівні, цілі й лут.
- `permadeath` агентів і кампанії; автосейв (?), повтор програної місії на складніших рівнях за замовчуванням недоступний.
- `meta-progression`: виконання цілей відкриває нових агентів і стартове спорядження (10 агентів + 6 варіантів).
- `difficulty-presets` (5 режимів) і `custom-difficulty` (повна кастомізація генерації).
- DLC Contingency Plan: нові агенти, вороги, місії, довша кампанія, рівні складності місій.

## Варіації й родичі
- Родичі в корпусі: [xcom](xcom.md) (загін, AP, overwatch), [spybot-nightfall](spybot-nightfall.md) (хакерська сітка), [frozen-synapse](frozen-synapse.md) (тісні кімнати, лінії зору).
- Поза корпусом: Hitman GO / Lara Croft GO (покроковий стелс на графі), Desperados III / Shadow Tactics (конуси зору в реальному часі), Heat Signature, Monaco.
- Натхнення тривоги — «голод» з NetHack, бомби XCOM, флот FTL, привид Spelunky (gamedeveloper).
- **Осі варіацій**: таймер тиску — голод / тривога / ворожий флот · зір — конус / радіус / лінія · знешкодження — KO з таймером / вбивство з ціною / обхід · другий шар — мейнфрейм (Incognita) / нема.

## Цікавинки для курсу
- Тривога як «голод»: росте щоходу, по 5 поділок на рівень, ефекти рівнів 2/3/… і підказка «що буде далі» — 📎.
- Конус зору з периферією (noticed vs seen) і станами охоронця patrol → noticed → searching → alerted — 🥈 (FSM + видимість).
- KO з таймером і «притиснути» (агент на тій самій клітині) — 🌱.
- Другий шар поля (мейнфрейм): пристрої з вогнестінами, PWR, програми, приховані daemons — 🥉.
- Підглядання за двері/ріг: часткове розкриття туману без дії — 📎.
- Стратегічний бюджет часу кампанії (3 дні, переліт коштує годин) — 📎.

## Мапа на каталог
- Є: `fog-of-war` · `enemy-patrol` · `chase-bfs` (пошук гравця) · `key-and-door` (замки/двері) · `reach-exit` (ліфт) · `permadeath` · `hp-damage` · `status-effects` / `temporary-modes` (KO, alerted) · `inventory` / `inventory-items` / `inventory-limit` · `round-currency` (credits, PWR) · `shop-between-levels` / `shop-catalog` · `in-round-upgrades` / `run-relics` (аугменти, програми) · `path-preview` · `threat-range` (конуси) · `legal-move-highlight` · `hover-highlight` · `button-toggle` (злам пристрою) · `reinforcements` / `spawn-schedule` (патрулі з тривогою) · `dungeon-generation` · `difficulty-levels` · `game-settings` · `map-window` · `character-select` · `mode-select` · `save-autosave`.
- **Нема** → пропозиції карток:
  - `+vision-cone` «Конус зору з периферією» · entities/state · 🥉 · {angle, range, peripheral}.
  - `+peek` «Підглянути за двері/ріг» · interface/render · 📎.
  - `+alarm-clock` «Тривога росте щоходу» · game-logic/waves · 📎 · {ticks_per_level: 5, levels: 6}.
  - `+action-points` «Очки дії на юніта» · game-logic/economy · 🌱.
  - `+overwatch` «Реакційний постріл/засідка» · entities/combat · 📎.
  - `+ko-and-pin` «Вирубити на N ходів і притиснути» · entities/state · 🌱.
  - `+hacking-layer` «Мейнфрейм: пристрої з вогнестінами» · entities/interact · 🥉.
  - `+noise-lure` «Шум приманює ворога» · entities/move · 📎.
  - `+campaign-time-budget` «Бюджет часу кампанії» · levels/progression · 📎.
  - `+meta-unlocks` «Відкриття агентів між забігами» · levels/progression · 📎.

## Пропозиції до словників
- `+trigger:seen` / `+trigger:noticed` — агент потрапив у основний / периферійний зір (дві різні реакції).
- `+trigger:alarm_level` — глобальний лічильник тривоги перейшов рівень.
- `+cond:in_vision` — клітина в конусі зору ворога; `+cond:in_cover` — агент за укриттям і присів.
- `+effect:alert` — перевести ворога в стан тривоги; `+effect:investigate` — ворог іде до точки (шум, тіло, остання позиція).
- `+effect:hack` — зменшити вогнестіну пристрою за ресурс; `+effect:ko` — вирубити на N ходів (тіло лишається на клітині).
- `+role:device` — пристрій з вогнестіною і власником (камера, турель, сейф, консоль); `+role:camera` — нерухомий спостерігач з конусом.
- `+ui:vision-cone` — конуси зору (основний/периферійний кольором); `+ui:alarm-dial` — диск тривоги з поділками; `+ui:pwr-counter` (`action-points` вже є).
- `+window:mainframe-view` — той самий план у шарі пристроїв; `+window:agency-screen` — агентство між місіями; `+window:destination-map` — карта світу з часом перельоту.
- `+feature:custom-generation` — ручні параметри генерації кампанії.

## Джерела
- ⭐ [Game Developer: Alarm systems deep dive](https://gamedeveloper.com/design/game-design-deep-dive-alarm-systems-in-klei-s-i-invisible-inc-i-) — тривога 0–6, 5 поділок, що її піднімає, рівні 2 (вогнестіни +1) і 3 (новий патруль), натхнення і компроміси.
- [Wikipedia](https://en.wikipedia.org/wiki/Invisible,_Inc.) — AP, Incognita + power, 3 дні, смерть агента (медкіт / винести), процедурність, DLC, дати й платформи.
- [Game Developer: Lesson — stealth design](https://www.gamedeveloper.com/design/lesson-the-problems-of-modern-stealth-design-and-how-invisible-inc-solves-them) — підозра й пошук, укриття затримує, крик у кімнаті, звук, ресурс передбачення руху.
- [Steam](https://store.steampowered.com/app/243970/Invisible_Inc/) — 10 агентів + 6 варіантів, 6 програм, аугменти, 5 режимів, кастомна генерація.
- [Steam-форум](https://steamcommunity.com/app/243970/discussions/0/617336568086845807) — укриття і зір (суперечливо), периферійний зір, peek.
- YouTube: пошук «Invisible Inc gameplay».

## Непевне
- (?) Ціни AP (рух 1/клітина, peek, двері), запас AP агента, тривалість KO — з памʼяті.
- (?) Як саме укриття блокує зір (лише клітина за ним чи сектор 90°) — на форумі суперечать.
- (?) Ефекти тривоги вище 3-го рівня (камери, Enforcer-и), daemons і їхні ефекти, турелі, лазерні сітки, дрони — з памʼяті.
- (?) Overwatch / ambush механіка, «стріляє наступного ходу», чи є HP у агентів — з памʼяті й форумних підказок.
- (?) Наявність автосейву і магазину всередині місії — не перевірено.
