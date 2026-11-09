---
title: Mirror Block (Дзеркальні блоки, ミラーブロック)
slug: mirror-block
aka: [ミラーブロック, Mirā Burokku, mirrorbk, Дзеркальні блоки]
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
year: 2021
platforms: [paper, web]
links:
  - {kind: other, url: "https://puzz.link/rules.html?mirrorbk", best: true, note: "puzz.link: правила EN/JA і поле-приклад у браузері (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/mirrorbk.js", note: "puzz.link: правила EN/JA, історія (Nikoli vol. 177), приклад 6×6 з розвʼязком, коди помилок"}
  - {kind: play, url: "https://puzz.link/p?mirrorbk/6/6/g3h23g3n2l1l4i3g404000080083", note: "той самий приклад 6×6 — грати в браузері"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/cbblock.js", note: "pzprjs: код Mirror Block у спільному файлі з Combi Block, Double Choco, Nikoji — перевірка дзеркала, рендер подвійної лінії, режими вводу"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json", note: "pzprjs: тексти помилок bkMirror, bdUnused.mirrorbk, bkSizeNe, bkNumGe2"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=mirror+block+nikoli+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [satisfy-constraints, markup-validity, completion-detection, edge-marking, conflict-highlight, in-game-editor, undo-redo, import-open-formats, +mirror-across-border, +region-size-check, +one-clue-per-region, +given-border-must-divide]
proposes: ["+cond:mirror_symmetric", "+cond:separates", "+role:edge-clue", "+card:given-border-must-divide"]
author: opus
date: 2026-11-09
---

# Mirror Block — поділи сітку на блоки так, щоб два блоки обабіч кожного дзеркала були віддзеркаленнями один одного

## Суть
Сітка з числами в деяких клітинках і кількома даними ребрами-дзеркалами (подвійна лінія). Гравець малює межі по пунктирних лініях і ділить сітку на блоки: число — розмір блоку, у блоці не більше одного числа, блок без числа — будь-якого розміру. Дві клітинки обабіч дзеркала мусять бути в різних блоках, і ці два блоки — дзеркальні копії один одного відносно прямої, на якій лежить дзеркало. Незвичне: симетрія задана **між двома сусідніми блоками через дане ребро**, а ланцюг дзеркал переносить форму далі — блок між двома дзеркалами має копії з обох боків. Жанр з'явився в Puzzle Communication Nikoli vol. 177.

## Поле і час
- Прямокутна сітка; приклад puzz.link — 6×6, нове поле в редакторі pzprjs — 8×8; число в клітинці — до cols·rows (`maxnum`).
- Дзеркало — дане ребро між двома клітинками; колінеарні сусідні дзеркальні ребра малюються однією довгою лінією. Рендер — подвійна лінія: товста чорна смуга з білою серединою (`drawMirrorBase` + `drawMirrorSplit`).
- Вісь відбиття — пряма, що містить ребро-дзеркало: вертикальне ребро віддзеркалює зліва направо, горизонтальне — зверху вниз; жодна клітинка на осі не лежить.
- Дзеркало вже є межею (`isGround`), малювати по ньому гравцеві не дають (`isLineNG`); межі гравця — лише по пунктирних ребрах.
- Шари: числа й дзеркала (незмінні) · стан ребра: невідомо / межа / допоміжна позначка.
- Час статичний; хід = змінити стан одного ребра.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | порожня | належить рівно одному блоку |
| Клітинка з числом | static | N ≤ cols·rows | блок, що її містить, має рівно N клітинок |
| Дзеркало | static | ребро; вертикальне / горизонтальне | клітинки обабіч — у різних блоках; ці блоки — віддзеркалення один одного відносно прямої дзеркала |
| Ребро | mark | невідомо / межа / допоміжна лінія | межі ріжуть сітку на блоки |
| Блок | zone | розмір; 0 або 1 число | 4-звʼязна область між межами; без числа — довільного розміру |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, edge)` у Play → ТО `mark(edge, border)`; повтор → `unmark(edge)`; режим `subline` → `mark(edge, aux_line)` — позначка «межі тут нема» (?).
- КОЛИ `input(drag, edge)` в Edit → ТО `custom: «поставити / зняти дзеркало на ребрі»`; КОЛИ `input(click, cell)` в Edit → ТО `mark(cell, N)` (цифра з клавіатури або кліками).
- КОЛИ `constraint_broken(numbers)` → ЯКЩО `count(number_in_block, >, 1)` → ТО `message(bkNumGe2)` — «A block has multiple numbers».
- КОЛИ `constraint_broken(size)` → ЯКЩО `not region_size(block_with_N, N)` → ТО `message(bkSizeNe)` — «The size of the block is not equal to the number».
- КОЛИ `constraint_broken(mirror)` → ЯКЩО `custom: «блоки обабіч дзеркала різного розміру або хоч одна клітинка першого, віддзеркалена через вісь, не потрапляє в другий (чи виходить за поле)»` (`+cond:mirror_symmetric`) → ТО `message(bkMirror)` і `custom: «підсвітити обидва блоки»`.
- КОЛИ `constraint_broken(mirror)` → ЯКЩО `custom: «обидві клітинки обабіч дзеркала в одному блоці»` (`+cond:separates`) → ТО `message(bdUnused)` — «A mirror does not divide two regions».
- Порядок перевірок у pzprjs: кілька чисел → розмір → дзеркальність → невикористане дзеркало; кожне дзеркальне ребро перевіряється окремо.
- КОЛИ `all_constraints_met` → ТО `win`.
- Наслідки:
  - блок з числом N біля дзеркала → блок по той бік теж має N клітинок, навіть без числа; два блоки з різними числами через дзеркало не стикаються;
  - віддзеркалення не може вийти за поле: глибина блоку від дзеркала ≤ відстані від дзеркала до краю з іншого боку;
  - ланцюг: у прикладі puzz.link смужка 1×3 у пʼятому рядку має копії над собою й під собою через два горизонтальні дзеркала в різних стовпцях;
  - найменший випадок — дві одиночні клітинки по обидва боки дзеркала (у прикладі двічі).
- Перемога: усі блоки задовольняють числа, кожне дзеркало розділяє два дзеркальні блоки. Поразки й рахунку нема.

## Керування і ввід
- puzz.link Play (цифрова версія): протягування мишею по пунктирних лініях — межа (`autoplay_func: border`); режим `subline` — допоміжна лінія.
- puzz.link Edit: режим `number` — клік по клітинці й цифра (тест: права кнопка двічі по клітинці поля 2×2 дала 4), режим `border` — протягування по ребру ставить дзеркало.
- Папір (Nikoli): межі олівцем поверх пунктиру.

## Вікна, меню, HUD
- `game-screen` (puzz.link): пунктирна сітка, числа, подвійні лінії дзеркал, межі гравця; `conflict-highlight` — блоки з помилкою підсвічуються після Check.
- Кнопки: Check (текст першої помилки) · Undo · Redo · Erase answer · перемикач Edit / Play (див. [puzz-link](puzz-link.md)).
- `help-window` — `rules.html?mirrorbk`: правила й поле-приклад.
- `puzzle-select` (цифрова версія) — журнал Nikoli; на puzz.link пазли поширюються лінками.
- `end-screen` — повідомлення «розвʼязано» після Check (?).

## Фічі поза полем
- `undo`/`redo`, `auto-check` за кнопкою з кодом помилки.
- `level-editor` (Edit: числа й дзеркала) + `share-code` — пазл у URL `p?mirrorbk/<cols>/<rows>/<код>`; файл `pzprv3` з числами, вертикальними й горизонтальними ребрами (`export-import`).

## Варіації й родичі
- [hinge](hinge.md) — теж дзеркало через межу, але межі кімнат дані, а дзеркальні — зафарбовані блоки; тут межі малює гравець, а дзеркала дані.
- [double-choco](double-choco.md) — у тому самому коді pzprjs (`cbblock.js`): блок з двох конгруентних половин, де дозволено поворот; тут дві сусідні області й лише відбиття через конкретну вісь.
- [tentai-show](tentai-show.md) — центральна симетрія однієї області навколо точки; тут осьова між двома областями.
- [fillomino](fillomino.md), [shikaku](shikaku.md) — число = розмір області; тут ≤ 1 число на блок, порожні блоки довільні.
- Combi Block і Nikoji — сусіди в `cbblock.js`, не описані (?).
- **Осі варіацій**: що віддзеркалюється (два блоки / дві половини блоку / зафарбований блок сам собі) · звідки вісь (дане ребро / межа кімнати / точка) · дозволені перетворення (лише відбиття / поворот і відбиття).

## Цікавинки для курсу
- Перевірка пари блоків: рівні розміри і для кожної клітинки (x, y) першого — (2·bx − x, y) у другому — 🌱 (у pzprjs ~20 рядків).
- Повний чекер: flood-fill блоків за межами, числа, дзеркала, «невикористане дзеркало» — 📎.
- Рендер подвійної лінії зі «зшиванням» колінеарних сегментів — 🌱.
- Розвʼязувач з поширенням форм через ланцюги дзеркал — 🥇.
- Генератор: розбиття → пари блоків-віддзеркалень → дзеркала й мінімум чисел для єдиного розвʼязку — 🥇.

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` · `completion-detection` · `edge-marking` ↔ межі по ребрах · `conflict-highlight` · `in-game-editor` ↔ Edit · `undo-redo` · `import-open-formats` ↔ URL і `pzprv3`.
- Перевикористано: `+mirror-across-border` (Hinge) — тут слот {axis: given-edge}; `+region-size-check` (Fillomino); `+one-clue-per-region` (Ququ) — тут слот {max: 1, min: 0}.
- **Нема** → пропозиції карток:
  - `+given-border-must-divide` «Дане ребро мусить розділяти дві різні області» · game-logic/constraints · 🌱 — Mirror Block (`bdUnused`), за текстами pzprjs також Fillomino з даними межами й Tren.

