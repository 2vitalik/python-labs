---
title: SokoSolitaire
slug: sokosolitaire
aka: []
family: push-slide
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2023
platforms: [Windows, macOS, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2318680/", best: true, note: "опис: штовхати карти до місць призначення, складати в стопки, перевертати, міняти масть; 60 рівнів, нескінченний undo, пропуск рівня"}
  - {kind: other, url: "https://ladiesgamers.com/sokosolitaire-review/", note: "огляд: кіт штовхає карти, одноразові іконки зміни масті, стрілка-переворот, замок, undo/рестарт, лічильник кроків і лідерборд"}
  - {kind: other, url: "https://steamcommunity.com/app/2318680/reviews/?browsefilter=toprated&l=english", note: "відгуки: стопки за кольором без чергування, місця для стопок певного кольору, не штовхаєш дві карти разом"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=SokoSolitaire+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, all-on-targets, cell-transform, undo-unlimited, restart-level, skip-level, level-unlock, level-select, move-counter, leaderboard, achievements-window, +card-as-block, +suit-change-tile, +flip-tile, +color-stack-cell, +optional-step-counter]
proposes: ["+cond:face_up", "+effect:flip", "+effect:stack", "+card:card-as-block", "+card:suit-change-tile", "+card:flip-tile", "+card:color-stack-cell"]
author: opus
date: 2026-11-09
---

# SokoSolitaire — Sokoban з гральних карт: кіт штовхає карти на місця, по дорозі перевертаючи, перефарбовуючи й складаючи їх у стопки

## Суть
Ящики Sokoban замінено гральними картами з мастю/кольором і лицем-сорочкою. Кіт штовхає карти по кімнаті до місць призначення, але місце приймає лише карту потрібної масті/кольору, тож карту часто треба спершу **перевернути** (клітина зі стрілкою) і **перефарбувати** (одноразова іконка масті). Окремі клітини дозволяють **складати карти в стопку** — лише свого кольору, без пасьянсного чергування. Нова механіка зʼявляється кожні кілька рівнів; за відгуками, ядро — саме Sokoban-рух, а пасьянсу небагато.

## Поле і час
- Квадратна сітка кімнати; один екран на рівень (?).
- Шари: підлога + спецклітини (місця призначення, переворот, зміна масті, стопка, замок) + карти + стіни.
- Хід = крок кота; без вводу нічого не рухається (Steam: «Playable without Timed Input»); таймера нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кіт | player | — | рух 4 напрямки; штовхає одну карту |
| Карта | object | масть/колір (червоний/чорний), лицем / сорочкою | зсувається на 1 від поштовху; дві карти підряд не штовхаються |
| Місце призначення | zone | потрібна масть/колір | приймає карту відповідної масті |
| Клітина перевороту (стрілка за годинниковою) | terrain | — | карта, що проїхала, перевертається |
| Іконка зміни масті | terrain | масть, одноразова | карта набуває масті іконки; іконка зникає навіть при збігу кольору |
| Місце для стопки | zone | колір (або будь-який) (?) | на нього можна складати карти лише свого кольору |
| Замок | gate | — | захаращує кімнату; зникає, коли пазл розвʼязано (?) |
| Стіна | static | — | непрохідна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(cat, dir)`, `counter(steps, +1)`.
- КОЛИ `contact(cat, card)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `contact(cat, card)` → ЯКЩО `occupied(cell_behind, card)` → ТО `block` (ланцюг карт не штовхається).
- КОЛИ `enter(card, flip_tile)` → ТО `set_state(card, flipped)` — `custom: «лицем ↔ сорочкою»`.
- КОЛИ `enter(card, suit_icon)` → ТО `set_value(card, icon_suit)`, `disappear_b` (іконка одноразова).
- КОЛИ `enter(card, stack_cell)` → ЯКЩО `same(card, stack_cell, color)` → ТО `custom: «карта лягає в стопку»`; інакше `block` (?).
- КОЛИ `enter(card, destination)` → ЯКЩО `same(card, destination, suit)` і `state(card, face_up)` (?) → ТО `custom: «карта зарахована»`.
- КОЛИ `all_on(card, destination)` → ТО `win`, `custom: «замок падає»` (?), `next_level`.
- КОЛИ `input(undo)` → ТО `undo(1)` (без ліміту); КОЛИ `input(restart)` → ТО `restart`.
- КОЛИ `input(skip)` → ТО `next_level` (рівень пропущено).
- Перемога: усі карти на своїх місцях. · Поразка: нема; глухий кут → undo. · Рахунок: опційно кроки → онлайн-лідерборд рівня.

## Керування і ввід
- Стрілки / D-pad — крок кота; кнопки undo, рестарт, пропуск рівня.
- Steam: повна підтримка контролера, «Keyboard Only Option»; «delightfully simple controls» (огляд).
- Перші рівні показують підказки про undo і рестарт.

## Вікна, меню, HUD
- `main-menu` → `level-select`: набори рівнів, які можна відкривати будь-коли без штрафу.
- `game-screen`: кімната з картами; HUD — `move-counter` (якщо ввімкнено), кнопки undo/рестарт.
- `leaderboard` — найменше кроків на рівні (Steam Leaderboards).
- `settings-window`: режим для дальтоніків (Trichromatic / Dichromatic / Monochromatic), гучність, лічильник кроків увімк./вимк.
- `achievements-window` (8); `tutorial-window`-підказки в перших рівнях.

## Фічі поза полем
- `puzzle-bank` на 60 рівнів; `level-unlock` наборами в будь-який момент; `skip-level`.
- `undo` без ліміту + `restart-level`.
- `+optional-step-counter`: лічильник кроків вмикається для челенджу й іде в `leaderboard-online`.
- `colorblind-palette` (3 режими), `gamepad-support`, `cloud-save`, Remote Play on TV, 7 мов.

## Варіації й родичі
- Серія Daisy's Puzzlers (Daisy Games) — інші сокобан-пазли того ж автора; збірка «Daisy's Sokoban Collection» (?).
- Родичі: [sokoban](sokoban.md) — ядро; [e9uations](e9uations.md) — блоки з символами/значеннями, які треба зібрати в правильне; `cell-transform`-клітини (Chip's Challenge) — тут вони одноразові.
- Осі варіацій:
  - **що несе ящик**: нічого (Sokoban) / колір / масть + лице/сорочка (SokoSolitaire) / цифру чи знак (рівняння);
  - **як змінюється ящик**: ніяк / клітиною-перетворювачем (багаторазово) / одноразовою іконкою (SokoSolitaire);
  - **місткість клітини**: один ящик / стопка за правилом кольору.

## Цікавинки для курсу
- Карта як ящик зі станом (масть, лице) і перевірка цілі за властивістю — 🌱.
- Одноразова клітина-перетворювач, яку треба врахувати в undo — 📎.
- Клітина-стопка з правилом допуску (колір) — 📎.
- Онлайн-лідерборд мінімуму кроків на рівень — 🥉 (або локальний — 📎).
- Розвʼязувач: стан = кіт + карти з властивостями + використані іконки — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object`; `impassable-cells`; `all-on-targets` ↔ карти на місцях; `cell-transform` ↔ переворот і зміна масті; `undo-unlimited` + `restart-level`; `skip-level`; `level-unlock` + `level-select`; `move-counter` + `leaderboard`; `achievements-window`.
- **Нема** → пропозиції карток:
  - `+card-as-block` «Ящик-карта з мастю й лицем; ціль перевіряє властивість» · entities/state · 🌱.
  - `+suit-change-tile` «Одноразова клітина задає властивість ящика» · entities/interact · 📎.
  - `+flip-tile` «Клітина перевертає ящик (лице ↔ сорочка)» · entities/interact · 🌱.
  - `+color-stack-cell` «Клітина-стопка, що приймає ящики свого кольору» · entities/legality · 📎.
  - `+optional-step-counter` «Лічильник кроків вмикається за бажанням» · interface/hud · 🌱.

## Пропозиції до словників
- `+cond:face_up` — карта лежить лицем догори.
- `+effect:flip` — перевернути обʼєкт (лице ↔ сорочка), не поворот на кут.
- `+effect:stack` — покласти обʼєкт поверх іншого в тій самій клітині.
- `+card:card-as-block`, `+card:suit-change-tile`, `+card:flip-tile`, `+card:color-stack-cell`.

## Джерела
- ⭐ [Steam: SokoSolitaire](https://store.steampowered.com/app/2318680/) — «push all the cards to their destination», стопки, переворот, зміна масті, 60 рівнів, нескінченний undo, пропуск рівня, 3 режими для дальтоніків; реліз 03.08.2023, Daisy Games / Martin Games.
- [LadiesGamers: огляд](https://ladiesgamers.com/sokosolitaire-review/) — кіт, одноразові іконки масті, стрілка перевороту, замок, undo/рестарт, опційний лічильник кроків з онлайн-лідербордом, набори рівнів відкриваються будь-коли.
- [Steam-відгуки](https://steamcommunity.com/app/2318680/reviews/?browsefilter=toprated&l=english) — «you don't have to alternate colors when stacking», стопки певного кольору, «can't push multiple back-to-back items», лідерборд за мінімумом ходів.
- YouTube: пошук «SokoSolitaire gameplay».

## Непевне
- (?) Чи має значення номінал карти (король, дама на скріншотах) — жодне джерело не згадує правило за значенням.
- (?) Стопка: лише на спеціальних клітинах чи будь-яка карта на будь-яку; що буває при невідповідному кольорі.
- (?) Чи місце призначення вимагає карту лицем догори і чи враховує масть чи лише колір («suits differ only by color» у відгуках).
- (?) Роль замка — огляд каже лише, що він «падає», коли пазл розвʼязано.
- (?) Скільки пропусків рівнів дозволено; чи є екран рівня з мінімумом кроків.
