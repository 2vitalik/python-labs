---
title: Geister (Ghosts!, Good & Bad Ghosts; «Привиди»)
slug: geister
family: hidden-deduction
also: [chess-abstract]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: none
  goal: state
year: 1982
platforms: [board (Milton Bradley, Schmidt, Drei Magier та ін.), PS2 (European Game Collection, 2003), web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ghosts_(board_game)", best: true, note: "правила коротко: 6×6, 4+4 привиди, три умови перемоги"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ガイスター", note: "японська стаття: вихід «стань на кут, наступним ходом вийди», заборона пропуску ходу, номінація Spiel des Jahres 1982"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=ghosts+randolph", note: "пошук BGG; видання"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=geister+ghosts+board+game+randolph+how+to+play", note: "пошук; правила"}
  - {kind: other, url: "https://en.wikipedia.org/w/index.php?search=Geister+AI&ns0=1", note: "пошук; Geister як тестова гра для AI з неповною інформацією"}
stage: v1
coverage: 80
mechanics: [piece-capture, piece-move-patterns, legal-move-highlight, cell-click, drag-drop-piece, hot-seat, turn-enforcement, ai-opponent, ai-random, ai-greedy, game-screen, end-screen, main-menu, help-window, mode-indicator, +hidden-rank-reveal, +setup-zone-placement, +dual-board-view, +exit-escape, +poison-capture, +capture-quota-win, +belief-state-ai]
proposes: ["+trigger:escape", "+cond:hidden_kind", "+effect:reveal_kind", "+ui:captured-by-kind", "+window:placement-screen", "+window:pass-device", "+feature:fog-of-ranks", "+axis:info-asymmetry", "+card:exit-escape", "+card:poison-capture", "+card:capture-quota-win", "+card:belief-state-ai"]
author: opus
date: 2026-11-02
---

# Geister — вісім однакових привидів, половина з них «отруйна»: блефуй, бий обережно, виведи доброго через кут

## Суть
Двоє гравців мають по 8 привидів, що виглядають однаково ззовні: 4 добрі (синя мітка на спині) і 4 злі (червона). Хід — один привид на 1 клітину ортогонально; удар — хід на ворожого, і лише тоді нападник дізнається, кого зʼїв. Три умови кінця роблять бій неоднозначним: зʼїж усіх добрих суперника — перемога; зʼїж усіх його злих — поразка; виведи свого доброго через кутовий вихід на боці суперника — перемога. Мінімальна гра «прихована ідентичність + блеф»: Stratego, стиснутий до двох типів фігур (Alex Randolph, 1982).

## Поле і час
- Дошка 6×6 («зачарований замок»), у кожному з 4 кутів — вихід; гравцю доступні лише два виходи на дальньому (ворожому) краю.
- Розстановка: два ряди по 4 привиди біля свого краю (центральні 4 стовпці; кути порожні (?)), розподіл добрих/злих — довільний, спинкою до себе.
- Шари: клітина → привид (сторона + вид good/bad) + видимість виду: власник бачить завжди, суперник — лише після взяття.
- Покроково, по черзі; пропуск ходу заборонений. Партія 5–25 хв.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Добрий привид | piece | ×4, вид good (прихований) | рух 1 ортогонально; лише він може вийти через вихід |
| Злий привид | piece | ×4, вид bad (прихований) | рух 1 ортогонально; на кут стати може, вийти — ні; бути зʼїденим — «отрута» для нападника |
| Вихід (кут) | static | 4 шт., працює лише для суперника з протилежного боку | добрий привид, що стоїть тут на початку свого ходу, може вийти з дошки |
| Порожня клітина | static | — | хід лише на порожню або ворожу |
| Полон (захоплені) | zone | лічильники good/bad | зʼїдені привиди лежать відкрито біля нападника, не повертаються |

