---
title: Noita
slug: noita
aka: []
family: dig-gravity
also: [roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2020
platforms: [PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Noita_(video_game)", best: true, note: "огляд: кожен піксель симульований, реакції, жезли, Holy Mountain, біоми, permadeath"}
  - {kind: fandom, url: "https://noita.wiki.gg/wiki/Materials", note: "wiki.gg: класи матеріалів, щільність, durability/hardness для копання вибухом"}
  - {kind: fandom, url: "https://noita.wiki.gg/wiki/Wands", note: "жезл як черга заклинань: shuffle, spells/cast, cast delay, recharge, mana, capacity, always cast"}
  - {kind: fandom, url: "https://noita.wiki.gg/wiki/Holy_Mountain", note: "безпечні зони: перки, крамниця, обвал, «гнів богів»"}
  - {kind: fandom, url: "https://noita.wiki.gg/wiki/Falling_Sand_Game", note: "Noita серед falling-sand ігор: процедурний світ + rigid bodies"}
  - {kind: fandom, url: "https://noita.wiki.gg/wiki/Polymorphine", note: "приклад «плями»-статусу від рідини"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Noita", note: "пошук Steam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Noita+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, gravity-fall, cell-transform, interaction-table, destructible-blocks, explode-area, chain-detonation, projectile-shot, shoot-cooldown, hp-damage, environment-death, player-death, permadeath, status-effects, run-relics, shop-between-levels, shop-catalog, round-currency, item-pickup, inventory-items, inventory-limit, dungeon-generation, stairs-levels, player-camera, particles, game-loop, command-program, +falling-sand-cell, +density-displacement, +phase-transition, +fire-spread, +rigid-body-debris, +material-durability, +spell-queue, +stain-status, +safe-zone-shop, +angered-guardian]
proposes: ["+trigger:submerged", "+cond:durability", "+cond:material", "+effect:ignite", "+effect:stain", "+effect:kick", "+role:material", "+window:wand-editor", "+ui:mana-bar", "+ui:levitation-bar", "+card:spell-queue", "+card:stain-status", "+card:material-durability", "+card:rigid-body-debris", "+card:safe-zone-shop", "+card:angered-guardian", "+card:fire-spread", "+axis:field-pixel"]
author: opus
date: 2026-11-09
---

# Noita — роглайк, де кожен піксель — клітина фізичної симуляції, а заклинання — програма в жезлі

## Суть
Відьма-мандрівниця спускається крізь процедурні біоми до Лабораторії, де чекає фінальний бос. Світ — величезна falling-sand симуляція: майже кожен піксель — матеріал (пісок, вода, лава, дерево, газ), що падає, тече, горить і реагує з сусідами. Зброя — жезли, кожен з яких є чергою заклинань (снаряди, модифікатори, мультикасти, тригери), тож бій і копання — це «програмування» жезла. Смерть остаточна; вороги й власні помилки вбивають з одного удару («Noita'd»).

## Поле і час
- **Шар пікселів**: світ — сітка клітин-пікселів; кожна має матеріал. Класи: тверді (не рухаються, лише руйнуються/перетворюються), порошки (падають, насипають купи), рідини (течуть, вирівнюються в озера, шаруються за щільністю), гази (без колізій, «падають угору»), вогонь і органіка.
- **Шар тіл**: Box2D-обʼєкти (уламки, ящики, «вільні тверді») — ціле тіло з фізикою; можна кинути або копнути у ворога.
- **Шар сутностей**: відьма, вороги, предмети, снаряди — ходять і взаємодіють із пікселями.
- Вертикаль: 8 біомів основного шляху (від Шахт до Лабораторії), між ними — Holy Mountain; кожна зона псевдовипадково згенерована; є приховані біоми.
- Real-time; камера слідує за гравцем; видно околицю (`info: partial`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Відьма (Mina) | player | HP, золото, інвентар (жезли + предмети) | біг, стрибок, левітація (?); стріляє жезлом; копає ногою предмети |
| Твердий матеріал (камінь, цегла, метал, дерево, мʼясо…) | static | durability 4…14, hardness (HP пікселя) | не рухається; руйнується вибухом/снарядом, якщо сила > durability |
| Порошок (пісок, ґрунт, порох, сніг…) | terrain | — | падає, насипається; порох вибухає від вогню |
| Рідина (вода, олія, кислота, лава, кров, токсичний мул…) | terrain | щільність | тече, вирівнюється; важча тоне під легшою |
| Магічна рідина (поліморфін, телепортатій…) | terrain | — | як рідина + ефект при дотику (пляма-статус) |
| Газ (пара, дим, отруйний газ) | terrain | — | підіймається; пара конденсується в дощ; дим душить |
| Вогонь | hazard | — | поширюється по горючому, лишає дим |
| Фізичне тіло (уламок, ящик) | object | маса | падає з інерцією; удар — шкода |
| Ворог | enemy | HP, опір | ходить/літає, стріляє; може бути вбитий середовищем |
| Жезл | pickup | shuffle, spells/cast, cast delay, recharge, mana max, mana charge, capacity, spread, always cast | черга заклинань |
| Заклинання | pickup | тип: снаряд / модифікатор / мультикаст / тригер / утиліта; мана | елемент черги жезла |
| Колба (flask) | container | матеріал усередині | набирає рідину, виливає або кидається |
| Holy Mountain | zone | цегла з високою durability | без ворогів; перки, крамниця, лікування, редагування жезлів |
| Вівтар перків | switch | зазвичай 3 перки | взяти один → пасивний ефект на забіг |
| Стеварі (страж) | boss | — | зʼявляється, якщо пошкодити цеглу Holy Mountain |
| Скриня, сфера (orb) | pickup | — | випадковий вміст; сфери — мета-прогрес і кінцівки |
| Фінальний бос (Kolmisilmä) | boss | — | у Лабораторії |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `cell(cell, powder)` and `free(below)` → ТО `fall(cell)`; інакше `custom: «сповзає по діагоналі, якщо вільно»`.
- КОЛИ `tick` → ЯКЩО `cell(cell, liquid)` → ТО `fall(cell)` або `custom: «розтікається вбік до вирівнювання»`.
- КОЛИ `tick` → ЯКЩО `cell(a, liquid)` and `cell(below, liquid)` and `custom: «a щільніша за нижню»` → ТО `swap(a, below)`.
- КОЛИ `tick` → ЯКЩО `cell(cell, gas)` → ТО `custom: «рух угору (обернена гравітація)»`.
- КОЛИ `adjacent(lava, water)` → ТО `transform(lava, rock)`, `transform(water, steam)`.
- КОЛИ `custom: «пара охолола вгорі»` → ТО `transform(steam, water)` (дощ).
- КОЛИ `adjacent(fire, wood|oil|…)` → ЯКЩО `prob(p)` → ТО `set_state(neighbour, burning)`; після згоряння `transform(wood, smoke)`.
- КОЛИ `enter(player, smoke)` → ТО `custom: «задуха: шкода без повітря»` (?).
- КОЛИ `adjacent(liquid_a, liquid_b)` → ЯКЩО `custom: «пара є в таблиці реакцій»` → ТО `transform(both, product)` (алхімія).
- КОЛИ `contact(player|enemy, magic_liquid)` → ТО `set_state(a, stain)`; поліморфін → `transform(a, sheep)`; занурення — 20 с.
- КОЛИ `custom: «вибух/снаряд з енергією E і силою D»` → ЯКЩО `custom: «durability клітини < D»` → ТО `custom: «енергія витрачає hardness пікселів по променях»`, `set_cell(cell, empty)`; інакше `block`.
- КОЛИ `input(fire)` → ЯКЩО `counter(mana, >=, cost)` and `custom: «cast delay минув»` → ТО `custom: «читає з черги spells/cast блоків зліва направо; модифікатори застосовуються до наступного снаряда»`, `spawn(projectile)`, `counter(mana, -cost)`.
- КОЛИ `custom: «черга жезла вичерпана»` → ТО `timer(start, recharge)` → `custom: «черга з початку»`; shuffle-жезл — `custom: «перемішати порядок»`.
- КОЛИ `contact(trigger_projectile, any)` → ТО `custom: «випускає payload — наступні заклинання черги»`.
- КОЛИ `tick` → ТО `counter(mana, +charge)` для всіх жезлів, навіть не в руках.
- КОЛИ `custom: «деякі снаряди (Giga Disc) прорізають ґрунт і летять назад до мага»` → ЯКЩО `contact(projectile, player)` → ТО `damage(player, n)`.
- КОЛИ `input(kick)` → ЯКЩО `in_range(player, body, 1)` → ТО `custom: «копняк: імпульс тілу»`; КОЛИ `contact(body, enemy)` → ТО `damage(enemy, n ~ швидкість)`.
- КОЛИ `enter(player, holy_mountain)` → ТО `heal(player, full)`, `custom: «оновлення заклинань»`, `window(wand-editor)` доступне.
- КОЛИ `input(pick perk)` → ТО `choose(3 perks)`, `set_state(player, perk)` до кінця забігу.
- КОЛИ `custom: «гравець минув похилий відрізок виходу»` → ТО `set_cell(ceiling, brick)` (обвал), `custom: «зона прокляття ~21 с, 2 шкоди/с»`.
- КОЛИ `destroyed(holy_mountain_brick)` → ТО `message(«You have angered the gods»)`, `spawn(stevari)` і в кожній наступній Holy Mountain.
- КОЛИ `hp_zero(player)` → ТО `lose`, `game_over` (permadeath; частина відкриттів лишається).
- КОЛИ `hp_zero(final_boss)` → ТО `win`; варіанти кінцівок за кількістю зібраних сфер.
- Перемога: перемогти боса Лабораторії (і секретні кінцівки). Поразка: HP 0. Рахунок: золото й статистика забігу (?).

## Керування і ввід
- Клавіатура + миша: WASD — рух, стрибок/левітація (?); миша — приціл; ЛКМ — постріл жезлом; ПКМ/клавіша — кинути предмет; копняк; колесо/цифри — вибір жезла/предмета.
- Інвентар: перетягування заклинань між слотами жезлів (лише в Holy Mountain або з перком Tinker with Wands Everywhere).
- Колба: ЛКМ — розлити рідину, ПКМ — кинути (?); набирає рідину, якщо занурити.

## Вікна, меню, HUD
- `main-menu`: нова гра, продовжити, налаштування, моди, Nightmare mode, вихід (?).
- `game-screen`: світ; HUD — `hp-bar`, `mana-bar` і перезарядка жезла, `levitation-bar`, `coins` (золото), `inventory-bar` (4 жезли + 4 предмети, ?), іконки статусів (мокрий, горить, пляма).
- `inventory-window` + `wand-editor` — характеристики жезла й слоти заклинань, drag-n-drop.
- `shop-window` (Holy Mountain): 5 жезлів або 10 заклинань з цінами.
- `choose`-вибір перка на вівтарі: `upgrade-window`.
- `codex-window` «Progress»: відкриті заклинання, вороги, перки (мета-прогрес) (?).
- `end-screen` — смерть: причина й статистика забігу.
- `settings-window`, `mod-support`-екран модів.

## Фічі поза полем
- `mode-hardcore` за замовчуванням (permadeath), `meta-progression` (відкриті заклинання й перки лишаються), `achievements`, секретні біоми й кінцівки.
- `mod-support` (офіційні моди в меню), Nightmare Mode, Twitch-інтеграція (глядачі голосують за події).
- Seed світу випадковий; розклад біомів фіксований, вміст — процедурний.

## Варіації й родичі
- У сімʼї: The Powder Toy, Sandspiel, Sandboxels — та сама клітинна фізика, але як пісочниця без мети; Noita додає аватара, ворогів і роглайк-петлю. Dig Dug / Mr. Driller — копання як ядро; тут копання — побічний ефект вибухів.
- Родичі-роглайки: Spelunky (руйнований рельєф бомбами, сітка тайлів замість пікселів), Terraria (тайловий світ).
- **Осі варіацій**: деталізація поля — «тайл 16 px (Spelunky) / піксель (Noita)»; руйнування — «будь-яка клітина / за durability»; зброя — «фіксована / програмована черга»; світ — «пісочниця / процедурний з метою».

## Цікавинки для курсу
- Falling-sand клітинний автомат з класами матеріалів (порошок/рідина/газ) і щільністю — 🥈.
- Таблиця реакцій «матеріал × матеріал → продукти» (лава + вода → камінь + пара) — 🥉.
- Вибух з енергією й durability: руйнує лише слабші пікселі — 🥉.
- Жезл як черга заклинань (модифікатори до наступного снаряда, мультикаст, тригер з payload, recharge після вичерпання) — 🥇.
- Пляма-статус від рідини (поліморф → вівця) — 📎.
- Безпечна зона-крамниця, яка карає за руйнування своїх стін — 📎.
- Пара → дощ: фазовий перехід, що замикає цикл води — 📎.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` ↔ порошки, рідини · `cell-transform` ↔ реакції · `interaction-table` ↔ алхімія · `destructible-blocks` · `explode-area` · `chain-detonation` ↔ порох, бочки · `projectile-shot` · `shoot-cooldown` ↔ cast delay · `hp-damage` · `environment-death` · `player-death` · `permadeath` · `status-effects` ↔ мокрий/горить/пляма · `run-relics` ↔ перки · `shop-between-levels` + `shop-catalog` ↔ Holy Mountain · `round-currency` ↔ золото · `item-pickup` · `inventory-items` · `inventory-limit` · `dungeon-generation` · `stairs-levels` ↔ біоми вниз · `player-camera` · `particles` · `game-loop` · `command-program` ↔ жезл як програма.
- **Нема** → пропозиції карток:
  - `+falling-sand-cell` (повтор з Powder Toy/Sandspiel) · `+density-displacement` (повтор) · `+phase-transition` (повтор).
  - `+fire-spread` «Вогонь поширюється по горючому» · entities/state · 📎 · слот {chance}.
  - `+rigid-body-debris` «Уламки як фізичні тіла поверх клітин» · entities/move · 🥇.
  - `+material-durability` «Руйнування за міцністю матеріалу» · entities/interact · 📎 · слот {durability}.
  - `+spell-queue` «Зброя як черга команд-модифікаторів» · entities/combat · 🥇 · слоти {per_cast, recharge, shuffle}.
  - `+stain-status` «Статус від контакту з рідиною» · entities/state · 📎.
  - `+safe-zone-shop` «Безпечна зона з крамницею між рівнями» · game-logic/economy · 🌱.
  - `+angered-guardian` «Страж за руйнування захищеного» · entities/spawn · 📎.

## Пропозиції до словників
- `+trigger:submerged` — сутність повністю в рідині (статус за 20 с у поліморфіні; утоплення).
- `+cond:durability` — міцність клітини менша за силу удару; `+cond:material` — клітина належить класу матеріалу (порошок/рідина/газ).
- `+effect:ignite` — підпалити клітину/сутність; `+effect:stain` — накласти статус-пляму від матеріалу; `+effect:kick` — копнути фізичне тіло.
- `+role:material` — клітина-матеріал симуляції (повтор з Powder Toy/Sandspiel).
- `+window:wand-editor` — редактор слотів зброї; `+ui:mana-bar`, `+ui:levitation-bar`.
- `+axis:field-pixel` — поле, де клітина = піксель і тайлів як таких нема (значення осі `field`).

## Джерела
- ⭐ [Wikipedia: Noita](https://en.wikipedia.org/wiki/Noita_(video_game)) — симуляція пікселів, реакції (лава + вода, пара → дощ, дерево → дим), Box2D-копняк, жезли, Holy Mountain, 8 біомів, permadeath, моди.
- [Noita Wiki: Materials](https://noita.wiki.gg/wiki/Materials) — класи матеріалів, щільність, durability 4…14, hardness, TNT проти Unstable Crystal.
- [Noita Wiki: Wands](https://noita.wiki.gg/wiki/Wands) — усі параметри жезла й порядок читання заклинань.
- [Noita Wiki: Holy Mountain](https://noita.wiki.gg/wiki/Holy_Mountain) — вміст, обвал, прокляття 21 с, Стеварі.
- [Noita Wiki: Polymorphine](https://noita.wiki.gg/wiki/Polymorphine) — пляма-статус, вівці, 20 с занурення.
- [Noita Wiki: Falling Sand Game](https://noita.wiki.gg/wiki/Falling_Sand_Game) — місце Noita серед falling-sand ігор.

## Непевне
- (?) Левітація з обмеженою енергією, кількість слотів інвентаря (4+4), задуха в диму як окрема механіка — з памʼяті, у відкритих джерелах лише «дим може задушити».
- (?) Точний алгоритм оновлення пікселів (порядок, чанки, симуляція поза екраном) — джерела не описують.
- (?) Пункти меню, `codex-window` «Progress», раховування золота як очок.
- (?) Як саме поширюється вогонь (ймовірність на тік).
