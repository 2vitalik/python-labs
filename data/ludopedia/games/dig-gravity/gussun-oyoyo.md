---
title: Gussun Oyoyo (ぐっすんおよよ)
slug: gussun-oyoyo
aka: [ぐっすんおよよ, Risky Challenge, Super Gussun Oyoyo, すーぱーぐっすんおよよ, Gussun Oyoyo S]
family: dig-gravity
also: [falling-match, grid-platformer]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: coop
  info: full
  random: runtime
  goal: state
year: 1993
platforms: [arcade, SNES, PlayStation, Saturn, mobile, Wii VC, Wii U VC]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ぐっすんおよよ", best: true, note: "система: блоки й бомби, герої-автомати (лізуть на 1 блок, тікають від блока, завмирають від вибуху), причини промаху, вода, кілька виходів, усі 10 ворогів"}
  - {kind: other, url: "https://www.hardcoregaming101.net/gussun-oyoyo/amp/", note: "HG101: «Lemmings + Tetris», підвезти героя на падаючому блоці, замурувати ворога, 10 дітей = життя, Risky Challenge, порти"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gussun_Oyoyo", note: "серія: аркада 1993 (Risky Challenge), порти й сиквели"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Gussun+Oyoyo+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, move-auto, cursor-place, explode-area, bomb-fuse, touch-death, environment-death, player-death, reach-exit, random-walk, chase-player, spawner-entity, respawn, item-pickup, temporary-modes, event-points, level-select, carrier-platform, +auto-walker-guide, +step-climb-one, +scare-away, +fear-freeze, +ride-falling-piece, +rising-hazard-front, +top-out-lose, +block-breaker-enemy, +trap-removes-respawn, +branching-exits, +collect-for-life]
proposes: ["+effect:raise_level", "+role:walker", "+card:step-climb-one", "+card:scare-away", "+card:ride-falling-piece", "+card:top-out-lose", "+card:block-breaker-enemy", "+card:trap-removes-respawn", "+card:branching-exits"]
author: opus
date: 2026-11-09
---

# Gussun Oyoyo — Tetris для Lemmings: скидай блоки, щоб дурник-автомат сам дійшов до виходу, поки підіймається вода

## Суть
Аркадна головоломка Irem: згори падають блоки й бомби, гравець рухає їх і скидає, а внизу **сам по собі** ходить герой Гуссун — лізе на сходинку лише в один блок, тікає від блока, що впав поруч, завмирає від вибуху, кидається з обривів і у воду. Гравцеві треба добудувати з блоків дорогу до дверей-виходу, водночас давлячи ворогів, не розчавивши героя і не завалившись блоками до стелі. Тиск часу — **вода, що підіймається** знизу. Візерунок блоків випадковий, тож одного розвʼязку нема.

## Поле і час
- Бічний вид, печера-екран з рельєфом, шипами, водою, виходом(ами). Квадратна сітка блоків; герой і вороги ходять по ній.
- Real-time: блок падає згори, гравець керує ним до приземлення; потім — наступний (блок чи бомба).
- Вода: через заданий час починає підійматися знизу; на деяких стадіях вода є з початку, на деяких на старті її спускають.
- Стадія закінчується, коли герой у дверях; кілька дверей — різні бонуси і різна наступна стадія.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гуссун (1P) / Ойойо (2P) | ally | життя (аркада) | іде сам; лізе лише на 1 блок; від блока поруч тікає в інший бік; від вибуху поруч завмирає; падає з обривів |
| Падаючий блок | object | форма — (?) | гравець рухає його під час падіння; приземлився — стає рельєфом; падаючим можна підвезти героя або штовхнути його в повітрі |
| Бомба | object | — | падає як блок; гравець підриває будь-коли; вибух прибирає рельєф і ворогів |
| Bomb block (ボムブロック) | object | — | блок з властивістю вибуху |
| Рельєф / складені блоки | terrain | — | по ньому ходять; складено до верху екрана — промах |
| Шипи (стіна, підлога) | hazard | — | дотик героя — промах |
| Вода | hazard | рівень | підіймається з часом; герой у воді тоне |
| Двері-вихід | gate | бонус за складність | герой у дверях — стадія пройдена; кілька дверей — розгалуження |
| Предмет | pickup | ефект | очки / тимчасово зупинити ворогів / зупинити воду / невразливість / дихання під водою |
| Дитина Гуссуна | pickup | — | 10 зібраних — додаткове життя |
| Puni-kun | enemy | помаранчевий слиз | стоїть на місці |
| Poni-kun | enemy | синьо-зелений слиз | повільно рухається |
| Oni no Chibita-kun | enemy | малий синій оні | просто ходить (рідко трапляється) |
| Gacha-kun | enemy | ріг | блок, що впав на нього, ламається — нею прибирають зайві блоки |
| Pompe-kun | enemy | великі ноги | рухається стрибками, не вище 2 блоків |
| Pero-kun | enemy | жовтий слимак | повзе по рельєфу, лізе на 2+ блоки, обходить зовнішні краї |
| Hinotama Meramera-kun | enemy | вогник | пливе у випадкових напрямках, то до героя, то від нього |
| Fuu-kun | enemy | «смерть» з косою | наближається до героя, поруч — замах косою |
| Yoyo-kun | enemy | зелений | вилазить із поставлених блоків, іноді просто під ногами героя |
| Dokidoki Bakuhatsu-kun | enemy | ходяча бомба | випадково світиться червоним і вибухає як bomb block |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(piece, dir)`; поворот і прискорення — `custom: «(?)»`.
- КОЛИ `tick` → ЯКЩО `free(below_piece)` → ТО `fall(piece)`; КОЛИ `locked(piece)` → ТО `set_cell(piece_cells, terrain)`, `spawn_at(next_piece, top)`.
- КОЛИ `locked(piece)` → ЯКЩО `custom: «стос досяг верху екрана»` → ТО `lose`, `lives(-1)`.
- КОЛИ `tick` → ТО `move(gussun, facing)`; ЯКЩО `not supported(gussun)` → ТО `fall(gussun)`.
- КОЛИ `blocked(gussun)` → ЯКЩО `custom: «перешкода заввишки рівно 1 блок і над нею вільно»` → ТО `custom: «вилазить на сходинку»`; інакше `face(gussun, reverse)` (?).
- КОЛИ `adjacent(piece, gussun)` → ЯКЩО `custom: «блок щойно приземлився поруч»` → ТО `face(gussun, away)` — тікає в протилежний бік.
- КОЛИ `custom: «вибух поруч із героєм»` → ТО `stun(gussun, n)` — завмирає від страху.
- КОЛИ `contact(piece, gussun)` → ЯКЩО `moving(piece, down)` and `not free(below_gussun)` → ТО `lose` — розчавлений.
- КОЛИ `contact(piece, gussun)` → ЯКЩО `moving(piece, down|left|right)` and `custom: «герой стоїть на блоці або блок штовхає його збоку»` → ТО `carry(piece, gussun)` — підвезти на падаючому блоці / перекинути через прірву.
- КОЛИ `contact(gussun, enemy|spikes)` → ТО `lose`, `lives(-1)`.
- КОЛИ `enter(gussun, water)` → ЯКЩО `not state(gussun, breathing)` → ТО `lose`, `lives(-1)`.
- КОЛИ `timer(water_delay)` → ЯКЩО `not state(water, frozen)` → ТО `custom: «вода піднімається на крок»`.
- КОЛИ `contact(piece, enemy)` → ЯКЩО `moving(piece, down)` and `not same(enemy, gacha)` → ТО `disappear_b`, `score(+n)`.
- КОЛИ `contact(piece, gacha)` → ЯКЩО `moving(piece, down)` → ТО `disappear_a` — ріг ламає блок.
- КОЛИ `custom: «ворога повністю замуровано блоками»` → ТО `custom: «ворог виключений зі списку респавну»`; інакше вбиті вороги `respawn` без попередження.
- КОЛИ `input(detonate)` → ЯКЩО `count(bomb, >, 0)` → ТО `explode(area, into: empty)`; ворогів у зоні — `disappear`, героя поруч — `stun`.
- КОЛИ `rng(p)` → ЯКЩО `same(enemy, bakuhatsu)` → ТО `set_state(enemy, glowing)`, потім `explode(area)`.
- КОЛИ `spawned(piece)` → ЯКЩО `custom: «точка появи yoyo-kun у блоці»` → ТО `spawn(yoyo)` (?).
- КОЛИ `contact(gussun, item)` → ТО `pickup`, `set_state(effect, on, dur)` — зупинка ворогів / води, невразливість, дихання.
- КОЛИ `contact(gussun, kid)` → ТО `counter(kids, +1)`; КОЛИ `counter(kids, ==, 10)` → ТО `lives(+1)`, `counter(kids, -10)`.
- КОЛИ `enter(gussun, exit)` → ТО `win`, `score(exit_bonus)`, `custom: «наступна стадія — за обраними дверима»`.
- Кооператив: КОЛИ `enter(gussun|oyoyo, exit)` → ТО `win` — дійти достатньо одному.
- Перемога: герой у дверях. · Промах: розчавлений, ворог, шипи, вода, блоки до стелі. · Рахунок: бонус дверей (важчі двері — більше), предмети-очки, вбиті вороги (?).

## Керування і ввід
- Джойстик — рух падаючого блока вліво-вправо; кнопки — поворот / пришвидшення (?) і підрив бомби.
- Героєм **не керують**: лише перебудовують світ навколо нього блоками і лякають блоками й вибухами (непряме керування).
- Перед стартом — вибір стартової стадії (налаштування); секретна комбінація вмикає «hentai mode» (інший пролог і репліки, ті самі стадії).

## Вікна, меню, HUD
- `attract-demo` / титул аркади; вибір 1 або 2 гравців (кооп) — `mode-select`.
- `level-select` — вибір стартової стадії (в EN-версії Risky Challenge — ні, завжди з початку).
- `dialogue-window` — пролог і репліки (Емілі), змінювані в hentai mode.
- `game-screen`: печера, падаючий блок, `next-piece-preview` (?), `score`, `lives`, лічильник дітей (?), рівень води.
- `end-screen` — бонус за двері; `game-over-continue` (аркада, кредити) (?).
- Переходи: титул → (вибір) → game-screen → (двері) бонус → наступна стадія гілки.

## Фічі поза полем
- Розгалужена прогресія: кілька дверей на стадії → різні наступні стадії (дерево замість ланцюга).
- `level-select` для старту; `mode-coop` на двох (Гуссун і Ойойо).
- Порти: SFC (Banpresto, 1995) — Super Gussun Oyoyo; PlayStation (Xing, 1995) — власні стадії після перших аркадних; Saturn (Gussun Oyoyo S, 1996) — нові стадії й катсцени; мобільні (2003); Virtual Console.
- Сиквели: Super Gussun Oyoyo 2 (SFC, 1996), Zoku Gussun Oyoyo (PS 1996, Saturn 1997), Gussun Paradise (PS 1996; EU — YoYo's Puzzle Park).

## Варіації й родичі
- Родичі в корпусі: [Lemmings](lemmings.md) (автоходці, рятувати), [Survivors](survivors.md), [Doki Doki Penguin Land](doki-doki-penguin-land.md) (вантаж, що падає), [Mr. Driller](mr-driller.md); з `grid-platformer` — Troddlers, Krusty's Fun House; з `falling-match` — Tetris (падаючі блоки, програш на стелі).
- **Осі варіацій**: керування героєм — «аватар / роздача вмінь (Lemmings) / лише середовище, яке ти скидаєш згори (Gussun)»; реакція автомата — «ігнорує / розвертається від стіни / тікає від нового блока / завмирає від вибуху»; тиск часу — «таймер / вода, що підіймається (тут) / стос до стелі (Tetris)»; прогресія — «ланцюг / дерево за виходами».

## Цікавинки для курсу
- Автохідник зі сходинкою рівно в 1 блок і реакціями «тікає / завмирає» — 🥉 (автомат з кількома тригерами-стимулами).
- Tetris-шар (падаючий блок під керуванням, фіксація в рельєф, програш на стелі) над платформерним шаром — 🥉.
- Підвезти героя на ще падаючому блоці (сутність-платформа, що сама рухається під керуванням) — 🥈.
- Вода, що підіймається, і предмет, що її зупиняє, — 📎.
- Ворог Gacha-kun, що ламає блоки, як «гумка» для гравця — 🌱; замурований ворог випадає з респавну — 📎.
- Двері з різним бонусом і різною наступною стадією — 📎 (граф стадій).

## Мапа на каталог
- Є: `gravity-fall` ↔ блоки й герой · `move-auto` ↔ Гуссун · `cursor-place` ↔ куди впаде блок · `explode-area` ↔ бомби · `bomb-fuse` ↔ Bakuhatsu-kun (випадковий запал) · `touch-death` + `environment-death` + `player-death` ↔ вороги, шипи, вода · `reach-exit` · `random-walk` ↔ Hinotama · `chase-player` ↔ Fuu-kun · `spawner-entity` ↔ Yoyo-kun з блоків · `respawn` ↔ вороги повертаються · `item-pickup` + `temporary-modes` ↔ предмети · `event-points` · `level-select` · `carrier-platform` ↔ падаючий блок везе героя.
- **Нема** → пропозиції карток:
  - `+auto-walker-guide` (вже пропонована) — тут {control: drop-pieces}.
  - `+step-climb-one` «Автомат лізе лише на сходинку висотою 1» · entities/move · 🌱.
  - `+scare-away` «Новий блок поруч — автомат розвертається й тікає» · entities/move · 📎; `+fear-freeze` «Вибух поруч — завмирає» · entities/state · 🌱.
  - `+ride-falling-piece` «Падаючий керований блок підвозить/штовхає сутність» · entities/interact · 🥈.
  - `+rising-hazard-front` (вже пропонована) — вода знизу.
  - `+top-out-lose` «Стос до стелі — програш» · game-logic/lose · 🌱.
  - `+block-breaker-enemy` «Ворог, що ламає блок, який на нього впав» · entities/interact · 🌱.
  - `+trap-removes-respawn` «Замурований ворог виключається з респавну» · entities/spawn · 📎.
  - `+branching-exits` «Кілька виходів — різний бонус і різна наступна стадія» · levels/progression · 📎.
  - `+collect-for-life` «N зібраних — додаткове життя» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:raise_level` — рівень води/лави підіймається на крок (Gussun, Pac-Man 256 — фронт небезпеки).
- `+role:walker` — союзний автомат, якого треба провести (Гуссун, лемінги); відрізняється від `ally` тим, що ним не керують.
- `+card:step-climb-one`, `+card:scare-away`, `+card:ride-falling-piece`, `+card:top-out-lose`, `+card:block-breaker-enemy`, `+card:trap-removes-respawn`, `+card:branching-exits` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia JA: ぐっすんおよよ](https://ja.wikipedia.org/wiki/ぐっすんおよよ) — система (блоки й бомби, випадковий візерунок, підвезти/штовхнути героя блоком), поведінка героїв, причини промаху, вода, предмети, кілька дверей і бонуси, вибір стартової стадії, hentai mode, усі вороги з поведінкою, 1–4 гравці, порти й сиквели.
- [HG101: Gussun Oyoyo](https://www.hardcoregaming101.net/gussun-oyoyo/amp/) — «Lemmings + Tetris», герой стрибає з обривів і в воду, страх від блока, підвезти падаючим блоком, бомба виправити помилку, замурувати ворога, предмети (невразливість, дихання, стоп часу), 10 дітей = життя, кооп, Risky Challenge без вибору стадії, порти PS/Saturn.
- [Wikipedia EN: Gussun Oyoyo](https://en.wikipedia.org/wiki/Gussun_Oyoyo) — серія і випуски.
- YouTube: пошук «Gussun Oyoyo gameplay».

## Непевне
- (?) Форми блоків (тетраміно? одиночні?), поворот і пришвидшення падіння, кнопки, прев'ю наступного блока — у джерелах нема.
- (?) Чи герой розвертається біля стіни, чи гине від великої висоти — джерела кажуть лише «стрибає з обривів».
- (?) Режим на 1–4 гравці: JA-вікі пише «versus», HG101 — кооператив, де досить дійти одному; у шапці — `coop`.
- (?) Чи дають очки за вбитих ворогів; як саме зʼявляються Yoyo-kun (з «поставлених блоків»).
