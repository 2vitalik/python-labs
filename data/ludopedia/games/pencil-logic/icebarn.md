---
title: Icebarn (アイスバーン)
slug: icebarn
aka: [Ice Barn, アイスバーン, Айсберн]
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
  - {kind: other, url: "https://puzz.link/rules.html?icebarn", best: true, note: "puzz.link: сторінка правил (рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/icebarn.js", note: "puzz.link: правила EN/JP, «Nikoli vol. 108», тести вводу, коди помилок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=icebarn+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, path-drawing, path-cut, one-way-cell, inertia-slide, in-game-editor, import-open-formats, undo-redo, +ice-straight-path, +must-visit-checkpoints, +crossing-detection]
proposes: ["+cond:turns", "+cond:crosses", "+cond:visited", "+trigger:pattern(loop_branch)", "+card:ice-straight-path", "+card:must-visit-checkpoints"]
author: opus
date: 2026-11-09
---

# Icebarn — проведи одну лінію від IN до OUT: на льоду не повертаєш, перетинатись можна лише на льоду

## Суть
На сітці є крижані клітинки (сусідні утворюють «айсберн» — каток) і стрілки на лініях сітки; дві стрілки на краю — вхід IN і вихід OUT. Гравець малює одну безперервну лінію від IN до OUT через центри клітинок, яка проходить через кожну стрілку в її напрямку. На льоду лінія не може повертати, зате лише там може перетинати сама себе під прямим кутом; кожен айсберн треба відвідати хоча б раз. Незвичне: правило «ковзання по льоду» з аркад (`push-slide`) перенесене в статичний пазл про шлях.

## Поле і час
- Прямокутна сітка; клітинки звичайні або крижані; група звʼязних крижаних — один айсберн.
- Стрілки лежать на межах між клітинками (у тестах редактора — drag уздовж межі) (?); IN і OUT — стрілки на рамці поля.
- Шари: тип клітинки й стрілки (незмінні) · лінія гравця (сегменти між центрами сусідніх клітинок) · мітки «тут нема лінії».
- Час статичний; хід = додати/стерти сегмент лінії.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Звичайна клітинка | terrain | — | лінія може пройти, повернути; перетин заборонено |
| Крижана клітинка | terrain | — | лінія йде лише прямо; перпендикулярний перетин дозволено |
| Айсберн | zone | звʼязна група льоду | має бути відвіданий лінією хоча б раз |
| Стрілка | static | напрямок | лінія мусить пройти через неї і лише в її напрямку |
| Стрілка IN | source | позиція на рамці | початок лінії |
| Стрілка OUT | sink | позиція на рамці | кінець лінії |
| Лінія | mark | сегменти | одна, без розгалужень; від IN до OUT |
| Мітка «нема лінії» | mark | — | хрестик гравця (права кнопка) (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_drag, cells)` → ТО `custom: «додати сегменти лінії між сусідніми центрами»`; повторний drag по наявному сегменту — стерти (pzpr) (?).
- КОЛИ `input(right_drag, cells)` → ТО `mark(edge, no_line)` (?).
- КОЛИ `pattern(loop_branch)` → ЯКЩО `custom: «з клітинки виходить 3+ сегменти, не прямий хрест»` → ТО конфлікт (puzz.link `lnBranch`).
- КОЛИ `constraint_broken(crossing)` → ЯКЩО `custom: «лінія перетинає себе»` (`+cond:crosses`) and `not cell(x, ice)` → ТО конфлікт (puzz.link `lnCrossExIce`).
- КОЛИ `constraint_broken(ice_turn)` → ЯКЩО `cell(x, ice)` and `custom: «лінія повертає в клітинці»` (`+cond:turns`) → ТО конфлікт (puzz.link `lnCurveOnIce`).
- КОЛИ `constraint_broken(arrow)` → ЯКЩО `not facing(line, arrow_dir)` → ТО конфлікт (puzz.link `lrReverse`).
- КОЛИ `constraint_broken(arrow)` → ЯКЩО `custom: «стрілку не пройдено»` (`+cond:visited`) → ТО конфлікт (puzz.link `arNoLine`).
- КОЛИ `constraint_broken(icebarn)` → ЯКЩО `not custom: «айсберн відвідано»` → ТО конфлікт (puzz.link `bkNoLine`).
- КОЛИ `edge(line)` → ЯКЩО `not occupied(edge, out_arrow)` → ТО конфлікт (лінія виходить за поле не через OUT; puzz.link `lrOffField`).
- КОЛИ `constraint_broken(path)` → ЯКЩО `custom: «лінія обривається, не дійшовши до OUT»` → ТО конфлікт (puzz.link `lrDeadEnd`).
- КОЛИ `constraint_broken(single_line)` → ЯКЩО `custom: «є окремий шматок лінії поза шляхом IN→OUT»` → ТО конфлікт (puzz.link `lnPlLine`) (?).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «лід як коридор»: на льоду лінія, що увійшла, мусить пройти айсберн наскрізь прямо — як ковзання; клітинки льоду біля стіни/рамки, куди прямий прохід неможливий, — порожні або лише в одному напрямку.
- Дедукція «стрілка»: напрямок стрілки фіксує напрямок обходу — лінію можна вести від IN і перевіряти сумісність з усіма стрілками.
- Перемога: одна лінія IN→OUT, усі стрілки пройдені за напрямком, кожен айсберн відвіданий, повороти лише поза льодом, перетини лише на льоду. Поразки й рахунку нема.

## Керування і ввід
- puzz.link play mode: ліва кнопка + drag по клітинках малює лінію; права кнопка + drag — мітки/стирання (тести `mouse,left` / `mouse,right` з ламаними траєкторіями).
- Drag може починатися з-за рамки (координата −1) — так лінія виходить з IN / йде в OUT (?).
- puzz.link edit mode: drag ставить стрілки на межах, drag з-за рамки — IN/OUT; права кнопка — інший тип редагування (лід?) (?).
- Цифрова версія: undo/redo, перевірка за кнопкою.

## Вікна, меню, HUD
- `game-screen`: сітка, крижані клітинки (блакитні), стрілки на межах, IN/OUT на рамці, лінія, `conflict-highlight` для помилкових сегментів.
- puzz.link: play/edit, кнопка перевірки з повідомленням першої помилки, `settings-window`.
- `help-window` — правила (puzz.link rules).
- Переходи: edit → play; check → повідомлення.

## Фічі поза полем
- `auto-check` за кнопкою (коди puzz.link).
- `undo` / `redo`; `level-editor` + `share-code` (puzz.link URL пазла).
- Банк — журнал Nikoli; генератора не бачив (?).

## Варіації й родичі
- Родичі в сімʼї: [Masyu](masyu.md) і [Yajilin](yajilin.md) (одна лінія через центри з правилами поворотів), [Slitherlink](slitherlink.md) (петля по ребрах).
- Поза сімʼєю: льодові рівні Pokémon / Kwirk-подібні ковзання (`push-slide`, `inertia-slide`), стрілки-однобічки Lolo/Supaplex (`one-way-cell`).
- Пов'язані pzpr-жанри на льоду: Icelom, Icelom 2 (?) — не відкривав.
- **Осі варіацій**: шлях IN→OUT / замкнена петля · де дозволено перетин (лід / ніде / всюди) · що обовʼязково відвідати (стрілки / айсберни / числа) · стрілки на межах / в клітинках.

## Цікавинки для курсу
- Модель лінії як множини ребер між центрами клітинок + перевірка ступенів (0, 2, або 4 лише як прямий хрест на льоду) — 📎.
- «На льоду лише прямо» — 🌱 (перевірка пари сегментів у клітинці).
- Обхід лінії від IN з перевіркою напрямку кожної стрілки — 📎.
- Перевірка «кожен айсберн відвідано» — 🌱 (компоненти льоду через flood fill + перетин з лінією).
- Повний валідатор зі списком кодів помилок, як у puzz.link, — 🥉; розвʼязувач — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `path-drawing`, `path-cut` ↔ drag-лінія · `one-way-cell` ↔ стрілки · `inertia-slide` ↔ «на льоду лише прямо» (аналогія) · `in-game-editor`, `import-open-formats` (puzz.link) · `undo-redo`.
- **Нема** → пропозиції карток:
  - `+ice-straight-path` «Лід: лінія не повертає, але може перетинатися» · game-logic/constraints · 📎 · слот {cross: ice|none|any}.
  - `+must-visit-checkpoints` «Шлях мусить пройти всі обовʼязкові точки/зони» · game-logic/constraints · 📎 · слот {what: arrows|zones|cells}.
  - `+crossing-detection` — повтор пропозиції з інших файлів: виявлення самоперетину лінії.

## Пропозиції до словників
- `+cond:turns` — лінія повертає в клітинці (повтор з Masyu).
- `+cond:crosses` — лінія перетинає себе/іншу в клітинці (повтор).
- `+cond:visited` — шлях пройшов через клітинку/зону/стрілку.
- `+trigger:pattern(loop_branch)` — розгалуження лінії (повтор).
- `+card:ice-straight-path`, `+card:must-visit-checkpoints` — див. мапу.

## Джерела
- ⭐ [puzz.link rules: Icebarn](https://puzz.link/rules.html?icebarn) — сторінка правил із прикладом (через WebFetch текст не рендериться).
- [puzz.link icebarn.js](https://puzz.link/js/pzpr-samples/icebarn.js) — правила: «starts at the IN arrow, goes through every arrow before reaching the OUT arrow», перетин лише на льоду, без поворотів на льоду, не проти стрілки, кожен icebarn — хоча б раз; Nikoli vol. 108; коди `lnBranch`, `lnCrossExIce`, `lnCurveOnIce`, `stNoLine`, `lrDeadEnd`, `lrOffField`, `lrReverse`, `lnPlLine`, `bkNoLine`, `arNoLine`.
- YouTube: пошук «icebarn puzzle».

## Непевне
- (?) Рік: перша поява — Puzzle Communication Nikoli vol. 108; рік номера не перевірено (`year: null`). Сторінки Nikoli EN для жанру нема (404), статті Wikipedia нема.
- (?) Стрілки на межах клітинок, а не в клітинках, — висновок з тестів редактора pzpr.
- (?) Розшифровка `stNoLine` (можливо, нема лінії з IN) і `lnPlLine` (кілька ліній) — за назвами.
- (?) Деталі вводу (права кнопка, стирання, редагування льоду) — з назв тестів, не з опису.
- (?) Icelom / Icelom 2 як родичі — з памʼяті, не перевірено.
