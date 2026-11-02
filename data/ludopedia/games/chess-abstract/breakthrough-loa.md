---
title: Breakthrough і Lines of Action (Прорив і Лінії дії)
slug: breakthrough-loa
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: none
  goal: race
year: 1969
platforms: [board, PC, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lines_of_Action", note: "LOA: правила, одночасне зʼєднання, MSO-чемпіонати, Scrambled Eggs"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Breakthrough_(board_game)", best: true, note: "Breakthrough: правила на одному екрані, розвʼязані малі дошки"}
  - {kind: play, url: "https://playabstractgames.com/en/breakthrough/", note: "Breakthrough у браузері проти AI"}
  - {kind: play, url: "https://playabstractgames.com/en/lines-of-action/", note: "LOA у браузері, «Practice vs AI»"}
  - {kind: play, url: "https://martinmspedersen.github.io/Breakthrough-Web/", note: "відкрита веб-версія Breakthrough (лінк зі статті Wikipedia)"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=lines+of+action", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=lines+of+action+board+game+rules", note: "пошук; правила LOA"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=breakthrough+board+game+troyka", note: "пошук; партії Breakthrough"}
stage: v1
coverage: 80
mechanics: [piece-move-patterns, piece-capture, move-8dir, destroy-all-enemies, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-random, ai-greedy, ai-minimax, cell-click, legal-move-highlight, hover-highlight, drag-drop-piece, game-screen, end-screen, help-window, field-size-picker, replay, reachability-check, +reach-row-win, +line-count-move, +jump-own-only, +connect-all-win, +move-notation]
proposes: ["+cond:connected", "+cond:line_count", "+cond:path_clear", "+trigger:connected", "+ui:group-outline", "+axis:win-condition", "+card:line-count-move", "+card:jump-own-only", "+card:connect-all-win"]
author: opus
date: 2026-11-02
---

# Breakthrough і Lines of Action — два «чистих» абстракти: гонка пішаків до тилу і зʼєднання всіх фішок у групу

## Суть
Парасолька над двома мінімалістичними абстрактами на 8×8, де вся глибина — з одного-двох правил. **Breakthrough** (Dan Troyka, 2000): 16 «пішаків» на сторону ходять лише вперед, бʼють по діагоналі; хто першим дійде до тилу — виграв. **Lines of Action** (Claude Soucie, 1969; популяризував Sid Sackson): фішка ходить рівно на стільки клітин, скільки фішок стоїть на лінії руху; мета — зібрати всі свої фішки в одну звʼязну групу. Обидві — еталонні полігони для AI (minimax/MCTS).

## Поле і час
- Обидві: дошка 8×8 (Breakthrough масштабується на будь-який прямокутник — по 2 ряди фішок кожному), хід = одне переміщення однієї фішки, нічиїх фактично нема.
- **Breakthrough**: білі (1–2 ряди) проти чорних (7–8 ряди), по 16 фішок; перший хід — за домовленістю.
- **LOA**: по 12 фішок; чорні на b1–g1 і b8–g8, білі на a2–a7 і h2–h7 (кути порожні); чорні ходять першими.
- Звʼязність у LOA — 8-сусідство (ортогонально й діагонально).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фішка Breakthrough | piece | сторона, напрям «вперед» | крок 1 прямо або діагонально вперед на порожню; бʼє лише діагонально вперед |
| Тил суперника (BT) | zone | дальній ряд | фішка тут = перемога |
| Фішка LOA | piece | сторона | рух по 8 напрямках рівно на N клітин, N = усі фішки на цій лінії (обидва кольори) |
| Лінія руху (LOA) | zone | рядок/стовпець/діагональ | визначає довжину кроку; свої фішки можна перестрибувати, чужі — ні |
| Група (LOA) | zone | 8-звʼязна множина своїх фішок | одна група = перемога |

## Правила (КОЛИ → ЯКЩО → ТО)
**Breakthrough**
- КОЛИ `input(move(p, to))` → ЯКЩО `turn_of(side)` and `custom: «to — прямо або діагонально вперед на 1»` and `free(to)` → ТО `move(p, to)`, `end_turn`.
- КОЛИ `input(move(p, to))` → ЯКЩО `custom: «to — діагонально вперед»` and `occupied(to, enemy)` → ТО `disappear_b`, `move(p, to)` (взяття необовʼязкове, без ланцюгів).
- КОЛИ `reach(p, far_row)` → ТО `win(side(p))`.
- КОЛИ `all_gone(enemy_pieces)` → ТО `win`.
- Нічия неможлива: передова фішка завжди має діагональний хід (або хід уже виграшний).

**Lines of Action**
- КОЛИ `input(move(p, dir))` → ТО `custom: «n = line_count(p, dir)»` — кількість усіх фішок на всій лінії (обидва боки від p, включно з нею).
- ЯКЩО `custom: «клітина на відстані n у межах поля»` and `not occupied(path, enemy)` (свої — можна перестрибнути) and `not occupied(target, own)` → ТО `move(p, target)`.
- ЯКЩО `occupied(target, enemy)` → ТО `disappear_b` (взяття приземленням), `move(p, target)`.
- КОЛИ `turn_end(side)` → ЯКЩО `connected(own_pieces, 8)` → ТО `win(side)`; одна фішка = звʼязна → перемога.
- КОЛИ `turn_end(side)` → ЯКЩО взяття зробило звʼязними **обидві** сторони → ТО за оригіналом `win(mover)`, за сучасними турнірними правилами (MSO) — `draw`.
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` → ТО `pass_turn` (?).
- Перемога: BT — дійти до тилу / знищити всіх · LOA — одна група. Рахунок: 1/0.

## Керування і ввід
- Обидві: клік по фішці → підсвічені легальні цілі → клік або drag (Play Abstract Games, Wikipedia-лінкові клієнти).
- У LOA підсвітка особливо важлива: довжина кроку не очевидна людині — клієнт рахує фішки на лінії.
- Нотація шахова: `a2-b3`, взяття `a2xb3` (?).

## Вікна, меню, HUD
- `game-screen` (цифрова версія): дошка, `legal-move-highlight`, `turn-indicator`, `captured-pieces` / `piece-count-bar`, `move-list`; LOA — `group-outline` (контур/кількість груп кожної сторони).
- `match-setup`: розмір дошки (BT — довільний прямокутник), рівень AI, колір.
- `help-window`: правила; `end-screen`: «прорив» / «зʼєднав усі» / одночасне зʼєднання.
- Переходи: main-menu → match-setup → game-screen → end-screen → replay.

## Фічі поза полем
- `ai-opponent-levels`, `hotseat`, `online-multiplayer` на сайтах абстрактних ігор; `replay`.
- `custom-difficulty` / `field-size-picker` — Breakthrough на 5×5, 6×6, 7×7 (малі розвʼязані: 6×6 — перемога першого; 6×5, 5×5, 3×7 — другого).
- LOA: щорічні чемпіонати світу на Mind Sports Olympiad (з 1997); рекомендовано Spiel des Jahres 1988.
- Breakthrough виграв 8×8 Game Design Competition 2001 (Zillions of Games).

## Варіації й родичі
- LOA: **Scrambled Eggs** (інша стартова розстановка, Soucie) · «Black hole» (?) — згадано Wikipedia без деталей.
- Breakthrough: розміри поля, асиметричні армії (?).
- Родичі: шашки й шахові пішаки (рух вперед), Hex (мета-зʼєднання) [hex.md](hex.md), Arimaa (гонка кролика) [arimaa.md](arimaa.md), Quoridor (гонка до краю) [quoridor.md](quoridor.md).
- **Осі варіацій**:
  - **Довжина кроку**: фіксована 1 (BT) · будь-яка до упору (тура) · **обчислена з поля** (LOA: кількість фішок на лінії) · за кубиком.
  - **Перестрибування**: нема · через свої (LOA) · через будь-які (кінь) · з взяттям (шашки).
  - **Мета**: дійти рядом (BT) · зʼєднати всі свої (LOA) · зʼєднати сторони (Hex) · знищити всіх.

## Цікавинки для курсу
- Breakthrough цілком — 🌱 логіка + 📎 AI-жадібний: найпростіша «повна» настільна гра для першої лаби.
- AI для Breakthrough (minimax/alpha-beta з оцінкою «просування + захист») — 🥇; розвʼязання 5×5 перебором — 👑 (?).
- LOA: довжина кроку = кількість фішок на лінії, з перевіркою «не через чужі» — 📎.
- LOA: перемога за звʼязністю (flood fill 8-сусідства) після кожного ходу + одночасне зʼєднання — 📎.
- Параметризований розмір поля з автогенерацією стартової розстановки (BT) — 🌱.

## Мапа на каталог
- Є: `piece-move-patterns` (BT-пішак, LOA-крок) · `piece-capture` · `move-8dir` (LOA) · `destroy-all-enemies` (BT) · `hot-seat` · `turn-enforcement` · `move-timer` · `ai-opponent` / `ai-random` / `ai-greedy` / `ai-minimax` · `cell-click` + `legal-move-highlight` + `hover-highlight` + `drag-drop-piece` · `game-screen` · `end-screen` · `help-window` · `field-size-picker` · `replay` · `reachability-check` ↔ звʼязність групи.
- **Нема** → пропозиції карток:
  - `+reach-row-win` (з quoridor/checkers) — Breakthrough.
  - `+line-count-move` «Крок = кількість фішок на лінії» · entities/legality · 📎 — LOA.
  - `+jump-own-only` «Перестрибувати лише свої» · entities/legality · 🌱 · слоти {over: own|any|none}.
  - `+connect-all-win` «Зʼєднати всі свої фігури» · game-logic/win · 📎 · слоти {adjacency: 4|8, simultaneous: draw|mover} — LOA (≠ `+connect-sides-win` Hex).
  - `+move-notation` — запис партій.

## Пропозиції до словників
- `+cond:connected` (🔥 нове, ×4) — підтверджую: усі фішки сторони в одній 8-звʼязній групі.
- `+cond:line_count(p, dir)` — скільки фішок на лінії через клітину (LOA) — без нього довжина кроку лише `custom`.
- `+cond:path_clear(a, b)` — пряма лінія вільна (тут — від чужих фішок); див. amazons.md.
- `+trigger:connected` — підтверджую (з hex.md): склалось зʼєднання.
- `+ui:group-outline` — обвести/порахувати групи сторони (LOA, го).
- `+axis:win-condition` — значення `race` (BT) і `connect-all` (LOA).

## Джерела
- ⭐ [Wikipedia: Breakthrough](https://en.wikipedia.org/wiki/Breakthrough_(board_game)) — рух/взяття, перемога, неможливість нічиї, розвʼязані малі дошки, Troyka і конкурс 2001.
- [Wikipedia: Lines of Action](https://en.wikipedia.org/wiki/Lines_of_Action) — рух на N клітин, стрибки через свої, одночасне зʼєднання (оригінал vs MSO), чемпіонати, Scrambled Eggs.
- [Play Abstract Games: Breakthrough](https://playabstractgames.com/en/breakthrough/) — гра проти AI (лінк зі статті Wikipedia).
- [Play Abstract Games: Lines of Action](https://playabstractgames.com/en/lines-of-action/) — правила коротко, «Practice vs AI».
- [Breakthrough-Web](https://martinmspedersen.github.io/Breakthrough-Web/) — відкрита веб-версія.
- YouTube: пошуки «lines of action board game rules», «breakthrough board game troyka».

## Непевне
- (?) Стартова розстановка LOA (чорні b1–g1/b8–g8, білі a2–a7/h2–h7) — з памʼяті; сторінки, які відкривав, її не наводять.
- (?) Що робить у LOA гравець без ходів (пас) — не перевірено; так само деталі «Black hole» і комп'ютерної гри (MIA, розвʼязання малих дощок).
- (?) Нотація, розвʼязання 5×5 BT перебором як навчальне завдання — оцінка, не факт.
- `year: 1969` — за LOA; Breakthrough — 2000.
