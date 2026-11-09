---
title: Pixel Miner
slug: pixel-miner
aka: []
family: dig-gravity
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: hidden
  random: both
  goal: score
year: 2026
platforms: [Windows]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4809600/Pixel_Miner/", best: true, note: "опис: idle/incremental копання випадкових печер; руда зберігається в інвентарі-«falling sand simulation»; здача в піч бази за кредити; автономні дрони; апгрейди; престиж за Ancient Ore; 6 скріншотів UI; вихід 6.11.2026"}
  - {kind: other, url: "https://steamcommunity.com/stats/4809600/achievements", note: "26 досягнень з описами: глибини 5/20/100, вихід з рівня, 16 руд з одного блока, престиж-тири 2–4, Depth Charge, Warp Relay, 20 дронів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pixel+Miner+Maddogs+gameplay", note: "пошук; є трейлер на Steam"}
stage: v1
coverage: 45
mechanics: [move-by-input, dig-terrain, destructible-blocks, hp-damage, explode-area, teleport-cooldown, inventory-limit, round-currency, in-round-upgrades, shop-window, shop-preview, stairs-levels, fog-of-war, player-camera, keyboard-controls, cell-click, save-progress, +sand-inventory, +core-deposit, +sell-cargo, +auto-drone-miner, +drone-roles, +ore-yield-multiplier, +depth-goal, +light-radius, +cave-generation, +prestige-reset, +meta-tier-unlock, +bulk-buy, +remote-deposit, +idle-automation]
proposes: ["+role:material", "+effect:deposit", "+ui:sand-inventory", "+ui:bulk-buy-modifier", "+window:prestige-tree", "+feature:prestige-reset", "+card:sand-inventory", "+card:auto-drone-miner", "+card:drone-roles", "+card:prestige-reset", "+card:bulk-buy"]
author: opus
date: 2026-11-09
---

# Pixel Miner — idle-шахта згори: руда сиплеться в рюкзак-пісочницю, дрони копають самі, престиж скидає все за древню руду

## Суть
Мінімалістичний піксельний idle/incremental: шахтар від бази в центрі мапи бурить блоки випадкових печер, збирає руду й здає її в піч бази за кредити, а кредити йдуть на апгрейди бура, швидкості, інвентаря, світла, вибухівки й дронів. Незвичне — **інвентар як falling-sand контейнер**: руда кожного блока падає пікселями в колонку STORAGE і пересипається там, тож заповненість видно буквально. Далі гру забирає автоматизація: рої дронів трьох типів копають і прокладають тунелі, а **престиж** за рідкісну Ancient Ore скидає прогрес в обмін на постійні апгрейди 4 тирів. Межова гра сімʼї: гравітація діє лише в інвентарі, поле — вид згори без падіння.

