---
title: Satogaeri (Сатоґаері, «Повернення додому»)
slug: satogaeri
aka: [さとがえり, Сатоґаері, Homecoming, Повернення додому]
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
year: 2002
platforms: [paper, web]
links:
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/satogaeri/", best: true, note: "Nikoli: 3 правила, Sample → Progressing → Solution, історія (vol.99, 2002, автор Z_H, повернення 2013)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/satogaeri.js", note: "puzz.link: правила EN/JA, коди помилок"}
  - {kind: play, url: "https://puzz.link/rules.html?satogaeri", note: "puzz.link: сторінка правил і вхід у плеєр/редактор"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Satogaeri/index.htm", note: "Janko: правила, значення назви, родичі Yosenabe/Herugolf, 150 пазлів 8×8…15×15"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Satogaeri+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [path-drawing, path-cut, satisfy-constraints, markup-validity, completion-detection, conflict-highlight, cell-click, keyboard-controls, in-game-editor, import-open-formats, level-bank, impassable-cells, undo-redo, level-solver, +straight-move-line, +exact-distance-move, +one-per-region-final, +show-final-position]
proposes: ["+cond:straight_line", "+cond:line_length", "+cond:region_has", "+cond:crosses", "+card:exact-distance-move", "+card:one-per-region-final", "+card:straight-move-line", "+card:show-final-position"]
author: opus
date: 2026-11-09
---

# Satogaeri — пересунь кружки прямо по рядку чи стовпцю рівно на їхнє число, щоб у кожній «країні» опинився один

## Суть
Поле поділене жирними лініями на «країни»; у клітинках стоять кружки, частина з числами. Кожен кружок можна пересунути по прямій — горизонтально чи вертикально, без поворотів: числовий рівно на N клітинок, без числа — на будь-яку відстань або ніяк. Сліди руху не перетинаються й не накладаються, а кружок не може проїхати через інший. Наприкінці в кожній країні рівно один кружок.

## Поле і час
- Прямокутна сітка, розбита на регіони-«країни»; банк Janko — 8×8, 10×10, 12×12, 15×15.
- Шари: регіони (незмінні) · кружки на старті · лінії-сліди гравця · похідне: кінцеві позиції кружків.
- Рух — відрізок по ортогоналі через центри клітинок від старту до фінішу.
- Час статичний; хід = провести або стерти відрізок.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кружок з числом | object | N | їде по прямій рівно на N клітинок, без повороту |
| Кружок без числа | object | — | їде на будь-яку відстань або лишається на місці |
| Країна (регіон) | zone | межі жирними лініями | наприкінці містить рівно один кружок |
| Слід руху | mark | довжина | від старту до фінішу; не перетинає й не торкається іншого сліду |
| Кінцева позиція | mark | — | похідна; на ній не може бути старту чи сліду іншого кружка |
| Межа поля | static | — | кружок не виїжджає за край |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, circle → cell)` → ЯКЩО `custom: «пряма по ортогоналі»` (`+cond:straight_line`) → ТО `mark(segment, line)`.
- КОЛИ `input(right_drag, line)` → ТО `unmark(segment)` (puzz.link).
- КОЛИ `custom: «слід має поворот»` → ТО `constraint_broken(curve)` (puzz.link `laCurve`).
- КОЛИ `custom: «слід кружка з числом N завершено»` → ЯКЩО `custom: «довжина ≠ N»` (`+cond:line_length`) → ТО `constraint_broken(length)` (`laLenNe`).
- КОЛИ `custom: «кружок з числом без сліду»` → ТО `constraint_broken(no_move)` (`nmNoMove`) (?).
- КОЛИ `custom: «слід проходить клітинку»` → ЯКЩО `occupied(cell, circle)` → ТО `constraint_broken(over_circle)` (`laOnNum`).
- КОЛИ `custom: «два сліди в одній клітинці»` → ТО `constraint_broken(cross)` (`lnCross`, `lnBranch`; `+cond:crosses`).
- КОЛИ `custom: «один слід зʼєднує два кружки»` → ТО `constraint_broken(connected)` (`nmConnected`).
- КОЛИ `custom: «слід не починається з кружка»` → ТО `constraint_broken(isolated_line)` (`laIsolate`).
- КОЛИ `edge(circle)` → ТО `block`.
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «у кожній країні рівно один кружок за кінцевими позиціями»` (`+cond:region_has`) → ТО `win`; країна без кружка — `bkNoNum`.
- Кружок без числа може лишитись на місці: тоді він рахується у своїй стартовій країні (Nikoli: «деякі не рухаються»).
- Перемога: у кожній країні один кружок, усі довжини правильні, сліди не перетинаються. · Поразки й рахунку нема.

## Керування і ввід
- Папір (Nikoli): лінія від кружка до нової клітинки, кружок обводиться там.
- puzz.link: drag лівою від кружка — слід по клітинках; права кнопка — стерти; edit mode — числа, кружки без числа (`-`), межі регіонів.
- Зручно (?): показувати кружок у кінці сліду, а на старті — тінь (як `dispmove` у Herugolf).

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка з жирними межами країн, кружки, сліди; `check-button`, `undo-button`, `redo-button`; `conflict-highlight` після перевірки (?).
- `editor-window` (puzz.link edit mode): розмір, межі регіонів, кружки й числа; експорт у URL.
- `help-window`: сторінка правил (Nikoli — Sample → Progressing → Solution).
- `puzzle-select` (Janko): 150 пазлів за розміром і складністю 1–8.
- Переходи: puzz.link rules → URL пазла → game-screen → Check → «розвʼязано» (?).

