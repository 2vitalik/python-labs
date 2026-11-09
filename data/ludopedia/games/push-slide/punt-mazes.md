---
title: Punt mazes
slug: punt-mazes
aka: [Punt, Punt-discs]
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
year: 2005
platforms: [web (JavaScript, 2005), web (PuzzleScript, 2018)]
links:
  - {kind: itch, url: "https://chz.itch.io/punt-mazes", best: true, note: "грати (PuzzleScript, CHz): правила, клавіші й тач, перемикач напрямних X"}
  - {kind: official, url: "https://www.clickmazes.com/punt/new-punt.htm", note: "clickmazes: правила, автори концепції й рівнів, історія 2005 → 2018 → 2021, SVG-порт"}
  - {kind: other, url: "https://gist.github.com/chz16/033fbf6b1d605e6efaeb633e15601391", note: "код PuzzleScript: зонд дальності, перевірка приземлення, напрямні, 12 рівнів з авторами"}
  - {kind: other, url: "https://www.puzzlescript.net/editor.html?hack=033fbf6b1d605e6efaeb633e15601391", note: "код у редакторі PuzzleScript (hackable)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Punt+mazes+clickmazes+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [move-4dir, keyboard-controls, swipe-gestures, inertia-slide, push-object, impassable-cells, all-on-targets, path-preview, undo-unlimited, restart-level, sequential-levels, sound-effects, +stop-on-entity, +distance-punt, +leap-over-walls, +illegal-move-flash]
proposes: ["+card:distance-punt", "+card:leap-over-walls", "+card:illegal-move-flash", "+card:stop-on-entity", "+feature:guides-toggle", "+window:title-screen", "+window:message-screen"]
author: opus
date: 2026-11-09
---

# Punt mazes — штовхач ковзає до упору, а шайба відлітає вперед на ту саму відстань — навіть через стіни

## Суть
Sokoban, де штовхач (зелений хрест) не ходить, а **ковзає** до стіни або до першої шайби. Вʼїхавши в шайбу, він стає на її місце, а шайба відлітає вперед рівно на стільки клітин, скільки він проїхав: розгін = дальність удару. Шайба **перелітає** стіни й інші шайби — важить лише клітина приземлення: вона має бути вільна й у межах поля. Мета — закрити шайбами всі чорні цілі.

## Поле і час
- Квадратна сітка зі стінами; шари: підлога (шахова у PuzzleScript, лише візуально) → ціль → штовхач, стіни, шайби → службові маркери (зонди, напрямні).
- Стіни зупиняють штовхача, але не шайбу в польоті; шайба не може впасти на стіну, на іншу шайбу чи за межі поля.
- Хід = один ковзний рух штовхача (з можливим ударом); без вводу нічого не змінюється.
- PuzzleScript-реалізація рахує дальність зондом до 15 клітин — для рівнів цього досить.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Штовхач (зелений хрест) | player | — | ковзає в напрямку вводу до клітини перед стіною або на клітину першої шайби |
| Шайба (punt-disc) | object | — | від удару переноситься на k клітин уперед (k = пробіг штовхача), над стінами й шайбами |
| Стіна | static | — | непрохідна для штовхача; шайбу пропускає над собою, але приземлитись на неї не можна |
| Ціль | terrain | — | місце для шайби |
| Напрямна (guide) | mark | вкл/викл | червоний хрестик — де зупиниться штовхач, червоний ромб — куди впаде шайба, для кожного з 4 напрямків; ромб на стіні чи шайбі = хід недопустимий |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, wall)` → ТО `block`, `sound(hit_wall)`.
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `slide(player, dir)` — до клітини перед стіною; k = кількість пройдених клітин.
- КОЛИ `contact(player, puck)` → ЯКЩО `free(landing_cell)` (k клітин за шайбою: нема стіни, шайби, не за краєм) → ТО `custom: «штовхач стає на клітину шайби»`, `move(puck, landing_cell)`.
- Шайба не ковзає й не штовхає інших: це стрибок, клітини між стартом і приземленням не перевіряються.
- КОЛИ `contact(player, puck)` → ЯКЩО `not free(landing_cell)` → ТО `block` (увесь хід скасовано), `flash(landing_cell)`, `sound(illegal)`.
- k = 1 (шайба впритул) — звичайний поштовх Sokoban на 1 (`sound(puck_by_1)`); k > 1 — далекий удар (інший звук).
- КОЛИ `input(action)` → ТО `custom: «увімкнути / вимкнути напрямні»`.
- КОЛИ `all_on(puck, target)` (у коді — кожна ціль під шайбою) → ТО `win`, `next_level`.
- КОЛИ `input(undo)` → ТО `undo(1)`; КОЛИ `input(restart)` → ТО `restart`.
- Перемога: усі цілі закриті шайбами. · Поразка: нема; глухий кут → undo/рестарт. · Рахунок: нема.

## Керування і ввід
- Клавіатура: стрілки / WASD — ковзнути; `X` — напрямні («maybe useful for larger levels»); `Z` — undo; `R` — рестарт.
- Тач: тап у головному меню, свайп — рух, тап під час гри — напрямні, меню-вкладка вгорі ліворуч — undo / рестарт.
- Ціль ходу задається лише напрямком: дальність штовхач обирає не сам, вона випливає з поля.

## Вікна, меню, HUD
- `title-screen` (custom, стандарт PuzzleScript): «Punt mazes», автор «mathgrant et al.».
- `message-screen` (custom): перед кожним рівнем «N/12, author: …».
- `game-screen`: поле без лічильників; HUD — `path-preview` (напрямні: хрестики там, де зупиниться штовхач, ромби там, де впаде шайба) і спалах недопустимого приземлення.
- Переходи: title → message → рівень → … → 12/12.

## Фічі поза полем
- `levels-sequential`: 12 рівнів (mathgrant, Andrea Gilbert, zag, fadeblue, lostdummy; двоє — без автора).
- `undo` ∞, `restart-level`, `touch-controls` поруч із клавіатурою.
- Перемикач напрямних — підказка-«рентген» замість hint-кнопки.
- Відкритий код (hackable).

## Варіації й родичі
- Історія: концепція mathgrant на форумі greylabyrinth (березень 2005), JS-реалізація ralphmerridew, перевідкриття й PuzzleScript-переробка CHz (2018), нова сторінка на clickmazes (2021), SVG-порт Henri Manson.
- Родичі в корпусі: [sokoban](sokoban.md) (k = 1), [ice-sliding-puzzles](ice-sliding-puzzles.md) (ковзання до упору), [ricochet-robots](ricochet-robots.md) (зупинка об сутність), [pengo](pengo.md) (блок відлітає від удару), [spacekoban](spacekoban.md) (інший спосіб передати рух).
- Осі варіацій:
  - **як рухається штовхач**: крок (Sokoban) / ковзання до упору (Punt);
  - **дальність поштовху**: 1 клітина / до упору (Pengo) / рівно стільки, скільки розгін (Punt);
  - **що бачить шайба в польоті**: усе (ковзання) / нічого — лише клітину приземлення (Punt);
  - **недопустимий хід**: тихо ігнорувати / скасувати й підсвітити причину (Punt).

## Цікавинки для курсу
- Ковзання з підрахунком пробігу k і стрибок шайби на k — 🌱: дві петлі по напрямку.
- Перевірка приземлення до виконання ходу (атомарний хід або нічого) + спалах причини — 📎.
- Напрямні: попередній розрахунок результату для всіх 4 напрямків і їх відмальовка — 📎 (той самий код ходу, викликаний «насухо»).
- Звуки за типом події (упор, поштовх на 1, далекий удар, недопустимо) — 🌱.
- Розвʼязувач BFS: стан = позиція штовхача + множина шайб; гілок лише 4 — 🥉.
- Генератор рівнів, де розвʼязок вимагає перелітання через стіни, — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` + `swipe-gestures`; `inertia-slide` ↔ ковзання штовхача; `push-object` ↔ випадок k = 1; `impassable-cells` ↔ стіни лише для штовхача; `all-on-targets`; `path-preview` ↔ напрямні; `undo-unlimited` + `restart-level`; `sequential-levels`; `sound-effects`.
- **Нема** → пропозиції карток:
  - `+stop-on-entity` (вже пропонована, Klotski / ice-sliding) — ковзання зупиняється об сутність.
  - `+distance-punt` «Удар переносить обʼєкт на відстань розгону» · entities/interact · 📎 · слот {max_k}.
  - `+leap-over-walls` «Обʼєкт перелітає перешкоди, важить лише клітина приземлення» · entities/legality · 🌱.
  - `+illegal-move-flash` «Недопустимий хід скасовано, причина підсвічена» · interface/hud · 🌱.

