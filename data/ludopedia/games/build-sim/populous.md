---
title: Populous
slug: populous
aka: [Populous (1989), Популус]
family: build-sim
also: [tactics]
klass: cursor
axes:
  field: iso
  time: realtime
  opponent: ai
  info: full
  random: setup
  goal: state
year: 1989
platforms: [Amiga, Atari ST, DOS, PC Engine, Mega Drive, SNES]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Populous_(video_game)", best: true, note: "підняття/опускання землі, мана, сили (землетрус, болото, лицар, вулкан, повінь), 500 рівнів, ландшафти, World Editor"}
  - {kind: other, url: "https://ts.popre.net/archive/Downloads/Docs/Populous_1989_Manual.pdf", note: "скан мануалу 1989 (великий PDF): хатини на 1–2 ділянках, замок — велика пласка площа, Papal Magnet, режими поселенців, лицар"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Populous+1989+gameplay", note: "пошук; геймплей"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Populous", note: "пошук"}
stage: v1
coverage: 50
mechanics: [cell-click, height-levels, cell-transform, spawner-entity, round-currency, in-round-upgrades, chase-greedy, random-walk, piece-capture, map-window, minimap-radar, level-password, sequential-levels, rule-variants, game-pause, online-multiplayer, ai-opponent, +vertex-heightmap, +flat-area-building, +god-powers, +rally-magnet, +follower-modes, +world-code-progression]
proposes: ["+card:vertex-heightmap", "+card:flat-area-building", "+card:god-powers", "+card:rally-magnet", "+card:follower-modes", "+effect:raise", "+cond:height_diff", "+cond:flat_area", "+ui:mana-slider", "+ui:command-icons"]
author: opus
date: 2026-11-09
---

# Populous — бог не керує людьми, а рівняє землю: чим більша пласка площа, тим більший дім і тим більше мани

## Суть
Перша «god game»: гравець — божество над ізометричною мапою-«столом», де живуть його послідовники і ворожі. Головний інструмент — **підняти або опустити землю**; поселенці самі шукають пласку ділянку і будують житло, розмір якого залежить від того, скільки пласкої землі навколо. Будинки родять нових людей і ману; мана відкриває «божественні втручання» — від землетрусу до Армагеддону. Мета — щоб твоїх послідовників стало досить, аби знищити ворожих.

