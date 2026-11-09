---
title: Space Run
slug: space-run
aka: ["Space Run: Fast and Safe Delivery"]
family: tower-lanes
also: [build-sim]
klass: cursor
axes:
  field: hex
  time: realtime
  opponent: ai
  info: partial
  random: none
  goal: race
year: 2014
platforms: [PC, macOS, Linux]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Space_Run", best: true, note: "гекс-платформа, зброя назовні, живлення від сусіда, вантаж корпорацій, гайки, два пороги бонусу за час, зірки-репутація"}
  - {kind: steam, url: "https://store.steampowered.com/app/275670/Space_Run/", note: "модулі: лазери, ракетниці, щити, двигуни, генератори; повтор місій із новими модулями"}
  - {kind: other, url: "https://operationrainfall.com/?p=137250", note: "огляд: лазер біля краю, ракетниця будь-де з фіксованим напрямом, щит, глушилка, генератор живить сусідів, вибухівка, VIP, бос-пірат із ланцюгом"}
  - {kind: other, url: "https://www.gog.com/game/space_run", note: "опис GOG: астероїди, пірати, конкуренти-перевізники"}
  - {kind: other, url: "https://gamegrin.com/reviews/space-run-galaxy-review", note: "сиквел Space Run Galaxy (2016): місток, крафт, онлайн-галактика"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Space+Run+2014+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [tower-placement, cursor-place, hp-damage, projectile-shot, coverage-area, multi-cell-size, orientation-state, round-currency, drop-on-death, item-pickup, time-bonus, explode-area, level-unlock, level-select, shop-between-levels, +hex-grid-render, +adjacency-power, +outward-facing-slot, +cargo-occupies-cells, +explosive-cargo, +thrust-speed, +hover-collect, +stars-rating, +reputation-unlock, +weapon-jam, +disable-chain, +cargo-production]
proposes: ["+cond:faces_void", "+ui:bonus-tier-timer", "+card:adjacency-power", "+card:outward-facing-slot", "+card:cargo-occupies-cells"]
author: opus
date: 2026-11-09
---

# Space Run — корабель із гексів як поле TD: вантаж, двигуни й гармати борються за ті самі клітини

## Суть
Корабель-платформа з гексагональних клітин летить маршрутом доставки; гравець у реальному часі ставить на гекси вантаж, двигуни, зброю, щити й генератори. Головна напруга — **просторова**: зброя мусить дивитись назовні, у порожній космос, пасажири теж хочуть край, вантаж займає клітини, а частині модулів потрібне живлення від сусіднього генератора. Нагорода — за вцілілий вантаж і швидкість доставки; це «перегони» з дедлайном, а не просто виживання хвиль.

## Поле і час
- Поле — **плаский корпус із гексів** (форма задана місією); навколо — космос, звідки летять астероїди й вороги. Модулі бувають на одну або кілька клітин.
- Сусідство гексів — 6 напрямків; воно визначає і живлення (генератор → сусіди), і «погляд» модуля (гекс перед ним має бути поза корпусом).
- Real-time: корабель летить маршрутом, швидкість залежить від кількості двигунів; місія триває до прибуття, в середньому ~10 хв (огляд).
- Будувати можна **під час польоту**: на старті місії корпус порожній, гравець одразу кладе вантаж і хоча б один двигун.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гекс корпусу | terrain | вільний / зайнятий | клітина для модуля; край корпусу межує з космосом |
| Ящик вантажу | object | цінність | займає гекс; уцілілий наприкінці — у нагороду |
| Вибухівка | object | цінність | знищена — шкодить кораблю навколо; треба прикривати |
| VIP-пасажири | object | потребує живлення | лише на краю, дивляться назовні; без живлення гинуть |
| Вантаж інших корпорацій | object | своє правило розміщення | кожна корпорація — свій тип вантажу з власним обмеженням |
| Механік | spawner | — | виробляє додаткові ящики під час місії → більша нагорода |
| Двигун (thruster) | tower | +швидкість | без двигунів корабель не долетить до дедлайну; бос їх вимикає |
| Лазерна турель | tower | дешева, влучає й у дрібні астероїди | потребує вільного гекса **назовні**; після апгрейда можна повертати |
| Ракетниця | tower | дорога, велика шкода | ставиться будь-де; напрям фіксований; ракети летять над модулями |
| Генератор щита | tower | радіус у гексах | силове поле над сусідніми гексами; поки щит цілий — атаки не проходять |
| Глушилка (jammer) | tower | — | вимикає ворожу зброю на час; краще проти великих босів |
| Генератор живлення | source | — | живить модулі в сусідніх гексах |
| Гайки (lug nuts) | resource | — | валюта будівництва; капають із часом і з уламків |
| Уламок-дроп | pickup | кількість гайок | лишається від знищеного ворога; збирається наведенням курсора |
| Астероїд | hazard | розмір | летить на корабель, шкодить модулю при контакті |
| Піратський винищувач | enemy | — | атакує корабель і вантаж |
| Конкурент-перевізник | enemy | — | суперник у доставці; його вантаж можна атакувати |
| Піратський бос | boss | великий корабель | на підльоті «світловий ланцюг» вимикає всі двигуни; кружляє й стріляє, часто тікає за 1–2 хв |
| Пункт призначення | static | — | прибуття = кінець місії |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «порожній корпус заданої форми»`, `custom: «стартовий запас гайок»`.
- КОЛИ `input(place, module, hex)` → ЯКЩО `free(hex)` and `fits(module, hex)` and `counter(lug_nuts, >=, cost)` → ТО `place(player, module)`, `currency(-cost)`; інакше `block`.
- КОЛИ `input(place, laser, hex)` → ЯКЩО `custom: «гекс у напрямку погляду — поза корпусом»` → ТО `place(player, laser)`; інакше `block`.
- КОЛИ `input(place, vip, hex)` → ЯКЩО `custom: «гекс на краю, погляд назовні»` → ТО `place(player, vip)`; інакше `block`.
- КОЛИ `input(place, missile_launcher, hex)` → ТО `place(player, missile_launcher)`, `face(missile_launcher, dir)` назавжди.
- КОЛИ `input(rotate, laser)` → ЯКЩО `custom: «відкрито апгрейд повороту»` → ТО `face(laser, dir)`.
- КОЛИ `tick` → ЯКЩО `adjacent_count(module, power_generator, >=, 1)` → ТО `set_state(module, powered)`; інакше `clear_state(module, powered)`.
- КОЛИ `tick` → ЯКЩО `state(module, powered)` → ТО `custom: «посилений режим / особлива здібність модуля»`; сильні версії модулів без живлення не працюють.
- КОЛИ `tick` → ЯКЩО `state(vip, powered)` → ТО `custom: «пасажири живі»`; інакше `damage(vip, n)`.
- КОЛИ `in_range(laser, target, n)` → ЯКЩО `line_of_sight(laser, target)` → ТО `spawn(laser_shot)`.
- КОЛИ `in_range(missile_launcher, target, n)` → ТО `spawn(missile)`; ракета `custom: «летить над власними модулями»`.
- КОЛИ `contact(hostile_shot, hex)` → ЯКЩО `state(hex, shielded)` → ТО `damage(shield, n)`, `disappear_a`; інакше `damage(module, n)`.
- КОЛИ `hp_zero(shield)` → ТО `clear_state(covered_hexes, shielded)`.
- КОЛИ `contact(asteroid, module)` → ТО `damage(module, n)`, `disappear_a`.
- КОЛИ `hp_zero(module)` → ТО `disappear(module)`, `set_cell(hex, free)`.
- КОЛИ `destroyed(explosive)` → ТО `explode(area, n)`: шкода сусіднім модулям.
- КОЛИ `timer(every)` → ТО `currency(+1)` гайок.
- КОЛИ `destroyed(enemy|asteroid)` → ТО `spawn(drop)`; КОЛИ `input(hover, drop)` → ТО `pickup(player, drop)`, `currency(+n)`.
- КОЛИ `timer(every)` → ЯКЩО `count(mechanic, >=, 1)` → ТО `spawn(crate)`.
- КОЛИ `in_range(jammer, enemy_weapon, n)` → ТО `stun(enemy_weapon, n)`.
- КОЛИ `tick` → ТО `speed(ship, +n)` за кожен двигун; КОЛИ `spawned(pirate_boss)` → ТО `set_state(thrusters, disabled)`.
- КОЛИ `reach(ship, destination)` → ТО `win`, `custom: «кредити = цінність уцілілого вантажу + бонус за час (два пороги)»`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `custom: «дедлайн пропущено»` (див. Непевне).
- Перемога: долетіти до мети · Поразка: див. Непевне · Рахунок: кредити за вантаж і час; зірки-репутація за пороги вантажу й часу (повна репутація — лише з бонусом за час).

## Керування і ввід
- Миша: вибір модуля з панелі → клік по гексу корпусу; поворот лазера (після апгрейда).
- Збір гайок — **наведення курсора** на уламок, без кліку: рука гравця бігає полем, поки будує.
- Зум — утримання клавіші (огляд скаржиться на незручність).

## Вікна, меню, HUD
- `game-screen`: корпус із гексів, космос навколо, панель модулів із цінами в гайках, лічильник гайок (`coins`), прогрес маршруту (`progress-bar`), таймер місії з двома порогами бонусу.
- `level-select` / `map-window`: вибір місії-контракту від корпорацій.
- `upgrade-window` між місіями: кредити → особливі здібності й бонуси модулів.
- `end-screen`: цінність доставленого вантажу, час, кредити, зірки репутації.
- `main-menu`, `settings-window`, `achievements-window` (Steam) — (?) деталі не бачив.
- Переходи: вибір місії → `game-screen` → прибуття → `end-screen` → апгрейди → вибір місії.

## Фічі поза полем
- `unlockables`: репутація (сума найкращих зірок) відкриває нові модулі; кредити купують здібності й апгрейди.
- `stars-rating` по місії + повтор пройдених місій із новими модулями, щоб пройти швидше й отримати більше (`replay`-мотив без запису).
- Steam: досягнення, хмарні збереження (`cloud-save`); 6 мов (`localization`).
- Сюжет: Бак Манн і андроїд Addam-12 беруть контракти; пірати Brown Beard і Captain Black — боси.

## Варіації й родичі
- **Space Run Galaxy** (2016): корабель починається з **містка** (знищено — корабель втрачено) і двигуна; кілька куплених корпусів різної форми; нові модулі (подвійна турель, overcharge-підсилювач зʼєднаних модулів, іонна гармата по кількох цілях, ПРО, ремонтник, плазмова гармата); напрям і час хвилі показано заздалегідь, паузи нема; онлайн-галактика: гравці створюють місії одне одному, крафт-матеріали, 3 зірки за швидкість («Lightspeed Delivery»).
- Родичі в корпусі: [cobalt-core](cobalt-core.md) (корабель як поле бою), [defense-grid](defense-grid.md) і [desktop-tower-defense](desktop-tower-defense.md) (класичні вежі на сітці), [they-are-billions](they-are-billions.md) (будівництво під тиском хвиль), [grid-forge-td](grid-forge-td.md).
- **Осі варіацій**: де стоять вежі — на шляху ворога / **на захищуваному обʼєкті** (тут); що обмежує вежу — радіус / **напрям погляду назовні** / сусідство з генератором; що захищаємо — базу / **вантаж, що займає ті самі клітини**.

## Цікавинки для курсу
- Гекс-поле корпусу з правилом «гекс перед модулем — поза корпусом» — 🥉 (сусідство гексів + орієнтація модуля).
- Живлення від сусіднього генератора (`adjacent_count` → стан `powered`) — 📎.
- Вантаж і гармати конкурують за клітини; цінність уцілілого = рахунок — 📎.
- Щит, що накриває гекси навколо й має свій запас міцності — 📎 (`coverage-area`).
- Збір дропу наведенням курсора — 🌱.
- Швидкість = кількість двигунів, дедлайн із двома порогами бонусу — 🌱.

## Мапа на каталог
- Є: `tower-placement` · `cursor-place` · `hp-damage` · `projectile-shot` · `coverage-area` (щит) · `multi-cell-size` · `orientation-state` (напрям ракетниці/лазера) · `round-currency` (гайки) · `drop-on-death` · `item-pickup` · `time-bonus` · `explode-area` (вибухівка) · `level-unlock` · `level-select` · `shop-between-levels`.
- **Нема** → пропозиції карток:
  - `+adjacency-power` «Живлення від сусіда» · entities/state · 📎 · слот {source: entity} — модуль працює/посилюється, якщо поруч джерело.
  - `+outward-facing-slot` «Розміщення лише поглядом назовні» · entities/legality · 🥉 · слот {edge: hull} — гекс перед модулем має бути поза корпусом.
  - `+cargo-occupies-cells` «Захищуваний вантаж займає клітини» · game-logic/win · 📎.
  - `+explosive-cargo`, `+thrust-speed`, `+hover-collect`, `+reputation-unlock`, `+weapon-jam`, `+disable-chain`, `+cargo-production`, `+hex-grid-render`, `+stars-rating` — дрібні, 🌱–📎.

## Пропозиції до словників
- `+cond:faces_void` — клітина в напрямку погляду сутності — поза полем/корпусом (зброя назовні; Space Run, сусідні «бортові» TD).
- `+ui:bonus-tier-timer` — таймер місії з двома позначками бонусу за час.
- `+card:adjacency-power` · `+card:outward-facing-slot` · `+card:cargo-occupies-cells` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Space Run](https://en.wikipedia.org/wiki/Space_Run) — гекс-платформа, правила розміщення, живлення, вантаж корпорацій, механік, гайки, два пороги бонусу, репутація-зірки.
- [Steam](https://store.steampowered.com/app/275670/Space_Run/) — список модулів, вороги, повтор місій.
- [Operation Rainfall, огляд](https://operationrainfall.com/?p=137250) — лазер/ракетниця/щит/глушилка/генератор, вибухівка, VIP, бос із ланцюгом, ~30 місій по ~10 хв.
- [GOG](https://www.gog.com/game/space_run) — офіційний опис.
- [GameGrin: Space Run Galaxy](https://gamegrin.com/reviews/space-run-galaxy-review) — відмінності сиквела.

## Непевне
- (?) Умова поразки в оригіналі: дедлайн «жорсткий» за оглядом, але чи це провал місії, чи лише нуль бонусу — не підтверджено; знищення корабля як поразка описане лише для Galaxy (місток).
- (?) Чи можна продавати модулі й чи є пауза в оригіналі (у Galaxy паузи нема).
- (?) Іонні гармати й ПРО — в описах, але можливо лише з Galaxy.
- (?) Кількість місій (~30) — з огляду й відгуку, не з офіційного джерела; `random: none` і `info: partial` — припущення (хвилі сценарні, заздалегідь не показані).
