---
title: Puddle Knights
slug: puddle-knights
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
year: 2020
platforms: [PC, Mac, Switch]
links:
  - {kind: youtube, url: "https://www.youtube.com/watch?v=5Ghk4cZw-yU", best: true, note: "офіційний launch-трейлер: плащі-змійки, бруд, леді й єпископи, стрибки по головах"}
  - {kind: steam, url: "https://store.steampowered.com/app/1180540/Puddle_Knights/", note: "опис: лицарі з плащами різної довжини, леді й єпископи, рвання плащів, 100+ рівнів, undo/reset"}
  - {kind: official, url: "https://www.lockpickle.com/puddleknights.html", note: "сторінка студії Lockpickle (Гельсінкі)"}
  - {kind: other, url: "https://www.lockpickle.com/press-sheet-puddleknights.html", note: "прес-кіт: механіки (рвання плаща, односторонні підйомні мости, стрибки по головах), історія, команда"}
  - {kind: other, url: "https://www.nintendo.com/games/detail/puddle-knights-switch/", note: "Switch-версія (жовтень 2020, більше рівнів і механік), сенсорний ввід"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=N3vasRKn1D4", note: "жовтневий трейлер (Switch)"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=3775566560", note: "Steam-гайд: відеорозвʼязки всіх світів"}
stage: v1
coverage: 55
mechanics: [move-4dir, keyboard-controls, body-queue, floor-types, impassable-cells, reach-exit, sequential-levels, level-select, save-progress, movement-animation, +undo-redo, +multi-avatar-switch, +exit-all-actors, +body-as-bridge, +cape-tear, +head-hop, +one-way-bridge, +escort-npc]
proposes: ["+trigger:input", "+trigger:enter", "+cond:cell", "+cond:occupied", "+cond:free", "+effect:move", "+effect:shrink", "+effect:set_cell", "+effect:set_state", "+role:terrain", "+role:ally", "+role:gate", "+feature:undo", "+axis:actors", "+axis:undo"]
author: opus
date: 2026-11-02
---

# Puddle Knights — лицарі тягнуть за собою плащі-змійки, а знать переходить калюжі лише по цих плащах

## Суть
Покрокова головоломка на сітці в ізометричному вигляді: кілька лицарів, у кожного плащ певної довжини, що тягнеться за ним, як тіло змійки. Шляхетні пасажири (леді, єпископи) не можуть ступити в бруд — але можуть іти по плащах, тож лицар «стелить» плащ через калюжу як міст. Гравець по черзі керує всіма персонажами й має довести знать до виходу. Тактики — стрибати по головах лицарів, рвати плащі, тримати підйомні мости; ящиків, ключів і кнопок у грі свідомо нема.

