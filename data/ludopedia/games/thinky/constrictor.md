---
title: CONSTRICTOR
slug: constrictor
aka: [Constrictor, Удав]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2024
platforms: [web]
links:
  - {kind: itch, url: "https://beepyeah.itch.io/constrictor", best: true, note: "грати в браузері; мета «зʼїж усі яблука й придуши всіх гризунів»; стрілки, Z — undo, R — рестарт; теги PuzzleScript / Snake / Sokoban"}
  - {kind: play, url: "https://html-classic.itch.zone/html/11728394/index.html", note: "PuzzleScript-збірка: у файлі повний сирцевий код — обʼєкти, 13 правил, 4 умови перемоги, 15 рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=v0pu04b87VA", note: "проходження від автора, вбудоване на сторінці itch (спойлери)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=CONSTRICTOR+puzzlescript+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 90
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, self-collision, visited-trail, item-pickup, collect-all, fill-hole, undo-unlimited, restart-level, sequential-levels, level-from-txt, +trail-wall, +grow-every-step, +custodian-capture, +sticky-floor, +object-loss-restart, +level-intro-message]
proposes: ["+effect:leave_trail", "+cond:sandwiched", "+window:message-screen", "+axis:undo", "+card:grow-every-step", "+card:custodian-capture", "+card:sticky-floor", "+card:object-loss-restart"]
author: opus
date: 2026-11-19
---

# CONSTRICTOR — удав, що лишає за собою вічний хвіст: зʼїж усі яблука й заморозь кожного гризуна, затиснувши його з двох боків

## Суть
PuzzleScript-змійка навпаки: голова ходить по клітинах, а хвіст не тягнеться за нею, а **лишається на місці назавжди** — змія росте на клітину щоходу й сама будує собі лабіринт. Мета рівня — зʼїсти всі яблука й «придушити» всіх гризунів: гризун замерзає, коли з двох протилежних боків від нього опиняється змія (голова чи хвіст). Гризунів і камені можна штовхати, як у Sokoban; далі додаються клей, що приклеює назавжди, і ями з шипами, які засипає камінь. 15 рівнів, автор — Tom Brinton (Beep Yeah!).

## Поле і час
- Квадратна сітка, вигляд згори; рівні від 11×3 (коридор-навчання) до 13×10, обнесені стінами.
- Три шари (collision layers PuzzleScript): тло → підлога з властивістю (клей, яма) → обʼєкти (голова, хвіст, яблуко, гризун, камінь, стіна). Клей і яма не заважають руху — на них можна ступити чи заштовхнути.
- Покроково: хід = одна клавіша. Хід, у якому голова не зрушила, не зараховується (`require_player_movement`). Таймера й випадковості нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Констриктор (голова) | player | вільна / застрягла | крок у 4 напрямки; позаду лишає хвіст; штовхає гризуна чи камінь на 1; зʼїдає яблуко |
| Хвіст | segment | +1 клітина щоходу | нерухомий слід, непрохідний для всіх; разом із головою затискає гризунів |
| Яблуко | pickup | — | зникає, коли голова входить; не штовхається, для штовханих обʼєктів — перешкода |
| Гризун | object | живий / приклеєний / заморожений | штовхається на 1; затиснутий — замерзає й стає нерухомою перешкодою; у ямі — рестарт рівня |
| Камінь | object | вільний / приклеєний | штовхається на 1; заважає; у ямі — засипає її |
| Клей | terrain | — | хто на нього став, приклеюється назавжди |
| Яма з шипами | hazard | — | гризун → рестарт рівня; голова → застрягла; камінь → яма засипана |
| Стіна | static | — | непрохідна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(head+dir)` → ТО `move(head, dir)`, `spawn_at(tail, old_head_cell)` — хвіст лишається слідом, тіло ніколи не коротшає (у сирці: `[ > Player | No Obstacle ] -> [ Tail | Player ]`).
- КОЛИ `input(dir)` → ЯКЩО `occupied(head+dir, rodent|rock)` і `free(cell_behind)` → ТО `push`, `move(head, dir)`, `spawn_at(tail, old_head_cell)`.
- КОЛИ `contact(head, apple)` → ТО `pickup`, `move(head, dir)`, `spawn_at(tail, old_head_cell)`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(head+dir, wall|tail|frozen_rodent|stuck_rodent|stuck_rock)` або за обʼєктом не `free` → ТО `block` (хід не зараховано).
- «Вільно» = нема стіни, хвоста, яблука, гризуна (будь-якого) чи каменя; клей і яма лежать нижчим шаром і рух не блокують.
- КОЛИ `turn_end` → ЯКЩО `custom: «з двох протилежних боків гризуна (ліво-право або верх-низ) — голова чи хвіст змії»` → ТО `transform(rodent, frozen_rodent)`; так само й для приклеєного гризуна.
- КОЛИ `enter(head, glue)` → ТО `set_state(snake, stuck)` — ходити більше не можна, перемога неможлива; застрягла голова вже не рахується тілом для затиску.
- КОЛИ `enter(rodent, glue)` → ТО `set_state(rodent, stuck)` — більше не штовхається, але заморозити його все одно треба.
- КОЛИ `enter(rock, glue)` → ТО `set_state(rock, stuck)` — нерухомий назавжди.
- КОЛИ `enter(rock, pit)` → ТО `disappear_a`, `set_cell(pit, floor)` — камінь і яма зникають, лишається підлога.
- КОЛИ `enter(rodent, pit)` → ТО `restart` — рівень одразу починається спочатку.
- КОЛИ `enter(head, pit)` → ТО `set_state(snake, stuck)`.
- КОЛИ `turn_end` → ЯКЩО `count(apple, ==, 0)` і `count(rodent, ==, 0)` (живих і приклеєних, не заморожених) і `not state(snake, stuck)` → ТО `win`, `next_level`.
- Перемога: усі яблука зʼїдено, усі гризуни заморожені, змія не застрягла. · Поразка: явна лише одна — гризун у ямі (миттєвий рестарт); глухі кути (замурувала себе хвостом, приклеїлась, упала в яму) — undo або рестарт. · Рахунку нема.

