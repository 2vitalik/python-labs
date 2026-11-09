---
title: Three Musketeers (Три мушкетери)
slug: three-musketeers
aka: [Три мушкетери, 3 Musketeers]
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
year: 1969
platforms: [board, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Three_Musketeers_(game)", best: true, note: "редірект на розділ A Gamut of Games: розстановка (кути + центр), хід мушкетера = взяття сусіда, хід ворога = крок у порожню, обидві умови перемоги, маскот Zillions"}
  - {kind: play, url: "https://ludii.games/details.php?keyword=Three%20Musketeers", note: "Ludii: 5×5, 3 мушкетери проти 22 ворогів, «вороги виграють, якщо мушкетери будь-коли на одній лінії», 1969, Haar Hoolim"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Three+Musketeers+board+game+Sackson", note: "пошук; партії"}
stage: v1
coverage: 80
mechanics: [piece-move-patterns, piece-capture, move-4dir, no-moves-left, hot-seat, turn-enforcement, ai-opponent, ai-minimax, level-solver, cell-click, drag-drop-piece, legal-move-highlight, selection-highlight, last-move-highlight, remaining-counter, mode-indicator, game-screen, main-menu, end-screen, help-window, settings-window, state-as-data, unit-tests, +asymmetric-sides, +capture-only-move, +align-opponent-win, +stalemate-win, +side-swap-match]
proposes: ["+trigger:aligned", "+cond:can_capture", "+window:side-select", "+feature:side-swap-match", "+card:capture-only-move", "+card:align-opponent-win"]
author: opus
date: 2026-11-09
---

# Three Musketeers — троє ходять лише взяттям, двадцять двоє лише відступають; вишикуй мушкетерів в одну лінію

## Суть
Асиметрична гра на дошці 5×5: три мушкетери проти 22 солдатів кардинала Рішельє. Мушкетер **може ходити лише взяттям** — на сусідню клітину з ворогом; ворог ходить лише на сусідню порожню клітину й не бʼє ніколи. Вороги виграють, якщо всі три мушкетери опиняться на одному рядку або стовпці; мушкетери виграють, коли на своєму ході не мають кого бити. Парадокс гри: сильна сторона програє, коли надто «вдало» бʼє, а слабка виграє відступом.

## Поле і час
- Квадратна дошка 5×5 (25 клітин), один шар, у клітині ≤1 фішка.
- Сусідство — ортогональне (4 напрямки) за Wikipedia; діагоналей нема.
- Старт: дошка заповнена повністю — 3 мушкетери (два протилежні кути + центр) і 22 вороги на решті клітин; перший хід — мушкетерів.
- Покроково, по одній фішці за хід; поле лише рідшає (мушкетери прибирають ворогів, нових фішок нема).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мушкетер | piece | ×3; сторона musketeers | хід = взяття ортогонально сусіднього ворога (стає на його клітину); на порожню не ходить |
| Ворог (солдат Рішельє) | piece | ×22; сторона enemy | хід = крок на ортогонально сусідню порожню клітину; не бʼє |
| Клітина | terrain | 25 | порожня або зайнята однією фішкою |
| Рядок / стовпець | zone | 5 + 5 | три мушкетери в одному — перемога ворогів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «мушкетери в двох протилежних кутах і в центрі, 22 вороги на всіх інших клітинах»`; першим ходить мушкетер.
- КОЛИ `input(move, musketeer, dir)` → ЯКЩО `occupied(next_cell, enemy)` → ТО `disappear(enemy)`, `move(musketeer, dir)`, `end_turn`.
- КОЛИ `input(move, musketeer, dir)` → ЯКЩО `free(next_cell)` або `occupied(next_cell, musketeer)` → ТО `block` — мушкетер не ходить без взяття.
- КОЛИ `input(move, enemy, dir)` → ЯКЩО `free(next_cell)` → ТО `move(enemy, dir)`, `end_turn`.
- КОЛИ `input(move, enemy, dir)` → ЯКЩО `occupied(next_cell, any)` → ТО `block` — ворог ніколи не бʼє.
- КОЛИ `input(move, piece, diagonal)` → ТО `block` (лише ортогонально, за Wikipedia).
- КОЛИ `after(move)` → ЯКЩО `custom: «усі три мушкетери на одному рядку або одному стовпці»` (`+trigger:aligned`) → ТО `win(enemy)` — навіть якщо мушкетери вишикувались власним ходом (Ludii: «are ever on the same line or column»).
- КОЛИ `turn_start(musketeers)` → ЯКЩО `no_moves(musketeers)` — жоден мушкетер не має ортогонально сусіднього ворога (`not can_capture`) → ТО `win(musketeers)`.
- КОЛИ `turn_start(side)` → ТО пас неможливий: хто має хід — мусить ходити (мушкетер — бити, навіть на шкоду собі).
- Перемога ворогів: три мушкетери на одній лінії · Перемога мушкетерів: на своєму ході нема кого бити · Рахунок: нема; партія 1 / 0.

## Керування і ввід
- Настільна: 3 фішки одного кольору й 22 іншого (у Sackson — гральні карти / жетони (?)); хід — пересунути фішку на сусідню клітину, взяту прибрати.
- (цифрова версія) Клік по своїй фішці → підсвітка 1–4 сусідніх цілей: для мушкетера — лише клітини з ворогами, для ворога — лише порожні; клік по цілі. Drag-n-drop на сусідню клітину.
- Перед партією — вибір сторони (людина за мушкетерів чи за ворогів).

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Грати → `side-select` (мушкетери / вороги) → рівень AI · Двоє за одним пристроєм · Правила → `help-window` · `settings-window`.
- `game-screen`: дошка 5×5; `turn-indicator` (чий хід); `remaining-counter` — скільки ворогів лишилось; `legal-move-highlight` (для мушкетерів — лише взяття); `last-move-highlight`; підсвітка рядка/стовпця, де вже стоять два мушкетери (`threat-range` для мушкетерів (?)); `undo-button` проти AI.
- `end-screen`: «Мушкетерів вишикувано» / «Мушкетерам нема кого бити»; реванш зі зміною сторін.
- Переходи: main-menu → side-select → game-screen → end-screen.

## Фічі поза полем
- `ai-opponent-levels` за будь-яку сторону; Zillions of Games — гра була маскотом цього рушія.
- `side-swap-match` — дві партії з обміном сторін для чесного порівняння (звичай асиметричних ігор, правилами не вимагається (?)).
- `undo`, `replay`, розвʼязувач позицій (`level-solver`) як режим «задачі».

## Варіації й родичі
- Джерело: Sid Sackson, A Gamut of Games (1969), розділ «Game Inventors Are People Too»; автор — Haar Hoolim.
- Асиметричні «полювання» з різними силами й цілями: [bagh-chal](bagh-chal.md) (тигри й кози), [hnefatafl](hnefatafl.md), [guerrilla-checkers](guerrilla-checkers.md), Fox and Geese — Wikipedia ставить Three Musketeers в один ряд із ним.
- «Ходити можна лише взяттям» — як примусові взяття в [checkers](checkers.md) і Peg Solitaire ([peg-solitaire](peg-solitaire.md) — кожен хід теж знімає фішку).
- Лінія як поразка — дзеркало k-в-ряд з [line-games](line-games.md): тут вишикувати мушкетерів намагається **суперник**.
- **Осі варіацій**: хто бʼє (обидві сторони / лише сильна) · ціль сильної сторони (з'їсти всіх / лишитись без ходів) · ціль слабкої (оточити / вишикувати) · сусідство (4 / 8).

## Цікавинки для курсу
- Два різні генератори ходів для двох сторін (лише взяття / лише крок у порожню) — 🌱.
- Перевірка «три фігури на одному рядку або стовпці» після кожного ходу — 🌱.
- Перемога через відсутність ходів (`no_moves` = виграш, а не програш) — 🌱.
- Minimax / alpha-beta для обох сторін; оцінка — «розкиданість» мушкетерів і число сусідніх ворогів — 🥉.
- Повний розвʼязок гри перебором станів з мемоізацією (позиції 3 мушкетерів × підмножина ворогів) — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ два різні патерни сторін · `piece-capture` ↔ взяття мушкетером · `move-4dir` ↔ ортогональне сусідство · `no-moves-left` ↔ детектор «нема кого бити» (з оберненим наслідком) · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-minimax`, `level-solver` · `cell-click`, `drag-drop-piece`, `legal-move-highlight`, `selection-highlight`, `last-move-highlight`, `remaining-counter`, `mode-indicator` ↔ чия сторона ходить · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+asymmetric-sides` (див. [bagh-chal](bagh-chal.md)), `+stalemate-win` «Пат = перемога запатованого» (див. [duck-chess](duck-chess.md)), `+side-swap-match` (див. [hnefatafl](hnefatafl.md)).
  - `+capture-only-move` «Фігура ходить лише взяттям» · entities/legality · 🌱 — Three Musketeers, Peg Solitaire.
  - `+align-opponent-win` «Перемога — вишикувати фігури суперника в лінію» · game-logic/win · 🌱 · слоти {k: 3, lines: rows|cols|diag}.

## Пропозиції до словників
- `+trigger:aligned` — усі фігури виду на одній прямій (рядок / стовпець / діагональ).
- `+cond:can_capture` — у сторони є хоч одне взяття (тут: інакше мушкетери виграють).
- `+window:side-select` — вибір сторони в асиметричній грі.
- `+feature:side-swap-match` — матч із двох партій зі зміною сторін.
- `+card:capture-only-move`, `+card:align-opponent-win` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Three Musketeers (game)](https://en.wikipedia.org/wiki/Three_Musketeers_(game)) — редірект на статтю A Gamut of Games: повний текст правил (розстановка, черговість, ходи обох сторін, умови перемоги), Haar Hoolim, звʼязок із Fox and Geese, маскот Zillions.
- [Ludii: Three Musketeers](https://ludii.games/details.php?keyword=Three%20Musketeers) — 5×5, 3 проти 22, «мушкетери ходять лише взяттям», «вороги виграють, якщо мушкетери будь-коли на одній лінії», 1969.

## Непевне
- (?) Сусідство мушкетера: Wikipedia — ортогонально, Ludii — «any adjacent space» (на квадратній дошці Ludii, ймовірно, теж ортогонально).
- (?) Що буває, коли вороги не мають жодного ходу (нема порожньої клітини поруч із жодним ворогом) — джерела не кажуть.
- (?) Порядок перевірок, коли мушкетер власним ходом і вишикувався, і лишився без цілей: за Ludii «будь-коли на одній лінії» — перемога ворогів, але явно не прописано.
- (?) Чим грали в книжці Sackson (жетони / карти) і чи «Haar Hoolim» — справжнє імʼя.
- (?) Розвʼязаність гри й перевага сторони — не бачив у джерелах.
