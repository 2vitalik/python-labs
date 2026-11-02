---
title: Conway's Game of Life (Гра «Життя»)
slug: game-of-life
family: build-sim
also: [pencil-logic]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 1970
platforms: [web, PC, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life", note: "правило, патерни, історія, алгоритми"}
  - {kind: play, url: "https://copy.sh/life/", best: true, note: "грати в браузері: малювання, step/run/rewind, бібліотека, імпорт RLE, правило-рядок"}
  - {kind: official, url: "https://golly.sourceforge.io/", note: "Golly — еталонний симулятор: HashLife, RLE/macrocell, Generations, скрипти"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Life-like_cellular_automaton", note: "таблиця правил B/S: Seeds, HighLife, Day & Night…"}
  - {kind: fandom, url: "https://conwaylife.com/wiki/Run_Length_Encoded", note: "LifeWiki: формат RLE (сторінка віддала 403 фетчеру)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=conway+game+of+life+patterns", note: "пошук; патерни й гармати"}
stage: v1
coverage: 75
mechanics: [cell-click, hover-highlight, game-loop, game-pause, state-as-data, level-from-txt, import-open-formats, map-validation, level-metadata, in-game-editor, editor-palette, editor-draw-tools, editor-erase, field-scaling, game-settings, field-size-picker, console-render, gui-render, logic-render-split, +cellular-automaton-rule, +rule-string, +toroidal-wrap, +step-run-speed, +pattern-library, +rewind-history]
proposes: ["+cond:adjacent_count", "+effect:set_cell", "+effect:wrap", "+trigger:tick", "+role:mark", "+ui:step-button", "+ui:speed-slider", "+ui:generation-counter", "+ui:population-counter", "+ui:rule-input", "+window:pattern-library", "+feature:step-mode", "+feature:speed-control", "+feature:rewind", "+feature:custom-rules", "+axis:time=programmed", "+card:cellular-automaton-rule"]
author: opus
date: 2026-11-02
---

# Гра «Життя» — нуль гравців: намалюй початковий стан і дивись, як правило B3/S23 його розвиває

## Суть
Клітинний автомат Конвея: кожна клітина жива або мертва, усі одночасно оновлюються за правилом «народження при 3 сусідах, виживання при 2–3». Гравець не грає в звичному сенсі — він малює початкову конфігурацію (або бере з бібліотеки), запускає, зупиняє, крокує, редагує. Ядро — одне правило на 8 сусідів, з якого виростають стабільні фігури, осцилятори, кораблі, гармати й навіть універсальні компʼютери. Як «іграшка» — це редактор + симулятор + бібліотека патернів; клас `cursor` (рука малює клітини), час `programmed` (стан задано, далі — автомат).

## Поле і час
- Квадратна сітка, двостанова клітина (live/dead). Сусідство Мура — 8 клітин (ортогональні + діагональні).
- Поле в теорії нескінченне; реалізації: **обмежене** (за межею — мертві, патерни «бʼються» об край), **тор** (протилежні краї склеєні — найчастіше в навчальних версіях), **нескінченне** (розріджене зберігання живих клітин / HashLife у Golly). Golly додатково — пляшка Клейна, сфера (?).
- Тік = **покоління**: новий стан рахується з повного старого (подвійна буферизація; оновлення «на місці» — класична помилка студента).
- Темп задає гравець: пауза, крок на 1, запуск із fps-лімітом, «суперкрок» на 2ⁿ поколінь (copy.sh/life, HashLife), rewind.
- Камера: зум від окремих клітин до мільйонів, пан мишею/стрілками.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Жива клітина | tile | стан 1 | виживає при 2–3 живих сусідах, інакше вмирає |
| Мертва клітина | terrain | стан 0 | народжується при рівно 3 живих сусідах |
| Натюрморт (block, beehive, loaf, boat, tub) | object | період 1 | не змінюється між поколіннями |
| Осцилятор (blinker, toad, beacon — p2; pulsar — p3) | object | період p | повертається у свій стан через p поколінь |
| Корабель (glider, LWSS, MWSS, HWSS) | object | швидкість, напрям | через період зʼявляється зсунутим (глайдер — по діагоналі) |
| Гармата (Gosper glider gun) | spawner | період 30 | породжує глайдер кожні 30 поколінь (перший — на 15-му) |
| Матусалем (R-pentomino, Acorn) | object | час стабілізації | малий патерн, що розвивається тисячі поколінь (R — 1103, Acorn — 5206) |
| Межа поля | static | dead / wrap | за краєм — мертві клітини або протилежний край |

Патерни — не окремі сутності для двіжка, а **емерджентні** групи клітин; у таблиці вони, бо саме їх людина «бачить» і ставить з бібліотеки.

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → для кожної клітини рахується `n = adjacent_count(cell, live, 8)` по **старому** стану; усі зміни застосовуються разом.
- КОЛИ `tick` → ЯКЩО `cell(x, dead)` and `adjacent_count(x, live, ==, 3)` → ТО `set_cell(x, live)` (народження, B3).
- КОЛИ `tick` → ЯКЩО `cell(x, live)` and `adjacent_count(x, live, in, {2,3})` → ТО лишається (виживання, S23).
- КОЛИ `tick` → ЯКЩО `cell(x, live)` and `adjacent_count(x, live, <, 2)` → ТО `set_cell(x, dead)` (самотність); `> 3` → `set_cell(x, dead)` (перенаселення).
- КОЛИ `edge(neighbour)` → ЯКЩО `mode(torus)` → ТО `wrap` (сусід береться з протилежного краю); `mode(bounded)` → сусід вважається мертвим.
- КОЛИ `input(click, cell)` → ТО `set_cell(cell, toggle)` (лише в паузі або «на льоту» — залежить від реалізації).
- КОЛИ `input(paste, pattern)` → ТО `custom: «вставити патерн з бібліотеки/буфера у позицію курсора, з поворотом/віддзеркаленням»`.
- Правило-рядок `B{цифри}/S{цифри}` задає таблицю 2×9: для стану (dead/live) і числа сусідів 0–8 — новий стан. Варіанти: HighLife `B36/S23` (реплікатор), Seeds `B2/S` (кожна жива вмирає одразу — вибухове зростання), Day & Night `B3678/S34678` (симетричне до інверсії), Life without Death `B3/S012345678`, Replicator `B1357/S1357`, 2x2 `B36/S125`, Diamoeba `B35678/S5678`.
- Brian's Brain (Generations, `B2/S/3`): три стани — live → dying → dead; народження при 2 живих сусідах, жива завжди переходить у dying (`custom: «багатостановий цикл»`).
- КОЛИ `tick` → ЯКЩО `custom: «стан повторився»` → ТО можна визначити період (стабілізація/осцилятор) — опційна фіча, не правило гри.
- Перемоги/поразки/рахунку **нема** (zero-player); «цілі» задає людина: знайти патерн, побудувати гармату, дожити до N поколінь. Лічильники — покоління й популяція.

## Керування і ввід
- Миша: клік/drag — малювати або стирати клітини (copy.sh/life: права кнопка — створити/видалити, ліва drag — пан; колесо — зум).
- Клавіші (copy.sh/life): Space — крок, Enter — run/pause, Tab — багато поколінь, Backspace — rewind, `[`/`]` — повільніше/швидше, стрілки або HJKL — пан.
- Вставка патерна з бібліотеки, імпорт файла/посилання (RLE, Life 1.06, Plaintext), експорт.
- Randomize: випадкове заповнення прямокутника з густиною (параметри width/height/density).
- Golly: виділення прямокутником, copy/paste/rotate/flip, скрипти Lua/Python.

## Вікна, меню, HUD
- `game-screen`: поле з `zoom-control`, `grid-lines` (зникають на дрібному зумі), панель кнопок: Run/Pause, `step-button`, Superstep, Rewind, `speed-slider` (««/»»), Clear, Randomize.
- HUD: `generation-counter` (номер покоління), `population-counter` (живих клітин), `cell-coordinates` під курсором, назва поточного патерна (клік — опис).
- `pattern-library` (custom-window): список/дерево патернів за категоріями (still lifes, oscillators, spaceships, guns, methuselahs), опис і автор.
- `settings-window`: `rule-input` (рядок правила + пресети Conway/HighLife/2x2/Replicator), max fps, крок як степінь 2, товщина сітки.
- Import/Export (custom-window): текстове поле RLE / вибір файла / URL.
- `help-window` (About): клавіші й миша.
- Переходи: game-screen ↔ pattern-library (вибір → вставка на поле) · game-screen ↔ settings (зміна правила — поле лишається) · import → game-screen з новим полем.

## Фічі поза полем
- `level-editor` фактично = гра: малювання, гумка, прямокутне виділення, paste з поворотом.
- `export-import`: **RLE** — стандарт спільноти: заголовок `x = 3, y = 3, rule = B3/S23`, далі рядки з `b` (мертва), `o` (жива), `$` (кінець рядка), `!` (кінець), число перед символом — повтор; коментарі `#N` (назва), `#O` (автор), `#C` (опис). Глайдер: `bo$2bo$3o!`. Також Plaintext (`.`/`O`), Life 1.06 (координати живих), macrocell (Golly, квадродерево).
- `speed-control` + `step-mode` + `rewind` (історія поколінь), «суперкрок» (2ⁿ поколінь за раз — HashLife).
- `custom-rules` — рядок правила як налаштування; `custom-difficulty` ~ розмір/топологія поля.
- `puzzle-bank` ~ бібліотека патернів; `seed-input` ~ Randomize із заданою густиною (сид зазвичай не показують).
- Нема збережень прогресу, рахунку, рекордів — лише файли патернів.

## Варіації й родичі
- Life-like (2 стани, Мур-8): усі `B…/S…` — 2¹⁸ правил; вісь — **таблиця народження/виживання**.
- Generations (Brian's Brain, Star Wars): >2 станів із «затуханням»; Larger than Life — більший радіус сусідства; Wireworld — 4 стани для електроніки (окремий запис у черзі); Langton's Ant — один «агент» на клітинах (→ `program-robots`).
- Інші сітки: гексагональне Life, трикутне, 1D-автомати Вольфрама (Rule 30/110) — вісь **сусідство**: фон Нейман-4 / Мур-8 / гекс-6 / радіус r.
- Межа: обмежена / тор / нескінченна (розріджена множина, HashLife) — вісь **топологія**.
- Ігрові нащадки: Immigration/QuadLife (кольори-власники, народжена клітина бере колір більшості — основа для PvP-автомата), Advent of Code-задачі на автомати, Noita/falling-sand (→ `dig-gravity`).

## Цікавинки для курсу
- Крок B3/S23 з подвійним буфером і сусідами на торі — 🌱 (класика першої лаби; пастка — оновлення на місці).
- Рядок правила `B/S` як дані + пресети HighLife/Seeds/Day&Night — 📎 (парсер + таблиця 2×9).
- Парсер/експорт RLE з бібліотекою патернів — 🥉 (формат з повторами, коментарями, перевіркою розміру).
- Нескінченне поле через множину живих клітин + камера/зум — 🥉 (розріджене зберігання, межі вʼюпорта).
- Rewind/історія поколінь і детектор періоду (хеш стану → «осцилятор p=3», «стабілізувався») — 🥈.
- Generations (Brian's Brain) — багатостанові клітини — 📎 поверх базового.
- HashLife (квадродерево з мемоізацією, суперкрок 2ⁿ) — 👑 (дослідницький алгоритм).

## Мапа на каталог
- Є: `cell-click` + `hover-highlight` (малювання) · `game-loop` + `game-pause` (run/pause) · `state-as-data` (поле = множина клітин) · `level-from-txt` + `import-open-formats` (RLE/Plaintext) + `map-validation` (битий RLE) + `level-metadata` (`#N/#O/#C`) · `in-game-editor` + `editor-palette` + `editor-draw-tools` + `editor-erase` · `field-scaling` (зум) · `game-settings` + `field-size-picker` · `console-render`/`gui-render`/`logic-render-split` · `unit-tests` + `fixture-level-tests` (блінкер через 2 покоління = він сам).
- **Нема** → пропозиції карток:
  - `+cellular-automaton-rule` «Крок клітинного автомата» · game-logic · 🌱 · слоти {birth, survive, neighbourhood} — синхронне оновлення всіх клітин за кількістю сусідів.
  - `+rule-string` «Правило рядком B/S» · game-logic · 📎 · слот {presets} — парсер `B36/S23`.
  - `+toroidal-wrap` «Поле-тор» · levels · 🌱 — краї склеєні (також Snake, Pac-Man тунель).
  - `+step-run-speed` «Крок / запуск / швидкість» · interface/input · 🌱 — керування часом симуляції.
  - `+pattern-library` «Бібліотека патернів» · levels/bank · 📎 — вставка готових конфігурацій.
  - `+rewind-history` «Перемотка назад» · game-logic · 🥉 — історія станів (з `state-as-data`).

## Пропозиції до словників
- `+cond:adjacent_count` — ядро правила (рахує живих серед 8 сусідів); вжито як основна умова.
- `+effect:set_cell` — народження/смерть як зміна типу клітини; `+effect:wrap` — сусід через край тора.
- `+trigger:tick` — правило на кожне покоління без періоду.
- `+role:mark` — кандидат для «живої клітини» у статичному редакторі (у симуляції ближче `tile`).
- `+ui:step-button`, `+ui:speed-slider` (⏳ є) — уживані; нові `+ui:generation-counter` (номер покоління), `+ui:population-counter` (кількість живих), `+ui:rule-input` (поле рядка правила).
- `+window:pattern-library` — каталог готових конфігурацій для вставки (близько до `puzzle-select`, але без прогресу).
- `+feature:step-mode`, `+feature:speed-control`, `+feature:rewind`, `+feature:custom-rules` (⏳ є) — усі в ядрі іграшки.
- `+axis:time=programmed` — підтвердження значення ⏳: гравець задає початковий стан, далі автомат.
- `+card:cellular-automaton-rule` — див. «Мапа на каталог».

## Джерела
- ⭐ [copy.sh/life](https://copy.sh/life/) — найшвидший вхід: малюєш, запускаєш, вантажиш патерни, міняєш правило; HashLife у браузері.
- [Wikipedia: Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) — правило, натюрморти/осцилятори/кораблі, Gosper gun (p30), матусалеми, тор.
- [Wikipedia: Life-like cellular automaton](https://en.wikipedia.org/wiki/Life-like_cellular_automaton) — нотація B/S vs S/B (MCell), таблиця відомих правил, Brian's Brain як Generations.
- [Golly](https://golly.sourceforge.io/) — HashLife, Generations, Larger than Life, RuleLoader, RLE/macrocell, скрипти Lua/Python, обмежені й необмежені всесвіти.
- [LifeWiki: RLE](https://conwaylife.com/wiki/Run_Length_Encoded) — специфікація формату (фетчер отримав 403; опис формату з власних знань).
- YouTube: пошук «conway game of life patterns».

## Непевне
- (?) Формат RLE (`#N/#O/#C`, `b/o/$/!`, приклад глайдера) — з власних знань; LifeWiki недоступна фетчеру.
- (?) Топології Golly (тор, пляшка Клейна, сфера, хрест-кап) — сторінка Golly згадує лише bounded/unbounded.
- (?) Швидкість глайдера c/4 і LWSS c/2 — не підтверджено джерелом, тому в таблицю не вписано.
