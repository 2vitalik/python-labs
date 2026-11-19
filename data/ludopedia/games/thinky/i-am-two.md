---
title: I am Two
slug: i-am-two
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [web]
links:
  - {kind: itch, url: "https://nebu-soku.itch.io/i-am-two", best: true, note: "грати в браузері; опис авторки: X ставить клона, друге X — «стати» клоном; 8 рівнів, PuzzleScript"}
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=25ee2f1c9000620aa7b6f429c958d095", note: "виправлена копія на puzzlescript.net (increpare, грудень 2024)"}
  - {kind: other, url: "https://gist.github.com/25ee2f1c9000620aa7b6f429c958d095", note: "вихідний код PuzzleScript: клон, синя й жовта кулі, умова перемоги, 8 рівнів"}
  - {kind: other, url: "https://github.com/increpare/PuzzleScript/issues/1044", note: "«i am two broken»: у новому рушії зʼявлялось два клони; виправлення правил"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=I+am+Two+nebu+soku+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, inertia-slide, impassable-cells, all-on-targets, undo-unlimited, restart-level, sequential-levels, spawn-animation, facing-icon, sound-effects, +recall-to-checkpoint, +input-lock, +clone-anchor]
proposes: ["+card:clone-anchor", "+window:title-screen", "+window:message-screen"]
author: opus
date: 2026-11-19
---

# I am Two — Sokoban, де X ставить двійника-стопора, а друге X переносить тебе на його місце

## Суть
Коротка PuzzleScript-головоломка nebu soku: персонаж штовхає кулі на фіолетові цілі. Головне дієслово — клон: X ставить двійника там, де стоїш; щойно відходиш, він стає твердою перешкодою для куль і для тебе. Друге X — «стати клоном»: персонаж зникає зі свого місця й опиняється на місці двійника, а двійник зникає. Синя куля штовхається на одну клітину, жовта після поштовху ковзає до першої перешкоди — і клон слугує їй стопором. Мета — кожна ціль накрита кулею; 8 рівнів.

## Поле і час
- Квадратна сітка 13×10 з рамкою порожнечі; кімната всередині — до 10 клітин завширшки разом зі стінами. Стіни мають псевдо-3D декор (грані, тіні) — лише вигляд.
- Хід = крок або натискання X; без вводу світ стоїть. Анімації (поява, ходьба, ковзання жовтої кулі) програються тіками реального часу (`realtime_interval 0.2`): поки жовта куля їде, персонаж «заморожений».
- Шари: тло · ціль · клон · (персонаж, стіни, кулі) · декор стін · анімації.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж | player | дивиться ліворуч/праворуч; позначка «клон є» | крок у 4 напрямки, спрайт повертається за горизонтальним рухом (3 кадри ходьби); штовхає кулі; X — клон |
| Клон (двійник) | object | орієнтація персонажа в момент постановки; не більше 1 | стоїть; коли персонаж зійде з його клітини — тверда перешкода й стопор для жовтої кулі |
| Синя куля | object | — | зсувається на 1, якщо за нею вільно; ланцюгом не штовхається |
| Жовта куля | object | стан «їде» + напрям | після поштовху ковзає до першої стіни, кулі чи клона |
| Ціль | static | — | фіолетова плитка; кулі й персонаж проходять над нею, ковзання вона не зупиняє |
| Стіна | static | — | непрохідна для всього |
| Точка появи | spawner | 3 кадри | на старті рівня «проявляє» персонажа |
| Порожнеча | static | — | чорне тло поза кімнатою |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `spawn_at(player, P)` — за 3 тіки анімації появи.
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`, `face(player, left|right)`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(next_cell, wall|clone)` → ТО `block`.
- КОЛИ `contact(player, blue_orb)` → ЯКЩО `free(cell_behind)` → ТО `push(blue_orb)`; інакше `block` (дві кулі підряд не штовхаються).
- КОЛИ `contact(player, yellow_orb)` → ЯКЩО `free(cell_behind)` → ТО `push(yellow_orb)`, `set_state(player, frozen)`, `slide(yellow_orb, dir)`; інакше `block`.
- КОЛИ `blocked(yellow_orb)` → ТО `clear_state(player, frozen)` — куля стала звичайною, персонаж знову ходить.
- Жовта куля проїжджає ціль: щоб лишити її на цілі, за ціллю має стояти стіна, інша куля або клон.
- КОЛИ `input(action)` → ЯКЩО `count(clone, ==, 0)` → ТО `clone(player)`, `sound(sfx0)` — двійник у клітині персонажа.
- КОЛИ `leave(player, clone)` → ТО `set_state(clone, solid)` — перешкода для персонажа, синіх і жовтих куль.
- КОЛИ `input(action)` → ЯКЩО `count(clone, ==, 1)` і `not occupied(player_cell, clone)` → ТО `teleport(player, clone)`, `disappear(clone)`, `face(player, clone_facing)`, `sound(sfx1)` — на старому місці лишається відблиск на один тік.
- КОЛИ `input(action)` → ЯКЩО `state(player, frozen)` → ТО `block` (поки куля їде, ні кроку, ні клона).
- КОЛИ `all_on(orb, target)` → ТО `win`, `next_level` (синя й жовта рахуються однаково).
- Перемога: на кожній цілі стоїть куля. · Поразки нема (глухий кут → undo або рестарт). · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок або поштовх; X — поставити клона / перейти на нього.
- Z — undo, R — рестарт (стандарт PuzzleScript); на itch вказано лише клавіатуру.

