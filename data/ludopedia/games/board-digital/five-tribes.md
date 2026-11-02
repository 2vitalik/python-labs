---
title: Five Tribes
slug: five-tribes
family: board-digital
also: [chess-abstract]
klass: cursor
axes:
  field: square
  time: turn
  opponent: online
  info: partial
  random: both
  goal: score
year: 2014
platforms: [board, web]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/five-tribes/game-rules.php", best: true, note: "покроковий хід: ставка, рух міплів, контроль плитки, дії племен і плиток, кінець, рахунок"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=fivetribes", note: "грати в браузері (BGA), 2–4"}
  - {kind: official, url: "https://www.daysofwonder.com/game/fives-tribes-the-djinns-of-naqala/", note: "Days of Wonder: склад коробки, 22 джини, рулбуки"}
  - {kind: other, url: "https://cdn.svc.asmodee.net/production-daysofwonder/uploads/2024/07/8401-FT-Rules-EN.pdf", note: "офіційні правила EN (PDF)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Five_Tribes_(board_game)", note: "огляд, розширення"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Five+Tribes", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Five+Tribes+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 55
mechanics: [cell-click, hover-highlight, legal-move-highlight, turn-enforcement, hot-seat, ai-opponent, event-points, round-currency, no-moves-left, piece-capture, game-settings, +mancala-sowing, +last-piece-action, +tile-control-on-empty, +turn-order-auction, +drafting-market, +set-collection-scoring, +majority-bonus, +area-multiplier-income, +ranged-kill, +power-cards, +end-on-last-marker, +tile-action]
proposes: ["+effect:sow", "+effect:place", "+effect:draft", "+effect:kill", "+cond:same", "+cond:afford", "+cond:not_reverse", "+trigger:last_drop", "+role:supply", "+role:card", "+ui:sow-path", "+ui:bid-track", "+ui:card-row", "+ui:opponent-boards", "+window:card-zoom", "+window:match-setup", "+axis:turn-structure", "+card:mancala-sowing", "+card:last-piece-action", "+card:turn-order-auction"]
author: opus
date: 2026-11-02
---

# Five Tribes — манкала на сітці 5×6: підбери всіх міплів з плитки, розсій по одному, останній колір визначає дію

## Суть
Поле — 30 плиток 5×6, на кожній по 3 випадкові міпли пʼяти кольорів (племен). Хід: береш **усіх** міплів з однієї плитки й «сієш» по одному на кожну наступну плитку шляху (як у манкалі), але останній мусить упасти туди, де вже є міпл того самого кольору. Потім забираєш з фінальної плитки всіх міплів цього кольору й виконуєш дію племені (вбивці, старійшини, купці, будівельники, візирі) плюс дію самої плитки; спорожнив плитку — вона твоя (верблюд). Порядок ходу щораунду купується ставкою золота. Ядро — пошук шляху, де «довжина = кількість міплів» і кінцева умова кольору.

## Поле і час
- 30 плиток у прямокутнику 5×6, кожна має тип (село, базар малий/великий, оаза, священне місце), вартість у ПО і колір цінності (синій — 12 плиток: села й священні місця; червоний — 18: базари й оази).
- Шари клітини: плитка (тип, ПО) · міпли (мультимножина кольорів) · верблюд власника · пальми/палаци.
- Сусідство ортогональне; шлях без діагоналей, без негайного повернення назад; петлі дозволені, якщо міплів вистачає.
- Раунд: ставка за порядок → кожен гравець по черзі виконує повний хід → поповнення рядів карт. Кінець — коли хтось поставив останнього верблюда або нема легального руху.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка | zone | тип, ПО, синя/червона цінність | несе міплів; дія плитки для того, хто закінчив на ній хід |
| Мiпл жовтий (візир) | resource | 16 шт. | забирається гравцю; 1 ПО + 10 ПО за кожного суперника, в кого їх строго менше |
| Мiпл білий (старійшина) | resource | 20 шт. | забирається гравцю; 2 ПО; платіж за джина |
| Мiпл зелений (купець) | resource | 18 шт. | у мішок; беру стільки карт товару з початку ряду |
| Мiпл синій (будівельник) | resource | 18 шт. | у мішок; золото = синіх плиток у 3×3 навколо × кількість будівельників |
| Мiпл червоний (вбивця) | resource | 18 шт. | у мішок; вбити 1 міпла в межах N клітин або візира/старійшину в руці суперника |
| Верблюд | object | 8 на гравця (2 гравці — 11) | позначає контроль плитки назавжди |
| Пальма | object | 12 | на оазі; 3 ПО власнику плитки |
| Палац | object | 10 | у селі; 5 ПО власнику плитки |
| Карта товару | supply | 9 видів (ivory, jewels, gold … fish, wheat, pottery) (?) | збирається сетами різних; продаж за 1/3/7/13/21/30/40/50/60 |
| Факір (у 1-му виданні «раб») | supply | карти в ряду ресурсів | скидається для +1 до дальності/множника або замість старійшини |
| Джин | supply | 22 карти; ПО + здатність | ряд із 3; купується на священному місці |
| Маркер порядку | object | 1 на гравця (2 гравці — 2) | трек ставок і трек порядку ходу |
| Золото | resource | старт 50, приховано | ставки, базари; 1 ПО за монету |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(round)` → ТО за порядком треку ставок кожен `input(bid(slot))` → `currency(-cost(slot))`; хто дорожче — ходить раніше; на «0» можуть стояти до 3 маркерів.
- КОЛИ `input(pick(tile))` → ЯКЩО `count(meeples_on(tile), >=, 1)` → ТО `take(all_meeples)` у руку.
- КОЛИ `input(step(next_tile))` → ЯКЩО `adjacent(next_tile)` ортогонально and `not_reverse` → ТО `sow(1 meeple, next_tile)`.
- КОЛИ `last_drop` → ЯКЩО `occupied(tile, same_color(meeple))` → ТО хід легальний; інакше `block` (`custom: «останній міпл — лише туди, де є його колір»`).
- КОЛИ `last_drop(tile, color)` → ТО `take(all meeples of color from tile)` у руку.
- КОЛИ `count(meeples_on(tile), ==, 0)` після забору → ЯКЩО `custom: «плитка нічия»` → ТО `place(camel, tile)` — контроль назавжди.
- Дія племені (за кольором зібраних): жовті/білі — `give(player)`; зелені — `draft(n cards from row start)`; сині — `currency(+blue_tiles_3x3 × n)`; червоні — `custom: «kill: міпл у радіусі n ортогонально або візир/старійшина суперника»` → ЯКЩО плитка спорожніла → `place(camel)`.
- Дія плитки (необовʼязкова, крім позначених): оаза — `place(palm)` (обовʼязково); село — `place(palace)` (обовʼязково); малий базар — `currency(-3)`, 1 з перших 3 карт; великий — `currency(-6)`, 2 з перших 6; священне місце — 2 старійшини або старійшина+факір → `draft(djinn)`.
- Факір: `custom: «скинь → +1 до дальності вбивці / множника будівельників / замінник старійшини»`.
- Джин: `custom: «постійна або платна здатність, раз на хід»` + ПО в кінці.
- КОЛИ `custom: «продаж товарів»` → ТО сет різних товарів → `currency(1/3/7/13/21/30/40/50/60)`; факіри не продаються.
- КОЛИ `custom: «хтось поставив останнього верблюда»` → ТО раунд дограють, `game_over`.
- КОЛИ `no_moves(player)` → ТО він і наступні не рухають міплів (джинів можна), `game_over` після раунду.
- Рахунок: золото 1 · візир 1 + 10 за кожного, в кого менше · старійшина 2 · джини за картою · пальма 3 · палац 5 · ПО власних плиток · товари за сетами. Нічия — спільна перемога.

## Керування і ввід
- Цифрова версія (BGA): клік по плитці-джерелу → клік по сусідніх плитках по одному кроку (або вибір готового шляху з підсвіченого), гра показує лише кінцеві клітини, де лежить потрібний колір.
- Окремі кроки: вибір ставки на треку, вибір цілі вбивці, вибір карт з ряду, оплата старійшинами/факірами, активація джина.
- Порядок ходу змінюється щораунду (ставки), не по колу.

## Вікна, меню, HUD
(цифрова версія — BGA)
- `match-setup`: 2–4 гравці, таймер, розширення (?).
- `game-screen`: поле 5×6 з міплами, верблюдами, пальмами, палацами; `bid-track` — трек ставок і трек порядку; `card-row` — 9 карт ресурсів і 3 джини; панелі гравців з візирами, старійшинами, золотом, джинами; `sow-path` — підсвічений шлях і клітини, де можна закінчити; `turn-indicator`.
- `card-zoom` (кандидат): збільшений джин із здатністю.
- `end-screen`: таблиця рахунку по 8 категоріях.
- `help-window`: довідка по племенах, плитках і джинах.
- Переходи: match-setup → game-screen (раунди) → end-screen.

## Фічі поза полем
- `online-multiplayer` (BGA), `turn-timer`, асинхронна гра.
- Розширення: Artisans of Naqala (6-те плем'я, предмети, гори/прірви), Thieves of Naqala, Whims of the Sultan (5-й гравець, міста із завданнями).
- Перевидання 2024 «The Djinns of Naqala»: «раби» перейменовані на «факірів» (?).
- Цифровий застосунок Days of Wonder (iOS/Android/PC) (?) — у Steam-пошуку не знайдено.

## Варіації й родичі
- Манкала (Овари, Калах) — пряме джерело «сівби» по одному; тут на 2D-сітці з вільним вибором напрямку.
- Родичі: Trajan (манкала як вибір дії), Mancala-плитки в Five Tribes-подібних, Kingdomino (контроль плиток), Tiny Towns.
- **Осі варіацій** сівби: 1D-коло (класична манкала) / 2D-сітка з вибором напрямку · дозволені повернення/петлі · умова кінця шляху (той самий колір / порожня лунка / будь-де) · що дає кінцева лунка (захоплення / дія / ще хід).

## Цікавинки для курсу
- Манкала-рух на сітці: перелік усіх шляхів довжини N без розвороту з кінцевою умовою кольору — 🥈 (DFS з обмеженням + підсвітка легальних кінців).
- «Останній камінь визначає дію» — таблиця дій за кольором — 📎.
- Контроль плитки «спорожнив — став верблюда» — 🌱.
- Будівельники: сума за сусідством 3×3 × множник — 📎.
- Ставка за порядок ходу з ціною слотів — 🥉 (аукціон + переупорядкування черги).
- Сети товарів 1/3/7/13… — 🌱 (таблиця трикутних-подібних сум).
- AI, що оцінює всі легальні ходи раунду (сотні шляхів × дії) — 🥇.

## Мапа на каталог
- Є: `cell-click` · `hover-highlight` · `legal-move-highlight` (кінці шляху) · `turn-enforcement` · `hot-seat` · `ai-opponent` · `event-points` · `round-currency` (золото) · `no-moves-left` · `piece-capture` (вбивця) · `game-settings`.
- **Нема** → пропозиції карток:
  - `+mancala-sowing` «Сівба: підбери всіх і розклади по одному» · entities/move · 🥈 · слоти {grid: 1d|2d, no_reverse: bool}.
  - `+last-piece-action` «Останній покладений визначає дію» · entities/interact · 📎.
  - `+tile-control-on-empty` «Спорожнив клітину — вона твоя» · game-logic/score · 🌱.
  - `+turn-order-auction` «Ставка за порядок ходу» · game-logic/opponent · 🥉 · слот {slots: costs}.
  - `+drafting-market` (як Azul/Sagrada) — ряд карт ресурсів і джинів.
  - `+set-collection-scoring` «Сети різних карт за таблицею» · game-logic/score · 🌱.
  - `+majority-bonus` «Бонус за перевагу над кожним суперником» (візирі) · game-logic/score · 🌱.
  - `+area-multiplier-income` «Дохід = сусіди 3×3 × кількість» · game-logic/economy · 📎.
  - `+ranged-kill` «Знищити сутність у радіусі N» · entities/combat · 📎.
  - `+power-cards` «Карти з постійними здатностями» · game-logic/economy · 🥉.
  - `+end-on-last-marker` «Кінець, коли хтось виклав останній маркер» · game-logic/win · 🌱.
  - `+tile-action` «Дія клітини для того, хто закінчив хід на ній» · entities/interact · 📎.

## Пропозиції до словників
- `+effect:sow(path)` — розкласти взяті сутності по одній уздовж шляху (манкала).
- `+trigger:last_drop` — останній елемент сівби покладено (звідси дія).
- `+effect:kill` — прибрати сутність без входу в її клітину (вбивця; на відміну від `piece-capture`).
- `+effect:place` · `+effect:draft` · `+cond:same` · `+cond:afford` · `+cond:not_reverse` (як Labyrinth) · `+role:supply` · `+role:card` (як Onitama: джини).
- `+ui:sow-path` — підсвічений шлях сівби з кінцевими клітинами.
- `+ui:bid-track` — трек ставок/порядку ходу.
- `+ui:card-row` · `+ui:opponent-boards` · `+window:card-zoom` · `+window:match-setup`.
- `+axis:turn-structure` = `auction-order` (нове значення: порядок ходу купується щораунду).
- `+card:mancala-sowing` · `+card:last-piece-action` · `+card:turn-order-auction`.

## Джерела
- ⭐ [UltraBoardGames: Five Tribes rules](https://www.ultraboardgames.com/five-tribes/game-rules.php) — покроковий хід з номерами розділів, дії племен і плиток, кінець, рахунок.
- [BGA: Five Tribes](https://en.boardgamearena.com/gamepanel?game=fivetribes) — Bruno Cathala, Days of Wonder 2014, 2–4 гравці.
- [Days of Wonder: The Djinns of Naqala](https://www.daysofwonder.com/game/fives-tribes-the-djinns-of-naqala/) — склад: 30 плиток, міпли 16/18/18/18/20, 10 палаців, 12 пальм, 54 карти ресурсів, 22 джини; [рулбук EN (PDF)](https://cdn.svc.asmodee.net/production-daysofwonder/uploads/2024/07/8401-FT-Rules-EN.pdf).
- [Wikipedia](https://en.wikipedia.org/wiki/Five_Tribes_(board_game)) — огляд, розширення.
- YouTube: пошук «Five Tribes how to play».

## Непевне
- (?) Чи можна сіяти на порожню плитку: Wikipedia — «кожна плитка шляху вже має міпла», UBG — лише «не можна закінчити на порожній». Також Wikipedia: «не на плитку, що вже отримала міпла цього ходу» проти UBG «петлі дозволені».
- (?) Ціни слотів треку порядку: памʼять — 0,0,0,1,3,5,8,12,18; UBG пише «0–5».
- (?) Значення ПО плиток (≈4–15), склад 9 видів товарів і кількість факірів (памʼять: 36 товарів + 18 рабів/факірів) — PDF не прочитався.
- (?) Конкретні джини (напр. Haurvatat — пальми по 5) і їхні ПО — з памʼяті, не наведено.
- (?) Цифровий застосунок Days of Wonder і його платформи — не перевірено.
