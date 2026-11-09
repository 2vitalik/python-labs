---
title: Maze Craze
slug: maze-craze
aka: [Maze Craze: A Game of Cops 'n Robbers, Maze Mania]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: hidden
  random: both
  goal: race
year: 1978
platforms: [Atari 2600]
links:
  - {kind: other, url: "https://discmaster.textfiles.com/view/1886/1000gamemanuals.iso/Atari%202600/Maze%20Craze.txt", best: true, note: "текст мануалу: швидкості, 4 рівні видимості, усі варіації, перемикачі"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Maze_Craze", note: "огляд: випадковий лабіринт, копи, грабіжники, Blockade, невидимі лабіринти"}
  - {kind: other, url: "https://atari.com/pages/mazecraze", note: "офіційна сторінка: номери ігор і варіації"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=maze+craze+atari+2600+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [maze-generation, move-4dir, impassable-cells, reach-exit, touch-death, random-walk, hot-seat, rule-variants, game-settings, difficulty-levels, +race-to-exit, +invisible-walls, +peek-reveal, +fake-wall-placement, +wound-slowdown, +scout-guide, +numbered-variations]
proposes: ["+trigger:reach_first", "+effect:place_fake_wall", "+ui:robbers-bars", "+feature:visibility-levels", "+feature:numbered-variations", "+role:scout"]
author: opus
date: 2026-11-09
---

# Maze Craze — двоє копів наввипередки до виходу з випадкового лабіринту міських кварталів, де ховаються грабіжники і стіни зникають

## Суть
Двоє гравців одночасно ведуть копів (червоний і синій квадрат) з лівого краю лабіринту до виходу справа; хто вийде першим — переміг. Лабіринт генерується наново щогри. Варіації додають грабіжників, що бродять за рогами (дотик — вибув або паралізований), невидимі частини лабіринту з «підглядуванням», фальшиву стіну-обманку для суперника і розвідника, що показує шлях.

## Поле і час
- Один екран, лабіринт «міських кварталів» на прямокутній сітці; вхід ліворуч, вихід праворуч, обидва копи стартують з лівого боку.
- Новий випадковий лабіринт на кожну гру (Reset або кнопка після гри).
- Видимість (число вгорі праворуч): 1 — видно все; 2 — мала частина невидима; 3 — велика частина невидима; 4 — невидимо все. Коп, що вийшов, — показує лабіринт.
- Real-time; швидкість (число вгорі ліворуч): 1 — середня, 2 — швидка, 3 — повільна, 4 — «розважливо повільна».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Коп ×2 | player | швидкість (перемикач a/b) | рух 4 напрямки коридорами; a — як грабіжники, b — швидше |
| Стіна кварталу | static | видима / невидима | непрохідна |
| Вихід | static | праворуч | хто дійшов перший — переміг |
| Грабіжник | enemy | 2 / 3 / 5 на поле | блукає, «чатує за рогами»; дотик — коп вибуває або поранений |
| Фальшива стіна (Blockade) | static | одна на гравця | виглядає як тупик, але прохідна |
| Розвідник (Scout) | neutral | — | біжить попереду копа, випадково «показує дорогу» |
| Смужки грабіжників | mark | 3 | HUD у Capture: зникає по одній за спійманого |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(cop, dir)`; інакше `block` (стіна блокує і невидима).
- КОЛИ `reach(cop, exit)` → ЯКЩО `count(cop_out, ==, 0)` → ТО `win` (перший); `reveal(maze)` у невидимих іграх.
- КОЛИ `tick` → ТО грабіжник: `move(robber, rng_dir)` (`random-walk`) (?).
- КОЛИ `contact(cop, robber)` → ЯКЩО `mode(robbers)` → ТО `lose` — коп вибуває з гри.
- КОЛИ `contact(cop, robber)` → ЯКЩО `mode(wounds)` → ТО `custom: «коп паралізований на кілька миттєвостей, далі поступово набирає швидкість»` (`stun`); поки поранений — `custom: «їде прямо до наступного перехрестя»`.
- КОЛИ `contact(cop, robber)` → ЯКЩО `mode(capture)` → ТО `disappear_b`, `counter(captured, +1)`; КОЛИ `counter(captured, ==, 3)` → ТО `custom: «можна вигравати — вихід відкрито»` (?).
- КОЛИ `reach(cop, exit)` → ЯКЩО `mode(terror)` `and not state(opponent, knocked_out)` → ТО `block` — вийти можна лише після того, як суперника вибили грабіжники.
- КОЛИ `input(button)` → ЯКЩО `mode(blockade)` → ТО `custom: «поставити фальшиву стіну позаду копа; попередня зникає»` (`+effect:place_fake_wall`).
- КОЛИ `contact(cop, fake_wall)` → ТО `custom: «проходить крізь»`.
- КОЛИ `input(button)` → ЯКЩО `mode(player_peek)` → ТО `reveal(maze)` на мить, потім `hide(maze)`.
- КОЛИ `timer(few_seconds)` → ЯКЩО `mode(auto_peek)` → ТО `reveal(maze)` на мить.
- КОЛИ `tick` → ЯКЩО `mode(scouts)` → ТО `custom: «розвідник іде попереду копа випадковим маршрутом»`.
- Перемога: першим вийти справа (з умовами Capture/Terror). Поразка: суперник вийшов першим або тебе вибили грабіжники. Рахунку нема.

## Керування і ввід
- Джойстик — 4 напрямки; червона кнопка — Blockade або Player Peek (за варіацією), після гри — новий лабіринт.
- Консоль: Game Select перебирає комбінації «номер гри × швидкість × видимість»; Game Reset — старт, інший лабіринт тієї ж гри, або показати невидимий лабіринт перед виходом; Difficulty a/b — швидкість власного копа (лівий перемикач — лівий гравець).
- Обидва гравці грають одночасно на одному екрані.

## Вікна, меню, HUD
- `game-screen` — лабіринт; ліворуч угорі — швидкість, праворуч — видимість; номер гри.
- `mode-select` — без меню: Game Select змінює числа на екрані.
- HUD у Capture — кольорові смужки грабіжників, що лишились.
- Переходи: Select → Reset → гонка → (перший вийшов) лабіринт показано → кнопка/Reset → новий лабіринт.

## Фічі поза полем
- 16 ігор × 4 рівні видимості × 4 швидкості — пронумеровані варіації (`custom-rules`): Robbers 2/3/5, Wounds, Capture, Terror, Blockade, Auto Peek, Player Peek, Scouts; гра 16 — без варіацій.
- Гандикап: перемикач швидкості для кожного гравця окремо (`difficulty-presets`).
- Соло: варіації без взаємодії з другим копом можна грати самому (на час/на виживання).
- Новий лабіринт щогри — `seed`-генерації не видно, повтору нема.

## Варіації й родичі
- Pac-Man / Lock 'n' Chase (копи і грабіжники в лабіринті, але проти AI), Wizard of Wor (двоє в лабіринті), 3D Monster Maze (той самий страх за рогом), Amazing Maze (Midway 1976, аркадна гонка в згенерованому лабіринті) (?).
- Сучасні: генератори лабіринтів у навчальних задачах, Labyrinth (настолка) — інша ідея руху стін.
- **Осі варіацій:** видимість лабіринту (уся / частина / нічого + «підглядання» за кнопкою / за таймером) · дотик ворога (вибув / паралізований / спійманий) · умова виходу (будь-коли / після 3 спійманих / після вибуття суперника) · підлість проти суперника (фальшива стіна).

## Цікавинки для курсу
- Генерація ідеального лабіринту щогри (DFS / Прима) + гонка двох — 🥈 (генерація + коректний вихід).
- Невидимий лабіринт: стіни є, але не малюються; «підглядання» за кнопкою або періодично — 📎 (розділ логіка/рендер).
- Часткова видимість (мала / велика частина невидима) — 📎.
- Фальшива стіна-обманка, одна на гравця (нова замінює стару) — 🌱.
- Поранення: паралізований, потім розгін, і «їде до перехрестя» — 📎 (стан з розгоном).
- Terror: вихід закритий, доки суперника не вибили — 🌱 (умова перемоги через стан іншого гравця).
- Розвідник, що випадково біжить попереду — 📎.

## Мапа на каталог
- Є: `maze-generation` · `move-4dir` · `impassable-cells` · `reach-exit` · `touch-death` · `random-walk` (грабіжники (?)) · `hot-seat` (двоє за однією консоллю) · `rule-variants` · `game-settings` · `difficulty-levels` (швидкість, перемикач a/b).
- **Нема** → пропозиції карток:
  - `+race-to-exit` «Двоє наввипередки до виходу» · game-logic/win · 🌱.
  - `+invisible-walls` «Стіни є, але не видно» · interface/render · 📎 · слот {fraction}.
  - `+peek-reveal` «Підглянути мапу на мить» · interface/render · 🌱 · слот {trigger: button|timer}.
  - `+fake-wall-placement` «Поставити суперникові фальшиву стіну» · entities/interact · 🌱 · слот {max: 1}.
  - `+wound-slowdown` «Поранений стоїть, потім розганяється» · entities/state · 📎.
  - `+scout-guide` «NPC-розвідник показує шлях» · entities/move · 📎.
  - `+numbered-variations` «Номер гри = набір правил» · game-logic/constraints · 📎.

## Пропозиції до словників
- `+trigger:reach_first` — гравець досяг цілі першим (гонки: Maze Craze, Combat-подібні дуелі).
- `+effect:place_fake_wall` — гравець кладе прохідну «стіну» (Maze Craze Blockade).
- `+ui:robbers-bars` — смужки «скільки ще спіймати».
- `+feature:visibility-levels` — рівні видимості мапи як налаштування.
- `+feature:numbered-variations` — пронумеровані варіації (Atari 2600).
- `+role:scout` — NPC-провідник гравця.

## Джерела
- ⭐ [Текст мануалу Maze Craze](https://discmaster.textfiles.com/view/1886/1000gamemanuals.iso/Atari%202600/Maze%20Craze.txt) — мета, керування, перемикачі a/b, швидкості 1–4, видимості 1–4, Robbers / Wounds / Capture / Terror / Blockade / Peek / Scouts, 16 ігор.
- [Wikipedia: Maze Craze](https://en.wikipedia.org/wiki/Maze_Craze) — копи-квадрати, новий лабіринт щогри, соло-варіанти.
- [atari.com: Maze Craze](https://atari.com/pages/mazecraze) — у результатах пошуку: відповідність номерів ігор варіаціям (сторінку не відкривав).
- YouTube: пошук «maze craze atari 2600 gameplay».

## Непевне
- (?) Точна матриця «номер гри → варіації» (секція 6 мануалу в тексті розсипана); відомо: гра 6 вид. 1 — 5 Robbers, 2–4 — Player Peek; гра 7 вид. 1 — 5 Robbers + Terror, 2–4 — Scouts; гра 16 — без варіацій.
- (?) Рух грабіжників — «чатують за рогами»; випадкове блукання — моє припущення.
- (?) Що відбувається після 3 спійманих у Capture (перемога одразу чи право на вихід).
- (?) Алгоритм генерації лабіринту невідомий.
- (?) Amazing Maze як предок — з памʼяті.
