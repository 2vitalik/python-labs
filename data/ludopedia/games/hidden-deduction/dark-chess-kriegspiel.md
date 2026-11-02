---
title: Kriegspiel + Dark Chess (Fog of War; «шахи наосліп із суддею» і «шахи в тумані»)
slug: dark-chess-kriegspiel
family: hidden-deduction
also: [chess-abstract]
klass: figure
axes:
  field: square
  time: turn
  opponent: online
  info: hidden
  random: none
  goal: state
year: 1899
platforms: [board (3 дошки + суддя), ICC (Kriegspiel = «Wild 16»), SchemingMind, Chess.com (Fog of War), web]
links:
  - {kind: other, url: "https://www.chess.com/terms/fog-of-war-chess", best: true, note: "Chess.com: правила Fog of War — видимість, без шаху, взяття короля, як зіграти"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kriegspiel_(chess)", note: "Kriegspiel: суддя, три дошки, оголошення (No / Hell no, взяття, напрям шаху, «Any?»), варіанти RAND"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dark_chess", note: "Dark chess (1989): видимість, без шаху, взяття короля, en passant, підваріанти"}
  - {kind: play, url: "https://lichess.org/variant", note: "Lichess: 8 варіантів, Fog of War / Kriegspiel серед них нема — для порівняння"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=fog+of+war+chess+chess.com+gameplay", note: "пошук; геймплей Fog of War"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kriegspiel+chess+umpire+explained", note: "пошук; Kriegspiel"}
stage: v1
coverage: 75
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, no-move-into-check, check-stalemate, checkmate, drag-drop-piece, cell-click, turn-enforcement, move-timer, ai-opponent, replay, sound-warnings, game-screen, end-screen, main-menu, settings-window, help-window, +visibility-by-moves, +capture-king-win, +referee-announcements, +illegal-try-feedback, +check-direction-announce, +pawn-try-query, +hidden-promotion, +opponent-guess-board, +post-game-reveal, +dual-board-view]
proposes: ["+trigger:attempt", "+cond:visible", "+effect:announce", "+role:referee", "+ui:ghost-pieces", "+ui:try-button", "+window:post-game-reveal", "+feature:fog-of-war", "+axis:info-asymmetry", "+card:visibility-by-moves", "+card:capture-king-win", "+card:referee-announcements", "+card:illegal-try-feedback", "+card:check-direction-announce", "+card:pawn-try-query", "+card:hidden-promotion", "+card:opponent-guess-board", "+card:post-game-reveal"]
author: opus
date: 2026-11-02
---

# Kriegspiel і Dark Chess — шахи, де ти не бачиш суперника: суддя каже «ні», або бачиш лише те, куди можеш піти

## Суть
Дві відповіді на питання «як сховати позицію суперника в шахах». **Kriegspiel** (Henry Michael Temple, 1899): кожен бачить лише свої фігури, повну позицію знає тільки суддя; гравець *пробує* ходи, суддя відповідає «No» (неможливо в цій позиції) або приймає хід, оголошує взяття з клітиною і шах із напрямком. **Dark Chess / Fog of War** (Jens Bæk Nielsen і Torben Osted, 1989): судді нема, гравець бачить свої фігури і **кожну клітину, куди може легально піти** (з ворожими фігурами на ній); шаху нема, мета — взяти короля. Ядро обох — дедукція позиції з часткових спостережень, а не з прихованих рангів.

## Поле і час
- Шахова дошка 8×8, стандартна розстановка і рух фігур ([chess.md](../chess-abstract/chess.md)).
- Kriegspiel: **три дошки** — своя у кожного (свої фігури + за бажанням здогадки про чужі), третя — у судді (повна позиція). Онлайн суддя — сервер.
- Dark Chess: одна дошка на гравця, але кожна клітина має стан видимості: видна (своя фігура або досяжна ходом) / туман. Видимість перераховується після кожного ходу.
- Покроково; у Kriegspiel хід може містити кілька спроб (нелегальні — безкоштовні, суперник їх не чує). Онлайн — з шаховим годинником.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Свої фігури (K, Q, R, B, N, P) | piece | стандартні патерни | як у шахах; видно власнику |
| Ворожі фігури | piece | приховані | Kriegspiel — ніколи не видно до кінця; Dark — видно, коли стоять на клітині, куди твоя фігура може піти |
| Король | piece | ціль | Kriegspiel — мат; Dark — взяття (може стояти під шахом, ходити під бій) |
| Пішак | piece | — | Dark: клітина перед ним невидима, якщо він заблокований (бо прямо не бʼє); Kriegspiel — «спроби» взяття через «Any?» |
| Клітина в тумані | zone | — | Dark: позначена як прихована, щоб не сплутати з порожньою |
| Суддя | neutral | повна позиція | Kriegspiel: перевіряє спроби, оголошує події обом |
| Здогадки про ворожі фігури | mark | — | Kriegspiel: гравець ставить «привидів» на свою дошку як нотатки; на гру не впливають |

