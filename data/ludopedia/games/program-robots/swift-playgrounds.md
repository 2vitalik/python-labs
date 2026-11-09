---
title: Swift Playgrounds (Learn to Code, Byte)
slug: swift-playgrounds
aka: [Learn to Code, Everyone Can Code Puzzles, Byte]
family: program-robots
also: []
klass: avatar
axes:
  field: layers
  time: programmed
  opponent: none
  info: full
  random: setup
  goal: collect
year: 2016
platforms: [iPad, Mac]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Swift_Playgrounds", best: true, note: "що це, Byte/Blu/Hopper, iPad 2016, Mac 2020, SwiftUI-застосунки"}
  - {kind: official, url: "https://developer.apple.com/swift-playgrounds/", note: "Apple: уроки-пазли, playgrounds, SwiftUI, iPad/Mac"}
  - {kind: other, url: "https://education-static.apple.com/teaching-code/learn-to-code-solutions.pdf", note: "Apple Education: розвʼязки Learn to Code 1–2 — назви розділів, увесь API світу"}
  - {kind: other, url: "https://developer.apple.com/forums/thread/703779", note: "форум: Roll Right Roll Left, while і isBlocked"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=swift+playgrounds+learn+to+code+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [command-program, user-procedures, sensor-predicates, height-levels, teleport, teleport-pair, button-toggle, orientation-state, collect-all, completion-detection, code-editor-window, step-execution, tutorial-window, level-select, sequential-levels, save-progress, game-screen, end-screen, +real-language-code, +code-built-level, +multi-character-program, +lock-raises-platform, +portal-toggle-by-code, +random-level-layout, +array-world-building]
proposes: ["+effect:jump(a)", "+effect:lift(a, ±level)", "+feature:code-built-level", "+feature:lesson-book", "+window:lesson-page", "+ui:camera-orbit", "+ui:code-completion-bar", "+cond:standing_on(a, kind, state)"]
author: opus
date: 2026-11-09
---

# Swift Playgrounds (Learn to Code) — Swift-кодом веди Byte по 3D-сітці островів: самоцвіти, перемикачі, портали, сходи, платформи

## Суть
У застосунку Apple для iPad/Mac уроки Learn to Code — це пазли: на ізометричному 3D-острові з клітин стоїть персонаж (Byte, пізніше Blu, Hopper, Expert), і гравець пише справжній Swift: `moveForward()`, `turnLeft()`, `collectGem()`, `toggleSwitch()`. Мета рівня — зібрати всі самоцвіти й увімкнути всі перемикачі. Уроки йдуть за поняттями програмування: команди → функції → цикли `for` → умови → логічні оператори → `while` → алгоритми → змінні → типи (властивість `isActive` порталу) → ініціалізація (`let expert = Expert()`) → параметри → побудова світу кодом (`world.place(...)`) → масиви. Незвичне: пізні рівні змушують **будувати сам рівень кодом** — ставити блоки, сходи, портали, персонажів.

## Поле і час
- Квадратна сітка клітин з **висотами**: блоки, сходи (`Stair`, з напрямком), вода, рухомі платформи на рівнях (`Platform(onLevel: 4, controlledBy: lock)`); у клітині можна поставити кілька `Block()` — стовпчик.
- Координати `column`/`row` (від 0); `world.allPossibleCoordinates`, `world.coordinates`, `world.row(...)` для обходу.
- Камера 3D, обертається й наближається (?); видимість повна.
- Час `programmed`: код запускається кнопкою, персонаж виконує команди з анімацією; швидкість і покроковий режим (?).
- Випадковість: у частині рівнів кількість/місця самоцвітів і розміри прямокутників змінюються між запусками (`randomNumberOfGems`, «Random Rectangles», «Randomized Lands») — розвʼязок мусить бути загальним.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Byte (`Character()`) | player | позиція, напрямок | рухається, повертає, збирає самоцвіти, перемикає, `jump()` (?) |
| Blu, Hopper | player | імʼя (`Character(name: .blu)`) | як Byte; кілька персонажів на рівні |
| Expert (`Expert()`) | player | позиція, напрямок | усе, що персонаж, плюс `turnLockUp()` / `turnLockDown()` |
| Самоцвіт (`Gem()`) | pickup | — | `collectGem()` на клітині — зникає, лічильник |
| Перемикач (`Switch()`) | switch | відкритий / закритий | `toggleSwitch()` на клітині змінює стан; ціль — усі відкриті |
| Портал (`Portal(color:)`) | gate | колір, початок і кінець, `isActive` | вхід у початок → вихід з кінця; вимкнений — не переносить |
| Замок (lock) | switch | повʼязані платформи | Expert крутить вгору/вниз — платформи піднімаються/опускаються |
| Платформа (`Platform`) | platform | рівень висоти, замок | рухається по вертикалі за замком; по ній ходять |
| Блок (`Block()`) | terrain | висота стовпчика | підлога/стіна залежно від висоти; ставиться кодом |
| Сходи (`Stair()`) | terrain | напрямок | дозволяють перейти на сусідню висоту |
| Вода (`Water()`) | hazard | — | непрохідна клітина (?) |
| Край / перепад висоти | static | — | `isBlocked` = попереду не пройти |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(moveForward)` → ЯКЩО `free(front)` → ТО `move(character, forward)`; інакше `block` (персонаж упирається).
- КОЛИ `exec(turnLeft)` / `exec(turnRight)` → ТО `face(character, ±90°)`; `turnAround` — власна функція з двох поворотів.
- КОЛИ `exec(collectGem)` → ЯКЩО `occupied(here, gem)` → ТО `pickup`, `counter(gems, +1)`.
- КОЛИ `exec(toggleSwitch)` → ЯКЩО `occupied(here, switch)` → ТО `set_state(switch, open|closed)` (інвертувати).
- КОЛИ `enter(character, portal_start)` → ЯКЩО `state(portal, active)` → ТО `teleport(character, portal_end)`.
- КОЛИ `custom: «код присвоює portal.isActive = false/true»` → ТО `set_state(portal, inactive|active)`.
- КОЛИ `exec(turnLockUp)` → ЯКЩО `custom: «Expert стоїть перед замком»` → ТО `custom: «усі платформи цього замка +1 рівень»`; `turnLockDown` — −1.
- КОЛИ `exec(jump)` → ТО `custom: «персонаж стрибає вперед на клітину іншої висоти»` (?).
- КОЛИ `exec(world.place(item, column, row, facing))` → ТО `spawn_at(item, (column, row))` — до старту руху; блоки стосуються, сходи й портали — пари клітин.
- КОЛИ `exec(world.removeItems(at))` → ТО `disappear_b` (прибрати предмети з клітини).
- Сенсори в умовах `if` / `while`: `isBlocked`, `isBlockedLeft`, `isBlockedRight` ↔ `not free(dir)`; `isOnGem` ↔ `occupied(here, gem)`; `isOnClosedSwitch` / `isOnOpenSwitch` ↔ `occupied(here, switch) and state(switch, closed|open)`.
- КОЛИ `program_end` → ЯКЩО `all_gone(gem)` and `custom: «усі перемикачі відкриті»` → ТО `win`, `window(end-screen)`.
- КОЛИ `program_end` → ЯКЩО `count(gem, >, 0)` or `custom: «є закритий перемикач»` → ТО `message(«ще не все»)`, повторити.
- КОЛИ `custom: «на рівні з випадковою кількістю самоцвітів»` → ТО `custom: «розвʼязок має працювати для будь-якої розкладки (лічильник gemCounter < totalGems)»`.
- КОЛИ `custom: «зайвий/хибний виклик (collectGem на порожній клітині)»` → ТО `custom: «персонаж показує, що не може»` (?) — без поразки.
- Перемога: усі самоцвіти зібрано й усі перемикачі відкриті · Поразка: нема, лише «спробуй ще» · Рахунок: нема.

## Керування і ввід
- Набір Swift-коду: на iPad — панель підказок-автодоповнення з командами, «coding keyboard», дотик для редагування (перетягнути дужку, щоб обгорнути код).
- Кнопка Run My Code; повторний запуск після правки; перегляд кроків (?).
- Пізні уроки: оголошення змінних, функцій з параметрами (`move(distance:)`), масивів (`[Coordinate]`), циклів `for coordinate in blockLocations`.
- Камера: жестами обертати й наближати 3D-сцену (?).

## Вікна, меню, HUD
- `main-menu` застосунку: Мої playgrounds + каталог уроків (Learn to Code 1, 2, 3, інші книги) (?).
- `lesson-page` — сторінка уроку: текст пояснення зліва, код + 3D-світ (?); `level-select` — перелік сторінок розділу з позначкою пройденого.
- `game-screen`: редактор коду, 3D-острів, кнопка запуску, `hint-button` (?).
- `tutorial-window` — вступні сторінки з поясненням понять перед пазлами.
- `end-screen` — «сторінку пройдено», перехід на наступну.
- Переходи: каталог → книга → розділ → сторінка-пазл → (успіх) наступна сторінка.

## Фічі поза полем
- `levels-sequential` за поняттями; розділи Learn to Code: Commands, Functions, For Loops, Conditional Code, Logical Operators, While Loops, Algorithms, Variables, Types, Initialization, Parameters, World Building, Arrays.
- `code-built-level` — `world.place(Block()/Stair()/Portal/Character/Gem)` будує рівень під час виконання; «World Creation» — власний світ.
- `random-level-layout` — частина рівнів генерує випадкову кількість/розкладку самоцвітів.
- `save-progress`, синхронізація між iPad і Mac через iCloud Drive.
- `hint`, `tutorial`, `accessibility` (VoiceOver; уроки «Swan's Quest»), `localization`.
- Поза пазлами: playgrounds з SpriteKit, Bluetooth, камерою; керування роботами (Lego Mindstorms EV3, Sphero, дрони Parrot); SwiftUI-застосунки й відправка в App Store Connect (версія 4.0+).

## Варіації й родичі
- Learn to Code 1 (основи) → 2 (змінні, типи, ініціалізація, параметри, побудова світу) → 3 (масиви, світ кодом) (?) — назви розділів з офіційного PDF.
- Родичі в корпусі: [Lightbot](lightbot.md) (ізометричні висоти, але іконки), [Karel](karel.md) (сенсори `frontIsClear` ≈ `isBlocked`), [CodeCombat](codecombat.md) (справжня мова, API героя), [Block maze games](block-maze-games.md) (блоки замість тексту), [Kara](kara.md).
- **Осі варіацій**: хто будує рівень (автор / код гравця) · скільки акторів і чи різні в них API (Character vs Expert) · умова перемоги (дійти / зібрати все / перемкнути все) · фіксований чи випадковий рівень.

## Цікавинки для курсу
- Сітка з висотами: блоки-стовпчики, сходи, перевірка «можна пройти» — 🥉.
- Портали з `isActive`, що код вмикає/вимикає — 📎.
- Замок і платформи на різних висотах (Expert) — 🥉.
- Рівень, який будує код гравця (`world.place`) — 🥈 (API для створення світу, валідація).
- Кілька персонажів з різними можливостями в одній програмі — 🥉.
- Випадкова кількість самоцвітів: перевірка, що розвʼязок загальний — 📎.
- Ізометричний 3D-рендер сітки — 🥈.

## Мапа на каталог
- Є в каталозі: `command-program` ↔ Swift-команди; `user-procedures` ↔ `func solveStair()`; `sensor-predicates` ↔ `isBlocked`, `isOnGem`; `height-levels` ↔ блоки й сходи; `teleport`/`teleport-pair` ↔ портали; `button-toggle` ↔ замок керує платформами; `orientation-state` ↔ напрямок персонажа; `collect-all`, `completion-detection`; `code-editor-window`; `step-execution` (?); `tutorial-window`, `level-select`, `sequential-levels`, `save-progress`, `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+real-language-code` «Справжня мова керує сутністю» · game-logic/program · 🥈 (спільна з CodeCombat).
  - `+code-built-level` «Код гравця розставляє елементи рівня» · levels/editor · 🥈.
  - `+multi-character-program` «Одна програма керує кількома різними акторами» · game-logic/program · 🥉.
  - `+lock-raises-platform` «Замок піднімає/опускає платформи» · entities/interact · 📎.
  - `+portal-toggle-by-code` «Стан порталу як змінна» · entities/interact · 🌱.
  - `+random-level-layout` «Випадкова розкладка рівня між запусками» · levels/generation · 📎.
  - `+array-world-building` «Масиви координат для обходу/побудови світу» · game-logic/program · 📎.

## Пропозиції до словників
- `+effect:jump(a)` — стрибок на сусідню клітину іншої висоти.
- `+effect:lift(a, ±level)` — вертикальний рух платформи (замок).
- `+cond:standing_on(a, kind, state)` — «стою на предметі виду в стані» (`isOnClosedSwitch`) — коротше за `occupied and state`.
- `+feature:code-built-level` — рівень будує код гравця.
- `+feature:lesson-book` — уроки як книга сторінок з поясненням і пазлом.
- `+window:lesson-page` — сторінка уроку: текст + код + світ.
- `+ui:camera-orbit` — обертання 3D-сцени жестом.
- `+ui:code-completion-bar` — панель автодоповнення команд над клавіатурою.

## Джерела
- ⭐ [Wikipedia: Swift Playgrounds](https://en.wikipedia.org/wiki/Swift_Playgrounds) — iPad 2016, Mac 2020, Byte/Blu/Hopper, роботи й дрони, SwiftUI 4.0.
- [Apple Developer: Swift Playgrounds](https://developer.apple.com/swift-playgrounds/) — уроки-пазли, iPad-редагування, Mac, iCloud.
- [Learn to Code solutions (PDF)](https://education-static.apple.com/teaching-code/learn-to-code-solutions.pdf) — назви всіх розділів і сторінок; `moveForward`, `collectGem`, `toggleSwitch`, `isBlocked*`, `isOnGem`, `isOnClosedSwitch`, `Portal.isActive`, `Expert.turnLockUp/Down`, `Character.jump`, `world.place`, `Block/Stair/Platform/Water`, `randomNumberOfGems`.
- [Apple Developer Forums: Roll Right Roll Left](https://developer.apple.com/forums/thread/703779) — типовий застряг з `while` і `isBlocked`.

## Непевне
- (?) Точна семантика `jump()` (вгору/вниз на 1 чи через проміжок) і `Water` (непрохідна чи падіння).
- (?) Чи є покрокове виконання й регулятор швидкості в Learn to Code; кнопка підказок.
- (?) Розподіл розділів між Learn to Code 2 і 3 — PDF містить усі розділи підряд.
- (?) Що буває при хибній команді (немає поразки — з памʼяті).
- (?) Вигляд головного меню й сторінки уроку; жести камери.
