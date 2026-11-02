---
title: Legend of Grimrock
slug: legend-of-grimrock
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 2012
platforms: [PC (Windows, macOS, Linux), iOS, Nintendo Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Legend_of_Grimrock", best: true, note: "суть, загін 1–4, клітинний real-time, Old School mode без мапи, редактор, натхнення Dungeon Master / Eye of the Beholder"}
  - {kind: steam, url: "https://store.steampowered.com/app/207170/Legend_of_Grimrock/", note: "сторінка гри"}
  - {kind: official, url: "https://www.grimrock.net/", note: "офіційний сайт Almost Human, модинг-документація (WebFetch: 403)"}
  - {kind: other, url: "https://www.crimsontear.com/gaming/legend-of-grimrock/spells", note: "9 рун, заклинання й вимоги навичок"}
  - {kind: other, url: "https://www.crimsontear.com/gaming/legend-of-grimrock/skills", note: "класи й навички, Reach Attack з заднього ряду"}
  - {kind: fandom, url: "https://grimrock.fandom.com/wiki/Legend_of_Grimrock", note: "фан-вікі (WebFetch: 402)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=legend+of+grimrock+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, orientation-state, impassable-cells, key-and-door, teleport-pair, teleport-one-way, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, projectile-shot, melee-vs-ranged, chase-bfs, enemy-patrol, shoot-cooldown, temporary-modes, player-death, sequential-levels, save-multi-slot, minimap-radar, in-game-editor, gui-render, +first-person-grid, +party-formation, +action-cooldown, +pressure-plate, +lever-toggle, +hidden-button, +pit-trapdoor, +item-alcove, +throw-to-cell, +spinner-tile, +rune-casting, +facing-attack-rows, +hunger-clock, +light-source, +auto-map-notes, +old-school-mode, +step-dance]
proposes: ["+trigger:item_placed", "+trigger:weight_on", "+trigger:weight_off", "+trigger:cooldown_ready", "+cond:row", "+cond:facing", "+cond:rune_sequence", "+effect:turn", "+effect:throw", "+effect:fall_level", "+effect:open", "+effect:close", "+role:alcove", "+role:party-member", "+window:character-sheet", "+window:map-window", "+window:character-create", "+ui:party-portraits", "+ui:hand-slots", "+ui:rune-grid", "+ui:food-bar", "+ui:compass", "+feature:old-school-mode", "+feature:map-notes", "+feature:level-editor", "+axis:actors=party", "+axis:view=first-person"]
author: opus
date: 2026-11-02
---

# Legend of Grimrock — Dungeon Master 2012 року: загін 2×2 кроками по клітинах, у реальному часі, серед плит, ям і телепортів

## Суть
Чотири вʼязні рухаються підземеллям гори Гримрок **одним загоном-клітиною** від першої особи: крок вперед/вбік/назад і поворот на 90°. Бій у реальному часі, але на сітці: монстри займають клітини й мають напрямок погляду, кожна рука кожного героя після удару стоїть на кулдауні, а вбік можна відступати «танцем» навколо квадрата 2×2. Половина гри — пазли механізмів: натискні плити, приховані кнопки, важелі, ями-люки, телепорти, ніші під предмети, кинуті предмети, що лягають на клітину. Гра відроджує dungeon crawler Dungeon Master / Eye of the Beholder з сучасною графікою.

## Поле і час
- Рівень — квадратна сітка (редактор: 32×32) з кількох поверхів; між поверхами — сходи та ями. Вид від першої особи з видимістю кількох клітин уперед; освітлення від смолоскипів (вигорають) або заклинання Light.
- Загін займає **одну клітину** й має напрямок (N/E/S/W). Усередині — формація 2×2: передній ряд (лівий, правий) і задній ряд.
- Real-time: крок займає короткий фіксований час (плавна анімація між клітинами), монстри рухаються своїм темпом; кожна дія героя — з кулдауном. Пауза — через меню (у реальному часі гра не зупиняється сама) (?).
- Монстр займає клітину (деякі — групою до 4 в одній клітині) і має напрямок; атакує лише клітину перед собою.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Загін | player | напрямок, клітина | рух/поворот як одна сутність |
| Герой ×4 | player (party-member) | раса (Human, Minotaur, Lizardman, Insectoid), клас (Fighter, Mage, Rogue), Health, Energy, Str/Dex/Vit/Will, їжа, навички, риси, позиція 2×2 | дві руки; кожна дія — кулдаун |
| Монстр | enemy | HP, атака, швидкість, напрямок, групи в клітині | патруль/погоня; атакує клітину перед собою; дальні — стріляють |
| Монстр-група (скелети, слимаки) | enemy | до 4 в клітині | клітина = група |
| Стіна | static | — | непрохідна |
| Натискна плита (pressure plate) | switch | хто натискає: загін / монстр / предмет | активується вагою, деактивується, коли вага зникла |
| Прихована кнопка | switch | маленька, у стіні | клік → подія (двері, міст, секрет) |
| Важіль | switch | стан вгору/вниз | перемикає ціль |
| Двері / ґрати | gate | відкриті/закриті | відкриваються механізмом, ключем або вручну |
| Замок (keyhole) | gate | тип ключа | ключ того ж типу → двері |
| Ключ (iron, gold, ornate…) | pickup | тип | витрачається в замку |
| Ніша (alcove) | switch | очікуваний предмет | покласти предмет → подія (часто конкретний) |
| Яма / люк (pit) | hazard | відкрита/закрита | падіння на поверх нижче зі шкодою; предмет теж падає |
| Телепорт | terrain | ціль, хто переноситься | переносить загін / монстрів / предмети |
| Обертач (spinner) | terrain | — | розвертає загін (?) |
| Кристал лікування | static | перезарядка | клік → лікує й воскрешає героїв (?) |
| Смолоскип / тримач смолоскипа | pickup / switch | паливо | світло; тримач іноді — механізм |
| Предмет на підлозі | pickup | вага | береться курсором; можна кинути — летить і лягає на клітину |
| Зброя / броня / метальна зброя / стріли | pickup | шкода, кулдаун, вага | у руку; стріли лишаються на клітині після пострілу |
| Їжа | pickup | ситість | годує героя |
| Сувій / записка | pickup | текст | підказки, рунні формули |
| Зілля, флакони, трави | pickup | — | алхімія і зілля (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(step dir)` → ЯКЩО `free(cell)` → ТО `move(party, dir)` (крок вбік/назад без повороту); стіна/монстр → `block`.
- КОЛИ `input(turn left|right)` → ТО `face(party, ±90°)`.
- КОЛИ `input(click hand of hero)` → ЯКЩО `custom: «рука не на кулдауні»` → ТО дія предмета в руці (удар, постріл, каст), `timer(cooldown[item])`.
- КОЛИ `input(melee)` → ЯКЩО `row(hero) == front` or `custom: «Reach Attack (Assassination)»` → ТО `damage(monster in front cell)`; задній ряд — лише метальна/стрілецька зброя й заклинання.
- КОЛИ `contact(monster attack, party)` → ЯКЩО `facing(monster → party front)` → ТО `damage(front row)`; атака збоку/ззаду → бʼє відповідний бік/задній ряд.
- КОЛИ `input(rune grid sequence, cast)` → ЯКЩО `custom: «руни утворюють формулу»` and `skill(school) >= req` and `energy >= cost` → ТО заклинання (Fireburst, Fireball, Frostbolt, Shock, Poison Cloud, Light, Darkness, Invisibility, щити); інакше `custom: «fizzle»`.
- КОЛИ `enter(party|monster|item, pressure_plate)` → ТО `trigger(linked: open/close door, spawn, teleport)`; КОЛИ вага зникла → протилежна дія (якщо плита не одноразова).
- КОЛИ `input(click hidden button|lever)` → ТО `trigger(linked)`; важіль — `toggle`.
- КОЛИ `input(place item in alcove)` → ЯКЩО `custom: «предмет потрібного типу»` → ТО `trigger(linked)`.
- КОЛИ `input(key on keyhole)` → ЯКЩО `same(key, lock, type)` → ТО `open(door)`, `take(key)`.
- КОЛИ `enter(a, open_pit)` → ТО `fall_level(a)`, `damage(n)` (для загону); предмети падають на поверх нижче.
- КОЛИ `enter(a, teleport)` → ТО `teleport(a, target)` — працює і для монстрів, і для кинутих предметів.
- КОЛИ `input(throw item)` → ТО `custom: «предмет летить по прямій, доки не вдариться; шкода монстру; лягає на клітину»` — так можна натиснути плиту здалеку.
- КОЛИ `timer` → ТО `counter(food[hero], -1)`; голод → `custom: «нема регенерації / штрафи»` (?).
- КОЛИ `timer` → ТО `counter(torch_fuel, -1)`; 0 → темрява.
- КОЛИ `hp_zero(hero)` → ТО `set_state(hero, dead)`; кристал лікування воскрешає; КОЛИ всі мертві → `lose`.
- КОЛИ `custom: «досвід за вбивство»` → `counter(xp, +n)`; рівень → `custom: «+очки навичок»`, нові заклинання доступні за навичкою школи.
- КОЛИ `enter(party, secret)` → ТО `message(«Secret found!»)`, `counter(secrets, +1)`.
- Перемога: дійти до дна й знищити Невмирущого (Undying One). Поразка: загинув увесь загін. Рахунок: нема; статистика (секрети, час) (?).

## Керування і ввід
- Клавіші: `W/A/S/D` — крок вперед/вліво/назад/вправо (стрейф), `Q/E` — поворот; миша — дії.
- Права кнопка на руці героя — атака предметом у руці; у мага — відкриває сітку рун 3×3: клік по рунах у порядку → «Cast».
- Ліва кнопка — взяти/покласти предмет курсором (з підлоги, з ніші, в руку, в рюкзак); кинути — відпустити предмет у верхній частині вʼю (летить уперед) (?).
- Перетягування портретів — зміна формації 2×2.
- Відпочинок (клавіша/кнопка) — швидкий плин часу, відновлення, перерване появою монстра.
- Мапа: клавіша `Tab`/`M` (?), нотатки на мапі.

## Вікна, меню, HUD
- `main-menu`: New Game · Load · Custom Dungeon (моди) · Options · Credits · Quit.
- `+window:character-create` — портрет, раса, клас, риси, атрибути для кожного з 4 героїв (або готовий загін).
- `game-screen`: вид від першої особи + `+ui:party-portraits` 2×2 у кутку з HP/Energy-барами, `+ui:hand-slots` (дві руки, затемнені на кулдауні), повідомлення-текст, `+ui:rune-grid` у мага.
- `inventory-window` / `+window:character-sheet` — лялька спорядження, рюкзак-сітка, атрибути, навички (розподіл очок), риси, `+ui:food-bar`.
- `+window:map-window` — автомапа поверху з клітинами, сходами, ямами (вимкнена в Old School); нотатки на мапі (`+feature:map-notes`) (?).
- `pause-menu` → Save/Load (`save-multi-slot`), Options, Quit.
- `settings-window` — графіка, звук, керування, складність не змінюється в грі (?).
- `end-screen` — загін загинув → Load; фінал → титри (`credits-window`).
- Переходи: main-menu → character-create → game-screen; game-screen ↔ inventory/map (без паузи світу?) (?); смерть → end-screen → load.

## Фічі поза полем
- Складність: Easy / Normal + опція **Old School** (без автомапи — гравець малює на папері; у PDF-мануалі сітка для друку).
- Збереження будь-де, кілька слотів.
- `level-editor` (з патча 1.3.1): клітинний редактор, обʼєкти-механізми з звʼязками (connectors), Lua-скрипти; Steam Workshop / Custom Dungeon — сотні модів.
- Немає permadeath: смерть = завантажити сейв.

## Варіації й родичі
- Предки: Dungeon Master (1987; real-time, руни, загін 2×2, кулдауни — прямий прототип), Eye of the Beholder (1991; D&D-правила, 4 герої у формації, ніші під предмети), Lands of Lore, Ultima Underworld (вільний рух, не клітини).
- Нащадки: Legend of Grimrock II (2014, відкритий острів), Vaults of Vulnerability, Dungeons of Dreadrock (одна клітина-герой, пазли), Druidstone (той самий студіо, тактика), Etrian Odyssey (покрокове + мапа, яку малює гравець).
- Осі варіацій: **час** (покроковий EOB-клон / real-time з кулдаунами) · **загін** (1 / 4 у 2×2 / 6 у 3×2) · **мапа** (автомапа / Old School / мапу малює гравець у грі — Etrian) · **магія** (меню / руни-формули) · **поворот** (лише 90° / вільний).

## Цікавинки для курсу
- Перша особа на сітці: рендер «коридору» з клітин попереду за напрямком — 🥉 (класичний трюк raycast-free).
- Натискна плита + вага (загін, монстр, кинутий предмет) + звʼязки «механізм → ціль» — 🥉.
- Кинутий предмет летить по клітинах і лягає — і натискає плиту здалеку — 📎.
- Формація 2×2 і правило «хто може бити з якого ряду», атака з флангу по ряду — 🥉.
- Кулдаун кожної руки окремо як real-time ресурс — 📎.
- Руни 3×3 як формула заклинання (послідовність → словник) — 📎.
- Автомапа з нотатками vs Old School mode — 🌱 / 🥉 (мапа з відкриттям клітин).
- «Танець» монстра навколо квадрата 2×2 — 🌱 як урок про експлойти ШІ з фіксованим кроком.

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `orientation-state` (напрямок загону) · `impassable-cells` · `key-and-door` · `teleport` + `teleport-pair` + `teleport-one-way` · `hp-damage` · `inventory` + `inventory-items` + `inventory-limit` (вага) · `item-pickup` · `projectile-shot` (кинуті предмети, стріли, заклинання) · `melee-vs-ranged` · `chase-bfs` · `enemy-patrol` · `shoot-cooldown` · `temporary-modes` (щити, невидимість) · `player-death` · `sequential-levels` (поверхи) · `save-multi-slot` · `minimap-radar` (автомапа) · `in-game-editor` · `gui-render` · `keyboard-controls` · `cell-click` · `game-screen` · `main-menu` · `settings-window` · `pause-menu`.
- **Нема** → пропозиції карток:
  - `+first-person-grid` «Вид від першої особи на клітинному полі» · interface/render · 🥈.
  - `+party-formation` «Загін 2×2: передній і задній ряд» · entities/state · 🥉.
  - `+action-cooldown` «Кулдаун кожної дії/руки» · entities/state · 📎.
  - `+pressure-plate` «Натискна плита з вагою» · entities/interact · 📎 · слоти {who, once}.
  - `+lever-toggle` «Важіль перемикає ціль» · entities/interact · 🌱.
  - `+hidden-button` «Прихована кнопка в стіні» · entities/interact · 🌱.
  - `+pit-trapdoor` «Яма-люк на поверх нижче» · entities/interact · 📎.
  - `+item-alcove` «Ніша, що чекає предмет» · entities/interact · 📎.
  - `+throw-to-cell` «Кинутий предмет летить і лягає на клітину» · entities/combat · 📎.
  - `+spinner-tile` «Клітина-обертач» · entities/interact · 🌱.
  - `+rune-casting` «Заклинання послідовністю рун» · interface/input · 📎.
  - `+facing-attack-rows` «Атака з напрямку бʼє відповідний ряд» · entities/combat · 🥉.
  - `+light-source` «Смолоскип вигорає, темрява» · entities/state · 🌱.
  - `+auto-map-notes` «Автомапа з нотатками гравця» · interface/render · 🥉.
  - `+old-school-mode` «Режим без автомапи» · game-logic/difficulty · 🌱.
  - `+step-dance` «Обхід ворога по квадрату (ШІ-експлойт як механіка)» · entities/move · 🌱.
  - `+hunger-clock` (з Rogue).

## Пропозиції до словників
- `+trigger:item_placed` — предмет покладено в нішу/на клітину; `+trigger:weight_on` / `+trigger:weight_off` — на плиті зʼявилась/зникла вага; `+trigger:cooldown_ready`.
- `+cond:row` — позиція героя у формації; `+cond:facing` (є ⏳, тут — напрямок монстра відносно загону); `+cond:rune_sequence` — введена послідовність рун.
- `+effect:turn` — поворот на 90° без руху (≈ `face`, але для гравця-вʼю); `+effect:throw`; `+effect:fall_level` — перехід на поверх нижче з шкодою; `+effect:open` / `+effect:close` — механізм.
- `+role:alcove` — ніша-слот під предмет; `+role:party-member` — член загону всередині одного аватара.
- `+window:character-create`, `+window:character-sheet`, `+window:map-window` (є ⏳).
- `+ui:party-portraits`, `+ui:hand-slots`, `+ui:rune-grid`, `+ui:food-bar`, `+ui:compass`.
- `+feature:old-school-mode`, `+feature:map-notes`, `+feature:level-editor` (є ⏳).
- `+axis:actors=party` — 4 героя в одній клітині; `+axis:view=first-person` — нова вісь «камера»: згори / ізо / перша особа на сітці.

## Джерела
- ⭐ [Wikipedia: Legend of Grimrock](https://en.wikipedia.org/wiki/Legend_of_Grimrock) — суть, загін 1–4, клітинний real-time, Old School mode, редактор 1.3.1, натхнення DM/EOB.
- [Steam: Legend of Grimrock](https://store.steampowered.com/app/207170/Legend_of_Grimrock/) — сторінка гри.
- [Crimson Tear: заклинання](https://www.crimsontear.com/gaming/legend-of-grimrock/spells) — 9 рун, заклинання за школами, вимоги навичок.
- [Crimson Tear: навички](https://www.crimsontear.com/gaming/legend-of-grimrock/skills) — класи Fighter/Mage/Rogue, навички, Reach Attack з заднього ряду.
- [grimrock.net](https://www.grimrock.net/) — офіційний сайт і модинг (не відкрився).
- YouTube: пошук «legend of grimrock gameplay».

## Непевне
- (?) Правило «атака збоку/ззаду бʼє бічний/задній ряд», групи монстрів до 4 у клітині, обертачі — з памʼяті.
- (?) Кристали лікування воскрешають героїв; ефекти голоду — з памʼяті.
- (?) Нотатки на мапі в LoG1 (а не лише в LoG2), клавіша мапи, пауза під час меню — не перевірено.
- (?) Раси/класи/риси героїв — з памʼяті (джерело згадує лише класи й навички).
- (?) Розмір рівня 32×32 — з памʼяті про редактор; формат рівня — Lua-скрипт (?).
- (?) Кидок предмета «у верхній частині вʼю» — з памʼяті.
