---
title: Wumpus world («Світ Вампуса»)
slug: wumpus-world
aka: [Wumpus World, WumpusWorld, Світ Вампуса]
family: program-robots
also: [hidden-deduction]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: setup
  goal: score
year: 1995
platforms: [textbook, PC, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wumpus_world", best: true, note: "4×4, сенсори, очки, Genesereth і AIMA"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hunt_the_Wumpus", note: "оригінальна гра 1972–73; згадка AIMA з 1995"}
  - {kind: other, url: "https://github.com/holderlb/wumpus-world-simulator", note: "Wumpus World Simulator (C++/Python): -size N, -trials, -tries, -seed, файли світів, 1000 ходів"}
  - {kind: other, url: "https://eecs.wsu.edu/~holder/courses/AI/wumpus/", note: "Larry Holder, WSU: сторінка симулятора, Prolog-версії"}
  - {kind: other, url: "https://www.appliedaicourse.com/blog/wumpus-world-in-artificial-intelligence", note: "PEAS і приклад виведення безпечних клітин"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wumpus+world+agent+simulation", note: "пошук; лекції й симуляції агента"}
stage: v1
coverage: 75
mechanics: [touch-death, environment-death, projectile-shot, item-pickup, reach-exit, orientation-state, event-points, seed-share, level-from-txt, fog-of-war, game-screen, end-screen, +adjacent-hazard-sense, +ammo-limit, +percept-vector, +agent-program-interface, +knowledge-base-inference, +batch-trials, +exit-at-start]
proposes: ["+effect:sense(percepts)", "+trigger:step_done", "+feature:agent-api", "+feature:batch-trials", "+ui:percept-panel", "+ui:knowledge-overlay", "+card:knowledge-base-inference"]
author: opus
date: 2026-11-09
---

# Wumpus world — агент у темній печері 4×4 відчуває вітер і сморід і має логікою вивести, куди ступати, щоб винести золото

## Суть
Навчальне середовище штучного інтелекту (Michael Genesereth; підручник Russell & Norvig «Artificial Intelligence: A Modern Approach», з 1995), за мотивами [Hunt the Wumpus](../hidden-deduction/hunt-the-wumpus.md). Печера — сітка 4×4, де є Вампус, ями й золото; агент стартує в (1,1) і на кожному кроці отримує **вектор сприйняття** `[Stench, Breeze, Glitter, Bump, Scream]`. Тут «гравець» — **програма-агент**: функція `percept → action`, а розумна гра — це виведення з бази знань («у (1,2) вітер ⇒ яма в (1,3) або (2,2)»). Мета — схопити золото, повернутися в (1,1) і вилізти, втративши якнайменше очок.

## Поле і час
- Квадратна сітка 4×4 (у симуляторі WSU — `-size N`, N > 1, або фіксований світ з файла); стіни по периметру.
- Клітина (1,1) — вхід/вихід; Вампус і золото — у випадкових клітинах, крім стартової; кожна інша клітина — яма з імовірністю 0.2.
- Час `turn`: хід = одна дія агента; середовище детерміноване, статичне (Вампус не рухається), дискретне, частково спостережуване, з одним агентом.
- Агент бачить лише сприйняття своєї клітини; мапу будує сам.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Агент | player | позиція, напрямок, 1 стріла, має золото? | виконує дії, отримує сприйняття |
| Вампус | enemy | живий / мертвий | нерухомий; вхід у його клітину живим = смерть; сусідні клітини смердять |
| Яма | hazard | — | вхід = смерть; сусідні клітини віють вітром |
| Золото | pickup | — | у своїй клітині блищить; `Grab` бере |
| Стріла | projectile | 1 шт. | летить прямо у напрямку агента до Вампуса або стіни |
| Стіна (межа) | static | — | крок у неї → Bump, позиція не змінюється |
| Вхід (1,1) | zone | — | лише тут `Climb` виводить з печери |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(Forward)` → ЯКЩО `free(front)` → ТО `move(agent, forward)`, `score(-1)`.
- КОЛИ `input(Forward)` → ЯКЩО `not free(front)` (стіна) → ТО `block`, `custom: «наступне сприйняття містить Bump»`, `score(-1)`.
- КОЛИ `input(TurnLeft)` / `input(TurnRight)` → ТО `face(agent, ∓90°)`, `score(-1)`.
- КОЛИ `input(Grab)` → ЯКЩО `occupied(here, gold)` → ТО `pickup`, `score(-1)`.
- КОЛИ `input(Shoot)` → ЯКЩО `has(agent, arrow)` → ТО `take(agent, arrow)`, `score(-10)`, `custom: «стріла летить прямо до Вампуса або стіни»`.
- КОЛИ `contact(arrow, wumpus)` → ТО `set_state(wumpus, dead)`, `custom: «наступне сприйняття містить Scream»`.
- КОЛИ `input(Climb)` → ЯКЩО `custom: «агент у (1,1)»` and `has(agent, gold)` → ТО `score(+1000)`, `win`.
- КОЛИ `input(Climb)` → ЯКЩО `custom: «агент у (1,1)»` and `not has(agent, gold)` → ТО `game_over` (вийшов без золота).
- КОЛИ `enter(agent, pit)` → ТО `score(-1000)`, `lose`.
- КОЛИ `enter(agent, wumpus)` → ЯКЩО `state(wumpus, alive)` → ТО `score(-1000)`, `lose`.
- КОЛИ `custom: «агент завершив дію»` → ЯКЩО `adjacent_count(here, wumpus, >=, 1)` → ТО `custom: «сприйняття Stench»`.
- КОЛИ `custom: «агент завершив дію»` → ЯКЩО `adjacent_count(here, pit, >=, 1)` → ТО `custom: «сприйняття Breeze»`.
- КОЛИ `custom: «агент завершив дію»` → ЯКЩО `occupied(here, gold)` → ТО `custom: «сприйняття Glitter»`.
- КОЛИ `counter(moves, >=, 1000)` (симулятор WSU) → ТО `game_over`.
- Агент (логіка): КОЛИ `custom: «у клітині нема Breeze і Stench»` → ТО `mark(neighbors, OK)` — усі сусіди безпечні.
- Агент (логіка): КОЛИ `custom: «Breeze у (1,2), а (1,1) і (2,2) відомі як OK»` → ТО `custom: «яма в (1,3)»` — висновок резолюцією з бази знань.
- Агент (логіка): КОЛИ `custom: «безпечних невідвіданих клітин нема»` → ТО `custom: «ризикнути (імовірнісне виведення) або вилізти без золота»`.
- Перемога: вилізти з золотом · Поразка: яма або живий Вампус · Рахунок: +1000 за вихід із золотом, −1000 за смерть, −1 за дію, −10 за постріл.

## Керування і ввід
- Шість дій: Forward, TurnLeft, TurnRight, Grab, Shoot, Climb (у симуляторі WSU клавіші `f l r g s c`).
- Основний режим — **програма-агент**: інтерфейс `Initialize`, `Process(percept) → action`, `GameOver(score)` (C++ або Python, `pywumpsim`).
- Ручний режим — людина вводить дії з клавіатури (симулятор WSU).

## Вікна, меню, HUD
- `game-screen` (симулятор/візуалізатор): сітка з відкритими клітинами, `percept-panel` поточного сприйняття, `score`, `move-counter`; `knowledge-overlay` — позначки агента OK / P? / W? / ями й Вампус (як на рисунках AIMA) (?).
- Консольний вивід: стан світу ASCII-сіткою й рахунок після кожної спроби, серії і всієї симуляції.
- `end-screen` — підсумок спроби: очки, причина кінця.
- (цифрова версія) `match-setup` — розмір, seed, кількість trials/tries, файл світу; `replay-window` — покрокова історія.
- Переходи: setup → спроба → підсумок → наступна спроба/світ → підсумок симуляції.

## Фічі поза полем
- `seed-input` — `-seed N` повторює генерацію; `export-import` — світ з файла (`-world`).
- `batch-trials` — `-trials N` різних світів × `-tries N` спроб на кожному; середній рахунок як оцінка агента.
- `custom-difficulty` — розмір поля `-size N`.
- Мобільні версії симулятора (iOS, Android) і Prolog-версії (2.3 — зображення кімнат і підказки природною мовою для тестування зору й NLP агента).
- Турніри агентів у курсах AI (?).

## Варіації й родичі
- Оригінал — [Hunt the Wumpus](../hidden-deduction/hunt-the-wumpus.md) (1972–73): граф-додекаедр, кажани-телепорти, 5 «кривих» стріл, Вампус ворушиться від промаху; Wumpus world спрощує до сітки, нерухомого Вампуса й однієї прямої стріли.
- Варіанти підручника/курсів: дія Release (?), кілька Вампусів, рухомий Вампус, більші сітки, імовірнісний агент (байєсівські ями) (?).
- Родичі в корпусі: [Karel](karel.md) (сенсори робота), [Robot Odyssey](robot-odyssey.md) (сенсори → логічні схеми), [Bot arenas](bot-arenas.md) (агент проти середовища); Minesweeper — та сама дедукція за сусідами.
- **Осі варіацій**: хто ходить (людина / програма-агент) · поле (граф / сітка) · ворог (нерухомий / блукає) · стріла (пряма / крива, 1 / 5) · виведення (логіка / імовірність).

## Цікавинки для курсу
- Генерація печери: ями з p = 0.2, золото і Вампус поза стартом, seed — 🌱.
- Вектор сприйняття (5 булевих) і Bump/Scream як «події попереднього кроку» — 🌱.
- Стріла по прямій до першої перешкоди — 📎.
- Інтерфейс агента `Process(percept) → action` і запуск N світів × M спроб із середнім рахунком — 🥉.
- Логічний агент: база знань, позначки OK/P?/W?, виведення безпечних клітин — 🥇.
- Імовірнісний агент для ситуацій «безпечних ходів нема» — 👑.
- Візуалізація знань агента поверх поля — 📎.

## Мапа на каталог
- Є в каталозі: `touch-death` ↔ живий Вампус; `environment-death` ↔ яма; `projectile-shot` ↔ стріла; `item-pickup` ↔ золото; `reach-exit` ↔ вихід у (1,1); `orientation-state` ↔ напрямок агента; `event-points` ↔ таблиця +1000/−1000/−1/−10; `seed-share`; `level-from-txt` ↔ файл світу; `fog-of-war` ↔ невидимі клітини; `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+adjacent-hazard-sense` «Сенсор небезпеки в сусідній клітині» · entities/state · 🌱 (вже пропонувала Hunt the Wumpus).
  - `+ammo-limit` «Обмежений боєзапас» · entities/combat · 🌱 (так само).
  - `+percept-vector` «Сприйняття як вектор ознак на кроці» · game-logic/program · 🌱.
  - `+agent-program-interface` «Гравець — функція percept → action» · game-logic/program · 🥉.
  - `+knowledge-base-inference` «Агент виводить безпечні клітини логікою» · game-logic/program · 🥇.
  - `+batch-trials` «Оцінка програми на N згенерованих світах» · levels/solvability · 📎.
  - `+exit-at-start` «Вихід — у стартовій клітині, після здобичі» · game-logic/win · 🌱.

## Пропозиції до словників
- `+effect:sense(percepts)` — видати агенту сприйняття (Stench, Breeze, Glitter, Bump, Scream).
- `+trigger:step_done` — кінець дії агента (момент формування сприйняття).
- `+feature:agent-api` — гра надає API для програми-агента замість людини.
- `+feature:batch-trials` — серії світів і спроб з підсумковою статистикою.
- `+ui:percept-panel` — панель поточних сприйнять.
- `+ui:knowledge-overlay` — позначки знань агента на клітинах.
- `+card:knowledge-base-inference` — картка логічного агента (база знань + виведення).

## Джерела
- ⭐ [Wikipedia: Wumpus world](https://en.wikipedia.org/wiki/Wumpus_world) — 4×4, старт (1,1), сенсори, −1 за хід, +1000 за золото, −10 за постріл, Genesereth, AIMA.
- [Wikipedia: Hunt the Wumpus](https://en.wikipedia.org/wiki/Hunt_the_Wumpus) — оригінал і згадка, що AIMA використовує його версію з 1995.
- [Wumpus World Simulator (GitHub)](https://github.com/holderlb/wumpus-world-simulator) — дії `f l r g s c`, `-size`, `-world`, `-trials`, `-tries`, `-seed`, ліміт 1000 ходів, інтерфейс агента.
- [WSU: Wumpus World Simulator](https://eecs.wsu.edu/~holder/courses/AI/wumpus/) — історія, Prolog-версії, мобільні застосунки.
- [Applied AI Course](https://www.appliedaicourse.com/blog/wumpus-world-in-artificial-intelligence) — PEAS, властивості середовища, приклад виведення.
- Результати пошуку (курсові нотатки): −1000 за смерть, p(яма) = 0.2, одна стріла летить до Вампуса або стіни, Bump і Scream — на кроці після події.

## Непевне
- (?) Рік: Genesereth запропонував середовище раніше за AIMA (1995) — точну дату не знайдено; у шапці 1995.
- (?) Дія Release і чи Climb без золота дає кінець гри чи просто 0 очок — джерела різняться.
- (?) Частка нерозвʼязних без ризику світів (≈21% — з памʼяті про AIMA).
- (?) Вигляд візуалізатора й позначок знань — з памʼяті про рисунки підручника.
- (?) Турніри агентів у курсах.
