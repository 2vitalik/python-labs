---
title: Country Road
slug: country-road
aka: [カントリーロード, Megurinku, メグリンク]
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
year: 1997
platforms: [paper, web]
links:
  - {kind: other, url: "https://puzz.link/rules.html?country", best: true, note: "puzz.link: сторінка правил і плеєр (рендериться JS)"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Country-Road/index.htm", note: "Janko: правила, автор Gesaku Desu Yo, PCN №65 (02.1997), стара назва, варіант Mebane, банк 270 пазлів"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/country.js", note: "puzz.link: правила EN/JA, «Nikoli vol. 65», коди помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "pzprjs: тексти bkPassTwice/bkLineNe/bkNoLine/cbNoLine .country"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=country+road+puzzle+nikoli", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, conflict-highlight, single-loop-check, path-drawing, path-cut, edge-marking, cell-click, keyboard-controls, undo-redo, in-game-editor, import-open-formats, level-bank, +irregular-regions, +region-quota, +region-visit-once, +unvisited-border-ban]
proposes: ["+cond:visits(loop, region, n)", "+trigger:pattern(loop_branch)", "+effect:draw", "+card:region-visit-once", "+card:unvisited-border-ban"]
author: opus
date: 2026-11-09
---

# Country Road — одна петля заходить у кожну країну рівно раз; число країни = скільки її клітинок пройшла петля

## Суть
Поле поділене товстими межами на «країни». Гравець малює одну замкнену петлю через центри клітинок, що заходить у кожну країну рівно один раз (увійшла — пройшла — вийшла). Число в країні каже, скільки клітинок цієї країни петля відвідала. Дві клітинки по різні боки межі країн не можуть обидві лишитись поза петлею — це правило не дає петлі «оминати» прикордоння.

