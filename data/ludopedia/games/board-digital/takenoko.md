---
title: Takenoko (Такеноко)
slug: takenoko
aka: [Такеноко, Takenoko Chibis, 竹の子]
family: board-digital
also: []
klass: hybrid
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: partial
  random: both
  goal: score
year: 2011
platforms: [board]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/takenoko/game-rules.php", best: true, note: "повні правила: ділянки, зрошення, панда й садівник, погода, поліпшення, цілі, кінець гри"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Takenoko_(board_game)", note: "рік, автор Antoine Bauza, видавці, нагороди, доповнення Chibis"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Takenoko+how+to+play", note: "пошук; як грати"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Takenoko", note: "пошук BGG"}
stage: v1
coverage: 55
mechanics: [cell-click, drag-drop-piece, legal-move-highlight, hover-highlight, turn-enforcement, hot-seat, ai-opponent, event-points, goal-counter, match-setup, end-screen, help-window, +hex-grid-render, +path-move-any-distance, +connected-placement, +irrigation-network, +bamboo-stack-growth, +same-color-neighbor-growth, +weather-die, +two-different-actions, +secret-objective-hand, +objective-hand-limit, +pattern-objective, +endgame-trigger-by-count, +tile-draft-three-keep-one, +protected-cell-improvement]
proposes: ["+cond:irrigated(cell)", "+cond:straight_line(from, to)", "+cond:connected_to_network", "+trigger:objective_met", "+effect:eat(cell)", "+role:objective", "+role:network-edge", "+ui:objective-cards", "+ui:bamboo-reserve", "+window:weather-roll", "+card:irrigation-network", "+card:weather-die", "+card:secret-objective-hand"]
author: opus
date: 2026-11-09
---

# Takenoko — гекс-сад росте від ставка; садівник вирощує бамбук, панда його їсть, а гравці виконують таємні цілі

## Суть
Гравці спільно викладають гекс-ділянки трьох кольорів навколо ставка, проводять канали зрошення по ребрах гексів і ходять двома спільними фігурами: садівник додає бамбук на ділянку й сусідні того самого кольору, панда зʼїдає секцію й віддає її гравцеві. Очки — лише за виконані таємні картки цілей трьох типів: візерунок ділянок, висота бамбуку, набір зʼїдених секцій. Незвичне: поле, фігури й бамбук спільні, а цілі приховані — кожен хід працює й на суперників. Клас `hybrid`: `cursor` (викладання ділянок і каналів) + `figure` (дві спільні фігури з ходом «прямою»).

## Поле і час
- Поле — гекс-сітка без меж, що росте від центрального ставка; на старті лише ставок, на ньому панда й садівник.
- Шари: ділянки (гекси кольору green / yellow / pink) · ребра між гексами (канали зрошення) · стос бамбуку на ділянці (0–4 секції) · поліпшення (≤1 на ділянку).
- Хід гравця: (з 2-го раунду) кидок кубика погоди → дві **різні** дії → виконання цілей. Ходи за годинниковою стрілкою.
- Інформація: поле відкрите; цілі в руці приховані; колода ділянок і колоди цілей закриті.
- Випадковість: кубик погоди щоходу, витяг ділянок і цілей.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ставок | static | центр | старт мережі зрошення з кутів; сусідні ділянки зрошені автоматично |
| Ділянка | terrain | колір green/yellow/pink; зрошена так/ні | кладеться біля ставка або біля двох ділянок; росте лише свій колір |
| Секція бамбуку | object | колір ділянки | стос ≤4 на ділянці; росте лише на зрошеній |
| Канал зрошення | conduit | на ребрі | мережа від кута ставка; зрошує обидві ділянки ребра; не на боках ставка |
| Садівник | piece | спільний | хід прямою на будь-яку відстань по ділянках; +1 секція на кінцевій і сусідніх того самого кольору |
| Панда | piece | спільна | хід прямою на будь-яку відстань по ділянках; зʼїдає 1 секцію на кінцевій → на планшет гравця |
| Огорожа (enclosure) | static | поліпшення | панда може стати, але не їсть |
| Добриво (fertilizer) | static | поліпшення | кожен ріст +2 замість +1 (у межах 4) |
| Водозбір (watershed) | static | поліпшення | ділянка зрошена сама; не стартує мережу |
| Ціль «ділянки» | objective | візерунок 3–4 ділянок | усі ділянки візерунку зрошені |
| Ціль «садівник» | objective | висота/поліпшення | стос 4 з (без) поліпшенням або кілька стосів по 3 |
| Ціль «панда» | objective | 2–3 секції кольорів | скинути ці секції з планшета |
| Картка Імператора | pickup | 2 очки | тому, хто запустив фінал |
| Кубик погоди | spawner | 6 граней | Sun / Rain / Wind / Storm / Clouds / «?» |
| Планшет гравця | supply | 2 жетони дій | зʼїдені секції, запас каналів і поліпшень, рука цілей ≤5 |

