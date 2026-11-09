---
title: Pente (Пенте)
slug: pente
aka: [Пенте, Ninuki-renju, Keryo-Pente]
family: chess-abstract
also: [board-digital]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1977
platforms: [board, web, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pente", best: true, note: "19×19, взяття пари затиском, 5 у ряд або 10 взятих, турнірне правило, варіанти Keryo / Poof / Boat / Ninuki-renju, статистика переваги першого"}
  - {kind: official, url: "https://pente.org/help/helpWindow.jsp?file=playGameRules", note: "Pente.org: правила й таблиця варіантів — Gomoku, Keryo, G-, D-, Poof-, Boat-, DK-, O-Pente, Connect6, Swap2"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pente+board+game+rules", note: "пошук; правила й партії"}
stage: v1
coverage: 75
mechanics: [piece-capture, hot-seat, turn-enforcement, ai-opponent, ai-random, ai-greedy, ai-minimax, cell-click, hover-highlight, last-move-highlight, remaining-counter, online-multiplayer, rating-system, rule-variants, game-screen, main-menu, end-screen, help-window, settings-window, replay, state-as-data, unit-tests, +place-stone, +line-win, +custodial-capture, +capture-count-win, +safe-into-flank, +tournament-opening-rule, +swap-rule, +win-survives-reply, +multi-stone-per-turn]
proposes: ["+cond:sandwiched", "+effect:capture_pair", "+trigger:placed", "+cond:line_breakable", "+ui:capture-tally", "+ui:win-line", "+ui:forbidden-zone", "+window:variant-select", "+window:swap-dialog", "+card:safe-into-flank", "+card:tournament-opening-rule", "+card:win-survives-reply", "+card:multi-stone-per-turn"]
author: opus
date: 2026-11-09
---

# Pente — гомоку з взяттям: склади пʼять у ряд або зніми пʼять пар, затиснувши їх з обох кінців

## Суть
Двоє по черзі ставлять камені на перетини дошки го 19×19; камені не ходять. Перемагає той, хто першим складе **пʼять і більше** в ряд — або хто **візьме 10 каменів** (5 пар). Взяття — «затиск»: якщо рівно два ворожі камені стоять поруч на лінії, а з одного боку вже твій камінь, постав свій з іншого — пара знімається. Відмінність від gomoku (`line-games.md`): лінію можна розірвати взяттям, а загроза взяттям — друга, паралельна дорога до перемоги.

## Поле і час
- Дошка 19×19 перетинів (як го); камені ставлять на перетини, центр — K10 у нотації Pente.org (стовпці A–T, рядки 1–19).
- Покроково, двоє; хід = поставити 1 камінь (Connect6 — 2).
- Першим ходять білі; перший камінь — у центр (турнірне правило).
- Повна інформація, без випадковості; за статистикою, перевага першого ≈ 53 % і росте з рейтингом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Камінь | piece | сторона (білі / чорні) | ставиться з запасу на порожній перетин; не рухається; знімається лише взяттям пари |
| Перетин | static | 19×19 | місце для каменя |
| Пара | zone | рівно 2 сусідні камені одного кольору на лінії | вразлива до затиску; 1 або 3+ — не беруться |
| Лінія з 5 | zone | 5+ своїх поспіль (гор., верт., діаг.) | перемога |
| Лічильник взятих | — | камені, взяті кожною стороною | 10 — перемога |
| Заборонена зона першого гравця | zone | ближче ніж 3 перетини від центру | для другого каменя першого гравця (турнірне правило) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `place(white_stone, center)` (перший камінь — у центр).
- КОЛИ `input(place, stone, cell)` → ЯКЩО `free(cell)` → ТО `place(stone, cell)`, `end_turn`.
- Турнірне правило: КОЛИ `input(place, stone, cell)` → ЯКЩО `custom: «другий камінь першого гравця ближче ніж 3 перетини від центру»` → ТО `block`.
- КОЛИ `after(place)` → ЯКЩО `custom: «у будь-якому з 8 напрямків від нового каменя рівно 2 ворожі, а за ними свій»` (`+cond:sandwiched`) → ТО `custom: «зняти пару»` (`+effect:capture_pair`): `disappear(pair)`, `counter(captured, +2)`. Кілька пар одним ходом — усі знімаються.
- КОЛИ `after(place)` → ЯКЩО `custom: «новий камінь сам утворив пару між двома ворожими»` → ТО нічого — ставити в затиск безпечно.
- КОЛИ `after(place)` → ЯКЩО `custom: «затиснуто 1 або 3+ каменів»` → ТО нічого (Keryo-Pente: 3 теж знімаються).
- КОЛИ `pattern(line(5))` (5 і більше своїх поспіль) → ТО `win`; overline (6+) теж виграє (на відміну від gomoku standard / Ninuki-renju).
- КОЛИ `counter(captured, ≥, 10)` → ТО `win` (Keryo-Pente — 15).
- Boat-Pente: КОЛИ `pattern(line(5))` → ЯКЩО `custom: «суперник може розірвати лінію взяттям пари з неї»` (`+cond:line_breakable`) → ТО гра триває; лінія, що пережила відповідь суперника, виграє.
- Poof-Pente: КОЛИ `after(place)` → ЯКЩО `custom: «новий камінь утворив власну затиснуту пару»` → ТО `disappear(own_pair)`, `counter(captured_by_enemy, +2)`; взяття й «пуфи» рахуються до перевірки лінії; нічиїх нема.
- Connect6: КОЛИ `turn_start(side)` → ЯКЩО `custom: «не перший хід партії»` → ТО `extra_move` (2 камені за хід); мета — 6 у ряд, взяття нема.
- D-Pente: КОЛИ `game_start` → ТО перший ставить 4 камені (2 білі + 2 чорні), другий `choose(keep | swap)`. Swap2: перший ставить 3, другий `choose(white | black | +2 stones and give choice)`.
- КОЛИ `custom: «дошка заповнена без перемоги»` → ТО `draw` (?).
- Перемога: 5 у ряд або 10 взятих · Поразка: суперник раніше · Рахунок: партія 1 / 0, рейтинг на сервері.

## Керування і ввід
- Настільна: камені з чаші на перетини; взяті кладуть собі в лоток-лічильник.
- (цифрова версія) Клік по перетину ставить камінь; наведення показує тінь каменя; у турнірному правилі заборонена зона підсвічена.
- Взяття — автоматично після постановки; знята пара коротко анімується й додається в `capture-tally`.
- Онлайн: хід за ходом у реальному часі або з довгим контролем часу (?).

## Вікна, меню, HUD
(цифрова версія; орієнтир — Pente.org)
- `main-menu`: Грати проти AI · Двоє · Онлайн (лобі, рейтинг) · Правила.
- `variant-select` / `match-setup`: Pente, Keryo, G-, D-, Poof-, Boat-, DK-, O-Pente, Gomoku, Connect6, Swap2; рейтингова чи ні (турнірне правило), контроль часу.
- `swap-dialog` (D-Pente, Swap2): вибір сторони або додаткових каменів.
- `game-screen`: дошка 19×19 з координатами (`cell-coordinates`); `turn-indicator`; `capture-tally` (взяті кожним, з порогом 10/15); `last-move-highlight`; `forbidden-zone` для другого каменя; `win-line` у кінці; `move-list`; `player-clock` онлайн; `resign-button`.
- `end-screen`: «5 у ряд» чи «10 взятих»; зміна рейтингу; Реванш.
- `lobby-window`, `leaderboard` / рейтинг, `replay-window` (архів партій).
- `help-window`: затиск пари, безпечна постановка в затиск, турнірне правило.
- Переходи: main-menu → variant-select → game-screen → end-screen → replay-window / game-screen.

## Фічі поза полем
- `custom-rules` / `rule-variants` — понад 10 наборів правил одним двигуном (Pente.org).
- `online-multiplayer`, рейтинг (`rating-system`), `turn-timer`, `history` / архів партій, `stats` (перевага першого).
- `ai-opponent-levels`; `undo` проти AI; `hint` / аналіз загроз.
- Командна й багатокористувацька гра (пари партнерів або кілька незалежних гравців).

## Варіації й родичі
- Предок — **Ninuki-renju** (15×15, першими чорні, обмеження для першого, overline не виграє).
- **Keryo-Pente**: беруться й трійки, перемога — 15 взятих. **G-Pente**: ще й заборона 2-го каменя на 4-му і 5-му перетині від центру по горизонталі/вертикалі від першого. **D-Pente** / **DK-Pente**: 4 стартові камені + вибір сторони. **Poof-Pente**: самогубна постановка знімає власну пару. **Boat-Pente**: лінію можна «відбити» взяттям. **O-Pente**: Keryo + Poof + Boat.
- **Connect6**: 6 у ряд, по 2 камені за хід, без взяття — родич через Pente.org.
- Без взяття — gomoku / renju (див. `line-games.md`: freestyle vs exactly five, swap/swap2, заборони renju).
- Затиск як взяття: го (`go.md`, але оточення групи), хнефатафл (`hnefatafl.md`, затиск однієї фігури), Baroque chess (`baroque-chess.md`), Reversi (`reversi.md`, затиск перефарбовує замість знімати).
- **Осі варіацій**: розмір групи, що береться (рівно 2 / 2–3 / будь-яка) · постановка в затиск (безпечна / самогубна) · поріг взятих (10 / 15) · overline (виграє / ні) · дебют (центр / турнірне / D / swap2) · каменів за хід (1 / 2) · перевірка лінії (одразу / після відповіді).

## Цікавинки для курсу
- Перевірка 5-в-ряд від останнього каменя в 4 напрямках — 🌱 (база з `line-games.md`).
- Затиск пари в 8 напрямках від нового каменя, з винятком «сам став у затиск» — 🌱.
- Дві умови перемоги одночасно (лінія або квота взятих) — 🌱.
- Набір із 10+ варіантів як конфіг одного двигуна — 🥉.
- Boat-Pente: виграш відкладено до відповіді суперника — 📎.
- AI: пошук загроз (four / open three / загроза взяттям) + alpha-beta — 🥇.

## Мапа на каталог
- Є: `piece-capture` ↔ взяття пари (неточно: тут затиском, не ходом на клітину) · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-random`, `ai-greedy`, `ai-minimax` · `cell-click`, `hover-highlight`, `last-move-highlight` · `remaining-counter` ↔ взяті до порогу · `online-multiplayer`, `rating-system` · `rule-variants` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `replay`, `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+place-stone`, `+line-win` (див. `line-games.md`).
  - `+custodial-capture` (див. `baroque-chess.md`) — тут рівно пара.
  - `+capture-count-win` (див. `abalone.md`) — 10 / 15 взятих.
  - `+swap-rule` (див. `line-games.md`) — D-Pente, Swap2.
  - `+safe-into-flank` «Постановка в затиск безпечна» · entities/legality · 🌱.
  - `+tournament-opening-rule` «Обмеження раннього ходу першого гравця» · game-logic/opponent · 🌱 · слоти {min_distance: 3}.
  - `+win-survives-reply` «Перемога, якщо пережила відповідь суперника» · game-logic/win · 📎.
  - `+multi-stone-per-turn` «Кілька постановок за хід» · game-logic/opponent · 🌱 (Connect6).

## Пропозиції до словників
- `+cond:sandwiched` — уже в `baroque-chess.md`: групу ворогів затиснуто між своїми.
- `+effect:capture_pair` — зняти затиснуту групу заданого розміру.
- `+trigger:placed` — уже в `line-games.md`: камінь поставлено (тут через `after(place)`).
- `+cond:line_breakable` — суперник може розірвати лінію взяттям (Boat-Pente).
- `+ui:capture-tally` — лічильник взятих з порогом перемоги · `+ui:win-line` (уже в `line-games.md`) · `+ui:forbidden-zone` — підсвічена зона заборони для ходу.
- `+window:variant-select`, `+window:swap-dialog` — уже в `line-games.md`.
- `+card:safe-into-flank` · `+card:tournament-opening-rule` · `+card:win-survives-reply` · `+card:multi-stone-per-turn` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Pente](https://en.wikipedia.org/wiki/Pente) — 19×19, білі першими, турнірне правило (центр, другий ≥3 від центру), взяття рівно двох затиском, безпечна постановка в затиск, 5+ у ряд або 10 взятих, Keryo / Poof / Boat / Ninuki-renju / multiplayer, Гері Габрел 1977, Pente.org (нотація A–T/1–19, swap2), статистика ≈53 %.
- [Pente.org: правила](https://pente.org/help/helpWindow.jsp?file=playGameRules) — базові правила і таблиця варіантів: Gomoku, Keryo, G-, D-, Poof- (до 5 каменів пуфом, нічиїх нема), Boat-, DK-, O-Pente, Connect6, Swap2.
- YouTube: пошук «Pente board game rules».

## Непевне
- (?) Нічия при заповненій дошці — у джерелах не сказано явно (лише для Poof-Pente «draws are not possible»).
- (?) Чи одним ходом можна взяти кілька пар у різних напрямках — логічно так (кожна затиснута пара знімається), явно в джерелах не прочитав.
- (?) Режими часу й асинхронні («поштою») партії на Pente.org — не перевірено.
- (?) Розвʼязаність Pente — у джерелах нема; freestyle gomoku розвʼязаний (див. `line-games.md`), Pente — ні (?).
