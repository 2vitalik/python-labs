---
title: Strata
slug: strata
aka: []
family: connect-rotate
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2013
platforms: [iOS, Android, Windows Phone, PC (Windows, macOS, Linux)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/286380/Strata/", best: true, note: "мета «layer colored ribbons to match a pattern», Perfect без відкликання стрічки, 24 досягнення"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Strata_(video_game)", note: "розробник Graveck, дати iOS/Steam, платформи; верхній шар має збігтися з кольором клітини"}
  - {kind: other, url: "https://www.cultofmac.com/reviews/strata-review", note: "огляд: сітки 2×2…6×6, стрічка на кожен рядок і стовпець"}
  - {kind: other, url: "https://images.jayisgames.com/review/strata.php", note: "огляд: свайп від краю, лише верхня стрічка «торкається», палітра внизу, undo і рестарт"}
  - {kind: other, url: "https://www.pocketgamer.com/strata/review/", note: "огляд: нові набори додають рядок"}
  - {kind: other, url: "https://mashthosebuttons.com/2014/06/simplicity-and-challenge-meet-in-strata", note: "огляд PC-версії: порядок кладення"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Strata+Graveck+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [swipe-gestures, cell-click, satisfy-constraints, completion-detection, markup-validity, undo-step, restart-level, sequential-levels, level-select, level-bank, sound-effects, game-screen, +layer-order-paint, +line-stamp, +perfect-rating, +reverse-peel-solver]
proposes: ["+effect:lay_line(axis, i, color)", "+cond:top(cell, color)", "+card:layer-order-paint", "+card:line-stamp", "+card:reverse-peel-solver"]
author: opus
date: 2026-11-09
---

# Strata — клади кольорові стрічки в правильному порядку, щоб згори лежав потрібний колір

## Суть
Сітка з частиною кольорових клітин; гравець по одній кладе кольорові стрічки через **цілий рядок або стовпець**. Стрічки лягають одна на одну, і клітина «бачить» лише **верхню** — тож розвʼязок не в тому, які кольори обрати, а в **порядку кладення**: що ляже останнім, те й переможе на перетинах. Стрічки ще й переплітаються в красивий візерунок, а «Perfect» дається за розвʼязок без жодного відкликання стрічки. Цифровий пазл без паперового предка; за механікою — родич «принтера, що друкує лініями» (Strange Printer).

## Поле і час
- Квадратна сітка від 2×2 до 6×6 (огляд Cult of Mac), показана повернутою на 45° («slanted grid»); стрічки «вистрілюють» навскіс через екран.
- Кожен рядок і кожен стовпець отримує одну стрічку; клітина на перетині рядка i і стовпця j бачить ту з двох стрічок, яку поклали пізніше.
- Шари: клітини-цілі (колір або без кольору) + стос стрічок (порядок кладення).
- Час статичний: хід = покласти одну стрічку; ліміту часу нема.
- Наступні набори додають рядок або ще один колір стрічок.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кольорова клітина | mark | колір | верхня стрічка на ній мусить бути цього кольору |
| Клітина без кольору | static | — | будь-який верхній колір підходить (?) |
| Стрічка | tile | колір, вісь (рядок / стовпець), індекс, номер у стосі | покриває весь рядок/стовпець; кладеться поверх уже покладених |
| Палітра стрічок | static | доступні кольори | внизу екрана; з неї обирається колір наступної стрічки |
| Край сітки (слот) | static | рядок / стовпець | свайп або клік від краю кладе стрічку на цю лінію |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select_color)` → ТО `custom: «вибрати колір наступної стрічки з палітри»`.
- КОЛИ `input(swipe, edge_i)` → ЯКЩО `custom: «на лінії i ще нема стрічки»` → ТО `place(player, ribbon[color, line_i])` — стрічка стає верхньою на всіх клітинах лінії.
- КОЛИ `input(swipe, edge_i)` → ЯКЩО `custom: «на лінії вже є стрічка»` → ТО `block` (?) — чи можна перекласти лінію без відкликання, не перевірено.
- На перетині: клітина (i, j) показує стрічку з більшим номером у стосі — `custom: «верхня = пізніша з двох»`.
- КОЛИ `input(pull_back)` → ТО `undo(1)` — остання стрічка знімається; `custom: «Perfect для цієї сітки втрачено»`.
- КОЛИ `input(restart)` → ТО `restart`.
- КОЛИ `constraint_broken(top_color ≠ cell_color)` → ТО `sound`, `custom: «клітина лишається порожнистою (hollow)»` (?).
- КОЛИ `all_constraints_met` → ЯКЩО `cover_all(ribbon)` → ТО `win`, `next_level`.
- КОЛИ `all_constraints_met` → ЯКЩО `counter(pull_backs, ==, 0)` → ТО `custom: «Perfect»` — окремий лічильник досягнень (1, 10, 50, 100, 200 Perfect).
- Перемога: на кожній кольоровій клітині згори її колір, усі лінії покриті. · Поразки нема. · Рахунку нема, лише Perfect.

## Керування і ввід
- Тач: свайп від краю сітки вздовж рядка/стовпця — стрічка вилітає й лягає; на PC — мишею (клік/протяг від краю) (?).
- Вибір кольору — з палітри внизу (?) або колір закріплений за лінією (?).
- Кнопки: undo (по одній стрічці), швидкий рестарт.

## Вікна, меню, HUD
- `main-menu` → `level-select` наборів (тутор, Entwine, Flourish і ін.) → `puzzle-select` з позначками пройдено / Perfect (?).
- `game-screen`: повернута сітка, палітра стрічок, `undo-button`, `restart-button`.
- `end-screen` (?) — сітка зібрана, позначка Perfect.
- `settings-window` (?) — звук/музика.
- `tutorial-window` — навчальні сітки (досягнення «Complete Tutorial»).

## Фічі поза полем
- `levels-sequential` наборами зі зростанням розміру й кількості кольорів; «сотні» пазлів.
- `undo` по одному кроку, `restart-level`; `par-target`-подібне Perfect (0 відкликань).
- `achievements` (24 у Steam: Perfect-серії, завершення наборів), `cloud-save`.
- Звуки кладення стрічок як зворотний звʼязок («beautifully recorded»).

## Варіації й родичі
- Strange Printer / «Stamp the grid» — задачі про друк лініями з перекриттям; Nonogram — ті самі рядки/стовпці, але без шарів.
- У корпусі: [Flow Free](flow-free.md), [Infinity Loop](infinity-loop.md) — статичні мінімалістичні пазли; шарування — Tachiawase Block (перекриття фігур).
- Осі варіацій: **що кладеться** — лінія (Strata) / прямокутник / поліоміно · **хто видимий** — верхній шар / змішування кольорів (Trainyard) · **оцінка** — розвʼязано / Perfect без відкликань.

## Цікавинки для курсу
- Стос стрічок і функція «верхній колір клітини» (max номера з двох ліній) — 🌱.
- Перевірка розвʼязку і підсвітка порожнистих клітин — 🌱.
- Розвʼязувач «зворотним здиранням»: останньою може бути лише лінія, всі кольорові клітини якої вже її кольору або «звільнені»; знімай такі лінії, доки можна (топологічне сортування) — 🥉.
- Генерація: випадковий порядок і кольори ліній → пазл, перевірка єдиності розвʼязку — 🥇.
- Perfect: лічильник відкликань на рівень + досягнення-серії — 🌱.

## Мапа на каталог
- Є: `swipe-gestures` / `cell-click` ↔ кладення від краю; `satisfy-constraints` + `completion-detection` + `markup-validity` ↔ верхні кольори; `undo-step` + `restart-level` ↔ відкликання і рестарт; `sequential-levels` + `level-select` + `level-bank` ↔ набори зі зростанням сітки й кольорів; `sound-effects`; `game-screen`.
- **Нема** → пропозиції карток:
  - `+layer-order-paint` «Шари: клітина бачить останній покладений» · game-logic/constraints · 🥉.
  - `+line-stamp` «Хід покриває весь рядок або стовпець» · entities/interact · 🌱.
  - `+perfect-rating` (Flow Free) — Perfect за розвʼязок без відкатів.
  - `+reverse-peel-solver` «Розвʼязувач зворотним зняттям верхнього шару» · levels/solvability · 🥉.

## Пропозиції до словників
- `+effect:lay_line(axis, i, color)` — покласти лінію-шар через рядок/стовпець (зараз — `place` з аргументом-лінією).
- `+cond:top(cell, color)` — верхній шар клітини має колір (умова розвʼязку шарових пазлів).
- `+card:layer-order-paint`, `+card:line-stamp`, `+card:reverse-peel-solver` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Strata](https://store.steampowered.com/app/286380/Strata/) — мета, порядок ходів, Perfect «without pulling a ribbon back», «hundreds» пазлів; через appdetails — 24 досягнення (набори Entwine, Flourish), видавець GLITCH, дата 29.05.2014.
- [Wikipedia: Strata (video game)](https://en.wikipedia.org/wiki/Strata_(video_game)) — Graveck, iOS 12.09.2013, Steam Greenlight, платформи, Unity.
- [Cult of Mac](https://www.cultofmac.com/reviews/strata-review) — сітки 2×2…6×6, стрічки через кожен рядок і стовпець, верхня стрічка = колір клітини.
- [JayIsGames](https://images.jayisgames.com/review/strata.php) — свайп від краю, «only the topmost piece counts», палітра внизу, undo по кроку, рестарт.
- [Pocket Gamer](https://www.pocketgamer.com/strata/review/) · [Mash Those Buttons](https://mashthosebuttons.com/2014/06/simplicity-and-challenge-meet-in-strata) — нові набори додають рядок; стрічки навскіс; порядок.
- YouTube: пошук «Strata Graveck gameplay».

## Непевне
- (?) Чи кожна лінія **мусить** бути покрита, чи достатньо кольорових клітин (Cult of Mac: «across every row and column»).
- (?) Клітини без кольору — будь-який колір чи окремий нейтральний; чи кількість стрічок кожного кольору обмежена палітрою.
- (?) «Порожнисті» клітини до правильного розміщення і звуковий сигнал помилки — лише з пошукового резюме оглядів, сторінку не відкрив.
- (?) Чи можна перекласти лінію поверх власної стрічки; керування мишею на PC; назви всіх наборів.
- Рядок черги: рік 2014 — це Steam-реліз; оригінал iOS — 2013.