## Правила (КОЛИ → ЯКЩО → ТО)
- Погода: КОЛИ `turn_start(p)` → ЯКЩО `custom: «раунд ≥ 2»` → ТО `custom: «кинути кубик погоди і застосувати грань»`.
- Sun: ТО `extra_move` — третя дія, відмінна від двох звичайних.
- Rain: ТО `grow(bamboo, 1)` на зрошеній ділянці на вибір (≤4).
- Wind: ТО `custom: «цього ходу дві дії можуть бути однаковими»`.
- Storm: ТО `move(panda, any_plot)` + `custom: «панда зʼїдає 1 секцію там»`.
- Clouds: ТО `give(p, improvement)`; ЯКЩО `count(improvement_reserve, =, 0)` → ТО `choose(Sun|Rain|Wind|Storm)`.
- «?»: ТО `choose(Sun|Rain|Wind|Storm|Clouds)`.
- Дії: КОЛИ `input(action)` → ЯКЩО `custom: «дія ще не виконана цього ходу»` → ТО виконати; дві різні дії на хід.
- Ділянка: КОЛИ `input(custom: «дія Ділянки»)` → ТО `custom: «взяти 3 ділянки, лишити 1, решту — на верх колоди в обраному порядку»`; КОЛИ `input(place(plot, cell))` → ЯКЩО `adjacent_count(cell, pond, >=, 1)` or `adjacent_count(cell, plot, >=, 2)` → ТО `place(plot)`; інакше `block`.
- Перше зрошення: КОЛИ `custom: «ділянка вперше стала зрошеною»` → ТО `grow(bamboo, 1)` — один раз за гру.
- Зрошеність: ЯКЩО `adjacent_count(cell, pond, >=, 1)` or `custom: «на одному з 6 ребер є канал»` or `state(cell, watershed)` → ТО `set_state(cell, irrigated)`.
- Канал: КОЛИ `input(custom: «покласти канал на ребро»)` → ЯКЩО `custom: «ребро зʼєднане з мережею, що починається з кута ставка»` and `not custom: «ребро — бік ставка»` → ТО `place(channel)`; канал можна взяти дією й тримати в запасі, класти — будь-коли у свій хід безкоштовно.
- Садівник: КОЛИ `input(move(gardener, cell))` → ЯКЩО `custom: «ціль на прямій лінії гексів, без проміжків»` → ТО `move(gardener)` + `grow(bamboo, 1)` на кінцевій і на кожній сусідній ділянці того самого кольору, ЯКЩО `state(cell, irrigated)`.
- Ріст: ЯКЩО `custom: «стос = 4»` → ТО `block` росту; ЯКЩО `state(cell, fertilizer)` → ТО `grow(bamboo, 2)` замість 1.
- Панда: КОЛИ `input(move(panda, cell))` → ЯКЩО `custom: «пряма лінія без проміжків»` → ТО `move(panda)`; ЯКЩО `custom: «стос > 0»` and `not state(cell, enclosure)` → ТО `take(cell, bamboo)` + `give(p, bamboo)`.
- Поліпшення: КОЛИ `input(place(improvement, cell))` → ЯКЩО `custom: «на ділянці ще не ріс бамбук»` and `not state(cell, improved)` → ТО `set_state(cell, improvement)`; назавжди, ≤1 на ділянку; не дія.
- Ціль: КОЛИ `input(action)` «Ціль» → ЯКЩО `count(hand, <, 5)` → ТО `give(p, objective)` з обраної колоди; з 5 картами — спершу виконати хоча б одну.
- Виконання: КОЛИ `custom: «умова картки в руці справджується»` → ТО `custom: «відкрити картку перед собою»` + `score(n)`; не дія, кілька за хід; виконана лишається, хоч би поле змінилось.
- Ціль «ділянки»: КОЛИ `pattern(custom: «3–4 сусідні ділянки заданих кольорів і форми»)` → ЯКЩО `custom: «усі зрошені»` → ТО виконано.
- Ціль «панда»: ЯКЩО `has(p, bamboo_set)` → ТО виконано + `custom: «секції повертаються в резерв»`.
- Фінал: КОЛИ `counter(objectives_done, >=, 9|8|7)` (2|3|4 гравці) → ТО `give(p, emperor)` + `score(2)` + `custom: «кожен інший гравець має ще один хід»`.
- Рахунок: сума очок виконаних цілей + Імператор; невиконані в руці — 0.
- Перемога: найбільше очок · нічия — більше очок за цілі «панда» · далі — спільна перемога.

