---
title: Gem Miner 2
slug: gem-miner-2
aka: []
family: dig-gravity
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: setup
  goal: state
year: 2012
platforms: [Android]
links:
  - {kind: other, url: "https://www.pocketgamer.com/gem-miner-2/review/", best: true, note: "огляд 2012-02-15: світлі й темні камені, дерев'яні опори, скінченні драбини, вода/вогонь/газ, витривалість, рятувальники, магазин, Expedition і Freeplay"}
  - {kind: other, url: "https://www.pocketgamer.com/gem-miner-2/", note: "сторінка гри: розробник і видавець Psym Mobile, Android"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=au.com.psymmobile.gemminer2", note: "Google Play (розробник Phil Symonds); опис у фетчі не віддається"}
  - {kind: other, url: "https://frostclick.com/wp/index.php/2012/07/24/gem-miner-get-ready-for-a-challenge", note: "перша частина Gem Miner: падіння каменів і провалля, магазин, спальник і драбини, режим без витривалості, 3 слоти"}
  - {kind: other, url: "https://www.gameyum.com/other-games/98239-guide-to-building-a-fortune-in-gem-miner/", note: "поради серії: драбини й опори по 10, ліфти, аптечки витривалості, більша сумка, бур, мапи генеруються"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Gem+Miner+2+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-by-input, dig-terrain, destructible-blocks, gravity-fall, ladder-climb, item-pickup, inventory-limit, inventory-items, hunger-clock, environment-death, player-death, round-currency, shop-between-levels, shop-catalog, shop-window, in-round-upgrades, mode-select, difficulty-levels, sequential-levels, save-multi-slot, +delayed-fall, +support-beam, +place-limited-items, +rescue-penalty, +depth-tiered-ore, +sell-cargo]
proposes: ["+trigger:undermined", "+effect:sell", "+ui:stamina-bar", "+card:support-beam", "+card:place-limited-items", "+card:rescue-penalty"]
author: opus
date: 2026-11-09
---

# Gem Miner 2 — копай униз по клітинах, став опори під світлим камінням і драбини назад, поки не скінчилась витривалість

## Суть
Мобільна гра Psym Mobile: шахтар копає ґрунт кайлом, шукає вугілля, залізо, золото й самоцвіти і продає їх у магазині на поверхні, щоб купити кращий інструмент. Ядро — **обвали й запаси**: світлий камінь падає, якщо підкопати під ним і швидко не поставити дерев'яну опору; униз можна спуститись, лише маючи драбини, яких у сумці скінченна кількість. Будь-яка дія з'їдає витривалість — на нулі шахтаря витягають рятувальники, але знайдене забирають. Два режими: Expedition (місії з ціллю) і Freeplay (копай скільки хочеш).

## Поле і час
- Шахта — вертикальний розріз під поверхнею, квадратні клітини ґрунту, каміння, руди; цінніше лежить глибше (поради серії).
- Камера йде за шахтарем; бачимо околицю (`info: partial`, ?).
- Час — real-time: камінь падає за мить після підкопу, тому опору треба ставити швидко.
- Шахти генеруються випадково (для серії, ?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шахтар | player | витривалість, сумка, драбини, опори | ходить, копає в напрямку руху, лізе драбиною |
| Ґрунт | terrain | — | копається кайлом → прохід; з'їдає витривалість |
| Темний камінь | static | — | не падає; копається чи ні — (?) |
| Світлий (білий) камінь | object | — | падає, коли під ним порожньо й нема опори; смертельний |
| Дерев'яна опора | object | запас у сумці; ціна 10 (серія) | ставиться під світлий камінь — тримає його |
| Драбина | object | запас скінченний; ціна 10 (серія) | ставиться в прохід; дає лізти вгору й униз; лазіння з'їдає витривалість |
| Руда / самоцвіт | resource | ціна; глибина | у сумку; продається на поверхні |
| Вода | hazard | — | небезпека в шахті (?) |
| Вогонь | hazard | — | небезпека в шахті (?) |
| Вугільний газ | hazard | — | «задушливий» — шкодить біля вугілля (?) |
| Сендвіч | pickup | +витривалість | з'їсти в шахті |
| Магазин на поверхні | static | — | продаж знахідок, купівля спорядження |
| Ліфт (серія) | object | дорожчий | полегшує глибокий спуск (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(miner, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, soil)` and `custom: «кайло увімкнене»` → ТО `set_cell(next_cell, tunnel)`, `counter(stamina, −n)`; без кайла рух у стіну — `block`.
- КОЛИ `input(place_ladder)` → ЯКЩО `has(miner, ladder)` → ТО `place(miner, ladder)`, `take(miner, ladder)`.
- КОЛИ `input(up|down)` → ЯКЩО `cell(here, ladder)` → ТО `move(miner, dir)`, `counter(stamina, −n)`.
- КОЛИ `custom: «розкопано клітину під світлим каменем»` → ЯКЩО `not supported(light_rock)` → ТО `custom: «камінь падає після короткої паузи»`, `fall(light_rock)`.
- КОЛИ `input(place_support)` → ЯКЩО `has(miner, support)` and `free(cell_under_rock)` → ТО `place(miner, support)` — камінь лишається.
- КОЛИ `contact(light_rock, miner)` → ТО `lose` (?) — «може бути смертельним».
- КОЛИ `contact(miner, water|fire|gas)` → ТО `custom: «шкода або втрата витривалості»` (?).
- КОЛИ `custom: «викопано руду»` → ЯКЩО `counter(bag, <, capacity)` → ТО `pickup(miner, ore)`.
- КОЛИ `input(eat)` → ЯКЩО `has(miner, sandwich)` → ТО `take(miner, sandwich)`, `counter(stamina, +n)`; КОЛИ `input(rest)` → ТО `counter(stamina, +n)` повільно.
- КОЛИ `counter(stamina, ==, 0)` → ТО `custom: «рятувальники піднімають на поверхню»`, `take(miner, all_found)`.
- КОЛИ `enter(miner, shop)` → ТО `window(shop-window)`: продаж → `currency(+Σ)`; купівля → `currency(−price)`, `give(miner, item)`.
- КОЛИ `custom: «ціль експедиції виконано»` → ТО `win`, `next_level`.
- Перемога: ціль місії (Expedition) · Поразка: шахтар загинув під каменем або вичерпав витривалість (рятування з втратою знахідок) · Рахунок: гроші за продане.

## Керування і ввід
- Тач: рух у бік стіни = копання; через це легко вдарити не туди; кайло можна вимкнути для безпечного руху, але це «fiddly».
- Окремі кнопки — поставити драбину, опору, з'їсти, відпочити (?).

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Expedition · Freeplay.
- `level-select` — 70+ експедицій у 3 складностях (опис застосунку зі сніпета пошуку, ?).
- `game-screen`: розріз шахти; HUD — `stamina-bar`, запаси драбин і опор, сумка, гроші (?).
- `shop-window` на поверхні: продаж знахідок, спорядження.
- `end-screen` — підсумок місії / рятування.

## Фічі поза полем
- `mode-classic` (Expedition, місії з цілями) і `mode-sandbox` (Freeplay без цілей); `difficulty-presets` — 3 (?).
- `in-round-upgrades`: краще кайло, бур, більша сумка, спальник, ліфти (серія).
- Перша частина: 3 слоти збереження, режим без витривалості; другу — Bluetooth-мультиплеєр і платні пакети місій (сніпет пошуку, ?).

## Варіації й родичі
- Gem Miner (перша частина, Psym Mobile) — те саме ядро, простіша графіка й правила.
- У сімʼї: [motherload.md](motherload.md) — продаж руди й апгрейди, паливо замість витривалості; [steamworld-dig.md](steamworld-dig.md) — світло й драбини; [dig-dug.md](dig-dug.md) і [banana.md](banana.md) — камінь, що падає з затримкою після підкопу.
- **Осі варіацій**: обвал «камінь падає завжди / лише світлий / тримає опора»; повернення «драбини зі скінченного запасу / ліфт / телепорт»; ціна дій «витривалість / паливо / енергія з часом»; провал «смерть / рятування з втратою знахідок».

## Цікавинки для курсу
- Два типи каменю: світлий падає з затримкою без опори, темний стоїть — 🌱.
- Опора як витратний предмет, що скасовує падіння, — 🌱.
- Скінченні драбини: планування спуску з думкою про повернення — 📎.
- Витривалість, що тане від копання й лазіння, + рятування з конфіскацією знахідок — 📎.
- Генерація шахти з рудами за глибиною — 📎.

## Мапа на каталог
- Є: `move-by-input` · `dig-terrain` + `destructible-blocks` ↔ ґрунт · `gravity-fall` ↔ світлий камінь · `ladder-climb` · `item-pickup` · `inventory-limit` ↔ сумка · `inventory-items` ↔ драбини, опори, сендвічі · `hunger-clock` ↔ витривалість · `environment-death` + `player-death` · `round-currency` · `shop-between-levels` + `shop-catalog` + `shop-window` · `in-round-upgrades` · `mode-select` · `difficulty-levels` · `sequential-levels` ↔ експедиції · `save-multi-slot` (перша частина).
- **Нема** → пропозиції карток:
  - `+support-beam` «Опора під каменем скасовує падіння» · entities/interact · 🌱.
  - `+place-limited-items` «Скінченний запас предметів, що ставляться на поле» · entities/state · 🌱 · слот {count}.
  - `+rescue-penalty` «Провал повертає на базу й забирає знахідки» · game-logic/lose · 🌱.
  - Повтори: `+delayed-fall` (Banana, Dig Dug), `+depth-tiered-ore` і `+sell-cargo` (Motherload).

## Пропозиції до словників
- `+trigger:undermined` — з-під обʼєкта прибрали опору (клітину під ним розкопано).
- `+effect:sell` — повтор (Motherload): знахідки → гроші.
- `+ui:stamina-bar` — шкала витривалості шахтаря.

## Джерела
- ⭐ [Pocket Gamer: огляд Gem Miner 2](https://www.pocketgamer.com/gem-miner-2/review/) — темні й світлі камені, опори, скінченні драбини, вода/вогонь/вугільний газ, витривалість від лазіння й копання, сендвічі й відпочинок, рятувальники забирають знахідки, магазин, Expedition/Freeplay, копання рухом у стіну.
- [Pocket Gamer: сторінка гри](https://www.pocketgamer.com/gem-miner-2/) — Psym Mobile, Android.
- [Frostclick: Gem Miner](https://frostclick.com/wp/index.php/2012/07/24/gem-miner-get-ready-for-a-challenge) — перша частина: падіння каменів, провалля, спальник, драбини, режим без витривалості, 3 слоти.
- [GameYum: поради Gem Miner](https://www.gameyum.com/other-games/98239-guide-to-building-a-fortune-in-gem-miner/) — драбини й опори по 10, ліфти, аптечки, сумка, бур, випадкові шахти (версія не вказана).
- Сніпети пошуку (supercheats, опис застосунку): «білі камені впадуть, якщо швидко не поставити опору», 70+ експедицій у 3 складностях, Bluetooth-мультиплеєр.

## Непевне
- (?) Чи темний камінь копається (повільніше / іншим інструментом) чи непрохідний.
- (?) Як саме шкодять вода, вогонь і газ (смерть, витривалість, тече вода чи ні).
- (?) Ціни, генерація шахт, ліфти, сумка — з порад до серії Gem Miner, не обовʼязково для другої частини.
- (?) Чи гравітація діє на самого шахтаря (падіння в прокопану яму).
- (?) Кількість експедицій, складностей і мультиплеєр — лише зі сніпетів пошуку.
