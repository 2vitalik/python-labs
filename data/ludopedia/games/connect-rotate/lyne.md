---
title: LYNE
slug: lyne
family: connect-rotate
also: [pencil-logic]
klass: puzzle
axes:
  field: graph
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: 2014
platforms: [iOS, Android, PC, Mac, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/266010/LYNE/", best: true, note: "сторінка Steam: «Connect the shapes. Fill the board.», скріншоти й трейлер, сотні пазлів + щоденні"}
  - {kind: official, url: "https://www.lynegame.com/", note: "офіційний сайт: правило у двох реченнях, лінки на App Store / Google Play"}
  - {kind: other, url: "https://www.cultofmac.com/reviews/lyne-stressful-game-disguise-review", note: "огляд iOS: без перетинів, фігури, крізь які йде кілька ліній"}
  - {kind: other, url: "https://itunes.apple.com/us/app/lyne/id731753333?ls=1&mt=8", note: "App Store"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.thomasbowker.lynerelease", note: "Google Play"}
  - {kind: official, url: "http://www.thomasbowker.com", note: "сайт автора"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=LYNE+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [swipe-gestures, hover-highlight, satisfy-constraints, completion-detection, markup-validity, level-bank, level-select, level-unlock, daily-puzzle, unique-puzzle-generation, theme-select, language-picker, game-screen, main-menu, +path-drawing, +path-cut, +fill-all-cells, +visit-all-nodes, +multi-pass-node, +no-crossing-lines, +move-8dir-path]
proposes: ["+role:terminal", "+role:mark", "+trigger:input(drag)", "+trigger:all_constraints_met", "+cond:same", "+cond:edge_free", "+cond:crosses", "+effect:extend_path", "+effect:cut_path", "+ui:node-pass-counter", "+window:puzzle-select", "+window:daily-window", "+feature:unlockable-palettes", "+card:visit-all-nodes", "+card:multi-pass-node", "+card:no-crossing-lines"]
author: opus
date: 2026-11-02
---

# LYNE — проведи для кожної фігури одну лінію через усі її вузли, не перетинаючи інших

## Суть
На маленькій решітці вузлів-фігур (трикутники, квадрати, ромби — кожна свого кольору) гравець проводить пальцем **одну лінію на тип фігури**: від одного кінцевого вузла до другого через **кожен** вузол свого типу рівно раз. Сірі вузли-«розвилки» з числом треба пройти рівно стільки разів (будь-якими лініями). Лінії не перетинаються, ходити можна й по діагоналі, і в кінці зайнятим має бути все поле. Мінімальні правила, з яких виростає задача про гамільтонові шляхи на кількох кольорах одразу.

## Поле і час
- Решітка вузлів (порядку 3×3…5×6 (?)); сусіди — 8 напрямків (ортогональ + діагоналі), тобто поле — граф 8-сусідства, а не клітини.
- Ребро між двома вузлами використовується максимум раз; діагональні ребра не можуть перехрещуватись.
- Час статичний: без таймера, без ходів-лічильників.
- Пазли: банк наборів (A, B, C … за алфавітом) + нескінченні щоденні згенеровані.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кінцевий вузол (terminal) | terminal (custom) | фігура/колір; 2 на фігуру; з обідком | лінія фігури починається й закінчується на них |
| Вузол фігури | mark | трикутник / квадрат / ромб | має бути пройдений рівно раз лінією своєї фігури |
| Сірий вузол (розвилка) | mark | число 1–4 (?) | пройти рівно N разів (будь-якими лініями); лінія може пройти крізь нього кілька разів |
| Лінія | mark | фігура/колір, послідовність вузлів | малюється drag-ом; без перетинів, без повторних ребер |
| Порожнє місце | static | — | дірка в решітці — вузла нема |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag_start, terminal[s])` → ТО `custom: «почати лінію фігури s»` (стара лінія s стирається (?)).
- КОЛИ `input(drag, node)` → ЯКЩО `adjacent8(path_end, node)` and `edge_free(path_end, node)` and `not crosses(edge)` and (`same(node, s, shape)` and не відвіданий **або** `cell(node, gray)` and `counter(passes, <, n)`) → ТО `extend_path(s, node)`; інакше `block`.
- КОЛИ `input(drag, node)` → ЯКЩО `occupied(node, path[s])` (назад по своїй лінії) → ТО `cut_path(s, node)`.
- КОЛИ `input(tap, node)` на лінії → ТО `cut_path` до цього вузла (?).
- КОЛИ лінія `s` дійшла до другого термінала → ЯКЩО відвідані всі вузли `s` → ТО `custom: «лінію завершено»`; інакше `block` або лінія лишається незавершеною (?).
- КОЛИ `all_constraints_met` — усі лінії завершені, кожен сірий вузол пройдено рівно N разів, жодного вільного вузла → ТО `win`, `sound`, `next_level`.
- Порушення (вузол чужої фігури, зайняте ребро, перетин діагоналей) — просто не дає провести лінію; поразки нема.
- Перемога: «Connect the shapes. Fill the board.» Рахунку немає.

## Керування і ввід
- Тач/миша: затиснути на кінцевому вузлі й вести через вузли; відпустити — лінія зберігається незавершеною.
- Повести назад — відкат; натиснути на вузол лінії — обрізати від нього (?).
- Жодних кнопок перевірки: розвʼязаний пазл визнається автоматично й одразу веде далі.

## Вікна, меню, HUD
- `main-menu` (мінімалістичний): набори пазлів, щоденні, налаштування.
- `puzzle-select`: сітка наборів A…Z → сітка пазлів набору з позначками «розвʼязано»; наступний набір відкривається після попереднього (?).
- `daily-window`: щоденні згенеровані пазли (кілька на день, різного розміру (?)).
- `game-screen`: лише поле вузлів і лінії; назва набору/номер пазла; HUD майже відсутній.
- `settings-window`: `skin-select`-палітри (розблоковуються), мова (12), звук.
- Переходи: main-menu → набір → пазл → (розвʼязано) наступний пазл автоматично.

## Фічі поза полем
- `puzzle-bank` («hundreds of pre-built puzzles») + `level-unlock` наборів.
- `daily-puzzle`: «infinite number of procedurally-generated puzzles, released daily».
- `unlockables`: кольорові палітри; `achievements` (Steam), `cloud-save`.
- `localization` (12 мов); динамічне аудіо, що реагує на лінії.
- Нема undo-кнопки (відкат жестом), підказок, таймерів.

## Варіації й родичі
- Flow Free (пари одного кольору, заповнити поле, без діагоналей), Numberlink, Two Dots (лінія через однакові точки), The Witness (лінія на панелі за правилами регіонів), Hashiwokakero (числа = кількість мостів, як сірі вузли).
- Осі варіацій: **сусідство: 4 / 8 / гекс** · **скільки ліній на колір: 1 (LYNE) / 1 на пару (Flow)** · **вузол-лічильник: 1 / N проходів** · **заповнення: обовʼязкове / ні** · **перетини: заборонені / мости / дозволені діагоналі**.

## Цікавинки для курсу
- Шлях drag-ом по графу 8-сусідства з відкатом — 📎.
- Заборона перетину діагональних ребер (перевірка двох діагоналей одного квадрата) — 🌱, але її легко забути.
- Вузол «пройти рівно N разів» + «ребро лише раз» — 📎.
- Перевірка розвʼязку: кожен вузол фігури відвіданий раз, сірі — N разів, лінії звʼязні від термінала до термінала — 🥉.
- Розвʼязувач: кілька одночасних гамільтонових шляхів з бектрекінгом — 🥇.
- Генератор щоденних пазлів з єдиним розвʼязком — 👑 (картка `unique-puzzle-generation`).

## Мапа на каталог
- Є: `swipe-gestures`, `hover-highlight` · `satisfy-constraints`, `completion-detection`, `markup-validity` · `level-bank`, `level-select`, `level-unlock` · `daily-puzzle` · `unique-puzzle-generation` · `theme-select` (палітри), `language-picker` · `game-screen`, `main-menu`.
- **Нема** → пропозиції карток:
  - `+path-drawing` «Малювання шляху drag-ом» · interface/input · 📎 — з Flow Free; слот {diagonal: true}.
  - `+path-cut` «Відкат шляху до вузла» · entities/legality · 📎.
  - `+fill-all-cells` «Покрити все поле» · game-logic/win · 🌱 — з Flow Free.
  - `+visit-all-nodes` «Шлях через усі вузли свого типу рівно раз» · game-logic/constraints · 🥉 · слоти {per_type: 1}.
  - `+multi-pass-node` «Вузол на N проходів» · entities/legality · 📎 · слот {n: 1..4}.
  - `+no-crossing-lines` «Заборона перетину ліній, зокрема діагоналей» · entities/legality · 🌱.
  - `+move-8dir-path` «Шлях у 8 напрямках» · entities/move · 🌱 (дитина `move-8dir` для шляху, не аватара).

## Пропозиції до словників
- `+role:terminal` — кінцеві вузли з обідком (з Flow Free; друга гра); `+role:mark` ⏳ — вузли й лінії як розмітка.
- `+trigger:input(drag)` · `+trigger:all_constraints_met` ⏳ — ядро.
- `+cond:same` ⏳ (фігура вузла = фігура лінії) · `+cond:edge_free(a, b)` — ребро ще не використане · `+cond:crosses(edge)` — нове ребро перетинає наявне.
- `+effect:extend_path` · `+effect:cut_path` — з Flow Free.
- `+ui:node-pass-counter` — число на сірому вузлі, що зменшується з проходами (?).
- `+window:puzzle-select` ⏳ · `+window:daily-window` ⏳ — підтвердження.
- `+feature:unlockable-palettes` — палітри як нагорода (дитина `unlockables`).

## Джерела
- ⭐ [Steam: LYNE](https://store.steampowered.com/app/266010/LYNE/) — опис, правило «Connect the shapes. Fill the board.», сотні пазлів + щоденні згенеровані, палітри, 12 мов; 17.03.2014.
- [lynegame.com](https://www.lynegame.com/) — офіційний сайт, лінки на мобільні версії, IndieCade finalist.
- [Cult of Mac](https://www.cultofmac.com/reviews/lyne-stressful-game-disguise-review) — огляд iOS (13.01.2014, $2.99): лінії між однаковими фігурами, без перетинів, вузли на кілька ліній.
- [App Store](https://itunes.apple.com/us/app/lyne/id731753333?ls=1&mt=8) · [Google Play](https://play.google.com/store/apps/details?id=com.thomasbowker.lynerelease) · [Thomas Bowker](http://www.thomasbowker.com).
- YouTube: пошук «LYNE puzzle gameplay».

## Непевне
- Веб-пошук вичерпано, статті Wikipedia нема, Hardcore Gaming 101 на обслуговуванні — детальні правила (діагоналі, сірі вузли з числом, ребро лише раз, обідок термінала) з памʼяті; перевірено лише «зʼєднай фігури, заповни поле, без перетинів, вузли на кілька ліній».
- (?) Діапазон чисел на сірих вузлах (1–4?) і чи може одна лінія пройти той самий сірий вузол кілька разів.
- (?) Кількість наборів (A–Z?) і пазлів у наборі; скільки щоденних пазлів на день.
- (?) Чи старт нової лінії від термінала стирає стару; чи тап по вузлу обрізає лінію.
- (?) Розмір решітки.