## Фічі поза полем
- `auto-check` за кнопкою: перший знайдений код помилки (puzz.link).
- `undo` / `redo` (puzz.link) (?).
- `level-editor` + `share-code` — пазл як URL puzz.link.
- `puzzle-bank` (Janko: 150 пазлів).

## Варіації й родичі
- Janko: родичі Yosenabe і [herugolf](herugolf.md) — «рух предмета, записаний лінією»; у Herugolf удари коротшають і є повороти, тут — один прямий рух.
- [Saltatori](saltatori.md) — стрибок фіксованої довжини, але з перельотом і 8 напрямками; [tren](tren.md) — число каже, на скільки вагончик *може* відʼїхати.
- [Yajisan-Sokoban](yajisan-sokoban.md) — інший пазл з рухом по прямій.
- Регіони «по одному»: [star-battle](star-battle.md), [heyawake](heyawake.md) — обмеження на регіон, але без руху.
- **Осі варіацій**: довжина руху (рівно N / до N / будь-яка) · повороти (нема / є) · ціль (по одному в регіоні / у лунку / у групу) · чи може кружок лишитись.

## Цікавинки для курсу
- Валідація сліду: прямий, правильної довжини, починається з кружка — 🌱.
- Перевірка «сліди не перетинаються й не проходять через чужий старт/фініш» — 📎 (множина зайнятих клітинок).
- Підрахунок кружків по регіонах за кінцевими позиціями — 🌱.
- Розвʼязувач: для кожного кружка 0–4 варіанти (числовий) або до 4·L (без числа) + exact cover по регіонах з забороною перетинів — 🥈.
- Рендер «кружок у кінці, тінь на старті» — 🌱.
- Генератор з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `path-drawing`, `path-cut` ↔ сліди · `satisfy-constraints`, `markup-validity`, `conflict-highlight`, `completion-detection` · `cell-click`, `keyboard-controls` ↔ редактор puzz.link · `in-game-editor`, `import-open-formats` ↔ URL · `level-bank` ↔ Janko · `impassable-cells` ↔ край і чужі кружки · `undo-redo` · `level-solver`.
- **Нема** → пропозиції карток:
  - `+exact-distance-move` «Обʼєкт переміщується по прямій рівно на N» · entities/move · 🌱 · слот {exact|max|any}.
  - `+one-per-region-final` «Після руху в кожному регіоні рівно один обʼєкт» · game-logic/constraints · 🌱.
  - `+straight-move-line` (повтор із Yajisan-Sokoban), `+show-final-position` (повтор із Herugolf).

## Пропозиції до словників
- `+cond:straight_line` — відрізок без поворотів (повтор із корпусу).
- `+cond:line_length` — довжина сліду дорівнює числу (повтор).
- `+cond:region_has` — у регіоні рівно N обʼєктів виду (повтор).
- `+cond:crosses` — лінії перетинаються / накладаються (повтор).
- `+card:exact-distance-move`, `+card:one-per-region-final`, `+card:straight-move-line`, `+card:show-final-position` — див. мапу.

## Джерела
- ⭐ [Nikoli: Satogaeri](https://www.nikoli.co.jp/en/puzzles/satogaeri/) — правила (рух по вертикалі/горизонталі, один кружок на країну; число = скільки клітинок; без числа — будь-скільки, деякі не рухаються; не перетинати сліди й не проходити через кружки), дебют 2002 у Nikoli vol.99, автор Z_H, повернення на nikoli.com у 2013.
- [puzz.link satogaeri.js](https://puzz.link/js/pzpr-samples/satogaeri.js) — правила EN/JA («не може проїхати через старт чи фініш іншого», «без числа — може не рухатись»), коди `brNoLine lnBranch lnCross nmConnected laOnNum laCurve laLenNe bkNoNum nmNoMove laIsolate`.
- [puzz.link rules](https://puzz.link/rules.html?satogaeri) — сторінка правил (рендериться JS).
- [Janko: Satogaeri](https://www.janko.at/Raetsel/Satogaeri/index.htm) — правила DE/EN, назва ≈ «повернення додому», родичі, 150 пазлів.
- YouTube: пошук «Satogaeri puzzle».

## Непевне
- (?) Автор: Nikoli — Z_H, Janko — Ichinokoto; обидва кажуть «vol.99», Janko — червень 2002.
- (?) `nmNoMove` — у pzprjs текст «A circle doesn't move»; що саме він ловить для Satogaeri (числовий кружок без сліду) — висновок з назви.
- (?) Код для країни з ≥2 кружками в тестах puzz.link не показано (у pzprjs є загальний `bkNumGe2`).
- (?) Undo/redo, «розвʼязано» й підсвітка помилок — загальна поведінка pzpr, не перевірена саме для Satogaeri.
