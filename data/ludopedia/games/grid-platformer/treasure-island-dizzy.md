---
title: Treasure Island Dizzy
slug: treasure-island-dizzy
aka: [Dizzy II, "Treasure Island Dizzy (Quattro Adventure)"]
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: free
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: collect
year: 1988
platforms: [ZX Spectrum, Amstrad CPC, C64, NES, Amiga, Atari ST]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Treasure_Island_Dizzy", best: true, note: "одне життя, інвентар бере/кладе верхній предмет, трубка під водою, 30 монет, складність"}
  - {kind: official, url: "https://www.olivertwins.com/treasureislanddizzy", note: "розробники: 3 предмети на одній кнопці, трубка, чому прибрали життя"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dizzy_(series)", note: "серія: інвентар з кількох предметів уперше тут, монети, енергія з Magicland Dizzy"}
  - {kind: other, url: "https://www.mobygames.com/game/3137/treasure-island-dizzy/user-review/2573560/", note: "відгук: порядок предметів важливий"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Treasure+Island+Dizzy+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [inventory, inventory-items, inventory-limit, item-pickup, key-and-door, interaction-table, gravity-fall, touch-death, environment-death, player-death, collect-quota, floor-types, game-screen, +stack-inventory, +passive-carry-item, +give-item-to-npc, +flip-screen-rooms, +one-life-run]
proposes: ["+cond:top_item", "+effect:drop_top", "+card:stack-inventory", "+card:passive-carry-item", "+card:give-item-to-npc", "+card:flip-screen-rooms", "+feature:one-life"]
author: opus
date: 2026-11-09
---

# Treasure Island Dizzy — яйце з одним життям тягає три предмети стосом і застосовує «верхній» як ключ до місця світу

## Суть
Пригодницький платформер з екранів-кімнат острова: Dizzy бігає, стрибає, бере предмети й кладе/застосовує їх у правильному місці (предмет = ключ до конкретної точки світу або NPC). Інвентар — 3 предмети, і все робиться **однією кнопкою**: діє лише предмет зверху списку, тож порядок підбирання — частина головоломки. Життя одне, енергії нема; під водою треба нести трубку — якщо вона «спливла» з верху стосу, Dizzy гине. Друга мета — знайти 30 схованих монет, без яких з острова не випустять.

## Поле і час
- Світ — набір нескролінгових екранів (flip-screen): вихід за край екрана → сусідній екран.
- Рух вільний (піксельний), але екрани зібрані з тайлів: платформи, дерева, драбини-ліани (?), вода.
- Real-time, гравітація; під водою — плавання (лише з трубкою).
- Інформація часткова: видно один екран; частина монет захована за декораціями.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Dizzy | player | 1 життя; інвентар 3 | біг, стрибок; бере/кладе верхній предмет |
| Предмет-ключ | pickup | місце застосування | у правильному місці/біля NPC змінює світ; деінде — просто лежить |
| Трубка (snorkel) | pickup | пасивний | поки в інвентарі — можна бути під водою |
| Монета | pickup | одна з 30 | лічильник; частина за декораціями |
| Крамар (Shopkeeper) | neutral | — | бере предмет-скарб в обмін на човен (?); не випускає без 30 монет |
| Вода | terrain | — | без трубки — смерть |
| Пастки, вогонь, шипи (?) | hazard | — | дотик — смерть |
| Вороги (?) | enemy | мало | дотик — смерть |
| Платформи, дерева, будиночки на деревах | static | — | опора; лабіринт будиночків на деревах |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(dizzy, dir)`; без опори — `fall(dizzy)`.
- КОЛИ `input(jump)` → ТО `custom: «стрибок-сальто по дузі»`.
- КОЛИ `input(action)` → ЯКЩО `occupied(here, pickup)` і `counter(inventory, <, 3)` → ТО `pickup(dizzy, item)`; новий предмет стає верхнім.
- КОЛИ `input(action)` → ЯКЩО `custom: «предметів на місці нема»` → ТО `custom: «верхній предмет кладеться / застосовується»`.
- КОЛИ `custom: «верхній предмет покладено в його місці»` → ТО `set_cell(place, opened)` або `spawn(item)` — предмет-ключ відкриває шлях.
- КОЛИ `custom: «предмет віддано NPC»` → ЯКЩО `has(dizzy, wanted_item)` → ТО `take(dizzy, item)`, `give(dizzy, reward)`.
- КОЛИ `enter(dizzy, water)` → ЯКЩО `not has(dizzy, snorkel)` → ТО `lose`.
- КОЛИ `custom: «під водою покладено верхній предмет, і це трубка»` → ТО `lose` — класична пастка порядку.
- КОЛИ `contact(dizzy, hazard|enemy)` → ТО `lose` (одне життя).
- КОЛИ `contact(dizzy, coin)` → ТО `pickup`, `counter(coins, +1)`.
- КОЛИ `custom: «спроба відплисти з острова»` → ЯКЩО `counter(coins, <, 30)` → ТО `message(text)`, `block`.
- КОЛИ `edge(dizzy)` → ТО `custom: «перехід на сусідній екран»`.
- Перемога: човен + усі 30 монет → відплисти. Поразка: будь-яка смерть = кінець гри. Рахунок: (?).

## Керування і ввід
- Ліво/право, стрибок (на місці або в бік — сальто), одна кнопка дії: взяти / покласти / застосувати.
- Вибору предмета нема: щоб дістати нижній, треба покласти верхні й підібрати в іншому порядку.

## Вікна, меню, HUD
- `splash-screen` / `main-menu` (?).
- `game-screen`: екран острова + рядок з назвою екрана й лічильником монет (?).
- `inventory-window` (?): список із 3 предметів, верхній — активний.
- `end-screen`: смерть → кінець гри; перемога — відплиття.

## Фічі поза полем
- Збережень і продовжень нема: одне життя на всю гру (розробники пізніше назвали це помилкою).
- Друкована розвʼязка журналу й гаряча лінія Codemasters пропускали сховані монети.

## Варіації й родичі
- Dizzy (1987) — 5 життів, 1 предмет; Fantasy World Dizzy — 3 життя; Magicland Dizzy — уперше смуга здоровʼя.
- Пізніші: Spellbound, Prince of the Yolkfolk, Crystal Kingdom, Wonderful Dizzy (2020).
- У корпусі: інвентар-ключ — [Knight Lore](knight-lore.md), [Solstice](solstice.md); кімнати-екрани — [Montezuma's Revenge](montezumas-revenge.md), [Rick Dangerous](rick-dangerous.md).
- Осі: **доступ до інвентаря** (вибір будь-якого / лише верхній-стос / один предмет); **ціна помилки** (енергія / життя / одне життя); **ключ** (кольоровий ключ до дверей / будь-який предмет до будь-якого місця).

## Цікавинки для курсу
- Інвентар-стос: дія лише з верхнім, перебирання через «поклади й підбери» — 🌱.
- Пасивний предмет: дає здатність, поки лежить в інвентарі (трубка) — 🌱.
- Таблиця «предмет × місце → подія світу» як дані, а не код — 🥉.
- Flip-screen світ: перехід через край на сусідній екран з графа екранів — 📎.
- Фінальна квота монет, частину яких сховано за декораціями — 🌱.
- Перевірка «гра не стає непрохідною» (предмет утоплено, трубка загублена) — 🥇.

## Мапа на каталог
- Є: `inventory` · `inventory-items` · `inventory-limit` (3) · `item-pickup` · `key-and-door` (предмет-ключ) · `interaction-table` · `gravity-fall` · `touch-death` · `environment-death` (вода) · `player-death` · `collect-quota` (30 монет) · `floor-types` (вода потребує трубки) · `game-screen`.
- **Нема** → пропозиції карток:
  - `+stack-inventory` «Інвентар-стос: діє лише верхній предмет» · entities/state · 🌱.
  - `+passive-carry-item` «Предмет дає здатність, поки його несеш» · entities/state · 🌱.
  - `+give-item-to-npc` «Віддати предмет NPC в обмін на інший / прохід» · entities/interact · 📎.
  - `+flip-screen-rooms` «Світ з екранів, вихід за край → сусідній екран» · levels/progression · 📎.
  - `+one-life-run` «Одне життя на всю гру, без продовжень» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+cond:top_item(a, item)` — предмет зверху інвентаря A (Treasure Island Dizzy).
- `+effect:drop_top(a)` — A кладе верхній предмет інвентаря.
- `+feature:one-life` — одне життя на гру, без continue.
- `+card:stack-inventory`, `+card:passive-carry-item`, `+card:give-item-to-npc`, `+card:flip-screen-rooms` — див. вище.

## Джерела
- ⭐ [Wikipedia: Treasure Island Dizzy](https://en.wikipedia.org/wiki/Treasure_Island_Dizzy) — одне життя, верхній предмет, трубка, 30 монет, складність, платформи.
- [Oliver Twins: Treasure Island Dizzy](https://www.olivertwins.com/treasureislanddizzy) — 3 предмети на одній кнопці, трубка, чому прибрали життя, лабіринт будиночків на деревах.
- [Wikipedia: Dizzy (series)](https://en.wikipedia.org/wiki/Dizzy_(series)) — еволюція інвентаря, життів і здоровʼя в серії.
- [MobyGames: відгук](https://www.mobygames.com/game/3137/treasure-island-dizzy/user-review/2573560/) — порядок предметів важливий.
- YouTube: пошук «Treasure Island Dizzy gameplay».

## Непевне
- (?) Точна механіка дії: кнопка спершу бере предмет з підлоги, а лише потім кладе верхній, чи відкриває вибір — джерела кажуть лише «верхній предмет».
- (?) Крамар і човен: за одним джерелом — обмін на один із чотирьох скарбів острова; не перевірено.
- (?) Види ворогів і пасток; чи є драбини/ліани; склад HUD і меню — з памʼяті.
- (?) Чи є рахунок очок.