## Поле і час
- Квадратна сітка з **висотами у вершинах** (heightmap): кожна точка має рівень; клітина між 4 вершинами пласка, якщо всі 4 однакові, інакше схил. Рівень 0 — вода (?).
- Видно ізометричне вікно (частина світу) і мапу всього світу у вигляді розкритої книги.
- Ландшафти: трава, пустеля, сніг і лід, скелі й лава (+5 у The Promised Lands, +1 у The Final Frontier) — впливають на розвиток поселень.
- Час — real-time; люди ходять і будують без вводу; мана накопичується безперервно.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вершина рельєфу | terrain | висота | гравець піднімає/опускає; сусідні вершини тягнуться так, щоб схил був ≤1 (?) |
| Пласка ділянка | terrain | — | місце для будинку; більша площа → більший будинок |
| Вода | hazard | — | хто зайшов — тоне (?); опускання до 0 топить будинки |
| Послідовник (walker, peep) | neutral | сила, сторона | блукає, шукає пласку землю; у режимі бою б'ється з ворогом; зливається з іншими, сила сумується (?) |
| Лідер | neutral | — | один на сторону; іде до Papal Magnet; з нього робиться лицар |
| Лицар (knight) | ally | сила | незалежний боєць: іде нищити ворожих людей і будинки, не підконтрольний |
| Поселення: намет/хатина … замок | spawner | рівень = розмір пласкої площі | росте до заповнення, випускає нового послідовника; дає ману |
| Papal Magnet (анкх) | switch | позиція | точка збору: у режимі «до магніту» послідовники йдуть сюди |
| Болото | hazard | дрібне / бездонне (опція) | хто зайшов — гине |
| Скеля / камінь | static | — | не дає будувати (?) |
| Ворожий бог (AI) | enemy | мана | робить те саме: рівняє землю, кидає втручання |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, vertex)` → ЯКЩО `in_range(vertex, own_settlement, r)` (?) and `has(god, mana >= cost_raise)` → ТО `custom: «висота вершини +1; сусідні вершини підтягуються, щоб різниця з нею була ≤1»`, `currency(-cost)`.
- КОЛИ `input(right_click, vertex)` → ТО `custom: «висота −1 з тим самим підтягуванням вниз»`.
- КОЛИ `tick` → ЯКЩО `state(walker, settle)` and `custom: «під ним пласка вільна ділянка»` → ТО `spawn(settlement)`, `disappear_a`.
- КОЛИ `tick` → ЯКЩО `custom: «навколо поселення пласка площа ≥ поріг рівня»` → ТО `transform(settlement, next_level)` — від намету (1–2 ділянки) до замку (велика площа).
- КОЛИ `tick` → ЯКЩО `custom: «площу навколо зіпсовано (схил, вода)»` → ТО `transform(settlement, smaller)`.
- КОЛИ `counter(settlement.population, >=, capacity)` → ТО `spawn_at(walker, settlement)` — новий послідовник іде шукати землю.
- КОЛИ `tick` → ТО `currency(+Σ settlements)` — мана від поселень (більші — більше (?)).
- КОЛИ `input(mode, go_to_magnet)` → ТО `custom: «послідовники збираються до лідера, лідер іде до Papal Magnet»`.
- КОЛИ `contact(walker, walker)` → ЯКЩО `mode(gather)` and `same(a, b, side)` → ТО `merge(a, b → stronger_walker)`.
- КОЛИ `input(mode, fight)` → ТО `custom: «послідовники шукають ворога»`.
- КОЛИ `contact(walker, enemy_walker)` → ТО `custom: «бій: сильніший виживає з залишком сили»`.
- КОЛИ `contact(walker, enemy_settlement)` → ЯКЩО `state(walker, fight|knight)` → ТО `custom: «напад на будинок; переможений будинок стає твоїм або руйнується (?)»`.
- КОЛИ `input(power, earthquake)` → ЯКЩО `has(god, mana)` → ТО `custom: «випадково здибити рельєф у зоні»`.
- КОЛИ `input(power, swamp)` → ТО `spawn_at(swamp, flat_cells)`.
- КОЛИ `input(power, knight)` → ТО `transform(leader, knight)`.
- КОЛИ `input(power, volcano)` → ТО `custom: «підняти гору й закидати камінням зону»`.
- КОЛИ `input(power, flood)` → ТО `custom: «рівень води +1 по всьому світу»` — топить низини.
- КОЛИ `input(power, armageddon)` → ТО `custom: «усі послідовники обох сторін ідуть у фінальну битву»`.
- КОЛИ `enter(walker, water|swamp)` → ТО `disappear_a`.
- КОЛИ `all_gone(enemy_walkers)` and `all_gone(enemy_settlements)` → ТО `win` → наступний світ (Conquest).
- КОЛИ `all_gone(own_walkers)` and `all_gone(own_settlements)` → ТО `lose`.
- Рахунок: перехід на світ, номер якого залежить від результату (?).

## Керування і ввід
- Миша: ЛКМ по вершині — підняти землю, ПКМ — опустити (стрілка-курсор); клік по іконці втручання, потім по точці.
- Іконки-команди на «столі»: 4 режими поселенців (до магніту / поселитися / збиратися / битися), сили, прокрутка вікна, «знайти лідера / лицаря / битву» (?).
- Клік по сутності — щит показує її сторону й силу (?).
- Книга-мапа: клік — перемістити вікно в цю точку.

## Вікна, меню, HUD
- `game-screen`: ізометричне вікно на «столі» + книга-мапа (`minimap`) + `+ui:mana-slider` (шкала божественної сили) + `+ui:command-icons` + щит вибраного.
- `main-menu`/вибір гри: Conquest · Custom game · 2-player (?); `level-password` — назва світу як пароль (?).
- `custom-window` налаштувань Custom game: ландшафт, хто грає, обмеження сил, правила (вода смертельна, болота бездонні, будування лише вгору (?)).
- `end-screen` світу → наступний світ.
- `pause-menu` (?).

## Фічі поза полем
- `levels-sequential` — Conquest на 500 світів; `level-password` / `share-code` — імʼя світу як код (?).
- `custom-rules` — Custom game з перемикачами правил; `level-editor` — Populous World Editor (зовнішній вигляд людей, міст, рельєфу).
- `online-multiplayer` — два гравці через лінк (модем/кабель (?)); DS-версія — до 4 гравців бездротово.
- `pause`; збереження (?).

## Варіації й родичі
- Populous II (1991), Populous: The Beginning (1998, 3D-сфера), Populous DS (2008); Powermonger; духовні нащадки — Black & White, Reus, Godus.
- Родичі в корпусі: `townscaper` (форма з сусідів), `dorfromantik`, `caesar-3` (житло росте від умов), `oxygen-not-included-cells`.
- **Осі варіацій рельєфу**: висоти в клітинах / у вершинах · підтягування сусідів (схил ≤1) / вільний · будова на пласкій ділянці 1×1 / площі N×N · рівень води константа / змінний (повінь).

## Цікавинки для курсу
- Heightmap у вершинах з каскадним підтягуванням сусідів (схил ≤1) — 🥉 (BFS-хвиля, як «пісочна купа» навпаки).
- Будинок росте від розміру пласкої площі навколо — 📎 (перевірка квадрата навколо клітини).
- Поселенці з режимами (поселитися / до магніту / злитися / битися) — 🥉 (FSM для натовпу).
- Мана-економіка з лінійкою сил, що відкриваються за порогом — 📎.
- Повінь: глобальний рівень води і перерахунок суші — 🌱.

## Мапа на каталог
- Є: `height-levels` (висоти клітин) · `cell-transform` (поселення ↔ рівень) · `spawner-entity` (будинок випускає людей) · `round-currency` (мана) · `in-round-upgrades` (сили за порогом мани) · `random-walk` (блукання) · `chase-greedy` (лицар іде на ворога) · `piece-capture` (захоплення будинку (?)) · `map-window` + `minimap-radar` · `level-password` · `sequential-levels` · `rule-variants` (Custom game) · `online-multiplayer` · `ai-opponent`.
- **Нема** → пропозиції карток:
  - `+vertex-heightmap` «Висоти у вершинах з підтягуванням сусідів» · entities/legality · 🥉 · слот {max_slope}.
  - `+flat-area-building` «Розмір будови = пласка площа навколо» · entities/state · 📎 · слот {levels}.
  - `+god-powers` «Сили за ману з лінійкою відкриття» · game-logic/economy · 📎.
  - `+rally-magnet` «Точка збору для автономних одиниць» · entities/move · 🌱.
  - `+follower-modes` «Глобальний режим поведінки натовпу» · entities/move · 🥉.
  - `+world-code-progression` «Наступний рівень і його код — за результатом» · levels/progression · 📎 (?).

## Пропозиції до словників
- `+card:vertex-heightmap`, `+card:flat-area-building`, `+card:god-powers`, `+card:rally-magnet`, `+card:follower-modes` — див. вище.
- `+effect:raise` — підняти/опустити рельєф (підтвердження наявної пропозиції); `+cond:height_diff` — різниця висот сусідів (підтвердження).
- `+cond:flat_area` — довкола клітини пласка площа ≥ N.
- `+ui:mana-slider` — шкала сили бога з позначками порогів сил; `+ui:command-icons` — панель глобальних наказів.

## Джерела
- ⭐ [Wikipedia: Populous](https://en.wikipedia.org/wiki/Populous_(video_game)) — підняття землі для пласких ділянок, більша площа → більший дім, мана і сили, 500 рівнів, ландшафти, доповнення, платформи.
- [Мануал 1989 (скан, PDF)](https://ts.popre.net/archive/Downloads/Docs/Populous_1989_Manual.pdf) — бачив лише фрагмент у пошуку: хатини на 1–2 ділянках, замок — велика площа, Papal Magnet + режим «до магніту» → «поселитися», лицар незалежний. Файл завеликий для читання.
- YouTube: пошук «Populous 1989 gameplay».

## Непевне
- (?) Точна кількість рівнів поселень (≈9 від намету до замку) і площа замку (≈5×5) — з памʼяті.
- (?) Підтягування сусідів при піднятті (схил ≤1), обмеження «піднімати лише біля своїх», вода = рівень 0 — з памʼяті.
- (?) Злиття послідовників з сумуванням сили, захоплення будинку після бою, щит, «знайти лідера», пароль-імʼя світу, вибір наступного світу за рахунком — з памʼяті.
- (?) Порядок сил (земля, магніт, землетрус, болото, лицар, вулкан, повінь, Армагеддон) і опції Custom game — з памʼяті; Wikipedia підтверджує лише землетрус, повінь, болото, вулкан, лицаря.
- (?) 2-player через модем/кабель — Wikipedia каже лише «multiplayer».
