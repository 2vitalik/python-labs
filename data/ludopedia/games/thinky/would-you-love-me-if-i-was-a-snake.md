---
title: Would You Love Me If I Was a Snake?
slug: would-you-love-me-if-i-was-a-snake
aka: [This Game Is Full Of Snakes!]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2024
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4284670/Would_You_Love_Me_If_I_Was_a_Snake/", best: true, note: "«Push objects, block lasers, teleport, and bite your tail off»; 150 пазлів; реліз Steam 10.09.2026"}
  - {kind: itch, url: "https://andreaboroni.itch.io/wouldyoulovemeifiwasasnake", note: "лазери, портали, плити, «колекційні предмети, що дають силу вам і обʼєктам»; raylib; ранні коментарі ~2024"}
  - {kind: other, url: "https://andreaboroni.itch.io/wouldyoulovemeifiwasasnake/devlog/1039516/this-game-is-full-of-snakes", note: "devlog 09.2025: переробка, робоча назва «This Game Is Full Of Snakes!», гра стала платною"}
  - {kind: other, url: "https://steamcommunity.com/app/4284670/reviews/?browsefilter=toprated", note: "відгуки: блоки = нерухомі тіла змії, кнопки, ворота, лазери, «синя» механіка, мета-рівні, секретні рівні"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Would+You+Love+Me+If+I+Was+a+Snake+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-4dir, move-by-input, body-queue, keyboard-controls, push-object, multi-cell-size, beam-tracing, teleport-pair, button-toggle, key-and-door, impassable-cells, reach-exit, level-select, world-map, level-unlock, save-progress, settings-window, game-screen, background-music, sound-effects, +bite-tail-into-block, +cut-body, +pressure-plate, +laser-blocking, +power-up-colour-mode, +diagonal-laser, +meta-level-quadrants, +feeder-levels, +secret-levels, +level-preview]
proposes: ["+effect:cut_body", "+cond:held_by", "+window:level-preview", "+feature:secret-levels", "+card:bite-tail-into-block", "+card:feeder-levels"]
author: opus
date: 2026-11-09
---

# Would You Love Me If I Was a Snake? — змійка-сокобан: відкуси собі хвіст, і відрізаний шматок стане блоком, яким закриваєш лазери й тиснеш кнопки

## Суть
Покрокова головоломка Andrea Boroni Grazioli (raylib; спершу безкоштовно на itch близько 2024, перероблена й платна в Steam 2026). Гравець — змійка в кімнаті-рівні: голова ходить по клітинах, тіло тягнеться слідом; треба вийти через двері. Головна механіка — **відкусити власний хвіст**: відрізана частина лишається на полі нерухомим блоком тієї ж форми, який можна штовхати, ставити на кнопки й під лазери. Навколо — кнопки з дротами до дверей, лазери з випромінювачами-трикутниками, парні портали і «сині» підсилювачі, що змінюють поведінку змії, блоків і лазерів. 150 рукотворних пазлів, «кожен — окрема ідея».

