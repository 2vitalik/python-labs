---
title: Animal Planner
slug: animal-planner
aka: [动物安排员]
family: push-slide
also: [pencil-logic]
klass: figure
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2023
platforms: [PC, Mac, iOS]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2479960/", best: true, note: "опис: тварина = ковзний блок зі своїм характером, 15 тварин, ~80 рівнів, мапа, подарунки"}
  - {kind: itch, url: "https://lunardust.itch.io/animal-planner", note: "повна версія; керування мишею"}
  - {kind: itch, url: "https://lunardust.itch.io/animalrequests", note: "демо: ЛКМ рухає, Z — undo, R — заново; вівці/вовки/капуста"}
  - {kind: other, url: "https://steamcommunity.com/app/2479960/reviews/?browsefilter=toprated&filterLanguage=english", note: "відгуки: правила тварин, краб лише вбік, яйця, бомби"}
  - {kind: other, url: "https://www.taptap.cn/review/48639913", note: "огляд CN: свині/сніг, пінгвін, бомби з відліком 99 ходів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Animal+Planner+PawPaw+Games+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [cell-click, drag-drop-piece, impassable-cells, satisfy-constraints, completion-detection, undo-redo, restart-level, world-map, level-unlock, tutorial-window, sound-effects, +no-adjacent-check, +adjacency-need, +axis-locked-move, +egg-hatch, +bomb-countdown, +collectible-gifts, +unlock-all-levels]
proposes: ["+cond:adjacent_to", "+trigger:countdown_zero", "+ui:countdown-on-tile", "+ui:mood-animation", "+feature:unlock-all-levels", "+card:adjacency-need", "+card:bomb-countdown"]
author: opus
date: 2026-11-09
---

# Animal Planner — розсели тварин-блоки на маленькій сітці так, щоб кожна була щаслива: ведмідь сам, вівця біля трави й далі від вовка

## Суть
Ковзна головоломка в дусі Klotski, де кожен блок — тварина зі **своїм правилом сусідства чи підлоги**. Гравець мишею пересуває тварин по сітці; рівень пройдено, коли всі тварини задоволені одночасно. Кожна глава вводить нову тварину і її умову; пізніше зʼявляються яйця (стають твариною, що поруч) і бомби з відліком (повертають тварину в яйце). Жанрово — Sokoban-рух поверх задачі на обмеження («дитя Sokoban і судоку», огляд TapTap).

## Поле і час
- Маленька квадратна сітка, «зазвичай 4×4 або менше» (відгук), 2–3 види тварин на рівень; клітини підлоги — звичайні, трава, сніг, капуста як обʼєкт.
- Покроково: хід — переміщення однієї тварини; бомби рахують ходи (`time: turn`).
- ~80 рівнів (79/80 у відгуках), 15 глав — по главі на тварину, 4–5 рівнів зі зростанням складності.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ведмідь | piece | — | щасливий, коли поруч нікого |
| Риба | piece | — | щаслива разом з іншими (рибами?) |
| Вівця | piece | — | хоче бути впритул до трави; боїться вовка поруч |
| Вовк | piece | — | алергія на капусту — не поруч із нею |
| Свиня | piece | — | хоче капусту поруч; не стоїть на снігу (мерзне) |
| Пінгвін | piece | — | хоче стояти на снігу; не любить траву |
| Краб | piece | рядок старту | рухається лише вбік у своєму рядку; не хоче сусіда-краба, до інших байдужий |
| Жаба | piece | — | є досягнення «зробити жабу щасливою»; умова — (?) |
| Кролик, медуза, акула… | piece | — | інші тварини 15-ки; правила — (?) |
| Яйце | piece | без типу | стає твариною, яка опинилась поруч |
| Бомба з таймером | hazard | відлік ходів (напр. 99) | на нулі повертає тварину в яйце |
| Трава | terrain | — | потрібна вівцям (поруч), заважає пінгвінам |
| Сніг | terrain | — | потрібен пінгвінам, свиням заборонений |
| Капуста | object | — | їжа свиней, алерген вовків |
| Кнопка-перемикач (flip button) | switch | — | додана у демо 0.6.0; дія — (?) |
| Перешкоди / межі поля | static | — | непрохідні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, animal)` → ЯКЩО `free(target_cell)` і `legal(move)` → ТО `move(animal, dir)` (тип руху — див. «Непевне»); інакше `block`.
- КОЛИ `input(drag, crab)` → ЯКЩО `custom: «ціль поза рядком краба»` → ТО `block`.
- Умови щастя (перевіряються щоходу як обмеження):
  - ведмідь: `adjacent_count(bear, animal, ==, 0)`;
  - риба: `adjacent_count(fish, fish, >=, 1)` (?);
  - вівця: `custom: «поруч трава»` (слово — `+cond:adjacent_to`) і `adjacent_count(sheep, wolf, ==, 0)`;
  - вовк: `adjacent_count(wolf, cabbage, ==, 0)`;
  - свиня: `custom: «поруч капуста»` і `not cell(under_pig, snow)`;
  - пінгвін: `cell(under_penguin, snow)`;
  - краб: `no_adjacent(crab)`.
- КОЛИ `constraint_broken(animal_rule)` → ТО `custom: «тварина показує невдоволення анімацією»` (свиня тремтить на снігу, вівця тікає від вовка).
- КОЛИ `adjacent(egg, animal)` → ТО `transform(egg, same_type_as_animal)`.
- КОЛИ `custom: «відлік бомби = 0»` (слово — `+trigger:countdown_zero`) → ТО `transform(animal, egg)` для тварини під/біля бомби (?).
- КОЛИ `turn_end` → ТО `counter(bomb_fuse, -1)`.
- КОЛИ `all_constraints_met` → ТО `win`, `custom: «групове фото тварин»`, `next_level`.
- КОЛИ `input(undo)` → ТО `undo(1)`; КОЛИ `input(retry)` → ТО `restart` (undo не проходить крізь рестарт).
- Перемога: усі тварини задоволені. · Поразка: нема; глухий кут → undo/R. · Рахунок: нема; за главу — подарунок.

## Керування і ввід
- Лише миша: ЛКМ хапає й переміщує тварину (drag) (?); клік по тварині — звук.
- Z — undo, R — почати рівень заново; працює на Steam Deck.

## Вікна, меню, HUD
- `map-window` — мапа села з рівнями-вузлами: майже лінійна, з кількома необовʼязковими гілками; кнопка «Unlock All Levels»; вибір рівня завжди повертає на перший рівень (скарга).
- `game-screen` — сітка з тваринами; HUD: `countdown-on-tile` на бомбах (?), анімації настрою тварин як підказка порушеного правила (`conflict-highlight`-подібно).
- `tutorial-window` — інтерактивне навчання (лише перші тварини; яйця й бомби не пояснюються).
- `custom-window` — колекція подарунків (15) на екрані вибору рівнів; лист-фінал («The Letter»).
- `end-screen` — групове фото задоволених тварин.

## Фічі поза полем
- `undo`, `restart-level`; немає збереження посеред рівня.
- `world-map`, `level-unlock` + `unlock-all-levels` (пропуск порядку).
- `collectibles`: 15 подарунків — улюблена їжа тварини за всю главу; прикраси дому після проходження (огляд TapTap) (?).
- `achievements` (8, 3 приховані), `localization` (7 мов), `tutorial`.

## Варіації й родичі
- Родичі: `klotski` (ковзні блоки — тут без мети «вивести блок»), `sokoban`, задачі розсаджування гостей (обмеження сусідства), `pencil-logic`-пазли з `no-adjacent`.
- Осі варіацій:
  - **мета ковзного пазла**: вивести блок (`klotski`, `rush-hour`) / впорядкувати (`sliding-tile-permutation`) / **задовольнити умови кожного блока** (Animal Planner);
  - **умова блока**: сусіди виду (так/ні) / тип підлоги під собою / обʼєкт поруч / одинокість;
  - **рух блока**: вільний 4 напрямки / **лише по осі** (краб, як `rush-hour`);
  - **зміна типу**: нема / яйце копіює сусіда / бомба повертає в яйце.

## Цікавинки для курсу
- Таблиця правил тварин як дані: `{animal: [needs, hates, floor]}` + одна функція `happy(cell)` — 🌱 (гарний приклад «правило = рядок даних»).
- Перевірка всіх умов після кожного ходу + анімація невдоволених — 📎.
- Рух лише по осі для окремого виду (краб) — 🌱.
- Яйце, що стає типом сусіда (порядок, якщо поруч двоє різних?) — 📎.
- Бомба з відліком ходів, що повертає в яйце — 📎.
- Розвʼязувач: BFS по розстановках на 4×4 з перевіркою обмежень — 🥉.

## Мапа на каталог
- Є: `cell-click` + `drag-drop-piece` ↔ миша; `impassable-cells` ↔ межі/перешкоди; `satisfy-constraints` + `completion-detection` ↔ «усі щасливі»; `undo-redo` + `restart-level` ↔ Z/R; `world-map` + `level-unlock` ↔ мапа села; `tutorial-window` ↔ навчання; `sound-effects` ↔ голоси тварин.
- **Нема** → пропозиції карток:
  - `+no-adjacent-check` (вже пропонована Hitori) — ведмідь, краби.
  - `+adjacency-need` «Сутності потрібен/заборонений сусід виду» · game-logic/constraints · 🌱 · слоти {need, hate, floor}.
  - `+axis-locked-move` (вже пропонована) — краб лише в рядку.
  - `+egg-hatch` (вже пропонована) · слот {type: copy-neighbor}.
  - `+bomb-countdown` «Бомба з відліком ходів змінює сутність» · entities/state · 📎 · слот {turns}.
  - `+collectible-gifts` «Нагорода за главу — колекційний предмет» · levels/progression · 🌱.
  - `+unlock-all-levels` «Кнопка відкрити все» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+cond:adjacent_to` — поруч є обʼєкт/клітина виду (трава, капуста); `adjacent_count` рахує сутності, а тут — тип клітини.
