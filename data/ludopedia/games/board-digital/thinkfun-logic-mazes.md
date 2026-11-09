---
title: ThinkFun Laser Maze і Gravity Maze
slug: thinkfun-logic-mazes
aka: [Laser Maze, Gravity Maze, Лазерний лабіринт, Гравітаційний лабіринт, Laser Maze Jr]
family: board-digital
also: [connect-rotate, dig-gravity]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2013
platforms: [board]
links:
  - {kind: other, url: "https://geekdad.com/2013/06/laser-maze/", best: true, note: "огляд Laser Maze: сітка 5×5, усі жетони й кількості, як читати картку (?-орієнтація, жетони до додавання), 60 карток, правило «промінь торкається всіх жетонів»"}
  - {kind: other, url: "https://legacy.thinkfun.com/wp-content/uploads/2013/09/Laser-1014-Instructions.pdf", note: "офіційні правила Laser Maze (бачив у видачі пошуку; при відкритті 503)"}
  - {kind: other, url: "https://officialgamerules.org/game-rules/gravity-maze/", note: "Gravity Maze: сетап за карткою, вежі обертаються, лише вказані вежі, кулька до цільової вежі"}
  - {kind: other, url: "https://www.presentsofmind.com.au/game/gravity-maze-by-thinkfun-2/", note: "Gravity Maze: склад (сітка, 10 веж, 3 кульки), 60 завдань Beginner–Expert"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ThinkFun+Laser+Maze", note: "пошук; Laser Maze"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ThinkFun+Gravity+Maze", note: "пошук; Gravity Maze"}
stage: v1
coverage: 55
mechanics: [beam-tracing, mirror-reflect, piece-rotate-flip, drag-drop-piece, cell-click, level-bank, puzzle-select, level-select, level-unlock, difficulty-levels, level-solver, reachability-check, height-levels, gravity-fall, in-game-editor, game-screen, end-screen, help-window, undo-redo, +beam-splitter, +challenge-card-setup, +fixed-vs-free-orientation, +must-use-all-pieces, +beam-touches-all, +target-count-goal, +placement-blocker, +marble-path-sim, +3d-tower-stack, +simulate-button]
proposes: ["+trigger:beam_hit", "+trigger:marble_stopped", "+cond:hit_side", "+cond:all_pieces_used", "+effect:emit_beam", "+effect:reflect", "+effect:split_beam", "+effect:release_marble", "+ui:beam-preview", "+ui:pieces-tray", "+ui:orientation-lock-badge", "+window:challenge-card", "+card:beam-touches-all", "+card:challenge-card-setup", "+card:marble-path-sim"]
author: opus
date: 2026-11-09
---

# ThinkFun Laser Maze і Gravity Maze — пасьянс-головоломки з картками: доставити жетони так, щоб промінь (кулька) дійшов до цілі

## Суть
Дві однокористувацькі логічні головоломки ThinkFun з однаковою схемою: картка завдання показує частину жетонів, уже стоїть на полі (іноді з фіксованою орієнтацією), і список жетонів, які треба додати. **Laser Maze**: на сітці 5×5 розставити дзеркала й розщеплювачі так, щоб лазер засвітив задану кількість цілей і торкнувся кожного жетона. **Gravity Maze**: на сітці з вежами-жолобами побудувати тривимірний шлях, яким кулька, кинута зі старту, докотиться до цільової вежі. Обидві — «зʼєднати джерело з ціллю» з обмеженим набором деталей; одна про оптику на площині, друга про гравітацію в 3D.

