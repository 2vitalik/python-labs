---
title: Surround (Atari 2600)
slug: surround
aka: [Chase, Сураунд]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: survive
year: 1977
platforms: [Atari VCS / 2600]
links:
  - {kind: other, url: "https://atariage.com/manual_html_page.php?SoftwareLabelID=535", best: true, note: "мануал: 14 ігор, матриця опцій, 5 швидкостей, перемикачі складності, Video Graffiti"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Surround_(video_game)", note: "1977, Alan Miller, до 10 очок, 4 варіації, CPU, Video Graffiti"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Snake_(video_game_genre)", note: "один із 9 стартових тайтлів VCS у США; Sears продавав як Chase"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=surround+atari+2600+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-auto, move-4dir, move-8dir, touch-death, impassable-cells, wrap-edges, event-points, progress-acceleration, rule-variants, ai-opponent, difficulty-levels, no-reverse-turn, game-settings, +trail-wall, +trail-toggle, +shared-field-versus, +hardware-switch-settings, +drawing-sandbox]
proposes: ["+feature:hardware-switches", "+card:hardware-switch-settings", "+card:drawing-sandbox"]
author: opus
date: 2026-11-09
---

# Surround — Blockade на Atari 2600: 14 «ігор» як комбінації перемикачів правил, плюс режим малювання слідом

## Суть
Домашня версія Blockade: два блоки-«лідери» безупинно рухаються й лишають за собою стіну; хто врізався — дає очко суперникові, перший до 10 перемагає. Механіку `blockade` повторено; новим є те, як подано варіанти: 14 номерів гри — це таблиця увімкнених опцій (Speed Up, Diagonal, Erase, Wraparound) і кількості гравців, а перемикачі складності на консолі змінюють правило розвороту й силу CPU. Ігри 13–14 — не змагання, а «Video Graffiti»: слід стає пензлем.

