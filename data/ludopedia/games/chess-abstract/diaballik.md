---
title: Diaballik (Діабалік)
slug: diaballik
aka: [Діабалік, Диабалик]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: race
year: 2004
platforms: [board, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Diaballik", best: true, note: "правила: 7×7, по 7 фішок і мʼяч, хід = 2 кроки + 1 пас, носій мʼяча не ходить, пас крізь своїх, анти-гра за глуху стіну"}
  - {kind: wiki, url: "https://fr.wikipedia.org/wiki/Diaballik", note: "FR: 1-2-3-games, перше видання 2002, діагональ = два кроки з вільною проміжною, варіант «по дві фішки в зоні суперника», Senseï"}
  - {kind: play, url: "https://ludii.games/details.php?keyword=Diaballik", note: "Ludii: формалізовані правила (.lud) — старт, лічильники дій, умова «нема шляху + ≥3 дотики»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Diaballik+board+game", note: "пошук; відео не перевіряв"}
stage: v1
coverage: 60
mechanics: [move-4dir, piece-move-patterns, cell-click, drag-drop-piece, selection-highlight, legal-move-highlight, last-move-highlight, turn-enforcement, hot-seat, ai-opponent, ai-minimax, connectivity-check, move-notation, state-as-data, rule-variants, game-screen, end-screen, help-window, undo-step, +action-budget-turn, +ball-pass, +carrier-immobile, +reach-row-win, +anti-blockade-rule]
proposes: ["+cond:actions_left(kind, n)", "+cond:path_clear", "+cond:contacts(side_a, side_b, op, n)", "+trigger:actions_spent", "+ui:pass-lines", "+card:action-budget-turn", "+card:anti-blockade-rule", "+axis:turn-structure=action-points"]
author: opus
date: 2026-11-09
---

# Diaballik — футбол на 7×7: за хід два кроки й один пас, носій мʼяча стоїть, а глуха стіна карається поразкою

## Суть
Абстрактна гра Philippe Lefrançois на двох: у кожного 7 фішок, одна з них тримає мʼяч. За хід — до трьох дій у будь-якому порядку: **два кроки** фішками без мʼяча і **один пас** по вертикалі, горизонталі чи діагоналі будь-якої довжини, якщо між ними нема суперника. Виграє той, хто доставить мʼяч на крайній ряд суперника. Фішки ніколи не знімаються, тож захист — це стіни, а правило анти-гри забороняє глухо замуровуватись.

## Поле і час
- Дошка 7×7 (49 клітин); фішки ходять ортогонально на 1; пас — по 8 лініях.
- Старт (Ludii): 7 фішок кожного на своєму крайньому ряду, мʼяч у центральної фішки.
- Хід = бюджет дій: 2 кроки + 1 пас, у будь-якому порядку, кожна дія необовʼязкова. Кроки можуть робити дві різні фішки або одна двічі.
- Завжди 14 фішок на полі — взяття нема. Варіантів дії за хід — від 200 до 1000 (FR: у середньому ~600).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фішка | piece | колір | крок на 1 ортогонально в порожню клітину; діагональ — два кроки через вільну проміжну |
| Носій мʼяча | piece | колір, тримає мʼяч | не ходить; може лише віддати пас |
| Мʼяч | object | 1 на команду | летить по прямій (8 напрямків) до своєї фішки, якщо між ними нема суперника |
| Крайній ряд суперника | zone | 7 клітин | мʼяч тут (у своєї фішки) → перемога |
| Стіна (блокада) | zone | лінія фішок, по одній у кожній вертикалі | якщо мʼячу суперника нема шляху і ≥3 його фішки торкаються — автор стіни програє |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «по 7 фішок на своєму крайньому ряду, мʼяч у центральної»`.
- КОЛИ `turn_start(side)` → ТО `custom: «бюджет: 2 кроки + 1 пас»`.
- КОЛИ `input(move(piece, dir))` → ЯКЩО `turn_of(side)` and `custom: «кроків лишилось > 0»` and `custom: «фішка без мʼяча»` and `free(cell)` → ТО `move(piece, dir)`, `counter(moves, -1)`.
- КОЛИ `input(move(diagonal))` → ЯКЩО `custom: «лишилось 2 кроки»` and `free(intermediate_cell)` → ТО `custom: «два ортогональні кроки, діагональ між двома фішками заборонена»`.
- КОЛИ `input(pass(to))` → ЯКЩО `custom: «пас ще не витрачено»` and `occupied(to, own_piece)` and `custom: «на одній вертикалі, горизонталі чи діагоналі»` and `custom: «між ними нема фішки суперника (свої не заважають)»` → ТО `throw(ball, to)`, `counter(passes, -1)`.
- КОЛИ `input(move(carrier))` → ТО `block` (носій мʼяча не ходить; одержувач може зробити крок до прийому, але не після).
- КОЛИ `counter(actions, =, 0)` або `input(end_turn)` → ТО `end_turn`.
- КОЛИ `reach(ball, enemy_back_row)` → ТО `win`.
- КОЛИ `turn_end(side)` → ЯКЩО `custom: «сторона A утворила лінію, яку мʼяч B не обійде»` (`path_exists(ball_B, row_A)` хибне, шлях — через порожні й свої клітини) and `custom: «≥3 фішки B ортогонально торкаються фішок A»` → ТО `custom: «A програє»` — B `win` (анти-гра).
- КОЛИ `no_moves(side)` → ТО `custom: «Ludii: суперник, що не може завершити хід, програє»`.
- Перемога: мʼяч на крайньому ряду суперника · анти-гра суперника. Нічиєї в джерелах нема.

## Керування і ввід
- Дошка: пересунути фішку, передати мʼяч рукою; кількість дій рахує сам гравець.
- Цифрова версія: клік по фішці → підсвітка кроків; клік по носію → лінії пасу до своїх фішок (`+ui:pass-lines`); лічильник дій, що лишились (`action-points`); кнопка «Завершити хід».
- Ludii: явний пас (кінець ходу) лише після хоча б однієї дії.

## Вікна, меню, HUD
- (цифрова версія — Ludii; інших не відкривав)
- `main-menu`: гра з AI / удвох, правила.
- `match-setup`: суперник, рівень AI, варіант старту (класика / «по дві фішки в зоні суперника»).
- `game-screen`: дошка 7×7, мʼяч на носії, `turn-indicator`, `action-points` (кроки 2 / пас 1), `legal-move-highlight`, `+ui:pass-lines`, `last-move-highlight` (усі дії ходу суперника), кнопки End turn / Undo.
- `help-window` — правила, анімація пасу й анти-гри.
- `end-screen` — гол / перемога через анти-гру.
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- `ai-opponent-levels`: Ludii-агенти (alpha-beta, MCTS) — (?) рівні не перевіряв.
- `hotseat`, `undo` (у межах ходу — природно для бюджету дій), `replay` — (цифрова версія).
- `custom-rules`: варіант швидкої атаки (по дві фішки вже в зоні суперника).

## Варіації й родичі
- **Варіант швидкої атаки** (FR): кожна команда починає з двома фішками в зоні суперника.
- **Senseï** (Ferti Games) — натхнений Diaballik.
- Родичі: [breakthrough-loa.md](breakthrough-loa.md) (перегони до краю без взяття), [phutball.md](phutball.md) (мʼяч і гравці на полі), [quoridor.md](quoridor.md) (стіни, які не можуть повністю закрити шлях — там заборона, тут кара), [arimaa.md](arimaa.md) (хід як бюджет кроків).
- **Осі варіацій**: бюджет ходу (1 дія / N кроків / N кроків + пас) · пас (лише ортогонально / 8 напрямків; свої блокують / ні) · носій (стоїть / ходить) · анти-блокада (нема / заборона / кара з порогом дотиків) · старт (класика / фішки в зоні суперника).

## Цікавинки для курсу
- Хід як бюджет дій з лічильниками і проміжними станами (undo в межах ходу) — 📎.
- Пас по 8 лініях до першої фішки, крізь своїх, з блоком на суперника — 🌱.
- Анти-гра: BFS від мʼяча через порожні й свої клітини до цільового ряду + підрахунок дотиків ≥3 — 🥉.
- Генерація всіх комбінацій дій за хід (до ~1000) і дедуплікація однакових позицій — 🥈.
- AI: alpha-beta по «макроходах» з оцінкою відстані мʼяча до краю — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `piece-move-patterns` · `cell-click` / `drag-drop-piece` · `selection-highlight` · `legal-move-highlight` · `last-move-highlight` · `turn-enforcement` · `hot-seat` · `ai-opponent` / `ai-minimax` · `connectivity-check` (анти-гра: чи досяжний цільовий ряд) · `move-notation` · `state-as-data` · `rule-variants` · `game-screen` / `end-screen` / `help-window` · `undo-step`.
- **Нема** → пропозиції карток:
  - `+action-budget-turn` «Хід як бюджет дій різних видів» · game-logic/opponent · 📎 · слоти {moves: 2, passes: 1, order: any}.
  - `+ball-pass` «Пас мʼяча по лінії до своєї фішки» · entities/move · 🌱 · слоти {dirs: 8, blockers: enemy}.
  - `+carrier-immobile` — фігура з мʼячем не ходить.
  - `+reach-row-win` — доставити мʼяч/фігуру на крайній ряд (споріднено з `reach-exit`).
  - `+anti-blockade-rule` «Кара за глуху стіну» · game-logic/win · 🥉 · слоти {touch_threshold: 3}.

## Пропозиції до словників
- `+cond:actions_left(kind, n)` — у бюджеті ходу лишилось N дій виду.
- `+cond:path_clear` — лінія між двома клітинами вільна від фішок виду (тут — суперника).
- `+cond:contacts(side_a, side_b, op, n)` — кількість фішок A, що ортогонально торкаються фішок B.
- `+trigger:actions_spent` — бюджет ходу вичерпано.
- `+ui:pass-lines` — лінії можливих пасів від носія.
- `+card:action-budget-turn` · `+card:anti-blockade-rule`.
- `+axis:turn-structure=action-points` — хід як бюджет дій (Diaballik, Tash-Kalar, Arimaa).

## Джерела
- ⭐ [Wikipedia: Diaballik](https://en.wikipedia.org/wiki/Diaballik) — 7×7, 7 фішок і мʼяч, 2 кроки + 1 пас, пас по 8 лініях без суперника між, мета, анти-гра (з неоднозначним формулюванням), 200–1000 варіантів за хід.
- [Wikipedia FR: Diaballik](https://fr.wikipedia.org/wiki/Diaballik) — 1-2-3-games, 2002; діагональ через вільну проміжну; анти-гра «автор стіни програє при 3 дотиках»; варіант; Senseï.
- [Ludii: Diaballik](https://ludii.games/details.php?keyword=Diaballik) — правила й .lud: старт, лічильники 3/2/1, пас крізь своїх, перемога через `not Connectable` + ≥3 дотики.
- YouTube: пошук «Diaballik board game».

## Непевне
- (?) Рік: EN-Wikipedia (категорія) і Ludii — 2004, FR-Wikipedia — перше видання 2002 (1-2-3-games).
- (?) Офіційний сайт diaballik.com не відкривається (DNS) — повних офіційних правил не бачив.
- (?) Програш за «нема ходів» — з короткого опису Ludii; у Wikipedia такого правила нема.
- (?) Чи обовʼязкова хоча б одна дія за хід — офіційно дії необовʼязкові, Ludii вимагає ≥1 перед пасом ходу.
- (?) Цифрові версії, крім Ludii, не шукав; вікна «(цифрова версія)».
