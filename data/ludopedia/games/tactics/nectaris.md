---
title: Nectaris (Military Madness)
slug: nectaris
aka: [Military Madness, Neo Nectaris, Military Madness 2, "Military Madness: Nectaris", Nectaris GB]
family: tactics
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 1989
platforms: [PC Engine / TurboGrafx-16, PC-98, X68000, MS-DOS, Windows, Game Boy, PlayStation, WiiWare, Xbox 360, PS3, iPhone]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Nectaris", best: true, note: "серія: гекси, sci-fi, Hudson Soft; список версій і ремейків"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Military_Madness", note: "перша гра: 16+16 карт, паролі, ZOC оточенням, бонус сусідів, захоплення юнітів у фабриках, табір полонених"}
  - {kind: other, url: "https://nectaris.tg-16.com/strategy_guide.html", note: "Base Nectaris: ZOC (6 гексів), Supporting Effect, Surrounding Effect (протилежні гекси ділять захист навпіл)"}
  - {kind: other, url: "https://nectaris.tg-16.com/how-to-play-tutorial.html", note: "Base Nectaris: порядок ходу, пряма/непряма атака, фабрики, досвід 1–8 зірок, ліміт 50 ходів, піхота захоплює"}
  - {kind: other, url: "https://nectaris.tg-16.com/nectaris-military_madness-FAQ-playstation-play.html", note: "Base Nectaris FAQ (PlayStation): юніти, вивантаження, фабрики, перемога/поразка"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Military+Madness+TurboGrafx+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [piece-move-patterns, legal-move-highlight, melee-vs-ranged, hp-damage, unit-xp-skills, inventory-limit, destroy-all-enemies, ai-opponent, hot-seat, level-password, sequential-levels, level-unlock, turn-enforcement, tutorial-window, +zone-of-control, +support-adjacent, +surround-penalty, +terrain-bonus, +terrain-move-cost, +capture-property, +factory-stock, +transport-load, +turn-limit]
proposes: ["+trigger:enter_zone", "+cond:zoc", "+cond:surrounded", "+effect:capture", "+effect:load", "+effect:unload", "+effect:store", "+effect:counterattack", "+role:property", "+ui:terrain-percent", "+ui:battle-forecast", "+window:command-box", "+window:battle-scene"]
author: opus
date: 2026-11-09
---

# Nectaris (Military Madness) — гексова війна на Місяці: зони контролю, підтримка сусідів і оточення

## Суть
Дві армії на гексовій карті Місяця ходять по черзі всіма юнітами. Головні ідеї — **позиційні**: кожен юніт тримає зону контролю з 6 сусідніх гексів, у яку ворог може зайти лише на один крок; сусідні свої юніти підсилюють атаку й захист; ворог між двома твоїми юнітами на протилежних гексах втрачає половину захисту. Нових юнітів не виробляють — їх **захоплюють** разом із фабриками, де вони стоять на складі. Перемога — знищити всіх або зайняти піхотою табір полонених ворога.

## Поле і час
- Гексова карта; ландшафт (дорога, рівнина, гори, кратери/долини, фабрики, табори) змінює рух, атаку й захист наземних юнітів; авіація ландшафт ігнорує.
- Хід = хід сторони: рухаєш і атакуєш кожним юнітом раз, потім End.
- 16 базових карт кампанії + 16 складніших після проходження; ліміт 50 ходів на карту (за FAQ).
- Інформація повна, туману нема (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Піхота (GX-78 Charlie, GX-88 Kilroy, CBX-1 Panther) | piece | рух, атака/захист, зірки досвіду | бʼє, захоплює фабрики й табори |
| CX-97 Teknik (Neo Nectaris) | piece | — | піхота-ремонтник: сусіднім юнітам +2 «одиниці» за хід, до 6 сусідів |
| Танки / бронетехніка | piece | рух, пряма атака | пряма атака по сусідньому гексу (?) |
| Артилерія / ракети | piece | непряма атака, дальність | бʼє не сусідні гекси; рух + стрільба в одному ході — ні (?) |
| ППО і авіація | piece | — | авіація ігнорує ландшафт; ППО бʼє повітря (?) |
| C-61 Pelican | piece | літак-транспорт | везе піхоту |
| NC-2 Mule | piece | наземний транспорт | везе юніти; завантажити й вивантажити того ж ходу не можна |
| SS-80 Atlus | piece | нерухомий | важка стаціонарна гармата (?) |
| HMB-4 Giant | piece | дуже повільний | повільний важкий юніт |
| Фабрика (нейтральна / ворожа / своя) | spawner | склад юнітів | захоплена → юніти на складі твої; ремонт юнітів у ній |
| Табір полонених | static | — | зайнятий ворожою піхотою → поразка власника |
| Дорога / рівнина | terrain | 0 % / 5 % | дешевий рух; вивантаження лише сюди або на фабрику |
| Гори, нерівний ґрунт, кратери | terrain | + захист | дорогий/неможливий рух для техніки |
| Зона контролю (6 сусідніх гексів) | zone | — | ворог, що увійшов, зупиняється |

## Правила (КОЛИ → ЯКЩО → ТО)
- Порядок ходу: рух → атака → відправити/забрати юніт із фабрики → захоплення → End; КОЛИ `input(end)` → ТО `end_turn`.
- КОЛИ `input(move, unit, hex)` → ЯКЩО `custom: «шлях за ціною ландшафту ≤ рух юніта»` → ТО `move`.
- ZOC: КОЛИ `enter(unit, enemy_zoc)` → ТО `custom: «рух зупиняється на першому гексі зони»`; крізь ворожу зону за хід пройти не можна.
- КОЛИ `custom: «юніт оточений кільцем ворожих юнітів»` → ТО `custom: «атака і захист падають; рухатись може лише на 1 гекс»`.
- Пряма атака: КОЛИ `input(attack, a, t)` → ЯКЩО `adjacent(a, t)` → ТО `damage(t, n)`; захисник, що вижив, відповідає (?).
- Непряма атака: КОЛИ `input(attack, a, t)` → ЯКЩО `in_range(a, t, range)` і not `adjacent(a, t)` → ТО `damage(t, n)`; мало хто вміє обидві.
- Шкода: `custom: «атака vs захист з урахуванням ландшафту, досвіду, підтримки й оточення; кількість «одиниць» у загоні зменшується»` + випадковість (?).
- Підтримка: ЯКЩО `adjacent_count(target, attacker_allies, ≥, 1)` → ТО `custom: «атака нападника росте з кожним його союзником поруч із ціллю»`; навпаки, `adjacent_count(attacker, defender_allies, ≥, 1)` → `custom: «захист цілі росте»`.
- Оточення: ЯКЩО `custom: «два нападники на протилежних гексах цілі (1–4, 2–5, 3–6)»` → ТО `custom: «захист цілі ділиться навпіл»`; повне кільце з 6 — максимум.
- Досвід: КОЛИ `custom: «юніт бився»` → ТО `counter(stars, +1)` до 8; ЯКЩО `counter(stars, ==, 8)` → ТО `custom: «найбільший бонус»`.
- Фабрика: КОЛИ `input(capture, factory)` → ЯКЩО `custom: «юніт — піхота»` → ТО `set_side(factory, side)`, `custom: «юніти зі складу фабрики — твої»`.
- КОЛИ `input(store, unit, own_factory)` → ТО `custom: «юніт заходить у фабрику, ремонтується; виходить лише наступного ходу»`; відправити й забрати за один хід не можна.
- КОЛИ `input(deploy, factory)` → ТО `spawn_at(unit, adjacent road|plain|transport)`.
- Транспорт: КОЛИ `input(load, unit, transport)` → ТО `custom: «load»`; КОЛИ `input(unload, cell)` → ЯКЩО `cell(cell, road|plain|factory)` → ТО `custom: «unload»`; не в тому ж ході, що завантаження.
- Teknik: КОЛИ `turn_start(side)` → ТО `heal(adjacent_allies, 2)` (до 6 сусідів).
- КОЛИ `all_gone(enemy)` → ТО `win`; КОЛИ `custom: «піхота зайняла ворожий табір полонених»` → ТО `win`.
- КОЛИ `custom: «ворог зайняв твій табір»` → ТО `lose`; КОЛИ `counter(turn, >, 50)` → ТО `lose`.
- Перемога: знищити всіх / зайняти табір · Поразка: втрата табору / ліміт ходів · Рахунок: —.

## Керування і ввід
- Курсор по гексах (D-pad), кнопка I — вибрати/підтвердити, II — скасувати.
- I на порожньому — COMMAND BOX: Shift (рух) · … · End Turn; вибраний юніт показує зону руху, далі ціль атаки.
- Бій — окрема анімаційна сцена з цифрами юнітів у загоні.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: 1P (кампанія) · 2P (versus) · Manual (навчання) · Password.
- `level-password` — ввід пароля карти; `tutorial-window` «Manual».
- `game-screen`: гексова карта, курсор; панель юніта (назва, кількість, зірки досвіду); панель ландшафту з відсотком; `turn-counter`; `turn-indicator`.
- `custom-window` «Command box» — меню команд ходу.
- `custom-window` «Battle scene» — анімація обміну ударами з атакою/захистом.
- `end-screen` — карта пройдена + пароль наступної.
- Переходи: main-menu → (Password) → карта → бій → end-screen → наступна карта.

## Фічі поза полем
- `levels-sequential` 16 карт + `level-unlock` 16 advanced; збереження — `level-password`.
- `hotseat` 2P versus; `tutorial` «Manual».
- Ремейк 2009 (WiiWare/XBLA/PSN): нова графіка, онлайн-гра (?).

## Варіації й родичі
- Серія: Nectaris (1989), Neo Nectaris / Military Madness 2 (1994, Teknik), версії PC і консолей, Nectaris GB (1998), Military Madness: Nectaris (2009), Neo Nectaris (iPhone, 2010).
- Родичі: [advance-wars](advance-wars.md) (без ZOC, економіка будівель), [battle-for-wesnoth](battle-for-wesnoth.md) (ZOC на гексах), [polytopia](polytopia.md); Battle Isle, Panzer General (гекси, ZOC).
- **Осі варіацій**: ZOC — нема / зупинка на вході / заборона виходу · підтримка — нема / +за сусідів цілі / лідерство · поповнення — виробництво / захоплення складів / підкріплення · оточення — нема / протилежні гекси / повне кільце.

## Цікавинки для курсу
- Зона контролю: рух зупиняється на першому гексі зони — модифікація BFS по гексах — 📎.
- Підтримка від сусідів і ефект оточення протилежними гексами — 📎 (сусідство на гекс-сітці, пари протилежних напрямків).
- Фабрики як склади юнітів, що змінюють власника, ремонт усередині — 🌱.
- Транспорт з обмеженнями «не завантажити й вивантажити за хід» — 🌱.
- Досвід зірками 1–8 з ростом бонусу — 🌱.
- Ліміт 50 ходів як поразка — 🌱.

## Мапа на каталог
- Є: `piece-move-patterns` · `legal-move-highlight` · `melee-vs-ranged` (пряма/непряма) · `hp-damage` (кількість у загоні) · `unit-xp-skills` (зірки) · `inventory-limit` (місткість транспорту) · `destroy-all-enemies` · `ai-opponent` · `hot-seat` · `level-password` · `sequential-levels` + `level-unlock` · `turn-enforcement` · `tutorial-window`.
- **Нема** → пропозиції карток:
  - `+zone-of-control` «Зона контролю: зупинка руху поруч з ворогом» · entities/legality · 📎.
  - `+support-adjacent` «Бонус від сусідніх своїх юнітів» · entities/combat · 📎.
  - `+surround-penalty` «Оточення протилежними гексами: захист /2» · entities/combat · 📎.
  - `+terrain-bonus` / `+terrain-move-cost` / `+capture-property` / `+transport-load` — спільні з Advance Wars.
  - `+factory-stock` «Склад юнітів у будівлі, що переходить до захопника» · game-logic/economy · 🌱.
  - `+turn-limit` «Ліміт ходів карти як поразка» · game-logic/goal · 🌱 (близько до `move-limit`, але для партії, не пазла).

## Пропозиції до словників
- `+trigger:enter_zone` — увійшов у зону контролю (повтор із tactics).
- `+cond:zoc` — клітина в зоні контролю ворога · `+cond:surrounded` — ціль між нападниками на протилежних гексах.
- `+effect:capture` · `+effect:load` · `+effect:unload` · `+effect:counterattack` — повтори з Advance Wars; `+effect:store` — сховати юніт у будівлю (ремонт, вихід наступного ходу).
- `+role:property` — будівля з власником і складом (повтор).
- `+ui:terrain-percent` — відсоток ландшафту під курсором · `+ui:battle-forecast` — атака/захист перед ударом.
- `+window:command-box` — меню команд ходу · `+window:battle-scene` — анімація обміну ударами.

## Джерела
- ⭐ [Wikipedia: Nectaris](https://en.wikipedia.org/wiki/Nectaris) — огляд серії, розробник, список версій.
- [Wikipedia: Military Madness](https://en.wikipedia.org/wiki/Military_Madness) — 16+16 карт, паролі, 2P, ZOC оточенням, бонус сусідів, фабрики, табір полонених.
- [Base Nectaris: strategy guide](https://nectaris.tg-16.com/strategy_guide.html) — ZOC, Supporting Effect, Surrounding Effect (пари гексів 1–4, 2–5, 3–6).
- [Base Nectaris: how to play](https://nectaris.tg-16.com/how-to-play-tutorial.html) — порядок ходу, пряма/непряма атака, фабрики, ландшафт 0 %/5 %, досвід 1–8, ліміт 50 ходів.
- [Base Nectaris FAQ (PlayStation)](https://nectaris.tg-16.com/nectaris-military_madness-FAQ-playstation-play.html) — юніти, вивантаження, перемога/поразка.

## Непевне
- (?) Точні формули підтримки й оточення: Wikipedia і FAQ кажуть «зростає» / «навпіл»; пошукове зведення згадує «+50 % атаки сусіда» — не підтверджено сторінкою.
- (?) Розбіжність ZOC: Wikipedia — «кільце знижує атаку/захист, оточений рухається на 1»; Base Nectaris — «ворог зупиняється на першому гексі зони»; обидва записані.
- (?) Назви юнітів у таблиці — з посібника Neo Nectaris / PS-версії; склад армії першої гри (Lynx, Grizzly тощо) не перевірено.
- (?) Типи техніки (танки, артилерія «рух або постріл», ППО) і відповідний удар захисника — з памʼяті.
- (?) Що означають відсотки ландшафту (0 % дорога, 5 % рівнина) — імовірно бонус захисту.
- (?) Ліміт 50 ходів — з FAQ PS-версії; чи діє в оригіналі PC Engine.
- (?) Онлайн у ремейку 2009 — з памʼяті.
