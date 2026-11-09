---
title: Yoshi (Mario & Yoshi)
slug: yoshi-nes
aka: [ヨッシーのたまご, Yoshi no Tamago, Yoshi's Egg, Mario & Yoshi]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 1991
platforms: [Famicom, NES, Game Boy, Wii VC, 3DS, Wii U, Switch Online]
links:
  - {kind: fandom, url: "https://www.mariowiki.com/Yoshi_(game)", best: true, note: "Super Mario Wiki: 4 тарілки, збіг двох однакових, половинки шкаралупи, таблиця Йоші й очок, A/B-Type, 2P, налаштування, відмінності NES/GB"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Yoshi_(video_game)", note: "4 стовпці, обмін сусідніх стосів, нижня на нижню зникають, верхня без пари — без очок, B-Type очистити все, 2P до 3 перемог"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ヨッシーのたまご", note: "JA: 8 рядів FC / 7 GB, поразка на 9-му (8-му), стартові ряди B-Type, яйця шлють ворогів супернику"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Yoshi+NES+1991+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [gravity-fall, keyboard-controls, event-points, progress-acceleration, difficulty-levels, game-settings, music-toggle, sequential-levels, score-records, garbage-attack, simultaneous-versus, +swap-adjacent-stacks, +stack-top-match, +bracket-enclose-clear, +clear-all-goal, +prefilled-board, +timing-window]
proposes: ["+cond:enclosed", "+card:swap-adjacent-stacks", "+card:bracket-enclose-clear"]
author: opus
date: 2026-11-09
---

# Yoshi (NES/Game Boy) — міняй місцями стоси на чотирьох тарілках, щоб однакові вороги злипались, а половинки шкаралупи замикали їх у яйце

## Суть
Перша спільна гра Game Freak і Nintendo: на чотири тарілки падають вороги з Mario (Гумба, Блупер, Бу, Піранья) і половинки яйця. Гравець не керує тим, що падає, — Маріо внизу лише міняє місцями два сусідні стоси разом із тарілками. Ворог, що впав на такого самого, зникає разом із ним; верхня половинка шкаралупи, що впала на стос із нижньою, замикає всіх ворогів між ними — вилуплюється Йоші, тим більший, чим більше замкнено. Стос, вищий за межу, — кінець гри.

## Поле і час
- 4 стовпці-тарілки; висота 8 на FC/NES і 7 на Game Boy; поразка — коли елемент лягає на 9-й (8-й на GB) ряд (JA-вікі) / стос перетнув чорну лінію (EN-вікі).
- Real-time: вороги падають зверху у стовпці; A-Type — дедалі швидше; швидкість задається перед грою.
- Шари: стоси на тарілках + елементи, що падають + Маріо під полем між двома тарілками.
- Обмін зсуває весь стос разом із тарілкою; що відбувається з елементами в польоті — (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Маріо | player | позиція між двома сусідніми тарілками | ←/→ — до іншої пари тарілок; A або B — міняє місцями дві тарілки над собою |
| Тарілка (стовпець) ×4 | zone | ємність 8 (NES) / 7 (GB) | тримає стос; переповнення → Game Over |
| Гумба, Блупер, Бу, Піранья | tile | вид | падає на стос; той самий вид зверху стосу → обидва зникають (5 очок) |
| Нижня половина шкаралупи | tile | — | лежить, доки на неї не ляже такий самий елемент (зникають обидві) або верхня половина |
| Верхня половина шкаралупи | tile | — | падає на стос: проходить крізь ворогів до нижньої половини → яйце; без нижньої — розсіюється без очок |
| Йоші (результат) | object | Little / Yoshi / Winged / Star | очки 50 / 100 / 200 / 500 за кількістю замкнених: NES 0–1 / 2–4 / 5–6 / 7, GB 0 / 1–3 / 4–5 / 6 |
| Чорна лінія | static | верх поля | стос перетнув → Game Over |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(drop_rate)` → ТО `spawn_at(falling_item, column_top)` — вороги й половинки шкаралупи у випадкові стовпці.
- КОЛИ `tick` → ЯКЩО `free(cell_below)` → ТО `move(falling_item, down)`.
- КОЛИ `input(left|right)` → ТО `move(mario, dir)`.
- КОЛИ `input(a|b)` → ТО `swap(stack_left, stack_right)`.
- КОЛИ `input(down)` → ТО `speed(falling_item, ×k)` — прискорене падіння (JA).
- КОЛИ `contact(falling_item, stack_top)` → ЯКЩО `same(falling_item, stack_top, kind)` → ТО `disappear_both`, `score(5)`.
- КОЛИ `contact(top_shell, stack)` → ЯКЩО `custom: «у стосі є нижня половина»` → ТО `custom: «верхня проходить крізь стос до найвищої нижньої половини — усе між ними зникає»`, `spawn_at(yoshi, column)`, `score(50|100|200|500)`.
- КОЛИ `contact(top_shell, stack)` → ЯКЩО `custom: «у стосі нема нижньої половини»` → ТО `disappear_a` — без очок.
- КОЛИ `counter(stack_height, >, cap)` → ТО `lose` — cap 8 на NES, 7 на GB.
- КОЛИ `timer(level_period)` → ЯКЩО `mode(a_type)` → ТО `speed(falling_item, +1)`.
- КОЛИ `game_over` → ЯКЩО `counter(eggs, ≥, 10)` → ТО `custom: «бонус-раунд — 4 яйця вилуплюються по черзі; A у момент вилуплення дає кращого Йоші й очки»`.
- КОЛИ `counter(eggs, ≥, 100)` → ТО `animate(yoshi_dance)`, `message(super player)`.
- B-Type: КОЛИ `level_start` → ЯКЩО `mode(b_type)` → ТО `spawn_at(enemies, bottom_rows)` — стартовий стос росте з рівнем, до 6 рядів з рівня 6 (FC) / 5 з рівня 5 (GB).
- B-Type: КОЛИ `all_gone(enemy)` → ТО `win`, `next_level`, `score(bonus)` — бонус від 50 до 1500 за рівнем, записується й час.
- 2P: КОЛИ `custom: «вилупився Йоші із замкненими ворогами»` → ТО `send_garbage(enclosed_enemies)` — замкнені вороги падають супернику.
- 2P: КОЛИ `all_gone(enemy)` → ЯКЩО `mode(versus)` → ТО `win` раунду; суперник з переповненням — `lose`; 3 перемоги = матч.
- Перемога: A-Type — нема (на рекорд); B-Type — очищене поле; 2P — 3 виграні раунди. · Поразка: переповнена тарілка. · Рахунок: 5 за пару, 50–500 за Йоші, бонуси раундів.

## Керування і ввід
- Хрестовина ←/→ — Маріо переходить під іншу пару сусідніх тарілок.
- A або B — обміняти дві тарілки над Маріо (обидві кнопки роблять те саме); ↓ — прискорити падіння (JA).
- Бонус-раунд A-Type: натиснути A в момент вилуплення.
- 2P (NES): одне поле навпіл — Маріо ліворуч, Луїджі праворуч; GB — через Link Cable.

## Вікна, меню, HUD
- `splash-screen` — титул.
- `settings-window` перед грою: тип гри (A / B), складність (рівень), швидкість падіння, музика.
- `game-screen`: 4 тарілки, Маріо під ними; HUD — `score`, `hi-score` (дошка рекордів зі спрайтом Маріо), `custom: «egg-counter» — кількість вилуплених яєць`, `level-number` (B-Type), `timer-elapsed` (B-Type, ?).
- `custom-window` — бонус-раунд A-Type; між рівнями B-Type — сценка: Маріо на Йоші ковтає предмет.
- 2P: розділене поле, позначки O/X за раунди, виграні раунди — яйцями; GB — лічильник ворогів кожної сторони.
- `end-screen` — Game Over.
- Переходи: splash → settings → game-screen → (A: Game Over → бонус-раунд при ≥10 яєць) / (B: поле чисте → сценка → наступний рівень).

## Фічі поза полем
- `mode-classic` A-Type (нескінченно на рекорд) і B-Type (`levels-sequential` 1…28+, очистити поле; записуються очки й час).
- `custom-difficulty`: рівень + швидкість окремо; `music-toggle` з вибором треку.
- `mode-versus` / `local-multiplayer` до 3 перемог.
- Пасхалка: 100 яєць — танець Йоші й «super player».

## Варіації й родичі
- NES/Famicom і Game Boy (обидві — 14.12.1991 у Японії): GB — 7 рядів замість 8, пороги Йоші зсунуті на одного ворога, інші бонус-предмети, інший 2P-екран.
- Наступна головоломка з Йоші — Yoshi's Cookie (`yoshis-cookie`, зовсім інше ядро — зсув рядів).
- Родичі: Klax (`klax`, верх стосу як точка збігу), Dr. Mario (`dr-mario`, вертикальний збіг), Panel de Pon (`panel-de-pon`, обмін двох клітин курсором), Kirby's Star Stacker (`kirbys-star-stacker`, затискання між двома однаковими).
- **Осі варіацій**: що міняє гравець (падаючу фігуру / дві клітини / **цілі стоси**) · умова зникнення (лінія N / **пара зверху стосу** / **дужки, що замикають вміст**) · нагорода (очки / розмір Йоші за замкненими).

## Цікавинки для курсу
- Обмін двох сусідніх стосів як єдиний ввід (масиви-стеки, swap) — 🌱.
- Збіг лише з верхнім елементом стосу (стек: peek і pop) — 🌱.
- Верхня половина, що «прорізає» стос до найвищої нижньої, і розмір нагороди за кількістю замкнених — 📎.
- Real-time спавн у 4 стовпці з прискоренням + переповнення — 📎.
- 2P: замкнені вороги летять супернику — 🥉.
- AI, що обирає обмін за прогнозом наступних падінь — 🥈.

## Мапа на каталог
- Є: `gravity-fall` · `keyboard-controls` · `event-points` (5 / 50…500) · `progress-acceleration` (A-Type) · `difficulty-levels` · `game-settings` (тип, рівень, швидкість, музика) · `music-toggle` · `sequential-levels` (B-Type) · `score-records` · `garbage-attack` + `simultaneous-versus` (2P).
- **Нема** → пропозиції карток:
  - `+swap-adjacent-stacks` «Обмін двох сусідніх стосів» · entities/move · 🌱 · слот {columns: 4}.
  - `+stack-top-match` «Збіг лише з верхнім елементом стосу» · entities/interact · 🌱.
  - `+bracket-enclose-clear` «Пара дужок замикає вміст стосу» · entities/interact · 📎 · слот {reward_by_count}.
  - `+prefilled-board` «Стартовий стос росте з рівнем» · levels/generation · 🌱.
  - `+clear-all-goal` · `+timing-window` — теги вже є в корпусі.

## Пропозиції до словників
- `+cond:enclosed` — сутності замкнені між двома частинами (верхня й нижня шкаралупа; пропозиція вже є в корпусі — підтверджую).
- `+card:swap-adjacent-stacks`, `+card:bracket-enclose-clear` — див. «Мапу».

## Джерела
- ⭐ [Super Mario Wiki: Yoshi (game)](https://www.mariowiki.com/Yoshi_(game)) — 4 тарілки, ємність 8/7, пара однакових = 5 очок, правила половинок, таблиця Йоші, A/B-Type, бонус-раунд, бонуси рівнів, 2P, налаштування, відмінності NES/GB, дати.
- [Wikipedia: Yoshi (video game)](https://en.wikipedia.org/wiki/Yoshi_(video_game)) — обмін сусідніх стосів, нижня на нижню зникають, верхня без пари — без очок, B-Type очистити все, 2P до 3 перемог, Game Freak.
- [JA Wikipedia: ヨッシーのたまご](https://ja.wikipedia.org/wiki/ヨッシーのたまご) — 8/7 рядів, поразка на 9-му/8-му, прискорене падіння, стартові ряди B-Type, яйця шлють ворогів супернику.
- YouTube: пошук «Yoshi NES 1991 gameplay».

## Непевне
- (?) Скільки елементів падає одночасно і як обирається стовпець.
- (?) Чи переносить обмін тарілок елементи, що вже падають, — джерела кажуть лише про стоси.
- (?) Очки за Йоші: таблиця дає 50–500 за розміром, а текст Mario Wiki — «50 за кожного ворога в стосі»; узято таблицю.
- (?) Що буває, коли нижня половина падає на ворога (вважаю — лягає зверху, як звичайний елемент).
- (?) Інтервал прискорення A-Type, кількість рівнів складності й градації швидкості, наявність таймера на екрані B-Type.
