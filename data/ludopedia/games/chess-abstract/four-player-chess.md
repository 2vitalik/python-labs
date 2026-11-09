---
title: Four-player chess (шахи на чотирьох)
slug: four-player-chess
aka: [4-player chess, Four-handed chess, 4PC, FFA chess, Шахи вчотирьох]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: online
  info: full
  random: none
  goal: score
year: 1784
platforms: [web, mobile, board]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Four-player_chess", best: true, note: "дошка 8×8 + по 3 ряди з кожного боку; FFA vs Teams; правила Chess.com і клубу Верні; історія"}
  - {kind: other, url: "https://www.chess.com/terms/4-player-chess", note: "Chess.com: очки FFA (мат +20, взяття 1/3/5/5/9, подвійний шах), сірі фігури, король-блукач після здачі, Teams"}
  - {kind: play, url: "https://www.chess.com/4-player-chess", note: "грати онлайн (потрібен вхід)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=4+player+chess+chess.com+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, piece-capture, no-move-into-check, check-stalemate, checkmate, pawn-promotion, castling, repetition-draw, turn-enforcement, move-timer, online-multiplayer, hot-seat, event-points, score-records, rating-system, legal-move-highlight, last-move-highlight, drag-drop-piece, cell-click, move-notation, lobby-window, game-screen, end-screen, rule-variants, +multi-side-turn-order, +player-elimination, +dead-pieces, +team-partners, +multi-king-check-bonus, +lead-claim-win, +cross-board]
proposes: ["+effect:eliminate(side)", "+effect:auto_move(a)", "+cond:teammate(a, b)", "+cond:lead(op, n)", "+ui:team-arrows", "+ui:side-scoreboard", "+feature:claim-win", "+feature:team-chat", "+axis:sides", "+card:player-elimination", "+card:dead-pieces", "+card:multi-king-check-bonus"]
author: opus
date: 2026-11-09
---

# Шахи вчотирьох — чотири армії на хрестоподібній дошці: кожен сам за себе за очки або пара на пару до першого мату

## Суть
Звичайні шахові фігури, але сторін чотири, вони сидять по колу й ходять за годинниковою стрілкою (Червоні → Сині → Жовті → Зелені). Дві основні форми: **FFA** — кожен сам, перемагає більше очок (за взяття, мати, подвійні шахи); **Teams** — партнери навпроти, мета — заматувати одного суперника. Ядро нового для корпусу: вибування сторони посеред партії (її фігури «мертвіють» і стають стінами), черга з N сторін і бонуси за шах кільком королям одразу.

## Поле і час
- Дошка 8×8, до кожного боку якої прибудовано 3 ряди по 8 клітин → хрест 14×14 без кутів 3×3; 160 клітин (Chess.com). Історично — також 8×2 і 8×4 розширення.
- Кожна армія стоїть у звичайній шаховій розстановці на своєму «рукаві» хреста; ряди однієї сторони — це вертикалі сусідньої, тож «8-ма горизонталь» для кожного своя.
- Хід = один хід однієї сторони; черга — за годинниковою, стартують Червоні. Вибулі сторони пропускаються.
- Інформація повна; випадковості нема (крім короля-блукача після здачі в FFA).
- Онлайн — годинник на кожного гравця.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король | piece | сторона, вартість — (мат +20) | крок на 1 у 8 напрямків; не можна лишати під шахом |
| Ферзь | piece | 9 очок | тура + слон |
| Тура | piece | 5 очок | по прямій до перешкоди |
| Слон | piece | 5 очок (не 3!) | по діагоналі; у хресті діагоналі довші й цінніші |
| Кінь | piece | 3 очки | стрибок «Г» |
| Пішак | piece | 1 очко | вперед від свого краю; бʼє по діагоналі; перетворення |
| Перетворений ферзь | piece | 1 очко при взятті | ходить як ферзь, але «вартий» пішака |
| Мертва фігура | static | сіра | після мату/пату сторони: не ходить, займає клітину, взяття не дає очок |
| Король-блукач | piece | — | після здачі/тайм-ауту в FFA: король лишається й ходить випадково; його мат ще дає +20 |
| Партнер | ally | сторона навпроти (Teams) | його фігури не можна брати; може закрити мат партнера |
| Кутова «дірка» | static | 3×3 у кожному куті | поза полем: блокує рух і лінії |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, piece, to)` → ЯКЩО `turn_of(side)` і `legal(move)` → ТО `move(piece, to)`, `end_turn`; хід переходить наступній активній стороні за годинниковою.
- КОЛИ `input(move, piece, to)` → ЯКЩО `occupied(to, enemy)` і `custom: «фігура жива»` → ТО `disappear_b`, `score(вартість)` (FFA: пішак/перетворений 1, кінь 3, слон 5, тура 5, ферзь 9).
- КОЛИ `input(move, piece, to)` → ЯКЩО `custom: «to зайнята мертвою фігурою»` → ТО `disappear_b`, `score(0)`.
- КОЛИ `input(move, piece, to)` → ЯКЩО `custom: «to — фігура партнера»` (Teams) → ТО `block`.
- Хід, після якого свій король (у Teams — і король партнера, за клубними правилами) під шахом, — нелегальний: ЯКЩО `in_check(own_king)` → ТО `block`.
- КОЛИ `check` → ЯКЩО `custom: «ферзь шахує двох королів одночасно»` → ТО `score(1)`; трьох — `score(5)`.
- КОЛИ `check` → ЯКЩО `custom: «не ферзь шахує двох королів»` → ТО `score(5)`; трьох — `score(20)`.
- КОЛИ `no_moves(side)` → ЯКЩО `in_check(king)` → ТО `score(20)` матуючому, `custom: «сторона вибуває»` (`+effect:eliminate`), `set_state(pieces, dead)`.
- FFA Chess.com: мат спрацьовує одразу, не чекаючи ходу заматованого. Teams: мат/пат фіксується лише на ходу заматованого — партнер встигає закрити або заматувати когось першим.
- КОЛИ `no_moves(side)` → ЯКЩО `not in_check(king)` (пат) → ТО FFA: `score(20)` тому, хто запатувався сам, або `score(10)` кожній активній стороні за пат суперника; `custom: «вибуває»`. Teams: `draw`.
- КОЛИ `input(resign)` або `timer(op, 0)` → ЯКЩО `mode(ffa)` → ТО `custom: «сторона вибуває, фігури мертвіють, король лишається й ходить випадково»` (`+effect:auto_move`).
- КОЛИ `input(resign)` або `timer(op, 0)` → ЯКЩО `mode(teams)` → ТО `win` команді суперників.
- КОЛИ `reach(pawn, rank_8)` → ЯКЩО `mode(ffa)` → ТО `transform(pawn, queen)` автоматично (центр дошки). Teams: на 11-й горизонталі, з недоперетворенням (`choose`).
- Клубні правила (Four-handed Chess Club): пішак перетворюється на останньому ряду суперника за вибором; на ряд партнера — розвертається (`custom: «змінити напрям пішака»`); заблокований пішаком партнера — перестрибує по діагоналі.
- Клубні правила: заматований пропускає хід, його фігури стоять як «заморожені» (не беруться, не шахують); партнер знімає мат — взяттям/перекриттям — і сторона повертається.
- КОЛИ `repetition` або `custom: «недостатньо матеріалу / 50 ходів»` → ТО `draw` + `score(10)` кожній активній стороні (FFA).
- КОЛИ `custom: «вибули три сторони»` → ТО `game_over`; перемога — за `counter(points)`.
- КОЛИ `custom: «лишилось двоє»` → ЯКЩО `custom: «лідер попереду на ≥21 очко»` (`+cond:lead`) → ТО `custom: «лідер може заявити перемогу»` (claim win — здача, яка дає іншому +20).
- Перемога: FFA — більше очок наприкінці; Teams — мат одному з суперників; клуб — мат обом. · Поразка: мат, пат, здача, тайм-аут. · Рахунок: очки FFA → рейтинг.
- FFA забороняє домовлятися в чаті (окремий варіант Diplomacy дозволяє); допомагати атаці іншого — легально.

## Керування і ввід
- Онлайн: drag або клік фігури → клік клітини; підсвітка легальних ходів; премув (?).
- Teams: стрілки на дошці й приватний чат команди — підказати партнерові хід.
- Настільно: чотири гравці по сторонах дошки; дві різнокольорові шахові пари.

## Вікна, меню, HUD
- `lobby-window`: вибір режиму (FFA / Teams / Solo / варіанти) і контролю часу; підбір 4 гравців.
- `game-screen`: хрест-дошка, чотири панелі гравців по кутах — імʼя, `player-clock`, поточні очки (`+ui:side-scoreboard`); `turn-indicator`; `last-move-highlight`; сірі фігури вибулих.
- Teams: `team-arrows` (стрілки партнера), `chat-box` команди.
- `confirm-dialog`: «здатись?» / «заявити перемогу?».
- `end-screen`: місця 1–4, очки, зміна рейтингу.
- `replay-window` / `move-list` (цифрова версія; нотація на 4 сторони (?)).
- Переходи: lobby-window → game-screen → (3 вибули / claim win / мат у Teams) → end-screen.

## Фічі поза полем
- `online-multiplayer`, `rating` окремо для FFA і Teams (?), `turn-timer` (контроль часу).
- `mode-select`: FFA, Teams, Solo, Diplomacy; чемпіонатні формати 2023 «Original Solo» і «Standard FFA».
- `feature:claim-win` — дострокова перемога при відриві у 2-гравцевому ендшпілі.
- `custom-rules`: варіанти розстановки (місце короля/ферзя), «взяти короля» замість мату, напрями пішаків.

## Варіації й родичі
- **Чатураджі** — давня індійська гра на 4 з кубиком, що вказує тип фігури для ходу; Four Seasons Chess з «Libro de los Juegos» (XIII ст.), ймовірно, неспоріднена.
- **Клубні правила Ллойд-Верні** (1881–1884, London Four-Handed Chess Club) проти **Chess.com** (FFA з 2016, Teams згодом).
- Родичі в корпусі: `chess.md` (база), `bughouse.md` (командні шахи 2×2 на двох дошках), `lichess-variants.md`, `glinski-hex-chess.md` (інша геометрія), `chess-rule-twists.md`.
- Осі варіацій: **сторін** (2 / 3 / 4) · **союзи** (кожен сам / пари / дипломатія) · **мета** (перший мат / останній живий / очки) · **доля вибулого** (мертві стіни / заморожені до звільнення / король-блукач) · **форма дошки** (8×2 / 8×3 / 8×4 рукави).

## Цікавинки для курсу
- Хрестоподібна дошка як маска «дірок» на 14×14 + повороти координат для чотирьох сторін (напрям пішака, «свій» ряд перетворення) — 🥉.
- Черга N сторін зі скіпом вибулих і перевірка мату «одразу» vs «на своєму ходу» — 🥉.
- Мертві фігури: сторона зникає з черги, але її фігури лишаються перешкодами без очок — 📎.
- Таблиця очок FFA + бонус за шах кільком королям (рахувати, скільки королів атакує фігура після ходу) — 🥈.
- Король-блукач після здачі: `ai-random` для однієї фігури всередині людської партії — 📎.
- Teams: заборона ходу, що відкриває шах партнерові, — легальність з урахуванням чужого короля — 🥈.
- Умова «лідер на ≥21 при двох живих» → claim win — 🌱.

## Мапа на каталог
- Є в каталозі: `piece-move-patterns`, `piece-capture` ↔ фігури й взяття · `no-move-into-check`, `check-stalemate`, `checkmate` · `pawn-promotion` (FFA — автоферзь у центрі) · `castling` (?) · `repetition-draw` · `turn-enforcement` ↔ черга 4 сторін · `move-timer` · `online-multiplayer`, `hot-seat` (настільно) · `event-points`, `score-records`, `rating-system` · `legal-move-highlight`, `last-move-highlight`, `drag-drop-piece`, `cell-click`, `move-notation` · `lobby-window`, `game-screen`, `end-screen` · `rule-variants` ↔ FFA/Teams/клуб.
- **Нема** → пропозиції карток:
  - `+multi-side-turn-order` «Черга N сторін по колу» · game-logic/turns · 📎 · слоти {sides, skip_eliminated}.
  - `+player-elimination` «Вибування сторони посеред партії» · game-logic/lose · 🥉 · слоти {when: immediate|on-own-turn}.
  - `+dead-pieces` «Мертві фігури вибулого — перешкоди без очок» · entities/death · 📎.
  - `+team-partners` «Союзник: не бити, не відкривати його короля» · game-logic/legality · 🥈.
  - `+multi-king-check-bonus` «Бонус за шах кільком королям» · game-logic/score · 🥉.
  - `+lead-claim-win` «Дострокова перемога за відривом» · game-logic/win · 🌱.
  - `+cross-board` «Хрестоподібна дошка з вирізаними кутами» · field/topology · 📎.

## Пропозиції до словників
- `+effect:eliminate(side)` — сторона вибуває з черги ходів (мат/пат/здача у грі на N).
- `+effect:auto_move(a)` — сутність ходить сама (випадково), хоча належить людині (король після здачі).
- `+cond:teammate(a, b)` — A і B в одній команді.
- `+cond:lead(op, n)` — відрив від наступного за очками порівняно з N.
- `+ui:team-arrows` — стрілки-підказки партнерові на дошці; `+ui:side-scoreboard` — очки кожної з N сторін.
- `+feature:claim-win` — кнопка «заявити перемогу» при виконанні умови; `+feature:team-chat` — приватний чат команди.
- `+axis:sides` — кількість сторін у партії: 2 · 3 · 4 · N.
- `+card:player-elimination`, `+card:dead-pieces`, `+card:multi-king-check-bonus` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Four-player chess](https://en.wikipedia.org/wiki/Four-player_chess) — розміри дошки, FFA/Teams, мат одразу vs на своєму ходу, клубні правила (заморожені фігури, розворот пішака, стрибок через пішака партнера), Чатураджі, історія 1784/1881/2016.
- [Chess.com: 4-Player Chess](https://www.chess.com/terms/4-player-chess) — 160 клітин, очки FFA (мат +20, пат 20/10, подвійний/потрійний шах 1/5 і 5/20, взяття 1/3/5/5/9), сірі фігури, король-блукач, кінець при 3 вибулих або відриві ≥21, Teams (11-та горизонталь, стрілки, чат).
- [Chess.com: грати](https://www.chess.com/4-player-chess) — сторінка гри (вміст видно лише після входу).

## Непевне
- (?) Рокіровка й взяття на проході в FFA Chess.com — у відкритих джерелах не описані; рокіровка, ймовірно, є.
- (?) Розбіжність щодо кінця FFA: Wikipedia — відрив «більше 20», Chess.com — «21 або більше».
- (?) Чи рейтинги FFA і Teams окремі; формат нотації ходів на чотири сторони; премув.
- (?) Правила «Original Solo» і «Standard FFA» (2023) — у джерелах лише назви.
- (?) За клубними правилами — чи заборона «шах партнерові власним ходом» стосується лише розкриття, чи будь-якого ходу.
