---
title: Room to Grow
slug: room-to-grow
aka: []
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1471960/", best: true, note: "«Growing enables you to move», ріст у стіну зсуває все тіло, штовхання рослин, 100+ пазлів, undo/restart/skip, доступність"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Room_to_Grow_(video_game)", note: "кактус видовжується по сітці, мета — інші кактуси на сіру ціль, порівняння зі Snake, кілька розвʼязків"}
  - {kind: other, url: "https://www.gamegrin.com/reviews/room-to-grow-review", note: "три напрямки росту, без вкорочення, поштовх від краю сітки, світи Grassland/Tundra/Desert, багатоголові кактуси, сітки з дірами"}
  - {kind: other, url: "https://geekdad.com/2021/03/geekmom-room-to-grow-a-deceptively-tricky-cactus-based-indie-puzzle-game/", note: "WASD/стрілки, Z — undo, R — рестарт, пропуск рівнів, два кактуси на дві цілі, розквіт при розвʼязку"}
  - {kind: other, url: "https://www.cubed3.com/games/reviews/pc/room-to-grow", note: "цілі — чорні лунки, камінь у Forest задає напрям, мапа вибору рівнів, кнопка Skip Level, другий набір важчих рівнів"}
  - {kind: other, url: "https://www.digitallydownloaded.net/?p=41341", note: "тіло не перетинає себе, лише росте; кожен вазон у свою лунку"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Room+to+Grow+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [push-object, all-on-targets, self-collision, no-reverse-turn, impassable-cells, move-4dir, keyboard-controls, controls-remap, undo-redo, restart-level, skip-level, world-map, level-select, sequential-levels, +grow-on-move, +growth-push, +wall-recoil, +multi-head-body, +hard-mode]
proposes: ["+card:wall-recoil", "+card:grow-on-move", "+card:multi-head-body", "+feature:input-repeat-delay", "+feature:no-move-counter"]
author: opus
date: 2026-11-09
---

# Room to Grow — Sokoban, де крок — це ріст: кактус лише довшає, а впершись у стіну, відсуває себе цілком

## Суть
Гравець — кактус на квадратній сітці. Кожен «хід» — це **ріст** голови на одну клітину в одному з трьох напрямків (назад, у себе, не можна); тіло ніколи не вкорочується і не перетинає себе. Якщо ріст упирається в стіну чи край сітки, **усе тіло зсувається на клітину в протилежний бік** — так кактус «рухається», штовхаючи маленькі кактуси у вазонах до лунок-цілей. Ядро — подвійне використання росту: він і переміщує, і краде простір, тому кожен хід зменшує свободу наступних.

## Поле і час
- Квадратна сітка-кімната зі стінами; пізніше — сітки з вирізаними шматками і нерівномірними сегментами (GameGrin), цілі поза сіткою, до яких дотягуються поштовхом від краю.
- Шари: підлога (звичайна / лунка-ціль) + обʼєкти (тіло кактуса, вазони з малими кактусами, стіни, живоплоти, особливі камені).
- Хід = один ріст (з можливим зсувом тіла й поштовхом вазонів); без вводу нічого не відбувається. Ні таймера, ні лічильника ходів (Steam).
- Камера статична, рівень на одному екрані; GeekDad згадує «можна рухати весь екран» (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кактус гравця | player | довжина (лише зростає), 1+ голів | голова росте на 1 у 3 напрямки; тіло не перетинає себе; упор → зсув усього тіла назад |
| Малий кактус у вазоні | object | — | штовхається на 1, якщо за ним вільно (Sokoban) |
| Лунка-ціль | terrain | — | «чорна лунка» / «сіре коло»: сюди треба поставити вазон |
| Стіна | static | — | непрохідна; ріст у неї зсуває кактус |
| Живопліт | static | — | як стіна: від нього відштовхуються (GeekDad) |
| Край сітки | static | — | теж опора для відштовхування (GameGrin) |
| Особливий камінь (Forest) | static | напрям (?) | удар росту в нього посилає кактус у визначений бік (Cubed3) |
| Багатоголовий кактус | player | N голів | кілька точок росту в одному тілі (GameGrin) |
| Вирізана клітина сітки | static | — | діра в полі: не можна ні рости, ні зсуватись туди (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `custom: «dir — назад, у власне тіло»` → ТО `block`, `sound(squeak)` (кактус червоніє й пищить).
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead_of_head)` → ТО `grow(cactus, 1)` (нова клітина тіла попереду голови).
- КОЛИ `input(dir)` → ЯКЩО `occupied(cell_ahead_of_head, pot)` і `free(cell_behind_pot)` → ТО `push(pot)`, `grow(cactus, 1)` (?).
- КОЛИ `input(dir)` → ЯКЩО `occupied(cell_ahead_of_head, own_body)` → ТО `block` (тіло не перетинає себе).
- КОЛИ `blocked(head)` (стіна, живопліт, край) → ЯКЩО `custom: «клітини за тілом у протилежному напрямку вільні або там вазони, що зсуваються»` → ТО `move(cactus_body, opposite_dir)`, `grow(cactus, 1)`; вазони на шляху зсуву — `push`.
- КОЛИ `blocked(head)` → ЯКЩО `custom: «зсув тіла теж заблокований»` → ТО `block` (?).
- КОЛИ `contact(head, special_rock)` → ТО `custom: «кактус зсувається в напрямку, заданому каменем»` (?).
- КОЛИ `input(dir)` → ЯКЩО `custom: «кактус багатоголовий»` → ТО `custom: «ростуть голови, що можуть рости в цьому напрямку»` (?).
- КОЛИ `enter(pot, hole)` → ТО `custom: «вазон сідає в лунку»` (?); пізніше його ще можна зрушити чи ні — (?).
- КОЛИ `all_on(pot, hole)` → ТО `win`, `custom: «кактус розквітає»`, `window(map-window)`.
- КОЛИ `input(Z)` → ТО `undo(1)`, без обмежень глибини (?); КОЛИ `input(R)` → ТО `restart`.
- КОЛИ `input(skip)` → ТО `custom: «рівень пропущено без штрафу»` — лише зсередини рівня, не з мапи (Cubed3).
- Перемога: усі вазони в лунках. · Поразка: нема — глухий кут лікується undo/restart. · Рахунок: нема (ні часу, ні лічильника ходів, ні таблиць).

## Керування і ввід
- Стрілки або WASD — ріст голови в напрямку; Z — undo по одному ходу; R — рестарт; окрема кнопка Skip Level.
- Перепризначення клавіш, налаштовувана затримка повтору вводу при утриманні клавіші (Steam).
- На мапі світу — рух між вузлами-рівнями (Cubed3 скаржиться, що лише по доріжках).

## Вікна, меню, HUD
- `main-menu` (?): Грати · Налаштування · Вихід.
- `map-window` / `world-map`: мапа вибору рівнів по світах (Forest/Grassland, Snow/Tundra, Desert); вузли рівнів + окремі гілки важчих рівнів.
- `game-screen`: кімната; HUD мінімальний — без лічильника ходів і таймера; підказки клавіш undo/restart/skip (?).
- `settings-window`: перепризначення клавіш, high-contrast, затримка повтору вводу, звук (?).
- `pause-menu` (?): Skip Level · Restart · вихід на мапу.
- Переходи: map-window → game-screen → (усі вазони в лунках, кактус розквітає) → map-window; Skip → map-window.

## Фічі поза полем
- `undo` (по кроку, ∞ (?)), `restart-level`, `skip-level` без ліміту й штрафу.
- `world-map` з трьома світами й важчими «вторинними» рівнями в кожній зоні (Cubed3) — `+hard-mode`.
- `remap-controls`, `high-contrast`, `+feature:input-repeat-delay`.
- 100+ рівнів, нові механіки в кожному світі; нема редактора, таблиць і сюжету (Wikipedia: критика GameGrin).

## Варіації й родичі
- Осі варіацій:
  - **тіло**: тягнеться за головою (Snake) / лише росте, не вкорочується (Room to Grow) / росте і вкорочується (Kine, `+extend-retract-body`);
  - **як рухається аватар**: крок (Sokoban) / ріст + віддача від стіни (Room to Grow) / падіння під гравітацією (Snakebird);
  - **що штовхає**: голова / все тіло при віддачі / обидва;
  - **кількість голів**: одна / кілька в одному тілі.
- Родичі: Snakebird і Hanano Puzzle (ріст, що штовхає — `+growth-push`), [sokoban](sokoban.md), [wriggle](wriggle.md) (тіло-ланцюг), [boxup](boxup.md); автор називає натхненням Baba Is You і The Witness.

## Цікавинки для курсу
- Ріст голови з тілом-множиною клітин без вкорочення + заборона перетину — 🌱.
- Віддача: ріст у стіну зсуває все тіло на 1 назад із поштовхом вазонів на шляху — 📎 (перевірка всього тіла як блока, ланцюг поштовхів).
- Sokoban-ціль «усі вазони в лунках» — 🌱 (картка `all-on-targets`).
- Багатоголовий кактус: ріст кількох голів за один ввід — 🥉 (порядок застосування і конфлікти голів).
- Розвʼязувач: BFS по станах (множина клітин тіла + вазони) з монотонно зростаючим тілом — 🥈; монотонність дає хороше відсікання.
- Undo/restart/skip як «жодної фрустрації» — 🌱.

## Мапа на каталог
- Є: `push-object` ↔ вазони; `all-on-targets` ↔ лунки; `self-collision` ↔ тіло не перетинає себе (варіант «блок»); `no-reverse-turn` ↔ не рости назад; `impassable-cells` ↔ стіни/живоплоти/діри сітки; `move-4dir` + `keyboard-controls` + `controls-remap`; `undo-redo` + `restart-level` + `skip-level`; `world-map` + `level-select` + `sequential-levels`.
- **Нема** → пропозиції карток:
  - `+grow-on-move` (Spybot) «Хід = ріст тіла» · entities/move · 🌱.
  - `+growth-push` (Hanano Puzzle) — ріст штовхає обʼєкти.
  - `+wall-recoil` «Упор у стіну зсуває все тіло назад» · entities/move · 📎 · слот {grows: bool}.
  - `+multi-head-body` «Тіло з кількома головами росту» · entities/move · 🥉.
  - `+hard-mode` — важчі рівні-гілки в кожній зоні.

## Пропозиції до словників
- `+feature:input-repeat-delay` — затримка автоповтору руху при утриманні клавіші (і в Pâquerette).
- `+feature:no-move-counter` — свідома відсутність лічильника ходів/таймера як дизайн-рішення (Steam: «No timer, no action elements, no move counter»).
- `+card:wall-recoil`, `+card:grow-on-move`, `+card:multi-head-body` — див. вище.

## Джерела
- ⭐ [Steam: Room to Grow](https://store.steampowered.com/app/1471960/) — «Growing enables you to move», «growing into walls shifts your whole body in the opposite direction», «push plants», 100+ пазлів, undo/restart/skip, доступність.
- [Wikipedia](https://en.wikipedia.org/wiki/Room_to_Grow_(video_game)) — видовження по сітці, ціль — сіре коло, порівняння зі Snake, кілька розвʼязків, критика відсутності таблиць і редактора.
- [GameGrin](https://www.gamegrin.com/reviews/room-to-grow-review) — 3 напрямки росту, без вкорочення, поштовх від краю збільшує тіло, світи Grassland/Tundra/Desert, багатоголові кактуси, сітки з дірами й нерівними сегментами, цілі поза сіткою.
- [GeekMom/GeekDad](https://geekdad.com/2021/03/geekmom-room-to-grow-a-deceptively-tricky-cactus-based-indie-puzzle-game/) — WASD/стрілки, Z/R, пропуск, два вазони на дві цілі, розквіт.
- [Cubed3](https://www.cubed3.com/games/reviews/pc/room-to-grow) — лунки, камінь у Forest, Snow-глава, мапа рівнів, Skip лише в рівні, важчі рівні.
- [Digitally Downloaded](https://www.digitallydownloaded.net/?p=41341) — 4 напрямки (з урахуванням заборони назад — 3), не перетинає себе, лише росте.
- YouTube: пошук «Room to Grow puzzle gameplay».

## Непевне
- (?) Чи голова штовхає вазон напряму (Sokoban-поштовх при рості), чи вазони рухаються лише від зсуву тіла — Steam каже тільки «use this to push plants».
- (?) Що буде, коли і ріст, і зсув тіла заблоковані — логічно `block`, джерелом не підтверджено.
- (?) Поведінка особливого каменю в Forest і механіки Snow/Tundra та Desert — назви світів відомі, механіки ні.
- (?) Як ростуть багатоголові кактуси (усі голови одночасно чи по черзі).
- (?) Чи вазон у лунці фіксується; чи undo без ліміту; меню паузи як окремий екран.
- (?) Розбіжність назв першого світу: Forest (Cubed3) vs Grassland (GameGrin).
