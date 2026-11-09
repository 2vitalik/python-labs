---
title: Civilization VI — шар районів і бонусів суміжності
slug: civ6-districts
aka: [Civ 6, Civ VI, Sid Meier's Civilization VI, Цивілізація VI]
family: build-sim
also: [board-digital]
klass: cursor
axes:
  field: hex
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2016
platforms: [PC, Mac, Linux, iOS, Android, Switch, PS4, Xbox One]
links:
  - {kind: other, url: "https://player.one/civ-6-district-cheat-sheet-tips-tricks-and-info-buildings-yields-and-adjacency-564800", best: true, note: "шпаргалка районів (версія 2016): суміжність, обмеження розміщення, будівлі кожного району"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Civilization_VI", note: "«розшарування міст» на райони-гекси, Eureka, дати і порти, доповнення Rise and Fall / Gathering Storm"}
  - {kind: other, url: "https://www.skills.lc/benchflow-ai/skillsbench/benchflow-ai-skillsbench-tasks-civ6-adjacency-optimizer-environment-skills-civ6lib-skill-md", note: "сторонній довідник оптимізатора: таблиця суміжності після патчу 2019, округлення +0.5 окремо за типом, ліміт районів за населенням"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Civilization+VI", note: "пошук"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=civ+6+district+adjacency+guide", note: "пошук; гайди суміжності"}
stage: v1
coverage: 70
mechanics: [cell-click, hover-highlight, impassable-cells, neighbor-count-clue, coverage-area, round-currency, fog-of-war, ai-opponent, save-game, minimap-radar, +adjacency-buff, +hex-adjacency-yield, +district-slots, +placement-preview-yield, +map-overlay, +cell-feature-clear]
proposes: ["+card:hex-adjacency-yield", "+card:district-slots", "+card:placement-preview-yield", "+card:cell-feature-clear", "+ui:adjacency-overlay", "+cond:adjacent_count_in", "+effect:yield"]
author: opus
date: 2026-11-09
---

# Civilization VI (райони) — місто розкладається на гекси, і кожен район рахує сусідів: +2, +1 чи +½ за тип

## Суть
Описано **лише клітинний шар районів** Civ VI. Місто не «стопка будівель у клітині», як у попередніх Civ: спеціалізовані будівлі живуть у **районах** (Campus, Holy Site, Theater Square, Commercial Hub, Harbor, Industrial Zone…), кожен займає окремий гекс у межах 3 гексів від центру. Бонус району — **сума за сусідами**: гори, ріки, ліси, чудеса, інші райони дають +2 / +1 / +½ ресурсу за хід. Гравець розвʼязує задачу розміщення: де поставити кожен район, щоб сусідство дало максимум, і як райони підсилюють одне одного кластером. Війни, дипломатія, техдерево — поза описом.

## Поле і час
- Гексова мапа (6 сусідів), процедурна генерація (`random: setup`), туман війни (`info: hidden`); бій має розкид (`random: runtime`) — тому `both`.
- Шар клітини: рельєф (рівнина, пагорб, гора — непрохідна), фіча (ліс, джунглі, болото, риф, геотермальна тріщина), ресурс (бонусний / стратегічний / розкішний), ріка — **по ребрах** гексів, покращення (шахта, кар'єр, лісопилка), чудо природи / світу, район.
- Межі міста — гекси, що належать місту; район — лише у своїх гексах і ≤3 від центру.
- Час — покроковий; бонус суміжності нараховується щоходу як прибуток ресурсу (наука, віра, культура, золото, виробництво).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Центр міста (City Center) | zone | гекс, населення | рахується як район для сусідів; дає Harbor +2 (після патчу); від нього відлік 3 гексів |
| Campus (наука) | tile | 1 на місто | +1 за кожну сусідню гору, +1 за 2 джунглі, +1 за 2 райони (2016); пізніше +2 риф/тріщина, +½ джунглі/район |
| Holy Site (віра) | tile | 1 на місто | +2 за чудо природи, +1 за гору, +1 за 2 ліси, +1 за 2 райони |
| Theater Square (культура) | tile | 1 на місто | +1 за чудо світу, +1 за 2 райони (2016); пізніше +2 за чудо і за Entertainment Complex / Water Park |
| Commercial Hub (золото) | tile | 1 на місто | +2, якщо на ріці (бінарно); +2 за сусідній Harbor; +1 за 2 райони |
| Harbor (золото) | tile | на воді біля суші | +1 за прибережний ресурс, +1 за 2 райони; після патчу +2 за центр міста |
| Industrial Zone (виробництво) | tile | 1 на місто | +1 за шахту/кар'єр, +1 за 2 райони (2016); пізніше +2 Aqueduct/Dam/Canal, +1 кар'єр/стратегічний, +½ шахта/лісопилка |
| Encampment, Preserve | tile | не поруч з центром | суміжності не мають; Encampment обороняє (його треба взяти до штурму центру) |
| Entertainment Complex, Water Park, Aerodrome, Spaceport, Government Plaza | tile | — | власної суміжності не мають; Plaza дає +1 сусіднім спеціалізованим |
| Aqueduct | tile | біля центру і прісної води | неспеціалізований; +житло; рахується як район для сусідів |
| Dam / Canal | tile | Dam — заплава, ріка ≥2 ребра | неспеціалізовані; дають Industrial Zone +2 (після патчу) |
| Neighborhood | tile | кілька на місто | житло за привабливістю (Appeal) гекса: +2…+6 |
| Гора, ріка, ліс, джунглі, риф, тріщина | terrain | — | джерела суміжності; ліс/джунглі/болото **знищуються**, коли на гекс ставлять район |
| Чудо природи | static | — | не можна будувати; +2 Holy Site поруч |
| Шахта, кар'єр, лісопилка | terrain | покращення | джерела суміжності Industrial Zone |
| Будівлі району (Library → University → Research Lab тощо) | object | ланцюг, утримання | +ресурс і слоти спеціалістів; Zoo/Stadium/Factory/Power Plant — ефект на міста в 6 гексах |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place_district, hex)` → ЯКЩО `in_range(hex, city_center, 3)` and `custom: «гекс належить місту»` and `not cell(hex, mountain)` and `not cell(hex, natural_wonder)` and `not cell(hex, luxury|strategic)` and `free(hex)` → ТО `place(district)`; інакше `block`.
- КОЛИ `place(district)` → ЯКЩО `cell(hex, woods|rainforest|marsh)` or `cell(hex, bonus_resource)` → ТО `set_cell(hex, plain)` (фіча/ресурс зникає).
- КОЛИ `input(place_district, hex)` → ЯКЩО `count(specialty_districts, >=, 1 + floor((pop − 1) / 3))` → ТО `block`; неспеціалізовані (Aqueduct, Neighborhood, Canal, Dam, Spaceport) ліміту не мають.
- КОЛИ `input(place_district, hex)` → ЯКЩО `count(same_district_in_city, >=, 1)` → ТО `block` (спеціалізовані — по одному на місто; Government Plaza, Diplomatic Quarter — по одному на цивілізацію).
- КОЛИ `input(place_harbor, hex)` → ЯКЩО `not cell(hex, coast|lake)` or `custom: «нема сусідньої суші»` → ТО `block`.
- КОЛИ `input(place_encampment|preserve, hex)` → ЯКЩО `custom: «сусідній гекс — центр міста»` → ТО `block`.
- КОЛИ `input(place_aqueduct, hex)` → ЯКЩО `custom: «сусіднього центру міста нема»` or `custom: «нема сусідньої прісної води: гора, ріка, озеро, оаза»` → ТО `block`.
- КОЛИ `turn_start(player)` → ЯКЩО `adjacent_count(campus, mountain, >=, 1)` → ТО `custom: «наука += 1 за кожну гору»`.
- КОЛИ `turn_start(player)` → ЯКЩО `cell(commercial_hub, river)` → ТО `currency(+2)` (бінарний бонус: ріка по будь-якому ребру).
- КОЛИ `turn_start(player)` → ТО `custom: «бонус району = Σ_тип floor(кількість_сусідів_типу × вага_типу); ваги +2 / +1 / +0.5; кожен тип з +0.5 округлюється вниз окремо, потім сума (після патчу 2019)»`.
- КОЛИ `turn_start(player)` → ЯКЩО `adjacent_count(district, any_district, >=, 2)` → ТО `custom: «+1 за кожні 2 сусідні райони»` (центр міста, Aqueduct, Dam теж рахуються).
- КОЛИ `turn_start(player)` → ЯКЩО `adjacent_count(specialty_district, government_plaza, >=, 1)` → ТО `custom: «+1 бонусу суміжності»`.
- КОЛИ `turn_start(player)` → ЯКЩО `mode(civ = Japan)` → ТО `custom: «райони дають сусідам +1 замість +0.5» (Meiji Restoration)`.
- КОЛИ `turn_start(player)` → ЯКЩО `in_range(city_center, stadium|zoo|power_plant, 6)` → ТО `custom: «регіональний ефект будівлі на всі міста в радіусі»`.
- КОЛИ `input(build, district_building)` → ЯКЩО `has(district, prev_building)` → ТО `place(building)` (Library → University → Research Lab).
- КОЛИ `contact(enemy_unit, district)` → ТО `custom: «пограбування (pillage): район вимкнено до ремонту»` (?).
- Перемоги/поразки на цьому шарі нема; «рахунок» шару — прибуток ресурсів за хід і швидкість до науки/культури/релігії.

## Керування і ввід
- Обрати місто → панель виробництва → вкладка районів → клік по району: поле підсвічує **допустимі гекси**, над кожним — іконки бонусу, який район тут отримає, і стрілки від джерел суміжності.
- Клік по гексу — почати будівництво (кілька ходів) або купити за золото/віру (?).
- Купівля гекса за золото — розширити межі під район (?).
- Hover над районом — розклад бонусу за джерелами.

## Вікна, меню, HUD
- `game-screen`: гексова мапа + верхня смуга ресурсів (наука, культура, віра, золото) + `minimap` з лінзами + панель міста.
- `custom-window` міста: виробництво (будівлі, райони, юніти, чудеса), громадяни, межі.
- Лінзи мапи (`+ui:map-overlay`): поселенець, релігія, привабливість (Appeal), райони; `+ui:adjacency-overlay` — бонус на кожному гексі під час розміщення.
- `codex-window` — Civilopedia (довідник районів, будівель, правил).
- `main-menu`: Single Player (New Game / Load / Scenarios) · Multiplayer · Options · Mods · Exit; `match-setup` (цивілізація, мапа, розмір, швидкість, складність); `pause-menu`.
- Переходи: місто → панель виробництва → режим розміщення району → поле з підсвіткою.

## Фічі поза полем
- `ai-opponent-levels`, `online-multiplayer`, `hotseat` (?), `save-slots`, `autosave`, `mod-support`, `seed-input` (?), `difficulty-presets`.
- Доповнення: Rise and Fall (2018), Gathering Storm (2019) — нові райони (Dam, Canal, Government Plaza (?), Preserve), стихійні лиха.
- Патчі змінили ваги суміжності (2019): одна гра — дві редакції правил, гарний приклад «версіонування балансу».

## Варіації й родичі
- Унікальні райони цивілізацій замінюють базові з іншими правилами (Hansa замість Industrial Zone, Lavra замість Holy Site тощо (?)).
- Родичі в корпусі: `luck-be-a-landlord` і `backpack-hero` (`+adjacency-buff` — бонус за сусідство), `dorfromantik` (гекси й збіг ребер), `townscaper` (контекстна форма), `big-pharma`.
- Настільні: Tiny Towns, Suburbia, Isle of Skye — очки за сусідство.
- **Осі варіацій суміжності**: квадрат 4/8 / гекс 6 · ваги за тип (+2/+1/+½) / прапорець (ріка — бінарно) · дробові частки з округленням (разом / за типом окремо) · симетрична (район A дає B і B дає A) / одностороння (Harbor → Commercial Hub +2, назад ні) · локальна (сусіди) / регіональна (6 гексів).

## Цікавинки для курсу
- Гексова суміжність (6 сусідів, осьові координати) і підрахунок сусідів за типом — 📎.
- Бонус = Σ floor(count × weight) з окремим округленням за типом — 🥉 (тонке місце: floor(½+½+½)≠Σfloor).
- Превʼю бонусу на всіх допустимих гексах перед розміщенням — 🥉.
- Оптимізатор розміщення кількох районів (райони підсилюють один одного) — 🥇 (комбінаторний пошук / жадібний + локальний).
- Ліміт районів від населення `1 + floor((pop−1)/3)` — 🌱.
- Ріка по ребрах гексів (атрибут ребра, не клітини) — 🥉.

## Мапа на каталог
- Є: `neighbor-count-clue` (рахунок сусідів типу — та сама арифметика, тут для прибутку) · `coverage-area` (регіональні 6 гексів) · `impassable-cells` (гори, чудеса) · `cell-click` + `hover-highlight` · `round-currency` · `fog-of-war` · `ai-opponent` · `minimap-radar` · `save-game`.
- **Нема** → пропозиції карток:
  - `+hex-adjacency-yield` «Прибуток клітини за сусідами з вагами» · game-logic/economy · 🥉 · слоти {weights, rounding} — Civ VI, Tiny Towns.
  - `+district-slots` «Ліміт спеціалізованих клітин від розміру міста» · game-logic · 🌱 · слот {formula}.
  - `+placement-preview-yield` «Підсвітка допустимих клітин з прогнозом бонусу» · interface/hud · 🥉.
  - `+cell-feature-clear` «Будова знищує фічу клітини» · entities/state · 🌱.
  - `+adjacency-buff`, `+map-overlay` — уже пропоновані (Backpack Hero, SimCity).

## Пропозиції до словників
- `+card:hex-adjacency-yield`, `+card:district-slots`, `+card:placement-preview-yield`, `+card:cell-feature-clear` — див. вище.
- `+ui:adjacency-overlay` — іконки бонусу над гексами в режимі розміщення (уже пропонувалось у корпусі — підтвердження).
- `+cond:adjacent_count_in` — підрахунок сусідів із множини типів (Mine **або** Quarry) — підтвердження наявної пропозиції.
- `+effect:yield` — прибуток ресурсу за хід із клітини (наука/віра/золото), не одноразовий `currency`.

## Джерела
- ⭐ [player.one: Civ 6 District Cheat Sheet](https://player.one/civ-6-district-cheat-sheet-tips-tricks-and-info-buildings-yields-and-adjacency-564800) — суміжність і будівлі всіх районів (версія релізу).
- [civ6lib (skills.lc)](https://www.skills.lc/benchflow-ai/skillsbench/benchflow-ai-skillsbench-tasks-civ6-adjacency-optimizer-environment-skills-civ6lib-skill-md) — таблиця після патчу 2019, окреме округлення, ліміт за населенням, обмеження розміщення.
- [Wikipedia: Civilization VI](https://en.wikipedia.org/wiki/Civilization_VI) — розшарування міст, Campus поруч з горами/джунглями, Encampment не біля центру, дати.
- YouTube: пошук «civ 6 district adjacency guide».
- Мертві для мене: civilization.fandom.com (402), pcgamesn (403) — у шапку не клав.

## Непевне
- (?) Дві редакції ваг: реліз 2016 (player.one: «+1 за 2 райони») і патч 2019 (civ6lib: «+0.5 за район», +2 риф/тріщина, Harbor +2 центр) — civ6lib сторонній, не офіційний; які саме ваги в актуальній версії — перевірити в Civilopedia.
- (?) Неспеціалізованими у формулі ліміту названо й Spaceport — дивно, але так у джерелі.
- (?) Pillage, купівля гексів/районів, ціна району (зростає з прогресом (?)), hotseat, seed — з памʼяті.
- (?) Hansa/Lavra як приклади унікальних районів — з памʼяті.
