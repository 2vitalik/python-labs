---
title: Log!cal
slug: logical
aka: [Logical, Cogency]
family: connect-rotate
also: [falling-match]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 1991
platforms: [C64, Atari ST, Amiga, DOS]
links:
  - {kind: wiki, url: "https://www.c64-wiki.com/wiki/Log!cal", best: true, note: "C64-Wiki: усі спецелементи, таймери, рахунок, керування, паролі"}
  - {kind: other, url: "https://everygamegoing.com/larticle/logical-000/49003", note: "огляд ST Format: колеса, ліміт кульок, пароль редактора"}
  - {kind: other, url: "https://www.atarimagazines.com/compute/issue147/142_Logical.php", note: "COMPUTE! #147 (1992): PC-версія, опції, YOU FAILED"}
  - {kind: play, url: "https://novomundus.itch.io/cogency", note: "Cogency — HTML5-ремейк, 10 рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Logical+Rainbow+Arts+Amiga+gameplay", note: "пошук; геймплей Amiga"}
stage: v1
coverage: 60
mechanics: [tile-rotate, cell-click, one-way-cell, teleport-pair, next-queue, time-out, time-bonus, event-points, score-records, leaderboard, level-password, sequential-levels, in-game-editor, game-pause, keyboard-controls, game-screen, end-screen, +shoot-from-wheel, +wheel-four-match, +recolor-station, +color-filter, +transit-limit, +ordered-fill-lights, +recipe-fill, +per-object-timer, +all-once-goal]
proposes: ["+role:wheel", "+cond:recipe_match", "+ui:transit-counter", "+ui:order-lights", "+ui:roll-timer-bar", "+card:wheel-four-match", "+card:transit-limit", "+card:ordered-fill-lights"]
author: opus
date: 2026-11-09
---

# Log!cal — крути колеса з чотирма гніздами й відстрілюй кульки трубами, щоб у кожному колесі зібралось чотири однакові й воно вибухнуло

## Суть
Поле — решітка коліс, зʼєднаних тунелями; кульки чотирьох кольорів вкочуються згори й лягають у вільні гнізда коліс. Гравець повертає колесо на 90° і вистрілює кульку з гнізда в потрібний тунель — так кульки «пересилаються» між колесами. Колесо, у якому зібрались чотири кульки одного кольору, вибухає й звільняється; рівень пройдено, коли кожне колесо вибухнуло хоча б раз. Ядро — real-time логістика: черга кольорів іде безперервно, у русі одночасно не більше чотирьох кульок, а кольорофільтри, перефарбовувачі, стрілки й світлофор перетворюють сортування на пазл.

