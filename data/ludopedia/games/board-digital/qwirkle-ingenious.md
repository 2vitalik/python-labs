---
title: Qwirkle + Ingenious (Квіркл, Genial)
slug: qwirkle-ingenious
family: board-digital
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: score
year: 2006
platforms: [board, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Qwirkle", best: true, note: "повні правила Qwirkle: 108 плиток, рука 6, лінія без повторів, рахунок і бонус 6, обмін, кінець"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ingenious_(board_game)", note: "повні правила Ingenious: 120 подвійних гекс-плиток, промені з 5 граней, 18 і бонусний хід, обмін руки, перемога за найслабшим кольором"}
  - {kind: other, url: "https://www.redblobgames.com/grids/hexagons/", note: "Red Blob Games: гекс-координати, сусіди, промені — для коду Ingenious"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Qwirkle", note: "пошук BGG"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Ingenious", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Qwirkle+how+to+play", note: "пошук; пояснення правил"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ingenious+Knizia+board+game+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 75
mechanics: [cell-click, drag-drop-piece, hover-highlight, legal-move-highlight, turn-enforcement, hot-seat, ai-opponent, ai-greedy, event-points, completion-detection, no-moves-left, score-records, game-settings, +hand-of-tiles, +tile-bag-draw, +tile-exchange, +unbounded-field, +line-placement-rule, +attribute-line-rule, +line-run-scoring, +full-line-bonus, +empty-hand-bonus, +hex-grid-render, +domino-tile, +ray-scoring, +per-color-tracks, +weakest-track-wins, +track-cap-bonus-turn, +conditional-hand-swap, +start-symbols]
proposes: ["+trigger:placed", "+trigger:counter", "+effect:place", "+effect:extra_move", "+effect:counter", "+cond:same", "+cond:fits", "+cond:line_uniform", "+cond:in_line", "+role:supply", "+role:tile", "+ui:pocket", "+ui:score-preview", "+ui:color-tracks", "+ui:remaining-tiles", "+window:match-setup", "+axis:turn-structure"]
author: opus
date: 2026-11-02
---

# Qwirkle + Ingenious — плиткові «скрабли без слів»: склади лінію, порахуй довжину

## Суть
Дві класики, де очки = довжини ліній, які проходять через щойно покладені плитки. **Qwirkle** (2006, Susan McKinley Ross, MindWare): 108 плиток «6 форм × 6 кольорів × 3», кожна лінія на столі мусить мати **спільну ознаку** (усі одного кольору або однієї форми) і **без повторів** — отже не довша за 6; лінія з 6 — «Qwirkle», +6. **Ingenious** (2004, Reiner Knizia): гекс-поле, подвійні гекс-плитки з символами 6 кольорів; від кожної вільної грані покладеної плитки пускаємо промінь і рахуємо однакові символи підряд; очки ведуться **окремо по кольорах**, а переможця визначає **найслабший** колір.

## Поле і час
- **Qwirkle**: необмежена квадратна сітка (стіл); поле росте від першого ходу; поле спільне.
- **Ingenious**: спільне гекс-поле-шестикутник з 6 надрукованими стартовими символами (по одному кольору); зовнішні кільця — лише для 3–4 гравців.
- Рука прихована: 6 плиток (обидві гри); мішок/стос — випадкове поповнення.
- Хід = покласти (Qwirkle: 1–6 плиток в одну лінію; Ingenious: одну подвійну плитку) або обміняти. Партія — доки є ходи/плитки; 30–45 хв.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка Qwirkle | tile | колір ∈ 6, форма ∈ 6; 3 копії кожної з 36 (108) | кладеться в лінію за правилом ознаки |
| Лінія | zone | ознака (колір або форма), довжина ≤6 | максимальний неперервний ряд/стовпець; без дублікатів |
| Плитка Ingenious | tile | 2 гекси, по символу кольору на кожному; 15 різнокольорових × 6 + 6 однокольорових × 5 = 120 | займає 2 сусідні вільні гекси, будь-яка орієнтація |
| Стартовий символ | static | 6 на полі, по одному кольору | рахується в променях; перший хід кожного — поруч з іншим стартовим символом |
| Промінь | zone | напрям (з 6), колір | неперервний ряд однакових символів від грані плитки |
| Доріжка кольору | resource | 0–18 на колір, 6 доріжок у гравця | відкрита всім; 18 — стеля і бонусний хід |
| Рука | supply | 6 плиток, прихована | поповнюється до 6 з мішка |
| Мішок | supply | усі неприкладені плитки | поповнення й обмін |

## Правила (КОЛИ → ЯКЩО → ТО)
**Qwirkle**
- КОЛИ `game_start` → ТО кожен тягне 6; починає той, у кого найбільша група з руки, сумісна за ознакою; вона й іде першим ходом.
- КОЛИ `input(place(tiles))` → ЯКЩО `in_line(tiles)` (одна лінія, не обовʼязково впритул одна до одної) and `custom: «хоча б одна торкається наявної плитки»` and `line_uniform(every touched line)` (спільна ознака, нема двох однакових) → ТО `place`; інакше `block`.
- КОЛИ `placed(tiles)` → ТО `score(Σ len(line))` по кожній лінії, яку створено чи подовжено (плитка на перетині двох ліній рахується в обох).
- КОЛИ `pattern(line(6))` → ТО `score(+6)` («Qwirkle»: 6 + 6 = 12).
- КОЛИ `input(exchange(k))` → ТО k плиток у мішок, k нових, `score(0)`, хід закінчено.
- КОЛИ `turn_end` → ТО рука до 6 з мішка.
- КОЛИ `custom: «мішок порожній і гравець виклав останню плитку»` → ТО `score(+6)`, `game_over`. Перемога — найбільше очок.

**Ingenious**
- КОЛИ `input(place(tile, cells))` → ЯКЩО `free(cells)` and `fits(tile, board)` and (перший хід → поруч зі стартовим символом, ще не використаним іншим гравцем) → ТО `place`.
- КОЛИ `placed(tile)` → ТО для кожного гекса плитки й кожної з його 5 вільних граней: `counter(colour, +k)`, де k — кількість однакових символів підряд у промені (власна плитка не рахується); одна плитка може рахувати два кольори.
- КОЛИ `counter(colour, ≥, 18)` → ТО значення = 18 (стеля), `extra_move` («Ingenious!»); два кольори одночасно — два бонусні ходи; далі цей колір не росте.
- КОЛИ `counter(all_colours, ==, 18)` → ТО `win` негайно.
- КОЛИ `turn_end` → ЯКЩО `not has(hand, tile of my weakest colour)` → може показати руку, скинути її всю й набрати 6 нових; рука завжди добирається до 6.
- КОЛИ `no_moves(all)` (жодна плитка не лізе) → ТО `game_over`; перемагає найвищий **мінімальний** колір; нічия → порівняти другий найслабший і т. д.

## Керування і ввід
- Цифрова версія: рука внизу (`pocket`); drag плитки на поле або клік-плитка → клік-клітина; Ingenious — друга клітина задає орієнтацію подвійної плитки (6 напрямків) або кнопка повороту.
- Кнопки: «Підтвердити хід», «Обмін» (вибір плиток), «Скасувати» в межах ходу.
- Підсвітка легальних клітин; у Qwirkle — після першої плитки лишаються лише клітини тієї ж лінії.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Гра з AI / Hot-seat / Онлайн / Правила / Налаштування.
- `match-setup`: кількість гравців, рівень AI, розмір поля Ingenious (2 гравці — менший шестикутник).
- `game-screen`: поле (pan/zoom для Qwirkle), `pocket` (рука), `remaining-counter` (плиток у мішку), `score` гравців (Qwirkle) / `color-tracks` 6×(0–18) для кожного гравця (Ingenious), `turn-indicator`, `score-preview` до підтвердження.
- `confirm-dialog` для обміну; `end-screen` з рейтингом (Ingenious — «найслабший колір»).
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- `ai-opponent-levels`, `hotseat`, `online-multiplayer` (?), `tutorial`, `undo` в межах ходу.
- `stats` / `score-records` — найкращий рахунок, кількість Qwirkle за партію.
- `custom-rules`: Ingenious — розмір поля від кількості гравців; Qwirkle — без варіантів у базі.

## Варіації й родичі
- Qwirkle Cubes (кубики замість плиток), Qwirkle Cards (rummy), Qwirkle Trio (?).
- Ingenious Travel (2006, менше поле), Knobelspass (2007, пазл-версія), Junior (2007, квадратне поле), Mensa Connections (UK-назва).
- Родичі: Scrabble (рука + мішок + лінії, але слова), Take It Easy (рахунок суцільних ліній), Azul (суміжні ряди × стовпці), SET (ознаки «всі різні або всі однакові»), Sagrada.
- **Осі варіацій**: поле (квадрат без меж / гекс з межами) · правило лінії (спільна ознака без повторів / просто колір) · рахунок (довжина лінії / промені однакових) · агрегат очок (сума / мінімум по кольорах) · бонус (повна лінія / стеля доріжки → додатковий хід).

## Цікавинки для курсу
- Валідатор лінії Qwirkle: «одна спільна ознака + усі різні» для кожної зачепленої лінії, кілька плиток за хід — 📎.
- Рахунок ходу: усі лінії через нові плитки, плитка на перетині рахується двічі — 📎.
- Ingenious: промені з 5 вільних граней на гекс-сітці (axial-вектори) — 📎.
- «Перемога за мінімумом» — заохочує баланс; AI має максимізувати min-колір, а не суму — 🥉 (жадібний), 🥇 (з урахуванням руки й блокування).
- Стеля 18 + бонусний хід (ланцюг можливих бонусів) — 🌱.
- Умовний обмін руки (нема плиток найслабшого кольору) — 🌱.
- Генератор «чи є хоч один легальний хід» для кінця Ingenious — 🥉.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `hover-highlight` · `legal-move-highlight` · `turn-enforcement` · `hot-seat` · `ai-opponent` · `ai-greedy` · `event-points` · `completion-detection` · `no-moves-left` (кінець Ingenious) · `score-records` · `game-settings`.
- **Нема** → пропозиції карток:
  - `+hand-of-tiles` «Прихована рука з N плиток з добором» · game-logic/economy · 🌱 · слоти {size: 6}.
  - `+tile-bag-draw` · `+tile-exchange` — як у Scrabble/Mathable.
  - `+unbounded-field` — уже в корпусі; тут стіл без меж.
  - `+line-placement-rule` «Усі плитки ходу — в одній лінії» · entities/legality · 🌱 — родич Scrabble.
  - `+attribute-line-rule` «Лінія: спільна ознака, без повторів» · entities/legality · 📎 · слоти {attrs: [colour, shape], max: 6}.
  - `+line-run-scoring` — як у Take It Easy; тут довжина кожної зачепленої лінії.
  - `+full-line-bonus` «Бонус за лінію максимальної довжини» · game-logic/score · 🌱 — Qwirkle +6.
  - `+empty-hand-bonus` «Бонус за першу порожню руку» · game-logic/score · 🌱.
  - `+hex-grid-render` — див. hex.md.
  - `+domino-tile` — як у Kingdomino; тут гекс-доміно.
  - `+ray-scoring` «Очки = однакові символи по променях від граней» · game-logic/score · 📎 · слоти {directions: 5}.
  - `+per-color-tracks` «Окремий рахунок на кожен колір» · game-logic/score · 🌱.
  - `+weakest-track-wins` «Перемога за найслабшою доріжкою» · game-logic/win · 🌱 · тай-брейк лексикографічно.
  - `+track-cap-bonus-turn` «Стеля доріжки → додатковий хід» · game-logic/score · 🌱 · слоти {cap: 18}.
  - `+conditional-hand-swap` «Обмін руки лише за умови» · game-logic/economy · 🌱.
  - `+start-symbols` «Надруковані стартові клітини, перший хід поруч» · entities/legality · 🌱 — родич `+start-cell-rule` (Blokus).

## Пропозиції до словників
- `+trigger:placed` · `+trigger:counter(colour, ≥, 18)` — уже ⏳ `counter`.
- `+effect:place` · `+effect:extra_move` (уже ⏳) · `+effect:counter`.
- `+cond:line_uniform` — запропоновано Take It Easy; тут «спільна ознака + усі різні» (ширше: `uniform_or_distinct`).
- `+cond:in_line` — набір клітин лежить на одній прямій; `+cond:same` · `+cond:fits`.
- `+role:supply` (мішок, рука) · `+role:tile`.
- `+ui:pocket` (рука) · `+ui:score-preview` · `+ui:color-tracks` — шість доріжок 0–18 для кожного гравця · `+ui:remaining-tiles`.
- `+window:match-setup` · `+axis:turn-structure` = `round-robin` (з бонусними ходами).

## Джерела
- ⭐ [Wikipedia: Qwirkle](https://en.wikipedia.org/wiki/Qwirkle) — склад, сетап, хід, правила ліній, рахунок, бонус 6, кінець, варіанти Cubes/Cards, Spiel des Jahres 2011.
- [Wikipedia: Ingenious](https://en.wikipedia.org/wiki/Ingenious_(board_game)) — поле, 120 плиток, промені, 18 і бонусні ходи, обмін руки, перемога за найслабшим кольором, тай-брейки, редакції.
- [Red Blob Games: Hexagonal Grids](https://www.redblobgames.com/grids/hexagons/) — координати, сусіди, лінії — основа для коду Ingenious.
- BGG: пошуки «Qwirkle», «Ingenious»; YouTube: пошуки правил.

## Непевне
- (?) Цифрові версії не перевірено: Steam — 0 результатів для Qwirkle; BGA-сторінки обох ігор не відкрились (500). Мобільні застосунки — з памʼяті.
- (?) Розмір поля Ingenious (сторона шестикутника для 2 vs 3–4 гравців) — Вікі каже лише «зовнішні кільця для 3–4».
- (?) Два кольори до 18 одночасно → два бонусні ходи — у Вікі з позначкою «citation needed».
- (?) Qwirkle Trio та інші варіанти — з памʼяті.
