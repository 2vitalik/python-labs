---
title: "Unity of Command: Stalingrad Campaign"
slug: unity-of-command
aka: [UoC, "Unity of Command", "UoC2", "Unity of Command II"]
family: tactics
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2011
platforms: [PC, Mac, Linux]
links:
  - {kind: other, url: "https://store.steampowered.com/manual/218090", best: true, note: "офіційний мануал (PDF): кроки, AP, ZOC, формула шансів, зсуви, CRT, відступ/overrun, постачання, підкріплення, спеціалісти"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Unity_of_Command_(video_game)", note: "Stalingrad 1942/43, операційний рівень, DLC Red Turn / Black Turn, UoC II (2019: 3D, туман, штаби)"}
  - {kind: official, url: "https://unityofcommand.net/unity-of-command/", note: "17 сценаріїв, 20 км на гекс, 4 дні на хід, History Mode, мультиплеєр через сервер"}
  - {kind: steam, url: "https://store.steampowered.com/app/218090/Unity_of_Command_Stalingrad_Campaign/", note: "Steam: опис, демо, мануал"}
  - {kind: steam, url: "https://store.steampowered.com/app/809230/Unity_of_Command_II/", note: "сиквел"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Unity+of+Command+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [hp-damage, piece-move-patterns, legal-move-highlight, reachable-highlight, path-preview, ai-opponent, async-multiplayer, difficulty-levels, sequential-levels, level-unlock, in-game-editor, replay, round-currency, unit-xp-skills, reinforcements, +hex-grid-render, +supply-lines, +supply-trace-rail, +out-of-supply-decay, +suppressed-steps, +step-strength, +specialist-step, +action-point-or-extended-move, +zone-of-control, +weak-unit-no-zoc, +front-line-sweep, +combat-odds-shifts, +combat-results-table, +damage-forecast, +retreat-overrun, +entrenchment, +terrain-move-cost, +weather-modifiers, +theater-assets, +prestige-economy, +victory-tiers, +turn-limit-objectives, +reorganize-disband, +encirclement-win]
proposes: ["+trigger:enter_zoc", "+effect:suppress", "+effect:recover", "+effect:retreat", "+effect:overrun", "+effect:lock_ap", "+cond:in_supply", "+cond:weak", "+role:supply-source", "+role:specialist", "+ui:combat-sheet", "+ui:step-dots", "+ui:supply-overlay", "+window:objective-view", "+window:force-pool", "+feature:history-mode"]
author: opus
date: 2026-11-09
---

# Unity of Command — гекси Сталінграда: постачання тече рейками, оточений юніт тане без бою

## Суть
Операційна воєнна гра на гексах (20 км на гекс, 4 дні на хід) про кампанію 1942/43 років за вермахт або Червону армію. Головне — **постачання**: його «розливають» від джерел по мапі, як рух, рейками — безкоштовно; юніт, відрізаний від мережі на початку ходу, з кожним ходом втрачає готовність (**пригнічені кроки**), AP і рух — тож оточення виграє більше, ніж лобова атака. Юніт складається з **кроків** (до 7 + 1 спеціаліст), має одне очко дії: або атакувати, або зробити ривок. Бій прозорий: шанси, зсуви і прогноз втрат видно до кліку, але результат трохи рандомізовано.

## Поле і час
- Гекс-мапа з ландшафтом (рівнина, ліс, гори, болото, пагорби, пустеля, місто, руїни, море), річками з мостами, залізницями; частина гексів поза грою.
- Хід — дві фази: діє одна сторона, інша спостерігає; потім навпаки. Ліміт ходів сценарію.
- **Лінія фронту**: кожен гекс має власника; рух по ворожій території забирає маршрут і «замітає» сусідні гекси.
- Погода (суха / багнюка / сніг) змінює ціну руху, постачання і зсуви бою.
- Повна інформація в UoC1 (туман лише в UoC II); видно мережу постачання обох сторін (Supply View).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Юніт (дивізія / корпус) | piece | тип, Attack, Defense, Armor, Normal/Extended Mov, кроки ≤7, досвід, 1 AP | рух, атака сусіда, окопування |
| Активний крок | mark | — | бере участь у бою і першим приймає втрати |
| Пригнічений крок (сірий) | mark | — | не бʼється; втрачається лише коли активних нема; відновлюється в постачанні |
| Спеціаліст (88 мм FlaK, StuG III, SdKfz 250, Pioniere, NKVD…) | mark | позиція в черзі втрат, зсув броні або артилерії | інженери, розвідка, ППО, ПТ, «ні кроку назад» |
| Слабкий юніт | piece | < 3 активних кроків або відступив цього ходу | не має ZOC |
| Джерело постачання | spawner | радіус (очки) | щоходу «розливає» постачання; захоплене — заперечує ворогу |
| Залізниця | terrain | — | постачання по ній безкоштовне від джерела |
| Річка / міст | terrain | — | переправа без мосту — лише з повними MP, коштує всі MP, AP блокується |
| Місто / руїни | terrain | зсув −2 / −3 | артилерія може зруйнувати місто в руїни |
| Ціль сценарію | zone | очки, строк | взяти всі → перемога; утримувати до кінця |
| Точка розгортання | spawner | — | сюди ставлять нові юніти з резерву |
| Театральні засоби | object | використань за хід | авіаудар, авіапостачання, логістика, мости, партизани (СРСР) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(side)` → ТО `custom: «трасування постачання від джерел з очками = радіус, ціна за ландшафт/погоду; рейками — безкоштовно; крізь фронт — ні»`.
- КОЛИ `phase_start(side)` → ЯКЩО `custom: «гекс юніта в постачанні»` → ТО `custom: «відновити пригнічені кроки: green 1, standard 2, veteran 3, elite 4»`.
- КОЛИ `phase_start(side)` → ЯКЩО `not custom: «в постачанні»` → ТО `counter(oos_turns, +1)`: 1 хід — без відновлення; 2 — `custom: «нема AP, пригнічено 3/2/1 кроки за досвідом»`; 3+ — `custom: «нема AP, MP −1, пригнічено все»`.
- КОЛИ `phase_start(side)` → ТО `counter(ap, =1)`, `counter(mp, =normal)` кожному юніту.
- КОЛИ `input(move, unit, hex)` → ЯКЩО `path_exists(unit, hex)` за таблицею руху (normal / mobile × ландшафт × погода) → ТО `move`, `counter(mp, −cost)`; `custom: «маршрут і сусідні гекси, що межують більше з моїми, стають моїми (крім ZOC, міст, цілей)»`.
- КОЛИ `input(extended_move, unit, hex)` → ЯКЩО `counter(ap, ==, 1)` і `not state(unit, ap_locked)` → ТО `counter(ap, −1)`, `counter(mp, +extended)`, `move`.
- КОЛИ `enter(unit, enemy_zoc)` → ЯКЩО `not custom: «ворог слабкий»` → ТО `counter(mp, =0)`, `set_state(unit, ap_locked)` (розвідка — без блокування); у ZOC не можна ривком.
- КОЛИ `custom: «переправа без мосту або вхід у важкий гекс (A)»` → ЯКЩО `custom: «повні MP і AP»` → ТО `counter(mp, =0)`, `set_state(unit, ap_locked)`.
- КОЛИ `input(attack, unit, target)` → ЯКЩО `adjacent(unit, target)` і `counter(ap, ==, 1)` → ТО `custom: «шанси = round(3·log(A·кроки_атак / D·кроки_зах) / log 3) + зсуви»`, `counter(ap, −1)` (крім overrun).
- Зсуви: `custom: «ландшафт (ліс −1, гори −2, пагорби −1, болото −1, місто −2, руїни −3), окоп −1, багнюка −2, сніг −1, броня +(різниця броні)/10 лише в атаці, артилерія спеціаліста, досвід»`.
- КОЛИ `custom: «бій розраховано»` → ТО `custom: «втрати атакувальника і захисника з CRT за шансами ± випадковий зсув»`, `damage(steps)`; ЯКЩО захисник без втрат і не відступив → `custom: «пригнічення його кроків»`.
- КОЛИ `custom: «після бою»` → ЯКЩО `prob(retreat[odds])` (0…100 %; досвід і NKVD знижують) → ТО `custom: «відступ у найближчий вільний свій гекс, юніт стає слабким»`; нема куди → `custom: «усі кроки пригнічено»`.
- КОЛИ `custom: «захисник відступив»` → ЯКЩО `prob(overrun[odds])` → ТО `custom: «overrun: атакувальник зберігає AP, але отримує пригнічені кроки»`.
- КОЛИ `custom: «завдано втрату»` → ТО `counter(xp, +1)` атакувальнику за кожен знищений/пригнічений крок; пороги рівнів: green 5, standard 10, veteran 25, elite 50.
- КОЛИ `input(dig_in, unit)` → ЯКЩО `counter(ap, ==, 1)` і `custom: «повні MP»` → ТО `set_state(unit, entrenched)`, `custom: «2 кроки пригнічено (інженери — без штрафу)»`; КОЛИ `custom: «юніт рушив або атакував»` → ТО `clear_state(unit, entrenched)`.
- КОЛИ `custom: «окопаний захисник втратив ≥2 кроки або будь-що від інженерів»` → ТО `clear_state(defender, entrenched)`.
- КОЛИ `input(add_steps, unit, n)` → ЯКЩО `custom: «в постачанні (не авіа), n ≤ 3 за хід, разом ≤ 7, та сама нація і тип»` → ТО `custom: «+n пригнічених кроків»`, `currency(−prestige)` для резерву ставки, `counter(xp, −1/5 порогу за крок)`.
- КОЛИ `input(deploy, unit, spot)` → ЯКЩО `free(spot)` і `custom: «точка розгортання не ворожа»` → ТО `spawn_at(unit, spot)` з повними AP/MP.
- КОЛИ `input(reorganize, unit)` → ЯКЩО `custom: «повні AP/MP, в постачанні, не поповнювався»` → ТО `custom: «активні кроки → у пул на наступний хід, пригнічені губляться»`; розформування — `currency(−prestige)` (v1.1).
- КОЛИ `input(asset, air_attack, target)` → ЯКЩО `counter(asset_uses, >, 0)` і ціль не під ППО → ТО `custom: «пригнітити кроки цілі»`; logistics → `custom: «радіус джерела +1»`; bridging → `set_cell(river_hex, bridge)`; partisans → `set_side(hex, soviet)`.
- КОЛИ `enter(unit, objective)` → ТО `set_side(objective, side)`; КОЛИ `custom: «усі цілі мої»` → ТО `win` (Victory / Decisive / Brilliant — за кількістю ходів).
- КОЛИ `counter(turn, >, deadline)` → ЯКЩО `not custom: «усі цілі взято»` → ТО `lose`; у кампанії — кінець кампанії.
- Перемога: усі цілі вчасно · Поразка: ліміт ходів · Рахунок: очки цілей за цінність і час → престиж.

## Керування і ввід
- Клік юніта → помаранчевий контур досяжного (можна атакувати після) / сірий — ривок (Space або колесо перемикає); стрілка маршруту з залишком MP і AP на кінчику.
- Наведення на ворога → **бойовий лист**: сили, усі зсуви (зелені/червоні), шанс, прогноз втрат обох, ймовірність відступу й overrun; клік — атака.
- Кнопки: Supply View (S), Objective View, Terrain view, Show Ownership, Force Pool / Enroute, Dig in, Reorganize/Disband, театральні засоби зліва, End Turn.
- ПКМ / Esc — зняти вибір; Ctrl-H — History Mode.

## Вікна, меню, HUD
- `main-menu`: Campaign (Axis / Soviet) · Scenario · Multiplayer · Editor · Options · Quit.
- `custom-window` «Campaign map» — пройдені/відкриті сценарії, поточний престиж; `level-select` за сценаріями.
- `game-screen`: гекс-мапа; іконка юніта з крапками кроків (`+ui:step-dots`: активні / сірі / спеціаліст), блискавка AP, маркери weak, entrenched, `!` без постачання; `turn-counter` і строк; `+ui:combat-sheet`.
- `custom-window` «Unit sheet» — тип, рух normal + extended, броня, досвід, тип поповнення, деталі спеціаліста.
- Оверлеї: `+ui:supply-overlay` (цифри радіусу, X-бочка поза постачанням), власність гексів, ландшафт.
- `custom-window` «Objective View» (`+window:objective-view`) — цілі, очки, строки.
- `custom-window` «Force Pool / Enroute» (`+window:force-pool`) — кроки й юніти в пулі та резерві з ціною в престижі.
- `replay-window` «History Mode» — після-бойовий повтор ходів.
- `end-screen` — рівень перемоги / поразка, очки, престиж; `editor-window` — редактор сценаріїв.

## Фічі поза полем
- Кампанія за обидві сторони: послідовність сценаріїв на мапі кампанії, відкриття залежить від рівня перемоги; одна поразка — кінець; престиж за рахунок вище порогу.
- 17 сценаріїв; DLC Red Turn (1943–45), Black Turn (1941).
- `async-multiplayer`: партії ходами через сервер розробника, можна повернутися за кілька днів; `replay` (History Mode); редактор і community scenarios.
- UoC II (2019): 3D, туман війни, штаби (HQ) і логістика, розгалужена кампанія, Steam Workshop.

## Варіації й родичі
- Наступник Unity of Command II і його DLC (Blitzkrieg, Barbarossa, Moscow 41, Stalingrad, Don 42, Kursk, Berlin, Desert Rats/Fox, Ardennes 44).
- Родичі: Panzer General (постачання точкове, без мережі) — у корпусі `panzer-general`; [Advance Wars](advance-wars.md) (APC постачає сусідів), [Polytopia](polytopia.md); настільні гекс-варгейми з CRT (Avalon Hill, SPI).
- **Осі варіацій**: логістика — нема / пальне в юніті ([Advance Wars](advance-wars.md)) / мережа постачання, що трасується від джерел (UoC) · бій — детермінований / CRT з шансами й зсувами / кубики · сила — HP / кроки активні + пригнічені.

## Цікавинки для курсу
- Трасування постачання як BFS/Дейкстра з бюджетом очок від кількох джерел, рейки з нульовою ціною, бар'єр — лінія фронту — 🥈.
- Деградація оточених за кількістю ходів поза постачанням (1 / 2 / 3+) — 🌱.
- Кроки «активні / пригнічені» замість HP: хто бʼється, хто приймає втрати першим — 📎.
- Шанси через логарифм відношення сил + сума зсувів + таблиця результатів (CRT) — 📎.
- Прозорий прогноз бою (лист шансів) перед атакою — 🥉.
- Лінія фронту: власність гексів, «замітання» сусідів за правилом більшості — 🥉.
- Одне очко дії: атака або ривок, блокування AP після ZOC/річки — 🌱.

## Мапа на каталог
- Є: `hp-damage` (кроки) · `piece-move-patterns` · `legal-move-highlight` + `reachable-highlight` · `path-preview` (стрілка маршруту) · `ai-opponent` · `async-multiplayer` · `difficulty-levels` (?) · `sequential-levels` + `level-unlock` (кампанія) · `in-game-editor` · `replay` (History Mode) · `round-currency` (престиж) · `unit-xp-skills` · `reinforcements`.
- **Нема** → пропозиції карток:
  - `+supply-lines` «Мережа постачання від джерел» · game-logic/economy · 🥈; `+supply-trace-rail` — рейки безкоштовні.
  - `+out-of-supply-decay` «Ефекти за кількістю ходів без постачання» · entities/state · 🌱.
  - `+suppressed-steps` / `+step-strength` «Сила кроками: активні й пригнічені» · entities/state · 📎.
  - `+specialist-step` «Приєднаний спеціаліст із властивістю» · entities/state · 📎.
  - `+action-point-or-extended-move` «Одне AP: атака або ривок» · game-logic/turns · 🌱.
  - `+weak-unit-no-zoc` «Слабкий юніт без ZOC» · entities/state · 🌱.
  - `+front-line-sweep` «Власність гексів і лінія фронту» · game-logic/territory · 🥉.
  - `+combat-odds-shifts` + `+combat-results-table` «Шанси, зсуви, CRT» · entities/combat · 📎.
  - `+retreat-overrun` «Відступ і прорив з таблиці» · entities/combat · 📎.
  - `+theater-assets` «Обмежені засоби щоходу (авіаудар, мости)» · game-logic/economy · 📎.
  - `+reorganize-disband` «Розформувати юніт у пул кроків» · entities/state · 🌱.
  - `+entrenchment` / `+zone-of-control` / `+weather-modifiers` / `+prestige-economy` / `+victory-tiers` / `+damage-forecast` / `+encirclement-win` — уже в корпусі.

## Пропозиції до словників
- `+trigger:enter_zoc` — вхід у зону контролю ворога.
- `+effect:suppress` — пригнітити N кроків; `+effect:recover` — відновити пригнічені.
- `+effect:retreat` — відступ у свій гекс; `+effect:overrun` — прорив зі збереженням AP.
- `+effect:lock_ap` — AP лише для атаки, без ривка.
- `+cond:in_supply` — гекс юніта в мережі постачання; `+cond:weak` — юніт слабкий.
- `+role:supply-source` — джерело постачання з радіусом; `+role:specialist` — приєднаний крок-спеціаліст.
- `+ui:combat-sheet` — лист шансів і прогнозу; `+ui:step-dots` — крапки кроків; `+ui:supply-overlay` — карта постачання.
- `+window:objective-view` — цілі з очками й строками; `+window:force-pool` — пул поповнень.
- `+feature:history-mode` — повтор кампанії після бою.

## Джерела
- ⭐ [Мануал UoC (Steam)](https://store.steampowered.com/manual/218090) — повні правила: кроки ≤7 + спеціаліст, досвід 5/10/25/50, AP і ривок, таблиці руху, ZOC і слабкі, лінія фронту, формула шансів 3·log(r)/log 3, зсуви, CRT, відступ/overrun, постачання 1/2/3+ ходи, відновлення 1–4, поповнення, реорганізація, спеціалісти, театральні засоби.
- [Wikipedia: Unity of Command (video game)](https://en.wikipedia.org/wiki/Unity_of_Command_(video_game)) — 2011, 2x2 Games, DLC, UoC II.
- [Офіційна сторінка](https://unityofcommand.net/unity-of-command/) — 17 сценаріїв, 20 км/гекс, 4 дні/хід, History Mode, мультиплеєр через сервер.
- [Steam: UoC Stalingrad Campaign](https://store.steampowered.com/app/218090/Unity_of_Command_Stalingrad_Campaign/) — опис, демо.
- YouTube: пошук «Unity of Command gameplay».

## Непевне
- (?) Пункти головного меню (Multiplayer / Editor) — зі змісту мануалу і категорій Wikipedia, екран не бачив.
- (?) Hot-seat — лише категорія Wikipedia; сайт каже про партії через сервер.
- (?) Рівні складності — не перевіряв.
- (?) Лінк `queue` на Wikipedia «Unity_of_Command» веде на військовий принцип — замінено статтею про гру.
- (?) Точні пороги очок для Decisive/Brilliant — у кожного сценарію свої, не перевіряв.
