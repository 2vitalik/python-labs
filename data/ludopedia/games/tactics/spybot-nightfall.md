---
title: "Spybot: The Nightfall Incident (Lego Spybotics)"
slug: spybot-nightfall
family: tactics
also: [maze-arcade]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: none
  goal: state
year: 2002
platforms: [web (Shockwave, lego.com)]
links:
  - {kind: other, url: "https://github.com/breakid/Spybotics-The-Nightfall-Incident", best: true, note: "фанатський браузерний ремейк; program_data.js — таблиця всіх програм (move, max size, команди, ціна), README — плитки поля й умови перемоги"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lego_Spybotics", note: "контекст серії Spybotics; Gamelab, 2002, data battles, кредити, Disarray"}
  - {kind: other, url: "https://github.com/fergusq/java-nightfall", note: "Java-клон: магазини, лікування, модифікація сітки (Bit-Man)"}
  - {kind: other, url: "https://github.com/Eastonium/nightfall-solidjs", note: "ще один ремейк (SolidJS)"}
  - {kind: other, url: "https://github.com/svew/spybotics-icons", note: "спрайти програм оригіналу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=spybot+the+nightfall+incident+gameplay", note: "пошук; геймплей оригіналу"}
stage: v1
coverage: 70
mechanics: [body-queue, hp-damage, move-4dir, impassable-cells, legal-move-highlight, hover-highlight, item-pickup, round-currency, shop-between-levels, shop-catalog, shop-preview, destroy-all-enemies, collect-all, ai-opponent, ai-greedy, chase-bfs, sequential-levels, level-unlock, save-progress, game-screen, end-screen, shop-window, +body-as-hp, +grow-on-move, +tail-damage, +deployment-phase, +movement-points, +grid-edit, +self-cost-ability, +size-requirement, +speed-debuff, +max-size-buff, +world-map]
proposes: ["+effect:grow", "+effect:shrink", "+effect:speed", "+effect:set_cell", "+effect:currency", "+cond:size", "+cond:in_range", "+trigger:input", "+role:piece", "+role:terrain", "+window:map-window", "+window:prep-screen", "+window:dialogue-window", "+ui:program-card", "+ui:reachable-highlight", "+axis:actors"]
author: opus
date: 2026-11-02
---

# Spybot: The Nightfall Incident — тактика змійками: тіло програми — її HP, рух розтягує тіло, удар відрізає хвіст

## Суть
Гравець-агент S.M.A.R.T. проводить «data battles» на сітках мережевих вузлів: кожна його програма — **змійка з клітин-секторів**, що росте при русі до свого максимального розміру. Розмір = здоровʼя: атака ворога «видаляє N секторів» з хвоста, програма розміром 0 стерта. Тому рух — не лише позиціонування, а й лікування (відростити тіло), а довге тіло — живий щит і стіна для ворога. Між боями — кредити, магазин нових програм і карта мережі з вузлами.

## Поле і час
- Поле — квадратна сітка довільної форми (зазвичай ~16×12–20×14 (?)): є клітини-сектори і **дірки** (немає сітки — непрохідно). Деякі клітини — зони завантаження (upload), кредити, дані.
- Два шари: клітина сітки (є/нема, спецклітина) + програма, що займає клітину головою чи тілом.
- Хід покроковий, фазами сторін: гравець ходить усіма своїми програмами в будь-якому порядку, потім AI — усіма своїми. Кожна програма за хід: до `move` кроків, потім одна команда (або нічого).
- Камера статична, поле видно повністю; ворожі програми й їхні параметри видно наведенням.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Програма (загалом) | piece | move, max size, поточний size, 1–2 команди (range, сила, size_req) | голова ходить 4 напрямки; тіло — черга пройдених клітин |
| Сектор тіла | object | належить програмі | займає клітину; блокує рух інших; першим зникає найстаріший |
| Hack / Hack 2.0 / 3.0 | piece | move 2–4, max 4 | ближня атака Slice −2; вищі версії — Dice −3 / Mutilate −4 |
| Slingshot | piece | move 2, max 2 | Stone: −1 на дальності 2 (?) — стартова дистанційна |
| Bug · Mandelbug · Heisenbug | piece | move 5, max 1 | крихітні швидкі; Glitch −2 / −4 / −6 впритул — одна атака вбиває їх самих |
| Wolf Spider · Black Widow · Tarantula | piece | move 3–5, max 3 | Byte −2/−3 + Paralyze: швидкість цілі −3 |
| Golem.Mud / Clay / Stone | piece | move 1–3, max 5–7 | повільні важкі: Thump −3 / Bash −5 / Crash −7 |
| Sumo | piece | move 2, max 12 | Dataslam −8; велике тіло як стіна |
| Seeker / 2.0 / 3.0 | piece | move 3–4, max 3–5 | дальні атаки −2; 3.0 — Seek & Destroy: −5 цілі і −2 собі |
| Tower · Mobile Tower · Satellite · Laser Satellite | piece | move 0–2, max 1 | «турелі»: стаціонарні або майже, дальні атаки −3/−4 |
| Ballista · Catapult | piece | move 1–2, max 2–3 | Fling −2 на дальності 4 |
| Bit-Man | piece | move 3, max 3 | Zero: видалити клітину сітки; One: створити клітину сітки |
| Data Doctor · Pro · Medic | piece | move 3–5 | Grow/Hypo: +2 сектори цілі; Megagrow +4; Surgery: max size цілі +1 |
| Turbo · Turbo Deluxe | piece | move 3–4 | Boost: move цілі +1 (+2), ціною 1 (2) власних секторів |
| Fiddle | piece | move 3, max 3 | Tweak: move +1 / Twiddle: max size +1 цілі, ціною 1 власного сектора |
| Clog.01 / .02 / .03 | piece | move 2, max 4 | Lag/Chug: move цілі −1/−2; Hang (потрібен розмір 4): move цілі = 0 |
| Wizard · Guru | piece | move 2–3 | змішані: атака + Stretch (max +1) / Ice (move −3) |
| Buzzbomb · Logic Bomb | piece | move 8 / 3 | камікадзе: −5 / −10 цілі й самознищення |
| Memory Hog | piece | move 5, max 30, без команд | лише займає місце: живий блок (?) |
| Sentinel / 2.0 / 3.0 | enemy | move 1–2, max 3–4 | ближні Cut −2 / Taser −4 |
| Watchman / X / SP | enemy | move 1, max 2–4 | дальні Phaser/Photon −2 |
| Warden / + / ++ | enemy | move 1–3, max 5–7 | важкі ближні −3/−5/−7 |
| Guard Pup / Dog · Attack Dog | enemy | move 3–4 | швидкі «собаки» Byte −2/−3 |
| Sensor · Sonar · Radar | enemy | move 0, max 1 | нерухомі дальні −1/−2 |
| Fire Wall | enemy | move 2, max 20 | довга стіна Burn −1 |
| Boss | boss | move 6, max 25 | Shutdown −5; фінальний вузол |
| Клітина сітки | terrain | є/нема | по ній ходять; дірка — непрохідна (як стіна) |
| Зона завантаження | terrain | колір сторони | лише тут на старті ставлять свої програми |
| Кредити | pickup | сума | голова стала → гроші в кінці бою |
| Дані (logs) | pickup | — | у деяких вузлах — мета зібрати (?) |

Параметри програм — з фанатської таблиці ремейку (відтворено з оригіналу за відео), не з офіційного джерела.

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «фаза завантаження»`: гравець ставить програми з інвентаря на свої зони upload (одна програма = одна зона, розмір 1); незайняті зони зникають.
- КОЛИ `input(select, program)` → ТО підсвітка досяжних клітин на `moves_left` кроків (BFS з урахуванням дірок і чужих тіл).
- КОЛИ `input(move, program, dir)` → ЯКЩО `free(cell)` або `occupied(cell, own_body)` → ТО `move(head, dir)`, `counter(moves_left, -1)`; інакше `block`.
- КОЛИ голова зайшла на нову клітину → ЯКЩО `size < max_size` → ТО `grow(program, 1)`; інакше `custom: «найстаріший сектор хвоста зникає»` (тіло як черга фіксованої довжини).
- КОЛИ голова зайшла на клітину власного тіла → ТО `custom: «розмір не росте, порядок секторів оновлюється»`.
- КОЛИ `input(command, target)` → ЯКЩО `in_range(program, target, range)` and `size ≥ size_req` → ТО ефект команди; після команди хід програми скінчено (рух після атаки заборонено).
- КОЛИ команда-атака → ТО `shrink(target, n)` — видаляються **найстаріші** сектори (з хвоста); голова лишається.
- КОЛИ `counter(size(target), ==, 0)` → ТО `disappear_b` (програма стерта; своя — втрачена з інвентаря назавжди (?)).
- КОЛИ Grow/Hypo/Megagrow → ТО `grow(target, n)` до max_size: нові сектори додаються біля тіла (?).
- КОЛИ Surgery/Stretch/Twiddle → ТО `custom: «max_size(target) +1»`; КОЛИ Boost/Tweak → ТО `speed(target, +n)`; КОЛИ Lag/Chug/Paralyze/Ice → ТО `speed(target, -n)`; Hang → `speed(target, =0)` (до кінця бою (?)).
- КОЛИ Turbo/Fiddle/Seek & Destroy → ТО додатково `shrink(self, n)` — плата власним тілом; Buzzbomb/Logic Bomb → `disappear_a` після удару.
- КОЛИ Zero (Bit-Man) → ЯКЩО `cell` порожня звичайна → ТО `set_cell(hole)`; One → `set_cell(grid)` на місці дірки.
- КОЛИ `enter(head, credits)` → ТО `pickup`, `currency(+n)` після перемоги; `enter(head, data)` → `counter(data_left, -1)`.
- КОЛИ всі програми сторони зробили хід або `input(end_turn)` → ТО `custom: «хід переходить до AI»`; AI-програми ходять по черзі до найближчої цілі й бʼють найсильнішою командою.
- Перемога: стерти всі ворожі програми (`all_gone(enemy)`), у вузлах з даними — зібрати всі дані (?) · Поразка: стерто всі свої програми · Нагорода: кредити вузла + підібрані на полі; відкриваються сусідні вузли.

## Керування і ввід
- Лише миша: клік по програмі — вибір; клік по сусідній клітині — крок (або стрілки (?)); клік по команді в панелі — режим прицілу; клік по цілі — виконати.
- «Undo» руху, доки програма не використала команду (?); «No action» — завершити програму без команди; «End turn».
- На старті бою: клік по зоні upload → вибір програми зі списку інвентаря; «Start» — почати бій.

## Вікна, меню, HUD
- `splash-screen` / вхід агента — логін S.M.A.R.T. (?).
- `map-window` «Netmap» — граф вузлів мережі (компанії, рівень безпеки); вузли: бій, магазин warez; закриті — до рівня допуску чи попередніх місій; наведення — назва, компанія, рівень.
- `dialogue-window` — повідомлення персонажів (куратори агенції, хакери, Disarray) перед/після вузлів.
- `custom-window` «Upload» (`prep-screen`) — поле з зонами завантаження + список програм інвентаря з кількістю.
- `game-screen` — сітка; ліва панель `program-card`: іконка, назва, Move, Max Size, Current Size, список команд з описом/дальністю/size_req; `reachable-highlight` (досяжні клітини) і `threat-range` (дальність команди); кнопки Undo, No Action, End Turn.
- `shop-window` «Warez» — каталог програм з ціною, описом і параметрами; кредити гравця.
- `end-screen` — перемога (кредити, нові вузли) / поразка (повтор вузла).
- Переходи: Netmap → (вузол) діалог → Upload → game-screen → end-screen → Netmap; Netmap → (магазин) shop-window.

## Фічі поза полем
- `world-map` вузлів + `level-unlock` за рівнем допуску (рівень агента росте з перемогами).
- Економіка: кредити → нові програми в `shop-window`; програми — кількісні (можна мати 2 Hack); стерті в бою — втрачені (?).
- `save-progress` — продовження на сайті (пароль/збереження агента) (?).
- Ремейки додають налаштування `friendly fire`, undo, редактори вузлів.

## Варіації й родичі
- Фанатські клони й ремейки: Haxxit, Slydot: The Sunrise Event, java-nightfall, Spybot-Reloaded — гра жива лише через спільноту (оригінал на Shockwave зник з lego.com).
- Ідея «тіло = HP» перегукується зі Snake (тіло = рахунок) і Snakebird (тіло = форма для руху).
- Родичі за жанром: Into the Breach (мала сітка, атаки з ефектами), Advance Wars (магазин і ростер).
- **Осі варіацій**: HP — число / **тіло-довжина** · рух — фіксований / розтягує тіло · шкода — по HP / з хвоста / з голови / розрізає навпіл · поле — статичне / **редагується грою (Bit-Man)** · ціна здібності — нічого / власні сектори / самознищення.

## Цікавинки для курсу
- Тіло-черга з max size, що росте при русі й ріжеться з хвоста атакою — 🥉 (поверх `body-queue`, деталі з власним тілом і повторними клітинами).
- Досяжність за `move` кроків з дірками й тілами (BFS) + підсвітка — 📎 (як `legal-move-highlight`).
- Команди-модифікатори параметрів (speed ±, max size ±, плата власними секторами, size_req) — 🥉: таблиця команд як дані.
- Bit-Man: редагування поля (видалити/створити клітину) — 📎; тактично — відрізати ворогові шлях.
- AI «йди до найближчої програми й бий найсильнішим» на BFS — 🥈.
- Netmap-граф вузлів з відкриттям за рівнем + магазин програм — 🥉.

## Мапа на каталог
- Є: `body-queue` ↔ тіло програми · `hp-damage` (розмір як HP) · `move-4dir` · `impassable-cells` (дірки, чужі тіла) · `legal-move-highlight` · `hover-highlight` · `item-pickup` (кредити, дані) · `round-currency` · `shop-between-levels` + `shop-catalog` + `shop-preview` · `destroy-all-enemies` · `collect-all` (дані) · `ai-opponent` / `ai-greedy` / `chase-bfs` · `sequential-levels` / `level-unlock` · `save-progress` · `game-screen` · `end-screen` · `shop-window`.
- **Нема** → пропозиції карток:
  - `+body-as-hp` «Довжина тіла = здоровʼя» · entities/state · 🥉 · слот {max_size} — дитина `hp-damage`.
  - `+grow-on-move` «Тіло росте при русі до максимуму» · entities/move · 📎 — дитина `body-queue`.
  - `+tail-damage` «Шкода зрізає з хвоста» · entities/combat · 📎 · слот {from: tail|head}.
  - `+deployment-phase` «Розстановка на зони перед боєм» · game-logic/opponent · 🌱 (вже пропонували в tactics).
  - `+movement-points` «Очки руху на хід» · entities/move · 🌱 (є в tactics).
  - `+grid-edit` «Сутність створює/видаляє клітини поля» · entities/interact · 📎.
  - `+self-cost-ability` «Здібність коштує власного HP» · entities/combat · 🌱.
  - `+size-requirement` «Команда доступна від розміру N» · entities/legality · 🌱.
  - `+speed-debuff` / `+max-size-buff` «Зміна параметрів цілі» · entities/state · 📎 — сімʼя модифікаторів.
  - `+world-map` «Граф вузлів-рівнів» · levels/progression · 🥉 (є в корпусі).

## Пропозиції до словників
- `+effect:grow` / `+effect:shrink` — ⏳ уже є; тут шкода = `shrink` з хвоста, лікування = `grow`.
- `+effect:speed` — зміна move цілі; `+effect:set_cell` — Bit-Man; `+effect:currency` — кредити.
- `+cond:size` — розмір програми ≥ N (size_req команди); `+cond:in_range` — дальність команди.
- `+trigger:input` — вибір/крок/команда мишею.
- `+role:piece` — програма гравця; `+role:terrain` — клітина сітки, зона upload.
- `+window:map-window` — Netmap; `+window:prep-screen` — фаза завантаження програм; `+window:dialogue-window` — повідомлення персонажів.
- `+ui:program-card` — панель параметрів обраної фігури (move, max/поточний розмір, команди з описом).
- `+ui:reachable-highlight` — підсвітка досяжних клітин.
- `+axis:actors` — `party` (кілька програм, кожна ходить раз).

## Джерела
- ⭐ [breakid/Spybotics-The-Nightfall-Incident](https://github.com/breakid/Spybotics-The-Nightfall-Incident) — браузерний ремейк; `assets/js/program_data.js` (усі програми: команди, шкода, дальність, max size, move, ціна), `models.js` (ріст тіла, зріз з хвоста, умови перемоги).
- [Wikipedia: Lego Spybotics](https://en.wikipedia.org/wiki/Lego_Spybotics) — розділ про гру: Gamelab 2002, data battles, кредити, вузли, Disarray.
- [fergusq/java-nightfall](https://github.com/fergusq/java-nightfall) — Java-клон з магазинами, лікуванням і Bit-Man.
- [Eastonium/nightfall-solidjs](https://github.com/Eastonium/nightfall-solidjs) — ремейк.
- [svew/spybotics-icons](https://github.com/svew/spybotics-icons) — спрайти програм.
- YouTube: пошук «spybot the nightfall incident gameplay».

## Непевне
- (?) Усі числа програм — з фанатської реконструкції, не з оригіналу; окремі значення (Slingshot range, Hang size_req, тривалість ефектів швидкості) не перевірено.
- (?) Чи є в оригіналі умова «зібрати всі дані» — є в ремейку (logs), в оригіналі не підтверджено.
- (?) Undo руху до команди — є в ремейку; в оригіналі — з памʼяті.
- (?) Чи втрачається стерта в бою власна програма назавжди — з памʼяті, не перевірено.
- (?) Розміри сіток, куди додаються сектори при Grow — не перевірено.
- (?) Пошук (WebSearch) вичерпано: фан-вікі (fandom) і архів lego.com недоступні; Wikipedia-статті про саму гру нема.
