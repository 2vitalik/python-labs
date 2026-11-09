---
title: Exit
slug: exit-taito
aka: [Exit DS, Kangaeru Exit, Exit 2, Mr. ESC]
family: grid-platformer
also: [thinky]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 2005
platforms: [PSP, Xbox 360, Nintendo DS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Exit_(video_game)", best: true, note: "типи супутників, накази, інструменти, небезпеки, таймер, рахунок до 100, платформи й сиквел"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=exit+psp+taito+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, push-object, item-pickup, inventory-items, key-and-door, one-way-cell, environment-death, player-death, time-out, reach-exit, collect-quota, party-switch, time-bonus, score-records, sequential-levels, level-select, cell-click, game-screen, end-screen, pause-menu, +assign-skill, +rescue-followers, +actor-type-abilities, +carry-ally, +crate-steps, +tool-clears-obstacle, +swim-only-avatar, +darkness-needs-light, +rescuer-on-fail, +par-time-score]
proposes: ["+effect:rescue(a)", "+effect:command(a, action, target)", "+cond:can_climb(a, height)", "+cond:fits_passage(a, cell)", "+cond:awakened(a)", "+trigger:required_lost", "+role:survivor", "+axis:actors=party-commanded", "+card:rescue-followers", "+card:actor-type-abilities"]
author: opus
date: 2026-11-09
---

# Exit — рятівник Mr. ESC виводить з будівлі людей різних типів, наказуючи їм носити ящики, гасити вогонь і лізти на уступи

## Суть
Гравець керує Mr. ESC — бігає, стрибає, плаває — і має вивести з катастрофи (пожежа, повінь, землетрус) потрібну кількість людей до таймера. Люди мають **типи з різними вміннями**: діти пролазять у вузьке, дорослі штовхають важке, підлітки допомагають іншим лізти, пацієнтів треба нести. Ядро — розподіл завдань між підлеглими (як Lemmings + Lost Vikings) на бічній клітинній мапі з ящиками-сходинками та інструментами. Клас — гібрид: `avatar` (ESC) + `figure` (накази людям).

## Поле і час
- Бічний вид, будівля з поверхів і уступів; рух по клітинній логіці (уступи у висоту ящика, ящик як сходинка).
- Real-time з таймером рівня; ESC швидший за всіх, стрибає вище, добре плаває.
- Рівень: старт ESC, вихід, необовʼязкові заблоковані люди, ліміт часу.
- Небезпеки змінюють поле: вогонь, вода, завали, темні зони, оголені дроти.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Mr. ESC | player | 1 травма = рестарт | біжить, стрибає високо, плаває; будить людей дотиком, наказує, бере/використовує інструменти; травмується від небезпек і падіння |
| Young (підліток) | ally | середній зріст | лізе на помірну висоту, стрибає, допомагає іншим залізти |
| Дитина | ally | малий зріст | лізе лише на малу висоту; пролазить у прохід, замалий для дорослих і ESC |
| Дорослий | ally | сильний | штовхає дуже великі обʼєкти; на помірну висоту — лише з допомогою одного іншого |
| Пацієнт | ally | не ходить сам | його несуть або везуть на ношах, якщо ноші є |
| Ноші | object | — | дозволяють довезти пацієнта до виходу |
| Ящик | object | розмір | штовхається; стає сходинкою на вищий уступ |
| Великий обʼєкт | object | важкий | зсуває лише дорослий |
| Вогонь | hazard | — | непрохідний, доки не згасять вогнегасником |
| Вогнегасник | pickup | інструмент | гасить вогонь |
| Кайло | pickup | інструмент | розчищає завал |
| Ліхтарик | pickup | інструмент | потрібен, щоб бачити в темній зоні |
| Завал | static | — | непрохідний, доки не розбити кайлом |
| Вода | terrain | глибина | плаває лише ESC |
| Темна зона | zone | — | без ліхтарика не видно |
| Односторонні двері | gate | напрям | прохід лише в один бік |
| Оголені дроти | hazard | — | травмують |
| Вихід | static | — | ціль для ESC і врятованих |
| Jet | neutral | реактивний ранець | зʼявляється, коли люди загинули або час вийшов; виносить травмованих |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(esc, dir)`; КОЛИ `input(jump)` → ТО `custom: «стрибок, вище за інших»`.
- КОЛИ `tick` → ЯКЩО `not supported(a)` → ТО `fall(a)`; ЯКЩО `custom: «падіння зависоке»` → ТО `damage(a, 1)`.
- КОЛИ `contact(esc, survivor)` → ЯКЩО `state(survivor, panic)` → ТО `clear_state(survivor, panic)`, `custom: «приєднується до групи»`.
- КОЛИ `input(order, survivor, target)` → ЯКЩО `not state(survivor, panic)` → ТО `custom: «людина йде до цілі / виконує дію»` (пропозиція `command`).
- КОЛИ `custom: «людина має лізти на уступ»` → ЯКЩО `custom: «висота ≤ вміння типу»` → ТО `move(survivor, up)`; інакше `block` або потрібна допомога іншого.
- КОЛИ `input(order, child, passage)` → ЯКЩО `custom: «прохід малий»` → ТО `move(child, through)`; для дорослих і ESC — `block`.
- КОЛИ `contact(adult, big_object)` → ЯКЩО `free(cell_behind)` → ТО `push(big_object)`; інші типи — `block`.
- КОЛИ `contact(a, crate)` → ЯКЩО `free(cell_behind)` → ТО `push(crate)`; ящик біля уступу дає сходинку.
- КОЛИ `input(pick, tool)` → ТО `pickup(a, tool)`; КОЛИ `input(order, a, trade)` → ТО `custom: «передати інструмент іншому»`.
- КОЛИ `input(use, extinguisher)` → ЯКЩО `adjacent(a, fire)` → ТО `disappear(fire)`.
- КОЛИ `input(use, pickaxe)` → ЯКЩО `adjacent(a, rubble)` → ТО `disappear(rubble)`.
- КОЛИ `enter(a, dark_zone)` → ЯКЩО `not has(a, flashlight)` → ТО `custom: «не видно»`.
- КОЛИ `enter(a, water)` → ЯКЩО `custom: «a ≠ ESC»` → ТО `block` (люди не плавають).
- КОЛИ `enter(a, one_way_door)` → ЯКЩО `not moving(a, allowed_dir)` → ТО `block`.
- КОЛИ `custom: «ESC несе пацієнта або везе на ношах»` → ТО `carry`.
- КОЛИ `contact(a, hazard)` → ТО `damage(a)`; люди самі уникають явно смертельних дій, але непрямі небезпеки їх травмують.
- КОЛИ `died(survivor)` або `custom: «людина травмована»` → ТО `spawn(jet)`, `custom: «Jet виносить травмованого»`.
- КОЛИ `custom: «травмованих забагато, квоти не досягти»` → ТО `restart`.
- КОЛИ `hp_zero(esc)` → ТО `restart` (одна травма ESC).
- КОЛИ `counter(time_left, ==, 0)` → ТО `spawn(jet)`, `lose`.
- КОЛИ `reach(esc, exit)` → ЯКЩО `counter(rescued, >=, required)` → ТО `win`, `score(до 100)`.
- Перемога: вивести потрібну кількість людей і самого ESC · Поразка: травма ESC, нестача людей, таймер · Рахунок: до 100 очок за врятованих і пар-час.

## Керування і ввід
- PSP/360: ESC керується напряму (рух, стрибок, дія) (?).
- Наказ: вибрати людину, вказати місце або обʼєкт — вона йде і виконує (рух, завдання, взяти/використати/передати інструмент) (?).
- DS: наказ стилусом по екрану (?).

## Вікна, меню, HUD
- `main-menu` → `level-select` (ситуації, 70 доступні одразу, будь-який порядок) → `game-screen`.
- `game-screen`: будівля, HUD — `timer-countdown`, лічильник «врятовано / треба» (`remaining-counter`), інструмент у руках (?).
- `pause-menu`: продовжити, рестарт, вихід (?).
- `end-screen`: очки до 100 (врятовані + час проти пар), рекорд рівня.

## Фічі поза полем
- PSP: 100 рівнів (70 відкриті з початку), +100 завантажуваних; Xbox 360: 220 рівнів.
- Повтор рівня заради кращого рахунку (`score-records`).
- `mode-classic` лише; мультиплеєра нема (?).

## Варіації й родичі
- Сиквел Kangaeru Exit / Exit 2 (2006, XBLA 2009); Exit DS (2008, MOSS).
- Родичі: Lemmings (накази автономним), The Lost Vikings (герої з різними вміннями), Troddlers, Space Panic-подібні будівлі.
- Осі: **хто діє** (один аватар / аватар + підлеглі / лише накази) · **вміння за типом** (зріст, сила, плавання) · **ціна помилки** (травма → допомога Jet / рестарт).

## Цікавинки для курсу
- Типи підлеглих як таблиця вмінь (висота підйому, прохід, сила) — 📎.
- Наказ «піди і зроби» з пошуком шляху з урахуванням типу — 🥉.
- Ящик-сходинка й допомога іншому залізти (кооп двох сутностей) — 📎.
- Інструменти, що знімають тип перешкоди (вогонь → вогнегасник, завал → кайло, темрява → ліхтар) — 🌱.
- Рахунок до 100 за врятованих і пар-час — 🌱.
- Перевірка «квоти вже не досягти» → авто-рестарт — 📎.

## Мапа на каталог
- Є: `gravity-fall` · `push-object` ↔ ящики · `item-pickup` + `inventory-items` ↔ інструменти · `key-and-door` ↔ інструмент → перешкода · `one-way-cell` ↔ односторонні двері · `environment-death` · `player-death` · `time-out` · `reach-exit` · `collect-quota` ↔ врятувати N · `party-switch` ↔ вибір людини · `time-bonus` ↔ пар-час · `score-records` · `cell-click` ↔ вказати ціль наказу.
- **Нема** → пропозиції карток:
  - `+assign-skill` (як у Lemmings) — наказ підлеглому.
  - `+rescue-followers` «Розбудити й вивести людей» · entities/interact · 📎.
  - `+actor-type-abilities` «Типи підлеглих з різними вміннями» · entities/legality · 📎.
  - `+carry-ally` «Нести союзника» · entities/move · 📎.
  - `+crate-steps` «Ящик як сходинка» · entities/legality · 🌱.
  - `+tool-clears-obstacle` «Інструмент знімає тип перешкоди» · entities/interact · 🌱.
  - `+swim-only-avatar` «Вода прохідна лише для аватара» · entities/legality · 🌱.
  - `+darkness-needs-light` «Темна зона потребує ліхтаря» · interface/render · 📎.
  - `+rescuer-on-fail` «NPC-рятівник при провалі» · game-logic/lose · 🌱.
  - `+par-time-score` «Рахунок проти пар-часу» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:rescue(a)` — сутність зараховується врятованою (вийшла).
- `+effect:command(a, action, target)` — наказ підлеглому виконати дію.
- `+cond:can_climb(a, height)` — висота уступу в межах вміння типу.
- `+cond:fits_passage(a, cell)` — сутність вміщується у прохід.
- `+cond:awakened(a)` — людина вийшла з паніки (можна замінити `state`).
- `+trigger:required_lost` — квоти врятованих уже не досягти.
- `+role:survivor` — сутність, яку треба вивести (не `ally`, бо сама не допомагає до пробудження).
- `+axis:actors=party-commanded` — аватар + підлеглі за наказами.
- `+card:rescue-followers` · `+card:actor-type-abilities` — див. вище.

## Джерела
- ⭐ [Wikipedia: Exit (video game)](https://en.wikipedia.org/wiki/Exit_(video_game)) — чотири типи людей і їхні вміння, паніка до дотику, накази й інструменти, вогонь/вода/завали/темрява/двері/дроти, Jet, рахунок до 100, кількість рівнів, платформи, сиквел.
- YouTube: пошук «exit psp taito gameplay».

## Непевне
- (?) Драбини, мотузки, ключі — у Wikipedia не згадані; `ladder-climb` у теги не взято.
- (?) Точна схема наказів на PSP (кнопки, курсор) і на DS (стилус).
- (?) Чи падіння з висоти травмує людей так само, як ESC; висоти в клітинах.
- (?) Чи є пауза-меню з рестартом і HUD-інструмента — за звичаєм жанру.
- (?) Рівень — квадратна сітка лише логічно (ящики, уступи); рух персонажів плавний.
- Офіційного сайту/вікі не відкрито — опис спирається на одну статтю Wikipedia.
