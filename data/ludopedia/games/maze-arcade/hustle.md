---
title: Hustle (Gremlin, 1977)
slug: hustle
aka: [Хасл, Gremlin Hustle, TI Hustle]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: hidden
  random: runtime
  goal: score
year: 1977
platforms: [arcade (Gremlin), TI-99/4A (Milton Bradley)]
links:
  - {kind: other, url: "https://www.arcade-history.com/game/1156/", best: true, note: "правила з мануала: ≤2 цілі, mystery −900…+900, аварія = 400 + цілі суперникові, хвости ростуть від аварій, таймер 90 ходів"}
  - {kind: other, url: "https://www.honestgamers.com/13967/arcade/hustle/review.html", note: "огляд: 90 с, штрафний лічильник в 1P, прискорення від серії, рекордів не зберігає"}
  - {kind: other, url: "https://4apedia.com/index.php/Hustle", note: "TI-99/4A: Normal / Countdown / Countup, Snakefight, Blockade, 3 рівні складності, клавіші"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gremlin_Industries", note: "Hustle — травень 1977, після Blockade і CoMotion"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Esports", note: "промотур Gremlin 1977: 19 міст, best of three, ~7 переможців із 1300"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Snake_(video_game_genre)", note: "Hustle як клон Blockade, ліцензійна версія для TI-99/4A"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hustle+gremlin+1977+arcade+gameplay", note: "пошук; аркада"}
stage: v1
coverage: 70
mechanics: [move-auto, move-4dir, body-queue, self-collision, spawn-random-cell, timed-despawn, item-pickup, event-points, progress-acceleration, time-out, rule-variants, difficulty-levels, ai-opponent, keyboard-controls, +shared-field-versus, +operator-settings, +crash-grows-tail, +mystery-value-pickup, +decaying-target-value, +crash-transfers-board, +move-tick-timer, +free-game-threshold]
proposes: ["+trigger:expired", "+ui:penalty-meter", "+card:crash-grows-tail", "+card:mystery-value-pickup", "+card:decaying-target-value", "+card:crash-transfers-board", "+card:move-tick-timer"]
author: opus
date: 2026-11-09
---

# Hustle — Blockade з цілями: змійки ганяються за коробками з очками, а від аварії хвіст не зникає, а росте

## Суть
Наступник Blockade від Gremlin: один або двоє гравців керують стрілкою з хвостом сталої довжини, що рухається за головою. На полі зʼявляються коробки-цілі з очками (не більше двох одночасно) і зникають, якщо їх не встигли взяти. Головна інверсія відносно класичної змійки: хвіст росте не від «їжі», а від аварії — це штраф, що звужує поле. Аварія ще й віддає суперникові 400 очок плюс усе, що зараз лежить на полі.

