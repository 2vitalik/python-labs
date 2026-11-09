---
title: Kuralin (クラリン)
slug: kuralin
aka: [クラリン, Kurarin, Clarine]
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
year: 2025
platforms: [paper]
links:
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/kuralin/", best: true, note: "Nikoli: 3 правила EN, картинки Sample / Progressing / Solution (5×5)"}
  - {kind: official, url: "https://www.nikoli.co.jp/ja/puzzles/kuralin/", note: "Nikoli: правила JA («小さな丸»), ті самі картинки"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Nikoli/191.htm#5", note: "Janko: огляд Nikoli № 191, дата 10.06.2025, правила EN/DE/JA, 3 пазли"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kuralin+nikoli+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, single-loop-check, path-drawing, cell-click, dot-mark, help-window, +cell-shade-toggle, +cell-coverage-check, +vertex-clue, +majority-touch-clue]
proposes: ["+cond:majority", "+cond:on_loop", "+trigger:pattern(loop_branch)", "+card:majority-touch-clue", "+card:cell-coverage-check"]
author: opus
date: 2026-11-09
---

# Kuralin — петля через усі білі клітинки, а кружки на ребрах і у вузлах кажуть, якого кольору довкола більше

## Суть
Гравець проводить одну замкнену петлю через центри клітинок; кожна клітинка, якою петля не пройшла, стає чорною. Підказки — маленькі кружки на межах клітинок: чорний кружок торкається більше чорних клітинок, ніж білих, білий — більше білих, сірий — порівну. Незвичне: підказка — **порівняння «більше / менше / порівну»**, а не число, і колір клітинки визначається самою петлею.

## Поле і час
- Прямокутна сітка; приклад Nikoli — 5×5.
- Петля йде по центрах клітинок горизонтально й вертикально, без перетинів і розгалужень, кожну клітинку проходить щонайбільше раз.
- Кружки стоять на ребрі між двома клітинками або у вузлі між чотирма (видно на прикладі Nikoli); «торкається» = клітинки, що мають це ребро чи вузол.
- Шари: кружки трьох кольорів (незмінні) · лінія петлі · чорні клітинки · допоміжні крапки «тут біле» (картинка «Progressing»).
- Час статичний; хід = провести/стерти відрізок лінії або позначити клітинку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | на петлі (біла) / чорна | без лінії — чорна |
| Петля | zone | — | рівно один цикл через центри; проходить усі білі клітинки |
| Чорний кружок | static | 2 або 4 дотичні клітинки | чорних серед дотичних більше, ніж білих |
| Білий кружок | static | 2 або 4 | білих більше, ніж чорних |
| Сірий кружок | static | 2 або 4 | чорних і білих порівну |
| Чорна клітинка | mark | — | сусідство з іншими чорними дозволене (на розвʼязку Nikoli чорні стоять блоком) |
| Крапка | mark | — | допоміжна позначка «біла», не перевіряється |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells)` → ТО `mark(cells, line)` (цифрова версія) (?).
- КОЛИ `input(click, cell)` → ТО `mark(cell, shaded)` або `mark(cell, dot)` (цифрова версія) (?).
- КОЛИ `constraint_broken(cover)` → ЯКЩО `custom: «клітинка без лінії не чорна або чорна з лінією»` (`+cond:on_loop`) → ТО помилка — кожна клітинка рівно в одному з двох станів.
- КОЛИ `pattern(loop_branch)` → ТО `set_state(cell, error)` — розгалуження заборонене.
- КОЛИ `pattern(loop_cross)` → ТО `set_state(cell, error)` — перетин заборонений.
- КОЛИ `constraint_broken(one_loop)` → ЯКЩО `not single_loop` → ТО помилка.
- КОЛИ `constraint_broken(black_circle)` → ЯКЩО `occupied(edge_or_vertex, black_circle)` and `custom: «чорних серед дотичних ≤ білих»` (`+cond:majority`) → ТО `set_state(circle, error)`.
- КОЛИ `constraint_broken(white_circle)` → ЯКЩО `occupied(edge_or_vertex, white_circle)` and `custom: «білих серед дотичних ≤ чорних»` → ТО `set_state(circle, error)`.
- КОЛИ `constraint_broken(gray_circle)` → ЯКЩО `occupied(edge_or_vertex, gray_circle)` and `not same(black_touching, white_touching, count)` → ТО `set_state(circle, error)`.
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «кружок на ребрі»: чорний → обидві клітинки чорні; білий → обидві білі (на петлі); сірий → одна чорна, одна біла.
- Дедукція «кружок у вузлі»: чорний → ≥ 3 з 4 чорні; білий → ≥ 3 з 4 білі; сірий → рівно 2 і 2.
- Дедукція «два виходи»: біла клітинка має рівно двох сусідів по петлі — якщо білих сусідів лише два, петля йде через обидва; біла кутова клітинка поля — обидва її сусіди білі.
- Дедукція «тупик»: клітинка з трьома чорними сусідами не може бути білою.
- Перемога: одна петля, решта клітинок чорні, усі кружки правдиві. Поразки й рахунку нема.

## Керування і ввід
- Папір: олівцем лінія через центри клітинок, зафарбування решти; крапки — допоміжні позначки білих (картинка «Progressing» Nikoli).
- Цифрова версія: протяжка по клітинках — відрізки лінії; клік — чорна / крапка; undo/redo; перевірка за кнопкою.
- Реалізації в puzz.link / pzprjs не знайшов: `pzpr-samples/kuralin.js` — 404, у `variety.js` такого id нема.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): сітка з кружками на ребрах і вузлах, лінія петлі, чорні клітинки, крапки, `conflict-highlight` на хибному кружку.
- `help-window` — правила Nikoli з трьома картинками (Sample → Progressing → Solution).
- `puzzle-select` — 3 пазли Janko в огляді № 191 (цифрова версія).
- Переходи: help-window → game-screen → Check → помилка / розвʼязано.

## Фічі поза полем
- `auto-check`, `undo` / `redo` — у цифровій версії (?).
- `puzzle-bank`: журнал Puzzle Communication Nikoli № 191; Janko — 3 пазли з розвʼязками.

## Варіації й родичі
- [Yajilin](yajilin.md) — той самий каркас «петля через усі нечорні клітинки», але чорні там не торкаються, а підказки — стрілки з числами.
- [Masyu](masyu.md) — кружки двох кольорів керують петлею, але стоять у клітинках і задають поворот/прямий хід.
- [No Three](no-three.md) — кружки на ребрах і у вузлах рахують дотичні клітинки (рівно одна чорна).
- [Moon or Sun](moon-or-sun.md), [Country Road](country-road.md) — петля по центрах клітинок з обмеженнями регіонів.
- **Осі варіацій**: де стоїть кружок (ребро / вузол / клітинка) · що порівнює (більшість / рівність / точна кількість) · чи можуть чорні торкатися · чи всі нечорні клітинки на петлі.

## Цікавинки для курсу
- Підрахунок кольорів дотичних клітинок для кружка на ребрі чи у вузлі — 🌱 (подвоєні координати, як у pzpr).
- Тризначне порівняння `sign(black − white)` замість числа — 🌱; чудове завдання на `match`/`case`.
- Перевірка «петля проходить усі білі»: ступінь 2 для кожної білої клітинки + одна компонента — 📎.
- Повний валідатор — 🥉; розвʼязувач (кружки → кольори → петля з відкатом) — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `single-loop-check` ↔ одна петля · `path-drawing` ↔ лінія протяжкою · `cell-click`, `dot-mark` · `help-window`.
- Перевикористано: `+cell-shade-toggle`, `+cell-coverage-check` (Yajilin: кожна клітинка — петля або чорна), `+vertex-clue` (Slant; тут ще й ребра).
- **Нема** → пропозиції карток:
  - `+majority-touch-clue` «Кружок: якого кольору більше серед дотичних клітинок» · game-logic/constraints · 🌱 · слот {result: more-black|more-white|equal, anchor: edge|vertex}.

## Пропозиції до словників
- `+cond:majority` — повтор (Blue Lagoon, Bosk): більшість серед заданих клітинок; тут ще й «порівну» для сірого.
- `+cond:on_loop` — повтор із Yajilin: клітинка належить петлі.
- `+trigger:pattern(loop_branch)` — повтор.
- `+card:majority-touch-clue` — див. мапу; `+card:cell-coverage-check` — повтор.

## Джерела
- ⭐ [Nikoli: Kuralin](https://www.nikoli.co.jp/en/puzzles/kuralin/) — 3 правила («blacken all cells that the line does not pass through», чорний/білий/сірий кружок), приклад 5×5 з ходом розвʼязання.
- [Nikoli: クラリン](https://www.nikoli.co.jp/ja/puzzles/kuralin/) — правила JA, «小さな丸» торкається довколишніх клітинок.
- [Janko: Nikoli № 191, № 5](https://www.janko.at/Raetsel/Nikoli/191.htm#5) — Kurarin, «Datum: 10. Juni 2025», назва неперекладна (Clarine), правила EN/DE/JA, 3 пазли.

## Непевне
- (?) Чи бувають кружки в центрі клітинки — у прикладі лише на ребрах і у вузлах; кружок у вузлі на краю поля торкався б 2 клітинок.
- (?) Цифрової реалізації (puzz.link, застосунки Nikoli) не знайшов; керування й вікна — гіпотетична цифрова версія.
- (?) Автора Janko не називає; рік — за датою огляду № 191 (червень 2025).
