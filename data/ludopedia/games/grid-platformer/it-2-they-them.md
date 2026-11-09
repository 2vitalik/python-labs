---
title: "It 2: They/Them"
slug: it-2-they-them
aka: [It 2, It2]
family: grid-platformer
also: [thinky]
klass: figure
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2025
platforms: [PICO-8, web, Windows, macOS, Linux, Raspberry Pi]
links:
  - {kind: itch, url: "https://twinbeard.itch.io/it2", best: true, note: "керування (D-pad, X — сила, O — розділити/перемкнути групу), премиса; грати в браузері"}
  - {kind: other, url: "https://itch.io/jam/picostevemo-3/topic/5489323/it-2", note: "технічний dev log: сили всіх лузерів, «turn-based puzzle platformer», список обʼєктів карти"}
  - {kind: other, url: "https://twinbeard.itch.io/it2/devlog/1137791/it-2-design-notes", note: "дизайн: гравітація на всю групу, плавання, вода в межах кімнати, кульки й двері, без смерті"}
  - {kind: play, url: "https://html-classic.itch.zone/html/15699881/index.html", note: "web-збірка; з неї розпаковано Lua-код картриджа"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=It+2+They+Them+twinbeard+pico-8", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [party-switch, stick-together, gravity-fall, push-object, inertia-slide, dig-terrain, projectile-shot, button-toggle, checkpoint, teleport, collect-quota, save-autosave, save-progress, objective-text, game-screen, splash-screen, end-screen, keyboard-controls, +caterpillar-follow, +cluster-gravity, +ability-per-character, +summon-ally, +room-reset, +water-flow, +float-in-water, +timed-target, +counter-gate, +flip-screen-rooms, +dialogue-choice]
proposes: ["+effect:float", "+effect:regroup", "+effect:reset_area", "+feature:fast-travel", "+card:cluster-gravity", "+card:caterpillar-follow", "+card:counter-gate", "+card:water-flow"]
author: opus
date: 2026-11-09
---

# It 2: They/Them — сім лузерів однією «гусінню»: гравітація діє на всю групу, у кожного своя сила

## Суть
PICO-8-гра Twinbeard для джему PiCoSteveMo 3: покроковий пазл-платформер у каналізації. Ти рухаєш одного з дітей Клубу лузерів, а решта групи повзе слідом, як гусінь; **гравітація діє на звʼязну групу цілком** — досить, щоб хоч один стояв, і група може звисати з уступу чи тримати форму мосту. Телефоном Майк кличе нових друзів, у кожного своя сила (копати, стріляти з рогатки, плавати, скидати кімнату, збиратись на чекпойнті, пролазити трубами). Мета — відвідати 5 зливових решіток («банка кринжу») і віднести її They/Them; таємна кінцівка — луснути всі кульки.

## Поле і час
- Світ — мапа ~120×120 клітин, поділена на кімнати 15×15 (сітка 8×8 кімнат); екран показує одну кімнату, перехід — при виході за край.
- Хід = крок вибраної дитини (або сила); після ходу гравітація ітеративно зсуває групи вгору/вниз до стабільного стану. Без вводу світ стоїть, крім мішеней (таймер реального часу) і анімацій.
- Вода — поле «вологості» 0…1 у клітинах; після кожної зміни в кімнаті вода перетікає вниз і вбік і вирівнюється — лише в межах поточної кімнати.
- Смерті й поразки нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Майк | piece | старт | дзвонить: став на телефон → приходить наступний лузер |
| Білл | piece | X | уся група телепортується до активного чекпойнта |
| Бен | piece | X | скидає кімнату: обʼєкти на початкові місця, викопане — назад, вода — як була |
| Стен | piece | — | рух у землю = копання (клітина зникає) |
| Бев | piece | X | постріл з рогатки в напрямку останнього руху |
| Едді | piece | — | його група плаває: не спливає й не тоне у воді |
| Річі | piece | ↓ на унітазі | лише він лізе в унітаз: група пролітає трубою до іншого виходу |
| Курсор | — | — | позначає вибрану дитину; переходить на дитину, в яку «впираєшся» |
| Повітряна кулька | object | — | від поштовху ковзає до упору або краю кімнати; не може рушити — лускає; у воді спливає |
| Брила | object | тверда | падає до опори; кульки під нею зсуває вниз або лускає |
| Земля | terrain | — | копає лише Стен |
| Вода | terrain | вологість 0…1 | тече; не-Еддієві групи виносить до поверхні |
| Кнопка (2 види) | switch | — | натиснута, поки на ній дитина чи кулька; перемикає блоки у своєму рядку й стовпці кімнати |
| Мішень | switch | ~90 «тіків» | влучання рогаткою (чи дотик) вмикає на кілька секунд — як кнопку |
| Перемикний блок | gate | стан 2 спрайти | твердий / прохідний залежно від кнопок і мішеней у його рядку чи стовпці |
| Ворота (6) | gate | поріг лопнутих кульок | тверді, доки лопнуто менше порогу; показують, скільки лишилось |
| Телефон | switch | одноразовий | Майк на ньому → «ring ring!» → новий лузер; далі «disconnected» |
| Зливова решітка | pickup | — | стала дитина → сценка з перехожим, решітку засипають, банка кринжу +1 |
| Чекпойнт | switch | один активний | наступив → активний (і збережений), попередній гасне |
| Унітаз / труба | teleport | повороти труби | вхід для групи Річі, вихід — у іншому унітазі |
| They/Them | neutral | — | розмова; банка ≥ 5 → фінал |
| Джорджі | neutral | — | секретна кімната з паперовими корабликами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `occupied(target, loser)` → ТО `custom: «вибрати ту дитину»` (ходу нема).
- КОЛИ `input(dir)` → ЯКЩО `free(target)` → ТО `move(selected, dir)`, `custom: «звільнену клітину займає сусід із групи, за ним — його сусід (гусінь)»`.
- КОЛИ `input(dir)` при затиснутій O → ЯКЩО `free(target)` → ТО `move(selected, dir)` без послідовників — дитина відокремлюється.
- КОЛИ `input(O)` (коротко, без руху) → ТО `custom: «курсор на наступну групу»`.
- Група = звʼязна (4-сусідство) множина дітей; перераховується після кожного ходу.
- КОЛИ `turn_end` → ЯКЩО `custom: «хоч один член групи у воді має воду над собою»` і `not occupied(above_any, solid)` і `not` група Едді → ТО `custom: «група спливає на 1»`; інакше ЯКЩО `not supported(any member)` → ТО `fall` групи на 1; повторювати до стабільності.
- КОЛИ `input(dir)` → ЯКЩО `occupied(target, dirt)` і `state(selected, stan)` → ТО `disappear(dirt)` (копання = хід).
- КОЛИ `input(X)` → ЯКЩО `state(selected, bev)` → ТО `spawn(shot)` — летить до першого твердого чи краю кімнати; кульки на шляху лускають, мішень вмикається.
- КОЛИ `input(X)` → ЯКЩО `state(selected, ben)` → ТО `custom: «скинути кімнату»`, `message(room reset!)`; нічого скидати → `message(nothing to reset!)`.
- КОЛИ `input(X)` → ЯКЩО `state(selected, bill)` → ТО `teleport(group, checkpoint)`.
- КОЛИ `input(down)` → ЯКЩО `occupied(cell, toilet)` і `state(selected, richie)` → ТО `custom: «група Річі мандрує трубою до наступного унітаза й збирається там»`; інакше `message(toilet is too gross to enter)`.
- КОЛИ `contact(loser, balloon)` → ЯКЩО `free(behind_balloon)` → ТО `slide(balloon, dir)` до упору чи краю кімнати; інакше `disappear(balloon)`, `counter(popped, +1)`.
- КОЛИ `counter(popped, >=, threshold)` → ТО `custom: «ворота відчиняються»` — пороги шести воріт 6…99.
- КОЛИ `enter(loser|balloon, button)` → ТО `set_state(blocks_in_row_and_col, toggled)`; КОЛИ `leave` → ТО `clear_state`.
- КОЛИ `custom: «постріл влучив у мішень»` → ТО `set_state(target, on, ~90)` — блоки в рядку й стовпці перемкнені, доки мішень не згасне.
- КОЛИ `enter(mike, phone)` → ТО `message(ring ring!)`, `spawn(next_loser)`, `transform(phone, disconnected)`; інша дитина → `message(only mike can make phone calls)`.
- КОЛИ `enter(loser, stormdrain)` → ТО `window(dialogue-window)`, `counter(cringe_jar, +1)`, `transform(stormdrain, clogged)`.
- КОЛИ `enter(loser, checkpoint)` → ТО `custom: «зробити активним і зберегти»`.
- КОЛИ `enter(loser, theythem)` → ЯКЩО `counter(cringe_jar, >=, 5)` → ТО `window(dialogue-window)`, `win`; інакше `message(fill up that cringe jar!)`.
- КОЛИ `counter(popped, =, 99)` → ТО `custom: «відкрито таємну кінцівку»` (за devlog).
- Перемога: банка кринжу ≥ 5 і розмова з They/Them. · Поразки нема — застряг → скидання кімнати (Бен) або чекпойнт (Білл). · Рахунок: лічильник лопнутих кульок.

## Керування і ввід
- D-pad — рух вибраної дитини; рух у іншу дитину — вибір її.
- X — сила вибраної дитини (Білл, Бен, Бев); у Стена, Едді, Майка, Річі сила пасивна або «на клітині».
- O (Z) коротко — перемкнути групу; O затиснути + рух — відокремити дитину від групи.
- У діалогах: ↑/↓ — варіант відповіді, O — вибір.

## Вікна, меню, HUD
- Меню PICO-8 при запуску: Restore game / Run game.
- `splash-screen`: логотип, «press O or X to begin»; далі діалог Пеннівайза (нова гра) або «continue / start over».
- `game-screen`: кімната 15×15; праворуч колонка з портретами 7 дітей (`player-portraits`, курсор на вибраній), лічильник лопнутих кульок (червоний на 99), анімація банки кринжу; знизу — рядок повідомлень, що друкується по літері (`objective-text`: «press O to switch to bill», «hold O to separate», «ring ring!»).
- `dialogue-window`: портрет співрозмовника, текст, 1–3 варіанти відповіді (`choose`) — дзвінки кожному лузерові, перехожі над решітками, They/Them.
- Сценка решітки: вигляд знизу на перехожого, що засипає решітку.
- `end-screen`: «the end...?» і титри.

## Фічі поза полем
- `autosave` у cartdata: зібрані діти, лопнуті кульки, засипані решітки, осілі брили, активний чекпойнт; «continue / start over» на старті.
- Швидка подорож — сила Білла до чекпойнта; скидання кімнати — сила Бена (замість undo).
- Порядок появи дітей фіксований (Майк → Білл → Бен → Стен → Бев → Едді → Річі); у другій половині пазли вимагають ділити групу й поєднувати сили (devlog).
- Діалоги з вибором відповіді — лише смак, на механіку не впливають.

## Варіації й родичі
- Попередні ігри дизайнера: рух групи запозичено з копальної міні-гри Frog Fractions (Hat DLC); скидання кімнати — нащадок предметів-перемотки з Look Who's The Shining Two (devlog).
- Родичі: The Lost Vikings, Quadrax, Kwirk — кілька героїв з перемиканням; Snakebird — тіло з кількох клітин під гравітацією; Mekorama, Toki Tori 2 — покрокова платформна логіка.
- Осі варіацій:
  - **група**: окремі герої (Lost Vikings) / звʼязне тіло (Snakebird) / гусінь із розділенням (It 2);
  - **опора**: кожен сам / група стоїть, якщо стоїть хоч один (It 2, Snakebird);
  - **вода**: смерть / спливання / плавання за умови (Едді в групі);
  - **ворота**: ключ / кнопка / глобальний лічильник (лопнуті кульки).

## Цікавинки для курсу
- Гусінь: рух лідера + заповнення звільненої клітини сусідом рекурсивно; утримання O — відрив — 🥉.
- Гравітація на звʼязну групу (компоненти звʼязності після кожного ходу, «стоїть хоч один») — 🥉.
- Вода як поле дробових рівнів, що перетікає в межах кімнати — 🥈.
- Кнопки й мішені, що перемикають блоки свого рядка і стовпця — 📎.
- Ворота з порогом глобального лічильника — 🌱.
- Скидання кімнати (збережені початкові позиції + журнал викопаного + знімок води) — 📎.
- Труби з поворотами як телепорт групи — 📎.

## Мапа на каталог
- Є: `party-switch` ↔ перемикання груп; `stick-together` ↔ звʼязні групи; `gravity-fall` ↔ падіння груп і брил; `push-object` + `inertia-slide` ↔ кульки ковзають до упору; `dig-terrain` ↔ Стен; `projectile-shot` ↔ рогатка; `button-toggle` ↔ кнопки й мішені; `checkpoint` ↔ чекпойнти; `teleport` ↔ Білл і труби; `collect-quota` ↔ 5 решіток, пороги кульок; `save-autosave` + `save-progress` ↔ cartdata; `objective-text` ↔ рядок повідомлень; `splash-screen` / `game-screen` / `end-screen`; `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+caterpillar-follow` «Гусінь: решта групи заповнює звільнену клітину» · entities/move · 🥉.
  - `+cluster-gravity` «Гравітація на звʼязну групу: стоїть, якщо стоїть хоч один» · entities/move · 🥉.
  - `+ability-per-character` «Своя сила в кожного героя загону» · entities/state · 📎.
  - `+summon-ally` «Покликати нового героя з точки» · entities/spawn · 🌱.
  - `+room-reset` «Скинути лише поточну кімнату» · game-logic/history · 📎.
  - `+water-flow` «Вода як рідина, що перетікає клітинами» · entities/move · 🥈.
  - `+float-in-water` «Спливання до поверхні» · entities/move · 🌱.
  - `+timed-target` «Мішень вмикає перемикач на час» · entities/interact · 🌱.
  - `+counter-gate` «Ворота відчиняються на порозі глобального лічильника» · entities/interact · 🌱.
  - `+flip-screen-rooms` «Світ кімнат, екран перемикається на краю» · interface/render · 📎.
  - `+dialogue-choice` «Діалог із вибором відповіді» · interface/menus · 📎.

## Пропозиції до словників
- `+effect:float(a)` — спливає на 1 клітину вгору у воді (It 2; родич `fall` з протилежним знаком).
- `+effect:regroup(group, where)` — зібрати всю групу навколо точки (Білл).
- `+effect:reset_area(room)` — повернути до початкового стану лише частину поля (Бен; відмінне від `restart` рівня).
- `+feature:fast-travel` — перенестися до відвіданої точки (чекпойнт Білла).
- `+card:cluster-gravity`, `+card:caterpillar-follow`, `+card:counter-gate`, `+card:water-flow` — див. вище.

## Джерела
- ⭐ [itch.io: It 2: They/Them](https://twinbeard.itch.io/it2) — премиса, керування, теги (Turn-based, Puzzle-Platformer), коментарі гравців (чекпойнти, Cringe Jar, мішені на час).
- [PiCoSteveMo 3: It 2 dev log](https://itch.io/jam/picostevemo-3/topic/5489323/it-2) — сили Майка, Білла, Бена, Стена, Бев, Едді; «turn-based puzzle platformer»; обʼєкти balloon, boulder, phone, target, stormdrain, checkpoint, button, gate, theythem; швидка подорож.
- [Devlog: It 2 design notes](https://twinbeard.itch.io/it2/devlog/1137791/it-2-design-notes) — «The group follows whoever's in the lead, and gravity affects the entire group»; плавання; вода в межах кімнати; кульки й двері; «no death, no lose state»; таємна кінцівка за всі кульки.
- [Web-збірка](https://html-classic.itch.zone/html/15699881/index.html) — Lua-код картриджа розпаковано й прочитано: гусінь, кластери й гравітація, пороги воріт, кнопки рядок/стовпець, мішені, банка ≥ 5, Річі й труби, тексти сил і діалогів.
- YouTube: пошук «It 2 They Them twinbeard pico-8».

## Непевне
- (?) Розмір мапи ~120×120 і сітка 8×8 кімнат — з коду (цикли до 120, кімната 15), реальна заповненість невідома.
- (?) Мішень вмикається на ~90 «тіків» лічильника з кроком 0,5 за кадр — у секундах приблизно 6 (?), не перевірено в грі.
- (?) Який зі станів перемикного блока твердий за замовчуванням — з коду не видно (прапорці спрайтів не розбирались).
- (?) Чи всі 99 кульок потрібні саме для таємної кінцівки, чи лише для останніх воріт (поріг 99) — devlog каже «за всі кульки».
- (?) Автор: у титрах «jim stormdancer», акаунт — Twinbeard.
