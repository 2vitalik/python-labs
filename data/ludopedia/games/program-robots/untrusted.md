---
title: Untrusted — or the Continuing Adventures of Dr. Eval
slug: untrusted
family: program-robots
also: [roguelike, thinky]
klass: hybrid
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: setup
  goal: state
year: 2014
platforms: [web]
links:
  - {kind: play, url: "https://untrustedgame.com/", best: true, note: "грати в браузері: редактор коду, API Reference, Level Select"}
  - {kind: official, url: "https://github.com/AlexNisnevich/untrusted", note: "відкритий код: формат рівнів .jsx, маркери editable, бонус-рівні, rot.js + CodeMirror"}
  - {kind: other, url: "https://raw.githubusercontent.com/AlexNisnevich/untrusted/master/scripts/reference.js", note: "повний довідник API: map.*, player.*, object.*, validate*"}
  - {kind: other, url: "https://github.com/AlexNisnevich/untrusted/tree/master/levels", note: "21 рівень + credits + bonus; код кожного рівня"}
  - {kind: other, url: "https://raw.githubusercontent.com/AlexNisnevich/untrusted/master/levels/03_validationEngaged.jsx", note: "приклад validateLevel: мінімум блоків і рівно один вихід"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=untrusted+javascript+game+walkthrough", note: "пошук; проходження"}
stage: v1
coverage: 75
mechanics: [move-4dir, impassable-cells, push-object, item-pickup, inventory-items, key-and-door, teleport-pair, chase-greedy, touch-death, projectile-shot, reach-exit, interaction-table, maze-generation, level-from-txt, sequential-levels, level-select, game-screen, help-window, music-toggle, +editable-locked-code, +level-validation, +exit-condition-hook, +object-definition-api, +code-editor-window, +user-procedures, +key-override, +phone-callback, +runtime-error-stop, +api-reference-window, +level-reset-execute, +bonus-levels-mod, +notepad]
proposes: ["+trigger:exec(cmd)", "+trigger:level_start", "+trigger:validate", "+trigger:on_exit", "+trigger:phone", "+cond:validate_count(kind, op, n)", "+effect:define_object(type, props)", "+effect:override_key(key, fn)", "+effect:crash", "+effect:killed_by(text)", "+role:item", "+window:code-editor", "+window:api-reference", "+window:notepad", "+ui:locked-lines", "+ui:status-line", "+feature:code-unlock-items", "+feature:mod-support", "+axis:control"]
author: opus
date: 2026-11-02
---

# Untrusted — роглайк, де рівень і є програма: допиши незаблоковані рядки JavaScript

## Суть
Dr. Eval (символ `@`) мусить вибратися з «MACHINE CONTINUUM». Кожен рівень у завантаженому вигляді **непрохідний**; поруч з картою відкритий JavaScript-код цього рівня, більшість рядків заблоковані (червоне тло), а кілька — редаговані. Гравець змінює ці рядки (поставити менше стін, перевизначити поведінку дрона, виставити телепорт, перемалювати клавішу), натискає Execute — рівень перезбирається з новим кодом. Перевірки `validateLevel` і `onExit` відкидають грубі обходи, тож треба знайти дозволену «щілину» в правилах.

## Поле і час
- Квадратна сітка-консоль (rot.js): клітина = символ + колір + колір тла (`map.setSquareColor`). Розмір мапи — сталий для гри (`map.getWidth/Height`), розміщення в коді — координатами (x, y) від лівого верхнього кута.
- Шари: тло клітини · статичні обʼєкти (`block`, `exit`, `tree`…) · динамічні обʼєкти (дрони, роботи, снаряди) · гравець · верхнє полотно для малювання ліній (`map.getCanvasContext`).
- Час двох рівнів: **код** виконується один раз при Execute (`startLevel`) — це `programmed`-фаза; далі гра покрокова: на кожен хід гравця кожен `dynamic`-обʼєкт раз викликає свій `behavior`. Плюс таймери `map.startTimer` (≥25 мс) — справжній real-time у деяких рівнях.
- Видимість повна; випадковість — у генерації (`ROT.Map.DividedMaze`, `map.getRandomColor`) і в чужих поведінках, які пише сам рівень.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Dr. Eval (`@`) | player | колір, інвентар | рух 4 напрямки; `player.move` — один крок на функцію |
| Стіна `block` | static | — | непрохідна |
| Вихід `exit` | static | — | вхід → `onExit(map)`; true → наступний рівень |
| Компʼютер | pickup | — | з ним відкривається редактор коду (без нього — лише рух) (?) |
| Телефон (function phone) | pickup | callback | клавіша Q викликає функцію `setPhoneCallback` — «друга кнопка дії» |
| Ключі (red/green/blue/yellow) | pickup | колір | відкривають барʼєри/умови виходу |
| Барʼєр | gate | `passableFor: ['robot']` | непрохідний для гравця, прохідний для визначених типів |
| Атакуючий дрон | enemy | `dynamic`, символ `d` | `behavior`: жадібний крок до найближчого гравця; `onCollision` → `player.killedBy` |
| Робот | ally | `dynamic`, символ `R` | поведінку **пише гравець** (`me.move`, `me.canMove`); дотик до гравця → `giveItemTo(player, key)` |
| Телепорт | terrain | ціль `setTarget` | переносить на інший телепорт |
| Міна / невидимі пастки | hazard | — | дотик → смерть; видимі лише якщо перефарбувати клітину (?) |
| Дерево, вода, пліт | terrain | — | рівні-варіації: ліс з генерацією, річка з плотом (?) |
| Лазер | hazard | колір | вбиває гравця, якщо його колір не збігається (?) |
| Користувацький обʼєкт | будь-яка | `type: item|dynamic|—`, `symbol`, `color`, `impassable(player, me)`, `onCollision`, `behavior`, `onDestroy`, `pushable`, `projectile` | усе, що гравцеві дозволено визначити через `map.defineObject` |
| Снаряд | projectile | `projectile: true` | знищує те, у що влучив, і сам зникає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(execute)` → ТО `custom: «перезапустити startLevel(map) з поточним кодом»`, далі `validate`.
- КОЛИ `validate` → ЯКЩО `validateLevel(map)` кидає помилку (`validateAtLeastXObjects`, `validateExactlyXManyObjects`, `validateAtMostXObjects`, `validateAtMostXDynamicObjects`, `validateNoTimers`, `validateAtLeastXLines`) → ТО `crash` — рівень не завантажується, текст помилки в консолі.
- КОЛИ `exec(map.placeObject(x, y, type))` → ЯКЩО `free(cell)` → ТО `spawn_at(type, cell)`; у деяких рівнях — перевірка на перезапис (`allowOverwrite`) (?).
- КОЛИ `exec(map.defineObject(type, props))` → ТО `define_object(type, props)` — новий тип лише в межах рівня.
- КОЛИ `input(arrow)` → ЯКЩО `not impassable(next)` → ТО `move(player, dir)`; `pushable` обʼєкт → `push`; `map.overrideKey(key, fn)` → ТО `override_key` (стрілка робить інше).
- КОЛИ `turn_end(player)` → ТО для кожного `dynamic` — `behavior(me)`; `me.move(dir)` лише раз на хід.
- КОЛИ `contact(player, object)` → ТО `onCollision(player)` цього типу (вбити, дати предмет, телепортувати).
- КОЛИ `contact(player, item)` → ТО `pickup` (у інвентар; `player.hasItem` у перевірках).
- КОЛИ `contact(projectile, x)` → ТО `disappear_both`; КОЛИ `destroyed(dynamic)` → ТО `onDestroy`.
- КОЛИ `contact(player, exit)` → ЯКЩО `onExit(map)` = true (напр. `has(player, computer)`, `has(player, redKey)`) → ТО `next_level`; інакше `message(«Don't forget to pick up the computer!»)`, `block`.
- КОЛИ `objective(map)` = true → ТО `next_level` одразу (рівні без виходу) (?).
- КОЛИ `input(phone)` → ЯКЩО `has(player, phone)` → ТО `custom: «викликати phone-callback»` (перемкнути колір, світло, телепорт…).
- КОЛИ `exec(player.killedBy(text))` → ТО `lose`, `message(text)` → рівень з початку (Reset).
- КОЛИ `custom: «виняток JS у коді гравця»` → ТО `crash`, рядок помилки в консолі; попередній стан рівня лишається (?).
- Перемога рівня: дійти до виходу з виконаною умовою `onExit` · Поразка: смерть від дрона/міни/снаряду → перезапуск · Рахунку нема; є прихований бонус — пройти рівень «не так, як задумав автор».

## Керування і ввід
- Стрілки (або hjkl (?)) — рух `@`; `Q` — телефон.
- Ctrl+1 API Reference · Ctrl+2 перемкнути фокус карта/редактор · Ctrl+3 Notepad · Ctrl+4 Reset (повернути рівень і код до початку) · Ctrl+5 Execute · Ctrl+0 Menu.
- Редактор CodeMirror: курсор не заходить у заблоковані рядки; маркери `#BEGIN_EDITABLE#…#END_EDITABLE#` (цілі рядки) і `#{#…#}#` (шматок рядка) визначають, що можна змінити.
- Код — справжній JavaScript: цикли, функції, замикання; `map.timeout`/`map.startTimer` для асинхронності.

## Вікна, меню, HUD
- `game-screen`: ліворуч поле rot.js з рядком статусу (`map.writeStatus`), заголовком розділу (`displayChapter`); праворуч `code-editor` з підсвіткою заблокованих рядків; нижче — консоль повідомлень/помилок; панель кнопок `^1…^5`, `Q Phone`, `^0 Menu`.
- `api-reference` (^1) — довідник команд, що вже «відкриті» на поточному рівні (`commandsIntroduced`).
- `notepad` (^3) — нотатник гравця між рівнями.
- `level-select` (Menu) — дерево файлів `/levels/`, `/scripts/`, `/bonus/`: пройдені рівні як файли.
- `credits-window` — рівень 22 «credits».
- HUD: `locked-lines`, `status-line`, іконка mute.
- Переходи: старт → intro → рівень 1; Execute → нова версія рівня; exit → наступний `.jsx`; Menu → Level Select.

## Фічі поза полем
- `sequential-levels` (21 рівень у розділах) + `level-select` пройдених; прогрес зберігається в браузері (?).
- `code-unlock-items`: можливості гравця — предмети на полі (компʼютер = редактор, телефон = callback); API росте з рівнями.
- `restart-level` (Reset), `music-toggle` (саундтрек; трек задає рівень), `rules-page` (API Reference).
- `mod-support`: бонус-рівні `.jsx` у `levels/bonus`, збірка `make mod=…`, власні команди документуються в `reference.js`.
- Нема undo в класичному сенсі — є Reset коду рівня.

## Варіації й родичі
- Рівні як міні-курс: Cell Block A (прибрати стіну), The Long Way Out (лабіринт `DividedMaze`), Validation Engaged (обійти `validateLevel`), Multiplicity, Minesweeper, Drones 101, Colors, Into the Woods, Fording the River, Ambush, Robot / Robot Nav / Robot Maze (запрограмувати робота), Crisps Contest, Exceptional Crossing, Lasers, Pointers, Super Dr. Eval Bros, Document Object Madness, Boss Fight, End of the Line.
- Родичі: Baba Is You (правила як обʼєкти — тут правила як код), hackmud, Bitburner, Else Heart.Break() (редагування коду світу), CodeCombat (JS-керування героєм).
- Осі варіацій: **що редагує гравець** (програму аватара / код рівня / правила-слова); **гранулярність замка** (весь рівень / рядки / частини рядка); **захист від читу** (нема / валідація стану / перевірка на виході).

## Цікавинки для курсу
- Рівень як Python-модуль з `start_level(map)`, частина рядків якого заблокована, а гравець вводить свій код — 🥇 (пісочниця `exec`, маркери, перезбирання).
- `validate_level` як набір інваріантів («≥N стін», «рівно 1 вихід», «без таймерів») — 🥉.
- `define_object(type, {symbol, impassable, on_collision, behavior})` — таблиця взаємодій як дані/функції — 🥈 (картка `interaction-table`).
- `on_exit(map)` — умова виходу як функція, а не клітина — 📎.
- Дрон з `behavior` «жадібно до гравця» і робот, поведінку якого пише гравець (`me.can_move`, `me.move`) — 🥉.
- Перевизначення клавіш (`override_key`) і «телефон» як callback — 📎.
- Консольний рендер rot.js з кольором тла клітини як окремим шаром — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` · `push-object` (`pushable`) · `item-pickup` + `inventory-items` (компʼютер, телефон, ключі) · `key-and-door` (барʼєри/ключі) · `teleport-pair` (`setTarget`) · `chase-greedy` (дрон `moveToward`) · `touch-death` · `projectile-shot` · `reach-exit` · `interaction-table` (`onCollision`/`impassable` як функції) · `maze-generation` (`DividedMaze`) · `level-from-txt` (`createFromGrid` з рядків) · `sequential-levels` · `level-select` · `game-screen` · `help-window` (API) · `music-toggle`.
- **Нема** → пропозиції карток:
  - `+editable-locked-code` «Код рівня із заблокованими й відкритими рядками» · levels/format · 🥇.
  - `+level-validation` «Інваріанти рівня після зміни коду» · levels/solvability · 🥉 · слоти {checks: list}.
  - `+exit-condition-hook` «Вихід з умовою-функцією» · game-logic/win · 📎.
  - `+object-definition-api` «Новий тип обʼєкта з поведінкою на рівень» · entities · 🥈.
  - `+code-editor-window` (є з Karel) · `+user-procedures` (функції JS) · `+runtime-error-stop` (виняток → рівень не стартує).
  - `+key-override` «Перевизначити дію клавіші» · interface/input · 📎.
  - `+phone-callback` «Предмет = користувацька функція на клавіші» · entities/state · 📎.
  - `+api-reference-window` «Довідник API, що росте з рівнями» · interface/menus (#window) · 📎.
  - `+level-reset-execute` «Execute/Reset: перезбирання рівня з коду» · interface/input · 📎.
  - `+bonus-levels-mod` «Бонус-рівні як файли-моди» · levels/editor · 🥉.
  - `+notepad` «Нотатник гравця в грі» · interface · 🌱.

## Пропозиції до словників
- `+trigger:exec(cmd)` — спільний для сімʼї; `+trigger:level_start` — є ⏳ (`startLevel`); `+trigger:validate` — після збирання рівня; `+trigger:on_exit` — спроба вийти; `+trigger:phone` — використано предмет-функцію.
- `+cond:validate_count(kind, op, n)` — інваріант кількості (уже близько до ⏳ `count`, але як перевірка коду гравця).
- `+effect:define_object(type, props)` — оголосити тип; `+effect:override_key(key, fn)`; `+effect:crash` — 🔥 з Karel; `+effect:killed_by(text)` — смерть з причиною (= `lose` + `message`).
- `+role:item` — предмет-здатність (компʼютер, телефон), відмінний від `pickup`-ефекту тим, що відкриває інтерфейс.
- `+window:code-editor` 🔥 · `+window:api-reference` · `+window:notepad`.
- `+ui:locked-lines` — заблоковані рядки коду з підсвіткою; `+ui:status-line` — рядок статусу під картою.
- `+feature:code-unlock-items` — можливості відкриваються предметами на полі; `+feature:mod-support` — ⏳ уже є, тут бонус-рівні.
- `+axis:control` — `direct` аватар + `programmed` світ: гравець програмує не себе, а рівень.

## Джерела
- ⭐ [Untrusted — грати](https://untrustedgame.com/) — гра в браузері з редактором, API Reference, Level Select.
- [GitHub: AlexNisnevich/untrusted](https://github.com/AlexNisnevich/untrusted) — README: автори (Alex Nisnevich, Greg Shuflin), маркери editable, properties рівня, бонус-рівні, ліцензія.
- [reference.js](https://raw.githubusercontent.com/AlexNisnevich/untrusted/master/scripts/reference.js) — повний API: map.*, player.*, object.*, validate*, canvas.
- [Список рівнів](https://github.com/AlexNisnevich/untrusted/tree/master/levels) — 21 рівень + credits.
- [03_validationEngaged.jsx](https://raw.githubusercontent.com/AlexNisnevich/untrusted/master/levels/03_validationEngaged.jsx) — приклад validateLevel.
- YouTube: пошук «untrusted javascript game walkthrough».

## Непевне
- (?) Рік 2014 — з памʼяті й черги; README року не вказує.
- (?) Розмір мапи (у памʼяті 50×25) — не перевірено.
- (?) Поведінка мін, лазерів, плоту й дерев — висновок з назв рівнів (Minesweeper, Lasers, Fording the River, Into the Woods), коду цих рівнів не читав.
- (?) Що саме дає компʼютер (без нього редактор недоступний) і чи зберігається прогрес у localStorage — з памʼяті.
- (?) `objective(map)` як альтернатива виходу — є в API, на яких рівнях — не перевіряв; поведінка при винятку в `behavior` — з памʼяті.
- (?) Клавіші hjkl — не перевірено; на сторінці гри видно лише ^0–^5 і Q.
