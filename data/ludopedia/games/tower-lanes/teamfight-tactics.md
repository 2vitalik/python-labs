---
title: Teamfight Tactics (TFT)
slug: teamfight-tactics
family: tower-lanes
also: [tactics]
klass: cursor
axes:
  field: hex
  time: realtime
  opponent: online
  info: partial
  random: runtime
  goal: survive
year: 2019
platforms: [PC, Mac, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Teamfight_Tactics", best: true, note: "раунди, карусель, золото й відсотки, магазин, зірки з 3 копій, трейти, предмети, аугменти"}
  - {kind: official, url: "https://teamfighttactics.leagueoflegends.com/en-us/"}
  - {kind: wiki, url: "https://wiki.leagueoflegends.com/en-us/TFT:Gold", note: "доход, відсотки, серії, продаж"}
  - {kind: wiki, url: "https://wiki.leagueoflegends.com/en-us/TFT:Experience", note: "XP, рівні, ліміт юнітів"}
  - {kind: wiki, url: "https://wiki.leagueoflegends.com/en-us/TFT:Item", note: "компоненти, збирання, емблеми"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=teamfight+tactics+beginner+guide", note: "пошук; гайд для новачка"}
stage: v1
coverage: 55
mechanics: [round-currency, shop-catalog, shop-buyback, shop-preview, tile-merge, inventory-items, inventory-limit, drag-drop-piece, hp-damage, chase-greedy, melee-vs-ranged, ai-opponent, enemy-waves, move-timer, +auto-battle, +bench-and-board, +interest-economy, +streak-bonus, +shop-reroll, +star-up-merge, +trait-synergy, +item-combine, +shared-draft-carousel, +augment-choice, +shared-unit-pool]
proposes: ["+trigger:phase_start", "+trigger:round_lost", "+cond:count_unique", "+cond:same", "+effect:merge", "+effect:reroll", "+effect:interest", "+effect:choose", "+role:unit", "+role:bench", "+ui:trait-tracker", "+ui:shop-bar", "+ui:player-list", "+ui:gold-interest", "+window:choice-window", "+window:lobby-window", "+feature:mode-coop", "+axis:time"]
author: opus
date: 2026-11-02
---

# Teamfight Tactics — auto battler: купуй юнітів, збирай трійки, став на гекси — бій іде сам

## Суть
Вісім гравців паралельно будують загони: між раундами купують юнітів у магазині з 5 карт, тримають їх на лаві або ставлять на свою половину гексового поля, вішають предмети. Бій іде **без участі гравця**: юніти самі шукають цілі, бʼють, накопичують ману й кастують здібність. Програш раунду знімає HP гравця; виживає останній. Глибина — в економіці (відсотки на золото, серії), злитті 3 копій у зірку і трейтах, що вмикаються за кількістю різних юнітів одного класу.

## Поле і час
- Гексове поле: своя половина — кілька рядів гексів (4×7 (?)), у бою — дві половини разом; окремо — лава (bench) для запасних (9 слотів (?)).
- Раунд = фаза планування (купівля, розстановка, предмети; таймер ~30 с (?)) + фаза бою (real-time, з ліміт-часом).
- Стадії по 7 раундів: стадія 1 — 3 раунди проти PvE-монстрів; далі PvP із суперником-гравцем; останній раунд стадії — PvE; після 3-го раунду стадії — **карусель** (спільний вибір юніта з предметом).
- Інформація: можна дивитися чужі дошки; випадковість — магазин, лут з PvE, аугменти, пари суперників.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тактик (аватар гравця) | player | HP гравця (100 (?)) | бігає по арені, збирає лут; програш раунду → −HP |
| Чемпіон | ally (`+role:unit`) | ціна 1–5, зірки 1–3, HP, мана, атака, дальність, трейти | у бою: іде до найближчої цілі, атакує, при повній мані — здібність |
| Лава (bench) | zone | N слотів | склад юнітів поза боєм; не воюють |
| Гекс поля | zone | — | на одному гексі — один юніт; кількість юнітів на полі ≤ рівень гравця |
| Магазин | spawner | 5 слотів, реролл | пропонує юнітів з пулу за шансами рівня |
| Золото | resource | — | дохід за раунд + відсотки + серії + перемога PvP |
| Досвід / рівень | resource | 1–10 | рівень = ліміт юнітів на полі й шанси дорогих у магазині |
| Компонент предмета | pickup | 9 базових (B.F. Sword, Recurve Bow, Rod, Tear, Chain Vest, Negatron Cloak, Giant's Belt, Sparring Gloves, Spatula) (?) | 2 на одному юніті → готовий предмет |
| Готовий предмет | pickup | стати + ефект | ≤3 предмети на юніта |
| Емблема (Spatula + компонент) | pickup | трейт | додає юніту трейт |
| Трейт (клас/походження) | zone | пороги 2/4/6… (?) | рахує **унікальних** юнітів трейту на полі; на порозі — бонус |
| PvE-монстр | enemy | — | у раундах «крипів»; дропає лут-сфери |
| Лут-сфера | pickup | золото / юніт / предмет | тактик підбирає |
| Карусель | neutral | 9 юнітів з предметами | гравці по черзі (від найменшого HP) біжуть і хапають одного |
| Аугмент | pickup | silver / gold / prismatic | вибір 1 з 3 на певних раундах; постійний бонус на партію |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «trigger phase_start(planning)»` → ТО `currency(+income)`: базові 5 (на старті 2/2/3/4), +`custom: «effect interest: +1 за кожні 10 золота, максимум +5, рахується до доходу»`, + серія перемог/поразок (+1 за 3–4, +2 за 5, +3 за 6+), +1 за перемогу в PvP; `counter(xp, +2)`.
- КОЛИ `input(buy, slot)` → ЯКЩО `has(gold, cost)` and `custom: «є місце на лаві»` → ТО `currency(-cost)`, `spawn(unit, bench)`.
- КОЛИ `custom: «на лаві+полі 3 копії однакових зі зірками k»` → ТО `merge(3 → 1, stars k+1)`, предмети переходять на результат; 3 × ★2 → ★3 (разом 9 копій).
- КОЛИ `input(reroll)` → ЯКЩО `has(gold, 2)` (?) → ТО `custom: «effect reroll: 5 нових юнітів за шансами рівня»`.
- КОЛИ `input(buy_xp)` → ЯКЩО `has(gold, 4)` → ТО `counter(xp, +4)`; КОЛИ `counter(xp, >=, need(level))` → ТО `custom: «level +1, ліміт поля +1»`.
- КОЛИ `input(sell, unit)` → ТО `currency(+value)` (1★ — повна ціна, інакше −1), `disappear_a` (юніт повертається в пул (?)).
- КОЛИ `input(drag, unit, hex)` → ЯКЩО `count(units_on_board, <, level)` or `occupied(hex, unit)` (обмін місцями) → ТО `move` / `swap`.
- КОЛИ `input(drag, component, unit)` → ЯКЩО `custom: «у юніта вже є компонент»` → ТО `merge(component+component → item)`; ЯКЩО `count(items, ==, 3)` → `block`.
- КОЛИ `custom: «змінився склад поля»` → ТО трейти: `cond:count_unique(trait, >=, threshold)` → `set_state(units_with_trait, bonus)`.
- КОЛИ `custom: «trigger phase_start(combat)»` → ТО копія суперника на протилежну половину; юніти `chase-greedy` → `in_range(a, target, range)` → `damage`; кожна атака/отримана шкода `counter(mana, +n)`; повна мана → `custom: «здібність»`, `counter(mana, 0)`.
- КОЛИ `all_gone(units, side)` або `timer(combat_limit)` → ТО раунд завершено; КОЛИ `custom: «trigger round_lost»` → ТО `hp(player, -(stage_damage + за кожного живого юніта суперника))`.
- КОЛИ `hp_zero(player)` → ТО `custom: «вибув на місце 8…2»`; останній живий — `win` (1 місце); топ-4 рахується як «перемога» в рейтингу.
- КОЛИ `schedule(round x-4)` → ТО карусель: `custom: «гравці стартують парами від найменшого HP»`, `pickup(unit+item)`.
- КОЛИ `schedule(augment_rounds)` → ТО `choose(3 augments)` (з Set 6).
- КОЛИ `died(pve_monster)` → ТО `spawn(loot_orb)`; КОЛИ `contact(tactician, orb)` → ТО `pickup`.
- Перемога: останній живий з 8 · Поразка: HP гравця = 0 · Рахунок: місце 1–8, ранг (LP).

## Керування і ввід
- Миша/тач: drag юніта з лави на гекс, між гексами, на магазин (продаж); drag компонента на юніта.
- Клік по слоту магазину — купити; кнопки Reroll (D), Buy XP (F), Lock shop; ПКМ — бігти тактиком (збір луту, карусель).
- Клік по іконці гравця в списку — подивитися чужу дошку; гарячі клавіші — Q (?), E (продати), W (переставити).

## Вікна, меню, HUD
- `lobby-window` (⏳) — черга Normal/Ranked/Hyper Roll/Double Up, вибір тактика й арени (`skin-select`).
- `game-screen`: гексове поле, лава, тактик; `+ui:shop-bar` (5 карт з ціною, трейтами; Reroll, Buy XP, Lock), рівень і XP-бар, `coins` з індикатором відсотків (`+ui:gold-interest`), `+ui:trait-tracker` ліворуч (трейти з лічильником і порогами), `+ui:player-list` праворуч (HP усіх 8, серії), `timer-countdown` фази, номер стадії-раунду, `tooltip` юнітів і предметів.
- `choice-window` (`+window:choice-window`) — вибір 1 з 3 аугментів.
- `custom-window` карусель — кругова арена з юнітами.
- `end-screen` — місце 1–8, зміна LP; `stats-window`/історія матчів; `pause-menu` нема (онлайн).
- Переходи: клієнт → lobby → завантаження → game-screen (раунди) → end-screen → lobby.

## Фічі поза полем
- `mode-versus` 8 гравців; Double Up — `mode-coop` 2v2v2v2; Hyper Roll — швидкий режим; Ranked — `rank-tiers`.
- Сети: кожні ~4 місяці новий пул юнітів, трейтів, механік; mid-set оновлення ~3 місяці (`custom-rules` на рівні дизайну).
- Тактики, арени, ефекти — `unlockables`/косметика; `stats`, `history`, `leaderboard-online`; кросплатформа PC↔mobile.

## Варіації й родичі
- Dota Auto Chess (мод, 2019 — першоджерело жанру), Dota Underlords, Hearthstone Battlegrounds (без поля, ряд юнітів), Super Auto Pets (асинхронний, 1D ряд), The Bazaar.
- **Осі варіацій**: поле — гекси / квадрати / ряд (1d) · суперник — живий синхронно / записані дошки асинхронно · підсилення — зірки злиттям / рівні · економіка — відсотки / фіксований дохід · спільний пул юнітів — так / ні.

## Цікавинки для курсу
- Злиття 3 однакових у зірку (з урахуванням лави і поля, каскадне ★1→★2→★3) — 🥉.
- Економіка: дохід + відсотки з капом + серії — 📎 (формула, але вчить точкам рішень).
- Трейти: підрахунок унікальних юнітів за трейтом і пороги бонусів — 🥉.
- Предмети: таблиця «компонент × компонент → предмет» (рецепти як дані) — 🥉.
- Авто-бій на гексах: пошук найближчої цілі, рух, атака, мана — 🥈 (гекс-сітка + real-time AI).
- Магазин зі шансами за рівнем і спільним скінченним пулом копій — 🥈.
- Карусель з чергою від найслабшого — 📎 (catch-up механіка).

## Мапа на каталог
- Є: `round-currency` ↔ золото · `shop-catalog` + `shop-preview` ↔ магазин з трейтами · `shop-buyback` ↔ продаж · `tile-merge` ↔ 3 копії → зірка · `inventory-items` + `inventory-limit` ↔ предмети, 3 слоти · `drag-drop-piece` ↔ розстановка · `hp-damage` · `chase-greedy` ↔ рух до найближчої цілі · `melee-vs-ranged` ↔ дальність юнітів · `ai-opponent` ↔ PvE-раунди · `enemy-waves` ↔ PvE-стадії · `move-timer` ↔ таймер фази · `status-panel` · `leaderboard`.
- **Нема** → пропозиції карток:
  - `+auto-battle` «Автобій без участі гравця» · game-logic/opponent · 🥈.
  - `+bench-and-board` «Лава і поле з лімітом» · entities/state · 📎 · слот {limit: level}.
  - `+interest-economy` «Відсотки на накопичене» · game-logic/economy · 📎 · слоти {per, cap}.
  - `+streak-bonus` «Бонус за серію» · game-logic/economy · 🌱.
  - `+shop-reroll` «Оновити вітрину за ціну» · game-logic/economy · 📎 · слот {odds_by_level}.
  - `+star-up-merge` «Три копії → вища зірка» · entities/legality · 🥉 (дитина `tile-merge`).
  - `+trait-synergy` «Синергії за кількістю» · game-logic/economy · 🥉 · слот {thresholds}.
  - `+item-combine` «Рецепти: два предмети в один» · entities/state · 🥉.
  - `+shared-draft-carousel` «Спільний драфт із чергою від слабшого» · game-logic/opponent · 📎.
  - `+augment-choice` «Вибір 1 з 3 бонусів» · game-logic/economy · 📎.
  - `+shared-unit-pool` «Спільний скінченний пул копій» · game-logic/economy · 🥉.

## Пропозиції до словників
- `+trigger:phase_start` — початок фази (планування/бій), ширше за `turn_start`; `+trigger:round_lost` — сторона програла раунд.
- `+cond:count_unique` — кількість **різних** сутностей з ознакою (трейт); `same` ⏳ — однаковий юніт і зірки для злиття.
- `+effect:merge` ⏳ — підтвердження (3 → 1); `+effect:reroll` — оновити набір пропозицій; `+effect:interest` — дохід від накопиченого; `+effect:choose` ⏳ — аугменти.
- `+role:unit` — бойовий юніт загону зі статами (ширше за `piece`); `+role:bench` — зона запасу поза полем.
- `+ui:trait-tracker` · `+ui:shop-bar` · `+ui:player-list` (HP суперників) · `+ui:gold-interest` (скільки до наступних відсотків).
- `+window:choice-window` — див. inscryption; `+window:lobby-window` ⏳ — підтвердження.
- `+feature:mode-coop` ⏳ — Double Up.
- `+axis:time` — значення `phased` (планування покроково + бій real-time без вводу).

## Джерела
- ⭐ [Wikipedia: Teamfight Tactics](https://en.wikipedia.org/wiki/Teamfight_Tactics) — 8 гравців, гексове поле, стадії по 7 раундів, карусель від найменшого HP, відсотки й серії, магазин на 5, 3 копії → ★2, 9 → ★3, трейти, мана, предмети з 2 компонентів, 3 слоти, аугменти, сети.
- [League of Legends Wiki: TFT Gold](https://wiki.leagueoflegends.com/en-us/TFT:Gold) — дохід 5 (2/2/3/4 на старті), +1 за 10 золота до +5, серії +1/+2/+3, +1 за PvP-перемогу, продаж.
- [League of Legends Wiki: TFT Experience](https://wiki.leagueoflegends.com/en-us/TFT:Experience) — 4 золота = 4 XP, +2 XP за раунд, рівні 1–10, ліміт юнітів = рівень.
- [League of Legends Wiki: TFT Item](https://wiki.leagueoflegends.com/en-us/TFT:Item) — компоненти, готові предмети, 3 слоти, Spatula → емблема.
- [Офіційний сайт TFT](https://teamfighttactics.leagueoflegends.com/en-us/) — сети, новини.
- YouTube: пошук «teamfight tactics beginner guide».

## Непевне
- (?) Розмір половини поля (4×7 гексів) і лави (9) — не підтверджено джерелами.
- (?) HP гравця 100 і формула шкоди (стадія + за кожного живого юніта); вартість рероллу 2 золота; пороги трейтів 2/4/6 — залежать від сету.
- (?) Список 9 компонентів — змінюється між сетами (Frying Pan, артефакти тощо).
- (?) Чи повертається проданий юніт у спільний пул; розміри пулу за ціною.
- (?) Гарячі клавіші, крім D/F/E.
