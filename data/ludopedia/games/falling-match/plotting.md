---
title: Plotting (Flipull)
slug: plotting
aka: [Flipull, フリップル, Furippuru]
family: falling-match
also: [thinky]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: coop
  info: full
  random: none
  goal: state
year: 1989
platforms: [arcade, Famicom, Game Boy, Amiga, C64, Atari ST, ZX Spectrum, Amstrad CPC, PS2, Xbox, PC, Switch, PS4]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/フリップル", best: true, note: "JA: повні правила — кидок, відскок від стіни/стелі/труб, обмін блоком, спецблок, ціль-залишок, відмінності портів, кількість стадій"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Plotting_(video_game)", note: "EN: назви, дати, порти, перевидання (Taito Legends, Arcade Archives)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=plotting+flipull+taito+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [keyboard-controls, projectile-shot, gravity-fall, line-match-clear, event-points, time-bonus, time-out, sequential-levels, satisfy-constraints, no-moves-left, game-over-continue, score-records, end-screen, attract-demo, +throw-swap-return, +wall-bounce-shot, +wildcard-tile, +leftover-quota, +pass-through-pipe, +stun-on-return, +move-limit-puzzle]
proposes: ["+effect:return_to_hand", "+ui:held-block", "+ui:quota-target", "+card:throw-swap-return", "+card:leftover-quota", "+card:pass-through-pipe"]
author: opus
date: 2026-11-09
---

# Plotting (Flipull) — кидаєш блок у купу: він вибиває однакові й повертає тобі перший інший

## Суть
Персонаж стоїть праворуч від купи символьних блоків і рухається лише вгору-вниз. Він тримає **один** блок і кидає його горизонтально: блок вибиває всі однакові з собою підряд, а впершись у **інший** блок — міняється з ним місцями, і цей інший повертається гравцеві як новий «снаряд». Стіни, стеля й труби відбивають кидок униз, тож можна бити купу й згори. Мета стадії — залишити на полі не більше блоків, ніж задано; якщо жодного влучного кидка не лишилось — промах.

