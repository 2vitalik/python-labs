---
title: Yajisan-Sokoban (Yajisoko)
slug: yajisan-sokoban
aka: [Yajisoko, やじさんソコバン, Яджісан-Сокобан]
family: pencil-logic
also: [push-slide]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: null
platforms: [paper, web]
links:
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/yajisoko.js", best: true, note: "puzz.link: правила EN/JP, автор Jamie Hargrove, тестові поля й коди помилок"}
  - {kind: other, url: "https://puzz.link/rules.html?yajisoko", note: "puzz.link: сторінка правил (рендериться JS)"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json", note: "pzprjs: тексти помилок, зокрема yajisoko"}
  - {kind: other, url: "https://hutthutthuttspuzzledump.blogspot.com/2025/12/a52-yajisan-sokoban-and-exercise.html", note: "блог автора пазлів: «відчувається як сокобан», звʼязок назви з Yajisan-Kazusan"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=yajisan+sokoban+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, path-drawing, path-cut, push-object, cell-click, level-solver, level-bank, in-game-editor, import-open-formats, undo-redo, +arrow-count-clue, +straight-move-line, +crossing-detection, +clue-void-when-covered]
proposes: ["+cond:count_dir", "+cond:crosses", "+cond:turns", "+cond:clue_covered", "+card:straight-move-line", "+card:clue-void-when-covered"]
author: opus
date: 2026-11-09
---

# Yajisan-Sokoban — сокобан як статичний пазл: намалюй прямі шляхи ящиків так, щоб стрілки-підказки рахували ящики правильно

## Суть
На сітці стоять ящики і клітинки-підказки зі стрілкою та числом. Гравець вирішує, які ящики зрушити і куди: рух ящика малюється прямою лінією по горизонталі чи вертикалі від старту до фінішу, без поворотів. Лінії не перетинаються і не накладаються, не проходять через старт чи фініш інших ящиків. Число зі стрілкою — скільки ящиків стоїть у тому напрямку **після руху**; якщо ящик зупинився на підказці, вона втрачає силу. Незвичне: рух з `push-slide` перетворено на обмеження — розвʼязок — набір траєкторій, а не послідовність ходів.

## Поле і час
- Прямокутна сітка (у тестах puzz.link — 2×2, 3×3, 4×4).
- Клітинки: порожні, з ящиком (старт), з підказкою «стрілка + число».
- Шари: ящики й підказки (незмінні) · лінії руху гравця (сегменти між центрами сусідніх клітинок) · підсумкове положення ящиків (кінець лінії).
- Час статичний: порядок рухів не важить, бо лінії не перетинаються — усі рухи «одночасні».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ящик | object | стартова клітинка | лишається на місці або їде прямо в одному з 4 напрямків до кінця своєї лінії |
| Лінія руху | mark | старт, напрямок, довжина | пряма, з одного ящика; не гілкується, не повертає |
| Підказка-стрілка | static | напрямок, число n | у напрямку стрілки після руху рівно n ящиків |
| Накрита підказка | static | — | ящик зупинився на ній → число не діє (може бути як істинним, так і хибним) |
| Порожня клітинка | terrain | — | через неї може пройти одна лінія |
| Зафарбована клітинка | static | — | лінія не проходить (pzprjs `lnOnShade`) (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_drag, box → cells)` → ТО `custom: «намалювати лінію руху від ящика»`; drag назад по лінії — укоротити (`path-cut`) (?).
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінія повертає»` (`+cond:turns`) → ТО конфлікт (pzprjs `laCurve`).
- КОЛИ `constraint_broken(line)` → ЯКЩО `pattern(loop_branch)` → ТО конфлікт (`lnBranch`).
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінії перетинаються»` (`+cond:crosses`) → ТО конфлікт (`lnCross`).
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінія проходить через клітинку іншого ящика (старт чи фініш)»` → ТО конфлікт (`laOnNum`: «A line goes through a box»).
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінія зʼєднує два ящики»` → ТО конфлікт (`nmConnected`: «There are connected boxes») (?).
- КОЛИ `constraint_broken(line)` → ЯКЩО `not custom: «лінія починається з ящика»` → ТО конфлікт (`laIsolate`).
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінія перетинає межу»` → ТО конфлікт (`laOnBorder`) (?).
- Рух: КОЛИ `custom: «лінія завершена»` → ТО `move(box, line_end)` (кінцеве положення = кінець лінії; без лінії — на місці).
- КОЛИ `constraint_broken(clue)` → ЯКЩО `not custom: «ящик стоїть на підказці»` (`+cond:clue_covered`) and `custom: «ящиків у напрямку стрілки ≠ n»` (`+cond:count_dir`) → ТО конфлікт (`anShadeNe`: «The number of boxes is not correct»).
- КОЛИ `custom: «ящик зупинився на підказці»` (`+cond:clue_covered`) → ТО `custom: «підказка вимикається»`.
- Підказка, через яку ящик лише проїхав, лишається чинною (Cross+A, за результатом пошуку).
- КОЛИ `all_constraints_met` → ТО `win`.
- Редактор: КОЛИ `constraint_broken(clue)` → ЯКЩО `custom: «число без стрілки»` → ТО помилка вводу (`anNoArrow`).
- Дедукція «зайнятий коридор»: лінія ящика не може пройти через іншу лінію чи інший ящик — доступна довжина руху обмежена найближчою перешкодою.
- Дедукція «рахунок по стрілці»: ящики, що можуть увійти у промінь стрілки чи вийти з нього, — кандидати; число n відсікає варіанти руху.
- Дедукція «накрити, щоб вимкнути»: суперечливу підказку можна «вимкнути», лише поставивши на неї ящик — це прямо дає місце фінішу.
- Перемога: усі лінії прямі, без перетинів і накладань, кожна з ящика; кожна ненакрита підказка правильна. Поразки й рахунку нема.

## Керування і ввід
- puzz.link: ліва кнопка + drag — лінія по центрах клітинок; права кнопка — стерти/мітка (тести `mouse,left` у failcheck) (?).
- Edit mode: ящики й підказки зі стрілками ставить автор пазла; стрілка задається напрямком drag (?).
- Цифрова версія: undo/redo, перевірка за кнопкою з повідомленням першої помилки.

## Вікна, меню, HUD
- `game-screen`: сітка, ящики, підказки зі стрілками, лінії руху, `conflict-highlight`.
- puzz.link: перемикач play/edit, кнопка перевірки, `settings-window`.
- `help-window` — правила (puzz.link rules).
- Переходи: edit → play; check → повідомлення з кодом помилки.

## Фічі поза полем
- `auto-check` за кнопкою (коди pzprjs).
- `undo` / `redo`; `level-editor` + `share-code` (URL пазла).
- Банк: авторські пазли (puzz.link, Puzzle Square JP за згадкою в блозі) (?).
- Блог: бракує редактора, що показує рух ящиків, — один з бар'єрів для авторів.

## Варіації й родичі
- Автор — Jamie Hargrove (puzz.link).
- Назва: «Yajisan» — ймовірно від [Yajisan-Kazusan](https://en.wikipedia.org/wiki/Yajisan-Kazusan) через правило «накрита підказка не діє»; «Sokoban» — «кладовщик» (блог, як здогад).
- Родичі в сімʼї: [Yajilin](yajilin.md) (стрілки з числом, лінія), [Icebarn](icebarn.md) (прямий рух як обмеження шляху), [Kuromasu](kuromasu.md).
- Поза сімʼєю: Sokoban і `push-slide` — динамічний рух ящиків; тут — лише кінцеві траєкторії.
- Інші «рухові» жанри puzz.link з черги: Herugolf, Rectangle-Slider, Tren (не описані).
- **Осі варіацій**: траєкторія (пряма / з поворотами) · порядок руху (одночасно / послідовно) · що рахує підказка (ящики / клітинки / відстань) · накрита підказка (вимкнена / хибна / заборонено накривати).

## Цікавинки для курсу
- Перевірка ліній: пряма, без гілок, без перетинів, з ящика — 🌱.
- Підрахунок ящиків у напрямку стрілки з правилом «накрита — вимкнена» — 🌱.
- Анімація «програти» розвʼязок: ящики їдуть по своїх лініях одночасно — 📎.
- Розвʼязувач: для кожного ящика перелічити (напрямок, довжина), CSP з неперетином і лічильниками — 🥇.
- Генератор: випадкові ящики й рухи → підказки → вибір мінімального набору з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `path-drawing`, `path-cut` ↔ лінії руху · `push-object` ↔ рух ящика (тут без штовхача; тег за змістом «ящик зсувається, якщо вільно») · `cell-click` · `level-solver`, `level-bank`, `in-game-editor`, `import-open-formats`, `undo-redo`.
- Перевикористано: `+arrow-count-clue` (з Yajilin), `+crossing-detection` (з Icebarn).
- **Нема** → пропозиції карток:
  - `+straight-move-line` «Рух обʼєкта як пряма лінія без поворотів» · game-logic/constraints · 📎 · слот {turns: 0|any, overlap: no}.
  - `+clue-void-when-covered` «Накрита обʼєктом підказка не діє» · game-logic/constraints · 🌱 — Yajisan-Sokoban, Yajisan-Kazusan.

## Пропозиції до словників
- `+cond:count_dir` — кількість сутностей у напрямку від клітинки (повтор з Yajilin).
- `+cond:crosses`, `+cond:turns` — лінія перетинає себе/іншу, лінія повертає (повтори з Icebarn).
- `+cond:clue_covered` — на клітинці-підказці стоїть обʼєкт.
- `+card:straight-move-line`, `+card:clue-void-when-covered` — див. мапу.

## Джерела
- ⭐ [puzz.link: yajisoko.js](https://puzz.link/js/pzpr-samples/yajisoko.js) — правила EN/JP (3 пункти), автор Jamie Hargrove, тестові поля 2×2…4×4 і коди помилок.
- [puzz.link: rules](https://puzz.link/rules.html?yajisoko) — сторінка правил (без JS текст не віддає).
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json) — тексти помилок `yajisoko`: кількість ящиків, лінія через ящик, через зафарбовану, зʼєднані ящики.
- [Hutthutthutt's Puzzle Dump #A52](https://hutthutthuttspuzzledump.blogspot.com/2025/12/a52-yajisan-sokoban-and-exercise.html) — враження автора пазлів, здогад про назву.
- YouTube: пошук «yajisan sokoban puzzle».

## Непевне
- (?) `nmConnected` («connected boxes»): лінія зʼєднує два ящики чи ящики не можуть стояти поруч після руху — тексти помилки не досить; правила про сусідство мовчать.
- (?) `laOnBorder` («line across a border») і `lnOnShade` (зафарбовані клітинки) — які елементи поля їх викликають, не зʼясував.
- (?) Чи може лінія пройти через клітинку-підказку — Cross+A (лише сніпет пошуку, сторінка не відкрилась) каже, що так.
- (?) Рік винаходу; розкладка вводу puzz.link.
