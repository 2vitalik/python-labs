---
title: Piping Hot
slug: piping-hot
aka: []
family: connect-rotate
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: state
year: 2019
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1168160/Piping_Hot/", best: true, note: "єдиний опис правил: поворот труб, нагрівач посередині, кілька поверхів одночасно, вода наздоганяє, gold за найбільше труб, режим Unlimited"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Piping+Hot+Odd+Digs", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [tile-rotate, pipe-connectors, cell-click, connectivity-check, reachability-check, completion-detection, time-out, sequential-levels, level-select, mode-select, game-screen, +flow-propagation, +must-visit-checkpoints, +multi-board-field, +path-length-rating, +procedural-levels]
proposes: ["+cond:path_through(a, via, b)", "+ui:board-tabs", "+card:path-length-rating", "+card:procedural-levels"]
author: opus
date: 2026-11-09
---

# Piping Hot — поверни труби від входу до виходу через нагрівач, на кількох поверхах, поки вода наздоганяє

## Суть
Пазл на поворот труб (як мобільний Plumber / Pipes): клітини з відрізками труб, клік повертає відрізок, мета — звʼязати стартовий блок із кінцевим. Дві особливості: шлях **мусить пройти через нагрівач** посередині поля, і гравець веде **кілька поверхів одночасно**, перемикаючись між ними, бо на кожному тече своя вода. Коли таймер вичерпано, вода рушає — і це перегони: дотягти шлях до кожного кінцевого блока раніше за неї. Оцінка — за довжиною: gold за найбільше задіяних труб, або челендж «найменше труб».

## Поле і час
- Квадратна сітка труб на кожному поверсі; поверхи — окремі поля, між якими гравець перемикається (?) — чи поєднані труби між поверхами, невідомо.
- Спершу таймер (планування з поворотами), потім вода тече по зʼєднаних трубах у реальному часі (`time: realtime`).
- Рівні двох видів: ручні (Levels) і процедурні (Unlimited) — звідси `random: setup`.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Відрізок труби | tile | форма (?), орієнтація | клік повертає; зʼєднання = збіг портів сусідів |
| Стартовий блок | static | — | джерело води (source) |
| Кінцевий блок | static | — | ціль шляху (sink); на кожному поверсі свій |
| Нагрівач (heating pipe) | static | — | обовʼязкова точка шляху посередині поля |
| Вода | object | фронт потоку | після таймера тече зʼєднаними трубами; «наздоганяє» гравця |
| Поверх | zone | своє поле, свій таймер (?) | розвʼязується паралельно з іншими |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, pipe)` → ТО `rotate(pipe, 90)`.
- КОЛИ `input(switch_floor)` → ТО `custom: «показати інший поверх»` — інші поверхи тим часом не стоять (?).
- КОЛИ `tick` → ЯКЩО `timer(<=, 0)` → ТО `custom: «вода рушає від стартового блока»`.
- КОЛИ `tick` → ЯКЩО `custom: «наступна труба зʼєднана з фронтом води»` → ТО `custom: «вода просувається на одну трубу»`.
- КОЛИ `tick` → ЯКЩО `custom: «наступна труба не зʼєднана»` → ТО `lose` (?) — вода виливається.
- КОЛИ `reach(water, end_block)` → ЯКЩО `path_exists(start, end) and custom: «шлях пройшов через нагрівач»` → ТО `custom: «поверх виконано»`.
- КОЛИ `all_constraints_met` (усі поверхи) → ТО `win`, `score(pipes_used)`.
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «задіяно найбільше труб»` → ТО `custom: «gold»`; челендж — найменше труб.
- Перемога: на всіх поверхах вода через нагрівач дійшла до кінця. · Поразка: вода випередила (?). · Рахунок: кількість задіяних труб, gold.