## Правила (КОЛИ → ЯКЩО → ТО)
- Розстановка: КОЛИ `input(place, ghost, cell)` → ЯКЩО клітина у своїй зоні 2×4 і `free(cell)` → ТО `place`; КОЛИ обидва поставили всі 8 → `turn_start(first)`.
- КОЛИ `input(move, g, to)` → ЯКЩО `turn_of(side)` і `to` — сусідня ортогональна і не `occupied(to, own)` → ТО `move(g, to)`; інакше `block`.
- КОЛИ `contact(g, enemy)` (хід на ворожу клітину) → ТО `disappear_b`, `reveal(enemy_kind)` нападнику, `counter(captured_<kind>, +1)`.
- КОЛИ `counter(captured_good, ==, 4)` (зʼїв усіх добрих суперника) → ТО `win`.
- КОЛИ `counter(captured_bad, ==, 4)` (зʼїв усіх злих суперника) → ТО `lose` — `custom: «отруєння: перемога супернику»`.
- КОЛИ `turn_start(side)` → ЯКЩО `cell(g, enemy_exit)` і `hidden_kind(g, good)` → ТО гравець може `input(escape, g)` → `disappear_a`, `win`.
- КОЛИ `input(escape, g)` → ЯКЩО `hidden_kind(g, bad)` → ТО `block` (у цифровій версії кнопки виходу для злого просто нема — суперник нічого не дізнається).
- Вихід у два кроки: стати на кут → дочекатись свого наступного ходу. Суперник має рівно один хід, щоб зʼїсти привида на куті — і ризикнути, що той злий.
- КОЛИ `no_moves(side)` → `custom: «у джерелах не описано»` (?).
- Перемога: 4 зʼїдені добрі ворога · вихід доброго · суперник зʼїв усіх твоїх злих. Поразка — дзеркально. Рахунку нема.

## Керування і ввід
- Настолка: рука переставляє фігуру; взяття — забрати і перевернути.
- Цифрова версія: клік по своєму привиду → підсвітка 1–4 легальних клітин → клік по цілі (або drag-n-drop); на куті — окрема кнопка/стрілка «вийти»; фаза розстановки — тап для перемикання good/bad або перетягування з лотка.
- Hotseat: між ходами — екран-завіса, бо на одному пристрої видно мітки своїх привидів.

## Вікна, меню, HUD
- `main-menu`: гра проти AI · hotseat · правила (`help-window`).
- `placement-screen` (цифрова версія): своя половина дошки 2×4 + лоток із 4 синіми і 4 червоними; «Випадково», «Готово».
- `pass-device` (цифрова версія, hotseat): «Передай пристрій гравцю 2» між ходами, щоб не підглянути мітки.
- `game-screen`: дошка 6×6, свої привиди з кольоровою міткою, чужі — однакові; виходи підсвічено на кутах; `turn-indicator`; `captured-by-kind` — дві полички «зʼїв: 🔵×n 🔴×m» для кожного; `last-move-arrow` (див. Stratego).
- `end-screen`: причина кінця (втеча / 4 добрі / 4 злі «отруєння») + розкриття всіх привидів суперника.
- Переходи: main-menu → placement-screen ×2 (через pass-device) → game-screen → end-screen → main-menu / реванш.

## Фічі поза полем
- `hotseat` + `pass-device`, `ai-opponent-levels` (випадковий → жадібний → з моделлю переконань), `rules-page`, `history`/реванш.
- `fog-of-ranks` (термін зі Stratego) — режим прихованого виду; навчальний режим «відкрито» (усе видно) — для пояснення правил (?).
- PS2: у збірці European Game Collection (2003) — єдина відома комерційна цифрова версія за Wikipedia.

## Варіації й родичі
- Stratego / L'Attaque — та сама ідея прихованої ідентичності, але 12 рангів і бій за таблицею; Gunjin Shōgi — суддя порівнює приховані ранги.
- Kriegspiel / Dark Chess — приховано не *хто* фігура, а *де* вона ([dark-chess-kriegspiel.md](dark-chess-kriegspiel.md)).
- Battleship — приховане розміщення без руху.
- **Осі варіацій**: що приховано «вид фігури (Geister, Stratego) / позиція (Kriegspiel) / розміщення (Battleship)»; взяття «завжди добре / може бути отрутою (Geister) / вирішує ранг (Stratego)»; втеча «через кут у 2 кроки / нема»; кількість видів «2 / 12».

