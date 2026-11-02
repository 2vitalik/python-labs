---
title: Rogue
slug: rogue
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 1980
platforms: [Unix, MS-DOS, Amiga, Atari ST, Macintosh, C64, ZX Spectrum, web]
links:
  - {kind: docs, url: "https://docs-archive.freebsd.org/44doc/usd/30.rogue/paper.pdf", best: true, note: "A Guide to the Dungeons of Doom (Toy, Arnold) — 8 сторінок: екран, символи, всі команди, опції, рахунок"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rogue_(video_game)", note: "історія, генерація 3×3 кімнат, платформи"}
  - {kind: wiki, url: "https://www.roguebasin.com/index.php/Rogue", note: "RogueBasin: версії, сирці, онлайн-гра"}
  - {kind: wiki, url: "https://nethackwiki.com/wiki/Rogue_(game)", note: "таблиця монстрів A–Z з особливостями, списки предметів"}
  - {kind: play, url: "https://archive.org/details/ROGUE_PD", note: "DOS-версія в браузері"}
  - {kind: play, url: "http://rlgallery.org/", note: "Roguelike Gallery: кілька версій онлайн"}
  - {kind: other, url: "https://www.mobygames.com/game/1743", note: "MobyGames: порти і скріншоти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=rogue+1980+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-8dir, dungeon-generation, hp-damage, inventory, inventory-items, item-pickup, chase-player, random-walk, sequential-levels, player-death, round-currency, score-records, save-single-slot, console-render, status-panel, +fov-room-lit, +remembered-map, +item-identification, +hunger-clock, +permadeath, +search-hidden, +stairs-levels, +curse-item, +message-line, +run-command]
proposes: ["+trigger:revealed", "+trigger:hunger", "+cond:identified", "+cond:cursed", "+effect:identify", "+effect:steal", "+effect:drain", "+role:stairs", "+window:inventory-window", "+window:log-window", "+window:tombstone", "+ui:status-line", "+ui:more-prompt", "+feature:permadeath", "+feature:save-and-quit", "+axis:session"]
author: opus
date: 2026-11-02
---

# Rogue — @ спускається в Підземелля Долі по Амулет Йендора: одне життя, туман, невідомі зілля

## Суть
Гравець — `@` на ASCII-мапі; кожен поверх генерується заново: до девʼяти кімнат у сітці 3×3, зʼєднаних коридорами `#`. Треба спуститися вниз, знайти Амулет Йендора й піднятися назад живим; смерть остаточна, а сейв стирається при завантаженні. Ядро — керування ризиком у неповній інформації: невідомі зілля й сувої (назви кольорами й абракадаброю, свої в кожній партії), голод, пастки, монстри-літери, що сильніші з глибиною. Гра дала назву жанру «роглайк».

## Поле і час
- Екран терміналу 80×24: верхній рядок — повідомлення, нижній — статус, решта — мапа поверху. Камера статична (весь поверх на екрані).
- Поверх: до 3×3 «комірок», у кожній кімната, або лише вузол коридору (тупик, розвилка), на глибших — лабіринт. Кімнати бувають **освітлені** (входиш — бачиш усю й усіх) і **темні**; у коридорі видно лише 1 клітину навколо.
- Мапа **памʼятається**: досліджені стіни/двері/предмети лишаються на екрані; монстрів, що поза полем зору, стирає (виходиш із кімнати — її монстри зникають з екрана).
- Покроково: одна команда = один хід; монстри ходять після гравця, швидкі (haste) — двічі. Деякі дії (одягти/зняти обладунок) коштують кілька ходів.
- Глибина — шкала складності: що нижче, то сильніші монстри й кращі предмети; вгору (`<`) без Амулета не пускає.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Rogue `@` | player | Hp(max), Str(max), Arm, Exp lvl/pts, Gold, ситість | рух 8 напрямків; атакує, увійшовши в клітину монстра |
| Монстр `A`–`Z` | enemy | 26 видів, HP, рівень глибини | сплять або бродять; прокинувшись — переслідують; «злі» (mean) атакують без провокації |
| Aquator `A` | enemy | — | дотик іржавить обладунок (−Arm) |
| Bat `B` | enemy | літає | рух хаотичний |
| Ice monster `I` | enemy | — | заморожує гравця (пропуск ходів) |
| Leprechaun `L` | enemy | — | краде золото й зникає |
| Nymph `N` | enemy | — | краде магічний предмет з рюкзака й зникає |
| Medusa `M` | enemy | — | погляд плутає (confusion: рух у випадковий бік) |
| Rattlesnake `R` | enemy | — | укус знижує Str |
| Venus flytrap `F` | enemy | нерухома | тримає гравця; шкода росте щоходу |
| Vampire `V` / Wraith `W` | enemy | регенерація (V) | V — знімає max Hp; W — знімає рівень досвіду |
| Xeroc `X` | enemy | маскування | виглядає як предмет, доки не торкнешся |
| Phantom `P` | enemy | невидимий | видно лише з «see invisible» |
| Orc `O` | enemy | жадібний | біжить до золота |
| Dragon `D` | enemy | — | дихає полумʼям на відстань |
| Troll `T` / Griffin `G` | enemy | регенерація | відновлюють HP |
| Підлога кімнати `.` / коридор `#` | terrain | освітлена / темна | прохідні |
| Стіна `-` `|` | static | — | непрохідна |
| Двері `+` | gate | звичайні / таємні | прохід кімната↔коридор; таємні видно лише після пошуку `s` |
| Пастка `^` | hazard | тип, прихована | спрацьовує при вході; до виявлення не видно |
| Сходи `%` | static | — | `>` вниз; `<` вгору лише з Амулетом |
| Золото `*` | pickup | купка N | → Gold |
| Їжа `:` | pickup | раціон / фрукт | `e` — скидає голод |
| Зілля `!` | pickup | колір = тип (свій у кожній партії) | `q` — одноразовий ефект |
| Сувій `?` | pickup | «назва» = тип | `r` — одноразовий ефект |
| Жезл/палиця `/` | pickup | метал/дерево = тип; заряди | `z` + напрямок |
| Кільце `=` | pickup | камінь = тип | `P` — постійний ефект, прискорює голод |
| Зброя `)` | pickup | урон, зачарування ±N | `w` — у руку; стріли — `t` з лука |
| Обладунок `]` | pickup | Arm 2–7, ±N | `W` — надягти (кілька ходів) |
| Амулет Йендора `,` | pickup | на найглибшому поверсі | ціль гри; відкриває `<` |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move dir)` → ЯКЩО `free(cell)` → ТО `move(rogue, dir)`; ЯКЩО `occupied(cell, monster)` → ТО `custom: «атака: кидок на влучання → damage(weapon+Str)»`; стіна → `block`.
- КОЛИ `enter(rogue, lit_room)` → ТО `reveal(room)`; КОЛИ `leave(rogue, room)` → ТО `hide(monsters_in_room)`; у коридорі/темній кімнаті — `reveal(adjacent8)`.
- КОЛИ `contact(rogue, item)` → ЯКЩО `not input(m-prefix)` and `count(pack, <, limit)` → ТО `pickup`; повний рюкзак → `message(«pack too full»)`.
- КОЛИ `input(s)` → ТО `custom: «кожна сусідня клітина: з імовірністю p відкрити таємні двері/пастку»` → `set_cell(door|trap)`.
- КОЛИ `enter(rogue, trap)` → ТО залежно від типу: `custom: «люк — падіння на поверх нижче»`, `teleport(random)`, `damage(n)` (стріла/дротик, дротик ще −Str), `freeze(rogue, n)` (сонний газ, капкан); пастка стає видимою.
- КОЛИ `turn_end(player)` → ТО `counter(food, -1)` (кільця — швидше); КОЛИ `counter(food, <, t)` → ТО `set_state(rogue, hungry→weak→faint)`; faint → `stun(rogue, n)` випадково; 0 → `lose` («starvation»).
- КОЛИ `input(e)` → ЯКЩО `has(rogue, food)` → ТО `counter(food, +N)`, `take(rogue, food)`.
- КОЛИ `input(q|r)` → ТО ефект типу, `take(item)`; ЯКЩО `not identified(type)` → ТО `identify(type)` (усі такі ж предмети в цій партії відтепер з назвою).
- КОЛИ `input(c)` → ТО `custom: «call — гравець дає свою назву невідомому типу»`.
- КОЛИ `input(W|w|P)` → ЯКЩО `cursed(item)` → ТО `custom: «не можна зняти/замінити»`; обладунок зі скороченим Arm може бути проклятим.
- КОЛИ `contact(rogue, monster)` (монстр атакує) → ТО `damage(n)`; спецатаки: `custom: «іржа −Arm»` (A), `freeze` (I), `steal(gold)` + `teleport` (L), `steal(magic_item)` (N), `set_state(confused)` (M), `custom: «−Str»` (R), `drain(max_hp)` (V), `drain(xp_level)` (W).
- КОЛИ `hp_zero(monster)` → ТО `disappear_b`, `counter(exp, +n)`; КОЛИ `counter(exp, >=, threshold)` → ТО `custom: «Exp level +1, max Hp +»`.
- КОЛИ `turn_end` → ТО `heal(rogue, 1)` раз на кілька ходів (відпочинок `.`).
- КОЛИ `rng(p)` щоходу → ТО `spawn_at(wandering_monster, random_room)`.
- КОЛИ `input(>)` → ЯКЩО `cell(stairs)` → ТО `next_level` (новий генерований поверх); `input(<)` → ЯКЩО `has(amulet)` → ТО поверх вище, інакше `message`.
- КОЛИ `hp_zero(rogue)` → ТО `lose`, `window(tombstone)`, `currency(-10%)`; КОЛИ `input(Q)` → ТО `game_over` з усім золотом.
- Перемога: вийти на поверхню з Амулетом. Поразка: Hp = 0 або голод; смерть остаточна. Рахунок: золото (смерть — мінус 10 % «за похорон») + глибина; топ-10 на машині.

## Керування і ввід
- Клавіатура, одна-дві клавіші на дію. Рух `hjkl` + діагоналі `yubn` (vi-клавіші); `H`…`N` — біг до упору; `Ctrl+напрямок` — біг до «чогось цікавого»; DOS-версія — стрілки.
- Префікс-лічильник: `10s` — пошукати 10 разів; `Esc` скасовує.
- Префікс-команди з напрямком: `t` кинути, `z` зап жезла, `f` бити до смерті, `m` крок без підбору, `^` нагадати тип пастки.
- Предмети: `i`/`I` інвентар, `q r e w W T P R d c`; вибір предмета — буквою з рюкзака (`a`…).
- Службові: `?` довідка по клавішах, `/` «що це за символ», `s` пошук, `.` відпочинок, `,` підібрати, `<` `>` сходи, `o` опції, `Ctrl-R` перемалювати, `Ctrl-P` попередні повідомлення (до 5), `S` зберегти й вийти, `Q` здатися, `v` версія.

## Вікна, меню, HUD
- `game-screen` — мапа поверху (`console-render`) + `message-log` в один верхній рядок з `--More--` (чекає пробілу) + `stat-panel` в один нижній рядок: `Level`, `Gold`, `Hp: 12(12)`, `Str: 16(16)`, `Arm`, `Exp: 1/0`, стан голоду.
- `inventory-window` — список рюкзака з літерами `a)`…; з нього ж — вибір для `q r w …`.
- `help-window` — `?`: опис клавіші або повний список команд (`?*`).
- `settings-window` — `o`: сторінка опцій (jump, passgo, skull, name, fruit, file) — Enter/`-` гортають, `t`/`f` або текст змінюють.
- `log-window` — `Ctrl-P`: попередні повідомлення по одному (до 5).
- `tombstone` (`end-screen`) — ASCII-надгробок «REST IN PEACE» з імʼям, золотом і причиною смерті (опція `skull`); далі — `leaderboard` топ-10 (`rogue -s` — без гри).
- Переходи: запуск → `game-screen`; `i`/`?`/`o` → модальні екрани поверх мапи → назад будь-якою клавішею; смерть → надгробок → рекорди → вихід у shell.

## Фічі поза полем
- `mode-hardcore` за замовчуванням: сейв `S` — лише «зберегти й вийти»; відновлений файл видаляється (анти-save-scum) — `+feature:save-and-quit`.
- `leaderboard-local` топ-10 на машині; `custom-difficulty` нема; опції через `o` або змінну `ROGUEOPTS` (`remap-controls` нема).
- Кожна партія — новий світ (`seed` не показується); `session: endless`-подібна одна довга партія.
- Порти мали графічні тайли (Epyx/Amiga/Atari ST) — `theme-select` між ASCII і тайлами.

## Варіації й родичі
- Нащадки: Hack → NetHack (таблиця взаємодій усього з усім), Moria/Angband (глибина без повернення), Brogue (рідини й світло), DCSS (автодослідження), Mystery Dungeon (консоль).
- Попередники: Beneath Apple Manor (1978) — процедурні кімнати.
- Осі варіацій: **ідентифікація** (усе невідоме / частково / все відоме) · **голод** (нема / таймер / таймер+кільця) · **сейв** (нема / save-and-quit / вільний) · **FOV** (кімната цілком / тіньове лиття / радіус світла) · **повернення** (не можна / можна, поверх памʼятається / поверх перегенеровується).

## Цікавинки для курсу
- Генерація поверху «сітка 3×3 кімнат + коридори + таємні двері» — 🥉 (класичний алгоритм, гарантована звʼязність через сітку).
- Видимість «освітлена кімната цілком / темрява на 1 клітину» + памʼять мапи (два шари: бачу зараз / бачив) — 📎 (простіше за shadowcasting, але вже fog-of-war).
- Ідентифікація: перемішати назви кольорів/титулів з типами на старті партії; спожите — розкриває тип для всіх таких — 📎 (словник `type → label`, дуже елегантна механіка невідомості).
- Голод-таймер з прискоренням від кілець і станами hungry/weak/faint — 🌱.
- Спецатаки монстрів (крадіжка+телепорт, іржа, заморозка, злив рівня) як таблиця «літера → ефект» — 🥉 (data-driven вороги).
- Анти-save-scum: сейв видаляється при завантаженні — 🌱, але показовий приклад рішення дизайну через файл.
- Командний рядок з лічильником і префіксами (`10s`, `th`, `fh`) — 📎 (парсер вводу).

## Мапа на каталог
- Є: `move-8dir` · `move-by-input` · `dungeon-generation` (3×3 кімнат) · `hp-damage` · `inventory` + `inventory-items` + `inventory-limit` · `item-pickup` · `chase-player` (прокинуті монстри) · `random-walk` (кажан) · `sequential-levels` (поверхи) · `player-death` · `round-currency` (золото) · `score-records` + `leaderboard` · `save-single-slot` · `console-render` · `status-panel` · `keyboard-controls` · `game-screen` · `help-window` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+fov-room-lit` «Видимість: кімната цілком / 1 клітина в темряві» · entities/visibility · 📎 · слот {dark_radius}.
  - `+remembered-map` «Памʼять мапи: бачене лишається, монстри — ні» · interface/render · 📎.
  - `+item-identification` «Невідомі типи предметів з випадковими назвами» · entities/state · 📎 · слоти {classes, auto_on_use}.
  - `+hunger-clock` «Голод-таймер зі станами» · entities/state · 🌱 · слоти {max, rate, states}.
  - `+permadeath` «Одне життя, сейв стирається» · rules/lose · 🌱.
  - `+search-hidden` «Пошук прихованого (двері, пастки) з імовірністю» · entities/interact · 🌱 · слот {p}.
  - `+stairs-levels` «Сходи між поверхами, вгору — за умовою» · rules/progress · 🌱.
  - `+curse-item` «Проклятий предмет не знімається» · entities/state · 🌱.
  - `+message-line` «Рядок повідомлень з --More--» · interface/hud · 🌱.
  - `+run-command` «Біг до упору / до цікавого» · interface/input · 📎.
  - `+repeat-count` «Числовий префікс-повтор команди» · interface/input · 🌱.

