---
title: Tiny Metal
slug: tiny-metal
aka: [TINY METAL, "Tiny Metal: Full Metal Rumble"]
family: tactics
also: [build-sim]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: none
  goal: state
year: 2017
platforms: [PC, PS4, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tiny_Metal", best: true, note: "розробник Area 35, натхнення Advance Wars, дати, сиквел Full Metal Rumble, Tiny Metal 2"}
  - {kind: steam, url: "https://store.steampowered.com/app/751500/TINY_METAL/", note: "Focus Fire, фланг ззаду/збоку, Assault, герої з орбітальних кораблів, 15–16 юнітів, бонуси ландшафту"}
  - {kind: other, url: "https://www.destructoid.com/review-tiny-metal/", note: "огляд: Focus Fire (lock on), Advance/Assault, снайпер лише по піхоті, обовʼязковий туман, 50+ skirmish-мап"}
  - {kind: other, url: "https://www.pocketgamer.com/tiny-metal/review/", note: "огляд: радари бачать у тумані, податки з міст, камінь-ножиці-папір"}
  - {kind: other, url: "https://www.gamereactor.eu/tiny-metal-review/", note: "огляд: густий туман, блокування заводу юнітом, 56 skirmish-місій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tiny+Metal+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, legal-move-highlight, melee-vs-ranged, hp-damage, round-currency, destroy-all-enemies, interaction-table, fog-of-war, unit-xp-skills, ai-opponent, online-multiplayer, save-game, +capture-property, +unit-production, +terrain-bonus, +damage-matrix, +focus-fire, +assault-displace, +flank-bonus, +radar-reveal, +hero-units, +production-block, +retaliation]
proposes: ["+effect:focus_fire", "+effect:assault", "+effect:counterattack", "+effect:capture", "+effect:produce", "+cond:flanked", "+role:property", "+role:hero-unit", "+ui:lock-on-markers", "+window:production"]
author: opus
date: 2026-11-09
---

# Tiny Metal — Advance Wars з командою «Focus Fire»: кілька юнітів бʼють одну ціль, ворог відповідає лише одному

## Суть
Пряма спадкоємиця Advance Wars ([advance-wars](advance-wars.md)): квадратна карта, захоплення будівель піхотою, податки з міст, виробництво юнітів на заводах, камінь-ножиці-папір між типами. Відмінності: **Focus Fire** (lock on) — кілька юнітів призначають ціль і атакують разом, тож контратаку отримує лише один; **Assault** — атака з витісненням захисника з клітини; бонус за удар **збоку і ззаду**; **туман війни обовʼязковий** на всіх картах; герої-юніти замість командирів із силою. Тут описано лише різницю — спільне з AW див. у її файлі.

## Поле і час
- Квадратна сітка; ліси, міста, заводи дають бонуси ландшафту; ландшафт і будівлі не руйнуються.
- Хід сторони: усі юніти ходять у довільному порядку (як AW).
- Туман війни **завжди**: видно кілька клітин від юнітів; ворог часто помітний лише поруч; радарні станції/радар-юніти відкривають туман.
- Юніти мають напрямок (?) — від нього залежить фланговий бонус.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Rifleman (піхота) | piece | — | захоплює будівлі |
| RPG-піхота | piece | — | контрить броньовані машини |
| Sniper | piece | гібрид прямого/непрямого вогню | бʼє **лише піхоту** |
| Броньована розвідмашина | piece | — | сильна проти піхоти, слабка проти RPG |
| Tank / Metal | piece | міцні | основна сила; Metal — важкий робот-танк (?) |
| Artillery (непрямий) | piece | змінена форма зони атаки | або рух, або постріл |
| Radar (юніт) | piece | без зброї | розкриває туман |
| Gunship та інші повітряні | piece | — | виробляються у вежі-аеропорту |
| Герой | piece | XP, переносяться між місіями | посилена версія звичайного юніта, ростe по кампанії |
| HQ | static | — | захоплення → перемога |
| Місто | static | податок | дохід за хід |
| Завод (склад) / Вежа | spawner | — | наземні / повітряні юніти; ворожий юніт на ньому блокує виробництво |
| Радарна станція / обсерваторія | static | — | видимість у тумані; відкриває героїв |
| Прихована лабораторія | pickup | — | у кампанії: нагорода за дослідження мапи |
| Ліс, місто, завод (ландшафт) | terrain | бонус | захист / прихованість |

## Правила (КОЛИ → ЯКЩО → ТО)
Спільне з AW (захоплення, дохід, виробництво, прямий/непрямий вогонь, контратака) — у [advance-wars](advance-wars.md). Відмінні правила:
- КОЛИ `input(lock_on, unit, target)` → ЯКЩО `in_range(unit, target, n)` → ТО `custom: «юніт стає в чергу атаки на ціль, не стріляючи»`.
- КОЛИ `input(focus_fire, target)` → ЯКЩО `count(locked_on(target), ≥, 2)` → ТО `custom: «усі призначені атакують по черзі»`, `damage(n)` кожен; `custom: «ціль контратакує лише одного (першого)»`.
- КОЛИ `input(assault, target)` → ЯКЩО `adjacent(unit, target)` → ТО `custom: «захисник стріляє першим»`; якщо атакуючий вижив → `damage(n)`, `custom: «захисника витіснено з клітини, атакуючий займає її»`.
- КОЛИ `input(fire, target)` → ЯКЩО `custom: «атакуючий збоку або ззаду від цілі»` → ТО `custom: «+шкода»`.
- КОЛИ `input(fire, target)` для Sniper → ЯКЩО `not state(target, infantry)` → ТО `block`.
- КОЛИ `turn_start(side)` → ТО `reveal(cells)` у радіусі зору юнітів і радарів; решта → `hide(cells)`.
- КОЛИ `input(move, unit, cell)` → ЯКЩО `custom: «шлях у тумані»` → ТО `custom: «рух лише на 1 клітину в туман»` (?).
- КОЛИ `occupied(enemy_factory, unit)` → ТО `custom: «ворог не може виробляти на цій будівлі»` (без захоплення).
- КОЛИ `custom: «захоплено радар/обсерваторію»` → ТО `unlock(hero)`; `input(deploy, hero)` → `spawn_at(hero, cell)` (з орбітального корабля).
- КОЛИ `died(enemy)` від юніта → ТО `custom: «XP юніту, ріст сили»`.
- КОЛИ `all_gone(enemy_units)` → ТО `win`; КОЛИ `set_side(enemy_HQ, player)` → ТО `win`.
- Поразка: втрачено HQ / усі юніти · Рахунок: —.

## Керування і ввід
- Курсор / миша: юніт → зона руху → клітина → меню дій: Attack · Lock On · Assault · Capture · Wait (?).
- Lock On ставить маркер на цілі; Focus Fire з меню цілі запускає всі призначені атаки.
- Порожня клітина → загальне меню (кінець ходу, збереження майже будь-коли).
- Сутичка показується короткою анімацією (можна пропустити) (?).

## Вікна, меню, HUD
- `main-menu`: Campaign · Skirmish · Multiplayer · Options → `settings-window`.
- `level-select` (кампанія по місіях) і `match-setup` для skirmish (мапа, 2–4 армії, ШІ).
- `game-screen`: карта, `fog-overlay`, `threat-range`, HP на юнітах, маркери lock on, панель ландшафту, `turn-indicator`, гроші.
- `custom-window` «Production» — купівля юнітів на заводі/вежі.
- `dialogue-window` — сюжетні діалоги (англ. текст, японська озвучка).
- `end-screen` — перемога/поразка місії.
- `save-slots` — збереження посеред місії.

## Фічі поза полем
- Кампанія ~10–20 год зі сюжетом; герої й досвід переносяться між місіями.
- Skirmish: 50+ мап проти ШІ (2–4 армії); `online-multiplayer` 1×1 доданий патчем після релізу.
- New Game+.
- Чотири фракції — косметично однакові.
- Сиквел Full Metal Rumble (2019): DLC-кампанії; Tiny Metal 2 — анонсовано.

## Варіації й родичі
- Батько: [advance-wars](advance-wars.md); брати: [wargroove](wargroove.md) (командир-юніт на полі), [nectaris](nectaris.md) (бонус оточення сусідами), [battle-for-wesnoth](battle-for-wesnoth.md).
- **Осі варіацій** (у сімʼї AW-подібних): групова атака — нема / оточення дає бонус (Nectaris) / явна Focus Fire з однією контратакою (Tiny Metal) · напрямок удару — байдуже / фланг і тил сильніші · туман — опція карти / завжди · командир — пасивний бонус + сила / юніт-герой.

## Цікавинки для курсу
- Focus Fire: черга призначених атак на одну ціль і контратака лише першому — 📎 (черга дій + правило відповіді).
- Assault: захисник бʼє першим, потім витіснення на сусідню клітину — 📎.
- Фланговий бонус залежно від сторони удару відносно цілі — 🌱.
- Блокування ворожого заводу юнітом без захоплення — 🌱.
- Обовʼязковий туман + радари як джерела зору — 🥉 (кілька джерел видимості).

## Мапа на каталог
- Є: `piece-move-patterns` · `legal-move-highlight` · `melee-vs-ranged` · `hp-damage` · `round-currency` (податки) · `destroy-all-enemies` · `interaction-table` (камінь-ножиці-папір) · `fog-of-war` · `unit-xp-skills` (герої, досвід) · `ai-opponent` · `online-multiplayer` · `save-game`.
- **Нема** → пропозиції карток:
  - `+focus-fire` «Групова атака з однією контратакою» · entities/combat · 📎.
  - `+assault-displace` «Атака з витісненням захисника» · entities/combat · 📎.
  - `+flank-bonus` «Бонус шкоди за удар збоку/ззаду» · entities/combat · 🌱 (родич `+facing-hit-bonus` у корпусі).
  - `+radar-reveal` «Будівля/юніт-джерело зору в тумані» · interface/render · 🌱.
  - `+hero-units` «Іменні посилені юніти, що переносяться між місіями» · entities/state · 📎.
  - `+production-block` «Юніт на ворожому заводі блокує виробництво» · game-logic/economy · 🌱.
  - `+capture-property` / `+unit-production` / `+terrain-bonus` / `+damage-matrix` / `+retaliation` — спільні з Advance Wars і корпусом.

## Пропозиції до словників
- `+effect:focus_fire` — запустити всі призначені на ціль атаки; `+effect:assault` — атака з витісненням.
- `+effect:counterattack` — відповідь захисника (вже просять AW і інші); `+effect:capture` / `+effect:produce` — як у AW.
- `+cond:flanked` — атакуючий збоку/ззаду відносно напрямку цілі.
- `+role:property` — будівля з власником; `+role:hero-unit` — іменний юніт, що переходить між місіями.
- `+ui:lock-on-markers` — позначки призначених атак на цілі.
- `+window:production` — купівля юнітів.

## Джерела
- ⭐ [Wikipedia: Tiny Metal](https://en.wikipedia.org/wiki/Tiny_Metal) — Area 35, натхнення AW і Warhammer 40k, реліз 21.12.2017 (PS4/Switch/PC), Full Metal Rumble (2019), Tiny Metal 2.
- [Steam](https://store.steampowered.com/app/751500/TINY_METAL/) — Focus Fire, атаки ззаду/збоку, Assault, герої з орбітальних кораблів, 15/16 юнітів, бонуси ландшафту, skirmish, онлайн PvP.
- [Destructoid](https://www.destructoid.com/review-tiny-metal/) — механіка lock on / Focus Fire і Advance (Assault), снайпер, непрямі юніти, обовʼязковий туман, приховані лабораторії, New Game+.
- [Pocket Gamer](https://www.pocketgamer.com/tiny-metal/review/) — радари в тумані, податки з міст, приклад «розвідмашина vs піхота vs RPG».
- [Gamereactor](https://www.gamereactor.eu/tiny-metal-review/) — густий туман, блокування заводу, герої з обсерваторії, 56 skirmish-місій.
- YouTube: пошук «Tiny Metal gameplay».

## Непевне
- (?) Чи є випадковість у шкоді — джерела мовчать; `random: none` — припущення.
- (?) Точна механіка Assault: «захисник бʼє першим, потім витіснення» — з одного огляду (Destructoid).
- (?) Чи мають юніти напрямок (facing), чи фланг рахується за позицією відносно попередньої атаки — не перевірено.
- (?) Героїв відкриває радар чи обсерваторія — огляди різняться (можливо, одна будівля).
- (?) «Рух лише на 1 клітину в туман» — з переказу огляду в пошуку, не з першоджерела.
- (?) Повний список юнітів (Metal, Gunship тощо) і назви пунктів меню — з памʼяті/Steam-опису.
- (?) Тривалість кампанії: Steam — 20 год, Destructoid — 10–15.
