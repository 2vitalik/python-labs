---
title: Akropolis (Акрополіс)
slug: akropolis
family: board-digital
also: [build-sim]
klass: cursor
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: score
year: 2022
platforms: [board, web]
links:
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=akropolis", best: true, note: "BGA: опис, правила-витяг (ціна каменями, будування вгору, формула очок), варіанти районів, грати в браузері"}
  - {kind: other, url: "https://en.doc.boardgamearena.com/Gamehelpakropolis", note: "BGA game help: покриття ≥2 тайлів, кар'єри → камені, таблиця кількостей площ і районів на 2/3/4"}
  - {kind: wiki, url: "https://fr.wikipedia.org/wiki/Akropolis_(jeu)", note: "FR-вікі: п'ять районів і їхні умови, As d'Or 2023"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Akropolis", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Akropolis+board+game+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 75
mechanics: [cell-click, drag-drop-piece, hover-highlight, legal-move-highlight, turn-enforcement, hot-seat, ai-opponent, round-currency, event-points, game-settings, +hex-grid-render, +tri-hex-tile, +tile-rotate, +connected-placement, +stacked-layers-scoring, +skip-cost-market, +cover-reward, +support-rule, +connected-group-scoring, +neighbor-difference-rule, +edge-district-rule, +surround-reward, +plaza-multiplier, +scoring-gate, +leftover-currency-score]
proposes: ["+trigger:round_end", "+trigger:placed", "+effect:place", "+effect:rotate", "+effect:currency", "+cond:fits", "+cond:afford", "+cond:supported", "+cond:connected", "+cond:adjacent_count", "+role:supply", "+role:tile", "+role:zone", "+ui:opponent-boards", "+ui:score-preview", "+ui:height-badge", "+window:match-setup", "+feature:custom-rules", "+axis:turn-structure", "+axis:field=hex+layers"]
author: opus
date: 2026-11-02
---

# Akropolis — гекс-тріади кладуть поруч або на інші: висота множить район, площа множить колір

## Суть
Кожен гравець будує своє місто з тайлів-тріад (три гекси трикутником). Тайл можна покласти на рівень землі поруч із містом **або поверх уже покладених**, якщо під ним нема порожнечі. Кожен гекс — район одного з пʼяти кольорів, площа (множник кольору) або каменоломня. Очки району = висота × зірки площ його кольору, але лише якщо район задовольняє своє просторове правило (житло — одна найбільша група, ринок — без сусідів-ринків, казарма — на краю, храм — оточений, сад — будь-де).

## Поле і час
- **Особисте поле** — нескінченна гекс-площина без меж; місто росте від стартового тайла. **Третій вимір**: тайли складаються в стоси, у кожного гекса є рівень (1, 2, 3…). Для коду — `dict[(q, r)] → stack[list[hex]]`, видно лише верхній гекс.
- **Спільна зона** — «будмайданчик» (construction site): ряд відкритих тайлів, N+2 для N гравців (?); 11 закритих стосів для поповнення.
- Хід = купити один тайл з будмайданчика + покласти. Раунд = поки на майданчику не лишиться один тайл; він стає першим, ряд доповнюється з наступного стосу, маркер першого гравця переходить.
- Партія — 12 раундів (початковий ряд + 11 стосів); 15–25 хв.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тайл-тріада | tile | 3 гекси трикутником; вміст кожного гекса | купується з майданчика, обертається (6 орієнтацій), кладеться на землю або поверх |
| Стартовий тайл | static | 4 гекси: синя площа ★1 + 3 каменоломні (?) | центр міста гравця |
| Житло (синій) | terrain | — | рахується лише найбільша звʼязна група житла |
| Ринок (жовтий) | terrain | — | рахується, якщо жоден сусід — не ринок |
| Казарма (червоний) | terrain | — | рахується, якщо на краю міста (є порожній сусід) |
| Храм (фіолетовий) | terrain | — | рахується, якщо оточений з усіх 6 боків |
| Сад (зелений) | terrain | — | рахується завжди |
| Площа (plaza) | zone | колір, ★1 (синя) / ★2 (жовта, червона, фіолетова) / ★3 (зелена) | сума зірок площ кольору = множник цього кольору; 0 зірок → колір не рахується |
| Каменоломня (quarry) | terrain | — | очок не дає; коли її накривають — +1 камінь |
| Камінь | resource | лічильник у гравця; стартово 1/2/3/4 за чергою (?) | платіж за пропуск тайлів; 1 очко в кінці; тай-брейк |
| Будмайданчик | supply | N+2 тайлів (?), впорядкований ряд | перший тайл безкоштовний, k-й коштує k−1 каменів |
| Стос тайлів | supply | 11 закритих стосів | поповнює майданчик щораунду |
| Маркер першого гравця | piece | — | переходить по колу в кінці раунду |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(take(i))` → ЯКЩО `afford(stones ≥ i−1)` → ТО `currency(−(i−1))`, тайл у руку; інакше `block`.
- КОЛИ `input(place(tile, cells, rot))`, рівень 1 → ЯКЩО `free(cells)` and `adjacent(tile, city)` → ТО `place`.
- КОЛИ `input(place(tile, cells, rot))`, рівень h+1 → ЯКЩО `supported(cells)` (усі 3 гекси лежать на гексах рівня h, без «повітря») and `custom: «тайл накриває ≥2 різних тайли»` → ТО `place`; інакше `block`.
- КОЛИ `placed(tile)` → ТО для кожної накритої каменоломні `currency(+1)`; накриті гекси перестають існувати для рахунку.
- КОЛИ `custom: «на майданчику лишився один тайл»` → ТО він зсувається на першу позицію, `spawn(row)` з нового стосу, маркер першого — далі; `round_end`.
- КОЛИ `custom: «стос для поповнення відсутній»` → ТО `game_over` після 12-го раунду.
- Рахунок кольору c: `S_c = Σ★ площ кольору c`; ЯКЩО `S_c = 0` → 0; інакше `S_c × Σ height(hex)` по районах c, що проходять умову:
  - житло: лише гекси найбільшої `connected` групи житла;
  - ринок: `adjacent_count(hex, market, ==, 0)`;
  - казарма: `adjacent_count(hex, empty, ≥, 1)` — на краю міста;
  - храм: `adjacent_count(hex, any, ==, 6)` — оточений;
  - сад: без умови.
- Фінал: Σ кольорів + 1 очко за камінь. Перемога — найбільше очок; нічия → більше каменів.
- Варіанти (подвоєння, BGA): житло — група вартістю ≥10; ринок — поруч з ринковою площею; казарма — 3–4 порожні сусіди; храм — на рівні ≥2; сад — поруч з «озером» (порожня клітина, оточена містом).

## Керування і ввід
- Цифрова версія (BGA): клік по тайлу будмайданчика (ціна показана каменями) → тайл «у руці»; клік по гексу міста ставить привид; кнопки/колесо — поворот; підтвердження. Легальні позиції підсвічуються.
- Перегляд чужих міст — перемикання вкладок/мініатюр; 3D-вигляд з висотою стосів.
- Черга: по колу від маркера першого гравця.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): власне місто (гекс-поле з тінями рівнів), будмайданчик з цінами, лічильник стосів, `coins` (камені), `score-preview` за кольорами, `opponent-boards`.
- `match-setup`: кількість гравців, варіанти районів (5 перемикачів), соло-бот.
- `end-screen`: таблиця 5 кольорів × (зірки × висоти) + камені.
- HUD: `turn-indicator`, `remaining-counter` (стоси), `height-badge` (рівень гекса), `legal-move-highlight`, `drag-ghost`, `tooltip` з умовою району.
- Переходи: lobby → match-setup → game-screen → end-screen.

## Фічі поза полем
- `custom-rules` — п'ять варіантів районів як перемикачі.
- Соло проти автомата-архітектора (?) з рівнями складності — `ai-opponent-levels`.
- BGA: `online-multiplayer`, `turn-timer`, `stats`, `leaderboard-online` (ELO), `replay`.
- `undo` у межах ходу до підтвердження (BGA-типово) (?).

## Варіації й родичі
- Доповнення Athena (?) — додаткові цілі-статуї.
- Родичі: NMBR 9 (стоси з опорою, очки × рівень), Taluva (гекс-тріади з висотою, вулкани), Kingdomino/Cascadia (вільна прибудова), Patchwork/Century (ціна = позиція в ряду).
- **Осі варіацій**: третій вимір (нема / стоси з опорою / стоси з вимогою «≥2 тайли під») · множник кольору (зірки площ / фіксований / за кількістю) · умова району (група / ізоляція / край / оточення / без умови) · ринок (безкоштовний вибір / ціна за пропуск / драфт).

## Цікавинки для курсу
- Стос на гекс-полі: перевірка опори «усі три гекси на рівні h і під ними ≥2 різні тайли» — 🥉 (3D-стан поверх 2D-сітки).
- П'ять умов району як п'ять предикатів над сусідством (група, ізоляція, край, оточення, завжди) — 🥉 за набір, кожен окремо 📎.
- Найбільша звʼязна група з урахуванням лише верхніх гексів (flood fill по гекс-сусідству) — 📎.
- Ціна = кількість пропущених у ряду + камені як валюта і очки одночасно — 🌱.
- Гекс-координати (axial/cube), 6 поворотів тріади — 📎.
- AI-жадібний: перебір (позиція × поворот × рівень × вибір тайла) з оцінкою приросту — 🥇.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `hover-highlight` · `legal-move-highlight` · `turn-enforcement` · `hot-seat` · `ai-opponent` · `round-currency` (камені) · `event-points` · `game-settings` (варіанти).
- **Нема** → пропозиції карток:
  - `+hex-grid-render` — див. hex.md; тут гекс-площина без меж + висоти.
  - `+tri-hex-tile` «Тайл з трьох гексів трикутником» · entities/state · 📎 · слоти {rotations: 6} — гекс-родич `+domino-tile`.
  - `+tile-rotate` · `+connected-placement` — як у Kingdomino; тут прибудова без збігу місцевості.
  - `+stacked-layers-scoring` — як у Odin/NMBR 9; тут «висота × множник кольору».
  - `+skip-cost-market` «Ціна = кількість пропущених у ряду» · game-logic/economy · 🌱 · слоти {first_free: true}.
  - `+cover-reward` «Нагорода за накриття клітини певного типу» · game-logic/economy · 🌱 — каменоломня → камінь.
  - `+support-rule` «Новий шар лише на повній опорі, ≥2 тайли під» · entities/legality · 🥉 · слоти {min_under: 2}.
  - `+connected-group-scoring` — як у Kingdomino; тут лише найбільша група житла.
  - `+neighbor-difference-rule` — як у Sagrada; тут ринок не торкається ринку.
  - `+edge-district-rule` «Клітина рахується лише на краю області» · game-logic/score · 🌱.
  - `+surround-reward` — як у Cartographers; тут храм оточений з 6 боків.
  - `+plaza-multiplier` «Окремі клітини-множники для типу» · game-logic/score · 📎 — зірки площ.
  - `+scoring-gate` «Тип не рахується без хоча б одного ключа» · game-logic/score · 🌱 — без площі колір = 0.
  - `+leftover-currency-score` «Невитрачена валюта = очки й тай-брейк» · game-logic/score · 🌱.

## Пропозиції до словників
- `+trigger:round_end` · `+trigger:placed` — як у Kingdomino/Carcassonne; тут накриття каменоломень.
- `+effect:place` · `+effect:rotate` · `+effect:currency` — як у сусідів.
- `+cond:fits` · `+cond:afford` · `+cond:supported` (є в корпусі: опора знизу) — тут «три гекси на тому ж рівні».
- `+cond:connected` · `+cond:adjacent_count` — використано для п'яти умов районів.
- `+role:supply` (майданчик, стоси) · `+role:tile` · `+role:zone` (площа як множник кольору).
- `+ui:opponent-boards` · `+ui:score-preview` · `+ui:height-badge` — цифра рівня/тінь на гексі.
- `+window:match-setup` · `+feature:custom-rules` (варіанти районів).
- `+axis:turn-structure` = `round-robin`; `+axis:field=hex+layers` — значення осі для «гекс зі стосами» (одна вісь не вміщує обидва).

## Джерела
- ⭐ [BGA: Akropolis](https://en.boardgamearena.com/gamepanel?game=akropolis) — опис, Jules Messaud / Gigamic 2022, правила-витяг, формула очок, варіанти районів, гра онлайн.
- [BGA game help](https://en.doc.boardgamearena.com/Gamehelpakropolis) — покриття ≥2 різних тайлів, каменоломні → камені, кількості площ/районів на 2/3/4 гравців, 11 стосів.
- [Wikipedia FR: Akropolis](https://fr.wikipedia.org/wiki/Akropolis_(jeu)) — умови п'яти районів, As d'Or 2023, Tric Trac.
- BGG: пошук «Akropolis»; YouTube: пошук «Akropolis board game how to play».

## Непевне
- (?) Стартовий тайл (синя площа + 3 каменоломні) і стартові камені 1/2/3/4 за чергою — з памʼяті, джерела не наводять.
- (?) Розмір будмайданчика N+2 — з памʼяті; BGA каже лише «перший безкоштовний, далі 1 камінь за кожен пропущений».
- (?) «Край міста» для казарми = хоча б один порожній сусід — трактування; джерела кажуть «on the edge».
- (?) Соло-автомат і його рівні, доповнення Athena — не перевірено.
- (?) Офіційного застосунку/Steam немає (пошук Steam — 0 результатів); цифрова версія підтверджена лише на BGA.
