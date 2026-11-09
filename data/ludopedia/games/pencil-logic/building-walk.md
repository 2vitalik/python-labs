---
title: Building Walk (ビルウォーク)
slug: building-walk
aka: [ビルウォーク, bdwalk, Прогулянка будинком]
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
  - {kind: other, url: "https://puzz.link/rules.html?bdwalk", best: true, note: "puzz.link: правила EN/JA і поле-приклад (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/bdwalk.js", note: "puzz.link: текст правил, історія (Nikoli vol.174), ~20 тестових полів з кодами помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/haisu.js", note: "pzprjs: код Building Walk у спільному файлі з Haisu і Kaisu — ліфти, обхід шляху зі станом поверху"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json", note: "pzprjs: тексти помилок bdw*"}
  - {kind: other, url: "https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000N6M", note: "Logic Masters: Sashigane Building Walk (yttrio, 2025) — правила ліфтів «на ≥ 1 поверх» словами"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/パズル通信ニコリ", note: "JA-Вікіпедія про журнал: №174 — весна 2021"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=building+walk+puzzle+nikoli", note: "пошук; розвʼязання"}
stage: v1
coverage: 55
mechanics: [path-drawing, path-cut, edge-marking, cell-click, keyboard-controls, markup-validity, completion-detection, satisfy-constraints, conflict-highlight, undo-redo, rule-variants, in-game-editor, import-open-formats, level-bank, level-solver, +must-visit-checkpoints, +crossing-detection, +start-goal-path, +path-floor-state]
proposes: ["+cond:crosses", "+cond:visited", "+card:path-floor-state", "+card:start-goal-path"]
author: opus
date: 2026-11-09
---

# Building Walk — проведи одну лінію від S до G крізь план багатоповерхового будинку: ліфти змінюють поверх, числа його перевіряють

## Суть
Сітка — вигляд згори на будинок. Гравець малює одну лінію від S до G, що проходить через усі числа й усі сірі клітинки-ліфти. Поверх лінії — прихований стан: ліфт зі стрілкою ▲ піднімає, ▼ опускає, ліфт без стрілки змінює поверх у будь-який бік; число n означає «тут лінія мусить бути на поверсі n». Незвичне: на папері лише 2D-шлях, а перевірка — **автомат зі станом уздовж шляху** (поверх), тобто третій вимір живе в голові розвʼязувача.

## Поле і час
- Прямокутна сітка (у коді pzprjs за замовчуванням 7×7; приклад puzz.link — 4×4); сусідство ортогональне.
- Шари: символи (S, G, ліфти, числа — незмінні) · відрізки лінії між центрами сусідніх клітинок · хрестики «тут лінії нема» на ребрах.
- Висота будинку = найбільше число на полі; поверхи 1…max. Варіант правил (`bdwalk_height`) знімає верхню межу.
- Поверх не намальований: його виводять, ідучи лінією від S до G (напрямок ▲/▼ читається саме в цьому напрямку).
- Час статичний; хід = додати/стерти відрізок лінії.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Старт S | static | клітинка | один кінець лінії; лінія не може пройти через S посередині |
| Фініш G | static | клітинка | другий кінець лінії |
| Ліфт ▲ | switch | сіра клітинка, стрілка вгору | лінія, проходячи, піднімається на ≥ 1 поверх |
| Ліфт ▼ | switch | сіра клітинка, стрілка вниз | лінія опускається на ≥ 1 поверх |
| Ліфт без стрілки | switch | сіра клітинка | поверх мусить змінитися (вгору чи вниз, ≥ 1) |
| Число n | static | 1…99 у редакторі | лінія проходить тут лише на поверсі n |
| Порожня клітинка | terrain | — | лінія може пройти або ні; поверх не змінюється |
| Лінія | mark | відрізки, поточний поверх | одна, без гілок і перетинів, від S до G |
| Хрестик на ребрі | mark | — | позначка гравця «тут лінії нема» (peke) |
| Будинок | zone | висота = max(n) | поверх лінії лишається в межах 1…max |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_drag, cells)` → ТО `custom: «намалювати відрізки лінії між центрами клітинок»`; drag назад по лінії — стерти хвіст (`path-cut`).
- КОЛИ `input(right_click, edge)` → ТО `mark(edge, cross)` (?).
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінія гілкується»` → ТО `message(lnBranch)`.
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінії перетинаються»` (`+cond:crosses`) → ТО `message(lnCross)`.
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінія проходить крізь S або G, а не закінчується в них»` → ТО `message(haisuSG)`.
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «на полі більше однієї лінії»` → ТО `custom: «помилка check: лінія не одна»` (`checkOneLine`).
- КОЛИ `constraint_broken(visit)` → ЯКЩО `custom: «число, ліфт, S чи G без лінії»` (`+cond:visited`) → ТО `message(lnIsolate)` («A symbol has no line»).
- Обхід: КОЛИ `enter(line, lift_up)` → ТО `counter(floor, +k)`, `custom: «k ≥ 1, будь-яке»`.
- КОЛИ `enter(line, lift_down)` → ТО `counter(floor, −k)`, k ≥ 1.
- КОЛИ `enter(line, lift_any)` → ТО `counter(floor, ±k)`, k ≥ 1 (поверх мусить змінитися).
- КОЛИ `enter(line, number_n)` → ЯКЩО `not counter(floor, ==, n)` → ТО `message(bdwMismatch)` («different numbers without switching floors»).
- КОЛИ `enter(line, lift_any)` → ЯКЩО `custom: «поверх до і після ліфта однаковий»` → ТО `message(bdwSkipElevator)`.
- КОЛИ `enter(line, lift_up)` → ЯКЩО `custom: «наступне число ≤ попереднього поверху»` → ТО `message(bdwInvalidDown)` («goes down at an upward elevator»); дзеркально для ▼ → `bdwInvalidUp`.
- КОЛИ `enter(line, lift_down)` → ЯКЩО `counter(floor, ==, 1)` → ТО `message(bdwGroundFloor)`; ▲ на верхньому поверсі → `message(bdwTopFloor)`.
- КОЛИ `level_start` → ЯКЩО `mode(any_height)` → ТО `custom: «верхньої межі поверху нема»` (код: висота = max(n) + rows·cols).
- КОЛИ `all_constraints_met` → ТО `win`.
- Механіка перевірки (pzprjs `walkLine`): стан поверху — не число, а інтервал: ANYWHERE (на старті) · SINGLE x (після числа) · ABOVE x / BELOW x (після ▲/▼, x — виключна межа) · EXCEPT x (після ліфта без стрілки). Кілька ▲ поспіль зсувають межу на +1 кожен.
- Дедукція «один ліфт між числами»: між n і m рівно один ▲ → m > n; ▲ між двома однаковими числами неможливий.
- Дедукція «ліфт без стрілки на краю»: на поверсі 1 він мусить вести вгору, на верхньому — вниз (коментар у коді: «unknown lift must go up»).
- Дедукція «ланцюг поверхів»: сусідні вздовж лінії числа без ліфта між ними мусять бути рівні — різні числа відрізають прямі коридори.
- Перемога: одна лінія S→G без гілок і перетинів, через усі символи, поверхи узгоджені з усіма числами й ліфтами. Поразки й рахунку нема.

## Керування і ввід
- puzz.link play mode: drag — лінія; режими вводу `line`, `peke` (хрестик на ребрі), `diraux` (допоміжні стрілки), `info-line` (підсвітити лінію).
- Edit mode: клік по клітинці — цикл «порожньо → ліфт → ▲ → ▼ → 1 → числа»; клавіші `s`/`g` ставлять старт/фініш, `u`/`d` — ліфт ▲/▼, цифри — число.
- Undo/redo, Check (перша помилка з кодом), Clear.
- Цифрова версія (тач): drag пальцем, тап по ребру — хрестик.

## Вікна, меню, HUD
- `game-screen`: сітка, сірі ліфти зі стрілками, числа, S/G, лінія + `conflict-highlight` (ділянка лінії між двома символами, що суперечать).
- Кнопки: Check, Undo, Redo, Clear answer.
- `settings-window` — перемикач варіанта «будь-яка висота» (`bdwalk_height`), налаштування вводу.
- `editor-window` — puzz.link edit mode: символи, S/G, розмір поля, експорт URL.
- `help-window` — правила (puzz.link rules).
- `puzzle-select` — банк пазлів (цифрова версія).
- `end-screen` — повідомлення «розвʼязано».
- Переходи: editor → game-screen → Check → помилка / end-screen.

## Фічі поза полем
- `auto-check` за кнопкою з кодом порушення; `undo` / `redo`.
- `custom-rules`: варіант вшитий у URL пазла — з прапорцем `m` висота = max(n) (так закодовано приклад puzz.link), без нього — будь-яка висота.
- `level-editor` + `share-code` (URL puzz.link).
- `puzzle-bank`: журнал Nikoli, puzz.link; поодинокі авторські гібриди на Logic Masters.

## Варіації й родичі
- **Sashigane Building Walk** (yttrio, Logic Masters, 2025) — гібрид: поле ще й ділиться на L-регіони Sashigane, кожен регіон (крім ліфтів) — на одному поверсі.
- **RGB Haisu Building Walk** (Logic Masters, 2025) — три кольорові лінії покривають усі клітинки, кожна стартує з поверху 1, поверхів 4 (?).
- Код: спільний файл pzprjs з Haisu і Kaisu — теж «шлях S→G через символи» (?, правила не перевіряв).
- Родичі в сімʼї: [Icebarn](icebarn.md) (шлях S→G з обовʼязковими клітинками), [Suraromu](suraromu.md) (шлях зі станом «скільки воріт пройдено»), [Nuri-Maze](nuri-maze.md), [Country Road](country-road.md).
- **Осі варіацій**: зміна на ліфті (рівно 1 / ≥ 1 / будь-яка ≠ 0) · межі будинку (1…max / необмежено) · стартовий поверх (вільний / 1) · кількість ліній (1 / кілька кольорів) · що задає поверх (числа / регіони).

## Цікавинки для курсу
- Модель лінії на ребрах: ступінь кожної клітинки 0/1/2, один компонент, кінці — S і G — 🌱.
- Обхід лінії від S і «автомат поверху» з інтервальним станом (ANYWHERE/SINGLE/ABOVE/BELOW/EXCEPT) — 📎: невеликий автомат над послідовністю символів, гарний приклад стану вздовж шляху.
- Підсвітити саме ту ділянку лінії між двома символами, де сталась суперечність, — 📎.
- Перемикач варіанта правил у URL пазла — 🌱.
- Розвʼязувач: DFS по шляху з відсіканням за інтервалом поверху й обовʼязковими клітинками — 🥇.
- Генератор з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `path-drawing`, `path-cut` ↔ лінія drag-ом · `edge-marking` ↔ хрестики на ребрах · `cell-click`, `keyboard-controls` ↔ редактор (s/g/u/d) · `markup-validity`, `completion-detection`, `satisfy-constraints`, `conflict-highlight` · `undo-redo` · `rule-variants` ↔ «будь-яка висота» · `in-game-editor`, `import-open-formats`, `level-bank`, `level-solver`.
- Перевикористано: `+must-visit-checkpoints` (Icebarn, Suraromu) ↔ усі числа й ліфти · `+crossing-detection` (Icebarn).
- **Нема** → пропозиції карток:
  - `+path-floor-state` «Шлях несе прихований стан, який змінюють спецклітинки й перевіряють клітинки-числа» · game-logic/constraints · 📎 · слоти {change: exact1|atleast1|any, bounds: 1..max|free, start: free|1}.
  - `+start-goal-path` «Одна лінія від S до G без гілок, кінці лише в S і G» · game-logic/constraints · 🌱 · слот {cover: all-cells|symbols}.

## Пропозиції до словників
- `+cond:crosses` — лінія перетинає іншу (повтор з Icebarn, Yajisan-Sokoban).
- `+cond:visited` — клітинку пройдено лінією (повтор з Icebarn).
- `+card:path-floor-state`, `+card:start-goal-path` — див. мапу.

## Джерела
- ⭐ [puzz.link: Building Walk](https://puzz.link/rules.html?bdwalk) — сторінка правил і приклад (текст рендериться JS).
- [puzz.link: bdwalk.js](https://puzz.link/js/pzpr-samples/bdwalk.js) — правила EN/JA, «first appeared in Puzzle Communication Nikoli vol. 174», тестові поля з кодами помилок.
- [pzprjs: haisu.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/haisu.js) — код: цикл вводу ліфтів, клавіші s/g/u/d, `walkLine` з інтервальним станом поверху, `bdwalk_height`.
- [pzprjs: failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json) — тексти `bdwGroundFloor`, `bdwTopFloor`, `bdwInvalidUp/Down`, `bdwMismatch`, `bdwSkipElevator`.
- [Logic Masters: Sashigane Building Walk](https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000N6M) — правила словами: ▲/▼ на ≥ 1 поверх, ліфт без стрілки — мусить змінити поверх.
- [JA-Вікіпедія: パズル通信ニコリ](https://ja.wikipedia.org/wiki/パズル通信ニコリ) — №174 — весна 2021.

## Непевне
- (?) Стартовий поверх: код pzprjs починає зі стану «будь-який», тобто S не мусить бути на 1-му поверсі; чи так у Nikoli — не перевірено.
- (?) Розкладка мишею в play mode (права кнопка — хрестик) — тести вводу у файлі порожні.
- (?) RGB Haisu Building Walk — лише сніпет результату пошуку, сторінку не відкривав.
- (?) Правила Haisu/Kaisu (спільний файл коду) не перевірені.
- (?) Рік 2021 — з датування №174 у JA-Вікіпедії; дату першої появи жанру Nikoli не називає.
