---
title: Hexic (Hexic HD, Hexic 2)
slug: hexic
aka: [Hexic HD, Hexic 2, Hexic Deluxe, Гексік]
family: falling-match
also: [connect-rotate]
klass: cursor
axes:
  field: hex
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2003
platforms: [web, PC, Xbox 360, Zune, Windows Mobile, Windows Phone]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hexic", best: true, note: "правила: кластер 3, квітки, срібні зірки, чорна перлина, бомби, режими Marathon/Timed/Survival"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hexic_2", note: "Hexic 2 (2007): смарагд, рубін, метри кольорів, атаки, режим Battle"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hexic+hd+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [keyboard-controls, gravity-fall, spawn-random-cell, chain-reaction, event-points, time-out, time-bonus, score-records, leaderboard, mode-select, game-pause, end-screen, particles, background-music, gui-render, selection-highlight, +rotate-triple-hex, +hex-cluster-match, +cascade-refill, +special-tiles, +countdown-tile, +ring-match, +lock-on-no-moves, +color-meter-attack]
proposes: ["+effect:rotate_group", "+trigger:pattern(ring6)", "+cond:mutually_adjacent", "+effect:lock_all", "+card:rotate-triple-hex", "+card:ring-match", "+ui:vertex-cursor"]
author: opus
date: 2026-11-09
---

# Hexic — крутиш трійку гексів навколо спільної вершини, щоб зібрати кластер одного кольору

## Суть
Поле шестикутних плиток різних кольорів; гравець ставить курсор у вершину, де сходяться три гекси, і обертає цю трійку за чи проти годинникової стрілки. Три однакові гекси, що всі торкаються одне одного (трикутник), утворюють кластер і зникають; зверху падають нові, можливі каскади. Кільце з шести однакових навколо центру («квітка») дає спецфігуру з новим способом обертання. Автор — Олексій Пажитнов (Tetris); родом із match-3, але хід — обертання, а не обмін, звідси `also: connect-rotate`.

