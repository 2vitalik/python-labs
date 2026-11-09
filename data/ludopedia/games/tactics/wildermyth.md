---
title: Wildermyth
slug: wildermyth
aka: []
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2021
platforms: [PC, macOS, Linux, Switch, PS4, PS5, Xbox One, Xbox Series]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wildermyth", best: true, note: "огляд: сітка, XCOM-подібний бій, кампанія, старіння, стосунки, комікс-подача, релізи"}
  - {kind: other, url: "https://wildermyth.com/wiki/Interfusion", note: "офіційна вікі: правила інтерфузії і таблиця 12 типів обʼєктів"}
  - {kind: other, url: "https://wildermyth.com/wiki/Combat_mechanics", note: "офіційна вікі: лінія видимості, укриття, формула влучання, броня/вардинг, Injury"}
  - {kind: other, url: "https://wildermyth.com/wiki/Grayplane", note: "офіційна вікі: стан Hidden (Grayplane) — вхід, ефект, зняття"}
  - {kind: other, url: "https://wildermyth.com/wiki/Hero", note: "офіційна вікі: рівні, XP, mortal choice, каліцтва, відставка, legacy"}
  - {kind: other, url: "https://wildermyth.com/wiki/Combat", note: "офіційна вікі: типи боїв, монстри з колоди calamity"}
  - {kind: steam, url: "https://store.steampowered.com/app/763890/Wildermyth/", note: "трансформації, legacy, кооп до 5, редактор, Workshop"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Wildermyth+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, melee-vs-ranged, line-of-sight-attack, destructible-blocks, unit-xp-skills, status-effects, inventory-items, world-map, map-window, difficulty-levels, online-multiplayer, in-game-editor, save-autosave, destroy-all-enemies, reinforcements, hover-highlight, reachable-highlight, threat-range, +hit-chance, +cover-system, +flanking, +concealment, +object-possession, +object-spell-table, +armor-shred, +mortal-choice, +hero-aging, +legacy-roster, +monster-deck, +fractional-range, +fire-spread]
proposes: ["+trigger:attacked", "+effect:interfuse", "+effect:withdraw", "+effect:shred", "+cond:interfused", "+cond:distance_le", "+role:interactable", "+ui:range-circle", "+ui:hit-chance", "+window:mortal-choice", "+window:comic-panel", "+window:legacy-window", "+feature:legacy-heroes", "+feature:mode-coop", "+feature:level-editor", "+axis:session"]
author: opus
date: 2026-11-09
---

# Wildermyth — сітковий бій, де маг «вселяється» в ліхтар, дерево чи камінь і стріляє ними

## Суть
Гравець веде загін героїв трьох класів (воїн, мисливець, містик) через процедурну кампанію: між боями — карта-мапа з територіями, у боях — покрокова тактика на квадратній сітці. Головна незвична механіка — **інтерфузія**: містик «вселяється» в обʼєкт поля (вогонь, камінь, рослину, метал, тканину…) і кастує заклинання, тип якого визначає матеріал обʼєкта; частина заклинань руйнує сам обʼєкт. Поле — набір матеріалів, а не просто перешкоди. Герої старіють, калічаться, змінюють тіло й переходять у наступні кампанії як «легенди».