## Керування і ввід
- Стрілки — крок голови (стандартний PuzzleScript приймає й WASD).
- Z — скасувати хід (без ліміту), R — рестарт рівня; Esc — назад у титульне меню PuzzleScript (?).
- Клавіша дії (X / Enter) — лише закрити екран-повідомлення.

## Вікна, меню, HUD
- `main-menu` — титульний екран PuzzleScript: «CONSTRICTOR», «by Tom Brinton», початок / продовження гри (?).
- `custom-window` (екран-повідомлення PuzzleScript, `+window:message-screen`) — перед рівнями з новою механікою: «You are CONSTRICTOR, mightiest snake in town.», «Surround rodents on at least two opposite sides to freeze them», «Freeze all rodents AND get all apples!», «Glue is sticky!», «Rocks get in the way!», «Watch out for spike pits!», «Rocks can fill pits!».
- `game-screen` — поле на весь екран; HUD нема.
- `end-screen` — два фінальні повідомлення: «Good work today, CONSTRICTOR.» і «Sleep well.»
- Переходи: main-menu → (повідомлення) → game-screen → (перемога) → наступне повідомлення / рівень → … → фінальні повідомлення.

## Фічі поза полем
- `undo` без ліміту, `restart-level`; рестарт стається й автоматично (гризун у ямі).
- `levels-sequential`: 15 рівнів по черзі, без вибору рівня й без мапи.
- `onboarding-hints` — екрани-повідомлення перед кожною новою механікою (затиск, клей, камені, ями).
- Нема рахунку, підказок, редактора, налаштувань.

## Варіації й родичі
- [Snake](../maze-arcade/snake.md) — там тіло-черга тягнеться за головою; тут тіло — вічний слід, як у [Tron Light Cycles](../maze-arcade/tron-light-cycles.md).
- [Hnefatafl](../chess-abstract/hnefatafl.md) — той самий «затиск з двох боків» (custodian capture), тільки ловить змія.
- Змійки-сокобани корпусу: [Snakebird](snakebird.md) (гравітація), [Would You Love Me If I Was a Snake?](would-you-love-me-if-i-was-a-snake.md) (відкушений хвіст — блок), [Temple of Snek](temple-of-snek.md), [The Snake That Eats Puzzle Game Mechanics](the-snake-that-eats-puzzle-game-mechanics.md).
- **Осі варіацій:** тіло — черга (Snake) / вічний слід (тут) / відкушуваний хвіст · ловля — затиск з двох протилежних боків (тут, Тафл) / оточення з усіх боків (Го) · клей — для всіх обʼєктів (тут) / лише для гравця · яма — засипається каменем / губить ціль (рестарт) / ловить гравця.

