---
title: Sumoku
slug: sumoku
aka: [Сумоку, Speed Sumoku, Spot Sumoku, Team Sumoku, Solo Sumoku]
family: word-number
also: [board-digital]
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: score
year: 2010
platforms: [board]
links:
  - {kind: other, url: "https://ultraboardgames.com/sumoku/game-rules.php", best: true, note: "правила базової гри: 96 плиток, 6 кольорів, кубик 3/4/5, лінії 2–6, колір не повторюється, 6 = 9, очки, бонус 6 кольорів, кінець і штраф"}
  - {kind: other, url: "https://ultraboardgames.com/sumoku/variants.php", note: "Speed, Spot, Team, Solo Sumoku"}
  - {kind: other, url: "https://rulespal.com/sumoku/rulebook", note: "те саме + «extra challenge»: ключ = сума двох кидків"}
  - {kind: official, url: "https://blueorangegames.com/games/sumoku", note: "Blue Orange Games #00360: 1–8 гравців, 9+, 10–30 хв, 5 способів гри, нагороди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=sumoku+board+game+how+to+play", note: "пошук; правила й партія"}
stage: v1
coverage: 65
mechanics: [hot-seat, turn-enforcement, event-points, leftover-penalty, markup-validity, completion-detection, simultaneous-versus, mode-select, game-screen, end-screen, help-window, +hand-of-tiles, +tile-bag-draw, +connected-placement, +line-placement, +cross-word-scoring, +tile-exchange, +sum-multiple-line, +no-repeat-in-line, +dual-value-tile, +bonus-turn-full-set, +key-number-die, +spot-the-set]
proposes: ["+cond:sum_multiple", "+cond:line_length", "+trigger:claim", "+effect:refill_hand", "+ui:key-number", "+ui:line-sum-preview", "+feature:mode-speed-race", "+card:sum-multiple-line", "+card:no-repeat-in-line", "+card:dual-value-tile", "+card:bonus-turn-full-set", "+card:key-number-die", "+card:spot-the-set"]
author: opus
date: 2026-11-09
---

# Sumoku — числовий Scrabble: склади кросворд із кольорових плиток, де сума кожного ряду кратна ключовому числу

## Суть
Гравці викладають числові плитки зі своєї руки в спільну кросвордоподібну структуру в центрі столу. Кожен ряд і стовпець — суцільна лінія з 2–6 плиток; його сума має ділитися на ключове число (3, 4 або 5), яке один раз кидають кубиком на всю гру, а колір у лінії не може повторюватись. Очки = сума плиток лінії, яку ти створив чи продовжив; повна лінія з усіх 6 кольорів дає ще один хід. Ядро — Scrabble без словника: «легальне слово» замінено арифметичною умовою подільності плюс кольоровим обмеженням як у судоку.

## Поле і час
- Поле без дошки: плитки лягають на стіл у квадратну сітку, що росте від першої лінії (необмежене поле, межі нема).
- Лінія = максимальний суцільний відрізок плиток у рядку чи стовпці, довжина 2–6.
- Рука — 8 плиток кожного гравця, лежать **лицем догори** (інформація відкрита); мішок — закритий запас.
- Хід — покроковий, по колу; ключове число фіксоване на всю гру.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Числова плитка | tile | число, колір (1 з 6) | кладеться з руки в сітку; входить у ряд і стовпець одночасно |
| Плитка «6» | tile | 6 або 9 на вибір | гравець вирішує значення при викладанні |
| Кубик ключа | object | грані 3 / 4 / 5 | кидається раз на гру; дає ключове число |
| Ключове число | static | 3, 4 або 5 (опція: сума двох кидків) | дільник для суми кожної лінії |
| Лінія | zone | 2–6 плиток, сума, набір кольорів | легальна, якщо сума кратна ключу і кольори різні |
| Рука | supply | 8 плиток, лицем догори | після ходу добирається до 8 |
| Мішок | supply | 96 плиток на старті | джерело добору; порожній — тригер кінця |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `give(each player, 8 tiles)`, `custom: «плитки руки лицем догори»`.
- КОЛИ `game_start` → ЯКЩО `custom: «у гравця найменша сума руки»` → ТО `custom: «він кидає кубик: ключове число 3, 4 або 5 на всю гру»` і ходить першим.
- Перший хід: КОЛИ `input(place line)` → ЯКЩО `custom: «сума лінії кратна ключовому числу»` → ТО `place(tiles)`, `score(sum)`.
- КОЛИ `input(place tiles)` → ЯКЩО `connected(all tiles)` і `custom: «кожна зачеплена лінія суцільна, 2–6 плиток»` і `custom: «сума кожної зачепленої лінії кратна ключовому числу»` і `unique(line colors)` → ТО `place(tiles)`; інакше `block`.
- Легальні типи ходу: `custom: «продовжити наявну лінію / створити нову, приєднану до наявних / і те, і те одним ходом»`.
- Числа можуть повторюватися в лінії: `custom: «обмеження лише на колір»` (крім Solo).
- КОЛИ `input(place tile 6)` → ТО `choose(6 | 9)`, `set_value(tile, choice)`.
- Очки: КОЛИ `after(place)` → ТО `score(sum of created/extended line)`; ЯКЩО `custom: «хід утворив чи завершив і ряд, і стовпець»` → ТО `score(both sums)`.
- Бонус: КОЛИ `after(place)` → ЯКЩО `custom: «утворено або завершено лінію з усіх 6 кольорів»` → ТО `extra_move` без добору; потім `custom: «скласти обидві суми й добрати до 8»`.
- КОЛИ `turn_end(player)` → ТО `give(player, as many tiles as played)` з мішка.
- КОЛИ `no_moves(all)` → ЯКЩО `custom: «мішок порожній»` → ТО `game_over`, `score(−sum of tiles left in hand)` кожному.
- Перемога: найбільше очок після штрафу · Поразка: менше очок · Рахунок: сума плиток ліній, які гравець створив чи продовжив, мінус залишок у руці.
- Опція «extra challenge»: `custom: «ключ = сума двох кидків кубика»`.
- Speed Sumoku: КОЛИ `input(call "Sumoku!")` → ЯКЩО `custom: «усі 10+ плиток гравця в одній структурі, кожна лінія кратна ключу, кольори не повторюються»` → ТО `win` раунду; інакше `custom: «"Tubadoku": гравець вибуває з раунду, його плитки в запас, решта бере по 2»`.
- Speed: КОЛИ `input(swap)` → ТО `take(player, 1 tile)`, `give(player, 2 tiles)` («Swapoku», скільки завгодно разів).
- Spot Sumoku: КОЛИ `input(shout sum)` → ЯКЩО `custom: «4 плитки з 10 відкритих мають суму, кратну ключу»` → ТО `give(player, 4 tiles)`, `spawn(4 new open tiles)`; інакше `custom: «повернути 4 своїх плитки в запас»`.

