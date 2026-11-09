---
title: "King's Valley II: The Seal of El Giza"
slug: kings-valley-2
aka: [King's Valley II, "王家の谷 エルギーザの封印", Ouke no Tani El Giza no Fuuin, KV2]
family: grid-platformer
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1988
platforms: [MSX, MSX2 (лише Японія)]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/王家の谷_エルギーザの封印", best: true, note: "JA: контекстна кнопка, 6 предметів з формою копання, 4 вороги, зникомі драбини й підлога, рухомі камені, двері, тор-екран, життя, паролі"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/King%27s_Valley_II", note: "EN: 6 пірамід × 10, камені душі, редактор із записом на диск/касету, конкурс рівнів"}
  - {kind: other, url: "https://generation-msx.nl/software/konami/kings-valley-ii-the-seal-of-el-giza/cheats/1079", note: "паролі (формат XXKONAMI), секретні кімнати: стрибок у точці → піраміда → двері"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=King%27s+Valley+II+MSX+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-by-input, ladder-climb, gravity-fall, collect-all, reach-exit, touch-death, environment-death, player-death, chase-player, enemy-patrol, speed-per-type, spawner-entity, spawn-animation, dig-terrain, destructible-blocks, impassable-cells, cell-transform, timed-despawn, one-way-cell, push-object, projectile-shot, temporary-modes, inventory-items, inventory-limit, wrap-edges, player-camera, extra-life-threshold, sequential-levels, level-password, cheat-codes, in-game-editor, editor-palette, level-exchange, attract-demo, +jump-fixed-height, +single-use-tool, +dig-shape-per-tool, +boomerang-return, +enemy-as-platform, +vanish-after-n-uses, +growing-wall, +secret-door-by-jump]
proposes: ["+effect:dig", "+effect:jump(height)", "+effect:return_to(a, owner)", "+cond:uses(a, op, n)", "+trigger:used(a)", "+feature:level-save-tape", "+feature:edit-contest", "+card:dig-shape-per-tool", "+card:vanish-after-n-uses"]
author: opus
date: 2026-11-09
---

# King's Valley II — шість інструментів копання різної форми, бумеранг і зникомі драбини: збери камені душі й не загубись у торі-екрані

## Суть
Нащадок Бік XIII у шести пірамідах збирає камені душі й виходить крізь двері. Ядро першої частини (одна річ у руках, без предмета — стрибок) розросло: **чотири одноразові інструменти копають різні форми** (стіну 2×1, підлогу 1×2, стіну 2×2, підлогу 2×2), **дві багаторазові зброї** (ніж і бумеранг) і чотири вороги з різною поведінкою, один з яких після зупинки стає платформою. Поле — від 1 до 6 екранів, замкнене по горизонталі. Вбудований редактор пише рівні на диск або касету — Konami навіть проводила конкурс рівнів.

