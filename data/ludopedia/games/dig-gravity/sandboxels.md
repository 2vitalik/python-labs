---
title: Sandboxels
slug: sandboxels
aka: [Sandboxels Lite, "Sandboxels: Steam Edition", "Sandboxels: Discord Edition"]
family: dig-gravity
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: none
year: 2021
platforms: [web, Windows, macOS, Steam, Discord, mobile]
links:
  - {kind: wiki, url: "https://sandboxels.wiki.gg/wiki/Behavior", best: true, note: "сітка поведінки 3×3: коди M1/M2/DL/CR/CH/SW/EX… і модифікатори — серце двіжка"}
  - {kind: play, url: "https://sandboxels.r74n.com/", note: "грати в браузері"}
  - {kind: other, url: "https://sandboxels.r74n.com/controls", note: "офіційний довідник клавіш, кнопок і рядка статусу"}
  - {kind: wiki, url: "https://sandboxels.wiki.gg/wiki/Sandboxels", note: "огляд: 546 елементів (1.11.2), стани, редакції"}
  - {kind: wiki, url: "https://sandboxels.wiki.gg/wiki/Element", note: "категорії і таблиця елементів; 558 елементів, 231 прихований (1.12)"}
  - {kind: wiki, url: "https://sandboxels.wiki.gg/wiki/Modding_tutorial/Element_properties", note: "властивості елемента: tempHigh/stateHigh, density, burn, conduct, hardness/breakInto, tick"}
  - {kind: wiki, url: "https://sandboxels.wiki.gg/wiki/Temperature", note: "теплообмін дотиком, 20 °C за замовчуванням, Heat/Cool"}
  - {kind: wiki, url: "https://sandboxels.wiki.gg/wiki/Falling-sand_game", note: "жанр і місце Sandboxels у ньому"}
  - {kind: steam, url: "https://store.steampowered.com/app/3664820/Sandboxels/", note: "Steam Edition (лінк з вікі)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sandboxels+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [gravity-fall, cell-transform, interaction-table, chain-detonation, explode-area, game-pause, game-loop, state-as-data, in-game-editor, editor-palette, editor-draw-tools, editor-erase, save-game, save-multi-slot, level-exchange, theme-select, game-settings, keyboard-controls, cell-click, +falling-sand-cell, +density-displacement, +heat-diffusion, +phase-transition, +electric-signal, +behavior-grid-dsl, +reaction-table, +break-into, +view-modes, +frame-step, +tps-control, +replace-mode, +secondary-element, +hidden-elements, +mod-manager]
proposes: ["+cond:temp", "+cond:charged", "+effect:diffuse", "+effect:heat", "+effect:leave_behind", "+role:material", "+ui:stats-bar", "+window:element-info", "+window:mod-manager", "+feature:scripting", "+card:behavior-grid-dsl", "+card:reaction-table", "+card:hidden-elements"]
author: opus
date: 2026-11-09
---

# Sandboxels — falling sand на 500+ елементів, де поведінку елемента пишуть 3×3-сіткою правил

## Суть
Браузерна пісочниця R74n: гравець малює пікселі з понад 500 елементів (земля, рідини, гази, метали, їжа, живність, машини, зброя) і дивиться, як вони падають, течуть, нагріваються, плавляться, горять, проводять струм і реагують. Ядро незвичне для жанру: поведінка елемента описана **«сіткою поведінки»** — 3×3 масивом коротких кодів (`M1` — рухатись сюди першочергово, `DL` — видалити сусіда, `CH:x>y` — перетворити), тобто клітинний автомат записано як дані. Поверх сітки — властивості (температура переходів, густина, горючість, провідність, твердість) і таблиця реакцій «A + B → C + D».

## Поле і час
- Квадратна сітка пікселів на «чистому полотні»; один піксель — один елемент; розмір полотна — не перевірено (?).
- Кожен піксель має стан: елемент, температура (°C, за замовчуванням 20), електричний заряд, колір, «цілісність» (для ламання), поворот `r` для деяких.
- Real-time: тік симуляції; швидкість задається TPS (рядок статусу показує «30tps»), пауза й крок на один кадр.
- Межа полотна — елемент Border у категорії Special (?) щодо режимів краю.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Порошок / Land (Sand, Dirt, Clay, Ash…) | object | behavior POWDER, density | падає (`M1` знизу), інакше по діагоналі (`M2`); складається гіркою |
| Рідина (Water, Acid, Oil, Mercury, Honey…) | object | behavior LIQUID, density, viscosity | тече вниз і вбік; густіша тоне в легшій |
| Газ (Steam, Hydrogen, Oxygen, Methane, Smoke…) | object | density | розлітається в усі боки |
| Тверде (Iron, Gold, Glass, Ice, Steel…) | static | hardness, breakInto, tempHigh | нерухоме; плавиться, ламається від Smash |
| Стани (Molten Steel, Frozen Nitro, Liquid Helium…) | object | stateHigh / stateLow | варіанти іншого елемента за температурою |
| Life (Plant, Ant, Bee, Frog, Cell…) | neutral | tick-функція | рухаються, ростуть, їдять за власним кодом |
| Food (Bread, Cheese, Potato, Egg…) | object | reactions, tempHigh | готуються/горять від тепла, реагують |
| Energy (Fire, Electric, Laser, Lightning, Plasma) | hazard | burn, charge | гріють, підпалюють, заряджають |
| Weapons (TNT, Nuke, Grenade, Dynamite, Gunpowder) | hazard | `EX:r` | вибух радіусом r → `chain-detonation` |
| Machines (Wire, Battery, Heater, Pipe, Cloner) | conduit | conduct 0–1 | передають заряд; Cloner копіює торкнуте; Heater гріє |
| Special (Void, Sun, Ball, Balloon, Border) | static | — | Void видаляє (`DL` з чотирьох боків); Ball відскакує (`BO`) |
| Wall | static | лише `XX` | нічого не робить |
| Приховані елементи | object | 231 з 558 | не показані в меню за замовчуванням; доступні через пошук E (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
Сітка поведінки — 3 рядки по 3 коди; центр — сам піксель, вісім довкола — сусіди:
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `move(a, below)` — код `M1` (перший пріоритет).
- КОЛИ `tick` → ЯКЩО `custom: «M1 зайнятий»` and `free(below_diag)` → ТО `move(a, diag)` — `M2`, одна з кількох позицій навмання.
- КОЛИ `tick` → ЯКЩО `custom: «усі SP-позиції зайняті» / «будь-яка SA-позиція зайнята»` → ТО `block` — опора (`SP` / `SA`; `ST` — не липне до свого).
- КОЛИ `tick` → ЯКЩО `occupied(pos, kind)` → ТО `disappear_b` — `DL[:kind]`; `DB` — `disappear_both`.
- КОЛИ `tick` → ЯКЩО `free(pos)` → ТО `clone(a)` — `CL`; `CF` — копіює перший торкнутий (порядок: верх, ліво, право, низ); `CR:x` — `spawn_at(x, pos)`.
- КОЛИ `tick` → ЯКЩО `occupied(pos, x)` → ТО `transform(x → y)` — `CH:x>y`; `C2` — змінює себе після `M2`.
- КОЛИ `custom: «піксель зрушив»` → ТО `spawn_at(x, old_pos)` — `LB:x` (лишає слід), `L1`/`L2` — лише після `M1`/`M2`.
- КОЛИ `tick` → ЯКЩО `occupied(pos, x)` → ТО `swap(a, x)` — `SW:x` (напр. порошок проходить крізь дерево).
- КОЛИ `tick` → ТО `custom: «HT:n / CO:n — нагріти / охолодити сусіда на n °C»`; `CC:#hex` — `paint(pos, color)`; `SH` — `custom: «зарядити сусіда за його conduct»`.
- КОЛИ `blocked(a)` → ТО `bounce(a)` — `BO`; `FX`/`FY` — віддзеркалення, `RT` — `rotate(a)`.
- КОЛИ `occupied(pos, any)` → ТО `explode(r)` — `EX:r` (без радіуса гра падає в чорний екран).
- Модифікатори: `%n` — `prob(n%)` на тік; `,` — список (випадковий вибір); `AND` — кілька кодів в одній клітині зліва направо.
- КОЛИ `contact(a, b)` → ЯКЩО `custom: «реакція a+b в таблиці; умови — шанс, температура, висота»` → ТО `transform(a → c)`, `transform(b → d)` або `disappear_*`: Dirt + Water → Mud; Mud + Sawdust → Mulch; Hydrogen + Oxygen при високій температурі → Water.
- КОЛИ `tick` → ТО `custom: «теплообмін із сусідами дотиком»`.
- КОЛИ `custom: «temp ≥ tempHigh»` → ТО `transform(stateHigh)`; КОЛИ `custom: «temp ≤ tempLow»` → ТО `transform(stateLow)`: Ice > 5 °C → Water.
- КОЛИ `custom: «горить довше за burnTime»` → ТО `transform(burnInto)`; горючість — `burn`.
- КОЛИ `input(smash)` → ЯКЩО `custom: «не спрацював шанс hardness»` → ТО `transform(breakInto)`.
- КОЛИ `occupied(below, b)` → ЯКЩО `custom: «density(a) > density(b)»` → ТО `swap(a, b)` (?) — точне правило витіснення не відкрито.
- КОЛИ `input(draw)` → ТО `spawn_at(element, brush)`; права кнопка — `set_cell(cell, empty)`; режим Replace — малює поверх наявних.
- Елемент може мати і `behavior`, і `tick`-функцію JS: двіжок зливає їх у `tick1` → перевірка, чи змінився елемент → `tick2`.
- Перемоги, поразки, рахунку нема.

## Керування і ввід
- Миша: ліва — малювати, права — стерти, середня — піпетка (Shift — з властивостями), Shift+клік — лінія, колесо — розмір курсора.
- Пауза — Space/P/K/`; крок — `>`; швидкість TPS — T; розмір — `+`/`-` або `[`/`]` (Shift+`-` → 1, Shift+`+` → +15).
- Інструменти (категорія Tools): Erase, Drag, Pick, Heat, Cool, Paint, Mix, Shock, Smash — змінюють властивості пікселів під курсором; Shift + Heat/Cool/Drag/Mix/Shock/Smash — посилений ефект.
- Категорії — ←/→; вибір за назвою — E; інфо про елемент — I або `/`; другий елемент — Z; попередній — Backspace; Replace — `;`.
- Сейви: L — список, Ctrl+S — зберегти з назвою, Ctrl+Shift+S — миттєво, Ctrl+O — завантажити, Ctrl+Shift+O — перезавантажити останній; Ctrl+V / drag & drop — вставити файл.
- Вигляд: 1/0 — звичайний, 2 — термо, 3 — без ефектів, 4 — «шлейф», 5 — контури; H — сховати полотно; F1 — GUI; C/F2 — скриншот; F/F11 — fullscreen.
- R — очистити полотно; M — менеджер модів; `\` — налаштування; Esc — закрити меню.
- Мобільний: кнопка ↑ — Shift.

## Вікна, меню, HUD
- `game-screen`: полотно + кнопки Pause, `>`, −/+, Reset, Replace, Elem, Edit, Info, Saves, Mods, Settings + `element-picker` з категоріями (Land, Liquids, Gases, Powders, Solids, Life, Food, Machines, Energy, Weapons, Special, States, Tools).
- Рядок статусу: координати x,y · Pxls · TPS · загальна кількість тіків · [↑]/[A] (Shift/Alt) · ELEM під курсором · Temp · заряд C.
- `element-info` (I) — сторінка елемента.
- `save-slots` (L) — збереження й завантаження; експорт/імпорт файла.
- `mod-manager` (M) — підключення модів.
- `settings-window` (`\`) — серед іншого одиниці температури: °C / °F / K.
- Edit — режим з інструментами Ruler, Select (?) щодо складу.
- Переходи: game-screen ↔ кожне вікно; Esc закриває.

## Фічі поза полем
- `mode-sandbox` — уся гра.
- `pause`, `step-mode`, `speed-control` (TPS), `restart-level` (Reset), скриншот.
- `save-slots` + `export-import` + `level-sharing` — файли сейвів, з версії 1.9 — канал Discord для обміну.
- `mod-support`: JS-моди додають елементи, поведінки й реакції; менеджер модів.
- `custom-skins`-подібне: режими відображення (термо, шлейф, контури).
- Редакції: Lite, Discord Edition, Steam Edition, Demo; офлайн web-app на desktop і mobile.

## Варіації й родичі
- [the-powder-toy](the-powder-toy.md) — та сама ідея «елемент = властивості + переходи», плюс поле тиску; [sandspiel](sandspiel.md) — код на елемент і вітер; [sandspiel-studio](sandspiel-studio.md) — поведінка блоками від гравця.
- Powder Game, Hell of Sand, The Sandbox, sand:box, Noita.
- **Осі варіацій**: опис поведінки — «код на елемент / 3×3-шаблон кодів / блоки»; хімія — «лише CH у сітці / окрема таблиця реакцій з умовами»; стан пікселя — «лише вид / + температура / + заряд / + цілісність».

## Цікавинки для курсу
- Інтерпретатор сітки поведінки (3×3 рядків → дії `M1/M2/DL/CR/CH/SW`) — 🥈: DSL замість if-ів.
- Пріоритети руху M1 → M2 з випадковим вибором серед кількох позицій — 🌱.
- Таблиця реакцій «A + B → C + D» з умовами шансу й температури — 📎.
- Теплообмін і переходи tempHigh/tempLow (лід ↔ вода ↔ пара) — 🥉.
- Hardness/breakInto + інструмент Smash — 🌱.
- Режими відображення (звичайний, термо, контури) з того самого стану — 📎.
- Менеджер модів: завантаження JS, що додає елементи в реєстр — 🥈.

## Мапа на каталог
- Є: `gravity-fall` · `cell-transform` · `interaction-table` (реакції й сітки — дані) · `chain-detonation` + `explode-area` (`EX:r`) · `game-pause` · `game-loop` · `state-as-data` · `in-game-editor` + `editor-palette` + `editor-draw-tools` (лінія) + `editor-erase` · `save-game` + `save-multi-slot` · `level-exchange` · `theme-select` (режими вигляду) · `game-settings` · `keyboard-controls` · `cell-click` (клік/тап по полотну).
- **Нема** → пропозиції карток:
  - `+behavior-grid-dsl` «Поведінка елемента 3×3-сіткою кодів» · entities/interact · 🥈 · слоти {codes, modifiers %, AND, :}.
  - `+reaction-table` «Реакції пар елементів з умовами» · entities/interact · 📎 · слоти {elem1, elem2, chance, temp}.
  - `+break-into` «Ламання з шансом hardness у breakInto» · entities/state · 🌱.
  - `+hidden-elements` «Приховані елементи поза меню» · interface/menus · 🌱.
  - `+tps-control` «Швидкість симуляції в тіках/с» · interface/input · 🌱 · `+replace-mode` «Малювати поверх» · levels/editor · 🌱 · `+secondary-element` «Другий елемент на іншій кнопці» · levels/editor · 🌱 · `+mod-manager` «Менеджер модів» · levels/editor · 🥈.
  - Повтори TPT: `+falling-sand-cell`, `+density-displacement`, `+heat-diffusion`, `+phase-transition`, `+electric-signal`, `+view-modes`, `+frame-step`.

## Пропозиції до словників
- `+cond:temp(a, op, T)` — поріг температури (повтор TPT).
- `+cond:charged(a)` — піксель має заряд (умова реакцій і машин).
- `+effect:diffuse(field)` — розтікання значення по сусідах (повтор TPT).
- `+effect:heat(pos, ±n)` — змінити температуру сусіда (коди HT/CO, інструменти Heat/Cool).
- `+effect:leave_behind(x)` — при русі лишити x на старому місці (`LB`, `L1`, `L2`).
- `+role:material` — повтор.
- `+ui:stats-bar` — рядок статусу: координати, кількість пікселів, TPS, властивості під курсором.
- `+window:element-info` — сторінка властивостей елемента в грі (≈ `codex-window` для одного запису).
- `+window:mod-manager` — список модів з увімк./вимк.
- `+feature:scripting` — повтор TPT (тут JS-моди).
- `+card:behavior-grid-dsl` · `+card:reaction-table` · `+card:hidden-elements` — див. «Мапа на каталог».

## Джерела
- ⭐ [Sandboxels wiki: Behavior](https://sandboxels.wiki.gg/wiki/Behavior) — сітка 3×3, усі коди й модифікатори, приклад піску.
- [Controls Guide](https://sandboxels.r74n.com/controls) — миша, клавіші, кнопки, рядок статусу, режими вигляду.
- [Sandboxels wiki: Sandboxels](https://sandboxels.wiki.gg/wiki/Sandboxels) — 546 елементів, стани, реакції Dirt+Water, редакції, сейви й Discord.
- [Element](https://sandboxels.wiki.gg/wiki/Element) — 13 категорій з прикладами, 558/231 прихованих.
- [Element properties](https://sandboxels.wiki.gg/wiki/Modding_tutorial/Element_properties) — tempHigh/stateHigh, density, burn/burnTime/burnInto, conduct, viscosity, hardness/breakInto, злиття tick.
- [Temperature](https://sandboxels.wiki.gg/wiki/Temperature) — теплообмін дотиком, 20 °C, °F/K у налаштуваннях.
- [Falling-sand game](https://sandboxels.wiki.gg/wiki/Falling-sand_game) — рік 2021, платформи, «Behavior grid».

## Непевне
- (?) Точне правило витіснення за density і як працюють LIQUID/GAS-поведінки — сторінки не дають сіток.
- (?) Поля реакції (elem1, elem2, chance, tempMin…) — сторінка Reaction — заглушка, назви з памʼяті не пишу.
- (?) Розмір полотна, режими краю, склад режиму Edit (Ruler, Select) і як відкрити приховані елементи.
- (?) Кількість елементів міняється з версіями: 500+ / 546 (1.11.2) / 558 (1.12).
