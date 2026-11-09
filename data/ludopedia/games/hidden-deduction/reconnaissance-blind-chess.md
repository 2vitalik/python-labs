---
title: Reconnaissance Blind Chess (RBC)
slug: reconnaissance-blind-chess
aka: [RBC, Recon Chess, Reconnaissance Chess, Reconnaissance Blind Multi-Chess]
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
year: 2016
platforms: [web, Android, iOS, Python (reconchess)]
links:
  - {kind: official, url: "https://rbc.jhuapl.edu/gameRules", best: true, note: "правила: зонд 3×3, повідомлення про взяття, ковзання крізь фігуру, нелегальні ходи, без шаху, 15 хв + 5 с, нічия за 50 ходів"}
  - {kind: official, url: "https://rbc.jhuapl.edu/", note: "сайт JHU APL: гра з ботами й людьми, рейтинг, турніри NeurIPS 2019/2021/2022, застосунки"}
  - {kind: other, url: "https://reconchess.readthedocs.io/en/latest/rules.html", note: "правила бібліотеки reconchess: фази ходу, requested vs taken move, промоція у ферзя за замовчуванням"}
  - {kind: other, url: "https://ar5iv.labs.arxiv.org/html/1811.03119", note: "On the Complexity of RBC: 36 зон зонда, ~10^139 інформаційних множин"}
  - {kind: other, url: "https://rbc.jhuapl.edu/static/newman_2016.pdf", note: "Newman et al., SPIE 2016 — стаття, що запровадила гру (бачив у пошуку)"}
  - {kind: play, url: "https://play.google.com/store/apps/details?id=edu.jhuapl.android.reconchess", note: "Android"}
  - {kind: play, url: "https://apps.apple.com/us/app/reconnaissance-blind-chess/id1631199541", note: "iOS"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=reconnaissance+blind+chess", note: "пошук; партії й доповіді"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, piece-capture, pawn-promotion, castling, move-timer, repetition-draw, ai-opponent, online-multiplayer, rating-system, lobby-window, replay, message-log, game-screen, end-screen, help-window, +sense-window-3x3, +sense-then-move-turn, +capture-king-win, +truncated-slide-capture, +capture-square-notice, +illegal-try-feedback, +voluntary-pass, +no-check-rule, +belief-set-tracking, +bot-api-arena]
proposes: ["+effect:sense", "+effect:truncate_move", "+effect:announce", "+trigger:captured", "+ui:sense-overlay", "+ui:move-result", "+feature:bot-api", "+axis:info-asymmetry", "+card:sense-window-3x3", "+card:sense-then-move-turn", "+card:truncated-slide-capture", "+card:capture-square-notice", "+card:voluntary-pass", "+card:no-check-rule", "+card:bot-api-arena"]
author: opus
date: 2026-11-09
---

# Reconnaissance Blind Chess — шахи без видимості суперника: щоходу приватно «зондуєш» вікно 3×3, ходиш наосліп і виграєш, взявши короля

## Суть
Звичайні шахові фігури й ходи, але фігур суперника не видно. Кожен хід починається з **розвідки**: гравець обирає клітину, і арбітр показує справжній вміст квадрата 3×3 навколо неї — лише йому; потім гравець ходить або пасує. Шаху й мату нема: гравця не попереджають про загрозу, мета — **взяти короля**. Створена в Johns Hopkins APL як полігон для ШІ «рішення в невизначеності» (окремо керувати військом і сенсором); RBC-боти змагались на NeurIPS.

## Поле і час
- Дошка 8×8, стандартна стартова позиція.
- Два шари знання: справжня дошка (в арбітра) і «що знає кожен» — свої фігури + результати зондів і повідомлень.
- Хід гравця = три фази: (1) дізнатись, чи взяли його фігуру (і де); (2) зонд 3×3; (3) хід або пас.
- Змістовних положень зонда 36 (центри b–g × 2–7) — за статтею про складність.
- Годинник кожного: 15 хв сумарно + 5 с після кожного ходу; бачиш лише свій час.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король | piece | сторона | хід як у шахах; взятий = поразка; рокіровка дозволена крізь і під бій |
| Ферзь, тура, слон | piece | сторона | ковзні ходи; на шляху фігура суперника → хід обрізається на ній із взяттям |
| Кінь | piece | сторона | стрибок як у шахах |
| Пішак | piece | сторона | вперед на порожню, бʼє по діагоналі; подвійний хід, обрізаний до одного; промоція (за замовчуванням ферзь) |
| Зонд | mark | клітина-центр | показує власнику справжнє вікно 3×3; суперник не знає, де |
| Арбітр | neutral | справжня дошка | приймає запит ходу, модифікує або відхиляє, розсилає приватні повідомлення |
| Годинник | resource | 15 хв + 5 с | 0 → поразка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ЯКЩО `custom: «суперник щойно взяв мою фігуру»` → ТО `message(capture_square)` — клітина, без того, чим били.
- КОЛИ `input(sense, sq)` → ТО `reveal(area_3x3(sq))` лише для себе; `custom: «суперник не дізнається, де був зонд»`.
- КОЛИ `input(move, m)` → ЯКЩО `legal(m)` на справжній дошці → ТО `move(piece, to)`, `message(taken_move)`.
- КОЛИ `input(move, slider_move)` → ЯКЩО `custom: «на шляху фігура суперника»` → ТО `custom: «хід обрізається до першої фігури суперника»`, `disappear(opp_piece)`, `message(taken_move, capture_square)` — тому, хто ходив; суперник дізнається клітину взяття.
- КОЛИ `input(move, pawn_double)` → ЯКЩО `free(first_square)` і `occupied(second_square, opp)` → ТО `move(pawn, first_square)` (модифікований хід).
- КОЛИ `input(move, m)` → ЯКЩО `custom: «пішак по діагоналі на порожню / пішак у зайняту / рокіровка крізь фігуру»` → ТО `block`, `message(«illegal»)`, `end_turn` (хід утрачено).
- КОЛИ `input(pass)` → ТО `pass_turn` (той самий результат, що й нелегальний хід).
- КОЛИ `contact(piece, opp_piece)` → ТО `disappear_b`, `message(«взяв на клітині X»)` — без типу взятої фігури.
- КОЛИ `reach(pawn, last_rank)` → ТО `transform(pawn, chosen)`; не вказано → ферзь.
- Рокіровка: `custom: «дозволена під боєм і крізь биті поля»`; виняток ковзання на рокіровку не діє.
- Шах: `custom: «про шах не повідомляють; можна лишити свого короля під боєм»`.
- КОЛИ `destroyed(king)` → ТО `win` (сторона, що взяла).
- КОЛИ `turn_end(side)` → ТО `timer(+5s)`; КОЛИ `counter(clock, <=, 0)` → ТО `lose`, повідомлення обом.
- КОЛИ `counter(turns_without_pawn_move_or_capture, =, 50)` → ТО `draw` (оголошує арбітр, вимагати не треба).
- Перемога: взяти короля або суперник без часу · Поразка: втратити короля / час · Нічия: 50 ходів без пішака і взяття.

## Керування і ввід
- Фаза зонда: вибір клітини-центру (цифрова версія — клік по дошці).
- Фаза ходу: хід своєю фігурою з урахуванням лише своїх фігур (суперника не видно) або «pass»; результат приходить одразу (взято / обрізано / нелегально).
- Боти: Python-клас `Player` у бібліотеці reconchess — `choose_sense`, `choose_move`, обробники результатів зонда й ходу; запуск локально або на сервері з рейтингом.
- Люди: браузер (/challenge — друг, бот або рейтингова партія) і мобільні застосунки.

## Вікна, меню, HUD
- `lobby-window` (/challenge): запросити друга, кинути виклик боту, рейтингова гра.
- `game-screen` (цифрова версія): свої фігури; результат останнього зонда (вікно 3×3); `message-log` — «взяли на e4», «хід обрізано до d5», «нелегально»; `player-clock` лише свій.
- `leaderboard`: рейтинги ботів і людей після ≥10 рейтингових партій.
- `help-window`: Game rules; Building a bot; Ranking protocol; Past competitions.
- `replay-window`: покроковий перегляд партії зі зондами й ходами (reconchess «Replaying games»).
- `end-screen`: хто взяв короля / час / нічия (?), повна дошка після партії (?).

## Фічі поза полем
- `online-multiplayer` + `ai-opponent-levels` (боти різних авторів на сервері), `leaderboard-online` з рейтингом.
- `replay` / `history` партій; `turn-timer` 15 хв + 5 с.
- `mod-support`-подібне: власний бот через Python-API і HTTP-API сервера (реєстрація, запрошення, ігри).
- Турніри ботів NeurIPS 2019, 2021, 2022.

## Варіації й родичі
- [Kriegspiel і Dark Chess](dark-chess-kriegspiel.md) — фігури суперника сховані, але інформацію дає суддя (Kriegspiel) або видимість за ходами (Dark Chess); RBC натомість дає **керований** приватний сенсор 3×3 і жорстко втрачає хід на нелегальній спробі.
- [Stratego](stratego.md), [Luzhanqi](luzhanqi.md), [Geister](geister.md) — приховані фігури, але відомі позиції; [Battleship](battleship.md) — запит-клітина як «постріл-зонд».
- Reconnaissance Blind Multi-Chess (2016, Newman et al.) — первісна назва/концепція (?) у статті SPIE.
- **Осі варіацій**: сенсор «нема / вікно 3×3 / промінь / кілька типів»; хто знає про зонд «ніхто / суперник»; нелегальний хід «повтор (Kriegspiel) / втрата ходу (RBC)»; мета «мат / взяти короля»; повідомлення про взяття «клітина / клітина + фігура».

## Цікавинки для курсу
- Арбітр зі справжньою дошкою й двома приватними видами + модифікація ходів (обрізане ковзання, пішак на 1) — 🥉.
- Зонд 3×3 і приватне розкриття, журнал повідомлень — 📎.
- Множина можливих дошок суперника: оновлення після зонда, взяття й власного ходу (фільтр переконань) — 🥇.
- Вибір зонда, що максимізує очікувану інформацію (ентропія по множині дошок) — 🥇.
- «Взяти короля замість мату» й прибраний шах — 🌱 (спрощує двигун, але міняє стратегію).
- Бот для рейтингового сервера (reconchess API, ~10^139 інформаційних множин — «рівня го») — 👑.

## Мапа на каталог
- Є: `piece-move-patterns` + `piece-capture` + `pawn-promotion` + `castling` ↔ шахове ядро; `move-timer` ↔ 15 хв + 5 с; `repetition-draw` ↔ правило 50 ходів; `ai-opponent` + `online-multiplayer` + `rating-system` + `lobby-window` ↔ сервер /challenge і рейтинг; `replay` ↔ перегляд партій; `message-log` ↔ повідомлення арбітра; `game-screen` / `end-screen` / `help-window`.
- **Нема** → пропозиції карток:
  - `+sense-window-3x3` «Зонд: приватне розкриття вікна N×N» · game-logic/info · 📎 · слот {size: 3}.
  - `+sense-then-move-turn` «Хід = розвідка + дія» · game-logic/turns · 🌱.
  - `+capture-king-win` (є пропозиція з Kriegspiel) — перемога взяттям короля.
  - `+truncated-slide-capture` «Ковзна фігура зупиняється на першій невидимій перешкоді й бʼє її» · entities/legality · 📎.
  - `+capture-square-notice` «Обом повідомляють клітину взяття без типу фігури» · game-logic/info · 🌱.
  - `+illegal-try-feedback` (є пропозиція з Kriegspiel) — тут зі втратою ходу.
  - `+voluntary-pass` «Пас за бажанням як інструмент блефу» · game-logic/turns · 🌱.
  - `+no-check-rule` «Шах не повідомляється й не забороняється» · entities/legality · 🌱.
  - `+belief-set-tracking` (Scotland Yard) — множина можливих дошок.
  - `+bot-api-arena` «API для ботів + рейтинговий сервер» · code/architecture · 🥈.

## Пропозиції до словників
- `+effect:sense` — приватно розкрити область лише для одного гравця (інші не знають, де).
- `+effect:truncate_move` — хід виконано лише до першої перешкоди (модифікований хід).
- `+effect:announce` — арбітр повідомляє стороні факт (клітину взяття, «нелегально»).
- `+trigger:captured` — фігуру гравця взяли (подія для того, хто втратив).
- `+ui:sense-overlay` — показ вікна останнього зонда поверх відомої дошки.
- `+ui:move-result` — рядок «запитаний хід → виконаний хід (+ взяття)».
- `+feature:bot-api` — гра відкриває API для власних ботів.
- `+axis:info-asymmetry` — що знає кожна сторона (приватні види).

## Джерела
- ⭐ [RBC: Game Rules](https://rbc.jhuapl.edu/gameRules) — зонд 3×3 перед ходом, хід або пас, повідомлення про взяття, ковзання крізь фігуру, приклади нелегальних ходів, рокіровка крізь шах, без шаху й мату, взяття короля, 15 хв + 5 с, автоматична нічия за 50 ходів.
- [RBC: головна](https://rbc.jhuapl.edu/) — опис, /challenge, рейтинг, турніри NeurIPS 2019/2021/2022, застосунки.
- [reconchess: Rules](https://reconchess.readthedocs.io/en/latest/rules.html) — три фази ходу, модифікований пішак, промоція у ферзя за замовчуванням, свій час видно, чужий — ні.
- [On the Complexity of RBC (arXiv 1811.03119)](https://ar5iv.labs.arxiv.org/html/1811.03119) — 36 зон зонда, ~10^139 інформаційних множин, пас збільшує невизначеність суперника.
- [Newman et al., 2016 (PDF)](https://rbc.jhuapl.edu/static/newman_2016.pdf) — первинна стаття (бачив у пошуку, не відкривав).
- Застосунки: [Android](https://play.google.com/store/apps/details?id=edu.jhuapl.android.reconchess), [iOS](https://apps.apple.com/us/app/reconnaissance-blind-chess/id1631199541).

## Непевне
- (?) Рік: концепт і стаття SPIE — 2016 (за пошуком), футер сайту — © 2018; у черзі стоїть 2018.
- (?) Хто ходить першим і чи білі зондують на першому ході — правила не кажуть (за шаховою традицією — білі).
- (?) Взяття на проході: правила кажуть «стандартні шахи, крім змін», окремо не згадують.
- (?) Як саме виглядає браузерний інтерфейс (перетягування чи клік, чи показують усю дошку після партії) — не бачив.
- (?) Край дошки: чи зонд по крайовій клітині показує обрізане вікно, чи центр примусово зсувається (36 зон = центри b–g × 2–7).