## Керування і ввід
- Настільна гра: гравець викладає кілька плиток з руки за хід у лінії, оголошує суми й рахує очки; суперники перевіряють.
- Speed/Spot — без черги: усі будують/шукають одночасно, перемога — хто перший вигукне («Sumo-go!» — старт, «Sumoku!» — фініш).
- Цифрова версія: drag плитки з руки на сітку, клік по «6» — перемкнути на 9, кнопка «завершити хід» з підрахунком сум.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): спільна сітка, рука гравця (`pocket`), `key-number` (ключове число), `line-sum-preview` (сума лінії і чи кратна), `conflict-highlight` для повтору кольору, `score` усіх гравців, лічильник плиток у мішку.
- `mode-select`: Sumoku / Speed / Spot / Team / Solo.
- `end-screen`: рахунок мінус залишки рук.
- `help-window`: правила ліній, кольорів, плитки 6/9.

## Фічі поза полем
- Пʼять способів гри (`mode-select`); `custom-rules` — «extra challenge» з двома кидками.
- `mode-versus` (базова, 2–5), реал-тайм `simultaneous-versus` (Speed, 2–8), командна гонка Team (2–4 команди однаковими наборами 48 / 32 / 24 плитки), `mode-zen` Solo (1 гравець або група дітей, з таймером за бажанням).
- Матч у Speed: до 2 перемог поспіль або 3 загалом; переможець раунду кидає кубик наступного.

## Варіації й родичі
### Speed Sumoku (2–8)
- По 10 плиток кожному; кожен будує **власну** структуру одночасно; обмін 1 → 2; перший правильний «Sumoku!» виграє раунд, помилка («Tubadoku») — вибування з раунду.
### Spot Sumoku (2–8)
- 10 відкритих плиток у центрі; хто перший знайде 4 плитки з сумою, кратною ключу, — забирає їх; ціль — 16 плиток (2–4 гравці) або 12 (5–8); хибний вигук — мінус 4 плитки, з менше ніж 4 — пропуск раунду.
### Team Sumoku (2–4 команди)
- Кожна команда — 48 / 32 / 24 плитки; перемагає, хто перший правильно використає всі.
### Solo Sumoku
- 16 плиток, потім по 10; **і кольори, і числа** не повторюються в лінії; мета — використати всі 96.
- Родичі корпусу: [scrabble.md](scrabble.md) і [mathable.md](mathable.md) (рука, мішок, лінії, крос-очки), [bananagrams.md](bananagrams.md) (Speed — та сама гонка власних структур), [crossmath.md](crossmath.md), [cross-figure.md](cross-figure.md); кольорове обмеження — як рядок судоку (`pencil-logic/sudoku.md`).
- **Осі варіацій:** умова лінії (слово / рівняння / сума кратна k / сума = n) · обмеження в лінії (нема / колір / колір і число) · поле (спільне / власне в кожного) · темп (черга / одночасно) · кінець (мішок порожній / хтось використав усе / квота плиток).

