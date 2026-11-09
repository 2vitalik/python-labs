---
title: Feed All Monsters
slug: feed-all-monsters
aka: []
family: connect-rotate
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2023
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1597720/Feed_All_Monsters/", best: true, note: "сторінка Steam: «лінійний пазл» — провести лінію поруч кожного монстра; 200 рівнів; лише миша (ліва/права кнопки, drag-and-drop); трейлер"}
  - {kind: other, url: "https://indiegameculture.com/news/feed-all-monsters-review/", note: "огляд: працівники 7/1 · 5/2 · 2/3 (кроки/їжа), старт лише з точок, лінії не перекриваються, бруд, пліснява, боси, клік або клавіатура"}
  - {kind: other, url: "https://leopard-chicory-2eaa.squarespace.com/missgamernerd-plays/feed-all-monsters-review", note: "огляд: імена працівників, павер-апи Speed Carrot / Power Onigiri / Throwing Pan, підказки-старти, 6 островів, боси"}
  - {kind: other, url: "https://www.wasdland.com/game/feed-all-monsters-1597720", note: "агрегатор відгуків: портали, потоки, фото монстрів"}
  - {kind: other, url: "https://steamcommunity.com/stats/1597720/achievements", note: "20 досягнень: острови, фотоальбом, 1000 клітин, вимикач музики, автобус з їжею"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Feed+All+Monsters+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [path-drawing, cell-click, keyboard-controls, item-pickup, teleport, satisfy-constraints, completion-detection, world-map, level-unlock, sequential-levels, level-select, codex-window, music-toggle, language-picker, save-progress, game-screen, +adjacent-transfer, +track-budget, +variable-player-powers, +terrain-move-cost, +throw-item, +boss-fight, +hint-reveal, +resource-drain-cell, +forced-move-stream, +no-crossing-lines]
proposes: ["+role:terminal", "+effect:extend_path", "+ui:path-budget-label", "+feature:earned-hints", "+card:path-budget-per-actor"]
author: opus
date: 2026-11-09
---

# Feed All Monsters — проведи трьох кур'єрів так, щоб їхні лінії пройшли поруч кожного голодного монстра

## Суть
Лінійний пазл про службу доставки їжі: на сітці острова стоять монстри, яким потрібна певна кількість порцій, і кілька стартових точок. Гравець малює для кожного з трьох працівників лінію від стартової точки; монстр отримує їжу, коли лінія проходить **поруч** із ним, а не крізь нього. Ядро — розподіл ресурсів: працівники відрізняються довжиною ходу і порцією (довгий хід + мала порція проти короткого ходу + великої порції), лінії не можна перекривати, а місцевість змінює ціну кроку чи запас їжі. Таймера й помилок нема.

## Поле і час
- Квадратна сітка «плавучого острова»; весь рівень видно одразу, камера статична (?).
- Шари: місцевість (трава, бруд, пліснява, потік, портал) + монстри + стартові точки + павер-апи + лінії працівників.
- Час статичний: лінії малюються й перемальовуються без обмежень, симуляції нема (`time: static`).
- Боси: рівень з одним великим монстром, якому треба якомога довша лінія (наприкінці кожного острова).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Melonica | player | 7 кроків · порція 1 | довга лінія, годує по 1 |
| Mun-Chi | player | 5 кроків · порція 2 | середина |
| Umarius | player | 2 кроки · порція 3 | коротка лінія, годує по 3 |
| Стартова точка | terminal (custom) | — | лінія працівника починається лише тут |
| Лінія працівника | mark | довжина ≤ кроки | не перекривається з іншими лініями |
| Монстр | neutral | потреба N порцій | стоїть на місці; ситий, коли отримав N |
| Бос | boss | великий; потреба — довжина лінії (?) | один на рівні, закриває острів |
| Бруд | terrain | +1 крок | прохід коштує додатковий крок |
| Пліснява | hazard | −1 їжа | прохід забирає одну порцію |
| Портал | terrain | пара | переносить лінію в іншу точку |
| Потік | terrain | напрямок | змушує рух у певному напрямку (?) |
| Speed Carrot | pickup | +1 крок | подовжує лінію працівника |
| Power Onigiri | pickup | +2 їжі | збільшує запас/порцію |
| Throwing Pan | pickup | 1 їжа по прямій | дозволяє нагодувати монстра на відстані |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, worker)` або клавіша → ТО `custom: «обрати активного працівника»`.
- КОЛИ `input(drag, start_point)` → ЯКЩО `cell(start_point, start)` and `free(start_point)` → ТО `custom: «почати лінію активного працівника з цієї точки»`; інакше `block`.
- КОЛИ `input(drag, cell)` → ЯКЩО `free(cell)` and `counter(steps_left, >, 0)` and not `occupied(cell, other_path)` → ТО `custom: «подовжити лінію працівника на клітину»`, `counter(steps_left, -1)`; інакше `block`.
- КОЛИ `enter(path, mud)` → ТО `counter(steps_left, -1)` (додатковий крок).
- КОЛИ `enter(path, mold)` → ТО `take(worker, food)` (−1 порція).
- КОЛИ `enter(path, portal)` → ТО `teleport(path_end, pair)` (?).
- КОЛИ `enter(path, stream)` → ТО `custom: «лінію зносить у напрямку течії»` (?).
- КОЛИ `enter(path, speed_carrot)` → ТО `pickup(worker, carrot)`, `counter(steps_left, +1)`.
- КОЛИ `enter(path, power_onigiri)` → ТО `pickup(worker, onigiri)`, `counter(food, +2)`.
- КОЛИ `enter(path, throwing_pan)` → ТО `pickup(worker, pan)`; далі `throw(food, dir)` — перший монстр на прямій отримує 1 порцію (?).
- КОЛИ `adjacent(path_cell, monster)` → ЯКЩО `counter(need[monster], >, 0)` → ТО `counter(need[monster], -portion)`, `sound`.
- КОЛИ `counter(need[monster], <=, 0)` → ТО `set_state(monster, fed)`.
- КОЛИ `input(right_click, path)` → ТО `custom: «стерти лінію працівника»` (?).
- КОЛИ `input(tip)` → ЯКЩО `counter(tips, >, 0)` → ТО `custom: «поставити одного працівника на правильну стартову точку»`, `counter(tips, -1)`.
- КОЛИ `all_constraints_met` (усі монстри ситі) → ТО `win`, `counter(tips, +1)` (?), `next_level`.
- КОЛИ `custom: «монстра нагодовано вперше»` → ТО `unlock(photo)` (?).
- Перемога: усі монстри (або бос) нагодовані. · Поразка: нема — ні таймера, ні помилок. · Рахунок: нема; лічильники досягнень — порції, пройдені клітини.

## Керування і ввід
- Лише миша: лівий клік — обрати працівника, drag — тягнути лінію від стартової точки; правий клік — скасування/стирання (?).
- Працівника можна обрати й клавіатурою; контролер не підтримується (за оглядом).
- Під час drag біля лінії видно, скільки їжі вона дає і скільки кроків лишилось.
- Steam: позначки «Touch Only Option» і «Mouse Only Option».

## Вікна, меню, HUD
- `main-menu` (?) → `map-window`: острови сполучені маршрутом «автобуса з їжею»; рівні — вузли на мапі, пройдені можна перегравати.
- `game-screen`: сітка острова; портрети трьох працівників з кроками/порцією; HUD — `path-preview` (лінія під курсором), `path-budget-label` (їжа і кроки біля лінії), `remaining-counter` (потреба монстра) (?).
- `codex-window` (фотоальбом): фото нагодованих монстрів; досягнення за 5…35 фото й «усі фото».
- `settings-window`: гучність, музика вкл/викл, мова (11 мов).
- `credits-window` — титри (є досягнення за перегляд).
- Переходи: map-window → game-screen → (усі ситі) наступний вузол мапи; після боса — переїзд на наступний острів.

## Фічі поза полем
- `levels-sequential` + `level-unlock` + `world-map`: 200 рівнів на 6 островах — Grasslands, Dark Forest, Ruins, Oasis, Autumn Fields, Snowy Mountains; кожен острів додає свою механіку, монстрів, музику й боса.
- `hint` з токенами: підказка ставить одного працівника на правильний старт; токени заробляються проходженням рівнів.
- `collectibles`: фото монстрів (альбом); `achievements` Steam; `cloud-save`; `localization` 11 мов.
- Нема undo як окремої кнопки (?) — лінію просто перемальовують; нема таймера, помилок, редактора.

## Варіації й родичі
- [Cosmic Express](cosmic-express.md) — те саме «спрацьовує сусідство з лінією», але потяг один і пасажири мають місця; [Flow Free](flow-free.md) і [LYNE](lyne.md) — малювання ліній від термінала без перетинів; [Trainyard](trainyard.md) — кольорові джерела/цілі.
- Осі варіацій:
  - **як лінія діє на ціль**: проходить крізь (Flow Free) / поруч (Feed All Monsters, Cosmic Express) / по прямій кидком (сковорідка);
  - **бюджет лінії**: нема / спільний ліміт колій (Railbound) / власний для кожного актора;
  - **актори**: один / кілька з різними параметрами (тут — компроміс дальність ↔ порція);
  - **місцевість**: нейтральна / дорожча (бруд) / забирає ресурс (пліснява) / переносить (портал, потік).

## Цікавинки для курсу
- Лінія з бюджетом кроків і цінами клітин (бруд = 2) — 🌱.
- Годування за сусідством: після кожного кроку перевірити 4 сусідів і зменшити потребу на порцію — 📎 (слот: 4/8-сусідство, повторне годування тим самим працівником).
- Три актори з різними (кроки, порція) — перевірка всього рівня як обмеження — 📎.
- Сковорідка: промінь по прямій до першого монстра — 🌱.
- Розвʼязувач: перебір стартових точок × шляхів з бюджетом (DFS з відсіканням) — 🥇.
- Підказка «правильний старт одного працівника» з токенами за проходження — 📎 (потрібен збережений розвʼязок).

## Мапа на каталог
- Є: `path-drawing` ↔ лінії drag-ом; `cell-click` + `keyboard-controls` ↔ вибір працівника; `item-pickup` ↔ павер-апи; `teleport` ↔ портали; `satisfy-constraints` + `completion-detection` ↔ усі ситі; `world-map` + `level-unlock` + `sequential-levels` + `level-select` ↔ острови й вузли; `codex-window` ↔ фотоальбом; `music-toggle`, `language-picker`, `save-progress`, `game-screen`.
- **Нема** → пропозиції карток:
  - `+adjacent-transfer` (з Cosmic Express) — передача «поруч із лінією»; слот {amount: порція актора}.
  - `+track-budget` (з Railbound) · `+path-budget-per-actor` «Бюджет лінії в кожного актора свій» · game-logic · 📎.
  - `+variable-player-powers` — актори з різними параметрами.
  - `+terrain-move-cost` — бруд; `+resource-drain-cell` «Клітина забирає ресурс при проході» · entities/interact · 🌱.
  - `+forced-move-stream` «Потік змушує напрямок» · entities/move · 🌱 (?).
  - `+throw-item` — сковорідка; `+boss-fight` — великий монстр; `+hint-reveal` — підказка-старт; `+no-crossing-lines` — лінії не перекриваються.

## Пропозиції до словників
- `+role:terminal` — стартова точка лінії.
- `+effect:extend_path` — подовжити лінію на клітину (Flow Free, LYNE, Cosmic Express).
- `+ui:path-budget-label` — біля лінії під курсором: скільки їжі дасть і скільки кроків лишилось.
- `+feature:earned-hints` — токени підказок заробляються проходженням рівнів.
- `+card:path-budget-per-actor` — окремий бюджет лінії в кожного з кількох акторів.

## Джерела
- ⭐ [Steam: Feed All Monsters](https://store.steampowered.com/app/1597720/Feed_All_Monsters/) — суть «лінія поруч кожного монстра», три працівники, 200 рівнів, лише миша, DU&I, 22.06.2023.
- [Indie Game Culture: огляд](https://indiegameculture.com/news/feed-all-monsters-review/) — 7/1 · 5/2 · 2/3, старт лише з точок, лінії не перекриваються, різна потреба монстрів, бруд, пліснява, боси, клік/клавіатура, підпис лінії.
- [MissGamerNerd: огляд](https://leopard-chicory-2eaa.squarespace.com/missgamernerd-plays/feed-all-monsters-review) — імена працівників, павер-апи, підказки-старти, 6 зон, боси, «no timers and no mistakes».
- [WASDLand](https://www.wasdland.com/game/feed-all-monsters-1597720) — відгуки: портали, потоки, сковорідка, фото монстрів.
- [Steam: досягнення](https://steamcommunity.com/stats/1597720/achievements) — острови, фото, 1000 клітин, вимикач музики, титри, автобус.
- YouTube: пошук «Feed All Monsters gameplay».

## Непевне
- (?) Сусідство для годування — 4 чи 8 сусідів, і чи годує той самий працівник монстра двічі, якщо пройде поруч знову; пошуковий підсумок казав «orthogonally», сторінки — ні.
- (?) «Порція» — це скільки отримує кожен монстр, чи загальний запас працівника; огляди формулюють по-різному.
- (?) Точна дія потоку й порталу, роль правого кліку, наявність undo — з відгуків гравців, не перевірено.
- (?) Як заробляються токени підказок і як відкриваються фото — «за проходження рівнів» без деталей.
- (?) Бос: «максимізувати довжину лінії» — одне речення огляду.
