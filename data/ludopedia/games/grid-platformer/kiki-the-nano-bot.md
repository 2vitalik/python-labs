---
title: Kiki the Nano Bot
slug: kiki-the-nano-bot
aka: [kiki, kiki the nanobot, Кікі нанобот]
family: grid-platformer
also: [push-slide, thinky]
klass: avatar
axes:
  field: 3d
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2002
platforms: [Windows, Mac OS X, Linux, FreeBSD, web (HTML5-порт)]
links:
  - {kind: itch, url: "https://transmutrix.itch.io/kiki-the-nanobot", best: true, note: "HTML5-порт, грається в браузері; керування, правила каменів, гравітація від орієнтації бота, перемикачі, бомби й осколки, мотори/шестерні/генератори/дроти, меню ESC"}
  - {kind: official, url: "https://kiki.sourceforge.net/", note: "оригінал: «суміш Sokoban і Kula World», мануал Basics / Items / Setup"}
  - {kind: other, url: "https://kiki.sourceforge.net/manual/items.html", note: "мануал предметів: камені, перемикачі, бомби, осколки, мотори, шестерні, генератори, дроти, ворота, мутанти"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kiki_the_nano_bot", note: "гравітація до поверхні, якої торкнувся Kiki; 50 рівнів; Statistics; uDevGame 2002"}
  - {kind: other, url: "https://github.com/monsterkodi/kiki", note: "рімейк автора на CoffeeScript/three.js: дії бота (climb up/down, jump forward, fall), Pushable, WireStone"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Kiki+the+Nano+Bot+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-by-input, orientation-state, gravity-fall, push-object, impassable-cells, projectile-shot, blast-wave, chain-detonation, button-toggle, reach-exit, sequential-levels, level-select, objective-text, help-window, settings-window, controls-remap, stats-window, language-picker, move-counter, player-camera, movement-animation, +edge-roll-gravity, +pusher-relative-gravity, +relative-turn-controls, +jump-forward, +splitter-push-blast, +motor-gear, +current-network, +task-activates-exit, +ignorable-npc-bots]
proposes: ["+axis:gravity=actor-relative", "+card:pusher-relative-gravity", "+card:splitter-push-blast", "+card:current-network", "+card:task-activates-exit"]
author: opus
date: 2026-11-09
---

# Kiki the Nano Bot — 3D-Sokoban, де «низ» визначає сам бот: штовхнутий камінь падає туди, куди дивляться ноги того, хто штовхав

## Суть
Відкрита 3D-головоломка Торстена Кохнгорста (monsterkodi): нанобот Кікі ходить по кубічній воксельній сітці з каменів і стін, виконує завдання рівня (увімкнути струм, натиснути перемикачі тощо) і виходить в активовані ворота. Автор називає її «сумішшю Sokoban і Kula World»: Кікі лізе на перешкоду попереду й перевалюється через ребра, тож може ходити по стінах і по будь-якій грані блока, а **гравітація для нього і для того, що він штовхнув, — це його власний «низ»**. Додаткові шари — стрільба по перемикачах, бомби з осколками вздовж трьох осей і механічно-електричні ланцюги мотор → шестерні → генератор → дріт → ворота.

## Поле і час
- Поле — 3D-сітка клітин (рівні мають три розміри, у рімейку `size` з трьох чисел); межі світу — коробка рівня.
- Час — реальний: кожна дія бота має тривалість (крок, поворот, стрибок, падіння), мутанти діють самі; чисто покрокового режиму нема.
- Камера — за ботом, з кількома видами (перемикання) і поглядом угору/вниз.
- Гравітація не глобальна: для Кікі — вниз відносно його орієнтації («до поверхні, якої він торкнувся востаннє»); для штовхнутого обʼєкта — «низ» того бота, що штовхав.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кікі | player | позиція + орієнтація (6 «низів» × 4 напрями) | крок уперед/назад, поворот на 90°, стрибок угору або вперед, підйом на перешкоду попереду (поворот на 90° через ребро), спуск через край; штовхає з затиснутою кнопкою; стріляє |
| Камінь | object | звичайний / «слизький» (?) | штовхається на 1; якщо під новою позицією порожньо — падає в «низ» бота, що штовхав, до першої зайнятої клітини |
| Стіна | static | — | непрохідна, нерухома, опора |
| Камінь з дротами (WireStone) | object | дроти на вільних гранях | як камінь; при поштовху чи падінні його дроти вимикаються й мережа перераховується |
| Перемикач | switch | on / off | кожне влучання кулі перемикає стан; що робить — свій для рівня (пояснює help) |
| Бомба | object | — | вибухає від кулі або осколка іншої бомби; Кікі її не зсуне — лише інші боти |
| Осколок (splitter) | projectile | напрям ±x / ±y / ±z | 6 штук від вибуху; летить до першого обʼєкта і штовхає рухомий у своєму напрямку |
| Куля | projectile | — | летить від стрільця; перемикає перемикачі, підриває бомби |
| Мотор | source | шестерні, що крутяться | безперервно дає кінетичну енергію на свої шестерні |
| Шестерня | conduit | рухома | поставлена поруч з тією, що крутиться, — крутиться теж |
| Генератор | sink | рухома особлива шестерня | що крутиться — наводить струм у дротах поруч |
| Дріт | conduit | світло = є струм | проводить струм; струм може активувати вихідні ворота |
| Ворота (gate) | gate | неактивні / активні | неактивні — проходиш без наслідків; активні — «телепорт» на наступний рівень |
| Бот-мутант | neutral | орієнтація | «дуже дурні»: стріляють один в одного; зазвичай їх можна ігнорувати; штовхаються й падають |
| Клапан, клітка, лампа (рімейк) | object | — | є в коді рімейку (`valve`, `cage`, `light`); поведінка — (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(forward|back)` → ЯКЩО `free(next)` → ТО `move(kiki, dir)`, `counter(moves, +1)`.
- КОЛИ `input(left|right)` → ТО `rotate(kiki, ±90)` навколо власної осі «вгору».
- КОЛИ `input(forward)` → ЯКЩО `not free(next)` і `not state(kiki, push_mode)` → ТО `custom: «climb up — Кікі перевалюється на грань перешкоди, його низ повертається на 90°»`.
- КОЛИ `input(forward)` → ЯКЩО `free(next)` і `custom: «під наступною клітиною порожньо, але є ребро»` → ТО `custom: «climb down — перевалюється через край на бічну грань»` (?).
- КОЛИ `after(move)` → ЯКЩО `not supported(kiki)` (відносно його низу) → ТО `fall(kiki)` у напрямку свого низу.
- КОЛИ `input(jump)` → ЯКЩО `free(front)` і `free(above_front)` і `moving(kiki, forward)` → ТО `custom: «jump forward — угору й уперед»`; інакше `custom: «стрибок угору на місці»`.
- КОЛИ `input(push+forward)` → ЯКЩО `occupied(next, movable)` і `free(cell_behind)` → ТО `push`, `move(kiki, forward)`.
- КОЛИ `after(push)` → ЯКЩО `not supported(object)` відносно низу Кікі → ТО `fall(object)` у напрямку низу Кікі до першої зайнятої клітини.
- КОЛИ `after(push)` (штовхнутий бот) → ЯКЩО `not supported(bot)` → ТО `fall(bot)` у низ бота-штовхача.
- КОЛИ `input(shoot)` → ТО `spawn(bullet, front)`; КОЛИ `contact(bullet, switch)` → ТО `custom: «перемикач on ↔ off»`.
- КОЛИ `contact(bullet|splitter, bomb)` → ТО `explode(cross3d, 1, splitter)` — 6 осколків вздовж ±x, ±y, ±z.
- КОЛИ `contact(splitter, movable)` → ТО `push`; ЯКЩО обʼєкт — бот → `fall(bot)` у його власний низ; інший обʼєкт → `custom: «не падає, лишається у повітрі»`.
- КОЛИ `contact(splitter, bomb)` → ТО `custom: «ланцюгова детонація»`.
- КОЛИ `adjacent(gear, rotating_gear)` → ТО `set_state(gear, rotating)`; КОЛИ `adjacent(generator, rotating_gear)` → ТО `set_state(generator, rotating)`.
- КОЛИ `adjacent(wire, rotating_generator)` → ТО `set_state(wire, powered)`; струм іде мережею дротів.
- КОЛИ `push|fall` камінь з дротами → ТО `clear_state(its_wires, powered)`, `custom: «мережу перераховано від генераторів»`.
- КОЛИ `custom: «завдання рівня виконано»` (наприклад, струм дійшов до воріт) → ТО `set_state(gate, active)`.
- КОЛИ `enter(kiki, gate)` → ЯКЩО `state(gate, active)` → ТО `teleport(kiki, next_level)`, `win`, `next_level`; інакше — нічого.
- КОЛИ `tick` → ТО `custom: «мутанти рухаються й стріляють один в одного»`.
- Перемога: виконати завдання рівня й пройти в активні ворота. · Поразка: енергію/здоровʼя прибрали у 0.9.0; чи бот може загинути зараз — (?). · Рахунок: лише лічильник ходів.

## Керування і ввід
- Оригінал: ↑/↓ — крок уперед/назад; ←/→ — поворот; Ctrl — стрибок; Shift (утримання) — режим штовхання; Space — постріл; PageDown — змінити вид; Home/End — погляд угору/вниз; ESC — меню. HTML5-порт: Z — стрибок, решта та сама.
- Керування відносне: «уперед» — куди дивиться бот, тож на стіні чи стелі ті самі клавіші ведуть в інші світові напрямки.
- Клавіші й геймпад перепризначаються в Setup; щоб зберегти — пункт SAVE.

## Вікна, меню, HUD
- `main-menu`: старт / продовжити · Statistics (прогрес гравця) · Setup · вихід (?).
- `level-select` — вибір пройдених рівнів (у рімейку є `levelselection`) (?).
- `game-screen` — 3D-рівень; HUD — `move-counter` (з 0.9.0), `objective-text`/тексти на екрані (?).
- `pause-menu` (ESC): help · setup · …; Enter — обрати, ↑/↓ — вибір, ESC — скасувати.
- `help-window` — завдання рівня послідовними повідомленнями (Enter/↓/→/Space — далі, інша клавіша — закрити).
- `settings-window` (Setup): опції, `options-controls` для клавіатури й геймпада, SAVE.
- `stats-window` — Statistics у головному меню.
- Переходи: main-menu → game-screen → (ESC) pause-menu → help/setup; активні ворота → наступний рівень.

## Фічі поза полем
- `levels-sequential`: 50 рівнів у версії 1.0 (у списку рімейку — 53 назви), у кожного своє завдання.
- `stats` — прогрес у меню Statistics; `remap-controls` + `gamepad-support`; `localization` — англійська, баскська, німецька, нідерландська, іспанська, португальська, шведська.
- Undo, редактора й рестарту в описах нема (?).
- Відкритий код: рімейк автора (CoffeeScript + three.js, Electron) і HTML5/SDL3-порт на itch.

## Варіації й родичі
- uDevGame 2002 (Best Graphics, Best Originality, Best Overall) → 0.9.0 (2003, прибрано енергію/здоровʼя, додано лічильник ходів, рівень «captured») → 1.0 (2005, +27 рівнів, нове меню) → Mac 1.0.3 (2007) → рімейк monsterkodi на GitHub → HTML5-порт transmutrix.
- Родичі: Sokoban (штовхання), Kula World (ходьба по всіх гранях, гравітація від поверхні), Mekorama (3D-кубики й механізми), Captain Toad (3D-кімнатний пазл), Spherical (бічна логіка з магією й блоками), Portal-подібні пазли зміни «низу».
- Осі варіацій:
  - **звідки гравітація**: глобальна (Sokoban 3D, Mekorama) / від поверхні під гравцем (Kula World) / від орієнтації того, хто штовхнув (Kiki).
  - **вибух**: руйнує (Bomberman) / штовхає осколками вздовж осей (Kiki).
  - **мета рівня**: дійти / усі ящики на цілях / виконати довільне завдання, що вмикає вихід (Kiki).

## Цікавинки для курсу
- Орієнтація бота як матриця повороту: «вперед», «вгору», «низ» у 3D-сітці; перевал через ребро = поворот на 90° навколо осі ребра — 🥈.
- Падіння штовхнутого обʼєкта в «низ» штовхача, а не світу — 🥉 (параметр у правилі падіння).
- Бомба з 6 осколками вздовж осей, що штовхають, і ланцюгова детонація — 🥉.
- Мережа енергії: мотор → суміжні шестерні → генератор → дроти, перерахунок при зсуві каменя з дротами — 🥈 (BFS по графу суміжності, події перерахунку).
- Перемикач, що перемикається кулею, і завдання рівня як скрипт — 📎.
- Відносне керування (поворот + уперед) і камера за ботом у 3D — 🥈.
- Мутанти-NPC, що воюють між собою і є «шумом» — 🌱.

## Мапа на каталог
- Є: `move-by-input` ↔ крок/поворот; `orientation-state` ↔ орієнтація бота; `gravity-fall` ↔ падіння; `push-object` ↔ камені, шестерні, генератори; `impassable-cells` ↔ стіни; `projectile-shot` ↔ кулі; `blast-wave` ↔ хрест осколків (у 3D — 6 променів); `chain-detonation` ↔ бомба підриває бомбу; `button-toggle` ↔ перемикачі; `reach-exit` ↔ ворота; `sequential-levels` + `level-select`; `objective-text` + `help-window` ↔ завдання рівня; `settings-window` + `controls-remap` ↔ Setup; `stats-window` ↔ Statistics; `language-picker` ↔ 7 мов; `move-counter`; `player-camera` + `movement-animation`.
- **Нема** → пропозиції карток:
  - `+pusher-relative-gravity` «Штовхнутий падає в низ штовхача» · entities/move · 🥉.
  - `+splitter-push-blast` «Вибух штовхає осколками вздовж осей» · entities/combat · 🥉 — родич `blast-wave`, але без руйнування.
  - `+current-network` «Мотор → шестерні → генератор → дріт» · entities/interact · 🥈 — родич `+motor-gear` (Mekorama).
  - `+task-activates-exit` «Довільне завдання рівня вмикає вихід» · game-logic/win · 📎.
  - `+edge-roll-gravity` (Kula World), `+relative-turn-controls` (Kula World), `+jump-forward` «Стрибок угору-вперед з перевіркою двох клітин» · entities/move · 🌱, `+ignorable-npc-bots` «Ворожі NPC воюють між собою» · entities/move · 🌱.

## Пропозиції до словників
- `+axis:gravity=actor-relative` — нове значення осі `gravity`: «низ» задає орієнтація сутності (Kiki), а не поле (`down`, `toward-center`) чи тип (`per-type`).
- `+card:pusher-relative-gravity`, `+card:splitter-push-blast`, `+card:current-network`, `+card:task-activates-exit` — див. вище.
- Наявні слова, вжиті без пропозиції: ролі `source` / `conduit` / `sink` (🔥 у `roles.md`), `rotate`, `explode`, `spawn`, `teleport`, `supported`, `moving`, `options-controls`, `stats-window`, `objective-text`.

## Джерела
- ⭐ [itch.io: Kiki the Nanobot (HTML5-порт)](https://transmutrix.itch.io/kiki-the-nanobot) — керування, «гравітацію визначає сам Кікі», камені падають після поштовху, перемикачі від куль, бомби й 6 осколків, мотори/шестерні/генератори/дроти, падіння штовхнутих ботів, меню ESC, help, setup.
- [kiki.sourceforge.net](https://kiki.sourceforge.net/) і [мануал Items](https://kiki.sourceforge.net/manual/items.html) — «суміш Sokoban і Kula World»; предмети: неактивні/активні ворота, камені, перемикачі, бомби (рухають лише боти), осколки (штовхають, не-боти не падають), мотор, шестерня, генератор, дріт зі світлом; мутанти. [Basics](https://kiki.sourceforge.net/manual/index.html) — мета, клавіші, меню, help. [News](https://kiki.sourceforge.net/misc/news.html) — версії 2003–2007.
- [Wikipedia: Kiki the nano bot](https://en.wikipedia.org/wiki/Kiki_the_nano_bot) — гравітація до останньої поверхні, ходьба по стінах і всіх гранях, 50 рівнів, Statistics, мови, нагороди uDevGame 2002.
- [GitHub: monsterkodi/kiki](https://github.com/monsterkodi/kiki) — рімейк: дії `climb up` / `climb down` / `jump forward` / `fall`, низ = орієнтація бота, падіння після поштовху в низ штовхача, WireStone; список 53 рівнів у `levels.txt`.
- YouTube: пошук «Kiki the Nano Bot gameplay».

## Непевне
- (?) Чи Кікі може загинути (падіння за межу світу, кулі мутантів) після того, як у 0.9.0 прибрали енергію/здоровʼя; рестарт рівня й undo — у джерелах нема.
- (?) Точна умова `climb down` (перевал через край) і чи «прилипання» до ребра працює лише під час руху.
- (?) Що роблять «слизькі» камені, клапани, клітки й лампи (є в коді рімейку, у мануалі нема).
- (?) Склад головного меню й наявність вибору рівня в оригіналі; що показує HUD, крім лічильника ходів.
- (?) Рік: перша версія — конкурс uDevGame 2002; перший публічний реліз на SourceForge — 2003, Wikipedia пише «first released 2005» (версія 1.0).
