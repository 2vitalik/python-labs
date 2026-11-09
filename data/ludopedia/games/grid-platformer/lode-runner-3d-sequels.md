---
title: Lode Runner 2 і Lode Runner 3-D
slug: lode-runner-3d-sequels
aka: [Lode Runner 2, Lode Runner 3-D, ロードランナー3-D]
family: grid-platformer
also: []
klass: avatar
axes:
  field: iso
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: collect
year: 1998
platforms: [Windows, Mac OS, Nintendo 64]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lode_Runner_2", best: true, note: "ізометрія, заборона копати під себе й у вузький прохід, бомби з патернами, маскування, перетворення цегли, розтяжки, силові поля, стрибки лише на кутах, редактор"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lode_Runner_3-D", note: "N64: рівні-спіралі вгору, 5 світів × 5 етапів × 4 рівні, карти відкривають світи, золото активує портал"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lode_Runner", note: "місце обох у серії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lode+Runner+2+1998+gameplay", note: "пошук; Lode Runner 2"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lode+Runner+3-D+N64+gameplay", note: "пошук; Lode Runner 3-D"}
stage: v1
coverage: 45
mechanics: [dig-hole, hole-refill, ladder-climb, gravity-fall, collect-all, reach-exit, collect-quota, chase-player, touch-death, explode-area, inventory-items, in-game-editor, level-unlock, world-map, +iso-grid-movement, +dig-restrictions, +blast-patterns, +disguise-item, +block-morph, +tripwire-trap, +invisible-force-field, +corner-only-jump, +spiral-tower-level, +card-unlocks-world]
proposes: ["+cond:width(cell, n)", "+effect:disguise(a, t)", "+role:tripwire", "+axis:field=spiral", "+card:dig-restrictions", "+card:spiral-tower-level"]
author: opus
date: 2026-11-09
---

# Lode Runner 2 і Lode Runner 3-D — дві спроби вивести копання-й-драбини з площини: ізометричні кімнати й спіральні вежі

## Суть
Правила — з [lode-runner](lode-runner.md): бігун копає ями, ченці переслідують, падають у ями, треба зібрати золото й дійти до виходу; інструменти «тримай один пристрій» — з [lode-runner-the-legend-returns](lode-runner-the-legend-returns.md). Тут — лише що змінює **третій вимір**. **Lode Runner 2** (Presage, 1998, PC/Mac) розкладає рівень на ізометричну сітку з кількох поверхів: рух по діагоналях екрана, обмеження на копання, стрибки лише на кутах, невидимі силові поля, нові бомби й предмети. **Lode Runner 3-D** (Big Bang, 1999, N64) лишає гру здебільшого плоскою, але звиває рівень у **спіраль навколо вежі**, по якій треба підійматися.

