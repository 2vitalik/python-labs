---
title: Rectangle-Slider
slug: rectangle-slider
aka: [Rectslider, レクタングルスライダー]
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
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/rectslider.js", best: true, note: "puzz.link: правила EN/JP, історія (Nikoli vol. 145), коди помилок, тести вводу"}
  - {kind: other, url: "https://puzz.link/rules.html?rectslider", note: "puzz.link: сторінка правил (рендериться JS)"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json", note: "pzprjs: тексти помилок rectslider"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=rectangle+slider+puzzle+nikoli", note: "пошук; розвʼязання"}
stage: v1
coverage: 55
mechanics: [markup-validity, completion-detection, satisfy-constraints, path-drawing, cell-click, keyboard-controls, conflict-highlight, in-game-editor, undo-redo, +straight-move-line, +rect-shape-check, +crossing-detection]
proposes: ["+cond:is_rectangle", "+cond:crosses", "+cond:moved(a, n)", "+card:slide-to-assemble"]
author: opus
date: 2026-11-09
---

# Rectangle-Slider — зсунь частину панелей прямими лініями так, щоб вони склались у суцільні прямокутники

## Суть
На сітці розкидані зафарбовані панелі (клітинки), деякі з числами. Гравець малює лінії руху: панель їде по прямій горизонталі чи вертикалі, не повертаючи. Після всіх зсувів панелі мають утворити суцільні прямокутники чи квадрати, і кожна панель торкається стороною хоча б однієї іншої. Незвичне: розвʼязок — це план руху (як у Sokoban), записаний статичною розміткою на папері.

