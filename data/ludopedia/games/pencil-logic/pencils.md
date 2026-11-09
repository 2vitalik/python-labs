---
title: Pencils (Nikoli)
slug: pencils
aka: [ペンシルズ, Олівці]
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
  - {kind: other, url: "https://www.nikoli.co.jp/en/puzzles/pencils/", best: true, note: "Nikoli: правила й приклад"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/pencils.js", note: "puzz.link: правила EN/JP, коди помилок, тести вводу, пазл-приклад"}
  - {kind: other, url: "https://puzz.link/rules.html?pencils", note: "puzz.link: сторінка правил (рендериться JS)"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json", note: "pzprjs: тексти помилок pencils"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=nikoli+pencils+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, path-drawing, path-cut, cell-click, keyboard-controls, conflict-highlight, in-game-editor, level-bank, undo-redo, +crossing-detection, +full-cover-check, +pencil-tip-line]
proposes: ["+cond:crosses", "+cond:degree(cell, n)", "+cond:line_length(line, op, n)", "+card:pencil-tip-line", "+card:full-cover-check"]
author: opus
date: 2026-11-09
---

# Pencils — поділи поле на олівці й «почерк»: від вістря кожного олівця тягнеться лінія його ж довжини

## Суть
Поле треба повністю розкласти на олівці та лінії. Олівець — прямокутник 1×N (стрижень) з вістрям, що займає ще одну клітинку на короткому кінці. Від вістря йде лінія через центри клітинок, рівно стільки клітинок, скільки довжина стрижня. Числа в стрижнях кажуть довжину олівця. Незвичне: дві різні сутності (фігура-прямокутник і лінія-шлях) повʼязані однією довжиною й покривають поле без залишку.

## Поле і час
- Прямокутна сітка; дані: числа в клітинках (довжина свого олівця), інколи дані вістря (?).
- Шари: межі стрижнів (ребра) · вістря (клітинка зі стрілкою-напрямком) · лінії по центрах клітинок · дані числа.
- Кожна клітинка в розвʼязку — або стрижень, або вістря, або лінія.
- Час статичний; хід = провести межу / поставити вістря / намалювати відрізок лінії.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | terrain | — | має належати стрижню, вістрю або лінії |
| Стрижень олівця | zone | 1×N, ширина 1 | рівно одне вістря на короткому кінці |
| Вістря | source | напрямок (від стрижня) | початок лінії; рівно одна лінія |
| Лінія | mark | довжина L | від вістря через центри клітинок, повороти на 90°; L = N |
| Число | mark | N | довжина стрижня, у якому стоїть; кілька однакових чисел або жодного |
| Межа | mark | ребро | контур стрижня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, edges)` → ТО `mark(edge, border)` — контур стрижня.
- КОЛИ `input(click, cell)` → ЯКЩО `custom: «клітинка на короткому кінці стрижня»` → ТО `mark(cell, tip)`; Shift+стрілка — напрямок вістря (?).
- КОЛИ `input(drag, cells)` → ТО `mark(cells, line)` (`path-drawing`); повернення назад стирає хвіст (?).
- КОЛИ `constraint_broken(number)` → ЯКЩО `custom: «число не всередині стрижня»` → ТО `set_state(number, error)`.
- КОЛИ `constraint_broken(number)` → ЯКЩО `custom: «число ≠ довжина стрижня»` → ТО `set_state(pencil, error)` (nmSizeLt / nmSizeGt).
- КОЛИ `constraint_broken(tip)` → ЯКЩО `custom: «вістря не на короткому кінці прямокутника 1×N або всередині стрижня»` → ТО `set_state(tip, error)`.
- КОЛИ `constraint_broken(pencil)` → ЯКЩО `count(tip, gt, 1)` → ТО `set_state(pencil, error)` («A pencil has more than one tip»).
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінія розгалужується»` (`+cond:degree`) or `custom: «лінії перетинаються»` (`+cond:crosses`) → ТО `set_state(line, error)`.
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінія проходить крізь стрижень»` → ТО `set_state(line, error)`.
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінія не торкається вістря або торкається двох вістер»` → ТО `set_state(line, error)`.
- КОЛИ `constraint_broken(tip)` → ЯКЩО `custom: «з вістря не виходить лінія»` → ТО `set_state(tip, error)`.
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «довжина лінії ≠ довжина її олівця»` (`+cond:line_length`) → ТО `set_state(line, error)`.
- КОЛИ `constraint_broken(cover)` → ЯКЩО `custom: «клітинка не належить ні олівцю, ні лінії»` → ТО `set_state(cell, error)` («A cell is unused»).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «кишеня»: ізольований закуток з k клітинок може бути лише кінцем лінії або олівцем довжини k−1 з вістрям.
- Дедукція «баланс»: кожен олівець займає N+1+N клітинок, тож площа області без виходу має бути сумою 2N+1.
- Перемога: поле покрито олівцями й лініями, кожна лінія — від свого вістря, довжиною свого стрижня, без перетинів і розгалужень. Поразки й рахунку нема.

## Керування і ввід
- puzz.link: drag лівою — межі стрижнів або лінії (залежно від того, по ребрах чи по центрах); подвійний/потрійний клік, права кнопка — інші мітки (тести `mouse,leftx2`, `leftx3`, `right`) (?).
- Курсор + Shift+стрілки — поставити/повернути вістря; цифри — числа (edit mode).
- Папір: олівець малюють контуром із загостреним кінцем, лінію — як «почерк».
- Цифрова версія: undo/redo, перевірка за кнопкою.

## Вікна, меню, HUD
- `game-screen`: сітка, числа, межі, вістря-трикутники, лінії; `conflict-highlight` після перевірки.
- puzz.link: перемикач play/edit, кнопка перевірки, `settings-window`.
- `help-window` — правила (Nikoli / puzz.link).
- Переходи: edit → play; check → повідомлення з текстом помилки.

## Фічі поза полем
- `auto-check` за кнопкою (pzprjs: 15 кодів помилок для жанру).
- `undo` / `redo`; `level-editor` + `share-code` (URL пазла).
- Банк: пазли Nikoli (журнал, сайт) і авторські на puzz.link (?).

## Варіації й родичі
- У сімʼї: [Shikaku](shikaku.md) (прямокутники з числом-площею), [Fillomino](fillomino.md) (покриття областями з числом), [Masyu](masyu.md) і [Yajilin](yajilin.md) (лінія через центри клітинок), [Nurikabe](nurikabe.md).
- **Осі варіацій**: довжина лінії = N / задана окремо · лінія з поворотами / лише пряма · числа в стрижнях / на лініях · повне покриття / дозволені порожні клітинки.

## Цікавинки для курсу
- Модель: прямокутники-стрижні + клітинка-вістря + шлях як список клітинок — 🌱.
- Перевірка повного покриття трьома видами сутностей — 🌱.
- Перевірка ліній: ступінь клітинок, без перетинів, один кінець на вістрі, довжина = стрижень — 📎.
- Розвʼязувач з відсіканням за площею кишень — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints`, `conflict-highlight` · `path-drawing`, `path-cut` ↔ лінії · `cell-click`, `keyboard-controls` · `in-game-editor`, `level-bank`, `undo-redo`.
- **Нема** → пропозиції карток:
  - `+pencil-tip-line` «Фігура з кінцем-джерелом, від якого лінія тієї ж довжини» · game-logic/constraints · 📎.
  - `+full-cover-check` «Кожна клітинка належить рівно одній сутності» · game-logic/constraints · 🌱.
  - `+crossing-detection` — повтор з Yajisan-Sokoban.

## Пропозиції до словників
- `+cond:crosses`, `+cond:degree(cell, n)` — повтори (Tracks, Yajisan-Sokoban).
- `+cond:line_length(line, op, n)` — довжина намальованої лінії в клітинках.
- `+card:pencil-tip-line`, `+card:full-cover-check` — див. мапу.

## Джерела
- ⭐ [Nikoli: Pencils](https://www.nikoli.co.jp/en/puzzles/pencils/) — правила: олівець з вістрям, лінія від вістря через стільки клітинок, скільки в числі, без перетинів і розгалужень.
- [puzz.link: pencils.js](https://puzz.link/js/pzpr-samples/pencils.js) — 6 правил (стрижень 1×N + вістря, лінія не до чужого вістря, не крізь олівці, довжина = олівець, числа, повне покриття), тести вводу.
- [pzprjs: failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json) — тексти 15 помилок жанру.
- YouTube: пошук «nikoli pencils puzzle».

## Непевне
- (?) Рік і автор жанру — сторінка Nikoli не вказує (`year: null`).
- (?) Переказ Nikoli згадує поворот лінії «по діагоналі» — суперечить решті джерел; беру лише горизонтальні/вертикальні кроки.
- (?) Чи заборонено лініям торкатися одна одної (не лише перетинатись) — у кодах помилок такої нема.
- (?) Точна розкладка дій миші/клавіш у puzz.link — з назв тестів, не з довідки.
- (?) Чи бувають дані вістря в умові — не бачив прикладу.
