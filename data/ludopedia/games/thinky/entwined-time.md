---
title: Entwined Time
slug: entwined-time
aka: []
family: thinky
also: [grid-platformer]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2024
platforms: [PC, Mac, Linux, web]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3147300/Entwined_Time/", best: true, note: "безкоштовно (22.10.2024): два роботи з незалежними таймлайнами, 12+ розділів, Gain Insight, копіювання реплеїв, редактор і Community Puzzles"}
  - {kind: itch, url: "https://patashu.itch.io/entwined-time", note: "грати в браузері (HTML5) і збірки Win/Mac/Linux; Godot 3.5.3; перший реліз — квітень 2024"}
  - {kind: official, url: "https://github.com/Patashu/Entwined-Time", note: "увесь код: GameLogic.gd — гравітація, сила/вага, міцність, таймлайни, кольори часу, кристали; список ~200 плиток і розділів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Entwined+Time+Patashu+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, move-by-input, keyboard-controls, party-switch, gravity-fall, ladder-climb, push-object, one-way-cell, impassable-cells, environment-death, destructible-blocks, reach-exit, all-on-targets, undo-redo, undo-unlimited, redo, restart-level, replay, replay-window, level-select, level-unlock, sequential-levels, in-game-editor, editor-playtest, controls-remap, settings-window, main-menu, game-screen, sound-effects, background-music, save-progress, +per-character-timeline, +meta-undo, +timeline-length-limit, +time-crystal, +time-colour, +strength-vs-weight, +jump-hang, +sticky-top, +break-and-rewind, +insight-level]
proposes: ["+effect:rewind_actor", "+effect:timeline_slots", "+cond:stronger", "+ui:timeline-bar", "+feature:insight-level", "+feature:copy-paste-replay", "+feature:undo-restart", "+axis:undo", "+card:per-character-timeline", "+card:time-colour"]
author: opus
date: 2026-11-09
---

# Entwined Time — два роботи, два окремі таймлайни: кожен ходить і відмотує свої ходи незалежно від іншого

## Суть
Покрокова клітинна головоломка Patashu (вид збоку, з гравітацією). Гравець перемикається між двома роботами — важким **Heavy** (червоний) і легким **Light** (синій); у кожного **свій таймлайн**: власна кнопка «Rewind» скасовує всі події останнього ходу саме цього робота, а не останній хід гри. Отже можна, наприклад, штовхнути ящик Heavy, походити Light, а потім відмотати лише Heavy — ящик повернеться, а Light лишиться де був. Окремо є «мета-undo», що скасовує будь-який останній ввід. Мета — обидва роботи цілими на своїх порталах. Сотні пазлів у 12+ розділах, кожен додає елемент: шипи й вогонь, односторонні клітини, ящики різної ваги, кристали часу, кольори часу, фазові блоки, «загробне життя».

## Поле і час
- Квадратна сітка, вид збоку; гравітація вниз (у пізніх розділах — плитки зміни гравітації). Рівень — один екран; код обмежує поле ~21×10 клітин (?).
- Клітина має шари терену (кілька плиток одночасно) плюс актори: роботи, ящики, кристали, годинники, валуни.
- Хід = один ввід обраного робота або одна відмотка. Після ходу «йде час» для сутностей, чий **колір часу** це дозволяє: падіння, вогонь, тік годинника.
- Два таймлайни показано зліва (Heavy) і справа (Light) смугами клітинок-ходів; рівень може обмежити довжину таймлайна.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Heavy | player | вага STEEL, сила HEAVY, ламається від вогню, падає до 2 кл/хід | ходить, стрибає на 1, лізе драбинами; без керування в першому тіку падіння; несе на собі того, хто стоїть зверху |
| Light | player | вага IRON, сила LIGHT, ламається від шипів, падає 1 кл/хід і «зависає» | ходить, стрибає; у повітрі може рухатися вбік; у ланцюгу поштовхів слабшає на 1 |
| Портал Heavy / Light | static | червоний / синій | ціль; замкнений, доки на полі є цілі кристали |
| Стіна | static | — | непрохідна |
| Шипи | hazard | зелені / пустотні варіанти | ламають Light, дерев'яні ящики, годинники; Heavy — ні |
| Вогонь (+ лише для Heavy / лише для Light) | hazard | — | наприкінці ходу ламає того, хто стоїть (обох роботів, залізні ящики) |
| Безодня (низ поля), діри | hazard | — | падіння за низ ламає майже все, навіть сталь |
| Драбина, драбина-платформа | terrain | — | робот висить і лізе; не падає |
| Дерев'яна платформа | terrain | — | тримає при падінні згори; знизу й збоку — прохід |
| Одностороння клітина (4 напрями; зелена, пурпурова, сіра, «смертельна») | terrain | напрям | вхід лише в один бік |
| Заборона Heavy / Light / ящиків | terrain | — | непрохідна для одного типу актора |
| Дерев'яний ящик | object | вага WOODEN | штовхає будь-хто; Heavy розбиває, Light піднімає вгору, якщо поштовх не вдався |
| Залізний ящик | object | вага IRON | штовхають обидва; ламається від вогню |
| Сталевий ящик | object | вага STEEL | штовхає лише Heavy; падаючи на Light, ламає його |
| Power-ящик | object | вага WOODEN, сила HEAVY | легкий, але сам штовхає як Heavy |
| Ціль для ящика | static | — | має бути зайнята ящиком для перемоги |
| Чекпойнт (загальний / червоний / синій) | terrain | — | стираючи таймлайн робота, робить його ходи постійними |
| Кристал часу зелений | pickup | — | +1 хід таймлайна або розблокування замкненого |
| Кристал часу пурпуровий | pickup | — | замикає хід: доступний таймлайн коротшає на 1 |
| Годинник-зозуля | object | лічильник ходів | доходить до 0 — поразка |
| Скло (звичайне, зелене, тріснуте) | object | — | розбивається при падінні Heavy / поштовху |
| Плитки «No Undo» / «One Undo» / «No Retro» | terrain | — | забороняють або обмежують відмотку робота, що на них стоїть |
| Пізні елементи | — | — | фазові стіни й блискавки, дошки й діри, бустер, схили, валун з імпульсом, «nudge», вентилятор, бампер, бомба, павутина, туман, ремонтна станція, зомбі-плитка, міміки, зміна гравітації — (лише перелік з коду) |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух і гравітація:
- КОЛИ `input(dir)` → ЯКЩО `not state(selected, broken)` і `counter(turn_selected, <, max_moves)` → ТО `move(selected, dir)`; події ходу записуються в таймлайн обраного робота, `counter(turn_selected, +1)`.
- КОЛИ `input(dir)` → ЯКЩО `state(selected, broken)` → ТО `block`, `sound(bump)` — зламаний робот не ходить, але може відмотатись.
- КОЛИ `input(up)` → ЯКЩО `custom: «робот на опорі»` і `free(above)` → ТО `move(selected, up)`, `set_state(selected, airborne, 2)` — стрибок на 1 клітину з «зависанням».
- КОЛИ `turn_end(any)` → ЯКЩО `custom: «нема опори й не на драбині»` → ТО `fall(a)`: Heavy до 2 клітин за хід, Light — 1 і спершу зависає на хід.
- КОЛИ `input(dir)` → ЯКЩО `state(heavy, airborne)` і `custom: «Heavy вже почав падати»` → ТО `block`; Light у повітрі може лише вбік (`custom: «ходи вгору/вниз у повітрі заборонені»`).
- КОЛИ `enter(a, ladder)` → ТО `custom: «a висить: не падає, лізе вгору/вниз»`.
- КОЛИ `contact(a, wooden_platform)` → ЯКЩО `moving(a, down)` і `custom: «рух — це падіння»` → ТО `block`; інакше прохід.
- КОЛИ `contact(a, oneway)` → ЯКЩО `not moving(a, allowed_dir)` → ТО `block`.
- КОЛИ `contact(a, no_heavy|no_light|no_crate)` → ЯКЩО `same(a, forbidden, type)` → ТО `block`.

Поштовх і вага:
- КОЛИ `contact(a, crate)` → ЯКЩО `custom: «сила a ≥ вага crate»` і `free(cell_behind)` → ТО `push(crate)`; ланцюг ящиків дозволено; інакше `block`.
- Таблиця сили: WOODEN-вага — сила ≥ WOODEN; IRON — ≥ LIGHT; STEEL — лише HEAVY. Light у середині ланцюга має силу −1 (`custom: «Light Clumsiness Rule»`).
- КОЛИ `contact(heavy, wooden_crate)` → ЯКЩО `not free(cell_behind)` → ТО `set_state(wooden_crate, broken)`; для Light у тій самій ситуації → `push(wooden_crate)` вгору.
- КОЛИ `move(heavy, dir)` → ЯКЩО `occupied(above_heavy, a)` і `not moving(heavy, up)` → ТО `move(a, dir)` — «sticky top», Heavy везе того, хто на ньому.
- КОЛИ `contact(steel_crate, light)` → ТО `set_state(light, broken)` — сталь, що рухається або падає на Light, ламає його.

Небезпеки:
- КОЛИ `enter(a, spikes)` → ЯКЩО `custom: «міцність a = SPIKES»` (Light, дерев'яний ящик, годинник) → ТО `set_state(a, broken)`.
- КОЛИ `turn_end(any)` → ЯКЩО `occupied(fire, a)` і `custom: «міцність a ≤ FIRE»` → ТО `set_state(a, broken)`; червоний вогонь — лише Heavy, синій — лише Light.
- КОЛИ `edge(a)` → ЯКЩО `custom: «a не кристал»` → ТО `set_state(a, broken)` — безодня внизу.

Час:
- КОЛИ `input(rewind)` → ЯКЩО `counter(turn_selected, >, 0)` → ТО `custom: «скасувати всі події останнього ходу таймлайна обраного робота»`, `counter(turn_selected, -1)` (`+effect:rewind_actor`).
- КОЛИ `input(rewind)` → ЯКЩО `occupied(no_undo, selected)` → ТО `block`, `sound(rewindstopped)`; «One Undo» дозволяє одну відмотку й стає «No Undo».
- КОЛИ `input(meta_undo)` → ТО `undo(1)` — скасовує останній ввід (хід, відмотку, перемикання, навіть рестарт); `input(meta_redo)` → повтор.
- Колір часу: КОЛИ `turn_end(any)` → ТО `custom: «час іде для сутності лише за її кольором: сірий — коли хтось ходить уперед; червоний/синій — лише ходи Heavy/Light; пурпуровий — завжди; зелений — події не записуються й не відмотуються; білий — ніколи»`.
- КОЛИ `enter(robot, checkpoint)` → ТО `custom: «таймлайн робота стирається: записані ходи стають постійними»`.
- КОЛИ `contact(robot, green_crystal)` → ТО `pickup`, `custom: «+1 хід таймлайна або розблокувати замкнений хід»` (`+effect:timeline_slots`).
- КОЛИ `contact(robot, magenta_crystal)` → ТО `pickup`, `custom: «замкнути останній хід — таймлайн коротшає на 1»`; ЯКЩО `counter(moves, <, 0)` → ТО `lose` («Paradox: A character can't have less than 0 moves»).
- КОЛИ `custom: «на полі є цілі кристали»` → ТО `set_state(portals, locked)`.
- КОЛИ `counter(cuckoo_ticks, ==, 0)` → ТО `lose` («You didn't make it back to the Chrono Lab Reactor in time»).

Перемога й поразка:
- КОЛИ `custom: «обидва роботи цілі й на своїх порталах, усі цілі для ящиків зайняті, портали не замкнені»` → ТО `win`, `window(end-screen)`; під час мета-undo перемога не зараховується.
- Поразка: парадокс, годинник, нескінченний цикл — текст «Undo or Restart to continue». Зламаний робот — не поразка: його можна відмотати.

## Керування і ввід
- Стрілки або WASD — хід обраного робота; X або Tab — перемкнути робота; Z — Rewind обраного; C — мета-undo; Y — мета-redo; R — рестарт; G — Gain Insight; L — вибір рівня; Esc — меню; M — звук.
- Ctrl+C / Ctrl+V — скопіювати / вставити реплей (так роблять власні «чекпойнти»); F4 — показ реплею поточної спроби; F8–F11 і F5–F7 — програвання, швидкість, крок назад/вперед, пауза.
- Мишею: віртуальні кнопки на екрані; геймпад (часткова підтримка у Steam); перепризначення клавіш.

## Вікна, меню, HUD
- `splash-screen` / титул: Begin · Controls · Settings · Credits · Discord.
- `game-screen`: поле; зліва — таймлайн Heavy, справа — таймлайн Light (`+ui:timeline-bar`): клітинки ходів, замкнені й доступні слоти, ліміт; підписи роботів з номером ходу; назва рівня й зірка «пройдено»; навчальні підказки клавіш у перших рівнях; передбачення відмотки («Rewind Prediction» — напівпрозорі привиди).
- `pause-menu` «MaintBot OS v19.9 — Control Panel»: Continue · Restart · Level Select · Gain Insight · Your Replay · Author's Replay · Copy / Paste / Save Replay · Controls · Settings · Quit Game.
- `level-select`: розділ з рівнями, Prev/Next Chapter (F1/F2), пошук за назвою (Ctrl+F), Community Levels, Level Editor, варіанти й «Cutting Room Floor».
- `settings-window`: швидкість анімації, гучності, Jukebox, Colourblind Mode, шахівниця поля, прозорість передбачення, «Undo a Restart?», віртуальні кнопки, Unlock everything, копія/вставка сейва, скидання прогресу, роздільність, повний екран, VSync.
- `options-controls`: перепризначення клавіш.
- `replay-window`: реплей поточної спроби або авторський, повзунки ходу й швидкості.
- `editor-window`: редактор рівнів із шарами терену, полями назви, автора, ліміту ходів, лічильників годинників; тест рівня записує реплей автора.
- `end-screen`: напис перемоги (Enter — далі) або поразки з причиною; фінальні катсцени.

## Фічі поза полем
- `undo` двох рівнів: відмотка робота як механіка поля + `+feature:undo-restart` — мета-undo без ліміту, навіть після рестарту; `redo`.
- `replay`, `+feature:copy-paste-replay` — реплей як текст у буфері; кращий реплей рівня зберігається.
- `+feature:insight-level` — Gain Insight відкриває легшу або «реміксовану» версію пазла; розвʼязати її треба самому.
- `level-editor`, `user-levels-browser` (вкладка Community Puzzles; фанатські розділи), `levels-sequential` + `level-unlock` (розділи відкриваються кількістю пройдених), досягнення Steam, хмарні сейви.
- `colorblind-palette`, `remap-controls`, `touch-controls` (віртуальні кнопки), `animation-toggle` (швидкість), Jukebox.

## Варіації й родичі
- `games/roguelike/achronal-dungeon.md` — інша гра Patashu з тими самими «зеленими» подіями, що не відмотуються.
- `games/thinky/meet-me-at-noon.md` — теж два персонажі з різним часом (один програє ходи назад, другий повторює); тут обидва ходять уперед і відмотуються незалежно.
- `games/thinky/theta-and-paralldox-on-worldlines.md` — розщеплення світу суперечливими ходами; інша модель «кількох ліній часу».
- `games/thinky/snakebird.md`, `games/grid-platformer/catrap.md` — покрокова гравітація з undo; Braid — світи, де частина обʼєктів не відмотується (схоже на зелений колір часу).
- **Осі варіацій:** чий хід відмотує undo — гри / окремого персонажа (тут) / окремого обʼєкта; що не відмотується — нічого / зелене / чекпойнт; довжина таймлайна — безмежна / ліміт / змінна (кристали).

## Цікавинки для курсу
- Два стеки undo на двох персонажів + глобальний мета-undo над ними — 🥈 (події ходу як дані, відкат лише своїх).
- Колір часу: таблиця «коли для сутності йде час» (сірий/червоний/синій/пурпуровий/зелений/білий) — 🥇, бо взаємодія з обома стеками нетривіальна.
- Сила проти ваги: числова таблиця WOODEN/IRON/STEEL і правило «Light слабшає в ланцюгу» — 📎.
- Гравітація з різною швидкістю падіння й «зависанням» після стрибка — 🥉.
- Кристали, що подовжують або замикають таймлайн, і поразка-парадокс — 🥈.
- Реплей як рядок у буфері обміну (копія = чекпойнт) — 📎.

## Мапа на каталог
- Є: `move-4dir`, `move-by-input`, `keyboard-controls`; `party-switch` ↔ Heavy/Light; `gravity-fall`, `ladder-climb`, `one-way-cell`, `impassable-cells`; `push-object`; `environment-death` ↔ шипи/вогонь/безодня; `destructible-blocks` ↔ дерево, скло; `reach-exit` + `all-on-targets` ↔ портали й цілі ящиків; `undo-redo`, `undo-unlimited`, `redo`, `restart-level` ↔ мета-undo; `replay`, `replay-window`; `level-select`, `level-unlock`, `sequential-levels`; `in-game-editor`, `editor-playtest`; `controls-remap`, `settings-window`, `main-menu`, `game-screen`, `sound-effects`, `background-music`, `save-progress`.
- **Нема** → пропозиції карток:
  - `+per-character-timeline` «Окремий undo-стек на кожного персонажа» · game-logic/history · 🥈.
  - `+meta-undo` «Undo над undo: скасувати відмотку або рестарт» · game-logic/history · 🥉.
  - `+timeline-length-limit` «Ліміт ходів таймлайна персонажа» · game-logic/history · 📎.
  - `+time-crystal` «Предмет змінює довжину таймлайна» · entities/state · 🥉.
  - `+time-colour` «Колір часу: коли сутність живе і чи відмотується» · game-logic/history · 🥇.
  - `+strength-vs-weight` «Сила того, хто штовхає, проти ваги обʼєкта» · entities/legality · 📎.
  - `+jump-hang` «Стрибок на 1 із зависанням на хід» · entities/move · 🌱.
  - `+sticky-top` «Хто стоїть на обʼєкті, їде з ним» · entities/move · 📎.
  - `+break-and-rewind` «Зламаний персонаж — стан, який відмотується, не поразка» · entities/state · 📎.
  - `+insight-level` «Легша версія пазла як підказка» · levels/progression · 🌱.

## Пропозиції до словників
- `+effect:rewind_actor(a)` — скасувати події останнього ходу таймлайна сутності (Entwined Time; не те саме, що `undo` гри).
- `+effect:timeline_slots(a, ±n)` — змінити довжину таймлайна / замкнути хід (кристали часу).
- `+cond:stronger(a, b)` — сила A ≥ вага B (поштовх ящиків різної ваги).
- `+ui:timeline-bar` — смуга ходів таймлайна персонажа з замкненими слотами.
- `+feature:insight-level` — легша / реміксована версія пазла замість підказки.
- `+feature:copy-paste-replay` — реплей як рядок у буфері, вставка = відновлення спроби.
- `+feature:undo-restart` — рестарт теж скасовується undo.
- `+axis:undo` — значення `per-actor` (окремий стек на персонажа).
- `+card:per-character-timeline`, `+card:time-colour` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Entwined Time](https://store.steampowered.com/app/3147300/Entwined_Time/) — ядро («own timelines that can independently record and rewind actions»), 12+ розділів, реплеї, Gain Insight, редактор, Community Puzzles; безкоштовно, 22.10.2024.
- [itch.io: Entwined Time](https://patashu.itch.io/entwined-time) — гра в браузері, платформи, Godot 3.5.3, devlog «1st Releaseiversary» (14.04.2025).
- [GitHub: Patashu/Entwined-Time](https://github.com/Patashu/Entwined-Time) — `GameLogic.gd` (переліки Tiles, Strength/Heaviness/Durability, `strength_check`, `time_passes`, `character_undo`, `check_won`, коментар про кольори часу, назви розділів, тексти навчання), `project.godot` (клавіші), сцени меню й налаштувань.
- YouTube: пошук «Entwined Time Patashu gameplay».

## Непевне
- (?) Розмір поля ~21×10 — з коду (`map_x_max_max`), можливий скрол у великих рівнях.
- (?) Точна дія зеленого кристала («додати хід» чи «розблокувати замкнений») залежить від стану таймлайна — у коді обидві гілки.
- (?) Перелік пізніх елементів (фазові блоки, бустери, схили, валуни, міміки, гравітація) — лише з назв плиток і розділів; поведінку не перевірено.
- (?) Розділи після «Victory Lap» («Voices from the Void», WIP-розділи) і фанатські набори — які з них входять у Steam-версію, не перевірено.
- (?) «Light зависає на хід перед падінням» — з коду (`floats`, коментар «Light floats gracefully downwards»); у грі може виглядати як повільне падіння.
