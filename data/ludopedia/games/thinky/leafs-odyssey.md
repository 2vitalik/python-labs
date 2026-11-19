---
title: Leaf's Odyssey
slug: leafs-odyssey
aka: [Leafs Odyssey]
family: thinky
also: [roguelike]
klass: avatar
axes:
  field: layers
  time: turn
  opponent: ai
  info: full
  random: none
  goal: state
year: 2024
platforms: [PC (Windows/macOS/Linux), Steam Deck]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2880750/Leafs_Odyssey/", best: true, note: "опис, теги, 10 скриншотів кімнат із HUD; 100+ пазлів, редактор"}
  - {kind: itch, url: "https://themsalltook.itch.io/leafs-odyssey", note: "та сама гра на itch (акаунт автора themsalltook), devlog патчів"}
  - {kind: official, url: "https://ludobloom.com/", note: "сайт ludobloom (Alex Diener): ігри студії, лінки"}
  - {kind: other, url: "https://ludobloom.com/leafsodyssey_worlds.html", note: "54 світи спільноти (.world): класичні правила й експериментальні"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2880750&count=30&maxlength=0", note: "усі патчноути 1.0.3–1.1.0: назви монстрів і плиток, правила атаки, стосів, умиротворення"}
  - {kind: other, url: "https://steamcommunity.com/app/2880750/discussions/", note: "обговорення: руїни статуй без висоти, смерть Leaf, журнал спостережень"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Leaf%27s+Odyssey+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [move-by-input, keyboard-controls, push-object, impassable-cells, floor-types, inertia-slide, height-levels, touch-death, player-death, key-and-door, button-toggle, destructible-blocks, explode-area, destroy-all-enemies, codex-window, world-map, minimap-radar, undo-unlimited, redo, restart-level, checkpoint, replay, stats-window, in-game-editor, editor-playtest, level-exchange, controls-remap, background-music, +bump-attack, +flee-player, +wake-on-event, +push-chain, +flip-screen-rooms, +fast-travel-points, +player-notes, +poison-trail, +pacify-floor, +entity-stacking, +observation-journal, +corpse-stepping-stone]
proposes: ["+trigger:attacked", "+trigger:explosion", "+cond:pacified", "+cond:same_elevation", "+effect:leave_trail", "+effect:flee", "+window:world-select", "+ui:room-status-counters", "+feature:observation-journal", "+feature:replay-autosave", "+feature:room-checkpoint", "+card:pacify-floor", "+card:poison-trail", "+card:entity-stacking", "+card:observation-journal", "+card:corpse-stepping-stone"]
author: opus
date: 2026-11-19
---

# Leaf's Odyssey — тхір Leaf зачищає кімнати від монстрів, кожен хід яких передбачуваний

## Суть
Покрокова головоломка-пригода від ludobloom (Alex Diener): тхір Leaf іде вежею Tower of Destiny, кімната за кімнатою, і в кожній має перемогти монстрів, щоб розвʼязати пазл. Формула — «DROD-подібна»: монстри ходять, коли ходиш ти, кожен вид — за своїм правилом, тож «кожен хід можна передбачити» (Steam). Поверх боїв — кольорові ключі, натискні плити, перемикачі, двері, лід, отрута, вибухи і стоси сутностей на різній висоті. Поразки як покарання нема: Leaf атакований → знебарвлений екран → undo.

## Поле і час
- Квадратна сітка, вид згори; світ = граф кімнат з координатами (x, y, z), сусідні кімнати зʼєднані краями, поверхи — драбинами (форум: кімнати `(-1, 0, -1)` і `(0, 0, -1)` на «floor level 1»).
- Висота — окремий шар: сутності лежать **стосами** (до 100 у клітині з 1.0.10), блок може лежати на монстрі, ключ — на Leaf; лінія погляду монстра іншого кольору, якщо він на іншій висоті. Руїни статуї перекриваються, але висоти не дають (розробник на форумі).
- Хід = дія Leaf (крок / атака / очікування / взаємодія), потім монстри — у визначеному порядку ходу (патчі 1.0.9 і 1.0.17 правили саме «turn processing order»).
- Видимість повна в межах кімнати; невідвідані сусідні кімнати на мінікарті — «?».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Leaf (тхір) | player | висота; стан «умиротворений» | крок у сусідню клітину, атака, очікування, взаємодія (драбина, вказівник, waypoint); може нести сутність на голові |
| Бомбожук (bomb bug) | enemy | орієнтація; стан primed | тікає від блоків-монстрів; розвернувшись на попередньому ході, стає primed; може нести обʼєкти на спині; вибухає (?) |
| Слимак (slug) | enemy | — | лишає за собою слід отрути; гинучи, прибирає отруту під собою |
| Летючий змій (flying snake) | enemy | вісь руху; висота | літає й змінює висоту; рухається вздовж осі (?); може нести push block |
| Гнівне око (angry eye) | enemy | промінь погляду | бачить Leaf по лінії (промінь показано на полі); гине на отруті |
| Статуя | enemy | спить / пробуджена | пробуджується за подією (?); гинучи, лишає руїни; у воді стає каменем-переходом |
| Блок-монстр (monster block) | enemy | — | від нього тікають бомбожуки; поведінка (?) |
| Руїни статуї | object | без висоти | на них можна класти інше; вибух їх знищує |
| Камінь-перехід (stepping stone) | terrain | — | статуя у воді; по ньому ходять |
| Push block | object | — | штовхається; на льоду ковзає; може лежати на монстрі |
| Multipush block | object | — | штовхається разом із сусідніми (ланцюг) (?) |
| Block barrier | static | — | бар'єр для блоків; з 1.0.10 блок може лежати на ньому |
| Ключі (жовтий, синій, terra, зоряний…) | pickup | тип | у HUD 5 лічильників; не береться на ході 0 і з іншої висоти |
| Замкнені двері | gate | — | відкриваються за ключ (ключ витрачається); закриті — блокують waypoint |
| Ворота монстрів (monster gate) | gate | відкрито / закрито | відкриваються, коли кімнату зачищено (?); закриваючись, стирають отруту |
| Натискна плита | switch | привʼязка дверей | тримається вагою; перемикає привʼязані двері й підлоги |
| Перемикач (toggle switch) | switch | привʼязка | переносний обʼєкт: падаючи на плиту, тримає її; стирає отруту |
| Жертовний вівтар (sacrifice altar) | switch | привʼязка | спрацьовує від загибелі на ньому (?) |
| Toggle door / toggle floor | gate | open / closed | стан змінюють плити, вівтарі, перемикачі |
| Люк (trapdoor) | terrain | над ямою / водою / льодом | провалюється (?) |
| Розжарене вугілля (hot coals) | hazard | — | сутність на ньому згоряє; світиться, коли комусь загрожує |
| Лід | terrain | — | ковзання блоків і (?) Leaf |
| Вода · яма · небо · космос | terrain | — | непрохідні для ходячих; у яму падають |
| Умиротворююча підлога (pacific floor) | terrain | — | хто на ній — умиротворений: не атакує, не йде драбиною чи waypoint |
| Слід отрути | hazard | — | шкодить монстрам (око гине) (?); не лягає на стіни |
| Висока трава · очерет · штори | terrain | накладка | співіснують із люками й підлогами; ефект (?) |
| Тріснута стіна | static | — | руйнується (вибухом?) |
| Стіни, колони, дерева, паркани, ліхтарі, rough stone | static | — | непрохідні перешкоди |
| Драбина | terrain | одностороння / двостороння | перехід в іншу кімнату чи поверх |
| Waypoint (кристал на постаменті) | terrain | активовано / ні | швидке переміщення між кімнатами й у межах кімнати |
| Вказівник (signpost) | static | текст | текст при взаємодії |
| Зірка мети (goal star) | pickup | — | фінальна ціль: кінець гри / світу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(leaf, dir)`; інакше `block`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(next_cell, push_block)` and `free(cell_behind)` → ТО `push`, `move(leaf, dir)`; інакше `block`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(next_cell, monster)` and `not state(leaf, pacified)` → ТО `custom: «атака: знищується лише перша атакована сутність у клітині, решта стосу лишається»` (патч 1.0.10); атака рухом — (?).
- КОЛИ `input(wait)` → ТО хід минає без руху.
- КОЛИ `turn_end(leaf)` → ТО кожен монстр робить крок за правилом свого виду в порядку ходу.
- КОЛИ `contact(monster, leaf)` → ТО `lose`: «коли Leaf атаковано», екран знебарвлюється (розробник); далі undo або рестарт кімнати.
- КОЛИ `enter(a, pacific_floor)` → ТО `set_state(a, pacified)` (видно світіння).
- КОЛИ `input(ladder|waypoint|room_exit)` → ЯКЩО `state(leaf, pacified)` → ТО `block` — і для переходу в кімнату, де монстра стерло б при вході.
- КОЛИ `custom: «Leaf входить у кімнату на клітину монстра»` → ТО `disappear_b` (монстра стерто; кімната може бути зачищена на ході 0).
- КОЛИ `leave(slug, cell)` → ТО `set_cell(cell, poison_trail)`.
- КОЛИ `died(slug)` → ТО `set_cell(cell, floor)` (отрута під ним зникає).
- КОЛИ `enter(angry_eye, poison_trail)` → ТО `disappear_a` (запис у журналі); дія отрути на інших монстрів — (?).
- КОЛИ `enter(toggle_switch, poison_trail)` → ТО `set_cell(cell, floor)`.
- КОЛИ `custom: «ворота монстрів закриваються»` → ТО `set_cell(cell, floor)` — отрута під ними теж зникає.
- КОЛИ `turn_end(leaf)` → ТО бомбожук `custom: «тікає від найближчого блока-монстра; при рівних відстанях — фіксована перевага схід/захід»`.
- КОЛИ `custom: «бомбожук розвернувся на попередньому ході»` → ТО `set_state(bomb_bug, primed)`; вибух — `explode(area, ?)` (?).
- КОЛИ `custom: «вибух накрив статую»` → ТО `disappear_b` без руїн (запис журналу 1.0.13); вибух знищує й руїни.
- КОЛИ `died(statue)` → ЯКЩО `custom: «не від вибуху»` → ТО `spawn_at(rubble, cell)`.
- КОЛИ `enter(statue, water)` → ТО `transform(statue, stepping_stone)`.
- КОЛИ `custom: «статую пробуджено»` → ТО `set_state(statue, awake)`; умова пробудження — (?).
- КОЛИ `line_of_sight(angry_eye, leaf)` → ТО `custom: «промінь ока»`; наслідок для Leaf — (?).
- КОЛИ `enter(push_block, ice)` → ТО `slide(push_block, dir)`.
- КОЛИ `contact(leaf, key)` → ЯКЩО `custom: «та сама висота і хід ≠ 0»` → ТО `pickup`, `counter(keys[type], +1)`.
- КОЛИ `contact(leaf, locked_door)` → ЯКЩО `has(leaf, key)` → ТО `take(leaf, key)`, `disappear_b`; інакше `block`.
- КОЛИ `enter(a, pressure_plate)` → ТО `set_state(wired_targets, toggle)`.
- КОЛИ `leave(a, pressure_plate)` → ТО `set_state(wired_targets, toggle)` — стан повертається (?).
- КОЛИ `custom: «сутність лишається на вугіллі»` → ТО `custom: «згоряє»` (?) — гра підсвічує загрозу.
- КОЛИ `all_gone(monster)` у кімнаті → ТО кімната Cleared, `set_state(monster_gate, open)` (?).
- КОЛИ `input(interact)` на драбині → ТО `teleport(leaf, linked_room)`; одностороння драбина назад не веде.
- КОЛИ `input(waypoint_travel)` → ЯКЩО `custom: «шлях не перекрито замкненими дверима, Leaf не умиротворений»` → ТО `teleport(leaf, waypoint)`.
- КОЛИ `contact(leaf, goal_star)` → ТО `win`.
- КОЛИ `input(undo)` → ТО `undo(1)`; redo, рестарт кімнати (спершу — до чекпойнта кімнати).
- Перемога: зачистити кімнати й дійти до зірки мети; зоряні ключі — додаткова ціль. · Поразка: Leaf атаковано → знебарвлення, undo. · Рахунку нема; статистика — час і проходження.

## Керування і ввід
- Клавіатура (перепризначувана) або геймпад (DualShock, Steam Deck): крок, очікування, взаємодія, undo/redo з прискоренням при утриманні (×2 після 10 дій).
- Миша: ПКМ — огляд клітини (монстри й блоки отримують літери A, B, C…, показано орієнтацію і стан primed); Shift+клік — подорож до waypoint.
- G — сітка, P — пауза; журнал — своєю клавішею; режим курсора на геймпаді.

## Вікна, меню, HUD
- `main-menu` → `world-select` (custom-window): вибір світу, сортування за датою, «Import World», «Download more worlds».
- `game-screen`: кімната + ліва панель: назва кімнати вгорі, значок журналу, лічильники Explored / Cleared / Uncleared, 5 лічильників ключів, `minimap` з «?» і «!».
- `codex-window` (журнал): список монстрів, у кожного — спостереження, що відкриваються, коли гравець щось побачив; позначка «NEW».
- `map-window`: прокручувана мапа світу, змінені кімнати, напрямки огляду невідвіданих кімнат.
- `pause-menu`: Marks and Notes, Statistics, чекпойнт кімнати, сітка.
- `replay-window`: повтор кімнати зі сталою швидкістю, перемотка в кінець.
- `editor-window`: кімнати, стос-редактор, привʼязки механізмів, тест кімнати.
- `end-screen`: підсумок гри з переглядом кімнат.
- Переходи: main-menu → world-select → game-screen ↔ codex-window / map-window / pause-menu.

## Фічі поза полем
- `undo` без ліміту + `redo`, `restart-level` кімнати, чекпойнт кімнати з меню паузи.
- `replay` — автозапис повтору при першому відвідуванні кімнати; `stats` у меню паузи.
- `codex`, що наповнюється спостереженнями; підказок нема (гравці хвалять «сміливість без hint»).
- `level-editor` + `level-sharing`: файли `.world`, сторінка 54 світів спільноти.
- `world-map`, `fast-travel` через waypoints, `remap-controls`, `gamepad-support`, `grid-toggle`, сон персонажа після хвилини бездіяльності.

## Варіації й родичі
- Родичі в корпусі: [DROD](drod.md) (кімнати, детерміновані монстри, зачистка), [Void Stranger](void-stranger.md), [Hoplite](../tactics/hoplite.md), [Into the Breach](../tactics/into-the-breach.md), [Chip's Challenge](../maze-arcade/chips-challenge.md) (ключі, лід, кнопки), [Sokoban](../push-slide/sokoban.md).
- Осі варіацій:
  - **чим гравець бʼє**: дотиком-кроком (тут) / зброєю в сусідній клітині (DROD) / дистанційно;
  - **висота**: пласке поле / стоси сутностей на висотах (тут) / рельєф;
  - **що вимикає атаку**: нічого / підлога-умиротворення (тут);
  - **знання про монстрів**: довідка одразу / журнал спостережень, що відкривається від побаченого (тут).

## Цікавинки для курсу
- Стос сутностей у клітині з висотою: атака бʼє лише верхню, промінь ока залежить від висоти — 🥈.
- Слимак лишає слід отрути, отрута вбиває інших монстрів — 📎.
- Бомбожук: втеча від найближчого блока-монстра з фіксованим розвʼязком нічиєї + стан primed — 🥉.
- Умиротворююча підлога як стан, що забороняє дії (атака, драбина) — 🌱.
- Журнал, що відкриває рядки лише після спостереження події на полі — 🥉.
- Детермінізм + автозапис повтору кімнати як послідовності ходів — 🥈.

## Мапа на каталог
- Є: `move-by-input` · `keyboard-controls` · `push-object` · `impassable-cells` · `floor-types` · `inertia-slide` (лід) · `height-levels` (висота стосів) · `touch-death` · `player-death` · `key-and-door` · `button-toggle` · `destructible-blocks` (тріснуті стіни) · `explode-area` · `destroy-all-enemies` (зачистка кімнати) · `codex-window` (журнал) · `world-map` · `minimap-radar` · `undo-unlimited` · `redo` · `restart-level` · `checkpoint` · `replay` · `stats-window` · `in-game-editor` · `editor-playtest` · `level-exchange` · `controls-remap` · `background-music`.
- **Нема** → пропозиції карток:
  - `+bump-attack` (вже в корпусі) — тут атака знищує лише першу сутність стосу.
  - `+flee-player` (вже в корпусі) — тут утеча від блоків-монстрів, а не від гравця.
  - `+wake-on-event` (вже в корпусі) — статуї.
  - `+push-chain` (вже в корпусі) — multipush block.
  - `+flip-screen-rooms`, `+fast-travel-points`, `+player-notes` — вже в корпусі.
  - `+poison-trail` «Слід, що вбиває інших» · entities/interact · 📎 · слот {victims} — слимак.
  - `+pacify-floor` «Підлога вимикає атаку» · entities/state · 🌱.
  - `+entity-stacking` «Стос сутностей у клітині з висотою» · entities/state · 🥈 · слот {max: 100}.
  - `+observation-journal` «Журнал відкривається спостереженням» · interface/menus · 🥉.
  - `+corpse-stepping-stone` «Тіло ворога у воді стає мостом» · entities/interact · 🌱.

## Пропозиції до словників
- `+trigger:attacked` — сутність атакована (смерть Leaf, удар по стосу); `+trigger:explosion` — вибух накрив клітину.
- `+cond:pacified` — сутність умиротворена підлогою; `+cond:same_elevation` — сутності на одній висоті (ключ, промінь ока).
- `+effect:leave_trail` — слід отрути за слимаком; `+effect:flee` — утеча бомбожука.
- `+window:world-select` — вибір і імпорт світів (журнал — ⏳ `codex-window`).
- `+ui:room-status-counters` — Explored / Cleared / Uncleared.
- `+feature:observation-journal`, `+feature:replay-autosave`, `+feature:room-checkpoint`.
- `+card:pacify-floor`, `+card:poison-trail`, `+card:entity-stacking`, `+card:observation-journal`, `+card:corpse-stepping-stone` — див. «Мапа на каталог».
- ⏳-слова, вжиті тут: `input`, `turn_end`, `enter`, `leave`, `died`, `line_of_sight`, `all_gone`, `free`, `occupied`, `state`, `has`, `set_state`, `set_cell`, `spawn_at`, `transform`, `slide`, `take`, `explode`, `undo`.

## Джерела
- ⭐ [Steam: Leaf's Odyssey](https://store.steampowered.com/app/2880750/Leafs_Odyssey/) — «turn-based game where you fight various monsters», «Every move can be predicted», 100+ пазлів, редактор; 10 скриншотів із HUD (лічильники кімнат і ключів, мінікарта, журнал), назви кімнат, монстри.
- [Steam News API: патчноути 1.0.3–1.1.0](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2880750&count=30&maxlength=0) — головне джерело правил: атака по стосу, стоси до 100, отрута слимака, втеча й primed бомбожука, руїни і камінь-перехід статуй, око на отруті, умиротворення, ключі на ході 0, вівтарі й перемикачі, waypoints.
- [itch.io](https://themsalltook.itch.io/leafs-odyssey) — «Failure is not punished; you can undo», devlog.
- [Світи спільноти](https://ludobloom.com/leafsodyssey_worlds.html) — формат `.world`, Import World, 54 світи.
- [Steam-форум](https://steamcommunity.com/app/2880750/discussions/) — розробник: «When Leaf is attacked… desaturate the screen»; «rubble… doesn't provide any elevation»; журнал отримав запис про вибух статуї після питання гравця.

## Непевне
- (?) Механіка атаки Leaf: крок у клітину монстра (bump) — висновок із патчів («attacked position», «push… short circuit an attack»); чи заходить Leaf у клітину після вбивства — невідомо.
- (?) 4 чи 8 напрямків руху — не перевірено.
- (?) Правила руху монстрів (вісь змія, умова пробудження статуї, що робить промінь ока, як і коли вибухає бомбожук, що таке блок-монстр) — в журналі гри, якого не бачив.
- (?) Ворота монстрів відкриваються після зачистки (як зелені двері DROD) — висновок із «cleared rooms» і скриншотів.
- (?) Вівтар — загибель монстра на ньому; люк — провал після сходження; ковзання самого Leaf на льоду; дія високої трави.
- (?) Кількість рівнів: «100+» у кампанії Tower of Destiny; поверхів і кімнат точно не знаю.
