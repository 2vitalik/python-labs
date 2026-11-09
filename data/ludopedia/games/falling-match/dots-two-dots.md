---
title: Dots / Two Dots
slug: dots-two-dots
aka: [Dots, "Dots: A Game About Connecting", Two Dots, «Дві точки»]
family: falling-match
also: [connect-rotate]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 2013
platforms: [iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dots_(video_game)", best: true, note: "Dots: лінія через однакові точки, замкнена лінія знімає весь колір; Playdots, 2013, закрито 2023"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Two_Dots_(game)", note: "Two Dots: ≥2 точки по ортогоналі, контур ≥4 знімає колір і робить бомби всередині, 13+ точок, автоперемішування, цілі (якорі, лід), ліміт ходів, 5 життів по 20 хв, бустери"}
  - {kind: other, url: "https://www.imore.com/dots-update-adds-endless-mode-one-app-purchase", note: "Endless-режим Dots як разова покупка"}
  - {kind: other, url: "https://www.iclarified.com/34654/dots-is-updated-with-an-endless-play-mode", note: "новина про Endless-режим"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Two+Dots+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [path-drawing, path-cut, swipe-gestures, gravity-fall, spawn-random-cell, single-loop-check, explode-area, chain-reaction, event-points, move-limit, time-out, collect-quota, goal-counter, move-counter, objective-text, sequential-levels, level-unlock, world-map, mode-select, end-screen, score-records, shop-window, +loop-clears-color, +auto-shuffle, +lives-regen-timer, +booster-items]
proposes: ["+effect:shuffle", "+effect:clear_color", "+ui:path-color-flash", "+feature:lives-regen", "+card:loop-clears-color", "+card:auto-shuffle", "+card:lives-regen-timer", "+card:booster-items"]
author: opus
date: 2026-11-09
---

# Dots / Two Dots — проведи лінію через сусідні точки одного кольору; замкнений контур знімає весь колір

## Суть
Поле — сітка кольорових точок. Гравець пальцем веде лінію через сусідні (по горизонталі/вертикалі) точки одного кольору; відпустив — точки зникають, верхні падають, згори досипаються нові. Ядро — **замкнений контур**: якщо лінія повернулась у свою точку (квадрат 2×2 чи більший контур), зникають усі точки цього кольору на полі. Dots (2013) — на очки за час чи ходи; Two Dots (2014) — saga-рівні з цілями (зібрати N точок кольору, потопити якорі, розбити лід) за ліміт ходів.

## Поле і час
- Квадратна сітка точок (розмір у Dots сталий, у Two Dots — форма рівня; числа — у «Непевне»).
- Суміжність лише ортогональна; діагоналі заборонені.
- Хід = одна лінія. Після ходу — падіння й досипання, без каскадів-збігів (нова лінія — лише рукою гравця).
- Dots: режими «на час» і «на ходи», пізніше Endless; Two Dots — дискретні рівні з лімітом ходів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Точка | tile | колір (4–5, ?) | зʼєднується з сусідніми того ж кольору; зникає, падає вниз |
| Лінія гравця | mark | колір, список точок | росте під пальцем; повернення назад стирає хвіст; самоперетин у точці = контур |
| Контур (квадрат) | mark | ≥4 точки, замкнений | знімає всі точки свого кольору |
| Бомба (Two Dots) | object | — | зʼявляється в клітинах усередині контуру; вибух у 8 напрямках |
| Якір (Two Dots) | object | — | не зʼєднується; падає разом з точками; ціль — довести до нижнього краю, там зникає |
| Лід (Two Dots) | terrain | — | шар під точкою; розбивається, коли точку над ним знято |
| Інші перешкоди Two Dots (вогонь, стіни, павуки…) | hazard | залежить від світу | у кожному світі нові; переліку джерела не дають (?) |
| Бустери | pickup | тип | Dots: зупинка часу / +ходи, «зменшувач» однієї точки, зняти колір; Two Dots: shuffler, eraser, target, color booster |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, dot)` → ЯКЩО `same(dot, path.last, color)` and `custom: «точки сусідні ортогонально»` → ТО `custom: «додати точку до лінії»`; інакше `block`.
- КОЛИ `input(drag, back)` → ТО `custom: «відкотити лінію на одну точку»` (path-cut).
- КОЛИ `input(release)` → ЯКЩО `count(path, >=, 2)` → ТО `clear(path)`, `score(len(path))`, `counter(moves, -1)`; інакше нічого.
- КОЛИ `pattern(loop_closed)` → ТО `custom: «зникають усі точки кольору лінії»`.
- КОЛИ `pattern(loop_closed)` (Two Dots) → ЯКЩО `custom: «клітина всередині контуру»` → ТО `spawn_at(bomb, inner_cells)`.
- КОЛИ `custom: «лінія з 13+ точок»` (Two Dots) → ТО `custom: «зникають усі точки кольору лінії»` без контуру.
- КОЛИ `spawned(bomb)` → ТО `explode(area: 8_directions)` (?) — знімає сусідні точки.
- КОЛИ `after(clear)` → ТО `fall(dots)`, `spawn_at(dot, top_edge)` випадкового кольору.
- КОЛИ `settled` → ЯКЩО `not path_exists(same_color_pair)` → ТО `custom: «перемішати точки поля»`.
- КОЛИ `after(clear)` → ЯКЩО `cell(cleared, ice)` → ТО `set_cell(ice, floor)`.
- КОЛИ `reach(anchor, bottom_edge)` → ТО `disappear_a`, `counter(anchors, -1)`.
- КОЛИ `counter(goal_*, ==, 0)` (усі цілі рівня) → ТО `win`, `unlock(next_level)`.
- КОЛИ `counter(moves, ==, 0)` → ЯКЩО `not custom: «цілі виконано»` → ТО `lose`, `lives(-1)`.
- КОЛИ `timer(60s)` (Dots, режим на час) → ТО `game_over`, `window(end-screen)` з рахунком.
- КОЛИ `input(use, booster)` → ТО `custom: «ефект бустера»`: прибрати точку / колір / перемішати / зупинити час.
- Перемога: Dots — рекорд очок; Two Dots — усі цілі до кінця ходів · Поразка: ходи (або час) скінчились · Рахунок: точки = очки й валюта бустерів (Dots).

## Керування і ввід
- Тач-drag від точки через сусідні однакові; повернення назад знімає останню точку; відпускання — хід.
- Замикання контуру — повернутись у вже взяту точку лінії; гра підсвічує (?) і знімає колір.
- Бустер — тап по кнопці, потім тап по точці (?).

## Вікна, меню, HUD
- `main-menu` (Dots): режими «Timed», «Moves», «Endless» → `game-screen`; бустери; рекорди.
- `world-map` (Two Dots): світи з рівнями (перший — 10, далі 25+), листівка за пройдений світ.
- `game-screen`: поле, `move-counter` або `timer-countdown`, `objective-text` / `goal-counter` (скільки точок кольору / якорів / льоду лишилось), `score`.
- `custom-window` «цілі рівня» на старті (Two Dots).
- `end-screen`: рахунок / «рівень пройдено» / «ходи скінчились» → повтор (−життя) або `shop-window` (бустери).
- HUD: `lives` (Two Dots, 5).
- Переходи: world-map → вікно цілей → game-screen → end-screen → world-map.

## Фічі поза полем
- `levels-sequential`, `level-unlock`, `world-map` (Two Dots): нові світи з новими перешкодами приблизно раз на два тижні.
- `lives-regen` (+ `feature:lives-regen`): 5 життів, +1 за 20 хв.
- Бустери за рекламу або покупку (Two Dots); за зароблені точки (Dots).
- `mode-time-attack` / `mode-classic` (на ходи) / `mode-endless` (Dots); тижневий «Treasure Hunt» (Two Dots, закритий).
- Dots мав онлайн-мультиплеєр (?) — джерела розходяться.

## Варіації й родичі
- Родичі в корпусі: Candy Crush (saga-структура, цілі, ліміт ходів — обмін, а не лінія), Bejeweled, Puzzle & Dragons (лінія через поле), Flow Free і LYNE (лінія через вузли одного кольору, але статично), SameGame/Flood (зняти групу).
- **Осі варіацій:** форма ходу — обмін двох / лінія-шлях / тап по групі · винагорода за форму — довжина / замкнений контур / 13+ · після ходу — каскад збігів / лише падіння · ціль — очки / квоти кольорів / предмети до дна (якорі).

## Цікавинки для курсу
- Валідація лінії: сусідство + колір + відкат хвоста при поверненні — 🌱.
- Виявлення замкненого контуру в лінії (повторна точка, довжина ≥4) — 📎.
- Клітини «всередині контуру» (point-in-polygon на сітці / flood fill ззовні) → бомби — 🥉.
- Перевірка «є хоча б одна пара сусідів одного кольору» + перемішування, що гарантує хід — 📎.
- Гравітація з досипанням і якір, що «тоне» до дна — 📎.
- Saga-мета: мапа світів, життя з таймером відновлення — 🥉.

## Мапа на каталог
- Є: `path-drawing` ↔ лінія через точки · `path-cut` ↔ повернення назад · `swipe-gestures` · `gravity-fall` · `spawn-random-cell` (досипання згори) · `single-loop-check` ↔ замкнений контур · `explode-area` ↔ бомба · `chain-reaction` ↔ бомба знімає сусідів · `event-points` · `move-limit` · `time-out` · `collect-quota` · `goal-counter` · `move-counter` · `objective-text` · `sequential-levels` · `level-unlock` · `world-map` · `mode-select` · `end-screen` · `score-records` · `shop-window`.
- **Нема** → пропозиції карток:
  - `+loop-clears-color` «Замкнений контур знімає весь колір» · entities/interact · 📎.
  - `+auto-shuffle` «Перемішування, коли нема ходів» · game-logic · 📎 — родич `no-moves-left`, але без програшу.
  - `+lives-regen-timer` «Життя відновлюються за реальним часом» · game-logic/economy · 🥉.
  - `+booster-items` «Бустери поза полем (прибрати точку/колір/перемішати)» · game-logic/economy · 📎.

## Пропозиції до словників
- `+effect:shuffle` — переставити плитки поля випадково, зберігаючи кількості (автоперемішування Two Dots).
- `+effect:clear_color` — зняти всі плитки кольору з поля (контур, 13+ точок, color booster).
- `+ui:path-color-flash` — підсвітка всього поля кольором лінії при замиканні контуру (?).
- `+feature:lives-regen` — життя відновлюються за реальним часом (5 по 20 хв).
- `+card:loop-clears-color`, `+card:auto-shuffle`, `+card:lives-regen-timer`, `+card:booster-items` — див. «Мапа на каталог».

## Джерела
- ⭐ [Dots (video game) — Wikipedia](https://en.wikipedia.org/wiki/Dots_(video_game)) — ядро: лінія, замкнений контур знімає колір; дати, Playdots, закриття 2023.
- [Two Dots (game) — Wikipedia](https://en.wikipedia.org/wiki/Two_Dots_(game)) — ≥2 точки ортогонально, контур ≥4 → колір + бомби в 8 напрямках, 13+ точок, автоперемішування, цілі (якорі, лід), ліміт ходів, світи 10 / 25+, 5 життів по 20 хв, бустери.
- [iMore](https://www.imore.com/dots-update-adds-endless-mode-one-app-purchase), [iClarified](https://www.iclarified.com/34654/dots-is-updated-with-an-endless-play-mode) — Endless-режим Dots.
- WebSearch-описи: Timed — 60 секунд, Moves — 30 ходів; бустери Time Stop (+5 с / +5 ходів), Shrinker (одна точка), зняття кольору; точки = валюта.

## Непевне
- (?) Розмір поля Dots (6×6?) і кількість кольорів — з памʼяті, не звірено.
- (?) 60 с / 30 ходів / бустери Dots — з результатів пошуку, сторінок не відкривав (TouchArcade 403); склад бустерів мінявся між версіями.
- (?) Як саме бомба детонує (одразу після контуру чи наступним ходом) і що знімає «8 напрямків» — Wikipedia коротко.
- (?) Решта перешкод Two Dots (вогонь, стіни, павуки, магніти тощо) — з памʼяті; fandom віддає 402.
- (?) Онлайн-мультиплеєр Dots: текст Wikipedia каже «є», інфобокс — лише single-player.
- Тека: `falling-match` (родина Candy Crush / Bejeweled, гравітація й досипання), а не призначена `connect-rotate` — там лише в `also`.
