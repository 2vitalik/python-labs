---
title: Hexapawn (гексапішак) і машина, що вчиться на сірникових коробках
slug: hexapawn
aka: [Гексапішак, HER, Hexapawn Educable Robot, Octapawn, Октапішак, Dawson's chess]
family: chess-abstract
also: [program-robots]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 1962
platforms: [board, paper, web, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hexapawn", best: true, note: "правила 3×3, розвʼязок (білі програють за 3 ходи), MENACE і 24 коробки, Octapawn, Dawson's chess"}
  - {kind: other, url: "https://www.Gwern.net/doc/reinforcement-learning/model-free/1991-gardner-ch8amatchboxgamelearningmachine.pdf", note: "Gardner, «A Matchbox Game-Learning Machine» (Scientific American, 1962; передрук) — скан, первинне джерело HER"}
  - {kind: other, url: "https://www.mscroggs.co.uk/blog/52", note: "MENACE і HER: HER грає другою, 19 позицій, які бачить другий гравець"}
  - {kind: other, url: "https://github.com/hansklav/Hexapawn", note: "реалізація Hexapawn з навчанням (з результатів пошуку, не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hexapawn+matchbox+machine+learning", note: "пошук; збирання HER/MENACE"}
stage: v1
coverage: 65
mechanics: [piece-move-patterns, piece-capture, no-moves-left, ai-opponent, ai-random, ai-minimax, level-solver, hot-seat, cell-click, drag-drop-piece, legal-move-highlight, field-size-picker, rule-variants, state-as-data, stats-window, game-screen, end-screen, help-window, +reach-row-win, +forced-capture, +matchbox-learning, +symmetry-reduction, +learning-curve]
proposes: ["+effect:adjust_weight", "+effect:pick_weighted", "+cond:mirror_of", "+ui:policy-view", "+ui:learning-curve", "+feature:ai-learning", "+feature:ai-reset", "+axis:opponent", "+card:matchbox-learning", "+card:symmetry-reduction", "+card:learning-curve"]
author: opus
date: 2026-11-09
---

# Hexapawn — шість пішаків на дошці 3×3 і «робот» із 24 сірникових коробок, що вчиться не програвати

## Суть
Мінігра Мартіна Гарднера (Scientific American, березень 1962): у кожного три пішаки на дошці 3×3, ходять і бʼють як шахові пішаки, без подвійного кроку. Перемагає той, хто довів пішака до протилежного краю або залишив суперника без ходів. Дерево гри таке мале, що Гарднер запропонував читачам зібрати HER (Hexapawn Educable Robot) — механічного гравця за зразком MENACE Дональда Мічі: коробка на позицію, намистинка на хід, за поразку забирають намистинку. Для курсу це найменший повний приклад навчання з підкріпленням.

## Поле і час
- Дошка n×m; канон — 3×3, три пішаки кожного на ближньому до себе ряду.
- Ходять по черзі, пасу нема; білі (людина в досліді Гарднера) — першими.
- Повна інформація, сама гра детермінована; випадковість — лише у виборі ходу машиною (`random: runtime`).
- Партія — 3–5 ходів кожного (?); дерево вичерпне вручну.
- Родичі за розміром: Octapawn — 4×4 з 4 пішаками; Dawson's chess — 3×N з обовʼязковим взяттям.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пішак | piece | сторона | 1 клітина прямо вперед на порожню; бʼє на 1 по діагоналі вперед; подвійного кроку нема |
| Протилежний ряд | zone | для кожної сторони свій | пішак, що дійшов сюди, виграє партію |
| Коробка HER | container | одна на позицію, яку бачить машина | містить намистинки — по одній на кожен легальний хід у цій позиції |
| Намистинка | resource | колір = хід (стрілка-діаграма на кришці) | витягується навмання; за поразку конфіскується |
| HER (машина) | enemy | грає другою (чорними) | у свій хід бере намистинку з коробки поточної позиції й робить її хід |

## Правила (КОЛИ → ЯКЩО → ТО)
Гра:
- КОЛИ `input(move(pawn, forward))` → ЯКЩО `free(cell_ahead)` → ТО `move(pawn, forward)`, `end_turn`; інакше `block`.
- КОЛИ `input(move(pawn, diag_forward))` → ЯКЩО `occupied(cell_diag, enemy_pawn)` → ТО `move(pawn, diag_forward)`, `end_turn`; ЯКЩО `free(cell_diag)` → ТО `block`.
- КОЛИ `contact(pawn, enemy_pawn)` → ТО `disappear_b`.
- КОЛИ `reach(pawn, last_rank)` → ТО `win`.
- КОЛИ `turn_start(side)` → ЯКЩО `custom: «у сторони нема легального ходу»` → ТО `lose` (сюди ж — усі пішаки взяті); тригер-кандидат `no_moves(side)`.
- Перемога: пішак на протилежному ряду або суперник без ходів · Нічиєї нема.
- Розвʼязок 3×3: при ідеальній грі білі завжди програють за 3 ходи (напр. 1.b2 axb2 2.cxb2 c2 3.a2 c1#).

Машина HER (алгоритм Гарднера, MENACE-подібний):
- КОЛИ `turn_start(HER)` → ТО `custom: «знайти коробку з поточною позицією (дзеркальну позицію — у тій самій коробці)»`.
- КОЛИ `turn_start(HER)` → ЯКЩО `has(box, bead)` → ТО `custom: «витягти випадкову намистинку, відкласти біля коробки»` (вибір рівноймовірний серед лишених; кандидат `+effect:pick_weighted`), `move(pawn, bead.move)`, `end_turn`.
- КОЛИ `turn_start(HER)` → ЯКЩО `not has(box, bead)` → ТО `lose` (усі ходи з позиції вже «покарані» — машина здається) (?).
- КОЛИ `game_over` → ЯКЩО `custom: «HER програла»` → ТО `take(last_box, last_bead)` — покарання: конфіскувати **лише** намистинку останнього ходу.
- КОЛИ `game_over` → ЯКЩО `custom: «HER виграла»` → ТО `custom: «повернути всі відкладені намистинки в їхні коробки»` (без нагороди, як у Гарднера).
- Варіант з нагородою: КОЛИ `game_over` → ЯКЩО HER виграла → ТО `give(box, bead)` за кожен свій хід партії — ходи-переможці множаться (кандидат `+effect:adjust_weight(state, move, +1)`).

Алгоритм словами (для студента):
1. Перелічити всі позиції, у яких ходить HER (після 1-го, 2-го, 3-го ходу білих), злити дзеркальні — Гарднер дає 24 коробки.
2. У кожну коробку покласти по намистинці кожного кольору, що відповідає легальному ходу (колір ↔ стрілка на кришці).
3. Хід машини: відкрити коробку позиції → навмання витягти → зіграти.
4. Кінець партії: поразка — викинути намистинку останнього ходу; перемога — усе повернути.
5. Порожня коробка = позиція програшна → здатися; з часом порожніють і коробки на крок раніше — програш «поширюється назад» деревом.
6. Після кількох десятків партій лишаються тільки виграшні ходи: HER грає ідеально другою (бо другий гравець виграє теоретично).

Варіанти:
- **Octapawn** (4×4, 4 пішаки): за ідеальної гри виграють білі (кутовий перший хід) (?); 11 420 позицій, 2 330 356 партій; Richard L. Sites (MIT) навчав програму на FORTRAN для IBM 1620.
- **Dawson's chess** (T. R. Dawson, 1935; 3×N): КОЛИ `turn_start(side)` → ЯКЩО `custom: «є взяття»` → ТО легальні лише взяття; зводиться до імпартіальної гри .137 (нім-подібна, за Конвеєм).

## Керування і ввід
- Людина: клік/drag пішака на легальну клітину (цифрова версія); у паперовій — рух фішкою, машина «ходить» руками оператора.
- Оператор HER: знайти коробку за діаграмою на кришці, витрусити намистинку, виконати хід її кольору.
- Режими (цифрова версія): людина проти HER · HER проти HER (дві машини вчать одна одну) · людина проти людини · людина проти ідеального розвʼязувача.

## Вікна, меню, HUD
- `match-setup` (цифрова версія): хто ходить першим, суперник (людина / HER / minimax), розмір дошки (3×3 / 4×4 Octapawn / 3×N Dawson), нагорода вкл/вимк.
- `game-screen`: дошка 3×3, `turn-indicator`, `legal-move-highlight`; поруч — `policy-view`: коробка поточної позиції з намистинками-стрілками (скільки лишилось на кожен хід).
- `stats-window`: `learning-curve` — накопичені поразки HER від номера партії (крива виходить на плато), лічильник W/L.
- `custom-window` — «усі коробки» (сітка 24 мініатюр позицій з лишеними намистинками).
- `end-screen`: хто виграв і яку намистинку конфісковано.
- `help-window` — правила і пояснення навчання.
- Переходи: main-menu → match-setup → game-screen ⇄ custom-window (коробки) → end-screen → наступна партія / stats-window.

## Фічі поза полем
- `ai-learning` — машина зберігає «памʼять» між партіями (стан коробок); `ai-reset` — знову наповнити коробки й навчати з нуля.
- `autosave` стану коробок; `export-import` — стан навчання як дані.
- `speed-control` / `skip-animation` для сотень партій HER проти HER.
- `custom-rules` — розмір дошки, обовʼязкове взяття (Dawson), нагорода за перемогу.
- `hotseat` — двоє людей.

## Варіації й родичі
- [chess.md](chess.md) — пішаки звідти; [breakthrough-loa.md](breakthrough-loa.md) — Breakthrough: «дійти пішаком до краю» на великій дошці.
- [line-games.md](line-games.md) — хрестики-нулики, на яких Мічі побудував оригінальну MENACE (сотні коробок).
- [checkers.md](checkers.md) — обовʼязкове взяття як у Dawson's chess.
- **Осі варіацій**:
  - **Розмір**: 3×3 (Hexapawn) · 4×4 (Octapawn) · 3×N (Dawson) · n×m.
  - **Взяття**: за бажанням · обовʼязкове (Dawson).
  - **Навчання машини**: лише покарання (Гарднер) · покарання + нагорода · стартова кількість намистинок 1 / k на хід.
  - **Хто вчиться**: HER проти людини · HER проти HER (самогра) · проти ідеального гравця.

## Цікавинки для курсу
- Генератор ходів пішака + перемога «дійшов або суперник без ходів» на n×m — 🌱.
- Повний перебір дерева 3×3 і доказ «другий виграє» (minimax без евристик) — 📎; Octapawn 4×4 з підрахунком 11 420 позицій — 🥉.
- HER як алгоритм: таблиця «позиція → мультимножина ходів», випадковий вибір, конфіскація за поразку — 🥉 (табличне RL з нуля, без бібліотек).
- Канонізація позиції з дзеркальною симетрією (ключ коробки) — 📎.
- Крива навчання: HER проти HER або проти minimax на 1000 партій і графік поразок — 🥈.
- Перенести машину на хрестики-нулики (MENACE, 300+ коробок) чи Octapawn і порівняти швидкість навчання — 🥇.
- Dawson's chess як нім: обчислити значення Шпрага–Гранді для 3×N — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ хід/взяття пішака · `piece-capture` · `no-moves-left` ↔ поразка без ходів · `ai-opponent` / `ai-random` ↔ HER до навчання · `ai-minimax` ↔ ідеальний суперник · `level-solver` ↔ розвʼязок дерева · `hot-seat` · `cell-click` / `drag-drop-piece` · `legal-move-highlight` · `field-size-picker` ↔ 3×3 / 4×4 / 3×N · `rule-variants` ↔ Dawson · `state-as-data` ↔ ключ позиції для коробки · `stats-window` · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+matchbox-learning` «Машина, що вчиться на сірникових коробках (MENACE/HER)» · game-logic/opponent · 🥉 · слоти {reward: none|+1, beads_per_move, resign_on_empty}.
  - `+symmetry-reduction` «Злиття симетричних позицій в один ключ» · code/architecture · 📎 · слоти {symmetries: mirror|rot|both}.
  - `+learning-curve` «Графік навчання AI за партіями» · interface/results · 📎.
  - `+reach-row-win`, `+forced-capture` — див. [chess-2-sequel.md](chess-2-sequel.md), [lichess-variants.md](lichess-variants.md).

## Пропозиції до словників
- `+effect:adjust_weight(state, move, ±n)` — змінити вагу ходу в таблиці навчання (конфіскація/нагорода намистинки); загальне для будь-якого табличного AI.
- `+effect:pick_weighted(box)` — випадковий вибір з мультимножини/за вагами (хід HER; родич `rng`, але з розподілом).
- `+cond:mirror_of(pos_a, pos_b)` — позиції однакові з точністю до симетрії.
- `+ui:policy-view` — видимий «мозок» AI: варіанти ходу з вагами (намистинки в коробці).
- `+ui:learning-curve` — графік поразок/перемог AI за номером партії.
- `+feature:ai-learning` — AI змінюється між партіями й памʼятає досвід; `+feature:ai-reset` — скинути навчання.
- `+axis:opponent` — нове значення `learning-ai` (суперник, що вчиться під час серії).
- `+card:matchbox-learning` · `+card:symmetry-reduction` · `+card:learning-curve` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Hexapawn](https://en.wikipedia.org/wiki/Hexapawn) — правила n×m, перемога, розвʼязок 3×3, мета Гарднера (MENACE, 24 коробки), Octapawn (Sites, IBM 1620, 11 420 позицій), Dawson's chess (1935, .137), Scientific American 03.1962.
- [Gardner, «A Matchbox Game-Learning Machine» (PDF, скан)](https://www.Gwern.net/doc/reinforcement-learning/model-free/1991-gardner-ch8amatchboxgamelearningmachine.pdf) — первинне джерело; відкрився лише як скан без тексту; цитати «twenty-four boxes» і «confiscating only the bead that represents its last move» — з результатів пошуку.
- [Matt Scroggs: MENACE / HER](https://www.mscroggs.co.uk/blog/52) — HER грає другою; 19 позицій, які бачить другий гравець.
- YouTube: пошук «hexapawn matchbox machine learning».

## Непевне
- (?) 24 коробки (Гарднер) проти 19 позицій (Scroggs): різниця, мабуть, у тому, чи лічити позиції, де вже нема ходу або гра скінчилась, і як зливати дзеркальні — сам не перерахував.
- (?) «Порожня коробка → HER здається» — за переказами MENACE; у скані не прочитав.
- (?) Скільки партій до бездоганної гри: переказ «30–40 партій» і памʼять «11 поразок за перші 36 із 50» — не перевірено в джерелі.
- (?) Хто ходить першим у досліді Гарднера — людина білими (за Scroggs HER — другий гравець).
- (?) Octapawn: «білі виграють» у Wikipedia позначено «потрібне джерело»; тривалість партій 3×3 — оцінка.
