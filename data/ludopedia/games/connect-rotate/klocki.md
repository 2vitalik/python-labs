---
title: klocki
slug: klocki
aka: [Klocki]
family: connect-rotate
also: [thinky]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2016
platforms: [PC, Mac, Linux, iOS, Android]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/499440/klocki/", best: true, note: "опис: зʼєднати всі лінії; нові дії — розділити, повернути, перевернути, зсунути; без таймерів і очок"}
  - {kind: other, url: "https://apps.apple.com/gb/app/klocki/id1105390093", note: "App Store: опис, Cloud Save (2022), історія версій"}
  - {kind: other, url: "https://gameramble.com/klocki-PC-Review", note: "огляд: обмін лініями кліком, криві, 3D, крапки, що не торкаються, перемикачі; 80+ пазлів, лише вимкнення музики"}
  - {kind: other, url: "https://www.commonsensemedia.org/app-reviews/klocki", note: "огляд: тап міняє плитки місцями, лінії фіксуються; затінені плитки відкривають крапки"}
  - {kind: other, url: "https://www.macstories.net/reviews/game-day-klocki/", note: "огляд: обмін парами плиток, 2D → 3D, без тексту й туторіалу"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=726764889", note: "картинковий гайд: розвʼязки всіх рівнів, у коментарях — правило крапок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=klocki+game+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [cell-click, tile-rotate, pipe-connectors, connectivity-check, satisfy-constraints, completion-detection, button-toggle, sequential-levels, game-screen, background-music, music-toggle, sound-effects, save-progress, +tile-swap, +line-lock-on-connect, +cube-face-adjacency, +rules-without-text]
proposes: ["+effect:flip", "+effect:lock", "+trigger:all_connected", "+feature:no-text-onboarding", "+card:tile-swap", "+card:line-lock-on-connect", "+card:cube-face-adjacency"]
author: opus
date: 2026-11-09
---

# klocki — міняй місцями плитки з відрізками ліній, доки всі лінії на блоці не зійдуться; кожен «світ» додає нову дію

## Суть
Мінімалістичний пазл Maciej Targoni (автора [Hook](hook.md)): на кожному екрані — блок із плиток, на плитках відрізки ліній; треба, щоб усі лінії зʼєдналися. Базова дія — тап по плитці міняє її місцями з іншою; правильно зʼєднані лінії фіксуються й світяться. Далі гра без жодного тексту вводить нові дії й об'єкти: криві лінії, обертання, ковзання, розділення блоків, важелі, тривимірні блоки з лініями на гранях і рівні з крапками, які не мають торкатися. Без таймера, очок і зірок.

## Поле і час
- Один екран — один блок (2D-плита, згодом ізометричні 3D-фігури з плитками на кількох гранях). Плитки квадратні, лінії переходять через межі плиток і граней.
- Статичний пазл: нічого не відбувається без дотику; рівень завершується миттєво, щойно виконано умову.
- 80+ рівнів (огляди: «більше 80», «80–90»); після останнього гра повертається до першого.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка з лінією | tile | відрізок: прямий / кривий; положення | тап — обмін місцями; правильно зʼєднана — фіксується й світиться |
| Блок | zone | форма 2D або 3D, грані | носій плиток; лінії мають зійтися на всьому блоці |
| Частина блока | object | — | у пізніх рівнях блок розділений на шматки, які зсуваються / зʼєднуються (?) |
| Затінена плитка | tile | чорна | рівні з крапками: переставляєш, щоб відкрити білі крапки |
| Біла крапка | mark | — | дві крапки (чорні квадрати) не стоять поруч у рядку чи стовпці; по діагоналі можна |
| Важіль | switch | жовта кулька на стрижні | перемикає / рухає частини блока (?) |
| Фігура-заливка | tile | частина серця, овалу, кола | плитки складають цілі фігури (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, tile)` → ЯКЩО `not state(tile, locked)` → ТО `swap(tile, other)` (з якою плиткою — див. «Непевне»).
- КОЛИ `after(swap)` → ЯКЩО `custom: «кінці відрізків на спільних межах плиток збігаються»` → ТО `set_state(lines, locked)`, `custom: «лінії світяться»`.
- КОЛИ `all_constraints_met` → ТО `sound(gong)`, `custom: «тап — наступний рівень»` → `next_level`.
- Рівні з крапками: КОЛИ `input(click, shaded_tile)` → ТО `swap`; КОЛИ `all_constraints_met` → ЯКЩО `no_adjacent(shaded_tile)` (ортогонально; діагональ дозволена) → ТО рівень пройдено.
- Пізні рівні: КОЛИ `input(drag, part)` → ТО `slide(part, dir)` (?); КОЛИ `input(click, piece)` → ТО `rotate(piece, 90)` (?); перевертання частини — `custom: «перевернути (flip)»` (?).
- КОЛИ `input(click, lever)` → ТО `custom: «важіль змінює положення частин блока»` (?).
- 3D-рівні: КОЛИ `after(swap)` → ЯКЩО `custom: «лінія переходить через ребро куба на сусідню грань і там продовжується»` → ТО з'єднання зараховується.
- Перемога: усі лінії зʼєднані (або крапки розставлено за правилом) · Поразки нема · Рахунку нема.

## Керування і ввід
- Лише миша / тап (Steam-тег Mouse Only): тап по плитці — обмін; пізніше — перетягування й тапи по важелях (?).
- Після розвʼязання — тап по екрану, щоб перейти далі: темп задає гравець.

## Вікна, меню, HUD
- Нема титульного екрана, туторіалу й тексту: гра стартує одразу з першого пазла.
- `game-screen`: блок по центру на пастельному тлі, маленька кругла кнопка в кутку (меню (?)).
- `settings-window` (?): єдине налаштування — вимкнути музику.
- `level-select` (?): огляд Gameramble — «можна перейти до будь-якого пазла»; GameBrain — «нема вибору рівня й індикатора прогресу».

## Фічі поза полем
- `levels-sequential`; після фіналу — знову з першого рівня.
- `music-toggle`; саундтрек Wojciech Wasiak; звук перемоги не вимикається.
- `cloud-save` (Steam Cloud; iOS — з версії 1.9, 2022).
- `achievements`: одне Steam-досягнення «The End» — пройдено всі рівні.
- Ні очок, ні таймерів, ні зірок, ні реклами; `onboarding-hints` замінено самими рівнями.

## Варіації й родичі
- Того ж автора: [Hook](hook.md) (2015), PUSH (2017), Up Left Out (2018, ковзання плиток з гачками), Naboki (2019).
- Корпус: [Infinity Loop](infinity-loop.md) — та сама мета «зʼєднай усе», але дія — поворот плитки, а не обмін; [Plumber / Pipes](plumber-pipe-rotation.md); [Flow Free](flow-free.md) — лінії малюють, а не збирають.
- Осі варіацій: **дія над плиткою** — обмін / поворот / ковзання / перевертання / розділення · **поверхня** — плоска плита / грані 3D-фігури · **мета** — звʼязати лінії / розставити крапки без сусідства / скласти фігури.

## Цікавинки для курсу
- Обмін двох плиток і перевірка збігу портів на спільних межах — 🌱.
- Фіксація зʼєднаних плиток (вони більше не міняються) — 🌱.
- Лінії на гранях 3D-фігури: суміжність клітин через ребро куба (розгортка) — 🥈.
- Рівні з крапками: обмеження «без ортогональних сусідів» + обмін — 📎.
- Важіль, що рухає частину блока — 📎.
- Онбординг без тексту: послідовність рівнів, кожен вводить одну дію — 🥉 (дизайн рівнів, не код).

## Мапа на каталог
- Є: `cell-click` ↔ тап по плитці; `tile-rotate` ↔ поворот у пізніх рівнях (?); `pipe-connectors` ↔ кінці ліній на межах плиток; `connectivity-check` ↔ усі лінії зʼєднані; `satisfy-constraints`, `completion-detection`; `button-toggle` ↔ важіль; `sequential-levels`; `game-screen`; `background-music`, `music-toggle`, `sound-effects` ↔ гонг; `save-progress` ↔ Cloud Save.
- **Нема** → пропозиції карток:
  - `+tile-swap` «Обмін двох плиток місцями» · entities/legality · 🌱.
  - `+line-lock-on-connect` «Зʼєднана плитка фіксується» · game-logic/constraints · 🌱.
  - `+cube-face-adjacency` «Сусідство клітин через ребро 3D-фігури» · entities/space · 🥈.
  - `+rules-without-text` «Правила вчать рівні, без тексту» · interface/onboarding · 🥉.

## Пропозиції до словників
- `+effect:flip` — перевернути плитку / частину (підтвердження, ×7 у корпусі).
- `+effect:lock` — зафіксувати сутність, дія над нею більше не діє.
- `+trigger:all_connected` — усі лінії / порти зʼєднані (частковий випадок `all_constraints_met` для сімʼї connect-rotate).
- `+feature:no-text-onboarding` — гра без тексту й туторіалу, правила відкриваються рівнями.
- `+card:tile-swap`, `+card:line-lock-on-connect`, `+card:cube-face-adjacency`.

## Джерела
- ⭐ [Steam: klocki](https://store.steampowered.com/app/499440/klocki/) — опис (connecting, separating, rotating, turning, sliding), без таймерів і очок, теги, платформи, дата 13.07.2016.
- [App Store: klocki](https://apps.apple.com/gb/app/klocki/id1105390093) — опис, Cloud Save, історія версій.
- [Gameramble: klocki PC Review](https://gameramble.com/klocki-PC-Review) — клік міняє лінію місцями, гонг, криві, 3D, крапки, перемикачі, 80+ пазлів, цикл після фіналу.
- [Common Sense Media: klocki](https://www.commonsensemedia.org/app-reviews/klocki) — перший рівень: дві плитки, тап — обмін, лінії фіксуються; затінені плитки відкривають крапки.
- [MacStories: Game Day — klocki](https://www.macstories.net/reviews/game-day-klocki/) — обмін парами плиток, 2D → 3D, тап для переходу, без тексту.
- [Steam-гайд: klocki 100% Picture-guide](https://steamcommunity.com/sharedfiles/filedetails/?id=726764889) — розвʼязки рівнів; коментар автора: чорні квадрати не поруч у рядку / стовпці, по діагоналі можна.
- GameBrain (https://gamebrain.co/game/klocki) — зведення відгуків: ковзання, обертання, обмін, заливка фігур, важелі; «нема вибору рівня».

## Непевне
- (?) Обмін: тап по одній плитці міняє її з сусідньою чи треба тапнути дві — огляди формулюють по-різному.
- (?) Точна дія світів «розділити / повернути / перевернути / зсунути» — Steam лише перелічує; з картинок гайду (розвʼязані стани) механіку не відновити.
- (?) Важіль: що саме перемикає; «заливка фігур» (серця, овали) — лише згадка у відгуках.
- (?) Вибір рівня: Gameramble — «можна перейти до будь-якого пазла», GameBrain — «нема»; кругла кнопка в кутку — призначення не перевірено.
- (?) Кількість рівнів: «80+» / «80–90»; гайд має 82 знімки.
