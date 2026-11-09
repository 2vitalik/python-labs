---
title: One Room One Door (ワンルームワンドア)
slug: one-room-one-door
aka: [ワンルームワンドア, Wanrumuwandoa, Oneroom, «Одна кімната — одні двері»]
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
  - {kind: other, url: "https://www.janko.at/Raetsel/Wanrumuwandoa/index.htm", best: true, note: "Janko: правила EN/DE/JA, Nikoli № 169, 40 пазлів 6×6–17×17"}
  - {kind: other, url: "https://puzz.link/rules.html?oneroom", note: "puzz.link: правила з прикладом (рендер JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/oneroom.js", note: "правила EN/JA, Nikoli vol. 169, коди помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/heyawake.js", note: "код pzprjs: oneroom у файлі Heyawake — двері між парою кімнат, цілісність кімнати"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти помилок pzpr"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Nikoli/169.htm", note: "Janko: огляд Nikoli № 169, походження назви"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=one+room+one+door+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, connectivity-check, conflict-highlight, keyboard-controls, dot-mark, in-game-editor, import-open-formats, undo-redo, level-bank, +cell-shade-toggle, +no-adjacent-check, +global-connectivity, +region-quota, +irregular-regions, +input-scheme-toggle, +door-limit-per-region-pair, +region-internal-connectivity]
proposes: ["+cond:door_count(room_a, room_b)", "+card:door-limit-per-region-pair", "+card:region-internal-connectivity"]
author: opus
date: 2026-11-09
---

# One Room One Door — зафарбуй клітинки в кімнатах так, щоб між будь-якими двома кімнатами лишилось щонайбільше одні «двері»

## Суть
Поле поділене на кімнати, частина з числом — скільки в ній чорних клітинок. Гравець зафарбовує клітинки: чорні не торкаються сторонами, усі білі звʼязні, а білі кожної кімнати — одна суцільна область. «Двері» — дві білі клітинки, що сусідять через межу кімнат; між будь-якою парою кімнат таких дверей щонайбільше одні. Незвичне: обмеження накладено **на пару регіонів**, а не на регіон чи лінію.

