---
title: Orcs Must Die!
slug: orcs-must-die
aka: [OMD, OMD!, Орки мають померти]
family: tower-lanes
also: []
klass: avatar
axes:
  field: 3d
  time: realtime
  opponent: none
  info: full
  random: none
  goal: survive
year: 2011
platforms: [Xbox 360, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Orcs_Must_Die!", best: true, note: "rift points, 4–12 хвиль, перерва кожні 3 хвилі, лоадаут до 10, пастки на підлогу/стіну/стелю, рефанд, черепи 1–5, weavers"}
  - {kind: steam, url: "https://store.steampowered.com/app/102600/Orcs_Must_Die/", note: "24 фортеці, 19 пасток і союзників, 6 зброй/заклять, 11 типів ворогів, Nightmare, лідерборд"}
  - {kind: other, url: "https://www.gamepressure.com/orcsmustdie2/traps-p-1/zb3d3a", note: "гайд OMD2: пастки, барикади (вороги ламають повний блок), стельові пастки"}
  - {kind: steam, url: "https://store.steampowered.com/app/201790/Orcs_Must_Die_2/", note: "сиквел: кооп на двох"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=orcs+must+die+2011+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [tower-placement, tower-range, cursor-place, enemy-waves, spawn-points, enemy-reached-base, round-currency, shop-buyback, drop-on-death, item-pickup, hp-damage, projectile-shot, shoot-cooldown, melee-vs-ranged, speed-per-type, environment-death, impassable-cells, destructible-blocks, chase-bfs, player-death, respawn, shop-between-levels, in-round-upgrades, difficulty-levels, sequential-levels, level-unlock, leaderboard, save-progress, event-points, +trap-surfaces, +trap-rearm, +loadout-select, +rift-points-pool, +skull-rating, +knockback-push, +maze-by-barricade, +call-wave-early]
proposes: ["+role:trap", "+role:base", "+cond:surface", "+effect:sell", "+effect:knockback", "+effect:rearm", "+trigger:wave_break", "+ui:rift-points", "+ui:trap-bar", "+window:loadout-select", "+window:weaver-window", "+feature:loadout-lock", "+card:trap-surfaces", "+card:trap-rearm"]
author: opus
date: 2026-11-09
---

# Orcs Must Die! — маг-пасткар бігає фортецею і вкладає підлогу, стіни й стелю пастками, поки орки йдуть до розлому

## Суть
Action-TD від третьої особи: War Mage стоїть у лабіринті коридорів фортеці, орки хвилями йдуть від входів до **розлому (rift)**. Гравець купує й ставить пастки на клітинки **підлоги, стін і стелі** просто туди, куди дивиться, і водночас сам стріляє з арбалета й чаклує. Кожен орк, що дійшов до розлому, знімає очки розлому; нуль — поразка. Ставити пастки можна будь-коли, навіть посеред бою; продати — з поверненням ціни.

## Поле і час
- 3D-рівень (фортеця), але поверхні поділені на **сітку клітинок** — пастка займає клітинки однієї поверхні: підлога, стіна або стеля. Тип пастки визначає, на яку поверхню її можна поставити.
- Камера — від третьої особи за магом; приціл (центр екрана) = курсор розміщення.
- Real-time: рівень = 4–12 хвиль; наступна хвиля стартує за кілька секунд після очищення попередньої; кожні **3 хвилі — перерва**, яку гравець закінчує сам (крім Nightmare — без перерв).
- Вороги йдуть від точок входу до розлому(-ів); на рівні може бути кілька розломів.
- Висота й обриви: «скинути» орка в прірву чи лаву — окремий спосіб убити.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| War Mage | player | HP, мана | бігає, стріляє/бʼє зброєю, ставить і продає пастки; смерть або падіння → респавн біля розлому за rift points |
| Розлом (rift) | static (`+role:base`) | спільний пул rift points | орк, що увійшов, знімає 1 (великі — більше) |
| Точка входу | spawner | — | двері, з яких виходять хвилі |
| Орк | enemy | HP, швидкість | іде до розлому; атакує мага й барикади на шляху |
| Гнол / огр / великі | enemy | більше HP, ціна в rift points (?) | важчі; огр не відкидається легко (?) |
| Летючий hellbat | enemy | летить | ігнорує підлогові пастки (?) |
| Ворожий стрілець | enemy | дальня атака | бʼє мага й гвардійців (?) |
| Шипи (spike trap) | hazard (`+role:trap`) | підлога, cooldown | бʼє всіх, хто стоїть на клітинках, ховається і перезаряджається |
| Стіна стріл (arrow wall) | hazard | стіна, дальність | стріляє вздовж коридору перед собою |
| Обертові леза (wall blades) | hazard | стіна | ріже тих, хто йде повз стіну |
| Пружина (spring trap) | hazard | підлога | підкидає/відкидає орка — у прірву, лаву, під іншу пастку |
| Смола (tar trap) | hazard | підлога | сповільнює всіх на клітинках |
| Сірка (brimstone) | hazard | підлога | підпалює (шкода в часі) |
| Стельова пастка (crusher / pounder) | hazard | стеля | бʼє тих, хто під нею (?) |
| Барикада | object | підлога, HP | непрохідна: орки обходять; якщо обходу нема — ламають (з гайду OMD2) |
| Гвардієць (bowman / swordsman) | ally | HP, ціна | стоїть на місці, сам атакує ворогів |
| Монети | pickup | — | падають з деяких ворогів; плюс нагорода за вбивство і хвилю |
| Зілля HP / мани | pickup | — | випадають з орків |
| Лава / прірва | hazard | частина рівня | миттєва смерть для того, хто туди впав (і для мага — респавн) |
| Weaver | neutral | дерево апгрейдів | між рівнями/до старту: обраний один на спробу, дає тимчасові апгрейди |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `choose(loadout ≤ 10 пасток/зброї з spellbook)`; КОЛИ `custom: «поставлено першу пастку»` → ТО `custom: «лоадаут зафіксовано до кінця рівня»`.
- КОЛИ `input(place, trap, cell)` → ЯКЩО `custom: «cond surface(cell) == поверхня пастки»` and `free(cells)` and `counter(money, >=, cost)` → ТО `currency(-cost)`, `place(player, trap)`; інакше `block`.
- КОЛИ `input(sell, trap)` → ТО `disappear(trap)`, `currency(+cost)` — `custom: «sell: повний рефанд»` (?) лише в перерві чи завжди — див. «Непевне».
- КОЛИ `enter(enemy, trap_cells)` → ЯКЩО `state(trap, armed)` → ТО `damage(n)` усім на клітинках, `clear_state(trap, armed)`; КОЛИ `timer(cooldown)` → ТО `set_state(trap, armed)`.
- КОЛИ `enter(enemy, tar_cells)` → ТО `speed(enemy, ×k)` поки на клітинках.
- КОЛИ `enter(enemy, spring_cells)` → ТО `custom: «knockback: відкинути в напрямку пружини»`; ЯКЩО `custom: «у точці приземлення лава/прірва»` → ТО `disappear(enemy)`, нагорода.
- КОЛИ `in_range(arrow_wall, enemy, n)` and `line_of_sight(arrow_wall, enemy)` → ЯКЩО `state(arrow_wall, armed)` → ТО `spawn(projectile)`.
- КОЛИ `custom: «на шляху барикада»` → ЯКЩО `path_exists(enemy, rift)` → ТО `custom: «орки обходять»`; інакше `custom: «атакують барикаду»`; `hp_zero(barricade)` → `disappear(barricade)`.
- КОЛИ `in_range(guardian, enemy, n)` → ТО `damage(n)` (лучник — здалеку, мечник — впритул).
- КОЛИ `input(fire)` → ЯКЩО `counter(mana, >=, cost)` → ТО `spawn(projectile)` / закляття, `counter(mana, -cost)`.
- КОЛИ `died(enemy)` → ТО `currency(+n)`, `rng(p)` → `spawn_at(potion|coins, тіло)`.
- КОЛИ `contact(player, potion)` → ТО `pickup`, `heal(player, n)` або `counter(mana, +n)`; КОЛИ `in_range(player, rift, n)` → ТО `heal(player, n)`.
- КОЛИ `hp_zero(player)` або `custom: «маг впав у прірву»` → ТО `respawn(player, rift)`, `counter(rift_points, -n)`.
- КОЛИ `reach(enemy, rift)` → ТО `disappear(enemy)`, `counter(rift_points, -1)` (великі — більше).
- КОЛИ `counter(rift_points, <=, 0)` → ТО `lose`, `restart`.
- КОЛИ `wave_cleared` → ТО `currency(+bonus)`; ЯКЩО `custom: «номер хвилі кратний 3»` and not `mode(Nightmare)` → ТО `custom: «перерва до натискання "почати хвилю"»`; інакше `timer(start, кілька секунд)` → `wave_start`.
- КОЛИ `custom: «остання хвиля очищена»` → ТО `win`, `window(end-screen)` з черепами.
- КОЛИ `level_end` → ТО `custom: «черепи 1–5 = f(залишок rift points, час проходження)»`; ЯКЩО `difficulty(Apprentice)` → ТО `custom: «максимум 2 черепи»`.
- КОЛИ `level_end` → ЯКЩО `first_time` and `custom: «рівень пройдено»` → ТО `unlock(новий предмет)`.
- КОЛИ `input(buy_upgrade, trap)` у spellbook → ЯКЩО `counter(skulls, >=, cost)` → ТО `custom: «одне постійне покращення пастки (шкода / ціна / оглушення)»`.
- Перемога: пережити всі хвилі рівня · Поразка: rift points = 0 · Рахунок: черепи 1–5 + очки для лідерборда (за вбивства й комбо (?)).

## Керування і ввід
- WASD/стік — біг; миша/правий стік — камера й приціл; ЛКМ — атака зброєю/постріл; ПКМ — альтернативна атака зброї (?).
- Цифри / хрестовина — вибір слота в панелі лоадауту (пастка, зброя, закляття, гвардієць); з пасткою в руці приціл показує контур на клітинках поверхні, натискання — поставити.
- Продаж — навести на пастку й утримувати кнопку (?).
- «Почати хвилю» — окрема клавіша в перерві.

## Вікна, меню, HUD
- `main-menu`: кампанія → `level-select` (24 фортеці в 3 актах) · налаштування → `settings-window` · лідерборд.
- `+window:loadout-select` — spellbook: вибір до 10 слотів перед стартом рівня; апгрейди пасток за черепи тут же.
- `+window:weaver-window` — вибір weaver-а й дерева тимчасових апгрейдів (пізніше в грі).
- `difficulty-select` — Apprentice / звичайна / Nightmare (Nightmare відкривається після кампанії (?)).
- `game-screen`: 3D-сцена, `hp-bar`, mana-бар (`energy-bar`), `coins`, `+ui:rift-points`, `wave-counter`, `+ui:trap-bar` (слоти лоадауту з цінами), `ghost-piece` (контур пастки на клітинках), `popup-text` (комбо-вбивства), `minimap` (?).
- `pause-menu`: продовжити, рестарт, вихід.
- `end-screen` — черепи, час, rift points; нові розблоковані предмети; кнопка повтору.
- Переходи: main-menu → level-select → loadout → game-screen ↔ pause → end-screen → level-select.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: 24 рівні кампанії, перше проходження рівня відкриває новий предмет.
- `meta-progression`: черепи → постійні покращення пасток; повтор старих рівнів заради кращого рейтингу.
- `stars-rating` у формі черепів (1–5); `difficulty-presets` (Apprentice обмежує рейтинг 2 черепами), `mode-hardcore`-подібний Nightmare (без перерв).
- `leaderboard-online` — рахунок рівня.
- `+feature:loadout-lock` — лоадаут фіксується з першою поставленою пасткою.

## Варіації й родичі
- Сиквели: Orcs Must Die! 2 (2012, кооп на двох), Unchained (PvP-MOBA), OMD 3 (великі «війнові» пастки), Deathtrap (2025, кооп на чотирьох, роглайт).
- Родичі: [dungeon-warfare](dungeon-warfare.md) (те саме «штовхни в лаву» у 2D з курсором), [dungeon-keeper](dungeon-keeper.md) (пастки підземелля), [desktop-tower-defense](desktop-tower-defense.md) і [fieldrunners](fieldrunners.md) (мейзинг — тут барикадами), [plants-vs-zombies](plants-vs-zombies.md) (кулдауни й лоадаут перед рівнем), Sanctum, Dungeon Defenders (TD від третьої особи).
- **Осі варіацій**: де стоїть пастка — лише підлога / підлога+стіна / ще й стеля · гравець — курсор / аватар, що стріляє сам · поразка — HP бази / пул очок, з якого платить і смерть гравця · перерви — кожні N хвиль / жодних.

## Цікавинки для курсу
- Пастки за поверхнями: клітинка має тип поверхні, пастка — список дозволених; легальність розміщення = поверхня + вільні клітинки + гроші — 🥉.
- Перезарядка пастки: стан armed/disarmed з cooldown і шкодою всім на клітинках — 📎.
- Барикада як мейзинг: перерахунок шляху BFS; якщо шляху нема — вороги атакують перешкоду замість «заборони будувати» — 🥈.
- Відкидання (spring) у небезпеку: імпульс + перевірка клітинки приземлення (лава, прірва, інша пастка) — 🥉.
- Пул rift points, з якого платять і прориви ворогів, і смерті гравця, і рейтинг 1–5 за залишок + час — 📎.
- Лоадаут з ≤10 слотів і блокування після першої пастки — 🌱.
- Повний рефанд при продажу: план «переставити оборону між хвилями» — 🌱.

## Мапа на каталог
- Є: `tower-placement` + `cursor-place` ↔ пастка під прицілом · `tower-range` ↔ стіна стріл · `enemy-waves`, `spawn-points`, `enemy-reached-base` ↔ розлом · `round-currency`, `shop-buyback` (тут — повний рефанд) · `drop-on-death`, `item-pickup` ↔ зілля й монети · `hp-damage`, `projectile-shot`, `shoot-cooldown`, `melee-vs-ranged` ↔ лучник/мечник · `speed-per-type` · `environment-death` ↔ лава/прірва · `impassable-cells`, `destructible-blocks`, `chase-bfs` ↔ барикада · `player-death`, `respawn` · `shop-between-levels` ↔ апгрейди за черепи · `in-round-upgrades` ↔ weaver · `difficulty-levels`, `sequential-levels`, `level-unlock`, `leaderboard`, `save-progress`, `event-points`.
- **Нема** → пропозиції карток:
  - `+trap-surfaces` «Пастка лише на свій тип поверхні (підлога/стіна/стеля)» · entities/legality · 🥉 · слот {surfaces}.
  - `+trap-rearm` «Пастка спрацьовує і перезаряджається» · entities/combat · 📎 · слот {cooldown}.
  - `+loadout-select` «Лоадаут перед рівнем» (з PvZ/Monster Train) · game-logic/economy · 🌱.
  - `+rift-points-pool` «Спільний пул життів бази, з якого платить і смерть гравця» · game-logic/lose · 📎.
  - `+skull-rating` «Рейтинг 1–N за залишок життів і час» · game-logic/score · 🌱.
  - `+knockback-push`, `+maze-by-barricade`, `+call-wave-early` — як у dungeon-warfare.

## Пропозиції до словників
- `+role:trap` — пастка гравця (а не стихія рівня): ціна, поверхня, перезарядка (Dungeon Warfare, OMD).
- `+role:base` — ціль ворогів з пулом життів (розлом, хатина, командний центр).
- `+cond:surface` — тип поверхні клітинки: floor / wall / ceiling.
- `+effect:sell` — прибрати свою споруду з поверненням валюти (TD-повтор).
- `+effect:knockback` — відкинути сутність імпульсом у напрямку.
- `+effect:rearm` — пастка знову готова (≈ `set_state(armed)`, але як окреме слово для TD).
- `+trigger:wave_break` — настала перерва між пачками хвиль.
- `+ui:rift-points` — лічильник життів бази; `+ui:trap-bar` — слоти лоадауту з ціною і кулдауном.
- `+window:loadout-select`, `+window:weaver-window` — вибір лоадауту / помічника з деревом апгрейдів.
- `+feature:loadout-lock` — лоадаут фіксується з першою дією рівня.
- `+card:trap-surfaces`, `+card:trap-rearm` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Orcs Must Die!](https://en.wikipedia.org/wiki/Orcs_Must_Die!) — rift points, 4–12 хвиль, перерви кожні 3 хвилі (крім Nightmare), лоадаут до 10 і блокування, поверхні пасток, перезарядка шипів, рефанд, потіони, респавн за rift points, weavers, черепи 1–5, Apprentice ≤ 2.
- [Steam: Orcs Must Die!](https://store.steampowered.com/app/102600/Orcs_Must_Die/) — 24 фортеці, 19 пасток і союзників, 6 зброй/заклять, 11 типів ворогів (орки, огри, летючі hellbats), Nightmare, лідерборд.
- [Gamepressure: OMD2 traps](https://www.gamepressure.com/orcsmustdie2/traps-p-1/zb3d3a) — барикада (протискаються в щілини або ламають повний блок), стельові пастки, пружина біля прірв (для сиквела).
- [Steam: Orcs Must Die! 2](https://store.steampowered.com/app/201790/Orcs_Must_Die_2/) — сиквел із коопом.
- YouTube: пошук «orcs must die 2011 gameplay».

## Непевне
- (?) Розмір пасток у клітинках (більшість 2×2, барикада 1×1?) і чи сітка однакова на всіх поверхнях.
- (?) Чи можна продавати пастки посеред бою, чи лише в перерві (Wikipedia привʼязує рефанд до перерви); чи рефанд справді повний.
- (?) Скільки rift points коштує смерть мага і скільки — великі вороги.
- (?) Чи дає ранній старт хвилі бонус (у сиквелах — так); формула часу для черепів.
- (?) Hellbat ігнорує підлогові пастки — логічно, але не перевірено; точний список 19 пасток OMD1 (fandom 402).
- (?) Комбо-очки за вбивства пастками для лідерборда.
