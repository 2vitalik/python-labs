---
title: Knot in 3D
slug: knot-in-3d
aka: []
family: maze-arcade
also: []
klass: avatar
axes:
  field: 3d
  time: realtime
  opponent: ai
  info: partial
  random: none
  goal: survive
year: 1983
platforms: [ZX Spectrum 48K]
links:
  - {kind: other, url: "https://spectrumcomputing.co.uk/pub/sinclair/games-info/k/KnotIn3D.txt", best: true, note: "інструкція: сліди, до 4 переслідувачів, фази й маркери, очки за крок, faults, density, клавіші"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Knot_in_3D", note: "суть: 3D Light Cycles у сітці 16×16×16, вид від першої особи, рух лише вперед"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/entry/2729/ZX-Spectrum/Knot_in_3D", note: "картка ZXDB: New Generation, Malcolm E. Evans, Interface 2 і Kempston, огляди"}
  - {kind: other, url: "https://everygamegoing.com/larticle/Knot-In-3D-000/34955", note: "огляд ZX Computing: гра закінчується, коли забагато зіткнень зі слідами"}
  - {kind: other, url: "https://crashonline.org.uk/06/3d.htm", note: "Crash «3D or not 3D»: 3D Light Cycles, заповнити простір раніше за компʼютер"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Knot+in+3D+ZX+Spectrum", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-auto, orientation-state, realtime-ai, ai-opponent, player-camera, event-points, keyboard-controls, game-pause, restart-level, attract-demo, status-panel, game-screen, +trail-wall, +first-person-view, +fault-limit, +phase-marker-reset, +density-meter, +relative-3d-turn]
proposes: ["+effect:leave_trail", "+effect:clear_trail", "+card:trail-wall", "+card:first-person-view", "+card:fault-limit", "+card:phase-marker-reset", "+card:relative-3d-turn", "+ui:density-meter", "+ui:crosshair"]
author: opus
date: 2026-11-09
---

# Knot in 3D — Tron-мотоцикл у кубі 16×16×16 від першої особи: ти лише повертаєш, слід лишається назавжди

## Суть
Гравець безупинно летить уперед крізь порожній тривимірний простір і лишає за собою слід; комп'ютерні «переслідувачі» роблять те саме своїми кольорами. Простір поступово заплітається у «вузол» слідів, і проходити крізь них стає дедалі важче — кожен прохід крізь слід записується як fault, а забагато faults завершують гру. Це тривимірна версія Light Cycles з фільму «Трон» з видом із кабіни; автор — Malcolm Evans (New Generation Software).

## Поле і час
- Сітка 16×16×16 клітин (4096 комірок), на старті порожня; рендер — перспективний вид від першої особи (видно лише те, що попереду) з перехрестям.
- Real-time: щотіку і гравець, і переслідувачі просуваються на клітину вперед; зупинитись не можна.
- Фази: коли гравець проходить маркери, починається нова фаза — простір очищається, додається ще один переслідувач (до 4).
- Що буває біля стінок куба — у «Непевне».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | напрям у 3D | рух лише вперед; поворот у 4 боки відносно погляду |
| Слід гравця | hazard | зелений або жовтий | лишається в кожній пройденій клітині; прохід крізь нього — fault |
| Переслідувач (chaser) | enemy | 1–4, червоні/сині; +1 за фазу | рухається так само, лишає слід свого кольору |
| Слід переслідувача | hazard | колір переслідувача | як слід гравця |
| Маркер | zone | — | пройти маркери → нова фаза |
| Порожня клітина | terrain | — | вільний простір; частка зайнятих — Density |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(player, forward)`, `custom: «лишити слід у клітині, з якої пішов»` (`+effect:leave_trail`), `score(1)`.
- КОЛИ `input(turn_dir)` (коротке натискання) → ТО `face(player, turn90 dir)` — вгору / вниз / ліворуч / праворуч відносно поточного погляду.
- КОЛИ `input(turn_dir)` (довше натискання) → ТО `face(player, turn90 dir)` ще раз (розворот на 180° двома поворотами).
- КОЛИ `input(turn_dir)` → ЯКЩО `custom: «клавішу цього напрямку не відпущено після попереднього повороту»` → ТО `block` (повторний поворот лише після відпускання).
- КОЛИ `enter(player, trail)` → ТО `counter(faults, +1)`; рух уздовж наявного сліду нараховує faults безперервно.
- КОЛИ `counter(faults, >=, limit)` → ТО `game_over` (ліміт — у «Непевне»).
- КОЛИ `tick` → ТО переслідувачі: `move(chaser, forward)`, `custom: «лишити слід свого кольору»`, поворот за власним AI.
- КОЛИ `reach(player, marker)` → ТО `custom: «очистити простір від усіх слідів»` (`+effect:clear_trail`), `spawn(chaser)`, `counter(phase, +1)`.
- КОЛИ `tick` → ТО `counter(density, = occupied / 4096)` — показник, чи лишились великі порожнечі.
- КОЛИ `input(H)` → ТО `custom: «пауза (hold)»`; КОЛИ `input(S)` → ТО `restart`.
- КОЛИ `input(BREAK)` → ЯКЩО `state(game, demo)` → ТО `custom: «вийти з демонстрації»`.
- Перемога: нема — гра на очки. Поразка: забагато faults. Рахунок: 1 очко за кожен крок уперед.

## Керування і ввід
- Курсорні клавіші ZX Spectrum, Interface 2 (правий порт) або Kempston-джойстик.
- Чотири повороти (вгору, вниз, ліворуч, праворуч) відносно напрямку погляду; газу й гальма нема — швидкість стала.
- Коротке натискання — один поворот на 90°, довше — ще один; перед повторним поворотом у той самий бік клавішу треба відпустити.
- H — пауза, S — рестарт, BREAK — вихід із демонстрації.

## Вікна, меню, HUD
- `attract-demo` — демонстраційний політ, вихід через BREAK.
- `game-screen` — перспективний вид із кабіни з перехрестям; під ним панель: `score` (кроки вперед), Density (заповненість простору), Faults (проходи крізь сліди), номер фази ліворуч (= кількість переслідувачів).
- Окремих меню, налаштувань і таблиці рекордів інструкція не описує.
- Переходи: завантаження → демонстрація → (BREAK) гра → (маркери) нова фаза → (ліміт faults) кінець; S — рестарт.

## Фічі поза полем
- `pause` (H), `restart-level` (S) — і все. Рівнів, складності, збережень нема; прогресія — фази з дедалі більшою кількістю переслідувачів.
- Завантаження у дві частини з магнітофона (файл «KNOT»).

## Варіації й родичі
- [Tron Light Cycles](tron-light-cycles.md), [Blockade](blockade.md), [Surround](surround.md) — той самий «слід = стіна» у 2D, де зіткнення — смерть.
- [Armagetron Advanced](armagetron-advanced.md) — 3D-рендер, але площина 2D; тут сама сітка тривимірна.
- [3D Monster Maze](3d-monster-maze.md) — та сама студія й автор (Malcolm Evans), теж вид від першої особи.
- **Осі варіацій:** поле сліду — 2D-площина / 3D-куб; вид — згори / від першої особи; зіткнення зі слідом — смерть / штраф (fault) з лімітом; слід — вічний / очищається за подією (маркер фази) / скінченний (Armagetron); суперники — один / додаються з фазами.

## Цікавинки для курсу
- 3D-сітка зайнятості 16³ і рух уперед з перевіркою клітини — 🌱 (масив 4096 булевих).
- Відносні повороти в 3D: орієнтація як пара векторів «вперед + вгору», поворот на 90° довкола осі — 🥉.
- Рендер слідів у перспективі від першої особи (воксельні блоки з відстанню) — 🥈.
- Штраф замість смерті: лічильник faults і безперервне нарахування при русі вздовж сліду — 🌱.
- AI переслідувача в 3D, що уникає слідів (оцінка вільного обʼєму по 6 напрямках) — 🥉.
- Показник Density і фаза, що очищає простір і додає суперника, — 📎.

## Мапа на каталог
- Є: `move-auto` ↔ рух уперед, ввід лише повертає · `orientation-state` ↔ напрям у 3D · `realtime-ai` + `ai-opponent` ↔ переслідувачі · `player-camera` ↔ вид із кабіни · `event-points` ↔ очко за крок · `keyboard-controls` · `game-pause` · `restart-level` · `attract-demo` ↔ демонстрація · `status-panel` ↔ Score/Density/Faults/Phase · `game-screen`.
- **Нема** → пропозиції карток:
  - `+trail-wall` (вже Blockade, Tron) — слід як перешкода; тут м'яка: прохід можливий зі штрафом.
  - `+first-person-view` (вже 3D Monster Maze) — рендер сітки з кабіни.
  - `+fault-limit` «Штраф за зіткнення замість смерті, ліміт штрафів» · game-logic/lose · 🌱 · слот {limit}.
  - `+phase-marker-reset` «Маркер фази: очистити поле, додати суперника» · levels/progression · 📎.
  - `+density-meter` «Показник заповненості поля» · interface/hud · 🌱.
  - `+relative-3d-turn` «Поворот відносно погляду в 3D» · entities/move · 🥉 · слот {turns: 4}.

## Пропозиції до словників
- `+effect:leave_trail` (вже ×11 у корпусі: Tron, Blockade, Xonix…) — сутність лишає слід у покинутій клітині.
- `+effect:clear_trail` — стерти всі сліди з поля (нова фаза).
- `+card:trail-wall`, `+card:first-person-view`, `+card:fault-limit`, `+card:phase-marker-reset`, `+card:relative-3d-turn` — див. «Мапу на каталог».
- `+ui:density-meter` — частка зайнятих клітин; `+ui:crosshair` — перехрестя по центру виду від першої особи.
- Вид із кабіни — слово коду `view: first-person` (поле), нового не треба.

## Джерела
- ⭐ [Інструкція Knot in 3D (txt)](https://spectrumcomputing.co.uk/pub/sinclair/games-info/k/KnotIn3D.txt) — сліди зелені/жовті, до 4 переслідувачів червоних/синіх, маркери і фази, очко за крок, fault за прохід крізь слід, Density, клавіші H/S/BREAK, короткі й довгі натискання.
- [Wikipedia: Knot in 3D](https://en.wikipedia.org/wiki/Knot_in_3D) — 16×16×16, вид від першої особи, постійний рух уперед, переслідувачі зі слідом іншого кольору, простір заповнюється.
- [ZXDB: Knot in 3D](https://spectrumcomputing.co.uk/entry/2729/ZX-Spectrum/Knot_in_3D) — New Generation Software, Malcolm E. Evans, Interface 2 і Kempston, перехрестя, перспективна 3D-графіка, огляди 1983–1984.
- [ZX Computing (everygamegoing)](https://everygamegoing.com/larticle/Knot-In-3D-000/34955) — гра закінчується, коли забагато зіткнень зі слідами; статус унизу екрана.
- [Crash: «3D or not 3D»](https://crashonline.org.uk/06/3d.htm) — «3D Light Cycles», заповнити простір раніше за компʼютер.
- YouTube: пошук «Knot in 3D ZX Spectrum».

## Непевне
- (?) Скільки faults дозволено до кінця гри — джерела кажуть лише «забагато».
- (?) Що відбувається біля меж куба 16×16×16: стіна, fault чи перехід на протилежний бік.
- (?) Як виглядають маркери, скільки їх треба пройти для нової фази і де вони стоять.
- (?) Чи зіткнення з самим переслідувачем (не слідом) — окрема подія.
- (?) Поведінка AI переслідувачів (переслідують гравця чи лише уникають слідів) і чи вона випадкова.
- (?) Чи довше натискання дає саме розворот на 180°, чи другий поворот іншої осі — інструкція: «довше натискання повертає ще раз».
