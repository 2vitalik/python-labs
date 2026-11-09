---
title: Crossing Chains
slug: crossing-chains
aka: []
family: connect-rotate
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2025
platforms: [PC, Mac, Linux, web]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3565250/Crossing_Chains/", best: true, note: "правило перетину, 75 рівнів, daily і random, необмежені підказки"}
  - {kind: itch, url: "https://danijmn.itch.io/crossingchains", note: "браузерне демо (18 рівнів), опції вводу, спадкоємець Cardinal Chains"}
  - {kind: other, url: "https://danijmn.itch.io/cardinalchains/devlog/1132946/introducing-crossing-chains", note: "анонс: заповнити всю сітку ланцюгами від коренів; перетин лише за рівних довжин"}
  - {kind: other, url: "https://danijmn.itch.io/cardinalchains", note: "попередник Cardinal Chains: ланцюги неспадних чисел від клітин-X"}
  - {kind: other, url: "https://www.bontegames.com/2025/12/crossing-chains-browser-download-paid.html", note: "коротко правило; коментар: ланцюг можна лише продовжувати від старту"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=1mZqSPsy-sY", note: "трейлер (вбудований на сторінці itch)"}
stage: v1
coverage: 40
mechanics: [path-drawing, path-cut, satisfy-constraints, completion-detection, daily-puzzle, level-select, puzzle-select, sequential-levels, tutorial-window, theme-select, controls-remap, keyboard-controls, swipe-gestures, save-progress, game-screen, main-menu, settings-window, +fill-all-cells, +equal-length-crossing, +hidden-crossings, +hint-reveal, +curated-random-puzzles, +one-button-mode]
proposes: ["+cond:length_equal", "+effect:extend_chain", "+ui:crossings-counter", "+feature:one-button-mode", "+card:equal-length-crossing", "+card:hidden-crossings"]
author: opus
date: 2026-11-09
---

# Crossing Chains — заповни все поле ланцюгами від коренів; ланцюги можуть перетнутись лише там, де їхні довжини рівні

## Суть
Лінійний пазл від Daniel Nora, «духовний спадкоємець» його Cardinal Chains. Рівень — «сузірʼя» кіл; з одного чи кількох коренів треба протягнути ланцюги так, щоб покрити все поле. Головне правило: ланцюги **можуть перетинатися, але лише там, де їхні довжини в точці перетину однакові**, а самі точки перетину наперед не показані — їх треба вивести. Далі в грі зʼявляються кола, що «по-різному перетворюють ланцюги».

## Поле і час
- Кола стоять на квадратній решітці; ланки ланцюга — горизонтальні й вертикальні відрізки між сусідніми колами (у ресурсах демо є окремі матеріали для горизонтальних і вертикальних ланок) (?).
- Пазл без часу (`static`): хід — подовжити або вкоротити ланцюг. Кожен рівень має рівно один розвʼязок.
- Інформація повна: перетини «приховані» лише тим, що їх не позначено, а не випадковістю.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Корінь | source | колір ланцюга | звідси починається ланцюг; рівень має один або кілька коренів |
| Коло | mark | номер (?), зайнятість | ланцюг заходить у коло й продовжується до сусіднього; кожне коло має бути покрите |
| Ланцюг | conduit | довжина, голова | росте лише від голови; повернення назад стирає хвіст |
| Точка перетину | zone | наперед невідома | коло, через яке проходять два ланцюги однакової довжини в цій точці |
| Особливі кола | tile | вид (?) | «перетворюють ланцюги по-різному»; вводяться поступово (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, head → circle)` → ЯКЩО `custom: «коло сусіднє з головою ланцюга»` і `free(circle)` → ТО `mark(circle, chain)`, `counter(chain_length, +1)`.
- Ланцюг можна лише продовжувати від кореня/голови: окремі «відомі» шматки розвʼязку наперед не ставляться.
- КОЛИ `input(drag)` у коло, яке вже проходить інший ланцюг → ЯКЩО `custom: «довжини обох ланцюгів у цьому колі рівні»` → ТО `custom: «перетин — обидва ланцюги проходять крізь коло»`, `counter(crossings, +1)`; інакше `block` (?).
- КОЛИ `input(drag)` назад по своєму ланцюгу → ТО `unmark(tail)` (опція «Paths erase themselves»).
- КОЛИ `input(drag)` через чужий ланцюг без права на перетин → ЯКЩО `mode(paths_erase_each_other)` → ТО `custom: «чужий ланцюг обрізається»`; інакше `block` (?).
- КОЛИ `contact(chain, special_circle)` → ТО `custom: «коло перетворює ланцюг»` (?) — механіки повних рівнів не підтверджені.
- КОЛИ `input(hint)` → ТО `custom: «показати один правильний хід»` (підказок без ліміту).
- КОЛИ `all_constraints_met` — тобто `cover_all(circles)` і всі перетини легальні → ТО `win`, `next_level`.
- Перемога: усі кола покриті ланцюгами від коренів, кожен перетин — у точці рівних довжин. · Поразки нема. · Рахунку нема.

## Керування і ввід
- Протягування мишею або пальцем від голови ланцюга; клавіатура, геймпад і режим однієї кнопки — без миші.
- Опції вводу: авто-протягування для клавіатури й миші, «ланцюги стирають один одного», «ланцюг стирає сам себе».
- Кнопки рівня: назад, попередній/наступний рівень, рестарт, підказка, налаштування, повний екран.

## Вікна, меню, HUD
- `main-menu`: основний набір рівнів · щоденні рівні · набір «прототипів» · продовжити останню гру · налаштування · керування · титри · вихід (назви з ресурсів веб-демо).
- `puzzle-select` — сітка рівнів з позначкою «в процесі».
- `game-screen`: поле; `crossings-counter` («Crossings: N»); кнопки підказки, рестарту й переходу між рівнями; `hint-marker`.
- `settings-window`: тема кольорів, гучність музики й ефектів, опції стирання й авто-протягування, висока контрастність.
- `options-controls` — перепризначення клавіш і кнопок геймпада.
- `tutorial-window` — інтерактивне навчання; `credits-window`; `end-screen` демо з переліком фіч повної гри.

## Фічі поза полем
- 75 ручних рівнів (`levels-sequential`), `daily-puzzle`, тисячі відібраних «Random» пазлів (`mode-endless`).
- `hint` необмежений, по одному ходу; `restart-level`; `autosave` прогресу (файл `progress.dat`, Steam Cloud).
- `theme-select`, `high-contrast`, `remap-controls`, `one-button-mode`, `touch-controls`, `gamepad-support`, `localization` (6 мов).
- «Секрети» в грі (?) — які саме, невідомо.

## Варіації й родичі
- Cardinal Chains (той самий автор): числа в клітинах, ланцюги від клітин-X мають іти неспадною послідовністю й залити все поле; перетинів нема.
- Родичі: Flow Free (заповнити поле шляхами, без перетинів), LYNE (перетини дозволені лише в особливих вузлах), Numberlink.
- Осі варіацій: **перетин шляхів**: заборонено (Flow Free) / лише у позначених вузлах (LYNE) / де завгодно, якщо довжини рівні, а місце невідоме (Crossing Chains) · **обмеження ланцюга**: неспадні числа (Cardinal Chains) / рівність довжин у перетині.

## Цікавинки для курсу
- Протягування ланцюга від голови зі стиранням хвоста при поверненні — 📎 (картки `path-drawing`, `path-cut`).
- Перевірка перетину: довжина обох ланцюгів у спільному колі — 🌱.
- Перевірка покриття всього поля — 🌱.
- Розвʼязувач з невідомими точками перетину (перебір з відсіканням) — 🥇.
- Генерація «Random»-пазлів з єдиним розвʼязком — 👑 (картка `unique-puzzle-generation`).
- Підказка «один правильний хід» за збереженим розвʼязком — 📎.

## Мапа на каталог
- Є: `path-drawing` + `path-cut` ↔ протягування й стирання; `satisfy-constraints` + `completion-detection`; `daily-puzzle`; `level-select` + `puzzle-select` + `sequential-levels`; `tutorial-window`; `theme-select`; `controls-remap` + `keyboard-controls` + `swipe-gestures`; `save-progress`; `game-screen`, `main-menu`, `settings-window`.
- **Нема** → пропозиції карток:
  - `+fill-all-cells` «Покрити всі клітини шляхами» · game-logic/win · 🌱 (є в сімʼї).
  - `+equal-length-crossing` «Перетин лише за рівних довжин» · game-logic/constraints · 📎.
  - `+hidden-crossings` «Точки перетину не позначені» · game-logic/constraints · 🥉 (дедукція місця перетину).
  - `+hint-reveal` «Підказка відкриває один хід» · interface/hud · 🌱 (є в сімʼї).
  - `+curated-random-puzzles` «Банк відібраних згенерованих пазлів» · levels/bank · 🥉.
  - `+one-button-mode` «Керування однією кнопкою» · interface/input · 📎.

## Пропозиції до словників
- `+cond:length_equal` — довжини двох ланцюгів у точці рівні (тут — `custom`).
- `+effect:extend_chain` — подовжити ланцюг від голови (тут — `mark` + `counter`).
- `+ui:crossings-counter` — лічильник перетинів на екрані.
- `+feature:one-button-mode` — гра однією кнопкою (доступність).
- `+card:equal-length-crossing`, `+card:hidden-crossings`.

## Джерела
- ⭐ [Steam: Crossing Chains](https://store.steampowered.com/app/3565250/Crossing_Chains/) — «сузірʼя кіл», корені, перетин за рівних довжин, точки не показані, кола перетворюють ланцюги; 75 рівнів, daily, random, підказки.
- [itch.io](https://danijmn.itch.io/crossingchains) — демо, опції (контрастність, одна кнопка, налаштування керування), реліз 12.12.2025, спадкоємець Cardinal Chains.
- [Devlog «Introducing Crossing Chains»](https://danijmn.itch.io/cardinalchains/devlog/1132946/introducing-crossing-chains) — «заповнити всю сітку ланцюгами від кореневих клітин»; інші механіки вводяться поступово.
- [Cardinal Chains](https://danijmn.itch.io/cardinalchains) — правила попередника.
- [Bonte Games](https://www.bontegames.com/2025/12/crossing-chains-browser-download-paid.html) — правило одним реченням; коментар про продовження лише від старту.
- [Трейлер](https://www.youtube.com/watch?v=1mZqSPsy-sY).
- Ресурси веб-демо (назви сцен, ключі рядків, напис «Crossings: 0») — пункти меню й опції стирання.

## Непевне
- (?) Що означають числа на колах (черга каже «нумеровані кола»): імовірно, номер кроку ланцюга, з якого видно рівність довжин.
- (?) Які особливі кола є в повній грі й що вони роблять з ланцюгами.
- (?) Що відбувається при спробі нелегального перетину: блок чи обрізання чужого ланцюга залежно від опції.
- (?) Чи ланцюг у перетині йде лише прямо, чи може повертати.
- (?) Кількість рівнів демо: 16 (анонс), 17 (Bonte Games), 18 (devlog після оновлення).
