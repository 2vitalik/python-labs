---
title: Unblock Me і Parking Jam 3D (мобільні Rush Hour)
slug: unblock-me
aka: [Unblock Me Free, Unblock Me Premium, Parking Jam 3D, Car Parking Jam, Розблокуй мене]
family: push-slide
also: []
klass: figure
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2009
platforms: [iOS, Android, Mac]
links:
  - {kind: other, url: "https://apps.apple.com/us/app/unblock-me/id315019111", best: true, note: "App Store Unblock Me (Kiragames): 18 000+ пазлів, режими Relax/Challenge, Easy Game, Fixed Block Mode, підказки, досягнення, теми"}
  - {kind: official, url: "https://www.kiragames.com/", note: "Kiragames: Unblock Me Free і Premium (без реклами), лінки на магазини"}
  - {kind: other, url: "http://play.google.com/store/apps/details?id=com.kiragames.unblockmefree", note: "Google Play Unblock Me Free (сторінка у фетчі майже порожня)"}
  - {kind: other, url: "https://apps.apple.com/app/1498229533", note: "App Store Parking Jam 3D (Popcore): порядок виїзду, аварії, Granny, челенджі, монети, скіни, життя, реклама за ходи"}
  - {kind: official, url: "https://popcore.com/", note: "Popcore: Parking Jam 3D — «un-parking master», машини перевертаються після одного хибного ходу"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Sliding_puzzle", note: "рід ковзних пазлів; Rush Hour серед прикладів, мобільних клонів не описує"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=unblock+me+gameplay", note: "пошук; Unblock Me"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=parking+jam+3d+gameplay", note: "пошук; Parking Jam 3D"}
stage: v1
coverage: 60
mechanics: [multi-cell-size, impassable-cells, reach-exit, drag-drop-piece, swipe-gestures, level-bank, difficulty-levels, level-select, level-unlock, sequential-levels, mode-select, move-counter, move-limit, restart-level, undo-step, round-currency, shop-window, achievements-window, theme-select, collect-all, +axis-locked-move, +hint-currency, +rewarded-ad, +exit-by-direction, +crash-on-blocked, +lives-energy, +idle-income]
proposes: ["+effect:drive_out", "+trigger:exited", "+feature:rewarded-ad", "+feature:hint-currency", "+feature:lives-energy", "+feature:idle-income", "+card:exit-by-direction", "+card:crash-on-blocked", "+role:neutral"]
author: opus
date: 2026-11-09
---

# Unblock Me і Parking Jam 3D — Rush Hour на телефоні: банк із тисяч рівнів, підказки за валюту/рекламу; у Parking Jam — виїжджають усі машини, напрям задає свайп

## Суть
Обидві гри — мобільні нащадки [rush-hour.md](rush-hour.md); тут лише **відмінності**. **Unblock Me** (Kiragames, 2009 (?)) — та сама механіка дерев'яних брусків 1×2/1×3, що ковзають уздовж своєї осі, щоб червоний брусок вийшов праворуч; новизна — банк понад 18 000 пазлів за рівнями складності, режими Relax/Challenge, Fixed Block Mode (нерухомі блоки) і підказки як витратна валюта. **Parking Jam 3D** (Popcore) перевертає ціль: виїхати мають **усі** машини, свайп запускає машину в напрямку осі, і вона їде, доки не виїде з парковки або не вріжеться — порядок виїзду і є пазлом.

## Поле і час
- Unblock Me: поле 6×6 з виходом праворуч на рядку червоного бруска (як Rush Hour); у Fixed Block Mode — нерухомі блоки-перешкоди.
- Parking Jam 3D: парковка-сітка довільної форми з перешкодами (стовпці, клумби), машини різної довжини (є «автобусні» рівні); виїзд — через будь-який край на дорогу довкола.
- Час: Unblock Me — `static` (світ змінюється лише ходом). Parking Jam — хід анімований (машина проїжджає), можлива рухома перешкода (Granny), але сам пазл покроковий.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Червоний брусок (Unblock Me) | piece | 1×2, горизонтальний | дійшов до виходу — рівень пройдено |
| Брусок (Unblock Me) | piece | 1×2 / 1×3, H/V | ковзає вздовж осі на N вільних клітин |
| Фіксований блок (Unblock Me) | static | 1×1 (?) | не рухається (Fixed Block Mode) |
| Машина (Parking Jam) | piece | довжина, вісь, колір | свайп уздовж осі → їде до краю або до перешкоди |
| Автобус (Parking Jam) | piece | довша | те саме; рівні з автобусами найважчі (відгуки) |
| Перешкода парковки | static | — | машина в неї врізається |
| Granny (Parking Jam) | neutral | — | ходить між машинами, перевертає й відкидає машини (опис App Store) |
| Вихід / дорога | zone | краї поля | машина, що доїхала, зникає з поля |

## Правила (КОЛИ → ЯКЩО → ТО)
- Unblock Me — правила Rush Hour: КОЛИ `input(drag, block, n)` → ЯКЩО `custom: «уздовж осі бруска»` і `free(n клітин)` → ТО `move(block, n)`, `counter(moves, +1)`; КОЛИ `reach(red, exit)` → ТО `win`.
- Fixed Block Mode: КОЛИ `input(drag, fixed_block)` → ТО `block`.
- КОЛИ `input(hint)` → ЯКЩО `counter(hints, >, 0)` → ТО `counter(hints, -1)`, `custom: «показати наступний хід розвʼязку»`.
- КОЛИ `custom: «новий день»` → ТО `give(player, hints)`; КОЛИ `custom: «переглянуто рекламу»` → ТО `custom: «денні підказки ×2»`.
- Parking Jam: КОЛИ `input(swipe, car, dir)` → ЯКЩО `custom: «dir уздовж осі машини (вперед або назад)»` → ТО `slide(car, dir)`.
- КОЛИ `reach(car, edge)` → ТО `custom: «машина виїжджає на дорогу й зникає»` (+effect:drive_out), `counter(cars_left, -1)`.
- КОЛИ `blocked(car)` → ЯКЩО `occupied(cell_ahead, car)` → ТО `custom: «аварія: машини стикаються / перевертаються»`, `lives(-1)` (?).
- КОЛИ `contact(granny, car)` → ТО `custom: «Granny перевертає й відкидає машину»`.
- КОЛИ `all_gone(car)` → ТО `win`, `currency(+n)`, `next_level`.
- КОЛИ `counter(moves, =, 0)` → ЯКЩО `custom: «переглянуто рекламу»` → ТО `counter(moves, +n)`; інакше `lose` (?).
- Перемога: червоний на виході (Unblock Me) / парковка порожня (Parking Jam). · Поразка: Unblock Me — нема; Parking Jam — скінчились ходи/життя (?). · Рахунок: кількість ходів (Unblock Me), монети за рівень (Parking Jam).

## Керування і ввід
- Unblock Me: drag бруска пальцем уздовж осі, привʼязка до сітки (як цифровий Rush Hour); кнопки підказки, рестарту, undo (?).
- Parking Jam: свайп по машині в бік руху — машина сама доїжджає; керувати довжиною ходу не можна (до упору, як [ice-sliding-puzzles.md](ice-sliding-puzzles.md)).

## Вікна, меню, HUD
- Unblock Me: `main-menu` → `mode-select` (Relax / Challenge / Fixed Block) → `difficulty-select` → `puzzle-select` (сітка пазлів з позначками «розвʼязано»); пауза → «Puzzles» відкриває рівні складності (відповідь розробника в App Store).
- Unblock Me `game-screen`: поле, `move-counter`, `par-moves` (?), `hint-button` з лічильником, `restart-button`, `pause-button`.
- `shop-window`: пакети підказок 30–1000 (Unblock Me), Remove Ads; Parking Jam — гроші, «Life Restore».
- `achievements-window` (Game Center, Unblock Me); `settings-window` / `skin-select` — сезонні теми (Unblock Me), скіни машин і сцени (Parking Jam).
- Parking Jam: `game-screen` з лічильником ходів і `lives` (сердечка); `end-screen` з монетами і пропозицією «×2 за рекламу»; `map-window` (мапи/челенджі), `daily-window` — дошка денних челенджів, місячні трофеї; idle-екран будівництва нерухомості (`custom-window`).
- Переходи: main-menu → game-screen → end-screen (нагорода, реклама) → наступний рівень.

## Фічі поза полем
- `puzzle-bank` на 18 000+ пазлів з `difficulty-presets` (Unblock Me: від Easy до Expert (?)); `mode-zen` ≈ Relax, Challenge — з оцінкою (?).
- `hint` як валюта: денні безкоштовні, купівля пакетів, подвоєння за рекламу (rewarded ad).
- `daily-puzzle` → перероблено у Fixed Block Mode (Unblock Me 2.4.2).
- `achievements`, `cloud-save`-подібна синхронізація прогресу після офлайну (Unblock Me).
- Parking Jam: `levels-sequential`, челенджі й денні дошки, `streaks`/трофеї, `unlockables` (машини, скіни, сцени), життя-енергія, idle-дохід із нерухомості, реклама після рівнів.
- Генератор рівнів: банк Unblock Me, ймовірно, згенерований і відсортований за довжиною розвʼязку (?) — див. генерацію в `rush-hour.md` (Fogleman).

## Варіації й родичі
- [rush-hour.md](rush-hour.md) — оригінал: усі правила руху; Unblock Me = Rush Hour + банк + підказки.
- [klotski.md](klotski.md) — фігури 2×2, рух у будь-який бік; [sliding-tile-permutation.md](sliding-tile-permutation.md) — 15-puzzle.
- [ice-sliding-puzzles.md](ice-sliding-puzzles.md), [tomb-of-the-mask.md](tomb-of-the-mask.md) — рух «до упору» від свайпа, як машини Parking Jam.
- Інші клони: Blocked (2009), Car Parking Jam, Parking Jam Out, Traffic Escape (?).
- **Осі варіацій:**
  - ціль: вивести одну фігуру (Unblock Me) / вивести всі (Parking Jam);
  - довжина ходу: будь-яка кількість клітин drag-ом / до упору свайпом;
  - виїзд: одна щілина в бортику / будь-який край за напрямом осі;
  - помилка: безкоштовна (зворотний хід) / аварія, втрата життя;
  - монетизація підказок: нема / валюта + реклама.

## Цікавинки для курсу
- «Виїжджають усі»: свайп → машина їде до краю або до першої перешкоди; рівень = порядок звільнення (топологічне сортування залежностей «хто кого блокує») — 🥉.
- Детектор «машина вріжеться» до запуску (перевірка всього променя) і анімація аварії — 📎.
- Підказка «наступний хід» через BFS від поточного стану (а не з початку рівня) — 🥈.
- Генератор банку: випадкова розстановка → BFS → відбір за довжиною розвʼязку → сортування за складністю — 🥇.
- Режим фіксованих блоків як прапорець генератора — 🌱.
- Підказки як валюта з денним поповненням — 🌱 (стан між сесіями).

## Мапа на каталог
- Є: `multi-cell-size` + `drag-drop-piece` + `swipe-gestures` ↔ бруски/машини; `impassable-cells` ↔ фіксовані блоки, перешкоди парковки; `reach-exit` ↔ червоний на виході; `collect-all` ↔ «вивести всі машини»; `level-bank` + `difficulty-levels` + `level-select` + `level-unlock` + `sequential-levels` ↔ банк і рівні; `mode-select` ↔ Relax/Challenge/Fixed; `move-counter`; `move-limit` ↔ ходи Parking Jam; `restart-level`, `undo-step` (?); `round-currency` + `shop-window` ↔ монети, пакети підказок; `achievements-window`; `theme-select` ↔ сезонні теми, скіни.
- **Нема** → пропозиції карток:
  - `+axis-locked-move` — уже просив `rush-hour.md`.
  - `+exit-by-direction` «Фігура виїжджає за край у напрямку свайпа» · entities/move · 📎.
  - `+crash-on-blocked` «Рух до упору в іншу фігуру — аварія/штраф» · entities/death · 📎.
  - `+hint-currency` «Підказки як витратна валюта» · game-logic/economy · 🌱.
  - `+rewarded-ad` «Нагорода за перегляд реклами» · game-logic/economy · 🌱 — як патерн дизайну, не як вимога.
  - `+lives-energy` «Життя, що відновлюються з часом» · game-logic/lose · 📎.
  - `+idle-income` «Пасивний дохід між рівнями» · game-logic/economy · 📎.

## Пропозиції до словників
- `+effect:drive_out` — сутність їде за край і зникає з поля зарахованою (Parking Jam; також «вийти з рівня» у Lemmings-подібних); поки `custom`.
- `+trigger:exited` — сутність покинула поле через вихід/край (відмінне від `edge` — там «вийшов за межу» як помилка).
- `+feature:rewarded-ad`, `+feature:hint-currency`, `+feature:lives-energy`, `+feature:idle-income` — мобільні фічі поза полем.
- `+card:exit-by-direction`, `+card:crash-on-blocked` — див. «Мапу на каталог».
- `+role:neutral` — Granny (вже ⏳ у roles.md — просто підтвердження вжитку, не нове слово).

## Джерела
- ⭐ [App Store: Unblock Me](https://apps.apple.com/us/app/unblock-me/id315019111) — Kiragames, 18 000+ пазлів, Relax/Challenge, Easy Game, Fixed Block Mode (замість Daily Puzzle), пакети підказок 30–1000, денні підказки ×2 за рекламу, Remove Ads, досягнення Game Center, сезонні теми, офлайн із синхронізацією.
- [Kiragames](https://www.kiragames.com/) — Unblock Me Free/Premium, «red wooden block puzzle», лінки на магазини.
- [App Store: Parking Jam 3D](https://apps.apple.com/app/1498229533) — Popcore, порядок виїзду, аварії й перевертання, Granny, мапи й челенджі, монети/скіни/сцени, idle-нерухомість, реклама за ходи, Life Restore; відгуки: сердечка, автобусні рівні, денні дошки, місячні трофеї.
- [Popcore](https://popcore.com/) — опис Parking Jam 3D.
- [Wikipedia: Sliding puzzle](https://en.wikipedia.org/wiki/Sliding_puzzle) — рід ковзних пазлів (мобільних клонів не описує).
- [Google Play: Unblock Me Free](http://play.google.com/store/apps/details?id=com.kiragames.unblockmefree) — сторінка магазину (у фетчі без вмісту).

## Непевне
- (?) Рік виходу Unblock Me (2009 — за ID App Store і чергою, у джерелі не бачив).
- (?) Зірки за мінімум ходів, лічильник «мінімум» (par) і undo в Unblock Me — App Store про це мовчить.
- (?) Parking Jam: що саме коштує аварія (життя? хід?), чи машина при аварії відскакує назад, умова поразки — офіційний опис і відгуки неточні; механіку «їде до краю сама» дав лише сторонній опис жанру.
- (?) Чи рівні Unblock Me згенеровані алгоритмом — не сказано.
- (?) Розмір полів Parking Jam і наявність черги машин на виїзді.
