---
title: Wildfrost
slug: wildfrost
family: tower-lanes
also: [roguelike]
klass: cursor
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2023
platforms: [Switch, PC, Android, iOS, Xbox]
links:
  - {kind: fandom, url: "https://wildfrostwiki.com/Getting_Started", best: true, note: "офіційна вікі: поле 2 ряди, лічильники, дзвін перездачі, корони, wave bell"}
  - {kind: fandom, url: "https://wildfrostwiki.com/Stats", note: "усі стати й статуси (Snow, Frost, Shroom, Ink, Spice, Shell, Block, Teeth, Bom, Haze, Overburn…)"}
  - {kind: fandom, url: "https://wildfrostwiki.com/Map", note: "мапа забігу: 3 зони, вузли подій, боси"}
  - {kind: fandom, url: "https://wildfrostwiki.com/Companions", note: "розстановка, вільне переміщення, recall"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wildfrost", note: "огляд, племена, Storm Bells, платформи"}
  - {kind: official, url: "https://wildfrostgame.com", note: "офіційний сайт (з Wikipedia)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Wildfrost", note: "пошук Steam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wildfrost+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [hp-damage, turn-enforcement, ai-opponent, telegraphed-intents, enemy-waves, round-currency, shop-between-levels, shop-catalog, inventory-items, dungeon-generation, combo-multiplier, daily-puzzle, save-progress, drag-drop-piece, mode-indicator, +lane-grid, +deck-draw, +card-sigils, +run-relics, +countdown-initiative, +status-stacks, +redraw-charge, +front-target, +free-reposition, +injury-carryover]
proposes: ["+trigger:counter_zero", "+trigger:turn_end", "+cond:frontmost", "+effect:tick_counter", "+effect:add_status", "+effect:draw", "+effect:recall", "+role:card", "+role:lane", "+ui:counter-badge", "+ui:bell-button", "+ui:wave-bell", "+ui:status-icons", "+window:map-window", "+window:choice-window", "+window:town-window", "+feature:run-map", "+feature:difficulty-modifiers", "+axis:session"]
author: opus
date: 2026-11-02
---

# Wildfrost — карткова битва на двох смугах, де ініціатива — це лічильники, що тікають до атаки

## Суть
Роглайк-декбілдер: на своїй половині поля (2 ряди × 3 слоти) гравець виставляє лідера й компаньйонів, проти них — така сама половина ворогів. У кожної бойової карти є **лічильник** (Counter): щоходу всі лічильники −1, на нулі карта бʼє найпередніший ворожий юніт свого ряду і лічильник скидається. Хід гравця — зіграти одну карту (компаньйона або предмет); головний ресурс — час: Snow заморожує чужі лічильники, Frost зменшує атаку, Shroom отруює. Загинув лідер — забіг скінчився.

## Поле і час
- Дві половини по 2 горизонтальні ряди (lanes) × 3 слоти; слот ближче до центру — «передній». Атака йде в найпередніший ворожий юніт **того самого ряду** (ключові слова змінюють ціль).
- Покроково: хід гравця = одна дія (зіграти карту / дзвін перездачі), потім усі лічильники −1 і спрацьовують нульові: спершу вороги, далі кожне поле зверху вниз, спереду назад.
- Хвилі ворогів: Wave Bell показує, скільки ходів до підкріплення; бій виграно, коли знищено всі хвилі.
- Інформація: лічильники, атака, HP і статуси всіх карт на столі видно (наміри телеграфовані часом); колода й порядок добору — приховані.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лідер | player | HP, атака, лічильник | бойова карта гравця; HP = 0 → кінець забігу |
| Компаньйон | ally | HP, атака, лічильник, здібність | ставиться у слот, лишається на полі, бʼє при 0 |
| Клункер (Clunker) | ally | Scrap замість HP | механізм; будь-яке влучання ≥1 знімає 1 Scrap |
| Предмет (Item) | card | атака/ефект | грається з руки в ціль, іде у скид |
| Junk / дрібні карти | card | — | слабкі предмети, що засмічують колоду (?) |
| Ворог | enemy | HP, атака, лічильник | бʼє за тим самим правилом лічильника |
| Бос / мінібос | boss | багато HP, Resist Snow | фінал зони; часто тримає лише 1 Snow |
| Гоблінг (Gobling) | enemy | — | несе Bling, дає винагороду при вбивстві |
| Слот | static | ряд, позиція | клітина поля для однієї карти |
| Wave Bell | spawner | ходів до хвилі | відлік до появи наступної хвилі ворогів |
| Redraw Bell | switch | заряд 4 ходи | скинути руку і добрати 6 |
| Charm | pickup | модифікатор | прикріплюється до карти між боями |
| Crown | pickup | — | коронована карта завжди в стартовій руці й грається без витрати ходу |

Статуси (стаки на карті): **Snow** — лічильник не тікає, реакції не спрацьовують, −1 у кінці ходу · **Frost** — −атака, скидається після атаки · **Shroom** — у кінці ходу шкода = Shroom, потім −1 · **Ink** — текст карти вимкнено, −1 щоходу · **Spice** — +атака, скидається після атаки · **Shell** — поглинає шкоду до HP · **Block** — скасовує одне влучання, −1 · **Teeth** — шкода атакувальнику при влучанні · **Bom** — +шкода, що отримує карта, не спадає · **Demonize** — наступна шкода ×2 · **Haze** — бʼє випадкового союзника · **Overburn** — при Overburn ≥ HP вибухає по своєму ряду · **Lumin** — подвоює числа ефектів · **Frenzy** — атакує N разів поспіль · **Reaction** — спрацьовує за умовою, а не за лічильником.

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО гравець робить одну дію: `input(play, companion, slot)` ЯКЩО `free(slot)` → `spawn(companion)`; або `input(play, item, target)` → ефект предмета, предмет у скид.
- КОЛИ `input(play, crowned_card)` → ТО `custom: «грається без витрати ходу»`.
- КОЛИ `input(move, companion, slot)` → ТО `move(a, slot)` / `swap` — вільно протягом свого ходу (без витрати дії).
- КОЛИ `input(recall, companion)` → ТО `custom: «effect recall: у скид, зняти дебафи, +5 HP»`; знову зіграти — коли добереться.
- КОЛИ `input(redraw_bell)` → ТО `custom: «скинути руку, effect draw(6)»`, `end_turn`; ЯКЩО `custom: «дзвін заряджений (4 ходи без нього)»` → без витрати ходу.
- КОЛИ `turn_end(player)` → ТО для кожної карти: ЯКЩО `not state(a, snow)` → `custom: «effect tick_counter(a, -1)»`.
- КОЛИ `custom: «trigger counter_zero(a)»` → ТО `damage(custom: «cond frontmost(enemy, same_row)», attack + spice − frost)`, `custom: «counter = max»`; Frenzy — повторити N разів.
- КОЛИ `contact(attack, target)` → ЯКЩО `state(target, block)` → `custom: «скасувати, block −1»`; інакше Shell → HP; ЯКЩО `state(target, teeth)` → `damage(attacker, teeth)`.
- КОЛИ `turn_end` → ТО Shroom: `damage(a, shroom)`, `shroom −1`; Snow/Ink/Haze: `−1`.
- КОЛИ `custom: «Overburn ≥ HP»` → ТО `custom: «вибух: шкода = Overburn собі й союзникам у ряду»`.
- КОЛИ `custom: «зовнішній ефект ставить лічильник = 0»` (Sun Rod) → ТО карта спрацьовує одразу.
- КОЛИ `timer(wave_bell == 0)` → ТО `wave_start`, `spawn_at(enemies, enemy_slots)`.
- КОЛИ `hp_zero(enemy)` → ТО `disappear_a`; кілька вбивств за хід → `combo` → більше Bling.
- КОЛИ `all_gone(enemy)` і хвиль більше нема → ТО `win` (бій), `window(map-window)`.
- КОЛИ `hp_zero(leader)` → ТО `lose` (кінець забігу, повернення в Snowdwell).
- КОЛИ `hp_zero(companion)` → ТО `disappear_a` до кінця бою; `custom: «стає Injured на наступний бій»` (?).
- Перемога (забіг): перемогти фінального боса (Frost Guardian / Emperor Shade) · Поразка: смерть лідера · Рахунок: нема; прогрес — розблокування в місті.

## Керування і ввід
- Миша/тач/геймпад: перетягнути карту з руки у слот або на ціль (`drag-drop-piece`); підсвічуються легальні слоти/цілі.
- Перетягування компаньйонів між своїми слотами — вільна дія; recall — тягнути в «кишеню» скиду.
- Клік по Redraw Bell — перездача; наведення на карту — підказка з поясненням ключових слів.
- Хід закінчується автоматично після зіграної карти (дзвін «кінець ходу» не потрібен).

## Вікна, меню, HUD
- `main-menu`: Continue / New Run, Daily Voyage, налаштування.
- `+window:town-window` — Snowdwell: будівлі (Tribe Hall, Pet House, Inventor's Hut, Icebreaker Cabin, Hot Spring, Frostoscope) відкривають нові карти, події, налаштування складності.
- `character-select` — вибір лідера з 3 випадкових і племені (Snowdwellers / Shademancers / Clunkmasters).
- `+window:map-window` — мапа забігу з розгалуженням: бої, боси, скрині, події.
- `+window:choice-window` — Frozen Travellers (1 з 3 компаньйонів), Treasure Chest (1 з 3 предметів), Charm Dispenser.
- `shop-window` — Woolly Snail (предмети, чарми, корона за Bling); Charm Merchant; Muncher (видалити до 2 карт); Shade Sculptor (дублювати предмет).
- `deck-window` / колода й склад команди між боями; прикріплення чармів і корон.
- `game-screen`: дві половини поля, рука з 6 карт, `+ui:counter-badge` (число-лічильник на карті), `+ui:status-icons` (стаки статусів), `+ui:bell-button` (Redraw Bell з індикатором заряду), `+ui:wave-bell` (ходів до хвилі), колода і скид, `coins` (Bling).
- `end-screen` — кінець забігу; `achievements-window`.
- Переходи: town → character-select → map ↔ (бій / подія / магазин) → … → бос → end-screen → town.

## Фічі поза полем
- `meta-progression`: місто Snowdwell і будівлі відкривають нові карти/події; переможений лідер стає наступним Frost Guardian.
- `+feature:difficulty-modifiers` — Storm Bells (після першої перемоги): ручне додавання ускладнень; максимум відкриває справжнього боса.
- `mode-daily` — Daily Voyage з фіксованими умовами.
- `autosave` забігу, `achievements`, `codex`-подібний перегляд карт (?).
- `+feature:run-map` — мапа забігу (як Inscryption/Slay the Spire); `+run-relics` ≈ чарми й корони.
- Поранений компаньйон з програного забігу може зʼявитись вузлом у наступному.

## Варіації й родичі
- Родичі: Inscryption (смуги + колода, але атака щоходу), Slay the Spire (мапа й наміри), Plants vs. Zombies (смуги), Hearthstone (юніти з HP/атакою).
- **Осі варіацій**: ініціатива — щоходу всі / лічильник до атаки / швидкість-черга (ATB) · ціль — навпроти / найпередніший у ряду / вибір гравця · ресурс ходу — мана / одна карта за хід / жертва · поле — 1 ряд / 2 ряди × 3 / сітка.
- Модифікатори часу як окремий «жанр статусів»: заморозити лічильник (Snow), змусити спрацювати зараз (Sun Rod), прискорити/сповільнити.

## Цікавинки для курсу
- Ініціатива через лічильники: кожна карта — таймер, що тікає до дії; Snow як «пауза» чужого таймера — 🥉 (простий, але дуже виразний планувальник).
- Система статусів-стаків, що спадають у кінці ходу, з порядком застосування (Block → Shell → HP; Bom/Demonize множать) — 🥈.
- Атака в найпередніший слот ряду + вільне переміщення своїх: тактика розстановки як головне рішення — 🥉.
- Дзвін перездачі, що заряджається пропуском (4 ходи → безкоштовно) — 📎.
- Wave Bell: хвилі ворогів з відліком як тиск на швидкість убивства — 📎.
- Мапа забігу + метапрогресія міста — 🥈 (окремі вікна й збереження між забігами).

## Мапа на каталог
- Є: `hp-damage` · `turn-enforcement` (одна дія за хід) · `ai-opponent` · `telegraphed-intents` ↔ видимі лічильники ворогів · `enemy-waves` ↔ Wave Bell · `round-currency` ↔ Bling · `shop-between-levels` + `shop-catalog` ↔ Woolly Snail · `inventory-items` ↔ чарми/корони · `dungeon-generation` ↔ мапа забігу · `combo-multiplier` ↔ комбо-вбивства · `daily-puzzle` ↔ Daily Voyage · `save-progress` · `drag-drop-piece` · `mode-indicator` ↔ заряд дзвону.
- **Нема** → пропозиції карток:
  - `+lane-grid` — див. plants-vs-zombies; тут 2 ряди × 3 слоти з кожного боку.
  - `+deck-draw`, `+card-sigils` — див. inscryption (ключові слова/чарми).
  - `+run-relics` — див. isle-of-arrows (чарми, корони).
  - `+countdown-initiative` «Лічильник до дії» · game-logic/opponent · 🥉 · слоти {counter, reset}.
  - `+status-stacks` «Стаки статусів, що спадають» · entities/state · 🥈 · слоти {statuses: list, decay: turn_end|on_hit|on_attack}.
  - `+redraw-charge` «Перездача руки із зарядом» · game-logic/economy · 📎 · слот {charge_turns}.
  - `+front-target` «Атака в найпередніший у ряду» · entities/combat · 🌱.
  - `+free-reposition` «Вільна перестановка своїх юнітів» · interface/input · 📎.
  - `+injury-carryover` «Поранення переходить у наступний бій» · entities/state · 📎.

## Пропозиції до словників
- `+trigger:counter_zero` — лічильник карти досяг 0 (спрацювання); `+trigger:turn_end` ⏳ — підтвердження (тут тікають статуси).
- `+cond:frontmost` — сутність найближча до центру у своєму ряду.
- `+effect:tick_counter` — змінити лічильник карти (−1 щоходу, Snow блокує, Sun Rod обнуляє); `+effect:add_status` — додати N стаків статусу; `+effect:draw` — з inscryption; `+effect:recall` — повернути юніт з поля в руку/скид.
- `+role:card`, `+role:lane` — з inscryption/PvZ.
- `+ui:counter-badge` — число до дії на сутності; `+ui:status-icons` — іконки стаків; `+ui:bell-button` — підтвердження; `+ui:wave-bell` — відлік до хвилі.
- `+window:map-window`, `+window:choice-window` — підтвердження; `+window:town-window` — хаб метапрогресії з будівлями.
- `+feature:run-map` — підтвердження; `+feature:difficulty-modifiers` — ручні ускладнення (Storm Bells, як Ascension/Heat).
- `+axis:session` — `match` (забіг з 9 боїв).

## Джерела
- ⭐ [Wildfrost Wiki: Getting Started](https://wildfrostwiki.com/Getting_Started) — 2 ряди, порядок відліку, рука 6, Redraw Bell і заряд, корони, Bling, Wave Bell.
- [Wildfrost Wiki: Stats](https://wildfrostwiki.com/Stats) — HP/Scrap/Attack/Counter/Reaction/Frenzy і всі баффи/дебаффи з точними правилами.
- [Wildfrost Wiki: Map](https://wildfrostwiki.com/Map) — 3 зони, 9 боїв, вузли подій і магазинів.
- [Wildfrost Wiki: Companions](https://wildfrostwiki.com/Companions) — розстановка, вільне переміщення, recall (+5 HP, зняття дебафів).
- [Wikipedia: Wildfrost](https://en.wikipedia.org/wiki/Wildfrost) — 6 слотів у двох смугах, різні інтервали атак, племена, Storm Bells, платформи.
- [Офіційний сайт](https://wildfrostgame.com) · Steam: пошук «Wildfrost» · YouTube: пошук «wildfrost gameplay».

## Непевне
- (?) Injury: що саме дає «поранений» компаньйон у наступному бою (половина HP/атаки?) і як лікується; Bell of Death у вікі не описаний.
- (?) Чи переміщення компаньйона справді не витрачає хід (вікі: «вільно протягом свого ходу»).
- (?) Точний порядок: лічильники тікають після дії гравця чи на початку ходу ворога.
- (?) Junk і повний список ключових слів (Barrage, Aimless, Smackback…) не перевіряв.
