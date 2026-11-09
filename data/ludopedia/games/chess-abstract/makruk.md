---
title: Makruk (Макрук, тайські шахи)
slug: makruk
aka: [Thai chess, Тайські шахи, Mak ruk, Ouk Chatrang, Ouk, Камбоджійські шахи]
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
year: 1600
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Makruk", best: true, note: "фігури, пішаки на 3-му ряду, перетворення на 6-му, рахунок ходів у ендшпілі з таблицею лімітів, сутри, камбоджійський ук"}
  - {kind: play, url: "https://www.pychess.org/variants/makruk", note: "PyChess: правила, рахунок «честі дошки» і «честі фігур», гра онлайн; також сіттуїн, макпонг, ук чатранг"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=makruk+thai+chess+rules", note: "пошук; правила"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, piece-capture, pawn-promotion, no-move-into-check, check-stalemate, checkmate, legal-move-highlight, last-move-highlight, hot-seat, online-multiplayer, turn-enforcement, ai-opponent, ai-minimax, cell-click, drag-drop-piece, move-counter, move-notation, rule-variants, game-screen, main-menu, end-screen, help-window, mode-select, +endgame-count, +bare-king-win]
proposes: ["+trigger:count_start", "+effect:stop_count", "+ui:count-display", "+card:endgame-count", "+feature:start-count-button"]
author: opus
date: 2026-11-09
---

# Makruk — тайські шахи: короткі ферзь і слон, ранній переворот пішака і рахунок ходів до мату

## Суть
Живий нащадок чатуранги (`chaturanga-shatranj.md`), у який досі грають у Таїланді. Відмінності від `chess.md`: пішаки стартують на 3-му ряду й перетворюються вже на 6-му, ферзь (met) ходить на 1 по діагоналі, «слон» (khon) — як срібний генерал шогі. Через слабкі фігури ендшпіль затяжний, тому замість правила 50 ходів — **рахунок**: сторона, що тікає, вголос рахує ходи, і сильніша мусить заматувати до ліміту, який залежить від її матеріалу. Пат — нічия.

## Поле і час
- Дошка 8×8 (вертикалі A–H, ряди 1–8), традиційно без шахової розфарбовки (?).
- Розстановка: задній ряд як у шахах, але ферзь (met) — праворуч від короля; пішаки (bia) — на 3-му і 6-му рядах, тобто між арміями лише два порожні ряди.
- Покроково, двоє, повна інформація. Нема рокіровки, подвійного кроку пішака й en passant; зате є лічильник рахунку, який вмикає гравець.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Khun (король, «пан») | piece | royal; ×1 | 1 клітина в 8 напрямках; без рокіровки |
| Met (ферзь, «зерно») | piece | step; ×1 | 1 клітина по діагоналі |
| Khon (слон, «вельможа») | piece | step; ×2 | 1 по діагоналі або 1 прямо вперед (5 напрямків, як срібний генерал) |
| Ma (кінь) | piece | leaper (2,1); ×2 | як шаховий кінь |
| Ruea (тура, «човен») | piece | slider; ×2 | будь-яка відстань по ортогоналі |
| Bia (пішак, «каурі») | piece | напрям; ×8; старт — 3-й ряд | 1 вперед, бʼє 1 по діагоналі вперед; без подвійного кроку |
| Bia-ngai (перевернутий пішак) | piece | step | перетворений на 6-му ряду; ходить як met; ферзів може бути кілька |
| Лічильник рахунку | — | вид (дошки / фігур), значення, ліміт | вмикає слабша сторона; досягнуто ліміту — нічия |

## Правила (КОЛИ → ЯКЩО → ТО)
- Хід, взяття, черга, заборона лишати короля під ударом, мат — як у `chess.md`; нижче відмінності.
- КОЛИ `input(move(met, to))` → ЯКЩО `custom: «to — діагональний сусід»` і `legal(move)` → ТО `move(met, to)`.
- КОЛИ `input(move(khon, to))` → ЯКЩО `custom: «to — діагональний сусід або клітина прямо вперед»` і `legal(move)` → ТО `move(khon, to)`.
- КОЛИ `input(move(bia, +2))` → ТО `block`; КОЛИ `input(castle)` → ТО `block`.
- КОЛИ `reach(bia, rank_6)` → ТО `transform(bia → bia_ngai)` — обовʼязково, без вибору.
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` і `in_check(side)` → ТО `lose(side)`; ЯКЩО `no_moves(side)` і `not in_check(side)` → ТО `draw` (пат).
- **Рахунок дошки**: КОЛИ `custom: «на дошці не лишилось жодного непереведеного bia»` → ТО слабша сторона може `input(start_count)` (`+trigger:count_start`) → `counter(board_count, +1)` кожним своїм ходом від 1.
- КОЛИ `counter(board_count, ≥, 64)` → ЯКЩО `not custom: «мат»` → ТО `draw`.
- КОЛИ `input(stop_count)` (`+effect:stop_count`) → ТО `custom: «рахунок зупинено»` — слабша сторона може зупинити будь-коли; КОЛИ слабша сторона матує сильнішу, **не зупинивши** рахунок → ТО `draw`.
- **Рахунок фігур**: КОЛИ `custom: «у слабшої сторони знято останню фігуру, крім короля»` → ТО `counter(piece_count, =, n_pieces_on_board)` (обидва королі включно) і ліміт за матеріалом сильнішої (береться найменший застосовний): дві тури — 8 · одна тура — 16 · без тур, два khon — 22 · без тур і khon, два коні — 32 · без тур, один khon — 44 · без тур і khon, один кінь — 64 · лише met/bia-ngai — 64. Цей рахунок перекриває рахунок дошки; ліміт не змінюється, навіть якщо далі щось забрано.
- КОЛИ `counter(piece_count, ≥, limit)` → ЯКЩО `not custom: «мат»` → ТО `draw` (приклад: дві тури й кінь проти голого короля — 5 фігур, лишається 8 − 5 = 3 ходи).
- Перемога: мат · Нічия: пат · вичерпано рахунок · угода · Рахунок: 1 / ½ / 0.

## Керування і ввід
- Настільна: рахунок ведуть уголос, «один, два, три…» на кожен свій хід.
- (цифрова версія, PyChess) Клік-клік або drag; перетворення автоматичне; кнопка «почати/зупинити рахунок» (`+feature:start-count-button`) для сторони, що тікає; поточне значення й ліміт видно біля годинника.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu` / `mode-select`: Makruk · Ouk Chatrang · Sittuyin · Makpong · проти AI / онлайн.
- `game-screen`: дошка; два `player-clock`; `move-list`; `captured-pieces`; `last-move-highlight`; `legal-move-highlight`; індикатор рахунку «12 / 64» (`+ui:count-display`); кнопки рахунку, `resign-button`, `offer-draw-button`.
- `end-screen`: «Мат» / «Нічия: пат» / «Нічия: рахунок вичерпано».
- `help-window`: таблиця фігур і лімітів рахунку.
- Переходи: main-menu → (пейринг) game-screen → end-screen → Реванш.

## Фічі поза полем
- `online-multiplayer` і `ai-opponent-levels` (PyChess із рушієм Fairy-Stockfish (?)); `rating`.
- `rule-variants`: формальні правила проти «сутр» (неформальних ходів) і регіональні варіанти.
- `replay`, `export-import` нотації.

## Варіації й родичі
- Сутри (неформальні, у професійній грі відкинуті): Sut Khun — король, що не ходив, може піти конем на вільну клітину наступного ряду; Sut Met — пішак перед met іде вперед, і met одразу стає на 2 вперед на звільнену клітину (найпопулярніший неформальний перший хід); Sut Ma — кінь і пішак за ходом коня від нього рухаються за один хід; Takhaeng Ruea — тура(и) перевертаються і стають met.
- Ouk Chatrang (Камбоджа): якщо взять ще не було, король може першим ходом піти конем (не під шахом); met першим ходом — на 2 прямо; kar ouk — перемагає той, хто перший оголосив шах; стандартні правила і перший національний турнір — 3–4 квітня 2008; ук — серед видів спорту SEA Games 2023.
- Сіттуїн (Мʼянма): половина пішаків на 4-му ряду, гравці самі розставляють фігури (`+start-from-position` у `chaturanga-shatranj.md`).
- Makpong — варіант у PyChess (правила не бачив).
- Предок — `chaturanga-shatranj.md` (той самий короткий ферзь); khon ≈ срібний генерал `shogi.md`.
- **Осі варіацій**: ряд перетворення (6-й / останній) · правило кінця (50 ходів / рахунок з лімітом за матеріалом / оголений король) · пат (нічия / перемога) · особливі перші ходи (нема / сутри / камбоджійські).

## Цікавинки для курсу
- Файл-відмінність: перепараметризувати шаховий генератор ходів (met, khon, пішаки з 3-го ряду, перетворення на 6-му) — 🌱.
- Рахунок дошки як стан, яким керує гравець (старт/стоп, мат під рахунком = нічия), — 📎.
- Рахунок фігур: таблиця лімітів за матеріалом, «найменший застосовний», старт від кількості фігур — 🥉.
- Сутри як перемикачі `rule-variants` (особливі перші ходи з умовою «ще не ходив») — 🥉.
- AI ендшпілю під лімітом: мат за ≤N ходів — пошук з обмеженою глибиною або таблиці — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ met, khon · `piece-capture` · `pawn-promotion` ↔ на 6-му ряду, лише в bia-ngai · `no-move-into-check`, `check-stalemate`, `checkmate` · `legal-move-highlight`, `last-move-highlight` · `hot-seat`, `online-multiplayer`, `turn-enforcement` · `ai-opponent`, `ai-minimax` · `cell-click`, `drag-drop-piece` · `move-counter` ↔ лічильник рахунку · `move-notation` · `rule-variants` ↔ сутри, ук · `game-screen`, `main-menu`, `end-screen`, `help-window`, `mode-select`.
- **Нема** → пропозиції карток:
  - `+endgame-count` «Рахунок ходів до мату з лімітом за матеріалом» · game-logic/constraints · 🥉 · слоти {limits, who_counts, stop_allowed} — макрук, ук; узагальнення правила 50 ходів.
  - `+bare-king-win` (див. `chaturanga-shatranj.md`) — тут «голий король» вмикає рахунок фігур, а не перемогу.

## Пропозиції до словників
- `+trigger:count_start` — гравець оголосив початок рахунку (подія вводу, що вмикає лічильник-обмеження).
- `+effect:stop_count` — зупинити рахунок (зі зміною наслідків мату).
- `+ui:count-display` — поточне значення рахунку й ліміт біля годинника.
- `+feature:start-count-button` — кнопка рахунку для сторони, що тікає.
- `+card:endgame-count` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Makruk](https://en.wikipedia.org/wiki/Makruk) — 16 фігур кожного, пішаки на 3-му/6-му рядах, met праворуч від khun; ходи всіх фігур; перетворення на 6-му в bia-ngai; пат — нічия; рахунок без пішаків до 64 і таблиця лімітів 8/16/22/32/44/64/64 з прикладом 8 − 5 = 3; сутри; Ouk Chatrang (хід конем королем, met на 2, kar ouk, турнір 2008, SEA Games 2023).
- [PyChess: Makruk](https://www.pychess.org/variants/makruk) — «board's honor counting» (1→64, мат під рахунком = нічия) і «piece's honor counting» (старт = фігури + 1, ліміт не змінюється); сіттуїн — половина пішаків на 4-му, вільна розстановка; у меню — makpong, cambodian, shatranj.
- YouTube: пошук «makruk thai chess rules».

## Непевне
- (?) Відлік рахунку фігур: Wikipedia — «від кількості фігур на дошці», PyChess — «кількість + 1»; приклад «дві тури проти короля — від 5 до 8» (PyChess) і «8 − 5 = 3» (Wikipedia) дають різницю в один хід.
- (?) Хто саме може оголосити нічию в рахунку дошки — PyChess каже «той, хто наздоганяє, може оголосити нічию будь-коли» (дивно), Wikipedia — лише про слабшу сторону.
- (?) Неклітчаста дошка, рушій PyChess і правила Makpong — з памʼяті / не бачив.
- (?) `year: 1600` — умовно (~XVI ст. за чергою); Wikipedia каже лише, що макрук старший за сіттуїн.
