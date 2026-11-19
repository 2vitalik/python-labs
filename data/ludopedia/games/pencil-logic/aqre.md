---
title: Aqre
slug: aqre
aka: [Ейкер]
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
year: 2020
platforms: [paper, web]
links:
  - {kind: other, url: "https://www.janko.at/Raetsel/Aqre/index.htm", best: true, note: "Janko: 4 правила DE/EN/JA з прикладом, 90 пазлів у браузері, автор Eric Fox, назва acre + Q, варіант Symmetric"}
  - {kind: official, url: "https://ericfox53.blogspot.com/2020/12/4-aqre.html", note: "блог автора, 16.12.2020: «Aqre is a genre I invented a few months ago», правила, пазл 9×9 на puzz.link"}
  - {kind: official, url: "https://ericfox53.blogspot.com/2021/07/300-my-original-genres.html", note: "автор про свої жанри: вимова «AY-kurr», правила Aqre"}
  - {kind: other, url: "https://ericfox53.blogspot.com/search/label/Aqre", note: "усі пости з пазлами Aqre, зокрема гібриди з Tapa й Kurotto"}
  - {kind: play, url: "https://puzz.link/rules.html?aqre", note: "puzz.link: правила EN/JA і вхід у плеєр/редактор (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/aqre.js", note: "3 правила EN, 4 JA, «invented by Eric Fox», приклад 6×6, тест-дошки з кодами помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/aqre.js", note: "код pzprjs: checklist, вікно з 4 клітинок, варіант aqre_borders"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Aqre+puzzle", note: "пошук"}
stage: v1
coverage: 70
mechanics: [cell-click, dot-mark, connectivity-check, satisfy-constraints, markup-validity, completion-detection, conflict-highlight, keyboard-controls, in-game-editor, editor-window, import-open-formats, undo-redo, help-window, level-bank, rule-variants, fixture-level-tests, level-solver, +cell-shade-toggle, +irregular-regions, +region-quota, +no-triple-run, +no-touch-across-border, +trial-mode]
proposes: ["+cond:run_length", "+cond:count_in", "+card:room-symmetry-check", "+card:no-touch-across-border"]
author: opus
date: 2026-11-19
---

# Aqre — зафарбуй клітинки за числами областей так, щоб чорні були одним шматком і ніде не стояло чотири однакові поспіль

## Суть
Сітку поділено на області, у частині з них стоїть число — скільки там чорних клітинок; в областях без числа — скільки завгодно. Гравець зафарбовує клітинки так, щоб усі чорні утворили одну ортогонально звʼязну групу, а в жодному рядку чи стовпці не стояло чотири клітинки одного кольору поспіль — ні чорних, ні білих. Незвичне: заборона довгих серій діє на **обидва кольори** (Janko називає це новизною жанру), тож біле поле теж обмежене, а не лише «стіна».

## Поле і час
- Квадратна сітка з довільними областями; у Janko — від 4×4 до 17×17, найбільше 10×10; приклад puzz.link — 6×6, пазл автора в блозі — 9×9.
- Число області пишеться в її лівій верхній клітинці; від 0 до площі рамки області.
- Сусідство ортогональне — і для звʼязності чорних, і для серій у рядках та стовпцях.
- Шари: межі й числа (умова) · стан клітинки гравця: невідомо / чорна / крапка «біле» · допоміжні хрестики.
- Час статичний; хід = змінити стан клітинки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Область | zone | довільне поліоміно | — |
| Число області | static | N ≥ 0 | в області рівно N чорних |
| Область без числа | zone | — | будь-яка кількість чорних |
| Клітинка | mark | невідомо / чорна / крапка | клік змінює стан |
| Чорна група | zone | кількість компонент | усі чорні — одна 4-звʼязна група |
| Серія | zone | 4 клітинки поспіль у рядку чи стовпці | не може бути одного кольору |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, shaded)`; повтор → `unmark(cell)` (схема puzz.link для зафарбовувань).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, dot)` — позначка «біле».
- КОЛИ `constraint_broken(black_divided)` → ЯКЩО `not connected(shaded)` → ТО `set_state(shaded_group, error)`, `message(«The shaded cells are divided.»)` (код csDivide).
- КОЛИ `constraint_broken(room_count)` → ЯКЩО `custom: «в області з числом N чорних не N»` (`+cond:count_in`) → ТО `set_state(region, error)`, `message(«The number of shaded cells in the room and the number written in the room is different.»)` (bkShadeNe).
- КОЛИ `pattern(line(4))` → ЯКЩО `custom: «4 чорні поспіль у рядку чи стовпці»` (`+cond:run_length`) → ТО `set_state(run, error)`, `message(«There are 4 or more shaded cells in a row.»)` (cs3).
- КОЛИ `pattern(line(4))` → ЯКЩО `custom: «4 не-чорні поспіль у рядку чи стовпці»` (`+cond:run_length`) → ТО `set_state(run, error)`, `message(«There are 4 or more unshaded cells in a row.»)` (cu3; ще не визначена клітинка теж лічиться білою).
- Варіант з межами: КОЛИ `constraint_broken(border)` → ЯКЩО `custom: «по обидва боки межі області однаковий колір»` (`+cond:touch_across_border`) → ТО `message(«Shaded cells are adjacent over a border.»)` або `message(«Unshaded cells are adjacent over a border.»)` (cbShade / cbUnshade): кожна межа торкається рівно однієї чорної.
- КОЛИ `all_constraints_met` → ТО `win`.
- Порядок перевірок puzz.link: межі (варіант) → звʼязність чорних → числа областей → 4 чорні → межі білих (варіант) → 4 білі → усі клітинки визначені (лише статус «не завершено»).
- Перемога: числа областей виконані, чорні — одна група, ніде 4 однакові поспіль. · Поразки й рахунку нема.
- Наслідки правил (дедукції): у будь-яких 4 сусідніх клітинках ряду є і чорна, і біла; три білі поспіль роблять чорними обидві клітинки на продовженні, три чорні — білими; область з «0» уся біла, тож її три білі в ряд одразу дають чорні на обох кінцях; чорна клітинка не може лишитися відрізаною білими від решти чорних.