## Правила (КОЛИ → ЯКЩО → ТО)
**Kriegspiel (правила Chess Variant Pages за Wikipedia)**
- КОЛИ `turn_start(side)` → ТО `announce(«White/Black to move»)`.
- КОЛИ `attempt(move)` → ЯКЩО хід неможливий у будь-якій позиції (слон ходить як кінь) → ТО `announce(«Hell no» / «Impossible»)`, спроба знову.
- КОЛИ `attempt(move)` → ЯКЩО `not legal(move)` у реальній позиції (під шах, крізь ворожу фігуру) → ТО `announce(«No»)` лише гравцю, що пробував, спроба знову (суперник про це не дізнається).
- КОЛИ `attempt(move)` → ЯКЩО `legal(move)` → ТО хід виконано; ЯКЩО взяття → `announce(«Pawn gone» | «Piece gone», square)` обом (en passant — окремо).
- КОЛИ після ходу `check` → ТО `announce(«Check on the vertical | horizontal | long diagonal | short diagonal | by a knight»)` — без клітини фігури, що дає шах.
- КОЛИ `input(any)` («Are there any?») → ЯКЩО є легальні взяття пішаком → ТО `announce(«Try!»)` і гравець **зобовʼязаний** спробувати хоч одне взяття пішаком; невдача → далі вільний хід; ЯКЩО нема → `announce(«No»)`. Без пішаків «Any?» — нелегальна спроба («Hell no»).
- Не оголошується: перетворення пішака, нелегальні спроби суперника.
- Кінець: мат, пат, троєкратне повторення, недостатній матеріал, правило 50 ходів — оголошує суддя.
- RAND-правила: суддя оголошує лише нелегальні ходи, взяття і шахи; для швидкості — ще спроби пішаків і перший хід кожного.

**Dark Chess / Fog of War**
- КОЛИ `turn_start(side)` → ТО `reveal(cells)` = свої фігури ∪ усі клітини легальних ходів своїх фігур (разом із ворожими фігурами на них); решта — `hide` (туман).
- Пішак: КОЛИ `occupied(ahead, any)` → ТО клітина попереду лишається в тумані (Wikipedia; SchemingMind показує «зайнято», але не ким).
- Шаху нема: КОЛИ `input(move)` → ЯКЩО `legal(move)` за шаховими патернами → ТО хід, навіть якщо король лишається чи йде під бій; рокіровка дозволена з-під шаху, через бите поле і під шах.
- КОЛИ король не має ходів, крім битих клітин → ТО він **мусить** туди піти (пату нема).
- КОЛИ `contact(piece, enemy_king)` → ТО `win` (`capture-king`).
- En passant: дозволено; пішак-ціль і пропущена клітина видні тому, хто бʼє, лише до кінця ходу.
- Chess.com: чуже взяття і перетворення не видно, якщо жодна твоя фігура не «дивиться» на ту клітину.
- Підваріанти: Dark chess (checkmate) — звичайні правила шаху, мета мат; Dark chess (check) — шах оголошується, але можна лишатись під шахом, мета — взяття.
- Перемога: Kriegspiel — мат; Dark — взяти короля · Поразка — дзеркально · Нічия: Kriegspiel — пат, повторення, 50 ходів; Dark — пату нема.

## Керування і ввід
- Обидва: drag-n-drop або клік фігура → клітина; підсвітка легальних ходів (у Dark вона ж і є «що я бачу»).
- Kriegspiel: невдала спроба лишає фігуру на місці з повідомленням «No» — можна пробувати далі; кнопка «Any?» (`try-button`); ручні «привиди» ворожих фігур на дошці (права кнопка / окрема палітра) (?).
- Обидва онлайн: годинник, кнопки здатися / нічия.

