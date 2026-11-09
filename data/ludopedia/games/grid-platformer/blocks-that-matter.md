---
title: Blocks That Matter
slug: blocks-that-matter
aka: [BTM, Tetrobot]
family: grid-platformer
also: [falling-match]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2011
platforms: [PC, Mac, Linux, Xbox 360, OpenPandora]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Blocks_That_Matter", best: true, note: "Tetrobot, збір блоків буром і ударом знизу, будування по 4, скрині-колекції"}
  - {kind: steam, url: "https://store.steampowered.com/app/111800/", note: "типи блоків, лінії 8+, 40 + 20 рівнів, редактор і Workshop"}
  - {kind: other, url: "https://www.destructoid.com/review-blocks-that-matter/", note: "огляд: режим будування в паузі, пісок/дерево/обсидіан, зірки за ефективність"}
  - {kind: other, url: "https://www.speedrun.com/blocks_that_matter/guides/yqxp6", note: "гайд speedrun.com про рухомі блоки (бачив у пошуку; 403)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=blocks+that+matter+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, dig-terrain, destructible-blocks, inventory-items, inventory-limit, polyomino-placement, piece-rotate-flip, line-match-clear, floor-types, inertia-slide, chase-player, touch-death, reach-exit, sequential-levels, level-unlock, level-select, in-game-editor, editor-palette, editor-playtest, level-exchange, game-pause, +drill-to-inventory, +build-mode-pause, +bump-collect-from-below, +burnable-block, +collapse-on-step, +efficiency-stars, +hidden-collectible-block, +tool-upgrade-unlocks-material]
proposes: ["+effect:drill(cell)", "+effect:burn(cell)", "+cond:drillable(cell)", "+cond:line_length(cells, op, n)", "+trigger:bump(a, cell)", "+window:build-mode", "+ui:block-stock", "+card:drill-to-inventory", "+card:build-mode-pause", "+card:collapse-on-step"]
author: opus
date: 2026-11-09
---

# Blocks That Matter — робот-бур видобуває блоки з рівня і викладає їх тетроміно-платформами

## Суть
Tetrobot — маленький робот у бічному платформері. Він **видобуває блоки** (буром збоку або ударом знизу), складає їх у запас і в режимі будування викладає **фігурою з 4 блоків**, створюючи сходинки, мости й стіни. Лінію з 8+ блоків можна зламати, як у Tetris, щоб звільнити матеріал або прохід. Ядро — економіка матеріалу: блоки скінченні, тож часом доводиться розбирати власні споруди.

## Поле і час
- Бічний вид, квадратна сітка блоків; рівень більший за екран (камера за роботом (?)).
- Real-time платформер з гравітацією: робот ходить, стрибає, падає.
- Режим будування — пауза: час стоїть, гравець розкладає фігуру; збудоване зʼявляється миттєво після зняття паузи.
- Частина блоків має власну фізику: пісок і обсидіан падають, гравій обсипається під ногами, лід ковзає.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Tetrobot | player | бур, запас блоків | ходить, стрибає, свердлить блок збоку, б'є блок знизу → блок у запас |
| Пісок | object | бурится | падає без опори (`gravity-fall`) |
| Дерево | object | бурится | може горіти |
| Камінь | object | бурится після апгрейду (?) | звичайна опора |
| Залізо | object | (?) | інша поведінка — не перевірено |
| Обсидіан | object | не бурится | падає без опори, як пісок |
| Діамант | object | (?) | найтвердіший, бурится пізно (?) |
| Гравій | terrain | не бурится | падає, коли на нього стати; не падає, якщо зруйнувати блок під ним |
| Лід | object | не бурится | від удару буром ковзає (`inertia-slide`) |
| Блок, що обвалюється | terrain | — | руйнується, коли на ньому стоять (Destructoid) |
| Вогняна істота | enemy | — | переслідує робота (`chase-player`) |
| Скриня-колекція (Block That Matters) | pickup | 1 на рівень | схована; відкриває бонусні рівні й історію ігор |
| Вихід рівня | static | — | дістатись → рівень пройдено (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(robot, dir)`; КОЛИ `input(jump)` → ТО `custom: «стрибок»`.
- КОЛИ `tick` → ЯКЩО `not supported(robot)` → ТО `fall(robot)`.
- КОЛИ `input(drill, dir)` → ЯКЩО `custom: «блок поруч бурится цим буром»` → ТО `disappear(block)`, `pickup(robot, block)` (пропозиція `drill`).
- КОЛИ `custom: «робот б'є блок знизу стрибком»` → ТО `pickup(robot, block)`.
- КОЛИ `input(drill, ice)` → ТО `slide(ice, dir)`.
- КОЛИ `input(build_mode)` → ТО `window(build-mode)`, `custom: «час зупинено»`.
- КОЛИ `input(place, shape)` → ЯКЩО `counter(stock, >=, 4)` і `fits(shape, cells)` → ТО `place(robot, tetromino)`, `counter(stock, -4)`.
- КОЛИ `input(break, line)` → ЯКЩО `custom: «у лінії ≥ 8 блоків»` → ТО `clear(line)`.
- КОЛИ `tick` → ЯКЩО `cell(x, sand)` або `cell(x, obsidian)` і `not supported(x)` → ТО `fall(x)`.
- КОЛИ `enter(robot, gravel)` → ТО `fall(gravel)`.
- КОЛИ `enter(robot, crumbling_block)` → ТО `custom: «блок обвалюється»`.
- КОЛИ `custom: «вогонь торкнувся дерева»` → ТО `custom: «дерево горить»` (?).
- КОЛИ `contact(robot, fire_creature)` → ТО `lose` → рестарт (?).
- КОЛИ `picked(robot, chest)` → ТО `unlock(bonus_level)`.
- КОЛИ `reach(robot, exit)` → ТО `win`, `next_level`.
- Перемога: дійти до виходу · Поразка: ворог/небезпека (?) · Рахунок: зірки за ефективність при повторі.

## Керування і ввід
- Геймпад/клавіатура: рух, стрибок, бур (напрям), вхід у режим будування.
- Режим будування: вибрати 4 клітини фігури біля робота, підтвердити (?); окремий режим ламання лінії (?).
- Матеріал вибирається з запасу — порядок/тип блоків має значення (пісок у фігурі падатиме) (?).

## Вікна, меню, HUD
- `main-menu`: Adventure → `level-select`; Bonus levels; Editor → `editor-window`; Options → `settings-window`.
- `game-screen`: рівень, HUD запасу блоків (`custom: «block-stock»`), позначка скрині рівня (?).
- `custom-window` «режим будування»: поле на паузі, сітка, привид фігури (`ghost-piece`).
- `pause-menu`, `end-screen` рівня з зірками.
- `achievements-window` (Steam, 30+ досягнень).

## Фічі поза полем
- Пригода: 40 рівнів; 20 бонусних рівнів, що відкриваються скринями (Steam).
- 40 колекційних «Blocks That Matter» — відсилки до ?-блоку, Companion Cube, кубика Рубіка, кубика, Boulder Dash; відкривають історію блочних ігор.
- `level-editor` + `level-sharing` через Steam Workshop.
- `stars-rating` за ефективність проходження; `achievements`; cloud-save.
- Нові типи бурених блоків відкриваються за сюжетом (апгрейд бура).

## Варіації й родичі
- Попередник: Tuper Tario Tros. (та сама студія, Mario × Tetris); наступник — Tetrobot and Co. (?).
- Родичі: Lode Runner (копання), Solomon's Key (створити/зламати блок), Terraria/Minecraft (видобуток і будування), Tetris (тетроміно й лінії).
- Осі: **матеріал** (необмежений / скінченний з рівня) · **форма будування** (по 1 блоку / тетроміно / довільна) · **фізика блоку** (тримається / падає / ковзає / горить).

## Цікавинки для курсу
- Запас блоків як ресурс + видобуток з рівня — 📎.
- Режим будування на паузі з привидом тетроміно і перевіркою «вміщується» — 🥉.
- Ламання лінії 8+ (пошук горизонтальних/вертикальних рядів) — 📎.
- Типи блоків з різною фізикою (падає, обсипається від кроку, ковзає від удару) — 🥉 (таблиця взаємодій).
- Перевірка розвʼязності з обмеженим матеріалом — 🥇.

## Мапа на каталог
- Є: `gravity-fall` · `dig-terrain` ↔ бур · `destructible-blocks` · `inventory-items` + `inventory-limit` ↔ запас блоків · `polyomino-placement` + `piece-rotate-flip` ↔ тетроміно · `line-match-clear` ↔ лінія 8+ · `floor-types` ↔ типи блоків · `inertia-slide` ↔ лід · `chase-player` · `touch-death` · `reach-exit` · `in-game-editor`, `level-exchange`.
- **Нема** → пропозиції карток:
  - `+drill-to-inventory` «Видобути блок у запас» · entities/interact · 📎.
  - `+build-mode-pause` «Будування на паузі з привидом фігури» · interface/input · 🥉.
  - `+bump-collect-from-below` «Удар знизу забирає блок» · entities/interact · 🌱.
  - `+burnable-block` «Блок горить» · entities/state · 📎.
  - `+collapse-on-step` «Блок обвалюється під ногами» · entities/state · 🌱.
  - `+efficiency-stars` «Зірки за ефективність» · game-logic/score · 🌱.
  - `+hidden-collectible-block` «Схована колекційна скриня рівня» · game-logic/win · 🌱.
  - `+tool-upgrade-unlocks-material` «Апгрейд інструмента відкриває матеріал» · levels/progression · 📎.

## Пропозиції до словників
- `+effect:drill(cell)` — видобути блок у запас (не просто `disappear`, бо поповнює ресурс).
- `+effect:burn(cell)` — клітина горить і зникає/поширює вогонь.
- `+cond:drillable(cell)` — блок піддається поточному інструменту.
- `+cond:line_length(cells, op, n)` — довжина суцільної лінії обраних блоків.
- `+trigger:bump(a, cell)` — удар знизу стрибком.
- `+window:build-mode` — режим будування на паузі.
- `+ui:block-stock` — запас блоків за типами.
- `+card:drill-to-inventory` · `+card:build-mode-pause` · `+card:collapse-on-step` — див. вище.

## Джерела
- ⭐ [Wikipedia: Blocks That Matter](https://en.wikipedia.org/wiki/Blocks_That_Matter) — Tetrobot, збір блоків ударом/буром, будування по 4, скрині, платформи, премія Dream Build Play.
- [Steam](https://store.steampowered.com/app/111800/) — шість типів блоків, лінії 8+, 40 + 20 рівнів, 40 колекцій, редактор і Workshop.
- [Destructoid: огляд](https://www.destructoid.com/review-blocks-that-matter/) — будування на паузі, пісок падає, дерево горить, обсидіан не бурится, вогняні вороги, обвали, зірки.
- [speedrun.com: рухомі блоки](https://www.speedrun.com/blocks_that_matter/guides/yqxp6) — пісок, обсидіан, гравій, лід (зміст — з пошукового сніпета, сторінка 403).

## Непевне
- (?) Правило розміщення тетроміно: чи має фігура торкатися наявних блоків/робота і чи можна обертати перед викладанням.
- (?) Ламання лінії 8+: окремий режим, які типи можна ламати, чи блоки повертаються в запас.
- (?) Поведінка заліза, каменю й діаманта; порядок відкриття бурених типів.
- (?) Ліміт запасу (кількість слотів) і чи важить порядок блоків у фігурі.
- (?) Що вбиває робота (вогняні істоти, падіння, роздавлення піском) і чи є вихід як клітина.
