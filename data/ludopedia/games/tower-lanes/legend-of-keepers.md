---
title: Legend of Keepers
slug: legend-of-keepers
aka: ["Legend of Keepers: Career of a Dungeon Manager", LoK]
family: tower-lanes
also: [roguelike]
klass: hybrid
axes:
  field: 1d
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: survive
year: 2021
platforms: [PC, macOS, Linux, Switch, Xbox]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/978520/Legend_of_Keepers_Career_of_a_Dungeon_Manager/", note: "офіційний опис: менеджер підземелля, найм монстрів, запас пасток, страйки й події; перед рейдом бачиш стати й опори групи, герої проходять пастки, з монстрами — покроковий бій"}
  - {kind: other, url: "https://fingerguns.net/reviews/2021/04/29/legend-of-keepers-review-pc-a-reverse-dungeon-crawler/", best: true, note: "огляд: кімнати монстрів (по 3 у позиціях перед/центр/тил), пасток, заклять, бос-кімната; мораль героїв і монстрів, кров/сльози/золото, тижневі події, артефакти, Endless"}
  - {kind: other, url: "https://mgn.gg/?p=7185", note: "огляд: фіксований порядок кімнат, швидкість визначає чергу, мотивація монстрів і 10 тижнів відпочинку, три майстри й умови відкриття, 5 місій × ~40 тижнів, Ascension"}
  - {kind: other, url: "https://gideonsgaming.com/legend-of-keepers-review-villains-of-might-and-musk", note: "огляд: кімнати відпочинку й катастроф, опори й слабкості, мораль, меню грабунку, модульна складність, швидкість анімацій"}
  - {kind: other, url: "https://www.148apps.com/reviews/legend-of-keepers-review/", note: "огляд: тижневий розклад-кнопки, дві команди по 3 монстри + пастки, міні-бос"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=978520&count=60&maxlength=5000&enddate=1625000000", note: "патчноути (JSON): пороги моралі 75/50/25, −20 % моралі за полеглого, Burn/Frostbite 5 %, мотивація −1/−2, кров і сльози на рівні 4+, інтерни, 3 швидкості"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Legend+of+Keepers+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [placement-screen, hp-damage, status-effects, melee-vs-ranged, run-relics, shop-catalog, shop-between-levels, unit-xp-skills, difficulty-levels, rule-variants, character-select, mode-select, codex-window, achievements-window, leaderboard, +reverse-td, +room-sequence, +party-formation, +target-position, +speed-turn-order, +morale-states, +scare-or-kill, +elemental-resistance, +unit-fatigue-rest, +random-encounter, +weekly-schedule, +talent-tree, +run-meta-carry, +ascension-levels, +fast-forward, +leader-death-lose]
proposes: ["+trigger:fled", "+effect:morale", "+cond:position", "+cond:morale", "+role:unit", "+window:week-planner", "+window:raid-select", "+window:talent-tree", "+window:custom-run", "+feature:ascension-levels", "+feature:mutators", "+card:scare-or-kill", "+card:unit-fatigue-rest", "+axis:session"]
author: opus
date: 2026-11-09
---

# Legend of Keepers — реверс-кроулер: розстав монстрів і пастки по кімнатах, а потім покроково бий героїв, що йдуть до скарбу

## Суть
Гравець — менеджер підземелля в «Dungeons Company»: між рейдами він тижнями керує персоналом (найм, тренування, лікування, мотивація, події), а коли приходить група з трьох героїв — бачить їхні стати й опори і **розставляє монстрів і пастки по кімнатах** фіксованої послідовності. Далі герої проходять кімнати: пастки спрацьовують самі, у кімнатах монстрів іде покроковий бій «три на три» з позиціями, у кімнаті заклять гравець кидає закляття, наприкінці чекає Майстер. Клас — `hybrid`: курсорна розстановка (TD) + фігурний бій (Darkest Dungeon навиворіт); героя можна вбити (кров) або налякати до втечі (сльози).

## Поле і час
- Підземелля — **лінійна послідовність кімнат** (`field: 1d`): зазвичай 2 кімнати монстрів, 1–2 кімнати пасток, кімната заклять і кімната Майстра в кінці; порядок задано на рейд, монстра в «чужу» кімнату не перенести.
- Пізніше додаються кімнати відпочинку (Campfire, Fountain of Youth, Sacred Altar — лікують героїв), кімнати катастроф (ефект залежить від середовища) і офіс інтерна — міні-бос замість 3-ї кімнати монстрів.
- Кімната монстрів — дві шеренги по 3 позиції: перед, центр, тил; уміння бʼють певну позицію або всіх.
- Час: стратегічний шар — **тижні** (місія ≈ 40 тижнів; у ранньому доступі — 2 роки по 52), рейди раз на кілька тижнів; бій — покроковий, черга за швидкістю.
- Середовища: Fortress, Frozen Caves, Aztec Ruins, Cursed Temple, Pyramids (DLC).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Майстер (Slaveholder, Enchantress, Lira — Monkey Engineer) | boss (сторона гравця) | HP, рівень, дерево талантів, уміння | бʼється в останній кімнаті; HP після рейду не відновлюється повністю, регенерує з часом; загинув — кінець забігу |
| Монстр | ally (`+role:unit`) | HP, швидкість, 1–3 уміння, опори/слабкості, рівень, мотивація | стоїть на позиції; гравець обирає його уміння в бою |
| Мех-монстр | ally | механічний тип | окремий клас монстрів (0.9.0) |
| Інтерн | boss | міні-бос | займає 3-тю кімнату монстрів |
| Пастка (Ballista, Furnace, Icy Breeze, Oil Cauldron, Poisonous Plant, Mechanical Spider, Tesla Cannon, Polar Portal, Electrical Coil) | hazard | шкода / шкода моралі / дебаф, рівень | спрацьовує сама, коли група входить у кімнату |
| Закляття / катастрофа | object | ефект | кидається в кімнаті заклять / катастроф |
| Кімната | zone | тип: монстри · пастки · закляття · відпочинок · катастрофа · інтерн · Майстер | визначає, що відбувається з групою |
| Герой (Monk, Bard, Hoplite, Nomad, Druidess, Mamluk, Knight, Ice Wizard, Hunter, Wizard…) | enemy | HP, мораль, швидкість, опори, ранг | атакує позиції монстрів; тікає при моралі 0 |
| Чемпіон | boss (ворожий) | вищий ранг | у пізніх місіях і наприкінці забігу; рідкісні нагороди |
| Артефакт | pickup | пасив | позиційні/групові бафи, шанс воскресіння, трансформація при смерті, ефекти на все підземелля |
| Золото · кров · сльози | resource | — | за захист · за вбитих · за наляканих героїв |
| Стани: Burn, Frostbite, Stunned, Guaranteed Critical, Dodge | — | — | Burn/Frostbite — 5 % max HP вогнем/льодом щоходу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(week)` → ТО `choose(завдання тижня)`: торговець, лікар, терапевт, тренування, Siege, Ritual, Interview, Plunder, Business Trip, випадкова подія.
- КОЛИ `input(task, plunder)` → ТО `choose(поселення)` — сильніша група героїв ↔ більша нагорода.
- КОЛИ `input(task, siege)` → ТО `custom: «здати пастки Компанії в оренду»`, `currency(+gold)`.
- КОЛИ `custom: «вампіри вимагають податок»` → ТО `counter(blood, -n)`, `currency(+gold)`.
- КОЛИ `custom: «тиждень рейду»` → ТО `reveal(hero_stats, resistances)`, `window(placement-screen)`.
- КОЛИ `input(place, monster, room)` → ЯКЩО `count(monsters_in_room, <, 3)` and `not state(monster, demotivated)` and `not state(monster, injured)` → ТО `place(player, monster)`.
- КОЛИ `input(place, trap, trap_room)` → ТО `place(player, trap)`.
- КОЛИ `enter(heroes, trap_room)` → ТО `damage(targets, n)` або `custom: «−мораль»`, або `set_state(heroes, debuff)`.
- КОЛИ `enter(heroes, monster_room)` → ТО `custom: «покроковий бій; черга за швидкістю»`.
- КОЛИ `turn_start(monster)` → ТО `choose(skill)`; ціль — `custom: «позиція перед / центр / тил або вся група»`.
- КОЛИ `custom: «удар стихією»` → ЯКЩО `custom: «ціль має опір цій стихії»` → ТО `damage(target, зменшена)`; слабкість — `damage(target, збільшена)`.
- КОЛИ `turn_start(fighter)` → ЯКЩО `state(fighter, burn)` → ТО `damage(fighter, 5 % max HP)`; Frostbite — так само льодом.
- КОЛИ `custom: «мораль героя < 50 %»` → ТО `custom: «герой отримує більше шкоди»`.
- КОЛИ `custom: «мораль героя впала нижче порога 75 / 50 / 25 %»` → ТО `custom: «вище цього порога вона вже не відновиться»`.
- КОЛИ `custom: «мораль героя = 0»` → ТО `custom: «герой тікає з підземелля»`, `currency(+tears)`.
- КОЛИ `hp_zero(hero)` → ТО `disappear(hero)`, `counter(blood, +n)`.
- КОЛИ `died(hero)` or `custom: «герой утік»` → ТО `custom: «решта групи −20 % max моралі»`.
- КОЛИ `custom: «герой добив монстра»` → ТО `custom: «+5 % моралі цьому герою»`.
- КОЛИ `hp_zero(monster)` → ТО `disappear(monster)` до кінця бою, `counter(motivation, -1|-2)`; після рейду — `respawn(monster, garrison)` з повним HP.
- КОЛИ `counter(motivation, ==, 0)` → ТО `set_state(monster, demotivated, ~10 тижнів)`.
- КОЛИ `input(task, rest, monster)` → ТО `counter(motivation, +n)` щотижня; монстр недоступний на рейд.
- КОЛИ `input(task, doctor | therapist)` → ТО `heal(master, n)` / `counter(motivation, +n)`.
- КОЛИ `enter(heroes, rest_room)` → ТО `heal(heroes, n)`.
- КОЛИ `enter(heroes, spell_room)` → ТО `choose(spell)` → ефект на групу.
- КОЛИ `enter(heroes, master_room)` → ТО `custom: «бій з Майстром та його вміннями»`.
- КОЛИ `all_gone(heroes)` → ТО `currency(+gold)`, `choose(нагорода: монстр | пастка | артефакт | апгрейд)`.
- КОЛИ `hp_zero(master)` → ТО `lose` — забіг завершено.
- КОЛИ `input(train, monster)` → ЯКЩО `custom: «рівень 4+»` → ТО `counter(blood, -10 | -15 для рідкісних)`; пастка рівня 4+ — `counter(tears, -n)`.
- КОЛИ `counter(week, ==, mission_length)` → ТО `win` — місію пройдено, відкривається наступна.
- КОЛИ `game_over` → ТО `custom: «Майстер отримує досвід (і за перемогу, і за поразку)»`.
- Перемога: протриматися всі тижні місії · Поразка: Майстер загинув · Рахунок: кров, сльози, золото; в Ascension — накопичені дебафи.

## Керування і ввід
- Миша / геймпад (повна підтримка контролера); Switch — тач і кнопки.
- Тижневий шар: кнопки-завдання тижня, меню грабунку, крамниця, тренування.
- Розстановка: перетягнути монстра на позицію кімнати, пастку — у кімнату пасток; під час бою розстановку не змінити.
- Бій: вибір уміння монстра і цілі; закляття в кімнаті заклять; три швидкості гри.

## Вікна, меню, HUD
- `main-menu` → `character-select` (Майстер) → `mode-select`: місії, Endless, Ascension; `+window:custom-run` — модульна складність (?).
- `+window:week-planner` — тижневий розклад: кнопки подій і завдань; `+window:raid-select` — меню грабунку (поселення, сила героїв, нагорода).
- `placement-screen` — схема кімнат, стати й опори групи героїв, розстановка монстрів і пасток.
- `game-screen` бою: шеренги 3×3, `hp-bar` і шкала моралі на кожному бійці, черга ходу, `ability-buttons` монстра, `tooltip` опорів.
- `shop-window` — торговець; `+window:talent-tree` — таланти Майстра; `codex-window` — Archivist (артефакти, герої); `end-screen` — результат рейду/забігу.
- `settings-window`: швидкість, screen shake, V-Sync.

## Фічі поза полем
- `meta-progression`: досвід Майстра → таланти (респек між забігами); Enchantress відкривається на рівні 5 Slaveholder; архетипи відкривають монстрів, пастки й артефакти.
- Режими: місії (5 на Майстра, ≈ 40 тижнів кожна) · `mode-endless` · `+feature:ascension-levels` — кожна перемога додає накопичувальний дебаф.
- `difficulty-presets` + модульна складність; `speed-control` (3 швидкості); `achievements`, Steam Workshop, `leaderboard-online`, хмарні сейви.
- DLC: Return of the Goddess (Pyramids, мумії), Feed the Troll, Soul Smugglers.

## Варіації й родичі
- Родичі в корпусі: [dungeon-keeper](dungeon-keeper.md) (зле підземелля проти героїв, але real-time і копання), [dungeon-warfare](dungeon-warfare.md) (пастки на шляху героїв), [monster-train](monster-train.md) (поверхи-смуги й призов захисників), [my-life-as-a-darklord](my-life-as-a-darklord.md); поза корпусом — Darkest Dungeon (позиції 1–4, стрес), Slay the Spire (карта й артефакти).
- **Осі варіацій**: оборона — вежі на шляху / кімнати-етапи з боями · бій — авто / покроковий за позиціями · ворог переможений — смерть / втеча за моралі 0 · персонал — витратний / зі втомою й мотивацією.

## Цікавинки для курсу
- Дві шкали в героя (HP і мораль) і дві різні нагороди за «вбити» та «налякати» — 📎.
- Пороги моралі 75/50/25, нижче яких відновлення не піднімає — 🌱.
- Бій «3 на 3» з позиціями перед/центр/тил і вміннями, що бʼють позицію чи всіх; черга за швидкістю — 🥉.
- Мотивація монстра: падає за смерть, на нулі — 10 тижнів простою; відпочинок як ротація складу — 📎.
- Лінійна послідовність кімнат різних типів як «смуга» TD — 🌱.
- Тижневий менеджмент: вибір однієї події з кількох із ризиком і нагородою — 🥉.

## Мапа на каталог
- Є: `placement-screen` ↔ розстановка перед рейдом · `hp-damage` · `status-effects` ↔ Burn, Frostbite, Stunned · `melee-vs-ranged` ↔ удари по позиціях · `run-relics` ↔ артефакти · `shop-catalog`, `shop-between-levels` ↔ торговець · `unit-xp-skills` ↔ рівні монстрів · `difficulty-levels`, `rule-variants` ↔ модульна складність · `character-select` ↔ Майстри · `mode-select` · `codex-window` ↔ Archivist · `leaderboard`, `achievements-window`.
- **Нема** → пропозиції карток:
  - `+reverse-td`, `+party-formation`, `+speed-turn-order`, `+morale-states`, `+elemental-resistance`, `+random-encounter`, `+talent-tree`, `+run-meta-carry`, `+fast-forward`, `+leader-death-lose` — уже в корпусі.
  - `+room-sequence` «Підземелля — ланцюг кімнат різних типів на шляху ворога» · game-logic/waves · 🌱.
  - `+target-position` «Уміння бʼє позицію шеренги (перед/центр/тил) або всіх» · entities/combat · 📎.
  - `+scare-or-kill` «Друга шкала (мораль): ворог тікає на нулі, окрема нагорода» · entities/state · 📎.
  - `+unit-fatigue-rest` «Мотивація юніта падає від смертей, нуль — простій на N ходів» · entities/state · 📎.
  - `+weekly-schedule` «Стратегічний календар: один вибір події на тиждень» · game-logic/economy · 🥉.
  - `+ascension-levels` «Кожна перемога додає накопичувальний модифікатор складності» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+trigger:fled(a)` — сутність утекла з поля (мораль 0) — інша подія, ніж `died`.
- `+effect:morale(a, ±n)` — змінити мораль; `+cond:morale(a, op, n)` — порівняння моралі з порогом.
- `+cond:position(a, front|mid|back)` — позиція в шерензі.
- `+role:unit` — повтор (бойовий юніт загону).
- `+window:week-planner` — тижневий розклад подій; `+window:raid-select` — вибір цілі набігу з ризиком/нагородою; `+window:talent-tree` — повтор; `+window:custom-run` — налаштування складності забігу по пунктах.
- `+feature:ascension-levels` — накопичувальна складність; `+feature:mutators` — повтор (модульна складність).
- `+card:scare-or-kill`, `+card:unit-fatigue-rest`; `+axis:session` — `run`.

## Джерела
- [Steam: Legend of Keepers](https://store.steampowered.com/app/978520/Legend_of_Keepers_Career_of_a_Dungeon_Manager/) — офіційний опис, Goblinz Studio, ранній доступ 19.03.2020, реліз 29.04.2021, DLC, платформи PC/macOS/Linux.
- ⭐ [Finger Guns: огляд](https://fingerguns.net/reviews/2021/04/29/legend-of-keepers-review-pc-a-reverse-dungeon-crawler/) — кімнати й розстановка по 3, позиції, мораль героїв і монстрів, валюти, тижневі події, артефакти, Майстер з HP і деревом.
- [MGN: огляд](https://mgn.gg/?p=7185) — фіксований порядок кімнат, швидкість і черга, 1–3 атаки монстра, мотивація й 10 тижнів, три майстри, 5 місій × 40 тижнів, Endless і Ascension.
- [Gideon's Gaming: огляд](https://gideonsgaming.com/legend-of-keepers-review-villains-of-might-and-musk) — кімнати відпочинку й катастроф, опори, мораль, меню грабунку, модульна складність, прискорення анімацій.
- [148Apps: огляд](https://www.148apps.com/reviews/legend-of-keepers-review/) — тижневий розклад, дві команди по 3 монстри, міні-бос, перемога — Майстер вижив.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=978520&count=60&maxlength=5000&enddate=1625000000) — пороги моралі, втрата моралі групою, Burn/Frostbite, ціни рівнів у крові й сльозах, інтерни, назви пасток, героїв і середовищ, 3 швидкості.
- YouTube: пошук «Legend of Keepers gameplay».

## Непевне
- (?) Кількість кімнат пасток — 1 чи 2 (джерела розходяться) і чи змінюється порядок кімнат між рейдами.
- (?) Чи може герой пропустити або знешкодити пастку; чи має пастка обмеження використань.
- (?) Як саме працює кімната заклять (ресурс, кількість заклять).
- (?) Чи монстри відроджуються автоматично після кожного рейду чи через подію некроманта.
- (?) Назва третього Майстра в релізі (у патчах — Lira, the Monkey Engineer) і умова його відкриття.
- (?) Модульна складність: які саме параметри; вікно `custom-run` — з патчноутів («custom run settings»).
- (?) Платформи Switch/Xbox — з назв оглядів у пошуку, сторінок не відкривав.
