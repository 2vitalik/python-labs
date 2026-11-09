---
title: "Wizardry: Proving Grounds of the Mad Overlord"
slug: wizardry
aka: [Wizardry I, Wizardry 1, "Wizardry: Proving Grounds", PGMO]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 1981
platforms: [Apple II, C64, IBM PC, Macintosh, MSX2, PC-9801, FM-7, Sharp X1, NES, Super Famicom, TurboGrafx-16, Game Boy Color, WonderSwan Color, Windows, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wizardry:_Proving_Grounds_of_the_Mad_Overlord", best: true, note: "загін 6, 5 рас, 3 світогляди, 4+4 класи, 10 поверхів 20×20, темні зони, телепорти, сейв лише поза лабіринтом"}
  - {kind: fandom, url: "https://wizardry.wiki.gg/wiki/Wizardry:_Proving_Grounds_of_the_Mad_Overlord", note: "Wizardry Wiki (wiki.gg): замок, порядок дій за спритністю, втрата загону, підсторінки"}
  - {kind: fandom, url: "https://wizardry.wiki.gg/wiki/Wizardry:_Proving_Grounds_of_the_Mad_Overlord/Walkthrough", note: "поверхи 20×20 з загортанням, координати 0E/0N, статуї-ключі, смоги, ліфти, односторонні двері"}
  - {kind: fandom, url: "https://wizardry.wiki.gg/wiki/Wizardry:_Proving_Grounds_of_the_Mad_Overlord/Spells", note: "усі заклинання мага й жерця за 7 рівнями"}
  - {kind: fandom, url: "https://wizardry.wiki.gg/wiki/Temple_of_Cant", note: "храм: воскресіння, попіл, параліч 300g"}
  - {kind: other, url: "https://www.mocagh.org/sir-tech/wiz1-manual.pdf", note: "скан мануалу (бачив у пошуку; файл >10 MB, не прочитав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wizardry+proving+grounds+of+the+mad+overlord+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, orientation-state, wrap-edges, impassable-cells, one-way-cell, key-and-door, teleport, teleport-random-exit, stairs-levels, fog-of-war, hp-damage, status-effects, inventory, inventory-items, item-pickup, item-identification, unit-xp-skills, round-currency, shop-catalog, shop-window, character-select, player-death, permadeath, save-game, melee-vs-ranged, keyboard-controls, +first-person-grid, +hand-drawn-map, +party-formation, +town-hub, +random-encounter, +dark-zone, +coordinate-teleport, +class-change, +alignment-party-rule, +spell-slots-by-level, +corpse-recovery, +resurrect-failure-chain, +chest-trap-identify]
proposes: ["+trigger:encounter", "+cond:alignment(a, x)", "+cond:coordinates_valid(cell)", "+effect:start_battle", "+effect:return_to_town", "+effect:resurrect(a)", "+effect:level_drain(a)", "+effect:identify", "+role:party-member", "+window:town-hub", "+window:battle-screen", "+window:character-create", "+window:character-sheet", "+ui:party-roster", "+ui:monster-picture", "+feature:scenario-export", "+feature:corpse-recovery", "+card:coordinate-teleport", "+card:class-change"]
author: opus
date: 2026-11-09
---

# Wizardry — загін із шести в клітинному лабіринті 10×(20×20): малюй мапу сам, бо телепорт у камінь — назавжди

## Суть
Гравець створює в замку загін до 6 героїв (раса, світогляд, клас) і веде його вниз 10 поверхами лабіринту під замком, щоб на нижньому вбити Вердну й забрати амулет. Лабіринт показано вузьким каркасним видом від першої особи, автомапи нема — гравець малює на міліметрівці. Небезпека — не лише бої з групами монстрів, а й **сам лабіринт**: темні зони, телепорти без попередження, загортання країв, камінь, у який можна телепортуватися й загинути. Смерть записується на диск одразу, тож уся гра — хардкорна з першого ходу.

## Поле і час
- 10 поверхів, кожен — сітка **20×20**; координати рахують на схід і північ від лівого нижнього кута (0E/0N).
- Поверх **загортається** (тор): з 19E крок на схід веде на 0E того ж рядка.
- Стіни — на ребрах між клітинами (лабіринт, а не кімнати); є двері, таємні двері, односторонні двері, ділянки суцільного каменю.
- Вид від першої особи — малий каркасний (≈10 % екрана) у текстовому інтерфейсі; у бою вид заміняє картинка монстра.
- Час покроковий: крок/поворот = хід; бій — раунди, у яких дії всіх розставлено наперед, а виконуються в порядку спритності.
- Видимість: лише клітини попереду; у темній зоні загін іде наосліп.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Загін | player | до 6 героїв, клітина, орієнтація | рухається як одна фігура; світогляди мають бути сумісні |
| Герой | ally | раса (Human, Elf, Dwarf, Gnome, Hobbit), світогляд (Good/Neutral/Evil), клас, HP, рівень, досвід, предмети | діє в бою за вказівкою гравця; кастери мають заклинання 7 рівнів |
| Базові класи | ally | Fighter · Priest · Mage · Thief | бій / лікування й захист / атакуюча магія / замки й пастки |
| Елітні класи | ally | Bishop (обидві магії) · Samurai (воїн + маг) · Lord (воїн + жрець) · Ninja (воїн + злодій) | доступні після прогресу (зміна класу), вищі вимоги до атрибутів |
| Група монстрів | enemy | 1–4 групи на бій, HP, ефекти | випадкові або фіксовані зустрічі; дружні зустрічі можуть зсунути світогляд |
| Тінь (Shade) | enemy | — | висмоктує рівень досвіду |
| Ніндзя / Capybara (пов. 3) | enemy | — | удар-обезголовлення (миттєва смерть) |
| Вердна | boss | амулет | на 10-му поверсі; перемога = забрати амулет і повернутись |
| Стіна / камінь | static | — | блокує; телепорт у камінь = загін зникає назавжди |
| Двері | gate | звичайні / таємні / односторонні / незнищенні | таємні — знайти; односторонні відчиняються з одного боку; незнищенні — лише з предметом-статуеткою |
| Темна зона | terrain | постійна темрява | загін іде наосліп; розвіює світло Lomilwa |
| Пастка-телепорт (клітина) | terrain | ціль | переносить загін; в оригіналі без повідомлення |
| «Area out of Bounds» | terrain | — | телепортує загін у замок |
| Сходи / ліфт | static | поверх-ціль | сходи на сусідній поверх; ліфт — на кілька поверхів |
| Смог (Bronze/Silver) | gate | потрібен ключ | пропускає лише з відповідним ключем |
| Статуя | container | ключ / статуетка / подія | обшукати — дістати предмет або викликати фіксований бій (Murphy's Ghost) |
| Скриня після бою | container | пастка, золото, предмети | пастку можна розпізнати (Calfo, не завжди вірно) і зняти злодієм |
| Предмети (зброя, броня, ключі, статуетки) | pickup | — | екіпірування, доступ до зон |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(forward)` → ЯКЩО `free(ahead)` → ТО `move(party, facing)`; інакше `block`.
- КОЛИ `input(left|right)` → ТО `face(party, ±90°)`.
- КОЛИ `edge(party)` → ТО `wrap(party)` (поверх — тор).
- КОЛИ `input(kick door)` → ЯКЩО `cell(ahead, door)` → ТО `move(party, facing)` крізь двері.
- КОЛИ `enter(party, dark_zone)` → ТО `custom: «вид темний, клітини попереду не показано»`, `clear_state(party, light)`.
- КОЛИ `enter(party, teleporter)` → ТО `teleport(party, fixed cell)` без повідомлення.
- КОЛИ `enter(party, out_of_bounds)` → ТО `custom: «перенести загін у замок»`.
- КОЛИ `enter(party, smog)` → ЯКЩО `has(party, matching key)` → ТО `move`; інакше `block`.
- КОЛИ `contact(party, indestructible door)` → ЯКЩО `has(party, statue)` → ТО пройти; інакше `block`.
- КОЛИ `input(search)` → ЯКЩО `cell(here, statue)` → ТО `give(party, key|statuette)` або `custom: «фіксований бій»`.
- КОЛИ `rng(p)` на крок → ТО `custom: «випадкова зустріч: 1–4 групи монстрів»`, `window(battle-screen)`.
- КОЛИ `turn_start(round)` → ТО `custom: «гравець задає дію кожному герою (атака, заклинання, предмет, втеча…)»`; виконання — `custom: «у порядку спритності»`.
- КОЛИ `custom: «ціль дії вже знищена цього раунду»` → ТО `custom: «дію втрачено»` (у деяких портах — автоціль).
- КОЛИ `input(cast Katino|Manifo)` → ТО `set_state(group, asleep|paralyzed)`; ЯКЩО `state(target, asleep|paralyzed)` → ТО `damage(×2)`.
- КОЛИ `input(cast Dumapic)` → ТО `message(coordinates + depth)`.
- КОЛИ `input(cast Malor)` поза боєм → ЯКЩО `custom: «цільова клітина не камінь»` → ТО `teleport(party, coords)`; інакше `custom: «загін втрачено назавжди»`, `lose`.
- КОЛИ `input(cast Malor)` у бою → ТО `teleport(party, random cell on level)`.
- КОЛИ `input(cast Loktofeit)` → ТО `custom: «повернення в замок»`, `take(party, all items)`, `currency(−most)`.
- КОЛИ `input(cast Haman|Mahaman)` → ТО `choose(divine effects)`, `custom: «кастер втрачає рівень»`.
- КОЛИ `input(cast Di)` → ЯКЩО `prob(success)` → ТО `custom: «герой оживає з 1 HP»`; інакше `transform(dead, ashes)`.
- КОЛИ `input(cast Kadorto)` → ЯКЩО `prob(success)` → ТО `heal(a, full)` з воскресінням; інакше `custom: «герой втрачений назавжди»`.
- КОЛИ `contact(shade, hero)` → ТО `custom: «мінус рівень досвіду»`.
- КОЛИ `contact(decapitator, hero)` → ЯКЩО `prob(crit)` → ТО `custom: «миттєва смерть»`.
- КОЛИ `wave_cleared` → ТО `custom: «досвід і золото»`; ЯКЩО `custom: «лишилась скриня»` → ТО `choose(inspect | Calfo | disarm | open)`.
- КОЛИ `input(Calfo)` → ТО `custom: «назва пастки скрині, інколи хибна»`.
- КОЛИ `hp_zero(hero)` → ТО `set_state(hero, dead)`, `custom: «одразу записати на диск»`.
- КОЛИ `custom: «загинув весь загін»` → ТО `custom: «загін лежить у лабіринті; врятувати може лише новий загін, що знайде тіла»`.
- КОЛИ `custom: «дружня зустріч»` → ЯКЩО `prob(small)` → ТО `custom: «світогляд героя змінюється Good↔Evil»`.
- КОЛИ `custom: «загін повернувся в замок»` → ТО `custom: «можна міняти склад загону, якщо світогляди сумісні»`.
- КОЛИ `custom: «Вердну переможено й амулет у загону»` і `reach(party, castle)` → ТО `win`.
- Перемога: амулет Вердни в замку. Поразка: окремий герой — мертвий/попіл/втрачений; загін — лежить у лабіринті до рятувальників. Рахунку нема.

## Керування і ввід
- Клавіатура: вперед, поворот ліворуч/праворуч, вибити двері, обшукати, табір, інвентар, заклинання.
- Бій — меню на кожного героя: вибір дії та цілі (групи), потім виконання раунду.
- Заклинання вводять **назвою** (Halito, Malor…); Malor — далі задати поверх і кроки на північ/південь/схід/захід.
- У замку — текстові меню закладів (букви пунктів).

## Вікна, меню, HUD
- `town-hub` (замок): Gilgamesh's Tavern (склад загону), Adventurer's Inn (відпочинок), Boltac's Trading Post (`shop-window`: купити/продати), Temple of Cant (воскресіння, параліч 300g), Training Grounds (`character-create`), Edge of Town (вхід у лабіринт, вихід/збереження).
- `game-screen` у лабіринті: маленький каркасний вид, `party-roster` (імʼя, клас, AC, HP, стан), рядок повідомлень.
- `battle-screen`: `monster-picture` замість виду, список груп монстрів (кількість), меню дій героїв.
- `character-sheet` (inventory-window): атрибути, заклинання за рівнями, предмети, спорядження.
- `character-create`: раса, світогляд, клас (елітний — якщо атрибути дозволяють).
- `save-slots`: «scenario disk» — новий або наявний диск.
- Переходи: `town-hub` → Edge of Town → лабіринт → (зустріч) `battle-screen` → скриня → лабіринт; сходи на 1-му поверсі → замок.

## Фічі поза полем
- Сейв лише поза лабіринтом (scenario disk); смерть пишеться на диск одразу — `permadeath` без перезавантаження.
- Рятувальна експедиція: новий загін несе тіла загиблих у храм.
- Експорт переможного загону в Wizardry II і III (`scenario-export`).
- Мапу малює гравець (у коробці — міліметрівка).
- Порти й ремейк (2024) додають автомапу і зручності (?).

## Варіації й родичі
- Нащадки: Wizardry II–VIII, Might and Magic, [dungeon-master](dungeon-master.md) (той самий клітинний вид, але real-time), [etrian-odyssey](etrian-odyssey.md) (ручна мапа як механіка), [legend-of-grimrock](legend-of-grimrock.md), [dungeon-encounters](dungeon-encounters.md) (каркасна клітинна мапа з координатами), [labyrinth-of-refrain](labyrinth-of-refrain.md) (японська гілка дрпг).
- Сусіди по поколінню: [rogue](rogue.md) (1980) — один герой, процедурні поверхи; Wizardry — фіксований лабіринт і загін.
- Осі варіацій: **мапа** (лише папір / автомапа / ручна в грі) · **поверх** (тор / з межами) · **телепорт** (за координатами з ризиком / лише пари) · **смерть** (одразу на диск / перезавантаження) · **загін** (6 у дві лінії (?) / 4 у 2×2 / один).

## Цікавинки для курсу
- Поверх-тор 20×20 зі стінами на ребрах: модель «клітина + 4 стіни», загортання координат — 🌱.
- Телепорт за координатами з загибеллю в камені: перевірка клітини-цілі, «MALOR-калькулятор» для гравця — 🌱.
- Каркасний вид від першої особи з 2D-мапи ребер — 🥉.
- Ланцюг станів героя: живий → мертвий → (невдала спроба) попіл → (невдала) втрачений — скінченний автомат з імовірностями переходів — 📎.
- Бій раундами: усі дії наперед, виконання за спритністю, «втрачена дія» на вже вбиту ціль — 📎.
- Світогляд як обмеження складу загону й дрейф світогляду від дружніх зустрічей — 🌱.
- Ключі-статуетки й смоги: доступ до зон лабіринту через предмети — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `orientation-state` (крок/поворот) · `wrap-edges` (тор-поверх) · `impassable-cells` · `one-way-cell` (односторонні двері) · `key-and-door` (смоги, незнищенні двері) · `teleport` / `teleport-random-exit` (Malor у бою) · `stairs-levels` (сходи й ліфти) · `fog-of-war` (темрява, вид попереду) · `hp-damage` · `status-effects` (сон, параліч, отрута) · `inventory` / `inventory-items` / `item-pickup` · `item-identification` (Calfo для скринь, Latumapic для монстрів) · `unit-xp-skills` · `round-currency` (золото) · `shop-catalog` / `shop-window` (Boltac) · `character-select` (таверна) · `player-death` · `permadeath` · `save-game` · `melee-vs-ranged` (?) · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+first-person-grid` (як у Dungeon Master) · `+hand-drawn-map` (як у Etrian Odyssey) · `+party-formation` (як у DM) · `+town-hub` (як у EO) · `+random-encounter` (як у EO).
  - `+dark-zone` «Клітини постійної темряви: рух наосліп, гасять світло» · interface/render · 🌱.
  - `+coordinate-teleport` «Телепорт за введеними координатами; камінь = загибель» · entities/interact · 🌱.
  - `+class-change` «Зміна класу після прогресу; елітні класи-гібриди» · entities/state · 📎.
  - `+alignment-party-rule` «Світогляд обмежує склад загону» · game-logic/constraints · 🌱.
  - `+spell-slots-by-level` «Заклинання 7 рівнів, кількість на рівень» (?) · entities/combat · 📎.
  - `+corpse-recovery` «Загиблий загін лежить у світі до рятувальників» · game-logic/lose · 📎.
  - `+resurrect-failure-chain` «Мертвий → попіл → втрачений за невдач» · entities/state · 📎.
  - `+chest-trap-identify` «Пастка скрині: розпізнати (неточно) і зняти» · entities/interact · 🌱.

## Пропозиції до словників
- `+trigger:encounter` — почалась зустріч (випадкова або фіксована) з групою монстрів.
- `+cond:alignment(a, x)` — світогляд героя; `+cond:coordinates_valid(cell)` — ціль телепорту не камінь.
- `+effect:start_battle` (як у EO) · `+effect:return_to_town` (як у EO; Loktofeit) · `+effect:resurrect(a)` — оживити з імовірністю провалу · `+effect:level_drain(a)` — мінус рівень досвіду · `+effect:identify` (як у Rogue; Calfo/Latumapic).
- `+role:party-member` (як у DM).
- `+window:town-hub` · `+window:battle-screen` (як у EO) · `+window:character-create` · `+window:character-sheet` (як у DM).
- `+ui:party-roster` — таблиця загону (клас, AC, HP, стан) · `+ui:monster-picture` — картинка ворога замість виду.
- `+feature:scenario-export` — перенести загін у наступну гру серії · `+feature:corpse-recovery` — рятувальна експедиція.
- `+card:coordinate-teleport` · `+card:class-change`.

## Джерела
- ⭐ [Wikipedia: Wizardry: Proving Grounds of the Mad Overlord](https://en.wikipedia.org/wiki/Wizardry:_Proving_Grounds_of_the_Mad_Overlord) — загін 6, 5 рас, 3 світогляди (Good і Evil не разом), 4 базові + 4 елітні класи, 7 рівнів магії, 10 поверхів 20×20, темні зони, телепорти без повідомлення, Teleport за координатами (камінь = кінець), 1–4 групи монстрів, сейв лише поза лабіринтом, експорт загону в II/III.
- [Wizardry Wiki: гра](https://wizardry.wiki.gg/wiki/Wizardry:_Proving_Grounds_of_the_Mad_Overlord) — заклади замку, порядок дій за спритністю, «втрачені» дії, дрейф світогляду, загиблий загін і рятувальники.
- [Wizardry Wiki: проходження](https://wizardry.wiki.gg/wiki/Wizardry:_Proving_Grounds_of_the_Mad_Overlord/Walkthrough) — загортання поверху, координати від 0E/0N, статуї з ключами, смоги, незнищенні двері, ліфти, «Area out of Bounds», односторонні двері, Shades і обезголовлення.
- [Wizardry Wiki: заклинання](https://wizardry.wiki.gg/wiki/Wizardry:_Proving_Grounds_of_the_Mad_Overlord/Spells) — 21 закл. мага і 29 жерця за 7 рівнями; Di → попіл, Kadorto → втрачений, Malor, Loktofeit, Haman/Mahaman за рівень.
- [Wizardry Wiki: Temple of Cant](https://wizardry.wiki.gg/wiki/Temple_of_Cant) — воскресіння без гарантії, попіл, параліч 300g.

## Непевне
- (?) Лише перші 3 герої бʼються впритул і отримують удари, задні 3 — магія/дальні — з памʼяті; у відкритих джерелах не знайшов.
- (?) Кількість заклинань за рівень (слоти за рівнем мага/жерця, а не очки мани) — з памʼяті.
- (?) Обертачі (spinners), ями, жолоби вниз (chutes) і антимагічні зони — класика серії з памʼяті; відкриті сторінки згадують лише темні зони, телепорти, ліфти, односторонні двері.
- (?) Типи пасток скринь (отруйна голка, газ, телепорт, тривога…) і камери таверни/готелю за ціною — з памʼяті.
- (?) Бонусні очки при створенні героя й вимоги атрибутів елітних класів — у джерелах без чисел.
- (?) «Дзеркальні телепорти» з рядка черги не підтвердив — джерела кажуть просто «телепорти без попередження».
- (?) Ремейк 2024 (автомапа, 3D) — бачив згадку лише в назві підсторінки досягнень ремейку.
- (?) Мануал (mocagh.org) — PDF >10 MB, WebFetch не прочитав.
