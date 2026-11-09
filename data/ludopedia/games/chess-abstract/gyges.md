---
title: Gyges
slug: gyges
aka: [Gygès, Гігес]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: race
year: 1985
platforms: [board, web]
links:
  - {kind: other, url: "https://www.boardspace.net/english/about_gyges.html", best: true, note: "Boardspace: хід лише з найближчого ряду, 1–3 кроки за висотою, рикошет, displace у просунутій грі, перемога на ціль суперника"}
  - {kind: other, url: "https://jpneto.github.io/world_abstract_games/gyges.htm", note: "правила Claude Leroy (©1984) + переклад 2001: «берег», заборона повторів (Ko / Renop), пас, нотація"}
  - {kind: other, url: "https://bg.doc.boardgamearena.com/Gamehelpgyges", note: "BGA: 6×6, точний рахунок до цілі, без проходу крізь фігури й повторних клітин, Replace"}
  - {kind: official, url: "https://blueorangegames.eu/?p=40661", note: "Blue Orange: дерев'яна дошка 38 полів, 2 трони, 12 металевих кілець 4+4+4"}
  - {kind: bgg, url: "https://boardgamegeek.com/boardgame/10527/gyges", note: "BGG (HTML агентам не відкривається)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Gyges+board+game+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, move-4dir, legal-move-highlight, path-preview, reach-exit, pass-turn, hot-seat, turn-enforcement, ai-opponent, ai-minimax, online-multiplayer, rating-system, cell-click, drag-drop-piece, selection-highlight, last-move-highlight, move-notation, replay, game-screen, main-menu, end-screen, help-window, state-as-data, unit-tests, +shared-neutral-piece, +nearest-row-control, +bounce-chain, +exact-landing-win, +relocate-landed, +path-no-revisit, +ko-rule, +rule-variants]
proposes: ["+cond:in_shore", "+effect:chain_move", "+cond:path_unused", "+ui:bounce-path", "+ui:shore-highlight", "+window:variant-select", "+card:nearest-row-control", "+card:bounce-chain", "+card:exact-landing-win", "+card:relocate-landed"]
author: opus
date: 2026-11-09
---

# Gyges — фігури нічиї: ходиш будь-якою з найближчого до себе ряду й рикошетиш по чужих висотах до трону суперника

## Суть
12 фігур-кілець (по 4 одинарних, подвійних і потрійних) не належать нікому. Ходиш будь-якою фігурою з **«берега»** — найближчого до тебе ряду, де є фігури; вона йде рівно на 1, 2 або 3 кроки (за кількістю кілець) ортогонально, зі зміною напрямку. Якщо останній крок упав на іншу фігуру — рух продовжується на стільки кроків, скільки кілець у тієї («рикошет»), і так ланцюжком. Хто точно приземлився на трон суперника за його рядом, виграв. Автор — Claude Leroy (©1984, видання 1985; пізніше Blue Orange).

## Поле і час
- Поле 6×6 (36 клітин) + 2 трони-цілі; кожен трон зʼєднаний з усіма 6 клітинами крайнього ряду свого гравця (Blue Orange: 38 полів, зʼєднаних відрізками). Реалізація jpneto — 6 стовпців × 8 рядів, де перший і останній ряди — службові.
- Сусідство ортогональне; трон — особливий вузол графа, тому поле фактично `square` + 2 вузли.
- Хід = рух однієї фігури разом з усіма рикошетами; часу нема.
- «Берег» кожного гравця рухається: щойно найближчий ряд спорожнів, береговим стає наступний.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Одинарна фігура | piece | 1 кільце, ×4, нічия | рівно 1 крок; на чужій фігурі дає рикошет на 1 |
| Подвійна фігура | piece | 2 кільця, ×4, нічия | рівно 2 кроки; рикошет на 2 |
| Потрійна фігура | piece | 3 кільця, ×4, нічия | рівно 3 кроки; рикошет на 3 |
| Клітина | terrain | 6×6 | порожня — прохідна; зайнята — лише як кінець кроку (рикошет або заміна) |
| Трон (ціль) | zone | 2, за крайнім рядом кожного | точне приземлення на трон суперника — перемога; крізь трон не проходять |
| Берег | zone | найближчий до гравця непорожній ряд | лише його фігурами можна ходити |

## Правила (КОЛИ → ЯКЩО → ТО)
- Розстановка: КОЛИ `turn_start(side)` → ЯКЩО `custom: «фаза розстановки»` → ТО `place(piece, own_first_row)` — кожен ставить 2+2+2 у свій ряд у будь-якому порядку; першим — південь.
- КОЛИ `input(select, piece)` → ЯКЩО `custom: «фігура в найближчому до мене непорожньому ряду»` (`+cond:in_shore`) → ТО дозволено; інакше `block`.
- КОЛИ `input(move, piece, path)` → ЯКЩО `custom: «рівно n ортогональних кроків, n = кільця фігури»` and `custom: «проміжні клітини порожні»` and `custom: «жоден відрізок шляху не використано двічі»` (`+cond:path_unused`) → ТО `move(piece, path_end)`.
- КОЛИ `input(move, piece, path)` → ЯКЩО `custom: «шлях іде крізь трон або зупиняється не на кінці»` → ТО `block`.
- КОЛИ `after(move)` → ЯКЩО `occupied(path_end, other_piece)` and `not mode(replace)` → ТО `custom: «рух триває на m кроків, m = кільця фігури, на яку стали»` (`+effect:chain_move`) — і знову до порожньої клітини або наступного рикошету.
- КОЛИ `after(move)` → ЯКЩО `occupied(path_end, other_piece)` and `mode(replace)` → ТО `teleport(other_piece, custom: «будь-яка вільна клітина, не за берегом суперника»)`, рухома фігура лишається — Replace / displace (Boardspace — просунута гра).
- КОЛИ `after(move)` → ЯКЩО `free(path_end)` → ТО `end_turn`.
- КОЛИ `reach(piece, opponent_throne)` → ЯКЩО `custom: «трон — точний кінець руху»` → ТО `win`; власний трон недосяжний.
- КОЛИ `custom: «рикошетна фігура не може зробити свої кроки»` → ТО `block` (увесь хід нелегальний).
- КОЛИ `input(move, …)` → ЯКЩО `custom: «позиція після ходу вже була»` → ТО `block` (Ko / закон Renop).
- КОЛИ `no_moves(side)` → ЯКЩО `custom: «жодна фігура берега не ходить»` → ТО `custom: «можна ходити фігурами наступного ряду»` (Boardspace); інакше `pass_turn`, суперник ходить далі, доки не виграє або хід не зʼявиться (jpneto).
- Перемога: точне приземлення на трон суперника · Поразка: те саме для суперника · Рахунок: нема.

## Керування і ввід
- Настільна: узяти фігуру з берега, провести по клітинах, на зайнятій — «відскочити» далі.
- (цифрова версія) Клік по фігурі берега → `path-preview` з усіма кінцями (включно з рикошетами); при приземленні на фігуру — вибір «рикошет / заміна» і клік по вільній клітині для переставленої фігури.
- Нотація jpneto — ланцюжок клітин «16-35», крапка з комою між кількома ходами поспіль.

## Вікна, меню, HUD
- `main-menu` / лобі Boardspace: людина або робот (роботи «досить сильні» — незвичний для людини перебір).
- `variant-select`: базова гра / просунута з displace.
- `game-screen`: поле 6×6 з двома тронами, `shore-highlight` (поточний берег кожного), `legal-move-highlight`, `bounce-path` (ламаний шлях з точками рикошету), `turn-indicator`, `last-move-highlight`, `move-list`.
- `end-screen`: хто дійшов до трону.
- `help-window`: правило берега і рикошету.
- Переходи: main-menu → variant-select → game-screen → end-screen.

## Фічі поза полем
- `online-multiplayer`, `ai-opponent-levels` — Boardspace (рейтинг, архів партій), BGA.
- `history` / `replay` — архів Boardspace.
- `custom-rules` — базова / просунута (displace) гра.

## Варіації й родичі
- Boardspace ставить у групу «перегони з дивними правилами» разом із Gounki та [kamisado](kamisado.md).
- Спільні нічиї фігури — [martian-chess](martian-chess.md) (фігура твоя, поки на твоїй половині), [neutron](neutron.md) (нейтральний нейтрон); вибір фігури за положенням, а не кольором — як у Kamisado за кольором клітини.
- Ланцюжок рухів за один хід до цільової зони — [halma-chinese-checkers](halma-chinese-checkers.md) (серія стрибків); рух рівно на висоту — [dvonn](dvonn.md) (там стос летить прямою).
- Осі варіацій: **хто власник фігури** (сторона / ніхто, вирішує позиція) · **дальність** (= висота, точно) · **на зайняту** (рикошет / заміна / заборона) · **мета** (точно на трон / дійти до ряду).

## Цікавинки для курсу
- «Берег» — динамічний вибір дозволених фігур за найближчим непорожнім рядом — 🌱.
- Шляхи рівно n кроків з поворотами без повтору відрізків (DFS) — 📎.
- Рикошетні ланцюжки: DFS по станах (клітина, лишок кроків, використані відрізки), повний набір кінців ходу — 🥈.
- Replace: додаткова гілка «переставити будь-куди, крім за берегом суперника» — 🌱 (але множить розгалуження).
- Заборона повтору позицій (хеш історії) — 📎.
- AI: оцінка «скільки шляхів до трону у суперника наступного ходу» — турнірна думка «створити дві загрози» — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns`, `move-4dir` ↔ рівно 1–3 ортогональні кроки · `legal-move-highlight`, `path-preview` ↔ кінці ходу й ламаний шлях · `reach-exit` ↔ трон суперника · `pass-turn` · `hot-seat`, `turn-enforcement`, `ai-opponent`, `ai-minimax`, `online-multiplayer`, `rating-system` · `cell-click`, `drag-drop-piece`, `selection-highlight`, `last-move-highlight` · `move-notation`, `replay` · `game-screen`, `main-menu`, `end-screen`, `help-window` · `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+shared-neutral-piece` (є в сімʼї) — усі 12 фігур нічиї.
  - `+nearest-row-control` «Ходити можна лише фігурами найближчого непорожнього ряду» · entities/legality · 🌱.
  - `+bounce-chain` «Рикошет: рух триває силою фігури, на яку стали» · entities/move · 🥈.
  - `+exact-landing-win` «Перемога лише точним приземленням на ціль» · game-logic/win · 🌱.
  - `+relocate-landed` «Фігуру, на яку стали, переставляють будь-куди» · entities/interact · 🌱 · слот {forbidden: beyond_opponent_shore}.
  - `+path-no-revisit` «Шлях без повторних відрізків» · entities/legality · 📎.
  - `+ko-rule` (див. go.md) — заборона повтору позиції.
  - `+rule-variants` — базова / просунута гра (у каталозі є `rule-variants` як конструктор; тут лише 2 режими).

## Пропозиції до словників
- `+cond:in_shore` — фігура в найближчому до сторони непорожньому ряду.
- `+cond:path_unused` — шлях не використовує той самий відрізок/клітину двічі за хід.
- `+effect:chain_move` — рух продовжується на N, взяте з сутності, на яку стали (рикошет).
- `+ui:bounce-path` — ламаний шлях з точками рикошету; `+ui:shore-highlight` — поточний берег кожного гравця.
- `+window:variant-select` (уже пропонувалось у checkers / line-games).
- `+card:nearest-row-control`, `+card:bounce-chain`, `+card:exact-landing-win`, `+card:relocate-landed` — див. «Мапа на каталог».

## Джерела
- ⭐ [Boardspace: про Gyges](https://www.boardspace.net/english/about_gyges.html) — правило найближчого ряду, 1/2/3 кроки ортогонально зі зміною напрямку, рикошет «за висотою фігури на полі», displace у просунутій грі, перемога, родичі Gounki / Kamisado.
- [World of Abstract Games: Gyges](https://jpneto.github.io/world_abstract_games/gyges.htm) — правила Claude Leroy і переклад 2001: «берег», шлях крізь порожні, без стрибків, Ko / Renop, пас і продовження ходів суперником, нотація.
- [BGA: довідка Gyges](https://bg.doc.boardgamearena.com/Gamehelpgyges) — 6×6, розстановка в перший ряд, точний рахунок, заборона проходу крізь трон, Replace.
- [Blue Orange: Gygès](https://blueorangegames.eu/?p=40661) — видання: 38 полів, 2 трони, 12 кілець 4+4+4, автор Claude Leroy.

## Непевне
- (?) Рикошет: Boardspace і переклад Leroy — рухома фігура «позичає» хід фігури, на яку стала; jpneto-підсумок — «ту фігуру мусять рухати»; BGA — «далі на свою кількість кілець». Беру перше.
- (?) BGA: «після рикошету від потрійної треба пройти 2 клітини, перш ніж знову рикошетити» — не зрозумів, не вписав.
- (?) Replace: у Boardspace — лише просунута гра, у BGA і jpneto — звичайна опція.
- (?) Рік: черга дає «?»; jpneto — ©1984, видання на BGG/analog.games — 1985 (бачив лише в результатах пошуку).
- (?) Розстановка — «перший ряд» (BGA, Boardspace) vs «другий ряд» (jpneto, де перший — службовий); на 6×6 це той самий ряд.
- (?) Турнірне правило «виграти лише створивши дві загрози, а не на помилці суперника» — з результатів пошуку, сторінки не бачив.
