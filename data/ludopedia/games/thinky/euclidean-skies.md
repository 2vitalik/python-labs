---
title: Euclidean Skies
slug: euclidean-skies
aka: [Euclidean Lands]
family: thinky
also: [tactics]
klass: avatar
axes:
  field: 3d
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: state
year: 2019
platforms: [PC, iOS]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/983980/Euclidean_Skies/", best: true, note: "опис і девлоги: обертання шарів світу, щоб зайти ворогу в спину; 40 рівнів + 15 з Euclidean Lands, боси, нескінченний генератор, skip, орбіта камери ПКМ"}
  - {kind: other, url: "https://www.macworld.com/article/3188925/euclidean-lands-twists-the-rubiks-cube-into-an-absorbing-brain-pleaser.html", note: "Euclidean Lands: 40 рівнів у 5 главах, обертання по стовпцю, вороги бʼють лише вперед, шипи на покинутій клітині, телепорти між кубами"}
  - {kind: other, url: "https://www.pocketgamer.com/articles/073300/euclidean-lands-review-a-masterful-puzzle-adventure/", note: "Euclidean Lands: тап — крок, свайп — обертання, вихід відкривається після всіх ворогів, щит для фронтальної атаки"}
  - {kind: other, url: "https://www.macstories.net/reviews/game-day-euclidean-lands/", note: "Euclidean Lands: мета, щити на полі, вороги, що теж обертають куб"}
  - {kind: other, url: "https://www.tapsmart.com/games/euclidean-skies-mind-bending-puzzle-experience/", note: "Euclidean Skies на iOS: власна гравітація кластера, перемикачі й двері в інших площинах, Endless Mode (v1.5), AR-режим"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Euclidean+Lands+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, cell-click, swipe-gestures, impassable-cells, touch-death, player-death, destroy-all-enemies, reach-exit, item-pickup, teleport, button-toggle, crush-by-slide, sequential-levels, level-select, skip-level, field-scaling, achievements-window, save-progress, streak-stats, +rotate-structure, +world-slice-rotate, +backstab-facing, +flanking, +front-only-attack, +spike-behind, +enemy-phase-after-player, +procedural-endless-unlock]
proposes: ["+cond:from_behind", "+effect:rotate_slice", "+card:world-slice-rotate", "+card:front-only-attack", "+card:spike-behind", "+card:procedural-endless-unlock", "+ui:camera-orbit"]
author: opus
date: 2026-11-09
---

# Euclidean Skies — тактичний «кубик Рубіка»: обертаєш шари світу, щоб опинитися в спині сильнішого ворога

## Суть
Герой зі списом стоїть на поверхні тривимірної сітки з кубів. Вороги сильніші й бʼють лише клітину перед собою, тому атака в лоб — смерть; перемога — опинитися **збоку або ззаду**. Головний інструмент — не крок, а **обертання шару світу** (стовпця/зрізу кубів) на 90°, як грань кубика Рубіка: шар везе з собою героя, ворогів, шипи й вихід, змінюючи, хто куди дивиться і що з чим сусідить. Euclidean Skies (2019, ПК) — сиквел мобільної Euclidean Lands (2017) і на Steam обʼєднує обидві: 40 нових рівнів, 15 найкращих з Lands як навчання та нескінченний генератор.

