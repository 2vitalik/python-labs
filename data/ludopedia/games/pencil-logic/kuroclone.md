---
title: Kuroclone (クロクローン)
slug: kuroclone
aka: [クロクローン, Чорний клон, Куроклон]
family: pencil-logic
also: []
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
  - {kind: other, url: "https://www.janko.at/Raetsel/Kuroclone/index.htm", best: true, note: "Janko: правила DE/EN/JA з прикладом і розвʼязком, 50 пазлів 6×6…17×17 у браузері, походження назви"}
  - {kind: play, url: "https://puzz.link/rules.html?kuroclone", note: "puzz.link: правила EN/JA і вхід у плеєр/редактор (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/kuroclone.js", note: "4 правила EN/JA, «first appeared in Puzzle Communication Nikoli vol. 153», приклад 6×6, 6 тест-дошок з кодами помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/kuroclone.js", note: "код pzprjs: checklist із 6 перевірок, ввід чисел зі стрілками, число не фарбується"}
  - {kind: other, url: "https://api.github.com/repos/robx/pzprjs/commits?path=src/variety/kuroclone.js", note: "історія файла: «Add Kuroclone (#388)», Subaru_Saito, 2023-03-07"}
  - {kind: other, url: "https://puzz.link/db/?type=kuroclone", note: "банк пазлів puzz.link (рендериться JS; лінк зі сторінки Janko)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Kuroclone+puzzle", note: "пошук"}
stage: v1
coverage: 70
mechanics: [cell-click, dot-mark, satisfy-constraints, markup-validity, completion-detection, conflict-highlight, keyboard-controls, in-game-editor, editor-window, import-open-formats, undo-redo, help-window, level-bank, fixture-level-tests, level-solver, +cell-shade-toggle, +irregular-regions, +shape-identity-check, +region-quota, +region-size-check, +no-touch-across-border, +trial-mode]
proposes: ["+cond:same_shape", "+cond:group_size", "+cond:count_in", "+cond:touch_across_border", "+card:no-touch-across-border"]
author: opus
date: 2026-11-19
---

# Kuroclone — зафарбуй у кожній області два блоки-«клони» однакової форми; стрілка з числом каже розмір блока, на який вказує

## Суть
Сітку поділено товстими межами на області; у деяких клітинках стоїть число зі стрілкою. Гравець зафарбовує клітинки так, щоб у кожній області вийшло рівно два блоки (4-звʼязні групи чорних) однакової форми — з точністю до поворотів і віддзеркалень. Чорні з різних областей не сусідять сторонами, тож кожен блок живе в одній області. Число зі стрілкою (саме завжди біле) — розмір блока, що займає сусідню клітинку в напрямку стрілки. Незвичне: головне обмеження — **конгруентність пари поліоміно** в кожній області, тоді як самі форми ніде не задано.

