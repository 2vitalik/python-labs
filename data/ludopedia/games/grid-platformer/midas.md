---
title: Midas (Wanderlands)
slug: midas
aka: [Midas PuzzleScript]
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2013
platforms: [web (PuzzleScript)]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=6878337", best: true, note: "грати в браузері; 15 рівнів"}
  - {kind: other, url: "https://gist.github.com/anonymous/6878337", note: "вихідний скрипт PuzzleScript: обʼєкти, правила, рівні — повна специфікація механіки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Midas+puzzlescript+wanderlands+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 85
mechanics: [move-by-input, gravity-fall, coverage-area, cell-transform, reach-exit, undo-unlimited, restart-level, level-from-txt, sequential-levels, sound-effects, game-screen, keyboard-controls, +jump-arc-states, +midas-touch-aura, +item-loss-hazard, +goal-forbids-item, +spoilable-goal]
proposes: ["+card:midas-touch-aura", "+card:jump-arc-states", "+card:item-loss-hazard", "+card:goal-forbids-item", "+card:spoilable-goal"]
author: opus
date: 2026-11-09
---

# Midas (Wanderlands) — корона перетворює стіни поруч на золото, що падає; щоб обійняти кохану, корону треба втопити

## Суть
Бічна кімната-пазл: цар Мідас у короні ходить і підстрибує, а кожна стіна, якої торкається корона (4 сусіди аватара), за хід буріє і стає золотим блоком, що падає вниз. Так гравець «розбирає» підлогу й стіни під собою, будує сходи з золота й скидає блоки в ями. Мета — опинитись поруч із жінкою, але без корони: торкнувшись її в короні, Мідас перетворює кохану на золото (рівень зіпсовано), а корону змиває лише вода. Порт однойменної гри Wanderlands у PuzzleScript (2013) з дозволу авторів.

## Поле і час
- Квадратна сітка, бічний вид; рівні від 14×6 до 21×17 клітин (15 рівнів, підраховано за скриптом). Камери нема — рівень на весь екран.
- Покроково: тік = одне натискання. Гравець, що стоїть на землі без опори, падає до опори **в межах того ж ходу**; золоті блоки й жінка падають **на 1 клітину за хід** — дві різні моделі гравітації в одній грі.
- Шари PuzzleScript: фон · тверді обʼєкти (гравець, стіна, вода, золото, жінка) · корона (окремий шар над гравцем) · серце (маркер перемоги).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мідас | player | стан ground / jump2 / jump1 | ходить уліво-вправо; стрибок на 1 вгору, далі до 2 кроків убік у повітрі; без опори падає |
| Корона | object | є / змита | шар над гравцем, переходить за ним щоходу; перетворює сусідні стіни; змивається водою назавжди |
| Стіна | static | — | непрохідна; поруч із короною → «золотіє» |
| Золотіюча стіна | object | живе 1 хід | проміжний стан (коричнева); наступного ходу стає золотим блоком |
| Золотий блок | object | — | непрохідний, падає на 1 клітину за хід; опора для Мідаса; повторно не перетворюється |
| Вода | hazard | — | непрохідна; корона поруч з водою зникає |
| Жінка | neutral | жива / золота | ціль рівня; непрохідна; падає, як золото; поруч із короною → золота статуя |
| Золота жінка | object | — | «зіпсована» ціль: падає, перемогу вже не дає |
| Серце | mark | — | зʼявляється над Мідасом, коли він поруч із живою жінкою без корони; = перемога |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `state(midas, ground)` і `free(next)` → ТО `move(midas, dir)`; інакше `block`.
- КОЛИ `input(up)` → ЯКЩО `state(midas, ground)` і `free(above)` → ТО `move(midas, up)`, `set_state(midas, jump2)`.
- КОЛИ `input(up)` → ЯКЩО `state(midas, jump1|jump2)` і `free(below)` → ТО `block` — подвійного стрибка нема.
- КОЛИ `input(left|right)` → ЯКЩО `state(midas, jump2)` і `free(next)` → ТО `move(midas, dir)`, `set_state(midas, jump1)`.
- КОЛИ `input(left|right)` → ЯКЩО `state(midas, jump1)` і `free(next)` → ТО `move(midas, dir)`, `set_state(midas, ground)` — далі падіння.
- КОЛИ `after(move)` → ЯКЩО `state(midas, ground)` і `free(below)` → ТО `fall(midas)` до опори в межах ходу.
- КОЛИ `after(move)` → ЯКЩО `state(midas, jump1|jump2)` і `occupied(below, obstacle)` → ТО `set_state(midas, ground)` — приземлився на виступ.
- КОЛИ `turn_end(player)` → ЯКЩО `free(below)` → ТО `move(gold|lady|gold_lady, down)` — по 1 клітині за хід.
- КОЛИ `after(move)` → ТО `custom: «корона переноситься в клітину Мідаса»`.
- КОЛИ `turn_end(player)` → ЯКЩО `occupied(here, golding_wall)` → ТО `transform(golding_wall, gold_block)`.
- КОЛИ `adjacent(crown, wall)` → ТО `transform(wall, golding_wall)` — усі 4 сусіди, включно зі стіною під ногами й над головою.
- КОЛИ `adjacent(crown, water)` → ТО `disappear(crown)` — назавжди, повернути не можна.
- КОЛИ `adjacent(crown, lady)` → ТО `transform(lady, gold_lady)` — рівень стає нерозвʼязним (лише undo/рестарт).
- КОЛИ `adjacent(midas, lady)` → ЯКЩО `not has(midas, crown)` і `state(lady, alive)` → ТО `spawn(heart, above_midas)`, `win`, `next_level`.
- Порядок фази late: спершу «золотіюча → золото», потім «стіна біля корони → золотіюча», потім вода/жінка біля корони, і лише тоді перевірка перемоги — тому в короні обійняти не вийде: жінка золотіє раніше, ніж спрацює перевірка.
- Перемога: серце над Мідасом (поруч із живою жінкою без корони). Поразка: формальної нема — зіпсована жінка, застряглий без корони Мідас чи завалений прохід → undo/рестарт. Рахунку нема.

## Керування і ввід
- Стрілки / WASD: вліво-вправо — крок; вгору — стрибок (лише з землі); вниз — крок униз у повітрі (?).
- Стандарт PuzzleScript: Z — undo (без ліміту), R — рестарт рівня, Esc — меню; клавіша дії (X) у правилах не задіяна.
- Між рівнями — текстові інтермедії (короткі рядки історії Мідаса), закриваються будь-якою клавішею.

## Вікна, меню, HUD
- `splash-screen` / `main-menu` — титул PuzzleScript: «Midas by wanderlands», Start / Continue.
- `game-screen` — лише поле, без HUD: усе видно з самого поля (корона на голові = стан «з короною»).
- `custom-window` — текстова інтермедія («message») між рівнями.
- `end-screen` — фінальне повідомлення після 15-го рівня.
- Переходи: main-menu → game-screen рівня → (серце) → message → наступний рівень; Esc → main-menu.

## Фічі поза полем
- `undo` (∞ кроків), `restart-level`, `levels-sequential` з автозбереженням поточного рівня браузером (стандарт PuzzleScript, `continue`).
- Звук на події: дотик корони до води, золотіння стіни, золотіння жінки, кінець рівня.
- Рівні — текстові мапи у скрипті (`level-from-txt`): `#` стіна, `W` вода, `G` золото, `D` золотіюча, `T` жінка, `P` Мідас у короні.

## Варіації й родичі
- Оригінал — гра Wanderlands «Midas»; порт у PuzzleScript автор назвав «трохи безладним». Відмінності від оригіналу — (?).
- Родичі: Solomon's Key (створює/руйнує блоки поруч), Catrap і Block Dude (покрокова гравітація в бічній кімнаті), Lode Runner (руйнування підлоги під собою), Toki Tori.
- Осі варіацій: **що робить аура аватара** (нічого / руйнує / перетворює на обʼєкт, що падає); **модель стрибка** (нема / автомат станів «1 вгору + N убік» / фізика); **предмет-ключ навпаки** (предмет треба не здобути, а позбутися перед фіналом).

## Цікавинки для курсу
- Аура навколо аватара (4 сусіди) з перетворенням із затримкою в 1 хід — 📎: два проходи по сітці, порядок важливий.
- Стрибок як автомат станів `ground → jump2 → jump1 → ground` у покроковій грі — 🥉: класичний патерн «стан визначає дозволені ходи».
- Дві гравітації: миттєве падіння гравця й покрокове падіння блоків — 🥉 (дві черги оновлення).
- Незворотна втрата предмета (корона змита) як перемикач фаз рівня «будуй → позбудься → дійди» — 🌱.
- Ціль, яку можна зіпсувати, і виявлення нерозвʼязного стану з підказкою «тільки undo» — 🥈 (детектор dead state).
- Порядок late-правил як частина геймдизайну (чому в короні обійняти неможливо) — 📎.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `coverage-area` (корона діє на 4 сусідів) · `cell-transform` (стіна → золото) · `reach-exit` (дійти до жінки) · `undo-unlimited` · `restart-level` · `level-from-txt` · `sequential-levels` · `sound-effects` · `game-screen` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+midas-touch-aura` «Аура перетворює сусідні клітини» · entities/interact · 📎 · слоти {shape: 4|8, from, into, delay} — стіни → падаючі блоки.
  - `+jump-arc-states` «Стрибок як автомат станів у покроковій грі» · entities/move · 🥉 · слоти {up, side_steps}.
  - `+item-loss-hazard` «Клітина забирає предмет назавжди» · entities/interact · 🌱 — вода змиває корону.
  - `+goal-forbids-item` «Фінал лише без предмета» · game-logic/win · 🌱 — обійняти можна тільки без корони.
  - `+spoilable-goal` «Ціль, яку можна зіпсувати» · game-logic/lose · 📎 — жінка → золото, рівень нерозвʼязний.

## Пропозиції до словників
- `+card:midas-touch-aura`, `+card:jump-arc-states`, `+card:item-loss-hazard`, `+card:goal-forbids-item`, `+card:spoilable-goal` — див. вище.
- Вісь `gravity` (вже є в classes.md) тут = `per-type`: гравець падає миттєво, блоки й жінка — по 1 клітині за хід; нового слова не треба.

## Джерела
- ⭐ [PuzzleScript: Midas](https://www.puzzlescript.net/play.html?p=6878337) — грати в браузері, 15 рівнів.
- [Gist 6878337](https://gist.github.com/anonymous/6878337) — повний скрипт (OBJECTS, LEGEND, RULES, WINCONDITIONS «some love», LEVELS); з нього взято всі правила й порядок late-фази; дата створення 2013-10-08.
- YouTube: пошук «Midas puzzlescript wanderlands gameplay».

## Непевне
- (?) Рік і платформа оригіналу Wanderlands: адреса з коментаря скрипту не віддала вмісту; рік у шапці — дата порту (2013).
- (?) Чи відрізняються правила оригіналу (скрипт — «порт з дозволу», без переліку змін).
- (?) Що робить «вниз» у стрибку: окремого правила нема, тож рух униз, мабуть, звичайний (стан стрибка лишається до опори).
- (?) Чи може Мідас у стані jump «висіти» без кінця, якщо не тиснути вбік: правила падіння для jump-станів у скрипті нема — висновок з коду, у грі не перевірено.
