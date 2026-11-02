---
title: "Deadly Rooms of Death (DROD: King Dugan's Dungeon)"
slug: drod
family: thinky
also: [roguelike]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: none
  goal: state
year: 1996
platforms: [PC (Windows/Linux/Mac), web (Flash, 2012)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Deadly_Rooms_of_Death", best: true, note: "поле 38×32, хід/поворот меча, детермінізм, історія версій і серії"}
  - {kind: official, url: "https://forum.caravelgames.com/viewsitepage.php?id=90294", note: "сайт DROD (Caravel Games): демо, holds, гайди"}
  - {kind: other, url: "https://forum.caravelgames.com/viewsiteboard.php?b=59", note: "бестіарій: сторінка на кожного монстра з точними правилами руху"}
  - {kind: other, url: "https://forum.caravelgames.com/site/roach", note: "тарган: вибір клітини, відкат на вісь при упорі, «мозкова» поведінка"}
  - {kind: other, url: "https://forum.caravelgames.com/site/goblins", note: "гоблін: оцінка клітин балами, уникнення меча"}
  - {kind: other, url: "https://forum.caravelgames.com/site/guide", note: "гайд новачка: кімната = пазл, кімнати без памʼяті"}
  - {kind: play, url: "http://caravelgames.com/Articles/Games_2/FlashDROD/KDDL.html", note: "Flash-версія King Dugan's Dungeon (потрібен Flash-емулятор)"}
  - {kind: other, url: "http://forum.caravelgames.com/holds.php", note: "holds — 400+ рівнів спільноти"}
  - {kind: other, url: "https://www.wurb.com/stack/archives/127", note: "есей «DROD: Solving Puzzles»"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=DROD", note: "пошук; серія в Steam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=DROD+King+Dugan%27s+Dungeon+gameplay", note: "пошук; геймплей"}
stage: v2
coverage: 75
mechanics: [move-8dir, keyboard-controls, chase-player, chase-greedy, chase-bfs, spawn-schedule, impassable-cells, destroy-all-enemies, touch-death, player-death, checkpoint, key-and-door, sequential-levels, in-game-editor, level-exchange, replay, state-as-data, minimap-radar, help-window, body-queue, +sword-cell, +rotate-as-move, +flee-player, +wake-on-event, +score-field-move, +pack-behaviour, +blob-growth, +shrink-to-death, +button-toggle, +clear-unlocks, +crumble-floor, +one-way-cell, +hint-tile, +room-memory, +mimic-copy, +undo-redo, +movement-order]
proposes: ["+trigger:input", "+trigger:turn_end", "+trigger:line_of_sight", "+trigger:all_gone", "+trigger:leave", "+trigger:timer", "+cond:facing", "+cond:free", "+cond:occupied", "+cond:sword_at", "+effect:rotate", "+effect:face", "+effect:set_state", "+effect:set_cell", "+effect:spawn_at", "+effect:shrink", "+effect:checkpoint", "+effect:message", "+role:weapon", "+role:gate", "+role:switch", "+role:spawner", "+role:hazard", "+window:map-window", "+window:replay-window", "+window:editor-window", "+window:hold-select", "+ui:sword-direction", "+feature:demo-recording", "+feature:room-reset-on-leave", "+card:movement-order", "+axis:undo"]
author: opus
date: 2026-11-02
---

# DROD — повністю детермінований данжен: меч займає сусідню клітину, кожен монстр ходить за своєю формулою

## Суть
Беетро, «винищувач підземель», проходить рівні з кімнат 38×32; кімната вважається підкореною (conquered), коли в ній не лишилось монстрів. Його єдина зброя — «Really Big Sword», що завжди займає **сусідню клітину в напрямку погляду**: поворот меча на 45° — це повноцінний хід, а монстр гине, щойно меч увійде в його клітину. Кожен тип монстра ходить після гравця за жорсткою детермінованою формулою, тож кімната — шаховий етюд у реальних клітинах: випадковості нема, усе можна передбачити. Гра — еталон «детермінованих монстрів як пазла» і родоначальник thinky-підземель.

## Поле і час
- Кімната 38×32 клітини, один екран; рівень = граф кімнат, сусідні по краях екрана; між кімнатами ходять через край. Рівні зʼєднані сходами (exit stairs); у King Dugan's Dungeon 25 рівнів (?).
- Шари: підлога (тип: звичайна, стіна, яма, пастка-люк, стрілка, сувій, чекпойнт) + обʼєкт (двері, сфера, смола) + монстр + меч (як окрема «клітина-сутність» Беетро).
- Хід = одна дія гравця (крок у 8 напрямках / поворот / очікування); потім **усі монстри ходять по черзі в порядку створення** («movement order», видно в інфо клітини).
- Деякі події — за лічильником ходів: королева тарганів кладе яйця кожні 30 ходів, смола росте кожні 30 ходів, яйце вилуплюється за 5 ходів, змія міняє бажану вісь кожні 5 ходів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Беетро | player | напрям погляду (8) | крок у 8 напрямків на вільну клітину / поворот меча ±45° / чекати |
| Меч (Really Big Sword) | weapon | клітина = Беетро + напрям | убиває монстра, у клітину якого входить; б'є сфери; монстри в клітину меча не заходять |
| Тарган (roach) | enemy | — | крок у сусідню з 8 клітину, найближчу до Беетро; діагональ заблокована → пробує вертикальну, потім горизонтальну складову; ортогональ заблокована → стоїть |
| Яйце таргана | enemy | 5 ходів | лежить; вилуплюється тарганом; вбивається мечем |
| Королева тарганів | enemy + spawner | кожні 30 ходів | тікає (крок, протилежний «найближчому до Беетро»); кладе до 8 яєць на вільні сусідні клітини в порядку NW, N, NE, W, E, SW, S, SE |
| Зле око (evil eye) | enemy | напрям погляду | спить; прокидається, коли Беетро стає на промінь у напрямку погляду (стіни/двері блокують, монстри — ні); далі ходить як тарган |
| Гоблін | enemy | — | оцінює 9 варіантів (8 сусідів + стояти): клітина Беетро = 50000, біля меча = 5000, інші = 5000 − 100·відстань (евклідова); при рівності — NW, N, NE, W, стояти, E, SW, S, SE |
| Wraithwing | enemy | літає | над ямами й водою; X = Чебишевська відстань; X > 5 — атакує як тарган; X ≤ 5 — атакує лише якщо інший wraithwing на схожій відстані (\|X−Y\| < 3) і не поруч (Z > 2), інакше X = 5 — завмирає, X < 5 — тікає як королева |
| Смола (tar) | object | маса клітин | непрохідна; розрізається мечем по краю маси, кути не ріжуться |
| Смоляна мати (tar mother) | enemy + spawner | кожні 30 ходів | маса смоли розростається; де не виходить ділянки шириною ≥ 2 — народжуються смолянята |
| Смоляня (tar baby) | enemy | — | ходить як тарган |
| Змія (serpent) | enemy | довжина N клітин | лише 4 напрямки; голова — до Беетро, якщо він прямо попереду/позаду, інакше бажана вісь змінюється кожні 5 ходів; заблокована на всі боки — коротшає на 1; мечем невразлива; гине, скоротившись до нуля |
| Мозок (brain) | enemy | нерухомий | доки живий, монстри з досяжним шляхом ідуть **найкоротшим шляхом** (BFS) до Беетро замість жадібного кроку; ворог для зачистки |
| Мімік | ally | з зілля | повторює кожен хід і поворот Беетро зі своїм мечем, убиває ним монстрів (?) |
| Стіна | static | — | непрохідна |
| Яма (pit) | hazard | — | непрохідна для ходячих; літаючі пролітають |
| Люк (trapdoor) | terrain | — | коли Беетро зійшов з нього — провалюється, стає ямою |
| Стрілка (force arrow) | terrain | напрям | не можна рухатися проти стрілки (ні на неї, ні з неї) (?) |
| Сувій (scroll) | terrain | текст | наступ — текст у бічній панелі |
| Чекпойнт | terrain | — | наступ — зберегти стан кімнати; смерть повертає сюди |
| Сфера (orb) | switch | список дверей + дія open/close/toggle | удар мечем → дія над привʼязаними жовтими дверима |
| Жовті двері | gate | open/closed | перемикаються сферами |
| Зелені двері | gate | — | відчиняються, коли кімнату підкорено (монстрів 0) |
| Сині двері | gate | — | відчиняються, коли пройдено рівень (усі обовʼязкові кімнати) (?) |
| Червоні двері | gate | — | відчиняються, коли в кімнаті провалились усі люки (?) |
| Сходи виходу | static | — | перехід на наступний рівень |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(step, dir8)` → ЯКЩО `free(cell)` і нема стрілки проти → ТО `move(beethro, dir)`; меч переміщується разом (лишаючись у напрямку погляду); інакше `block` (хід не витрачається (?)).
- КОЛИ `input(rotate, cw|ccw)` → ТО `rotate(sword, ±45°)`; меч проходить одну нову клітину.
- КОЛИ `input(wait)` → ТО хід минає без руху.
- КОЛИ `sword_at(cell)` стає новим → ЯКЩО `occupied(cell, monster)` і монстр вразливий → ТО `disappear_b`; ЯКЩО `occupied(cell, orb)` → ТО `set_state(linked_doors, open|close|toggle)`; ЯКЩО край смоли → ТО `set_cell(floor)`.
- КОЛИ `turn_end(player)` → ТО кожен монстр у порядку створення робить свій крок за формулою виду (таблиця вище); монстри не заходять у клітину меча, стіни, ями (крім літаючих), двері, сфери.
- КОЛИ `contact(monster, beethro)` → ТО `lose`: смерть → кімната з входу або з останнього чекпойнта.
- КОЛИ `line_of_sight(eye, beethro)` уздовж погляду ока → ТО `set_state(eye, awake)`.
- КОЛИ `timer(30)` для королеви → ТО `spawn_at(egg, free_neighbours)`; КОЛИ `timer(5)` яйця → ТО `transform(roach)`.
- КОЛИ `timer(30)` для смоляної матері → ТО `custom: «смола розростається на сусідні клітини; вузькі місця дають смолянят»`.
- КОЛИ `blocked(serpent)` на всі 4 боки → ТО `shrink(serpent, 1)`; довжина 0 → `disappear_a`.
- КОЛИ `count(brain, >, 0)` → ТО монстри з досяжним шляхом обирають крок за BFS-мапою відстаней (стіни, смола, сфери — перешкоди; інші монстри — ні).
- КОЛИ `leave(beethro, trapdoor)` → ТО `set_cell(pit)`; КОЛИ всі люки кімнати провалились → ТО червоні двері `set_state(open)` (?).
- КОЛИ `enter(beethro, scroll)` → ТО `message(text)`; КОЛИ `enter(beethro, checkpoint)` → ТО `checkpoint`.
- КОЛИ `all_gone(monsters)` у кімнаті → ТО кімната conquered, зелені двері `set_state(open)`; стан кімнати зберігається назавжди.
- КОЛИ `leave(beethro, room)` → ЯКЩО кімнату не підкорено → ТО кімната повертається у початковий стан («кімнати без памʼяті»).
- КОЛИ всі обовʼязкові кімнати рівня conquered → ТО рівень пройдено, сині двері `set_state(open)` (?); `contact(beethro, stairs)` → `next_level`.
- Перемога: зачистити кімнату → рівень → підземелля. Поразка: лише смерть від дотику монстра (лічильника життів нема — повтор з чекпойнта). Рахунку нема; змагання спільноти — мінімум ходів у кімнаті (?).

## Керування і ввід
- Нумпад 1–9: 8 напрямків кроку, 5 — чекати; Q / W — поворот меча проти / за годинниковою стрілкою (перепризначувані).
- Undo останнього ходу (Backspace у пізніх версіях) і Restart кімнати / з чекпойнта (?).
- Мишею: ПКМ на клітині — інфо (елементи, порядок ходу монстра, довжина змії); ЛКМ на сфері/плиті — підсвітка привʼязаних дверей (зелений = відкриває, бурштиновий = перемикає, червоний = закриває).
- F1 — довідка, F6 — демо (експорт/імпорт розвʼязків).

## Вікна, меню, HUD
- `splash-screen` → `main-menu` (Title): Продовжити, Нова гра, Restore, Вибрати hold (`hold-select`), Build (`editor-window`), Налаштування, Довідка, Вихід.
- `game-screen`: кімната 38×32 + бічна панель: `minimap` рівня (підкорені кімнати іншим кольором), `level-number`/назва рівня й позиція кімнати, панель тексту сувоїв (`objective-text`-подібна), портрет Беетро; `sword-direction` — меч видно на полі.
- `map-window` — карта рівня з відвіданими/підкореними кімнатами.
- Restore (`save-slots`-подібний): повернення до початку будь-якої відвіданої кімнати або чекпойнта.
- `replay-window` (демо, F6): записані розвʼязки кімнат, експорт/імпорт/завантаження.
- `settings-window`: керування (`options-controls`), звук, графіка.
- `help-window` (F1): керування й опис усіх монстрів і елементів — фактично `codex-window`.
- `editor-window` (з DROD: Architects' Edition, 2003): палітра елементів, кімнати, звʼязки сфера→двері, тестування.
- `end-screen`-діалоги: смерть («Беетро загинув» → повтор), кінець рівня, фінал.
- Переходи: Title → game-screen; game-screen → (смерть) → та сама кімната/чекпойнт; game-screen ↔ map-window; Title → hold-select → game-screen іншого hold; Title → editor-window → плейтест.

## Фічі поза полем
- `level-editor` + `level-sharing` (holds на сайті Caravel, 400+), `user-levels-browser` у пізніх версіях (CaravelNet) (?).
- `replay` / `demo-recording` — розвʼязки кімнат зберігаються як послідовність ходів (детермінізм робить це тривіальним), експорт/імпорт.
- `checkpoint`-збереження всередині кімнати; `autosave` підкорених кімнат; `save-slots` через Restore.
- `undo` (обмежено/∞ — залежить від версії (?)), `restart-level` (кімнати).
- `codex` у довідці; `tutorial` у DROD 2–4; `remap-controls`.
- Відкритий код (2000, MPL 1.1) — рідкісна для курсу можливість читати реальний двіжок.

## Варіації й родичі
- Серія: King Dugan's Dungeon (рімейк 1.0), Journey to Rooted Hold (2005), The City Beneath (2007), Gunthro and the Epic Blunder (2012), The Second Sky (2014); DROD RPG (2008, HP і спорядження); Countless Rooms of Death (2015) — короткі кімнати.
- Нові монстри пізніх ігор: вартові (guards), мавки-wubba, грязь і гель (варіанти смоли з іншою вразливістю), seep у стінах, големи, велетні, адери, бомби, тиснучі плити, зілля невидимості, приманки.
- Родичі: Hoplite (детерміновані вороги з телеграфом), Chip's Challenge (монстри з патернами), Into the Breach (тактика з відомими намірами), Void Stranger (покроковий пазл з ворогами-автоматами), роглайки (покроковий рух у 8 напрямках).
- Осі варіацій: **як ворог обирає крок** — жадібно / з відкатом на вісь / утеча / оцінка клітин балами / BFS / зграя / по осі за таймером; **чим гравець б'є** — дотиком / зброєю в сусідній клітині / поворотом зброї.

## Цікавинки для курсу
- Меч як сутність у сусідній клітині й поворот як хід: убивство при вході меча в клітину — 🥉.
- Бестіарій із 8 формул руху (тарган, королева, око, гоблін, wraithwing, змія, смоляня, мозок) — 🥉 за сімʼю, кожна дитина 📎…🥉.
- Мозок: увімкнути BFS-переслідування всім монстрам, поки він живий — 🥇.
- Гоблін з оцінкою клітин балами (тяжіння до гравця, відштовхування від меча) — 🥈: «поле потенціалів» на 9 клітинах.
- Wraithwing: поведінка залежить від інших монстрів (зграя) — 🥈.
- Смола: ріст маси кожні 30 ходів + вразливість лише на краях — 🥇 (аналіз форми маси).
- Порядок ходу монстрів як явні дані + запис демо ходами (детермінізм) — 🥈.
- Кімнати без памʼяті vs підкорені назавжди — 🥉 (стан частини світу).

## Мапа на каталог
- Є: `move-8dir` · `keyboard-controls` · `chase-player`/`chase-greedy` (тарган) · `chase-bfs` (мозок) · `spawn-schedule` (королева, смола) · `impassable-cells` · `destroy-all-enemies` · `touch-death` · `player-death` · `checkpoint` · `key-and-door` (сфери/двері — найближче) · `sequential-levels` · `in-game-editor` · `level-exchange` (holds) · `replay` (демо) · `state-as-data` · `minimap-radar` · `help-window` · `body-queue` (змія).
- **Нема** → пропозиції карток:
  - `+sword-cell` «Зброя в сусідній клітині» · entities/combat · 🥉 — меч як сутність, що вбиває входом у клітину.
  - `+rotate-as-move` «Поворот як хід» · entities/move · 📎.
  - `+flee-player` «Утеча від гравця» · entities/move · 📎 — дзеркало `chase-greedy`.
  - `+wake-on-event` «Сплячий ворог прокидається» · entities/state · 📎 (є з Lolo) — тут за променем погляду.
  - `+score-field-move` «Крок за оцінкою клітин» · entities/move · 🥈 — гоблін.
  - `+pack-behaviour` «Поведінка залежить від зграї» · entities/move · 🥈 — wraithwing.
  - `+blob-growth` «Ріст маси» · entities/spawn · 🥉 (є з Boulder Dash) — смола.
  - `+shrink-to-death` «Скорочення в пастці» · entities/state · 📎 — змія.
  - `+button-toggle` (є з Chip's) — сфера з дією open/close/toggle.
  - `+clear-unlocks` «Зачистка відкриває двері» · game-logic/win · 📎 — зелені двері.
  - `+crumble-floor` «Підлога руйнується, коли з неї зійшли» · entities/interact · 📎 — люк (також скло у Void Stranger).
  - `+one-way-cell` (є з Lolo) — стрілки.
  - `+hint-tile` (є з Chip's) — сувої.
  - `+room-memory` «Непідкорена кімната скидається при виході» · levels/progression · 🥉.
  - `+mimic-copy` «Двійник повторює ходи гравця» · entities/move · 🥉 (також Void Stranger).
  - `+undo-redo` (є з Sokoban).
  - `+movement-order` «Явний порядок ходу монстрів» · code/architecture · 🥉.

## Пропозиції до словників
- `+cond:sword_at` — клітина зайнята зброєю гравця (узагальнення: «зброя/інструмент у клітині»).
- `+effect:shrink` (⏳ є як `shrink`) — тут без розміру: змія −1 сегмент; `+effect:checkpoint` (⏳ є) — зберегти стан кімнати.
- `+role:weapon` — зброя-сутність, що займає клітину й убиває входом (меч DROD).
- `+window:hold-select` — вибір набору рівнів спільноти; ⏳ `map-window`, `replay-window`, `editor-window` вжито.
- `+ui:sword-direction` — напрям зброї видно на полі (або індикатор).
- `+feature:demo-recording` — розвʼязки як послідовність ходів, експорт/імпорт; `+feature:room-reset-on-leave` — кімнати без памʼяті.
- `+card:movement-order` — порядок ходу сутностей як частина правил (DROD, Chip's MS vs Lynx).
- `+axis:undo` — тут обмежений/версійний undo + чекпойнти.
- ⏳-слова, вжиті тут: `input`, `turn_end`, `line_of_sight`, `all_gone`, `leave`, `timer`, `facing`, `free`, `occupied`, `rotate`, `face`, `set_state`, `set_cell`, `spawn_at`, `message`, `gate`, `switch`, `spawner`, `hazard`.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Deadly_Rooms_of_Death) — поле 38×32, хід/поворот/очікування, детермінізм, сфери й люки, історія версій, серія.
- [Caravel: бестіарій](https://forum.caravelgames.com/viewsiteboard.php?b=59) — сторінки монстрів: [тарган](https://forum.caravelgames.com/site/roach), [королева](https://forum.caravelgames.com/site/roachqueen), [око](https://forum.caravelgames.com/site/evileyes), [гоблін](https://forum.caravelgames.com/site/goblins), [смола](https://forum.caravelgames.com/site/tar), [змії](https://forum.caravelgames.com/site/serpents), [мозок](https://forum.caravelgames.com/site/brain), [wraithwing](https://forum.caravelgames.com/site/wraithwings) — точні формули руху.
- [Гайд новачка](https://forum.caravelgames.com/site/guide) і [частина 3](https://forum.caravelgames.com/site/guide3) — кімнати без памʼяті, інфо клітини, кольори привʼязки сфер, F1/F6.
- [Сайт DROD](https://forum.caravelgames.com/viewsitepage.php?id=90294) — демо, [holds](http://forum.caravelgames.com/holds.php), [Flash-версія KDD](http://caravelgames.com/Articles/Games_2/FlashDROD/KDDL.html).
- [wurb.com «DROD: Solving Puzzles»](https://www.wurb.com/stack/archives/127) — есей про розвʼязання кімнат (стрілки як односторонні).

## Непевне
- (?) Правила кольорових дверей: зелені — зачистка кімнати (впевнено), сині — пройдений рівень, червоні — усі люки впали — з памʼяті, у знайдених джерелах не описано.
- (?) Точне правило стрілок: блокують протилежний напрям і дві суміжні діагоналі, на вхід і на вихід.
- (?) Чи вимагає підкорення кімнати знищення всієї смоли і чи рахуються змії/мозок.
- (?) Мімік і зілля невидимості — є в KDD чи лише з DROD 2.
- (?) Наявність undo в KDD-версії й обсяг (1 хід / ∞); клавіша Backspace.
- (?) Кількість рівнів KDD (25) і чи є павуки в KDD.
- (?) Чи витрачається хід при спробі піти в стіну.
