---
title: Cosmo Gang the Puzzle (Pac-Attack)
slug: cosmo-gang-the-puzzle
aka: [コスモギャング ザ パズル, Pac-Attack, Pac Attack]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 1992
platforms: [arcade, Super Famicom, SNES, Mega Drive, Game Gear, Game Boy, CD-i, iOS, i-mode]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pac-Attack", best: true, note: "Pac-Attack: ряди блоків, привидів їсть лише Pac-Man у бік погляду, шкала феї, Puzzle 100 рівнів з паролями, versus зі сміттям"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cosmo_Gang_the_Puzzle", note: "оригінал Namco: Jammers, синя куля зі стрілкою, зірка зі шкали, ряд із шести блоків, 2P з роботами Pipopapo-Tai"}
  - {kind: other, url: "https://gamesdb.launchbox-app.com/games/details/21052-pac-attack", note: "опис: Pac-Man розвертається біля блока/стіни, фея стирає ~6–7 рядів привидів, Puzzle — до 4 Pac-Man і кнопка напрямку"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pac-Attack+snes+gameplay", note: "пошук; геймплей Pac-Attack"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cosmo+Gang+the+Puzzle+gameplay", note: "пошук; аркадний оригінал"}
stage: v1
coverage: 55
mechanics: [gravity-fall, multi-cell-size, keyboard-controls, destroy-all-enemies, progress-acceleration, sequential-levels, level-password, garbage-attack, simultaneous-versus, mode-select, +line-clear, +chain-reaction, +eater-piece, +line-immune-tile, +meter-summon-piece, +clear-below-piece, +move-limit-puzzle]
proposes: ["+effect:eat", "+trigger:meter_full", "+card:eater-piece", "+card:meter-summon-piece"]
author: opus
date: 2026-11-09
---

# Cosmo Gang the Puzzle / Pac-Attack — блоки зникають рядом, а ворогів у стосі зʼїдає фігура-пожирач, що біжить у бік погляду

## Суть
Падаючі формації складаються з двох видів клітин: блоків, що зникають повним рядом, як у Tetris, і ворогів (Jammers у Cosmo Gang, привиди в Pac-Attack), яких ряд **не бере**. Ворогів прибирає лише особлива фігура-пожирач — синя куля зі стрілкою (Cosmo Gang) або Pac-Man: після приземлення вона котиться в бік погляду, їсть усіх ворогів на шляху й зникає, коли їсти більше нічого. Зʼїдене наповнює шкалу, а повна шкала скидає зірку/фею, що стирає всіх ворогів під собою. Тож гравець не лише складає ряди, а й «готує стіл» — розкладає ворогів так, щоб пожирач пройшов їх одним заходом.

