---
title: Code Master (ThinkFun)
slug: code-master
aka: [ThinkFun Code Master, Code Master Programming Logic Game, Майстер коду]
family: board-digital
also: [program-robots]
klass: puzzle
axes:
  field: graph
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2015
platforms: [board]
links:
  - {kind: other, url: "https://geekdad.com/2015/09/stack-overflow-steam/", best: true, note: "GeekDad, огляд STEAM-ігор: мета (кристали → портал після повного виконання), кольорові шляхи, while-цикли й if-then-else, блок-схеми, 60 рівнів"}
  - {kind: official, url: "https://legacy.thinkfun.com/products/code-master/", note: "офіційна сторінка (при відкритті 503)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ThinkFun+Code+Master", note: "пошук; як грати"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Code+Master", note: "пошук BGG"}
stage: v1
coverage: 50
mechanics: [command-program, sensor-predicates, step-execution, collect-all, reach-exit, level-bank, puzzle-select, difficulty-levels, sequential-levels, drag-drop-piece, level-solver, unique-puzzle-generation, +colored-edge-graph, +follow-colored-path, +use-all-tokens, +finish-on-exit-only, +flowchart-program, +while-loop-token, +if-else-token, +token-supply-per-level]
proposes: ["+cond:edge_of_color(node, c)", "+role:node", "+role:program-token", "+ui:program-slots", "+ui:token-supply", "+card:follow-colored-path", "+card:use-all-tokens", "+card:flowchart-program"]
author: opus
date: 2026-11-09
---

# Code Master — скласти з виданих токенів програму-блок-схему, за якою аватар пройде кольоровими шляхами між планетами, збере кристали й закінчить на порталі

## Суть
Одиночна головоломка ThinkFun про програмування без компʼютера. Мапа — граф «планет», зʼєднаних кольоровими шляхами; картка рівня задає старт аватара, кристали, портал і набір токенів-команд. Гравець розкладає токени в програму; виконання програми веде аватара шляхами; рівень пройдено, лише якщо після **повного** виконання аватар зібрав усі кристали й стоїть на порталі. Пізні рівні додають цикли while і розгалуження if-then-else у вигляді блок-схеми. Близько до `program-robots`, але поле — граф, а програма будується з фізичних токенів.

## Поле і час
- Поле — граф: вузли-планети, ребра-шляхи різних кольорів; кілька мап, кожна з рівнями зростаючої складності.
- Шари: мапа (граф) + жетони рівня (аватар, кристали, портал) + програма (послідовність або блок-схема токенів поза полем).
- Час `programmed`: спершу скласти програму, потім виконати її покроково; гравець не втручається під час виконання.
- Інформація повна; випадковості нема — рівень детермінований.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Планета | static | вузол графа | точка, де аватар стоїть між командами |
| Шлях | conduit | колір | ребро між планетами; ним аватар іде за командою того самого кольору |
| Аватар | player | позиція | виконує команди програми; великий пластиковий жетон |
| Кристал | pickup | на планеті | зникає, коли аватар проходить/стає на планету |
| Портал | static | вузол-ціль | рівень пройдено, якщо аватар тут після кінця програми |
| Токен дії | object | колір | «іди шляхом цього кольору» |
| Токен циклу | object | умова | while: повторювати блок, доки умова (?) |
| Токен розгалуження | object | умова | if-then-else: гілка залежно від умови (?) |
| Картка рівня | supply | мапа, старт, кристали, портал, набір токенів | задає завдання; розвʼязок у книзі (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- Складання: КОЛИ `input(place(token, slot))` → ЯКЩО `has(level, token)` → ТО `place(token)`; токени — лише з набору картки рівня.
- Запуск: КОЛИ `input(custom: «виконати програму»)` → ТО `custom: «аватар виконує токени по порядку блок-схеми»`.
- Дія: КОЛИ `exec(color c)` → ЯКЩО `custom: «з поточної планети виходить шлях кольору c»` → ТО `move(avatar, custom: «інший кінець шляху»)`.
- Немає шляху: КОЛИ `exec(color c)` → ЯКЩО `not custom: «шлях кольору c є»` → ТО `crash` → `lose` (див. «Непевне»).
- Кристал: КОЛИ `enter(avatar, crystal)` → ТО `pickup` + `counter(crystals_left, −1)`.
- Цикл: КОЛИ `exec(while)` → ЯКЩО `custom: «умова циклу справджується»` → ТО `trigger(loop_body)`; інакше — наступний токен.
- Розгалуження: КОЛИ `exec(if)` → ЯКЩО `custom: «умова справджується»` → ТО гілка then; інакше гілка else.
- Портал завчасно: КОЛИ `enter(avatar, portal)` → ЯКЩО `custom: «програма ще не завершена»` → ТО `custom: «рух триває; портал не зараховано»`.
- Перемога: КОЛИ `program_end` → ЯКЩО `all_gone(crystal)` and `occupied(portal, avatar)` → ТО `win`.
- Поразка: КОЛИ `program_end` → ЯКЩО `not all_gone(crystal)` or `not occupied(portal, avatar)` → ТО `restart`.
- Усі токени: ЯКЩО `custom: «невикористаний токен з набору»` → ТО `custom: «розвʼязок недійсний»` (див. «Непевне»).

## Керування і ввід
- Фізично: обрати картку рівня → поставити аватар, кристали, портал на мапу → розкласти токени в програму → «виконати» пальцем аватар крок за кроком.
- Цифрова версія: drag токенів з запасу в слоти блок-схеми, кнопки «запуск» / «крок» / «скинути», підсвітка поточного токена.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Грати → `puzzle-select` · Як грати → `help-window`.
- `puzzle-select`: мапи × рівні з позначками «розвʼязано».
- `game-screen`: мапа-граф, кристали й портал, `token-supply` (кандидат), `program-slots` (кандидат: блок-схема), `instruction-highlight`, `remaining-counter` (кристали), кнопки `step-button` і `restart-button`.
- `end-screen`: «рівень пройдено» / «аватар застряг».
- Переходи: main-menu → puzzle-select → game-screen → end-screen → наступний рівень.

## Фічі поза полем
- `puzzle-bank`: 60 рівнів, складність росте; кожна мапа має кілька рівнів-ярусів.
- `levels-sequential` — рекомендований порядок: спершу лише кольорові шляхи, далі цикли й умови.
- `show-solution` — розвʼязки в книжці (?).

## Варіації й родичі
- Програмування на сітці: [robot-turtles](../program-robots/robot-turtles.md) (картки-команди, дитяча настолка), [lightbot](../program-robots/lightbot.md), [robozzle](../program-robots/robozzle.md) (умовні команди за кольором клітини), [karel](../program-robots/karel.md).
- ThinkFun «картка + фішки»: [thinkfun-logic-mazes](thinkfun-logic-mazes.md), [chocolate-fix](chocolate-fix.md).
- **Осі варіацій**: поле (граф з кольоровими ребрами / сітка) · програма (лінійна / блок-схема / функції) · умова (колір / наявність шляху) · обмеження (усі токени обовʼязкові / ліміт слотів) · фініш (будь-коли на цілі / лише після кінця програми).

## Цікавинки для курсу
- Граф з кольоровими ребрами як мапа: «іди ребром кольору c» — 🌱.
- Інтерпретатор блок-схеми з while і if-else над станом аватара — 📎.
- Умова перемоги «після повного виконання», а не «торкнувся цілі» — 🌱.
- Розвʼязувач: перебір перестановок виданих токенів з перевіркою — 📎; з циклами й гілками — 🥉 (обмеження на кількість кроків).
- Генератор рівнів з єдиним розвʼязком при обовʼязковому використанні всіх токенів — 🥇.

## Мапа на каталог
- Є: `command-program` · `sensor-predicates` (умови if/while) · `step-execution` · `collect-all` · `reach-exit` · `level-bank` · `puzzle-select` · `difficulty-levels` · `sequential-levels` · `drag-drop-piece` · `level-solver` · `unique-puzzle-generation`.
- **Нема** → пропозиції карток:
  - `+colored-edge-graph` «Поле — граф з кольоровими ребрами» · entities/move · 📎.
  - `+follow-colored-path` «Команда кольору → рух ребром цього кольору» · game-logic/program · 🌱.
  - `+use-all-tokens` «Розвʼязок мусить використати весь виданий набір команд» · game-logic/program · 🌱.
  - `+finish-on-exit-only` «Ціль зараховується лише після кінця програми» · game-logic/win · 🌱.
  - `+flowchart-program` «Програма як блок-схема з гілками» · game-logic/program · 🥉.
  - `+while-loop-token` · `+if-else-token` — керувальні токени · game-logic/program · 📎.
  - `+token-supply-per-level` «Рівень видає конкретний набір команд» · levels/bank · 🌱.

## Пропозиції до словників
- `+cond:edge_of_color(node, c)` — з вузла виходить ребро кольору c.
- `+role:node` — вузол графа як сутність поля.
- `+role:program-token` — фізичний токен команди поза полем.
- `+ui:program-slots` · `+ui:token-supply`.
- `+card:follow-colored-path` · `+card:use-all-tokens` · `+card:flowchart-program`.

## Джерела
- ⭐ [GeekDad: Stack Overflow — STEAM-Powered Kids](https://geekdad.com/2015/09/stack-overflow-steam/) — огляд: мета (старт → портал, зібрати всі кристали, портал лише після повного виконання), ранні рівні — кольорові лінії по порядку, пізні — логічні вузли, while і if-then-else, блок-схема, 60 рівнів; великі пластикові аватар і портал.
- [ThinkFun: Code Master](https://legacy.thinkfun.com/products/code-master/) — офіційна сторінка (503 при відкритті).
- BGG: [пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=Code+Master); YouTube: пошук.

## Непевне
- (?) Рік 2015 — за датою огляду GeekDad (вересень 2015); точна дата виходу й автор (Mark Engelberg?) — не перевірено.
- (?) Що відбувається, коли з планети нема шляху потрібного кольору (провал чи пропуск) — з памʼяті, провал.
- (?) Чи обовʼязково використати всі токени набору — з памʼяті, так; огляд не каже.
- (?) Умови while/if: за чим саме перевіряються (колір планети, наявність шляху, кристал) — огляд не уточнює.
- (?) Кількість мап (10?) і розвʼязки в книжці — з памʼяті.
- (?) Офіційної цифрової версії не бачив; вікна гіпотетичні.
