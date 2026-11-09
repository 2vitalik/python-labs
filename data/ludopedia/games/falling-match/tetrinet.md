---
title: TetriNET
slug: tetrinet
aka: [TetriNET2, TetriFast, Blocktrix, gtetrinet]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: online
  info: full
  random: runtime
  goal: survive
year: 1997
platforms: [Windows, Unix, Mac OS X, BeOS, Haiku]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/TetriNET", best: true, note: "до 6 гравців, команди, 9 спецблоків з літерами, інвентар, варіанти TetriFast / Blocktrix / TetriNET2"}
  - {kind: fandom, url: "https://tetris.wiki/Tetrinet", note: "TetrisWiki: поле 12×22, 1 next, без hold, обертання на базі Tengen, кіки лише від стін"}
  - {kind: other, url: "https://www.harddrop.com/wiki/Tetrinet2", note: "HardDrop: 14 спецблоків TetriNET2 з тривалостями, множення за рядами, shuffle"}
  - {kind: other, url: "https://manpages.org/tetrinet-server/6", note: "man tetrinet-server: налаштування сервера, ймовірності фігур і спецблоків"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tetrinet+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [gravity-fall, multi-cell-size, keyboard-controls, progress-acceleration, inventory, inventory-items, inventory-limit, garbage-attack, simultaneous-versus, online-multiplayer, lobby-window, explode-area, swap-on-contact, next-queue, score-records, +special-blocks-in-stack, +targeted-item-use, +field-swap, +server-rules-config, +team-play, +winlist]
proposes: ["+trigger:item_used", "+cond:target", "+effect:use_item", "+effect:add_line", "+effect:clear_bottom_line", "+effect:quake_rows", "+effect:swap_fields", "+effect:nuke_field", "+effect:scramble_controls", "+role:special-block", "+ui:special-inventory", "+ui:target-numbers", "+window:partyline", "+window:winlist", "+feature:server-settings", "+feature:team-play"]
author: opus
date: 2026-11-09
---

# TetriNET — онлайн-тетріс до 6 полів, де зчищені ряди дають предмети-літери, якими б'єш будь-яке поле

## Суть
Кожен гравець має своє поле [Tetris](tetris.md) (12×22, ширше за стандарт), усі грають одночасно; перемагає останній, хто ще може ставити фігури. Головна новинка — **спецблоки**: після очисток на твоєму полі зʼявляються клітини з літерою (a, c, n, r, s, b, g, q, o); зчистиш ряд із такою — літера йде в **інвентар-чергу**, і її можна в будь-який момент застосувати до **будь-якого** з 6 полів, свого чи чужого. Тактика — не лише складати ряди, а «лікувати» себе (`c`, `n`, `g`) і псувати лідера (`a`, `q`, `s`). Чат-лобі partyline і команди — частина гри.

## Поле і час
- Поле 12×22 (видимих), фігури — 7 тетроміно; 1 next, без hold (TetriNET2 — hold і тінь), hard drop є.
- Обертання на базі Tengen NES: спавн під стелею по центру, **випадковий початковий поворот**; I/S/Z мають два стани; кіки лише від стін поля, не від блоків; кіків від підлоги нема.
- Real-time; між фігурами — затримка ~1 с на клієнті (TetriFast її прибирає).
- На екрані одночасно 6 полів: своє велике + 5 малих чужих.
- Рівень/швидкість росте за кількістю зчищених рядів; сервер може усереднювати рівні всіх гравців.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Активна фігура | player | тип, поворот | як у Tetris; спавн з випадковим поворотом |
| Клітина стеку | tile | колір | як у Tetris |
| Спецблок | pickup | літера a/c/n/r/s/b/g/q/o | звичайна клітина стеку з літерою; при зчищенні ряду → в інвентар |
| Інвентар спецблоків | container | ємність (типово 18) | черга: застосовується лише перший; переповнення — нові не беруться |
| Add Line `a` | pickup | — | +1 «битий» ряд знизу цільового поля |
| Clear Line `c` | pickup | — | знищує нижній ряд цілі |
| Nuke Field `n` | pickup | — | очищує все поле цілі |
| Random Blocks Clear `r` | pickup | — | прибирає випадкові клітини, лишаючи дірки |
| Switch Fields `s` | pickup | — | ти й ціль міняєтесь полями |
| Clear Specials `b` | pickup | — | усі спецблоки цілі стають звичайними |
| Block Gravity `g` | pickup | — | усі клітини падають у дірки, утворені ряди одразу зчищаються |
| Blockquake `q` | pickup | — | кожен ряд цілі зсувається вбік — «землетрус» |
| Block Bomb `o` | pickup | — | вибухають спецблоки `o` на полі цілі, розкидаючи клітини 3×3 довкола |
| Битий ряд | hazard | з діркою | приходить від `a` і від очисток суперників |
| Суперник | enemy | своє поле, команда | людина по мережі; ціль для твоїх спецблоків |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух, поворот, лок, очистка рядів — як у [tetris.md](tetris.md) з поправками «Поля і часу».
- КОЛИ `counter(lines_cleared, ≥, speciallines)` → ТО `spawn_at(special_block × specialcount, random_stack_cell)` (типово 1 спецблок за 1 ряд; вид — за таблицею ймовірностей сервера).
- КОЛИ `pattern(row_full)` → ЯКЩО `occupied(row, special_block)` → ТО `pickup` кожної літери ряду в інвентар; багаторядна очистка множить кількість (TetriNET2: подвійна → 2).
- КОЛИ `custom: «спецблок у чергу»` → ЯКЩО `count(inventory, ≥, specialcapacity)` → ТО `custom: «не береться»`.
- КОЛИ `input(target_n)` → ЯКЩО `count(inventory, >, 0)` → ТО `custom: «use_item — перший спецблок черги застосовується до поля гравця n (1–6, зокрема себе)»`.
- КОЛИ `input(discard)` → ТО `custom: «перший спецблок черги викидається без дії»` (?).
- `a`: ТО `spawn_at(garbage_row, bottom)`, стек зсувається вгору · `c`: ТО `clear(bottom_row)`, `drop_rows` · `n`: ТО `clear(all)`.
- `r`: ТО `custom: «знищити N випадкових клітин»` · `b`: ТО `transform(special_blocks → plain)`.
- `g`: ТО `fall(all_cells)`, далі `clear(rows)` для утворених повних рядів.
- `q`: ТО `custom: «кожен ряд — shift на випадковий зсув»` · `s`: ТО `custom: «swap_fields — обмін вмісту полів»` (захист від надмірної висоти — (?)).
- `o`: ТО `explode(3×3, into: scatter)` довкола кожного `o` на полі цілі.
- КОЛИ `pattern(row_full)` → ЯКЩО `count(rows, ≥, 2)` → ТО `send_garbage(all_opponents)` (класичний режим: 2 → 1, 3 → 2, 4 → 4 (?)); у команді — лише суперникам.
- КОЛИ `spawned(piece)` → ЯКЩО `not free(spawn_cells)` → ТО `custom: «гравець вибув»`; КОЛИ `counter(alive_teams, ==, 1)` → ТО `win` для останнього (команди).
- Варіанти правил сервера: «pure» — без спецблоків; «7tetris» — перемагає перший, хто зробив 7 Tetris.
- TetriNET2 (додаткові): Immunity — ціль невразлива 15 с · Clear Column — знищує випадковий стовпець · Mutate Pieces — 3 наступні фігури стають великими дивними · Darkness — поле цілі чорне, крім фігури, 10 с · Confusion — керування цілі перемішане 10 с; shuffle інвентаря коштує 1 спецблок.
- Blocktrix: `l` — гравітація вліво · `p` — заміна фігури · `z` — «зебра» на полі.
- Рахунок: winlist — очки за виграні партії гравцю або команді.

## Керування і ввід
- Стрілки: зсув, поворот, soft drop; пробіл — hard drop.
- Цифри **1–6** — застосувати перший спецблок до поля гравця з цим номером (свій номер — на себе).
- Клавіша `d` — викинути перший спецблок (?).
- Чат partyline — текстовий ввід у вікні лобі, також під час гри.

## Вікна, меню, HUD
- `custom-window` «Connect» — адреса сервера, нік, назва команди.
- `custom: «partyline»` (`lobby-window`) — чат, список гравців з номерами й командами, кнопка «Start game» (лише модератор каналу).
- `game-screen`: своє поле 12×22 + 5 малих полів суперників (`opponent-boards`) з іменами/номерами; `next-piece-preview`; `custom: «рядок інвентаря спецблоків»` з підписом першого; рядки/рівень; лог подій «X використав `a` на Y» (`message-log`); міні-чат.
- `custom: «winlist»` (`leaderboard`) — таблиця переможців з очками й кількістю ігор; T/P — команда чи гравець.
- `settings-window` — розкладка клавіш (`controls-remap`), звук.
- Переходи: Connect → partyline → (Start) game-screen → (кінець) partyline + оновлений winlist.

## Фічі поза полем
- `online-multiplayer` клієнт–сервер; до 6 гравців; `custom: «team-play»` — команди за назвою; `chat`; `spectator` (?) у пізніших клієнтах.
- `custom: «server-settings»` — сервер задає правила партії: стартовий рівень, рядів на рівень, приріст рівня, усереднення рівнів, speciallines/specialcount/specialcapacity, ймовірності 7 фігур і 9 спецблоків (кожна таблиця = 100), класичний режим.
- `pause` — пауза всієї партії модератором (?).
- `leaderboard-online` — winlist сервера.
- Варіанти клієнтів: TetriNET 1.13 (останній офіційний), TetriFast (без затримки між фігурами, несумісний протокол), 1.14 (однакова послідовність фігур у всіх), Blocktrix, TetriNET2 (2000: графіка, hold, тінь, майстер-сервер; закритий 2007, повернувся 2010).

## Варіації й родичі
- [tetris.md](tetris.md) — механіка поля; Tetris 99 — battle royale з таргетингом без предметів.
- [puzzle-quest.md](puzzle-quest.md) і [puzzle-and-dragons.md](puzzle-and-dragons.md) — «очистка заряджає дію» в іншій формі.
- Предмети-атаки як у картингах: спецблоки — це Mario Kart для тетрісу.
- **Осі варіацій**: атака (лише ряди / предмети / обидва) · ціль (усі суперники / вибір цифрою / автотаргет) · доставка предметів (ряд з літерою в стеку / шкала) · інвентар (черга з першим / вільний вибір / shuffle) · рівень (свій / усереднений).

## Цікавинки для курсу
- Спецблоки в стеку + інвентар-черга + застосування до поля за номером — 🥉 (предмет живе в клітині, переходить у чергу, діє на чужу модель поля).
- Набір 9 ефектів на полі (add/clear line, nuke, gravity, quake, switch, bomb) — 📎 за кожні 2–3 ефекти; `g` з подальшою очисткою — каскад.
- Таблиці ймовірностей сервера як конфіг партії (сума 100) — 🌱.
- Кілька полів одного движка на екрані (своє + 5 малих) — 📎.
- Клієнт–сервер з лобі-чатом і синхронізацією полів — 🥇.

## Мапа на каталог
- Є: `gravity-fall`, `multi-cell-size`, `keyboard-controls`, `progress-acceleration`, `inventory` + `inventory-items` + `inventory-limit` (черга спецблоків, ємність), `garbage-attack`, `simultaneous-versus`, `online-multiplayer`, `lobby-window` (partyline), `explode-area` (`o`), `swap-on-contact` (близько до `s`, але обмін полями), `next-queue`, `score-records` (winlist).
- **Нема** → пропозиції карток:
  - `+special-blocks-in-stack` «Клітини-предмети в стеку, що беруться очисткою ряду» · entities/interact · 📎 · слоти {every_lines, count}.
  - `+targeted-item-use` «Застосувати предмет до вибраного гравця» · game-logic/opponent · 🥉.
  - `+field-swap` «Обмін полями з суперником» · game-logic/opponent · 🌱.
  - `+server-rules-config` «Сервер задає правила партії» · game-logic/opponent · 📎.
  - `+team-play` «Команди у FFA» · game-logic/opponent · 📎.
  - `+winlist` «Таблиця переможців сервера» · interface/results · 🌱.

## Пропозиції до словників
- `+trigger:item_used` — гравець застосував предмет з інвентаря (точка всіх ефектів спецблоків).
- `+cond:target` — ефект діє на вибране поле/гравця, а не на себе.
- `+effect:use_item` — взяти перший предмет черги і застосувати до цілі.
- `+effect:add_line` / `+effect:clear_bottom_line` / `+effect:nuke_field` — додати/знищити нижній ряд/очистити поле цілі.
- `+effect:quake_rows` — зсунути кожен ряд на випадкову величину; `+effect:swap_fields` — обмін полів двох гравців.
- `+effect:scramble_controls` — тимчасово перемішати керування (Confusion; ширше за наявний `invert_controls`).
- `+role:special-block` — клітина поля, що несе предмет.
- `+ui:special-inventory` — рядок предметів-черги; `+ui:target-numbers` — номери полів для таргетингу.
- `+window:partyline` — чат-лобі каналу; `+window:winlist` — таблиця переможців сервера.
- `+feature:server-settings` — правила партії задає сервер; `+feature:team-play` — команди.

## Джерела
- ⭐ [Wikipedia: TetriNET](https://en.wikipedia.org/wiki/TetriNET) — 6 гравців, команди, «останній живий», 9 спецблоків з літерами й ефектами, інвентар з першим, варіанти pure/7tetris, TetriFast, 1.14, Blocktrix (l, p, z), TetriNET2.
- [TetrisWiki: Tetrinet](https://tetris.wiki/Tetrinet) — поле 12×22, 1 next, без hold, hard drop, обертання Tengen з випадковим спавн-поворотом, кіки.
- [HardDrop: Tetrinet2](https://www.harddrop.com/wiki/Tetrinet2) — 14 спецблоків, Immunity 15 с, Darkness/Confusion 10 с, Mutate — 3 фігури, Block Bomb 3×3, таргет цифрою, shuffle за 1 спецблок.
- [man tetrinet-server](https://manpages.org/tetrinet-server/6) — speciallines/specialcount/specialcapacity (18), linesperlevel, levelinc, averagelevels, ймовірності фігур і спецблоків, формат winlist.

## Непевне
- (?) Скільки битих рядів шле очистка 2/3/4 рядів (класично 1/2/4) — з памʼяті, жодне відкрите джерело не дало таблиці.
- (?) Клавіша `d` для викидання спецблоку й пауза модератором — з памʼяті.
- (?) Скільки клітин знищує `r` і на скільки зсуває `q` — джерела кажуть лише «випадково».
- (?) Обмеження `s` (обмін з дуже високим полем) — з памʼяті.
- (?) Типові значення сервера (рядів на рівень 2, ємність 18, таблиці ймовірностей) — з man-сторінки сервера Andrew Church, не оригінального Windows-сервера.