## Поле і час
- **Laser Maze**: пластикова сітка 5×5 з гніздом для картки; жетони стоять у клітинах, кожен має орієнтацію (4 повороти).
- **Gravity Maze**: базова сітка, у клітини ставлять прозорі вежі різної висоти й форми; вежі складаються одна на одну — поле фактично тривимірне (`3d`), висота — кількість ярусів. Розмір сітки — у «Непевне».
- Часу нема: перевірка розвʼязку — увімкнути лазер / кинути кульку.
- Інформація повна; на звороті картки — розвʼязок.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лазер (Laser Maze) | source | орієнтація | випускає промінь у напрямку погляду |
| Ціль/дзеркало | object | 5 шт., орієнтація | одна грань — дзеркало (відбиває на 90°), червона прозора грань — ціль; влучання в червону грань засвічує |
| Розщеплювач променя | object | 2 шт. | ділить промінь: частина проходить прямо, частина повертає на 90° |
| Подвійне дзеркало | object | 1 шт. | обидві грані відбивають на 90° |
| Контрольна точка | object | 1 шт. | промінь мусить пройти крізь неї |
| Блокатор клітини | static | 1 шт. | у його клітину не можна ставити жетон; промінь не блокує |
| Промінь | projectile | — | іде прямо до жетона або краю; може перетинати сам себе й торкатися жетона двічі з різних боків |
| Картка завдання | supply | 60 шт. | задає жетони на полі, орієнтації, жетони до додавання, кількість цілей (1–3) |
| Стартова вежа (Gravity Maze) | source | — | місце, куди кидають кульку |
| Вежа-жолоб | conduit | 10 веж (разом із цільовою), висота, форма | направляє кульку вниз і вбік залежно від орієнтації |
| Цільова вежа | sink | 1 | кулька, що в ній зупинилась, = розвʼязок |
| Кулька | object | 3 сталеві | котиться під дією гравітації крізь вежі |

## Правила (КОЛИ → ЯКЩО → ТО)
Laser Maze:
- Сетап: КОЛИ `level_start` → ТО `place(token)` як на картці; ЯКЩО `custom: «на картці знак ?»` → ТО `custom: «орієнтація вільна»`, інакше `custom: «орієнтація зафіксована»`.
- Розміщення: КОЛИ `input(place(token, cell))` → ЯКЩО `free(cell)` and `not occupied(cell, blocker)` → ТО `place(token)`; КОЛИ `input(rotate(token))` → ЯКЩО `custom: «орієнтація не зафіксована карткою»` → ТО `rotate(token, 90)`.
- Промінь: КОЛИ `input(custom: «увімкнути лазер»)` → ТО `custom: «промінь іде прямо з лазера»`.
- КОЛИ `contact(beam, mirror)` → ТО `custom: «відбиття на 90° за діагоналлю дзеркала»`.
- КОЛИ `contact(beam, target_mirror)` → ЯКЩО `custom: «влучив у червону грань»` → ТО `set_state(target, lit)`; ЯКЩО `custom: «влучив у дзеркальну грань»` → ТО `custom: «відбиття на 90°»`.
- КОЛИ `contact(beam, splitter)` → ТО `custom: «промінь ділиться: прямо + поворот на 90°»`.
- КОЛИ `contact(beam, checkpoint)` → ЯКЩО `custom: «промінь іде крізь проріз»` → ТО `set_state(checkpoint, passed)`.
- КОЛИ `contact(beam, blocker)` → ТО `custom: «промінь проходить без змін»`.
- КОЛИ `edge(beam)` → ТО `custom: «гілка променя зникає»`.
- Перемога: КОЛИ `custom: «усі гілки променя завершились»` → ЯКЩО `counter(lit_targets, =, card_targets)` and `custom: «промінь торкнувся кожного жетона, крім блокатора»` and `custom: «використано всі жетони картки»` → ТО `win`; ЯКЩО `custom: «картка називає конкретні цілі»` → ТО засвітитись мусять саме вони.
- Розвʼязок на картці єдиний (за правилами ThinkFun).

Gravity Maze:
- Сетап: КОЛИ `level_start` → ТО `place(tower)` у клітини з картки — їхні позиції фіксовані; решта веж зі списку — до розміщення.
- Будова: КОЛИ `input(place(tower, cell))` → ЯКЩО `custom: «вежа є в списку картки»` → ТО `place(tower)`; можна `rotate(tower, 90)` і ставити на іншу вежу.
- Пуск: КОЛИ `input(custom: «кинути кульку в старт»)` → ТО `fall(marble)`.
- КОЛИ `contact(marble, tower)` → ТО `custom: «жолоб веде кульку в сусідню клітину нижчим ярусом за орієнтацією»`; далі `fall(marble)`.
- Перемога: КОЛИ `custom: «кулька зупинилась»` → ЯКЩО `occupied(target_tower, marble)` → ТО `win`; інакше — переставити й повторити.
- Деякі завдання мають кілька розвʼязків.

