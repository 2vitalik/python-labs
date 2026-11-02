---
title: Repton 1–3
slug: repton
family: dig-gravity
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1985
platforms: [BBC Micro, Acorn Electron, C64, PC, RISC OS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Repton_(video_game)", best: true, note: "уся серія: Repton 1, 2, 3, add-on набори, Infinity з мовою Reptol"}
  - {kind: fandom, url: "https://8bs.com/elecgame/repton_3.htm", note: "оригінальна інструкція Repton 3: елементи, клавіші, очки, редактор"}
  - {kind: fandom, url: "https://www.reptonresourcepage.co.uk/AboutRepton.php", note: "Repton Resource Page: правила скочування, статистика Repton 2, очки"}
  - {kind: wiki, url: "https://acornelectron.co.uk/info/electron/superior/Repton-3.html", note: "архів Superior Software: Repton 3"}
  - {kind: play, url: "https://c64.krissz.hu/repton-3/play-online/", note: "Repton 3 (C64) у браузері"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=repton+3+bbc+micro+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, gravity-fall, push-object, collect-all, time-out, touch-death, environment-death, player-death, key-and-door, chase-player, chase-greedy, teleport, item-pickup, event-points, sequential-levels, in-game-editor, editor-palette, player-camera, minimap-radar, cheat-codes, +dig-terrain, +roll-off-rounded, +wall-follower, +blob-growth, +level-password]
proposes: ["+trigger:enter", "+trigger:counter", "+cond:state", "+cond:free", "+effect:fall", "+effect:roll", "+effect:spread", "+effect:timer", "+role:container", "+role:spawner", "+role:terrain", "+role:hazard", "+card:egg-hatch", "+card:lure-to-goal", "+card:teleport-single-use", "+card:timer-reset-pickup", "+window:map-window", "+window:level-password", "+feature:level-password"]
author: opus
date: 2026-11-02
---

# Repton 1–3 — британський родич Boulder Dash: діаманти, яйця-монстри, духи в клітки

## Суть
Ящірка Repton копає землю, збирає **всі** діаманти й уникає каменів, що падають і скочуються з заокруглених стін. Кожна частина додає елементи: Repton 1 — яйця, з яких вилуплюються монстри-переслідувачі, сейфи й ключ; Repton 2 — один величезний світ з транспортерів, духи, яких треба **заманити в клітки**, черепи й метеорити; Repton 3 — грибок, що росте, капсули часу, корона й годинникова бомба. На відміну від Boulder Dash — немає квоти: треба зібрати геть усе, а випадковості нема зовсім.

## Поле і час
- Рівень — велика мапа з камерою за Repton; у Repton 3 — 24 екрани трьома наборами по 8 (Prelude/Toccata/Finale), у Repton 2 — один світ з багатьох екранів, сполучених транспортерами.
- Один шар; стіни бувають пласкі й заокруглені з одного чи двох боків — від цього залежить скочування.
- Real-time з дискретними кроками по клітинах. Таймер екрана (Repton 1 і 3): у Repton 3 це годинник бомби.
- Мапа рівня — окремим екраном за клавішею (Repton 3: обмежено першими екранами).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Repton | player | життя | 4 напрямки; копає землю; штовхає камені вбік |
| Земля | terrain | 1 очко (R1) | зникає, коли пройти; у Repton 2 треба вибрати всю |
| Камінь | object | — | падає без опори; скочується із заокругленого; вбиває, падаючи згори |
| Діамант | pickup | 50 (R1) / 5 (R3) очок | треба зібрати всі |
| Стіна пласка / заокруглена | static | бік заокруглення | непрохідна, невразлива; з заокругленого боку скочуються камені/яйця |
| Яйце | container | — | падає як камінь; тріскає після падіння → за затримку монстр |
| Монстр | enemy | 20 очок (R3) | невпинно женеться за Repton; гине від каменя/яйця згори або замкнений грибком |
| Сейф | gate | — | непрохідний; ключ перетворює всі сейфи на діаманти |
| Ключ | pickup | — | відкриває всі сейфи рівня; другий ключ — нічого |
| Дух (R2–3) | enemy | ≤8 на екран | тримається стіни ліворуч; у клітці → діамант; оглушений — кружляє вічно |
| Клітка (R2–3) | gate | одна на духа | приймає духа → діамант |
| Череп (R2–3) | hazard | заокруглений верх | стіна, що вбиває при вході; камені з неї скочуються |
| Транспортер | terrain | ціль; одноразовий | переносить у задану точку (R2 — на інший екран), потім зникає |
| Пазл-шматок (R2) | pickup | 42 на гру | збір складає таємне повідомлення |
| Метеорит (R2) | hazard | — | падає з «даху» на відкритих екранах, смертельний |
| Грибок (R3) | hazard | — | росте в порожнечу, поки може; смертельний; закривається камінням |
| Капсула часу (R3) | pickup | — | скидає таймер бомби на повний |
| Корона (R3) | pickup | 50 очок, одна на екран | обовʼязкова для завершення |
| Бомба з годинником (R3) | gate | таймер екрана | увійти після всіх цілей → екран пройдено; час вийшов → вибух, −1 життя |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(target, earth|empty|pickup)` → ТО `move(repton, dir)`; земля → `set_cell(empty)`, `score(1)` (R1).
- КОЛИ `contact(repton, rock)` горизонтально → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(rock|egg)`.
- КОЛИ `tick` → ЯКЩО `cell(below, rounded)` and `free(side)` and `free(side_below)` → ТО `roll(rock|egg, side)`; обидва боки вільні → ліворуч; двоє претендують на клітину → першим падає правий.
- КОЛИ `contact(falling rock, repton)` → ТО `lose`, `lives(-1)`; стояти під нерухомим каменем — безпечно («Repton shuffle»: відступити й одразу підштовхнути).
- КОЛИ `contact(falling rock|egg, monster)` → ТО `disappear_b`, `score(20)`.
- КОЛИ `after(fall(egg))` → ТО `transform(cracked_egg)`; КОЛИ `timer(delay)` → ТО `transform(monster)`.
- КОЛИ `tick` → ТО `move(monster, toward(repton))` (`chase-greedy`); КОЛИ `contact(monster, repton)` → ТО `lose`.
- КОЛИ `contact(repton, key)` → ТО `pickup`, усі `safe` → `transform(diamond)`.
- КОЛИ `tick` → ТО `custom: «дух: тримайся стіни/обʼєкта ліворуч»`; КОЛИ `contact(spirit, cage)` → ТО `disappear_a`, `transform(cage → diamond)`.
- КОЛИ `contact(falling rock, spirit)` або `custom: «зібрано діаманти навколо духа»` → ТО `set_state(spirit, dazed)` — кружляє на місці назавжди.
- КОЛИ `contact(repton, skull|spirit|fungus|meteor)` → ТО `lose`.
- КОЛИ `contact(repton, transporter)` → ТО `teleport(repton, target)`, `disappear_b`.
- КОЛИ `tick` → ЯКЩО `free(adjacent)` → ТО `spread(fungus, dir)` (R3); замкнений грибком монстр гине.
- КОЛИ `contact(repton, time_capsule)` → ТО `pickup`, `timer(reset)`.
- КОЛИ `contact(repton, crown)` → ТО `pickup`, `score(50)`.
- КОЛИ `contact(repton, timebomb)` → ЯКЩО `all_gone(diamond)` and `all_gone(crown)` and `all_gone(monster)` → ТО `win`, `message(password_next)`, `next_level`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `custom: «бомба вибухає»`, `lose`, `lives(-1)`.
- КОЛИ `input(escape)` → ТО `lose` (самогубство, коли застряг); `input(shift+R)` → `restart`.
- Перемога: R1 — останній діамант; R2 — усі діаманти, уся земля, усі пазли, усі транспортери, тоді перейти дах до зореліту; R3 — усі діаманти (і з сейфів/кліток), корона, усі монстри → бомба. Поразка: камінь згори, ворог, череп, грибок, метеорит, кінець часу.

## Керування і ввід
- Z/X — ліворуч/праворуч, * / ? — вгору/вниз; або джойстик (K/J/F — вибір пристрою).
- M — мапа рівня; P — ввести пароль; L — завантажити набір екранів; S/Q — звук; Escape — самогубство; Shift+R — рестарт.

## Вікна, меню, HUD
- `main-menu`: вибір вводу, звук, старт, пароль, завантаження набору (R3).
- `game-screen`: поле зі скролом + панель: `score`, `lives`, `timer-countdown`, лічильники діамантів/монстрів (у R2 — сумарні на всю гру, `remaining-counter`).
- `map-window`: увесь рівень зверху (клавіша M).
- `level-password`: введення пароля екрана; пароль наступного показують після проходження.
- `editor-window` (R3): Screen Designer (мапа A–H, кольори, ліміт часу, паролі) і Character Designer (піксельні спрайти, анімація).
- Переходи: меню → екран → (бомба знешкоджена) пароль → наступний екран; 0 життів → меню.

## Фічі поза полем
- `levels-sequential` + паролі (R1: 12 рівнів; R3: 24 екрани); виклик «пройти без паролів».
- R2 — `mode-hardcore` за природою: одна сесія без сейвів і паузи (PC-версія додала збереження).
- `level-editor` (R3): редактор екранів і графіки; офіційні add-on набори зроблено ним; ліміт часу й паролі задає автор.
- Repton Infinity: редактор **логіки** обʼєктів мовою Reptol — `custom-rules` (Repton 4, Robbo, Trakker на тому ж двіжку).
- `stats`: стиль проходжень «пацифіст / воєначальник» (вбивати монстрів чи ні, R1–2).

## Варіації й родичі
- Repton 1 → 2 (світ без рівнів) → 3 (повернення рівнів, редактор) → Around the World in 40 Screens, The Life of Repton, Repton Thru Time → Repton Infinity.
- Родичі: Boulder Dash (квота, вибухи, вороги), Supaplex, Emerald Mine.
- **Осі варіацій**: ціль — «квота (BD) / зібрати все (Repton) / все + знешкодити бомбу»; скочування — «з будь-якого круглого / лише з заокругленої сторони стіни»; ворог — «тримається стіни (дух) / женеться (монстр)»; телепорт — «багаторазовий / одноразовий / на інший екран».

## Цікавинки для курсу
- Стіни із заокругленням з одного боку + правило «обидва вільні → ліворуч, конфлікт → правий першим» — 🥉: детермінізм порядку.
- Яйце: обʼєкт-контейнер, що падає як камінь і з затримкою вилуплює ворога — 📎.
- Дух → клітка: ворога треба **заманити** (wall-follower + перебудова лабіринту каменями) — 🥈, бо це пазл про маршрут чужого агента.
- Грибок: ріст у порожнечу, що відрізає зону назавжди — 📎.
- Одноразові транспортери й «використати всі» як ціль — 🌱.
- Редактор логіки (Reptol) як «правила як дані» — 👑 для повного; 🥈 для таблиці взаємодій.

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` · `push-object` · `collect-all` · `time-out` · `touch-death` · `environment-death` · `player-death` · `key-and-door` ↔ ключ → сейфи · `chase-player`/`chase-greedy` ↔ монстри · `teleport` ↔ транспортери · `item-pickup` · `event-points` · `sequential-levels` · `in-game-editor` + `editor-palette` · `player-camera` · `minimap-radar` ↔ мапа · `cheat-codes` ↔ паролі як пропуск.
- **Нема** → пропозиції карток:
  - `+egg-hatch` «Яйце: падає й вилуплює ворога» · entities/spawn · 📎 · слот {delay}.
  - `+lure-to-goal` «Заманити ворога в ціль» · game-logic/win · 🥈 — дух у клітку → діамант.
  - `+teleport-single-use` «Одноразовий телепорт» · entities/interact · 🌱 — дитина `teleport`.
  - `+timer-reset-pickup` «Предмет, що скидає таймер» · entities/state · 🌱.
  - `+level-password` «Вхід за паролем» — повтор із Chip's Challenge.
  - Повтори: `+dig-terrain`, `+roll-off-rounded` (слот side: left|right|both на стіні), `+wall-follower`, `+blob-growth` (грибок — без фіналу-перетворення).

## Пропозиції до словників
- `+trigger:enter` ⏳ (земля, транспортер), `+trigger:counter` ⏳ (таймер бомби = 0).
- `+cond:state` ⏳ (дух оглушений), `+cond:free` ⏳.
- `+effect:fall` ⏳, `+effect:roll`, `+effect:spread`, `+effect:timer` ⏳ (`timer(reset)`).
- `+role:container` ⏳ (яйце, сейф), `+role:spawner` (тріснуте яйце), `+role:terrain` (земля), `+role:hazard` (череп, грибок) — ⏳.
- `+window:map-window` ⏳ (мапа на весь екран), `+window:level-password` ⏳, `+feature:level-password`.

## Джерела
- ⭐ [Wikipedia: Repton](https://en.wikipedia.org/wiki/Repton_(video_game)) — уся серія коротко: мета кожної частини, нові елементи, Infinity/Reptol.
- [8BS: Repton 3 — інструкція](https://8bs.com/elecgame/repton_3.htm) — повний опис елементів, клавіші, очки (5/20/50), редактор.
- [Repton Resource Page](https://www.reptonresourcepage.co.uk/AboutRepton.php) — правила скочування, «Repton shuffle», статистика Repton 2, R1-очки.
- [Acorn Electron World: Repton 3](https://acornelectron.co.uk/info/electron/superior/Repton-3.html) — архів видання.
- [C64 online: Repton 3](https://c64.krissz.hu/repton-3/play-online/) — грати в браузері.

## Непевне
- (?) Кількість життів на старті й таймер у Repton 1 — інструкції R1 не читав; Wikipedia лише «time limit».
- (?) Алгоритм погоні монстра (жадібний крок по осях) — джерело каже лише «relentlessly chase».
- (?) Мапа в Repton 3 — інструкція «лише екрани A–E», рецензія — «детальна мапа рівня»; можливо, різні версії.
- (?) Чи гинуть духи від каменя, чи лише оглушуються — інструкція R3 каже «dazed»; для R2 не перевірено.
- (?) Розмір мапи екрана (кількість клітин) — не знайшов.
