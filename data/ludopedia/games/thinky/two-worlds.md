---
title: Two Worlds
slug: two-worlds
aka: []
family: thinky
also: [push-slide, grid-platformer]
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
  - {kind: itch, url: "https://nebu-soku.itch.io/two-worlds", best: true, note: "грати в браузері; «a sokoban-like where you have to create an environment for the inner world from the outer world»; натхнення Ice Path, Ahoist Cratey, The Golem, YAPP2"}
  - {kind: other, url: "https://www.puzzlescript.net/editor.html?hack=fc724eb147fef6888222db429ca68fcd", note: "PuzzleScript-сирці v1.6: два світи зі зсувом 19 клітин, повітря = фіолетова зона + ящики, лазіння на 1, жорсткі ящики-групи"}
  - {kind: youtube, url: "https://youtu.be/NpoHaOetxSA", note: "проходження від автора (лінк зі сторінки itch)"}
  - {kind: other, url: "https://nebu-soku.itch.io/two-worlds/devlog", note: "девлог v1.1–v1.6 (липень–серпень 2021): виправлення рівнів 13–14, необовʼязкові цілі"}
stage: v1
coverage: 70
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, gravity-fall, party-switch, multi-cell-size, carrier-platform, reach-exit, undo-redo, undo-unlimited, restart-level, sequential-levels, level-from-txt, tutorial-window, movement-animation, event-effects, sound-effects, +linked-worlds, +perspective-switch, +freeze-inactive, +step-climb-1, +ghost-projection, +optional-challenges]
proposes: ["+effect:sync_world", "+role:ghost", "+axis:gravity-per-mode", "+card:linked-worlds", "+card:ghost-projection"]
author: opus
date: 2026-11-19
---

# Two Worlds — сокобан згори вирізає печеру внутрішнього світу, де компаньйон-платформер іде до серця

## Суть
PuzzleScript-гра з двома героями й двома полями однакового розміру. Синій ходить зовнішнім світом згори й штовхає ящики; рожевий живе у внутрішньому світі збоку — з гравітацією, лазінням на одну клітину й блоками. Світи зшиті клітина-в-клітину: фіолетова зона зовні — це печера всередині, а кожен ящик зовні вирізає ще одну клітину повітря в скелі внутрішнього світу. Гравець перемикає героїв (X / пробіл), будуючи ящиками рельєф, яким рожевий дійде до серця.

