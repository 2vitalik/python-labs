---
title: "Gunbrick (Gunbrick: Reloaded)"
slug: gunbrick
aka: ["Gunbrick: Reloaded", Ганбрік, Цеглина-гармата]
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: state
year: 2015
platforms: [iOS (2015), web (браузерна версія), Windows, macOS, Switch (Reloaded 2020)]
links:
  - {kind: other, url: "https://egmnow.com/gunbrick-reloaded-review/", best: true, note: "найясніше про ядро: перекат на грань, 4 перекати = та сама орієнтація, віддача гармати, guncube у 3D-рівнях, retro-рівні"}
  - {kind: steam, url: "https://store.steampowered.com/app/1222270/Gunbrick_Reloaded/", note: "Nitrome, 9.04.2020; гармата з одного боку, щит з іншого, постріл униз — rocket jump; боси, приховані рівні"}
  - {kind: other, url: "https://nintendoworldreport.com/review/53469/gunbrick-reloaded-switch-review", note: "щит блокує лазери й вогнемети, постріл по кнопках здалеку, цегляні стовпи, чекпойнти, ізометричні бонус-рівні"}
  - {kind: other, url: "https://goombastomp.com/gunbrick-reloaded-review/", note: "липкі поверхні, плитки-розворот, 40+ рівнів у трьох світах + 12 бонусних"}
  - {kind: other, url: "https://www.pocketgamer.com/gunbrick/review/", note: "свайп — перекат, тап — постріл; стрибок лише гарматою вниз; кнопки в послідовності"}
  - {kind: other, url: "https://www.pocketgamer.com/gunbrick/hands-on-with-nitromes-roly-poly-puzzle-platformer-gunbrick/", note: "турелі, патрульні, яких без щита не пройти, кнопки відчиняють ворота"}
  - {kind: other, url: "https://www.macworld.com/article/224990/you-should-play-gunbrick-is-a-puzzle-game-disguised-as-a-platformer.html", note: "вгору лише пострілом у землю; вогонь-і-перемикач; бос-поліцейська машина"}
  - {kind: other, url: "https://games.jayisgames.com/review/gunbrick.php", note: "браузерна версія: стрілки/A-D — перекат, вгору/W — постріл, 10 рівнів; віддача вбік"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Gunbrick+Reloaded+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-by-input, keyboard-controls, swipe-gestures, orientation-state, gravity-fall, projectile-shot, shoot-forward, destructible-blocks, button-toggle, touch-death, environment-death, checkpoint, respawn, reach-exit, sequential-levels, level-select, level-unlock, +roll-block, +recoil-jump, +shield-block, +sticky-surface, +reverse-tile, +move-synced-hazards, +remote-switch-shot, +switch-sequence, +boss-fight, +bonus-stage]
proposes: ["+effect:recoil", "+card:recoil-jump", "+card:sticky-surface", "+card:reverse-tile", "+card:move-synced-hazards", "+card:remote-switch-shot", "+card:switch-sequence"]
author: opus
date: 2026-11-09
---

# Gunbrick — цеглина з гарматою на одній грані й щитом на протилежній котиться перекатами; вгору — лише віддачею пострілу вниз

## Суть
Гравець — квадратна «цеглина», що рухається тільки **перекатом на сусідню грань**, тож кожен крок повертає її на 90°. На одній грані гармата, на протилежній щит; що з них дивиться вгору, вниз чи вбік, визначає кількість перекатів (4 перекати — та сама орієнтація, 2 — догори дриґом). Стрибка нема: щоб піднятися, треба докотитися гарматою вниз і вистрілити — **віддача** підкидає цеглину. Головна задача рівня — порахувати клітини так, щоб на місці потрібна грань дивилася в потрібний бік (щит до лазера, гармата до ворога чи землі).

