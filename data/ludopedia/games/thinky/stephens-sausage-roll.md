---
title: Stephen's Sausage Roll
slug: stephens-sausage-roll
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: layers
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2016
platforms: [PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Stephen%27s_Sausage_Roll", best: true, note: "правила: ковбаски 1×2, гриль на кожну сторону, підгоряння, вода, виделка як окрема клітина, без стрейфу, розділи"}
  - {kind: steam, url: "https://store.steampowered.com/app/353540/Stephens_Sausage_Roll/", note: "«A simple 3d puzzle game», increpare games"}
  - {kind: other, url: "https://www.wurb.com/stack/?p=3136", note: "рецензія з правилами: перекочування вбік, гриль непрохідний, підгоряння, повернутись на старт"}
  - {kind: other, url: "https://setsideb.com/tag/stephenssausageroll/", note: "граф станів двох ранніх рівнів; Z — undo, R — restart"}
  - {kind: other, url: "https://dspace.mit.edu/handle/1721.1/156825", note: "MIT-теза «Further Hardness Results for Stephen's Sausage Roll» (2024): складність варіантів механік, драбини"}
  - {kind: other, url: "https://thinkygames.com/games/stephens-sausage-roll/", note: "Thinky Games — картка гри"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=stephen%27s+sausage+roll+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-by-input, keyboard-controls, push-object, multi-cell-size, orientation-state, impassable-cells, environment-death, sequential-levels, level-unlock, movement-animation, save-progress, +undo-redo, +tank-controls, +rotating-tool-sweep, +face-cooking, +height-levels, +skewer-carry, +return-to-start, +world-map]
proposes: ["+trigger:input", "+trigger:sweep", "+cond:face_state", "+cond:supported", "+effect:roll", "+effect:rotate", "+effect:fall", "+effect:set_state", "+effect:move", "+role:hazard", "+role:terrain", "+window:map-window", "+feature:undo", "+feature:world-map", "+axis:undo"]
author: opus
date: 2026-11-02
---

# Stephen's Sausage Roll — засмаж кожен бік ковбасок виделкою, не підпаливши й не втопивши

## Суть
Стівен із виделкою, що завжди стирчить перед ним, штовхає ковбаски 1×2 на грилі на маленьких островах. Ковбаска має 2 половинки × 2 боки = 4 «плями», і **кожна має бути засмажена рівно один раз**: удруге — підгоріла, рівень провалено. Штовхання вбік перекочує ковбаску (верх↔низ), уздовж — лише зсуває, тож порядок поштовхів визначає, який бік торкнеться гриля. Після того як усе засмажено, Стівен має повернутися на стартову клітину. Гра відома мінімалізмом і жорсткою складністю: нових механік мало, кожен рівень вичавлює з них максимум.

## Поле і час
- 3D-сітка з висотами (рівні землі, сходинки, драбини), камера ізометрична/зверху; кожен рівень — острів у воді. Для опису — квадратна сітка + висота клітини (`layers`).
- Покроково: хід = крок уперед/назад або поворот на 90°.
- Обʼєкти можуть лежати на обʼєктах (ковбаска на ковбасці); Стівен у пізніх рівнях ходить по ковбасках.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Стівен | player | напрям погляду | крок уперед/назад без зміни напрямку; поворот на місці на 90°; без стрейфу |
| Виделка | object | клітина перед Стівеном | займає власну клітину; штовхає те, у що впирається; при повороті замітає дугу |
| Ковбаска | object | 1×2, 2 половинки × {верх, низ}, стан кожної: сира/засмажена/підгоріла | штовхається; вбік — перекочується (верх↔низ), уздовж — ковзає; падає, якщо нема опори |
| Гриль | hazard | — | непрохідний для Стівена; засмажує нижній бік половинки ковбаски, що на нього лягла |
| Земля | terrain | висота | опора; уступи блокують рух на іншу висоту |
| Вода | hazard | — | ковбаска без опори падає у воду → провал; Стівен у воді → провал |
| Драбина | terrain | — | дозволяє Стівенові піднятися/спуститися на рівень висоти (?) |
| Стартова клітина | static | — | після засмаження всього треба повернутися сюди |
| Рожеві стіни рівня | static | — | обгороджують рівень на мапі; зникають, коли рівень розвʼязано (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(forward|back)` → ЯКЩО `free(target)` для Стівена і виделки (з урахуванням поштовху) → ТО `move(stephen, dir)`, `move(fork, dir)`.
- КОЛИ `input(turn_left|turn_right)` → ТО `rotate(stephen, ±90)`; виделка `custom: «замітає діагональну клітину між старою і новою позицією, штовхаючи те, що там лежить»` (?); якщо замітання заблоковане — поворот не відбувається.
- КОЛИ `contact(fork|stephen, sausage)` → ЯКЩО весь ланцюг ковбасок може зсунутись → ТО `push`; інакше `block`.
- КОЛИ ковбаску штовхнуто перпендикулярно довгій осі → ТО `roll(sausage)`: нижні боки ↔ верхні.
- КОЛИ ковбаску штовхнуто вздовж довгої осі → ТО `move(sausage, dir)` без перекочування.
- КОЛИ `enter(half, grill)` → ЯКЩО `face_state(half.bottom, raw)` → ТО `set_state(half.bottom, cooked)`; ЯКЩО `face_state(half.bottom, cooked)` → ТО `set_state(burnt)`, `lose`.
- КОЛИ ковбаска лежить на грилі без руху → ТО нічого (повторно не смажить).
- КОЛИ `contact(stephen, grill)` → ТО `block`.
- КОЛИ `after(move)` → ЯКЩО `not supported(sausage)` → ТО `fall(sausage)`; у воду → `lose`.
- КОЛИ `enter(stephen, water)` → ТО `lose`.
- КОЛИ `contact(fork, sausage)` → ЯКЩО `custom: «поштовх неможливий і виделка входить у торець/бік»` → ТО `attach(fork, sausage)` — ковбаска наколота й рухається з виделкою (пізні розділи) (?).
- КОЛИ `custom: «усі 4 боки всіх ковбасок cooked»` і `contact(stephen, start_tile)` → ТО `win`.
- Поразка: підгоріла пляма або ковбаска/Стівен у воді — рівень заморожується до undo/restart. Рахунку нема.

## Керування і ввід
- Стрілки/WASD: уперед/назад — крок, ліво/право — поворот на 90° («танкове» керування).
- Z — undo на один хід (без ліміту), R — рестарт рівня.
- Пізні механіки (стати на ковбаску, наколоти, відʼєднатися від виделки) — тими самими клавішами в певних ситуаціях, без нових кнопок (?).

## Вікна, меню, HUD
- `main-menu` — мінімальне: продовжити, налаштування, вихід (?).
- `map-window` — сам світ: острови-рівні, зʼєднані стежками, Стівен ходить ними; кам'яні таблички з текстом сюжету; розділ відкривається після всіх рівнів попереднього.
- `game-screen` — рівень у 3D без HUD: ні лічильників, ні підказок (лише табличка з керуванням на старті).
- `pause-menu` — продовжити, налаштування, вихід (?).
- `settings-window` — гучність, графіка, керування (?).
- Переходи: світ → (вхід на острів) рівень → (розвʼязано, стіни зникають) світ.

## Фічі поза полем
- `undo` ∞ (по одному ходу) + `restart-level`; `autosave`.
- `world-map` як ходильний світ (не меню) + `level-unlock` розділами.
- Підказок, редактора, рахунку нема; навчання — лише через дизайн рівнів і табличку з керуванням.

## Варіації й родичі
- Автор — Stephen Lavelle (increpare), PuzzleScript; родичі: Sokoban, DROD (замітання мечем при повороті), A Monster's Expedition (колоди 1×2 перекочуються), Bloxorz (брусок, що перекочується), English Country Tune.
- **Осі варіацій:** обʼєкт — 1×1 / 1×2 / брусок 1×1×2; орієнтація — немає / вісь / 4 грані з власним станом; інструмент — немає / виделка спереду / меч, що обертається; мета — покласти на ціль / «обробити» кожну грань рівно раз.

## Цікавинки для курсу
- Обʼєкт 1×2 з 4 гранями й станом кожної, перекочування vs ковзання — 🥇 (`orientation-state` + `multi-cell-size` одночасно).
- «Рівно один раз» як умова: смажити кожну грань один раз, повтор = провал — 🥉.
- Танкове керування + інструмент у сусідній клітині, що замітає дугу при повороті — 🥈.
- Висоти й опора (падіння з уступу, ковбаска на ковбасці) — 🥈.
- Повернення на старт як друга фаза перемоги — 🌱.
- Розвʼязувач/оцінка складності (є MIT-роботи про обчислювальну складність варіантів механік) — 👑 для дослідницьких студентів.

## Мапа на каталог
- Є: `move-by-input` + `keyboard-controls` ↔ крок/поворот; `push-object` ↔ поштовх ковбасок; `multi-cell-size` ↔ 1×2; `orientation-state` ↔ «Обʼєкт перекочується, боки різні (Sausage Roll)» — картка прямо названа на честь гри; `impassable-cells` ↔ гриль для Стівена, уступи; `environment-death` ↔ вода; `sequential-levels` + `level-unlock` + `save-progress` ↔ розділи світу; `movement-animation` ↔ перекочування.
- **Нема** → пропозиції карток:
  - `+undo-redo` «Undo ходів у грі» · game-logic/flow · 📎.
  - `+tank-controls` «Уперед/назад + поворот» · interface/input · 📎.
  - `+rotating-tool-sweep` «Інструмент у сусідній клітині замітає дугу при повороті» · entities/interact · 🥈 — і DROD.
  - `+face-cooking` «Кожна грань обробляється рівно раз» · game-logic/win · 🥉 · слот {faces: 2|4}.
  - `+height-levels` «Висоти клітин, уступи, драбини» · entities/legality · 🥈.
  - `+skewer-carry` «Наколоти обʼєкт і нести» · entities/interact · 🥉 — споріднено з `stick-together`.
  - `+return-to-start` «Після мети повернутися на старт» · game-logic/win · 🌱.
  - `+world-map` «Ходильний світ-хаб» · levels/progression · 🥉.

## Пропозиції до словників
- `+trigger:input`; `+trigger:sweep(fork, cell)` — поворот інструмента зачіпає діагональну клітину.
- `+cond:face_state(obj.face, s)` — стан конкретної грані обʼєкта (сира/засмажена/підгоріла).
- `+cond:supported(x)` — є опора під обʼєктом (і в Snakebird).
- `+effect:roll(a, dir)` — перекотити обʼєкт: міняє грані верх/низ, на відміну від `move`.
- `+effect:rotate`, `+effect:fall`, `+effect:set_state`, `+effect:move` — кандидати, тут основні.
- `+role:hazard` (гриль, вода), `+role:terrain` (драбина, уступ).
- `+window:map-window` — світ як ходильний хаб; `+feature:undo`, `+feature:world-map`.
- `+axis:undo` — `unlimited`, по одному ходу.

## Джерела
- ⭐ [Wikipedia: Stephen's Sausage Roll](https://en.wikipedia.org/wiki/Stephen%27s_Sausage_Roll) — правила смаження, провали, undo/restart, виделка як окрема клітина, відсутність стрейфу, розділи й нові механіки.
- [Steam](https://store.steampowered.com/app/353540/Stephens_Sausage_Roll/) — сторінка, нагороди.
- [The Stack (wurb.com)](https://www.wurb.com/stack/?p=3136) — перекочування вбік, гриль непрохідний, лежати на грилі безпечно, повернення на старт.
- [Set Side B](https://setsideb.com/tag/stephenssausageroll/) — граф станів ранніх рівнів, клавіші Z/R.
- [MIT DSpace: Further Hardness Results for SSR](https://dspace.mit.edu/handle/1721.1/156825) — складність, драбини.
- [Thinky Games](https://thinkygames.com/games/stephens-sausage-roll/).
- YouTube: [пошук «stephen's sausage roll gameplay»](https://www.youtube.com/results?search_query=stephen%27s+sausage+roll+gameplay).

## Непевне
- (?) Точна механіка повороту (яку діагональну клітину замітає виделка і куди штовхає) — з памʼяті.
- (?) Драбини, ходіння по ковбасках, наколювання, відʼєднання від виделки — Wikipedia згадує як пізні механіки без деталей.
- (?) Чи «повернутися на старт» означає ще й той самий напрям погляду.
- (?) Чи падає ковбаска, оперта лише однією половинкою.
- (?) Меню і налаштування — з памʼяті; кількість рівнів не знайдено.