## Поле і час
- Квадратна сітка з довільними областями (поліоміно); у Janko — 6×6…17×17, приклад puzz.link — 6×6 з 4 областями.
- Сусідство ортогональне: і для злиття чорних у блок, і для заборони через межу; по діагоналі блоки можуть торкатися (у прикладі puzz.link два одиночні блоки однієї області стоять навскіс).
- Шари: межі областей і числа зі стрілками (умова) · стан клітинки гравця: невідомо / чорна / «біле».
- Час статичний; хід = змінити стан клітинки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Область | zone | довільне поліоміно | містить рівно 2 блоки однакової форми |
| Число зі стрілкою | static | N (1 … клітинок/2), напрямок ↑↓←→ | клітинка біла; сусідня за стрілкою — чорна, її блок має розмір N |
| Клітинка | mark | невідомо / чорна / «біле» | клік змінює стан |
| Блок (unit) | zone | розмір, форма | 4-звʼязна група чорних у межах однієї області |
| Межа області | static | ребро сітки | через неї чорні не сусідять |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ЯКЩО `not custom: «у клітинці число»` → ТО `mark(cell, shaded)`; повтор → `unmark(cell)` (схема puzz.link для зафарбовувань).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, dot)` — позначка «біле» (у puzz.link — кольором тла клітинки).
- КОЛИ `constraint_broken(across_border)` → ЯКЩО `custom: «дві чорні сусідять сторонами через межу області»` (`+cond:touch_across_border`) → ТО `set_state(cells, error)`, `message(«Shaded cells are adjacent over a border.»)` (код cbShade).
- КОЛИ `constraint_broken(arrow_target)` → ЯКЩО `not custom: «клітинка за стрілкою чорна»` → ТО `set_state(number, error)`, `message(«The cell next to the arrow is not shaded.»)` (anNoShade).
- КОЛИ `constraint_broken(arrow_size)` → ЯКЩО `custom: «розмір блока за стрілкою ≠ N»` (`+cond:group_size`) → ТО `set_state(number, error)`, `set_state(unit, error)`, `message(«The size of the pointed unit is not correct.»)` (anUnitNe).
- КОЛИ `constraint_broken(two_units)` → ЯКЩО `custom: «в області не рівно 2 блоки»` (`+cond:count_in`) → ТО `set_state(region, error)`, `message(«There is an area without exactly two units.»)` (bkUnitNe2).
- КОЛИ `constraint_broken(shape)` → ЯКЩО `not custom: «два блоки області однакові з точністю до поворотів і віддзеркалень»` (`+cond:same_shape`) → ТО `set_state(units, error)`, `message(«Two units in an area have different shapes.»)` (bkDifferentShape; перевіряється лише там, де блоків рівно 2).
- КОЛИ `constraint_broken(no_arrow)` → ЯКЩО `custom: «число без стрілки»` → ТО `set_state(number, error)`, `message(«A number has no arrow.»)` (anNoArrow — перевірка умови, а не відповіді).
- КОЛИ `all_constraints_met` → ТО `win`.
- Порядок перевірок puzz.link: через межу → стрілка на білу → розмір за стрілкою → два блоки в області → форма → число без стрілки.
- Перемога: у кожній області рівно два конгруентні блоки, чорні не сусідять через межі, кожна стрілка вказує на блок свого розміру, клітинки з числами білі. · Поразки й рахунку нема.
- Наслідки правил (дедукції): два блоки однієї області не торкаються сторонами (інакше це один блок); у звʼязній області з двома блоками розміру s щонайменше 2s + 1 клітинок; число N зі стрілкою задає розмір **обох** блоків своєї області-цілі; чорна біля межі робить білою сусідку за межею.

## Керування і ввід
- puzz.link play: ліва кнопка (з протяжкою) — фарба, права — «біле»; режими `shade` / `unshade`.
- puzz.link edit: межі областей — протяжкою по ребрах; число — клавішами або кліком; стрілка — протяжкою з клітинки в бік стрілки (режим `direc`); `clear` — стерти; найбільше число — половина клітинок поля.
- Janko: інтерактивна сітка — клік фарбує сірі клітинки в чорний або білий.
- Папір: чорнити клітинки олівцем.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка зі світлими лініями, товсті межі, числа зі стрілками, чорні клітинки, «біле» — тлом; кнопки Check · Undo · Redo · Erase answer · Trial (оболонка — [puzz.link](puzz-link.md)); `conflict-highlight` — область без пари, пара різної форми, хибне число чи блок за стрілкою.
- `editor-window` — той самий екран у режимі Edit: border · number · direc · clear, вивід URL.
- `help-window` — rules.html?kuroclone; Janko — сторінка правил із прикладом і розвʼязком.
- `puzzle-select` (Janko) — 50 пазлів, сортування за датою, розміром і складністю.
- Переходи: Janko список → пазл → перевірка; puzz.link rules → плеєр за URL → Check → «розвʼязано» або перша помилка.

## Фічі поза полем
- `auto-check` і Check з текстом першої помилки; `undo` ∞ / `redo`; `+feature:trial-mode` (puzz.link).
- `level-editor` + `share-code` (URL `p?kuroclone/6/6/…`), файли pzprv3.
- `puzzle-bank`: Janko — 50 пазлів (6×6 ×4, 8×8 ×10, 10×10 ×10, 12×12 ×10, 14×14 ×8, 17×17 ×8); puzz.link db.
- Нема генератора, підказок, рекордів.

## Варіації й родичі
- [Double Choco](double-choco.md) — теж «дві конгруентні частини», але область сама ділиться на білу й сіру половини однакової форми; тут — два чорні блоки всередині області, решта біла.
- [LITS](lits.md), [Statue Park](statue-park.md), [Chained Block](chained-block.md) — перевірка форми поліоміно з поворотами й віддзеркаленнями (`+shape-identity-check`).
- [Sto-Stone](sto-stone.md) — та сама заборона «чорні не сусідять через межу кімнат» (код cbShade), але блок у кімнаті один.
- Shimaguni (puzz.link) — звідти взято перевірку cbShade (коментар «From shimaguni.js» у коді).
- Kurotto — число каже розмір сусідніх чорних груп (Janko називає спорідненим жанром).
- **Осі варіацій**: скільки блоків в області (1 — Sto-Stone · 2 — Kuroclone) · що порівнюється в парі (форма з віддзеркаленням / лише розмір / нічого) · що каже число (розмір блока за стрілкою / розмір своєї групи — Nurikabe / сума сусідніх груп — Kurotto) · сусідство через межу (заборонене / дозволене).

## Цікавинки для курсу
- Блоки як 4-звʼязні компоненти чорних (BFS чи union-find) і групування блоків за областями — 🌱.
- Конгруентність двох блоків: нормалізація координат + 8 симетрій квадрата → канонічна форма — 📎.
- Адресація «клітинка + напрямок стрілки» → сусідня клітинка → розмір її блока — 🌱.
- Заборона сусідства через межу: обхід ребер між різними областями — 🌱.
- Валідація умови в редакторі: число без стрілки, межа числа (половина поля) — 🌱.
- Розвʼязувач: перебір пар конгруентних поліоміно в кожній області з обмеженнями стрілок і меж — 🥇.

## Мапа на каталог
- Є: `cell-click`, `dot-mark` ↔ фарба / «біле» · `satisfy-constraints`, `markup-validity`, `completion-detection`, `conflict-highlight` ↔ Check з кодами · `keyboard-controls`, `in-game-editor`, `editor-window`, `import-open-formats` ↔ редактор і URL · `undo-redo` · `help-window` · `level-bank` ↔ Janko, puzz.link db · `fixture-level-tests` ↔ тест-дошка на кожен код · `level-solver`.
- Перевикористано: `+cell-shade-toggle` · `+irregular-regions` · `+shape-identity-check` (слот {symmetry: rot+mirror, scope: pair-in-region}) · `+region-quota` (слот {n: 2, of: units}) · `+region-size-check` (слот {clue: arrow → сусідній блок}) · `+trial-mode`.
- **Нема** → пропозиції карток:
  - `+no-touch-across-border` «Чорні клітинки різних областей не сусідять сторонами» · game-logic/constraints · 🌱 · слот {colors: shaded|both} — Kuroclone, Sto-Stone, Shimaguni; `both` — варіант Aqre з межами.

## Пропозиції до словників
- `+cond:same_shape` — повтор (Double Choco, LITS): дві групи однакової форми з поворотами й віддзеркаленнями.
- `+cond:group_size` — повтор: розмір 4-звʼязної групи, до якої належить клітинка.
- `+cond:count_in` — повтор: кількість блоків в області (тут = 2).
- `+cond:touch_across_border` — повтор (Sto-Stone).
- `+card:no-touch-across-border` — див. мапу.

## Джерела
- ⭐ [Janko: Kuroclone](https://www.janko.at/Raetsel/Kuroclone/index.htm) — правила («Each region contains exactly two groups of black cells which must be congruent», «A cell with a number and an arrow is always white», «Black cells must not be orthogonally adjacent across region borders»), 50 пазлів, назва «чорний клон», автор і перша публікація невідомі («можливо, Nikoli»).
- [puzz.link: Kuroclone](https://puzz.link/rules.html?kuroclone) — правила й плеєр (рендериться JS).
- [pzpr-samples/kuroclone.js](https://puzz.link/js/pzpr-samples/kuroclone.js) — 4 правила EN/JA, «Puzzle Communication Nikoli vol. 153», приклад 6×6 з розвʼязком (пари доміно, L-тріоміно, одиночних клітинок і дзеркальних L-тетроміно), коди anNoShade · cbShade · anUnitNe · bkUnitNe2 · bkDifferentShape.
- [pzprjs kuroclone.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/kuroclone.js) — checklist, режими вводу, `numberRemainsUnshaded`, `maxnum` = клітинок / 2.
- [failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json) — тексти помилок.
- [Історія kuroclone.js](https://api.github.com/repos/robx/pzprjs/commits?path=src/variety/kuroclone.js) — жанр у puzz.link з 2023-03-07.
- [JA-Вікіпедія: パズル通信ニコリ](https://ja.wikipedia.org/wiki/パズル通信ニコリ) — дати випусків журналу (для оцінки року).
- YouTube: [пошук «Kuroclone puzzle»](https://www.youtube.com/results?search_query=Kuroclone+puzzle).

## Непевне
- (?) Рік: Nikoli vol.153 — за JA-Вікі vol.150 вийшов навесні 2015, журнал щоквартальний, тож vol.153 ≈ кінець 2015; прямої дати не бачив, `year: null`. Janko автора й першої публікації не знає.
- (?) Дії мишею в puzz.link (ліва — фарба, права — «біле») — загальна схема pzpr для зафарбовувань; тестів вводу в жанру нема.
- (?) Як саме вводиться стрілка з клавіатури (Shift + стрілки) — типово для pzpr, у коді жанру видно лише `key_inputdirec`.
