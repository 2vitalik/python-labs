---
title: Tricone Lab
slug: tricone-lab
aka: []
family: thinky
also: []
klass: cursor
axes:
  field: graph
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2017
platforms: [PC (Windows, macOS)]
links:
  - {kind: other, url: "https://www.gamespew.com/?p=7887", best: true, note: "огляд Early Access (2015): ціль — Tricone з червоного, зеленого й синього конуса, лінія від каталізатора, стінки, breaker, mover, replicator, anti-catalyst, constructor, редактор"}
  - {kind: steam, url: "https://store.steampowered.com/app/392610/Tricone_Lab/", note: "опис: клітини-камери, ламати стінки, каталізатори → сполуки з власною дією; 100 рівнів, undo/redo, редактор, режим для дальтоніків"}
  - {kind: other, url: "https://thegemsbok.com/art-reviews-and-articles/mid-week-mission-tricone-lab-partickhill-games", note: "стаття: лінія між каталізатором і елементом, анти-каталізатори, заряджені ділянки, «mobility markers», статистика рівнів"}
  - {kind: other, url: "https://steamcommunity.com/app/392610/reviews/?browsefilter=toprated&filterLanguage=english", note: "відгуки: 23 мапи по 3–5 рівнів, заряди ±, кнопка Describe, ламання стінки нейтралізує заряд"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2749451694", note: "Steam-гайд: відеопроходження всіх рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tricone+Lab+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [drag-drop-piece, path-drawing, destructible-blocks, connectivity-check, undo-redo, redo, restart-level, level-select, level-unlock, in-game-editor, editor-palette, editor-erase, editor-playtest, level-exchange, save-progress, +catalyst-recipe, +compartment-graph, +charge-zone-decompose, +anti-catalyst-grab, +mobility-markers, +cloner-element, +describe-button]
proposes: ["+card:catalyst-recipe", "+card:compartment-graph", "+card:charge-zone-decompose", "+card:anti-catalyst-grab", "+card:mobility-markers", "+ui:describe-button"]
author: opus
date: 2026-11-09
---

# Tricone Lab — синтез у живій клітині: зʼєднуй вузли з каталізаторами, ламай стінки камер, збери червоний + зелений + синій у Tricone

## Суть
Абстрактна «лабораторна» головоломка: рівень — мікроорганізм із камер, розділених стінками; у камерах плавають вузли-елементи. Гравець тягне лінії від каталізатора до потрібних вузлів у тій самій камері; коли рецепт каталізатора повний, вузли перетворюються на сполуку з власною дією (ламати стінки, переносити, клонувати, будувати стінку). Ціль — синтезувати Tricone з трьох конусів (червоний, зелений, синій) при каталізаторі Tricone. **Межа сімʼї:** поле не сітка клітин, а граф камер — описано коротко.

## Поле і час
- Поле — граф: вершини = камери (cells/compartments) неправильної форми, ребра = стінки між сусідніми камерами; вузли не мають координат, важить лише «у якій камері».
- Камери анімовано «дихають» і змінюють форму в реальному часі, але логіка покрокова: дія → наслідок; undo по одній дії, анімації не блокують ввід.
- Деякі камери мають заряд (+ / −).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Камера | zone | заряд: 0 / + / − | вміщує вузли; лінії не перетинають її стінок |
| Стінка | static | — | ділить камери; ламається breaker-ом; constructor будує нову |
| Конус R / G / B | resource | колір | інгредієнт Tricone |
| Каталізатор Tricone | spawner | рецепт R+G+B | з повним набором ліній дає Tricone |
| Каталізатор сполуки | spawner | рецепт (шаблон + модифікатор) | дає breaker / mover / replicator / constructor |
| Шаблон, модифікатор мобільності | resource | тип | інгредієнти сполук |
| Breaker | object | — | ламає стінку |
| Mover | object | — | переносить вузли крізь стінку |
| Replicator | object | — | клонує вузол (коли конусів бракує) |
| Constructor | object | — | ставить стінку (напр. замкнути анти-каталізатор) |
| Анти-каталізатор | enemy | — | хапає/тягне потрібні вузли (конуси, шаблони, модифікатори) |
| Tricone | pickup | — | продукт; ціль рівня — N штук |
| Ключ | pickup | — | колекційний предмет рівня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag line catalyst ↔ node)` → ЯКЩО `custom: «обидва в одній камері, лінія не перетинає стінку»` → ТО `attach(catalyst, node)`.
- КОЛИ `custom: «до каталізатора приєднано весь рецепт»` → ТО `merge(nodes, catalyst → compound)`.
- КОЛИ `custom: «рецепт Tricone: R + G + B»` → ТО `spawn(tricone)`, `counter(tricone, +1)`.
- КОЛИ `counter(tricone, >=, goal)` → ТО `win`.
- КОЛИ `input(activate breaker → wall)` → ТО `set_cell(wall, open)` — камери зливаються.
- КОЛИ `input(activate mover → node, wall)` → ТО `carry(mover, node)` у сусідню камеру.
- КОЛИ `input(activate replicator → node)` → ТО `clone(node)`.
- КОЛИ `input(activate constructor → edge)` → ТО `set_cell(edge, wall)` (?).
- КОЛИ `tick` → ЯКЩО `occupied(cell, anti_catalyst)` → ТО `pull(node)` — анти-каталізатор забирає потрібні вузли своєї камери (?).
- КОЛИ `enter(compound, negative_cell)` → ТО `split(compound)` — заряд розбирає великі одиниці (Tricone → конуси, які можна клонувати).
- КОЛИ `custom: «стінку зарядженої камери зламано»` → ТО `clear_state(cell, negative)` — заряд нейтралізовано.
- КОЛИ `input(move element)` → ЯКЩО `counter(mobility, >, 0)` → ТО `move(element, to)`, `counter(mobility, -1)` (?).
- КОЛИ `input(undo)` → ТО `undo(1)`; redo і рестарт — без ліміту.
- Перемога: синтезовано потрібні Tricone. · Поразка: нема (глухий кут → undo). · Рахунку нема, гра показує агреговану статистику рівня.

## Керування і ввід
- Миша: тягнути лінію з каталізатора або з вузла (обидва напрямки рівноцінні); клік — вибрати вузол, кнопка Describe — показати формулу вузла.
- Undo / Redo, рестарт; у редакторі — гарячі клавіші на всіх командах.

## Вікна, меню, HUD
- `level-select` / `map-window`: мапи (BewilderBlend, ConstructConfuse, Outcloned…) у вигляді сітки «іскристих дротів»; 23 мапи по 3–5 рівнів, пізні заблоковані до проходження попередніх.
- `game-screen`: організм з камерами, вузли, лінії; `undo-button`, `redo-button`, кнопка Describe.
- `editor-window`: малювати стінки мишею, ставити елементи кліком, режим видалення, плейтест; доступні всі елементи.
- `custom-window`: браузер мап спільноти (Workshop, модерація розробником).
- `stats-window`: агрегована статистика кожного рівня.
- `settings-window`: режим для дальтоніків.

## Фічі поза полем
- `levels-sequential` + `level-unlock` (нелінійно: мапа відкривається опануванням елемента), 4 демо-мапи як навчання.
- `undo` + `redo` без ліміту, `restart-level`.
- `level-editor` + `level-sharing` + `user-levels-browser` (Steam Workshop).
- `stats`, `colorblind-palette`, досягнення за кожен набір рівнів, колекційні ключі.

## Варіації й родичі
- Early Access грудень 2015 → реліз 27.07.2017; автор — Josh Singer / Partickhill Games (Глазго).
- Родичі: Opus Magnum / SpaceChem (рецепт → продукт, `program-robots`), `games/thinky/sokobond.md` (зʼєднання атомів), Divide by Sheep (обмежений ресурс у камерах).
- **Осі варіацій:** поле — сітка (SpaceChem) / граф камер (Tricone Lab); синтез — сусідство (Sokobond) / лінія до каталізатора; перешкоди — стінки / заряди / вороги-анти-каталізатори.

## Цікавинки для курсу
- Поле-граф камер зі злиттям вершин після зламаної стінки — 🥉 (union-find).
- Каталізатор із рецептом: перевірка «чи приєднано весь набір» → продукт — 📎.
- Заряджена камера, що розбирає сполуку на складники, — 📎.
- Редактор з плейтестом і обміном мапами — 🥈.

## Мапа на каталог
- Є: `drag-drop-piece` + `path-drawing` ↔ лінії; `destructible-blocks` ↔ стінки; `connectivity-check` ↔ «в одній камері»; `undo-redo` + `redo` + `restart-level`; `level-select` + `level-unlock`; `in-game-editor` + `editor-palette` + `editor-erase` + `editor-playtest` + `level-exchange`; `save-progress`.
- Уже пропонована: `+cloner-element` (Sandspiel).
- **Нема** → пропозиції карток:
  - `+catalyst-recipe` «Каталізатор + повний рецепт → сполука» · entities/interact · 📎.
  - `+compartment-graph` «Поле з камер, стінки — ребра» · entities/legality · 🥉.
  - `+charge-zone-decompose` «Заряджена зона розбирає сполуки» · entities/state · 📎.
  - `+anti-catalyst-grab` «Ворог забирає потрібні вузли» · entities/interact · 📎.
  - `+mobility-markers` «Ліміт переміщень на кожному елементі» · entities/legality · 🌱.
  - `+describe-button` «Показати формулу/рецепт вибраного елемента» · interface/hud · 🌱.

## Пропозиції до словників
- `+card:catalyst-recipe`, `+card:compartment-graph`, `+card:charge-zone-decompose`, `+card:anti-catalyst-grab`, `+card:mobility-markers` — механік нема в каталозі.
- `+ui:describe-button` — кнопка «що це і з чого складається» для вибраного вузла.

## Джерела
- ⭐ [GameSpew: огляд Early Access](https://www.gamespew.com/?p=7887) — ціль Tricone з трьох конусів, лінія від каталізатора, breaker = модифікатор мобільності + шаблон + каталізатор, mover, replicator, anti-catalyst і constructor, редактор і обмін мапами.
- [Steam: Tricone Lab](https://store.steampowered.com/app/392610/Tricone_Lab/) — 100 рівнів, навчальні рівні, undo/redo, редактор, нелінійна прогресія, режим для дальтоніків.
- [The Gemsbok](https://thegemsbok.com/art-reviews-and-articles/mid-week-mission-tricone-lab-partickhill-games) — лінія тягнеться з будь-якого кінця, анти-каталізатори, заряджені ділянки, «mobility markers», статистика, ключі, мапи.
- [Відгуки Steam](https://steamcommunity.com/app/392610/reviews/?browsefilter=toprated&filterLanguage=english) — 23 мапи × 3–5 рівнів, заряди ±, Describe, зламана стінка нейтралізує заряд, негативний заряд розбирає Tricone.

## Непевне
- (?) Як саме діють mobility markers, constructor і анти-каталізатор (за тік чи за хід) — описано лише словами оглядів.
- (?) Позитивний заряд — що робить; чи сполуки витрачаються після дії.
- (?) Межа сімʼї: поле — граф камер без сітки; файл короткий навмисно.
