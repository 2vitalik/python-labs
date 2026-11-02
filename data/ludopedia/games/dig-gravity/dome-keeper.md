---
title: Dome Keeper
slug: dome-keeper
family: dig-gravity
also: [tower-lanes, roguelike]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2022
platforms: [PC, macOS, Linux, Xbox Series]
links:
  - {kind: fandom, url: "https://domekeeper.wiki.gg/wiki/Dome_Keeper_Wiki", best: true, note: "wiki.gg: дві фази, ресурси, хранителі, куполи, гаджети, вороги, режими"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dome_Keeper", note: "огляд: копання між хвилями, таймер, лазер і меч, Relic Hunt, Ludum Dare 48"}
  - {kind: steam, url: "https://store.steampowered.com/app/1637320/Dome_Keeper/", note: "Steam: фічі, кооп на 4, versus"}
  - {kind: fandom, url: "https://domekeeper.wiki.gg/wiki/Engineer", note: "бур, джетпак, місткість, формула сповільнення, трос рветься >6 клітин"}
  - {kind: fandom, url: "https://domekeeper.wiki.gg/wiki/Relic_Hunt", note: "розміри мап, цикл, вага хвилі, умова перемоги"}
  - {kind: fandom, url: "https://domekeeper.wiki.gg/wiki/Gadgets", note: "усі гаджети і як їх знаходять"}
  - {kind: fandom, url: "https://domekeeper.wiki.gg/wiki/Enemies", note: "22 види монстрів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dome+Keeper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-8dir, impassable-cells, enemy-waves, inventory-limit, round-currency, in-round-upgrades, item-pickup, hp-damage, player-camera, difficulty-levels, field-size-picker, telegraphed-intents, status-panel, game-pause, controls-remap, +dig-terrain, +dig-wall, +core-deposit, +carry-object, +phase-cycle, +fog-of-war, +carry-tether, +gadget-chamber-choice, +wave-weight-budget, +base-turret-aim, +deliver-goal]
proposes: ["+trigger:wave_start", "+trigger:wave_cleared", "+effect:deposit", "+effect:choose", "+effect:drop", "+cond:inside_base", "+role:resource", "+ui:wave-timer", "+ui:dome-hp", "+window:loadout-select", "+window:upgrade-window", "+axis:control", "+card:carry-tether", "+card:gadget-chamber-choice", "+card:wave-weight-budget", "+card:base-turret-aim", "+card:deliver-goal"]
author: opus
date: 2026-11-02
---

# Dome Keeper — копай під куполом, доки тикає таймер, і встигни назад до хвилі монстрів

## Суть
Хранитель на джетпаку буром розкопує клітинну шахту під скляним куполом і тягне на тросі руду (залізо, воду, кобальт) назад у купол, де вона стає валютою апгрейдів. Над шахтою тикає **таймер хвилі**: коли він спливає, на купол нападають монстри, і відбиватися можна лише зброєю купола, якою керує хранитель зсередини. Головне рішення кожного циклу — наскільки глибоко піти й скільки нести, щоб устигнути назад. Гібрид: `avatar` у шахті (копання, `dig-gravity`) + `cursor`-подібне керування туреллю на поверхні (`tower-lanes`); тека — за першим, бо 80 % часу — копання.

## Поле і час
- Шахта — прямокутна сітка під куполом (Relic Hunt: 40×40, 50×50, 60×65, 70×90 клітин), краї непорушні; горизонтальні шари з дедалі твердішими клітинами, своїми звуками й фауною; приховані печери й камери гаджетів 2×2.
- Поверхня — окрема «арена» навколо купола: монстри приходять з боків і з повітря.
- Невидиме, доки не прокопано (`info: hidden`); мапа і розкладка ресурсів — процедурні; склад хвилі — випадковий у межах бюджету (`random: both`).
- Real-time: цикл = фаза копання (таймер) + фаза бою (до знищення всіх монстрів). Тривалість циклу росте з часткою видобутого заліза: `60 + 45 × √(тайлів/1000) × %заліза`.
- **Межовий випадок:** рух хранителя вільний (джетпак, прискорення), не по клітині; клітинні — ґрунт, руда, копання.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Хранитель (Engineer) | player | сила бура 2, швидкість 56, місткість 3 | літає джетпаком; бʼє клітину раз на 0.35 с; тягне ресурси на тросі |
| Хранитель (Assessor, Infiltrator, Beastmaster) | player | свої здібності | альтернативні хранителі (DLC частково) (?) |
| Купол | static | HP (Laser 800) | база: приймає ресурси, магазин апгрейдів, ціль монстрів; HP 0 → поразка |
| Зброя купола (лазер / меч / артилерія / тесла) | ally | шкода, швидкість обертання | керується хранителем зсередини; лазер обертається навколо купола |
| Клітина ґрунту | terrain | міцність за шаром | знімає міцність ударами бура; 0 → порожнеча |
| Межа / корінна порода | static | — | непорушна (корінну пробиває лише Power Drill) |
| Залізо | resource | 1–4 з руди, більше з глибиною | основна валюта апгрейдів |
| Вода | resource | 1–4 | підсилення гаджетів, частина апгрейдів |
| Кобальт | resource | 1–3 | ремонт купола, опір шкоді |
| Камера гаджета | container | 2×2 | розкопати, принести вміст у купол → вибір 1 з 2 гаджетів або 2 кобальту |
| Реліквія | container | під 12 особливими клітинами + 2–5 вузлів | донести в купол → фінальна хвиля |
| Вузол (node) | switch | 2–5 за розміром мапи | активувати всі, щоб відкрити реліквію |
| Монстри (Walker, Flyer, Diver, Tick, Worm, Breeder…) | enemy | вага, HP, атака | 22 види: наземні, літаючі, стрільці, телепортери, закопувачі, спавнери |
| Гаджети (Shield, Repellent, Orchard, Droneyard, Lift, Teleporter, Probe…) | ally | слот | щит, відстрочка хвилі, бафи, ліфт ресурсів, портал шахта–купол, радар руди |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ТО `move(keeper, dir)` вільно, швидкість × `(1 − 0.01 × loss × N(N+1)/2)` для N ресурсів на тросі.
- КОЛИ `input(drill, dir)` → ЯКЩО `cell(target, rock)` → ТО `damage(drill_strength)` кожні 0.35 с; міцність 0 → `set_cell(empty)`; ЯКЩО `cell(target, ore)` → ТО `spawn(resource × 1–4)`.
- КОЛИ `input(pickup)` → ЯКЩО `count(tether, <, capacity)` → ТО `attach(resource, keeper)`; `input(drop)` → `detach`.
- КОЛИ `custom: «довжина троса > 6 клітин»` → ТО `detach(all)` — ресурси падають.
- КОЛИ `enter(resource, dome)` → ТО `deposit`: `currency(iron|water|cobalt, +n)`.
- КОЛИ `input(buy, upgrade)` → ЯКЩО `inside_base(keeper)` and `has(iron, price)` → ТО `set_value(stat)` (бур 4/8/14/22, швидкість 4/8/12/18, місткість 4/8/12/20 заліза…).
- КОЛИ `timer(cycle)` спливає → ТО `wave_start`: `spawn_at(monsters, edges)` за бюджетом ваги (цикл, видобуто, складність).
- КОЛИ `contact(monster_attack, dome)` → ТО `hp(dome, -n)`; КОЛИ `hp_zero(dome)` → ТО `lose` (кінець забігу).
- КОЛИ `input(aim|fire)` → ЯКЩО `inside_base(keeper)` → ТО `custom: «лазер обертається по дузі й бʼє в напрямку»`; поза куполом — зброя мовчить.
- КОЛИ `wave_cleared` → ТО `timer(next_cycle)` — новий цикл копання.
- КОЛИ `enter(gadget_item, dome)` → ТО `choose(gadget_a | gadget_b | 2 cobalt)`.
- КОЛИ `input(repellent)` → ТО `timer(+n)` — відстрочка хвилі; Shield поглинає шкоду й заряджається щохвилі.
- КОЛИ `all(nodes active)` and `custom: «12 клітин над реліквією прокопані»` → ТО реліквію можна взяти.
- КОЛИ `enter(relic, dome)` → ТО `wave_start(final)` вагою max(800, 4.5 × поточна); фінальна хвиля = `win`; якщо купол падає у фінальній — реліквія спрацьовує, все одно `win`.
- Перемога: реліквія в куполі й фінальна хвиля. Поразка: HP купола 0 у звичайному циклі. Рахунок: цикли, видобуто (Prestige — на очки) (?).

## Керування і ввід
- WASD/стрілки — політ і копання в напрямку руху (бур бʼє клітину, в яку впираєшся); Space — підібрати, Q — скинути вантаж; перепризначення в Options → Input.
- У куполі: ті самі напрямки обертають лазер/наводять зброю, дія — вогонь; меню апгрейдів — у куполі.
- Геймпад; локальний кооп до 4 і versus (хто довше вживе / більше доставить).

## Вікна, меню, HUD
- `main-menu`: Relic Hunt / Prestige / Guild Assignments → `mode-select`.
- `loadout-select`: хранитель, купол, основний гаджет, розмір мапи, складність, модифікатори забігу.
- `game-screen`: шахта знизу, купол зверху; HUD — `wave-timer` (відлік до хвилі), `dome-hp`, лічильники заліза/води/кобальту (`coins`), стрілка/лічильник монстрів хвилі (?).
- `upgrade-window` (у куполі): дерево апгрейдів хранителя, купола, гаджетів з цінами.
- `choose`-вікно гаджета з камери (1 з 2 або кобальт).
- `end-screen`: перемога/поразка зі статистикою циклів і видобутку; `settings-window`, `pause-menu`.

## Фічі поза полем
- `difficulty-presets` (Normal, Hard, Brutal, «You asked for it» — цикли на 24 с коротші), `custom-difficulty` (розмір мапи, модифікатори).
- `mode-classic` (Relic Hunt), Prestige (на рахунок) (?), Guild Assignments (челенджі), `mode-coop` до 4, `mode-versus`.
- `meta-progression`: перемоги відкривають доповнення (supplements) до гаджетів; нові куполи й хранителі.
- `remap-controls`, `gamepad-support`.

## Варіації й родичі
- Dome Romantik (Ludum Dare 48, 2021, 9-те місце) — джем-прототип.
- Родичі: SteamWorld Dig і Motherload (копай — неси — апгрейдь), Mindustry (ядро як склад), tower defense (хвилі до бази), FTL-подібна «база + вилазка».
- **Осі варіацій**: як ресурси потрапляють на базу — «несеш сам на тросі / ліфт / дрони / телепорт»; що тисне — «таймер хвилі / паливо / повітря»; хто захищає базу без тебе — «ніхто / автотурелі-гаджети / щит».

## Цікавинки для курсу
- Цикл фаз «копання за таймером → бій до зачистки» з таймером, що росте від видобутку — 🥉.
- Трос з вантажем: місткість, квадратичне сповільнення `N(N+1)/2`, обрив за довжиною — 🥉.
- Склад хвилі за бюджетом ваги: випадкові монстри набираються до цільової ваги з цикла й багатства гравця — 🥈.
- Міцність клітини за шаром проти сили бура з апгрейдами — 📎.
- Знахідка в шахті → вибір 1 з 2 на базі — 📎.
- Ручна турель купола, що працює лише коли гравець усередині — 📎 (стан «де аватар» вмикає іншу механіку).
- Реліквія як «донести предмет на базу» + фінальна хвиля — 🌱.

## Мапа на каталог
- Є: `move-8dir` (умовно; насправді вільний політ) · `impassable-cells` · `enemy-waves` (слот final_wave — реліквія) · `inventory-limit` ↔ місткість троса · `round-currency` ↔ залізо/вода/кобальт · `in-round-upgrades` · `item-pickup` · `hp-damage` ↔ HP купола · `player-camera` · `difficulty-levels` · `field-size-picker` ↔ розмір мапи · `telegraphed-intents` ↔ таймер хвилі · `status-panel` · `game-pause` · `controls-remap`.
- **Нема** → пропозиції карток:
  - `+carry-tether` «Вантаж на тросі: сповільнення й обрив» · entities/state · 🥉 · слоти {capacity, slow_fn, max_len: 6}.
  - `+gadget-chamber-choice` «Знахідка в полі → вибір 1 з 2 на базі» · game-logic/economy · 📎 · слот {options: 2, fallback: 2 cobalt}.
  - `+wave-weight-budget` «Склад хвилі за бюджетом ваги» · game-logic/waves · 🥈 · слоти {weight_fn, min: 15}.
  - `+base-turret-aim` «Зброя бази, яку наводить гравець, коли він у базі» · entities/combat · 📎.
  - `+deliver-goal` «Донести предмет на базу» · game-logic/win · 🌱.
  - Повтори: `+dig-terrain`, `+dig-wall`, `+core-deposit` (ресурс у купол = валюта), `+carry-object`, `+phase-cycle` (слоти {phases: dig, fight; timer: росте з видобутком}), `+fog-of-war` (невідкрита шахта).

## Пропозиції до словників
- `+trigger:wave_start` / `+trigger:wave_cleared` ⏳ — повтор; тут вони перемикають фази гри.
- `+effect:deposit` — предмет із троса/інвентаря на базу = валюта (може бути `currency` + `disappear`, слабка).
- `+effect:choose` ⏳ — повтор (вибір гаджета); `+effect:drop` — скинути вантаж (пара до `attach`/`detach` ⏳).
- `+cond:inside_base` — аватар у базі (вмикає турель і магазин).
- `+role:resource` ⏳ — повтор (залізо, вода, кобальт).
- `+ui:wave-timer` — відлік до наступної хвилі (близько ⏳ `next-wave-preview` + `timer-countdown`); `+ui:dome-hp` — HP бази окремо від гравця.
- `+window:loadout-select` — вибір хранителя/купола/гаджета/мапи перед забігом (ширше за ⏳ `character-select`); `+window:upgrade-window` ⏳ — повтор.
- `+axis:control` — у шахті `direct`, у куполі — наведення турелі: одна гра, два режими.

## Джерела
- ⭐ [Dome Keeper Wiki](https://domekeeper.wiki.gg/wiki/Dome_Keeper_Wiki) — дві фази, ресурси, 4 хранителі, 4 куполи, гаджети, вороги, режими.
- [Wikipedia](https://en.wikipedia.org/wiki/Dome_Keeper) — копання між хвилями, таймер до хвилі, лазер і меч, Relic Hunt, Bippinbits/Raw Fury, Ludum Dare 48.
- [Engineer](https://domekeeper.wiki.gg/wiki/Engineer) — 0.35 с на удар, місткість 3→30, формула сповільнення, обрив троса >6 клітин, таблиця апгрейдів, клавіші Space/Q.
- [Relic Hunt](https://domekeeper.wiki.gg/wiki/Relic_Hunt) — розміри мап і вузли, формула циклу, вага хвилі, 12 клітин над реліквією, фінальна хвиля.
- [Gadgets](https://domekeeper.wiki.gg/wiki/Gadgets) — основні й знайдені гаджети, камери 2×2, вибір 1 з 2 або 2 кобальту.
- [Enemies](https://domekeeper.wiki.gg/wiki/Enemies) · [Minerals](https://domekeeper.wiki.gg/wiki/Minerals) · [Laser Dome](https://domekeeper.wiki.gg/wiki/Laser_Dome) — монстри, ресурси 1–4/1–3, HP 800 і шкода 15.
- [Steam](https://store.steampowered.com/app/1637320/Dome_Keeper/) — фічі, кооп до 4, versus.

## Непевне
- (?) Поразка «HP купола 0 у звичайному циклі» — з памʼяті; сторінка Relic Hunt описує лише фінальну хвилю.
- (?) Чи на HUD є лічильник/стрілки монстрів хвилі.
- (?) Правила Prestige-режиму (рахунок) і Guild Assignments — не відкривав.
- (?) Скільки хранителів у базовій грі (Steam: два типи; вікі: чотири — ймовірно з DLC/оновленнями).
- (?) `move-8dir` — наближення: насправді вільний політ з прискоренням.
