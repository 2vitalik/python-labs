---
title: puzz.link (pzprjs / pzprv3)
slug: puzz-link
aka: [pzprjs, pzprv3, pzpr.js, ぱずぷれ, Puzzle Square JP applet, pzv.jp]
family: pencil-logic
also: [push-slide, hidden-deduction]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2016
platforms: [web]
links:
  - {kind: official, url: "https://puzz.link/list.html", best: true, note: "список жанрів з групами (зафарбовування, області, петлі, лінії, рухомі, лід, татамі, числа, інше); звідти — плеєр і редактор"}
  - {kind: official, url: "https://puzz.link/", note: "головна: плеєр p, база пазлів db, File > Export URL, Network play, автоперевірка, формат p?genre/w/h/data"}
  - {kind: play, url: "https://puzz.link/rules.html", note: "сторінка правил жанру (?<id>); рендериться JS, EN/JP"}
  - {kind: other, url: "https://github.com/robx/pzprjs", note: "код (MIT), форк sabo2/pzprjs; як додати жанр: variety.js → src/variety → test/script"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/pzpr/variety.js", note: "таблиця жанрів: id → [pzprapp, kanpen, JP-назва, EN-назва, скрипт, {alias, pzprurl, kanpen}]"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/docs/InputModes.md", note: "режими вводу: спільні / question (edit) / answer (play) / info-перевірки"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/docs/Config.md", note: "налаштування: irowake, autocmp, autoerr, multierr, use, lrinvert…"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src-ui/p.html", note: "розмітка плеєра: меню File/Edit/Display/Setting/Help, кнопки, trial, timer, network"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/Changelog.md", note: "історія фіч: trial mode 2016, autocheck 2017–2020, network play 2020"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/aquarium.js", note: "приклад файла жанру: правила EN/JP + тест-дошки на кожен код помилки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=puzz.link+puzzle+solve", note: "пошук; розвʼязання в плеєрі"}
stage: v1
coverage: 60
mechanics: [satisfy-constraints, markup-validity, completion-detection, conflict-highlight, cell-click, keyboard-controls, hover-highlight, edge-marking, dot-mark, path-drawing, pencil-marks, connectivity-check, single-loop-check, neighbor-count-clue, line-sum-clue, run-length-clues, undo-redo, undo-unlimited, redo, in-game-editor, editor-window, editor-erase, level-exchange, level-bank, import-open-formats, state-string, state-as-data, logic-render-split, rule-variants, game-settings, field-size-picker, language-picker, help-window, about-window, unit-tests, fixture-level-tests, +platform-shell, +trial-mode, +fail-code-checklist, +url-puzzle-encoding]
proposes: ["+window:genre-list", "+window:game-id-dialog", "+window:network-popup", "+ui:input-mode-panel", "+ui:trial-marker", "+ui:play-edit-toggle", "+feature:trial-mode", "+feature:fail-code-check", "+feature:board-transform", "+feature:image-export", "+feature:auto-check-levels", "+feature:solve-tracking", "+cond:checklist_pass", "+card:fail-code-checklist", "+card:url-puzzle-encoding", "+card:trial-mode"]
author: opus
date: 2026-11-09
---

# puzz.link — сотні жанрів паперових пазлів в одному браузерному плеєрі-редакторі з автоперевіркою правил

## Суть
puzz.link — не гра, а **платформа**: веб-аплет pzprjs (форк sabo2/pzprjs, що працює на pzv.jp), у якому кожен жанр Nikoli/WPF-типу описаний як модуль: поле, ввід, рендер, кодування в URL і перевірка відповіді. Пазли тут не генеруються — їх складають люди в режимі редактора й діляться посиланням `puzz.link/p?<жанр>/<ширина>/<висота>/<дані>`. Гравець розвʼязує в режимі play з undo/redo, «пробним шаром» (trial), кольоруванням ліній і перевіркою, що називає перше порушене правило. Для курсу це другий еталон платформи після [Tatham](tatham-collection.md): там — генератор і 40 ігор, тут — редактор, формат обміну і ~сотні жанрів, кожен — «таблиця правил як дані + тест на кожне правило».