## Поле і час
- Бічний вид: купа блоків у куті поля, над нею стеля, ліворуч стіна; на деяких стадіях — труби й виступи стелі, через які частина стовпців недосяжна.
- Персонаж — на драбині/стовпці праворуч від купи; висота кидка = рядок персонажа.
- Траєкторія: горизонтально → упор у стіну/стелю/трубу збоку → вертикально вниз. Через трубу блок проходить лише вертикально.
- Real-time з таймером стадії; сам кидок дискретний. Блоки над вибитими осідають (гравітація вниз).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж | player | рядок; блок у руках | рух ↑/↓; кидає блок, ловить блок, що повертається |
| Блок-символ | tile | тип (форма/знак) | вибивається однаковим блоком; інший — обмінюється з кинутим |
| Спецблок (джокер) | supply | запас = «життя» | на старті стадії і після промаху в руках; вибиває будь-який блок |
| Стіна / стеля | static | — | кидок, що вперся збоку, падає вниз |
| Труба | static | вертикальний прохід | блок проходить лише згори вниз, збоку — відбиває вниз |
| Підлога | static | — | блок, що долетів до неї, повертається гравцеві тим самим |
| Синій блок з маркою Taito | tile | аркада | прихований бонус: +1 спецблок за умови (див. правила) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(up|down)` → ТО `move(player, row±1)`.
- КОЛИ `input(fire)` → ТО `throw(held, left)` — блок летить горизонтально по рядку персонажа.
- КОЛИ `contact(shot, wall|ceiling|pipe_side)` → ТО `fall(shot)` — рух униз по стовпцю.
- КОЛИ `contact(shot, block)` → ЯКЩО `same(shot, block, type)` → ТО `clear(block)`, `score(n)`, кидок летить далі; кілька однакових підряд вибиваються одним кидком з бонусом за кількість.
- КОЛИ `contact(shot, block)` → ЯКЩО `not same(shot, block, type)` і перед цим щось вибито → ТО `swap(shot, block)`, `custom: «return_to_hand — вибитий інший блок летить до гравця й стає новим снарядом»`.
- КОЛИ `contact(shot, block)` → ЯКЩО `not same(shot, block, type)` і нічого не вибито → ТО `custom: «return_to_hand — кинутий блок повертається тим самим»`.
- КОЛИ `contact(shot, floor)` → ТО `custom: «return_to_hand — повертається тим самим»`.
- КОЛИ `after(clear)` → ТО `fall(blocks_above)`.
- КОЛИ `custom: «блок повернувся в руки»` → ЯКЩО `mode(famicom|gameboy)` → ТО `stun(player, ≈2 s)` — персонаж трясеться і завмирає.
- КОЛИ `level_start` або після промаху → ТО `give(player, special_block)` у руки; спецблок `same(*, any)` — вибиває будь-який тип; кожен промах витрачає один.
- КОЛИ `no_moves(player)` (з жодного рядка не вибити нічого) → ТО `custom: «промах — −1 спецблок»`; ЯКЩО `count(special, =, 0)` → ТО `game_over`.
- КОЛИ `timer(stage_limit)` вичерпано → ТО `custom: «−1 спецблок»`; ЯКЩО спецблоків нема → ТО `game_over`.
- КОЛИ `counter(blocks_left, ≤, quota)` → ЯКЩО `mode(arcade)` → ТО `win` стадії одразу, `score(bonus за малий залишок)`, `next_level`.
- КОЛИ `counter(blocks_left, ≤, quota)` → ЯКЩО `mode(famicom|gameboy)` → ТО гра триває, стадія закінчується на `no_moves` або вичерпаному часі з `score(bonus)`.
- КОЛИ `win` стадії → ЯКЩО `timer(≤, 10 s)` і в руках синій Taito-блок (аркада) → ТО `sound(secret)`, `give(player, special_block)`.
- КОЛИ стадія 0 (аркада, тренувальна) → ТО промах або вичерпаний час теж зараховуються як проходження.
- ADVANCE (Famicom): фіксовані розкладки, ліміт ходів, без таймера; КОЛИ `no_moves` → ТО `game_over`; continue без ліміту.
- Перемога: пройти всі стадії (аркада 0–59) · Поразка: промах або час без спецблоків · Рахунок: очки за вибиті блоки (більше за серію), бонус за малий залишок.

## Керування і ввід
- Важіль лише вгору/вниз — вибір рядка кидка; одна кнопка — кинути.
- Гравець читає геометрію: прямий удар по рядку, «навісний» удар через стелю/трубу згори вниз, і **який блок повернеться** — це план наступного ходу.

## Вікна, меню, HUD
- `attract-demo` / `splash-screen` → вибір 1P/2P (аркада).
- `game-screen`: купа блоків, персонаж, блок у руках (`+ui:held-block`), `remaining-counter` блоків і `+ui:quota-target` (скільки треба залишити), `timer-countdown`, запас спецблоків, `score`, `hi-score`, номер стадії (`level-number`).
- `end-screen` стадії з бонусом за залишок; `game-over-continue` (Famicom і Game Boy — 3 continue).
- `mode-select` (Famicom): звичайна гра / ADVANCE.
- Ending після останньої стадії.
- Переходи: title → game-screen → бонус стадії → наступна; промах без спецблоків → continue / game over.

## Фічі поза полем
- `levels-sequential`: аркада — 60 стадій (0–59, нульова тренувальна); Famicom — 50, далі повтор до 250 зі спільним ендінгом; Game Boy — 32, з 33-ї розкладки повторюються.
- ADVANCE-режим (Famicom): 50 пазлових стадій із лімітом ходів, без часу — `mode-puzzle`.
- 2 гравці — у JA-інфобоксі «кооператив» (?); `continue` (3 на FC/GB).
- Перевидання: Taito Legends (2005, PS2/Xbox/PC), Arcade Archives (2022, Switch/PS4) з онлайн-рейтингом (?).

## Варіації й родичі
- Графічно і частково механікою близька до [puzznic](puzznic.md) (Taito того ж періоду): купа блоків-символів, гравітація, ціль-залишок.
- Кидок «вибий однакові — поверни інший» — родич [puzzle-bobble](puzzle-bobble.md) (кидок у купу, відбиття від стіни) і [magical-drop](magical-drop.md) (тримаєш те, що витягнув з поля).
- Той самий принцип «снаряд береться з поля / вливається в поле» — [zuma](zuma.md).
- Відмінності портів: FC/GB — віддзеркалене поле, заморожування при поверненні, інша умова закінчення стадії.
- **Осі варіацій**: звідки снаряд (черга / рука / те, що вибив) · траєкторія (пряма / рикошет / вертикальне падіння після упору) · ціль стадії (очистити все / лишити ≤ N / бал) · кінець стадії (одразу на квоті / доки є хід).

## Цікавинки для курсу
- Кидок, що повертає перший невідповідний блок як новий снаряд (`swap` + повернення) — 📎: красивий цикл «стан руки = наслідок попереднього ходу».
- Траєкторія з упором: горизонтально, потім униз по стовпцю; труби, прохідні лише вертикально — 🥉.
- Детекція «нема жодного влучного кидка з будь-якого рядка» — 🥉: симуляція всіх кидків.
- Спецблок-джокер як «життя», що видається після промаху — 🌱.
- Ціль «залишити ≤ N» замість «очистити все» + бонус за залишок — 🌱.
- Розвʼязувач ADVANCE-стадій з лімітом ходів — 🥈.

## Мапа на каталог
- Є: `keyboard-controls` · `projectile-shot` (кинутий блок) · `gravity-fall` · `line-match-clear` (серія однакових у лінії вибивається) · `event-points` · `time-bonus` (аркадний секрет) · `time-out` · `sequential-levels` · `satisfy-constraints` · `no-moves-left` (промах) · `game-over-continue` · `score-records` · `end-screen` · `attract-demo`.
- **Нема** → пропозиції карток:
  - `+throw-swap-return` «Снаряд вибиває однакові й обмінюється з першим іншим, який повертається гравцеві» · entities/interact · 📎.
  - `+wall-bounce-shot` — ⏳ підтверджую (Puzzle Bobble), тут упор → падіння вниз.
  - `+wildcard-tile` — ⏳ підтверджую (спецблок).
  - `+leftover-quota` «Стадія пройдена, коли лишилось ≤ N» · game-logic/win · 🌱 · слоти {quota}.
  - `+pass-through-pipe` «Клітина, прохідна лише в одному напрямку руху» · entities/legality · 🌱 (≈ `one-way-cell`, але для снаряда).
  - `+stun-on-return` «Гравець завмирає, ловлячи снаряд» · entities/state · 🌱.
  - `+move-limit-puzzle` — ⏳ підтверджую (Panel de Pon): ADVANCE.

## Пропозиції до словників
- `+effect:return_to_hand` — снаряд/предмет повертається в руки гравця (Plotting; бумеранги).
- `+ui:held-block` — блок у руках персонажа (що буде кинуто).
- `+ui:quota-target` — ціль «залишити ≤ N».
- `+card:throw-swap-return` · `+card:leftover-quota` · `+card:pass-through-pipe`.

## Джерела
- ⭐ [Wikipedia JA: フリップル](https://ja.wikipedia.org/wiki/フリップル) — правила кидка, відбиття, обміну, спецблоку, промаху, таймера, умови стадій; 60/50/32 стадії, ADVANCE, відмінності портів, прихований бонус.
- [Wikipedia: Plotting (video game)](https://en.wikipedia.org/wiki/Plotting_(video_game)) — назви, роки, порти, перевидання; згадка схожості з Puzznic.
- YouTube: пошук «plotting flipull taito arcade gameplay».

## Непевне
- (?) Числа квоти по стадіях і довжина таймера — не названо.
- (?) Як саме працює 2P (кооператив за інфобоксом JA, без опису; можливо — по черзі).
- (?) Чи розкладки аркадних стадій фіксовані (ймовірно так) — `random: none` з памʼяті.
- (?) JA-формулювання гейм-овера неоднозначне: «час вийшов — −1 спецблок» і «час вийшов — кінець» в одному абзаці.
- (?) Онлайн-рейтинг Arcade Archives — типова фіча серії, для цієї гри не перевірено.