## Керування і ввід
- Цифрова версія: лоток жетонів поза полем (`pieces-tray`, кандидат) → `drag-drop-piece` на клітину; клік по жетону — поворот на 90° (заблоковано для фіксованих, позначка-замок `orientation-lock-badge`, кандидат).
- Кнопка «Увімкнути лазер» / «Кинути кульку» — анімація траси; помилки (неосвітлена ціль, непройдений жетон) підсвічуються.
- Gravity Maze — 3D-камера з обертанням, вежа ставиться на вибраний ярус.
- `undo-button`, `restart-button`, «Показати розвʼязок» (зворот картки).

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Laser / Gravity → `puzzle-select` · Правила → `help-window` · Редактор (Gravity: «будуй свої»).
- `puzzle-select`: 60 карток за рівнями Beginner → Expert зі статусом «розвʼязано».
- `challenge-card` (кандидат): картка завдання збоку — сітка з жетонами, знаки «?», жетони до додавання, кількість цілей.
- `game-screen`: поле, лоток, картка, кнопка пуску, `beam-preview` (кандидат) — траса після пуску; лічильник засвічених цілей (`progress-bar`).
- `solutions-window`: розвʼязок (зворот картки).
- `end-screen`: «розвʼязано» → наступна картка.
- Переходи: main-menu → puzzle-select → game-screen ⇄ solutions-window → end-screen → наступна.

## Фічі поза полем
- `puzzle-bank` (60 карток кожна гра), `difficulty-presets` (Beginner–Expert), `levels-sequential`.
- `show-solution` — розвʼязок на звороті картки.
- `level-editor` — Gravity Maze прямо радить будувати власні лабіринти після всіх карток.
- `undo`, `restart-level`.

## Варіації й родичі
- Laser Maze Jr — дитячий варіант (є окремі правила ThinkFun; не відкривав); Gravity Maze Builder — набір розширення.
- Цифрові родичі лазера: [deflektor](../connect-rotate/deflektor.md), [khet](../connect-rotate/khet.md) (лазер як зброя у дуелі), [laser-tank](../connect-rotate/laser-tank.md), [chromatron](../connect-rotate/chromatron.md).
- Родичі «збудуй шлях з набору деталей»: [railroad-ink](railroad-ink.md), [karuba](karuba.md); марбл-рани й жолоби — [wheres-my-water](../dig-gravity/wheres-my-water.md) (рідина замість кульки).
- Схема «картка-завдання + набір деталей» у сімʼї — [ubongo](ubongo.md), [daedalian-opus](daedalian-opus.md).
- **Осі варіацій**: носій (промінь / кулька / вода) · деталі (дзеркало / розщеплювач / контрольна точка / жолоб) · фіксація (позиція / орієнтація / обидві) · мета (кількість цілей / торкнутися всіх / дійти до однієї) · вимір (2D / 3D з ярусами).

## Цікавинки для курсу
- Трасування променя на 5×5 з дзеркалами й гранями «ціль/дзеркало» — 📎.
- Розщеплювач: промінь як дерево гілок, захист від циклів (стан клітина+напрямок у множині відвіданих) — 🥉.
- Перевірка умови «промінь торкнувся всіх жетонів, засвічено рівно N цілей» — 🌱.
- Розвʼязувач Laser Maze перебором розстановок і поворотів з відсіканням — 🥇.
- Gravity Maze: симуляція кульки по ярусах веж як граф переходів «клітина-висота» — 🥉; 3D-рендер веж з обертанням камери — 🥈.
- Редактор картки-завдання з позначками «фіксовано / вільно / до додавання» — 📎.