## Поле і час
- Поле — прямокутна сітка W×H; обʼєкти живуть на кількох шарах координат: клітинки, ребра між ними (межі областей, лінії), вершини (cross), позаполеві клітинки `excell` (підказки по краю: Aquarium, Skyscrapers, Nonogram).
- Кожен обʼєкт має два набори станів: **question** (дане умовою, ставиться в edit) і **answer** (розмітка гравця в play) + допоміжні `qsub`-мітки (крапка, хрестик `peke`), що не впливають на перевірку.
- Області (`room`) обчислюються з меж; звʼязні компоненти зафарбованих / незафарбованих / ліній — графи, які аплет перераховує на кожному ході (для перевірки й `irowake`).
- Час статичний; хід = одна операція вводу. Є необовʼязковий таймер (з 2020 — стартує, коли пазл видно).
- «Рухомі» жанри (`移動系`: обʼєкти зсуваються стрілкою-лінією) і «льодові» (`アイスバーン系`) — усе одно статичні розвʼязки; є опція `dispmove` — малювати обʼєкт так, ніби він уже переїхав.

## Сутності
Дві частини: (1) обʼєкти дошки, спільні для всіх жанрів; (2) жанри як дані.

| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | ques / qnum (дане) · qans / anum (відповідь) · qsub (мітка) | перемикається вводом за поточним режимом; рендер і перевірка — модулем жанру |
| Ребро (border) | mark | межа області (дане) · лінія (відповідь) · хрестик `peke` | межі задають `room`; лінії утворюють граф шляхів/петель |
| Вершина (cross) | mark | число / крапка | підказки на перетинах (Slant-подібні, Tentai Show) |
| Позаполева клітинка (excell) | static | число по краю | підказка ряду/стовпця; можна позначити «виконано» (сіріє) |
| Область (room) | zone | клітинки між межами | звʼязна компонента без меж; квоти й однорідність — у перевірках жанру |
| Число-підказка | static | значення, «?» | `autocmp`: виконане відображається інакше, ніж невиконане |
| Мітки-символи | mark | коло / трикутник / квадрат / стрілка / зірка / літера | спільні режими `mark-circle`, `mark-triangle`, `mark-rect`, `arrow` |
| Допоміжна мітка | mark | крапка `dot`, хрестик `peke`, `objblank`, `numblank` | нотатки гравця; при перевірці ігноруються; стираються окремою кнопкою |
| Компонента (лінія / блок) | zone | колір | `irowake` / `irowakeblk` — кожна компонента свого кольору |
| Пробний шар (trial) | mark | глибина | ходи після «Enter trial» малюються як припущення; Accept зливає, Reject відкочує |

Жанри як дані (групи — зі списку puzz.link; приклади — жанри, вже описані в корпусі):

| Група list.html | Що розмічає гравець | Приклади |
|---|---|---|
| 黒マス配置系 / 領域＋黒マス系 / 連黒分断禁系 — зафарбовування | клітинки чорне/біле | [Nurikabe](nurikabe.md), [Heyawake](heyawake.md), [Hitori](hitori.md), [Kuromasu](kuromasu.md), [Yin-Yang](yin-yang.md), [Aquarium](aquarium.md), [Nuri-Maze](nuri-maze.md) |
| 領域分割系 / 領域＋数字系 — поділ на області | межі / числа в областях | [Shikaku](shikaku.md), [Fillomino](fillomino.md), [Tentai Show](tentai-show.md), [LITS](lits.md) |
| ループ系 / 交差ありループ系 — петлі | лінії по центрах клітинок або ребрах | [Slitherlink](slitherlink.md), [Masyu](masyu.md), [Yajilin](yajilin.md) |
| 線でつなぐ / ひとつながり — зʼєднання | лінії між обʼєктами | [Hashiwokakero](hashiwokakero.md) |
| 移動系 — рухомі | лінія = траєкторія обʼєкта | [Yajisan-Sokoban](yajisan-sokoban.md), Herugolf |
| アイスバーン系 — лід | лінія з ковзанням | [Icebarn](icebarn.md) |
| タタミ系 / 数字系 / その他 | числа, розстановка | [Sudoku](sudoku.md), [Kakuro](kakuro.md), [Skyscrapers](skyscrapers.md), [Nonogram](nonogram.md), [Takuzu](takuzu.md), Minesweeper |

