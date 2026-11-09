---
title: Gridmount
slug: gridmount
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: graph
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2024
platforms: [web]
links:
  - {kind: itch, url: "https://hempuli.itch.io/gridmount", best: true, note: "грати в браузері (Clickteam Fusion HTML5), безкоштовно; скриншоти й коментарі з поясненнями автора"}
  - {kind: other, url: "https://hempuli.itch.io/gridmount/comments", note: "усі коментарі: «cover every X with a box», ящики «followed the line», Ctrl+Q"}
  - {kind: other, url: "https://thinkygames.com/games/gridmount/", note: "Thinky Games (403 для агента; опис бачив у результатах пошуку)"}
  - {kind: other, url: "https://hempuli.itch.io/circlemount", note: "сусідня гра серії: полярна сітка"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Gridmount+Hempuli", note: "пошук; проходження"}
stage: v1
coverage: 35
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, all-on-targets, reach-exit, impassable-cells, skip-level, sequential-levels, +glued-edges, +cell-orientation-marker, +exit-unlocks-on-goal, +linked-boxes]
proposes: ["+effect:cross_edge", "+card:glued-edges", "+card:cell-orientation-marker"]
author: opus
date: 2026-11-09
---

# Gridmount — «проклята» сітка Sokoban: ребра клітин склеєні як завгодно, кожна клітина показує свою «північ»

## Суть
Безкоштовна браузерна гра Hempuli (Arvi Teikari, автор Baba Is You), видана на Хелловін 2024 у серії мініатюрних «Covemount-like» сокобанів. Перші рівні — звичайний Sokoban: заштовхати ящики на хрестики, тоді прапорець оживає, і до нього треба дійти. Потім гра «ламає сітку»: ребра клітин зʼєднуються одне з одним у найнесподіваніших комбінаціях. Клітини відриваються від решітки, висять окремо й повʼязані з іншими клітинами лініями. Щоб гравець «не заблукав», на кожній клітині намальовано, де в неї північ.

