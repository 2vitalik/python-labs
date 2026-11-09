---
title: Mycelium Heaven
slug: mycelium-heaven
aka: []
family: thinky
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2025
platforms: [PC, Switch, PS, Android (альфа-демо)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2656520/Mycelium_Heaven/", best: true, note: "реліз 27.02.2025; дії «spread, bloom, consume» за енергію; 4 сезонні світи; демо"}
  - {kind: itch, url: "https://3dgoblindev.itch.io/mycelium-heaven", note: "сформульовані правила й керування (3 слоти енергії, родючі клітини біля гриба, X — рестарт, ПКМ — undo), джем-версія і демо на 60 рівнів"}
  - {kind: other, url: "https://3dgoblindev.itch.io/mycelium-heaven/devlog/612834/getting-things-ready-for-indie-games-mlaga", note: "devlog: зимові механіки — камінь і могили"}
  - {kind: other, url: "https://steamcommunity.com/app/2656520/reviews/?browsefilter=toprated", note: "відгуки з розбором: 3 енергії, ціни дій, кінцівка дає 2, зомбі — все; равлики, гриб-суперник, пеньки"}
  - {kind: other, url: "https://steamcommunity.com/app/2656520/discussions/0/595142571487928089/", note: "розробник: 120 рівнів, по 30 на сезон"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mycelium+Heaven+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, move-limit, destroy-all-enemies, collect-all, enemy-patrol, impassable-cells, undo-redo, undo-unlimited, restart-level, sequential-levels, level-select, level-unlock, world-map, save-progress, settings-window, main-menu, game-screen, remaining-counter, background-music, sound-effects, movement-animation, +spread-network, +energy-budget, +eat-to-refuel, +fertile-adjacency, +grave-timer, +reach-extender, +rival-spreader, +mushroom-eater, +wordless-tutorial]
proposes: ["+effect:spread", "+ui:energy-pips", "+cond:fertile", "+feature:death-hints", "+card:energy-budget", "+card:spread-network"]
author: opus
date: 2026-11-09
---

# Mycelium Heaven — гриб розростається клітинами поля за енергію і поповнює її, поїдаючи зомбі; зʼїж усіх, не виснажившись

## Суть
Покрокова головоломка іспанського соло-розробника 3DGoblinDev (Unreal Engine, з геймджему MálagaJam Weekend 16). Гравець — фіолетовий гриб-некрофаг: клацаючи по клітинах, він **поширює міцелій** на родючі клітини поруч із грибом, **вирощує гриби** на міцелії і **споживає** трупи й зомбі під міцелієм. Кожна дія коштує 1 енергії з трьох; зʼїдене поповнює енергію (зомбі — повністю, кінцівка — частково). Мета — зʼїсти всіх зомбі рівня, не лишившись без енергії. Правила гра не пояснює: їх відкривають на перших рівнях.

## Поле і час
- Квадратна сітка, вигляд 3D low-poly згори під кутом; розмір залежить від рівня, деякі рівні складаються з кількох окремих сіток.
- Шари: тип клітини (земля, камінь, пеньок, могила) + стан гриба (порожньо / міцелій / гриб) + обʼєкт (зомбі, кінцівка, равлик).
- Хід = одна дія (клік); після дії ходять зомбі-ходоки, рахуються таймери могил, рухаються равлики й гриб-суперник (?).
- Чотири світи-сезони по 30 рівнів: осінь 1–30, зима 31–60, весна 61–90, літо 91–120.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гриб (клітина з грибом) | player | — | робить сусідні клітини родючими |
| Міцелій | player | — | на ньому можна виростити гриб; споживає труп на своїй клітині |
| Енергія | resource | 3 слоти | −1 за дію; поповнюється їжею; понад 3 не накопичується |
| Зомбі, що стоїть | enemy | дає повну енергію | ціль; споживається з міцелію |
| Зомбі-ходок | enemy | лінія руху | ходить туди-сюди по одній лінії — позиція передбачувана на кілька ходів |
| Кінцівка (рука тощо) | pickup | дає 2 енергії | їжа без статусу цілі (?) |
| Могила | spawner | число на надгробку | зомбі входить і виходить за таймером — зʼїсти треба в момент, коли він зовні (зима) |
| Камінь | terrain | — | на ньому не можна виростити гриб (зима) |
| Пеньок / стовбур | terrain | — | спожитий і з грибом — дає досяжність далі, ніж звичайна клітина (осінь) |
| Равлик | enemy | — | їсть гриби, йде до найближчого (весна) |
| Гриб-суперник | enemy | ті самі правила | теж поширюється і їсть зомбі; не можна дати йому зʼїсти жодної їжі (весна) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ЯКЩО `adjacent_count(cell, mushroom, >=, 1)` і `free(cell)` і `counter(energy, >=, 1)` → ТО `set_cell(cell, mycelium)`, `counter(energy, -1)` — поширення (`+effect:spread`).
- КОЛИ `input(click, mycelium)` → ЯКЩО `not cell(mycelium, stone)` і `counter(energy, >=, 1)` → ТО `transform(mycelium, mushroom)`, `counter(energy, -1)` — цвітіння; сусіди нового гриба стають родючими.
- КОЛИ `input(click, mycelium)` → ЯКЩО `occupied(mycelium, zombie|limb)` і `counter(energy, >=, 1)` → ТО `disappear(zombie|limb)`, `counter(energy, -1)`, далі `counter(energy, +k)`: зомбі — до максимуму, кінцівка — +2.
- КОЛИ `counter(energy, ==, max)` → ЯКЩО `custom: «зʼїдено ще щось»` → ТО `custom: «надлишок згорає»` — головна пастка: не «перегодовуватись».
- КОЛИ `turn_end(player)` → ТО `move(walker, line_dir)`; КОЛИ `blocked(walker)` → ТО `face(walker, reverse)` (?).
- КОЛИ `timer(grave_n)` → ТО `custom: «зомбі виходить з могили або ховається»`; спожити можна лише зовні.
- КОЛИ `input(click, stump)` → ЯКЩО `custom: «пеньок спожито і на ньому гриб»` → ТО `custom: «родючою стає ширша зона, ніж 4 сусіди»` (?).
- КОЛИ `turn_end(player)` → ТО `move(snail, toward_nearest_mushroom)`; КОЛИ `contact(snail, mushroom)` → ТО `disappear(mushroom)` (?).
- КОЛИ `turn_end(player)` → ТО `custom: «гриб-суперник робить свою дію за тими ж правилами»`; КОЛИ `custom: «суперник зʼїв їжу»` → ТО `lose` (?).
- КОЛИ `all_gone(zombie)` → ТО `win`, `next_level`.
- КОЛИ `counter(energy, ==, 0)` → ЯКЩО `count(zombie, >, 0)` і `custom: «нема їжі під міцелієм»` → ТО `lose`; на перших рівнях після смерті показується підказка.
- КОЛИ `input(undo)` → ТО `undo(1)` (без ліміту, разом із зомбі); КОЛИ `input(restart)` → ТО `restart`.

## Керування і ввід
- Лише миша на ПК (itch): ЛКМ по клітині — дія, яка залежить від стану клітини (поширити / виростити / спожити); ПКМ або стрілка вліво — undo; X — рестарт.
- Геймпад: повна підтримка (Steam), курсор по клітинах (гравці скаржились на чутливий стік).
- Камера рухається (демо 1.5.0).

## Вікна, меню, HUD
- `main-menu`: пасхалка Obo (гарбуз підстрибує, якщо привітатися); музика й звуки окремими кнопками; кнопка виходу.
- `level-select` / `world-map`: селектор рівнів кожного сезону, переходи між сезонами анімацією.
- `game-screen`: поле в сезонному пейзажі; ліворуч — кнопки undo (стрілка) і рестарт, три кружки енергії (`+ui:energy-pips`); праворуч унизу — череп з лічильником «зʼїдено / всього» (`remaining-counter`); угорі праворуч — додому й налаштування; виділення клітини рамкою.
- `settings-window`: гучність музики й ефектів (?), мова (10 мов).
- `end-screen` поразки з підказкою на перших рівнях; титри окремою сценою.

## Фічі поза полем
- `undo` ∞, `restart-level`; пропусків рівнів і підказок нема (гравці просили — розробник визнав лінійність проблемою й опублікував відео-розвʼязки в гайдах).
- `+feature:death-hints` — бессловесне навчання: на перших рівнях кружечки показують, куди клацати; після смерті — підказка.
- `levels-sequential` + `level-unlock` всередині сезону; `world-map` з чотирьох сезонів; Steam-досягнення, хмарні сейви.
- `localization` (10 мов); `high-contrast`-подібна правка: активні плитки отримали товсту рамку, числа на могилах — білий контур (альфа 1.4.1).
- Супутні: друкований міні-пазлбук і Print & Play дуель на двох «грибів» (2026).

## Варіації й родичі
- Джем-версія (MálagaJam Weekend 16) → демо на 60 рівнів (осінь + зима) → повна гра на 120 рівнів (весна й літо додали равликів, гриба-суперника тощо).
- Print & Play Duels — та сама механіка як змагання двох грибів за трупи на папері.
- `games/thinky/starseed-pilgrim.md` — садіння, що розширює досяжну зону; `games/build-sim/game-of-life.md` — поширення клітинами за сусідством, але без бюджету й без гравця.
- **Осі варіацій:** звідки ресурс — фіксований ліміт ходів / їжа на полі (тут) / таймер; як росте мережа — лише від «вузлів»-грибів (тут) / від будь-якої своєї клітини; хто заважає — нікого / рухомі цілі / їдці мережі / суперник з тими самими правилами.

## Цікавинки для курсу
- Бюджет енергії 3 з поповненням їжею і «надлишок згорає» — 📎.
- Двоетапний ріст: міцелій на родючих клітинах, гриб на міцелії, родючість = сусіди грибів — 🥉.
- Могили з таймером, зомбі-ходоки туди-сюди — 📎 (детермінований рух на N ходів уперед).
- Гриб-суперник за тими самими правилами — 🥈 (AI, що грає вашими ж діями).
- Undo, що відкочує і рух зомбі — 🥉 (стан поля як знімок).
- Розвʼязувач рівня: стан = клітини + енергія + позиції зомбі — 🥈.

## Мапа на каталог
- Є: `cell-click` ↔ дія по клітині; `move-limit` ↔ енергія як ліміт ходів; `destroy-all-enemies` + `collect-all` ↔ зʼїсти всіх зомбі; `enemy-patrol` ↔ ходоки; `impassable-cells` ↔ камінь для грибів; `undo-redo`, `undo-unlimited`, `restart-level`; `sequential-levels`, `level-select`, `level-unlock`, `world-map`, `save-progress`; `settings-window`, `main-menu`, `game-screen`, `remaining-counter`; `background-music`, `sound-effects`, `movement-animation`.
- **Нема** → пропозиції карток:
  - `+spread-network` «Мережа росте з клітин-вузлів на сусідні» · entities/state · 🥉.
  - `+energy-budget` «Енергія на дії з малим максимумом» · game-logic/economy · 📎.
  - `+eat-to-refuel` «Зʼїдене поповнює енергію, надлишок згорає» · game-logic/economy · 🌱.
  - `+fertile-adjacency` «Дозволені клітини — сусіди спеціальних» · entities/legality · 🌱.
  - `+grave-timer` «Ціль ховається й виходить за таймером» · entities/spawn · 📎.
  - `+reach-extender` «Клітина, що розширює зону досяжності» · entities/interact · 📎.
  - `+rival-spreader` «Суперник з тими самими правилами росту» · game-logic/opponent · 🥈.
  - `+mushroom-eater` «Ворог, що йде до найближчої клітини мережі й зʼїдає її» · entities/move · 📎.
  - `+wordless-tutorial` «Навчання без слів: підсвітка кліків і підказка після смерті» · interface/hud · 🌱.

## Пропозиції до словників
- `+effect:spread(cell)` — поширити свою мережу на клітину (Mycelium Heaven; уже пропонувалось у корпусі).
- `+cond:fertile(cell)` — клітина сусідить зі «вузлом» мережі.
- `+ui:energy-pips` — кілька кружків енергії замість смуги.
- `+feature:death-hints` — підказка після поразки на навчальних рівнях.
- `+card:energy-budget`, `+card:spread-network` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Mycelium Heaven](https://store.steampowered.com/app/2656520/Mycelium_Heaven/) — «use energy to: spread, bloom, or consume», сезони, «defeat all the zombies»; 27.02.2025, демо.
- [itch.io: Mycelium Heaven](https://3dgoblindev.itch.io/mycelium-heaven) — «3 energy slots… propagate, bloom or consume»; «Tiles next to a Mushrooms are fertile»; «Mycelium tiles can consume corpses»; X — рестарт, ПКМ / стрілка — undo; Unreal Engine; MálagaJam Weekend 16; демо 1–60.
- [Devlog Alpha 1.2.0](https://3dgoblindev.itch.io/mycelium-heaven/devlog/612834/getting-things-ready-for-indie-games-mlaga) — камінь (гриби не ростуть) і могили (зомбі входять і виходять).
- [Відгуки Steam](https://steamcommunity.com/app/2656520/reviews/?browsefilter=toprated) — старт з 3 енергії, дія = 1, кінцівка 2, зомбі — все; ходоки по лінії, пеньок, равлики, гриб-суперник, кілька сіток у рівні, ПКМ — undo.
- [Обговорення: кількість рівнів](https://steamcommunity.com/app/2656520/discussions/0/595142571487928089/) — 120 рівнів, 30 на сезон; гайди з відео — порядок сезонів.
- Новини Steam (devlog #0–#2, Alpha 1.3.5/1.4.1, Demo 1.5.0, «First birthday») — undo відкочує зомбі, рамки плиток, числа на могилах, Switch/PS, PnP-дуель.

## Непевне
- (?) Точна ціна поповнення: «зомбі — до максимуму (3)» і «кінцівка — 2» з двох різних відгуків; чи кінцівки обовʼязково зʼїдати для перемоги — не перевірено.
- (?) Поразка: «без енергії й без їжі» — з опису «without running out of energy» і скарг «you're dead»; точна умова не перевірена.
- (?) Поведінка равликів, гриба-суперника і пеньків — лише з відгуків; механіки літа не знайдено.
- (?) Чи ходять зомбі після кожної дії гравця і що буває при зустрічі ходока з грибом — не перевірено.
- (?) Мобільна версія анонсувалась («including mobile»), на Android була лише альфа на itch.
