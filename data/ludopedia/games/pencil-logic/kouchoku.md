---
title: Kouchoku (Коучоку, «Перетин — лише під прямим кутом»)
slug: kouchoku
aka: [交差は直角に限る, Kōchoku, Перетин лише під прямим кутом]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: graph
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: null
platforms: [paper, web]
links:
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/kouchoku.js", best: true, note: "puzz.link: 5 правил EN, правила JA, історія (Nikoli vol.133), коди помилок, тести вводу й налаштувань enline/lattice"}
  - {kind: play, url: "https://puzz.link/rules.html?kouchoku", note: "puzz.link: сторінка правил і вхід у плеєр/редактор (рендериться JS)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Kouchoku+puzzle", note: "пошук"}
stage: v1
coverage: 60
mechanics: [path-drawing, single-loop-check, satisfy-constraints, markup-validity, completion-detection, conflict-highlight, keyboard-controls, settings-window, in-game-editor, import-open-formats, undo-redo, level-solver, +visit-all-nodes, +node-graph-field, +right-angle-crossing, +letter-run-clue, +any-angle-segment]
proposes: ["+cond:crosses", "+cond:right_angle", "+cond:visited", "+cond:consecutive", "+card:right-angle-crossing", "+card:letter-run-clue", "+card:any-angle-segment", "+card:visit-all-nodes", "+card:node-graph-field"]
author: opus
date: 2026-11-09
---

# Kouchoku — замкни одну петлю через усі вузли прямими відрізками під будь-яким кутом; перетинатись можна лише під 90°

## Суть
На точках квадратної решітки стоять вузли: прості точки й кружки з буквами. Гравець зʼєднує вузли прямими відрізками будь-якого нахилу так, щоб вийшла одна петля, що проходить кожен вузол рівно раз. Петля може перетинати сама себе, але лише під прямим кутом і не у вузлі. Кружки з однаковою буквою мають іти в петлі поспіль, а між різними буквами потрібен хоча б один простий вузол. Незвичне для сімʼї: лінії не привʼязані до клітинок і ортогоналей — це геометрія відрізків на решітці.

