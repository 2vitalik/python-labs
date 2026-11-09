---
title: Marvin's Maze
slug: marvins-maze
aka: []
family: maze-arcade
also: []
klass: avatar
axes:
  field: layers
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: collect
year: 1983
platforms: [arcade (SNK), PSP/PS3 (PlayStation Minis, 2011)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Marvin%27s_Maze", best: true, note: "два поверхи, переходи в 4 кутах, power dot = 1 лазер крізь ряд ворогів, рухомі перехрестя, «trick» — ворог у яму, Robonoids прискорюються"}
  - {kind: other, url: "https://www.arcade-museum.com/Videogame/marvins-maze", note: "KLOV: вертикальні труби між поверхами, ковзні платформи, постріли накопичуються, бонус за кількох одним пострілом, 4-way + 1 кнопка"}
  - {kind: other, url: "https://archive.org/details/ArcadeGameManualMarvinsmaze", note: "інструкція conversion kit: DIP — життя 1/2/3/5, перше бонус-життя 10 000–80 000, другий бонус, continue, музика в attract"}
  - {kind: other, url: "https://www.familyfriendlygaming.com/Reviews/2011/Marvins%20Maze.html", note: "PS Minis: ліфти в кутах, платформи через прогалини, Super Dot = 1 постріл, вибір життів, Immortal, збереження"}
  - {kind: other, url: "https://www.thelogbook.com/?p=34151", note: "огляд: труби між поверхами, односторонні мости, рівень — лише після всіх точок і power-ups"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Marvin%27s+Maze+SNK", note: "пошук; геймплей аркади"}
stage: v1
coverage: 50
mechanics: [move-4dir, collect-all, chase-player, touch-death, player-death, item-pickup, projectile-shot, shoot-forward, carrier-platform, one-way-cell, event-points, extra-life-threshold, progress-acceleration, sequential-levels, hot-seat, attract-demo, game-over-continue, game-screen, +two-layer-field, +junction-toggle, +pit-trick, +piercing-shot, +ammo-limit, +multi-kill-bonus, +alt-clear-condition]
proposes: ["+card:pit-trick", "+card:piercing-shot", "+card:multi-kill-bonus", "+card:alt-clear-condition"]
author: opus
date: 2026-11-09
---

# Marvin's Maze — двоповерховий лабіринт: їж точки, тікай на інший поверх кутовими переходами, скидай Robonoids у ями

## Суть
Марвін збирає точки в лабіринті з двох поверхів, а Robonoids женуться за ним. Переходи в чотирьох кутах перекидають на інший поверх, рухомі перехрестя й платформи перебудовують коридори: так можна відрізати погоню або скинути ворога в яму («trick»). Великі точки дають по одному лазерному пострілу, що пробиває всіх ворогів на лінії. Рівень пройдено, коли зʼїдено всі точки або знищено задану кількість Robonoids.

## Поле і час
- Поле — **два поверхи** одного лабіринту (`field: layers`); переходи між ними — у чотирьох кутах (Wikipedia; KLOV — «вертикальні труби», PS Minis — «ліфти»). Перехід може вивести просто біля іншого ворога.
- Рухомі перехрестя / ковзні платформи міняють, які коридори зʼєднані; у місцях, де перехрестя відʼїхало, лишається яма (?).
- Односторонні мости (огляд The Logbook) пропускають лише в один бік.
- Real-time, вертикальний монітор; лабіринт міняється з рівнем, Robonoids швидшають з прогресом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Марвін | player | життя (DIP: 1/2/3/5) | рух 4 напрямки, стріляє лазером, переходить між поверхами |
| Точка | pickup | — | очки; зʼїсти всі — пройти рівень |
| Велика точка (power / Super Dot) | pickup | +1 постріл | постріли накопичуються (KLOV) |
| Лазер (стріла) | projectile | пробивний | летить по коридору, знищує всіх Robonoids на лінії |
| Robonoid | enemy | швидкість росте з рівнем | переслідує Марвіна; дотик — смерть Марвіна |
| Нижній / верхній поверх | zone | 2 | окремі мережі коридорів |
| Кутовий перехід (труба, ліфт) | terrain | 4 кути | переносить на той самий кут іншого поверху |
| Рухоме перехрестя / ковзна платформа | terrain | положення | перебудовує коридори; везе Марвіна через прогалину |
| Яма | hazard | — | Robonoid, що опинився над нею, падає й гине («trick») |
| Односторонній міст | terrain | напрям | прохід лише в один бік |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(marvin, dir)`.
- КОЛИ `contact(marvin, dot)` → ТО `disappear(dot)`, `score(+dot)`.
- КОЛИ `contact(marvin, power_dot)` → ТО `disappear(power_dot)`, `counter(shots, +1)`.
- КОЛИ `input(fire)` → ЯКЩО `counter(shots, >, 0)` → ТО `spawn(laser)` у напрямку руху, `counter(shots, -1)`.
- КОЛИ `contact(laser, robonoid)` → ТО `disappear(robonoid)`, `score(+)`, `custom: «промінь летить далі й знищує всіх на лінії»`.
- КОЛИ `destroyed(robonoid)` → ЯКЩО `chain(2)` у межах одного пострілу → ТО `score(bonus)`.
- КОЛИ `enter(marvin, corner_passage)` → ТО `teleport(marvin, same_corner_other_floor)`.
- КОЛИ `enter(marvin, sliding_platform)` → ТО `carry(marvin)` через прогалину.
- КОЛИ `custom: «рухоме перехрестя зсунулось»` → ЯКЩО `occupied(gap, robonoid)` → ТО `fall(robonoid)`, `disappear(robonoid)`, `score(+trick)`.
- КОЛИ `enter(marvin, one_way_bridge)` → ЯКЩО `not moving(marvin, bridge_dir)` → ТО `block`.
- КОЛИ `tick` → ТО `custom: «Robonoid іде до Марвіна коридорами свого поверху»`.
- КОЛИ `contact(robonoid, marvin)` → ТО `lives(-1)` (Марвіна «вбиває струмом»).
- КОЛИ `all_gone(dot)` → ТО `next_level`.
- КОЛИ `counter(robonoids_killed, >=, quota)` → ТО `next_level`.
- КОЛИ `level_start` → ТО `speed(robonoid, +1)`, `custom: «інший план лабіринту»`.
- КОЛИ `counter(score, >=, first_bonus)` → ТО `lives(+1)`; другий бонус — на `first_bonus + first_bonus × k` (k = 1…3 або вимкнено, DIP).
- КОЛИ `counter(lives, ==, 0)` → ЯКЩО `custom: «DIP continue увімкнено»` → ТО `window(game-over-continue)`; інакше `game_over`.
- Перемога: нескінченна черга рівнів. Поразка: життя вичерпано. Рахунок: точки, великі точки, Robonoids (лазер, «trick»), бонус за кількох одним пострілом.

## Керування і ввід
- Аркада: 4-напрямний джойстик і одна кнопка — постріл (KLOV).
- 1–2 гравці по черзі (alternating); у PS Minis — hotseat із порівнянням рахунку.
- Перехід між поверхами — рухом у кутовий перехід, окремої кнопки нема (?).

## Вікна, меню, HUD
- `attract-demo` — режим очікування автомата; музика в ньому вмикається DIP-перемикачем.
- `game-screen`: лабіринт двох поверхів, `score`, `hi-score`, `lives`, запас пострілів (?).
- `game-over-continue` — «продовжити?» після останнього життя, якщо оператор увімкнув continue.
- `end-screen` — GAME OVER (?).
- PS Minis: `settings-window` — кількість життів на старті, режим Immortal (нескінченні життя), складність; збереження й продовження гри.
- Переходи: attract → game-screen → (рівень пройдено) наступний лабіринт; (0 життів) → continue / end-screen → attract.

## Фічі поза полем
- `operator-settings` (DIP SW): життя 1/2/3/5; continue; монети/кредити й free play; перше бонус-життя 10 000–80 000 кроком 10 000; другий бонус — вимкнено / +1-й / +1-й×2 / +1-й×3; музика в attract; стіл/стійка, переворот екрана; «screen stop».
- `levels-sequential` з наростанням темпу ворогів.
- PS Minis (2011): `assist-mode` (Immortal), `difficulty-presets`, `save-slots` (?), `hotseat`.

## Варіації й родичі
- `pac-man` — точки й погоня; Марвін додає поверхи, зброю й перебудову лабіринту.
- `lock-n-chase` — двері, що відрізають погоню; `mouse-trap` — перемикні двері-перехрестя; `heiankyo-alien` — ворог у ямі як спосіб убивства.
- `crystal-castles` — ізометричні рівні з висотами, `3d-monster-maze` — інший підхід до «більше одного виміру».
- **Осі варіацій:** поверхи (1 / 2 з кутовими переходами / багато) · як убити ворога (стріляти / скинути в яму / не можна) · зброя (за підбиранням / запас / нескінченна) · умова рівня (усі точки / квота вбивств / будь-яка з двох).

## Цікавинки для курсу
- Два шари поля з переходами в кутах: пошук шляху ворога мусить враховувати перехід між поверхами — 🥈 (BFS по двошаровому графу).
- «Trick»: перехрестя зсувається, ворог над прогалиною падає — 📎 (подія поля вбиває сутність, а не контакт).
- Пробивний лазер: усі вороги на лінії до стіни — 🌱; бонус за кількох одним пострілом — 🌱.
- Запас пострілів із підбирань — 🌱 (лічильник ammo).
- Дві альтернативні умови рівня (усі точки АБО N убитих) — 🌱.
- Односторонній міст як клітина з дозволеним напрямком — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `collect-all` · `chase-player` · `touch-death` + `player-death` · `item-pickup` · `projectile-shot` + `shoot-forward` · `carrier-platform` (платформа везе через прогалину) · `one-way-cell` (односторонні мости) · `event-points` · `extra-life-threshold` · `progress-acceleration` · `sequential-levels` · `hot-seat` · `attract-demo` · `game-over-continue` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+two-layer-field` (є пропозиція) — тут слот {layers: 2, link: corners}.
  - `+junction-toggle` (є пропозиція) — рухоме перехрестя в лабіринті, не лише стрілка колії.
  - `+pit-trick` «Ворог падає в прогалину рухомого перехрестя» · entities/death · 📎.
  - `+piercing-shot` «Постріл пробиває ряд ворогів» · entities/combat · 🌱.
  - `+ammo-limit` (є пропозиція) — тут постріли з великих точок, накопичуються.
  - `+multi-kill-bonus` «Бонус за кількох одним ударом» · game-logic/score · 🌱 · слот {min: 2}.
  - `+alt-clear-condition` «Рівень проходиться будь-якою з двох умов» · game-logic/win · 🌱 · слот {or: [collect_all, kill_n]}.

## Пропозиції до словників
- `+card:pit-trick`, `+card:piercing-shot`, `+card:multi-kill-bonus`, `+card:alt-clear-condition` — див. «Мапу на каталог».
- Слова правил вистачило: перехід між поверхами — `teleport`, платформа — `carry`, падіння — `fall`; DIP-налаштування — уже ✅ `operator-settings`.

## Джерела
- ⭐ [Wikipedia: Marvin's Maze](https://en.wikipedia.org/wiki/Marvin%27s_Maze) — два поверхи з переходами в кутах, power dot = один лазер, рухомі перехрестя, «trick», прискорення ворогів, PS Minis.
- [KLOV: Marvin's Maze](https://www.arcade-museum.com/Videogame/marvins-maze) — труби між рівнями, ковзні платформи, накопичення пострілів, бонус за кількох, джойстик + кнопка, 2 гравці по черзі.
- [Internet Archive: SNK conversion kit manual](https://archive.org/details/ArcadeGameManualMarvinsmaze) — таблиця DIP-перемикачів (OCR).
- [Family Friendly Gaming: огляд PS Minis](https://www.familyfriendlygaming.com/Reviews/2011/Marvins%20Maze.html) — ліфти в кутах, платформи, Super Dot, меню життів/Immortal/складності, збереження.
- [The Logbook: Phosphor Dot Fossils](https://www.thelogbook.com/?p=34151) — труби між поверхами, односторонні мости, умова рівня.
- YouTube: пошук «Marvin's Maze SNK».

## Непевне
- (?) Що саме зсуває перехрестя (прохід Марвіна, таймер чи кнопка) і як утворюється яма — джерела кажуть лише «рухомі перехрестя» / «ковзні платформи».
- (?) Очки: сніпет пошуку (сторінка не відкрилась) дає «trick — 500, Super Dot — 200, бонус кінця раунду 500 × знищені»; не перевірено.
- (?) Квота Robonoids для проходу рівня, кількість ворогів, їхні типи й алгоритм погоні.
- (?) Як два поверхи показано на одному екрані; чи бачать і переслідують Robonoids через поверхи; чи ходять вони кутовими переходами.
- (?) Чи рівень вимагає ще й усіх великих точок (The Logbook: «усі точки й power-ups»).
- (?) Розташування лічильника пострілів у HUD; збереження в PS Minis — зі слів одного огляду.
