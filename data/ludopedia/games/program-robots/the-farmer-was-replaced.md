---
title: The Farmer Was Replaced
slug: the-farmer-was-replaced
family: program-robots
also: [build-sim]
klass: avatar
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 2023
platforms: [PC, Mac (Steam)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/", note: "опис: Python-подібна мова, тех-дерево, .py-файли, IntelliSense, leaderboards"}
  - {kind: fandom, url: "https://thefarmerwasreplaced.wiki.gg/", best: true, note: "wiki.gg: усі культури, функції, вартість операцій, розблокування"}
  - {kind: fandom, url: "https://thefarmerwasreplaced.wiki.gg/wiki/Available_Functions", note: "повний API дрона"}
  - {kind: fandom, url: "https://thefarmerwasreplaced.wiki.gg/wiki/Execution_Details", note: "тіки, вартість операцій, енергія"}
  - {kind: fandom, url: "https://thefarmerwasreplaced.wiki.gg/wiki/Unlocks", note: "дерево розблокувань"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=the+farmer+was+replaced+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, impassable-cells, inventory-items, round-currency, in-round-upgrades, maze-generation, body-queue, collect-quota, save-progress, leaderboard, game-screen, +command-program, +sensor-predicates, +user-procedures, +tech-tree-unlock-language, +crop-growth-timer, +torus-wrap, +tick-cost-model, +adjacency-growth-penalty, +sort-by-swap, +giant-merge, +multi-drone-spawn, +code-editor-window, +external-editor-sync]
proposes: ["+trigger:exec(cmd)", "+trigger:grown(a)", "+cond:ground(cell, type)", "+cond:water(cell, op, x)", "+effect:wrap(a)", "+effect:set_state(a, infected)", "+effect:merge_region", "+effect:crash", "+role:resource", "+window:code-editor", "+window:research-tree", "+window:output-console", "+ui:instruction-highlight", "+feature:tech-tree", "+feature:simulation-run", "+feature:external-editor", "+axis:control"]
author: opus
date: 2026-11-02
---

# The Farmer Was Replaced — автоматизуй ферму, програмуючи дрон на Python-подібній мові

## Суть
Гравець не садить нічого руками: дрон на клітинній фермі робить лише те, що написано в коді (`move`, `plant`, `harvest`, `till`, `use_item`, `measure`, `swap`…). Урожай — валюта, за яку відкриваються нові культури, предмети, розмір ферми й **самі можливості мови** (змінні, цикли, функції, списки, словники, import). Кожна культура — окремий алгоритмічний пазл: дерева не можна садити поруч, кактуси треба відсортувати свопами, з куща виростає лабіринт зі скарбом, капелюх динозавра перетворює дрон на змійку. Рівнів нема — одна безперервна прогресія до «оптимальної ферми».

## Поле і час
- Квадратна ферма n×n (стартує з 1 клітини (?), розширюється розблокуванням Expand; `set_world_size()` тимчасово зменшує до ≥3). Поле — **тор**: `move` за край виводить з протилежного боку (крім режиму динозавра).
- Шари клітини: ґрунт (Grassland / Soil, рівень води 0–1) + сутність (рослина зі стадією росту, кущ, дерево, кактус з розміром, гарбуз, соняшник з пелюстками, лабіринтна огорожа, скарб, яблуко) + дрон(и) згори.
- Час `programmed`, але в реальному часі: базова операція = **тік 2,5 мс** (400 тіків/с); `harvest`/`plant`/`move` коштують ~200 тіків, `if`/`while` — 1 тік + умова, присвоєння й читання змінних — безкоштовні. Апгрейди Speed ділять тік на 1,5; енергія соняшників прискорює ×2.
- Рослини ростуть у реальному часі незалежно від коду (випадковий час у діапазоні); вода прискорює ріст до ×5.
- Видимість повна, але дрон «знає» лише те, що спитає функціями (`get_entity_type`, `measure`, `get_pos_x`…).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дрон | player | позиція, капелюх, швидкість | виконує код; одна дія за раз; з Megafarm — кілька дронів |
| Ґрунт Grassland | terrain | вода 0–1 | тут росте трава; `till()` → Soil |
| Ґрунт Soil | terrain | вода 0–1 | для моркви, гарбузів, соняшників, кактусів (?); `till()` → Grassland |
| Трава | resource | ріст 0,5 с | дає Hay |
| Кущ (bush) | resource | ріст 3,2–4,8 с | дає трохи Wood; основа для лабіринту |
| Дерево | resource | ріст 5,6–8,4 с; ×2 за кожне дерево-сусіда (4-сусідство) | дає 5 Wood; садити шахівницею |
| Морква | resource | ріст 4,8–7,2 с; посадка коштує Wood + Hay; лише Soil | дає Carrot |
| Гарбуз | resource | ріст 0,2–3,8 с; 20 % шанс згнити після дозрівання; коштує Carrot | повний квадрат дозрілих → гігантський гарбуз; врожай n×n×n до 5, далі n²·6 |
| Соняшник | resource | 7–15 пелюсток (`measure`) | дає Power; зрізати найбільший при ≥10 соняшниках → ×8 |
| Кактус | resource | розмір 0–9 (`measure`) | відсортовані сусіди збираються ланцюгом; n кактусів → n² |
| Огорожа лабіринту (hedge) | static | — | непрохідна; `move` повертає False |
| Скарб | pickup | позиція (`measure`) | `harvest` → Gold = площа лабіринту |
| Яблуко (режим динозавра) | pickup | позиція наступного — `measure()` | зʼїсти → хвіст +1 |
| Хвіст динозавра | object | довжина n | слідує за дроном; врізатись → `move` = False; зняти капелюх → n² Bones |
| Вода (бак) | — (предмет) | 0,25 води; +1 бак / 10 с | `use_item(Water)` підвищує рівень води клітини |
| Добриво | — (предмет) | +1 / 10 с | −2 с росту; рослина стає інфікованою |
| Weird Substance | — (предмет) | з половини врожаю інфікованих | перемикає інфекцію клітини й сусідів; на кущі — створює лабіринт |
| Компаньйон (Polyculture) | mark | бажана рослина й позиція в ≤3 кроках | `get_companion()`; посадити → бонус врожаю |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(move(dir))` → ЯКЩО `free(dir)` → ТО `move(drone, dir)`, на краю — `wrap(drone)`; інакше (огорожа, хвіст) повертає False, `block`.
- КОЛИ `exec(till())` → ТО `set_cell(here, Grassland ↔ Soil)`.
- КОЛИ `exec(plant(e))` → ЯКЩО `ground(here, потрібний)` і `has(drone, cost(e))` і клітина порожня → ТО `spawn_at(e, here)`, `take(cost)`; інакше повертає False.
- КОЛИ `exec(harvest())` → ЯКЩО `grown(here)` → ТО `pickup` урожаю; інакше рослина знищується без урожаю.
- КОЛИ `grown(pumpkin)` → ЯКЩО `prob(0.2)` → ТО `transform(dead_pumpkin)` (`can_harvest` завжди False; пересадити).
- КОЛИ `custom: «квадрат k×k повністю з дозрілих гарбузів»` → ТО `merge_region(giant_pumpkin)`.
- КОЛИ `exec(harvest())` на кактусі → ЯКЩО `custom: «N і E сусіди ≥, S і W сусіди ≤, усі дозрілі»` → ТО ланцюгова жатва по всіх відсортованих сусідах (flood fill), `score(n²)`.
- КОЛИ `exec(swap(dir))` → ТО `swap(here, neighbour)` — сутності двох клітин міняються місцями (сортування кактусів).
- КОЛИ `custom: «ріст дерева»` → ТО час × 2^(кількість дерев у 4-сусідстві).
- КОЛИ `exec(harvest())` на соняшнику → ЯКЩО `count(sunflower, >=, 10)` і пелюсток максимум → ТО Power ×8; інакше — звичайна кількість.
- КОЛИ `custom: «є Power»` → ТО `speed(drone, ×2)`; витрата 1 Power / 30 дій.
- КОЛИ `exec(use_item(Water))` → ТО вода клітини ↑; ріст ×(1 + 4·water); `timer` — випаровування ~1 % / с.
- КОЛИ `exec(use_item(Fertilizer))` → ТО ріст −2 с, `set_state(plant, infected)`; КОЛИ `harvest(infected)` → ТО ½ урожаю → Weird Substance.
- КОЛИ `exec(use_item(Weird_Substance, n))` → ЯКЩО `occupied(here, bush)` → ТО `custom: «кущ → лабіринт n×n зі скарбом у випадковому місці»`; на скарбі — переносить скарб і може прибрати частину стін (до 300 разів).
- КОЛИ `exec(harvest())` → ЯКЩО `occupied(here, treasure)` → ТО Gold = площа; на огорожі — лабіринт зникає.
- КОЛИ `exec(change_hat(Dinosaur_Hat))` → ТО режим змійки: `move` 400 тіків (−3 % за яблуко), без тору; КОЛИ `contact(drone, apple)` і `leave` → ТО `grow(tail, 1)`, нове яблуко у випадковій вільній клітині; КОЛИ інший капелюх → ТО хвіст збирається: n² Bones.
- КОЛИ `exec(spawn_drone(f))` → ЯКЩО `num_drones < max_drones` → ТО новий дрон у поточній клітині виконує функцію f паралельно; `wait_for(drone)` — дочекатися результату.
- КОЛИ `custom: «код використовує нерозблоковану конструкцію / помилка»` → ТО `crash` з повідомленням (?).
- Перемоги як такої нема: мета — розблокувати все (у т. ч. приховане `The_Farmers_Remains`), далі — leaderboard-забіги на час з чистого старту.

## Керування і ввід
- Ввід — **текст коду** у вікнах-редакторах гри: Python-підмножина (`def`, `while`, `for … in range`, `if/elif/else`, списки, словники, множини, кортежі, `import` з інших файлів) + вбудований API дрона; enum-и `North/East/South/West`, `Entities.*`, `Items.*`, `Grounds.*`, `Unlocks.*`, `Hats.*`.
- Кнопка запуску біля вікна коду; Stop; `set_execution_speed()` уповільнює для спостереження; `print()` малює «дим» над дроном, `quick_print()` — лише у вивід.
- Код зберігається в `.py`-файлах — можна редагувати у VS Code; File Watcher підхоплює зміни; IntelliSense працює зі стабами гри.
- Ручного керування дроном нема.

## Вікна, меню, HUD
- `main-menu`: Continue / New game / Settings / Leaderboard (?).
- `game-screen`: ферма (камера на поле) + довільна кількість **вікон коду** (`code-editor`: файл, номер рядка, підсвітка виконуваного рядка (?), кнопка ▶) + `output-console` (вивід `quick_print`) + `inventory-bar` (Hay, Wood, Carrot, Pumpkin, Power, Cactus, Gold, Bones, Water, Fertilizer, Weird Substance).
- `research-tree` — дерево розблокувань з цінами (Speed, Expand, Plant, Loops, Variables, Functions, Lists, Dictionaries, Senses, Operators, Watering, Trees, Carrots, Pumpkins, Sunflowers, Cactus, Mazes, Dinosaurs, Polyculture, Megafarm, Debug, Timing, Import, Simulation, Leaderboard, Hats…).
- `help-window`/`codex-window` — вбудована документація: опис кожної функції й культури, що відкривається разом з розблокуванням (?).
- `leaderboard` — Steam-таблиці забігів (`leaderboard_run`).
- `settings-window`: мова (11 мов), звук, File Watcher, шрифт редактора (?).
- `achievements-window` (Steam).
- Переходи: main-menu → game-screen; з game-screen модально — research-tree, docs, leaderboard; вікна коду відкриваються/закриваються на полі.

## Фічі поза полем
- `tech-tree` — головна прогресія: ресурси → розблокування мовних конструкцій і механік ферми (мова як прокачування).
- `simulation-run` — `simulate(...)`: тестовий прогін зі заданими ресурсами й seed у пісочниці, без витрат (Simulation unlock).
- `leaderboard-online` — забіги на час з чистого стану (`leaderboard_run`).
- `external-editor` — синхронізація .py з зовнішнім редактором.
- `autosave`, `cloud-save`, `achievements`, косметичні капелюхи (`unlockables`).
- Debug-розблокування: уповільнення й зменшення ферми для налагодження.

## Варіації й родичі
- Родичі: Screeps (JS, MMO-колонія), Bitburner (JS, хакінг), Factorio/Shapez (автоматизація без коду), Karel (мінімальний робот на сітці), farmbot-клони на itch.io.
- Осі варіацій: **як відкривається мова** (уся одразу / тех-деревом); **час** (покрокові тіки / реальний час з вартістю операцій); **кількість виконавців** (один дрон / spawn_drone); **ціль** (рівень-задача / безкінечна економіка / забіг на час).

## Цікавинки для курсу
- Модель вартості операцій у тіках (дія 200, `if` 1, присвоєння 0) як ціна часу програми — 🥈.
- Кактус: сортування свопами на 2D-сітці + ланцюгова жатва flood fill з n² — 🥇.
- Лабіринт з куща: генерація ідеального лабіринту, скарб за `measure()`, повторне використання з видаленням стін — 🥇 (генерація + розвʼязувач).
- Динозавр-змійка на дроні (хвіст, яблука, n² кісток) — 🥈.
- Дерева з подвоєнням росту за сусіда → шахівниця — 📎.
- Гігантський гарбуз: злиття повного квадрата дозрілих + 20 % гниття — 🥉.
- Мова, що розблоковується тех-деревом (цикли, функції, списки як апгрейди) — 👑 (власний інтерпретатор з вмиканням конструкцій).

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` (огорожа лабіринту) · `inventory-items` · `round-currency` (урожай як валюта) · `in-round-upgrades` (Speed, Expand) · `maze-generation` · `body-queue` (хвіст динозавра) · `collect-quota` (ціни розблокувань) · `save-progress` · `leaderboard` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+tech-tree-unlock-language` «Конструкції мови відкриваються прогресією» · game-logic/economy · 👑.
  - `+crop-growth-timer` «Рослина росте за випадковий час, вода прискорює» · entities/state · 📎 · слоти {min, max, water_mult}.
  - `+torus-wrap` «Поле-тор» · entities/move · 🌱.
  - `+tick-cost-model` «Кожна операція програми коштує тіки» · code/architecture · 🥈.
  - `+adjacency-growth-penalty` «Сусіди того ж виду сповільнюють ріст» · entities/state · 📎.
  - `+sort-by-swap` «Сортування сітки обмінами сусідів» · game-logic/constraints · 🥈.
  - `+giant-merge` «Повний квадрат дозрілих зливається в один обʼєкт» · entities/legality · 🥉.
  - `+multi-drone-spawn` «Запуск додаткових виконавців з функцією» · entities/spawn · 🥇.
  - `+command-program`, `+sensor-predicates`, `+user-procedures` — спільні для сімʼї.
  - `+code-editor-window` · interface/menus · 🥉; `+external-editor-sync` «Код у файлах, підхоплення змін» · code/architecture · 📎.

## Пропозиції до словників
- `+trigger:exec(cmd)` — спільний для сімʼї; `+trigger:grown(a)` — рослина дозріла (подія росту за таймером).
- `+cond:ground(cell, type)` — тип ґрунту; `+cond:water(cell, op, x)` — рівень води.
- `+effect:wrap(a)` вже ⏳ — тут для тора ферми; `+effect:set_state(a, infected)` — інфекція від добрива; `+effect:merge_region` — злиття області в один обʼєкт (гарбуз); `+effect:crash`.
- `+role:resource` — рослини як джерело ресурсу.
- `+window:code-editor`, `+window:research-tree` (тех-дерево), `+window:output-console` (вивід програми).
- `+ui:instruction-highlight`.
- `+feature:tech-tree`, `+feature:simulation-run` (прогін у пісочниці з seed), `+feature:external-editor`.
- `+axis:control` — `programmed` у реальному часі (не покроково, як у Karel).

## Джерела
- ⭐ [The Farmer Was Replaced Wiki (wiki.gg)](https://thefarmerwasreplaced.wiki.gg/) — культури, функції, вартість операцій, розблокування; окремі сторінки: [Cactus](https://thefarmerwasreplaced.wiki.gg/wiki/Cactus), [Mazes](https://thefarmerwasreplaced.wiki.gg/wiki/Mazes), [Dinosaurs](https://thefarmerwasreplaced.wiki.gg/wiki/Dinosaurs), [Pumpkins](https://thefarmerwasreplaced.wiki.gg/wiki/Pumpkins), [Trees](https://thefarmerwasreplaced.wiki.gg/wiki/Trees), [Sunflowers](https://thefarmerwasreplaced.wiki.gg/wiki/Sunflowers), [Polyculture](https://thefarmerwasreplaced.wiki.gg/wiki/Polyculture), [Watering](https://thefarmerwasreplaced.wiki.gg/wiki/Watering), [Fertilizer](https://thefarmerwasreplaced.wiki.gg/wiki/Fertilizer), [Plant Growth](https://thefarmerwasreplaced.wiki.gg/wiki/Plant_Growth).
- [Available Functions](https://thefarmerwasreplaced.wiki.gg/wiki/Available_Functions) — повний API дрона.
- [Execution Details](https://thefarmerwasreplaced.wiki.gg/wiki/Execution_Details) — тіки, вартість операцій, Power.
- [Unlocks](https://thefarmerwasreplaced.wiki.gg/wiki/Unlocks) — перелік розблокувань.
- [Steam](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/) — EA 10.02.2023, реліз 10.10.2025, Timon Herzog; .py-файли, IntelliSense, File Watcher.
- YouTube: пошук «the farmer was replaced gameplay».

## Непевне
- (?) Вигляд UI (кілька вікон коду, вікно виводу, підсвітка рядка, docs-вікно, головне меню) — з памʼяті; wiki й Steam не описують.
- (?) Стартовий розмір ферми і порядок дерева розблокувань — wiki дає лише алфавітний список.
- (?) Чи кактус потребує Soil; вартість ходу `move` у тіках (200 — з аналогії з harvest/plant; для динозавра wiki дає 400).
- (?) Колізії між кількома дронами і помилки виконання — не перевірено.