## Поле і час
- Прямокутна сітка; дані — зафарбовані панелі, частина з числами.
- Шари: панелі на стартових клітинках · лінії руху по центрах клітинок · кінцеві позиції панелей (кінець лінії).
- Час статичний: усі рухи «одночасні» в розвʼязку, перевіряється лише геометрія ліній і кінцевий стан.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | terrain | — | порожня, старт панелі, траса лінії або фініш |
| Панель | object | старт | стоїть або їде по прямій до кінця своєї лінії |
| Панель з числом | object | N | мусить зсунутись рівно на N клітинок |
| Лінія руху | mark | напрямок, довжина | пряма від панелі; без поворотів |
| Прямокутник | zone | W×H | звʼязна група кінцевих панелей, суцільний прямокутник |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells)` → ЯКЩО `occupied(start, panel)` → ТО `mark(cells, move_line)`; кінець лінії — нова позиція панелі.
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінія повертає»` → ТО `set_state(line, error)` («A line has curve»).
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінії перетинаються, накладаються або розгалужуються»` (`+cond:crosses`) → ТО `set_state(line, error)`.
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінія проходить через старт або фініш іншої панелі»` → ТО `set_state(line, error)` («A line goes through a shaded cell»).
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінія не починається з панелі»` → ТО `set_state(line, error)`.
- КОЛИ `constraint_broken(number)` → ЯКЩО `custom: «довжина лінії ≠ число панелі»` (`+cond:moved`) → ТО `set_state(panel, error)`.
- КОЛИ `constraint_broken(number)` → ЯКЩО `custom: «панель з числом не рухалась»` → ТО `set_state(panel, error)` («A shaded cell doesn't move»).
- КОЛИ `constraint_broken(adjacency)` → ЯКЩО `adjacent_count(panel, panel, eq, 0)` → ТО `set_state(panel, error)` («There is an isolated shaded cell»).
- КОЛИ `constraint_broken(shape)` → ЯКЩО `custom: «група панелей не суцільний прямокутник»` (`+cond:is_rectangle`) → ТО `set_state(group, error)`.
- КОЛИ `constraint_broken(board)` → ЯКЩО `custom: «на полі нема жодної лінії»` → ТО `custom: «пазл не розвʼязано»` («There is no line on the board»).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «число-радар»: панель з N може опинитись лише в 4 клітинках на відстані N — часто лише одна з них не порушує інших правил.
- Дедукція «вузький прохід»: лінії не перетинаються, тож панель, що проїхала коридором, перекриває його іншим.
- Перемога: кожна лінія пряма, не перетинає інших і чужих стартів/фінішів, числа збігаються, усі кінцеві панелі — суцільні прямокутники без одиночок. Поразки й рахунку нема.

## Керування і ввід
- puzz.link: drag лівою від панелі — лінія руху; права кнопка, подвійний/потрійний клік — інші мітки (тести `mouse,leftx2/x3`, `rightx2/x3`) (?).
- Edit mode: клік зафарбовує панель, курсор + цифри — число (`key,1,right,2…`); `-` — панель зі знаком «?» (?).
- Цифрова версія: undo/redo, перевірка за кнопкою.

## Вікна, меню, HUD
- `game-screen`: сітка, панелі з числами, лінії руху, кінцеві позиції, `conflict-highlight`.
- puzz.link: перемикач play/edit, кнопка перевірки, `settings-window`.
- `help-window` — правила жанру.

## Фічі поза полем
- `auto-check` за кнопкою (pzprjs).
- `undo` / `redo`; `level-editor` + `share-code` (URL пазла).

## Варіації й родичі
- У сімʼї: [Yajisan-Sokoban](yajisan-sokoban.md) (прямі лінії руху ящиків), [Herugolf](herugolf.md) (лінія-траєкторія з довжиною), [Shikaku](shikaku.md) (прямокутники), [Tren](tren.md) (рухомі блоки, число = свобода руху).
- Поза сімʼєю: [Rush Hour](../push-slide/rush-hour.md), [Klotski](../push-slide/klotski.md) — ті самі зсуви, але покроково й з ігровим часом.
- Bonsan (puzz.link) — схожі правила «коло не рухається» (код помилки nmNoMove.bonsan) (?).
- **Осі варіацій**: мета (прямокутники / одна фігура / задані області) · довжина руху (точна / вільна) · один крок на панель / кілька · перетин ліній (заборонено / дозволено).

## Цікавинки для курсу
- Модель «стартова позиція + пряма лінія → кінцева позиція» і перевірка без перетинів — 🌱.
- Перевірка «кожна компонента — суцільний прямокутник» (bbox = площа) — 🌱.
- Анімація розвʼязку: показати, як панелі їдуть по лініях — 📎.
- Розвʼязувач: перебір напрямків і довжин з відсіканням за перетином ліній — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints`, `conflict-highlight` · `path-drawing` ↔ лінії руху · `cell-click`, `keyboard-controls` · `in-game-editor`, `undo-redo`.
- **Нема** → пропозиції карток:
  - `+slide-to-assemble` «Зсунути панелі, щоб склалась задана форма» · game-logic/win · 📎 · слот {target: rectangles|shape}.
  - `+straight-move-line`, `+rect-shape-check`, `+crossing-detection` — повтори (Yajisan-Sokoban, Shikaku).

## Пропозиції до словників
- `+cond:is_rectangle`, `+cond:crosses` — повтори (Shikaku, Tracks).
- `+cond:moved(a, n)` — сутність зміщена від старту рівно/щонайменше на N.
- `+card:slide-to-assemble` — див. мапу.

## Джерела
- ⭐ [puzz.link: rectslider.js](https://puzz.link/js/pzpr-samples/rectslider.js) — 5 правил (пряма, без перетинів і чужих стартів/фінішів, число = відстань, сусідство, прямокутники), історія «Puzzle Communication Nikoli vol. 145», тести вводу.
- [pzprjs: failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json) — тексти помилок (isolated shaded cell, line goes through a shaded cell, shaded cell doesn't move).
- YouTube: пошук «rectangle slider puzzle nikoli».

## Непевне
- (?) Правило «торкається хоча б однієї іншої панелі» не каже, старт чи фініш; код помилки «isolated shaded cell» вказує на кінцевий стан.
- (?) Код `nmConnected` («There are connected shaded cells») — сенс не зрозумів: можливо, стартові панелі не можуть торкатися.
- (?) Чи панелі без числа можуть стояти на місці — правило «move some of the panels» дозволяє; числові мусять рухатись.
- (?) Рік випуску vol. 145 і автор жанру — не перевіряв (`year: null`).
- (?) Розкладка дій миші — з назв тестів.
