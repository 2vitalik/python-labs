---
title: Electric Box (+ Lazors)
slug: electric-box
family: connect-rotate
also: [build-sim, thinky]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2009
platforms: [web (Flash), iOS, Android]
links:
  - {kind: other, url: "https://www.kongregate.com/en/games/TwinkleStarGames/electric-box", best: true, note: "Electric Box на Kongregate: опис, керування, 15 рівнів + пак на 30, бейджі, 19.02.2009"}
  - {kind: other, url: "https://www.kongregate.com/en/games/TwinkleStarGames/electric-box-2", note: "Electric Box 2 (1.10.2010): перевертання предметів, пробіл — показати рухомі, редактор і рівні гравців"}
  - {kind: other, url: "http://www.appspy.com/review/3388/electric-box/", note: "огляд iOS-версії: 65 рівнів, перетягування на сітку, тап — опис/напрям, парові машини, магніти, лазери"}
  - {kind: other, url: "https://toucharcade.com/2009/08/11/electric-box-an-energy-transmission-puzzler/", note: "огляд iOS 2009 (з черги; 403)"}
  - {kind: other, url: "https://apps.apple.com/us/app/lazors/id386458926", note: "Lazors (Pyrosphere, 2010): дзеркала й блоки, Crystal/Portal/Spin, щоденні пазли, підказки"}
  - {kind: other, url: "https://mwm.ai/apps/lazors/386458926", note: "Lazors: 280+ рівнів серіями (Spin, Diagonal, Darkroom), щоденний пазл"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Electric+Box+flash+game+walkthrough", note: "пошук; проходження"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lazors+game+gameplay", note: "пошук; Lazors"}
stage: v1
coverage: 55
mechanics: [drag-drop-piece, cell-click, game-screen, end-screen, level-select, level-unlock, sequential-levels, in-game-editor, level-exchange, completion-detection, score-records, help-window, +run-simulation, +energy-conversion-chain, +limited-parts-inventory, +fixed-vs-movable, +tile-rotate, +beam-tracing, +mirror-reflect, +beam-splitter, +all-targets-hit, +lit-from-source, +hint-reveal, +daily-puzzle-calendar]
proposes: ["+role:source", "+role:sink", "+role:conduit", "+role:supply", "+trigger:input(drag)", "+trigger:exec(tick)", "+trigger:beam_hit", "+trigger:program_end", "+cond:energy_type(in, kind)", "+effect:place", "+effect:convert(energy_in → energy_out)", "+effect:emit_beam", "+effect:reflect", "+effect:split_beam", "+effect:absorb", "+ui:parts-tray", "+ui:power-button", "+ui:movable-highlight", "+card:energy-conversion-chain", "+card:limited-parts-inventory", "+card:all-targets-hit"]
author: opus
date: 2026-11-02
---

# Electric Box (+ Lazors) — розстав пристрої на сітці, щоб енергія дійшла від джерела до цілі через перетворення

## Суть
Electric Box (TwinkleStarGames, 2009, Flash) — головоломка в дусі The Incredible Machine на сітці: є джерело живлення, ціль і обмежений набір пристроїв. Гравець перетягує пристрої на поле, натискає «живлення» — і енергія біжить ланцюгом, **змінюючи форму**: струм → світло лампи → сонячна панель → струм, струм → вентилятор → вітер → вітряк, і т. д. Пазл — підібрати порядок і орієнтацію перетворювачів, щоб ланцюг замкнувся на цілі. Lazors (Pyrosphere, 2010) — споріднена «чиста» версія: лише один вид енергії (лазер), блоки-дзеркала/скло/стопи переставляються, щоб промінь пройшов через усі цілі.