## Поле і час
- Точки решітки (puzz.link: вузли на перетинах; тестове поле — 4×3 клітинки, тобто 5×4 точки); вузол може стояти не на кожній точці.
- Вузол: простий (`-` у редакторі) або кружок з буквою a…z.
- Ребро — відрізок між двома вузлами під довільним кутом; суміжність задає не сітка, а «видимість» вузлів (`field: graph`).
- Час статичний; хід = провести або стерти відрізок.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Простий вузол | static | координати точки решітки | петля проходить рівно раз (2 відрізки) |
| Кружок з буквою | static | буква | як вузол + однакові букви поспіль, різні — через простий вузол |
| Точка решітки без вузла | terrain | — | відрізок може пройти крізь, кінцем бути не може |
| Відрізок | mark | два кінці-вузли, будь-який нахил | не проходить через інший вузол; перетин з іншим — лише під 90° і не у вузлі |
| Петля | mark | — | одна, без розгалужень і тупиків |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, node → node)` → ЯКЩО `custom: «на відрізку нема інших вузлів»` → ТО `mark(segment, line)`.
- КОЛИ `input(drag, node → node)` → ЯКЩО `custom: «такий відрізок уже є»` → ТО `unmark(segment)` (повтор стирає; тест puzz.link).
- КОЛИ `custom: «відрізок проходить через вузол»` → ТО `constraint_broken(pass_over)` (`lnPassOver`; з налаштуванням `lattice` — `block` при вводі).
- КОЛИ `custom: «кінець відрізка не на вузлі»` → ТО `constraint_broken(isolate)` (`lnIsolate`; з `enline` — `block` при вводі).
- КОЛИ `custom: «два відрізки перетинаються»` (`+cond:crosses`) → ЯКЩО `custom: «кут ≠ 90°»` (`+cond:right_angle`) → ТО `constraint_broken(right_angle)` (`lnRightAngle`).
- КОЛИ `custom: «у вузла 3+ відрізки»` → ТО `constraint_broken(branch)` (`lnBranch`).
- КОЛИ `custom: «у вузла 1 відрізок»` → ТО `constraint_broken(dead_end)` (`lnDeadEnd`).
- КОЛИ `custom: «у вузла < 2 відрізків»` (`+cond:visited`) → ТО `constraint_broken(unvisited)` (`nmLineLt2`).
- КОЛИ `pattern(loop_closed)` → ЯКЩО `not single_loop` → ТО `constraint_broken(multi_loop)` (`lnPlLoop`).
- КОЛИ `custom: «відрізок зʼєднує два кружки»` → ЯКЩО `not same(a, b, letter)` → ТО `constraint_broken(diff_letters)` (`nmConnDiff`).
- КОЛИ `custom: «кружки з буквою X не йдуть у петлі поспіль»` (`+cond:consecutive`) → ТО `constraint_broken(not_consecutive)` (`nmNotConseq`).
- КОЛИ `custom: «на полі нема жодного відрізка»` → ТО `constraint_broken(no_line)` (`brNoLine`).
- КОЛИ `all_constraints_met` → ЯКЩО `single_loop` and `cover_all(node)` → ТО `win`.
- Перемога: одна петля через усі вузли, перетини лише прямі й поза вузлами, буквені умови виконані. · Поразки й рахунку нема.

## Керування і ввід
- puzz.link play: drag лівою від вузла до вузла — відрізок; повторний drag тим самим відрізком — стерти.
- Налаштування puzz.link: `enline` — відрізки лише між вузлами (інакше дозволено між будь-якими точками решітки); `lattice` — не дає провести відрізок через інший вузол.
- puzz.link edit: курсор по точках; клавіші `a`…`z` — буква, `-` — простий вузол, пробіл — прибрати; клік мишею циклічно перебирає значення, права кнопка — назад.

## Вікна, меню, HUD
- `game-screen` (puzz.link): решітка точок, вузли, відрізки; `check-button`, `undo-button`, `redo-button`; `conflict-highlight` для перетину не під 90° чи розгалуження (?).
- `settings-window` (puzz.link): `enline`, `lattice`.
- `editor-window` (puzz.link edit mode): розмір, вузли й букви; експорт у URL.
- `help-window`: 5 правил (puzz.link).
- Переходи: puzz.link rules → URL пазла → game-screen → Check → «розвʼязано» (?).

## Фічі поза полем
- `auto-check` за кнопкою: перший знайдений код помилки (puzz.link).
- `undo` / `redo` (puzz.link) (?).
- Налаштування-помічники вводу (`enline`, `lattice`) — відсікають заздалегідь нелегальні відрізки.
- `level-editor` + `share-code` — пазл як URL puzz.link.

## Варіації й родичі
- Петлі сімʼї: [masyu](masyu.md), [slitherlink](slitherlink.md), [country-road](country-road.md) — петля по ортогоналях без перетинів; тут — довільні кути й дозволені прямі перетини.
- [Hashiwokakero](hashiwokakero.md) — теж відрізки між вузлами, але ортогональні, без перетинів і без петлі.
- Untangle з [Tatham](tatham-collection.md) — геометрія перетину відрізків, але точки рухаються, а не зʼєднуються.
- [Goishi Hiroi](goishi-hiroi.md) — гамільтонів шлях по каменях; тут — гамільтонів цикл по вузлах.
- **Осі варіацій**: кути (лише ортогональ / 8 напрямків / будь-які) · перетини (заборонені / лише 90° / будь-які) · підказки (букви-групи / числа / без підказок) · кінці відрізків (лише вузли / будь-яка точка).

## Цікавинки для курсу
- Чи лежить точка решітки на відрізку: цілочисельно через `gcd(dx, dy)` — 📎.
- Перетин двох відрізків + перевірка прямого кута через скалярний добуток = 0 — 📎 (класична обчислювальна геометрія).
- Одна петля через усі вузли (ступінь 2 + звʼязність) — 🥉 (картка `single-loop-check`).
- Буквені групи: однакові поспіль, різні не впритул — обхід циклу з порівнянням сусідів — 📎.
- Ввід drag-ом «від вузла до вузла» з прилипанням і перемикачами `enline`/`lattice` — 📎.
- Розвʼязувач: кандидати-ребра = усі пари видимих вузлів, обмеження перетину робить пошук важким — 🥇.

## Мапа на каталог
- Є: `path-drawing` ↔ drag відрізка · `single-loop-check` ↔ одна петля · `satisfy-constraints`, `markup-validity`, `conflict-highlight`, `completion-detection` · `keyboard-controls` ↔ редактор · `settings-window` ↔ enline/lattice · `in-game-editor`, `import-open-formats` ↔ URL · `undo-redo` · `level-solver`.
- **Нема** → пропозиції карток:
  - `+right-angle-crossing` «Лінії можуть перетинатись лише під 90° і не у вузлі» · game-logic/constraints · 📎.
  - `+letter-run-clue` «Однакові мітки — поспіль на шляху, різні — не впритул» · game-logic/constraints · 📎.
  - `+any-angle-segment` «Ребро — відрізок між точками під будь-яким кутом» · interface/input · 📎.
  - `+visit-all-nodes` (повтор із LYNE), `+node-graph-field` (повтор із Hitman GO).

## Пропозиції до словників
- `+cond:crosses` — дві лінії перетинаються (повтор із корпусу).
- `+cond:right_angle` — кут між відрізками 90°.
- `+cond:visited` — вузол уже пройдено / пройдено N разів (повтор).
- `+cond:consecutive` — елементи з однаковою міткою йдуть у шляху поспіль.
- `+card:right-angle-crossing`, `+card:letter-run-clue`, `+card:any-angle-segment`, `+card:visit-all-nodes`, `+card:node-graph-field` — див. мапу.

## Джерела
- ⭐ [puzz.link kouchoku.js](https://puzz.link/js/pzpr-samples/kouchoku.js) — 5 правил EN і 4 JA, «вперше в Puzzle Communication Nikoli vol.133», коди `brNoLine lnIsolate lnBranch lnPassOver nmConnDiff lnRightAngle lnPlLoop lnDeadEnd nmLineLt2 nmNotConseq`, тести drag-вводу й налаштувань `enline`/`lattice`.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти кодів («A segment passes over a clue», «Segments don't intersect at a right angle», «Equal letters are not connected directly»…).
- [puzz.link rules](https://puzz.link/rules.html?kouchoku) — сторінка правил (текст рендериться JS).
- YouTube: пошук «Kouchoku puzzle».

## Непевне
- (?) Рік: Nikoli vol.133 — дати випуску не бачив (оцінка за квартальним виходом ≈ 2010–2011); автор жанру невідомий.
- (?) Сторінки жанру на Nikoli EN і Janko немає (404); правила лише з puzz.link.
- (?) Точний зміст `lattice` — виведений з тестів (відрізок через вузол відхиляється, через порожню точку — ні).
- (?) Чи мусить точка перетину двох відрізків бути точкою решітки — правила кажуть лише «не у вузлі».
- (?) Undo/redo, «розвʼязано» й підсвітка помилок — загальна поведінка pzpr.
