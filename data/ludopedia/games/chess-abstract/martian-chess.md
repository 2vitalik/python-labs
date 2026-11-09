---
title: Martian Chess
slug: martian-chess
aka: [Марсіанські шахи, "Icehouse: The Martian Chess Set"]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: score
year: 1999
platforms: [board]
links:
  - {kind: official, url: "https://www.looneylabs.com/sites/default/files/pyramid_rules/Rules.MartianChess.pdf", best: true, note: "чинні правила Looney Labs (2 с.): розстановка 3×3, ходи трьох пірамід, власність за зоною, No Undos, Field Promotions, кінець, тай-брейк, гра на 4"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Martian_Chess", note: "огляд: Andrew Looney, 1999, Origins Award 2001; очки 3/2/1; на 4 — команди по діагоналі"}
  - {kind: official, url: "https://www.looneylabs.com/rules/martian-chess", note: "версія Pyramid Primer #1: перший гравець — червона Королева з мішка, No Bouncing, тай-брейк"}
  - {kind: official, url: "https://www.looneylabs.com/content/martian-chess", note: "сторінка гри: правило «call the clock» (7 ходів без взяття), тай-брейк при годиннику"}
  - {kind: bgg, url: "https://boardgamegeek.com/boardgame/19803/martian-chess", note: "BGG (бачив посилання на сайті Looney Labs)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=martian+chess+looney+pyramids+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 75
mechanics: [piece-move-patterns, move-8dir, piece-capture, legal-move-highlight, selection-highlight, last-move-highlight, hot-seat, turn-enforcement, ai-opponent, ai-minimax, cell-click, drag-drop-piece, event-points, game-screen, main-menu, end-screen, help-window, match-setup, mode-select, state-as-data, unit-tests, +zone-ownership, +no-immediate-return, +merge-promotion, +material-points-win, +empty-zone-end, +call-the-clock, +tie-goes-to-ender, +team-play, +friendly-fire-capture]
proposes: ["+cond:in_own_zone", "+ui:zone-border", "+ui:clock-counter", "+card:zone-ownership", "+card:no-immediate-return", "+card:merge-promotion", "+card:empty-zone-end", "+card:call-the-clock", "+card:tie-goes-to-ender"]
author: opus
date: 2026-11-09
---

# Martian Chess — колір нічого не важить: твоє те, що стоїть у твоїй зоні; напав через канал — віддав фігуру супернику

## Суть
Шахоподібна гра Andrew Looney для пірамідок Icehouse (Looney Labs, 1999) на 2 або 4 гравців. Дошка поділена «каналами» на зони; гравець керує **усіма й лише** тими фігурами, що зараз стоять у його зоні. Взяти можна тільки фігуру в чужій зоні — тож атакувальна фігура після взяття опиняється в зоні суперника і стає його. Мети «мат» нема: перемагає той, хто набрав більше очок за взяті фігури (Королева 3, Дрон 2, Пішак 1), коли чиясь зона спорожніє.

## Поле і час
- 2 гравці: половина шахівниці — дві зони по 16 клітин (4×4) з каналом посередині; 4 гравці: уся шахівниця 8×8, два канали хрестом ділять її на 4 квадранти по 4×4.
- Один шар, у клітині ≤1 фігура. Колір пірамідок не має значення — їх навмисно перемішують (Rainbow-style: 9 різних кольорів кожному; Shady-style: два схожі кольори порівну).
- Розстановка: 9 фігур квадратом 3×3 у куті своєї зони (праві кути, поворотна симетрія): Королева в куті й ще дві Королеви ортогонально поруч, діагональний ряд Дронів, решта — Пішаки.
- Покроково, хід = рух однієї фігури; на 4 — хід переходить ліворуч. Першого визначає мішок: червона Королева + ще одна Королева, хто витяг червону — ходить першим (Pyramid Primer).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пішак (Pawn, мала піраміда) | piece | 1 очко; ×3 у кожного | на 1 клітину по будь-якій діагоналі, зокрема назад |
| Дрон (Drone, середня) | piece | 2 очки; ×3 | на 1–2 клітини по горизонталі чи вертикалі, без перестрибування |
| Королева (Queen, велика) | piece | 3 очки; ×3 | на будь-яку відстань по прямій у 8 напрямках, без перестрибування |
| Зона (квадрант) | zone | 16 клітин; власник — гравець | хто стоїть у зоні — належить її власнику; порожня зона = кінець гри |
| Канал | static | межа між зонами | перетин каналу = зміна власника фігури |
| Гравець | player | рахунок = сума очок взятих фігур | ходить лише фігурами своєї зони |
| Мішок для жеребу | container | червона + інша Королева | визначає першого гравця |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «кожен ставить 9 пірамід квадратом 3×3 у куті своєї зони»`; першим ходить той, хто витяг з мішка червону Королеву.
- КОЛИ `input(move, piece, to)` → ЯКЩО `turn_of(side)` і `custom: «piece стоїть у зоні side»` (`+cond:in_own_zone`) і `free(path)` → ТО `move(piece, to)`, `end_turn`; чужою зоною фігурою ходити не можна (вона не твоя).
- Патерн Пішака: ЯКЩО `custom: «to — сусідня клітина по діагоналі»` → ТО `move`; інакше `block`.
- Патерн Дрона: ЯКЩО `custom: «to на 1–2 клітини ортогонально, проміжна вільна»` → ТО `move`; інакше `block`.
- Патерн Королеви: ЯКЩО `custom: «to на прямій у 8 напрямках»` і `free(path)` → ТО `move`; перестрибувати не можна нікого.
- КОЛИ `enter(piece, zone(B))` → ТО `set_side(piece, B)` — перейшла канал і стала фігурою B, навіть без взяття.
- КОЛИ `input(move, piece, to)` → ЯКЩО `occupied(to, piece_of(B))` → ТО `disappear(target)`, `score(+pips(target))` гравцю, що бив, `move(piece, to)`, `set_side(piece, B)` («будь-яка фігура бʼє будь-яку»).
- КОЛИ `input(move, piece, to)` → ЯКЩО `occupied(to, own_piece)` і `not custom: «злиття дозволене»` → ТО `block`.
- Field promotion: КОЛИ `input(move, drone|pawn, to)` → ЯКЩО `count(own_queens, ==, 0)` і `occupied(to, own_pawn|own_drone)` → ТО `merge(drone, pawn, queen)` — обидві знімаються, ставиться одна Королева.
- Field promotion: КОЛИ `input(move, pawn, to)` → ЯКЩО `count(own_drones, ==, 0)` і `occupied(to, own_pawn)` → ТО `merge(pawn, pawn, drone)`.
- No Undos (лише на 2): КОЛИ `input(move, piece, to)` → ЯКЩО `mode(2p)` і `custom: «piece щойно перетнув канал ходом суперника, а to — клітина, з якої він прийшов»` → ТО `block`.
- КОЛИ `all_gone(pieces_in_zone(any))` → ТО `game_over` — гра кінчається, щойно будь-яка зона порожня (можна навмисно вивести свою останню фігуру за канал).
- КОЛИ `input(call_clock)` → ЯКЩО `turn_of(side)` → ТО `counter(no_capture_moves, 0)`, `custom: «годинник запущено»`.
- КОЛИ `destroyed(any_piece)` → ЯКЩО `state(clock, running)` → ТО `counter(no_capture_moves, 0)` (будь-яке взяття скидає відлік).
- КОЛИ `counter(no_capture_moves, ==, 7)` → ТО `game_over`.
- КОЛИ `game_over` → ЯКЩО `custom: «очки A > усіх інших»` → ТО `win` для A.
- КОЛИ `game_over` → ЯКЩО `custom: «нічия за очками, гру закінчила порожня зона»` → ТО `win` того, хто зробив останній хід (навіть якщо нічия між двома іншими на 3+ гравців).
- КОЛИ `game_over` → ЯКЩО `custom: «нічия за очками, гру закінчив годинник»` → ТО `draw`.
- 4 гравці (Wikipedia): КОЛИ `input(move, piece, to)` → ЯКЩО `mode(teams)` і `occupied(to, teammate_piece)` → ТО `disappear(target)`, `score(+pips)` — бити фігуру партнера легально; очки команди сумуються.
- Перемога: більше очок на момент кінця · Поразка: менше · Рахунок: Королева 3 · Дрон 2 · Пішак 1.

## Керування і ввід
- Настільна: пересунути піраміду; взята — у свою «скарбничку» поруч із дошкою.
- (цифрова версія) Клік/drag по фігурі **у своїй зоні** → `legal-move-highlight` (взяття — іншим кольором; клітини за каналом позначені як «віддаси фігуру»); фігури в чужих зонах не виділяються.
- Окрема кнопка «Запустити годинник» у свій хід; злиття (Field Promotion) — хід на свою фігуру, коли умова виконана (підсвічується як особливий хід).

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Двоє · Четверо · Проти AI · Правила → `help-window`.
- `match-setup` / `mode-select`: кількість гравців, команди на 4 (так/ні), стиль кольорів (rainbow / shady), рівень AI.
- `game-screen`: дошка 4×8 або 8×8 з каналами (`zone-border`); `turn-indicator`; `score` кожного (або команди); `captured-pieces` (піраміди з очками); `selection-highlight`, `legal-move-highlight`, `last-move-highlight` (видно, яка фігура щойно «перейшла» до тебе); `clock-counter` «ходів без взяття: N/7» після виклику годинника.
- `confirm-dialog`: «Запустити годинник?».
- `end-screen`: рахунок, причина кінця (порожня зона / годинник), тай-брейк «переміг той, хто закінчив гру».
- Переходи: main-menu → match-setup → game-screen → end-screen → game-screen (реванш) / main-menu.

## Фічі поза полем
- `mode-versus` (2), гра на 4 вільна або командна (`team-play`); `ai-opponent-levels`.
- `rules-page`; `custom-rules`: No Undos вкл/викл, годинник, Field Promotions.
- Гра на 3, 5, 6 — клиноподібні дошки Elliott «Eeyore» Evans і ромбоподібні панелі Bruno Curfs (окремий рендер поля).

## Варіації й родичі
- Видання: Icehouse: The Martian Chess Set (1999), 3HOUSE (2007), Pyramid Primer No. 1 (2013), Pyramid Arcade (2016), окреме видання 2020 (PDF правил).
- Monochrome Chess (Looney, 1996) — попередник зі звичайними шаховими фігурами, король не королівський.
- Родичі: [banqi](banqi.md) (фігури без постійного власника-кольору — інакше: відкриваються), [hexapawn](hexapawn.md) (міні-шахи), [four-player-chess](four-player-chess.md), [djambi](djambi.md) (перехід фігур між гравцями).
- **Осі варіацій**: що визначає власника фігури (колір — шахи / місце — Martian Chess / перевертання — Reversi) · мета (мат / очки за взяті) · коли кінець (мат / порожня зона / ліміт ходів без взяття) · кількість гравців (2 / 4 / клинові дошки 3–6).

## Цікавинки для курсу
- Власник фігури = функція клітини (`owner(cell)` замість `piece.color`): уся логіка ходу через одну перевірку зони — 🌱, але корисний злам звички «фігура має колір».
- Генерація ходів трьох видів + заборона ходити чужою зоною — 📎.
- No Undos: памʼять останнього ходу суперника як частина стану (`state-as-data` з полем `last_crossing`) — 🌱.
- Field Promotion — злиття двох фігур у більшу за умови «нема такого виду» — 📎.
- Годинник: лічильник ходів без взяття, що скидається будь-яким взяттям, + два різні тай-брейки — 🌱.
- AI minimax з оцінкою «очки + ризик Double Whammy» (фігура, що щойно взяла, може одразу бити твою) — 🥇.
- Гра на 4 з командами й діагональними партнерами — 🥉.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ Пішак/Дрон/Королева · `move-8dir` ↔ Королева · `piece-capture` · `legal-move-highlight`, `selection-highlight`, `last-move-highlight` · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-minimax` · `cell-click`, `drag-drop-piece` · `event-points` ↔ 3/2/1 за взяту · `game-screen`, `main-menu`, `end-screen`, `help-window`, `match-setup`, `mode-select` · `state-as-data`, `unit-tests`.
- Наявні пропозиції корпусу: `+material-points-win` (див. [janggi](janggi.md); тут — сума взятих) · `+team-play` · `+friendly-fire-capture` (на 4 — бити партнера).
- **Нема** → пропозиції карток:
  - `+zone-ownership` «Власник фігури — зона, де вона стоїть» · entities/state · 🌱 · слоти {zones: 2|4, transfer: on_enter}.
  - `+no-immediate-return` «Заборона одразу повернути фігуру суперника на клітину, з якої вона прийшла» · entities/legality · 🌱 · слот {players: 2}.
  - `+merge-promotion` «Злиття двох своїх фігур у більшу, коли такого виду нема» · entities/state · 📎 · слоти {recipes: [drone+pawn→queen, pawn+pawn→drone]}.
  - `+empty-zone-end` «Кінець гри, щойно чиясь зона порожня» · game-logic/win · 🌱.
  - `+call-the-clock` «Гравець запускає лічильник N ходів без взяття» · game-logic/opponent · 🌱 · слот {n: 7}.
  - `+tie-goes-to-ender` «Нічия за очками — перемога того, хто закінчив гру» · game-logic/score · 🌱.

## Пропозиції до словників
- `+cond:in_own_zone` — підтверджую (paper-io, splix-io): тут фігура в зоні того, хто ходить, — і це вся умова «чия фігура».
- `+ui:zone-border` — підтверджую (babble-royale): канали між зонами на полі.
- `+ui:clock-counter` — лічильник «N із 7 ходів без взяття» після виклику годинника.
- `+card:zone-ownership`, `+card:no-immediate-return`, `+card:merge-promotion`, `+card:empty-zone-end`, `+card:call-the-clock`, `+card:tie-goes-to-ender` — див. «Мапа на каталог».

## Джерела
- ⭐ [Looney Labs: Martian Chess rules (PDF)](https://www.looneylabs.com/sites/default/files/pyramid_rules/Rules.MartianChess.pdf) — зона на 16 клітин, розстановка 3×3, ходи, «будь-яка фігура бʼє будь-яку», No Undos, Field Promotions, кінець при порожній зоні, очки 1/2/3, тай-брейк, гра на 4 без No Undos, клинові дошки, стилі кольорів, поради (Double Whammy, Run for the Border).
- [Wikipedia: Martian Chess](https://en.wikipedia.org/wiki/Martian_Chess) — автор, 1999, Origins Award, командна гра на 4 з дозволом бити партнера, Monochrome Chess, перевидання.
- [Looney Labs: Pyramid Primer #1 rules](https://www.looneylabs.com/rules/martian-chess) — жереб червоною Королевою, ownership, No Bouncing, тай-брейк для 3+ гравців.
- [Looney Labs: Martian Chess (сторінка гри)](https://www.looneylabs.com/content/martian-chess) — «call the clock»: 7 ходів без взяття, взяття скидає; нічия за годинником — нічия.
- [BGG: Martian Chess](https://boardgamegeek.com/boardgame/19803/martian-chess) — посилання з сайту Looney Labs (сторінку не відкривав).
- YouTube: пошук «martian chess looney pyramids how to play».

## Непевне
- (?) Рік: Wikipedia й видання — 1999, сторінка Looney Labs каже «created in 1995» (категорія Wikipedia теж 1995) — 1995 радше рік винайдення.
- (?) Командна гра на 4 (партнери в протилежних кутах, спільний рахунок) — лише за Wikipedia; чинний PDF описує гру на 4 без команд.
- (?) Точна схема розстановки 3×3 (де саме Пішаки «similar-but-opposite») — з тексту, без схеми; на 4 — кожен у своєму куті, орієнтацію не бачив.
- (?) Чи можна ходити фігурою всередині своєї зони без перетину каналу — правила це не забороняють (так і описано), але прямо не кажуть.
- (?) Правило годинника — лише на сторінці гри, у PDF 2020 його нема; чи воно в чинному наборі правил — не ясно.