## Керування і ввід
- puzz.link play: ліва кнопка з протяжкою — фарба, права — крапка «біле»; режими `shade` · `unshade` · `peke` (хрестики) · `info-blk` (підсвітити звʼязну чорну групу).
- puzz.link edit: межі областей — протяжкою по ребрах; число вводиться в область (клавіші або клік); режими `border` · `number` · `clear` · `info-blk`.
- Варіант з межами задається прапорцем пазла (у URL — `b`).
- Janko: інтерактивна сітка — клік фарбує сірі клітинки в чорний або білий.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка з темними лініями поверх чорних, товсті межі, числа в кутах областей, чорні, крапки (тлом), хрестики; кнопки Check · Undo · Redo · Erase answer · Erase marks · Trial (оболонка — [puzz.link](puzz-link.md)); `conflict-highlight` — 4 однакові поспіль, розірвані чорні, область з хибною кількістю.
- `editor-window` — той самий екран у режимі Edit, вивід URL, позначка варіанта.
- `help-window` — rules.html?aqre; Janko — сторінка правил з прикладом і розвʼязком.
- `puzzle-select` (Janko) — 90 пазлів, сортування за датою, розміром і складністю; розвʼязні логікою без вгадування виділено кольором.
- Переходи: Janko список → пазл → перевірка; puzz.link rules → плеєр за URL → Check → «розвʼязано» або перша помилка.

## Фічі поза полем
- `auto-check` і Check з текстом першої помилки; `undo` ∞ / `redo`; `+feature:trial-mode`; `info-blk` (puzz.link).
- `custom-rules` — прапорець `aqre_borders` («Borders must touch exactly one shaded cell»).
- `level-editor` + `share-code` (URL `p?aqre/9/9/…` — так автор публікує пазли), файли pzprv3.
- `puzzle-bank`: Janko — 90 пазлів; блог Eric Fox — пазли з міткою Aqre; puzz.link db.
- Нема генератора, підказок, рекордів.

## Варіації й родичі
- Symmetric (Janko) — чорні в кожній області симетричні відносно центру області.
- `aqre_borders` (puzz.link) — через кожну межу областей сусідять чорна й біла.
- Гібриди з блогу автора: Aqre-Tapa (пости №195, №345), Kurotto-Aqre (№242), Aqre (All or Nothing) (№480) — бачив лише назви.
- [Heyawake](heyawake.md) — числа в областях і звʼязність, але звʼязні білі, чорні не торкаються, а біла смуга не перетинає дві межі; Janko називає Heyawake найближчим.
- [Takuzu](takuzu.md), [Nondango](nondango.md), [Tawamurenga](tawamurenga.md) — заборона серій однакових (там довжина ≤ 2, тут ≤ 3).
- [Nurikabe](nurikabe.md), [LITS](lits.md), [Tapa](tapa.md) — «чорні — одна стіна»; [Yin-Yang](yin-yang.md) — звʼязні обидва кольори.
- **Осі варіацій**: найдовша серія (2 — Takuzu · 3 — Aqre) і для яких кольорів (обидва / лише чорні) · що звʼязне (чорні / білі / обидва) · що каже число області (кількість чорних / розмір білої області — Akichiwake) · межі (вільні / різнокольорові — `aqre_borders`) · симетрія всередині області.

