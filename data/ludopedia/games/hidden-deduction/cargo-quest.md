---
title: Cargo Quest
slug: cargo-quest
aka: []
family: hidden-deduction
also: [roguelike]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: setup
  goal: score
year: 2026
platforms: [web (itch.io, HTML5), mobile browser]
links:
  - {kind: itch, url: "https://kyuroguneiro.itch.io/cargo-quest", best: true, note: "грати в браузері; опис: три кошики GOOD/HOLD/BAD, лічильники рядків і стовпців, перо-підказка, ✓-ящик, сортування наосліп ×2, скан, 5 сердець, трюм 5×5 → 8×8"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cargo+Quest+kyuroguneiro+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cell-click, drag-drop-piece, line-sum-clue, neighbor-count-clue, hp-damage, player-death, event-points, weighted-spawn, sequential-levels, save-progress, codex-window, tutorial-window, main-menu, game-screen, end-screen, language-picker, sound-effects, +sort-into-bins, +category-line-counts, +blind-commit-bonus, +live-recount-clue, +safe-start-cell, +ambiguous-cell, +scan-charges, +streak-milestone-bonus, +growing-board]
proposes: ["+effect:sort_into", "+ui:odds-preview", "+ui:streak-counter", "+ui:bins", "+card:sort-into-bins", "+card:category-line-counts", "+card:blind-commit-bonus", "+card:live-recount-clue", "+card:safe-start-cell", "+card:ambiguous-cell", "+card:scan-charges", "+card:streak-milestone-bonus"]
author: opus
date: 2026-11-09
---

# Cargo Quest — розклади закриті ящики підземелля по кошиках GOOD / HOLD / BAD за лічильниками рядків і стовпців; наосліп — подвійно

## Суть
Сапер-роглайт від Kyuroguneiro: на кожному поверсі трюм n×n **закритих** ящиків, і кожен треба кинути в один із трьох кошиків — GOOD, HOLD або BAD. Головна підказка — **лічильники на краях**: скільки GOOD/HOLD/BAD ще лишилось у кожному рядку й стовпці, тобто «сапер за категоріями», а не за мінами. Відкрити ящик можна, але червоний вантаж кусає (−1 серце); кинутий **не відкритим** правильний ящик дає подвійну масу, тож гра винагороджує дедукцію замість підглядання. Пройшов поверх — трюм росте від 5×5 до 8×8, зʼявляються нові предмети.

