---
title: Asteroids Minesweeper
slug: asteroids-minesweeper
aka: []
family: hidden-deduction
also: []
klass: cursor
axes:
  field: 3d
  time: turn
  opponent: none
  info: hidden
  random: both
  goal: state
year: 2016
platforms: [PC (Windows), SteamOS / Linux, Windows-планшети]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/425070/Asteroids_Minesweeper/", best: true, note: "опис: 3D-сапер з обертанням, типи рівнів (вертикальний лічильник, рухомі міни, звʼязані куби), керування, Lua-моди"}
  - {kind: other, url: "https://www.gamegrin.com/reviews/asteroids-minesweeper-review/", note: "огляд GameGrin 8/10: 26 сусідів, знешкодження замість прапорців, 7 спроб, міни зсуваються після 5 ходів, кольорові обводки, опції"}
  - {kind: other, url: "https://3rd-strike.com/?p=48358", note: "огляд: обертати кластери кубів, 0-блоки, клавіша C, гроші → гаджети, інтел перед завданням"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=3163298108", note: "гайд досягнень: фази Tutorial, A–E, End of contract; 850 $ за міну; секрет через робочий компʼютер"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=750913221", note: "гайд модінгу: Loving Cube Engine, Lua, документація в теці documentation, -chdir"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Asteroids+Minesweeper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, neighbor-count-clue, line-sum-clue, keyboard-controls, round-currency, sequential-levels, difficulty-levels, game-settings, tutorial-window, game-screen, main-menu, settings-window, +camera-orbit, +disarm-instead-of-flag, +attempts-pool, +live-recount-clue, +moving-mines-deduction, +linked-cells, +shaped-board, +clear-zeros-key, +desk-computer-story, +lua-modding]
proposes: ["+axis:field=3d-26", "+effect:disarm", "+trigger:wrong_disarm", "+ui:3d-cursor", "+ui:column-counter", "+window:work-computer", "+card:disarm-instead-of-flag", "+card:attempts-pool", "+card:clear-zeros-key", "+card:desk-computer-story", "+card:lua-modding"]
author: opus
date: 2026-11-09
---

# Asteroids Minesweeper — сапер на 3D-астероїді з кубів: обертай, розбирай порожні куби, знешкоджуй міни

## Суть
Астероїд — кластер кубів (куб, порожнистий куб, сфера та інші форми), який гравець обертає в 3D і «обрізає» куб за кубом. Відкритий порожній куб показує кількість мін серед **26 сусідів** (замість 8 у 2D) і фарбується за цим числом. Прапорців нема: міну треба **знешкодити** окремою дією, а помилка в будь-який бік — клік по міні або «знешкодження» порожнього куба — коштує одну з 7 спроб. Окремі рівні додають модифікатори: лічильник мін у вертикальній колоні, міни, що переповзають у нерозкриті куби, і «заплутані» куби з однаковим станом.

