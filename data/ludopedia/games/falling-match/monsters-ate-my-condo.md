---
title: Monsters Ate My Condo
slug: monsters-ate-my-condo
aka: [MAMC]
family: falling-match
also: []
klass: cursor
axes:
  field: 1d
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2011
platforms: [iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Monsters_Ate_My_Condo", best: true, note: "чотири монстри, свайп поверху монстру його кольору, трійка 3+ міняє монстра, режими Endless і Timed Attack, умови поразки"}
  - {kind: other, url: "https://www.pocketgamer.com/monsters-ate-my-condo/review/", note: "рецензія: бронза → срібло → золото → діамант, сили всіх чотирьох монстрів, бетонні й бомбові поверхи, гнів і хитання вежі"}
  - {kind: other, url: "https://kotaku.com/monsters-ate-my-condo-is-colorful-candy-coated-kaiju-ma-5840972", note: "збіг лишає металевий поверх; монстр «здається» й міняє колір; сили Reginald і Lord Ferocious"}
  - {kind: other, url: "https://www.commonsensemedia.org/app-reviews/monsters-ate-my-condo", note: "поверхи падають у стос; виймаєш чужий колір, щоб зійшлись 3+; туторіал, досягнення"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Monsters+Ate+My+Condo+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [swipe-gestures, line-match-clear, gravity-fall, chain-reaction, event-points, score-records, time-out, temporary-modes, tutorial-window, achievements-window, mode-select, +feed-color-sink, +monster-swap-on-match, +star-up-merge, +tower-tilt-balance, +anger-meter, +garbage-adjacent-clear, +countdown-tile, +sink-power-on-special]
proposes: ["+cond:tilt", "+effect:tilt", "+card:feed-color-sink", "+card:monster-swap-on-match", "+card:tower-tilt-balance", "+card:sink-power-on-special"]
author: opus
date: 2026-11-09
---

# Monsters Ate My Condo — вийми поверх із хиткої вежі й віддай монстру його кольору, щоб решта поверхів зійшлась трійками

## Суть
Поле — одна вертикальна вежа з кольорових поверхів-кондо (1D), обабіч — два гігантські монстри з чотирьох. Гравець свайпом вліво чи вправо виймає будь-який поверх і згодовує його монстру з того боку: свій колір монстра тішить, чужий — злить. Вийнятий поверх дає верхнім осісти, і коли 3+ однакові поверхи опиняються поспіль, вони зникають, лишаючи металевий поверх; металеві теж збираються трійками в дорожчі. Ядро — одночасно «сортувати» стос через двох «смітників» з обмеженим смаком і тримати вежу рівною.

## Поле і час
- Поле — 1D: стос поверхів однієї ширини посеред екрана; новий поверх падає згори на стос (як саме й як часто — (?)).
- Ліворуч і праворуч — по монстру; кожен приймає «свій» колір.
- Real-time: потік поверхів не чекає; Time Attack — близько 2 хв, Endless — до поразки.
- Стан вежі — нахил/хитання: гнів монстрів і бомбові поверхи її розгойдують, вирівнює сила одного з монстрів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Поверх-кондо | tile | колір | лежить у стосі; свайп — летить до монстра; 3+ однакові поспіль — зникають |
| Металевий поверх (бронза → срібло → золото → діамант) | tile | рівень | лишається після збігу; три однакові → наступний рівень; «блискучий» — згодувати монстру = сила |
| Бетонний поверх | object | — | не виймається свайпом; знищується лише збігом поруч / довкола |
| Поверх-бомба | hazard | таймер (?) | дестабілізує вежу; прибирати так само, як бетон, і швидко |
| Монстр (Boat Head, Reginald Starfire, Mr. Shigoto, Lord Ferocious) | sink | колір, гнів | їсть поверхи; свій колір — задоволений; багато чужих — злиться й бʼє вежу; блискучий поверх → сила |
| Вежа | zone | нахил | вирівняна — гра триває; перекинулась — кінець |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(every)` → ТО `spawn_at(condo(random color), top)`, `fall(condo)` на стос (?).
- КОЛИ `input(swipe floor, left|right)` → ЯКЩО `not cell(floor, concrete)` → ТО `custom: «поверх вилітає з вежі до монстра з того боку»`, `fall(floors_above)`.
- КОЛИ `custom: «монстр зʼїв поверх»` → ЯКЩО `same(floor, monster, color)` → ТО `score(+n)` (монстр задоволений); інакше `counter(anger, +1)`.
- КОЛИ `counter(anger, ≥, max)` → ТО `custom: «монстр атакує вежу»`, `custom: «tilt — вежа хитається / нахиляється»`.
- КОЛИ `settled` → ЯКЩО `pattern(line(3+, same color))` уздовж вежі → ТО `clear(group)`, `spawn_at(metal_condo(bronze), group_place)`, `score(+n)`.
- КОЛИ `after(clear)` → ТО `custom: «монстр кольору групи «здається» й міняється на одного з трьох інших»`.
- КОЛИ `pattern(line(3, same metal tier))` → ТО `merge(metal ×3 → next tier)`: бронза → срібло → золото → діамант.
- КОЛИ `custom: «збіг поруч / довкола бетонного поверху»` → ТО `disappear(concrete)`; так само прибирається бомба.
- КОЛИ `custom: «бомба в стосі»` → ТО `custom: «tilt — дестабілізує вежу»`.
- КОЛИ `input(swipe shiny condo → monster)` → ТО сила монстра (замість продовження ланцюга металу):
  - Boat Head — `custom: «колискова»`, `speed(time, slow)`, `set_state(monsters, no_anger, dur)`;
  - Reginald Starfire — `custom: «вирівнює вежу»`, `set_state(tower, stable, dur)` (не впаде, доки сяє веселка);
  - Mr. Shigoto — `custom: «два блоки за кожне комбо»` (?);
  - Lord Ferocious — `multiplier(×10)` на всі очкові дії на час дії.
- КОЛИ `custom: «нахил вежі за межею»` → ТО `lose` (вежа впала).
- КОЛИ `custom: «забагато поверхів не того кольору»` → ТО `lose` (Wikipedia).
- КОЛИ `timer(time_attack, ==, 0)` → ТО `game_over` (Time Attack).
- Перемога: нема (очки) · Поразка: вежа перекинулась / монстрів розлютили · Рахунок: монстр свого кольору, збіги, металеві рівні аж до діаманта, множник ×10.

## Керування і ввід
- Свайп по поверху вліво або вправо — «згодувати» монстру з того боку; інших дій нема (SlashGear: «swipe left, or swipe right»).
- Блискучий металевий поверх — той самий свайп, але до монстра, чию силу хочеш.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Endless · Time Attack.
- `game-screen`: вежа посередині, два монстри з боків; `score`, `timer-countdown` (Time Attack); стан гніву монстра й хитання вежі — анімацією (окремого індикатора не підтверджено).
- `tutorial-window` — вбудоване навчання під час гри.
- `achievements-window` — довгий список досягнень.
- `end-screen` — підсумок очок, порівняння з рекордом.
- Переходи: main-menu → mode-select → game-screen → (вежа впала / час вийшов) end-screen.

## Фічі поза полем
- `mode-endless`, `mode-time-attack` (≈2 хв).
- `achievements`, рекорд (`leaderboard-local` (?)), `tutorial`.
- Складність зростає з грою (Common Sense Media), механізм — (?).

## Варіації й родичі
- Super Monsters Ate My Condo (2012): раунди на час «як у старих телешоу», рівні з нагородами й прокачкою, «погані» блоки з 4-го рівня — радше розширення, ніж нова механіка.
- **Осі варіацій «1D-стос»**: виймати будь-який поверх (MAMC) / лише верхній (стек LIFO, Water Sort `water-sort`) / зсувати рядок (Tetris-лінії `tetris`); **куди йде вийняте**: монстр-приймач із кольоровим смаком (MAMC) / пробірка (Water Sort) / нікуди (SameGame `samegame-flood`).
- Родичі: Tetris (повний ряд), Columns (`columns`, три в ряд по вертикалі), Triple Town / Suika (`triple-town`, `suika-game`, трійка → рівень вище); Jenga — за хитанням.

## Цікавинки для курсу
- 1D-стос: виймання будь-якого елемента + осідання + пошук відрізків 3+ однакових — 🌱 (список і один прохід).
- Ланцюг рівнів металу (3 бронзи → срібло → …) як рекурсивне злиття після кожного збігу — 📎.
- Монстри-приймачі зі смаком і лічильником гніву, обмін монстра після збігу — 📎.
- Нахил вежі як число, що росте від атак і бомб і скидається силою монстра; поразка за межею — 🥉 (баланс параметрів).
- Сили монстрів як тимчасові стани (сповільнення часу, ×10, вирівнювання) — 📎.

## Мапа на каталог
- Є: `swipe-gestures` ↔ свайп поверху; `line-match-clear` ↔ 3+ однакових поспіль у вежі; `gravity-fall` ↔ осідання верхніх поверхів; `chain-reaction` ↔ збіг після осідання; `event-points`, `score-records`; `time-out` ↔ Time Attack; `temporary-modes` ↔ сили монстрів на час; `tutorial-window`, `achievements-window`, `mode-select`.
- **Нема** → пропозиції карток:
  - `+feed-color-sink` «Приймач приймає лише свій колір» · entities/interact · 🌱 · слот {sinks: 2, wrong_limit}.
  - `+monster-swap-on-match` «Збіг міняє приймача на інший колір» · game-logic/score · 🌱.
  - `+star-up-merge` (вже пропонована) ↔ бронза → срібло → золото → діамант.
  - `+tower-tilt-balance` «Нахил стосу як лічильник поразки» · game-logic/lose · 🥉 · слот {max_tilt}.
  - `+anger-meter` ↔ гнів монстра за чужий колір.
  - `+garbage-adjacent-clear` ↔ бетонний поверх зникає від сусіднього збігу.
  - `+countdown-tile` ↔ поверх-бомба (?).
  - `+sink-power-on-special` «Особливий обʼєкт приймачу → його сила» · entities/state · 📎.

## Пропозиції до словників
- `+cond:tilt` — нахил стосу/вежі порівняно з межею (MAMC, Tricky Towers-подібні).
- `+effect:tilt` — змінити нахил стосу (атака монстра, бомба, вирівнювання).
- `+card:feed-color-sink`, `+card:monster-swap-on-match`, `+card:tower-tilt-balance`, `+card:sink-power-on-special`.

## Джерела
- ⭐ [Wikipedia: Monsters Ate My Condo](https://en.wikipedia.org/wiki/Monsters_Ate_My_Condo) — чотири монстри, свайп поверху, 3+ дає очки й міняє монстра, Endless і Timed Attack, дві умови поразки, PikPok / Adult Swim, 2011.
- [Pocket Gamer: рецензія](https://www.pocketgamer.com/monsters-ate-my-condo/review/) — бронза → срібло → золото → діамант, сили чотирьох монстрів, бетон і бомби, гнів хитає стос, Time Attack ~2 хв.
- [Kotaku](https://kotaku.com/monsters-ate-my-condo-is-colorful-candy-coated-kaiju-ma-5840972) — збіг лишає металевий поверх, монстр «tap out» і міняє колір, сили Reginald і Lord Ferocious, «вежа впала — кінець».
- [Common Sense Media](https://www.commonsensemedia.org/app-reviews/monsters-ate-my-condo) — поверхи падають у стос, виймаєш чужі кольори, щоб зійшлись 3+; туторіал, досягнення.
- [SlashGear: рецензія](https://www.slashgear.com/monsters-ate-my-condo-review-13213294/) — керування лише свайпом вліво/вправо.
- YouTube: пошук «Monsters Ate My Condo gameplay».

## Непевне
- (?) Звідки і як часто падають нові поверхи, чи можна вийняти будь-який поверх, чи лише нижній — джерела кажуть «свайпаєш поверх», не уточнюючи.
- (?) Скільки чужих поверхів до атаки монстра, чи видно гнів окремим індикатором, як саме виражається нахил вежі.
- (?) Хто з двох монстрів міняється після збігу — той, чий колір у групі, чи випадковий.
- (?) Сила Mr. Shigoto («два блоки за кожне комбо») — формулювання Pocket Gamer незрозуміле.
- (?) Чи бомба має видимий таймер (тому `+countdown-tile` під питанням).
- (?) Наявність онлайн-рекордів.
