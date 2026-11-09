---
title: Not the Robots
slug: not-the-robots
aka: [Not The Robots]
family: roguelike
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: both
  goal: collect
year: 2013
platforms: [PC, macOS, Linux]
links:
  - {kind: other, url: "https://indiegamereviewer.com/?p=20451", best: true, note: "огляд: смуга їжі відкриває ліфт, сентрі, пастки, сині блоки-здібності, зелені бонуси, 21 апгрейд, керування"}
  - {kind: steam, url: "https://store.steampowered.com/app/257120/Not_The_Robots/", note: "Steam: 2DArray / tinyBuild, 12.12.2013, 7 будівель, режими short/medium/long"}
  - {kind: itch, url: "https://2darray.itch.io/not-the-robots", note: "itch.io: опис, ввід, доступність"}
  - {kind: other, url: "https://gamegrin.com/reviews/not-the-robots-review", note: "огляд: укриття зникає, коли їси; предмети заряджаються їжею; ящики з обміном предмета"}
  - {kind: other, url: "https://www.cubed3.com/games/reviews/pc/not-the-robots", note: "огляд: горючі плитки, обертові лазери, список здібностей"}
  - {kind: other, url: "https://www.gamingonlinux.com/2014/09/gol-cast-hiding-and-eating-furniture-in-not-the-robots", note: "огляд: квота відкриває вихід, плитки по черзі, бонус за все зʼїдене"}
  - {kind: other, url: "https://en.wikipedia.org/wiki/List_of_roguelikes", note: "рядок у списку роглайків (2DArray, 2013)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Not+the+Robots+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-8dir, keyboard-controls, enemy-patrol, line-of-sight-attack, touch-death, environment-death, collect-quota, reach-exit, destructible-blocks, inventory-items, inventory-limit, item-pickup, temporary-modes, permadeath, dungeon-generation, sequential-levels, difficulty-levels, event-points, combo-multiplier, controls-remap, +eat-your-cover, +charge-by-eating, +blind-swap-box, +sequence-floor-switches, +tag-all-enemies]
proposes: ["+trigger:spotted(a)", "+cond:in_cover", "+card:eat-your-cover", "+card:charge-by-eating"]
author: opus
date: 2026-11-09
---

# Not the Robots — стелс-роглайк: їж меблі, за якими ховаєшся

## Суть
Робот в офісній будівлі мусить **їсти меблі** — і ці ж меблі є його єдиним укриттям від патрулів і лазерів. Кожен зʼїдений стіл наближає вихід (смуга їжі відкриває ліфт), але відкриває лінії вогню: що ближче до кінця рівня, то менше сховків. Рівні процедурні, смерть остаточна, здібності заряджаються лише їжею.

## Поле і час
- Офісні кімнати з клітинною розкладкою (меблі, стіни, плитки підлоги); вид згори.
- Реальний час, рух на WASD (огляди кажуть про «пливке» керування і проскакування повз укриття) — рух, ймовірно, не покроковий по клітинах (?).
- Кампанія — 7 будівель зі зростаючою складністю, у кожній — кілька випадкових рівнів (огляд: 2).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робот | player | броня (з апгрейдом), слоти здібностей | ходить, присідає, їсть меблі поруч |
| Меблі | object | — | укриття від погляду; зʼїдена — зникає, наповнює смугу їжі |
| Ліфт | gate | — | відкривається, коли смуга їжі повна |
| Сентрі (летюча голова) | enemy | невразлива (?) | патрулює; бачить — стріляє |
| Лазер (у т.ч. обертовий) | hazard | патерн | промінь вбиває / шкодить |
| Прожектор | hazard | — | виявляє робота |
| Пастка підлоги (горюча плитка) · стінна пастка · бомба | hazard | — | шкода при вході / за таймером (?) |
| Плитки-перемикачі | switch | порядок | друга ціль рівня: натиснути у визначеному порядку |
| Вузли (nodes) | switch | — | друга ціль: активувати |
| Синій блок (ящик здібності) | container | — | дає випадкову здібність; відкрити = викинути поточну |
| Зелений бонус-ящик | container | — | після цілей: + слот, сканер, множник очок |
| Сяючий ноутбук | pickup | — | зʼїсти — аудіощоденник (сюжет) |
| Стіни, частина — незламні | static | — | здібність може пробити |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(eat)` → ЯКЩО `adjacent(player, furniture)` → ТО `disappear(furniture)`, `counter(food, +n)`, `custom: «здібності заряджаються»`.
- КОЛИ `counter(food, >=, quota)` → ТО `custom: «ліфт відкрито»`; КОЛИ `reach(player, lift)` → ЯКЩО `custom: «додаткові цілі виконано»` → ТО `next_level`.
- КОЛИ `line_of_sight(sentry, player)` → ЯКЩО `not custom: «за меблями / невидимий»` (`+cond:in_cover`) → ТО `damage(player, n)` (`+trigger:spotted(a)`).
- КОЛИ `contact(player, laser)` → ТО `damage(player, n)`; КОЛИ `enter(player, floor_trap)` → ТО `damage(player, n)`.
- КОЛИ `hp_zero(player)` → ТО `lose` — забіг з початку; очки йдуть у постійні розблокування.
- КОЛИ `contact(player, ability_box)` → ЯКЩО `has(player, ability)` → ТО `take(player, ability)`, `give(player, random_ability)`.
- КОЛИ `input(ability)` → ЯКЩО `custom: «заряджено»` → ТО одна з: `set_state(player, invisible)` (не рухатись) · `spawn(pillar)` (закриває огляд) · `set_cell(wall, floor)` · `speed(player, +n)` · `custom: «пастка, що вимикає сентрі на час»`.
- КОЛИ `input(switch)` → ЯКЩО `custom: «наступний за порядком»` → ТО `counter(sequence, +1)`; інакше `custom: «скидання (?)»`.
- КОЛИ `custom: «тегнуто всіх ворогів і пастки»` → ТО ціль рівня виконано.
- КОЛИ `level_end` → ЯКЩО `all_gone(furniture)` або `custom: «без шкоди»` → ТО `score(bonus)`.
- КОЛИ `contact(player, bonus_box)` → ТО `choose(slot | scanner | multiplier)` (?), `custom: «рівень постійного апгрейду»`.
- Перемога: пройти 7 будівель · Поразка: смерть (permadeath) · Рахунок: очки за рівні, бонуси, множник.

## Керування і ввід
- WASD — рух, Shift — присісти, Space — їсти (рекомендують ЛКМ), ПКМ — здібність; геймпад, перепризначення клавіш.

## Вікна, меню, HUD
- `game-screen`: офіс; смуга їжі (`progress-bar`), слоти здібностей (`ability-buttons`), очки, множник.
- `mode-select`: кампанія short / medium / long, challenge-рівні на час (відкриваються в кампанії); `difficulty-select`.
- Екран постійних апгрейдів (21 шт.) — `custom-window`; `tutorial-window` (інтерактивний).
- `settings-window`: керування, субтитри, кольоросліпий режим.

## Фічі поза полем
- `permadeath` · `meta-progression`: очки й бонус-ящики підіймають 21 постійний апгрейд (частина робить пастки смертоноснішими, інші — броня, слоти).
- `difficulty-presets`; `mode-time-attack` (challenge-рівні); сюжет — аудіощоденники; розблоковується попередня гра 2DArray «You Find Yourself In A Room».
- `colorblind-palette` · `remap-controls` · `tutorial` · `gamepad-support`.

## Варіації й родичі
- Робот-їдець + укриття: «Pac-Man навпаки» — кожна зʼїдена точка робить поле небезпечнішим; родичі — `maze-arcade` (стелс-лабіринти), `roguelike/robots` (уникання роботів).
- **Осі варіацій**: ресурс, що є укриттям — їжа (тут) / світло / патрони; квота — % поля / число; здібності — заряд за час / за дію (тут — за їжу).

## Цікавинки для курсу
- «Зʼїж своє укриття»: ресурс = сховок, прогрес = ризик — 🌱 (одна взаємодія, ціле рішення).
- Лінія погляду сентрі з урахуванням меблів — 📎 (Bresenham + оновлення при зʼїданні).
- Заряд здібностей лише їжею — 🌱.
- Сліпий ящик: щоб відкрити, викинь поточну здібність — 🌱.
- Плитки-перемикачі в заданому порядку як друга ціль — 🌱.

## Мапа на каталог
- Є: `move-8dir` (?) · `keyboard-controls` · `enemy-patrol` · `line-of-sight-attack` · `touch-death` · `environment-death` · `collect-quota` · `reach-exit` · `destructible-blocks` (меблі, пробиті стіни) · `inventory-items` · `inventory-limit` (слоти) · `item-pickup` · `temporary-modes` (невидимість) · `permadeath` · `dungeon-generation` · `sequential-levels` · `difficulty-levels` · `event-points` · `combo-multiplier` (множник) · `controls-remap`.
- **Нема** → пропозиції карток:
  - `+eat-your-cover` «Зібране було укриттям» · game-logic/win · 🌱.
  - `+charge-by-eating` «Здібність заряджається збором» · entities/state · 🌱.
  - `+blind-swap-box` «Сліпий обмін предмета» · game-logic/economy · 🌱.
  - `+sequence-floor-switches` «Плитки в заданому порядку» · entities/interact · 🌱.
  - `+tag-all-enemies` «Позначити всіх ворогів» · game-logic/win · 🌱.

## Пропозиції до словників
- `+trigger:spotted(a)` — ворог побачив гравця (стелс), відмінне від `line_of_sight`, бо враховує укриття/стан.
- `+cond:in_cover` — гравець за укриттям / невидимий.
- `+card:eat-your-cover` · `+card:charge-by-eating`.

## Джерела
- ⭐ [Indie Game Reviewer: огляд](https://indiegamereviewer.com/?p=20451) — смуга їжі → ліфт, другі цілі, сентрі, пастки, сині й зелені ящики, 21 апгрейд, керування.
- [Steam](https://store.steampowered.com/app/257120/Not_The_Robots/) — опис, режими, 7 будівель.
- [itch.io](https://2darray.itch.io/not-the-robots) — опис, пристрої вводу, доступність.
- [GameGrin](https://gamegrin.com/reviews/not-the-robots-review) — укриття, заряд їжею, ящики, бонуси, challenge-рівні.
- [Cubed3](https://www.cubed3.com/games/reviews/pc/not-the-robots) — горючі плитки, обертові лазери, здібності.
- [GamingOnLinux](https://www.gamingonlinux.com/2014/09/gol-cast-hiding-and-eating-furniture-in-not-the-robots) — квота, плитки по черзі.
- YouTube: [пошук «Not the Robots gameplay»](https://www.youtube.com/results?search_query=Not+the+Robots+gameplay).

## Непевне
- (?) Опис черги «рівень зникає під тобою» — у жодному джерелі не підтверджено; можливо, плутанина з горючими плитками.
- (?) Рух клітинний чи вільний; 4 чи 8 напрямків.
- (?) Чи сентрі вбиває одразу, чи знімає броню/HP; чи є HP взагалі (огляд: «виявлення — майже завжди смерть»).
- (?) Розмір квоти їжі, кількість рівнів у будівлі, точні ефекти бонус-ящиків.
- (?) Сторінка Wikipedia на гру (⭐ черги) — 404; Steam-ID у черзі (252150) веде на іншу гру.
