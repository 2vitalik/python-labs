---
title: "Next Station: London"
slug: next-station-london
aka: [Next Station London, Next Station Tokyo, Next Station Paris]
family: board-digital
also: [connect-rotate]
klass: cursor
axes:
  field: graph
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2022
platforms: [board, web]
links:
  - {kind: other, url: "https://rulespal.com/next-station-london/rulebook", best: true, note: "повні правила: 11 карт, секції по сірих лініях, без перетинів, стрілка, формула очок, пересадки, модулі, соло-таблиця"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=nextstation", note: "BGA: Matthew Dunstan, 1–4 гравці, модулі, Solo Daily Challenge, грати в браузері"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Next+Station+London", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Next+Station+London+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 70
mechanics: [cell-click, hover-highlight, legal-move-highlight, path-preview, simultaneous-versus, online-multiplayer, event-points, daily-puzzle, game-settings, match-setup, rule-variants, game-screen, end-screen, help-window, score-records, +flip-and-write, +simultaneous-turns, +graph-edge-drawing, +no-crossing-edges, +extend-from-endpoints, +symbol-match-target, +wild-card, +branch-switch, +round-end-by-count, +rotating-color-rounds, +district-product-scoring, +crossing-bonus-edge, +interchange-scoring, +escalating-track-score, +public-objectives, +once-per-round-power, +solo-rank-table]
proposes: ["+cond:edge_free", "+cond:on_line", "+effect:draw_edge", "+trigger:card_flipped", "+role:station", "+role:objective", "+ui:flipped-card", "+ui:line-score-preview", "+ui:underground-count", "+feature:solo-rank-table", "+card:no-crossing-edges", "+card:district-product-scoring", "+card:branch-switch"]
author: opus
date: 2026-11-09
---

# Next Station: London — flip-and-write метро: відкрита карта каже форму станції, ти тягнеш пряму секцію з кінця своєї лінії, не перетинаючи жодної проведеної

## Суть
Чотири раунди — чотири лінії метро чотирма олівцями. Ведучий відкриває карти станцій по одній; після кожної всі одночасно можуть провести одну пряму секцію з будь-якого кінця своєї поточної лінії до станції показаної форми (квадрат, трикутник, пʼятикутник, коло), не проходячи крізь станції й не перетинаючи жодної проведеної секції. Раунд закінчується на 5-й «підземній» карті. Очки лінії = кількість районів, через які вона пройшла, × найбільша кількість її станцій в одному районі, плюс 2 за кожен перетин Темзи; у кінці — бонуси за туристичні місця й пересадки. Ядро — граф станцій з планарним обмеженням «без перетинів», що з кожним раундом стискає простір для наступних ліній.

## Поле і час
- Особиста карта Лондона: станції чотирьох форм + центральна «?», сірі «потенційні лінії» (ребра графа — горизонталь, вертикаль, діагональ), 13 районів (9 основних і 4 кутові з однією станцією), Темза, 5 туристичних місць.
- Секція = ребро між двома станціями вздовж сірої лінії; лінія = шлях (з гілками після «стрілки»).
- Тік = відкрита карта; раунд = від першої карти до 5-ї підземної; гра = 4 раунди; у кожному раунді новий колір і нова стартова станція.
- Гравці не взаємодіють, крім передачі олівців (яка лінія тобі випаде наступною).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Станція | static | форма: квадрат / трикутник / пʼятикутник / коло; район | ціль секції, коли форма збігається з картою |
| Стартова станція | static | одна на колір олівця | перша секція раунду виходить звідси; для інших ліній — звичайна |
| Центральна станція «?» | static | будь-яка форма; туристичне місце | до неї можна вести за будь-якої карти |
| Туристичне місце | zone | 5 станцій з компасом | у кінці раунду — хрестики на треку (≤10) |
| Потенційна лінія | static | сіре ребро між станціями | лише по ній можна провести секцію |
| Секція | mark | колір лінії; чи під Темзою | не проходить крізь станцію; не перетинає іншу секцію |
| Лінія | zone | колір; станції; гілки | рахується в кінці раунду |
| Пересадка | zone | 2 / 3 / 4 лінії | станція на кількох лініях: 2 / 5 / 9 очок |
| Район | zone | 13; основні й кутові | множник «районів» і «станцій у районі» |
| Темза | terrain | ділянки під рікою | секція під Темзою — +2 |
| Карта станції | supply | 11: 6 вуличних + 5 підземних | форма; підземна п'ята закінчує раунд |
| Джокер | supply | одна з карт (?) | гравець обирає будь-яку форму |
| Стрілка (Switch) | supply | одна з карт (?) | наступна карта одразу; секцію можна вести з будь-якої станції лінії — гілка |
| Олівець | supply | 4 кольори | визначає стартову станцію; передається ліворуч |
| Сила олівця | supply | 4 (модуль) | раз за раунд: подвійна секція / подвоєна станція |
| Спільна ціль | supply | 5, з них 2 у грі (модуль) | +10 за виконання |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(round)` → ТО `custom: «перетасувати 11 карт; кожен бере колір олівця і його стартову станцію»`.
- КОЛИ `custom: «ведучий відкрив карту»` (`+trigger:card_flipped`) → ТО кожен гравець може провести одну секцію (необовʼязково).
- КОЛИ `input(draw(section, a, b))` → ЯКЩО `custom: «a — стартова станція (перша секція) або кінець своєї лінії»` і (`same(b, card, shape)` або `cell(b, central)`) → ТО перевірити далі; інакше `block`.
- КОЛИ `input(draw(section, a, b))` → ЯКЩО `custom: «по сірій лінії, не крізь станцію, не перетинає жодної проведеної секції будь-якого кольору»` (`+cond:edge_free`) → ТО `mark(section, color)`; інакше `block`.
- КОЛИ `input(draw(section, a, b))` → ЯКЩО `custom: «b уже на цій лінії або між a і b вже є секція»` (`+cond:on_line`) → ТО `block`.
- Джокер: КОЛИ `custom: «відкрито джокер»` → ТО `choose(shape)` кожен окремо.
- Стрілка: КОЛИ `custom: «відкрито стрілку»` → ЯКЩО `counter(cards_in_round, >, 2)` → ТО `custom: «одразу відкрити наступну карту; секцію можна вести з будь-якої станції лінії — нова гілка»`; інакше ігнорується.
- КОЛИ `counter(underground_cards, =, 5)` → ТО `custom: «остання секція за формою цієї карти»`, підрахунок лінії.
- Очки лінії: ТО `score(+districts × max_stations_in_district)` + `score(+2)` за кожну секцію під Темзою.
- Туристичні місця: КОЛИ `turn_end(round)` → ТО `counter(tourist_track, +k)` (k — туристичні місця на лінії; трек ≤10).
- КОЛИ `turn_end(round)` → ЯКЩО `counter(round, <, 4)` → ТО `custom: «передати олівець ліворуч, взяти справа; ведучим стає сусід ліворуч»`.
- КОЛИ `counter(round, =, 4)` → ТО `game_over`; `score(+lines)` + `score(+tourist: найлівіше незакреслене)` + `score(+2 / +5 / +9)` за кожну пересадку з 2 / 3 / 4 ліній.
- Модуль «Сила олівця»: КОЛИ `input(power(double))` → ЯКЩО `not state(power, used)` → ТО `extra_move` (друга секція до тієї ж форми), `set_state(power, used)` до кінця раунду; «подвоєна станція» — `custom: «одна станція лінії рахується як дві в районі»`.
- Модуль «Спільні цілі»: КОЛИ `custom: «виконано ціль (≥8 пересадок / усі 13 районів / усі 5 туристичних / 9 станцій центрального району / ≥6 перетинів Темзи)»` → ТО `score(+10)`.
- Соло: ТО `custom: «−10 за кожен модуль; рейтинг за таблицею <90 … >150»`.
- Перемога: найбільше очок · Тайбрейк: найкраща одна лінія → спільна перемога · Поразка: — · Рахунок: лінії + туристи + пересадки (+ цілі).

## Керування і ввід
- Паперово: олівцем провести пряму між двома станціями.
- (цифрова версія; BGA) Клік по кінцю лінії → підсвічуються досяжні станції потрібної форми (`legal-move-highlight`, `path-preview` секції); клік — провести; кнопка «пропустити»; після стрілки — клік по будь-якій станції лінії як початку гілки.
- Сила олівця — кнопка біля олівця (раз за раунд).

## Вікна, меню, HUD
(цифрова версія; BGA)
- `lobby-window` / `match-setup`: 1–4 гравці, модулі (спільні цілі, сили олівців), Solo Daily Challenge.
- `game-screen`: карта Лондона з лініями; `flipped-card` — поточна карта; `underground-count` — скільки підземних уже відкрито (з 5); поточний олівець і стартова станція; `line-score-preview` (райони × станції + Темза); трек туристів; спільні цілі; `opponent-boards`.
- `end-screen`: таблиця 4 ліній + туристи + пересадки + цілі; для соло — рейтинг.
- `daily-window`: соло-щоденний виклик (потрібно ввімкнути обмін даними з видавцем).
- `help-window`: правила секцій і формула очок.
- Переходи: lobby-window → game-screen ×4 раунди → end-screen.

## Фічі поза полем
- `daily-puzzle` / `mode-daily`: Solo Daily Challenge на BGA (однаковий порядок карт для всіх (?)).
- `custom-rules`: модулі спільних цілей і сил олівців (окремо або разом).
- `online-multiplayer`; `stats` (ELO BGA); `localization` (десятки мов).
- Соло-рейтинг (`+feature:solo-rank-table`): шість титулів від «LAST STOP!» до «Underground expert».

## Варіації й родичі
- Next Station: Tokyo (?) і Paris (?) — та сама система з новими картами й правилами.
- Родичі: Railroad Ink (мережі з кидка), Welcome To (flip-and-write), Ticket to Ride (маршрути між містами), Flow Free й Lyne (лінії без перетинів), Mini Metro (відео-гра про метро).
- **Осі варіацій**: звідки продовжувати (лише кінці / будь-яка станція після стрілки) · що задає ціль (форма / колір / район) · перетини (заборонені / мости) · як рахується лінія (райони × станції / довжина / пересадки) · порядок кольорів (передача олівців / фіксований).

## Цікавинки для курсу
- Граф станцій із «потенційними ребрами» на площині; секція = ребро — 🌱.
- Перевірка перетину відрізків (орієнтація трьох точок) і «не крізь станцію» — 📎.
- Лінія як шлях з двома кінцями; після стрілки — дерево з гілками — 📎.
- Підрахунок «районів × максимум станцій у районі» + перетини Темзи — 🌱.
- Колода, що закінчує раунд на 5-й підземній карті (змінна довжина раунду) — 🌱.
- Пересадки між раундами: облік станцій на кількох лініях — 🌱.
- AI-порадник: куди вести лінію, щоб не замкнути себе (оцінка майбутніх форм з колоди) — 🥇.

## Мапа на каталог
- Є: `cell-click` · `hover-highlight` · `legal-move-highlight` · `path-preview` ↔ превʼю секції · `simultaneous-versus` · `online-multiplayer` · `event-points` · `daily-puzzle` ↔ Solo Daily · `match-setup` · `rule-variants` ↔ модулі · `score-records` · `game-screen`, `end-screen`, `help-window`.
- **Нема** → пропозиції карток:
  - `+graph-edge-drawing` «Провести ребро між вузлами графа» · interface/input · 📎.
  - `+no-crossing-edges` «Ребра не перетинаються (планарність)» · game-logic/constraints · 📎.
  - `+extend-from-endpoints` «Продовжувати шлях лише з кінців» · entities/legality · 🌱; `+branch-switch` «Карта дозволяє гілку з будь-якого вузла» · 📎.
  - `+symbol-match-target` · `+wild-card` · `+round-end-by-count` («5-та підземна») · `+rotating-color-rounds` — по 🌱.
  - `+district-product-scoring` «Райони × максимум у районі» · game-logic/score · 🌱.
  - `+crossing-bonus-edge` (Темза) · `+interchange-scoring` (2/5/9) · 🌱.
  - `+once-per-round-power` · `+solo-rank-table` · 🌱.

## Пропозиції до словників
- `+cond:edge_free` — ребро вільне: не перетинає проведених і не проходить крізь вузол.
- `+cond:on_line` — вузол уже належить цій лінії.
- `+effect:draw_edge` — провести ребро між двома вузлами (Next Station, Lyne, Hashi).
- `+trigger:card_flipped` — ведучий відкрив карту (flip-and-write).
- `+role:station` — вузол графа з типом (форма станції).
- `+role:objective` — спільна ціль поза полем.
- `+ui:flipped-card` · `+ui:underground-count` · `+ui:line-score-preview`.
- `+feature:solo-rank-table` — титул за діапазоном очок у соло.
- `+card:no-crossing-edges` · `+card:district-product-scoring` · `+card:branch-switch` — див. «Мапа на каталог».

## Джерела
- ⭐ [RulesPal: Next Station London rulebook](https://rulespal.com/next-station-london/rulebook) — компоненти (11 карт: 6 вуличних, 5 підземних), 13 районів, правила секцій, джокер і стрілка, формула очок, пересадки 2/5/9, сили олівців, спільні цілі, соло-таблиця.
- [BGA: Next Station London](https://en.boardgamearena.com/gamepanel?game=nextstation) — автор, 1–4 гравці, модулі, Solo Daily Challenge, інтерфейс.
- ⭐-лінк черги `ultraboardgames.com/next-station-london/game-rules.php` віддав індекс сайту без правил — у шапку не клав.
- BGG: [пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=Next+Station+London); YouTube: пошук «Next Station London how to play».

## Непевне
- (?) Склад 11 карт: скільки кожної форми, де джокер і стрілка (вуличні чи підземні) — джерело не розкладає.
- (?) Цінності треку туристів (найлівіше незакреслене) — лише на друкованому треку.
- (?) Який район «центральний» з 9 станціями і де стартові станції — карта не описана.
- (?) Чи дозволені петлі гілок після стрілки — правила кажуть лише «не повертатись у станцію своєї лінії».
- (?) Tokyo / Paris — інші правила (Tokyo, здається, з парками й мостами), не відкривав.