## Поле і час
- Вид згори; рівень («глибина») — піксельна сітка блоків із випадково згенерованими печерами й тунелями; база в центрі, люк-вихід — окремо на мапі.
- Видно лише освітлене: світло навколо шахтаря (радіус — апгрейд Lumens), бази й дронів; решта — темрява з видимими сполохами руди поруч (`info: hidden`).
- Real-time, без ворогів і поразки; камера за шахтарем.
- Глибини послідовні: вихід або Breach Lance — на шар нижче; світ можна розширювати (Breach: «+8 блоків»).
- Окреме «поле» — колонка STORAGE праворуч: вертикальний контейнер, де пікселі руди падають і лягають шарами за кольором.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шахтар | player | бур: шкода, cooldown, радіус; швидкість; радіус світла | літає печерами, бурить блоки в радіусі |
| Камінь | terrain | твердість (Erosion зменшує) | бур знищує; з шансом дає руду (Cracking) |
| Рудний блок | resource | тип (≥20 типів), ціна | знищений — дає кілька руд (досягнення — 16 з одного блока) |
| Ancient Ore | resource | рідкісна; апгрейд «Mark ancient ores» підсвічує | валюта престижу |
| Піксель руди в рюкзаку | material | колір = тип | падає й пересипається в колонці STORAGE |
| База з піччю | static | центр мапи; іконки магазину й систем | DEPOSIT: руда → кредити (€) |
| Люк-вихід | static | — | перехід на наступну глибину |
| Mining-дрон | ally | власний мінібак, швидкість (Servos), затримка (CPU) | копає найближчу або найдорожчу руду |
| Excavator-дрон | ally | радіус (Payload) | тунелить до найближчої руди |
| Prospector-дрон | ally | Sensor — ×2 вихід | підвищує вихід руди |
| Вибухівка | projectile | шкода, радіус, запас x/y, регенерація | руйнує блоки площею (до тисяч за раз) |
| Depth Charge | projectile | клавіша Z, cooldown | вибух у точці курсора |
| Warp Relay | — | клавіша X, cooldown | телепорт шахтаря до курсора |
| Breach Lance | — | клавіша C | прокопати шар униз |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(miner, dir)` (?) — печерами, крізь відкриті клітини.
- КОЛИ `input(drill)` → ЯКЩО `in_range(miner, block, drill_radius)` → ТО `damage(block, drill_damage)`; `timer(cooldown)` між ударами.
- КОЛИ `hp_zero(block)` → ТО `disappear(block)`; ЯКЩО `cell(block, ore)` → ТО `give(miner, ore × yield)`.
- КОЛИ `destroyed(stone)` → ЯКЩО `prob(cracking)` → ТО `give(miner, ore)`.
- КОЛИ `picked(miner, ore)` → ЯКЩО `custom: «у колонці STORAGE є місце»` → ТО `spawn_at(ore_pixel, storage_top)`; інакше `custom: «руда не влазить»` (?).
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(ore_pixel)` — falling sand усередині інвентаря.
- КОЛИ `picked(miner, ore)` → ЯКЩО `prob(relay)` → ТО `custom: «руда одразу здається на базу»`.
- КОЛИ `input(deposit)` → ЯКЩО `custom: «шахтар на базі або є Remote»` (?) → ТО `currency(+value)`, `custom: «колонка STORAGE спорожніє»`.
- КОЛИ `tick` → ЯКЩО `state(drone, mining)` → ТО `custom: «летить до найближчої або найвигіднішої руди й копає»`.
- КОЛИ `tick` → ЯКЩО `state(drone, excavator)` → ТО `custom: «прокладає тунель до найближчої руди»`.
- КОЛИ `counter(drone_cargo, >=, capacity)` → ТО `custom: «дрон везе руду на базу»`; ЯКЩО `has(player, hoppers)` → ТО `custom: «здає віддалено»`.
- КОЛИ `tick` → ЯКЩО `has(player, fracking)` and `prob(fracking)` → ТО `custom: «mining-дрон кидає вибухівку»`.
- КОЛИ `input(explosive)` → ЯКЩО `counter(explosives, >, 0)` → ТО `explode(circle, blast_radius)`, `counter(explosives, -1)`.
- КОЛИ `timer(recycle)` → ЯКЩО `counter(explosives, <, max)` → ТО `counter(explosives, +1)`.
- КОЛИ `input(Z)` → ЯКЩО `timer(cooldown, ==, 0)` → ТО `explode(circle, at_cursor)`; КОЛИ `input(X)` → ТО `teleport(miner, cursor)`; КОЛИ `input(C)` → ТО `next_level`.
- КОЛИ `enter(miner, exit)` → ТО `next_level`, `counter(depth, +1)`.
- КОЛИ `tick` → ТО `reveal(cells_in_light_radius)` — світло шахтаря, бази й дронів.
- КОЛИ `input(buy, upgrade)` → ЯКЩО `counter(credits, >=, price)` → ТО `currency(-price)`, `custom: «рівень апгрейда +1, ціна росте»`; Shift — до ×5, Ctrl — скільки вистачить.
- КОЛИ `input(prestige)` → ЯКЩО `has(player, ancient_ore)` → ТО `custom: «скинути кредити й шоп-апгрейди, нарахувати PTS»` (?).
- КОЛИ `counter(pts, >=, 16|64|256)` → ТО `unlock(prestige_tier_2|3|4)`.
- Перемога: нема (нескінченні глибини). · Поразка: нема. · Рахунок: кредити, глибина, Ancient Ore.