## Поле і час
- Квадратна сітка; рівень — одна кімната з неправильними стінами; деякі рівні — склеєні з кількох кімнат (мета-рівні).
- Хід = один крок голови; тіло — черга клітин; часу нема (Steam: «Playable without Timed Input»).
- Шари: стіни й підлога · кнопки й портали на підлозі · змія, блоки, кулі · промені лазерів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Змія | player | довжина = кількість сегментів | голова — крок у 4 напрями; тіло повторює шлях; штовхає обʼєкти |
| Блок-тіло | object | форма відрізаного шматка (кілька клітин) | нерухоме «мертве» тіло змії; штовхається як ціле; тисне кнопки, закриває лазери |
| Куля (зелений восьмикутник) | object | — | штовхається; кладеться на кнопку (?) |
| Кнопка (жовтий квадрат) | switch | дріт до цілі | натиснута, поки на ній тіло змії, блок або куля; відкриває двері / вмикає лазери (?) |
| Двері-вихід (жовта смуга в стіні) | gate | звʼязані кнопки | відкриті, коли натиснуто всі свої кнопки; крізь них змія залишає кімнату |
| Випромінювач лазера (трикутник) | hazard | напрям; «важкий» | б'є променем до перешкоди; звичайна змія його не зрушить |
| Лазерний промінь | hazard | вмикається кнопкою в частині рівнів | змія чи блок на шляху його перекриває; дотик голови — (?) |
| Портал (пара клітин з хрестиком одного кольору) | terrain | пара | змія входить в один — виходить з другого, тіло тягнеться крізь пару |
| Синій підсилювач (квадратний предмет) | pickup | — | робить змію / блоки синіми |
| Синя змія / синій блок | object | — | може «відрізати» інше; штовхає випромінювачі |
| Синій лазер | hazard | — | бʼє по діагоналі назад |
| Золоте кільце | static | — | біля проходів у стінах; призначення не встановлено (?) |
| Стіна | static | — | непрохідна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(head+dir)` → ТО `move(head, dir)`, тіло `custom: «кожен сегмент на місце попереднього»`.
- КОЛИ `contact(head, block|ball)` → ЯКЩО `custom: «увесь ланцюг обʼєктів може зсунутися на 1»` → ТО `push`; інакше `block`.
- КОЛИ `contact(head, emitter)` → ЯКЩО `not state(snake, blue)` → ТО `block` — випромінювач «заважкий»; синя змія його штовхає.
- КОЛИ `custom: «змія кусає свій хвіст»` → ТО `custom: «сегменти за місцем укусу відокремлюються»` (`+effect:cut_body`), `transform(cut_segments, block)` — змія коротшає, на полі новий блок її форми.
- КОЛИ `enter(snake_part|block|ball, button)` → ТО `set_state(button, pressed)`; КОЛИ `leave` → `clear_state(button, pressed)`.
- КОЛИ `custom: «усі кнопки дроту натиснуті»` (`+cond:held_by`) → ТО `set_state(door, open)`; інакше `set_state(door, closed)`; так само кнопки перемикають лазери.
- КОЛИ `tick` → ТО `custom: «промінь іде від випромінювача до першої перешкоди; змія, блок або куля його перекривають»`; синій промінь — по діагоналі назад.
- КОЛИ `custom: «промінь влучає в змію»` → ТО `custom: «наслідок не встановлено — смерть або розріз»` (?).
- КОЛИ `enter(head, portal)` → ЯКЩО `free(pair_exit)` → ТО `teleport(head, pair)`, тіло продовжується з виходу.
- КОЛИ `contact(snake, blue_powerup)` → ТО `pickup`, `set_state(snake, blue)`; синя змія чи синій блок `custom: «відрізає інші тіла й обʼєкти»` (?).
- КОЛИ `reach(head, door)` → ЯКЩО `state(door, open)` → ТО `custom: «змія виповзає з кімнати»`, `win`, `next_level`.
- Мета-рівні: `custom: «рівень із 4 квадрантів, кожен — окремий пазл, і зведений рівень з усіх»`; фінальний рівень бере розвʼязки 5 рівнів-«постачальників».

## Керування і ввід
- Клавіатура (стрілки / WASD (?)), миша на мапі рівнів, геймпади Xbox і PlayStation (повна підтримка); «Keyboard Only Option».
- Мапа рівнів: H — сховати превʼю, Enter — перейти на рівень, O — налаштування (скриншот і відгук).
- Undo і рестарт — (?) не підтверджено джерелами.

## Вікна, меню, HUD
- `world-map` / `level-select`: кольорові зони-області (Storm, Beach, Volcano, синя зона тощо), вузли-рівні з номерами, звʼязані лініями; зірки на вузлах-мета-рівнях; замки; літерні вузли A1, B1, C1… (секретні гілки); праворуч унизу — живе превʼю рівня (`+window:level-preview`).
- `game-screen`: лише кімната на тлі з візерунком зони; дроти від кнопок до дверей видно на полі; HUD майже нема.
- `settings-window` (клавіша O), регулювання гучності.
- Анімації «усі рівні пройдено» і «секретні рівні відкрито», окремий рівень-титри з музикою.

## Фічі поза полем
- `world-map` з нелінійним відкриттям (відгук: «non-linear but not TOO non-linear» — застряг — граєш інше).
- `+feature:secret-levels` — додаткові рівні після основних; досягнення Steam.
- Динамічна музика Grzegorz Bednorz (композитор Taiji): шари реагують на події (двері, лазери, зони).
- `autosave` («Save Anytime»); хмарного сейву на старті не було (тред).

## Варіації й родичі
- Безкоштовна itch-версія (≈2024) → переробка 2025 під робочою назвою «This Game Is Full Of Snakes!» → Steam-реліз 2026 зі старою назвою.
- `games/thinky/snakebird.md` — змійка з гравітацією й ростом від фруктів; тут гравітації нема, довжина лише зменшується.
- `games/thinky/woim.md` — черв'як, що розрізає себе навпіл, щоб мати помічника; тут відрізане стає мертвим блоком.
- `games/maze-arcade/snake.md` — класика, де укус себе = смерть; `games/thinky/the-snake-that-eats-puzzle-game-mechanics.md`.
- **Осі варіацій:** що буває при укусі себе — смерть / обрізання хвоста / відрізане стає блоком (тут) / стає другим героєм (WOIM); довжина — росте / фіксована / лише зменшується (тут).

## Цікавинки для курсу
- Укус хвоста: розрізати чергу тіла й перетворити хвіст на багатоклітинний блок — 🥉.
- Поштовх багатоклітинного блоку довільної форми ланцюгом — 🥉.
- Промінь лазера до першої перешкоди з перекриттям тілом — 📎; діагональний синій промінь — 📎.
- Кнопки з дротами: двері відкриті, поки натиснуто всі — 📎.
- Портал, крізь який тягнеться тіло змії (тіло в двох місцях одночасно) — 🥈.
- Мета-рівень, що бере стани розвʼязку з інших рівнів — 🥇.

## Мапа на каталог
- Є: `move-4dir`, `move-by-input`, `body-queue`, `keyboard-controls`; `push-object` + `multi-cell-size` ↔ блоки-тіла; `beam-tracing` ↔ лазери; `teleport-pair` ↔ портали; `button-toggle` + `key-and-door` ↔ кнопки й двері; `impassable-cells`; `reach-exit`; `level-select`, `world-map`, `level-unlock`, `save-progress`; `settings-window`, `game-screen`; `background-music`, `sound-effects`.
- **Нема** → пропозиції карток:
  - `+bite-tail-into-block` «Укус себе відрізає хвіст, і він стає блоком» · entities/interact · 🥉.
  - `+cut-body` «Розрізати тіло-чергу» · entities/move · 📎 (як у WOIM).
  - `+pressure-plate` «Плита натиснута, поки на ній щось лежить» · entities/interact · 🌱.
  - `+laser-blocking` «Тіло чи блок перекриває промінь» · entities/combat · 📎.
  - `+power-up-colour-mode` «Предмет переводить гравця й обʼєкти в інший режим правил» · entities/state · 📎.
  - `+diagonal-laser` «Промінь по діагоналі» · entities/combat · 🌱.
  - `+meta-level-quadrants` «Рівень, складений з окремих пазлів-квадрантів» · levels/progression · 🥉.
  - `+feeder-levels` «Розвʼязки рівнів-постачальників стають входом фінального» · levels/progression · 🥇.
  - `+secret-levels` «Приховані рівні на мапі» · levels/progression · 🌱.
  - `+level-preview` «Живе превʼю рівня на мапі» · interface/menus · 📎.

## Пропозиції до словників
- `+effect:cut_body(a, at)` — розрізати тіло-чергу в точці; відрізане стає окремою сутністю (тут — блоком).
- `+cond:held_by(switch, kind)` — плита натиснута, поки на ній лежить сутність виду.
- `+window:level-preview` — живе превʼю рівня при наведенні на мапі.
- `+feature:secret-levels` — приховані рівні, що відкриваються після основних.
- `+card:bite-tail-into-block`, `+card:feeder-levels` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/4284670/Would_You_Love_Me_If_I_Was_a_Snake/) — «Push objects, block lasers, teleport, and bite your tail off»; 150 пазлів; Windows; повна підтримка геймпада; 10.09.2026; новини оновлень (зони Storm, Beach, Volcano, жовті двері, перемикані лазери, секретні рівні, рівень-титри).
- [itch.io](https://andreaboroni.itch.io/wouldyoulovemeifiwasasnake) — опис (лазери, портали, плити, колекційні підсилювачі), raylib, вводи; коментарі гравців.
- [Devlog «This Game Is Full Of Snakes!»](https://andreaboroni.itch.io/wouldyoulovemeifiwasasnake/devlog/1039516/this-game-is-full-of-snakes) — переробка, раніше гра була безкоштовною.
- [Відгуки Steam](https://steamcommunity.com/app/4284670/reviews/?browsefilter=toprated) — «Pushable blocks… are just inert snake bodies», «cut yourself off to build certain blocks», синя механіка, мета-рівні з 4 квадрантів і 5 «feeder»-рівнів, секретні рівні, O — налаштування.
- Steam-обговорення (рівень 8 демо; краш у «blue area with the square power up thingies») і 7 скриншотів Steam — кнопки, кулі, двері, портали, лазери, мапа.

## Непевне
- (?) Як саме відкушується хвіст (голова входить у власне тіло чи окрема дія) — джерела кажуть лише «bite your tail off».
- (?) Що робить промінь зі змією — смерть, розріз чи лише блокування.
- (?) Роль зелених куль і золотих кілець — з скриншотів і згадки «3 balls» у треді.
- (?) Undo/рестарт і точні клавіші руху не знайдено в джерелах (для такого жанру майже напевно є).
- (?) Рік: itch-версія з коментарями «2 years ago» (≈2024), Steam — 2026.
