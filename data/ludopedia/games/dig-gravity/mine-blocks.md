---
title: Mine Blocks
slug: mine-blocks
aka: [Mine Blocks 1]
family: dig-gravity
also: [build-sim]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: both
  goal: none
platforms: [web, PC]
links:
  - {kind: official, url: "https://mineblocks.com/", best: true, note: "офіційний сайт Zanzlanz: список фіч Mine Blocks 1 і 2, лінки грати/завантажити"}
  - {kind: play, url: "https://mineblocks.com/1", note: "грати в браузері (HTML5)"}
  - {kind: play, url: "https://www.crazygames.com/game/mine-blocks", note: "CrazyGames: режими, клавіші, копання утриманням, крафт в інвентарі"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=fnR7djDnkyo", note: "відео оновлення з офіційного сайту"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mine+Blocks+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [dig-terrain, cursor-place, destructible-blocks, gravity-fall, move-by-input, inventory, inventory-items, inventory-limit, item-pickup, hp-damage, chase-player, spawn-random-cell, player-camera, save-game, controls-remap, keyboard-controls, cell-click, mode-select, +tile-mining-hold, +tool-per-block, +crafting-recipes, +hotbar, +creative-flight, +world-dimensions, +tame-mount, +wiring-components, +procedural-world]
proposes: ["+effect:craft", "+effect:mine", "+cond:holding", "+window:crafting-window", "+ui:hotbar", "+feature:mode-creative", "+card:tool-per-block", "+card:crafting-recipes", "+card:hotbar"]
author: opus
date: 2026-11-09
---

# Mine Blocks — Minecraft у двох вимірах: копай блоки, крафть інструменти, став блоки назад

## Суть
Браузерна 2D-гра за мотивами Minecraft від Zanzlanz: вид збоку на тайловий процедурний світ, де гравець утриманням миші розбиває блоки (потрібен правильний інструмент), збирає матеріали, крафтить у сітці інвентаря інструменти, броню й їжу, ставить блоки назад і відбивається від мобів. Понад 300 блоків і предметів, понад 20 істот, три виміри з підземеллями і босом-драконом. Для корпусу — найпростіший вхід у «копай + будуй + крафть» на сітці (поряд із [terraria-liquids.md](../build-sim/terraria-liquids.md)).

## Поле і час
- Квадратна тайлова сітка бічного виду; світ генерується випадково, ширший за екран — камера за гравцем.
- Real-time; гравітація для аватара й мобів (стрибок, падіння); мобі зʼявляються під час гри (`random: both`).
- Три виміри (окремі світи-поля) з переходом між ними (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | HP, інвентар, хотбар | ходить WASD, стрибає; копає й ставить блоки поруч; у creative — літає, не втрачає HP |
| Блок (земля, камінь, дерево, руда… 300+ разом з предметами) | terrain | вид, потрібний інструмент | утримання кліку руйнує; падає в інвентар як предмет |
| Предмет / блок у хотбарі | pickup | кількість | правий клік — поставити блок у вільну клітину або вжити (зʼїсти, використати) |
| Інструменти (сокира, кайло…) | pickup | матеріал | прискорюють/дозволяють добування свого типу блоків |
| Броня | pickup | — | екіпірується в інвентарі |
| Ворожі моби (кріпери, павуки, зомбі) | enemy | — | нападають на гравця в survival |
| Пес, свиня | neutral | — | пса можна приручити, на свині — їздити |
| Підземелля | zone | — | згенеровані структури з мобами й лутом (?) |
| Дракон | boss | — | бос одного з вимірів |
| Компоненти «проводки» | switch | — | механізми й сигнали (як redstone) (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ТО `move(player, dir)`; подвійне A/D → `speed(player, ×k)` (спринт).
- КОЛИ `tick` → ЯКЩО `not supported(player)` and not `mode(creative)` → ТО `fall(player)`.
- КОЛИ `input(hold_click, block)` → ЯКЩО `in_range(player, block, n)` → ТО `custom: «блок тріскає за час, залежний від інструмента»` → `set_cell(empty)`, `give(player, block_item)`.
- КОЛИ `input(hold_click, block)` → ЯКЩО `custom: «інструмент не підходить»` → ТО `custom: «довше / без дропу»` (?).
- КОЛИ `input(right_click, empty_cell)` → ЯКЩО `has(player, block)` → ТО `place(player, block)`, `take(player, block)`.
- КОЛИ `input(right_click_hold, food)` → ТО `use(player, food)` → `heal(player, n)`.
- КОЛИ `input(craft, recipe)` → ЯКЩО `has(player, ingredients)` → ТО `take(ingredients)`, `give(player, item)` — напр., дерев'яна сокира з дерева й каменю.
- КОЛИ `contact(enemy, player)` → ЯКЩО `mode(survival|hardcore)` → ТО `damage(player, n)`.
- КОЛИ `hp_zero(player)` → ЯКЩО `mode(hardcore)` → ТО `game_over` (?); інакше `respawn(player, spawn)` (?).
- КОЛИ `input(hold_click, mob)` → ТО `damage(mob, n)`; КОЛИ `hp_zero(mob)` → ТО `spawn(drops)` (?).
- КОЛИ `input(use, dog)` → ЯКЩО `custom: «предмет для приручення»` → ТО `set_side(dog, player)` (?).
- Scavenger Hunt (мультиплеєр): КОЛИ `counter(found, =, 10)` → ТО `win`; КОЛИ `timer(8 min)` спливає → ТО `custom: «кінець гри, рахунок знайденого»`.
- Перемога: нема (пісочниця); дракон — умовна мета. Поразка: HP 0 (у hardcore — остаточно (?)).

## Керування і ввід
- WASD — рух; подвійне A/D — спринт; у creative подвійне W/Space — політ.
- Ліва кнопка утриманням — копати блок / бити істоту; права — поставити блок із вибраного слота хотбару; права утриманням — вжити/зʼїсти.
- E — інвентар: крафт і броня; клавіші перепризначаються в налаштуваннях.

## Вікна, меню, HUD
- `main-menu`: Singleplayer (нова/збережена гра), Minigames, Multiplayer Scavenger Hunt, Skins, Settings (?) — розкладка з памʼяті.
- `mode-select`: Survival / Creative / Hardcore при створенні світу.
- `game-screen`: світ збоку; HUD — `hp-bar`, `hotbar` (слоти предметів), підсвітка блока під курсором.
- `inventory-window` (E): сітка предметів, слоти броні, сітка крафту (`crafting-window`).
- `save-slots` / список збережених світів; `settings-window` (клавіші); вікно скінів (`skin-select`, 11 000+ скінів гравців).

## Фічі поза полем
- `mode-sandbox` (creative), `mode-hardcore`, survival; міні-ігри; онлайн Scavenger Hunt (10 предметів за 8 хв).
- `save-slots` світів, обмін мапами (`level-sharing`), команди (консоль), кастомні скіни.
- Mine Blocks 2 (альфа): нескінченні світи, освітлення, інтерфейс крафту, текстур-паки; Mine Blocks 3 скасовано.

## Варіації й родичі
- Minecraft (оригінал, 3D), [terraria-liquids.md](../build-sim/terraria-liquids.md) і [minecraft-redstone.md](../build-sim/minecraft-redstone.md) — рідини й проводка в тайлах.
- [motherload.md](motherload.md), [steamworld-dig.md](steamworld-dig.md) — копання вглиб без будування.
- **Осі варіацій**: блок після копання — «зникає / стає предметом в інвентарі»; час копання — «миттєво / залежить від інструмента і блока»; повернення — «лише руйнуєш / ставиш назад (будування)».

## Цікавинки для курсу
- Копання утриманням із часом, що залежить від пари «блок × інструмент» — 📎.
- Блок → предмет → знову блок (інвентар як «запас клітин») — 🌱.
- Крафт за рецептами з інгредієнтів у сітці — 🥉 (таблиця рецептів як дані).
- Хотбар: вибраний слот визначає, що робить правий клік — 🌱.
- Режими survival / creative / hardcore як прапорці одних правил — 🌱.
- Scavenger Hunt: знайти 10 предметів за 8 хв у спільному світі — 🥈 (мережа).

## Мапа на каталог
- Є: `dig-terrain` · `cursor-place` ↔ поставити блок у вільну клітину · `destructible-blocks` · `gravity-fall` · `move-by-input` · `inventory` / `inventory-items` / `inventory-limit` · `item-pickup` · `hp-damage` · `chase-player` ↔ моби (?) · `spawn-random-cell` ↔ поява мобів (?) · `player-camera` · `save-game` · `controls-remap` · `keyboard-controls` · `cell-click` · `mode-select`.
- **Нема** → пропозиції карток:
  - `+tool-per-block` «Блок добувається відповідним інструментом» · entities/interact · 📎 · слоти {block → tool, time}.
  - `+crafting-recipes` «Крафт предметів за рецептами» · entities/state · 🥉.
  - `+hotbar` «Швидкі слоти: вибраний визначає дію» · interface/input · 🌱.
  - Також: `+tile-mining-hold`, `+creative-flight`, `+world-dimensions`, `+tame-mount`, `+wiring-components`, `+procedural-world`.

## Пропозиції до словників
- `+effect:craft` — інгредієнти → предмет за рецептом (можна `take` + `give`, але рецепт — окреме поняття).
- `+effect:mine` — поступове руйнування блока утриманням (зараз `custom` + `set_cell`).
- `+cond:holding` — у вибраному слоті хотбару предмет X (інструмент, блок, їжа).
- `+window:crafting-window` — сітка крафту з результатом.
- `+ui:hotbar` — ряд швидких слотів (ширше за ⏳ `inventory-bar`: визначає дію кліку).
- `+feature:mode-creative` — нескінченні ресурси, безсмертя, політ (близько ⏳ `mode-sandbox`).

## Джерела
- ⭐ [mineblocks.com](https://mineblocks.com/) — Zanzlanz, Flash → HTML5; 300+ блоків і предметів, 20+ істот, creative/survival/hardcore, Scavenger Hunt, обмін мапами, 3 виміри, підземелля, дракон, крафт, зачарування, зілля, риболовля, команди й проводка, скіни, пес і свиня; Mine Blocks 2 і 3.
- [CrazyGames](https://www.crazygames.com/game/mine-blocks) — клавіші, копання утриманням правильним інструментом, крафт і броня в інвентарі (E), creative без шкоди з польотом, Scavenger Hunt 10 предметів за 8 хв.
- [Грати](https://mineblocks.com/1) · [відео оновлення](https://www.youtube.com/watch?v=fnR7djDnkyo) — лінки з офіційного сайту (вміст відео не дивився).

## Непевне
- (?) Рік першого релізу: у черзі 2011; на CrazyGames — грудень 2021 (це дата лістингу HTML5). Поле `year` не заповнене.
- (?) Чи падають пісок/гравій, чи течуть вода й лава (як у Minecraft) — у відкритих джерелах нема; правило гравітації записане лише для аватара.
- (?) Смерть у survival — респавн чи втрата інвентаря; hardcore — чи видаляє світ.
- (?) Голод, день/ніч, освітлення в Mine Blocks 1 — не підтверджено (освітлення згадано лише для Mine Blocks 2).
- (?) Вікі гри (mineblocks.com/1/wiki) віддала 403 — сутності за нею не звірені.
