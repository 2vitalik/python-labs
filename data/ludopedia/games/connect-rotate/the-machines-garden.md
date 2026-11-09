---
title: The Machine's Garden
slug: the-machines-garden
aka: []
family: connect-rotate
also: [thinky]
klass: avatar
axes:
  field: hex
  time: turn
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2020
platforms: [PC, iOS, Android]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1317310/The_Machines_Garden/", best: true, note: "сторінка Steam: 35+ гекс-пазлів, «спецклітини запускають, приєднують і розмножують гекси», сюжет про військовий суперкомпʼютер"}
  - {kind: itch, url: "https://toomuchtomato.itch.io/the-machines-garden", note: "itch: 36 пазлів, Windows-збірка, лінки на App Store / Google Play; відгук «пройти кожну клітину рівно раз»"}
  - {kind: other, url: "https://www.pocketgamer.com/articles/083870/the-machines-garden-review-still-needs-some-time-to-grow/", note: "огляд мобільної версії: торкнутись кожного гекса без повернення, стіни, телепорти, дублікатори, перемотка, журнал, мапа-гекс"}
  - {kind: other, url: "https://indie-hive.com/machine-garden", note: "огляд: зайняти всі клітини, у зайняті не можна, відкат тапом по клітині, стіни/телепорти/дублікатори/гальма руху"}
  - {kind: other, url: "https://www.gameshedge.com/?p=37077", note: "огляд: блоки, що приєднуються, мультиплікатори, мапа рівнів-гексів з відкриттям сусідніх"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2191929808", note: "гайд-розвʼязки: 37 рівнів + епілог, 2 досягнення"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Machine%27s+Garden+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [visited-trail, path-cut, teleport, impassable-cells, stick-together, no-moves-left, completion-detection, world-map, level-unlock, sequential-levels, game-screen, map-window, +hex-grid-render, +move-6dir-hex, +fill-all-cells, +multi-agent-sync, +launch-cell, +move-inhibitor-cell, +story-journal]
proposes: ["+trigger:stuck", "+window:journal-terminal", "+card:launch-cell", "+card:duplicate-avatar"]
author: opus
date: 2026-11-09
---

# The Machine's Garden — проведи гекс через кожну клітину гекс-поля рівно раз, використовуючи телепорти, запуски й дублікатори

## Суть
Короткий наративний пазл Jon Miller і Michael Schmitt (Too Much Tomato): гравець веде «гекс» сусідніми клітинами гексагонального поля й має зайняти **всі клітини, не ступаючи двічі** — гамільтонів шлях на гекс-сітці. Ускладнюють спецклітини, які, за описом, «запускають, приєднують і розмножують гекси»: телепорт, дублікатор (другий гекс в іншому місці), клітина, що приєднує блок, стіни й гальма руху. Між рівнями — записи журналу про пробудження військового суперкомпʼютера.

## Поле і час
- Гексагональна сітка рівня, 6 сусідів; на пізніх рівнях поле обставлене стінами й спецклітинами; видно цілком.
- Зайняті клітини лишаються позначеними (слід) і непрохідні.
- Хід = переміщення гекса на сусідню клітину; без вводу нічого не змінюється.
- Головне меню — теж гекс-сітка: рівні-гекси, пройдений відкриває сусідні.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гекс гравця | player | позиція | крок на вільну сусідню клітину, займає її |
| Вільна клітина | terrain | — | має бути зайнята рівно раз |
| Зайнята клітина (слід) | mark | — | непрохідна; тап по ній відкочує шлях до неї |
| Стіна | static | — | блокує рух на сусідню клітину |
| Телепорт | terrain | пара (?) | переносить гекс в іншу точку поля |
| Дублікатор («multiply») | spawner | — | створює другий гекс в іншій частині поля |
| Клітина-приєднання («attach») | terrain | — | приєднує до гекса блок, яким теж треба керувати (?) |
| Клітина-запуск («launch») | terrain | напрям (?) | запускає гекс (?) |
| Гальмо руху | terrain | — | «movement inhibitor» — обмежує рух (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap|dir, cell)` → ЯКЩО `free(cell)` and not `occupied(cell, trail)` → ТО `move(hex, cell)`, `mark(cell, taken)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(target, wall)` або `occupied(target, trail)` → ТО `block`.
- КОЛИ `enter(hex, teleporter)` → ТО `teleport(hex, pair)`, `mark(exit, taken)` (?).
- КОЛИ `enter(hex, duplicator)` → ТО `spawn_at(hex, other_cell)`; далі обидва гекси рухаються одним вводом (?).
- КОЛИ `enter(hex, attach_cell)` → ТО `attach(hex, block)` (?).
- КОЛИ `enter(hex, launch_cell)` → ТО `custom: «гекс запускається в напрямку клітини»` (?).
- КОЛИ `enter(hex, inhibitor)` → ТО `custom: «обмеження руху»` (?).
- КОЛИ `no_moves(hex)` → ЯКЩО not `cover_all(cells)` → ТО `custom: «застряг: лише відкат або рестарт»`.
- КОЛИ `input(tap, taken_cell)` → ТО `undo(n)` — шлях відкочується до цієї клітини.
- КОЛИ `input(restart)` → ТО `restart`.
- КОЛИ `all_constraints_met` (`cover_all(cells)`) → ТО `win`, `window(journal)`, `unlock(adjacent_level_hexes)`.
- Перемога: зайнято всі клітини. · Поразка: нема; глухий кут лікується відкатом. · Рахунок: нема (ні мінімуму ходів, ні зірок).

## Керування і ввід
- Тач / миша: тап по сусідній клітині — крок; тап по вже зайнятій — відкат до неї.
- Клавіатурні напрями (?) — у гайді епілогу «move right three times».

## Вікна, меню, HUD
- `main-menu` = `map-window`: велика гекс-сітка рівнів; пройдений рівень відкриває сусідні; термінал суперкомпʼютера.
- `journal-terminal` (custom-window): записи журналу, що зʼявляються після кожного рівня; минулі можна перечитати в терміналі.
- `game-screen`: поле-гекс без лічильників; окремого меню налаштувань нема.
- Епілог — окремий фінальний рівень.

## Фічі поза полем
- `levels-sequential` + `level-unlock` + `world-map`: 35–37 рівнів + епілог; відкриваються сусідні гекси мапи.
- `rewind` тапом по сліду + `restart-level`; підказок, налаштувань, редактора нема.
- `achievements`: 2 (після 14 пазлів і після фіналу).
- Сюжет журналом: супутній, на правила не впливає.

## Варіації й родичі
- [LYNE](lyne.md), [Flow Free](flow-free.md) — заповнити поле лініями; [Hands of Time](hands-of-time.md) — шлях з обмеженнями; [Tantrix](tantrix.md), [Entanglement](entanglement.md), [Palago](palago.md) — гекс-поле в сімʼї.
- Головоломки «одним розчерком»: pencil-logic (Haisu), лицарський тур ([n-queens-knights-tour](../pencil-logic/n-queens-knights-tour.md)).
- Осі варіацій: **поле**: квадрат / гекс · **агентів**: один / дублікатор додає синхронного другого · **розрив шляху**: нема / телепорт / запуск · **відкат**: рестарт / тап по сліду.

## Цікавинки для курсу
- Шлях на гекс-сітці з 6 сусідами (координати axial/cube) — 📎.
- Слід непрохідний + відкат тапом до будь-якої клітини сліду (обрізати стек) — 🌱.
- Перевірка «застряг»: нема вільних сусідів, а клітини лишились — 🌱; рання відсічка «поле розпалось на дві частини» — 🥉.
- Дублікатор: два гекси під одним вводом, кожен займає свою клітину — 🥉.
- Розвʼязувач гамільтонового шляху з телепортами (DFS з відсіканням звʼязності) — 🥇.
- Мапа рівнів як гекс-сітка, де пройдений відкриває сусідів — 📎.

## Мапа на каталог
- Є: `visited-trail` ↔ слід; `path-cut` ↔ відкат тапом; `teleport`; `impassable-cells` ↔ стіни; `stick-together` ↔ приєднаний блок (?); `no-moves-left` ↔ застряг; `completion-detection`; `world-map` + `level-unlock` + `sequential-levels` + `map-window`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` (у корпусі вже багато) · `+move-6dir-hex` «Рух на 6 сусідів гекс-сітки» · entities/move · 📎.
  - `+fill-all-cells` — зайняти кожну клітину рівно раз.
  - `+multi-agent-sync` — дублікатор (?).
  - `+launch-cell` «Клітина-запуск» · entities/interact · 🌱 (?).
  - `+move-inhibitor-cell` «Клітина-гальмо руху» · entities/interact · 🌱 (?).
  - `+story-journal` «Запис журналу після рівня» · interface/menus · 🌱.

## Пропозиції до словників
- `+trigger:stuck` — у агента нема ходів, але ціль не досягнута (точніше за `no_moves` для одиночних пазлів).
- `+window:journal-terminal` — архів сюжетних записів, що відкриваються проходженням.
- `+card:launch-cell`, `+card:duplicate-avatar` — клітина, що створює другого аватара під тим самим вводом.

## Джерела
- ⭐ [Steam: The Machine's Garden](https://store.steampowered.com/app/1317310/The_Machines_Garden/) — 35+ гекс-пазлів, спецклітини «launch, attach, multiply», 07.08.2020.
- [itch.io](https://toomuchtomato.itch.io/the-machines-garden) — 36 пазлів, мобільні версії, відгук «кожна клітина рівно раз».
- [Pocket Gamer: огляд](https://www.pocketgamer.com/articles/083870/the-machines-garden-review-still-needs-some-time-to-grow/) — правило без повернень, стіни, телепорти, дублікатори, перемотка, журнал, мапа, без налаштувань.
- [Indie Hive: огляд](https://indie-hive.com/machine-garden) — зайняти всі, тап для відкату, «you're stuck», чотири механіки.
- [Games Hedge: огляд](https://www.gameshedge.com/?p=37077) — приєднаний блок, мультиплікатори, відкриття сусідніх рівнів.
- [Steam-гайд розвʼязків](https://steamcommunity.com/sharedfiles/filedetails/?id=2191929808) — 37 рівнів + епілог, 2 досягнення.
- YouTube: пошук «The Machine's Garden gameplay».

## Непевне
- (?) Точна дія «launch», «attach» і гальма руху — огляди лише називають; таблиця — здогад з описів.
- (?) Чи дублікат рухається синхронно з першим гексом (скриншот Indie Hive: «дубль без вільних сусідів — застряг» натякає, що так).
- (?) Стіни — на клітинах чи на ребрах між гексами.
- (?) Кількість рівнів: 35 / 36 / 37 + епілог — джерела розходяться; macOS-збірка згадана лише в заголовку пошуку itch.