## Поле і час
- Квадратна сітка; стіни й предмети дають укриття (Partial / Good), ями (crevasse) не блокують видимість.
- Відстані — **дробові** (радіус 4.6, лінія 5, «6 + Long Reach»): дальність рахується евклідово від центру клітини, а не в кроках.
- Хід за сторонами: фаза героїв (довільний порядок), потім фаза ворогів (?).
- Вороги приходять поступово — у бою-перехопленні «вся сила зазвичай на полі до 3-го ходу»; монстри беруться з колоди фракції.
- Інформація часткова: прихованих (Grayplane) героїв вороги не бачать; огляд обʼєкта-носія обмежений (7–8 клітин).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Воїн | piece | Health, Block, Armor, Accuracy, Bonus Damage | ближній бій, «охоронець загону» |
| Мисливець | piece | лук, Accuracy | дальній бій; Silkstep → Grayplane (невидимість) |
| Містик | piece | Potency, Warding, Spell Damage | інтерфузія з обʼєктами; до 2 активних носіїв |
| Обʼєкт-носій (Blaze, Bone, Lamp, Liquid, Plant, Metal, Shards, Stone, Textile, Tools, Wood) | object | матеріал, health (у частини), розмір 1+ клітин | дає містику заклинання свого типу; деякі руйнуються від використання |
| Вогонь (blaze) | hazard | — | палає; Fireleash і Splinterblast розносять вогонь |
| Пастка Sharktrap | hazard | — | пінить першого ворога, що стане, на 1 хід |
| Укриття (стіна, двері, предмет) | static | Partial до +30 / Good до +60 | додається до захисту, якщо ціль поруч (і по діагоналі); пошкоджується промахами |
| Монстр (картка calamity) | enemy | HP, броня, здібності | AI фракції; деякі мають Search (знімає Hidden у радіусі 2) |
| Бос / сила ворога | boss | — | сюжетні бої з власними умовами |
| Фермер (у обороні) | ally | — | щонайменше 2 у бою-обороні |
| Предмет спорядження | pickup | слот | змінює стати й здібності (напр., плащ Forestlord: раз за бій Hidden) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(heroes)` → ТО `custom: «кожен герой: рух і одна дія, що завершує його хід; swift-дії хід не завершують»` (?).
- КОЛИ `input(interfuse, mystic, obj)` → ЯКЩО `in_range(mystic, obj, 6)` and `custom: «активних носіїв < 2»` → ТО `custom: «interfuse — swift-дія, містик привʼязується до obj»`.
- КОЛИ `turn_start(mystic)` → ЯКЩО `custom: «відстань до носія > 8.0»` → ТО `custom: «інтерфузія рветься»`.
- КОЛИ `input(cast, mystic, obj, target)` → ЯКЩО `custom: «target у дальності, рахованій від obj»` → ТО `custom: «заклинання матеріалу obj; хід містика закінчується»`.
- Blaze → Fireleash: КОЛИ `input` → ТО `damage(line)` + `set_state(enemies_on_path, burn)` (половина шкоди по шляху, відкладений опік).
- Plant → Wild Grasp: ТО `damage(target)` + `pull(target)` до рослини + `set_state(target, pinned)`.
- Metal → Shackle: ТО `set_state(target, pinned, 2)` зі 100 % влучанням.
- Stone → Discus: ТО `damage(target)` + `custom: «рикошет у другу ціль на ½ шкоди»`.
- Tools → Barrage / Wood → Splinterblast: ТО `explode(area)` + `disappear(obj)`; Wood ще `spawn_at(fire, area)`.
- Lamp → Steal Fire: ТО `spawn_at(fire, cell)` + `transform(lamp, extinguished)`; Lamp → Flare: ТО `set_state(area, blind, 1)` + `damage(lamp)`.
- Shards → Sharktrap: ТО `place(mystic, trap)`; КОЛИ `enter(enemy, trap)` → ТО `set_state(enemy, pinned, 1)` + `disappear(trap)`.
- КОЛИ `custom: «атака»` → ТО `custom: «сила удару = Accuracy − (Block + Dodge + Cover); ≤ −75 — 0 %, 0 — 75 %, +40 — 100 %»`.
- КОЛИ `custom: «промах»` → ЯКЩО `custom: «сила удару < cover»` → ТО `damage(cover_object)`.
- КОЛИ `custom: «влучання»` → ТО `damage(target, n − Armor)` (магія — мінус Warding); ЯКЩО `custom: «броня звела шкоду до 0»` → ТО `custom: «shred: −1 броні до кінця місії»`.
- Walling: ЯКЩО `adjacent_count(hero, hero, >=, 1)` (ортогонально) → ТО `custom: «шкода по герою −1»` (не складається).
- Фланг: ЯКЩО `custom: «ціль затиснута між двома героями»` → ТО `custom: «фланговий бонус»`; інтерфузійні атаки теж флангують.
- КОЛИ `input(silkstep, hunter)` → ТО `set_state(hunter, hidden)` + `end_turn`; КОЛИ `custom: «hunter атакує або ворог атакує/проходить крізь нього»` → ТО `clear_state(hunter, hidden)`.
- ЯКЩО `state(attacker, hidden)` → ТО `custom: «атака ігнорує Armor і Warding»`.
- КОЛИ `hp_zero(hero)` → ТО `window(mortal-choice)`: `choose(загинути з бонусом загону | каліцтво й вихід з бою)`; каліцтво: рука → гак, нога → деревʼяна нога (`transform`).
- КОЛИ `all_gone(enemy)` → ТО `win`; КОЛИ `all_gone(hero)` на полі → ТО `lose` (?).
- Рахунок: XP — ~5 за картку монстра, ділиться між учасниками; рівні 1–7.

## Керування і ввід
- Клік по герою → підсвітка досяжних клітин → клік по клітині (рух) або по ворогу/обʼєкту (дія); прицільне вікно показує шанс і шкоду.
- Інтерфузія: обрати містика → обʼєкт у радіусі → панель заклинань обʼєкта (з кільцем дальності від обʼєкта).
- Між боями: перетягування героїв по територіях карти, призначення робіт (будувати, розвідувати, крафтити) (?).
- Кооп: кожен із до 5 гравців керує своїми героями.

## Вікна, меню, HUD
- `main-menu`: нова кампанія / продовжити / Legacy / редактор / налаштування.
- `character-select` — вибір із кількох випадкових стартових героїв.
- `map-window` — карта кампанії з територіями, містами, станціями, силами ворога.
- `game-screen` бою: сітка, `hp-bar` героїв, `hit-chance`, `range-circle` для заклинань, позначки укриття, `ability-buttons`.
- `mortal-choice` — вікно вибору «смерть / каліцтво».
- `comic-panel` — історії подаються коміксовими панелями з вибором відповіді.
- `upgrade-window` — при підвищенні: 3 випадкові здібності + апгрейд наявної.
- `inventory-window` (спорядження героя), `legacy-window` (пантеон героїв), `editor-window`, `settings-window`, `end-screen` глави.

## Фічі поза полем
- Процедурна кампанія з главами; кожна глава відкриває нові області карти; зростання загрози (calamity track) додає нові типи монстрів у колоду.
- Герої старіють і йдуть на пенсію (передають 3/8 XP молодшому або 3 Legacy Points); стосунки (дружба, суперництво, кохання).
- Трансформації (вовчий бог тощо) міняють вигляд і бойові здібності.
- `legacy-heroes`: герої переходять у наступні кампанії молодшими, з рівнем = тир легенди.
- `difficulty-presets`, `mode-coop` (онлайн/LAN до 5), `level-editor` + Steam Workshop, DLC Omenroad (роглайкова кампанія).

## Варіації й родичі
- XCOM (укриття, шанс влучання, фланги), Battle Brothers (кампанія + сітка, каліцтва), Banner Saga (доля героїв між боями), Into the Breach (поле як зброя).
- Осі варіацій:
  - **поле як ресурс**: перешкоди лише блокують (Fire Emblem) / руйнуються (XCOM) / є «боєприпасами» за матеріалом (Wildermyth);
  - **дальність**: кроки манхеттен (більшість) / Чебишев / дробова евклідова (Wildermyth);
  - **доля героя**: смерть / лічильник / вибір смерть-чи-каліцтво (Wildermyth);
  - **вороги**: фіксовані / з колоди, що росте з загрозою.

## Цікавинки для курсу
- Інтерфузія: таблиця «матеріал → заклинання» і обʼєкт як точка відліку дальності — 🥉 (data-driven здібності).
- Дробова евклідова дальність на квадратній сітці (`dist ≤ 4.6`) — 🌱, але показово: як «коло» лягає на клітини.
- Формула влучання: кусково-лінійна від різниці атаки й захисту — 📎.
- Укриття з частковою «експозицією» (5 точок стрільця × 5 точок цілі) — 🥈 (лінії видимості з нахилом).
- Броня і shred: якщо броня з'їла всю шкоду — знижується сама — 🌱.
- Колода монстрів, що росте з загрозою кампанії — 📎.
- Mortal choice + старіння + legacy: життєвий цикл героя між партіями — 🥉.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `line-of-sight-attack` · `destructible-blocks` ↔ обʼєкти руйнуються від заклинань · `unit-xp-skills` · `status-effects` (pinned, blind, hobble, burn) · `world-map`/`map-window` · `reinforcements` · `online-multiplayer` ↔ кооп · `in-game-editor` · `reachable-highlight`, `threat-range`.
- **Нема** → пропозиції карток:
  - `+object-possession` «Вселення в обʼєкт поля» · entities/combat · 🥉 · слоти {max_links: 2, range: 6, break_range: 8}.
  - `+object-spell-table` «Заклинання за матеріалом обʼєкта» · entities/combat · 🥉 · слот {table}.
  - `+armor-shred` «Знос броні» · entities/combat · 🌱.
  - `+mortal-choice` «Смерть чи каліцтво» · entities/death · 📎.
  - `+hero-aging` · `+legacy-roster` «Герої між кампаніями» · levels/progression · 📎.
  - `+monster-deck` «Вороги з колоди, що росте» · levels/spawn · 📎.
  - `+fractional-range` «Евклідова дальність» · entities/legality · 🌱.
  - `+fire-spread` «Поширення вогню» · entities/cells · 📎.
  - `+hit-chance`, `+cover-system`, `+flanking`, `+concealment` — як у XCOM.

## Пропозиції до словників
- `+trigger:attacked` — для знімання Hidden і реакцій (як у Wesnoth/XCOM).
- `+effect:interfuse(a, obj)` / `+effect:withdraw(a, obj)` — привʼязати/відвʼязати мага до обʼєкта.
- `+effect:shred(a, n)` — знизити броню до кінця місії.
- `+cond:interfused(a, obj)` — маг повʼязаний з обʼєктом; `+cond:distance_le(a, b, x)` — дробова відстань.
- `+role:interactable` — обʼєкт поля, що дає дію (носій інтерфузії).
- `+ui:range-circle` — кільце дальності від обʼєкта; `+ui:hit-chance`.
- `+window:mortal-choice`, `+window:comic-panel`, `+window:legacy-window`.
- `+feature:legacy-heroes`, `+feature:mode-coop`, `+feature:level-editor`; `+axis:session` = `campaign`.

## Джерела
- ⭐ [Wikipedia: Wildermyth](https://en.wikipedia.org/wiki/Wildermyth) — жанр, сітка, кампанія, старіння і стосунки, комікс-подача, DLC Omenroad, платформи.
- [Wildermyth Wiki: Interfusion](https://wildermyth.com/wiki/Interfusion) — swift-дія, радіус 6 + Long Reach, розрив > 8, ліміт 2, таблиця 12 заклинань.
- [Wildermyth Wiki: Combat mechanics](https://wildermyth.com/wiki/Combat_mechanics) — LOS з 5×5 точками, укриття +30/+60, формула шансу, Armor/Warding, shred, walling, Injury.
- [Wildermyth Wiki: Grayplane](https://wildermyth.com/wiki/Grayplane) — Hidden: вхід, ігнор броні, зняття, Search.
- [Wildermyth Wiki: Hero](https://wildermyth.com/wiki/Hero) — рівні Greenhorn…Blackhorn, пороги XP, mortal choice, каліцтва, відставка, legacy.
- [Wildermyth Wiki: Combat](https://wildermyth.com/wiki/Combat) — типи боїв (Assault, Defense, Ambush, Intercept), монстри з карток calamity.
- [Steam](https://store.steampowered.com/app/763890/Wildermyth/) — трансформації, кооп до 5, редактор, Workshop.

## Непевне
- (?) Точна структура ходу (рух + дія, swift-дії, подвійний рух) — сторінку правил ходу не відкрито, з памʼяті.
- (?) Величина флангового бонусу (лише модифікатор Cunning «+2 до флангових атак» бачив); правила Guard воїна не перевірено.
- (?) Умова поразки в бою (усі герої вибули / відступ) і правила поширення вогню.
- (?) Як саме росте загроза на мапі кампанії й коли починаються вторгнення (сторінки Threat/Calamity track не відкрились).