Запис жанру в `variety.js`: `id: [pzprapp, kanpen, "JP-назва", "EN-назва", "скрипт", {alias, pzprurl, kanpen}]` — напр. `mashu: [0, 1, "ましゅ", "Masyu", "", {kanpen: "masyu", alias: "pearl"}]`; кілька id можуть ділити один скрипт (`aho` → `shikaku`).

## Правила (КОЛИ → ЯКЩО → ТО)
Спільні правила оболонки:
- КОЛИ `input(click, cell)` → ЯКЩО `mode(play)` and `mode(auto)` → ТО `custom: «дія за жанром і кнопкою: ліва — основний стан, права — допоміжний»` (`mark` / `unmark`); ЯКЩО `mode(edit)` → ТО `custom: «змінити дане умовою (question)»`.
- КОЛИ `input(drag, cells)` → ТО `custom: «протяжка: лінія по ребрах/центрах або той самий стан на всі клітинки шляху»`.
- КОЛИ `input(select_mode, m)` → ТО `custom: «inputMode = m»` (≈70 режимів: `shade`, `unshade`, `line`, `peke`, `number`, `border`, `completion`, `bgcolor`…); `auto` — дефолт.
- КОЛИ `input(key, digit)` → ЯКЩО `custom: «клітинка під курсором приймає число»` → ТО `set_value(cell, digit)`.
- КОЛИ `input(undo)` → ТО `undo(1)`; КОЛИ `input(redo)` → ТО `custom: «повторити скасоване»`.
- КОЛИ `input(enter_trial)` → ТО `undo_point`, `custom: «наступні ходи — пробні, з trial marker»`; КОЛИ `input(accept_trial)` → ТО `custom: «пробні ходи стають звичайними»`; КОЛИ `input(reject_trial)` → ТО `custom: «відкотити до точки входу в trial»`; `enter further trial` — вкладений рівень.
- КОЛИ `input(ansclear)` → ТО `custom: «стерти всю відповідь, лишити умову»`; КОЛИ `input(subclear)` → ТО `custom: «стерти лише допоміжні мітки»`.
- КОЛИ `input(check)` → ТО `custom: «пройти checklist жанру по порядку»`; ЯКЩО `custom: «функція перевірки впала»` → ТО `constraint_broken(fail_code)`, `message(текст коду)`, `custom: «підсвітити клітинки-порушники»`; ЯКЩО `mode(multierr)` → показати всі порушення, а не перше.
- КОЛИ `all_constraints_met` → ЯКЩО `mode(autocheck)` → ТО `message(complete)`, `timer(stop)` (?); режими autocheck: off / guarded / simple (з 0.13.0).
- КОЛИ `custom: «підказку виконано»` → ЯКЩО `mode(autocmp)` → ТО `custom: «число змінює колір»`; ЯКЩО `mode(autoerr)` → ТО `custom: «неповні/хибні числа підсвічуються одразу»`.
- КОЛИ `input(url_output)` → ТО `custom: «encode: p?<pzprurl>/<w>/<h>/<дані умови>»`; КОЛИ `input(url_input, url)` → ТО `custom: «decode → нова дошка»`.
- КОЛИ `input(file_save)` → ТО `custom: «файл pzprv3: умова + відповідь (+ стан)»`; КОЛИ `input(file_open)` → ТО `custom: «прочитати pzprv3 або Kanpen-формат»` (`kanpen`-id у variety.js).
- КОЛИ `input(adjust | turnflip)` → ЯКЩО `mode(edit)` → ТО `custom: «розширити/обрізати край, повернути/віддзеркалити поле»`.
- КОЛИ `input(network_start)` → ТО `custom: «кооперативна сесія: ходи всіх учасників синхронізуються»`.
- КОЛИ `custom: «змінився граф ліній»` → ЯКЩО `mode(irowake)` → ТО `paint(component, color)`.
Перевірка жанру як дані (приклад Aquarium):
- `checklist = ["checkShadeCellExist+", "checkSupports", "checkPoolLevel", "checkRegionLevel", "checkShadeCount+"]` — кожен елемент — функція, що повертає код помилки (`csNoSupport`, `csNoLevel`, `bkNoLevel`, `exShadeNe`…); `+` у назві — спільна функція фреймворку (?).
- КОЛИ `custom: «тест-дошка з test/script/<жанр>.js»` → ЯКЩО `custom: «перевірка повертає очікуваний fail code»` → ТО тест пройдено — на кожен код помилки є дошка, що його викликає, і дошка `null` — правильний розвʼязок.
- Перемога: checklist жанру проходить без помилок. Поразки й рахунку нема; таймер — лише для себе (і статистики розвʼязань у db (?)).

