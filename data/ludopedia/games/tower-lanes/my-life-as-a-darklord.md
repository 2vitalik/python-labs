---
title: "Final Fantasy Crystal Chronicles: My Life as a Darklord"
slug: my-life-as-a-darklord
aka: [My Life as a Darklord, FFCC Darklord, "光と闇の姫君と世界征服の塔 FFCC", Hikari to Yami no Himegimi to Sekai Seifuku no Tō]
family: tower-lanes
also: []
klass: cursor
axes:
  field: layers
  time: realtime
  opponent: ai
  info: partial
  random: none
  goal: survive
year: 2009
platforms: [Wii (WiiWare)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Final_Fantasy_Crystal_Chronicles:_My_Life_as_a_Darklord", best: true, note: "вид збоку, поверхи з ефектами, артефакт поверху, Negative Power, Karma, тріада ближній/дальній/магія, DLC"}
  - {kind: other, url: "https://www.vgchartz.com/game/32951/final-fantasy-crystal-chronicles-my-life-as-a-darklord/reviews/4780/", note: "огляд: 4 місця на поверсі, артефакт як монстр, 10 монстрів = 5 типів × 2, один авантюрист на поверх, керування"}
  - {kind: other, url: "https://gameyum.com/final-fantasy-chronicles/44099-ffcc-final-fantasy-crystal-chronicles-my-life-as-a-darklord-review", note: "огляд: типи авантюристів, NP, Karma (+5 поверхів), побічні шляхи, сувої заклять, довідка на «−»"}
  - {kind: other, url: "https://tech-gaming.com/dlc-darklord-style-my-life-as-a-darklord-reviewed", note: "огляд: старт лише з верхнього поверху, вставка поверхів між наявними, пропуск зайнятих поверхів"}
  - {kind: other, url: "https://kotaku.com/final-fantasy-crystal-chronicles-my-life-as-a-darklord-5330810", note: "мікроогляд: 10–30 героїв на рівень, фінальний бос"}
  - {kind: other, url: "https://www.rpgsite.net/review/2855-final-fantasy-crystal-chronicles-my-life-as-a-darklord-review", note: "огляд: втрата артефакту руйнує поверх, Karma, керування Wii Remote боком"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=My+Life+as+a+Darklord+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [tower-placement, enemy-waves, enemy-reached-base, hp-damage, melee-vs-ranged, status-effects, round-currency, in-round-upgrades, level-unlock, world-map, map-window, save-autosave, game-pause, help-window, tutorial-window, +lane-grid, +floor-ascend, +floor-capacity, +insert-floor, +floor-core-artifact, +skip-occupied-floor, +damage-type-wheel, +no-refund-placement, +karma-meta, +spell-scroll, +side-path-stages]
proposes: ["+role:floor", "+effect:collapse_floor", "+cond:type_beats", "+card:skip-occupied-floor"]
author: opus
date: 2026-11-09
---

# My Life as a Darklord — TD збоку: вежа з поверхів, авантюристи лізуть угору, артефакт тримає поверх

## Суть
Міра, донька Темного лорда, захищає вежу, на вершині якої **Темний кристал** з душею батька. Гравець будує поверхи (кожен — зі своїм типом-ефектом), садить на них монстрів, а авантюристи групами піднімаються знизу вгору, поверх за поверхом. На кожному поверсі стоїть **артефакт**: знищили його — поверх руйнується разом з усім, що на ньому. Ядро — тріада типів (ближній / дальній / магія) і порядок поверхів, а не лабіринт.

## Поле і час
- Поле — **вертикальний стос поверхів** (вид збоку); кожен поверх — горизонтальна «смуга», яку авантюрист проходить лінійно. На поверсі **4 місця**, щонайменше одне займає артефакт.
- Рівень починається лише з верхнього поверху; нові поверхи можна вставляти й **між уже збудованими**. Максимум поверхів обмежений (старт — 5, кожне розширення за Karma +5).
- Real-time: хвилі авантюристів ідуть, поки гравець будує; бій на поверсі автоматичний і триває час, залежний від статів. Відкрите меню ставить гру на паузу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Темний кристал | static | — | верх вежі; авантюрист дійшов — поразка |
| Поверх | zone (`+role:floor`) | тип: offensive / defensive / support / special; 4 місця | дає бонуси своїм монстрам або шкодить/накладає статуси на авантюристів, що проходять |
| Артефакт поверху | ally | HP, здібності «як у монстра» | займає місце; знищено — поверх руйнується |
| Монстр ближнього бою | ally | HP, шкода, рівень | сильний проти дальніх, слабкий проти магії |
| Монстр дальнього бою | ally | HP, шкода, рівень | сильний проти магії, слабкий проти ближніх |
| Монстр-маг | ally | HP, шкода, рівень | сильний проти ближніх, слабкий проти дальніх |
| Монстр-цілитель | ally | — | лікує своїх на поверсі; без переваг і слабкостей |
| Загальний (generic) монстр | ally | — | без переваг і слабкостей |
| Пастка | hazard | — | шкодить авантюристу на поверсі |
| Авантюрист (5 типів) | enemy | тип, стати | лізе вгору; бʼється на поверсі; зайнятий іншим авантюристом поверх пропускає |
| Іменований бос | boss | сильніші здібності | наприкінці «замкових» етапів; фінальний бос |
| Negative Power (NP) | resource | — | валюта рівня: за кожного зваленого авантюриста |
| Karma | resource | — | за пройдений рівень; витрачається між рівнями |
| Сувій закляття | pickup | 1 раз на етап | додаткова шкода ворогам; нагорода побічного шляху |
| Предмет | pickup | — | з меню: атака або +NP на старті (частина — DLC) |
| Тонберрі | neutral | — | провідник Міри; без механіки на полі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «лише верхній поверх із кристалом; стартовий запас NP; монстрів і пасток із минулого рівня нема»`.
- КОЛИ `input(build_floor, position)` → ЯКЩО `counter(np, >=, cost)` and `count(floor, <, max_floors)` → ТО `place(player, floor)`, `currency(-cost)`; позиція — будь-яка, і між наявними поверхами.
- КОЛИ `input(summon, monster, slot)` → ЯКЩО `free(slot)` and `counter(np, >=, cost)` → ТО `place(player, monster)`, `currency(-cost)`; прибрати поставлене не можна, NP не повертається.
- КОЛИ `input(upgrade, monster)` → ЯКЩО `counter(np, >=, cost)` → ТО `custom: «рівень +1: шкода й HP, інколи нова здібність»`, `currency(-cost)`.
- КОЛИ `wave_start` → ТО `spawn_at(adventurer, bottom)` (поодинці або групою).
- КОЛИ `custom: «авантюрист готовий іти вище»` → ЯКЩО `occupied(next_floor, adventurer)` → ТО `custom: «пропускає зайнятий поверх»`; інакше `move(adventurer, up)`.
- КОЛИ `enter(adventurer, floor)` → ТО `custom: «автобій із монстрами поверху; тривалість — за статами»`.
- КОЛИ `enter(adventurer, offensive_floor)` → ТО `damage(adventurer, n)` або `set_state(adventurer, status)`.
- КОЛИ `tick` → ЯКЩО `cell(floor, defensive|support)` → ТО `set_state(monsters_on_floor, buff)`.
- КОЛИ `contact(attacker, target)` → ЯКЩО `custom: «тип атакера перемагає тип цілі: ближній > дальній > магія > ближній»` → ТО `damage(target, n)` з бонусом; інакше `damage(target, n)`.
- КОЛИ `tick` → ЯКЩО `count(healer_on_floor, >=, 1)` → ТО `heal(allies_on_floor, n)`.
- КОЛИ `hp_zero(adventurer)` → ТО `disappear(adventurer)`, `currency(+np)`.
- КОЛИ `hp_zero(artifact)` → ТО `custom: «поверх руйнується: усі монстри й пастки поверху зникають»`, `clear_state(floor, effects)`, авантюрист іде вище.
- КОЛИ `reach(adventurer, dark_crystal)` → ТО `lose`.
- КОЛИ `all_gone(adventurer)` → ЯКЩО `custom: «остання хвиля етапу»` → ТО `win`, `counter(karma, +n)`, `unlock(new_monster|floor|spell|item)`.
- КОЛИ `custom: «поразка»` → ЯКЩО `counter(defeated_adventurers, >=, 1)` → ТО `counter(karma, +part)`.
- КОЛИ `input(spend_karma, tower_size)` → ТО `counter(max_floors, +5)`; КОЛИ `input(spend_karma, monster)` → ТО `custom: «вища стартова сила монстра»`.
- КОЛИ `input(cast, scroll)` → ЯКЩО `first_time` → ТО `damage(adventurers, n)`.
- КОЛИ `input(open_menu)` → ТО `custom: «пауза»`; КОЛИ `input(use, item)` → ТО `use(player, item)`.
- Перемога: пережити всі хвилі етапу (10–30 героїв) · Поразка: авантюрист дійшов до кристала · Рахунок: нема; прогрес — Karma і розблокування.

## Керування і ввід
- Wii Remote **боком**, як NES-контролер: хрестовина — навігація по меню й поверхах, «2» — вибрати, «1» — назад; вказівник і рух не використовуються.
- «−» — довідка: поради, таблиця типів, статуси.
- Поставити поверх / монстра — через меню з паузою; «будувати на ходу» між хвилями.

## Вікна, меню, HUD
- `game-screen`: вежа збоку, поверхи з місцями, лічильник NP (`coins`), авантюристи на поверхах, `remaining-counter` героїв етапу; кут з Мірою, що коментує.
- `map-window`: вибір етапу на мапі; замки, побічні шляхи (складніші, нагорода — монстр або сувій).
- `upgrade-window`: витрата Karma — розмір вежі, стартова сила монстрів.
- `help-window` (кнопка «−»): поради, таблиця типів, статуси.
- `pause-menu` (будь-яке меню): будівництво, призов, апгрейд, предмети.
- `tutorial-window`: перші два етапи — навчання, можна пропустити (тоді старт з етапу 3 з одним типом поверху й одним монстром).
- `dialogue-window`: сюжетні сцени; `end-screen` етапу.
- Переходи: `map-window` → `game-screen` → `end-screen` → `upgrade-window` / `map-window`; автозбереження після етапу.

## Фічі поза полем
- `meta-progression`: Karma між рівнями (розмір вежі, стати монстрів); частина Karma зберігається й після поразки.
- `level-unlock` і `world-map`: нелінійна мапа з побічними шляхами; нові монстри, поверхи, закляття й предмети за перемоги.
- `autosave` після кожного етапу; одна складність; частина етапів — платні DLC або відкриваються після фіналу.
- DLC (14 пакетів на старті): костюми Міри, нові монстри й поверхи, предмети на NP, пакет заклять, персонажі FF IV: The After Years (Kain, Palom) як монстри.

## Варіації й родичі
- Попередник — FFCC: My Life as a King (2008, будівництво міста, не TD).
- Родичі в корпусі: [monster-train](monster-train.md) (вороги піднімаються поверхами, ядро нагорі), [dungeon-warfare](dungeon-warfare.md) і [orcs-must-die](orcs-must-die.md) (пастки проти «героїв»), [dungeon-keeper](dungeon-keeper.md) (ти — лиходій, герої вторгаються).
- **Осі варіацій**: вісь шляху — горизонтальний лабіринт / **вертикальний стос поверхів**; що тримає ділянку — HP бази / **артефакт поверху** (локальне «ядро»); черговість — усі вороги одночасно / **один авантюрист на поверх, решта перескакує**.

## Цікавинки для курсу
- Поверх як смуга з локальним ядром-артефактом: смерть ядра стирає вміст поверху — 📎.
- Правило «зайнятий поверх перескакують» — черга з обходом зайнятих слотів — 📎.
- Тріада типів із бонусом шкоди + нейтральні цілителі/загальні — 🌱 (таблиця множників).
- Вставка поверху між наявними (вставка у список, перерахунок порядку) — 🌱.
- Мета-валюта Karma, що частково лишається після поразки — 📎.

## Мапа на каталог
- Є: `tower-placement` · `enemy-waves` · `enemy-reached-base` · `hp-damage` · `melee-vs-ranged` · `status-effects` · `round-currency` (NP) · `in-round-upgrades` · `level-unlock` · `world-map` · `map-window` · `save-autosave` · `game-pause` · `help-window` · `tutorial-window`.
- **Нема** → пропозиції карток:
  - `+skip-occupied-floor` «Зайнятий поверх перескакують» · entities/move · 📎 — один ворог на смугу, наступні йдуть вище.
  - `+floor-core-artifact` «Локальне ядро поверху» · game-logic/win · 📎 — знищено → поверх і все на ньому зникає.
  - `+insert-floor` «Вставити поверх між наявними» · entities/legality · 🌱.
  - `+damage-type-wheel` (тріада), `+floor-ascend`, `+floor-capacity`, `+lane-grid` — як у [monster-train](monster-train.md).
  - `+no-refund-placement`, `+karma-meta`, `+spell-scroll`, `+side-path-stages` — 🌱.

## Пропозиції до словників
- `+role:floor` — поверх-смуга з власним типом і місткістю (Darklord, Monster Train).
- `+effect:collapse_floor` — поверх руйнується з усім вмістом (сутності, стани).
- `+cond:type_beats(a, b)` — тип A має перевагу над типом B (тріада, «камінь-ножиці-папір»).
- `+card:skip-occupied-floor` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Final_Fantasy_Crystal_Chronicles:_My_Life_as_a_Darklord) — жанр, вид збоку, поверхи з ефектами, артефакт, NP, Karma, тріада, DLC, дати.
- [VGChartz, огляд](https://www.vgchartz.com/game/32951/final-fantasy-crystal-chronicles-my-life-as-a-darklord/reviews/4780/) — 4 місця, артефакт, 10 монстрів, пропуск зайнятих поверхів, керування, мапа етапів.
- [GameYum, огляд](https://gameyum.com/final-fantasy-chronicles/44099-ffcc-final-fantasy-crystal-chronicles-my-life-as-a-darklord-review) — 5 типів авантюристів, NP, Karma (+5 поверхів), побічні шляхи, «−»-довідка, автосейв.
- [Tech-Gaming](https://tech-gaming.com/dlc-darklord-style-my-life-as-a-darklord-reviewed) — старт з одного поверху, вставка поверхів, DLC.
- [RPG Site](https://www.rpgsite.net/review/2855-final-fantasy-crystal-chronicles-my-life-as-a-darklord-review) · [Kotaku](https://kotaku.com/final-fantasy-crystal-chronicles-my-life-as-a-darklord-5330810) — колапс поверху, 10–30 героїв, фінальний бос.

## Непевне
- (?) Конкретні типи поверхів (назви, що саме дають) — джерела називають лише 4 категорії (offensive/defensive/support/special).
- (?) Напрям тріади: два огляди — «магія > ближній > дальній > магія»; Wikipedia лише каже, що три категорії мають бонус одна проти одної.
- (?) Чи пастки — окремий тип місця, чи властивість offensive-поверху; чи артефакт атакує сам.
- (?) `random: none` — випадковості в описах нема; склад хвиль заздалегідь відомий лише як кількість і загальний клас.
