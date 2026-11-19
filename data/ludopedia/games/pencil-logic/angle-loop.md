---
title: Angle Loop (鋭直鈍ループ)
slug: angle-loop
aka: [鋭直鈍ループ, angleloop, Петля кутів]
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
platforms: [web]
links:
  - {kind: play, url: "https://puzz.link/rules.html?angleloop", best: true, note: "puzz.link: правила EN/JA з прикладом і вхід у плеєр/редактор (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/angleloop.js", note: "текст правил: 5 EN і 2 JA, приклад 5×5, 11 тест-дошок з кодами помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/kouchoku.js", note: "код pzprjs: Angle Loop ділить скрипт із Kouchoku й Tajmahal; кут через скалярний добуток, ввід відрізків, клавіші a/b/c"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json", note: "тексти помилок: lnPassOver, lnWrongAngle, nmLineLt2…"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/Changelog.md", note: "жанр зʼявився в pzprjs 0.11.0 (2019-04-17)"}
  - {kind: other, url: "https://mathequalslove.net/angle-loop-puzzles/", note: "родич: Angle Loop Наокі Інаби (角DEループ) — числа-градуси, петля через усі точки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=angle+loop+puzzle+puzz.link", note: "пошук"}
stage: v1
coverage: 65
mechanics: [path-drawing, single-loop-check, satisfy-constraints, markup-validity, completion-detection, conflict-highlight, keyboard-controls, settings-window, in-game-editor, editor-window, import-open-formats, undo-redo, help-window, fixture-level-tests, level-solver, +any-angle-segment, +node-graph-field, +visit-all-nodes, +crossing-detection, +angle-class-clue, +trial-mode]
proposes: ["+cond:angle", "+cond:crosses", "+cond:degree", "+card:angle-class-clue", "+card:any-angle-segment"]
author: opus
date: 2026-11-19
---

# Angle Loop — замкни петлю прямими відрізками через усі фігурки: у трикутнику кут гострий, у квадраті прямий, у пʼятикутнику тупий

## Суть
На точках решітки стоять фігурки трьох видів: трикутник, квадрат і пʼятикутник. Гравець зʼєднує їх прямими відрізками будь-якого нахилу в одну петлю, що проходить кожну фігурку рівно раз, без розгалужень, накладань і перетинів. Фігурка задає кут, під яким у ній сходяться два відрізки: трикутник — гострий, квадрат — рівно 90°, пʼятикутник — тупий; пройти фігурку навпростець (180°) не можна. Незвичне: підказка — не число й не напрямок, а **клас кута**, тож перевірка розвʼязку — шкільна геометрія векторів на решітці.

