---
title: Google Snake (Змійка в пошуку Google)
slug: google-snake
aka: [Google Snake Game, Play Snake, Snake Game Google]
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
year: null
platforms: [web, mobile]
links:
  - {kind: other, url: "https://snakegame.net/how-to-play-google-snake", best: true, note: "фан-гайд: опис кожного режиму (Wall, Portal, Cheese, No Borders, Twin, Winged, Yin Yang, Key, Sokoban, Poison, Dimension, Minesweeper, Statue, Light, Peace, Blender), розміри поля, швидкості, клавіші"}
  - {kind: other, url: "https://www.tycoonstory.com/snake-google-game/", note: "налаштування: кількість яблук 1/3/5/10/Dice/Bomb/Tally, цілі 25/50/100/All, повний список режимів зі Shield/Arrow/Hotdog/Magnet/Gate/Bridge"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/List_of_Google_Easter_eggs", note: "пошук «snake» / «play snake» → картка гри; шестірня — налаштування і режим; гра регулярно оновлюється"}
  - {kind: other, url: "https://uk.news.yahoo.com/googles-snake-game-daily-challenge-170139115.html", note: "щоденний челендж: тісне поле з перешкодами, дивні хвости"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Google+Snake+modes", note: "пошук; режими"}
stage: v1
coverage: 65
mechanics: [move-auto, body-queue, self-collision, touch-death, player-death, spawn-random-cell, item-pickup, impassable-cells, wrap-edges, teleport-pair, push-object, key-and-door, hidden-under-block, random-walk, fog-of-war, collect-quota, collect-all, rule-variants, field-size-picker, game-settings, settings-window, game-screen, end-screen, score-records, daily-puzzle, keyboard-controls, swipe-gestures, +eat-spawns-wall, +body-gaps-passable, +head-tail-swap, +moving-food, +mirrored-second-move, +crate-target-opens, +poison-random-steer, +dimension-phase, +mine-radius-countdown, +body-to-wall, +light-radius-pulse]
proposes: ["+card:head-tail-swap", "+card:mine-radius-countdown", "+card:body-to-wall", "+card:dimension-phase", "+card:crate-target-opens", "+card:eat-spawns-wall"]
author: opus
date: 2026-11-09
---

# Google Snake — класична змійка, до якої можна підмішати десятки модифікаторів правил одночасно

## Суть
Змійка з пошуку Google (запит «snake» / «play snake»): голова йде сама, яблуко подовжує тіло, удар у стіну чи в себе — кінець. Ядро — у `snake`; цей файл описує, чим Google Snake незвичайна: **режими-модифікатори**, кожен з яких змінює одне правило (що стається після їжі, що робить край, як поводиться тіло), і режим **Blender**, що вмикає кілька модифікаторів разом. Це готовий конструктор варіантів правил: та сама петля «тік → крок → зіткнення → їжа» з набором хуків.

## Поле і час
- Квадратна сітка трьох розмірів: Small 10×9, Regular 17×15, Big 24×21. Край — стіна (Classic) або обгортка (No Borders, Peace).
- Real-time, тік = крок голови; швидкість — налаштування: Snake (звичайна), Rabbit (утричі швидше), Turtle (утричі повільніше).
- Кількість яблук на полі — налаштування (1 / 3 / 5 / 10 / Dice / Bomb / Tally); ціль — 25 / 50 / 100 / усі яблука (87 / 252 / 501 для трьох розмірів).
- Dimension додає другий «вимір» тих самих клітин — два шари предметів; Light ховає поле в темряві, крім кола довкола голови.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Голова змійки | player | напрям, швидкість | щотік крок; зіткнення з тілом/краєм — кінець (Classic) |
| Тіло | object | довжина | черга сегментів; Cheese — частина сегментів невидима й прохідна |
| Яблуко / фрукт | pickup | — | +1 довжина, нове зʼявляється у вільній клітині |
| Стіна (Wall) | static | — | зʼявляється після кожної їжі; дотик — кінець |
| Яблуко-портал (Portal) | pickup | пара | зʼївши одне, голова виходить з іншого |
| Летюче яблуко (Winged) | pickup | напрям | рухається полем, відбивається від країв і тіла |
| Друга змійка (Yin Yang) | player | протилежний колір | рухається дзеркально до першої; зіткнення — кінець |
| Ключ і замок (Key) | pickup / gate | — | ключ знімає замок і відкриває сховані за ним предмети; удар у замок — кінець |
| Ящик (Sokoban) | object | ціль | штовхається; на цільовій клітині відкривається — всередині предмет |
| Отруйний фрукт (Poison) | hazard | сірий | змійка коротко рухається випадково |
| Міна (Minesweeper) | hazard | радіус | зʼявляється після їжі; вхід у радіус запускає відлік; центр — миттєва смерть |
| Статуя (Statue) | static | — | після їжі тіло (крім голови) стає непрохідним барʼєром |
| Коло світла (Light) | zone | радіус | видно лише довкола голови; їжа ненадовго розширює коло |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(head, dir)`; тіло — `custom: «сегмент на місце попереднього»`.
- КОЛИ `input(dir)` → ТО `face(head, dir)`.
- КОЛИ `contact(head, apple)` → ТО `disappear(apple)`, `grow(snake, 1)`, `counter(apples, +1)`, `spawn_at(apple, random_free)`.
- КОЛИ `contact(head, body)` → ЯКЩО `not mode(peace)` → ТО `lose`.
- КОЛИ `edge(head)` → ЯКЩО `mode(borderless)` або `mode(peace)` → ТО `wrap(head)`; інакше `lose`.
- КОЛИ `counter(apples, ==, target)` або `custom: «зʼїдено всі можливі яблука»` → ТО `win`.
- Wall: КОЛИ `picked(snake, apple)` → ЯКЩО `mode(wall)` → ТО `spawn_at(wall, random_free)`; КОЛИ `contact(head, wall)` → ТО `lose`.
- Portal: КОЛИ `contact(head, portal_apple)` → ТО `teleport(head, paired_apple)`; КОЛИ `custom: «нова пара порталів не вміщується»` → ТО `game_over`.
- Cheese: КОЛИ `contact(head, body)` → ЯКЩО `state(segment, invisible)` → ТО `custom: «прохід крізь сегмент»`.
- Twin: КОЛИ `picked(snake, apple)` → ЯКЩО `mode(twin)` → ТО `swap(head, tail)`, `face(head, reverse)`.
- Winged: КОЛИ `tick` → ЯКЩО `mode(winged)` → ТО `move(apple, dir)`; КОЛИ `blocked(apple)` → ТО `bounce(apple)` (край і тіло).
- Yin Yang: КОЛИ `input(dir)` → ЯКЩО `mode(yinyang)` → ТО `mirror_input` для другої змійки; КОЛИ `contact(snake, twin_snake)` → ТО `lose`.
- Key: КОЛИ `contact(head, key)` → ТО `disappear(lock)`, `reveal(hidden_items)`; КОЛИ `contact(head, lock)` → ТО `lose`.
- Sokoban: КОЛИ `contact(head, crate)` → ЯКЩО `free(cell_behind)` → ТО `push`; КОЛИ `enter(crate, target)` → ТО `disappear(crate)`, `spawn(apple)`.
- Poison: КОЛИ `contact(head, poison)` → ТО `set_state(snake, poisoned, dur)`; ЯКЩО `state(snake, poisoned)` → `custom: «напрям обирається випадково»`.
- Dimension: КОЛИ `picked(snake, apple)` → ЯКЩО `mode(dimension)` → ТО `set_state(snake, dimension, other)`; КОЛИ `contact(head, item)` → ЯКЩО `not same(snake, item, dimension)` → ТО `custom: «взаємодії нема»`.
- Minesweeper: КОЛИ `picked(snake, apple)` → ТО `spawn_at(mine, random_free)`; КОЛИ `in_range(head, mine, r)` → ТО `timer(start)`; КОЛИ `timer(op, n)` вичерпано → ЯКЩО `in_range(head, mine, r)` → ТО `lose`; КОЛИ `contact(head, mine)` → ТО `lose`.
- Statue: КОЛИ `picked(snake, apple)` → ЯКЩО `mode(statue)` → ТО `transform(body, wall)` (усе, крім голови); КОЛИ `contact(head, wall)` → ТО `lose`.
- Light: КОЛИ `picked(snake, apple)` → ЯКЩО `mode(light)` → ТО `custom: «радіус світла зростає, далі поступово стискається»`; довше тіло — яскравіше світло крізь нього.
- Peace: зіткнень нема — гра закінчується за бажанням гравця або коли зʼїдено все.
- Blender: КОЛИ `level_start` → ТО `custom: «увімкнути всі обрані модифікатори одночасно»`.
- Перемога: зʼїсти ціль (25 / 50 / 100 / усі). · Поразка: зіткнення за правилами режиму. · Рахунок: зʼїдені яблука; найкращий рахунок зберігається для набору налаштувань (?).

## Керування і ввід
- Стрілки або WASD — напрям; на мобільному — свайпи в 4 боки.
- Enter / Space — рестарт після кінця; T — показати час; M — звук.
- Шестірня (вгорі праворуч) — налаштування й режими; у Blender — вибір кількох режимів кліками.

## Вікна, меню, HUD
- `custom-window` — картка «Play Snake» у результатах пошуку Google, «Click to Play».
- `settings-window` (шестірня): сітка іконок режимів, кількість яблук, швидкість, розмір поля; Blender — мультивибір режимів.
- `game-screen` — поле; HUD: `score` (зʼїдені яблука), `hi-score`, `timer-elapsed` (клавіша T).
- `end-screen` — рахунок і рекорд, кнопка «грати ще» (?).
- `daily-window` — щоденний челендж: заданий набір (тісне поле з перешкодами, незвичні хвости).
- Переходи: пошук → картка → game-screen; шестірня → settings-window → game-screen; кінець → end-screen → Enter → game-screen.

## Фічі поза полем
- `custom-rules` — головна фіча: режими-модифікатори + Blender для комбінацій.
- `custom-difficulty`: розмір поля, кількість яблук, швидкість, ціль.
- `daily-puzzle` — щоденний челендж.
- `leaderboard-local` — найкращий рахунок (?).
- `touch-controls` (свайпи) і `mouse-and-keyboard`; `sound-toggle` (M).
- Нема мультиплеєра, undo, редактора.

## Варіації й родичі
- `snake` — базове ядро (черга тіла, самозіткнення, обгортання як варіант).
- `nibbler`, `snake-rattle-n-roll`, `slither-io` — інші відгалуження змійки; `blockade` — тіло-стіна назавжди (тут Statue робить це за подією).
- `snakebird` (thinky) — змійка з гравітацією; тут штовхання ящиків — від `sokoban`; Minesweeper-режим — від `minesweeper`.
- **Осі варіацій «що змінити в змійці»:** наслідок їжі (ріст / стіна / міна / портал / swap голова-хвіст / тіло → статуя / зміна виміру); край (смерть / тор); тіло (смертельне / дірки / прохідне); їжа (стоїть / летить / в ящику / за замком / отруйна); видимість (усе / коло світла); кількість змійок (1 / дзеркальна пара).

## Цікавинки для курсу
- Режими як хуки `on_eat` / `on_edge` / `on_self_hit` над однією петлею + Blender, що компонує кілька хуків, — 🥈 (архітектура модифікаторів).
- Twin: swap голови й хвоста через розворот черги — 🌱.
- Portal: пара яблук-телепортів з перевіркою «чи є місце для нової пари» — 📎.
- Minesweeper: міна з радіусом і відліком, поки голова в радіусі — 📎.
- Yin Yang: дзеркальна друга змійка, керована тим самим вводом — 📎.
- Sokoban: ящик-контейнер, що відкривається на цілі, — 📎.
- Light: туман з радіусом, що пульсує після їжі, — 🌱.
- Dimension: два шари предметів і перемикання шару після їжі — 🥉.

## Мапа на каталог
- Є: `move-auto` + `body-queue` + `self-collision`; `touch-death` + `player-death`; `spawn-random-cell` + `item-pickup`; `impassable-cells` ↔ Wall/Statue; `wrap-edges` ↔ No Borders/Peace; `teleport-pair` ↔ Portal; `push-object` ↔ Sokoban; `key-and-door` + `hidden-under-block` ↔ Key; `random-walk` ↔ Poison; `fog-of-war` ↔ Light; `collect-quota` / `collect-all` ↔ цілі 25…All; `rule-variants` ↔ Blender; `field-size-picker`, `game-settings`, `settings-window`; `daily-puzzle`; `keyboard-controls`, `swipe-gestures`.
- **Нема** → пропозиції карток:
  - `+eat-spawns-wall` «Кожна їжа ставить стіну» · entities/spawn · 🌱.
  - `+body-gaps-passable` «Тіло з прохідними дірками» · entities/legality · 📎.
  - `+head-tail-swap` «Голова й хвіст міняються, рух розвертається» · entities/move · 🌱.
  - `+moving-food` «Їжа рухається і відбивається» · entities/move · 🌱.
  - `+mirrored-second-move` — уже пропонована: друга сутність повторює ввід дзеркально.
  - `+crate-target-opens` «Ящик на цілі відкривається» · entities/interact · 📎.
  - `+poison-random-steer` «Отрута — тимчасовий випадковий напрям» · entities/state · 🌱.
  - `+dimension-phase` «Два шари предметів, сутність у одному з них» · field · 🥉.
  - `+mine-radius-countdown` «Міна з радіусом і відліком» · entities/combat · 📎.
  - `+body-to-wall` «Тіло стає стіною за подією» · entities/state · 🌱.
  - `+light-radius-pulse` «Коло світла довкола аватара, що пульсує від подій» · interface/render · 📎.

## Пропозиції до словників
- `+card:head-tail-swap` — розворот змійки через обмін голови й хвоста.
- `+card:mine-radius-countdown` — небезпечна зона з відліком перебування.
- `+card:body-to-wall` — тіло перетворюється на статичні стіни.
- `+card:dimension-phase` — сутності в одному з двох шарів, взаємодія лише в межах шару.
- `+card:crate-target-opens` — контейнер, що відкривається на цільовій клітині.
- `+card:eat-spawns-wall` — наслідок їжі — нова перешкода.

## Джерела
- ⭐ [snakegame.net: How to play Google Snake](https://snakegame.net/how-to-play-google-snake) — опис 16 режимів і Blender, розміри Small/Regular/Big, швидкості Snake/Rabbit/Turtle, клавіші.
- [Tycoon Story: Snake Google Game](https://www.tycoonstory.com/snake-google-game/) — кількість яблук, цілі й «усі яблука» для розмірів, повний перелік режимів (частина без опису).
- [Wikipedia: List of Google Easter eggs](https://en.wikipedia.org/wiki/List_of_Google_Easter_eggs) — запуск через пошук, шестірня налаштувань, регулярні оновлення.
- [Yahoo / For The Win (2024)](https://uk.news.yahoo.com/googles-snake-game-daily-challenge-170139115.html) — щоденний челендж.
- YouTube: пошук «Google Snake modes».

## Непевне
- (?) Рік запуску гри в пошуку Google — у відкритих джерелах не знайдено (у шапці `year: null`).
- (?) Режими Shield, Arrow, Hotdog, Magnet, Gate, Bridge названі в переліку Tycoon Story, але опису їхньої дії не знайдено; Magnet/Shield з інших змійок (притягує їжу / переживає удар) — не підтверджено для Google.
- (?) Кількість яблук Dice, Bomb, Tally — лише назви з коротким «змінна кількість»; деталі невідомі.
- (?) Назви швидкостей розходяться між джерелами (Snake/Rabbit/Turtle проти Slow/Normal/Fast; ще одне — Cheetah).
- (?) Statue: чи після «застигання» змійка продовжує з самою головою; Dimension: як саме видно другий вимір.
- (?) Чи рекорд зберігається окремо для кожної комбінації налаштувань.
