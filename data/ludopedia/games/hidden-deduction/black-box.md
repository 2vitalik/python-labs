---
title: Black Box (Чорна скринька)
slug: black-box
family: hidden-deduction
also: [connect-rotate, pencil-logic]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 1977
platforms: [board (Waddingtons, Parker Brothers), BBC Micro (Acornsoft 1984), Acorn Atom, ZX81, GNU Emacs (blackbox.el 1985), Simon Tatham's Puzzles (PC, web, mobile)]
links:
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/blackbox.html", best: true, note: "Tatham: правила променів, керування, перевірка, параметри (розмір, кількість куль або діапазон)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Black_Box_(game)", note: "Eric Solomon, 8×8, hit/deflection/reflection/detour, рахунок і штрафи, комп'ютерні версії"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=black+box", note: "пошук BGG; видання Waddingtons/Parker"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=black+box+eric+solomon+game", note: "пошук; пояснення променів"}
stage: v1
coverage: 75
mechanics: [cell-click, hover-highlight, satisfy-constraints, completion-detection, event-points, difficulty-levels, game-settings, field-size-picker, game-screen, end-screen, help-window, hot-seat, level-solver, +ray-probe, +ray-deflection, +edge-ray-markers, +probe-cost-score, +counterexample-hint, +lock-cell]
proposes: ["+trigger:probe", "+cond:ray_consistent", "+effect:trace_ray", "+effect:reveal", "+effect:mark", "+role:mark", "+ui:edge-ports", "+ui:ray-pair-label", "+ui:guess-counter", "+feature:counterexample-check", "+feature:lock-cells", "+card:ray-probe", "+card:ray-deflection", "+card:edge-ray-markers", "+card:probe-cost-score", "+card:counterexample-hint", "+card:lock-cell"]
author: opus
date: 2026-11-02
---

# Black Box — знайди приховані атоми в коробці 8×8, стріляючи променями з країв і дивлячись, де вони виходять

## Суть
У квадратній «скриньці» сховано кілька атомів (куль). Гравець запускає промінь з будь-якої з 32 крайових позицій і дізнається лише результат: поглинено (H), повернувся туди ж (R) або вийшов в іншому місці (пара позначена однаковим числом). Атоми поблизу шляху відхиляють промінь на 90°, тож кожен постріл — нелінійний «запит» до прихованого стану. Мета — розставити гіпотези й перевірити їх, витративши якомога менше променів; при 5+ атомах частина позицій принципово невизначна.

## Поле і час
- Поле W×H (класика 8×8) + рамка з 2·(W+H) крайових портів (8×8 → 32), кожен порт — і вхід, і вихід.
- Шари: приховані атоми · гіпотези гравця (маркери) · позначки на портах (H / R / номер пари).
- Покроково: хід = один промінь або зміна гіпотези; часу нема. Наприкінці — одна перевірка (настолка) або перевірка з контрприкладом (Tatham).
- Настолка: двоє гравців — «ховач» таємно ставить атоми на свою дошку й трасує промені, «шукач» питає; потім міняються ролями.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Атом (куля) | object | позиція, прихований | поглинає промінь «в лоб», відхиляє той, що йде повз діагонально |
| Промінь (laser) | projectile | порт входу, напрям | іде прямо; поглинається / повертає на 90° / розвертається |
| Крайовий порт | static | сторона, індекс | клік = запуск; показує результат H / R / число |
| Мітка H (hit) | mark | — | промінь поглинено |
| Мітка R (reflection) | mark | — | промінь вийшов через той самий порт |
| Мітка-число (detour) | mark | номер пари | вхід і вихід позначено одним числом |
| Гіпотеза атома | mark | — | чорне коло гравця всередині поля; клік ще раз — прибрати |
| Замок клітини / ряду | mark | — | (Tatham) захист від випадкової зміни |
| Кнопка перевірки | static | зʼявляється при допустимій кількості гіпотез | (Tatham) верхній лівий кут поля |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(fire, port)` → ТО `custom: «trace_ray: рухати промінь крок за кроком від порту в поле»`, `score(+1)` за кожен новий позначений порт (настолка).
- На кожному кроці променя:
  - ЯКЩО `occupied(ahead, atom)` → ТО поглинання: `mark(port, H)`; кінець (пріоритет над відхиленням).
  - ЯКЩО атом діагонально попереду ліворуч і праворуч одночасно → ТО `bounce(ray)` (розворот на 180°).
  - ЯКЩО атом діагонально попереду ліворуч → ТО `rotate(ray, right 90)`; праворуч → `rotate(ray, left 90)`.
  - Інакше → `move(ray, ahead)`.
- Крайовий випадок: КОЛИ промінь лише входить і атом стоїть діагонально біля порту (у першому ряду поруч з лінією входу) → ТО `mark(port, R)` ще до входу.
- КОЛИ `edge(ray)` → ЯКЩО вихід = вхідний порт → ТО `mark(port, R)`; інакше `mark(entry, n)`, `mark(exit, n)` — нове число пари.
- Промінь може відхилятися багато разів; «прохід навиліт» без атомів — теж detour з номером.
- КОЛИ `input(toggle_guess, cell)` → ТО `mark(cell, atom)` / `unmark(cell)`.
- Настолка, рахунок: кожен позначений порт = 1 очко (H і R — 1, detour — 2); КОЛИ перевірка → ТО за кожну неправильну гіпотезу `score(+5)` (Parker Brothers, комп'ютерні) або `score(+10)` (Waddingtons); менший рахунок перемагає.
- Tatham, перевірка: КОЛИ `input(check)` → ЯКЩО гіпотези суперечать уже запущеним променям → ТО `custom: «обвести один такий промінь як доказ»`; ЯКЩО узгоджені, але неправильні → ТО `custom: «показати червоним новий промінь, який гіпотеза передбачає хибно»`; ЯКЩО правильні (або інший набір, що дає ті самі результати всіх променів) → ТО `win`.
- Tatham «Solve»: правильні — чорні кола, хибні — чорні з червоним хрестом, пропущені — червоні кола; суперечливі промені обведено; червоним текстом — промінь, який розрізнив би гіпотезу й відповідь.
- Перемога: знайти всі атоми · Поразка: нема (лише гірший рахунок) · Рахунок: промені + штрафи (настолка); Tatham — без очок.

## Керування і ввід
- Лівий клік по порту — запустити промінь; клік/утримання на результаті — підсвітити парний вихід.
- Лівий клік у полі — поставити/прибрати гіпотезу атома.
- Правий клік по клітині — заблокувати її; по порту біля ряду/стовпця — заблокувати весь ряд/стовпець (Tatham).
- Клавіатура (Tatham): стрілки — курсор, Enter — промінь/гіпотеза, Space — замок.
- Кнопка перевірки зʼявляється, коли кількість гіпотез у допустимому діапазоні.

## Вікна, меню, HUD
- `game-screen`: поле з рамкою портів (`edge-ports`), мітки H/R/числа (`ray-pair-label`), гіпотези-кола, `check-button` у кутку; підсвітка пари вхід–вихід при наведенні.
- Меню Tatham (спільне для колекції): Game (New, Restart, Undo/Redo, Solve, Load/Save, Exit) · Type (пресети + Custom… → `settings-window`: Width, Height, No. of balls «4» або «2-6») · Help → `help-window`.
- HUD (цифрова версія з рахунком): `score` (кількість портів), `guess-counter` «поставлено 3 з 4».
- `end-screen` / статус-рядок: «You got it!» або розкриття з позначками помилок.
- Hotseat-настолка (цифрова версія): `pass-device` між ролями ховача й шукача (?).
- Переходи: game-screen → Type → нова гра; game-screen → Solve → розкритий стан → New.

## Фічі поза полем
- `custom-difficulty`: розмір поля, кількість атомів або діапазон (тоді гравець не знає точної кількості).
- `undo`/`redo` (Tatham) для гіпотез і променів (?), `restart-level`, `save-slots` через Load/Save, `seed-input` (Tatham game ID).
- `counterexample-check`: перевірка не просто «так/ні», а видає промінь-контрприклад — унікальна фіча.
- `lock-cells`: заморозити клітину/ряд, щоб не змінити випадково.
- Настолка: два гравці, ролі міняються, рахунок як у гольфі.

## Варіації й родичі
- Видання: Waddingtons (Велика Британія, 1977), Parker Brothers (США); комп'ютерні — Acornsoft BBC Micro (Ben Finn, 1984), ZX81 (Microhobby, 1985), Emacs `blackbox.el` (F. Thomas May, 1985), Tatham (внесок James Harvey).
- Більші поля 10×10, 12×12; 5+ атомів (частина позицій нерозрізнена — гра визнає будь-яку сумісну відповідь у Tatham).
- Родичі з дзеркалами й призмами: GFingerPoken (GNOME), секція System's Twilight (Mac).
- **Осі варіацій**: результат променя «H / R / пара» → «лише вийшов чи ні» → «вихід + довжина шляху»; перешкода «атом-відхилювач / дзеркало / призма»; кількість атомів «відома / діапазон»; перевірка «одна, зі штрафом / необмежена з контрприкладом».
- Родичі за ідеєю: Battleship (запит-клітина → відповідь), Mastermind (запит → агрегований відгук), Deflektor (промені з відбиттям, але видимі).

## Цікавинки для курсу
- Трасування променя з правилами «в лоб / діагонально / обидві діагоналі / край» — 🥉 (крок-автомат з пріоритетами і крайовим випадком).
- Рамка портів навколо поля з парними мітками й підсвіткою пари — 📎.
- Перевірка гіпотези через повторне трасування всіх променів по гіпотетичному полю — 🥉.
- Контрприклад: знайти промінь, що розрізняє гіпотезу й відповідь (перебір 2(W+H) портів) — 🥉.
- Розвʼязувач/генератор: чи визначають запущені промені розміщення однозначно (перебір C(64,4) ≈ 635 тис.) — 🥇.
- Рахунок «гольфом»: промені + штраф за хибний атом — 🌱.

## Мапа на каталог
- Є: `cell-click` (порт, гіпотеза) · `hover-highlight` (пара вхід–вихід) · `satisfy-constraints` + `completion-detection` (перевірка) · `event-points` (рахунок) · `difficulty-levels` + `game-settings` + `field-size-picker` · `level-solver` (Solve) · `hot-seat` (настолка удвох) · `game-screen` / `end-screen` / `help-window`.
- **Нема** → пропозиції карток:
  - `+ray-probe` «Промінь-запит з краю» · entities/combat · 🥉 · слот {outcomes: hit|reflect|exit-pair}.
  - `+ray-deflection` «Відхилення променя сусідньою перешкодою» · entities/interact · 🥉 · слот {rule: diagonal-90|mirror|prism}.
  - `+edge-ray-markers` «Мітки портів на рамці поля» · interface/hud · 📎.
  - `+probe-cost-score` «Рахунок за кількість запитів і штраф за помилку» · game-logic/score · 🌱.
  - `+counterexample-hint` «Перевірка з контрприкладом» · levels/solvability · 🥉.
  - `+lock-cell` «Замок клітини/ряду» · interface/input · 🌱.

## Пропозиції до словників
- `+trigger:probe` — гравець запустив запит (промінь, постріл, спроба коду) у приховане поле; спільне для Battleship/Mastermind/Black Box.
- `+cond:ray_consistent` — гіпотеза дає ті самі результати променів, що й справжнє поле.
- `+effect:trace_ray` — прокласти промінь за правилами відхилення й повернути результат (не `move`, бо миттєвий і з результатом).
- `+effect:reveal` / `+effect:mark` — ⏳, тут основні.
- `+role:mark` — мітки H/R/числа, гіпотези.
- `+ui:edge-ports` — клікабельна рамка навколо поля; `+ui:ray-pair-label` — однакове число на вході й виході; `+ui:guess-counter` — «поставлено N з M».
- `+feature:counterexample-check` — перевірка, що пояснює, чому неправильно; `+feature:lock-cells` — заморозка розмітки.

## Джерела
- ⭐ [Simon Tatham's Puzzles: Black Box](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/blackbox.html) — точні правила променів, керування, перевірка з контрприкладом, Solve, параметри.
- [Wikipedia: Black Box (game)](https://en.wikipedia.org/wiki/Black_Box_(game)) — Eric Solomon, 8×8, 32 порти, типи результатів, рахунок і штрафи 5/10, комп'ютерні версії, варіанти з дзеркалами.
- [BGG пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=black+box) — видання.
- YouTube: пошук «black box eric solomon game».

## Непевне
- (?) Рік: Tatham — Waddingtons 1977, Wikipedia — «середина 1970-х», категорія 1977; бриф куратора — 1976. Взято 1977.
- (?) Рахунок «detour = 2» — бо позначаються два порти; у Wikipedia так і сказано, але чи вважаються «прохід навиліт» і detour однаково — так за логікою портів.
- (?) Чи Undo в Tatham відкочує запущений промінь — колекція має спільний Undo, але для Black Box не перевірено.
- (?) Hotseat у цифрових версіях — невідомо, чи є.