## Керування і ввід
- Миша: ліва/права кнопка — два основні стани (фарба/крапка, лінія/хрестик); `lrinvert` міняє їх місцями; `use` 1/2 — дві схеми вводу зафарбовування (клік-перемикач чи «права = біле») (?).
- Протяжка: drag малює лінію по центрах клітинок (петлі), по ребрах (межі, Slitherlink-ребра) або фарбує ряд клітинок одним станом.
- Клавіатура: курсор (стрілки, `cursor` у Display), цифри й літери для чисел, переходи по `excell` по краю.
- Панель режимів вводу: явний вибір інструмента (`shade`, `unshade`, `line`, `peke`, `bgcolor`, `completion`…) — для тачу й неоднозначних жанрів.
- Тач: pinch-zoom (Android Chrome) і змішаний тач+миша (0.9.0, 2017).
- Перемикач Edit / Play: той самий екран — і редактор умови, і розвʼязування.

## Вікна, меню, HUD
- `game-screen`: поле + рядок меню + панель кнопок: Check · Undo · Redo · Erase answer · Erase marks · Enter trial / Accept / Reject / Further trial · Colour all (irowake) · жанрові кнопки (напр. `dropblocks`).
- Меню File: New board · URL input · URL output · File open · File save · Duplicate · Image save · Network play.
- Меню Edit: Adjust (край поля) · Turn/flip.
- Меню Display: Cell size (XS…XL, custom) · Font (sans/serif) · `undefcell`, Cursor, Trial marker, Timer, Adjust size, Full width, Pin menu/buttons · сховати панель інструментів.
- Меню Setting: LR invert · bgcolor · multierr · forceallcell · enline/lattice · singlenum · discolor · Autosave · `use_tri` 1–3 · Autocheck (off / guarded / simple) · мова 日本語 / English.
- Меню Help: Rules (`help-window`, rules.html) · About (`about-window`) · Translate (Weblate) · Issues.
- Діалоги: `confirm-dialog` («Confirmation»/«Notice», OK/Cancel) · `+window:game-id-dialog` (URL input/output) · New board (`custom-window`: розмір W×H) · `+window:network-popup` (Start, Share).
- HUD: `timer-elapsed` з Reset / Pause / Resume · `+ui:input-mode-panel` · `+ui:play-edit-toggle` · `+ui:trial-marker` · `conflict-highlight` · `selection-highlight` (курсор).
- Поза аплетом: `+window:genre-list` (list.html: групи, сортування за датою / за абеткою) → `game-screen` у edit; `puzzle-select` — база `puzz.link/db` (публічні пазли з посиланням на джерело).
- Переходи: list.html → p?<жанр> (edit) → URL output → друг відкриває p?<жанр>/<w>/<h>/<дані> (play) → Check → повідомлення.

