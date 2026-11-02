---
title: Crypt of the NecroDancer
slug: crypt-of-the-necrodancer
family: roguelike
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: rhythm
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2015
platforms: [PC, PS4, PS Vita, Xbox One, Switch, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Crypt_of_the_NecroDancer", best: true, note: "ядро коротко: хід у такт, множник монет, 4 зони × 4 поверхи, діаманти, персонажі, DLC"}
  - {kind: steam, url: "https://store.steampowered.com/app/247080/", note: "сторінка Steam: 15 персонажів, власні MP3, танцювальний килимок, кооп"}
  - {kind: official, url: "https://braceyourselfgames.com/crypt-of-the-necrodancer/", note: "Brace Yourself Games"}
  - {kind: fandom, url: "https://necrodancer.fandom.com/wiki/Groove_Chain", note: "вікі ворогів/предметів (агенту не відкрилась: 402)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=crypt+of+the+necrodancer+gameplay+zone+1", note: "пошук; геймплей зі смугою бітів"}
stage: v1
coverage: 60
mechanics: [move-4dir, hp-damage, pattern-automaton, chase-greedy, random-walk, enemy-patrol, telegraphed-intents, speed-per-type, combo-multiplier, round-currency, shop-catalog, inventory-items, item-pickup, dungeon-generation, sequential-levels, time-out, cell-transform, impassable-cells, melee-vs-ranged, blast-wave, player-death, background-music, +beat-tick, +missed-beat, +dig-wall]
proposes: ["+trigger:beat", "+trigger:missed_beat", "+trigger:song_end", "+cond:dig_power", "+cond:on_beat", "+effect:reset_combo", "+effect:dig", "+role:boss", "+role:neutral", "+ui:beat-bar", "+ui:heart-container", "+window:lobby-window", "+window:character-select", "+feature:custom-music", "+feature:meta-progression", "+axis:time=rhythm", "+card:rule-twist-character"]
author: opus
date: 2026-11-02
---

# Crypt of the NecroDancer — роглайк, де хід = удар музики: рухайся в такт, бо вороги вже танцюють

## Суть
Покроковий данжен-кроулер, у якому тік задає музика: гравець може ходити й бити лише в біт, а кожен ворог має свій ритмічний патерн (крок щобіта, через біт, по квадрату, ривок по лінії). Убивства без пропущеного біта й без отриманої шкоди ростять множник монет; пропуск його скидає. Кожен поверх обмежений довжиною пісні; коли пісня скінчилась — тебе скидає люком униз. Персонажі — «модифікатори правил» (Bard грає без ритму, Aria гине від пропуску, Monk гине від золота).

## Поле і час
- Квадратна сітка поверху (процедурні кімнати, коридори, крамниця), вид згори, камера стежить за героєм; темрява поза радіусом світла (смолоскипи на стінах, предмет-смолоскип).
- **Тік = біт пісні** (`time: rhythm`): усі вороги діють на кожен біт, навіть якщо гравець пропустив. Темп росте з поверхом (BPM пісні) — складність через швидкість.
- Вікно влучання навколо біта; поза ним — «Missed!»: хід не відбувся, множник скинуто. Гравець може не рухатися (стояти — теж пропуск, якщо ворогів поряд нема — без шкоди).
- 4 зони × 4 поверхи (DLC Amplified — 5-та зона); поверхи 1–3 — знайти вихід (відкривається після мінібоса), 4-й — бос.
- Шари: підлога (диско-підсвітка при множнику, пастки, вогонь/лід у пізніх зонах) + стіни різної міцності + сутності.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Cadence (і ін. персонажі) | player | серця (½ серця = 1 шкода), слоти: зброя, лопата, тіло, голова, ноги, смолоскип, кільце, заклинання, витратні | на біт: крок 4 напрямки / удар / копання |
| Зелений слиз | enemy | 1 HP | не ходить, «підстрибує» на місці |
| Синій слиз | enemy | 2 HP | туди-сюди по лінії кожні 2 біти |
| Помаранчевий слиз | enemy | 1 HP | ходить по квадрату 2×2, крок щобіта |
| Скелет (білий/жовтий/чорний) | enemy | 1–3 HP | крок до гравця кожні 2 біти; жовтий/чорний без голови тікає |
| Кажан (синій/червоний) | enemy | 1 HP | випадковий крок; синій — через біт, червоний — щобіта |
| Зомбі | enemy | 1 HP | прямо кожні 2 біти, упершись — розворот |
| Привид | enemy | 1 HP | рухається до тебе, лише коли ти віддаляєшся; підходиш — стає безтілесним |
| Мінотавр | enemy (miniboss) | 3+ HP | на одній лінії з гравцем — ривок до упору; у стіну — оглушений кілька бітів |
| Мавпа | enemy | — | чіпляється на гравця; доки не скинеш — ходи слабші |
| Дракон (зелений/червоний) | enemy (miniboss) | багато HP | повільний; червоний дихає вогнем по лінії |
| Крамар (Shopkeeper) | neutral | співає (гучність = відстань) | стоїть у крамниці; атакуєш — стає ворогом |
| Бос (King Conga, Death Metal, Deep Blues, Coral Riff, Dead Ringer, NecroDancer) | boss | фази | своя механіка (конга-лінія зомбі, шахова дошка, щупальця з води, дзвони) |
| Стіна: земля / камінь / катакомби / крамниця / межа | static | міцність 1…∞ | лопата ≥ міцності → стіна зникає; межа — ніколи |
| Двері | gate | — | відчиняються кроком |
| Сходи (вихід) | static | замкнені до смерті мінібоса | спуск на наступний поверх |
| Люк кінця пісні | terrain | — | коли пісня скінчилась — гравець падає на поверх нижче |
| Пастки (шипи, стрибкова стрілка, телепорт, бомба, люк, сповільнення/прискорення ритму) | hazard | тип | спрацьовують при вході на біт |
| Золото | pickup / resource | купка × множник | падає з убитих ворогів |
| Скриня / ящик / бочка | container | — | ламається ударом, усередині предмет |
| Предмети крамниці | pickup | ціна в золоті | купуються кроком на клітину з ціною |
| Бомба | object | таймер 3 біти | вибух 3×3: шкода всім, руйнує стіни |
| Діамант | resource | — | лишається після смерті; валюта лобі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `beat` → ТО кожен ворог виконує свій `pattern-automaton` крок (див. таблицю); гравець діє лише в цьому вікні.
- КОЛИ `input(dir)` → ЯКЩО `on_beat` → ТО: ЯКЩО `occupied(cell, enemy)` або у зоні зброї → ТО `damage(weapon)`; ЯКЩО `cell(wall)` → ТО `dig`; ЯКЩО `free(cell)` → ТО `move(player, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `not on_beat` → ТО `custom: «Missed! — дія не відбувається»`, `reset_combo`.
- КОЛИ `missed_beat` (не натиснув за біт) → ТО `reset_combo` (Aria/Coda — `lose`).
- КОЛИ `input(dir into wall)` → ЯКЩО `dig_power(shovel) >= hardness(wall)` → ТО `set_cell(floor)`; інакше `custom: «лопата дзвякає, хід витрачено»`.
- КОЛИ `died(enemy)` → ЯКЩО `not missed_beat` і `not damaged` з попереднього вбивства → ТО `combo(+1)` → `multiplier(×1→×2→×3)`; підлога світиться («диско»).
- КОЛИ `died(enemy)` → ТО `spawn(gold)`; КОЛИ `contact(player, gold)` → ТО `currency(+n × multiplier)` (Monk/Coda — `lose`).
- КОЛИ `contact(enemy, player)` (атака на біт) → ТО `hp(player, -n)`, `reset_combo`.
- КОЛИ `hp_zero(player)` → ТО `lose`: забіг закінчено, предмети й золото втрачені, діаманти лишаються.
- КОЛИ `line_of_sight(minotaur, player)` → ТО `custom: «ривок по лінії до упору»`; КОЛИ `blocked(minotaur)` → ТО `stun(minotaur, n)`.
- КОЛИ `beat` → ЯКЩО `state(player, moving_away)` → ТО `move(ghost, to player)`; інакше ghost `set_state(intangible)`.
- КОЛИ `contact(player, shop_item)` → ЯКЩО `count(gold, >=, price)` → ТО `currency(-price)`, `give(player, item)`; інакше `block`.
- КОЛИ `contact(player, shopkeeper)` (удар у клітину крамаря) → ТО `set_side(shopkeeper, enemy)`.
- КОЛИ `input(bomb)` → ТО `spawn(bomb)`; КОЛИ `timer(3 beats)` → ТО `blast-wave` 3×3: `damage` усім, `set_cell(floor)` для руйнованих стін.
- КОЛИ `died(miniboss)` → ТО `unlock(stairs)`; КОЛИ `enter(player, stairs)` → ТО `next_level`.
- КОЛИ `song_end` → ТО `custom: «люк під гравцем»` → `next_level` (без нагород поверху).
- КОЛИ `died(boss)` на 4-му поверсі → ТО наступна зона; NecroDancer у зоні 4 → `win`.
- Перемога: пройти всі поверхи й боса зони (або All Zones Mode без смерті). Поразка: серця = 0 (або порушення правила персонажа). Рахунок: золото (з множником), швидкість, діаманти в мета-прогрес.

## Керування і ввід
- 4 стрілки (або WASD / геймпад / **USB-килимок для танців**) — рух/атака/копання в напрямку; діагоналей нема (крім окремих персонажів).
- Комбінації двох клавіш одночасно — використати предмет/бомбу/заклинання (напр. вниз+ліворуч — бомба, вгору+вниз — витратний предмет) (?).
- Біт видно на `beat-bar` унизу: рисочки збігаються до серця в центрі; калібрування затримки в налаштуваннях.
- Bard: ритму нема — гра чекає натискання, як класичний покроковий роглайк.

## Вікна, меню, HUD
- `game-screen` — поле, `beat-bar` з серцем у центрі (бʼється в такт), `hp-bar` як ряд сердець, `coins` + `multiplier`, діаманти, слоти спорядження (зброя, лопата, тіло, голова, ноги, смолоскип, кільце, заклинання, витратні) з клавішами.
- `minimap` (поверх у кутку) — досліджене; видно позицію виходу після знаходження.
- `lobby-window` — хаб між забігами: входи в зони, тренування, крамарі мета-апгрейдів за діаманти, вибір персонажа.
- `character-select` — портрети персонажів з описом правил-модифікаторів.
- `shop-window` у лобі (мета) — розблокувати предмети/серця за діаманти; у забігу крамниця — це просто клітини з цінами (без вікна).
- `end-screen` — смерть: причина, зібране золото/час, «спробувати знову»; кінцевий рахунок зони.
- `leaderboard` — онлайн-таблиці для кожного режиму/персонажа/daily.
- `settings-window` — калібрування аудіо/відео затримки, гучності, власна музика (вибір MP3 на зону/поверх), перепризначення клавіш.
- `pause-menu` — гра на паузі (музика стоїть).
- Переходи: `main-menu` → `lobby-window` → (вхід у зону / `character-select`) → `game-screen` → (сходи) наступний поверх → … → бос → наступна зона; смерть → `end-screen` → лобі.

## Фічі поза полем
- `meta-progression`: діаманти й розблокування в лобі (нові предмети в пулі, стартові серця).
- `mode-classic` (зона за зоною), All Zones Mode (`mode-hardcore`-подібний: усе без смерті), `mode-daily` (Daily Challenge, одна спроба), `seed-input` (Seeded runs), `mode-practice` (тренування на конкретних ворогах/босах).
- `custom-music` — власні MP3 з автовизначенням BPM; `remap-controls`, `gamepad-support`, `local-multiplayer` (кооп на двох), Synchrony — онлайн до 8 гравців.
- `leaderboard-online`, `replay` (?) спідранів у таблицях.
- `mod-support` (Synchrony), скіни персонажів.

## Варіації й родичі
- Cadence of Hyrule (2019) — та сама ритм-механіка у світі Zelda; Rift of the NecroDancer — ритм-гра без роглайку.
- Персонажі як осі правил: **ритм** (обовʼязковий / нема — Bard / подвійний темп — Bolt) · **пропуск біта** (лише скид множника / смерть — Aria) · **золото** (валюта / смерть — Monk) · **атака** (є / нема — Dove) · **рух** (4 напрямки / 8 — Diamond (?)).
- Осі ворогів «на біт»: період (1 / 2 / 3+ біти), напрям (до гравця / фіксований патерн / випадковий / по лінії до упору), реакція на погляд (привид).
- Родичі: Rogue/DCSS (тік = хід гравця), Hoplite (детерміновані реакції), Crypt-клони з ритмом.

## Цікавинки для курсу
- Тік = біт: глобальний метроном + вікно влучання навколо біта; ввід поза вікном — «Missed» — 🥉 (game loop з аудіо-синхронізацією і калібруванням).
- Патерн-автомати ворогів у бітах (слиз по квадрату, зомбі туди-сюди, скелет через біт до гравця, мінотавр-ривок, привид-«не дивись») — 📎 кожен, 🥉 за сімʼю.
- Множник монет за серію убивств без пропуску й шкоди + диско-підсвітка підлоги — 📎.
- Копання стін лопатами різної «міцності» (`dig_power ≥ hardness`) — 🌱 (таблиця «лопата × стіна»).
- Пісня = таймер поверху, кінець — примусовий спуск — 🌱.
- Персонаж = набір модифікаторів правил (Bard без ритму, Aria — смерть за пропуск, Monk — смерть від золота) — 🥈 (архітектура правил як даних, що їх персонаж перевизначає).
- Власна музика: визначити BPM з MP3 і побудувати сітку бітів — 👑 (beat detection — дослідницька задача).

## Мапа на каталог
- Є: `move-4dir` · `hp-damage` · `pattern-automaton` (слизи, зомбі) · `chase-greedy` (скелети) · `random-walk` (кажани) · `enemy-patrol` · `telegraphed-intents` (вороги готуються перед ударом (?)) · `speed-per-type` (через біт / щобіта) · `combo-multiplier` · `round-currency` (золото) · `shop-catalog` · `inventory-items` · `item-pickup` · `dungeon-generation` · `sequential-levels` · `time-out` (кінець пісні) · `cell-transform` (копання) · `impassable-cells` · `melee-vs-ranged` (зброя: кинджал/спис/широкий меч) · `blast-wave` (бомба) · `player-death` · `background-music`.
- **Нема** → пропозиції карток:
  - `+beat-tick` «Тік = біт музики з вікном влучання» · core/loop · 🥉 · слоти {bpm, window_ms}.
  - `+missed-beat` «Пропуск біта: штраф (скид множника / смерть)» · rules/penalty · 📎 · слот {penalty}.
  - `+dig-wall` «Копання стіни інструментом за міцністю» · entities/interact · 📎 · слоти {hardness, tool_power}.
  - `+line-charge` «Ворог-ривок по лінії, оглушення об стіну» · entities/move · 📎.
  - `+look-away-chase` «Ворог рухається, лише коли гравець віддаляється (привид)» · entities/move · 🌱.
  - `+song-timer` «Довжина пісні = ліміт поверху» · rules/lose · 🌱 (дитина `time-out`).
  - `+rule-twist-character` «Персонаж змінює правила гри» · rules/meta · 🥈.

## Пропозиції до словників
- `+trigger:beat` — подія метронома музики (окремо від `timer`: період задає аудіо, не годинник); `+trigger:missed_beat` — біт минув без вводу; `+trigger:song_end` — пісня поверху скінчилась.
- `+cond:on_beat` — ввід у вікні влучання; `+cond:dig_power` — сила інструмента ≥ міцності клітини.
- `+effect:reset_combo` уже ⏳ — вживано; `+effect:dig` — зруйнувати стіну інструментом (окремо від `set_cell`, бо витрачає хід і має міцність).
- `+role:boss`, `+role:neutral` (крамар) — ⏳, підтверджую вжиток.
- `+ui:beat-bar` — смуга бітів, що збігаються до центру; `+ui:heart-container` — HP рядом сердець з половинками.
- `+window:lobby-window` — хаб між забігами (входи в зони, мета-крамниці); `+window:character-select` — ⏳, вжито.
- `+feature:custom-music` — власні треки задають темп гри; `+feature:meta-progression` — ⏳, вжито.
- `+axis:time=rhythm` — ⏳-значення осі, тут еталон.
- `+card:rule-twist-character` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Crypt of the NecroDancer](https://en.wikipedia.org/wiki/Crypt_of_the_NecroDancer) — хід у біт, множник, зони/поверхи/боси, діаманти, Monk, DLC Amplified і Synchrony.
- [Steam](https://store.steampowered.com/app/247080/) — 15 персонажів, власні MP3, килимок, кооп.
- [Brace Yourself Games](https://braceyourselfgames.com/crypt-of-the-necrodancer/) — офіційна сторінка.
- [NecroDancer Wiki (fandom)](https://necrodancer.fandom.com/wiki/Groove_Chain) — довідник ворогів/предметів (агенту не відкрився — 402).
- YouTube: пошук «crypt of the necrodancer gameplay zone 1».

## Непевне
- (?) Патерни ворогів (слизи, скелети, кажани, зомбі, привид, мінотавр, мавпа), типи стін і лопат, пастки, комбінації клавіш для предметів — з памʼяті; фан-вікі агенту недоступна (402/403), підтверджено лише «скелети ходять через біт» (Wikipedia).
- (?) Максимальний множник (×3, з кільцем більше) і умова «без шкоди» для серії — Wikipedia: «убивства поспіль без шкоди й без пропуску біта», стелю не названо.
- (?) Правила персонажів: Aria (гине від пропуску, мала кількість сердець, зони в зворотному порядку), Bard (без ритму), Bolt (подвійний темп), Dove (не атакує), Diamond (діагоналі) — з памʼяті; Monk «гине від золота, безкоштовний предмет у крамниці» — підтверджено Wikipedia.
- (?) BPM поверхів і ширина вікна влучання.
