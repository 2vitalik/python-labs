---
title: Mr. Do's Castle
slug: mr-dos-castle
aka: [Mr. Do! vs. Unicorns, Mr. Do!'s Castle, Knights vs. Unicorns]
family: grid-platformer
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 1983
platforms: [arcade, ColecoVision, Atari 2600, Atari 5200, Atari 8-bit, Commodore 64, MSX, X68000, Switch, PS4]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mr._Do%27s_Castle", best: true, note: "правила аркади: блоки, щит, EXTRA, ескалація ворогів, ревізії, порти"}
  - {kind: other, url: "https://www.arcade-history.com/game/1686/", note: "детально про аркаду: черепи, ключі, щит, оглушення, очки за поверхи й мультикіл"}
  - {kind: other, url: "https://discmaster.textfiles.com/view/1886/1000gamemanuals.iso/Colecovision/Mr%20Dos%20Castle.txt", note: "мануал ColecoVision: типи блоків, кольори єдинорогів, очки, способи пройти сцену"}
  - {kind: other, url: "https://discmaster.textfiles.com/file/1886/1000gamemanuals.iso/Atari%205200/Mr%20Do's%20Castle.TXT", note: "мануал Atari 5200: керування, похилі драбини, бонус дверей"}
  - {kind: other, url: "https://arcade-museum.com/dipswitch-settings/mr-do-s-castle", note: "DIP-налаштування аркади (неперевірені спільнотою)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mr.+Do%27s+Castle+arcade+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 70
mechanics: [move-4dir, ladder-climb, gravity-fall, destructible-blocks, chase-player, touch-death, player-death, destroy-all-enemies, collect-all, key-and-door, item-pickup, temporary-modes, event-points, progress-acceleration, sequential-levels, difficulty-levels, hot-seat, status-panel, +knock-through-hole, +fall-distance-score, +multi-kill-bonus, +letter-collection, +alt-win-conditions, +enemy-mutation, +enemy-split, +hammer-stun, +hole-escape-upgrade, +skull-section-drop, +swing-ladder, +bonus-credit-item]
proposes: ["+trigger:landed", "+effect:flip", "+ui:letter-progress", "+card:fall-distance-score", "+card:enemy-split", "+card:hammer-stun", "+card:hole-escape-upgrade", "+card:skull-section-drop", "+card:swing-ladder", "+card:bonus-credit-item"]
author: opus
date: 2026-11-09
---

# Mr. Do's Castle — замок із блоків: вибий молотом дірку, впіймай єдинорога й добий блоком згори

## Суть
Аркадний платформер у дусі Space Panic під брендом Mr. Do!: клоун з молотом бігає поверхами замку, зʼєднаними драбинами, і вибиває блоки підлоги. Дірка стає пасткою для єдинорога: впіймавши, його можна збити молотом крізь дірку на нижні поверхи або розчавити блоком, вибитим поверхом вище; чим глибше падіння, тим більше очок. Сцену проходять кількома шляхами: вибити всі вишневі блоки, знищити всіх єдинорогів або (через три ключі й щит) зібрати слово EXTRA з «літерних» монстрів. Задумувалась як «Knights vs. Unicorns», у Японії вийшла як Mr. Do! vs. Unicorns.

## Поле і час
- Один екран-замок, бічний вид: 6 поверхів (7 з укріпленнями нагорі) за arcade-history; мануали домашніх версій кажуть 7 (Atari 5200) або 8 (ColecoVision) з підвалом і верхом. Середні поверхи складені з блоків-клітин — їх і вибивають.
- Драбини двох видів: вертикальні (нерухомі) і похилі, що перекидаються вліво/вправо, «як підніжка велосипеда».
- Real-time: єдинороги рухаються безперервно; час сцени тисне ескалацією ворогів (зелені → сині, що діляться).
- Шари: блоки підлоги (з вмістом: вишня/ключ/череп/порожній) · дірки · драбини · двері нагорі · рухомі (Mr. Do, єдинороги, падаючі блоки).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Mr. Do | player | 5 життів (домашні версії) | ходить уліво/вправо, лізе драбинами, бʼє молотом; падає з будь-якої висоти без шкоди (аркада) |
| Звичайний блок | object | 20 очок | молот вибиває → дірка в підлозі; вибитий блок падає вниз |
| Вишневий блок | pickup | 20 очок | вибити всі вишні → сцену пройдено (у ранніх ревізіях вишень нема) |
| Ключ-блок | pickup | 3 на сцену, 20 очок | вибити всі три → відчиняються двері нагорі (аркада: за ними щит) |
| Череп-блок | switch | пара на кінцях секції | вибити обидва → секція між ними обвалюється, лишаючи дерев'яний настил; давить єдинорогів під собою |
| Блок єдинорога (fill) | object | 20 очок | ним єдиноріг засипає дірку, з якої вибрався; вибивається, як звичайний |
| Дірка | terrain | порожня / з єдинорогом | пастка: єдиноріг застрягає |
| Вертикальна драбина | terrain | — | рух між поверхами |
| Похила драбина | terrain | нахил ліво/право | стати на верх → перекидається на інший бік; відрізає переслідувачів |
| Двері замку | gate | закриті / відчинені | відчиняються ключами; домашні версії — бонус за досягнення дверей |
| Щит (аркада) | pickup | — | узяв → єдинороги стають «Альфа-монстрами» (EXTRA) на час |
| Червоний єдиноріг | enemy | 500 × поверхи падіння | переслідує; молот оглушує; провалюється крізь дірку |
| Зелений єдиноріг | enemy | ×2 очок | розумніший, іноді чекає нагорі; зʼявляється з часом або після втечі з ями (тоді не оглушується) |
| Синій єдиноріг | enemy | ×3 очок | ділиться надвоє; крізь дірку не провалюється — лише блоком згори |
| Альфа-монстр (буква) | enemy | буква E-X-T-R-A | тікає від Mr. Do; гине від одного удару; через час знову єдиноріг |
| Діамант | pickup | 8000 очок + кредит | зʼявляється зрідка, у випадковий момент (пізні ревізії) |
| Дерев'яний настил | terrain | — | лишається на місці обваленої секції черепів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(mr_do, dir)`; КОЛИ `input(up|down)` → ЯКЩО `cell(here, ladder)` → ТО `move(mr_do, dir)`.
- КОЛИ `input(hammer)` → ЯКЩО `occupied(front, block)` → ТО `disappear(block)`, `set_cell(front, hole)`, `score(20)`; блок падає вниз — `fall(block)`.
- КОЛИ `input(hammer)` → ЯКЩО `occupied(front, unicorn)` і `not state(unicorn, trapped)` → ТО `stun(unicorn, n)` (аркада; домашні — лише на сценах 1–2).
- КОЛИ `enter(unicorn, hole)` → ТО `set_state(unicorn, trapped)`.
- КОЛИ `input(hammer)` → ЯКЩО `state(unicorn, trapped)` і `not state(unicorn, blue)` → ТО `fall(unicorn)` крізь дірки вниз, `disappear(unicorn)`, `score(500 × поверхи)`.
- КОЛИ `contact(block, unicorn)` → ЯКЩО `moving(block, down)` → ТО `disappear(unicorn)`, `score(500 × поверхи)`; 2/3/4 за один блок → ×2/×4/×6.
- КОЛИ `timer(escape)` → ЯКЩО `state(unicorn, trapped)` → ТО `clear_state(unicorn, trapped)`, `spawn(fill_block, hole)`, `transform(unicorn, unicorn_tough)` — більше не оглушується.
- КОЛИ `custom: «обидва череп-блоки секції вибито»` → ТО `fall(section)`, `set_cell(section, floorboards)`; хто під нею — `disappear`.
- КОЛИ `enter(mr_do, ladder_top)` → ЯКЩО `cell(here, slanted_ladder)` → ТО `rotate(ladder, 180)` — `custom: «драбина перекидається на інший бік»`.
- КОЛИ `custom: «під Mr. Do дірка»` → ТО `fall(mr_do)` без шкоди.
- КОЛИ `counter(key_blocks, ==, 0)` → ТО `set_state(door, open)`; аркада — `spawn(shield)` за дверима.
- КОЛИ `picked(mr_do, shield)` → ТО `transform(unicorns, alpha_monster)`, `set_state(alpha_monster, flee, dur)`.
- КОЛИ `contact(mr_do, alpha_monster)` → ЯКЩО `input(hammer)` → ТО `disappear(alpha_monster)`, `counter(letters, +1)` — `custom: «буква зʼявляється на флагштоці нагорі»`.
- КОЛИ `state_off(alpha_monster, flee)` → ТО `transform(alpha_monster, unicorn)`.
- КОЛИ `counter(letters, ==, 5)` → ТО `lives(+1)`; домашні версії — ще й `next_level`.
- КОЛИ `counter(cherry_blocks, ==, 0)` → ТО `next_level`.
- КОЛИ `all_gone(unicorn)` → ТО `next_level`.
- КОЛИ `timer(scene_time)` → ТО `transform(unicorns, green)`, далі `transform(green, blue)`; сині періодично — `clone(unicorn)`.
- КОЛИ `count(red_unicorn, ==, 1)` → ТО `transform(unicorn, blue)`, `clone(unicorn)` (домашні версії).
- КОЛИ `rng(p)` → ТО `spawn_at(diamond, random)`; КОЛИ `picked(mr_do, diamond)` → ТО `score(8000)`, `custom: «+1 кредит»`.
- КОЛИ `reach(mr_do, door)` → ТО `score(1500 + 500 × (сцена − 1))`, максимум 8000 (домашні версії).
- КОЛИ `contact(mr_do, unicorn)` → ЯКЩО `not state(unicorn, stunned)` → ТО `lives(-1)`, `restart`.
- Перемога: нескінченний цикл сцен; сцена проходиться вишнями / всіма єдинорогами / EXTRA (домашні) — «4 способи» в стандартній аркаді, 3 у ранніх ревізіях. Поразка: 0 життів → game over. Рахунок: блоки по 20, єдинороги 500–7500 за глибину падіння й колір, множник мультикілу, двері, діамант.

## Керування і ввід
- 4-позиційний джойстик: уліво/вправо — хід, угору/вниз — драбини.
- Кнопка молота: кожен удар — окреме натискання. Аркада має 2 кнопки (призначення другої — (?)).
- Два гравці по черзі (аркада).

## Вікна, меню, HUD
- `game-screen` — замок на весь екран, поруч рахунок; нагорі флагшток з літерами EXTRA; життя (Atari 5200 — смужки, ColecoVision — кепки Mr. Do).
- `end-screen` — game over; домашні версії: Fire → нова гра зі сцени 1.
- `attract-demo` (?) — типовий аркадний демо-режим, у джерелах не описаний.
- Аркадний сервіс: `custom-window` тест-режим; DIP-перемикачі (див. «Фічі»).
- Переходи: старт → game-screen сцени 1 → (сцену пройдено) → наступна сцена; втрата останнього життя → game over.

## Фічі поза полем
- `operator-settings` (DIP аркади): кількість гравця/життів 2–5 (?), тип корпусу Table/Upright, складність «EXTRA Game» і «SPECIAL Game» (Easy/Hard), складність 4 рівні, автоматичний/звичайний екран, Free Play, тест-режим.
- `levels-sequential`: домашні версії — 8 сцен і 16 рівнів складності (більше єдинорогів, агресивніші, інші драбини й блоки).
- `hotseat` (2 гравці по черзі); бонусний кредит від діаманта — фіча «на автомат», а не на гравця.
- Порти: ColecoVision/Atari/C64 (Parker Brothers), MSX, X68000; Arcade Archives (Switch, PS4) і Arcade Archives 2.

## Варіації й родичі
- Ревізії аркади: ранні й «Mr. Do! vs. Unicorns» — без вишень (лише 3 способи пройти сцену), блоки-заповнювачі міняють колір кожні дві сцени; пізні — вишні, діамант-кредит.
- Домашні порти: замість щита — двері, що відкриваються ключами й перетворюють єдинорогів на літерних; EXTRA ще й завершує сцену; на ColecoVision часті удари фарбують червоного в зеленого, зеленого — в синього.
- Родичі: Space Panic (ями й «добивання» падінням — пряма основа), Mr. Do! (бренд, EXTRA, вишні), Lode Runner (дірки-пастки, що заростають), Wrecking Crew (молот і руйнування блоків), Bugs Bunny Crazy Castle.
- Осі: **як убити ворога в ямі** (засипати / збити вниз / блок згори); **що робить ворог, якого лишили в ямі** (гине / вилазить і засипає / вилазить сильнішим); **скільки способів пройти рівень** (1 / кілька альтернативних).

## Цікавинки для курсу
- Альтернативні умови перемоги сцени (вишні / всі вороги / EXTRA) — 📎: кілька тригерів `next_level`.
- Очки за глибину падіння ворога + множник за кількох одним блоком — 📎.
- Череп-блоки: пара кінців секції як «замок», обвал секції як масовий удар — 🥉 (пошук сегмента між двома мітками й падіння групи).
- Похила драбина-перемикач, що відрізає маршрут переслідувача — 🥉 (ребро графа, яке гравець вмикає/вимикає).
- Ескалація ворогів за часом (червоний → зелений → синій, що ділиться) — 🥉.
- Ворог, що вибрався з ями, засипає її і стає сильнішим — 📎.

## Мапа на каталог
- Є: `move-4dir` · `ladder-climb` · `gravity-fall` (блоки й вороги падають крізь дірки) · `destructible-blocks` · `chase-player` · `touch-death` · `player-death` · `destroy-all-enemies` · `collect-all` (вишні) · `key-and-door` (3 ключі → двері) · `item-pickup` (щит, діамант) · `temporary-modes` (Альфа-монстри) · `event-points` · `progress-acceleration` · `sequential-levels` · `difficulty-levels` · `hot-seat` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+fall-distance-score` «Очки за глибину падіння ворога» · game-logic/score · 🌱 · слот {per_floor}.
  - `+enemy-split` «Ворог ділиться з часом» · entities/spawn · 📎.
  - `+hammer-stun` «Удар оглушує ворога на час» · entities/combat · 📎 · слот {duration}.
  - `+hole-escape-upgrade` «Ворог вилазить з ями, засипає її й посилюється» · entities/interact · 📎.
  - `+skull-section-drop` «Секція між двома мітками обвалюється» · entities/interact · 🥉.
  - `+swing-ladder` «Драбина-перемикач між двома положеннями» · entities/move · 🥉.
  - `+bonus-credit-item` «Рідкісний предмет дає кредит/продовження» · game-logic/score · 🌱.
  - Повтори наявних пропозицій корпусу: `+knock-through-hole` (Space Panic), `+multi-kill-bonus`, `+letter-collection`, `+alt-win-conditions`, `+enemy-mutation` (Mr. Do!).

## Пропозиції до словників
- `+trigger:landed` — блок/ворог/гравець приземлився (рахунок за глибину, обвал секції).
- `+effect:flip` — перекинути двопозиційний обʼєкт (похила драбина); зараз — `rotate(…, 180)` з `custom`.
- `+ui:letter-progress` — флагшток із зібраними літерами EXTRA.
- `+card:fall-distance-score`, `+card:enemy-split`, `+card:hammer-stun`, `+card:hole-escape-upgrade`, `+card:skull-section-drop`, `+card:swing-ladder`, `+card:bonus-credit-item` — див. вище.

## Джерела
- ⭐ [Wikipedia: Mr. Do's Castle](https://en.wikipedia.org/wiki/Mr._Do%27s_Castle) — платформи й драбини, вишні/ключі/черепи, щит і EXTRA-монстри, ескалація зелені → сині, діамант-кредит, ревізії, порти (розділ геймплею частково без цитувань).
- [arcade-history.com #1686](https://www.arcade-history.com/game/1686/) — 6/7 поверхів, похилі драбини, черепи → настил, ключі → щит, оглушення, втеча з ями, сині не збиваються молотом, очки 500/1000/1500/2000 за поверхи, ×2/×4/×6 за мультикіл, діамант 8000.
- [Мануал ColecoVision](https://discmaster.textfiles.com/view/1886/1000gamemanuals.iso/Colecovision/Mr%20Dos%20Castle.txt) і [мануал Atari 5200](https://discmaster.textfiles.com/file/1886/1000gamemanuals.iso/Atari%205200/Mr%20Do's%20Castle.TXT) — домашні правила: 20 очок за блок, кольори єдинорогів і очки 500–7500, 5 життів, 8 сцен × 16 рівнів складності, бонус дверей.
- [arcade-museum: DIP-перемикачі](https://arcade-museum.com/dipswitch-settings/mr-do-s-castle) — налаштування автомата.
- YouTube: пошук «Mr. Do's Castle arcade gameplay».

## Непевне
- (?) Кількість поверхів: 6/7 (arcade-history), 7 (Atari 5200), 8 (ColecoVision).
- (?) Четвертий спосіб пройти сцену в аркаді: Wikipedia каже «4 у стандартній, 3 у ранніх», але явно перелічує лише вишні й усіх ворогів; EXTRA як завершення сцени — з мануалів домашніх версій.
- (?) Чи вбиває Альфа-монстрів падаючий блок (arcade-history: так) і чи EXTRA в аркаді завершує сцену.
- (?) Яку саме клітину вибиває молот (поруч на рівні ніг чи під собою) — джерела кажуть лише «вибиває блоки підлоги».
- (?) DIP «Player» 2–5 — найпевніше кількість життів, сторінка не підписує; друга кнопка аркади — призначення невідоме.
- (?) arcade-history в одному місці називає предмет за дверима «хрестом», в іншому — щитом.
