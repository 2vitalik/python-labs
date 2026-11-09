---
title: Gladiabots
slug: gladiabots
aka: []
family: program-robots
also: [tactics]
klass: figure
axes:
  field: free
  time: programmed
  opponent: online
  info: full
  random: both
  goal: score
year: 2019
platforms: [PC, Mac, Linux, mobile]
links:
  - {kind: other, url: "https://wiki.gladiabots.com/index.php?title=Conditions_and_actions", best: true, note: "офіційна вікі: усі дії, умови й селектори цілі — повний «словник» редактора ШІ"}
  - {kind: steam, url: "https://store.steampowered.com/app/871930/", note: "GFX47, 22.05.2019: режими, кампанія, онлайн-кар'єра, асинхронні матчі, пісочниця"}
  - {kind: official, url: "https://gladiabots.com/", note: "сайт: опис, лінки на вікі, пресскіт, Discord"}
  - {kind: other, url: "https://wiki.gladiabots.com/index.php?title=BotProgramming_Basics", note: "як обходиться дерево: корінь, дія, умова, конектор, sub-AI, порядок перевірки, тік"}
  - {kind: other, url: "https://wiki.gladiabots.com/index.php?title=Basics", note: "мапи 50×50 м, симетрія, режими, щит/здоровʼя"}
  - {kind: other, url: "https://wiki.gladiabots.com/index.php?title=Bot_classes", note: "4 класи: HP, щит, швидкість, DPS за дальністю, точність, ліміт 35 %"}
  - {kind: other, url: "https://wiki.gladiabots.com/index.php?title=Special_entities", note: "бази, ресурси, силові поля, аптечки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=gladiabots+gameplay+ai+tree", note: "пошук; геймплей і розбори ШІ"}
stage: v1
coverage: 65
mechanics: [command-program, sensor-predicates, user-procedures, code-editor-window, undo-redo, hp-damage, projectile-shot, melee-vs-ranged, respawn, collect-quota, destroy-all-enemies, time-out, online-multiplayer, async-multiplayer, rating-system, leaderboard, replay, replay-window, match-setup, game-pause, spawn-points, spawn-random-cell, item-pickup, shop-window, +behavior-tree-priority, +target-selector, +range-bands, +health-band-conditions, +shield-regen-delay, +bot-tags-memory, +class-composition-limit, +symmetric-map-generation, +carry-slows, +domination-capture, +sandbox-both-teams, +replay-rewind-speed, +tournaments]
proposes: ["+window:ai-editor-graph", "+window:team-setup", "+window:ai-list", "+ui:debug-target-lines", "+cond:range_band(target, band)", "+cond:health_band(target, pct)", "+cond:current_action(target, act)", "+cond:tagged(target, tag)", "+effect:flee(a, from)", "+effect:tag(target, tag)", "+effect:score_resource", "+feature:sandbox-both-teams", "+feature:tournaments", "+axis:control"]
author: opus
date: 2026-11-09
---

# Gladiabots — збери загін роботів і дерево умов-дій для кожного; у матчі вони б'ються самі

## Суть
Гравець не керує роботами в бою: він обирає класи бійців (штурмовик, кулеметник, дробовик, снайпер) і будує для них **ШІ — візуальне дерево** з вузлів-умов, вузлів-дій, конекторів і вкладених sub-AI. Щотіку кожен бот обходить своє дерево в глибину і виконує першу валідну дію: атакувати найслабшого ворога на середній дистанції, тікати при щиті < 25 %, нести ресурс на базу. Матч — на симетричній процедурній арені в одному з трьох режимів; програв — дивишся реплей, правиш дерево, пробуєш знову проти кампанії чи гравців онлайн.