## Керування і ввід
- Рух шахтаря й бур — клавіатура/миша (?); курсор — ціль для Depth Charge (Z) і Warp Relay (X); C — Breach Lance.
- Кнопки на панелях: DEPOSIT, MENU, вкладка TAB (таблиця руд), «?» INFO у секціях магазину.
- Купівля: клік — 1 рівень, Shift — до 5, Ctrl — максимум.

## Вікна, меню, HUD
- `game-screen`: печера в центрі; ліва панель — лічильник ORE (Ancient Ore), MINING DRONES — список дронів, у кожного міні-колонка вантажу, підказки ролей (Prospector / Excavator / Mining); права панель — € (`coins`), колонка STORAGE (`+ui:sand-inventory`), кнопка DEPOSIT, смуга x/y (запас вибухівки?), MENU.
- `custom-window` TAB — таблиця типів руд: колір, кількість, вартість у €.
- `upgrade-window` (магазин): Drill (+1 шкоди), Coolant (−5 % cooldown), Engine (+5 % швидкості), Storage (більший інвентар), Lumens (+5 % світла), Blast (+1 радіус бура); секції Prospector Drones (Drone, Sensor, Servos, CPU) і Explosives (Reagent, Assembly, Precursor, Catalyst); бічні вкладки закриті замками; кнопка MAX.
- `+window:prestige-tree` «Ancient Technology»: PTS і ORE; 4 тири по 6 апгрейдів (тир 2 — 16 PTS, тир 3 — 64, тир 4 — 256), невідкриті — «???».
- `pause-menu` / `settings-window` — за кнопкою MENU (?).
- Переходи: game-screen ↔ магазин (база) ↔ Ancient Technology; вихід → нова глибина.

## Фічі поза полем
- `meta-progression` через `+feature:prestige-reset`: Ancient Ore → PTS → постійні апгрейди (Alloys, Supply, Motors, Cracking, Compact, Subsidy, Analysis, Breach, Relay, Remote, Erosion, Refining, Payload, Fracking, Recycle, Hoppers, Biogeology, Operations, Singularity, Depth Charge, Warp Relay, Breach Lance).
- `achievements` (26, Steam) — частина як виклики: глибина 5 без апгрейдів магазину, вихід без жодного зламаного блока й телепорту, вибух, що нічого не зламав.
- `stats`, `cloud-save` (Steam), `localization` (EN, JA, ZH-CN); демо з 8.10.2026.

## Варіації й родичі
- Копати → здати → апгрейд: [Motherload](motherload.md) (продаж вантажу, глибина), [Dome Keeper](dome-keeper.md) і [Wall World](wall-world.md) (здача на базу), [SteamWorld Dig](steamworld-dig.md) (світло й рюкзак), [Pocket Mine](pocket-mine.md) (idle-кліки по блоках), [Mr. Driller](mr-driller.md) (глибина як мета).
- Інвентар як окреме поле-пазл — [Diablo II](../build-sim/diablo2-inventory.md), [Tarkov](../build-sim/tarkov-inventory.md), [Backpack Hero](../build-sim/backpack-hero.md); тут не сітка-тетріс, а сипучка. Falling sand як симуляція світу — [Noita](noita.md), [Sandspiel](sandspiel.md).
- **Осі варіацій**: інвентар — «лічильник / слоти / сітка фігур / пісочниця пікселів (тут)»; автоматизація — «нема / дрони з ролями (тут) / програма команд»; скидання — «нема / забіг роглайту / престиж-валюта (тут)».

## Цікавинки для курсу
- Інвентар-пісочниця: руда падає пікселями в колонку, місткість = площа — 📎 (falling sand в одному стовпці + перевірка заповненості).
- Дрони з трьома ролями (найближча руда / найдорожча / тунель) — 🥉: вибір цілі й BFS-тунель.
- Світло як туман війни з радіусом-апгрейдом — 📎.
- Магазин з рівнями апгрейдів, ростом ціни й купівлею ×5 / max — 🌱.
- Престиж: скинути прогрес за валюту, тири за порогами 16/64/256 — 📎.
- Вибух радіусом, що ламає тисячі блоків за раз, і chance-дроп руди з каменю — 🌱.

