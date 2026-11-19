---
title: Snake (Змійка) / Nibbles / Nokia Snake
slug: snake
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 1976
platforms: [arcade (Blockade 1976), BBC Micro, MS-DOS (Nibbles 1991), Nokia 6110/5110, web, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Snake_(video_game_genre)", best: true, note: "жанр цілком: правила, історія від Blockade до Slither.io і Snake.io"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Nibbles_(video_game)", note: "QBasic Nibbles: цифри 1–9, рівні з перешкодами, двоє гравців"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Snake_(1998_video_game)", note: "Nokia Snake і наступники: Snake II, EX, Xenzia"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Blockade_(video_game)", note: "предок 1976: двоє гравців, слід = стіна"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Slither.io", note: "сучасний мультиплеєр: буст за масу, смерть → гранули"}
  - {kind: play, url: "https://slither.io/", note: "грати в браузері"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=nokia+snake+II+gameplay+3310", note: "пошук; Snake II з лабіринтами"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=qbasic+nibbles+gameplay", note: "пошук; Nibbles"}
stage: v2
coverage: 70
mechanics: [move-auto, body-queue, std-collections, spawn-random-cell, item-pickup, touch-death, progress-acceleration, impassable-cells, timed-despawn, event-points, score-records, sequential-levels, difficulty-levels, player-death, game-pause, ai-opponent, swipe-gestures, keyboard-controls, +no-reverse-turn, +wrap-edges, +self-collision, +relative-turn-controls, +boost-for-mass, +death-drops-loot, +simultaneous-versus]
proposes: ["+trigger:self_contact", "+effect:drop", "+effect:boost", "+card:no-reverse-turn", "+card:wrap-edges", "+card:boost-for-mass", "+card:death-drops-loot", "+feature:maze-select", "+axis:control"]
author: opus
date: 2026-11-02
---

# Snake — голова біжить сама, тіло росте з кожною їжею, врізатися в себе не можна

## Суть
Гравець керує лише напрямком голови змійки, що рухається безупинно; кожна їжа подовжує тіло, і найбільший ворог — власний хвіст, який займає дедалі більше поля. Жанр виріс із дуельного Blockade (1976), де слід лишався назавжди (див. `tron-light-cycles`), і став «змійкою», коли хвіст почав рухатися за головою. Варіанти відрізняються стінами (смерть чи обгортання), лабіринтами, бонусами й темпом; .io-нащадки зробили з нього мультиплеєр з масою як ресурсом.

## Поле і час
- Класика: прямокутна сітка (Nokia — «коробка розміром з екран»; Nibbles — сітка 80×50, емульована в текстовому режимі 80×25).
- Межа поля: суцільна стіна (Nokia 6110, Nibbles) або тор — вихід за край з'являється з протилежного (Snake II без лабіринту) (?).
- Тік = крок голови на 1 клітину; швидкість — налаштування рівня (Nokia: рівні 1–9 (?)) або росте з довжиною (BBC Micro) / з рівнем (Nibbles).
- Slither.io: вільне поле-коло (`free`), рух неперервний, без сітки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Голова змійки | player | напрям, швидкість | щотік крок у напрямку; розворот на 180° заборонено |
| Тіло (сегменти) | object | довжина, черга клітин | кожен сегмент займає місце попереднього (хвіст повторює шлях) |
| Їжа (яблуко/точка/куля) | pickup | очки, +N довжини | зʼявляється у вільній випадковій клітині, одна на полі |
| Бонус-жук (Snake II) | pickup | лічильник часу, більше очок | зʼявляється періодично, зникає за часом (?) |
| Цифра 1–9 (Nibbles) | pickup | номер | з'являються по черзі; кожна подовжує змійку; після 9 — наступний рівень |
| Стіна / межа | static | — | дотик — смерть |
| Перешкоди лабіринту | static | макет рівня | дотик — смерть; різні макети рівнів/лабіринтів |
| Друга змійка (Nibbles, Blockade) | player | своя клавіатура | дотик до будь-якого тіла — смерть |
| Гранули (Slither.io) | pickup | маса | розкидані по полю; «chase»-гранули тікають від змійок |
| Чужа змійка (Slither.io) | enemy | маса, довжина | голова в чуже тіло — смерть; тіло → яскраві гранули |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(head, dir)`; тіло — `custom: «кожен сегмент на місце попереднього; хвіст звільняє клітину»` (черга: push голова, pop хвіст).
- КОЛИ `input(dir)` → ЯКЩО `not moving(head, opposite(dir))` → ТО `face(head, dir)` (одна зміна на тік, решта в буфер (?)).
- КОЛИ `contact(head, food)` → ТО `disappear_b`, `grow(snake, n)` (хвіст не знімається n тіків), `score(+k)`, `spawn_at(food, random_free)`.
- КОЛИ `contact(head, body)` → ТО `lose` — самозіткнення; у мультиплеєрі — те саме з чужим тілом.
- КОЛИ `contact(head, wall)` → ТО `lose`.
- КОЛИ `edge(head)` → ЯКЩО `mode(no_walls)` → ТО `wrap(head)`; інакше `lose`.
- КОЛИ `counter(eaten, %, 5)` → ТО `spawn_at(bonus_bug, random_free)`, `timer(start)`; КОЛИ `timer(0)` → `disappear_a` (Snake II, ?).
- КОЛИ `contact(head, bonus_bug)` → ТО `score(+k × time_left)` (?), без росту або з ростом (?).
- КОЛИ `counter(length|level, ≥, n)` → ТО `speed(snake, +1)` (BBC Micro: швидшає з ростом, одне життя; Nibbles: новий рівень швидший).
- КОЛИ `picked(digit_9)` (Nibbles) → ТО `next_level` — складніші перешкоди і вища швидкість.
- КОЛИ `input(boost)` (Slither.io) → ЯКЩО `counter(mass, >, min)` → ТО `speed(snake, ×k)`, `shrink(snake, 1)` щотік, `custom: «скинута маса лишається гранулами позаду»`.
- КОЛИ `died(snake)` (Slither.io) → ТО `custom: «тіло → великі гранули кольору змійки»`; від межі-кола — без гранул.
- Перемога: нема (рекорд) / усі цифри рівня (Nibbles) / вижити довше за суперника (Blockade: гра до 3–6 зіткнень, задає оператор). Поразка: зіткнення, у Nibbles — втрата життя і рестарт рівня (?). Рахунок: очки за їжу, у Nokia — більше на вищій швидкості (?).

## Керування і ввід
- Абсолютне: 4 стрілки / цифрова клавіатура (Nokia; клавіші 2-4-6-8 (?)) задають напрям; розворот назад ігнорується.
- Відносне: «повернути ліворуч/праворуч» від напрямку голови (BBC Micro Snake) — дві кнопки замість чотирьох.
- Тач: свайп (Snake Rewind, Snake.io) (?); Slither.io — голова повертає до курсора миші; буст — пробіл, стрілка вгору або кнопка миші, на мобільному — подвійний дотик.
- Nibbles вдвох: дві групи клавіш на одній клавіатурі, одночасно (не по черзі).

## Вікна, меню, HUD
- `main-menu` (Nokia, з памʼяті (?)): New game · Level (швидкість) · Mazes (Snake II) · Top score · Instructions → `help-window`.
- `game-screen`: поле + `score` (і `hi-score`), у Snake II — `timer-countdown` бонус-жука (?); Nibbles — `score` і `lives` для кожного гравця, `level-number`.
- `settings-window` / `difficulty-select`: рівень швидкості 1–9 (?); Nibbles — кількість гравців і швидкість на старті (?).
- `end-screen` «Game over» + рахунок; `leaderboard` — один найкращий рахунок (Nokia), топ-10 за масою на сервері (Slither.io, у правому верхньому куті).
- `pause-menu` (Nokia — вихід у меню ставить паузу (?)).
- Slither.io: `main-menu` з полем імені + `skin-select` (66 стандартних скінів, 32 косметики, 19 фонів; конструктор «Build a Slither»), `minimap` (?).
- Переходи: main-menu → game-screen → (смерть) end-screen → main-menu.

## Фічі поза полем
- `difficulty-presets` — рівень швидкості; `maze-select` — вибір макета перешкод (Snake II) (?).
- `leaderboard-local` (один рекорд), `leaderboard-online` (Slither.io, топ-10 серверу).
- `local-multiplayer` одночасний (Nibbles, Blockade); `online-multiplayer` (Slither.io); `ai-opponent-levels` — режим «проти AI» на мобільному Slither.io.
- `custom-skins`, `unlockables` (Snake.io).
- Нема undo, редактора, збережень.

## Варіації й родичі
- Blockade (1976) і клони Surround / Tron Light Cycles — слід не зникає (вісь «хвіст рухається чи лишається»).
- Nibbler (1982) — змійка в тісному лабіринті, швидше за класику; Rattler Race (1992) — ворожі змійки; Snake Byte (1982) — яблука закривають рівень.
- Nokia: Snake (1998, 6110/5110), Snake II (7110; лабіринти (?)), EX (2002), EX2 (2003), III (2005), Xenzia (2005); Snake Rewind (2015) — духовний наступник.
- .io: Slither.io (2016, маса і буст), Snake.io (2016, Kooapps); Snake Core (2020, OrangePixel) — зі стрільбою.
- Thinky-родич: Snakebird (гравітація для змійки) — у `thinky`; Snake Pass (2017) — 3D-платформер з фізикою тіла без сітки, у корпус не взято.
- **Осі варіацій:**
  - межа: стіна-смерть / обгортання (тор) / лабіринт усередині;
  - зростання: +1 / +N / росте від цифри (Nibbles);
  - темп: фіксований (налаштування) / росте з довжиною / росте з рівнем / буст гравцем за масу;
  - самозіткнення: смерть / відкушує хвіст (деякі сучасні клони) (?) / дозволене (Slither.io — своє тіло не вбиває (?));
  - керування: абсолютне / відносне (ліво-право) / до курсора;
  - смерть: кінець гри / рестарт рівня з життям / тіло стає їжею для інших.

## Цікавинки для курсу
- Тіло як `deque`: push голови, pop хвоста, без pop при рості — 🥉: класичне завдання на структуру даних, картка `body-queue` + `std-collections`.
- Заборона розвороту на 180° і буфер вводу (два натискання за один тік) — 📎: дрібниця, яку всі ламають.
- Спавн їжі у вільну клітину, коли змійка займає 90 % поля — 📎: вибір зі списку вільних замість «кидати, доки не влучиш».
- Обгортання як режим (стіна/тор) — 🌱: `wrap` одним прапорцем.
- Бонус-предмет з таймером зникнення і очками за залишок часу — 🌱.
- AI-змійка (BFS до їжі + перевірка, що з цільової клітини видно хвіст) — 🥇: алгоритмічно нетривіально, бо жадібний шлях замикає сам себе.
- Буст за масу з гранулами-слідом (Slither.io) — 🥉: ресурс = довжина, витрата лишає здобич суперникам.

## Мапа на каталог
- Є: `move-auto` (рух сам, ввід змінює напрям) · `body-queue` · `std-collections` (deque) · `spawn-random-cell` · `item-pickup` · `touch-death` · `progress-acceleration` (темп з довжиною) · `impassable-cells` (лабіринти) · `timed-despawn` (бонус-жук) · `event-points` · `score-records` · `sequential-levels` (Nibbles) · `difficulty-levels` · `player-death` · `game-pause` · `ai-opponent` · `swipe-gestures` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+no-reverse-turn` «Заборона розвороту назад» · entities/legality · 🌱 — з буфером вводу.
  - `+wrap-edges` «Тор: вихід за край з протилежного» · entities/move · 🌱 · слот {axes: x|y|both}.
  - `+self-collision` «Зіткнення з власним тілом» · entities/death · 🌱 · слот {result: death|cut_tail|ignore}.
  - `+relative-turn-controls` «Відносне керування ліво/право» · interface/input · 🌱.
  - `+boost-for-mass` «Прискорення за рахунок довжини» · entities/state · 📎 · слот {cost_per_tick}.
  - `+death-drops-loot` «Смерть розсипає здобич» · entities/death · 📎 — тіло → гранули (Slither.io).
  - `+simultaneous-versus` «Двоє на одній клавіатурі одночасно» · game-logic/opponent · 📎 — на відміну від `hot-seat` (по черзі).

## Пропозиції до словників
- `+trigger:self_contact` — голова торкнулась власного тіла; через `contact(head, body)` нечитко, бо `body` — частина тієї ж сутності.
- `+effect:drop` — сутність скидає предмети/гранули на свою клітину чи шлях (буст і смерть у Slither.io; підсилення в Bomberman battle).
- `+effect:boost` — тимчасове прискорення з витратою ресурсу (можна `speed` + `shrink`, але як пара це часта механіка).
- `+card:no-reverse-turn`, `+card:wrap-edges`, `+card:boost-for-mass`, `+card:death-drops-loot` — див. «Мапу на каталог».
- `+feature:maze-select` — вибір макета поля перед грою без «рівнів» (Snake II).
- `+axis:control` — тут три значення в межах одного жанру: `direct` абсолютне, відносне ліво/право, «до курсора» (Slither.io) — варто розрізнити `direct-absolute` / `direct-relative` / `pointer`.

## Джерела
- ⭐ [Wikipedia: Snake (video game genre)](https://en.wikipedia.org/wiki/Snake_(video_game_genre)) — визначення жанру, Blockade, BBC Micro (відносне керування, прискорення), Nibbler, Nibbles, Nokia, Slither.io, Snake.io.
- [Wikipedia: Nibbles](https://en.wikipedia.org/wiki/Nibbles_(video_game)) — цифри 1–9, рівні зі складнішими перешкодами й вищою швидкістю, другий гравець на тій самій клавіатурі, 80×50 у текстовому режимі.
- [Wikipedia: Snake (1998)](https://en.wikipedia.org/wiki/Snake_(1998_video_game)) — Nokia 6110/5110, стіна і тіло вбивають, Snake II на 7110, лінійка наступників з роками.
- [Wikipedia: Blockade](https://en.wikipedia.org/wiki/Blockade_(video_game)) — дуель, слід як стіна, 3–6 зіткнень до кінця гри.
- [Wikipedia: Slither.io](https://en.wikipedia.org/wiki/Slither.io) — буст за масу, гранули, смерть від чужого тіла й межі, топ-10.
- [Slither.io](https://slither.io/) — грати.
- YouTube: пошук «nokia snake II gameplay 3310», «qbasic nibbles gameplay».

## Непевне
- (?) Snake II (Wikipedia називає лише Nokia 7110; 3310 — з памʼяті): обгортання країв у режимі без лабіринту, список лабіринтів, бонус-жуки кожні 5 їж з таймером і очками за швидкість, рівні 1–9, меню Nokia — з памʼяті; Wikipedia про це мовчить.
- (?) Slither.io: мінікарта, свайп-керування Snake Rewind / Snake.io — не перевірено.
- (?) Nibbles: кількість життів (5 у QBasic-версії), імена змійок Sammy/Jake, приріст довжини за цифру — Wikipedia цього не каже.
- (?) Буфер вводу (кілька поворотів за тік) — поведінка залежить від реалізації.
- (?) Slither.io: чи вбиває власне тіло — Wikipedia говорить лише про чуже.
- Виправлено 2026-11-19 (T364, знахідка хвилі 3): Snake Pass не thinky і без сітки.