## Поле і час
- **LR2:** ізометрична сітка клітин-цеглин з поверхами (цегла, драбини, рейки-перекладини, ґрунт); дальня камера, щоб менше скролити — ближча ховала важливі елементи. Напрямки керування — діагоналі екрана, а не «ліво/право».
- **LR2:** силові поля блокують шляхи, що виглядають відкритими; стрибок можливий лише на кутах конструкції.
- **LR 3-D:** гра «здебільшого у двох вимірах», але інколи можна рушити в третьому напрямку; рівні — переважно спіралі, якими лізеш угору (поверхня вежі, як у [nebulus](nebulus.md)).
- Real-time обидві; ченці переслідують.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бігун (Jake Peril) | player | — | ходить, лізе драбинами, висить на рейках, копає; битися з ченцями не може |
| Божевільний чернець | enemy | — | переслідує; падає в ями; дотик — смерть |
| Цегла | terrain | копається | яма тимчасова (як у базі) |
| Драбина, рейка | terrain | — | як у базі, але в ізометрії |
| Ґрунт | terrain | — | опора |
| Бомба (LR2) | pickup | кілька патернів вибуху | руйнує копану цеглу, ченців — або самого бігуна |
| Маскування (LR2) | pickup | тимчасове | ченці не впізнають бігуна (?) |
| Перетворення цегли (LR2) | pickup | — | змінює тип/стан цеглини (?) |
| Розтяжка, тригер (LR2) | switch | — | запускає механізм рівня |
| Силове поле (LR2) | gate | виглядає порожнім | блокує прохід |
| Золото | pickup | — | LR2 — усе; LR 3-D — задана кількість |
| Вихід (LR2) / портал (LR 3-D) | static | — | LR 3-D: активується, коли зібрано квоту золота |
| Карта (LR 3-D) | pickup | 5 на світ | відкриває наступний світ |
| Нові обʼєкти, інструменти, перешкоди (LR 3-D) | — | за світами | без деталей у джерелі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dig, dir)` → ЯКЩО `cell(target, brick)` and `custom: «ціль не прямо під бігуном»` and `custom: «прохід ширший за 1 клітину»` (`+cond:width`) → ТО `set_cell(target, hole)`; інакше `block`.
- КОЛИ `timer(refill)` → ТО `set_cell(hole, brick)` — як у базі; ченця в ямі засипає, бігуна теж.
- КОЛИ `input(jump)` → ЯКЩО `custom: «бігун на куті конструкції»` → ТО `move(runner, jump_target)`; інакше `block` (LR2).
- КОЛИ `contact(runner, force_field)` → ТО `block`.
- КОЛИ `enter(a, tripwire)` → ТО `trigger(mechanism)`.
- КОЛИ `input(use)` → ЯКЩО `has(runner, bomb)` → ТО `explode(pattern, empty)`; зачіпає копану цеглу, ченців і бігуна.
- КОЛИ `input(use)` → ЯКЩО `has(runner, disguise)` → ТО `set_state(runner, disguised, t)`; ЯКЩО `state(runner, disguised)` → ченці `custom: «не переслідують»` (?).
- КОЛИ `input(use)` → ЯКЩО `has(runner, brick_morph)` → ТО `transform(brick)` (?).
- КОЛИ `contact(runner, monk)` → ТО `lose`.
- LR2: КОЛИ `contact(runner, exit)` → ЯКЩО `all_gone(gold)` → ТО `win`.
- LR 3-D: КОЛИ `counter(gold, >=, quota)` → ТО `set_state(portal, active)`; КОЛИ `contact(runner, portal)` → ЯКЩО `state(portal, active)` → ТО `next_level`.
- LR 3-D: КОЛИ `counter(cards, ==, 5)` → ТО `unlock(next_world)`.

## Керування і ввід
- **LR2:** клавіатура; рух по діагоналях ізометрії — огляд Macworld назвав це заплутаним.
- **LR 3-D:** геймпад N64; переважно рух уздовж спіралі, інколи — у третьому напрямку.

## Вікна, меню, HUD
- **LR2:** `game-screen` (ізометричний рівень); `editor-window` — редактор рівнів; `mode-select` — є мультиплеєрні режими (?).
- **LR 3-D:** `world-map` / `level-select` — 5 світів, кожен з 5 етапів по 4 рівні; лічильник золота до порталу (`goal-counter`).

## Фічі поза полем
- LR2: `level-editor`; мультиплеєр (деталі невідомі).
- LR 3-D: `level-unlock` — світ відкривається п'ятьма картами з попереднього; 5 × 5 × 4 = 100 рівнів (підрахунок з джерела).

## Варіації й родичі
- У корпусі: [lode-runner](lode-runner.md) (база), [lode-runner-the-legend-returns](lode-runner-the-legend-returns.md) (предмети, ченці; LR2 — його сиквел), [lode-runner-sequels](lode-runner-sequels.md) (Championship, Legacy — воксельна подача того самого 2D), [nebulus](nebulus.md) (вежа-спіраль), [knight-lore](knight-lore.md), [head-over-heels](head-over-heels.md) (ізометричні кімнати).
- **Осі варіацій «Lode Runner у 3D»:** подача (плоска сітка / ізометрія з поверхами / спіраль на вежі / воксельна 2D); що 3D ламає (напрямки керування, видимість — силові поля, стрибки лише на кутах); мета рівня (усе золото + вихід / квота + портал).

## Цікавинки для курсу
- Обмеження на копання (не під себе, не в прохід шириною 1) — 🌱.
- Бомби з кількома патернами вибуху, що шкодять і собі — 📎.
- Ізометрична сітка з поверхами: координати → екран і діагональне керування — 🥉.
- Рівень на спіралі навколо вежі (циліндрична сітка) — 🥈.
- Квота золота активує портал + карти відкривають світи — 🌱.

## Мапа на каталог
- Є: `dig-hole` · `hole-refill` · `ladder-climb` · `gravity-fall` · `collect-all` (LR2) · `collect-quota` (LR 3-D) · `reach-exit` · `chase-player` · `touch-death` · `explode-area` · `inventory-items` · `in-game-editor` · `level-unlock` · `world-map`.
- **Нема** → пропозиції карток:
  - `+iso-grid-movement` «Рух по ізометричній сітці з поверхами» · interface/render · 🥉.
  - `+dig-restrictions` «Де копати не можна» · entities/legality · 🌱.
  - `+blast-patterns` «Бомби з різною формою вибуху» · entities/combat · 📎 (дитина `explode-area`).
  - `+disguise-item` «Маскування: вороги не переслідують» · entities/state · 📎.
  - `+block-morph` «Предмет змінює тип блока» · entities/interact · 🌱.
  - `+tripwire-trap` «Розтяжка запускає механізм» · entities/interact · 🌱.
  - `+invisible-force-field` «Невидима стіна» · entities/legality · 🌱.
  - `+corner-only-jump` «Стрибок лише з певних клітин» · entities/move · 🌱.
  - `+spiral-tower-level` «Рівень-спіраль навколо вежі» · levels/format · 🥈.
  - `+card-unlocks-world` «N колекційних предметів відкривають світ» · levels/progression · 🌱.

## Пропозиції до словників
- `+cond:width(cell, n)` — ширина проходу в клітинах (LR2: копати не можна в прохід шириною 1).
- `+effect:disguise(a, t)` — вороги тимчасово ігнорують сутність (можна як `set_state(a, disguised)`).
- `+role:tripwire` — сенсор на клітині, що запускає механізм (близько до ⏳ `switch`, але без ручного вмикання).
- `+axis:field=spiral` — поле на бічній поверхні вежі (циліндр); Nebulus, LR 3-D.
- `+card:dig-restrictions`, `+card:spiral-tower-level` — див. вище.

## Джерела
- ⭐ [Wikipedia: Lode Runner 2](https://en.wikipedia.org/wiki/Lode_Runner_2) — ізометрія, правила копання, бомби з патернами, маскування, перетворення цегли, розтяжки й тригери, силові поля, стрибки на кутах, мультиплеєр і редактор, дальня камера; Macworld про діагональне керування.
- [Wikipedia: Lode Runner 3-D](https://en.wikipedia.org/wiki/Lode_Runner_3-D) — спіралі, світи/етапи/рівні, 5 карт для світу, квота золота і портал.
- [Wikipedia: Lode Runner](https://en.wikipedia.org/wiki/Lode_Runner) — місце в серії.
- YouTube: пошуки «Lode Runner 2 1998 gameplay», «Lode Runner 3-D N64 gameplay».

## Непевне
- (?) Що саме роблять маскування й «перетворення цегли» в LR2 — Wikipedia лише називає їх.
- (?) Кількість рівнів LR2, типи мультиплеєра, деталі редактора.
- (?) LR 3-D: які нові обʼєкти й інструменти в пізніх світах; чи є бомби; як працює камера.
- (?) `field: iso` — за LR2; LR 3-D радше поверхня вежі (`3d`/«spiral»).
- (?) Чи ченці в LR2 мають нову поведінку в ізометрії (джерело каже лише «переслідують»).
