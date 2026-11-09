---
title: Head On
slug: head-on
aka: [ヘッドオン, Head On Part II, Head On 2, Head On N]
family: maze-arcade
also: []
klass: avatar
axes:
  field: graph
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: collect
year: 1979
platforms: [arcade (Sega/Gremlin), Commodore 64, VIC-20, PC-8801, Sharp MZ, Sega Saturn, PS2]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Head_On_(video_game)", best: true, note: "суть: доріжки, проміжки для перемикання, ШІ-машина назустріч; таймер → життя; сиквели й клони"}
  - {kind: other, url: "https://ja.wikipedia.org/wiki/ヘッドオン", note: "JA Wikipedia: 5 смуг, газ, 2 смуги на низькій / 1 на високій швидкості, червоні машини +1 за 2 стадії до 3, 8 стадій, Head On II"}
  - {kind: other, url: "https://www.arcade-museum.com/Videogame/head-on", note: "KLOV: 4-way джойстик, 4 місця зміни смуги, більше/швидших суперників з рівнем"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=head+on+1979+sega+arcade+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 70
mechanics: [move-auto, move-4dir, collect-all, touch-death, player-death, chase-greedy, sequential-levels, progress-acceleration, reinforcements, event-points, status-panel, game-screen, +lane-ring-field, +lane-switch-gaps, +speed-boost-button, +speed-limits-turns, +head-on-collision, +u-turn-lane]
proposes: ["+effect:lane_change", "+cond:speed_mode", "+role:lane", "+card:lane-ring-field", "+card:lane-switch-gaps", "+card:speed-boost-button", "+card:head-on-collision"]
author: opus
date: 2026-11-09
---

# Head On — машина кружляє концентричними смугами, збирає точки й ухиляється від лобового зіткнення з ШІ

## Суть
Гравцева машина безупинно їде по колу концентричних прямокутних смуг, усипаних точками; назустріч їде машина компʼютера. Змінювати смугу можна лише в чотирьох проміжках — посередині кожної сторони. Мета — з'їсти всі точки, не зіткнувшись лоб у лоб; кнопка газу пришвидшує, але тоді в проміжку можна перескочити лише на одну смугу. Одна з перших dot-eating ігор: Pac-Man вийшов наступного року.

## Поле і час
- Поле — 4–5 вкладених прямокутних кілець-смуг (джерела розходяться) з проміжками на чотирьох сторонах; у центрі — табло очок і запасних машин. Суміжність — граф кілець, з'єднаних лише в проміжках (`field: graph`).
- Real-time: машини рухаються постійно; гравець проти годинникової (?) — суперник навстріч.
- Стадія = прохід усіх точок; 8 стадій, далі цикл з початку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Машина гравця | player | швидкість: низька / висока (газ) | рух уперед по смузі; у проміжку — зміна смуги джойстиком |
| Червона машина | enemy | 1→3 шт. (Head On II — до 4) | їде назустріч; у проміжку змінює смугу на ≤1 до гравця |
| Смуга | terrain (`+role:lane`) | кільце | замкнений шлях без розворотів |
| Проміжок перемикання | zone | 4 шт. (по центру сторін) | лише тут можна змінити смугу |
| Точка | pickup | очки | з'їдається проїздом |
| Спецточка (червоний ромб) | pickup | більше очок, ніж звичайна | з'їдається проїздом |
| U-turn смуга (Head On II) | terrain | — | дозволяє розвернутися; біля неї перемикання до 4 смуг |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(car, forward)` уздовж смуги; на розі — `face(car, next_side)`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(cell, switch_gap) and not custom: «газ натиснуто»` → ТО `custom: «перехід до 2 смуг убік dir»` (`+effect:lane_change`).
- КОЛИ `input(dir)` → ЯКЩО `occupied(cell, switch_gap) and custom: «газ натиснуто»` (`+cond:speed_mode`) → ТО `custom: «перехід на 1 смугу»`.
- КОЛИ `input(gas)` → ТО `speed(player, +n)` поки кнопку тримають.
- КОЛИ `enter(enemy, switch_gap)` → ТО `custom: «змінює смугу на ≤1 у бік смуги гравця»` (жадібне переслідування).
- КОЛИ `contact(player, dot)` → ТО `disappear_b`, `score(dot_value)`.
- КОЛИ `contact(player, special_dot)` → ТО `disappear_b`, `score(special_value)`.
- КОЛИ `contact(player, enemy)` → ТО `sound(crash)`, `lives(-1)`, `restart` позицій (?).
- КОЛИ `all_gone(dot)` → ТО `message("BONUS")`, `next_level`.
- КОЛИ `level_start` → ЯКЩО `custom: «номер стадії парний»` → ТО `spawn(enemy)` до максимуму 3.
- КОЛИ `all_gone(dot)` → ЯКЩО `counter(stage, ==, 8)` → ТО `custom: «цикл з першої стадії»`.
- КОЛИ `counter(score, >=, 100000)` → ТО `set_value(score, 0)` — лічильник переповнюється.
- Head On II: КОЛИ `enter(player, u_turn_lane)` → ТО `face(player, opposite)`; `spawn(enemy)` щостадії до 4.
- Перемога: з'їсти всі точки стадії · Поразка: 0 запасних машин · Рахунок: точки й спецточки, бонус за стадію (?).

## Керування і ввід
- 4-напрямний джойстик: у верхньому/нижньому проміжку — вгору/вниз, у лівому/правому — ліворуч/праворуч = перехід на сусідню смугу.
- Кнопка газу (тримати) — висока швидкість; без неї — повільно.
- 1–2 гравці по черзі (alternating).

## Вікна, меню, HUD
- `attract-demo` — режим очікування автомата (?).
- `game-screen`: кільця-смуги з точками; у центрі `score` і `lives` (запасні машини).
- `custom-window` «BONUS» — напис після зачистки стадії.
- `end-screen` — GAME OVER (?).
- Кабінет: вертикальна орієнтація для японських коктейль-столів, горизонтальна для американських upright.

## Фічі поза полем
- `levels-sequential`: 8 стадій із наростанням кількості суперників, потім цикл.
- У прототипі раунди були на час; дизайнер Lane Hauck замінив таймер на життя — «ключ до успіху».
- `operator-settings` — кількість машин тощо (?).

## Варіації й родичі
- Head On Part II / Head On 2 (1979): U-turn смуга, розумніший ШІ, суперників +1 щостадії до 4.
- Car Hunt (1979, «Head On III»): складніший лабіринт, естакади, поворот у будь-який бік, вороги різної агресивності.
- Head On N (Irem/Nintendo) — ліцензована японська версія.
- Клони: Crash (Exidy, 1979), Dodge 'Em (Atari 2600) — 3–6 смуг у різних клонах.
- Родичі: `pac-man` (точки + переслідувачі), `amidar` (рух графом), `frogger` (смуги).
- **Осі варіацій:** смуг 3–6 · розворот: нема / U-turn смуга / будь-де · перемикання: лише в проміжках / будь-де · кількість суперників: росте за 2 стадії / щостадії · ціна газу: менше смуг за перемикання / нема.

## Цікавинки для курсу
- Поле як граф кілець із чотирма «вузлами перемикання» — 🌱: найменший цікавий граф руху.
- Компроміс швидкості: газ = швидше, але менша свобода маневру — 📎.
- Жадібний суперник, що в кожному проміжку зсувається на 1 смугу до гравця — 🌱.
- Передбачення лобового зіткнення: на якій смузі будеш ти і він у момент зустрічі — 🥉 (простий AI-помічник або AI-гравець).
- Наростання суперників за розкладом стадій — 🌱.

## Мапа на каталог
- Є: `move-auto` · `move-4dir` (джойстик) · `collect-all` · `touch-death` · `player-death` · `chase-greedy` · `sequential-levels` · `progress-acceleration` · `reinforcements` (+1 суперник за стадії) · `event-points` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+lane-ring-field` «Поле з концентричних кілець» · board/field · 📎 · слот {lanes: 3–6}.
  - `+lane-switch-gaps` «Зміна смуги лише в проміжках» · entities/move · 🌱 · слот {gaps: 4}.
  - `+speed-boost-button` «Газ: тримай — швидше» · entities/move · 🌱.
  - `+speed-limits-turns` «Швидкість обмежує маневр» · entities/move · 📎 — 2 смуги повільно / 1 швидко.
  - `+head-on-collision` «Суперник навстріч» · entities/combat · 🌱.
  - `+u-turn-lane` «Смуга для розвороту» · entities/move · 🌱 (Head On II).

## Пропозиції до словників
- `+effect:lane_change` — перехід на N сусідніх смуг (Head On, Frogger-подібні, лейн-шутери).
- `+cond:speed_mode` — сутність у режимі швидкості (газ натиснуто).
- `+role:lane` — смуга-доріжка як сутність поля (уже пропонували інші ігри; підтверджую).
- `+card:lane-ring-field`, `+card:lane-switch-gaps`, `+card:speed-boost-button`, `+card:head-on-collision` — див. «Мапу на каталог».

## Джерела
- ⭐ [Wikipedia: Head On (video game)](https://en.wikipedia.org/wiki/Head_On_(video_game)) — суть гри, таймер → життя, орієнтації кабінету, Head On II, Car Hunt, Head On N, Crash, Dodge 'Em.
- [Wikipedia JA: ヘッドオン](https://ja.wikipedia.org/wiki/ヘッドオン) — 5 смуг, газ, правило 2/1 смуги, червоні машини 1→3, 8 стадій, спецточки, переповнення на 100 000, деталі Head On II.
- [KLOV: Head On](https://www.arcade-museum.com/Videogame/head-on) — 4 смуги, 4 місця перемикання, джойстик 4-way, 2 гравці по черзі.
- YouTube: пошук «head on 1979 sega arcade gameplay».

## Непевне
- (?) Кількість смуг: 5 (JA Wikipedia) чи 4 (KLOV).
- (?) Вартість звичайної точки й спецточки; чи є бонус за стадію, за яким з'являється напис BONUS.
- (?) Напрямок руху гравця (за чи проти годинникової стрілки).
- (?) Що відбувається після аварії: рестарт позицій зі збереженням з'їдених точок чи ні.
- (?) Пороги додаткової машини й DIP-налаштування оператора.
- (?) Як саме червона машина обирає смугу (завжди до гравця чи з випадковістю).
