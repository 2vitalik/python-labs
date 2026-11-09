---
title: Sandustry
slug: sandustry
aka: []
family: dig-gravity
also: [build-sim]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: collect
year: 2026
platforms: [Windows, macOS, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2764460/Sandustry/", best: true, note: "опис: кожен піксель — фізична сутність і ресурс; лід → вода → пара → дощ, пісок вбирає воду, мокрий пісок → золото; конвеєри, фільтри, дрони, труби, помпи, ліфти; ранній доступ з 13.08.2026"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Sandustry", note: "геймплей: літаючий прибулець, золото з мокрого піску через shaker, kinetic press, collector-зони, дерево навичок, цілі-тири, процедурний світ із seed"}
  - {kind: steam, url: "https://store.steampowered.com/app/3490390/Sandustry_Demo/", note: "демо (31.01.2025): той самий опис, лава, вогнемет, ракетниця, артефакти, сховища"}
  - {kind: other, url: "https://kotaku.com/sandustry-steam-factory-incremental-mining-crafting-lantto-games-2000725317", note: "Kotaku: лопати, launcher тягнеш мишею вгору, конвеєр drag-ом, shaker-«сходи», Sweeper Drone, список цілей, fluxite"}
  - {kind: other, url: "https://gamerant.com/steam-games-like-terraria-factorio-sandustry/", note: "GameRant: вибухівка, перенаправлення лави, «conveyor spaghetti»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sandustry+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-by-input, gravity-fall, cell-transform, interaction-table, dig-terrain, destructible-blocks, cursor-place, drag-drop-piece, row-conveyor, explode-area, objective-text, seed-share, player-camera, +falling-sand-cell, +phase-transition, +absorb-wet, +water-cycle, +separator-machine, +collector-zone, +launcher-block, +free-rebuild, +goal-tier-unlock, +skill-tree, +sweeper-drone, +seeded-generator, +pass-through-own-build]
proposes: ["+cond:temp", "+effect:separate", "+role:material", "+window:skill-tree", "+card:absorb-wet", "+card:water-cycle", "+card:separator-machine", "+card:launcher-block", "+card:free-rebuild", "+card:goal-tier-unlock", "+axis:field-pixel"]
author: opus
date: 2026-11-09
---

# Sandustry — фабрика на falling-sand: кожен піксель світу — ресурс, який треба намочити, просіяти й довезти конвеєром

## Суть
2D-світ планети з піксельних матеріалів: пісок і золото сипляться, вода тече й випаровується, лід тане, насіння проростає. Гравець — маленький літаючий прибулець, що копає й **безкоштовно** ставить, переносить і прибирає блоки-машини: конвеєри, катапульти-launcher, сито-shaker, колектори. Перша виробнича лінія — **намочити пісок, просіяти й зібрати золото**; золото відкриває гілки дерева навичок і нові тири цілей. Це Factorio, де «предмети» — частинки клітинної фізики, а не іконки на стрічці.

## Поле і час
- Бічний вид, піксельна сітка: піксель — найменша одиниця матеріалу; сипучі (пісок, золото) мають частинкову фізику, рідини — потік і температуру (кипіння, замерзання).
- Світ процедурний з seed, який можна змінити; біоми (трав'яний старт, пустеля, інші за апгрейдами), підземні печери, страти порід, випадкові підземні споруди-сховища.
- Real-time; поразки не описано — темп задає список цілей.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Прибулець | player | політ на реактивній тязі; ширяння й прохід крізь свої споруди — апгрейди | копає лопатами, ставить/переносить/прибирає блоки |
| Пісок | material | — | сиплеться; вбирає сусідню воду → мокрий пісок |
| Мокрий пісок | material | — | сировина для shaker |
| Золото | resource | — | сиплеться; збирається в колектор; валюта навичок |
| Залишок (residue) | material | — | з shaker; спалений і стиснутий у kinetic press → ще золото |
| Вода | material | — | тече; водойми вичерпуються піском; кипить → пара |
| Пара | material | — | повертається дощем |
| Лід / сніг | material | — | нагрітий тане → вода; вогнемет розчищає |
| Лава | hazard | — | тече; її перенаправляють |
| Насіння → квітка | material | — | полите проростає; квітку підпалюють → ресурс |
| Порода, страти | terrain | — | руйнується після відкриття інструментів |
| Fluxite | resource | — | для апгрейдів |
| Конвеєр | conduit | напрям | везе матеріал уздовж; малюється drag-ом |
| Launcher | conduit | напрям викиду | підкидає матеріал угору; тягнеш мишею вгору, відхил убік задає напрям |
| Shaker | static | «сходи» | розділяє мокрий пісок на золото й залишок |
| Collector-зона | sink | — | приймає й зберігає золото |
| Kinetic press | static | — | стискає спалений залишок у золото |
| Sweeper Drone | ally | ранній апгрейд | збирає матеріал із землі, коли гравітація не допомагає |
| Фільтри, труби, помпи, ліфти | conduit | — | логістика матеріалів і рідин |
| Артефакт | pickup | — | знайдений — витрачаєш ресурси, щоб відкрити його бонус |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(alien, dir)` — політ; ЯКЩО `has(alien, hover)` → `custom: «ширяє на місці»`; ЯКЩО `has(alien, phase)` → ТО `custom: «проходить крізь власні споруди»`.
- КОЛИ `input(dig, cell)` → ЯКЩО `cell(target, dirt|sand)` → ТО `set_cell(target, empty)`; тверда порода — `block`, доки не відкрито інструмент.
- КОЛИ `input(place, block)` → ЯКЩО `free(cells)` → ТО `place(alien, block)` — без витрат; так само переносити й прибирати.
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(sand|gold)` — `custom: «сипучий піксель осипається вниз / по діагоналі»`.
- КОЛИ `adjacent(sand, water)` → ТО `transform(sand, wet_sand)`, `disappear_b` — пісок вбирає воду, водойма меншає.
- КОЛИ `tick` → ЯКЩО `custom: «лід нагрітий»` → ТО `transform(ice, water)`; ЯКЩО `custom: «вода кипить»` → ТО `transform(water, steam)`.
- КОЛИ `tick` → ЯКЩО `custom: «пара охолола вгорі»` → ТО `transform(steam, rain)` — кругообіг води; підземне нагрівання дає опади.
- КОЛИ `contact(water, seed)` → ТО `transform(seed, flower)`; КОЛИ `contact(fire, flower)` → ТО `custom: «квітка згоряє в ресурс»`.
- КОЛИ `enter(material, conveyor)` → ТО `move(material, belt_dir)`.
- КОЛИ `enter(material, launcher)` → ТО `custom: «викинути вгору в заданому напрямку»`.
- КОЛИ `enter(wet_sand, shaker)` → ТО `custom: «розділити на золото й залишок»`.
- КОЛИ `enter(residue, kinetic_press)` → ЯКЩО `state(residue, burnt)` → ТО `transform(residue, gold)`.
- КОЛИ `enter(gold, collector)` → ТО `disappear_a`, `currency(+1)`.
- КОЛИ `tick` → ЯКЩО `count(loose_material, >, 0)` → ТО `custom: «Sweeper Drone підбирає матеріал із землі й несе в лінію»`.
- КОЛИ `input(flamethrower)` → ЯКЩО `cell(target, ice)` → ТО `transform(ice, water)`.
- КОЛИ `input(rocket|explosive)` → ТО `explode(area, into: debris)` — швидке копання.
- КОЛИ `counter(goal_progress, >=, quota)` → ТО `unlock(tier)`, `message(next_goal)` — перша ціль: переробити N мокрого піску.
- КОЛИ `input(buy, skill)` → ЯКЩО `counter(gold, >=, cost)` → ТО `currency(-cost)`, `unlock(skill)` — машини, інструменти, апгрейди.
- КОЛИ `picked(alien, artifact)` → ТО `custom: «витратити ресурси, щоб відкрити бонус артефакту»`.
- Перемога: нема (ранній доступ) — прогрес цілями й деревом. · Поразка: не описана. · Рахунок: золото.

## Керування і ввід
- Рух прибульця (клавіші; «уславлений курсор» — RPS за Wikipedia), копання лопатами.
- Будівництво мишею: click-and-drag — конвеєр малюється в напрямку руху; launcher тягнеш угору, легкий відхил убік задає напрям викиду. Блоки ставляться, переносяться й прибираються безкоштовно, тому лінію можна переробляти без штрафу.
- Інструменти: вогнемет (лід), ракетниця, вибухівка.

## Вікна, меню, HUD
- `game-screen`: піксельний світ, споруди, прибулець; `objective-text` — постійно оновлюваний список цілей.
- `custom-window` «дерево навичок»: гілки за золото й fluxite, тири за виконані цілі.
- `dialogue-window`: Archon Pri ставить завдання, Flight Officer Zoe (зелена кішка) — гід навчання (`tutorial-window`).
- `settings-window`; Steam: 23 мови, досягнення, Workshop (моди), хмара.
- Переходи: (не описані) — меню → новий світ (seed) → game-screen ↔ дерево навичок.

## Фічі поза полем
- `seed-input`: процедурний світ з seed, який можна змінити.
- `tutorial` + `onboarding-hints` (Zoe); `achievements`; `cloud-save`; `mod-support` (власні мапи, будівлі, процеси); `localization` (23 мови).
- Прогресія `level-unlock`-подібна: цілі → тири → дерево навичок; ранній доступ на рік (обіцяні нові будівлі, ресурси, ланцюги, квести, біоми).

## Варіації й родичі
- Родичі в корпусі: [Noita](noita.md), [The Powder Toy](the-powder-toy.md), [Sandspiel](sandspiel.md), [Sandboxels](sandboxels.md) (піксельна фізика матеріалів), [Sugar, Sugar](sugar-sugar.md) (направити потік сипучого), [Dome Keeper](dome-keeper.md) і [Motherload](motherload.md) (копати по ресурс); з `build-sim` — [Factorio](../build-sim/factorio-belts.md) і [Mindustry](../build-sim/mindustry.md) (конвеєри), Terraria.
- **Осі варіацій**: «предмет» на конвеєрі — «іконка-одиниця (Factorio) / піксель фізики, що сиплеться й розсипається (тут)»; перетворення — «рецепт у машині / реакція матеріалів на полі (вода + пісок)»; ціна будівництва — «ресурси / безкоштовно, платиш лише відкриттям (тут)».

## Цікавинки для курсу
- Сипучий піксель, що вбирає сусідню воду й стає іншим матеріалом, — 📎 (клітинний автомат з парною реакцією).
- Кругообіг: лід → вода → пара → дощ на тих самих правилах температури — 🥉.
- Конвеєр, що везе не предмети, а частинки з гравітацією (просипаються на краях) — 🥈.
- Машина-розділювач «один матеріал → два» (shaker) і колектор-зона як стік — 📎.
- Цілі-тири + дерево навичок як прогресія без поразки — 🌱.
- Безкоштовна перебудова (ставити/переносити/прибирати без ціни) — 🌱, але змінює весь дизайн: помилки не карають.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` ↔ пісок і золото · `cell-transform` + `interaction-table` ↔ реакції матеріалів · `dig-terrain` ↔ лопати · `destructible-blocks` ↔ порода · `cursor-place` + `drag-drop-piece` ↔ будівництво мишею · `row-conveyor` ↔ конвеєр · `explode-area` ↔ ракетниця, вибухівка · `objective-text` ↔ список цілей · `seed-share` ↔ seed світу · `player-camera`.
- **Нема** → пропозиції карток:
  - `+falling-sand-cell` (вже пропонована) · `+phase-transition` (вже пропонована) — лід/вода/пара.
  - `+absorb-wet` «Матеріал вбирає сусідню рідину й стає іншим» · entities/interact · 📎.
  - `+water-cycle` «Випаровування → пара → дощ» · entities/interact · 🥉.
  - `+separator-machine` «Машина ділить матеріал на продукти» · entities/interact · 📎; `+collector-zone` «Зона-стік рахує зібране» · game-logic/score · 🌱.
  - `+launcher-block` «Блок-катапульта з напрямом викиду» · entities/move · 📎.
  - `+free-rebuild` «Будувати, переносити й прибирати без ціни» · game-logic/economy · 🌱.
  - `+goal-tier-unlock` «Виконана ціль відкриває тир» · levels/progression · 🌱; `+skill-tree` «Дерево навичок за валюту» · game-logic/economy · 📎.
  - `+sweeper-drone` «Дрон-збирач розсипаного» · entities/move · 📎; `+seeded-generator` (вже пропонована); `+pass-through-own-build` «Аватар проходить крізь свої споруди» · entities/legality · 🌱.

## Пропозиції до словників
- `+cond:temp(a, op, n)` — температура клітини/матеріалу (лід тане, вода кипить); повтор з корпусу.
- `+effect:separate(a → b, c)` — розділити матеріал на два продукти (shaker).
- `+role:material` — піксель речовини з фізикою, не одиниця економіки (повтор з Sandspiel/Powder Toy).
- `+window:skill-tree` — дерево навичок/технологій з гілками й цінами.
- `+card:absorb-wet`, `+card:water-cycle`, `+card:separator-machine`, `+card:launcher-block`, `+card:free-rebuild`, `+card:goal-tier-unlock` — див. «Мапа на каталог».
- `+axis:field-pixel` — поле-маска пікселів (повтор з Lemmings, Noita); у шапці `square`.

## Джерела
- ⭐ [Steam: Sandustry](https://store.steampowered.com/app/2764460/Sandustry/) — опис реакцій матеріалів, машин і логістики, ранній доступ, платформи, мови, Workshop.
- [Wikipedia: Sandustry](https://en.wikipedia.org/wiki/Sandustry) — прибулець на реактивній тязі, безкоштовні блоки, shaker, kinetic press, collector, launcher, дерево навичок і тири, процедурний світ із seed, біоми, персонажі, продажі.
- [Steam: Sandustry Demo](https://store.steampowered.com/app/3490390/Sandustry_Demo/) — дата демо, лава, вогнемет, ракетниця, артефакти, сховища, дика природа.
- [Kotaku](https://kotaku.com/sandustry-steam-factory-incremental-mining-crafting-lantto-games-2000725317) — лопати, малювання launcher і конвеєра мишею, Sweeper Drone, список цілей, fluxite.
- [GameRant](https://gamerant.com/steam-games-like-terraria-factorio-sandustry/) — вибухівка, лава, «spaghetti».
- YouTube: пошук «Sandustry gameplay».

## Непевне
- (?) Чи є туман/невідкриті ділянки (`info`), поразка чи небезпека для прибульця (лава?), голод/паливо — не знайдено.
- (?) Як саме сипучі поводяться на конвеєрі (просипаються з країв?) і що робить «дика природа» — лише згадки.
- (?) Розмір світу, точні ціни навичок, кількість тирів — не бачив.
- (?) Меню й екрани поза грою — не описані; `custom-window` дерева навичок — з опису «skill tree».
