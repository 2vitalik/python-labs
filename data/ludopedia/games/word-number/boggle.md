---
title: Boggle
slug: boggle
aka: [Богл, Find-A-Word, Big Boggle, Boggle Master, Super Big Boggle]
family: word-number
also: [board-digital]
klass: puzzle
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: setup
  goal: score
year: 1973
platforms: [board, PC, mobile, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Boggle", best: true, note: "правила, суміжність 8, Qu, таблиця очок, скасування спільних слів, Big/Super Big Boggle, challenge cube"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=boggle+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [word-validation, time-out, event-points, hot-seat, online-multiplayer, completion-detection, spawn-random-cell, leaderboard, score-records, difficulty-levels, field-size-picker, rule-variants, level-solver, game-screen, end-screen, settings-window, help-window, +path-trace-word, +word-length-scoring, +dice-tray-shuffle, +shared-word-cancel, +blocker-die, +bonus-die, +multi-letter-face, +found-words-list, +word-challenge]
proposes: ["+cond:path_adjacent8", "+cond:not_played", "+cond:length", "+effect:shuffle", "+effect:strike_shared", "+ui:found-words-list", "+ui:word-preview", "+window:round-results", "+feature:word-challenge"]
author: opus
date: 2026-11-09
---

# Boggle — 3 хвилини шукаєш слова з сусідніх кубиків сітки 4×4; спільні з суперниками слова згорають

## Суть
16 кубиків з літерами трясуть у закритому лотку, вони лягають сіткою 4×4. За 3 хвилини всі гравці одночасно виписують слова, кожна наступна літера яких сусідить з попередньою (8 напрямків), без повторного вживання кубика. Потім списки порівнюють: слово, знайдене двома і більше гравцями, викреслюється в усіх; решта дає очки за довжиною. Ядро — пошук шляхів у графі сітки + змагання на унікальність, а не на кількість.

## Поле і час
- Сітка 4×4 (Classic); 5×5 — Big Boggle / Boggle Master / Boggle Deluxe; 6×6 — Super Big Boggle (2012).
- Поле статичне протягом раунду: кубики не можна торкатись, доки біжить таймер.
- Час — пісочний годинник 3 хв (Super Big — 4 хв); усі шукають одночасно. Сесія = кілька раундів з перетрушуванням.
- Цифрова версія: поле клікабельне, шлях підсвічується; таймер — `timer-countdown`.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кубик | tile | 6 граней з літерами; видно верхню | випадково лягає в одну з 16 клітин верхньою гранню |
| Кубик Qu | tile | грань «Qu» | одна клітина = 2 літери; в очках рахується як 2 |
| Кубик з двома літерами (5×5, 2011) | tile | грані Qu, Th, In… | клітина дає диграф |
| Кубик «word stop» (6×6) | static | суцільний квадрат | клітину не можна вживати в словах — розрив графа |
| Challenge cube | tile | 6 рідкісних літер, червоний | слово через нього дає бонус |
| Лоток з кришкою | container | 16 / 25 / 36 гнізд | трясіння = перемішування позицій і граней |
| Пісочний годинник | static | 3 хв | кінець = стоп раунду |
| Список слів гравця | zone | слова | порівнюється з чужими в кінці |
| Словник | static | узгоджений заздалегідь | вирішує оскарження |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` (раунд) → ТО `shuffle(dice)`: кожен кубик — у випадкову клітину, випадковою гранню догори.
- КОЛИ `input(word)` → ЯКЩО `length(word) >= 3` and `path_adjacent8(word)` and кожен кубик не більше раз → ТО `custom: «слово в список гравця»`.
- КОЛИ `input(word)` → ЯКЩО `not path_adjacent8(word)` → ТО `block` (цифрова версія: шлях не продовжується).
- Великі літери (власні назви) і слова з дефісом заборонені; множина, похідні і «слово в слові» (mast у master) — дозволені.
- 5×5 і 6×6: КОЛИ `input(word)` → ЯКЩО `length(word) < 4` → ТО `block`.
- 6×6: КОЛИ `input(path)` → ЯКЩО `occupied(cell, word-stop)` → ТО `block`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `custom: «писати заборонено; гравці читають списки»`.
- КОЛИ `after(читання)` → ЯКЩО `not not_played(word)` (є у ≥2 гравців) → ТО `strike_shared(word)` — викреслити в усіх.
- КОЛИ `input(challenge word)` → ЯКЩО `not in_dictionary(word)` → ТО `custom: «слово знято»`.
- Очки 4×4 за довжиною: 3–4 → `score(1)` · 5 → `score(2)` · 6 → `score(3)` · 7 → `score(5)` · 8+ → `score(11)`.
- Очки 6×6: 4 → 1 · 5 → 2 · 6 → 3 · 7 → 5 · 8 → 11 · 9+ → 2 за літеру.
- Qu рахується як 2 літери в довжині.
- КОЛИ слово вживає challenge cube → ТО `score(+бонус)` (?).
- Перемога: найбільше очок (за раунд чи після кількох) · Нічия: зазвичай за кількістю довгих слів · Поразки як стану нема.

## Керування і ввід
- Настільна: дивишся на сітку, пишеш слова на папері; торкатись кубиків не можна.
- Цифрова: drag пальцем по сусідніх клітинах (з діагоналями) або набір з клавіатури; відпуск / Enter = подати слово; повернення назад по шляху — скасувати хвіст (?).
- Одночасний ввід усіх гравців (не по черзі) — тому hot-seat у цифровій версії незручний, частіше онлайн або соло проти таймера.

## Вікна, меню, HUD
- (цифрова версія) `game-screen`: сітка, `timer-countdown`, `word-preview` (поточний шлях-слово), `found-words-list`, `score`.
- (цифрова версія) `round-results`: слова всіх гравців поруч, викреслені спільні, пропущені слова поля з найдовшими.
- (цифрова версія) `settings-window`: розмір поля (4×4 / 5×5 / 6×6), час раунду, мінімальна довжина, словник.
- (цифрова версія) `main-menu`: соло · онлайн · правила (`help-window`); `leaderboard`.
- Переходи: `main-menu` → `game-screen` → таймер 0 → `round-results` → новий раунд / меню.

## Фічі поза полем
- `custom-difficulty` (розмір, час, мінімальна довжина) і `custom-rules` (challenge cube, word stop).
- `word-challenge` — оскарження слова за узгодженим словником.
- `online-multiplayer` — Hasbro Interactive CD-ROM для Windows (до 4 гравців онлайн); `mboggle` у MIT Project Athena.
- (цифрова) `show-solution` — показ усіх слів поля після раунду (?).

## Варіації й родичі
- Boggle Jr. (1988, діти), Big Boggle 5×5 (без 3-літерних), Super Big Boggle 6×6 (4 хв, word stop, нові очки), challenge cube, Boggle Bowl (кидаєш свої кубики, просуваєш фішку).
- Ruzzle — мобільна гра на основі Boggle (раунди проти суперника).
- SpellTower (`spelltower.md`), Bookworm (`bookworm.md`) — той самий шлях по сусідах, але з гравітацією і зникненням.
- NYT Strands (див. `nyt-connections.md`) — шлях по сусідах з точним покриттям сітки; Letterpress (`letterpress.md`) — літери без суміжності, але з захопленням.
- **Осі варіацій:** розмір (4×4 / 5×5 / 6×6) · суміжність (8 / 4 / гекс) · мін. довжина (3 / 4) · спільні слова (згорають / рахуються) · особливі клітини (Qu, диграфи, блокер, бонус) · таймер (3 / 4 хв / без).

## Цікавинки для курсу
- Генерація поля: перемішати 16 кубиків і вибрати грань — 🌱.
- Перевірка шляху: чи можна скласти слово на сітці без повтору клітин (DFS з backtracking) — 📎.
- Солвер «усі слова поля»: DFS по сітці з префіксним деревом (trie) для відсічення — 🥇.
- Скасування спільних слів між гравцями і таблиця очок за довжиною — 🌱.
- Генератор «цікавого» поля (мін. N слів, є довге слово) через солвер — 🥈.
- Super Big: блокер-клітини як дірки в графі + диграфи на гранях — 📎.

## Мапа на каталог
- Є: `word-validation` ↔ словник і оскарження · `time-out` ↔ пісочний годинник · `event-points` ↔ таблиця за довжиною · `hot-seat` ↔ спільний стіл · `online-multiplayer` ↔ Hasbro CD-ROM · `spawn-random-cell` ↔ трясіння лотка · `level-solver` ↔ усі слова поля · `field-size-picker` ↔ 4/5/6 · `rule-variants` ↔ challenge cube, word stop · `difficulty-levels` · `leaderboard` · `score-records` · `completion-detection` · `game-screen` · `end-screen` · `settings-window` · `help-window`.
- **Нема** → пропозиції карток:
  - `+path-trace-word`, `+word-length-scoring` — див. `nyt-connections.md`, `bookworm.md`.
  - `+dice-tray-shuffle` «Поле з кубиків: позиція + грань випадкові» · levels/generation · 🌱 · слоти {dice: list of faces}.
  - `+shared-word-cancel` «Спільне з суперником не рахується» · game-logic/score · 🌱.
  - `+blocker-die` «Клітина-блокер у графі слів» · entities/legality · 🌱.
  - `+bonus-die` «Кубик, що дає бонус слову» · game-logic/score · 🌱.
  - `+multi-letter-face` «Клітина з диграфом (Qu, Th)» · entities/state · 🌱.
  - `+found-words-list` «Список знайдених слів з дублюванням-забороною» · interface/hud · 🌱.
  - `+word-challenge` «Оскарження слова» · game-logic/opponent · 📎 (є і в `scrabble.md`).

## Пропозиції до словників
- `+cond:path_adjacent8` — літери слова йдуть шляхом по 8-сусідах без повтору клітин (Boggle, SpellTower, Strands).
- `+cond:not_played` — слово ще не було знайдене/зігране (Boggle, Letterpress).
- `+cond:length` — довжина слова порівняно з N (мінімум 3/4; очки).
- `+effect:shuffle` — перемішати плитки/кубики поля (Boggle, Connections).
- `+effect:strike_shared` — зняти з рахунку всіх гравців елемент, що збігся у ≥2 (Boggle, Scattergories).
- `+ui:found-words-list` — список знайдених слів раунду.
- `+ui:word-preview` — поточне слово з обраного шляху.
- `+window:round-results` — порівняння списків гравців після таймера.
- `+feature:word-challenge` — оскарження слова словником.

## Джерела
- ⭐ [Wikipedia: Boggle](https://en.wikipedia.org/wiki/Boggle) — кубики, Qu, суміжність, заборони, очки 4×4 і 6×6, скасування спільних слів, тай-брейк, варіанти (Jr., Big, Super Big, challenge cube, Bowl), цифрові версії, автор Allan Turoff.
- YouTube: пошук «boggle how to play».

## Непевне
- (?) Рік: Wikipedia (fetch) — «випущено 1973», у черзі — 1972; прототип Find-A-Word — 1969.
- (?) Розмір бонусу challenge cube і точні правила оскарження — вікі каже лише «бонусні очки».
- (?) Вигляд цифрових вікон (round-results, налаштування) — узагальнено з типових клонів, не з конкретної версії.
- (?) Відкат шляху drag-ом назад у цифрових версіях — з памʼяті.
- (?) Розподіл літер на кубиках різниться між виданнями (1986 жовта коробка — дві K; сучасна UK — одна); точні грані не записував.
