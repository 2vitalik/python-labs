---
title: Toon Blast
slug: toon-blast
aka: [Toy Blast]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 2017
platforms: [iOS, Android]
links:
  - {kind: other, url: "https://www.pocketgamer.com/toon-blast/toon-blast-cheats-tips-and-tricks/", best: true, note: "Pocket Gamer: Rocket 5 / Bomb 7 / Disco 9, комбінації двох спец, фізика падіння"}
  - {kind: other, url: "https://www.levelwinner.com/?p=11479", note: "Level Winner (2017): комбо, ліміт ходів без таймера, зірки й скрині, бустери Dice/Glove/Anvil, команди з 20 рівня"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Toon_Blast", note: "редирект на Peak Games: розробник, Toy Blast 2015 → Toon Blast 2017, Android/iOS"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=toon+blast+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cell-click, gravity-fall, spawn-random-cell, chain-reaction, chain-detonation, explode-area, move-limit, collect-quota, goal-counter, sequential-levels, level-unlock, inventory-items, round-currency, shop-window, end-screen, +connected-group-pop, +group-size-specials, +tap-activate-special, +special-combos, +star-thresholds, +stamina-energy, +team-lives-request, +milestone-chest, +reshuffle-booster]
proposes: ["+ui:special-preview", "+window:chest-reward", "+card:group-size-specials", "+card:milestone-chest", "+card:reshuffle-booster"]
author: opus
date: 2026-11-09
---

# Toon Blast — SameGame у форматі рівнів-цілей: тап по групі однакових кубиків, велика група стає ракетою, бомбою чи диско-кулею

## Суть
Ядро — **tap-to-blast** як у SameGame (`samegame-flood`): дотик по звʼязній групі однакових кубиків прибирає її, решта падає. Але все інше — з `candy-crush`: **рівні з цілями** (зібрати N кубиків кольору / прибрати перешкоди), **ліміт ходів**, поповнення згори без кінця й **спецплитки за розміром групи**: 5 → Rocket, 7 → Bomb, 9+ → Disco Ball. Спецплитки активуються дотиком і підривають одна одну ланцюгом; дві поруч дають комбінацію. Порівняно з Bejeweled тут не треба шукати обмін — питання лише в тому, **яку групу підірвати першою**, щоб вирости більшу.

## Поле і час
- Прямокутне поле кубиків кількох кольорів довільної форми (?) з перешкодами.
- Покроково: хід = тап; без таймера, лише ліміт ходів (Level Winner).
- Після вибуху — падіння вниз і поповнення згори (на відміну від SameGame, поле не порожніє й стовпці не зсуваються вліво).
- Звʼязність — 4-сусідство (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кубик | tile | колір | у звʼязній групі ≥ min однакових → лопається за тап; падає |
| Rocket | tile | напрям (випадковий) | з групи 5; тап — чистить увесь рядок або стовпець |
| Bomb | tile | — | з групи 7; тап — чистить 8 сусідніх клітин (3×3) |
| Disco Ball | tile | колір | з групи 9+; тап — прибирає всі кубики свого кольору |
| Перешкоди | hazard | шари (?) | знищуються вибухами поруч; частина — ціль рівня (?) |
| Зірка | resource | 1–3 за рівень (?) | накопичується в Star Chest |
| Монети | resource | — | купують ходи, життя, бустери |
| Життя | resource | відновлюються повільно | −1 за програний рівень; запит у команди |
| Бустери in-game (Dice, Boxing Glove, Anvil) | supply | запас | Dice — перемішати поле; Glove — прибрати рядок; Anvil — прибрати стовпець |
| Toon Chest / Star Chest | container | бустери, монети | Toon Chest — кожні 10 рівнів; Star Chest — за накопичені зірки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap cell)` → ЯКЩО `connected(group)` and `region_size(group, ≥, min)` (min 2 (?)) → ТО `clear(group)`, `counter(moves, −1)`; одиночний кубик — тап не діє.
- КОЛИ `input(tap cell)` → ЯКЩО `region_size(group, ≥, 5)` → ТО `clear(group)`, `spawn_at(rocket, tapped_cell)`; `≥ 7` → `spawn_at(bomb)`; `≥ 9` → `spawn_at(disco_ball)`.
- КОЛИ `input(tap special)` → ТО спрацьовує: rocket → `clear(row|col)`; bomb → `explode(3×3)`; disco_ball → `custom: «clear_color — усі кубики свого кольору»`; `counter(moves, −1)`.
- КОЛИ `after(clear)` → ЯКЩО `occupied(area, special)` → ТО спецплитка в зоні ураження спрацьовує (`chain-detonation`).
- КОЛИ `input(tap special)` → ЯКЩО `adjacent(special, special)` → ТО комбінація: rocket + rocket → `clear(row and col)` · bomb + bomb → `explode(більша площа)` · disco + disco → `clear(all)`; rocket + bomb, disco + rocket|bomb — (?).
- КОЛИ `after(clear)` → ТО `fall(cubes)`, `spawn_at(random_cube, top)`; падіння відкриває більші групи (Pocket Gamer: «чистити знизу»).
- КОЛИ `after(clear)` → ЯКЩО `adjacent(obstacle, group)` → ТО `custom: «layer_down — перешкода втрачає шар / зникає»` (?).
- КОЛИ `counter(goals, ==, done)` → ТО `win`, `give(star)`; менше ходів витрачено → більше зірок (?).
- КОЛИ `counter(moves, ==, 0)` → ЯКЩО `not custom: «цілі виконано»` → ТО `lose`, `lives(−1)`; продовження за монети (?).
- КОЛИ `input(booster dice)` → ТО `custom: «reshuffle»`; glove → `clear(row)`; anvil → `clear(col)` — без витрати ходу (?).
- КОЛИ `level_end` → ЯКЩО `level(%, 10)` → ТО `give(toon_chest)`; КОЛИ `counter(stars, ≥, chest_cost)` → ТО `give(star_chest)` (з 15 рівня).
- КОЛИ `level(≥, 20)` → ТО `unlock(teams)`; у команді — `custom: «запит життів»`, чат.
- Перемога: виконати цілі рівня за ліміт ходів · Поразка: ходи 0 · Рахунок: зірки за рівень (не очки), прогрес по рівнях.

## Керування і ввід
- Тап по кубику — лопнути його групу; тап по спецплитці — активувати; тап по спецплитці поруч з іншою — комбінація (?).
- Бустер: вибрати іконку, потім клітину/рядок/стовпець.

## Вікна, меню, HUD
- `map-window` — шлях рівнів по епізодах (?) зі скринями.
- `custom: «level-intro»` — цілі рівня й pre-level бустери (?).
- `game-screen`: поле, `move-counter`, `goal-counter`, панель бустерів; `custom: «special-preview»` — кубики великої групи показують іконку спецплитки, яка вийде (?).
- `end-screen` — перемога / «Level failed», −1 життя.
- `custom: «chest-reward»` — відкриття Toon Chest / Star Chest.
- `shop-window` (монети, бустери, життя) · вікно команди (чат, запит життів) · `settings-window`.

## Фічі поза полем
- `levels-sequential` + `level-unlock`; скрині-віхи кожні 10 рівнів і за зірки.
- `custom: «lives-regen»` — життя відновлюються з часом; запит у команди або друзів (Facebook).
- Команди з 20 рівня: чат, обмін життями; командні події (?).
- `shop-window` + монети; бустери як запас.

## Варіації й родичі
- **Відмінності від `samegame-flood`** (тап по групі там теж): SameGame — фіксоване поле без поповнення, квадратичні очки, зсув стовпців уліво, мета — вичистити все; Toon Blast — **поповнення згори**, **ліміт ходів**, **цілі рівня**, **спецплитки за розміром групи** (5/7/9) з комбінаціями, мета-шар (скрині, життя, команди).
- Відмінності від `candy-crush` / `match3-meta-renovation`: хід — тап, а не обмін; немає «нелегального» ходу, лише замала група; спецплитка залежить від **розміру** групи, а не від **форми** (лінія 4, L/T, квадрат).
- Toy Blast (2015, той самий розробник Peak) — попередник з тим самим ядром (?).
- **Осі варіацій**: хід (тап групи / обмін / зсув) · як народжується спецплитка (розмір групи / форма лінії) · поповнення (нема / згори) · мета рівня (вичистити поле / квота кольору / перешкоди).

## Цікавинки для курсу
- Flood fill групи по тапу + падіння + поповнення — 🌱 (якщо вже є SameGame).
- Спецплитка за розміром групи (5 / 7 / 9) з превʼю на кубиках до тапу — 📎.
- Ланцюгова детонація спецплиток і таблиця комбінацій двох — 🥉.
- Цілі рівня + ліміт ходів поверх SameGame-ядра (дані рівня у файлі) — 📎.
- Скрині-віхи: кожні N рівнів і за накопичені зірки — 🌱.

## Мапа на каталог
- Є: `cell-click` · `gravity-fall` · `spawn-random-cell` · `chain-reaction` · `chain-detonation` · `explode-area` (Bomb) · `move-limit` · `collect-quota` · `goal-counter` · `sequential-levels` · `level-unlock` · `inventory-items` (бустери) · `round-currency` (монети) · `shop-window` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+connected-group-pop` (з SameGame) — тап по звʼязній групі.
  - `+group-size-specials` «Спецплитка за розміром групи» · entities/spawn · 📎 · слот {thresholds: 5,7,9}.
  - `+tap-activate-special` (з Royal Match) · `+special-combos` · `+star-thresholds` · `+stamina-energy` (з Candy Crush).
  - `+team-lives-request` (з Royal Match) — команди з 20 рівня.
  - `+milestone-chest` «Скриня-віха кожні N рівнів / за N зірок» · game-logic/economy · 🌱.
  - `+reshuffle-booster` «Бустер перемішування поля» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+ui:special-preview` — іконка на плитках групи: яка спецплитка вийде, якщо тапнути (?).
- `+window:chest-reward` — відкриття скрині з нагородами (також у `match3-meta-renovation`).
- `+card:group-size-specials` · `+card:milestone-chest` · `+card:reshuffle-booster` — див. «Мапу».

## Джерела
- ⭐ [Pocket Gamer: Toon Blast tips](https://www.pocketgamer.com/toon-blast/toon-blast-cheats-tips-and-tricks/) — Rocket 5 (рядок/стовпець, напрям випадковий), Bomb 7 (8 сусідніх), Disco Ball 9 (увесь колір), комбінації двох спец, чистити знизу.
- [Level Winner: Toon Blast guide](https://www.levelwinner.com/?p=11479) — комбінації rocket+rocket / bomb+bomb / disco+disco, ліміт ходів без таймера, зірки й Star Chest з 15 рівня, Toon Chest кожні 10, Dice/Glove/Anvil, команди з 20 рівня, запит життів.
- [Wikipedia: Toon Blast → Peak Games](https://en.wikipedia.org/wiki/Toon_Blast) — розробник (Стамбул), Toy Blast 2015 і Toon Blast 2017, Android/iOS; механік статті нема.

## Непевне
- ⭐-лінк черги (W:Toon_Blast) — редирект на статтю Peak Games без механік; fandom (toonblast.fandom.com) віддав 402.
- (?) Мінімальна група: Level Winner пише 3, з памʼяті — 2; поріг Bomb: 7 у більшості гайдів, 6 у Gamezebo; площа Bomb — 8 сусідів чи 3×3.
- (?) Типи цілей рівня (кольори кубиків, качки, кульки, коробки) і перелік перешкод — з памʼяті; Level Winner пише «очистити поле».
- (?) Скільки зірок за рівень і від чого (ходи), ціна Star Chest (20 зірок?) — джерела розходяться (кожні 7 рівнів vs 20 зірок).
- (?) Комбінації rocket + bomb, disco + rocket|bomb; чи бустери витрачають хід; продовження за монети; карта епізодів; превʼю спецплитки на кубиках.