## Вікна, меню, HUD
- `main-menu` / `mode-select`: розділ «Variants» → Fog of War (chess.com); на ICC — «Wild 16».
- `match-setup`: контроль часу, виклик конкретного гравця або пошук суперника.
- `game-screen` Dark: дошка з `fog-overlay` (туман — заштриховані клітини), свої фігури, видимі ворожі; `player-clock` ×2; `move-list` лише своїх ходів (?); `captured-pieces`.
- `game-screen` Kriegspiel: своя дошка + `message-log` судді («No», «Piece gone d5», «Check on the long diagonal», «Try!»), `try-button` «Any?», лічильник ворожих фігур (відомо, скільки лишилось), `ghost-pieces` — здогадки.
- `end-screen` + `post-game-reveal`: після кінця — повна дошка обох сторін і повтор партії з усіма фігурами (`replay`) (?).
- `help-window` / сторінка правил варіанту (chess.com Terms).
- Переходи: main-menu → variants → match-setup → game-screen → end-screen → post-game-reveal/replay → реванш.

## Фічі поза полем
- `online-multiplayer` (головний режим: потрібен судді-сервер або приховування позиції від клієнта), `turn-timer` (контроль часу), `spectator` (глядач бачить усю дошку?) (?), `history` / `replay` з повною інформацією після гри.
- `ai-opponent-levels` — проблема: класичні рушії не працюють з неповною інформацією; потрібні моделі переконань / Monte Carlo за ймовірними позиціями (?).
- `custom-rules`: набори правил Kriegspiel (English, ICC/Wild 16, RAND, Cincinnati (?)), підваріанти Dark (checkmate / check / capture).
- Онлайн-платформи: ICC («Wild 16»), SchemingMind (обидва), Chess.com (Fog of War; у вересні 2020 — найпопулярніший варіант сайту). На Lichess цих варіантів нема.

## Варіації й родичі
- Kriegsspiel фон Райсвіца (1812) — військова гра-попередник назви. Варіанти Kriegspiel: Frankenstein 1903 «Pickle pot» / «One-eye» (один бачить усе, але має менше фігур), Semi-kriegspiel (1971), Modern kriegspiel (1986), Crazyhouse Kriegspiel; tsuitate shogi — шогі-аналог.
- Dark: Dark crazyhouse, Dark suicide, Sun Tzu, Lao Tzu, Dark Omega, Dark Seirawan.
- Родичі: Stratego і Geister (приховано *хто*, а не *де*), Battleship (приховане розміщення, відгук «влучив/мимо» = «No/взяття»), RTS-«туман війни».
- **Осі варіацій**: що приховано «позиція всіх ворожих фігур (Kriegspiel) / поза зоною досяжності (Dark)»; джерело інформації «суддя-оголошення / власна видимість»; шах «оголошується з напрямком / не існує / оголошується без примусу»; ціль «мат / взяття короля»; нелегальна спроба «безкоштовна, приватна / неможлива (UI не дає)».

