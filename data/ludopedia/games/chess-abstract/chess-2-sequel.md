---
title: "Chess 2: The Sequel (Sirlin's Chess)"
slug: chess-2-sequel
aka: [Chess 2, Sirlin's Chess, Шахи 2]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: online
  info: partial
  random: none
  goal: state
year: 2014
platforms: [PC, Ouya, board]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Chess_2:_The_Sequel", best: true, note: "6 армій, midline invasion, дуелі, king turn; Sirlin і Burns, Ouya 2013 / Steam 2014"}
  - {kind: other, url: "https://static1.squarespace.com/static/50f14d35e4b0d70ab5fc4f24/t/57c7d553b8a79bf277add71c/1472714070464/chess2_rulebook2-4.pdf", note: "рулбук v2.4 (PDF): повні правила дуелей, армій, перетворення, нічиїх"}
  - {kind: steam, url: "https://store.steampowered.com/app/314340", note: "онлайн, ranked, кореспонденція 11 днів на хід, 21 матчап, 36 дебютних книг; знято з продажу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=chess+2+the+sequel+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, no-move-into-check, check-stalemate, checkmate, pawn-promotion, drag-drop-piece, cell-click, move-timer, online-multiplayer, async-multiplayer, rating-system, ai-opponent, character-select, match-setup, game-screen, end-screen, achievements-window, help-window, +army-select, +sealed-bid-duel, +reach-row-win, +castling, +en-passant, repetition-draw, +move-count-draw, +insufficient-material, +extra-king-turn, +friendly-fire-capture, +aura-move-sharing, +area-attack, +uncapturable-piece, +teleport-move, +double-blind-choice]
proposes: ["+trigger:capture_attempt", "+trigger:bid_reveal", "+cond:rank_higher", "+effect:bid", "+effect:whirlwind", "+effect:rampage", "+effect:return_after_capture", "+ui:stone-counter", "+ui:bid-hand", "+ui:duel-prompt", "+window:army-select", "+window:duel-window", "+feature:loser-switches-army", "+axis:info", "+card:sealed-bid-duel", "+card:army-select"]
author: opus
date: 2026-11-09
---

# Chess 2: The Sequel — шість асиметричних армій, перемога переходом короля через середину й дуелі на сліпих ставках

## Суть
Шахи, перероблені Девідом Сірліном як змагальна гра «для читання суперника»: кожен гравець потай обирає одну з шести армій (Classic, Nemesis, Empowered, Reaper, Two Kings, Animals), тож замість одного матчапу — 21. Друга нова вісь — **дуелі**: коли бʼють твою фігуру, можна викликати на дуель, і обидва потай ставлять 0–2 камені; якщо захисник поставив більше, гине й нападник. Третя — **Midline Invasion**: король, що безпечно дійшов до 5-ї горизонталі, виграє; пату немає. Це зламує дебютні книги й ендшпільні таблиці.

## Поле і час
- Дошка 8×8, стандартна розстановка (кожна армія замінює частину фігур на свої); черга як у шахах.
- Ресурс поза дошкою — **камені** (stones): старт 3, максимум 6.
- Приховане: вибір армії (одночасно, наосліп) і ставки в дуелі (у закритих кулаках, одночасне розкриття) — `info: partial`.
- Онлайн-контроль часу (Steam): live — 25 хв Fischer + 15 с; кореспонденція — 11 днів на хід.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Класична армія | piece | — | звичайні шахи; єдина армія з рокіровкою |
| Nemesis (ферзь Nemesis) | piece | ранг queen | ходить як ферзь; бере й може бути взятий **лише ворожим королем**; дає шах і мат |
| Пішак Nemesis | piece | ранг pawn | звичайний хід (без подвійного кроку) або «nemesis move» — на 1 у бік ворожого короля (у межах прямокутника пішак–король, можна й назад); бʼє лише навскоси вперед |
| Empowered кінь/слон/тура | piece | — | поки ортогонально поруч зі своїм конем/слоном/турою — отримує рух сусіда на додачу до свого |
| Elegant queen (Empowered) | piece | ранг queen | ходить лише як король |
| Reaper (ферзь Reaper) | piece | ранг queen | телепорт на будь-яку порожню клітину або бере будь-яку ворожу фігуру, крім задньої горизонталі суперника; короля не бере |
| Ghost (тури Reaper) | piece | — | телепорт на будь-яку порожню клітину; не бере й не береться; крізь нього не проходять; Whirlwind його не знищує |
| Warrior king ×2 (Two Kings) | piece | royal | ходить і бʼє як король; або Whirlwind: стоїть і знищує всіх сусідів (8), своїх і ворожих; не можна, якщо поруч другий warrior king |
| Wild horse (Animals, кінь) | piece | ранг knight | ходить як кінь; може брати свої фігури |
| Tiger (Animals, слон) | piece | ранг bishop | до 2 клітин навскоси; після взяття повертається на клітину, звідки атакував |
| Elephant (Animals, тура) | piece | ранг rook | до 3 клітин ортогонально; бере своїх і чужих; після взяття «rampage» — мусить пройти максимум, знищуючи все на шляху; не береться фігурами далі 2 клітин (поза 5×5) |
| Jungle queen (Animals) | piece | ранг queen | ходить як тура або кінь |
| Камінь | resource | 3 → max 6 | ставка в дуелі; +1 за взяття ворожого пішака |

## Правила (КОЛИ → ЯКЩО → ТО)
Дуелі:
- КОЛИ `contact(attacker, defender)` → ЯКЩО `custom: «defender — не король і attacker — не король»` and `custom: «захисник вирішив дуель»` → ТО `window(duel-window)`.
- КОЛИ `input(duel)` → ЯКЩО `custom: «ранг нападника вищий за ранг захисника (pawn < knight/bishop < rook < queen)»` → ТО `take(defender_side, stone)` (плата 1 камінь за виклик).
- КОЛИ `input(duel)` → ЯКЩО `not has(defender_side, stone)` → ТО `block` (з 0 каменів дуель не викликати).
- КОЛИ `input(bid(n))` → ЯКЩО `custom: «0 ≤ n ≤ 2 і n ≤ камені гравця»` → ТО `custom: «закрита ставка»`; КОЛИ `custom: «обидві ставки зроблені»` → ТО `reveal(bids)`, `custom: «усі показані камені знищуються»`.
- КОЛИ `custom: «розкрито»` → ЯКЩО `custom: «ставка захисника > ставки нападника»` → ТО `disappear_both` (захисник усе одно втрачає фігуру, нападник — теж); інакше (нічия — на користь нападника) → `disappear_b`.
- КОЛИ `custom: «обидва поставили 0 (блеф розкрито)»` → ТО `choose(+1 камінь нападнику | −1 камінь захиснику)`.
- КОЛИ `custom: «дуель проти гравця з 0 каменів»` → ТО `custom: «ставка 1 обовʼязкова, автоматична перемога»`.
- КОЛИ `contact(p, enemy_pawn)` → ЯКЩО `count(stones, <, 6)` → ТО `give(capturer_side, stone)` (і коли пішак гине в дуелі); перетворення пішака каменя супернику не дає.

Перемога й нічия:
- КОЛИ `reach(king, rank_5)` → ЯКЩО `not in_check(side)` → ТО `win` (Midline Invasion); Two Kings — лише коли **обидва** warrior kings за серединою.
- КОЛИ `no_moves(side)` → ТО `lose` (пату немає).
- КОЛИ `check(side)` → ЯКЩО `no_moves(side)` → ТО `lose` (мат); Two Kings — мат будь-якому з двох = поразка.
- КОЛИ `repetition(3)` → ТО `draw` · 50 ходів без взяття й руху пішака → `draw` · недостатньо матеріалу для мату і Midline Invasion неможливий → `draw`.

Армії:
- Nemesis: КОЛИ `contact(p, nemesis)` → ЯКЩО `custom: «p — не король»` → ТО `block`; nemesis бере лише короля (?), але шахує як ферзь.
- Empowered: КОЛИ `turn_start(side)` → ЯКЩО `custom: «кінь/слон/тура ортогонально поруч зі своїм конем/слоном/турою»` → ТО `custom: «додати фігурі патерн ходу сусіда (не транзитивно)»`.
- Reaper: КОЛИ `input(move(reaper, to))` → ЯКЩО `free(to)` or (`occupied(to, enemy)` and `custom: «не задня горизонталь суперника і не король»`) → ТО `teleport(reaper, to)`; ghost — `teleport` лише на порожні; `contact(any, ghost)` → `block`.
- Two Kings: КОЛИ `input(whirlwind(wk))` → ЯКЩО `custom: «поруч нема другого warrior king і після цього жоден король не під шахом»` → ТО `explode(adjacent8)` (свої й чужі; ghost не знищується).
- Two Kings: КОЛИ `turn_end(side)` → ТО `extra_move` — необовʼязковий king turn: лише хід warrior king або Whirlwind; в обидва ходи не можна ставати під шах.
- Animals: wild horse і elephant можуть `contact(p, own_piece)` → `disappear_b`; tiger: КОЛИ `contact(tiger, enemy)` → ТО `disappear_b`, `custom: «тигр лишається на клітині, звідки атакував»`.
- Animals: КОЛИ `contact(elephant, any)` → ТО `custom: «rampage: пройти максимум (3) у цьому напрямку, знищуючи все на шляху»`; КОЛИ `contact(p, elephant)` → ЯКЩО `not in_range(p, elephant, 2)` → ТО `block` (діє навіть на Reaper).

Інше:
- КОЛИ `reach(pawn, last_rank)` → ТО `choose(фігура своєї армії, не пішак і не король)`, `transform`; перетворення обовʼязкове.
- Рокіровка — лише Classic; en passant — для всіх пішаків усіх армій.
- Вибір армій: `input(army)` обома наосліп одночасно; дзеркальні матчі дозволені; у серії партій програвший може змінити армію, переможець — ні.
- Перемога: мат · Midline Invasion · суперник без легальних ходів · Нічия: 3× повторення, 50 ходів, недостатній матеріал.

## Керування і ввід
- Звичайний шаховий хід (drag/клік). Спецдії: Whirlwind (кнопка на warrior king), «пропустити king turn» (у настільній версії — торкнутися warrior king як сигнал).
- Дуель: після спроби взяття захисник отримує запит «Дуель?»; далі обидва обирають 0/1/2 камені потай (у настілці — у кулаку), одночасне розкриття.
- Вибір армії — перед партією, одночасно.

## Вікна, меню, HUD
- `army-select` (`character-select`): шість армій з описом; одночасний сліпий вибір.
- `game-screen`: дошка (2D або 3D набори фігур кожної армії), `stone-counter` обох гравців, `player-clock`, `turn-indicator`, `legal-move-highlight` (у т.ч. посилені ходи Empowered), позначка king turn.
- `duel-window` / `duel-prompt`: «викликати дуель?» (з ціною, якщо нападник вищого рангу) → `bid-hand` (0/1/2) → розкриття.
- `match-setup`: live / кореспонденція, ranked / casual; `lobby-window`.
- `end-screen`: мат / Midline Invasion / нема ходів / нічия; `achievements-window`, `help-window` з правилами армій.
- Переходи: main-menu → match-setup → army-select → game-screen ⇄ duel-window → end-screen.

## Фічі поза полем
- `online-multiplayer` з ranked-підбором, live (25+15) і `async-multiplayer` (11 днів на хід); кросплей з Ouya.
- Single-player (Steam: «Single-player»); `ai-opponent-levels` — (?).
- 36 дебютних книг, 21 матчап армій; `achievements`, `cloud-save`, 2D/3D набори фігур (`theme-select`).
- `loser-switches-army` — у серії партій армію міняє лише програвший.
- Настільна версія: безкоштовний print-and-play рулбук, грається звичайним набором.
- Steam: гру знято з продажу.

## Варіації й родичі
- Асиметричні армії — родич [lichess-variants.md](lichess-variants.md) і «Chess with Different Armies» (Ralph Betza) (?); дуелі — сліпі ставки, як у покерних блефах.
- Midline Invasion — родич King of the Hill (lichess) і «дійти до ряду» у [breakthrough-loa.md](breakthrough-loa.md).
- Whirlwind — родич вибуху Atomic; rampage слона — каскадне взяття; ghost/nemesis — невразливі фігури (як качка в [chess-rule-twists.md](chess-rule-twists.md), але своя).
- **Осі варіацій**: склад армій (симетричний · асиметричний за вибором) · взяття (безумовне · з дуеллю-ставкою) · ціль (мат · мат або перехід середини) · пат (нічия · поразка) · кількість royal (1 · 2) · хід (один · + king turn) · friendly fire (ні · так для окремих фігур).

## Цікавинки для курсу
- Сліпа одночасна ставка з ресурсом, блефом і нічиєю на користь нападника — 🥉.
- Шість армій як набір конфігурацій фігур поверх одного рушія; вибір і підстановка — 🥉.
- Empowered: патерн ходу як обʼєднання патернів сусідів (перераховується щоходу) — 🥈.
- Elephant: обмежена дистанція + rampage + невразливість на відстані > 2 — 🥈.
- Two Kings: два royal, Whirlwind, додатковий king turn і перевірка шаху для обох — 🥈.
- Midline Invasion + «нема ходів = поразка» — 📎 поверх шахового рушія.
- AI, що враховує дуелі (очікувана цінність ставок) — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` · `legal-move-highlight` · `no-move-into-check` · `check-stalemate` ↔ шах (пату нема) · `checkmate` · `repetition-draw` ↔ 3× повторення · `pawn-promotion` ↔ у фігуру своєї армії · `drag-drop-piece` · `cell-click` · `move-timer` ↔ Fischer 25+15 · `online-multiplayer` · `async-multiplayer` ↔ 11 днів на хід · `rating-system` ↔ ranked · `ai-opponent` (?) · `character-select` ↔ вибір армії · `match-setup` · `game-screen` · `end-screen` · `achievements-window` · `help-window`.
- **Нема** → пропозиції карток:
  - `+army-select` «Вибір асиметричної армії перед партією» · entities/legality · 🥉 · слоти {armies, double_blind}.
  - `+sealed-bid-duel` «Дуель закритими ставками при взятті» · entities/combat · 🥉 · слоти {start: 3, max: 6, bid_max: 2, tie: attacker}.
  - `+reach-row-win` — підтверджую (корпус ×5): король на 5-й горизонталі.
  - `+castling` / `+en-passant` / `+move-count-draw` / `+insufficient-material` — підтверджую (chess.md).
  - `+extra-king-turn` «Необовʼязковий додатковий хід певною фігурою» · game-logic/opponent · 📎.
  - `+friendly-fire-capture` «Фігура може брати свої» · entities/combat · 🌱.
  - `+aura-move-sharing` «Сусіди ділять патерни ходу» · entities/legality · 🥈.
  - `+area-attack` «Удар по всіх сусідах без руху» · entities/combat · 📎.
  - `+uncapturable-piece` «Фігура, яку беруть лише певні (або ніхто)» · entities/combat · 🌱.
  - `+teleport-move` «Хід на будь-яку порожню клітину» · entities/move · 🌱.
  - `+double-blind-choice` «Одночасний прихований вибір обох гравців» · game-logic/opponent · 📎.

## Пропозиції до словників
- `+trigger:capture_attempt(a, b)` — спроба взяття, до її застосування (вікно реакції: дуель).
- `+trigger:bid_reveal` — обидві закриті ставки розкрито.
- `+cond:rank_higher(a, b)` — ранг A вищий за B (pawn < minor < rook < queen); родич `+cond:value_ge` з chess-rule-twists.
- `+effect:bid(n)` — закрита ставка ресурсу.
- `+effect:whirlwind` — знищити всіх сусідів без руху (або `explode(adjacent8)` ⏳ — тоді не потрібне).
- `+effect:rampage(a, dir, n)` — примусовий рух на максимум з взяттям усього на шляху.
- `+effect:return_after_capture` — фігура повертається на вихідну клітину після взяття (тигр).
- `+ui:stone-counter` · `+ui:bid-hand` (вибір 0/1/2 потай) · `+ui:duel-prompt`.
- `+window:army-select` · `+window:duel-window`.
- `+feature:loser-switches-army` — правило серії партій.
- `+axis:info` — значення `simultaneous-secret` (інформація прихована лише в момент одночасного вибору).
- `+card:sealed-bid-duel` · `+card:army-select`.

## Джерела
- ⭐ [Wikipedia: Chess 2: The Sequel](https://en.wikipedia.org/wiki/Chess_2:_The_Sequel) — армії, Midline Invasion, дуелі, king turn, автори, Ouya 12.2013 / Steam 19.08.2014.
- [Рулбук Chess 2 v2.4 (PDF)](https://static1.squarespace.com/static/50f14d35e4b0d70ab5fc4f24/t/57c7d553b8a79bf277add71c/1472714070464/chess2_rulebook2-4.pdf) — повні правила: камені 3→6, плата за виклик вищого рангу, блеф і «нічия → нападник», дипломатичний імунітет королів, армії, перетворення, нічиї, en passant для всіх.
- [Steam: Chess 2](https://store.steampowered.com/app/314340) — онлайн/ranked/кореспонденція, 21 матчап, 36 дебютних книг, ачівки, 2D/3D, знято з продажу.
- YouTube — пошук «chess 2 the sequel gameplay».

## Непевне
- (?) Nemesis «бере лише короля»: Wikipedia каже «не може брати й бути взятим, окрім як ворожим королем» — чи Nemesis бере короля чи лише шахує, неоднозначно.
- (?) Чи є в цифровій версії AI-суперник — Steam лише вказує «Single-player».
- (?) Хто вирішує, чи викликати дуель, — захисник; у цифровій версії, ймовірно, після кожної спроби взяття зʼявляється запит (як саме — не бачив).
- (?) «Chess with Different Armies» як предок — з памʼяті, у відкритих джерелах не бачив.
- (?) Рік: Ouya — грудень 2013, Steam — 2014; у шапці — 2014 за Steam.
- Сторінка chessvariants.org (з черги) віддала 403 — не прочитана.