## Керування і ввід
- Дві дії на хід: обрати жетон дії (Ділянка / Канал / Садівник / Панда / Ціль), порядок — на вибір.
- Ділянка: вибір 1 з 3, drag на вільний гекс із підсвіткою легальних (біля ставка або двох ділянок).
- Канал: клік по ребру гекса, підсвітка ребер, що продовжують мережу.
- Садівник / панда: клік по гексу на одній з 6 прямих; проміжок-порожнеча обриває лінію.
- Виконання цілей — у будь-який момент свого ходу кліком по картці.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Нова гра → `match-setup` · Правила → `help-window`.
- `match-setup`: 2–4 гравці, люди/AI, доповнення Chibis.
- `game-screen`: гекс-поле, панда й садівник, `turn-indicator`, `bamboo-reserve` (кандидат), запас каналів і поліпшень, `objective-cards` (кандидат: рука до 5), лічильник виконаних цілей проти порогу фіналу.
- `weather-roll` (кандидат): кидок і вибір ефекту для Clouds / «?».
- Вибір ділянки — модал «1 з 3».
- `end-screen`: виконані цілі кожного, очки, тай-брейк.
- Переходи: main-menu → match-setup → game-screen ⇄ weather-roll / вибір ділянки → end-screen.

## Фічі поза полем
- `hotseat` на 2–4; приховані цілі вимагають `pass-device` або особистих екранів.
- `custom-rules`: доповнення Chibis (панда-самка, панденята, нові ділянки й цілі).
- Колекційне видання — більші компоненти (не механіка).

## Варіації й родичі
- Takenoko: Chibis (доповнення).
- Спільні фігури, що рухаються прямою на будь-яку відстань по гексах: [hey-thats-my-fish](hey-thats-my-fish.md).
- Викладання гексів біля наявних і рахунок за візерунки: [cascadia-calico](cascadia-calico.md), [harmonies](harmonies.md), [akropolis](akropolis.md); мережа від джерела — [karuba](karuba.md), [railroad-ink](railroad-ink.md).
- Ріст рослин як стан клітини: [photosynthesis](photosynthesis.md).
- **Осі варіацій**: хто росте (садівник — ціль + сусіди кольору / дощ — одна ділянка) · що дає ріст (зрошення від мережі / поліпшення) · спільні фігури vs власні · цілі приховані vs відкриті · фінал (поріг цілей / вичерпання колоди).