## Вікна, меню, HUD
- `title-screen` (custom, стандарт PuzzleScript): назва «I am Two», автор, старт.
- `message-screen` (custom): «X to put a clone.», «Again X to be replaced with the clone.», «Level N of 8» перед кожним рівнем; фінал «Thanks for playing!».
- `game-screen`: кімната без HUD; номер рівня — лише в повідомленні перед ним.
- Переходи: title → повідомлення → рівень → повідомлення → … → фінальне повідомлення.

## Фічі поза полем
- `undo` ∞ і `restart-level` (рушій PuzzleScript); `levels-sequential`: 8 рівнів, сесія близько пів години (itch).
- Звук на кожну подію: крок, рух кулі, клон, перехід на клона, рестарт, undo, старт і кінець рівня.
- Відкритий код; копію на puzzlescript.net increpare виправив, коли новий рушій почав ставити двох клонів.

## Варіації й родичі
- Нове для корпусу: клон не повторює ходів (`thinky/loophole.md`, `thinky/recopy.md`, `grid-platformer/clony.md`), а є **закладкою позиції**, яка ще й тверда.
- Інші ігри авторки: `grid-platformer/magicube.md` («блок, що зникає»), Two Worlds (у черзі thinky), Sokoban-варіації на itch (The elephant in her room, DOKU no HANA).
- Родичі: `push-slide/sokoban.md` (синя куля), `push-slide/pengo.md` (блок ковзає до упору), Diamond Rush (`+recall-to-checkpoint`).
- **Осі варіацій**: друге натискання — перенести на клона (тут) / обмін місцями / клон повторює записані ходи; клон — тверда перешкода / привид; клонів — 1 / N; куля — на 1 клітину / до упору.

## Цікавинки для курсу
- Клон-закладка: позиція клона як стіна у перевірці «вільно» + перенесення по X — 🌱 (одна змінна стану).
- Жовта куля ковзає по тіках, а ввід заблоковано до зупинки — 📎 (анімація як стан гри).
- Ціль не зупиняє ковзання: перемога, лише коли куля зупинилась на цілі — 🌱.
- BFS-розвʼязувач: стан = персонаж + клон (є/нема, де) + кулі; X подвоює гілки — 🥉.
- Баг двох клонів у новому рушії (issue #1044) як вправа «тести на рівнях-фікстурах ловлять зміну порядку правил» — 📎.

## Мапа на каталог
- Є: `move-4dir` + `move-by-input` ↔ крок; `push-object` ↔ синя куля; `inertia-slide` ↔ жовта куля; `impassable-cells` ↔ стіни й клон; `all-on-targets` ↔ мета; `undo-unlimited` + `restart-level`; `sequential-levels` ↔ 8 рівнів; `spawn-animation` ↔ поява; `facing-icon` ↔ спрайт ліворуч/праворуч; `sound-effects`; `keyboard-controls`.
- Уже пропоновані іншими: `+recall-to-checkpoint` (Diamond Rush) ↔ друге X; `+input-lock` (Memory) ↔ персонаж чекає, поки куля їде.
- **Нема** → пропозиції карток:
  - `+clone-anchor` «Двійник-закладка: X ставить, друге X переносить на нього; двійник — тверда перешкода» · entities/spawn · 🌱 · слот {max: 1, solid: bool}.

## Пропозиції до словників
- `+card:clone-anchor` — механіки нема в каталозі.
- `+window:title-screen` — стандартний титул PuzzleScript (назва, автор, старт).
- `+window:message-screen` — текстовий екран між рівнями PuzzleScript (навчання, «Level N of 8», фінал).

## Джерела
- ⭐ [itch: I am Two](https://nebu-soku.itch.io/i-am-two) — грати; опис («You can put a clone and be replaced with it»), 8 рівнів, PuzzleScript, теги Sokoban; коментарі з березня 2021.
- [Код у gist](https://gist.github.com/25ee2f1c9000620aa7b6f429c958d095) — правила клона й відблиску, синя й жовта кулі, ковзання, «All Target on Orb», повідомлення рівнів.
- [puzzlescript.net](https://www.puzzlescript.net/play.html?p=25ee2f1c9000620aa7b6f429c958d095) — грати виправлену версію.
- [GitHub issue #1044](https://github.com/increpare/PuzzleScript/issues/1044) — «up x right x right» давало двох клонів у редакторі; правила виправлено, issue закрито 23.01.2025.
- YouTube: пошук «I am Two nebu soku puzzlescript».

## Непевне
- (?) Рік: найраніші коментарі на itch — 7.03.2021; у черзі стоїть 2024 — це рік виправленої копії increpare.
- (?) Чи itch-версія відрізняється від виправленої копії чимось, крім правила `ClonedCol`, — грав лише за кодом.
- (?) Тач-керування, Esc-меню й пункт continue — стандарт рушія PuzzleScript, на сторінці гри не описані.
- (?) Обʼєкт `Hall` (легенда `~`) є в коді, але в жодному рівні не вжитий.
