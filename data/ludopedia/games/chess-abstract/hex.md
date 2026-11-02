---
title: Hex (Гекс)
slug: hex
family: chess-abstract
also: [connect-rotate]
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1942
platforms: [board, paper, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hex_(board_game)", best: true, note: "правила, чому нема нічиїх, swap, історія Hein/Nash, компʼютерний Hex, варіанти"}
  - {kind: fandom, url: "https://www.hexwiki.net/index.php/Swap_rule", note: "HexWiki: два способи swap, які перші ходи чесні"}
  - {kind: fandom, url: "https://www.hexwiki.net/", note: "HexWiki — стратегія, задачі, теорія"}
  - {kind: play, url: "https://playabstractgames.com/en/hex/", note: "браузер: гра проти AI"}
  - {kind: other, url: "http://www.mseymour.ca/hex_book/hexstrat.html", note: "Hex: A Strategy Guide (лінк зі статті Wikipedia)"}
  - {kind: other, url: "http://www.mseymour.ca/hex_puzzle/hexpuzzle.html", note: "500 Hex Puzzles (лінк зі статті Wikipedia)"}
  - {kind: other, url: "https://www.boardgamegeek.com/boardgame/4112", note: "BGG (лінк зі статті Wikipedia)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Havannah_(board_game)", note: "варіація: кільце / міст / вилка"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Y_(game)", note: "варіація: зʼєднати три сторони трикутника"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hex+board+game+rules+strategy", note: "пошук; правила й стратегія"}
stage: v1
coverage: 80
mechanics: [hot-seat, turn-enforcement, move-timer, ai-opponent, ai-random, ai-minimax, cell-click, hover-highlight, game-screen, main-menu, end-screen, help-window, settings-window, field-size-picker, difficulty-levels, replay, reachability-check, +place-stone, +connect-sides-win, +swap-rule, +hex-grid-render, +move-notation]
proposes: ["+trigger:connected", "+effect:place", "+cond:path_exists", "+effect:swap_sides", "+window:swap-dialog", "+ui:edge-colors", "+ui:swap-button", "+feature:swap-rule", "+card:connect-sides-win", "+card:swap-rule", "+card:hex-grid-render"]
author: opus
date: 2026-11-02
---

# Hex — став камені на гекс-ромбі, щоб зʼєднати свої дві протилежні сторони

## Суть
Двоє по черзі ставлять по одному каменю свого кольору в будь-яку порожню шестикутну клітину ромба n×n. Кожному належить пара протилежних сторін; хто першим зʼєднає свої сторони неперервним ланцюгом сусідніх каменів — виграв. Камені не ходять і не знімаються. Головна математична цікавинка: **нічиєї не буває** — заповнене поле завжди містить рівно один виграшний ланцюг, бо «зʼєднати своє» і «перегородити чуже» — одна дія.

## Поле і час
- Ромб n×n шестикутних клітин: стандарт 11×11, популярні 13×13 і 19×19; малі (≤9×9) розвʼязані перебором.
- Сусідство 6-звʼязне: у клітини (r, c) сусіди (r±1, c), (r, c±1), (r−1, c+1), (r+1, c−1) в осьових координатах.
- Сторони: червоний — верх і низ, синій — ліва і права (кольори умовні); кутові клітини належать обом сусіднім сторонам.
- Позначення клітин: літера-стовпець + число-рядок (a1, k11).
- Покроково, хід = один камінь. Без випадковості, повна інформація; грається навіть олівцем на папері.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Камінь | piece | колір red/blue | ставиться в порожню клітину; ніколи не рухається і не знімається |
| Порожня клітина | static | осьові координати | ціль ходу |
| Сторона поля | zone | належить кольору; 4 сторони | ціль зʼєднання; кут — у двох сторонах |
| Ланцюг (група) | zone | множина зʼєднаних каменів | виграє, коли торкається обох своїх сторін |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, cell)` → ЯКЩО `turn_of(side)` і `free(cell)` → ТО `spawn_at(stone(side), cell)`, `end_turn`; інакше `block`.
- КОЛИ `after(place)` (2-й хід партії, лише з правилом swap) → ЯКЩО `custom: «другий гравець обрав swap»` → ТО `custom: «swap sides — гравці міняються кольорами» або «swap pieces — перший камінь замінюється каменем другого кольору, віддзеркаленим через довгу діагональ (a3 → c1)»`.
- КОЛИ `after(place)` → ЯКЩО `custom: «група нового каменя торкається обох сторін кольору»` → ТО `win`.
- Нічиєї нема: `custom: «на заповненому полі рівно один гравець має зʼєднання»` (Hein 1942, Nash; Gale 1979 — еквівалентно теоремі Брауера про нерухому точку).
- Пасу нема — порожня клітина завжди є, доки ніхто не виграв.
- Здача (resign) — звичай, а не правило.
- Перемога: ланцюг між своїми сторонами · Поразка: суперник зʼєднав · Рахунок: нема.

## Керування і ввід
- Настільна/папір: поставити камінь (намалювати знак) у клітину.
- (цифрова версія) Клік по шестикутнику; наведення підсвічує клітину. Після першого ходу суперник бачить вибір «Swap / Play» (кнопка або діалог).
- Черга строго чергується.

## Вікна, меню, HUD
- (цифрова версія) `main-menu`: проти AI → `difficulty-select` · з другом (один пристрій / онлайн) · Правила → `help-window` · Задачі → `puzzle-select`.
- (цифрова версія) `game-screen`: гекс-ромб з `edge-colors` (сторони пофарбовані у кольори власників), `cell-coordinates`, `turn-indicator`, `last-move-highlight`, `move-list`, `swap-button` на 2-му ході, `resign-button`, `undo-button` (проти AI).
- (цифрова версія) `swap-dialog`: «Поміняти сторони?» після першого ходу.
- (цифрова версія) `end-screen`: переможець + підсвічений виграшний ланцюг.
- (цифрова версія) `settings-window`: розмір поля (7…19), swap увімк/вимк, хто перший, рівень AI.
- Переходи: main-menu → game-screen → (2-й хід) swap-dialog → game-screen → end-screen.

## Фічі поза полем
- `custom-difficulty` / `custom-rules`: розмір поля, swap-правило (стандарт — увімкнене).
- `ai-opponent-levels` (Play Abstract Games — гра проти AI); `hotseat`; `online-multiplayer` (LittleGolem — турніри (?)).
- `puzzle-bank` — задачі «хід і виграш» (500 Hex Puzzles); `mode-puzzle`.
- `history`, `replay`, `export-import` партій у нотації клітин.

## Варіації й родичі
- **Y** — трикутне поле з гексів, треба одним ланцюгом зʼєднати **всі три** сторони; нічиїх теж нема; Hex вкладається в Y як частковий випадок (Milnor; Schensted і Titus, 1953).
- **Havannah** (Freeling, 1979) — гексагон зі стороною 8/10, три фігури перемоги: **кільце** (оточити ≥1 клітину), **міст** (зʼєднати 2 з 6 кутів), **вилка** (зʼєднати 3 сторони, кути не рахуються); нічиї можливі, але рідкісні; Freeling програв програмі Lajkonik у 2012.
- Rex (Reverse Hex) — місер: програє той, хто зʼєднав; Dark Hex — каменів суперника не видно; Projex — проективна площина; TwixT і гра Шеннона — інші ігри зʼєднання.
- Осі варіацій: **форма поля** (ромб / трикутник / гексагон / проективна) · **ціль** (2 сторони / 3 сторони / кільце-міст-вилка / місер) · **інформація** (повна / темна) · **баланс першого ходу** (нема / swap sides / swap pieces).

## Цікавинки для курсу
- Перевірка перемоги: BFS/DFS або union-find від однієї сторони до іншої по 6-сусідству — 🥉 (union-find з віртуальними вузлами-сторонами — 🥈).
- Гекс-сітка в осьових координатах + рендер ромба (консоль зі зсувом рядків / GUI) — 🥉.
- Swap/pie rule як вікно-вибір на другому ході, два способи (сторони / віддзеркалення каменя) — 📎.
- AI: випадковий — 🌱; оцінка «двох відстаней» або резисторна мережа Шеннона — 🥇; MCTS (як у сильних програмах після 2006) — 👑.
- Доведення «нічиєї не буває» як тест: на будь-якому випадково заповненому полі рівно один переможець — 🥉 (property-тест).
- Havannah: виявлення **кільця** на гексах — 🥇 (замкнений цикл, що оточує клітину).

## Мапа на каталог
- Є: `hot-seat` + `turn-enforcement` · `move-timer` · `ai-opponent` / `ai-random` / `ai-minimax` · `cell-click` + `hover-highlight` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `field-size-picker` ↔ 11/13/19 · `difficulty-levels` · `replay` · `reachability-check` ↔ пошук зʼєднання між сторонами.
- **Нема** → пропозиції карток:
  - `+place-stone` «Хід виставленням» · entities/legality · 🌱 — фігура ставиться, а не ходить (Reversi, Hex, Go).
  - `+connect-sides-win` «Зʼєднати сторони» · game-logic/win · 🥉 · слот {sides: 2|3, shapes: [ring, bridge, fork]} — перемога ланцюгом між зонами краю.
  - `+swap-rule` «Правило swap (pie)» · game-logic/opponent · 📎 · слот {mode: sides|mirror} — другий гравець може забрати перший хід собі.
  - `+hex-grid-render` «Гекс-поле» · interface/render · 🥉 — осьові координати, сусідство, рендер ромба/гексагона.

## Пропозиції до словників
- `+trigger:connected` — група сутностей зʼєднала дві/три зони (сторони, кути); варіант `pattern(...)` з формою `connect(zones)` — потрібен для Hex, Y, Havannah, Bridg-It.
- `+effect:place` — поставити камінь у порожню клітину (спільне з Go, Reversi); у правилах вище — `spawn_at`.
- `+cond:path_exists` — існує шлях між точкою/групою і зоною (Hex — перемога, Quoridor — легальність стіни).
- `+effect:swap_sides` — гравці міняються кольорами/сторонами.
- `+window:swap-dialog` — вибір «поміняти / грати» на другому ході.
- `+ui:edge-colors` — сторони поля пофарбовані за власником цілі; `+ui:swap-button` — кнопка swap.
- `+feature:swap-rule` — увімкнення pie-правила як налаштування партії.
- `+card:connect-sides-win`, `+card:swap-rule`, `+card:hex-grid-render` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Hex](https://en.wikipedia.org/wiki/Hex_(board_game)) — правила, розміри полів, чому нема нічиїх, swap, стратегія крадіжки (перший виграє без swap), історія Hein → Nash → Parker Brothers 1952, PSPACE-повнота, розвʼязані поля до 9×9, варіанти.
- [HexWiki: Swap rule](https://www.hexwiki.net/index.php/Swap_rule) — swap sides vs swap pieces (віддзеркалення через довгу діагональ), які перші ходи чесні на 11×11.
- [HexWiki](https://www.hexwiki.net/) — стратегія, задачі, теорія.
- [Play Abstract Games: Hex](https://playabstractgames.com/en/hex/) — гра проти AI в браузері.
- [Hex: A Strategy Guide](http://www.mseymour.ca/hex_book/hexstrat.html) і [500 Hex Puzzles](http://www.mseymour.ca/hex_puzzle/hexpuzzle.html) — лінки зі статті Wikipedia, сам не відкривав.
- [BoardGameGeek: Hex](https://www.boardgamegeek.com/boardgame/4112) — лінк зі статті Wikipedia.
- [Wikipedia: Havannah](https://en.wikipedia.org/wiki/Havannah_(board_game)) і [Wikipedia: Y](https://en.wikipedia.org/wiki/Y_(game)) — варіації ігор зʼєднання.
- YouTube: пошук «hex board game rules strategy».

## Непевне
- (?) Набір функцій цифрових версій (swap-діалог, підсвітка ланцюга, puzzle-select) — типовий для онлайн-сайтів Hex, але конкретний сайт не перевірено: Play Abstract Games підтверджує лише гру проти AI.
- (?) LittleGolem як місце турнірів Hex — Wikipedia згадує його в контексті матчу Mootwo 2019, функції сайту не дивився.
- (?) Розподіл сторін за кольорами (червоний — верх/низ) різниться між джерелами й сайтами.
