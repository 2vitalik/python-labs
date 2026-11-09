---
title: Craftomation 101
slug: craftomation-101
aka: [Craftomation 101 Programming & Craft, Craftomation 1, CraftoMates]
family: program-robots
also: [build-sim]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: state
year: 2024
platforms: [PC, Mac, Linux, web, Chromebook]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1724140/Craftomation_101_Programming_Craft/", best: true, note: "опис: візуальне програмування, крафт, паливо й тепло, самовідтворення, seed планет; EA 19.02.2024, реліз 14.09.2026"}
  - {kind: official, url: "https://luden.io/craftomation/", note: "сторінка Luden.io: суть і всі платформи"}
  - {kind: itch, url: "https://ludenio.itch.io/craftomation101/", note: "безкоштовне браузерне демо; назви блоків Pick From, Find and Pick, Drop to, Move to, Check Power, To idle"}
  - {kind: other, url: "https://ludenio.substack.com/p/meet-craftomation-101", note: "девлог: крафт двох предметів у двох руках, рецепти Stone+Stone→Spark, вогонь тримає землю від замерзання, історія від Assembler-стека до нод"}
  - {kind: other, url: "https://steamcommunity.com/app/1724140/discussions/0/4345480979782089167", note: "форум: змінні, find, comparator, функції з input-змінними"}
  - {kind: play, url: "https://poki.com/en/g/craftomation-1", note: "грати в браузері (Poki)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=craftomation+101+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [command-program, user-procedures, sensor-predicates, inventory-limit, item-pickup, hunger-clock, seed-share, codex-window, tutorial-window, game-screen, save-progress, +swarm-separate-programs, +node-graph-program, +two-item-craft-recipe, +recipe-discovery, +fuel-heat-radius, +self-replicating-robots, +tech-tree-unlock, +ability-modules, +program-variables, +find-nearest-target, +procedural-planet]
proposes: ["+effect:craft(a, b → c)", "+effect:find_nearest(kind)", "+trigger:fuel_out(x)", "+cond:power(a, op, n)", "+window:node-editor", "+window:tech-tree", "+feature:recipe-discovery", "+feature:self-replication"]
author: opus
date: 2026-11-09
---

# Craftomation 101 — програмуєш нодами крихітних роботів, які крафтять, гріють і тераформують замерзлу планету, а згодом будують одне одного

## Суть
Гравець висаджується з ракетою й одним роботом-CraftoMate на крижану планету. Спочатку крафтиш руками: береш два предмети й зʼєднуєш їх у новий (Stone + Stone → Spark, Spark + Coal → Fire), відкриваючи рецепти. Далі програмуєш роботів візуальними блоками-нодами (`Move to`, `Pick From`, `Find and Pick`, `Drop to`, `Check Power`…), щоб вони носили, крафтили й підкидали паливо у вогнища, бо без тепла земля знову замерзає. Ціль — самодостатня колонія роботів, що сама себе відтворює і тераформує планету (кисень, вода, дерева). Клас `hybrid`: `cursor` (ручний крафт і розстановка) + програмовані виконавці.

## Поле і час
- Карта планети — клітини-тайли зі «шаховою» розміткою, щоб зручно вказувати в програмі місця; генерується процедурно (ресурси, будівлі, вулкани), seed можна передати іншому.
- Шари: ґрунт / сніг-лід (непрохідний для базового робота) / предмети на тайлах / будівлі / вогнища / роботи.
- Час `realtime`: роботи безперервно виконують свої програми паралельно; паливо вогнищ і енергія роботів витрачаються з часом.
- Зона тепла навколо вогнищ і ракети — «острів» розталої землі, що росте або зникає.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| CraftoMate (робот) | ally | енергія (power), дві руки (2 предмети), програма, модулі-апгрейди | виконує свою програму-граф нодів; без енергії зупиняється; їсть батарейки |
| Гравець-«рука» | — (cursor) | — | бере й комбінує предмети вручну, ставить будівлі, пише програми |
| Ракета | container | вантаж | на старті розтоплює лід навколо; завантажені елементи → повертається з новими модулями програмування (?) |
| Command Center | sink | — | доставка ресурсів дає очки апгрейдів для дерева технологій |
| Ресурс (Stone, Coal, Wood, Water…) | resource | тип | лежить на тайлі; береться в руку |
| Проміжний предмет (Spark, Fire, Steam, батарея…) | object | рецепт | результат крафту двох предметів |
| Вогнище (Bonfire) | source | паливо | гріє зону; паливо скінчилось → земля навколо замерзає |
| Сніг/лід | terrain | — | блокує рух; тане від тепла; модуль дозволяє ходити по снігу |
| Піч / будівля (oxygen, water, temperature) | static | вхід/вихід | перетворює ресурси; частина цілей тераформування |
| Дерево / ферма | resource | ріст (?) | висаджується, дає деревину (паливо) |
| Модуль покращення | pickup | здібність | «згодовується» роботу → нові команди/вміння |
| Новий CraftoMate (крафт) | spawner | рецепт | роботи можуть скрафтити робота — самовідтворення |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag a onto b)` → ЯКЩО `custom: «є рецепт a + b»` → ТО `custom: «craft: a і b зникають, зʼявляється c»` (рецепт відкрито).
- КОЛИ `exec(Move to)` → ЯКЩО `path_exists(robot, target)` → ТО `move(robot, target)`; інакше `custom: «робот застряє/чекає»` (?).
- КОЛИ `exec(Pick From)` → ЯКЩО `occupied(tile, item)` and `custom: «є вільна рука»` → ТО `pickup`.
- КОЛИ `exec(Find and Pick)` → ТО `custom: «знайти найближчий тайл з предметом виду і взяти»`.
- КОЛИ `exec(Drop to)` → ЯКЩО `has(robot, item)` → ТО `place(item, tile)` (у піч / вогнище / на тайл).
- КОЛИ `exec(Craft)` → ЯКЩО `custom: «в обох руках інгредієнти рецепта»` → ТО `custom: «craft(a, b → c)»`.
- КОЛИ `exec(Check Power)` → ТО `custom: «гілка за рівнем енергії»` (сенсор-умова).
- КОЛИ `counter(power, <=, 0)` → ТО `set_state(robot, stopped)` (?); КОЛИ `exec(eat battery)` → ТО `custom: «енергія поповнюється»`.
- КОЛИ `exec(To idle)` або `custom: «вихід з функції»` → ТО `set_state(robot, idle)`; цикл програми починається спочатку.
- КОЛИ `custom: «змінна set/assign»` → ТО `set_value(var, v)`; `custom: «comparator»` порівнює змінну зі значенням → розгалуження.
- КОЛИ `timer(every)` → ТО `counter(fuel, -1)` у кожному вогнищі.
- КОЛИ `counter(fuel, <=, 0)` → ТО `custom: «вогонь гасне, тайли зони замерзають знову»` (`set_cell(zone, snow)`).
- КОЛИ `place(fuel, bonfire)` → ТО `counter(fuel, +n)`.
- КОЛИ `custom: «тепло на тайлі зі снігом»` → ТО `set_cell(tile, ground)`.
- КОЛИ `custom: «модуль згодовано роботу»` → ТО `unlock(ability)`.
- КОЛИ `custom: «ресурс доставлено в Command Center»` → ТО `counter(upgrade_points, +n)` → `choose(tech)` у дереві технологій.
- КОЛИ `custom: «робот скрафтив робота»` → ТО `spawn_at(craftomate, tile)` з порожньою програмою (?).
- Перемога: планета тераформована (атмосфера, вода, дерева) · Поразка: явної нема — колонія завмирає без тепла й енергії (?) · Рахунок: нема.

## Керування і ввід
- Мишею/тачем: drag предмета на предмет — крафт; клік по тайлу — вибір місця для програми; розстановка будівель.
- Програма — **граф нодів**: блоки-команди зʼєднуються лініями сигналу; змінні (cyan) передають значення по зелених лініях усім підключеним блокам.
- Функції з input-змінними — одна функція для кількох цілей (напр. кілька печей); бібліотеки й власні ноди (з літа 2021).
- Ранній прототип мав «стек команд» у стилі Assembler — від нього відмовились заради гілок і циклів.

## Вікна, меню, HUD
- `game-screen`: карта планети з роботами й тайлами + `node-editor` (custom) поверх/збоку для обраного робота.
- `codex-window`: вбудована вікі рецептів.
- `tech-tree` (custom): дерево технологій за очками апгрейдів.
- HUD: індикатор енергії робота (`energy-bar`), паливо вогнищ (?), вибраний робот, `instruction-highlight` активного нода (?).
- `tutorial-window`: стартовий сценарій із замерзлою ракетою, яку треба розігріти.
- `main-menu` → нова планета (seed) / продовжити; `settings-window` (32 мови).

## Фічі поза полем
- `seed-input` / `share-code`: процедурні планети з seed для друзів.
- `meta-progression` у межах планети: дерево технологій, модулі.
- Окрема DLC-мапа «Mega Map of Self-Replicating Machines».
- `autosave` / `continue` (?).
- `localization` (32 мови), браузерна версія й Chromebook (рушій Defold).

## Варіації й родичі
- [autonauts](autonauts.md) — найближчий родич: боти вчаться за демонстрацією й блоками, колонія, крафт ланцюгами.
- [the-farmer-was-replaced](the-farmer-was-replaced.md) — один дрон, текстовий Python, ферма замість тераформування.
- Luden.io: *while True: learn()* (ноди для ML-конвеєра) — попередня гра студії; Little Alchemy — крафт «двох у новий».
- Осі варіацій: **мова** (текст / блоки-стек / граф нодів); **скільки виконавців** (один / колонія з окремими програмами); **ресурс життя** (енергія робота, паливо вогнищ, нічого); **самовідтворення** (нема / робот крафтить робота).

## Цікавинки для курсу
- Крафт «два предмети в руках → новий» з таблицею рецептів і відкриттям — 🌱.
- Вогнище з паливом і радіусом тепла: тайли тануть і замерзають знову — 📎.
- Граф нодів як програма: обхід графа виконання, змінні-сигнали по ребрах — 🥇.
- `Find and Pick` — пошук найближчого тайла з предметом (BFS на сітці) — 🥉.
- Колонія роботів з окремими програмами в real-time + конфлікти за предмет — 🥈.
- Самовідтворення: робот за програмою крафтить робота — 🥉.

## Мапа на каталог
- Є: `command-program` · `user-procedures` (функції) · `sensor-predicates` (`Check Power`, comparator) · `inventory-limit` (дві руки) · `item-pickup` · `hunger-clock` (енергія робота/паливо вогнища падає з часом) · `seed-share` · `codex-window` (вікі рецептів) · `tutorial-window` · `game-screen` · `save-progress`.
- **Нема** → пропозиції карток:
  - `+swarm-separate-programs` (вже пропоновано).
  - `+node-graph-program` «Програма як граф нодів зі звʼязками» · game-logic/program · 🥇.
  - `+two-item-craft-recipe` «Крафт двох предметів за таблицею рецептів» · entities/interact · 🌱.
  - `+recipe-discovery` «Рецепт відкривається при першому вдалому крафті» · levels/progression · 🌱.
  - `+fuel-heat-radius` «Джерело тепла з паливом тримає зону розталою» · entities/state · 📎.
  - `+self-replicating-robots` «Роботи будують роботів» · entities/spawn · 🥉.
  - `+tech-tree-unlock` «Дерево технологій за очки доставки» · levels/progression · 🥉.
  - `+ability-modules` «Модуль згодовується роботу — нова команда» · entities/state · 📎.
  - `+program-variables` «Змінні в програмі робота» · game-logic/program · 📎.
  - `+find-nearest-target` «Знайти найближчу клітину з предметом» · entities/move · 🥉.
  - `+procedural-planet` «Процедурна карта з ресурсами й будівлями» · levels/generation · 🥈.

## Пропозиції до словників
- `+effect:craft(a, b → c)` — два предмети в руках/на тайлі за рецептом дають новий (не `merge`: інгредієнти різні).
- `+effect:find_nearest(kind)` — обрати найближчу клітину з сутністю виду як ціль.
- `+trigger:fuel_out(x)` — у джерела скінчилось паливо (вогнище, генератор).
- `+cond:power(a, op, n)` — рівень енергії актора.
- `+window:node-editor` — редактор програми як графа нодів (варіант `code-editor`).
- `+window:tech-tree` — дерево технологій.
- `+feature:recipe-discovery`, `+feature:self-replication`.

## Джерела
- ⭐ [Steam: Craftomation 101](https://store.steampowered.com/app/1724140/Craftomation_101_Programming_Craft/) — повний опис: блоки, функції, змінні й масиви, CraftoMates крафтять роботів, паливо й тепло, кисень, дерева, процедурні планети з seed; EA 19.02.2024, реліз 14.09.2026. (ID у черзі, 1569750, — неправильний.)
- [Luden.io: Craftomation](https://luden.io/craftomation/) — суть, платформи (itch, Steam, GOG, Poki).
- [itch.io: Craftomation 101](https://ludenio.itch.io/craftomation101/) — демо; блоки Pick From / Find and Pick / Drop to / Move to / Check Power / To idle; батарейки як їжа; Command Center і дерево технологій.
- [Substack: Meet Craftomation 101](https://ludenio.substack.com/p/meet-craftomation-101) — дві руки й крафт двох предметів, рецепти, вогонь і замерзання, ракета з модулями, історія розробки (LD48, Defold, Assembler-стек → ноди).
- [Steam-форум: змінні](https://steamcommunity.com/app/1724140/discussions/0/4345480979782089167) — set variable, input-змінна функції, find, comparator, idle і перезапуск циклу.
- [Poki: Craftomation 1](https://poki.com/en/g/craftomation-1) — браузерна версія, drag-and-drop.

## Непевне
- (?) Поле: черга каже «гекс», девлог — «шахова» розмітка тайлів; ставлю `square`, не перевірено скриншотом.
- (?) Рік: браузерна альфа 2022, Steam EA 2024, повний реліз 2026; у шапці — 2024.
- (?) Що відбувається з роботом при нулі енергії та при недосяжній цілі `Move to`.
- (?) Ракета «повертається з модулями» в обмін на елементи — з девлогу 2022, міг змінитися механізм.
- (?) Умова перемоги — тераформування; чи є явний екран кінця й поразка — невідомо.
- (?) Конкретні тексти інших блоків (Craft, Eat, цикли, мітки) — форум згадує лише заплановані labels/loops/Feed.
