---
title: Chess (Шахи) — цифрова гра
slug: chess
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: online
  info: full
  random: none
  goal: state
year: 1475
platforms: [web, mobile, PC, board]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rules_of_chess", best: true, note: "усі правила: рокіровка, en passant, перетворення, нічиї, годинник"}
  - {kind: official, url: "https://lichess.org/faq", note: "Lichess FAQ: Glicko-2, категорії контролю часу, повторення, тайм-аут проти недостатнього матеріалу"}
  - {kind: play, url: "https://lichess.org/analysis", note: "дошка аналізу Lichess"}
  - {kind: play, url: "https://lichess.org/training", note: "задачі (puzzles) Lichess"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=lichess+interface+tour", note: "пошук; огляд інтерфейсу клієнта"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, no-move-into-check, check-stalemate, checkmate, move-timer, ai-opponent, drag-drop-piece, sound-warnings, replay, profile-stats, daily-puzzle, level-bank, in-game-editor, +castling, +en-passant, +pawn-promotion, +repetition-draw, +move-count-draw, +insufficient-material, +premove, +move-notation, +engine-analysis, +rating-system]
proposes: ["+trigger:check", "+trigger:repetition", "+cond:attacked", "+cond:in_check", "+cond:moved", "+effect:choose_promotion", "+ui:premove-highlight", "+ui:eval-bar", "+ui:board-arrows", "+ui:last-move-highlight", "+window:analysis-board", "+window:puzzle-window", "+feature:premove", "+feature:takeback-request", "+feature:rating", "+feature:engine-analysis", "+axis:session"]
author: opus
date: 2026-11-02
---

# Шахи — шість типів фігур, мат королю, і навколо — годинник, рейтинг, аналіз

## Суть
Двоє гравців по черзі ходять фігурами шести типів на дошці 8×8; мета — мат: король суперника під ударом і жодний легальний хід цього не знімає. Ядро — патерни ходів фігур плюс глобальне обмеження «не можна лишити свого короля під шахом», яке робить легальність ходу залежною від усієї позиції. Цифрова гра (Lichess, Chess.com) додає шар, якого нема на дошці: годинник з інкрементом, premove, автоматичні нічиї, рейтинг Glicko-2, аналіз рушієм і банк задач.

## Поле і час
- Дошка 8×8, клітини a1–h8 (файли a–h, ряди 1–8), білий кут праворуч від гравця. Один шар: на клітині ≤1 фігура.
- Хід = переміщення однієї фігури (рокіровка — двох); білі ходять першими, черга строга.
- Стан позиції — не лише розстановка: право рокіровки ×4, клітина en passant, лічильник півходів без взяття/ходу пішака, номер ходу (усе це FEN). Для повторень потрібна історія позицій.
- Час — шаховий годинник: у кожного свій запас, тікає лише в того, хто ходить; Fischer-інкремент додає N с після ходу. Lichess: оцінка тривалості = `initial + 40 × increment` (с) → UltraBullet ≤29 с, Bullet ≤179, Blitz ≤479, Rapid ≤1499, Classical ≥1500. Кореспонденція — дні на хід.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король | piece | royal; moved; ×1 | 1 клітина в 8 напрямках; не може стати під удар; рокіровка |
| Ферзь | piece | slider; ×1 | будь-яка відстань по прямих і діагоналях до першої перешкоди |
| Тура | piece | slider; moved; ×2 | будь-яка відстань по горизонталі/вертикалі; бере участь у рокіровці |
| Слон | piece | slider; колір поля; ×2 | будь-яка відстань по діагоналі; завжди на полях свого кольору |
| Кінь | piece | leaper; ×2 | «буква Г» (2+1), перестрибує фігури — єдиний leaper |
| Пішак | piece | напрям; ×8 | 1 вперед на вільну; з початкового ряду — 2; бʼє по діагоналі вперед; en passant; перетворення на останньому ряду |
| Клітина en passant | zone | живе 1 півхід | «привид» пішака, що щойно ступив на 2: туди можна бити |
| Годинник | — | залишок, інкремент | тікає у сторони, що ходить; 0 → прапор |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move(piece, to))` → ЯКЩО `turn_of(side)` and `legal(move)` → ТО `move(piece, to)`, `end_turn`; інакше `block`.
- `legal(move)` = патерн фігури ∧ шлях вільний (для slider) ∧ ціль порожня або ворожа ∧ `custom: «після ходу свій король не під ударом»` (картка `no-move-into-check`).
- КОЛИ `contact(piece, enemy_piece)` (хід на зайняту) → ТО `disappear_b` (взяття); бити свого або короля не можна.
- КОЛИ `input(king two squares to rook)` → ЯКЩО `not moved(king)` and `not moved(rook)` and `free(between)` and `not in_check(side)` and `not attacked(path_of_king)` → ТО `move(king, ±2)`, `move(rook, over_king)` — рокіровка.
- КОЛИ `move(pawn, +2)` → ТО `set_state(cell_passed, en_passant, 1 ply)`; КОЛИ ворожий пішак бʼє в цю клітину → ТО `custom: «зняти пішака, що пройшов, не з клітини призначення»`; наступного півходу стан зникає.
- КОЛИ `reach(pawn, last_rank)` → ТО `choose(Q|R|B|N)` → `transform(piece)` (кількість ферзів не обмежена; auto-queen — налаштування клієнта).
- КОЛИ `after(move)` → ЯКЩО `attacked(enemy_king)` → ТО `custom: «шах»` (звук, підсвітка короля).
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` and `in_check(side)` → ТО `win` суперника (мат); ЯКЩО `no_moves(side)` and `not in_check(side)` → ТО `draw` (пат).
- КОЛИ `repetition(position, 3)` → ТО гравець може заявити `draw`; Lichess — опція автозаявки; КОЛИ `repetition(position, 5)` → ТО `draw` автоматично.
- КОЛИ `counter(halfmoves_no_capture_no_pawn, ≥, 100)` → ТО заява `draw` (правило 50 ходів); `≥ 150` → `draw` автоматично (75 ходів).
- КОЛИ `after(move)` → ЯКЩО `custom: «мат неможливий жодною послідовністю»` (K–K, K+B–K, K+N–K, заблокована позиція) → ТО `draw` (мертва позиція).
- КОЛИ `counter(clock[side], ==, 0)` → ЯКЩО суперник має матеріал, яким теоретично можна заматувати → ТО `lose(side)`; інакше `draw`.
- КОЛИ `input(resign)` → ТО `lose`; КОЛИ `input(offer_draw)` → ЯКЩО суперник приймає → ТО `draw`; КОЛИ `input(abort)` → ЯКЩО зроблено <2 ходів кожного → ТО партія скасована без рейтингу.
- Перемога: мат · здача · тайм-аут суперника · (онлайн) суперник покинув гру. Нічия: пат · повторення · 50/75 ходів · мертва позиція · угода · тайм-аут проти недостатнього матеріалу. Рахунок: 1 / ½ / 0 і зміна рейтингу.

