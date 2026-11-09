---
title: Railroad Ink
slug: railroad-ink
aka: [Railroad Ink Deep Blue Edition, Railroad Ink Blazing Red Edition, Railroad Ink Challenge]
family: board-digital
also: [connect-rotate]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2018
platforms: [board, iOS, Android]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/railroad-ink/game-rules.php", best: true, note: "правила Deep Blue: кубики, розміщення, спецмаршрути, підрахунок, помилки"}
  - {kind: other, url: "https://rulespal.com/railroad-ink/rulebook", note: "грані кубиків, таблиця очок за виходи 2→4 … 12→45, раунди розширень"}
  - {kind: other, url: "https://www.ultraboardgames.com/railroad-ink/expansions.php", note: "розширення River і Lake (Deep Blue)"}
  - {kind: bgg, url: "https://boardgamegeek.com/boardgamefamily/57676/game-railroad-ink", note: "сімʼя видань (сторінку не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Railroad+Ink+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 70
mechanics: [cell-click, hover-highlight, legal-move-highlight, tile-rotate, piece-rotate-flip, pipe-connectors, connectivity-check, event-points, score-records, game-settings, rule-variants, game-screen, end-screen, help-window, +named-resource-all-place, +simultaneous-turns, +dice-pool-draw, +mandatory-use-all, +limited-special-pieces, +connected-exits-scoring, +longest-path-scoring, +open-end-penalty, +central-area-bonus, +round-stamp, +crossing-overpass, +type-adapter-tile, +expansion-modules]
proposes: ["+trigger:round_end", "+cond:ports_compatible", "+cond:connected_to_network", "+role:exit", "+ui:dice-pool", "+ui:special-routes-panel", "+ui:open-end-markers", "+window:round-summary", "+card:connected-exits-scoring", "+card:longest-path-scoring", "+card:open-end-penalty", "+card:limited-special-pieces", "+card:type-adapter-tile"]
author: opus
date: 2026-11-09
---

# Railroad Ink — roll-and-write мереж: кидок 4 кубиків, усі малюють ті самі маршрути, щоб зʼєднати виходи краю

## Суть
На початку раунду кидають 4 кубики-маршрути; **кожен** гравець малює всі 4 показані фрагменти доріг і залізниць у клітини свого поля (повертати й віддзеркалювати можна). Кожен фрагмент мусить торкатися виходу на краю або вже намальованої мережі; дорогу й колію напряму не зʼєднати — потрібна станція. Після 7 раундів рахують мережі, що зʼєднують кілька виходів, найдовші дорогу й колію, центр поля — і віднімають по очку за кожен обірваний кінець. Ядро — сітка «плиток-зʼєднувачів» з типами портів і граф мереж, який будуєш з чужого рандому.

## Поле і час
- Особисте квадратне поле з виходами по периметру (кожен — дорога або колія); 9 центральних клітин (3×3) дають бонус. Розмір поля й кількість виходів — у «Непевне»; таблиця очок закінчується на 12 виходах.
- Клітина вміщує один фрагмент: у кожної з 4 сторін — порт «дорога», «колія» або «нічого».
- Раунд = один кидок 4 кубиків; усі малюють одночасно, взаємодії між гравцями нема («мультиплеєр-пасьянс»). У кінці раунду в кожну намальовану клітину пишуть номер раунду — пізніше не стерти.
- Базова гра: 7 раундів; з розширеннями River / Lake — 6.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина поля | zone | порожня / з фрагментом; номер раунду | приймає рівно один фрагмент; не переписується |
| Центральна клітина | zone | 9 штук (3×3) | +1, якщо в ній будь-який маршрут |
| Вихід (Exit) | static | тип порту: дорога / колія; на краю поля | точка, до якої може торкатись перший фрагмент; рахується в мережі |
| Фрагмент дороги | conduit | пряма / поворот / T-розвилка | зʼєднує сусідні клітини через порти «дорога» |
| Фрагмент колії | conduit | пряма / поворот / T-розвилка | те саме для портів «колія» |
| Станція | conduit | пряма / кутова | єдиний спосіб зʼєднати дорогу з колією в одній клітині |
| Естакада (Overpass) | conduit | дорога ✕ колія | дві мережі перетинаються без зʼєднання |
| Кубик маршрутів ×3 | supply | 6 граней: пряма/поворот/T дороги й колії | кидок на раунд; кожну грань малюють один раз |
| Кубик спецвузлів ×1 | supply | 3 види: естакада, пряма станція, кутова станція | так само обовʼязковий |
| Спецмаршрути | supply | 6 на полі гравця; ≤1 за раунд, ≤3 за гру, кожен 1 раз | перехрестя-«джокери» понад кубики |
| Мережа | zone | множина звʼязних фрагментів | рахується за кількістю зʼєднаних виходів |
| Кубики River / Lake | supply | лише в розширеннях | третій тип маршруту / озера з пірсами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(round)` → ТО `custom: «кинути 4 кубики маршрутів один раз для всіх гравців»`.
- КОЛИ `input(place(route, cell))` → ЯКЩО `free(cell)` і `custom: «хоч один порт торкається виходу або наявного маршруту»` (`+cond:connected_to_network`) → ТО `place(route, cell)`; інакше `block`.
- КОЛИ `input(rotate(route))` → ТО `rotate(route, 90)`; також `custom: «віддзеркалити фрагмент»` — будь-який із 8 образів.
- КОЛИ `input(place(route, cell))` → ЯКЩО `custom: «порт дороги впирається в порт колії сусіда»` (`+cond:ports_compatible`) → ТО `block` — потрібна станція.
- КОЛИ `turn_end(round)` → ЯКЩО `custom: «показаний фрагмент ще можна легально намалювати»` → ТО `block` кінця раунду: усі 4 грані обовʼязкові; кожну грань — рівно один раз.
- КОЛИ `input(place(special, cell))` → ЯКЩО `custom: «у цьому раунді спецмаршрут ще не брали»` і `count(used_specials, <, 3)` і `not state(special, used)` → ТО `place(special, cell)`, `set_state(special, used)`.
- КОЛИ `turn_end(round)` → ТО `mark(cells_drawn, round_number)` — фрагменти раунду зафіксовано.
- КОЛИ `counter(round, =, 7)` → ТО `game_over`, підрахунок.
- Мережі: для кожної мережі ЯКЩО `count(exits_in_network, >=, 2)` → ТО `score(+n)` за таблицею 2→4, 3→8, 4→12 … 11→40, 12→45 (`connected` — звʼязність мережі).
- Найдовша дорога: ТО `score(+len)` — `custom: «найдовший неперервний шлях дорогою без петель і розгалужень; станції не переривають»`. Те саме окремо для колії.
- Центр: ТО `score(+1)` за кожну з 9 центральних клітин з маршрутом.
- Помилки: КОЛИ `game_over` → ТО `score(-1)` за кожен `custom: «кінець маршруту, що не зʼєднаний з іншим маршрутом і не впирається в зовнішній край»`.
- Нічия: менше помилок перемагає; далі — спільна перемога.
- River: ЯКЩО `custom: «річка торкається виходу або іншого типу маршруту»` → ТО `block`; дорога/колія перетинає річку лише через грань-міст; одна обрана річка дає `score(+len)` і ще +3, якщо обидва кінці на краю поля.
- Lake: ЯКЩО `adjacent_count(cell, open_lake_side, >=, 3)` → ТО `set_cell(cell, lake)` одразу; мережі, що з пірсами в одне озеро, — одна мережа; найменше озеро дає `score(+cells)`; відкриті боки озера — не помилка.
- Перемога: найбільше очок після останнього раунду · Поразка: — · Рахунок: мережі + дві найдовші лінії + центр − помилки + бонус розширення.

## Керування і ввід
- Паперово: олівцем малюєш фрагмент у клітину, у кутку пишеш номер раунду, на полі закреслюєш використаний спецмаршрут.
- (цифрова версія) Перетягнути грань кубика на клітину (`drag-drop-piece`) або виділити грань і клікнути клітину; кнопки «повернути» / «віддзеркалити» перед підтвердженням; наведення показує фантом і нелегальні порти червоним.
- Кнопка «завершити раунд» активна лише коли використано всі 4 грані або решту справді нема куди поставити.
- Undo — лише в межах поточного раунду (фрагменти попередніх раундів зафіксовані).

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Соло на рекорд · Кілька гравців · Розширення · Правила · Налаштування.
- `match-setup`: кількість гравців, видання (Deep Blue / Blazing Red), розширення (River / Lake / …).
- `game-screen`: поле з виходами; `dice-pool` — 4 грані поточного кидка з позначкою «використано»; `special-routes-panel` — 6 спецмаршрутів, лічильник «≤1 за раунд, ≤3 за гру»; `turn-counter` (раунд 1/7); `open-end-markers` — підсвітка обірваних кінців; `score-preview`; `legal-move-highlight` для вибраної грані.
- `round-summary` (кандидат) не потрібен щораунду; `end-screen`: таблиця підрахунку (мережі · дорога · колія · центр · помилки · розширення · разом) з підсвіткою кожної мережі кольором.
- `leaderboard` / `stats-window`: найкращі соло-рахунки.
- `help-window`: грані кубиків і правило «станція між дорогою й колією».
- Переходи: main-menu → match-setup → game-screen ×7 → end-screen → main-menu.

## Фічі поза полем
- `seed-input` / `share-code`: однакові кидки для всіх → природний «щоденний виклик» (?) у цифрових версіях.
- `custom-rules`: вибір розширення (лише одне за гру), видання з іншими кубиками.
- `undo` у межах раунду; `rules-page`; `leaderboard-local`.
- Соло: та сама гра на рекорд — гравці й так не взаємодіють.

## Варіації й родичі
- Видання: Deep Blue (River, Lake), Blazing Red (лава, метеорити (?)), Challenge-видання Lush Green / Shining Yellow (?) з картками-цілями.
- Родичі «один кидок — усі малюють»: Take It Easy (плитки), NMBR 9, Cartographers, Tiny Towns, Welcome To; мережі з типами портів — Carcassonne (дороги/міста), Tantrix, Pipe Mania.
- **Осі варіацій**: хто дає фрагмент (кубики / колода / викликач) · типи портів (1 / 2 + адаптер / 3 з річкою) · обовʼязковість (усі грані / за вибором) · що рахується (виходи / найдовша лінія / центр / площа озера) · штраф за обірваний кінець (−1 / 0).

## Цікавинки для курсу
- Плитка-зʼєднувач з 4 портами трьох типів, поворот і дзеркало як перестановка портів — 📎.
- Перевірка легальності: «торкається мережі» + «порти сумісні» + «грань ще не використана» — 📎.
- Обовʼязковість: чи можна ще кудись поставити хоч одну грань (перебір клітин × 8 орієнтацій) — 🥉.
- Мережі через union-find / BFS з естакадами (одна клітина — два вузли) і рахунок виходів у кожній — 🥉.
- Найдовший шлях без петель і розгалужень по одному типу — NP-важко в загальному, але поле мале: DFS із відсіканням — 🥈.
- Підрахунок обірваних кінців (порт без пари й не на краю) — 🌱.
- AI-порадник «куди найкраще» з очікуванням майбутніх кидків — 🥇.

## Мапа на каталог
- Є: `cell-click` · `hover-highlight` · `legal-move-highlight` · `tile-rotate` + `piece-rotate-flip` (поворот і дзеркало) · `pipe-connectors` ↔ фрагменти з портами · `connectivity-check` ↔ мережі · `event-points` · `score-records` · `game-settings` · `rule-variants` ↔ розширення · `game-screen`, `end-screen`, `help-window`.
- **Нема** → пропозиції карток:
  - `+named-resource-all-place` (Tiny Towns) · `+simultaneous-turns` (Cartographers) — усі малюють той самий кидок.
  - `+dice-pool-draw` «Кидок кубиків = набір фігур на хід» · levels/generation · 🌱 · слоти {dice: 4, faces}.
  - `+mandatory-use-all` «Використати всі показані фігури, якщо можливо» · entities/legality · 🥉.
  - `+limited-special-pieces` «Джокери з лімітами за раунд і за гру» · game-logic/economy · 📎 · слоти {per_round: 1, per_game: 3, pool: 6}.
  - `+connected-exits-scoring` «Очки за кількість виходів у мережі» · game-logic/score · 🥉 · слоти {table}.
  - `+longest-path-scoring` «Найдовший шлях без розгалужень» · game-logic/score · 🥈.
  - `+open-end-penalty` «Мінус за обірваний кінець» · game-logic/score · 🌱.
  - `+central-area-bonus` «Бонус за зайняті центральні клітини» · game-logic/score · 🌱.
  - `+round-stamp` «Позначка раунду — фіксація ходу» · game-logic/history · 🌱.
  - `+crossing-overpass` «Перехрестя без зʼєднання» · entities/state · 📎 (родич `bridge-cell` у Flow Free).
  - `+type-adapter-tile` «Плитка-адаптер між двома типами портів» · entities/state · 📎 — станція.
  - `+expansion-modules` «Модулі правил: одне розширення за гру» · game-logic/constraints · 📎 (дитина `rule-variants`).

## Пропозиції до словників
- `+trigger:round_end` — кінець раунду (Railroad Ink: фіксація; Cartographers, Odin).
- `+cond:ports_compatible` — порти сусідніх фрагментів одного типу (дорога-дорога), інакше зʼєднання заборонене.
- `+cond:connected_to_network` — новий фрагмент торкається виходу або наявної мережі.
- `+role:exit` — вихід на краю поля з типом порту, що рахується в мережі (родич `source`/`sink`).
- `+ui:dice-pool` — грані поточного кидка з позначкою «використано».
- `+ui:special-routes-panel` — запас джокерів з лімітами.
- `+ui:open-end-markers` — підсвітка обірваних кінців (майбутніх штрафів).
- `+window:round-summary` — як у Take It Easy; тут — підсумковий розклад очок.
- `+card:connected-exits-scoring` · `+card:longest-path-scoring` · `+card:open-end-penalty` · `+card:limited-special-pieces` · `+card:type-adapter-tile` — див. «Мапа на каталог».

## Джерела
- ⭐ [UltraBoardGames: Railroad Ink rules](https://www.ultraboardgames.com/railroad-ink/game-rules.php) — компоненти, раунди, 6 правил розміщення, спецмаршрути (1/раунд, 3/гру), підрахунок, помилки, нічия.
- [RulesPal: Railroad Ink rulebook](https://rulespal.com/railroad-ink/rulebook) — грані кубиків, таблиця «виходи → очки» 2→4 … 12→45.
- [UltraBoardGames: expansions](https://www.ultraboardgames.com/railroad-ink/expansions.php) — River (6 раундів, міст, +3 за обидва краї) і Lake (пірси, примусове заповнення, найменше озеро).
- BGG: [сімʼя Railroad Ink](https://boardgamegeek.com/boardgamefamily/57676/game-railroad-ink) (не відкривав).
- YouTube: пошук «Railroad Ink how to play».

## Непевне
- (?) Поле 7×7 і 12 виходів (по 3 на бік) — з черги й памʼяті; джерела прямо не кажуть, але таблиця очок закінчується на 12 виходах, а центр — 3×3.
- (?) Склад 6 спецмаршрутів (різні перехрестя доріг/колій зі станціями) — на сторінках лише картинкою.
- (?) Скільки граней на кубику спецвузлів має кожен із 3 видів (імовірно по 2).
- (?) Розширення Blazing Red (лава, метеорити), Challenge-видання й цифрові застосунки — сторінок не відкривав.
- (?) Найдовша дорога: «петлі й розгалуження не рахуються» — неясно, чи можна пройти через T-розвилку, обравши одну гілку (імовірно так).
