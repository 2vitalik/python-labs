---
title: Magic Chalkboards
slug: magic-chalkboards
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: nested
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2023
platforms: [web, mobile]
links:
  - {kind: itch, url: "https://coolnico.itch.io/magic-chalkboards", best: true, note: "грати в браузері; керування ПК і мобільне, коментарі з ROT13-підказкою"}
  - {kind: other, url: "https://www.puzzlescript.net/editor.html?hack=968f998f4c2a366ba196a81d7597c2a4", note: "сирці PuzzleScript (посилання зі сторінки гри)"}
  - {kind: other, url: "https://itch.io/jam/thinky-puzzle-game-jam-3/rate/2142455", note: "сторінка на Thinky Puzzle Game Jam 3"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Magic+Chalkboards+puzzlescript+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, move-by-input, keyboard-controls, swipe-gestures, push-object, impassable-cells, all-on-targets, item-pickup, undo-unlimited, restart-level, sequential-levels, sound-effects, tutorial-window, +draw-to-spawn, +sub-grid-canvas, +glyph-recognition, +ink-budget, +merge-drawings, +simultaneous-avatars]
proposes: ["+cond:shape_match", "+effect:draw", "+trigger:mode_toggle", "+role:canvas", "+ui:ink-meter", "+card:draw-to-spawn", "+card:sub-grid-canvas", "+card:glyph-recognition", "+card:ink-budget", "+card:merge-drawings", "+card:simultaneous-avatars"]
author: opus
date: 2026-11-09
---

# Magic Chalkboards — Sokoban, де бракує ящика: зайди в дошку, намалюй його крейдою 5×5 — і він стане справжнім

## Суть
PuzzleScript-Sokoban з видом згори: ящики треба поставити на цілі. Особливість — **магічні дошки**: штовхнувши дошку, гравець «входить» у неї й малює курсором на сітці 5×5 усередині однієї клітини. Якщо малюнок збігся з одним із гліфів (ящик, ціль, ящик-на-цілі, чоловічок), дошка перетворюється на цю сутність; інакше лишається рухомим «каракулем», який можна штовхати й доклеювати до інших каракулів. Крейди обмежено. Розвʼязки часто з «панчлайном»: найсильніший гліф — **намалювати себе**, отримавши другого аватара, що ходить синхронно.

