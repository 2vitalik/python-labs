---
title: Hexanaut.io
slug: hexanaut-io
aka: [Hexanaut, Гексанаут]
family: maze-arcade
also: []
klass: avatar
axes:
  field: hex
  time: realtime
  opponent: online
  info: partial
  random: runtime
  goal: territory
year: 2022
platforms: [web, Android, iOS]
links:
  - {kind: other, url: "https://iogames.space/hexanautio", best: true, note: "грати + правила: петля захоплює гекси, король при 20 % і 3 хв, тотеми, без респавну"}
  - {kind: official, url: "https://hexanaut.io/", note: "офіційна сторінка: режими FFA/Duo/PRO/Weekly/Clan Wars, тотеми, PRO-предмети, ранги, меню, налаштування"}
  - {kind: play, url: "https://www.crazygames.com/game/hexanaut-io", note: "грати; розробник Exodragon Games, реліз березень 2022"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hexanaut.io+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-auto, touch-death, player-death, respawn, spawn-random-cell, online-multiplayer, teleport, coverage-area, item-pickup, inventory-items, fog-of-war, minimap-radar, player-camera, leaderboard, profile-stats, rating-system, streak-stats, avatar-picker, theme-select, shop-window, mode-select, game-settings, keyboard-controls, end-screen, main-menu, game-screen, +territory-capture, +region-fill, +trail-vulnerable, +pointer-steering, +percent-goal, +king-hold-timer, +respawn-lock, +capture-totem, +level-speed-bonus, +head-on-both-die, +team-shared-territory, +airdrop-items]
proposes: ["+effect:leave_trail", "+trigger:return_home", "+cond:in_own_zone", "+role:trail", "+card:king-hold-timer", "+card:respawn-lock", "+card:capture-totem", "+card:airdrop-items", "+ui:king-countdown", "+feature:mode-weekly"]
author: opus
date: 2026-11-09
---

# Hexanaut.io — Paper.io на гексах: обведи петлею шматок мапи, стань королем на 20 % і протримайся 3 хвилини

## Суть
Онлайн .io-гра на захоплення території: гравець виходить зі своєї землі, тягне хвіст і, повернувшись, забирає всі гекси всередині петлі. Хто перетнув чужий хвіст — вбив власника. Головна відмінність від [Paper.io](paper-io.md): **мета скінченна** — набрати 20 % мапи, стати королем і втримати поріг 3 хвилини (або вибити всіх). Поки король є, загиблі **не відроджуються**; на мапі стоять **тотеми** з пасивними бонусами, а в PRO-режимах падають одноразові предмети.

