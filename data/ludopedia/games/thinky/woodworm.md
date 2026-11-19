---
title: Woodworm
slug: woodworm
aka: [Woodworm Classic]
family: thinky
also: [dig-gravity]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2024
platforms: [web, PICO-8, Windows, macOS, Linux]
links:
  - {kind: itch, url: "https://spratt.itch.io/woodworm-classic", best: true, note: "оригінал PICO-8, безкоштовно в браузері: стрілки — рух, Z — undo, X — рестарт, ще раз X — до вибору рівня"}
  - {kind: steam, url: "https://store.steampowered.com/app/3404590/Woodworm/", note: "розширена версія 2025-12-09: нова графіка й звук, більше головоломок, контролер, 4 досягнення, Steam Cloud"}
  - {kind: itch, url: "https://spratt.itch.io/woodworm", note: "та сама нова версія на itch ($9.99+); оновлення 1.1 — 7 нових головоломок, кілька слотів збереження, Mac/Linux"}
  - {kind: other, url: "https://www.lexaloffle.com/bbs/?pid=149969", note: "перший пост на Lexaloffle BBS (2024-06-15), картридж woodworm-0, ліцензія CC4-BY-NC-SA"}
  - {kind: other, url: "https://www.lexaloffle.com/bbs/cposts/wo/woodworm-0.p8.png", note: "картридж PICO-8: код Lua, 17 рівнів (зразок + брусок), опора й падіння, перевірка форми"}
  - {kind: other, url: "https://spratt.itch.io/woodworm/devlog/1365065/woodworm-11-update", note: "devlog оновлення 1.1"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Woodworm+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, move-by-input, keyboard-controls, body-queue, no-reverse-turn, gravity-fall, dig-terrain, undo-unlimited, restart-level, level-select, puzzle-select, save-progress, save-multi-slot, controls-remap, particles, movement-animation, help-window, main-menu, game-screen, background-music, sound-effects, +carve-to-shape, +glued-blocks, +segment-support, +avatar-supports-blocks, +side-cling, +offscreen-return, +physical-reference, +trophy-shelf]
proposes: ["+cond:matches_shape", "+effect:eat", "+role:reference", "+window:trophy-shelf", "+card:carve-to-shape", "+card:glued-blocks", "+card:avatar-supports-blocks", "+card:side-cling", "+card:offscreen-return", "+card:physical-reference", "+card:trophy-shelf"]
author: opus
date: 2026-11-19
---

# Woodworm — личинка з трьох сегментів вигризає дерев'яний брусок, доки не лишиться точна копія фігурки-зразка; відгризене, що ні за що не тримається, падає

## Суть
Пазл Samuel Pratt (spratt): спершу PICO-8-картридж (Lexaloffle BBS, 2024-06-15, тепер «Woodworm Classic», 17 рівнів), потім розширена версія для Steam та itch (2025-12-09) з новою графікою, звуком і більшою кількістю головоломок. Поле видно збоку: на столі ліворуч стоїть фігурка-зразок, праворуч — суцільний дерев'яний брусок.

Личинка-шашіль повзає в 4 напрямки, і кожен крок у дерево з'їдає клітину. Дерево склеєне між сусідами: шматок, що після прогризання вже ні за що не тримається, падає; личинка теж падає, якщо їй нема на що спертися. Рівень пройдено, коли решта дерева — точна копія зразка (зсув дозволено, поворот ні); з'їдене назад не повертається, тож плануй, що відкусити і що скинути.