## Поле і час
- Квадратна сітка рівня; кожна клітина-дошка має власну вкладену сітку 5×5 пікселів крейди (`field: nested`).
- Шари: фон → цілі → персонаж(і) → дошки й каракулі → стіни з обводкою → ящики й крейда-бонус → лічильник крейди (вбудований у стіну) → 25 шарів пікселів крейди → курсор.
- Хід = натискання; `norepeat_action` — затиснута дія не повторюється.
- Два режими вводу: рух персонажа по рівню / рух курсора по дошці.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж | player | — | рух 4 напрямки; штовхає один штовхуваний обʼєкт; кілька персонажів ходять одночасно |
| Ящик | object | — | штовхається, якщо за ним вільно |
| Ціль | zone | — | має бути покрита ящиком |
| Стіна | static | — | непрохідна |
| Магічна дошка | static | 5×5 пікселів | непрохідна; штовхнути = увійти в режим малювання (якщо є крейда) |
| Курсор | player | позиція 5×5, старт у центрі | ходить у межах дошки; за краєм — хід скасовано |
| Піксель крейди | mark | одна з 25 позицій | лишається там, де курсор ходив у режимі малювання |
| Каракуль | object | набір пікселів | дошка, малювання на якій зупинили без збігу; штовхається; втиснутий в інший каракуль — зливається з ним |
| Крейда-бонус | pickup | +8 | персонаж наступає — додає крейду |
| Лічильник крейди | static | 0–25 + подовження смуги | смуга в стіні, −1 за кожен хід малювання |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(character, dir)` для **кожного** персонажа.
- КОЛИ `contact(character, pushable)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block` (лише один обʼєкт, без ланцюга).
- КОЛИ `contact(character, extra_chalk)` → ТО `pickup`, `counter(chalk, +8)`.
- КОЛИ `contact(character, chalkboard)` → ЯКЩО `has(player, chalk)` → ТО `custom: «персонаж лишається на місці, керування переходить на курсор у центрі 5×5 дошки»`.
- КОЛИ `input(dir)` (на дошці) → ЯКЩО `custom: «курсор не на краю 5×5»` → ТО `move(pointer, dir)`; на краю — `block`.
- КОЛИ `input(x)` (на дошці) → ЯКЩО `not state(board, drawing)` → ТО `set_state(board, drawing)`.
- КОЛИ `input` → ЯКЩО `state(board, drawing)` → ТО `mark(pointer_pixel, chalk)`, `counter(chalk, -1)`.
- КОЛИ `after(mark)` → ЯКЩО `custom: «пікселі клітини збігаються з гліфом чоловічка»` → ТО `transform(character)`, керування повертається, новий персонаж теж керований.
- КОЛИ `after(mark)` → ЯКЩО `custom: «збіг із гліфом квадрата-рамки»` → ТО `transform(crate)`; гліф кільця 3×3 → `transform(target)`; суцільний квадрат з діркою в центрі → `transform(crate_on_target)`.
- КОЛИ `input(x)` → ЯКЩО `state(board, drawing)` → ТО `transform(scribble)`, повернення до персонажа.
- КОЛИ `counter(chalk, =, 0)` → ЯКЩО `state(board, drawing)` → ТО `transform(scribble)` (крейда скінчилась).
- КОЛИ `contact(character, scribble)` → ЯКЩО `occupied(cell_behind, scribble)` → ТО `custom: «пікселі першого каракуля переходять у другий (обʼєднання), перший зникає»`; далі перевірка гліфів (так каракулі-половинки з рівня складаються в ящик чи ціль).
- КОЛИ `all_on(crate, target)` → ЯКЩО `count(target, >, 0)` → ТО `win`, `next_level`.
- КОЛИ `input(z)` → ТО `custom: «undo»`; `input(r)` → `restart`.
- Перемога: усі цілі під ящиками. · Поразка: нема; бракує крейди — undo/restart. · Рахунку нема.

## Керування і ввід
- ПК: стрілки — рух персонажа або курсора; X біля дошки після поштовху — почати малювати, X ще раз — зупинити; Z — undo; R — рестарт.
- Мобільні: свайп — рух; тап — почати/зупинити малювання; згорнуте меню вгорі з Undo і Restart.
- Режим «малювання» = окремий режим вводу без перемикача: увійти — штовхнути дошку, вийти — X або збіг гліфа.

## Вікна, меню, HUD
- `splash-screen` — титул PuzzleScript «Magic Chalkboards by Cool Nico».
- `game-screen`: поле; HUD вбудований у рівень — смуга залишку крейди всередині стіни (рядок пікселів), курсор на активній дошці.
- `tutorial-window` — текстові повідомлення між рівнями: «Press X while using a magic chalkboard to start drawing» / «…to stop drawing».
- `end-screen` — «Thank you for playing!».
- `custom-window` — мобільне згорнуте меню Undo/Restart.
- Переходи: splash → game-screen → (усі цілі) повідомлення → наступний рівень.

## Фічі поза полем
- `undo` ∞, `restart-level`; `levels-sequential` без явного вибору рівня (?).
- `touch-controls` — свайпи й тап на мобільних.
- Сирці відкриті в редакторі PuzzleScript.

## Варіації й родичі
- Сімʼя: [baba-is-you](baba-is-you.md) — створення сутностей зміною правил (тут — малюнком); [patricks-parabox](patricks-parabox.md) і [recursed](recursed.md) — вкладений простір у клітині; [increpare-micro-puzzles](increpare-micro-puzzles.md) — PuzzleScript-мініатюри з «панчлайном».
- Поза thinky: Scribblenauts (написане стає обʼєктом), Drawn to Life (намалюй героя), Maximilian / Crayon Physics (малюнок стає фізичним тілом).
- **Осі варіацій**: що визначає новий обʼєкт — точний гліф / класифікатор форми / текст; бюджет — пікселі крейди / кількість дошок; невдалий малюнок — зникає / стає рухомим каракулем (тут) / шкодить; полотно — у клітині (5×5) / на весь екран.

## Цікавинки для курсу
- Вкладена сітка 5×5 у клітині й другий режим вводу (курсор замість персонажа) — 📎.
- Розпізнавання гліфа: точне порівняння бітової маски 25 пікселів з таблицею зразків — 🌱; толерантне до зсуву (будь-де в 5×5) — 🥉.
- Бюджет крейди зі смугою, бонус +8 і подовження смуги — 🌱.
- Злиття каракулів поштовхом (OR масок) з повторною перевіркою гліфів — 📎.
- Кілька аватарів, що ходять синхронно, після «намалюй себе» — 🥉 (порядок руху й колізій між ними).
- Розвʼязувач BFS із малюванням (простір станів вибухає через 2^25 масок) — 👑 у загальному вигляді; 🥇 з обмеженням до гліфів.

## Мапа на каталог
- Є: `move-4dir` + `move-by-input` + `keyboard-controls` + `swipe-gestures` ↔ ввід; `push-object` ↔ ящики й каракулі; `impassable-cells` ↔ стіни й дошки; `all-on-targets` ↔ мета; `item-pickup` ↔ крейда-бонус; `undo-unlimited` + `restart-level`; `sequential-levels`; `sound-effects`; `tutorial-window` ↔ повідомлення.
- **Нема** → пропозиції карток:
  - `+draw-to-spawn` «Намалюй сутність — вона зʼявиться» · entities/spawn · 🥉 · слот {glyphs}.
  - `+sub-grid-canvas` «Вкладене полотно N×N у клітині з окремим курсором» · interface/input · 📎.
  - `+glyph-recognition` «Збіг бітової маски з таблицею гліфів» · game-logic/rules · 🌱–🥉.
  - `+ink-budget` «Обмежений запас чорнила/крейди на рівень» · entities/state · 🌱.
  - `+merge-drawings` «Злиття двох малюнків поштовхом (OR пікселів)» · entities/interact · 📎.
  - `+simultaneous-avatars` «Кілька аватарів ходять одночасно одним вводом» · entities/move · 🥉 (на відміну від `party-switch`).

## Пропозиції до словників
- `+cond:shape_match` — набір клітин/пікселів збігається з шаблоном (вже пропонувався іншими іграми).
- `+effect:draw` — лишити слід/піксель у позиції курсора (вже пропонувався).
- `+trigger:mode_toggle` — гравець перемкнув режим вводу (малювання ↔ рух).
- `+role:canvas` — клітина-полотно з власною вкладеною сіткою.
- `+ui:ink-meter` — смуга залишку чорнила/крейди.
- Карткові — див. «Мапа на каталог».

## Джерела
- ⭐ [itch.io: Magic Chalkboards](https://coolnico.itch.io/magic-chalkboards) — керування ПК і мобільне, X для малювання, коментарі (підказка автора в ROT13: треба створити щось нове, крім ящика, цілі, стіни, землі й дошки; відповідь гравця — «Draw yourself!»).
- [Сирці PuzzleScript](https://www.puzzlescript.net/editor.html?hack=968f998f4c2a366ba196a81d7597c2a4) — обʼєкти (25 пікселів C_*, курсор P_*, лічильник R_0–R_25, ExtraChalk, MovableDrawing), правила гліфів, злиття каракулів, wincondition; gist створено 30.06.2023.
- [Thinky Puzzle Game Jam 3](https://itch.io/jam/thinky-puzzle-game-jam-3/rate/2142455) — джемова сторінка.

## Непевне
- (?) Кількість рівнів не порахував надійно (у сирцях ≈ два-три десятки блоків карт разом із чернетками).
- (?) Гліф «суцільний квадрат з діркою → ящик на цілі» позначено автором у коді як «actually a bad mechanic i think», але правило активне; чи трапляється в рівнях — не перевірено.
- (?) Чи гліф мусить точно стояти в 5×5 (так за кодом — порівняння по фіксованих позиціях), чи є толерантність до зсуву — у коді нема, отже ні.
- (?) Наявність вибору рівня й збереження — стандарт PuzzleScript, не перевірено.
- (?) Рік 2023 — за gist-ом і Thinky Puzzle Game Jam 3; сторінка дати не має.
