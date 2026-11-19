---
title: N Step Steve (Part 1–2)
slug: n-step-steve
aka: [N Step Steve: part 1, N Step Steve: part 2, NSS]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2020
platforms: [web]
links:
  - {kind: itch, url: "https://epicpikaguy.itch.io/n-step-steve-part-1", best: true, note: "Part 1 у браузері; керування (стрілки/WASD, Z, Enter — мапа), FAQ; у коментарях — підказки (rot13) про прапорці, камені, мертвих Стівів"}
  - {kind: itch, url: "https://epicpikaguy.itch.io/n-step-steve-part-2", note: "Part 2 у браузері; автор: гравці, камені й прапорці — однакові «сутності»; редактор, криптиди, червоточини"}
  - {kind: play, url: "https://www.coolmathgames.com/0-n-step-steve", note: "Cool Math Games: інструкція — прапорець ставить лічильник = кількість крапок, «sometimes you need to run out of steps»"}
  - {kind: other, url: "https://docs.google.com/document/d/1dBC86RS_ULQSViPUuvWlQOZDTIY0S4CTEjcXWr6kYLk/edit?usp=sharing", note: "FAQ автора: сиквел 5 Step Steve, чому дві частини, дати"}
  - {kind: other, url: "https://www.bontegames.com/2020/12/n-step-steve-part-1-browser.html", note: "Bart Bonte; ~100 коментарів-підказок по кімнатах (рожеві прапорці, «higher number wins», лід, конвеєри)"}
  - {kind: itch, url: "https://epicpikaguy.itch.io/5-step-steve", note: "попередник 5 Step Steve (джем-версія, 2019)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=N+Step+Steve+walkthrough", note: "пошук; проходження"}
stage: v1
coverage: 50
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, checkpoint, respawn, player-death, touch-death, inertia-slide, carrier-platform, floor-types, item-pickup, collect-all, teleport, teleport-pair, map-window, undo-redo, undo-unlimited, restart-level, in-game-editor, state-string, level-exchange, save-autosave, save-progress, settings-window, controls-remap, pause-menu, main-menu, confirm-dialog, game-screen, +step-budget-refill, +sync-avatars, +multi-checkpoint-respawn, +corpse-blocker, +pushable-checkpoint, +duplicator-clone, +flip-screen-rooms, +quota-gate, +optional-collectibles, +collectible-secrets]
proposes: ["+feature:hold-to-undo", "+card:step-budget-refill", "+card:multi-checkpoint-respawn", "+card:pushable-checkpoint"]
author: opus
date: 2026-11-19
---

# N Step Steve — кроків лише стільки, скільки крапок на прапорці: смерть тут — інструмент, а відроджених Стівів може бути кілька

## Суть
Кіт-дослідник Стів рятує розкиданих по планеті кошенят. Світ складено з кімнат-екранів, і в кожній лічильник кроків: наступив на прапорець з k крапками — лічильник став k; не встиг до наступного прапорця — Стів гине, а його тіло лишається на полі як штовхана річ. Рожеві прапорці — точки відродження; якщо кілька таких «засвічено» одночасно, після смерті відроджується кілька Стівів, і всі вони ходять синхронно. Камені штовхають прапорці, тіла й інші камені; лід, конвеєри, шипи, клонери й статуї множать комбінації. Сиквел 5 Step Steve (2019), автор Ethan Clark (EPICPIKAGUY); Part 1 — грудень 2020, Part 2 — грудень 2022.

