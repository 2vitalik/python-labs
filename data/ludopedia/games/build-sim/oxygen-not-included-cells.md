---
title: Oxygen Not Included — клітинна фізика (гази, рідини, тепло)
slug: oxygen-not-included-cells
family: build-sim
also: [dig-gravity]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: survive
year: 2019
platforms: [PC, Mac, Linux]
links:
  - {kind: fandom, url: "https://oxygennotincluded.wiki.gg/wiki/Liquid", best: true, note: "вікі: одна рідина на клітину, шари за густиною, макс. маса на клітину, тиск, фазові переходи ±3 °C, мінімальна маса"}
  - {kind: fandom, url: "https://oxygennotincluded.wiki.gg/wiki/Gas", note: "гази: розтікання у вакуум, шари за густиною, конвекція, видалення <1 мкг"}
  - {kind: fandom, url: "https://oxygennotincluded.wiki.gg/wiki/Thermal_Conductivity", note: "формула теплообміну між клітинами (геом. середнє k, множники фаз, тік 0.2 с)"}
  - {kind: fandom, url: "https://oxygennotincluded.wiki.gg/wiki/Liquid_Airlock", note: "рідинний шлюз: форма, рідини, ризики"}
  - {kind: fandom, url: "https://oxygennotincluded.wiki.gg/wiki/Airflow_Tile", note: "плитка, що пропускає газ і тримає рідину"}
  - {kind: fandom, url: "https://oxygennotincluded.wiki.gg/wiki/Mesh_Tile", note: "плитка, що пропускає і газ, і рідину"}
  - {kind: fandom, url: "https://oxygennotincluded.wiki.gg/wiki/Vacuum", note: "вакуум: нема теплообміну, будь-який елемент його знищує"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Oxygen_Not_Included", note: "огляд гри"}
  - {kind: steam, url: "https://store.steampowered.com/app/457140/Oxygen_Not_Included/", note: "Steam: «Complex Gas and Liquid Simulations», Thermodynamics"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=oxygen+not+included+gas+liquid+physics+explained", note: "пошук; пояснення фізики"}
stage: v1
coverage: 50
mechanics: [game-loop, state-as-data, gravity-fall, cell-transform, impassable-cells, floor-types, hover-highlight, game-pause, field-scaling, +cellular-automaton-rule, +one-element-per-cell, +mass-equalize-flow, +density-layering, +liquid-overflow-up, +heat-diffusion, +phase-change-threshold, +selective-permeable-tile, +min-mass-delete, +vacuum-cell, +liquid-lock, +overlay-view, +fluid-network]
proposes: ["+trigger:tick", "+trigger:counter", "+trigger:adjacent", "+cond:cell", "+cond:same", "+cond:state", "+cond:free", "+effect:set_cell", "+effect:swap", "+effect:move", "+effect:transform", "+effect:set_value", "+effect:fall", "+role:terrain", "+role:resource", "+role:zone", "+ui:tooltip", "+ui:speed-slider", "+ui:pause-button", "+feature:speed-control", "+feature:overlays", "+axis:field=side-view", "+card:mass-equalize-flow", "+card:heat-diffusion", "+card:phase-change-threshold"]
author: opus
date: 2026-11-02
---

# Oxygen Not Included (клітинний шар) — кожна клітина: один елемент, маса й температура; світ — клітинний автомат

## Суть
Під колонією дуплікантів у ONI працює **симуляція на сітці**: кожна клітина містить рівно один елемент (тверде тіло, одну рідину, один газ або вакуум) із масою і температурою. Гази розтікаються й шаруються за густиною, рідини стікають, переповнюються вгору й тиснуть, тепло передається між сусідами, а за порогами температури елемент міняє фазу. Тут описано лише цей шар — без дуплікантів, будівель, потреб і досліджень — як приклад клітинного автомата «з фізикою».

## Поле і час
- Двовимірна квадратна сітка **збоку** (вид у розрізі астероїда): «вниз» = гравітація. Межі світу — нейтроній (непробивний); космос зверху/по краях знищує гази й рідини, що в нього потрапили (крім захищених клітин).
- Клітина = {element, mass, temperature} (+ мікроби (?)); будівлі й плитки — окремий шар поверх, частина з них займає клітину (плитка = тверде тіло).
- Real-time, тік симуляції 0.2 с (з формули теплообміну); швидкість ×1/×2/×3, пауза.
- Огляд — оверлеї: кисень, температура, рідини/гази, тиск (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина з газом | terrain | елемент, маса (г/кг), T | розтікається в сусідні клітини (у вакуум — завжди); шарується за молярною масою |
| Клітина з рідиною | terrain | елемент, маса (≤ макс. на клітину: вода 1000 кг), T | падає, тече вбік по рівній підлозі; надлишок маси піднімається в клітину вище |
| Тверда природна клітина | static | елемент, маса, T | не рухається; теплообмін із сусідами; може плавитись |
| Сипуча тверда клітина (пісок, реголіт) (?) | object | — | падає, якщо під нею порожньо (?) |
| Уламки (Debris) | pickup | маса | випадає з тиску-руйнування, замерзання рідини |
| Вакуум | static | — | нема елемента; не проводить тепло; знищується, щойно щось у нього затікає |
| Нейтроній | static | — | межа світу: непрохідний, незмінний |
| Плитка (Tile) | static | матеріал, міцність | тверда клітина від гравця; тримає тиск до межі |
| Ізольована плитка | static | k / ~16 256 | майже не проводить тепло |
| Повітропропускна плитка (Airflow Tile) | static | — | газ проходить у будь-якому напрямку, рідина — ні; витримує високий тиск рідини |
| Сітчаста плитка (Mesh Tile) | static | — | пропускає і газ, і рідину; по ній ходять |
| Двері (пневматичні тощо) | static | відкрито/закрито | закриті — тверда клітина; відкриті — пропускають (?) |
| Рідинний шлюз | zone | ≥2 рідинні клітини між стінами | рідина повністю перекриває газ між кімнатами; дупліканти проходять крізь неї (мокрі) |
| Дренажна стіна (Drywall) / темпшифт-пластина | static | — | захищає клітину від втрати газу/рідини в космос |

## Правила (КОЛИ → ЯКЩО → ТО)
- Інваріант: у клітині ≤ 1 елемент. Гази й рідини **не змішуються** в клітині — лише міняються місцями.
- КОЛИ `tick` для газової клітини → ЯКЩО сусід — вакуум → ТО `move(part_of_mass, neighbor)` (газ завжди йде у вакуум).
- КОЛИ `tick` для газової клітини → ЯКЩО сусід — той самий газ із меншою масою → ТО `custom: «перелити частину маси до вирівнювання тиску»`.
- КОЛИ `tick` ЯКЩО сусід згори — важчий газ (більша молярна маса), знизу — легший → ТО `swap(a, b)` (CO₂ осідає під кисень; H₂ спливає). Гази однакової густини (O₂ і забруднений O₂) не змішуються, а групуються окремо.
- КОЛИ `tick` для газу ЯКЩО `same(element)` і різна T → ТО `custom: «конвекція: гарячий вгору, холодний вниз»` (між різними газами — ні).
- КОЛИ `tick` для рідини ЯКЩО `free(below)` (газ/вакуум) → ТО `fall` / `swap(liquid, gas_below)` — рідина виштовхує газ.
- КОЛИ `tick` для рідини на підлозі → ТО `custom: «розтекти масу вбік до вирівнювання рівня»`; мінімальна маса для розтікання ~0.04 кг (?).
- КОЛИ `counter(mass, >, max_mass_per_cell)` ЯКЩО `free(above)` → ТО надлишок `move(…, above)`, витісняючи газ звідти; кожна нижня клітина «тисне» ≈1% маси над нею.
- КОЛИ легша рідина під важчою → ТО `swap` (шари: легша вгорі); важча рідина легшою не витісняється; рівні за густиною — не витісняють одна одну (довільно високі стовпи).
- КОЛИ тиск рідини ЯКЩО `counter(pressure, >, zmax(tile))` → ТО `custom: «руйнування плитки: природна клітина віддає 50% маси в уламки»`; стіни ≥3 клітин завтовшки не руйнуються.
- КОЛИ `tick` для пари сусідніх клітин ЯКЩО `|ΔT| >= 1 °C` → ТО `custom: «q = ΔT · 0.2 с · √(k₁k₂) · 1000 · множник фаз (тверде–газ ×25, рідина–рідина ×625)»`, обмеження: жодна клітина не змінює T більше ніж на ¼ різниці за тік; вакуум — `block`.
- КОЛИ `counter(T, >, boil_point + 3)` для рідини → ТО `transform(liquid → gas)` (вода → пара); `counter(T, <, freeze_point − 3)` → `transform(liquid → solid|debris)`; газ < точки конденсації − 3 → `transform(gas → liquid)`. Гістерезис ±3 °C не дає «миготіти».
- КОЛИ тверде тіло ЯКЩО T > точки плавлення → ТО `transform(solid → liquid)` (метал → розплав) (?).
- КОЛИ `counter(mass, <, 1 µg)` для газу або `< 10 g` для рідини поза трубами → ТО `set_cell(vacuum)` (елемент видаляється).
- КОЛИ газ/рідина в клітині, відкритій у космос, ЯКЩО `not state(cell, drywall)` → ТО `disappear_a`.
- КОЛИ газ біля airflow tile → ТО проходить; рідина — `block`. Mesh tile — `custom: «прозора для обох, тверда для ходьби»`.
- КОЛИ рідинний шлюз цілий → ТО гази з двох боків не обмінюються; ЯКЩО рідина закипіла / замерзла / викачана → шлюз зламано.
- Перемоги/поразки на цьому шарі нема: поразка гри — коли всі дупліканти загинули (задушились, замерзли, зварились).

## Керування і ввід
- Курсор: виділення області для копання (клітина стане вакуумом/газом, тверде → уламки), будування плиток/дверей/помп, демонтаж — дупліканти виконують накази (керування непряме).
- Наведення на клітину — `tooltip`: елемент, маса, температура, мікроби.
- Перемикання оверлеїв (F-клавіші (?)), пауза, швидкість ×1/×2/×3.

## Вікна, меню, HUD
- `game-screen`: поле в розрізі, панель будівель (`tool-palette`), `tooltip` клітини, панель оверлеїв, `speed-slider`/`pause-button`, ресурси колонії.
- Оверлеї (на тому ж екрані): Oxygen, Temperature (кольорова карта), Liquid/Gas pipes, Decor, Germs, Power… — головний «вид» на клітинний шар.
- `main-menu`, `pause-menu`, `settings-window`, `save-slots`, `end-screen` (колонія загинула) — загальні вікна гри.

## Фічі поза полем
- `speed-control` (×1–×3), `pause`, `autosave`/`save-slots`.
- Оверлеї як фіча візуалізації стану клітин (`+feature:overlays`).
- `seed-input` — астероїд із сіда при генерації світу (?); `mod-support` (Steam Workshop) (?).

## Варіації й родичі
- Noita (кожен піксель — матеріал, реакції), Powder Toy / falling sand (тиск, тепло, фази), Dwarf Fortress (рідини з рівнем 1–7), Terraria (рідина з рівнем у клітині), Boulder Dash (`dig-gravity`: падіння без маси).
- Осі варіацій: **що в клітині** — тип (falling sand) / тип+рівень (Terraria) / тип+маса+T (ONI); **змішування** — заборонене (ONI: обмін місцями) / дозволене (суміші); **тепло** — нема / дифузія до сусідів / з фазами й гістерезисом.

## Цікавинки для курсу
- Падіння й розтікання рідини по сітці збоку (одна рідина, рівень 0–N) — 🥉: класичний falling-sand з масою.
- Шарування за густиною через `swap` двох сусідніх газів — 📎: одне правило, ефектний результат (CO₂ осідає).
- Вирівнювання тиску: перетікання частини маси до сусідів + переповнення вгору — 🥈 (порядок оновлення, подвійний буфер).
- Дифузія тепла з геометричним середнім провідностей і обмеженням ¼ різниці — 🥈 (числова стабільність!).
- Фазові переходи з гістерезисом ±3 °C — 📎: як не дати клітині миготіти між станами.
- Плитки-фільтри (газ так / рідина ні) і рідинний шлюз як наслідок правил — 🥉.
- Повна модель ONI (тиск + тепло + фази + шари) — 👑 на рівні студентського проєкту.

## Мапа на каталог
- Є: `game-loop` (тік 0.2 с) · `state-as-data` (масиви element/mass/T) · `gravity-fall` (рідина падає) · `cell-transform` (фазові переходи) · `impassable-cells` (нейтроній, плитки) · `floor-types` (плитки з різною проникністю — частково) · `hover-highlight` (тултіп клітини) · `game-pause` · `field-scaling`.
- **Нема** → пропозиції карток:
  - `+cellular-automaton-rule` (як у Game of Life) — тут правило з масами, не з бітами.
  - `+fluid-network` (як у Factorio) — труби ONI поза цим описом.
  - `+one-element-per-cell` «Один елемент у клітині, обмін місцями замість змішування» · entities/state · 📎.
  - `+mass-equalize-flow` «Перетікання маси до вирівнювання» · entities/move · 🥈 · слоти {flow_rate, min_mass}.
  - `+density-layering` «Шари за густиною (swap)» · entities/move · 📎.
  - `+liquid-overflow-up` «Переповнення клітини вгору і тиск» · entities/move · 🥉 · слот {max_mass}.
  - `+heat-diffusion` «Теплообмін між сусідами» · entities/state · 🥈 · слоти {k_mix: min|geomean, phase_mult}.
  - `+phase-change-threshold` «Фаза за температурою з гістерезисом» · entities/state · 📎 · слот {hysteresis}.
  - `+selective-permeable-tile` «Клітина-фільтр: газ/рідина/ходьба» · entities/legality · 📎.
  - `+min-mass-delete` «Видалення елемента нижче мінімальної маси» · entities/death · 🌱.
  - `+vacuum-cell` «Вакуум: порожня клітина без теплообміну» · entities/state · 🌱.
  - `+liquid-lock` «Рідинний шлюз з правил тиску й густини» · entities/interact · 🥉.
  - `+overlay-view` «Оверлей-карта стану клітин (T, O₂)» · interface/render · 📎.

## Пропозиції до словників
- `+trigger:tick` (уся симуляція), `+trigger:counter` (маса > макс., T > поріг), `+trigger:adjacent` (пара клітин для теплообміну).
- `+cond:cell` (сусід — вакуум/газ/рідина), `+cond:same` (той самий елемент), `+cond:state` (захищена клітина), `+cond:free`.
- `+effect:set_cell`, `+effect:swap` (шари), `+effect:move` (частина маси), `+effect:transform` (фаза), `+effect:set_value` (маса/T), `+effect:fall`.
- `+role:terrain` (газова/рідинна клітина), `+role:resource` (елементи як ресурс), `+role:zone` (шлюз).
- `+ui:tooltip`, `+ui:speed-slider`, `+ui:pause-button`.
- `+feature:speed-control`; `+feature:overlays` — перемикні шари візуалізації поля (нове; кандидат і на `ui`).
- `+axis:field=side-view` — сітка в розрізі з гравітацією вниз (`square` не каже, де «низ»; спільне з `dig-gravity`).
- `+card:mass-equalize-flow`, `+card:heat-diffusion`, `+card:phase-change-threshold`.

## Джерела
- ⭐ [ONI Wiki: Liquid](https://oxygennotincluded.wiki.gg/wiki/Liquid) — одна рідина на клітину, шари, макс. маса (вода 1000 кг), тиск ≈1% маси над, zmax плиток, ±3 °C, мінімум 10 г, шлюзи.
- [ONI Wiki: Gas](https://oxygennotincluded.wiki.gg/wiki/Gas) — розтікання у вакуум, шари за молярною масою, конвекція, видалення <1 мкг, космос.
- [ONI Wiki: Thermal Conductivity](https://oxygennotincluded.wiki.gg/wiki/Thermal_Conductivity) — формула q, √(k₁k₂), множники фаз ×25/×625, обмеження ¼, ізоляція.
- [ONI Wiki: Liquid Airlock](https://oxygennotincluded.wiki.gg/wiki/Liquid_Airlock) · [Airflow Tile](https://oxygennotincluded.wiki.gg/wiki/Airflow_Tile) · [Mesh Tile](https://oxygennotincluded.wiki.gg/wiki/Mesh_Tile) · [Vacuum](https://oxygennotincluded.wiki.gg/wiki/Vacuum).
- [Wikipedia](https://en.wikipedia.org/wiki/Oxygen_Not_Included) — огляд, дифузія газів, рідини під гравітацією.
- [Steam](https://store.steampowered.com/app/457140/Oxygen_Not_Included/) — «Complex Gas and Liquid Simulations», оверлей кисню, термодинаміка.
- YouTube: пошук «oxygen not included gas liquid physics explained».

## Непевне
- (?) Точний алгоритм руху газу (яку частку маси і в якому порядку обходу клітин переливає за тік) — вікі описує ефекти, не код.
- (?) Сторінка «Pressure» на вікі не знайшлась (404): пороги overpressure будівель (напр. 1.8 кг для електролізера) — з памʼяті, тому не внесено в правила.
- (?) Чи падають сипучі тверді клітини (пісок, реголіт) — з памʼяті.
- (?) Поведінка дверей (відкриті пропускають газ/рідину, закриття видаляє малі кількості) — частково з вікі (airlock'и видаляють малі кількості рідини), решта з памʼяті.
- (?) Набір оверлеїв і гарячі клавіші, сід світу, моди — з памʼяті.