## Поле і час
- Рівень — одна карта 38×16: ліва половина (19×16) — зовнішній світ згори, права — внутрішній світ збоку; клітина (x, y) зовні відповідає (x+19, y) всередині. `flickscreen 19x16` — на екрані лише світ активного героя.
- Зовнішній світ: підлога, стіни, ящики 1×1, «жорсткі» ящики-групи (кілька клітин рухаються разом), фіолетова зона — контур печери.
- Внутрішній світ: скеля (тверда), повітря, блоки, серце-ціль, малі серця; гравітація вниз — лише тут.
- Хід = крок активного героя; падіння й анімації — додаткові кроки `again` (0.05 с); `realtime_interval` — лише анімація привидів. `time: turn`.
- 17 рівнів: 3 навчальні («Reach the heart to win.», «You can climb one square.», «You can only push one block at a time.») і 14 названих — від «1. Two Worlds» до «13. An Elevator That Allows 0 People» і «14. 3 x 21».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Синій | player | активний / застиглий | крок 4 напрямки згори; штовхає ящики |
| Рожевий | player | активний / застиглий; падає | ходить ліворуч / праворуч, лізе на 1, штовхає один блок, падає без опори |
| Ящик | object | 1×1 | штовхається синім; його клітина всередині стає повітрям |
| Жорсткий ящик | object | група клітин | рухається цілою групою; везе блоки, що лежать у його повітрі («ліфт») |
| Фіолетова зона | static | — | зовні непрохідна для синього й ящиків; всередині — постійне повітря |
| Стіна | static | — | непрохідна зовні; всередині — скеля |
| Скеля | terrain | — | на ній стоять; поруч із повітрям — сходинка висотою 1 |
| Блок | object | — | рожевий штовхає по одному; падає; на ньому стоять і лізуть |
| Привид рожевого / блока / серця | mark | — | показ внутрішнього стану в зовнішньому світі |
| Серце | zone | — | ціль: рожевий стоїть на ньому з опорою |
| Мале серце | pickup | — | необовʼязкова ціль (рівні 13–14 з v1.5) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(blue, dir)`; стіни й фіолетова зона непрохідні.
- КОЛИ `contact(blue, crate)` → ЯКЩО `free(cell_behind)` → ТО `push(crate)`, `move(blue, dir)`; інакше `block` (у фіолетову зону ящик не заходить).
- КОЛИ `contact(blue, crate)` → ЯКЩО `occupied(crate_cell, ghost_pink)` → ТО `block`, `sound(boo)` — повітря, в якому стоїть рожевий, не зрушити.
- КОЛИ `contact(blue, rigid_crate)` → ЯКЩО `custom: «уся група може зсунутись і в ній нема привида рожевого»` → ТО `push(rigid_crate)` цілою групою, `carry(ghost_block)` — блоки в її повітрі їдуть разом.
- КОЛИ `input(action)` → ЯКЩО `state(blue, active)` → ТО `set_state(blue, frozen)`, `clear_state(pink, frozen)`, `camera(inner_world)`; назад — так само, якщо рожевий не падає.
- КОЛИ `turn_end(blue)` → ТО `set_cell(inner_cell, rock)` там, де зовні нема ні фіолетової зони, ні ящика.
- КОЛИ `state_on(pink, active)` → ТО `set_cell(inner_cell, air)` під кожним ящиком, `spawn_at(ghost_pink, outer_cell)`, `spawn_at(ghost_block, outer_cell)`.
- КОЛИ `state_on(blue, active)` → ТО `custom: «блоки внутрішнього світу стають на місця своїх привидів»`.
- КОЛИ `input(dir)` → ЯКЩО `state(pink, active)` → ТО `move(pink, dir)` лише ліворуч / праворуч; хід угору — `block` (стрибка нема).
- КОЛИ `input(dir)` → ЯКЩО `custom: «попереду скеля або блок висотою 1, а над ними повітря»` → ТО `move(pink, up)`, `move(pink, dir)` — заліз на сходинку.
- КОЛИ `turn_end(pink)` → ЯКЩО `not supported(pink)` → ТО `fall(pink)`.
- КОЛИ `contact(pink, block)` → ЯКЩО `free(cell_behind)` → ТО `push(block)`; два блоки поспіль або блок під скелею — сходинка, на яку лізуть.
- КОЛИ `turn_end(pink)` → ЯКЩО `not supported(block)` → ТО `fall(block)`; поки блок падає, рожевий стоїть.
- КОЛИ `enter(pink, heart)` → ЯКЩО `supported(pink)` → ТО `win`, `next_level`.
- КОЛИ `enter(pink, small_heart)` → ЯКЩО `supported(pink)` → ТО `disappear(small_heart)` — необовʼязкова ціль.
- КОЛИ `input(undo)` → ТО `undo`.
- КОЛИ `input(restart)` → ТО `restart`.
- Перемога: рожевий стоїть на серці з опорою. · Поразки нема: застряг — undo / рестарт. · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок активного героя (рожевий — лише ←/→).
- X або пробіл — перемкнути героя (екран «шторкою» переходить в інший світ).
- Z — undo, R — рестарт (стандарт PuzzleScript).
- Навчальний прийом рівня 1: щойно ящик стає на позначку, гра на мить блокує синього й пише «X or spacebar to switch characters.»

## Вікна, меню, HUD
- `main-menu` PuzzleScript: «Two Worlds(v1.6)» by nebu soku.
- `tutorial-window`: повідомлення перед рівнями — навчальні тексти й назви 14 рівнів; фінал «Thanks for playing!».
- `game-screen`: половина карти активного героя; анімація переходу при перемиканні й на старті рівня; у зовнішньому світі — привиди рожевого, блоків і серця. HUD нема.
- Переходи: меню → рівень → (серце) повідомлення з назвою → наступний рівень → … → «Thanks for playing!».

## Фічі поза полем
- `undo` і `restart-level` PuzzleScript; рівні строго по черзі.
- Оновлення v1.1–v1.6 (30.07–25.08.2021): правки рівнів 13–14, у v1.5 — необовʼязкові цілі (малі серця), у v1.6 — проходження на YouTube.
- Редактора нема (питання в коментарях без відповіді); статус itch — «In development».

## Варіації й родичі
- Натхнення (за сторінкою): [Ice Path](ice-path.md) — рівень, який сам будуєш; [Ahoist Cratey](../grid-platformer/ahoist-cratey.md) — ящики в платформері з лазінням на 1; The Golem (Dom Camus); YAPP2 (Artless Games).
- Родичі: [Toodee and Topdee](toodee-and-topdee.md) — те саме поле то збоку, то згори; тут — два різні поля, зшиті відображенням. Інша гра автора — [Magicube](../grid-platformer/magicube.md).
- **Осі варіацій**: звʼязок світів — одне поле у двох проєкціях (Toodee) / один світ задає рельєф іншого (Two Worlds) · що несе ящик у другий світ — повітря (тут) / твердь · перенесення між світами — немає / блоки їдуть у повітрі жорсткого ящика («ліфт», але без людей).

## Цікавинки для курсу
- Два поля, зшиті зсувом клітин, і перерахунок рельєфу при перемиканні — 📎.
- Платформер на сітці: падіння, лазіння на 1, штовхання одного блока — 🥉.
- Привиди: проєкція стану іншого світу й заборона рухати повітря під компаньйоном — 📎.
- Жорсткі ящики-групи, що везуть блоки, — 🥉 (рух групи з перевіркою всіх клітин).
- Перемикання героя з застиганням і переходом екрана — 🌱.
- Розвʼязувач BFS по станах обох світів (герої, ящики, блоки, хто активний) — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls`; `push-object` ↔ ящики зовні й блоки всередині; `impassable-cells` ↔ стіни, фіолетова зона, скеля; `gravity-fall` ↔ рожевий і блоки; `party-switch` ↔ X / пробіл; `multi-cell-size` ↔ жорсткі ящики; `carrier-platform` ↔ жорсткий ящик везе блок; `reach-exit` ↔ серце; `undo-redo` · `undo-unlimited` · `restart-level`; `sequential-levels`; `level-from-txt`; `tutorial-window` ↔ повідомлення; `movement-animation` · `event-effects` ↔ анімації кроку, переходу, перемоги; `sound-effects`.
- **Нема** → пропозиції карток:
  - `+linked-worlds` «Два поля, зшиті відображенням: обʼєкти одного задають рельєф іншого» · entities/state · 🥈 · слот {offset}.
  - `+ghost-projection` «Привиди: позиції обʼєктів іншого світу» · interface/hud · 📎.
  - Уже в корпусі: `+perspective-switch` і `+freeze-inactive` (Toodee and Topdee), `+step-climb-1` (лазіння на 1), `+optional-challenges` (малі серця).