## Поле і час
- Гексагональна сітка в рамці; хід = обертання трійки, анімація каскаду без вводу.
- Курсор живе не в клітині, а у **вершині** між трьома гексами.
- Marathon — покроково без часу; Timed — таймер поверх покрокового поля; Survival — нові плитки самі не падають.
- Шари: плитки (колір + спецвластивість) · накладки (бомба з лічильником, замок у Survival) · курсор.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гекс | tile | колір | бере участь у кластері; падає в порожнечу |
| Кластер | zone | ≥3 гекси одного кольору, взаємно суміжні | зникає; >3 одночасно — бонус |
| Бонусна зірка | tile | — | додаткові очки; залежно від способу зачистки чистить більшу групу |
| Квітка (starflower) / срібна зірка | tile | колір центру | 6 однакових навколо іншого кольору → кільце зникає, центр стає срібною зіркою; зірка обертає шістку довкола себе |
| Чорна перлина | tile | — | утворюється квіткою зі срібних зірок; дозволяє рухати трійку у формі Y / перевернутого Y |
| Бомба | hazard | лічильник ходів | лічильник −1 за хід; 0 → кінець гри; знешкоджується кластером свого кольору |
| Множник | tile | колір, число (?) | бомба, знешкоджена поруч із множником свого кольору, чистить увесь колір |
| Замкнена плитка (Survival) | gate | — | нема ходів → лишки замикаються; знімається зачисткою бонус-зірок поруч |
| Смарагд (Hexic 2) | tile | — | 5 суміжних у ряд; обертає гекси з двох боків |
| Рубін (Hexic 2) | tile | — | ряд із 5 квіток; маніпулює чотирма гексами двох суміжних сторін |
| Курсор | — (ui) | вершина | вибирає трійку для обертання |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(rotate_cw | rotate_ccw)` → ТО `rotate(trio, 120)` навколо вершини курсора (`+effect:rotate_group`).
- КОЛИ `after(rotate)` → ЯКЩО `custom: «три+ однакові гекси взаємно суміжні»` (`+cond:mutually_adjacent`) → ТО `clear(cluster)` + `score(n)`.
- КОЛИ `after(rotate)` → ЯКЩО `not custom: «утворився кластер»` → ТО `custom: «трійка крутиться далі, до повного оберту»` (?).
- КОЛИ `after(clear)` → ТО `fall(tiles_above)` + `spawn_at(tile, top)`; КОЛИ `settled` → ЯКЩО `pattern(group(3))` → ТО `clear` знову (каскад).
- КОЛИ `custom: «кільце з 6 однакових навколо центру іншого кольору»` (`+trigger:pattern(ring6)`) → ТО `clear(ring)` + `transform(center, silver_star)`; ЯКЩО `state(center, silver_star)` → ТО `custom: «нова срібна зірка падає згори»`.
- КОЛИ `input(rotate, silver_star)` → ТО `rotate(ring6, 60)` навколо зірки.
- КОЛИ `pattern(ring6 of silver_star)` → ТО `transform(center, black_pearl)`.
- КОЛИ `input(rotate, black_pearl)` → ТО `custom: «рух трьох гексів довкола перлини у формі Y»`.
- КОЛИ `turn_end` → ТО `counter(bomb, -1)`; КОЛИ `counter(bomb, =, 0)` → ТО `lose`.
- КОЛИ `custom: «бомба в кластері / квітці свого кольору»` → ТО `disappear_a`; ЯКЩО `custom: «поруч множник того ж кольору»` → ТО `clear(all of color)`.
- КОЛИ `pattern(cluster | flower of black_pearl)` → ТО `lose` (Marathon).
- Timed: КОЛИ `timer(every)` → ТО `timer(-1)`; кластер → `timer(+n)`; квітка → `custom: «таймер до максимуму, максимум росте до 2 хв»`; час вийшов → `lose`.
- Survival: КОЛИ `no_moves(player)` → ТО `custom: «лишки замикаються, порожні клітини доповнюються»` (`+effect:lock_all`); КОЛИ `custom: «усі плитки замкнені»` → ТО `lose`; поле очищено або 50 раундів → `win`.
- Квітка в Survival → `custom: «відмикає все й чистить колір центру»`.
- Hexic 2: КОЛИ `counter(color_meter, full)` → ТО `choose(attack)`: бомба супернику, зачистка свого поля, замок плиток суперника, зменшення його поля.
- Перемога: — (Marathon на рекорд) · Поразка: бомба, кластер чорних перлин, час, усе замкнене · Рахунок: кластери, бонуси за >3, зірки.

## Керування і ввід
- Геймпад/клавіші: курсор стрибає між вершинами; дві кнопки — поворот за / проти годинникової (?).
- Курсор на срібній зірці чи перлині перемикає обертання на кільце / Y-трійку (?).
- ПК-версія MSN — мишею: наведення на вершину, ліва/права кнопка — напрямок (?).

## Вікна, меню, HUD
- `game-screen`: гексове поле, курсор-трикутник, лічильники бомб на плитках, рахунок, таймер (Timed).
- `main-menu` → `mode-select` (Marathon / Timed / Survival; Hexic 2 — ще Battle) → `game-screen`.
- `pause-menu`, `end-screen` з рахунком, `leaderboard` (онлайн у Hexic HD).
- HUD: `score`, `hi-score`, `timer-countdown`, `combo-meter` (?); Hexic 2 — метри кольорів.

## Фічі поза полем
- `mode-classic` (Marathon), `mode-time-attack` (Timed), Survival як `mode-puzzle`-подібний режим.
- `leaderboard-online` (Hexic HD, Xbox Live); `achievements` (Xbox) (?).
- Hexic 2: `mode-versus` / `online-multiplayer` (Battle).
- Музика Hexic HD — альбом *Hexophilia*.

## Варіації й родичі
- Hexic (MSN, 2003) → Hexic HD (Xbox 360, 2005, передвстановлена) → Hexic 2 (XBLA, 2007) → Windows Store (2014).
- Родичі: [Bejeweled](bejeweled.md) (обмін; Twist — обертання 2×2), [Hextris](hextris.md) (гекс + падіння), [Puyo Puyo](puyo-puyo.md) (групи), обертові пазли [connect-rotate](../connect-rotate/).
- **Осі варіацій**: хід — обмін / обертання 2×2 / обертання трійки гексів / обертання кільця · форма збігу — лінія / трикутник / кільце · загроза — таймер / бомба-лічильник / замикання.

## Цікавинки для курсу
- Гекс-сітка з координатами і вершинами як окремими обʼєктами (курсор у вершині) — 🥉 — нетривіальна адресація.
- Обертання трійки й пошук кластера «трикутник» після кожного кроку — 📎.
- Квітка: пошук кільця з 6 навколо центру, перетворення центру — 📎.
- Каскад із падінням на гекс-сітці (зсув стовпців півклітинками) — 🥉.
- Бомба-лічильник + множник «чистить увесь колір» — 🌱.
- Survival: замикання при безвиході та детектор «нема ходів» (перебрати всі вершини × 2 напрямки) — 🥉.

## Мапа на каталог
- Є: `gravity-fall`, `spawn-random-cell`, `chain-reaction` ↔ каскад · `event-points` · `time-out`, `time-bonus` ↔ Timed · `score-records`, `leaderboard` · `mode-select`, `game-pause`, `end-screen` · `selection-highlight` ↔ курсор · `gui-render`, `particles`, `background-music`.
- Перевикористано з Bejeweled: `+cascade-refill`, `+special-tiles`, `+countdown-tile`.
- **Нема** → пропозиції карток:
  - `+rotate-triple-hex` «Поворот трійки гексів навколо вершини» · entities/state · 📎 — курсор-вершина.
  - `+hex-cluster-match` «Кластер 3 взаємно суміжних гексів» · entities/interact · 📎.
  - `+ring-match` «Кільце з 6 однакових навколо центру» · entities/interact · 📎.
  - `+lock-on-no-moves` «Безвихідь замикає лишки» · game-logic/lose · 🥉.
  - `+color-meter-attack` «Метр кольору → атака супернику» · game-logic/opponent · 🥈 (Hexic 2).

## Пропозиції до словників
- `+effect:rotate_group` — повернути групу сутностей навколо точки (вершини, центру).
- `+trigger:pattern(ring6)` — нова форма для `pattern`: кільце з 6 навколо центру.
- `+cond:mutually_adjacent` — набір клітин попарно суміжний (трикутник гексів).
- `+effect:lock_all` — замкнути всі плитки на полі.
- `+card:rotate-triple-hex`, `+card:ring-match` — див. мапу.
- `+ui:vertex-cursor` — курсор у вершині між клітинами, а не в клітині.

## Джерела
- ⭐ [Wikipedia: Hexic](https://en.wikipedia.org/wiki/Hexic) — кластер «три однакові торкаються», каскади, бонусні зірки, квітка → срібна зірка, чорна перлина (Y), бомби з лічильником і множники, Marathon/Timed (до 2 хв)/Survival (50 раундів), Hexic HD 2005.
- [Wikipedia: Hexic 2](https://en.wikipedia.org/wiki/Hexic_2) — смарагд, рубін, метри кольорів, 4 атаки, Battle.
- YouTube: пошук «hexic hd gameplay».

## Непевне
- (?) Розмір поля й кількість кольорів — у відкритих джерелах не знайшов.
- (?) Що трійка без збігу крутиться до повного оберту (3 кроки) — з власних знань.
- (?) Wikipedia плутає «gold-star» і «silver-star» щодо того, що утворює квітка і що обертає кільце; у таблиці — найправдоподібніше прочитання.
- (?) Як саме зʼявляються бонусні зірки й множники та їхні числа — не описано.
- (?) Розкладка кнопок і мишача схема MSN-версії — з власних знань.
- (?) Сімʼя: за families.md гра — `falling-match` (падіння й поповнення), обертання трійки — другорядне.
