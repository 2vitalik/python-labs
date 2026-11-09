---
title: Catan
slug: catan
aka: [Колонізатори, Die Siedler von Catan, The Settlers of Catan, Settlers]
family: board-digital
also: []
klass: cursor
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: partial
  random: both
  goal: score
year: 1995
platforms: [board, PC, Xbox 360, PS3, Nintendo DS, iOS, Android, Switch, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Catan", best: true, note: "огляд правил, ресурси, розбійник, карти розвитку, доповнення, цифрові версії, нагороди"}
  - {kind: other, url: "https://www.catan.com/sites/default/files/2021-06/catan_base_rules_2020_200707.pdf", note: "офіційні правила й альманах 2020 (3–4 гравці): склад, підготовка, обмін, ціни, розбійник, найдовша дорога"}
  - {kind: official, url: "https://www.catan.com/understand-catan/game-rules", note: "сторінка всіх правил (база, 5–6 гравців, доповнення)"}
  - {kind: other, url: "https://www.ultraboardgames.com/catan/game-rules.php", note: "стислі правила: ціни, правило відстані, ліміти фігур, карти розвитку"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Catan+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 70
mechanics: [hot-seat, turn-enforcement, ai-opponent, online-multiplayer, rule-variants, match-setup, game-screen, end-screen, help-window, settings-window, leaderboard, cell-click, legal-move-highlight, +hex-grid-render, +vertex-edge-placement, +dice-production, +distance-rule, +connected-placement, +upgrade-in-place, +build-cost-recipes, +trade-offer, +maritime-trade-ratio, +blocker-piece, +steal-random-card, +hand-limit-discard, +deck-draw, +hidden-victory-points, +longest-path-scoring, +title-steal-bonus, +snake-setup, +piece-supply-limit, +shortage-no-one-gets, +random-board-setup]
proposes: ["+effect:roll_dice", "+effect:steal", "+effect:discard", "+effect:trade", "+effect:draw_cards", "+role:card", "+role:die", "+window:trade-window", "+ui:dice-result", "+ui:card-hand", "+axis:placement-site", "+card:vertex-edge-placement", "+card:dice-production", "+card:longest-path-scoring"]
author: opus
date: 2026-11-09
---

# Catan — острів із 19 гексів: поселення на вершинах, дороги на ребрах, кидок 2d6 запускає видобуток, на 7 — розбійник

## Суть
3–4 гравці (5–6 з розширенням) заселяють острів із випадково викладених гексів п'яти ландшафтів. Кожен хід кидок 2d6 запускає видобуток: кожен гекс із цим числом дає ресурс власникам сусідніх поселень (1) і міст (2). Ресурси обмінюють між гравцями й з банком і витрачають на дороги, поселення, міста й карти розвитку; перший, хто у свій хід має 10 переможних очок, виграє. Незвичне для сітки: фігури стоять не в клітинах, а на **вершинах** (поселення, міста) і **ребрах** (дороги) гексів. Автор Klaus Teuber, Kosmos.

## Поле і час
- Острів: 19 гексів ландшафту в рамці з 6 частин моря з 9 гаванями; гекси — горби (цегла), ліс (деревина), гори (руда), поля (зерно), пасовище (вовна), пустеля (нічого). Розклад: фіксований для новачків або випадковий.
- 18 жетонів чисел 2–12 без 7 (одна «2», одна «12», решта — по дві: 3, 4, 5, 6, 8, 9, 10, 11) лежать на гексах, крім пустелі; крапки під числом = кількість способів його викинути на 2d6, «6» і «8» червоні.
- Три шари позицій: гекс (видобуток, розбійник) · перехрестя-вершина (поселення / місто; торкається 1–3 гексів) · шлях-ребро (дорога; між двома гексами або гексом і рамкою).
- Хід: кидок → видобуток (або розбійник на 7) → обмін → будування; досвідчені гравці зливають обмін і будування в одну фазу. Хід — за годинниковою стрілкою.
- Інформація часткова: ресурси й карти розвитку в руці закриті (кількість карт видно), колода розвитку закрита, переможні карти розвитку приховані до перемоги.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гекс ландшафту | terrain | тип = ресурс; жетон числа | на кидок свого числа дає ресурс сусідам-вершинам |
| Пустеля | terrain | без числа | нічого не дає; старт розбійника |
| Жетон числа | mark | 2–12 без 7; 18 шт. | який кидок активує гекс |
| Гавань | zone | 9: 5 спеціальних 2:1 (по ресурсу) + 4 загальні 3:1 | поселення / місто на ній дає кращий курс обміну з банком |
| Поселення | piece | 5 на гравця; 1 ПО | на вершині; 1 ресурс з кожного сусіднього гекса на його число |
| Місто | piece | 4 на гравця; 2 ПО | лише замість свого поселення; 2 ресурси з гекса |
| Дорога | piece | 15 на гравця | на ребрі, звʼязана зі своєю мережею; одна дорога на ребро |
| Розбійник | neutral | 1 | стоїть на гексі й блокує його видобуток; рухається на 7 і картою лицаря |
| Карта ресурсу | resource | 95: по 19 цегли, деревини, руди, зерна, вовни | ціна будування й предмет обміну |
| Карта лицаря | card | 14 | перемістити розбійника й пограбувати; лишається відкритою перед гравцем |
| Карта прогресу | card | 6: по 2 Road Building, Year of Plenty, Monopoly | одноразова дія, потім з гри |
| Карта переможного очка | card | 5 | +1 ПО, прихована; можна відкрити в хід купівлі для перемоги |
| Найдовша дорога | pickup | 2 ПО | першому з неперервною дорогою ≥5; довша — відбирає |
| Найбільша армія | pickup | 2 ПО | першому з 3 зіграними лицарями; більше — відбирає |
| Кубики 2d6 | object | сума 2–12 | один кидок на хід |
| Банк | supply | стоси ресурсів, колода розвитку | платить видобуток, приймає ціну й обмін |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «раунд 1 за годинниковою: поселення + сусідня дорога; раунд 2 — у зворотному порядку (останній ставить першим)»` (змійка).
- КОЛИ `after(place(settlement_2))` → ТО `give(player, resource ×сусідні_гекси_другого_поселення)` — стартові ресурси.
- КОЛИ `turn_start(player)` → ТО `custom: «кинути 2d6»` (`+effect:roll_dice`); карту розвитку можна зіграти й до кидка.
- КОЛИ `after(roll_dice)` → ЯКЩО `custom: «сума ≠ 7»` і `not occupied(hex, robber)` і `custom: «жетон гекса = сума»` → ТО `give(owner_of_adjacent_vertex, resource ×1 за поселення / ×2 за місто)`.
- КОЛИ `after(roll_dice)` → ЯКЩО `custom: «у банку не вистачає ресурсу на всіх»` і `count(players_receiving, >, 1)` → ТО `custom: «цей ресурс цього кидка не отримує ніхто»`.
- КОЛИ `after(roll_dice)` → ЯКЩО `custom: «сума = 7»` → ТО ніхто не отримує; для кожного: ЯКЩО `counter(hand, >, 7)` → ТО `custom: «скинути половину, округлено вниз»` (`+effect:discard`).
- КОЛИ `after(discard)` → ТО `move(robber, other_hex)` (будь-який інший гекс або пустеля), `custom: «взяти 1 випадкову карту в гравця з поселенням / містом біля цього гекса; кількох — на вибір»` (`+effect:steal`).
- КОЛИ `input(trade(player_b, offer))` → ЯКЩО `turn_of(player)` і `custom: «одна зі сторін — активний гравець; обидва згодні»` → ТО `custom: «обмін картами»` (`+effect:trade`); неактивні між собою не міняються, однакові ресурси й подарунки заборонені.
- КОЛИ `input(maritime_trade(resource, n))` → ЯКЩО `has(player, resource ×n)` і `custom: «n = 4; 3 — з загальною гаванню; 2 — зі спеціальною цього ресурсу»` → ТО `take(player, resource ×n)`, `give(player, any_resource ×1)`.
- КОЛИ `input(build(road, edge))` → ЯКЩО `has(player, brick + lumber)` і `free(edge)` і `custom: «ребро торкається своєї дороги, поселення або міста»` і `count(road_supply, >, 0)` → ТО `place(player, road)`.
- КОЛИ `input(build(settlement, vertex))` → ЯКЩО `has(player, brick + lumber + wool + grain)` і `free(vertex)` і `custom: «усі 3 сусідні вершини порожні»` (правило відстані) і `custom: «до вершини веде своя дорога»` → ТО `place(player, settlement)`, `score(+1)`.
- КОЛИ `input(build(city, vertex))` → ЯКЩО `has(player, ore ×3 + grain ×2)` і `occupied(vertex, own_settlement)` → ТО `transform(settlement, city)`, `score(+1)` (разом 2); поселення повертається в запас.
- КОЛИ `input(buy_dev_card)` → ЯКЩО `has(player, ore + wool + grain)` і `count(dev_deck, >, 0)` → ТО `give(player, top_dev_card)` (`+effect:draw_cards`); карти розвитку не обмінюють і не дарують.
- КОЛИ `input(play_dev_card)` → ЯКЩО `counter(dev_played_this_turn, ==, 0)` і `not state(card, bought_this_turn)` → ТО ефект карти (VP-карти — винятки: не «граються», відкриваються для перемоги).
- КОЛИ `after(play(knight))` → ТО як на 7: `move(robber, other_hex)`, `custom: «пограбувати сусіда гекса»` (`+effect:steal`) — без скидання.
- КОЛИ `after(play(knight))` → ЯКЩО `counter(knights_played, >=, 3)` і `custom: «більше, ніж у власника карти»` → ТО `give(player, largest_army)`, `score(+2)` власнику / `score(-2)` попередньому.
- КОЛИ `after(play(road_building))` → ТО `place(player, road ×2)` безкоштовно за звичайними правилами.
- КОЛИ `after(play(year_of_plenty))` → ТО `give(player, any_resource ×2)` — можна витратити цього ж ходу.
- КОЛИ `after(play(monopoly))` → ТО `custom: «назвати ресурс; усі інші віддають усі карти цього ресурсу»`.
- КОЛИ `after(place(road))` або `after(place(settlement))` → ЯКЩО `custom: «найдовша неперервна дорога гравця ≥5 і довша за чинного власника (гілки не рахуються)»` → ТО `give(player, longest_road)` (+2 ПО).
- КОЛИ `after(place(settlement))` → ЯКЩО `custom: «поселення стало на чужу дорогу й розірвало її»` → ТО `custom: «перерахувати найдовшу дорогу; при нічиїй між іншими — карту відкласти, доки не буде єдиного лідера ≥5»`.
- КОЛИ `counter(vp, >=, 10)` → ЯКЩО `turn_of(player)` → ТО `win`; досягнуте в чужий хід — гра триває до власного ходу.
- КОЛИ `input(build(x))` → ЯКЩО `count(own_supply(x), ==, 0)` → ТО `block` (5 поселень, 4 міста, 15 доріг — «ні більше, ні менше»).
- Перемога: 10 ПО у свій хід (поселення 1, місто 2, найдовша дорога 2, найбільша армія 2, карта ПО 1) · Поразка: — · Рахунок: переможні очки.

## Керування і ввід
- Настільна: кидок кубиків; обмін — оголосити, що треба, приймати пропозиції й контрпропозиції; будування — заплатити карти в банк і поставити фігуру.
- Курсор по трьох типах позицій: вершина (поселення, місто), ребро (дорога), гекс (розбійник).
- (цифрова версія) Кнопка кидка, підсвітка легальних вершин і ребер з урахуванням правила відстані й ціни (`legal-move-highlight`), панель обміну з пропозиціями іншим гравцям і банку / гавані, `end-turn-button`; AI-суперники; онлайн-лобі.

## Вікна, меню, HUD
(цифрова версія: Catan Universe, Steam, консолі, мобільні)
- `main-menu`: Гра з AI · Онлайн · Hot-seat · Правила · Налаштування.
- `match-setup`: 3–4 (5–6) гравці, AI-суперники, мапа для новачків / випадкова, доповнення, ціль у ПО (?).
- `lobby-window`: онлайн-кімнати, запрошення.
- `game-screen`: гексовий острів з жетонами й гаванями, фігури на вершинах і ребрах, розбійник; `dice-result`; `card-hand` ресурсів і розвитку; `opponent-boards`: кількість карт, ПО, довжина дороги, лицарі; `score` ПО; `turn-indicator`; `message-log` (хто що отримав і збудував); памʼятка цін.
- `trade-window` (`+window:trade-window`): пропозиція «даю / хочу», відповіді гравців, обмін з банком 4:1 / гаванню.
- `confirm-dialog`: скидання половини карт на 7 (вибір карт), вибір жертви пограбування, вибір ресурсу Monopoly / Year of Plenty.
- `end-screen`: переможець, розклад ПО, статистика кидків (`stats-window`).
- `leaderboard` / рейтинг онлайн (?); `settings-window`; `help-window` / `tutorial-window`.
- Переходи: main-menu → match-setup / lobby-window → game-screen ⇄ trade-window → end-screen.

## Фічі поза полем
- `custom-rules`: фіксована мапа для новачків / випадкова; злиття фаз обміну й будування; розширення 5–6 гравців (1996).
- Доповнення: Seafarers (1997: кораблі, морські гекси, сценарії), Cities & Knights (1998), Traders & Barbarians (2008), Explorers & Pirates (2013).
- `ai-opponent-levels`, `online-multiplayer`, `hotseat` — у цифрових версіях: MSN Catan Online (2005), Xbox Live Arcade (2007), PS3 (2008), DS (2009), iOS (2009), Android (2011), Creators Edition на Steam (2013), Catan Universe (2017), Switch (2019).

## Варіації й родичі
- Сценарії доповнень змінюють поле (море, кораблі як дороги на воді), але ядро вершина-ребро-гекс лишається.
- Родичі: Takenoko (`takenoko.md`, гекси з ростом), Through the Desert (`through-the-desert.md`, гекси й ланцюги), Acquire (`acquire.md`, економіка на сітці), Kingdom Builder (`kingdom-builder.md`, розміщення за типом гекса).
- **Осі варіацій**: де стоять фігури (клітини / вершини / ребра) · джерело ресурсу (кубик за числом гекса / вибір / колода) · блокувальник (розбійник / нема) · обмін (вільний з активним / фіксовані курси / нема) · умова перемоги (поріг ПО / кінець раундів).

## Цікавинки для курсу
- Гексова сітка з вершинами й ребрами: координати вершин і ребер, сусідство «вершина ↔ 3 гекси ↔ 3 ребра» — 🥈.
- Найдовша дорога: найдовший шлях без повторення ребер у графі доріг, перерваний чужим поселенням — 🥇 (пошук із поверненням).
- Видобуток за кидком 2d6 з імовірностями (крапки на жетонах) і блоком розбійника — 🌱.
- Правило відстані (жодна сусідня вершина не зайнята) + звʼязність з власною мережею доріг — 📎.
- Розбійник на 7: скидання половини понад 7, переміщення, випадкове пограбування — 📎.
- Обмін між гравцями з пропозиціями й контрпропозиціями + курси банку 4:1 / 3:1 / 2:1 — 🥉 (інтерфейс і правила обміну).
- Генерація випадкової мапи зі збалансованими числами (наприклад, «6» і «8» не поруч) — 📎.
- AI, що оцінює вершини за сумою ймовірностей і різноманіттям ресурсів і веде обмін — 👑.

## Мапа на каталог
- Є: `hot-seat` · `turn-enforcement` · `ai-opponent` · `online-multiplayer` · `rule-variants` (злиття фаз, мапа новачків / випадкова) · `match-setup` · `game-screen` · `end-screen` · `help-window` · `settings-window` · `leaderboard` · `cell-click` (вершина / ребро / гекс) · `legal-move-highlight`.
- **Нема** → пропозиції карток:
  - `+vertex-edge-placement` «Фігури на вершинах і ребрах сітки» · entities/legality · 🥈 · слот {site: vertex|edge}.
  - `+dice-production` «Кидок активує клітини з числом» · game-logic/economy · 🌱 · слот {dice: 2d6}.
  - `+distance-rule` «Правило відстані між фігурами» · entities/legality · 🌱.
  - `+upgrade-in-place` «Апгрейд фігури на місці» · entities/state · 🌱 — поселення → місто.
  - `+build-cost-recipes` «Ціни будування комбінаціями ресурсів» · game-logic/economy · 🌱.
  - `+trade-offer` «Обмін між гравцями з пропозиціями» · game-logic/economy · 🥉.
  - `+maritime-trade-ratio` «Курс банку за позицією» · game-logic/economy · 🌱 — 4:1 / 3:1 / 2:1.
  - `+blocker-piece` «Нейтральна фігура блокує клітину» · entities/interact · 🌱.
  - `+steal-random-card` «Випадкова крадіжка карти» · entities/interact · 🌱.
  - `+hand-limit-discard` «Скинути половину понад ліміт» · game-logic/economy · 🌱.
  - `+hidden-victory-points` «Приховані очки» · game-logic/score · 🌱.
  - `+longest-path-scoring` «Найдовший шлях у графі» · game-logic/score · 🥇.
  - `+title-steal-bonus` «Бонус-титул переходить до кращого» · game-logic/score · 🌱 — найдовша дорога, найбільша армія.
  - `+snake-setup` «Змійка розстановки» · game-logic/opponent · 🌱.
  - `+piece-supply-limit` · `+shortage-no-one-gets` · `+random-board-setup` — 🌱 кожна.
  - `+hex-grid-render` · `+connected-placement` · `+deck-draw` — уже в корпусі.

## Пропозиції до словників
- `+effect:roll_dice` — кинути кубики (сума 2d6 запускає видобуток).
- `+effect:steal` — взяти випадкову карту з руки іншого гравця (розбійник, лицар).
- `+effect:discard` — скинути карти з руки (половина на 7).
- `+effect:trade` — обмін карт між гравцями або з банком за курсом.
- `+effect:draw_cards` — взяти карту з колоди (карта розвитку).
- `+role:card` — карта ресурсу / розвитку як сутність; `+role:die` — кубик як сутність з гранями.
- `+window:trade-window` — вікно обміну «даю / хочу» з відповідями гравців і курсами банку.
- `+ui:dice-result` — показ кидка; `+ui:card-hand` — рука карт.
- `+axis:placement-site` — де стоять фігури: `cell` · `vertex` · `edge` (Catan: поселення на вершинах, дороги на ребрах).
- `+card:vertex-edge-placement` · `+card:dice-production` · `+card:longest-path-scoring` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Catan) — автор, видавець, ресурси, фази ходу, розбійник, 5 типів карт розвитку, 10 ПО, курси обміну, доповнення, цифрові версії, нагороди.
- [Офіційні правила 2020 (PDF)](https://www.catan.com/sites/default/files/2021-06/catan_base_rules_2020_200707.pdf) — склад (19 гексів, 18 жетонів, 9 гаваней, 95 ресурсів, 25 карт розвитку), підготовка змійкою, обмін, нестача ресурсу в банку, розбійник, найдовша дорога з розривом і нічиєю, злиття фаз.
- [Catan: сторінка правил](https://www.catan.com/understand-catan/game-rules) — PDF бази, 5–6 гравців, доповнень.
- [UltraBoardGames](https://www.ultraboardgames.com/catan/game-rules.php) — ціни будування, правило відстані, ліміти фігур, VP-карти в хід купівлі.
- YouTube: пошук «Catan how to play».

## Непевне
- (?) Кількість гексів кожного типу (4 ліс, 4 пасовище, 4 поля, 3 горби, 3 гори, 1 пустеля — за памʼяттю), у прочитаному тексті правил її нема.
- (?) Правило «червоні 6 і 8 не поруч» для випадкової мапи — за памʼяттю; офіційні правила розкладають жетони за літерами по спіралі.
- (?) Інтерфейс цифрових версій (вікно обміну, рейтинг, вибір цілі ПО) — не бачив, описано як «(цифрова версія)».
- (?) Деталі доповнень (Seafarers, Cities & Knights) — лише назви й роки з Wikipedia.