## Пропозиції до словників
- `+trigger:revealed` — клітину/кімнату вперше відкрито (освітлення кімнати, відкриття таємних дверей).
- `+trigger:hunger` — лічильник ситості перейшов поріг (hungry/weak/faint); можна як `counter(food, <, t)`, але порогів кілька.
- `+cond:identified` — тип предмета відомий гравцю; `+cond:cursed` — предмет проклятий.
- `+effect:identify` — розкрити тип для всіх предметів цього виду; `+effect:steal` — ворог забирає предмет/золото і тікає; `+effect:drain` — зняти максимум (Hp, рівень).
- `+role:stairs` — перехід між поверхами (відрізняти від `static`-виходу: двосторонній, з умовою).
- `+window:inventory-window` — рюкзак із літерами; `+window:log-window` — попередні повідомлення; `+window:tombstone` — надгробок як `end-screen` з причиною смерті.
- `+ui:status-line` — однорядковий статус (консоль); `+ui:more-prompt` — `--More--`, черга повідомлень з підтвердженням.
- `+feature:permadeath`, `+feature:save-and-quit`.
- `+axis:session` — тут `run` (одна партія = забіг до смерті) — бракує значення поряд з `level`/`endless`/`match`.

## Джерела
- ⭐ [A Guide to the Dungeons of Doom](https://docs-archive.freebsd.org/44doc/usd/30.rogue/paper.pdf) — офіційний посібник BSD-версії: статус-рядок, символи, усі команди, обладунки, опції, рахунок.
- [Wikipedia: Rogue](https://en.wikipedia.org/wiki/Rogue_(video_game)) — генерація 3×3, ідентифікація, сейв, платформи.
- [NetHackWiki: Rogue](https://nethackwiki.com/wiki/Rogue_(game)) — монстри A–Z з особливостями, списки зіль/сувоїв/кілець/жезлів.
- [RogueBasin: Rogue](https://www.roguebasin.com/index.php/Rogue) — версії, сирці, онлайн-гра.
- [Internet Archive: Rogue (DOS)](https://archive.org/details/ROGUE_PD) — грати в браузері.
- YouTube: пошук «rogue 1980 gameplay».

## Непевне
- (?) Амулет на 26-му поверсі — так у Wikipedia лише як результат Rog-O-Matic 1983; у версіях може відрізнятися.
- (?) Типи пасток (люк, стріла, сонний газ, капкан, телепорт, отруйний дротик, у 5.x ще іржава) і стани голоду Hungry/Weak/Faint у статус-рядку — з памʼяті, у посібнику лише «faint → starvation».
- (?) Таблиця монстрів NetHackWiki частково «поїхала» при розборі — окремі особливості (Medusa, Kestrel) варто звірити.
- (?) Символ сходів `%` і їжі `:` — за посібником BSD; у DOS/Epyx-версіях символи інші (тайли/CP437). Символ Амулета `,` — з памʼяті.
