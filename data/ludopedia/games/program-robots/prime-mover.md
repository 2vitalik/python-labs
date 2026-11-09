---
title: Prime Mover
slug: prime-mover
aka: []
family: program-robots
also: [connect-rotate]
klass: cursor
axes:
  field: nested
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2018
platforms: [PC (Windows, macOS, Linux, Steam)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/693700/", best: true, note: "4Bit Games, 21.05.2018; плати з компонентів, плати в платах, лідерборди й гістограми, 16 досягнень"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=1401639168", note: "Big Ant's Prime Mover Guide: усі компоненти (Wire, Bridge, Relay, Duplicator, Sorter, Eraser, Junction, Stepper, Button, Lock, IC) і перші пазли"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=1776780774", note: "фінальний пазл Processor: потоки A/B/C → D, коди інструкцій 00–06, цикли"}
  - {kind: other, url: "https://gamingnexus.com/Article/5685/Prime-Mover", note: "огляд: плата 7×7, підплата 7×7 у одній клітині, такт, сортер +/−/0"}
  - {kind: other, url: "https://3rd-strike.com/?p=80253", note: "огляд: повільні й швидкі дроти, пачки пазлів, кнопки pause/start/stop, автозбереження"}
  - {kind: other, url: "https://gertlushgaming.co.uk/review-prime-mover-steam/", note: "огляд: керування трьома кнопками миші, fast forward, літери входів/виходів на краях"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Prime+Mover+4bit+games+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cell-click, sequential-levels, level-unlock, leaderboard, game-pause, save-multi-slot, save-autosave, tutorial-window, main-menu, settings-window, game-screen, end-screen, +solution-metrics, +metric-histograms, +io-test-streams, +fast-forward, +wire-drawing, +custom-component, +nested-board, +value-packets, +sign-router, +toggle-junction, +slow-wire-delay, +crossing-bridge, +lock-and-button, +self-built-cpu-runs-program]
proposes: ["+role:wire", "+role:pin", "+cond:sign(v, pos|neg|zero)", "+effect:route(v, out)", "+effect:toggle(a)", "+window:metric-histograms", "+feature:solution-metrics", "+feature:solution-slots", "+card:nested-board", "+card:value-packets", "+card:sign-router", "+card:toggle-junction", "+card:lock-and-button"]
author: opus
date: 2026-11-09
---

# Prime Mover — плата з плиток, якою течуть числа: сортуй за знаком, перемикай, рахуй і вкладай цілі плати в одну клітину як підпрограми

## Суть
Зачлайк від 4Bit Games: на квадратній платі гравець ставить компоненти й дроти, щоб числа з вхідних потоків (A, B, C на краях) дійшли до виходу в потрібному вигляді. Компоненти — не логічні вентилі, а «маршрутизатори» чисел: сортер за знаком, реле, дублікатор, лічильник ±1, замок, перемикач. Головна фішка — **Integrated Circuit**: ціла підплата стискається в одну клітину з чотирма контактами й вкладається в інші плати. Фінал кампанії — процесор, що виконує програму з потоку A.

## Поле і час
- Плата — квадратна сітка (7×7 за Gaming Nexus); входи й виходи — літери на краях плати.
- IC — підплата того ж розміру (?) в одній клітині з контактами зверху, знизу, ліворуч, праворуч; вкладення багаторівневе (`field: nested`).
- Час — такти: усі значення рухаються синхронно; повільний (фіолетовий) дріт затримує дані на 1 такт.
- Дані — цілі числа (позитивні, негативні, нуль) у потоках; потоки на фінальному рівні читаються синхронно, «індексовані разом».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Значення (число) | object | ціле зі знаком | рухається дротами від входу до виходу |
| Вхід A/B/C | spawner | потік чисел | видає наступне число потоку |
| Вихід (D …) | zone | очікуваний потік | приймає числа й порівнює з очікуваними |
| Wire | terrain | швидкий / повільний | веде дані; повільний — +1 такт затримки |
| Bridge | terrain | — | перетин двох дротів без зʼєднання; поки на ньому дані — блокує обидва |
| Relay | object | напрям стрілки; ≤ 4 зʼєднання | усе, що входить, виходить у бік стрілки; кнопка повертає за годинниковою |
| Duplicator | object | ≤ 3 зʼєднання | копіює вхід на всі зʼєднання, звідки не прийшло даних |
| Sorter | object | ≤ 3 зʼєднання | число → вихід Positive / Negative / Zero; кнопка міняє + і − |
| Eraser | object | ≤ 4 входи | знищує все, що увійшло |
| Junction | switch | стан | перемикає вихід щоразу, як крізь нього пройшли дані або натиснуто кнопку |
| Stepper | object | напрям | +1 або −1 залежно від напрямку проходу; кнопка розвертає |
| Button | switch | 2 зʼєднання | дані, що прийшли, «натискають» прикріплений компонент |
| Lock | gate | відімкнено / замкнено | пропускає одне значення й замикається; відмикає кнопка |
| Integrated Circuit | container | 4 контакти; вкладена плата | підплата гравця як компонент; кнопка всередині може діяти назовні |
| Фрагмент памʼяті | pickup | — | сюжетні колекційні фрагменти на «кресленні» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `custom: «кожне значення просувається дротом»`; ЯКЩО `custom: «дріт повільний»` → ТО `custom: «затримка на 1 такт»`.
- КОЛИ `enter(value, sorter)` → ЯКЩО `custom: «value > 0 / < 0 / = 0»` → ТО `custom: «вихід Positive / Negative / Zero»`.
- КОЛИ `enter(value, relay)` → ТО `move(value, arrow_dir)`.
- КОЛИ `enter(value, duplicator)` → ТО `clone(value)` — копії на всі зʼєднання без вхідних даних.
- КОЛИ `enter(value, eraser)` → ТО `disappear(value)`.
- КОЛИ `enter(value, junction)` → ТО `custom: «вихід у поточний бік»`, `set_state(junction, other_side)`.
- КОЛИ `enter(value, stepper)` → ЯКЩО `moving(value, forward)` → ТО `set_value(value, +1)`; ЯКЩО `moving(value, back)` → ТО `set_value(value, −1)`.
- КОЛИ `enter(value, lock)` → ЯКЩО `state(lock, open)` → ТО `custom: «пропустити»`, `set_state(lock, locked)`; ЯКЩО `state(lock, locked)` → ТО `block`.
- КОЛИ `enter(value, button)` → ТО `custom: «дія над прикріпленим: rotate(relay|stepper), перемкнути junction, відімкнути lock, обміняти виходи sorter»`.
- КОЛИ `enter(value, bridge)` → ЯКЩО `occupied(bridge, value)` → ТО `block`.
- КОЛИ `enter(value, ic_pin)` → ТО `custom: «значення переходить у вкладену плату через відповідний край»`.
- КОЛИ `enter(value, output)` → ЯКЩО `same(value, expected, value)` → ТО `custom: «наступне очікуване»`; інакше `custom: «помилка виходу»` (?).
- КОЛИ `all_constraints_met` → ТО `win`, `window(end-screen)` з метриками й гістограмами.
- Процесор (фінал): КОЛИ `exec(opcode)` → ТО `custom: «00 — кінець; 01 — записати B у комірку C; 02 — копія; 03/04 — додати/відняти; 05 — вивести в D C разів; 06 — відносний перехід, якщо памʼять[B] > 0»`.
- Перемога: вихідні потоки збіглися з очікуваними · Поразка: нема — правиш плату · Рахунок: швидкість і ефективність розвʼязку (порівняння з друзями й світом).

## Керування і ввід
- Три кнопки миші: ліва ставить компонент, права видаляє; підказки при наведенні.
- Кнопки pause / start / stop угорі по центру; fast forward; ціль рівня — у правому верхньому куті.
- Кнопка на компоненті (рушій кнопки) перемикає slow wire, повертає реле/степер, міняє виходи сортера.
- До 3 розвʼязків на пазл; вихід із пазла автоматично зберігає плату.

## Вікна, меню, HUD
- `main-menu`: Play, Options, Exit.
- `level-select`: пазли пачками; кількох розвʼязаних у пачці досить, щоб відкрити наступну.
- `game-screen`: плата, палітра компонентів (вкладки (?)), ціль, кнопки симуляції.
- `tutorial-window`: коротке відео перед пазлом нового компонента; підказки під час гри.
- `end-screen`: розбір продуктивності + `metric-histograms` (custom: гістограми світу) і `leaderboard` друзів.
- `dialogue-window`: сюжетні кат-сцени й спогади між пазлами.
- `settings-window`: зокрема читабельніший шрифт, вимкнення музики.

## Фічі поза полем
- Пазли (за гайдом): Connect, Bridge, Relay, Amplifier, Gater, Flipper, Transformer, Separator, Distributor, Differentiator, Alternator, Integrated Circuit, Reset, Clock, Transistor, Sign, Flow Control, Nil Cleaner, And Gate, Add, Modulo 2, Reverse, Copy If … Full memory, Processor.
- `leaderboard-online` + гістограми; 16 досягнень (Optimizer, Cut-rate — за ефективніший розвʼязок (?)).
- Колекційні фрагменти памʼяті на кресленні (`collectibles`), Steam Cloud, картки.

## Варіації й родичі
- Порівнюють з [opus-magnum](opus-magnum.md) («але зі схемами») і зачлайками [tis-100](tis-100.md), SHENZHEN I/O; близькі за «плата → компонент» — [turing-complete](turing-complete.md) (власні компоненти), [kohctpyktop](kohctpyktop.md), [virtual-circuit-board](virtual-circuit-board.md).
- Потоки чисел, що мандрують сіткою: [manufactoria](manufactoria.md) (стрічка кольорів), [befunge](befunge.md).
- **Осі варіацій:** що тече (біти / числа / стрічки) · елементи (вентилі / маршрутизатори) · абстракція (вкладені плати / власні компоненти / нема) · оцінка (розмір / такти / вартість).

## Цікавинки для курсу
- Симуляція пакетів-чисел на сітці з тактами й затримкою повільного дроту — 🥉.
- Сортер за знаком, junction-перемикач, лок з кнопкою як мінімальний набір керування потоком — 📎.
- Bridge, що блокує обидва дроти, поки зайнятий, — 🌱.
- IC: вкладена плата з 4 контактами, рекурсивна симуляція — 🥇.
- Тест-раннер потоків A/B/C → D і метрики розвʼязку з гістограмою — 🥉.
- Процесор з опкодами 00–06 на «маршрутизаторах», а не вентилях — 👑.

## Мапа на каталог
- Є: `cell-click` · `sequential-levels` · `level-unlock` (пачки) · `leaderboard` · `game-pause` · `save-multi-slot` (3 розвʼязки) · `save-autosave` · `tutorial-window` · `main-menu` · `settings-window` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+nested-board` «Підплата гравця в одній клітині з контактами на краях» · game-logic/program · 🥇.
  - `+value-packets` «Числа-пакети рухаються дротами потактово» · game-logic/program · 🥉.
  - `+sign-router` «Маршрутизація за знаком числа» · game-logic/program · 🌱.
  - `+toggle-junction` «Розвилка, що перемикається проходом» · entities/state · 🌱.
  - `+lock-and-button` «Замок, що замикається проходом і відмикається сигналом» · entities/interact · 📎.
  - `+slow-wire-delay`, `+crossing-bridge` — 🌱 кожна.
  - `+solution-metrics`, `+metric-histograms`, `+io-test-streams`, `+fast-forward`, `+wire-drawing`, `+custom-component`, `+self-built-cpu-runs-program` — підтвердження.

## Пропозиції до словників
- `+role:wire`, `+role:pin` — підтвердження (Turing Complete).
- `+cond:sign(v, pos|neg|zero)` — знак числа.
- `+effect:route(v, out)` — відправити значення в обраний вихід компонента.
- `+effect:toggle(a)` — перемкнути двостанову сутність (junction, slow wire).
- `+window:metric-histograms`, `+feature:solution-metrics` — підтвердження.
- `+feature:solution-slots` — кілька збережених розвʼязків на пазл.
- `+card:nested-board`, `+card:value-packets`, `+card:sign-router`, `+card:toggle-junction`, `+card:lock-and-button` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Prime Mover](https://store.steampowered.com/app/693700/) — 4Bit Games, 21.05.2018; плати, вкладені плати, лідерборди й гістограми; теги; 16 досягнень.
- [Big Ant's Prime Mover Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=1401639168) — опис кожного компонента й кнопок; коментар про кнопку в IC, що діє назовні.
- [Processor explainer](https://steamcommunity.com/sharedfiles/filedetails/?id=1776780774) — опкоди 00–06, потоки A/B/C → D, лічильник команд, цикли.
- [Gaming Nexus](https://gamingnexus.com/Article/5685/Prime-Mover) — плата 7×7, підплата в клітині, такт, сортер.
- [3rd-Strike](https://3rd-strike.com/?p=80253) — дроти slow/fast, пачки пазлів, керування, меню.
- [Gert Lush Gaming](https://gertlushgaming.co.uk/review-prime-mover-steam/) — миша, fast forward, «end of level performance breakdown».

## Непевне
- (?) Розмір плати: 7×7 (Gaming Nexus) чи 8×8 (французький огляд у пошуку); чи підплата IC того самого розміру.
- (?) Які саме метрики (кількість компонентів / такти / вартість) показує екран результату.
- (?) Що відбувається з неправильним значенням на виході: зупинка чи підрахунок помилок; чи вхідні потоки випадкові.
- (?) Чи значення, що «натиснуло» Button, зникає; повна семантика кнопки на кожному компоненті.
- (?) RST у фінальному рівні — сигнал скидання з потоку чи окремий механізм.
- (?) Скільки всього пазлів і пачок; чи є пісочниця.