## Поле і час
- Поле — неперервна арена 50×50 м (**не сітка**), процедурна, з дзеркальною або обертальною симетрією; кілька точок спавну на команду.
- Дальності — три смуги для всіх: коротка 3 м, середня 8 м, далека 15 м; поза — out of range.
- Час `programmed`: дерево перевіряється кожен тік, миттєво; рішення базуються на даних попереднього тіку (дії, HP, щит, дальності на початку тіку).
- Обмеження матчу за часом; рівна кількість знищень наприкінці Elimination — нічия.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Штурмовик (Assault) | piece | HP 5000, щит 3000, швидкість 1.2 / 0.5 з ресурсом, прицілювання 1 | середній у всьому; точність 95/55/15 % |
| Кулеметник (Machine gun) | piece | HP 7000, щит 6000, швидкість 2/3 (з ресурсом так само), прицілювання 2 | найбільша вогнева сила, 100 пострілів у черзі; ≤ 35 % команди |
| Дробовик (Shotgun) | piece | HP 3000, щит 5000, швидкість 2.0 / 0.5, 5 куль за постріл | дуже сильний близько, 0 шкоди далеко; ≤ 35 % |
| Снайпер (Sniper) | piece | HP 3000, щит 3000, швидкість 1.0 / 0.5, прицілювання 3 | 100 % влучність у межах дальності, 2000 за постріл; ≤ 35 % |
| Ресурс | resource | — | `Grab` → нести (повільніше), `Score` на союзну базу → +1 |
| База | zone | власник: свій / ворожий / нейтральний | Collection: приймає ресурси; Domination: захоплюється, дає очки з часом |
| Силове поле | pickup | один власник за раз | захоплений бот отримує на 70 % менше шкоди |
| Аптечка | pickup | спавн випадково (Elimination) | повністю відновлює HP, щит не чіпає |
| Точка спавну | spawner | — | з'являються боти; respawn у Collection і Domination |
| Вузол-дія | tile | дія + ціль + селектор | валідна → виконується цей тік, обхід зупинено |
| Вузол-умова | tile | умова + ціль | валідна → перевіряються діти; інакше — відкат |
| Конектор | tile | — | завжди валідний; з'єднує всіх батьків з усіма дітьми |
| Sub-AI | tile | інше дерево | вкладене дерево як процедура |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `custom: «кожен бот обходить своє дерево в глибину від кореня, дітей — проти годинникової стрілки»`.
- КОЛИ `custom: «обхід дійшов до вузла-умови»` → ЯКЩО умова виконана → ТО `custom: «перевіряти дітей»`; інакше `custom: «відкат до попередньої умови, наступна гілка»`.
- КОЛИ `custom: «обхід дійшов до вузла-дії»` → ЯКЩО `legal(action)` → ТО `custom: «виконати дію цей тік, обхід завершено»`.
- КОЛИ `custom: «валідної дії не знайдено»` → ТО `custom: «Idle»`.
- AND/OR/XOR — `custom: «складаються розташуванням кількох умов»`: ланцюжок умов = AND, сусідні гілки = OR.
- Умови: `count(kind, op, n)` (Exists, X1–X10, ≥, ≤) · `in_range(me, target, short|medium|long|out)` · відстань до краю арени · `has(target, resource)` · `state(target, health 0–25…75–100 %)` · щит тими ж смугами · HP/щит цілі нижче / рівно / вище мого · поточна дія моя / цілі / союзника на ціль / ворога на ціль · клас цілі · `custom: «тег бота 1–5 / тег команди A–E»`.
- Селектор цілі: closest / furthest to me, до краю арени, weakest / strongest health, shield, health+shield (абсолютно й у частках), Any (лише в умовах), All (лише Move/Flee/Tag/Untag).
- КОЛИ `exec(Attack enemy)` → ТО `custom: «прицілювання N с, далі черга»`, `damage(target)` з точністю за смугою дальності.
- КОЛИ `custom: «бот отримав шкоду»` → ТО `custom: «спершу знімається щит, потім HP»`; HP не відновлюється.
- КОЛИ `custom: «бот 3+ с без шкоди»` → ТО `custom: «щит відновлюється; повний — за 3 с»`.
- КОЛИ `exec(Move target)` / `exec(Flee target)` → ТО `move(bot, to|from target)`.
- КОЛИ `exec(Grab resource)` → ТО `pickup(bot, resource)`, `speed(bot, carrying)`; КОЛИ `exec(Score ally_base)` → ЯКЩО `in_range(bot, base, short)` → ТО `score(+1)`.
- КОЛИ `exec(Tag / Untag target n)` → ТО `set_state(target, tag_n)` / `clear_state(target, tag_n)` — памʼять і координація без змінних; Exclusive tag — лише на одного.
- КОЛИ `hp_zero(bot)` → ТО `disappear_a`; ЯКЩО `mode(collection|domination)` → ТО `respawn(bot, spawn)`.
- КОЛИ `in_range(bot, base, short)` → ЯКЩО `mode(domination)` і `custom: «ворога в базі нема»` → ТО `set_side(base, team)` з часом; союзна база → `score(+n)` за час, більше ботів — швидше.
- КОЛИ `contact(bot, force_field)` → ЯКЩО `custom: «поле вільне»` → ТО `set_state(bot, -70% damage)`.
- КОЛИ `contact(bot, health_pack)` → ТО `heal(bot, full)`.
- КОЛИ `timer(limit)` → ТО `game_over`: більше очок → `win`; Elimination — більше знищень, рівно → `draw`.
- Перемога: більше очок (ресурси / утримання баз / знищення) · Поразка: менше · Рахунок: ліга й рейтинг онлайн, зірки кампанії (?).