## Поле і час
- Мапа з шестикутних клітин (гекси) — одиниця власності й захоплення; рендер 3D.
- Рух безперервний, напрям — за курсором або клавішами з налаштовуваною швидкістю повороту; чи рух прив'язаний до центрів гексів — (?).
- Камера за гравцем, решту видно на мінікарті лише частково (`info: partial`): король бачить усіх і всі бачать короля; шпигунська антена відкриває чужу територію на мінікарті.
- Real-time; до 45 гравців на сервер.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець («змійка» з головою) | player | рівень, швидкість, скін, хвіст | рух безперервно; поза своєю землею тягне хвіст |
| Суперник | enemy | те саме | та сама фізика; ріже хвости, захоплює гекси |
| Партнер (Duo) | ally | спільна територія | спільні земля й бонуси |
| Гекс території | zone | власник | безпечний для власника; петлею перефарбовується, у т.ч. чужий |
| Хвіст | hazard | власник | слід поза своєю землею; чужий дотик — смерть власника |
| Король | player | стан `king`, 20 % мапи | +швидкість, видимий усім на мінікарті, бачить усіх; 3-хвилинний відлік |
| Тотем швидкості | static | — | пасивно додає швидкість власнику |
| Тотем поширення | static | — | сам захоплює гекси довкола |
| Шпигунська антена | static | — | показує чужу територію на мінікарті |
| Телепорт-брама | static | — | переносить у межах своєї території |
| Тотем сповільнення | hazard | хмара | суперники в хмарі сповільнюються |
| Аірдроп (PRO) | pickup | випадковий предмет | дає одноразовий PRO-предмет |
| Гармата (PRO) | projectile | — | «зрізає» голову суперника |
| Ножиці (PRO) | pickup | — | розрізають хвіст суперника |
| Граната захоплення (PRO) | projectile | — | захоплює область у місці влучання |
| Швидкісна комірка (PRO) | pickup | — | короткий прискорювач |
| Цегляна стіна (PRO) | static | — | непрохідний барʼєр перед гравцем |
| Щит (PRO) | pickup | — | коротко захищає хвіст і голову |
| Граблі захоплення (PRO) | pickup | — | захоплюють додаткові гекси вздовж хвоста |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(player, dir)`; КОЛИ `input(aim)` → ТО `face(player, dir)` (з обмеженою швидкістю повороту).
- КОЛИ `leave(player, own_zone)` → ТО `custom: «починає тягнути хвіст»` (`+effect:leave_trail`).
- КОЛИ `enter(player, own_zone)` → ЯКЩО `custom: «є хвіст»` → ТО `fill(region)`, `set_side(region_cells, player)` — захоплені й чужі гекси всередині петлі.
- КОЛИ `counter(captured, >=, next_level)` → ТО `custom: «рівень +1»`, `speed(player, +n)`.
- КОЛИ `contact(a, trail_of_b)` → ЯКЩО `not same(a, b, owner)` → ТО `custom: «b вибуває»`, `counter(slices, +1)` для a.
- КОЛИ `contact(head_a, head_b)` → ЯКЩО `custom: «a на своїй території»` → ТО вибуває лише b; інакше `custom: «вибувають обидва»`.
- КОЛИ `counter(territory_percent, >=, 20)` → ТО `set_state(player, king)`, `speed(player, +n)`, `reveal(all_players_on_minimap)`, `timer(start, 180 s)`.
- КОЛИ `custom: «відлік короля дійшов до 0»` → ЯКЩО `state(player, king)` `and counter(territory_percent, >=, 20)` → ТО `win`.
- КОЛИ `count(enemy, ==, 0)` → ТО `win` (вибито всіх).
- КОЛИ `died(player)` → ЯКЩО `not custom: «на мапі є король»` → ТО `respawn(player, random)` (кнопка RESPAWN); інакше `message(«You can't respawn when someone is King»)`.
- КОЛИ `custom: «тотем у власності гравця»` → ТО `custom: «пасивний бонус тотема»` (швидкість / поширення / антена / телепорт / сповільнення).
- КОЛИ `in_range(slow_totem, enemy, r)` → ТО `speed(enemy, ×k<1)`.
- КОЛИ `input(teleport_gate)` → ТО `teleport(player, own_zone)`.
- PRO: КОЛИ `contact(player, airdrop)` → ТО `give(player, pro_item)`; КОЛИ `input(click|space)` → ЯКЩО `has(player, pro_item)` → ТО `use(player, pro_item)`, `take(player, pro_item)`.
- Duo: КОЛИ `custom: «у команди не лишилось території»` → ТО `lose` (команду вибито).
- Перемога: 3 хв королем з ≥ 20 % або останній живий. · Поразка: перетнули хвіст, лоб у лоб поза своєю землею, команда без землі. · Рахунок: % мапи, «slices», вкрадені гекси → XP і ранг.

## Керування і ввід
- Миша: змійка прямує до курсора.
- WASD / стрілки — змінювати напрям; у налаштуваннях — поворот двома клавішами і швидкість повороту.
- Клік або пробіл — використати PRO-предмет.
- Мобільні: утримання/віртуальний джойстик + кнопка дії.

## Вікна, меню, HUD
- `main-menu`: Play · Play with Friends · коди групи (створити / приєднатись / хостити) · вибір скіна, бейджа, хвоста (`skin-select`).
- `mode-select`: Free For All · Duo · PRO FFA · PRO Duo · Weekly · Clan Wars (тимчасовий подійний режим трійок).
- `game-screen`: мапа з камерою; HUD — `minimap`, `+ui:live-ranking` з відсотками, `level-number` («LEVEL n»), `progress-bar` % території, `+ui:king-countdown` («King wins in» + корона).
- `shop-window` — монети, косметика, підписка без реклами.
- `settings-window` — графіка (згладжування, тіні), кольори й візерунки, `colorblind-palette`, безпечні нікнейми, стиль і швидкість повороту, розмір курсора, тач-джойстик, світла/темна тема, імпорт/експорт/скидання.
- `end-screen`: час гри, монети, % мапи, slices, вкрадені гекси, XP, прогрес рангу; кнопки REPLAY · RESPAWN · NEW GAME.
- `leaderboard` — день / тиждень / місяць, за регіоном і режимом; `stats-window` — профіль; `custom-window` — журнал змін.
- Переходи: main-menu → (mode-select) → game-screen → (вибув) end-screen → respawn / нова гра.

## Фічі поза полем
- `mode-coop` (Duo, Clan Wars) · `+feature:mode-weekly` (правила міняються щотижня) · PRO-режими з аірдропами.
- `rank-tiers`: Copper → Bronze → Silver → Gold → Platinum → Diamond → Master → Champion → Elite → нумеровані ранги з бейджами.
- `streaks` — щоденна нагорода, серія скидається пропуском дня.
- `stats` в акаунті: ігри, разів королем, перемоги, найшвидша перемога, slices, захоплені/вкрадені гекси, макс. % мапи, час гри; `cloud-save` через акаунт (email / Google / Facebook).
- `unlockables` / `custom-skins`: монети за гру → косметика; скрині з випадковими предметами.
- `invite-link` — коди групи; `colorblind-palette`, `theme-select`, `remap-controls` (стиль повороту).

## Варіації й родичі
- [Paper.io](paper-io.md) — те саме ядро «хвіст → петля → заливка», квадрати замість гексів, мета — безкінечний відсоток, без короля й тотемів.
- [Splix.io](splix-io.md) — клітинний .io-аналог з рухом 4 напрямки; [Xonix](xonix.md) — офлайн-предок заливки.
- [Slither.io](slither-io.md) — керування курсором, але без території.
- **Осі варіацій:** сітка (квадрат / гекс); кінець партії (нема / поріг + утримання / останній живий); респавн (завжди / заборонений, поки є король); бонуси (нема / тотеми на мапі / одноразові предмети); команди (соло / дует зі спільною землею).

## Цікавинки для курсу
- Заливка петлі на гекс-сітці: flood fill з зовнішнього краю в гексових координатах — 🥈.
- Стан «король»: поріг %, відлік 3 хв, зняття при падінні нижче порога, блокування респавну для всіх — 📎.
- Тотеми як захоплювані клітини з пасивним ефектом (аура сповільнення, авто-захоплення сусідів) — 🥉.
- Лоб у лоб: результат залежить від того, чия земля під головою — 🌱.
- Рівень за захоплене → швидкість: зворотний звʼязок «сильнішому — швидше» — 🌱.
- Набір одноразових PRO-предметів (ножиці, щит, стіна, граната захоплення) — 🥉 за кожен тип з власною геометрією.

## Мапа на каталог
- Є: `move-auto` · `touch-death` + `player-death` · `respawn` + `spawn-random-cell` · `online-multiplayer` · `teleport` (брама) · `coverage-area` (аура тотема) · `item-pickup` + `inventory-items` (PRO) · `fog-of-war` + `minimap-radar` · `player-camera` · `leaderboard` · `profile-stats` · `rating-system` (ранги) · `streak-stats` · `avatar-picker` + `theme-select` · `shop-window` · `mode-select` · `game-settings` · `keyboard-controls` · `end-screen` · `main-menu` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+territory-capture`, `+trail-vulnerable` (`tron-light-cycles`), `+region-fill`, `+percent-goal` (`xonix`), `+pointer-steering` (`slither-io`).
  - `+king-hold-timer` «Поріг % → король, утримати T хвилин» · game-logic/win · 📎 · слоти {percent, duration}.
  - `+respawn-lock` «Респавн заборонено, поки виконано умову (є король)» · entities/death · 🌱.
  - `+capture-totem` «Захоплюваний тотем з пасивним бонусом» · entities/interact · 🥉 · слот {effect}.
  - `+level-speed-bonus` «Рівень за захоплене дає швидкість» · entities/state · 🌱.
  - `+head-on-both-die` «Лоб у лоб — гинуть обидва, крім власної землі» · entities/combat · 🌱.
  - `+team-shared-territory` «Спільна земля команди» · game-logic/multiplayer · 📎.
  - `+airdrop-items` «Аірдропи з одноразовими предметами» · entities/spawn · 📎.

## Пропозиції до словників
- `+effect:leave_trail`, `+trigger:return_home`, `+cond:in_own_zone`, `+role:trail` — підтверджую з `paper-io` / `splix-io` (ще одна гра).
- `+card:king-hold-timer`, `+card:respawn-lock`, `+card:capture-totem`, `+card:airdrop-items` — див. вище.
- `+ui:king-countdown` — відлік до перемоги лідера з короною на HUD.
- `+feature:mode-weekly` — режим з правилами, що змінюються щотижня (поруч із `mode-daily`).

## Джерела
- ⭐ [iogames.space: Hexanaut.io](https://iogames.space/hexanautio) — грати; хвіст і петля, рівні й швидкість, король при 20 % і 3 хв, тотеми (швидкість, телепорт, сповільнення, шпигунська вежа), без респавну, керування мишею/клавішами/тачем.
- [hexanaut.io](https://hexanaut.io/) — офіційна сторінка: усі режими, правила лоб у лоб, король, п'ять тотемів, сім PRO-предметів, ранги, щоденна серія, лідерборди, меню, налаштування, екран результатів, до 45 гравців.
- [CrazyGames: Hexanaut.io](https://www.crazygames.com/game/hexanaut-io) — розробник Exodragon Games, реліз березень 2022, платформи.
- YouTube: пошук «Hexanaut.io gameplay».

## Непевне
- (?) Рік: CrazyGames дає березень 2022, журнал змін на офіційній сторінці починається з січня 2022 — у шапці 2022.
- (?) Рух: курсор і «швидкість повороту» вказують на вільний кут; чи голова «стрибає» гексами — не перевірено.
- (?) Як саме захоплюється тотем (обвести петлею чи наїхати) і чи його можна відібрати.
- (?) Що стає з територією загиблого (нічия чи вбивці) і чи смертельний власний хвіст — на сторінках не сказано.
- (?) Що буває, коли король падає нижче 20 % або гине до кінця відліку.
- (?) Чи є боти (тоді додати `realtime-ai`). Розмір мапи й кількість рівнів — невідомо.