## Поле і час
- Квадратна сітка, рендер ізометричний 3D (тег Steam «Isometric»); клітини — суша, бруд/калюжі, стіни/вода (?), підйомні мости, вихід.
- Хід = крок одного активного персонажа на 1 клітину; плащ лицаря зсувається за ним (кінчик плаща звільняє клітину).
- Ні часу, ні випадковості, ні ворогів; повна інформація.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лицар | player | довжина плаща N (різна в різних лицарів) | крок у 4 напрямки; може йти по бруду (?); тягне плащ за собою |
| Плащ | object | N клітин, порядок від шиї до кінчика | повторює шлях лицаря (як тіло змійки); лежить на бруді як міст для знаті |
| Леді | ally | керована гравцем | крок у 4 напрямки; не може ступити в бруд; може йти по плащу й по голові лицаря (?) |
| Єпископ | ally | керований гравцем | як леді; відмінності в русі не перевірено (?) |
| Бруд / калюжа | terrain | — | непрохідний для знаті; лицар проходить (?) |
| Голова лицаря | — | клітина лицаря | на неї можна стати («head hop») і так перейти (?) |
| Підйомний міст | gate | односторонній; стан опущено/піднято | тримається опущеним, поки хтось на ньому/тисне; одностороння дія (?) |
| Стіна / перешкода | static | — | непрохідна |
| Вихід (ворота) | static | — | ціль знаті (і лицарів?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select, character)` → ТО активний персонаж змінюється (без витрати ходу (?)).
- КОЛИ `input(dir)` для лицаря → ЯКЩО `free(next_cell)` → ТО `move(knight, dir)`; кожна клітина плаща переходить на місце попередньої (`body-queue`), кінчик звільняє клітину.
- КОЛИ `input(dir)` для знаті → ЯКЩО `cell(next, mud)` і `not occupied(next, cape)` → ТО `block`; інакше `move(noble, dir)`.
- КОЛИ знать стоїть на плащі → ТО плащ під нею накриває бруд і служить мостом.
- КОЛИ лицар рухається, а `occupied(cape_cell, someone)` → ТО `custom: «плащ рветься — частина за точкою притиску лишається на місці, лицар іде з коротшим плащем»` (?), `shrink(cape)`.
- КОЛИ `enter(character, knight_head)` → ТО `custom: «стрибок по голові — проходить над лицарем»` (?).
- КОЛИ `enter(any, drawbridge)` → ТО `set_state(drawbridge, down)`; `leave` → піднімається; міст односторонній (?).
- КОЛИ `all_on(noble, exit)` (і, можливо, усіх персонажів) → ТО `win`.
- Поразки нема: незворотні дії (порваний плащ) лікуються undo/reset. Рахунку нема.

## Керування і ввід
- Клавіатура/геймпад: стрілки — крок активного персонажа; кнопка перемикання персонажа (?); Undo, Reset.
- Switch: сенсорний екран підтримується (вибір персонажа дотиком (?)).
- Миша на ПК (?).

## Вікна, меню, HUD
- `main-menu` — Continue/Play, Options, Quit (?).
- `level-select` — світи й рівні; гайд згадує «all worlds» — рівні згруповані у світи.
- `game-screen` — ізометричне поле, підсвітка активного персонажа (`selection-highlight`), підказки клавіш undo/reset.
- `settings-window` — мова (8 мов), звук, керування (?).
- Переходи: main-menu → level-select → game-screen → (усі на виході) → наступний рівень.

## Фічі поза полем
- `undo` + `restart-level` (явно в описі); без тиску часу.
- `levels-sequential` 100+ рівнів, згруповані у світи; `achievements`, `cloud-save` (Steam).
- `localization` — 8 мов з озвучкою; Switch-версія (жовтень 2020) — розширена новими рівнями й механіками.
- Демо на Steam; власні інструменти редагування рівнів — внутрішні, гравцю не дані.

## Варіації й родичі
- Snakebird (тіло-черга з гравітацією) — плащ тут як тіло змійки, але без гравітації й з іншою роллю: **тіло — це міст для інших**.
- Sokoban-сімʼя без ящиків: замість штовхання — «прокладання» тілом.
- Скинуті механіки (прес-кіт): випасання свиней.
- **Осі варіацій:** тіло-черга — шкодить / блокує / є опорою для інших; довжина — фіксована / рветься / росте; хто ходить по тілу — свої / чужі; кілька підконтрольних — перемикання / синхронно.

## Цікавинки для курсу
- Тіло-черга, що стає прохідною підлогою для інших персонажів — 🥉 (deque + шар «що лежить на клітині»).
- Рвання плаща при притиснутій клітині (обрізання черги в точці) — 🥈 (зміна структури тіла посеред ходу, частина лишається на полі).
- Кілька персонажів з різними правилами прохідності (лицар у бруд, знать — ні) — 📎 (матриця «хто куди може»).
- Стрибок по голові: клітина-персонаж як тимчасова підлога — 📎.
- Односторонній підйомний міст, що тримається вагою — 🥉.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ крок; `body-queue` ↔ плащ іде за лицарем; `floor-types` ↔ бруд для знаті; `impassable-cells`; `reach-exit` ↔ вихід; `sequential-levels` + `level-select` + `save-progress`; `movement-animation` ↔ анімація плаща (власна система студії).
- **Нема** → пропозиції карток:
  - `+undo-redo` · game-logic/flow · 📎.
  - `+multi-avatar-switch` «Кілька аватарів, перемикання активного» · interface/input · 📎 (з Snakebird).
  - `+exit-all-actors` «Перемога, коли всі потрібні дійшли» · game-logic/win · 🌱 (з Snakebird).
  - `+body-as-bridge` «Тіло однієї сутності — підлога для інших» · entities/interact · 🥉.
  - `+cape-tear` «Розрив тіла-черги в притиснутій точці» · entities/state · 🥈 — дитина `body-queue`.
  - `+head-hop` «Стати на клітину персонажа» · entities/legality · 📎.
  - `+one-way-bridge` «Односторонній міст, що тримається вагою» · entities/interact · 🥉.
  - `+escort-npc` «Супровід слабших підконтрольних до виходу» · game-logic/win · 📎.

## Пропозиції до словників
- `+trigger:input`; `+trigger:enter` — стати на клітину типу (бруд, міст, голова).
- `+cond:cell(next, mud)`; `+cond:occupied(cell, cape)` — на клітині лежить плащ; `+cond:free`.
- `+effect:move`; `+effect:shrink(cape, n)` — рвання; `+effect:set_cell` — шматок плаща лишається на бруді (?); `+effect:set_state` — міст.
- `+role:terrain` (бруд), `+role:ally` (леді, єпископ — підконтрольні, але слабші), `+role:gate` (підйомний міст).
- `+feature:undo`; `+axis:actors` — `party`; `+axis:undo` — `unlimited` (?).

## Джерела
- ⭐ [Launch Trailer (YouTube)](https://www.youtube.com/watch?v=5Ghk4cZw-yU) — побачити плащі-змійки й бруд за хвилину.
- [Steam](https://store.steampowered.com/app/1180540/Puddle_Knights/) — опис механік, 100+ рівнів, 10–35 год, 8 мов, 3 березня 2020.
- [Прес-кіт Lockpickle](https://www.lockpickle.com/press-sheet-puddleknights.html) — рвання плаща, односторонні мости, head hops; прототип грудня 2018; команда; два трейлери.
- [Сторінка гри](https://www.lockpickle.com/puddleknights.html) · [Nintendo](https://www.nintendo.com/games/detail/puddle-knights-switch/) — Switch 8 жовтня 2020, сенсорний ввід.
- [Steam-гайд з розвʼязками](https://steamcommunity.com/sharedfiles/filedetails/?id=3775566560) · [жовтневий трейлер](https://www.youtube.com/watch?v=N3vasRKn1D4).

## Непевне
- (?) Точна механіка рвання плаща (що стається з відірваною частиною) — джерела лише називають механіку.
- (?) Чи можуть лицарі ходити по бруду і чи брудниться плащ (прес-кіт: «capes collect mud»).
- (?) Чим єпископ відрізняється від леді (можливий шаховий натяк — рух по діагоналі — не перевірено).
- (?) Умова перемоги: лише знать на виході чи всі персонажі.
- (?) Як працює «односторонній» підйомний міст і «тримати міст опущеним».
- (?) Пункти меню, клавіша перемикання персонажа; чи коштує перемикання хід.
- (?) Офіційний сайт puddleknights.com не відповідав (ECONNREFUSED).
