---
title: Kingdomino (Кінґдоміно)
slug: kingdomino
family: board-digital
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: setup
  goal: score
year: 2016
platforms: [board, PC, mobile, web]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/kingdomino/game-rules.php", best: true, note: "повні правила: розстановка за к-стю гравців, лінії доміно, черга за королями, зʼєднання, рахунок, варіанти"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kingdomino", note: "Spiel des Jahres 2017, спіноффи (Queendomino, Origins, Duel, Dragomino)"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=kingdomino", note: "грати в браузері (BGA): Mighty Duel, Harmony, Middle Kingdom як опції"}
  - {kind: steam, url: "https://store.steampowered.com/app/3029180/Kingdomino/", note: "Meeple Corp, 2025: AI, онлайн, локальна гра, квести, Mighty Duel 7×7, daily"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Kingdomino", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Kingdomino+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 75
mechanics: [cell-click, drag-drop-piece, hover-highlight, legal-move-highlight, turn-enforcement, hot-seat, ai-opponent, ai-greedy, event-points, game-settings, field-size-picker, leaderboard, daily-puzzle, +domino-tile, +tile-rotate, +connected-placement, +edge-matching, +bounded-grid-growth, +draft-order-by-value, +area-times-multiplier, +connected-group-scoring, +leftover-penalty, +discard-unplayable, +center-bonus]
proposes: ["+trigger:round_end", "+effect:draft", "+effect:place", "+effect:rotate", "+effect:discard", "+cond:fits", "+cond:edge_match", "+role:supply", "+role:tile", "+ui:opponent-boards", "+ui:score-preview", "+ui:draft-line", "+window:match-setup", "+axis:turn-structure"]
author: opus
date: 2026-11-02
---

# Kingdomino — королівство 5×5 з доміно: площа × корони, а сильний тайл сьогодні = останній вибір завтра

## Суть
Гравці по черзі обирають доміно з відкритої лінії і прибудовують їх до свого королівства навколо замку, щоб воно вмістилось у квадрат 5×5. Кожне доміно — дві клітини місцевості, деякі з коронами; очки за кожну звʼязну область однієї місцевості = кількість клітин × кількість корон у ній. Хитрість драфту: доміно пронумеровані за цінністю, і хто бере найкраще, той наступного раунду обирає останнім.

## Поле і час
- **Особисте поле**: королівство гравця, що росте від стартової клітини із замком; межа — будь-який квадрат 5×5 (у Mighty Duel — 7×7), положення квадрата не фіксоване наперед, лише його розмір.
- **Спільна зона**: дві лінії доміно — поточна (на ній стоять королі гравців) і наступна (на неї ставлять королів на цьому ході); стос з 48 доміно, нумерованих 1–48 на звороті.
- Хід = «покласти своє доміно з поточної лінії» + «поставити короля на доміно наступної лінії». Черговість — зверху вниз за номером доміно, на якому стоїть король.
- Партія: 12 раундів (3–4 гравці) або 6 раундів по 2 доміно (2 гравці); останній раунд — лише викладання.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Доміно | tile | номер 1–48 (зворот), 2 клітини, тип місцевості кожної, корони 0–3 на клітині | обирається королем, викладається поруч з королівством у будь-якій орієнтації |
| Клітина місцевості | terrain | тип ∈ {пшениця, ліс, озеро, луки, болото, шахта}, корони | зливається з сусідніми того ж типу в область |
| Стартова клітина із замком | static | 1×1, «джокер» | збігається з будь-якою місцевістю; варіант Middle Kingdom хоче її в центрі |
| Король (мейпл) | piece | колір гравця; 1 або 2 на гравця | стоїть на обраному доміно; позиція в лінії = черга ходу |
| Лінія доміно | supply | 3 або 4 доміно, відсортовані за номером | наповнюється зі стосу щораунду |
| Стос доміно | supply | 48 (2 гравці: 24, 3 гравці: 36) | випадковий порядок, номер відомий лише при викладанні в лінію |
| Область (property) | zone | тип, площа, сума корон | очки = площа × корони; без корон = 0 |
| Королівство | zone | межа 5×5 (7×7) | нове доміно не може вийти за межу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО кожен має замок на стартовій клітині; `spawn(line)` з N доміно (N = кількість королів), сортування за номером ↑, перевернути лицем; королі ставляться у випадковому порядку (перший раунд).
- КОЛИ `round_start` → ТО `spawn(next_line)` з N доміно, сортування ↑, лицем догори.
- КОЛИ `turn_start(king)` → ТО ходить король, що стоїть на доміно з найменшим номером поточної лінії (найближче до стосу), далі за зростанням.
- Дія 1: КОЛИ `input(place(domino, cells, orientation))` → ЯКЩО `fits(domino, kingdom_5x5)` and `edge_match(domino, kingdom)` → ТО `place`; інакше `block`.
- `edge_match`: хоча б одна клітина доміно ортогонально торкається клітини **тієї ж місцевості** або стартової клітини (джокер); діагоналі не рахуються.
- КОЛИ `custom: «для доміно нема легального місця»` → ТО `discard` (доміно зникає, очок не дає). Сюди ж — «не вміщається в 5×5 через погане планування».
- Дія 2: КОЛИ `input(claim(next_domino))` → ЯКЩО `free(next_domino)` → ТО `move(king, next_domino)`; останній гравець обирає з того, що лишилось.
- Наслідок: `custom: «доміно з більшим номером (рідкісна місцевість, більше корон) ставить короля нижче → наступного раунду цей гравець ходить пізніше»`.
- КОЛИ `custom: «стос порожній і лінія розіграна»` → ТО останній раунд лише з дією 1, потім `game_over`.
- Рахунок: для кожної області `score(+площа × корони)`; області без корон = 0.
- Варіант Middle Kingdom: КОЛИ `custom: «замок у центрі квадрата 5×5»` → ТО `score(+10)`.
- Варіант Harmony: КОЛИ `custom: «королівство 5×5 повне, жодне доміно не скинуто»` → ТО `score(+5)`.
- Варіант Dynasty: 3 партії поспіль, сума очок.
- Варіант Mighty Duel (2 гравці): усі 48 доміно, королівство 7×7.
- Перемога: більше очок; тай-брейк → найбільша область (незалежно від корон) → більше корон → спільна перемога.

## Керування і ввід
- Обрати доміно наступної лінії: клік по ньому (король переміщується).
- Викласти своє доміно: drag на поле, поворот на 90° (кнопка/клавіша/жест), підсвічені легальні позиції; підтвердити.
- Якщо легальних позицій нема — кнопка «скинути» (або автоматично).
- Дві дії ходу йдуть у фіксованому порядку: спершу викласти, потім обрати наступне.

## Вікна, меню, HUD
(цифрова версія — Meeple Corp/Steam, BGA)
- `main-menu`: Соло (expedition) · Проти AI · Онлайн · Локально (split-screen / pass-and-play, PvP і кооп) · Квести · Daily · Колекція (мейплі, замки) · Налаштування.
- `match-setup`: кількість гравців, AI-рівні, варіанти (Mighty Duel, Harmony, Middle Kingdom, Dynasty).
- `game-screen`: своє королівство з рамкою 5×5, що «прилипає» до вже зайнятих клітин; `draft-line` — дві лінії доміно з королями; `opponent-boards`; `turn-indicator`; `drag-ghost` доміно з `legal-move-highlight`; `score-preview` по областях; `remaining-counter` доміно в стосі.
- `end-screen`: таблиця областей кожного гравця (площа × корони), бонуси варіантів.
- `leaderboard` · `achievements-window` · `stats-window` (Steam).
- Переходи: main-menu → match-setup → game-screen → end-screen → main-menu.

## Фічі поза полем
- `ai-opponent-levels`, `online-multiplayer` (крос-платформа), `local-multiplayer`, `mode-coop`, `daily-puzzle` (щоденні виклики), квести (15+ задач з умовами), сезонні події.
- `unlockables` (мейплі, замки), `theme-select` (два стилі арту: класичний і новий), `achievements`, `cloud-save`, `stats`, `leaderboard-online`.
- `custom-rules`: варіанти Harmony/Middle Kingdom/Dynasty/Mighty Duel як перемикачі.

## Варіації й родичі
- **Queendomino** (2017): будівлі, лицарі-податки, дракон; **Age of Giants** (2018): велетні закривають корони; **Kingdomino Origins** (2021): вогонь замість корон, печерні люди; **Kingdomino Duel** (2019): roll-and-write; **Dragomino** (2021): дитяча.
- Родичі: Carcassonne і Dorfromantik (збіг місцевості), Patchwork/Cartographers (квадрат з межею), Isle of Skye (прибудова тайлів).
- **Осі варіацій**: межа (5×5 / 7×7 / без межі) · правило зʼєднання (хоча б одна сторона збігається / усі сторони / без збігу) · рахунок (площа×множник / площа / завдання) · порядок вибору (по колу / за цінністю взятого тайлу).

## Цікавинки для курсу
- Підрахунок очок: області однієї місцевості (flood fill / union-find) × сума корон — 📎.
- Межа 5×5 без фіксованого положення: перевірка, що bounding box усіх клітин ≤ 5×5 — 🌱, але красива ідея «рамка ковзає».
- Черга ходів = номер обраного тайлу: драфт, що сам балансує сильних — 🌱.
- Перевірка «чи є хоч одне легальне місце» (позиції × 4 орієнтації × збіг × рамка) для автоматичного скидання — 🥉.
- Middle Kingdom/Harmony як окремі оцінювачі-плагіни — 🌱.
- AI: жадібний (максимізувати приріст очок) — 🥉; з урахуванням черговості драфту й майбутніх місць — 🥇.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `hover-highlight` · `legal-move-highlight` · `turn-enforcement` · `hot-seat` · `ai-opponent` / `ai-greedy` · `event-points` · `game-settings` · `field-size-picker` (5×5 / 7×7) · `leaderboard` · `daily-puzzle`.
- **Нема** → пропозиції карток:
  - `+domino-tile` «Двоклітинний тайл з різними половинами» · entities/state · 📎 — родич `multi-cell-size`.
  - `+tile-rotate` — як у Dorfromantik; тут 4 орієнтації доміно.
  - `+connected-placement` — як у Sagrada; тут ортогонально, без «першого на краю».
  - `+edge-matching` — як у Dorfromantik/Carcassonne; тут «хоча б одна сторона», замок — джокер.
  - `+bounded-grid-growth` «Поле росте, але в межах рамки N×N» · entities/legality · 🌱 · слоти {n: 5|7}.
  - `+draft-order-by-value` «Хто взяв цінніше — обирає пізніше» · game-logic/opponent · 🌱.
  - `+area-times-multiplier` «Очки = площа × множник області» · game-logic/score · 📎.
  - `+connected-group-scoring` «Очки за звʼязні групи однакового типу» · game-logic/score · 📎 — Kingdomino, Cartographers, Isle of Cats.
  - `+leftover-penalty` — тут неявний: діра в 5×5 знімає Harmony.
  - `+discard-unplayable` «Тайл без легального місця скидається» · game-logic/constraints · 🌱.
  - `+center-bonus` «Бонус за стартову клітину в центрі» · game-logic/score · 🌱.

## Пропозиції до словників
- `+trigger:round_end` — нова лінія доміно; `+effect:draft` · `+effect:place` · `+effect:rotate` · `+cond:fits` — як у сусідах по теці.
- `+effect:discard` — тайл виходить з гри без ефекту (як у Azul — на підлогу).
- `+cond:edge_match` — запропоновано Dorfromantik; тут достатньо однієї сторони.
- `+role:supply` (стос, лінія) · `+role:tile`.
- `+ui:opponent-boards` · `+ui:score-preview` · `+ui:draft-line` — дві лінії тайлів (поточна з королями і наступна для вибору).
- `+window:match-setup` — як у Blokus: гравці, AI, варіанти.
- `+axis:turn-structure` = `draft-order`.

## Джерела
- ⭐ [UltraBoardGames: Kingdomino rules](https://www.ultraboardgames.com/kingdomino/game-rules.php) — склад, розстановка 2/3/4, лінії, черговість, зʼєднання, скидання, рахунок, тай-брейки, варіанти.
- [Wikipedia: Kingdomino](https://en.wikipedia.org/wiki/Kingdomino) — Бруно Катала, Spiel des Jahres 2017, Harmony, спіноффи, цифрова гра 2025.
- [BGA: Kingdomino](https://en.boardgamearena.com/gamepanel?game=kingdomino) — гра в браузері, варіанти як опції столу.
- [Steam: Kingdomino](https://store.steampowered.com/app/3029180/Kingdomino/) — режими цифрової версії (соло-експедиція, AI, онлайн, кооп, квести, daily, Mighty Duel).
- BGG: пошук «Kingdomino»; YouTube: пошук «Kingdomino how to play».

## Непевне
- (?) Шість типів місцевості й розподіл корон (шахти до 3 корон, пшениця найчастіша) — з памʼяті; джерела не перелічують.
- (?) Гра на 3: UltraBoardGames — лінія з 3 доміно і 36 у стосі; BGA описує «одне доміно скидається щораунду» (новіша редакція з 4 у лінії?) — розходиться.
- (?) Mighty Duel використовує всі 48 доміно попри стандартне «прибрати 24» для двох — так кажуть обидва джерела, механіка злиття правил не описана.
- (?) Пункти меню Steam-версії — з опису магазину, не з запуску.
