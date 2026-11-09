---
title: Ticket to Ride
slug: ticket-to-ride
aka: [Zug um Zug, Les Aventuriers du Rail, TTR, Квиток на потяг]
family: board-digital
also: [connect-rotate]
klass: cursor
axes:
  field: graph
  time: turn
  opponent: hotseat
  info: partial
  random: both
  goal: score
year: 2004
platforms: [board, web, PC, Mac, iOS, Android, Xbox, PlayStation, Switch]
links:
  - {kind: other, url: "https://ncdn0.daysofwonder.com/tickettoride/en/img/tt_rules_2015_en.pdf", best: true, note: "офіційні правила (Days of Wonder, 2015): склад, 3 дії, локомотиви, сірі й подвійні маршрути, таблиця очок, кінець гри, тай-брейк"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ticket_to_Ride_(board_game)", note: "усі версії й мапи, таблиця очок до 10 вагонів, бонуси, доповнення, нагороди"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ticket_to_Ride_(video_game)", note: "цифрові версії: браузер 2004, PC/Mac 2006, XBLA 2008, iPad 2011, Android 2013, Marmalade 2023"}
  - {kind: other, url: "https://www.ultraboardgames.com/ticket-to-ride/game-rules.php", note: "переказ правил базової гри"}
  - {kind: other, url: "https://www.ultraboardgames.com/ticket-to-ride/europe.php", note: "Europe: тунелі, пороми, станції, European Express, довгі квитки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ticket+to+Ride+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 70
mechanics: [hot-seat, pass-device, ai-opponent, difficulty-levels, online-multiplayer, async-multiplayer, connectivity-check, event-points, rule-variants, pocket, main-menu, match-setup, lobby-window, tutorial-window, game-screen, end-screen, shop-window, achievements-window, leaderboard, +deck-draw, +drafting-market, +market-wild-reset, +wildcard-tile, +claim-edge-by-set, +parallel-edge-lock, +secret-objective, +draft-keep-at-least, +longest-path-scoring, +last-round-trigger, +tiebreak-chain, +discard-reshuffle, +tunnel-risk-cost, +ferry-wild-quota, +station-borrow-edge]
proposes: ["+effect:draw_card", "+effect:discard", "+trigger:deck_empty", "+role:card", "+ui:card-hand", "+ui:card-market", "+window:keep-choice", "+card:claim-edge-by-set", "+card:longest-path-scoring"]
author: opus
date: 2026-11-09
---

# Ticket to Ride — граф залізниць: набір карт одного кольору захоплює ребро між містами, таємні квитки вимагають зʼєднати пари міст

## Суть
Гравці будують залізниці на мапі-графі: місто — вершина, маршрут — ребро з довжиною й кольором. За хід робиш рівно одну з трьох дій: береш дві карти вагонів, захоплюєш один маршрут набором карт його кольору або береш нові квитки-цілі. Очки дають захоплені ребра (довше — вигідніше, нелінійно), виконані таємні квитки (невиконані — мінус) і найдовший неперервний шлях. Гра закінчується, коли в когось лишилось ≤2 вагонів.

## Поле і час
- Поле — граф: міста (вершини) і маршрути між сусідніми містами (ребра). Ребро складається з 1–6 клітин-вагонів (USA); у мапах інших версій — до 10. Колір ребра — один із 8 або сірий (будь-який один колір).
- Мультиребра: деякі пари міст мають подвійний маршрут (два паралельні ребра, часто різних кольорів).
- Трек очок іде по краю мапи; маркер кожного гравця рухається при кожному нарахуванні.
- Час — покроковий, по черзі за годинниковою стрілкою; хід = рівно одна дія.
- Інформація часткова: рука карт і квитки приховані; ринок із 5 відкритих карт і всі захоплені ребра видно всім. Випадковість — тасування колод (setup) і добір наосліп (runtime).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Місто | static | назва | вершина графа; нікому не належить |
| Маршрут | zone | довжина 1–6, колір або сірий | вільний → захоплює один гравець; вагони гравця на кожній клітині |
| Подвійний маршрут | zone | два паралельні ребра | один гравець не бере обидва; у грі на 2–3 після першого друге закрите |
| Вагон гравця | piece | 45 на гравця | по одному на клітину маршруту; запас ≤2 запускає кінець гри |
| Карта вагона ×8 кольорів | object | по 12 кожного кольору | у руці; набір одного кольору = довжина ребра |
| Локомотив | object | 14 карт, джокер | замінює будь-який колір; з ринку — лише як єдина карта ходу |
| Ринок | supply | 5 відкритих карт | взяту карту одразу доповнюють з колоди; ≥3 локомотиви → скинути всі 5, відкрити нові |
| Колода й скид вагонів | supply | 110 карт разом | колода вичерпалась → перетасувати скид |
| Квиток | object | 2 міста + очки; 30 карт | таємна ціль: зʼєднав своїми ребрами → +очки, ні → −очки |
| Колода квитків | supply | — | повернені квитки — під низ |
| Маркер очок | mark | 1 на гравця | рухається треком по краю мапи |
| Карта Longest Path | object | +10 | найдовшому неперервному шляху наприкінці |
| Станція (Europe) | piece | 3 на гравця; ціна 1/2/3 карти | дозволяє взяти для квитків одне чуже ребро з цього міста; невикористана — 4 очки |
| Тунель (Europe) | zone | довжина, колір | після оплати відкриваються 3 карти колоди; збіги вимагають доплати |
| Пором (Europe) | zone | N символів локомотива | кожен символ — обовʼязковий локомотив у наборі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «кожному 4 карти вагонів; 5 верхніх карт — на ринок; кожному 3 квитки»`, `choose(keep ≥ 2 з 3 квитків)`; повернені — `custom: «під низ колоди квитків»`.
- КОЛИ `turn_start(player)` → ТО `choose(draw_cards | claim_route | draw_tickets)` — рівно одна дія за хід.
- Дія 1. КОЛИ `input(take_card)` → ЯКЩО `custom: «перша карта ходу — локомотив з ринку»` → ТО `custom: «взяти»` (`+effect:draw_card`), `end_turn`; інакше `custom: «взяти карту з ринку чи наосліп з колоди, потім другу»`.
- КОЛИ `input(take_card)` → ЯКЩО `custom: «друга карта ходу»` і `custom: «на ринку обрано локомотив»` → ТО `block`; локомотив, узятий наосліп з колоди, — звичайна карта, другу брати можна.
- КОЛИ `after(take_from_market)` → ТО `custom: «відкрити заміну з колоди»`; ЯКЩО `custom: «заміна — локомотив, а гравець бере другу карту»` → ТО `block` для цієї карти.
- КОЛИ `counter(face_up_locomotives, >=, 3)` → ТО `custom: «скинути всі 5 карт ринку, відкрити 5 нових»` (`+effect:discard`).
- КОЛИ `custom: «колода вагонів порожня»` (`+trigger:deck_empty`) → ТО `custom: «перетасувати скид у нову колоду»`; ЯКЩО `custom: «скид теж порожній»` → ТО `block` для дії 1 (лишаються дії 2 і 3).
- Дія 2. КОЛИ `input(claim, route)` → ЯКЩО `free(route)` і `has(player, trains ≥ length)` і `custom: «набір з length карт одного кольору ребра; локомотиви — будь-який колір; сіре ребро — будь-який один колір»` → ТО `place(player, train × length)`, `score(table[length])`, `custom: «набір — у скид»`.
- Таблиця очок (USA): 1 → 1, 2 → 2, 3 → 4, 4 → 7, 5 → 10, 6 → 15; у мапах інших версій 7 → 18, 8 → 21, 9 → 27, 10 → 40.
- Ребро можна взяти будь-де, не обовʼязково поруч зі своїми; максимум одне ребро за хід.
- КОЛИ `input(claim, twin_route)` → ЯКЩО `custom: «цей гравець уже має паралельне ребро тієї ж пари міст»` → ТО `block`.
- КОЛИ `custom: «захоплено одне з подвійних ребер»` → ЯКЩО `count(players, <=, 3)` → ТО `set_state(twin_route, closed)` для всіх.
- Дія 3. КОЛИ `input(draw_tickets)` → ТО `custom: «взяти 3 верхні квитки (менше, якщо в колоді менше)»`, `choose(keep ≥ 1)`, решта — під низ; квитків у руці може бути скільки завгодно.
- Карт у руці — без ліміту.
- Кінець. КОЛИ `turn_end(player)` → ЯКЩО `count(own_trains, <=, 2)` → ТО `custom: «кожен гравець, включно з цим, робить ще один хід»`, потім `game_over`.
- КОЛИ `game_over` → ТО `reveal(tickets)`; для кожного квитка ЯКЩО `path_exists(city_a, city_b)` (лише по власних ребрах) → ТО `score(+value)`; інакше `score(−value)`.
- КОЛИ `game_over` → ТО `custom: «знайти найдовший неперервний шлях з власних вагонів: петлі й повторні міста дозволені, кожен вагон — не більше одного разу»` → `score(+10)` кожному з тих, хто ділить перше місце.
- Перемога: найбільше очок · нічия → більше виконаних квитків → власник Longest Path · Поразка: — · Рахунок: ребра (під час гри) + квитки ± + бонус.
- Europe, тунель: КОЛИ `input(claim, tunnel)` → ТО `custom: «зіграти набір, потім відкрити 3 верхні карти колоди»`; за кожну відкриту того ж кольору або локомотив ЯКЩО `has(player, extra_card)` → ТО `custom: «доплатити 1 карту того ж кольору чи локомотив»`; інакше `custom: «забрати набір назад»`, `end_turn`. Якщо набір лише з локомотивів — доплата тільки за відкриті локомотиви; 3 відкриті — у скид.
- Europe, пором: КОЛИ `input(claim, ferry)` → ЯКЩО `custom: «у наборі є по локомотиву на кожен символ ребра»` → ТО як звичайне ребро; інакше `block`.
- Europe, станція: КОЛИ `input(build_station, city)` → ЯКЩО `not occupied(city, station)` і `custom: «ціна: 1-ша — 1 карта, 2-га — 2 однакові, 3-тя — 3 однакові»` → ТО `place(player, station)`; одна станція за хід.
- КОЛИ `game_over` → ЯКЩО `custom: «у місті є станція гравця»` → ТО `custom: «для квитків дозволено одне чуже ребро з цього міста, одне й те саме для всіх квитків»`; за кожну невикористану станцію `score(+4)`.
- Europe: бонус European Express (+10) рахує лише власні вагони, без станцій і чужих ребер; тай-брейк — квитки → менше використаних станцій → European Express. Старт: 1 довгий квиток з 6 + 3 звичайні (тримати ≥2).

## Керування і ввід
- Настільна: взяти карту з ринку/колоди, викласти набір карт і вагони на ребро, взяти й переглянути квитки.
- Цифрові версії: клік по карті ринку або колоді; клік по ребру → вибір набору, якщо підходить кілька кольорів; квитки — вибір позначками з мінімумом і кнопкою підтвердження.
- Черга ходів: hot-seat, pass-and-play (iPad), онлайн; на iOS з 2015 — асинхронна й кросплатформна гра.

## Вікна, меню, HUD
(цифрова версія; функції — з Wikipedia про відеогру, макет — типовий)
- `main-menu`: Соло проти ботів · Онлайн · Pass & Play · Навчання · Магазин мап.
- `match-setup`: 2–5 гравців, боти (у PC-версії 2006 — до 4 «Robots»), складність, мапа (USA / Europe / DLC), режим (iPad: 3 режими на мапу).
- `tutorial-window`: покрокове навчання (iPad-версію хвалили саме за нього).
- `lobby-window`: онлайн-партії, асинхронні ігри.
- `game-screen`: мапа-граф із зумом; ринок 5 карт і колода (`card-market`); рука, згрупована за кольорами (`card-hand`, `pocket`); квитки гравця з позначкою «виконано»; HUD — `score` на треку, `remaining-counter` вагонів кожного гравця, `turn-indicator`, кількість карт і квитків у руках суперників; `path-preview` маршруту квитка.
- `keep-choice` (`custom-window`): вибір квитків з 3 з мінімумом 1 (на старті — 2).
- `end-screen`: покроковий фінальний підрахунок (ребра, квитки ±, Longest Path), переможець.
- `shop-window`: мапи як DLC; `achievements-window` (Xbox-досягнення, 69 трофеїв PS); `leaderboard` (XBLA).
- Переходи: main-menu → match-setup → game-screen → keep-choice (старт) → game-screen ↔ keep-choice (дія 3) → end-screen.

## Фічі поза полем
- `ai-opponent-levels`: «Robots» у PC-версії 2006, змінна складність на Xbox, «адаптивні» боти Marmalade (2023).
- `online-multiplayer` (на PC/Mac класичної версії вимкнено у 2024), асинхронна гра й cross-play (iOS 2.0, 2015), `hotseat` / pass-and-play, локальна мережа (iPhone).
- `achievements`, `leaderboard-online` (Xbox), `tutorial`.
- `custom-rules` як набір мап: кожна мапа-DLC — свої правила (тунелі, пороми, станції, кораблі).
- Alexa-скіл (2019) з фізичною коробкою — гра проти голосового асистента.

## Варіації й родичі
- Окремі версії з новими правилами: Europe (тунелі, пороми, станції), Märklin, Switzerland і Nordic Countries (локомотив з ринку без обмеження «одна карта»), Germany, Rails and Sails (кораблі; 3 карти вагонів + 7 карт кораблів; кінець при <7 вагонів і кораблів разом), First Journey (дитяча), міські мапи (New York, London, Amsterdam… — 2 стартові карти).
- Бонуси наприкінці різняться за версією: Longest Path 10, «найбільше виконаних квитків» 10 або 15, у деяких версіях бонусу нема.
- **Осі варіацій**: ціна ребра (набір кольору / сірий — будь-який колір / тунель з ризиком доплати / пором з обовʼязковими джокерами) · ціль (таємні квитки / найдовший шлях / найбільше квитків) · доступ до чужих ребер (нема / станція) · обмеження ринку на джокер (одна карта / без обмеження) · тригер кінця (вагонів ≤2 / вагонів і кораблів <7).
- Родичі: TransAmerica (`transamerica.md`, одна спільна мережа замість власних ребер), Next Station London (`next-station-london.md`, лінії метро між станціями), Catan (`catan.md`, дороги на ребрах і «найдовша дорога»), Copenhagen (`copenhagen.md`, дві карти з ринку), Patchwork (`patchwork.md`, бонус першому).

## Цікавинки для курсу
- Мапа як граф з мультиребрами, довжиною й кольором; рендер ребра ланцюжком клітин між містами — 🥉 (структура даних + відмалювання).
- Ринок 5 карт: заміна з колоди, правило локомотива «перша й єдина», скидання при ≥3 локомотивах — 📎.
- Перевірка квитка: BFS / union-find лише по ребрах гравця — 📎.
- Найдовший шлях без повторення ребер, з петлями: DFS-перебір по ребрах (у загальному випадку задача складна) — 🥇.
- Тунель: доплата за відкритими 3 картами, відмова — повернення набору — 🌱.
- Станції: у пошуку шляху дозволено одне позичене чуже ребро на станцію, однакове для всіх квитків; оптимальний вибір — перебір — 🥈.
- Бот: обрати квитки, прокласти найдешевші шляхи (Дейкстра за довжиною ребер), вирішити — брати карти чи блокувати — 🥈.
- Тригер кінця «ще одне коло всім» — 🌱.

## Мапа на каталог
- Є: `hot-seat` · `pass-device` ↔ pass-and-play · `ai-opponent` / `difficulty-levels` ↔ боти · `online-multiplayer` · `async-multiplayer` ↔ асинхронні партії iOS · `connectivity-check` ↔ квиток виконано · `event-points` ↔ таблиця очок за довжину · `rule-variants` ↔ версії й мапи · `pocket` ↔ рука · `main-menu`, `match-setup`, `lobby-window`, `tutorial-window`, `game-screen`, `end-screen`, `shop-window`, `achievements-window`, `leaderboard`.
- **Нема** → пропозиції карток:
  - `+claim-edge-by-set` «Захоплення ребра графа набором карт кольору» · entities/legality · 📎 · слоти {length, color|any}.
  - `+longest-path-scoring` «Бонус за найдовший шлях без повтору ребер» · game-logic/score · 🥇 — уже пропоноване корпусом.
  - `+parallel-edge-lock` «Подвійне ребро: одне на гравця, закрите при малій кількості гравців» · entities/legality · 🌱 · слот {min_players}.
  - `+drafting-market` / `+market-wild-reset` «Відкритий ринок з доповненням і скиданням при N джокерах» · game-logic/economy · 📎 · слоти {size: 5, wild_reset: 3}.
  - `+secret-objective` / `+draft-keep-at-least` «Таємні цілі: взяти N, лишити ≥K; невиконана — мінус» · game-logic/score · 📎.
  - `+tunnel-risk-cost` · `+ferry-wild-quota` · `+station-borrow-edge` «Ризикова доплата / обовʼязкові джокери / позичене ребро» · entities/legality · 🌱 / 🌱 / 🥈.
  - `+deck-draw`, `+wildcard-tile`, `+last-round-trigger`, `+tiebreak-chain`, `+discard-reshuffle` — уже пропоновані корпусом.

## Пропозиції до словників
- `+effect:draw_card(deck|market, n)` — тягнути карту з колоди чи ринку (`draw` у словнику — нічия).
- `+effect:discard(cards)` — карти в скид (набір після захоплення, ринок при 3 локомотивах).
- `+trigger:deck_empty(deck)` — колода вичерпалась (перетасувати скид).
- `+role:card` — карта в руці, ринку чи колоді (вагони, квитки), не плитка поля.
- `+ui:card-hand` — рука, згрупована за кольором з кількістю; `+ui:card-market` — ряд відкритих карт ринку з колодою поруч.
- `+window:keep-choice` — вибір K з N карт з мінімумом (квитки).
- `+card:claim-edge-by-set` · `+card:longest-path-scoring` — див. «Мапа на каталог».

## Джерела
- ⭐ [Правила Ticket to Ride (Days of Wonder, PDF 2015)](https://ncdn0.daysofwonder.com/tickettoride/en/img/tt_rules_2015_en.pdf) — склад (45 вагонів, 110 карт: 8×12 + 14 локомотивів, 30 квитків), 3 дії, локомотиви, сірі й подвійні маршрути, таблиця 1–6, кінець при 0–2 вагонах, Longest Path, тай-брейк.
- [Wikipedia: Ticket to Ride (board game)](https://en.wikipedia.org/wiki/Ticket_to_Ride_(board_game)) — версії й мапи, стартові руки, таблиця до 10 вагонів, бонуси, Europe-механіки, доповнення, нагороди (Spiel des Jahres 2004), Alan R. Moon.
- [Wikipedia: Ticket to Ride (video game)](https://en.wikipedia.org/wiki/Ticket_to_Ride_(video_game)) — платформи, роки, боти, онлайн, асинхронна гра, DLC-мапи, досягнення.
- [UltraBoardGames: rules](https://www.ultraboardgames.com/ticket-to-ride/game-rules.php) — переказ базових правил.
- [UltraBoardGames: Europe](https://www.ultraboardgames.com/ticket-to-ride/europe.php) — тунелі, пороми, станції (1/2/3 карти, 4 очки), European Express, 6 довгих квитків, тай-брейк.
- YouTube: пошук «Ticket to Ride how to play».

## Непевне
- (?) Регіональні назви в `aka` (Zug um Zug, Les Aventuriers du Rail, «Квиток на потяг») — з памʼяті, у відкритих джерелах не бачив.
- (?) Вікна цифрових версій — функції з Wikipedia, конкретні екрани й назви пунктів меню — припущення.
- (?) Бонус «Globetrotter» у переказі Wikipedia описано неоднозначно (найбільше квитків чи мережа від краю до краю) — не вніс як правило.
- (?) Чи «3 локомотиви на ринку» перевіряють після кожної заміни посеред ходу — правила кажуть «at any time», порядок не уточнено.
- (?) `also: [connect-rotate]` — моє тлумачення: ядро «зʼєднати пари міст» близьке до TransAmerica.