## Керування і ввід
- Два способи ходу: drag-n-drop фігури або клік «фігура → клітина»; на вибрану фігуру — підсвітка легальних клітин (крапки, кільця на взяттях).
- Premove: поки ходить суперник, гравець задає свій хід; він виконується миттєво після ходу суперника, якщо легальний (у Bullet економить секунди). Скасування — правий клік.
- Перетворення: вікно-вибір із 4 фігур над клітиною; або auto-queen.
- Правий клік / drag правою — стрілки й кола на дошці (анотація для себе).
- Клавіатура: стрілки ←/→ — гортати історію ходів; введення ходу текстом (Lichess: поле «keyboard move», напр. `e4`, `Nf3`); `f` — перевернути дошку (?).
- Онлайн: запити takeback (повернути хід — потрібна згода суперника), «додати 15 с» супернику, пропозиція нічиєї, здача, abort.

## Вікна, меню, HUD
- `main-menu` (головна Lichess): швидкі пейринги-плитки контролю часу (1+0 … 30+20), «Create a game», «Play with a friend», «Play with the computer», список живих ігор, турніри.
- `lobby-window`: таблиця відкритих викликів (гравець, рейтинг, час, режим rated/casual) + графік-«хмара».
- `game-screen`: дошка з `cell-coordinates`; праворуч — два `player-clock` (активний підсвічений, червоніє на малому часі), імена й рейтинги, `move-list` (SAN, пари ходів, клік → позиція), `captured-pieces` / різниця матеріалу (+3), кнопки `resign-button`, `offer-draw-button`, takeback, abort, flip; `chat-box` і список глядачів.
- HUD поля: `last-move-highlight` (дві клітини останнього ходу), `legal-move-highlight`, шах — червоне сяйво під королем, `premove-highlight`, `board-arrows`.
- `end-screen` (модал/панель результату): «White wins by checkmate • 1-0», зміна рейтингу (+8), кнопки Rematch, New opponent, Analysis board.
- `analysis-board`: дошка + `eval-bar` (оцінка рушієм), лінії рушія (multi-PV), дерево варіантів з гілками, opening explorer, endgame tablebase, PGN/FEN імпорт-експорт, графік оцінки по ходах з позначками ?!/?/??, «Learn from your mistakes».
- `editor-window` (board editor): палітра фігур, розстановка, право рокіровки, хто ходить → FEN; «Continue from here» проти друга/рушія.
- `puzzle-window`: позиція, «Find the best move for white», рейтинг задачі і свій рейтинг задач, теми (мат за 2, вилка, звʼязка…), режими Puzzle Storm/Streak/Racer.
- `profile-window` / `stats-window`: рейтинги за категоріями, графік рейтингу, історія партій, перемоги/поразки/нічиї.
- `settings-window`: дошка й фігури (`skin-select`), звуки, auto-queen, premove on/off, підтвердження ходу, автозаявка трикратного повторення, Zen mode, blind mode.
- Переходи: main-menu → (плитка) пошук суперника → game-screen → end-screen → Rematch → game-screen | Analysis → analysis-board.

