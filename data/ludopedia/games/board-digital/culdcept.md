---
title: Culdcept
slug: culdcept
aka: [カルドセプト, Culdcept The First]
family: board-digital
also: [tower-lanes]
klass: hybrid
axes:
  field: graph
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: race
year: 1997
platforms: [Saturn, PlayStation, Dreamcast, PS2, Xbox 360, DS, 3DS, PSP, PS3, Switch, PS5, PC]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/カルドセプト", best: true, note: "JA-вікі: поле, замок і форти, ланцюги, рівні земель, формули вартості, бій, магія, умови перемоги"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Culdcept", note: "EN-вікі: ядро гри, книга 50 карт, мито/бій, перелік версій"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Culdcept_Saga", note: "стихії й бонуси, мито рівнів, умова перемоги, ~500 карт, онлайн до 4"}
  - {kind: steam, url: "https://store.steampowered.com/app/3825600/Culdcept_The_First/", note: "PC-порт оригіналу 1997 (2026): 50 карт, 300+ видів, rewind до чекпойнта, quick save"}
  - {kind: steam, url: "https://store.steampowered.com/app/3322630/Culdcept_BEGINS/", note: "Culdcept BEGINS (2026)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Culdcept+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [hp-damage, round-currency, ai-opponent, hot-seat, online-multiplayer, teleport, save-game, game-screen, main-menu, end-screen, match-setup, character-select, +roll-and-move, +territory-capture, +toll-on-landing, +land-chain-multiplier, +land-level-upgrade, +elemental-terrain-bonus, +adjacency-buff, +card-battle-items, +deck-builder, +card-collection, +deck-draw, +hand-limit, +lap-bonus, +checkpoint-forts, +bankruptcy, +target-wealth-race, +ring-board, +checkpoint-rewind]
proposes: ["+effect:roll_dice", "+effect:draw_card", "+effect:transfer", "+effect:fight", "+trigger:passes", "+cond:adjacent_owned", "+window:deck-builder", "+window:battle-screen", "+ui:card-hand", "+card:toll-on-landing"]
author: opus
date: 2026-11-09
---

# Culdcept — Монополія з колодою: кидай кубик, став істоту-карту на землю, бери мито й захоплюй чужі клітини боєм

## Суть
Покрокова гра 1–4 «септерів» на кільцевій (іноді розгалуженій) карті клітин-земель. Гравець кидає кубик, іде на N клітин і на вільній землі **викликає істоту з руки** — земля стає його, а суперник, що стане на неї, платить **мито** магією або **вторгається** своєю істотою (бій ST проти HP з предметами). Землі однієї стихії утворюють **ланцюг**, що множить вартість і мито; землі можна прокачувати до рівня 5. Перемагає той, хто першим набрав **цільову загальну магію** й повернувся в замок. Колода («книга») — 50 карт істот, предметів і заклять, яку збирають між партіями.

## Поле і час
- Поле — граф клітин-доріжки (`field: graph`): найчастіше кільце; клітини-землі зі стихією (вогонь, вода, земля, вітер, нейтральна) + спеціальні клітини: замок (старт і фініш кола), форти-чекпойнти (до 4: N/S/W/E), святилища, телепорт-кола.
- Коло = пройти всі форти й повернутися в замок → бонус кола.
- Хід гравця: добір 1 карти → (необовʼязково) 1 закляття до кидка → кидок кубика → рух на N клітин → дія на клітині (виклик / вторгнення / команда землі).
- Покроковий, без таймера; обмеження партії — ціль магії або ліміт раундів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Септер | player | магія (G), рука ≤ 6, книга 50 | рухається на кидок кубика; викликає, вторгається, платить мито |
| Земля | zone | стихія, рівень 1–5, власник, вартість | зайнята істотою власника; бере мито з чужих |
| Нейтральна земля | zone | рівень | без бонусу місцевості |
| Замок | static | — | старт/фініш кола; бонус кола; перемога при цілі магії |
| Форт | static | N/S/W/E | позначка проходу; усі форти → коло зараховане |
| Святилище | static | — | спецклітина (ефект — у «Непевне») |
| Телепорт-коло | static | — | переносить септера (`teleport`) |
| Карта істоти | piece | ST, HP, вартість виклику, стихія, здібності (напр. перший удар) | ставиться на землю; бʼється при вторгненні |
| Карта предмета | pickup | ефект (Long Sword +30 ST, Tower Shield ½ фізичної шкоди) | одна на бік у бою, ціна ≤ поточної магії |
| Карта закляття | pickup | ефект (Firebolt 30 шкоди, ігнорує місцевість; вплив на кубик) | одне за хід, до кидка |
| Книга (колода) | supply | 50 карт, ≤ 4 копії однієї | добір 1 карта за хід |
| Кубик | object | грані — у «Непевне» | дає кроки руху |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(cepter)` → ТО `custom: «добрати 1 карту з книги»` (+effect:draw_card); рука > 6 → `custom: «скинути до 6»`.
- КОЛИ `input(spell)` → ЯКЩО `custom: «ще до кидка і закляття цього ходу не було»` і `counter(magic, >=, cost)` → ТО `currency(-cost)`, `custom: «ефект закляття»`.
- КОЛИ `input(roll)` → ТО `custom: «кинути кубик»` (+effect:roll_dice), `custom: «рух по доріжці на N клітин»` (`move` × N).
- КОЛИ `custom: «септер проходить форт»` (+trigger:passes) → ТО `set_state(cepter, fort_passed)`.
- КОЛИ `custom: «септер проходить замок»` (+trigger:passes) → ЯКЩО `state(cepter, all_forts_passed)` → ТО `currency(+lap_bonus)` (росте з кількістю кіл і земель), `custom: «скинути позначки фортів; лікування поранених істот»`.
- КОЛИ `enter(cepter, teleport_circle)` → ТО `teleport(cepter, pair)`.
- КОЛИ `enter(cepter, free_land)` → ЯКЩО `has(cepter, creature)` і `counter(magic, >=, cost)` → ТО `place(cepter, creature)`, `set_side(land, cepter)`, `currency(-cost)`.
- КОЛИ `enter(cepter, enemy_land)` → ТО `choose(pay_toll | invade)`.
- Мито: → ТО `custom: «віддати власнику мито = вартість землі × ланцюг»` (+effect:transfer).
- Вторгнення: → ТО `custom: «бій істоти з руки проти захисника»` (+effect:fight); кожен бік може додати 1 предмет (`use(item)`), ціна ≤ поточної магії.
- Бій: нападник бʼє першим (якщо в захисника нема «перший удар»): `damage(defender, ST)`; КОЛИ `hp_zero(defender)` → ТО `disappear(defender)`, `set_side(land, attacker)`, мито не платиться, нападник не отримує шкоди.
- Відповідь: ЯКЩО `not hp_zero(defender)` → ТО `damage(attacker, ST_def)`; нападник програв або нічия → `custom: «заплатити мито»`; уцілілі істоти зберігають змінене HP.
- Місцевість: ЯКЩО `same(creature, land, element)` → ТО `custom: «HP захисника + рівень × 10»`; нейтральна земля — без бонусу; нападник на чужій землі бонусу місцевості не має.
- Підтримка: ЯКЩО `adjacent_count(land, own_land, >=, 1)` → ТО `custom: «ST +10 за кожну сусідню свою землю»` (+cond:adjacent_owned).
- Ланцюг: ЯКЩО `custom: «у власника кілька земель однієї стихії в області»` → ТО `multiplier(chain)` (множник до 5) для вартості й мита.
- Рівень: КОЛИ `input(land_command(level_up))` → ЯКЩО `custom: «своя земля, рівень < 5»` → ТО `currency(-base_price × 2 × Δрівнів)`, `custom: «рівень +Δ»`.
- Зміна стихії: → ТО `currency(-(рівень × 100) | -(рівень × 100 + 200))` (нейтральна / стихійна), `set_cell(land, element)`.
- Інші команди землі: перемістити істоту (безкоштовно), обміняти істоту на карту з руки (ціна виклику нової).
- Загальна магія: `custom: «вартість земель + магія на руках + чари»`.
- Банкрутство: КОЛИ `counter(magic, <, 0)` → ТО `custom: «продати землі/чари»`; ЯКЩО все одно < 0 → ТО `custom: «банкрут: повернення в замок, отримати магію як бонус кола»`.
- Перемога: КОЛИ `enter(cepter, castle)` → ЯКЩО `counter(total_magic, >=, target)` → ТО `win`.
- Ліміт раундів: КОЛИ `counter(round, ==, limit)` → ТО `game_over` (переможець — за загальною магією (?)).
- Нагорода: КОЛИ `level_end` → ТО `custom: «випадкові карти в колекцію за місцем»`.

## Керування і ввід
- Меню-керування геймпадом: вибір карти з руки, підтвердження кидка, вибір «мито / вторгнення», команди землі зі списку.
- Під час бою — вибір предмета з руки (або без предмета).
- Local multiplayer 1–4 за одним пристроєм (shared screen), онлайн — у пізніх версіях (Saga — Xbox Live до 4).

## Вікна, меню, HUD
- `main-menu`: Story · Free Battle · Book Edit · Options (за версією).
- `match-setup`: карта, цільова магія, ліміт раундів, суперники AI/люди.
- `character-select`/вибір книги перед партією.
- `game-screen`: дошка (вид на доріжку), портрети й **загальна магія** кожного септера, `+ui:card-hand`, результат кубика, інформація клітини (стихія, рівень, власник, мито).
- `+window:battle-screen`: дві істоти, ST/HP, вибір предмета, анімація ударів.
- `custom-window` команд землі: рівень / стихія / перемістити / обміняти; `confirm-dialog` «платити мито?».
- `+window:deck-builder`: редагування книги 50 карт з колекції, ліміт 4 копії.
- `end-screen`: місця й випадкові карти-нагороди.
- `codex-window`/альбом карт (колекція).
- Переходи: main-menu → match-setup → game-screen ↔ battle-screen → end-screen → нагороди → main-menu/story.

## Фічі поза полем
- Story Mode з прогресією й паками карт; `card-collection` (~500 карт у Saga, 300+ видів у The First, 180 істот).
- `ai-opponent-levels`, `local-multiplayer` 1–4, `online-multiplayer` (Saga).
- The First (2026): `rewind` до будь-якого проходу форту/замку, quick save/load, перемикач «показувати руки обох», Bonus Pack (більше карт-нагород).
- Saga: рука суперників видима — критики скаржились на втрату несподіванки.
- `save-game`, `achievements` (Steam).

## Варіації й родичі
- Серія: Culdcept (1997, Saturn; порт на PlayStation), Culdcept II (Dreamcast 2001), II: Expansion (PS2 2002), Saga (Xbox 360), DS (2008), 3DS (2012, ремейк II), Revolt (3DS 2016), The First (Steam 2026, порт 1997), BEGINS (Switch/Steam 2026, книга 40 (?)).
- Осі варіацій: **рух** (кубик / вибір кроків картою) · **захоплення** (виклик на порожню / бій за зайняту) · **дохід** (мито × ланцюг стихії × рівень) · **умова перемоги** (ціль магії + замок / ліміт раундів) · **колода** (50 / 40, ≤ 4 копії).
- Родичі: Monopoly (roll-and-move, мито, банкрутство; у корпусі нема); `catan.md` (кубик → дохід за положенням); `triple-triad.md` (картки з числами, захоплення бою); `tigris-and-euphrates.md` (стихійні ланцюги/конфлікти); `cartagena.md`, `hare-and-tortoise.md` — рух доріжкою.

## Цікавинки для курсу
- Доріжка як граф із розгалуженнями: рух на N з вибором гілки — 📎.
- Мито = базова × рівень × ланцюг стихії (підрахунок звʼязних однакових земель в «області») — 🥉.
- Бій ST/HP у два удари з першим ударом, предметами й бонусами місцевості/підтримки — 🥉.
- Колода 50 з добором 1/хід, ліміт руки 6, редактор книги з обмеженням 4 копій — 📎.
- Економіка: загальна магія = земля + готівка + чари, продаж земель при мінусі, банкрутство з поверненням — 🥉.
- Rewind до «чекпойнта форту» — список знімків стану на подіях проходу — 🥉.
- AI септера: мито чи вторгнення (оцінка шансу бою з невідомим предметом суперника) — 🥇.

## Мапа на каталог
- Є: `hp-damage` ↔ ST/HP; `round-currency` ↔ магія G; `ai-opponent`, `hot-seat`, `online-multiplayer`; `teleport` ↔ телепорт-кола; `save-game`; вікна `main-menu`, `match-setup`, `character-select`, `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+toll-on-landing` «Мито за зупинку на чужій клітині» · game-logic/economy · 📎 · слоти {base, level, chain}.
  - `+land-chain-multiplier` «Множник за кілька клітин однієї стихії» · game-logic/score · 🥉.
  - `+land-level-upgrade` «Прокачка клітини до рівня N за ціну» · game-logic/economy · 📎.
  - `+elemental-terrain-bonus` «Бонус HP, коли стихія істоти = стихії клітини» · entities/combat · 🌱.
  - `+card-battle-items` «Одна карта-предмет на бік у бою, ціна ≤ готівки» · entities/combat · 📎.
  - `+lap-bonus` · `+checkpoint-forts` · `+bankruptcy` · `+target-wealth-race` · `+checkpoint-rewind` — дрібні, теги.
  - `+roll-and-move`, `+territory-capture`, `+adjacency-buff`, `+deck-builder`, `+card-collection`, `+deck-draw`, `+hand-limit`, `+ring-board` — наявні в корпусі теги.

## Пропозиції до словників
- `+effect:roll_dice` — кинути кубик (рух на результат).
- `+effect:draw_card` — добрати карту з колоди в руку.
- `+effect:transfer` — передати валюту від одного гравця іншому (мито).
- `+effect:fight` — запустити бій двох сутностей за окремою процедурою.
- `+trigger:passes` — сутність проходить клітину без зупинки (форт, замок).
- `+cond:adjacent_owned` — кількість сусідніх клітин того ж власника (підтримка).
- `+window:deck-builder` — редактор колоди з колекції з лімітами копій.
- `+window:battle-screen` — окремий екран бою двох сутностей з вибором предметів.
- `+ui:card-hand` — рука карт гравця.
- `+card:toll-on-landing` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia JA: カルドセプト](https://ja.wikipedia.org/wiki/カルドセプト) — 1–4 септери, стихії земель, замок/форти/святилища/телепорти, порядок ходу, рука ≤ 6, книга 50 (≤ 4 копії), предмети й приклади, загальна магія, банкрутство, ланцюг (до 5), рівні 1–5 і формули вартості, бонус місцевості й підтримки, порядок бою, умова перемоги.
- [Wikipedia: Culdcept](https://en.wikipedia.org/wiki/Culdcept) — ядро (кубик, виклик, мито або бій), колода 50, story mode з паками, платформи й сиквели.
- [Wikipedia: Culdcept Saga](https://en.wikipedia.org/wiki/Culdcept_Saga) — стихії й бонуси, мито прокачаних земель, перемога «магія + повернення», ~500 карт, онлайн.
- [Steam: Culdcept The First](https://store.steampowered.com/app/3825600/Culdcept_The_First/) — 300+ карт, 180 істот, rewind до форту/замку, quick save, reveal hands, нагороди за місцем.
- YouTube: пошук «Culdcept gameplay».

## Непевне
- (?) Грані кубика (1–6? 1–8?) і чи є кубик-модифікатори в оригіналі — не знайдено.
- (?) Точні значення множника ланцюга, бонусу кола, мита й типової цілі магії — джерело не дає чисел.
- (?) Ефект святилищ і правила розгалужень доріжки (вибір гілки) — не перевірено.
- (?) Підтримка «+10 ST за сусідню свою землю» — так у переказі JA-вікі; у серії правило змінювалось.
- (?) Хто перемагає при ліміті раундів — за загальною магією (припущення).
- (?) Книга 40 карт — для BEGINS чи іншої версії («Beginz») — у переказі не ясно.
