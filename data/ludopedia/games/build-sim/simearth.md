---
title: SimEarth (сітковий шар і Daisyworld)
slug: simearth
aka: [SimEarth, "SimEarth: The Living Planet", Daisyworld]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: both
  goal: none
year: 1990
platforms: [Mac, DOS, Windows, Amiga, SNES, FM Towns, PC-98, X68000, TurboGrafx CD, Mega-CD]
links:
  - {kind: other, url: "https://archive.org/details/Mac_SimEarth_manual", best: true, note: "повний мануал Maxis: Edit Window (інструменти й ціни), шари даних, події, біоми, класи життя, енергія, шкали часу, розділ Daisyworld"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/SimEarth", note: "огляд: сценарії, Daisy World, Gaia і Лавлок, цивілізації, exodus, катастрофи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=SimEarth+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [cell-click, cursor-place, hover-highlight, cell-transform, round-currency, rule-variants, difficulty-levels, difficulty-select, map-window, minimap-radar, field-scaling, game-pause, save-game, help-window, tutorial-window, sound-effects, background-music, music-toggle, game-loop, +overlay-view, +biome-climate-table, +albedo-feedback, +species-competition, +evolution-tree, +terraformer-emitter, +time-scale-shift, +global-parameter-sliders, +plate-drift, +disasters, +biome-terraform, +data-sonification]
proposes: ["+card:biome-climate-table", "+card:albedo-feedback", "+card:species-competition", "+card:evolution-tree", "+card:terraformer-emitter", "+card:time-scale-shift", "+card:global-parameter-sliders", "+card:plate-drift", "+card:data-sonification", "+effect:raise", "+ui:map-overlay", "+ui:layer-toggle", "+window:model-control-panel", "+window:graphs-window"]
author: opus
date: 2026-11-09
---

# SimEarth (сітковий шар і Daisyworld) — планета як сітка клітин-масивів: клімат вибирає біом, біом годує життя, а ромашки самі тримають температуру

## Суть
Will Wright і Fred Haslam (Maxis, 1990) зробили «пісочницю планети» за гіпотезою Гаї Джеймса Лавлока: від остигання кори до розумного виду й відльоту цивілізації (exodus). Гравець не керує істотами — він за енергію змінює висоту клітин, садить біоми, підселяє життя, викликає події й крутить глобальні повзунки моделі. Тут описано **сітковий шар**: клітина з кількома масивами даних, правила вибору біому, конкуренція за клітину, і сценарій **Daisyworld**, де вісім відтінків ромашок через альбедо регулюють температуру планети. Решта (атмосферна хімія, енергетика цивілізацій) — коротко.

## Поле і час
- Карта планети — прямокутна сітка клітин у пласкій проєкції (у Map Window ще й сферична). Edit Window показує збільшений фрагмент; опція «Compress edit screen» — кожна друга клітина, вчетверо більша площа.
- Кожна клітина — набір масивів: Altitude (32 рівні, крок 500 м, рівень моря змінний), Air Temperature, Rainfall, Sea Temperature, Biome, Life, Humans; плюс напрям магми, вітри, морські течії, подія.
- Біом і життя («ніша») можуть стояти в одній клітині; місто — окремий шар.
- Час — цикли симуляції. Шкали: Geologic (1 цикл = 10 млн років), Evolution, Civilization, Technology; планета живе 10 млрд років. Швидкість: Fast / Moderate (~75 %) / Slow (~25 %) / Pause — на паузі інструменти працюють.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина планети | terrain | висота, температура повітря, опади, температура моря, біом, життя, місто, магма | масиви перераховуються моделями щоциклу |
| Глибоке море / океан / шельф | terrain | глибина: > 2500 м / 1000–2500 м / мілко | у морі й океані зароджується життя; без шельфів морське життя не еволюціонує |
| Біом ×7 + Rock | terrain | Arctic, Boreal Forest, Desert, Temperate Grasslands, Forest, Jungle, Swamp | обирається за температурою × опадами (+ висота, CO2); потребує CO2 й опадів |
| Ромашка ×8 відтінків (Daisyworld) | terrain | відтінок білий → чорний = альбедо | замість біомів; темні гріють себе й планету, світлі охолоджують |
| Життя: 15 класів × 16 видів | neutral | клас, вид, IQ, середовище (4 оцінки щастя) | розселяється, конкурує за клітину, просувається у виді й мутує в новий клас |
| Карниферни | neutral | — | мобільні хижі рослини; лише з еволюції, поставити не можна |
| Місто ×7 епох | spawner | густина 3 рівні (Nanotech — 4), «мандрівне населення» | росте; мандрівне населення = торгівля й рух між містами |
| Тераформер ×5 | spawner | Biome Factory, Oxygenator, N2 Generator, Vaporator, CO2 Generator | працює постійно після встановлення; зупинити — лише метеором, вогнем, вулканом |
| Моноліт | object | 2500 E.U. | 1/3 шансу, що життя мутує на клас вище → наступна шкала часу |
| Крижаний метеор | projectile | 500 E.U. | додає воду сухій планеті |
| Подія ×11 | hazard | 8 викликаються за 50 E.U. | ураган, цунамі, метеор, вулкан, атомний тест, пожежа, землетрус, чума; лише сама — війна, забруднення, exodus |
| Потік магми | zone | напрям | рухає плити (дрейф континентів); на стику різних напрямів — землетруси |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `custom: «біом клітини = таблиця (температура < 0 / 0–25 / > 25 °C) × (опади < 30 / 30–90 / > 90 см/рік)»`: холодно — Arctic / Boreal / Boreal; помірно — Desert / Grasslands / Forest; жарко — Desert / Swamp / Jungle.
- КОЛИ `input(plant_biome, cell)` → ТО `set_cell(cell, biome)`, `currency(-50)`; КОЛИ `tick` → ЯКЩО `custom: «клімат клітини не підходить біому»` → ТО `set_cell(cell, suitable_biome)` (Arctic на екваторі не встоїть).
- КОЛИ `input(set_altitude, cell)` → ТО `custom: «висота клітин довкола курсора ±1 рівень (режим raise / lower)»`, `currency(-50)` — нові острови, озера, гори; змінює клімат і біоми.
- КОЛИ `input(place_life, cell)` → ЯКЩО `counter(energy, >=, cost)` → ТО `spawn(life_class, cell)`, `currency(-cost)` (35 E.U. прокаріоти … 490 E.U. ссавці; місто 500 … 3500 E.U.).
- КОЛИ `input(extinct, life_class)` → ТО `custom: «усі особини класу зникають»` (лише до появи міст).
- КОЛИ `input(move, cell)` → ТО `custom: «перетягнути біом, нішу чи місто в іншу клітину»`, `currency(-30)`.
- КОЛИ `input(examine, cell)` → ТО `window(custom-window)` — інфо-вікно Examine: біом і стан, опади, температура, вітер, головне життя й предок/нащадок, місто, висота, магма; `currency(-5)`.
- КОЛИ `contact(life_a, life_b)` → ТО `custom: «у спільній клітині вищий (клас, вид, IQ) знищує нижчого»`; нова вища мутація переважає всіх нижчих.
- КОЛИ `tick` → ЯКЩО `custom: «є глибоке море або океан»` → ТО `spawn(prokaryote)` — зародження життя.
- КОЛИ `tick` → ЯКЩО `custom: «популяція класу велика, клімат і біом придатні»` and `prob(advance_rate)` → ТО `transform(species, next_species)`; `prob(mutation_rate)` → `transform(species, new_class)` (лише певні види класу мутують).
- КОЛИ `counter(species_index, ==, 16)` → ТО `custom: «клас стає розумним, зʼявляються міста»` — розумний одночасно лише один вид.
- КОЛИ `input(monolith, life)` → ЯКЩО `prob(1/3)` → ТО `transform(life, higher_class)`, `custom: «наступна шкала часу»`; `currency(-2500)` у будь-якому разі.
- КОЛИ `custom: «O2 > 25 %»` → ТО `spawn_at(fire, random)`; КОЛИ `custom: «O2 < 15 %»` → ТО `custom: «тварини гинуть»`; КОЛИ `custom: «CO2 < 0,1 %»` → ТО `custom: «рослини гинуть»`; КОЛИ `custom: «CO2 > 1 %»` → ТО `custom: «парниковий нагрів»`.
- КОЛИ `input(trigger_event, cell)` → ТО `currency(-50)` і ефект події: вулкан — `custom: «висота росте, пил у повітря → похолодання»`; метеор на суші — кратер і пил, у воді — пара → опади; ураган — опади; землетрус із напрямом — `custom: «магма в клітинах міняє напрям»`; чума — `custom: «вимирає місто й перекидається на сусідні»`.
- КОЛИ `custom: «океан теплий»` → ТО `spawn_at(hurricane, ocean)`; КОЛИ `custom: «землетрус чи вулкан у воді»` → ТО `spawn_at(tidal_wave, cell)` — хвиля йде з глибокого в мілке й нищить узбережжя.
- КОЛИ `custom: «міста виросли швидше за паливо»` → ТО `custom: «війна між містами, доки паливо не стане досить»`.
- КОЛИ `timer(cycle)` → ЯКЩО `custom: «запас < максимум складності»` → ТО `currency(+k)` (1 E.U. у Geologic … 8 E.U. у Nanotech).
- КОЛИ `custom: «Nanotech Age або вдалий Моноліт у шкалі Technology»` → ТО `custom: «Exodus: міста відлітають, планета стає заповідником, назад у шкалу Evolution»` — найближче до перемоги.
- КОЛИ `counter(planet_age, >=, 10e9)` → ТО `game_over` (Сонце — червоний гігант).
- **Daisyworld:**
- КОЛИ `tick` → ТО `custom: «сонячне тепло трохи зростає»`.
- КОЛИ `tick` → ЯКЩО `custom: «температура клітини 5–40 °C»` → ТО `custom: «ромашки ростуть, найшвидше при 22,5 °C»`; інакше `custom: «ромашки гинуть»`.
- КОЛИ `tick` → ТО `custom: «ромашка темніша за середовище — тепліша; світліша — холодніша; температура планети залежить від середнього альбедо»`.
- КОЛИ `custom: «кінець сезону»` → ТО `custom: «насіння відтінку, що ріс краще, більшає — наступного сезону його більше»` → холодна планета чорніє й гріється, гаряча біліє й охолоджується.
- КОЛИ `custom: «сонце сильніше, ніж білі ромашки можуть відбити»` → ТО `custom: «регуляція ламається, усе вимирає»`.
- Мета Daisyworld — заповнити світ ромашками; рахунку нема. Поразка загалом — смерть усього життя.

## Керування і ввід
- Миша: панель інструментів Edit Window — Place Life, Trigger Event, Plant Biome (підменю з утриманням кнопки), Set Altitude (клік перемикає raise ↔ lower), Move (drag), Examine (утримання й ведення курсором оновлює дані).
- Plant Biome — тягнеш мишу, і біом кладеться клітина за клітиною; клацання звучить вище або нижче за висотою.
- Землетрус — під-підменю з 8 напрямами енергії. Shift + клік на будь-чому — довідка.

## Вікна, меню, HUD
- `game-screen` = кілька вікон одночасно: Edit Window — мапа клітин, `tool-palette` (6 інструментів), поточний інструмент із ціною, `energy-bar` (Available Energy), `+ui:layer-toggle` (Oceans, Biomes, Cities, Life, Events) і `+ui:map-overlay` (Heat, Rainfall, Winds, SeaFlow, SeaHeat, Magma — лише один одночасно).
- `map-window` — уся планета, 12 відображень у 5 групах (Geosphere, Hydrosphere, Atmosphere, Bio, Civ), рамка Edit Window (`minimap`), Info Box з легендою чи графіком.
- `custom-window` Gaia Window — обличчя планети, реагує на стан життя й дії гравця.
- `stats-window` History Window — 15 показників у часі; `+window:graphs-window` — Air Sample, Biome Ratio (у Daisyworld — 8 відтінків), Life Class Ratio, Technology Ratio.
- `custom-window` Report Window — звіт про планету; у Daisyworld — Major Daisy, Empty Space, Major Animal, Current Task.
- `+window:model-control-panel` ×4 — Geosphere (7 повзунків: дрейф, ядро, вулкани, ерозія…), Atmosphere (сонце, хмари, альбедо, парниковий ефект, обмін повітря-море…), Biosphere (reproduction, advance, mutation), Civilization (інвестиції в джерела енергії й розподіл: наука, агро, медицина, мистецтво, філософія).
- `custom-window` New Planet — складність (Easy / Medium / Hard / Experimental), сценарій чи випадкова планета, шкала часу; `tutorial-window`, `help-window` (Shift + клік), Glossary.
- Меню: File (New, Load, Save, Save As, Quit) · Windows · Models · Graphs · Options (Goto Events, Update Background, Compress Edit Screen, Music, Sound, Messages, Autoscroll) · Speed · Datasound.

## Фічі поза полем
- `mode-sandbox` — Experimental: необмежена енергія; Random Planet — «іграшка» без цілі.
- `difficulty-presets` — енергія Easy 5000 / Medium і Hard 2000 E.U. (і стартова, і максимум).
- 8 сценаріїв: Aquarium, Cambrian Earth, 1990 Earth, Mars, Venus, Ice Planet, Dune, Earth 2XXX + Daisyworld (рельєф випадковий щоразу).
- `speed-control`, `pause`, збереження планети у файл, Relative / Absolute Date.
- Datasound: Tone Monitor (тон = значення масиву, напр. температура) і Data Song — 32 рядки мапи згори донизу, усереднені, грають як ноти.

## Варіації й родичі
- Daisyworld — модель Лавлока як окремий сценарій: 8 відтінків замість 2 у класичній моделі.
- Родичі Maxis у корпусі: `simant` (мураха й мапа ділянок), `simcity-1989` (поля впливу). Тераформінг клітинами: `terra-nil`, `reus`; клітинний клімат: `oxygen-not-included-cells`, `rimworld-rooms`.
- **Осі варіацій**: як вибирається тип клітини — таблиця клімату / сусіди (Life) / гравець; хто змінює клімат — гравець / самі мешканці (альбедо) / обидва; глобальні правила — константи / повзунки моделі.

## Цікавинки для курсу
- Біом за таблицею «температура × опади» з відкатом непридатного біому — 📎.
- Daisyworld: альбедо клітин → температура → ріст → альбедо, петля зворотного звʼязку на сітці — 🥈.
- Конкуренція в клітині «вищий клас перемагає» + дерево просування й мутацій — 🥉.
- Кілька масивів на клітину й перемикачі шарів/оверлеїв для перегляду — 🥉.
- Тераформер: поставлена сутність постійно змінює глобальний параметр, зупинити — лише подією — 📎.
- Data Song: звук як візуалізація масиву — 🌱.

## Мапа на каталог
- Є: `cell-click` · `cursor-place` (Place Life, тераформери) · `hover-highlight` (Examine) · `cell-transform` · `round-currency` (енергія E.U.) · `rule-variants` (повзунки моделей) · `difficulty-levels` + `difficulty-select` · `map-window` + `minimap-radar` · `field-scaling` · `game-pause` · `save-game` · `help-window` · `tutorial-window` · `sound-effects` · `background-music` + `music-toggle` · `game-loop`.
- **Нема** → пропозиції карток:
  - `+biome-climate-table` «Тип клітини з таблиці двох полів» · entities/state · 📎 · слоти {rows, cols}.
  - `+albedo-feedback` «Клітини змінюють поле, що керує їхнім ростом» · entities/state · 🥈.
  - `+species-competition` «Вищий за рангом витісняє з клітини» · entities/interact · 📎.
  - `+evolution-tree` «Сутність просувається або мутує за деревом» · entities/state · 🥉.
  - `+terraformer-emitter` «Поставлена сутність постійно змінює глобальний параметр» · entities/spawn · 📎.
  - `+time-scale-shift` «Шкали часу з різною ціною тіку» · game-logic/progression · 📎.
  - `+global-parameter-sliders` «Повзунки глобальної моделі» · interface/settings · 🌱.
  - `+plate-drift` «Поле течій зсуває блоки клітин» · entities/move · 🥈.
  - `+data-sonification` «Масив поля як звук» · interface/sound · 🌱.
  - `+overlay-view`, `+disasters`, `+biome-terraform` — підтвердження (ONI, SimCity, Reus).

## Пропозиції до словників
- `+card:biome-climate-table`, `+card:albedo-feedback`, `+card:species-competition`, `+card:evolution-tree`, `+card:terraformer-emitter`, `+card:time-scale-shift`, `+card:global-parameter-sliders`, `+card:plate-drift`, `+card:data-sonification` — див. вище.
- `+effect:raise` — підняти/опустити рельєф (підтвердження пропозиції з Populous).
- `+ui:map-overlay` — один кліматичний шар поверх мапи (підтвердження); `+ui:layer-toggle` — вмикач шарів Oceans/Biomes/Cities/Life/Events (підтвердження).
- `+window:model-control-panel` — панель повзунків глобальної моделі; `+window:graphs-window` — графіки співвідношень у часі (підтвердження).

## Джерела
- ⭐ [SimEarth manual (Mac), archive.org](https://archive.org/details/Mac_SimEarth_manual) — читав OCR: Edit Window (ціни інструментів, 32 рівні висоти, 7 біомів і таблиця, 14 класів для розселення, 7 тераформерів), Map Window, меню, Events (11), Atmosphere, Life and Evolution, Civilization, Energy, Daisyworld (с. 118–121).
- [Wikipedia: SimEarth](https://en.wikipedia.org/wiki/SimEarth) — сценарії, Daisy World, Лавлок, цивілізації, exodus, карниферни, платформи.
- YouTube: пошук «SimEarth gameplay».

## Непевне
- (?) Розмір сітки планети і чи зациклена вона по горизонталі — у мануалі не знайшов.
- (?) Енергія Medium і Hard — обидві 2000 E.U. в OCR; можливо, помилка розпізнавання.
- (?) Цикл шкал Evolution / Civilization / Technology — бачив лише Geologic (10 млн років).
- (?) Як саме насіння ромашок переходить між сусідніми клітинами — мануал пояснює модель на рівні планети.
- (?) Карниферни зʼявляються від надлишку комах — лише Wikipedia.