## Поле і час
- Блокова сітка: ламкі й неламкі блоки, драбини (тепер вертикальні, не діагональні сходи), порожнеча; клітинна гравітація.
- Стадія — 1–6 екранів зі скролом; краї замкнені: вийшов праворуч — зайшов зліва (тор по горизонталі).
- Real-time; вороги мають власну швидкість, на драбинах — свою.
- 6 пірамід × 10 кімнат = 60 стадій; після кожної 10-ї — демо переходу до наступної піраміди.
- Усе видно; у деяких стадіях — секретні кімнати, вхід у які проявляється стрибком у певній точці.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бік XIII | player | несе ≤ 1 предмет/зброю | біг, драбини, стрибок (з порожніми руками), падіння |
| Ламкий блок | terrain | — | опора; копається інструментами |
| Неламкий блок | static | — | не копається |
| Драбина | terrain | — | вертикальний рух |
| Зникома драбина | terrain | жовта, 2 проходи | після двох підйомів верх стає підлогою, потім драбина зникає |
| Зникома підлога | terrain | ряд кружечків, 2 проходи | зникає після двох переходів |
| Ростуча стіна | hazard | тригер-точки | росте зі стелі; копається; розчавлення — миттєва смерть |
| Рухомий камінь | object | блакитний | штовхається; служить платформою |
| Обертові двері | gate | біла сторона | прохід лише з білого боку |
| Одностороння двері | gate | плаский бік | прохід лише з плаского боку |
| Камінь душі | pickup | — | треба зібрати всі; відчиняє вихід |
| Вихідні двері | gate | — | вихід після збору всіх каменів |
| Ніж | pickup | зброя, багаторазова | летить прямо; у польоті не зловити; лежить, де впав |
| Бумеранг | pickup | зброя, багаторазова | без влучання повертається; можна зловити в польоті |
| Молот | pickup | одноразовий | копає стіну 2 вгору × 1 вшир |
| Лопата | pickup | одноразова | копає підлогу 1 вглиб × 2 вшир |
| Дриль | pickup | одноразовий | копає стіну 2×2 |
| Кирка | pickup | одноразова | копає підлогу 2×2 |
| Саркофаг | spawner | — | з нього виходять Slow Man і Fast Man |
| Slow Man | enemy | біла мумія | ходить по підлозі вліво-вправо; драбинами не користується |
| Fast Man | enemy | жовта мумія | швидко лазить драбинами |
| Пйонші (Pyonshi) | enemy | зʼявляється з диму | переслідує стрибками; у стрибку проходить крізь підлогу; драбинами — повільно |
| Rock Roll | enemy | зʼявляється з диму | роззирається, згортається в кулю й котиться підлогою; зупинений — нешкідливий і стає платформою |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(bick, dir)`.
- КОЛИ `input(up|down)` → ЯКЩО `cell(here, ladder)` → ТО `move(bick, dir)`.
- КОЛИ `tick` → ЯКЩО `not supported(a)` → ТО `fall(a)`.
- КОЛИ `edge(a)` → ТО `wrap(a)` — горизонтальний тор стадії.
- КОЛИ `input(space)` → ЯКЩО `not has(bick, item)` → ТО `custom: «стрибок»`.
- КОЛИ `input(space)` → ЯКЩО `has(bick, weapon)` → ТО `throw(weapon, facing)`.
- КОЛИ `input(space)` → ЯКЩО `has(bick, hammer)` і `cell(ahead, breakable)` → ТО `set_cell(wall 2×1, empty)`, `take(bick, hammer)`.
- КОЛИ `input(space)` → ЯКЩО `has(bick, shovel)` і `cell(below, breakable)` → ТО `set_cell(floor 1×2, empty)`, `take(bick, shovel)`.
- КОЛИ `input(space)` → ЯКЩО `has(bick, drill)` → ТО `set_cell(wall 2×2, empty)`, `take(bick, drill)`.
- КОЛИ `input(space)` → ЯКЩО `has(bick, pickaxe)` → ТО `set_cell(floor 2×2, empty)`, `take(bick, pickaxe)`.
- КОЛИ `contact(bick, item)` → ЯКЩО `not has(bick, item)` → ТО `pickup` — один предмет або одна зброя.
- КОЛИ `contact(weapon, enemy)` → ТО `disappear_b`, `custom: «ворог знову зʼявиться зі свого джерела»` (?).
- КОЛИ `blocked(knife)` → ТО `custom: «ніж падає й лежить»` — підняти знову.
- КОЛИ `custom: «бумеранг пролетів без влучання»` → ТО `custom: «повертається до Біка»`; ЯКЩО `contact(bick, boomerang)` у польоті → ТО `pickup`.
- КОЛИ `contact(bick, enemy)` → ЯКЩО `not state(enemy, stopped)` → ТО `lose`, `lives(-1)`, `restart`.
- КОЛИ `contact(weapon, rock_roll)` → ТО `set_state(rock_roll, stopped)` — зупинений там, де влучили; стає опорою.
- КОЛИ `contact(bick, rock_roll)` → ЯКЩО `state(rock_roll, stopped)` → ТО `block` — можна стояти зверху.
- КОЛИ `timer(spawn)` → ТО `spawn_at(slow_man|fast_man, coffin)`; `spawn_at(pyonshi|rock_roll, smoke)`.
- Slow Man: `enemy-patrol` по підлозі; Fast Man: `chase-player` з драбинами; Пйонші: `chase-player` стрибками, `custom: «у стрибку проходить крізь підлогу»`; Rock Roll: `custom: «роззирається, згортається в кулю»`, далі `roll(rock_roll)` уздовж підлоги.
- КОЛИ `custom: «Бік вдруге піднявся зникомою драбиною»` → ТО `set_cell(ladder_top, floor)`, потім `custom: «драбина зникає»`.
- КОЛИ `leave(bick, vanishing_floor)` → ЯКЩО `custom: «вже вдруге»` → ТО `set_cell(cell, empty)`.
- КОЛИ `enter(bick, trigger_spot)` → ТО `spawn_at(growing_wall, ceiling)`; КОЛИ `contact(growing_wall, bick)` → ТО `lose`.
- КОЛИ `contact(bick, moving_stone)` → ЯКЩО `free(cell_behind)` → ТО `push(moving_stone)`.
- КОЛИ `enter(a, revolving_door)` → ЯКЩО `facing(a, white_side)` → ТО `move(a, dir)`; інакше `block`. Одностороння двері — те саме з плаского боку.
- КОЛИ `contact(bick, soul_stone)` → ТО `pickup`, `counter(stones_left, -1)`.
- КОЛИ `counter(stones_left, ==, 0)` → ТО `unlock(exit_door)`.
- КОЛИ `enter(bick, exit_door)` → ЯКЩО `counter(stones_left, ==, 0)` → ТО `win`, `lives(+1)`, `message(password)`, `next_level`.
- КОЛИ `input(space)` → ЯКЩО `custom: «Бік у секретній точці»` → ТО `spawn_at(pyramid, here)`; повторний стрибок → `transform(door)` — вхід у секретну кімнату (звукова кімната, пазл-пʼятнашки).
- Старт без запасних життів, +1 життя за кожну пройдену стадію. Поразка: дотик ворога, розчавлення стіною → життя −1; 0 — кінець.

## Керування і ввід
- Стрілки: вліво/вправо — рух; вгору/вниз — драбини.
- Space (одна кнопка, три дії): зі зброєю — кинути; з інструментом — копати; з порожніми руками — стрибок.
- Предмет у руках — стрибати не можна.
- Пароль вводиться на старті; спеціальні паролі відкривають режими (безсмертя FESTIVAL, продовження після game over TRYAGAIN, режими HELPMODE/GAMEMODE/DEMOMODE/KINGMODE).

## Вікна, меню, HUD
- `splash-screen` → титульне меню: GAME · EDIT (редактор) · введення пароля (?).
- `game-screen` — поле (1–6 екранів зі скролом) + `status-panel`: життя, стадія, предмет у руці (?).
- `end-screen` стадії — показує пароль (`level-password`).
- `attract-demo` — демо переходу до наступної піраміди після кожної 10-ї стадії.
- `editor-window` — редактор стадій із записом на диск або касету.
- Секретні кімнати: звукова (прослухати музику й звуки) і пазл-пʼятнашки — `custom-window`.
- Переходи: меню → game-screen → (двері) пароль → наступна стадія; кожні 10 — демо; меню → editor-window → тест.

## Фічі поза полем
- `levels-sequential`: 60 стадій у 6 пірамідах; музика міняється кожні 2 стадії.
- `level-password` на кожній стадії (формат «дві змінні літери + KONAMI»); спецпаролі = `cheat-codes`.
- `level-editor` + `level-sharing`: збереження на диск або касету; рівні сумісні між MSX1 і MSX2.
- Конкурс редактора: гравці малювали мапи на бланках з мануалу й надсилали поштою; переможці отримали золотий картридж із 20 стадіями й іменем автора.
- MSX1 і MSX2 в одній коробці (Японія): MSX2 — ремікс музики, перефарбовані предмети й тло.

## Варіації й родичі
- Попередник: [kings-valley](kings-valley.md) — одна кирка (яма 2×1), меч, сходи-діагоналі, 5 мумій з таблицею.
- Що додала II: розкладка «форма копання = інструмент» (4 інструменти), бумеранг, ворог-платформа, зникомі драбини/підлога, рухомі камені, тор-екран, редактор у картриджі.
- Родичі: [lode-runner](lode-runner.md), [lode-runner-the-legend-returns](lode-runner-the-legend-returns.md) (пристрої різної сили), [toki-tori](toki-tori.md), [solomons-key](solomons-key.md), [catrap](catrap.md).
- Осі: **форма копання** (клітина / 2×1 / 1×2 / 2×2; стіна чи підлога); **зброя** (летить і лежить / повертається); **зношування клітин** (вічні / N проходів / таймер).

## Цікавинки для курсу
- Інструмент = форма копання (стіна 2×1, підлога 1×2, стіна 2×2, підлога 2×2) — 🥉: шаблон-маска клітин відносно гравця.
- Одна кнопка — три дії залежно від того, що в руках — 🌱.
- Бумеранг: снаряд із поверненням і ловом у польоті — 📎.
- Rock Roll: ворог, який після зупинки стає платформою — 📎.
- Драбина/підлога, що зношуються за 2 проходи — 📎 (лічильник на клітині).
- Горизонтальний тор кількаекранної стадії з камерою — 📎.
- Редактор із записом рівня у файл і обміном — 🥈.

## Мапа на каталог
- Є: `move-by-input` · `ladder-climb` · `gravity-fall` · `collect-all` · `reach-exit` · `touch-death` · `environment-death` · `player-death` · `chase-player` · `enemy-patrol` · `speed-per-type` · `spawner-entity` (саркофаг) · `spawn-animation` (дим) · `dig-terrain` · `destructible-blocks` · `impassable-cells` · `cell-transform` · `timed-despawn` (?) · `one-way-cell` · `push-object` · `projectile-shot` · `temporary-modes` · `inventory-items` · `inventory-limit` · `wrap-edges` · `player-camera` · `extra-life-threshold` (+1 за стадію, не за очки — неточна відповідність) · `sequential-levels` · `level-password` · `cheat-codes` · `in-game-editor` · `editor-palette` (?) · `level-exchange` · `attract-demo`.
- **Нема** → пропозиції карток:
  - `+jump-fixed-height` «Стрибок на N клітин» · entities/move · 📎.
  - `+single-use-tool` «Одноразовий інструмент у руці» · entities/state · 📎.
  - `+dig-shape-per-tool` «Форма копання задана інструментом» · entities/interact · 🥉 · слоти {shape, target: wall|floor}.
  - `+boomerang-return` «Снаряд повертається до власника» · entities/combat · 📎.
  - `+enemy-as-platform` «Зупинений ворог — опора» · entities/move · 📎.
  - `+vanish-after-n-uses` «Клітина зникає після N проходів» · entities/interact · 📎 · слот {n}.
  - `+growing-wall` «Стіна росте зі стелі після тригера» · entities/spawn · 📎.
  - `+secret-door-by-jump` «Прихований вхід проявляється дією в точці» · levels/progression · 🌱.

## Пропозиції до словників
- `+effect:dig(cell, shape)` — прибрати блоки маскою відносно гравця.
- `+effect:jump(height)` — стрибок на N клітин.
- `+effect:return_to(a, owner)` — снаряд повертається до власника.
- `+cond:uses(a, op, n)` — клітиною скористались N разів (зношування).
- `+trigger:used(a)` — сутністю/клітиною щойно скористались (пройшли, піднялись).
- `+feature:level-save-tape` — запис рівнів на касету/диск як носій обміну.
- `+feature:edit-contest` — конкурс користувацьких рівнів від видавця.
- `+card:dig-shape-per-tool`, `+card:vanish-after-n-uses` — див. вище.

## Джерела
- ⭐ [Wikipedia JA: 王家の谷 エルギーザの封印](https://ja.wikipedia.org/wiki/王家の谷_エルギーザの封印) — Space-контекст, ніж/бумеранг, молот/лопата/дриль/кирка з формами, 4 вороги, зникомі драбина й підлога, ростучі стіни, рухомі камені, двоє типів дверей, 1–6 екранів з торами, 60 стадій, життя +1 за стадію, паролі, конкурс редактора, MSX1/MSX2.
- [Wikipedia EN: King's Valley II](https://en.wikipedia.org/wiki/King%27s_Valley_II) — 6 пірамід × 10, камені душі відчиняють вихід, редактор із записом на диск/касету, сумісність MSX1/MSX2, конкурс із золотим картриджем на 20 стадій.
- [Generation MSX: читі](https://generation-msx.nl/software/konami/kings-valley-ii-the-seal-of-el-giza/cheats/1079) — формат паролів, спецпаролі, секретні кімнати через стрибок у точці.
- YouTube: пошук «King's Valley II MSX gameplay».

## Непевне
- (?) Чи ворог після влучання зброї гине назавжди чи повертається (і через скільки).
- (?) Як саме відчиняються вихідні двері (в оригіналі I — стрибком під перемикач); тут лише «камені відчиняють вихід».
- (?) Скільки стадій вміщує редактор і чи можна тестувати рівень прямо з нього.
- (?) Очки й HUD не описані в джерелах.
- (?) Чи мумії й Rock Roll падають у викопані ями.
- (?) «Спецпаролі» з Generation MSX, ймовірно, для MSX2-версії; для MSX1 не перевірено.