## Поле і час
- Квадратна сітка W×H клітинок, але гра йде на її точках, (W+1)×(H+1): фігурки стоять на перетинах, сітку намальовано пунктиром. Приклад puzz.link — 5×5 клітинок, 10 фігурок.
- Ребро петлі — відрізок між двома фігурками з будь-яким цілим вектором (dx, dy), не лише 8 напрямків. Суміжність задає «видимість» фігурок, а не сітка (`field: graph`, як у [Kouchoku](kouchoku.md)).
- Відрізок не може пройти крізь іншу фігурку; порожню точку решітки — може, але кінцем відрізка вона бути не може.
- Шари: фігурки (умова, edit) · відрізки (відповідь, play).
- Час статичний; хід = провести або стерти відрізок.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Трикутник ▲ | static | значення 1, чорна заливка | два відрізки сходяться під гострим кутом (0° < α < 90°) |
| Квадрат ▨ | static | значення 2, сіра заливка | два відрізки сходяться рівно під 90° |
| Пʼятикутник ⬠ | static | значення 3, біла заливка | два відрізки сходяться під тупим кутом (90° < α < 180°) |
| Порожня точка решітки | terrain | — | відрізок може пройти крізь неї, але не закінчитись на ній |
| Відрізок | mark | два кінці-фігурки, вектор (dx, dy) | прямий; не накладається на інший, не перетинає його, не проходить крізь фігурку |
| Петля | mark | — | одна; кожна фігурка має рівно 2 відрізки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, point_to_point)` → ЯКЩО `custom: «такого відрізка ще нема»` → ТО `mark(segment, line)`; інакше `unmark(segment)` (той самий жест стирає).
- КОЛИ `input(drag, point_to_point)` → ЯКЩО `mode(enline)` and `custom: «один із кінців — порожня точка»` → ТО `block` (налаштування puzz.link).
- КОЛИ `input(drag, point_to_point)` → ЯКЩО `mode(lattice)` and `custom: «на відрізку між кінцями лежить фігурка»` → ТО `block`.
- КОЛИ `constraint_broken(no_segment)` → ЯКЩО `count(segment, ==, 0)` → ТО `message(«There is no segment.»)` (код brNoLine).
- КОЛИ `constraint_broken(isolate)` → ЯКЩО `custom: «кінець відрізка — порожня точка»` → ТО `set_state(point, error)`, `message(«A segment starts outside a clue.»)` (lnIsolate).
- КОЛИ `constraint_broken(branch)` → ЯКЩО `custom: «у фігурці сходяться 3+ відрізки»` (`+cond:degree`) → ТО `set_state(symbol, error)`, `message(«There is a branch line.»)` (lnBranch).
- КОЛИ `constraint_broken(pass_over)` → ЯКЩО `custom: «фігурка лежить усередині відрізка»` → ТО `set_state(segment, error)`, `message(«A segment passes over a clue.»)` (lnPassOver).
- КОЛИ `constraint_broken(overlap)` → ЯКЩО `custom: «два відрізки лежать один на одному»` → ТО `set_state(segments, error)`, `message(«Some segments overlap.»)` (lnOverlap).
- КОЛИ `constraint_broken(multi_loop)` → ЯКЩО `not single_loop` → ТО `set_state(other_loop, error)`, `message(«There are multiple loops.»)` (lnPlLoop).
- КОЛИ `constraint_broken(dead_end)` → ЯКЩО `custom: «у фігурці рівно 1 відрізок»` (`+cond:degree`) → ТО `set_state(symbol, error)`, `message(«There is a dead-end line.»)` (lnDeadEnd).
- КОЛИ `constraint_broken(unvisited)` → ЯКЩО `custom: «у фігурки менше 2 відрізків»` (`+cond:degree`) → ТО `set_state(symbol, error)`, `message(«A clue doesn't have two segments.»)` (nmLineLt2).
- КОЛИ `constraint_broken(cross)` → ЯКЩО `custom: «два відрізки перетинаються»` (`+cond:crosses`) → ТО `set_state(segments, error)`, `message(«There is a crossing line.»)` (lnCross).
- КОЛИ `constraint_broken(angle)` → ЯКЩО `custom: «кут між двома відрізками фігурки не її класу»` (`+cond:angle`) → ТО `set_state(symbol, error)`, `message(«Some segments meet at the wrong angle.»)` (lnWrongAngle).
- Як рахується кут (код `checkAngle`): вектори від фігурки d1 і d2; d1·d2 > 0 — гострий (лише ▲), d1·d2 = 0 — прямий (лише ▨), d1·d2 < 0 — тупий (лише ⬠); колінеарні відрізки (кут 180°) — помилка для будь-якої фігурки.
- КОЛИ `all_constraints_met` → ТО `win`.
- Перемога: одна петля без розгалужень, тупиків, накладань і перетинів; кожна фігурка — рівно 2 відрізки під кутом свого класу. · Поразки й рахунку нема.
- Наслідки правил (дедукції): квадрат у куті поля можливий лише з відрізками вздовж обох країв (два невідʼємні вектори дають d1·d2 = 0 лише так) — до найближчих фігурок на цих краях; пʼятикутник у куті неможливий (d1·d2 ≥ 0); дві фігурки з третьою між ними на одній прямій не зʼєднуються напряму.

## Керування і ввід
- puzz.link play: натиснути на точці решітки й протягнути до іншої — відпущена кнопка ставить відрізок; той самий жест по наявному відрізку його стирає.
- Налаштування puzz.link, спільні з Kouchoku: `enline` — відрізок лише між двома фігурками; `lattice` — не дає провести відрізок крізь фігурку.
- puzz.link edit: курсор ходить по точках решітки; клавіші `a` / `b` / `c` — трикутник / квадрат / пʼятикутник (повтор прибирає), пробіл чи Backspace — стерти; клік мишею перебирає фігурки по колу; знака «?» нема (`disInputHatena`).

## Вікна, меню, HUD
- `game-screen` (puzz.link): пунктирна решітка, фігурки трьох заливок, відрізки; кнопки Check · Undo · Redo · Erase answer · Trial (оболонка — [puzz.link](puzz-link.md)); `conflict-highlight` — фігурка з помилкою фарбується кольором помилки, хибні відрізки — теж.
- `settings-window` (меню Setting): `enline`, `lattice`.
- `editor-window` — той самий екран у режимі Edit: розмір поля, фігурки, вивід URL (`+window:game-id-dialog` — див. [puzz.link](puzz-link.md)).
- `help-window` — rules.html?angleloop (English / 日本語).
- Переходи: rules → плеєр за URL → Check → «розвʼязано» або текст першої помилки.

## Фічі поза полем
- `auto-check` (off / guarded / simple) і Check з текстом першого порушеного правила (puzz.link).
- `undo` ∞ / `redo`; `+feature:trial-mode` — шар припущень з прийняттям чи відкатом.
- `level-editor` + `share-code`: пазл — URL `p?angleloop/5/5/…`, файли pzprv3.
- Нема генератора, банку рівнів, підказок.

## Варіації й родичі
- [Kouchoku](kouchoku.md) — той самий скрипт pzprjs: відрізки між вузлами під будь-яким кутом, але перетин дозволено (лише під 90° і не у вузлі), а букви групують вузли; в Angle Loop перетинів нема, кут задає фігурка.
- Tajmahal — третій жанр того ж скрипта `kouchoku.js` (правил не читав).
- Angle Loop Наокі Інаби (角DEループ, Math = Love) — петля через **усі** точки сітки, число в точці — кут у градусах (приклад — 120°); тут замість градусів три класи кута.
- [Masyu](masyu.md) — ортогональний аналог «підказка задає поворот»: чорна перлина — поворот, біла — прямо; тут прямо не можна ніде, а поворот поділено на гострий / прямий / тупий.
- [Slitherlink](slitherlink.md), [Country Road](country-road.md) — петлі по ортогоналях сітки.
- **Осі варіацій**: що каже підказка у вузлі (поворот/прямо — Masyu · клас кута — Angle Loop · точні градуси — Інаба) · напрямки відрізків (4 / 8 / будь-який вектор) · перетини (заборонені / лише під 90° — Kouchoku) · обовʼязкові точки (лише фігурки / усі точки).

## Цікавинки для курсу
- Клас кута через скалярний добуток цілих векторів (> 0 / = 0 / < 0) і заборона колінеарності — 🌱 (жодної тригонометрії й float).
- Чи лежить фігурка на відрізку: точки решітки на відрізку через `gcd(dx, dy)` — 📎.
- Перетин і накладання відрізків (орієнтації трійок точок, колінеарний випадок) — 📎.
- Одна петля через усі фігурки: ступінь 2 + звʼязність — 🥉 (картка `single-loop-check`).
- Ввід «від точки до точки» з прилипанням до решітки й помічниками `enline` / `lattice` — 📎.
- Дедукції-доведення: квадрат у куті — лише вздовж країв, пʼятикутника в куті не буває — 🌱 (вправа на знак скалярного добутку).
- Розвʼязувач: кандидати-ребра — пари фігурок без фігурки між ними; гамільтонів цикл з кутами й без перетинів — 🥇.

## Мапа на каталог
- Є: `path-drawing` ↔ відрізок протяжкою · `single-loop-check` ↔ одна петля · `satisfy-constraints`, `markup-validity`, `completion-detection`, `conflict-highlight` ↔ Check з кодами · `keyboard-controls` ↔ a/b/c у редакторі · `settings-window` ↔ enline/lattice · `in-game-editor`, `editor-window`, `import-open-formats` ↔ edit-режим і URL · `undo-redo` · `help-window` · `fixture-level-tests` ↔ тест-дошка на кожен код помилки · `level-solver`.
- Перевикористано: `+any-angle-segment`, `+node-graph-field` (Kouchoku) · `+visit-all-nodes` (LYNE, Kouchoku) · `+crossing-detection` · `+trial-mode` (puzz.link).
- **Нема** → пропозиції карток:
  - `+angle-class-clue` «Підказка-клас кута у вузлі шляху» · game-logic/constraints · 🌱 · слот {classes: acute|right|obtuse, straight: forbidden} — Angle Loop; родич `+turn-straight-clue` (Masyu).

## Пропозиції до словників
- `+cond:angle` — кут між двома відрізками у вузлі: acute / right / obtuse / straight (за знаком скалярного добутку); узагальнює `+cond:right_angle` з Kouchoku.
- `+cond:crosses` — повтор: два відрізки перетинаються.
- `+cond:degree` — повтор: скільки відрізків сходиться у вузлі (0 / 1 / 2 / 3+).
- `+card:angle-class-clue` — див. мапу; `+card:any-angle-segment` — повтор (Kouchoku).

## Джерела
- ⭐ [puzz.link: Angle Loop](https://puzz.link/rules.html?angleloop) — правила EN/JA і вхід у плеєр (текст рендериться JS).
- [pzpr-samples/angleloop.js](https://puzz.link/js/pzpr-samples/angleloop.js) — «Lines go straight from symbol to symbol, and can be drawn at any angle», гострий / прямий / тупий; JA: ▲ / ▨ / ⬠, «лінія повертає лише на фігурках»; приклад `5/5/…`; тест-дошки lnPassOver · lnIsolate · lnDeadEnd · lnCross · nmLineLt2 · lnBranch · lnPlLoop · lnWrongAngle ×4 · розвʼязок.
- [pzprjs kouchoku.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/kouchoku.js) — спільний скрипт kouchoku / angleloop / tajmahal; checklist Angle Loop з 10 перевірок, `checkAngle`, клавіші `a`–`c`, `maxnum: 3`, малювання фігурок.
- [failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json) — тексти помилок.
- [pzprjs Changelog](https://raw.githubusercontent.com/robx/pzprjs/main/Changelog.md) — «angleloop: Introduce new puzzle: Angle Loop», версія 0.11.0 від 2019-04-17.
- [Math = Love: Angle Loop Puzzles](https://mathequalslove.net/angle-loop-puzzles/) — однойменний родич Наокі Інаби (角DEループ).
- YouTube: [пошук «angle loop puzzle puzz.link»](https://www.youtube.com/results?search_query=angle+loop+puzzle+puzz.link).

## Непевне
- (?) Автор і перша публікація невідомі: поле `history` у puzz.link порожнє, пошук «鋭直鈍ループ» вивів лише на 角DEループ Інаби; відомо тільки, що в pzprjs жанр є з 0.11.0 (2019) — `year: null`.
- (?) Чи повʼязаний 鋭直鈍ループ з 角DEループ Інаби — спільна лише ідея «кут у точці петлі».
- (?) JA-правило «лінія повертає лише на фігурках» окремою перевіркою не реалізоване — воно випливає з того, що кінці відрізків мусять бути фігурками (lnIsolate).
- (?) Права кнопка миші й значення `enline` / `lattice` за замовчуванням — загальна поведінка pzpr; тестів вводу в жанру нема (`inputs: []`).