## Поле і час
- Оригінал (з коду): поле 25×12 клітин по 4 px, вигляд збоку з гравітацією; під нижнім рядом — стіл, опора для всього.
- Перед стартом зразок і брусок «падають» на стіл, потім між ними зʼявляється личинка.
- Брусок у 17 рівнях оригіналу — суцільний прямокутник на 20–90 клітин (від 4×5 до 9×10); зразок — 10–41 клітина.
- Хід = крок личинки (кілька кадрів анімації); після кроку — пошук опори й падіння: усе, що не тримається, опускається на клітину за раз з прискоренням, доки поле не осяде; потім перевірка форми.
- Краї: личинка може виповзти за межу екрана — тоді рука повертає її на бік бруска.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Личинка (шашіль) | player | 3 сегменти: голова + 2 | крок у 4 напрямки, але не назад у шию; крок у дерево з'їдає клітину; хвіст підтягується |
| Дерево | object | склейка з кожним із 4 сусідів | з'їдається; падає, якщо не має опори |
| Шматок дерева | object | склеєна група клітин | падає цілим; приземлившись, лежить на опорі без нових склейок |
| Зразок (фігурка) | static | форма рівня | не їсться й не проходиться; фізичний: на нього можна залізти; з ним порівнюють решту дерева |
| Стіл | static | під нижнім рядом | опора для всього |
| Рука | neutral | — | повертає личинку, що виповзла за край; переносить пройдену фігурку на полицю |
| Торт | object | після всіх рівнів | з'їси весь — повернення в меню |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух і їжа:
- КОЛИ `input(dir)` → ЯКЩО `custom: «напрям не протилежний останньому кроку»` and `not cell(target, sample)` and `custom: «ціль не нижче столу»` → ТО `move(head, dir)`, `custom: «хвіст підтягується, довжина лишається 3»`.
- КОЛИ `enter(head, wood)` → ТО `disappear(wood)`, `custom: «сусідні клітини втрачають склейку з нею»` — шашіль з'їдає клітину, щойно кінчилась анімація кроку.

Опора й падіння (після кожного кроку, доки поле не осяде):
- КОЛИ `turn_end(player)` → ЯКЩО `not supported(wood)` → ТО `fall(wood)` — опора: стіл, опорна клітина просто під деревом або склейка з опорною клітиною збоку чи згори; угору опора передається завжди, убік і вниз — лише через склейку.
- КОЛИ `turn_end(player)` → ЯКЩО `not supported(worm)` → ТО `fall(worm)` — личинку тримає стіл, опорне дерево чи зразок під будь-яким сегментом або опорна клітина ліворуч чи праворуч від середнього сегмента.
- КОЛИ `turn_end(player)` → ЯКЩО `supported(worm)` → ТО `custom: «клітини просто над сегментами теж опорні»` — дерево може лежати на личинці.
- КОЛИ `settled` → ТО `custom: «шматок, що впав, лежить без склейки з новими сусідами»`.

Край і перемога:
- КОЛИ `edge(worm)` → ЯКЩО `custom: «голова далеко за краєм екрана»` → ТО `respawn(worm, block_side)` — рука повертає її до бруска з того боку, куди вона пішла, і личинка падає на поле.
- КОЛИ `settled` → ЯКЩО `custom: «решта дерева клітина в клітину збігається зі зразком (зсув дозволено, поворот ні), поза нею порожньо»` → ТО `win`, `custom: «блиск по фігурці, рука несе її на полицю»`, `window(level_select)`.
- КОЛИ `custom: «пройдено всі рівні»` → ТО `spawn(cake)`.
- КОЛИ `all_gone(cake)` → ТО `window(main_menu)`.
- Перемога: збіг зі зразком · Поразки нема: зайве з'їдене не повертається — undo чи рестарт · Рахунку й лічильника кроків нема.

## Керування і ввід
- Стрілки — крок; одне натискання запамʼятовується, поки триває анімація (буфер вводу).
- Z (кнопка O PICO-8) — undo; X — рестарт рівня; X одразу після рестарту — назад до полиць.
- Меню: X — далі (титул → довідка → полиці), Z — назад; стрілки — вибір фігурки на полицях (по 6 у ряд), X — грати.
- Нова версія: повна підтримка контролера, режим «лише клавіатура», переназначення клавіш (devlog 1.1 згадує виправлений збій при переназначенні).

