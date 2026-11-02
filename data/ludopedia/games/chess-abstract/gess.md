---
title: Gess
slug: gess
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: none
  goal: state
year: 1994
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gess", best: true, note: "правила: 3×3-відбиток, напрями від каменів, центр = дальність, кільця"}
  - {kind: play, url: "https://playgess.com/", note: "грати проти AI (колишній hGess; лінк зі статті Wikipedia)"}
  - {kind: other, url: "https://www.chessvariants.com/old.dir/gess.html", note: "Chess Variant Pages: правила Archimedeans"}
  - {kind: play, url: "https://sites.astro.caltech.edu/~aam/personal/fun/egames/gess.html", note: "старий веб-аплет з коротким формулюванням правил"}
  - {kind: other, url: "https://red-bean.com/sgf/gess.html", note: "SGF FF[4]: формат запису партій Gess"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=gess", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=gess+board+game+go+chess", note: "пошук; пояснення й партії"}
stage: v1
coverage: 65
mechanics: [piece-capture, move-8dir, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-minimax, cell-click, hover-highlight, legal-move-highlight, drag-drop-piece, game-screen, end-screen, help-window, replay, state-as-data, +footprint-piece, +pattern-directions, +overlap-capture, +off-board-removal, +ring-survival-win, +move-notation]
proposes: ["+trigger:pattern", "+cond:footprint", "+cond:pattern_present", "+effect:move_group", "+effect:clear", "+ui:footprint-preview", "+ui:direction-arrows", "+window:footprint-select", "+axis:piece-identity", "+axis:field-bounds", "+axis:win-condition", "+card:footprint-piece", "+card:pattern-directions", "+card:overlap-capture"]
author: opus
date: 2026-11-02
---

# Gess — «шахи на дошці го»: фігура — будь-який 3×3-відбиток твоїх каменів, його візерунок і є правилом ходу

## Суть
На поле 18×18 (дошка го) кожна сторона ставить по 43 камені. Фігур як таких нема: «фігурою» стає будь-який квадрат 3×3, у якому лише твої камені; камені по периметру задають, у які з 8 напрямків квадрат може рухатися, а камінь у центрі — чи далеко (до 3 клітин або необмежено). Рухається весь відбиток разом і зупиняється, щойно накриє чужі камені, — накриті знімаються. Програє той, у кого не лишилось жодного «кільця» (8 каменів навколо порожнього центру) — аналог короля. Гру придумали Archimedeans (Кембридж) у 1994-му, популяризував Ian Stewart у Scientific American.