## Поле і час
- Клітинне поле в рамці; слід — стіна до кінця розіграшу.
- Real-time; Speed Up — автоматичне прискорення, 5 швидкостей без контролю гравця.
- Wraparound — тор: вихід за край → поява з протилежного боку; тоді рамка не вбиває.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Блок-лідер гравця / CPU | player | напрям, швидкість | щотік крок; лишає слід |
| CPU-блок | enemy | amateur / pro | у 1P; обережний, уникає ризику |
| Слід | static | власник | стіна; Erase — не лишається, поки тиснеш кнопку |
| Рамка поля | static | — | дотик = очко суперникові (лише без Wraparound) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(leader, dir)`, `custom: «клітина позаду стає слідом»` (як у `blockade`).
- КОЛИ `input(dir)` → ЯКЩО `mode(diagonal) or custom: «напрям ортогональний»` → ТО `face(leader, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «перемикач складності B» and custom: «назад на свій слід»` → ТО `block` (розворот заборонено).
- КОЛИ `input(button)` → ЯКЩО `mode(erase)` → ТО `custom: «поки кнопку тримають, слід не лишається»`.
- КОЛИ `contact(leader, trail)` → ТО `score(+1)` суперникові, `custom: «новий розіграш»` (?).
- КОЛИ `edge(leader)` → ЯКЩО `mode(wraparound)` → ТО `wrap(leader)`; інакше `score(+1)` суперникові.
- КОЛИ `timer(interval)` → ЯКЩО `mode(speed_up)` → ТО `speed(leader, +1)` (до 5-ї швидкості).
- КОЛИ `counter(score, ==, 10)` → ТО `win`.
- Video Graffiti: КОЛИ `tick` → ЯКЩО `mode(graffiti)` → ТО `custom: «рух лише малює, зіткнень і очок нема»`.
- Перемога: першим 10 очок · Поразка: 10 очок у суперника · Рахунок: очко за аварію суперника.

## Керування і ввід
- Джойстик — напрям лідера; діагональ — лише в іграх з Diagonal Movement.
- Червона кнопка — Erase (тримати).
- Консоль: GAME SELECT — перебір 14 ігор; GAME RESET — старт/рестарт; TV TYPE — колір / ч-б.
- Перемикачі складності: B — не можна відступити на власний попередній блок сліду (для новачків); у 1P лівий перемикач — сила CPU (B amateur, A pro). У Video Graffiti складність не діє.

## Вікна, меню, HUD
- Окремих вікон нема: номер гри обирається на `game-screen` перемикачем SELECT.
- `game-screen`: поле, рахунок двох гравців угорі (?), номер гри (?).

## Фічі поза полем
- `rule-variants`: 14 ігор = комбінації опцій; у 2P опції комбінуються, у 1P — лише Speed Up (за Wikipedia).
- `+feature:hardware-switches` — правила й складність задаються фізичними перемикачами консолі.
- `ai-opponent-levels` — amateur / pro.
- `mode-sandbox` — Video Graffiti (2 режими: «Etch A Sketch» і з гумкою).

## Варіації й родичі
- `blockade` — аркадний оригінал (ліміт аварій від оператора); там уже перелічено 4 варіації Surround.
- `hustle` — аркадна гілка Gremlin з цілями і хвостом сталої довжини.
- `tron-light-cycles`, `achtung-die-kurve`, `snake` — нащадки.
- **Осі варіацій:** як у `blockade` + подача варіантів: номери ігор-комбінації / окремі перемикачі · заборона розвороту як налаштування складності.

## Цікавинки для курсу
- Номер гри = бітова маска опцій (матриця 14 × 4) — 🌱: один рушій, таблиця конфігурацій.
- Заборона розвороту як перемикач складності — 🌱.
- Erase-кнопка: тимчасово без сліду — 🌱.
- Режим-пісочниця на тому самому рушії (слід → малюнок) — 🌱.
- Обережний CPU «не помилятися» (flood fill найбільшої вільної області) — 🥉.

## Мапа на каталог
- Є: `move-auto` · `move-4dir` · `move-8dir` · `touch-death` · `impassable-cells` · `wrap-edges` · `event-points` · `progress-acceleration` · `rule-variants` · `ai-opponent` · `difficulty-levels` · `no-reverse-turn` · `game-settings`.
- **Нема** → пропозиції карток:
  - `+trail-wall`, `+trail-toggle`, `+shared-field-versus` — уже запропоновані в `blockade`; підтверджую.
  - `+hardware-switch-settings` «Налаштування фізичними перемикачами / номером гри» · interface/menus · 🌱.
  - `+drawing-sandbox` «Режим малювання на ігровому рушії» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+feature:hardware-switches` — налаштування правил і складності фізичними перемикачами консолі (Atari 2600).
- `+card:hardware-switch-settings`, `+card:drawing-sandbox` — див. «Мапу на каталог».

## Джерела
- ⭐ [AtariAge: мануал Surround](https://atariage.com/manual_html_page.php?SoftwareLabelID=535) — 14 ігор, матриця опцій, 5 швидкостей, перемикачі складності, рамка дає очко лише без Wraparound, до 10, Video Graffiti.
- [Wikipedia: Surround](https://en.wikipedia.org/wiki/Surround_(video_game)) — вересень 1977, Alan Miller, CPU, 4 варіації, у 1P лише Speed Up, Video Graffiti.
- [Wikipedia: Snake (video game genre)](https://en.wikipedia.org/wiki/Snake_(video_game_genre)) — стартовий тайтл VCS, Sears «Chase».

## Непевне
- (?) Точна матриця 14 ігор: у текстовій версії мануала стовпці зсунуті; у таблиці гра 3 — «3 гравці», що суперечить тексту.
- (?) Перемикач A дозволяє розворот на власний слід (тобто самогубство) — випливає з опису B.
- (?) Чи очищається поле після кожного очка; що буває при лобовому зіткненні.
- (?) Розміщення рахунку й номера гри на екрані.
