---
title: Karel the Robot (Reeborg's World)
slug: karel
family: program-robots
also: []
klass: avatar
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: setup
  goal: state
year: 1981
platforms: [book, PC, web]
links:
  - {kind: play, url: "https://reeborg.ca/reeborg.html", best: true, note: "Reeborg's World — Karel на справжньому Python у браузері, з редактором світів"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Karel_(programming_language)", note: "Pattis 1981, примітиви, сенсори, нащадки"}
  - {kind: official, url: "https://reeborg.ca/docs/en/reference/index.html", note: "довідник команд Reeborg"}
  - {kind: official, url: "https://reeborg.ca/docs/en/basics/index.html", note: "туторіал Reeborg: Home, Newspaper, Hurdles, Harvest, Storm"}
  - {kind: official, url: "https://compedu.stanford.edu/karel-reader/docs/python/en/reference.html", note: "Stanford Karel (Python): команди й умови"}
  - {kind: official, url: "https://cs.stanford.edu/people/eroberts/karel-the-robot-learns-java.pdf", note: "Karel the Robot Learns Java (Stanford CS106A)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=reeborg%27s+world+python+tutorial", note: "пошук; розбори задач"}
stage: v1
coverage: 70
mechanics: [impassable-cells, inventory-items, item-pickup, reach-exit, collect-all, level-select, in-game-editor, editor-palette, editor-erase, editor-playtest, level-exchange, state-as-data, replay, game-screen, help-window, +command-program, +sensor-predicates, +user-procedures, +runtime-error-stop, +goal-state-check, +step-execution, +random-world-variants, +code-editor-window]
proposes: ["+trigger:program_end", "+trigger:exec(cmd)", "+effect:crash", "+window:code-editor", "+ui:instruction-highlight", "+ui:step-counter", "+feature:goal-check", "+feature:random-variants", "+axis:control"]
author: opus
date: 2026-11-02
---

# Karel the Robot — робот на сітці вулиць, якому пишеш програму з чотирьох команд

## Суть
Гравець не керує роботом напряму: він пише програму з кількох примітивів (`move`, `turn_left`, `put_beeper`, `pick_beeper`) і сенсорів (`front_is_clear`, `beepers_present`…), натискає Run — і дивиться, як Карел її виконує. Мета кожної задачі — привести світ у заданий стан (робот у точці, біпери розкладені). Ядро — мінімальна мова: навіть `turn_right` треба визначити самому через три `turn_left`. Reeborg's World — браузерний нащадок на справжньому Python, з автоперевіркою цілі й випадковими варіантами світу, щоб програма не була «записом рухів».

## Поле і час
- Квадратна сітка: горизонталі — **streets**, вертикалі — **avenues**; перетини (**corners**) — клітини. Світ обмежений стінами по краях; усередині — стіни між сусідніми перетинами (стіна стоїть **на ребрі**, не займає клітину).
- Шари клітини: тло (у Stanford Python — колір клітини, `paint_corner`; у Reeborg — плитки: трава, вода, багно, лід…) + обʼєкти (біпери або в Reeborg токени, зірки, морква тощо, лічильник на клітину) + робот з орієнтацією N/E/S/W.
- Час `programmed`: тік = одна виконана інструкція-дія. Програма виконується послідовно до кінця, до `done()`/`turnoff` або до помилки. Швидкість анімації налаштовується; є покроковий режим.
- Видимість — повна: світ видно цілком; «невідоме» з'являється лише як випадковий варіант світу при кожному запуску (Reeborg: Hurdles 3–4, Storm (?)).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Карел / Reeborg | player | позиція, напрям N/E/S/W, сумка біперів (число або ∞) | виконує команди програми; сам нічого не вирішує |
| Стіна (на ребрі) | static | між двома клітинами | `move` крізь неї → помилка «врізався» |
| Межа світу | static | — | як стіна |
| Біпер (beeper) / обʼєкт Reeborg | pickup | кількість на клітині; тип (токен, зірка, морква…) | `pick_beeper/take` переносить у сумку; `put_beeper/put` — із сумки на клітину |
| Сумка біперів | — (інвентар) | N або нескінченно | джерело для `put`; порожня → помилка |
| Колір клітини (Stanford Python) | mark | колір | `paint_corner(c)` фарбує; `corner_color_is(c)` перевіряє |
| Плитка тла (Reeborg) | terrain | трава/гравій/лід/вода/багно… (?) | частина плиток небезпечна (вода, багно — робот «застрягає»/тоне) (?) |
| Твердий обʼєкт (Reeborg: паркан, міст) | static | — | паркан непрохідний; міст дозволяє перетнути воду (?) |
| Ціль: дім/прапор | static | позиція (+ напрям) | наприкінці робот має стояти тут |
| Ціль: обʼєкти | mark | кількість і тип на клітинах | наприкінці кількість обʼєктів має збігтися з ціллю |
| Ціль: стіни (Reeborg) | mark | — | наприкінці мають стояти саме ці стіни (`build_wall`) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(move)` → ЯКЩО `free(front)` → ТО `move(karel, facing)`; інакше `crash` («врізався у стіну»).
- КОЛИ `exec(turn_left)` → ТО `face(karel, left)`; поворот праворуч — лише як процедура користувача (`def turn_right(): repeat 3: turn_left()`).
- КОЛИ `exec(pick_beeper)` → ЯКЩО `occupied(here, beeper)` → ТО `pickup`, `counter(bag, +1)`; інакше `crash`.
- КОЛИ `exec(put_beeper)` → ЯКЩО `has(karel, beeper)` → ТО `spawn_at(beeper, here)`, `counter(bag, -1)`; інакше `crash`.
- Сенсори — без побічних ефектів, повертають bool: `front_is_clear` ↔ `free(front)`; `left_is_clear`/`right_is_clear` ↔ `free(left|right)`; `beepers_present` ↔ `occupied(here, beeper)`; `beepers_in_bag` ↔ `has(karel, beeper)`; `facing_north…` ↔ `facing(karel, dir)`; кожен має заперечну форму (`front_is_blocked`…).
- Reeborg: `object_here()`/`carries_object()` повертають список типів обʼєктів; `at_goal()` ↔ `custom: «робот на клітині-цілі»`; `is_facing_north()` — єдиний напрямковий сенсор; `wall_in_front`/`wall_on_right` (?) — окремо від `front_is_clear`, бо вода теж «не clear».
- Керування потоком: `if/else`, `while <сенсор>`, `repeat n` (Reeborg; n — лише літерал), `for … in range` (Python), визначення нових інструкцій (`DEFINE-NEW-INSTRUCTION` у Pattis 1981, `def` у Python), рекурсія дозволена.
- КОЛИ `exec(done|turnoff)` → ТО `custom: «зупинити програму»` і перевірка цілі.
- КОЛИ `program_end` → ЯКЩО `custom: «стан світу = ціль (позиція, обʼєкти, стіни)»` → ТО `win` («завдання виконано»); інакше `message(«ціль не досягнуто»)`.
- КОЛИ `crash` → ТО `custom: «error shutoff: програма зупиняється, робот лишається на місці»`, `lose` для цієї спроби.
- КОЛИ `custom: «перевищено ліміт кроків»` → ТО `crash` (захист від нескінченного циклу) (?).
- Перемога: після завершення програми світ збігається з ціллю. Поразка: помилка виконання або невідповідність цілі. Рахунку нема; Reeborg веде лічильник виконаних кроків.

## Керування і ввід
- Ввід — **текст програми**: Python (Reeborg, Stanford), JavaScript/CoffeeScript (Reeborg), оригінальна Pascal-подібна мова Pattis-а (`BEGINNING-OF-PROGRAM … ITERATE 3 TIMES … END-OF-EXECUTION`), Java (Karel J. Robot / Stanford), або блоки Blockly (Reeborg).
- Кнопки виконання Reeborg: Run, Step (одна інструкція і пауза), Reverse step (крок назад по запису), Pause, Stop, Reload (повернути світ у початковий стан); `pause()` у коді — програмна точка зупину; `think(ms)` — затримка між кроками (швидкість).
- Окремий REPL-режим (Reeborg) — команди по одній, тобто «пряме керування» через консоль.
- Редактор світу — мишею: обрати інструмент (стіна, обʼєкт, плитка, ціль) і клікати по клітинах/ребрах.

## Вікна, меню, HUD
- `game-screen` = три панелі: світ (сітка з координатами, робот, стіни, обʼєкти з числами, цілі напівпрозоро) + `code-editor` (підсвітка синтаксису, номер поточного рядка, undo/redo, розмір шрифту, панель символів `: ; # " ' = < > ( ) [ ]`) + вкладки Library (власні функції, `from library import …`), Pre/Post code, Description (умова задачі).
- HUD: `step-counter` «0/0» (крок / усього), `instruction-highlight` (рядок, що виконується), `step-button`, `pause-button`, `restart-button` (Reload), `speed-slider`-еквівалент через `think()`.
- `level-select` — випадний список світів (Home 1–3, Around 1–4, Center 1–3, Hurdles 1–4, Harvest 1–4, Newspaper 0–2, Storm 1–3, Tokens, Maze… (?)) + завантаження світу з URL.
- `editor-window` — палітра: орієнтація робота (N/E/S/W/випадкова), обʼєкти, плитки, заливка, тверді обʼєкти (паркан, міст), декор, фон-картинка; меню Set dimensions · Robot · World · Goal (robot/wall/objects).
- `help-window` — вбудована документація й туторіал (окремий сайт docs).
- Діалоги результату (`end-screen`-модал): «завдання виконано» / перелік невиконаних цілей / текст помилки з номером рядка.
- `settings-window`: мова програмування (Python, JS, CoffeeScript, C++ (?), Blockly), мова інтерфейсу (EN, FR, DE, PL, PT, ZH, KO, LT + двомовні пари).
- Переходи: вибір світу → `game-screen`; Run → анімація → модал результату → Reload; меню World editor → `editor-window` → Save world (.json) → назад.

## Фічі поза полем
- `goal-check` — автоматична перевірка кінцевого стану; задача формулюється ціллю, а не «скриптом рухів».
- `random-variants` — один світ має кілька початкових конфігурацій (висота перешкод, кількість обʼєктів), обирається випадково при Reload (?): змушує писати умови й цикли.
- `step-mode`, `rewind` (reverse step — запис кадрів, а не справжній undo стану), `speed-control`.
- `level-editor` + `export-import`: світ — JSON (`World()` у коді завантажує світ за назвою/URL), розвʼязок — .py; Save/Open solution.
- `rules-page`/`tutorial` — повний підручник Python з Reeborg; `localization` інтерфейсу.
- Нема очок, зірок, прогресії; світи — банк задач без замків.

## Варіації й родичі
- Pattis 1981 (Pascal-подібна мова) → Karel++ (1996, ООП, C++/Java-стиль) → Karel J. Robot → Stanford Karel (Java, потім Python; SuperKarel з `turn_right`, `random`, `paint_corner`) → Karel the Dog (CodeHS, JS, тенісні мʼячі) → Guido van Robot (Python-синтаксис) → Reeborg's World.
- Robot Karol (німецька гілка): клітини з висотою, робот кладе цеглини стопками й лізе на них — вісь «поле 2D vs з висотою». Robot Emil — 3D.
- Осі варіацій: **мова** (власний мінімум / Python / блоки / іконки → Lightbot); **набір сенсорів** (лише front / три сторони / + обʼєкт під собою / + координати); **що вважається помилкою** (стіна, порожня клітина, порожня сумка, вода); **ціль** (позиція / розклад обʼєктів / побудовані стіни); **випадковість світу** (фіксований / кілька варіантів).

## Цікавинки для курсу
- Інтерпретатор міні-мови команд робота з `if/while/def` поверх клітинного поля — 🥇 (парсер/AST або вбудований Python із пісочницею).
- Сенсори як чисті функції від стану світу + «error shutoff» при недопустимій дії — 🥉.
- Перевірка цілі як порівняння двох станів світу (позиція, обʼєкти, стіни) — 📎.
- Стіни на ребрах клітин, а не в клітинах — 🥉 (інша модель суміжності, ніж у Sokoban).
- Покрокове виконання з підсвіткою рядка і reverse step через запис кадрів — 🥈.
- Світ з кількома випадковими варіантами, на яких має пройти одна програма — 📎.
- Редактор світу з ціллю (не лише початковий стан, а й кінцевий) і збереженням у JSON — 🥈.

## Мапа на каталог
- Є: `impassable-cells` (стіни) · `inventory-items` (сумка біперів) · `item-pickup` (`pick_beeper`) · `reach-exit` (дім) · `collect-all` (зібрати всі біпери — частина задач) · `level-select` (меню світів) · `in-game-editor` + `editor-palette` + `editor-erase` + `editor-playtest` · `level-exchange` (JSON-світ) · `state-as-data` · `replay` (reverse step) · `game-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+command-program` «Програма команд для аватара» · entities/move · 🥉 · слоти {commands: list, mode: run|step} — рух не з клавіш, а з послідовності.
  - `+sensor-predicates` «Сенсори робота» · entities/state · 📎 · слоти {sensors: front|left|right|here|bag|facing}.
  - `+user-procedures` «Власні процедури/функції в мові робота» · game-logic · 🥈 — визначення й виклик, рекурсія.
  - `+runtime-error-stop` «Помилка виконання зупиняє програму» · game-logic/lose · 📎 — врізався / нема що брати.
  - `+goal-state-check` «Кінцевий стан проти цілі» · game-logic/win · 📎.
  - `+step-execution` «Run / Step / Pause / Reload з підсвіткою рядка» · interface/input · 🥉.
  - `+random-world-variants` «Кілька стартових варіантів одного рівня» · levels/generation · 📎.
  - `+code-editor-window` «Вікно редактора програми» · interface/menus (#window) · 🥉.

## Пропозиції до словників
- `+trigger:exec(cmd)` — виконується інструкція програми (базовий тригер для всієї сімʼї program-robots); `+trigger:program_end` — програма дійшла до кінця/`done()`.
- `+effect:crash` — аварійна зупинка програми з повідомленням (error shutoff); відрізняється від `lose` — гра не закінчується, лише спроба.
- `+window:code-editor` — редактор коду як частина ігрового екрана або окреме вікно.
- `+ui:instruction-highlight` — підсвітка поточної інструкції; `+ui:step-counter` — лічильник виконаних кроків «k/N».
- `+feature:goal-check` — автоматична перевірка кінцевого стану; `+feature:random-variants` — кілька варіантів стартового світу.
- `+axis:control` — тут чисте `programmed`.

## Джерела
- ⭐ [Reeborg's World](https://reeborg.ca/reeborg.html) — грати одразу: редактор, світи, Run/Step/Reverse, редактор світів.
- [Wikipedia: Karel (programming language)](https://en.wikipedia.org/wiki/Karel_(programming_language)) — Pattis 1981, примітиви, сенсори, Python-варіант, нащадки (Karel++, Robot Karol, Guido van Robot, Karel the Dog).
- [Reeborg: довідник](https://reeborg.ca/docs/en/reference/index.html) — move, turn_left, take, put, front_is_clear, right_is_clear, at_goal, object_here, carries_object, pause, done, think, build_wall, World().
- [Reeborg: Basic tutorial](https://reeborg.ca/docs/en/basics/index.html) — порядок задач (Home, Newspaper, Hurdles, Harvest, Storm, Center), `repeat`.
- [Stanford Karel (Python) reference](https://compedu.stanford.edu/karel-reader/docs/python/en/reference.html) — команди, умови з запереченнями, paint_corner.
- [Karel the Robot Learns Java (PDF)](https://cs.stanford.edu/people/eroberts/karel-the-robot-learns-java.pdf) — класичний підручник CS106A (зміст не вдалося прочитати автоматично).
- YouTube: пошук «reeborg's world python tutorial».

## Непевне
- (?) Точні тексти помилок («Ouch! I hit a wall!» у Reeborg) і чи є ліміт кроків від нескінченного циклу — з памʼяті.
- (?) Сенсори `wall_in_front`/`wall_on_right` і поведінка води/багна в Reeborg — у довіднику Reeborg бачив лише front_is_clear/right_is_clear; решта з памʼяті.
- (?) Які саме світи мають випадкові варіанти і чи вибираються вони при Reload — з памʼяті.
- (?) Підтримка C++ як мови Reeborg — бачив пункт у списку мов на сторінці, але не перевіряв, чи робочий.
- (?) Оригінальні сенсори Pattis-а (`next-to-a-beeper`, `any-beepers-in-beeper-bag`) і обовʼязковий `turnoff` — з памʼяті; Wikipedia підтверджує лише їх існування загалом.
