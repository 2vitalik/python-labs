---
title: Levelhead
slug: levelhead
aka: ["Levelhead: Platformer Maker"]
family: grid-platformer
also: [build-sim, program-robots]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: coop
  info: full
  random: none
  goal: state
year: 2020
platforms: [PC, Switch, Xbox One, iOS, Android]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/792710/Levelhead/", best: true, note: "GR-18 і посилка, 90+ рівнів кампанії, сотні деталей редактора, програмовані перемикачі, публікація, Marketing Department, кооп до 4"}
  - {kind: other, url: "https://blog.bscotch.net/post/levelhead-patch-08/", note: "патч 0.8: канали Send/Receive, Relay (Any/All Active), ZOOM-R, Rift, Eyeswitch, purge gate, кік і Super Jump"}
  - {kind: other, url: "https://gamingtrend.com/reviews/the-makers-maker-levelhead-review/", note: "огляд: телескопічні руки, кидок посилки, платформи редактора, назви з фраз, Exposure Bucks, Tower"}
  - {kind: other, url: "https://www.xboxtavern.com/levelhead-review/", note: "огляд: один удар, чекпойнти, тимчасові сили, par-час відкриває деталі, чайові творцю"}
  - {kind: other, url: "https://steamcommunity.com/app/792710/guides/", note: "гайди спільноти: скидання перемикачів, one-tick, технічні збірки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Levelhead+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [in-game-editor, editor-palette, editor-playtest, level-exchange, level-rating, level-bank, button-toggle, key-and-door, teleport-pair, gravity-fall, carrier-platform, timed-despawn, temporary-modes, touch-death, player-death, checkpoint, reach-exit, event-points, time-bonus, leaderboard, profile-stats, avatar-picker, game-screen, player-camera, online-multiplayer, +carry-goal-object, +signal-channels, +relay-logic, +throw-object-to-jump, +stealth-sensor, +power-purge-gate, +promote-currency, +curated-showcase, +preset-phrase-names, +coop-editing, +unlock-parts-by-par, +camera-trigger]
proposes: ["+trigger:signal(channel)", "+effect:send_signal(channel)", "+cond:signals(mode, channels)", "+effect:throw(a, dir)", "+role:relay", "+window:level-browser", "+window:publish-dialog", "+feature:promote-currency", "+feature:coop-editing", "+card:signal-channels", "+card:relay-logic", "+card:carry-goal-object", "+card:power-purge-gate"]
author: opus
date: 2026-11-09
---

# Levelhead — платформер-конструктор, де робот-курʼєр несе посилку до цілі, а перемикачі звʼязані каналами й реле в справжню логіку

## Суть
Гібрид: **аватар** (робот GR-18 біжить, стрибає, хапає й кидає) + **редактор** на тайловій сітці з сотнями деталей (вороги, пастки, шляхи, програмовані перемикачі, секрети, погода, музика, сили). Мета будь-якого рівня — знайти Посилку й донести до Цілі. Логіка рівня — сигнали на нумерованих каналах: перемикачі «надсилають», двері й інші деталі «слухають», а невидимі Relay переносять сигнал між каналами з режимами Any/All Active, тож гравці збирають логічні вентилі й навіть «комп'ютери». Готовий рівень публікують для всіх, просувають за внутрішню валюту, найкращі потрапляють у Tower.

## Поле і час
- Рівень — тайлова сітка (блоки, бекдропи, контекстні тайлсети, що самі стають стіною/підлогою/мостом); рух аватара вільний з фізикою (швидкість, інерція, кидки).
- Real-time; кроки логіки — тіки (спільнота будує «one-tick» механізми); Relay не змінює стан під час паузи.
- Камера стежить за GR-18; Camera Anchor і ZOOM-R (керований сигналом, 80–140 % поля зору) змінюють огляд.
- Кооп: до 4 гравців локально або через Steam Remote Play — і в грі, і в редакторі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| GR-18 | player | 1 удар | біг (довгий біг — прискорення), стрибок, телескопічні руки хапають обʼєкти; кік униз — маленький «подвійний стрибок» |
| Посилка (Package) | object | — | несуть до Цілі; кинути вниз — вищий стрибок; можна стати на неї |
| Ціль (Goal) | static | — | посилка тут → рівень пройдено |
| BUDD-E | object | (?) | обʼєктна деталь рівня, у тій же категорії, що Посилка й Ціль |
| Jem | pickup | малий / великий варіант | очки; вказує шлях |
| Ключ, батарея, бомба, Flapjack | pickup | — | переносні предмети (ключ — двері, батарея — (?), бомба — руйнування) |
| Pressure plate | switch | канал | надсилає сигнал, поки на ній щось стоїть |
| Clockswitch / Countdown switch | switch | період / відлік | сигнал за часом |
| Eyeswitch | switch | — | сигнал, коли бачить гравця; невидимого (stealth) не бачить |
| Relay | switch | вхідний і вихідний канали; Any / All Active | невидимий; переносить сигнал між каналами |
| Двері | gate | канал | відчиняються, поки отримують сигнал |
| Rift | static | ID | телепорт; вороги теж проходять і повертаються |
| Шлях (Path) | terrain | форма | деталі рухаються ним (платформи, пастки) |
| Платформи: тверді, зникаючі, прохідні знизу, фальшиві стіни/підлоги | terrain | — | різна прохідність |
| Пружина | object | — | підкидає; швидша в тунелі висотою 1 клітина |
| Гармата | spawner | — | стріляє |
| Spike Trap, лезо | hazard | — | дотик — смерть |
| Вороги: Flipegg, Lizumi Thorn, Wingarang, Swoopadoop, Blopfush… | enemy | вид | власна поведінка; частину можна схопити й кинути |
| Сила (Ripcord, Tiptow…) | pickup | тимчасова | Ripcord — гелікоптер-ковзання; Tiptow — прокрастись повз Eyeswitch |
| Purge gate | static | — | знімає сили (stealth, удар, ковзання, ракета) |
| Checkpoint | static | — | точка відродження |
| Jukebox, Boombox, Camera Anchor, ZOOM-R, Sign, Arrow Hologram | static | канал / текст | музика, камера, підказки; частину вмикає сигнал |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(gr18, dir)`; ЯКЩО `custom: «біжить досить довго»` → ТО `speed(gr18, +n)`; без опори — `fall(gr18)`.
- КОЛИ `input(grab)` → ЯКЩО `in_range(gr18, object, n)` → ТО `pickup(gr18, object)` — телескопічні руки.
- КОЛИ `input(throw)` → ЯКЩО `has(gr18, package)` → ТО `custom: «кидок; кинута вниз посилка підкидає GR-18»`.
- КОЛИ `input(kick_down)` → ТО `custom: «вертикальна швидкість встановлюється вгору — малий подвійний стрибок»`.
- КОЛИ `contact(package, goal)` → ТО `win`.
- КОЛИ `contact(gr18, enemy|hazard)` → ТО `custom: «смерть від одного удару»`, `respawn(gr18, checkpoint)`.
- КОЛИ `enter(gr18, checkpoint)` → ТО `custom: «нова точка відродження»`.
- КОЛИ `contact(gr18, jem)` → ТО `pickup`, `score(n)`.
- КОЛИ `contact(any, pressure_plate)` → ТО `custom: «сигнал на канал N, поки натиснута»`.
- КОЛИ `custom: «на каналі N є сигнал»` → ЯКЩО `occupied(cell, door)` і `custom: «двері слухають канал N»` → ТО `custom: «відчинити»`; сигнал зник — зачинити.
- КОЛИ `custom: «зміна сигналів на вхідних каналах Relay»` → ЯКЩО `custom: «режим Any Active — хоч один; All Active — усі»` → ТО `custom: «Relay надсилає сигнал на свій вихідний канал»` — з реле будують AND/OR/NOT і памʼять.
- КОЛИ `timer(every)` → ТО `custom: «Clockswitch надсилає сигнал»`; Countdown — один раз після відліку.
- КОЛИ `line_of_sight(eyeswitch, gr18)` → ЯКЩО `not state(gr18, invisible)` → ТО `custom: «Eyeswitch надсилає сигнал»`.
- КОЛИ `contact(gr18, power)` → ТО `set_state(gr18, power)`; КОЛИ `enter(gr18, purge_gate)` → ТО `clear_state(gr18, power)`.
- КОЛИ `enter(a, rift)` → ТО `teleport(a, rift_pair)`.
- КОЛИ `custom: «сигнал на каналі ZOOM-R»` → ТО `camera(zoom)`.
- Перемога: Посилка на Цілі. Поразка: нема — нескінченні спроби, лічаться Attempts. Рахунок: час і очки (Jem) — окремі таблиці лідерів рівня; бенчмарк-час кампанії.

## Керування і ввід
- Гра: рух, стрибок, схопити/кинути, кік униз; геймпад або клавіатура, тач на мобільних.
- Редактор: курсор по сітці, палітра деталей з варіантами (dropdown), налаштування деталі (канали Send/Receive до 999, видимість, увімк/вимк за сигналом, ID Rift), редактор шляхів, плейтест; спільне редагування до 4 гравців.

## Вікна, меню, HUD
- `main-menu`: кампанія (тренування GR-18), редактор, пошук рівнів, Marketing Department, Tower, профіль.
- `game-screen`: рівень + HUD: Jem/очки, таймер (?), чекпойнт.
- `editor-window`: сітка, палітра деталей за категоріями (у т. ч. «Carryables», «обʼєктні» — GR-18/Посилка/BUDD-E/Ціль), налаштування деталі, режим шляхів.
- `custom-window` «публікація»: назва складається з готових фраз (name combobulator), тег складності (?).
- `custom-window` «Marketing Department»: рівні, просунуті за Exposure Bucks; Tower — постійна вітрина з фільтрами за довжиною й сортуваннями (Hidden Gems).
- `leaderboard` рівня (час, очки) · `profile-window`: аватар, підписники, статистика рівнів (Play Time, Attempts, Followers).
- `end-screen`: доставку виконано, час і порівняння з бенчмарком (?).

## Фічі поза полем
- Прогресія: 90+ рівнів кампанії; бенчмарк-час і умови відкривають деталі редактора й аватари; застряглий рівень не пропустити.
- Спільнота: публікація для всіх платформ, підписки, пошук, Exposure Bucks за гру → просування своїх/чужих рівнів, чайові творцю, Tower (кураторство розробників), Tower Trial, Daily Build.
- Хмара: незавершені рівні зберігаються й переносяться між пристроями.
- Badges — набори деталей, що відкриваються (Hyper Reactive із Relay тощо).

## Варіації й родичі
- [Super Mario Maker](super-mario-maker.md) — головний родич-конструктор; Levelhead відрізняється каналами-сигналами, реле й обовʼязковою доставкою.
- Логіка-дроти: Terraria/Minecraft-редстоун, Factorio-сигнали; канали без дротів — радіо-модель.
- Осі: **звʼязок перемикача з ціллю** (сусідство / дріт / номер каналу); **логіка** (лише toggle / Any/All-реле / таймери); **мета рівня** (дійти / донести обʼєкт / вбити всіх); **просування рівнів** (лайки / валюта / кураторство).

## Цікавинки для курсу
- Канали сигналів: перемикачі «надсилають», деталі «слухають» номер — 🥉.
- Relay з режимами Any/All: логічні вентилі з однієї деталі — 🥈.
- Обʼєкт-мета, який треба донести, і використати як платформу/стрибок — 📎.
- Eyeswitch + невидимість: сенсор лінії бачення, що ігнорує stealth — 📎.
- Purge gate знімає тимчасові сили — 🌱.
- Внутрішня валюта за гру, якою просувають рівні інших, + кураторська вітрина — 🥈.
- Назва рівня з набору готових фраз (без модерації тексту) — 🌱.

## Мапа на каталог
- Є: `in-game-editor` · `editor-palette` · `editor-playtest` · `level-exchange` (публікація) · `level-rating` · `level-bank` · `button-toggle` · `key-and-door` · `teleport-pair` (Rift) · `gravity-fall` · `carrier-platform` (шляхи) · `timed-despawn` (зникаючі платформи) · `temporary-modes` (сили) · `touch-death` · `player-death` · `checkpoint` · `reach-exit` · `event-points` (Jem) · `time-bonus` · `leaderboard` · `profile-stats` · `avatar-picker` · `game-screen` · `player-camera` · `online-multiplayer` (спільнота рівнів).
- **Нема** → пропозиції карток:
  - `+carry-goal-object` «Донести обʼєкт до цілі» · game-logic/win · 📎.
  - `+signal-channels` «Перемикачі й цілі звʼязані номером каналу» · entities/interact · 🥉.
  - `+relay-logic` «Реле Any/All: логіка з сигналів» · entities/interact · 🥈.
  - `+throw-object-to-jump` «Кинутий униз обʼєкт підкидає гравця» · entities/move · 📎.
  - `+stealth-sensor` «Сенсор бачення, якого обходить невидимість» · entities/interact · 📎.
  - `+power-purge-gate` «Ворота, що знімають сили» · entities/state · 🌱.
  - `+promote-currency` «Валюта за гру для просування рівнів» · levels/bank · 🥈.
  - `+curated-showcase` «Кураторська вітрина найкращих рівнів» · levels/bank · 📎.
  - `+preset-phrase-names` «Назва з готових фраз» · levels/editor · 🌱.
  - `+coop-editing` «Спільне редагування рівня» · levels/editor · 🥇.
  - `+unlock-parts-by-par` «Деталі редактора відкриваються за par-час» · levels/progression · 🌱.
  - `+camera-trigger` «Деталь, що за сигналом змінює камеру» · interface/render · 📎.

## Пропозиції до словників
- `+trigger:signal(channel)` — на каналі зʼявився/зник сигнал (Levelhead).
- `+effect:send_signal(channel)` — надіслати сигнал на канал.
- `+cond:signals(mode, channels)` — Any/All вхідних каналів активні (Relay).
- `+effect:throw(a, dir)` — кинути взятий обʼєкт.
- `+role:relay` — невидима логічна деталь, що переносить сигнал.
- `+window:level-browser` — пошук і вітрини рівнів спільноти; `+window:publish-dialog` — публікація з назвою й тегами.
- `+feature:promote-currency`, `+feature:coop-editing` — див. вище.
- `+card:signal-channels`, `+card:relay-logic`, `+card:carry-goal-object`, `+card:power-purge-gate` — див. вище.

## Джерела
- ⭐ [Steam: Levelhead](https://store.steampowered.com/app/792710/Levelhead/) — GR-18, 90+ рівнів, сотні деталей, програмовані перемикачі, публікація, Marketing Department, кооп до 4, статистика рівнів.
- [Bscotch: патч 0.8 Rickety Relay](https://blog.bscotch.net/post/levelhead-patch-08/) — канали Send/Receive (до 999), Relay Any/All Active, ZOOM-R, Rift, Eyeswitch і Tiptow, purge gate, кік, Super Jump, Daily Build, Badges.
- [Gaming Trend: огляд](https://gamingtrend.com/reviews/the-makers-maker-levelhead-review/) — руки, кидок посилки, платформи, назви з фраз, теги складності, Exposure Bucks, Tower.
- [Xbox Tavern: огляд](https://www.xboxtavern.com/levelhead-review/) — один удар, чекпойнти, тимчасові сили, par-час відкриває деталі, чайові.
- [Steam-гайди](https://steamcommunity.com/app/792710/guides/) — скидання перемикачів, one-tick, технічні збірки.
- YouTube: пошук «Levelhead gameplay».

## Непевне
- (?) Що таке BUDD-E і батарея; дія Flapjack.
- (?) Чи треба пройти рівень перед публікацією (як у Mario Maker) — у джерелах не знайдено.
- (?) Розмір рівня, кількість деталей і склад HUD.
- (?) Чи двері лише «поки сигнал», чи мають режим toggle/latch.
- Wikipedia-статті про гру нема (лише згадка в списку ігор Switch).
- (?) Точний список платформ (огляд: «консолі, PC і смартфони»; Xbox One / iOS / Android — з памʼяті).