## Фічі поза полем
- `online-multiplayer` з пейрингом за рейтингом; `rating` Glicko-2: старт 1500 ± 1000, «?» біля рейтингу — відхилення > 110 (провізорний). Окремий рейтинг на кожну категорію часу і варіант.
- `turn-timer` / `move-timer`: Fischer-інкремент; кореспонденція — дні на хід.
- `premove`, `takeback-request` (undo лише за згодою), `replay` (будь-яка партія — PGN), `export-import` PGN/FEN.
- `engine-analysis` (Stockfish у браузері), `ai-opponent-levels` (рівні 1–8 проти компʼютера).
- `puzzle-bank` з рейтингом задач і `daily-puzzle`; навчальний розділ (Learn, координатний тренажер).
- `spectator`, `chat`, турніри (Arena, Swiss), `theme-select`/`custom-skins` (дошки, набори фігур), `sound-toggle`, accessibility: blind mode.

## Варіації й родичі
- Цифрові варіанти — окремий файл `lichess-variants` (Chess960, Crazyhouse, Atomic …). Родичі: шогі (дропи), сянці, макрук; шашки.
- Осі цифрового клієнта: **годинник** (абсолютний / Fischer-інкремент / Bronstein-delay / кореспонденція) · **хто визнає нічию** (гравець заявляє / автоматично) · **undo** (нема / за згодою / необмежено проти AI) · **ввід** (drag / клік-клік / текст / голос).
- Осі правил фігури: slider (тура/слон/ферзь) · leaper (кінь) · step (король) · асиметрична (пішак: рух ≠ взяття, напрям залежить від сторони).