## Поле і час
- Поле — кластер кубів-блоків (форма «башти», «острова»), ходять по верхніх гранях; в одному рівні може бути кілька кубів, звʼязаних телепортами. У Skies кожен кластер має власну гравітацію, вихід може бути в іншій площині.
- Обертання: зріз (стовпець/шар) або цілий блок повертається навколо однієї з осей; обертання — повноцінний хід.
- Покроково: хід = крок героя або обертання; у частині глав вороги ходять після кожного ходу героя.
- Камера ізометрична; на ПК — орбіта камери правою кнопкою миші, чутливість обертання в меню; на iOS — AR-режим (Skies).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | 1 життя; спис (Skies) / меч і червоний шарф (Lands) | тап по сусідній клітині — крок на 1; бʼє ворога, заходячи з боку чи ззаду |
| Блок-куб | terrain | належить зрізам | поверхня для ходьби; обертається разом із зрізом |
| Обертовий зріз / блок | zone | вісь, напрям | поворот на 90° везе все, що на ньому |
| Непрохідний блок / провалля | static | — | не пройти й не перетнути |
| Вартовий-солдат | enemy | напрям погляду | атакує лише клітину перед собою; знищується збоку чи ззаду |
| Ворог, що ходить | enemy | напрям | у деяких главах робить хід після кожного ходу героя |
| Ворог, що обертає куб | enemy | — | сам повертає зрізи (пізні рівні Lands) (?) |
| Ворог із захистом | enemy | «форма захисту» | вимагає особливого підходу (?) |
| Скелет-монстр | enemy | — | вороги Skies (?) |
| Бос | boss | — | окремі бої, «важко перехитрити» |
| Щит | pickup | одноразовий (?) | дає змогу вбити ворога в лоб |
| Шипи на покинутій клітині | hazard | — | виростають з клітини, яку герой щойно покинув — туди не повернутись; обертання може насадити на них ворога |
| Шипована плита + перемикач | hazard / switch | — | плита небезпечна, перемикач поруч її вимикає (?) |
| Механізм-давилка | hazard | — | деяких ворогів можна розчавити механізмом рівня |
| Телепорт | static | пара | переносить між кубами рівня |
| Перемикач і двері | switch / gate | — | треба вивести героя в одну площину з ними |
| Вихід | gate | — | відкривається, коли знищено всіх ворогів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap_adjacent)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`.
- КОЛИ `input(swipe_slice)` → ТО `rotate(slice, 90)` — разом із героєм, ворогами, шипами й виходом.
- КОЛИ `contact(hero, guard)` → ЯКЩО `custom: «герой заходить з боку або ззаду відносно погляду вартового»` → ТО `disappear(guard)`.
- КОЛИ `contact(hero, guard)` → ЯКЩО `facing(guard, hero)` and `has(hero, shield)` → ТО `disappear(guard)`, `take(hero, shield)`.
- КОЛИ `enter(hero, cell_in_front_of_guard)` → ЯКЩО not `has(hero, shield)` → ТО `lose` — вартовий бʼє вперед.
- КОЛИ `turn_end(hero)` → ЯКЩО `mode(walking_enemies)` → ТО `move(enemy, dir)` (?).
- КОЛИ `leave(hero, cell)` → ТО `set_cell(cell, spikes)` (глава зі шипами).
- КОЛИ `custom: «обертання ставить ворога на шипи»` → ТО `disappear(enemy)`.
- КОЛИ `enter(enemy, crusher)` → ТО `disappear(enemy)`.
- КОЛИ `enter(hero, teleport)` → ТО `teleport(hero, pair)`.
- КОЛИ `contact(hero, shield)` → ТО `pickup`.
- КОЛИ `all_gone(enemy)` → ТО `set_state(exit, open)`; КОЛИ `enter(hero, exit)` → ЯКЩО `state(exit, open)` → ТО `win`, `next_level`.
- Перемога: усі вороги знищені + вихід · Поразка: герой у зоні атаки ворога → рестарт рівня · Рахунку нема; необовʼязковий челендж — мінімум ходів.
- Endless (Skies): КОЛИ `win` → ТО `counter(streak, +1)`; КОЛИ `lose` → ТО `custom: «серія обнуляється»` (?).

## Керування і ввід
- Lands / iOS: тап по сусідній клітині — крок; свайп по зрізу — обертання.
- Skies / ПК: лише миша («Mouse Only»): клік — крок, перетягування — обертання зрізу, права кнопка — орбіта камери (змінено після релізу, щоб уникати хибних кліків); чутливість обертання — в меню.
- iOS Skies: AR-режим для огляду (?).

## Вікна, меню, HUD
- `main-menu`: основна гра, навчання (15 рівнів Lands), нескінченний режим (з показом найдовшої серії перемог), налаштування.
- `level-select` — глави й рівні (Lands: 5 глав × 8) (?).
- `game-screen`: кластер кубів, герой, вороги; HUD мінімальний (?).
- `settings-window`: чутливість обертання миші, мова (14), звук (?).
- `end-screen` — смерть / перемога рівня (?); `achievements-window` (Steam).

## Фічі поза полем
- `skip-level` («Skip-a-level option for impatient players»).
- `mode-endless` — процедурні рівні з трьома базовими типами ворогів; відкривається після 15–20 рівнів основної гри; `streaks` — лічильник серії перемог і рекорд у меню.
- `tutorial` — 15 рівнів з Euclidean Lands; `achievements`; `cloud-save` (Steam Cloud); `localization`.
- Сюжету майже нема; гра заохочує «бавитися формами» без мети.

## Варіації й родичі
- **Euclidean Lands (2017, iOS)** — оригінал: 40 рівнів у 5 главах, кожна глава — новий поворот (вороги, що ходять; шипи на покинутій клітині; шиповані плити з перемикачами; кілька кубів з телепортами); щит на полі; вихід відкривається після всіх ворогів. Розробники — Miro Straka і kunabi brother (автори Blek).
- **Euclidean Skies (2019)** — сиквел: кластери з власною гравітацією, плавніша архітектура, більше рухомих частин і осей, боси; на Steam — збірка з найкращими рівнями Lands і генератором.
- Родичі: [Monument Valley](monument-valley.md) (обертання конструкцій), Hitman GO / Lara Croft GO ([Hitman GO](../push-slide/hitman-go.md): покрокова атака вартових збоку), [Hoplite](../tactics/hoplite.md) (покрокова тактика одного героя), кубик Рубіка.
- **Осі варіацій:** що обертається — зріз / цілий блок / камера; хто обертає — лише гравець / і вороги; атака ворога — лише вперед / по лінії / хід після гравця.

## Цікавинки для курсу
- Атака лише вперед і вбивство збоку/ззаду через напрям погляду — 📎 (порівняння векторів напрямку).
- Обертання зрізу 3D-сітки на 90° з усім вмістом і їхньою орієнтацією — 🥈 (матриці повороту координат + напрямків).
- Шипи на клітині, яку щойно покинув — 🌱 (слід, що забороняє повернення).
- Вихід відкривається, коли всі вороги знищені — 🌱.
- Генератор рівнів із перевіркою розвʼязності + лічильник серії — 🥇 (BFS по станах «позиція + орієнтація зрізів»).

## Мапа на каталог
- Є: `move-4dir`, `cell-click`, `swipe-gestures` ↔ тап і свайп · `impassable-cells` · `touch-death`, `player-death` ↔ удар вартового · `destroy-all-enemies` + `reach-exit` ↔ мета · `item-pickup` ↔ щит · `teleport` ↔ між кубами · `button-toggle` ↔ перемикач шипованих плит · `crush-by-slide` ↔ ворог на шипах після обертання · `sequential-levels`, `level-select`, `skip-level` · `field-scaling` ↔ орбіта/зум камери · `achievements-window`, `save-progress` · `streak-stats` ↔ серія в нескінченному режимі.
- **Нема** → пропозиції карток:
  - `+rotate-structure` (уже з Monument Valley) — тут з тактичним наслідком.
  - `+world-slice-rotate` «Обертання зрізу 3D-сітки з усім вмістом і орієнтаціями» · entities/move · 🥈 · слоти {axis, size}.
  - `+backstab-facing` / `+flanking` (уже пропоновані) ↔ атака ззаду/збоку.
  - `+front-only-attack` «Ворог бʼє лише клітину перед собою» · entities/combat · 📎.
  - `+spike-behind` «Покинута клітина стає шипами» · entities/interact · 🌱.
  - `+enemy-phase-after-player` (уже пропонована) ↔ вороги ходять після героя.
  - `+procedural-endless-unlock` «Нескінченний генератор, що відкривається після N рівнів, із серією перемог» · levels/generation · 🥇.

## Пропозиції до словників
- `+cond:from_behind` — атака з боку, протилежного погляду цілі (підтверджую; у `vocab/` ще нема).
- `+effect:rotate_slice(axis, i, deg)` — повернути зріз поля з усім вмістом (відмінне від `rotate`, що крутить одну сутність).
- `+card:world-slice-rotate`, `+card:front-only-attack`, `+card:spike-behind`, `+card:procedural-endless-unlock` — див. вище.
- `+ui:camera-orbit` — обертання камери навколо поля (уже просили інші файли).

## Джерела
- ⭐ [Steam: Euclidean Skies](https://store.steampowered.com/app/983980/Euclidean_Skies/) — опис, 40 + 15 рівнів, боси, генератор, skip, Cloud; девлоги про орбіту камери ПКМ, чутливість і умову відкриття нескінченного режиму.
- [Macworld: Euclidean Lands](https://www.macworld.com/article/3188925/euclidean-lands-twists-the-rubiks-cube-into-an-absorbing-brain-pleaser.html) — 5 глав × 40 рівнів, обертання по стовпцю й блоками, удар лише вперед, шипи, телепорти, мінімум ходів.
- [Pocket Gamer](https://www.pocketgamer.com/articles/073300/euclidean-lands-review-a-masterful-puzzle-adventure/) — тап/свайп, щит, вихід після всіх ворогів.
- [MacStories](https://www.macstories.net/reviews/game-day-euclidean-lands/) — мета, щити, вороги, що обертають куб, Miro Straka і kunabi brother.
- [TapSmart: Euclidean Skies](https://www.tapsmart.com/games/euclidean-skies-mind-bending-puzzle-experience/) — гравітація кластерів, перемикачі/двері в інших площинах, Endless Mode і навчання у v1.5, AR.
- YouTube: [пошук «Euclidean Lands gameplay»](https://www.youtube.com/results?search_query=Euclidean+Lands+gameplay).

## Непевне
- (?) Типи ворогів поіменно (крім вартових і скелетів) і механіка «ворогів, що обертають куб», «ворогів із захистом».
- (?) Умова відкриття нескінченного режиму: «15 рівнів» (пост до релізу) vs «20 рівнів» (пізніший девлог).
- (?) Чи знищення ворога — хід на його клітину чи удар із сусідньої.
- (?) Чи щит одноразовий; як працюють шиповані плити з перемикачами.
- (?) Розбивка рівнів Skies на глави, пункти меню й HUD — не описані.
