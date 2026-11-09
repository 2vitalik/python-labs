---
title: Order of the Sinking Star
slug: order-of-the-sinking-star
aka: [OotSS]
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
year: 2026
platforms: [PC, Switch 2, PS5]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/499170/Order_of_the_Sinking_Star/", best: true, note: "опис: 1000+ пазлів, чотири світи, герої (королева, злодій, воїн, чарівник, човен), чотири гри-основи з авторами"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Order_of_the_Sinking_Star", note: "геймплей по світах: герої тягнуть/штовхають, дзеркала й клони, каміння, промені й самоцвіти; undo/rewind; 1400+ пазлів; дати, платформи"}
  - {kind: official, url: "https://www.orderofthesinkingstar.com/", note: "офіційний сайт (лише титул і гасло)"}
  - {kind: other, url: "https://www.keengamer.com/articles/reviews/pc-reviews/order-of-the-sinking-star-review-a-puzzle-marathon-that-trusts-you-to-find-the-answers-pc/", note: "рецензія: чотири світи за сторонами світу, воїн/злодій/чарівник, клавіша перемикання героїв, undo по кроку, restart"}
  - {kind: other, url: "https://www.altchar.com/reviews/order-of-the-sinking-star-review-moving-stones-sinking-brains-agudf8w4smyH", note: "рецензія: камінь ковзає водою до берега, латаття тримає камінь і відпливає, дзеркала множать героя, ізометрія + план зверху"}
  - {kind: other, url: "https://nintendoeverything.com/order-of-the-sinking-star-review-for-nintendo-switch-2/", note: "рецензія: воїн штовхає ланцюг і ворогів, злодій тягне по одному, чарівник міняється з блоком/ворогом/героєм; rewind"}
  - {kind: other, url: "https://pixeltwelve.com/articles/order-of-the-sinking-star-review", note: "рецензія: Gold Rooms змішують правила, нема підказок, кольорові промені важко читати"}
  - {kind: other, url: "https://alan.draknek.org/games/", note: "каталог Alan Hazelden: Skipping Stones to Lonely Homes (2015) і Mirror Isles (2014) — ігри-основи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Order+of+the+Sinking+Star+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, pull-object, party-switch, swap-on-contact, mirror-reflect, beam-tracing, impassable-cells, all-on-targets, reach-exit, undo-step, restart-level, world-map, game-screen, pause-menu, settings-window, field-scaling, player-camera, fog-of-war, save-autosave, achievements-window, +chain-push, +line-of-sight-swap, +mirror-image-swap, +skipping-stone, +floating-stepping-pad, +beam-granted-ability, +mechanic-crossover, +open-world-puzzles, +overworld-travel, +multi-agent-sync]
proposes: ["+effect:skip_across", "+effect:drift", "+cond:in_beam", "+card:skipping-stone", "+card:floating-stepping-pad", "+card:beam-granted-ability", "+card:mechanic-crossover", "+feature:fast-travel"]
author: opus
date: 2026-11-09
---

# Order of the Sinking Star — «суперколайдер» чотирьох Sokoban-серій: герої з дієсловами, дзеркала, каміння по воді й промені

## Суть
Відкритий світ Джонатана Блоу (Thekla) із понад тисячею однокранних Sokoban-пазлів на квадратній сітці. Основа — чотири незалежні серії інших авторів, кожна стала окремим світом: [Heroes of Sokoban](heroes-of-sokoban.md) (герої з різними дієсловами: штовхати / тягти / мінятися), [Mirror Isles](mirror-isles.md) (обмін місцями з відображенням), Skipping Stones to Lonely Homes (камінь, кинутий у воду, ковзає до берега) і Promesst Шона Барретта (промені світла з самоцвітів). Ядро гри — **схрещування**: після кількох десятків пазлів кожного світу зʼявляються кімнати на межах світів і Gold Rooms, де правила двох-трьох серій діють одночасно (дзеркальні клони героїв, герої в променях). Пазли 2D, пізні — 3D.

## Поле і час
- Оверворлд — суцільна мапа з чотирма світами за сторонами світу (Північ — Hearty Heroes of Hauling, Схід — Mirror Isles, Південь — Skipping Stones, Захід — The Promise / Vault of the Beamcasters), «туман» знімається, коли відкриваєш нову сушу. Між світами вільний перехід, є швидке переміщення між позначеними точками.
- Пазл — невелика квадратна сітка (острів, кімната храму), вхід з оверворлду; кожна локація-пазл відкриває прохід далі або вчить механіку.
- Покроково: тік = крок активного героя; випадковості й таймерів нема.
- Камера ізометрична, з відʼїздом у план зверху для планування; у пізніх пазлах — третій вимір.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Воїн (Warrior) | player | дієслово push | крок 4 напрямки; штовхає блок, ланцюг блоків, а ланцюгом — і ворогів |
| Злодій (Thief) | player | дієслово pull | тягне блок, що позаду, по одному; штовхати не вміє |
| Чарівник (Wizard) | player | дієслово swap | рух до блока / ворога / героя на лінії — обмін місцями |
| Королева, Бард, Друїд, човен, що говорить | player | власне вміння (?) | нові герої приєднуються впродовж гри, кожен з одним вродженим умінням |
| Торговець (Mirror Isles) | player | — | міняється місцями зі своїм відображенням |
| Дослідник (The Promise) | player | — | самоцвіти живлять пристрої світла |
| Неактивний герой | object | — | стоїть; інші герої штовхають/тягнуть/міняються з ним |
| Блок / валун | object | — | штовхає воїн, тягне злодій, обмінюється чарівник; деревʼяні огорожі обмежують валуни (?) |
| Камінь (Skipping Stones) | object | — | на суші зсувається на 1; у воді ковзає поверхнею до найближчого берега; у куті чи без місця позаду — більше не зсувається |
| Латаття | terrain | вільне / з каменем | тримає камінь → сходинка, на яку можна стати; відпливає, якщо поруч проходить камінь; за іншим джерелом — везе героя (?) |
| Вода | terrain | — | герой не ходить; перетин — каменями, лататтям або дзеркалом |
| Дзеркало | object | — | кидає відображення героя за себе (телепорт-обмін); у світі Mirror Isles також згинає промінь |
| Відображення / дзеркальний клон | ally | — | копія героя; в комбінованих пазлах усі копії ходять разом |
| Промінь (рожевий, золотий, фіолетовий, зелений) | zone | колір = сила | герой, що стоїть у промені, отримує його силу поверх свого вміння |
| Самоцвіт (gem) | pickup | колір | вмикає промінь певної сили (світ The Promise) |
| Кристал-блок (фіолетовий, рожевий) | object | колір | перекриває, пропускає або перенаправляє промінь |
| Ворог (гоблін, монстр) | enemy | — | треба оминути; ланцюгом воїна зсувається як блок; бере участь у маршрутизації променів (?) |
| Статуя, що дихає вогнем | hazard | напрям | вогонь по лінії (?) |
| Цільова клітина героя | static | — | кожен герой має стати на свою |
| Нотатки й записи дослідника | pickup | текст | пояснюють механіки й сюжет |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(active, dir)`.
- КОЛИ `contact(warrior, block)` → ЯКЩО `free(cell_behind)` → ТО `push(block)`; ланцюг блоків і ворогів зсувається разом; упор → `block`.
- КОЛИ `input(dir)` → ЯКЩО `turn_of(thief)` and `occupied(cell_behind, block)` → ТО `move(thief, dir)`, `pull(block)`.
- КОЛИ `input(dir)` → ЯКЩО `turn_of(wizard)` and `line_of_sight(wizard, block)` → ТО `swap(wizard, block)` (також з ворогом чи іншим героєм).
- КОЛИ `input(switch_hero)` → ТО `custom: «керування переходить до наступного героя пазла»`.
- КОЛИ `contact(hero, stone)` → ЯКЩО `free(cell_behind)` → ТО `push(stone)`; ЯКЩО `cell(cell_behind, water)` → ТО `custom: «камінь ковзає поверхнею до найближчого берега»`.
- КОЛИ `enter(stone, lily)` → ТО `set_state(lily, stepping)` — герой може стати на латаття.
- КОЛИ `adjacent(stone, lily)` під час ковзання → ТО `custom: «латаття відпливає»`.
- КОЛИ `input(action)` → ЯКЩО `count(reflection, >, 0)` → ТО `swap(hero, reflection)`.
- КОЛИ `custom: «дзеркало стоїть на лінії героя»` → ТО `spawn(reflection)` за дзеркалом; у комбінованих пазлах `clone(hero)` — усі копії ходять одним вводом.
- КОЛИ `enter(hero, beam)` → ТО `set_state(hero, beam_power)`; КОЛИ `leave(hero, beam)` → ТО `clear_state(hero, beam_power)`.
- КОЛИ `picked(explorer, gem)` → ТО `custom: «самоцвіт вмикає промінь свого кольору»`.
- КОЛИ `contact(beam, crystal)` → ТО `custom: «кристал перекриває / перенаправляє промінь»`.
- КОЛИ `contact(hero, enemy)` → ТО `custom: «поразка спроби — лікується undo»` (?).
- КОЛИ `all_on(hero, target)` → ТО `win`, `custom: «відкривається прохід / нова ділянка оверворлду»`.
- Перемога: усі герої пазла на своїх цілях (або дійти до виходу) · Поразки як стану нема — undo / rewind / reset · Рахунку нема.

## Керування і ввід
- Рух — стрілки / стік; окрема клавіша — перемикання між героями, коли в пазлі їх кілька.
- Одна кнопка — undo на крок (можна тиснути поспіль, rewind); інша — reset усього пазла; вихід в оверворлд.
- Камера: ізометрія, відʼїзд у план зверху. Повна підтримка геймпада (Steam).

## Вікна, меню, HUD
- `map-window` — оверворлд як ігровий простір: чотири світи, туман над невідкритою сушею, точки швидкого переміщення, входи в пазли (не окремий екран-мапа, а сам світ) (?).
- `game-screen` — пазл: поле, активний герой; HUD мінімальний, пазли без явних підписів.
- `pause-menu` — повернення, reset, вихід в оверворлд (?).
- `settings-window` — мова (11), керування, гучність (?).
- `dialogue-window` — діалоги героїв і записи дослідника; пропущений діалог не повторюється (рецензія).
- `achievements-window` (Steam Achievements).
- Переходи: оверворлд → (вхід у локацію) пазл → (усі цілі) оверворлд з новим проходом.

## Фічі поза полем
- `undo` (по кроку, без ліміту) + `restart-level`; підказок нема (свідомо).
- `world-map` / відкритий світ: свобода порядку світів, повернення до кинутих пазлів, туман, швидке переміщення.
- Прогресія: пазли відкривають ділянки, Gold Rooms і схрещування світів; кілька фіналів (рецензія) (?).
- `autosave` + `cloud-save` (Steam Cloud), `achievements`, `localization` (11 мов), `gamepad-support`.

## Варіації й родичі
- Світи-основи: [Heroes of Sokoban](heroes-of-sokoban.md) (Jonah Ostroff), [Mirror Isles](mirror-isles.md) і Skipping Stones to Lonely Homes (Alan Hazelden), Promesst 1–3 (Sean Barrett). У дизайні також брали участь Patrick Traynor ([Patrick's Parabox](patricks-parabox.md)), Marc ten Bosch (Miegakure), Zach Polansky (Enigmash).
- Родичі за структурою «відкритий світ однокранних пазлів»: [A Monster's Expedition](a-monsters-expedition.md), [Islands of Insight](islands-of-insight.md), The Witness.
- **Осі варіацій:** дієслово героя — push / pull / swap / власне вміння; переправа через воду — камінь до берега / латаття / дзеркальний обмін; сила героя — вроджена / тимчасова від променя; кількість світів у пазлі — один / межа двох / Gold Room.

## Цікавинки для курсу
- Партія героїв з різними дієсловами над спільним полем — 🥉 (таблиця «герой × обʼєкт → дія»).
- Камінь, що ковзає водою до берега, і латаття як сходинка, що відпливає — 🥉 (ковзання до умови + стан клітини).
- Сила від променя, поки стоїш у ньому: стан, що залежить від трасування — 🥈 (перерахунок променів після кожного ходу).
- Схрещування механік: один рушій, у якому правила світів вмикаються прапорцями рівня — 🥇 (архітектура правил як даних).
- Дзеркальні клони героїв, що ходять разом — 🥈 (синхронний рух кількох аватарів з колізіями між собою).
- Undo без ліміту на стеку станів — 📎.

## Мапа на каталог
- Є: `move-4dir`, `move-by-input`, `keyboard-controls` ↔ крок · `push-object` ↔ воїн · `pull-object` ↔ злодій · `party-switch` ↔ перемикання героїв · `swap-on-contact` ↔ чарівник · `mirror-reflect`, `beam-tracing` ↔ промені й дзеркала · `impassable-cells` · `all-on-targets`, `reach-exit` · `undo-step`, `restart-level` · `world-map` ↔ оверворлд із входами в пазли · `fog-of-war` ↔ туман невідкритої суші · `field-scaling`, `player-camera` ↔ відʼїзд камери · `save-autosave`, `achievements-window`, `game-screen`, `pause-menu`, `settings-window`.
- **Нема** → пропозиції карток:
  - `+chain-push`, `+line-of-sight-swap` — див. heroes-of-sokoban.md; `+mirror-image-swap` — див. mirror-isles.md.
  - `+skipping-stone` «Камінь у воді ковзає до найближчого берега» · entities/move · 🥉 · слоти {stop: shore|pad}.
  - `+floating-stepping-pad` «Латаття: з каменем — сходинка, від сусіднього руху — відпливає» · entities/interact · 🥉.
  - `+beam-granted-ability` «Сила, поки стоїш у промені» · entities/state · 🥈 · слоти {colors}.
  - `+mechanic-crossover` «Рівень вмикає набір механік з кількох світів» · levels/format · 🥇.
  - `+open-world-puzzles`, `+overworld-travel` (уже пропоновані) · `+multi-agent-sync` (уже пропонована) ↔ клони, що ходять разом.

## Пропозиції до словників
- `+effect:skip_across(a, water)` — обʼєкт ковзає по воді до першої суші (відмінне від `slide`: зупинка — берег, а не упор).
- `+effect:drift(a)` — плавуча клітина відпливає від збурення.
- `+cond:in_beam(a, color)` — сутність стоїть у промені кольору.
- `+card:skipping-stone`, `+card:floating-stepping-pad`, `+card:beam-granted-ability`, `+card:mechanic-crossover` — див. вище.
- `+feature:fast-travel` — швидке переміщення між відкритими точками оверворлду.
- Вісь `actors` (уже кандидат у `classes.md`): тут `party` (герої з перемиканням) і клони в одному пазлі.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/499170/Order_of_the_Sinking_Star/) — 1000+ пазлів, чотири світи, перелік героїв, ігри-основи з авторами, мови, досягнення, Cloud.
- [Wikipedia](https://en.wikipedia.org/wiki/Order_of_the_Sinking_Star) — механіки чотирьох світів, комбіновані пазли 2D→3D, reset і rewind, 1400+ пазлів, 250+ годин, дати й платформи.
- [KeenGamer](https://www.keengamer.com/articles/reviews/pc-reviews/order-of-the-sinking-star-review-a-puzzle-marathon-that-trusts-you-to-find-the-answers-pc/) — сторони світу, перші герої, кристали, статуя з вогнем, клавіша перемикання, undo/restart.
- [AltChar](https://www.altchar.com/reviews/order-of-the-sinking-star-review-moving-stones-sinking-brains-agudf8w4smyH) — правила каменів і латаття, дзеркальні копії, туман оверворлду, камера.
- [Nintendo Everything](https://nintendoeverything.com/order-of-the-sinking-star-review-for-nintendo-switch-2/) — дієслова трьох героїв докладно, rewind, межі світів.
- [Pixel Twelve](https://pixeltwelve.com/articles/order-of-the-sinking-star-review) — Gold Rooms, відсутність підказок, читабельність кольорів.
- [Alan Hazelden: ігри](https://alan.draknek.org/games/) — оригінали Skipping Stones і Mirror Isles у браузері.
- YouTube: [пошук «Order of the Sinking Star gameplay»](https://www.youtube.com/results?search_query=Order+of+the+Sinking+Star+gameplay).

## Непевне
- (?) Уміння королеви, барда, друїда й човна — у джерелах лише імена; ролі не описані. Бард/друїд — з неофіційного гайда.
- (?) Назва західного світу: «The Promise» (рецензія) vs «Vault of the Beamcasters» (Wikipedia); сили кольорових променів не описані.
- (?) Що буває при контакті з монстром — поразка спроби чи блок; як працює вогняна статуя.
- (?) Чи латаття везе героя (одне джерело) — інше каже лише про камінь на лататті.
- (?) Точна кількість пазлів: 1000+ (Steam), 1400+ (Блоу в Wikipedia).
- (?) Пункти меню й налаштувань — не описані в джерелах.
