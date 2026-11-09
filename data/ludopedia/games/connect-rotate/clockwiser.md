---
title: Clockwiser
slug: clockwiser
aka: ["Clockwiser: Time is Running Out"]
family: connect-rotate
also: [push-slide]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 1994
platforms: [Amiga, Amiga CD32, DOS, Java, Android, iOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Clockwiser", best: true, note: "ядро: два поля, прямокутник за/проти годинника, гравітація, метал, телепорти, бомби; порти"}
  - {kind: other, url: "https://agdb.abime.net/DBA1/ClockW.html", note: "огляд Amiga: бомби, антигравітація, діаманти, ліміт часу після першого ходу, паролі, 4 іконки"}
  - {kind: other, url: "https://homeoftheunderdogs.net/game.php?id=2714", note: "огляд DOS: типи блоків, телепорт-капсули, редактор рівнів"}
  - {kind: other, url: "https://gamesdb.launchbox-app.com/games/details/81962-clockwiser-time-is-running-out", note: "100 рівнів Amiga/CD32, 110 DOS; таймер від першого ходу"}
  - {kind: other, url: "https://www.dazeland.com/en/Amiga/Clockwiser.html", note: "ввід мишею: намалювати прямокутник, клікнути один із двох годинників"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Clockwiser+Amiga+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [multi-select, selection-highlight, gravity-fall, impassable-cells, teleport-pair, explode-area, time-out, restart-level, sequential-levels, level-password, in-game-editor, game-screen, +rotate-ring-rect, +goal-state-check, +target-preview-board, +timer-starts-on-first-move, +anti-gravity-block, +spreading-terrain]
proposes: ["+effect:rotate_ring", "+trigger:landed", "+cond:matches_solution", "+effect:set_gravity", "+ui:target-board", "+card:rotate-ring-rect", "+card:target-preview-board"]
author: opus
date: 2026-11-09
---

# Clockwiser — виділи прямокутник і прокрути його обідок за чи проти годинника, щоб скласти зразок під дією гравітації

## Суть
Екран рівня має дві половини: ліва — активна, права — нерухомий зразок; треба, щоб ліва стала точно як права. Окремий блок посунути не можна: гравець виділяє прямокутну групу клітин і зсуває блоки вздовж краю прямокутника за годинниковою стрілкою чи проти. Блоки підкоряються гравітації, тож після зсуву все, під чим порожньо, падає. Пізніше додаються метал, телепорти, бомби, діаманти й антигравітаційні блоки, а кожен рівень має ліміт часу.

## Поле і час
- Дві квадратні сітки поруч: активна (ліворуч) і цільова (праворуч, лише показ). Розмір полів — (?).
- Покроково: стан змінюється лише від ходу-обертання (плюс падіння, що йдуть за ним). Таймер рівня — real-time, від секунд до хвилин; запускається першим ходом, тож рівень можна спершу роздивитись.
- Гравітація вниз для звичайних блоків; метал і блоки під дією антигравітації не падають.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Звичайний блок | object | колір/вигляд | рухається обертанням; падає без опори; руйнується бомбою |
| Металевий блок | static | — | не рухається, не руйнується (за фан-описом — і не падає (?)) |
| Бомба | object | — | рухається як блок; падаючи на блок, руйнує його (і, можливо, сусідні (?)); може везти на собі інші блоки |
| Діамант | object | — | впавши, «розмножується»: перетворює сусідні блоки (і порожнечу (?)) на діаманти |
| Телепорт-капсула | terrain | пара | переносить блок з однієї капсули в іншу |
| Антигравітаційний блок | object | — | блоки над ним не підкоряються гравітації |
| Зразок (права половина) | zone | розкладка блоків | ціль; не змінюється |
| Виділений прямокутник | zone | ширина × висота | обідок, що прокручується на хід |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, rect)` → ТО `custom: «виділити прямокутну групу клітин»`.
- КОЛИ `input(rotate_cw)` або `input(rotate_ccw)` → ТО `custom: «блоки на обідку прямокутника зсуваються на одну клітину вздовж краю за/проти годинника»` (`+effect:rotate_ring`).
- КОЛИ `input(rotate_cw)` → ЯКЩО `first_time` → ТО `timer(start)`.
- КОЛИ `after(rotate)` → ЯКЩО `free(cell_below)` і `not state(block, antigravity)` → ТО `fall(block)`.
- КОЛИ `custom: «бомба приземлилась на блок»` (`+trigger:landed`) → ТО `disappear(block_below)`, `custom: «сама бомба теж вибухає (?)»`.
- КОЛИ `custom: «діамант приземлився»` (`+trigger:landed`) → ТО `transform(neighbours, diamond)` (?).
- КОЛИ `enter(block, pod)` → ТО `teleport(block, pair_pod)`.
- КОЛИ `settled` → ЯКЩО `custom: «блок стоїть на антигравітаційному»` → ТО `set_state(blocks_above, antigravity)` (`+effect:set_gravity`) — до найближчого блока, що й так не падає (за GiantBomb).
- КОЛИ `custom: «рух зачіпає метал»` → ТО `block` (?).
- КОЛИ `settled` → ЯКЩО `custom: «ліва половина точно як права»` (`+cond:matches_solution`) → ТО `win`, `next_level`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `lose` (рівень заново (?)).
- КОЛИ `input(restart)` → ТО `restart`.
- Перемога: розкладка = зразок. · Поразка: вийшов час рівня. · Рахунок — (?) (огляди про очки мовчать).

## Керування і ввід
- Миша: намалювати прямокутник на активному полі, потім клікнути один із двох годинників — за або проти годинникової стрілки.
- Чотири іконки: обернути проти годинника, обернути за годинником, рестарт рівня, вихід.
- Мобільні порти (Android 2010, iOS 2014) — дотик (?).

## Вікна, меню, HUD
- `game-screen`: активне поле ліворуч, `+ui:target-board` (зразок) праворуч; `selection-highlight` прямокутника; `timer-countdown` рівня; `level-number` (?); іконки `custom-window`-панелі: ↺ / ↻ / `restart-button` / вихід.
- `level-password`: кожен рівень має свій пароль — продовжити з першого непройденого.
- `editor-window`: редактор рівнів (згадано в оглядах HOTU і Dazeland).
- `main-menu`, `end-screen` — (?).
- Переходи: main-menu → (пароль) → game-screen → (збіг) наступний рівень / (час) повтор.

## Фічі поза полем
- `levels-sequential`: 100 рівнів (Amiga, CD32), 110 (DOS); складність росте нерівно — легкі трапляються серед важких.
- `level-password` на кожен рівень.
- `level-editor`.
- `restart-level`; ліміт часу на рівень як підказка: короткий — розвʼязок в 1–2 ходи, довгий — кілька фаз (огляд AGDB).

## Варіації й родичі
- Порти: Java (2008, онлайн), Android (2010), iOS (2014).
- **Осі варіацій** «одного генератора ходу»:
  - обертання обідка прямокутника з гравітацією (Clockwiser) / поворот блока n×n разом із вмістом (Twiddle у `push-slide/sliding-tile-permutation`) / зсув ряду (Loopover) / кільце куль навколо шестерні (`falling-match/trouballs`, `hexic`);
  - мета: точна розкладка-зразок (Clockwiser, пʼятнашки) / збіг 3 і очищення (Hexic);
  - гравітація: нема / вниз з антигравітаційними винятками (Clockwiser).
- Не плутати з `spin-doctor` (ClockWerx): там паличка обертається навколо точки, а тут — блоки по периметру прямокутника.
- Родичі: `sliding-tile-permutation` (перестановка до цільового порядку), `cogs` (зсув до цілі), Boulder Dash-подібна гравітація (`dig-gravity`).

## Цікавинки для курсу
- Зсув обідка довільного прямокутника на клітину (список клітин периметра + циклічний зсув) — 📎.
- Гравітація після кожного ходу до стабілізації + антигравітаційний стовп — 🥉.
- Ефекти приземлення: бомба руйнує, діамант перетворює сусідів — 📎.
- Порівняння стану зі зразком + таймер, що стартує першим ходом — 🌱.
- Розвʼязувач BFS по станах поля (хід = прямокутник × напрям — гілкування велике) — 🥇.
- Редактор рівнів із двома полями (поле + зразок) і перевіркою розвʼязності — 🥈.

## Мапа на каталог
- Є: `multi-select` + `selection-highlight` ↔ прямокутник мишею · `gravity-fall` ↔ падіння · `impassable-cells` ↔ метал · `teleport-pair` ↔ капсули · `explode-area` ↔ бомба (площа вибуху — ?) · `time-out` ↔ ліміт рівня · `restart-level` · `sequential-levels` + `level-password` · `in-game-editor` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+rotate-ring-rect` «Циклічний зсув обідка виділеного прямокутника» · entities/move · 📎 · слоти {dir: cw|ccw, step: 1}.
  - `+goal-state-check` (є в корпусі) — стан проти цілі.
  - `+target-preview-board` «Зразок цільового стану поруч із полем» · interface/hud · 🌱.
  - `+timer-starts-on-first-move` «Таймер вмикається першим ходом» · game-logic/lose · 🌱.
  - `+anti-gravity-block` «Блок, що скасовує гравітацію над собою» · entities/move · 📎.
  - `+spreading-terrain` (є в корпусі) — діамант перетворює сусідів.

## Пропозиції до словників
- `+effect:rotate_ring` (повтор Trouballs) — циклічний зсув сутностей по замкненому контуру.
- `+trigger:landed` (повтор корпусу) — сутність завершила падіння.
- `+cond:matches_solution` (повтор корпусу) — стан поля збігається з цільовим.
- `+effect:set_gravity` (повтор корпусу) — змінити дію гравітації на сутності/стовпі.
- `+ui:target-board` — друга сітка-зразок поруч з активним полем.
- `+card:rotate-ring-rect`, `+card:target-preview-board` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Clockwiser](https://en.wikipedia.org/wiki/Clockwiser) — дві половини, хід прямокутником уздовж краю, гравітація, метал, телепорти, бомби, порти.
- [AGDB (abime): огляд Clockwiser](https://agdb.abime.net/DBA1/ClockW.html) — бомби як вибух і «носій», антигравітація, діаманти, що множаться, ліміт часу від першого ходу, 100 рівнів, пароль на кожен рівень, чотири іконки.
- [Home of the Underdogs](https://homeoftheunderdogs.net/game.php?id=2714) — типи блоків (цегла, метал, діаманти, бомби, телепорт-капсули), ліміт часу, редактор.
- [LaunchBox Games DB](https://gamesdb.launchbox-app.com/games/details/81962-clockwiser-time-is-running-out) — 100/110 рівнів, «diamond-producers», таймер стартує першим ходом.
- [Dazeland](https://www.dazeland.com/en/Amiga/Clockwiser.html) — намалювати прямокутник мишею, клік по одному з двох годинників, паролі, редактор.
- GiantBomb (сторінка «Clockwiser: Time is Running Out», бачив у пошуку, фетч 403) — опис де-гравітатора.
- YouTube: пошук «Clockwiser Amiga gameplay».

## Непевне
- (?) Чи прокручується лише обідок прямокутника, чи й внутрішні клітини (для прямокутників від 3×3); крок — одна клітина за клік — так прочитано «move along the rectangle's edge».
- (?) Що буде, якщо в обідку метал: хід заборонено чи метал лишається, а інші його оминають.
- (?) Бомба: руйнує лише блок під собою (Wikipedia) чи всіх сусідів разом із собою (пошуковий фрагмент фан-вікі).
- (?) Діамант: які саме клітини перетворює (лише сусідні блоки чи й порожні) — джерела розходяться.
- (?) Антигравітаційний блок vs «де-гравітатор» GiantBomb — один і той самий тип чи два.
- (?) Наслідок вичерпаного часу (рестарт, життя), рахунок, розміри полів, мінімальний розмір прямокутника.
- Плутанина черги: автоматика звʼязала Clockwiser з `connect-rotate/spin-doctor` — це різні ігри.
