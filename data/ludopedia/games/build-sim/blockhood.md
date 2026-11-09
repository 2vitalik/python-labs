---
title: Block'hood
slug: blockhood
aka: [Blockhood, Block hood]
family: build-sim
also: []
klass: cursor
axes:
  field: 3d
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 2017
platforms: [Windows, macOS, Linux]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Block%27hood", best: true, note: "механіка входів/виходів, гниття, доступність, режими Story/Challenge/Sandbox"}
  - {kind: steam, url: "https://store.steampowered.com/app/416210", note: "200+ блоків, гниття без входів, три режими"}
  - {kind: other, url: "https://bdcnetwork.com/new-game-challenges-players-create-utopian-city-block?page=1", note: "стаття: назви ресурсів, приклад дерев, «гроші — ресурс, а не мета»"}
  - {kind: official, url: "https://www.devolverdigital.com/games/blockhood", note: "сторінка видавця (фетчеру 429)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=block%27hood+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [multi-cell-size, cell-click, hover-highlight, round-currency, reachability-check, connectivity-check, cell-transform, sequential-levels, tutorial-window, mode-select, +io-blocks, +resource-pool, +input-decay, +structural-support, +access-path, +resource-unlock, +inhabitant-demands, +weather-modifier]
proposes: ["+cond:inputs_met", "+effect:decay", "+card:io-blocks", "+card:input-decay", "+card:structural-support", "+feature:event-toggle"]
author: opus
date: 2026-11-09
---

# Block'hood — вертикальний квартал з блоків-«машинок»: кожен їсть свої входи й дає виходи, голодний — гниє

## Суть
Гравець будує вертикальну вежу-квартал з квадратних блоків-вокселів (житло, ферми, вітряки, водонапірні башти, парки, крамниці, клініки). Кожен блок має **входи** (що споживає) і **виходи** (що виробляє); мета — скласти мережу, де виходи одних покривають входи інших. Блок без потрібних входів **гниє** й зрештою занедбується або руйнується. Гроші — лише один з ресурсів, а не мета; гра наголошує на екології й взаємозалежності.

## Поле і час
- 3D-сітка вокселів: блоки ставляться один на одного й поруч; ділянка обмежена (у пісочниці розмір налаштовується).
- Real-time симуляція з тіком обміну ресурсами; ресурси накопичуються в спільних запасах (?) і витрачаються блоками.
- Будова має бути **доступною** (сходи й коридори) і **стійкою** (коридор має мати опору, перш ніж на ньому будувати).
- Динаміка середовища: вітер і дощ (додані в EA 2016), запити мешканців (грудень 2016).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор-будівельник | — | вибраний блок | ставить/прибирає блоки |
| Блок (200+ типів) | object | входи · виходи · вартість · стан гниття | щотіку бере входи й дає виходи; без входів — гниття |
| Житло (Flats) | sink | — | споживає ресурси, дає мешканців/працю (?) |
| Ферма | source | — | виробляє їжу |
| Вітряк (Wind Turbine) | source | — | виробляє енергію/електрику |
| Водонапірна башта | source | — | виробляє воду |
| Дерева: Trees / Two Trees / Dense Trees | source | свіже повітря ↔ вода ↔ дозвілля | густі дають найбільше повітря, але ковтають найбільше води й дають найменше дозвілля |
| Парк | source | — | свіже повітря |
| Крамниця | source | — | гроші |
| Клініка | object | — | зменшує хворобливість |
| Сходи · коридор | conduit | опора | дають доступ до блоків; коридор потребує опори |
| Ресурси: вода, свіже повітря, дозвілля, електрика, праця, органічні відходи, споживачі, сіра вода, гроші, енергія, їжа | resource | кількість | виходи одних блоків — входи інших |
| Занедбаний / зруйнований блок | object | — | наслідок довгого гниття; не працює |
| Мешканці | neutral | запити | просять ресурси/блоки (можна вимкнути в пісочниці) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, block, cell)` → ЯКЩО `supported(cell)` and `has(player, resources_for_cost)` → ТО `place(block)`, `take(player, cost)`; інакше `block`.
- КОЛИ `input(place, block, cell)` → ЯКЩО `not supported(cell)` → ТО `block` (коридор без опори не тримає).
- КОЛИ `tick` → ЯКЩО `custom: «усі входи блока є в запасі»` and `path_exists(block, access)` → ТО `take(pool, inputs)`, `give(pool, outputs)`.
- КОЛИ `tick` → ЯКЩО `not path_exists(block, access)` → ТО `custom: «блок недоступний — не працює»`.
- КОЛИ `tick` → ЯКЩО `custom: «хоч одного входу бракує»` → ТО `counter(decay, +1)`, `set_state(block, decaying)`.
- КОЛИ `tick` → ЯКЩО `state(block, decaying)` and `custom: «входи знову є»` → ТО `clear_state(block, decaying)` (?).
- КОЛИ `counter(decay, >=, limit)` → ТО `transform(block, abandoned)` або `disappear_a` (зруйновано).
- КОЛИ `counter(resource, >=, n)` → ТО `unlock(block_type)` — нові блоки й комбінації вимагають додаткових ресурсів.
- КОЛИ `rng(p)` → ЯКЩО `mode(demands_on)` → ТО `custom: «мешканці висувають запит на ресурс/блок»`.
- КОЛИ `rng(p)` → ЯКЩО `mode(events_on)` → ТО `custom: «випадкова подія»` (?).
- КОЛИ `timer(weather)` → ТО `custom: «вітер змінює виробіток вітряків, дощ дає воду»` (?).
- КОЛИ `input(remove, block)` → ТО `disappear_b`.
- КОЛИ `counter(target_resource, >=, quota)` → ЯКЩО `mode(challenge)` and `custom: «у межах обмеженого бюджету»` → ТО `win`.
- Поразка: явної нема — квартал деградує через гниття; у челенджі — не вкластись у ресурси (?). Рахунок — потоки ресурсів.

## Керування і ввід
- Миша: вибір блока з панелі-каталогу → клік по вокселю — поставити; інструмент знесення; обертання/зум камери навколо вежі.
- Наведення на блок — підказка з входами й виходами (?).

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Story · Challenge · Sandbox.
- `game-screen`: 3D-вежа; HUD — палітра блоків (`element-picker`), лічильники ресурсів (`progress-bar`/`coins`), `tooltip` входів/виходів блока (?).
- `level-select` — список 24 челенджів; Story — 5 розділів, що водночас є навчанням (`tutorial-window`), плюс окремі туторіали з просунутих механік.
- `match-setup` (пісочниця): розмір ділянки, запити мешканців увімк/вимк, випадкові події увімк/вимк.
- `end-screen` челенджу (?); `settings-window`; Steam-досягнення (`achievements-window`).
- Переходи: main-menu → mode-select → (Story: розділ / Challenge: level-select / Sandbox: match-setup) → game-screen.

## Фічі поза полем
- Режими: `mode-sandbox`, `mode-puzzle` (челенджі з квотою під обмеженим бюджетом), сюжет із 5 розділів як `tutorial`.
- `custom-difficulty`: розмір ділянки, перемикачі запитів і подій.
- `achievements` (Steam); прогресія — `unlockables` (нові блоки за ресурси).

## Варіації й родичі
- Наступник — Common'hood (2022) від тієї ж Plethora Project.
- Родичі в корпусі: `factorio-belts` (ланцюги виробництва), `oxygen-not-included-cells` (ресурси й газ у клітинах), `townscaper` (вертикальна забудова без економіки), `game-of-life` (стан клітини від умов).
- Осі варіацій:
  - **як доходить ресурс:** спільний запас / лише сусідам / по мережі-провіднику;
  - **що буде з голодним блоком:** простій / гниття з відновленням / руйнування / зараження сусідів (?);
  - **обмеження будови:** доступність шляхом · опора знизу · без обмежень.

## Цікавинки для курсу
- Блок як функція «входи → виходи» з таблиці типів — 🌱; баланс мережі з 10+ типів — 🥉.
- Гниття-лічильник за нестачу входу з порогом занедбання — 📎.
- Доступність: кожен блок має бути досяжний сходами/коридорами (BFS у 3D) — 📎.
- Опора: коридор без підпори не тримає блок (перевірка підтримки в 3D) — 📎.
- Trade-off дерев (повітря ↔ вода ↔ дозвілля) як дизайн таблиці — 🌱.
- Розблокування блоків за накопичені ресурси — 🌱.

## Мапа на каталог
- Є: `multi-cell-size` (?) · `cell-click` + `hover-highlight` · `round-currency` (гроші як ресурс) · `reachability-check` (доступність) · `connectivity-check` · `cell-transform` (гниття → занедбаний блок) · `sequential-levels` (челенджі) · `tutorial-window` · `mode-select`.
- **Нема** → пропозиції карток:
  - `+io-blocks` «Блок з входами й виходами ресурсів» · game-logic/economy · 📎 · слоти {inputs, outputs}.
  - `+resource-pool` «Спільний запас ресурсів» · game-logic/economy · 🌱.
  - `+input-decay` «Гниття без входів» · entities/state · 📎 · слоти {limit, recover}.
  - `+structural-support` «Опора знизу для будови» · entities/legality · 📎.
  - `+access-path` «Кожен блок має бути досяжний» · entities/legality · 📎.
  - `+resource-unlock` «Нові блоки за ресурси» · game-logic · 🌱.
  - `+inhabitant-demands` «Запити мешканців» · game-logic · 📎.
  - `+weather-modifier` «Погода змінює виробіток» · game-logic · 🌱.

## Пропозиції до словників
- `+cond:inputs_met` — у сутності є всі вхідні ресурси за рецептом (Block'hood, Factorio-машини).
- `+effect:decay` — крок деградації сутності з порогом (зараз `counter(decay, +1)` + `set_state`).
- `+card:io-blocks`, `+card:input-decay`, `+card:structural-support` — див. вище.
- `+feature:event-toggle` — увімк/вимк випадкових подій і запитів у пісочниці.

## Джерела
- ⭐ [Wikipedia: Block'hood](https://en.wikipedia.org/wiki/Block%27hood) — 200+ блоків, входи/виходи, гниття, доступність і стійкість, Story (5 розділів) / Challenge (24) / Sandbox, вітер, дощ, запити мешканців.
- [Steam](https://store.steampowered.com/app/416210) — «блоки без потрібних входів гниють і стають занедбаними або зруйнованими», нові блоки за ресурси.
- [BD+C: стаття про гру](https://bdcnetwork.com/new-game-challenges-players-create-utopian-city-block?page=1) — назви ресурсів, приклад трьох видів дерев, гроші як ресурс.
- [Devolver Digital](https://www.devolverdigital.com/games/blockhood) — сторінка видавця (не відкрилась, 429).
- YouTube: пошук «block'hood gameplay».

## Непевне
- (?) «Гниючий блок заражає сусідів» — з рядка черги; жодне відкрите джерело (Wikipedia, Steam, стаття, 1 WebSearch) цього не підтвердило — у правила не внесено.
- (?) Чи ресурси спільні на весь квартал, чи передаються лише сусідам/по мережі; чи гниття відновлюється, коли входи повернулись.
- (?) Розмір блока (1 воксель для всіх?), розміри ділянки, швидкість тіку, поріг гниття.
- (?) Що саме дає житло (праця, споживачі) і точні рецепти блоків; HUD-деталі, екран результату челенджу, умова поразки.
