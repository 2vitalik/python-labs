---
title: Unstoppable Gorg
slug: unstoppable-gorg
aka: [Gorg]
family: tower-lanes
also: []
klass: cursor
axes:
  field: graph
  time: realtime
  opponent: ai
  info: partial
  random: none
  goal: survive
year: 2012
platforms: [PC, Mac, iPad]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Unstoppable_Gorg", best: true, note: "орбіти зі слотами навколо бази, поворот орбіти зсуває всі її супутники, озброєні й неозброєні супутники"}
  - {kind: steam, url: "https://store.steampowered.com/app/18120/Unstoppable_Gorg/", note: "40+ рівнів, супутники замість веж і сітки, лідерборди, демо"}
  - {kind: other, url: "https://www.pocketgamer.com/unstoppable-gorg/review", note: "огляд iPad: концентричні кільця, фіксовані слоти, поворот на 360°, research tokens"}
  - {kind: other, url: "https://destructoid.com/?p=122678", note: "огляд: типи супутників (ресурсні, гармати, Space Ray, дослідницькі), Gorg / Sunbots / Brain Riders, орбіти фіксовані й самохідні"}
  - {kind: other, url: "https://gamingnexus.com/Article/3343/Unstoppable-Gorg", note: "огляд: 18 супутників, ремонт і рівні, медалі досліджень, Story / Challenge / Arcade"}
  - {kind: other, url: "https://www.honestgamers.com/9929/pc/unstoppable-gorg/review.html", note: "огляд: маршрути показані лініями, вибір загону, отруйні хмари, складності"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Unstoppable+Gorg+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [tower-placement, tower-range, enemy-waves, spawn-points, spawner-entity, enemy-reached-base, hp-damage, round-currency, in-round-upgrades, speed-per-type, row-conveyor, path-preview, difficulty-levels, level-select, level-unlock, mode-select, codex-window, leaderboard, +orbit-slots, +ring-rotate, +damage-type-wheel, +income-tower, +repair-tower, +research-points, +reassignable-upgrades, +loadout-select, +level-objectives, +game-speed-toggle, +endless-arcade]
proposes: ["+effect:upgrade", "+effect:income", "+role:slot", "+role:base", "+cond:damage_type", "+ui:research-bar", "+ui:orbit-handle", "+window:loadout-select", "+axis:field=polar"]
author: opus
date: 2026-11-09
---

# Unstoppable Gorg — tower defense на орбітах: супутники в слотах кілець навколо бази, поворот кільця зсуває їх усі

## Суть
TD від Futuremark у стилі sci-fi 1950-х: у центрі екрана — база (станція, місяць, планета), навколо — концентричні орбіти з фіксованими слотами. Гравець купує супутники в слоти, а замість перебудови **повертає кільце**: усі супутники орбіти разом переїжджають до нового напрямку атаки. Вороги вилітають із материнських кораблів на краях екрана маршрутами, що змінюються між хвилями. Ядро — «поле як набір кілець-барабанів», де одна дія зсуває групу веж.

## Поле і час
- Полярне поле: кілька концентричних орбіт, на кожній ≥2 слоти з різним кроком (залежить від орбіти й рівня); вільної розстановки нема.
- Орбіти бувають: керовані (гравець крутить), заблоковані (не крутяться) і самохідні (обертаються постійно).
- Вороги летять вільно маршрутами від країв до центру; маршрути поточних хвиль показані лініями, нові додаються.
- Real-time з прискоренням часу (клавіша); супутники стріляють і під час обертання.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| База | static (`+role:base`) | HP | ціль ворогів; знищена → поразка |
| Орбіта | zone | слоти, стан: керована / заблокована / самохідна | обертається разом з усіма супутниками на ній |
| Слот орбіти | static (`+role:slot`) | позиція на кільці | місце під один супутник |
| Гармата (gun) | tower | фізична шкода, швидка й слабка | бʼє ворогів у радіусі |
| Cannon / Laser / Missile | tower | різна шкода | атакують у радіусі (деталі (?)) |
| Space Ray | tower | енергетична шкода | ефективна проти Sunbots |
| Ресурсний (solar generator) | tower | дохід | генерує гроші; дорожчий на початку рівня |
| Дослідницький | tower | — | заповнює шкалу досліджень; займає слот і коштує гроші |
| Ремонтний | tower | радіус | лагодить інші супутники |
| Сповільнювач | tower | радіус | сповільнює ворогів поруч |
| Материнський корабель | spawner | край екрана | випускає хвилі; кілька одночасно |
| Gorg | enemy | вразливі до фізичної шкоди | летить маршрутом до бази |
| Sunbot | enemy | механічні | потребують енергетичної шкоди |
| Brain Rider | enemy | енергетичний щит | щит протистоїть Space Ray |
| Отруйна хмара / «нитки» ворогів | hazard | — | шкодять супутнику, що опинився в них |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `choose(обмежений набір супутників)`, `custom: «розподілити медалі досліджень на апгрейди»`.
- КОЛИ `input(buy, satellite, slot)` → ЯКЩО `has(money, cost)` and `free(slot)` → ТО `place(satellite, slot)`, `currency(-cost)`.
- КОЛИ `input(drag, orbit)` → ЯКЩО `not state(orbit, locked)` → ТО `rotate(orbit, deg)` — усі супутники орбіти переїжджають разом.
- КОЛИ `tick` → ЯКЩО `state(orbit, auto_spin)` → ТО `rotate(orbit, step)`.
- КОЛИ `wave_start` → ТО `spawn_at(ships, mothership)`, `custom: «маршрут хвилі показано лінією»`.
- КОЛИ `tick` → ТО `move(ship, along_route)`.
- КОЛИ `in_range(satellite, ship, r)` → ЯКЩО `custom: «cond damage_type: тип шкоди підходить цілі»` → ТО `damage(ship, n)`; інакше шкода слабка.
- КОЛИ `in_range(space_ray, brain_rider, r)` → ЯКЩО `state(brain_rider, shield)` → ТО `block`.
- КОЛИ `in_range(slower, ship, r)` → ТО `speed(ship, ×k)`.
- КОЛИ `in_range(repair, satellite, r)` → ТО `heal(satellite, n)`.
- КОЛИ `timer(every)` → ЯКЩО `occupied(slot, generator)` → ТО `currency(+n)`.
- КОЛИ `timer(every)` → ЯКЩО `occupied(slot, research_sat)` → ТО `counter(research_bar, +n)`; КОЛИ `counter(research_bar, ==, full)` → ТО `custom: «+1 research point на наступні рівні»`.
- КОЛИ `hp_zero(ship)` → ТО `disappear(ship)`, `currency(+bounty)`.
- КОЛИ `enter(satellite, poison_cloud)` → ТО `damage(satellite, n)`; КОЛИ `hp_zero(satellite)` → ТО `disappear(satellite)`.
- КОЛИ `input(upgrade, satellite)` → ЯКЩО `has(money, cost)` → ТО `custom: «effect upgrade: рівень супутника +1»`.
- КОЛИ `reach(ship, base)` → ТО `damage(base, n)`; КОЛИ `hp_zero(base)` → ТО `lose`.
- КОЛИ `all_gone(waves)` → ТО `win`, `custom: «медалі за цілі рівня (без шкоди, без втрат супутників)»`, `unlock(challenge_level)`.
- КОЛИ `custom: «режим Arcade»` → ТО `custom: «хвилі нескінченні, рахунок — у таблицю»`.
- Перемога: пережити всі хвилі рівня · Поразка: база знищена · Рахунок: медалі/цілі рівня; Arcade — найкращий рахунок у лідерборді.

## Керування і ввід
- Миша: вибрати супутник з панелі (або клавішею) → клік у вільний слот; клік по орбіті й обертання мишею — поворот кільця.
- Клавіша прискорення часу; майже миттєвий рестарт після поразки.
- iPad: ті самі дії дотиком.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Story / Challenge / Arcade; `difficulty-select`: easy / normal / challenge.
- `level-select` / `map-window`: рівні кампанії (станції, місяці, планети) й челенджі.
- `+window:loadout-select`: вибір обмеженого набору супутників і розподіл медалей досліджень перед рівнем.
- `game-screen`: база, кільця зі слотами, лінії маршрутів (`path-preview`), гроші, `+ui:research-bar`, `+ui:orbit-handle` (?), панель супутників.
- `codex-window`: енциклопедія персонажів, ворогів і спорядження, відкривається з прогресом.
- `dialogue-window`: чорно-білі відеоролики з акторами на початку й наприкінці рівнів.
- `leaderboard` Steam (Arcade); `end-screen` з медалями.

## Фічі поза полем
- `meta-progression`: медалі досліджень за рівні; **не постійні** — щоразу перерозподіляються між апгрейдами перед рівнем.
- `level-unlock`: добрий результат відкриває челендж-версію рівня (обмежені гроші, інше спорядження, самохідні або заблоковані орбіти).
- `mode-endless` (Arcade), `difficulty-presets`, `speed-control` (прискорення часу), досягнення Steam, хмарні збереження.

## Варіації й родичі
- Вісь «поле TD»: дорога + клітини ([plants-vs-zombies](plants-vs-zombies.md), [defense-grid](defense-grid.md)) → відкрите поле-лабіринт ([desktop-tower-defense](desktop-tower-defense.md), [gem-td](gem-td.md)) → **кільця зі слотами, що обертаються** (Gorg).
- Повороти як основна дія — рідні сімʼї `connect-rotate` (обертання кілець і плиток); у TD-сімʼї поруч [rampart](rampart.md) (будування між фазами) і [anomaly-warzone-earth](anomaly-warzone-earth.md) (обернений TD).
- **Осі варіацій**: розміщення веж — будь-де / клітини / фіксовані слоти · переміщення — продати й поставити / повернути кільце / самохідне кільце · типи шкоди — один / фізична + енергетична + щити.

## Цікавинки для курсу
- Полярне поле: орбіта як циклічний масив слотів, поворот = циклічний зсув на k — 🌱 (модель), 📎 (з плавною анімацією й стрільбою під час повороту).
- Самохідні й заблоковані орбіти як модифікатори рівня — 🌱.
- Типи шкоди × типи ворогів (фізична / енергетична / щит проти енергетичної) — 📎.
- Ресурсний і дослідницький супутник займають бойові слоти: економіка проти оборони — 📎.
- Медалі досліджень, що перерозподіляються перед кожним рівнем (не постійні апгрейди), — 🥉 (екран розподілу + застосування до старту рівня).
- Маршрути хвиль як лінії, що змінюються між хвилями, — 🌱.

## Мапа на каталог
- Є: `tower-placement` ↔ супутник у слот · `tower-range` · `enemy-waves` · `spawn-points` + `spawner-entity` ↔ материнські кораблі · `enemy-reached-base` · `hp-damage` · `round-currency` · `in-round-upgrades` ↔ рівні й ремонт супутників · `speed-per-type` · `row-conveyor` ↔ самохідна орбіта, що везе всі супутники · `path-preview` ↔ лінії маршрутів · `difficulty-levels` · `level-select` + `level-unlock` · `mode-select` · `codex-window` · `leaderboard`.
- **Нема** → пропозиції карток:
  - `+orbit-slots` «Поле з кілець і фіксованих слотів» · entities/legality · 📎 · слоти {rings, slots_per_ring}.
  - `+ring-rotate` «Поворот кільця зсуває всі обʼєкти на ньому» · entities/move · 📎 · слот {step}.
  - `+damage-type-wheel` — уже пропонувалась (Element TD 2).
  - `+income-tower` «Вежа-генератор доходу в бойовому слоті» · game-logic/economy · 🌱.
  - `+repair-tower` «Вежа лагодить інші» · entities/combat · 🌱.
  - `+research-points` «Окрема шкала досліджень у рівні → очки апгрейдів» · game-logic/economy · 📎.
  - `+reassignable-upgrades` «Апгрейди перерозподіляються перед рівнем» · game-logic/economy · 🥉.
  - `+level-objectives` «Додаткові цілі рівня (без шкоди, без втрат)» · game-logic/score · 🌱.
  - `+game-speed-toggle` «Прискорення часу» · game-logic/difficulty · 🌱.
  - `+endless-arcade` «Нескінченний режим з рекордом» · game-logic/waves · 🌱.
  - `+loadout-select` — уже пропонувалась (PvZ).

## Пропозиції до словників
- `+effect:upgrade`, `+effect:income` — підтвердження сімʼї.
- `+role:slot` — фіксоване місце під вежу (не клітина поля); `+role:base` — ціль ворогів у центрі (підтвердження Clash Royale).
- `+cond:damage_type` — тип шкоди атаки підходить / не підходить цілі.
- `+ui:research-bar` — шкала до наступного очка досліджень; `+ui:orbit-handle` — елемент повороту кільця.
- `+window:loadout-select` — підтвердження.
- `+axis:field=polar` — кільця й слоти як окремий тип поля (зараз `graph`).

## Джерела
- ⭐ [Wikipedia: Unstoppable Gorg](https://en.wikipedia.org/wiki/Unstoppable_Gorg) — орбіти зі слотами, поворот орбіти, озброєні й неозброєні супутники (гроші, ремонт, сповільнення), Futuremark, 2012, PC/Mac/iPad.
- [Steam](https://store.steampowered.com/app/18120/Unstoppable_Gorg/) — 40+ рівнів, супутники замість веж і сітки, перестановка між хвилями, лідерборди.
- [Pocket Gamer](https://www.pocketgamer.com/unstoppable-gorg/review) — концентричні кільця, фіксовані слоти, поворот на 360°, research tokens, складності.
- [Destructoid](https://destructoid.com/?p=122678) — типи супутників, Gorg / Sunbots / Brain Riders, фіксовані й самохідні орбіти, research bar, прискорення часу.
- [Gaming Nexus](https://gamingnexus.com/Article/3343/Unstoppable-Gorg) — 18 супутників, ремонт і рівні, медалі досліджень, Story 21 / Challenge 21 / Arcade, енциклопедія.
- [HonestGamers](https://www.honestgamers.com/9929/pc/unstoppable-gorg/review.html) — маршрути лініями, вибір загону, отруйні хмари, самохідні/заблоковані вузли, три складності.
- YouTube: [пошук «Unstoppable Gorg gameplay»](https://www.youtube.com/results?search_query=Unstoppable+Gorg+gameplay).

## Непевне
- (?) Розбіжність у кількості рівнів: Steam «40+», Gaming Nexus «21 story + 21 challenge».
- (?) Точні функції Cannon / Laser / Missile і решти з 18 супутників; чи сповільнювач — окремий тип.
- (?) Чи поворот орбіти безкоштовний і миттєвий, чи має швидкість; HP бази й супутників.