## Поле і час
- Поле — 3D-кластер кубів довільної форми (куб, порожнистий куб, сфера…), камера обертається навколо (повне 3D). Внутрішні куби видно, коли зовнішні розібрано.
- Сусідство — 3×3×3 без центру = 26 кубів.
- Хід = одна дія над кубом; у рівнях з рухомими мінами міни зсуваються після кожних 5 ходів — тому `time: turn`. Без модифікатора поле статичне.
- Рівні: туторіальні, сюжетні фази (A–E, потім End of contract) з випадково згенерованими астероїдами, Custom (складність + додаткові опції).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Астероїд | zone | форма, розмір, складність | кластер кубів-клітин; мета — розібрати |
| Закритий куб | static | — | дія «розібрати» або «знешкодити» |
| Відкритий порожній куб | mark | 0–26, колір за числом | кількість мін серед 26 сусідів; перераховується після знешкоджень |
| 0-куб | mark | 0 | безпечний; клавіша C знімає всі 0-куби одразу |
| Міна | hazard | — | «розібрати» → вибух, −1 спроба; «знешкодити» → зникає, +850 $ |
| Рухома міна | hazard | крок раз на 5 ходів | переходить у нерозкритий куб |
| Звʼязані куби | zone | колір обводки | куби з однаковою обводкою мають однаковий вміст/стан |
| Вертикальний лічильник | mark | число на колону | кількість мін у вертикальній колоні кубів |
| Спроби | resource | 7 на старті | −1 за клік по міні або хибне знешкодження |
| Гроші компанії | resource | 850 $ за міну | що більше, то більше гаджетів |
| Гаджет / ефект | pickup | — | «нові ефекти й здібності» для складних астероїдів (?) |
| Робочий компʼютер | — | пароль, мережеві теки, звіти | сюжет: інтел перед завданням, секретна гілка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dismantle, c)` → ЯКЩО `not cell(c, mine)` → ТО `reveal(c)`, `custom: «куб показує кількість мін серед 26 сусідів і колір за числом»`.
- КОЛИ `input(dismantle, c)` → ЯКЩО `cell(c, mine)` → ТО `custom: «вибух»`, `lives(-1)` (спроба).
- КОЛИ `input(disarm, c)` → ЯКЩО `cell(c, mine)` → ТО `disappear`, `currency(+850)`, `custom: «відкриті куби навколо перераховують числа без цієї міни»`.
- КОЛИ `input(disarm, c)` → ЯКЩО `not cell(c, mine)` → ТО `lives(-1)`.
- КОЛИ `input(clear_zeros)` (клавіша C) → ТО `custom: «прибрати всі відкриті 0-куби, оголивши внутрішні»`.
- КОЛИ `counter(moves, ==, 5)` → ЯКЩО `mode(moving_mines)` → ТО `move(mine, unrevealed_cube)`, `counter(moves, =0)`.
- КОЛИ `input(dismantle, c)` → ЯКЩО `mode(entangled)` and `custom: «c має кольорову обводку»` → ТО `custom: «куб тієї ж обводки має той самий вміст і стан»`.
- Вертикальний лічильник: `custom: «число на колоні = кількість мін у вертикальній колоні»` — обмеження поверх 26-сусідства.
- КОЛИ `counter(attempts, ==, 0)` → ТО `lose`.
- КОЛИ `custom: «усі міни знешкоджено, порожні куби розібрано»` → ТО `win`, `next_level`.
- КОЛИ `counter(money, >=, n)` → ТО `unlock(gadget)`.
- КОЛИ `level_start` (сюжет) → ТО `message(intel)` — інтел про завдання і його вплив на компанію.
- Перемога: розібраний астероїд. · Поразка: 0 спроб. · Рахунок: гроші компанії (850 $ за знешкоджену міну).

## Керування і ввід
- Три схеми: екранні кнопки; вибір куба мишею або пальцем; 3D-курсор, який орієнтують клавіатурою або геймпадом Xbox 360.
- Обертання астероїда в 3D (обовʼязкове: цілі ховаються з інших боків).
- Дві дії над кубом — розібрати / знешкодити; знака питання нема — кожен клік остаточний.
- Клавіша C — масово зняти безпечні 0-куби.

## Вікна, меню, HUD
- `main-menu` → `level-select` (?): Tutorial · фази A–E · End of contract (відкривається після E) · Custom.
- `custom-window` Custom: складність + кілька додаткових опцій (за GameGrin — «небагато варіантів на кожне налаштування»).
- `game-screen`: астероїд у 3D (космічний фон вимкнено за замовчуванням), лічильник спроб (`lives`), гроші (`coins`) (?), `cursor` 3D.
- `custom-window` «робочий компʼютер» (`work-computer`): кнопка «i», пароль, Network shares, Recycle bin, відправлення data report — сюжетна і секретна гілки.
- `settings-window`: перемикач космічної графіки; роздільності, повноекранного режиму й повзунків звуку — нема (скарга GameGrin).
- `end-screen` (?) — результат астероїда.

## Фічі поза полем
- `tutorial` — туторіальні рівні; генерація випадкових астероїдів для реіграбельності.
- `custom-difficulty` — Custom-рівні.
- `mod-support`: Loving Cube Engine, правки Lua-файлів у `data/`; документація механік — `documentation/index.html`; окремий мод через `-chdir`.
- Steam: досягнення (Ethics fail — ≥589 знешкоджених мін; Curiosity killed the cat, Oops!, Ethics win — секретна сюжетна гілка).
- Сюжет-ARG: офісний телеворкер Abstract Space Industry Corp; історія проявляється наприкінці.

## Варіації й родичі
- [minesweeper](minesweeper.md) — база; [minesweeper-dimensions](minesweeper-dimensions.md) — 4D-сусідство і Timesweeper (рухомі міни); [globesweeper](globesweeper.md) — сапер на сфері; [14-minesweeper-variants](14-minesweeper-variants.md) — інші правила підказок; [venom-sweep](venom-sweep.md) — підказки, що перераховуються.
- Осі варіацій: **сусідство** 4 / 8 / 26 (3D) / 80 (4D); **позначка міни** — прапорець без ціни / знешкодження зі штрафом за помилку (тут); **міни** — статичні / рухаються раз на N ходів; **клітини** — незалежні / звʼязані парами за кольором; **додаткові підказки** — лише сусіди / лічильник колони.

## Цікавинки для курсу
- 3D-сітка з 26 сусідами + обертання камери + доступ лише до «оголених» кубів — 🥈.
- Знешкодження зі штрафом замість прапорця й пул спроб — 📎.
- Перерахунок чисел після знешкодження (підказка рахує лише живі міни) — 📎.
- Рухомі міни раз на 5 ходів: дедукція, що «старіє» — 🥈.
- Звʼязані куби з однаковим вмістом — 📎 (генерація з парами-клонами).
- Лічильник мін на вертикальну колону поверх 3D-сусідства — 📎.
- Рушій, де механіки — Lua-скрипти поверх двигуна кубів — 🥉 (як ідея архітектури).

## Мапа на каталог
- Є: `cell-click` ↔ вибір куба; `neighbor-count-clue` ↔ 26-сусідство; `line-sum-clue` ↔ вертикальний лічильник; `keyboard-controls` ↔ 3D-курсор; `round-currency` ↔ гроші за міни; `sequential-levels` ↔ фази; `difficulty-levels` ↔ Custom; `game-settings` + `settings-window`; `tutorial-window`; `game-screen` · `main-menu`.
- Корпус уже пропонує: `+camera-orbit`, `+live-recount-clue`, `+moving-mines-deduction`, `+linked-cells`, `+shaped-board`.
- **Нема** → пропозиції карток:
  - `+disarm-instead-of-flag` «Знешкодження як дія зі штрафом за помилку» · interface/input · 📎.
  - `+attempts-pool` «Пул спроб на поле (помилка = −1, не смерть)» · game-logic/lose · 🌱 · слот {attempts: 7}.
  - `+clear-zeros-key` «Масово прибрати безпечні 0-клітини однією клавішею» · interface/input · 🌱.
  - `+desk-computer-story` «Сюжет через вигаданий робочий компʼютер (пошта, теки, паролі)» · interface/menus · 🥉.
  - `+lua-modding` «Механіки як скрипти, що їх можна правити» · code · 🥉.

## Пропозиції до словників
- `+axis:field=3d-26` — 3D-сітка з повним 26-сусідством (уточнення `3d`, де сусідство зазвичай 6).
- `+effect:disarm` — знешкодити приховану небезпеку (уже пропонував Dragonsweeper).
- `+trigger:wrong_disarm` — дія «знешкодити» по безпечній клітині (окрема помилка, не вибух).
- `+ui:3d-cursor` — курсор у тривимірній сітці, керований клавіатурою/геймпадом; `+ui:column-counter` — підказка на колону в 3D.
- `+window:work-computer` — вікно-«робочий стіл» з теками, поштою й паролем як сюжетний інтерфейс.
- `+card:disarm-instead-of-flag`, `+card:attempts-pool`, `+card:clear-zeros-key`, `+card:desk-computer-story`, `+card:lua-modding` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Asteroids Minesweeper](https://store.steampowered.com/app/425070/Asteroids_Minesweeper/) — «Trim that asteroid», типи рівнів (tutorial, random, vertical counter, moving mines, matching/entangled cubes), три схеми керування, Lua, реліз 8.07.2016, Francois Braud (Volatile Dove).
- [GameGrin: огляд](https://www.gamegrin.com/reviews/asteroids-minesweeper-review/) — 26 кубів замість 8, колір за числом, disarm замість прапорця, 7 спроб і за що вони губляться, міни зсуваються після 5 ходів, лічильник колони на порожнистому кубі й сфері, кольорові обводки, опції.
- [3rd-strike: огляд](https://3rd-strike.com/?p=48358) — обертання кластерів, 0-блоки, клавіша C, гроші → гаджети, інтел перед завданнями, Custom-рівні.
- [Steam-гайд досягнень](https://steamcommunity.com/sharedfiles/filedetails/?id=3163298108) — фази Tutorial, A–E, End of contract; 850 $ за міну; секрет через робочий компʼютер і data report.
- [Steam-гайд модінгу](https://steamcommunity.com/sharedfiles/filedetails/?id=750913221) — Loving Cube Engine, Lua, документація, `-chdir`.

## Непевне
- (?) Як саме «розібрати» відрізняється від «відкрити»: чи відкритий порожній куб лишається в астероїді з числом, а прибирається окремо (як 0-куби клавішею C), — з оглядів не однозначно.
- (?) Куди переходить рухома міна — у сусідній чи будь-який нерозкритий куб, і чи випадково (тому `random: both`).
- (?) Чи відкриття одного звʼязаного куба автоматично відкриває пару.
- (?) Які саме гаджети/ефекти дають гроші і чи є магазин.
- (?) Чи є flood-відкриття нулів (огляди згадують лише клавішу C).
