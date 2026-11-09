---
title: "Krusty's Fun House"
slug: krustys-fun-house
aka: ["Krusty's Super Fun House", "Rat Trap (оригінал, 1991)"]
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 1992
platforms: [SNES, Genesis, NES, Master System, Game Gear, Game Boy, Amiga, DOS]
links:
  - {kind: other, url: "https://www.video-games-museum.com/en/faqs/Megadrive/3006-Krustys-Super-Fun-House.pdf", best: true, note: "FAQ SubSane (Genesis): поведінка щурів, таблиця блоків і предметів, керування, HUD, кімнати й двері, пастки, паролі"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Krusty%27s_Fun_House", note: "походження від Rat Trap (Fox Williams, Audiogenic), версії, пастки персонажів Сімпсонів, вороги й пироги"}
  - {kind: other, url: "https://simpsonswiki.com/wiki/Krusty's_Fun_House", note: "Simpsons Wiki"}
  - {kind: other, url: "https://www.almarsguides.com/retro/walkthroughs/snes/games/KrustysSuperFunHouse/", note: "проходження SNES"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Krusty%27s+Super+Fun+House+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, gravity-fall, move-auto, turn-when-blocked, destructible-blocks, hidden-under-block, item-pickup, projectile-shot, hp-damage, touch-death, player-death, event-points, time-bonus, level-password, level-unlock, sequential-levels, game-pause, status-panel, game-screen, +auto-walker-guide, +carry-one-block, +place-block, +step-climb-1, +fan-blow, +pipe-travel, +capture-jar, +kick-slide, +hub-room-doors, +secret-area, +group-herding]
proposes: ["+effect:blow(a, dir)", "+effect:kick(b)", "+cond:height_diff(a, cell, op, n)", "+window:hub-room", "+ui:held-block", "+card:fan-blow", "+card:capture-jar", "+card:hub-room-doors", "+card:group-herding"]
author: opus
date: 2026-11-09
---

# Krusty's Fun House — клоун Красті будує блоками сходинки й труби, щоб тупі щури самі дійшли до пастки

## Суть
Гібрид платформера й Lemmings: Красті бігає, стрибає й бʼється пирогами, але головне — **щури**, що йдуть самі: перелазять усе, що не вище за них, і розвертаються біля вищої стіни. Красті підбирає й ставить блоки (звичайні, труби, вентилятори, пружини, глеки), щоб зробити щурам сходинку, загородити яму чи направити трубою — до пастки, яку крутить Барт, Гомер, Сайдшоу Мел чи Капрал Покарання. Двері-рівні розкидано по кімнатах-хабах; кімнату закрито, коли пройдено всі її двері.

## Поле і час
- Двері ведуть у рівень: кілька повʼязаних екранів збоку з платформами, ямами, рухомими платформами й ліфтами; камера за Красті.
- Структура: 5 кімнат (світів) × кілька дверей; двері 8 кімнати 1 відкриваються після 1–7; останні двері кімнати — після «спецблоку» в інших.
- Real-time; деякі рівні з таймером (бонус за залишок).
- Блоки займають клітину; щур перелазить перепад у 1 блок, вищий — розвертає.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Красті | player | 10 ударів до втрати життя; життя | біг, стрибок, підняти/поставити блок, кинути пиріг/кульку, копнути блок |
| Щур | neutral | напрямок | іде вперед; перелазить перепад ≤ свого росту; біля вищої перешкоди — розворот; падає в ями |
| Синій блок | object | — | носять і ставлять; сходинка для щурів і Красті |
| Блок-труба | conduit | пряма / L | ставлять у розрив труби; труба переносить щурів між висотами |
| Труба (статична) | conduit | горизонтальна / вертикальна | горизонтальну щури переходять, вертикальна — перешкода; вхід → вихід |
| Блок-вентилятор | object | напрям: вгору / вліво / вправо | дме щурів у свій бік; повернутий до стіни — тримає щурів купкою |
| Пружина | object | — | підкидає Красті; утримання стрибка — вище |
| Глек (jar) | container | 0 / 1 щур | ловить одного щура; копнути — розбити й випустити; можна носити як блок |
| Бочка | object | — | копнути — котиться вбік, падає з краю |
| Фіолетовий блок | container | вміст | копнути — предмет, новий прохід, новий фіолетовий блок або платформа |
| Спецблок (фіолетовий) | switch | — | відкриває приховані двері в кімнаті / закриває кімнату |
| Коричневий блок | terrain | — | ламається, коли на ньому стоять, або кулькою |
| Пастка (Smash-/Zap-/Pop-/Eat-/Slice-O-Matic) | sink | оператор | щур, що зайшов, знищується |
| Рухома платформа / ліфт | platform | — | везе Красті |
| Невидима платформа | terrain | прихована | зʼявляється після удару по фіолетовому блоку над нею |
| Змії, прибульці, летючі свині, птахи | enemy | очки за кімнату 100–1000 | шкодять Красті при дотику; гинуть від пирога |
| Краплі води, лазерна гармата | hazard | — | шкодять Красті |
| Пироги / кульки | projectile | запас | кидок уперед; кульки ще й ламають коричневі блоки й тріснуті стіни |
| Бургер, чіпси, Squishee | pickup | — | відновлюють здоровʼя |
| Іконка Красті | pickup | — | +1 життя |
| Мішечок / кухоль / ріжок | pickup | 10 / 20 / 50 | очки |
| Двері | gate | закриті / відкриті / пройдені | вхід у рівень; вихід з рівня — тими ж дверима |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(rat, facing)`; ЯКЩО `not supported(rat)` → ТО `fall(rat)`.
- КОЛИ `blocked(rat)` → ЯКЩО `custom: «перешкода в 1 блок»` → ТО `custom: «щур вилазить на неї»`; інакше `face(rat, reverse)`.
- КОЛИ `input(down)` → ЯКЩО `occupied(below, block)` і `not has(player, block)` → ТО `pickup` блока (у «коробку блоків»).
- КОЛИ `input(down)` → ЯКЩО `has(player, block)` і `free(cell)` → ТО `place(block, cell)`.
- КОЛИ `input(kick)` → ЯКЩО `occupied(front, barrel)` → ТО `custom: «бочка котиться вбік, падає з краю»`.
- КОЛИ `input(kick)` → ЯКЩО `occupied(front, purple_block)` → ТО `reveal(contents)` — `spawn_at(item, here)` або `set_cell(passage, open)` або `spawn_at(platform, hidden)`.
- КОЛИ `contact(rat, fan)` → ТО `custom: «щура віднесе в напрямку вентилятора»`.
- КОЛИ `enter(rat, pipe_in)` → ТО `custom: «щур проходить трубою до виходу»` → `move(rat, pipe_out)`.
- КОЛИ `contact(rat, jar)` → ЯКЩО `count(rats_in_jar, ==, 0)` → ТО `custom: «щур усередині глека»`; КОЛИ `input(kick)` → ЯКЩО `occupied(front, jar)` → ТО `custom: «глек розбито, щур виходить»`.
- КОЛИ `enter(rat, trap)` → ТО `disappear_a`, `animate(operator)`.
- КОЛИ `all_gone(rat)` → ТО `custom: «рівень дверей пройдено»`, вихід через двері.
- КОЛИ `enter(player, brown_block)` або `contact(marble, brown_block)` → ТО `disappear_b`.
- КОЛИ `input(throw)` → ЯКЩО `has(player, ammo)` → ТО `spawn_at(pie, front)`, `take(player, ammo)`; КОЛИ `contact(pie, enemy)` → ТО `disappear_b`, `score(n)`.
- КОЛИ `contact(player, enemy)` або `contact(player, hazard)` → ТО `damage(1)`; КОЛИ `hp_zero(player)` → ТО `lives(-1)`.
- КОЛИ `contact(player, food)` → ТО `heal(player, n)`; КОЛИ `contact(player, krusty_icon)` → ТО `lives(+1)`.
- КОЛИ `contact(player, spring)` → ТО `custom: «підкидає; утримання стрибка — вище»`.
- КОЛИ `custom: «усі двері кімнати пройдено + спецблок»` → ТО `unlock(next_room)`; після кімнати 5 — `custom: «повернутись до головних дверей»` → `win`.
- КОЛИ `level_end` → ЯКЩО `timer(op, n)` → ТО `score(time_left)` (рівні з таймером).
- Перемога: очистити всі 5 кімнат. Поразка: 0 життів. Рахунок: вороги (100/100/500/500/1000 за кімнату), предмети 10–50, залишок часу.

## Керування і ввід
- ←/→ — рух; ↑ — увійти в двері; ↓ — підняти/поставити блок; A — стрибок; B — кинути пиріг/кульку або копнути блок.
- Select — вийти з дверей (рестарт рівня), Start — пауза.
- Тактика: спершу оглянути весь рівень; зібрати щурів у купку (два-три блоки або вентилятор до стіни); блок під виходом труби ставити й забирати вчасно, поки щур перелазить.

## Вікна, меню, HUD
- `splash-screen` — титул.
- `level-password` — екран пароля одразу після Start (порожній — нова гра).
- `+window:hub-room` — кімната-хаб: Красті ходить між дверима (пройдені/закриті/відкриті).
- `game-screen`: рівень + HUD: блок у руках (`+ui:held-block`) угорі зліва, `score` (6 цифр), поточна зброя з запасом, `lives`; здоровʼя не показано — Красті важко дихає, коли мало.
- `pause-menu` — пауза; вихід з рівня з паузи.
- `end-screen` — фінальне повідомлення «GET TO THE MAIN DOOR» → перемога.
- Переходи: титул → пароль → хаб-кімната → двері (рівень) → хаб → наступна кімната.

## Фічі поза полем
- `level-password`: 4 паролі — після кожної кімнати 1–4.
- `level-unlock`: двері відкриваються послідовно / за спецблоком; кімнати — по черзі.
- Секретні зони (`+secret-area`): бонусні кімнати за фіолетовими «магічними» блоками; деякі обовʼязкові для відкриття останніх дверей.
- `pause`; `restart-level` через вихід з дверей.

## Варіації й родичі
- Оригінал: Rat Trap (1991, Fox Williams / Audiogenic, Atari ST, Amiga, C64) — та сама гра, перемальована під ліцензію The Simpsons; Genesis/SNES/DOS/Amiga — «Super Fun House»; NES/SMS/Game Boy — інші версії.
- Родичі: Lemmings (автоходці, яких треба врятувати/знищити), [troddlers](troddlers.md) (блоки + автоходці), [mario-and-wario](mario-and-wario.md), [block-dude](block-dude.md) (носити один блок, сходинка в 1), [fire-n-ice](fire-n-ice.md) (труби), [mario-vs-donkey-kong](mario-vs-donkey-kong.md) (вести міні-Маріо).
- Осі: **керування автоходцями** (непряме: будуєш середовище / пряме: даєш ролі як у Lemmings); **висота, яку долає автоходець** (0 / 1 блок / будь-яка); **ціль автоходців** (врятувати / знищити в пастці).

## Цікавинки для курсу
- Автоходець «іди, перелазь ≤1, розвертайся біля вищого» — 🌱.
- Носити один блок і ставити його як сходинку/стіну, рахуючи висоту для щурів — 📎.
- Вентилятор, що дме автоходців у свій бік; повернутий до стіни — «загін» — 📎.
- Труба: вхід переносить сутність до виходу; розрив лагодиться блоком-трубою — 📎.
- Глек-контейнер на одного щура, який можна носити й розбити над пасткою — 🥉 (сутність у сутності).
- Хаб-кімната з дверима-рівнями та прихованими дверима — 🥉.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `move-auto` (щури) · `turn-when-blocked` · `destructible-blocks` (коричневі) · `hidden-under-block` (фіолетові) · `item-pickup` · `projectile-shot` (пироги, кульки) · `hp-damage` (10 ударів) · `touch-death` · `player-death` · `event-points` · `time-bonus` · `level-password` · `level-unlock` · `sequential-levels` · `game-pause` · `status-panel` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+fan-blow` «Вентилятор зсуває сутності в напрямку» · entities/move · 📎 · слот {dir}.
  - `+capture-jar` «Контейнер ловить одну сутність; розбити — випустити» · entities/interact · 🥉.
  - `+hub-room-doors` «Хаб: двері-рівні, відкриття за умовою» · levels/progression · 🥉.
  - `+group-herding` «Зібрати автоходців у купку перед випуском» · entities/move · 📎.
  - `+auto-walker-guide`, `+carry-one-block`, `+place-block`, `+step-climb-1`, `+pipe-travel` — як у Troddlers, Block Dude, Fire 'n Ice; `+kick-slide`, `+secret-area`.

## Пропозиції до словників
- `+effect:blow(a, dir)` — потік повітря зсуває сутність (вентилятор).
- `+effect:kick(b)` — копнути обʼєкт: зсув/розбиття/відкриття залежно від типу.
- `+cond:height_diff(a, cell, op, n)` — перепад висоти перед сутністю (≤1 — перелазить).
- `+window:hub-room` — ігрова кімната-хаб з дверима замість меню вибору рівня.
- `+ui:held-block` — слот предмета в руках.
- `+card:fan-blow`, `+card:capture-jar`, `+card:hub-room-doors`, `+card:group-herding`.

## Джерела
- ⭐ [FAQ/Walkthrough by SubSane (Genesis), PDF](https://www.video-games-museum.com/en/faqs/Megadrive/3006-Krustys-Super-Fun-House.pdf) — поведінка щурів, таблиці блоків, предметів і очок, керування, HUD, 10 ударів, 5 кімнат з ворогами й операторами пасток, паролі.
- [Wikipedia: Krusty's Fun House](https://en.wikipedia.org/wiki/Krusty%27s_Fun_House) — походження від Rat Trap, версії, пастки Барта/Гомера/Капрала Покарання/Сайдшоу Мела, вороги й пироги.
- [Simpsons Wiki](https://simpsonswiki.com/wiki/Krusty's_Fun_House), [Almar's Guides (SNES)](https://www.almarsguides.com/retro/walkthroughs/snes/games/KrustysSuperFunHouse/) — у результатах пошуку, не відкривав.
- YouTube: пошук «Krusty's Super Fun House gameplay».

## Непевне
- (?) FAQ — версія Genesis; NES/Game Boy/SMS відрізняються (інша структура рівнів, менше блоків).
- (?) Чи може Красті нести більше одного блока (HUD — «коробка блоків»).
- (?) Чи щури гинуть від падіння з висоти або від ворогів.
- (?) Чи вентилятор можна повернути, чи напрям фіксований на блоці.
- (?) Як саме пастку запускає оператор — автоматично при вході щура (за FAQ — так).
