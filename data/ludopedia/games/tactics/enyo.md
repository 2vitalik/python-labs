---
title: ENYO
slug: enyo
aka: [Hook & Shield, Еньо]
family: tactics
also: [roguelike]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: state
year: 2016
platforms: [iOS, Android, visionOS]
links:
  - {kind: official, url: "https://apps.apple.com/us/app/enyo/id1118353232", best: true, note: "App Store: опис ядра (лише штовхати/тягнути в лаву й шипи) + історія версій: precise hook/bash, danger zones, Tortuga/Monkey/Froggo, Odyssey, Chronos Blessing"}
  - {kind: other, url: "https://www.ancientworldmagazine.com/reviews/enyo-game-arnold-rauers/", note: "огляд: 4 дії, 3 серця, поле 10×10, перезарядка стрибка, усі вороги, режими"}
  - {kind: other, url: "https://www.killscreen.com/indirect-combat-al-youll-tackle-enyos-labyrinth-monsters/", note: "непряма боротьба; походження з джему Hook & Shield; команда"}
  - {kind: other, url: "http://www.148apps.com/reviews/enyo-review/", note: "огляд: кинутий щит блокує bash до повернення; 10 процедурних рівнів"}
  - {kind: other, url: "https://www.pocketgamer.com/enyo/review/", note: "огляд: кільця на стінах, бомби тріскають плитки, Mimic у Daily"}
  - {kind: itch, url: "https://tinytouchtales.itch.io/hook-and-shield", note: "прототип 7DRL «Hook & Shield» у браузері; керування drag-ом"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ENYO+tinytouchtales+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [push-object, pull-object, environment-death, hp-damage, melee-vs-ranged, line-of-sight-attack, projectile-shot, status-effects, threat-range, destroy-all-enemies, sequential-levels, difficulty-levels, daily-puzzle, event-points, leaderboard, mode-select, tutorial-window, codex-window, achievements-window, settings-window, confirm-dialog, main-menu, game-screen, save-single-slot, language-picker, +environment-kill-only, +hook-pull, +wall-anchor-hook, +thrown-weapon-retrieve, +stun-leap, +cooldown-ability, +cracking-floor, +procedural-arena, +one-retry, +score-threshold-descent]
proposes: ["+card:environment-kill-only", "+card:hook-pull", "+card:thrown-weapon-retrieve", "+card:stun-leap", "+feature:one-retry", "+ui:danger-tiles-toggle"]
author: opus
date: 2026-11-09
---

# ENYO — роглайк без удару: гак тягне, щит штовхає, вбиває лише лава й шипи

## Суть
Богиня Еньо спускається лабіринтом за трьома артефактами, але **не має прямої атаки**: ворога можна вбити, лише виштовхнувши його щитом або витягнувши гаком у лаву чи на шипи. Кожна арена — маленька задача «як розставити ворогів і себе так, щоб наступна дія когось скинула». Гра виросла з джему 7DRL «Hook & Shield» (Arnold Rauers / Tinytouchtales), натхненного Auro і Hoplite.

## Поле і час
- Квадратна сітка 10×10 (ancientworldmagazine); стіни по краях і всередині, клітини лави, шипів, стрілок; кільця на стінах для гака.
- Покроково: Еньо робить дію → усі вороги ходять (ancientworldmagazine: «enemies move after each of Enyo's moves»). Таймера нема.
- Забіг Normal — 10 процедурно згенерованих глибин поспіль; рівень пройдено, коли вбито всіх живих ворогів.
- Інформація повна: зони, які ворог атакує, показано на полі (з 1.3.1, «enemy danger zones»); їх можна вимкнути в налаштуваннях.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Еньо | player | 3 серця | рух + 4 уміння: bash щитом, кидок щита, гак, стрибок з оглушенням |
| Щит (кинутий) | projectile | — | летить по лінії, штовхає/оглушує ціль, падає на порожню клітину; лежить, доки Еньо не підбере |
| Кільце на стіні | static | — | ціль гака: підтягує Еньо через поле до стіни |
| Стіна | static | — | непрохідна; удар об неї з Мінотавром оглушує Еньо |
| Шипована стіна | hazard | — | ворог, вбитий у неї, гине («impale») |
| Шипи на підлозі | hazard | — | смертельні для ворогів; кинутий щит їх руйнує |
| Лава | hazard | — | ворог, що потрапив, гине; летючих не бере |
| Тріснута плитка | terrain | — | від вибуху бомби; провалюється в лаву, коли на неї стає Еньо |
| Стрілка | terrain | напрям | змінює напрям бочки / ворога, яких зрушила Еньо |
| Бочка | object | — | штовхається; влучання оглушує; не рахується ворогом |
| Бомба | object | — | штовхається; вибух тріскає плитки; не рахується ворогом |
| Wardog | enemy | спис | підходить і бʼє впритул |
| Кентавр | enemy | лук | стріляє лише по ортогоналі з відстані |
| Мінотавр | enemy | — | розганяється по лінії, коли бачить Еньо; притиснуту до стіни оглушує |
| Гатор | enemy | — | кидає бомби, що тріскають плитки |
| Медуза | enemy | летить | лава їй не шкодить |
| Циклоп | enemy | щит | не штовхається; гак — лише якщо між ним і Еньо ≥1 вільна клітина |
| Сатир | enemy | гак | тягне Еньо через арену |
| Тортуга | neutral | не атакує | рухома «стіна для гака»: підтягнувшись до неї, Еньо оглушує сусідів |
| Мавпа | enemy | — | кидає бочки, щоб перекрити Еньо шлях |
| Froggo | enemy | стрибун | перестрибує клітини (з 1.3.0 стрибуни не оглушують) |
| Мімік | enemy | — | лише в Daily: випадкові здібності інших ворогів |
| Артефакт | pickup | 3 за гру | мета забігу (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(bash, target)` → ЯКЩО `has(enyo, shield)` and `not state(target, unpushable)` → ТО `push(target)`; precise bash — `custom: «гравець обирає клітину за ціллю, куди її відкинути»`.
- КОЛИ `input(bash, target)` → ЯКЩО `not has(enyo, shield)` → ТО `block` (щит кинуто — bash недоступний).
- КОЛИ `input(throw, dir)` → ЯКЩО `has(enyo, shield)` → ТО `throw(shield)`, `take(enyo, shield)`.
- КОЛИ `contact(shield, enemy)` → ТО `push(enemy)`, `stun(enemy, 1)`; щит `custom: «падає на найближчу порожню клітину»`.
- КОЛИ `contact(shield, floor_spikes)` → ТО `set_cell(floor)`.
- КОЛИ `contact(enyo, shield)` → ТО `pickup`, `score(+1 skull)` (повернення стрибком/кроком); КОЛИ `input(hook, shield)` → ТО `pull(shield)`, `pickup`.
- КОЛИ `input(hook, target)` → ЯКЩО `line_of_sight(enyo, target)` → ТО `pull(target)` до Еньо; precise hook — `custom: «зупинити на обраній клітині або перекинути за спину Еньо»`.
- КОЛИ `input(hook, wall_ring)` → ТО `move(enyo, wall_ring)` — `custom: «Еньо підтягується до кільця через поле»`.
- КОЛИ `input(hook, cyclops)` → ЯКЩО `not free(cell_between)` → ТО `block`.
- КОЛИ `input(bash|throw, cyclops)` → ТО `block` (щит циклопа, `state(cyclops, unpushable)`).
- КОЛИ `input(hook, tortuga)` → ТО `move(enyo, tortuga)`, `stun(adjacent(tortuga), 1)`.
- КОЛИ `input(leap, cell)` → ЯКЩО `not state(leap, cooldown)` → ТО `move(enyo, cell)`, `stun(adjacent(enyo), 1)`, `set_state(leap, cooldown, 1)` — двічі поспіль не можна.
- КОЛИ `enter(enemy, lava)` → ЯКЩО `not state(enemy, flying)` → ТО `disappear_a`, `score(+1 skull)`.
- КОЛИ `contact(enemy, spiked_wall|floor_spikes)` → ТО `disappear_a`, `score(+1 skull)`.
- КОЛИ `after(explode(bomb))` → ТО `set_cell(cracked)` навколо (?); КОЛИ `enter(enyo, cracked)` → ТО `set_cell(lava)`; ворог на клітині, що стала лавою, — `disappear`.
- КОЛИ `enter(barrel|enemy, arrow)` → ТО `face(a, arrow_dir)` і рух триває в новому напрямку.
- КОЛИ `contact(barrel, unit)` → ТО `stun(unit, 1)`.
- КОЛИ `turn_end(enyo)` → ТО кожен ворог `custom: «ходить за своїм патерном»`, далі хід Еньо.
- Wardog: КОЛИ `adjacent(wardog, enyo)` → ТО `damage(enyo, 1)` (?).
- Кентавр: КОЛИ `line_of_sight(centaur, enyo)` → ЯКЩО `custom: «по ортогоналі, не впритул»` → ТО `damage(enyo, 1)` (?).
- Мінотавр: КОЛИ `line_of_sight(minotaur, enyo)` → ТО `custom: «розгін по лінії до перешкоди»`; ЯКЩО `custom: «Еньо притиснута до стіни»` → ТО `stun(enyo, 1)`.
- Сатир: КОЛИ `line_of_sight(satyr, enyo)` → ТО `pull(enyo)`.
- Гатор / Мавпа: КОЛИ `turn_start(enemy)` → ТО `throw(bomb)` / `throw(barrel)` у бік Еньо.
- КОЛИ `all_gone(enemy)` → ТО `next_level` (кільця, бомби, бочки не рахуються — «non-living units»).
- КОЛИ `hp_zero(enyo)` → ЯКЩО `first_time` → ТО `custom: «Chronos' Blessing»`, `restart` глибини без втрати прогресу; інакше `lose`.
- Odyssey: КОЛИ `counter(skulls, >=, target)` → ТО `next_level`, `custom: «поріг росте з кожною глибиною»`.
- Перемога: пройти 10 глибин і забрати артефакти · Поразка: серця вичерпано після використаного благословення · Рахунок: черепи за вбивства середовищем, повернення щита, серії вбивств (лідерборди Game Center).

## Керування і ввід
- Тач: тап по кнопці уміння (з 1.3.1 вибір зброї — лише тапом), потім напрям/ціль; у прототипі — клік по дії + drag ліворуч/праворуч/вгору/вниз для bash і гака, клік по підсвіченій клітині для стрибка.
- Precise-режими (1.3.0): тап по самій цілі — повна сила; тап по клітині за ціллю — точне місце приземлення (hook, bash, throw).
- Рух — drag пальцем і відпускання (148Apps: на малих екранах палець закриває поле).
- Тап по ворогу — інфо; tap-and-hold — підказка (`tooltip`).

## Вікна, меню, HUD
- `main-menu`: Normal · Expert · Daily · Odyssey → `mode-select`; Tutorial (переграваний) → `tutorial-window`; Monster help → `codex-window`; Settings → `settings-window` (danger tiles вкл/викл, мова); Game Center → `leaderboard`, `achievements-window`; Unlock ENYO & remove ads → `shop-window` (IAP).
- `confirm-dialog`: продовжити збережену гру? Так / Ні (кнопка «No» з 1.3.0).
- `game-screen`: поле 10×10; `lives` (серця); `score` (черепи); `ability-buttons` (bash, throw, hook, leap; стан стрибка — перезарядка); `threat-range` (danger zones); `tooltip`.
- `end-screen`: смерть → пропозиція Chronos' Blessing або підсумок забігу з черепами; Odyssey — поріг наступної глибини (?).
- Переходи: main-menu → mode-select → game-screen → (усі вбиті) наступна глибина → … → end-screen; Save & quit → main-menu → confirm-dialog.

## Фічі поза полем
- Режими: `mode-classic` (Normal) · Expert (`difficulty-presets`, свій лідерборд) · `mode-daily` (однакова гра для всіх; у Killscreen — для платних) · Odyssey (однакові випадкові виклики, поріг черепів для спуску; з 1.2.1).
- `continue`: save & quit (з 1.3.1; save states — з 1.0.2).
- `tutorial`, `codex` (довідка по монстрах), `leaderboard-online`, `achievements`, `localization` (EN, DE, JA, PT, RU, ES).
- Одна повторна спроба глибини за забіг — Chronos' Blessing (1.0.2).
- Прокачки між рівнями нема (Pocket Gamer; рецензенти просили).

## Варіації й родичі
- «Hook & Shield» (7DRL, HTML5) → ENYO 2016 → 1.2.1 (2018: Tortuga, Monkey, Froggo, Odyssey) → 1.3 Anniversary (precise-контроль, danger zones, save & quit).
- Родичі: [Auro](auro.md) (лише bump у воду), [Hoplite](hoplite.md) (лава + штовхання щитом, але є й спис), [Into the Breach](into-the-breach.md) (штовхання в середовище), [Tactical Breach Wizards](tactical-breach-wizards.md) (викидання у вікна), Lara Croft GO (пастки замість атаки).
- **Осі варіацій**: чим вбити — пряма шкода / лише середовище (ENYO, Auro) / обидва (Hoplite) · переміщення ворога — штовхання / тягнення / перекид за спину · зброя — завжди при собі / кинута й треба повернути (щит ENYO, спис Hoplite).

## Цікавинки для курсу
- Вбивство лише середовищем: у гравця нема `damage`, рахуються тільки `push`/`pull` у лаву чи шипи — 🥉 (таблиця «ворог × клітина» з винятками: летючий, нештовхуваний).
- Гак: тягнення по лінії до гравця з вибором точки зупинки і перекидом за спину — 🥉 (трасування лінії + вибір клітини на ній).
- Кинутий щит лишається на полі й вимикає bash до повернення — 📎 (стан інвентаря, що залежить від предмета на сітці).
- Стрибок з оглушенням сусідів і перезарядкою в один хід — 📎.
- Бомба → тріснуті плитки → лава під гравцем: середовище змінюється подіями — 🥉.
- Odyssey: поріг черепів для спуску, що росте — 🌱.

## Мапа на каталог
- Є: `push-object` (bash, кидок) · `pull-object` (гак) · `environment-death` (лава, шипи) · `hp-damage` (серця) · `melee-vs-ranged` (Wardog / Кентавр) · `line-of-sight-attack` (Кентавр, Мінотавр, Сатир) · `projectile-shot` (щит, бомби, бочки) · `status-effects` (оглушення) · `threat-range` (danger zones) · `destroy-all-enemies` · `sequential-levels` · `difficulty-levels` · `daily-puzzle` · `event-points` (черепи) · `leaderboard` · вікна.
- **Нема** → пропозиції карток:
  - `+environment-kill-only` «Вбити лише середовищем» · entities/combat · 🥉 · слот {hazards: list} — ENYO, Auro.
  - `+hook-pull` «Гак: тягнення по лінії» · entities/legality · 🥉 · слот {stop: adjacent|chosen|behind} — дитина `pull-object`, але на відстань.
  - `+thrown-weapon-retrieve` «Кинута зброя лежить на полі до повернення» · entities/state · 📎 — щит ENYO, спис Hoplite.
  - `+stun-leap` «Стрибок, що оглушує сусідів» · entities/combat · 📎 · слот {cooldown: 1}.
  - `+wall-anchor-hook` «Гак до кільця — рух самого гравця» · entities/move · 🌱.
  - `+cracking-floor` «Плитка тріскає і стає ямою/лавою» · entities/interact · 📎.
  - `+one-retry` «Одна повторна спроба рівня за забіг» · game-logic/lose · 🌱.
  - `+score-threshold-descent` «Спуск лише після порогу очок» · levels/progression · 🌱.

## Пропозиції до словників
- `+card:environment-kill-only` — гравець не має шкоди, вороги гинуть лише від клітин (лава, шипи, вода).
- `+card:hook-pull` — тягнення цілі по лінії з вибором точки зупинки (відмінне від Sokoban-тягнення сусіда).
- `+card:thrown-weapon-retrieve` — кинутий предмет лежить на полі й блокує частину дій до повернення.
- `+card:stun-leap` — стрибок у межах радіуса з оглушенням сусідів і перезарядкою.
- `+feature:one-retry` — одна безкоштовна повторна спроба рівня за забіг (Chronos' Blessing).
- `+ui:danger-tiles-toggle` — перемикач показу клітин загрози (для досвідчених гравців).

## Джерела
- ⭐ [App Store: ENYO](https://apps.apple.com/us/app/enyo/id1118353232) — опис ядра, історія версій 1.0–1.3.2 (вороги, precise-контроль, режими, Chronos' Blessing).
- [Ancient World Magazine](https://www.ancientworldmagazine.com/reviews/enyo-game-arnold-rauers/) — 4 дії, перезарядка стрибка, 3 серця, 10×10, поведінка всіх ворогів, режими.
- [Kill Screen](https://www.killscreen.com/indirect-combat-al-youll-tackle-enyos-labyrinth-monsters/) — непряма боротьба, джем Hook & Shield, команда.
- [148Apps](http://www.148apps.com/reviews/enyo-review/) — кинутий щит вимикає bash до повернення.
- [Pocket Gamer](https://www.pocketgamer.com/enyo/review/) — кільця на стінах, бомби й тріснуті плитки, Mimic, 10 поверхів.
- [itch: Hook & Shield](https://tinytouchtales.itch.io/hook-and-shield) — прототип 7DRL, керування.

## Непевне
- (?) Чи рух — окрема дія за хід, чи хід = одна дія з п'яти (крок або вміння): джерела кажуть лише «limited set of actions per turn».
- (?) Скільки клітин пролітає ціль при bash «на всю силу» і при кидку щита.
- (?) Шкода ворогів по Еньо (1 серце?), чи шкодять Еньо лава/шипи.
- (?) Як саме вибух бомби тріскає плитки (радіус) і що відбувається з ворогом на тріснутій плитці.
- (?) Як артефакти привʼязані до глибин (3 артефакти на 10 рівнів); черепи за серію («kill streak 2 skulls») — лише згадка в патч-нотах.
- (?) «Стрибок на оглушеного ворога оглушує його» і «Free mode» — лише в патч-нотах, без пояснень.
