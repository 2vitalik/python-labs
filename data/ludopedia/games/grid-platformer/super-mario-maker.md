---
title: Super Mario Maker 2
slug: super-mario-maker
family: grid-platformer
also: [build-sim]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: online
  info: full
  random: none
  goal: state
year: 2019
platforms: [Switch (SMM2 2019), Wii U (SMM 2015), 3DS (SMM 2016)]
links:
  - {kind: fandom, url: "https://www.mariowiki.com/Super_Mario_Maker_2", best: true, note: "Super Mario Wiki: повний список деталей курсу з легендою модифікаторів, теми, Course World, Endless, Maker points"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Super_Mario_Maker_2", note: "стилі, кооп-створення, World Maker, Story Mode, оновлення"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Super_Mario_Maker", note: "перша частина: стек, гриб/крила, upload лише після проходження, 100 Mario Challenge"}
  - {kind: fandom, url: "https://www.mariowiki.com/Undodog", note: "Undodog (undo), Reset Rocket, Mr. Eraser, Coursebot як персонажі-інструменти"}
  - {kind: fandom, url: "https://www.mariowiki.com/Clear_Condition", note: "умови проходження: категорії Actions / Parts / Status / Other"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=super+mario+maker+2+course+maker+tutorial", note: "пошук; редактор"}
stage: v1
coverage: 65
mechanics: [in-game-editor, editor-palette, editor-erase, editor-undo, editor-playtest, editor-draw-tools, editor-map-check, level-exchange, level-metadata, level-rating, level-bank, save-multi-slot, gravity-fall, item-pickup, touch-death, player-death, reach-exit, collect-quota, time-out, checkpoint, teleport-pair, key-and-door, temporary-modes, enemy-patrol, theme-select, leaderboard, profile-stats, difficulty-levels, game-screen, main-menu, pause-menu, end-screen, field-scaling, +part-modifiers, +part-variants, +container-part, +clear-condition, +level-share-code, +sub-area-link, +liquid-level, +random-level-run, +world-map, +ghost-run]
proposes: ["+feature:level-editor", "+feature:level-sharing", "+feature:user-levels-browser", "+feature:level-rating", "+feature:ghost-run", "+feature:mode-endless", "+window:editor-window", "+window:course-browser", "+window:part-menu", "+window:upload-dialog", "+window:comment-board", "+ui:tool-palette", "+ui:element-picker", "+ui:clear-rate", "+ui:like-boo-buttons", "+effect:attach", "+effect:set_state", "+cond:clear_condition", "+axis:session", "+card:part-modifiers", "+card:clear-condition"]
author: opus
date: 2026-11-02
---

# Super Mario Maker 2 — редактор платформерних рівнів, де кожна деталь — клітинний «конструктор» з модифікаторами

## Суть
Гра-редактор: курсором ставиш деталі (рельєф, предмети, вороги, механізми) на сітку 2D-курсу Mario, миттєво перемикаєшся в гру й назад, а пройдений тобою курс викладаєш у Course World, де інші грають, лайкають, коментують, а кліринг-рейт визначає складність. Для корпусу цінне не стрибання, а **система деталей**: кожна має варіанти й набір модифікаторів (крила, парашут, великий гриб, ключ, стек, «покласти всередину блоку/труби/гармати», «на рейку»), і майже будь-яку деталь можна вкласти в іншу. Клас `hybrid`: редактор — `cursor`, гра — `avatar`.

## Поле і час
- Курс — 2D-сітка блоків, горизонтальна (до кількох сотень клітин (?)) або вертикальна; основна зона + **підзона** (sub-area) з власною темою, звʼязані трубами/дверима.
- Редактор: статичний, курсор/тач; зум (стік), прокрутка; рендер у стилі SMB / SMB3 / SMW / NSMBU / SM3DW (3D World — окремий «extra»-стиль, перемикання стирає курс).
- Гра: real-time, 60 fps фізика платформера; таймер курсу (налаштовуваний), автоскрол (вимкнено / повільно / норм. / швидко / Custom Scroll — до 10 змін напрямку на зону), рівень води/лави/отрути (фіксований / росте / спадає).
- Теми: Ground, Underground, Castle, Airship, Underwater, Ghost House, Desert, Snow, Sky, Forest; **нічна версія** теми змінює правила (у нічному Forest вода стає отрутою; інші ефекти — (?)).

## Сутності
Палітра поділена на категорії (mariowiki: Terrain · Items · Enemies · Gizmos · Other). Таблиця — за типами з власною поведінкою, не кожна деталь.
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Mario (і Luigi/Toad/Toadette онлайн) | player | форма small/super/power-up | біг, стрибок, гравітація; у Course World стартує small |
| Ground | static | — | опора; малюється перетягуванням |
| Slope (steep/gentle) | static | напрям, довжина | похила опора |
| Pipe | gate | довжина, напрям, колір (швидкість виходу) | вхід → інша труба (пара) / підзона; може випускати вкладену деталь |
| Clear Pipe | terrain | шлях | транспортує героя/предмети |
| Semisolid / Mushroom Platform / Bridge | terrain | ширина, колір | опора знизу прохідна |
| Spike Trap | hazard | — | дотик = шкода |
| Block / ? Block / Hard / Hidden / Donut / Note / Music / Cloud / Ice | object | вміст | ? і цегла — контейнер; Donut падає під вагою; Note відкидає; Hidden — невидимий до удару |
| Coin / 10-/30-/50-Coin / Pink Coin | pickup | номінал | Pink Coin: усі зібрані в зоні → зʼявляється ключ |
| Power-ups (Super Mushroom, Fire Flower, Super Leaf, Cape Feather, Super Bell, Frog Suit, Master Sword …) | pickup | залежить від стилю | змінює форму/здібності героя |
| Super Star | pickup | тривалість | `temporary-modes`: невразливість |
| 1-Up / Rotten Mushroom | pickup / enemy | — | життя / переслідує героя |
| Key + Key Door | pickup + gate | — | ключ відкриває двері |
| Door / P Door / Warp Door | gate | пара | телепорт між дверима однієї мітки |
| Вороги (Goomba, Koopa, Piranha Plant, Bill Blaster, Boo, Thwomp, Lakitu, Bowser…) | enemy | варіант, модифікатори | власні патерни; більшість — `enemy-patrol` / чекання / погоня |
| Lakitu's Cloud / Clown Car | container | хто пілотує | вкладений ворог/предмет «керує» хмарою/машиною |
| Bill Blaster / Cannon | spawner | що стріляє | випускає вкладену деталь |
| Track | terrain | контур | деталь «на рейці» рухається по ній |
| ON/OFF Switch + ON/OFF Blocks | switch + gate | стан червоний/синій | удар перемикає всі блоки курсу |
| P Switch | switch | тривалість | монети ↔ цегла, P-двері відкриваються |
| Conveyor / Snake Block / Lift / Seesaw | terrain | напрям, швидкість | везе героя |
| Checkpoint Flag | static | до 2 на курс (?) | точка респавну; може містити power-up |
| Goal (флаг/ворота) | static | — | кінець курсу; перевірка clear condition |

## Правила (КОЛИ → ЯКЩО → ТО)
**Редактор (основний донор):**
- КОЛИ `input(drag part → cell)` → ЯКЩО `free(cell)` і `count(category, <, limit)` (?) → ТО `place(part, cell)`; тягнення по рядку — малює серію (ground).
- КОЛИ `input(drag part → container_part)` (блок, труба, гармата, хмара, клоун-кар, дерево, прапорець) → ЯКЩО модифікатор «can go into …» дозволено → ТО `attach(part, container)`: деталь стає вмістом.
- КОЛИ `input(drag mushroom|wings|parachute|key → part)` → ЯКЩО деталь має цей модифікатор → ТО `set_state(part, big|winged|parachute|holds_key)`.
- КОЛИ `input(drag enemy → enemy)` → ЯКЩО обидва стекові → ТО `custom: «стек»` (вежа ворогів, рухаються разом).
- КОЛИ `input(long-press/tap part)` → ТО `window(part-menu)`: варіант (колір Koopa, напрям труби, розмір), модифікатори вкл/викл. У SMM1 — **трусанути** деталь (shake) → варіант.
- КОЛИ `input(eraser, cell)` → ТО `disappear(part)`; КОЛИ `input(undo)` → ТО `custom: «скасувати останню дію (Undodog)»`; Reset Rocket — очистити курс.
- КОЛИ `input(copy+drag)` → ТО `clone(part)`; `multigrab` — рамка → переміщення/копія групи (?).
- КОЛИ `input(play)` → ТО `custom: «миттєвий тест з поточного стану; назад — у той самий кадр редагування»`.
- КОЛИ `input(upload)` → ЯКЩО `custom: «автор пройшов курс від старту до фінішу з виконаною clear condition (Clear Check)»` → ТО `window(upload-dialog)`: назва, опис, 2 теги → видача 9-символьного Course ID.

**Гра:**
- КОЛИ `contact(mario, enemy)` збоку → ТО `custom: «шкода: power-up → small; small → смерть»`; згори → ТО `disappear_b` (stomp) для більшості.
- КОЛИ `contact(mario, power_up)` → ТО `pickup`, `transform(mario → form)`.
- КОЛИ `input(enter pipe|door)` → ТО `teleport(mario, linked_exit)` (у т.ч. в підзону).
- КОЛИ `contact(any, on_off_switch)` → ТО `set_state(all on_off_blocks, flip)`.
- КОЛИ `counter(pink_coins_in_area, ==, 0)` → ТО `spawn(key)`.
- КОЛИ `enter(mario, pit|lava|poison)` → ТО `lose`; КОЛИ `counter(timer, ==, 0)` → ТО `lose`.
- КОЛИ `contact(mario, goal)` → ЯКЩО `clear_condition_met` (напр. зібрано N монет, переможено N ворогів, без стрибків, у формі X) → ТО `win`; інакше — ворота не зараховують (?).
- КОЛИ `contact(mario, checkpoint)` → ТО `checkpoint`.
- Course World: КОЛИ `win` або `lose` → ТО `custom: «clear rate = clears/attempts → тир складності Easy/Normal/Expert/Super Expert»`; КОЛИ `input(like|boo)` → ТО `counter(maker_points, ±)`.

## Керування і ввід
- Редактор: тач-екран (портатив) або курсор стіком (док), кнопки — швидкі слоти деталей, «-» — гра/редагування, стік-клік — зум.
- Палітра: смуга останніх деталей + повне колесо/список за категоріями; drag деталі на клітину; drag модифікатора на деталь; довге натискання — меню варіантів.
- Інструменти: Mr. Eraser (гумка, тягнути), Undodog (undo), копіювання, multigrab (?), Reset Rocket (очистити), Coursebot (збережені курси).
- Кооп-редагування: два гравці на одній консолі редагують один курс.
- Гра: біг/стрибок/спін; онлайн до 4 гравців коопом чи наввипередки.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Story Mode · Course Maker → `editor-window` · Course World → `custom-window` «Course World» · Coursebot → `save-slots`.
- `editor-window`: курс у сітці, верхня `tool-palette` з останніми деталями, ліва колонка: стиль, тема/день-ніч, налаштування курсу (таймер, автоскрол, рідина, clear condition), Undodog, гумка, копія, Coursebot; перемикач основна/підзона; `zoom-control`.
- `custom-window` «part-menu» — меню деталі: варіанти й модифікатори з іконками (крила, парашут, гриб, ключ).
- `custom-window` «clear-condition picker» — категорії Actions/Parts/Status/Other і число N.
- `upload-dialog`: Clear Check-статус, назва, опис, теги; після — Course ID.
- Course World: `custom-window` «course-browser» (Popular, New, Hot, пошук за ID, фільтри: стиль, тема, складність, регіон, теги) → сторінка курсу (clear rate, світовий рекорд, перший кліринг, лайки) → `custom-window` «comment board» (текст, малюнки, 12 штампів) → `game-screen`.
- `profile-window` (Maker profile: медалі, Maker points, Versus Rating D…S+), `leaderboard` (медалі за рейтинги).
- Endless Challenge: `difficulty-select` (Easy/Normal/Expert/Super Expert) → низка курсів, лічильник життів і пройдених.
- `game-screen` HUD: `timer-countdown`, `coins`, `score`, `lives` (Endless), `objective-text` clear condition, `progress-bar` умови (?).
- `pause-menu`: продовжити · рестарт (у Endless — −1 життя) · вийти; у тестовому режимі — назад у редактор.
- `end-screen` курсу: час, лайк/бу, коментар.

## Фічі поза полем
- `level-editor` + `editor-playtest` миттєвий + `editor-map-check` (Clear Check: курс не вийде онлайн, поки автор сам не пройде).
- `level-sharing` (Course ID 9 символів, 33 знаки алфавіту), `user-levels-browser`, `level-rating` (like/boo), кліринг-рейт → тир складності, коментарі з малюнками, модерація (видалення курсів/коментарів, заміна імені на «????»).
- `mode-endless` (Endless Challenge: випадкові курси, 5/5/15/30 життів за складністю, рекорди), `ghost-run` (Ninji Speedruns з привидами), `online-multiplayer` (кооп/versus до 4, Versus Rating).
- `world-map` — World Maker: Super World до 8 світів × до 5 курсів, Toad houses, труби-варпи; збережено до 6, викласти — 1.
- Story Mode: понад 100 «робіт» від Nintendo як навчання прийомам.
- `save-slots` у Coursebot; у SMM1 — поступове розблокування деталей, 100/10 Mario Challenge, зірки → більше аплоадів, Soundfrog (звукові ефекти), Mystery Mushroom-костюми.

## Варіації й родичі
- SMM (Wii U 2015) → SMM 3DS (без аплоаду) → SMM2 (2019: схили, ON/OFF, підзони вертикальні, clear conditions, 3D World-стиль, World Maker, онлайн-мультиплеєр).
- Родичі-редактори: Lode Runner (Game Generator 1983), Excitebike (Design mode), LittleBigPlanet, Levelhead, Mario Paint (Undodog).
- Осі: **стиль як набір правил** (одні деталі — різна фізика в SMB/SMW/3DW); **як деталь змінюється** (трусанути / меню варіантів / модифікатор-перетягування); **вкладеність** (деталь у блоці / трубі / гарматі / хмарі / на рейці); **умова проходження** (фініш / фініш + умова); **як рівень потрапляє до людей** (файл / код ID / браузер з рейтингом / випадкова низка).

## Цікавинки для курсу
- Модифікатори як дані: таблиця «деталь × {wings, parachute, big, key, stack, into-block, on-track}» з дозволами — 🥈 (майже `interaction-table`).
- Вкладення деталі в деталь (ворог у ?-блоці, гриб у трубі, Goomba пілотує клоун-кар) — 🥈 (дерево контейнерів).
- Clear Check: не дати зберегти/викласти рівень, поки автор його не пройшов — 🥉 (простий аналог — `editor-map-check` з BFS 🥇).
- Clear condition з параметром N як окремий шар перемоги — 📎.
- Миттєве перемикання редактор ↔ гра з поверненням у той самий стан — 🥉 (state-as-data).
- Кліринг-рейт → автоматичний тир складності + Endless-режим з випадкових рівнів тиру — 🥉.
- Код рівня з 9 символів (база 33) як ключ обміну — 📎.

## Мапа на каталог
- Є: `in-game-editor` · `editor-palette` · `editor-erase` · `editor-undo` · `editor-playtest` · `editor-draw-tools` (малювання ground перетягуванням) · `editor-map-check` (Clear Check) · `level-exchange` · `level-metadata` (назва, опис, теги) · `level-rating` · `level-bank` (Coursebot) · `save-multi-slot` · `gravity-fall` · `item-pickup` · `touch-death` · `player-death` · `reach-exit` · `collect-quota` (clear condition «N монет») · `time-out` · `checkpoint` · `teleport-pair` (труби/двері) · `key-and-door` · `temporary-modes` (Star) · `enemy-patrol` · `theme-select` · `leaderboard` · `profile-stats` · `difficulty-levels` (Endless) · `game-screen` · `main-menu` · `pause-menu` · `end-screen` · `field-scaling` (зум).
- **Нема** → пропозиції карток:
  - `+part-modifiers` «Модифікатори деталей (крила, парашут, великий, ключ)» · levels/editor · 🥈 · слот {modifiers: list}.
  - `+part-variants` «Варіанти деталі (трусанути/меню)» · levels/editor · 📎.
  - `+container-part` «Деталь у деталі (блок, труба, гармата)» · entities/spawn · 🥈.
  - `+clear-condition` «Додаткова умова перемоги з N» · game-logic/win · 📎.
  - `+level-share-code` «Код рівня для обміну» · levels/editor · 📎 — родич `+seed-share`.
  - `+sub-area-link` «Підзона, звʼязана входом» · levels/format · 🥉.
  - `+liquid-level` «Рівень рідини, що росте/спадає» · entities/interact · 📎.
  - `+random-level-run` «Низка випадкових рівнів з життями» · levels/bank · 📎 (Endless/100 Mario).
  - `+world-map` «Мапа світу з вузлами-рівнями» · levels/progression · 🥉 — World Maker.
  - `+ghost-run` «Привид найкращого проходження» · interface/results · 🥈.

## Пропозиції до словників
- `+feature:level-editor`, `+feature:level-sharing`, `+feature:user-levels-browser`, `+feature:level-rating`, `+feature:ghost-run`, `+feature:mode-endless` — усі вже ⏳ у `features.md`; SMM2 — еталон для них.
- `+window:editor-window` (еталон), `+window:course-browser` (каталог чужих рівнів з фільтрами), `+window:part-menu` (меню властивостей вибраної деталі), `+window:upload-dialog` (публікація з перевіркою), `+window:comment-board` (коментарі з малюнками).
- `+ui:tool-palette`, `+ui:element-picker` (смуга останніх деталей + колесо), `+ui:clear-rate` (відсоток проходжень), `+ui:like-boo-buttons`.
- `+effect:attach(a, b)` (є ⏳) — вкладення деталі в контейнер; `+effect:set_state` — ON/OFF перемикання.
- `+cond:clear_condition` — умова на фініші (зібрано N / без дії X / у формі Y).
- `+axis:session` — `level` для курсів, `endless` для Endless Challenge.
- `+card:part-modifiers`, `+card:clear-condition`.

## Джерела
- ⭐ [Super Mario Wiki: Super Mario Maker 2](https://www.mariowiki.com/Super_Mario_Maker_2) — теми, нічні версії, Custom Scroll, легенда модифікаторів (гриб, крила, парашут, ключ, стек, у трубу/блок/гармату, Lakitu, пілот, дерево, рейка, прапорець), список деталей Terrain/Items/Enemies/Gizmos, Course World (like/boo, штампи, фільтри, ID 9 символів), Maker points, Versus Rating, Endless (життя за складністю), Story Mode.
- [Wikipedia: Super Mario Maker 2](https://en.wikipedia.org/wiki/Super_Mario_Maker_2) — 5 стилів, 3D World «extra», кооп-редагування, онлайн 4 гравці, World Maker (6/1, 8 світів × 5), оновлення (Ninji Speedruns, ON/OFF).
- [Wikipedia: Super Mario Maker](https://en.wikipedia.org/wiki/Super_Mario_Maker) — стек ворогів, гриб/крила, вміст блоків і труб, публікація лише після проходження, 100/10 Mario Challenge, розблокування деталей, Soundfrog.
- [Super Mario Wiki: Undodog](https://www.mariowiki.com/Undodog) — Undodog як кнопка undo, Reset Rocket, Mr. Eraser, Coursebot.
- [Super Mario Wiki: Clear Condition](https://www.mariowiki.com/Clear_Condition) — категорії умов Actions/Parts/Status/Other.
- YouTube: пошук «super mario maker 2 course maker tutorial».

## Непевне
- (?) Ліміти деталей на зону (кількість ground, ворогів тощо) і максимальна довжина курсу — не перевірено.
- (?) Multigrab, копіювання, redo в SMM2 — з памʼяті; Undodog у SMM2 описаний лише сюжетно.
- (?) Повний список clear conditions і чи перевіряються вони на воротах (ворота «не пускають» чи кліринг не зараховано).
- (?) Ліміт аплоадів (32→64→100), пороги кліринг-рейту для тирів складності, ліміт 2 чекпойнтів.
- (?) Ефекти нічних тем, крім отруйної води в Forest.
- `info: full` і `random: none` — для редактора/курсу; Endless Challenge додає випадковість вибору курсів (`setup`).