## Цікавинки для курсу
- Хвіст як вічний слід і ріст на 1 щоходу: змія сама будує собі лабіринт — 🌱 (одна клітина в множину на хід).
- Затиск із двох протилежних боків, перевірка після кожного ходу для всіх гризунів — 📎.
- Два шари клітини (клей / яма під обʼєктами) і різна реакція кожного типу обʼєкта — 📎.
- Уся гра — 13 правил-перезаписів PuzzleScript (`[A | B] -> [C | D]`) і 4 умови `no X`: міні-інтерпретатор таких шаблонів — 🥉.
- Розвʼязувач BFS: стан = голова + множина хвоста + гризуни й камені; стан лише росте, тож відсікання глухих кутів дає багато — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки; `push-object` ↔ гризуни й камені; `impassable-cells` ↔ стіни, хвіст, заморожені гризуни; `self-collision` + `visited-trail` ↔ хвіст лишається й не пускає; `item-pickup` + `collect-all` ↔ яблука; `fill-hole` ↔ камінь засипає яму; `undo-unlimited`, `restart-level`; `sequential-levels` ↔ 15 рівнів; `level-from-txt` ↔ рівні текстом у сирці PuzzleScript.
- **Нема** → пропозиції карток:
  - `+trail-wall` (вже пропонована Tron) — слід стає стіною.
  - `+grow-every-step` «Тіло росте на 1 щоходу, ніколи не коротшає» · entities/move · 🌱.
  - `+custodian-capture` (вже пропонована Hnefatafl) — тут ловить один гравець власним тілом · entities/combat · 📎.
  - `+sticky-floor` «Клей: хто став — застряг назавжди» · entities/interact · 🌱 · слот {affects: all|player}.
  - `+object-loss-restart` «Втрата важливого обʼєкта — миттєвий рестарт» · game-logic/lose · 🌱.
  - `+level-intro-message` «Екран-повідомлення перед рівнем з новою механікою» · interface/menus · 🌱.

## Пропозиції до словників
- `+effect:leave_trail` — сутність лишає за собою постійний слід (хвіст удава, слід Tron).
- `+cond:sandwiched` — обʼєкт затиснутий з двох протилежних боків сутностями виду (тут — тілом змії).
- `+window:message-screen` — повноекранне текстове повідомлення між рівнями (PuzzleScript `MESSAGE`).
- `+axis:undo` — `unlimited` (Z), плюс автоматичний рестарт за втрату гризуна.
- `+card:grow-every-step`, `+card:custodian-capture`, `+card:sticky-floor`, `+card:object-loss-restart` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch: CONSTRICTOR](https://beepyeah.itch.io/constrictor) — опис («You must eat all the apples and squeeze all the rodents»), керування (стрілки, Z, R), теги, «Made using Puzzlescript», відео-проходження.
- [PuzzleScript-збірка](https://html-classic.itch.zone/html/11728394/index.html) — сирець гри: обʼєкти (Player, Tail, Apple, Victim, Stunned, Glue, Rock, Hole), правила росту хвоста, штовхання, затиску `[ Players | Victims | Players ]`, клею, ям, `late [StuckV Hole] -> RESTART`, умови `no Apple / no Victim / no StuckV / no Stuck`, 15 рівнів і тексти повідомлень.
- [YouTube: проходження від автора](https://www.youtube.com/watch?v=v0pu04b87VA) — посилання вбудоване на сторінці itch.

## Непевне
- (?) Рік 2024 — за датами коментарів на itch (найперший — 16.10.2024) і номером збірки; точна дата публікації на сторінці не показана.
- (?) Пункти титульного меню й дія Esc — стандартна поведінка PuzzleScript, у сирці гри окремо не задані.
