---
title: Compass (コンパス)
slug: compass
aka: [コンパス, Компас]
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
year: 2014
platforms: [paper, web]
links:
  - {kind: other, url: "https://puzz.link/rules.html?compass", best: true, note: "puzz.link: правила EN/JA і плеєр (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/compass.js", note: "puzz.link: текст правил EN/JA, тестові поля з кодами помилок, тести вводу"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/compass.js", note: "pzprjs: код перевірки checkDirectionSize; спільний файл з Mukkonn Enn"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "pzprjs: тексти помилок bkNumGe2/ceDirection .compass"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Compass/index.htm", note: "Janko: правила DE/EN/JA, Robert Vollmer, Puzzle GP 2014 R1, 50 пазлів 5×5–10×10, схеми підрахунку"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=compass+logic+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, edge-marking, cell-click, keyboard-controls, conflict-highlight, in-game-editor, import-open-formats, level-bank, undo-redo, +one-clue-per-region, +no-dead-end-border, +compass-clue]
proposes: ["+cond:count_in", "+cond:no_dead_end(borders)", "+ui:sector-clue-cell", "+card:compass-clue"]
author: opus
date: 2026-11-09
---

# Compass — розріж поле на області з одним компасом у кожній, де числа кажуть, скільки клітинок області лежить вище, нижче, лівіше й правіше

## Суть
Гравець проводить межі вздовж пунктирних ліній сітки й ділить поле на області. У кожній області — рівно один «компас»: клітинка з чотирма секторами ↑ → ↓ ←, у частині секторів стоять числа. Число в секторі — скільки клітинок своєї області лежить **далі в цьому напрямку**, ніж компас: для ↑ — усі клітинки області вище рядка компаса, а не лише на одній з ним вертикалі. Порожній сектор нічого не обмежує; область з однієї клітинки-компаса дозволена.

