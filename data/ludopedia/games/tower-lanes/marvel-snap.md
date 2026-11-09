---
title: Marvel Snap
slug: marvel-snap
aka: [MARVEL SNAP, Snap]
family: tower-lanes
also: []
klass: cursor
axes:
  field: 1d
  time: wego
  opponent: online
  info: hidden
  random: both
  goal: territory
year: 2022
platforms: [iOS, Android, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Marvel_Snap", best: true, note: "колода 12, енергія +1/хід, 3 локації з ефектами, перемога в 2 з 3, ставка Snap/Retreat, режими, ранги"}
  - {kind: other, url: "https://outof.games/realms/marvel-snap/guides/255-how-to-play-marvel-snap/", note: "правила: рука 3 + 1/хід, ліміт 7, хто розкриває першим, Move/Destroy/Discard, Retreat"}
  - {kind: other, url: "https://www.shacknews.com/article/132689/how-to-play-marvel-snap?amphtml=1", note: "4 карти на локацію, порядок розкриття локацій, On Reveal / Ongoing, максимум 8 кубів"}
  - {kind: steam, url: "https://store.steampowered.com/app/1997040/MARVEL_SNAP/", note: "6 ходів, 3 локації, 200+ локацій, режими"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=marvel+snap+gameplay+explained", note: "пошук; пояснення правил"}
stage: v1
coverage: 60
mechanics: [drag-drop-piece, pocket, inventory-limit, online-multiplayer, rating-system, mode-select, move-timer, hp-damage, piece-capture, +lane-grid, +deck-draw, +card-sigils, +simultaneous-turns, +reveal-order-priority, +location-modifiers, +zone-capacity, +majority-of-lanes, +stake-doubling, +retreat-concede, +ramping-energy, +deck-builder, +card-collection]
proposes: ["+trigger:reveal", "+trigger:card_played", "+effect:draw", "+effect:discard", "+effect:double_stake", "+effect:retreat", "+role:card", "+ui:lane-power", "+ui:cube-stake", "+ui:priority-glow", "+window:deck-builder", "+window:collection-window", "+feature:season-reset", "+card:stake-doubling", "+card:reveal-order-priority"]
author: opus
date: 2026-11-09
---

# Marvel Snap — 6 ходів, 3 локації-смуги з правилами, приховані одночасні ходи і ставка «Snap», що подвоює куби

## Суть
Два гравці з колодами по 12 карт за 6 ходів викладають карти на **три локації**; у кожної локації є власне правило-модифікатор. Ходи **одночасні й приховані**: обидва кладуть карти, потім вони розкриваються по черзі — і спрацьовують ефекти. Хто має більше сили на локації — тримає її; виграє той, хто тримає **2 з 3**. Зверху — ставка: стартує з 1 куба, будь-хто може натиснути **Snap** (подвоїти), суперник може **відступити** й програти менше.

## Поле і час
- Поле — **3 локації в ряд** (лінійне «поле з трьох смуг»); кожна локація має по **4 слоти** на кожен бік (свій і суперника).
- Локації випадкові з пулу 200+; ліва відкривається на старті (ходу 1), середня — на ходу 2, права — на ходу 3; до відкриття локація без ефекту для зіграних туди карт (крім Ongoing).
- Хід: обидва одночасно розплановують, натискають «End Turn» → розкриття за порядком → ефекти → наступний хід.
- 6 ходів (деякі локації міняють: TVA — 4, Limbo — 7); енергія = номер ходу, не накопичується.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Карта персонажа | piece (`+role:card`) | ціна (енергія), сила, здібність | кладеться в слот локації з руки; дає силу локації |
| On Reveal-карта | piece | — | ефект один раз у момент розкриття |
| Ongoing-карта | piece | — | постійна аура, поки на полі (може діяти й на інші локації) |
| Move-карта | piece | — | може перейти на іншу локацію після свого ходу; On Reveal при цьому не спрацьовує |
| Локація | zone | ефект, 4 слоти на бік | своє правило (змінює силу, енергію, кількість ходів, забороняє чи дублює) |
| Рука | zone | ≤ 7 карт | старт 3 карти, +1 на початку кожного ходу; повна рука — добір пропускається |
| Колода | zone | 12 карт | перемішана, без мулігану |
| Енергія | resource | = номер ходу | витрачається на карти, залишок згорає |
| Ставка (куби) | resource | 1 → 2 → 4 → 8 | Snap подвоює; фінальний хід — подвоєння автоматично |
| Суперник | — | прихована рука | людина онлайн |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «draw ×3»`, ставка = 1 куб; `reveal(ліва локація)`.
- КОЛИ `turn_start(both)` → ТО `custom: «draw 1»` ЯКЩО `count(hand, <, 7)`; енергія = номер ходу.
- КОЛИ `turn_start(both)` → ЯКЩО `custom: «хід 2 / хід 3»` → ТО `reveal(середня / права локація)`.
- КОЛИ `input(drag, card, location)` → ЯКЩО `counter(energy, >=, cost)` and `count(свої карти на локації, <, 4)` and `legal(локація дозволяє)` → ТО `place(player, card)` лицем донизу; інакше `block`.
- КОЛИ `input(drag_back, card)` до кінця ходу → ТО `custom: «скасувати план, енергія повертається»`.
- КОЛИ `turn_end(both)` → ТО `custom: «reveal: першим розкриває той, хто зараз лідирує (більше локацій / сили), при рівності — випадково; карти кожного — у порядку, в якому їх клали»`.
- КОЛИ `custom: «reveal(card)»` → ЯКЩО `custom: «здібність On Reveal»` → ТО `custom: «ефект картки»` (сила ±, добір, переміщення, знищення, створення карт).
- КОЛИ `custom: «карта з Ongoing на полі»` → ТО `custom: «модифікатор діє постійно, перераховується після кожної зміни»`.
- КОЛИ `custom: «ефект Destroy(card)»` → ЯКЩО `custom: «ціль уже розкрита»` → ТО `disappear(card)`.
- КОЛИ `custom: «ефект Discard»` → ТО `custom: «discard: випадкова (або вказана) карта з руки»`.
- КОЛИ `input(move, card, location)` → ЯКЩО `custom: «карта має Move»` and `count(slots, <, 4)` → ТО `move(card, location)`; On Reveal не спрацьовує.
- КОЛИ `custom: «локація розкрита»` → ТО `custom: «її правило діє на карти, зіграні після розкриття»`.
- КОЛИ `input(snap)` → ЯКЩО `custom: «цей гравець ще не снапав»` → ТО `custom: «double_stake: ставка ×2 з початку наступного ходу»` (max 8).
- КОЛИ `turn_start(final)` → ТО `custom: «double_stake автоматично»`.
- КОЛИ `input(retreat)` → ТО `custom: «retreat: гравець втрачає поточну ставку (≥1)»`, суперник `win`; обидва відступили — `draw`.
- КОЛИ `turn_end(6)` → ТО `custom: «для кожної локації: більша сума сили — локація твоя; рівно — нічия на локації»`.
- КОЛИ `custom: «тримаєш ≥ 2 локацій»` → ТО `win`, `custom: «+куби = ставка»`; суперник `lose`, `-куби`.
- КОЛИ `custom: «локації поділено / нічиї»` → ТО `custom: «тайбрейк — див. Непевне»`; повна рівність → `draw`, куби не міняються.
- Battle Mode: КОЛИ `win` раунду → ТО `damage(суперник, ставка)`; 10 HP на старті; з раунду 5 ставка подвоюється.
- Перемога: 2 з 3 локацій · Поразка: 2 локації в суперника або Retreat · Рахунок: куби → ранг.

## Керування і ввід
- Тач/миша: drag карти з руки на локацію; перетягнути назад — скасувати до кінця ходу.
- Кнопка «End Turn» (обидва гравці, одночасно); кнопка-куб — Snap; прапорець — Retreat (одразу або «пізніше»).
- Затиснути карту/локацію — повний опис ефекту (`tooltip`).
- Таймер ходу — після нього хід закінчується (?).

## Вікна, меню, HUD
- `main-menu` / хаб: Play (ранговий) → пошук суперника; вибір колоди; режими (`mode-select`): Conquest, Battle Mode (з другом), тимчасові (Deadpool's Diner, High Voltage…).
- `+window:deck-builder` — 12 слотів, фільтри колекції.
- `+window:collection-window` — колекція, варіанти (косметика), рівень колекції й треки нагород.
- `shop-window` — магазин (косметика, сезонний пропуск).
- `lobby-window` / пошук суперника.
- `game-screen`: 3 локації з описом правила, по 4 слоти на бік, `+ui:lane-power` (сума сили на кожній локації з обох боків), рука (`pocket`), `energy-bar`, `turn-counter` (n/6), `+ui:cube-stake`, `+ui:priority-glow` (підсвітка імені того, хто розкриває першим), кнопки End Turn / Snap / Retreat.
- `end-screen` — переможець, зміна кубів, рангова шкала.
- Переходи: хаб → вибір колоди → пошук → game-screen → end-screen → хаб.

## Фічі поза полем
- `rank-tiers`: рангова драбина за куби; щомісячний сезон із `+feature:season-reset` (м'який скид на 30 рангів, до кратного 10).
- `unlockables`: пули карт 1–5 відкриваються з рівнем колекції; варіанти — косметика.
- `mode-versus`: Battle Mode з другом (10 HP), Conquest (ліги з квитками), тимчасові режими.
- `online-multiplayer`, спільний акаунт мобайл/Steam.

## Варіації й родичі
- High Voltage: 3 ходи, по 2 карти й 2–5 енергії за хід; Deadpool's Diner — більше снапів.
- Родичі: [inscryption](inscryption.md) (колонки-смуги, сила проти сили), [wildfrost](wildfrost.md) і [monster-train](monster-train.md) (карти на смугах/поверхах), [plants-vs-zombies](plants-vs-zombies.md) (смуги), Hearthstone (ціна-енергія, ефекти «Battlecry» ≈ On Reveal), Backgammon (подвоєння ставки), «Lost Cities» / Schotten Totten (боротьба за кілька точок з обмеженими слотами).
- **Осі варіацій**: ходи — по черзі / одночасні приховані · смуга — бій істот навпроти / сума сили · поле — фіксоване / локації з правилами, що відкриваються · ставка — фіксована / подвоєння з відступом.

## Цікавинки для курсу
- Одночасні приховані ходи + детермінований порядок розкриття (лідер першим, далі — порядок клацань) — 🥉.
- Перерахунок Ongoing-аур після кожної зміни поля (порядок застосування модифікаторів) — 🥈.
- Локації як правила-модифікатори, що відкриваються на ходах 1–3 — «правило як обʼєкт поля» — 🥉.
- Ставка з подвоєнням і відступом: стан партії поза полем, теорія блефу — 📎.
- Перемога «більшість із трьох смуг» з тайбрейком — 🌱.
- Рука з лімітом 7, добір 1/хід, колода 12 без мулігану — 🌱.
- AI-суперник для «трьох смуг» (Monte Carlo по прихованій руці) — 👑.

## Мапа на каталог
- Є: `drag-drop-piece` ↔ карта на локацію · `pocket` ↔ рука · `inventory-limit` ↔ рука ≤7 · `online-multiplayer`, `rating-system` (куби/ранги), `mode-select`, `move-timer` (?) · `hp-damage` ↔ Battle Mode · `piece-capture` ≈ Destroy (?).
- **Нема** → пропозиції карток:
  - `+lane-grid` (з Inscryption/PvZ) — тут три локації-смуги.
  - `+deck-draw`, `+card-sigils` (On Reveal / Ongoing / Move) — повтори з Inscryption.
  - `+simultaneous-turns` «Одночасні приховані ходи» · game-logic/opponent · 🥉.
  - `+reveal-order-priority` «Порядок розкриття: лідер першим, далі — порядок дій» · game-logic/opponent · 🥉.
  - `+location-modifiers` «Зони поля з власними правилами, що відкриваються з часом» · game-logic/win · 🥉.
  - `+zone-capacity` «Ліміт N фігур на зону з кожного боку» · entities/legality · 🌱.
  - `+majority-of-lanes` «Перемога — більшість смуг, тайбрейк за сумою» · game-logic/win · 🌱.
  - `+stake-doubling` «Подвоєння ставки (Snap) і відступ» · game-logic/score · 📎.
  - `+retreat-concede` «Здатися раніше з меншою втратою» · game-logic/lose · 🌱.
  - `+ramping-energy` «Енергія = номер ходу, без накопичення» · game-logic/economy · 🌱.
  - `+deck-builder`, `+card-collection` — колода з колекції; колекція з рівнями.

## Пропозиції до словників
- `+trigger:reveal` — карту розкрито (On Reveal); `+trigger:card_played` — повтор з Inscryption.
- `+effect:draw` — взяти карту з колоди (повтор); `+effect:discard` — скинути карту з руки.
- `+effect:double_stake` — подвоїти ставку партії; `+effect:retreat` — вийти з партії з поточною втратою.
- `+role:card` — карта як сутність (повтор з Inscryption).
- `+ui:lane-power` — сума сили на смузі з обох боків; `+ui:cube-stake` — поточна ставка; `+ui:priority-glow` — хто розкриває першим.
- `+window:deck-builder`, `+window:collection-window`.
- `+feature:season-reset` — м'який скид рангу щосезону.
- `+card:stake-doubling`, `+card:reveal-order-priority` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Marvel Snap](https://en.wikipedia.org/wiki/Marvel_Snap) — колода 12, енергія 1 і +1 щоходу, 3 випадкові локації з ефектами (відкриваються на перших трьох ходах), розкриття в кінці раунду, 2 з 3, ставка 1 куб, Snap подвоює, автоподвоєння на фінальному ході, Retreat, сезонний скид на 30 рангів, пули карт, Battle Mode (10 HP), Conquest, High Voltage.
- [Out of Games: How to play](https://outof.games/realms/marvel-snap/guides/255-how-to-play-marvel-snap/) — рука 3 + 1/хід, ліміт 7, без мулігану, одночасні приховані ходи, лідер розкриває першим (світіння імені), Move/Destroy/Discard, Retreat «зараз / пізніше», обидва відступили — нічия.
- [Shacknews: How to play](https://www.shacknews.com/article/132689/how-to-play-marvel-snap?amphtml=1) — 4 карти на локацію, порядок відкриття локацій ліва → середня → права, TVA/Limbo міняють кількість ходів, On Reveal / Ongoing, максимум 8 кубів.
- [Steam: MARVEL SNAP](https://store.steampowered.com/app/1997040/MARVEL_SNAP/) — 6 ходів, 200+ локацій, режими.
- YouTube: пошук «marvel snap gameplay explained».

## Непевне
- (?) Тайбрейк при поділі локацій: джерела розходяться — «більша сума сили на всіх трьох» (PC Gamer, Prima за пошуком) проти «більший відрив на своїй локації» (Shacknews, Out of Games).
- (?) Автоподвоєння: на початку фінального ходу (Wikipedia) чи по завершенні партії (Out of Games).
- (?) Snap діє з наступного ходу (а не одразу) і один раз на гравця — з памʼяті.
- (?) Таймер ходу і його тривалість.
- (?) Destroy як `piece-capture` — схоже лише частково (нема ходу на клітину).
