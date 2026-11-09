---
title: TRAILS (PurpleSloth)
slug: trails-purplesloth
aka: [Trails]
family: connect-rotate
also: [program-robots]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [PC (Windows, macOS, Linux)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3605120/Trails/", best: true, note: "правила в 3 рядки: малюй маршрути, без повторних клітин і зіткнень, один предмет на корабель, аванпости, небезпеки"}
  - {kind: itch, url: "https://purplesloth.itch.io/trails", note: "той самий опис + девлоги (v1.1–1.3, демо на 20 рівнів)"}
  - {kind: other, url: "https://gamersocialclub.ca/2025/06/10/trails-review", note: "огляд: одночасний рух після Y, покроковий перегляд, збережений прогін, депо, монети, ~40 рівнів"}
  - {kind: other, url: "https://purplesloth.itch.io/trails/devlog/968680/lets-talk-about-difficulty-design-in-puzzle-games", note: "девлог про дизайн складності: монетні рівні, 7 монет, біом midnight"}
  - {kind: other, url: "https://ladiesgamers.com/trails-review", note: "огляд: бонусні рівні, налаштування палітри"}
  - {kind: other, url: "https://kotaku.com/games/trails", note: "коротко: шлях без самоперетину, запуск симуляції, дрони, союзні кораблі"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Trails+PurpleSloth+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [path-drawing, swipe-gestures, keyboard-controls, step-execution, impassable-cells, item-pickup, inventory-limit, key-and-door, completion-detection, satisfy-constraints, world-map, level-select, level-unlock, replay, theme-select, volume-control, game-settings, game-screen, +run-simulation, +collision-fail, +no-revisit-path, +simultaneous-execution, +outpost-delivery, +item-handoff, +crumbling-floor, +collectible-unlock, +undo-redo]
proposes: ["+cond:swap(a, b)", "+effect:handoff", "+ui:run-button", "+ui:route-highlight", "+feature:saved-solution", "+card:no-revisit-path", "+card:simultaneous-execution", "+card:item-handoff", "+card:outpost-delivery"]
author: opus
date: 2026-11-09
---

# TRAILS — намалюй маршрути піщаних кораблів, потім усі рушать одночасно

## Суть
Кожен піщаний корабель має дійти до порту свого кольору; гравець малює його маршрут по клітинах пустелі, а потім запускає виконання — і **всі кораблі рухаються одночасно**, кожен своїм слідом. Маршрут не може двічі зайти в ту саму клітину, кораблі не можуть зіткнутися ні між собою, ні з дронами. Зверху — логістика: корабель везе **один** предмет (вантаж, ключ, підсилення), вантажі треба довезти до аванпостів/депо перед стоянкою, ключі відкривають нові проходи. Родич Trainyard і Cosmic Express: план → симуляція → правка.

## Поле і час
- Квадратна сітка пустелі (3D-рендер, вид згори); клітини: пісок, ями/провалля, піщані гори, вузькі проходи, порти, депо/аванпости, предмети.
- Дві фази: **планування** (статичне малювання маршрутів) і **виконання** (`time: programmed`): на кожен тік кожен корабель робить крок на наступну клітину свого маршруту.
- Виконання можна дивитися покроково; після невдачі — правка маршрутів і новий запуск.
- Розміри полів — (?); пізні рівні більші й тісніші.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Піщаний корабель | object | колір, маршрут, вміст (0–1 предмет) | на тік — крок по своєму маршруту; не відвідує клітину двічі |
| Маршрут | mark | список клітин | малюється гравцем від корабля; без самоперетину і повторних клітин |
| Порт | static | колір | ціль корабля відповідного кольору (sink) |
| Депо / аванпост | static | потрібний вантаж | корабель має привезти вантаж (вода, кактуси) до стоянки |
| Вантаж | pickup | тип (вода, кактус, …) | береться в корабель; займає єдине місце |
| Ключ | pickup | — | відкриває новий прохід (gate) |
| Підсилення (power-up) | pickup | ефект (?) | покращує можливості корабля — які саме, (?) |
| Небажаний предмет | pickup | — | «avoid unwanted items»: забирає місце (?) |
| Прохід під ключ | gate | закритий / відкритий | прохідний після доставки ключа (?) |
| Яма, провалля | hazard | — | корабель не проходить / гине (?) |
| Піщана гора | static | — | непрохідна |
| Обвальна клітина (collapsing terrain) | terrain | ціла / обвалена | руйнується після проїзду (?) |
| Дрон | enemy | траєкторія (?) | зіткнення з кораблем = провал |
| Союзний корабель | ally | — | «support allied ships» — поведінка (?) |
| Золота монета | pickup | — | на бічних рівнях один корабель має довезти її до порту |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cell)` → ЯКЩО `free(cell) and not occupied(cell, route[ship])` → ТО `mark(cell, route[ship])` — клітина додається до маршруту.
- КОЛИ `input(drag, cell)` → ЯКЩО `occupied(cell, route[ship])` → ТО `block` — повторна клітина заборонена (?) — чи відкат до неї, як у Flow Free, не перевірено.
- КОЛИ `input(drag, cell)` → ЯКЩО `cell(cell, mountain)` → ТО `block`.
- КОЛИ `input(run)` (кнопка Y на геймпаді) → ТО `custom: «фаза виконання: усі кораблі стартують разом»`.
- КОЛИ `tick` → ТО `move(ship, next_route_cell)` для **всіх** кораблів одночасно.
- КОЛИ `contact(ship, ship)` → ТО `lose`, `custom: «зіткнення, прогін провалено, повернення до планування»`.
- КОЛИ `tick` → ЯКЩО `custom: «два кораблі міняються клітинами на одному тіку»` → ТО `lose` (?) — чи це зіткнення, не перевірено.
- КОЛИ `contact(ship, drone)` → ТО `lose`.
- КОЛИ `enter(ship, hole)` → ТО `lose` (?) — або клітина просто непрохідна для маршруту (?).
- КОЛИ `leave(ship, collapsing)` → ТО `set_cell(collapsing, chasm)` (?).
- КОЛИ `enter(ship, item)` → ЯКЩО `not has(ship, any)` → ТО `pickup(ship, item)`, `disappear_b`.
- КОЛИ `enter(ship, item)` → ЯКЩО `has(ship, any)` → ТО `custom: «предмет лишається / обмін»` (?).
- КОЛИ `enter(ship, depot)` → ЯКЩО `has(ship, cargo) and same(cargo, depot, kind)` → ТО `take(ship, cargo)`, `custom: «аванпост забезпечено»`.
- КОЛИ `enter(ship, gate)` → ЯКЩО `has(ship, key)` → ТО `take(ship, key)`, `set_cell(gate, open)` (?).
- КОЛИ `adjacent(ship, ship)` → ТО `custom: «передача предмета між кораблями»` (handoff) (?) — механізм не описано.
- КОЛИ `reach(ship, port)` → ЯКЩО `same(ship, port, color)` → ТО `custom: «корабель пришвартовано»`.
- КОЛИ `program_end` → ЯКЩО `custom: «усі кораблі в портах і всі аванпости забезпечені»` → ТО `win`, `next_level`, `custom: «успішний прогін зберігається»`.
- КОЛИ `program_end` → ЯКЩО `has(ship, coin)` у порту → ТО `counter(coins, +1)` (бічні рівні).
- КОЛИ `counter(coins, >=, N)` → ТО `unlock(midnight_levels)` — до 7 монет відкривають 3 рівні біому midnight; поріг N — (?).
- КОЛИ `input(restart)` → ТО `restart` — у будь-який момент.
- Перемога: усі кораблі в портах без зіткнень + усі умови рівня. · Поразка: зіткнення / дрон / яма — без покарання, повтор. · Рахунку нема.

## Керування і ввід
- Малювання маршруту мишею, тачем або геймпадом (рекомендований); налаштування «toggle draw» — клік вмикає/вимикає малювання замість утримання.
- Перемикання між кораблями підсвічує маршрут вибраного, решта лишаються видимими.
- Кнопка запуску (Y на Xbox-геймпаді), покроковий перегляд, швидка правка маршруту, рестарт.
- Повна підтримка геймпадів (Xbox, DualShock, DualSense), Keyboard Only / Mouse Only / Touch Only.

## Вікна, меню, HUD
- `map-window` (overworld): рівні-вузли основного шляху; бічні рівні — відгалуження з «вогняними» іконками; на мапу повертаєшся сам або в глухому куті.
- `game-screen`: поле, маршрути кольорами кораблів, `path-preview`, `run-button`, перемикач кораблів, кнопки кроку й рестарту.
- `tutorial-window` — інтерактивне навчання; гра «textless».
- `settings-window`: гучність музики/ефектів, масштаб тексту інтерфейсу, темна палітра, «sketch»-стиль, колір кораблів, приховати іконки кнопок геймпада, high-contrast.
- `replay-window` (?) — перегляд збереженого успішного прогону пройденого рівня.
- `end-screen` (?) — завершення рівня.

## Фічі поза полем
- `world-map` з основним шляхом (~40 рівнів) і бічними складнішими рівнями; фінальний — єдиний багатоетапний.
- `collectibles` — 7 монет на прихованих бічних рівнях (відкриваються після монетного туторіалу j1) → `level-unlock` біому midnight.
- `replay` — кожен рівень зберігає успішний прогін.
- `step-mode` перегляду виконання; `restart-level`; швидка правка.
- `theme-select` (темна / sketch), `colorblind-palette`-подібний вибір кольору кораблів, `high-contrast`, `font-scale`, `volume-sliders`, `touch-controls`, `gamepad-support`.
- `achievements` (24), `cloud-save`; демо — 20 рівнів (18 основних + 2 бічні).

## Варіації й родичі
- [Trainyard](trainyard.md) — малюєш колію, потяги рушають одночасно, змішування кольорів; [Cosmic Express](cosmic-express.md) — один маршрут, пасажири; [Railbound](railbound.md) — порядок прибуття; [Flow Free](flow-free.md) — кольорові шляхи без перетинів, але статично.
- Frozen Synapse / RoboRally — «план усіх одночасно, потім виконання» (`wego`), але з суперником.
- Осі варіацій: **повторний візит** — дозволено / заборонено (TRAILS) · **конфлікт двох у клітині** — краш / злиття (Trainyard) / черга · **вміст** — нема / 1 предмет / вагони · **виконання** — одночасно / по черзі · **середовище під час прогону** — статичне / обвали й дрони (TRAILS).

## Цікавинки для курсу
- Малювання маршрутів кількох агентів з забороною повторних клітин — 📎.
- Одночасне покрокове виконання з виявленням зіткнень: в одній клітині і **обмін клітинами** (A→B, B→A на тому ж тіку) — 🥉 (класична пастка «swap collision»).
- Ємність 1 предмет, підбір/доставка/ключі: таблиця «клітина × вміст» — 📎.
- Покроковий перегляд і збережений успішний прогін (стан = маршрути, симуляція детермінована) — 🌱.
- Обвальні клітини, що змінюють поле під час прогону, і дрони з власною траєкторією — 🥉.
- Розвʼязувач: пошук сукупних шляхів кількох агентів (multi-agent path finding, час як вимір) — 🥇.

## Мапа на каталог
- Є: `path-drawing` ↔ маршрути; `swipe-gestures` + `keyboard-controls` ↔ ввід; `step-execution` ↔ покроковий перегляд; `impassable-cells` ↔ гори; `item-pickup` + `inventory-limit` ↔ 1 предмет; `key-and-door` ↔ ключі й проходи; `completion-detection` + `satisfy-constraints` ↔ усі умови; `world-map` + `level-select` + `level-unlock` ↔ мапа і монетні рівні; `replay` ↔ збережений прогін; `theme-select`, `volume-control`, `game-settings`, `game-screen`.
- **Нема** → пропозиції карток:
  - `+run-simulation` (Cosmic Express) — фаза план → запуск.
  - `+collision-fail` (Railbound) — зіткнення = провал прогону.
  - `+no-revisit-path` «Маршрут не відвідує клітину двічі» · entities/legality · 🌱.
  - `+simultaneous-execution` «Усі агенти крокують одночасно, перевірка конфліктів після тіку» · game-logic · 🥉 · слот {swap_is_collision: bool}.
  - `+outpost-delivery` «Доставити вантаж у точку до фінішу» · game-logic/win · 📎.
  - `+item-handoff` «Передача предмета між агентами» · entities/interact · 📎.
  - `+crumbling-floor` — клітина обвалюється після проходу.
  - `+collectible-unlock` «Колекційні предмети відкривають приховані рівні» · levels/progression · 🌱.
  - `+undo-redo` — швидка правка маршруту.

## Пропозиції до словників
- `+cond:swap(a, b)` — дві сутності на одному тіку обмінялися клітинами (зіткнення «лоб у лоб» між клітинами).
- `+effect:handoff` — предмет переходить від одного агента до іншого.
- `+ui:run-button` — запуск виконання; `+ui:route-highlight` — підсвітка маршруту вибраного агента.
- `+feature:saved-solution` — гра зберігає успішний розвʼязок рівня для перегляду.

## Джерела
- ⭐ [Steam: TRAILS](https://store.steampowered.com/app/3605120/Trails/) — правило «without visiting the same space twice — and without crashing», 1 предмет на корабель (вантаж, ключі, підсилення), аванпости, перелік небезпек; через appdetails — 24 досягнення, категорії вводу.
- [itch: TRAILS](https://purplesloth.itch.io/trails) + девлоги [v1.1–1.3, демо](https://purplesloth.itch.io/trails/devlog) — «without collisions, dead ends, or backtracking», toggle draw, колір кораблів, демо 20 рівнів.
- [Девлог про складність](https://purplesloth.itch.io/trails/devlog/968680/lets-talk-about-difficulty-design-in-puzzle-games) — монетні рівні, 7 монет, біом midnight, j1.
- [Gamer Social Club: огляд](https://gamersocialclub.ca/2025/06/10/trails-review) — одночасний рух після Y, покроковий перегляд, збережений прогін, депо з водою й кактусами, дрони, ями, гори, ~40 рівнів, бічні рівні.
- [Ladies Gamers: огляд](https://ladiesgamers.com/trails-review) · [Kotaku: картка гри](https://kotaku.com/games/trails) — бонусні рівні, налаштування; «draw lines on a grid», симуляція, дрони, союзні кораблі.
- YouTube: пошук «Trails PurpleSloth gameplay».

## Непевне
- (?) Чи обмін клітинами двох кораблів на одному тіку рахується зіткненням; що буває, коли маршрут закінчився не в порту.
- (?) Як працюють підсилення, передача предметів між кораблями, «небажані» предмети, обвальна земля, пастки, союзні кораблі; рух дронів.
- (?) Чи можна вести маршрут назад (відкат), чи є undo окремо від правки; розміри полів.
- (?) Поріг монет для біому midnight (відомо «up to 7 coins» і 3 рівні); точна кількість рівнів (огляд: «40 or so»).
- (?) Підтримка Steam Deck — не перевірено (є Touch Only і повний геймпад).
