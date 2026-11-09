---
title: Wriggle (clickmazes)
slug: wriggle
aka: [Wriggler, Wriggle puzzles, TJ-wriggle, Colour-wriggle, Wriggle 3D]
family: push-slide
also: []
klass: figure
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2006
platforms: [web (Java applet, 2006), iOS (2009), web (JS, 2019), web (PuzzleScript, 2024)]
links:
  - {kind: itch, url: "https://clickmazes.itch.io/wriggle", best: true, note: "грати: 80 пазлів з iOS-застосунку 2009 року, вивести синього через кут; undo / restart"}
  - {kind: official, url: "https://www.clickmazes.com/new-indexw.htm", note: "індекс Wriggle: правило «Rush Hour, але блок гнеться», хронологія, усі варіанти"}
  - {kind: other, url: "https://www.clickmazes.com/wriggle/new-wriggle.htm", note: "оригінальний Wriggle: накрити свої кольорові клітини; 8 + 12 пазлів; drag"}
  - {kind: other, url: "https://www.clickmazes.com/tjwrig/new-jwrig.htm", note: "TJ-wriggle (Tom Jolly): 6×6, до 4 вриглів, сірі блокери, вихід знизу"}
  - {kind: other, url: "https://www.clickmazes.com/wrigc/new-wrigc.htm", note: "Colour-wriggle: один вригл, кольори не повторюються, автогенерація"}
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=c58ba6f441c8b2ecb817", note: "Wriggler demake (Tapio Saarinen, 2021): курсор хапає кінець"}
  - {kind: other, url: "https://gist.github.com/tapiosaarinen/c58ba6f441c8b2ecb817", note: "код demake: кульки-сегменти, ланки, цілі за кольором"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Wriggle+sliding+block+puzzle", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [body-queue, drag-drop-piece, multi-cell-size, impassable-cells, reach-exit, all-on-targets, level-select, sequential-levels, restart-level, undo-redo, keyboard-controls, legal-move-highlight, +bidirectional-worm, +no-repeat-colour-body]
proposes: ["+card:bidirectional-worm", "+card:no-repeat-colour-body", "+feature:legality-hint-modes"]
author: opus
date: 2026-11-09
---

# Wriggle — Rush Hour з гнучкими блоками: «черви» з кружечків повзуть лише вперед-назад за свої кінці

## Суть
На полі лежать вригли — ланцюжки кружечків, як черви. Вригл не може зсунутись убік чи стрибнути: він повзе тільки вздовж себе — потягнеш за голову, повзе вперед, за хвіст — назад, а тіло повторює шлях. Це правило Rush Hour (блок рухається лише вздовж своєї осі), послаблене тим, що блок **гнеться**, тому досяжних станів незрівнянно більше. Мета залежить від набору: накрити кожним вриглом свої кольорові клітини, вивести синього через проріз або провести одного вригла крізь кольорове поле без повторів кольору.

## Поле і час
- Квадратна сітка; TJ-wriggle — 6×6 з сірими клітинами-блокерами й прорізом-виходом у краю; Extreme TJ-wriggle — 4×4 (компʼютерно знайдені пазли).
- Один шар тіл: кожна клітина — або порожня, або блокер, або сегмент рівно одного вригла; цілі (блідий відтінок кольору) — шар підлоги.
- Сусідство — 4 напрямки; сегменти вригла завжди сусідні по ланцюжку.
- Час відсутній (`static`): світ змінюється лише ходом гравця; хід = зсув вригла на 1 клітину за кінець (перетягування може складатися з кількох таких кроків).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вригл | piece | довжина N, колір, два кінці (голова / хвіст) | кінець стає в сусідню вільну клітину, кожен сегмент — на місце попереднього, протилежний кінець звільняє клітину |
| Синій вригл (TJ) | piece | — | його треба вивести через проріз, головою або хвостом уперед |
| Сірий блокер | static | 1 клітина | непрохідний |
| Цільова зона | zone | колір вригла (блідий відтінок) | має бути накрита вриглом свого кольору |
| Проріз-вихід (TJ) | static | у нижньому краї / правому нижньому куті | лише через нього синій покидає поле |
| Кольорова клітина (Colour-wriggle) | terrain | колір; кольорів на 1 більше за довжину вригла | вригл не може одночасно займати дві клітини одного кольору |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag_end, dir)` → ЯКЩО `free(next_cell)` → ТО `move(end, dir)`, `pull(body)` — тіло тягнеться слідом, як хвіст змійки.
- КОЛИ `input(drag_end, dir)` → ЯКЩО `occupied(next_cell, other_wriggler)` або `cell(next_cell, blocker)` → ТО `block`.
- КОЛИ `input(drag_end, dir)` → ЯКЩО `occupied(next_cell, own_body)` → ТО `block` (власний хвіст теж заважає — за clickmazes).
- КОЛИ `input(drag_middle)` → ТО `custom: «нічого — тягнути можна лише за кінці»` (demake).
- Тягнути можна за будь-який кінець: «голова» і «хвіст» міняються ролями залежно від того, за який кінець узявся.
- Боком і стрибком вригл не рухається — лише вздовж себе.
- Оригінал: КОЛИ `all_on(wriggler, own_zone)` для всіх вриглів → ТО `win`, `custom: «наступний пазл вантажиться сам»`.
- TJ-wriggle: КОЛИ `reach(blue, exit_gap)` → ТО `win`, `next_level`.
- Colour-wriggle: КОЛИ `input(drag_end, dir)` → ЯКЩО `not unique(colours_under_body)` після ходу → ТО `block`.
- Colour-wriggle: КОЛИ `reach(wriggler, right_column)` (зі старту в лівому стовпці) → ТО `win`.
- КОЛИ `input(restart)` (пробіл / кнопка) → ТО `restart`; КОЛИ `input(undo)` (меню itch) → ТО `undo(1)`.
- Перемога: за набором — накрити зони / вивести синього / дійти до правого краю. · Поразка: нема. · Рахунок: нема.

## Керування і ввід
- Мишею або дотиком: торкнутись поля, щоб воно отримало фокус, і тягнути вригла за голову чи хвіст; вригл іде за курсором, «якщо тільки може».
- Colour-wriggle — курсорні клавіші.
- Demake: курсор на клавіатурі хапає кінець; середина тіла не реагує.
- Пробіл / кнопка — рестарт пазла; на itch — меню-вкладка зліва вгорі з undo і рестартом.

## Вікна, меню, HUD
- Сторінки clickmazes (аплети / JS): поле + кнопка «Click here to play» → вибір набору й список-розгортка пазлів (`puzzle-select`); у Colour-wriggle — розгортка опцій (візуальний режим) і кнопка Auto-generate.
- Оригінальний Wriggle: пазл обрати не можна — після розвʼязку наступний вантажиться сам.
- itch (PuzzleScript, 2024): головне меню (тап), `game-screen` без HUD, меню-вкладка undo / restart.
- HUD Colour-wriggle: `legal-move-highlight` у режимах Top-n-tail (стінки навколо голови й хвоста показують допустимі кроки) і Tunnel.

## Фічі поза полем
- `puzzle-bank`: оригінал — 8 одночервних і 12 багаточервних; iOS-набір (TJ-подібні) — 80 пазлів, з 2024 — на itch.
- Colour-wriggle: генерація нового пазла на поточній сітці (Auto-generate) і три візуальні режими підказок (No-walls / Top-n-tail / Tunnel) — те саме поле, різна кількість підказки.
- `restart-level`, `undo` (itch).
- Big-wriggle bonus challenge (2009, перебудовано 2025).

## Варіації й родичі
- Хронологія: розробка з 2003 (Andrea Gilbert) → Java-аплет 2006 → TJ-wriggle (концепція Tom Jolly, 2006–09) → iOS-застосунок 2009 (розробник Conlan Rios) → «Observations on wriggle puzzles» і пошук простору Bob Henderson (2010) → JS (2019) → demake Tapio Saarinen (2021) → PuzzleScript на itch (2024); фізичний прототип Oskar van Deventer (IPP23, 2003); Wriggle 3D (Amazon app store); SVG-порт TJ-wriggle (Henri Manson).
- Родичі в корпусі: [rush-hour](rush-hour.md) і [unblock-me](unblock-me.md) (твердий блок уздовж осі, вивести одного через вихід), [klotski](klotski.md), [snakebird](../thinky/snakebird.md) (тіло-черга, але з гравітацією й лише вперед), [snake](../maze-arcade/snake.md).
- Осі варіацій:
  - **жорсткість блока**: твердий (Rush Hour) / гнучкий ланцюжок (Wriggle);
  - **напрямки руху**: лише вперед головою (Snake, Snakebird) / вперед і назад за будь-який кінець (Wriggle);
  - **мета**: вивести одного (TJ, Rush Hour) / накрити зони кольором (оригінал) / пройти поле без повтору кольору (Colour-wriggle);
  - **підказка легальності**: нема / стінки навколо кінців / анімовані тунелі.

## Цікавинки для курсу
- Вригл як `deque` сегментів: рух за голову — додати в голову й зняти хвіст, за хвіст — навпаки — 🌱.
- Drag кінця з перевіркою кожного кроку шляху курсора (вригл «тягнеться, якщо може») — 📎.
- Перевірка «усі кольори під тілом різні» на кожному кроці (Colour-wriggle) — 🌱.
- Підсвітка допустимих кроків голови й хвоста (режим Top-n-tail) — 🌱.
- Розвʼязувач BFS: стан = набір шляхів-клітин усіх вриглів; простір вибухає через згини — 🥈.
- Пошук найважчих пазлів на 4×4 / 6×6 (як Bob Henderson) — 🥇.

## Мапа на каталог
- Є: `body-queue` ↔ тіло повторює шлях кінця; `drag-drop-piece` ↔ тягнути за кінець; `multi-cell-size` ↔ тіло на N клітин, що рухається лише вздовж себе (узагальнення Rush Hour); `impassable-cells` ↔ блокери; `reach-exit` ↔ вивести синього (TJ); `all-on-targets` ↔ накрити свої зони; `level-select` ↔ список пазлів; `sequential-levels` ↔ автозавантаження наступного; `restart-level` + `undo-redo`; `keyboard-controls` ↔ Colour-wriggle; `legal-move-highlight` ↔ Top-n-tail.
- **Нема** → пропозиції карток:
  - `+bidirectional-worm` «Черв рухається за будь-який кінець: голова веде вперед, хвіст — назад» · entities/move · 📎 · слот {ends: one|both}.
  - `+no-repeat-colour-body` «Тіло не може займати дві клітини одного кольору» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+card:bidirectional-worm`, `+card:no-repeat-colour-body`.