## Поле і час
- Прямокутна сітка, розбита на неправильні області-країни (товсті межі задає автор).
- Петля йде по ортогоналі між центрами сусідніх клітинок; клітинка має степінь 0 (не відвідана) або 2; не мусить відвідати всі клітинки.
- Шари: межі країн і числа (незмінні) · сегменти петлі й хрестики гравця.
- Час статичний; хід = провести/стерти сегмент.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Країна | zone | клітинки, межа | петля входить і виходить рівно раз; не можна пропустити |
| Число | static | N | у країні N клітинок на петлі; без числа — будь-яка кількість ≥1 |
| Межа країни | static | — | через неї петля переходить; дві клітинки по боках не можуть обидві бути порожні |
| Сегмент петлі | mark | ребро між клітинками | частина єдиної петлі |
| Хрестик | mark | ребро / клітинка | допоміжне «тут петлі нема» |
| Петля | zone | довжина | одна, замкнена, без розгалужень і перетинів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells…)` → ТО `custom: «намалювати сегменти вздовж шляху»` (`+effect:draw`); drag по наявній лінії — стирає (?).
- КОЛИ `input(right_click, edge)` → ТО `mark(edge, cross)` (?).
- КОЛИ `custom: «клітинка з 3+ сегментами»` → ТО `constraint_broken(branch)` (`lnBranch`).
- КОЛИ `custom: «лінії перетинаються в клітинці»` → ТО `constraint_broken(cross)` (`lnCross`).
- КОЛИ `custom: «лінія обривається»` → ТО `constraint_broken(dead_end)` (`lnDeadEnd`).
- КОЛИ `custom: «на полі кілька петель»` → ЯКЩО `not single_loop` → ТО `constraint_broken(many_loops)` (`lnPlLoop`).
- КОЛИ `custom: «петля заходить у країну вдруге»` → ТО `constraint_broken(pass_twice)` (`bkPassTwice`; `+cond:visits`).
- КОЛИ `custom: «країну не відвідано»` → ТО `constraint_broken(no_line)` (`bkNoLine`).
- КОЛИ `custom: «перевірка числа країни»` → ЯКЩО `custom: «клітинок петлі в країні ≠ N»` → ТО `constraint_broken(count)` (`bkLineNe`).
- КОЛИ `custom: «дві сусідні клітинки різних країн»` → ЯКЩО `custom: «обидві поза петлею»` → ТО `constraint_broken(empty_border)` (`cbNoLine`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Перемога: одна петля, кожна країна рівно раз, числа виконані, прикордонних «дірок» нема. Поразки й рахунку нема.
- Дедукція: у країні з N=1 петля займає одну клітинку: входить і виходить через дві її сторони на межі країни; числова країна з N = розмір — петля проходить усі її клітинки; правило межі робить сусідів невідвіданої клітинки через межу обовʼязковими.

## Керування і ввід
- puzz.link (play): drag лівою по клітинках — малювати лінію; права кнопка — хрестик на ребрі / стирання (?).
- puzz.link (edit): межі країн малюються drag-ом по ребрах сітки, числа — з клавіатури (?).
- Папір: олівцем лінія через центри, хрестиками — закриті ребра.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка з товстими межами, числа, лінії, хрестики; `check-button`, `undo-button`, `redo-button`; `conflict-highlight` — порушену країну/лінію видно після перевірки (?).
- `editor-window` (puzz.link edit mode): межі, числа, розмір, експорт у URL.
- `help-window` — правила (puzz.link, Janko).
- `puzzle-select` (Janko): 270 пазлів за номером, розміром, складністю.
- Переходи: Janko список → пазл → game-screen → перевірка.

## Фічі поза полем
- `auto-check` за кнопкою (puzz.link); `undo`/`redo`.
- `level-editor` + `share-code` (URL puzz.link).
- `puzzle-bank` — Janko: 270 пазлів від 5×5 до 15×15.

## Варіації й родичі
- Варіант Palmer Mebane: «рівно раз» → «щонайменше раз»; сам автор пізніше назвав його помилкою (Janko). Ще варіант — петля не мусить пройти всі країни.
- У pzprjs той самий модуль обслуговує сусідні жанри з «кімнатами»: Moon or Sun, Onsen, Nothing тощо (видно з кодів `bkPassTwice.moonsun`, `cbNoLine.nothing`, `bkNoLine.onsen`).
- Петлі сімʼї: [masyu](masyu.md), [slitherlink](slitherlink.md), [yajilin](yajilin.md); кімнати з числами — [heyawake](heyawake.md).
- **Осі варіацій**: скільки разів у кімнату (рівно 1 / ≥1 / 0 або 1) · що рахує число (клітинки петлі / повороти) · обовʼязковість кімнат (усі / не всі) · правило порожнього прикордоння (є / нема).

## Цікавинки для курсу
- Лічба «входів у країну»: пройти петлю й рахувати переходи через межі — 📎.
- Перевірка порожнього прикордоння: для кожного ребра-межі обидві клітинки поза петлею → помилка — 🌱.
- Одна петля: степені 0/2 + одна компонента — 🥉 (повтор з Masyu).
- Розвʼязувач: порядок обходу країн як гамільтонів цикл на графі країн + розкладка всередині — 🥇.
- Генератор з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `single-loop-check` ↔ одна петля · `path-drawing`, `path-cut`, `edge-marking` ↔ ввід ліній · `markup-validity`, `conflict-highlight`, `completion-detection`, `satisfy-constraints` · `level-bank` ↔ Janko · `in-game-editor`, `import-open-formats` · `undo-redo`.
- **Нема** → пропозиції карток:
  - `+irregular-regions`, `+region-quota` — уже пропоновані в корпусі.
  - `+region-visit-once` «Шлях входить у кожну область рівно раз» · game-logic/constraints · 📎.
  - `+unvisited-border-ban` «Сусіди через межу не можуть обидва бути поза шляхом» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+cond:visits(loop, region, n)` — петля входить в область N разів.
- `+trigger:pattern(loop_branch)` — розгалуження лінії (повтор з Yajilin/Icebarn).
- `+effect:draw` — гравець малює сегмент лінії (повтор з Herugolf).
- `+card:region-visit-once`, `+card:unvisited-border-ban` — див. мапу.

## Джерела
- ⭐ [puzz.link: Country Road](https://puzz.link/rules.html?country) — правила й плеєр (рендериться JS).
- [Janko: Country Road](https://www.janko.at/Raetsel/Country-Road/index.htm) — 5 правил, автор Gesaku Desu Yo, PCN №65 (лютий 1997) під назвою メグリンク, варіант Mebane, 270 пазлів 5×5…15×15.
- [puzz.link country.js](https://puzz.link/js/pzpr-samples/country.js) — правила EN/JA, коди `lnBranch lnCross bkPassTwice bkLineNe bkNoLine cbNoLine lnDeadEnd lnPlLoop`.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок `.country` і сусідніх жанрів.
- YouTube: пошук «country road puzzle nikoli».

## Непевне
- (?) Японська назва カントリーロード — з памʼяті, у джерелах бачив лише メグリンク (стара назва).
- (?) `en.wikipedia.org/wiki/Country_Road_(puzzle)` перенаправляє на статтю про Nikoli — окремої статті нема.
- (?) Ввід (drag-стирання, хрестики, малювання меж у редакторі) — загальна поведінка pzpr, не перевірена саме для Country.
- (?) У failcode є `lnIsolate.country` «A circle doesn't have a line» — схоже, для іншого жанру того самого модуля; не перевіряв.
