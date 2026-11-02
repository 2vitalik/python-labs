---
title: The Battle of Polytopia
slug: polytopia
family: tactics
also: [build-sim]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: setup
  goal: territory
year: 2016
platforms: [iOS, Android, PC, Mac, Linux, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Battle_of_Polytopia", best: true, note: "4X на квадратних клітинах, зірки, міста з сіл, спільне дерево технологій, режими Perfection (30 ходів) і Domination, племена"}
  - {kind: guide, url: "https://west-games.com/polytopia-damage-calculator/", note: "формула бою, бонуси захисту, таблиця юнітів (атака/HP/захист/рух/дальність/навички)"}
  - {kind: guide, url: "https://frothfrenzy.github.io/polytopiacalculator", note: "фанатський калькулятор бою"}
  - {kind: official, url: "https://polytopia.io/", note: "сайт Midjiwan (з Wikipedia)"}
  - {kind: fandom, url: "https://polytopia.fandom.com/wiki/File:Xin-Xi_Warrior_-_Poisoned.png", note: "вікі Polytopia (fandom недоступний агенту; є статуси на кшталт отрути)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=the+battle+of+polytopia"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=the+battle+of+polytopia+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [hp-damage, melee-vs-ranged, impassable-cells, floor-types, round-currency, legal-move-highlight, ai-opponent, hot-seat, difficulty-levels, field-size-picker, event-points, destroy-all-enemies, +capture-income, +recruit-from-base, +retaliation, +damage-formula, +tech-tree, +fog-of-war, +pilot-xp-skills, +movement-points, +turn-limit-score, +roads, +unit-cap-per-city, +city-levelup-choice, +tribe-rules]
proposes: ["+trigger:turn_start", "+trigger:attacked", "+trigger:counter", "+cond:has", "+cond:occupied", "+effect:set_side", "+effect:currency", "+effect:reveal", "+effect:choose", "+effect:unlock", "+role:site", "+role:resource", "+role:neutral", "+ui:stars-income", "+ui:reachable-highlight", "+ui:tile-actions", "+window:tech-tree", "+window:tribe-select", "+window:game-setup", "+window:city-levelup", "+feature:pass-and-play", "+axis:session"]
author: opus
date: 2026-11-02
---

# The Battle of Polytopia — 4X на кишеньковій сітці: міста беруть, ставши в них, а бій рахується формулою

## Суть
Плем'я стартує з одним містом на випадковій квадратній мапі в тумані й за ~30 ходів розростається: розвідує, захоплює села (ставши юнітом і витративши хід), збирає ресурси за **зірки**, купує технології з дерева й наймає юнітів у містах. Бій **детермінований**: шкода рахується з атаки, захисту, HP обох і бонусу місцевості, а вцілілий захисник відповідає. Мінімалізм — один ресурс, ~10 типів юнітів, без менеджменту виробництва — робить це «шахами 4X» для телефона.

## Поле і час
- Квадратна мапа N×N: Tiny 11×11 (121 кл.) … Huge 20×20 (400), Massive 30×30 (900) (?); типи мапи — суходіл, континенти, архіпелаг, водний світ, острови.
- Клітина: місцевість (поле, ліс, гора, мілководдя, океан; лід у Polaris) + ресурс (фрукти, звірі, риба, руда, урожай) + споруда/село/місто + до одного юніта. Кожне місто має територію (3×3, розширюється до 5×5).
- Покроково: гравці ходять по черзі; за хід кожен юніт може раз рухатися і раз атакувати (з обмеженнями навичок).
- Туман: нерозвідані клітини під хмарами; відкриваються в радіусі огляду юнітів і міст (з гори — далі).
- Випадковість лише в генерації мапи (`setup`); бій без кубиків.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Воїн (Warrior) | piece | 2★, HP 10, ATK 2, DEF 2, рух 1 | dash: може атакувати після руху |
| Вершник (Rider) | piece | HP 10, ATK 2, DEF 1, рух 2 | dash, escape: може рухатись після атаки |
| Лучник (Archer) | piece | HP 10, ATK 2, DEF 1, дальність 2 | dash, fortify |
| Захисник (Defender) | piece | HP 15, ATK 1, DEF 3 | fortify: бонус захисту в місті |
| Мечник (Swordsman) | piece | HP 15, ATK 3, DEF 3 | dash |
| Катапульта | piece | ATK 4, DEF 0, дальність 3 | без відповіді від цілі (не дістане) |
| Лицар (Knight) | piece | HP 10, ATK 3.5, DEF 1, рух 3 | persist: після вбивства атакує знову |
| Майндбендер (Mind Bender) | piece | ATK 0 | heal сусідів; convert — переманює ворожого юніта |
| Велетень (Giant) | piece | HP 40, ATK 5, DEF 4 | супер-юніт, нагорода за рівень міста |
| Човен / корабель / лінкор | piece | несе юніт, HP від нього | юніт у порту «сідає» на воду; дальність 1–2, рух 2–3 |
| Племінні юніти (Polytaur, Navalon, дракони, Cymanti…) | piece | особливі | свої правила (плавання, польот, отрута, ріст) |
| Місто | zone | рівень, населення, територія | дає зірки щоходу, наймає юнітів (ліміт = розмір) |
| Село | zone | нейтральне | захоплюється → нове місто |
| Руїна | pickup | — | розвідати: випадкова нагорода (технологія, зірки, юніт, населення) (?) |
| Ліс | terrain | захист ×1,5 з Archery (?) | зупиняє рух без дороги; звірі |
| Гора | terrain | захист ×1,5 з Climbing | непрохідна без Climbing; руда; огляд +1 |
| Мілководдя / океан | terrain | — | лише човнам (після Sailing/Fishing та портом) |
| Ресурси (фрукти, звірі, риба, урожай, руда) | resource | ціна збору в зірках | збір → +населення міста |
| Дорога / міст | terrain | Roads | рух по дорозі дешевший |
| Міська стіна | static | захист ×4 | нагорода за рівень міста |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ТО `currency(+Σ дохід міст)`; кожне місто дає зірки за рівнем, столиця — більше.
- КОЛИ `input(move, u, cell)` → ЯКЩО `custom: «у межах руху; ліс/гора зупиняють; гора лише з Climbing; вода лише з кораблем»` → ТО `move(u, cell)`, `reveal(radius)`.
- КОЛИ `input(attack, a, b)` → ЯКЩО `in_range(a, b, range)` and `custom: «ще не атакував (або dash після руху)»` → ТО шкода за формулою:
  `aF = ATK_a × HP_a/maxHP_a`, `dF = DEF_b × HP_b/maxHP_b × bonus_b`, `dmg = round(aF/(aF+dF) × ATK_a × 4.5)`.
- КОЛИ `attacked(b, a)` → ЯКЩО `not hp_zero(b)` and `in_range(b, a, range_b)` → ТО відповідь: `custom: «retal = round(dF/(aF+dF) × DEF_b × 4.5)»`, `damage(a, retal)`.
- КОЛИ `hp_zero(b)` після ближньої атаки → ТО `move(a, cell_b)` (переможець займає клітину), `counter(kills_a, +1)`.
- КОЛИ `counter(kills, ==, 3)` → ТО `custom: «можна підвищити до ветерана»`: `+5 maxHP`, `heal(full)` (?).
- КОЛИ юніт не рухався й не атакував → ТО `custom: «відпочинок: heal +2 HP, +4 на своїй території»` (?).
- КОЛИ `input(capture, u)` → ЯКЩО `occupied(village|enemy_city, u)` на початку ходу → ТО `set_side(site, u.side)`, `end_turn(u)`; село стає містом рівня 1.
- КОЛИ `input(harvest, cell)` → ЯКЩО `has(tech)` and `currency ≥ cost` and `custom: «клітина в межах міста»` → ТО `currency(−cost)`, `counter(population, +n)`.
- КОЛИ `counter(population, ≥, level+1)` → ТО рівень міста +1, `choose(дві нагороди)`: майстерня (+1★), дослідник, стіна, ресурси, ріст кордонів, парк, супер-юніт.
- КОЛИ `input(train, unit, city)` → ЯКЩО `has(tech)` and `currency ≥ cost` and `count(units_of_city, <, cap)` and `free(city)` → ТО `spawn_at(unit, city)`; юніт ходить наступного ходу.
- КОЛИ `input(research, tech)` → ЯКЩО `custom: «попередня в гілці відкрита»` → ТО `currency(−cost)`, `unlock(tech)`; ціна росте з кількістю міст.
- Бонус захисту (`bonus_b`): 1 — звичайно; 1,5 — ліс/гора з відповідною технологією, місто, вода з Aquatism; 4 — місто зі стіною.
- КОЛИ `input(convert, mind_bender, b)` → ТО `set_side(b, mind_bender.side)`.
- Perfection: КОЛИ `counter(turn, ==, 30)` → ТО `custom: «кінець, рахунок очок: міста, територія, розвідані клітини, технології, юніти, монументи»`.
- Domination: КОЛИ `custom: «лишилось одне плем’я»` → ТО `win`; оцінка за кількістю ходів.
- Мультиплеєр: Glory — першим набрати 10 000 очок; Might — захопити всі столиці (?).
- Поразка: втрачено всі міста. Рахунок: очки за досягнення + бонус складності.

## Керування і ввід
- Тап по юніту → підсвітка клітин руху й червоні цілі атаки; тап по клітині — рух/атака. Тап по клітині без юніта — панель дій клітини (зібрати, побудувати, ціна в зірках).
- Тап по місту → панель найму юнітів і рівня; кнопка дерева технологій; кнопка «Наступний хід».
- Нема undo; хід завершується кнопкою, черга гравців фіксована.

## Вікна, меню, HUD
- `main-menu`: New Game, Resume, Multiplayer (Pass & Play, Online), Throne Room (статистика, рекорди), Settings, Help.
- `tribe-select` — вибір племені (бонус-технологія, стартовий юніт, особлива мапа/ресурси).
- `game-setup` — режим (Perfection, Domination, Creative), кількість суперників, складність AI (Easy/Normal/Hard/Crazy), розмір і тип мапи.
- `game-screen`: поле; верх — `score`, `turn-counter` «Turn 12/30», `stars-income` (зірки і `+N` за хід); низ — кнопки технологій, статистики, наступного ходу; `tile-actions` — панель дій вибраної клітини; `reachable-highlight` руху; `tooltip` юніта (HP, ATK, DEF, навички).
- `tech-tree` — радіальне дерево з 5 гілок з цінами.
- `city-levelup` — вибір одного з двох бонусів при рості міста.
- `end-screen` — перемога/поразка, рахунок, рейтинг зірками; `leaderboard`/Throne Room — найкращі результати за племенами.
- `help-window` — «Tribe info», підказки про юнітів і технології; `settings-window` — звук, музика, хмари, мова.

## Фічі поза полем
- `mode-classic` (Perfection, 30 ходів), Domination, Creative (`custom-rules`: карта, суперники, без ліміту) (?).
- `hotseat` (Pass & Play), `online-multiplayer` (асинхронний, кросплатформний, рейтингові ігри), `ai-opponent-levels` 4.
- `unlockables` — платні племена-DLC, «особливі» племена з власними правилами; `save-autosave`; статистика й рекорди.
- Пізніші оновлення: дипломатія (посольства, мирні угоди), щотижневі виклики (?).

## Варіації й родичі
- Родичі: Civilization (4X на гексах, складна економіка), Advance Wars (детермінований бій, міста-фабрики, захоплення стоянням), Into the Breach (мала сітка, чиста інформація), Antiyoy, Unciv.
- Племена як варіації правил: Polaris — заморожує клітини в лід; Aquarion — плавучі юніти й мілководдя; Elyrion — перетворює звірів на бійців, дракони; Cymanti — отрута й гриби; Luxidoor — стартує з великою столицею.
- Осі варіацій:
  - **бій**: детермінована формула (Polytopia, Advance Wars) / ймовірність влучання (Wesnoth, XCOM) / кубики з вибором (Blood Bowl);
  - **захоплення**: вхід = захоплення (Wesnoth) / стояти й витратити хід (Polytopia) / кілька ходів «capture points» (Advance Wars);
  - **кінець гри**: ліміт ходів і очки / знищення всіх / перший до N очок.

## Цікавинки для курсу
- Детермінована формула бою з відповіддю й прогнозом «до кліку» — 📎 (чиста функція від двох юнітів).
- Міста-«сайти»: стати, витратити хід, змінити власника, отримати дохід — 📎.
- Дерево технологій з ціною, що залежить від кількості міст, і розблокуванням дій/юнітів — 🥉.
- Рівень міста → вибір з двох нагород (`choose`) — 🌱.
- Туман із розвідкою та бонусом огляду з гори — 🥉.
- Племена як набори правил над спільним двіжком — 🥈 (`custom-rules` як дані).
- Perfection: обмежено 30 ходів, мета — очки, а не знищення — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` ↔ лучник/катапульта vs ближній · `impassable-cells` ↔ гори без Climbing, вода · `floor-types` ↔ ліс/гора/вода · `round-currency` ↔ зірки · `legal-move-highlight` · `cell-click` · `ai-opponent` + `ai-greedy` · `hot-seat` · `difficulty-levels` · `field-size-picker` · `save-autosave` · `score-records` + `event-points` ↔ рахунок Perfection · `destroy-all-enemies` ↔ Domination · `game-screen`/`main-menu`/`end-screen`/`help-window`.
- **Нема** → пропозиції карток:
  - `+capture-income` (з Wesnoth) — села й міста як точки доходу.
  - `+recruit-from-base` (з Wesnoth) — найм у місті.
  - `+retaliation` (з Wesnoth) — відповідь вцілілого.
  - `+damage-formula` «Детермінована формула бою» · entities/combat · 📎 · слот {k: 4.5}.
  - `+tech-tree` «Дерево технологій» · game-logic/economy · 🥉 · слот {cost_formula}.
  - `+fog-of-war` (з Wesnoth).
  - `+pilot-xp-skills` (з Into the Breach) — ветеран після 3 вбивств.
  - `+movement-points` (з Wesnoth) — ліс/гора зупиняють, дорога прискорює.
  - `+turn-limit-score` «Очки за обмежену кількість ходів» · game-logic/win · 🌱 · слот {turns: 30}.
  - `+roads` «Дороги прискорюють рух» · entities/move · 📎.
  - `+unit-cap-per-city` «Ліміт юнітів на місто» · game-logic/economy · 🌱.
  - `+city-levelup-choice` «Рівень бази з вибором нагороди» · game-logic/economy · 📎.
  - `+tribe-rules` «Фракції з власними правилами» · game-logic/difficulty · 🥈.

## Пропозиції до словників
- `+trigger:turn_start` ⏳ (дохід), `+trigger:attacked` (з Wesnoth — відповідь), `+trigger:counter` ⏳ (населення → рівень міста).
- `+cond:has` ⏳ (технологія), `+cond:occupied` ⏳ (юніт стоїть у селі).
- `+effect:set_side` ⏳ (захоплення, convert), `+effect:currency` ⏳, `+effect:reveal` ⏳, `+effect:choose` ⏳ (нагорода рівня), `+effect:unlock` ⏳ (технологія).
- `+role:site` (з Wesnoth) — село/місто; `+role:resource` ⏳ — фрукти/риба/руда; `+role:neutral` ⏳ — звірі для полювання (?).
- `+ui:stars-income` — запас валюти + приріст за хід; `+ui:reachable-highlight` (є); `+ui:tile-actions` — контекстна панель дій вибраної клітини з цінами.
- `+window:tech-tree` — дерево технологій; `+window:tribe-select` (≈ `character-select` ⏳ для фракції); `+window:game-setup` — налаштування партії (режим, суперники, мапа); `+window:city-levelup` (≈ `upgrade-window` ⏳).
- `+feature:pass-and-play` = `hotseat` ⏳ на одному телефоні з екраном-заслінкою.
- `+axis:session` = `match`.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/The_Battle_of_Polytopia) — зірки, міста з сіл, спільне дерево технологій, режими Perfection (30 ходів) і Domination, Creative, племена, мультиплеєр, Midjiwan.
- [West Games: Polytopia Damage Calculator](https://west-games.com/polytopia-damage-calculator/) — формула шкоди, бонуси захисту, таблиця юнітів, «ветеран +5 HP».
- [Polytopia Battle Calculator](https://frothfrenzy.github.io/polytopiacalculator) — фанатський калькулятор.
- [polytopia.io](https://polytopia.io/) — офіційний сайт (адреса з Wikipedia).
- YouTube: пошук «the battle of polytopia gameplay».

## Непевне
- (?) Formula: калькулятори подають бонус місцевості по-різному (множник 1/1,5/4 чи додаток +1…+4); у файлі — множникова версія з памʼяті про фан-вікі.
- (?) Ветеран після 3 вбивств — з памʼяті; підтверджено лише «+5 maxHP».
- (?) Лікування відпочинком (+2/+4), розміри мап, Glory/Might, нагороди руїн, вартість юнітів (крім воїна 2★) не перевірено (fandom недоступний).
- (?) Чи може лицар отримати відповідь (калькулятор пише «no retaliation» для лицаря — сумнівно).
