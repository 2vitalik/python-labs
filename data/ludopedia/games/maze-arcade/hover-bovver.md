---
title: Hover Bovver
slug: hover-bovver
aka: [Hover Bover]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: collect
year: 1983
platforms: [Commodore 64, Atari 8-bit (1984), Windows (2002), Intellivision (2018), arcade (Galaxian/Scramble, 2022)]
links:
  - {kind: play, url: "https://c64.krissz.hu/hover-bovver/play-online/", best: true, note: "інструкція: Gordon Bennet і Air-Mo, три шкали (Dog Tolerance, Dog Loyalty, Mower Overload), живоплоти, очки, бонус Canine Fidelity, екран Start/Setup; грати в браузері"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hover_Bovver", note: "суть: скосити всі клітини трави, розгін і перегрів, сусід, садівник, пес, косарки Jim/Tom/Alf як життя, порти"}
  - {kind: other, url: "https://everygamegoing.com/larticle/gameplay-c64-hover-bovver/2313", note: "Personal Computer News: 16 газонів, F1 — вибір із перших семи, топ-5 з ініціалами, газони 9–16 змушують косити клумбу"}
  - {kind: other, url: "https://hardcoregamer.com/news/llamasoft-ports-hover-bovver-to-even-older-hardware/419229/", note: "порт 2022: косарка на повітряній подушці, дрейф по діагоналі"}
  - {kind: other, url: "https://www.atarimania.com/game-atari-400-800-xl-xe-hover-bovver_2519.html", note: "картка Atari 8-bit"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hover+Bovver+C64", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-by-input, impassable-cells, floor-types, cell-transform, collect-all, chase-player, chase-greedy, random-walk, player-death, event-points, sequential-levels, level-select, progress-acceleration, score-records, hot-seat, status-panel, background-music, attract-demo, game-screen, match-setup, +overheat-meter, +hold-to-accelerate, +ally-command, +ally-tolerance-betrayal, +event-summoned-enemy, +terrain-avoiding-enemy, +leftover-resource-bonus, +lives-as-lenders]
proposes: ["+effect:command", "+cond:speed", "+ui:heat-bar", "+ui:loyalty-bar", "+card:overheat-meter", "+card:hold-to-accelerate", "+card:ally-command", "+card:ally-tolerance-betrayal", "+card:event-summoned-enemy", "+card:terrain-avoiding-enemy", "+card:leftover-resource-bonus", "+card:lives-as-lenders"]
author: opus
date: 2026-11-09
---

# Hover Bovver — скоси весь газон позиченою косаркою, поки сусід не відібрав: розгін перегріває, пес допомагає, доки терпить

## Суть
Gordon Bennet без дозволу позичив у сусіда Jim косарку на повітряній подушці (Air-Mo) і мусить скосити **кожну клітину трави** на газоні, поки Jim женеться за ним, щоб її забрати. Косарка розганяється, якщо тримати напрям, але від швидкості **перегрівається** і глухне; скошені клітини та зупинка її охолоджують. Пес Rover за кнопкою кидається на переслідувачів, проте лише доки є «вірність», а від шуму косарки втрачає «терпіння» й сам кусає косарку. Перша гра Llamasoft (Jeff Minter) для C64.

## Поле і час
- Однекранний газон: сітка клітин трави, живоплоти, клумби з квітами.
- 16 газонів, кожен складніший; з 9-го газону скосити клумбу доводиться неминуче (PCN).
- Real-time; косарка з інерцією «повітряної подушки» — може дрейфувати по діагоналі (порт 2022).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Gordon на косарці Air-Mo | player | швидкість, нагрів (Mower Overload) | рух джойстиком; тримаєш напрям — розганяється |
| Трава | terrain | — | косарка проїжджає → скошена, +очки |
| Скошена трава | terrain | — | прохід охолоджує косарку |
| Живопліт | static | — | непрохідний для всіх; укриття й місце охолодити косарку |
| Клумба з квітами | terrain | — | косарка розорює; садівник не ступає; скошені квіти кличуть садівника |
| Сусід Jim | enemy | — | іде прямо на гравця; квіти ігнорує; ловить → забирає косарку |
| Садівник | enemy | зʼявляється вгорі екрана | після скошених квітів; переслідує, обходить клумби; Rover страшний йому лише коли гавкає |
| Пес Rover | ally | Dog Tolerance, Dog Loyalty | блукає сам; за кнопкою женеться за сусідом/садівником; без терпіння кусає косарку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(mower, dir)`; ЯКЩО `moving(mower, dir)` (той самий напрям) → ТО `speed(mower, +1)`; інакше `block` (живопліт).
- КОЛИ `enter(mower, grass)` → ТО `set_cell(cell, mown)`, `score(lawn_number)`.
- КОЛИ `tick` → ЯКЩО `moving(mower, any)` → ТО `counter(overload, +k·speed)` (`+cond:speed`).
- КОЛИ `tick` → ЯКЩО `custom: «косарка стоїть або їде скошеною травою»` → ТО `counter(overload, -k)`.
- КОЛИ `counter(overload, ==, max)` → ТО `stun(mower)` до спаду шкали до порога.
- КОЛИ `enter(mower, flowers)` → ТО `set_cell(cell, ploughed)`, `spawn_at(gardener, top)` (якщо його ще нема).
- КОЛИ `contact(neighbour, mower)` або `contact(gardener, mower)` → ТО `lives(-1)`, `custom: «косарку забрано, наступну позичено в іншого сусіда (Jim → Tom → Alf)»`.
- КОЛИ `input(fire)` → ЯКЩО `counter(loyalty, >, 0)` → ТО `custom: «пес біжить на сусіда/садівника»` (`+effect:command`); переслідувач тікає або завмирає (`stun`).
- КОЛИ `tick` → ЯКЩО `state(rover, commanded)` → ТО `counter(loyalty, -1)`; на нулі пес перестає слухатись.
- КОЛИ `contact(rover, neighbour)` → ТО `score(+n)` щотіку, поки кусає.
- КОЛИ `contact(gardener, rover)` → ЯКЩО `state(rover, barking)` → ТО `custom: «садівник тікає»`; інакше пса ігнорує.
- КОЛИ `tick` → ТО `counter(tolerance, -1)` (шум косарки дратує пса).
- КОЛИ `counter(tolerance, ==, 0)` → ТО `set_state(rover, hostile)` — пес женеться за косаркою.
- КОЛИ `contact(rover, mower)` → ЯКЩО `state(rover, hostile)` → ТО `stun(mower)` (миттєвий перегрів), `counter(tolerance, = 0)`.
- КОЛИ `contact(mower, rover)` (переїхав пса) → ТО `counter(tolerance, = 0)`, `custom: «пес тікає з вереском»`.
- КОЛИ `input(fire)` → ЯКЩО `state(rover, hostile)` and `counter(loyalty, >, 0)` → ТО `custom: «перенаправити ворожого пса на переслідувача»`.
- КОЛИ `tick` → ЯКЩО `not state(rover, commanded)` → ТО `custom: «пес блукає випадково»` (`random-walk`).
- КОЛИ `all_gone(grass)` → ТО `score(loyalty × lawn_number)` (Canine Fidelity Bonus), `next_level`.
- КОЛИ `counter(mowers_left, ==, 0)` (забрали косарку Alf) → ТО `game_over`.
- Перемога: окремого фіналу джерела не описують — гра на очки. Поразка: забрали останню косарку. Рахунок: номер газону за кожну клітину, очки за укуси пса, бонус за залишок вірності.

## Керування і ввід
- Джойстик (C64 — порт 1): рух косарки; утримання напрямку — розгін.
- Кнопка вогню — команда псу «фас» (на сусіда або садівника).
- C64: F1 — вибір стартового газону з перших семи (PCN); Atari: на екрані Start/Setup FIRE — газон 1–8, OPTION — 1/2 гравці, SELECT — кількість джойстиків, START — почати.
- Двоє гравців грають по черзі, зазвичай з одним джойстиком.

## Вікна, меню, HUD
- `attract-demo` — вступні анімації; натискання FIRE відкриває екран налаштувань.
- `leaderboard` — Top 5 з ініціалами між демо.
- `match-setup` (Start/Setup) — стартовий газон, кількість гравців, джойстиків.
- `game-screen` — газон; унизу три шкали: Dog Tolerance, Dog Loyalty, Mower Overload (`+ui:heat-bar`, `+ui:loyalty-bar`); `score`; життя показані іменем власника косарки (Jim / Tom / Alf).
- `end-screen` — кінець гри; введення ініціалів, якщо рекорд.
- Переходи: демо ⇄ Top 5 → (FIRE) Start/Setup → (START) газон → (усе скошено) бонус → наступний газон → (забрали косарку Alf) кінець → Top 5.

## Фічі поза полем
- `level-select` стартового газону (C64 — 1–7, Atari — 1–8; газони 9–16 лише після 8-го).
- `hotseat` на двох, `leaderboard-local` Top 5 з ініціалами.
- Музика у стилі музичної скриньки.

## Варіації й родичі
- Atari 8-bit (1984, Aaron Liddiment); Windows (2002, Idigicon/Kool Dog, не Minter) — без розгону, 5 життів замість 3; Hover Bovver 2: Grand Theft Flymo (2002, PC); Intellivision (2018, Elektronite, Óscar Toledo); порт Llamasoft на «залізо» Galaxian/Scramble (2022, MAME).
- [Amidar](amidar.md), [Xonix](xonix.md) — зафарбувати поле; [Pac-Man](pac-man.md) — зібрати всі клітини, тікаючи від переслідувачів; тут клітини — трава, а «енерджайзер» замінено псом із власними шкалами.
- **Осі варіацій:** рух — сталий (Pac-Man) / розгін при утриманні з перегрівом (Hover Bovver); помічник — нема / союзник за командою з ресурсом команд (вірність) і власним «настроєм» (терпіння), що може обернутись проти гравця; ворог за подією — завжди на полі / викликається порушенням (скошені квіти).

## Цікавинки для курсу
- Швидкість ↔ нагрів: розгін при утриманні напрямку, шкала перегріву, зупинка до порога, охолодження на скошеному — 📎.
- Союзник із двома шкалами: вірність витрачається на команди, терпіння тане від дій гравця, на нулі союзник атакує — 🥉 (два ресурси, стан ally ↔ hostile).
- Ворог, якого викликає порушення (скошена клумба), і шлях, що обходить певний тип клітин — 📎 (BFS з забороненим terrain).
- Мета «скосити всі клітини» з очками, що ростуть з номером газону — 🌱.
- Бонус кінця рівня за залишок ресурсу (вірність) — 🌱.
- Життя як «позичені косарки» з іменами власників — 🌱 (подача лічильника життів).

## Мапа на каталог
- Є: `move-by-input` · `impassable-cells` ↔ живоплоти · `floor-types` + `cell-transform` ↔ трава → скошена, клумба → розорана · `collect-all` ↔ кожна клітина трави · `chase-player` + `chase-greedy` ↔ сусід іде прямо на гравця · `random-walk` ↔ пес · `player-death` ↔ забрали косарку · `event-points` · `sequential-levels` ↔ 16 газонів · `level-select` · `progress-acceleration` ↔ газони складнішають · `score-records` ↔ Top 5 · `hot-seat` · `status-panel` ↔ три шкали · `background-music` · `attract-demo` · `game-screen` · `match-setup`.
- **Нема** → пропозиції карток:
  - `+overheat-meter` (вже Deflektor) — шкала, що росте від швидкості й зупиняє аватар на максимумі.
  - `+hold-to-accelerate` «Утримання напрямку розганяє» · entities/move · 🌱.
  - `+ally-command` «Союзник за командою з лімітом» · entities/interact · 📎 · слот {budget: meter}.
  - `+ally-tolerance-betrayal` «Союзник, що від дій гравця стає ворожим» · entities/state · 🥉.
  - `+event-summoned-enemy` «Порушення викликає нового ворога» · entities/spawn · 🌱.
  - `+terrain-avoiding-enemy` «Ворог не ступає на певний тип клітин» · entities/move · 📎.
  - `+leftover-resource-bonus` «Бонус за залишок ресурсу в кінці рівня» · scoring · 🌱 (протилежність `leftover-penalty`).
  - `+lives-as-lenders` «Життя як іменовані речі» · interface/hud · 🌱.

## Пропозиції до словників
- `+effect:command` (вже Exit) — наказати союзнику дію щодо цілі (фас на сусіда).
- `+cond:speed` — швидкість сутності порівняно з N (нагрів залежить від швидкості).
- `+ui:heat-bar` (вже ×3) — шкала перегріву Mower Overload; `+ui:loyalty-bar` — шкала ресурсу союзника (вірність, терпіння).
- `+card:overheat-meter`, `+card:hold-to-accelerate`, `+card:ally-command`, `+card:ally-tolerance-betrayal`, `+card:event-summoned-enemy`, `+card:terrain-avoiding-enemy`, `+card:leftover-resource-bonus`, `+card:lives-as-lenders` — див. «Мапу на каталог».

## Джерела
- ⭐ [c64.krissz.hu: Hover Bovver](https://c64.krissz.hu/hover-bovver/play-online/) — інструкція: історія Gordon Bennet, три шкали й що їх змінює, охолодження на скошеному, живоплоти для всіх, садівник поважає квіти, очки «1 × номер газону», бонус Canine Fidelity, косарки Jim/Tom/Alf, екран Start/Setup; гра в браузері.
- [Wikipedia: Hover Bovver](https://en.wikipedia.org/wiki/Hover_Bovver) — мета, розгін, перегрів, сусід прямо на гравця, садівник не ходить клумбами, пес із Loyalty/Tolerance, наїзд на пса, порти й відмінності Windows-версії.
- [Personal Computer News (everygamegoing)](https://everygamegoing.com/larticle/gameplay-c64-hover-bovver/2313) — 16 газонів, F1 і перші сім, Top 5 з ініціалами, газони 9–16 з неминучою клумбою, косарка розорює клумби, але не живопліт.
- [Hardcore Gamer: порт 2022](https://hardcoregamer.com/news/llamasoft-ports-hover-bovver-to-even-older-hardware/419229/) — повітряна подушка, дрейф по діагоналі, однекранні рівні, садівник за скошені квіти.
- [Atarimania: Hover Bovver](https://www.atarimania.com/game-atari-400-800-xl-xe-hover-bovver_2519.html) — картка Atari-версії, відгуки гравців.
- YouTube: пошук «Hover Bovver C64».

## Непевне
- (?) Екран Start/Setup з OPTION/SELECT/START — це клавіші Atari 8-bit; інструкцію на krissz.hu, ймовірно, взято з Atari-видання; на C64 вибір газону — F1 (PCN).
- (?) Що після 16-го газону — цикл чи кінець.
- (?) Скільки очок за укус пса і як саме рахується бонус Canine Fidelity (інструкція: «з вірності й номера газону»).
- (?) Чи поповнюються Dog Loyalty і Dog Tolerance між газонами.
- (?) Чи косарка рухається строго по клітинах, чи вільно з дрейфом (порт 2022 описує дрейф по діагоналі).
- (?) Чи сусідів-переслідувачів може бути двоє одночасно (один відгук на Atarimania каже «два сердиті сусіди»).
