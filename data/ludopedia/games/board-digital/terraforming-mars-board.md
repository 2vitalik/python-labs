---
title: Terraforming Mars (Тераформування Марса)
slug: terraforming-mars-board
aka: [Тераформування Марса, TM, TfM]
family: board-digital
also: []
klass: cursor
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: score
year: 2016
platforms: [board, PC, mobile, Steam]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/terraforming-mars/game-rules.php", best: true, note: "повні правила: тайли й розміщення, глобальні параметри, фази покоління, дії, стандартні проєкти, віхи й нагороди, кінець і рахунок"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Terraforming_Mars_(board_game)", note: "61 гекс, цілі параметрів, покоління, доповнення, цифрова версія 2018"}
  - {kind: steam, url: "https://store.steampowered.com/app/800270/Terraforming_Mars/", note: "цифрова версія: соло, онлайн, спільний екран, хід-нотифікації, DLC-доповнення"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Terraforming+Mars+board+game+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 55
mechanics: [cell-click, hover-highlight, legal-move-highlight, round-currency, event-points, turn-enforcement, hot-seat, online-multiplayer, async-multiplayer, pass-turn, status-panel, goal-counter, popup-text, game-screen, main-menu, match-setup, end-screen, settings-window, achievements-window, +hex-grid-render, +reserved-cells, +placement-bonus-cells, +adjacency-income, +adjacency-scoring, +global-parameters, +parameter-step-bonus, +production-engine, +resource-conversion, +standard-projects, +card-requirements, +card-tags, +milestones-awards, +escalating-fund-cost, +research-buy-cards, +actions-per-turn, +pass-until-all-passed]
proposes: ["+trigger:round_end", "+trigger:all_passed", "+cond:afford", "+cond:requirement", "+effect:raise_param", "+effect:production", "+effect:claim", "+ui:global-tracks", "+ui:generation-counter", "+ui:production-board", "+ui:card-hand", "+window:draft-window", "+window:production", "+card:global-parameters", "+card:adjacency-income", "+card:milestones-awards"]
author: opus
date: 2026-11-09
---

# Terraforming Mars — корпорації кладуть океани, озеленення й міста на 61 гекс Марса, доки три глобальні параметри не дійдуть до цілі

## Суть
Кожен гравець — корпорація, що за кілька поколінь робить Марс придатним до життя: підіймає температуру, кисень і кількість океанів. Ядро — двигун виробництва з карт проєктів (гроші, сталь, титан, рослини, енергія, тепло), а на карті — гексова сітка з бонусами клітин і сусідськими правилами: океан платить сусідам, місто рахує сусідні озеленення, озеленення тягнеться до своїх тайлів. Кожен крок глобального параметра підіймає рейтинг тераформування (TR) — це і очки, і базовий дохід. Гра спільна за метою (параметри одні на всіх) і змагальна за рахунком.

## Поле і час
- **Карта**: регіон Тарсис, 61 гекс; кожен тайл — 1 % поверхні. Типи ділянок: звичайні; блакитні низини, зарезервовані лише для океанів; 3 ділянки, зарезервовані під конкретні міста-карти (напр. Noctis).
- На ділянках надруковані **бонуси розміщення**: рослини (біля екватора), сталь і титан (гірські хребти), добір карт (особливі місця) — їх отримує той, хто кладе тайл.
- **Поза картою**: треки температури, кисню, TR (довкола карти) і покоління; стос 9 океанів; планшет гравця з 6 ресурсами й виробництвом; рука карт.
- **Час**: покоління = раунд з 4 фаз (черговість → дослідження → дії → виробництво). У фазі дій гравці по колу роблять по 1–2 дії або пасують; фаза триває, доки всі не спасують.
- Кінець: коли всі три параметри досягли цілі — гра завершується після виробництва того покоління.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ділянка карти (гекс) | terrain | тип: звичайна / океанська / зарезервована під місто; бонус розміщення | порожня або з тайлом; бонус дається при розміщенні |
| Океанська ділянка | zone | лише для океанів | інші тайли сюди не кладуться |
| Зарезервована ділянка міста | zone | 3 штуки, кожна під свою карту | лише відповідне місто (Noctis тощо) |
| Тайл океану | tile | нічий; 9 на гру | +1 TR; кожен сусідній новий тайл дає власнику 2 M€ |
| Тайл озеленення | tile | маркер власника; 1 ПО | +1 крок кисню; кладеться біля свого тайла, якщо можливо; +1 ПО кожному сусідньому місту |
| Тайл міста | tile | маркер власника | не поруч з іншим містом; наприкінці 1 ПО за кожне сусіднє озеленення (будь-чиє) |
| Столиця | tile | спецмісто з карти | рахує як місто + ПО за сусідні океани |
| Спецтайли | tile | з карт | розміщення й функція — за текстом карти |
| Маркер гравця | mark | колір гравця | позначає власника тайла / використану блакитну карту |
| Глобальний параметр: температура | counter | −30 → +8 °C | крок = +1 TR; на окремих поділках бонус (тепло-виробництво; океан при 0 °C) |
| Глобальний параметр: кисень | counter | 0 → 14 % | крок = +1 TR; бонус на 8 % |
| Глобальний параметр: океани | counter | 0 → 9 | кожен покладений океан = +1 TR |
| TR (рейтинг тераформування) | counter | старт 20 (соло 14) | = базові ПО і частина доходу M€ |
| Мегакредити (M€) | resource | виробництво ≥ −5 | гроші; дохід = TR + виробництво M€ |
| Сталь / титан | resource | 2 M€ / 3 M€ | оплата карт з тегом «будівля» / «космос» |
| Рослини | resource | — | 8 → тайл озеленення |
| Енергія | resource | — | на початку виробництва вся стає теплом |
| Тепло | resource | — | 8 → +1 крок температури |
| Карта проєкту | piece | ціна, теги, вимоги (параметри), ефект, ПО | грається з руки; блакитні — дія раз на покоління; події — одноразові |
| Карта корпорації | piece | стартові гроші / здібність | обирається на старті |
| Віха (milestone) | pickup | 8 M€, макс. 3 заявлено, 5 ПО | Terraformer, Mayor, Gardener, Builder, Planner |
| Нагорода (award) | pickup | 8 / 14 / 20 M€, макс. 3 | Landlord, Banker, Scientist, Thermalist, Miner; 1 місце 5 ПО, 2 — 2 ПО |
| Маркер першого гравця | object | — | зсувається за годинниковою щопокоління |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(player_order)` → ЯКЩО `custom: «покоління > 1»` → ТО `move(first_player_marker, clockwise)`, `counter(generation, +1)`.
- КОЛИ `phase_start(research)` → ЯКЩО `custom: «покоління > 1»` → ТО `custom: «кожен бере 4 карти, купує 0–4 по 3 M€, решту скидає; ліміту руки нема»`.
- КОЛИ `turn_start(player)` у фазі дій → ТО `choose(1–2 дії: карта / стандартний проєкт / віха / нагорода / дія блакитної карти / 8 рослин → озеленення / 8 тепла → температура)` або `pass_turn`.
- КОЛИ `input(play_card)` → ЯКЩО `custom: «вимоги карти виконано (рівні параметрів, теги)»` and `custom: «вистачає M€ (сталь/титан за тегом)»` → ТО `currency(-cost)`, `custom: «ефект карти»`; інакше `block`.
- КОЛИ `input(standard_project)` → ЯКЩО `custom: «вистачає M€»` → ТО продаж патентів: `take(cards)`, `currency(+n)` · електростанція 11 M€ → `custom: «+1 виробництво енергії»` · астероїд 14 → `counter(temperature, +1)` · акваферма 18 → `place(ocean)` · озеленення 23 → `place(greenery)` · місто 25 → `place(city)`, `custom: «+1 виробництво M€»`.
- КОЛИ `input(place(ocean, cell))` → ЯКЩО `cell(cell, ocean_area)` and `free(cell)` → ТО `place(ocean)`, `counter(oceans, +1)`, `counter(TR, +1)`.
- КОЛИ `input(place(greenery, cell))` → ЯКЩО `free(cell)` and (`adjacent_count(own_tile, >=, 1)` or `custom: «біля своїх тайлів місця нема»`) and `not cell(cell, ocean_area)` → ТО `place(greenery)`, `custom: «+1 крок кисню»`.
- КОЛИ `input(place(city, cell))` → ЯКЩО `free(cell)` and `adjacent_count(city, =, 0)` and `not cell(cell, ocean_area)` → ТО `place(city)`; інакше `block` (виняток — Noctis на своїй ділянці).
- КОЛИ `custom: «тайл покладено»` → ЯКЩО `custom: «на ділянці бонус»` → ТО `give(player, bonus)` (рослини / сталь / титан / карти).
- КОЛИ `custom: «тайл покладено»` → ЯКЩО `adjacent_count(ocean, >=, 1)` → ТО `currency(+2 × кількість сусідніх океанів)`.
- КОЛИ `counter(param, +1)` → ЯКЩО `custom: «параметр ще не на цілі»` → ТО `counter(TR, +1)`; інакше `custom: «TR не росте, ефект карти все одно грається без штрафу»`.
- КОЛИ `custom: «температура / кисень дійшли до поділки з бонусом»` → ТО `custom: «бонус: виробництво тепла / океан при 0 °C / крок температури при 8 % кисню»` (каскад).
- КОЛИ `input(convert_plants)` → ЯКЩО `has(player, plants, 8)` → ТО `take(plants, 8)`, `place(greenery)`.
- КОЛИ `input(convert_heat)` → ЯКЩО `has(player, heat, 8)` → ТО `take(heat, 8)`, `counter(temperature, +1)`.
- КОЛИ `input(claim_milestone)` → ЯКЩО `custom: «умову віхи виконано»` and `count(claimed_milestones, <, 3)` → ТО `currency(-8)`, `give(player, milestone)`.
- КОЛИ `input(fund_award)` → ЯКЩО `count(funded_awards, <, 3)` → ТО `currency(-(8 | 14 | 20))` (ціна росте з кожною профінансованою).
- КОЛИ `input(blue_action)` → ЯКЩО `not state(card, used)` → ТО `custom: «дія карти»`, `set_state(card, used)`.
- КОЛИ `custom: «усі гравці спасували»` → ТО `phase_start(production)`.
- КОЛИ `phase_start(production)` → ТО `custom: «енергія → тепло»`, `currency(+TR + виробництво M€)`, `custom: «інші ресурси за виробництвом»`, `clear_state(blue_cards, used)`.
- КОЛИ `custom: «виробництво M€ впало б нижче −5 / інше нижче 0»` → ТО `block`.
- КОЛИ `custom: «температура, кисень і океани на цілі»` → ТО `custom: «доіграти покоління з виробництвом; потім кожен по черзі ще раз міняє рослини на озеленення»`, `game_over`.
- Рахунок: TR + нагороди (5 / 2; у грі вдвох 2-го місця нема; рівність ділить місце) + віхи (5 кожна) + 1 за озеленення + 1 за кожне озеленення біля свого міста + ПО з карт.
- Перемога: найбільше ПО; рівність — більше M€.
- Соло: старт TR 14, гра триває до кінця 14-го покоління.

## Керування і ввід
- Цифрова версія: клік по карті в руці → перевірка вимог і оплата (вибір, скільки сталі/титану покласти); тайл — клік по підсвіченому гексу з легальних.
- Кнопки стандартних проєктів, віх і нагород — на окремих панелях; «пас» завершує участь у фазі дій.
- Фаза дослідження — вибір 0–4 карт з 4 (купівля по 3 M€).
- Черга: по колу від першого гравця; 1 або 2 дії за хід.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): соло, онлайн, локальна гра на спільному екрані, налаштування.
- `match-setup`: кількість гравців, доповнення (DLC), вибір корпорації — `character-select`.
- `game-screen`: гексова карта з бонусами, треки температури / кисню / TR довкола, лічильник океанів, `+ui:generation-counter`, планшет ресурсів і виробництва (`+ui:production-board`), рука карт (`+ui:card-hand`), зіграні карти з тегами.
- `+window:draft-window` — дослідження: 4 карти, позначка купівлі.
- Панелі стандартних проєктів, віх і нагород (цифрова версія; `custom-window`).
- `+window:production` — підсумок виробництва покоління.
- HUD: `score`/TR, `coins` (M€), `turn-indicator`, `legal-move-highlight` для гексів, `tooltip` над картою, `popup-text` (+2 M€ за океан).
- `end-screen`: розкладка рахунку (TR, нагороди, віхи, тайли, карти).
- `settings-window`, `achievements-window`.
- Переходи: main-menu → match-setup → game-screen ⇄ draft-window / production → end-screen.

## Фічі поза полем
- `online-multiplayer` (через акаунт Asmodee), локальна гра на спільному екрані (`hotseat`), соло.
- Хід-нотифікації Steam — асинхронна гра.
- `achievements`, `localization` (6 мов з озвученням).
- DLC: Hellas & Elysium (нові мапи), Venus Next, Prelude, Colonies, промо — `custom-rules` як набір увімкнених доповнень.

## Варіації й родичі
- Доповнення: Hellas & Elysium (2017, інші мапи — та сама гексова логіка), Venus Next (5-й параметр), Prelude, Colonies, Turmoil, Prelude 2, Milestones and Awards, Automa (соло), Amazonis & Vastitas, Utopia & Cimmeria (2024, мапи).
- Спін-офи: Ares Expedition (2021, карткова без карти), dice-версія (2023), пінбол-стіл.
- Родичі за гексами/сусідством: Kingdom Builder (обмеження розміщення біля своїх), Five Tribes, Tigris & Euphrates; за двигуном виробництва — The Castles of Burgundy.
- **Осі варіацій**: мапа (Тарсис / Hellas / Elysium …) · кількість глобальних параметрів (3 / +Венера) · бонус сусідства (гроші за океан / ПО за озеленення біля міста) · обмеження розміщення (біля свого / не біля міста / лише зарезервоване).

## Цікавинки для курсу
- Гекс-сітка з типами ділянок і бонусами розміщення: легальні клітини для кожного тайла (озеленення «біля свого, якщо можливо») — 📎.
- Сусідські ефекти: +2 M€ за кожен сусідній океан, ПО міста за сусідні озеленення — 📎 (сусіди в гекс-координатах).
- Глобальні параметри з поділками-бонусами й каскадом (кисень 8 % → температура → 0 °C → океан) — 🥉.
- Двигун виробництва: фаза виробництва, енергія → тепло, нижні межі (−5 для M€) — 🥉.
- Карти з вимогами й тегами, оплата сталлю/титаном за тегом — 🥈 (дані карт + перевірка вимог + оплата змішаними ресурсами).
- Віхи (перший заявив) і нагороди (ціна росте, рахунок з нічиїми й правилом «без 2-го місця вдвох») — 📎.
- Повний рушій 200+ карт з ефектами — 👑 (мова опису ефектів, порядок тригерів).

## Мапа на каталог
- Є: `cell-click` · `hover-highlight` · `legal-move-highlight` (гекси) · `round-currency` (M€ і виробництво) · `event-points` · `turn-enforcement` · `hot-seat` · `online-multiplayer` · `async-multiplayer` · `pass-turn` · `status-panel` · `goal-counter` (параметри до цілі) · `popup-text` · вікна `game-screen` / `main-menu` / `match-setup` / `end-screen` / `settings-window` / `achievements-window`.
- **Нема** → пропозиції карток:
  - `+global-parameters` «Спільні глобальні параметри з ціллю» · game-logic/score · 🥉 · слоти {min, max, step, bonus_marks} — кінець гри, коли всі на цілі.
  - `+adjacency-income` «Дохід за сусідство» · game-logic/economy · 📎 · слот {neighbor: ocean, amount: 2}.
  - `+adjacency-scoring` — ПО міста за сусідні озеленення.
  - `+reserved-cells` · `+placement-bonus-cells` — типи ділянок і надруковані бонуси.
  - `+production-engine` «Виробництво й фаза доходу» · game-logic/economy · 🥉.
  - `+milestones-awards` «Віхи й нагороди» · game-logic/score · 📎 · слоти {max: 3, costs: [8, 14, 20]}.
  - `+card-requirements` · `+card-tags` — умови гри карти й теги для оплати/рахунку.
  - `+standard-projects` · `+resource-conversion` · `+research-buy-cards` · `+actions-per-turn` · `+pass-until-all-passed` · `+escalating-fund-cost` · `+parameter-step-bonus` · `+hex-grid-render`.

## Пропозиції до словників
- `+trigger:round_end` — кінець покоління/раунду (тут — фаза виробництва як подія).
- `+trigger:all_passed` — усі гравці спасували, фаза закінчується.
- `+cond:afford(a, cost)` — вистачає валюти (з урахуванням замінників: сталь/титан).
- `+cond:requirement(card)` — вимоги карти до стану світу (рівень параметра, теги).
- `+effect:raise_param(p, n)` — підняти глобальний параметр (з TR і каскадом бонусів).
- `+effect:production(res, ±n)` — змінити виробництво ресурсу (не сам ресурс).
- `+effect:claim(x)` — заявити віху/нагороду.
- `+ui:global-tracks` — треки спільних параметрів довкола поля; `+ui:generation-counter`; `+ui:production-board` — планшет ресурс/виробництво; `+ui:card-hand`.
- `+window:draft-window` — вибір карт з N; `+window:production` — підсумок доходу.
- `+card:global-parameters` · `+card:adjacency-income` · `+card:milestones-awards`.

## Джерела
- ⭐ [UltraBoardGames: Terraforming Mars rules](https://www.ultraboardgames.com/terraforming-mars/game-rules.php) — тайли й правила розміщення, параметри, фази покоління, дії A–G, стандартні проєкти з цінами, віхи, нагороди, кінець, рахунок, соло.
- [Wikipedia: Terraforming Mars](https://en.wikipedia.org/wiki/Terraforming_Mars_(board_game)) — 61 гекс, цілі параметрів, доповнення і спін-офи, відеогра 2018.
- [Steam: Terraforming Mars](https://store.steampowered.com/app/800270/Terraforming_Mars/) — режими цифрової версії, DLC, досягнення, мови.
- YouTube: пошук «Terraforming Mars board game how to play».

## Непевне
- (?) Кількість океанських ділянок на Тарсисі і точний розклад бонусів по гексах — не перевірено.
- (?) Крок температури (2 °C на крок) і розташування бонусних поділок (−24, −20, 0 °C) — з памʼяті; джерело каже лише про «певні рівні».
- (?) Кольори карт (зелені автоматичні / блакитні активні / червоні події) — UBG згадує блакитні й події, кольорів повністю не перевірено.
- (?) Назви зарезервованих ділянок, крім Noctis, — не перевірено.
- (?) Меню, туторіал і рівні AI цифрової версії — Steam про них не пише; вікна зібрані як «(цифрова версія)».