## Поле і час
- Квадратна решітка: колеса стоять на перетинах тунелів (горизонтальних і вертикальних); угорі — подавальний тунель, звідки приходять нові кульки. Розмір решітки — (?)
- Колесо — 4 гнізда за сторонами світу; гніздо, що дивиться в тунель, може прийняти або випустити кульку.
- Real-time: кульки котяться тунелями; окремий таймер-смужка на кульку в подавальному тунелі й пісочний годинник рівня (є не на всіх рівнях).
- 99 рівнів з повільно, але неухильно зростаючою складністю; нові елементи додаються з рівнями.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Колесо (receptacle) | container | 4 гнізда, орієнтація, стан «вибухнуло» | повертається на 90°; 4 однакові кульки → вибух, гнізда порожні, колесо знову придатне |
| Кулька | object | колір: red, yellow, green, blue | котиться тунелем; лягає в гніздо, що дивиться на неї |
| Тунель (channel) | conduit | — | веде кульку між колесами |
| Подавальний тунель | source | таймер на кульку | угорі поля; звідси кульки входять у гру |
| Перефарбовувач ×4 | terrain | колір | кулька, що проходить під ним, стає його кольору |
| Кольорофільтр ×4 (colour stopper) | gate | колір | пропускає лише кульки свого кольору |
| Стрілка напрямку | terrain | напрям | повертає кульку за стрілкою; з протилежного боку — відштовхує (одностороння) |
| Телепорт | terrain | ≤1 горизонтальна + ≤1 вертикальна пара на рівень | переносить кульку на парний телепорт |
| Світлофор (lights) | mark | черга кольорів згори вниз | задає порядок кольорів, якими треба наповнювати колеса |
| Прогноз кольору | mark | 1 кулька | показує колір наступної кульки |
| Гандикап кольорів | mark | набір комбінацій | колесо можна наповнити показаною мішаною комбінацією; з часом комбінації зникають (пізні рівні) |
| Пісочний годинник | mark | час рівня | вбудований у поле; закінчився — провал |
| Табло кульок у русі | mark | ≤4 | показує, скільки кульок котиться |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(rotate, wheel)` → ТО `rotate(wheel, 90)` (C64: проти годинникової).
- КОЛИ `input(shoot, wheel, dir)` → ЯКЩО `occupied(hole[dir], marble) and counter(in_transit, <, 4)` → ТО `move(marble, dir)`, `counter(in_transit, +1)`; інакше `block`.
- КОЛИ `custom: «кулька в подавальному тунелі над гніздом, що дивиться вгору»` → ЯКЩО `free(hole)` → ТО `custom: «кулька лягає в гніздо»`, `counter(in_transit, -1)`.
- КОЛИ `timer(roll_time)` → ЯКЩО `custom: «кулька ще в подавальному тунелі»` → ТО `custom: «провал (?)»`.
- КОЛИ `custom: «кулька докотилась тунелем до колеса»` → ЯКЩО `free(hole_facing)` → ТО `custom: «лягає в гніздо»`; інакше `bounce(marble)` (?).
- КОЛИ `counter(wheel.marbles, ==, 4)` → ЯКЩО `same(marbles, color)` → ТО `explode(wheel)`, `set_state(wheel, exploded)`, `custom: «гнізда порожні, колесо працює далі»`.
- КОЛИ `counter(wheel.marbles, ==, 4)` → ЯКЩО `custom: «склад колеса = комбінація з елемента гандикапу»` → ТО `explode(wheel)`, `set_state(wheel, exploded)`, `score(+500)`.
- КОЛИ `counter(wheel.marbles, ==, 4)` → ЯКЩО `custom: «на рівні є світлофор»` → ТО `custom: «вибух зараховується лише кольору з верху світлофора; світлофор зсувається на наступний»` (?).
- КОЛИ `enter(marble, changer[c])` → ТО `set_value(marble, c)`.
- КОЛИ `enter(marble, stopper[c])` → ЯКЩО `not same(marble, stopper, color)` → ТО `block`.
- КОЛИ `enter(marble, arrow)` → ЯКЩО `moving(marble, opposite_of_arrow)` → ТО `bounce(marble)`; інакше `face(marble, arrow_dir)`.
- КОЛИ `enter(marble, teleport)` → ТО `teleport(marble, pair)`.
- КОЛИ `custom: «кулька вийшла з подавального тунелю»` → ТО `spawn_at(marble[forecast], feed_entry)`, `custom: «прогноз показує новий випадковий колір»` (?).
- КОЛИ `counter(wheels_not_exploded, ==, 0)` → ТО `score(+time_bonus)`, `score(+1000 - 100 × in_transit)`, `message(password)`, `next_level`.
- КОЛИ `counter(hourglass, ==, 0)` → ТО `lose`, `window(end-screen)` («YOU FAILED»).
- Перемога рівня: кожне колесо вибухнуло хоч раз. Поразка: пісочний годинник вичерпано (і, можливо, таймер кульки) (?). Рахунок: бонус за час, 1000 базових за рівень −100 за кожну кульку в русі (не нижче нуля), +500 за мішаний вибух; топ-10 рекордів зберігається на диск.

## Керування і ввід
- C64: джойстик водить курсор; fire — повернути колесо під курсором на 90° ліворуч; fire + напрям — вистрілити кульку з гнізда в той бік. Клавіша ← — кінець гри, Space — пауза.
- Amiga/ST/PC: миша — правий клік повертає колесо, лівий — виштовхує кульку (огляд ST Format); COMPUTE! радить мишу, без неї пізні рівні «майже неможливі»; джойстик — за бажанням.
- Ремейк Cogency: клік — повернути, свайп — «виштрикнути» кульку.

## Вікна, меню, HUD
- `splash-screen` — титул (C64-Wiki показує лише зображення).
- `game-screen`: решітка коліс, подавальний тунель угорі з `roll-timer-bar` (смужка часу кульки), пісочний годинник у полі (`timer-countdown`), табло кульок у русі (`transit-counter`), `next-piece-preview` (прогноз кольору), світлофор (`order-lights`), `score`.
- `level-password` — 5-літерний пароль рівня (C64: «zdhgz» для 05 тощо); після кожного пройденого рівня гра показує пароль наступного.
- `end-screen` — «YOU FAILED» з дражливою мелодією; підсумок рівня з бонусами (?).
- `leaderboard` — топ-10 рекордів.
- `editor-window` — редактор рівнів (ST/Amiga/PC; пароль після всіх 99 рівнів).
- `settings-window` (PC): 4 «мармурові» фони, монохромний режим, звук (PC-speaker / Ad Lib).

## Фічі поза полем
- `levels-sequential` 99 рівнів + `level-password` замість збереження.
- `level-editor` — прихований: пароль видається за проходження всіх 99 (ST/Amiga/PC); у C64 нема з технічних причин.
- `leaderboard-local` топ-10 на диску; `pause`; `theme-select` (фони, PC).
- Захист від копіювання C64 — питання з останньої сторінки мануалу.

## Варіації й родичі
- Версії: C64 (T. Brockhage), Atari ST, Amiga, PC (SoftGold) — однакові правила, редактор лише на 16-бітних.
- Ремейк: Cogency (NovoMundus, HTML5/Unity, 10 рівнів).
- Корпус: [Pipe Mania](pipe-mania.md) (рух по трубах на час) · [Marble Drop](marble-drop.md) (кульки, фарбувальники, маршрути) · [Spin Doctor](spin-doctor.md) і [Cogs](cogs.md) (обертання як основний хід) · [Zoo Keeper](../falling-match/zoo-keeper.md) і match-3 загалом (збір однакових — зникнення).
- Осі варіацій: **збір однакових** — у лінію на полі (match-3) / у контейнер на 4 (Log!cal) · **ввід** — повернути контейнер / вистрілити з нього · **маршрут** — тунелі фіксовані, змінюється лише орієнтація коліс · **ліміт** — кульок у русі / часу кульки / часу рівня.

## Цікавинки для курсу
- Колесо на 4 гнізда з поворотом і пострілом у тунель: орієнтація + порти + черга кульок — 🥉.
- Вибух за «4 однакові» і за рецептом-гандикапом (мішана комбінація) — 📎.
- Світлофор: глобальний порядок кольорів для вибухів — 🌱 (черга як обмеження).
- Ліміт «≤4 кульки в русі» + таймер кульки в подавальному тунелі: два різні тиски часу — 📎.
- Перефарбовувачі, кольорофільтри, односторонні стрілки, пари телепортів — набір «модифікаторів тунелю» — 📎 за набір.
- Пароль за рівень + прихований пароль редактора після фіналу — 🌱.

## Мапа на каталог
- Є: `tile-rotate` (колесо на 90°) · `cell-click` · `one-way-cell` (стрілки) · `teleport-pair` · `next-queue` (прогноз кольору) · `time-out` (пісочний годинник) · `time-bonus` · `event-points` · `score-records` + `leaderboard` · `level-password` · `sequential-levels` · `in-game-editor` · `game-pause` · `keyboard-controls` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+shoot-from-wheel` «Вистрілити обʼєкт з контейнера в напрямку» · interface/input · 📎.
  - `+wheel-four-match` «Контейнер на N гнізд: N однакових — вибух» · entities/interact · 📎 · слот {n: 4}.
  - `+recolor-station` «Клітина-фарбувальник» · entities/state · 🌱 (як у Marble Drop).
  - `+color-filter` «Фільтр пропускає лише свій колір» · entities/legality · 🌱.
  - `+transit-limit` «Не більше N рухомих обʼєктів одночасно» · game-logic · 🌱 · слот {n: 4}.
  - `+ordered-fill-lights` «Порядок кольорів для виконання цілей» · game-logic/win · 📎.
  - `+recipe-fill` «Наповнення за рецептом-комбінацією» · game-logic/win · 📎.
  - `+per-object-timer` «Таймер на окремий обʼєкт» · game-logic/lose · 🌱.
  - `+all-once-goal` «Кожен обʼєкт виду має спрацювати хоч раз» · game-logic/win · 🌱.

