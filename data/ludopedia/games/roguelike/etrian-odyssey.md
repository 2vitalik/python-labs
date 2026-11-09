---
title: Etrian Odyssey
slug: etrian-odyssey
aka: [Sekaiju no Meikyuu, 世界樹の迷宮, EO, Etrian Odyssey HD, Etrian Odyssey Untold]
family: roguelike
also: [tactics]
klass: hybrid
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 2007
platforms: [Nintendo DS, Nintendo 3DS (Untold), Switch, PC (HD, 2023)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Etrian_Odyssey_(video_game)", best: true, note: "суть: кроки по сітці, час іде лише від дії, мапа стилусом з обмеженим набором іконок, FOE ходять разом із гравцем"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Etrian_Odyssey", note: "серія: II–V, Untold (Classic/Story), Nexus, HD-колекція"}
  - {kind: other, url: "https://retronauts.com/article/611/etrian-odyssey-v-a-diy-tribute-to-the-art-of-game-mapping", note: "що на мапі автоматично (пройдені клітини), що вручну (стіни, кольори, іконки), ліміт іконок, нагорода за повну мапу"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Etrian_Odyssey_Untold:_The_Millennium_Girl", note: "режими Classic/Story, складність Picnic/Normal/Expert, автомапа, біг"}
  - {kind: steam, url: "https://store.steampowered.com/app/1868180/Etrian_Odyssey_HD/", note: "HD-ремастер: 9 класів, кодекс монстрів, журнал квестів, дерево навичок, вибір складності, слоти сейвів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=etrian+odyssey+gameplay+map+drawing", note: "пошук; геймплей і малювання мапи"}
stage: v1
coverage: 55
mechanics: [move-by-input, move-4dir, orientation-state, impassable-cells, enemy-patrol, chase-player, reinforcements, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, round-currency, shop-catalog, shop-between-levels, unit-xp-skills, status-effects, stairs-levels, player-death, fog-of-war, map-window, codex-window, character-select, difficulty-levels, save-game, save-multi-slot, gui-render, cell-click, dot-mark, +first-person-grid, +hand-drawn-map, +map-icon-limit, +auto-floor-trace, +random-encounter, +party-formation, +skill-tree, +gathering-point, +return-to-town-item, +quest-board, +map-completion-reward, +town-hub]
proposes: ["+trigger:noticed", "+effect:start_battle", "+effect:return_to_town", "+role:foe", "+ui:map-tool-palette", "+ui:encounter-gauge", "+ui:map-icon-counter", "+window:town-hub", "+window:battle-screen", "+window:quest-board", "+window:guild-roster", "+feature:hand-drawn-map", "+feature:map-completion-reward", "+axis:view=first-person", "+card:hand-drawn-map"]
author: opus
date: 2026-11-09
---

# Etrian Odyssey — данжен-кроулер від першої особи, де мапу підземелля малює сам гравець стилусом на нижньому екрані

## Суть
Загін із 5 найманців крок за кроком спускається в лабіринт під деревом Іґґдрасиль: верхній екран — вид від першої особи, нижній — **порожній міліметровий папір, на якому гравець стилусом малює стіни, фарбує підлогу й ставить іконки**. Час іде лише від дії; кожен крок може запустити випадковий покроковий бій. Особливі вороги FOE видно на мапі: вони ходять **разом із гравцем** за власним шаблоном і є головоломкою «прослизнути між ними». Мапа — не довідка, а інструмент гри: за точну мапу поверху дають нагороду, а якість мапи — на совісті гравця.

## Поле і час
- Квадратна сітка клітин, поверхи («страти» по кілька поверхів), вид від першої особи з орієнтацією загону; крок = 1 клітина, поворот на 90°.
- Покроково: кожен крок або дія — тік; FOE роблять свій крок у відповідь; випадкові бої — окремий покроковий екран.
- Шари мапи: **автоматичні** відмітки пройдених клітин (Retronauts: «кожен крок записується квадратом, пройдені клітини зеленіють») + **ручні** стіни, кольори підлоги, іконки.
- Видимість: туман — бачиш лише перед собою на кілька клітин; мапа знає тільки те, що ти намалював або пройшов.
- Між експедиціями — місто (Етрія): відновлення, покупки, найм, квести. Вихід/вхід у лабіринт через вхід на 1-му поверсі або телепорт на вже закартографований поверх.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Загін | player | до 5 персонажів, передній/задній ряд, орієнтація | рух як одна фігура: вперед/назад/вбік, поворот |
| Персонаж (клас) | ally | HP, TP, рівень, очки навичок, 9 класів у HD | у бою — команда на хід; навички з дерева |
| Звичайний ворог | enemy | HP, атаки, слабкості | невидимий на мапі; зʼявляється у випадковому бою |
| FOE (Field On Enemy) | enemy | дуже сильний, видимий на мапі | ходить на кожен крок гравця; більшість — по колу/маршруту; помітивши загін — прямо до нього |
| Бос страти | boss | — | стоїть у фіксованій кімнаті; кінець страти |
| Стіна | static | — | межа; лише її реєструє перевірка мапи (Retronauts) |
| Двері | gate | — | відкриваються проходом |
| Прихований прохід | gate | — | прохід крізь «стіну»; іконка на мапі |
| Сходи вгору/вниз | static | — | перехід між поверхами |
| Скриня | container | вміст | один раз; вміст можна позначити на мапі |
| Точка збирання | resource | Take/Chop/Mine (?) | дає матеріали на продаж; потрібна навичка (?) |
| Вода, шкідлива підлога | terrain | — | гравець фарбує кольором; деякі FOE переходять воду (EO V) |
| Плита-транспортер / конвеєр | terrain | напрям | зсуває загін; окрема іконка (пізні ігри) |
| Важіль / перемикач | switch | — | піднімає/опускає перешкоди (EO V: блокує шлях FOE) |
| Ниточка Аріадни | pickup | одноразова | повертає загін у місто (?) |
| Мапа гравця | mark | стіни, кольори, іконки (ліміт на поверх) | намальоване гравцем; гра не виправляє |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(forward|back|strafe)` → ЯКЩО `free(target)` → ТО `move(party, dir)`; інакше `block`.
- КОЛИ `input(turn)` → ТО `face(party, ±90°)`.
- КОЛИ `enter(party, cell)` → ТО `custom: «клітина на мапі позначається пройденою»` (автоматично).
- КОЛИ `input(stylus: pen)` → ТО `mark(map edge, wall)`; `input(stylus: brush)` → ТО `paint(map cell, color)`.
- КОЛИ `input(stylus: icon)` → ЯКЩО `count(icons on floor, <, limit)` → ТО `mark(map cell, icon)`; інакше `block`.
- КОЛИ `input(eraser)` → ТО `unmark(map cell)`.
- КОЛИ `turn_end(party)` → ТО `move(FOE, next on route)`.
- КОЛИ `custom: «FOE помітив загін»` → ТО `move(FOE, toward party)` кожен хід.
- КОЛИ `contact(FOE, party)` → ТО `custom: «бій з FOE»`; КОЛИ `turn_end(battle round)` → ЯКЩО `custom: «інший FOE дійшов до клітини бою»` → ТО `spawn(FOE)` у бій (підкріплення).
- КОЛИ `turn_end(party)` → ЯКЩО `rng(p)` → ТО `custom: «випадковий бій»` → `window(battle-screen)`.
- КОЛИ `input(command per member)` → ТО `custom: «раунд бою: усі діють за швидкістю»`; атака задніми рядами — слабша, крім дальньої зброї й заклинань (?).
- КОЛИ `hp_zero(member)` → ТО `set_state(member, dead)`; ЯКЩО `count(alive members, =, 0)` → ТО `lose` (game over, перезавантаження сейву).
- КОЛИ `all_gone(enemy in battle)` → ТО `custom: «досвід і матеріали»`; ЯКЩО `counter(xp, ≥, threshold)` → ТО `custom: «рівень +1, очко навички»`.
- КОЛИ `input(skill point)` → ЯКЩО `custom: «передумова в дереві виконана»` → ТО `custom: «навичка +1»`.
- КОЛИ `input(gather)` → ЯКЩО `enter(party, gathering point)` → ТО `give(party, material)`; ЯКЩО `rng(p)` → ТО `custom: «засідка»` (?).
- КОЛИ `input(use Ariadne thread)` → ТО `teleport(party, town)` (?).
- КОЛИ `custom: «мапа поверху збігається з еталоном»` → ТО `give(material)`, `unlock(warp to floor)` (Retronauts; рахуються лише стіни).
- КОЛИ `input(sell material)` → ТО `currency(+n)`, `unlock(new shop items)` (?).
- КОЛИ `died(stratum boss)` → ТО `unlock(next stratum)`.
- КОЛИ `input(inn)` → ТО `heal(party, full)`, `currency(−n)`.
- Перемога: пройти всі страти й фінального боса. Поразка: загинув весь загін. Рахунку нема.

## Керування і ввід
- Хрестовина / кнопки: крок, поворот, стрейф; A — взаємодія.
- Стилус на нижньому екрані: перо (стіни по лініях сітки), пензель (колір клітини), палітра іконок (двері, сходи, скриня, точка збирання, прихований прохід, транспортер, FOE, примітка), гумка, зум.
- Бій: меню команд на кожного члена загону (атака, навичка, предмет, захист, втеча).
- Untold і HD: опційна автомапа (?), біг, вибір складності.

## Вікна, меню, HUD
- `game-screen`: верх — вид від першої особи, низ — мапа поверху з позицією й орієнтацією загону, FOE на мапі; `encounter-gauge` — індикатор близькості бою (?); `map-tool-palette`; `map-icon-counter` (?).
- `battle-screen`: вороги-спрайти, `party-portraits` з `hp-bar`/TP, меню команд, `message-log`.
- `town-hub`: заклади міста — гільдія (найм і загін), трактир (відпочинок, сейв), крамниця (продаж матеріалів → нові товари), шинок (квести), лікарня (воскресіння), ратуша (місії) (?).
- `guild-roster` (`character-select`): створення персонажа, клас, портрет, імʼя; склад загону й рядів.
- `inventory-window`, `codex-window` (кодекс монстрів і предметів), `quest-board` / журнал квестів, дерево навичок.
- `map-window` — повна мапа поверху (той самий нижній екран; у HD — окремий режим редактора) (?).
- `main-menu` (новий / продовжити), `save-slots` (HD), `end-screen` (game over).
- Переходи: місто → вхід у лабіринт → `game-screen` ⇄ `battle-screen`; ниточка/телепорт → місто.

## Фічі поза полем
- Створення загону: 5 активних, решта — у гільдії; міняються лише в місті.
- Прогресія: рівні, очки навичок у дерево класу; матеріали → нове спорядження в крамниці.
- Квести й місії з міста; кодекс монстрів.
- `difficulty-presets` (Untold: Picnic / Normal / Expert; HD — вибір складності), `save-slots` (HD), один слот в Untold (критика).
- Untold: режими Classic (свій загін) і Story (готові персонажі), обидва з ручною мапою.
- Нагорода за повну мапу поверху (EO V за Retronauts).

## Варіації й родичі
- Серія: II (нові іконки мапи), III (плавання морем), IV (повітряний корабель над картою світу, FOE на ній), V (палітри інструментів, 8 кольорів, іконки големів і важелів), Nexus; спін-офи Etrian Mystery Dungeon ([mystery-dungeon](mystery-dungeon.md)).
- Предки: [dungeon-master](dungeon-master.md) (клітинний кроулер, мапу малюють на папері), Wizardry; сучасні: [legend-of-grimrock](legend-of-grimrock.md) (автомапа), [dungeon-encounters](dungeon-encounters.md), Persona Q (той самий рушій мапи).
- Осі варіацій: **мапа** (немає / автоматична / автоматичні клітини + ручні стіни / цілком ручна) · **видимі вороги** (лише випадкові / FOE на мапі / усі видимі) · **час FOE** (крок за крок / real-time).

## Цікавинки для курсу
- Ручна мапа: сітка-редактор з пером по ребрах, пензлем по клітинах і лімітом іконок — 🥉 (два шари: ребра й клітини).
- Звірка мапи гравця з еталоном лише за стінами → нагорода — 📎.
- FOE: патруль по маршруту, на кожен крок гравця; помітив — переслідує; інший FOE може дійти в бій — 🥉.
- Індикатор випадкового бою, що росте з кроками — 🌱.
- Дерево навичок з передумовами й очками за рівень — 📎.
- Місто-хаб: продаж матеріалів відкриває нові товари — 📎.

## Мапа на каталог
- Є: `move-4dir` + `orientation-state` (рух з поворотом) · `impassable-cells` · `enemy-patrol` + `chase-player` (FOE) · `reinforcements` (FOE доходить у бій) · `hp-damage` · `inventory` · `item-pickup` · `round-currency` · `shop-catalog` · `unit-xp-skills` · `status-effects` · `stairs-levels` · `player-death` · `fog-of-war` · `map-window` · `codex-window` · `character-select` · `difficulty-levels` · `save-multi-slot` · `cell-click` (стилус) · `dot-mark` (іконки).
- **Нема** → пропозиції карток:
  - `+hand-drawn-map` «Мапу малює гравець: ребра-стіни, колір клітин, іконки» · interface/input · 🥉 · слоти {tools, icon_limit}.
  - `+auto-floor-trace` «Пройдені клітини позначаються автоматично» · interface/render · 🌱.
  - `+map-icon-limit` «Ліміт іконок на поверх» · interface/input · 🌱 · слот {limit}.
  - `+map-completion-reward` «Нагорода за мапу, що збіглася з еталоном» · game-logic/goals · 📎.
  - `+random-encounter` «Випадковий бій на кроці» · entities/spawn · 🌱 · слот {p}.
  - `+party-formation` «Передній/задній ряд загону» · entities/combat · 📎.
  - `+skill-tree` «Дерево навичок з передумовами» · game-logic/economy · 📎.
  - `+gathering-point` «Точка збирання матеріалів» · entities/interact · 🌱.
  - `+return-to-town-item` «Предмет повернення в хаб» · entities/interact · 🌱.
  - `+quest-board` «Дошка квестів у хабі» · game-logic/goals · 📎.
  - `+town-hub` «Місто між експедиціями з закладами» · interface/menus · 📎.

## Пропозиції до словників
- `+trigger:noticed` — ворог помітив гравця й перейшов у переслідування (FOE; як у Brogue).
- `+effect:start_battle` — перехід з поля на окремий екран бою з учасниками; `+effect:return_to_town` — повернення в хаб зі збереженням знайденого.
- `+role:foe` — видимий на мапі сильний ворог, що ходить синхронно з гравцем (відрізняти від невидимих `enemy` випадкових боїв).
- `+ui:map-tool-palette` — перо/пензель/іконки/гумка; `+ui:encounter-gauge` — індикатор близькості випадкового бою; `+ui:map-icon-counter` — лишилось іконок на поверх.
- `+window:town-hub`, `+window:battle-screen`, `+window:quest-board`, `+window:guild-roster`.
- `+feature:hand-drawn-map`, `+feature:map-completion-reward`.
- `+axis:view=first-person`.
- `+card:hand-drawn-map`.

## Джерела
- ⭐ [Wikipedia: Etrian Odyssey (video game)](https://en.wikipedia.org/wiki/Etrian_Odyssey_(video_game)) — кроки, час від дії, мапа стилусом з обмеженим набором і лімітом іконок, FOE (коло → прямо до загону, другий/третій FOE приєднується), 5 у загоні, гільдія, очки навичок.
- [Wikipedia: серія](https://en.wikipedia.org/wiki/Etrian_Odyssey) — II–V, Nexus, HD, Untold.
- [Retronauts: EO V і мистецтво мапи](https://retronauts.com/article/611/etrian-odyssey-v-a-diy-tribute-to-the-art-of-game-mapping) — автоматичні клітини, перо/пензель/іконки, ліміт, нагорода за мапу (лише стіни), FOE через воду, важелі.
- [Wikipedia: Untold](https://en.wikipedia.org/wiki/Etrian_Odyssey_Untold:_The_Millennium_Girl) — Classic/Story, Picnic/Normal/Expert, автомапа, біг, 1 слот.
- [Steam: Etrian Odyssey HD](https://store.steampowered.com/app/1868180/Etrian_Odyssey_HD/) — 9 класів, кодекс, квести, дерево навичок, складність, слоти.

## Непевне
- (?) Індикатор випадкового бою (колір від синього до червоного) — з памʼяті; у якій саме грі серії зʼявився, не перевірено.
- (?) Ниточка Аріадни як предмет повернення в місто, три типи точок збирання (Take/Chop/Mine), перелік закладів міста — з памʼяті.
- (?) Штраф задніх рядів у ближньому бою, автомапа в Untold/HD (як саме працює) — не перевірено.
- (?) Односторонні «шорткати» (двері, що відчиняються з одного боку) — з памʼяті, тому не в правилах.
- (?) Чи перевірка мапи з нагородою є в першій грі, чи лише в пізніх — джерело описує EO V.