- `+trigger:countdown_zero` — відлік на сутності дійшов нуля (бомба).
- `+ui:countdown-on-tile` — число ходів на бомбі; `+ui:mood-animation` — тварина анімацією показує, яке правило порушено.
- `+feature:unlock-all-levels` — відкрити всі рівні одним перемикачем.
- `+card:adjacency-need`, `+card:bomb-countdown` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Animal Planner](https://store.steampowered.com/app/2479960/) — «кожна тварина — ковзний блок з унікальним характером», ведмідь сам, риба разом, 15 тварин, ~80 рівнів, мапа, 15 подарунків; PawPaw Games, 10.11.2023.
- [itch: Animal Planner](https://lunardust.itch.io/animal-planner) — lunarDust, Unity, лише миша, інтерактивне навчання.
- [itch: демо](https://lunardust.itch.io/animalrequests) — ЛКМ, Z, R; «вівці люблять траву, але бояться вовків», «вовки — алергія на капусту»; [devlog 0.6.0](https://lunardust.itch.io/animalrequests/devlog/560939/version-060-new-mechanics) — flip button і time bomb.
- [Steam: відгуки](https://steamcommunity.com/app/2479960/reviews/?browsefilter=toprated&filterLanguage=english) — краб лише вбік у рядку, яйця стають твариною поруч, бомби → яйце, ≤4×4, Unlock All Levels, undo не крізь рестарт.
- [Steam: досягнення](https://steamcommunity.com/stats/2479960/achievements) — «Hatch an egg», «Make a frog happy», «The Letter».
- [TapTap: огляд](https://www.taptap.cn/review/48639913) — свиня/капуста/сніг, вівця/вовк, пінгвін/сніг, бомби на 99 ходів, анімовані підказки, нелінійна мапа.
- [App Store](https://apps.apple.com/app/id6642680412) — iOS-версія 2024, Game Center.

## Непевне
- (?) Як саме рухається тварина: на одну клітину за drag, до будь-якої досяжної клітини, чи ковзає до упору — джерела кажуть лише «ковзний блок» і «обмеження руху як у Sokoban».
- (?) Вівця «поруч із травою» (Steam-відгук) чи «на траві» (TapTap); риба — разом з рибами чи з будь-ким; свиням капуста «лише парами» (незрозуміла фраза відгуку).
- (?) Яйце: стає твариною-сусідом (Steam) чи випадковою (TapTap); що, коли поруч дві різні тварини.
- (?) Бомба: на кого діє (під нею / поруч), чи є ліміт ходів на рівень (TapTap згадує «обмеження кроків»).
- (?) Дія flip button, «контролера клітин», мін, ламп, мушель — згадані без пояснень.
- (?) Розробник: Steam — PawPaw Games, itch — lunarDust (+ YELLOW ATTIC у демо), App Store — Chao Cui; демо мало адресу `animalrequests` — можливо, робоча назва «Animal Requests».
