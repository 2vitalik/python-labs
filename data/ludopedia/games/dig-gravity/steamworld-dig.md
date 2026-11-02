---
title: SteamWorld Dig
slug: steamworld-dig
family: dig-gravity
also: [grid-platformer, build-sim]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: setup
  goal: state
year: 2013
platforms: [3DS, PC, macOS, Linux, PS4, Vita, Wii U, Xbox One, Switch, Stadia, Luna]
links:
  - {kind: fandom, url: "https://steamworld.wiki.gg/wiki/SteamWorld_Dig", best: true, note: "wiki.gg: 4 типи ґрунту, продаж руди в Tumbleton, XP → крамниці, 3 зони по 3 печери, шахта рандомна, печери ні"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/SteamWorld_Dig", note: "ресурси (здоровʼя, вугілля для світла, вода), драбини, самознищення, штраф за смерть"}
  - {kind: steam, url: "https://store.steampowered.com/app/252410/SteamWorld_Dig/", note: "сторінка Steam"}
  - {kind: fandom, url: "https://steamworld.wiki.gg/wiki/Resources/SteamWorld_Dig", note: "таблиця руд і самоцвітів з цінами"}
  - {kind: fandom, url: "https://steamworld.wiki.gg/wiki/Rusty", note: "здібності й апгрейди Расті"}
  - {kind: fandom, url: "https://steamworld.wiki.gg/wiki/Tumbleton", note: "місто: продавці, скупниця руди, телепорт"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=SteamWorld+Dig+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, gravity-fall, impassable-cells, hp-damage, environment-death, player-death, item-pickup, inventory-limit, shop-between-levels, shop-catalog, round-currency, in-round-upgrades, teleport-pair, blast-wave, player-camera, minimap-radar, save-autosave, checkpoint, status-panel, +dig-terrain, +dig-wall, +destructible-blocks, +crumbling-floor, +ladder-climb, +core-deposit, +hunger-clock, +fog-of-war, +energy-resource, +fall-damage, +wall-jump, +death-loot-drop, +ore-vein-generation]
proposes: ["+trigger:land", "+effect:sell", "+effect:place", "+cond:supported", "+ui:depth-meter", "+ui:light-gauge", "+ui:water-gauge", "+ui:bag-slots", "+card:fall-damage", "+card:wall-jump", "+card:death-loot-drop", "+card:ore-vein-generation"]
author: opus
date: 2026-11-02
---

# SteamWorld Dig — копай шахту під містом, неси руду нагору на продаж, купуй інструменти, копай глибше

## Суть
Робот Расті розкопує шахту під містечком Tumbleton: кожна клітина ґрунту руйнується киркою, буром чи динамітом, а викопане стає рельєфом, по якому треба потім вилізти нагору. Руда і самоцвіти займають місце в сумці; повна сумка → повернення в місто, продаж, гроші й досвід → нові крамниці й апгрейди → глибший спуск. Під землею тиснуть три ресурси: здоровʼя (вороги, падіння), світло лампи (паливо згасає) і вода (живить бур, парові стрибки й удари). Цикл «спуститись — набрати — вилізти — продати — прокачатись» і є ядром.

## Поле і час
- Вертикальна шахта на клітинній сітці ґрунту; три зони вниз: Archaea → Old World → Vectron; у кожній по 3 ручні печери з технологіями, решта шахти **генерується випадково** на кожне проходження (розкладка руд, порожнин).
- **Межовий випадок:** клітинні лише ґрунт і руйнування; рух Расті — платформерний, з піксельною фізикою (біг, стрибки, інерція), а не крок на клітину. У модель корпусу лягає «копання і руда»; платформінг — текстом.
- Камера за гравцем; поза світлом лампи темно (видимість — радіус світла); мінікарта відкривається тим, що побачено.
- Real-time; час не тисне, крім палива лампи.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Расті | player | HP, паливо лампи, вода, сумка | біг, стрибок, стрибок від стіни (?), копає в 4 сторони; падіння з висоти шкодить |
| Пісок | terrain | — | копається легко; (?) осипається |
| Звичайна земля | terrain | міцність | кілька ударів кирки (залежно від рівня кирки) |
| Камінь | terrain | — | лише бур (витрачає воду) або динаміт |
| Крихка земля | terrain | — | руйнується від дотику гравця або ворога |
| Межа шахти | static | — | непорушна |
| Клітина з рудою | resource | тип: 22 руди 1–60 $, 9 самоцвітів 15–500 $ | викопана → предмет у сумку |
| Сфера (orb) | resource | — | валюта апгрейдів (?) |
| Вода (джерело) | resource | — | поповнює бак (?) |
| Вороги (трилобіти, печерні жителі, роботи Vectron) | enemy | HP, патерн атаки | ходять/стріляють; зі зниженням — нові патерни й слабкі місця |
| Драбина | object | купується | ставиться на клітину, по ній лізуть угору |
| Телепорт | object | у місті + переносний | повернення між шахтою й містом (?) |
| Печера з технологією | zone | ручний рівень | пазл/платформінг → нова здібність |
| Tumbleton | zone | продавці | скупниця Dorothy, крамниці Cranky, Dandy, Biff; інструменти тут не працюють |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dig, dir)` → ЯКЩО `cell(target, dirt|sand)` → ТО `damage(tool_power)`; міцність 0 → `set_cell(empty)`.
- КОЛИ `input(dig, dir)` → ЯКЩО `cell(target, rock)` → ТО `block`; ЯКЩО `has(drill)` and `has(water)` → ТО `set_cell(empty)`, `counter(water, -n)`.
- КОЛИ `contact(player|enemy, brittle_dirt)` → ТО `set_cell(empty)`.
- КОЛИ `set_cell(ore_cell, empty)` → ЯКЩО `count(bag, <, capacity)` → ТО `give(player, ore)`; інакше `custom: «руда лишається лежати»` (?).
- КОЛИ `not supported(player)` → ТО `fall(player)`; КОЛИ `land(player, height)` → ЯКЩО `height > safe` and `not has(fall_dampeners)` → ТО `hp(player, -n)`.
- КОЛИ `contact(player, wall)` у стрибку → ТО `custom: «стрибок від стіни»` (?).
- КОЛИ `input(place, ladder)` → ЯКЩО `has(ladder)` → ТО `place(ladder, here)`; по драбині — `move(up)`.
- КОЛИ `timer(1 s)` → ЯКЩО `not in_town` → ТО `counter(fuel, -1)`; `counter(fuel, ==, 0)` → `custom: «радіус світла мінімальний»`.
- КОЛИ `died(enemy)` → ТО `counter(fuel, +n)`; КОЛИ `enter(player, town)` → ТО `counter(fuel, max)`.
- КОЛИ `input(steam_jump|steam_punch|drill)` → ЯКЩО `has(water, n)` → ТО дія, `counter(water, -n)`.
- КОЛИ `input(dynamite)` → ТО `explode(3×3)`.
- КОЛИ `input(sell)` у місті → ТО `sell(bag)`: `currency(+Σ price)`, `counter(xp, +n)`; КОЛИ `counter(xp, >=, level_n)` → ТО `unlock(shop)`.
- КОЛИ `input(buy, upgrade)` → ЯКЩО `has(money, price)` and `has(orbs, k)` (?) → ТО `custom: «апгрейд інструмента/сумки/лампи/баку/здоровʼя»`.
- КОЛИ `contact(enemy, player)` → ТО `hp(player, -n)`; `hp_zero(player)` → `respawn(player, town)`, `currency(-fee)`, `custom: «здобич лишилась на місці смерті»`.
- КОЛИ `input(self_destruct)` → ТО те саме, що смерть (вихід із безвиході).
- КОЛИ `custom: «пройдено печеру»` → ТО `give(player, ability)` (бур, парові боти, динаміт, детектор мінералів, амортизатори…).
- Перемога: дійти до дна Vectron і завершити сюжет. Поразки нема — лише штраф і повернення. Рахунок: гроші, час проходження.

## Керування і ввід
- Стик/стрілки — рух; стрибок; копати (утримання в напрямку); окремі кнопки для бура, парового стрибка, удару, динаміту, драбини/телепорта.
- Головне рішення — порядок копання: «не підрізати собі дорогу назад», лишати виступи й шахти, по яких можна вилізти.

## Вікна, меню, HUD
- `main-menu` → `save-slots` (?) → `game-screen`.
- `game-screen`: HUD — `hp-bar`, `light-gauge` (паливо лампи), `water-gauge`, `bag-slots`, `coins`, `depth-meter` (?), `minimap` (з рудою, якщо є детектор).
- `shop-window` ×3 (Cranky, Dandy, Biff) + вікно скупниці (`sell`).
- `map-window` — вся відкрита шахта.
- `dialogue-window` — розмови з мешканцями Tumbleton.
- `end-screen` з часом проходження й статистикою (?).

## Фічі поза полем
- `autosave`, `continue`; `meta-progression` у межах проходження (рівні досвіду відкривають крамниці).
- `xp-level` за продаж руди; `unlockables` — здібності з печер.
- Платформи: 3DS, ПК, консолі; ПК — клавіатура й геймпад, досягнення Steam.

## Варіації й родичі
- SteamWorld Dig 2 (2017) — більший світ, ручніші печери, гак; SteamWorld Heist — тактика.
- Родичі за циклом «копай — продай — апгрейдь»: Motherload (2004), Terraria (вільніше), Dome Keeper (копання + оборона), Spelunky (руйнування й платформи, але рівні).
- **Осі варіацій**: хто генерує шахту — «ручна / рандом за каркасом (SWD) / повністю рандом»; що обмежує вилазку — «сумка / світло / вода / HP»; повернення — «лізти / драбина / телепорт / ліфт».

## Цікавинки для курсу
- Цикл економіки «копай → сумка → місто → продаж → апгрейд → глибше» — 🥈 (кілька модулів: інвентар із лімітом, магазин, прогресія).
- Міцність клітини проти сили інструмента (кирка рівня N, бур для каменю) — 📎.
- Шкода від висоти падіння, амортизатори скасовують — 📎.
- Світло як годинник: паливо гасне, радіус видимості — 🥉 (туман + ресурс).
- Руда, розкидана генератором за таблицею глибини поверх ручного каркасу шахти — 🥇.
- Штраф за смерть і здобич, що лишилась на місці загибелі — 📎.
- Крихка земля, що валиться під гравцем і ворогами — 🌱.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `impassable-cells` (межа, камінь без бура) · `hp-damage` · `environment-death` · `player-death` · `item-pickup` · `inventory-limit` ↔ сумка · `shop-between-levels` + `shop-catalog` ↔ Tumbleton · `round-currency` · `in-round-upgrades` · `teleport-pair` ↔ телепорт місто–шахта · `blast-wave` ↔ динаміт 3×3 · `player-camera` · `minimap-radar` (детектор мінералів) · `save-autosave` · `checkpoint` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+fall-damage` «Шкода від висоти падіння» · entities/state · 📎 · слоти {safe_height, per_cell}.
  - `+wall-jump` «Стрибок від стіни» · entities/move · 📎 — межовий: потребує платформерної фізики.
  - `+death-loot-drop` «Смерть: штраф і здобич лишається на місці» · game-logic/lose · 📎 · слоти {fee, recoverable}.
  - `+ore-vein-generation` «Руда за таблицею глибини поверх ручного каркасу» · levels/generation · 🥇 · слоти {depth_table, fixed_rooms}.
  - Повтори: `+dig-terrain`, `+dig-wall` (міцність × сила інструмента), `+destructible-blocks`, `+crumbling-floor` (крихка земля), `+ladder-climb`, `+core-deposit` (тут — продаж за гроші й досвід), `+hunger-clock` (паливо лампи), `+fog-of-war` (світло), `+energy-resource` (вода).

