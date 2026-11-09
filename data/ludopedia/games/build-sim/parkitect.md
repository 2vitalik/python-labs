---
title: Parkitect
slug: parkitect
aka: [Паркітект]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: constraints
year: 2018
platforms: [PC, macOS, Linux]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Parkitect", best: true, note: "огляд: службові будівлі, склади ресурсів, приховані зони для персоналу, гілляста кампанія, co-op до 8"}
  - {kind: steam, url: "https://store.steampowered.com/app/453090/Parkitect/", note: "«тримати зони персоналу подалі від очей», маршрутизація ресурсів до магазинів, 26 сценаріїв"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=1591515214", note: "гайд: зони персоналу, хоулери, депо й труби, службові доріжки"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2318427852", note: "гайд: рейтинг декору, стіни й паркани закривають огляд на туалети/депо"}
  - {kind: other, url: "https://www.texelraptor.com/blog/seven-years-of-parkitect", note: "розробники: лінія видимості для декору, сховати працівників, доставка ресурсів у магазини"}
  - {kind: official, url: "https://www.themeparkitect.com/"}
  - {kind: other, url: "https://www.texelraptor.com/games/parkitect/presskit", note: "пресскіт: шматковий конструктор колії з ресайзом і банкою"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Parkitect+gameplay+logistics+staff+paths", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [impassable-cells, height-levels, multi-cell-size, cell-click, drag-drop-piece, hover-highlight, chase-bfs, line-of-sight-attack, round-currency, game-pause, save-game, sequential-levels, level-unlock, world-map, in-game-editor, level-exchange, game-loop, +queue-line, +track-builder, +agent-needs, +staff-only-path, +staff-zones, +restock-logistics, +sight-penalty, +decoration-rating, +zone-paint]
proposes: ["+role:visitor", "+cond:visible_from", "+effect:queue_join", "+ui:decoration-overlay", "+window:staff-zones", "+card:staff-only-path", "+card:staff-zones", "+card:restock-logistics", "+card:sight-penalty", "+card:decoration-rating"]
author: opus
date: 2026-11-09
---

# Parkitect — парк розваг, де закулісся окреме: службові доріжки й депо для персоналу, а гості псують собі настрій усім, що бачать зі своїх доріжок

## Суть
Тайкун-наступник RollerCoaster Tycoon: рельєф, доріжки, атракціони, магазини, персонал, гості з потребами. Нове для корпусу — **два шари руху і видимості**: доріжки для гостей і **службові** (employee-only), на які гості не заходять; магазини треба **постачати** товаром (хоулери везуть від Deliveries біля входу або через депо з трубами), а гості **бачать** парк — потворні обʼєкти (туалети, депо, службові зони) в лінії видимості знижують рейтинг, стіни й паркани закривають огляд, декор у полі зору — підвищує. Колія гірок — шматкова з ресайзом і власним кутом банки.

## Поле і час
- Квадратна тайлова мапа з висотами рельєфу (деформація, вода), 3D-камера з поворотом і нахилом (?); на тайлі — кілька рівнів (доріжка-міст, колія над, тунель).
- Шари: рельєф · доріжки (гостьові / службові) · атракціони й будівлі N×M · декор (обʼєкти, стіни, паркани) · **зони персоналу** (розмітка доріжок) · підземні транспортні труби.
- Real-time з паузою й швидкостями (?); календар місяцями (за гайдом «Feb–June»); нічний режим — освітлення атракціонів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гостьова доріжка | terrain | висота, стиль | гості ходять і шукають цілі |
| Службова доріжка (employee only) | terrain | — | персонал ходить, гості — ні |
| Табличка на доріжці | gate | — | не пускає гостей на відгалуження за магазинами |
| Черга | terrain | — | FIFO від входу атракціону |
| Атракціон / гірка | object | колія, рейтинги | гості стають у чергу, катаються |
| Шматок колії | tile | напрям, нахил, довжина (ресайз), кут банки | приєднується до кінця попереднього |
| Магазин / кіоск | sink | запас товару, ціна | продає, поки є запас; спорожнів — потрібна доставка |
| Deliveries (біля входу) | source | — | сюди надходять товари для парку |
| Депо (1×2) | container | список прикріплених магазинів | поповнює прикріплені магазини; звʼязане трубою з Deliveries |
| Транспортна труба | conduit | бажано під землею | везе вантаж від Deliveries до депо |
| Туалет, депо, службова будівля | hazard | — | у полі зору гостя — мінус до рейтингу/занурення |
| Декор (обʼєкт, ліхтарі-паркан) | object | — | у полі зору — плюс до рейтингу декору |
| Стіна / паркан | static | висота | перекриває лінію видимості; сам рейтингу не дає |
| Лава | object | — | відновлює енергію гостей |
| Гість | neutral | гроші, щастя, енергія, потреби | ходить гостьовими доріжками, бачить декор і потворне |
| Хоулер | ally | зона | везе товар у магазини своєї зони |
| Прибиральник / охоронець / механік / маскот | ally | зона | працюють лише в призначеній зоні |
| Зона персоналу | zone | імʼя, тайли доріжок | зони не перетинаються; працівник — лише в одній |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, path, kind)` → ТО `place(path)` (тип: гостьова / службова).
- КОЛИ `custom: «гість будує маршрут»` → ЯКЩО `cell(next, employee_path)` або `custom: «табличка заборони»` → ТО `block`.
- КОЛИ `input(drag, staff_zone, path_cells)` → ЯКЩО `not occupied(path_cells, other_zone)` → ТО `set_state(path_cells, zone=id)`; інакше `block`.
- КОЛИ `input(assign, worker, zone)` → ТО `set_state(worker, zone=id)` — `custom: «працівник лише в одній зоні»`.
- КОЛИ `counter(shop.stock, <, n)` → ЯКЩО `custom: «магазин не прикріплено до депо»` → ТО `carry(hauler, goods: deliveries → shop)` службовими/гостьовими доріжками.
- КОЛИ `counter(shop.stock, <, n)` → ЯКЩО `connected(depot, deliveries, tube)` і `custom: «магазин у списку депо»` → ТО `custom: «депо поповнює магазин з тилу»`.
- КОЛИ `input(add, depot, shop)` → ТО `custom: «прикріпити магазин до депо (кнопка Add)»`.
- КОЛИ `counter(shop.stock, =, 0)` → ТО `custom: «магазин не продає»`.
- КОЛИ `tick` → ЯКЩО `line_of_sight(guest, hazard)` (туалет, депо, службова зона) → ТО `custom: «рейтинг декору тайла −, щастя/занурення −»`.
- КОЛИ `tick` → ЯКЩО `line_of_sight(guest, decor)` → ТО `custom: «рейтинг декору +»`.
- Стіна/паркан між гостем і обʼєктом → `line_of_sight` = false (закрити туалет стінами — мінус зникає).
- КОЛИ `custom: «енергія гостя низька»` → ЯКЩО `custom: «поруч лава»` → ТО `custom: «відпочинок»`.
- КОЛИ `reach(guest, ride_entrance)` → ТО `custom: «стати в кінець черги»`.
- КОЛИ `input(add_piece, track)` → ЯКЩО `legal(piece)` → ТО `place(piece)`; `custom: «ресайз довжини, свій кут банки»`.
- КОЛИ `custom: «декор біля атракціону»` → ТО `custom: «excitement +»` (?).
- КОЛИ `all_constraints_met` (цілі сценарію) → ТО `win` → `unlock(next_scenarios)` на мапі кампанії.

## Керування і ввід
- Миша: інструменти рельєфу, доріжок (вибір типу: гостьова / службова / черга), будівель, декору, колії.
- Drag по доріжці — намалювати зону персоналу; панель персоналу — найняти й призначити в зону.
- Вибрати депо → «Add» → клікнути магазини; труби — drag, бажано під землею.
- Конструктор колії: наступний шматок, ресайз, банка; тест; або готовий дизайн.

## Вікна, меню, HUD
- `main-menu`: кампанія → `world-map` (гілляста мапа сценаріїв) · пісочниця · редактор сценаріїв · мультиплеєр · Workshop · `settings-window`.
- `game-screen`: 3D-поле, панелі інструментів, гроші, дата, гості.
- Оверлей рейтингу декору (`+ui:decoration-overlay`): тайли «погано / нормально / добре» (?).
- Вікно атракціону (`custom-window`): рейтинги, ціна, черга, обслуговування.
- `+window:staff-zones` — список зон з іменами («Shops #1») і працівниками.
- Вікно гостя: потреби, думки (`+ui:thought-bubble` — пропоноване в RCT).
- Вікно депо (`custom-window`): прикріплені магазини.

## Фічі поза полем
- Кампанія з 26 сценаріїв, гілляста `world-map`, DLC-кампанії (Taste of Adventure, Booms & Blooms).
- `mode-sandbox` з генератором рельєфу; редактор сценаріїв (`level-editor`).
- `mode-coop` online до 8 гравців (кампанія й пісочниця).
- Steam Workshop: парки, сценарії, декор, моди (`level-sharing`, `mod-support`).
- Нічний режим, збереження дизайнів колії (?).

## Варіації й родичі
- У корпусі: `rollercoaster-tycoon` (рельєф у кутах, черги, рейтинги колії, гості з потребами — база), `prison-architect-rooms` (двері з таблицею доступу для ролей), `theme-hospital` (черги до кімнат).
- Planet Coaster (вільний сплайн), RCT2/3, OpenRCT2.
- **Осі варіацій «закулісся»**: нема (RCT) / окремі службові доріжки + зони (Parkitect) · **«видимість»**: краса довкола тайла без лінії видимості (RCT-сценерія) / лінія видимості, яку перекривають стіни (Parkitect) · **«постачання»**: магазини безкінечні (RCT) / товар везуть агенти або труби (Parkitect).

## Цікавинки для курсу
- Два класи доріжок: агент-гість не може ступити на службову — фільтр сусідів у BFS — 🌱.
- Зони персоналу як розмітка тайлів, що не перетинаються; працівник шукає роботу лише в своїй зоні — 📎.
- Постачання: запас магазину спадає, хоулер везе з Deliveries, депо обслуговує список магазинів — 🥈.
- Лінія видимості гостя до «потворного» з перекриттям стінами (raycast по сітці з висотою) — 🥉.
- Рейтинг декору тайла як сума видимого декору мінус видимі потворні обʼєкти — 📎.
- Конструктор колії з ресайзом і кутом банки — 🥈 (див. `rollercoaster-tycoon`).

## Мапа на каталог
- Є: `impassable-cells` · `height-levels` · `multi-cell-size` · `cell-click` + `drag-drop-piece` + `hover-highlight` · `chase-bfs` (гості й персонал) · `line-of-sight-attack` (механізм лінії видимості; тут «атакує» настрій) · `round-currency` · `game-pause` · `save-game` · `sequential-levels` + `level-unlock` + `world-map` · `in-game-editor` + `level-exchange` · `game-loop`.
- **Нема** → пропозиції карток:
  - `+staff-only-path` «Доріжки лише для одного класу агентів» · entities/legality · 🌱.
  - `+staff-zones` «Зони роботи персоналу, що не перетинаються» · game-logic · 📎 · слоти {roles, exclusive}.
  - `+restock-logistics` «Запас точки поповнюють агенти або мережа» · game-logic/economy · 🥈.
  - `+sight-penalty` «Обʼєкт у полі зору агента змінює його стан» · entities/state · 🥉 · слоти {radius, blockers}.
  - `+decoration-rating` «Рейтинг тайла за видимим декором» · game-logic/score · 📎.
  - `+queue-line`, `+track-builder`, `+agent-needs`, `+zone-paint` — пропоновані раніше, підтвердження.

## Пропозиції до словників
- `+role:visitor` — автономний клієнт з потребами (гість) — повторно після RCT/Theme Hospital.
- `+cond:visible_from(a, b)` — B видно з позиції A з урахуванням стін і висот (відмінно від `line_of_sight` по прямій ряду).
- `+effect:queue_join` — стати в кінець черги (повторно).
- `+ui:decoration-overlay` — теплова мапа рейтингу декору.
- `+window:staff-zones` — керування зонами персоналу.
- `+card:staff-only-path`, `+card:staff-zones`, `+card:restock-logistics`, `+card:sight-penalty`, `+card:decoration-rating` — див. вище.

## Джерела
- ⭐ [Wikipedia: Parkitect](https://en.wikipedia.org/wiki/Parkitect) — службові будівлі, склади ресурсів, приховані зони для персоналу, гілляста кампанія, co-op до 8.
- [Steam](https://store.steampowered.com/app/453090/Parkitect/) — «keep the staff areas out of the public eye», маршрутизація ресурсів до магазинів, 70+ атракціонів, 26 сценаріїв, редактор, пісочниця.
- [Гайд: зони персоналу й депо](https://steamcommunity.com/sharedfiles/filedetails/?id=1591515214) — зони не перетинаються, працівник в одній зоні, депо 1×2 за магазинами, «Add», труба до Deliveries, службова доріжка або табличка, гості не люблять бачити депо.
- [Гайд: рейтинг декору](https://steamcommunity.com/sharedfiles/filedetails/?id=2318427852) — туалет — мінус, обгородити — мінус зникає; стіни/паркани лише перекривають огляд; лави й енергія.
- [Texel Raptor: Seven years of Parkitect](https://www.texelraptor.com/blog/seven-years-of-parkitect) — лінія видимості для декору й рейтингів (Alpha 19), сховати працівників, доставка ресурсів у магазини.
- [Пресскіт](https://www.texelraptor.com/games/parkitect/presskit) — шматковий конструктор колії з ресайзом і банкою, генератор рельєфу.

## Непевне
- (?) Як точно рахується рейтинг декору (радіус, вага, штраф за невідповідність теми) — гайди не пояснюють.
- (?) Звідки фізично приходять товари в Deliveries (вантажівка біля входу?) — з памʼяті.
- (?) Чи декор біля атракціону підвищує excitement — лише коментар гравця.
- (?) Набір рейтингів атракціону (Excitement/Intensity/Nausea як у RCT), швидкості гри, консольні версії — з памʼяті.
- (?) Гайди Steam позначені «removed» — механіку варто звірити у грі.
