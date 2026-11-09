---
title: Trouballs
slug: trouballs
aka: []
family: falling-match
also: [connect-rotate]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2001
platforms: [Game Boy Color]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Trouballs", best: true, note: "суть: колеса-шестерні, групи по 4 і 6, два режими, життя"}
  - {kind: other, url: "https://retro-replay.com/db/game-boy-color/trouballs", note: "огляд: шестерні за групою, обертання в обидва боки, таймер з бонусом часу, фіксовані кілки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=trouballs+game+boy+color+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [tile-rotate, gravity-fall, chain-reaction, time-out, time-bonus, player-death, sequential-levels, level-select, tutorial-window, event-points, score-records, +gear-rotate-group, +rectangle-group-match, +clear-all-goal, +fixed-peg]
proposes: ["+effect:rotate_ring", "+role:rotator", "+card:gear-rotate-group", "+card:rectangle-group-match"]
author: opus
date: 2026-11-09
---

# Trouballs — крутиш шестерні під кулями, щоб зібрати прямокутник з 4 або 6 однакових

## Суть
Кольорові кулі закріплені на полі навколо шестерень-обертачів. Гравець не рухає кулі поодинці — він **обирає шестерню й крутить її** за або проти годинникової, і всі кулі, що прилягають до неї, переїжджають по колу. Коли однакові кулі складаються в «коробку» з 4 або 6 (прямокутник), вона зникає. Мета рівня — прибрати всі кулі до кінця таймера.

## Поле і час
- Сітка куль із розставленими між ними шестернями; розмір поля і скільки куль навколо шестерні — не підтверджено (?).
- Пізніші рівні — шестерні-перешкоди й фіксовані кілки, що обмежують шляхи обертання.
- Real-time таймер рівня; швидке очищення додає секунди.
- У режимі «ever more balls» кулі продовжують падати згори — треба не дати екрану заповнитись.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор | player | шестерня під ним | обирає шестерню, крутить її |
| Куля | tile | колір | їде по колу разом із шестернею; група 4/6 у прямокутнику зникає |
| Шестерня-обертач | switch | напрям ↻/↺ | обертає всі прилеглі кулі на крок |
| Шестерня-перешкода | static | — | заважає обертанню (?) |
| Фіксований кілок | static | — | не обертається, обмежує шлях |
| Лебідка | object | — | згадана як рухомий елемент поля (?) |
| Падаюча куля | tile | колір | режим 2: зʼявляється згори й падає (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select)` → ТО `move(cursor, gear)`.
- КОЛИ `input(rotate_cw|rotate_ccw)` → ТО `custom: «rotate_ring — кулі навколо шестерні зсуваються по колу на крок»`.
- КОЛИ `pattern(group(4|6, same_color))` у формі прямокутника → ТО `clear(group)`, `score(n)`.
- КОЛИ `after(clear)` → ТО `fall(balls_above)` (?); КОЛИ `settled` → ЯКЩО новий прямокутник → ТО ланцюг.
- КОЛИ одним поворотом складено кілька груп → ТО `combo(+1)` (гравці готують кілька груп і замикають одним поворотом).
- КОЛИ `after(clear)` → ЯКЩО очищено швидко → ТО `timer(+n)`.
- КОЛИ `all_gone(ball)` → ЯКЩО `mode(set_number)` → ТО `win`, `next_level`.
- КОЛИ `timer(=0)` → ТО `lives(-1)`; КОЛИ `counter(lives, =, 0)` → ТО `custom: «повернення на перший рівень»`.
- КОЛИ `timer(every)` → ЯКЩО `mode(ever_more_balls)` → ТО `spawn_at(ball, top)`; КОЛИ екран заповнено → ТО `lives(-1)` (?).
- Перемога: прибрати всі кулі (режим 1) / протриматись до кінця часу (режим 2) · Поразка: усі життя втрачено · Рахунок: очки за групи, бонус часу.

## Керування і ввід
- Хрестовина — вибір шестерні; дві кнопки — крутити за / проти годинникової (?).
- Головна навичка — планувати, як один поворот зсуне кілька куль одразу.

## Вікна, меню, HUD
- `main-menu` → вибір режиму: «set number» / «ever more balls».
- `level-select` з іконками складності; перші рівні — навчальні (`tutorial-window`).
- `game-screen`: поле, курсор на шестерні, `timer-countdown`, `lives`, `score`.
- `end-screen` рівня.

## Фічі поза полем
- Понад 100 рівнів (текст коробки).
- Два режими; режиму без таймера нема (оглядач про це шкодує).
- Збереження / паролі — не підтверджено (?).

## Варіації й родичі
- Обертання групи куль навколо центру — родич [connect-rotate](../connect-rotate/) (повороти плиток) і Hexic (обертання трійки) (?).
- Збіг-прямокутник — як квадрати [lumines](lumines.md) і [puzzle-scape](puzzle-scape.md).
- **Осі варіацій**: що обертається (плитка / кільце куль навколо вузла / трійка) · форма збігу (лінія / квадрат / прямокутник 4–6) · подача (фіксований набір / падіння згори).

## Цікавинки для курсу
- Обертання кільця клітин навколо вузла-шестерні — 📎: циклічний зсув списку сусідів.
- Пошук прямокутника 2×2 / 2×3 одного кольору — 🌱.
- Фіксовані кілки, що вилучають клітину з кільця — 🌱.
- Режим «фіксований набір» як пазл: розвʼязувач мінімальних поворотів — 🥈.

## Мапа на каталог
- Є: `tile-rotate` (найближча: поворот як хід) · `gravity-fall` (?) · `chain-reaction` · `time-out` · `time-bonus` · `player-death` (життя) · `sequential-levels` · `level-select` · `tutorial-window` · `event-points` · `score-records`.
- **Нема** → пропозиції карток:
  - `+gear-rotate-group` «Обертання кільця клітин навколо вузла» · entities/legality · 📎 · слоти {ring: 4|6|8, dir: cw|ccw}.
  - `+rectangle-group-match` «Прямокутник 2×2 / 2×3 одного кольору зникає» · entities/interact · 🌱.
  - `+clear-all-goal` «Прибрати всі плитки рівня» · game-logic/win · 🌱.
  - `+fixed-peg` «Нерухома клітина в кільці обертання» · entities/legality · 🌱.

## Пропозиції до словників
- `+effect:rotate_ring` — циклічний зсув сутностей навколо вузла (Trouballs, Hexic (?)).
- `+role:rotator` — вузол поля, що обертає сусідні клітини (шестерня).
- `+card:gear-rotate-group` · `+card:rectangle-group-match`.

## Джерела
- ⭐ [Wikipedia: Trouballs](https://en.wikipedia.org/wiki/Trouballs) — колеса, групи 4 і 6, два режими, життя і повернення на перший рівень; Paragon Five / Capcom, 2001.
- [Retro Replay: Trouballs](https://retro-replay.com/db/game-boy-color/trouballs) — шестерні за групами куль, обертання в обидва боки, таймер і бонус часу, кілки, навчальні рівні, вибір рівня з іконками.
- YouTube: пошук «trouballs game boy color gameplay».

## Непевне
- (?) Скільки куль навколо шестерні (4? 6? 8?) і чи шестерні ділять кулі між собою — не знайдено.
- (?) Точна форма груп: «boxes of four or six» — читаю як прямокутники 2×2 і 2×3.
- (?) Чи падають кулі після зникнення в режимі 1; що таке «moving winches».
- (?) Кількість життів, довжина таймера, паролі.
- (?) «Понад 100 рівнів» — з тексту коробки, цитованого в пошуку.
- Опис найбідніший у хвилі: джерел із правилами майже нема (MobyGames — 403).
