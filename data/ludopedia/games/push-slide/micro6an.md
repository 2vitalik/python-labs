---
title: micro6an
slug: micro6an
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
year: 2025
platforms: [web (HTML5, PuzzleScript)]
links:
  - {kind: itch, url: "https://stingby12.itch.io/micro6an", best: true, note: "грати в браузері; «Your steps gets traced on each room. Don't follow your footsteps and solve each 6 rooms»; Confounding Calendar 2025"}
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=bb0125d4a9d9d3ece31c74254970e090", note: "та сама гра на puzzlescript.net; сирець — gist bb0125d4…: правила сліду, перевірка кімнати, мапа 6 кімнат"}
  - {kind: other, url: "https://www.bontegames.com/2025/12/micro6an-browser.html", note: "огляд Bart Bonte (06.12.2025): 6 кімнат, Z — undo, R — рестарт; у коментарях — де застрягають"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=micro6an+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 85
mechanics: [move-4dir, keyboard-controls, push-object, all-on-targets, impassable-cells, visited-trail, undo-unlimited, restart-level, level-from-txt, sound-effects, +trail-wall, +trail-carryover, +sequential-rooms]
proposes: ["+effect:trace", "+trigger:room_solved", "+card:trail-carryover", "+card:sequential-rooms", "+ui:active-room-frame"]
author: opus
date: 2026-11-19
---

# micro6an — шість мікрокімнат Sokoban: кожен твій крок стає стіною в наступній кімнаті

## Суть
Шість маленьких кімнат Sokoban на одному екрані розвʼязуються по черзі, у кожній свій герой. Кожна клітина, де побував герой кімнати N, **відбивається** в кімнаті N+1 у тій самій відносній позиції: спершу як позначка-слід, а щойно кімнату N розвʼязано — як справжня стіна. Тож розвʼязок кімнати треба шукати такий, щоб його слід не замурував ящик чи ціль сусіда («Don't follow your footsteps»), а фінальне повідомлення підморгує: «Sometimes, tracing your steps is the key».

Мініатюра Stingby12 для Confounding Calendar 2025 на PuzzleScript: один екран, 6 кімнат, 11 ящиків.

## Поле і час
- Одна мапа 33×23 клітини сирця: 6 кімнат 3×2, кожна — 9×9 клітин усередині спільних стін.
- Порядок кімнат по колу: 1 → 2 → 3 (верхній ряд зліва направо) → 4 (нижня праворуч) → 5 → 6 (нижня ліворуч); слід кімнати 6 падає в уже розвʼязану кімнату 1.
- Слід — зсув на 10 клітин (9 клітин кімнати + стіна): праворуч для 1→2 і 2→3, донизу для 3→4, ліворуч для 4→5 і 5→6, догори для 6→1. Без поворотів і віддзеркалень.
- Хід = крок героя; без вводу світ стоїть. Короткий цикл `again` — лише перевірка «кімнату розвʼязано» й передача ходу наступному героєві.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой кімнати 1–6 | player | очікує / активний / готово | рух 4 боки, штовхає ящик; активний завжди один |
| Ящик | object | — | зсувається на 1, якщо за ним вільно; ящик за ящиком не штовхається |
| Ціль | zone | — | місце для ящика; кімната розвʼязана, коли всі її цілі зайняті |
| Стіна | static | — | рамки кімнат; межа «кімнати» для перевірки |
| Слід | mark | — | позначка в кімнаті N+1 на клітинах, де побував герой N; поки що не заважає |
| Стіна зі сліду | static | — | слід після розвʼязку кімнати N: блокує і героя, і ящики |
| Рамка активної кімнати | mark | світла / темна | підсвічує кімнату, де зараз грають |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(hero, dir)`; стіна чи стіна зі сліду → `block`.
- КОЛИ `contact(hero, crate)` → ЯКЩО `free(cell_behind)` → ТО `push`, `move(hero, dir)`; за ящиком стіна чи інший ящик → `block`.
- КОЛИ `level_start` або `after(input)` → ТО `spawn_at(trail, same_cell_in_next_room)` — слід ставиться і на стартову клітину героя.
- КОЛИ `all_on(crate, target)` у кімнаті активного героя → ТО `transform(trail, wall)` для всього сліду, `set_state(hero, done)`, `set_state(next_hero, active)`.
- Межа кімнати для перевірки — заливка від героя до старих стін; стіни зі сліду заливку не зупиняють.
- Стіна зі сліду може лягти на ящик, ціль чи старт героя: ящик звідти ще виштовхнеш, а ціль під стіною стає недосяжною (з сирця).
- КОЛИ `counter(rooms_solved, ==, 6)` → ТО `message(«Sometimes, tracing your steps is the key.»)`, `win`.
- КОЛИ `input(z)` → ТО `undo` (відкочує й перетворення сліду на стіни).
- КОЛИ `input(r)` → ТО `restart` усього екрана.
- Перемога: розвʼязано всі 6 кімнат. · Поразка: нема; якщо слід замурував наступну кімнату — undo назад у попередню. · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок активного героя (стандарт PuzzleScript); перемикати героїв не можна — черга фіксована.
- Z — undo без ліміту, R — рестарт усієї мапи.

## Вікна, меню, HUD
- `splash-screen` — титул PuzzleScript «micro6an by Stingby12».
- `tutorial-window`: текстовий екран «Solve all of the rooms.»; у кінці — «Sometimes, tracing your steps is the key.»
- `game-screen`: усі 6 кімнат одночасно; HUD нема; активну кімнату видно з підсвіченої рамки, розвʼязані — з потемнілого героя; слід у наступній кімнаті видно одразу.
- Переходи: титул → текст → game-screen → (6 кімнат) фінальний текст.

## Фічі поза полем
- `undo` без ліміту, `restart-level`; рівень один — без вибору й збережень.
- Браузерна мініатюра на один вечір (тег itch «Short»); сирець відкритий (gist), можна переробити в редакторі PuzzleScript.

## Варіації й родичі
- [Maxwell's puzzling demon](maxwells-puzzling-demon.md) — розвʼязані рівні стають ящиками наступних: результат одного пазла — дані іншого.
- [Watch Your Step](watch-your-step-steed.md), [Tactic Toe](tactic-toe.md) — слід героя породжує обʼєкти (`+trail-spawn`).
- [Blockade](../maze-arcade/blockade.md) — слід-стіна в тій самій арені (`+trail-wall`).
- [Sokoban](sokoban.md) — кожна кімната окремо — класичний мікро-Sokoban.
- Осі варіацій:
  - **куди йде слід**: та сама арена (Tron) / наступна кімната (тут) / наступний рівень;
  - **коли твердне**: одразу / після розвʼязку кімнати;
  - **чим стає**: стіною / обʼєктом / ящиком.

## Цікавинки для курсу
- Перенесення сліду в наступну кімнату зсувом координат на ±10 — 🌱.
- Двофазний слід: позначка під час гри → стіна після розвʼязку — 📎.
- Перевірка «кімнату розвʼязано» заливкою від героя до стін кімнати — 📎.
- Undo, що відкочує й передачу ходу, і перетворення сліду (стан = знімок усіх 6 кімнат) — 📎.
- Пошук розвʼязку кімнати N з «безпечним» слідом для N+1, ланцюгом через усі 6 кімнат — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ крок героя; `push-object` ↔ ящики; `all-on-targets` ↔ цілі кімнати; `impassable-cells` ↔ стіни й стіни зі сліду; `visited-trail` ↔ позначки сліду; `undo-unlimited` + `restart-level` ↔ Z і R; `level-from-txt` ↔ мапа символами в сирці; `sound-effects` ↔ звуки кроку, ящика, завершення кімнати.
- **Нема** → пропозиції карток:
  - `+trail-wall` (уже пропонована, Tron) — слід стає стіною.
  - `+trail-carryover` «Слід кімнати N стає стінами кімнати N+1» · entities/move · 📎.
  - `+sequential-rooms` «Кілька кімнат на одному екрані, активна — по черзі» · levels/progression · 🌱.

## Пропозиції до словників
- `+effect:trace` — залишити позначку-слід у відповідній клітині іншої зони (micro6an); `spawn_at` не каже, що це копія шляху.
- `+trigger:room_solved` — у зоні (кімнаті) всі цілі закрито; ширше за `all_on`, бо обмежене зоною.
- `+card:trail-carryover`, `+card:sequential-rooms` — див. «Мапу на каталог».
- `+ui:active-room-frame` — підсвічена рамка зони, де зараз хід.

## Джерела
- ⭐ [itch.io: micro6an](https://stingby12.itch.io/micro6an) — опис, гра в браузері, посилання на сирець.
- [Сирець PuzzleScript](https://www.puzzlescript.net/play.html?p=bb0125d4a9d9d3ece31c74254970e090) — gist: обʼєкти, правила поштовху, сліду (`Set` → `WallProto` → `WallX`), перевірки кімнати заливкою, активації героїв, умова `no Player`, мапа 33×23 з 6 кімнатами.
- [Bonte Games: micro6an](https://www.bontegames.com/2025/12/micro6an-browser.html) — огляд, керування Z / R, відгуки гравців (застрягли на 4-й кімнаті, не розуміючи, у якій попередній помилка).

## Непевне
- (?) Чи є в itch-версії дотикове керування; титул і екрани — зі стандарту PuzzleScript, окремо не перевірені.
