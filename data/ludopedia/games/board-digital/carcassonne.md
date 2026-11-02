---
title: Carcassonne (Каркасон)
slug: carcassonne
family: board-digital
also: [build-sim]
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: score
year: 2000
platforms: [board, PC, mobile, web, Xbox 360, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Carcassonne_(board_game)", best: true, note: "правила 3-ї редакції: фази ходу, міплі, підрахунок, поля, відмінності редакцій, доповнення, цифрові версії"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=carcassonne", note: "грати в браузері (BGA): River, Inns & Cathedrals, Traders & Builders, Princess & Dragon"}
  - {kind: steam, url: "https://store.steampowered.com/app/598810/Carcassonne_Tiles_Tactics/", note: "Tiles & Tactics, 2017: соло, pass&play, рейтинг, підсвітка заблокованих місць, перегляд полів, список тайлів"}
  - {kind: steam, url: "https://store.steampowered.com/app/648730/Carcassonne_The_River/", note: "DLC The River"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Carcassonne", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Carcassonne+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 70
mechanics: [cell-click, drag-drop-piece, hover-highlight, legal-move-highlight, turn-enforcement, hot-seat, ai-opponent, event-points, goal-counter, field-scaling, leaderboard, save-game, game-settings, +edge-matching, +tile-rotate, +tile-connectors, +connected-placement, +feature-claim-worker, +feature-completion-scoring, +majority-control, +worker-return, +end-game-incomplete-scoring, +discard-unplayable, +blocked-cell-detection, +tile-supply-counter, +scripted-opening-tiles]
proposes: ["+trigger:pattern", "+trigger:placed", "+effect:place", "+effect:rotate", "+effect:give", "+cond:edge_match", "+cond:occupied", "+cond:legal", "+role:tile", "+role:worker", "+role:supply", "+ui:remaining-tiles", "+ui:feature-overlay", "+ui:score-track", "+window:match-setup", "+feature:expansion-toggle", "+axis:turn-structure"]
author: opus
date: 2026-11-02
---

# Carcassonne — тягни тайл, приклади з дотриманням країв, постав міпла й закрий місто раніше за інших

## Суть
Гравці по одному витягують квадратні тайли й прикладають до спільної мапи так, щоб дороги, міста й поля на сусідніх краях збігалися. На щойно покладений тайл можна поставити свого міпла на одну ділянку — дорогу, місто, монастир чи поле — і отримати очки, коли ця ділянка завершиться. Ділянки, що ростуть з різних тайлів, можуть злитися; тоді вирішує більшість міплів.

## Поле і час
- **Спільне поле** без меж: росте від стартового тайла в будь-який бік; клітина = тайл. Кожен тайл має 4 краї (місто / дорога / поле) і внутрішню топологію (як краї зʼєднані всередині).
- Ділянки (features) — графи поверх тайлів: дорога, місто, монастир (1 тайл + 8 сусідів), поле (області між дорогами й містами).
- Хід: витягти тайл → покласти → (необовʼязково) поставити міпла → підрахувати завершені ділянки. Гравці ходять по колу.
- Кінець: коли покладено останній тайл (71 тайл + стартовий); далі фінальний підрахунок.
- Інформація: стос закритий (порядок прихований), але склад тайлів відомий — цифрові версії показують, які лишились.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тайл | tile | 4 краї {city, road, field}, внутрішні зʼєднання, щит (вимпел), монастир | прикладається до мапи з повним збігом країв, 4 повороти |
| Стартовий тайл | static | місто + дорога + поле | центр мапи (з River — заміщується джерелом річки) |
| Стос тайлів | supply | 71 (база) | тягнеться по одному, порядок випадковий |
| Міпл | piece | 7 у грі на гравця (8-й — маркер очок) | ставиться на ділянку щойно покладеного тайла; повертається після підрахунку |
| Розбійник (на дорозі) | piece | роль міпла | володіє дорогою |
| Лицар (у місті) | piece | роль міпла | володіє містом |
| Чернець (у монастирі) | piece | роль міпла | володіє монастирем |
| Селянин (у полі) | piece | лежить; до кінця гри | володіє полем, не повертається |
| Дорога | zone | тайли, кінці | завершена, коли обидва кінці замкнені (перехрестя, місто, монастир, петля) |
| Місто | zone | тайли, вимпели | завершене, коли стіни замкнені з усіх боків |
| Монастир | zone | 1 тайл + 8 сусідів | завершений, коли всі 8 сусідніх клітин зайняті |
| Поле | zone | область, суміжні завершені міста | рахується лише в кінці гри |
| Вимпел (щит) | static | на тайлі міста | +2 (+1 у кінці) до очок міста |
| Трек очок | zone | 0–49, коло | міпл-маркер біжить по колу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(p)` → ТО `custom: «витягти тайл зі стосу»`.
- КОЛИ `input(place(tile, cell, rotation))` → ЯКЩО `adjacent(cell, any_tile)` and `edge_match(tile, всі сусіди)` → ТО `place`; інакше `block`. Кути не зʼєднуються; дорога ↔ дорога, місто ↔ місто, поле ↔ поле.
- КОЛИ `custom: «тайлу нема куди лягти»` → ТО `discard` (вийти з гри або повернути в стос) і витягти новий.
- КОЛИ `placed(tile)` → ЯКЩО `has(p, meeple)` and `not occupied(feature, any_meeple)` (у всій звʼязній ділянці, а не лише на тайлі) → ТО гравець може `place(meeple, feature_on_tile)`.
- Ділянка може стати спільною: два окремо зайняті шматки злилися новим тайлом — легально, бо міпл ставили, коли вони були окремі.
- КОЛИ `pattern(road_closed)` → ТО власники `score(+1 × тайл)`; міплі повертаються.
- КОЛИ `pattern(city_closed)` → ТО `score(+2 × тайл + 2 × вимпел)`; міплі повертаються.
- КОЛИ `pattern(cloister_surrounded)` → ТО `score(+9)`; чернець повертається.
- Більшість: очки отримує той, хто має **найбільше** міплів у ділянці; при рівності — усі рівні отримують повні очки; решта — нічого.
- КОЛИ `custom: «покладено останній тайл»` → ТО `game_over` і фінальний підрахунок:
  - незавершена дорога `score(+1 × тайл)`; незавершене місто `score(+1 × тайл + 1 × вимпел)`; незавершений монастир `score(+1 + сусіди)`;
  - поле: `score(+3 × кожне завершене місто, що межує з полем)` власникам більшості селян; поле без завершених міст — 0.
- Підрахунок ділянки — одразу в тому ж ході, тож міпл може повернутися й одразу бути поставлений наступним ходом.
- River (міні-доповнення): 12 тайлів річки замінюють стартовий і викладаються першими (джерело → гирло), річка не може робити різкого розвороту (?) — потім звичайний стос.
- Перемога: більше очок.

## Керування і ввід
- Тайл видно в «руці»; поворот (клік/клавіша/жест) і drag на мапу; підсвічені клітини, де цей тайл лягає хоча б в одному повороті; невідповідні повороти недоступні.
- Після підтвердження — вибір ділянки для міпла: підсвічені ділянки тайла, вільні від чужих міплів; кнопка «без міпла».
- Камера: pan/zoom мапи, бо поле необмежене.
- Підрахунок автоматичний, з анімацією очок.

## Вікна, меню, HUD
(цифрова версія — Tiles & Tactics/Steam, BGA)
- `main-menu`: Соло (проти AI) · Pass & Play · Онлайн (публічні, приватні за запрошенням, рейтингові) · Доповнення · Налаштування.
- `match-setup`: гравці, AI, увімкнені доповнення (River, Inns & Cathedrals, Traders & Builders, Princess & Dragon, Winter, The Abbot).
- `lobby-window` + `chat-box` (онлайн).
- `game-screen`: мапа з `zoom-control`; поточний тайл у руці з кнопкою повороту; `legal-move-highlight` місць; `remaining-tiles` — список тайлів, що лишились у стосі (Tiles & Tactics); `feature-overlay` / «field view» — підсвітка полів і хто ними володіє; підсвітка **заблокованих** клітин, куди вже жоден тайл не стане; `score-track` гравців; `remaining-counter` міплів кожного гравця; `turn-indicator`.
- `end-screen`: фінальний підрахунок по типах ділянок.
- `leaderboard` (рейтингові ігри).
- Переходи: main-menu → match-setup → game-screen → end-screen → main-menu.

## Фічі поза полем
- `ai-opponent-levels` (?), `hotseat`, `online-multiplayer`, `leaderboard-online` (ranked), `chat`, асинхронна гра зі сповіщеннями про хід (Steam Turn Notifications) — `turn-timer`.
- `expansion-toggle`: доповнення як DLC, вмикаються перед партією — набір правил як налаштування.
- `rules-page`, `tutorial` (?) — у BGA довідка з правилами.
- Класичні застосунки (iOS, Xbox 360) — історично перші цифрові настолки з онлайн-грою (?).

## Варіації й родичі
- Редакції: 1-ша і 2-га рахували поля інакше (4 за місто на все поле / 3 за місто на кожне поле), маленькі міста з 2 тайлів давали бонус; 3-тя редакція — стандарт.
- Доповнення: Inns & Cathedrals (великий міпл ×2, корчми/собори змінюють очки), Traders & Builders (будівельник = додатковий хід, свиня, товари за більшість), Princess & Dragon (дракон зʼїдає міплів), The Tower, Abbey & Mayor, Bridges, Castles & Bazaars, Hills & Sheep тощо.
- Родичі: Dorfromantik (збіг країв без міплів; є в корпусі), Kingdomino (збіг місцевості), Isle of Skye, Cacao, Hive (необмежене поле).
- **Осі варіацій**: збіг країв (повний / хоча б один / нема) · власність ділянки (міпл-більшість / перший / спільна) · коли рахується (по завершенню / в кінці) · незавершене (половина очок / нуль) · стос (закритий / видно N наступних).

## Цікавинки для курсу
- Ділянки як union-find поверх тайлів із внутрішніми зʼєднаннями (дороги, міста, поля — три окремі графи; поле — вершини «пів-країв») — 🥇 (поле — найскладніша частина).
- Перевірка завершеності дороги/міста (немає відкритих країв) і монастиря (8 сусідів) — 🥉.
- Підсвітка легальних місць для тайла (усі вільні сусідні клітини × 4 повороти × збіг країв) — 📎; «заблоковані клітини» (жоден з тайлів, що лишились, не стане) — 🥉.
- Більшість міплів зі спільною перемогою при рівності — 🌱.
- Фінальний підрахунок полів: поле → множина завершених міст, що його торкаються — 🥈.
- AI: жадібний з оцінкою очок і ризику «не завершиться» — 🥇.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `hover-highlight` · `legal-move-highlight` · `turn-enforcement` · `hot-seat` · `ai-opponent` · `event-points` · `goal-counter` (міплі в запасі) · `field-scaling` (необмежена мапа, зум) · `leaderboard` · `save-game` · `game-settings`.
- **Нема** → пропозиції карток:
  - `+edge-matching` · `+tile-rotate` — як у Dorfromantik; тут повний збіг усіх сусідніх країв.
  - `+tile-connectors` — уже запропоновано в корпусі (зʼєднання країв усередині тайла); тут дороги/міста/поля.
  - `+connected-placement` — як у Sagrada/Kingdomino; тут новий тайл мусить торкатися мапи.
  - `+feature-claim-worker` «Поставити робітника на ділянку» · entities/interact · 🥉 · слоти {only_new_tile: true, free_feature: true}.
  - `+feature-completion-scoring` «Очки при завершенні ділянки» · game-logic/score · 🥉 · слоти {road: 1, city: 2+2, cloister: 9}.
  - `+majority-control` «Більшість фігур у спільній зоні» · game-logic/score · 📎 · слоти {tie: all_score} — родич `+majority-win` (Reversi/Ataxx).
  - `+worker-return` «Робітник повертається після підрахунку» · game-logic/economy · 🌱.
  - `+end-game-incomplete-scoring` «Незавершене рахується в кінці за зниженим тарифом» · game-logic/score · 🌱.
  - `+discard-unplayable` — як у Kingdomino.
  - `+blocked-cell-detection` «Клітини, куди вже нічого не ляже» · levels/solvability · 🥉 — Tiles & Tactics.
  - `+tile-supply-counter` «Список тайлів, що лишились» · interface/hud · 🌱.
  - `+scripted-opening-tiles` «Спершу викладається заданий набір» · game-logic/waves · 🌱 — River.

## Пропозиції до словників
- `+trigger:pattern(road_closed|city_closed|cloister_surrounded)` — розширення ⏳ `pattern` формами «ділянку замкнено».
- `+trigger:placed` — щойно покладено тайл (у корпусі є одна згадка): фаза міпла.
- `+effect:place` · `+effect:rotate` · `+cond:edge_match` — як у сусідах; `+cond:occupied(feature)` — уже ⏳, тут на всю звʼязну ділянку; `+cond:legal`.
- `+effect:give` — уже ⏳: міпл повертається власнику.
- `+role:tile` · `+role:supply` · `+role:worker` — фігура-власник, яка не ходить, а «займає» зону й повертається (міпл, вікінг в Odin) — відрізняється від `piece`.
- `+ui:remaining-tiles` — список/лічильник тайлів у стосі за типами; `+ui:feature-overlay` — підсвітка ділянок (поля, міста) з власниками; `+ui:score-track` — кругова доріжка очок.
- `+window:match-setup` — як у Blokus; `+feature:expansion-toggle` — доповнення як перемикачі правил перед партією.
- `+axis:turn-structure` = `round-robin`.

## Джерела
- ⭐ [Wikipedia: Carcassonne](https://en.wikipedia.org/wiki/Carcassonne_(board_game)) — правила 3-ї редакції (фази, міплі, очки, поля, більшість), відмінності редакцій, доповнення, цифрові версії, Spiel des Jahres 2001.
- [BGA: Carcassonne](https://en.boardgamearena.com/gamepanel?game=carcassonne) — гра в браузері з чотирма доповненнями.
- [Steam: Carcassonne – Tiles & Tactics](https://store.steampowered.com/app/598810/Carcassonne_Tiles_Tactics/) — режими, заблоковані місця, field view, список тайлів, DLC.
- [Steam: Carcassonne – The River](https://store.steampowered.com/app/648730/Carcassonne_The_River/) — DLC річки.
- BGG: пошук «Carcassonne»; YouTube: пошук «Carcassonne how to play».

## Непевне
- (?) Правило River «не можна двічі поспіль повертати в один бік» — з памʼяті.
- (?) Підсвітка легальних місць, підказки й рівні AI у цифрових версіях — Steam-опис їх не згадує (лише «blocked locations detected», field view, список тайлів); BGA-інтерфейс не перевірений.
- (?) Чи тайли в цифровій версії показують «наступний тайл» заздалегідь — не перевірено.
