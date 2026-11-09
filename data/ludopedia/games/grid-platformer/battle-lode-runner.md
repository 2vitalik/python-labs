---
title: Battle Lode Runner
slug: battle-lode-runner
aka: [バトルロードランナー]
family: grid-platformer
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: partial
  random: runtime
  goal: survive
year: 1993
platforms: [PC Engine, Wii Virtual Console (2007), Wii U Virtual Console (2016)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Battle_Lode_Runner", best: true, note: "Hudson, PC Engine 1993: до 5 гравців, режими Survival / Escape / Tag match, копання ліворуч-праворуч"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ロードランナー", note: "розділ バトルロードランナー: Puzzle Mode, мультитап, виштовхування з драбини, швидке падіння, редактор з 3 розмірами"}
  - {kind: other, url: "https://shacknews.com/article/46685/battle-lode-runner-virtual-console", note: "огляд VC: як вибувають у battle, носії схованого золота в Escape, предмети speed і заразна отрута, боти"}
  - {kind: official, url: "https://nintendo.com/en-gb/Games/TurboGrafx/Battle-Lode-Runner--276324.html", note: "сторінка VC: режими PUZZLE / BATTLE / EDIT, 1–5 гравців"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Battle+Lode+Runner+PC+Engine+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [dig-hole, hole-refill, ladder-climb, gravity-fall, collect-all, reach-exit, touch-death, environment-death, respawn, item-pickup, temporary-modes, ai-opponent, realtime-ai, mode-select, match-setup, level-password, save-game, sequential-levels, in-game-editor, editor-window, +last-standing, +team-versus, +contagious-status, +enemy-carries-item, +ladder-top-push, +bot-fill-slots, +local-versus]
proposes: ["+feature:bot-fill-slots", "+feature:editor-size-presets", "+card:last-standing", "+card:contagious-status", "+card:ladder-top-push"]
author: opus
date: 2026-11-09
---

# Battle Lode Runner — Lode Runner для п'ятьох на одному екрані: єдина зброя — яма, в яку має впасти суперник

## Суть
Hudson переносить правила [lode-runner](lode-runner.md) (біг, драбини, перекладини, копання цегли ліворуч-праворуч униз, ями заростають, вартові, золото, вихід угору) на PC Engine і додає **battle**: до п'яти бігунів на одній арені через мультитап, як у Bomberman. Суперника не можна вдарити — його треба загнати в яму, яку ти викопав, або під вартового. Поряд — звичайний одиночний Puzzle Mode з епохами, паролями й сейвом, і редактор рівнів.

## Поле і час
- Як у [lode-runner](lode-runner.md): один екран-сітка, клітинна гравітація, real-time.
- Battle-арена видна всім повністю; усі бігуни діють одночасно (`hotseat` тут — спільний екран, не почергово).
- Відмінність від серії: падіння «значно швидше», ніж в інших частинах (JA-вікі).
- Puzzle Mode: кожні 10 стадій — нова епоха (фон і вигляд ворогів).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Цегла, бетон, драбина, перекладина, золото, вартовий | — | — | як у [lode-runner](lode-runner.md) |
| Бігун (Runner 93) | player | 1–5 на арені | біг, лазіння, висіння, копання ліворуч/праворуч униз; ходить по головах ворогів |
| Бот-бігун | enemy | займає порожній слот | CPU-суперник у battle; «хитріший» за вартових Puzzle Mode (огляд) |
| Вартовий | enemy | у Puzzle Mode інколи — Black Bomberman | дотик — смерть/вибування; застряглий і засипаний — респавн в іншому місці |
| Вартовий-носій (Escape) | enemy | несе схований злиток | злиток випадає, коли його спіймати в яму |
| Схований злиток (Escape) | pickup | кілька на арену | зібрати — відкрити драбину-вихід |
| Speed-up | pickup | — | бігун швидшає |
| Отрута | pickup | заразна | інвертує напрямки керування; передається іншим (?) |
| Яма | terrain | таймер заростання | хто в ній, коли заросла, — гине / вибуває |

## Правила (КОЛИ → ЯКЩО → ТО)
- Правила руху, копання, заростання ям і поведінки вартових — як у [lode-runner](lode-runner.md); нижче лише відмінності.
- КОЛИ `input(dig_left|dig_right)` → ЯКЩО `cell(below_side, brick)` → ТО `set_cell(below_side, hole)`; під себе копати не можна.
- КОЛИ `enter(runner_b, hole)` → ТО `set_state(runner_b, trapped)` — у battle це «майже миттєва смерть» (огляд): вибратися до заростання не встигнути.
- КОЛИ `timer(refill)` → ЯКЩО `occupied(hole, runner)` → ТО `custom: «бігун вибуває з раунду»`; ЯКЩО `occupied(hole, guard)` → ТО `respawn(guard, elsewhere)`.
- КОЛИ `contact(runner, guard)` → ТО `custom: «бігун вибуває»` (battle) або `lives(-1)`, `restart` (Puzzle Mode).
- Survival: КОЛИ `counter(runners_alive, ==, 1)` → ТО `win` для останнього.
- Escape: КОЛИ `enter(carrier, hole)` → ТО `custom: «схований злиток випадає на поле»`.
- Escape: КОЛИ `picked(runner, hidden_gold)` → ЯКЩО `custom: «зібрано все сховане золото»` → ТО `reveal(exit_ladder)`.
- Escape: КОЛИ `reach(runner, top_edge)` → ЯКЩО `custom: «драбину відкрито»` → ТО `win` (перший, хто втік).
- Tag match: команди 2×2 за правилами Survival; КОЛИ `custom: «усі бігуни команди вибули»` → ТО `win` для іншої команди.
- КОЛИ `custom: «під час матчу»` → ТО `spawn(item)` — предмети з'являються на арені; за сторінкою Nintendo в Survival їх «забирають у ворогів» (?).
- КОЛИ `picked(runner, speed_up)` → ТО `speed(runner, +1)`.
- КОЛИ `picked(runner, poison)` → ТО `set_state(runner, poisoned)`, `invert_controls(n)`.
- КОЛИ `contact(runner_poisoned, runner_b)` → ТО `set_state(runner_b, poisoned)` — «заразна» отрута; механізм передачі дотиком (?).
- КОЛИ `custom: «бігун стоїть на верхівці драбини, знизу лізе вартовий»` → ТО `custom: «вартовий виштовхує бігуна вгору»` — не смерть; частина стадій розв'язується лише так (JA-вікі).
- Puzzle Mode: КОЛИ `reach(runner, top_edge)` → ЯКЩО `counter(gold_left, ==, 0)` → ТО `next_level`; продовжень без ліку.
- Перемога: Survival — останній живий; Escape — перший, хто вийшов зі схованим золотом; Tag — остання команда · Поразка: яма заросла над тобою або дотик вартового · Рахунок у battle — (?).

## Керування і ввід
- PC Engine: хрестовина — рух, дві кнопки — копати ліворуч / праворуч (?); до 5 геймпадів через мультитап.
- Wii VC: Wii Remote, Classic Controller, контролер GameCube.
- Порожні слоти battle займають CPU-боти.

## Вікна, меню, HUD
- `main-menu`: PUZZLE → `game-screen` (кампанія) · BATTLE → `mode-select` · EDIT → `editor-window`.
- `mode-select` (battle): SURVIVAL · ESCAPE · TAG MATCH; `match-setup` — хто людина, хто бот, команди для Tag (?).
- `game-screen`: арена на весь екран, усі бігуни видимі.
- `level-password` — повернутися до пройдених стадій Puzzle Mode; окремо — збереження прогресу.
- `editor-window`: вибір одного з трьох розмірів стадії → сітка з палітрою; збереження в PC Engine Backup Unit.
- `end-screen` з переможцем раунду (?).

## Фічі поза полем
- `mode-versus` до 5 гравців, `mode-coop` немає (Tag — 2 на 2), `ai-opponent-levels` — (?), боти в порожніх слотах.
- `levels-sequential` Puzzle Mode з епохами; `continue` без ліку; паролі + `save-slots` (Backup Unit) (?).
- `level-editor` з трьома розмірами поля: що більша стадія, то менше їх уміщається в пам'ять.
- Перевидання: Wii VC 2007 (перша японська гра на VC за межами Японії), Wii U VC 2016.

## Варіації й родичі
- База: [lode-runner](lode-runner.md); сиквели: [lode-runner-sequels](lode-runner-sequels.md), [lode-runner-the-legend-returns](lode-runner-the-legend-returns.md), [lode-runner-3d-sequels](lode-runner-3d-sequels.md).
- Формула battle — з Bomberman тієї ж Hudson: мультитап на 5, останній живий, предмети з тимчасовими ефектами (див. `maze-arcade/bomberman-battle-mode`; череп-прокляття Bomberman теж передається дотиком).
- Lode Runner Twin (T&E Soft, SFC 1994) — кооп і versus на двох; Lode Runner Legacy — локальний кооп.
- Осі варіацій: **чим шкодиш супернику** (лише яма / яма + вороги / предмети); **умова перемоги** (останній живий / перший вийшов / остання команда); **хто носить мету** (поле / вороги-носії).

## Цікавинки для курсу
- Battle поверх Lode Runner: яма як єдина зброя, заростання вбиває того, хто всередині, — 🥉 (той самий двіжок, n бігунів).
- Escape: вороги-носії скидають злиток у ямі, потім драбина й гонка до верху — 📎.
- Заразна отрута з інверсією керування — 📎.
- Боти, що копають ями під суперниками на графі руху з гравітацією — 🥇.
- Виштовхування з верхівки драбини як легальний прийом — 🌱.
- Редактор з трьома пресетами розміру й обмеженою пам'яттю на стадії — 📎.

## Мапа на каталог
- Є: `dig-hole` · `hole-refill` · `ladder-climb` · `gravity-fall` · `collect-all` · `reach-exit` · `touch-death` · `environment-death` · `respawn` · `item-pickup` · `temporary-modes` (speed, отрута) · `ai-opponent` + `realtime-ai` (боти) · `mode-select` · `match-setup` · `level-password` · `save-game` · `sequential-levels` · `in-game-editor` · `editor-window`.
- **Нема** → пропозиції карток:
  - `+last-standing` «Останній живий перемагає» · game-logic/win · 🌱.
  - `+team-versus` «Команди 2×2 за правилами free-for-all» · game-logic/opponent · 📎.
  - `+contagious-status` «Стан передається дотиком» · entities/state · 📎.
  - `+enemy-carries-item` — як у lode-runner (тут — схований злиток Escape).
  - `+ladder-top-push` «Ворог знизу виштовхує з драбини» · entities/move · 🌱.
  - `+bot-fill-slots` «Боти займають порожні слоти» · game-logic/opponent · 🥉.
  - `+local-versus` «До 5 гравців одночасно на одному екрані (мультитап)» · game-logic/opponent · 🥉 — `hot-seat` у каталозі почерговий.

## Пропозиції до словників
- `+feature:bot-fill-slots` — CPU-суперники доповнюють неповний склад гравців.
- `+feature:editor-size-presets` — редактор з вибором розміру поля, від якого залежить місткість збереження.
- `+card:last-standing`, `+card:contagious-status`, `+card:ladder-top-push` — див. вище.

## Джерела
- ⭐ [Wikipedia: Battle Lode Runner](https://en.wikipedia.org/wiki/Battle_Lode_Runner) — Hudson, 10.02.1993, до 5 гравців, Survival / Escape / Tag match, копання ліворуч-праворуч, ходіння по ворогах, VC 2007.
- [Wikipedia JA: ロードランナー](https://ja.wikipedia.org/wiki/ロードランナー) — розділ バトルロードランナー: Puzzle Mode і Runner 93, епохи по 10 стадій, Black Bomberman серед ворогів, виштовхування з драбини, швидке падіння, редактор з 3 розмірами і Backup Unit, Wii U VC.
- [Shacknews: огляд VC](https://shacknews.com/article/46685/battle-lode-runner-virtual-console) — вибування в ямі чи від ворогів, Escape з носіями золота, Tag 2 на 2, боти, предмети speed і заразна отрута з інверсією, паролі й сейв, безліч продовжень.
- [Nintendo: сторінка VC](https://nintendo.com/en-gb/Games/TurboGrafx/Battle-Lode-Runner--276324.html) — PUZZLE / BATTLE / EDIT, 1–5 гравців, у Survival предмети забирають у ворогів.
- YouTube: пошук «Battle Lode Runner PC Engine gameplay».

## Непевне
- (?) Кількість стадій Puzzle Mode: EN-вікі — «50 стадій у 11 епохах», огляд Shacknews — «100 рівнів», JA-вікі — нова епоха кожні 10 стадій; числа не зводяться.
- (?) Повний список предметів battle — названо лише speed і отруту; як саме предмети з'являються (на полі чи з ворогів) — джерела розходяться.
- (?) Як передається отрута (дотиком — за аналогією з черепом Bomberman) і скільки триває.
- (?) Призначення кнопок PC Engine, рахунок і кількість раундів у battle, екран результатів — не перевірено.
- (?) Чи можна стояти на голові суперника-бігуна, як на вартовому.
- Черга називає гру «сиквелом»; точніше — окрема гра серії з battle-режимом, не покрита `lode-runner-sequels`.
