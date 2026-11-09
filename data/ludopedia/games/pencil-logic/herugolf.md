---
title: Herugolf (Хелгольф)
slug: herugolf
aka: [ヘルゴルフ, Hell Golf, Хелгольф, Пекельний гольф]
family: pencil-logic
also: [push-slide]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: null
platforms: [paper, web]
links:
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/herugolf/", best: true, note: "Nikoli: 4 правила, Sample → Progressing → Solution"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Herugolf/index.htm", note: "Janko: правила з прикладом «останній удар не мусить бути 1», походження назви, банк пазлів 8×8…36×20"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/herugolf.js", note: "puzz.link: правила EN/JA, коди помилок, тести вводу (dispmove)"}
  - {kind: play, url: "https://puzz.link/rules.html?herugolf", note: "puzz.link: сторінка правил і вхід у редактор/плеєр"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=herugolf+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [path-drawing, path-cut, satisfy-constraints, markup-validity, completion-detection, conflict-highlight, all-on-targets, cell-click, keyboard-controls, in-game-editor, import-open-formats, level-bank, impassable-cells, +undo-redo, +decreasing-stroke-length, +no-stop-cells, +show-final-position]
proposes: ["+cond:stroke_length", "+cond:path_clear", "+effect:draw", "+effect:cut_path", "+role:line", "+card:decreasing-stroke-length", "+card:no-stop-cells", "+card:show-final-position"]
author: opus
date: 2026-11-09
---

# Herugolf — заведи кожен мʼяч у лунку ударами, кожен з яких на клітинку коротший за попередній

## Суть
На сітці стоять мʼячі з числами, лунки H і сірі клітинки-водойми. Гравець малює для кожного мʼяча траєкторію з прямих відрізків-ударів: перший удар — рівно стільки клітинок, скільки на мʼячі, кожен наступний — на одну менше, напрямок між ударами можна міняти. Мʼяч має зупинитись точно в лунці; у кожній лунці — рівно один мʼяч. Незвичне: «фізика гри в гольф» стає статичним пазлом-розміткою — рух не симулюється, а записується лінією, і перевіряються довжини відрізків, зупинки й перетини.

## Поле і час
- Прямокутна сітка; клітинка — порожня, мʼяч (кружок з числом), лунка H, вода (сіра).
- Удар — пряма по ортогоналі через центри клітинок; між ударами — точка зупинки (поворот можливий).
- Межа поля — непрохідна: удар не може вилетіти за край (Nikoli; японський текст puzz.link — «OB»).
- Шари: тип клітинки (незмінний) · лінії-стрілки гравця · похідне: де стоїть кожен мʼяч після останнього удару.
- Час статичний; хід = провести або стерти відрізок лінії.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мʼяч | object | N — довжина першого удару | траєкторія з ударів N, N−1, N−2…; зупиняється, щойно лічильник = 0 або потрапив у лунку; мʼяч з 0 не рухається (Janko, JA-правила) |
| Лунка H | static | — | кінцева точка; приймає рівно один мʼяч; через неї не можна прокотитись |
| Вода (water hazard) | terrain | — | над нею можна пролетіти, зупинитись — ні |
| Порожня клітинка | terrain | — | прохідна; кожну клітинку лінія перетинає не більше одного разу |
| Траєкторія (стрілка) | mark | відрізки довжин N…k | малює гравець; не перетинає й не накладається на іншу лінію чи саму себе; не проходить через інший мʼяч чи лунку |
| Межа поля | static | — | удар не може її перетнути |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, ball → cell)` → ЯКЩО `custom: «пряма по ортогоналі»` → ТО `custom: «намалювати відрізок-удар»` (`+effect:draw`).
- КОЛИ `input(right_drag, line)` → ТО `custom: «стерти відрізок»` (`+effect:cut_path`; puzz.link — права кнопка).
- КОЛИ `custom: «удар номер k мʼяча N»` → ЯКЩО `custom: «довжина ≠ N − k + 1»` → ТО `constraint_broken(stroke_length)` (puzz.link `laLenNe`).
- КОЛИ `custom: «удар закінчився»` → ЯКЩО `cell(stop, water)` → ТО `constraint_broken(stop_on_water)` (`laWaterHazard`).
- КОЛИ `custom: «удар проходить клітинку»` → ЯКЩО `occupied(cell, ball)` → ТО `constraint_broken(over_ball)` (`laOnNum`).
- КОЛИ `custom: «удар проходить клітинку»` → ЯКЩО `cell(x, hole)` and `custom: «удар там не закінчується»` → ТО `constraint_broken(over_hole)` (`laOnHole`).
- КОЛИ `custom: «дві лінії в одній клітинці»` → ТО `constraint_broken(cross)` (`lnCross`, `lnBranch`).
- КОЛИ `edge(ball)` → ТО `block`: удар не може вийти за поле.
- КОЛИ `enter(ball, hole)` → ТО `set_state(ball, holed)`: далі мʼяч не рухається (Janko, JA).
- КОЛИ `custom: «лічильник удару = 0»` → ЯКЩО `not cell(stop, hole)` → ТО `constraint_broken(ball_not_in_hole)` (`nmOutOfHole`).
- КОЛИ `custom: «дві траєкторії зʼєднані»` → ТО `constraint_broken(balls_connected)` (`nmConnected`) (?).
- КОЛИ `custom: «лінія з повороту посеред удару»` → ТО `constraint_broken(curve)` (`laCurve`) (?).
- КОЛИ `custom: «у лунці 0 або ≥2 мʼячі»` → ТО `constraint_broken(hole_count)`.
- КОЛИ `all_on(ball, hole)` and `all_constraints_met` → ТО `win`.
- Останній удар не мусить мати довжину 1: мʼяч з 3 може влучити ударом 2 (Janko).
- Перемога: усі мʼячі в різних лунках, довжини правильні, нема зупинок на воді й перетинів. Поразки й рахунку нема.

## Керування і ввід
- puzz.link: drag лівою від мʼяча — малює лінію по клітинках; права кнопка / drag правою — стирає; перемикач edit/play: у режимі редактора клавіатурою ставляться числа, лунки й тип клітинки, курсор — стрілками.
- Налаштування `dispmove` у puzz.link: показувати мʼяч у кінці траєкторії замість стартової клітинки (?) — змінює лише рендер.
- Папір (Nikoli): стрілка від мʼяча до лунки з кутами на зупинках.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка, мʼячі-кружки з числами, H, сірі водойми, лінії-стрілки; кнопки `check-button`, `undo-button`, `redo-button`; `conflict-highlight` — порушене виділяється після перевірки (?).
- `settings-window` (puzz.link): `dispmove` та загальні параметри відображення (?).
- `editor-window` (puzz.link edit mode): розмір поля, числа, лунки, вода; експорт у URL.
- `help-window` — сторінка правил (Nikoli, puzz.link, Janko).
- `puzzle-select` (Janko): банк за розмірами й складністю.
- Переходи: puzz.link rules → URL пазла → game-screen → Check → «Complete!» (?).

## Фічі поза полем
- `auto-check` за кнопкою: перший знайдений код помилки (puzz.link).
- `undo`/`redo` (puzz.link) (?).
- `level-editor` + `share-code` — пазл як URL puzz.link.
- `puzzle-bank` (Janko: поля від 8×8 до 36×20, кілька рівнів складності).

## Варіації й родичі
- Родичі за типом лінії: Yosenabe, Bonsan, Rectslider (Janko групує їх разом) — теж «рух предмета, записаний лінією»; Yajisan-Sokoban — інший жанр «руху на папері» в puzz.link.
- Line-пазли сімʼї: [masyu](masyu.md), [slitherlink](slitherlink.md) — петля; тут — дерево з незалежних шляхів. [Icebarn](icebarn.md) — теж напрямки руху лінією.
- Цифрові «гольф» і ковзання з `push-slide` (Inertia-подібні): там рух симулюється, тут — пишеться заздалегідь.
- **Осі варіацій**: закон довжин (спадає на 1 / стала / задана послідовність) · що заборонено для зупинки (вода, пісок) · через що не можна летіти (мʼячі, лунки, лінії) · одна лунка — один мʼяч чи кілька.

## Цікавинки для курсу
- Перевірка траєкторії: розбити лінію на відрізки, порівняти довжини з N, N−1… — 📎.
- Заборона зупинки на воді при дозволеному прольоті — 🌱: два різні предикати «пройти» й «зупинитись».
- Досяжні лунки мʼяча: DFS по деревах ударів з довжинами, що спадають, і забороною самоперетину — 🥉.
- Розвʼязувач: вибір траєкторії для кожного мʼяча без перетинів + паросполучення мʼяч–лунка — 🥇.
- Рендер «мʼяч у кінці лінії» (dispmove) — 🌱; фігура мʼяча як стан, а не клітинка.
- Генератор з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `path-drawing` ↔ траєкторії drag-ом · `path-cut` ↔ стирання · `all-on-targets` ↔ кожен мʼяч у лунці · `markup-validity`, `conflict-highlight`, `completion-detection`, `satisfy-constraints` · `impassable-cells` ↔ межа й лунки для прольоту · `in-game-editor`, `import-open-formats` ↔ puzz.link URL · `level-bank` ↔ Janko.
- **Нема** → пропозиції карток:
  - `+decreasing-stroke-length` «Удари, що коротшають на 1» · game-logic/constraints · 📎 · слот {start, step}.
  - `+no-stop-cells` «Клітинки, через які можна пройти, але не зупинитись» · entities/legality · 🌱.
  - `+show-final-position` «Рендер обʼєкта в кінці траєкторії» · interface/render · 🌱.

## Пропозиції до словників
- `+cond:stroke_length` — довжина k-го відрізка лінії дорівнює формулі (N − k + 1).
- `+cond:path_clear` — відрізок не проходить через заборонені клітинки (мʼячі, лунки, інші лінії); повтор із корпусу.
- `+effect:draw` — гравець малює відрізок лінії (повтор із корпусу, для правила трьох).
- `+effect:cut_path` — стерти відрізок / хвіст лінії (повтор).
- `+role:line` — траєкторія як сутність із порядком відрізків (повтор із sudoku-variants).
- `+card:decreasing-stroke-length`, `+card:no-stop-cells`, `+card:show-final-position` — див. мапу.

## Джерела
- ⭐ [Nikoli: Herugolf](https://www.nikoli.co.jp/en/puzzles/herugolf/) — 4 правила: кожен мʼяч у H, одна H — один мʼяч; стрілки не перетинають мʼячі, H і одна одну; перший удар = число, далі на 1 коротше; не за поле, не зупинятись у воді.
- [Janko: Herugolf](https://www.janko.at/Raetsel/Herugolf/index.htm) — «останній удар не мусить бути 1», мʼяч з 0 чи в лунці не рухається, назва = «hell golf», автор і перша публікація невідомі; банк 8×8…36×20.
- [puzz.link herugolf.js](https://puzz.link/js/pzpr-samples/herugolf.js) — EN/JA-правила, коди `brNoLine lnBranch lnCross nmConnected laOnNum laOnHole laCurve laMoveOver laLenNe laWaterHazard nmOutOfHole nmIgnored`, тести миші й `setconfig,dispmove`.
- [puzz.link rules](https://puzz.link/rules.html?herugolf) — сторінка рендериться JS, текст через WebFetch не дістався.
- YouTube: пошук «herugolf puzzle».

## Непевне
- (?) Рік і місце першої публікації: Janko — «невідомо, можливо Puzzle Communication Nikoli»; Nikoli дати не дає.
- (?) Значення кодів `nmConnected`, `laCurve`, `laMoveOver`, `nmIgnored` — виведені з назв (траєкторії злиті, поворот посеред удару, удар задовгий, мʼяч без лінії).
- (?) Що саме робить `dispmove` у puzz.link — з назви й тестів; undo/redo і «Complete!» — загальна поведінка pzpr, не перевірена саме для Herugolf.
- (?) Чи лінія не може перетинати *стартову* клітинку іншого мʼяча, якщо той уже поїхав, — EN-текст puzz.link каже «any ball's starting point», тобто ні.
