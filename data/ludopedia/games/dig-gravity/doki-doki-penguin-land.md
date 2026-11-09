---
title: Doki Doki Penguin Land (ドキドキペンギンランド)
slug: doki-doki-penguin-land
aka: [ドキドキペンギンランド, Penguin Land, Doki Doki Penguin Land Uchuu Daibouken, Ikasuze! Ai no Doki Doki Penguin Land MD]
family: dig-gravity
also: [grid-platformer]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: state
year: 1985
platforms: [SG-1000, MSX, arcade, Master System (1987), Mega Drive (1991), Game Boy]
links:
  - {kind: other, url: "https://www.hardcoregaming101.net/doki-doki-penguin-land/amp/", best: true, note: "HG101: огляд усієї серії — блоки, яйце й лінія падіння, ведмеді, кроти, скрол, запасні яйця, редактор SMS, відмінності MD/GB/Arrange"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Doki_Doki_Penguin_Land", note: "серія: довести яйце донизу, руйнуючи й зсуваючи блоки; яйце не можна впускати занадто далеко"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Penguin_Land", note: "Master System (1987): лід, тріснутий лід, камені, пружини, труби, Gangow, Cameel, привиди, 50 стадій і редактор на 15"}
  - {kind: other, url: "https://www.smspower.org/Games/DokiDokiPenguinLand-SG", note: "SMS Power: SG-1000, 1985, 1–2 гравці по черзі, текст коробки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Doki+Doki+Penguin+Land+SG-1000+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-by-input, gravity-fall, dig-terrain, dig-hole, push-object, destructible-blocks, impassable-cells, one-way-cell, touch-death, environment-death, item-pickup, event-points, time-bonus, player-camera, sequential-levels, level-select, hidden-under-block, in-game-editor, editor-palette, save-game, undo-step, checkpoint, +carry-goal-object, +fall-height-death, +crush-by-fall, +stun-not-death, +pit-trap-enemy, +egg-thief, +scroll-follows-cargo, +cargo-only-passage, +idle-punisher, +invert-buttons, +spring-jump, +egg-shield]
proposes: ["+trigger:landed", "+cond:fall_height", "+role:cargo", "+card:carry-goal-object", "+card:egg-thief", "+card:scroll-follows-cargo", "+card:cargo-only-passage", "+card:stun-not-death"]
author: opus
date: 2026-11-09
---

# Doki Doki Penguin Land — пінгвін прокопує шлях крихкому яйцю донизу, поки ведмеді б'ються, а кроти крадуть

## Суть
Бічний вид, вертикальна шахта з цегли: пінгвін Adelie має довести **яйце** з верху рівня до низу, до своєї пінгвінки. Яйце — пасивний вантаж: воно котиться від поштовху й падає, але **розбивається**, якщо пролетить надто далеко (нижче лінії за три поверхи) або торкнеться ворога. Пінгвін сам не гине — його лише оглушують, — тому вся напруга в долі яйця: копати так, щоб воно падало потроху, підставляти камені-платформи, давити білих ведмедів каменями чи ловити їх у викопані ями. Гра — спільний предок «ескорт-копалок»; сиквел на Master System (1987) — **Penguin Land** з редактором рівнів.

## Поле і час
- Вертикальна шахта: цегла (копається), суцільні підлоги (не копаються), люки, камені. Real-time.
- **Камера йде за яйцем**: екран скролиться донизу лише настільки, наскільки впало яйце; пінгвін, що забіг далеко вперед, зʼявляється згори екрана. Видно не весь рівень — `info: partial`.
- «Лінія падіння»: на екрані показано межу на три поверхи нижче яйця — далі воно не переживе падіння (SMS: «більше 3 блоків»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Adelie (пінгвін) | player | невмирущий | ходить, стрибає, копає цеглу, штовхає яйце й камені; від удару ведмедя на кілька секунд оглушений |
| Яйце | object (вантаж) | запасних 3 | котиться від поштовху, падає без опори; розбивається від падіння за лінію, від ворога, від каменя згори |
| Цегла | terrain | — | пінгвін вибиває → порожня клітина; кроти з неї вилазять |
| Суцільна підлога | static | — | не копається |
| Камінь | object | — | вибивається/зсувається; падає; ловить яйце як платформа; падаючи — давить ведмедя |
| Люк | terrain | лише для яйця | яйце провалюється на нижчу ділянку; пінгвін — ні, мусить шукати обхід |
| Білий ведмідь | enemy | — | б'є пінгвіна (оглушення) і загрожує яйцю; гине від каменя згори або у викопаній ямі |
| Кріт | enemy | боягуз | вилазить із цегли, щоб украсти лишене яйце; тікає, коли пінгвін поруч |
| Серце | pickup | — | лише очки |
| Пінгвінка / дно рівня | static | — | ціль: яйце дісталося низу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(adelie, dir)`; КОЛИ `input(jump)` → ТО `custom: «стрибок»`.
- КОЛИ `input(dig)` → ЯКЩО `cell(target, brick)` → ТО `set_cell(target, empty)`; ЯКЩО `cell(target, solid_floor)` → ТО `block`. Напрям копання — (?).
- КОЛИ `contact(adelie, egg)` → ЯКЩО `moving(adelie, left|right)` and `free(cell_behind)` → ТО `push(egg)` — яйце котиться.
- КОЛИ `tick` → ЯКЩО `not supported(egg)` → ТО `fall(egg)`; те саме для каменів.
- КОЛИ `custom: «яйце приземлилось»` → ЯКЩО `custom: «пролетіло нижче лінії за три поверхи»` → ТО `transform(egg, broken)`, `counter(eggs, -1)`, `restart`.
- КОЛИ `contact(egg, enemy)` → ТО `transform(egg, broken)`, `counter(eggs, -1)`, `restart`.
- КОЛИ `contact(rock, egg)` → ЯКЩО `moving(rock, down)` → ТО `transform(egg, broken)` (SMS; в оригіналі — (?)).
- КОЛИ `contact(rock, bear)` → ЯКЩО `moving(rock, down)` → ТО `disappear_b`, `score(+n)`.
- КОЛИ `enter(bear, dug_hole)` → ТО `custom: «ведмідь вибуває в ямі»` (?).
- КОЛИ `contact(bear, adelie)` → ТО `stun(adelie, n)` — пінгвін не гине.
- КОЛИ `enter(egg, trapdoor)` → ТО `fall(egg)`; КОЛИ `enter(adelie, trapdoor)` → ТО `block`.
- КОЛИ `custom: «яйце лишилось без пінгвіна»` → ТО `spawn_at(mole, brick)`, `custom: «кріт іде красти яйце»`; КОЛИ `in_range(mole, adelie, n)` → ТО `custom: «кріт тікає назад у цеглу»`.
- КОЛИ `contact(adelie, heart)` → ТО `pickup`, `score(+n)`.
- КОЛИ `custom: «яйце впало нижче краю екрана»` → ТО `camera(down)`; КОЛИ `edge(adelie)` (низ) → ТО `custom: «зʼявляється згори екрана»`.
- КОЛИ `reach(egg, bottom)` → ТО `win`, `next_level`.
- КОЛИ `counter(eggs, ==, 0)` → ТО `game_over`.
- Перемога: яйце внизу. · Поразка: розбиті всі яйця. · Рахунок: серця, ведмеді; на SMS — бонус за час і складність раунду.

## Керування і ввід
- Хрестовина: ходьба вліво-вправо; кнопки — стрибок і копання/удар (точна розкладка — (?)). Яйце й камені штовхаються ходьбою в них.
- 1–2 гравці по черзі (SG-1000).
- SMS: пауза дає прокрутити весь рівень і роздивитися маршрут.

## Вікна, меню, HUD
- `splash-screen` / титул з вибором 1 або 2 гравців.
- `game-screen`: шахта зі скролом за яйцем; лінія граничного падіння під яйцем; `score`, запасні яйця (`lives`), `level-number` (?); SMS — `timer-countdown`.
- `pause-menu` (SMS): пауза з прокруткою рівня.
- `level-select` (SMS): перші 30 з 50 стадій.
- `editor-window` (SMS): редактор рівнів, збереження до 15 рівнів у батарейній памʼяті картриджа.
- `end-screen` / game over.
- Переходи: титул → game-screen → (яйце внизу) наступний рівень; (яйце розбилось) → той самий рівень; (яєць нема) → game over.

## Фічі поза полем
- `levels-sequential`: SG-1000 — 25 рівнів; SMS — 50 (30 на вибір); MD — 30; GB — 25 (стадії оригіналу з елементами SMS).
- `level-editor` + `save-slots` (SMS): 15 власних рівнів у батарейній памʼяті — перша домашня консольна гра з батарейним збереженням; обмеження редактора — без рухомих шипів, не більше 5 ведмедів.
- `checkpoint` + `undo` (MD, 1991): прапорець-рестарт із цього місця і скасування.
- `hotseat`: два гравці по черзі (SG-1000).

## Варіації й родичі
- **Penguin Land / Doki Doki Penguin Land Uchuu Daibouken** (Master System, 1987) — те саме ядро, інші сутності: лід (пінгвін розтоплює), тріснутий лід (тане, коли на ньому яйце), камені (можна штовхати й скидати на ворогів, але розбивають яйце), камʼяні блоки (не рухаються, але іноді їдуть самі), пружини (вищий стрибок), труби (проходять і яйце, і пінгвін), щит яйця; Gangow (ведмідь атакує пінгвіна й яйце, розбиває його, загнавши в кут або стрибнувши), Cameel (птах прилітає, якщо яйце довго не рухалось, і скидає цеглину), привид (ховається в блоках; звільнений — інвертує керування до кінця рівня); блоки, що ростуть і зменшуються, ширяючі платформи, шипи зі стелі; три пташенята на дні. Нове правило: пінгвін, що стрибнув на яйце, яке нікуди відкотитись, — розбиває його.
- **Ikasuze! Ai no Doki Doki Penguin Land MD** (Mega Drive, 1991): крила (кращий стрибок), сталева шкаралупа (тимчасово незламне яйце), прапорець і undo; Arrange — подушки (рятують від падіння, давлять ведмедів), гарячі плити (варять яйце), тюлені (ковтають яйце), привиди після кінця часу.
- Родичі в корпусі: [Lemmings](lemmings.md) і [Survivors](survivors.md) (довести вразливих донизу), [Dig Dug](dig-dug.md) (камінь на ворога, ями), [Mr. Driller](mr-driller.md) (копати вниз), [Dot Valley](dot-valley.md) і [Repton](repton.md) (яйця, що падають).
- **Осі варіацій**: вантаж — «герой сам (Boulder Dash) / пасивний вантаж, що котиться (яйце) / юрба-автомат (Lemmings)»; крихкість — «висота падіння / дотик ворога / удар згори / притиснутий без виходу»; камера — «за героєм / за вантажем (тут)».

## Цікавинки для курсу
- Вантаж-ескорт: пасивне яйце з гравітацією, поштовхом і трьома причинами розбитися — 🥉.
- Лінія граничного падіння, намальована під яйцем (поріг висоти як видимий HUD) — 📎.
- Камера за вантажем, а не за гравцем, і «телепорт» гравця на верх екрана — 📎.
- Люк, що пропускає лише вантаж, — фільтр прохідності за типом сутності — 🌱.
- Кріт-злодій, що зʼявляється, коли вантаж лишено, і тікає від гравця — 🥉 (два режими поведінки за відстанню).
- Птах-каратель за бездіяльність (SMS) — 🌱; привид з інверсією керування — 🌱.
- Редактор рівнів із жорсткими лімітами (≤ 5 ведмедів, без рухомих шипів) і збереженням у слотах — 🥈.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` ↔ яйце й камені · `dig-terrain` ↔ цегла → порожньо · `dig-hole` ↔ ями для ведмедів · `push-object` ↔ яйце/камені · `destructible-blocks` ↔ цегла · `impassable-cells` ↔ суцільні підлоги · `one-way-cell` ↔ люки (лише вниз і лише для яйця) · `touch-death` + `environment-death` ↔ яйце від ворога й падіння · `item-pickup` + `event-points` ↔ серця · `time-bonus` (SMS) · `player-camera` ↔ скрол (тут за яйцем) · `sequential-levels` + `level-select` · `hidden-under-block` ↔ привид у блоці (SMS) · `in-game-editor` + `editor-palette` + `save-game` (SMS) · `undo-step` + `checkpoint` (MD).
- **Нема** → пропозиції карток:
  - `+carry-goal-object` (вже пропонована) — тут вантаж котиться й падає сам.
  - `+fall-height-death` (вже пропонована) — поріг для яйця, лінія на екрані.
  - `+crush-by-fall` (вже пропонована) — камінь на ведмедя.
  - `+stun-not-death` «Гравця не вбивають — оглушують на N тіків» · entities/state · 🌱.
  - `+pit-trap-enemy` «Викопана яма ловить ворога» · entities/interact · 📎 (родич `hole-refill`).
  - `+egg-thief` «Злодій вантажу: приходить, коли вантаж лишено, тікає від гравця» · entities/move · 🥉.
  - `+scroll-follows-cargo` «Камера за вантажем; гравець, що випередив, переноситься на верх екрана» · interface/render · 📎.
  - `+cargo-only-passage` «Прохід лише для певного типу сутностей» · entities/legality · 🌱.
  - `+idle-punisher` (вже пропонована) — Cameel за бездіяльність.
  - `+invert-buttons` (вже пропонована) — привид.
  - `+spring-jump` «Пружина — вищий стрибок» · entities/move · 🌱; `+egg-shield` «Щит вантажу на час / на одне падіння» · entities/state · 🌱.

## Пропозиції до словників
- `+trigger:landed` — сутність приземлилась після падіння (повтор з Lemmings).
- `+cond:fall_height(a, op, n)` — висота падіння порівняно з N (повтор з Lemmings, Leap Year).
- `+role:cargo` — пасивний обʼєкт-ціль, який треба доставити цілим (яйце); відрізняється від `object` тим, що його втрата — поразка.
- `+card:carry-goal-object`, `+card:egg-thief`, `+card:scroll-follows-cargo`, `+card:cargo-only-passage`, `+card:stun-not-death` — див. «Мапа на каталог».

## Джерела
- ⭐ [HG101: Doki Doki Penguin Land](https://www.hardcoregaming101.net/doki-doki-penguin-land/amp/) — оригінал SG-1000: копання цегли, суцільні підлоги, люки лише для яйця, камені-платформи, лінія падіння на три поверхи, ведмеді й ями, кроти-злодії, серця, скрол за яйцем, 3 запасних яйця, 25 рівнів; SMS/MD/GB/Arrange: нові блоки, вороги, редактор і його ліміти, прапорець і undo.
- [Wikipedia: Doki Doki Penguin Land](https://en.wikipedia.org/wiki/Doki_Doki_Penguin_Land) — ядро серії і випуски (SG-1000/MSX 1985, SMS 1987, MD 1991).
- [Wikipedia: Penguin Land](https://en.wikipedia.org/wiki/Penguin_Land) — SMS 1987: «яйце розбивається, якщо впаде більше ніж на 3 блоки», правило стрибка на яйце, лід, камені, пружини, труби, Gangow, Cameel, привиди, очки, 50 стадій і редактор на 15 у батарейній памʼяті.
- [SMS Power: Doki Doki Penguin Land (SG-1000)](https://www.smspower.org/Games/DokiDokiPenguinLand-SG) — дата, 1–2 гравці по черзі, текст коробки («білі ведмеді, кроти й суперники в коханні»).
- YouTube: пошук «Doki Doki Penguin Land SG-1000 gameplay».

## Непевне
- (?) Напрям копання (лише вниз чи й убік), кнопки, HUD SG-1000 — не знайдено; суперник «у коханні» з тексту коробки як ворог не описаний.
- (?) Чи ведмідь у ямі гине чи лише застрягає; чи в оригіналі камінь розбиває яйце (точно — у SMS).
- (?) Одна переказана фраза HG101 каже, що після розбитого яйця «в зоні зʼявляються ведмеді» — не ясно, до якої версії це стосується.
- (?) Аркадна версія — «та сама гра в кабінеті»; відмінностей MSX-порту не знайдено. JA-вікі статті про гру нема.
