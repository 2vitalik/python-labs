---
title: Can of Wormholes
slug: can-of-wormholes
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2023
platforms: [PC, Mac, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1295320/Can_of_Wormholes/", best: true, note: "опис, дієслова «push, slice, ingest, flip, squish», 100+ рівнів, підказки-мініетапи, доступність"}
  - {kind: official, url: "https://muntedfinger.com/canofwormholes", note: "сайт гри: платформи, прескіт"}
  - {kind: other, url: "https://ladiesgamers.com/can-of-wormholes-review/", note: "рецензія: ціль-отвір, довжина черва, кульки, край поля, Game Insights"}
  - {kind: other, url: "https://opencritic.com/game/16249/can-of-wormholes", note: "OpenCritic: огляди преси"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Can+of+Wormholes+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [move-by-input, move-4dir, body-queue, push-object, fill-hole, multi-cell-size, item-pickup, environment-death, undo-unlimited, restart-level, world-map, keyboard-controls, +exact-fit-hole, +grow-by-eating, +cut-body, +hint-ministage, +party-control-room]
proposes: ["+feature:hint-ministage", "+window:hint-stage", "+effect:cut_body", "+cond:fits_exactly", "+card:exact-fit-hole", "+card:hint-ministage"]
author: opus
date: 2026-11-09
---

# Can of Wormholes — штовхай, ріж, ковтай і перевертай черв'яків, щоб кожен ліг точно у свій отвір

## Суть
Sokoban зі змійками: гравець — бляшанка з черв'яками всередині, на рівні керує черв'яком, що повзе сіткою як змійка. Ціль — завести черв'яка (або заштовхнути іншого) в отвір, обведений жовто-чорною стрічкою, і він має підійти **точно за довжиною й формою**. Дієслова — штовхнути, розрізати, проковтнути, перевернути, сплющити; кожен з 100+ рівнів відкриває нову взаємодію між тими самими кількома обʼєктами. Особливість — підказка як окремий маленький рівень, що ізолює ключову ідею.

## Поле і час
- Квадратна сітка, 3D-графіка; рівні — окремі невеликі поля, звʼязані інтерактивним оверворлдом зі своїми пазлами.
- Покроково: тік = один хід; жодних таймінгів і одночасних натискань (так заявлено в доступності).
- Край поля смертельний: черв'як, що торкнувся зовнішньої межі, розчиняється, рівень починається знову.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бляшанка | player | — | на оверворлді ходить «на ногах-черв'яках», штовхає обʼєкти, запускає кільце-кротовину в рівень |
| Черв'як | player / object | довжина, форма тіла | повзе як змійка (тіло йде за головою); інші черв'яки — обʼєкти, які штовхають |
| Отвір-ціль | static | форма й розмір | заповнюється лише черв'яком тієї самої форми й довжини |
| Кулька | pickup / object | — | черв'як зʼїдає автоматично й довшає; можна відштовхнути, щоб не рости |
| Блок | object | — | штовхається (?) |
| Межа поля | hazard | — | дотик → черв'як розчиняється |
| Кільце-кротовина | static | — | вхід з оверворлду в рівень |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(worm_head, dir)`, `custom: «тіло зсувається слідом за головою»`.
- КОЛИ `contact(worm, object)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `contact(worm, ball)` → ТО `pickup`, `grow(worm, 1)` (?).
- КОЛИ `edge(worm)` → ТО `custom: «черв'як розчиняється»`, `restart`.
- КОЛИ `enter(worm, hole)` → ЯКЩО `custom: «форма й довжина черв'яка збігаються з отвором»` → ТО `custom: «отвір заповнено»`.
- КОЛИ `custom: «черв'як зʼїв іншого черв'яка»` → ТО `custom: «хвіст відрізається»` (зі слів автора в інтерв'ю).
- КОЛИ `custom: «slice / flip / squish»` → ТО `custom: «розрізати / розвернути / сплющити черв'яка»` — механізм у джерелах не описано (?).
- КОЛИ `all_on(worm, hole)` → ТО `win`, `next_level` (?).
- КОЛИ `input(undo)` → ТО `custom: «відкотити хід»` (необмежено); КОЛИ `input(restart)` → ТО `restart`.
- Перемога: усі отвори заповнені (?) · Поразка: лише «мʼяка» — вихід за край перезапускає рівень · Рахунку нема.

## Керування і ввід
- Клавіатура або геймпад; миша не потрібна, жодного таймінгу.
- Undo і рестарт без обмежень.
- Після першого світу — «кімната керування»: зібрана енергія стає кнопками напрямків для кількох черв'яків на екрані (?).

## Вікна, меню, HUD
- `main-menu` → оверворлд (`map-window`-подібний світ, по якому ходить бляшанка).
- `game-screen`: поле рівня в 3D, без лічильників.
- `settings-window`: звідси відкривається Game Insights — підказка-мінірівень (`hint-stage`, custom).
- `hint-stage`: спрощена версія рівня, що ізолює головну механіку; розвʼязавши, повертаєшся до повного.
- Переходи: оверворлд → (кільце) → game-screen → оверворлд; game-screen → settings → hint-stage → game-screen.

## Фічі поза полем
- `undo` ∞, `restart-level`, `world-map` (інтерактивний оверворлд з власними пазлами).
- `hint-ministage` — підказка не текстом, а окремим рівнем на кожен рівень.
- `achievements` (Steam), `cloud-save`; локалізація EN / FR / zh-CN.
- Доступність: без таймінгу, без одночасних клавіш, дружня до глухих і дальтоніків (`colorblind-palette` (?)).

## Варіації й родичі
- Snakebird (змійка, гравітація, їжа подовжує), Snake (ріст від їжі), Sokoban (штовхання), Sokobond, jelly no puzzle (злипання форм), Baba Is You (кожен рівень — нова грань правил).
- Осі варіацій: **як рухається черв'як** — голова тягне тіло / задній хід / його штовхають як ящик; **що змінює довжину** — їжа / розріз / ковтання іншого; **ціль** — дійти / заповнити отвір точно за формою.

## Цікавинки для курсу
- Отвір, що приймає лише тіло тієї самої форми й довжини (порівняння поліоміно з урахуванням поворотів) — 🥉.
- Ріст від кульки й свідоме відштовхування їжі, щоб не перерости отвір — 📎.
- Розріз черв'яка на два незалежні — 🥉 (розщеплення черги тіла).
- Підказка як окремий мінірівень, привʼязаний до рівня — 📎 (дизайн, не код).
- Кілька черв'яків з одного пульта — 🥉.

## Мапа на каталог
- Є: `move-by-input` · `move-4dir` · `body-queue` (тіло-черга) · `push-object` · `fill-hole` · `multi-cell-size` · `item-pickup` (кульки) · `environment-death` (край) · `undo-unlimited` · `restart-level` · `world-map` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+exact-fit-hole` «Отвір під точну форму тіла» · game-logic/win · 🥉 · слоти {match: length|shape|both}.
  - `+grow-by-eating` «Ріст від їжі» · entities/state · 🌱 (можливо, вже є в Snake-файлах).
  - `+cut-body` «Розрізати тіло-чергу» · entities/interact · 🥉.
  - `+hint-ministage` «Підказка — мінірівень» · levels/progression · 📎.
  - `+party-control-room` «Пульт кількох аватарів» · entities/move · 🥉 — дитина `party-switch` (?).

## Пропозиції до словників
- `+feature:hint-ministage` — підказка як окремий спрощений рівень; `+window:hint-stage` — вікно цього мінірівня.
- `+effect:cut_body` — розрізати тіло-чергу в точці; `+cond:fits_exactly` — сутність збігається з формою цілі.
- `+card:exact-fit-hole`, `+card:hint-ministage` — див. вище.
- ⏳-слова, вжиті тут: `input`, `free`, `edge`, `enter`, `all_on`, `move`, `grow`, `restart`, `next_level`.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/1295320/Can_of_Wormholes/) — дієслова, 100+ рівнів, оверворлд, підказки-мінірівні, доступність, дата 24.03.2023.
- [Сайт гри](https://muntedfinger.com/canofwormholes) — платформи PC / Mac / Switch.
- [LadiesGamers](https://ladiesgamers.com/can-of-wormholes-review/) — ціль у стрічці, точна довжина, кульки, край поля, Game Insights у налаштуваннях.
- [OpenCritic](https://opencritic.com/game/16249/can-of-wormholes) — Nintendo Life 9/10, Nindie Spotlight 8.2.

## Непевне
- (?) Конкретика дієслів slice / flip / squish / ingest — джерела їх лише називають; відкриті сторінки рецензій і інтерв'ю (Thinky Games — 403) механізму не описують.
- (?) Хто саме керований у рівні — черв'як, бляшанка чи обидва; рецензія каже «рухаєш черв'яка, як змійку».
- (?) Кімната керування й енергія після першого світу — з короткого пошукового резюме, не з першоджерела.
- (?) Розробник згадував задній хід змійки як вихідну ідею прототипу — подробиць нема.
- (?) Умова перемоги з кількома отворами.
