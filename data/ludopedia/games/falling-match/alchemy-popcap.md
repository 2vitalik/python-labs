---
title: Alchemy (PopCap)
slug: alchemy-popcap
aka: [Alchemy, Alchemy Deluxe, PopCap Alchemy]
family: falling-match
also: [board-digital]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: partial
  random: runtime
  goal: state
year: 2001
platforms: [web, PC, Mac]
links:
  - {kind: other, url: "https://gameyum.com/free-retro-games/65868-popcap-alchemy-review", best: true, note: "огляд: поле 8×9 зі свинцю, руна перетворює клітину на золото, сусідство за кольором або символом, wildcard, руйнівна фігура, скидання (≤3 поспіль), очищення рядка/стовпця, звичайний і time attack, 3 складності"}
  - {kind: other, url: "https://www.giantbomb.com/games/3030-10352/", note: "Giant Bomb: Alchemy Deluxe (бачено в пошуку; WebFetch 403)"}
  - {kind: other, url: "https://www.mobygames.com/game/30884/alchemy-deluxe/", note: "MobyGames: Alchemy Deluxe (бачено в пошуку; WebFetch 403)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=PopCap+Alchemy+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cursor-place, cell-click, hover-highlight, next-queue, spawn-random-cell, no-moves-left, event-points, score-records, time-out, difficulty-levels, difficulty-select, mode-select, sequential-levels, game-screen, end-screen, main-menu, +line-clear, +adjacency-match-placement, +wild-tile, +remove-any-tile, +discard-limit, +paint-on-place-goal]
proposes: ["+effect:discard", "+cond:neighbors_match", "+trigger:all_painted", "+ui:forge-meter", "+card:adjacency-match-placement", "+card:discard-limit", "+card:paint-on-place-goal"]
author: opus
date: 2026-11-09
---

# Alchemy (PopCap) — клади руни поруч зі схожими за кольором чи символом; кожна клітина під руною стає золотом, повний ряд очищується

## Суть
Поле зі «свинцевих» клітин; гравець по одній отримує випадкові руни (алхімічні символи різних кольорів) і кладе їх на порожні клітини поруч із вже покладеними. Сусіди мусять збігатися з новою руною **за кольором або за символом**. Клітина під покладеною руною назавжди стає золотою; повністю заповнений рядок чи стовпець очищується від рун (золото лишається), звільняючи місце. Рівень пройдено, коли золоте все поле; невдалі руни можна скинути в кузню, але не безкінечно поспіль. Ліній тут не «складають», як у match-3, — їх заповнюють, як у [block-blast](block-blast.md), а легальність задає сусідство.

## Поле і час
- Поле 8×9 клітин (огляд gameyum); дві властивості клітини: золото/свинець і руна/порожньо.
- Хід = покласти поточну руну або скинути її; без падіння й поповнення поля.
- Звичайний режим без часу; time attack — таймер (?).
- Видно лише поточну руну (`info: partial` — наступні не відомі) (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина-свинець | terrain | — | порожня, ще не золота |
| Клітина-золото | terrain | — | стала золотою під руною; лишається такою після очищення |
| Руна | tile | колір, символ | кладеться поруч із покладеною; усі сусіди мають збігатися кольором або символом |
| Камінь-wildcard | tile | — | сусідство з ним дозволяє класти будь-яку руну (?) |
| Череп (руйнівна фігура) | pickup | — | замість руни; прибирає будь-яку обрану руну з поля |
| Кузня (forge) | container | рівень заповнення | приймає скинуті руни; переповнення = кінець гри |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО `spawn(random_rune)` у слот поточної руни; кольорів і символів більше на пізніх рівнях.
- КОЛИ `input(click cell)` → ЯКЩО `free(cell)` and `adjacent_count(cell, rune, >=, 1)` and `custom: «кожен сусід збігається з руною кольором або символом, або це wildcard»` (+cond:neighbors_match) → ТО `place(rune, cell)`, `set_cell(cell, gold)`, `score(n)`; інакше `block`.
- КОЛИ `input(click cell)` → ЯКЩО `custom: «поточна фігура — wildcard»` → ТО `place(stone, cell)` (?).
- КОЛИ `input(click rune)` → ЯКЩО `custom: «поточна фігура — череп»` → ТО `disappear_b` (обрана руна зникає).
- КОЛИ `input(discard)` → ТО `custom: «руну скинуто в кузню»` (+effect:discard), `counter(forge, +1)`.
- КОЛИ `counter(forge, >, 3)` → ТО `lose` — більше трьох скидань поспіль не можна.
- КОЛИ `custom: «використано wildcard або череп»` → ТО `counter(forge, −1)` (?).
- КОЛИ `pattern(row_full)` або `custom: «col_full»` → ТО `clear(line)`, `score(bonus)`; клітини лишаються золотими; кузня спорожніє (?).
- КОЛИ `no_moves(player)` → ЯКЩО `counter(forge, ==, max)` → ТО `lose`; інакше руну доведеться скинути.
- КОЛИ `custom: «усі клітини золоті»` (+trigger:all_painted) → ТО `next_level` (більше кольорів/символів).
- Time attack: КОЛИ `timer(==, 0)` → ТО `lose` (?).
- Рахунок: очки за кожну покладену руну + бонус за очищений рядок/стовпець; таблиця рекордів.

## Керування і ввід
- Миша: клік по порожній клітині — покласти руну; клік по кузні — скинути (?); з черепом — клік по руні, яку прибрати.
- Підсвітка клітини під курсором (?).

## Вікна, меню, HUD
- `game-screen`: поле 8×9, поточна руна, кузня зі шкалою скидань (`forge-meter`), `score`, `level-number`.
- `main-menu` → `mode-select` (звичайний / time attack) → `difficulty-select` (3 рівні: старт з пізнішого поля).
- `end-screen` з очками → `leaderboard` (рекорди) (?).
- `help-window` (?).

## Фічі поза полем
- `mode-classic` (без часу) і `mode-time-attack`; `difficulty-presets` ×3 — вища складність стартує з пізнішого поля з більшою кількістю кольорів і символів.
- `levels-sequential` — поле за полем до програшу; `leaderboard-local`.

## Варіації й родичі
- Deluxe-видання (Alchemy Deluxe) — та сама механіка (?).
- Родичі в корпусі: [block-blast](block-blast.md) (кладеш фігури, повні лінії очищаються), [lines-98](lines-98.md) (поле як ресурс), [tantrix](../connect-rotate/tantrix.md) і доміно-ігри (легальність за сусідами), [triple-town](triple-town.md) (одна випадкова фігура на хід).
- **Осі варіацій**: легальність (будь-де / поруч із чимось / усі сусіди збігаються за ознакою) · ознаки збігу (1 / 2 — колір або символ) · мета (очки / зафарбувати все поле) · вихід із глухого кута (скидання з лімітом / руйнівна фігура / wildcard).

## Цікавинки для курсу
- Перевірка легальності: усі 4-сусіди збігаються кольором або символом, хоча б один сусід є — 🌱.
- Два шари клітини (золото + руна) і мета «все поле золоте» — 🌱.
- Очищення повних рядків і стовпців одночасно — 🌱.
- Кузня з лімітом скидань поспіль і знижкою за спецфігури — 📎.
- Генерація руни з урахуванням рівня (більше кольорів/символів) і перевірка, чи є хоч одне легальне місце — 📎.

## Мапа на каталог
- Є: `cursor-place` · `cell-click` · `hover-highlight` · `next-queue` (поточна руна) · `spawn-random-cell` (випадкова руна) · `no-moves-left` · `event-points` · `score-records` · `time-out` · `difficulty-levels` · `difficulty-select` · `mode-select` · `sequential-levels` · `game-screen` · `end-screen` · `main-menu`.
- Повтор чужих: `+line-clear` (Block Blast).
- **Нема** → пропозиції карток:
  - `+adjacency-match-placement` «Постав, якщо всі сусіди збігаються за ознакою» · entities/legality · 🌱 · слоти {ознаки}.
  - `+wild-tile` «Плитка-джокер» · entities/legality · 🌱.
  - `+remove-any-tile` «Фігура, що прибирає обрану плитку» · entities/interact · 🌱.
  - `+discard-limit` «Скидання з лімітом поспіль» · game-logic/lose · 📎.
  - `+paint-on-place-goal` «Клітина фарбується назавжди, мета — усе поле» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+effect:discard(a)` — скинути поточну фігуру замість ходу.
- `+cond:neighbors_match(cell, a, props)` — кожен зайнятий сусід збігається з A хоча б за однією ознакою.
- `+trigger:all_painted(kind)` — усі клітини поля мають стан/колір (золото).
- `+ui:forge-meter` — шкала скидань поспіль.

## Джерела
- ⭐ [gameyum: PopCap Alchemy review](https://gameyum.com/free-retro-games/65868-popcap-alchemy-review) — поле 8×9, свинець → золото, сусідство за кольором/символом, wildcard і руйнівна фігура, ≤3 скидань поспіль, очищення ряду/стовпця, режими й складності.
- Результати WebSearch (сніпети Giant Bomb, Wikipedia-дзеркала, Softpedia) — кузня (forge), камінь-wildcard, череп прибирає руну, 4 скидання поспіль = кінець, wildcard/череп знижують кузню.
- [Giant Bomb](https://www.giantbomb.com/games/3030-10352/), [MobyGames](https://www.mobygames.com/game/30884/alchemy-deluxe/) — бачено в пошуку, не відкрились (403).

## Непевне
- (?) «Усі сусіди мусять збігатися» (дзеркало Wikipedia) чи «поруч із хоча б однією схожою» (gameyum) — джерела формулюють по-різному.
- (?) Камінь-wildcard: чи стоїть на старті поля, чи випадає як фігура; чи його можна класти будь-де.
- (?) Скидання: «≤3 поспіль» і «4 поспіль = кінець» — узгоджено як ліміт 3; чи очищення лінії спорожняє кузню — з одного сніпета.
- (?) Число кольорів і символів, очки, тривалість time attack — не названо.
- (?) Чи видно наступну руну — не бачив.
- (?) Вікна й керування кузнею — з загальних знань про жанр.
