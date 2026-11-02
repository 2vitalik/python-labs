---
title: Chip's Challenge
slug: chips-challenge
family: maze-arcade
also: [push-slide]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1989
platforms: [Lynx, Windows (Microsoft Entertainment Pack 4), Steam (2015)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Chip%27s_Challenge", note: "історія, версії, правила коротко"}
  - {kind: fandom, url: "https://bitbusters.club/wiki/", best: true, note: "Bit Busters Wiki — повний довідник плиток, монстрів, відмінностей MS/Lynx"}
  - {kind: steam, url: "https://store.steampowered.com/app/346850/Chips_Challenge_1/", note: "безкоштовна офіційна версія"}
  - {kind: play, url: "https://www.chuckschallenge.com/", note: "спадкоємець від Chuck Sommerville"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=chip%27s+challenge+gameplay+windows", note: "пошук; геймплей MS-версії"}
  - {kind: official, url: "https://tw2.bitbusters.club/", note: "Tile World 2 — відкритий емулятор обох наборів правил"}
stage: v2
coverage: 85
mechanics: [move-4dir, impassable-cells, floor-types, key-and-door, push-object, inventory-items, item-pickup, collect-quota, reach-exit, time-out, touch-death, environment-death, teleport-pair, cell-transform, level-from-txt, level-select, score-records, event-points, time-bonus, game-pause, music-toggle, help-window, splash-screen, inertia-slide, +wall-follower, +turn-when-blocked, +bounce-move, +button-toggle, +clone-machine, +trap-release, +popup-wall, +fake-wall, +thief, +hint-tile, +level-password, +permit-item]
proposes: ["+trigger:enter", "+cond:has", "+effect:slide", "+effect:set_cell", "+effect:take", "+effect:message", "+effect:set_state", "+role:terrain", "+role:switch", "+role:gate", "+role:spawner", "+window:level-password", "+ui:inventory-bar", "+ui:hint-text", "+feature:level-password", "+axis:control"]
author: fable
date: 2026-11-02
---

# Chip's Challenge — лабіринт-енциклопедія: збери чипи, пройди крізь розетку до виходу

## Суть
Чіп бігає по лабіринту 32×32, збирає компʼютерні чипи, щоб відкрити розетку перед виходом, і виживає серед води, вогню, льоду, конвеєрів, дверей з ключами й монстрів із жорсткими патернами. Кожен рівень — комбінація з ~40 типів плиток; саме розмаїття взаємодій «плитка × Чіп × монстр × блок» зробило гру еталоном клітинної механіки (T32: «енциклопедія клітинних механік»). 149 рівнів, кожен має 4-літерний пароль.

## Поле і час
- Поле 32×32 клітини, видно вікно 9×9 навколо Чіпа (камера слідує). Клітина має **два шари**: верхній (обʼєкт/монстр/блок) і нижній (плитка підлоги) — блок на льоду, монстр на кнопці.
- Real-time: Чіп ходить з фіксованою швидкістю (MS: 5 клітин/с), монстри — своїм тіком; Teeth ходить через такт. Таймер рівня в секундах (бувають рівні без ліміту).
- Два канонічні набори правил — **MS** (Windows 1992) і **Lynx** (1989): відрізняються порядком ходів монстрів, «бустами» на льоду, поведінкою блоків. Tile World емулює обидва.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чіп | player | 1 життя на спробу | рух 4 напрямки, штовхає блоки, збирає предмети |
| Чип (IC) | pickup | — | збирається, зменшує лічильник «Chips Left» |
| Розетка (socket) | gate | потрібно chips_left = 0 | пропускає лише коли всі чипи зібрані; зникає |
| Вихід | static | — | перемога рівня |
| Стіна | static | — | непрохідна для всіх |
| Тонка стіна (panel) | static | сторона N/S/E/W/SE | блокує рух лише через ребро клітини |
| Невидима стіна | static | постійна / «проявна» | блокує; проявна показується на мить після дотику |
| Синя стіна | static | справжня / фальшива | дотик: фальшива → підлога, справжня → звичайна стіна |
| Popup-стіна | terrain | — | пройти можна раз, потім стає стіною |
| Вода | terrain | — | без ласт — смерть; блок у воду → земля |
| Вогонь | terrain | — | без вогнетривких черевиків — смерть; більшість монстрів не входить |
| Лід (+ кути) | terrain | 4 кутові варіанти | ковзання до упору; кут повертає на 90°; ковзани скасовують |
| Силова підлога | terrain | напрям N/S/E/W або random | тягне в напрямку; присоски скасовують |
| Земля (dirt) | terrain | — | Чіп входить → стає підлогою; монстри не входять |
| Гравій | terrain | — | підлога, куди монстри не входять |
| Блок (dirt block) | object | — | штовхається на 1; у воду → земля; на льоду ковзає |
| Двері ×4 кольори | gate | колір | відкриваються ключем того ж кольору |
| Ключ ×4 кольори | pickup | колір | синій/червоний/жовтий витрачаються; зелений — вічний |
| Ласти · вогнетривкі черевики · ковзани · присоски | pickup | «дозвіл» на тип підлоги | дають прохід/скасовують ефект плитки |
| Злодій | enemy (static) | — | забирає всі черевики при контакті |
| Бомба | hazard | — | Чіп → смерть; монстр/блок → бомба й монстр зникають |
| Пастка | terrain | звʼязана з коричневою кнопкою | тримає того, хто став, доки кнопка не натиснута |
| Коричнева кнопка | switch | → пастка | звільняє пастку |
| Зелена кнопка | switch | → усі toggle-стіни | перемикає відкрито/закрито |
| Toggle-стіна | gate | стан open/closed | стіна або підлога залежно від стану |
| Червона кнопка | switch | → клон-машина | машина випускає копію того, що на ній стоїть |
| Клон-машина | spawner | що на ній | породжує сутність у напрямку її погляду |
| Синя кнопка | switch | → усі танки | розвертає танки |
| Телепорт | terrain | ланцюг у порядку скану | переносить на наступний телепорт, що має вихід |
| Підказка (hint) | terrain | текст | показує текст у панелі, доки стоїш |
| Жук (bug) | enemy | — | іде вздовж стіни ліворуч |
| Парамеція | enemy | — | іде вздовж стіни праворуч |
| Вогняна куля | enemy | — | прямо; впершись — повертає праворуч |
| Планер (glider) | enemy | — | прямо; впершись — повертає ліворуч |
| Рожева куля | enemy | — | туди-сюди, відбивається від перешкод |
| Танк | enemy | напрям | прямо до упору, стоїть; синя кнопка розвертає |
| Зуби (teeth) | enemy | ходить через такт | жадібна погоня за Чіпом |
| Ходок (walker) | enemy | — | прямо; впершись — випадковий поворот |
| Крапля (blob) | enemy | — | випадковий крок кожного ходу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `contact(chip, ic)` → ТО `pickup`, `counter(chips_left, -1)`.
- КОЛИ `contact(chip, socket)` → ЯКЩО `counter(chips_left, ==, 0)` → ТО `disappear_b`; інакше `block`.
- КОЛИ `contact(chip, exit)` → ТО `win`, `score(level×500 + time_left×10)`, `next_level`.
- КОЛИ `enter(chip, water)` → ЯКЩО `not has(chip, flippers)` → ТО `lose` («Chip can't swim without flippers»).
- КОЛИ `enter(chip, fire)` → ЯКЩО `not has(chip, fire_boots)` → ТО `lose`.
- КОЛИ `enter(a, ice)` → ЯКЩО `not has(a, skates)` → ТО `slide(a, dir)`; на куті — `face(a, turn90)` і далі ковзання.
- КОЛИ `enter(a, force_floor)` → ЯКЩО `not has(a, suction)` → ТО `move(a, floor_dir)` щотік; `random` варіант — `move(a, rng_dir)`.
- КОЛИ `contact(chip, door[c])` → ЯКЩО `has(chip, key[c])` → ТО `disappear_b`, `take(chip, key[c])` (зелений — без `take`); інакше `block`.
- КОЛИ `contact(chip, block)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `enter(block, water)` → ТО `disappear_a`, `set_cell(dirt)`.
- КОЛИ `enter(chip, dirt)` → ТО `set_cell(floor)`.
- КОЛИ `contact(chip, thief)` → ТО `take(chip, all_boots)`.
- КОЛИ `contact(chip, bomb)` → ТО `lose`; КОЛИ `contact(monster|block, bomb)` → ТО `disappear_both`.
- КОЛИ `contact(chip, blue_wall)` → ЯКЩО `state(fake)` → ТО `set_cell(floor)`; інакше `set_cell(wall)`, `block`.
- КОЛИ `leave(chip, popup_wall)` → ТО `set_cell(wall)`.
- КОЛИ `contact(any, green_button)` → ТО `set_state(toggle_walls, flip)`.
- КОЛИ `contact(any, red_button)` → ТО `spawn(clone_of(entity_on_machine))` у напрямку машини.
- КОЛИ `contact(any, brown_button)` → ТО `clear_state(trap, holding)`.
- КОЛИ `enter(a, trap)` → ТО `set_state(a, trapped)` доки кнопка.
- КОЛИ `contact(any, blue_button)` → ТО `face(tank, reverse)` для всіх танків.
- КОЛИ `enter(a, teleport)` → ТО `teleport(a, next_in_scan_order)`; нема вільного виходу → виходить назад.
- КОЛИ `enter(chip, hint)` → ТО `message(hint_text)`; `leave` → ховає.
- КОЛИ `contact(chip, monster)` → ТО `lose`.
- КОЛИ `enter(monster, fire|dirt|gravel)` → ТО `block` (крім вогняної кулі у вогні).
- Монстри (щотік): жук/парамеція — `custom: «тримайся стіни ліворуч/праворуч»`; вогняна куля/планер — `blocked(a)` → `face(a, right|left)`; рожева куля — `blocked(a)` → `face(a, reverse)`; танк — `blocked(a)` → `custom: «стоїть»`; зуби — `chase-greedy` через такт; ходок — `blocked(a)` → `face(a, rng)`; крапля — `move(a, rng_dir)`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `lose` («Ooops! Out of time!»).
- Поразка: смерть від монстра/води/вогню/бомби/часу → діалог → рівень з початку. Рахунок: за рівень `level×500 + 10×секунда, що лишилась`; найкращий час рівня зберігається.

## Керування і ввід
- Стрілки — рух на одну клітину (утримання — біг); миша (MS) — клік по клітині: Чіп іде найкоротшим шляхом.
- Pause (MS: клавіша/меню), Restart рівня, Next/Previous level (пройдені або за паролем).
- Жодного drag/курсора: чистий аватар.

## Вікна, меню, HUD
- `splash-screen` — титул «Chip's Challenge».
- `game-screen` — поле 9×9 + права панель: `level-number`, `timer-countdown` (`---` без ліміту), `remaining-counter` «Chips Left», `inventory-bar` 4×2 (ключі з кількістю, черевики), `hint-text` (текст підказки, доки стоїш на плитці).
- `level-password` (MS «Go To Level»): номер рівня + 4-літерний пароль; відкриває будь-який рівень, якщо пароль вірний.
- `leaderboard` «Best Times» — таблиця найкращих часів по рівнях.
- `end-screen`-діалоги: смерть (текст причини + «Try again»), рівень пройдено (очки за рівень, бонус за час, разом), «decade»-повідомлення кожні 10 рівнів, фінал після 149-го.
- `pause-menu` — простий модал «Paused».
- Меню-бар MS: Game (New Game, Pause, Best Times, Go To Level, Exit) · Options (Background Music, Sound Effects, Color/Black & White) · Help (`help-window` з правилами і плитками, `about-window`).
- Переходи: splash → game-screen; game-screen → (смерть) діалог → game-screen того ж рівня; game-screen → (вихід) діалог рахунку → game-screen наступного рівня; Game→Go To Level → level-password → game-screen.

## Фічі поза полем
- `level-password` + `levels-sequential` + `continue` (MS зберігає найвищий відкритий рівень і паролі в ini) — прогресія без «карти світу».
- `leaderboard-local` найкращих часів; `par-target` неявно (час = очки).
- `pause`, `restart-level`, `sound-toggle`, `music-toggle`, режим чорно-білий (доступність/старі монітори).
- Нема undo, hint-кнопки, редактора у MS; спільнота зробила **CCLP** (рівень-паки), редактор ChipEdit, Tile World з вибором правил MS/Lynx — приклад `custom-rules` (набір правил як налаштування).
- Chip's Challenge 2 (2015): редактор, нові плитки (залізниця, бонуси часу, ліфти), два персонажі — Чіп і Мелінда.

## Варіації й родичі
- Набори правил MS vs Lynx — одна гра, дві «фізики» (порядок ходів, бусти з льоду, блоки з телепортами). Вісь: **чи є у грі офіційні альтернативні набори правил**.
- Chuck's Challenge 3D — ті самі ідеї в 3D; Chip's Challenge 2 — розширення словника плиток.
- Родичі за механіками: Adventures of Lolo (блоки-щити, ворог стріляє по лінії), Kwirk (турнікети/дірки), DROD (детерміновані монстри з правилами руху), Sokoban (штовхання), Tomb of the Mask (ковзання до упору як основа).
- Осі варіацій, які видно на цій одній грі: монстр ↔ стіна: «тримається лівої / правої / повертає праворуч / ліворуч / розвертається / випадково / стоїть» — сім значень однієї осі «що робить ворог, впершись».

## Цікавинки для курсу
- Типи підлоги як **окремий шар** клітини (лід, вода, вогонь, конвеєр) + черевики-«дозволи», що скасовують ефект — 🥈 (два шари поля + інвентар дозволів).
- Сімейство «впершись → поворот» для ворогів: 7 поведінок із одного параметра — 🥉 за сімʼю, кожна дитина 📎.
- Кнопка → пара-ціль (toggle-стіни, клон-машина, пастка, танки): одна механіка `switch→target` з 4 видами наслідків — 🥈.
- Блок у воду → земля: трансформація клітини наслідком взаємодії двох сутностей — 📎 (картка `cell-transform` є).
- Пароль рівня як прогресія без збереження стану — 🌱, але гарний приклад вікна.
- Два набори правил як налаштування гри (MS/Lynx) — 🥇, якщо студент реалізує обидві поведінки за перемикачем.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` (стіни, тонкі стіни) · `floor-types` (лід/вода/вогонь/силова) · `key-and-door` · `push-object` · `inventory-items` (черевики, ключі) · `item-pickup` · `collect-quota` (чипи → розетка) · `reach-exit` · `time-out` · `touch-death` · `environment-death` · `teleport-pair` · `cell-transform` · `inertia-slide` (лід) · `level-select` + `score-records` + `time-bonus` + `event-points` · `game-pause` · `music-toggle` · `help-window` · `splash-screen`.
- **Нема** → пропозиції карток:
  - `+wall-follower` «Ворог тримається стіни» · entities/move · 🥉 · слот {side: left|right} — жук/парамеція.
  - `+turn-when-blocked` «Поворот при упорі» · entities/move · 📎 · слот {turn: left|right|reverse|random|stop} — куля/планер/рожева куля/ходок/танк (сімʼя з `enemy-patrol`).
  - `+button-toggle` «Кнопка перемикає стан цілей» · entities/interact · 🥉 · слот {targets: text} — зелена кнопка/toggle-стіни, синя/танки.
  - `+clone-machine` «Клон-машина за кнопкою» · entities/spawn · 🥉 — спавн копії при натисканні.
  - `+trap-release` «Пастка і кнопка звільнення» · entities/interact · 📎.
  - `+popup-wall` «Прохід один раз» · entities/legality · 🌱.
  - `+fake-wall` «Стіна-обманка» · entities/legality · 🌱 · слот {reveal: on_touch|never}.
  - `+thief` «Злодій забирає предмети» · entities/interact · 📎.
  - `+hint-tile` «Клітина-підказка» · interface/hud · 🌱.
  - `+permit-item` «Предмет-дозвіл на тип підлоги» · entities/state · 📎 — черевики як скасування ефекту (дитина `inventory`).
  - `+level-password` «Вхід на рівень за паролем» · interface/menus (#window) · 🌱.

## Пропозиції до словників
- `+trigger:enter` — сутність стала на клітину типу (лід, вода, силова підлога); відрізняється від `contact`, бо друга сторона — плитка-шар, а не сутність.
- `+cond:has` — у сутності є предмет (черевики, ключ кольору).
- `+effect:slide` — ковзати до упору (лід); `+effect:set_cell` — змінити тип клітини (земля → підлога, popup → стіна); `+effect:take` — забрати предмет (двері витрачають ключ, злодій — черевики); `+effect:message` — текст у панелі (підказка); `+effect:set_state` — стан toggle-стін/пастки/розвороту.
- `+role:terrain` (лід, вода, конвеєр — на ній стоять), `+role:switch` (кнопки), `+role:gate` (двері, розетка, toggle-стіна), `+role:spawner` (клон-машина).
- `+window:level-password` — екран введення пароля рівня; `+ui:inventory-bar` — сітка предметів у HUD; `+ui:hint-text` — текстова панель підказки на екрані гри.
- `+feature:level-password` — прогресія паролями.
- `+axis:control` — тут `direct` (стрілки) і `indirect` (клік мишею → автошлях) одночасно: одна гра, два режими керування.

## Джерела
- ⭐ [Bit Busters Wiki](https://bitbusters.club/wiki/) — довідник усіх плиток і монстрів із відмінностями MS/Lynx, рівні, паролі, спільнота.
- [Wikipedia](https://en.wikipedia.org/wiki/Chip%27s_Challenge) — версії, історія, 149 рівнів, Chuck Sommerville.
- [Steam: Chip's Challenge 1](https://store.steampowered.com/app/346850/Chips_Challenge_1/) — безкоштовне перевидання (Lynx-правила).
- [Tile World 2](https://tw2.bitbusters.club/) — відкритий емулятор з обома наборами правил і редактором.
- YouTube: пошук «chip's challenge gameplay windows» — геймплей MS-версії з панеллю інвентаря.

## Непевне
- (?) Точна формула очок MS (`level×500 + 10×time_left`) — з памʼяті про MS-версію; у Lynx рахунок інший.
- (?) Швидкість Чіпа 5 клітин/с і «через такт» для Teeth — MS-правила; у Lynx тайминги відрізняються.
- (?) Порядок пошуку виходу з телепорта (зворотний порядок читання карти) — перевірити на Bit Busters.
