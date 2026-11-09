---
title: "Code Name: Sector"
slug: code-name-sector
aka: [Code Name Sector, CODE NAME SECTOR]
family: hidden-deduction
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: both
  goal: score
year: 1977
platforms: [electronic board (Parker Brothers), web (HTML5-версія)]
links:
  - {kind: other, url: "https://rulespal.com/code-name-sector/rulebook", best: true, note: "Teach Mode покроково: дисплей, компас, RANGE, F-дальність пострілу, OFF 1 / OFF 2 / SOS, очки"}
  - {kind: other, url: "http://www.hasbro.com/common/instruct/codenamesector.pdf", note: "скан оригінальних правил: лінія дальності — квадрат, LIMIT LINE, Evasive Sub, обмеження стрільби (рис. 21), Sub Finder, рахунок"}
  - {kind: play, url: "https://thatmichaelpark.github.io/code-name-sector/", note: "HTML5-версія: Regular / Evasive / Sub Teach Mode, AUTO-PLOT, Battle Log; Sub Finder не реалізовано"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=code+name+sector+parker+brothers", note: "пошук; огляди й геймплей"}
stage: v1
coverage: 65
mechanics: [move-8dir, hot-seat, turn-enforcement, event-points, difficulty-levels, tutorial-window, mode-select, message-log, game-screen, +range-only-sonar, +steady-course-target, +compass-ray-firing, +depth-guess-feedback, +limit-line-bounce, +evasive-turn-on-miss, +retaliation-displacement, +shared-info-rival-hunters, +manual-plot-chart, +belief-set-tracking]
proposes: ["+effect:report_range", "+cond:on_compass_ray", "+ui:compass-lights", "+ui:range-display", "+ui:plot-chart", "+feature:auto-plot", "+feature:recall-display", "+card:range-only-sonar", "+card:steady-course-target", "+card:compass-ray-firing", "+card:depth-guess-feedback", "+card:limit-line-bounce", "+card:evasive-turn-on-miss", "+card:retaliation-displacement", "+card:shared-info-rival-hunters", "+card:manual-plot-chart"]
author: opus
date: 2026-11-09
---

# Code Name: Sector — есмінці полюють на невидиму субмарину: комп'ютер каже лише дальність, курс і глибину треба вивести крейдою на карті

## Суть
Електронна настільна гра Parker Brothers: до чотирьох есмінців (гравців або одного гравця за всіх) шукають субмарину, яку веде вбудований комп'ютер. Субмарина невидима, рухається **сталим курсом** на 1 точку щоходу корабля й має сталу глибину 1–3; кнопка RANGE дає лише дальність від свого корабля. Гравці крейдою малюють на карті «лінії дальності» (квадрати), перетинають їх і виводять позицію та курс. Стріляти можна лише на ≤2 точки по одному з 8 компасних напрямків; влучання вимагає ще й угадати глибину, а промах повз напрямок викликає відповідь субмарини.

## Поле і час
- Карта — сітка точок (перетинів ліній) з координатами 25N–50N × 25E–50E; кораблі стартують з позицій 1–4 у нижньому лівому куті (Ship 1 — 35N 25E).
- Червона пунктирна LIMIT LINE обмежує район субмарини; кораблі можуть вийти й за край карти.
- Дальність — у «точках» по горизонталі, вертикалі й діагоналі: лінія дальності — **квадрат** навколо корабля (метрика Чебишова; дальність 10 → квадрат, на якому лежить субмарина).
- Хід: кораблі ходять за фіксованою чергою 1 → 2 → 3 → 4; кожне NEXT SHIP зсуває субмарину на 1 точку.
- Шари: справжній стан у комп'ютері (позиція, курс, глибина) + карта гравців із крейдовими лініями.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Субмарина | enemy | позиція, курс (8 напрямків), глибина 1–3 (стала), +1 точка за хід корабля | невидима; йде сталим курсом; біля LIMIT LINE розвертається; в режимі Evasive після промаху може звернути на 45° |
| Есмінець (Ship 1–4) | player | позиція N/E, курс (8 напрямків), швидкість 0–9 | щоходу — курс і швидкість, рух на «speed» точок; RANGE; один постріл за хід |
| LIMIT LINE | zone | червона пунктирна межа | субмарина не виходить за неї |
| Постріл (глибинна атака) | projectile | напрям (8), глибина 1–3 | результат миттєвий: SUB / OFF 1 / OFF 2 / SOS |
| Комп'ютер (Combat Information Center) | neutral | знає все | веде субмарину, рахує дальність, «подвійний агент» — допомагає й тобі, й суперникам |
| Карта й крейди | mark | 4 кольори (червоний, зелений, синій, чорний) | гравці вручну позначають позиції кораблів, лінії дальності, слід субмарини |
| Трофей-субмарина | resource | 8 штук | за кожну потоплену |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт: КОЛИ `game_start` → ТО `custom: «комп'ютер таємно задає позицію, курс і глибину субмарини»`; кораблі — на позиціях 1–4.
- КОЛИ `turn_start(ship)` (кнопка NEXT SHIP) → ТО `move(sub, course)` на 1 точку; дисплей показує швидкість, координати й курс корабля.
- КОЛИ `reach(sub, limit_line)` → ЯКЩО `custom: «субмарину не потоплено до наступного NEXT SHIP»` → ТО `move(sub, inward)` на 1 точку, `custom: «новий курс — один із трьох від лінії»`.
- КОЛИ `input(range)` → ТО `custom: «показати дальність = max(|ΔN|, |ΔE|) від свого корабля»`.
- КОЛИ `input(range)` → ЯКЩО `custom: «субмарина ≤ 2 точки по одному з 8 компасних напрямків»` → ТО `custom: «перед числом F (дозвіл стріляти)»`; на дальності 0–1 F є завжди; дальність 0 → «FO» (прямо над субмариною, цілитись можна будь-куди).
- КОЛИ `input(left|right)` → ТО `face(ship, ±45°)`.
- КОЛИ `input(faster|slower)` → ТО `speed(ship, ±1)` у межах 0–9.
- КОЛИ `input(move_ship)` → ТО `move(ship, course)` на «speed» точок.
- КОЛИ `contact(ship, ship)` → ТО `message(«COLL»)`, `teleport(ship, random)`, `face(ship, random)`; швидкість лишається.
- КОЛИ `edge(ship)` → ТО `message(«OFF CHART»)`; наступним ходом корабель повертається, взявши курс назад.
- КОЛИ `input(aim, dir)` + `input(fire, depth)` → ЯКЩО `custom: «є F і субмарина в напрямку dir»` і `same(depth, sub_depth)` → ТО `message(«SUB»)`, `score(10)`, `win`.
- … ЯКЩО `custom: «напрям влучний, глибина відрізняється на 1»` → ТО `feedback(«OFF 1»)`, `score(5)`; на 2 → `feedback(«OFF 2»)`, `score(3)` (вистріл на глибину 2 → OFF 1 означає 1 або 3).
- … ЯКЩО `custom: «напрям хибний або F нема»` → ТО `feedback(«SOS»)`, `teleport(ship, random)`, `face(ship, random)` — субмарина відповідає, швидкість та сама.
- Один постріл за хід: `custom: «не більше одного FIRE на хід корабля»`.
- КОЛИ `custom: «невдалий постріл (OFF 1 / OFF 2 / SOS)»` → ЯКЩО `mode(evasive)` → ТО `rotate(sub, −45° | 0 | +45°)` — глибини й швидкості не змінює.
- КОЛИ `input(recall)` → ТО `custom: «повторно показати дисплей (після SOS/COLL — нова позиція й курс)»`.
- КОЛИ `input(sub_finder)` → ТО `reveal(sub)`: позиція, глибина, курс (спрощує гру).
- КОЛИ `input(range)` після перемоги → ТО `restart` з поточних позицій; вимкнути/увімкнути → нова гра з порту.
- Перемога: потопити субмарину першим (трофей) або набрати узгоджену суму очок (новачкам 15, ветеранам 35+) · Поразка: нема · Рахунок: SUB 10 · OFF 1 — 5 · OFF 2 — 3.

## Керування і ввід
- Кнопки Combat Information Center: RANGE, MOVE SHIP, NEXT SHIP, FASTER, SLOWER, LEFT, RIGHT, AIM, FIRE, RECALL, SUB FINDER, EVASIVE SUB, TEACH MODE.
- Курс — вісім ламп компаса (LEFT/RIGHT крутить на 45°); вибір глибини — цифра, що блимає на дисплеї (гравці прикривають дисплей рукою від суперників).
- Карта — крейди й паралельна лінійка: позиції кораблів кольором корабля, квадрати дальності, слід субмарини.
- Гравці: від 1 (усі 4 кораблі) до 4; удвох — кораблі 1+3 проти 2+4; соло з меншою кількістю кораблів — «пропускати» кораблі NEXT SHIP.
- HTML5-версія: ті самі кнопки, глибина — випадний список, AUTO-PLOT (комп'ютер сам малює), інструменти Eraser / Ship 1–4 / Clear All.

## Вікна, меню, HUD
- `game-screen` (пристрій): дисплей SHIP · SPEED · NORTH · EAST · DEPTH · RANGE + компас з 8 лампами; повідомлення F2, FO, SUB, OFF 1, OFF 2, SOS, COLL, OFF CHART.
- Карта на коробці — `plot-chart`: сітка 25–50 × 25–50, позиції 1–4, LIMIT LINE.
- HTML5-версія: `mode-select` (Regular / Evasive / Sub Teach Mode, зміна — через RESTART), панель AUTO-PLOT, `message-log` (Battle Log), полотно-карта з інструментами.
- `tutorial-window`: Teach Mode — заскриптована гра на 9 ходів з покроковими вказівками в книжці.
- Переходи: увімкнення → (Teach Mode | гра) → SUB → RANGE (продовжити) / вимкнути (нова гра з порту).

## Фічі поза полем
- `tutorial` (Teach Mode, 9 ходів), режим складності Evasive Sub (`difficulty-presets`), `show-solution` (SUB FINDER).
- `local-multiplayer` 1–4 гравці за одним пристроєм; рахунок трофеями або очками з порогом, який гравці домовляються заздалегідь.
- HTML5: `auto-check`-подібний AUTO-PLOT (комп'ютер малює за гравця), журнал бою.
- Енергоощадження: дисплей гасне до двох крапок за ~30 с, RECALL повертає.

## Варіації й родичі
- [Battleship](battleship.md) — пошук прихованого флоту пострілами; тут ціль рухається, а відгук — дальність замість «попав/мимо».
- [Captain Sonar](captain-sonar.md) — субмарина, яку виводять з оголошених курсів; [Hunt the Wumpus](hunt-the-wumpus.md) — невидима ціль і стріла в напрямку; [Triangulation](triangulation.md), [Black Box](black-box.md) — дедукція позиції з вимірювань.
- Комп'ютерні «sub hunt»-ігри 1970-х (Sonar, Seawolf) (?) — та сама ідея пінгів.
- **Осі варіацій**: відгук «дальність / пеленг / обидва»; метрика дальності «Чебишов (квадрат) / Евклід (коло) / Манхеттен (ромб)»; ціль «стоїть / сталий курс / ухиляється»; постріл «будь-куди / лише по 8 променях ≤2»; невідомий вимір «нема / глибина 1–3»; гравці «співпраця / суперники зі спільною інформацією».

## Цікавинки для курсу
- Дальність Чебишова й «квадрат дальності» на карті, перетин квадратів кількох кораблів — 📎.
- Ціль зі сталим курсом: множина гіпотез (позиція × курс × глибина) і її фільтр після кожного RANGE — 🥈 (класичне відстеження цілі).
- Постріл по 8 променях ≤2 з F-дозволом і відгуком OFF n за різницею глибин — 🌱.
- Відбиття від LIMIT LINE (на 1 точку всередину, новий курс з 3) — 📎.
- Evasive: поворот ±45° після промаху — оновлення гіпотез розгалуженням — 🥉.
- SOS / COLL: відкидання корабля у випадкову позицію з новим курсом — 🌱.
- AUTO-PLOT: комп'ютер малює лінії дальності за гравця — 📎.

## Мапа на каталог
- Є: `move-8dir` ↔ курс на 8 напрямків; `hot-seat` + `turn-enforcement` ↔ черга кораблів 1→4; `event-points` ↔ SUB 10 / OFF 1 — 5 / OFF 2 — 3; `difficulty-levels` ↔ Regular / Evasive; `tutorial-window` ↔ Teach Mode; `mode-select` ↔ вибір режиму в HTML5; `message-log` ↔ Battle Log; `game-screen` ↔ дисплей + компас.
- **Нема** → пропозиції карток:
  - `+range-only-sonar` «Сенсор дає лише дальність до цілі» · game-logic/info · 📎 · слот {metric: chebyshev}.
  - `+steady-course-target` «Невидима ціль рухається сталим курсом» · entities/move · 🌱.
  - `+compass-ray-firing` «Постріл лише по 8 компасних променях на ≤N» · entities/combat · 🌱 · слот {range: 2}.
  - `+depth-guess-feedback` «Прихований вимір (глибина) і відгук різницею» · game-logic/info · 🌱.
  - `+limit-line-bounce` «Межа району: ціль розвертається всередину» · entities/move · 📎.
  - `+evasive-turn-on-miss` «Ціль ухиляється (±45°) після промаху» · entities/move · 📎.
  - `+retaliation-displacement` «Хибний постріл → тебе відкидає у випадкову позицію» · entities/combat · 🌱.
  - `+shared-info-rival-hunters` «Мисливці-суперники бачать відгуки одне одного» · game-logic/players · 🌱.
  - `+manual-plot-chart` «Карта для ручних позначок гравця (крейда / олівець)» · interface/input · 📎.
  - `+belief-set-tracking` (Scotland Yard) — множина можливих станів субмарини.

## Пропозиції до словників
- `+effect:report_range` — повідомити гравцю відстань від його сутності до прихованої.
- `+cond:on_compass_ray` — ціль на одному з 8 променів від сутності в межах N.
- `+ui:compass-lights` — 8 ламп напрямку (курс / приціл).
- `+ui:range-display` — числовий дисплей дальності з префіксом-статусом (F, FO).
- `+ui:plot-chart` — поле-карта для ручних позначок гравця.
- `+feature:auto-plot` — комп'ютер сам малює лінії дальності на карті.
- `+feature:recall-display` — повторно показати останній вивід дисплея.

## Джерела
- ⭐ [RulesPal: Code Name: Sector](https://rulespal.com/code-name-sector/rulebook) — Teach Mode: компоненти, дисплей і компас, RANGE, швидкість 0–9, F, OFF 1/OFF 2/SOS, COLL, Evasive Sub, Sub Finder, очки.
- [Hasbro: правила (PDF, скан)](http://www.hasbro.com/common/instruct/codenamesector.pdf) — с. 4–5: лінія дальності — квадрат; с. 22–25: COLL, FO, OFF n за різницею глибин, нова гра; с. 26–27: обмеження стрільби (рис. 21), LIMIT LINE; с. 28–29: Evasive Sub, Sub Finder, Off Chart, соло, очки.
- [HTML5-версія](https://thatmichaelpark.github.io/code-name-sector/) — кнопки CIC, режими Regular / Evasive / Sub Teach Mode, AUTO-PLOT, Battle Log, інструменти карти.
- YouTube: пошук «code name sector parker brothers».

## Непевне
- (?) Чи субмарина завжди йде рівно на 1 точку за хід кожного корабля (так у Teach Mode і на с. 28 «Single-person play»), чи швидкість може бути іншою.
- (?) Ймовірності виборів комп'ютера (новий курс з трьох на LIMIT LINE, поворот у Evasive, позиція після SOS/COLL) — правила кажуть лише «випадково».
- (?) Точна форма LIMIT LINE у звичайній грі (на рисунках — прямокутник ~30–48 × 30–48) і чи субмарина може стартувати будь-де всередині.
- (?) Чи F-дозвіл враховує глибину — ні: глибину вгадують окремо; чи можна стріляти, коли F нема (так, але гарантований SOS).
- (?) Ранні комп'ютерні «sub hunt»-родичі (Sonar, Seawolf) — з памʼяті, не перевірено.
