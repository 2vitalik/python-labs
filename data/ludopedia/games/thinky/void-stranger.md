---
title: Void Stranger
slug: void-stranger
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: none
  goal: state
year: 2023
platforms: [PC (Windows)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Void_Stranger", note: "огляд: жезл, 200+ кімнат, саранові ідоли, розробка"}
  - {kind: fandom, url: "https://voidstranger.miraheze.org/wiki/Enemies", best: true, note: "Miraheze-вікі: усі вороги з точними правилами руху й способами прибрати"}
  - {kind: fandom, url: "https://voidstranger.miraheze.org/wiki/Tiles", note: "усі типи плиток: скло, перемикачі, бомби, копі-плитка, смертельна"}
  - {kind: fandom, url: "https://voidstranger.miraheze.org/wiki/Void_Rod", note: "правила жезла"}
  - {kind: fandom, url: "https://voidstranger.miraheze.org/wiki/Statues", note: "статуї: Lover, Slower, Watcher, Greeder…"}
  - {kind: steam, url: "https://store.steampowered.com/app/2121980/Void_Stranger/"}
  - {kind: other, url: "https://system-erasure.itch.io/void-stranger", note: "itch.io, автосейв між кімнатами"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Void+Stranger+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, push-object, impassable-cells, reach-exit, touch-death, environment-death, player-death, item-pickup, inventory-limit, chain-detonation, sequential-levels, save-autosave, keyboard-controls, +lift-place-tile, +crumble-floor, +turn-when-blocked, +line-of-sight-attack, +charge-on-sight, +mimic-copy, +follower-chain, +crush-by-push, +hold-all-switches, +lethal-cell, +action-budget, +extra-life-pickup, +secret-pattern-input]
proposes: ["+trigger:input", "+trigger:enter", "+trigger:leave", "+trigger:line_of_sight", "+cond:free", "+cond:carrying", "+effect:lift_tile", "+effect:place_tile", "+effect:set_cell", "+effect:mirror_input", "+effect:lives", "+effect:respawn", "+role:hazard", "+role:switch", "+role:gate", "+ui:held-tile", "+ui:brane-number", "+window:brand-input", "+feature:brand-code", "+feature:step-confirm", "+card:lift-place-tile"]
author: opus
date: 2026-11-02
---

# Void Stranger — підлога як ресурс: жезлом піднімаєш плитку й кладеш у прірву деінде

## Суть
Сіра (Gray) спускається підземеллям із 200+ кімнат-«бран» (B001, B002…); у кожній треба дійти до сходів. Головний інструмент — Void Rod: він **піднімає плитку підлоги** перед героїнею (лишаючи прірву) і **кладе її** в прірву перед нею; за раз несеш одну плитку. Вороги ходять жорсткими автоматами після кожного ходу, а вбити їх можна лише середовищем: прибравши плитку під ними, заманивши в прірву чи присунувши статую. Гра покроково-детермінована, як DROD, але поле тут — не тло, а матеріал, який ти переставляєш.

## Поле і час
- Кімната = один екран квадратної сітки з краєм-прірвою; підлога — окремі плитки, між ними порожнеча (Empty tile = яма).
- Шари: плитка (звичайна, скло, перемикач, бомба/вибух, копі, смертельна, сходи) + сутність (героїня, ворог, статуя, скриня).
- Покроково: хід = крок у 4 напрямки або одне використання жезла; потім ходять вороги. До отримання жезла (B002) рух безперервний, з жезлом — клітинний.
- Вміст жезла скидається при переході між кімнатами; гра автозберігається між кімнатами.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Gray | player | саранові ідоли (≈ життя), жезл, предмети | крок 4 напрямки, штовхає статуї; жезл: підняти / покласти плитку попереду |
| Void Rod | — | місткість 1 плитка | підняти будь-яку тверду плитку попереду; покласти — лише на Empty попереду |
| Плитка | terrain | — | звичайна підлога; її можна перенести |
| Порожнеча (Empty, яма) | hazard | — | хто впав — прибраний; крок у яму вимагає підтвердження повторним натиском |
| Скло | terrain | — | руйнується (→ яма), коли сутність з неї сходить; вороги не можуть іти слідом |
| Перемикач | switch | ≤ 8 на кімнату | натиснутий, поки на ньому будь-яка сутність |
| Сходи | static | — | вихід у наступну брану |
| Замкнені сходи | gate | — | відчинені, лише коли **всі** перемикачі натиснуті одночасно |
| Бомба-плитка | terrain | — | сутність ступила → стає вибуховою |
| Вибухова плитка | hazard | мережа зʼєднаних | сутність ступила → уся мережа детонує, під нею ями |
| Копі-плитка (shade's sign) | spawner | — | героїня зійшла → зʼявляється Тінь, що йде слідом |
| Смертельна плитка | hazard | — | будь-хто, хто ступив, гине від блискавки; плитка ціла |
| Скриня | container | ідол або предмет | відкривається дією; дає саранового ідола (1) чи предмет |
| Пʼявка (Leech) | enemy | напрям ←/→ | ходить горизонтально; перед перешкодою/ямою зупиняється і хід розвертається |
| Опариш (Maggot) | enemy | напрям ↑/↓ | те саме вертикально |
| Посмішка (Smile) | enemy | — | побачивши героїню по рядку/стовпцю, іде до неї — навіть у яму |
| Бобер (Beaver) | enemy | — | побачивши — мчить у тому напрямку до упору, навіть якщо героїня зійшла; хід на «перезарядку» |
| Око (Eye) | enemy | — | нерухоме, смертельне на дотик; само в яму не падає |
| Мімік ×3 | enemy | білий / сірий / чорний | рухається за **вводом** гравця: білий копіює вертикаль і дзеркалить горизонталь, сірий — навпаки, чорний дзеркалить обидві |
| Октаедр | enemy | — | переслідує по шляху; сусідство з героїнею = смерть; при рівних шляхах Up > Down > Left > Right |
| Тінь (Shade) | ally/hazard | ланцюг | йде слідом за героїнею; смерть тіні = смерть героїні |
| Статуя Lover | object | — | штовхається; у яму → стає звичайною плиткою |
| Статуя Slower | object | — | після першого поштовху стає нерухомою |
| Статуя Watcher | object | — | кожне використання жезла запалює одну; усі запалені → блискавка вбиває героїню |
| Статуя Greeder | hazard | — | героїня на її рядку/стовпці без укриття → смерть |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` і там тверда плитка → ТО `move(gray, dir)`; якщо там статуя і за нею вільно → `push`; якщо там яма → `custom: «крок завис — повторний натиск падає, протилежний скасовує»`.
- КОЛИ `input(rod)` → ЯКЩО `not carrying` і попереду тверда плитка → ТО `lift_tile(cell_ahead)`, `set_cell(empty)`; ЯКЩО `carrying` і попереду Empty → ТО `place_tile(cell_ahead)`; інакше нічого (?). Використання = хід.
- КОЛИ `leave(room)` → ТО `custom: «вміст жезла зникає»`.
- КОЛИ `turn_end(player)` → ТО вороги ходять: пʼявка/опариш — `move` по своїй осі, `blocked` або яма попереду → `face(reverse)` за хід; Smile — `line_of_sight` → `move` до героїні; Beaver — `line_of_sight` → `slide(dir)` до упору; мімік — `mirror_input` за своїм типом; Октаедр — `chase-bfs`.
- КОЛИ `contact(enemy, gray)` → ТО `lose`; КОЛИ `enter(gray, empty)` → ТО `lose`.
- КОЛИ `lose` → ЯКЩО `has(gray, locust) > 0` → ТО `lives(-1)`, `respawn` на початку кімнати; інакше — вибір: почати гру спочатку або продовжити з нескінченними спробами.
- КОЛИ `enter(enemy|object, empty)` → ТО `disappear_a` (ворог прибраний); Lover → `set_cell(tile)`.
- КОЛИ `push(object)` в клітину ворога → ТО ворог `disappear` (розчавлений).
- КОЛИ два вороги йдуть в одну клітину → ТО обидва `disappear_both`.
- КОЛИ `leave(any, glass)` → ТО `set_cell(empty)`.
- КОЛИ `enter(any, bomb_tile)` → ТО `transform(explo_tile)`; КОЛИ `enter(any, explo_tile)` → ТО `chain-detonation`: уся звʼязна мережа → ями, хто стоїть — падає.
- КОЛИ `enter(any, death_tile)` → ТО `disappear_a`.
- КОЛИ `leave(gray, copy_tile)` → ТО `spawn(shade)` у кінець ланцюга; КОЛИ `died(shade)` → ТО `lose`.
- КОЛИ `input(rod)` і в брані є Watchers → ТО `set_state(next_watcher, lit)`; `count(unlit, ==, 0)` → ТО `lose`.
- КОЛИ `line_of_sight(greeder, gray)` → ТО `lose`.
- КОЛИ `all switches occupied` → ТО замкнені сходи `set_state(open)`; КОЛИ `contact(gray, stairs)` → ТО `next_level`.
- КОЛИ `contact(gray, chest)` → ТО `pickup(locust | burden)`.
- Перемога кімнати: дійти до сходів. Поразка: дотик ворога, падіння, блискавка, вибух; «життя» — саранові ідоли. Рахунку нема.

## Керування і ввід
- Стрілки — крок (з жезлом: строго по клітинах); дія (Z/пробіл (?)) — використати жезл / відкрити скриню / говорити з NPC; з предметом Void Sword — удар.
- Undo нема; рестарт кімнати — фактично через смерть (падіння).
- Крок у яму — двоетапний: перший натиск «зависає», другий падає.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Продовжити, Нова гра, Налаштування.
- `brand-input` (custom): на старті забігу гравець «гравіює» власне клеймо — малюнок 6×6 з чорних/білих клітин; деякі клейма вмикають спецрежими.
- `game-screen`: кімната + HUD: `brane-number` (B###), `lives` — кількість саранових ідолів, `held-tile` — іконка плитки біля іконки жезла.
- `dialogue-window` — розмови з NPC і статуями (монохромні діалоги).
- `pause-menu`: продовжити, налаштування (`settings-window`: звук, керування, вікно), вихід.
- Переходи: main-menu → brand-input → game-screen; game-screen → (сходи) → наступна брана; game-screen → (смерть без ідолів) → вибір «спочатку / продовжити».

## Фічі поза полем
- `autosave` між кімнатами; `levels-sequential` (брани по черзі) зі схованими гілками (ями-шорткати, приховані брани).
- Лічильник ідолів як ресурс-«життя», що переноситься між кімнатами; скрині дають ідолів.
- `brand-code` — введений на старті 6×6-патерн як секретний код режиму; кімнати-клейма (6×6), де патерн викладають переставленими плитками.
- Нема undo, підказок, вибору рівня; монохромна графіка, chiptune.
- Предмети-«тягарі»: крила (перелетіти одну яму), меч (атакувати ворогів, крім міміків і тіней), памʼять (читати знаки).

## Варіації й родичі
- Родичі: DROD (детерміновані вороги після кожного ходу), Sokoban (штовхання статуй), Bonfire Peaks / Stephen's Sausage Roll (поле як матеріал), Chip's Challenge (типи плиток), Hoplite.
- Осі варіацій **маніпуляції полем**: що можна брати — плитку / обʼєкт / стіну; скільки нести — 1 / стек (Endless Rod: LIFO без ліміту) / ∞; де класти — лише в яму / будь-куди.
- Осі ворогів: по осі з розворотом (пʼявка/опариш) / на погляд (Smile, Beaver) / дзеркальний ввід (міміки) / шлях (Октаедр) — та сама «сімʼя автоматів», що в DROD і Chip's.

## Цікавинки для курсу
- Жезл: підняти плитку → яма, покласти в яму → підлога; місткість 1 — 🥉 (поле стає змінним ресурсом).
- Скло, що руйнується після сходження, і наслідок «вороги не пройдуть слідом» — 📎.
- Міміки трьох типів: рух за вводом з дзеркаленням осей — 📎 за кожного, 🥉 за трійку.
- Бомба → вибухова мережа, що детонує звʼязною компонентою (flood fill) — 🥉.
- Перемикачі «всі натиснуті одночасно» + вороги як тягар на кнопці — 🥉.
- Тіні: ланцюг-послідовник, смерть якого = смерть гравця — 🥉.
- Watchers: бюджет дій жезла на кімнату — 📎.
- Клеймо 6×6 як секретний код старту — 📎.

## Мапа на каталог
- Є: `move-4dir` · `push-object` (статуї) · `impassable-cells` · `reach-exit` (сходи) · `touch-death` · `environment-death` (ями, блискавка, вибух) · `player-death` (ідоли як життя) · `item-pickup` (скрині) · `inventory-limit` (жезл на 1 плитку) · `chain-detonation` (вибухова мережа) · `sequential-levels` · `save-autosave` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+lift-place-tile` «Підняти й покласти плитку підлоги» · entities/interact · 🥉 · слот {capacity: 1|stack}.
  - `+crumble-floor` «Підлога руйнується, коли з неї зійшли» · entities/interact · 📎 (також люки DROD).
  - `+turn-when-blocked` (є з Chip's) — пʼявка/опариш розвертаються, витрачаючи хід.
  - `+line-of-sight-attack` (є з Lolo) — Smile, Greeder.
  - `+charge-on-sight` «Ривок до упору на погляд» · entities/move · 📎 — Beaver.
  - `+mimic-copy` «Двійник повторює ввід» · entities/move · 🥉 · слот {mirror: none|x|y|xy} (також DROD).
  - `+follower-chain` «Послідовники-ланцюг» · entities/move · 🥉 — тіні (схоже на `body-queue`, але з окремих сутностей).
  - `+crush-by-push` «Розчавити ворога присунутим обʼєктом» · entities/combat · 📎.
  - `+hold-all-switches` «Усі перемикачі одночасно» · entities/interact · 📎.
  - `+lethal-cell` «Клітина, що вбиває будь-кого» · entities/death · 🌱.
  - `+action-budget` «Ліміт дій інструментом у кімнаті» · game-logic/lose · 📎 — Watchers.
  - `+extra-life-pickup` «Підбирання життя» · entities/interact · 🌱.
  - `+secret-pattern-input` «Секретний патерн-код на старті» · game-logic/difficulty · 📎.

## Пропозиції до словників
- `+effect:lift_tile` / `+effect:place_tile` — забрати плитку в інвентар (клітина → Empty) / покласти з інвентаря (Empty → плитка); спеціалізація `set_cell` + `take`/`give`.
- `+cond:carrying` — в інструменті є плитка/предмет.
- `+ui:held-tile` — іконка того, що несе інструмент; `+ui:brane-number` — номер поверху/кімнати як головний індикатор прогресу (або ⏳ `level-number`).
- `+window:brand-input` — екран малювання клейма/коду 6×6 на старті.
- `+feature:brand-code` — патерн-код, що вмикає режими; `+feature:step-confirm` — небезпечний крок вимагає повторного натиску.
- `+card:lift-place-tile` — див. «Мапа на каталог».
- ⏳-слова, вжиті тут: `input`, `enter`, `leave`, `line_of_sight`, `free`, `set_cell`, `mirror_input`, `lives`, `respawn`, `hazard`, `switch`, `gate`.

## Джерела
- ⭐ [Miraheze: Enemies](https://voidstranger.miraheze.org/wiki/Enemies) — усі вороги з правилами руху, способи прибрати (яма, присунута статуя, смертельна плитка, зіткнення двох).
- [Miraheze: Tiles](https://voidstranger.miraheze.org/wiki/Tiles) — 10 типів плиток із взаємодіями; [Void Rod](https://voidstranger.miraheze.org/wiki/Void_Rod) — підняти/покласти, скидання між кімнатами; [Statues](https://voidstranger.miraheze.org/wiki/Statues); [Locust idol](https://voidstranger.miraheze.org/wiki/Locust_idol); [Burdens](https://voidstranger.miraheze.org/wiki/Burdens); [Brand](https://voidstranger.miraheze.org/wiki/Brand).
- [Wikipedia](https://en.wikipedia.org/wiki/Void_Stranger) — огляд, 200+ кімнат, ідоли рятують від смерті, System Erasure, GameMaker.
- [Steam](https://store.steampowered.com/app/2121980/Void_Stranger/) · [itch.io](https://system-erasure.itch.io/void-stranger) — «every step counts», автосейв між кімнатами.

## Непевне
- (?) Чи можна підняти плитку, на якій стоїть ворог/статуя, — вікі прямо не каже (найімовірніше, ні).
- (?) Розкладка клавіш дії та чи є окремий рестарт кімнати в меню.
- (?) Розмір кімнати в клітинах (один екран, ~14×8 (?)).
- (?) У HUD Void Stranger, за згадками на вікі, є значення HP і лічильники, що грають роль у секретах; їх механіку свідомо не описано (спойлери) і не перевірено.
- (?) Сірі/білі міміки — яку вісь копіюють — взято з вікі, але легко переплутати у грі.
