---
title: Stardew Valley — фермерська сітка
slug: stardew-farm
family: build-sim
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2016
platforms: [PC, Switch, PS4, Xbox One, mobile]
links:
  - {kind: fandom, url: "https://stardewvalleywiki.com/Sprinkler", best: true, note: "офіційна вікі: форми покриття спринклерів (фетчеру віддала 403)"}
  - {kind: fandom, url: "https://stardewvalleywiki.com/Crops", note: "вікі: стадії, сезони, якість, гігантські культури (403 фетчеру)"}
  - {kind: fandom, url: "https://stardewvalleywiki.com/Scarecrow", note: "вікі: радіус опудала, ворони (403 фетчеру)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Stardew_Valley", note: "сезони по 28 днів, енергія, інструменти"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=stardew+valley", note: "пошук; точну сторінку не бачив"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=stardew+valley+sprinkler+layout+guide", note: "пошук; схеми ферм"}
stage: v1
coverage: 70
mechanics: [move-8dir, impassable-cells, floor-types, cell-transform, multi-cell-size, inventory, inventory-items, inventory-limit, item-pickup, round-currency, shop-catalog, shop-window, save-game, cell-click, hover-highlight, event-points, +day-tick, +growth-stages, +season-kill, +coverage-area, +tool-area-charge, +energy-cost, +quality-roll, +fertilizer-layer, +crow-raid]
proposes: ["+trigger:day_start", "+trigger:season_change", "+trigger:rng", "+trigger:input", "+cond:state", "+cond:in_range", "+cond:cell", "+cond:prob", "+effect:set_cell", "+effect:set_state", "+effect:transform", "+effect:give", "+effect:take", "+effect:counter", "+role:terrain", "+role:resource", "+role:zone", "+ui:energy-bar", "+ui:coins", "+ui:inventory-bar", "+ui:hover-tile-highlight", "+ui:clock-calendar", "+feature:autosave", "+feature:mode-coop", "+window:inventory-window", "+window:shop-window", "+window:end-of-day-shipping", "+card:coverage-area", "+card:growth-stages"]
author: opus
date: 2026-11-02
---

# Stardew Valley (ферма) — клітина ґрунту зі станами «зорано / полито / посаджено» і щоденним ростом

## Суть
Описано **лише фермерську сітку**: гравець-фермер обробляє клітини інструментами (мотика, лійка, коса), садить насіння, щодня поливає, збирає врожай і продає. Кожна клітина ґрунту — маленький автомат зі станами (зорано, полито, удобрено, культура зі стадією), що оновлюється раз на добу. Розміщувані предмети — спринклери, опудала, шпалери — мають **форми покриття** або блокування. Рибалка, шахти, стосунки, тварини — поза описом.