## Поле і час
- Квадратне поле n×n: поверхи 1–2 — 5×5, 3–5 — 6×6, 6–8 — 7×7, з 9-го — 8×8 («трюм росте поступово»).
- Над рядками й стовпцями — трійки чисел G/H/B: скільки предметів кожного типу ще лежить у лінії; лінія, де все розкладено, гасне.
- Під полем — три кошики; поруч — панель шансів невідомого вантажу (скільки й який % кожного типу серед ще невідомих).
- Час не тисне (`time: static`); хід = відкрити, просканувати або кинути ящик. Кожен поверх генерується з сіду забігу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закритий ящик 📦 | tile | печатка ціла / зламана, скановано | будь-який предмет; тап — відкрити, перетягнути в кошик — кинути |
| Мішок трав 🌿 | pickup | GOOD, маса 3 (наосліп 6) | звичайний безпечний вантаж |
| Перо розвідника 🪶 | mark | GOOD, число 0–8 | скільки BAD **ще лежить** серед 8 сусідів; зменшується, коли BAD іде з поля; ⓪ = усі сусіди безпечні |
| Цілюща трава 🍀 | pickup | GOOD, з 7-го поверху, рідко | +1 серце, лише якщо кинута в GOOD з цілою печаткою; відкрита — вʼяне |
| Сувій 📜 | pickup | HOLD, маса 2 (наосліп 4) | «ні добре, ні погано» — причина існування середнього кошика |
| Монета-череп 💀 | hazard | BAD, маса 1 (наосліп 2) | відкрити = −1 серце |
| Червоний кристал 💎 | hazard | BAD, з 4-го поверху | відкрити = −1 серце |
| Перстень 💍 | tile | HOLD або BAD (50/50), з 4-го поверху | відкриття нічого не каже; скан показує ауру (бурштин = HOLD, червона = BAD) |
| Скриня-пастка 🧰 | hazard | BAD | відкрити = −1 серце; закрита в BAD — +4, відкрита в BAD — +3; закрита не в той кошик — пастка −1 |
| ✓-ящик | tile | один на поверх | гарантовано безпечний: завжди перо з ⓪ |
| Кошики GOOD / HOLD / BAD | zone | — | приймають ящик; перевіряють тип |
| Лічильник лінії | mark | G/H/B для рядка й стовпця | зменшується, коли ящик цього типу йде з лінії |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «мішок предметів за вагами поверху (трави 20, пера 12, сувої 18, черепи 15, скрині 5; з 4-го — кристали, персні; з 7-го — цілюща трава) → n×n закритих ящиків; пер ≥ 2, скринь ≥ 1»`, `custom: «перстень стає HOLD або BAD 50/50»`.
- КОЛИ `level_start` → ТО `custom: «вибрати перо з найменшою кількістю BAD довкола, обміняти BAD/персні/цілющу траву з його 3×3 на трави чи сувої з-поза зони»`, `mark(that_feather, ✓)` — гра його не відкриває, перший хід за гравцем.
- КОЛИ `input(tap, crate)` → ЯКЩО `state(crate, sealed)` і `not state(crate, scanned)` → ТО `reveal(crate)`, `clear_state(crate, sealed)`.
- … ЯКЩО `same(crate, BAD, type)` і `custom: «не перстень»` → ТО `damage(player, 1)` («IT BITES!», для кристала — «CRACKED!», для скрині — «TRAPPED!»).
- … ЯКЩО `custom: «перстень»` → ТО `custom: «тип лишається невідомим; ставка ×2 зберігається»`.
- … ЯКЩО `custom: «перо»` → ТО `set_value(crate, adjacent_count(crate, BAD, on_board))`; ЯКЩО `adjacent_count(crate, BAD, ==, 0)` → ТО `flash(neighbors8, safe)`.
- КОЛИ `input(scan, crate)` → ЯКЩО `counter(scans, >, 0)` і `not state(crate, scanned)` → ТО `counter(scans, -1)`, `reveal(crate)`, `set_state(crate, scanned)` — печатка ціла, нічого не кусає, перстень показує ауру.
- КОЛИ `input(drag, crate → bin)` → ЯКЩО `same(crate, bin, type)` → ТО `disappear(crate)` (`+effect:sort_into`), `score(mass[type] × 2, якщо ящик не відкривали або це несканований перстень; інакше × 1)`, `combo(+1)`.
- … інакше → ТО `disappear(crate)` (ящик однаково йде з поля), `damage(player, 1)`, `reset_combo`, `message(«<предмет> was <ТИП>»)`.
- Скриня: КОЛИ `input(drag, chest → BAD)` → ТО `score(4)`, якщо `state(chest, sealed)`, інакше `score(3)`; ЯКЩО кошик не BAD і `state(chest, sealed)` → ТО `damage(player, 1)` («пастка спрацювала в кошику»).
- Цілюща трава: КОЛИ `input(drag, aid → GOOD)` → ЯКЩО `state(aid, sealed)` → ТО `heal(player, 1)` (не більше 5).
- КОЛИ `after(disappear crate)` → ТО `counter(row_left[type], -1)`, `counter(col_left[type], -1)`; ЯКЩО тип BAD → ТО `custom: «кожне сусіднє перо перераховує число»`.
- КОЛИ `counter(streak, ==, 5k)` → ТО `score(min(streak, 10))` («STREAK ×N!»).
- КОЛИ `counter(sorted, ==, n×n)` → ТО `next_level`; ЯКЩО `counter(floor_mistakes, ==, 0)` → ТО `score(10)` («FLAWLESS»).
- КОЛИ `level_start` (новий поверх) → ТО `counter(scans, +1)` (старт 3, максимум 6); ЯКЩО `level(% 3, ==, 0)` → ТО `heal(player, 1)`.
- КОЛИ `hp_zero(player)` → ТО `game_over`, `window(end-screen)`.
- Перемоги нема (глибина забігу) · Поразка: 0 сердець · Рахунок: маса вантажу + бонуси серії й «FLAWLESS»; рекорд — найглибший поверх.

## Керування і ввід
- Тап/клік по закритому ящику — відкрити.
- Перетягнути ящик у кошик — кинути (з печаткою або без); або утримати ящик і тапнути кошик.
- Кнопка 🔍 SCAN вмикає режим скану (світяться ящики, які можна сканувати), тап — сканувати.
- 📖 — Книга гільдії: довідник предметів, мова (EN / TH), звук; Esc закриває. Миша й тач, на телефоні — портретна орієнтація.

## Вікна, меню, HUD
- `main-menu` (титул): PLAY, CONTINUE — FLOOR n (якщо є збереження), коротке «як грати».
- `game-screen`: поле з `line-clue` над рядками/стовпцями, три кошики (`+ui:bins`), `lives` (серця), лічильник сканів (`ability-buttons`), маса (`score`), поверх (`level-number`), найкращий поверх (`hi-score`), кнопка звуку; `+ui:odds-preview` — «UNKNOWN CARGO — N LEFT» зі смугами G/H/B; `+ui:streak-counter` — «🔥 STREAK ×N»; `popup-text` («SEALED ×2! +6», «WRONG! −1 HP»); банери «FLOOR n CLEAR!», «NEW CARGO BELOW!», «THE HOLD GROWS!».
- `codex-window` — Книга гільдії: усі предмети з типом і масою, правила скану, лічильників і сердець; там же мова і звук.
- `tutorial-window` — картка-підказка при першій зустрічі кожного предмета (і при першому кидку наосліп).
- `end-screen` — «💔 RUN OVER»: досягнутий поверх, маса, найкращий поверх, RETRY.

## Фічі поза полем
- `continue` — продовження з початку поточного поверху (знімок стану на старті поверху в сховищі браузера); `stats` — найкращий поверх.
- `onboarding-hints` — картки першої зустрічі; `rules-page` — Книга гільдії; `localization` (EN, тайська); `sound-toggle`; `touch-controls`.
- Прогресія без мети: нові предмети на 4-му і 7-му поверхах, трюм росте, скринь і перснів більшає з глибиною.

## Варіації й родичі
- «Кожна клітина закрита, пріоритет — дедукція, помилка коштує HP» — як [dragonsweeper](dragonsweeper.md) і [dungeon-squire](dungeon-squire.md) (автор прямо посилається на Dragonsweeper у коді).
- Лічильники рядків і стовпців — [voltorb-flip](voltorb-flip.md) (сума й кількість бомб у лінії), [minesweeper-genius](minesweeper-genius.md), [tametsi](tametsi.md); живе перерахування підказок — [venom-sweep](venom-sweep.md).
- **Осі варіацій:** що ховається — міна / монстр із силою / одна з трьох категорій; що робить гравець — відкриває / відкриває й бʼється / **класифікує**; підказка — сусіди / лінії / лінії за категоріями; ціна інформації — безкоштовна / серце / заряд скану; винагорода за ризик — нема / ×2 за кидок наосліп.

## Цікавинки для курсу
- Лічильники ліній за трьома категоріями, що зменшуються після кожного кидка — 🌱.
- Панель шансів: сума лінійних лічильників мінус відомі клітини → % кожного типу серед невідомих — 🌱.
- Кидок наосліп ×2 і окрема ідея «печатки»: скан бачить, але не ламає печатку — 📎.
- Перо, що рахує лише ще не прибрані BAD (жива підказка) — 🌱.
- Генерація з гарантіями: ваги за поверхом, найбільший залишок, мінімум пер і скринь, ✓-перо з чистою зоною 3×3 — 🥉.
- Перстень-«неоднозначність», що розкривається лише сканом — 🌱.
- Розвʼязувач/оцінювач: чи можна розкласти поверх без жодного відкриття, лише за лічильниками й пером — 🥇.

## Мапа на каталог
- Є: `cell-click` ↔ відкрити; `drag-drop-piece` ↔ кинути в кошик; `line-sum-clue` ↔ лічильники ліній; `neighbor-count-clue` ↔ перо; `hp-damage` + `player-death` ↔ серця; `event-points` ↔ маса за типом; `weighted-spawn` ↔ ваги предметів; `sequential-levels` ↔ поверхи; `save-progress` ↔ продовження з поверху; `codex-window` ↔ Книга гільдії; `tutorial-window` ↔ картки першої зустрічі; `main-menu`, `game-screen`, `end-screen`; `language-picker` ↔ EN/TH; `sound-effects`.
- **Нема** → пропозиції карток:
  - `+sort-into-bins` «Кожну приховану клітину треба віднести до однієї з категорій-кошиків» · game-logic/win · 📎 · слот {bins: 3}.
  - `+category-line-counts` «Лічильники ліній окремо для кожної категорії» · game-logic/constraints · 🌱 — дитина `line-sum-clue`.
  - `+blind-commit-bonus` «Подвійна винагорода за правильну дію без підглядання» · game-logic/score · 🌱.
  - `+live-recount-clue` «Підказка рахує лише те, що ще на полі» · game-logic/constraints · 📎 (пропонується і з Venom Sweep).
  - `+safe-start-cell` «Позначена гарантовано безпечна стартова клітина» · levels/generation · 📎.
  - `+ambiguous-cell` «Клітина, яку відкриття не розкриває, лише спецдія» · entities/state · 🌱.
  - `+scan-charges` «Безпечний погляд із зарядами, що поповнюються між рівнями» · game-logic/economy · 🌱.
  - `+streak-milestone-bonus` «Бонус кожні N правильних дій поспіль» · game-logic/score · 🌱.
  - `+growing-board` (вже пропонована) — трюм 5×5 → 8×8.

## Пропозиції до словників
- `+effect:sort_into(a, bin)` — прибрати клітину з поля в кошик-категорію з перевіркою типу.
- `+ui:odds-preview` — шанси невідомого (уже пропонувався); `+ui:streak-counter` — серія (уже пропонувався); `+ui:bins` — кошики-цілі під полем.
- `+card:sort-into-bins`, `+card:category-line-counts`, `+card:blind-commit-bonus`, `+card:live-recount-clue`, `+card:safe-start-cell`, `+card:ambiguous-cell`, `+card:scan-charges`, `+card:streak-milestone-bonus`.

## Джерела
- ⭐ [itch.io: Cargo Quest](https://kyuroguneiro.itch.io/cargo-quest) — опис: кошики, лічильники рядків/стовпців, перо, ✓-ящик, ×2 наосліп, скан, 5 сердець, трюм 5×5 → 8×8, Книга гільдії, EN/TH; опубліковано 29.10.2026, у розробці.
- Код гри (вбудований `index.html` на html-classic.itch.zone, JS) — таблиця предметів `ITEMS`, ваги за поверхом, розмір трюму, маси, правила відкриття/скану/кидка, серія й FLAWLESS, нагороди між поверхами, тексти Книги гільдії.
- YouTube: пошук «Cargo Quest kyuroguneiro gameplay».

## Непевне
- (?) Усі числа — з однієї збірки (кінець жовтня 2026, «In development»); баланс може змінитись.
- (?) Чи панель шансів завжди видна, чи лише на широкому екрані.
- (?) Чи можна кинути вже відкритий ящик у будь-який момент (у коді так) і чи гра забороняє дії під час анімації польоту.