## Керування і ввід
- Миша: клік по трубі — поворот (?); перемикання поверхів — кнопка або клавіша (?).
- Деталі керування в описі Steam не наведено.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Levels / Unlimited.
- `level-select` (Levels) з найкращим результатом / gold (?).
- `game-screen`: поточний поверх, перемикач поверхів, `timer-countdown` до старту води (?).
- `end-screen`: кількість задіяних труб, gold (?).

## Фічі поза полем
- `levels-sequential` ручних рівнів з повторним проходженням заради кращої оцінки.
- `mode-endless`-подібний Unlimited: кожен рівень процедурний, новий.
- `stars-rating`-подібний gold-статус; `achievements` у Steam.

## Варіації й родичі
- [Pipe Mania](pipe-mania.md) — вода тече, поки кладеш труби з черги; [Plumber / Pipes](plumber-pipe-rotation.md) — поворот без таймера; [Infinity Loop](infinity-loop.md) — замкнути все.
- Обовʼязкова проміжна точка — як `must-visit-checkpoints` (Icebarn) у пазлах на шлях.
- Осі варіацій: **ввід** — поворот (Piping Hot) / кладення з черги (Pipe Mania) · **час** — статичний / вода після таймера · **оцінка** — лише звʼязок / довжина шляху (max або min) · **поля** — одне / кілька паралельних поверхів.

## Цікавинки для курсу
- Поворот плитки з портами і BFS від джерела: «чи звʼязано start → нагрівач → end» — 🌱.
- Довжина шляху як оцінка (max і min труб) — 📎 (найдовший простий шлях — NP-складна задача; для розвʼязувача — 🥇).
- Кілька паралельних полів з перемиканням і спільним годинником — 📎.
- Фронт води, що просувається по зʼєднаних трубах після таймера — 📎.
- Процедурна генерація рівня з гарантованим шляхом через нагрівач і перемішаними поворотами — 🥉.

## Мапа на каталог
- Є: `tile-rotate` + `pipe-connectors` ↔ труби; `cell-click` ↔ поворот; `connectivity-check` + `reachability-check` ↔ шлях start → end; `completion-detection`; `time-out` ↔ таймер до води; `sequential-levels` + `level-select` + `mode-select` ↔ Levels / Unlimited; `game-screen`.
- **Нема** → пропозиції карток:
  - `+flow-propagation` (Pipe Mania) — фронт води.
  - `+must-visit-checkpoints` (Icebarn) — шлях через нагрівач.
  - `+multi-board-field` (Shōbu) — кілька полів одночасно.
  - `+path-length-rating` «Оцінка за довжиною шляху (max / min)» · game-logic/score · 📎.
  - `+procedural-levels` «Нескінченні процедурні рівні з гарантією розвʼязку» · levels/generation · 🥉.

## Пропозиції до словників
- `+cond:path_through(a, via, b)` — існує шлях від A до B через обовʼязкову точку (розширення `path_exists`).
- `+ui:board-tabs` — перемикач між кількома паралельними полями.
- `+card:path-length-rating`, `+card:procedural-levels` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Piping Hot](https://store.steampowered.com/app/1168160/Piping_Hot/) — «Rotate the pipes to connect the starting block with the ending block», «include the heating pipe in the middle», кілька поверхів одночасно, «before the water catches up», gold за найбільше труб, челендж найменше, Levels / Unlimited; через appdetails — Odd Digs, 30.10.2019, Windows.
- YouTube: пошук «Piping Hot Odd Digs».

## Непевне
- (?) Єдине джерело — опис у Steam; оглядів і відгуків нема (0 відгуків), відео не переглянуто. Тому коротко.
- (?) Типи відрізків труб, чи можна замінювати труби, чи поверхи зʼєднані між собою (рядок черги каже «труби на кількох поверхах»).
- (?) Чи таймер спільний для всіх поверхів; що саме є поразкою — вода вилилась чи лише гірша оцінка.
- (?) Керування, HUD, кількість рівнів.