## Пропозиції до словників
- `+role:wheel` — контейнер з фіксованими гніздами-портами, що обертається (Log!cal, Cogency); від `container` відрізняється орієнтацією і портами.
- `+cond:recipe_match(container, recipe)` — вміст контейнера збігається з показаною комбінацією (гандикап кольорів).
- `+ui:transit-counter` — скільки обʼєктів зараз у русі з лімітом; `+ui:order-lights` — вертикальна черга кольорів-цілей; `+ui:roll-timer-bar` — смужка часу окремого обʼєкта.
- `+card:wheel-four-match`, `+card:transit-limit`, `+card:ordered-fill-lights` — див. «Мапа на каталог».

## Джерела
- ⭐ [C64-Wiki: Log!cal](https://www.c64-wiki.com/wiki/Log!cal) — колеса, 4 кольори, перефарбовувачі, фільтри, стрілки, телепорти, світлофор, прогноз, гандикап, таймери, рахунок, паролі, версії з редактором.
- [ST Format / everygamegoing](https://everygamegoing.com/larticle/logical-000/49003) — керування мишею, «зазвичай чотири» кульки в русі, пароль на кожен рівень і пароль редактора після 99.
- [COMPUTE! #147](https://www.atarimagazines.com/compute/issue147/142_Logical.php) — PC-версія: пісочний годинник, YOU FAILED, 4 фони, Ad Lib, SoftGold.
- [Cogency на itch.io](https://novomundus.itch.io/cogency) — браузерний ремейк.
- YouTube: пошук «Logical Rainbow Arts Amiga gameplay».

## Непевне
- (?) Що стається, коли вичерпано таймер кульки в подавальному тунелі (провал рівня, втрата життя чи лише штраф), — джерела не кажуть; чи є життя взагалі — теж.
- (?) Кулька, що докотилась до колеса з зайнятим гніздом: відскакує назад чи застрягає — не перевірено.
- (?) Світлофор: чи вибух «не того» кольору блокується, чи просто не зараховується.
- (?) Колір нової кульки випадковий чи заданий рівнем — прогноз показує лише наступну.
- (?) Розмір решітки коліс і кількість коліс на рівні — у джерелах чисел нема.
- (?) Розробник: C64-Wiki — T. Brockhage; Amiga-версію приписують Volker Eloesser (результат пошуку), PC — SoftGold GmbH (COMPUTE!).
