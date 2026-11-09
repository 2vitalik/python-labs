---
title: SokoChess (і SokoChess White / Black)
slug: sokochess
aka: [SokoChess White, SokoChess Black, Сокошахи]
family: push-slide
also: [chess-abstract, thinky]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: none
  goal: state
year: 2022
platforms: [PC, macOS, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1960400/SokoChess/", best: true, note: "опис: штовхай чорні фігури на цілі; чорні ходять, лише коли можуть взяти; 70 рівнів, ∞ undo, пропуск рівня"}
  - {kind: steam, url: "https://store.steampowered.com/app/2185860/SokoChess_White/", note: "лише білі фігури: доставити свої фігури на цілі"}
  - {kind: steam, url: "https://store.steampowered.com/app/2482820/SokoChess_Black/", note: "мета — взяти всі білі; свої фігури можна штовхати"}
  - {kind: other, url: "https://ladiesgamers.com/sokochess-review/", note: "огляд: ходи за шахами, цілі з червоним пішаком, тріснуті плитки, ключі й замки, налаштування"}
  - {kind: other, url: "https://www.gamingonlinux.com/2022/08/sokochess-combines-chess-with-the-sokoban-block-pushing-formula/page=1/", note: "новина: cracked tiles, locks + key; відео"}
  - {kind: other, url: "https://www.pieuvre.ca/2022/10/12/gaming-puzzles-sokochess-review/", note: "огляд FR: чорний пішак бʼє по діагоналі, жертви фігур, нема підказок"}
  - {kind: other, url: "https://www.gamegrin.com/reviews/sokochess-white-review/", note: "огляд White: ящики, заморожувальні плитки, бомби"}
  - {kind: other, url: "https://ladiesgamers.com/sokochess-white-review/", note: "огляд White: кінь переставляє фігури, кілька рівнів відкрито одночасно"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=nyUJq8s-VMM", note: "відео з новини GamingOnLinux"}
stage: v1
coverage: 55
mechanics: [piece-move-patterns, push-object, all-on-targets, piece-capture, impassable-cells, key-and-door, item-pickup, cell-click, undo-unlimited, restart-level, skip-level, level-select, level-unlock, sequential-levels, achievements-window, language-picker, game-settings, goal-counter, +crumbling-floor, +chess-push, +capture-only-opponent, +freeze-tile, +knight-relocate]
proposes: ["+cond:can_capture", "+card:chess-push", "+card:capture-only-opponent", "+card:freeze-tile", "+card:knight-relocate"]
author: opus
date: 2026-11-09
---

# SokoChess — Sokoban, де ящики й штовхачі — шахові фігури, а чорні бʼють, щойно ти підставився

## Суть
Мінімалістичний пазл: на зменшеній шаховій дошці твої білі фігури ходять за шаховими правилами, але замість взяття **штовхають** чорні фігури; мета рівня — поставити всі чорні на позначені цілі. Чорні стоять, доки не зʼявиться можливість взяти твою фігуру, — тоді бʼють. Тобто кожен хід — і Sokoban-поштовх, і перевірка «чи не підставив я фігуру». Сиквели інвертують ідею: White — лише білі, штовхай свої фігури на цілі; Black — мета взяти всі білі, а свої можна штовхати.

## Поле і час
- Квадратна сітка-«дошка» довільної форми й розміру на рівень (не 8×8); з рівнями дошки більшають і фігур більше (LadiesGamers).
- Покроково: хід гравця → реакція чорних (якщо є взяття) (`time: turn`).
- Шари: клітини (звичайна / ціль / тріснута / заморожувальна / замок) + фігури + предмети (ключ, ящик, бомба (?)).
- Ходів необмежено; рахунку нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біла фігура (пішак, кінь, слон, тура, король, ферзь (?)) | piece | тип → патерн ходу | ходить як у шахах; на клітину з чорною не бʼє, а штовхає її (?) |
| Чорна фігура | enemy | тип → патерн взяття | стоїть; якщо може взяти білу — бере (чорний пішак — по діагоналі) |
| Ціль | terrain | позначка «маленький червоний пішак» | рівень пройдено, коли всі чорні на цілях |
| Порожня клітина дошки | terrain | — | прохідна |
| Поза дошкою / діра | static | — | непрохідна (форма дошки = стіни) |
| Тріснута плитка | terrain | ціла → зламана | ламається після того, як фігура пройшла по ній; далі непрохідна (?) |
| Ключ | pickup | — | взяти фігурою → відкриває замок |
| Замок | gate | закрито / відкрито | блокує шлях до ключа |
| Ящик (з оригіналу, згадано в огляді White) | object | — | звичайний Sokoban-ящик (?) |
| Заморожувальна плитка | terrain | — | фігура на ній «замерзає» (?) — механіка не описана в джерелах |
| Бомба | object | — | (?) поведінку в джерелах не описано |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select, piece)` → ТО `custom: «підсвітити фігуру й доступні ходи»` (?).
- КОЛИ `input(move, piece, to)` → ЯКЩО `legal(move)` and `free(to)` → ТО `move(piece, to)`.
- КОЛИ `input(move, piece, to)` → ЯКЩО `legal(move)` and `occupied(to, black)` and `free(cell_behind)` → ТО `push` — чорна зсувається в напрямку руху білої (?); інакше `block`.
- КОЛИ `custom: «хід коня в клітину з фігурою»` → ТО `custom: «кінь переставляє фігуру»` (White: «changing their location with the knight») (?).
- КОЛИ `turn_end(player)` → ЯКЩО `can_capture(black, white)` → ТО `move(black, to)`, `disappear_b` — біла взята.
- КОЛИ `turn_end(player)` → ЯКЩО `not can_capture(black, any)` → ТО `custom: «чорні стоять»`.
- КОЛИ `died(white)` → ТО `restart` (за одним оглядом) або гра триває без фігури (інший огляд про «жертви») (?).
- КОЛИ `leave(piece, cracked_tile)` → ТО `set_cell(cracked_tile, hole)` (?).
- КОЛИ `enter(piece, key)` → ТО `pickup`; КОЛИ `contact(piece, lock)` → ЯКЩО `has(player, key)` → ТО `disappear_b`.
- КОЛИ `enter(piece, freeze_tile)` → ТО `custom: «фігура замерзає»` (?).
- КОЛИ `all_on(black, target)` → ТО `win`, `next_level`.
- White: КОЛИ `all_on(white, target)` → ТО `win`; чорних нема — штовхаєш власні фігури.
- Black: КОЛИ `all_gone(white)` → ТО `win`; свої фігури можна штовхати, щоб вони ходили «не за правилами».
- Перемога: усі чорні на цілях (оригінал). · Поразка: формально нема — undo/рестарт. · Рахунок: нема.

## Керування і ввід
- Миша: клік по фігурі → клік по клітині ходу (Steam: «Mouse Only» для оригіналу); White — миша й клавіатура.
- Кнопки: undo («back»), рестарт рівня, пропуск рівня; екранні контролі вмикаються в налаштуваннях.

## Вікна, меню, HUD
- `main-menu` (?) → `level-select`: сітка 70 рівнів; кілька рівнів відкрито одночасно, застряг — бери інший (White).
- `game-screen`: дошка, фігури, цілі; кнопки `undo-button`, `restart-button`, кнопка пропуску (`custom-window` (?)).
- `settings-window`: «surprising amounts of settings» — вимкнути тряску екрана (`screen-shake-toggle`), екранні контролі, мова (7 мов).
- `achievements-window` — Steam-досягнення.
- Підказок нема (pieuvre.ca).

## Фічі поза полем
- `undo` ∞, `restart-level`, `skip-level` без штрафу.
- `level-unlock` — кілька відкритих рівнів паралельно; поступове введення нових елементів.
- `cloud-save` (Steam Cloud), `achievements`, `localization`, `screen-shake-toggle`.

## Варіації й родичі
- Трилогія: SokoChess (2022) → SokoChess White (2023, без суперника) → SokoChess Black (2023, мета — взяти всі); бандл «Daisy's Sokoban Collection» — інші Sokoban-ігри тієї ж студії.
- [sokoban](sokoban.md) — база поштовху; [ricochet-robots](ricochet-robots.md) — фігури з власним рухом на цілі; [chessformer](../chess-abstract/chessformer.md) — шахи як пазл з гравітацією, ключами й кнопками; [chess-rule-twists](../chess-abstract/chess-rule-twists.md) — шахові варіанти.
- **Осі варіацій**: що штовхається — лише чужі / лише свої / обидва · суперник — нема / бʼє при нагоді / мета — взяти всіх · патерн поштовху — на 1 у напрямку руху / за патерном фігури (кінь) (?) · ціна втрати фігури — рестарт / жертва дозволена.

## Цікавинки для курсу
- «Хід = поштовх» для фігур з різними патернами (тура, слон, пішак): напрям поштовху з вектора ходу — 📎.
- Реактивний суперник «бʼє, якщо може»: після кожного ходу перевірити атаки всіх чорних — 📎.
- Розвʼязувач BFS по станах дошки з урахуванням реакції чорних — 🥇 (стан = позиції всіх фігур + тріснуті плитки + ключі).
- Тріснуті плитки, що ламаються після проходу: дошка змінює форму — 🌱.
- Інверсія режиму (White/Black) як параметр одного рушія — 🥉.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ шахові ходи; `push-object` ↔ поштовх; `all-on-targets` + `goal-counter` ↔ цілі; `piece-capture` ↔ чорні бʼють; `impassable-cells` ↔ форма дошки; `key-and-door` + `item-pickup` ↔ ключ і замок; `cell-click` ↔ ввід; `undo-unlimited` + `restart-level` + `skip-level` ↔ кнопки; `level-select` + `level-unlock` + `sequential-levels` ↔ прогрес; `achievements-window`; `language-picker` + `game-settings` ↔ налаштування.
- **Нема** → пропозиції карток:
  - `+chess-push` «Шахова фігура штовхає замість брати» · entities/legality · 📎 · слоти {push_dir: move-vector | last-step}.
  - `+capture-only-opponent` «Суперник ходить лише коли може взяти» · game-logic/opponent · 📎.
  - `+freeze-tile` «Плитка заморожує фігуру» · entities/interact · 🌱 (?).
  - `+knight-relocate` «Кінь переставляє фігуру» · entities/legality · 🌱 (?).
  - Повтор корпусу: `+crumbling-floor` (тріснута плитка).

## Пропозиції до словників
- `+cond:can_capture` — фігура A може наступним ходом взяти B (реакція чорних SokoChess).
- `+card:chess-push`, `+card:capture-only-opponent`, `+card:freeze-tile`, `+card:knight-relocate` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: SokoChess](https://store.steampowered.com/app/1960400/SokoChess/) — «push all the black pieces to their destination»; чорні ходять лише при можливості взяти; 70 рівнів, infinite undos, skip.
- [Steam: SokoChess White](https://store.steampowered.com/app/2185860/SokoChess_White/) — «get all the white pieces to their destination».
- [Steam: SokoChess Black](https://store.steampowered.com/app/2482820/SokoChess_Black/) — «capture every white piece», свої можна штовхати.
- [LadiesGamers: SokoChess](https://ladiesgamers.com/sokochess-review/) — цілі з червоним пішаком, «breakable tiles, keys and locks», налаштування, undo/restart/skip.
- [GamingOnLinux](https://www.gamingonlinux.com/2022/08/sokochess-combines-chess-with-the-sokoban-block-pushing-formula/page=1/) — «cracked tiles that break after moving over them, locks that need you to pick up a key»; відео.
- [Pieuvre.ca](https://www.pieuvre.ca/2022/10/12/gaming-puzzles-sokochess-review/) — чорний пішак бʼє по діагоналі, жертви, нема підказок.
- [GameGrin: White](https://www.gamegrin.com/reviews/sokochess-white-review/) — «crates, freezing tiles and bombs».
- [LadiesGamers: White](https://ladiesgamers.com/sokochess-white-review/) — кінь переставляє фігури, кілька рівнів відкрито.

## Непевне
- (?) Точна семантика поштовху: на скільки клітин і в якому напрямку зсувається чорна фігура (особливо від коня й слона); чи можна штовхати ланцюгом.
- (?) Наслідок взяття білої: один огляд — «forcing a restart», інший — «sacrifices become an occasional necessity».
- (?) Поведінка заморожувальних плиток, бомб і ящиків — у джерелах лише назви.
- (?) Набір фігур (чи є ферзь) і чи діє перетворення пішака.
- (?) Чи є в оригіналі клавіатура (Steam-тег «Mouse Only», але огляд White каже «mouse and keyboard»).