## Цікавинки для курсу
- Видимість = обʼєднання легальних ходів своїх фігур, перерахунок щоходу, туман-оверлей — 🥉 (поверх готового генератора ходів).
- Генератор «псевдолегальних» ходів без перевірки шаху + перемога взяттям короля — 📎 (Dark — простіше за класичні шахи!).
- Суддя-сервер Kriegspiel: спроба → «No» / виконання / оголошення взяття з клітиною і шаху з напрямком — 🥈.
- Класифікація напрямку шаху (вертикаль, горизонталь, довга/коротка діагональ відносно короля, кінь) — 📎.
- Дві/три проєкції одного стану (суддя бачить усе, гравець — свою) і чесний клієнт, який не отримує чужих фігур — 🥉 (архітектура «сервер знає, клієнт бачить»).
- «Привиди»-здогадки на своїй дошці — 🌱; AI, що підтримує множину можливих позицій суперника (belief state) — 👑.
- Розкриття всієї партії після кінця (replay з повною інформацією) — 📎.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` · `legal-move-highlight` (у Dark = видимість) · `no-move-into-check` + `check-stalemate` + `checkmate` (Kriegspiel) · `drag-drop-piece` + `cell-click` · `turn-enforcement` · `move-timer` · `ai-opponent` · `replay` · `sound-warnings` (шах) · `game-screen` / `end-screen` / `main-menu` / `settings-window` / `help-window`.
- **Нема** → пропозиції карток:
  - `+visibility-by-moves` «Туман: видно лише досяжні клітини» · interface/render · 🥉 · слот {pawn_forward: hidden|occupied-flag}.
  - `+capture-king-win` «Перемога взяттям короля, без правила шаху» · game-logic/win · 📎.
  - `+referee-announcements` «Суддя: публічні оголошення подій» · game-logic/opponent · 🥈 · слот {ruleset: english|rand|icc}.
  - `+illegal-try-feedback` «Нелегальна спроба — приватне «ні», хід не втрачено» · entities/legality · 📎.
  - `+check-direction-announce` «Оголошення напрямку шаху» · game-logic/constraints · 📎.
  - `+pawn-try-query` «Запит «Any?» і примусова спроба взяття» · game-logic/opponent · 📎.
  - `+hidden-promotion` «Перетворення, невидиме супернику» · entities/state · 🌱.
  - `+opponent-guess-board` «Нотатки-привиди ворожих фігур» · interface/hud · 🌱.
  - `+post-game-reveal` «Повне розкриття після кінця» · interface/results · 🌱.
  - `+dual-board-view` — див. Battleship (тут три проєкції: суддя + два гравці).

## Пропозиції до словників
- `+trigger:attempt(move)` — гравець *пробує* хід, рішення приймає суддя (відмінно від `input`, бо невдала спроба не завершує хід і невидима супернику).
- `+cond:visible(cell, side)` — клітина видна стороні (туман).
- `+effect:announce(text, to)` — публічне/приватне оголошення судді (див. Battleship).
- `+role:referee` — сутність, що знає повний стан і видає інформацію гравцям (суддя, сервер; у Gunjin Shōgi — теж).
- `+ui:ghost-pieces` — здогадки про ворожі фігури поверх своєї дошки; `+ui:try-button` — кнопка «Any?».
- `+window:post-game-reveal` — екран розкриття прихованого після кінця партії.
- `+feature:fog-of-war` — режим прихованої позиції (на відміну від Stratego `fog-of-ranks`).
- `+axis:info-asymmetry` — див. Geister; Kriegspiel — `both-but-referee`, Dark — `opponent` (динамічний).
- Вжито наявні ⏳ без пропозицій: `fog-overlay`, `message-log`, `player-clock`, `captured-pieces`, `move-list`, `mode-select`, `match-setup`, `neutral`.

## Джерела
- ⭐ [Chess.com: Fog of War chess](https://www.chess.com/terms/fog-of-war-chess) — видимість, без шаху й мату, без пату, взяття короля, приховані взяття/перетворення, як почати гру.
- [Wikipedia: Kriegspiel (chess)](https://en.wikipedia.org/wiki/Kriegspiel_(chess)) — Temple 1899, три дошки, усі оголошення судді, «Any?»/«Try!», RAND-правила, Wild 16 на ICC, SchemingMind, варіанти.
- [Wikipedia: Dark chess](https://en.wikipedia.org/wiki/Dark_chess) — Nielsen і Osted 1989, видимість, пішак, en passant, рокіровка, підваріанти, Chess.com 2020.
- [Lichess: варіанти](https://lichess.org/variant) — для порівняння: Fog of War / Kriegspiel нема.
- YouTube: пошуки «fog of war chess chess.com gameplay», «kriegspiel chess umpire explained».

## Непевне
- (?) Kriegspiel на ICC (Wild 16) — точні правила оголошень сервера не перевірено; Cincinnati-правила — з памʼяті.
- (?) Чи chess.com показує після партії повну дошку і чи глядачі бачать усе — не перевірено.
- (?) Інтерфейс «привидів» і кнопки «Any?» — загальна практика онлайн-Kriegspiel, конкретний сервер не перевірено.
- (?) AI для Fog of War / Kriegspiel (belief state, Monte Carlo) — загальне знання, джерело не дивився.
- (?) Чи chess.com прибрав підсвітку en passant-клітини (Wikipedia: «до 5.11.2021 підсвічувалась») — зміна є, деталі не перевірено.
