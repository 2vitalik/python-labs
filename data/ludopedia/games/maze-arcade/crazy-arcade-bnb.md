---
title: Crazy Arcade BnB (Bomb and Bubbles)
slug: crazy-arcade-bnb
aka: [Crazy Arcade, BnB, Bomb and Bubbles, PopTag!, 크레이지 아케이드 비앤비, 泡泡堂, Crazy Arcade BnB M]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: online
  info: full
  random: runtime
  goal: survive
year: 2001
platforms: [Windows (online), mobile (BnB M, 2019)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Crazy_Arcade", best: true, note: "водяні кулі хрестом, бульбашка-пастка: союзник рятує, ворог чи час — смерть; 8 гравців, Manner/Free, персонажі й стати"}
  - {kind: wiki, url: "https://en.wikipedia.org/w/index.php?title=Crazy_Arcade&oldid=944193703", note: "версія статті 2020: режими (Hedgehog, Catch the Leader, Combo, Time Bomb, Monster, Zombie, Boss Turtle) і предмети за регіонами"}
  - {kind: wiki, url: "https://zh.wikipedia.org/wiki/泡泡堂", note: "китайська версія (Shanda): стати персонажів, перелік режимів і карт з особливими цілями"}
  - {kind: wiki, url: "https://ko.wikipedia.org/wiki/크레이지_아케이드", note: "Loduma Studio / Nexon, 800×600, клавіатура й миша, закриття 13.08.2026"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Crazy+Arcade+BnB+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, bomb-fuse, blast-wave, destructible-blocks, in-round-upgrades, item-pickup, inventory-items, temporary-modes, touch-death, respawn, time-out, destroy-all-enemies, online-multiplayer, rating-system, lobby-window, match-setup, character-select, shop-window, keyboard-controls, +team-play, +trap-rescue-or-pop, +bomb-kick, +bomb-throw, +rideable-mount, +character-classes, +xp-level-up, +post-death-role, +hot-potato, +king-capture-win, +boss-fight, +territory-capture, +invisible-to-enemy-team]
proposes: ["+card:trap-rescue-or-pop", "+card:post-death-role", "+card:hot-potato", "+card:invisible-to-enemy-team", "+effect:eliminate", "+effect:mount", "+cond:team", "+cond:riding"]
author: opus
date: 2026-11-09
---

# Crazy Arcade BnB — командний «Бомбермен» з водяними кулями: суперник не гине, а застрягає в бульбашці, яку союзник рятує, а ворог лопає

## Суть
Онлайн-аркада Nexon (2001): до 8 гравців на арені-сітці кладуть водяні кулі, які лопають хрестом струменів. Влучений не вибуває одразу, а потрапляє в **бульбашку**: дотик союзника звільняє, дотик суперника або сплив часу — лопає (смерть). Через це гра командна за природою: рятувати своїх так само важливо, як ловити чужих. Поверх ядра — десятки регіонів-карт із власними предметами (маунти, танки, акули, дрилі) і режимами (хот-потейто з бомбою, лідер команди, кооп проти босів, зомбі).

## Поле і час
- Арена — один екран клітинної сітки (рендер 800×600); блоки, частина з яких руйнується (дриль і космічний корабель «ламають блоки» — отже, звичайно їх ламає вода).
- Real-time; раунд — до перемоги команди; Combo — на час.
- Понад 20 тематичних регіонів з кількома картами в кожному; на частині — особливі цілі («місії»), рейки (Mine), «Ex»-регіони — лише в партнерських PC-bang або з платним апгрейдом кімнати.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж | player | Count (кулі), Power (радіус), Speed; профіль Normal | рух 4 напрямки, кладе кулі |
| Водяна куля | object | власник, сила | вибухає хрестом по вертикалі й горизонталі |
| Струмінь | hazard | довжина = Power | влучив у гравця → бульбашка |
| Бульбашка (пастка) | container | таймер | гравець усередині безпорадний; дотик союзника — вільний, ворога — смерть |
| Блок | object | руйнований / ні | вода руйнує руйнований |
| Liquid | pickup | — | струмінь +1 |
| Water balloon | pickup | — | одночасних куль +1 |
| Roller skates | pickup | — | швидкість +1 |
| Ultra water balloon | pickup | — | струмінь — максимум |
| Red devil | pickup | — | швидкість — максимум |
| Shoes | pickup | — | можна штовхати кулі |
| Gloves | pickup | — | можна кидати кулі |
| Magpie | pickup | — | розворот напрямку або вільне розміщення куль (джерело нечітке) |
| Green devil | pickup | — | змушує «виплюнути» зʼїдений предмет |
| Superman | pickup | тимчасово | максимум усіх здібностей; знімається, якщо потрапив у бульбашку |
| Spacecraft / broken spacecraft | ally | швидкість 10 | маунт; ламає блоки |
| Turtle / pirate turtle | ally | повільний | маунт |
| Owl | ally | швидкість 5 | маунт |
| Ghost | pickup | — | гравця не бачить інша команда |
| Tank (Camp) | ally | швидкість 5 | маунт; стріляє кулями вперед |
| Shark (Aqua) | ally | місткість 3 | ковтає до 3 куль і випльовує вперед |
| Oxygen canister (Factory) | pickup | — | бульбашка лопає повільніше |
| Trap (Factory) | hazard | — | ставиться між нерухомими блоками, ловить перехожих |
| Drill (Mine) | pickup | — | ламає блоки без куль |
| Ore carrier (Mine) | ally | — | маунт, швидший на рейках |
| Octopus / pirate octopus (Sea) | ally | — | маунт, як черепаха |
| Clover (Clover) | pickup | — | +очки, від яких залежить перемога |
| Life potion (Zombie) | pickup | — | лікує інфекцію, +швидкість, тимчасова невразливість |
| Їжак (Hedgehog) | player | — | форма вибулого: лопає кулі дотиком, звільняє будь-кого |
| Лідер (Catch the Leader) | player | прапорець | загинув — гине вся команда |
| Монстри, бос, Boss Turtle | enemy / boss | — | кооп-режими |
| Зомбі | enemy | складність | AI; заражає людей |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(balloon)` → ЯКЩО `counter(my_balloons, <, count)` і `free(cell)` → ТО `place(player, balloon)`.
- КОЛИ `timer(fuse)` → ТО `explode(cross, power)` — струмені по вертикалі й горизонталі.
- КОЛИ `contact(stream, block)` → ЯКЩО `custom: «блок руйнований»` → ТО `disappear_b`; предмет на місці — (?).
- КОЛИ `contact(stream, player)` → ТО `set_state(player, trapped)`; ЯКЩО `state(player, superman)` → ТО `clear_state(player, superman)`.
- КОЛИ `contact(ally, trapped_player)` → ЯКЩО `custom: «одна команда»` → ТО `clear_state(player, trapped)`.
- КОЛИ `contact(enemy_player, trapped_player)` → ЯКЩО `custom: «різні команди»` → ТО `custom: «бульбашка лопає»`, `custom: «гравець вибуває»` (за режимом — або респавн).
- КОЛИ `timer(trap_ttl)` → ЯКЩО `state(player, trapped)` → ТО `custom: «бульбашка лопає»`; Oxygen canister подовжує `trap_ttl`.
- КОЛИ `contact(player, liquid|balloon|roller)` → ТО `pickup`, `counter(power|count|speed, +1)`; ultra balloon / red devil → `set_value(power|speed, max)`.
- КОЛИ `contact(player, balloon)` → ЯКЩО `has(player, shoes)` → ТО `push` (кулю); ЯКЩО `has(player, gloves)` і `input(throw)` → ТО `throw(balloon)`.
- КОЛИ `contact(player, mount)` → ТО `custom: «сідає верхи»`, `speed(player, mount_speed)`; spacecraft/drill: КОЛИ `contact(player, block)` → ТО `disappear_b`.
- Tank: КОЛИ `input(fire)` → ЯКЩО `custom: «гравець верхи на танку»` → ТО `custom: «куля летить у напрямку погляду»`.
- Shark: КОЛИ `contact(shark, balloon)` → ЯКЩО `counter(eaten, <, 3)` → ТО `pickup`; КОЛИ `input(fire)` → ТО `custom: «виплюнути кулю вперед»`.
- КОЛИ `contact(player, ghost)` → ТО `set_state(player, invisible_to_enemies)`.
- Normal: КОЛИ `all_gone(enemy_team)` → ТО `win` (команда).
- Hedgehog: КОЛИ `died(player)` → ТО `transform(player, hedgehog)`; КОЛИ `contact(hedgehog, balloon)` → ТО `custom: «куля лопає»`; КОЛИ `contact(hedgehog, trapped_player)` → ТО `clear_state(player, trapped)` (будь-якого кольору).
- Catch the Leader: КОЛИ `died(leader)` → ТО `custom: «гине вся команда лідера»`.
- Combo: КОЛИ `died(player)` → ТО `respawn(player, start)`, `counter(team_kills, +1)` супернику; КОЛИ `timer(match)` → ТО `custom: «корона — команді з більшою кількістю вбивств, нічия — хто менше помирав»`.
- Time Bomb: КОЛИ `game_start` → ТО `give(random_player, bomb)`; КОЛИ `contact(carrier, player)` → ТО `custom: «бомба переходить»`; КОЛИ `timer(5 s)` → ЯКЩО `has(carrier, bomb)` → ТО `set_state(carrier, trapped)`, `give(random_player, bomb)`.
- Zombie: КОЛИ `contact(zombie, human)` → ТО `transform(human, zombie)`; КОЛИ `contact(player, life_potion)` → ТО `clear_state(player, infected)`, `speed(player, +1)`.
- Monster / Boss Turtle: кооп; КОЛИ `destroyed(boss)` → ТО `win`, `currency(+lucci)` (більше тому, хто лопнув боса).
- Treasure Island: КОЛИ `timer(match)` → ТО `custom: «перемагає сторона, що контролює більше землі»`; Bunny Nest: КОЛИ `counter(rabbits_popped, ==, 20)` → ТО `win`; Lucky Clover: більше конюшини — перемога.
- КОЛИ `game_over` → ТО `custom: «досвід: перемога > нічия > поразка»`.
- Перемога: команда лопнула всіх суперників (Normal) або ціль карти/режиму · Поразка: уся команда в бульбашках, що лопнули · Рахунок: досвід за матч, вбивства (Combo), очки конюшини, лучі (кооп).

## Керування і ввід
- Клавіатура (і миша в меню); стрілки — рух, окрема клавіша — куля, окрема — використати предмет (див. «Непевне»).
- Гравці в кімнаті — до 8 (у деяких регіонах менше; Village 10 — 6); Manner — команди рівно за кольором, Free — довільно.

## Вікна, меню, HUD
- `lobby-window` — список кімнат каналу, створення кімнати.
- `match-setup` (кімната): Manner / Free, команда-колір, регіон і карта, режим.
- `character-select` — 8 базових персонажів (Dao, Dizni, Ethen, Uni, Mos, Kephi, Marid, Bazzi) + Random (може випасти Lodumani чи Santa Claus).
- `shop-window` — платні «Luxury»-версії персонажів, апгрейд кімнати до Ex-регіонів.
- `game-screen` — арена; HUD — `player-portraits` гравців і стан (?), `timer-countdown` у режимах на час (?), `inventory-bar` для предмета, що використовується вручну (?).
- `end-screen` — результат і досвід.
- `profile-window` — рівень: 720 рівнів, позначених формою й кольором медалі, кольором і числом смуг; ladder-ранг важливіший за рівень.
- Переходи: вхід → `lobby-window` → кімната (`match-setup` + `character-select`) → `game-screen` → `end-screen` → кімната.

## Фічі поза полем
- `online-multiplayer` (до 8 у кімнаті) · `mode-coop` (Monster, Zombie, Boss Turtle) · `mode-versus` (Normal та інші).
- `xp-level` — 720 рівнів за досвід; `rank-tiers` — ladder-ранги.
- `unlockables` — зомбі-очки відкривають зомбі; платні Luxury-персонажі.
- Регіони з власними предметами й місіями — фактично `custom-rules` на рівні карти.
- Відгалуження: KartRider (2004), AirRider (2009), Bubble Fighter (2009), BnB M (mobile, 2019); у Північній Америці — PopTag! (2010–2011). Режими-міні-ігри Tetris, Hidden Catch, Dizzy Pang, Bz — були й зникли.

## Варіації й родичі
- `bomberman`, `bomberman-battle-mode` — ядро «бомба з запалом + хрест»; Hudson судилася з Nexon (2003), суд Сеула у 2007 став на бік Nexon.
- `bomberman-multiplayer-variants` — маунти Saturn Bomberman (динозавр поглинає удар) — родич маунтів BnB.
- `bombergirl` — інший командний Bomberman (MOBA 4×4).
- **Осі варіацій:** влучання — смерть (Bomberman) / пастка з рятуванням (BnB) · після смерті — вибув / їжак-помічник / респавн (Combo) · ціль — останній вижилий / лідер / територія / квота (кролики, конюшина) / бос.

## Цікавинки для курсу
- Бульбашка-пастка: стан «у пастці» з таймером, дотик союзника знімає, дотик ворога добиває — 🥉 (командна логіка і стани).
- Hot potato «Time Bomb»: носій має передати бомбу дотиком за 5 с, інакше пастка і новий носій — 🌱.
- Їжак після смерті — роль-помічник, що лопає кулі й рятує будь-кого — 📎.
- Маунти з власною швидкістю й здібностями (танк стріляє кулями, акула ковтає 3 кулі й випльовує) — 🥉.
- Предмети-модифікатори куль: штовхати (shoes) і кидати (gloves) — 📎 кожен.
- Невидимість для команди суперника (ghost) — 📎: рендер залежить від того, хто дивиться.
- Регіон = набір предметів + ціль: правила як дані карти — 🥈.

## Мапа на каталог
- Є: `move-4dir` · `bomb-fuse` ↔ куля · `blast-wave` ↔ струмені хрестом · `destructible-blocks` · `in-round-upgrades` ↔ liquid/balloon/skates · `item-pickup` · `inventory-items` ↔ предмети з ручним використанням · `temporary-modes` ↔ Superman, life potion · `touch-death` ↔ дотик ворога до бульбашки · `respawn` ↔ Combo · `time-out` ↔ Combo/Time Bomb · `destroy-all-enemies` ↔ Normal · `online-multiplayer` · `rating-system` ↔ ladder · `lobby-window` · `match-setup` · `character-select` · `shop-window` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+trap-rescue-or-pop` «Влучений у пастці: союзник рятує, ворог або таймер добиває» · entities/state · 🥉 · слот {ttl}.
  - `+post-death-role` «Вибулий грає далі в іншій ролі (їжак-помічник)» · game-logic/opponent · 📎.
  - `+hot-potato` «Передай бомбу дотиком за N с» · game-logic/opponent · 🌱 · слот {fuse: 5}.
  - `+invisible-to-enemy-team` «Сутність не видна команді суперника» · interface/render · 📎.
  - З корпусу: `+team-play`, `+bomb-kick`, `+bomb-throw` (`bomberman`), `+rideable-mount` (`bomberman-multiplayer-variants`), `+character-classes` (`gauntlet`), `+xp-level-up`, `+king-capture-win` (лідер), `+boss-fight`, `+territory-capture` (Treasure Island).

## Пропозиції до словників
- `+card:trap-rescue-or-pop`, `+card:post-death-role`, `+card:hot-potato`, `+card:invisible-to-enemy-team` — див. вище.
- `+effect:eliminate` — підтримую (`bomberman-battle-mode`): гравець вибуває з раунду.
- `+effect:mount` / `+cond:riding` — підтримую (`bomberman-multiplayer-variants`): сісти на маунта / чи гравець верхи.
- `+cond:team` — підтримую (`bomberman-battle-mode`): чи сутності з однієї команди (рятує союзник, добиває ворог).

## Джерела
- ⭐ [Wikipedia: Crazy Arcade](https://en.wikipedia.org/wiki/Crazy_Arcade) — ядро: кулі хрестом, бульбашка, рятування й добивання, 8 гравців, Manner/Free, персонажі й стати, 720 рівнів, регіони, Ex, назви й видавці, відгалуження, суд з Hudson, закриття.
- [Wikipedia, версія 2020-03-06](https://en.wikipedia.org/w/index.php?title=Crazy_Arcade&oldid=944193703) — режими Normal / Hedgehog / Catch the Leader / Combo / Time Bomb / Monster / Zombie / Boss Turtle; предмети загальні й за регіонами (Camp, Factory, Ice, Sea, Mine, Clover, Zombie, Aqua…).
- [Wikipedia ZH: 泡泡堂](https://zh.wikipedia.org/wiki/泡泡堂) — сильні сторони персонажів, список режимів і карт, особливі цілі (Treasure Island, Zombies, Bunny Nest, Lucky Clover).
- [Wikipedia KO: 크레이지 아케이드](https://ko.wikipedia.org/wiki/크레이지_아케이드) — розробник Loduma Studio, клавіатура й миша, 800×600, закриття сервісу.

## Непевне
- (?) Клавіші: з памʼяті — стрілки, Shift — куля, Ctrl — предмет; джерела лише кажуть «клавіатура й миша».
- (?) Needle, shield, spring — згадані як випадкові предмети зі «Stalker's Box»; що саме роблять (голка — вирватися з власної бульбашки?) — не перевірено.
- (?) Чи падають предмети з розбитих блоків, чи вода ланцюгом підриває інші кулі, чи маунт поглинає влучання — з памʼяті, не з джерел.
- (?) Тривалість бульбашки й ліміт часу раунду — «короткий час», чисел нема.
- (?) Magpie: текст старої статті «розвертає напрям або дозволяє вільно ставити кулі» — переклад сумнівний.
- (?) Режими 2020 року могли змінюватися до закриття у 2026.
