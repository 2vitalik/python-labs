---
title: Sprawlopolis
slug: sprawlopolis
aka: []
family: board-digital
also: [build-sim]
klass: cursor
axes:
  field: square
  time: turn
  opponent: coop
  info: hidden
  random: both
  goal: score
year: 2018
platforms: [board]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/sprawlopolis/game-rules.php", best: true, note: "правила: 3 карти умов і цільовий рахунок, передача руки, викладання з перекриттям, підрахунок, соло, складність"}
  - {kind: other, url: "https://rulespal.com/sprawlopolis/rulebook", note: "те саме + кольори зон, список доповнень, сумісність з Agropolis/Naturopolis"}
  - {kind: other, url: "https://www.meeplemountain.com/reviews/sprawlopolis/", note: "огляд: приклад міста 8×8, умови Park hopping / Superhighway, дороги"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Sprawlopolis", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sprawlopolis+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 60
mechanics: [cell-click, drag-drop-piece, hover-highlight, legal-move-highlight, tile-rotate, connectivity-check, field-scaling, event-points, rule-variants, match-setup, end-screen, help-window, score-records, +connected-group-scoring, +random-scoring-goals, +public-objectives, +target-score-win, +overlap-placement, +pass-hand-left, +road-segment-penalty, +largest-group-per-type, +deck-top-visible, +unbounded-field]
proposes: ["+trigger:deck_empty", "+cond:overlaps", "+cond:edge_contact", "+effect:cover", "+effect:pass_hand", "+ui:target-score", "+ui:goal-cards", "+ui:zone-groups", "+window:goal-reveal", "+card:target-score-win", "+card:overlap-placement", "+card:road-segment-penalty"]
author: opus
date: 2026-11-09
---

# Sprawlopolis — кооперативне місто з 18 карт: карти перекривають одна одну, а три випадкові правила очок задають ціль партії

## Суть
Колода — 18 карт: на лицьовому боці квартали чотирьох зон (житлова, комерційна, промислова, парки) і дороги; на звороті — унікальна умова очок із числом. На старті 3 карти відкладають зворотом догори: їхні умови діють цю партію, а сума їхніх чисел — **цільовий рахунок**. Решта 15 карт по одній викладаються в спільне місто, і їх можна класти **частково поверх** уже покладених, перебудовуючи квартали. Команда виграє, якщо рахунок ≥ цілі.

## Поле і час
- Спільне поле — необмежена сітка кварталів; карта = прямокутник з кількох кварталів (див. «Непевне»), кладеться горизонтально, можна розвернути на 180°.
- Шари: нова карта може перекрити частину старих — видимий верхній квартал; підсовувати карту під інші не можна.
- Хід: стартовий гравець з 3 картами в руці грає одну, передає 2 ліворуч (той стає наступним стартовим із 3), добирає одну. 15 ходів на партію.
- Соло: рука 3 карти, після ходу добір до 3, доки колода не скінчиться.
- Інформація: руки приховані, але обговорювати можна все; верхня карта колоди лежить лицем догори — видно, що прийде.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Карта міста | tile | квартали 4 зон + відрізки доріг; зворот — умова і число | кладеться з контактом по ребру кварталу або перекриттям |
| Квартал | zone | тип: residential / commercial / industrial / park | видимий верхній; групи по ребрах рахуються |
| Дорога | static | неперервна ділянка доріг | −1 за кожну окрему дорогу (звʼязна ділянка = одна) |
| Карта умови | object | 3 на партію, номер-число | дає ± очки за своєю умовою; сума чисел = ціль |
| Колода | supply | 15 карт лицем догори | верхня видна всім |
| Рука | supply | 3 у стартового / 1 в інших | прихована; відкрита карта мусить зіграти |
| Місто | zone | спільне | росте й перекривається |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт: КОЛИ `game_start` → ТО `custom: «3 випадкові карти — умови цієї партії; ціль = сума їхніх чисел»`; верхня карта колоди — стартова в місті.
- КОЛИ `turn_start(p)` → ЯКЩО `custom: «p має 3 карти»` → ТО `choose(card)`; відкрита карта мусить бути зіграна.
- КОЛИ `input(place(card, pos))` → ЯКЩО `custom: «≥1 спільне ребро кварталу з містом або перекриття ≥1 кварталу»` and `custom: «не лише кутом»` and `custom: «не під наявну карту»` and `custom: «горизонтально, поворот лише на 180°»` → ТО `place(card, pos)`; інакше `block`. Діри в місті дозволені.
- КОЛИ `custom: «карта перекрила квартали»` → ТО `custom: «нижні квартали й дороги більше не існують для підрахунку»`.
- КОЛИ `custom: «карту зіграно»` → ТО `custom: «2 решта карт передаються ліворуч»` і `custom: «гравець добирає 1 з колоди»` (колода порожня — без добору).
- КОЛИ `custom: «зіграно всі 15 карт»` → ТО підрахунок.
- Зони: для кожного типу `custom: «найбільша звʼязна по ребрах група кварталів»` → `score(+1 × кварталів)`; при рівних групах — гравці обирають.
- Дороги: `score(−1 × доріг)` — `custom: «неперервна ділянка доріг будь-якої довжини = одна дорога»`.
- Умови: для кожної з 3 карт `custom: «± очки за текстом умови»` (напр. довжина найдовшої дороги, парки поруч з житлом) — деякі віднімають.
- Перемога: ЯКЩО `custom: «зони − дороги ± умови ≥ ціль»` → ТО `win`; інакше `lose`.
- Легше: `custom: «дороги не віднімають»` · Важче: `custom: «рахується найбільша група лише одного типу»`.

## Керування і ввід
- Цифрова версія: вибір карти з руки → drag на поле з «привидом» карти, що показує контакти й перекриті квартали; клавіша/кнопка поворот 180°.
- Підсвітка легальних позицій: дотик по ребру або перекриття, без кутового дотику.
- Перед підтвердженням — превʼю рахунку: як зміняться найбільші групи, кількість доріг і очки умов.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Соло · Кооператив → `match-setup` · Правила → `help-window`.
- `match-setup`: кількість гравців (1–4 (?)), складність (легше / звичайна / важче), модулі доповнень.
- `goal-reveal` (кандидат): три карти умов з текстом і числами, `target-score`.
- `game-screen`: місто (зум/скрол); рука; верхня карта колоди; `goal-cards` (3 умови з поточними очками); `zone-groups` — підсвітка найбільших груп кожного типу; лічильник доріг; `score-preview` проти `target-score`; `remaining-counter` (карт у колоді).
- `end-screen`: розклад рахунку (зони, дороги, умови) проти цілі, перемога/поразка; `score-records` для соло.
- Переходи: main-menu → match-setup → goal-reveal → game-screen ×15 → end-screen.

## Фічі поза полем
- `mode-coop` — уся команда проти цілі; соло — той самий режим з рукою 3.
- `difficulty-presets` (дороги без штрафу / один тип зон).
- `custom-rules` / `expansion-toggle`: Beaches, Construction Zones, Interstate, Points of Interest, Wrecktar (монстр перекриває карту), комбінування з Agropolis і Naturopolis.
- `seed-input` / `daily-puzzle` — природна фіча: фіксовані 3 умови + порядок колоди.

## Варіації й родичі
- Серія Button Shy «‑opolis»: Agropolis, Naturopolis, Casinopolis, Ultimopolis, Combopolis.
- Родичі: [harmonies](harmonies.md), [cascadia-calico](cascadia-calico.md) (найбільша група за типом), [cartographers](cartographers.md) (випадкові цілі партії), [tiny-towns](tiny-towns.md); перекриття карт — Honshu (?).
- **Осі варіацій**: перекриття (заборонене / частково / повністю) · цілі (фіксовані / 3 випадкові з колоди) · гравці (змагання / кооп проти цілі) · штраф (дороги / порожні клітини) · рахується (найбільша група / усі групи).

## Цікавинки для курсу
- Поле з шарів: кожна карта — 2D-патерн кварталів; видимий стан = останній покладений квартал у клітині; валідатор «ребро або перекриття, не кут, не під» — 📎.
- Найбільша звʼязна група кожного типу (flood fill по видимих кварталах) — 🌱.
- Дороги як компоненти звʼязності по відрізках на краях кварталів (−1 за компоненту) — 🥉.
- 18 карт = 18 функцій підрахунку з одним інтерфейсом; ціль = сума номерів трьох обраних — 🥉 (патерн «стратегія»).
- Превʼю рахунку для позиції під курсором (перерахунок усіх груп і умов) — 📎.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `hover-highlight` · `legal-move-highlight` · `tile-rotate` (лише 180°) · `connectivity-check` (групи зон, дороги) · `field-scaling` · `event-points` · `rule-variants` · `match-setup` · `end-screen` · `help-window` · `score-records`.
- **Нема** → пропозиції карток:
  - `+connected-group-scoring` · `+random-scoring-goals` · `+public-objectives` · `+unbounded-field` — уже в корпусі.
  - `+target-score-win` «Перемога, якщо рахунок ≥ цілі партії» · game-logic/score · 🌱 · слоти {target: sum(goal_cards)}.
  - `+overlap-placement` «Нова фігура/карта може перекрити частину старих» · entities/legality · 📎 · слоти {under: forbidden, corner_only: forbidden}.
  - `+pass-hand-left` «Передати решту руки сусіду» · game-logic/opponent · 🌱.
  - `+road-segment-penalty` «−1 за кожну окрему звʼязну дорогу» · game-logic/score · 🥉.
  - `+largest-group-per-type` «Очки лише за найбільшу групу кожного типу» · game-logic/score · 🌱.
  - `+deck-top-visible` «Верх колоди відкритий усім» · interface/hud · 🌱.

## Пропозиції до словників
- `+trigger:deck_empty` — колода/карти вичерпано (також Arboretum).
- `+cond:overlaps(card, cells)` — нова карта перекриває ≥1 наявний квартал.
- `+cond:edge_contact(card, city)` — дотик ≥1 ребром (кутовий не рахується).
- `+effect:cover(cells)` — покрити клітини новим шаром (нижні зникають для підрахунку).
- `+effect:pass_hand(dir)` — передати карти руки сусіду.
- `+ui:target-score` — ціль партії поруч із поточним рахунком.
- `+ui:goal-cards` — у сімʼї вже раз; тут 3 умови з поточними ± очками.
- `+ui:zone-groups` — підсвітка найбільших груп кожного типу.
- `+window:goal-reveal` — розкриття цілей партії перед стартом.
- `+card:target-score-win` · `+card:overlap-placement` · `+card:road-segment-penalty`.

## Джерела
- ⭐ [UltraBoardGames: Sprawlopolis rules](https://www.ultraboardgames.com/sprawlopolis/game-rules.php) — 18 карт, ціль, передача руки, викладання, підрахунок, соло, складність.
- [RulesPal: Sprawlopolis rulebook](https://rulespal.com/sprawlopolis/rulebook) — кольори зон, доповнення, сумісність з Agropolis/Naturopolis.
- [Meeple Mountain: Sprawlopolis review](https://www.meeplemountain.com/reviews/sprawlopolis/) — місто 8×8 кварталів, Park hopping, Superhighway, підрахунок доріг.
- BGG: [пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=Sprawlopolis); YouTube: пошук «Sprawlopolis how to play».

## Непевне
- (?) Скільки кварталів на карті й як розміщені (найімовірніше 4 = 2×2, по одному кожної зони: огляд показує місто 8×8 з ~16 карт) — правила прямо не кажуть.
- (?) Огляд Meeple Mountain пише «cards can't overlap», правила UBG/RulesPal — «overlap or cover» дозволено; у файлі — за правилами.
- (?) Чи можна повністю перекрити наявну карту — RulesPal: правила не уточнюють.
- (?) Кількість гравців (1–4) і повний перелік 18 умов — не бачив.
- (?) Цифрових версій не знайдено; Honshu як родич — з памʼяті.
