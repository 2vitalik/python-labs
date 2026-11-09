---
title: Warp Factory
slug: warp-factory
aka: []
family: program-robots
also: [build-sim, thinky]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2021
platforms: [PC (Windows, macOS, Linux; Steam, itch)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1601860/Warp_Factory/", best: true, note: "опис: портали з поворотом і віддзеркаленням, зварювачі, поршні, сенсори, магніти, дроти; 90+ рівнів"}
  - {kind: itch, url: "https://milo.itch.io/warp-factory", note: "itch: 100+ пазлів, модинг, ключ Steam"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2519867066", note: "гайд Logic Gates: сенсори ±, дроти, поршень 1 тік, портальні гейти з нульовою затримкою, рівень Adder"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2524031399", note: "гайд Data Storage: защіпки, ROM, магніти, такти, падіння"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2562028493", note: "гайд Cross Weld: зварювання до неактивного порталу, хрест з 1×1"}
  - {kind: other, url: "https://steamcommunity.com/app/1601860/discussions/0/3202621953671766080/", note: "Portal mechanics: привиди-превʼю, колесо миші повертає портал, F віддзеркалює"}
  - {kind: other, url: "https://steamcommunity.com/app/1601860/reviews/?browsefilter=toprated", note: "огляди: «2D Infinifactory», випадкові входи, динамічні специфікації, нема гістограм"}
  - {kind: other, url: "https://gamingonlinux.com/2021/06/automation-factory-building-puzzle-game-warp-factory-is-out-now", note: "анонс виходу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=warp+factory+milo+brandt+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [teleport-pair, gravity-fall, push-object, cursor-place, level-select, sequential-levels, game-screen, +portal-rotate-reflect, +portal-through-portal, +portal-toggle-by-wire, +ghost-preview-through-portal, +weld-adjacent, +piston-extend, +sensor-signal-wire, +signal-propagation, +logic-gates, +magnet-hold, +random-test-cases, +sandbox-mode, +mod-support, +level-side-challenges]
proposes: ["+effect:reflect(a, axis)", "+effect:weld", "+effect:extend", "+effect:release", "+cond:portal_active", "+trigger:signal", "+role:portal", "+ui:portal-ghost-preview", "+card:portal-rotate-reflect", "+card:portal-through-portal", "+card:magnet-hold", "+card:level-side-challenges"]
author: opus
date: 2026-11-09
---

# Warp Factory — 2D-фабрика фігур, де портали склеюють простір із поворотом і віддзеркаленням

## Суть
Гравець будує на сітці фабрику, що збирає з блоків 1×1 потрібні фігури й візерунки, а пізніше — системи, які обробляють випадковий вхід і реагують на змінну специфікацію виходу. Інструменти — портали, зварювачі, поршні, сенсори, магніти й дроти поверх фізики з гравітацією. Головне: портал переносить обʼєкт і може його **повернути чи віддзеркалити**, портали можна вимикати сигналом і навіть проносити крізь інші портали — простір переконфігуровується. Гравці порівнюють гру з «2D Infinifactory».

## Поле і час
- Двовимірна квадратна сітка «збоку»: незакріплені блоки падають (гравітація), фабрика стоїть на місці.
- Шари: блоки-деталі (портали, поршні, сенсори, магніти), сировина (кольорові блоки 1×1, білі — вільні деталі), дроти між деталями.
- Час `programmed`: розставлена фабрика — програма; симуляція в тіках, поршень висувається чи втягується за 1 тік; ланцюг логіки триває стільки тіків, скільки найдовший шлях.
- Портальна пара склеює дві ділянки простору; обʼєкт може бути частково по обидва боки порталу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Блок сировини | object | колір (червоний, синій …), 1×1 | падає без опори; штовхається; зварюється |
| Портал (пара) | terrain | орієнтація, поворот, віддзеркалення; active/inactive | активний — переносить обʼєкт на пару з поворотом/дзеркалом; неактивний — звичайний блок |
| Зварювач | object | — | зварює сусідні блоки в одну деталь, що рухається цілою |
| Поршень | object | напрям | за сигналом висуває плече й штовхає (1 тік), втягується (1 тік) |
| Сенсор | switch | промінь, сторони + і − | бачить блок/портал/голову поршня на промені → +; промінь дійшов до кінця → − |
| Магніт | object | — | тримає сенсор чи блок, доки є сигнал; без сигналу відпускає |
| Дріт | conduit | — | несе сигнал сенсора до поршня, магніту, порталу; кілька + на одному вході = OR |
| Вхід / джерело | spawner | випадкова послідовність | подає блоки (фігури) на вхід рівня |
| Вихід / ціль | zone | специфікація фігури (буває динамічна) | приймає зібрані фігури |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `not supported(block)` → ТО `fall(block)`.
- КОЛИ `enter(object, portal)` → ЯКЩО `state(portal, active)` → ТО `teleport(object, pair)`, `rotate(object, portal_deg)`; дзеркальна пара → `custom: «віддзеркалити обʼєкт»`.
- КОЛИ `enter(portal, portal)` → ЯКЩО `state(portal, active)` → ТО `teleport(portal, pair)` — портал теж обʼєкт і проходить крізь інші портали.
- КОЛИ `custom: «сигнал на дріт порталу»` → ТО `set_state(portal, inactive)`; без сигналу — `set_state(portal, active)` (полярність — за стороною сенсора).
- КОЛИ `contact(block, portal)` → ЯКЩО `state(portal, inactive)` → ТО `block`; до активного порталу нічого не зварюється з фронтальної грані.
- КОЛИ `custom: «зварювач діє на сусідні блоки»` → ТО `attach(a, b)` — деталь рухається й падає цілою.
- КОЛИ `state_on(portal, active)` → ЯКЩО `custom: «блок приварено до грані порталу»` → ТО `custom: «зварка рветься»`, `fall(block)`.
- КОЛИ `custom: «сигнал на поршень»` → ТО `push(object)` (висування 1 тік); сигнал знято → втягування 1 тік; повторно — лише після повернення.
- КОЛИ `tick` → ЯКЩО `line_of_sight(sensor, block)` → ТО `custom: «вихід + активний»`; ЯКЩО `custom: «промінь дійшов до кінця»` → ТО `custom: «вихід − активний»`.
- КОЛИ `tick` → ЯКЩО `state(portal, active)` → ТО `custom: «промінь сенсора проходить крізь портал»`; неактивний портал зупиняє промінь (сенсор бачить сам портал).
- КОЛИ `custom: «кілька + дротів на одному вході»` → ТО `custom: «OR»`; AND/NAND/NOR/NOT — через поршень-гейт (затримка в тіках) або порталі-гейти (затримка 0).
- КОЛИ `custom: «сигнал на магніт»` → ТО `attach(magnet, object)`; сигнал знято → `custom: «відпустити»`, `fall(object)`.
- КОЛИ `tick` → ЯКЩО `custom: «настав час входу»` → ТО `spawn_at(block, input)` (випадкова послідовність).
- КОЛИ `enter(shape, output)` → ЯКЩО `same(shape, target, shape)` → ТО `counter(done, +1)`; інакше — тест провалено (?).
- КОЛИ `counter(done, >=, quota)` → ТО `win`, `unlock(next)` (?).
- Перемога: фабрика видає потрібні фігури за специфікацією · Поразка: нема (переробка) · Рахунок: опційні виклики рівня — напр. «без сенсорів», за час (?).

## Керування і ввід
- Мишею: вибір деталі з палітри, розстановка на сітці, зʼєднання дротами.
- Колесо миші — поворот деталі (порталу), **F** — віддзеркалення.
- Привиди-превʼю: фігура, що входить у портал, і як вона вийде з пари — видно до запуску.
- Запуск/пауза симуляції (?).

## Вікна, меню, HUD
- `game-screen`: сітка фабрики, палітра деталей, специфікація входу й виходу, привиди-превʼю порталів.
- `level-select`: кампанія світами (світ 2 — повороти й дзеркала; «dynamical systems» з рівнем copycat).
- Пісочниця (custom) — без цілей; гравці питають, як ставити емітери.
- `settings-window` (розмір вікна) (?).
- Переходи: level-select → game-screen → (виконано) → наступний рівень; пісочниця — окремо.

## Фічі поза полем
- Кампанія 90+ рівнів (itch: 100+): збирання фігур, сортування/фільтрація, цифрова логіка, «фокуси».
- Опційні виклики рівня: «sensorless» (без сенсорів) і на швидкість (?).
- `mod-support`: рівні спільноти через Steam Workshop — Lua-скрипти + бінарний `start_save`; редактор «для розробника» (консоль, текстові файли).
- Нема гістограм і порівняння з іншими гравцями (з оглядів).

## Варіації й родичі
- У сімʼї: `infinifactory` (3D-фабрика блоків, зварювачі, сенсори — найближчий предок), `opus-magnum`, `spacechem`, `factorio-circuit-network` (логіка на дротах).
- Портали з поворотом/дзеркалом як окрема ідея — родичі `thinky` (Patrick's Parabox — склеєний простір; Portal); у грі згадано варіант порталів «Nortals» (?).
- Осі варіацій: **портал** (лише перенос / + поворот / + віддзеркалення / вимикається сигналом / сам рухомий); **логіка** (поршень-гейт із затримкою / портальний гейт без затримки); **вхід** (фіксований / випадковий / динамічна специфікація).

## Цікавинки для курсу
- Портальна пара як афінне перетворення клітин: перенос + поворот на 90° + віддзеркалення, превʼю виходу — 🥈.
- Обʼєкт частково в порталі (склеєний простір, дві половини одного тіла) — 👑.
- Зварювання блоків у жорсткі деталі, що падають цілими, з розривом зварки при вмиканні порталу — 🥇.
- Сенсор-промінь з виходами +/−, дроти й OR, поршень-гейт із затримкою в тіках — 🥉.
- Пам'ять на фізиці: защіпки, ROM, такт — 🥈.
- Фабрика проти випадкового входу й змінної специфікації — 🥉.

## Мапа на каталог
- Є: `teleport-pair` · `gravity-fall` · `push-object` (поршні) · `cursor-place` · `level-select` · `sequential-levels` · `game-screen` · `+weld-adjacent` · `+piston-extend` · `+sensor-signal-wire` · `+signal-propagation` · `+logic-gates` · `+random-test-cases` · `+sandbox-mode` · `+mod-support` (уже в корпусі).
- **Нема** → пропозиції карток:
  - `+portal-rotate-reflect` «Портал повертає/віддзеркалює обʼєкт» · entities/interact · 🥈 · слоти {deg: 90|180|270, mirror: bool}.
  - `+portal-through-portal` «Портал — рухомий обʼєкт, проходить крізь інші портали» · entities/interact · 🥇.
  - `+portal-toggle-by-wire` «Портал вмикається/вимикається сигналом» · entities/interact · 📎.
  - `+ghost-preview-through-portal` «Превʼю обʼєкта на виході порталу» · interface/hud · 🥉.
  - `+magnet-hold` «Магніт тримає, доки є сигнал» · entities/interact · 📎.
  - `+level-side-challenges` «Опційні виклики рівня (без X, на час)» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:reflect(a, axis)` — віддзеркалити сутність/фігуру (бракує поруч із `rotate`).
- `+effect:weld` / `+effect:extend` / `+effect:release` — зварити, висунути поршень, відпустити магнітом (уже пропоновані в сімʼї; підтвердження).
- `+cond:portal_active` — портал активний (альтернатива `state(portal, active)`).
- `+trigger:signal` — на вхід деталі прийшов сигнал по дроту (уже пропонований у сімʼї).
- `+role:portal` — пара клітин, що склеює простір (дріт — уже є `conduit` у 🔥 ролей).
- `+ui:portal-ghost-preview`.
- `+card:portal-rotate-reflect`, `+card:portal-through-portal`, `+card:magnet-hold`, `+card:level-side-challenges`.

## Джерела
- ⭐ [Steam: Warp Factory](https://store.steampowered.com/app/1601860/Warp_Factory/) — Milo Brandt, 10.06.2021; портали з поворотами й віддзеркаленнями, зварювачі, поршні й сенсори, магніти, дроти; випадковий вхід; 90+ рівнів; тег Moddable.
- [itch.io](https://milo.itch.io/warp-factory) — 100+ пазлів, модинг.
- [Гайд Logic Gates](https://steamcommunity.com/sharedfiles/filedetails/?id=2519867066) — сенсори +/−, OR дротами, поршень 1 тік, затримка = найдовший ланцюг, портальні гейти без затримки, рівень Adder (8 біт, 24 тіки).
- [Гайд Data Storage](https://steamcommunity.com/sharedfiles/filedetails/?id=2524031399) — сенсор не бачить бік голови поршня, магніти й тригери, ROM блоками, падіння сенсора.
- [Гайд Cross Weld](https://steamcommunity.com/sharedfiles/filedetails/?id=2562028493) — до активного порталу не зварюється; неактивний — як блок; хрест з 5 блоків неможливий з 1×1 без цього прийому.
- [Portal mechanics](https://steamcommunity.com/app/1601860/discussions/0/3202621953671766080/) — привиди-превʼю, колесо миші й F.
- [Огляди гравців](https://steamcommunity.com/app/1601860/reviews/?browsefilter=toprated) — портали крізь портали, зварені інструменти рухаються як блоки, нема гістограм, редактор незручний.

## Непевне
- (?) Як саме працює зварювач (сусідні блоки на клітині-зварювачі чи окрема дія) — гайди говорять лише про «welded».
- (?) Умова виходу: кількість фігур / послідовність — точних чисел не бачив.
- (?) «Nortals» — ймовірно, портали з віддзеркаленням (неорієнтовані), не перевірено.
- (?) Опційні виклики «sensorless» і «under 300 seconds» — з форуму; чи це офіційні медалі рівня — не перевірено.
- (?) Три гайди Steam позначені як прибрані з Community — текст ще читався.
