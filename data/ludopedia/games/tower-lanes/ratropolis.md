---
title: Ratropolis
slug: ratropolis
aka: [Ратрополіс, 鼠之城邦]
family: tower-lanes
also: [build-sim]
klass: cursor
axes:
  field: 1d
  time: realtime
  opponent: none
  info: partial
  random: both
  goal: survive
year: 2020
platforms: [PC, Mac]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1108370/Ratropolis/", best: true, note: "Cassel Games; EA 1.11.2019, реліз 22.12.2020; 500+ карт 4 типів, 8 базових карт на лідера, 6 лідерів, радники, 100+ подій, 6 кінцівок"}
  - {kind: other, url: "https://www.metacritic.com/game/ratropolis/", note: "уривки рецензій: real-time карти, side-scrolling TD, вороги з обох боків міста, найм воїнів, повільні юніти"}
  - {kind: other, url: "https://steamcommunity.com/app/1108370/guides/", note: "гайди: лідери Builder/Merchant, «забруднення» 20 як складність, скриптові події на хвилях 4, 9, 14, 20, 23, 27, 120 хвиль"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ratropolis+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [round-currency, enemy-waves, spawn-schedule, enemy-reached-base, hp-damage, melee-vs-ranged, move-auto, run-relics, permadeath, character-select, difficulty-levels, achievements-window, leaderboard, game-pause, codex-window, +lane-grid, +deck-draw, +deck-builder, +realtime-card-play, +two-sided-lane, +card-types-economy-build-army-skill, +advisor-choice, +random-run-events, +scripted-wave-events, +pollution-difficulty-ladder, +multiple-endings]
proposes: ["+role:card", "+role:building", "+role:unit", "+effect:draw", "+effect:discard", "+trigger:event", "+window:choice-window", "+window:deck-window", "+ui:hand-bar", "+ui:wave-timer", "+axis:session=run", "+feature:difficulty-ladder"]
author: opus
date: 2026-11-09
---

# Ratropolis — карткова оборона щурячого міста на одній лінії: граєш карти в реальному часі, будуєш і наймаєш, хвилі йдуть з обох боків

## Суть
Роґлайт-декбілдер, схрещений з tower defense і будуванням міста. Місто щурів — горизонтальна смуга; хижаки й монстри хвилями заходять з лівого і правого краю. Гравець не керує юнітами напряму: він у реальному часі грає карти з руки — економіка (дохід), будівлі (на лінії), військо (найм воїнів), навички (миттєві ефекти). Між хвилями й на подіях колода росте, карти покращуються; місто впало — забіг скінчився.

## Поле і час
- Поле — 1D-смуга вид збоку з центром-містом; вороги приходять з обох країв, отже оборону треба ділити на два фланги.
- Будівлі займають місця на лінії; місто розростається в обидва боки (?).
- Час — realtime: хвилі за таймером, карти граються будь-коли; рецензенти наголошують на «шаленому» темпі; пауза — є в оригіналі (?).
- Забіг ділиться на нумеровані хвилі; на певних хвилях (4, 9, 14, 20, 23, 27) — скриптові події з вибором (за гайдом).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Місто / головна будівля | static (`+role:building`) | HP | серце бази; падіння = кінець забігу (?) |
| Карта економіки | `+role:card` | ціна | дає золото / дохід / жителів (?) |
| Карта будівлі | `+role:card` | ціна | ставить будівлю на лінію: житло, стіну, вежу, виробництво (?) |
| Карта війська | `+role:card` | ціна | наймає воїнів, що йдуть на фланг і бʼються самі |
| Карта навички | `+role:card` | ціна | миттєвий ефект: шкода, баф, ресурс (?) |
| Будинок / житло | static (`+role:building`) | — | збільшує населення й дохід (?) |
| Стіна / укріплення | static (`+role:building`) | HP | тримає ворога на краю міста (?) |
| Воїн-щур | ally (`+role:unit`) | HP, шкода, ближній/дальній | автономно рухається до ворогів; рецензії скаржаться на повільність |
| Хижак / монстр | enemy | HP, шкода | заходить хвилею з лівого або правого краю, руйнує все на шляху |
| Бос-хвиля | boss | — | сильний ворог на ключових хвилях (?) |
| Лідер | supply | 8 базових карт, риси | обирається перед забігом, задає стиль гри (Builder, Merchant…) |
| Радник | neutral | талант: фінанси / оборона / лідерство | пропонує варіанти, коли виникає проблема |
| Золото | resource | — | ціна розіграшу карт (?) |
| Колода / рука | supply | — | з колоди карти приходять у руку (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «колода = 8 базових карт обраного лідера»`.
- КОЛИ `timer(every)` → ТО `custom: «карта з колоди в руку»` (?) — або за дією гравця, частіше за золото (?).
- КОЛИ `input(play, card)` → ЯКЩО `has(gold, price)` → ТО `currency(-price)` і ефект за типом карти:
  - економіка: `currency(+n)` / `custom: «дохід або жителі»` (?);
  - будівля: `place(player, building)` на вільне місце лінії;
  - військо: `spawn_at(unit, city)`;
  - навичка: `damage(n)` / `set_state(a, s, dur)` / `currency(+n)` за картою.
- КОЛИ `timer(every)` → ЯКЩО `custom: «є житло/економічні будівлі»` → ТО `currency(+income)` (?).
- КОЛИ `wave_start` → ТО `spawn_at(enemy, left_edge)` and/or `spawn_at(enemy, right_edge)`.
- КОЛИ `spawned(unit)` → ТО `move(unit, toward_enemy)`; КОЛИ `in_range(unit, enemy, range)` → ТО `damage(n)`.
- КОЛИ `contact(enemy, building)` → ТО `damage(building, n)`; КОЛИ `hp_zero(building)` → ТО `disappear_a`.
- КОЛИ `wave_cleared` → ТО `choose(options)` — нова карта / апгрейд / прибрати карту з колоди (?).
- КОЛИ `custom: «виникла проблема»` → ТО `choose(options)` від радника з талантом.
- КОЛИ `rng(p)` → ТО `custom: «випадкова подія з вибором»` (100+ подій).
- КОЛИ `counter(wave, ==, n)` → ЯКЩО `custom: «скриптова хвиля 4/9/14/20/23/27»` → ТО `custom: «подія, вибір у якій веде до різних кінцівок»`.
- КОЛИ `destroyed(city)` → ТО `lose`, `custom: «забіг скінчено; прогрес розблокувань лишається»`.
- КОЛИ `counter(wave, ==, final)` → ЯКЩО `custom: «місто вціліло»` → ТО `win`, `custom: «одна з 6 кінцівок»` (?).
- Перемога: пережити кампанію до кінцівки · Поразка: місто впало · Рахунок: Steam-лідерборди (?), час проходження (досягнення «за 19 хвилин»).

## Керування і ввід
- Миша: клік/перетягування карти з руки на лінію (будівля — у місце, військо — на фланг (?)), прокрутка камери вздовж міста.
- Одночасно стежити за двома флангами й рукою — основний «тиск» гри.
- Армією керування обмежене (рецензія CD-Action).

## Вікна, меню, HUD
- `main-menu` → `character-select` (6 лідерів) → `difficulty-select` («забруднення», до 20 рівнів (?)).
- `game-screen`: смуга міста, `+ui:hand-bar` (рука карт з цінами), `coins`, `wave-counter`, `+ui:wave-timer`, HP міста (`hp-bar`), напрямок наступної хвилі (`spawn-indicator` (?)).
- `+window:choice-window` — радник/подія: текст і 2–3 варіанти.
- `upgrade-window` / `+window:deck-window` — вибір нової карти, апгрейд, видалення (?).
- `codex-window` — внутрішня енциклопедія карт (гайд радить «дивитися в енциклопедії»).
- `pause-menu` (?) · `end-screen` — кінцівка або падіння міста · `achievements-window` (Steam).

## Фічі поза полем
- `meta-progression`: розблокування нових карт за грою; 6 лідерів з власними колодами й рисами.
- `difficulty-presets` — драбина «забруднення» (Pollution 1…20) (?).
- 6 кінцівок; `achievements` (пережити 120 хвиль за Builder, пройти за 19 хвилин), `leaderboard-online`, `cloud-save`.

## Варіації й родичі
- У корпусі: [monster-train](monster-train.md) (декбілдер-оборона по поверхах), [thronefall](thronefall.md) (оборона міста з будівлями-доходом), [swords-and-soldiers](swords-and-soldiers.md) і [age-of-war-stick-war](age-of-war-stick-war.md) (1D-лінія, юніти діють самі), [plants-vs-zombies](plants-vs-zombies.md) (валюта → розстановка на смугах), [wildfrost](wildfrost.md), [inscryption](inscryption.md) (карткові бої).
- Поза корпусом: Kingdom (2D-смуга, загроза з обох боків), Slay the Spire (декбілдер-роґлайт) — порівняння рецензентів.
- **Осі варіацій**: ресурс — золото з будівель / мана за таймером · загроза — з одного боку / з обох · розіграш — реальний час / покроково · прогрес — карти між хвилями / мета між забігами.

## Цікавинки для курсу
- Двобічна 1D-оборона: хвиля з випадкового краю, ресурс ділиться між флангами — 🌱.
- Розіграш карт у реальному часі: рука + ціна + таймер добору — 📎.
- Чотири типи карт з різними цілями ефекту (гроші / місце на лінії / юніт / миттєве) — 📎.
- Декбілдинг між хвилями: додати / покращити / видалити карту — 🥉.
- Події з вибором і скриптові хвилі, що ведуть до різних кінцівок (граф подій) — 🥉.
- Драбина складності-модифікаторів (20 рівнів) — 📎.

## Мапа на каталог
- Є: `round-currency` ↔ золото · `enemy-waves` / `spawn-schedule` · `enemy-reached-base` ↔ падіння міста · `hp-damage` · `melee-vs-ranged` · `move-auto` ↔ воїни самі · `run-relics` ↔ риси лідерів/радники (?) · `permadeath` ↔ кінець забігу · `character-select` · `difficulty-levels` · `codex-window` · `achievements-window` · `leaderboard` · `game-pause` (?).
- **Нема** → пропозиції карток:
  - `+lane-grid`, `+deck-draw`, `+deck-builder` — уже в корпусі (Swords & Soldiers, Monster Train).
  - `+realtime-card-play` «Карти граються в реальному часі, без ходів» · game-logic/economy · 📎.
  - `+two-sided-lane` «Загроза з обох кінців лінії» · fields/topology · 🌱.
  - `+card-types-economy-build-army-skill` «Типи карт з різною ціллю ефекту» · game-logic/economy · 📎.
  - `+advisor-choice` / `+random-run-events` «Подія з вибором посеред забігу» · game-logic/events · 📎.
  - `+scripted-wave-events` «Сюжетні події на фіксованих хвилях» · game-logic/waves · 🌱.
  - `+pollution-difficulty-ladder` «Драбина складності з N рівнів-модифікаторів» · game-logic/difficulty · 📎.
  - `+multiple-endings` «Кінцівка залежить від виборів» · levels/progression · 🥉.

## Пропозиції до словників
- `+role:card` · `+role:building` · `+role:unit`.
- `+effect:draw` — карта з колоди в руку · `+effect:discard` — видалити/скинути карту.
- `+trigger:event` — випадкова/скриптова подія забігу.
- `+window:choice-window` — подія чи радник з варіантами · `+window:deck-window` — перегляд і правка колоди.
- `+ui:hand-bar` — рука карт з цінами · `+ui:wave-timer` — відлік до хвилі.
- `+axis:session=run` · `+feature:difficulty-ladder`.

## Джерела
- ⭐ [Steam: Ratropolis](https://store.steampowered.com/app/1108370/Ratropolis/) — опис: real-time карти, 500+ карт (economy, building, military, skill), 8 базових на лідера, 6 лідерів, радники, 100+ подій, 6 кінцівок, дати.
- [Metacritic: Ratropolis](https://www.metacritic.com/game/ratropolis/) — уривки рецензій: side-scrolling TD, вороги з обох боків, найм воїнів, повільні юніти, порівняння з Kingdom і Slay the Spire.
- [Steam-гайди](https://steamcommunity.com/app/1108370/guides/) — назви гайдів: лідери, «забруднення 20», скриптові хвилі 4/9/14/20/23/27, 120 хвиль.
- YouTube: пошук «ratropolis gameplay».

## Непевне
- (?) Джерело золота (житло, податок, жителі), механіка добору карт (таймер чи купівля), розмір руки — Steam-опис мовчить, гайди віддали 429.
- (?) Чи є стіни як окремі будівлі й «клітини» лінії; як саме ставиться будівля.
- (?) Пауза в оригіналі; кількість хвиль до фіналу; чи 120 хвиль — нескінченний режим.
- (?) Імена 4 інших лідерів; що дає «забруднення» на кожному рівні.
- Рік: черга казала 2021 — за Steam повний реліз 22.12.2020 (EA з 1.11.2019).
