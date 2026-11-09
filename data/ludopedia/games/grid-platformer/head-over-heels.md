---
title: Head over Heels
slug: head-over-heels
aka: [Head Over Heels, HoH]
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: iso
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: collect
year: 1987
platforms: [ZX Spectrum, Amstrad CPC, C64, MSX, Atari 8-bit, Atari ST, Amiga, PC (ремейк 2003), Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Head_over_Heels_(video_game)", best: true, note: "здібності Head і Heels, поєднання, 300+ кімнат, планети й корони, вороги, порти й ремейки"}
  - {kind: other, url: "https://www.everygamegoing.com/larticle/Head-Over-Heels-000/28421", note: "огляд Zzap! 1987: пончики й рупор, сумка з діркою, 4 види кроликів, риба-воскресіння, собаки-мости, телепорти"}
  - {kind: other, url: "https://www.theregister.com/2012/05/09/antique_code_show_head_over_heels/?page=2", note: "перемикання героїв, злиття, подвійна висота, окремі життя, мапи нема"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Head+over+Heels+1987+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [party-switch, stick-together, gravity-fall, projectile-shot, item-pickup, inventory-items, temporary-modes, touch-death, environment-death, player-death, checkpoint, teleport, teleport-one-way, button-toggle, timed-despawn, multi-cell-size, game-screen, +fuse-avatars, +ability-split, +observer-vanish, +per-avatar-powerup, +stun-projectile, +carry-in-room, +crown-goal]
proposes: ["+effect:switch_avatar", "+trigger:seen_by", "+card:fuse-avatars", "+card:observer-vanish", "+card:per-avatar-powerup", "+card:ability-split"]
author: opus
date: 2026-11-09
---

# Head over Heels — два шпигуни з різними вміннями проходять 300+ ізометричних кімнат окремо й зʼєднуються в одного

## Суть
Ізометрична пригода-головоломка з 300+ кімнат. Гравець по черзі керує двома героями: **Head** високо стрибає, керує польотом і (з рупором) стріляє пончиками, що знерухомлюють ворогів; **Heels** бігає вдвічі швидше, лізе на певні сходи й носить предмети в сумці. Коли Head стає на Heels, вони **зливаються в одного** з поєднаними вміннями, але вдвічі вищого — у вузькі проходи такий не пролізе. Мета — повернути корони планет імперії Blacktooth або просто втекти.

## Поле і час
- Мапа — граф кімнат (300+), кожна — ізометрична коробка з блоків-платформ, з виходами на 4 боки й угору/вниз (?).
- Рух у кімнаті плавний, але кімнати збудовані з однакових блоків-кубів сітки (рушій Filmation II від Batman 1986).
- Real-time; гравітація; висота — третя вісь (блоки ставлять одне на одне).
- Інформація часткова: видно одну кімнату; мапи в грі нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Head | player | життя; пончики | високий стрибок із керуванням у повітрі; з рупором стріляє пончиками |
| Heels | player | життя | біг ×2, лізе на певні сходи; сумка — несе один предмет у межах кімнати (?) |
| Head+Heels (злиті) | player | висота 2 | рухаються разом; вміння обох; не пролазить у низькі проходи |
| Рупор (hooter) | pickup | — | лише Head: дає стріляти пончиками |
| Таця пончиків | pickup | +6 | запас набоїв для рупора |
| Сумка (bag) | pickup | — | лише Heels: брати й класти предмети; між кімнатами не несе |
| Кролик «життя» | pickup | +життя | діє на обох, якщо злиті |
| Кролик «невразливість» | pickup | тривалість | тимчасовий щит |
| Кролик «стрибок» | pickup | тривалість | вищий стрибок — марний для Head |
| Кролик «швидкість» | pickup | тривалість | швидший біг — марний для Heels |
| Риба-воскресіння | pickup | жива / мертва | жива = точка відродження; мертва — отрута |
| Корона | pickup | одна на планету | мета гри; 5 штук |
| Телепорт | static | парний / односторонній | переносить між кімнатами й планетами |
| Собаки-місток (Hush Puppies) | terrain | видимі / зникли | зникають, коли Head у кімнаті; повертаються, коли він не бачить |
| Платформи, що зникають | terrain | — | зникають під героєм (?) |
| Смертельна підлога, котли | hazard | — | дотик — смерть |
| Робот-«Далек» | enemy | керується кнопкою | рухається / стоїть за станом кнопки |
| Дрон-шукач | enemy | — | пікірує на героя на великій швидкості |
| Інші вороги | enemy | вид за планетою | дотик — смерть; пончик знерухомлює |
| Кнопка (push switch) | switch | вкл/викл | перемикає роботів |
| Блоки-кубики | object | — | платформи; частину можна штовхати чи носити (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(swop)` → ТО `custom: «керування переходить до іншого героя»`; якщо злиті — перемикач між злитим і окремими (?).
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(active, dir)`; Heels — з подвоєною швидкістю.
- КОЛИ `input(jump)` → ТО `custom: «стрибок; у Head — вищий і керований у повітрі»`; без опори — `fall(active)`.
- КОЛИ `custom: «Head приземлився на Heels»` → ТО `attach(head, heels)` — злиття; висота злитого = 2 блоки.
- КОЛИ `input(dir)` → ЯКЩО `state(pair, fused)` і `custom: «прохід нижчий за 2»` → ТО `block`.
- КОЛИ `input(fire)` → ЯКЩО `has(head, hooter)` і `has(head, doughnuts)` → ТО `spawn(doughnut)`, `take(head, doughnut)`.
- КОЛИ `contact(doughnut, enemy)` → ТО `freeze(enemy, n)` — ворог злизує пончик.
- КОЛИ `input(carry)` → ЯКЩО `has(heels, bag)` і `occupied(below, object)` → ТО `pickup`; повторно → `place(object, here)`.
- КОЛИ `leave(heels, room)` → ЯКЩО `custom: «у сумці предмет»` → ТО `custom: «предмет лишається в кімнаті» (дірка в сумці)`.
- КОЛИ `contact(active, bunny)` → ТО `set_state(active, power, duration)`; ЯКЩО `state(pair, fused)` → діє на обох; невідповідний кролик — `custom: «ефект марний»`.
- КОЛИ `contact(active, fish)` → ЯКЩО `state(fish, alive)` → ТО `checkpoint`; ЯКЩО `state(fish, dead)` → ТО `lives(-1)`.
- КОЛИ `custom: «Head у кімнаті й бачить собак-місток»` → ТО `disappear_b`; КОЛИ `custom: «Head вийшов»` → ТО `spawn_at(dogs, place)`.
- КОЛИ `contact(active, button)` → ТО `set_state(robots, toggled)`.
- КОЛИ `enter(active, teleport)` → ТО `teleport`; односторонній — без повернення.
- КОЛИ `contact(active, enemy|hazard)` → ЯКЩО `not state(active, invulnerable)` → ТО `lives(-1)` для цього героя; КОЛИ `custom: «у героя 0 життів»` → ТО `custom: «герой зникає назавжди»` — без нього гру, можливо, не пройти.
- КОЛИ `contact(active, crown)` → ТО `pickup`, `counter(crowns, +1)`.
- Перемога: повернути 5 корон (усі не обовʼязкові) або втекти на Freedom. Поразка: життя обох вичерпано. Рахунок: відсоток дослідженого й визволені планети (?).

## Керування і ввід
- 4 напрямки ізометрії (клавіші/джойстик), стрибок, вогонь (Head), взяти/покласти (Heels), «swop» — перемкнути героя.
- Кнопки перевизначаються в меню (?).
- Злиття — фізичне: стрибнути Head на голову Heels.

## Вікна, меню, HUD
- `splash-screen` / `main-menu`: Грати, Продовжити (від риби), Клавіші, Звук (?).
- `game-screen`: ізометрична кімната + HUD: `lives` для кожного героя окремо, запас пончиків, індикатори кроликів (щит, швидкість, стрибок), іконки рупора й сумки (?).
- `end-screen` — підсумок (відсоток, планети) (?).
- Переходи: меню → камери Blacktooth → ринок → Moonbase (хаб телепортів) → планети → (корони) повстання / втеча на Freedom.

## Фічі поза полем
- Збереження нема; `continue` від останньої з'їденої живої риби.
- Немає внутрішньої карти — гравці малювали на папері.
- Ремейк 2003 (Retrospec, PC): сейв — так само через рибу, без безсмертя.
- Відкритий ремейк: камера за активним героєм, чити, інші розміри екрана.

## Варіації й родичі
- Batman (1986) — той самий рушій, один герой; Monster Max (1994) — спадкоємець.
- Knight Lore, Alien 8 (Ultimate) — ізометричні попередники Filmation.
- Сучасні родичі «два аватари з різними вміннями»: Thomas Was Alone, Brothers, Trine; party-switch у Catrap, XOR.
- Осі: **як поєднуються аватари** (ніяк / стати один на одного / злипання); **поділ умінь** (ортогональні / часткові); **ресурс бонусу** (на одного / на пару).

## Цікавинки для курсу
- Два аватари з ортогональними вміннями + злиття в третю сутність з обʼєднаними вміннями й більшим розміром — 🥈.
- Бонус, що діє лише на «правильного» героя (марний кролик) — 🌱.
- Обʼєкт, що зникає, коли його «бачить» певна сутність (собаки-місток) — 📎.
- Риба-checkpoint, що псується в отруту — 🌱.
- Окремі життя на кожного героя; втрата одного може зробити гру непрохідною — 🌱 (дизайн-питання).
- Граф кімнат з односторонніми телепортами — 🥉.

## Мапа на каталог
- Є: `party-switch` · `stick-together` (злиття) · `gravity-fall` · `projectile-shot` (пончики) · `item-pickup` · `inventory-items` (рупор, сумка) · `temporary-modes` (кролики) · `touch-death` · `environment-death` · `player-death` · `checkpoint` (риба) · `teleport` · `teleport-one-way` · `button-toggle` (кнопки роботів) · `timed-despawn` (зникаючі платформи) · `multi-cell-size` (злитий — висота 2) · `game-screen`.
- **Нема** → пропозиції карток:
  - `+fuse-avatars` «Два аватари зливаються в один з обʼєднаними вміннями» · entities/move · 🥈.
  - `+ability-split` «Вміння розподілені між аватарами» · entities/state · 📎.
  - `+observer-vanish` «Обʼєкт зникає, коли його бачить певна сутність» · entities/interact · 📎.
  - `+per-avatar-powerup` «Бонус діє лише на певного героя» · entities/state · 🌱.
  - `+stun-projectile` «Снаряд знерухомлює, а не вбиває» · entities/combat · 🌱.
  - `+carry-in-room` «Нести предмет лише в межах кімнати» · entities/interact · 🌱.
  - `+crown-goal` «Збери N ключових предметів, не всі обовʼязкові» · game-logic/win · 🌱.

## Пропозиції до словників
- `+effect:switch_avatar` — передати керування іншому аватару (Head over Heels, Catrap, XOR).
- `+trigger:seen_by(a, b)` — B у полі зору / в кімнаті з A (собаки зникають від Head).
- `+card:fuse-avatars`, `+card:observer-vanish`, `+card:per-avatar-powerup`, `+card:ability-split` — див. вище.

## Джерела
- ⭐ [Wikipedia: Head over Heels](https://en.wikipedia.org/wiki/Head_over_Heels_(video_game)) — здібності, 300+ кімнат, Blacktooth, Moonbase, планети, корони, вороги-Далеки, собаки-сходи, порти й ремейки.
- [Everygamegoing: огляд Zzap! 1987](https://www.everygamegoing.com/larticle/Head-Over-Heels-000/28421) — пончики по 6, рупор, сумка з діркою, 4 кролики й марні ефекти, риба, собаки-мости, телепорти, дрони, 5 планет.
- [The Register: Antique Code Show](https://www.theregister.com/2012/05/09/antique_code_show_head_over_heels/?page=2) — перемикання клавішею, злиття, подвійна висота, окремі життя, мапи нема, ремейк.
- YouTube: пошук «Head over Heels 1987 gameplay».

## Непевне
- (?) Хто з героїв лізе на сходи і що саме носить сумка (один предмет?); чи можна штовхати блоки.
- (?) Як працює «swop», коли герої злиті (окреме керування з'єднаної пари).
- (?) Склад HUD, меню й підсумкового екрана; рахунок у відсотках — з памʼяті.
- (?) Як виглядають виходи кімнат (угору/вниз) і чи є конвеєри й пружини — у відкритих джерелах не згадано.
- (?) Кількість життів на старті.