## Поле і час
- Кімната — квадратна сітка 16×16 (з даних гри); кімнати мають координати (x, y) і стикуються краями: Стів, що вийшов за край, опиняється в сусідній кімнаті (`+flip-screen-rooms`).
- Шари: підлога (порожньо, стіна, лід, конвеєр, шипи, клонер, бар'єр) · сутності (Стіви, тіла, камені, прапорці, статуї, зірки) · «гнучкі» обʼєкти поза логікою (таблички, телепорти).
- Хід = один крок; усі живі Стіви крокують одночасно в одному напрямку; лічильник кроків спільний.
- Part 1: 9 кошенят, коза-секрет, 16 зірок (з даних кімнат). Part 2 — «значно більша», з червоточинами, криптидами й редактором.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Стів | player | живий / мертвий | крок у 4 напрямки синхронно з іншими Стівами; штовхає камені й тіла |
| Тіло Стіва | object | — | лишається, де Стів загинув; штовхається; ним можна закрити шипи чи доштовхати до кошеняти/зірки |
| Прапорець (синій) | switch | 0–9 крапок | Стів, що став на нього, ставить лічильник = крапки; сам Стів його не штовхає, камінь — штовхає |
| Прапорець-checkpoint (рожевий) | switch | 0–9 крапок, засвічений | як синій + точка відродження; кілька засвічених → стільки ж Стівів після відродження |
| Зламаний прапорець | static | — | вимкнений прапорець (?) |
| Камінь | object | — | штовхається; штовхає прапорці, тіла (і зірки в Part 2) |
| Кошеня | pickup | імʼя, репліка | дотик Стіва (і тіла — у Part 2) рятує; «Rescued Kittens» |
| Зірка | pickup | — | необовʼязкова; відчиняє замки; «Collected Stars» |
| Замок | gate | потрібно N кошенят або N зірок | пропускає, коли зібрано достатньо; інакше пише, скільки бракує |
| Лід | terrain | — | ковзання до упору; ковзання через прапорець поповнює кроки |
| Конвеєр (зелена стрілка) | terrain | напрям | щоходу зсуває сутність на 1; зустрічні стрілки гойдають її туди-сюди |
| Шипи (червоні) | hazard | — | Стів гине; тіло лишається на шипах |
| Клонер (верт. / гориз.) | spawner | орієнтація | сутність, заштовхнута в нього, роздвоюється, якщо поруч є місце |
| Статуя | hazard | — | «Don't look at the statues!»; перетворює Стіва на камінь (?) |
| Бар'єр | static | — | (?) |
| Телепорт-база | static | — | точка, куди переносить мапа |
| Табличка | static | текст | підказки й лор у світі |
| Коза | pickup | секрет | «Rescued Goats: 1» |
| Червоточина (Part 2) | terrain | пара за id | після відкриття переносить на парну; дві одночасні — у секретну кімнату з криптидом |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(steve, dir)` для кожного живого Стіва одночасно, `counter(steps, -1)`.
- КОЛИ `contact(steve, rock|corpse)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `contact(rock, flag)` → ЯКЩО `free(cell_behind)` → ТО `push` — прапорці зсувають лише штовханими сутностями.
- КОЛИ `enter(steve, flag)` → ТО `set_value(steps, pips)` — лічильник = кількість крапок; ЯКЩО `custom: «Стіви стоять на кількох прапорцях»` → ТО `custom: «береться більше число»`.
- КОЛИ `enter(steve, pink_flag)` → ТО `checkpoint`, `set_state(pink_flag, lit)`; `custom: «засвічуються рожеві прапорці, на яких Стіви стоять разом; новий дотик перезаписує набір»` (?).
- КОЛИ `counter(steps, ==, 0)` → ЯКЩО `not cell(steve_cell, flag)` → ТО `transform(steve, corpse)` (усі живі Стіви).
- КОЛИ `enter(steve, spikes)` → ТО `transform(steve, corpse)`.
- КОЛИ `input(dir)` → ЯКЩО `count(live_steve, ==, 0)` → ТО `respawn(steve, кожен засвічений рожевий прапорець)` («Move again to restart»).
- КОЛИ `enter(x, ice)` → ТО `slide(x, dir)`; ЯКЩО `custom: «шлях ковзання проходить через прапорець»` → ТО `set_value(steps, pips)`.
- КОЛИ `enter(x, conveyor)` → ТО `move(x, arrow_dir)` щоходу.
- КОЛИ `custom: «сутність заштовхнуто в клонер»` → ЯКЩО `free(cells_beside)` → ТО `clone(x)` (?).
- КОЛИ `contact(steve, kitten)` → ТО `pickup`, `counter(kittens, +1)`, `message(kitten_dialog)`.
- КОЛИ `contact(steve, star)` → ТО `pickup`, `counter(stars, +1)`.
- КОЛИ `contact(steve, lock)` → ЯКЩО `counter(kittens|stars, >=, N)` → ТО `disappear_b`; інакше `block`, `message(«N more …»)`.
- КОЛИ `edge(steve)` → ТО `custom: «Стів переходить у сусідню кімнату»`.
- КОЛИ `input(Enter)` → ТО `window(map-window)`; вибір відкритої бази → `teleport(steve, base)`.
- КОЛИ `enter(steve, wormhole)` (Part 2) → ТО `teleport(steve, pair)`; КОЛИ `custom: «два Стіви одночасно проходять два різні переходи»` → ТО `teleport(steve, cryptid_room)`.
- КОЛИ `input(Z)` → ТО `undo(1)` (Part 1 — у межах кімнати, Part 2 — і між кімнатами); пауза → Restart Room → `restart`.
- Перемога: врятовано всіх кошенят → фінал; додатково — секретні кінцівки (зламаний телепорт, коза). Поразка тимчасова: смерть — частина розвʼязку, undo без ліміту.

## Керування і ввід
- Стрілки або WASD — крок усіх живих Стівів; Z — undo (опція «Hold to Undo» — утримання повторює); Enter — мапа; на мапі вліво/вправо — вибір бази, Enter — телепорт.
- Пауза — меню з рестартом кімнати; клавіші можна перепризначити (Remap Keys).
- Part 2, редактор: курсор і палітра тайлів, «Set player start», «Set / Erase barriers», колір і музика кімнати, «Copy level to clipboard» / «Load level from clipboard», «Play level».

## Вікна, меню, HUD
- `main-menu`: «Press any key to start!»; `confirm-dialog` «Start a new game?».
- `dialogue-window`: вступна історія (катастрофа корабля, кошенята в капсулах), репліка кожного врятованого кошеняти, таблички в кімнатах.
- `game-screen`: кімната на весь екран; лічильник кроків показано крапками на Стіві/прапорці (?).
- `map-window`: сітка відкритих кімнат, бази-телепорти, лічильники «Collected Stars», «Rescued Kittens», «Rescued Goats»; Part 2 — трекер криптидів.
- `pause-menu`: Resume · Restart Room · Settings · Credits (?).
- `settings-window`: Audio (Music), Video (Post Processing), Gameplay (Hold to Undo), Remap Keys, Restore to Defaults.
- `editor-window` (Part 2): редактор рівня з копіюванням рівня рядком.
- Переходи: main-menu → game-screen ⇄ map-window (Enter) → телепорт; game-screen → pause-menu → settings-window.

## Фічі поза полем
- `undo` без ліміту, `restart-level` (кімнати); автозбереження в localStorage браузера, у Part 2 — резервні копії збереження з вибором.
- Відкритий світ: кімнати в будь-якому порядку, `world-map`-подібна мапа з телепортами, замки за кількістю зірок і кошенят.
- `collectibles`: зірки (необовʼязкові, «can be very hard»), коза, у Part 2 — криптиди-камео з трекером і галерея.
- Part 2: `level-editor` + `level-sharing` рядком (гравці постять рівні в коментарях), червоточини.
- Налаштування: музика, постобробка, «Hold to Undo», перепризначення клавіш; на itch заявлено «Color-blind friendly» та «Interactive tutorial» (навчання через перші кімнати й таблички).

## Варіації й родичі
- **5 Step Steve** (2019, джем Extra Credits; Kongregate, Cool Math) — той самий світ, але завжди 5 кроків між прапорцями, мертві й кілька Стівів уже є; запис черги можна закрити цим файлом.
- Part 1 → Part 2: undo між кімнатами, червоточини, криптиди, редактор, значно більший світ; «нові конвеєри працюють інакше» (репліка кошеняти) (?).
- [Baba Is You](baba-is-you.md) — автор називає її натхненням; синхронні аватари як «кілька YOU». [Tres Undos](tres-undos.md), [Snakebird](snakebird.md) — смерть / відкат як частина розвʼязку.
- Осі варіацій: **запас кроків** — фіксований (5) / за прапорцем (N) / додається («зелені» прапорці в X Step Steve (?)) · **смерть** — кінець / тіло-обʼєкт + відродження · **відродження** — один Стів / по одному на кожен засвічений checkpoint · **хто штовхає прапорець** — ніхто / камінь / Стів.

## Цікавинки для курсу
- Спільний лічильник кроків, що скидається прапорцями (з правилом «більше число перемагає» для кількох аватарів) — 🌱.
- Смерть як дія: тіло стає штовханим обʼєктом, а відродження множить аватарів за кількістю засвічених checkpoint — 🥉.
- Синхронний рух кількох аватарів з колізіями між собою і штовханням (порядок обробки!) — 🥈.
- Світ кімнат-екранів зі стиком країв, мапою й телепортами між базами — 🥉; undo через межі кімнат — 📎.
- Редактор рівня з рядком-кодом для обміну (copy/paste) — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `move-by-input` + `keyboard-controls`; `push-object` ↔ камені й тіла; `checkpoint` + `respawn` ↔ рожеві прапорці; `player-death` + `touch-death` ↔ кроки скінчились / шипи; `inertia-slide` ↔ лід; `carrier-platform` ↔ конвеєри; `floor-types` ↔ лід, конвеєри, шипи; `item-pickup` + `collect-all` ↔ кошенята; `teleport` ↔ бази на мапі; `teleport-pair` ↔ червоточини; `map-window`; `undo-redo` + `undo-unlimited` + `restart-level`; `in-game-editor` + `state-string` + `level-exchange` (Part 2); `save-autosave` + `save-progress`; `settings-window` + `controls-remap`; `pause-menu`, `main-menu`, `confirm-dialog`, `game-screen`.
- **Нема** → пропозиції карток:
  - `+step-budget-refill` «Запас кроків, який прапорець виставляє на своє число» · entities/state · 🌱 — родич `move-limit`.
  - `+multi-checkpoint-respawn` «Відродження на кожному засвіченому checkpoint — аватарів стає більше» · game-logic/lose · 🥉.
  - `+pushable-checkpoint` «Checkpoint — сутність, яку можна посунути іншими обʼєктами» · entities/interact · 🌱.
  - `+sync-avatars`, `+corpse-blocker`, `+duplicator-clone`, `+flip-screen-rooms`, `+quota-gate`, `+optional-collectibles`, `+collectible-secrets` — уже в корпусі.

## Пропозиції до словників
- `+feature:hold-to-undo` — утримання клавіші undo повторює відкат (опція налаштувань).
- `+card:step-budget-refill`, `+card:multi-checkpoint-respawn`, `+card:pushable-checkpoint` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch.io: N Step Steve part 1](https://epicpikaguy.itch.io/n-step-steve-part-1) — гра, керування (Arrows/WASD, Z, Enter), FAQ; коментарі: «you can push flags using rocks», undo не працює між кімнатами, коза, секретна кінцівка, 9 кошенят / 16 зірок.
- [itch.io: N Step Steve part 2](https://epicpikaguy.itch.io/n-step-steve-part-2) — автор про сутності (гравці, камені, прапорці — однаково) і «гнучкі» обʼєкти; дублікатор, знищувач клонів, «Pink = Checkpoint, Blue = Regular», криптиди через два переходи одночасно, редактор, localStorage.
- [Cool Math Games: N Step Steve](https://www.coolmathgames.com/0-n-step-steve) — офіційна інструкція: ліміт кроків, прапорець ставить лічильник = крапки, таблички, Z — undo, «run out of steps to solve a puzzle».
- [FAQ автора (Google Docs)](https://docs.google.com/document/d/1dBC86RS_ULQSViPUuvWlQOZDTIY0S4CTEjcXWr6kYLk/edit?usp=sharing) — сиквел 5 Step Steve, поділ на дві частини, Part 2 — грудень 2022.
- [bontegames: n step steve part 1](https://www.bontegames.com/2020/12/n-step-steve-part-1-browser.html) — підказки гравців: «When cats are on two different flags, the higher number wins», «Sliding over flag = recharge», рожеві прапорці множать Стівів, «Split the cat», зелені стрілки.
- [itch.io: 5 Step Steve (jam)](https://epicpikaguy.itch.io/5-step-steve) — «only move 5 steps between checkpoints», клік по прапорцю — чит-телепорт.
- Збірки обох частин (SDL/Emscripten, `index.data`): каталог тайлів (лід, конвеєри, шипи, клонери, бар'єр, прапорці 1–9, зламаний, камінь, статуя), кімнати 16×16, тексти табличок, меню й налаштувань, реплики кошенят, замки з кількістю зірок/кошенят.

## Непевне
- (?) Статуя: табличка «Don't look at the statues!» і підказки гравців («turn the other cat into a rock») — схоже, статуя камʼянить Стіва, на якого «дивиться»; точне правило не перевірено.
- (?) Клонер: напрям, куди виходять копії, і що копії зберігають напрям — з коментарів, не з правил.
- (?) Бар'єр і зламаний прапорець — поведінка не знайдена.
- (?) Точний момент смерті (на 0 після кроку чи при спробі кроку з 0) і як саме засвічується набір рожевих прапорців.
- (?) Чи може тіло (не живий Стів) рятувати кошеня в Part 1; у Part 2 — так (кастомний рівень гравця, автор рівня підтвердив задум).
- (?) «Зелені» прапорці, що додають кроки, — з гри X Step Steve (Playmath) за словами гравця; у NSS не перевірено.