## Поле і час
- Electric Box: квадратна сітка клітин (точний розмір — ?), частина пристроїв закріплена на рівні, решта — в інвентарі під полем.
- Дві фази: **розстановка** (статична) → **запуск** (анімований ланцюг подій; коментарі гравців скаржаться, що він повільний). Помилка → назад до розстановки.
- Lazors: сітка слотів під блоки; лазери стартують з фіксованих точок під 45° і рухаються **по діагоналі**, відбиваючись від граней блоків; цілі — точки на гранях/кутах (?). Час статичний: промінь перераховується миттєво після кожного переставлення (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Джерело / кнопка живлення | source (custom) | — | після запуску подає струм у сусідній провідник |
| Ціль (target) | sink (custom) | — | отримала енергію → рівень пройдено |
| Дріт | conduit (custom) | форма: пряма/кут/розгалуження (?) | передає струм по суміжних клітинах |
| Лампочка → сонячна панель | conduit (custom) | напрям світла (?) | струм → світло; панель під світлом → струм |
| Вентилятор → вітряк | conduit (custom) | напрям; перевертається кліком | струм → потік повітря по лінії; вітряк у потоці → струм |
| Конвеєр | conduit (custom) | напрям | везе предмет до наступного пристрою (?) |
| Парова машина | conduit (custom) | — | нагрів/вода → обертання → струм (?) |
| Магніт | conduit (custom) | — | притягує/рухає металевий предмет, що замикає контакт (?) |
| Лазер → приймач | conduit (custom) | напрям променя | струм → промінь по прямій; приймач → струм |
| Електромагнітна перешкода / стіна | static | — | займає клітину |
| EB2: дриль, гармата, гелі-бот, перемикач, бездротовий передавач/приймач | conduit (custom) | — | нові види перетворень; передавач шле струм без дроту на приймач (?) |
| Інвентар рівня | supply (custom) | список предметів з кількістю | гравець витрачає все або частину (?) |
| Lazors: лазер | source (custom) | точка і діагональний напрям | промінь по діагоналі до виходу з поля |
| Lazors: дзеркальний блок | object | рухомий / закріплений | відбиває промінь від грані |
| Lazors: непрозорий блок | object | рухомий / закріплений | поглинає промінь |
| Lazors: скляний блок | object | рухомий / закріплений | промінь і проходить, і відбивається — ділиться на два |
| Lazors: ціль | sink (custom) | точка | має лежати на шляху хоча б одного променя |
| Lazors: Crystal, Portal, Mirror+, Stop+, Spin, Trap target | object | пізні оновлення | кристал/портал переносять промінь, Spin обертається, Trap — ціль, якої **не можна** торкатися (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, item, cell)` → ЯКЩО `free(cell)` and `has(inventory, item)` → ТО `place(item, cell)`; перетягнути з поля назад → `give(inventory, item)`.
- КОЛИ `input(click, item)` → ЯКЩО `custom: «предмет має напрям»` → ТО `face(item, flip)` (EB2: «flip items that can be reversed»); тап на iOS — показати опис.
- КОЛИ `input(power)` → ТО `custom: «фаза запуску»`, джерело `emit(current)`.
- КОЛИ `exec(tick)` → ЯКЩО `energy_type(in, current)` and `custom: «пристрій приймає цей вид енергії з цього боку»` → ТО `convert(current → out_kind)` і передати вихід у напрямку пристрою.
- КОЛИ `exec(tick)` → ЯКЩО вихід не потрапив на жоден приймач → ТО `custom: «ланцюг обірвався»`, `program_end` без перемоги.
- КОЛИ `contact(energy, target)` → ТО `win`, `window(end-screen)`, `unlock(next)`.
- Lazors: КОЛИ `after(place|move)` → ТО `emit_beam` з кожного лазера; на грані блока: дзеркало → `reflect`; непрозорий → `absorb`; скло → `split_beam` (продовжується прямо + відбитий).
- Lazors: КОЛИ `beam_hit(target)` для всіх цілей одночасно → ТО `win` (`all_constraints_met`).
- Lazors: КОЛИ `input(drag, block)` → ЯКЩО `state(block, fixed)` → ТО `block`.
- Lazors: КОЛИ `input(hint)` → ЯКЩО `has(player, hints)` → ТО `custom: «показати позицію одного блока»` (?), `take(hint)`.
- Перемога: енергія/промінь на цілі (Lazors — на всіх) · Поразка: нема, лише «ще раз» · Рахунок: локальні рекорди в iOS-версії Electric Box (?).

## Керування і ввід
- Electric Box: лише миша — перетягнути предмет з лотка на сітку чи з сітки назад; клік — перевернути напрямлений предмет (EB2); утримувати пробіл — підсвітити рухомі предмети (EB2).
- iOS: тап і drag; тап по предмету — опис і зміна напряму.
- Lazors: перетягування блоків між слотами; кнопка підказки; щоденний пазл з календаря.

## Вікна, меню, HUD
- `main-menu`: Play → `level-select` (сітка рівнів з відкритими/закритими), Level Pack (30 додаткових, EB1), EB2: Editor → `editor-window`, User Levels → браузер рівнів гравців.
- `game-screen`: сітка, `parts-tray` (інвентар рівня під/збоку від поля), `power-button`, кнопка рестарту, `movable-highlight` (пробіл, EB2).
- `end-screen`: «рівень пройдено» → наступний; бейджі Kongregate (Short Circuit, Uninterruptible Power Solver; EB2 — Power from the Players, Flip Flop).
- Lazors: `level-select` серіями (Spin, Diagonal, Darkroom…), `daily-window` з датою, `shop-window` (20 підказок, Lazors Deluxe), лічильник «Hints left», Game Center досягнення.
- Переходи: main-menu → level-select → game-screen ⇄ (запуск) → end-screen → наступний.

## Фічі поза полем
- `levels-sequential` + `level-unlock`; EB1 на Kongregate — 15 рівнів + пак із 30; iOS — 65 рівнів з обіцяними оновленнями.
- EB2: `level-editor`, `level-sharing`, `user-levels-browser` (рівні гравців).
- `achievements` (бейджі Kongregate / Game Center у Lazors), `leaderboard-local` (iOS Electric Box).
- Lazors: `daily-puzzle` (з v3.1, щорічні набори), `hint` з покупним запасом, пак Deluxe (70 рівнів).

## Варіації й родичі
- The Incredible Machine / Contraption Maker (вільна фізика замість сітки), Crazy Machines; Electric Box — їх «клітинна» версія.
- Лазерні родичі: Deflektor, Laser Tank, Khet, Lazors, Laser Maze (ThinkFun) — промінь як «енергія одного виду».
- Осі варіацій: **види енергії: один (лазер) / багато з перетвореннями** · **розвʼязок: ланцюг до однієї цілі / покрити всі цілі** · **виконання: миттєвий перерахунок / анімований запуск** · **предмети: усі використати / підмножина** · **промінь: ортогональний / діагональний**.

## Цікавинки для курсу
- Ланцюг перетворювачів енергії як граф типів: таблиця «пристрій: вхід → вихід, напрям» + симуляція поширення — 🥉.
- Інвентар обмежених деталей з поверненням з поля і закріплені/рухомі предмети — 📎.
- Lazors: трасування діагонального променя з відбиттям від граней блоків на півкроковій сітці — 🥉; скло, що розщеплює промінь (черга променів, захист від циклу) — 📎.
- Lazors-розвʼязувач: перебір розстановок блоків по слотах з відсіканням + перевірка всіх цілей — 🥇 (класичне студентське завдання, формат `.bff`, ?).
- Редактор рівнів + обмін рівнями гравців (EB2) — 🥈.
- Щоденний пазл з календарем — 📎.

## Мапа на каталог
- Є: `drag-drop-piece` · `cell-click` · `game-screen` · `end-screen` · `level-select` · `level-unlock` · `sequential-levels` · `in-game-editor` · `level-exchange` (EB2) · `completion-detection` · `score-records` · `help-window`.
- **Нема** → пропозиції карток:
  - `+run-simulation` «План → запуск симуляції» · game-logic · 🥉 — з Cosmic Express/Railbound.
  - `+energy-conversion-chain` «Ланцюг перетворювачів енергії» · entities/interact · 🥉 · слоти {kinds: [current, light, wind, laser, steam], table: text}.
  - `+limited-parts-inventory` «Набір деталей рівня з поверненням» · entities/state · 📎 · слот {must_use_all: bool}.
  - `+fixed-vs-movable` «Закріплені й рухомі предмети» · entities/legality · 🌱.
  - `+tile-rotate` «Обертання/перевертання предмета» · entities/state · 🌱.
  - `+beam-tracing` «Трасування променя» · entities/combat · 🥉 · слот {directions: diagonal}.
  - `+mirror-reflect` «Дзеркало» · entities/interact · 📎.
  - `+beam-splitter` «Розщеплення променя» · entities/interact · 📎 — з Khet.
  - `+all-targets-hit` «Усі цілі одночасно на промені» · game-logic/win · 🌱.
  - `+lit-from-source` «Підсвітка живлених від джерела» · interface/hud · 📎.
  - `+hint-reveal` «Підказка відкриває частину розвʼязку» · game-logic/difficulty · 📎.
  - `+daily-puzzle-calendar` «Календар щоденних пазлів» · levels/bank · 📎 (розширення `daily-puzzle`).

## Пропозиції до словників
- `+role:source` / `+role:sink` / `+role:conduit` — джерело, ціль, перетворювач/дзеркало (підтвердження); `+role:supply` — лоток деталей.
- `+trigger:exec(tick)` ⏳, `+trigger:program_end` ⏳, `+trigger:beam_hit` (з Khet/Deflektor).
- `+cond:energy_type(in, kind)` — пристрій отримав енергію певного виду з певного боку.
- `+effect:place` ⏳; `+effect:convert(energy_in → energy_out)` — пристрій змінює вид енергії; `+effect:emit_beam` / `+effect:reflect` / `+effect:split_beam` (з Khet); `+effect:absorb` — промінь поглинуто.
- `+ui:parts-tray` — лоток деталей рівня; `+ui:power-button` — запуск (як `run-button`); `+ui:movable-highlight` — показати рухомі предмети.

## Джерела
- ⭐ [Electric Box на Kongregate](https://www.kongregate.com/en/games/TwinkleStarGames/electric-box) — опис, керування мишею, 15 рівнів + пак на 30, бейджі, дата 19.02.2009, вентилятори/лампи/конвеєри у FAQ.
- [Electric Box 2 на Kongregate](https://www.kongregate.com/en/games/TwinkleStarGames/electric-box-2) — 1.10.2010, перевертання кліком, пробіл, вентилятори/перемикачі/лазери, редактор і рівні гравців.
- [AppSpy review](http://www.appspy.com/review/3388/electric-box/) — iOS: 65 рівнів, тап — опис і напрям, парові машини, магніти, лазери, локальні рекорди.
- [Lazors — App Store](https://apps.apple.com/us/app/lazors/id386458926) — Pyrosphere, v1.0 17.08.2010, Crystal/Portal/Mirror+/Stop+/Spin/Trap, щоденні пазли, підказки, Deluxe.
- [Lazors — mwm.ai](https://mwm.ai/apps/lazors/386458926) — 280+ рівнів серіями, щоденний пазл.
- YouTube: пошуки «Electric Box flash game walkthrough», «Lazors game gameplay».

## Непевне
- (?) Повний список пристроїв Electric Box (сонячна панель, вітряк, парова машина, магніт — частина з оглядів, частина з памʼяті) і точна таблиця перетворень — не звірено; Kongregate FAQ називає лише вентилятори, лампи, конвеєри, коментарі — лазери й дроти.
- (?) Розмір сітки, чи треба використати всі деталі, рахунок/очки — невідомо.
- (?) Lazors: базові блоки «відбивний / непрозорий / скляний», діагональний промінь і цілі на гранях — з памʼяті (та з популярного студентського завдання «Lazor»), офіційні сторінки їх не перелічують.
- (?) Розробник EB: TwinkleStarGames за URL Kongregate, EB2 — разом із Candystand; рік iOS-версії ~2009 (огляд TouchArcade, 403).
- (?) WebSearch вичерпаний — частину фактів не вдалося перевірити.
