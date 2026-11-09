---
title: ZZT
slug: zzt
aka: [Super ZZT, ZZT-OOP]
family: maze-arcade
also: [push-slide]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 1991
platforms: [DOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/ZZT", note: "історія, світи й дошки, редактор, ZZT-OOP, Super ZZT"}
  - {kind: fandom, url: "https://wiki.zzt.org/wiki/Elements", best: true, note: "ZZT Wiki: усі елементи з параметрами й точною поведінкою, мова ZZT-OOP"}
  - {kind: fandom, url: "https://wiki.zzt.org/wiki/ZZT-OOP", note: "префікси, команди, вбудовані повідомлення, умови, напрямки"}
  - {kind: other, url: "https://museumofzzt.com/", note: "Museum of ZZT — архів тисяч світів спільноти, грати в браузері"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=zzt+tim+sweeney+gameplay", note: "пошук; геймплей і редактор"}
stage: v1
coverage: 70
mechanics: [move-4dir, move-by-input, projectile-shot, shoot-forward, projectile-collision, hp-damage, item-pickup, inventory, key-and-door, destructible-blocks, impassable-cells, push-object, teleport-one-way, teleport-pair, random-walk, chase-player, body-queue, temporary-modes, bomb-fuse, explode-area, mirror-reflect, blob-growth, fog-of-war, time-out, in-game-editor, editor-palette, level-exchange, command-program, sensor-predicates, save-game, game-pause, console-render, status-panel, +object-scripting, +message-passing-objects, +board-edge-links, +duplicator-clone, +rotating-conveyor, +ejection-ray, +axis-aligned-shooter, +shared-global-flags, +hyperlink-text-window]
proposes: ["+trigger:message", "+trigger:aligned", "+effect:send", "+effect:eject", "+effect:duplicate", "+effect:goto_label", "+role:scripted", "+window:scroll-window", "+feature:world-editor", "+card:object-scripting", "+card:message-passing-objects"]
author: opus
date: 2026-11-09
---

# ZZT — ASCII-пригодницька аркада з дошками-екранами, де будь-який обʼєкт можна запрограмувати мовою ZZT-OOP

## Суть
Білий смайлик на синьому фоні бігає дошками (екранами) світу: стріляє в левів і тигрів, збирає боєприпаси, самоцвіти, смолоскипи, ключі й штовхає валуни. Ядро — набір ~45 вбудованих елементів з чіткою поведінкою (див. таблицю) плюс **Object** — елемент з власною програмою на ZZT-OOP, який реагує на дотик, постріл, вибух і повідомлення інших обʼєктів. Гра постачалась з редактором світу, тому корпус ZZT — це тисячі авторських світів: від шутерів до головоломок і текстових історій.

## Поле і час
- Світ = набір дошок (boards); дошка — сітка клітин тексту, суміжні дошки звʼязані краями (вийшов за край — перейшов на сусідню) або пасажами.
- Відображення: 255 символів IBM PC, 16 кольорів (у редакторі — 7 для кольорових обʼєктів); праворуч — бічна панель.
- Real-time: кожен елемент зі «статами» ходить зі своїм `cycle` (раз на N тіків); гравець — по натисканню.
- Налаштування дошки: темрява (видно лише навколо смолоскипа), ліміт часу, максимум куль на екрані, «повернення на старт при ураженні».
- Super ZZT (1991): більші дошки з прокруткою, нові елементи.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (смайлик) | player | здоровʼя, патрони, смолоскипи, самоцвіти, ключі, очки | рух 4 напрямки, постріл, смолоскип |
| Лев | enemy | інтелект (шанс іти до гравця 10–90 %) | інакше випадковий крок; дотик — шкода гравцю, лев гине |
| Тигр | enemy | інтелект, частота стрільби, кулі/зірки | рухається як лев; стріляє, коли гравець на лінії ±2 клітини |
| Ведмідь | enemy | чутливість | детермінований: іде до гравця, коли той на одній осі; −10 здоровʼя; ламка стіна знищує обох |
| Розбійник (ruffian) | enemy | інтелект, час відпочинку | чергує «стоїть / летить по прямій»; на одній лінії може повернути до гравця |
| Голова сороконіжки | enemy | інтелект, відхилення | веде ланцюг сегментів; упершись — бік або розворот |
| Сегмент | enemy | лідер/послідовник | іде в клітину, де була попередня частина |
| Акула | enemy | інтелект | ходить лише по воді, як лев; кусає гравця поруч; невразлива для куль і бомб |
| Слиз (slime) | enemy | поріг клонування | розмножується в 4 сусідні порожні, лишає за собою ламку стіну свого кольору; дотик гравця → ламка стіна |
| Обертова гармата | enemy | інтелект, частота, кулі/зірки | непрохідна, невразлива; стріляє в гравця на лінії ±2 або у випадковий бік |
| Штовхач (pusher) | object | напрямок | їде у своєму напрямку, штовхаючи все штовхоме, доки не впреться |
| Обʼєкт (Object) | object | символ, колір, програма ZZT-OOP | робить те, що написано: ходить, говорить, стріляє, змінює дошку |
| Куля | projectile | чия | летить прямо; шкодить гравцю або вбиває істоту; розбиває ламкі стіни |
| Зірка | projectile | — | кинута тигром/гарматою, повзе за гравцем, з часом зникає |
| Патрони | pickup | — | + патрони |
| Смолоскип | pickup | 200 тіків горіння | + смолоскип; T на темній дошці — світло радіусом ~7×4 |
| Самоцвіт | pickup | — | + самоцвіт (валюта) і + здоровʼя |
| Ключ ×кольори | pickup | колір | відкриває двері того ж кольору |
| Енерджайзер | pickup | 75 тіків | невразливість (крім бомб), дотик вбиває ворогів, вороги тікають |
| Сувій (scroll) | pickup | текст / ZZT-OOP | показує текст і зникає; може виконати одно-тікові команди |
| Двері | gate | колір | пропускає з ключем того ж кольору |
| Пасаж (passage) | gate | цільова дошка, колір | переносить на іншу дошку, на пасаж того самого кольору |
| Бомба | object | відлік 9→1 | дотик запалює; вибух ~15×9: −10 здоровʼя, нищить істот, ламкі стіни, самоцвіти |
| Дублікатор | spawner | напрямок, швидкість | копіює елемент з одного боку на інший (з програмою); штовхає те, що заважає |
| Конвеєр за / проти год. | terrain | напрям обертання | обертає штовхомі елементи у 8 сусідніх клітинах по колу |
| Транспортер | terrain | напрямок | пропускає, якщо рух у його напрямку; виводить за протилежний бік або до зустрічного транспортера на лінії |
| Валун | object | — | штовхається в будь-який бік |
| Слайдер NS / EW | object | вісь | штовхається лише вздовж своєї осі |
| Вода | terrain | — | непрохідна для гравця, кулі летять над нею |
| Ліс | terrain | — | прохідний, гравець вирубує його кроком |
| Стіна суцільна / звичайна / лінія | static | — | непрохідна |
| Ламка стіна (breakable) | static | — | руйнується кулею чи вибухом |
| Фальшива стіна (fake) | terrain | — | виглядає як стіна, прохідна |
| Невидима стіна | static | — | непрохідна, проявляється при дотику |
| Мерехтлива стіна (blink wall) | hazard | старт, період, напрям | періодично випускає промінь до перешкоди; промінь виштовхує гравця вбік або вбиває |
| Рикошет | static | — | відбиває кулі |
| Текст | static | колір | непрохідний текст на дошці |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(player, dir)`; ЯКЩО `occupied(cell_ahead, pushable)` → ТО `push`.
- КОЛИ `input(shoot_dir)` → ЯКЩО `counter(ammo, >, 0) and count(player_bullets, <, board_max)` → ТО `spawn(bullet)`, `counter(ammo, −1)`.
- КОЛИ `contact(bullet, creature)` → ТО `disappear_both`, `score(1|2)`; КОЛИ `contact(bullet, breakable)` → ТО `disappear_both`; КОЛИ `contact(bullet, ricochet)` → ТО `bounce(bullet)`.
- КОЛИ `contact(enemy, player)` → ЯКЩО `state(player, energized)` → ТО `disappear(enemy)`; інакше `damage(player, n)`, `disappear(enemy)`.
- КОЛИ `contact(player, gem|ammo|torch|key)` → ТО `pickup`; самоцвіт — `heal(player, n)`.
- КОЛИ `contact(player, door[c])` → ЯКЩО `has(player, key[c])` → ТО `take(player, key[c])`, `disappear_b`; інакше `block`.
- КОЛИ `contact(player, energizer)` → ТО `set_state(player, energized, 75)`, `custom: «надіслати energize усім обʼєктам»`; поки стан — вороги-переслідувачі тікають.
- КОЛИ `contact(player, bomb)` → ТО `set_state(bomb, lit)`; КОЛИ `timer(bomb_countdown)` → `explode(area, breakable→empty)`, `damage(player, 10)` у радіусі, `custom: «обʼєктам у радіусі — повідомлення bombed»`.
- КОЛИ `input(torch)` → ЯКЩО `state(board, dark) and has(player, torch)` → ТО `take(player, torch)`, `reveal(radius)` на 200 тіків.
- КОЛИ `contact(player, passage)` → ТО `teleport(player, matching_passage_on_target_board)`.
- КОЛИ `edge(player)` → ТО `custom: «перейти на сусідню дошку з того боку»`.
- КОЛИ `contact(a, transporter)` → ЯКЩО `moving(a, transporter_dir)` → ТО `teleport(a, opposite_side | facing_transporter)`.
- КОЛИ `timer(duplicator)` → ТО `custom: «копія елемента зі сторони-джерела зʼявляється з протилежного боку»` (`+effect:duplicate`).
- КОЛИ `timer(conveyor)` → ТО `rotate(neighbours, ±45)` — обертання по колу штовхомих сусідів.
- КОЛИ `timer(blink_wall)` → ТО `spawn(ray)` до першої перешкоди / `disappear(ray)`; КОЛИ `contact(ray, player)` → ТО `custom: «виштовхнути вбік; нема куди — смерть»` (`+effect:eject`).
- КОЛИ `timer(slime)` → ТО `spawn(slime)` у вільні сусідні, `transform(slime → breakable)`.
- КОЛИ `contact(player, slime)` → ТО `transform(slime → breakable)`.
- КОЛИ `line_of_sight(tiger|spinning_gun, player)` → ЯКЩО `prob(rate)` → ТО `spawn(bullet|star)` у бік гравця.
- КОЛИ `timer(lion)` → ЯКЩО `prob(intelligence)` → ТО `move(lion, toward_player)`; інакше `move(lion, rnd)`.
- КОЛИ `blocked(centipede_head)` → ТО `face(head, perpendicular)`, потім `face(head, reverse)`; сегменти — `move` у місце попередника.
- КОЛИ `counter(time_left, ==, 0)` → ЯКЩО `custom: «на дошці задано ліміт часу»` → ТО `custom: «наслідок вичерпаного часу (?)»`.
- КОЛИ `hp_zero(player)` → ТО `game_over`.
- ZZT-OOP: КОЛИ `contact(player, object)` → ТО `custom: «стрибок на мітку :touch»`; аналогічно `:shot`, `:bombed`, `:thud` (обʼєкт упʼявся), `:energize`.
- ZZT-OOP: КОЛИ `custom: «#send obj:label»` → ТО `custom: «обʼєкт obj стрибає на мітку label»` (`+trigger:message`, `+effect:send`).
- ZZT-OOP: КОЛИ `custom: «#if alligned|contact|blocked dir|energized|any element|flag»` → ТО `custom: «перейти на мітку»`; `#set`/`#clear` — 10 спільних для світу прапорців.
- ZZT-OOP ефекти: `#go/#walk dir` (`move`), `#shoot`, `#throwstar` (`spawn`), `#put dir element` (`spawn_at`), `#change A B` (`transform`), `#become` (`transform` себе), `#give/#take` (`counter`), `#zap/#restore label`, `#lock/#unlock`, `#die` (`disappear`), `#endgame`, `#play` (`sound`), текст (`message` у вікні з пунктами-гіперпосиланнями `!label;текст`).
- Перемога: визначає автор світу (зазвичай фінальний обʼєкт / прапорець і `#endgame`, або просто кінець історії). Поразка: здоровʼя = 0. Рахунок: очки за знищених істот і за `#give score`.

## Керування і ввід
- Стрілки — рух; Shift+стрілки — постріл у той бік (?); T — смолоскип; S — зберегти; P — пауза; B — звук; H — довідка; Q — вихід (?).
- Текст обʼєкта/сувою — вікно-прокрутка, стрілками вибирається пункт-гіперпосилання, Enter виконує мітку.
- Редактор: курсор по дошці, вибір елемента за категоріями, колір, «малювання», налаштування дошки, звʼязки країв.

## Вікна, меню, HUD
- `main-menu` (титульна дошка-«монітор»): Play, Restore game, Load world, About, High scores, Board editor (?) — команди в бічній панелі.
- `custom-window` вибір світу — список *.ZZT (Town, Caves, Dungeons, City, Tour, Demo).
- `game-screen` — дошка + бічна панель (`status-panel`): `hp-bar` (Health), Ammo, Torches (+шкала горіння), Gems, `score`, ключі кольорами, список клавіш.
- `+window:scroll-window` — модальне вікно тексту сувою/обʼєкта з гіперпосиланнями.
- `+ui:message-line` (з `kroz.md`) — однорядкове повідомлення внизу дошки («Energizer - You are invincible»).
- `save-slots` — ввести імʼя файла збереження; `pause-menu` — «Pausing…».
- `leaderboard` — рекорди світу (?).
- `editor-window` — редактор: дошка, палітра елементів (Items / Creatures / Terrain), колір, Board info (темрява, час, макс. куль, вихід за краї), World info (прапорці, ключі гравця), транзит між дошками.
- Переходи: main-menu → вибір світу → game-screen; торкнувся обʼєкта → scroll-window → назад; здоровʼя 0 → «Game over» → рекорди → main-menu.

## Фічі поза полем
- `level-editor` → `+feature:world-editor` — повний редактор світу в коробці, плюс мова сценаріїв для поведінки й діалогів.
- `level-sharing` — світи як файли .ZZT: BBS-обмін, конкурси, понад 3000 світів (архів Museum of ZZT).
- `save-slots` будь-коли (головний засіб проти «пастки» в пазлах — повернутись до старого сейву).
- `sound-toggle` — PC-speaker, ноти й ударні через `#play`.
- Super ZZT — прихований редактор (через це менше спільноти).

## Варіації й родичі
- Super ZZT (1991): більші дошки з прокруткою, нові вороги й обʼєкти; спільнотні порти й клони (Zeta, MegaZeux — нащадок з розширеною мовою).
- Родичі в корпусі: `kroz` (ASCII-підземелля Apogee, без редактора й скриптів), `chips-challenge` (набір вбудованих клітин), `sokoban` / `kwirk` (валуни, слайдери — пазл-дошки), `gauntlet` (дублікатори як «генератори»).
- **Осі варіацій:** поведінка (лише вбудовані елементи / вбудовані + скрипт-обʼєкти); звʼязок дошок (краї / пасажі / обидва); видимість (світла / темна дошка зі смолоскипом); ворог «впершись» — бік або розворот (сороконіжка), стоп (розбійник).

## Цікавинки для курсу
- Обʼєкт зі скриптом: мітки, вбудовані повідомлення `touch/shot/bombed/thud`, `#send` між обʼєктами — 🥇 (маленький інтерпретатор подій усередині гри).
- Дублікатор, що копіює сусіда разом зі станом і програмою — 🥉.
- Конвеєр, що обертає 8 сусідів по колу — 📎.
- Мерехтлива стіна з променем і виштовхуванням гравця — 📎.
- Слиз, що росте і лишає ламку стіну — 📎 (клітинний автомат на одному правилі).
- Сороконіжка: голова + сегменти як черга, розворот голови — 🥉.
- Транспортер з пошуком зустрічного по лінії — 📎.
- Темна дошка + смолоскип з радіусом і таймером — 📎.

## Мапа на каталог
- Є: `move-4dir` · `projectile-shot` + `shoot-forward` + `projectile-collision` · `hp-damage` · `item-pickup` · `inventory` · `key-and-door` · `destructible-blocks` · `impassable-cells` · `push-object` (валуни, слайдери, штовхачі) · `teleport-one-way` (транспортер) · `teleport-pair` (пасажі) · `random-walk` + `chase-player` (лев, ведмідь) · `body-queue` (сороконіжка) · `temporary-modes` (енерджайзер) · `bomb-fuse` + `explode-area` · `mirror-reflect` (рикошет) · `blob-growth` (слиз) · `fog-of-war` (темні дошки) · `time-out` · `in-game-editor` + `editor-palette` · `level-exchange` · `command-program` + `sensor-predicates` (ZZT-OOP) · `save-game` · `game-pause` · `console-render` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+object-scripting` «Обʼєкт з власною програмою подій» · game-logic/program · 🥇 · слоти {labels, commands}.
  - `+message-passing-objects` «Обʼєкти шлють повідомлення один одному» · game-logic/program · 🥈.
  - `+board-edge-links` «Вихід за край → сусідній екран» · levels/progression · 🌱.
  - `+duplicator-clone` «Дублікатор копіює сусіда» · entities/spawn · 🥉.
  - `+rotating-conveyor` «Конвеєр обертає сусідів по колу» · entities/move · 📎.
  - `+ejection-ray` «Промінь виштовхує гравця» · entities/interact · 📎.
  - `+axis-aligned-shooter` «Стріляє, коли гравець майже на лінії» · entities/combat · 🌱 · слот {tolerance}.
  - `+shared-global-flags` «Прапорці, спільні для всіх рівнів» · game-logic/save · 🌱 · слот {n}.
  - `+hyperlink-text-window` «Текст з пунктами вибору» · interface/menus · 📎.

## Пропозиції до словників
- `+trigger:message` — сутність отримала повідомлення (мітку) від іншої або від рушія (touch, shot, bombed, thud, energize).
- `+trigger:aligned` — гравець на одній горизонталі/вертикалі з сутністю (ZZT `alligned`, тигр, ведмідь).
- `+effect:send` — надіслати повідомлення іншій сутності; `+effect:goto_label` — перейти на мітку власної програми.
- `+effect:eject` — виштовхнути сутність у сусідню вільну клітину (blink wall).
- `+effect:duplicate` — копія сутності разом зі станом (дублікатор).
- `+role:scripted` — сутність, поведінку якої задає програма автора (Object).
- `+window:scroll-window` — модальне вікно тексту з гіперпосиланнями.
- `+feature:world-editor` — редактор світу з мовою поведінки обʼєктів.
- `+card:object-scripting`, `+card:message-passing-objects` — див. вище.

## Джерела
- ⭐ [ZZT Wiki: Elements](https://wiki.zzt.org/wiki/Elements) — категорії елементів; сторінки Lion, Tiger, Bear, Ruffian, Head, Shark, Slime, Spinning gun, Pusher, Duplicator, Transporter, Conveyor, Blink wall, Bomb, Energizer, Torch, Passage — параметри й формули.
- [ZZT Wiki: ZZT-OOP](https://wiki.zzt.org/wiki/ZZT-OOP) — префікси, команди, вбудовані повідомлення, умови.
- [Wikipedia: ZZT](https://en.wikipedia.org/wiki/ZZT) — світи, дошки, предмети, редактор, 10 прапорців, Super ZZT.
- [Museum of ZZT](https://museumofzzt.com/) — архів світів спільноти.
- YouTube: пошук «zzt tim sweeney gameplay».

## Непевне
- (?) Розмір дошки (60×25 у ZZT) і стартове здоровʼя (100) — з памʼяті, у відкритих сторінках не бачив.
- (?) Клавіші: Shift+стрілки для пострілу, S/P/B/H/Q — з памʼяті.
- (?) Скільки шкоди завдають лев/тигр/куля (бачив лише −10 від ведмедя й бомби).
- (?) Що відбувається, коли вичерпано ліміт часу дошки.
- (?) Чи є таблиця рекордів на кожен світ і пункти головного меню дослівно.
- (?) Скільки кольорів ключів і чи можна носити кілька ключів одного кольору.