## Цікавинки для курсу
- Серії: ковзне вікно з 4 клітинок по рядках і стовпцях, окремо для чорних і «не-чорних» — 🌱.
- Квота чорних в області з числом (області без числа — вільні) — 🌱.
- Звʼязність чорних: BFS чи union-find — 📎 (картка `connectivity-check`).
- Варіант як прапорець пазла: перевірка вмикається лише з ним, прапор їде в URL — 📎.
- Розвʼязувач: серії дають багато локальних виводів, звʼязність — глобальна; backtracking або SAT — 🥇.
- Генератор з унікальним розвʼязком — 👑.

## Мапа на каталог
- Є: `cell-click`, `dot-mark` ↔ фарба / крапка · `connectivity-check` ↔ чорні звʼязні · `satisfy-constraints`, `markup-validity`, `completion-detection`, `conflict-highlight` ↔ Check з кодами · `keyboard-controls`, `in-game-editor`, `editor-window`, `import-open-formats` ↔ редактор і URL · `undo-redo` · `help-window` · `level-bank` ↔ Janko · `rule-variants` ↔ `aqre_borders` · `fixture-level-tests` ↔ тест-дошки · `level-solver`.
- Перевикористано: `+cell-shade-toggle` · `+irregular-regions` · `+region-quota` (слот {n: число області, zones: numbered}) · `+no-triple-run` (слот {k: 4, colors: both}; та сама механіка, що `+no-three-in-row` у Tawamurenga) · `+no-touch-across-border` (слот colors: both — варіант; картку запропоновано в [Kuroclone](kuroclone.md)) · `+trial-mode`.
- **Нема** → нових карток понад повтори не треба; Symmetric Aqre — `+room-symmetry-check`, уже запропонована в Heyawake.

## Пропозиції до словників
- `+cond:run_length` — повтор: довжина серії одного кольору в рядку чи стовпці (тут 4 — помилка).
- `+cond:count_in` — повтор: кількість чорних в області.
- `+card:room-symmetry-check` — повтор (Heyawake): Symmetric Aqre.
- `+card:no-touch-across-border` — повтор із Kuroclone: варіант `aqre_borders` (colors: both).

## Джерела
- ⭐ [Janko: Aqre](https://www.janko.at/Raetsel/Aqre/index.htm) — правила («Stripes of adjacent cells of the same color may not span across more than 3 cells», «All black cells must form a single orthogonally-connected area»), 90 пазлів, автор Eric Fox (грудень 2020, блог), назва = acre + Q, варіант Symmetric, Heyawake як найближчий.
- [Eric Fox: #4 — Aqre](https://ericfox53.blogspot.com/2020/12/4-aqre.html) — «Aqre is a genre I invented a few months ago», три правила, «Solve online» на puzz.link.
- [Eric Fox: #300 — My Original Genres](https://ericfox53.blogspot.com/2021/07/300-my-original-genres.html) — вимова «AY-kurr», правила; Aqre серед оригінальних жанрів автора.
- [Eric Fox: мітка Aqre](https://ericfox53.blogspot.com/search/label/Aqre) — пости з пазлами й гібридами.
- [puzz.link: Aqre](https://puzz.link/rules.html?aqre) — правила й плеєр (рендериться JS).
- [pzpr-samples/aqre.js](https://puzz.link/js/pzpr-samples/aqre.js) — правила EN/JA (JA: «області без числа — будь-яка кількість»), «This genre was invented by Eric Fox», тести bkShadeNe · csDivide · cs3 · cu3.
- [pzprjs aqre.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/aqre.js) — checklist, `checkRun3`, `aqre_borders`, режими вводу.
- [pzprjs Config.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/puzzle/Config.js) — `aqre_borders`: «Borders must touch exactly one shaded cell».
- [Історія aqre.js](https://api.github.com/repos/robx/pzprjs/commits?path=src/variety/aqre.js) — «New puzzle type: Aqre», Robert Vollmert, 2020-10-26.
- YouTube: [пошук «Aqre puzzle»](https://www.youtube.com/results?search_query=Aqre+puzzle).

## Непевне
- (?) Перша публікація: Janko пише «грудень 2020, блог», але puzz.link додав жанр ще 2020-10-26, а автор 16.12.2020 каже «invented a few months ago» — отже, жанр жив до блогу (рік 2020 певний).
- (?) Походження назви (acre + улюблена літера автора Q) — лише Janko; автор у пості №300 дає тільки вимову.
- (?) Правила гібридів із блогу (Aqre-Tapa, Kurotto-Aqre, All or Nothing) не читав.
- (?) Що позначає хрестик `peke` у play (межу між клітинками?) — у тестах жанру вводу нема.
- (?) Де саме в інтерфейсі puzz.link вмикається варіант `aqre_borders` — у коді видно лише прапор `b` в URL і `variant: true` у Config.