## Цікавинки для курсу
- Патерни ходів як дані: slider/leaper/step + напрямки — 🥉 (одна функція генерації ходів на всі фігури).
- Легальність через «не під шах»: згенерувати псевдоходи, зробити, перевірити атаку на короля, відкотити — 🥇 (картка `no-move-into-check`).
- Мат/пат = «нема легальних ходів» × «чи під шахом» — 🥇 (картка `check-stalemate`).
- Рокіровка + en passant + перетворення: стан поза розстановкою (права, «привид»-клітина, вибір фігури) — 🥈.
- Нічиї: трикратне повторення (хеш позиції з правами і черговістю), 50 ходів, недостатній матеріал — 🥈.
- Шаховий годинник з інкрементом і premove — 🥉 (стан часу + черга відкладеного ходу).
- Нотація SAN/FEN/PGN як імпорт-експорт і `replay` — 🥈 (неоднозначність Nbd2, суфікси +/#).

## Мапа на каталог
- Є: `piece-move-patterns` ↔ 6 типів фігур · `piece-capture` ↔ взяття ходом на клітину · `legal-move-highlight` ↔ крапки-підсвітка · `no-move-into-check` · `check-stalemate` · `checkmate` · `move-timer` ↔ годинник · `turn-enforcement` · `hot-seat` (гра з другом за одним пристроєм) · `ai-opponent`/`ai-minimax` ↔ рівні компʼютера · `drag-drop-piece` + `cell-click` · `movement-animation` · `sound-effects` + `sound-warnings` (шах, мало часу) · `replay` · `profile-stats` · `leaderboard` · `daily-puzzle` + `level-bank` + `level-rating` ↔ банк задач із рейтингом · `in-game-editor` ↔ board editor · `theme-select` · `state-as-data` ↔ FEN.
- **Нема** → пропозиції карток:
  - `+castling` «Рокіровка» · entities/legality · 🥉 · слоти {conditions: text} — хід двох фігур з умовами «не ходили / шлях не під ударом».
  - `+en-passant` «Взяття на проході» · entities/legality · 🥉 — тимчасова клітина-привид на 1 півхід.
  - `+pawn-promotion` «Перетворення пішака» · entities/state · 📎 · слоти {choices} — вибір фігури на останньому ряду.
  - `+repetition-draw` «Нічия повторенням» · game-logic/constraints · 🥈 · слоти {n: 3|5, auto} — хеш позиції в історії.
  - `+move-count-draw` «Правило N ходів» · game-logic/constraints · 🌱 · слоти {n: 50|75}.
  - `+insufficient-material` «Недостатній матеріал / мертва позиція» · game-logic/constraints · 🥉.
  - `+premove` «Попередній хід» · interface/input · 🥉 — хід у черзі, виконується після ходу суперника.
  - `+move-notation` «Нотація ходів» · interface/hud · 🥈 · слоти {format: SAN|UCI|PGN} — список ходів і експорт.
  - `+engine-analysis` «Аналіз позиції рушієм» · game-logic/opponent · 🥇 — оцінка, найкраща лінія, eval-bar.
  - `+rating-system` «Рейтинг гравців» · interface/results · 🥈 · слоти {algo: elo|glicko2}.

## Пропозиції до словників
- `+trigger:check` — після ходу король сторони під ударом (звук, підсвітка, лічильник у Three-check).
- `+trigger:repetition` — позиція повторилась N разів (шахи, шогі, го-суперко).
- `+cond:attacked` — клітина під ударом сторони (рокіровка, хід короля); `+cond:in_check` — сторона під шахом; `+cond:moved` — фігура вже ходила (рокіровка, подвійний крок пішака).
- `+effect:choose_promotion` — вибір фігури перетворення (окремий від загального `choose`, бо модал над клітиною).
- `+ui:premove-highlight` · `+ui:eval-bar` · `+ui:board-arrows` (стрілки/кола гравця) · `+ui:last-move-highlight`.
- `+window:analysis-board` — дошка з рушієм і деревом варіантів; `+window:puzzle-window` — задача з рейтингом і темами.
- `+feature:premove` · `+feature:takeback-request` (undo за згодою суперника) · `+feature:rating` (Elo/Glicko) · `+feature:engine-analysis`.
- `+axis:session` — тут `match` (партія) і водночас банк задач (`level`) — два режими сесії в одному клієнті.

## Джерела
- ⭐ [Wikipedia: Rules of chess](https://en.wikipedia.org/wiki/Rules_of_chess) — рокіровка, en passant, перетворення, 3/5 повторень, 50/75 ходів, мертва позиція, прапор і недостатній матеріал (FIDE vs USCF).
- [Lichess FAQ](https://lichess.org/faq) — Glicko-2 (1500 ± 1000, «?» при RD > 110), формула контролю часу і межі категорій, автозаявка повторення, тайм-аут vs недостатній матеріал.
- [Lichess Analysis](https://lichess.org/analysis) — дошка аналізу.
- [Lichess Puzzles](https://lichess.org/training) — задача «Find the best move», Zen mode, blind mode.
- YouTube: пошук «lichess interface tour».

## Непевне
- (?) Хоткеї Lichess (`f` — перевернути, стрілки — історія) і «+15 s» — з памʼяті, сторінки налаштувань потребують логіну.
- (?) Набір вікон аналізу (tablebase, opening explorer, графік оцінки, «Learn from your mistakes») — з памʼяті; WebFetch сторінки аналізу віддав лише каркас без JS.
- (?) Режими Puzzle Storm/Streak/Racer і рівні AI 1–8 — з памʼяті.
- `year: 1475` — умовно (сучасні правила ферзя/слона, кінець XV ст.); цифрові клієнти — 1990-ті–2010-ті.
