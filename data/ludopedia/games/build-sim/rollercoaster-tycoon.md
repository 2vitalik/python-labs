---
title: RollerCoaster Tycoon
slug: rollercoaster-tycoon
aka: [RCT, RCT1, OpenRCT2, RollerCoaster Tycoon Classic]
family: build-sim
also: []
klass: cursor
axes:
  field: iso
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: constraints
year: 1999
platforms: [PC, Xbox]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/RollerCoaster_Tycoon_(video_game)", best: true, note: "тайлова мапа, рельєф і вода, доріжки, колія з шматків, персонал, 21 сценарій, Mega Park, доповнення"}
  - {kind: other, url: "https://docs.openrct2.io/en/latest/playing/landscaping/index.html", note: "OpenRCT2: висота кутів тайла, гірський інструмент, вода, право на землю vs право на будову"}
  - {kind: other, url: "https://docs.openrct2.io/en/latest/playing/footpath/index.html", note: "OpenRCT2: доріжки й черги, автозʼєднання сусідніх тайлів, мости"}
  - {kind: other, url: "https://github.com/OpenRCT2/OpenRCT2/wiki/Peep-AI", note: "пошук шляху гостей: бюджет кроків і перехресть, оцінка відстані, без розвороту"}
  - {kind: other, url: "https://github.com/OpenRCT2/OpenRCT2/wiki/Ride-rating-calculation", note: "Excitement/Intensity/Nausea: G-сили, спуски, інверсії, декор біля станції, штрафи"}
  - {kind: other, url: "https://github.com/OpenRCT2/OpenRCT2/wiki/Sizes-and-angles-in-the-game-world", note: "кути схилів колії"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=RollerCoaster+Tycoon", note: "пошук; Classic/Deluxe"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=RollerCoaster+Tycoon+1999+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [height-levels, multi-cell-size, impassable-cells, cell-click, drag-drop-piece, hover-highlight, chase-bfs, random-walk, round-currency, game-pause, save-game, save-multi-slot, objective-text, status-panel, sequential-levels, level-unlock, minimap-radar, game-loop, +corner-heights, +queue-line, +track-builder, +ride-ratings, +agent-needs, +land-rights, +drag-build-line, +entity-rotate, +breakdown-repair, +litter-cleanup, +pathfind-budget, +town-builder]
proposes: ["+card:corner-heights", "+card:queue-line", "+card:track-builder", "+card:ride-ratings", "+card:agent-needs", "+card:land-rights", "+card:breakdown-repair", "+card:pathfind-budget", "+trigger:month_start", "+cond:prefers", "+effect:queue_join", "+effect:vomit", "+role:visitor", "+ui:thought-bubble", "+ui:ride-stats-graph", "+window:track-designer", "+window:research-window", "+window:finance-window", "+feature:track-design-save"]
author: opus
date: 2026-11-09
---

# RollerCoaster Tycoon — парк на тайлах з висотою кутів: доріжки й черги вели гостей, колію збирають зі шматків, а її форма дає рейтинги атракціону

## Суть
Гравець будує парк розваг за сценарієм: ліпить рельєф, кладе доріжки й черги, ставить атракціони, ларьки, туалети, наймає персонал і ставить ціни. Клітинне ядро — **тайл із висотою кожного кута** (схили, обриви, вода), по якому йдуть **доріжки** (автозʼєднання з сусідами, схили, мости) і **колія** американських гірок, яку гравець складає шматок за шматком (напрям, висота, крутизна, елементи). Готова колія «їздить» на тесті, і з її геометрії рахуються **Excitement / Intensity / Nausea**, від яких залежить, хто з гостей піде кататись. Гості — автономні агенти з потребами, що шукають шлях доріжками, стають у **чергу** і думають уголос.

## Поле і час
- Квадратна тайлова мапа в ізометрії, поворот на 4 сторони; кожен тайл має висоти **чотирьох кутів** (плоский, схил, сідло, обрив); вода — рівень над рельєфом, сама утворює підпірні стінки.
- Вертикаль: на одному тайлі може бути кілька елементів на різних висотах (земля, тунель колії, доріжка-міст, колія над нею) — `field: iso` з реальними шарами висоти.
- Межа парку: свої тайли (можна все), **права на будову** (можна будувати над/під, але не міняти землю), чужі тайли продаються.
- Real-time, календар місяцями (березень–жовтень (?)), регулятор швидкості нема в RCT1 (?), пауза.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тайл землі | terrain | висоти 4 кутів, тип ґрунту, власник (парк / право на будову / ні) | міняється інструментом рельєфу; схил кута визначає, що можна поставити |
| Вода | terrain | рівень | заливає тайли нижче рівня; на ній — водні атракціони |
| Доріжка | terrain | стиль, схил | автоматично зʼєднується з сусідніми доріжками в перехрестя/широкі; міст над рельєфом |
| Черга (queue line) | terrain | довжина | окремий тип доріжки від входу атракціону; гості стоять в ній у порядку приходу |
| Додатки доріжки (лава, урна, ліхтар) | object | — | лава — відпочинок, урна — менше сміття (?) |
| Вхід/вихід атракціону | gate | — | ставиться біля станції; вхід — кінець черги, вихід — на доріжку |
| Станція | object | довжина | початок/кінець колії, посадка |
| Шматок колії | tile | напрям, нахил (пологий/крутий), поворот, банк, елемент (петля, штопор…) | приєднується до кінця попереднього; висота наростає |
| Атракціон пласкі (карусель, гойдалка…) | object | розмір N×N, ціна квитка | готові обʼєкти фіксованого розміру |
| Ларьок / туалет / інфо-кіоск | object | товар, ціна | задовольняє потребу гостя |
| Гість (peep) | neutral | гроші, щастя, енергія, голод, спрага, туалет, нудота, бажана інтенсивність | шукає ціль (атракціон, ларьок, вихід); стає в чергу; думає; блює; смітить; іде додому |
| Прибиральник (handyman) | ally | зона | підмітає, спорожняє урни, поливає квіти, косить траву |
| Механік | ally | зона | інспектує й лагодить атракціони |
| Охоронець | ally | зона | стримує вандалізм |
| Аніматор (entertainer) | ally | костюм | піднімає настрій поруч, скорочує нудьгу в черзі (?) |
| Сміття / блювота | hazard | — | знижує враження від доріжки; прибирає handyman |
| Декор (дерева, огорожі, тематичні обʼєкти) | static | — | біля станції підвищує Excitement (до 5 тайлів) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(raise|lower, tile_or_corner)` → ЯКЩО `custom: «тайл належить парку»` and `has(park, money)` → ТО `custom: «висота кута ±1 крок»`, `currency(-cost)`; гірський інструмент робить схили замість обривів.
- КОЛИ `input(drag_path, tiles)` → ЯКЩО `free(tile)` and `custom: «право на тайл»` → ТО `place(path)`; сусідні доріжки `custom: «автоматично зʼєднуються»`.
- КОЛИ `input(place, queue, tile)` → ТО `place(queue)`; черга зʼєднується лише з чергою, входом атракціону й однією доріжкою на початку (?).
- КОЛИ `input(add_track_piece)` → ЯКЩО `custom: «шматок продовжує кінець колії без колізії з іншими елементами на цій висоті»` → ТО `place(track_piece)`; інакше `block` з поясненням.
- КОЛИ `custom: «колія замкнута в кільце / має станцію»` → ТО `custom: «можна тестувати»`; КОЛИ `input(test, ride)` → ТО `custom: «потяг проїжджає колію; збираються G-сили, швидкості, спуски, інверсії»`.
- КОЛИ `after(test)` → ТО `set_value(ride.excitement|intensity|nausea, f(G-сили, спуски, інверсії, швидкість, довжина, декор у 5 тайлах від станції, близькість до доріжок/води))`.
- КОЛИ `custom: «бічні G > ≈2,8»` → ТО `custom: «+Intensity, +Nausea»`; ЯКЩО `custom: «бічні G > 3,1»` → ТО `custom: «Excitement ×0,5»`.
- КОЛИ `counter(intensity, >, 10)` → ТО `custom: «Excitement −25 % на кожному порозі 10/11/12/13,2/14,5»`; нижче мінімумів (висота спуску, швидкість, кількість спусків) — усі рейтинги діляться.
- КОЛИ `tick` → ЯКЩО `state(guest, wants_ride)` → ТО `custom: «обрати атракціон за бажаною інтенсивністю й толерантністю до нудоти»` (`+cond:prefers`).
- КОЛИ `tick` → ЯКЩО `state(guest, has_goal)` → ТО `custom: «пошук шляху доріжками: на кожному перехресті оцінка min(dx,dy)/16 + 2·dz; бюджет 15000 кроків, 200 тайлів; без розвороту; черги — лише коли шукає саме чергу»`.
- КОЛИ `tick` → ЯКЩО `not state(guest, has_goal)` → ТО `custom: «блукає доріжками»` (`random-walk`); заблуканий — думка «I'm lost» (?).
- КОЛИ `reach(guest, queue_start)` → ЯКЩО `custom: «черга не задовга для гостя»` (?) → ТО `custom: «стати в кінець черги»` (`+effect:queue_join`).
- КОЛИ `tick` → ЯКЩО `custom: «перед гостем у черзі вільно»` → ТО `move(guest, queue_next)`; на вході — `currency(+ticket)` (?), посадка.
- КОЛИ `custom: «поїздка закінчилась»` → ТО `custom: «гість отримує щастя за Excitement / нудоту за Nausea»`, виходить на вихід.
- КОЛИ `counter(guest.nausea, >=, high)` → ТО `spawn_at(vomit, guest.tile)` (`+effect:vomit`); інші гості, що йдуть повз, — гірше настрій.
- КОЛИ `input(buy, stall)` → ЯКЩО `has(guest, money)` → ТО `currency(+price)`, `custom: «−голод/спрага»`; КОЛИ товар зʼїдено → ТО `spawn_at(litter, tile)` якщо поруч нема урни (?).
- КОЛИ `contact(handyman, litter|vomit)` → ТО `disappear_b`.
- КОЛИ `rng(p)` → ЯКЩО `custom: «атракціон давно не інспектували»` → ТО `set_state(ride, broken_down)`; КОЛИ `contact(mechanic, ride)` → ТО `clear_state(ride, broken_down)`.
- КОЛИ `custom: «гість без грошей / втомлений / нещасний»` → ТО `custom: «іде до виходу парку»`.
- КОЛИ `timer(month)` (`+trigger:month_start`) → ТО `custom: «рейтинг парку = f(щастя гостей, сміття, поламки, кількість атракціонів…)»` (?).
- КОЛИ `custom: «дата цілі сценарію»` → ЯКЩО `all_constraints_met` (напр. N гостей і рейтинг парку ≥ порогу (?)) → ТО `win` → `unlock(next_scenario)`; інакше `lose`.
- Рахунок — кошти, вартість парку, рейтинг.

## Керування і ввід
- Миша: панель інструментів (рельєф, вода, доріжки, атракціони, декор, персонал), drag для рельєфу й доріжок, розмір пензля −/+.
- Конструктор колії: кнопки напряму (прямо/ліво/право, радіус повороту), нахилу (вниз/пологий/рівно/вгору/крутий), банку, спецелементів; кожен клік додає шматок; кнопка видалення останнього.
- Клік по гостю/персоналу/атракціону — вікно з даними; для персоналу — малювання зони патрулювання по тайлах.
- Поворот камери, зум (?), гарячі клавіші вікон (F1 рельєф, F2 вода, F4 доріжки в OpenRCT2).

## Вікна, меню, HUD
- `main-menu` → `level-select` сценаріїв (статус пройдено), Load, вихід.
- `game-screen`: ізометрія, верхня панель інструментів, нижня — гроші, кількість гостей, рейтинг парку, дата, повідомлення-новини.
- `+window:track-designer` — конструктор колії (кнопки шматків, ціна, статус).
- Вікно атракціону (`custom-window`): вкладки — вигляд, режим роботи, обслуговування, кольори, музика, рейтинги (`+ui:ride-stats-graph` — графіки швидкості/висоти/G), клієнти, прибуток.
- Вікно гостя (`custom-window`): потреби-шкали, гроші, `+ui:thought-bubble` (думки «This ride looks too intense»), інвентар, де був.
- `+window:finance-window` — фінанси, позика, маркетинг; `+window:research-window` — фінансування досліджень і категорії.
- `custom-window` парку: рейтинг, гості, ціна входу, мета сценарію (`objective-text`); `stats-window` (?).
- `map-window` / `minimap` (?) парку; `confirm-dialog` при знесенні.

## Фічі поза полем
- `levels-sequential` + `level-unlock` (21 сценарій, + по 30 у доповненнях — 81); Mega Park — майже пісочниця з позикою $50 000.
- `save-slots`, `pause`, `+feature:track-design-save` (збереження й повторна установка дизайну колії) (?).
- Доповнення: Added Attractions (Corkscrew Follies), Loopy Landscapes; RCT Classic (2017); OpenRCT2 — відкрита реімплементація з `speed-control`, мультиплеєром, редактором.

## Варіації й родичі
- RCT2/3, Parkitect (службові доріжки, видимість зі шляху), Planet Coaster, Theme Park (Bullfrog, 1994) — попередник.
- У корпусі: `populous` (рельєф у вершинах сітки), `openttd-rails` (колія по тайлах з висотою), `theme-hospital` (кімнати й черги до них), `caesar-3` (агенти-шукачі по графу доріг), `mini-motorways` (дороги-граф).
- **Осі варіацій «рельєф»**: висота тайла / висота вершини (кутів) / воксель · **«колія»**: шматки зі слотами напряму й нахилу / вільна сплайн-крива (Planet Coaster) · **«гість»**: випадкове блукання / цільовий пошук з бюджетом / мапа парку дає знання цілей.

## Цікавинки для курсу
- Тайл з висотами 4 кутів: схил/обрив/сідло, «гірський» інструмент — 🥉.
- Доріжки з автозʼєднанням (маска 4 сусідів → спрайт) — 🌱.
- Черга як FIFO на ланцюжку тайлів від входу атракціону — 📎.
- Конструктор колії: шматок з вхідним і вихідним станом (напрям, нахил, банк), перевірка колізій по висоті — 🥈.
- Рейтинг атракціону з геометрії: G-сили, спуски, інверсії, пороги-штрафи — 🥈 (симуляція потяга).
- Гість з потребами й вибором атракціону за бажаною інтенсивністю — 📎.
- Пошук шляху з бюджетом кроків і перехресть, евристика відстані — 🥇 (обмежений A*/DFS з відомими артефактами).

## Мапа на каталог
- Є: `height-levels` (тайли з висотою; кути — глибше) · `multi-cell-size` (атракціони N×N) · `impassable-cells` · `cell-click` + `drag-drop-piece` + `hover-highlight` · `chase-bfs` (пошук шляху гостя) · `random-walk` (блукання) · `round-currency` · `game-pause` · `save-game` + `save-multi-slot` · `objective-text` + `status-panel` · `sequential-levels` + `level-unlock` · `minimap-radar` (?) · `game-loop`.
- **Нема** → пропозиції карток:
  - `+corner-heights` «Висота в кутах тайла: схили й обриви» · entities/legality · 🥉 (Populous, OpenTTD — родичі).
  - `+queue-line` «Черга-доріжка FIFO до обʼєкта» · entities/move · 📎 · слоти {capacity, join_rule}.
  - `+track-builder` «Колія зі шматків зі станом кінця» · entities/legality · 🥈.
  - `+ride-ratings` «Рейтинг споруди з її геометрії й оточення» · game-logic/score · 🥈.
  - `+agent-needs` «Агенти з потребами обирають ціль» · entities/state · 📎.
  - `+land-rights` «Тайли: власні / право будови / чужі» · entities/legality · 🌱.
  - `+breakdown-repair` «Поломка за ймовірністю, лагодить агент» · entities/state · 📎.
  - `+pathfind-budget` «Пошук шляху з бюджетом кроків» · entities/move · 🥇.
  - `+litter-cleanup` «Сміття від агентів, прибиральники» · entities/spawn · 📎.
  - `+drag-build-line`, `+entity-rotate`, `+town-builder` — уже пропоновані іншими.

## Пропозиції до словників
- `+card:corner-heights`, `+card:queue-line`, `+card:track-builder`, `+card:ride-ratings`, `+card:agent-needs`, `+card:land-rights`, `+card:breakdown-repair`, `+card:pathfind-budget` — див. вище.
- `+trigger:month_start` — календарний тік (Caesar III, Pharaoh, RCT).
- `+cond:prefers` — агент обирає ціль, якщо її параметр у його діапазоні (інтенсивність атракціону).
- `+effect:queue_join` — стати в кінець черги; `+effect:vomit` — агент лишає забруднення на тайлі (взагалі «лишити слід»).
- `+role:visitor` — автономний клієнт з потребами й грошима (гість парку, пацієнт).
- `+ui:thought-bubble` — думка агента текстом; `+ui:ride-stats-graph` — графік вимірів атракціону.
- `+window:track-designer`, `+window:research-window`, `+window:finance-window`.
- `+feature:track-design-save` — збереження власних дизайнів для повторного використання.

## Джерела
- ⭐ [Wikipedia: RollerCoaster Tycoon](https://en.wikipedia.org/wiki/RollerCoaster_Tycoon_(video_game)) — тайли, рельєф і вода, колія зі шматків (напрям, висота, крутизна), персонал і їхні задачі, 21/81 сценарій, Mega Park, Chris Sawyer, асемблер.
- [OpenRCT2 docs: Landscaping](https://docs.openrct2.io/en/latest/playing/landscaping/index.html) — висота кутів, гірський інструмент, вода з підпірними стінками, власність і права на будову.
- [OpenRCT2 docs: Footpaths](https://docs.openrct2.io/en/latest/playing/footpath/index.html) — доріжки й черги, автозʼєднання, мости.
- [OpenRCT2 wiki: Peep AI](https://github.com/OpenRCT2/OpenRCT2/wiki/Peep-AI) — бюджет 15000/50000 кроків, 200 тайлів, оцінка відстані, без розвороту, черги відкидаються.
- [OpenRCT2 wiki: Ride rating calculation](https://github.com/OpenRCT2/OpenRCT2/wiki/Ride-rating-calculation) — внески G-сил, спусків, інверсій, декору в 5 тайлах, пороги інтенсивності.
- [OpenRCT2 wiki: Sizes and angles](https://github.com/OpenRCT2/OpenRCT2/wiki/Sizes-and-angles-in-the-game-world) — кути пологого (≈22°) і крутого (≈58,5°) схилу колії.

## Непевне
- (?) Правило вступу в чергу (довжина черги vs терпіння гостя) і чи гості покидають чергу — fandom дав 402, джерела не відкрито.
- (?) Цілі сценаріїв (N гостей + рейтинг до дати), шкала рейтингу парку і закриття парку при низькому рейтингу — з памʼяті.
- (?) Сезон березень–жовтень, ціна входу vs ціна атракціонів у RCT1 — з памʼяті.
- (?) Урни й сміття, аніматори в черзі, думка «I'm lost», збереження дизайнів колії — з памʼяті.
- (?) Мінімапа/мапа парку і зум у RCT1 — не перевірено.
