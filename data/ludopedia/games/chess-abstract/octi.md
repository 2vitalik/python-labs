---
title: Octi (Окті)
slug: octi
aka: [Окті, OCTI, "Octi: New Edition", Octi for Kids, "Octi-6×7", Octi-X, Octi-Extreme]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1999
platforms: [board, web, PC]
links:
  - {kind: other, url: "https://homepages.inf.ed.ac.uk/csutton/publications/tourney-2001.pdf", best: true, note: "C. Sutton, «Computers and Octi» (2002): правила Octi-6×7 і Octi-X, формації, розгалуження, турнір програм 2001"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Octi", note: "огляд: Donald Green, 1999, 2 або 4 гравці, 9×9 і дитяча 6×7, Computer Olympiad 2004, SGF"}
  - {kind: other, url: "https://project.dke.maastrichtuniversity.nl/games/files/msc/Roijakkers_thesis.pdf", note: "магістерська C. Roijakkers: детальні правила Octi: New Edition, нотація, стратегії, складність 10^28 / 10^37"}
  - {kind: other, url: "https://www.red-bean.com/sgf/octi.html", note: "SGF для Octi: нотація ходів, суперзубці, резервні поди, варіанти full/fast/kids, edgeless"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Octi+board+game", note: "пошук; відео не перевіряв"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, move-8dir, cell-click, drag-drop-piece, selection-highlight, legal-move-highlight, last-move-highlight, path-preview, turn-enforcement, hot-seat, ai-opponent, ai-minimax, pocket, remaining-counter, move-notation, state-as-data, rule-variants, game-screen, end-screen, help-window, undo-step, +build-move-directions, +jump-over, +multi-jump, +optional-capture, +friendly-capture, +capture-steals-resource, +base-occupation-win, +no-moves-lose, +piece-stacking, +reserve-drop]
proposes: ["+cond:has_indicator(piece, dir)", "+effect:add_direction(piece, dir)", "+effect:jump_over", "+effect:capture", "+cond:jumped_this_move(cell)", "+ui:direction-picker", "+ui:capture-toggle", "+card:build-move-directions", "+card:optional-capture"]
author: opus
date: 2026-11-09
---

# Octi — фігури без ходів: кожен «зубець» відкриває поду новий напрямок, а стрибки через свої й чужі несуть до бази суперника

## Суть
Абстрактна стратегія Donald Green (1999), «шашки на стероїдах». Фігура-под — восьмикутник без жодного ходу; хід гравця — **або** вставити в под зубець (prong) у будь-якому з 8 напрямків, **або** рухати под: на клітину чи стрибком через сусідній под — лише туди, де є зубець. Стрибати можна через свої й чужі поди, взяття необовʼязкове, а взятий под віддає свої зубці захоплювачу. Перемога — зайняти Octi-клітину суперника; ядро — дилема «будувати чи ходити».

## Поле і час
- **Octi-6×7** (Octi: New Edition, колишня Octi for Kids): дошка 6×7, у кожного 4 Octi-клітини (бази) у своєму краї, 4 поди на них і 12 зубців у запасі.
- **Octi-X** (Octi-Extreme, оригінальна «Octi»): 9×9, у кожного 3 Octi-клітини, 25 зубців і 4 резервні поди.
- Напрямки — 8 (ортогональні й діагональні); зубці a–h, `a` — «вгору» від жовтого, далі за годинниковою. Поди не повертаються, зубці не знімаються.
- Хід за ходом, пасу нема; першим ходить жовтий. Партія 6×7 — зазвичай до 20–25 ходів, Octi-X — до 100.
- Є версія на 4 гравців (правила онлайн у Green 2002; SGF її не підтримує).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Под | piece | колір, набір зубців (0–8) | ходить / стрибає лише в напрямках своїх зубців; взятий — знімається назавжди (6×7) |
| Зубець (prong) | resource | напрямок a–h; запас 12 (6×7) / 25 (Octi-X) | вставляється в под з запасу; при взятті пода переходить захоплювачу |
| Суперзубець | resource | Octi-X, варіант | є в SGF (`!`); правил не бачив |
| Octi-клітина | zone | власник; 4 (6×7) / 3 (Octi-X) | старт подів; под суперника на ній → перемога (у Octi-X — на всіх трьох) |
| Резервний под | supply | Octi-X: 4 | ставиться на свою Octi-клітину або на зайняту ворожу |
| Стек | container | Octi-X | свої поди на одній клітині; рухаються разом, не перестрибують одне одного |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «по поду на кожній своїй Octi-клітині, зубці в запасі»`; першим ходить жовтий.
- КОЛИ `input(add_prong(pod, dir))` → ЯКЩО `turn_of(side)` and `has(player, prong)` and `custom: «у пода ще нема зубця в напрямку dir»` → ТО `take(player, prong)`, `custom: «зубець вставлено в под назавжди»`, `end_turn`.
- КОЛИ `input(move(pod, dir))` → ЯКЩО `custom: «у пода є зубець у напрямку dir»` and `free(cell_ahead)` → ТО `move(pod, dir)`, `end_turn`.
- КОЛИ `input(jump(pod, dir))` → ЯКЩО `custom: «у пода є зубець у напрямку dir»` and `occupied(cell_ahead, pod)` (свій або чужий) and `free(cell_beyond)` → ТО `custom: «под перестрибує на 2 клітини»`.
- КОЛИ `after(jump)` → ТО `choose(capture|keep)` для перестрибнутого пода; захоплення: `disappear(jumped_pod)`, `give(mover, prongs_of_jumped)`.
- КОЛИ `after(jump)` → ЯКЩО `custom: «з нової клітини можливий ще стрибок»` and `custom: «ця клітина ще не перестрибувалась у цьому ході»` → ТО `choose(continue|stop)`; приземлятися на ту саму клітину двічі можна, перестрибувати ту саму — ні (у 6×7 максимум 7 стрибків).
- Взяття свого пода дозволене: `custom: «зубці лишаються в себе, а не дістаються супернику»`.
- КОЛИ `enter(pod, enemy_octi_square)` (кроком або стрибком) → ТО `win` негайно (6×7).
- КОЛИ `no_moves(opponent)` → ТО `win` (усі поди взято; лише порожні поди без зубців у запасі; усі заблоковані).
- Пасу нема: `custom: «гравець без легального ходу програє»`.
Octi-X:
- КОЛИ `custom: «поди займають усі 3 Octi-клітини суперника»` → ТО `win`.
- КОЛИ `input(drop(reserve_pod, square))` → ЯКЩО `has(player, reserve_pod)` and `custom: «своя Octi-клітина або ворожа, яку займає твій под»` → ТО `place(pod, square)`, `end_turn`.
- КОЛИ `input(free_pod)` → ЯКЩО `custom: «гравець займає ворожу Octi-клітину»` → ТО `custom: «взятий раніше свій под повертається на зайняту Octi-клітину»`.
- КОЛИ `input(move(pod, dir))` → ЯКЩО `occupied(cell_ahead, own_pod)` → ТО `custom: «под стає в стек»`; поди стеку ходять одночасно, але не перестрибують одне одного.
- Перемога: под на Octi-клітині суперника (6×7: будь-якій; Octi-X: усіх трьох) · суперник без ходу. Нічиєї в офіційних правилах нема.

## Керування і ввід
- Дошка: вставити зубець у гніздо пода — хід; переставити под рукою.
- Цифрова версія: клік по поду → навколо 8 гнізд (`+ui:direction-picker`) — клік по порожньому гнізду ставить зубець; клік по клітині — крок; ланцюг стрибків клацається по клітинах з перемикачем «брати / не брати» на кожному перестрибнутому поді (`+ui:capture-toggle`).
- Нотація (Roijakkers, SGF): `22+a` — додати зубець, `22a-23` — крок, `23ad-41-43-61x` — ланцюг стрибків з узяттям останнього; SGF `GM[19] RU[kids]`.

## Вікна, меню, HUD
- (цифрова версія; octi-online.com з тези не відкривав)
- `main-menu`: гра з AI / людиною, правила.
- `match-setup`: версія (6×7 / Octi-X / 4 гравці), варіанти (fast, edgeless, superprong), хто ходить першим.
- `game-screen`: дошка з тонованими Octi-клітинами; поди з іконками зубців; запас зубців і резервні поди кожної сторони (`pocket`, `remaining-counter`); `turn-indicator`; `legal-move-highlight` кроків і стрибків; `path-preview` ланцюга; `last-move-highlight`; `move-list` у нотації.
- `help-window` — три види ходу і правила стрибка.
- `end-screen` — зайнята база / суперник без ходу.
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- `ai-opponent-levels`: програми з турнірів (AaronBot, ChiouBot, Casbah, HAL; alpha-beta).
- `export-import`: SGF (GM[19], властивості RU, BO/WO, NP, NR, NS).
- `custom-rules`: full / fast / kids, edgeless, superprong; задання кількості зубців і резервних подів.
- `hotseat`, `undo`, `replay` — (цифрова версія).

## Варіації й родичі
- **Octi-6×7 vs Octi-X**: 4 бази / 3 бази, перемога — одна / усі три, 12 / 25 зубців, без резерву / 4 резервні поди, без стеків / стеки, звільнення взятих подів через зайняту базу.
- Варіанти з SGF: fast, kids, edgeless, superprong; версія на 4 гравців.
- Родичі: [checkers.md](checkers.md) (стрибок-узяття, ланцюги — але тут взяття необовʼязкове, а стрибати можна через своїх), [ploy.md](ploy.md) (напрямки ходу як індикатори на фігурі, що повертається), [the-duke.md](the-duke.md) (патерн ходу на самій фігурі), [halma-chinese-checkers.md](halma-chinese-checkers.md) (ланцюг стрибків через будь-які фігури).
- **Осі варіацій**: напрямки фігури (фіксовані / повертаються / будуються зубцями) · стрибок (лише через чужі / через будь-які) · взяття (обовʼязкове / за вибором / нема) · ресурс фігур (без / запас зубців, що переходить при взятті) · мета (одна база / усі бази / знищити всіх).

## Цікавинки для курсу
- Под як 8-бітна маска напрямків, хід «додати біт» — 🌱; генерація кроків з маски — 🌱.
- Ланцюг стрибків з вибором «брати чи ні» на кожному перестрибнутому і забороною перестрибувати ту саму клітину — 🥈 (DFS з розгалуженням).
- Взяття переносить ресурс (зубці) захоплювачу, взяття свого — 📎.
- Перемога «нема ходів» з трьома причинами (нема подів / порожні поди без запасу / блок) — 📎.
- Octi-X: стеки, що ходять одночасно, — вибух кількості ходів (до 626 у позиції) — 🥇.
- AI alpha-beta для 6×7: розгалуження ~31 (2–101), складність 10^28 станів / 10^37 дерево — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` · `move-8dir` · `cell-click` / `drag-drop-piece` · `selection-highlight` · `legal-move-highlight` · `last-move-highlight` · `path-preview` (ланцюг стрибків) · `turn-enforcement` · `hot-seat` · `ai-opponent` / `ai-minimax` · `pocket` (запас зубців і резерв) · `remaining-counter` · `move-notation` · `state-as-data` · `rule-variants` · `game-screen` / `end-screen` / `help-window` · `undo-step`.
- **Нема** → пропозиції карток:
  - `+build-move-directions` «Напрямки ходу будуються по одному за хід» · entities/legality · 📎 · слоти {dirs: 8, supply, removable: false}.
  - `+jump-over` «Стрибок через сусідню фігуру» · entities/move · 🌱; `+multi-jump` — ланцюг (див. checkers.md).
  - `+optional-capture` «Взяття за вибором при стрибку» · entities/combat · 📎.
  - `+friendly-capture` — можна брати свою фігуру.
  - `+capture-steals-resource` «Узяття передає ресурс фігури захоплювачу» · entities/combat · 📎.
  - `+base-occupation-win` «Зайняти базу суперника» · game-logic/win · 🌱 · слоти {need: any|all}.
  - `+no-moves-lose` — програє гравець без ходу.
  - `+piece-stacking` (Octi-X), `+reserve-drop` — поставити резервну фігуру на свою базу.

## Пропозиції до словників
- `+cond:has_indicator(piece, dir)` — у фігури є маркер напрямку (Ploy, Octi).
- `+effect:add_direction(piece, dir)` — фігура отримує новий дозволений напрямок.
- `+effect:jump_over` — перестрибнути сусідню фігуру на клітину за нею.
- `+effect:capture` — взяти фігуру з поля з передачею її ресурсу (спільне з манкалою).
- `+cond:jumped_this_move(cell)` — клітину вже перестрибували в цьому ланцюгу.
- `+ui:direction-picker` — 8 гнізд навколо фігури для вибору напрямку.
- `+ui:capture-toggle` — перемикач «брати / не брати» на кожній перестрибнутій фігурі.
- `+card:build-move-directions` · `+card:optional-capture`.

## Джерела
- ⭐ [Sutton, «Computers and Octi: Report from the 2001 Tournament»](https://homepages.inf.ed.ac.uk/csutton/publications/tourney-2001.pdf) — правила Octi-6×7 і Octi-X (бази, зубці, резерв, стеки, звільнення), формації, розгалуження 31 / 39, турнір 2001.
- [Wikipedia: Octi](https://en.wikipedia.org/wiki/Octi) — автор, рік, 2 або 4 гравці, 9×9 і 6×7, програма перемогла автора на 6×7, Computer Olympiad 2004.
- [Roijakkers, «Analysis and Implementation of the Game of Octi»](https://project.dke.maastrichtuniversity.nl/games/files/msc/Roijakkers_thesis.pdf) — гл. 2: правила New Edition (12 зубців, a–h, стрибки, взяття свого, ≤7 стрибків, нічиї), нотація, стратегії; гл. 3: складність.
- [SGF: Octi](https://www.red-bean.com/sgf/octi.html) — нотація, суперзубці, резервні поди, варіанти.
- YouTube: пошук «Octi board game».

## Непевне
- (?) Офіційна книжка правил (tesera.ru PDF зі статті) не відкрилась — правила зібрані з Sutton і Roijakkers.
- (?) Суперзубці, варіанти fast і edgeless, гра на 4 — лише назви з SGF, правил не бачив.
- (?) Нічиї (обидва без ходів / вічне повторення) — у тезі «можливі, але в офіційних правилах не згадані».
- (?) Чи можна в Octi-X розділити стек частково (SGF має нотацію «частина стеку») — деталей правил не бачив.
- (?) Wikipedia називає оригінальну Octi грою 9×9, а Sutton — що Octi-X «спершу продавалась як Octi»; узгоджується, але дати виходу версій не бачив.