## Вікна, меню, HUD
- `main-menu`: титул — банка з личинками й логотип.
- `help-window`: три стікери — «move worm with» і намальовані стрілки, «carve a replica of the object in each level to progress!».
- `level-select` (`trophy-shelf`): полиці з мініатюрами зразків по 6; обрану рука тримає над полицею; пройдені стоять вирізьбленими фігурками.
- `game-screen`: стіл із зразком ліворуч і бруском праворуч, стружка-частинки при кожному укусі; HUD нема.
- `end-screen`: після збігу — блиск по фігурці, рука забирає її на полицю.
- `custom-window`: фінал — рука приносить торт, який теж можна з'їсти.
- Пауза-меню PICO-8: пункт «erase save data».
- Переходи (камера панорамує між ними): титул → довідка → полиці → рівень → (збіг) полиці → … → (усі) торт → титул.

## Фічі поза полем
- `level-select` вільний: в оригіналі всі рівні відкриті з початку (з коду); прогрес — бітова маска пройдених у cartdata, останній обраний рівень пам'ятається.
- `undo` ∞ — журнал змін клітин і положень личинки; `restart-level`.
- Нова версія (Steam/itch): кілька слотів збереження (1.1), Steam Cloud, 4 досягнення, колірні альтернативи, налаштування гучності, гра без вимог до таймінгу; 1.1 переставила й підправила частину рівнів і змінила рух («easier to control»).
- Нагорода за все: торт.

## Варіації й родичі
- Версії: Woodworm (PICO-8, 2024; на itch тепер «Woodworm Classic», 17 рівнів) → Woodworm (Steam/itch, 2025; нові головоломки, графіка й музика) → 1.1 (2026: +7 головоломок, слоти, Mac/Linux).
- Тіло з гравітацією й опорою будь-яким сегментом — [Snakebird](snakebird.md); черв'як, що прогризає ґрунт, — [WOIM](woim.md); копання без падіння ґрунту — [Dig Dug](../dig-gravity/dig-dug.md); падіння без опори — [Boulder Dash](../dig-gravity/boulder-dash.md).
- Ціль «форма, а не вихід» — [Cyborg Earthworm](../program-robots/cyborg-earthworm.md) (зафарбувати шаблон), тут — скульптура відʼємним простором.
- Осі варіацій: **що стається з викопаним** — тунель, ґрунт стоїть (Dig Dug) / шматки без опори падають (тут) / сипучий пісок; **ціль** — дійти до виходу / лишити задану форму (тут); **опора тіла** — будь-який сегмент знизу (Snakebird) / ще й бічне чіпляння середнім сегментом (тут); **чи тримає аватар блоки** — ні / так, дерево може лежати на личинці (тут).

