---
title: Gururin (ぐるりん)
slug: gururin
aka: [ぐるりん, ACA NEOGEO GURURIN]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 1994
platforms: [arcade (Neo Geo MVS), PS4, Xbox One, Switch, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gururin", best: true, note: "A/B обертають арену, 3 одного кольору по вертикалі/горизонталі, стрілка-підказка, люди тримаються за руки, versus, поразка"}
  - {kind: other, url: "https://neo-geo.com/reviews/neo-reviews/Gururin/gururin.html", note: "огляд: квадратна яма, 90° за натиск і 180° утриманням, черепи-сміття супернику"}
  - {kind: other, url: "https://www.arcade-history.com/game/1054/", note: "трійки людей, кнопки A — вліво, B — вправо, 2 гравці, травень 1994"}
  - {kind: official, url: "https://www.nintendo.com/us/store/products/aca-neogeo-gururin-switch/", note: "ACA NEOGEO (Hamster, 2018): режими One Player / Challenge (VS CPU) / Two Player, налаштування, онлайн-рекорди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Gururin+Neo+Geo+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [gravity-fall, keyboard-controls, line-match-clear, chain-reaction, ai-opponent, simultaneous-versus, garbage-attack, mode-select, game-over-continue, score-records, leaderboard, difficulty-levels, +shifting-gravity, +rotate-whole-field, +linked-pieces, +hint-arrow, +cascade-gravity]
proposes: ["+effect:rotate_field", "+axis:gravity-rotating", "+ui:rotation-hint", "+card:rotate-whole-field", "+card:hint-arrow"]
author: opus
date: 2026-11-09
---

# Gururin — кнопками крутиш усю квадратну яму на 90°, і чоловічки падають уже в новий низ; три одного кольору зникають

## Суть
У квадратну яму посеред екрана падають групи маленьких кольорових «чарівних артистів». Гравець може зсувати їх джойстиком, але **не обертати**: замість фігури A/B повертають **усе поле** на 90° вліво/вправо (утримання — на 180°), і те, що було стіною, стає дном. Три однакові кольори в ряд по вертикалі чи горизонталі зникають. Пізніше чоловічки беруться за руки й не розʼєднуються, лишаючи дірки.

## Поле і час
- Квадратна яма (щоб після повороту розміри не змінювались); розмір у клітинах — (?).
- Real-time: група падає зверху; після приземлення гравець повертає яму, і вміст перебудовується під новий напрям «вниз» (?) — головне джерело ланцюгів і головна складність.
- Одиночна гра — падають трійки людей, у versus — пари (Nintendo Life, за пошуковим уривком) (?).
- Versus: дві ями поруч, гравець проти CPU (Challenge) або проти людини.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Падаюча група (трійка / пара) | player | кольори людей | зсув джойстиком, падає; сама не обертається |
| Чоловічок (артист трупи) | tile | колір костюма | лежить у ямі; 3 одного кольору в ряд по вертикалі/горизонталі → зникає |
| Зчеплені за руки | tile | звʼязок із сусідом | не розʼєднуються при падінні/повороті, лишають дірки |
| Череп-цеглина | hazard | — | зʼявляється в ямі суперника після твого збігу (versus); як прибирається — (?) |
| Стрілка-підказка | mark | напрям | іноді показує правильний бік повороту для збігу |
| Яма | static | квадрат, орієнтація | повертається цілком кнопками A/B |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(group, down)`.
- КОЛИ `input(stick_left|right)` → ЯКЩО `free(target_cells)` → ТО `move(group, dir)`.
- КОЛИ `input(a)` → ТО `rotate(field, -90)`; КОЛИ `input(b)` → ТО `rotate(field, +90)`.
- КОЛИ `input(hold_a|hold_b)` → ТО `rotate(field, 180)`.
- КОЛИ `after(rotate)` → ТО `fall(all_unsupported)` у новий низ (?) — `custom: «зчеплені за руки падають разом»`.
- КОЛИ `pattern(line(3))` → ЯКЩО `same(people, color)` and `custom: «вертикаль або горизонталь»` → ТО `clear(line)`, `score(+n)` (?).
- КОЛИ `after(clear)` → ТО `fall(all_unsupported)`; ЯКЩО `pattern(line(3))` → ТО `clear`, `combo(+1)` (ланцюг) (?).
- КОЛИ `spawned(group)` → ЯКЩО `custom: «є хід, що дає збіг»` → ТО `custom: «іноді — стрілка, куди повернути»`.
- КОЛИ `spawned(group)` → ЯКЩО `level(op, n)` → ТО `custom: «частина людей тримається за руки»` — `attach(a, b)`.
- Versus: КОЛИ `after(clear)` → ТО `send_garbage(skull_brick)` у яму суперника.
- КОЛИ `custom: «люди займають яму, нова група не входить»` → ТО `lose`; аркада — `game-over-continue`; versus — `win` суперника.
- Перемога: versus — суперник переповнився; соло — рахунок до поразки. · Рахунок: high score, зберігається з memory card (Neo Geo).

## Керування і ввід
- 8-напрямний джойстик — зсув падаючої групи (і, ймовірно, прискорене падіння вниз (?)).
- A — повернути яму вліво, B — вправо; утримання кнопки — поворот на 180°.
- Ввід принципово інший за Columns/Puyo: фігура не обертається, обертається **поле** — разом зі всім стеком.

## Вікна, меню, HUD
- `attract-demo` / `splash-screen` — титул аркади.
- `mode-select`: One Player · Challenge (VS CPU) · Two Player (ACA).
- `game-screen`: квадратна яма в центрі (у versus — дві), `score`, `next-piece-preview` (?), стрілка-підказка (`+ui:rotation-hint`).
- `game-over-continue` — «вставте монету»; `end-screen` раунду у versus.
- `leaderboard` — high score (memory card); в ACA — онлайн-рейтинг.
- `settings-window` (ACA): складність, налаштування екрана «як в аркаді».
- Переходи: splash → mode-select → game-screen → (переповнення) game-over-continue / end-screen.

## Фічі поза полем
- `mode-versus` (2 гравці на автоматі), Challenge — `ai-opponent-levels` (?) проти CPU.
- `difficulty-presets` + `operator-settings` (DIP-налаштування автомата; в ACA — у меню).
- `leaderboard-online` (ACA NEOGEO, 2018) + `leaderboard-local`.
- `continue` за монети.

## Варіації й родичі
- Face (перша гра для Neo Geo, продюсер Kenichi Iwanaga), видавець SNK; версія Neo Geo CD анонсована, але не вийшла; ACA NEOGEO від Hamster (2018).
- Родичі в корпусі: [Columns](columns.md) і [Puyo Puyo](puyo-puyo.md) (з ними порівнює Wikipedia), [Hextris](hextris.md) (обертання цілого поля, але без перебудови гравітацією), [Magical Drop](magical-drop.md) (гравітація в інший бік).
- **Осі варіацій**:
  - **що обертає гравець**: фігуру (Tetris, Puyo) / колір у фігурі (Columns) / усе поле (Gururin, Hextris);
  - **гравітація**: завжди вниз / змінюється з поворотом поля (Gururin; Bone Cruncher у сімʼї dig-gravity);
  - **зчеплені фігури**: розпадаються після приземлення (Puyo) / тримаються разом (Gururin, «за руки»).

## Цікавинки для курсу
- Поворот квадратного поля на ±90/180° як транспонування + віддзеркалення матриці — 🌱.
- Перебудова стеку після повороту: повторна гравітація в новий низ, з групами, що падають цілим — 📎.
- Звʼязані пари людей («за руки»), що падають як одна фігура й лишають дірки — 📎.
- Стрілка-підказка: перебрати 3 повороти, змоделювати падіння й знайти збіг — 🥉.
- Versus із черепами-сміттям — 🥉.

## Мапа на каталог
- Є: `gravity-fall` ↔ падіння людей; `keyboard-controls` ↔ джойстик+A/B; `line-match-clear` ↔ 3 в ряд; `chain-reaction` ↔ ланцюги (?); `ai-opponent` + `simultaneous-versus` ↔ Challenge і 2P; `garbage-attack` ↔ черепи; `mode-select`; `game-over-continue`; `score-records` + `leaderboard` ↔ high score, онлайн-рейтинг ACA; `difficulty-levels`.
- **Нема** → пропозиції карток:
  - `+shifting-gravity` (Bone Cruncher) — тут {by: player-rotation}; `+linked-pieces` (Pushmo) — люди «за руки»; `+cascade-gravity` — уже в корпусі.
  - `+rotate-whole-field` «Хід — поворот усього поля на 90°/180°, гравітація перебудовує стек» · entities/move · 📎 · слоти {angles: 90|180, field: square}.
  - `+hint-arrow` «Стрілка підказує напрям повороту для збігу» · interface/hud · 🥉.

## Пропозиції до словників
- `+effect:rotate_field` — повернути все поле разом зі стеком (відрізняється від `rotate(a)` сутності: міняє напрям гравітації); можна виразити `rotate(field, deg)`, але кодові потрібна окрема семантика.
- `+axis:gravity-rotating` — нове значення осі `gravity`: напрям «вниз» залежить від орієнтації поля (поруч із `gravity-shifting` Bone Cruncher).
- `+ui:rotation-hint` — стрілка-підказка повороту.
- `+card:rotate-whole-field`, `+card:hint-arrow` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Gururin](https://en.wikipedia.org/wiki/Gururin) — A/B обертають арену, 3 одного кольору по вертикалі/горизонталі, стрілка-підказка, «тримаються за руки», versus, поразка й continue, Face/SNK, ACA 2018.
- [neo-geo.com: огляд](https://neo-geo.com/reviews/neo-reviews/Gururin/gururin.html) — квадратна яма, поворот 90° і 180° утриманням, обертається яма, а не люди, черепи-цеглини супернику.
- [arcade-history](https://www.arcade-history.com/game/1054/) — трійки людей, «rotate the puzzle itself», A — вліво, B — вправо, 2 гравці, травень 1994.
- [Nintendo eShop: ACA NEOGEO GURURIN](https://www.nintendo.com/us/store/products/aca-neogeo-gururin-switch/) — режими One Player / Challenge (VS CPU) / Two Player, налаштування, онлайн-рекорди, Hamster, 12.04.2018.
- YouTube: пошук «Gururin Neo Geo gameplay».

## Непевне
- (?) Чи осідає вже покладений стек після повороту в новий низ — рядок черги й логіка кажуть так, огляди прямо не пишуть.
- (?) Пари у versus і трійки в соло — з пошукового уривку Nintendo Life (сама сторінка 403).
- (?) Розмір ями, бонус ланцюга, очки, як прибирається череп-цеглина, чи є next-preview — не знайдено.
- (?) Дата: Wikipedia — 25.05.1994; деякі каталоги — 25.01.1994.
- (?) JA-вікі статті про гру не має (лише неоднозначність «ぐるりん»).
