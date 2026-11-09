---
title: Tawamurenga (たわむれんが)
slug: tawamurenga
aka: [Tawa, たわむれんが, Цегляна стіна]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: hex
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: null
platforms: [paper, web]
links:
  - {kind: other, url: "https://puzz.link/rules.html?tawa", best: true, note: "puzz.link: правила EN/JA і поле-приклад (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/tawa.js", note: "puzz.link: 4 правила, історія (Nikoli vol.127), коди помилок, тести вводу на полях 5×5, 5×2, 9×2"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/tawa.js", note: "pzprjs: код — 4 форми цегляної стіни, 6 сусідів, перевірки опори й трійок"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Tawa/index.htm", note: "Janko: правила DE/EN, пазли для гри в браузері, «автор невідомий»"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json", note: "pzprjs: тексти помилок tawa"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tawamurenga+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [cell-click, keyboard-controls, dot-mark, neighbor-count-clue, markup-validity, completion-detection, satisfy-constraints, conflict-highlight, undo-redo, field-size-picker, in-game-editor, import-open-formats, level-bank, level-solver, +cell-shade-toggle, +support-rule, +brick-offset-grid, +no-three-in-row]
proposes: ["+cond:run_length", "+card:brick-offset-grid", "+card:no-three-in-row", "+card:support-rule"]
author: opus
date: 2026-11-09
---

# Tawamurenga — зафарбуй цеглини стіни так, щоб кожна чорна спиралася на чорну знизу і жодні три не стояли поспіль

## Суть
Поле — цегляна кладка: ряди прямокутних цеглин, кожен ряд зсунутий на півцеглини відносно сусіднього. Гравець зафарбовує цеглини: кожна чорна (крім нижнього ряду) мусить мати чорну під собою, у ряду не можна мати 3 і більше чорних поспіль, число — скільки з 6 сусідніх цеглин чорні. Незвичне: **сітка-кладка** (топологічно гексагональна, 6 сусідів) і **«гравітація» як обмеження** — чорні стоять «вежами», що спираються на нижній ряд.

## Поле і час
- Кладка з рядів цеглин; ширина задається кількістю цеглин у верхньому ряду. Код pzprjs знає 4 форми країв: другий ряд «втягнутий з обох боків», «виступає праворуч», «виступає ліворуч», «виступає з обох боків».
- Сусідство: 2 цеглини зверху, 2 знизу, 1 ліворуч, 1 праворуч — 6, як у гекс-сітці; на краях менше.
- Орієнтація важлива: «знизу» має сенс (вісь `gravity: down` — статично, лише як обмеження, нічого не падає).
- Шари: числа (незмінні) · стан цеглини гравця: невідомо / чорна / крапка («точно біла»).
- Час статичний; хід = зміна стану однієї цеглини.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Цеглина | mark | стан unknown / shaded / dot | клік змінює стан |
| Чорна цеглина | mark | — | спирається хоча б на одну чорну з двох нижніх; ≤ 2 поспіль у ряду |
| Цеглина з числом | static | 0…6 | ніколи не чорна; рахує чорні серед 6 сусідів |
| Крапка | mark | — | позначка гравця «тут біле», на перевірку не впливає |
| Нижній ряд | zone | — | чорним тут опора не потрібна |
| Ряд | zone | — | серія чорних підряд ≤ 2 |
| Край стіни | static | форма 0–3 | на виступі в цеглини лише одна нижня сусідка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, brick)` → ТО `mark(brick, shaded)`; повтор → `unmark(brick)` (?).
- КОЛИ `input(right_click, brick)` → ТО `mark(brick, dot)` (?).
- КОЛИ `input(click, clue_brick)` → ТО `custom: «зафарбування ігнорується — число завжди біле»` (`numberRemainsUnshaded`).
- КОЛИ `constraint_broken(no_shade)` → ЯКЩО `count(shaded, ==, 0)` → ТО `message(brNoShade)`.
- КОЛИ `constraint_broken(row_run)` → ЯКЩО `custom: «≥ 3 чорні цеглини поспіль у ряду»` (`+cond:run_length`) → ТО `message(csConsecGt3)` («Three or more shaded cells continue horizontally»).
- КОЛИ `constraint_broken(support)` → ЯКЩО `not supported(shaded_brick)` and `custom: «цеглина не в нижньому ряду»` → ТО `message(csNotOnShade)` («no shaded cells under a shaded cell»).
- КОЛИ `constraint_broken(clue)` → ЯКЩО `not adjacent_count(clue, shaded, ==, n)` (6 сусідів) → ТО `message(nmShadeNe)`.
- КОЛИ `all_constraints_met` → ТО `win`.
- Звʼязності білих чи чорних правила **не** вимагають — чорні можуть утворювати кілька окремих «веж».
- Дедукція «вежа до низу»: за індукцією кожна чорна цеглина зʼєднана ланцюжком чорних донизу аж до нижнього ряду; чорна, під якою обидві нижні білі (або числа), неможлива.
- Дедукція «пара в ряду»: дві чорні поруч → цеглини одразу ліворуч і праворуч від пари білі.
- Дедукція «0»: усі 6 сусідів білі; цеглина, обидві нижні сусідки якої серед них (або є числами), теж біла.
- Дедукція «виступ краю»: цеглина на виступі має одну нижню сусідку — якщо вона біла, цеглина над нею біла.
- Перемога: числа виконані, чорні мають опору, нема трьох поспіль, хоча б одна чорна. Поразки й рахунку нема.

## Керування і ввід
- puzz.link play mode: режими `shade` / `unshade`; клік по цеглині визначається за півклітинною адресою (`getcell` з поправкою на зсув ряду).
- Курсор клавіатури: вгору/вниз переходить на ліву чи праву з двох цеглин сусіднього ряду (`movedir` з поправкою на зсув).
- Edit mode: числа 0–6 з клавіатури або кліком; форма стіни — при створенні поля (`setShape`).
- Undo/redo, Check (перша помилка з кодом), Clear.
- Janko (інтерактивно): сірі цеглини фарбуються в чорне або біле.

## Вікна, меню, HUD
- `game-screen`: кладка з тонкими швами (`drawGrid_tawa`), числа, чорні цеглини, крапки + `conflict-highlight` (трійка в ряду, цеглина без опори, число з неправильним лічильником разом із сусідами).
- Кнопки: Check, Undo, Redo, Clear answer.
- `editor-window` — puzz.link edit mode: розмір, форма країв, числа, експорт URL.
- `help-window` — правила (puzz.link, Janko).
- `puzzle-select` — архів Janko (цифрова версія).
- `end-screen` — повідомлення «розвʼязано».
- Переходи: editor → game-screen → Check → помилка / end-screen.

## Фічі поза полем
- `auto-check` за кнопкою з кодом порушення; `undo` / `redo`.
- `custom-difficulty`: розмір стіни й одна з 4 форм країв.
- `level-editor` + `share-code` (URL puzz.link).
- `puzzle-bank`: журнал Nikoli (час від часу), Janko.

## Варіації й родичі
- Родичі в сімʼї: [Dosun-Fuwari](dosun-fuwari.md) (опора знизу як обмеження), [Sto-Stone](sto-stone.md) («падіння» як перевірка), [Takuzu](takuzu.md) (нема трьох поспіль), [Light Up](light-up.md) і [Fill-a-Pix](fill-a-pix.md) (число рахує сусідів), [Hexologic](hexologic.md) (гекс-сусідство).
- Поза сімʼєю: `falling-match` і `dig-gravity` — там опора динамічна (падіння), тут лише статична перевірка кінцевого стану.
- **Осі варіацій**: сусідство числа (6 / лише ряд) · опора (≥ 1 знизу / обидві знизу / нема) · обмеження ряду (≤ 2 / ≤ k / нема) · форма краю стіни (4 типи) · звʼязність (нема / чорні звʼязні).

## Цікавинки для курсу
- Модель цегляної кладки: координати з півкроком, 6 сусідів, 4 форми країв — 🌱 (та сама арифметика, що й гекс-сітка «offset rows»).
- Рендер кладки й клік по цеглині з поправкою на зсув ряду — 📎.
- Перевірки: трійки в ряду, опора знизу, лічильник 6 сусідів — 🌱.
- Курсор клавіатури по кладці (вгору — ліва чи права цеглина) — 🌱.
- Розвʼязувач: CSP над бітами цеглин + дедукція «вежа до низу» — 🥉.
- Генератор з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `cell-click`, `keyboard-controls` · `dot-mark` · `neighbor-count-clue` ↔ число рахує 6 сусідів · `markup-validity`, `completion-detection`, `satisfy-constraints`, `conflict-highlight` · `undo-redo` · `field-size-picker` ↔ розмір і форма · `in-game-editor`, `import-open-formats`, `level-bank`, `level-solver`.
- Перевикористано: `+cell-shade-toggle` (Hitori, Heyawake) · `+support-rule` (Akropolis, Taluva — там опора для плиток у висоту).
- **Нема** → пропозиції карток:
  - `+brick-offset-grid` «Цегляна кладка: ряди зі зсувом на півклітинки, 6 сусідів» · entities/legality · 🌱 · слоти {edge_shape: 0..3} — родич `+hex-grid-render`.
  - `+no-three-in-row` «Не більше K однакових поспіль у ряду» · game-logic/constraints · 🌱 · слоти {k: 2, axis: row|row+col} — Tawamurenga, Takuzu.
  - `+support-rule` «Розмічена клітинка мусить мати розмічену опору знизу» · game-logic/constraints · 🌱 · слоти {need: any|all, base: bottom-row}.

## Пропозиції до словників
- `+cond:run_length` — довжина серії однакових клітинок підряд у ряду (повтор з Drop7).
- `+card:brick-offset-grid`, `+card:no-three-in-row`, `+card:support-rule` — див. мапу.

## Джерела
- ⭐ [puzz.link: Tawamurenga](https://puzz.link/rules.html?tawa) — сторінка правил і приклад (текст рендериться JS).
- [puzz.link: tawa.js](https://puzz.link/js/pzpr-samples/tawa.js) — правила EN/JA, «first appeared in Puzzle Communication Nikoli vol. 127», коди `brNoShade`, `nmShadeNe`, `csNotOnShade`, `csConsecGt3`.
- [pzprjs: tawa.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/tawa.js) — 4 форми стіни, 6 сусідів числа, перевірка опори, курсор по кладці.
- [Janko: Tawa](https://www.janko.at/Raetsel/Tawa/index.htm) — правила DE/EN, «автор і перша публікація невідомі», назва «здається неперекладною».
- [pzprjs: failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json) — тексти помилок tawa.

## Непевне
- (?) Рік: Nikoli vol.127 — за датуванням номерів у JA-Вікіпедії (№130 — весна 2010, журнал квартальний) це приблизно літо 2009; прямої дати не бачив.
- (?) Назва: れんが = цегла; たわむれ — «гра, забава» (тоді «грайлива цегла»); Janko вважає назву неперекладною. `aka` «Цегляна стіна» — описова, не усталена.
- (?) Розкладка мишею в puzz.link (ліва/права кнопка) — за загальною схемою зафарбовувань.
- (?) Скільки пазлів в архіві Janko — сторінка показала лише кілька номерів.
