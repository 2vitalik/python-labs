---
title: Fallout Shelter
slug: fallout-shelter
aka: [Фоллаут Шелтер]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: survive
year: 2015
platforms: [iOS, Android, PC, Xbox One, PS4, Switch]
links:
  - {kind: fandom, url: "https://fallout.wiki/wiki/Fallout_Shelter_rooms", best: true, note: "усі кімнати: SPECIAL, ресурс, поріг населення, ціни, розмір 3–9, злиття до 3, формули місткості й виробництва, rush"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Fallout_Shelter", note: "ядро: сховище, мешканці, SPECIAL, ресурси, народжуваність, пустка, ланчбокси, оновлення (survival, крафт, квести), платформи"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Fallout+Shelter", note: "пошук"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Fallout+Shelter+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [cell-click, drag-drop-piece, multi-cell-size, tile-merge, impassable-cells, round-currency, in-round-upgrades, unit-xp-skills, inventory, inventory-items, hp-damage, spawn-random-cell, spawner-entity, enemy-waves, level-unlock, save-game, save-multi-slot, status-panel, objective-text, achievements-window, +room-merge, +rush-gamble, +stat-pool-production, +incident-spread, +worker-assignment, +cost-scaling, +loot-box, +vertical-stack]
proposes: ["+card:room-merge", "+card:rush-gamble", "+card:stat-pool-production", "+card:incident-spread", "+card:cost-scaling", "+card:loot-box", "+trigger:incident", "+cond:stat_sum", "+cond:adjacent_same_level", "+ui:resource-gauges", "+window:floor-select"]
author: opus
date: 2026-11-09
---

# Fallout Shelter — сховище в скелі: однакові кімнати-сусіди зливаються до потрійних, а виробництво — це пул SPECIAL робітників

## Суть
Гравець — Наглядач підземного сховища: вирізає в скелі кімнати на сітці поверхів, з'єднує ліфтами і перетягує мешканців на роботу. Кімнати виробляють енергію, їжу, воду; **дві-три однакові кімнати поруч зливаються** в одну ширшу з більшою місткістю й дешевшим апгрейдом. Швидкість кімнати = сума потрібної характеристики SPECIAL її працівників; можна «поквапити» (rush) — азарт з ризиком інциденту. Інциденти (пожежа, таргани, кротощури) поширюються в сусідні кімнати.

## Поле і час
- Вид збоку: **25 поверхів**, на кожному місце для 8 кімнат (?) або ліфтів; одиниця ширини — «клітинка» (кімната 3, подвійна 6, потрійна 9, ліфт 1, двері сховища 6).
- Шари: скеля (непрохідна до розкопки) · кімнати · мешканці всередині (ходять, сидять за станками) · інциденти поверх кімнат.
- Час — real-time, гра йде й у фоні (таймери виробництва, походи пустищею); мобільний free-to-play ритм «зайди — збери».
- Камера — прокрутка й зум сховища.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Скеля | static | — | місце під майбутні кімнати |
| Двері сховища | gate | ширина 6, рівень | перша лінія оборони від рейдерів |
| Ліфт | terrain | ширина 1, ≤2 на поверх (більше — втрата місця) | зʼєднує поверхи; мешканці переходять ним |
| Виробнича кімната (Power Generator, Diner, Water Treatment, Nuclear Reactor, Garden, Water Purification, Nuka-Cola Bottler, Medbay, Science Lab, Radio Studio) | object | тип, SPECIAL, рівень 1–3, розмір 3/6/9 | накопичує пул з SPECIAL працівників; повний пул → партія ресурсу |
| Житлова кімната (Living Room) | object | Charisma, розмір, рівень | додає місткість сховища `2·S/3·(L+4)−2`; тут пари заводять дітей |
| Склад (Storage Room) | container | Endurance, розмір, рівень | місткість речей `5·S·(L+1)` |
| Тренувальна кімната (Weight Room, Athletics, Armory, Classroom, Fitness, Lounge, Game Room) | object | одна з SPECIAL | піднімає характеристику мешканця, не рівень |
| Майстерні (Weapon, Outfit, Theme) | object | ширина 9 | крафт з хламу |
| Overseer's Office, Barbershop | object | ширина 6 | квести; зовнішність |
| Мешканець (dweller) | ally | SPECIAL ×7, рівень, HP, щастя, спорядження | працює в кімнаті; б'ється з інцидентом у своїй кімнаті; може піти в пустку |
| Інцидент: пожежа, радтаргани, кротощури | hazard | сила ↑ з рівнем і розміром кімнати | шкодить мешканцям у кімнаті; якщо не загашено — переходить у сусідню |
| Рейдери, смертокігті та ін. | enemy | HP | атакують через двері, рухаються кімнатами; рейдери крадуть кришки |
| Mister Handy | ally | — | робот-помічник, лише з ланчбоксів |
| Ланчбокс | container | картки | предмети, ресурси, мешканці |
| Ресурси: енергія, їжа, вода, кришки (caps), стімпаки, RadAway | resource | ліміт сховищем | споживаються мешканцями / витрачаються на будову |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(build, room_type, slot)` → ЯКЩО `free(slot_width)` and `custom: «прилягає до ліфта або кімнати»` (?) and `counter(population, >=, unlock_pop)` and `has(vault, caps >= base + incr × count_of_type)` → ТО `place(room)`, `currency(-cost)`.
- КОЛИ `place(room)` → ЯКЩО `adjacent_count(room, same_type, >=, 1)` and `custom: «сусід — того ж рівня»` and `custom: «у групі < 3 кімнат»` → ТО `merge(room, neighbor → wider_room)`.
- КОЛИ `input(upgrade, room)` → ЯКЩО `custom: «сусід того ж типу вже на новому рівні»` → ТО `merge(room, neighbor → wider_room)` — злиття після вирівнювання рівнів.
- КОЛИ `input(upgrade, room)` → ЯКЩО `has(vault, caps >= upgrade_cost)` → ТО `set_value(room.level, +1)`; злиту кімнату апгрейдити дешевше, ніж окремі.
- КОЛИ `input(drag_dweller, room)` → ЯКЩО `count(dwellers_in_room, <, 2 × width_units)` → ТО `move(dweller, room)`; 2 на одиничну, до 6 на потрійну.
- КОЛИ `tick` → ТО `counter(room.pool, +Σ SPECIAL_працівників)` — щосекунди кожен додає свою характеристику.
- КОЛИ `counter(room.pool, >=, room.pool_max)` → ТО `custom: «партія ресурсу готова — значок над кімнатою»` (наприклад пул одиничного генератора 1320 ≈ 22 хв).
- КОЛИ `input(tap, room_ready)` → ТО `give(vault, resource)`, `counter(room.pool, 0)`, `custom: «досвід працівникам»`.
- КОЛИ `input(rush, room)` → ЯКЩО `prob(1 − fail(Luck, SPECIAL, room.penalty))` → ТО `give(vault, resource)`, `currency(+caps)`, `custom: «щастя +10»`; інакше `spawn_at(incident, room)`, `custom: «щастя −10»`.
- КОЛИ `input(rush, room)` → ТО `custom: «штраф кімнати ↑; спадає з часом»` (кожен rush ризикованіший).
- КОЛИ `rng(p)` → ЯКЩО `custom: «кімната порожня»` → ТО `spawn_at(infestation, room)` — порожні кімнати вразливі.
- КОЛИ `tick` → ЯКЩО `state(room, incident)` and `custom: «мешканці кімнати перемагають»` → ТО `clear_state(room, incident)`, `custom: «досвід/кришки»`.
- КОЛИ `timer(spread)` → ЯКЩО `state(room, incident)` → ТО `custom: «інцидент переходить у сусідню кімнату»`.
- КОЛИ `contact(enemy, dweller)` → ТО `damage(n)`; КОЛИ `hp_zero(dweller)` → ТО `custom: «загинув — воскресити за кришки»` (?).
- КОЛИ `tick` → ЯКЩО `counter(power, <=, 0)` → ТО `custom: «кімнати вимикаються (дальші — першими (?))»`.
- КОЛИ `tick` → ЯКЩО `counter(food, <=, 0)` → ТО `custom: «мешканці втрачають HP»` (?); `counter(water, <=, 0)` → `custom: «радіація»` (?).
- КОЛИ `contact(male, female)` → ЯКЩО `cell(room, living_room)` and `custom: «досить Charisma й місця»` (?) → ТО `spawn(child)` через час.
- КОЛИ `schedule(raid)` or `rng(p)` → ТО `spawn_at(raiders, vault_door)`; рейдери крадуть кришки й ресурси.
- КОЛИ `input(send_to_wasteland, dweller)` → ТО `custom: «похід у пустку: збирає хлам/зброю, ризикує HP; повернення — час»`.
- КОЛИ `counter(population, >=, unlock_pop)` → ТО `unlock(room_type)` (Storage 12, Medbay 14, Science 16 … Nuka-Cola 100).
- Мети нема; рахунок — населення (макс. 200), щастя, квести. У режимі Survival смерть остаточна (?).

## Керування і ввід
- Тач/миша: кнопка «будувати» → вибір кімнати → підсвічені допустимі місця → тап.
- Drag мешканця з кімнати в кімнату; drag на двері — у пустку.
- Тап по готовому значку ресурсу — зібрати; тап по кімнаті — апгрейд, rush, знести (?).
- Зум/прокрутка сховища; тап по мешканцю — картка з SPECIAL, спорядженням.

## Вікна, меню, HUD
- `game-screen`: розріз сховища + верхня смуга (`+ui:resource-gauges` енергії/їжі/води, населення, кришки, щастя) + кнопки будування, складу, мешканців, ланчбоксів.
- `custom-window` мешканця: SPECIAL, рівень, HP, спорядження, щастя.
- `inventory-window` — склад предметів і хламу; `custom-window` крафту в майстернях.
- `custom-window` списку мешканців з сортуванням (за SPECIAL, рівнем, щастям).
- `map-window` пустки — походи й квести; `custom-window` Overseer's Office — список квестів.
- `shop-window` — ланчбокси, Mister Handy; `achievements-window`/цілі — щоденні й постійні цілі (`objective-text`).
- `save-slots` — кілька сховищ; `settings-window`.
- Переходи: сховище → тап по кімнаті → дії; кнопка будування → режим розміщення.

## Фічі поза полем
- `save-slots` (кілька сховищ), `cloud-save` (з 1.2), `mode-hardcore` (Survival mode з 1.2 (?)), `achievements`, `objective-text` (цілі за ланчбокси).
- Монетизація: ланчбокси за реальні гроші (`+loot-box`); free-to-play без обов'язкових платежів.
- Оновлення: улюбленці і виселення (1.3), крафт і нові кімнати (1.4), квести (1.6).

## Варіації й родичі
- Родичі в корпусі: `prison-architect-rooms` (кімнати з вимогами), `oxygen-not-included-cells` (колонія в скелі, вид збоку), `backpack-hero` (бонус за сусідство), `caesar-3` (кількісні пороги розвитку).
- Схожі: Tiny Tower (поверхи-магазини), Sheltered, XCOM-база (вид збоку).
- **Осі варіацій злиття**: однакові сусіди зливаються одразу / після вирівнювання рівнів · ліміт ширини (3) / без ліміту · зливання дає більше місць + знижку апгрейду.
- Осі «виробництво»: таймер / пул із суми навичок працівників / ризиковий прискорювач.

## Цікавинки для курсу
- Злиття однакових сусідніх кімнат до ширини 3 з умовою «той самий рівень» — 📎.
- Пул виробництва як сума характеристик працівників за секунду — 🌱.
- Rush: ймовірність провалу росте з кожною спробою і спадає з часом — 📎.
- Інцидент, що поширюється в сусідню кімнату, якщо не подолано, і сила росте з розміром кімнати — 🥉.
- Ціна наступної кімнати = база + приріст × кількість таких — 🌱.
- Ліфти-граф і рух мешканців між поверхами (пошук шляху) — 🥉.

## Мапа на каталог
- Є: `tile-merge` (злиття однакових кімнат) · `multi-cell-size` (ширина 3/6/9) · `drag-drop-piece` (мешканці) · `cell-click` · `impassable-cells` (скеля) · `round-currency` (кришки) · `in-round-upgrades` (рівні кімнат) · `unit-xp-skills` (рівень і SPECIAL мешканця) · `inventory` + `inventory-items` · `hp-damage` · `spawn-random-cell` (інциденти) · `spawner-entity` · `enemy-waves` (рейди) · `level-unlock` (кімнати за населенням) · `save-multi-slot` · `status-panel` · `objective-text` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+room-merge` «Сусідні однакові кімнати зливаються до N» · entities/legality · 📎 · слоти {max_width, same_level}.
  - `+rush-gamble` «Прискорення з ризиком і зростаючим штрафом» · game-logic · 📎.
  - `+stat-pool-production` «Виробництво = пул суми навичок працівників» · game-logic/economy · 🌱.
  - `+incident-spread` «Лихо переходить у сусідню кімнату» · entities/state · 🥉.
  - `+cost-scaling` «Ціна росте з кількістю таких самих» · game-logic/economy · 🌱.
  - `+loot-box` «Скринька з випадковими картками» · game-logic/economy · 📎.
  - `+worker-assignment`, `+vertical-stack` — уже пропоновані (див. `frostpunk`, корпус).

## Пропозиції до словників
- `+card:room-merge`, `+card:rush-gamble`, `+card:stat-pool-production`, `+card:incident-spread`, `+card:cost-scaling`, `+card:loot-box` — див. вище.
- `+trigger:incident` — подія-лихо в кімнаті (пожежа, нашестя) як тригер ланцюга.
- `+cond:stat_sum` — сума характеристики сутностей у зоні ≥ N; `+cond:adjacent_same_level` — підтвердження наявної пропозиції.
- `+ui:resource-gauges` — кілька шкал ресурсів із позначкою «бракує» (енергія/їжа/вода).
- `+window:floor-select` — підтвердження (тут — прокрутка поверхів).

## Джерела
- ⭐ [Fallout Wiki: Fallout Shelter rooms](https://fallout.wiki/wiki/Fallout_Shelter_rooms) — таблиця кімнат (SPECIAL, поріг населення, ціни, розмір 3–9), 25 поверхів, ≤2 ліфти на поверх, злиття до 3, 2/6 мешканців, макс. 200, формули, пул 1320, rush ±10 щастя, інциденти.
- [Wikipedia: Fallout Shelter](https://en.wikipedia.org/wiki/Fallout_Shelter) — ядро, SPECIAL, народжуваність, пустка, ланчбокси, Mister Handy, оновлення 1.2–1.6, дати.
- YouTube: пошук «Fallout Shelter gameplay».

## Непевне
- (?) «8 кімнат на поверх» — дослівно з вікі, але з шириною 3 і ліфтами 1 це радше 8 одиничних слотів на поверх; точна ширина поверху (≈26 одиниць) не перевірена.
- (?) Розкопка скелі, правило «прилягає до ліфта/кімнати», знесення — з памʼяті.
- (?) Наслідки нестачі: енергія — вимикання кімнат (дальніх від генераторів), їжа — HP, вода — радіація — з памʼяті.
- (?) Умови народження дітей, воскресіння за кришки, Survival як hardcore — з памʼяті.
- (?) Формула виходу генератора на вікі зіпсована — не наводжу.
