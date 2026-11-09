---
title: Domino Man
slug: domino-man
aka: []
family: maze-arcade
also: []
klass: avatar
axes:
  field: free
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 1983
platforms: [arcade (Bally Midway MCR-II)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Domino_Man", best: true, note: "доміно на кожну чорну крапку, перехожі валять, хуліган, бджола, годинник, бонус за кожне доміно, вірш наприкінці"}
  - {kind: other, url: "https://www.arcade-history.com/game/660/", note: "Arcade History: персонажі (хуліган, бджола, бабця, хлопчик з візком), 8-way + 1 кнопка, вибір «повалити або чекати»"}
  - {kind: other, url: "https://basementarcade.com/Domino_Man.html", note: "огляд: рівень = виставити весь ланцюг і повалити"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Domino+Man+arcade", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-8dir, chain-reaction, random-walk, chase-player, touch-death, player-death, event-points, keep-playing-after-win, sequential-levels, game-screen, end-screen, background-music, +fill-marked-spots, +remove-to-break-chain, +shove-wanderer, +push-your-luck-bonus, +invincible-wanderer]
proposes: ["+window:poem-rating", "+card:fill-marked-spots", "+card:remove-to-break-chain", "+card:shove-wanderer", "+card:push-your-luck-bonus"]
author: opus
date: 2026-11-09
---

# Domino Man — розстав доміно на всі позначки, поки перехожі їх валять, і повали весь ланцюг сам

## Суть
Аркада без лабіринту: Domino Man бігає вулицею й ставить доміно на чорні крапки, що складаються в лінію чи фігуру. Перехожі блукають навмання і збивають доміно — падіння біжить ланцюгом, і його треба зупинити, прибравши одне доміно на шляху. Коли весь ланцюг стоїть, гравець вирішує: повалити його й забрати бонус за кожне доміно — чи ризикнути й грати далі, щоб бонус ріс. Межова гра сімʼї: рух вільний, а «сітковий шар» — лише ланцюг слотів-крапок.

## Поле і час
- Один екран вулиці; рух вільний 8-напрямний (`field: free`).
- Дискретний шар — послідовність крапок-слотів: кожен порожній або з доміно; падіння поширюється вздовж цієї послідовності (по суті 1D-ланцюг).
- Real-time; перехожі, бджола й годинник рухаються незалежно від гравця.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Domino Man | player | життя | ставить і знімає доміно, бʼє доміно як палицею |
| Чорна крапка | mark | позиція в ланцюгу | місце під доміно |
| Доміно | object | стоїть / падає | збите — падає й валить сусіднє в ланцюгу |
| Перехожі (бабця, хлопчик з візком) | neutral | — | блукають наосліп, зрідка збивають доміно; удар — міняють напрям |
| Хуліган | enemy | більший за героя | іде до найближчих доміно, щоб збити; удар доміно — оглушений на кілька секунд, відштовхнути не можна |
| Бджола-вбивця | enemy | зʼявляється постійно | полює на героя; жало — втрата життя |
| Годинник, що ходить | enemy | невразливий | блукає полем (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `contact(domino_man, dot)` → ЯКЩО `not occupied(dot, domino)` → ТО `place(domino_man, domino)`.
- КОЛИ `input(button)` біля доміно → ТО `take(domino_man, domino)` — дірка в ланцюгу зупиняє падіння.
- КОЛИ `contact(pedestrian|bully, domino)` → ТО `fall(domino)`.
- КОЛИ `after(fall(domino))` → ЯКЩО `occupied(next_dot, domino)` → ТО `fall(next_domino)` — ланцюг; порожня крапка обриває.
- КОЛИ `input(button)` → ЯКЩО `in_range(domino_man, pedestrian, 1)` → ТО `custom: «відштовхнути / змінити напрям перехожого»`.
- КОЛИ `input(button)` → ЯКЩО `in_range(domino_man, bully, 1)` → ТО `stun(bully, n)` (штани спадають).
- КОЛИ `contact(bee, domino_man)` → ТО `lives(-1)`.
- КОЛИ `custom: «зачеплено крайнє ліве доміно»` → ТО `lives(-1)`.
- КОЛИ `all_on(domino, dot)` → ТО `choose(повалити | грати далі)`.
- КОЛИ `custom: «гравець валить ланцюг»` → ТО `score(bonus × n_fallen)`, `set_value(bonus, 100)`, `next_level`.
- КОЛИ `custom: «гравець чекає»` → ТО `custom: «бонус росте»`, `next_level` з недоваленим ланцюгом (кілька ланцюгів разом — великий бонус).
- КОЛИ `died(domino_man)` → ТО `set_value(bonus, 100)`.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`, `window(poem-rating)`.
- Перемога: окремого фіналу нема — екран за екраном. Поразка: жало бджоли або зачеплене крайнє ліве доміно; життя скінчились. Рахунок: бонус × кількість повалених доміно.

## Керування і ввід
- 8-напрямний джойстик — рух; одна кнопка — поставити/зняти доміно, замахнутись доміно на перехожого чи хулігана.
- До 2 гравців (?) по черзі.

## Вікна, меню, HUD
- `game-screen`: вулиця з крапками й доміно; `score`, `lives`, поточний бонус (?).
- `poem-rating` — після кінця гри вірш оцінює гравця.
- `attract-demo` (?).
- Переходи: гра → (ланцюг стоїть) вибір «повалити / чекати» → наступний екран → (життя скінчились) вірш.

## Фічі поза полем
- `operator-settings`: DIP-перемикачі, серед них колір шкіри героя (за результатами пошуку).
- Музика — «Maple Leaf Rag» Скотта Джопліна.

## Варіації й родичі
- Герой схожий на бармена з Tapper і лісоруба з Timber (Bally Midway).
- У корпусі: [Frogger](frogger.md) — заповнити всі «домівки»; [Hover Bovver](hover-bovver.md) — роботу псує стороння істота, поки ти працюєш.
- **Осі варіацій**: ланцюг — «падіння по сусіду / обривається порожнім»; завершення — «авто / вибір гравця з ризиком»; захисник — «відштовхує / оглушує / не діє (годинник)».

## Цікавинки для курсу
- Ланцюг падіння по сусідніх слотах і обрив на порожньому — 📎.
- Зняти доміно, щоб зупинити каскад, — рішення гравця під тиском часу — 📎.
- Вибір «забрати бонус / ризикнути далі» (push-your-luck) — 🌱.
- Різні реакції на удар: перехожий змінює напрям, хуліган оглушений, годинник невразливий — 🥉 як таблиця взаємодій.

## Мапа на каталог
- Є: `move-8dir` · `chain-reaction` ↔ падіння доміно · `random-walk` ↔ перехожі · `chase-player` ↔ бджола · `touch-death` + `player-death` · `event-points` · `keep-playing-after-win` ↔ «грати далі» з бонусом · `sequential-levels` · `game-screen` · `end-screen` · `background-music`.
- **Нема** → пропозиції карток:
  - `+fill-marked-spots` «Поставити обʼєкт на кожну позначку» · game-logic/win · 🌱.
  - `+remove-to-break-chain` «Прибрати ланку, щоб зупинити каскад» · entities/interact · 📎.
  - `+shove-wanderer` «Відштовхнути блукача ударом» · entities/interact · 🌱.
  - `+push-your-luck-bonus` «Бонус росте, поки ризикуєш» · game-logic/score · 🌱.
  - `+invincible-wanderer` «Невразливий блукач» · entities/move · 🌱 — годинник.

## Пропозиції до словників
- `+window:poem-rating` — підсумковий вірш-оцінка гравця.
- `+card:fill-marked-spots`, `+card:remove-to-break-chain`, `+card:shove-wanderer`, `+card:push-your-luck-bonus` — див. «Мапу на каталог».

## Джерела
- ⭐ [Wikipedia: Domino Man](https://en.wikipedia.org/wiki/Domino_Man) — ціль (доміно на кожну крапку), перехожі, бджола, хуліган (оглушити, не відштовхнути), невразливий годинник, зняти доміно, щоб зупинити каскад, вибір «повалити / грати далі», бонус × доміно зі скиданням до 100, вірш.
- [Arcade History #660](https://www.arcade-history.com/game/660/) — хуліган, бабця і хлопчик з візком, удар міняє напрям, 8-way + 1 кнопка, 2 гравці, MCR-II, грудень 1982.
- [Basement Arcade](https://basementarcade.com/Domino_Man.html) — рівень = виставити ланцюг і повалити; звуки «поставити/взяти доміно».
- YouTube: пошук «Domino Man arcade».

## Непевне
- (?) Рік: черга й EN-вікі — 1983, Arcade History — грудень 1982.
- (?) Що саме означає «зачеплено крайнє ліве доміно» — початок ланцюга, з якого гравець сам валить усе?
- (?) Як гравець валить ланцюг: штовхає перше доміно чи кнопкою; чи ланцюг при «чекати» переходить на наступний екран.
- (?) Як ставиться доміно: пробігти по крапці (Arcade History) чи кнопкою на крапці.
- (?) Поведінка годинника; стартова кількість життів; як зростає бонус.
- (?) 2 гравці — по черзі чи одночасно.
