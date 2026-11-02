---
title: Triple Town
slug: triple-town
family: falling-match
also: [build-sim]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: partial
  random: runtime
  goal: score
year: 2010
platforms: [Kindle, Facebook, Google+, iOS, Android, PC (Steam), Mac]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Triple_Town", best: true, note: "правила: 6×6, злиття 3+, ведмеді, ніндзя, надгробки, кристал, бот, склад"}
  - {kind: steam, url: "https://store.steampowered.com/app/209950/Triple_Town/", note: "PC/Mac версія 2012, без мікротранзакцій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=triple+town+gameplay+bears", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [tile-merge, cell-click, spawn-random-cell, random-walk, inventory-limit, round-currency, shop-window, shop-catalog, event-points, score-records, save-autosave, +connected-group-pop, +chain-reaction, +weighted-spawn, +merge-at-placement, +enclosure-capture, +wildcard-tile, +hold-piece, +remover-item, +turn-limit-energy]
proposes: ["+trigger:input", "+trigger:no_moves", "+trigger:pattern", "+cond:adjacent_count", "+cond:free", "+effect:merge", "+effect:transform", "+effect:move", "+effect:hold_swap", "+effect:currency", "+role:tile", "+role:neutral", "+ui:next-tile-preview", "+ui:hold-slot", "+window:shop-window", "+axis:undo"]
author: opus
date: 2026-11-02
---

# Triple Town — постав предмет; три сусідні однакові зливаються в наступний рівень міста

## Суть
Гравець отримує по одному випадковому предмету (здебільшого траву) і ставить його в будь-яку порожню клітину поля 6×6. Коли 3+ однакових предмети стикаються (по сторонах), вони зливаються в один предмет наступного рівня **у клітині, куди поставлено останній**: трава → кущ → дерево → хатина → … → замок. Ведмеді блукають порожніми клітинами й займають місце; замкнений ведмідь стає надгробком, а надгробки теж зливаються. Гра триває, доки є місце; мета — рахунок.

## Поле і час
- Поле 6×6, квадратна сітка, суміжність 4 (по сторонах). Одна клітина в куті (зазвичай верхня ліва) — склад (storehouse), не ігрова.
- Покроково: хід = поставити поточний предмет (або обміняти зі складом). Після ходу ходять ведмеді.
- Поточний предмет відомий, наступний — ні (`info: partial`). Випадкові: що прийде і куди піде ведмідь.
- Поле на старті частково заповнене випадковими предметами (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Трава | tile | рівень 1 | 3 → кущ |
| Кущ | tile | рівень 2 | 3 → дерево |
| Дерево | tile | рівень 3 | 3 → хатина |
| Хатина (hut) | tile | рівень 4 | 3 → будинок |
| Будинок (house) | tile | рівень 5 | 3 → маєток (?) |
| Маєток (mansion) | tile | рівень 6 (?) | 3 → замок |
| Замок | tile | рівень 7 (?) | 3 → літаючий замок (?) |
| Літаючий / потрійний замок | tile | вищі рівні (?) | вершина ланцюга; дає найбільше очок |
| Ведмідь | enemy | — | щоходу йде у випадкову сусідню порожню клітину; займає місце |
| Ніндзя-ведмідь | enemy | — | щоходу стрибає в будь-яку порожню клітину поля |
| Надгробок | tile | зʼявляється з ведмедя | 3 → церква |
| Церква | tile | — | 3 → собор |
| Собор (cathedral) | tile | — | 3 → скриня зі скарбом (?) |
| Скриня зі скарбом | pickup | монети | клік → монети, клітина звільняється (?) |
| Камінь | static | — | займає місце; 3 → гора (?) |
| Гора | static | — | 3 → велика скриня (?) |
| Кристал | tile | wildcard | ставиться як будь-який предмет, що дає злиття (найвищий можливий); нема злиття → камінь (?) |
| Imperial bot (робот) | pickup | одноразовий | знищує предмет у клітині; на ведмедя — перетворює його на надгробок |
| Склад (storehouse) | container | 1 слот | тримає один предмет; обмін з поточним |
| Поточний предмет | player | тип | «у руці»; ставиться кліком у порожню клітину |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `spawn(current_item)` з колоди ймовірностей: трава найчастіше, далі кущ, ведмідь, ніндзя, кристал, бот, рідко дерево/хатина (`custom: «зважений випадок»`).
- КОЛИ `input(click cell)` → ЯКЩО `free(cell)` → ТО `move(current_item, cell)`; інакше `block` (крім бота — його можна на зайняту).
- КОЛИ `after(place)` → ЯКЩО `pattern(group(3+, same_type, adj4))`, що містить нову клітину → ТО `merge(group → next_tier)` у клітині щойно поставленого, решта клітин групи звільняється; `score(+n)`.
- КОЛИ `after(merge)` → ЯКЩО новий предмет утворює групу 3+ зі своїми сусідами → ТО `merge` знову (каскад: кущ, що зʼявився поруч із двома кущами, одразу дає дерево) — `combo(+1)`.
- КОЛИ `pattern(group(4+))` → ТО `custom: «бонус — більше очок / монети або предмет у склад»` (за Wikipedia).
- КОЛИ `input(click cell with crystal)` → ТО кристал `transform` у тип, що дає злиття з сусідами (найвищий варіант); ЯКЩО жоден → ТО `transform(rock)` (?).
- КОЛИ `input(click cell with bot)` → ЯКЩО `occupied(cell, bear)` → ТО `transform(bear → tombstone)`; ЯКЩО `occupied(cell, item)` → ТО `disappear_b`; порожня клітина — бот пропадає даремно (?).
- КОЛИ `turn_end(player)` → ТО кожен ведмідь `move(bear, random_adjacent_free)` (`random-walk`); ніндзя — `teleport(random_free)`.
- КОЛИ `turn_end(player)` → ЯКЩО `blocked(bear)` для всієї звʼязаної групи ведмедів (жоден не має порожньої сусідньої клітини) → ТО `transform(bears → tombstone)`, і надгробки зливаються за звичайним правилом 3+.
- КОЛИ `input(click storehouse)` → ТО `custom: «hold_swap — поточний ↔ збережений; порожній склад просто забирає поточний»`.
- КОЛИ `input(click chest)` → ТО `currency(+n)`, `disappear_b` (?).
- КОЛИ `custom: «поле заповнене»` (`count(empty, ==, 0)`) → ТО `game_over`; рахунок фіксується.
- Перемога: нема — гра на рахунок. Поразка: заповнене поле. Рахунок: очки за кожне розміщення і злиття, вищі рівні — значно більше.
- Монетизація (Kindle/Facebook/мобільні): обмежена кількість ходів, що відновлюється з часом або купується (`custom: «turn energy»`); Steam-версія — без обмеження.

## Керування і ввід
- Курсор/тап: клік у порожню клітину ставить поточний предмет; наведення показує, що злиється (контур/підсвітка групи) (?).
- Клік по складу — обмін поточного з тим, що лежить у складі.
- Клік по скрині — забрати монети.
- Магазин: купити конкретний предмет (кристал, бот, хатину…) замість випадкового за монети.

## Вікна, меню, HUD
- `main-menu` → нова гра / продовжити; у веб-версії 2012 — «Capital City» (база з містами-партіями) (`custom-window`).
- `game-screen`: поле 6×6, склад у куті (`+ui:hold-slot`), поточний предмет (`+ui:next-tile-preview`), `score`, `coins`, лічильник ходів (`turn-counter`, у freemium — енергія), кнопка магазину.
- `shop-window`: каталог предметів з цінами в монетах.
- `end-screen`: місто заповнене — підсумковий рахунок, рекорд.
- `help-window`/`tutorial-window`: перші ходи з підказками, як зливати і замикати ведмедів (?).
- Переходи: main-menu → game-screen ↔ shop-window → end-screen → main-menu.

## Фічі поза полем
- `autosave` — партія триває між сесіями (одне місто — довга гра).
- `leaderboard-local`/`leaderboard-online` (Facebook — друзі) (?).
- `shop` за ігрову валюту (`round-currency`), freemium-ліміт ходів з відновленням у реальному часі.
- Web 2012: Capital City — мета-прогресія між партіями (`meta-progression`).
- `tutorial`.

## Варіації й родичі
- Предок ідеї «3 сусідні → наступний рівень» серед match-ігор: Triple Town сама стала зразком; наступники — Merge Dragons, Merge Mansion, Triple Town Stars (?), Yeti Town (Spry Fox, 2013) (?).
- 2048/Threes — злиття за рухом поля, а не за розміщенням; Triple Town — розміщення курсором.
- **Осі варіацій**: розмір групи (3 / 4 / 5) · де зʼявляється результат (остання клітина / центр групи) · каскад (так / ні) · перешкоди (ведмідь-блукач / ніндзя-телепорт / статичний камінь) · як прибрати перешкоду (замкнути / бот) · джокер (кристал) · кишеня (склад на 1 / нема).

## Цікавинки для курсу
- Злиття групи 3+ у клітині останнього розміщення + каскад вгору по ланцюгу рівнів — 📎 (flood fill + цикл).
- Ведмідь-блукач і замикання групи ведмедів (flood fill по ведмедях, перевірка виходів) — 🥉.
- Кристал-джокер: перебрати типи й обрати найвищий, що дає злиття — 📎.
- Склад-обмін (hold) — 🌱; бот-видалення — 🌱.
- Зважений рандом предметів з таблиці — 🌱; магазин за монети — 📎.
- Простий AI-радник «куди поставити» (жадібна оцінка) — 🥈.

## Мапа на каталог
- Є: `tile-merge` (3 → наступний рівень) · `cell-click` · `spawn-random-cell` (лише як «випадковий предмет», клітину обирає гравець) · `random-walk` (ведмеді) · `inventory-limit` (склад на 1) · `round-currency` + `shop-window` + `shop-catalog` · `event-points` · `score-records` · `save-autosave`.
- **Нема** → пропозиції карток:
  - `+connected-group-pop` — ⏳ підтверджую (Puyo), тут слоти {min: 3, adjacency: 4, result: next_tier}.
  - `+chain-reaction` — ⏳ підтверджую: каскад злиттів.
  - `+weighted-spawn` — спільна з 2048.
  - `+merge-at-placement` «Результат злиття — в клітині останнього ходу» · entities/legality · 🌱.
  - `+enclosure-capture` «Замкнена сутність без виходу гине/перетворюється» · entities/interact · 🥉 — групова перевірка виходів (споріднено з го).
  - `+wildcard-tile` «Джокер-плитка» · entities/legality · 📎 — також Magical Drop (rainbow) (?).
  - `+hold-piece` — ⏳ підтверджую (Tetris): склад.
  - `+remover-item` «Предмет-знищувач клітини» · entities/interact · 🌱 (бот).
  - `+turn-limit-energy` «Ходи, що відновлюються з часом» · game-logic/economy · 🌱 (freemium).

## Пропозиції до словників
- `+trigger:input` · `+trigger:pattern` (`group(3+)`) · `+trigger:no_moves` (заповнене поле) — ⏳ підтверджую.
- `+cond:adjacent_count` — у ведмедя 0 порожніх сусідів (замикання); `+cond:free`.
- `+effect:merge` · `+effect:transform` (ведмідь → надгробок, кристал → тип) · `+effect:move` · `+effect:hold_swap` (з Tetris) · `+effect:currency`.
- `+role:tile`; `+role:neutral` — ведмідь не шкодить, лише займає місце (тому в таблиці `enemy`, але сутнісно — «заважальник»).
- `+ui:next-tile-preview` (поточний предмет, з Isle of Arrows) · `+ui:hold-slot` (склад).
- `+window:shop-window` ✅ — тут магазин всередині партії.
- `+axis:undo` — `none`.

## Джерела
- ⭐ [Wikipedia: Triple Town](https://en.wikipedia.org/wiki/Triple_Town) — 6×6, злиття в позиції останнього, ведмеді й ніндзя, надгробки → церква → собор, кристал, бот, склад, кінець при заповненні, freemium-ходи.
- [Steam: Triple Town](https://store.steampowered.com/app/209950/Triple_Town/) — PC/Mac 2012, опис, 6×6.
- YouTube: пошук «triple town gameplay bears».

## Непевне
- (?) Рівні після «будинку» (маєток, замок, літаючий замок, потрійний замок) — з памʼяті; Wikipedia обривається на «house, and so forth».
- (?) Собор → скриня; камінь → гора → велика скриня — з памʼяті, не підтверджено.
- (?) Кристал без можливого злиття стає каменем; бот на порожню клітину — даремно.
- (?) Ймовірності предметів і стартове заповнення поля.
- (?) Як саме дає бонус група 4+ (Wikipedia: «coins or a tile to the sidebar inventory»).
- WebSearch-бюджет вичерпано на цій грі; фан-вікі (fandom) не відкрилась (402) — список предметів не звірено.