## Поле і час
- Клітинне поле в рамці; одна арена на весь екран, хвости обох гравців — перешкоди.
- Real-time; темп зростає з кожною взятою ціллю, максимум — після 10 цілей поспіль без аварії; аварія скидає темп до початкового.
- Таймер гри — 90 «одиниць», що спливають із кроками змійки, а не з секундами; під час нарахування очок стоїть; гра триває ≈ 2 хв (перемичка оператора скорочує до ≈ 1,5 хв).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Стрілка з хвостом гравця 1 / 2 | player | довжина хвоста, напрям | щотік крок, хвіст тягнеться за головою; ріст лише після аварії |
| Хвіст | static | власник | перешкода для обох гравців, рухається разом з головою |
| Рамка поля | static | — | дотик = аварія |
| Ціль-коробка | pickup | значення > 0, час життя | зʼявляється у випадковому місці; не взяли вчасно — зникає без очок |
| Mystery-коробка «???» | pickup | −900…+900 | значення відкривається при взятті |
| Лічильник штрафу (1P) | — | сума | наприкінці віднімається від рахунку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(snake, dir)` (тіло — черга клітин), `counter(timer, -1)`.
- КОЛИ `input(dir)` → ТО `face(snake, dir)` (4 напрямки).
- КОЛИ `rng(p)` → ЯКЩО `count(target, <, 2)` → ТО `spawn_at(target, random)` зі значенням і часом життя.
- КОЛИ `custom: «час життя цілі вийшов»` (`+trigger:expired`) → ТО `disappear_a`, без очок.
- КОЛИ `contact(snake, target)` → ТО `score(value)`, `disappear_b`, `speed(snake, +1)`.
- КОЛИ `contact(snake, mystery)` → ТО `reveal(value)`, `score(value)` (може бути мінус).
- КОЛИ `counter(targets_in_row, ==, 10)` → ТО `custom: «темп більше не росте»`.
- КОЛИ `contact(snake, edge|tail)` → ЯКЩО `mode(two_player)` → ТО `score(+400)` суперникові, `custom: «плюс сума всіх цілей на полі, mystery — як додатні»`.
- КОЛИ `contact(snake, edge|tail)` → ЯКЩО `mode(one_player)` → ТО `counter(penalty, +400)`, `custom: «плюс сума цілей на полі»`.
- КОЛИ `after(crash)` → ТО `grow(snake_1, n)`, `grow(snake_2, n)`, `speed(snake, reset)`.
- КОЛИ `custom: «нарахування очок»` → ТО `timer(stop)` до кінця анімації.
- КОЛИ `counter(timer, ==, 0)` → ТО `game_over`; 2P — `win` у кого більше; 1P — `score(-penalty)`.
- КОЛИ `counter(score, >=, threshold)` → ЯКЩО `mode(one_player) and custom: «оператор увімкнув free game»` → ТО `custom: «безкоштовна гра»` (не двічі поспіль).
- TI Countdown: КОЛИ `timer(1s)` → ЯКЩО `mode(countdown)` → ТО `set_value(target, value - 100)`; від 900 до 100, далі зникає.
- TI Countup: КОЛИ `timer(1s)` → ЯКЩО `mode(countup)` → ТО `set_value(target, value + 100)`; від 100 до 900, далі зникає.
- TI Snakefight: КОЛИ `contact(snake, target)` → ЯКЩО `mode(snakefight)` → ТО `custom: «очки цілі — суперникові»`.
- TI Blockade: КОЛИ `contact(snake, edge|tail)` → ЯКЩО `mode(blockade)` → ТО `score(+100)` суперникові, `custom: «поле очищається, відлік, новий раунд швидше»`.
- Перемога: більше очок, коли таймер дійшов до 0 · Поразка: — (аварія = штраф, не смерть) · Рахунок: цілі, 400 за аварію суперника, штраф в 1P.

## Керування і ввід
- Аркада: 4-ходовий джойстик на гравця, кнопки ONE PLAYER START / TWO PLAYER START; одиночні органи керування — праворуч на панелі.
- TI-99/4A: гравець 1 — E/S/D/X, гравець 2 — I/J/K/M або Wired Remote Controllers; без діагоналей; напрям тримається до нового натискання.
- Обидва гравці грають одночасно на одному полі.

## Вікна, меню, HUD
- `game-screen`: поле, рахунок обох гравців, таймер; в 1P — `+ui:penalty-meter`.
- `attract-demo` — режим очікування автомата (?).
- TI: `main-menu` (список «Players» → режим → рівень складності), `help-window` (клавіша AID), BACK — назад у списку; після гри REDO (ті самі опції), BEGIN — до списку гравців, QUIT — титульний екран.
- `end-screen` з підсумком (?).

## Фічі поза полем
- `operator-settings`: перемичка «коротка гра», free game на 11 000 / 13 000 / 15 000 / 17 000 очок (з заводу вимкнено).
- Рекордів аркада не зберігає.
- TI: 1P проти компʼютера (біла змійка), 2P; режими Hustle (Normal / Countdown / Countup), Snakefight (ті самі 3), Blockade; рівні Novice / Amateur / Hustler — відлік перед грою, стартова й максимальна швидкість, приріст хвоста за аварію, розум CPU.
- Промо 1977: «Gremlin Girls» обʼїхали міста США, грали best of three на гроші — ранній кіберспорт.

## Варіації й родичі
- `blockade` — предок (слід вічний, мета — ліміт аварій); Hustle робить хвіст сталим і додає цілі.
- `snake` — пізніша класика, де хвіст росте від їжі; Hustle — проміжна ланка (хвіст рухається, але ріст — покарання).
- `surround` — паралельна домашня гілка Blockade (Atari 2600).
- **Осі варіацій:** ріст хвоста від їжі / від аварії / ніколи · ціль стала / спадає / зростає / mystery · аварія: кінець раунду / штраф / очки суперникові · таймер у секундах / у кроках.

## Цікавинки для курсу
- Ціль із часом життя і значенням, що змінюється щосекунди (Countdown/Countup) — 🌱.
- Mystery-коробка з прихованим знаком — 🌱: ризик vs винагорода.
- Аварія віддає суперникові «банк» поля + 400 — 📎: очки як перерозподіл, не лише нарахування.
- Ріст хвоста як штраф за аварію — 🌱: інверсія звичного правила Snake.
- Таймер у кроках, що стоїть під час нарахування — 📎: час гри = кількість тіків.
- Темп від серії, скидання при аварії — 🌱.

## Мапа на каталог
- Є: `move-auto` · `move-4dir` · `body-queue` · `self-collision` · `spawn-random-cell` · `timed-despawn` · `item-pickup` · `event-points` · `progress-acceleration` · `time-out` · `rule-variants`, `difficulty-levels`, `ai-opponent`, `keyboard-controls` (TI).
- **Нема** → пропозиції карток:
  - `+shared-field-versus`, `+operator-settings` — уже запропоновані в `blockade`; підтверджую.
  - `+crash-grows-tail` «Аварія подовжує хвіст» · entities/state · 🌱.
  - `+mystery-value-pickup` «Предмет з прихованим значенням ±» · entities/interact · 🌱 · слот {range: −900…900}.
  - `+decaying-target-value` «Значення цілі спадає/росте з часом» · game-logic/score · 🌱 · слот {step: 100}.
  - `+crash-transfers-board` «Аварія віддає суперникові очки поля» · game-logic/score · 📎.
  - `+move-tick-timer` «Таймер гри в кроках, не в секундах» · game-logic/lose · 🌱.
  - `+free-game-threshold` «Безкоштовна гра за поріг очок» · game-logic/score · 🌱.

## Пропозиції до словників
- `+trigger:expired` — сутність вичерпала час життя (ціль Hustle, тимчасові предмети); зараз — `custom` або `timer` на кожну сутність.
- `+ui:penalty-meter` — лічильник штрафу, що віднімається наприкінці.
- `+card:crash-grows-tail`, `+card:mystery-value-pickup`, `+card:decaying-target-value`, `+card:crash-transfers-board`, `+card:move-tick-timer` — див. «Мапу на каталог».

## Джерела
- ⭐ [arcade-history: Hustle](https://www.arcade-history.com/game/1156/) — правила з мануала: цілі, mystery, 400 + цілі, ріст хвостів, темп, таймер 90, free game, перемичка.
- [HonestGamers: Hustle](https://www.honestgamers.com/13967/arcade/hustle/review.html) — 90 с, штрафний лічильник, ≈400 штрафу без цілей, без рекордів.
- [4apedia: Hustle (TI-99/4A)](https://4apedia.com/index.php/Hustle) — режими, значення Countdown/Countup, Snakefight, Blockade, рівні, клавіші.
- [Wikipedia: Gremlin Industries](https://en.wikipedia.org/wiki/Gremlin_Industries) — дата травень 1977.
- [Wikipedia: Esports](https://en.wikipedia.org/wiki/Esports) — промотур 1977.
- [Wikipedia: Snake (video game genre)](https://en.wikipedia.org/wiki/Snake_(video_game_genre)) — клон Blockade, порт для TI-99/4A.

## Непевне
- (?) Опис у черзі («росте від їжі») не підтвердився: усі три джерела кажуть, що хвіст росте від аварій.
- (?) На скільки клітин росте хвіст за аварію в аркаді; чи змійки після аварії ставляться на старт.
- (?) Аркада на «залізі» Blockade (переробка непроданих автоматів) — лише з пошукової виписки.
- (?) Snakefight: «врізатися в суперника дає тобі всі очки на полі» — формулювання 4apedia неоднозначне.
- (?) Рік порту TI: Wikipedia — 1980, 4apedia — 1981.
- (?) Промотур: 19 міст (Wikipedia) чи 12 (інше джерело з пошуку).