## Поле і час
- Бічний вид, квадратна сітка, клітина = розмір цеглини; рівні з кількох екранів, камера слідує (?).
- Час іде сам (`realtime`): вороги патрулюють, турелі стріляють, але рух цеглини дискретний — один перекат = одна клітина.
- У пізніх рівнях частина пасток **ходить разом із гравцем**: робить свій крок, коли перекочується цеглина, тож помилка в підрахунку смертельна (EGM).
- Reloaded має три види рівнів: основні 2D, ізометричні 3D-бонусні (цеглина стає кубом, guncube) і спрощені retro 2D (EGM, NWR).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Gunbrick (цеглина) | player | 4 грані: гармата, щит навпроти, 2 порожні; орієнтація | перекат на 1 клітину з поворотом на 90°; падає без опори; стріляє з грані-гармати |
| Постріл | projectile | напрям грані-гармати | летить по прямій; знищує ворогів, ламає частину перешкод, натискає кнопки |
| Щит (грань цеглини) | player | напрям | непробивний; блокує кулі, лазери, вогонь з того боку, куди дивиться; ним можна котитися через небезпеки |
| Стіна / платформа | static | — | опора й перешкода |
| Яма | hazard | — | падіння = смерть |
| Цегляний стовп / стіна, що ламається | object | — | руйнується пострілом; у дірку можна впасти |
| Липка поверхня | terrain | — | цеглина котиться нею по стіні й стелі |
| Плитка-розворот | terrain | — | цеглина, що стала на неї, рухається у зворотний бік |
| Кнопка / перемикач | switch | → ворота; часом порядок | натискається пострілом здалеку; частину треба натискати в послідовності |
| Ворота | gate | відкрито/закрито | відчиняються кнопкою |
| Лазер | hazard | напрям | убиває, якщо не прикритися щитом |
| Вогнемет / вогняна пастка | hazard | вмик/вимик (?) | убиває без щита; є варіант «вогонь і перемикач» |
| Синхронна пастка | hazard | — | робить крок, коли перекочується цеглина (пізні рівні) |
| Турель | enemy | — | стріляє кулями; кулі зупиняє щит |
| Патрульний | enemy | маршрут | ламає цеглину при контакті, якщо не підставлено щит |
| Панк з ножем, «нерд», мутант, поліція | enemy | — | гинуть від пострілу або розчавлені перекатом |
| Цивільні | neutral | — | ходять рівнем, їх можна розчавити |
| Бос | boss | фази (?) | окремі бої наприкінці світів (поліцейська машина, «бензопилковий поєдинок») |
| Схований колекційний предмет | pickup | — | відкриває 3D-бонусний рівень (Reloaded) |
| Чекпойнт | static | — | точка повернення після смерті |
| Вихід | static | — | кінець рівня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(roll, dir)` → ЯКЩО `free(next_cell)` і `supported(brick)` → ТО `move(brick, dir)`, `rotate(brick, 90)`.
- Наслідок перекату: орієнтація = кількість перекатів mod 4; гармата, що була внизу, після двох перекатів дивиться вгору (EGM).
- КОЛИ `input(fire)` → ТО `spawn(shot)` з грані-гармати в її напрямку.
- КОЛИ `input(fire)` → ЯКЩО `facing(gun, down)` → ТО `custom: «віддача підкидає цеглину вгору (rocket jump)»` — єдиний спосіб вибратися на вищий ярус.
- КОЛИ `input(fire)` → ЯКЩО `facing(gun, left)` або `facing(gun, right)` → ТО `custom: «віддача зсуває цеглину в протилежний бік без перекату»` — орієнтація не міняється, мінус один перекат у підрахунку (EGM, JayIsGames).
- КОЛИ `contact(shot, enemy)` → ТО `disappear_b`.
- КОЛИ `contact(shot, breakable_wall)` → ТО `disappear_b`; КОЛИ `tick` → ЯКЩО `not supported(brick)` → ТО `fall(brick)` (у пробиту дірку теж).
- КОЛИ `contact(shot, button)` → ТО `set_state(gate, open)`; для групи кнопок — ЯКЩО `custom: «натиснуто в правильному порядку»`.
- КОЛИ `contact(laser, brick)` або `contact(flame, brick)` або `contact(bullet, brick)` → ЯКЩО `facing(shield, toward_source)` → ТО `block`; інакше `lose`.
- КОЛИ `contact(guard, brick)` → ЯКЩО `not facing(shield, guard)` → ТО `lose`.
- КОЛИ `input(roll, dir)` → ЯКЩО `occupied(next_cell, punk)` або `occupied(next_cell, civilian)` → ТО `disappear_b` (розчавлено перекатом).
- КОЛИ `enter(brick, sticky)` → ТО `custom: «перекат по стіні й стелі, без падіння»`.
- КОЛИ `enter(brick, reverse_tile)` → ТО `bounce(brick)`.
- КОЛИ `input(roll, dir)` → ТО `custom: «синхронні пастки роблять свій крок»`.
- КОЛИ `enter(brick, pit)` → ТО `lose`.
- КОЛИ `contact(brick, checkpoint)` → ТО `checkpoint`; після `lose` → `respawn(brick, checkpoint)`.
- КОЛИ `contact(brick, secret_item)` → ТО `pickup`, `unlock(bonus_level)`.
- КОЛИ `contact(brick, exit)` → ТО `win`, `next_level`.
- 3D-бонусні рівні: КОЛИ `input(roll, dir)` → ТО `custom: «guncube котиться як бочка: верхня й нижня грані лишаються на місці»` — інша вісь обертання, ніж у 2D (EGM).
- Перемога: дійти до виходу. · Поразка: остаточної нема (?) — смерть повертає на чекпойнт. · Рахунок: у джерелах не згадано.

## Керування і ввід
- Мобільна версія: свайп убік — перекат, тап — постріл (Pocket Gamer, Macworld).
- Браузерна версія: стрілки або A/D — перекат, стрілка вгору або W — постріл (JayIsGames).
- Reloaded (PC/Switch): кнопки геймпада (?), на Switch — HD-вібрація.
- Окремої кнопки стрибка нема; напрям пострілу задається лише орієнтацією цеглини.

## Вікна, меню, HUD
- `splash-screen` (?) — титул.
- `level-select`: світи й рівні; серед пунктів — «телешоу», які можна дивитися (GoombaStomp); рецензент NWR скаржиться, що меню погано показує, де ти в грі.
- `game-screen`: рівень; HUD — (?), у джерелах не описано.
- `pause-menu` (?) — продовжити, рестарт, вихід.
- `end-screen` (?) — рівень пройдено.
- Сюжетні вставки про світ, де цеглини замінили машини, — `dialogue-window` (?).
- Переходи: level-select → game-screen → (вихід) → наступний рівень; схований предмет → відкривається 3D-рівень у level-select.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: світи з боссами наприкінці; GoombaStomp — 40+ рівнів у трьох світах, Steam — «п'ять локацій» (розбіжність — у «Непевне»).
- `checkpoint`-респавн замість життів (NWR).
- `collectibles` → відкривають 12 ізометричних 3D-рівнів (Reloaded); деякі предмети дуже важко знайти навіть після фіналу (EGM).
- Retro 2D-рівні — спрощені версії базових (EGM).
- `achievements` (Steam), `localization` (англійська + 10 мов з повним озвученням і субтитрами).

## Варіації й родичі
- Gunbrick (iOS, 2015) → браузерна версія (10 рівнів) → Gunbrick: Reloaded (2020, Windows/macOS/Switch): + 3D-бонусні рівні з guncube, + retro-рівні.
- Родичі в сімʼї: `kula-world` (кочення в 3D), `boxboy` (форма як інструмент, щит від лазера), `mekorama`; поза сімʼєю — Bloxorz і Stephen's Sausage Roll (орієнтація від перекату).
- Осі варіацій:
  - **як підніматися**: стрибок кнопкою / сходинка на 1 (`block-dude`) / віддача пострілу вниз (Gunbrick);
  - **орієнтація тіла**: нема / 4 стани від перекату в 2D (Gunbrick) / 24 стани куба в 3D (guncube, Bloxorz);
  - **хто рухається з гравцем**: ніхто / синхронні пастки / весь світ (покрокові ігри).

## Цікавинки для курсу
- Перекат з орієнтацією mod 4 і перевірка «яка грань куди дивиться» — 📎 (масив граней + зсув індексу).
- Віддача: постріл униз — підйом, вбік — зсув без повороту; рух як наслідок дії, а не вводу напрямку — 🥉.
- Щит-грань: промінь чи куля зупиняється, лише якщо грань дивиться на джерело — 📎.
- Пастки, що ходять синхронно з гравцем, у real-time грі — 🥉 (дві моделі часу в одному рівні).
- Розвʼязувач рівня BFS по станах (клітина, орієнтація) — 🥈.
- Guncube у 3D: 24 орієнтації куба й обертання навколо різних осей — 🥇.

## Мапа на каталог
- Є: `move-by-input` + `keyboard-controls` + `swipe-gestures` ↔ перекат свайпом/клавішами; `orientation-state` ↔ грані з гарматою й щитом; `gravity-fall` ↔ падіння без опори; `projectile-shot` + `shoot-forward` ↔ постріл з грані; `destructible-blocks` ↔ цегляні стовпи; `button-toggle` ↔ кнопки й ворота; `touch-death` + `environment-death` ↔ вороги, лазери, ями; `checkpoint` + `respawn`; `reach-exit`; `sequential-levels` + `level-select` + `level-unlock`.
- **Нема** → пропозиції карток:
  - `+recoil-jump` «Віддача пострілу рухає стрільця» · entities/move · 🥉 · слот {down: launch, side: shift}.
  - `+roll-block` (вже пропонована) — рух перекатом з поворотом тіла.
  - `+shield-block` (BoxBoy) — грань-щит зупиняє промінь/снаряд з одного боку.
  - `+sticky-surface` «Липка поверхня: рух по стінах і стелі» · entities/move · 📎.
  - `+reverse-tile` «Плитка розвертає напрям руху» · entities/interact · 🌱.
  - `+move-synced-hazards` «Пастки роблять крок разом із гравцем» · entities/move · 🥉.
  - `+remote-switch-shot` «Кнопка натискається пострілом» · entities/interact · 🌱.
  - `+switch-sequence` «Кнопки треба натиснути в порядку» · entities/interact · 📎.
  - `+boss-fight`, `+bonus-stage` (вже пропоновані) — боси світів, приховані 3D-рівні.

## Пропозиції до словників
- `+effect:recoil(a, dir)` — постріл зсуває стрільця в протилежний бік (униз — зліт, убік — зсув без перекату).
- `+card:recoil-jump`, `+card:sticky-surface`, `+card:reverse-tile`, `+card:move-synced-hazards`, `+card:remote-switch-shot`, `+card:switch-sequence` — див. «Мапа на каталог».

## Джерела
- ⭐ [EGM: Gunbrick: Reloaded review](https://egmnow.com/gunbrick-reloaded-review/) — перекат на грань, 4 / 2 перекати, щит зверху й гармата знизу, віддача вбік як «мінус крок», пастки, що рухаються з гравцем, guncube, retro-рівні, колекційні предмети.
- [Steam: Gunbrick: Reloaded](https://store.steampowered.com/app/1222270/Gunbrick_Reloaded/) — Nitrome, 9.04.2020, гармата/щит, rocket jump, вороги, боси, п'ять локацій, приховані рівні, музика Eirik Suhrke.
- [Nintendo World Report](https://nintendoworldreport.com/review/53469/gunbrick-reloaded-switch-review) — щит від лазерів і вогнеметів, постріл по кнопках, цегляні стовпи, чекпойнти, ізометричні бонус-рівні, cube mode.
- [GoombaStomp](https://goombastomp.com/gunbrick-reloaded-review/) — липкі поверхні, плитки-розворот, цивільні, 40+ рівнів, 3 світи, 12 бонусних, телешоу в level-select.
- [Pocket Gamer: review](https://www.pocketgamer.com/gunbrick/review/) і [hands-on](https://www.pocketgamer.com/gunbrick/hands-on-with-nitromes-roly-poly-puzzle-platformer-gunbrick/) — свайп/тап, стрибок лише гарматою вниз, кнопки в послідовності, турелі, патрульні, ворота.
- [Macworld](https://www.macworld.com/article/224990/you-should-play-gunbrick-is-a-puzzle-game-disguised-as-a-platformer.html) — підйом пострілом у землю, вогонь-і-перемикач, бос-поліцейська машина.
- [JayIsGames](https://games.jayisgames.com/review/gunbrick.php) — браузерна версія, клавіші, віддача вбік, 10 рівнів.
- YouTube: пошук «Gunbrick Reloaded gameplay».

## Непевне
- (?) Модель часу: рецензії кажуть про «дію» й патрулі (real-time), але EGM — що пізні пастки ходять, коли ходить гравець; чи вороги теж синхронні — не перевірено.
- (?) Кількість світів: GoombaStomp — три основні + 12 бонусних рівнів; Steam — «п'ять локацій» (можливо, з бонусними й retro).
- (?) Що відбувається при пострілі гарматою вгору; чи можна стріляти в польоті.
- (?) Життя, рахунок, HUD, кнопки Reloaded на геймпаді — у відкритих джерелах не описано.
- (?) Як саме «розчавлюють» панків і цивільних (перекатом зверху чи збоку).