## Поле і час
- Прямокутна сітка з пунктирними лініями; компаси — у частині клітинок (дані пазла). Janko — 5×5…10×10; редактор pzprjs за замовчуванням 8×8.
- Шари: компаси з числами (незмінні) · межі гравця на ребрах · допоміжні лінії гравця «одна область» між центрами клітинок (режим `subline`).
- Область — звʼязна група клітинок, обмежена межами гравця й краєм поля; форма вільна.
- Час статичний; хід = поставити / зняти межу на ребрі.
- Janko: клітинки, які рахує сектор, не мусять бути суміжні з компасом і між собою.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | — | належить рівно одній області |
| Межа на ребрі | mark | є / нема | ставить гравець; не обривається всередині області |
| Допоміжна лінія | mark | — | «ці дві клітинки в одній області»; на перевірку не впливає (?) |
| Компас | static | 4 сектори ↑ → ↓ ← | рівно один на область; сам належить області |
| Число в секторі | static | n ≥ 0 або порожньо | клітинок області строго за компасом у напрямку сектора = n |
| Область | zone | клітинки | рівно один компас; будь-яка форма, хоч 1 клітинка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, edges)` → ТО `mark(edge, border)`; повторний drag по межі — `unmark(edge)` (play-режим `border`) (?).
- КОЛИ `input(drag, cells)` → ЯКЩО `custom: «увімкнено режим subline»` → ТО `mark(link, same_region)` — допоміжна лінія (?).
- КОЛИ `constraint_broken(no_compass)` → ЯКЩО `custom: «в області нема компаса»` → ТО `set_state(region, error)` (`bkNoNum`: «A block has no number»).
- КОЛИ `constraint_broken(direction)` → ЯКЩО `custom: «клітинок області за компасом у напрямку сектора ≠ n»` (`+cond:count_in`) → ТО `set_state(compass, error)` і підсвітити пораховані клітинки (`ceDirection`: «The number of cells in the direction is wrong»).
- КОЛИ `constraint_broken(two_compasses)` → ЯКЩО `custom: «в області два й більше компасів»` (`+cond:count_in`) → ТО `set_state(region, error)` (`bkNumGe2`: «There is an area with more than one clue»).
- КОЛИ `constraint_broken(border)` → ЯКЩО `custom: «межа обривається всередині області»` (`+cond:no_dead_end(borders)`) → ТО `set_state(edge, error)` (`bdDeadEnd`).
- КОЛИ `custom: «перевірка сектора»` → ЯКЩО `custom: «число в секторі не задане»` → ТО `custom: «сектор не перевіряється»` (Janko: «beliebig viele Felder»).
- Підрахунок ↑ у pzprjs: `custom: «клітинки обрамного прямокутника області з рядком < рядка компаса, відфільтровані за належністю до області»`; ↓ → ← — так само (півплощина, не промінь).
- КОЛИ `all_constraints_met` → ТО `win`.
- Порядок перевірки pzprjs: нема компаса → числа секторів → два компаси → обірвана межа.
- Дедукція «тотожність»: |область| = ↑ + ↓ + r = ← + → + c, де r і c — клітинки області в рядку й стовпці компаса (з ним самим); три відомі числа часто дають четверте.
- Дедукція «нуль»: ↑ = 0 — жодна клітинка області не вища за компас, тож межа йде над рядком компаса по всій ширині області.
- Дедукція «сусіди-компаси»: два компаси поруч — між ними межа; клітинка, яку не може «взяти» жоден компас без перевищення чисел, — суперечність.
- Перемога: усе поле розрізане, у кожній області один компас, усі задані сектори збігаються. Поразки й рахунку нема.

## Керування і ввід
- Папір: олівцем лінії по пунктиру між клітинками.
- puzz.link play: drag по ребрах — межа (режим `border`); режим `subline` — допоміжні лінії між центрами клітинок; кнопки миші й автодія `border` (код `autoplay_func`).
- puzz.link edit: курсор на клітинку, клавіша `q` ставить / прибирає компас; цифри пишуть у сектор; клік у частину клітинки обирає сектор (тест `mouse,leftx2,2.5,3` → `key,1` пише в один сектор) (?).
- Число сектора — від 0 до W·H (`minnum: 0`, `maxnum = cols × rows`).

## Вікна, меню, HUD
- `game-screen`: сітка з пунктиром, компаси з чотирма числами (`+ui:sector-clue-cell`), межі гравця, `conflict-highlight` — компас і клітинки, пораховані в секторі з помилкою.
- `editor-window` (puzz.link edit): компаси, числа секторів, розмір; експорт URL (зразок `5/5/l2.21g.2.4m.4.3g.1..l`).
- `help-window` — правила (puzz.link; Janko з двома схемами підрахунку).
- `puzzle-select` — Janko: 50 пазлів за датою, розміром, складністю.
- Решта — оболонка [puzz.link](puzz-link.md): Check, Undo/Redo, Trial, URL, таймер.

## Фічі поза полем
- `auto-check` за кнопкою з текстом першої помилки; `undo` / `redo`; trial-режим оболонки.
- `level-editor` + `share-code` (URL puzz.link); `export-import` (файл pzprv3).
- `+feature:board-transform` — поворот і відображення поля в редакторі переставляють числа секторів компаса (`adjustBoardData2`: FLIPX міняє ←/→, TURNR зсуває всі чотири).
- `puzzle-bank` — Janko 50 пазлів; генератора не бачив.

## Варіації й родичі
- **Mukkonn Enn** — у pzprjs той самий тип клітинки з чотирма числами, але жанр петлі: петля проходить усі клітинки, а число на боці — скільки клітинок вона йде прямо після виходу з цього боку (WPC 2017, індійська команда).
- Розбиття поля з однією підказкою на область: [Shikaku](shikaku.md) (число = площа прямокутника), [Fillomino](fillomino.md), [Palisade](palisade.md), [Double Choco](double-choco.md), [Ququ](ququ.md).
- Janko: в інших змаганнях є «Compass» з іншими правилами, що мало спільного мають з цим.
- **Осі варіацій**: що рахує сектор (півплощина / промінь / лише суміжні) · обовʼязкові всі сектори чи частина · форма областей (вільна / прямокутна) · чи можна область з одного компаса.

## Цікавинки для курсу
- Підрахунок сектора: обрамний прямокутник + фільтр за областю — 🌱, одна функція на чотири напрямки.
- Розбиття поля межами на компоненти (flood fill з барʼєрами на ребрах) — 🌱.
- Межа без тупиків (кожен кінець межі на краю чи в іншій межі) — 📎.
- Тотожність ↑ + ↓ + r = ← + → + c як автопідказка «четверте число» — 📎.
- Перестановка секторів при повороті / відображенні поля — 🌱, гарна вправа на напрямки.
- Розвʼязувач: присвоєння клітинок компасам зі звʼязністю й лічильниками секторів — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `edge-marking` ↔ межі по ребрах · `cell-click`, `keyboard-controls` (edit) · `conflict-highlight` · `in-game-editor`, `import-open-formats` (puzz.link) · `level-bank` (Janko) · `undo-redo`.
- Перевикористано: `+one-clue-per-region` (Ququ) — рівно один компас на область; `+no-dead-end-border` (Palisade).
- **Нема** → пропозиції карток:
  - `+compass-clue` «Підказка-компас: скільки клітинок своєї області за кожним напрямком» · game-logic/constraints · 📎 · слот {count: half-plane|ray|adjacent} — Compass, Mukkonn Enn (той самий тип клітинки).

## Пропозиції до словників
- `+cond:count_in` — повтор (Star Battle): кількість клітинок виду в зоні; тут зона — частина області за компасом у напрямку.
- `+cond:no_dead_end(borders)` — повтор (Palisade, Double Choco).
- `+ui:sector-clue-cell` — клітинка з кількома числами в секторах (компас; родич клітинки-підказки Kakuro).
- `+card:compass-clue` — див. мапу.

## Джерела
- ⭐ [puzz.link: Compass](https://puzz.link/rules.html?compass) — правила і плеєр; текст — у pzpr-samples.
- [pzpr-samples compass.js](https://puzz.link/js/pzpr-samples/compass.js) — «Each block contains exactly one cell with a compass», «further in the indicated direction than the compass itself»; JA: область лише з компаса дозволена; коди `bkNumGe2`, `bkNoNum`, `ceDirection`.
- [pzprjs compass.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/compass.js) — `checkDirectionSize` (прямокутник + фільтр), checklist, `inputnumber51`, `adjustBoardData2`, режими `border` / `subline`, спільний код з Mukkonn Enn.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.
- [Janko: Compass](https://www.janko.at/Raetsel/Compass/index.htm) — правила DE/EN/JA (JA-текст за фанзином «トケタ？»), Robert Vollmer, Puzzle Grand Prix 2014 R1, 50 пазлів, порожній сектор = без обмеження.

## Непевне
- (?) Автор і рік: Janko — «möglicherweise» Robert Vollmer, найстаріший відомий пазл — Puzzle GP 2014; `year: 2014` — за цим.
- (?) Як саме play-режим puzz.link ставить і знімає межу (drag / клік), і чи допоміжна лінія впливає на перевірку.
- (?) Вибір сектора в редакторі кліком у частину клітинки — висновок з тесту вводу, не з документації.
- (?) Як компас виглядає на екрані (коло з хрестом / чотири трикутники) — не бачив зображення.
