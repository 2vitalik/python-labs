---
title: Frostpunk
slug: frostpunk
aka: [Фростпанк, Frostpunk: Beyond the Ice (мобільна)]
family: build-sim
also: []
klass: cursor
axes:
  field: graph
  time: realtime
  opponent: none
  info: partial
  random: runtime
  goal: survive
year: 2018
platforms: [PC, PS4, Xbox One, macOS, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Frostpunk", best: true, note: "кругова сітка навколо генератора, радіус тепла, ресурси, надія/невдоволення, закони, сценарії, Endless"}
  - {kind: steam, url: "https://store.steampowered.com/app/323190", note: "опис, режими Endless (Endurance, Builders, Serenity), 8 мап"}
  - {kind: other, url: "https://www.gamepressure.com/frostpunk/hazards/z1ad84", note: "гайд: діапазон і рівень пари генератора, обігрівачі, steam hubs, хвороби, голод"}
  - {kind: other, url: "https://www.gog.com/forum/frostpunk/steam_hub_vs_generator_range_upgrade", note: "форум: steam hub проти розширення радіуса генератора"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Frostpunk+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, drag-drop-piece, hover-highlight, multi-cell-size, coverage-area, round-currency, game-pause, save-game, save-autosave, map-window, objective-text, status-panel, mode-select, game-settings, achievements-window, +polar-grid, +heat-zones, +overload-stress, +hope-discontent, +law-book, +day-tick, +worker-assignment, +tech-tree, +influence-map]
proposes: ["+axis:polar", "+card:polar-grid", "+card:heat-zones", "+card:overload-stress", "+card:hope-discontent", "+card:law-book", "+card:worker-assignment", "+cond:heat", "+trigger:day_start", "+ui:heat-bar", "+ui:temperature-forecast", "+window:law-book", "+window:tech-tree"]
author: opus
date: 2026-11-09
---

# Frostpunk — місто кільцями навколо генератора: тепло — радіус, кожне кільце дорожче, а холод вбиває

## Суть
Гравець керує останнім містом під час вулканічної зими: ставить будівлі на **круговій (полярній) сітці** навколо вугільного генератора в кратері. Генератор гріє коло заданого радіуса; будівлі в зоні теплі, за нею — потрібні обігрівачі або steam hubs. Усе зводиться до балансу: вугілля на тепло ↔ робочі руки на видобуток ↔ надія й невдоволення людей, які регулюються законами. Програш — вибух генератора або бунт.

## Поле і час
- **Кругова сітка**: кільця навколо генератора в центрі, поділені на сектори; дороги — по кільцях і радіальних променях; будівлі прилипають до секторів. Сусідство — не квадратне (тому `field: graph`, пропоную `+axis:polar`).
- Шари: рельєф кратера (сніг, купи вугілля/деревини/сталі, які розбирають збирачі, скелі) · будівлі · поле тепла (зона генератора + зони хабів + обігрівачі) · люди на дорогах.
- Час — real-time з паузою і прискоренням; цикл доби (робота лише вдень, за замовчуванням), прогноз температури на кілька днів (?).
- Поза кратером — мапа Frostland (`map-window`) з експедиціями.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Генератор | source | рівень пари (steam), радіус (range), стрес | гріє коло радіуса; більший рівень пари — тепліше в усіх зонах, дорожче вугілля; без вугілля зупиняється; при максимумі стресу вибухає |
| Кільце тепла генератора | zone | радіус 1..N (?) | будівлі всередині отримують тепло генератора |
| Steam hub | source | рівень 1–4 | власна менша зона тепла поза генератором (+1..+4 рівні тепла, вугілля 100–400 %); ставиться на дорозі; режим «вимикати вночі» |
| Обігрівач (heater) | object | рівень технології | вмикається на окремій виробничій будівлі, гріє лише її |
| Житло: намет / барак / будинок (?) | object | ізоляція, місткість | у холодному житлі люди хворіють |
| Медпункт / лікарня | object | місткість, працівники | лікує хворих; місткість мала |
| Кухня (cookhouse) | object | працівники | сира їжа → пайки; чутлива до температури |
| Мисливська хата, збирачі, вугільна шахта, лісопилка, сталеливарня | object | працівники | виробляють вугілля, деревину, сталь, їжу |
| Склад ресурсів | container | місткість | надлишок ресурсів |
| Майстерня (workshop) | object | інженери | дослідження технологій і апгрейдів будівель |
| Маяк (beacon) | object | — | відкриває експедиції за кратер; скаути — єдиний спосіб нових людей |
| Аванпост | spawner | лінія постачання | регулярні поставки з Frostland |
| Автоматон | neutral | steamcore | повністю автоматизує частину будівель, не мерзне |
| Робітник / інженер / дитина | neutral | здоровʼя, стан | ходять на роботу; інженери — у медицину й науку; діти — працюють лише за законом |
| Купа ресурсу (вугілля, дерево, сталь) | resource | кількість | розбирається збирачами, вичерпується |
| Платформа страти (Order/Faith) | object | — | шлях до тоталітаризму (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(build, sector)` → ЯКЩО `free(sector)` and `has(city, wood|steel)` and `custom: «сектор прилягає до дороги»` → ТО `place(building)`; інакше `block`.
- КОЛИ `tick` → ЯКЩО `state(generator, on)` → ТО `take(stockpile, coal_rate(steam_level, range))` — наприклад 6 вугілля/год на рівні 1, радіусі 1 (за вікі).
- КОЛИ `counter(coal, <=, 0)` → ТО `clear_state(generator, on)` — тепла нема.
- КОЛИ `tick` → ЯКЩО `in_range(building, generator, range)` and `state(generator, on)` → ТО `custom: «+steam_level рівнів тепла до будівлі»`.
- КОЛИ `tick` → ЯКЩО `in_range(building, steam_hub, hub_range)` and `state(steam_hub, on)` → ТО `custom: «+hub_level рівнів тепла»`.
- КОЛИ `tick` → ТО `custom: «температура будівлі = зовнішня + джерела тепла + ізоляція → рівень (комфортно … лютий холод)»` (?).
- КОЛИ `input(overdrive, generator)` → ТО `custom: «+1 рівень тепла (+2 з Overdrive Couplings)»`, `custom: «стрес росте»`.
- КОЛИ `counter(generator.stress, >=, 100)` → ТО `explode(generator)`, `lose`.
- КОЛИ `tick` → ЯКЩО `custom: «житло/робота людини холодне»` and `prob(p)` → ТО `set_state(citizen, ill)`; також від трупів і нещасних випадків.
- КОЛИ `set_state(citizen, ill)` → ЯКЩО `free(medical_slot)` → ТО `heal(citizen)` з часом; інакше `custom: «стан погіршується → смерть (?)»`.
- КОЛИ `timer(day)` → ЯКЩО `not has(citizen, food)` → ТО `custom: «голод; невдоволення ↑»`.
- КОЛИ `tick` → ЯКЩО `custom: «день»` → ТО `custom: «робітники працюють»`; вночі — ні, якщо нема закону про зміни.
- КОЛИ `input(emergency_shift, building)` → ТО `custom: «продуктивність ↑ на зміну»`, `custom: «невдоволення ↑, ризик смертей (?)»`.
- КОЛИ `input(sign_law, law)` → ЯКЩО `custom: «минув кулдаун підпису»` (?) → ТО `unlock(law_effect)`, `custom: «надія / невдоволення змінюються»` (дитяча праця, 24-год зміни → ↑продуктивність, ↑невдоволення; протезування, паб → ↑надія).
- КОЛИ `input(research, tech)` → ЯКЩО `has(city, materials)` and `state(workshop, staffed)` → ТО `unlock(tech)` через час.
- КОЛИ `counter(hope, <=, low)` or `counter(discontent, >=, high)` → ЯКЩО `timer(>=, grace)` → ТО `custom: «бунт: тебе виганяють»`, `lose`.
- КОЛИ `input(expedition, location)` → ТО `custom: «скаути йдуть мапою Frostland, приносять людей/ресурси, відкривають аванпости»`.
- КОЛИ `schedule(storm)` → ТО `custom: «температура різко падає на кілька днів (Great Storm у кампанії)»`.
- КОЛИ `rng(p)` → ЯКЩО `mode(endurance)` → ТО `custom: «частини міста випадково вимикаються»`.
- КОЛИ `all_constraints_met` (сценарій: пережити бурю / дожити до дати (?)) → ТО `win`.
- Поразка: вибух генератора; бунт через надію/невдоволення. Рахунок: виживання, кількість людей, смертей.

## Керування і ввід
- Миша: меню будівель (ресурси, житло, тепло, їжа, медицина, технології) → привид будівлі тягнеться по сектору, повертається за кільцем автоматично; дороги — drag уздовж кілець/радіусів.
- Клік по будівлі: призначити/зняти робітників, вкл/викл обігрівач, апгрейд, знести.
- Генератор: кнопки рівня пари, радіуса (range), overdrive.
- Пауза, 3 швидкості (?), швидке перемикання на теплову карту.

## Вікна, меню, HUD
- `game-screen`: кратер згори + верхня смуга: ресурси, населення (робітники/інженери/діти/хворі), **шкали надії й невдоволення**, прогноз температури (`+ui:temperature-forecast`), час доби.
- Теплова карта (`+ui:heat-bar`/оверлей): кольорові зони тепла поверх міста.
- `+window:law-book` — Книга законів: дерева «Адаптація»/«Мета», потім Order або Faith.
- `+window:tech-tree` — дослідження в майстерні (тепло, видобуток, їжа, Frostland).
- `map-window` — Frostland, експедиції, аванпости.
- Вікно генератора (`custom-window`): рівень пари, радіус, overdrive, стрес-шкала.
- `main-menu`: Нова гра → `mode-select` (сценарії, Endless) · Завантажити · Налаштування · Вийти; `difficulty-select`; `pause-menu`; `end-screen` (оповідь про долю міста).
- Події-рішення громадян (`custom-window`): петиції й обіцянки з таймером (?).

## Фічі поза полем
- `mode-endless` (Endurance, Builders — без генератора на старті, Serenity — мʼякша погода) на 8 мапах; сценарії (A New Home, The Arks, The Refugees, The Fall of Winterhome) і DLC (The Rifts, The Last Autumn, On the Edge).
- `difficulty-presets`, `custom-difficulty` у Endless (?), `autosave`, `cloud-save`, `achievements`, `pause`, `speed-control`, `localization` (12 мов).

## Варіації й родичі
- Frostpunk 2 (2024) — мегаміста на гексах (?), Frostpunk 1886 (2027 (?)), мобільна Beyond the Ice.
- Родичі в корпусі: `factorio-belts` (`+coverage-area` стовпа), `oxygen-not-included-cells` (температура клітин), `caesar-3` (служби — шлях ходока, не радіус), `simcity-1989` (поля-карти).
- **Осі варіацій поля**: квадрат / гекс / полярна сітка з кільцями. **Осі «тепла»**: радіус джерела (Frostpunk) / дифузія по клітинах (ONI) / сума рівнів від кількох джерел.

## Цікавинки для курсу
- Полярна сітка: координати (кільце, сектор), кількість секторів росте з кільцем, сусідство по кільцю й радіусу — 🥈.
- Зони тепла від кількох джерел як сума рівнів + ізоляція → порогові стани — 📎.
- Генератор: рівень і радіус ↔ витрата вугілля, overdrive зі стрес-лічильником — 📎.
- Дві шкали суспільства (надія/невдоволення) і закони як незворотні модифікатори правил — 🥉.
- Призначення робітників у будівлі з денним циклом і аварійною зміною — 🥉.

## Мапа на каталог
- Є: `coverage-area` (зона тепла генератора/хаба) · `multi-cell-size` · `cell-click` + `drag-drop-piece` + `hover-highlight` · `round-currency` · `map-window` · `mode-select` · `status-panel` · `objective-text` · `save-game` + `save-autosave` · `game-pause`.
- **Нема** → пропозиції карток:
  - `+polar-grid` «Кругова сітка: кільця × сектори» · levels · 🥈 · слоти {rings, sectors_per_ring}.
  - `+heat-zones` «Зони тепла від кількох джерел» · entities/state · 📎 · слоти {radius, level}.
  - `+overload-stress` «Форсаж з лічильником стресу і вибухом» · entities/state · 📎.
  - `+hope-discontent` «Дві шкали настрою і бунт» · game-logic · 🥉.
  - `+law-book` «Закони — незворотні модифікатори» · game-logic · 🥉.
  - `+worker-assignment` «Призначення людей у будівлі» · game-logic/economy · 📎.
  - `+tech-tree` «Дерево досліджень» · levels/progression · 🥉.
  - `+day-tick`, `+influence-map` — уже пропоновані (Stardew, SimCity).

## Пропозиції до словників
- `+axis:polar` — нове значення осі `field`: кругова/полярна сітка (Frostpunk, Circle-sudoku (?)).
- `+card:polar-grid`, `+card:heat-zones`, `+card:overload-stress`, `+card:hope-discontent`, `+card:law-book`, `+card:worker-assignment` — див. вище.
- `+cond:heat` (рівень тепла клітини), `+trigger:day_start` — підтвердження наявних пропозицій.
- `+ui:heat-bar` (тут — теплова карта-оверлей), `+ui:temperature-forecast` — прогноз температури на дні вперед.
- `+window:law-book`, `+window:tech-tree`.

## Джерела
- ⭐ [Wikipedia: Frostpunk](https://en.wikipedia.org/wiki/Frostpunk) — кругова сітка, радіус тепла, overdrive-вибух, автоматони, закони, Order/Faith, сценарії, Endless, дати.
- [Steam](https://store.steampowered.com/app/323190) — режими Endless (Endurance, Builders, Serenity), 8 мап.
- [Gamepressure: Hazards](https://www.gamepressure.com/frostpunk/hazards/z1ad84) — радіус і рівень пари в панелі генератора, обігрівачі, steam hubs над дорогою, нічний режим, хвороби, голод.
- [GOG forum: steam hub vs range](https://www.gog.com/forum/frostpunk/steam_hub_vs_generator_range_upgrade) — хаби вигідніші за розширення радіуса.
- YouTube: пошук «Frostpunk gameplay».

## Непевне
- (?) 6 вугілля/год (рівень 1, радіус 1), steam hub +1..+4 і 100–400 % вугілля — з фрагментів Frostpunk Wiki у пошуку; сторінку не відкрив (402).
- (?) Назви рівнів температури, формула «зовнішня + джерела + ізоляція», кількість кілець радіуса, рівні житла (намет/барак/будинок) — з памʼяті.
- (?) Чи overdrive коштує додаткового вугілля — джерела суперечать.
- (?) Кулдаун підпису законів, петиції з таймером, кількість швидкостей, умова перемоги сценарію — з памʼяті.
- (?) Frostpunk 2 — гекси; 1886 — анонс, дата 2027 за Wikipedia.