## Пропозиції до словників
- `+card:distance-punt`, `+card:leap-over-walls`, `+card:illegal-move-flash`; повтор `+card:stop-on-entity`.
- `+feature:guides-toggle` — перемикач підказок-напрямних на полі (куди потрапить кожен обʼєкт за кожного напрямку).
- `+window:title-screen`, `+window:message-screen` — повтор.
- ⏳-слова, вжиті тут: `input`, `cell`, `free`, `slide`, `move`, `flash`, `sound`, `all_on`, `undo`.

## Джерела
- ⭐ [Punt mazes на itch.io](https://chz.itch.io/punt-mazes) — правила («you slide until you hit a wall or land on a puck … moved forward the same distance you traveled»), шайби над стінами, заборона приземлення на шайбу й за край, клавіші, тач, кредити.
- [clickmazes: Punt](https://www.clickmazes.com/punt/new-punt.htm) — фігури (зелений хрест, жовті шайби, сірі стіни, чорні цілі), правило дальності, автори 2005, greylabyrinth, CHz 2018, сторінка 2021, SVG-порт.
- [Gist з кодом](https://gist.github.com/chz16/033fbf6b1d605e6efaeb633e15601391) — зонди Probe0–Probe15, `PlayerBadDestination`, `IllegalMoveFlash`, напрямні, звуки, `All Target on Puck`, 12 рівнів з авторами; [те саме в редакторі](https://www.puzzlescript.net/editor.html?hack=033fbf6b1d605e6efaeb633e15601391).
- YouTube: пошук «Punt mazes clickmazes puzzlescript».

## Непевне
- (?) Інтерфейс оригінальної JS-версії 2005 року (мишею чи клавішами, undo) — сторінка відсилає до головної clickmazes, не перевірено.
- (?) Чи всі 12 рівнів PuzzleScript — повний набір оригіналу 2005 року, чи добірка.
- (?) Межа дальності 15 клітин — властивість PuzzleScript-реалізації, не правило гри.
