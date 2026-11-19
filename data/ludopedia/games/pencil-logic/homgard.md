---
title: Homgard
slug: homgard
aka: ["Homgard: Book 1"]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2026
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4287570/Homgard/", best: true, note: "675 ручних пазлів, 25 регіонів, 6 нових механік (форми полів, кольорові клітини), без таймерів, асисти; трейлер, демо"}
  - {kind: other, url: "https://ladiesgamers.com/homgard-review/", note: "рецензія: червоні й сині клітини, мапа-сітка з тайлами, телепорти, якорі реальності, компендіум, спогади, радіо"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=4287570&count=20", note: "Steam News: патчі 1.0.1–1.0.8 — маркери зелених і синіх клітин, Hint Coins, Cell Marking, асисти, зум"}
  - {kind: official, url: "https://homgard.carrd.co/", note: "лендинг: Steam, розсилка, прес-кіт"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Homgard+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [run-length-clues, satisfy-constraints, completion-detection, markup-validity, cell-click, hover-highlight, conflict-highlight, connectivity-check, undo-redo, world-map, map-window, teleport-pair, codex-window, save-autosave, controls-remap, theme-select, +cross-mark, +auto-cross-line, +drag-paint-line, +clue-greying, +shaped-board, +color-cell-rules, +all-or-nothing-group, +hint-reveal, +paid-hint, +cell-count-marker, +drag-axis-lock, +story-journal]
proposes: ["+ui:cell-counter", "+feature:assist-presets", "+feature:in-world-radio", "+card:color-cell-rules", "+card:all-or-nothing-group", "+card:cell-count-marker"]
author: opus
date: 2026-11-19
---

# Homgard — нонограми з кольоровими клітинами-правилами відкривають мапу зламаного світу

## Суть
Сюжетна нонограм-пригода Manapunk Studio, «книга 1» з чотирьох. Основа — звичайна нонограма (серії на рядках і стовпцях), але частина пазлів має неквадратне поле, а кольорові клітини додають свої правила: червона група — уся зафарбована або вся закреслена, зафарбована синя має бути звʼязана з синім ядром. Розвʼязані пазли відкривають тайли мапи-сітки, а з ними — короткі тексти-спогади, з яких складається загадка світу.

## Поле і час
- Пазл — прямокутна сітка від 5×5 (перший регіон) до великих (у рецензії 25×15); є поля «варійованих форм» — маска на квадратній сітці.
- Кольорові клітини лежать на тій самій сітці: червоні групи, сині області з ядром, зелені, чорні, «інертні» (на скриншотах ще помаранчеві з перемичками й сіра зона з підказками праворуч і знизу — правила не перевірив).
- Мапа світу — окрема сітка тайлів: більша частина схована, розвʼязання сусідніх пазлів відкриває тайли; 25 регіонів.
- Без таймерів; кожен пазл розвʼязний без вгадування.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина | mark | порожня / зафарбована / X | ставиться гравцем; X — позначка «точно порожньо» |
| Підказка лінії | static | серії | як у нонограмі; виконана блякне |
| Червона клітина | mark | група червоних | уся група зафарбована або вся закреслена |
| Синя клітина | mark | синя область | зафарбована синя має бути звʼязана з синім ядром |
| Синє ядро | static | число (?) | центр синьої області; клітинами-позначками не рахується |
| Зелена клітина | mark | умова (?) | маркер помилки, лише коли умову вже не виконати |
| Чорна / інертна клітина | static | — | не враховується лічильником клітин (?) |
| Тайл-пазл (фіолетовий) | gate | пазл | відкривається лише розвʼязанням свого пазла |
| Тайл-шлях (помаранчевий, зелений) | terrain | — | відкривається, коли на нього стати (миша або WASD) |
| Телепорт | terrain | пара | миттєво переносить до парного тайла |
| Якір реальності | pickup | — | без нього частина тайлів недоступна; не всі обовʼязкові |
| Ядро сновидця | pickup | 3 на гру | зібрати три й повернутися до Origin |
| Спогад | pickup | текст, регіон | відкривається пазлом; зберігається в компендіумі |
| Hint Coin | resource | кількість | відкриває випадкову порожню або хибну клітину |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(fill, c)` → ТО `mark(c, filled)`; повтор — `unmark(c)`; з опцією «Overwrite Cells» протяжка перезаписує позначене.
- КОЛИ `input(cross, c)` → ТО `mark(c, x)`.
- Серії: ЯКЩО `run_lengths(line)` — як у [nonogram.md](nonogram.md); виконане число блякне, лінію з правильним і хибним групуванням підсвічено.
- Червоні: ЯКЩО `same(red_group, state)` — `custom: «згруповані червоні або всі зафарбовані, або всі закреслені»`.
- Сині: ЯКЩО `connected(blue_filled + core)` — кожна зафарбована синя клітина звʼязана з синім ядром своєї області.
- Зелені: ЯКЩО `custom: «умова зеленої клітини»` (?).
- КОЛИ `constraint_broken(green)` → ЯКЩО `custom: «умову вже не виконати»` → ТО `set_state(c, error_marker)`.
- КОЛИ `constraint_broken(blue)` → ЯКЩО `mode(markers_errors_only)` → ТО `set_state(c, error_marker)`; режими маркерів — On / Off / Errors Only.
- Маска поля: ЯКЩО `custom: «клітини поза формою поля не існують»`.
- КОЛИ `custom: «серії лінії виконано»` → ЯКЩО `mode(auto_cross)` → ТО `mark(empty_cells_of_line, x)`.
- КОЛИ `input(hint_coin)` → ЯКЩО `has(player, hint_coin)` → ТО `take(player, hint_coin)`, `reveal(random_empty_or_wrong_cell)`, `set_state(cell, locked)`; монети назад не повертаються.
- КОЛИ `custom: «відкрито нову частину мапи»` → ТО `give(player, hint_coin)`.
- КОЛИ `all_constraints_met` → ТО `win`; з «Auto Close Puzzle» (типово увімкнено) — `custom: «пазл закривається сам»`; далі `reveal(map_tiles)`, `unlock(memory)`.
- Мапа: КОЛИ `input(move, tile)` → ЯКЩО `cell(tile, path)` → ТО `move(marker, tile)`, `reveal(tile)`.
- КОЛИ `input(move, tile)` → ЯКЩО `cell(tile, puzzle)` → ТО `window(game-screen)` пазла.
- КОЛИ `enter(marker, teleport)` → ТО `teleport(marker, pair)`.
- КОЛИ `picked(player, reality_anchor)` → ТО `reveal(area)`, `unlock(tiles)`.
- КОЛИ `reach(marker, origin)` → ЯКЩО `counter(dreamer_cores, ==, 3)` → ТО `win` гри (книги 1).
- Перемога: усі підказки й кольорові правила виконано. · Поразка: нема. · Рахунок: нема, прогрес — відкрита мапа й спогади.

## Керування і ввід
- Миша: зафарбувати й закреслити (кнопки — типові для нонограм (?)), протяжка лінією; «Drag Assist» фіксує протяжку на одній осі.
- Cell Marking (колись Cell Counting): протяжкою підсвітити клітини й побачити їх кількість; режими «тимчасовий» і «Sticky»; можна навісити на СКМ.
- Клавіша «I» — показати колір і стан клітини під курсором; СКМ — підсвітка клітини.
- Мапа: миша або WASD; з v1.0.2 — геймпад і повне перепризначення клавіш (з другими привʼязками).

## Вікна, меню, HUD
- `map-window`: мапа-сітка з тайлами, назви «Homgard → регіон → локація», маркер гравця, тайли-пазли й тайли-шляхи; зум мапи з клавіатури й геймпада.
- `game-screen` (пазл): поле з підказками згори й зліва (на частині пазлів — ще з інших боків (?)); колесо-HUD ліворуч угорі: налаштування, назад, «?», монети-підказки, рестарт (?), радіо; `+ui:cell-counter`; `conflict-highlight` для кольорових правил; зум пазла (Disabled / 10×10 / 15×15 / 20×20).
- `custom-window` спогаду: текст запису з підписом і датою.
- `codex-window` — Compendium: спогади (пошук за змістом, станом, регіоном, часом) і правила кожного типу клітин.
- `settings-window`: асисти, палітри, розмір шрифту, клавіші, гучність радіо.
- `help-window` (?) — «?» на HUD.
- Переходи: map-window → (тайл-пазл) game-screen → (усі підказки виконано) map-window з відкритими тайлами → спогад.

## Фічі поза полем
- `world-map` з туманом: 25 регіонів, тайли відкриваються пазлами, телепорти, якорі реальності; мета — три ядра сновидця й повернення до Origin.
- Спогади (сотні коротких текстів) у компендіумі — `+story-journal`; термінальна програма підказує й підбадьорює.
- Асисти й пресети «Full / No Assist» (`+feature:assist-presets`): блякнення виконаних чисел, підсвітка правильних і хибних групувань, `auto-check`-подібні маркери кольорових правил, автохрестики в завершеній лінії, Drag Assist, Auto Close Puzzle, Puzzle Preview, Overwrite Cells.
- `hint` за Hint Coins (з v1.0.4): випадкова порожня або хибна клітина, відкрита клітина замикається.
- `undo` / `redo`, `autosave` з резервними копіями, `remap-controls`, `gamepad-support`, `colorblind-palette`-подібні палітри, `font-scale`, радіо з шести станцій (`+feature:in-world-radio`), `achievements`.

## Варіації й родичі
- База — [nonogram.md](nonogram.md); кольорові підказки й складені картини Nintendo — [picross-variants.md](picross-variants.md).
- Інші нонограми хвилі з власними правилами: [liquidum.md](liquidum.md) (вода й гравітація), [cinicross.md](cinicross.md) (роглайт, боси міняють правила), [squarecells.md](squarecells.md) (розміри груп).
- «Звʼязано з ядром» — родич [nurikabe.md](nurikabe.md) / [hashiwokakero.md](hashiwokakero.md) за перевіркою звʼязності.
- **Осі варіацій**: форма поля — прямокутник / маска · колір клітини — нічого не значить (Color Picross) / додає правило (Homgard) · правило групи — серії / усе-або-нічого / звʼязність з ядром · мета-структура — список пазлів / мапа з туманом і сюжетом.

## Цікавинки для курсу
- Червона група «усе або нічого»: перевірка однакового стану в кожній групі — 🌱.
- Сині клітини, звʼязані з ядром: BFS від ядра по зафарбованих синіх — 📎.
- Поле-маска неправильної форми з підказками нонограми — 📎 (як рахувати серії через «дірки»).
- Мапа з туманом, де тайли відкриває розвʼязаний пазл, плюс телепорти й якорі — 🥉.
- Hint Coin: знайти випадкову порожню чи хибну клітину, відкрити й замкнути — 🌱.
- Лінійний солвер нонограми з кольоровими правилами як додатковими обмеженнями — 🥇.

## Мапа на каталог
- Є: `run-length-clues`, `satisfy-constraints`, `completion-detection`, `markup-validity` ↔ хибні групування; `cell-click`; `hover-highlight` ↔ підсвітка клітини; `conflict-highlight` ↔ маркери «Errors Only»; `connectivity-check` ↔ сині з ядром; `undo-redo`; `world-map`, `map-window` ↔ мапа тайлів; `teleport-pair` ↔ телепорти мапи; `codex-window` ↔ Compendium; `save-autosave`; `controls-remap`; `theme-select` ↔ палітри.
- **Нема** → пропозиції карток:
  - `+cross-mark`, `+auto-cross-line`, `+drag-paint-line`, `+clue-greying` (повтор: nonogram).
  - `+shaped-board` (повтор) «Поле довільної форми-маски» · levels/format · 🌱.
  - `+color-cell-rules` «Колір клітини додає своє правило поверх основного» · game-logic/constraints · 📎 · слот {colors: red|blue|green|…}.
  - `+all-or-nothing-group` «Група клітин — уся зафарбована або вся порожня» · game-logic/constraints · 🌱.
  - `+hint-reveal` (повтор) · `+paid-hint` (повтор) — монети за відкриту мапу.
  - `+cell-count-marker` «Протяжкою позначити клітини й бачити їх кількість» · interface/input · 🌱.
  - `+drag-axis-lock` «Протяжка фіксується на одній осі» · interface/input · 🌱.
  - `+story-journal` (повтор) — спогади за пазли.

## Пропозиції до словників
- `+ui:cell-counter` — кількість позначених протяжкою клітин біля курсора.
- `+feature:assist-presets` — пресети «усі асисти / без асистів» одним перемикачем.
- `+feature:in-world-radio` — радіо зі станціями як частина світу й фону.
- `+card:color-cell-rules`, `+card:all-or-nothing-group`, `+card:cell-count-marker` — див. мапу.

## Джерела
- ⭐ [Steam: Homgard](https://store.steampowered.com/app/4287570/Homgard/) — 675 пазлів, 25 регіонів, «six new mechanics … varied grid shapes and coloured cells that play by different rules», без таймерів, асисти, палітри й шрифти, радіо, книга 1 з 4; скриншоти з червоними, синіми (ядро «3»), помаранчевими клітинами й мапою.
- [LadiesGamers, рецензія](https://ladiesgamers.com/homgard-review/) — правила червоних і синіх клітин, тайли мапи (фіолетові, помаранчеві, зелені), телепорти, якорі реальності, три ядра сновидця, компендіум, асисти.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=4287570&count=20) — v1.0.1–1.0.8: маркери зелених і синіх клітин, «Black cells», «inert cells», Hint Coins, Cell Marking, Drag Assist, Auto Close Puzzle, Puzzle Preview, Overwrite Cells, зум.
- [homgard.carrd.co](https://homgard.carrd.co/) — лендинг без опису механік.
- YouTube: пошук «Homgard gameplay».

## Непевне
- (?) Правила зелених, чорних та інертних клітин, а також помаранчевих із перемичками й сірої зони з підказками з чотирьох боків (видно на скриншоті) — у відкритих джерелах не описані.
- (?) Що означає число на синьому ядрі (на скриншоті «3» і рівно 3 зафарбовані сині поруч — ймовірно, кількість звʼязаних синіх).
- (?) Які саме шість механік гра вважає «новими» — Steam називає лише форми полів і кольорові клітини.
- (?) Кількість пазлів: Steam — 675, сторонній (згенерований ШІ) огляд — 690; беру Steam.
- (?) Кнопки миші для зафарбування й хрестика та чи перевіряє гра хід одразу (Hint Coin знаходить «incorrectly filled cell», отже хибне можна поставити).
