---
title: Chew Man Fu (Be Ball)
slug: chew-man-fu
aka: [Be Ball, ビーボール, Bī Bōru, Chew-Man-Fu]
family: push-slide
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 1990
platforms: [PC Engine / TurboGrafx-16, mobile (2007), Wii Virtual Console, Wii U Virtual Console, PC Engine Mini]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Chew_Man_Fu", best: true, note: "куля бʼє ворога й летить далі, штовхання й тягнення навіть за ріг, куля на плиті рухається далі, Kick-Ball для двох, паролі, редактор"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ビーボール", note: "4 кольори Holy Ball з властивостями, плити того ж кольору, 100 с на раунд → вороги-вогняні кулі, предмети, 5 веж × 10 раундів × 10 кіл, KICK BALL, EDIT MODE"}
  - {kind: other, url: "https://www.avclub.com/chew-man-fu-turbografx", note: "чотири кулі на кожному рівні, вороги вбиваються кулями й скоро повертаються, «розворот у три прийоми» в коридорах"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Chew+Man+Fu+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [push-object, pull-object, inertia-slide, all-on-targets, move-4dir, keyboard-controls, touch-death, player-death, respawn, timeout-punisher, time-bonus, event-points, item-pickup, temporary-modes, level-password, level-select, in-game-editor, editor-window, mode-select, extra-life-threshold, +pull-around-corner, +ball-stats-by-colour, +colour-matched-targets, +breakable-wall-hits, +bait-lure, +kickball-minigame, +mode-coop]
proposes: ["+effect:knockback", "+effect:lure", "+cond:colour_match", "+window:kickball-match", "+card:pull-around-corner", "+card:ball-stats-by-colour", "+card:colour-matched-targets", "+card:breakable-wall-hits", "+card:kickball-minigame"]
author: opus
date: 2026-11-09
---

# Chew Man Fu (Be Ball) — Sokoban у реальному часі: штовхай і тягни кольорові кулі на плити свого кольору, а кинутою кулею бий ворогів

## Суть
Одноекранний лабіринт з чотирма кольоровими кулями, чотирма плитами тих самих кольорів і ворогами, що бродять. Гравець (Rin-Rin, у 2P — і Ran-Ran) кулю **штовхає** перед собою, **тягне** за собою — навіть за ріг — і **кидає/копає**: куля котиться по коридору, бʼє ворогів і ламає стіни. Раунд пройдено, коли кожна куля лежить на плиті свого кольору. Незвичне: ті самі кулі — і вантаж Sokoban, і зброя, а колір кулі задає її силу, відскок і пробивну здатність.

## Поле і час
- Один екран-лабіринт на квадратній сітці; кулі завширшки з коридор, тож розвернутися з кулею можна лише через бічний прохід («розворот у три прийоми», AV Club).
- Шари: підлога (звичайна / плита кольору / прихована плита) + стіни (цілі / тріснуті) + кулі + вороги + предмети.
- Real-time: вороги рухаються безперервно, «без фіксованих патернів»; таймер раунду 100 с, після нього вороги стають вогняними кулями.
- Структура: 5 веж × 10 раундів = 50 раундів на коло; 10 кіл — 500 раундів (JA-вікі).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Rin-Rin / Ran-Ran | player | життя | рух 4 напрямки; штовхає, тягне, кидає кулю; дотик ворога — −1 життя |
| Червона Holy Ball | object | сила max | будь-якого ворога вбиває з одного удару |
| Синя Holy Ball | object | відскок max, сила min | після удару довго відскакує між стінами; найлегше носити й швидко кидати |
| Зелена Holy Ball | object | збалансована | середня сила, відскок і пробивність |
| Чорна Holy Ball | object | пробивність max | ламає будь-яку стіну за два удари |
| Holy Plate ×4 | zone | колір | ціль: куля того ж кольору; куля на плиті ще рухається |
| Прихована плита | zone | — | невидима, доки не взято Sutra |
| Стіна | static | ціла / тріснута | зупиняє кулю; удари кулі тріскають і ламають її |
| Звичайний ворог | enemy | HP за типом | бродить; дотик — смерть гравця; убитий скоро повертається |
| Їжак | enemy | — | котиться (JA-вікі) |
| Черепаха / броньована черепаха | enemy | більше HP | від удару ховається в панцир |
| Вороги «на кулях» | enemy | — | заморожують, піднімають кулі чи танцюють на них (JA-вікі) |
| Вогняна куля | enemy | — | на кого перетворюються всі вороги після 100 с |
| Відлюдник (仙人) | neutral | — | дає діаманти за гру |
| Діамант | pickup | — | 30 → тренувальна бонус-гра з життями; часом 5 → 1UP |
| Оберіг (お守り) | pickup | 1 удар | блокує один удар ворога |
| Color Change | pickup | тривалість | усі кулі на час однакового кольору й властивостей |
| Ki Blast / Ki Wave | pickup | лінія: гориз./верт./хрест / площа | нищить стіни й ворогів у напрямку / в області |
| Fire · Earthquake · Misfortune | pickup | — | убити всіх ворогів · пошкодити всі стіни · відновити тріснуті стіни |
| Ramen | pickup | тривалість | приманює ворогів до себе |
| Sutra | pickup | — | показує приховані плити |
| Фрукти | pickup | очки | лише рахунок |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)` (real-time).
- КОЛИ `contact(player, ball)` (рух у кулю) → ЯКЩО `free(cell_behind_ball)` → ТО `push`; інакше `block`.
- КОЛИ `input(pull)` → ЯКЩО `custom: «куля поруч позаду гравця»` → ТО `pull(ball)`; на повороті куля йде слідом за ріг (`custom: «тягнення за ріг»`).
- КОЛИ `input(kick)` → ЯКЩО `custom: «куля перед гравцем»` → ТО `slide(ball, facing_dir)`.
- КОЛИ `contact(ball, enemy)` → ЯКЩО `state(ball, moving)` → ТО `damage(enemy, power[colour])`; куля котиться далі в тому самому напрямку; гравця трохи відкидає назад (`custom: «віддача»`).
- КОЛИ `contact(ball, enemy)` → ЯКЩО `same(ball, red, colour)` → ТО `disappear_b` (з одного удару).
- КОЛИ `blocked(ball)` (стіна) → ЯКЩО `state(ball, moving)` → ТО `damage(wall, pierce[colour])`; стіна → тріснута → `set_cell(wall, floor)`; чорна — за 2 удари.
- КОЛИ `blocked(blue_ball)` → ЯКЩО `custom: «запас відскоків не вичерпано»` → ТО `bounce`.
- КОЛИ `enter(ball, plate)` → ЯКЩО `same(ball, plate, colour)` → ТО `set_state(plate, filled)`; куля лишається рухомою.
- КОЛИ `all_on(ball, plate)` (кожна на плиті свого кольору) → ТО `win`, `score(time_bonus + special_bonus)`, `next_level`.
- КОЛИ `contact(enemy, player)` → ЯКЩО `has(player, charm)` → ТО `take(player, charm)`; інакше `lives(-1)`, `restart` (?).
- КОЛИ `died(enemy)` → ТО `respawn(enemy, spawn_point)` за деякий час (AV Club: «return from the dead quickly»).
- КОЛИ `counter(time_left, ==, 0)` → ТО `transform(all_enemies, fireball)`; життя не знімається, але небезпека росте.
- КОЛИ `picked(player, color_change)` → ТО `set_state(all_balls, one_colour, dur)`.
- КОЛИ `picked(player, ki_blast)` → ТО `clear(line)` у напрямку стрілки (ворогів і стіни); `ki_wave` → `clear(area)`.
- КОЛИ `picked(player, fire)` → ТО `disappear(all_enemies)`; `earthquake` → `damage(all_walls, 1)`; `misfortune` → `set_cell(cracked_walls, wall)`.
- КОЛИ `picked(player, ramen)` → ТО `custom: «вороги йдуть до рамену»` на час.
- КОЛИ `picked(player, sutra)` → ТО `reveal(hidden_plates)`.
- КОЛИ `counter(diamonds, >=, 30)` → ТО `window(custom: «修業» тренувальна бонус-гра)` → `lives(+n)`; КОЛИ `counter(diamonds, ==, 5)` → ЯКЩО `prob(p)` → ТО `lives(+1)`.
- КОЛИ `counter(lives, <, 0)` → ТО `window(game-over-continue)`: «ハイ» → `level-select` з пройдених; «イイエ» → показ пароля.
- Перемога: усі 4 кулі на плитах свого кольору. · Поразка: дотик ворога без оберегу; життя скінчились → game over. · Рахунок: бонус за час + спецбонус за раунд, фрукти, діаманти.

## Керування і ввід
- D-pad — рух; кнопки — тягнути (утримання) і кинути/копнути кулю (?) — точна розкладка I/II не перевірена.
- Kick-Ball «водночас тренує керування» (Wikipedia) — та сама схема кнопок.
- 2P кооператив: другий геймпад (у NA-версії — потрібен TurboTap, AV Club).

## Вікна, меню, HUD
- `splash-screen` → `mode-select`: 1 Player · 2 Players (кооп) · KICK BALL · EDIT MODE.
- `level-password`: введення пароля для продовження 1P/2P; з Backup RAM — збереження автоматично.
- `game-screen`: лабіринт; HUD — таймер 100 с (`timer-countdown`), життя, очки, діаманти (?).
- `game-over-continue`: «ハイ / イイエ» → `level-select` (пройдені етапи) або показ пароля.
- `editor-window` (EDIT MODE): 1P / 2P гра, EDIT, BACKUP (у Backup RAM), CLEAR, END; ліміт — 4 кулі, 4 плити, 8 предметів, 4 вороги.
- `+window:kickball-match`: дві половини поля, синя куля в центрі, рахунок до 5 у грі, до 3 ігор з 5 у матчі.
- `custom-window`: бонус-гра «修業» за 30 діамантів; зустріч із відлюдником.
- `end-screen` раунду: бонус за час і спецбонус (?).

## Фічі поза полем
- `level-password` + `continue` з Backup RAM; `level-select` пройдених етапів після game over.
- `level-editor` (EDIT MODE) зі збереженням у Backup RAM — EN-вікі цитує критику «lacking the ability to save levels» (розбіжність).
- `mode-coop` (2P), `mode-versus` (KICK BALL), 10 кіл по 50 раундів як `levels-sequential` з поверненням.
- Нема undo; рестарт — через втрату життя.

## Варіації й родичі
- Осі варіацій:
  - **як переміщується вантаж**: лише штовхання (Sokoban) / штовхання + тягнення за ріг + кидок (Chew Man Fu) / кидок і повернення (Plotting);
  - **ціль**: будь-яка куля на будь-яку ціль / колір до кольору (Chew Man Fu, [atomix](atomix.md) — атом до місця);
  - **вантаж як зброя**: ні (Sokoban) / ковзний блок давить (Pengo, `crush-by-slide`) / кинута куля бʼє і летить далі;
  - **властивості вантажу**: однакові / за кольором (сила, відскок, пробивність).
- Родичі: [pengo](pengo.md), [adventures-of-lolo](adventures-of-lolo.md), [kye](kye.md), Bomberman (`+bomb-kick`), Kickle Cubicle.

## Цікавинки для курсу
- Штовхання + тягнення, у тому числі за ріг (куля йде шляхом гравця) — 📎.
- Кидок кулі: ковзання до упору з ударом ворога «на проліт» і віддачею гравцю — 🥉.
- Колір кулі = набір параметрів (сила, відскок, пробивність) — 🌱 як таблиця, 📎 з відскоком синьої.
- Стіни з HP (ціла → тріснута → підлога) і предмети, що лагодять/руйнують усі стіни — 📎.
- Плити того ж кольору як умова перемоги + прихована плита, що відкривається предметом — 🌱.
- 100 с, після яких вороги стають вогняними кулями (`timeout-punisher`) — 🌱.
- Редактор раунду з лімітами на кількість сутностей і збереженням — 🥈.
- Kick-Ball: футбол на тій самій фізиці кулі для двох — 🥉.

## Мапа на каталог
- Є: `push-object` + `pull-object` ↔ штовхання/тягнення; `inertia-slide` ↔ кинута куля; `all-on-targets` ↔ кулі на плитах; `move-4dir` + `keyboard-controls`; `touch-death` + `player-death` ↔ дотик ворога; `respawn` ↔ вороги повертаються; `timeout-punisher` ↔ вогняні кулі після 100 с; `time-bonus` + `event-points`; `item-pickup` + `temporary-modes` ↔ предмети, Color Change; `level-password` + `level-select`; `in-game-editor` + `editor-window`; `mode-select`; `extra-life-threshold` ↔ діаманти → життя.
- **Нема** → пропозиції карток:
  - `+pull-around-corner` «Тягнення за ріг» · entities/legality · 📎 — розвиток `pull-object`.
  - `+ball-stats-by-colour` «Параметри обʼєкта за кольором» · entities/state · 🌱 · слоти {power, bounce, pierce}.
  - `+colour-matched-targets` «Ціль приймає лише свій колір» · game-logic/win · 🌱 — дитина `all-on-targets`.
  - `+breakable-wall-hits` (вже пропонована) · слот {hits: 2}.
  - `+bait-lure` (Pâquerette) — рамен.
  - `+kickball-minigame` «Футбол-міні-гра на механіці гри» · game-logic/opponent · 🥉.
  - `+mode-coop` — 2P кооператив на одному полі.

## Пропозиції до словників
- `+effect:knockback` — віддача гравцю після удару кулі (×11 у пропозиціях).
- `+effect:lure` — рамен кличе ворогів.
- `+cond:colour_match` — колір обʼєкта збігається з ціллю (тут записано через `same(…, colour)`).
- `+window:kickball-match` — екран міні-матчу з рахунком.
- `+card:pull-around-corner`, `+card:ball-stats-by-colour`, `+card:colour-matched-targets`, `+card:breakable-wall-hits`, `+card:kickball-minigame` — див. вище.

## Джерела
- ⭐ [Wikipedia: Chew Man Fu](https://en.wikipedia.org/wiki/Chew_Man_Fu) — одноекранні рівні, куля бʼє ворога й рухається далі, гравця відкидає, push/pull «including around corners», куля на плиті рухома, Kick-Ball, паролі, редактор, порти й дати.
- [Wikipedia JA: ビーボール](https://ja.wikipedia.org/wiki/ビーボール) — Holy Ball/Holy Plate, 4 кольори й властивості, вороги, 100 с і вогняні кулі, предмети, діаманти, 5 веж × 10 × 10 кіл, режими, ліміти EDIT MODE, паролі й Backup RAM.
- [AV Club](https://www.avclub.com/chew-man-fu-turbografx) — чотири кулі на рівень, колір → сила/пробивність, «розворот у три прийоми», вороги повертаються, TurboTap для 2P.
- YouTube: пошук «Chew Man Fu gameplay».

## Непевне
- (?) Розкладка кнопок (тягнути / кинути) — ні EN-, ні JA-вікі її не дають; necretro.org (мануал) віддає Access Denied.
- (?) Що відбувається з ворогами, коли кулі на плитах: AV Club — «clears all enemies on the stage», JA-вікі — раунд пройдено; записано як перемогу раунду.
- (?) Чи редактор зберігає рівні: JA-вікі — так (BACKUP у Backup RAM), EN-вікі цитує огляд «lacking the ability to save levels».
- (?) EN-речення «continue moving in the same direction, intervening walls» обірване; що куля робить зі стінами — за JA-вікі (ламає).
- (?) Чи вороги рухаються випадково (`random: runtime`) — AV Club: «no fixed patterns», «may take different paths at corners».
- (?) Скільки життів на старті і чи після смерті раунд починається спочатку.
