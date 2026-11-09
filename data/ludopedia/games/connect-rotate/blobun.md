---
title: Blobun
slug: blobun
aka: [Blobun Mini]
family: connect-rotate
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2025
platforms: [PC (Windows, Linux), PICO-8 (Mini), macOS (Mini)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3284270/Blobun/", best: true, note: "мета «торкнись кожної клітини», елементи (ключі-перемикачі, конвеєри, тріснута підлога, лазери, лава), стани Fire/Ice/Electric і «без слизу», undo, skip, редактор"}
  - {kind: steam, url: "https://store.steampowered.com/app/3827340/Blobun_Mini/", note: "безкоштовна Mini: 60 пазлів у 5 світах, floor zappers, fire/ice, налаштування Slime Overlap і Sprint"}
  - {kind: itch, url: "https://cyansorcery.itch.io/blobun", note: "той самий опис + mod.io, редактор лише Windows"}
  - {kind: itch, url: "https://cyansorcery.itch.io/blobun-mini", note: "клавіші (стрілки, Z/C/N sprint, X/V/M undo, P пауза), опис Slime Overlap"}
  - {kind: official, url: "https://blobun.com/", note: "сторінка-заглушка з лінками й прес-китом"}
  - {kind: other, url: "https://steamcommunity.com/app/3284270/discussions/0/594034910828727316/", note: "бета 1.1: ремап вводу; патчі 1.0.8–1.0.10: стрілки підказок, тривалість утримання restart/skip/undo"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Blobun+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, keyboard-controls, visited-trail, floor-types, button-toggle, environment-death, impassable-cells, undo-redo, restart-level, skip-level, level-select, level-unlock, in-game-editor, level-exchange, controls-remap, game-settings, volume-control, game-pause, pause-menu, game-screen, +fill-all-cells, +state-token, +crumbling-floor, +conveyor-push, +hint-arrows, +overlap-rule-toggle, +hold-to-repeat, +sprint-toggle]
proposes: ["+effect:toggle(group)", "+card:state-token", "+card:fill-all-cells", "+card:overlap-rule-toggle", "+card:hint-arrows", "+feature:hold-to-confirm", "+feature:sprint-toggle", "+ui:touched-counter"]
author: opus
date: 2026-11-09
---

# Blobun — слизовий зайчик мусить торкнутися кожної клітини кімнати

## Суть
Покрокова кімнатна головоломка з видом згори: Стефані (зайчик-слиз) ходить по сітці й лишає слизовий слід; рівень пройдено, коли **кожна** клітина підлоги торкнута. Простота мети ламається елементами: тріснута підлога ламається після кроку, конвеєри штовхають, ключі перемикають блоки, лава й лазери вбивають. Токени змінюють **стан** героїні (Fire — ходити лавою, Ice — ковзати водою, Electric, стан «без слизу»), тож одна кімната вимагає кількох «режимів» руху. Ближче до LYNE/Flow Free (покрити все одним шляхом), ніж до Sokoban: тут нічого не штовхаєш, лише плануєш маршрут.

## Поле і час
- Квадратна сітка-кімната; стіни, порожнеча й підлога різних типів. Розміри кімнат — (?).
- Шари: підлога (звичайна / тріснута / конвеєр / вода / лава) + обʼєкти (блоки-перемикачі, ключі, токени) + шар слизу (торкнуто / ні).
- Хід = крок на 1 клітину; без вводу світ стоїть (`time: turn`), ліміту часу нема; Mini має опційні таймери (лише показ).
- Світи (worlds) з власною музикою, фоном і набором механік; пак світів — `worldpak` (редактор).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Стефані (Blobun) | player | стан: normal / fire / ice / electric / no-slime | крок 4 напрямки; лишає слиз на клітині, крім стану no-slime |
| Підлога | terrain | торкнута / ні | має бути торкнута для перемоги |
| Слиз | mark | — | позначка «торкнуто»; з вимкненим Slime Overlap крок на свій слід заборонено (Mini) |
| Стіна | static | — | непрохідна |
| Тріснута підлога | terrain | ціла / зламана | ламається після того, як на неї стали; далі непрохідна (?) |
| Конвеєр | terrain | напрям | штовхає героїню в заданому напрямку; штовхає навіть на власний слід |
| Ключ (floating key) | switch | група блоків | при взятті перемикає блоки-перемикачі на полі |
| Блок-перемикач (toggle block) | gate | піднятий / опущений | піднятий — непрохідний; ключ змінює стан усієї групи |
| Токен стану | pickup | fire / ice / electric / no-slime | при взятті змінює стан героїні |
| Лава | hazard | — | смертельна; у стані fire — прохідна |
| Вода | terrain | — | у стані ice по ній можна «ковзати» (skate); без ice — (?) |
| Лазер | hazard | напрям променя (?) | небезпечний; точна поведінка — (?) |
| Floor zapper (Mini) | hazard | — | перешкода на підлозі; поведінка — (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(player, dir)`, `paint(next, slime)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next, wall)` або `cell(next, toggle_block_up)` → ТО `block`.
- КОЛИ `input(dir)` → ЯКЩО `mode(slime_overlap_off) and cell(next, slime)` → ТО `block` (Mini; з увімкненим перекриттям крок дозволено).
- КОЛИ `input(dir)` → ЯКЩО `free(next) and state(player, no_slime)` → ТО `move(player, dir)`, `custom: «клітина не позначається слизом»` — торкання не зараховується (?).
- КОЛИ `enter(player, conveyor)` → ТО `move(player, conveyor_dir)` — навіть на власний слід, коли перекриття вимкнено.
- КОЛИ `leave(player, cracked_floor)` → ТО `set_cell(cracked_floor, broken)` (?) — «break once you move onto them»; точний момент — (?).
- КОЛИ `contact(player, key)` → ТО `custom: «усі блоки-перемикачі міняють стан піднятий ↔ опущений»`, `disappear_b` (?).
- КОЛИ `contact(player, token)` → ТО `set_state(player, kind)` (fire / ice / electric / no_slime), `disappear_b` (?).
- КОЛИ `enter(player, lava)` → ЯКЩО `not state(player, fire)` → ТО `lose` — custom: «смерть; вихід — undo або рестарт» (?).
- КОЛИ `enter(player, water)` → ЯКЩО `state(player, ice)` → ТО `slide(player, dir)` (?) — «skate on water».
- КОЛИ `contact(player, laser)` → ТО `lose` (?).
- КОЛИ `all_constraints_met` → ЯКЩО `cover_all(slime)` → ТО `win`, `next_level`.
- КОЛИ `input(undo)` → ТО `undo(1)`; утримання кнопки → ТО `undo(n)` — кроки скасовуються серією (тривалість утримання — у налаштуваннях).
- КОЛИ `input(restart)` утримано → ТО `restart` (утримання 0.25/0.5/0.75 с або Instant).
- КОЛИ `input(skip)` утримано → ТО `next_level`, `custom: «пазл пропущено, не розвʼязано»`.
- КОЛИ `level_end` → ЯКЩО `counter(solved_in_world, >=, N)` → ТО `unlock(next_world)` — N (?).
- КОЛИ `input(hint)` → ТО `custom: «стрілки частини маршруту на клітинах»`; на вже торкнутих клітинах стрілки не малюються (патч 1.0.8+).
- Перемога: слиз на всіх клітинах підлоги. · Поразка: лава / лазер / пастка — повтор через undo. · Рахунку нема; є досягнення (31 у Steam).

## Керування і ввід
- Клавіатура (Mini): стрілки — крок; Z/C/N — sprint (швидша анімація ходу); X/V/M — undo (утримання — серія); P — пауза.
- Restart і skip — утриманням кнопки з налаштовуваною тривалістю.
- Повна підтримка геймпадів; Steam-категорії «Keyboard Only» і «Mouse Only»; ремап клавіш і геймпада — з v1.1.
- Редактор — лише мишею з клавіатурою, лише на Windows.

## Вікна, меню, HUD
- `game-screen`: кімната зі слідом; `hint-marker` (стрілки підказки); `timer-elapsed` (Mini, опційно).
- `level-select` (stage select): пазли світу, позначки пройдено/пропущено (?), імʼя автора пазла (патч 1.0.10).
- `map-window` світів (?) — «numerous puzzles across a variety of worlds».
- `pause-menu` (P): продовжити, restart, skip, налаштування (?).
- `settings-window`: Slime Overlap, Sprint By Default, музика/звуки, `options-accessibility` (Reduced Motion, тривалість утримань), `options-controls` (ремап), заливка letterbox кольором, перемикач «Lesbians Allowed».
- `editor-window`: редактор пазлів (Windows).
- `custom-window`: браузер спільнотних пазлів через mod.io.
- Сюжетні вставки (`dialogue-window`) — лише в повній грі; Mini без сюжету.

## Фічі поза полем
- `undo` (утримання — багато кроків), `restart-level`, `skip-level` без ліміту, але для просування світом треба розвʼязати певну кількість.
- `hint` — стрілки частини розвʼязку.
- `level-editor` (Windows) + `level-sharing` / `user-levels-browser` через mod.io; кастомні рівні вантажать усі десктоп-версії, демо — ні.
- `custom-rules`: Slime Overlap — перемикач правила «можна ступати на свій слід».
- `remap-controls`, `options-accessibility` (Reduced Motion, Camera Comfort, Color Alternatives), `volume-sliders`, `achievements`, `cloud-save`.
- Sprint By Default: інвертує кнопку sprint (швидко за замовчуванням, утримання — повільно).

## Варіації й родичі
- **Blobun Mini** (2025, PICO-8, безкоштовна): 60 нових пазлів у 5 світах на тих самих елементах + floor zappers; стани лише fire/ice; без сюжету; налаштування Slime Overlap, Sprint By Default, Show Timers.
- Родичі в корпусі: [LYNE](lyne.md) і [Flow Free](flow-free.md) — покрити все шляхом; [Hands of Time](hands-of-time.md) — гамільтонів шлях; Q*bert / Make Trax — «пофарбуй усі клітини», але real-time з ворогами.
- Осі варіацій: **повторний візит** — заборонено (гамільтонів шлях) / дозволено (Blobun з Overlap) / перемикач гравця · **примусовий рух** — нема / конвеєр / ковзання · **одноразові клітини** — нема / тріснута підлога · **стани аватара** — один / кілька токенами.

## Цікавинки для курсу
- Слід + перевірка «усі клітини торкнуті» (множина відвіданих = множина підлоги) — 🌱.
- Тріснута підлога як одноразова клітина + конвеєр як примусовий крок після входу — 📎.
- Токени станів (fire/ice/no-slime) і таблиця «клітина × стан → дозволено/смерть/ковзання» — 🥉 (класична таблиця взаємодій).
- Ключ, що перемикає групу блоків, і повʼязаний з ним undo (стан блоків теж у стеку) — 📎.
- Перемикач правила Slime Overlap: одна прапорцева умова в legality-перевірці, яка змінює клас задачі — 🌱.
- Розвʼязувач: DFS/BFS по станах (позиція, стан, множина торкнутих, блоки, зламані клітини) з бітмасками — 🥇.
- Undo утриманням з прискоренням + конфіг тривалості утримання для restart/skip — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ крок; `visited-trail` ↔ слиз; `floor-types` ↔ конвеєр, вода, лава, тріснута; `button-toggle` ↔ ключ перемикає блоки; `environment-death` ↔ лава/лазер; `impassable-cells` ↔ стіни, підняті блоки; `undo-redo` + `restart-level` ↔ undo/restart; `skip-level` ↔ пропуск; `level-select` + `level-unlock` ↔ stage select і поріг розвʼязаних; `in-game-editor` + `level-exchange` ↔ редактор і mod.io; `controls-remap`, `game-settings`, `volume-control`, `game-pause`, `pause-menu`, `game-screen`.
- **Нема** → пропозиції карток:
  - `+fill-all-cells` (Flow Free, LYNE) — «Покрити всі клітини» · game-logic/win · 🌱.
  - `+state-token` «Токен перемикає стан аватара; стан визначає дозволені клітини» · entities/state · 🥉 · слот {states: [fire, ice, …]}.
  - `+crumbling-floor` (Manic Miner) — «Клітина ламається після проходу» · entities/interact · 🌱.
  - `+conveyor-push` «Конвеєр штовхає аватара після входу» · entities/move · 📎 — `row-conveyor` зсуває смугу, а не того, хто стоїть.
  - `+hint-arrows` «Підказка-стрілки частини розвʼязку на клітинах» · game-logic/difficulty · 📎.
  - `+overlap-rule-toggle` «Перемикач правила повторного візиту» · game-logic/constraints · 🌱.
  - `+hold-to-repeat` «Утримання кнопки повторює дію (undo серією)» · interface/input · 🌱.
  - `+sprint-toggle` «Швидкість анімації ходу кнопкою / за замовчуванням» · interface/settings · 🌱.

## Пропозиції до словників
- `+effect:toggle(group)` — перемкнути стан цілої групи сутностей (блоки Blobun, плити Zelda) — без нього речення про ключ іде в `custom`.
- `+card:state-token`, `+card:fill-all-cells`, `+card:overlap-rule-toggle`, `+card:hint-arrows` — див. «Мапа на каталог».
- `+feature:hold-to-confirm` — небезпечні дії (restart, skip) лише утриманням, з налаштовуваною тривалістю.
- `+feature:sprint-toggle` — інверсія кнопки прискорення ходу.
- `+ui:touched-counter` — лишилось неторкнутих клітин (?) — чи є в HUD, не перевірено.

## Джерела
- ⭐ [Steam: Blobun](https://store.steampowered.com/app/3284270/Blobun/) — мета, елементи, стани Fire/Ice/Electric/без слизу, undo, без ліміту часу, skip з порогом розвʼязаних, редактор (Windows), mod.io; через appdetails — 31 досягнення, категорії доступності.
- [Steam: Blobun Mini](https://store.steampowered.com/app/3827340/Blobun_Mini/) — 60 пазлів / 5 світів, toggle blocks, floor zappers, fire/ice, Slime Overlap, Sprint, таймери.
- [itch: Blobun Mini](https://cyansorcery.itch.io/blobun-mini) — клавіші, «When disabled, you'll be prevented from overlapping your own trail», конвеєри «will still push you into it».
- [itch: Blobun](https://cyansorcery.itch.io/blobun) · [blobun.com](https://blobun.com/) — той самий опис, прес-кит.
- [Steam: обговорення бети 1.1](https://steamcommunity.com/app/3284270/discussions/0/594034910828727316/) і тред «controls and stuff» — ремап, утримання undo для серії кроків, тривалості restart/skip, стрілки підказок не на торкнутих клітинах.
- YouTube: пошук «Blobun gameplay».

## Непевне
- (?) Чи є Slime Overlap у повній грі і яке значення за замовчуванням; чи «гамільтонів» характер (рядок черги) — правило гри чи лише режим без перекриття. Джерела кажуть лише «touch every tile».
- (?) Точна поведінка лазерів, floor zappers, стану Electric (патч згадує «Electric Wire» Стефані), води без стану ice.
- (?) Чи зникають ключі й токени після взяття; чи тріснута клітина ламається одразу чи після виходу; чи стан діє до кінця кімнати чи до наступного токена.
- (?) Що відбувається при смерті (автоматичний undo / рестарт), кількість пазлів повної гри, поріг розвʼязаних для просування.
- (?) Підказки: як викликаються і чи обмежені — відомо лише про стрілки й «partial directions» з пошукового резюме.
