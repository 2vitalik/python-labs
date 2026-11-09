---
title: Stickets
slug: stickets
aka: []
family: falling-match
also: [board-digital]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: survive
year: 2013
platforms: [iOS]
links:
  - {kind: other, url: "https://www.148apps.com/reviews/stickets-review/", best: true, note: "огляд 148Apps: 4 L-фігури внизу, drag на поле, тап по групі ≥3 знімає її, режими Space/Time/Puzzle і їх відкриття"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Stickets", note: "поле 5×5, L-трійки з жовтим/синім/червоним, 4 орієнтації, кінець — нема місця"}
  - {kind: other, url: "https://www.pocketgamer.com/stickets/review/", note: "огляд Pocket Gamer: +1 очко за фігуру, без бонусів і гімміків"}
  - {kind: official, url: "https://sticketsgame.com/", note: "сайт: 3 режими, теми primary/classic/icecream"}
  - {kind: other, url: "https://toucharcade.com/2013/06/12/stickets-review-an-elegant-enchanting-puzzler/", note: "огляд TouchArcade (у фетчі 403)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=stickets+ios+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [polyomino-placement, drag-drop-piece, cell-click, next-queue, event-points, score-records, theme-select, mode-select, level-unlock, +connected-group-pop, +manual-group-clear, +fixed-shape-slots, +block-time-bomb, +no-space-left-lose]
proposes: ["+card:manual-group-clear", "+card:fixed-shape-slots", "+card:block-time-bomb", "+card:no-space-left-lose", "+ui:piece-tray"]
author: opus
date: 2026-11-09
---

# Stickets — L-трійки трьох кольорів на полі 5×5; групу з 3+ однакових знімаєш тапом, коли сам вирішиш

## Суть
Мінімалістичний «пакувальний» match-пазл: внизу екрана лежать чотири L-подібні трійки (по одному жовтому, синьому й червоному блоку в кожній), чотири орієнтації одного кута. Гравець перетягує будь-яку з них на поле 5×5; використана фігура замінюється новою **тієї ж форми**, але з іншим порядком кольорів. Коли три або більше блоків одного кольору стикаються, групу можна **тапнути** — вона зникає й звільняє місце. Гравітації нема; кожна поставлена фігура дає +1 очко, кінець — коли жодну фігуру нікуди поставити.

## Поле і час
- Поле 5×5 квадратних клітин, без гравітації: блоки лишаються там, де поставлені.
- Покроково: хід = поставити одну фігуру; знімати групи можна між ходами скільки завгодно разів (?).
- Режим Time: кожен блок — бомба з таймером, тобто зʼявляється реальний час.
- Випадковість — лише в розстановці кольорів у новій фігурі; форма слота фіксована.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| L-трійка | piece | форма-кут (1 з 4 орієнтацій), 3 блоки: жовтий, синій, червоний | лежить у слоті; ставиться drag-ом на 3 вільні клітини |
| Слот фігури | spawner | орієнтація фіксована | після використання видає нову фігуру тієї ж орієнтації з новими кольорами |
| Блок | tile | колір: жовтий / синій / червоний | займає клітину; у звʼязній групі ≥3 одного кольору — знімний |
| Група ≥3 | zone | колір, розмір | тап — зникає вся |
| Блок-бомба (Time) | hazard | таймер (?) | вибухає, якщо довго лежить; вибух — мінус життя |
| Порожня клітина | static | — | місце для фігури |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag piece → cell)` → ЯКЩО `fits(piece, cells)` → ТО `place(player, piece)`, `score(+1)`; інакше фігура повертається в слот.
- КОЛИ `after(place)` → ТО `spawn_at(piece_same_shape, slot)` з `custom: «випадковий порядок трьох кольорів»`.
- КОЛИ `input(tap block)` → ЯКЩО `connected(same_color_group)` `and` `count(group, >=, 3)` → ТО `clear(group)`.
- Групу не знімає автоматично: гравець може ростити її далі, щоб звільнити більше місця.
- КОЛИ `custom: «жодна з 4 фігур не вміщується на поле»` → ТО `game_over`.
- Time: КОЛИ `timer(bomb)` → ТО `custom: «блок вибухає»`, `lives(-1)`.
- Time: КОЛИ `clear(group)` → ЯКЩО `custom: «група велика»` → ТО `lives(+1)`.
- Time: КОЛИ `counter(lives, ==, 0)` → ТО `lose`.
- КОЛИ `counter(score, >=, 50)` у Space → ТО `unlock(Time)`; 50 у Time → `unlock(Puzzle)`.
- Перемога: нема (рахунок). Поразка: немає місця (Space) / життя скінчились (Time). Рахунок: +1 за кожну поставлену фігуру.

## Керування і ввід
- Тач: перетягнути фігуру зі слота на поле (`drag-drop-piece`); тап по групі — зняти.
- Поворотів нема: орієнтацію обираєш, беручи фігуру з потрібного слота (чотири слоти = чотири орієнтації).

## Вікна, меню, HUD
- `game-screen`: поле 5×5, лоток із 4 фігурами (`+ui:piece-tray`), `score`; у Time — `lives`.
- `main-menu` / `mode-select`: Space · Time (замок до 50 у Space) · Puzzle (замок до 50 у Time).
- `settings-window` або вибір теми — `theme-select`: primary / classic / icecream.
- `end-screen` — рахунок і рекорд (?).

## Фічі поза полем
- `level-unlock` режимів за порогом очок; `unlockables` — альтернативні теми блоків.
- `mode-classic` (Space), `mode-time-attack`-подібний Time, `mode-puzzle` (правила не описані).
- `leaderboard-local` / `leaderboard-online` (Game Center) — (?).
- Інтерактивний звук, що підлаштовується під тему.

## Варіації й родичі
- Родичі в корпусі: [block-blast](block-blast.md) (поліоміно з лотка на поле, без гравітації — але ряди зникають самі); [lines-98](lines-98.md) (групи кольору на статичному полі); [samegame-flood](samegame-flood.md) (тап по групі знімає її); [triple-town](triple-town.md) (3+ поруч).
- Особливість — **ручне зняття** групи: гравець вирішує, коли «збирати врожай», що дає ризик-ставку на більшу групу.
- **Осі варіацій**: зняття групи (автоматичне / тапом) · форма фігур (фіксовані слоти / випадкові) · поворот (нема / є) · гравітація (нема / вниз) · тиск часу (нема / бомби на блоках).

## Цікавинки для курсу
- Перевірка «вміщується хоч одна фігура хоч десь» для кінця гри — 🌱.
- Flood fill групи одного кольору + умова ≥3 + зняття тапом — 🌱.
- Слоти фіксованої форми з випадковими кольорами — 🌱.
- Drag-n-drop фігури з підсвіткою, куди ляже — 📎.
- Time: таймер на кожному блоці і життя за великі групи — 📎.
- Бот, що обирає фігуру й місце, максимізуючи кількість можливих наступних постановок — 🥉.

## Мапа на каталог
- Є: `polyomino-placement` (трійка на сітку) · `drag-drop-piece` · `cell-click` (тап по групі) · `next-queue` (лоток) · `event-points` · `score-records` · `theme-select` · `mode-select` · `level-unlock` (режими).
- **Нема** → пропозиції карток:
  - `+connected-group-pop` — підтверджую (група ≥N одного кольору).
  - `+manual-group-clear` «Група зникає за тапом, а не сама» · entities/interact · 🌱.
  - `+fixed-shape-slots` «Слоти фігур фіксованої форми, кольори випадкові» · entities/spawn · 🌱.
  - `+block-time-bomb` «Кожен блок має таймер-вибух» · entities/state · 📎.
  - `+no-space-left-lose` «Поразка: жодна фігура не вміщується» · game-logic/lose · 🌱 — Block Blast, Stickets, 1010!.

## Пропозиції до словників
- `+card:manual-group-clear` — гравець сам знімає готову групу (Stickets).
- `+card:fixed-shape-slots` — слот відновлює фігуру тієї ж форми (Stickets).
- `+card:block-time-bomb` — таймер на кожному блоці поля (Stickets Time).
- `+card:no-space-left-lose` — поразка, коли жодна фігура з лотка не вміщується.
- `+ui:piece-tray` — лоток доступних фігур під полем (Stickets, Block Blast).

## Джерела
- ⭐ [148Apps: Stickets review](https://www.148apps.com/reviews/stickets-review/) — лоток із 4 L-фігур, заміна тієї ж форми, тап по групі, режими й відкриття за 50 очок, бомби Time.
- [Wikipedia: Stickets](https://en.wikipedia.org/wiki/Stickets) — 5×5, жовтий/синій/червоний, 4 орієнтації, кінець — нема місця; Wanderlands, 30.05.2013.
- [Pocket Gamer: review](https://www.pocketgamer.com/stickets/review/) — +1 очко за фігуру, без павер-апів, складність стала.
- [sticketsgame.com](https://sticketsgame.com/) — 3 режими, теми primary/classic/icecream.
- [TouchArcade review](https://toucharcade.com/2013/06/12/stickets-review-an-elegant-enchanting-puzzler/) — не прочитано (403).

## Непевне
- (?) Чи групи сусідять лише по 4 сторонах — джерела не уточнюють.
- (?) Правила режиму Puzzle; таймінг бомб і скільки життів у Time; що вважається «великою» групою.
- (?) Чи можна знімати кілька груп за один хід і чи зняття рахується в очки (джерела: очки лише за фігури).
- (?) Онлайн-рекорди (Game Center).