## Мапа на каталог
- Є: `move-by-input` ↔ рух шахтаря · `dig-terrain` + `destructible-blocks` + `hp-damage` ↔ бур і твердість блоків · `explode-area` ↔ вибухівка й Depth Charge · `teleport-cooldown` ↔ Warp Relay · `inventory-limit` ↔ колонка STORAGE · `round-currency` ↔ € · `in-round-upgrades` + `shop-window` + `shop-preview` ↔ магазин з описом ефекту · `stairs-levels` ↔ глибини · `fog-of-war` ↔ світло · `player-camera` · `keyboard-controls` ↔ Z/X/C, Shift/Ctrl · `cell-click` ↔ ціль курсором · `save-progress` ↔ Steam Cloud.
- **Нема** → пропозиції карток:
  - `+sand-inventory` «Інвентар — falling-sand контейнер» · entities/state · 📎.
  - `+auto-drone-miner` «Автономний дрон-збирач» · entities/move · 🥉; `+drone-roles` «Ролі дронів з різною ціллю» · entities/move · 🥉.
  - `+ore-yield-multiplier` «Блок дає N одиниць ресурсу» · game-logic/economy · 🌱.
  - `+prestige-reset` «Скидання прогресу за постійну валюту» · game-logic/economy · 📎; `+meta-tier-unlock` «Тири дерева за порогами очок» · levels/progression · 🌱.
  - `+bulk-buy` «Купити ×N / максимум» · game-logic/economy · 🌱; `+remote-deposit` «Здача ресурсу без повернення на базу» · game-logic/economy · 🌱.
  - `+cave-generation` «Печери шумом / random walk» · levels/generation · 🥉; `+idle-automation` «Гра йде сама» · game-logic/economy · 📎.
  - `+core-deposit`, `+sell-cargo`, `+depth-goal`, `+light-radius` (вже пропоновані).

## Пропозиції до словників
- `+role:material` — піксель речовини (повтор: Sandustry, Noita) — тут піксель руди в рюкзаку.
- `+effect:deposit` — здати вантаж на базу за валюту (повтор: Dome Keeper, Wall World).
- `+ui:sand-inventory` — колонка інвентаря, де предмети падають пікселями; `+ui:bulk-buy-modifier` — модифікатор Shift/Ctrl для кількості покупки.
- `+window:prestige-tree` — дерево постійних апгрейдів за престиж-валюту з тирами за порогами.
- `+feature:prestige-reset` — добровільне скидання прогресу за постійні бонуси.
- `+card:sand-inventory`, `+card:auto-drone-miner`, `+card:drone-roles`, `+card:prestige-reset`, `+card:bulk-buy` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Pixel Miner](https://store.steampowered.com/app/4809600/Pixel_Miner/) — опис (через `api/appdetails`): falling-sand інвентар, піч бази, дрони, апгрейди, престиж; 6 скріншотів: HUD, магазин, Ancient Technology з тирами й клавішами Z/X/C.
- [Steam: досягнення Pixel Miner](https://steamcommunity.com/stats/4809600/achievements) — 26 описів: глибини, вихід, 16 руд з блока, ≥20 типів руд, тири престижу, 20 дронів.
- YouTube: пошук «Pixel Miner Maddogs gameplay».

## Непевне
- (?) Гра вийшла 6.11.2026, відгуків і вікі нема — усе з опису, скріншотів і досягнень.
- (?) Чи пікселі руди в STORAGE взаємодіють (густина, змішування) чи просто пересипаються; що дає Compact «ores stack up to 7».
- (?) Як саме рухається шахтар (WASD чи клік) і чи бур автоматичний; чи DEPOSIT працює далеко від бази без Remote.
- (?) Смуга x/y під DEPOSIT — запас вибухівки (за апгрейдом Assembly «+1 max explosive»), не підтверджено.
- (?) Що саме скидає престиж і чи генерується кожна глибина заново.
