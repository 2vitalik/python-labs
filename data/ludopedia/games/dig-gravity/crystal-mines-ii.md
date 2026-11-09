---
title: Crystal Mines II
slug: crystal-mines-ii
aka: [Crystal Mines 2, Crystal Mines]
family: dig-gravity
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: hidden
  random: none
  goal: collect
year: 1992
platforms: [Atari Lynx, NES, PC, Nintendo DS, PSP, iOS, Evercade]
links:
  - {kind: other, url: "https://retroisle.com/ExtraFiles/crystalmines2_manual.txt", best: true, note: "мануал Lynx: керування, TNT, труби, перемикачі гравітації, сплячі демони, коди"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Crystal_Mines_II", note: "огляд: Color Dreams, Ken Beckett, щити, радіація, метали, перевидання"}
  - {kind: other, url: "https://patpend.net/manuals/nes/crystal_mines.txt", note: "мануал NES-першої частини: усі брили, істоти й очки за спосіб вбивства"}
  - {kind: other, url: "https://www.mobygames.com/game/14207/crystal-mines-ii/", note: "MobyGames: платформи й перевидання"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Crystal+Mines+II+Lynx+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, gravity-fall, push-object, collect-quota, reach-exit, time-out, time-bonus, shoot-forward, destructible-blocks, explode-area, chain-detonation, touch-death, environment-death, player-death, temporary-modes, status-effects, inventory-items, item-pickup, cell-transform, level-password, sequential-levels, event-points, status-panel, goal-counter, game-pause, +shifting-gravity, +dormant-enemy, +pipe-transport, +kill-method-bonus, +blob-growth, +self-destruct, +multi-hit-block]
proposes: ["+effect:set_gravity", "+axis:gravity-shifting", "+ui:gravity-indicator", "+feature:self-destruct", "+card:dormant-enemy", "+card:pipe-transport", "+card:kill-method-bonus", "+card:multi-hit-block"]
author: opus
date: 2026-11-09
---

# Crystal Mines II — Boulder Dash зі стрільбою: робот, бластер, TNT, труби й перемикачі гравітації

## Суть
Робот обходить шахту, набирає кристали на задану **суму вартостей** до кінця часу й виходить у коло виходу. Від [Boulder Dash](boulder-dash.md) — падаючі брили, штовхання і квота, але робот **стріляє енергетичним зарядом** і кладе TNT, а блоки мають «міцність» (скільки пострілів/вибухів треба). У II додано **перемикачі напрямку гравітації**, труби, що проводять або перетворюють обʼєкти (брила ↔ кристал), і сплячих демонів, схожих на брили. Перша частина (NES, 1989 (?), неліцензійна Color Dreams) дала основу: багатошарова руйновність, бруд і лава, що ростуть, і очки за спосіб вбивства.

## Поле і час
- Шахта — сітка зі скролом; рамка — непробивна скеля.
- Один шар: у клітині один обʼєкт; брили й кристали падають у поточному напрямку гравітації.
- Real-time з таймером рівня (угорі праворуч) і квотою вартості (унизу праворуч); індикатор гравітації — унизу ліворуч.
- `info: hidden` — сплячі демони виглядають як брили, а вихід (NES) може бути схований під обʼєктами.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робот | player | життя (NES: 5); апгрейди пострілу | рух 4 напрямки; штовхає брили вбік; A — заряд вперед; B — TNT |
| Кристал | pickup | колір = вартість (жовтий найдешевший, білий найдорожчий) | падає; сума вартостей → квота |
| Мʼякий бруд | terrain | світлий | знімається пострілом |
| Твердий бруд | terrain | темний | кілька пострілів (NES: 2) або вибух |
| Брила | object | види за міцністю | падає; штовхається; падаюча вбиває демонів і шкодить роботу |
| Важка скеля | object | — | руйнується зарядом/TNT; падає без опори |
| Непробивна скеля | static | — | стіни й рамка |
| Дерев'яний блок | static | — | розбивається бластером |
| Сплячий демон | enemy | виглядає як брила | штовхнули або вистрілили → прокидається «дуже злим» |
| Демон / монстр | enemy | види | гине від заряду, TNT або розчавлення |
| Труба | object | вхід під прямим кутом до гравітації | проведе штовхнутий обʼєкт наскрізь; деякі: брила ↔ кристал |
| Перемикач гравітації | switch | напрямок | змінює напрямок гравітації для поля |
| TNT (пакети) | pickup | запас | B — кинути й тікати; бере те, що не бере заряд |
| Щит | pickup | час дії (?) | захист робота |
| Захист від радіації | pickup | NES: ~14 с | рятує й лікує опроміненого робота |
| Мішки міді / срібла / золота | pickup | бонус у кінці рівня | тисячі очок, не до квоти |
| Спецінструменти | pickup | — | заховані; потрібні для деяких рівнів |
| Вихід (коло) | gate | — | після звукового сигналу квоти — увійти |

### Елементи першої частини (NES), відомі з мануалу
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мʼяка / тверда / непробивна / вибухова брила | object | 3 постріли або 1 вибух / 2 вибухи / ніщо / детонує | усі штовхаються; вибухова — ланцюг від заряду, вибуху, лави |
| Радіоактивна скеля | hazard | 3 вибухи; відбиває заряд | опромінює робота й істот |
| Бруд (mud) | hazard | росте повільно | → земля, твердий бруд або порожнеча; у лаву → скеля; від заряду → твердий бруд |
| Твердий бруд | object | — | від вибуху → кристал |
| Лава | hazard | росте | у вибухову брилу чи активну бомбу → вибух; може вирости в кристали й брили |
| Істоти ×7 | enemy | мʼяка, тверда, непробивна, радіоактивна, брудна, лавова, газова | кожна має свою вразливість; падіння дає найбільше очок; газова проходить крізь усе й полює |
| Бонуси | pickup | rapid fire ≤5, дальність ≤30, невидимість, захист від вибуху / бруду й лави, заморозка таймера (~14 с) | частина губиться зі смертю |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(target, empty|soft_dirt)` → ТО `move(robot, dir)`; бруд → `set_cell(empty)` (?).
- КОЛИ `contact(robot, boulder)` горизонтально → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `input(A)` → ТО `spawn(energy_burst)` у напрямку погляду; КОЛИ `contact(burst, block)` → ТО `damage(1)`; `hp_zero(block)` → `disappear_b`.
- КОЛИ `input(B)` → ЯКЩО `has(robot, tnt)` → ТО `take(tnt)`, `place(tnt)`; КОЛИ `timer(fuse)` → `explode(area)`.
- КОЛИ `tick` → ЯКЩО `not supported(rock|crystal)` у напрямку гравітації → ТО `fall`.
- КОЛИ `contact(falling boulder, demon)` → ТО `disappear_b`, `score(n)` (NES: падіння = найвищі очки).
- КОЛИ `contact(falling boulder, robot)` → ТО `damage(n)` / `lose` (?).
- КОЛИ `contact(robot|burst, dormant_demon)` → ТО `transform(demon)`, `set_state(demon, angry)`.
- КОЛИ `contact(demon, robot)` → ТО `lose`, `lives(-1)`.
- КОЛИ `contact(robot, gravity_switch)` → ТО `custom: «set_gravity: новий напрямок для всіх падаючих»`, оновити індикатор.
- КОЛИ `after(push)` обʼєкта в трубу → ЯКЩО `custom: «вхід під прямим кутом до гравітації»` → ТО `custom: «обʼєкт ковзає крізь трубу»`; труба-перетворювач → `transform(crystal|boulder)`.
- КОЛИ `contact(robot, crystal)` → ТО `pickup`, `counter(value, +colour_value)`.
- КОЛИ `counter(value, >=, quota)` → ТО `sound(signal)`, `set_state(exit, open)`.
- КОЛИ `contact(robot, exit)` → ЯКЩО `state(exit, open)` → ТО `win`, `score(metals)`, `next_level`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `lose`, `lives(-1)`, `restart`.
- КОЛИ `contact(robot, shield|rad_protection)` → ТО `pickup`, `set_state(robot, protected, duration)`.
- NES: КОЛИ `adjacent(robot, radioactive)` → ТО `set_state(robot, irradiated)`; ЯКЩО `not state(protected)` → КОЛИ `timer` → `lose`.
- NES: КОЛИ `timer(grow)` → ТО `custom: «spread: бруд/лава займає сусідню клітину, перетворюючи її за таблицею»`.
- NES: КОЛИ `explode` → ЯКЩО `occupied(cell, explosive_boulder|bomb)` → ТО `explode` (ланцюг).
- NES: КОЛИ `input(start+select)` → ТО `lives(-1)`, `restart` (самознищення).
- Перемога: квота вартості + вихід до кінця часу. Поразка: демон, брила, вибух, радіація, час. Рахунок: кристали, вбивства (NES: 100–3000 залежно від істоти й способу), метали й залишок часу/бомб у кінці рівня.

## Керування і ввід
- Lynx: хрестовина — рух; A — енергетичний заряд (також старт і підтвердження коду); B — TNT; пауза → ввести код рівня.
- NES: A — заряд, B — бомба, Start — пауза, Start+Select — самознищення; вибір стартового рівня A/B на екрані «LEVEL 1».

## Вікна, меню, HUD
- `splash-screen`: титульні екрани (A або B — далі).
- `level-password`: «Enter Level Code» — A з порожнім кодом = рівень 1.
- `game-screen`: шахта зі скролом; HUD — `timer-countdown` (угорі праворуч), квота вартості (`progress-bar`, унизу праворуч), індикатор гравітації (`custom`, унизу ліворуч), `score`, `lives`, запас TNT.
- `pause-menu`: пауза; з неї — введення коду рівня.
- `game-over-continue` (NES): CONTINUE (з поточного рівня, не більше 3 разів поспіль) / END.

## Фічі поза полем
- `levels-sequential`: 150 рівнів шахти + 31 бонусний (Lynx); NES — 100 рівнів.
- `level-password`: коди рівнів з паузи.
- Перевидання: PC «Buried Treasure» CD-ROM (2000) з редактором рівнів, картридж 2003 зі 125 новими рівнями, DS/PSP/iPhone (2010), Evercade (2020).

## Варіації й родичі
- Попередник Crystal Mines (NES, 1989 (?), без ліцензії Nintendo) — багатший набір стихій (бруд, лава, радіація, 7 істот).
- Родичі: [Boulder Dash](boulder-dash.md) (квота, падіння), [Bone Cruncher](bone-cruncher.md) (теж змінна гравітація), [Emerald Mine](emerald-mine.md) (динаміт), [Mr. Do!](mr-do.md) (стрільба в копанні).
- **Осі варіацій**: знищення — «лише вибух (BD) / постріл + вибух з міцністю блоку»; квота — «кількість (BD) / сума вартостей кольорів»; гравітація — «завжди вниз / перемикачі на полі»; ворог — «видно / прикинувся брилою».

## Цікавинки для курсу
- Перемикач гравітації: та сама фізика падіння в 4 напрямках, скан залежить від напрямку — 🥉.
- Блоки з міцністю (кількість влучань / вибухів, імунітети за типом) — 📎: таблиця «тип × зброя».
- Труба: обʼєкт, штовхнутий збоку, ковзає наскрізь і може перетворитися — 📎.
- Сплячий демон-брила — 🌱: стан «спить», перехід від дотику/пострілу.
- NES: бруд і лава ростуть і перетворюють сусідів за таблицею — 🥈: клітинний автомат із кількома правилами.
- Очки за спосіб вбивства (падіння ×2–4 проти пострілу) — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` · `push-object` · `collect-quota` ↔ сума вартостей · `reach-exit` · `time-out` + `time-bonus` · `shoot-forward` ↔ енергетичний заряд · `destructible-blocks` · `explode-area` ↔ TNT · `chain-detonation` (NES вибухові брили) · `touch-death` · `environment-death` · `player-death` · `temporary-modes` ↔ щити й захисти · `status-effects` ↔ радіація · `inventory-items` ↔ TNT · `item-pickup` · `cell-transform` ↔ труби-перетворювачі · `level-password` · `sequential-levels` · `event-points` · `status-panel` + `goal-counter` · `game-pause`.
- **Нема** → пропозиції карток:
  - `+shifting-gravity` (з Bone Cruncher) — тут {by: switch}.
  - `+dormant-enemy` «Ворог прикидається обʼєктом» · entities/state · 🌱 — прокидається від дотику/пострілу.
  - `+pipe-transport` «Труба проводить обʼєкт» · entities/move · 📎 · слот {transform?}.
  - `+kill-method-bonus` «Очки за спосіб знищення» · game-logic/score · 🌱.
  - `+multi-hit-block` «Блок з міцністю» · entities/interact · 📎 · слоти {hits, immune_to} — дитина `destructible-blocks`.
  - `+blob-growth` (з BD) ↔ бруд і лава NES · `+self-destruct` (з Bone Cruncher).

## Пропозиції до словників
- `+effect:set_gravity(dir)` — повтор з Bone Cruncher (правило трьох).
- `+axis:gravity-shifting` — повтор з Bone Cruncher.
- `+ui:gravity-indicator` — куди зараз тягне гравітація.
- `+feature:self-destruct` — повтор з Bone Cruncher.

## Джерела
- ⭐ [Мануал Crystal Mines II (retroisle)](https://retroisle.com/ExtraFiles/crystalmines2_manual.txt) — A/B, коди з паузи, кольори кристалів, сплячі демони, твердий/мʼякий бруд, труби, перемикачі гравітації, метали, 150 + 31 рівень.
- [Wikipedia](https://en.wikipedia.org/wiki/Crystal_Mines_II) — розробник, дизайнер, щити й захист від радіації, дерев'яні блоки, перевидання.
- [Мануал Crystal Mines (NES)](https://patpend.net/manuals/nes/crystal_mines.txt) — таблиці міцності брил, 7 істот з очками, бруд і лава, бонуси ~14 с, 5 життів, continue ×3.
- [MobyGames](https://www.mobygames.com/game/14207/crystal-mines-ii/) — платформи.

## Непевне
- (?) Які NES-елементи (бруд, лава, радіоактивні істоти, бонуси) лишились у Lynx-версії — мануал II неповний; щит і радіація є за Wikipedia.
- (?) Чи брила вбиває робота одразу, чи знімає здоровʼя — мануал II каже «seriously damage».
- (?) Чи гравітація діє на самого робота після перемикача.
- (?) Точні вартості кристалів за кольорами і кількість пострілів для твердого бруду в II.
- (?) Чи демони переслідують робота (NES: лише газова істота «полює»).