## Керування і ввід
- Редактор графа: додати вузол, задати умову/дію, ціль і селектор, тягнути зв'язки «знизу батька — вгору дитини»; D — дублювати, E — правити вузол, T — правити ціль, Del — видалити, Z/Y — undo/redo.
- Список ШІ: створити, перейменувати (F2), дублювати, видалити; на бота — одне ШІ.
- Налаштування команди: класи бійців і ШІ для кожного; порядок у списку = порядок спавну.
- Реплей: Space пауза, ← назад на 10 с (30 у прискоренні), Z повільно, F швидко, A — автокамера, E — у редактор ШІ, R — заново.
- Тач-керування на мобільних (?).

## Вікна, меню, HUD
- `main-menu` → кампанія / онлайн-кар'єра / пісочниця / турніри / виклики.
- `ai-list` → `ai-editor-graph` (`code-editor`): дерево з вузлами-овалами (умови), прямокутниками (дії), ромбами (конектори), sub-AI.
- `team-setup` (`match-setup`): класи, ШІ, ліміт 35 % на клас.
- `game-screen`/`replay-window`: арена, боти з `hp-bar` і щитом, `debug-target-lines` (поточна ціль кожного бота), рахунок, `timer-countdown`, `speed-slider`, перемотка.
- `level-select` кампанії (сотні місій); `leaderboard` / ліги; `profile-window` (рівень гравця, XP); `shop-window` скінів за кредити.
- Консоль повідомлень гри (Ctrl+Alt+2).

## Фічі поза полем
- Кампанія з сотнями соло-місій; `mode-sandbox` — керуєш обома командами для тестів.
- Онлайн: ranked / unranked / private, асинхронні матчі (суперник не мусить бути онлайн), турніри, ліги з league score, XP-рівень, крос-платформа (свій акаунт).
- Синхронізація й резервні копії ШІ; скіни за кредити (DLC/покупки).

## Варіації й родичі
- [Carnage Heart](carnage-heart.md) — той самий принцип «бій без керування», але блок-схема на платі; [Bot Arenas](bot-arenas.md) — текстовий код замість графа; [RoboRally](roborally.md) — програма на хід.
- Ігри з деревами поведінки/гамбітами: Final Fantasy XII (gambits), Dragon Age (tactics) — список «умова → дія» за пріоритетом (?).
- Осі варіацій: **форма ШІ** (список пріоритетів / дерево з відкатом / блок-схема / автомат); **селектор цілі** (будь-хто / найближчий / найслабший); **памʼять** (нема / теги / змінні); **поле** (неперервне / сітка).

## Цікавинки для курсу
- Дерево поведінки з обходом у глибину і відкатом, конекторами й sub-AI — 🥇.
- Селектори цілі (closest, weakest health+shield) і смуги дальності як умови — 🥉.
- Щит з регенерацією після 3 с без шкоди поверх HP — 📎.
- Теги ботів як спільна памʼять команди без змінних — 🥉.
- Три режими на одному рушії (збір, утримання баз, знищення) — 🥈.
- Пісочниця «обидві команди мої» + реплей з перемоткою — 🥈.

