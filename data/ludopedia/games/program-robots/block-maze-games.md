---
title: Blockly Games Maze і Code.org Classic Maze
slug: block-maze-games
aka: [Blockly Maze, Blockly Games Maze, Classic Maze, Hour of Code Maze, Angry Birds Maze, Code.org Maze]
family: program-robots
also: []
klass: avatar
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2012
platforms: [web]
links:
  - {kind: play, url: "https://blockly.games/maze", best: true, note: "Blockly Games: Maze, 10 рівнів, грається в браузері без реєстрації"}
  - {kind: play, url: "https://studio.code.org/s/hourofcode", note: "Code.org Classic Maze: 20 пазлів Hour of Code"}
  - {kind: other, url: "https://raw.githubusercontent.com/google/blockly-games/master/appengine/maze/src/main.js", note: "код Blockly Maze: ліміти блоків, типи клітин, скіни, ліміт 10 000 тіків, підказки рівнів"}
  - {kind: other, url: "https://raw.githubusercontent.com/code-dot-org/code-dot-org/staging/apps/src/maze/skins.js", note: "скіни Code.org maze: birds, pvz, scrat, bee, farmer, collector, harvester…"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Blockly", note: "Blockly — візуальна мова блоків Google"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Code.org", note: "Hour of Code 2013, ~20 млн учасників, Blockly"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=code.org+classic+maze+hour+of+code", note: "пошук; проходження"}
stage: v1
coverage: 80
mechanics: [command-program, sensor-predicates, step-execution, code-editor-window, drag-drop-piece, impassable-cells, reach-exit, sequential-levels, level-unlock, game-screen, end-screen, help-window, tutorial-window, avatar-picker, language-picker, +block-programming, +block-budget, +repeat-until-goal, +relative-turn-commands, +step-limit-timeout, +crash-animation, +generated-code-view, +ideal-block-count]
proposes: ["+cond:path(dir)", "+cond:not_done", "+trigger:step_limit(n)", "+effect:crash", "+ui:block-workspace", "+ui:block-toolbox", "+ui:blocks-left", "+window:code-view", "+feature:block-limit", "+feature:skin-select", "+feature:certificate", "+axis:control"]
author: opus
date: 2026-11-09
---

# Blockly Maze / Code.org Classic Maze — склади з блоків програму, щоб персонаж дійшов лабіринтом до фінішу

## Суть
Персонаж (Pegman, Angry Bird, зомбі, білка Скрат) стоїть у лабіринті з квадратних клітин; треба довести його до фінішу. Гравець складає програму з **блоків Blockly** — «вперед», «ліворуч/праворуч», «повторювати, доки не фініш», «якщо шлях попереду/ліворуч/праворуч», «якщо-інакше» — і запускає її. Рівні вводять одну концепцію за раз, а **бюджет блоків** не дає розвʼязати рівень довгим ланцюжком команд — доводиться брати цикл і умову; фінал — алгоритм «правої руки» для будь-якого лабіринту. Два продукти обʼєднано в один файл: Code.org Classic Maze (Hour of Code 2013) — це той самий Blockly-лабіринт з ліцензованими персонажами й 20 пазлами; механічна різниця лише в деталях (див. «Варіації»).

## Поле і час
- Квадратна сітка невеликого розміру; клітини: стіна, прохід, старт, фініш. За межами мапи — як стіна.
- Видно все поле; камера фіксована; фон і спрайти залежать від скіна.
- Час `programmed`: блоки виконуються послідовно з анімацією; підсвічується поточний блок. Перевірка «шлях вільний» теж анімується (персонаж «дивиться»).
- Ліміт виконання: 10 000 тіків (≈8 хв) — далі TIMEOUT (Blockly Maze).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж (Pegman / Astro / Panda; Angry Bird / зомбі / Скрат у Code.org) | player | клітина, напрямок N/E/S/W | виконує блоки; удар об стіну = аварія |
| Стіна | static | — | непрохідна; також «за краєм мапи» |
| Прохід | terrain | — | можна стати |
| Старт | terrain | — | початкова клітина й напрямок |
| Фініш (маркер / свиня / соняшник / жолудь) | static | — | досягнення = перемога |
| Перешкода (TNT / ворожа рослина в Code.org) | hazard | — | контакт = невдача (?) |
| Блок програми | — (програма) | тип, вкладені блоки | частина дерева програми в робочій області |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(move_forward)` → ЯКЩО `free(front)` → ТО `move(hero, facing)`; інакше `crash` — анімація удару, результат FAILURE/ERROR.
- КОЛИ `exec(move_backward)` → ЯКЩО `free(back)` → ТО `move(hero, back)` (є в API, блок не в усіх рівнях (?)).
- КОЛИ `exec(turn_left|turn_right)` → ТО `face(hero, left|right)` — повороти відносні.
- КОЛИ `exec(repeat_until)` → ЯКЩО `not reach(hero, finish)` → ТО `custom: «виконати тіло циклу й перевірити знову»`.
- КОЛИ `exec(repeat_n)` → ТО `custom: «виконати тіло N разів»` (Code.org).
- КОЛИ `exec(if path_ahead|left|right)` → ЯКЩО `free(cell(dir))` → ТО `custom: «виконати вкладені блоки»`.
- КОЛИ `exec(if_else)` → ЯКЩО `free(cell(dir))` → ТО `custom: «гілка do»`; інакше `custom: «гілка else»`.
- КОЛИ `reach(hero, finish)` → ТО `win`, `window(end-screen)`, `next_level`.
- КОЛИ `program_end` → ЯКЩО `not reach(hero, finish)` → ТО `custom: «FAILURE: не дійшов»`, спроба невдала.
- КОЛИ `counter(ticks, >=, 10000)` → ТО `custom: «TIMEOUT: схоже на нескінченний цикл»` (Blockly Maze).
- КОЛИ `custom: «кількість блоків у робочій області ≥ ліміту»` → ТО `block` — новий блок не додається, підказка «capacity» (Blockly Maze: рівні 3–10, ліміти 2, 5, 5, 5, 5, 10, 7, 10).
- КОЛИ `win` → ЯКЩО `custom: «блоків більше за ідеальну кількість»` → ТО `message(«можна коротше»)` — м'яке обмеження (Code.org) (?).
- КОЛИ `contact(hero, obstacle)` → ТО `lose` спроби, `restart` (Code.org, TNT/рослина) (?).
- Перемога: дійти до фінішу · Поразка: удар об стіну, кінець програми не на фініші, таймаут — лише невдала спроба · Рахунок: нема; у Code.org — оцінка «оптимальна кількість блоків» (?).

## Керування і ввід
- Drag & drop блоків з панелі (toolbox) у робочу область; блоки клацаються один під одним і вкладаються в «пащі» циклів та умов; випадне меню на блоці — вибір напрямку (ahead/left/right).
- Видалити — витягти блок назад у toolbox або в кошик.
- Кнопки: Run Program → під час/після виконання Reset; Code.org — ще Step і показ коду (?).
- Рівень 1 Blockly Maze: стартовий блок закріплений (неможливо зрушити), далі — вільний.

## Вікна, меню, HUD
- `game-screen`: ліворуч поле лабіринту, праворуч `block-toolbox` і `block-workspace`; над ними — текст завдання (`objective-text`), `blocks-left` («лишилось N блоків»), номер рівня (кружечки 1–10 у Blockly Maze), кнопки Run/Reset; `instruction-highlight` на поточному блоці.
- `help-window` / `tutorial-window`: контекстні бульбашки Blockly Maze — «склади блоки стосом», «один верхній блок», «натисни Run», «Reset», «ліміт блоків», «спробуй repeat», «спробуй if», «відкрий меню напрямку», «спробуй if-else»; на рівні 10 — модальне пояснення стратегії «вздовж стіни».
- `skin-select` — меню вибору персонажа (Pegman, Astro, Panda), підказка зʼявляється на рівні 5.
- `end-screen` — «Вітаю!», показ згенерованого JavaScript (`code-view`) (?), перехід на наступний рівень; після рівня 10 — наступна гра Blockly Games.
- Code.org: `level-select` — кружечки 1–20 угорі, відео-уроки між блоками рівнів, сертифікат у кінці (?).
- `settings-window` — вибір мови (Blockly Games — багатомовні).
- Переходи: рівень N → (фініш) end-screen → рівень N+1; невдача → Reset → правка програми.

## Фічі поза полем
- `levels-sequential` + `level-unlock`; прогрес зберігається в браузері (?).
- `block-limit` — жорсткий бюджет блоків (Blockly) vs м'який «ідеал» (Code.org).
- `onboarding-hints` — контекстні підказки за станом програми (не використав цикл → підказка про цикл).
- `skin-select` (Blockly: різні анімації аварії — зупинка, обертання, падіння).
- Code.org: Hour of Code — відео між етапами, сертифікат, класи вчителя, показ коду JavaScript (?).
- `localization` — десятки мов.

## Варіації й родичі
- **Різниця близнюків**: Blockly Maze — 10 рівнів, жорсткий ліміт блоків, «repeat until» без лічильника, скіни-рескіни; Classic Maze — 20 пазлів, ліцензовані персонажі (Angry Birds, Plants vs. Zombies, Ice Age), блок «repeat N times», м'який ліміт через «ідеальну» кількість, відео-уроки (?). Модель світу й набір команд — однакові.
- Інші скіни лабіринту Code.org (у курсах A–F): **bee** (квітки з нектаром, вулики з медом, хмара ховає клітину), **farmer** (ями й купи землі: копати/засипати), **collector** (зібрати кристали), **harvester/planter** (зібрати/посадити культури), **neighborhood** (фарбувати) — це вже інші механіки поверх того ж лабіринту.
- Наступники: Blockly Games Bird, Turtle, Movie, Music, Pond (бої ботів, від блоків до JavaScript); Scratch.
- Родичі в корпусі: [Karel](karel.md) (текстова мова, frontIsClear), [Kara](kara.md), [Lightbot](lightbot.md), [RoboZZle](robozzle.md), [Cargo-Bot](cargo-bot.md).
- **Осі варіацій**: синтаксис (блоки / іконки-слоти / текст) · обмеження (жорсткий бюджет / м'який ідеал / нема) · цикл (repeat N / repeat until / рекурсія) · сенсор (шлях у напрямку / колір / предмет) · повороти (відносні / абсолютні N-E-S-W).

## Цікавинки для курсу
- Лабіринт + інтерпретатор дерева блоків (послідовність, цикл, if, if-else) — 🥉.
- Бюджет блоків з лічильником «лишилось» — 🌱.
- Ліміт кроків як захист від нескінченного циклу (TIMEOUT) — 🌱.
- Контекстні підказки за аналізом програми («цикл не використано») — 📎.
- Згенерований текстовий код із блоків (blocks → JavaScript) — 🥈.
- Генерація лабіринтів, де алгоритм «правої руки» працює (без островів) — 🥇.
- Скіни з різними анімаціями аварії — 📎.

## Мапа на каталог
- Є в каталозі: `command-program` ↔ програма з блоків; `sensor-predicates` ↔ «шлях попереду/ліворуч/праворуч»; `step-execution` ↔ підсвітка блоку; `code-editor-window` ↔ toolbox + робоча область; `drag-drop-piece` ↔ перетягування блоків; `impassable-cells` ↔ стіни; `reach-exit` ↔ фініш; `sequential-levels`/`level-unlock`; `game-screen`, `end-screen`, `help-window`, `tutorial-window`; `avatar-picker` ↔ вибір персонажа; `language-picker`.
- **Нема** → пропозиції карток:
  - `+block-programming` «Програма з блоків-пазлів (Blockly)» · game-logic/program · 🥈.
  - `+block-budget` «Ліміт блоків з лічильником» · game-logic/constraints · 🌱.
  - `+repeat-until-goal` «Цикл "повторювати, доки не фініш"» · game-logic/program · 🌱.
  - `+relative-turn-commands` «Відносні повороти ліво/право» · entities/move · 🌱.
  - `+step-limit-timeout` «Ліміт кроків виконання → таймаут» · game-logic/program · 🌱.
  - `+crash-animation` «Анімація аварії об стіну» · interface/graphics · 📎.
  - `+generated-code-view` «Показ коду, згенерованого з блоків» · interface/menus · 🥈.
  - `+ideal-block-count` «М'яке обмеження: ідеальна кількість блоків» · game-logic/score · 🌱.

## Пропозиції до словників
- `+cond:path(dir)` — у відносному напрямку вільна клітина (isPathForward/Left/Right/Backward); коротше за `free(cell(dir))`.
- `+cond:not_done` — ціль ще не досягнута (умова циклу `repeat until`).
- `+trigger:step_limit(n)` — виконання перевищило ліміт кроків.
- `+ui:block-workspace` · `+ui:block-toolbox` · `+ui:blocks-left`.
- `+window:code-view` — показ текстового коду програми.
- `+feature:block-limit` · `+feature:skin-select` · `+feature:certificate` (сертифікат проходження).
- `+axis:control` — `programmed`.

## Джерела
- ⭐ [Blockly Games: Maze](https://blockly.games/maze) — грати (сторінка — JS-застосунок, текст не читається скриптом).
- [main.js Blockly Maze](https://raw.githubusercontent.com/google/blockly-games/master/appengine/maze/src/main.js) — MAX_BLOCKS по рівнях, типи клітин, скіни й типи аварій, результати SUCCESS/FAILURE/TIMEOUT/ERROR, 10 000 тіків, isPath*, підказки рівнів.
- [skins.js Code.org](https://raw.githubusercontent.com/code-dot-org/code-dot-org/staging/apps/src/maze/skins.js) — скіни birds, pvz, scrat, bee, farmer, collector, harvester, planter, neighborhood.
- [Code.org: Classic Maze](https://studio.code.org/s/hourofcode) — назва «Classic Maze», пазли 1–20 (сторінка рівня «Puzzle 20»).
- [Wikipedia: Code.org](https://en.wikipedia.org/wiki/Code.org) — Hour of Code 9–15.12.2013, ~20 млн учасників, Blockly.
- [Wikipedia: Blockly](https://en.wikipedia.org/wiki/Blockly) — сама мова блоків (не відкривав).

## Непевне
- (?) Рік Blockly Maze: Blockly — 2012, Maze був одним з перших демо; бренд Blockly Games — пізніше (2014?).
- (?) Набір блоків і рівні Code.org Classic Maze (repeat N, repeat until, if, if-else; хто з персонажів на яких пазлах) — сторінки рівнів не завантажились, з памʼяті.
- (?) Перешкоди TNT/рослини в Classic Maze і що буде при контакті.
- (?) Показ згенерованого JavaScript: є в Code.org («Show code»); у Blockly Maze — у діалозі після рівня (?).
- (?) Розмір мап Blockly Maze (≈7×8) — карти в коді не рахував.
- (?) Відео-уроки, сертифікат, «ідеальна кількість блоків» Code.org — з памʼяті.