- `+feature:legality-hint-modes` — кілька рівнів візуальної підказки допустимих ходів на тому самому полі (No-walls / Top-n-tail / Tunnel).
- ⏳-слова, вжиті тут: `input`, `free`, `occupied`, `cell`, `move`, `pull`, `all_on`, `reach`, `unique`, `undo`; вікно `puzzle-select`.

## Джерела
- ⭐ [Wriggle на itch.io](https://clickmazes.itch.io/wriggle) — 80 пазлів з iOS-застосунку, мета «blue can exit through the bottom-right corner, either head-first or tail-first», тач / меню undo-restart, кредити (Gilbert, Jolly, Conlan Rios), реліз серпня 2024.
- [clickmazes: індекс Wriggle](https://www.clickmazes.com/new-indexw.htm) — правило «Rush Hour, але блок гнеться», хронологія 2003–2024, усі сторінки варіантів.
- [Оригінальний Wriggle](https://www.clickmazes.com/wriggle/new-wriggle.htm) — накрити свої кольорові клітини, блокування іншим вриглом і власним хвостом, drag, 8 + 12 пазлів, прототип Oskar van Deventer, demake.
- [TJ-wriggle](https://www.clickmazes.com/tjwrig/new-jwrig.htm) — 6×6, до 4 вриглів, сірі блокери, вихід знизу, тягнути за голову чи хвіст, рестарт пробілом, кредити Tom Jolly.
- [Colour-wriggle](https://www.clickmazes.com/wrigc/new-wrigc.htm) — кольорове обмеження, кольорів = довжина + 1, курсорні клавіші, три візуальні режими, Auto-generate.
- [Wriggler demake](https://www.puzzlescript.net/play.html?p=c58ba6f441c8b2ecb817) і [його код](https://gist.github.com/tapiosaarinen/c58ba6f441c8b2ecb817) — тягнути лише за кінці, «moves with the cursor if it possibly can», цілі за кольором, 14 рівнів, без undo (`noundo`).
- YouTube: пошук «Wriggle sliding block puzzle».

## Непевне
- (?) «Власний хвіст заважає»: clickmazes пише, що хід блокує власний хвіст; чи можна ступити головою в клітину, яку хвіст саме звільняє, — не перевірено.
- (?) Розміри поля оригінального Wriggle і максимальна довжина вригла — не названо (у demake до 9 сегментів, але це властивість demake).
- (?) Чи undo на itch необмежений — сказано лише «undo moves».
- (?) Рік 2006 — рік Java-аплета; розробка з 2003, фізичний прототип показано 2003 року.