## Фічі поза полем
- `undo` ∞ + `redo`; `+feature:trial-mode` — шар припущень з прийняттям/відкатом (з 0.4.0, 2016).
- `auto-check` трьох рівнів + `+feature:fail-code-check` (текст першого порушеного правила) + `multierr`.
- `level-editor` (той самий екран у edit) + `share-code` (URL) + `export-import` (файл pzprv3, Kanpen) + `+feature:image-export` (PNG/JPEG з налаштуванням фону).
- `+feature:board-transform` — Adjust і Turn/flip у редакторі.
- `custom-rules` — прапорці варіантів жанру (напр. `aquarium_regions`, `uramashu` для Masyu, `forceallcell` для Fillomino); з 0.13 пазл можна позначити як варіант.
- `mode-coop` — мережева кооперативна гра (з 2020, сервер — окремий проєкт).
- `puzzle-bank` — puzz.link/db; `+feature:solve-tracking` — облік розвʼязань і статистика для залогінених.
- `autosave`, `localization` (JP/EN, Weblate), налаштування — у localStorage браузера, на сервер не йдуть.
- Нема: генератора пазлів, розвʼязувача-підказки, рівнів і рекордів.

## Варіації й родичі
- Родовід: pzprv3 / pzpr.js (sabo2, «ぱずぷれ») → pzv.jp → pzprjs robx (puzz.link); 2022-11-17 влито pzprxs (X_Sheep) — «багато нових жанрів і виправлень».
- Найближчий родич — [Simon Tatham's Collection](tatham-collection.md): спільна оболонка + модуль на гру; різниця — генератор (Tatham) проти редактора й URL-обміну (puzz.link).
- Інші плеєри жанрів: Kanpen / pencilbox (формат, який pzprjs імпортує), SudokuPad (CtC, судоку-варіанти — [sudoku-variants](sudoku-variants.md)), Conceptis, puzzle-*.com (з daily і рекордами).
- **Осі варіацій** платформ: звідки пазли (генератор / автори / журнал) · як обмін (seed / опис / URL) · глибина перевірки (нічого / «complete» / перший код помилки / усі помилки) · шар припущень (нема / pencil / trial з accept-reject) · ширина (один жанр / 40 / сотні).

## Цікавинки для курсу
- Жанр = модуль із 5 частин (ввід, дошка, рендер, кодування, перевірка) поверх спільного ядра — 🥇 (та сама архітектура, що `logic-render-split`, але на сотні жанрів).
- Checklist як список функцій із кодами помилок + тест-дошка на кожен код — 🥉 (прямо переноситься на юніт-тести лабораторної).
- URL-кодування пазла `p?genre/w/h/data` (компактні числа й бітові маски в base-36-подібному алфавіті (?)) — 📎.
- Trial mode: вкладені шари припущень з accept/reject поверх undo-стеку — 🥉.
- `irowake`: перефарбування звʼязних компонент ліній на кожен хід (union-find / BFS) — 📎.
- Один екран для edit і play: те саме поле, різні шари (question/answer) — 📎.
- Кооп по мережі: синхронізація ходів кількох гравців на одній дошці — 🥈.

## Мапа на каталог
- Є: `satisfy-constraints`, `markup-validity`, `completion-detection`, `conflict-highlight` ↔ Check з підсвіткою · `cell-click`, `keyboard-controls`, `hover-highlight` (курсор) · `edge-marking` (лінії, межі, `peke`) · `dot-mark` · `path-drawing` (лінії drag-ом) · `pencil-marks` (кандидати в числових жанрах (?)) · `connectivity-check`, `single-loop-check`, `neighbor-count-clue`, `line-sum-clue`, `run-length-clues` ↔ типові функції checklist · `undo-redo`, `undo-unlimited`, `redo` · `in-game-editor`, `editor-window`, `editor-erase` ↔ edit-режим · `level-exchange`, `import-open-formats`, `state-string` ↔ URL і pzprv3 · `level-bank` ↔ db · `state-as-data`, `logic-render-split` · `rule-variants` ↔ прапорці варіантів · `game-settings`, `field-size-picker` (Cell size), `language-picker` · `help-window`, `about-window` · `unit-tests`, `fixture-level-tests` ↔ test/script/ з дошкою на кожен fail code.
- **Нема** → пропозиції карток:
  - `+platform-shell` (є в tatham-collection) — тут з редактором замість генератора.
  - `+fail-code-checklist` «Перевірка розвʼязку списком правил із кодами помилок» · game-logic/constraints · 🥉 · слот {order, multierr}.
  - `+url-puzzle-encoding` «Пазл у URL: жанр/розмір/дані» · levels/format · 📎.
  - `+trial-mode` «Шар припущень: увійти / прийняти / відкинути» · game-logic/history · 🥉.

## Пропозиції до словників
- `+window:genre-list` — каталог жанрів платформи з групами й сортуванням (list.html), окремо від `puzzle-select`.
- `+window:game-id-dialog` (повтор з Tatham) — ввід/вивід URL пазла.
- `+window:network-popup` — старт і запрошення в кооп-сесію.
- `+ui:input-mode-panel` — явний вибір інструмента вводу; `+ui:trial-marker` — позначка пробних ходів; `+ui:play-edit-toggle` — перемикач редактор/гра на тому самому екрані.
- `+feature:trial-mode`, `+feature:fail-code-check`, `+feature:board-transform`, `+feature:image-export`, `+feature:auto-check-levels` (off / guarded / simple), `+feature:solve-tracking`.
- `+cond:checklist_pass` — усі функції перевірки жанру пройшли (узагальнення `all_constraints_met` з порядком і кодами).
- `+card:fail-code-checklist`, `+card:url-puzzle-encoding`, `+card:trial-mode` — див. мапу.

## Джерела
- ⭐ [puzz.link: list of puzzle types](https://puzz.link/list.html) — групи жанрів JP/EN, сортування за датою й абеткою.
- [puzz.link](https://puzz.link/) — плеєр `p`, база `db`, Export URL, Network play, autocheck, приклади URL `p?skyscrapers/5/5/…`, історія (pzv.jp, pzprxs 2022-11-17).
- [robx/pzprjs](https://github.com/robx/pzprjs) — README: MIT, структура `src/`, `src-ui/`, `test/`; шість кроків додавання жанру; глосарій irowake / peke.
- [variety.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/pzpr/variety.js) — поля запису жанру, ≈349 записів (підрахунок WebFetch).
- [InputModes.md](https://raw.githubusercontent.com/robx/pzprjs/master/docs/InputModes.md) · [Config.md](https://raw.githubusercontent.com/robx/pzprjs/master/docs/Config.md) — режими вводу й налаштування.
- [src-ui/p.html](https://raw.githubusercontent.com/robx/pzprjs/master/src-ui/p.html) — меню й кнопки плеєра (i18n-ключі).
- [Changelog.md](https://raw.githubusercontent.com/robx/pzprjs/master/Changelog.md) — trial 2016-07-24, autocheck 2017–2020, network 2020-03-30.
- [aquarium.js (pzpr-samples)](https://puzz.link/js/pzpr-samples/aquarium.js) і [src/variety/aquarium.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/aquarium.js) — приклад жанру: правила, checklist, тест-дошки.
- YouTube: пошук «puzz.link puzzle solve».

## Непевне
- (?) Кількість жанрів: черга каже 244, підрахунок записів `variety.js` дав ≈349 (частина — аліаси/варіанти на спільному скрипті); точного числа не рахував сам.
- (?) Рік: 2016 — перший запис Changelog pzprjs (0.0.1, 2016-01-31); pzprv3/pzpr.js sabo2 і pzv.jp — старші, року не бачив.
- (?) Значення autocheck «guarded» проти «simple», зупинка таймера після розвʼязання, `use` 1/2 — лише назви з p.html/Config.md.
- (?) Алфавіт і схема кодування даних у URL, точна структура файла pzprv3 (рядки «pzprv3 / жанр / rows / cols …») — з памʼяті.
- (?) Склад груп list.html — текст сторінки прийшов без лінків, групи названі, жанри в них не перелічені.
- (?) Статистика розвʼязань у db — з головної («Solve tracking and stats for logged-in database users»), сам не бачив.
