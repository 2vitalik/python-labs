---
title: Make Trax (Crush Roller)
slug: make-trax
aka: [Crush Roller, クラッシュローラー, Brush Roller, Paint Roller]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: territory
year: 1981
platforms: [arcade (Alpha Denshi / Kural Samno, Williams у США), Neo Geo Pocket Color (1999), PC (NGPC Selection Vol. 1, 2021)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Make_Trax", best: true, note: "пензель фарбує лабіринт, дві рибки, валики на естакадах, нарушник із слідами, версії"}
  - {kind: other, url: "https://ja.wikipedia.org/wiki/クラッシュローラー", note: "JA Wikipedia: порядок нарушників, очки валика 50 → 9000, сиквел Korosuke Roller, Gakken Paint Roller"}
  - {kind: other, url: "https://www.arcade-museum.com/Videogame/make-trax", note: "KLOV: 6 виходів-тунелів, рибки з акваріума, список нарушників, 1000 за невидимця, пензель за 10 000"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=crush+roller+make+trax+arcade+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 70
mechanics: [move-4dir, visited-trail, collect-all, touch-death, player-death, chase-player, crush-by-slide, push-object, wrap-edges, spawner-entity, respawn, escalating-kill-points, extra-life-threshold, event-points, sequential-levels, progress-acceleration, status-panel, game-screen, +paint-all-cells, +overpass-cells, +trail-dirtying-intruder, +pincer-chasers, +learning-chasers]
proposes: ["+effect:unpaint", "+cond:all_painted", "+role:intruder", "+card:paint-all-cells", "+card:overpass-cells", "+card:trail-dirtying-intruder", "+card:pincer-chasers"]
author: opus
date: 2026-11-09
---

# Make Trax (Crush Roller) — пензель фарбує весь лабіринт, рибки ловлять, валиком їх можна розчавити

## Суть
Гравець веде пензель коридорами лабіринту, і кожна пройдена клітина фарбується; стадія пройдена, коли пофарбовано весь лабіринт. Дві рибки випливають з акваріумів і полюють на пензель, з часом навчаючись затискати його з двох боків. На естакадах стоять два валики: підштовхни валик на рибку — вона розчавлена й на кілька секунд зникає. Нарушник (кіт, миша, шина, невидимець…) топчеться по свіжій фарбі, лишаючи сліди, які треба перефарбувати.

## Поле і час
- Поле — лабіринт коридорів на клітинній сітці (типу Pac-Man) з двома естакадами-мостами: коридор проходить над іншим, валик котиться по естакаді.
- Шість виходів на краях — тунелі на протилежний бік (рибки теж ними ходять).
- Real-time; рибки «розумнішають» зі стадіями.
- Шари: коридор (непофарбований / пофарбований / зі слідами) → валики → персонажі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пензель | player | 3 життя | рух 4 напрямки; клітина під ним фарбується |
| Рибка (жовта, блакитна) | enemy | 2 шт. | переслідує пензель; згодом уникає валиків і затискає з двох боків |
| Акваріум | spawner | 2 шт. | звідси виходять і сюди повертаються рибки |
| Валик | object | 2 шт. (вертикальний, горизонтальний) | на естакаді; пензель штовхає його вздовж мосту, валик чавить рибку |
| Естакада | terrain | 2 шт. | коридор над коридором; доріжка валика |
| Нарушник | enemy (`+role:intruder`) | кіт → миша → птах → шина → бакенеко → невидимець | бігає лабіринтом, лишає сліди на фарбі; лише заважає (?) |
| Слід | terrain | — | пофарбована клітина знову брудна; треба перефарбувати |
| Тунель-вихід | static | 6 шт. | перехід на протилежний край |
| Клітина коридору | terrain | стан: чиста / фарба | ціль: усі в стані «фарба» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(brush, dir)`.
- КОЛИ `enter(brush, corridor)` → ТО `paint(cell, green)`.
- КОЛИ `edge(brush)` → ТО `wrap(brush)`; так само для рибок.
- КОЛИ `contact(fish, brush)` → ТО `lives(-1)`, `respawn(brush, start)`.
- КОЛИ `contact(brush, roller)` → ЯКЩО `custom: «пензель біля торця валика й рухається вздовж естакади»` → ТО `push(roller)`.
- КОЛИ `contact(roller, fish)` → ТО `disappear_b`, `score(crush_value)`, `custom: «наступне чавлення дорожче, від 50 до 9000»`.
- КОЛИ `destroyed(fish)` → ТО `custom: «за кілька секунд рибка виходить з акваріума»` (`respawn(fish, aquarium)`).
- КОЛИ `timer(intruder)` → ТО `spawn_at(intruder, edge)`.
- КОЛИ `contact(intruder, painted_cell)` → ТО `custom: «клітина стає брудною — слід»` (`+effect:unpaint`).
- КОЛИ `contact(brush, intruder)` → ТО `disappear_b`, `score(intruder_value)` (невидимець — 1000); сліди більше не з'являються.
- КОЛИ `timer(intruder_life)` → ЯКЩО `not custom: «нарушника спіймано»` → ТО `custom: «нарушник повертається на місце виходу»`; так само, якщо в цей час спіймано пензель.
- КОЛИ `enter(brush, track)` → ТО `paint(cell, green)`.
- КОЛИ `custom: «усі клітини лабіринту пофарбовані»` (`+cond:all_painted`) → ТО `next_level`.
- КОЛИ `counter(score, >=, 10000)` → ТО `lives(+1)`.
- КОЛИ `level_start` → ТО `custom: «рибки розумнішають; наступний нарушник у черзі»`.
- Перемога: пофарбувати весь лабіринт · Поразка: рибка спіймала останній пензель · Рахунок: чавлення валиком (зростає), спіймані нарушники, бали за фарбування (?).

## Керування і ввід
- Лише 4-напрямний джойстик, кнопок нема.
- Валик «керується» тим, що пензель упирається в його торець і рухається вздовж естакади.
- 1–2 гравці по черзі.

## Вікна, меню, HUD
- `attract-demo` — режим очікування (?).
- `game-screen`: лабіринт, акваріуми, валики; `score`, `hi-score`, `lives` (запасні пензлі) (?).
- `end-screen` — GAME OVER (?).
- Звук: вступ — народна мелодія «Neko Funjatta» (Собачий вальс).

## Фічі поза полем
- `levels-sequential` з циклом нарушників і розумнішими рибками.
- Додатковий пензель за 10 000 очок.
- Make Trax Turbo — хак, де пензель швидший, а рибки ні.

## Варіації й родичі
- Korosuke Roller (сиквел): гравець-кальмар; кнопка аварійного варпу вперед/назад уздовж коридору; два горизонтальні й один вертикальний варп-тунелі.
- Paint Roller (Gakken, 1982) — електронна гра на два важелі з режимом versus: пензель проти монстра.
- Brush Roller (NES, 1990, неліцензійний) і хак Bookyman.
- Родичі: `amidar` (фарбування ребер гратки), `qbert` (фарбування клітин), `pac-man` (лабіринт + переслідувачі, тунелі), Pengo (розчавити ковзним блоком).
- **Осі варіацій:** що фарбується: клітини коридору / ребра / кубики · хто псує фарбу: нікого / нарушник-слід · зброя: нема / валик на естакаді / варп · вороги: прямолінійні / що вчаться затискати.

## Цікавинки для курсу
- Фарбування пройдених клітин і перевірка «усе пофарбовано» — 🌱.
- Нарушник, що знову бруднить фарбу: ціль-територія, яка може відкотитися — 📎.
- Естакада: клітина з двома рівнями (міст над коридором), де валик і пензель розходяться з рибками — 🥉.
- Пара переслідувачів, що координуються «кліщами» з двох кінців коридору — 🥉.
- Ескалація очок за чавлення (50 → … → 9000) — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `visited-trail` (пофарбовані клітини) · `collect-all` (усі клітини) · `touch-death` · `player-death` · `chase-player` · `crush-by-slide` (валик) · `push-object` · `wrap-edges` (6 тунелів) · `spawner-entity` (акваріум) · `respawn` · `escalating-kill-points` · `extra-life-threshold` · `event-points` · `sequential-levels` · `progress-acceleration`.
- **Нема** → пропозиції карток:
  - `+paint-all-cells` «Пофарбуй увесь лабіринт» · game-logic/win · 🌱.
  - `+overpass-cells` «Естакада: міст над коридором» · board/field · 🥉 — дві доріжки в одній клітині.
  - `+trail-dirtying-intruder` «Нарушник бруднить зроблене» · entities/ai · 📎.
  - `+pincer-chasers` «Переслідувачі-кліщі» · entities/ai · 🥉 — двоє заходять з протилежних кінців.
  - `+learning-chasers` «Вороги розумнішають з рівнем» · game-logic/waves · 📎.

## Пропозиції до словників
- `+effect:unpaint` — повернути клітину у стан «не пофарбовано / брудна».
- `+cond:all_painted` — усі клітини виду пофарбовані (Make Trax, Q*bert, Amidar).
- `+role:intruder` — нешкідлива сутність, що псує прогрес гравця.
- `+card:paint-all-cells`, `+card:overpass-cells`, `+card:trail-dirtying-intruder`, `+card:pincer-chasers` — див. «Мапу на каталог».

## Джерела
- ⭐ [Wikipedia: Make Trax](https://en.wikipedia.org/wiki/Make_Trax) — пензель, дві рибки з акваріумів, валики на естакадах, нарушник і сліди, версії й клони.
- [Wikipedia JA: クラッシュローラー](https://ja.wikipedia.org/wiki/クラッシュローラー) — порядок нарушників, повернення нарушника за таймером, очки валика 50 → 9000, Korosuke Roller, Gakken Paint Roller.
- [KLOV: Make Trax](https://www.arcade-museum.com/Videogame/make-trax) — 6 виходів, тактика рибок, список нарушників, 1000 за невидимця, пензель за 10 000.
- YouTube: пошук «crush roller make trax arcade gameplay».

## Непевне
- (?) Чи нарушник шкодить пензлю при дотику (джерела кажуть лише «спіймати»).
- (?) Чи дають очки за саме фарбування клітин.
- (?) Як саме зростають очки за чавлення: «подвоєння» (KLOV) від 50 до 9000 (JA).
- (?) Списки нарушників розходяться (KLOV: кошеня, миша, птах, шина, танцюючий кіт, невидимець; JA: кіт, миша, птах, шина, бакенеко, невидимець).
- (?) Додатковий пензель: один за 10 000 чи до трьох.
- (?) Розміщення HUD і attract-режим — джерел нема.