## Поле і час
- Сітка 18×18 клітин (камені ставлять у клітини; набір го з 19×19 ліній теж підходить); нотація — ряди 2–19, колони b–s, тобто 20×20 з невидимою «сутінковою» рамкою, у яку може заходити частина відбитка, але камені там не живуть.
- Старт: кожна сторона — 43 камені, викладені «шаховою» формацією (тура, слон, ферзь, король, слон, тура + 6 «пішаків» відбитками) (?).
- Хід = один рух одного відбитка; чорні ходять першими; пасувати не можна, хід мусить змінити розстановку каменів.
- Фігури **емерджентні**: той самий камінь у різних 3×3-вікнах належить різним «фігурам»; набір фігур перераховується після кожного ходу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Камінь | object | колір | сам не ходить; рухається лише у складі відбитка; знімається, коли його накрили або виштовхнули за край |
| Відбиток (фігура) | piece | 3×3 вікно, центр | лише камені одного кольору; ≥1 камінь на 8 периферійних клітинах; рухається цілим |
| Периферійний камінь | — | позиція N/NE/E/SE/S/SW/W/NW | дозволяє рух у своєму напрямку від центру; порожня периферія — напрям заборонено |
| Центральний камінь | — | є / нема | є → дальність необмежена; нема → до 3 клітин |
| Кільце | zone | 8 каменів навколо порожнього центру | «король»: без жодного кільця після ходу — поразка; може бути кілька |
| Рамка (twilight zone) | static | 1 клітина довкола поля | відбиток може частково заходити; камені, що опинились там, знімаються |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select(center))` → ЯКЩО `footprint(center)` містить лише свої камені and `count(own on periphery, >=, 1)` → ТО відбиток — легальна фігура.
- КОЛИ `input(move(footprint, dir, n))` → ЯКЩО `occupied(periphery[dir], own)` and (`occupied(center, own)` or `n <= 3`) → ТО `move_group(footprint, dir)` крок за кроком.
- На кожному кроці: КОЛИ `custom: «відбиток у новому положенні накрив будь-які камені поза собою»` → ТО `disappear(overlapped)` (обох кольорів), рух зупиняється; інакше рух можна продовжити або зупинити за бажанням.
- КОЛИ `edge(stone)` (камінь вийшов у рамку/за край) → ТО `disappear(stone)`.
- КОЛИ `turn_end(side)` → ЯКЩО `custom: «розстановка не змінилась»` → ТО хід нелегальний.
- КОЛИ `turn_end(side)` → ЯКЩО `not pattern_present(ring, enemy)` and `pattern_present(ring, own)` → ТО `win(side)`.
- КОЛИ `turn_end(side)` → ЯКЩО `not pattern_present(ring, own)` → ТО `lose(side)` (і коли кілець нема в обох — програє той, хто ходив).
- Обмеження оригінальних правил: не можна брати кільце суперника частиною власного кільця (?).
- Перемога: знищити всі кільця суперника · Поразка: лишитися без кільця після свого ходу (самознищення теж рахується) · Рахунок: 1/0.

## Керування і ввід
- Клік по центру 3×3 → клієнт підсвічує відбиток і дозволені напрямки (стрілки) з дальністю; клік по цільовому центру або drag відбитка.
- Альтернативно — вибір рамкою 3×3 будь-де (цифрова версія), бо будь-яке вікно з власними каменями є фігурою.
- Нотація: центр відбитка до і після (`c3-c6`), як у SGF-форматі Gess.

## Вікна, меню, HUD
- `game-screen` (playgess.com, аплети): сітка 18×18 з рамкою, `footprint-preview` (рамка 3×3 під курсором), `direction-arrows` (дозволені напрямки), `legal-move-highlight` (досяжні центри), `turn-indicator`, лічильник кілець сторони, `move-list`.
- `footprint-select` (цифрова версія) — режим вибору довільного 3×3 вікна.
- `match-setup`: колір, рівень AI; `help-window` — правила з діаграмами відбитків.
- `end-screen`: «кільця суперника знищено» / «ти лишився без кільця».
- Переходи: main-menu → match-setup → game-screen → end-screen → replay.

## Фічі поза полем
- `ai-opponent-levels` (playgess.com), `hotseat`, `replay`, `export-import` партій у SGF (FF[4] має тип гри Gess).
- `rules-page` — у різних реалізацій правила рамки й частково поза-полевих відбитків розходяться, тож явна сторінка правил потрібна.
- `custom-rules` — опції країв (рамка 20×20 vs «за фізичним краєм»).

## Варіації й родичі
- Реалізації розходяться в обробці краю: «сутінкова зона» 20×20 vs відбитки, що повністю виходять за дошку (обговорення на сторінці Wikipedia).
- Родичі за ідеєю «фігура = візерунок»: Game of Life (поведінка з локального шаблону), [go.md](go.md) (камені й дошка), [chess.md](chess.md) (формація старту), Abalone (рух групи) [abalone.md](abalone.md).
- **Осі варіацій**:
  - **Ідентичність фігури**: фіксований тип (шахи) · ранг (Arimaa) · **емерджентна з візерунка** (Gess).
  - **Звідки береться патерн ходу**: таблиця типу · карта-рух (Onitama) · візерунок самої фігури (Gess).
  - **Взяття**: заміщення · накриття всім відбитком з зупинкою (Gess) · виштовхування за край (Abalone).
  - **«Король»**: одна фігура · будь-який екземпляр шаблону (кільце Gess).

## Цікавинки для курсу
- Фігура як 3×3-вікно з перевіркою «лише свої, ≥1 на периметрі» — 📎.
- Напрямки й дальність з візерунка (8 бітів + центр) — 🥉: патерн ходу як дані, а не код.
- Рух групи з покроковою перевіркою накриття й зупинкою, зняття каменів за краєм — 🥉.
- Пошук кілець після кожного ходу (шаблон 3×3 по всьому полю, включно з самознищенням) — 📎.
- Генерація всіх ходів: кожне вікно 3×3 × 8 напрямків × дальність — розгалуження величезне; AI — 🥇.
- Обидва режими краю (рамка vs поза дошкою) як налаштування — 🥉.

## Мапа на каталог
- Є: `piece-capture` (тут — накриттям) · `move-8dir` · `hot-seat` · `turn-enforcement` · `move-timer` · `ai-opponent` / `ai-minimax` · `cell-click` + `hover-highlight` + `legal-move-highlight` + `drag-drop-piece` · `game-screen` · `end-screen` · `help-window` · `replay` · `state-as-data`.
- **Нема** → пропозиції карток:
  - `+footprint-piece` «Фігура = вікно 3×3 своїх каменів» · entities/state · 🥉 — емерджентні фігури.
  - `+pattern-directions` «Напрямки й дальність з візерунка фігури» · entities/legality · 🥉 · слоти {range_short: 3, range_long: ∞}.
  - `+overlap-capture` «Взяття накриттям з зупинкою руху» · entities/combat · 📎.
  - `+off-board-removal` «Знімання за краєм поля» · entities/death · 🌱 · слоти {border: twilight|physical}.
  - `+ring-survival-win` «Програє той, у кого не лишилось шаблону-короля» · game-logic/win · 📎.
  - `+move-notation` — центр до/після.

## Пропозиції до словників
- `+trigger:pattern` (⏳ є) — підтверджую з новим шаблоном `ring` (8 навколо порожнього центру).
- `+cond:footprint(center, side)` — 3×3-вікно є легальною фігурою сторони.
- `+cond:pattern_present(shape, side)` — на полі існує хоч один екземпляр шаблону (кільце); ≠ тригер `pattern` (той — подія, тут — інваріант).
- `+effect:move_group` — підтверджую (з abalone.md): зсув групи каменів як цілого.
- `+effect:clear` (⏳ є) — зняття накритих каменів.
- `+ui:footprint-preview` — рамка 3×3 під курсором; `+ui:direction-arrows` — підтверджую (з abalone.md).
- `+window:footprint-select` — режим вибору довільного вікна як фігури (цифрова версія).
- `+axis:piece-identity` — нова вісь: `typed` · `ranked` · `emergent`.
- `+axis:field-bounds` — підтверджую: значення `twilight-border`.
- `+axis:win-condition` — значення `pattern-survival`.

## Джерела
- ⭐ [Wikipedia: Gess](https://en.wikipedia.org/wiki/Gess) — поле, 43 камені, визначення відбитка, напрямки/дальність, накриття, край, кільця, нотація, історія (Archimedeans, Eureka 1994, Ian Stewart).
- [playgess.com](https://playgess.com/) — гра проти AI (лінк зі статті Wikipedia; сторінка не відкрилась за таймаутом).
- [Chess Variant Pages: Gess](https://www.chessvariants.com/old.dir/gess.html) — правила (знайдено пошуком).
- [Caltech: Gess applet](https://sites.astro.caltech.edu/~aam/personal/fun/egames/gess.html) — коротке формулювання «вікно без каменів суперника, ≥1 свій на периметрі».
- [SGF: Gess](https://red-bean.com/sgf/gess.html) — формат запису партій.
- YouTube: пошук «gess board game go chess».

## Непевне
- (?) Точна стартова формація (які 3×3-шаблони відповідають яким шаховим фігурам) — Wikipedia лише каже «імітує шахові фігури на 6×6».
- (?) Заборона «брати кільце суперника частиною свого кільця» — з підсумку пошуку, першоджерела (Eureka) не бачив.
- (?) Чи може відбиток зайти за край більше ніж на одну клітину — реалізації й Wikipedia-обговорення розходяться.
- (?) Чи може відбиток рухатись через порожнечу «до 3» з зупинкою раніше без накриття — так за Wikipedia («move may end early»), але деталі зупинки на першому накритті — за пошуковим підсумком.