## Цікавинки для курсу
- Валідатор ходу: знайти всі зачеплені лінії (максимальні відрізки), перевірити довжину 2–6, суму mod k і різні кольори — 📎.
- Плитка-джокер «6 або 9»: перебір значень при валідації — 🌱.
- Підрахунок очок ряду і стовпця, бонус-хід за 6 кольорів, штраф залишком — 🌱.
- Генератор ходів AI: пошук розміщень з руки, де всі лінії кратні k (комбінаторика підмножин руки × позиції) — 🥈.
- Spot-режим: знайти 4 з 10 із сумою mod k = 0 (C(10,4) = 210 підмножин) і реакція «хто перший» — 🥉.
- Speed-режим: одночасна гонка, перевірка структури суперником і вибування за помилку — 📎.

## Мапа на каталог
- Є: `hot-seat` + `turn-enforcement` ↔ хід по колу · `event-points` ↔ сума лінії · `leftover-penalty` ↔ мінус залишок руки · `markup-validity` ↔ легальність ліній · `completion-detection` ↔ Speed «Sumoku!» · `simultaneous-versus` ↔ Speed (кожен своє поле) · `mode-select` · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+hand-of-tiles`, `+tile-bag-draw`, `+connected-placement`, `+line-placement`, `+cross-word-scoring`, `+tile-exchange` — є в корпусі (Scrabble, Mathable, board-digital).
  - `+sum-multiple-line` «Сума лінії кратна ключовому числу» · game-logic/constraints · 🌱 · слоти {key: 3..10}.
  - `+no-repeat-in-line` «Атрибут не повторюється в лінії» · game-logic/constraints · 🌱 · слоти {attr: color|number}.
  - `+dual-value-tile` «Плитка з двома значеннями на вибір (6/9)» · entities/state · 🌱.
  - `+bonus-turn-full-set` «Повний набір атрибутів у лінії → ще хід» · game-logic/score · 🌱.
  - `+key-number-die` «Параметр правил кидається раз на гру» · game-logic/random · 🌱.
  - `+spot-the-set` «Хто перший знайде підмножину за умовою» · game-logic/opponent · 🥉.

## Пропозиції до словників
- `+cond:sum_multiple` — сума групи кратна k (є `sum` = n, але не «кратна»).
- `+cond:line_length` — довжина лінії в межах [a, b].
- `+trigger:claim` — гравець оголошує готовність/знахідку («Sumoku!», «Bingo!»), далі перевірка.
- `+effect:refill_hand` — добрати руку до N (тут — стільки, скільки викладено).
- `+ui:key-number` — поточне ключове число; `+ui:line-sum-preview` — сума лінії з позначкою кратності.
- `+feature:mode-speed-race` — режим одночасної гонки з перевіркою й вибуванням.
- `+card:sum-multiple-line`, `+card:no-repeat-in-line`, `+card:dual-value-tile`, `+card:bonus-turn-full-set`, `+card:key-number-die`, `+card:spot-the-set`.

## Джерела
- ⭐ [UltraBoardGames: Sumoku rules](https://ultraboardgames.com/sumoku/game-rules.php) — компоненти (96 плиток, 6 кольорів, кубик), розстановка, лінії 2–6, колір не повторюється, 6/9, типи ходу, очки, бонус 6 кольорів, добір, кінець зі штрафом.
- [UltraBoardGames: Sumoku variants](https://ultraboardgames.com/sumoku/variants.php) — Speed (10 плиток, обмін 1→2, «Sumoku!»/«Tubadoku», 2 поспіль або 3), Spot (4 з 10, 16/12 плиток), Team (48/32/24), Solo (16 + по 10, без повтору чисел).
- [RulesPal: Sumoku rulebook](https://rulespal.com/sumoku/rulebook) — те саме + «extra challenge» з двома кидками.
- [Blue Orange Games: Sumoku](https://blueorangegames.com/games/sumoku) — 1–8 гравців, 9+, 10–30 хв, 5 способів гри, нагороди (Oppenheim Gold Seal, Parents' Choice Gold).
- YouTube: пошук «sumoku board game how to play».

## Непевне
- (?) Числа на плитках (діапазон, скільки плиток кожного числа й кольору) — жодне з відкритих джерел не дає; лише «96 плиток, 6 кольорів».
- (?) Рік 2010 — з черги; сторінка Blue Orange показує лише копірайт сайту «2010–2020»; автор гри не названий.
- (?) Пас і обмін плиток у базовій грі не описані; що робить гравець без легального ходу до кінця мішка — невідомо.
- (?) Чи всі плитки одного ходу мають лягти в одну лінію (як у Scrabble) — правила кажуть лише про три типи ходу.
- (?) Вікна — «(цифрова версія)»: офіційної цифрової Sumoku не знайдено.
