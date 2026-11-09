---
title: Devil World
slug: devil-world
aka: [デビルワールド]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: collect
year: 1984
platforms: [Famicom/NES (Японія, Європа), Wii/3DS/Wii U Virtual Console, Switch (NSO)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Devil_World", best: true, note: "Деві вказує напрям, міньйони зсувають лабіринт, хрести, Біблії в печатку, бонус-лабіринт"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/デビルワールド", note: "три сцени раунду, Bowa-Bowa, морозиво, вороги Medaman/Bonbon/子デビル, 2P-правила, бонус-скрині"}
  - {kind: official, url: "https://www.nintendo.com/jp/famicom/software/hvc-dd/index.html", note: "Nintendo (Famicom 40th): керування, яйце-старт, стрілки, раунди до 16 (сцена 46)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Devil+World+NES+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-auto, collect-all, touch-death, environment-death, player-death, temporary-modes, projectile-shot, shoot-forward, respawn, telegraphed-intents, time-out, event-points, sequential-levels, progress-acceleration, game-screen, +shifting-maze-crush, +power-gated-collect, +enemy-to-food, +carry-to-sockets, +pick-one-box, +arrow-scroll-tile, +bonus-stage, +shared-field-coop, +friendly-fire-stun]
proposes: ["+trigger:crushed_by(a, b)", "+axis:scroll", "+window:bonus-round", "+card:shifting-maze-crush", "+card:power-gated-collect", "+card:enemy-to-food", "+card:carry-to-sockets", "+card:pick-one-box", "+card:arrow-scroll-tile", "+card:friendly-fire-stun"]
author: opus
date: 2026-11-09
---

# Devil World — Pac-Man, у якому лабіринт рухає ворог: Деві зсуває все поле й чавить тебе об рамку

## Суть
Дракончик Тамагон їсть крапки Bowa-Bowa в лабіринті, але лише доки тримає хрест — без нього він беззахисний і рівень не пройти. Над полем танцює Деві (Devil) і пальцем показує напрям; міньйони під екраном крутять ролики й зсувають **увесь лабіринт** у цей бік, а рамка екрана стоїть. Тамагона, якого стіна притисла до рамки, розчавлює. Раунд — три сцени: зʼїсти всі крапки, віднести 4 Біблії в печатку в центрі, бонус-лабіринт зі скринями.

## Поле і час
- Лабіринт складено з однакових екранів, що повторюються, тож зсув циклічний: вийшла за край частина повертається з протилежного боку. Рамка (край екрана) нерухома й тверда.
- Прокрутка іде постійно в одному з 4 напрямків; напрям задає Деві жестом угорі екрана — це видимий «намір» до зміни.
- Real-time; Тамагон, рушивши, рухається сам, доки не впреться в стіну.
- Пізніші раунди змінюють форму й кольори лабіринту, додають ворогів; складність росте до 16-го раунду (сцена 46).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тамагон (1P зелений, 2P червоний) | player | життя; стани egg / armed | стартує яйцем; рухається сам до стіни; з хрестом або Біблією дихає вогнем |
| Деві (Devil) | boss | напрям-жест | танцює вгорі, вказує напрям прокрутки; після печатки перетворюється на кажана й тікає |
| Міньйони під екраном (Medaman) | neutral | 2 шт. | крутять ролики / тупотять — виконують зсув у напрямку Деві |
| Medaman | enemy | рожевий, одне око | частина ганяється за Тамагоном; вогонь → смажене яйце |
| Bonbon | enemy | з 7-го раунду | швидший за Medaman, відроджується швидше |
| Маленький Деві (子デビル) | enemy | незнищенний | блукає біля центру; вогонь лише розвертає його |
| Хрест | pickup | тривалість; блимає перед кінцем | дає вогонь і право їсти Bowa-Bowa на обмежений час |
| Bowa-Bowa | pickup | крапки в коридорах | зникають, лише коли Тамагон з хрестом |
| Біблія | pickup | 4, у кутах | як хрест (вогонь); відносять у Devil Hole |
| Devil Hole | static | 4 гнізда в центрі | приймає Біблії; 4/4 → печатка, кінець сцени |
| Смажене яйце (目玉焼き) | object | — | ворог після вогню; зʼїсти — ворог зникає на якийсь час |
| Вогонь | projectile | — | вилітає вперед з armed-Тамагона |
| Морозиво (ソフトクリーム) | pickup | час від часу | кружляє по краю поля, бонусні очки |
| Стіни лабіринту | static | рухаються з прокруткою | чавлять Тамагона об рамку |
| Рамка екрана | static | нерухома | межа, об яку чавить |
| Скриня «?» | container | 6 у бонус-лабіринті | в одній (завжди кутовій) яйце = +1 життя |
| Стрілка на доріжці | terrain | напрям | у бонус-лабіринті: наступив — поле прокручується в її бік |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `state(tamagon, egg)` → ТО `clear_state(tamagon, egg)`, `move(tamagon, dir)`; яйце не можна збити чи притиснути.
- КОЛИ `tick` → ЯКЩО `free(cell_ahead)` → ТО `move(tamagon, facing)`; інакше `custom: «стоїть біля стіни»`.
- КОЛИ `input(dir)` → ЯКЩО `free(cell_in_dir)` → ТО `face(tamagon, dir)`.
- КОЛИ `custom: «Деві змінив жест»` → ТО `custom: «новий напрям прокрутки»` — далі щотік `shift(all, devil_dir)` з циклічним загортанням лабіринту.
- КОЛИ `custom: «стіна, що зсувається, притиснула Тамагона до рамки»` → ЯКЩО `not state(tamagon, egg)` → ТО `lose` (−1 життя).
- КОЛИ `contact(tamagon, cross)` → ТО `pickup`, `set_state(tamagon, armed, dur)`; перед кінцем хрест блимає.
- КОЛИ `enter(tamagon, bowabowa)` → ЯКЩО `state(tamagon, armed)` → ТО `disappear_b`, `score(n)`; інакше `custom: «крапка лишається»`.
- КОЛИ `input(fire)` → ЯКЩО `state(tamagon, armed)` → ТО `spawn(fire)` у напрямку `facing`.
- КОЛИ `contact(fire, medaman|bonbon)` → ТО `transform(enemy, fried_egg)`.
- КОЛИ `contact(tamagon, fried_egg)` → ТО `disappear_b`, `custom: «цей ворог не відроджується якийсь час»`; Bonbon — `respawn` швидше.
- КОЛИ `contact(fire, child_devil)` → ТО `face(child_devil, reverse)` (знищити не можна).
- КОЛИ `contact(tamagon, enemy)` → ЯКЩО `not state(tamagon, egg)` → ТО `lose`.
- КОЛИ `all_gone(bowabowa)` → ТО `custom: «сцена 2 — Біблії»`.
- КОЛИ `contact(tamagon, bible)` → ТО `pickup`, `set_state(tamagon, armed)`.
- КОЛИ `contact(tamagon, devil_hole_slot)` → ЯКЩО `has(tamagon, bible)` → ТО `place(tamagon, bible)`, `counter(seals, +1)`.
- КОЛИ `counter(seals, ==, 4)` → ТО `transform(devil, bat)`, `custom: «Деві тікає до наступного лабіринту»`, `window(bonus-round)`.
- КОЛИ `contact(tamagon, ice_cream)` → ТО `pickup`, `score(bonus)`.
- Бонус-лабіринт: КОЛИ `contact(tamagon, box)` → ЯКЩО `custom: «у скрині яйце»` → ТО `lives(+1)`; КОЛИ `enter(tamagon, arrow)` → ТО `shift(all, arrow_dir)`; стіна не вбиває; КОЛИ `counter(time_left, ==, 0)` → ТО `next_level`.
- 2P: КОЛИ `contact(tamagon_1, tamagon_2)` → ТО `block` (не проходять один крізь одного); КОЛИ `contact(fire, other_tamagon)` → ТО `stun(other_tamagon, n)`.
- КОЛИ `level_start` → ЯКЩО `level(>=, 7)` → ТО `spawn(bonbon)`.
- Перемога: нема (раунди по колу, складність росте до 16-го). · Поразка: життя вичерпано → `game_over`. · Рахунок: Bowa-Bowa, смажені яйця, морозиво, бонус-скрині.

## Керування і ввід
- D-pad — розбити яйце й рушити; далі — задати напрям (Тамагон їде сам до упору).
- A або B — вогонь, лише з хрестом або Біблією.
- Пульт I — 1P (зелений), пульт II — 2P (червоний), гра вдвох одночасно.

## Вікна, меню, HUD
- `splash-screen` — титул; вибір 1 / 2 гравці (`mode-select`).
- `game-screen` — лабіринт у нерухомій рамці; Деві з жестом угорі (`telegraph-marker` напряму зсуву); міньйони внизу; HUD: `score`, `hi-score`, `lives` (?).
- `custom-window` бонус-лабіринту (`+window:bonus-round`): 6 скринь, стрілки, таймер (`timer-countdown`).
- `end-screen` — game over.
- Переходи: титул → сцена 1 (крапки) → сцена 2 (Біблії) → бонус-лабіринт → наступний раунд → … → game over.

## Фічі поза полем
- `levels-sequential`: раунд = 3 сцени; нові вороги й лабіринти; росте до 16-го раунду (сцена 46).
- `mode-coop` — 2P одночасно з дружнім вогнем (оглушує напарника) і без проходу крізь нього.
- Нема збережень, паролів, налаштувань (?).

## Варіації й родичі
- Порти — лише Virtual Console і NSO; у Північній Америці не виходила.
- Родичі: Pac-Man (крапки, тимчасова сила від енерджайзера — тут хрест є умовою самого збору), Rally-X (поле більше за екран, камера за гравцем), Entombed і 10000000 (прокрутка вбиває), Rompers (плити чавлять — той самий тригер «притиснуло»).
- Осі варіацій:
  - **хто рухає поле**: ніхто (Pac-Man) / камера за гравцем (Rally-X) / ворог зсуває все поле, рамка стоїть (Devil World) / автоскрол (Entombed);
  - **що потрібно для збору**: нічого / тимчасовий предмет-дозвіл (хрест) / носити предмет до гнізда (Біблії);
  - **що робить вогонь з ворогом**: убиває / перетворює на їжу (смажене яйце) / лише розвертає (маленький Деві).

## Цікавинки для курсу
- Зсув усього лабіринту з циклічним загортанням + перевірка «стіна притисла аватара до рамки» — 🥉.
- Видимий намір зміни поля (жест Деві) як підказка гравцю — 🌱.
- Хрест-дозвіл: збір можливий лише в тимчасовому стані, таймер з блиманням перед кінцем — 📎.
- Вогонь → ворог стає їжею → зʼїв → таймер відродження: ланцюг станів ворога — 📎.
- Сцена «віднести 4 предмети в гнізда» поверх того ж лабіринту — 🌱.
- Бонус: 6 скринь, яйце завжди в кутовій, стрілки-плитки прокручують поле — 🌱.
- 2P з дружнім вогнем (оглушення напарника) — 📎.

## Мапа на каталог
- Є: `move-auto` ↔ Тамагон їде сам; `collect-all` ↔ Bowa-Bowa; `touch-death` ↔ вороги; `environment-death` ↔ розчавлення об рамку; `player-death`; `temporary-modes` ↔ хрест; `projectile-shot` + `shoot-forward` ↔ вогонь; `respawn` ↔ ворог повертається після зʼїденого яйця; `telegraphed-intents` ↔ жест Деві; `time-out` ↔ таймер бонус-лабіринту; `event-points`; `sequential-levels` · `progress-acceleration` ↔ нові вороги до 16-го раунду; `game-screen`.
- **Нема** → пропозиції карток:
  - `+shifting-maze-crush` «Ворог зсуває все поле, рамка чавить» · entities/death · 🥉 · слот {wrap: bool}.
  - `+power-gated-collect` «Збирати можна лише в тимчасовому стані» · entities/interact · 🌱.
  - `+enemy-to-food` «Ворог після удару стає їжею» · entities/combat · 📎.
  - `+carry-to-sockets` «Віднести N предметів у гнізда» · game-logic/win · 🌱 · слот {n}.
  - `+pick-one-box` «Одна з N скринь з призом» · game-logic/score · 🌱.
  - `+arrow-scroll-tile` «Плитка-стрілка прокручує поле» · entities/interact · 🌱.
  - `+bonus-stage` (Clu Clu Land) · `+shared-field-coop` · `+friendly-fire-stun` «Постріл оглушує напарника» · entities/combat · 🌱.

## Пропозиції до словників
- `+trigger:crushed_by(a, b)` — A притиснуто до B рухомою стіною/плитою (Devil World, Rompers; уже пропонувалось у корпусі).
- `+axis:scroll` — хто рухає видиме поле: `none` · `follow` (камера за гравцем) · `forced` (автоскрол: Entombed) · `enemy` (ворог зсуває поле: Devil World).
- `+window:bonus-round` — бонус-екран між сценами.
- `+card:shifting-maze-crush`, `+card:power-gated-collect`, `+card:enemy-to-food`, `+card:carry-to-sockets`, `+card:pick-one-box`, `+card:arrow-scroll-tile`, `+card:friendly-fire-stun` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Devil World](https://en.wikipedia.org/wiki/Devil_World) — Деві вказує напрям, міньйони з роликами зсувають лабіринт, розчавлення, хрест як умова збору, 4 Біблії в печатку, бонус-лабіринт із 6 скринями на час.
- [Wikipedia JA: デビルワールド](https://ja.wikipedia.org/wiki/デビルワールド) — три сцени, Bowa-Bowa, морозиво по краю, вороги і їхня поведінка, смажене яйце, яйце в кутовій скрині, 2P (нема проходу, вогонь знерухомлює).
- [Nintendo: Famicom 40th — デビルワールド](https://www.nintendo.com/jp/famicom/software/hvc-dd/index.html) — керування, яйце-старт без розчавлення, хрест блимає, стрілки, Bonbon з 7-го раунду, складність до раунду 16 (сцена 46).
- YouTube: пошук «Devil World NES gameplay».

## Непевне
- (?) Очки за Bowa-Bowa, смажені яйця, морозиво; стартові життя; тривалість хреста і таймер бонус-лабіринту — не знайдено.
- (?) Як часто й за яким правилом Деві змінює напрям (розклад чи випадково) — `random: none` під питанням.
- (?) Чи стрілки бувають і поза бонус-лабіринтом (офіційна сторінка — без уточнення сцени).
- (?) Чи гра після 16-го раунду повторюється з тією ж складністю.