## Поле і час
- Основа — прямокутна решітка (на скриншотах 6×6), але суміжність задана графом: клітина може висіти поза решіткою й бути зʼєднаною лініями з далекими клітинами (наприклад, з двома кутовими).
- Кожна клітина має маркер-трикутник «північ»; повернуті клітини мають північ униз або вбік.
- Хід — один крок; часу нема. Збереження нема: рівні проходяться підряд у межах сесії.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж (Covemonty?) | player | — | рух 4 напрямки за ребрами клітин; штовхає ящики |
| Ящик | object | звичайний / «плюс» (?) | штовхається на 1, у тому числі через склеєне ребро «по лінії» |
| Плюс-ящик (?) | object | — | за коментарем, поштовх одного змушує інші «плюс»-ящики теж рушити |
| Хрестик X | zone | — | ціль для ящика |
| Прапорець | static | активний / ні | активується, коли всі X закриті ящиками; дійти до активного — рівень пройдено |
| Цегляна стіна | static | — | непрохідна |
| Клітина | terrain | позиція, «північ», звʼязки | вузол графа; лінії показують ребра, склеєні з іншими клітинами |
| Літери (фінал) | object | M, I, N, E, R | штовхаються; з них складають слово (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(player, dir)`; `next` — клітина за ребром у напрямку `dir`, зокрема склеєним з іншою клітиною (`custom: «перехід через склеєне ребро»`, `+effect:cross_edge`).
- КОЛИ `input(dir)` → ЯКЩО `occupied(next, wall)` → ТО `block`.
- КОЛИ `contact(player, box)` → ЯКЩО `free(cell_behind)` → ТО `push(box)`, `move(player, dir)`; «за ящиком» теж рахується через склеєне ребро (ящик «їде по лінії»); інакше `block`.
- КОЛИ `custom: «перехід через склеєне ребро»` → ТО `custom: «напрям руху перераховується за «північчю» клітини, куди перейшли»` (?).
- КОЛИ `push(plus_box)` → ТО `custom: «інші плюс-ящики пробують рушити в тому ж напрямку»` (?).
- КОЛИ `all_on(box, x)` → ТО `set_state(flag, active)` (відповідь у коментарях: «cover every X with a box to activate the flag»).
- КОЛИ `enter(player, flag)` → ЯКЩО `state(flag, active)` → ТО `win`, `next_level`; неактивний прапорець «нічого не робить».
- КОЛИ `input(ctrl+q)` → ТО `next_level` (пропуск рівня — звичний для серії).
- Поразки нема; рахунку нема.

## Керування і ввід
- Стрілки (?) — рух; Ctrl+Q — пропустити рівень (порада в коментарях: «у більшості Covemount-like нема збережень»).
- Undo/рестарт у сусідній грі серії (Circlemount) є; для Gridmount не перевірено (?).

## Вікна, меню, HUD
- `game-screen`: решітка з маркерами півночі, відірвані клітини на лініях; HUD нема.
- Меню й вибору рівня не видно; за фінальний екран слугує рівень зі словом із літер.

## Фічі поза полем
- `skip-level` (Ctrl+Q). Збереження нема: після краху браузера прогрес губиться (коментар).
- Devlog «Tiny fix» (31.10.2024) — виправлення глюка з плюс-ящиком, що їхав не туди.

## Варіації й родичі
- Серія Hempuli 2024: Mayban (березень, «нам повідомили про існування кольорів»), Circlemount (вересень, сітка в полярних координатах), Gridmount (жовтень, склеєні ребра). Спільне — той самий персонаж і «ламання» однієї основи Sokoban.
- `games/thinky/baba-is-you.md` — той самий автор; Baba ламає правила текстом, Gridmount — топологію поля.
- `games/thinky/patricks-parabox.md`, `games/thinky/4d-sokoban.md` — інші способи «зламати» простір Sokoban: рекурсія і зайвий вимір.
- `games/thinky/lock-and-pin.md` — поштовх рухає кілька однакових обʼєктів одразу (як «плюс»-ящики).
- **Осі варіацій:** топологія — площина / тор / полярна (Circlemount) / довільний граф ребер (тут); орієнтація клітини — нема / маркер півночі; група обʼєктів — незалежні / рухаються разом.

## Цікавинки для курсу
- Поле як граф: у кожної клітини 4 ребра, кожне веде в (клітину, ребро-вхід); рух і поштовх — обхід цього графа — 🥈.
- Перерахунок напряму при переході між повернутими клітинами (маркер «північ») — 🥈.
- Прапорець, що оживає, коли всі X закриті, — 🌱.
- Рендер графа: решітка + відірвані клітини з лініями-ребрами — 📎.

## Мапа на каталог
- Є: `move-4dir`, `move-by-input`, `keyboard-controls`; `push-object`; `all-on-targets` ↔ ящики на X; `reach-exit` ↔ прапорець; `impassable-cells`; `skip-level`; `sequential-levels`.
- **Нема** → пропозиції карток:
  - `+glued-edges` «Склеєні ребра клітин: поле як граф» · entities/move · 🥈 (узагальнення `wrap-edges`).
  - `+cell-orientation-marker` «Клітина з власною північчю» · entities/state · 🥈.
  - `+exit-unlocks-on-goal` «Вихід оживає після виконання умови» · game-logic/win · 🌱.
  - `+linked-boxes` «Ящики однієї групи рухаються разом» · entities/legality · 📎.

## Пропозиції до словників
- `+effect:cross_edge(a, edge)` — перейти через склеєне ребро у звʼязану клітину з перерахунком напряму (Gridmount, портальні сітки).
- `+card:glued-edges`, `+card:cell-orientation-marker` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch.io: Gridmount](https://hempuli.itch.io/gridmount) — опис («mark which way is north on each tile»), реліз 31.10.2024, HTML5, скриншот рівня (X, ящики, стіни, прапорець); скриншоти з коментарів: відірвані клітини з лініями, перевернута клітина, фінальне слово з літер.
- [Коментарі](https://hempuli.itch.io/gridmount/comments) — «cover every X with a box to activate the flag»; «they just followed the line»; глюк з плюс-ящиком; Ctrl+Q.
- Thinky Games (через результати пошуку) — «edges of grid cells can be connected to each other in all sorts of horrendous ways».
- [Circlemount](https://hempuli.itch.io/circlemount) — сусідня гра серії (undo, полярна сітка).

## Непевне
- (?) Як саме «північ» клітини впливає на напрям після переходу — з опису й скриншотів не видно; правило записано як гіпотезу.
- (?) Що таке «плюс-ящик» — відомо лише з одного коментаря; можливо, це група звʼязаних ящиків.
- (?) Розміри поля, кількість рівнів і наявність undo/рестарту не перевірено; гра на Clickteam Fusion, її дані (`.cch`) не розібрано.
- (?) Чи фінальне слово з літер — обовʼязкова мета, чи жарт (у коментарях «MINER» і «MR INW»).
