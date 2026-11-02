---
title: Hitman GO (+ Lara Croft GO)
slug: hitman-go
family: push-slide
also: [tactics, thinky]
klass: avatar
axes:
  field: graph
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2014
platforms: [iOS, Android, Windows Phone, PC (Steam, Definitive Edition 2016), PS4, PS Vita, VR]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hitman_Go", best: true, note: "вузли й лінії, вороги ходять разом після гравця, кольори = патерни, кидки, перевдягання, рослини, люки, ключі, зброя, бонус-цілі за зірки"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lara_Croft_Go", note: "та сама вузлова схема: змії, ящірки, павуки, валуни, пили, важелі, тріснута підлога, списи"}
  - {kind: wiki, url: "https://ru.wikipedia.org/wiki/Hitman_Go", note: "керування свайпом / drag на ПК, бонус-цілі, вирізана механіка засідки"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Hitman_Go", note: "5 + 2 розділи, кидки змінюють патерни, ключі й замкнені двері"}
  - {kind: steam, url: "https://store.steampowered.com/app/427820/Hitman_GO_Definitive_Edition/", note: "Definitive Edition: «distractions, disguises, hiding spots, sniper rifles»"}
  - {kind: steam, url: "https://store.steampowered.com/app/540840/Lara_Croft_GO/", note: "Lara Croft GO: Steam-версія з безлімітними підказками"}
  - {kind: official, url: "https://hitmango.com/", note: "сайт гри, магазини всіх платформ"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hitman+go+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [swipe-gestures, drag-drop-piece, piece-capture, touch-death, enemy-patrol, pattern-automaton, chase-player, reach-exit, key-and-door, item-pickup, teleport-pair, projectile-shot, telegraphed-intents, level-select, level-unlock, +node-graph-field, +line-of-sight-attack, +noise-lure, +disguise-pass, +hide-spot, +bonus-objectives, +move-limit, +enemy-phase-after-player, +push-pull-pillar, +crumbling-floor]
proposes: ["+trigger:input", "+trigger:turn_end", "+trigger:line_of_sight", "+trigger:adjacent", "+cond:facing", "+cond:state", "+cond:has", "+effect:move", "+effect:face", "+effect:throw", "+effect:set_state", "+effect:pull", "+role:hazard", "+role:gate", "+role:terrain", "+ui:objective-text", "+ui:path-preview", "+window:chapter-select", "+feature:stars-rating", "+feature:par-target", "+feature:hint-purchase", "+card:node-graph-field", "+card:noise-lure"]
author: opus
date: 2026-11-02
---

# Hitman GO — настільна діорама: крок агента по вузлу, потім крок усіх охоронців

## Суть
Рівень — ігрова дошка з **вузлів, зʼєднаних лініями**; Агент 47 ходить по лінії на сусідній вузол, після чого **всі вороги одночасно** роблять свій хід за жорсткими, видимими патернами (колір фігурки = тип поведінки). Стати на вузол ворога ззаду/збоку — прибрати його; опинитись там, куди ворог дивиться/піде, — загинути. Інструменти — кинутий предмет як приманка, перевдягання, укриття в рослинах, люки, ключі, гвинтівка. Ціль рівня — дійти до виходу або прибрати ціль; бонус-зірки — портфель, «без вбивств», «за N ходів». Lara Croft GO переносить ту саму схему на руїни й додає **штовхання/тягнення колон** і тріскучу підлогу — звідси сімʼя `push-slide`.

## Поле і час
- Поле — **граф** (`field: graph`): вузли на квадратній решітці, але суміжність задають намальовані лінії; є ізольовані частини, з'єднані люками (пара вузлів, перехід за один хід). Камера — діорама під кутом, видно все.
- Хід: (1) гравець рухає 47 на сусідній по лінії вузол або застосовує предмет; (2) усі вороги одночасно роблять по одному кроку/повороту; (3) перевірки зіткнень.
- Без вводу світ стоїть (`time: turn`); випадковості нема — кожен рівень детермінований пазл.
- Lara Croft GO: ті самі вузли й лінії, плюс вертикаль (уступи, стіни для лазіння); деякі обʼєкти (пили, валуни) мають власний тік у фазі середовища.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Агент 47 | player | позиція, предмет у руках, маскування | хід по лінії на сусідній вузол; вхід на вузол ворога (не спереду) = вбивство |
| Вузол | terrain | — | позиція; лінії = легальні ходи |
| Вихід | static | — | кінцева ціль більшості рівнів |
| Ціль (target) | enemy | — | ціль «прибрати» в рівнях-замовленнях |
| Охоронець «стоїть» (синій (?)) | enemy | напрямок погляду | нерухомий; якщо 47 на сусідньому вузлі по лінії погляду — іде туди й убиває |
| Патрульний (зелений (?)) | enemy | напрямок | щоходу крок уперед; у кінці лінії розвертається |
| Поворотний (жовтий (?)) | enemy | цикл повороту | на місці змінює напрямок погляду щоходу (?) |
| Собака | enemy | — | помітивши 47, біжить до нього (?) по 2 вузли (?) |
| Снайпер / стрілець | enemy | лінія | убиває 47 на своїй лінії на відстані (?) |
| Портфель | pickup | — | бонус-ціль «забрати портфель» |
| Камінь / пляшка (кидок) | pickup | дальність | кидок на вузол → вороги поруч ідуть на шум |
| Перевдягання | pickup | колір | вороги того ж кольору не реагують на 47 |
| Рослина (укриття) | terrain | — | 47 на цьому вузлі невидимий |
| Люк / трапдор | terrain | пара | перехід між двома вузлами за один хід |
| Ключ і двері | pickup · gate | — | ключ відкриває двері на шляху |
| Снайперська гвинтівка / пістолет | pickup | патрони | постріл по цілі/перешкоді з дистанції |
| Lara: змія | enemy | напрямок | нерухома; атакує, якщо стати на вузол перед нею |
| Lara: ящірка / павук | enemy | патерн | патрулює або переслідує (?) |
| Lara: колона | object | — | штовхається й тягнеться по лінії; блокує ворога/пилу (?) |
| Lara: пила, валун | hazard | траса | рухаються в фазі середовища; валун котиться за Ларою (?) |
| Lara: тріснута плита | terrain | ресурс кроків | тріскається від кожного кроку; обвалюється |
| Lara: важіль, тиск-плита | switch | ціль | зсуває стіни/платформи |
| Lara: спис | pickup | 1 використання | кинути у ворога на відстані |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(edge)` → ЯКЩО `custom: «між вузлами є лінія»` → ТО `move(47, neighbour)`, `counter(turns, +1)`.
- КОЛИ `contact(47, enemy)` → ЯКЩО `not facing(enemy, 47)` → ТО `disappear_b` (вбивство), `counter(kills, +1)`; інакше `lose`.
- КОЛИ `turn_end(player)` → ТО фаза ворогів: усі одночасно виконують `move`/`face` за типом.
- Стоїть: КОЛИ `turn_end(player)` → ЯКЩО `occupied(cell_in_front, 47)` і `not state(47, hidden|disguised_as_my_color)` → ТО `move(enemy, 47)`, `lose`.
- Патрульний: щоходу `move(enemy, forward)`; КОЛИ `blocked(enemy)` (кінець лінії) → ТО `face(enemy, reverse)`.
- Поворотний: щоходу `face(enemy, next_in_cycle)` (?).
- Собака: КОЛИ `in_range(dog, 47, n)` → ТО `custom: «біжить до 47 найкоротшим шляхом»` (?).
- КОЛИ `input(throw, node)` → ЯКЩО `has(47, throwable)` і `in_range(47, node, 1..2)` (?) → ТО `custom: «шум у вузлі»`; вороги в сусідніх вузлах до шуму `custom: «ідуть на шум, змінюючи маршрут»`.
- КОЛИ `contact(47, disguise)` → ТО `set_state(47, disguised, color)`; вороги цього кольору ігнорують 47.
- КОЛИ `enter(47, plant)` → ТО `set_state(47, hidden)`; `leave` → знімається.
- КОЛИ `enter(47, trapdoor)` → ТО `teleport(47, pair)` (за один хід).
- КОЛИ `contact(47, door)` → ЯКЩО `has(47, key)` → ТО `disappear_b`; інакше `block`.
- КОЛИ `input(shoot, target)` → ЯКЩО `has(47, rifle)` і `line_of_sight(47, target)` → ТО `disappear_b`, `take(47, ammo)`.
- КОЛИ `contact(47, exit)` або `died(target)` → ТО `win`; бонус: `has(47, briefcase)` / `counter(kills, ==, 0)` / `counter(turns, <=, N)` / `count(enemies, ==, 0)` — кожна виконана умова → зірка.
- Lara: КОЛИ `contact(lara, pillar)` → ТО `push`; `input(pull)` → `pull(pillar)`; КОЛИ `enter(lara, cracked_tile)` → ТО `counter(tile_hp, -1)`; на нулі — `custom: «плита обвалюється»` (Лара на ній → падає / `lose`).
- Lara: КОЛИ `contact(lara, lever)` → ТО `custom: «зсунути звʼязану стіну/платформу»`.
- Перемога: головна ціль рівня. · Поразка: ворог або небезпека на вузлі 47. · Рахунок: зірки за рівень (зазвичай 3: пройти + 2 бонуси), зірки відкривають наступні коробки-розділи.

## Керування і ввід
- Мобільні: свайп по лінії від фігурки 47 — хід; drag предмета на вузол — кидок/постріл.
- ПК (Definitive): клік-утримання й перетягування фігурки на сусідній вузол (`drag-drop-piece`).
- Undo нема (?); рестарт рівня — кнопкою; підказки — в меню (у мобільній версії за внутрішню валюту/покупку).

## Вікна, меню, HUD
- `splash-screen` → `main-menu`.
- `chapter-select` (custom-window): **коробки настільної гри** — кожна коробка = розділ; закрита, доки не набрано зірок.
- `level-select`: рівні коробки з позначками зірок.
- `game-screen`: діорама; HUD — `objective-text` (головна + бонус-цілі з галочками), `turn-counter` (для «за N ходів»), `restart-button`, `hint-button`, стрілки-напрямки погляду ворогів (`telegraph-marker`), підсвітка шляху патрульних (?).
- `pause-menu`: продовжити, рестарт, вихід до коробки, налаштування.
- `end-screen`: зірки за рівень (які бонуси виконано).
- `hints-window`: покрокова підказка-розвʼязок (мобільна — платна; Lara Croft GO на Steam — безлімітна).
- `shop-window` (мобільна): підказки, розблокування коробок.
- Переходи: main-menu → chapter-select → level-select → game-screen → (вихід/ціль) end-screen → наступний рівень; (загибель) → рестарт рівня.

## Фічі поза полем
- `stars-rating` (зірки за бонус-цілі) + `level-unlock` (зірки → нова коробка); `levels-sequential`.
- `par-target` як бонус-ціль «за N ходів» — не ліміт, а виклик.
- `hint` (платний у мобільній), `restart-level`; Definitive Edition — ПК/консолі; VR-версія.
- Lara Croft GO: колекційні реліквії, наряди (`unlockables`), безлімітні підказки на Steam.
- Серія: Hitman GO (2014) → Lara Croft GO (2015) → Deus Ex GO (2016).

## Варіації й родичі
- Осі варіацій «покрокова стелс-дошка»:
  - **поле**: вузли й лінії (GO) / квадратна сітка (Into the Breach, Hoplite) / гекси;
  - **як ворог убиває**: на вузол перед собою (стоїть) / по лінії на відстань (снайпер) / переслідує (собака);
  - **як гравець убиває**: вхід зі спини/збоку / постріл / кинутий спис;
  - **приховування**: укриття-клітина / перевдягання за кольором / відволікання шумом;
  - **ціль**: вихід / ціль-вбивство / бонуси (портфель, без вбивств, ходи);
  - **середовище** (Lara): колони штовхати й тягти, тріснута підлога як лічильник кроків, важелі.
- Родичі: Adventures of Lolo (ворог убиває по лінії погляду), Theseus and the Minotaur (два ходи ворога на один), Into the Breach (видимі наміри), Hoplite, шахові задачі; Helltaker (зважений бюджет ходів).

## Цікавинки для курсу
- Поле-граф (вузли + ребра) замість сітки + рендер ліній — 📎; уся решта механік працює на «сусідах вузла».
- Двофазний хід «гравець → усі вороги одночасно» з розвʼязанням зіткнень після фази — 🥉.
- Типи ворогів як стан-машини (стоїть / патруль з розворотом / поворот / погоня) — 📎 кожен, 🥉 сімʼя.
- Кидок-приманка: шум у вузлі змінює маршрути сусідніх ворогів — 🥉.
- Перевдягання за кольором і укриття — `set_state` гравця, що вимикає перевірку ворога — 📎.
- Бонус-цілі з зірками (портфель, без вбивств, ≤N ходів) і відкриття розділів за зірками — 📎.
- Розвʼязувач рівня з мінімумом ходів (BFS по стану «позиція 47 + стани всіх ворогів + предмети») — 🥈.

## Мапа на каталог
- Є: `swipe-gestures` + `drag-drop-piece` ↔ свайп / drag на ПК; `piece-capture` ↔ вхід на вузол ворога; `touch-death` ↔ ворог на вузлі 47; `enemy-patrol` ↔ патрульні; `pattern-automaton` ↔ поворотні; `chase-player` ↔ собаки; `reach-exit` ↔ вихід; `key-and-door` + `item-pickup` ↔ ключі, предмети; `teleport-pair` ↔ люки; `projectile-shot` ↔ гвинтівка, спис; `telegraphed-intents` ↔ видимі напрямки ворогів; `level-select` + `level-unlock` ↔ коробки й рівні.
- **Нема** → пропозиції карток:
  - `+node-graph-field` «Поле-граф: вузли й лінії» · interface/render + entities/legality · 📎.
  - `+line-of-sight-attack` (вже пропонована Lolo) — охоронець/снайпер/змія убивають на лінії погляду.
  - `+enemy-phase-after-player` «Усі вороги ходять одночасно після гравця» · game-logic/opponent · 🥉.
  - `+noise-lure` «Приманка шумом» · entities/interact · 🥉 · слот {range}.
  - `+disguise-pass` «Перевдягання: невидимість для свого кольору» · entities/state · 📎.
  - `+hide-spot` «Клітина-укриття» · entities/interact · 🌱.
  - `+bonus-objectives` «Бонус-цілі рівня» · game-logic/win · 📎 · слот {list}.
  - `+move-limit` (XOR, Helltaker) — тут як бонус «≤N ходів»; з Helltaker і XOR — третя гра.
  - `+push-pull-pillar` «Колона: штовхати й тягти» · entities/legality · 📎 — Lara Croft GO; родич `+pull-object` Sokoban.
  - `+crumbling-floor` «Плита, що тріскається від кроків» · entities/state · 📎 · слот {steps}.

## Пропозиції до словників
- `+trigger:input` — свайп по лінії; `+trigger:turn_end` — фаза ворогів; `+trigger:line_of_sight` — снайпер/змія; `+trigger:adjacent` — 47 поруч з охоронцем.
- `+cond:facing` — убиває, лише якщо дивиться на 47; `+cond:state` — перевдягнений/схований; `+cond:has` — ключ, гвинтівка, предмет для кидка.
- `+effect:move`, `+effect:face` (розворот патрульного), `+effect:throw` (кидок предмета), `+effect:set_state` (перевдягання, укриття), `+effect:pull` (колони Лари).
- `+role:hazard` (пили, валуни), `+role:gate` (двері), `+role:terrain` (рослина, люк, тріснута плита).
- `+ui:objective-text` — список цілей рівня з галочками; `+ui:path-preview` — траса патрульного.
- `+window:chapter-select` — коробки-розділи (також Helltaker).
- `+feature:stars-rating`, `+feature:par-target`, `+feature:hint-purchase` — платна підказка-розвʼязок.
- `+card:node-graph-field`, `+card:noise-lure`.

## Джерела
- ⭐ [Wikipedia: Hitman Go](https://en.wikipedia.org/wiki/Hitman_Go) — вузли й лінії, вороги ходять після гравця одночасно, колір = патерн, стоять/повертаються/патрулюють, кидки, перевдягання, рослини, люки, ключі, вогнепальна зброя, бонус-цілі (портфель, без вбивств) → зірки → розділи, коробки в меню.
- [Wikipedia: Lara Croft Go](https://en.wikipedia.org/wiki/Lara_Croft_Go) — змії, ящірки, павуки, валуни, пили, важелі, тріскуча підлога, разові списи; 5 розділів, 40 рівнів, підказки за покупки.
- [Wikipedia RU](https://ru.wikipedia.org/wiki/Hitman_Go) — свайп на мобільних, drag на ПК; вирізана механіка засади.
- [Wikipedia DE](https://de.wikipedia.org/wiki/Hitman_Go) — 5 розділів + 2 пізніше; кидки змінюють патерни.
- [Steam: Hitman GO Definitive Edition](https://store.steampowered.com/app/427820/Hitman_GO_Definitive_Edition/) — «distractions, disguises, hiding spots, sniper rifles», «silently or by force».
- [Steam: Lara Croft GO](https://store.steampowered.com/app/540840/Lara_Croft_GO/) — безлімітні підказки, наряди, реліквії.
- [hitmango.com](https://hitmango.com/) — офіційний сайт, магазини.
- YouTube: пошук «hitman go gameplay».

## Непевне
- (?) Кольори типів ворогів (синій — стоїть, зелений — патруль, жовтий — поворот) — з памʼяті; Wikipedia каже лише «кожен тип має свій колір».
- (?) Собаки й вороги-снайпери: поведінка й наявність у Hitman GO — з постановки куратора й памʼяті; Wikipedia про них мовчить, Fandom-вікі недоступна (402), WebSearch вичерпано.
- (?) Бонус «≤N ходів» і «вбити всіх» як типи бонус-цілей — з памʼяті; Wikipedia підтверджує портфель і «без вбивств».
- (?) Дальність кидка й радіус, на який реагують вороги.
- (?) Lara Croft GO: тягнення колон, поведінка ящірок/павуків/валунів — з памʼяті; Wikipedia лише перелічує.
- (?) Чи є undo — здається, лише рестарт.
