---
title: Wizard's Way Out
slug: wizards-way-out
aka: ["Wizard's Way Out - Free Version"]
family: push-slide
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2023
platforms: [PC (Windows, Linux), web (безкоштовна версія 2021)]
links:
  - {kind: play, url: "https://kikimora.itch.io/wizards-way-out-free", best: true, note: "безкоштовна версія 2021 у браузері (13 рівнів, лише миша); опис, коментарі про кнопку HELP"}
  - {kind: itch, url: "https://kikimora.itch.io/wizards-way-out", note: "розширена версія 2023 (Godot): опис, керування мишею / клавіатурою / геймпадом, девлоги"}
  - {kind: steam, url: "https://store.steampowered.com/app/2341410/Wizards_Way_Out/", note: "опис («push things away… pull things toward you»), 15 досягнень, трейлери Trailer і Confidence Update"}
  - {kind: other, url: "https://kikimora.itch.io/wizards-way-out/devlog/736526/are-you-feeling-confident-wizards", note: "Confidence Update 2024: проходження без ідеалу, «впевненість», клік по клітині, екран рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=8JooBP_yvVM", note: "проходження безкоштовної версії (LogixGenic), вбудоване на itch-сторінці"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=4A_8TK7qaDw", note: "трейлер Undo Update (Kikimora Games)"}
stage: v1
coverage: 60
mechanics: [move-4dir, cell-click, hover-highlight, keyboard-controls, push-object, pull-object, crush-by-slide, interaction-table, impassable-cells, environment-death, fill-hole, key-and-door, drop-on-death, destroy-all-enemies, move-limit, undo-redo, restart-level, sequential-levels, level-select, level-unlock, save-autosave, +remote-push, +remote-pull, +sleeping-enemy, +wake-on-event, +weight-classes, +hint-reveal, +auto-pathfind-command, +star-gate-unlock]
proposes: ["+ui:outcome-preview", "+feature:mastery-gate", "+axis:control"]
author: opus
date: 2026-11-19
---

# Wizard's Way Out — недовчений чарівник телекінезом штовхає й тягне урни, ключі та сплячих вартових, доки не скінчились дії

## Суть
Чарівник, що впав у колодязь, мусить пройти кімнати підземної вʼязниці, де сплять вартові. Телекінез діє на обʼєкт на одній лінії з чарівником на будь-якій відстані: його можна відштовхнути або притягнути, вбивши ним вартового, скинувши вартового в яму чи вкинувши ключ у двері-вартового. Кожен крок, поштовх і притягування — дія з обмеженого запасу кімнати: дії скінчились, а варта ще є — вона прокидається.

## Поле і час
- Дві версії: безкоштовна 2021 (Unity, 13 рівнів, лише миша) і розширена 2023 (Godot, рівнів «більш ніж удвічі» більше, клавіатура й геймпад).
- Квадратна сітка кімнати (`Grid`, `TileManager` у коді), камера центрує кімнату; клітини — підлога, стіни, ями.
- Хід = одна дія чарівника (крок, поштовх або притягування); вартові сплять і самі не рухаються, тож світ змінюється лише від дій гравця.
- Запас дій на кімнату видно в HUD; разом із ним — скільки лишилось ворогів, ключів і замків (`ActionsLeft`, `EnemiesLeft`, `KeysLeft`, `LocksLeft`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чарівник | player | вага гравця | крок на сусідню клітину; штовхає й тягне телекінезом обʼєкт на своїй лінії |
| Ratbug | ally | — | друг-оповідач у діалогах; його рій «подбає про ключі, які впускають вартові»; в епілозі — сюжетний поворот |
| Урна (глиняний глек) | object | легка | перший снаряд навчання: штовхнута у сплячого вартового, виводить його; звуки «ціла / розбилась» (?) |
| Важкий шипастий обʼєкт | object | важкий | «big, heavy… thing», може бути «просто на дорозі»; падає в яму (?) |
| Камʼяний блок (stop block) | object | масивний | зупиняє ковзний ключ у потрібному місці; є звук «тягнеться» — мабуть, теж рухається телекінезом (?) |
| Великий ключ | object | — | рухається телекінезом; влучивши в двері-вартового, відмикає їх |
| Вартовий | enemy | спить / потривожений / прокинувся; вага | рухається телекінезом; гине від удару, падає в яму |
| Вартовий-ключник | enemy | несе ключ | при загибелі лишає ключ (?) |
| Вартовий з рукою (hand guard) | enemy | тіло під ямою | телекінезом не рухається |
| Двері-вартовий | gate | замкнено / відімкнено | єдиний вихід із кімнати; «нагодуй великим ключем» |
| Важкий / масивний вартовий | enemy | вага heavy / massive | (?) інша реакція на удари й телекінез |
| Яма (pitfall) | terrain | — | що впало — гине; частина обʼєктів засипає яму (`PitfallDieAndFillBehaviour`) |
| Стіна | static | — | зупиняє рух і лінію телекінезу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(step, dir)` → ЯКЩО `free(next_cell)` → ТО `move(wizard, dir)`, `counter(actions, -1)`.
- КОЛИ `input(push, target)` → ЯКЩО `line_of_sight(wizard, target)` → ТО `slide(target, away)`, `counter(actions, -1)` — дальності нема, але треба стояти на одній лінії з ціллю.
- КОЛИ `input(pull, target)` → ЯКЩО `line_of_sight(wizard, target)` → ТО `pull(target)`, `counter(actions, -1)`.
- КОЛИ `input(push, hand_guard)` → ТО `block` — тіло під ямою, не зрушити ні штовханням, ні притягуванням.
- КОЛИ `contact(urn, guard)` → ЯКЩО `state(guard, asleep)` → ТО `disappear_b` — вартового виведено; чи розбивається при цьому урна — (?).
- КОЛИ `contact(guard, guard)` → ТО `custom: «удар вартовим об вартового — вартового виведено»` (?).
- КОЛИ `enter(guard, pit)` → ТО `fall(guard)`, `disappear_a` — «bottomless pit».
- КОЛИ `enter(heavy_object, pit)` → ТО `fall(heavy_object)`, `set_cell(pit, floor)` (?).
- КОЛИ `died(key_guard)` → ТО `spawn(key)` (?).
- КОЛИ `contact(key, stop_block)` → ТО `block` — ключ зупиняється перед блоком.
- КОЛИ `contact(key, door_guard)` → ТО `unlock(door)`, `disappear_a`.
- КОЛИ `counter(actions, ==, 0)` → ЯКЩО `count(guard, >, 0)` → ТО `set_state(guard, awoken)`, `lose` — «One step, push or pull too many and they'll wake right up».
- КОЛИ `all_gone(guard)` → ЯКЩО `custom: «двері-вартовий відімкнені, якщо вони є»` → ТО `win`, `next_level`.
- КОЛИ `input(hover, wizard|object)` → ТО `custom: «підсвітити доступні дії і їхні наслідки: знищить, буде знищено, впаде, засипле яму, відімкне, штовхне»`.
- КОЛИ `input(help)` → ТО `message(level_hint)`.
- КОЛИ `input(undo)` → ТО `undo`.
- КОЛИ `input(restart)` → ТО `restart`.
- КОЛИ `level_end` → ЯКЩО `custom: «рівень пройдено бездоганно»` → ТО `counter(confidence, +1)` — Steam-версія з 2024; останній рівень відкривається лише з повною «впевненістю».
- Перемога: кімнату очищено від варти (і відімкнено двері) до кінця дій. · Поразка: дії скінчились — варта прокидається («They Have Awoken…»). · Рахунок: нема; з 2024 — позначки «пройдено / опановано».

## Керування і ввід
- Безкоштовна версія: лише миша («One button»): навести на чарівника — видно доступні кроки; навести на підсвічений обʼєкт — доступні поштовх / притягування з підказками наслідків; клік — дія.
- Розширена версія: миша, повна клавіатура або геймпад; з 2024 — клік по будь-якій клітині, і чарівник іде найкоротшим шляхом.
- Undo (у безкоштовній — з v1.2.0, замість кнопки «міні-рестарту»), рестарт (меню паузи; у 2023 — окрема кнопка), HELP у правому нижньому куті.

## Вікна, меню, HUD
- `splash-screen` / екран завантаження з Ratbug.
- `main-menu` — грати, налаштування, «Brain Wipe» (стерти збереження).
- `level-select` — кнопки рівнів; із 2024 — усі рівні внизу екрана зі станами «пройдено / опановано / закрито»; закриті потребують N пройдених (`LevelsRequiredToUnlock`).
- `game-screen` — кімната; HUD: `action-points` (дії, що лишились), `remaining-counter` (вороги, ключі, замки), `level-number` (з 2023), кнопки undo, HELP, пауза; при наведенні — значки-наслідки дії.
- `dialogue-window` — портрети Wizard / RatBug, діалоги до й після кожного рівня; швидкість тексту Slow / Medium / Fast / Instant.
- `hints-window` (HELP) — текст-підказка рівня: «Every action counts…», «Doing things in a different order can make a big difference…».
- `pause-menu` — рестарт рівня; `settings-window` — роздільність, швидкість тексту, film grain, тряска екрана, сховати підказки кнопок, титри за 3 с.
- `end-screen` — «рівень пройдено» → одразу наступний (з v1.1.0); `credits-window` і епілог оповідача.
- Переходи: меню → вибір рівня → діалог → кімната → (очищено) діалог → наступна кімната; (дії скінчились) → поразка → undo / рестарт.

## Фічі поза полем
- `undo`, `restart-level`, `hint` (одна текстова підказка на рівень), `autosave` після кожного рівня (браузер теж), стирання прогресу.
- `levels-sequential` + `level-unlock`; з 2024 — `+feature:mastery-gate`: рівень можна пройти неідеально, опановані рівні піднімають «впевненість», а фінал вимагає повної.
- `achievements` (Steam, 15: «Pulled A Thing!», «Mastered 30 Levels!», «They Have Awoken…»), `gamepad-support`, `mouse-and-keyboard`, `one-hand-mode` (гра однією кнопкою миші).

## Варіації й родичі
- [RPG dungeon puzzle rooms](rpg-dungeon-puzzle-rooms.md) — Move з Golden Sun: штовхання здалеку здібністю.
- [Helltaker](helltaker.md) — бюджет ходів і вороги, яких прибирають штовханням; [Slayaway Camp](slayaway-camp.md), [The Brainies](the-brainies.md) — рух до першої перешкоди, удар — наслідок.
- [Hitman GO](hitman-go.md), [Adventures of Lolo](adventures-of-lolo.md) — варта як головоломка, а не бій.
- Осі варіацій:
  - **як діє гравець на обʼєкт**: впритул (Sokoban) / на лінії без дальності (тут) / тягнути (тут, Pull);
  - **ціна дії**: безкоштовно / бюджет ходів на кімнату (тут, Helltaker);
  - **що робить ворог**: ходить / спить, поки є дії (тут) / прокидається від шуму поруч.

## Цікавинки для курсу
- Телекінез по лінії: знайти обʼєкти на рядку й стовпці чарівника без перешкод між ними й рух до першої перешкоди — 📎.
- Таблиця зіткнень за вагою (легке / важке / масивне × обʼєкт / вартовий / стіна / яма: хто зникає, хто зупиняється, хто засипає яму) — 🥉 (картка `interaction-table`).
- Попередній перегляд наслідку при наведенні: прогнати дію на копії стану й показати значки — 🥉.
- Бюджет дій як таймер поразки — 🌱; «впевненість» як допуск до фіналу — 🌱.
- Клік по клітині → BFS-шлях, кожен крок — дія — 📎.
- Розвʼязувач: BFS по станах (чарівник, обʼєкти, живі вартові) з обмеженням на кількість дій — 🥈.

## Мапа на каталог
- Є: `move-4dir`; `cell-click` + `hover-highlight` ↔ керування мишею; `keyboard-controls`; `push-object` + `pull-object` ↔ телекінез; `crush-by-slide` ↔ урна чи вартовий у вартового; `interaction-table` ↔ реакції за вагою; `impassable-cells`; `environment-death` ↔ яма; `fill-hole` ↔ «PitfallDieAndFill»; `key-and-door` ↔ ключ і двері-вартовий; `drop-on-death` ↔ ключ з ключника (?); `destroy-all-enemies` ↔ очистити кімнату; `move-limit` ↔ запас дій; `undo-redo`, `restart-level`; `sequential-levels`, `level-select`, `level-unlock`; `save-autosave`.
- **Нема** → пропозиції карток:
  - `+remote-push` (є в корпусі) і `+remote-pull` «Притягнути обʼєкт здалеку по лінії» · entities/interact · 📎.
  - `+sleeping-enemy`, `+wake-on-event` (є в корпусі) — тут подія = кінець бюджету дій.
  - `+weight-classes` «Класи ваги визначають наслідок зіткнення» · entities/state · 🥉 · слот {classes: light|heavy|massive}.
  - `+hint-reveal` (є в корпусі) — тут текстова підказка, а не хід; `+auto-pathfind-command` (є в корпусі); `+star-gate-unlock` (є в корпусі) — фінал за кількістю опанованих рівнів.

## Пропозиції до словників
- `+ui:outcome-preview` — значки наслідку дії при наведенні (знищить / впаде / засипле яму / відімкне), до того як гравець її зробить.
- `+feature:mastery-gate` — рівень можна пройти «абияк», але фінал відкривається лише за опанування решти.
- `+axis:control` — тут `indirect` (клік по клітині → шлях) і `direct` (клавіатура, геймпад) в одній грі.

## Джерела
- ⭐ [itch.io: Free Version](https://kikimora.itch.io/wizards-way-out-free) — гра в браузері (Unity, v1.2.0), опис, «Mouse input», коментарі про кнопку HELP і рівні 5, 8, 12; тексти діалогів, підказок і назви класів — з її даних (`.data` збірки), не з геймплею.
- [itch.io: Wizard's Way Out](https://kikimora.itch.io/wizards-way-out) — розширена версія (Godot), девлоги 2023–2024: рівень видно на екрані, кнопка рестарту, швидкість тексту, Confidence Update.
- [Steam](https://store.steampowered.com/app/2341410/Wizards_Way_Out/) — опис, 15 досягнень, новини (те саме, що девлоги, плюс «The well bottom, it has widened?» — новий перший рівень із прийомами телекінезу).
- [Devlog Confidence Update](https://kikimora.itch.io/wizards-way-out/devlog/736526/are-you-feeling-confident-wizards) — «впевненість», клік по клітині, екран рівнів.
- [Проходження безкоштовної версії](https://www.youtube.com/watch?v=8JooBP_yvVM) і [трейлер Undo Update](https://www.youtube.com/watch?v=4A_8TK7qaDw) — не переглядав, назви звірено.

## Непевне
- (?) Чи штовхнутий обʼєкт летить до упору: так підказують «use a stop block to stop that key» і поля `continueMoving` / `nextPosition` у коді; притягнутий — чи зупиняється біля чарівника.
- (?) Хто кого знищує при зіткненні: у коді є легка / важка / масивна вага, «руйнівне» й «неруйнівне» зіткнення, `DestroyOtherOnImpact` — таблицю наслідків не бачив.
- (?) Як саме прокидається варта: лише на нулі дій чи раніше (стан «disturbed» між сном і пробудженням).
- (?) Що таке «бездоганне» проходження в Steam-версії (мінімум дій?) і скільки там рівнів: «більш ніж удвічі» від 13, досягнення «Mastered 30 Levels!» натякає на ≥ 30.
- (?) Чи всі механіки безкоштовної (Unity) збереглись у платній (Godot); описано за безкоштовною й описом Steam.
- (?) Рядок черги каже «оминаючи сплячу варту» — за грою варту треба прибрати всю («Rooms need to be cleared of enemies before they wake up»).
