---
title: BarrelBots
slug: barrelbots
aka: [Barrelbots, Barrel Bots]
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: 3d
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3851470/BarrelBots/", best: true, note: "FidgetBear Games, 28.05.2026; «small robots that can grab, stack, and carry barrels of nuclear waste», «multilayered grid-based»; нотатки доступності; Gameplay Trailer ≈53 с, три кліпи, 9 скріншотів, 18 досягнень"}
  - {kind: official, url: "https://www.fidgetbeargames.com", note: "сайт студії: опис, дата виходу, трейлер-анонс, прескіт"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=5TA4uUg5VpY", note: "Announcement Trailer (посилання з сайту студії)"}
  - {kind: other, url: "https://www.jestr.gg/games/barrelbots", note: "картка для стрімерів: той самий опис і нотатки доступності"}
stage: v1
coverage: 35
mechanics: [move-4dir, keyboard-controls, gravity-fall, height-levels, carrier-platform, undo-redo, undo-unlimited, restart-level, sequential-levels, game-settings, volume-control, +grab-and-carry, +carry-stack, +piece-stacking, +elevator-cell, +deliver-goal, +hub-world, +activate-ally, +nonlinear-progress]
proposes: ["+effect:grab", "+effect:drop", "+effect:stack_on", "+effect:lift", "+trigger:delivered", "+feature:accessibility-notes", "+card:side-claw-carry", "+card:disposal-goal", "+card:activate-ally"]
author: opus
date: 2026-11-19
---

# BarrelBots — маленькі роботи хапають клешнею високі бочки з ядерними відходами, складають їх стосами й везуть до утилізатора на багатоповерховій сітці

## Суть
Покрокова 3D-головоломка на клітинах із кількома поверхами. Гравець веде маленького синього робота з клешнею збоку: той хапає жовту бочку з відходами (вдвічі вищу за себе), несе її, ставить на іншу бочку чи на робота й зрештою опускає в контейнер-утилізатор. На рівнях бувають кілька роботів, ліфти, уступи й ями; правила прості, але кожен рівень має «aha»-взаємодію. Усе подано як доступну гру: undo й рестарт без ліміту, без таймінгу, кольору й лімітів ходів.

## Поле і час
- Квадратна сітка з кількома висотами («multilayered grid-based»): поверхи з блоків, уступи, сітчасті настили, ями; вигляд — 3D-камера під кутом.
- Бочка займає дві клітини по висоті, робот — одну (трейлери, скріншоти) (?).
- Хід = крок чи дія активного робота; без вводу нічого не рухається (без таймінгу — «Playable without Timed Input»).
- Між рівнями — 3D-хаб: коридор із капсулами-входами з номерами «4-4», «4-5», «4-6», «4-7», над пройденими — табличка «DONE»; у рівень заходять самим роботом (патч 02.06: зайти в рівень із бочкою в клешні ламало рівень).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робот (активний, синій з обвідкою) | player | клешня з одного боку | ходить клітинами; хапає бочку збоку, несе й ставить; може бути підставкою для бочки |
| Інші роботи (темні / фіолетові) | ally | вимкнений / звʼязаний (?) | вмикаються дотиком (іскри в трейлері, досягнення «Find A Friend») (?) |
| Бочка з відходами (жовта) | object | висота 2 | її хапають, несуть, ставлять стосом; мета — утилізатор |
| Темна низька бочка | object | висота 1 (?) | стоїть як підставка або перешкода (?) |
| Контейнер-утилізатор | container | вікно, підсвітка | приймає бочку; підсвічується, коли заповнений (?) |
| Ліфт (смугастий жовто-чорний диск) | platform | — | піднімає те, що на ньому, на поверх угору (патч 02.06) |
| Блоки, стіни, огорожі | static | висота | поверхи й перешкоди |
| Сітчастий настил | terrain | — | підлога, крізь яку видно нижчий поверх (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(robot, dir)`; бочка в клешні рухається разом із роботом.
- КОЛИ `input(grab)` → ЯКЩО `occupied(cell_ahead, barrel)` → ТО `attach(robot, barrel)` — клешня тримає бочку збоку (трейлери) (?).
- КОЛИ `input(grab)` → ЯКЩО `custom: «робот тримає бочку»` → ТО `detach(robot, barrel)` — бочку поставлено на клітину перед роботом чи на верх стосу (?).
- КОЛИ `custom: «бочку поставлено на робота або іншу бочку»` → ТО `custom: «лягає зверху й утворює стос»` — опис Steam «stack», досягнення «Stack My Bits Up», трейлер: бочка на голові робота.
- КОЛИ `turn_end` → ЯКЩО `not supported(barrel)` → ТО `fall(barrel)` — бочки й роботи без опори падають на нижчий поверх (?).
- КОЛИ `enter(robot, lift)` → ТО `custom: «ліфт піднімає робота з усім стосом на поверх угору»` — патч 02.06: стос на роботі на ліфті «shoot up through ceilings» (виправлено).
- КОЛИ `contact(barrel, disposal)` → ТО `disappear`, `custom: «бочку утилізовано»` (трейлер: бочка опускається в контейнер, той світиться) (?).
- КОЛИ `custom: «усі бочки утилізовано»` → ТО `win`, `next_level` (?).
- КОЛИ `contact(robot, sleeping_robot)` → ТО `custom: «вмикає сусіда — ще один робот під керуванням»` (досягнення «Find A Friend», «A Connection Is Made») (?).
- КОЛИ `input(undo)` → ТО `undo(1)` — без ліміту («Unlimited undos and resets»).
- КОЛИ `input(reset)` → ТО `restart`.
- Перемога: бочки в утилізаторі (?). · Поразка: нема — ні лімітів ходів, ні часу. · Рахунок: нема; 18 досягнень.

## Керування і ввід
- Клавіатура («Keyboard Only Option») або геймпад (повна підтримка, вібрація); рух, хапання / відпускання, undo, рестарт; розкладку — (?).
- Кілька роботів: як перемикати активного і чи рухаються звʼязані роботи разом — (?).
- Під час undo на екрані зʼявляється значок «<<» (трейлер).

## Вікна, меню, HUD
- Хаб (`custom-window`): 3D-коридор із капсулами рівнів «N-M» і табличками «DONE».
- `game-screen`: 3D-рівень; на старті — назва рівня (патч 29.05: «Level names not disappearing»); значок «<<» під час undo.
- `settings-window`: окрема гучність, альтернативні кольори, комфорт камери, вібрація («Rumble») (?).
- `achievements-window` — 18 досягнень Steam (World 1–3 Done, Moving Up!, The Test Suite, To The End…).
- Переходи: хаб → капсула → рівень → назад у хаб, над капсулою «DONE».

## Фічі поза полем
- `undo` без ліміту + `restart-level`; `autosave` («Save Anytime»), Steam Cloud.
- Доступність як фіча: без пазлів на звук, таймінг і колір («Color Alternatives»), без лімітів часу й ходів, комфорт камери, окрема гучність.
- Нелінійна прогресія: щоб іти далі, не треба розвʼязати всі пазли; щонайменше 4 світи (досягнення World 1–3 Done, рівні «4-x» у трейлері).
- Демо на Steam Next Fest 2026 (трейлер-анонс); теги гравців «Level Editor», «Moddable» — чи є редактор — (?).

## Варіації й родичі
- [bonfire-peaks](../thinky/bonfire-peaks.md) — тримати ящики стосом і будувати з них сходи; [qbillion](qbillion.md) — стоси й висоти.
- [stackrobats](../grid-platformer/stackrobats.md) — дотик лідера вмикає напарника; [sokobot](../program-robots/sokobot.md) — роботи хапають і носять блоки за програмою.
- [pipe-push-paradise](pipe-push-paradise.md) — стекування в 3D-Sokoban; [kwirk](kwirk.md) — кілька персонажів на рівні.
- Осі варіацій:
  - **як переміщують вантаж**: штовхання (Sokoban) / над головою стосом (Bonfire Peaks) / клешнею збоку (тут);
  - **висота**: пласка сітка / уступи / поверхи з ліфтами (тут);
  - **мета**: ящики на цілях / вантаж в утилізатор (тут);
  - **кілька аватарів**: перемикання / вмикання дотиком / звʼязка через спільний вантаж (тут, ?).

## Цікавинки для курсу
- Клешня збоку: звʼязка «робот + бочка» рухається як одне тіло з перевіркою вільності для обох — 🥉.
- Стоси з бочок і роботів у 3D-сітці з гравітацією — 🥈.
- Ліфт, що піднімає цілий стос, і баг «крізь стелю» як урок перевірки колізій — 🥉.
- Хаб із капсулами рівнів і позначкою «DONE» — 📎.
- Undo й рестарт без ліміту на стеку станів — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `gravity-fall` ↔ падіння без опори (?); `height-levels` ↔ поверхи; `carrier-platform` ↔ ліфт везе стос; `undo-redo` + `undo-unlimited` + `restart-level`; `sequential-levels`; `game-settings` + `volume-control` ↔ налаштування доступності.
- **Нема** → пропозиції карток:
  - `+side-claw-carry` «Хапання вантажу клешнею збоку: аватар і вантаж рухаються разом» · entities/interact · 🥉 (родич `+grab-and-carry`).
  - `+disposal-goal` «Мета — доставити всі обʼєкти в контейнер-утилізатор» · game-logic/win · 🌱 (родич `+deliver-goal`).
  - `+activate-ally` «Дотик вмикає сплячого напарника» · entities/interact · 📎 (?).
  - `+nonlinear-progress` «Іти далі можна, не розвʼязавши всіх пазлів» · levels/progression · 🌱.
  - `+grab-and-carry`, `+carry-stack`, `+piece-stacking`, `+elevator-cell`, `+hub-world` — підтверджую наявні нові теги.

## Пропозиції до словників
- `+effect:grab` / `+effect:drop` — схопити / поставити вантаж (уже пропоновані); зараз — `attach` / `detach`.
- `+effect:stack_on` — поставити обʼєкт на інший; `+effect:lift` — підняти на поверх (ліфт).
- `+trigger:delivered` — вантаж потрапив у контейнер-ціль.
- `+feature:accessibility-notes` — перелік доступності на сторінці гри (без таймінгу, кольору, лімітів).
- `+card:side-claw-carry`, `+card:disposal-goal`, `+card:activate-ally`.

## Джерела
- ⭐ [Steam: BarrelBots](https://store.steampowered.com/app/3851470/BarrelBots/) — опис («grab, stack, and carry barrels», «multilayered grid»), нотатки доступності, категорії (Keyboard Only, Color Alternatives, Camera Comfort, Save Anytime), 18 досягнень, Gameplay Trailer ≈53 с, Announcement Trailer ≈34 с, три кліпи; новини: «BarrelBots is Released!», фікси 29.05 і 02.06 (стоси на гравці, ліфт крізь стелю, вхід у рівень із бочкою, назви рівнів, вібрація).
- [FidgetBear Games](https://www.fidgetbeargames.com) — опис, дата, трейлер, прескіт.
- [YouTube: Announcement Trailer](https://www.youtube.com/watch?v=5TA4uUg5VpY).
- [Jestr](https://www.jestr.gg/games/barrelbots) — той самий опис.

## Непевне
- (?) Точна умова перемоги: усі бочки в утилізаторі, чи ще й робот у капсулі (кліп: після бочки в контейнер заходить і робот).
- (?) Як хапати: окрема кнопка чи хід у бочку; чи можна штовхати бочки; чи несе робот бочку збоку, піднятою, чи кладе собі на голову.
- (?) Кілька роботів: перемикання, вмикання дотиком, спільний рух звʼязаних через одну бочку (трейлер: кілька роботів тримають одну бочку з різних боків).
- (?) Що таке темні низькі циліндри (вимкнені роботи чи короткі бочки) і сітчасті настили.
- (?) Кількість рівнів і світів, наявність редактора (теги гравців «Level Editor», «Moddable»).