## Мапа на каталог
- Є: `command-program` ↔ ШІ бота; `sensor-predicates` ↔ умови; `user-procedures` ↔ sub-AI; `code-editor-window` ↔ редактор графа; `undo-redo`; `hp-damage`; `projectile-shot`, `melee-vs-ranged` ↔ класи за дальністю; `respawn`; `collect-quota` ↔ Collection; `destroy-all-enemies` ↔ Elimination (наближено — тут «більше»); `time-out`; `online-multiplayer`, `async-multiplayer`; `rating-system`, `leaderboard`; `replay`, `replay-window`; `match-setup`; `game-pause`; `spawn-points`, `spawn-random-cell` ↔ аптечки; `item-pickup`; `shop-window`.
- **Нема** → пропозиції карток:
  - `+behavior-tree-priority` «Дерево умов і дій з обходом у глибину» · game-logic/program · 🥇.
  - `+target-selector` «Вибір цілі: найближчий / найслабший» · game-logic/program · 🥉.
  - `+range-bands` «Дальність як смуги short/medium/long» · entities/combat · 📎.
  - `+health-band-conditions` «Умови за смугами HP/щита» · game-logic/program · 📎.
  - `+shield-regen-delay` «Щит відновлюється після паузи без шкоди» · entities/state · 📎.
  - `+bot-tags-memory` «Теги як памʼять і координація» · game-logic/program · 🥉.
  - `+class-composition-limit` «Ліміт частки класу в команді» · game-logic/constraints · 🌱.
  - `+symmetric-map-generation` (з Bot Arenas) — симетрична процедурна арена.
  - `+carry-slows` «Ноша сповільнює» · entities/state · 🌱.
  - `+domination-capture` «Захоплення й утримання точок» · game-logic/win · 🥉.
  - `+sandbox-both-teams` «Пісочниця з керуванням обома командами» · game-logic/opponent · 📎.
  - `+replay-rewind-speed` «Реплей з перемоткою й швидкістю» · interface/results · 🥉.
  - `+tournaments` «Турніри гравців» · interface/results · 🥈.

## Пропозиції до словників
- `+window:ai-editor-graph` — редактор дерева поведінки (різновид `code-editor`).
- `+window:team-setup` — склад команди й ШІ на бійця (ширше за `match-setup`).
- `+window:ai-list` — бібліотека збережених програм.
- `+ui:debug-target-lines` — лінії від бота до поточної цілі.
- `+cond:range_band(target, band)` — ціль у смузі дальності.
- `+cond:health_band(target, pct)` — HP/щит у смузі відсотків.
- `+cond:current_action(target, act)` — що зараз робить ціль.
- `+cond:tagged(target, tag)` / `+effect:tag(target, tag)` — мітки ботів.
- `+effect:flee(a, from)` — відступати від цілі.
- `+effect:score_resource` — здати ресурс на базу.
- `+feature:sandbox-both-teams` · `+feature:tournaments`.
- `+axis:control` — значення `behavior-tree`.

## Джерела
- ⭐ [Wiki: Conditions and actions](https://wiki.gladiabots.com/index.php?title=Conditions_and_actions) — Move, Flee, Attack, Grab, Score, Tag/Untag, Idle, DropResource; умови й селектори.
- [Wiki: BotProgramming Basics](https://wiki.gladiabots.com/index.php?title=BotProgramming_Basics) — корінь, дія, умова, конектор, sub-AI; обхід у глибину, проти годинникової стрілки, відкат, щотіку, дані попереднього тіку.
- [Wiki: Basics](https://wiki.gladiabots.com/index.php?title=Basics) — арена 50×50 м, симетрія, режими, щит/HP.
- [Wiki: Bot classes](https://wiki.gladiabots.com/index.php?title=Bot_classes) — таблиця характеристик, смуги 3/8/15 м, ліміт 35 %.
- [Wiki: Special entities](https://wiki.gladiabots.com/index.php?title=Special_entities) — бази, ресурси, силові поля (−70 %), аптечки.
- [Steam](https://store.steampowered.com/app/871930/) — режими, кампанія, ranked/unranked/private, турніри, асинхронні матчі, крос-платформа, пісочниця.
- [gladiabots.com](https://gladiabots.com/) — опис і лінки на вікі.

## Непевне
- (?) Рік: Steam-реліз 22.05.2019; ранній доступ / мобільний вихід раніше (у черзі — 2018) — не перевірено.
- (?) Мобільні платформи — висновок із «крос-платформи»; не бачив сторінок магазинів.
- (?) Тривалість матчу, туман війни (здається, нема — `info: full`), перешкоди на арені.
- (?) Одиниці регенерації щита й часу прицілювання у вікі не вказані; таблиця вікі може відставати від патчів.
- (?) Зірки кампанії; рівні ліг.
- Поле неперервне, не клітинне — описано через цінність дерева поведінки для сімʼї.
