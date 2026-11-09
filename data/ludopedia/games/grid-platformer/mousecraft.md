---
title: MouseCraft
slug: mousecraft
aka: [Mousecraft]
family: grid-platformer
also: [falling-match, dig-gravity]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2014
platforms: [PC (Windows, macOS, Linux), Ouya, PS3, PS4, PS Vita, Switch, Xbox One]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/252750/MouseCraft/", best: true, note: "опис: 80 рівнів, 7 видів тетроміно, кришені/вибухові/желейні блоки, active pause, прискорення, редактор"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/MouseCraft", note: "платформи й дати, 80 рівнів, редактор, оцінки"}
  - {kind: other, url: "https://www.destructoid.com/reviews/review-mousecraft/", note: "рецензія: миші йдуть праворуч, лізуть на 1 блок, падають ≤3 клітин; бомби, желе, undo"}
  - {kind: other, url: "https://www.gameinformer.com/games/mousecraft/b/playstation4/archive/2014/08/05/mousecraft-game-informer-review.aspx", note: "рецензія: електроблоки й вода, кислота, бомби обмежені, відкат"}
  - {kind: other, url: "https://hardcoregamer.com/reviews/review-mousecraft/92943/", note: "рецензія: кристали як «квиток» далі, механічні миші вибухають, 4 етапи"}
  - {kind: other, url: "https://kotaku.com/now-i-know-why-lemmings-died-1601913416", note: "миші розвертаються від стіни, ідуть у прірву; прискорення"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2210833329", note: "Steam-гайд з клавішами керування"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=MouseCraft+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, turn-when-blocked, polyomino-placement, piece-rotate-flip, cursor-place, environment-death, touch-death, item-pickup, collect-all, reach-exit, game-pause, undo-redo, level-select, level-unlock, sequential-levels, in-game-editor, editor-window, player-camera, minimap-radar, leaderboard, explode-area, keyboard-controls, +auto-walker-guide, +fall-height-death, +step-climb-one, +cushion-block, +electrified-water, +bomb-remove-piece, +tool-allotment, +fast-forward, +rescue-rating, +crumbling-floor, +no-line-clear]
proposes: ["+trigger:landed", "+cond:fall_height", "+feature:active-pause", "+card:step-climb-one", "+card:cushion-block", "+card:electrified-water", "+card:bomb-remove-piece", "+card:fast-forward", "+card:rescue-rating", "+card:no-line-clear"]
author: opus
date: 2026-11-09
---

# MouseCraft — Lemmings із тетроміно: миші йдуть самі, а ти кладеш фігури, щоб довести їх до сиру

## Суть
На бічному клітинному рівні з колеса виходять три миші й безвольно крокують, розвертаючись від стін і зриваючись у прірви. Гравець не керує мишами: він ставить і обертає тетроміно з обмеженого набору, будуючи мости, сходи й стіни, і підриває блоки бомбами, щоб хоч одна миша дійшла до сиру. Спецблоки змінюють фізику: желе ловить падіння, електричні вбивають і заряджають воду, вибухові спрацьовують від дотику. Ряди тетроміно **не зникають** — фігури тут будматеріал, а не Tetris.

## Поле і час
- Квадратна сітка, бічний вид; рівні часто ширші за екран і скролляться вбік (Hardcore Gamer), є мінікарта (?).
- Real-time: миші йдуть повільно і безперервно; «active pause» (заморозка) зупиняє час, але дозволяє ставити блоки; прискорення в будь-який момент.
- Шари: рельєф рівня (стіни, вода, кислота) · покладені гравцем тетроміно · рухомі (миші, ратоїди) · предмети (кристали, сир).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Миша | ally | 3 на рівень | іде вперед (на старті — праворуч); залазить на сходинку в 1 блок; вища стіна → розворот; без опори падає; падіння > 3 клітин — смерть |
| Колесо | spawner | — | з нього виходять три миші після команди «випустити» |
| Сир | static | — | ціль: миша, що дійшла, врятована |
| Тетроміно | object | 7 видів (Steam) | гравець обирає, обертає й ставить; опора й стіна для мишей; ряди не очищаються |
| Кришений блок | object | — | руйнується (?) — правило в джерелах не описане |
| Желейний блок | object | — | падіння на нього безпечне з будь-якої висоти |
| Вибуховий блок | object | — | вибухає після контакту; вбиває мишей поруч |
| Електроблок | object | — | закриває дрібні щілини, але вбиває мишу при дотику; у воді робить її смертельною |
| Бомба | object | обмежений запас | інструмент гравця: знищує тетроміно цілком; миші в радіусі гинуть |
| Ратоїд (механічна миша) | enemy | — | «злий робот-щур»: при контакті вибухає, вбиваючи мишу; його можна знищити (досягнення «Exterminate Ratoids») |
| Вода | hazard | струм є / нема | миша тоне (Hardcore Gamer); з електроблоком — смертельна пастка |
| Кислота | hazard | — | смерть миші |
| Кристал (Anima shard) | pickup | кілька на рівень | збирають миші; потрібні для найкращої оцінки й відкриття наступних рівнів |
| Стіна рівня | static | — | непрохідна опора |
| Привид миші | mark | — | лишається на місці смерті від падіння |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(release)` → ТО `spawn_at(mouse, wheel)` — `custom: «три миші по черзі сходять з колеса»`.
- КОЛИ `tick` → ЯКЩО `supported(mouse)` і `free(front)` → ТО `move(mouse, facing)`.
- КОЛИ `blocked(mouse)` → ЯКЩО `custom: «перешкода рівно в 1 блок заввишки»` → ТО `custom: «миша вилазить на сходинку»`.
- КОЛИ `blocked(mouse)` → ЯКЩО `custom: «перешкода вища за 1 блок»` → ТО `face(mouse, reverse)`.
- КОЛИ `tick` → ЯКЩО `not supported(mouse)` → ТО `fall(mouse)`.
- КОЛИ `custom: «миша приземлилась»` → ЯКЩО `custom: «пролетіла більше 3 клітин»` і `not occupied(below, jelly_block)` → ТО `disappear(mouse)`, `spawn(ghost)`.
- КОЛИ `input(select)` → ТО `choose(piece)` з доступного набору; КОЛИ `input(rotate)` → ТО `rotate(piece, 90)`.
- КОЛИ `input(place)` → ЯКЩО `fits(piece, cells)` → ТО `place(player, piece)`.
- КОЛИ `pattern(row_full)` → ТО `custom: «нічого — ряди не зникають»`.
- КОЛИ `input(bomb)` → ЯКЩО `counter(bombs, >, 0)` → ТО `disappear(tetromino)` цілком, `counter(bombs, -1)`; ЯКЩО `in_range(blast, mouse, r)` → ТО `disappear(mouse)`.
- КОЛИ `contact(mouse, electric_block)` → ТО `disappear(mouse)`.
- КОЛИ `enter(electric_block, water)` → ТО `set_state(water, electrified)`.
- КОЛИ `enter(mouse, water)` → ЯКЩО `state(water, electrified)` → ТО `disappear(mouse)`; без струму — тоне (?), див. «Непевне».
- КОЛИ `enter(mouse, acid)` → ТО `disappear(mouse)`.
- КОЛИ `contact(mouse, explosive_block)` → ТО `explode(area, n, empty)` — гинуть миші поруч.
- КОЛИ `contact(mouse, ratoid)` → ТО `explode(area, n, empty)`, `disappear(mouse)`.
- КОЛИ `contact(mouse, anima_shard)` → ТО `pickup`, `counter(shards, +1)`.
- КОЛИ `reach(mouse, cheese)` → ТО `counter(saved, +1)`.
- КОЛИ `count(mouse, ==, 0)` → ЯКЩО `counter(saved, >=, 1)` → ТО `win`; інакше `restart`.
- КОЛИ `input(freeze)` → ТО `custom: «час стоїть; вибір і установка блоків дозволені»`.
- КОЛИ `input(speed)` → ТО `speed(all, ×k)` — перемикач «нормально / швидко».
- КОЛИ `input(undo)` → ТО `undo(1)` — `custom: «відкат до попередньої точки рішення; миші йдуть з неї знову»`.
- Перемога: ≥1 миша на сирі. Найкраща оцінка («gold»): усі 3 миші + усі кристали. Поразка: жодної врятованої → рестарт без меню. Рахунок: оцінка рівня за мишами й кристалами; таблиці лідерів Steam.

## Керування і ввід
- ПК (Steam-гайд): A/D — вибір фігури; Enter / ЛКМ — взяти блок під курсором; WASD — рух блоку; Пробіл / ПКМ — поворот; R — випустити мишей, далі перемикає швидкість; E — швидкість; F — заморозка; Shift — режим бомби; ←/→ — рух мінікарти (?).
- Консолі: «двокнопкове» керування (Game Informer).
- Миші керуються лише непрямо: рельєфом, який будує гравець.

## Вікна, меню, HUD
- `main-menu` (?) → `level-select`: 4 локації, 80 рівнів; наступні відкриваються кристалами.
- `game-screen` — рівень зі скролом, колесо і сир; HUD: `element-picker` (набір доступних тетроміно), лічильник бомб, кристалів і мишей (?), кнопки заморозки/швидкості/undo, `minimap` (?).
- `end-screen` — результат рівня з оцінкою (gold за ідеал).
- `editor-window` — редактор рівнів.
- `leaderboard` — таблиці лідерів Steam.
- Переходи: level-select → game-screen → (усі миші вийшли) → end-screen → наступний рівень / повтор.

## Фічі поза полем
- `pause` у формі active pause (заморозка зі змогою будувати), `speed-control` (прискорення), `undo`, `restart-level` без завантаження.
- `levels-sequential` + `level-unlock` кристалами (Hardcore Gamer: «нема кристалів — повертайся й грай ще»), `stars-rating` (gold-оцінка).
- `level-editor`; Steam обіцяє обмін картами зі спільнотою, Destructoid на старті писав «поділитися поки не можна».
- `achievements` (Steam, зокрема «знищ ратоїдів»), `cloud-save`, `leaderboard-online`.

## Варіації й родичі
- Порти: Ouya, PS3/PS4/Vita (2014), Switch (2020), Xbox One (2022); сюжетна рамка — кіт-вчений Шредінгер і його мишачий винахід.
- Родичі: Lemmings (безвольні ходоки, рятувати частину), Troddlers (ходоки + блоки гравця), Tetris (форма фігур, але без очищення рядів), Pushover, Toki Tori.
- Осі: **чим керуємо ходоками** (навички — Lemmings / блоки-рельєф — MouseCraft, Troddlers / стрілки-клітини); **що лишає фігура** (ряд зникає / лишається як будматеріал); **поріг безпечного падіння** (нема / N клітин / амортизатор-клітина).

## Цікавинки для курсу
- Ходок «вперед; сходинка 1 — залізти; вище — розворот; без опори — падати» — 📎: класичний автомат для бічних сіток.
- Безпечна висота падіння + блок-амортизатор (желе) — 📎.
- Установка тетроміно з поворотом і перевіркою вільних клітин (без гравітації й очищення рядів) — 🥉.
- Електроблок, що змінює стан води (комбінація двох властивостей у третю) — 📎.
- Active pause: час стоїть, будувати можна — 🌱, але цікаво в real-time архітектурі.
- Оцінка рівня за кількома метриками (миші + кристали) і розблокування за накопиченими кристалами — 📎.

## Мапа на каталог
- Є: `gravity-fall` · `turn-when-blocked` (розворот від стіни) · `polyomino-placement` · `piece-rotate-flip` · `cursor-place` · `environment-death` (падіння, вода, кислота) · `touch-death` (електро, ратоїд) · `item-pickup` + `collect-all` (кристали) · `reach-exit` (сир) · `game-pause` · `undo-redo` · `level-select` · `level-unlock` · `sequential-levels` · `in-game-editor` · `editor-window` · `player-camera` · `minimap-radar` · `leaderboard` · `explode-area` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+auto-walker-guide` (Troddlers), `+fall-height-death` (Lemmings), `+tool-allotment` (Lemmings), `+crumbling-floor` (Manic Miner) — повтори наявних пропозицій.
  - `+step-climb-one` «Ходок залазить на сходинку в 1 клітину» · entities/move · 🌱.
  - `+cushion-block` «Клітина-амортизатор скасовує смерть від падіння» · entities/interact · 🌱.
  - `+electrified-water` «Провідник робить воду смертельною» · entities/interact · 📎.
  - `+bomb-remove-piece` «Бомба знищує всю фігуру» · entities/combat · 📎 — не клітину, а весь тетроміно.
  - `+fast-forward` «Прискорення симуляції» · game-logic/flow · 🌱.
  - `+rescue-rating` «Оцінка за врятованими й зібраним» · game-logic/score · 🌱.
  - `+no-line-clear` «Фігури Tetris без очищення рядів» · entities/legality · 🌱.

## Пропозиції до словників
- `+trigger:landed` — сутність приземлилась (перевірка висоти падіння).
- `+cond:fall_height` — висота щойно завершеного падіння порівняно з N.
- `+feature:active-pause` — пауза, під час якої дозволені дії гравця (будівництво).
- `+card:step-climb-one`, `+card:cushion-block`, `+card:electrified-water`, `+card:bomb-remove-piece`, `+card:fast-forward`, `+card:rescue-rating`, `+card:no-line-clear` — див. вище.

## Джерела
- ⭐ [Steam: MouseCraft](https://store.steampowered.com/app/252750/MouseCraft/) — опис: 80 рівнів у 4 локаціях, 7 видів тетроміно, кришені/вибухові/желейні блоки, 2 типи небезпек середовища, бомби, вороги, active pause, прискорення, редактор; реліз 8.07.2014, Crunching Koalas.
- [Wikipedia: MouseCraft](https://en.wikipedia.org/wiki/MouseCraft) — платформи й дати (Switch 2020, Xbox One 2022), 80 рівнів, редактор.
- [Destructoid](https://www.destructoid.com/reviews/review-mousecraft/) — 3 миші з колеса, рух праворуч, підйом на 1 блок, безпечне падіння до 3 клітин, бомби на цілу фігуру, желе, undo, ряди не зникають.
- [Game Informer](https://www.gameinformer.com/games/mousecraft/b/playstation4/archive/2014/08/05/mousecraft-game-informer-review.aspx) — електроблоки й вода, кислота, вибухові блоки, обмежені бомби, автоматичний відкат.
- [Hardcore Gamer](https://hardcoregamer.com/reviews/review-mousecraft/92943/) — кристали як умова прогресу, механічні миші вибухають, вода (тонуть), скрол рівнів, 4 етапи.
- [Kotaku](https://kotaku.com/now-i-know-why-lemmings-died-1601913416) — розворот від стіни, падіння в прірву, мета — хоч одна миша.
- [Steam-гайд: клавіші](https://steamcommunity.com/sharedfiles/filedetails/?id=2210833329) — розкладка ПК.

## Непевне
- (?) Поведінка кришеного блоку (кришиться під мишею? за часом?) — у доступних джерелах лише назва.
- (?) «7 types of Tetromino bricks» — 7 форм (I O T S Z J L) чи 7 матеріалів; електроблок у переліку Steam не названий, але є в рецензіях.
- (?) Вода без струму: Hardcore Gamer — «миші тонуть», Game Informer — «смертельною її робить електроблок».
- (?) Як знищити ратоїда (бомбою? блоком згори?) — відомо лише, що є досягнення «Exterminate Ratoids».
- (?) Чи падають покладені тетроміно, чи висять там, де поставлені (мости через прірви натякають, що висять).
- (?) Мінікарта й точна розкладка: Steam-гайд прихований і позначений як несумісний із грою; кількість мишей «≥1 для перемоги» — з Kotaku.
- (?) Undo: Destructoid — кнопка undo, Game Informer — відкат «не керується вручну, часом далі, ніж хотілось».
