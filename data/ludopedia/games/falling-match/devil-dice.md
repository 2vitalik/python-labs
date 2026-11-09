---
title: Devil Dice (XI)
slug: devil-dice
aka: [XI, "XI [sai]", サイ, Devil Dice]
family: falling-match
also: [push-slide]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: runtime
  goal: score
year: 1998
platforms: [PlayStation, PSP/PS3 (PS Classic, демо 2007)]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/XI_(ゲーム)", best: true, note: "JA: правила зникнення, ланцюг, Happy One, режими Trial/Battle/Wars/Puzzle, типи кубиків у Battle, сиквели"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Devil_Dice", note: "EN: ядро (група ≥ N граней N тоне), режими, дати, сиквели"}
  - {kind: other, url: "https://lewcid.com/lg/download/EvilDiceGuide.html", note: "Evil Dice — фанатський клон для Windows: правила котіння, ланцюг, одиниці, очки (для звірки, не оригінал)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Devil+Dice+PS1+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, keyboard-controls, orientation-state, height-levels, push-object, spawn-random-cell, chain-reaction, progress-acceleration, event-points, score-records, time-out, move-limit, sequential-levels, level-unlock, hp-damage, environment-death, simultaneous-versus, ai-opponent, mode-select, character-select, game-pause, +dice-face-group-clear, +sinking-step, +clear-all-of-kind, +shared-field-versus, +player-elimination, +steal-chain, +fill-up-lose]
proposes: ["+effect:sink", "+cond:on_top", "+role:die", "+card:dice-face-group-clear", "+card:sinking-step", "+card:clear-all-of-kind", "+card:steal-chain"]
author: opus
date: 2026-11-09
---

# Devil Dice (XI) — чортик котить кубики по полю: N сусідніх кубиків із гранню N тонуть

## Суть
Маленький чортик Акі (Aqui) бігає по полю, заставленому великими гральними кубиками: він може стояти на землі між ними або на їхніх верхівках. Стоячи на кубику й біжачи, він **перекочує** його через ребро — верхня грань змінюється, як у справжнього кубика. Група сусідніх кубиків з однаковою верхньою гранню розміром не менше за число на грані (дві двійки, три трійки… шість шісток) повільно **тоне** й зникає; поки тоне — до неї можна докотити ще кубик з тим самим числом (ланцюг) або скористатися нею як сходинкою. Ядро — просторова арифметика орієнтації кубика (Sausage Roll / Bloxorz) поверх збігу груп (Puyo).

## Поле і час
- Квадратна сітка; розмір поля в джерелах не названо (?). Два рівні висоти: земля і верх кубика (у XI JUMBO — ще другий ярус кубиків).
- Real-time: кубики **зринають** із землі в довільних місцях з часом; темп зростає з рівнем (Trial endless). Поле повністю заставлене — кінець гри.
- Зникнення не миттєве: група тоне кілька тіків (?), і весь цей час вона — частина поля зі станом `sinking` (на неї можна ступити з землі, до неї можна дочепити ланцюг).
- Battle і Wars — **одне спільне поле** на 2 або до 5 гравців (не окремі колодязі, як у Puyo).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Акі (чортик) | player | рівень: земля / верх кубика; у Wars — 99 HP | рух 4 напрямки; на кубику — котить його або переходить на сусідній; із землі — штовхає |
| Кубик звичайний | object | орієнтація (верх, напрям), стан normal / rising / sinking | перекочується під Акі (верх змінюється); штовхнутий із землі — ковзає без перекочування |
| Кубик, що зринає | object | стан rising | виростає з землі; поки росте — сходинка на верх |
| Кубик, що тоне | object | стан sinking, число групи | повільно опускається й зникає; сходинка вниз/вгору; приймає ланцюг |
| Одиниця (грань 1) | object | верх = 1 | сама по собі не зникає; приставлена до кубика, що тоне, — «Happy One» |
| Крижаний кубик (Battle) | object | — | інша поведінка при котінні/штовханні (?) |
| Камʼяний кубик (Battle) | object | важкий | лише перекочується; накотився на суперника — той гине незалежно від HP |
| Деревʼяний кубик (Puzzle?) | object | — | штовхнутий із землі перекочується, а не ковзає |
| Земля | terrain | — | клітина без кубика; звідси кубики штовхають і звідси вони зринають |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `custom: «Акі на кубику»` і `free(next_cell)` → ТО `roll(die, dir)`, `move(aqui, dir)` (Акі лишається нагорі; верх кубика стає гранню, що була з боку руху).
- КОЛИ `input(dir)` → ЯКЩО `custom: «Акі на кубику»` і `occupied(next_cell, die)` → ТО `move(aqui, dir)` — перехід на сусідній кубик без котіння.
- КОЛИ `input(dir)` → ЯКЩО `custom: «Акі на землі»` і `occupied(next_cell, die)` і `free(cell_behind_die)` → ТО `custom: «кубик ковзає без зміни верхньої грані»` (деревʼяний — `roll(die, dir)`); інакше `block`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «Акі на землі»` і `state(die_ahead, sinking)` або `state(die_ahead, rising)` → ТО `move(aqui, onto_die)` — вилізти нагору можна лише по такій «сходинці».
- КОЛИ `rng(p)` / `timer(every)` → ТО `spawn_at(rising_die, random_free_cell)`, `set_state(die, rising)`; виріс → `clear_state(die, rising)`.
- КОЛИ `pattern(group(n))` з однакових верхів → ЯКЩО `custom: «розмір групи ≥ число на грані»` і `not same(face, 1)` → ТО `set_state(group, sinking)`, `custom: «sink — кубики повільно опускаються й зникають»`, `score(n)`.
- КОЛИ `adjacent(die, sinking_group)` → ЯКЩО `same(die, group, top_face)` → ТО `set_state(die, sinking)`, `combo(+1)` — ланцюг; довші ланцюги з більших чисел дають більше очок.
- КОЛИ `adjacent(die_with_1, sinking_die)` → ТО `clear(all_ones_except_under_aqui)` — Happy One: зникають усі одиниці поля, крім тієї, на якій стоїть Акі.
- КОЛИ `custom: «кубик, що тоне, повністю зник»` → ТО `set_cell(cell, ground)`; Акі, що стояв на ньому, — на землі.
- Trial (endless/exhibition): КОЛИ `counter(cleared_dice, >=, n)` → ТО `custom: «level +1»`, `speed(spawn, +n)`, `custom: «змінюється тло»`.
- Trial: КОЛИ `custom: «усі клітини поля зайняті кубиками»` → ТО `lose`; на час — КОЛИ `timer(==, 0)` (3 хв) → ТО `game_over`, рахунок у таблицю.
- Battle: КОЛИ `after(clear)` → ТО `counter(rights, +1)`; КОЛИ `counter(rights, >=, n)` → ТО `win`; кубиком, що тоне, можна `custom: «перехопити право суперника»`.
- Battle: КОЛИ `contact(stone_die, rival)` (накочено зверху) → ТО `lose` для суперника, незалежно від HP.
- Wars: КОЛИ `after(clear)` → ТО `damage(rivals, n)`; ланцюг → `multiplier(×k)` сили атаки; КОЛИ `hp_zero(aqui)` → ТО `custom: «гравця вибито»`; останній живий — `win`; КОЛИ `timer(==, 0)` → ТО `win` того, у кого більше HP.
- Wars/Battle: КОЛИ `adjacent(own_die, rival_chain)` → ТО `custom: «steal — перехопити чужий ланцюг кубиком того ж числа»`.
- Puzzle: КОЛИ `counter(moves, ==, limit)` → ЯКЩО `count(die, >, 0)` → ТО `lose`; КОЛИ `all_gone(die)` → ТО `win`, ЯКЩО `counter(moves, <, limit)` → «Excellent».
- Перемога: Trial — рекорд; Battle — квота «прав» або камінь на суперника; Wars — останній живий; Puzzle — поле порожнє в ліміт ходів · Поразка: поле заповнене / HP 0 / ходи скінчились · Рахунок: кількість × число × довжина ланцюга (за клоном Evil Dice — (?)).

## Керування і ввід
- Хрестовина — біг Акі; той самий ввід або котить кубик, або переходить, або штовхає — залежно від того, де стоїть Акі і що попереду (контекстна дія без окремої кнопки (?)).
- Призначення кнопок (пауза, зміна камери) у джерелах не названо (?); клон Evil Dice має окрему клавішу «змінити вигляд».
- Wars — до 5 гравців одночасно через мультитап на одному полі; Battle — 2 (людина або CPU); Exhibition — кооператив двох.

## Вікна, меню, HUD
- `splash-screen` / титул (?).
- `main-menu` = `mode-select`: Trial (Endless · Time-limited 3 хв · Exhibition 2P) · Battle · Wars · Puzzle.
- `character-select`: пʼятеро братів Акі — Rosso (червоний), Azul, Verde, Momo (сестра), Huang; в оригіналі різниці в характеристиках не згадано (у JUMBO — різні швидкості й атаки).
- Battle: `match-setup` — вибір типу кубиків (звичайні / крижані / камʼяні) і, ймовірно, сторін (?).
- Puzzle: `puzzle-select` / `level-select` 100 задач рядами; завершений ряд відкриває картинку для Battle; після 100 — випадкові задачі 4×4.
- `game-screen`: поле в 3D-перспективі; HUD — `score`, `level-number`, `timer-countdown` (на час), у Wars — `hp-bar` кожного гравця, у Puzzle — `move-counter` / ліміт ходів (?).
- `end-screen`: game over з рахунком; Puzzle — «Excellent» за менше ходів, ніж ліміт.
- `pause-menu` (?).
- Переходи: титул → mode-select → (Battle/Wars) character-select → game-screen → end-screen → mode-select.

## Фічі поза полем
- `mode-endless` + `mode-time-attack` (3 хв) + `mode-coop` (Exhibition) + `mode-versus` (Battle) + багатокористувацький Wars до 5 гравців (`local-multiplayer`).
- `mode-puzzle`: 100 фіксованих задач з лімітом ходів + генеровані після 100-ї (4×4, шість кубиків за ≤20 ходів).
- `unlockables`: картинки для Battle за ряди пазлів.
- `custom-rules`: тип кубиків у Battle (normal/ice/stone).
- `ai-opponent-levels` у Battle проти CPU (рівні — (?)).

## Варіації й родичі
- **XI JUMBO** (1999, PS1, лише Японія): другий ярус кубиків, підняти й кинути кубик, кинути іншого Акі, стрибок, «резервні ланцюги»; нові кубики в Battle — залізний, магніт, вогняний, фантом, гігант; без режиму на 5.
- **XI Little** (2001, WonderSwan Color) — демейк + ритм-режим. **XI go / Bombastic** (2002, PS2) — стиль «вибух»: кубики загоряються, за таймером вибухають і поширюють вибух (6 очок — 6 клітин). **XI Coliseum** (2006, PSP) — оригінал у візуалі XI go, ad hoc до 5.
- Клон **Evil Dice** (Windows) — ті самі правила котіння, одиниць і ланцюга; рахунок `кубики × число × ланцюг`.
- Родичі: Puyo Puyo (група з порогом), Stephen's Sausage Roll / Bloxorz / Kula World (орієнтація перекочуваного тіла), Kwirk / Sokoban (штовхання з землі), Puzzle Bobble (поле, що заповнюється).
- **Осі варіацій**: поріг групи (стала 4 у Puyo / **залежить від значення** тут) · як змінюється тип плитки (свайп/обмін / **перекочування задає нову грань**) · актор (курсор / **аватар на плитках**) · зникнення (миттєве / **поступове з вікном для ланцюга**) · поле (окреме / **спільне на 5**).

## Цікавинки для курсу
- Орієнтація кубика: 6 граней, перекочування в 4 напрямки (протилежні грані в сумі 7) — 📎; чудова вправа на стан сутності.
- Поріг групи = значення на грані (flood fill з перевіркою `size ≥ face`) — 🥉.
- Поступове тонення як вікно для ланцюга + сходинка між рівнями висоти — 🥉 (стан із таймером, що впливає на рух і на збіги).
- Happy One: правило-виняток для одиниць, що чистить усе поле одного виду — 🌱.
- Контекстний ввід: одна стрілка = котити / перейти / штовхнути залежно від висоти й сусіда — 📎.
- Спільне поле на 5 гравців із HP і перехопленням чужих ланцюгів — 🥈.
- Генератор пазлів «очистити 6 кубиків за ≤20 ходів на 4×4» з перевіркою розвʼязності BFS — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `keyboard-controls` · `orientation-state` (грані кубика) · `height-levels` (земля / верх кубика) · `push-object` (із землі) · `spawn-random-cell` (кубики зринають) · `chain-reaction` · `progress-acceleration` · `event-points` · `score-records` · `time-out` (3 хв) · `move-limit` (Puzzle) · `sequential-levels` + `level-unlock` · `hp-damage` (Wars, 99 HP) · `environment-death` (камінь накотився) · `simultaneous-versus` · `ai-opponent` · `mode-select` · `character-select` · `game-pause`.
- **Нема** → пропозиції карток:
  - `+dice-face-group-clear` «Група з ≥ N однакових граней N зникає» · entities/legality · 🥉 · слот {threshold: value|const}.
  - `+sinking-step` «Плитка, що зникає поступово, — сходинка і вікно ланцюга» · entities/state · 🥉 · слот {sink_ticks}.
  - `+clear-all-of-kind` «Тригер прибирає з поля всі плитки одного виду» · entities/interact · 🌱 (Happy One; родич пірамідного каменя Cleopatra Fortune).
  - `+shared-field-versus` (вже пропонована Blockade/Lemmings) — 2–5 гравців на одному полі.
  - `+player-elimination` (вже пропонована) — Wars: останній живий.
  - `+steal-chain` «Перехопити чужий ланцюг своїм кубиком» · game-logic/opponent · 📎.
  - `+fill-up-lose` «Поразка, коли поле заповнене повністю» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+effect:sink` — сутність поступово опускається й зникає за N тіків, поки зберігаючи взаємодії (Devil Dice; вже є ×1 у Dig Dug II).
- `+cond:on_top` — аватар стоїть на обʼєкті, а не на землі (визначає, що робить той самий ввід).
- `+role:die` — гральний кубик як сутність поля з орієнтацією (вже пропонована ×3).
- `+card:dice-face-group-clear`, `+card:sinking-step`, `+card:clear-all-of-kind`, `+card:steal-chain` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia JA: XI (ゲーム)](https://ja.wikipedia.org/wiki/XI_(ゲーム)) — правила зникнення (N кубиків числа N), ланцюг, Happy One, котіння зверху / ковзання від поштовху (деревʼяний котиться), сходинка з кубика, що тоне/зринає, режими Trial/Battle/Wars/Puzzle з умовами перемоги, 99 HP, типи кубиків Battle, брати Акі, сиквели.
- [Wikipedia EN: Devil Dice](https://en.wikipedia.org/wiki/Devil_Dice) — ядро («група не менша за число очок»), режими, мультитап на 5, дати 1998, XI Jumbo / Little / Bombastic / Coliseum.
- [Evil Dice Guide](https://lewcid.com/lg/download/EvilDiceGuide.html) — фанатський клон: «котити, де нема іншого кубика; кубик попереду — перейти на нього», одиниці, ланцюг, формула очок, раунд 3 хв.
- YouTube: пошук «Devil Dice PS1 gameplay».

## Непевне
- (?) Розмір поля, швидкість тонення й зринання, кількість рівнів Trial — джерела не дають.
- (?) Чи ланцюговий кубик має знову набрати N штук, чи досить одного дотику до групи, що тоне: EN-вікі й клон кажуть «додати кубик», JA-текст можна прочитати і як «знову потрібна кількість = число».
- (?) Happy One: JA — «одиницю приставити до кубика, що тоне» (числа групи не уточнено); «якщо одиницю штовхнули з землі — зникає і штовхнутий кубик» — зміст неясний.
- (?) Поведінка крижаного кубика (ковзає до упору?) і чи деревʼяні кубики є в оригінальному Puzzle — не перевірено; «пʼять видів кубиків» згадано лише в пошуковому описі без джерела.
- (?) Формула очок оригіналу; `кубики × число × ланцюг` — з клону Evil Dice.
- (?) Батл: що таке «право» (権利) і як саме його перехоплюють кубиком, що тоне.
- (?) Вікна (титул, пауза, match-setup, HUD) — з загальної логіки PS1-ігор, не з джерел.
