---
title: Solomon's Key
slug: solomons-key
family: grid-platformer
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: state
year: 1986
platforms: [arcade (Tecmo), NES/Famicom, Master System, C64, ZX Spectrum, Game Boy (Solomon's Club)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Solomon%27s_Key", best: true, note: "основи: блоки, ключ і двері, таймер, вороги без ліміту, печатки й секретні кімнати"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ソロモンの鍵_(ゲーム)", note: "JA: де ставиться блок, феї й дзвін, глеки вогню, зілля, порти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=solomon%27s+key+arcade+gameplay", note: "пошук; геймплей аркади"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=solomon%27s+key+nes+longplay", note: "пошук; NES longplay з секретами"}
stage: v1
coverage: 60
mechanics: [move-4dir, gravity-fall, key-and-door, reach-exit, touch-death, player-death, spawn-points, spawn-schedule, projectile-shot, inventory-items, item-pickup, time-out, time-bonus, event-points, impassable-cells, cell-transform, sequential-levels, status-panel, +create-destroy-block, +headbutt-break, +hidden-item-in-block, +summon-fairy, +secret-room-seal, +undercut-enemy]
proposes: ["+effect:toggle_block", "+trigger:headbutt", "+trigger:cast", "+cond:hit_count", "+role:spawner", "+effect:reveal", "+feature:secret-levels", "+card:create-destroy-block"]
author: opus
date: 2026-11-02
---

# Solomon's Key — маг створює й руйнує блоки перед собою, щоб дістати ключ і вийти в двері до кінця часу

## Суть
Маг Dana на одноекранній кімнаті з блоків має взяти ключ і дійти до дверей, поки спадає лічильник часу-життя. Головна дія — **заклинання: створити помаранчевий блок у порожній клітині перед собою (або навскіс униз) чи прибрати вже наявний**. Блоками будують сходи, закривають ворогів і вибивають опору з-під них; білі камʼяні блоки незмінні. Вороги безкінечно виходять із «дзеркал»-генераторів, дотик — смерть; знищити їх можна лише обмеженими вогняними кулями або скинувши. У блоках сховано предмети — дзвін, що кличе фей, печатки до секретних кімнат.

## Поле і час
- Одноекранна кімната-сітка (≈ 15×12 клітин (?)); бічний вид, гравітація для Dana і частини ворогів.
- Real-time; час кімнати — лічильник, що спадає (у NES відображається як «LIFE») (?); нуль → смерть.
- Клітина: порожньо / помаранчевий блок (стан: цілий / тріснутий після удару головою) / білий блок / двері / генератор ворогів.
- Інформація часткова: предмети приховані в блоках чи порожнечі й проявляються лише після «створити-зруйнувати» у потрібній клітині.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Dana | player | життя; запас вогню | біг, стрибок, присідання; заклинання блоку; вогняна куля |
| Помаранчевий блок | object | цілий / тріснутий | створюється/руйнується заклинанням; 2 удари головою — руйнується |
| Білий блок | static | — | незмінний, непрохідний; заклинання не діє |
| Ключ | pickup | — | взяття відкриває двері |
| Двері | gate | закриті/відкриті | відкриті + Dana = кімнату пройдено |
| Генератор («дзеркало») | spawner | період | безкінечно випускає ворогів; поруч з ним блок не ставиться |
| Вороги (кілька видів) | enemy | вид | ходять/літають за своїм патерном; дотик — смерть |
| Глек вогню (Manda jar) | pickup | +заряд | дає вогняну кулю (обмежений запас на всю гру) |
| Вогняна куля | projectile | — | знищує ворогів; спалює фею, якщо влучить |
| Зілля (Melt'na) | pickup | — | знищує певні типи ворогів |
| Дзвін (Lilac bell) | pickup | — | з дверей вилітає фея |
| Фея | pickup | — | летить до Dana; 10 фей = додаткове життя |
| Печатка (Seal) | pickup | одна на сузірʼя | відкриває секретну бонус-кімнату сузірʼя |
| Предмети-очки, життя | pickup | — | приховані; очки / +1 життя / покращення вогню |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(dana, dir)`; `input(jump)` → стрибок угору/вперед; без опори — `fall(dana)`.
- КОЛИ `input(cast)` → ЯКЩО `free(cell_ahead)` і `not custom: «біля генератора»` → ТО `set_cell(cell_ahead, orange_block)`; ЯКЩО `cell(cell_ahead, orange_block)` → ТО `set_cell(cell_ahead, empty)`; ЯКЩО білий блок → нічого.
- Присід + заклинання → ціль — клітина навскіс униз-вперед; з краю клітини блок ставиться на 2 клітини далі.
- КОЛИ `custom: «Dana вдаряється головою в помаранчевий блок у стрибку»` → ТО перший раз `set_state(block, cracked)`, другий раз `set_cell(block, empty)`.
- КОЛИ `custom: «блок зруйновано / створено-зруйновано в особливій клітині»` → ТО `reveal(hidden_item)`.
- КОЛИ `contact(dana, key)` → ТО `pickup`, `set_state(door, open)`.
- КОЛИ `contact(dana, door)` → ЯКЩО `state(door, open)` → ТО `win` кімнати, `score(time_left)` (?), `next_level`.
- КОЛИ `timer(spawn)` → ТО `spawn(enemy)` з генератора; кількість не обмежена.
- КОЛИ `contact(dana, enemy)` → ТО `lose` (життя −1, кімната спочатку).
- КОЛИ `custom: «блок під ворогом зник»` → ТО `fall(enemy)` (?) — вибити опору; деякі вороги так гинуть або відходять.
- КОЛИ `input(fire)` → ЯКЩО `has(dana, fire)` → ТО `spawn(fireball)`, `take(dana, fire)`; КОЛИ `contact(fireball, enemy)` → ТО `disappear_both`; КОЛИ `contact(fireball, fairy)` → ТО `disappear(fairy)`.
- КОЛИ `contact(dana, bell)` → ТО `spawn_at(fairy, door)`; фея `custom: «дрейфує до Dana»`; `contact(dana, fairy)` → `counter(fairies, +1)`; `counter(fairies, ==, 10)` → `lives(+1)`.
- КОЛИ `contact(dana, seal)` → ТО `unlock(secret_room)` сузірʼя.
- КОЛИ `counter(time, ==, 0)` → ТО `lose`.
- Перемога гри: пройти всі сузірʼя; кінцівка залежить від знайдених печаток і секретних кімнат (кімната принцеси). Поразка: 0 життів. Рахунок: предмети-очки, феї, залишок часу (?); NES показує «GDV» — зважену оцінку гри.

## Керування і ввід
- Джойстик: ліво/право — біг, вгору — стрибок (аркада) (?), вниз — присісти.
- Кнопка заклинання (створити/зруйнувати блок), кнопка вогню.
- Ціль заклинання визначає поза: стоячи — клітина попереду, присівши — навскіс униз.

## Вікна, меню, HUD
- `splash-screen` / атракт.
- `game-screen` — кімната + HUD: `score`, `hi-score`, лічильник часу/життя (`timer-countdown`), `lives`, номер кімнати, запас вогню (`inventory-bar`) (?).
- Екран сузірʼя між групами кімнат (`custom-window` «constellation») (?).
- `end-screen` кімнати (нарахування бонусу), `game-over-continue` (?).
- NES: екран game over з «GDV»-оцінкою (`custom-window`).
- Master System / PC Engine: `level-password` — пароль кімнати (у NES паролів нема).
- Переходи: атракт → game-screen → (двері) бонус → наступна кімната; (печатка) → секретна кімната; (0 життів) game over → атракт.

## Фічі поза полем
- `levels-sequential`: 50 кімнат «сузірʼїв» (аркада); NES — 64 рівні: 48 основних (12 знаків зодіаку × 4), 15 секретних, фінальна кімната.
- Секретні рівні за печатками + розгалужена кінцівка (`collectibles`).
- Паролі — лише в деяких портах (SMS, PC Engine).
- Нема редактора, збережень, налаштувань у грі.

## Варіації й родичі
- Порти: NES (більше рівнів і секретів), SMS (паролі, підказка місця ключа), Game Boy — Solomon's Club (крамниця, нові предмети).
- Solomon's Key 2 / Fire 'n Ice (1992) — та сама ідея «створи/знищ блок», але лід і вогонь, без стрибків: чистий пазл.
- Родичі: Lode Runner (руйнування клітин), Catrap, Lolo; Mighty Bomb Jack (той самий розробник — камео).
- Осі: **де можна ставити блок** (попереду / навскіс / будь-де); **як руйнується блок** (заклинання / удар головою / вогонь); **ворожий спавн** (фіксований склад / безкінечний генератор).

## Цікавинки для курсу
- Одна кнопка «create/destroy» на клітину перед аватаром з урахуванням пози — 📎.
- Удар головою: лічильник ударів у стані блоку (цілий → тріснутий → зник) — 🌱.
- Схованки, що проявляються лише після «створити й зруйнувати» в певній клітині — 📎.
- Безкінечний генератор ворогів + заборона ставити блок поряд — 🥉.
- Вибити опору з-під ворога — гравітація ворогів як зброя — 📎.
- Феї-лічильник до життя і вогонь, що їх спалює — 🌱 (компроміс ресурсу).
- Розгалужена кінцівка за знайденими секретами — 🥉.

## Мапа на каталог
- Є: `move-4dir` (біг + стрибок) · `gravity-fall` · `key-and-door` · `reach-exit` · `touch-death` · `player-death` · `spawn-points` + `spawn-schedule` (генератори) · `projectile-shot` (вогонь) · `inventory-items` (запас вогню) · `item-pickup` · `time-out` · `time-bonus` (?) · `event-points` · `impassable-cells` (білі блоки) · `cell-transform` · `sequential-levels` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+create-destroy-block` «Створити/прибрати блок перед собою» · entities/interact · 📎 · слот {targets: ahead|diag-down}.
  - `+headbutt-break` «Руйнування ударом знизу за N ударів» · entities/interact · 🌱.
  - `+hidden-item-in-block` «Предмет у блоці / порожнечі» · entities/interact · 📎.
  - `+summon-fairy` «Предмет кличе бонус-сутність» · entities/spawn · 🌱.
  - `+secret-room-seal` «Предмет відкриває секретний рівень» · levels/progression · 📎.
  - `+undercut-enemy` «Вибити опору з-під ворога» · entities/move · 📎.

## Пропозиції до словників
- `+effect:toggle_block(cell)` — порожньо ↔ блок однією дією.
- `+trigger:headbutt(a, cell)` — удар головою об клітину знизу (стрибок у стелю).
- `+trigger:cast(a, target)` — гравець застосував заклинання до клітини (окремо від `input`, бо ціль залежить від пози).
- `+cond:hit_count(cell, n)` — скільки разів клітину вже вдарено.
- `+role:spawner` — генератор ворогів (є ⏳ — ще одне вживання).
- `+effect:reveal` ↔ є `reveal(cells)`; тут — проявити прихований предмет.
- `+feature:secret-levels` — секретні рівні + розгалужена кінцівка.
- `+card:create-destroy-block` — див. вище.

## Джерела
- ⭐ [Wikipedia: Solomon's Key](https://en.wikipedia.org/wiki/Solomon%27s_Key) — блоки, удар головою двічі, ключ і двері, таймер, вороги без ліміту, предмети, печатки, 64 рівні NES, GDV.
- [Wikipedia JA: ソロモンの鍵 (ゲーム)](https://ja.wikipedia.org/wiki/ソロモンの鍵_(ゲーム)) — блок попереду / навскіс униз / через клітину з краю, білі блоки й зони біля генераторів, глек вогню, зілля, дзвін і феї (10 = життя), порти.
- YouTube: пошук «solomon's key arcade gameplay» і «solomon's key nes longplay».

## Непевне
- (?) Розмір кімнати (≈15×12), кнопка стрибка (вгору чи окрема), вигляд HUD — з памʼяті.
- (?) Імена й патерни ворогів (Demonhead, Sparkball, Goblin, Gargoyle, Dragon тощо) не перевірено — тому в таблиці один рядок «вороги».
- (?) Як рухається вогняна куля (по контуру поверхні?) і що дають сувої/покращення вогню.
- (?) Чи вибивання блоку вбиває ворога падінням, чи лише скидає.
- (?) Пісочний годинник і інші предмети з брифу — не підтверджено джерелами; ліміт пошуку сесії вичерпано.
- (?) Бонус за залишок часу при виході.
