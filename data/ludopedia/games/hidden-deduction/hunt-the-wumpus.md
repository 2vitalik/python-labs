---
title: Hunt the Wumpus («Полювання на Вампуса»)
slug: hunt-the-wumpus
family: hidden-deduction
also: [roguelike]
klass: avatar
axes:
  field: graph
  time: turn
  opponent: none
  info: hidden
  random: both
  goal: state
year: 1973
platforms: [mainframe/мінікомпʼютер BASIC (People's Computer Company), C (Ken Thompson, 1974), TI-99/4A (1981), HP-41C (1981), web, console]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hunt_the_Wumpus", best: true, note: "правила, додекаедр, кривуляста стріла, історія і версії"}
  - {kind: other, url: "https://gitlab.com/esr/wumpus/-/raw/master/wumpus.c", note: "Eric S. Raymond: дослівний переклад оригінального BASIC на C — тексти, P=0.75, таблиця тунелів"}
  - {kind: other, url: "https://archive.org/details/Hunt_the_Wumpus_1977_Creative_Computing", note: "Creative Computing 1977: стаття й лістинг Gregory Yob"}
  - {kind: other, url: "https://archive.org/details/Hunt_the_Wumpus_II_1977_Creative_Computing", note: "Wumpus 2: інші мапи печер"}
  - {kind: other, url: "https://archive.org/details/WUMPUS3", note: "Wumpus 3 / Super Wumpus (PCC)"}
  - {kind: other, url: "https://archive.org/details/hunt-the-wumpus-1980", note: "мануал графічної TI-99/4A версії"}
  - {kind: other, url: "https://rosettacode.org/wiki/Hunt_the_Wumpus", note: "задача-реалізація десятками мов (спрощені правила)"}
  - {kind: other, url: "https://www.eecs.wsu.edu/~holder/courses/AI/wumpus/", note: "Wumpus World Simulator — версія з підручника AI (сітка 4×4)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hunt+the+wumpus+1973+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [projectile-shot, touch-death, environment-death, teleport-random-exit, random-walk, player-death, console-render, help-window, confirm-dialog, end-screen, game-screen, minimap-radar, state-as-data, +graph-field, +adjacent-hazard-sense, +crooked-arrow-path, +wake-on-noise, +ammo-limit, +same-setup-replay, +hazard-notes-map]
proposes: ["+cond:adjacent_kind", "+effect:trace_path", "+ui:sense-messages", "+ui:exits-list", "+ui:hazard-notes", "+window:text-prompt", "+feature:same-setup", "+axis:info-asymmetry", "+card:graph-field", "+card:adjacent-hazard-sense", "+card:crooked-arrow-path", "+card:wake-on-noise", "+card:ammo-limit", "+card:same-setup-replay", "+card:hazard-notes-map"]
author: opus
date: 2026-11-02
---

# Hunt the Wumpus — темна печера-додекаедр: за запахом, протягом і шурхотом вирахуй Вампуса й постріль кривулястою стрілою

## Суть
Гравець блукає 20 кімнатами печери, кожна зʼєднана тунелями з трьома іншими; нічого не видно, є лише відчуття з **сусідніх** кімнат: запах (Вампус), протяг (бездонна яма), шурхіт (суперкажани). Хід — перейти в сусідню кімнату або випустити «кривулясту» стрілу маршрутом до 5 кімнат. Влучив у Вампуса — перемога; ступив у яму, наскочив на Вампуса, що не втік, або поцілив стрілою в себе — поразка. Gregory Yob (1973) зробив її навмисно **не на сітці**, бо його дратували 10×10-ігри Hurkle і Mugwump, — перша гра-дедукція на прихованому графі.

## Поле і час
- Поле — граф: 20 вершин додекаедра, у кожної рівно 3 ребра; номери кімнат і зʼєднання фіксовані (таблиця DATA в коді). Wumpus 2 — інші топології.
- Шари вершини: гравець · Вампус · яма ×2 · кажани ×2 (усі 6 — у різних кімнатах на старті; гравець ніколи не стартує на небезпеці).
- Видимість: лише номер своєї кімнати, номери трьох сусідніх і відчуття; мапу гравець малює сам на папері.
- Покроково: хід = рух або постріл; Вампус спить і рухається лише коли його потривожити (промах або вхід у його кімнату).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | 5 стріл | хід у сусідню кімнату або постріл |
| Кімната ×20 | zone | номер, 3 тунелі | вузол графа; несе максимум одну небезпеку на старті |
| Тунель | static | ребро графа | рух і політ стріли лише по ребрах |
| Вампус | enemy | стан sleep/awake | спить; потривожений — з P=0.75 іде в сусідню кімнату, з 0.25 лишається; ями й кажани на нього не діють |
| Бездонна яма ×2 | hazard | — | гравець увійшов — смерть |
| Суперкажани ×2 | hazard | — | гравець увійшов — переносять у випадкову з 20 кімнат (будь-яку, включно з ямою чи Вампусом) |
| Кривуляста стріла | projectile | маршрут 1–5 кімнат | летить по списку кімнат; неможливий крок — випадковий тунель; ями/кажани не зупиняють |
| Відчуття | mark | запах / протяг / шурхіт | повідомлення на вході: небезпека в сусідній кімнаті (не яка саме з трьох) |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт: `spawn_at` 6 сутностей у різні випадкові кімнати (збіг → повторний розклад); стріл 5.
- КОЛИ `turn_start` → ТО `message(«YOU ARE IN ROOM n» / «TUNNELS LEAD TO a b c»)` і для кожного виду ЯКЩО `adjacent_kind(room, wumpus|pit|bats)` → `message(«I SMELL A WUMPUS!» | «I FEEL A DRAFT» | «BATS NEARBY!»)`.
- КОЛИ `input(move, r)` → ЯКЩО r сусідня (або та сама) → ТО `move(player, r)`; інакше `message(«NOT POSSIBLE»)`, повтор вводу.
- КОЛИ `enter(player, room_with_wumpus)` → ТО `message(«...OOPS! BUMPED A WUMPUS!»)`, `set_state(wumpus, awake)`: з P=0.75 `move(wumpus, random_neighbor)`; ЯКЩО Вампус лишився в кімнаті гравця → `lose` («TSK TSK TSK - WUMPUS GOT YOU!»).
- КОЛИ `enter(player, pit)` → ТО `lose` («YYYYIIIIEEEE . . . FELL IN PIT»).
- КОЛИ `enter(player, bats)` → ТО `teleport(player, random_room)` («ZAP--SUPER BAT SNATCH! ELSEWHEREVILLE FOR YOU!»), після чого всі перевірки входу — знову (можна впасти в яму чи на Вампуса, або знову до кажанів).
- Порядок перевірок на вході: Вампус → яма → кажани.
- КОЛИ `input(shoot, n, [r1..rn])` (n ≤ 5) → ЯКЩО r_k == r_{k-2} → ТО `message(«ARROWS AREN'T THAT CROOKED - TRY ANOTHER ROOM»)`, повтор вводу.
- Політ: для кожного r_k → ЯКЩО r_k сусідня до поточної кімнати стріли → `move(arrow, r_k)`; інакше `move(arrow, random_neighbor)` — `trace_path` далі від нової точки.
- КОЛИ стріла входить у кімнату Вампуса → ТО `win` («AHA! YOU GOT THE WUMPUS!»); КОЛИ в кімнату гравця → ТО `lose` («OUCH! ARROW GOT YOU!»).
- КОЛИ стріла пролетіла без влучання → ТО `message(«MISSED»)`, `counter(arrows, -1)`, Вампус прокидається (P=0.75 — крок у сусідню); ЯКЩО він опинився в кімнаті гравця → `lose`.
- КОЛИ `counter(arrows, ==, 0)` → ТО `lose`.
- Після кінця: `confirm-dialog` «SAME SETUP (Y-N)» — так: той самий розклад 6 сутностей і 5 стріл (рухи Вампуса й кажанів — уже інші випадкові); ні — новий.
- Перемога: влучити стрілою у Вампуса · Поразка: яма, Вампус у твоїй кімнаті, власна стріла, 0 стріл · Рахунку нема.

## Керування і ввід
- Текстовий діалог: «SHOOT OR MOVE (S-M)» → для M «WHERE TO» + номер кімнати; для S «NO. OF ROOMS (1-5)» → «ROOM #» n разів.
- На старті «INSTRUCTIONS (Y-N)» — текст правил у консолі.
- Жодного курсора: гравець мислить номерами вершин і веде власну мапу. Графічні версії (TI-99/4A) дають клік/джойстик по мапі (?).

## Вікна, меню, HUD
- `help-window` — текст інструкцій за запитом на старті.
- `game-screen` = `text-prompt`: рядки «YOU ARE IN ROOM n», «TUNNELS LEAD TO a b c», `sense-messages` (запах/протяг/шурхіт), запит дії. Лічильник стріл не показується постійно (?).
- `end-screen`: «HA HA HA - YOU LOSE!» / «HEE HEE HEE - THE WUMPUS'LL GET YOU NEXT TIME!!» (в оригіналі друкується і після перемоги — особливість коду).
- `confirm-dialog`: «SAME SETUP (Y-N)».
- Цифрова версія (сучасна): `map-window` — граф печери з відкритими кімнатами, ребрами і позначками гравця (`hazard-notes`: «тут протяг», «Вампуса тут нема»), `exits-list` кнопками, лічильник стріл, журнал відчуттів (`message-log`).
- Переходи: help? → game-screen ⇄ (shoot-маршрут) → end-screen → same setup? → game-screen.

## Фічі поза полем
- `same-setup` — повторити ту саму печеру (аналог `seed-input`, але лише стартового розкладу, а не всього RNG); `-s N` у версії ESR — явний seed.
- `rules-page` (INSTRUCTIONS), жодних рівнів, рахунку, збережень.
- Wumpus 2: вибір топології печери; Wumpus 3 (Super Wumpus): нові небезпеки (?).
- Wumpus World (підручник AI): поле 4×4, сприйняття Stench/Breeze/Glitter/Bump/Scream, одна стріла по прямій, золото — класичне завдання для агента з логічним виведенням (?).

## Варіації й родичі
- Hurkle (підказка — напрямок), Mugwump (підказка — відстань), Snark — пошук прихованого на сітці 10×10 (від них Yob відштовхнувся).
- Wumpus 2 (інші графи: стрічка Мебіуса, тор, «шари» (?)), Super Wumpus, Wumpus World (сітка замість графа, одна стріла, золото), Rogue і роглайки (темне підземелля, прихована мапа).
- Minesweeper — ті самі «відчуття сусідів», але точне число замість так/ні.
- **Осі варіацій**: поле «додекаедр / інші графи / сітка 4×4»; підказка «так/ні по виду (Wumpus) / число (Minesweeper) / напрямок (Hurkle) / відстань (Mugwump)»; стріла «маршрут до 5 кімнат / по прямій / одна»; ворог «спить і прокидається від шуму / стоїть / ходить».

## Цікавинки для курсу
- Поле як граф (список суміжності, фіксований додекаедр або згенерований 3-регулярний граф) замість сітки — 📎; генерація звʼязного 3-регулярного графа — 🥈.
- Відчуття сусідів «так/ні за видом» + мапа-нотатки гравця — 📎.
- Кривуляста стріла: маршрут із валідацією «не туди-назад», випадковий тунель на неможливому кроці, самоураження — 🥉.
- Вампус, що прокидається від шуму (P=0.75) — 🌱; кажани з повторною перевіркою входу (каскад подій) — 📎.
- «Same setup» — відтворюваний стартовий стан без відтворюваних подій: чудовий привід поговорити про seed і RNG — 🌱.
- AI-агент Wumpus World з логічним виведенням (безпечні кімнати з відчуттів) — 🥇.
- Консольний інтерфейс як повноцінне `game-screen` — гра без графіки, вся інформація в тексті — 🌱.

## Мапа на каталог
- Є: `projectile-shot` (стріла) · `touch-death` (Вампус) · `environment-death` (яма) · `teleport-random-exit` (кажани) · `random-walk` (Вампус прокинувся) · `player-death` · `console-render` · `help-window` · `confirm-dialog` (same setup) · `end-screen` / `game-screen` · `minimap-radar` (мапа в цифровій версії) · `state-as-data` (розклад для same setup).
- **Нема** → пропозиції карток:
  - `+graph-field` «Поле-граф (вузли і ребра)» · interface/render або levels/format · 📎 · слот {topology: dodecahedron|random3|custom}.
  - `+adjacent-hazard-sense` «Відчуття небезпеки в сусідніх вузлах» · entities/interact · 📎.
  - `+crooked-arrow-path` «Снаряд за маршрутом із кількох вузлів» · entities/combat · 🥉 · слот {max_hops: 5}.
  - `+wake-on-noise` «Ворог прокидається від шуму» · entities/move · 🌱 · слот {p_move: 0.75}.
  - `+ammo-limit` «Обмежені постріли, 0 = поразка» · entities/state · 🌱 · слот {ammo: 5}.
  - `+same-setup-replay` «Повторити ту саму розстановку» · game-logic/save · 🌱.
  - `+hazard-notes-map` «Мапа з позначками гравця» · interface/hud · 📎.

## Пропозиції до словників
- `+cond:adjacent_kind(cell, kind)` — серед сусідів є сутність виду (булевий варіант `adjacent_count ≥ 1`; підказка без числа).
- `+effect:trace_path(projectile, list)` — політ за маршрутом із кількох вузлів (поряд із `+effect:trace_ray` Black Box).
- `+ui:sense-messages` — рядки відчуттів на вході в кімнату; `+ui:exits-list` — список/кнопки сусідніх вузлів; `+ui:hazard-notes` — позначки гравця на мапі.
- `+window:text-prompt` — консольний екран «запит → відповідь» як вікно гри.
- `+feature:same-setup` — повтор стартової розстановки (ширше: `seed-input`).
- Вжито наявні ⏳ без пропозицій: `message` (головний канал інформації), `hazard` (ями, кажани), `map-window`, `message-log`.
- `+axis:info-asymmetry` — див. Geister; тут `player-vs-game`.

## Джерела
- ⭐ [Wikipedia: Hunt the Wumpus](https://en.wikipedia.org/wiki/Hunt_the_Wumpus) — 20 печер-додекаедр, ями, суперкажани, 5 кривулястих стріл, правила пострілу, історія (Hurkle/Mugwump), версії.
- [wumpus.c (ESR)](https://gitlab.com/esr/wumpus/-/raw/master/wumpus.c) — точні тексти повідомлень, P=0.75, порядок перевірок, «crooked» правило, same setup, таблиця тунелів.
- [Creative Computing 1977](https://archive.org/details/Hunt_the_Wumpus_1977_Creative_Computing) · [Wumpus 2](https://archive.org/details/Hunt_the_Wumpus_II_1977_Creative_Computing) · [Wumpus 3](https://archive.org/details/WUMPUS3) · [TI-99/4A manual](https://archive.org/details/hunt-the-wumpus-1980) — першоджерела (лінки з Wikipedia, не відкривались).
- [Rosetta Code: Hunt the Wumpus](https://rosettacode.org/wiki/Hunt_the_Wumpus) — спрощена задача (стріла лише в сусідню кімнату), реалізації.
- [Wumpus World Simulator](https://www.eecs.wsu.edu/~holder/courses/AI/wumpus/) — AI-варіант (лінк із Wikipedia, не відкривався).
- YouTube: пошук «hunt the wumpus 1973 gameplay».

## Непевне
- (?) Рік: Wikipedia — 1973; часто пишуть «1972 (написано), 1973 (опубліковано)».
- (?) Wumpus World (4×4, Stench/Breeze/Glitter, одна стріла, золото) — з памʼяті про підручник Russell & Norvig; Wikipedia лише згадує, що підручник використовує версію гри.
- (?) Як виглядала графічна TI-99/4A версія (мапа-сітка, що відкривається) — не перевірено.
- (?) Топології Wumpus 2 і небезпеки Wumpus 3 — Wikipedia лише «different cave arrangements» / «more hazards».
- (?) Чи показував оригінал кількість стріл щоходу — у тексті ESR такого рядка не видно.
- Виправлено 2026-11-19 (T364, знахідка хвилі 3): Hurkle дає напрямок, відстань — Mugwump.
