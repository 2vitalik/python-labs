---
title: Monocre
slug: monocre
aka: [モノクロルートクリエイター, モノクリ, Monochrome Route Creator]
family: thinky
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2013
platforms: [PC (конкурсна збірка 2013), iOS (2025), Steam (Windows, 2026)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4502500/Monocre/", best: true, note: "правило двох кольорів, дати/забрати колір, сірі/рамкові/обмінні блоки; 9 світів × 12 етапів; покроковий показ розвʼязку"}
  - {kind: steam, url: "https://store.steampowered.com/app/4779270/Monocre_Demo/", note: "безкоштовне демо (травень 2026), той самий опис блоків"}
  - {kind: other, url: "https://apps.apple.com/jp/app/id6753330299", note: "мобільна версія Shun Matsumoto (© 2013): ті самі блоки, «倉庫番系» у описі, кілька світів"}
  - {kind: other, url: "https://www.gamebusiness.jp/article/2013/07/31/8350.html", note: "фіналісти Japan Game Awards 2013, аматорський розділ: № 16 Project Monochrome (HAL Osaka), PC"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=gpkJPWKrLxg", note: "конкурсне відео 2013 «日本ゲーム大賞2013 アマチュア部門 16»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Monocre+gameplay", note: "пошук; геймплей Steam-версії"}
stage: v1
coverage: 35
mechanics: [move-by-input, impassable-cells, cell-transform, reach-exit, sequential-levels, save-progress, +color-pass-through, +color-transfer, +color-swap-block, +solidify-after-pass, +hint-solution-steps]
proposes: ["+card:color-transfer", "+card:color-swap-block", "+card:solidify-after-pass"]
author: opus
date: 2026-11-09
---

# Monocre — герой білий або чорний: свої блоки тверді, чужі — повітря, а колір можна віддати чи забрати

## Суть
Двоколірна головоломка: персонаж і блоки бувають лише білими або чорними. Блоки свого кольору — тверді (їх можна «торкатися»), блоки протилежного — персонаж проходить наскрізь. Ядро — вибір, що перефарбувати: віддати свій колір блоку чи забрати колір блоку собі, щоб «прокласти маршрут» до цілі (звідси назва «Monochrome Route Creator»). Гра виросла зі студентського проєкту HAL Osaka (фіналіст Japan Game Awards 2013), перевидана на iOS (2025) і Steam (2026).

## Поле і час
- Сітка блоків (Steam-тег «Grid-Based Movement», опис iOS — «для любителів 倉庫番», тобто Sokoban-подібне); вигляд згори чи збоку й наявність гравітації — (?).
- Покроково: розвʼязок показується «по одному ходу» (`答え合わせ`), отже стан змінюється дискретними ходами.
- Шари: клітина з блоком певного кольору (білий / чорний / сірий / рамка / обмінний) + персонаж; прохідність клітини залежить від пари «колір персонажа × колір блока».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж | player | колір: white / black | рух сіткою; торкається блоків свого кольору, проходить крізь протилежні; віддає або забирає колір |
| Білий блок | static | колір white | твердий для білого персонажа, прохідний для чорного; може бути перефарбований |
| Чорний блок | static | колір black | дзеркально до білого |
| Сірий блок | static | — | твердий для обох кольорів |
| Рамковий блок (frame) | terrain | контур / твердий | контур прохідний; після того як персонаж пройде крізь нього — стає твердим блоком |
| Обмінний блок (swap) | switch | колір | миттєво міняє колір між собою і персонажем |
| Ціль | static | — | досягти — етап пройдено |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(hero, dir)`.
- КОЛИ `contact(hero, block)` → ЯКЩО `same(hero, block, color)` → ТО `block` (блок твердий, його можна «торкатися»).
- КОЛИ `contact(hero, block)` → ЯКЩО `not same(hero, block, color)` → ТО `move(hero, dir)` — проходить наскрізь.
- КОЛИ `contact(hero, gray_block)` → ТО `block` — сірий твердий за будь-якого кольору.
- КОЛИ `contact(hero, frame_block)` → ЯКЩО `state(frame_block, outline)` → ТО `move(hero, dir)` — контур ще прохідний.
- КОЛИ `input(give_color)` → ЯКЩО `custom: «поруч / у клітині є білий або чорний блок» (?)` → ТО `paint(block, hero_color)`.
- КОЛИ `input(absorb_color)` → ЯКЩО `custom: «поруч / у клітині є білий або чорний блок» (?)` → ТО `set_state(hero, block_color)`.
- КОЛИ `contact(hero, swap_block)` → ТО `paint(swap_block, hero_color)`, `set_state(hero, old_block_color)` — обмін одночасно.
- КОЛИ `leave(hero, frame_block)` → ТО `set_cell(frame_block, solid_block)`.
- КОЛИ `reach(hero, goal)` → ТО `win`, `next_level`.
- Перемога: персонаж на цілі. · Поразка: явної нема (?) — глухий кут розвʼязується скиданням етапу. · Рахунку нема.

## Керування і ввід
- Рух персонажа сіткою + дві дії: «віддати колір» і «забрати колір»; точні клавіші й вибір цільового блока — (?).
- Опис: «просте керування, мислительний екшн» (`シンプル操作で…思考型アクション`); iOS — тач, Steam — клавіатура/геймпад (?).

## Вікна, меню, HUD
- `game-screen`: поле етапу з персонажем і блоками; HUD — (?).
- `level-select` / `map-window`: світи по 12 етапів; нові світи відкриваються проходженням (у версії iOS 1.1.1 правили «новий світ не відкривається»).
- `solutions-window` (`答え合わせ`): покроковий показ розвʼязку етапу, «по одному ходу».
- `settings-window`: звук (iOS 1.1.1 — гучність), мова (12 мов у Steam).
- iOS: діалог «нова версія», push-сповіщення, реклама між етапами.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: 9 світів × 12 етапів у Steam, нові світи обіцяні безкоштовними оновленнями.
- `show-solution` — покроковий розвʼязок, коли застряг.
- `cloud-save` (Steam Cloud), досягнення Steam, `localization` (12 мов).
- Undo — (?), не згадано в жодному джерелі.

## Варіації й родичі
- Версії: конкурсна PC-збірка 2013 (Project Monochrome, HAL Osaka) → iOS «モノクロルートクリエイター» (2025, Shun Matsumoto, безкоштовно з рекламою) → Steam «Monocre» (2026, Monogames) з демо.
- Родичі за ідеєю «твердість залежить від кольору»: Ikaruga-подібні полярності, `games/thinky/toodee-and-topdee.md` (два режими світу), Sokobetter (білі/чорні ящики).
- **Осі варіацій:** хто змінює колір — лише гравець (перемикач) / гравець і блоки (Monocre) / спецблок обміну; скільки кольорів — 2 / RGB-змішування; що стається з блоком після проходу — нічого / стає твердим (рамка).

## Цікавинки для курсу
- Прохідність як функція пари кольорів (`same(hero, block, color)` у перевірці руху) — 🌱.
- Дві дзеркальні дії «віддати колір / забрати колір» над одним блоком — 📎 (два ефекти, один вибір гравця).
- Рамковий блок: прохідний, доки не пройдеш, потім твердий — 🌱 (стан клітини після `leave`).
- Обмінний блок: атомарний обмін станами двох сутностей — 📎.
- Покроковий показ розвʼязку з файла рівня — 📎; розвʼязувач BFS по станах (позиція + колір героя + кольори блоків) — 🥈.

## Мапа на каталог
- Є: `move-by-input` ↔ рух персонажа; `impassable-cells` ↔ тверді блоки свого кольору й сірі; `cell-transform` ↔ рамка → твердий блок; `reach-exit` ↔ ціль; `sequential-levels` + `save-progress` ↔ світи й хмарні сейви.
- Уже пропоновані іншими файлами: `+color-pass-through` (прохід крізь чужий колір), `+hint-solution-steps` (покроковий розвʼязок).
- **Нема** → пропозиції карток:
  - `+color-transfer` «Віддати / забрати колір у блока» · entities/state · 📎 · слот {mode: give|absorb}.
  - `+color-swap-block` «Блок обміну кольором з гравцем» · entities/interact · 🌱.
  - `+solidify-after-pass` «Контур стає твердим після проходу» · entities/legality · 🌱.

## Пропозиції до словників
- `+card:color-transfer`, `+card:color-swap-block`, `+card:solidify-after-pass` — механік нема в каталозі.

## Джерела
- ⭐ [Steam: Monocre](https://store.steampowered.com/app/4502500/Monocre/) — правило двох кольорів, «дати колір / поглинути колір», сірі/рамкові/обмінні блоки, 9 світів × 12 етапів, покроковий `答え合わせ`, 12 мов, нагорода JGA 2013 (JP-версія сторінки — повніший опис).
- [Steam: Monocre Demo](https://store.steampowered.com/app/4779270/Monocre_Demo/) — той самий опис блоків.
- [App Store: モノクロルートクリエイター](https://apps.apple.com/jp/app/id6753330299) — iOS-версія, © 2013 Shun Matsumoto, «倉庫番系», історія версій (світи, реклама).
- [GameBusiness.jp: фіналісти JGA 2013](https://www.gamebusiness.jp/article/2013/07/31/8350.html) — № 16 «モノクロルートクリエイター», Project Monochrome, HAL Osaka, PC.
- [YouTube: конкурсне відео 2013](https://www.youtube.com/watch?v=gpkJPWKrLxg) — назва перевірена, опис не прочитано.

## Непевне
- (?) Вигляд поля (згори чи збоку з гравітацією) і чи є штовхання блоків — Steam-теги «Sokoban», «Grid-Based Movement», але правила руху ніде не описані.
- (?) Як обирається блок для «віддати / забрати колір» (сусідній, той, у якому стоїш, напрямок погляду) і чи діє це на сірі блоки.
- (?) Що відбувається, коли персонаж стоїть усередині чужого блока й робить його своїм кольором.
- (?) Undo/рестарт, клавіші, HUD — не згадано.
- (?) Чи конкурсна версія 2013 мала ті самі блоки (рамка, обмін) — App Store лише ставить © 2013.
