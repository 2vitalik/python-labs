---
title: Reversi / Othello (Реверсі)
slug: reversi
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: territory
year: 1883
platforms: [board, Windows, arcade, web, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Reversi", best: true, note: "правила Othello vs історичний Reversi, турнірний рахунок, варіанти, розвʼязання 8×8"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Computer_Othello", note: "оцінка позиції (таблиці клітин, мобільність, патерни), пошук, програми"}
  - {kind: official, url: "https://www.worldothello.org/about/tournaments/world-othello-championship", note: "World Othello Federation: чемпіонат світу"}
  - {kind: play, url: "https://playabstractgames.com/en/reversi/", note: "браузер: AI 10 рівнів, гра з другом"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=reversi", note: "Board Game Arena — онлайн на двох"}
  - {kind: other, url: "http://radagast.se/othello/howto.html", note: "Gunnar Andersson: як написати програму для Othello (лінк зі статті Wikipedia)"}
  - {kind: other, url: "https://arxiv.org/abs/2310.19387", note: "Takizawa 2023: Othello is Solved — нічия при ідеальній грі"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=othello+reversi+rules+strategy", note: "пошук; правила й стратегія"}
stage: v1
coverage: 85
mechanics: [no-moves-left, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-random, ai-greedy, ai-minimax, cell-click, hover-highlight, legal-move-highlight, game-screen, main-menu, end-screen, help-window, settings-window, difficulty-levels, field-size-picker, theme-select, profile-stats, replay, state-as-data, +place-stone, +flank-flip, +must-capture-legality, +pass-turn, +majority-win, +move-notation]
proposes: ["+trigger:placed", "+effect:place", "+cond:flanks", "+effect:flip_line", "+ui:piece-count-bar", "+ui:last-move-highlight", "+ui:pass-button", "+feature:hint-move", "+card:place-stone", "+card:flank-flip", "+card:must-capture-legality"]
author: opus
date: 2026-11-02
---

# Reversi / Othello — постав диск так, щоб затиснути ряд чужих, і переверни їх

## Суть
Двоє гравців по черзі кладуть двобічні диски (чорний/білий) на поле 8×8. Хід легальний, лише якщо новий диск **затискає** з одного чи кількох напрямків неперервний ряд ворожих дисків між собою і вже наявним своїм — і всі затиснуті перевертаються. Фігури не ходять: поле лише заповнюється, а колір дисків постійно перемикається. У кінці перемагає той, чиїх дисків більше.

## Поле і час
- Квадратне поле 8×8 без шахового розфарбування; 64 диски на всіх. Напрямки затискання — 8 (горизонталь, вертикаль, діагоналі).
- Шар: клітина порожня / диск чорним догори / диск білим догори. Диски не рухаються й не знімаються — лише перевертаються.
- Старт Othello: 4 диски хрестом у центрі (однакові кольори на діагоналях; чорні — на північному сході й південному заході); перший ходить чорний. Історичний Reversi: порожнє поле, перші 4 ходи — у центральні клітини без перевертань.
- Покроково; на турнірах — шаховий годинник на кожного.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Диск | piece | колір догори: black/white | кладеться в порожню клітину; перевертається, коли затиснутий ворожими з двох кінців ряду |
| Порожня клітина | static | — | ціль ходу, якщо хід у неї перевертає ≥1 диск |
| Кут | zone | 4 клітини | диск у куті неможливо перевернути (стабільний) — стратегічна, не правило |
| X-/C-клітини | zone | сусіди кутів | стратегічно небезпечні (віддають кут) — лише для оцінки AI |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, cell)` → ЯКЩО `turn_of(side)` і `free(cell)` і `custom: «хоча б в одному з 8 напрямків від cell іде ≥1 ворожий диск, а за ним — свій»` → ТО `spawn_at(disc(side), cell)`; інакше `block` (хід нелегальний).
- КОЛИ `after(place)` → ТО для **кожного** такого напрямку `set_side(discs_between, side)` — перевертаються всі затиснуті ряди одночасно; новоперевернуті диски каскаду не запускають.
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` → ТО `pass_turn` (пас лише вимушений; хід є — ходити обовʼязково).
- КОЛИ `no_moves(both)` або `custom: «поле заповнене»` → ТО `game_over`.
- КОЛИ `game_over` → ТО `win` тому, в кого `count(discs)` більше; 32:32 → `draw`.
- Турнір: якщо гра скінчилась до заповнення поля — порожні клітини зараховуються переможцю; вийшов час → `lose` незалежно від дошки; рівність у турнірній таблиці — коефіцієнт Брайтвелла.
- Варіант відкриття: перші диски не обовʼязково на одній діагоналі; в історичному Reversi перші 4 ходи — розстановка центру.
- Перемога: більшість дисків · Поразка: менше / час · Рахунок: кількість дисків свого кольору (часто «чорні 40 : білі 24»).

## Керування і ввід
- Настільна: покласти диск і руками перевернути затиснуті.
- (цифрова версія) Клік по клітині; легальні клітини підсвічені (часто — крапкою), нелегальний клік ігнорується; перевертання анімоване хвилею. Пас — автоматично з повідомленням або кнопкою «Pass» (Microsoft Reversi (?)).
- Черга: чорні/білі по черзі, hotseat або проти AI.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Грати проти AI → `difficulty-select` · Гра з другом (той самий пристрій / онлайн → `lobby-window`) · Навчання → `tutorial-window` · Правила → `help-window`.
- `game-screen`: поле 8×8, `piece-count-bar` / два `score` (кількість дисків), `turn-indicator`, `legal-move-highlight`, `last-move-highlight`, `player-clock` (турнірні сайти), `move-list` у нотації (f5, d6…), `undo-button`, `hint-button`, `resign-button`.
- `confirm-dialog` / `toast`: «Нема ходів — пас».
- `end-screen`: рахунок дисків, переможець, «ще раз».
- `settings-window`: хто ходить першим, рівень AI, звук, тема дошки (`skin-select`), розмір поля (у клонах 6×6/10×10).
- `stats-window` (Play Abstract Games — статистика за рівнями AI для залогінених), `replay-window` / історія партій.
- Переходи: main-menu → game-screen → end-screen → main-menu / реванш.

## Фічі поза полем
- `ai-opponent-levels`: Play Abstract Games — 10 рівнів; Microsoft Reversi (Windows 1.0–XP) — кілька рівнів майстерності (?).
- `hotseat`, `online-multiplayer` (BGA, eOthello тощо), `turn-timer`.
- `undo`, `hint` (найкращий хід від AI), `history` + `replay`, `stats` за рівнями.
- `export-import` партій у текстовій нотації; `custom-rules` (розмір поля, анти-реверсі).
- `tutorial`, `rules-page`, `theme-select`.

## Варіації й родичі
- Reversi (Англія, 1883, Waterman/Mollett) → Othello (Японія, 1971, Горо Хасеґава; фіксований старт) — сьогодні це одна гра з різними назвами.
- Розмір поля: 4×4 і 6×6 розвʼязані (виграють білі/другий), 8×8 — нічия за препринтом 2023 (Takizawa); 10×10 «Grand Othello» (?).
- Anti-Reversi — перемагає той, у кого **менше** дисків.
- Комерційні варіанти з більшою кількістю гравців чи нестандартним полем (Rolit, Octagon) (?).
- Осі варіацій: **старт** (фіксований хрест / вільна розстановка центру) · **ціль** (більше / менше дисків) · **кінець** (поле повне / обидва без ходів) · **затискання** (ряд у 8 напрямках / лише 4 / гекс-поле) · **кольорів** (2 / 4).
- Родичі: Ataxx (перефарбування сусідів замість затискання), Go (захоплення оточенням), Gomoku (те саме поле, мета — лінія).

## Цікавинки для курсу
- Генерація легальних ходів: промінь у 8 напрямків з перевіркою «ворожі, потім свій» — 📎; класична вправа на напрямки і межі.
- Перевертання кількох рядів одним ходом (`set_side` на всі промені) — 🌱 після генерації ходів.
- Пас і кінець гри за «обидва без ходів» — 📎.
- AI: жадібний «максимум перевернутих» — 🥉 (і програє слабкій людині, бо віддає кути); таблиця вартості клітин (кути +, X-клітини −) — 🥉; minimax/альфа-бета з мобільністю — 🥇; ідеальний ендшпіль на 10–14 порожніх — 👑.
- Анімація хвилі перевертання і підсвітка легальних ходів — 🥉 за GUI-частину.
- Нотація партії (f5 d6 …) + replay — 🥈.

## Мапа на каталог
- Є: `no-moves-left` ↔ пас/кінець · `hot-seat` + `turn-enforcement` · `move-timer` · `ai-opponent` / `ai-random` / `ai-greedy` / `ai-minimax` · `cell-click` + `hover-highlight` + `legal-move-highlight` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `difficulty-levels` ↔ рівні AI · `field-size-picker` ↔ 6×6/8×8/10×10 · `theme-select` · `profile-stats` · `replay` · `state-as-data` ↔ позиція як 64 клітини.
- **Нема** → пропозиції карток:
  - `+place-stone` «Хід виставленням» · entities/legality · 🌱 — фігура не ходить, а ставиться в порожню клітину (Reversi, Hex, Go, Gomoku).
  - `+flank-flip` «Затиснути й перевернути» · entities/combat · 📎 · слот {dirs: 4|8} — ряд ворожих між новим і своїм міняє колір.
  - `+must-capture-legality` «Хід легальний лише зі взяттям» · entities/legality · 📎 — нема ефекту → хід заборонений.
  - `+pass-turn` «Пас без ходів» · game-logic/opponent · 🌱.
  - `+majority-win` «Перемога більшістю» · game-logic/win · 🌱 · слот {invert: bool} — анти-варіант.

## Пропозиції до словників
- `+trigger:placed` — фігуру виставлено на поле (хід-розміщення, на відміну від `move`).
- `+effect:place` — поставити нову фігуру в порожню клітину (так само в Go, Hive, Hex); у правилах вище — `spawn_at`.
- `+cond:flanks` — клітина затискає ряд ворожих фігур у напрямку (основа легальності Reversi).
- `+effect:flip_line` — перевернути ряд між двома точками; зводиться до `set_side`, але потребує параметра «напрямок».
- `+ui:piece-count-bar` — два лічильники/смуга співвідношення дисків; `+ui:last-move-highlight` — позначка останнього ходу; `+ui:pass-button` — явна кнопка паса.
- `+feature:hint-move` — підказка «найкращий хід» від AI в абстрактних іграх (відрізняється від `hint` у пазлах, бо розвʼязку нема).
- `+card:place-stone`, `+card:flank-flip`, `+card:must-capture-legality` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Reversi](https://en.wikipedia.org/wiki/Reversi) — правила обох версій, пас і кінець, турнірний рахунок, Anti-Reversi, розвʼязані розміри, історія.
- [Wikipedia: Computer Othello](https://en.wikipedia.org/wiki/Computer_Othello) — оцінка (таблиці клітин, мобільність, патерни), alpha-beta, Multi-ProbCut, книги дебютів; Logistello, Edax, NTest; Reversi у Windows 1.0–XP.
- [World Othello Championship](https://www.worldothello.org/about/tournaments/world-othello-championship) — офіційні турніри WOF.
- [Play Abstract Games: Reversi](https://playabstractgames.com/en/reversi/) — гра проти AI (10 рівнів), з другом, статистика.
- [Board Game Arena: Reversi](https://en.boardgamearena.com/gamepanel?game=reversi) — онлайн на двох.
- [Writing an Othello program](http://radagast.se/othello/howto.html) — гайд для програміста (лінк зі статті, сам не відкривав).
- [Othello is Solved (arXiv)](https://arxiv.org/abs/2310.19387) — 8×8 — нічия при ідеальній грі.
- YouTube: пошук «othello reversi rules strategy».

## Непевне
- (?) Інтерфейс Microsoft Reversi (рівні, кнопка Pass, підказка) — з памʼяті; Wikipedia підтверджує лише сам факт гри у Windows 1.0–XP.
- (?) Rolit, Octagon, Grand Othello 10×10 — частина статті не прочиталась; деталі не перевірені.
- (?) Розмітка легальних ходів крапками і хвиля анімації — типові для цифрових версій, не перевірено на конкретній.
