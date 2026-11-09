---
title: "Isle of Skye: From Chieftain to King (Острів Скай)"
slug: isle-of-skye
aka: [Isle of Skye, "Isle of Skye: Vom Häuptling zum König", Острів Скай]
family: board-digital
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: both
  goal: score
year: 2015
platforms: [board, mobile, PC]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/isle-of-skye/game-rules.php", best: true, note: "повні правила: фази раунду, ширми й ціни, маркер скидання, купівля, збіг країв, сувої, золото, тай-брейк"}
  - {kind: other, url: "https://www.ultraboardgames.com/isle-of-skye/scoring.php", note: "усі 16 рахункових плиток з очками"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Isle_of_Skye:_From_Chieftain_to_King", note: "Pfister і Pelikan, Kennerspiel des Jahres 2016, Journeyman, застосунок Digidiced"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Isle+of+Skye", note: "пошук BGG (сторінка віддає 403)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Isle+of+Skye", note: "пошук; цифрова версія Digidiced"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Isle+of+Skye+board+game+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 70
mechanics: [cell-click, drag-drop-piece, hover-highlight, legal-move-highlight, turn-enforcement, hot-seat, ai-opponent, round-currency, event-points, goal-counter, game-settings, leaderboard, +edge-matching, +connected-placement, +tile-rotate, +self-pricing-auction, +hidden-simultaneous-pricing, +discard-marker, +discard-to-bag, +rotating-score-goals, +random-scoring-cards, +catch-up-income, +road-network-income, +completed-area-scoring, +completed-area-double, +set-collection, +majority-bonus, +gold-to-points, +discard-unplayable]
proposes: ["+trigger:round_end", "+effect:discard", "+effect:buy", "+effect:set_price", "+effect:draw_tile", "+cond:edge_match", "+cond:area_closed", "+cond:road_connected", "+ui:price-tags", "+ui:scoring-schedule", "+window:price-screen", "+card:self-pricing-auction", "+card:rotating-score-goals", "+card:catch-up-income"]
author: opus
date: 2026-11-09
---

# Isle of Skye — прибудовуєш тайли зі збігом країв, але кожен свій тайл спершу оцінюєш: дорожче — суперник не купить, дешевше — купить і ти отримаєш гроші

## Суть
Кожен гравець — вождь клану, що росте від свого замку квадратними тайлами ландшафту; ребра сусідніх тайлів мусять збігатися місцевістю (пасовище, гори, вода). Ядро — **самоцінування**: щораунду тягнеш 3 тайли, один таємно скидаєш, на два інші ставиш ціну зі свого золота; суперники можуть купити твій тайл за твою ціну, а некуплений ти «викуповуєш» сам, втрачаючи поставлене золото. Очки рахують **4 з 16** рахункових плиток, що вмикаються в різних раундах за розкладом, тож кожна партія має свою мету.

## Поле і час
- **Особисте поле**: територія клану — необмежена квадратна сітка, що росте від замку; новий тайл має торкатися ребром уже покладеного.
- **Спільне**: дошка з треком очок, треком раундів (A–D під кожним раундом) і 4 слотами рахункових плиток; мішок з 73 тайлами; банк золота.
- **Темп**: 6 раундів (2–4 гравці) або 5 (5 гравців); раунд = 6 фаз, у фазах 2–3 гравці діють **одночасно й таємно** (за ширмами), у фазі 4 — по колу від першого гравця.
- Тайл: 4 ребра з місцевістю, можливі дороги (не мусять продовжуватись), іконки (вівці, корови, кораблі, ферми, маяки, брохи, бочки віскі), сувої (кінцевий рахунок).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тайл ландшафту | tile | 4 ребра (пасовище / гори / вода), дороги, іконки, сувій | тягнеться з мішка, оцінюється, купується, викладається зі збігом ребер |
| Замок | static | стартовий тайл гравця, джерело доріг | дає 5 золота щораунду; від нього рахується «зʼєднано дорогою» |
| Ширма | object | 1 на гравця | за нею таємно ставиться ціна й маркер скидання |
| Маркер скидання (сокира) | mark | 1 на гравця | позначає тайл, що повертається в мішок |
| Золото | resource | банк, монети | ставиться на тайли як ціна; 5 золота = 1 ПО наприкінці |
| Мішок тайлів | supply | 73 тайли | випадкове тягнення по 3; скинуті й невикладні тайли повертаються |
| Рахункова плитка | mark | 4 з 16, слоти A–D | у своїх раундах дає ПО за умовою (2×2, завершені області, маяк біля корабля…) |
| Область | zone | місцевість, тайли, завершена? | завершена = повністю оточена іншою місцевістю; сувої в ній — подвійні |
| Дорожня мережа | zone | тайли, зʼєднані дорогою із замком | віскі в мережі = дохід; деякі плитки рахують корів/тайли в мережі |
| Маркер першого гравця, жетон раунду | object | — | передається за годинниковою; жетон рушає треком раундів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «4 з 16 рахункових плиток лягають у слоти A–D, решта в коробку»`; кожен кладе замок; золото — з банку.
- КОЛИ `phase_start(income)` → ТО `currency(+5)` за замок; ЯКЩО `custom: «тайл з віскі зʼєднаний дорогою із замком»` → ТО `currency(+1)` за кожен.
- КОЛИ `phase_start(income)` → ЯКЩО `level(>=, 3)` → ТО `currency(+k)` за кожного гравця, що випереджає тебе на треку очок (`k` росте з раундом — catch-up).
- КОЛИ `phase_start(draw)` → ТО `custom: «кожен тягне 3 тайли з мішка лицем догори перед своєю ширмою»`.
- КОЛИ `input(mark(tile, discard))` → ТО `custom: «маркер скидання на 1 тайл — таємно»`.
- КОЛИ `input(price(tile, n))` → ЯКЩО `has(player, gold >= n)` and `custom: «n ≥ 1 на кожному з двох нескинутих тайлів»` → ТО `custom: «золото кладеться на тайл, решта ховається в руці»`.
- КОЛИ `custom: «усі готові — ширми знято»` → ТО `custom: «тайл з маркером скидання — назад у мішок»`, мішок перемішати.
- КОЛИ `turn_start(side)` у фазі купівлі → ЯКЩО `has(side, gold >= price)` → ТО `input(buy(tile_of_other))`: `currency(-price)` покупцю, `currency(+price + золото на тайлі)` продавцю, тайл — покупцю; інакше `pass_turn`. Кожен купує ≤ 1 тайл.
- КОЛИ `custom: «фаза купівлі завершена»` → ТО `custom: «некуплені тайли — власнику; золото, поставлене на них, іде в банк»`.
- КОЛИ `input(place(tile, cell, rotation))` → ЯКЩО `free(cell)` and `custom: «торкається ребром тайла території»` and `custom: «кожне спільне ребро однакової місцевості»` → ТО `place(tile)`; дороги на ребрах збігатися не мусять.
- КОЛИ `custom: «тайл не має легального місця»` → ТО `custom: «тайл повертається в мішок, золото за нього не повертається»`.
- КОЛИ `pattern(region_closed)` → ТО `custom: «область завершена: сувої в ній рахуються двічі наприкінці»`; дороги не розривають область.
- КОЛИ `custom: «кінець раунду r»` → ТО для кожної плитки з розкладу раунду `score(+n)` за її умовою; кожна плитка спрацьовує 3 рази за партію.
- Приклади плиток: `score(+2)` за кожен квадрат 2×2 тайлів (тайли в кількох квадратах) · `score(+1)` за завершену область · `score(+3)` за воду з кораблем і маяком поруч · `score(+1/+3/+6)` за гори з 1/2/3 брохами · `score(+5/+2)` найбільше/друге за кораблями, віскі чи золотом · `score(+1)` за тайл, зʼєднаний дорогою із замком · `score(+3)` за вертикальну лінію ≥ 3 тайлів.
- КОЛИ `custom: «кінець раунду»` → ТО `custom: «маркер першого гравця за годинниковою; жетон раунду +1»`.
- КОЛИ `game_over` → ТО сувої: вівці / віскі / кораблі — `score(+1)` за пару; корови, брохи, ферми, маяки — `score(+1)` кожен; у завершеній області — ×2; `score(+1)` за кожні 5 золота.
- Перемога: найбільше ПО · тай-брейк: більше залишкового золота.

## Керування і ввід
- Фаза ціни: drag маркера скидання на один тайл, drag/клік монет на два інші (лічильник ціни); підтвердити — «готовий».
- Фаза купівлі: клік по тайлу суперника з ціною або «пас»; черга по колу від першого гравця.
- Фаза будування: drag тайла в територію, поворот на 90°, підсвічені легальні клітини (ребро + збіг місцевості); тайл без місця — автоскидання.
- Таємність: у цифровій версії ціни суперників приховані до кінця фази (замість ширми).

## Вікна, меню, HUD
(цифрова версія — застосунок Digidiced (?))
- `main-menu`: Локальна гра · Онлайн · Проти AI · Навчання · Правила · Налаштування.
- `match-setup`: кількість гравців (2–5), AI-рівні, вибір рахункових плиток (випадково / вручну).
- `game-screen`: своя територія, `opponent-boards`, `price-tags` над трьома тайлами, `scoring-schedule` (які плитки в якому раунді, поточна підсвічена), `coins`, трек очок як `score`, `turn-indicator`, `legal-move-highlight`, `remaining-counter` тайлів у мішку.
- `price-screen` (модал фази ціни): 3 тайли, маркер скидання, слайдер/кнопки ціни, скільки золота лишається в руці.
- `end-screen`: рахунок по сувоях, золоту і раундових плитках.
- `help-window` (опис 16 плиток) · `leaderboard`.
- Переходи: main-menu → match-setup → game-screen ⇄ price-screen → end-screen.

## Фічі поза полем
- `ai-opponent-levels`, `online-multiplayer`, `hotseat` (pass-and-play) (?).
- `custom-rules`: ручний вибір 4 плиток (сценарій) або випадковий; варіант на 5 гравців (інший бік дошки, 5 раундів).
- `tutorial`, `rules-page` з поясненням кожної рахункової плитки, `stats`.
- Розширення: Journeyman (мандрівник ходить територією й активує тайли; нові планшети змінюють аукціон), Druids (?).

## Варіації й родичі
- Родичі в корпусі: [carcassonne.md](carcassonne.md) (збіг ребер, але спільне поле), [kingdomino.md](kingdomino.md) (особисте королівство, драфт, де ціна — черговість), [dorfromantik](../build-sim/dorfromantik.md).
- Самоцінування з викупом — родич Harberger-податку і Castles of Burgundy/Spiel-аукціонів; вирішальна різниця — гроші купівлі йдуть **супернику**.
- Змінні цілі з колоди — родич Cartographers (едикти A–D за сезонами) і Sprawlopolis.
- **Осі варіацій**: хто призначає ціну (продавець / аукціон / фіксована) · доля некупленого (викуп своєю ціною / безкоштовно / скинути) · збіг (усі ребра / одне / нема) · рахунок (фіксований / 4 з N за розкладом / таємні цілі) · catch-up (дохід відстаючим / нема).

## Цікавинки для курсу
- Самоцінування: ціна як сигнал — дорого = «не продаю, але сам викуплю дорого», дешево = «бери, мені байдуже»; рушій фаз і розрахунок грошей — 📎.
- Розклад рахункових плиток: 4 слоти × 6 раундів, плитки-плагіни зі спільним інтерфейсом `score(territory)` — 🥉 (16 оцінювачів = 16 маленьких задач).
- Завершена область: flood fill по ребрах тайлів (області на ребрах, а не на тайлах) і перевірка «оточена іншою місцевістю» — 🥉.
- Дорожня мережа від замку: BFS по тайлах з дорогами для доходу віскі та плиток «корови/тайли в мережі» — 📎.
- AI ціноутворення: оцінити, скільки тайл вартий кожному супернику з урахуванням їхніх плиток — 🥇.
- Catch-up дохід за кожного, хто попереду — 🌱, але вартий обговорення «гумової стрічки».

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `hover-highlight` · `legal-move-highlight` · `turn-enforcement` · `hot-seat` · `ai-opponent` · `round-currency` (золото раунду) · `event-points` · `goal-counter` · `game-settings` · `leaderboard`.
- **Нема** → пропозиції карток:
  - `+self-pricing-auction` «Продавець сам ставить ціну, покупець платить продавцю, некуплене викуповує власник» · game-logic/economy · 📎 · слоти {скидати: так/ні, мінімум: 1}.
  - `+hidden-simultaneous-pricing` — одночасна таємна фаза; родич `simultaneous-turns` з Ubongo.
  - `+discard-marker` / `+discard-to-bag` — скинутий тайл повертається в мішок, а не з гри.
  - `+rotating-score-goals` «N цілей з колоди вмикаються за розкладом раундів» · game-logic/score · 🥉 · слоти {пул: 16, у партії: 4, розклад}.
  - `+random-scoring-cards` — як у Cartographers.
  - `+catch-up-income` «Дохід за кожного суперника попереду» · game-logic/economy · 🌱.
  - `+road-network-income` · `+completed-area-scoring` · `+completed-area-double` · `+set-collection` (пари сувоїв) · `+majority-bonus` (5/2 за перше/друге) · `+gold-to-points` · `+edge-matching` · `+connected-placement` · `+tile-rotate` · `+discard-unplayable` — як у сусідах по теці.

## Пропозиції до словників
- `+trigger:round_end` — тут спрацьовують раундові плитки (як у Kingdomino).
- `+effect:discard` — тайл повертається в мішок; `+effect:draw_tile` — тягнення N тайлів з мішка (`draw` у словнику — нічия).
- `+effect:set_price` — гравець призначає ціну своєму тайлу; `+effect:buy` — купівля за ціною іншого гравця (гроші — йому).
- `+cond:edge_match` — тут **усі** спільні ребра однакові (у Kingdomino — хоча б одне).
- `+cond:area_closed` — область оточена іншою місцевістю (Carcassonne-місто, Skye-область).
- `+cond:road_connected` — тайл зʼєднаний дорогою з точкою (замок).
- `+ui:price-tags` — ціна над тайлом · `+ui:scoring-schedule` — таблиця «плитка × раунд».
- `+window:price-screen` — таємна фаза ціни (`match-setup`, `turn-structure: simultaneous + sequential` — уже в словниках).
- `+card:self-pricing-auction` · `+card:rotating-score-goals` · `+card:catch-up-income`.

## Джерела
- ⭐ [UltraBoardGames: Isle of Skye rules](https://www.ultraboardgames.com/isle-of-skye/game-rules.php) — компоненти (73 тайли, 16 плиток, ширми, маркери скидання), 6 фаз раунду, купівля, збіг країв, завершені області, сувої, золото, тай-брейк.
- [UltraBoardGames: Scoring tiles](https://www.ultraboardgames.com/isle-of-skye/scoring.php) — умови й очки всіх 16 рахункових плиток.
- [Wikipedia: Isle of Skye: From Chieftain to King](https://en.wikipedia.org/wiki/Isle_of_Skye:_From_Chieftain_to_King) — автори, Kennerspiel des Jahres 2016, Journeyman, анонс застосунку Digidiced.
- BGG: пошук «Isle of Skye» (403 для WebFetch); Steam і YouTube — пошукові лінки.

## Непевне
- (?) Розклад плиток за раундами (1: A · 2: B · 3: A C · 4: B D · 5: A C D · 6: B C D) — з памʼяті; джерело підтверджує лише «кожна плитка тричі за партію».
- (?) Суми catch-up доходу по раундах і розклад для гри на 5 (5 раундів) — UltraBoardGames їх не наводить.
- (?) Цифрова версія Digidiced: Wikipedia каже лише «заплановано на 2018»; меню, AI і онлайн — з памʼяті.
- (?) Розширення Druids — UltraBoardGames має сторінку, правил не читав.
- (?) Чи поворот тайла довільний на 90° — так у фізичній грі, у джерелі явно не сказано.