## Поле і час
- Квадратна сітка клітин (тайл 16×16 px); ферма ~80×65 клітин (?) з кількома варіантами мап (Standard, Riverland, Forest, Hill-top, Wilderness, Four Corners, Beach, Meadowlands (?)).
- Шари клітини: тип підлоги (трава/земля/вода/доріжка/підлога будівлі) · ґрунт (`HoeDirt`: зорано, полито, добриво) · обʼєкт зверху (культура, спринклер, опудало, камінь, пеньок, бурʼян).
- Час: **ігровий годинник** 6:00–2:00 (10 ігрових хвилин ≈ 7 с реальних (?)), після 2:00 — непритомність. **День** — головний тік ферми: ріст, полив спринклерами, висихання ґрунту — у момент сну. Сезон — 28 днів, рік — 4 сезони.
- Камера — за фермером; освітлення змінюється за годинником; дощ поливає все просто неба.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фермер | player | енергія (старт 270 (?)), здоровʼя, інвентар | ходить 8 напрямків, бʼє інструментом у клітину попереду |
| Трава/земля | terrain | можна орати | мотика → зораний ґрунт |
| Зораний ґрунт | terrain | сухий/полито, добриво | посадка насіння; без культури може зникнути вночі |
| Полита клітина | terrain | до ранку | темніша; культура росте лише на поливаному ґрунті |
| Культура | object | сезони, днів на стадію, regrow, якість | щодня +1 до стадії, якщо полита; доросла — збір; regrow — після збору знову N днів |
| Гігантська культура (кольорова капуста, диня, гарбуз) | object | 3×3 | шанс злитися з 9 дорослих у квадраті; рубається сокирою, дає багато врожаю |
| Шпалерна культура (квасоля, хміль, виноград) | object | trellis | непрохідна для фермера |
| Мертва культура | object | — | наслідок зміни сезону; прибирається |
| Насіння | pickup | сезон(и) | садиться в зораний ґрунт |
| Добриво (Basic/Quality/Deluxe) | pickup | +якість | шар ґрунту; підвищує шанс кращої якості |
| Speed-Gro / Deluxe / Hyper | pickup | −10% / −25% / −33% днів росту | шар ґрунту |
| Retaining Soil (Basic/Quality/Deluxe) | pickup | шанс лишитись политим | 33% (?) / 66% (?) / 100% |
| Спринклер | object | 1×1, 4 клітини (хрест) | вранці поливає 4 ортогональні сусідні |
| Якісний спринклер | object | 8 клітин (3×3 без центру) | вранці поливає квадрат навколо |
| Іридієвий спринклер | object | 24 клітини (5×5 без центру) | вранці поливає квадрат 5×5 |
| Pressure Nozzle | pickup | +1 до радіусу | спринклер 3×3, якісний 5×5, іридієвий 7×7 (?) |
| Опудало | object | радіус 8 (≈248 клітин) (?) | захищає культури в радіусі від ворон |
| Deluxe-опудало | object | радіус 16 (?) | те саме, більше |
| Ворона | enemy | шанс за ніч | зʼїдає культуру поза зоною опудал |
| Бурʼян/камінь/гілка/пеньок/колода | static | потрібний інструмент і рівень | блокує клітину; знищується косою/кайлом/сокирою |
| Скриня продажу (shipping bin) | container | 2×1 (?) | покладене продається вночі |
| Будівлі (теплиця, хлів, курник, силос) | static | N×M | займають прямокутник; теплиця — ріст без сезонів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(use_hoe, cell)` → ЯКЩО `cell(x, tillable)` and `free(x)` → ТО `set_cell(x, hoe_dirt)`, `counter(energy, -cost)`.
- КОЛИ `input(use_can, cell)` → ЯКЩО `cell(x, hoe_dirt)` and `has(can, water)` → ТО `set_state(x, watered)`; лійка порожніє, наповнюється з води.
- КОЛИ `input(plant, cell)` → ЯКЩО `cell(x, hoe_dirt)` and `free(x)` and `custom: «сезон насіння = поточний»` → ТО `spawn(crop, stage 0)`.
- КОЛИ `day_start` (після сну) → ЯКЩО `state(cell, watered)` → ТО `custom: «crop.stage_day += 1; перехід стадії за таблицею днів»`; ЯКЩО не полито — ріст стоїть, культура **не гине**.
- КОЛИ `day_start` → для кожного спринклера `set_state(cells_in_shape, watered)` (хрест 4 / квадрат 8 / квадрат 24; nozzle +1 кільце).
- КОЛИ `day_start` → ЯКЩО `custom: «дощ»` → ТО всі клітини просто неба `watered`.
- КОЛИ `day_start` → ЯКЩО not `retaining_soil` (або програв шанс) → ТО `clear_state(cell, watered)` (висихає).
- КОЛИ `day_start` → ЯКЩО `cell(x, hoe_dirt)` and нема культури → ТО `rng(p)` → `set_cell(x, grass|dirt)` (?).
- КОЛИ `season_change` → ЯКЩО культура не росте в новому сезоні and not теплиця/острів → ТО `transform(crop, dead_crop)`.
- КОЛИ `input(harvest, crop)` → ЯКЩО `state(crop, mature)` → ТО `give(player, produce × quality)`; regrow-культура → `set_state(crop, stage_regrow)`, інакше `disappear_b`.
- Якість: `custom: «roll(gold) залежить від farming level і добрива; silver — ~2× шанс gold; iridium — лише з Deluxe-добривом»` (?).
- КОЛИ `day_start` → ЯКЩО `custom: «3×3 дорослих однієї гігантської культури»` and `prob(1%)` (?) → ТО `merge(9 crops → giant_crop)`.
- КОЛИ `day_start` → ЯКЩО `count(crops, >=, 16)` (?) and `not in_range(crop, scarecrow, 8)` → ТО `rng(p)` → `disappear(crop)` (ворона).
- КОЛИ `contact(player, trellis_crop)` → ТО `block`.
- КОЛИ `input(use_tool_charged, level)` → ТО область дії: базова 1 клітина; мідна — лінія 3; сталь — лінія 5; золота — 3×3; іридієва — 6×3 (?); енергія `×` кількість клітин (?).
- КОЛИ `counter(energy, <=, 0)` → ТО `set_state(player, exhausted)` (повільніший рух, ранок з меншою енергією); енергія відновлюється сном і їжею.
- КОЛИ `custom: «годинник = 2:00»` → ТО `custom: «фермер непритомніє, втрачає гроші, ранок удома»`.
- КОЛИ `day_start` → ТО продаж скрині: `currency(+sum(price × quality_mult))`.
- Перемоги/поразки нема; «рахунок» — гроші, оцінка діда на початку 3-го року (?), рівень фермерства.

## Керування і ввід
- WASD — рух (8 напрямків); ЛКМ / C — використати інструмент у клітину перед собою (на ПК — у клітину під курсором у межах досягу); ПКМ / X — взаємодія (посадити, зібрати, поставити).
- Утримання інструмента — заряд (мідна+): область росте, енергія витрачається більше.
- Колесо/цифри — вибір слоту quickbar; підсвітка клітини-цілі під курсором (`hover-tile-highlight`) і привид розміщуваного обʼєкта з покриттям (спринклер показує клітини поливу (?)).
- Геймпад: автонаведення на клітину попереду.

## Вікна, меню, HUD
- `game-screen`: поле; HUD — `clock-calendar` (день тижня, дата, час, погода, сезон), `coins`, `energy-bar` (і здоровʼя в шахтах), `inventory-bar` (12 слотів, активний виділений), сповіщення-тости.
- `inventory-window` (E/Esc) з вкладками: інвентар, навички, стосунки, мапа (`map-window`), крафт, колекції, налаштування, вихід.
- `shop-window`: крамниця Пʼєра (насіння сезону, добрива), кузня Клінта (апгрейд інструментів — 2 дні без інструмента).
- `end-of-day-shipping` (custom-window): підсумок проданого по категоріях з сумою.
- Level-up екран навички з вибором професії на 5/10 рівні (`upgrade-window`).
- `main-menu`: New, Load, Co-op, Exit; `character-select` (персонаж + вибір мапи ферми); `save-slots`.
- Переходи: сон у ліжку → end-of-day-shipping → level-up (якщо є) → збереження → новий день.

## Фічі поза полем
- `autosave` — лише в момент сну (між днями); `save-slots`.
- `mode-coop`/`online-multiplayer` до 4 (8 на ПК (?)) фермерів на одній мапі.
- Прогресія: апгрейди інструментів (область дії), навички (менша витрата енергії), рецепти крафту спринклерів/добрив за рівнями, теплиця (без сезонів).
- Вибір мапи ферми — `custom-difficulty` у широкому сенсі; моди (SMAPI) — `mod-support` неофіційно.
- Нема undo, паузи часу в мультиплеєрі (у синглі — меню паузить годинник).

## Варіації й родичі
- Harvest Moon / Story of Seasons (першоджерело: щоденний полив і сезони), Rune Factory, Sun Haven, Coral Island, Minecraft-ферми (ріст за випадковими тіками, вода в радіусі 4).
- Осі «полив»: вручну щодня / спринклер / вода поруч (Minecraft) / не потрібен.
- Осі «покриття»: хрест / квадрат / коло-радіус (опудало) / ромб; апгрейд форми.
- Осі «смерть культури»: зміна сезону / нестача води / шкідники / ніколи.
- Родичі в корпусі: Factorio-стовпи (покриття), Townscaper/Dorfromantik (розміщення на сітці без часу).

## Цікавинки для курсу
- Клітина ґрунту як автомат станів (трава → зорано → посаджено → стадії → дозріло; полито скидається щоночі) — 📎.
- Денний тік із порядком фаз (спринклери → ріст → висихання → ворони → гігантські культури) — 🥉 (порядок обробки визначає результат).
- Форми покриття спринклерів і апгрейд nozzle (+1 кільце) як таблиця шаблонів — 🌱; оптимальне покриття ферми мінімумом спринклерів — 🥈.
- Опудало з радіусом і випадкові ворони — 📎 (зона захисту + `rng`).
- Інструмент із зарядом: область 1 → 3 → 5 → 3×3 → 6×3 у напрямку погляду, енергія за клітину — 🥉.
- Злиття 3×3 у гігантську культуру — 📎 (пошук квадрата шаблону).
- Сезонна загибель і regrow-культури — 🌱.

## Мапа на каталог
- Є: `move-8dir` · `impassable-cells` (каміння, шпалери, будівлі) · `floor-types` (трава/ґрунт/вода/підлога) · `cell-transform` (оранка, загибель культури) · `multi-cell-size` (будівлі, гігантська культура 3×3) · `inventory` + `inventory-items` + `inventory-limit` · `item-pickup` · `round-currency` · `shop-catalog` + `shop-window` · `save-game` + `save-autosave` · `game-pause` · `cell-click` + `hover-highlight` · `event-points` (ціни продажу).
- **Нема** → пропозиції карток:
  - `+day-tick` «Денний тік із фазами» · game-logic · 🥉 — оновлення світу раз на добу у визначеному порядку.
  - `+growth-stages` «Стадії росту за днями» · entities/state · 📎 · слоти {stages, days, regrow}.
  - `+season-kill` «Зміна сезону вбиває» · game-logic · 🌱.
  - `+coverage-area` «Зона покриття навколо сутності» · entities/state · 📎 · слоти {shape: cross|square|circle, radius} — спільне з Factorio-стовпами.
  - `+tool-area-charge` «Інструмент із зарядом області» · interface/input · 🥉 · слот {levels}.
  - `+energy-cost` «Енергія за дію» · entities/state · 🌱 — витрата на кожну дію, відновлення сном.
  - `+quality-roll` «Якість результату» · game-logic/economy · 📎 — шанс срібла/золота/іридію.
  - `+fertilizer-layer` «Шар модифікатора клітини» · entities/state · 📎 — добриво/утримувач як властивість ґрунту.
  - `+crow-raid` «Шкідник поза зоною захисту» · entities/spawn · 📎.

## Пропозиції до словників
- `+trigger:day_start` — світовий тік раз на добу (сон); `+trigger:season_change` — кожні 28 днів.
- `+trigger:rng`, `+trigger:input`; `+cond:state`, `+cond:in_range`, `+cond:cell`, `+cond:prob` — уживані ⏳.
- `+effect:set_cell` (оранка), `+effect:set_state` (полито), `+effect:transform` (мертва культура), `+effect:give`/`+effect:take`, `+effect:counter` (енергія).
- `+role:terrain` (ґрунт), `+role:resource` (врожай), `+role:zone` (зона опудала/спринклера).
- `+ui:energy-bar`, `+ui:coins`, `+ui:inventory-bar`; нові `+ui:hover-tile-highlight` (рамка клітини-цілі інструмента) і `+ui:clock-calendar` (час + дата + сезон + погода).
- `+feature:autosave` (лише між днями), `+feature:mode-coop`.
- `+window:inventory-window`, `+window:shop-window`; новий `+window:end-of-day-shipping` — підсумок дня (продане, прибуток).
- `+card:coverage-area`, `+card:growth-stages` — див. вище.

## Джерела
- ⭐ [Stardew Valley Wiki: Sprinkler](https://stardewvalleywiki.com/Sprinkler) — схеми покриття всіх спринклерів і nozzle (офіційна вікі; фетчеру 403, лінк з черги куратора).
- [Stardew Valley Wiki: Crops](https://stardewvalleywiki.com/Crops) — стадії, сезони, якість, гігантські культури, добрива.
- [Stardew Valley Wiki: Scarecrow](https://stardewvalleywiki.com/Scarecrow) — радіус і ворони.
- [Wikipedia](https://en.wikipedia.org/wiki/Stardew_Valley) — 4 сезони по 28 днів, щоденний полив, енергія відновлюється сном і їжею.
- Steam: пошук «stardew valley».
- YouTube: пошук «stardew valley sprinkler layout guide».

## Непевне
- Вікі Stardew віддала 403, WebSearch вичерпано — більшість чисел з власних знань.
- (?) Енергія 270; Retaining Soil 33/66/100%; nozzle-форми 3×3/5×5/7×7; радіус опудал 8/16; поріг ворон 16 культур; шанс гігантської 1%; область іридієвої лійки/мотики 6×3; швидкість годинника.
- (?) Розмір стандартної ферми й список мап (Meadowlands — 1.6).
- (?) Формула якості (farming level + добриво) — лише якісно.
- (?) Чи зораний ґрунт без культури зникає вночі з шансом — так у 1.x, точний шанс невідомий.