## Поле і час
- Прямокутна сітка, поділена товстими межами на кімнати (у прикладі pzpr — прямокутні); Janko — 6×6…17×17.
- Сусідство ортогональне; «двері» — ребро межі кімнат з білими клітинками з обох боків.
- Шари: межі кімнат і числа (незмінні) · стан клітинки: невідома / чорна / крапка · допоміжні хрестики.
- Від Heyawake відрізняється відсутністю правила «білий ряд не тягнеться через три кімнати» (у pzpr `checkCountinuousUnshadeCell@!oneroom`).
- Час статичний; хід = зміна стану клітинки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кімната | zone | число N або без числа | рівно N чорних; білі в ній — одна область або нуль білих |
| Число кімнати | static | N | квота чорних у кімнаті |
| Клітинка | mark | невідома / чорна / крапка | гравець перемикає стан |
| Чорна клітинка | mark | — | без чорних сусідів по сторонах |
| Межа кімнат | static | ребро сітки | спільні ребра пари кімнат — кандидати на двері |
| Двері | mark | пара білих через межу | між двома кімнатами ≤ 1 |
| Біла область | zone | — | одна 4-звʼязна компонента на всьому полі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, shaded)`; права — `mark(cell, dot)`; режим `peke` — хрестик (схема `use` puzz.link) (?).
- КОЛИ `constraint_broken(no_shade)` → ЯКЩО `count(shaded, ==, 0)` → ТО помилка (`brNoShade`).
- КОЛИ `constraint_broken(adjacent)` → ЯКЩО `not no_adjacent(shaded)` → ТО `set_state(cells, error)` (`csAdjacent`).
- КОЛИ `constraint_broken(white_connected)` → ЯКЩО `not connected(white)` → ТО `set_state(board, error)` (`cuDivideRB`).
- КОЛИ `constraint_broken(room_whole)` → ЯКЩО `not connected(white in room)` → ТО `set_state(room, error)` (`bkSubdivided`: «A room is divided internally by shaded cells»).
- КОЛИ `constraint_broken(room_count)` → ЯКЩО `not count(shaded in room, ==, N)` → ТО `set_state(room, error)` (`bkShadeNe`).
- КОЛИ `constraint_broken(doors)` → ЯКЩО `custom: «між двома кімнатами більше однієї пари білих клітинок через межу»` (`+cond:door_count`) → ТО `set_state(doors, error)` (`bdDoorsGt`: «Two rooms have more than one door between them»).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «сусідні двері»: два сусідні ребра спільної межі не можуть обидва бути дверима — на одній із чотирьох клітинок мусить бути чорна.
- Дедукція «довга межа»: на межі довжини L між двома кімнатами щонайменше L − 1 пар мають хоча б одну чорну.
- Дедукція «чорна кімната»: кімната без білих можлива лише з однієї клітинки — дві чорні в ній торкнулися б.
- Дедукція «не розрізати кімнату»: чорна поперек вузької кімнати розділила б її білі — заборонено.
- Перемога: усі обмеження виконані. Поразки й рахунку нема.

## Керування і ввід
- Play (puzz.link): режими `shade`, `unshade`, `peke`, `info-blk` (підсвітити блок); схема кнопок `use`.
- Edit: протяжка по ребрах — межі кімнат; число — у верхню клітинку кімнати (`areanum`), цифри з клавіатури.
- Janko: інтерактивний розвʼязувач — сірі клітинки фарбуються чорним або білим.
- Папір: зафарбувати клітинку, крапкою — біла.

## Вікна, меню, HUD
- `game-screen`: сітка з товстими межами кімнат і числами, чорні, крапки, хрестики, `conflict-highlight` — усі зайві двері пари кімнат разом з їхніми клітинками, розрізана кімната, кімната з хибною кількістю.
- puzz.link — спільний інтерфейс ([puzz-link](puzz-link.md)): Check, Undo/Redo, Edit/Play, `help-window`, URL input/output, `settings-window`.
- `puzzle-select` — 40 пазлів Janko (за датою, розміром, складністю; пазли з простежуваним логічним шляхом виділено).
- Переходи: puzzle-select → game-screen → Check → помилка / розвʼязано.

## Фічі поза полем
- `auto-check` з кодами pzpr; `undo` / `redo`.
- `level-editor` + `share-code` (URL puzz.link).
- `puzzle-bank` Janko; генератора не бачив (?).

## Варіації й родичі
- [Heyawake](heyawake.md) — той самий каркас (кімнати, квоти, чорні не торкаються, білі звʼязні), але інше третє правило: білий ряд не через три кімнати; у pzpr — один файл `heyawake.js` разом з Ayeheya, Akichiwake, Sumiwake.
- [No Three](no-three.md), [Hitori](hitori.md), [Kuromasu](kuromasu.md) — той самий двигун «не торкаються + білі звʼязні».
- [Country Road](country-road.md), [Moon or Sun](moon-or-sun.md) — обмеження на перетини меж кімнат, але для петлі: вона заходить у кожну кімнату рівно раз.
- **Осі варіацій**: що обмежує кімнати (кількість дверей між парою / довжина білого ряду / симетрія) · чи мусить кімната лишатись цілою · квота чорних чи розмір білої області.

## Цікавинки для курсу
- Двері між парою кімнат: словник `(min_id, max_id) → список ребер`, лічильник білих пар (так у pzpr `getAllBorders`) — 📎.
- Модель кімнат з ребер (flood fill по товстих межах) — 📎.
- Звʼязність білих глобально й усередині кожної кімнати (BFS з межами-перегородками) — 🌱 + 📎.
- Повний валідатор із підсвіткою всіх дверей пари — 🥉; розвʼязувач — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `dot-mark` · `connectivity-check` ↔ білі · `conflict-highlight` · `keyboard-controls` · `in-game-editor`, `import-open-formats` · `undo-redo` · `level-bank` (Janko).
- Перевикористано: `+cell-shade-toggle`, `+no-adjacent-check`, `+global-connectivity`, `+region-quota`, `+irregular-regions` (Heyawake), `+input-scheme-toggle`.
- **Нема** → пропозиції карток:
  - `+door-limit-per-region-pair` «Між будь-якими двома регіонами ≤ K переходів» · game-logic/constraints · 📎 · слот {k: 1, door: white-white|line-crossing}.
  - `+region-internal-connectivity` «Позначені клітинки кожного регіону звʼязні всередині нього» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+cond:door_count(room_a, room_b)` — кількість пар білих клітинок через спільну межу двох регіонів.
- `+card:door-limit-per-region-pair`, `+card:region-internal-connectivity` — див. мапу.

## Джерела
- ⭐ [Janko: Wanrumuwandoa](https://www.janko.at/Raetsel/Wanrumuwandoa/index.htm) — правила EN/DE/JA, «If two white cells are orthogonally adjacent across region borders, this is called a 'door'», 40 пазлів.
- [puzz.link rules: oneroom](https://puzz.link/rules.html?oneroom) — правила з прикладом (рендер JS).
- [pzpr-samples oneroom.js](https://puzz.link/js/pzpr-samples/oneroom.js) — правила EN/JA («It's possible for a room to have no unshaded cells»), Nikoli vol. 169, коди `brNoShade`, `csAdjacent`, `cuDivideRB`, `bkShadeNe`, `bkSubdivided`, `bdDoorsGt`.
- [pzprjs heyawake.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/heyawake.js) — `checkRegionDivided`, `checkOneDoor`, `getAllBorders`, список перевірок.
- [failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.
- [Janko: Nikoli № 169](https://www.janko.at/Raetsel/Nikoli/169.htm) — назва як японська транслітерація «one room one door».

## Непевне
- (?) Рік: Nikoli vol. 169; за квартальним виходом (Janko: № 163 — червень 2018) ≈ грудень 2019 — дати не бачив; автора джерела не називають.
- (?) Чи бувають кімнати непрямокутні — у правилах заборони нема, у прикладі pzpr прямокутні.
- (?) Призначення кнопок миші в play-режимі puzz.link (схема `use`).