## Цікавинки для курсу
- Мережа зрошення на ребрах гексів від кутів ставка й обчислення «зрошених» ділянок (BFS по ребрах) — 🥉.
- Хід «прямою на будь-яку відстань» у гекс-координатах (кубічні координати, 6 напрямків, обрив на порожньому) — 📎.
- Ріст садівника: кінцева ділянка + сусіди того самого кольору, лише зрошені, кап 4, добриво ×2 — 🌱.
- Перевірка цілі-візерунка «3–4 ділянки заданих кольорів і форми» з поворотами на гекс-сітці — 🥈.
- Кубик погоди як таблиця модифікаторів ходу (зайва дія, дубль дій, телепорт панди) — 📎.
- AI, що оцінює ходи за власними прихованими цілями й не допомагає суперникам — 🥇.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `legal-move-highlight` · `hover-highlight` · `turn-enforcement` · `hot-seat` · `ai-opponent` · `event-points` (очки цілей) · `goal-counter` (виконані цілі до фіналу) · `match-setup` · `end-screen` · `help-window`.
- Уже в корпусі: `+hex-grid-render`, `+path-move-any-distance` (Hey, That's My Fish!), `+connected-placement` (Carcassonne, Kingdomino).
- **Нема** → пропозиції карток:
  - `+irrigation-network` «Мережа на ребрах від джерела вмикає стан клітин» · game-logic/constraints · 🥉 · слоти {source: pond_corners, edge_layer: true}.
  - `+bamboo-stack-growth` «Стос на клітині росте до капу» · entities/state · 🌱 · слоти {max: 4}.
  - `+same-color-neighbor-growth` «Ефект на клітину й сусідів того самого типу» · entities/interact · 🌱.
  - `+weather-die` «Кубик-модифікатор ходу» · game-logic/economy · 📎.
  - `+two-different-actions` «N різних дій на хід» · game-logic/turns · 🌱.
  - `+secret-objective-hand` «Рука таємних цілей, очки за виконані» · game-logic/score · 📎.
  - `+objective-hand-limit` «Ліміт карт цілей у руці» · entities/legality · 🌱.
  - `+pattern-objective` «Ціль — візерунок на полі» · game-logic/win · 🥈.
  - `+endgame-trigger-by-count` «Поріг виконаних цілей запускає фінальне коло» · game-logic/win · 🌱.
  - `+tile-draft-three-keep-one` «Взяти 3, лишити 1, решту назад у заданому порядку» · entities/legality · 🌱.
  - `+protected-cell-improvement` «Поліпшення клітини блокує ворожий ефект» · entities/state · 🌱.

## Пропозиції до словників
- `+cond:irrigated(cell)` — клітина отримує ресурс від мережі/джерела (Takenoko; родич `connected_to_network`).
- `+cond:straight_line(from, to)` — ціль на одній прямій без проміжків (гекс-ходи «на будь-яку відстань»).
- `+cond:connected_to_network` — ребро/клітина продовжує мережу від джерела.
- `+trigger:objective_met` — умова картки цілі справдилась.
- `+effect:eat(cell)` — зняти одиницю зі стосу клітини собі на планшет.
- `+role:objective` · `+role:network-edge` — картка цілі й ребро-канал як сутності.
- `+ui:objective-cards` · `+ui:bamboo-reserve`.
- `+window:weather-roll` — кидок модифікатора і вибір ефекту.
- `+card:irrigation-network` · `+card:weather-die` · `+card:secret-objective-hand`.

## Джерела
- ⭐ [UltraBoardGames: Takenoko Game Rules](https://www.ultraboardgames.com/takenoko/game-rules.php) — компоненти, сетап, хід, 6 граней погоди, 5 дій, зрошення, ріст і кап 4, поліпшення, цілі, ліміт руки 5, пороги фіналу 9/8/7, Імператор 2 очки, тай-брейк.
- [Wikipedia: Takenoko (board game)](https://en.wikipedia.org/wiki/Takenoko_(board_game)) — 2011, Antoine Bauza, Bombyx/Matagot, 2–4 гравці, нагороди, Chibis.
- BGG: [пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=Takenoko); YouTube: пошук «how to play».

## Непевне
- (?) Офіційна цифрова версія: Wikipedia не згадує, у Steam-пошуку нема; можлива онлайн-версія на Board Game Arena — не перевіряв. Вікна — гіпотетичні.
- (?) Розподіл 28 ділянок і 9 поліпшень за кольорами/типами (порівну по 3?) — сторінка правил не дає.
- (?) Очки на окремих картках цілей — сторінка правил їх не наводить.
- (?) Чи може садівник/панда пройти «крізь» ставок по прямій — сторінка каже лише «по ділянках, без проміжків».
- (?) Деталі механік Chibis (панденята, поведінка панди-самки) — лише перелік з Wikipedia.