## Пропозиції до словників
- `+effect:sync_world` — перерахувати клітини одного поля з другого (ящик → повітря, підлога → скеля).
- `+role:ghost` — проєкція сутності з іншого поля: без власної поведінки, лише показ і заборони.
- `+axis:gravity-per-mode` — гравітація лише в одному з режимів / світів (уже пропоновано в toodee-and-topdee.md).
- `+card:linked-worlds`, `+card:ghost-projection` — див. вище.

## Джерела
- ⭐ [itch.io: Two Worlds](https://nebu-soku.itch.io/two-worlds) — опис, натхнення, теги (Puzzle-Platformer, PuzzleScript, Sokoban), коментарі (рівень 2 важкий, 13–14 «ніхто не мав розвʼязати»), девлог.
- [Сирці v1.6 у редакторі PuzzleScript](https://www.puzzlescript.net/editor.html?hack=fc724eb147fef6888222db429ca68fcd) — gist Nebu-Soku від 25.08.2021: OBJECTS / LEGEND / RULES (відображення на 19 клітин, повітря під ящиками, лазіння, падіння, жорсткі групи, привиди, перемикання), 17 рівнів з назвами.
- [Проходження від автора](https://youtu.be/NpoHaOetxSA) — відео з v1.6 (не дивився, лінк зі сторінки).
- [Девлог](https://nebu-soku.itch.io/two-worlds/devlog) — версії 1.1–1.6.

## Непевне
- (?) Клавіші undo / restart автор не називає — стандарт PuzzleScript (Z, R).
- (?) Чи може синій штовхати привид блока, що стоїть поза фіолетовою зоною (правило в сирцях є, коли воно спрацьовує в рівнях — не перевірено).
- (?) Точні форми жорстких ящиків (у коментарях — блок 2×3; назви «3 x 6», «3 x 21») не виписував.
- (?) Малі серця прибирають свій привид і на перемогу не впливають; чи гра їх десь враховує — не знайшов.