## Поле і час
- Вертикальний колодязь; ряд блоків має доторкатися обох стінок (Pac-Attack); у Cosmo Gang — «повні ряди з шести» (EN-вікі), тобто ширина ~6 (?).
- Real-time: формації падають; з рівнем зростають швидкість і гравітація, змінюється, через скільки формацій приходить Pac-Man.
- Шари: блоки + вороги в стосі + активна формація + пожирач, що рухається вже після приземлення (живе своїм тіком).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Формація | player | кілька клітин: блоки і/або вороги | зсув, падіння, поворот (?); осіла — стає частиною стосу |
| Блок | tile | — | зникає в повному ряду від стінки до стінки |
| Привид / Jammer | enemy | — | у ряд не зчищується; зникає, лише коли його зʼїв пожирач або стерла фея |
| Pac-Man / синя куля | player | напрям (погляд / стрілка) | після приземлення рухається в бік погляду, їсть ворогів на шляху; розвертається біля блока чи стіни; без ворогів — зникає |
| Шкала феї / зірки | zone | наповнюється за зʼїдених | повна → згори падає фея (зірка) |
| Фея / зірка | object | — | стирає всіх ворогів під собою (~6–7 рядів, LaunchBox), блоки лишає — вони осідають |
| Pipopapo-Tai (2P Cosmo Gang) | enemy | — | білі роботи замість Jammers на полі другого гравця |
| Верх колодязя | static | — | стос дійшов → поразка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(piece, down)` з темпом рівня.
- КОЛИ `input(left|right)` → ЯКЩО `free(target)` → ТО `move(piece, dir)`.
- КОЛИ `pattern(row_full)` → ЯКЩО `custom: «у ряду лише блоки»` → ТО `clear(row)`, `score(n)`.
- КОЛИ `counter(pieces_since_eater, ≥, n)` → ТО `spawn_at(eater_piece, top)` (інтервал залежить від рівня).
- КОЛИ `locked(eater)` → ТО `custom: «eat — пожирач рушає в бік погляду»`.
- КОЛИ `tick` → ЯКЩО `occupied(cell_ahead, ghost)` → ТО `custom: «зʼїсти привида»`, `move(eater, dir)`, `counter(fairy_meter, +1)`.
- КОЛИ `blocked(eater)` → ТО `face(eater, opposite)` — розворот біля блока чи стіни.
- КОЛИ `blocked(eater)` → ЯКЩО `custom: «більше нема досяжних привидів»` → ТО `disappear(eater)`.
- КОЛИ `after(disappear)` → ТО `fall(unsupported)` — блоки над зʼїденими осідають.
- КОЛИ `settled` → ЯКЩО `chain(n)` → ТО `clear(row)`, `combo(+1)` — осідання після феї чи пожирача добирає нові ряди.
- КОЛИ `counter(fairy_meter, ≥, full)` → ТО `spawn_at(fairy, top)`.
- КОЛИ `locked(fairy)` → ТО `custom: «стерти всіх привидів під феєю»`, `fall(unsupported)`.
- КОЛИ `counter(level_progress, ≥, n)` → ТО `speed(piece, +1)`, `custom: «змінюється інтервал появи Pac-Man»`.
- КОЛИ `reach(stack, top)` → ТО `lose`.
- Puzzle: КОЛИ `input(button)` → ЯКЩО `mode(puzzle)` → ТО `face(eater, opposite)` — лише тут напрям пожирача обирає гравець.
- Puzzle: КОЛИ `all_gone(ghost)` → ТО `win`, `next_level`, `window(level-password)`.
- Puzzle: КОЛИ `counter(eaters_left, ==, 0)` → ЯКЩО `count(ghost, >, 0)` → ТО `lose`.
- Versus: КОЛИ `custom: «зчищено блоки або зʼїдено привидів»` → ТО `send_garbage(pieces)`; у Cosmo Gang — `send_garbage(jammers)` за перевагу у знищених Jammers.
- Versus: КОЛИ `reach(stack, top)` → ЯКЩО `mode(versus)` → ТО `lose` для цього гравця, `win` для суперника.
- Перемога: Puzzle — усі привиди зʼїдені в межах ліміту пожирачів; versus — суперник забив колодязь. · Поразка: стос дійшов до верху. · Рахунок: за ряди й зʼїдених привидів; у Normal — максимум очок до поразки.

## Керування і ввід
- Хрестовина ←/→ — зсув формації, ↓ — прискорення (?), кнопки — поворот формації (?).
- Normal / versus: напрям пожирача заданий наперед (стрілка на кулі / погляд Pac-Man; LaunchBox — випадково ліворуч чи праворуч), гравець обирає лише стовпець.
- Puzzle: кнопка розвертає Pac-Man перед приземленням.
- Versus: двоє гравців одночасно, кожен свій колодязь.

## Вікна, меню, HUD
- `splash-screen` — титул; `mode-select`: Normal · Versus (2P) · Puzzle.
- `game-screen`: колодязь; HUD — `score`, `level-number`, `custom: «fairy-meter» — шкала феї ліворуч` (Pac-Attack) або в центрі екрана (Cosmo Gang); `next-piece-preview` — (?).
- `level-password` — після кожного пазла видається пароль, щоб повернутися до нього.
- Versus: два колодязі поруч.
- `end-screen` / Game Over; аркада — `game-over-continue` (?).
- Переходи: splash → mode-select → game-screen → (поразка) end-screen; Puzzle: пазл → пароль → наступний пазл.

## Фічі поза полем
- Normal — нескінченний на очки зі зростанням рівня.
- Puzzle: `puzzle-bank` 100 рівнів, мета — зʼїсти всіх привидів мінімумом ходів / до 4 Pac-Man (у частині пазлів менше); паролі.
- `mode-versus` / `local-multiplayer` з атаками-сміттям.
- Порти Pac-Attack: SNES, Mega Drive, Game Gear, Game Boy, CD-i, iOS (2010); Cosmo Gang — аркада Namco NA-1 (1992), Super Famicom (1993), японські телефони.

## Варіації й родичі
- Cosmo Gang the Puzzle (Namco, аркада 1992, Super Famicom 1993) → Pac-Attack (1993): та сама гра з персонажами Pac-Man — Jammers → привиди, синя куля → Pac-Man, зірка → фея.
- Родичі: Tetris (`tetris`, ряд), Dr. Mario (`dr-mario`, вороги як ціль у полі), Wario's Woods (`warios-woods`, монстрів прибирає лише бомба-каталізатор), Pac-Man (`maze-arcade/pac-man`, джерело персонажів).
- **Осі варіацій**: хто прибирає ворогів (ряд — ніхто / пожирач / фея-зона) · напрям пожирача (заданий / випадковий / за вибором у Puzzle) · що дає шкала (фея під собою / зірка під собою) · сміття у versus (формації / Jammers / роботи).

## Цікавинки для курсу
- Два класи клітин: блок зникає рядом, ворог — ні (`row_full` лише з блоків) — 🌱.
- Пожирач як агент із власним тіком: іде в бік погляду, їсть, розвертається біля перешкоди, падає/зникає, коли їсти нічого — 🥉 (простий автомат станів поверх падаючого поля; треба виявити «застряг»).
- Шкала, що за N зʼїдених дає фігуру-зачистку «все під собою» — 🌱.
- Каскад: зʼїдені привиди → осідання → нові повні ряди — 📎.
- Puzzle-банк із лімітом пожирачів і паролями + розвʼязувач перебором стовпців і напрямків — 🥇.
- Versus зі сміттям за зчищене — 🥉.

## Мапа на каталог
- Є: `gravity-fall` · `multi-cell-size` (формації) · `keyboard-controls` · `destroy-all-enemies` (Puzzle: усі привиди) · `progress-acceleration` · `sequential-levels` (100 пазлів) · `level-password` · `garbage-attack` · `simultaneous-versus` · `mode-select`.
- **Нема** → пропозиції карток:
  - `+eater-piece` «Фігура-пожирач: після приземлення рухається й знищує ворогів на шляху» · entities/interact · 🥉 · слоти {dir: facing|random, turn_on_block: bool}.
  - `+line-immune-tile` «Клітина, яку не бере повний ряд» · entities/interact · 🌱.
  - `+meter-summon-piece` «Шкала знищених викликає спецфігуру» · game-logic/score · 🌱 · слот {meter}.
  - `+clear-below-piece` «Спецфігура стирає ворогів під собою» · entities/interact · 📎 · слот {depth}.
  - `+line-clear` · `+chain-reaction` · `+move-limit-puzzle` — теги вже є в корпусі.

## Пропозиції до словників
- `+effect:eat` — сутність зʼїдає ворога на своєму шляху й рухається далі (пропозиція вже є в корпусі — підтверджую).
- `+trigger:meter_full` — шкала наповнилась (фея/зірка; пропозиція вже є — підтверджую).
- `+card:eater-piece`, `+card:meter-summon-piece` — див. «Мапу».

## Джерела
- ⭐ [Wikipedia: Pac-Attack](https://en.wikipedia.org/wiki/Pac-Attack) — ряди блоків від стінки до стінки, привидів їсть лише Pac-Man у бік погляду, зникає без привидів, шкала феї, Puzzle 100 рівнів і паролі, сміття у 2P, порти.
- [Wikipedia: Cosmo Gang the Puzzle](https://en.wikipedia.org/wiki/Cosmo_Gang_the_Puzzle) — Jammers, синя куля зі стрілкою, зірка зі шкали, ряди з шести, 2P з роботами Pipopapo-Tai, платформи.
- [LaunchBox: Pac-Attack](https://gamesdb.launchbox-app.com/games/details/21052-pac-attack) — Pac-Man іде ліворуч/праворуч навмання й розвертається біля блока/стіни, фея стирає ~6–7 рядів привидів, Puzzle: до 4 Pac-Man і кнопка напрямку.
- YouTube: пошуки «Pac-Attack snes gameplay», «Cosmo Gang the Puzzle gameplay».

## Непевне
- (?) Ширина колодязя (Cosmo Gang «ряди з шести» — це ширина чи довжина ряду) і висота.
- (?) Склад і форма формацій (з пошукової видачі: «після трьох фігур, де бувають 1–2 блоки», і «нижні дві частини фігури» в умові поразки) — точно не перевірено.
- (?) Чи падає Pac-Man у порожнечу під собою під час руху й чи їсть привидів униз; чи привиди мають власну гравітацію.
- (?) Чи блокує привид у ряду його зчищення (вважаю, що так — ряд «лише з блоків»).
- (?) Чи стають привиди синіми, коли приземлюється Pac-Man (з пошукової видачі, сторінку не відкрив).
- (?) Очки за ряд, привида, ланцюг; наповнення шкали; поворот формацій і призначення кнопок.
