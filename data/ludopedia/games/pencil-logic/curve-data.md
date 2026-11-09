---
title: Curve Data
slug: curve-data
aka: [カーブデータ, Curvedata]
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
  - {kind: play, url: "https://puzz.link/rules.html?curvedata", best: true, note: "puzz.link: правила з картинками й плеєр (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/curvedata.js", note: "правила EN/JA, коди помилок, приклад"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/curvedata.js", note: "pzprjs: формат підказки-схеми, порівняння фігур, вкладений редактор"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти помилок shIncorrect / shMultiple / shNone .curvedata"}
  - {kind: other, url: "https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000LJL", note: "Logic Masters: «Nate H [Curve Data]» (wisty, 2025) — правила зі стінами"}
  - {kind: other, url: "https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000IA0", note: "Logic Masters: «9-1 (curve data)» (Aspartagcus, 2024) — правила із зафарбованими"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=curve+data+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 45
mechanics: [markup-validity, completion-detection, satisfy-constraints, conflict-highlight, path-drawing, path-cut, edge-marking, impassable-cells, undo-redo, in-game-editor, import-open-formats, +one-clue-per-region, +shape-identity-check, +edge-walls, +topological-shape-clue, +clue-sub-editor]
proposes: ["+cond:shape_match(figure, clue)", "+cond:region_has(figure, clue, n)", "+effect:draw", "+window:clue-sub-editor", "+card:topological-shape-clue", "+card:clue-sub-editor"]
author: opus
date: 2026-11-09
---

# Curve Data — розбий поле на фігури з ліній, кожна з яких топологічно повторює свою мініатюру-підказку

## Суть
Гравець проводить лінії між центрами клітинок і так утворює кілька окремих фігур. Кожна фігура проходить рівно через одну клітинку-підказку, а в підказці намальовано схему фігури: де кінці, кути, розгалуження. Збігатись мусить «скелет» (порядок і напрям вузлів), а не розміри: кожен прямий відрізок можна видовжити чи вкоротити до довжини ≥ 1; повертати чи дзеркалити схему не можна. Усі незафарбовані клітинки мають бути зайняті якоюсь фігурою.

## Поле і час
- Прямокутна сітка; можуть бути зафарбовані клітинки (ліній нема) і жирні межі-стіни (лінія не перетинає).
- Лінії — ортогональні сегменти між центрами сусідніх клітинок; фігура = звʼязна компонента сегментів (можуть бути кінці, кути, Т- і Х-вузли).
- Підказка — маленький малюнок усередині клітинки: сітка вузлів, зʼєднаних відрізками.
- Шари: стіни, зафарбовані клітинки, підказки (незмінні) · сегменти й хрестики гравця.
- Час статичний; хід = провести / стерти сегмент.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | terrain | — | крізь неї мусить пройти лінія якоїсь фігури |
| Зафарбована клітинка | static | — | ліній нема; сусідні ребра заборонені |
| Жирна межа | static | ребро | лінія через неї не проходить |
| Підказка-схема | mark | малюнок: вузли й відрізки | фігура через цю клітинку має той самий скелет, без поворотів і дзеркал |
| Порожня підказка | mark | — | у pzprjs: фігура з нею не перевіряється на форму (?) |
| Фігура | zone | кінці, кути, розгалуження | звʼязні сегменти; рівно одна підказка |
| Вузол фігури | mark | кінець / кут / Т / Х | визначає скелет; прямі проходи вузлами не є |
| Сегмент | mark | ребро між центрами | частина фігури |
| Хрестик | mark | ребро | нотатка «тут лінії нема» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells)` → ТО `custom: «намалювати сегменти вздовж шляху»` (+effect:draw); повторний drag по лінії стирає (?).
- КОЛИ `input(right_drag, edge)` → ТО `mark(edge, cross)`; клік без руху по порожньому ребру — теж хрестик.
- КОЛИ `input(drag, edge)` → ЯКЩО `custom: «ребро — жирна межа або торкається зафарбованої клітинки»` → ТО `block`.
- КОЛИ `input(click, cell)` → ЯКЩО `mode(edit)` → ТО `window(custom-window)` — вкладений редактор схеми; результат → `set_value(cell, shape)`.
- КОЛИ `input(copy_answer, cell)` → ЯКЩО `mode(edit)` → ТО `custom: «скопіювати намальовану фігуру під курсором у підказку»`.
- КОЛИ `constraint_broken(multiple_clues)` → ЯКЩО `custom: «фігура проходить через дві або більше підказок»` → ТО `message(«A shape is connected to multiple clues»)` · `flash(figure)` — shMultiple.
- КОЛИ `constraint_broken(shape)` → ЯКЩО `not custom: «скелет фігури збігається зі схемою: ті самі вузли в тому самому порядку праворуч і донизу; довжини прямих не важливі»` → ТО `message(«A shape does not match the clue»)` · `flash(figure)` — shIncorrect.
- КОЛИ `constraint_broken(no_clue)` → ЯКЩО `custom: «фігура без жодної підказки»` → ТО `message(«A shape is not connected to a clue»)` · `flash(figure)` — shNone.
- КОЛИ `constraint_broken(no_line)` → ЯКЩО `not cover_all(figure)` → ТО `message(«клітинка без лінії»)` · `flash(cell)` — ceNoLine.
- КОЛИ `all_constraints_met` → ТО `win`.
- Порядок перевірок у pzprjs: shMultiple → shIncorrect → shNone → ceNoLine.
- Перемога: кожна незафарбована клітинка в одній фігурі, кожна фігура з однією підказкою і її скелетом. Поразки й рахунку нема.
- Дедукція «тупик»: клітинка, з якої лінія може вийти лише в одному напрямку (кут поля, стіни), — кінець фігури; до неї підходить лише схема з кінцями.
- Дедукція «пряма»: схема-відрізок дає фігуру-пряму будь-якої довжини ≥ 1 у заданому напрямку (горизонталь чи вертикаль).
- Дедукція «лічба вузлів»: кількість кінців, кутів і розгалужень фігури задана схемою; клітинка, що дала б фігурі зайвий кут, мусить бути прямим проходом або належати іншій фігурі.

## Керування і ввід
- puzz.link (play): лівий drag — лінія; правий drag або клік по ребру — хрестик; режим info-line підсвічує фігуру (?).
- puzz.link (edit): стіни, зафарбовані клітинки, підказки; клік по клітинці відкриває вкладений редактор схеми (там свої режими: line — малювати, slide — зсунути всю схему на клітинку); copy-answer копіює намальовану фігуру в підказку; move-clue переносить підказку.
- Папір: лінії олівцем; схема в клітинці надрукована дрібно.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка, стіни, зафарбовані клітинки, мініатюри-схеми в клітинках, лінії; `check-button`, `undo-button`, `redo-button`; `conflict-highlight` — фігура з помилкою.
- `custom-window` — вкладений редактор схеми (окремий мініпазл curvedata-aux у плеєрі), відкривається з редактора (`+window:clue-sub-editor`).
- `editor-window` (puzz.link edit) — розмір, стіни, зафарбовані, підказки, експорт у URL.
- `help-window` — правила (puzz.link, Logic Masters).
- Переходи: `editor-window` → клік по клітинці → редактор схеми → повернення з готовою підказкою.

## Фічі поза полем
- `auto-check` за кнопкою; `undo` / `redo`.
- `level-editor` з вкладеним редактором підказки і «скопіювати відповідь у підказку»; `share-code` (URL; схеми кодуються бітами напрямків у рядку).
- Банк пазлів — авторські пазли на Logic Masters (теги «path puzzle»); окремого банку не знайшов.

## Варіації й родичі
- Різні автори формулюють довжини по-різному: «кожен відрізок можна видовжити чи вкоротити, ≥ 1» (wisty) або «схема не показує довжин» (Aspartagcus); стіни і зафарбовані клітинки — опційні.
- У корпусі: фігури за заданою формою — [Statue Park](statue-park.md), [Double Choco](double-choco.md), [Tachiawase Block](tachiawase-block.md); лінії через центри — [Masyu](masyu.md), [Country Road](country-road.md); розбиття поля на області з однією підказкою — [Fillomino](fillomino.md), [Shikaku](shikaku.md).
- **Осі варіацій**: що задає схема (точна форма з довжинами / скелет з орієнтацією / скелет без орієнтації) · покриття (усі клітинки / ні) · перешкоди (стіни / зафарбовані / нема) · замкненість (будь-яка фігура / лише петлі).

## Цікавинки для курсу
- Стиснення фігури до скелета: викинути прямі проходи, лишити кінці, кути, розгалуження — 📎.
- Порівняння двох скелетів як упорядкованих графів (перебір відповідностей у групах однакових вузлів; у pzprjs — алгоритм Хіпа) — 🥈.
- Мініатюра підказки, намальована в клітинці з масштабуванням під розмір схеми — 📎.
- Вкладений редактор підказки (мініполе в модалі) — 🥉.
- Перевірка покриття й «одна підказка на фігуру» через компоненти ліній — 🌱.
- Розвʼязувач — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `conflict-highlight` · `path-drawing`, `path-cut`, `edge-marking` ↔ ввід ліній · `impassable-cells` ↔ зафарбовані · `undo-redo` · `in-game-editor`, `import-open-formats`.
- **Нема** → пропозиції карток:
  - `+one-clue-per-region`, `+shape-identity-check`, `+edge-walls` — уже пропоновані в корпусі.
  - `+topological-shape-clue` «Підказка задає скелет фігури (вузли й напрямки), довжини гнучкі» · game-logic/constraints · 🥈.
  - `+clue-sub-editor` «Складна підказка редагується у вкладеному мініполі» · levels/editor · 🥉.

## Пропозиції до словників
- `+cond:shape_match(figure, clue)` — форма збігається зі схемою (повтор; тут — з точністю до довжин відрізків).
- `+cond:region_has(figure, clue, n)` — у фігурі рівно N підказок (повтор).
- `+effect:draw` — гравець малює сегмент лінії (повтор).
- `+window:clue-sub-editor` — модальний мініредактор для однієї складної підказки.
- `+card:topological-shape-clue`, `+card:clue-sub-editor` — див. мапу.

## Джерела
- ⭐ [puzz.link: Curve Data](https://puzz.link/rules.html?curvedata) — правила з картинками й плеєр (рендериться JS; текст узято з pzpr-samples).
- [puzz.link curvedata.js](https://puzz.link/js/pzpr-samples/curvedata.js) — правила EN (4 пункти: лінія в кожній клітинці, стіни, одна підказка, форма без поворотів, довжини ≥ 1) і JA; коди ceNoLine / shIncorrect / shNone / shMultiple.
- [pzprjs curvedata.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/curvedata.js) — схема як бітова сітка вузлів, порівняння ізоморфізмом, вкладений редактор, порядок перевірок.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.
- [Logic Masters: Nate H](https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000LJL) і [9-1](https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000IA0) — авторські пазли з двома формулюваннями правил.

## Непевне
- (?) Автор і перша публікація жанру: у pzpr-samples поле історії порожнє, японської сторінки правил не знайшов.
- (?) Тексту помилки ceNoLine для цього жанру не бачив — у `message` переказ.
- (?) «Порожня підказка» (qnum −2) знайдена лише в коді; у правилах її нема.
- (?) Згадку про «Curvedoku» (судоку + curve data) бачив лише в пошуковій видачі, сторінку не відкривав.
- (?) Дедукції «тупик», «пряма», «лічба вузлів» — загальна логіка, не з джерела.