## Цікавинки для курсу
- Три умови кінця з прихованим видом (дві з них симетричні, одна — інверсна «отрута») — 📎: просте, але змушує думати про стани гри.
- Вихід у 2 кроки (стань → наступним ходом вийди) як вікно реакції для суперника — 🌱.
- Дві проєкції одного стану (свій вид бачу / чужий — ні) + hotseat із завісою — 🥉 (спільне з Stratego, Battleship).
- AI з моделлю переконань: імовірність «добрий» для кожного ворожого привида оновлюється за поведінкою (тікає від взяття, біжить до виходу) — 🥇.
- Чесний AI, що не «підглядає» у прихований стан — архітектурна вимога: двіжок віддає AI лише його проєкцію — 🥉 (`logic-render-split` + проєкція стану).

## Мапа на каталог
- Є: `piece-capture` · `piece-move-patterns` (1 ортогонально) · `legal-move-highlight` · `cell-click` + `drag-drop-piece` · `hot-seat` + `turn-enforcement` · `ai-opponent` / `ai-random` / `ai-greedy` · `mode-indicator` (чий хід) · `game-screen` / `end-screen` / `main-menu` / `help-window`.
- **Нема** → пропозиції карток:
  - `+hidden-rank-reveal` · `+setup-zone-placement` — див. Stratego (тут ранг = good/bad).
  - `+dual-board-view` — див. Battleship (тут одна дошка, дві проєкції).
  - `+exit-escape` «Втеча через вихід у 2 кроки» · game-logic/win · 🌱 · слот {steps: 1|2, who: kind}.
  - `+poison-capture` «Отруйне взяття: зʼїв N певного виду — програв» · game-logic/lose · 🌱 · слот {kind, n}.
  - `+capture-quota-win` «Перемога за квотою взятих певного виду» · game-logic/win · 🌱 · слот {kind, n}.
  - `+belief-state-ai` «AI з імовірнісною моделлю прихованих фігур» · game-logic/opponent · 🥇.

## Пропозиції до словників
- `+trigger:escape` — фігура виходить за межу поля через дозволену клітину (відмінно від `edge(a)`, бо це дія гравця, а не випадковий вихід).
- `+cond:hidden_kind` — прихований вид фігури (good/bad, ранг); відомий власнику, невідомий суперникові.
- `+effect:reveal_kind` — розкрити вид лише одному гравцю (див. Dragonsweeper — там про вид клітини).
- `+ui:captured-by-kind` — полички взятих фігур, розкладені за видом (тут — головний індикатор близькості двох кінців гри).
- `+window:placement-screen` · `+window:pass-device` — див. Battleship/Stratego.
- `+feature:fog-of-ranks` — див. Stratego.
- `+axis:info-asymmetry` — від кого приховано: `everyone` (Memory, Minesweeper) · `opponent` (Geister, Stratego, Battleship) · `both-but-referee` (Kriegspiel) · `player-vs-game` (Wumpus, Mastermind).

## Джерела
- ⭐ [Wikipedia: Ghosts (board game)](https://en.wikipedia.org/wiki/Ghosts_(board_game)) — 6×6, 4 добрі + 4 злі, розстановка, рух, взяття, три умови перемоги, видавці.
- [Wikipedia JA: ガイスター](https://ja.wikipedia.org/wiki/ガイスター) — вихід у 2 кроки, злі не виходять, пропуск ходу заборонено, Spiel des Jahres 1982 (номінація), PS2-версія.
- [BGG пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=ghosts+randolph) — видання (сторінку BGG не відкрито: 403).
- YouTube: пошук «geister ghosts board game randolph how to play».

## Непевне
- (?) Точні клітини розстановки (центральні 4 стовпці двох задніх рядів, кути порожні) — з памʼяті; Wikipedia каже лише «два ряди по чотири вздовж краю».
- (?) Що буває, коли гравець не має ходу (усі заблоковані) — джерела мовчать.
- (?) Чи нападник показує зʼїденого привида обом гравцям, чи лише собі — у настолці зазвичай кладуть відкрито; Wikipedia: «only upon capture does the capturing player learn».
- (?) Geister як тестова гра для AI-змагань з неповною інформацією (Японія) — з памʼяті, не перевірено (вебпошук вичерпано).
