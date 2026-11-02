---
title: Sumplete
slug: sumplete
family: word-number
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: 2023
platforms: [web]
links:
  - {kind: play, url: "https://sumplete.com/", best: true, note: "грати; правила одним абзацом, туторіал, Daily 5×5/7×7, Unlimited 3×3–9×9"}
  - {kind: official, url: "https://sumplete.com/about/", note: "історія: Daniel Tait і ChatGPT, 3 березня 2023"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=sumplete+chatgpt+puzzle", note: "пошук; огляди й розвʼязки"}
stage: v1
coverage: 80
mechanics: [cell-click, satisfy-constraints, markup-validity, completion-detection, pencil-marks, daily-puzzle, difficulty-levels, field-size-picker, profile-stats, leaderboard, end-screen, game-screen, help-window, save-progress, unique-puzzle-generation, level-solver, +subset-sum-lines, +line-auto-complete, +tri-state-mark, +share-result, +streak-stats]
proposes: ["+trigger:input", "+trigger:all_constraints_met", "+cond:sum_equals", "+effect:mark", "+effect:flash", "+role:mark", "+ui:line-target", "+ui:timer-elapsed", "+ui:undo-button", "+window:mode-select", "+feature:undo", "+feature:share-result", "+feature:streaks", "+feature:custom-difficulty", "+axis:session"]
author: opus
date: 2026-11-02
---

# Sumplete — викресли числа так, щоб кожен рядок і стовпець дав свою суму

## Суть
Поле n×n заповнене числами; праворуч від кожного рядка і під кожним стовпцем — цільова сума. Гравець викреслює числа, доки суми залишених у кожному рядку й стовпці не дорівнюватимуть цілям. Це «олівцева логіка з арифметикою»: кожен рядок — задача subset-sum, а перетини рядків і стовпців звʼязують їх у систему. Гра відома походженням: Daniel Tait попросив ChatGPT вигадати новий пазл, і той з четвертої спроби запропонував «Sum Delete puzzle» та згенерував робочу браузерну версію.

## Поле і час
- Квадрат n×n, n = 3…9 (Unlimited), щоденні — 5×5 і 7×7.
- Шари: числа (фіксовані) + розмітка гравця (порожньо / викреслено / залишено) + цілі по краях.
- Час статичний; секундомір 00:00.00 рахує швидкість розвʼязку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина-число | mark | значення, стан unknown/deleted/kept | стан перемикається кліком по колу |
| Ціль рядка / стовпця | static | сума | клік → автодомальовування решти клітин лінії; світиться, коли сума збігається |
| Ціль 0 | static | 0 | клік → усі клітини лінії викреслено |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click cell)` → ТО `mark(cell, next_state)` за колом unknown → deleted (червоний хрестик) → kept (зелене коло) → unknown.
- КОЛИ `after(mark)` → ЯКЩО `sum_equals(line, target)` (сума не викреслених) → ТО `flash(line)` — лінія підсвічується як виконана.
- КОЛИ `input(click target)` → ТО `custom: «решта unknown-клітин лінії автоматично позначаються»` (на сайті: «auto-marks the remaining blank cells»).
- КОЛИ `input(click target)` → ЯКЩО `target == 0` → ТО `mark(all cells in line, deleted)`.
- КОЛИ `all_constraints_met` (усі 2n ліній зійшлись) → ТО `win`, `window(end-screen)` з часом і кнопкою Share Score.
- Позначка «kept» необовʼязкова: перевірка дивиться лише на викреслені — kept і unknown рахуються однаково (сайт: «circles are optional but helpful for marking definite keeps»).
- Перевірка за сумами, а не за ключем — будь-яке розмічення, що дає всі суми, зараховується (?).
- Генерація: випадкова сітка → випадковий набір викреслених → цілі як суми залишку; складність через розмір і діапазон чисел (на hard — і відʼємні числа (?)).
- Перемога: всі суми збіглися · Поразки нема · Рахунок: час, серія днів.

## Керування і ввід
- Клік/тап по клітині — цикл трьох станів (`mode-toggle` не потрібен: один жест, три стани).
- Клік по цілі — автодомальовування лінії.
- Кнопки Clear (скинути все) і Undo.

## Вікна, меню, HUD
- `game-screen`: сітка, цілі праворуч і знизу (`line-target`, світяться при збігу), секундомір, Clear, Undo.
- `mode-select`: Daily 5×5 · Daily 7×7 · Unlimited (розмір 3–9 + складність).
- `end-screen`: час, Share Score, «Try Daily 5×5» / «Play Daily 7×7 #N».
- `help-window` / `tutorial-window`: Watch Tutorial, правила одним абзацом.
- `stats-window`: Played, Current/Best streak; з акаунтом — час, лідерборд, архів, синхронізація.
- Переходи: старт → Start Game / Play Now → `game-screen` → `end-screen` → інший режим.

## Фічі поза полем
- `daily-puzzle` (5×5 і 7×7 з номером), `custom-difficulty` у Unlimited, `undo`, `stats`/`streaks`, `share-result`, `leaderboard-online` і архів пазлів для акаунта, `cloud-save` (cross-device sync), `invite-link` («Invite a friend»).

## Варіації й родичі
- Kakurasu (Nikoli-подібний: зафарбувати клітини, щоб зважені суми рядків/стовпців збіглися), Kakuro (суми в регіонах), Rullo (мобільна гра 2010-х: вимикати числа, щоб суми рядків/стовпців дали ціль) (?) — тому «оригінальність» ChatGPT-ідеї сумнівна.
- Hitori (викреслювати клітини за правилами повторів) — та сама дія «delete», інше обмеження.
- **Осі варіацій:** операція лінії (сума / добуток / зважена сума) · знак чисел (лише додатні / з відʼємними) · додаткові обмеження (заборона сусідніх викреслень, звʼязність залишку) · форма (квадрат / регіони замість ліній).

## Цікавинки для курсу
- Валідатор і підсвітка ліній, цикл трьох станів клітини — 🌱.
- Генератор: випадкова маска → цілі; гарантувати єдиність розвʼязку перебором — 🥉 (n ≤ 5) / 🥇 (n = 9 з відсіченням).
- Солвер: для кожної лінії перелік підмножин із потрібною сумою, перетин кандидатів рядків і стовпців (propagation) + backtracking — 🥇.
- Дедуктивні правила як підказка («число більше за ціль — точно викреслити», «сума всіх = ціль — усі залишити») — 📎.
- Історія з ChatGPT як кейс: генеративна модель «вигадала» пазл, що вже існував, — тема для обговорення, не код — 🌱.

## Мапа на каталог
- Є: `cell-click` · `satisfy-constraints` · `markup-validity` ↔ лінія світиться · `completion-detection` · `pencil-marks` ↔ «kept»-кружки як позначка-нотатка · `daily-puzzle` · `difficulty-levels` · `field-size-picker` ↔ 3–9 · `profile-stats` · `leaderboard` · `save-progress` ↔ серії · `end-screen` · `game-screen` · `help-window` · `unique-puzzle-generation` · `level-solver`.
- **Нема** → пропозиції карток:
  - `+subset-sum-lines` «Залишити в кожній лінії підмножину з потрібною сумою» · game-logic/constraints · 📎 · слоти {op: sum|product}.
  - `+line-auto-complete` «Клік по цілі домальовує лінію» · interface/input · 🌱.
  - `+tri-state-mark` «Цикл станів клітини одним кліком» · interface/input · 🌱 · слоти {states: list}.
  - `+share-result`, `+streak-stats` — див. wordle.md.

## Пропозиції до словників
- `+trigger:input`, `+trigger:all_constraints_met` (⏳).
- `+cond:sum_equals` — сума залишених у лінії = ціль.
- `+effect:mark` (⏳), `+effect:flash` (⏳).
- `+role:mark` (⏳).
- `+ui:line-target` — ціль лінії на краю, що світиться при виконанні (Sumplete, Picross-підказки, Kakurasu); `+ui:timer-elapsed`, `+ui:undo-button` (⏳).
- `+window:mode-select` (⏳).
- `+feature:undo`, `+feature:share-result`, `+feature:streaks`, `+feature:custom-difficulty` (⏳).
- `+axis:session` — `daily` + `endless` (Unlimited).

## Джерела
- ⭐ [sumplete.com](https://sumplete.com/) — грати; правила, керування (цикл станів, клік по цілі), режими, статистика.
- [sumplete.com/about](https://sumplete.com/about/) — як ChatGPT «вигадав» гру (Daniel Tait, 03.03.2023).
- YouTube: пошук «sumplete chatgpt puzzle».

## Непевне
- Wikipedia статті не має, WebSearch вичерпано — родичі й складність записані з памʼяті.
- (?) Rullo як попередник і назва Kakurasu як найближчого Nikoli-родича; дискусія про «неоригінальність» — з памʼяті.
- (?) Чи гарантує генератор єдиний розвʼязок; перевірка за сумами означає, що альтернативний розвʼязок теж зарахується.
- (?) Відʼємні числа на високій складності; доведення NP-повноти Sumplete — пригадується, не перевірено.
