---
title: Xonix (Ксонікс) / Qix / Volfied
slug: xonix
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: territory
year: 1984
platforms: [DOS (Xonix 1984), arcade (Qix 1981, Volfied 1989), mobile, web]
links:
  - {kind: wiki, url: "https://uk.wikipedia.org/wiki/Xonix", best: true, note: "Xonix: суша і море, точки на суші й у морі, слід, заливка області без точок"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Qix", note: "Qix: Stix, швидке/повільне малювання, Sparx, Fuse, 75 %, розділення двох Qix"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Volfied", note: "Volfied: 80 %, бос і дрібні вороги, сірі ящики з підсиленнями"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=xonix+dos+gameplay", note: "пошук; Xonix"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=qix+arcade+gameplay", note: "пошук; Qix"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=volfied+arcade+gameplay", note: "пошук; Volfied"}
stage: v1
coverage: 70
mechanics: [move-4dir, touch-death, player-death, random-walk, sequential-levels, progress-acceleration, event-points, combo-multiplier, item-pickup, temporary-modes, time-out, console-render, +region-fill, +territory-capture, +trail-vulnerable, +bounce-move, +border-crawler, +fuse-chaser, +percent-goal, +split-bonus, +slow-draw-bonus]
proposes: ["+effect:leave_trail", "+effect:fill", "+trigger:region_closed", "+cond:region_has", "+card:region-fill", "+card:border-crawler", "+card:fuse-chaser", "+card:percent-goal", "+ui:territory-percent", "+role:zone"]
author: opus
date: 2026-11-02
---

# Xonix / Qix — відрізай шматки моря слідом, заливай області без ворогів, захопи 75 % поля

## Суть
Гравець бігає по краю захопленої території («суші») і робить вилазки в незахоплену частину («море»), лишаючи вразливий слід. Коли слід повертається на сушу, відрізана частина моря, де нема ворогів, заливається й стає сушею — так поле відвойовується шматками, доки не набереться потрібний відсоток. Вороги-«мʼячі» відбиваються в морі й убивають, торкнувшись сліду; інші вороги повзають по суші/краях, тож безпечних місць нема.

## Поле і час
- Xonix: прямокутна сітка клітин двох типів — суша (по периметру на старті) і море (усередині); легко рендериться в текстовому режимі.
- Qix: та сама ідея на «пікселях»: межа поля + захоплені області; гравець ходить лише по межах і по своєму незамкненому Stix.
- Volfied: як Qix, кожен рівень має свій фон, захоплені ділянки відкривають картинку наступного рівня.
- Real-time: усі рухаються щотік; Xonix-мʼячі — по діагоналі; Qix — хаотична «лінійна фігура»; Qix має лічильник, що спускає нових Sparx.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор / Marker | player | життя | рух 4 напрямки по суші; у морі лишає слід |
| Суша (захоплене) | zone | частка поля | безпечна від морських мʼячів, по ній ходить гравець |
| Море (незахоплене) | zone | — | тут ходять морські вороги; заходити — лише зі слідом |
| Слід (trail / Stix) | hazard | власник — гравець | вразливий: дотик ворога — смерть гравця; повернення на сушу — стає сушею |
| Морський мʼяч (Xonix) | enemy | — | рух по діагоналі, відбивається від суші; дотик сліду/гравця — смерть |
| Сухопутний мʼяч (Xonix) | enemy | — | рух по діагоналі по суші, відбивається від моря; дотик гравця — смерть |
| Qix | enemy | 1 або 2 (з 3-го рівня) | хаотично рухається в незахопленому; дотик Stix або маркера на Stix — смерть |
| Sparx | enemy | лічильник появи | повзає всіма межами поля (крім незамкненого Stix); дотик — смерть |
| Super Sparx | enemy | — | мутований Sparx; може гнатися по незамкненому Stix |
| Fuse | hazard | — | спалах, що біжить по Stix до маркера, якщо той зупинився |
| Бос (Volfied) | boss | тип за рівнем | головний ворог; визначає, що «зовні» при відрізанні |
| Дрібні вороги (Volfied) | enemy | — | гинуть із бонусом, якщо опиняються у відрізаній області |
| Сірий ящик (Volfied) | pickup | — | підсилення: швидкість або зброя (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(target, land)` → ТО `move(player, dir)` (Qix: лише по межах).
- КОЛИ `move(player)` у море → ТО `leave_trail` — клітина стає слідом; (Qix: лише при утриманні Fast/Slow Draw).
- КОЛИ `contact(player, own_trail)` → ТО `block` (Qix: не можна перетинати чи повертатися своїм Stix) / `lose` (Xonix (?)).
- КОЛИ `enter(player, land)` зі слідом → ТО слід → суша; для кожної відрізаної області моря: ЯКЩО `not region_has(enemy)` → ТО `fill(region)` (стає сушею), `score(area)`.
- Qix: заливається область, де нема Qix (з двома — менша (?)); Volfied: «зовні» — бік, де бос; дрібні вороги всередині гинуть з бонусом.
- КОЛИ `contact(sea_ball, trail|player)` → ТО `lose` (життя −1, слід зникає (?)).
- КОЛИ `contact(land_ball, player)` → ТО `lose`.
- КОЛИ `tick` → ТО `move(ball, diag)`; ЯКЩО `blocked(ball)` (межа море/суша) → ТО `bounce(ball)`.
- КОЛИ `contact(qix, stix|marker_on_stix)` → ТО `lose`; Qix на межах і захопленому безпечний.
- КОЛИ `contact(sparx, marker)` → ТО `lose`.
- КОЛИ `idle(marker)` на незамкненому Stix (або глухий кут) → ТО `spawn(fuse)`, `custom: «Fuse біжить по Stix до маркера; рух його прибирає»`; `contact(fuse, marker)` → `lose`.
- КОЛИ `timer(meter)` (Qix) → ТО `spawn(sparx)`, згодом `transform(super_sparx)`.
- КОЛИ `counter(claimed%, ≥, target)` → ТО `next_level`, `score(+bonus × (claimed − target))` (Qix: 75 % за замовчуванням, 50–90 % налаштування; Volfied: 80 %; Xonix: 75 % (?)).
- КОЛИ `custom: «лінія розділила двох Qix у різні області»` → ТО `next_level`, `multiplier(+1)` до 9 на наступні рівні.
- Qix: область, обведена повністю Slow Draw → `score(×2)` (повільніше, але дорожче).
- Volfied: КОЛИ `contact(player, grey_box)` → ТО `custom: «підсилення: швидкість / зброя»`; зброєю можна вбити боса — теж кінець рівня.
- КОЛИ `level_start` → ТО `spawn(ball × level)` — більше мʼячів з кожним рівнем (Xonix (?)); Qix: більше Sparx, згодом лише Super Sparx.
- Перемога: відсоток поля. Поразка: 0 життів. Рахунок: площа залитого, бонус за відсоток понад ціль, множник розділень, ×2 за Slow Draw.

## Керування і ввід
- Xonix: стрілки — рух 4 напрямки; у морі курсор іде далі в останньому напрямку, доки не повернеш (?).
- Qix: 4-напрямний джойстик + кнопки Fast Draw і Slow Draw; без кнопки маркер ходить лише межами.
- Volfied: джойстик + кнопка «різати» (?).

## Вікна, меню, HUD
- `game-screen`: поле + `score`, `lives`, `level-number`, `territory-percent` (захоплено / ціль), Xonix — `timer-countdown` (?).
- Qix: лічильник появи Sparx угорі екрана (`progress-bar` до виходу нових ворогів), ціль у % на старті рівня.
- `splash-screen` / attract mode з демо («Spiral Death Trap» у Qix), `end-screen` GAME OVER, `leaderboard` (аркада).
- Volfied: між рівнями — показ відкритої картинки (`custom-window`) (?).
- Переходи: splash → game-screen → (% досягнуто) наступний рівень; (0 життів) → end-screen.

## Фічі поза полем
- `levels-sequential` з наростанням ворогів; `difficulty-presets` оператора аркади (поріг 50–90 % у Qix).
- Тематичні фони рівнів (Volfied), картинка як нагорода (у численних клонах — фото-«розкриття»).
- Нема збережень, undo, редактора.

## Варіації й родичі
- Qix (Taito, 1981) — оригінал на межах; Xonix (Ілан Рав, Дані Кац, 1984, DOS) — клітинний, з сушею й морем, двома видами мʼячів; Volfied (Taito, 1989) — бос, підсилення, картинки.
- Super Qix, Qix Adventure; безліч мобільних клонів «відкрий картинку».
- Сучасні .io: Paper.io / Splix.io — та сама заливка контуром, але проти інших гравців (див. `tron-light-cycles`).
- **Осі варіацій:**
  - поле: клітини (Xonix) / межі-лінії (Qix);
  - що заливається: область без ворогів / менша з двох / не та, де бос;
  - вороги: у морі / на суші / по межах (Sparx) / по сліду (Super Sparx, Fuse);
  - кара за зупинку: нема / Fuse;
  - ризик-винагорода: швидке малювання / повільне ×2;
  - мета: % поля / розділити ворогів / вбити боса зброєю.

## Цікавинки для курсу
- Заливка відрізаної області без ворогів — 🥈: flood fill від кожного ворога, все недосяжне → суша; класичне алгоритмічне завдання.
- Слід як вразлива тимчасова сутність, що стає сушею при поверненні — 📎.
- Мʼячі по діагоналі з відбиттям від межі двох типів клітин — 📎: відбиття окремо по x і y.
- Ворог, що повзе межею (Sparx) по графу ребер захопленої території — 🥇: межа змінюється після кожної заливки.
- Fuse за бездіяльність на сліді — 🌱.
- Розділення двох Qix з множником — 🥉: зв'язність області + стратегічний вибір.
- Відкриття картинки під захопленим (Volfied, клони) — 🌱 у GUI, хороший вау-ефект.

## Мапа на каталог
- Є: `move-4dir` · `touch-death` · `player-death` · `random-walk` (Qix) · `sequential-levels` · `progress-acceleration` (більше ворогів з рівнем) · `event-points` · `combo-multiplier` (множник розділень) · `item-pickup` + `temporary-modes` (Volfied) · `time-out` (Xonix (?)) · `console-render` (Xonix в текстовому режимі).
- **Нема** → пропозиції карток:
  - `+region-fill` «Заливка замкненої області без ворогів» · entities/interact · 🥈 · слот {rule: no_enemy|smaller|not_boss} — також у `tron-light-cycles`.
  - `+territory-capture` (запропоновано в `tron-light-cycles`).
  - `+trail-vulnerable` (запропоновано в `tron-light-cycles`).
  - `+bounce-move` (запропоновано в Chip's Challenge) — тут діагональне відбиття.
  - `+border-crawler` «Ворог по межі територій» · entities/move · 🥇 — Sparx.
  - `+fuse-chaser` «Переслідувач за бездіяльність по сліду» · entities/move · 📎 — Fuse.
  - `+percent-goal` «Ціль — % поля» · game-logic/win · 🌱 · слот {percent}.
  - `+split-bonus` «Розділити ворогів по областях» · game-logic/win · 🥉.
  - `+slow-draw-bonus` «Повільніше — дорожче» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:leave_trail` — клітина за гравцем стає слідом (див. `tron-light-cycles`); підтверджую другою грою.
- `+effect:fill` — уже кандидат `fill(region)`; потрібен параметр правила «яку область» — тому окремо `+cond:region_has(region, kind)`: чи є в області сутність виду.
- `+trigger:region_closed` — є як `pattern(region_closed)`; пропоную окремий тригер, бо подія тут від повернення на сушу, а не від шаблону на полі.
- `+card:region-fill`, `+card:border-crawler`, `+card:fuse-chaser`, `+card:percent-goal`.
- `+ui:territory-percent` — частка захопленого / ціль (Qix, Xonix, Paper.io).
- `+role:zone` — суша/море як зони з правилами руху для різних ворогів.

## Джерела
- ⭐ [Wikipedia (uk): Xonix](https://uk.wikipedia.org/wiki/Xonix) — автори й рік, суша/море, мʼячі на суші й у морі по діагоналі, слід, заливка області без мʼячів.
- [Wikipedia: Qix](https://en.wikipedia.org/wiki/Qix) — Fast/Slow Draw (×2), Qix, Sparx і Super Sparx, Fuse («Spiral Death Trap»), 75 % (50–90), бонус за кожен % понад ціль, два Qix і множник до 9.
- [Wikipedia: Volfied](https://en.wikipedia.org/wiki/Volfied) — 80 %, бос і дрібні вороги, що гинуть всередині, сірі ящики (швидкість/зброя), вбивство боса.
- YouTube: пошук «xonix dos gameplay», «qix arcade gameplay», «volfied arcade gameplay».

## Непевне
- (?) Xonix: ціль 75 %, таймер, кількість життів, +1 мʼяч з кожним рівнем, поведінка при дотику до власного сліду — з памʼяті; uk-Wikipedia цього не каже, пошуковий ліміт вичерпано.
- (?) Qix з двома Qix: чи заливається менша область, коли обидва в різних, — не перевірено (там рівень просто закінчується).
- (?) Volfied: конкретний список підсилень (лазер, щит, зупинка часу тощо) і таймер — Wikipedia називає лише «швидкість або зброю».
- (?) Чи зникає слід після смерті в Xonix і де респавн гравця.
