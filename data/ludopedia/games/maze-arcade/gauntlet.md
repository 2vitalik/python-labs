---
title: Gauntlet (1985)
slug: gauntlet
family: maze-arcade
also: [roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: coop
  info: partial
  random: runtime
  goal: score
year: 1985
platforms: [arcade, NES, Atari ST, Amiga, ZX Spectrum, Commodore 64]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gauntlet_(1985_video_game)", best: true, note: "класи, генератори, Death, здоровʼя, що тане, їжа, кооп, фрази оповідача"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gauntlet_II", note: "відмінності Gauntlet II: It, дракон, stun-плитки, рикошет"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=gauntlet+1985+arcade+4+player+gameplay", note: "пошук; геймплей на 4"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=gauntlet", note: "пошук; збірки й римейк 2014"}
stage: v1
coverage: 65
mechanics: [move-8dir, projectile-shot, melee-vs-ranged, hp-damage, inventory-items, key-and-door, reach-exit, teleport, chase-greedy, spawn-schedule, player-camera, +character-classes, +destructible-spawner, +health-drain, +smart-bomb, +shoot-items, +lobbed-projectile, +life-drain-enemy, +thief, +wall-trap, +multi-exit, +stall-exits, +shared-camera, +coin-continue, +stat-upgrade-pickup]
proposes: ["+trigger:tick", "+trigger:hp_zero", "+trigger:idle", "+trigger:input", "+cond:has", "+cond:in_range", "+cond:line_of_sight", "+effect:hp", "+effect:heal", "+effect:take", "+effect:set_cell", "+effect:spawn_at", "+effect:clear", "+role:spawner", "+role:gate", "+role:hazard", "+ui:hp-bar", "+ui:inventory-bar", "+window:character-select", "+window:game-over-continue", "+feature:mode-coop", "+axis:actors"]
author: opus
date: 2026-11-02
---

# Gauntlet — до чотирьох героїв продираються крізь лабіринти, повні генераторів монстрів, поки здоровʼя тане

## Суть
До 4 гравців одночасно обирають класи (Воїн, Валькірія, Чарівник, Ельф) і проходять рівні-лабіринти зверху: знищують генератори, що невпинно плодять монстрів, підбирають ключі, їжу, зілля, скарби і шукають вихід. Здоровʼя — і «життя», і таймер: воно тане щосекунди, від ударів монстрів і від Смерті; їжа його поповнює, монета — теж. Головне — потік ворогів і поділ ресурсів між гравцями (спільна їжа, спільний екран).