## Пропозиції до словників
- `+trigger:land` — сутність приземлилась після падіння з висоти N (основа шкоди від падіння).
- `+effect:sell` — перетворити вміст інвентаря на валюту за прайсом.
- `+effect:place` ⏳ — повтор (драбина, телепорт з інвентаря).
- `+cond:supported` ⏳ — повтор.
- `+ui:depth-meter` (повтор з Mr. Driller), `+ui:light-gauge`, `+ui:water-gauge` (обидва — підвиди ⏳ `energy-bar`), `+ui:bag-slots` (сумка як сітка слотів, близько `inventory-bar`).

## Джерела
- ⭐ [SteamWorld Wiki: SteamWorld Dig](https://steamworld.wiki.gg/wiki/SteamWorld_Dig) — 4 типи ґрунту (пісок, земля, камінь лише буром, крихка), продаж у Tumbleton за гроші й досвід, крамниці за рівнями, зони й печери, рандом шахти крім печер.
- [Wikipedia: SteamWorld Dig](https://en.wikipedia.org/wiki/SteamWorld_Dig) — HP, вугілля для світла, вода для здібностей, драбини, самознищення, штраф «reparation fee», платформи й дати.
- [Resources/SteamWorld Dig](https://steamworld.wiki.gg/wiki/Resources/SteamWorld_Dig) — 22 руди (1–60 $) і 9 самоцвітів (15–500 $).
- [Rusty](https://steamworld.wiki.gg/wiki/Rusty) — кирка, піч-лампа (паливо з убитих ворогів і в місті), Dash Boots, Steam Jump, бур на воді, динаміт 3×3, Steam Punch, Fall Dampeners, детектор мінералів, Static Jump.
- [Tumbleton](https://steamworld.wiki.gg/wiki/Tumbleton) — продавці, скупниця, транспортні труби й телепорт.
- [Steam](https://store.steampowered.com/app/252410/SteamWorld_Dig/) — опис і фічі.

## Непевне
- (?) Стрибок від стіни з самого початку — з памʼяті; джерела його не згадують.
- (?) Сфери (orbs) як друга валюта апгрейдів і де саме береться вода (джерела в шахті) — з памʼяті.
- (?) Що робиться з рудою при повній сумці; точна місткість сумки й апгрейди.
- (?) Чи пісок осипається (гравітація ґрунту) — не перевірено.
- (?) Як саме працює переносний телепорт (купується й ставиться в шахті) — з памʼяті.
- (?) Повернення здобичі після смерті — у Wikipedia з позначкою [citation needed].
