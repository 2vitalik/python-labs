---
title: "Puzzmo: Pile-Up Poker"
slug: pile-up-poker
aka: [Pile-Up Poker, Pileup Poker]
family: word-number
also: [board-digital]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: partial
  random: runtime
  goal: score
year: 2024
platforms: [web]
links:
  - {kind: other, url: "https://punishedbacklog.com/love-balatro-try-puzzmos-new-browser-game-pile-up-poker/", best: true, note: "правила: сітка 4×4, рука 5 карт, 4 на поле + 1 у скид, ряди/стовпці/кути, 10-та рука зі скиду"}
  - {kind: other, url: "https://preview-prod.w.houstonchronicle.com/about/newsroom-news/article/introducing-pileup-poker-19488552.php", note: "анонс 2024-06-03: фіксація карт після нової роздачі, спроби на день, спільний «банк» спільноти"}
  - {kind: play, url: "https://www.puzzmo.com/play/pile-up-poker", note: "грати (боту недоступно)"}
  - {kind: other, url: "https://adrianhon.substack.com/p/puzzmo", note: "платформа Puzzmo: daily, лідерборди, серії, групи, підписка"}
  - {kind: other, url: "https://pysolfc.sourceforge.io/doc/rules/pokersquare.html", note: "предок Poker Squares: 5×5, 10 рук рядами й стовпцями"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=puzzmo+pile+up+poker", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, drag-drop-piece, pocket, event-points, daily-puzzle, leaderboard, streak-stats, profile-stats, save-progress, game-screen, end-screen, help-window, +poker-hand-eval, +deal-place-discard, +line-hand-scoring, +discard-bonus-hand, +daily-attempt-limit, +community-goal]
proposes: ["+trigger:deal", "+effect:discard", "+cond:hand_rank", "+ui:hand-label", "+feature:daily-attempts", "+feature:community-goal"]
author: opus
date: 2026-11-09
---

# Puzzmo: Pile-Up Poker — пасьянс «покерні квадрати» 4×4: з кожної роздачі п'яти карт клади чотири на сітку, одну в скид

## Суть
Порожня сітка 4×4 і рука з п'яти карт. Щоходу гравець розкладає чотири карти по будь-яких вільних клітинах, п'яту скидає, і після нової роздачі попередні карти фіксуються. Після чотирьох роздач (16 карт на полі, 4 у скиді) кожен ряд і стовпець, а також чотири кути оцінюються як покерні руки; якщо всі дев'ять рук щось дали, скид стає десятою рукою. Гра — сучасна щоденна версія класичного пасьянсу Poker Squares; до «слів і чисел» вона близька як «комбінаторика рядків сітки».

## Поле і час
- Сітка 4×4; рука-роздача з 5 карт поза полем; скид — 4 слоти поза полем.
- Хід = одна роздача: розставити 4, скинути 1. Усього 4 роздачі — партія за хвилину-дві.
- Розставлене до нової роздачі ще можна переставити (?); після неї — фіксується.
- Оцінка — один раз наприкінці: 4 ряди + 4 стовпці + кути (+ скид).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Карта | tile | ранг, масть | у руці → на клітину або в скид; на полі — нерухома після нової роздачі |
| Клітина сітки | terrain | вільна / зайнята | приймає одну карту |
| Рука | zone | 5 карт | роздається щоходу з колоди |
| Скид | zone | 4 слоти | одна карта на роздачу; 10-та рука-бонус |
| Ряд / стовпець | zone | 4 клітини | оцінюється як покерна рука; без комбінації — 0 |
| Кути | zone | 4 кутові клітини | 9-та рука |
| Колода | spawner | склад і порядок приховані | джерело роздач; щоденна (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО `custom: «роздати 5 карт у руку»`.
- КОЛИ `input(drag card, cell)` → ЯКЩО `free(cell)` → ТО `place(player, card)`; інакше `block`.
- КОЛИ `input(drag card, discard)` → ЯКЩО `count(discard, <, 4)` і `custom: «з цієї роздачі ще не скинуто»` → ТО `custom: «карта йде в скид»`.
- КОЛИ `turn_end` → ЯКЩО `custom: «4 карти розставлено, 1 скинуто»` → ТО `set_state(placed cards, locked)`, `custom: «нова роздача»`.
- КОЛИ `counter(cards_on_grid, ==, 16)` → ТО `custom: «кінець партії — оцінка рук»`.
- КОЛИ `level_end` → ТО для кожного ряду, стовпця і кутів: `score(custom: «вартість найкращої покерної комбінації з 4 карт»)`.
- КОЛИ `level_end` → ЯКЩО `custom: «усі 9 рук мають комбінацію»` → ТО `score(custom: «скид як 10-та рука»)`.
- Пара, дві пари, трійка, стрит, флеш, каре тощо — лише з 4 карт: «повних» п'ятикарткових рук (фул-хаус, стрит-флеш з 5) нема (?).
- КОЛИ `level_end` → ТО `custom: «рахунок у денний лідерборд; внесок у спільний банк спільноти»`.
- КОЛИ `level_start` → ЯКЩО `counter(attempts_today, >=, limit)` → ТО `block`.
- Перемога: нема — рекорд дня · Поразка: нема · Рахунок: сума до 10 рук.

## Керування і ввід
- Перетягування карти з руки на клітину або в скид (миша/тач); клік-вибір карти й клік по клітині (?).
- Підтвердження роздачі після розстановки (?).

## Вікна, меню, HUD
- `game-screen`: сітка 4×4, рука з 5 карт (`pocket`), слоти скиду, підписи комбінацій біля рядів/стовпців (`hand-label`) (?), рахунок.
- `end-screen`: розбір 9–10 рук з очками, підсумок, перцентиль дня (типово для Puzzmo).
- `leaderboard`: денний / тижневий / місячний, групи друзів (платформа Puzzmo).
- `help-window`: правила й таблиця рук.
- Переходи: Today-сторінка Puzzmo → гра → результат → наступна спроба (якщо лишились).

## Фічі поза полем
- `daily-puzzle`: нова роздача щодня; `daily-attempts`: кілька спроб на день (кількість — у «Непевне»), підписка Puzzmo Plus дає більше.
- `community-goal`: спільний покерний «банк» гравців з цілями ($10 млрд → новий реліз, $1 трлн → сюрприз).
- Платформа: `streak-stats`, статистика для підписників, архів минулих днів, збереження між пристроями.

## Варіації й родичі
- Poker Squares / Poker Solitaire — 5×5, 25 карт, 10 рук (5 рядів + 5 стовпців), карти кладуть по одній; варіанти з резервом і скидом (PySol).
- Balatro — покерні руки як двигун очок; Pile-Up Poker — значно простіша, без джокерів і прокачки.
- Корпус: [sumplete.md](sumplete.md) (оцінка рядів і стовпців), [wordatro.md](wordatro.md) (покерна логіка зі словами), [scrabble.md](scrabble.md) (розміщення з руки).
- **Осі варіацій:** розмір сітки (4×4 / 5×5) · що оцінюється (ряди, стовпці / + кути / + діагоналі / + скид) · подача (по одній / роздача з вибором скиду) · фіксація (одразу / після роздачі).

## Цікавинки для курсу
- Оцінка покерної руки з 4–5 карт (класифікатор комбінацій) — 🌱.
- Роздача → розстановка → скид з фіксацією після нової роздачі — 🌱.
- Підрахунок рядів, стовпців, кутів і умовної бонус-руки — 🌱.
- AI-помічник «куди класти»: очікувана вартість за невідомими картами колоди — 🥇 (Monte-Carlo, класична задача Poker Squares).
- Щоденна роздача з однаковим seed для всіх + ліміт спроб — 📎.

## Мапа на каталог
- Є: `cell-click` / `drag-drop-piece` ↔ розстановка карт · `pocket` ↔ рука · `event-points` ↔ таблиця рук · `daily-puzzle` · `leaderboard` · `streak-stats` · `profile-stats` · `save-progress` · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+poker-hand-eval` «Оцінка покерної комбінації» · game-logic/score · 🌱 · слоти {hand_size, table}.
  - `+deal-place-discard` «Роздача N, розставити N−1, скинути 1» · game-logic/turns · 🌱.
  - `+line-hand-scoring` «Ряди/стовпці/кути як окремі руки» · game-logic/score · 🌱.
  - `+discard-bonus-hand` «Скид як бонус-рука за умови» · game-logic/score · 🌱.
  - `+daily-attempt-limit` «N спроб щоденного пазла» · levels/bank · 🌱.
  - `+community-goal` «Спільний лічильник спільноти з порогами» · interface/results · 📎.

## Пропозиції до словників
- `+trigger:deal` — роздача карт у руку (є в index/proposals як `deal(n)`).
- `+effect:discard` — карта/плитка йде в скид (index/proposals 🔥).
- `+cond:hand_rank` — набір карт утворює комбінацію рангу ≥ X.
- `+ui:hand-label` — підпис комбінації біля ряду/стовпця.
- `+feature:daily-attempts` — ліміт спроб щоденного пазла; `+feature:community-goal` — спільна ціль усіх гравців.

## Джерела
- ⭐ [Punished Backlog: огляд](https://punishedbacklog.com/love-balatro-try-puzzmos-new-browser-game-pile-up-poker/) — сітка, рука, скид, лінії, кути, 10-та рука, спроби.
- [Houston Chronicle / Hearst: анонс](https://preview-prod.w.houstonchronicle.com/about/newsroom-news/article/introducing-pileup-poker-19488552.php) — фіксація, «будь-який напрям», спільний банк.
- [Adrian Hon про Puzzmo](https://adrianhon.substack.com/p/puzzmo) — фічі платформи.
- [PySol: Poker Square](https://pysolfc.sourceforge.io/doc/rules/pokersquare.html) — предок і варіанти.
- Puzzmo.com — боту недоступний.

## Непевне
- (?) Таблиця очок за комбінації і чи є множники — у джерелах нема.
- (?) Чи рахуються діагоналі: Chronicle — «any direction», Punished Backlog про діагоналі не пише.
- (?) Ліміт спроб: Punished Backlog — 4 на день (5 з підпискою), Chronicle — 5 на день (безліміт з Puzzmo Plus).
- (?) Чи можна переставляти карти до нової роздачі; склад колоди (52 карти? джокери?).
- (?) Чи однакова щоденна роздача для всіх гравців.
- Рік: черга подає 2023 (старт Puzzmo), а гра вийшла 2024 (анонс 2024-06-03).
