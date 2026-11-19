---
title: YENDOR
slug: yendor
aka: [nh]
family: program-robots
also: [roguelike]
klass: avatar
axes:
  field: square
  time: programmed
  opponent: ai
  info: partial
  random: both
  goal: collect
year: 2025
platforms: [web (HTML5 на itch.io)]
links:
  - {kind: itch, url: "https://olifog.itch.io/yendor", best: true, note: "грати в браузері (≈30 хв); опис «{rogue, zach}-like programming game», коментарі гравців про баланс золота"}
  - {kind: other, url: "https://github.com/olifog/YENDOR", note: "сирці (GPL v3): мова nh → C → WebAssembly, сама гра написана на nh; README з синтаксисом"}
  - {kind: other, url: "https://raw.githubusercontent.com/olifog/YENDOR/main/game/tech.nh", note: "дерево апгрейдів: 3 гілки, ціни, попередники, фінал «???»"}
  - {kind: other, url: "https://raw.githubusercontent.com/olifog/YENDOR/main/game/docs_content.nh", note: "вбудована документація: 25 сторінок, API бота, легенда тайлів"}
  - {kind: other, url: "https://raw.githubusercontent.com/olifog/YENDOR/main/LANGUAGE.md", note: "довідник мови nh"}
  - {kind: other, url: "https://itch.io/jam/langjamgamejam", note: "Langjam Gamejam, 14–21 грудня 2025: створи мову, потім гру на ній"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=YENDOR+olifog+programming+game", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [command-program, user-procedures, sensor-predicates, step-execution, code-editor-window, dungeon-generation, stairs-levels, move-8dir, impassable-cells, item-pickup, hp-damage, player-death, shop-between-levels, cheat-codes, save-autosave, help-window, tutorial-window, main-menu, pause-menu, game-screen, popup-text, particles, sound-effects, +tech-tree-unlock-language, +purchasable-sensors, +bank-at-exit, +difficulty-as-investment, +ops-limit-timeout, +speed-upgrades, +tech-tree, +auto-pathfind-command, +meta-unlocks, +d20-combat, +drunken-walk-corridors, +program-restart-on-level]
proposes: ["+effect:bank", "+cond:unlocked(x)", "+window:tech-tree", "+window:tombstone", "+feature:unlockable-language", "+feature:difficulty-investment", "+axis:rules", "+card:tech-tree-unlock-language"]
author: opus
date: 2026-11-19
---

# YENDOR — пиши бота мовою nh для NetHack-підземелля, а здобутим золотом купуй саму мову

## Суть
Гравець не водить `@` руками: він пише програму мовою **nh** («злий нащадок C, Python і OCaml» з NetHack-синтаксисом), і бот сам іде згенерованим підземеллям, бʼється з кобольдами й гоблінами, збирає золото й спускається сходами. Золото, донесене до сходів, іде в банк, а банк витрачають на дерево апгрейдів, де купується **все**: швидкість симуляції, HP і сила бота, складність підземелля (вона підвищує дохід) і навіть **конструкції мови** — цикли, змінні, функції, масиви, лямбди, сенсори й пошук шляху.

Фінал — купити всі 50 апгрейдів і капстоун «???»: «Merge with the machine. Become the Wizard of Yendor.» Гру зроблено на Langjam 2025 (тиждень: спершу мова, потім гра на ній), і сама гра — рендер, редактор, генератор, бій — теж написана на nh і скомпільована у WebAssembly.

## Поле і час
- Мапа 50×20 клітин: кімнати зі стінами `-` `|`, двері `+`, коридори `#`, сходи `>`, золото `$`, гоблін `g`. Екран поділено: підземелля ліворуч, редактор коду праворуч.
- Генерація поверху: кімнати випадкового розміру (з апгрейдом Var Size — 3–7) з проміжком ≥1 клітина; кожна нова кімната звʼязується з найближчою вже приєднаною, починаючи з кімнати 0.
- Коридор копається «пʼяним ходом»: 85 % кроків до цілі, 12 % перпендикулярно, 3 % хитання, ліміт 280 кроків; з імовірністю 70 % додається ще один коридор від випадкової кімнати до найдальшої (петля).
- Бот стартує в центрі випадкової кімнати; сходи — у верхньому правому куті кімнати 0, а після апгрейду Rnd Stairs — у випадковій іншій кімнаті.
- Час `programmed`: програма виконується покроково з базовою затримкою 1000 мс на крок; апгрейди піднімають максимальну швидкість до ×5 / ×10 / ×100 / ×1000; за кадр — не більше 100 тіків.
- Тік бота закінчує лише **успішний** `/move/`; невдалий крок у стіну тіку не закінчує — програма виконується далі.
- Бот бачить тільки те, що повертають куплені сенсори: 3×3 довкола, квадрат радіуса r ≤ 5, найближчий обʼєкт, кімната, уся мапа.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бот `@` | player | HP 16, сила 18, AC 4 (база); рівень досвіду | виконує програму; `/move/dx/dy` — крок у 8 напрямків (dx, dy ∈ {−1, 0, 1}) |
| Програма nh | — (код) | ≤100000 операцій, глибина викликів ≤100, вкладених циклів ≤16 | згори вниз; дійшла до кінця — «Program complete.», не зациклюється; на новому поверсі — з першого рядка |
| Стіна `-` `\|` | static | — | непрохідна; `/can_move/` повертає 0 |
| Підлога кімнати | terrain | розмір кімнати | прохідна; тут спавн золота, монстрів і бота |
| Коридор `#` | terrain | «пʼяний хід» | прохідний, звʼязує кімнати |
| Двері `+` | terrain | — | клітина, де коридор входить у кімнату |
| Сходи `>` | static | фіксовані / випадкові | кінець поверху: переносне золото → банк + бонус, новий поверх |
| Купа золота `$` | pickup | 1–3 на поверх (= кількість кімнат); ×2 з Gold Spawn+ | дає переносне золото; зʼявляється лише з апгрейдом Gold Spawn |
| Кобольд | enemy | спавн з апгрейдом Kobolds | атакує кидком d20 проти AC бота |
| Гоблін `g` | enemy | з апгрейдом Goblins — кожен монстр 50/50 | те саме |
| Банк | resource | ціле | поповнюється лише на сходах; витрачається на апгрейди |
| Апгрейд | — (вузол дерева) | ціна 10–200000; попередник (часто «будь-який з кількох») | купівля відкриває можливість, перегенеровує поверх і скидає бота |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «кімнати + коридори пʼяним ходом»`, `spawn_at(stairs, room0_corner)` або випадкова кімната, `spawn_at(gold, random_floor)` (з Gold Spawn), `spawn_at(monster, random_floor)`.
- КОЛИ `exec(move)` → ЯКЩО `free(target)` → ТО `move(bot, dir)`, `end_turn`.
- КОЛИ `exec(move)` → ЯКЩО `cell(target, wall)` → ТО `block`; тік не закінчено, програма йде далі.
- КОЛИ `exec(move)` → ЯКЩО `occupied(target, monster)` → ТО `custom: «атака бота»` (?).
- КОЛИ `custom: «атака бота»` → ЯКЩО `custom: «d20 ≤ 10 + AC монстра + рівень + бонус»` → ТО `damage(monster, 1d6 + бонус сили)`.
- Бонус влучання = рівень бота + 1 за спритність > 14; бонус сили: > 15 → +1, 18 → +2, 18/51+ → +3, 18/100 → +6; сила на влучання не впливає.
- КОЛИ `custom: «атака монстра»` → ЯКЩО `custom: «d20 ≤ 10 + AC бота + рівень монстра + бонус»` → ТО `damage(bot, 1dN)`.
- КОЛИ `custom: «влучання»` → ЯКЩО `custom: «AC цілі < 0»` → ТО `custom: «шкода мінус rnd(0..|AC|), але не менше 1»`.
- КОЛИ `hp_zero(monster)` → ТО `disappear(monster)`, `counter(xp, +5 × рівень монстра)`.
- КОЛИ `hp_zero(monster)` → ЯКЩО `custom: «куплено Gold Drops»` → ТО `currency(+drop)` (×2 з Gold Drops+), `message(«(+$ gold)»)`.
- КОЛИ `hp_zero(bot)` → ТО `lose`, `custom: «програма зупиняється, екран-надгробок з кнопками рестарту»`.
- КОЛИ `enter(bot, gold)` → ТО `pickup`, `counter(carried_gold, +value)` (?).
- КОЛИ `enter(bot, stairs)` → ТО `sound(level_up)`, `custom: «банк += переносне + бонус поверху; переносне = 0»`, `counter(dungeon_level, +1)`, `next_level`.
- КОЛИ `level_start` → ЯКЩО `custom: «попередній поверх пройдено сходами»` → ТО `custom: «програма з першого рядка — Restarting on new level...»`.
- Бонус поверху — сума `+$N` куплених апгрейдів складності (Rnd Stairs +2, Var Size +3, +1 Room +4…+6, Kobolds +5, Goblins +5, +1 Monster +6); номер поверху на бонус і складність не впливає.
- КОЛИ `program_end` → ТО `message(«Program complete.»)`, `custom: «бот стоїть»`.
- КОЛИ `counter(ops, >, 100000)` → ТО `crash`, `message(«Bot timed out: Infinite loop detected»)`.
- КОЛИ `counter(call_depth, >=, 100)` → ТО `crash` (рекурсія); так само ділення на 0, індекс поза списком, невідома функція — з підсвіткою рядка.
- КОЛИ `input(buy)` → ЯКЩО `counter(bank, >=, cost)` and `custom: «куплено попередника»` → ТО `currency(-cost)`, `unlock(upgrade)`, `custom: «новий поверх і скидання бота»`.
- КОЛИ `counter(upgrades, ==, 50)` → ТО `unlock(capstone)`.
- КОЛИ `input(buy_capstone)` → ТО `win`, `window(ending)`.
- Перемога: капстоун «???» (усі 50 апгрейдів) · Поразка: HP бота = 0 → надгробок і рестарт · Рахунок: банк золота; глибина поверху — лише лічильник.

## Керування і ввід
- Редактор праворуч з vim-подібними клавішами (розкладку QWERTY виправляли хотфіксом); запуск і зупинка бота, покроковий режим з підсвіткою поточного рядка, швидкість — до купленого максимуму.
- Синтаксис nh: `>` і `<` — дужки блоку («сходи»), `.` — кінець речення, `:=` — нова змінна, `#name(args) >` … `<` — функція, `<< v` — return, `/f/a/b.` — виклик («паличка»), `|` — pipe, `\(x) => …` — лямбда.
- Ще: `loop >` з `>>` (break) і `><` (continue), `for i in 0..10 >`, хвостові `when` / `unless`, `a if c else b`, `value | >` з `_` — match, слова `lt gt le ge`, `and or not`, структури `{x: 5}` з `->`.
- API бота: `/move/dx/dy`, `/get_x/`, `/get_y/`, `/get_hp/`, `/get_max_hp/`, `/get_gold/`, `/get_level/`, `/print/`, `/rng_int/min/max`, списки `list_create/push/get/len`, `json`, `strcat`.
- Сенсори (купуються): `/can_move/dx/dy` → 1/0, `/check_surroundings/` → 3×3 тайлів, `/scan_area/r` → (2r+1)², `/find_nearest/"gold"|"monster"|"stairs"` → `{x, y, dist, type}` або 0, `/pathfind_to/x/y` → `{dx, dy, found}`, `/get_room_info/` → межі, виходи, предмети, сутності, `/full_map_scan/` («Expensive! Cache the result.»).
- Дерево апгрейдів — клік по вузлу; кнопка Center центрує дерево.

## Вікна, меню, HUD
- `main-menu` → вступ (CRT-ефект, за ним уже видно гру) → `game-screen`.
- `tutorial-window`: навчальний режим блокує інший ввід; мовні вузли дерева можуть знову показати свою спливну підказку-урок.
- `game-screen`: підземелля + `code-editor` + панель бота; `instruction-highlight` поточного рядка, `popup-text` — плаваючий текст над полем (?), частинки, текст помилки коду.
- `custom-window` «UPGRADES» (дерево): вузли трьох гілок, «Bank: $», кнопка Center.
- `help-window` — оверлей документації: 25 сторінок від Basics до Full Map, з прикладами коду.
- `pause-menu`; `custom-window` чат / вхідні повідомлення (?).
- `end-screen` смерті — надгробок; `custom-window` фіналу після капстоуна.
- Переходи: меню → вступ → game-screen ⇄ UPGRADES / docs / пауза / чат; смерть → надгробок → game-screen; «???» → фінал.

## Фічі поза полем
- `meta-progression` деревом на 50 вузлів + капстоун.
- Гілка Buff: +4 HP ×3, +1 сила ×3, −1 AC ×2, Gold Spawn / Gold Spawn+ (×2), Gold Drops / Gold Drops+ (×2), швидкість ×5 / ×10 / ×100 / ×1000.
- Гілка Difficulty: Rnd Stairs, Var Size, +1 Room ×4, Kobolds, Goblins, +1 Monster ×2 — складність купує сам гравець заради бонусу поверху.
- Гілка Language (24 вузли): For Loop (10) → When, Compare → Can Move, Variables, Math → Functions → Break, Return → Loop → Arrays, Structs, Strings → If-Else, Pipes, Block ? → Match, Lambda; сенсори Surround, Scan, Pathfind, Find, Room, Full Map (до 4000).
- Ціни від 10 до 200000 (Strength III); капстоун коштує 0, але вимагає всіх 50.
- `autosave` при зупинці бота; на itch — кнопки «Run game» і «Restore game».
- `speed-control` і `step-mode` — у редакторі; чит у сирцях: вбудована функція `jofhjyv` додає 1000000 до банку.
- Нема редактора рівнів, мультиплеєра й окремого вибору складності — складність теж покупка.

## Варіації й родичі
- [NetHack Learning Environment](nethack-learning-environment.md) — справжній NetHack для Python-агента; YENDOR — іграшкова NetHack-копія з власною мовою й економікою.
- [The Farmer Was Replaced](the-farmer-was-replaced.md), [The Miner Was Replaced](the-miner-was-replaced.md), [Kingdom.py](kingdom-py.md) — той самий хід «конструкції мови купуються за ресурс».
- [Screeps](screeps.md), [Untrusted](untrusted.md), [CodeCombat](codecombat.md) — код керує героєм, доступне API росте з прогресом.
- Роглайк-корені: тайли `- | + # > $`, кидок d20 проти класу броні, сила 18/xx — прямо з Rogue/NetHack.
- **Осі варіацій**: що купується (стати / сенсори / синтаксис мови) · хто задає складність (гра / гравець як інвестицію) · коли програма стартує заново (кожен тік / кожен поверх / ніколи) · що бачить бот (3×3 / радіус / уся мапа).

## Цікавинки для курсу
- Інтерпретатор із «замкненими» конструкціями: парсер знає, які вузли мови куплено, і відкидає решту — 🥈 (граматика + перевірка за списком відкритих фіч).
- Покроковий виконавець: yield на кожен успішний `/move/`, ліміт 100000 операцій як детектор нескінченного циклу, ліміт глибини рекурсії — 🥉.
- Генератор кімнат з коридорами «пʼяним ходом» 85/12/3 % і петлею з імовірністю 70 % — 🥇 (картка `dungeon-generation`).
- Економіка «неси до виходу»: переносне золото стає банком лише на сходах, плюс бонус за обрану складність — 📎.
- Сенсори як API різної сили: 3×3 → радіус → найближчий обʼєкт → шлях → уся мапа — 🥉 (кожен окремо 📎; `pathfind_to` з BFS/A* — 🥇).
- Бій d20 проти AC з бонусом сили 18/xx і зменшенням шкоди за відʼємного AC — 📎.
- Дерево апгрейдів з умовою «будь-який з кількох попередників» і капстоуном «усі 50» — 🥉.

## Мапа на каталог
- Є: `command-program` ↔ програма nh; `user-procedures` ↔ функції `#name`; `sensor-predicates` ↔ `/can_move/`, `/check_surroundings/`; `step-execution` ↔ покроковий режим з рядком; `code-editor-window` ↔ редактор праворуч; `dungeon-generation` ↔ кімнати й коридори; `stairs-levels` ↔ сходи → новий поверх; `move-8dir` ↔ dx, dy ∈ {−1, 0, 1}; `impassable-cells` ↔ стіни; `item-pickup` ↔ золото; `hp-damage` ↔ HP і d20; `player-death` ↔ надгробок; `shop-between-levels` ↔ дерево апгрейдів; `cheat-codes` ↔ `jofhjyv`; `save-autosave` ↔ збереження при зупинці; `help-window` ↔ docs; `tutorial-window`; `main-menu`; `pause-menu`; `game-screen`; `popup-text`; `particles`; `sound-effects`.
- **Нема** → пропозиції карток:
  - `+tech-tree-unlock-language` «Конструкції мови купуються» · game-logic/program · 🥈 — четверта гра корпусу після TFWR, TMWR і Kingdom.py.
  - `+purchasable-sensors` «Сенсори бота відкриваються апгрейдами» · game-logic/program · 🥉 · слот {sensors: 3x3|radius|nearest|path|room|map}.
  - `+bank-at-exit` «Здобуте зараховується лише на виході з рівня» · game-logic/economy · 📎.
  - `+difficulty-as-investment` «Гравець купує складність заради більшого доходу» · game-logic/difficulty · 📎.
  - `+ops-limit-timeout` «Ліміт операцій програми = нескінченний цикл» · game-logic/program · 🌱.
  - `+speed-upgrades` «Максимальна швидкість симуляції купується» · game-logic/economy · 🌱.
  - `+d20-combat` «Кидок d20 проти класу броні» · entities/combat · 📎.
  - `+drunken-walk-corridors` «Коридор випадковим блуканням з ухилом до цілі» · levels/generation · 🥉.
  - `+program-restart-on-level` «Програма бота стартує заново на кожному рівні» · game-logic/program · 🌱.
  - Уже пропоновані іншими: `+tech-tree`, `+auto-pathfind-command`, `+meta-unlocks`.

## Пропозиції до словників
- `+effect:bank` — переносне золото переходить у банк на виході з поверху.
- `+cond:unlocked(x)` — гравець уже купив апгрейд чи можливість (Gold Drops, мовна конструкція).
- `+window:tech-tree` — дерево апгрейдів з банком і кнопкою центрування.
- `+window:tombstone` — надгробок як екран смерті (традиція NetHack).
- `+feature:unlockable-language` — синтаксис мови відкривається покупками.
- `+feature:difficulty-investment` — складність як покупка, що підвищує дохід.
- `+axis:rules` — `unlocked`: правила (тут — сама мова програмування) відкриваються по ходу гри.
- `+card:tech-tree-unlock-language` — механіка вже в чотирьох іграх корпусу.

## Джерела
- ⭐ [itch.io: YENDOR](https://olifog.itch.io/yendor) — опис, автори olifog, GreenMan891, kenL4; HTML5, безкоштовно, ≈30 хв; коментарі: золото росте повільно, пошук шляху знецінює ранній код, у повторному проходженні мову можна вживати без купівлі.
- [GitHub: olifog/YENDOR](https://github.com/olifog/YENDOR) — README: nh, розділений екран, vim-клавіші, компілятор flex/bison → C → Emscripten, Langjam 2025.
- [tech.nh](https://raw.githubusercontent.com/olifog/YENDOR/main/game/tech.nh) — усі 50 апгрейдів з цінами й попередниками, капстоун, базові HP 16, сила 18, AC 4.
- [docs_content.nh](https://raw.githubusercontent.com/olifog/YENDOR/main/game/docs_content.nh) — 25 сторінок документації, API сенсорів, легенда тайлів.
- [LANGUAGE.md](https://raw.githubusercontent.com/olifog/YENDOR/main/LANGUAGE.md) — синтаксис nh.
- Сирці тієї ж теки `game/`: `dungeon.nh` (генерація), `combat.nh` (d20, шкода, XP), `bot.nh` (сходи, банк, ліміти, затримка кроку), `bot_eval.nh` (yield, помилки, 24 вбудовані функції), `main.nh` (стани екранів, 100 тіків за кадр).
- [Langjam Gamejam](https://itch.io/jam/langjamgamejam) — 14–21 грудня 2025, 33 роботи.
- YouTube: пошук «YENDOR olifog programming game».

## Непевне
- (?) Чи `/move/` у клітину монстра атакує (bump-to-attack): у прочитаних модулях виклику атаки не знайдено.
- (?) Поведінка монстрів (переслідують чи блукають), їхні HP і кістка шкоди — модуль `entity.nh` не читав; символ кобольда теж.
- (?) Звідки перше золото до апгрейду Gold Spawn — певно, базовий бонус поверху; формулу `calculate_floor_bonus` не бачив.
- (?) Підбір золота кроком на `$` і що стається з банком і переносним золотом після смерті.
- (?) Чи гра в першому проходженні справді забороняє ще не куплені конструкції і як (помилка, сірий синтаксис).
- (?) Лікування на сходах (`apply_stair_heal`) «якщо відкрито» — який апгрейд його відкриває.
- (?) Туман на мапі для людини, склад панелі бота (HP, золото, банк) і зміст чату / вхідних (`messages.nh`) — за назвами змінних, не за знімком екрана.
