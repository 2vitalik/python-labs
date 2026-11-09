---
title: Pepper II
slug: pepper-ii
aka: [Пеппер II]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: territory
year: 1982
platforms: [arcade, ColecoVision]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pepper_II", best: true, note: "застібка, вила, центральний енерджайзер, Whippersnapper, 4 лабіринти на рівень"}
  - {kind: play, url: "https://archive.org/details/arcade_pepper2", note: "Internet Arcade — грати; опис механік і формат автомата"}
  - {kind: other, url: "https://www.arcade-museum.com/Videogame/pepper-ii", note: "KLOV: джойстик 4 напрямки, 1–2 гравці по черзі, порівняння з Amidar"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pepper+ii+exidy+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, path-cut, visited-trail, touch-death, player-death, chase-player, temporary-modes, event-points, extra-life-threshold, sequential-levels, progress-acceleration, mode-indicator, status-panel, game-screen, +line-paint-box-fill, +trail-eraser-enemy, +multi-screen-maze-exits, +corner-power-up, +alternating-power-item, +enemy-removal-power, +prize-in-box]
proposes: ["+effect:leave_trail", "+effect:clear_trail", "+effect:switch_screen", "+ui:screens-done-marker", "+ui:prize-shelf", "+card:trail-eraser-enemy", "+card:multi-screen-maze-exits"]
author: opus
date: 2026-11-09
---

# Pepper II — Amidar із «застібкою»: обведи клітку — заллєш її, але ворог розстібає незавершене

## Суть
Ангел Пеппер бігає лініями сітки й лишає за собою «застібку»; щойно відрізки замкнуть клітку з усіх боків, вона заливається кольором і дає очки. Повернення назад по незавершеній застібці її розстібає, а ворог Whippersnapper розстібає все незавершене, по чому проїде. Рівень — це **чотири звʼязані лабіринти**: з кожного є виходи в три інші, і пройти рівень можна, лише заливши всі чотири. Енерджайзери — не точки, які зʼїдають, а клітки, які треба обвести.

## Поле і час
- Сітка ліній (відрізки між вузлами) поверх кліток-прямокутників; рух — лише лініями, як в Amidar.
- 4 екрани-лабіринти на рівень; виходи по краях ведуть в інші лабіринти (з кожного — у три інші). Стан заливки кожного лабіринту зберігається.
- Кутові клітки містять вила, центральна — «делюкс-енерджайзер», одна клітка — приз.
- Real-time; стан диявола триває близько 4 секунд.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пеппер (ангел) | player | життя | рух 4 напрямки лініями; лишає застібку |
| Застібка (відрізок) | mark | стан: застебнуто / ні | частина периметра клітки; розстібається від повернення назад і від Whippersnapper |
| Клітка | zone | залита / ні | заливається, коли весь периметр застебнуто |
| Вила (pitchfork) | pickup | 4 у кутах лабіринту | обвести клітку з вилами → Пеппер стає дияволом ~4 с |
| Делюкс-енерджайзер | pickup | стан: вила ↔ німб | у центрі; чергує вигляд; німб прибирає Whippersnapper з цього лабіринту |
| Приз | pickup | 1 на лабіринт | обвести клітку → очки, приз показано під лабіринтом |
| Roaming Eyes | enemy | — | переслідують; дотик вбиває; дияволом їх можна зʼїсти |
| Whippersnapper (Zipper Ripper на ColecoVision) | enemy | — | розстібає незавершені відрізки, по яких іде; завмирає, поки Пеппер диявол |
| Вихід з лабіринту | static | куди веде | перехід в інший із 4 лабіринтів рівня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `custom: «у напрямку dir є лінія»` → ТО `move(pepper, dir)`, `custom: «відрізок під Пеппером застебнуто»`.
- КОЛИ `custom: «Пеппер іде назад по застібці незамкненої клітки»` → ТО `custom: «відрізок розстібнуто»`.
- КОЛИ `pattern(region_closed)` → ТО `fill(box)`, `score(n)`.
- КОЛИ `pattern(region_closed)` → ЯКЩО `occupied(box, pitchfork)` → ТО `set_state(pepper, devil, ~4 с)`, `stun(whippersnapper, ~4 с)`.
- КОЛИ `pattern(region_closed)` → ЯКЩО `occupied(box, energizer)` and `state(energizer, pitchfork)` → ТО як для вил.
- КОЛИ `pattern(region_closed)` → ЯКЩО `occupied(box, energizer)` and `state(energizer, halo)` → ТО `disappear(whippersnapper)` у цьому лабіринті.
- КОЛИ `timer(every)` → ТО `custom: «енерджайзер міняє вигляд: вила ↔ німб»`.
- КОЛИ `pattern(region_closed)` → ЯКЩО `occupied(box, prize)` → ТО `pickup`, `score(n)`, `custom: «приз з'являється під лабіринтом»`.
- КОЛИ `contact(whippersnapper, zipper)` → ЯКЩО `custom: «клітка ще не залита»` → ТО `custom: «відрізок розстібнуто»`.
- КОЛИ `contact(pepper, eyes)` → ЯКЩО `state(pepper, devil)` → ТО `disappear_b`, `score(n)`; інакше `lose` (життя −1).
- КОЛИ `contact(pepper, whippersnapper)` → ЯКЩО `not state(pepper, devil)` → ТО `lose` (?).
- КОЛИ `edge(pepper)` → ТО `custom: «перехід у сусідній лабіринт рівня через вихід»`.
- КОЛИ `custom: «усі клітки лабіринту залито»` → ТО `score(bonus)`, `sound(Zip-a-Dee-Doo-Dah)`.
- КОЛИ `custom: «залито всі 4 лабіринти»` → ТО `score(bonus)`, `custom: «кубик-позначка внизу екрана»`, `next_level`.
- КОЛИ `counter(score, >=, threshold)` → ТО `lives(+1)`; поріг 40 000 / 50 000 / 70 000 / 90 000 — DIP оператора.
- Перемога: нема (нескінченна аркада). Поразка: 0 життів. Рахунок: заливка кліток, Eyes у стані диявола, призи, бонуси за лабіринт і за четвірку.

