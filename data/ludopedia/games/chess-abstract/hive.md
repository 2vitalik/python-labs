---
title: Hive (Вулик)
slug: hive
family: chess-abstract
also: [board-digital]
klass: figure
axes:
  field: hex
  time: turn
  opponent: online
  info: full
  random: none
  goal: state
year: 2001
platforms: [board, web, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hive_(game)", best: true, note: "усі комахи й ходи, один вулик, свобода руху, розширення, нічиї"}
  - {kind: official, url: "https://www.gen42.com/games/hive", note: "Gen42 — видавець; правила кількома мовами"}
  - {kind: official, url: "https://www.gen42.com/wp-content/uploads/Hive-rules.pdf", note: "PDF правил (скан-картинки)"}
  - {kind: play, url: "https://hivegame.com/", note: "офіційна онлайн-гра: виклики, боти, Base/MLP, годинник"}
  - {kind: other, url: "https://www.boardgamegeek.com/boardgame/2655", note: "BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hive+board+game+how+to+play", note: "пошук; правила"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, legal-move-highlight, turn-enforcement, move-timer, hot-seat, ai-opponent, drag-drop-piece, cell-click, no-moves-left, replay, profile-stats, +piece-drop, +one-hive-rule, +freedom-to-move, +stack-climb, +jump-over-line, +copy-move-pattern, +throw-neighbor, +surround-win, +placement-deadline, +unbounded-field]
proposes: ["+trigger:passes", "+trigger:repetition", "+cond:group", "+cond:connected_after", "+cond:can_slide", "+cond:surrounded", "+effect:place", "+effect:climb", "+effect:copy_pattern", "+role:zone", "+ui:pocket", "+ui:stack-viewer", "+window:expansion-select", "+axis:field-bounds"]
author: opus
date: 2026-11-02
---

# Hive — шахи без дошки: комахи-плитки самі утворюють поле, оточи королеву суперника

## Суть
Кожен гравець має 11 гексагональних плиток-комах (з розширеннями до 14); хід — викласти нову плитку або перемістити вже викладену. Дошки нема: поле — це сам «вулик», звʼязна група плиток, що росте й змінює форму. Перемога — оточити ворожу бджолу-королеву з усіх шести боків (будь-якими плитками, своїми чи чужими). Ядро — глобальні обмеження руху: вулик ніколи не можна розірвати, а плитка має фізично «пролізти» між сусідами.

## Поле і час
- Нескінченна гекс-площина без меж; існують лише клітини, що торкаються вулика. Камера/зум у цифровій версії — бо поле росте в будь-який бік.
- Шари по висоті: жук і сонечко можуть стояти **на** інших плитках (стек будь-якої висоти).
- Хід = викласти плитку з запасу **або** перемістити свою плитку (або, для мокриці, перекинути сусіда). Нема ходів — пас.
- Годинник — як у шахах (хвилини + інкремент; hivegame.com: пресети 1+2, 5+4, 10+10, кореспонденція, без часу).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бджола-королева (Queen Bee) | piece | royal; ×1 | 1 крок ковзанням; має бути викладена до 4-го ходу; без неї не можна рухати інші плитки |
| Павук (Spider) | piece | ×2 | рівно 3 кроки ковзанням по краю вулика, без повернення на пройдену клітину |
| Жук (Beetle) | piece | ×2; висота | 1 крок у будь-який бік, зокрема **на** вулик; згори ходить по плитках і може спуститись; плитка під ним заблокована; стек має колір верхньої |
| Коник (Grasshopper) | piece | leaper; ×3 | стрибає по прямій через ≥1 суцільний ряд плиток до першої порожньої клітини |
| Мураха-солдат (Soldier Ant) | piece | ×3 | будь-яка кількість кроків ковзанням по зовнішньому краю |
| Комар (Mosquito) | piece | розширення; ×1 | ходить як будь-яка сусідня комаха; на вершині вулика — лише як жук; поруч лише комар — не ходить (?) |
| Сонечко (Ladybug) | piece | розширення; ×1 | рівно 3 кроки: 2 по верху вулика, 1 вниз на порожню |
| Мокриця (Pillbug) | piece | розширення; ×1 | 1 крок як королева **або** замість руху переносить сусідню плитку (свою чи чужу) через себе на іншу порожню сусідню клітину |
| Запас (рука) | zone | плитки з лічильниками | джерело викладання |
| Вулик | zone | звʼязна група | поле гри; має лишатися звʼязним |

## Правила (КОЛИ → ЯКЩО → ТО)
- **Викладання** — КОЛИ `input(place(kind, cell))` → ЯКЩО `has(side, kind)` and `free(cell)` and `adjacent(cell, own)` and `not adjacent(cell, enemy)` → ТО `place(kind, cell)`, `take(side, kind)`, `end_turn`. Виняток: перша плитка — будь-де; перша плитка другого гравця — поруч із першою суперника. Нові плитки кладуться лише на рівень землі, не на вулик.
- **Королева до 4-го ходу** — КОЛИ `turn_start(side)` → ЯКЩО `counter(own_turns, ==, 4)` and `has(side, queen)` → ТО легальне лише `place(queen)`. Турнірне правило: королеву не можна класти першим ходом (офіційне в Hive Ultimate 2024).
- **Рух лише після королеви** — КОЛИ `input(move(piece))` → ЯКЩО `has(side, queen)` (ще в запасі) → `block`.
- **Один вулик** — КОЛИ `input(move(piece))` → ЯКЩО `not connected_after(hive − piece)` (навіть на мить під час руху) → `block`.
- **Свобода руху** — ЯКЩО `not can_slide(piece, from, to)` (прохід між двома сусідами завузький) → `block`; виняток: жук, коник, сонечко (не ковзають), рух по верху.
- **Ковзання по краю** — королева/павук/мураха рухаються лише кроками, на кожному з яких лишаються в контакті з вуликом.
- **Жук** — КОЛИ `input(move(beetle, occupied_cell))` → ТО `climb(beetle, cell)`; плитка під ним `set_state(pinned)`; колір стеку для правил викладання = колір верхньої плитки.
- **Коник** — КОЛИ `input(move(grasshopper, dir))` → ЯКЩО сусід у напрямку зайнятий → ТО `move(grasshopper, first_free_in_line)`; інакше `block`.
- **Комар** — КОЛИ `input(move(mosquito))` → ТО `copy_pattern(adjacent_kind)`; ЯКЩО `state(mosquito, on_top)` → патерн жука.
- **Мокриця** — КОЛИ `input(throw(pillbug, neighbor, to))` → ЯКЩО сусід не накритий, не ходив минулим ходом суперника, переміщення не розриває вулик і не проходить через «ворота» жука → ТО `move(neighbor, to)`, `set_state(neighbor, frozen, 1 turn)`.
- **Пас** — КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` → ТО `pass_turn` (обовʼязково).
- **Перемога** — КОЛИ `after(move)` → ЯКЩО `surrounded(queen[enemy], 6)` → ТО `win`; ЯКЩО обидві королеви оточено одним ходом → `draw`.
- **Нічия** — нескінченне повторення позицій (пат) або угода (?).
- Рахунку нема: 1 / ½ / 0, рейтинг онлайн.

## Керування і ввід
- Викладання: drag плитки з запасу на підсвічену порожню клітину (або клік-клік).
- Рух: клік по своїй плитці → підсвітка всіх досяжних клітин (для мурахи — десятки) → клік по цілі. Жук на стеку — клік по стеку бере верхню.
- Мокриця: окремий двокроковий ввід — вибрати сусідню плитку, потім клітину, куди її покласти.
- Пас, здача, пропозиція нічиєї, undo (takeback) за згодою (?).
- Зум/пан поля колесом або жестом; перегляд стеку (що під жуком).

## Вікна, меню, HUD
- (цифрова версія — hivegame.com / BGA / Steam)
- `game-screen`: гекс-поле з `zoom-control` і паном; два `pocket` (запаси плиток з лічильниками ×3 тощо), `player-clock` обох, `turn-indicator`, `move-list` (нотація UHP: `wA1 -bS1` тощо (?)), `legal-move-highlight` для вибраної плитки, `last-move-highlight`, `stack-viewer` при наведенні на стек.
- Виклик (`lobby-window` + `expansion-select`): набір Base або MLP (Mosquito, Ladybug, Pillbug), rated/casual, private/public, режим часу (real-time / кореспонденція / без часу), діапазон рейтингу; гра з ботом (Easy/Medium/Hard).
- `end-screen`: хто оточив королеву, зміна рейтингу, повтор.
- `help-window` («Learn to play»), `profile-window` з рейтингом і історією партій.
- Переходи: lobby → game-screen → end-screen → replay / новий виклик.

## Фічі поза полем
- `custom-rules` — вибір набору комах (Base / MLP / окремі розширення) і турнірного правила відкриття.
- `online-multiplayer` (виклики, матчі, турніри), `ai-opponent-levels` (3 рівні ботів), `rating`, `turn-timer` (інкремент, кореспонденція), `replay`/`history`.
- Фізична гра не потребує дошки — цифрова версія мусить мати камеру, бо поле необмежене.

## Варіації й родичі
- Hive Pocket (менші плитки, з комаром і сонечком), Hive Carbon (чорно-білі), Hive Ultimate (2024).
- Родичі: шахи (королівська фігура, патерни ходів), го (оточення), Onitama, Santorini (будування по висоті).
- **Осі варіацій**: набір комах (Base / +M / +L / +P) · відкриття (вільне / без королеви першим ходом) · дедлайн королеви (4-й хід) · поле (обмежене / нескінченне) · висота (1 шар / стеки).

## Цікавинки для курсу
- Гекс-координати (осьові/кубічні) на необмеженому полі — 🥉.
- «Один вулик»: перевірка звʼязності після вилучення плитки (BFS/точки зчленування) — 🥈.
- Свобода руху: ковзання між двома сусідами заборонене, якщо обидва «плечі» зайняті — 🥈.
- Різні патерни: рівно 3 кроки без повторів (павук — DFS глибини 3), будь-скільки по краю (мураха — BFS по периметру), стрибок по лінії (коник) — 🥈 за набір.
- Стеки по висоті (жук, сонечко) і «колір стеку» для викладання — 🥉.
- Комар копіює патерн сусіда, мокриця рухає чужу плитку — 🥇 разом (поведінка, залежна від сусідів, + заморозка на хід).

## Мапа на каталог
- Є: `piece-move-patterns` ↔ 8 видів комах · `legal-move-highlight` · `turn-enforcement` · `move-timer` · `hot-seat` · `ai-opponent` ↔ боти · `drag-drop-piece` + `cell-click` · `no-moves-left` (тут — пас, не поразка) · `replay` · `profile-stats`.
- **Нема** → пропозиції карток:
  - `+piece-drop` (див. lichess-variants) — тут викладання з запасу з правилом «торкатися лише своїх».
  - `+one-hive-rule` «Звʼязність поля після ходу» · entities/legality · 🥈.
  - `+freedom-to-move` «Ковзання через вузький прохід» · entities/legality · 🥈.
  - `+stack-climb` «Підйом на інші фігури (стек)» · entities/state · 🥉 · слоти {max_height}.
  - `+jump-over-line` «Стрибок через ряд до першої порожньої» · entities/move · 📎.
  - `+copy-move-pattern` «Копіювання патерну сусіда» · entities/legality · 🥉.
  - `+throw-neighbor` «Перекинути сусідню фігуру» · entities/interact · 🥉.
  - `+surround-win` «Перемога оточенням фігури» · game-logic/win · 📎 · слоти {sides}.
  - `+placement-deadline` «Обовʼязкове викладання фігури до N-го ходу» · game-logic/constraints · 🌱.
  - `+unbounded-field` «Поле без меж, що росте від фігур» · interface/render · 🥉 (камера + зум).

## Пропозиції до словників
- `+trigger:passes` (пас без ходів) · `+trigger:repetition` (нічия повторенням) — спільні з го/шахами.
- `+cond:group` · `+cond:connected_after` — звʼязність після вилучення; `+cond:can_slide` — пролізти між сусідами; `+cond:surrounded` — у клітини зайнято N з 6/4 сусідів (королева Hive, також го).
- `+effect:place` — викладання з запасу (спільне); `+effect:climb` — стати на зайняту клітину зверху; `+effect:copy_pattern` — взяти патерн ходу іншої сутності.
- `+role:zone` — вулик, запас.
- `+ui:pocket` (запас плиток) · `+ui:stack-viewer` (що під верхньою плиткою стеку).
- `+window:expansion-select` — вибір набору фігур/розширень перед партією (близько до `variant-select`).
- `+axis:field-bounds` — `bounded` / `unbounded` (Hive, Life, нескінченні раннери); `field: hex` не каже, що поля нема.

## Джерела
- ⭐ [Wikipedia: Hive (game)](https://en.wikipedia.org/wiki/Hive_(game)) — 11 плиток, ходи всіх комах і розширень, один вулик, свобода руху, викладання, королева до 4-го ходу, турнірне відкриття, нічиї.
- [Gen42: Hive](https://www.gen42.com/games/hive) — видавець, склад гри, правила 10+ мовами.
- [Hive rules PDF](https://www.gen42.com/wp-content/uploads/Hive-rules.pdf) — офіційні правила (скан; текст не витягується).
- [hivegame.com](https://hivegame.com/) — онлайн: Base/MLP, пресети часу, кореспонденція, боти Easy/Medium/Hard, Casual/Rated.
- [BGG: Hive](https://www.boardgamegeek.com/boardgame/2655) — сторінка гри.
- YouTube: пошук «hive board game how to play».

## Непевне
- (?) «Комар поруч лише з комаром не ходить», заморозка плитки після мокриці на 1 хід, заборона мокриці рухати плитку, що щойно ходила, — частково з Wikipedia, деталі з памʼяті.
- (?) Нічия угодою і точне формулювання «нескінченного повторення» — Wikipedia згадує лише повторення/пат.
- (?) Нотація UHP і функції takeback/stack-viewer на hivegame.com — з памʼяті.
- PDF правил Gen42 — скан без тексту, перевірено лише існування.