## Пропозиції до словників
- `+cond:mirror_symmetric` — дві групи (або група сама собі) дзеркальні відносно осі (повтор з Hinge, Epaminondas).
- `+cond:separates` — дві клітинки обабіч ребра лежать у різних областях.
- `+role:edge-clue` — підказка на ребрі між двома клітинками (повтор з sudoku-line-dot-variants).
- `+card:given-border-must-divide` — див. мапу.

## Джерела
- ⭐ [puzz.link: Mirror Block rules](https://puzz.link/rules.html?mirrorbk) — правила й приклад у браузері (рендер JS; WebFetch бачить лише заголовок).
- [puzz.link mirrorbk.js](https://puzz.link/js/pzpr-samples/mirrorbk.js) — правила EN/JA (JA: «подвійна лінія — дзеркало; дві клітинки біля нього в різних блоках»), історія vol. 177, коди `bkSizeNe bkNumGe2 bdUnused bkMirror`, приклад 6×6 з розвʼязком (розкодовано: 16 блоків, 6 дзеркальних ребер, 8 блоків без числа).
- [puzz.link: приклад 6×6](https://puzz.link/p?mirrorbk/6/6/g3h23g3n2l1l4i3g404000080083) — грати.
- [pzprjs cbblock.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/cbblock.js) — `checkMirrorShape`, `checkMirrorUnused`, рендер дзеркала, режими Edit `number`/`border` і Play `border`/`subline`, `maxnum = cols·rows`.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json) — тексти помилок.
- [pzprjs variety.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/pzpr/variety.js) — `mirrorbk: ミラーブロック / Mirror Block`, клас `cbblock`.
- [JA Wikipedia: パズル通信ニコリ](https://ja.wikipedia.org/wiki/パズル通信ニコリ) — журнал квартальний, vol. 174 — весна 2021.
- YouTube: [пошук](https://www.youtube.com/results?search_query=mirror+block+nikoli+puzzle).

## Непевне
- (?) `year: 2021` — виведено: vol. 174 = весна 2021, квартальний вихід → vol. 177 ≈ зима 2021; дати номера джерело не дає.
- (?) Довге дзеркало з кількох ребер: правила кажуть «дзеркало розділяє два блоки», а код перевіряє кожне ребро окремо — чи можуть різні ребра однієї лінії розділяти різні пари блоків, не з'ясовано.
- (?) Обірвані межі всередині блоку: у списку перевірок mirrorbk нема перевірки глухих кінців — схоже, це не помилка.
- (?) Права кнопка в Play і точна поведінка `subline` — за загальною схемою pzpr, тестів у файлі нема.
- (?) Англійської сторінки Nikoli і Janko для жанру не знайшов; Combi Block, Nikoji, Mirroring Tile (`mrtile`) — назви бачив лише в коді pzprjs.