## Мапа на каталог
- Є: `beam-tracing` · `mirror-reflect` · `piece-rotate-flip` (поворот жетона) · `drag-drop-piece` · `cell-click` · `level-bank` · `puzzle-select` · `level-select` · `level-unlock` · `difficulty-levels` · `level-solver` · `reachability-check` (кулька до цілі) · `height-levels` (яруси веж) · `gravity-fall` · `in-game-editor` · `game-screen` · `end-screen` · `help-window` · `undo-redo`.
- Уже в корпусі: `+beam-splitter` (Khet).
- **Нема** → пропозиції карток:
  - `+challenge-card-setup` «Картка-завдання: стартові деталі на полі + список до додавання» · levels/format · 📎.
  - `+fixed-vs-free-orientation` «Позначка, чи орієнтацію деталі можна змінювати» · levels/format · 🌱.
  - `+must-use-all-pieces` «Розвʼязок дійсний лише з усіма деталями набору» · game-logic/constraints · 🌱.
  - `+beam-touches-all` «Промінь мусить торкнутися кожної деталі» · game-logic/constraints · 🌱.
  - `+target-count-goal` «Засвітити рівно N цілей (обрати які)» · game-logic/win · 🌱.
  - `+placement-blocker` «Клітина, куди не можна ставити, але промінь проходить» · entities/legality · 🌱.
  - `+marble-path-sim` «Симуляція кульки крізь жолоби» · entities/move · 🥉.
  - `+3d-tower-stack` «Деталі ставляться одна на одну ярусами» · interface/render · 🥈.
  - `+simulate-button` «Кнопка пуску: побудова → перевірка анімацією» · interface/input · 🌱.

## Пропозиції до словників
- `+trigger:beam_hit(beam, a)` — промінь торкнувся сутності (вже пропонував Khet; тут — друга гра).
- `+trigger:marble_stopped(marble)` — кулька зупинилась (кінець симуляції).
- `+cond:hit_side(a, side)` — з якого боку влучено (ціль лише червоною гранню).
- `+cond:all_pieces_used` — усі деталі з набору на полі.
- `+effect:emit_beam(source)` · `+effect:reflect(beam, deg)` · `+effect:split_beam(beam)` — оптика (Khet, Deflektor).
- `+effect:release_marble(where)` — пустити кульку зі старту.
- `+ui:beam-preview` · `+ui:pieces-tray` · `+ui:orientation-lock-badge`.
- `+window:challenge-card`.
- `+card:beam-touches-all` · `+card:challenge-card-setup` · `+card:marble-path-sim`.

## Джерела
- ⭐ [GeekDad: Laser Maze (2013)](https://geekdad.com/2013/06/laser-maze/) — склад, сітка 5×5, жетони, знак «?», 60 карток, 1–3 цілі, «торкнутися всіх жетонів», подвійне влучання.
- [ThinkFun: Laser Maze instructions (PDF)](https://legacy.thinkfun.com/wp-content/uploads/2013/09/Laser-1014-Instructions.pdf) — офіційні правила; зміст бачив лише у фрагментах пошуку (розщеплювач, блокатор, ціль/дзеркало, єдиний розвʼязок).
- [OfficialGameRules: Gravity Maze](https://officialgamerules.org/game-rules/gravity-maze/) — сетап за карткою, обертання веж, лише вказані вежі, кулька до цільової вежі.
- [Presents of Mind: Gravity Maze](https://www.presentsofmind.com.au/game/gravity-maze-by-thinkfun-2/) — склад (сітка, 10 веж, 3 кульки), 60 завдань.
- YouTube: пошук «ThinkFun Laser Maze», «ThinkFun Gravity Maze».

## Непевне
- (?) Рік: Laser Maze — огляд 2013 (черга каже 2012); Gravity Maze — 2014 за чергою, джерела рік не дають.
- (?) Розмір сітки Gravity Maze (черга: 3×3) — жодне відкрите джерело не називає.
- (?) Склад Gravity Maze: ThinkFun — «10 веж», інші продавці — «9 будівельних + цільова»; типи веж за формою не перелічені.
- (?) Чи мусить кулька пройти **крізь усі** вежі (одна версія інструкції) чи лише дійти до цільової (інша) — у видачі пошуку обидва формулювання.
- (?) Кількість рівнів складності й розподіл 60 карток — у джерелах лише «Beginner → Expert»; деякі видання Laser Maze замість подвійного дзеркала мають звичайне.
- (?) Цифрових версій від ThinkFun не перевірено; вікна гіпотетичні. Laser Maze за families.md ближча до `connect-rotate` — файл спільний за дозволом куратора.