## Керування і ввід
- Джойстик 4 напрямки; кнопка на джойстику є у специфікації автомата (archive.org), призначення не підтверджено (?).
- Уся «дія» — сам маршрут: що обвести першим (вила, приз, німб) і як не дати Whippersnapper розстебнути довгу незавершену петлю.
- 1–2 гравці по черзі (KLOV).

## Вікна, меню, HUD
- `splash-screen` / атракт (?).
- `game-screen` — один із 4 лабіринтів; HUD: `score`, `hi-score` (?), `lives`, полиця зібраних призів під лабіринтом (`custom: «prize-shelf»`), кубики-позначки пройдених четвірок (`custom: «screens-done-marker»`).
- Переходи: атракт → (монета) game-screen ↔ (вихід на краю) інший лабіринт → (4 залито) наступний рівень → (0 життів) атракт.

## Фічі поза полем
- `levels-sequential`; складність зростає з рівнями (archive.org).
- `operator-settings`: поріг бонусного життя DIP-перемикачами.
- ColecoVision: 1–2 гравці, 4 рівні складності (`difficulty-presets`).
- Нема паузи, збережень.

## Варіації й родичі
- Amidar (заливка прямокутників обведенням), Pac-Man (енерджайзер → зʼїсти ворогів), Xonix і Qix (захоплення території).
- Осі: **хто руйнує прогрес** (ніхто — Amidar / ворог-стирач — Pepper II / дотик до сліду вбиває — Xonix); **поле**: один екран / кілька звʼязаних екранів; **енерджайзер**: точка, яку їдять / клітка, яку обводять / предмет зі змінним ефектом.

## Цікавинки для курсу
- Застібка: слід, що стає постійним лише після замикання клітки, і відкат по сліду — 🥉: стан ребер + перевірка замкненості периметра.
- Whippersnapper — ворог, що стирає незавершений прогрес гравця — 📎.
- Чотири лабіринти з виходами-порталами і збереженим станом кожного — 🥉: кілька полів і перемикання між ними.
- Делюкс-енерджайзер з циклом «вила ↔ німб» і різним ефектом залежно від моменту — 📎.
- Енерджайзер-клітка: сила вмикається не дотиком, а обведенням — 🌱 поверх заливки.

## Мапа на каталог
- Є: `move-4dir` · `path-cut` (повернення по сліду стирає його) · `visited-trail` (застебнуті відрізки) · `touch-death` · `player-death` · `chase-player` · `temporary-modes` (диявол) · `event-points` · `extra-life-threshold` · `sequential-levels` · `progress-acceleration` · `mode-indicator` · `status-panel` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+line-paint-box-fill` «Обвести клітку — залити» · entities/interact · 🥉 (є в Amidar).
  - `+trail-eraser-enemy` «Ворог стирає незавершений слід» · entities/move · 📎.
  - `+multi-screen-maze-exits` «Рівень із кількох екранів-лабіринтів, звʼязаних виходами» · levels/progression · 🥉 · слот {screens: 4}.
  - `+corner-power-up` «Сила в кутах» · entities/state · 🌱.
  - `+alternating-power-item` «Предмет із циклом ефектів» · entities/state · 📎.
  - `+enemy-removal-power` «Бонус прибирає ворога з поля» · entities/interact · 🌱.
  - `+prize-in-box` «Приз у клітці, яку треба обвести» · entities/interact · 🌱.

## Пропозиції до словників
- `+effect:leave_trail` — рух лишає позначку на відрізку/клітині (застібка).
- `+effect:clear_trail` — стерти незавершений слід (повернення назад, Whippersnapper).
- `+effect:switch_screen` — перейти на інший екран-лабіринт рівня зі збереженням його стану.
- `+ui:screens-done-marker` — позначки пройдених наборів екранів (кубики).
- `+ui:prize-shelf` — зібрані призи під полем.
- `+card:trail-eraser-enemy`, `+card:multi-screen-maze-exits` — див. вище.

## Джерела
- ⭐ [Wikipedia: Pepper II](https://en.wikipedia.org/wiki/Pepper_II) — застібка й розстібання, Roaming Eyes, Whippersnapper, вила ~4 с, делюкс-енерджайзер, призи, 4 лабіринти, бонусні життя.
- [Internet Arcade: Pepper II](https://archive.org/details/arcade_pepper2) — грати; переходи між лабіринтами через краї, формат автомата.
- [KLOV: Pepper II](https://www.arcade-museum.com/Videogame/pepper-ii) — джойстик 4 напрямки, 1–2 гравці по черзі, «як Amidar».
- YouTube: пошук «pepper ii exidy arcade gameplay».

## Непевне
- (?) Кількість Roaming Eyes, їхня поведінка (переслідування чи блукання), чи повертаються після зʼїдання.
- (?) Чи вбиває дотик до Whippersnapper, чи він лише стирає застібку.
- (?) Очки за клітку, Eyes, призи, бонуси лабіринту — у джерелах нема.
- (?) Призначення кнопки на джойстику; стартова кількість життів.
- (?) Період зміни «вила ↔ німб»; розмір сітки в клітках.
- (?) Як саме Pepper II розподіляє виходи (які краї ведуть у який лабіринт).