## Цікавинки для курсу
- Склейки як 4 біти на клітину + пошук опори обходом від столу (угору завжди, вбік і вниз — лише по склейці) — 🥉.
- Падіння шматків по клітині за тік з прискоренням і личинка як опора — 📎.
- Перевірка «решта = зразок» з точністю до зсуву — 📎.
- Тіло з 3 сегментів без розвороту назад + бічне чіпляння — 🌱.
- Undo як журнал змін (diff клітин), а не повні знімки поля — 📎.
- Розвʼязувач: стан = множина клітин дерева + личинка; що відкусити, щоб після всіх падінь лишився зразок — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` ↔ стрілки; `body-queue` ↔ 3 сегменти; `no-reverse-turn` ↔ не назад у шию; `gravity-fall` ↔ дерево й личинка падають без опори; `dig-terrain` ↔ укус: дерево → порожньо (але тут решта падає); `undo-unlimited` · `restart-level`; `level-select` + `puzzle-select` ↔ полиці зі статусом; `save-progress` ↔ cartdata; `save-multi-slot` ↔ слоти 1.1; `controls-remap` ↔ нова версія; `particles` ↔ стружка; `movement-animation` ↔ панорами камери й падіння; `help-window` · `main-menu` · `game-screen`; `background-music` · `sound-effects`.
- **Нема** → пропозиції карток:
  - `+carve-to-shape` «Вигризти зайве, щоб лишилась форма-зразок» · game-logic/win · 🥉 · слоти {match: translate; rotate: no}.
  - `+glued-blocks` «Клітини склеєні; шматок без опори падає цілим» · entities/move · 🥉.
  - `+segment-support` (Snakebird, є в корпусі) — опора будь-яким сегментом.
  - `+avatar-supports-blocks` «Аватар — опора для блоків над ним» · entities/move · 📎.
  - `+side-cling` «Середній сегмент чіпляється за опору збоку» · entities/move · 🌱.
  - `+offscreen-return` «Вийшов за екран — тебе повертають на поле» · entities/move · 🌱.
  - `+physical-reference` «Зразок цілі стоїть на полі як тверде тіло» · interface/hud · 🌱.
  - `+trophy-shelf` «Вибір рівня — полиця з пройденими фігурками» · interface/menus · 🌱.

## Пропозиції до словників
- `+cond:matches_shape` — решта обʼєктів збігається з зразком (з точністю до зсуву).
- `+effect:eat` — аватар з'їдає клітину-матеріал, на яку ступив (тепер — `disappear` + `custom`).
- `+role:reference` — зразок цілі на полі: тверде тіло, з яким порівнюють.
- `+window:trophy-shelf` — полиці з фігурками як вибір рівня.
- `+card:carve-to-shape`, `+card:glued-blocks`, `+card:avatar-supports-blocks`, `+card:side-cling`, `+card:offscreen-return`, `+card:physical-reference`, `+card:trophy-shelf` — див. «Мапу».

## Джерела
- ⭐ [Woodworm Classic на itch.io](https://spratt.itch.io/woodworm-classic) — оригінал у браузері (PICO-8), керування, рейтинг 4.8 з 511, посилання на нову версію.
- [Steam: Woodworm](https://store.steampowered.com/app/3404590/Woodworm/) — опис («grid-based puzzle game about carving bite-sized wooden sculptures», гравітація й геометрія), «expansion and re-imagining of the original PICO-8 hit», реліз 9 Dec 2025, Samuel Pratt, платформи, контролер, досягнення, Steam Cloud (також `store.steampowered.com/api/appdetails?appids=3404590`: 4 досягнення, Color Alternatives, Keyboard Only Option, Playable without Timed Input).
- [Woodworm на itch.io](https://spratt.itch.io/woodworm) і [devlog 1.1](https://spratt.itch.io/woodworm/devlog/1365065/woodworm-11-update) — нова версія: +7 головоломок, слоти збереження, Mac/Linux, зміни руху й порядку рівнів.
- [Lexaloffle BBS](https://www.lexaloffle.com/bbs/?pid=149969) і [картридж woodworm-0](https://www.lexaloffle.com/bbs/cposts/wo/woodworm-0.p8.png) — пост 2024-06-15; код Lua (розібрано з PNG): 17 рівнів, склейки й опора, падіння, рух личинки, перевірка форми, undo, полиці, торт.
- YouTube: пошук «Woodworm puzzle gameplay».

## Непевне
- (?) Механіки нової версії описано за оригіналом PICO-8; чи додала вона нові матеріали чи елементи, з опису Steam і devlog не видно (гравці згадують лише нові фігури: якір, ліжко).
- (?) Кількість головоломок у новій версії ніде не названа; відомо лише «+7» в оновленні 1.1.
- (?) Рушій нової версії — Love2D, за словами одного коментатора itch; не перевірено.
- (?) Фанатські версії (Woodworm+, Woodworm 2) згадуються на Lexaloffle BBS — не відкривав.
- (?) Рік: черга дає 2025 (Steam); перший реліз — PICO-8 2024-06-15, тому `year: 2024`.
