---
title: Lights Out
slug: lights-out
aka: [Погаси світло]
family: connect-rotate
also: [pencil-logic]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: state
year: 1995
platforms: [handheld (Tiger Electronics), Game.com, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lights_Out_(game)", best: true, note: "правила 5×5, старт випадковий або збережений, математика над Z2, light chasing, варіанти"}
  - {kind: other, url: "https://www.jaapsch.net/puzzles/lights.htm", note: "Jaap's Puzzle Page: 2^23 розвʼязних позицій, тихі патерни, ≤15 натисків, Lights Out 2000/Deluxe/Cube/Mini, Merlin, XL-25"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/flip.html", note: "Tatham Flip — грати в браузері (хрести або випадкові форми)"}
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/flip.html", note: "правила Flip, параметри, Solve позначає клітини червоним"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lights+Out+Tiger+Electronics+puzzle", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cell-click, keyboard-controls, move-counter, level-solver, rule-variants, wrap-edges, field-size-picker, game-settings, game-screen, +toggle-neighbors, +goal-state-check, +multi-state-cell, +light-chasing, +solvability-parity]
proposes: ["+effect:toggle(group)", "+trigger:all_off", "+cond:lit_only", "+ui:solution-marks", "+card:toggle-neighbors", "+card:light-chasing", "+card:solvability-parity"]
author: opus
date: 2026-11-09
---

# Lights Out — натиск перемикає клітину й чотирьох сусідів; погаси все поле за найменше натисків

## Суть
Поле 5×5 кнопок-ламп, частина з них світиться. Натиск на кнопку перемикає її саму і чотири ортогональні сусідні (вкл ↔ викл); мета — погасити всі лампи, бажано за мінімум натисків. Механіка — лінійна алгебра над полем Z₂: порядок натисків не важить, подвійний натиск нічого не змінює, тож розвʼязок — це множина кнопок. Гра Tiger Electronics (1995) перевинайшла ручний Merlin 1970-х і породила цілу сімʼю пристроїв і цифрових клонів.

## Поле і час
- Квадратна сітка 5×5 (Deluxe — 6×6, Mini — 4×4 з обгортанням країв, Cube — шість граней 3×3 з дією через ребра).
- Кожна клітина — двостанова лампа (Lights Out 2000 — три стани: викл / червоний / зелений).
- Сусідство «плюс»: сама клітина + 4 ортогональні; на краях і в кутах сусідів менше (якщо поле не тор).
- Часу нема: пазл статичний, хід = натиск.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кнопка-лампа | tile | стан on/off; шаблон дії: «+» (стандарт), «×» діагоналі (Deluxe), хід коня (XL-25), випадковий на клітину (Tatham Flip) | натиск перемикає її і клітини свого шаблону |
| Тихий патерн | mark | 2 базові на 5×5 | набір натисків, що не змінює поля: дає 4 розвʼязки на будь-яку розвʼязну позицію |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «увімкнути випадковий набір ламп або збережений патерн»`.
- КОЛИ `input(press, cell)` → ТО `custom: «перемкнути клітину й 4 ортогональних сусідів on↔off»` (`+effect:toggle(group)`), `counter(moves, +1)`.
- КОЛИ `input(press, cell)` → ЯКЩО `custom: «клітина на краю / в куті»` → ТО `custom: «перемкнути лише наявних сусідів (3 або 2)»`.
- КОЛИ `counter(lit, ==, 0)` → ТО `win` (`+trigger:all_off`).
- Інваріант: КОЛИ `input(press, cell)` двічі → ТО `custom: «поле як було»`; порядок натисків на результат не впливає.
- Розвʼязність 5×5: ЯКЩО `custom: «в обох тихих патернах парна кількість увімкнених ламп»` → ТО `custom: «позиція розвʼязна»`; розвʼязних — 2²³ = 8 388 608 з 2²⁵; кожна — не більше ніж за 15 натисків.
- Light chasing: КОЛИ `custom: «рядок 1…4 має вогні»` → ТО `custom: «натиснути кнопку під кожним вогнем у наступному рядку»`; залишок 5-го рядка → натиснути відповідні кнопки 1-го рядка за таблицею (A5 → D1+E1; B5 → B1+E1; C5 → D1) і повторити погоню.
- Lit-only (Deluxe): КОЛИ `input(press, cell)` → ЯКЩО `not state(cell, on)` → ТО `block` (`+cond:lit_only`).
- Toggle-гра (Deluxe): КОЛИ `input(press, cell)` → ЯКЩО `custom: «попередній натиск був по клітині того самого стану»` → ТО `block` — натискати поперемінно увімкнені й вимкнені.
- Шаблон «×» (Deluxe): КОЛИ `input(press, cell)` → ТО `custom: «перемкнути клітину й 4 діагональних сусідів»`.
- Mini Lights Out: КОЛИ `input(press, edge_cell)` → ТО `wrap(neighbour)` — сусід з протилежного боку; усі 2¹⁶ позицій 4×4 розвʼязні.
- Lights Out 2000: КОЛИ `input(press, cell)` → ТО `custom: «стан клітини й сусідів іде по колу викл → червоний → зелений»` (?).
- Перемога: усе темне. · Поразки нема. · Рахунок: кількість натисків (менше — краще).

## Керування і ввід
- Оригінал: натиск на будь-яку з 25 кнопок-ламп; поруч кнопки вибору гри / звуку / старту (?).
- Цифрові клони: клік мишею по клітині; Tatham Flip — ще й курсорні клавіші + Space/Enter.
- Жодного вибору фігури чи режиму вводу — одна дія «натиснути».

## Вікна, меню, HUD
- Пристрій: сама сітка — і поле, і ввід; номер пазла й лічильник натисків — (?).
- `game-screen` (цифрова версія): поле, `move-counter`, кнопка нової гри, `restart-button`.
- `settings-window` (Tatham Flip): ширина, висота, тип форм («хрести» / випадкові).
- `hints-window`-подібний режим Solve (Tatham): червоні позначки на клітинах, які треба натиснути; клік по непозначеній ставить позначку «відмінити».
- `mode-select` (Deluxe): хрест/діагоналі × звичайна / Lit-only / Toggle.
- Переходи: (цифрова версія) game-screen → (усе темне) повідомлення про перемогу → нова гра.

## Фічі поза полем
- `puzzle-bank`: вбудовані пазли (Classic; Lights Out 2000 — розвʼязні за 5–24 натиски; Deluxe — 150 пазлів на кожну з 6 комбінацій «шаблон × тип гри»).
- `custom-rules`: шаблон дії (+ / × / кінь), Lit-only, Toggle, тор (Mini), розмір поля.
- `show-solution` (Tatham Flip Solve), `custom-difficulty` через розмір.
- Lights Out 2000: окрема «екшн-гра» і гра на двох (подробиць джерела не дають).

## Варіації й родичі
- Попередники: Merlin (Parker Brothers, 1970-ті, 3×3, 512 позицій); XL-25 (Vulcan Electronics, ≈1983) — стандартна гра і варіант із ходом коня.
- Tiger: Lights Out 2000 (5×5, три стани), Lights Out Deluxe (6×6, + і ×, Lit-only і Toggle), Lights Out Cube (3×3×3, 2⁴⁸ позицій, ≤30 ходів), Mini Lights Out (4×4, тор); картридж Game.com (1997, у комплекті з консоллю). Orbix — на 12 гранях додекаедра.
- Цифрові: Tatham Flip (`pencil-logic/tatham-collection` — хрести або випадкові форми, мета навпаки: усе світле), GNOME Lights Off (?).
- **Осі варіацій**: шаблон дії (+ / × / кінь / довільний на клітину) · кількість станів (2 / 3) · топологія (прямокутник / тор / куб / додекаедр) · обмеження натиску (будь-яка / лише світла / поперемінно) · мета (усе темне / усе світле).
- Родичі: `falling-match/polarium` (перемикання кольору клітин), Reversi (перевертання), `program-robots/lightbot` — лише назва схожа: там робот запалює плитки програмою, не та сама гра.

## Цікавинки для курсу
- Натиск = XOR з шаблоном «+» (і крайові випадки) — 🌱.
- Генератор лише розвʼязних позицій: випадкові натиски від темного поля замість випадкових ламп — 🌱.
- Розвʼязувач Гаусом над GF(2) для n×n (25×25 матриця для 5×5) + мінімальний розвʼязок перебором 4 варіантів з тихими патернами — 🥇.
- Light chasing як «людський» алгоритм-підказка з таблицею для 5-го рядка — 📎.
- Варіанти правил одним параметром: шаблон, тор, Lit-only, 3 стани — 🥉.
- Перевірка розвʼязності за парністю тихих патернів — 🥈.

## Мапа на каталог
- Є: `cell-click` + `keyboard-controls` ↔ натиск · `move-counter` ↔ натиски · `level-solver` ↔ Гаус над GF(2) / Solve у Flip · `rule-variants` ↔ +/×/Lit-only/Toggle · `wrap-edges` ↔ Mini Lights Out · `field-size-picker` + `game-settings` ↔ розмір і форми Flip · `game-screen`.
- **Нема** → пропозиції карток:
  - `+toggle-neighbors` «Натиск перемикає клітину й сусідів за шаблоном» · entities/state · 🌱 · слоти {pattern: plus|x|knight|custom, states: 2|3}.
  - `+goal-state-check` (є в корпусі) — усе вимкнено.
  - `+multi-state-cell` (є в корпусі) — три стани Lights Out 2000.
  - `+light-chasing` «Алгоритм погоні за вогнями як підказка» · levels/solvability · 📎.
  - `+solvability-parity` «Розвʼязність за інваріантом парності» · levels/solvability · 🥈.

## Пропозиції до словників
- `+effect:toggle(group)` (повтор Blobun) — перемкнути стан групи клітин одним натиском.
- `+trigger:all_off` — усі лампи/клітини в стані «викл» (можна звести до `counter(lit, ==, 0)`; пропоную як читабельніше).
- `+cond:lit_only` — дія дозволена лише на клітині у стані «увімк».
- `+ui:solution-marks` — позначки клітин, які лишилось натиснути (Tatham Solve).
- `+card:toggle-neighbors`, `+card:light-chasing`, `+card:solvability-parity` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Lights Out (game)](https://en.wikipedia.org/wiki/Lights_Out_(game)) — правила 5×5, старт випадковий або збережений, мета «за мінімум натисків», вектори над Z₂, 4 розвʼязки, light chasing, n×n, Merlin, XL-25, Lights Out 2000/Cube/Deluxe, Game.com.
- [Jaap's Puzzle Page: Lights Out](https://www.jaapsch.net/puzzles/lights.htm) — 2²³ позицій, ≤15 натисків, тихі патерни й перевірка розвʼязності, таблиця 5-го рядка, Lights Out 2000 (5–24 ходи, екшн і 2P), Deluxe (+/×, Lit-only, Toggle, 150 пазлів), Cube, Mini, Merlin, XL-25.
- [Tatham: Flip (довідка)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/flip.html) і [грати](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/flip.html) — цифровий родич: хрести / випадкові форми, Solve з червоними позначками.
- YouTube: пошук «Lights Out Tiger Electronics puzzle».

## Непевне
- (?) Режими оригінального пристрою (скільки вбудованих пазлів, чи є ліміт ходів на пазл, ввід власного патерну, звук, табло) — джерела не описують; старий лист у ticalc.org згадує «додаток з усіма рівнями й кількістю дозволених ходів» у мануалі.
- (?) Порядок станів у Lights Out 2000 (викл → червоний → зелений) — Jaap називає лише три стани.
- (?) Правила екшн-гри й гри на двох у Lights Out 2000.
- (?) Автори (Avi Olti та ін.) — у Wikipedia без джерела.
- Межа сімʼї: зʼєднань і обертань тут нема — гра в `connect-rotate` за призначенням черги; за ядром ближча до `pencil-logic` (Tatham Flip), тому `also: [pencil-logic]`.
- Плутанина черги: автоматика звʼязала Lights Out з `program-robots/lightbot` — це різні ігри.