## Поле і час
- Рівень — клітинний лабіринт, більший за екран; камера одна на всіх і рухається лише так, щоб усі гравці лишались у кадрі (`+shared-camera`).
- Стіни і двері — клітини; герої й монстри рухаються у 8 напрямках, піксельно, але колізії — по клітинах.
- Real-time; здоровʼя зменшується щосекунди (≈ 1 HP/с) (?), тож простоювати не можна.
- Рівні 1–7 — фіксовані навчальні з підказками, далі — послідовність із набору; часом рівень віддзеркалюється/перевертається (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Thor, Воїн (червоний) | player | броня ~20% (?), найсильніший у ближньому бою, повільний | постріл сокирою, ближній удар при контакті |
| Thyra, Валькірія (синя) | player | найкраща броня (~30%) (?) | щит; збалансована |
| Merlin, Чарівник (жовтий) | player | найсильніша магія, без броні (?) | слабкий у ближньому |
| Questor, Ельф (зелений) | player | найшвидший; стріли | слабка броня |
| Привид (Ghost) | enemy | рівні 1–3 | летить до гравця, удар і зникає (камікадзе); лише стріляти |
| Ґрант (Grunt) | enemy | рівні 1–3 | біжить до гравця, бʼє кийком впритул |
| Демон (Demon) | enemy | рівні 1–3 | ближній удар + кидає вогняні кулі на лінії |
| Лобер (Lobber) | enemy | рівні 1–3 | тримає дистанцію, кидає каміння **через стіни** |
| Чаклун (Sorcerer) | enemy | рівні 1–3 | блимає невидимістю; у невидимого постріли пролітають |
| Злодій (Thief) | enemy | — | біжить до гравця, краде предмет, тікає до виходу (?) |
| Смерть (Death) | enemy | висмоктує до ~200 HP, потім зникає | невразлива для пострілів; знищується лише зіллям |
| Генератор | spawner | 3 рівні міцності (кістки/хатинки) | породжує монстрів свого рівня, поки не зруйнований |
| Стіна | static | — | непрохідна |
| Двері | gate | — | відкриваються ключем; суміжні дверні клітини зникають разом |
| Ключ | pickup | в інвентарі | витрачається на двері |
| Їжа | pickup | +100 HP (?) | частину можна знищити пострілом («don't shoot food») |
| Зілля (potion) | pickup | в інвентарі | кнопка Magic — уражає всіх монстрів на екрані; постріл у зілля — слабший вибух |
| Спецзілля | pickup | +броня / +магія / +сила пострілу / +швидкість пострілу / +ближній бій / +місткість (?) | постійне підсилення героя на гру |
| Амулет | pickup | тимчасовий (невидимість та ін.) (?) | тимчасовий стан |
| Скарб | pickup | очки | лише очки |
| Пастка (trap) | terrain | — | наступ → зникають певні стіни рівня |
| Телепорт | terrain | — | переносить до найближчого іншого телепорта |
| Вихід (Exit / Exit to N) | static | номер рівня | перехід на наступний або на N рівнів уперед |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(1 с)` → ТО `hp(each_player, -1)` (?) — здоровʼя тане постійно.
- КОЛИ `input(fire)` → ТО `spawn(shot, facing)`; КОЛИ `contact(shot, monster)` → ТО `hp(monster, -shot_power)`, ЯКЩО `hp == 0` → ТО `disappear_b`, `score(level × base)`.
- КОЛИ `contact(player, monster)` → ТО `hp(monster, -melee)` і `hp(player, -damage × (1 − armor))`.
- КОЛИ `contact(ghost, player)` → ТО `hp(player, -10·level)` (?), `disappear_a`.
- КОЛИ `contact(death, player)` → ТО `custom: «висмоктує HP, доки не забере ~200, потім зникає»`; кулі Смерть не беруть.
- КОЛИ `timer(spawn)` → ЯКЩО `free(adjacent_cell)` → ТО `spawn_at(monster(level), next_to_generator)`; КОЛИ `contact(shot, generator)` → ТО `hp(generator, -1)` → нижчий рівень → `destroyed`.
- КОЛИ `input(magic)` → ЯКЩО `has(player, potion)` → ТО `take(potion)`, `custom: «шкода всім монстрам на екрані за силою магії класу; Смерть гине»` (`+smart-bomb`).
- КОЛИ `contact(shot, potion)` → ТО `custom: «слабший вибух»`; КОЛИ `contact(shot, food)` → ТО `disappear_b` (для знищуваної їжі).
- КОЛИ `contact(player, food)` → ТО `heal(player, 100)` (?); КОЛИ `contact(player, treasure)` → ТО `score(100)` (?).
- КОЛИ `contact(player, key|potion)` → ЯКЩО `count(inventory, <, capacity)` → ТО `pickup`; інакше залишається.
- КОЛИ `contact(player, door)` → ЯКЩО `has(player, key)` → ТО `take(key)`, `set_cell(door_group, floor)`; інакше `block`.
- КОЛИ `contact(player, special_potion)` → ТО `custom: «+1 до стату класу назавжди (до смерті)»`.
- КОЛИ `enter(player, trap)` → ТО `set_cell(linked_walls, floor)`.
- КОЛИ `enter(player, teleporter)` → ТО `teleport(player, nearest_other_teleporter)`.
- КОЛИ `enter(player, exit)` → ТО `next_level(+1 | +N)` для всіх гравців.
- КОЛИ `idle(довго)` (ніхто не проходить рівень) → ТО `custom: «усі стіни стають виходами»` (?).
- КОЛИ `contact(thief, player)` → ТО `take(player, item)`, злодій тікає (?).
- КОЛИ `hp_zero(player)` → ТО `window(game_over_continue)`: монета протягом кількох секунд → відродження на місці з повним HP (?); інакше герой вибуває, інші грають далі.
- КОЛИ `counter(hp, <, 200)` → ТО `sound(«Warrior needs food, badly» / «… is about to die»)`.
- Перемога: нема (нескінченні рівні). Поразка: HP героя = 0 без доплати. Рахунок: монстри, генератори, скарби; підсумковий рахунок ділиться на кількість кредитів (за Wikipedia).

## Керування і ввід
- На кожного гравця — 8-позиційний джойстик, Fire (дальня атака) і Magic (зілля, також старт).
- У 4-місному автоматі кожне місце привʼязане до свого класу і кольору (?); у 2-місному — вибір класу.
- Гравець може приєднатись будь-коли, кинувши монету, — без перезапуску рівня.

## Вікна, меню, HUD
- `splash-screen` / атракт: представлення класів зі статами, монстрів і предметів, демо, таблиця рекордів.
- `+window:character-select` — вибір класу (2-місна версія) / приєднання до гри.
- `game-screen` — лабіринт + бічна панель на кожного гравця: `+ui:hp-bar` (числове здоровʼя), `score`, `+ui:inventory-bar` (ключі, зілля), назва класу.
- Між рівнями — номер рівня і текстові підказки на ранніх рівнях («Ghosts must be shot», …) (?).
- `+window:game-over-continue` — «Insert coin to continue» з відліком.
- `leaderboard` — рекорди з ініціалами.
- Звук: оповідач коментує події («Elf shot the food!», «Remember, don't shoot food»).
- Переходи: атракт → (монета) класи → гра → (вихід) наступний рівень → … → (HP 0) continue → гра / атракт.

## Фічі поза полем
- `mode-coop` до 4 гравців на одному екрані (`+feature:mode-coop`), вільний вхід/вихід посеред гри; дружній вогонь у Gauntlet I не шкодить («Shots do not hurt other players, yet»).
- `continue` за монету — здоровʼя як валюта; `+feature:operator-settings` — скільки HP дає монета (?).
- `leaderboard-local`; збережень, паузи нема.

## Варіації й родичі
- Gauntlet II (1986): «It» (гра в квача), дракон на кілька клітин, кислотні калюжі, рикошет пострілів, stun-плитки, невидимі і «магічні» стіни, фальшиві виходи, секретні кімнати, однакові класи різного кольору.
- Dandy (1983, Atari 8-bit) — прототип ідеї; Gauntlet: Dark Legacy, Gauntlet (2014); Diablo-подібні кооп-рубилки.
- Родичі: Wizard of Wor (кооп у лабіринті), Rogue (класи, зілля), Bomberman (спільна арена).
- **Осі варіацій:** спавн ворогів (фіксовані / генератори, що руйнуються / нескінченні); здоровʼя (життя / HP-таймер); ресурси (особисті / спільні на полі); камера (своя / спільна, що тримає всіх).

## Цікавинки для курсу
- Генератор-спавнер з рівнями міцності, що породжує монстрів свого рівня, — 🥉.
- Здоровʼя як таймер (тане щосекунди) + їжа як ресурс, за який змагаються союзники, — 📎.
- Шість поведінок монстрів: камікадзе, ближній бій, стрільба на лінії, кидок через стіни, невидимість, висмоктування — 🥉 за сімʼю.
- Зілля «розумна бомба» + постріл у предмет (знищити їжу / підірвати зілля) — 📎.
- Класи зі статами (броня, сила, магія, швидкість) як дані — 🥉.
- Спільна камера для 4 гравців — 🥈 (обмеження руху краєм кадру).
- Пастки, що прибирають стіни, і телепорт до найближчого — 📎.

## Мапа на каталог
- Є: `move-8dir` · `impassable-cells` · `projectile-shot` · `shoot-forward` · `melee-vs-ranged` (ближній удар vs постріл, лобери) · `hp-damage` · `item-pickup` · `inventory-items` (ключі, зілля) · `inventory-limit` (?) · `key-and-door` · `reach-exit` · `teleport` (до найближчого) · `chase-player`/`chase-greedy` · `spawn-schedule` (генератори) · `touch-death` · `player-death` · `event-points` · `sequential-levels` · `progress-acceleration` · `player-camera` · `status-panel` · `score-records` · `leaderboard` · `game-screen` · `splash-screen`.
- **Нема** → пропозиції карток:
  - `+character-classes` «Класи героя зі статами» · entities/state · 🥉 · слоти {armor, shot, melee, magic, speed}.
  - `+destructible-spawner` «Спавнер, якого можна зруйнувати» · entities/spawn · 🥉 · слоти {hp, every}.
  - `+health-drain` «Здоровʼя тане з часом» · entities/state · 🌱 · слот {rate}.
  - `+smart-bomb` «Предмет уражає всіх на екрані» · entities/combat · 📎.
  - `+shoot-items` «Постріл знищує/активує предмет» · entities/interact · 📎.
  - `+kamikaze-enemy` «Ворог гине разом з ударом» · entities/combat · 🌱.
  - `+lobbed-projectile` «Кидок через стіни» · entities/combat · 🥉.
  - `+life-drain-enemy` «Ворог висмоктує HP до ліміту і зникає» · entities/combat · 📎.
  - `+thief` «Злодій забирає предмети» · entities/interact · 📎 (Chip's Challenge).
  - `+wall-trap` «Плита прибирає звʼязані стіни» · entities/interact · 📎.
  - `+multi-exit` «Виходи на різні рівні» · levels/progression · 🌱.
  - `+stall-exits` «Після затримки все стає виходом» · levels/progression · 🌱 (протилежність Bomberman `+timeout-punisher`).
  - `+shared-camera` «Одна камера тримає всіх гравців» · interface/render · 🥈.
  - `+coin-continue` «Продовження за ресурс із відліком» · game-logic/lose · 📎.
  - `+stat-upgrade-pickup` «Предмет назавжди підсилює стат» · entities/state · 📎.

## Пропозиції до словників
- `+trigger:tick` / `timer` — танення HP; `+trigger:hp_zero` — смерть героя; `+trigger:idle` — довго без проходу → стіни-виходи; `+trigger:input` — Fire / Magic.
- `+cond:has` — ключ, зілля; `+cond:in_range` — лобер тримає дистанцію; `+cond:line_of_sight` — демон стріляє на лінії.
- `+effect:hp` / `+effect:heal`; `+effect:take` — ключ на двері, злодій; `+effect:set_cell` — двері, пастки; `+effect:spawn_at` — генератор; `+effect:clear` — зілля на весь екран.
- `+role:spawner` — генератор; `+role:gate` — двері; `+role:hazard` — пастка (?).
- `+ui:hp-bar` (числом), `+ui:inventory-bar` (ключі/зілля в панелі гравця).
- `+window:character-select`, `+window:game-over-continue` (Dig Dug).
- `+feature:mode-coop` — до 4 гравців, вільний вхід посеред гри.
- `+axis:actors` — `party`: кілька людей, кожен зі своїм героєм на одному полі.

## Джерела
- ⭐ [Wikipedia: Gauntlet (1985)](https://en.wikipedia.org/wiki/Gauntlet_(1985_video_game)) — класи, генератори, Death і зілля, танення здоровʼя, монета-продовження, фрази оповідача, керування.
- [Wikipedia: Gauntlet II](https://en.wikipedia.org/wiki/Gauntlet_II) — що додала друга частина (It, дракон, stun-плитки, рикошет, секретні кімнати).
- YouTube: пошук «gauntlet 1985 arcade 4 player gameplay».
- Steam: пошук «gauntlet».

## Непевне
- (?) Числові стати класів (броня 20/30%, сила, швидкість) — з памʼяті; Wikipedia лише якісно.
- (?) Темп танення HP (1/с), +100 HP за їжу, HP за монету, 100 очок за скарб — з памʼяті.
- (?) Набір спецзіль і амулетів у Gauntlet I (частина може бути з Gauntlet II).
- (?) «Усі стіни стають виходами» після затримки; поведінка злодія; привʼязка класу до місця в 4-місному автоматі — з памʼяті.
- (?) Фіксовані перші 7 рівнів і віддзеркалення рівнів — з памʼяті.
- Fandom (402) і StrategyWiki (403) недоступні, ліміт WebSearch вичерпано — перевірка лише по Wikipedia.
