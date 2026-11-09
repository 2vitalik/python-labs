---
title: Robbo
slug: robbo
aka: [The Adventures of Robbo, Robbo Millennium, iRobbo, GNU Robbo, Робо]
family: push-slide
also: [dig-gravity, maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 1989
platforms: [Atari 8-bit, MS-DOS, C64, Atari ST, Windows (Millennium), iOS, Linux/Windows/handhelds (GNU Robbo)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Robbo_(video_game)", best: true, note: "Boulder Dash без гравітації: гвинти → капсула; істоти, лазерні гармати, магніти; ключі, патрони, ящики, бомби, телепорти; версії й кількість рівнів"}
  - {kind: wiki, url: "https://pl.wikipedia.org/wiki/Robbo", note: "56 планет, вертикальний скрол, Robbo Konstruktor (до 32 плансз), неофіційні порти"}
  - {kind: official, url: "https://gnurobbo.sourceforge.net/", note: "GNU Robbo: відкритий ремейк, 1113 рівнів у 28 паках, дизайнер, скіни; без життів і очок"}
  - {kind: other, url: "https://sourceforge.net/p/gnurobbo/code/HEAD/tree/gnurobbo/", note: "код GNU Robbo (board.c — поведінка кожного обʼєкта; data/locales/en_GB/text — довідка й керування)"}
  - {kind: other, url: "http://tajemnice.atari8.info/2_91/2_91_robbo.html", note: "Tajemnice Atari 2/91: 9 життів, етапи по 4 планші, пароль JANUSZ PELC, розвʼязки складних плансз"}
  - {kind: other, url: "http://atariki.krap.pl/index.php/Robbo", note: "Atariki: версії, чіти, відмінності Konstruktor"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Robbo+Atari+1989", note: "пошук; геймплей Atari"}
stage: v1
coverage: 75
mechanics: [move-4dir, keyboard-controls, push-object, collect-quota, reach-exit, key-and-door, item-pickup, projectile-shot, shoot-forward, destructible-blocks, explode-area, chain-detonation, touch-death, player-death, wall-follower, turn-when-blocked, enemy-patrol, chase-greedy, inertia-slide, crush-by-slide, teleport, row-conveyor, player-camera, restart-level, level-select, level-password, cheat-codes, in-game-editor, controls-remap, theme-select, sound-effects, +magnet-pull, +rotating-turret, +laser-beam-gun, +random-object-block, +cyclic-teleport-group, +adjacency-kill]
proposes: ["+effect:attract", "+role:turret", "+card:magnet-pull", "+card:rotating-turret", "+card:laser-beam-gun", "+card:random-object-block", "+card:cyclic-teleport-group", "+card:adjacency-kill", "+feature:game-speed"]
author: opus
date: 2026-11-09
---

# Robbo — Boulder Dash без гравітації: збери гвинти, дійди до капсули між ведмедями, гарматами й магнітами

## Суть
Робот Робо застряг на чужій планеті: на кожній планші треба зібрати гвинти, після чого капсула оживає і везе на наступну планету. Нічого не падає — усе стоїть, доки його не штовхнуть чи не підірвуть, тому гра ближча до Sokoban, ніж до Boulder Dash. Серед обʼєктів: ящики (звичайні й ковзні), бомби, що вибухають від пострілу, ключі й двері, патрони, телепорти, магніти, гармати з трьома видами вогню, силові поля й «?», з якого випадає випадковий предмет. Вороги — ведмеді, що обходять стіни, птахи, що патрулюють і стріляють, і метелики, що полюють на Робо.

## Поле і час
- Квадратна сітка; лабіринт планші довший за екран, камера скролить за Робо (оригінал — вертикально). GNU Robbo: поле до 32×31, видно 16×12 клітин.
- Один шар обʼєктів: у клітині рівно один обʼєкт; Робо не є клітиною поля, він «над» порожньою.
- Real-time на тіках: кожен тип має свою затримку (у GNU Robbo: Робо — 4 тіки на крок, птах / ведмідь / метелик — 4, гармата — 8, поворот гармати — 20).
- Оригінал: 56 планет, етапи по 4 планші.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робо | player | патрони, ключі, гвинти, життя (Atari: 9) | крок 4 напрямки; штовхає; стріляє в 4 боки |
| Стіна (кілька стилів) | static | — | непрохідна, незнищенна |
| Земля / завал | static | — | непрохідна; знищується пострілом |
| Гвинт | pickup | — | зменшує лічильник гвинтів; 0 → капсула відкрита, екран блимає |
| Капсула | gate | закрита / відкрита | вихід, коли зібрано потрібні гвинти |
| Патрони | pickup | +9 | обойма для пострілів |
| Ключ | pickup | — | +1 ключ |
| Двері | gate | — | відкриваються, витрачаючи ключ |
| Ящик | object | — | штовхається на 1, якщо за ним порожньо |
| Ковзний ящик (push box) | object | — | після поштовху їде до упору; знищує на шляху все знищуване (ворогів) |
| Бомба | object | — | штовхається; від пострілу чи вибуху — вибух 3×3, ланцюг з іншими бомбами |
| «?» | object | — | штовхається; знищений пострілом — стає випадковим обʼєктом |
| Телепорт | terrain | номер групи | переносить до наступного телепорта тієї ж групи; вихід — у напрямку руху або в інший вільний бік |
| Магніт | hazard | напрям | Робо на його лінії без перешкод — притягується і гине; будь-який обʼєкт між ними захищає |
| Гармата | hazard | напрям; нерухома / обертова / рухома / штовхана | випадково стріляє в напрямку дула |
| Лазерна гармата | hazard | — | суцільний промінь, поки гармата на місці |
| Бластер | hazard | — | промінь, що руйнує знищуване на шляху |
| Постріл (лазерний заряд) | projectile | напрям | летить прямо; вбиває Робо, знищує знищуване, підриває бомби |
| Силове поле | hazard | — | сегменти циклічно зсуваються вздовж рядка між стінами; знищується пострілом |
| Ведмідь | enemy | — | обходить перешкоди за правилом лівої руки |
| Чорний ведмідь | enemy | — | те саме за правилом правої руки |
| Птах | enemy | — | летить прямо, впершись — розвертається; інколи стріляє вбік |
| Метелик | enemy | — | крок у бік Робо по x або y, інколи випадковий напрям |
| Додатковий Робо (Atari) | pickup | — | +1 життя |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(robbo, dir)`.
- КОЛИ `contact(robbo, screw)` → ТО `pickup`, `counter(screws_left, -1)`.
- КОЛИ `counter(screws_left, ==, 0)` → ТО `set_state(capsule, open)`, `flash`.
- КОЛИ `contact(robbo, capsule)` → ЯКЩО `state(capsule, open)` → ТО `win`, `next_level`; інакше `block`.
- КОЛИ `contact(robbo, bullets)` → ТО `pickup`, `counter(ammo, +9)`. КОЛИ `contact(robbo, key)` → ТО `pickup`, `counter(keys, +1)`.
- КОЛИ `contact(robbo, door)` → ЯКЩО `has(robbo, key)` → ТО `disappear_b`, `take(robbo, key)`; інакше `block`.
- КОЛИ `contact(robbo, box|bomb|qmark|movable_gun)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `contact(robbo, push_box)` → ЯКЩО `free(cell_behind)` → ТО `slide(push_box, dir)`.
- КОЛИ `contact(push_box, enemy|qmark|ground|bomb)` під час ковзання → ТО `disappear_b` (бомба — `explode(3x3)`).
- КОЛИ `input(fire + dir)` → ЯКЩО `has(robbo, ammo)` → ТО `spawn_at(shot, ahead)`, `counter(ammo, -1)`.
- КОЛИ `contact(shot, ground|enemy|barrier|qmark)` → ТО `disappear_both`.
- КОЛИ `contact(shot, bomb)` → ТО `explode(3x3)`: у зоні знищуване зникає, Робо — `lose`.
- КОЛИ `after(explode)` → ЯКЩО `occupied(blast_area, bomb)` → ТО `explode(3x3)` — ланцюг.
- КОЛИ `destroyed(qmark)` → ТО `spawn(random_object)` — порожньо / ковзний ящик / гвинт / патрони / ключ / бомба / земля / метелик / гармата / «?».
- КОЛИ `adjacent(robbo, bear|bird|butterfly)` (4-сусідство) → ТО `lose`.
- КОЛИ `contact(shot|laser|blaster, robbo)` → ТО `lose`.
- КОЛИ `line_of_sight(magnet, robbo)` (лише порожні клітини між ними) → ТО `custom: «Робо заблокований і щокроку тягнеться до магніту»`; КОЛИ `blocked(robbo)` біля магніту → ТО `lose`.
- КОЛИ `enter(robbo, teleport[n])` → ТО `teleport(robbo, next_teleport[n])`, вихід у бік руху, інакше в перший вільний.
- КОЛИ `timer(gun_period)` → ЯКЩО `prob(1/8)` → ТО `spawn_at(shot, muzzle)`; обертова — `rotate(gun, 90)` або випадковий напрям; рухома — `move(gun, patrol_dir)`, `bounce` на упорі.
- Ведмідь: `custom: «якщо ліворуч вільно — поверни ліворуч і крокуй; інакше вперед; інакше поверни праворуч»` (чорний — дзеркально).
- Птах: `blocked(bird)` → `face(bird, reverse)`; `prob(1/8)` → `spawn_at(shot, side)`.
- Метелик: `custom: «крок до Робо по x або по y»`; `prob(1/8)` → `face(butterfly, random)`.
- Силове поле: `timer(barrier_period)` → `shift(row, dir)` між стінами.
- КОЛИ `died(robbo)` → ТО `lives(-1)`, `restart` планші; Atari: 0 життів → з першої планші поточного етапу.
- Перемога: капсула після квоти гвинтів. · Поразка: дотик-сусідство з істотою, постріл/промінь, вибух, магніт. · Рахунок: Atari — життя; GNU Robbo — без життів і очок.

## Керування і ввід
- Джойстик / стрілки — крок; fire + напрямок (GNU: стрілка + RShift) — постріл у той бік без кроку.
- GNU Robbo: Enter — підтвердити, R — рестарт рівня («самогубство»), Escape — вихід; усе перепризначається, є джойстик і стилус.
- Поки магніт тягне або йде телепортація — ввід ігнорується.

## Вікна, меню, HUD
- Atari: титул/екран інструкцій (там вводиться пароль JANUSZ PELC → 81 життя).
- GNU `main-menu`: Start · Level (`level-select`) · Pack (вибір паку) · Help (`help-window`, 4 сторінки з описом усіх обʼєктів) · Options (`settings-window`: швидкість гри, повтор клавіш, джойстик, мова, частота збереження, перепризначення) · Designer (`editor-window`) · Exit.
- `game-screen`: вʼюпорт поля + рядок стану — гвинти, ключі, патрони, рівень, пак (GNU); життя — в Atari (?).
- `end-screen` після останнього рівня паку; DOS-версія — `level-password`.
- Переходи: main-menu → game-screen → (капсула) наступна планша → … → end-screen; смерть → та сама планша.

## Фічі поза полем
- `levels-sequential` (56 планет Atari; 60 DOS; 76 C64; 136 ST; 130 Millennium; 1113 у 28 паках GNU) + `level-select` до досягнутого рівня (GNU).
- `level-password` (DOS), чіти: пароль на 81 життя, пропуск планші (утримати Start+Select+Option при зборі гвинта).
- `level-editor`: Robbo Konstruktor (1990, до 32 плансз), дизайнер у GNU Robbo.
- `restart-level`, `remap-controls`, `+feature:game-speed` (Fast/Normal/Slow), скіни графіки й звуку (`theme-select`), `localization`.

## Варіації й родичі
- Atari 1989 → DOS / The Adventures of Robbo (1993, з паролями) → C64, Atari ST → Robbo Millennium (2000) → iRobbo (2010); GNU Robbo (з 2002) додає обʼєкти Robbo Millennium і клону Alex (радіоактивне поле, стоп, друга бомба).
- [Boulder Dash](../dig-gravity/boulder-dash.md), [Repton](../dig-gravity/repton.md), [Supaplex](../dig-gravity/supaplex.md) — те саме «зібрати квоту → вихід», але з гравітацією.
- [Chip's Challenge](../maze-arcade/chips-challenge.md) — ключі, двері, монстри за правилами руху; [Adventures of Lolo](adventures-of-lolo.md) — постріл і блоки; [Sokoban](sokoban.md) — штовхання.
- Осі варіацій: **гравітація** (є — Boulder Dash / нема — Robbo) · **постріл** (нема / обмежені патрони) · **смерть** (на спільній клітині / від сусідства) · **магніт** (тягне предмети / тягне гравця на смерть).

## Цікавинки для курсу
- Смерть від сусідства, а не від спільної клітини (перевірка 4 сусідів щотіку) — 🌱.
- Ведмеді за правилом лівої / правої руки, з фіксом «кружляння на місці» — 🥉.
- Ковзний ящик як зброя: їде до упору й знищує на шляху — 📎.
- Бомба 3×3 з ланцюговою детонацією — 🥉.
- Магніт: перевірка «чиста лінія до Робо» + примусове тягнення з блокуванням вводу — 🥉.
- Гармати з чотирма вимірами (стріляє / обертається / рухається / штовхається) і три типи вогню — 🥈.
- «?»: знищений блок → випадковий обʼєкт зі списку — 📎.
- Телепорти групами з циклічним пошуком наступного і вибором вільного виходу — 🥉.

## Мапа на каталог
- Є: `move-4dir`, `keyboard-controls`; `push-object` ↔ ящик, бомба, «?»; `collect-quota` + `reach-exit` ↔ гвинти → капсула; `key-and-door`; `item-pickup`; `projectile-shot` + `shoot-forward` ↔ постріли Робо й гармат; `destructible-blocks` ↔ земля; `explode-area` + `chain-detonation` ↔ бомби; `touch-death`, `player-death` ↔ життя; `wall-follower` ↔ ведмеді; `turn-when-blocked` + `enemy-patrol` ↔ птах, рухомі гармати; `chase-greedy` ↔ метелик; `inertia-slide` + `crush-by-slide` ↔ ковзний ящик; `teleport`; `row-conveyor` ↔ силове поле; `player-camera`; `restart-level`, `level-select`, `level-password`, `cheat-codes`, `in-game-editor`, `controls-remap`, `theme-select`, `sound-effects`.
- **Нема** → пропозиції карток:
  - `+magnet-pull` «Магніт тягне гравця по чистій лінії» · entities/interact · 🥉.
  - `+rotating-turret` «Гармата обертається / рухається / штовхається» · entities/combat · 🥉 · слоти {rotate: none|cw|random, movable, pushable}.
  - `+laser-beam-gun` «Суцільний промінь, що живе, поки є гармата» · entities/combat · 📎 · слот {destroys: bool} (бластер).
  - `+random-object-block` «Знищений блок стає випадковим обʼєктом» · entities/spawn · 📎.
  - `+cyclic-teleport-group` «Телепорти групами, перехід до наступного» · entities/interact · 📎.
  - `+adjacency-kill` «Смерть від сусідства з істотою» · entities/death · 🌱.

## Пропозиції до словників
- `+effect:attract` — примусово тягне сутність до джерела щокроку (магніт).
- `+role:turret` — нерухоме чи рухоме джерело пострілів (гармата).
- `+card:magnet-pull`, `+card:rotating-turret`, `+card:laser-beam-gun`, `+card:random-object-block`, `+card:cyclic-teleport-group`, `+card:adjacency-kill` — див. «Мапу на каталог».
- `+feature:game-speed` — швидкість тіків як налаштування (Fast/Normal/Slow).

## Джерела
- ⭐ [Wikipedia: Robbo](https://en.wikipedia.org/wiki/Robbo_(video_game)) — автор, мета (гвинти → капсула), небезпеки й предмети, версії, кількість рівнів, Konstruktor, GNU Robbo.
- [Wikipedia PL: Robbo](https://pl.wikipedia.org/wiki/Robbo) — 56 планет, скрол, Konstruktor до 32 плансз, неофіційні порти.
- [GNU Robbo](https://gnurobbo.sourceforge.net/) — правила ремейку, паки, дизайнер, скіни.
- [Код GNU Robbo](https://sourceforge.net/p/gnurobbo/code/HEAD/tree/gnurobbo/) — `board.c`: ведмеді (ліва/права рука), птах, метелик, магніт, гармати, бластер, ковзний ящик, бомба 3×3, «?», телепорти, смерть від сусідства; `text`: довідка, меню й клавіші.
- [Tajemnice Atari 2/91](http://tajemnice.atari8.info/2_91/2_91_robbo.html) — 9 життів, етапи по 4 планші, пароль, розвʼязки складних плансз.
- [Atariki: Robbo](http://atariki.krap.pl/index.php/Robbo) — версії, чіти, обмеження Konstruktor.
- YouTube: пошук «Robbo Atari 1989».

## Непевне
- (?) Поведінка обʼєктів — за GNU Robbo, який відтворює Atari з навмисними «розумними» змінами (ведмеді не кружляють, промінь гасне з гарматою, «?» не дає капсулу).
- (?) Розмір планші Atari (16 клітин завширшки?) і що саме показує рядок стану в Atari-версії (життя, гвинти, ключі, патрони).
- (?) Чи вбиває силове поле при дотику, чи лише блокує — довідка каже «seriously bad», код не позначає його як «killing».
- (?) Скільки гвинтів треба: у файлі рівня — окреме число, не обовʼязково всі на планші.
