---
title: Mouse Trap
slug: mouse-trap
aka: [Мишоловка]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 1981
platforms: [arcade, ColecoVision, Intellivision, Atari 2600]
links:
  - {kind: play, url: "https://archive.org/details/arcade_mtrap", best: true, note: "Internet Arcade — грати; кольори дверей, очки котів, 32 призи, яструб і IN"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mouse_Trap_(1981_video_game)", note: "двері, кістки, IN, яструб, різниця портів"}
  - {kind: other, url: "https://www.arcade-museum.com/Videogame/mouse-trap", note: "KLOV: 4 кнопки Red/Yellow/Blue/Dog"}
  - {kind: other, url: "https://pixelatedarcade.com/games/mouse-trap", note: "опис: двері рухає лише миша, IN як схованка"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=mouse+trap+exidy+1981+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, collect-all, touch-death, player-death, chase-player, temporary-modes, button-toggle, teleport-random-exit, inventory-items, spawn-schedule, respawn, escalating-kill-points, event-points, sequential-levels, progress-acceleration, mode-indicator, status-panel, game-screen, +color-door-sets, +wall-ignoring-enemy, +stored-power-up, +prize-ladder, +center-bonus-item]
proposes: ["+effect:toggle_block", "+effect:toggle_group", "+ui:power-stock", "+card:color-door-sets", "+card:stored-power-up", "+card:wall-ignoring-enemy"]
author: opus
date: 2026-11-09
---

# Mouse Trap — Pac-Man, де лабіринт перебудовуєш кнопками трьох кольорів, а енерджайзер носиш у кишені

## Суть
Миша їсть увесь сир у лабіринті, тікаючи від котів. Головна механіка — **три набори кольорових дверей** (жовті, червоні, сині): кнопка свого кольору перемикає всі двері набору, і гравець на ходу відрізає котам шлях. Кістки — не миттєвий енерджайзер, а **запас**: мишу на час перетворює на собаку окрема кнопка, коли гравець вирішить. Яструб, що літає понад лабіринтом, ловить і мишу, і собаку; від нього рятує лише центральна клітка IN, яка водночас телепортує мишу у випадковий кут.

## Поле і час
- Клітинний лабіринт одного екрана; у центрі — поле «IN»; кістки — у кутах.
- Двері — частини стін зі станом, згруповані за кольором; набір перемикається цілим.
- Real-time; коти виходять по одному, зʼїдені повертаються швидшими.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Миша | player | життя; запас кісток | рух 4 напрямки; їсть сир |
| Собака | player (стан миші) | тривалість | їсть котів; кінчається за часом |
| Сир | pickup | — | очки; усі зʼїдено → рівень пройдено |
| Кістка | pickup | у кутах | йде в запас; переходить між рівнями й життями |
| Двері (жовті / червоні / сині) | gate | колір; положення | перемикаються кнопкою свого кольору; коти їх не рухають |
| Кіт | enemy | до 6; швидкість | переслідує; дотик вбиває мишу |
| Яструб | enemy | — | періодично пролітає; ловить мишу й собаку |
| Поле IN | static | центр | телепорт миші у випадковий кут; збиває яструба |
| Приз | pickup | щабель 1–32 | один на полі; взяття → наступний, дорожчий, в іншому місці |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(mouse, dir)`.
- КОЛИ `input(button_color)` → ТО `custom: «усі двері цього кольору перемикаються»`.
- КОЛИ `contact(mouse, cheese)` → ТО `pickup`, `score(n)`.
- КОЛИ `contact(mouse, bone)` → ТО `pickup` (у запас кісток).
- КОЛИ `input(dog)` → ЯКЩО `has(mouse, bone)` → ТО `use(mouse, bone)`, `set_state(mouse, dog, duration)`.
- КОЛИ `contact(mouse, cat)` → ЯКЩО `state(mouse, dog)` → ТО `disappear_b`, `score(100 → 300 → 500 → 700 → 900)`; кіт повертається швидшим (`respawn`, `speed(cat, +n)`).
- КОЛИ `contact(mouse, cat)` → ЯКЩО `not state(mouse, dog)` → ТО `lose` (життя −1).
- КОЛИ `input(dog)` → ТО `custom: «серія очок за котів скидається до 100»`.
- КОЛИ `schedule(list)` → ЯКЩО `count(cat, <, 6)` → ТО `spawn(cat)`; на старті 2, решта по одному.
- КОЛИ `timer(every)` → ТО `spawn_at(hawk, edge)`; яструб летить крізь стіни (?) і полює.
- КОЛИ `contact(hawk, mouse)` → ТО `lose` — незалежно від стану собаки.
- КОЛИ `enter(mouse, in_box)` → ТО `teleport(mouse, random_corner)`, `custom: «яструб летить навмання й покидає лабіринт»`.
- КОЛИ `picked(mouse, prize)` → ТО `score(1000 + 200·(k−1))`, `spawn_at(prize_k+1, elsewhere)`; після 32-го або втрати життя — з першого.
- КОЛИ `all_gone(cheese)` → ТО `score(10000)`, `next_level`; ЯКЩО `state(mouse, dog)` → наступний рівень мишею-собакою.
- Перемога: нема. Поразка: 0 життів. Рахунок: сир, коти серією, призи 1000…7200, 10 000 за рівень.

## Керування і ввід
- Джойстик 4 напрямки + 4 кнопки: Red, Yellow, Blue (двері) і Dog (кістка).
- Atari 2600: одна кнопка — довге натискання перемикає всі двері, коротке — кістка.
- 1–2 гравці по черзі.

## Вікна, меню, HUD
- `splash-screen` / атракт (?).
- `game-screen` — лабіринт; HUD: `score`, `hi-score` (?), `lives`, запас кісток (`custom: «power-stock»`), поточний приз (?).
- Переходи: атракт → (монета) game-screen → (сир зʼїдено) наступний рівень → (0 життів) атракт.

## Фічі поза полем
- `levels-sequential`; коти швидшають, додається яструб.
- ColecoVision: опція прибрати яструба (`custom-rules`), 15 призів замість 32.
- Intellivision: звукове попередження перед виходом кота (`sound-warnings`).
- Нема паузи, збережень.

## Варіації й родичі
- Порти: ColecoVision, Intellivision (інші очки: сир 90, коти 100…1100), Atari 2600 (один набір дверей, без яструба, IN і призів, 3 коти).
- Родичі: Pac-Man, Lady Bug (двері-турнікети від проходу), Lock 'n' Chase (двері, які зачиняє гравець), Chip's Challenge (кнопки, що перемикають стіни).
- Осі: **як керують дверима** (проходом — Lady Bug / кнопкою кольору — Mouse Trap / ставлять позаду — Lock 'n' Chase); **енерджайзер** (миттєвий / у запасі з кнопкою); **ворог поза правилами поля** (яструб крізь стіни).

## Цікавинки для курсу
- Набори дверей за кольором, що перемикаються однією дією, — 🥉: стан групи стін + перерахунок шляху котів.
- Кістки як інвентар із застосуванням за кнопкою, що переживає життя й рівні, — 📎.
- Яструб, що ігнорує стіни, і клітка-телепорт, яка його збиває, — 📎.
- Драбина призів: 32 щаблі з кроком +200, скидання при смерті — 🌱.
- Серія очок за котів, скинута новою кісткою, — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `collect-all` · `touch-death` · `player-death` · `chase-player` · `temporary-modes` (собака) · `button-toggle` (кнопка перемикає двері-цілі) · `teleport-random-exit` (IN) · `inventory-items` (кістки) · `spawn-schedule` (коти по одному) · `respawn` (зʼїдений кіт повертається) · `escalating-kill-points` (найближче: серія 100→900, але приріст +200, не подвоєння) · `event-points` · `sequential-levels` · `progress-acceleration` · `mode-indicator` · `status-panel` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+color-door-sets` «Набори дверей за кольором» · entities/interact · 🥉 · слот {colors: 3}.
  - `+wall-ignoring-enemy` «Ворог летить крізь стіни» · entities/move · 🌱.
  - `+stored-power-up` «Бонус у запасі, активація кнопкою» · entities/state · 📎.
  - `+prize-ladder` «Драбина призів зі скиданням» · game-logic/score · 🌱 · слот {steps: 32}.
  - `+center-bonus-item` (є в Lady Bug) — приз зʼявляється в іншому місці після взяття.

## Пропозиції до словників
- `+effect:toggle_block` — перемкнути двері/стіну між станами.
- `+effect:toggle_group(color)` — перемкнути всі сутності групи одним вводом.
- `+ui:power-stock` — запас енерджайзерів (кістки).
- `+card:color-door-sets`, `+card:stored-power-up`, `+card:wall-ignoring-enemy` — див. вище.

## Джерела
- ⭐ [Internet Arcade: Mouse Trap](https://archive.org/details/arcade_mtrap) — грати; жовті/червоні/сині двері, кнопка Dog, очки котів 100…900, 32 призи 1000…7200, 10 000 за рівень.
- [Wikipedia: Mouse Trap (1981)](https://en.wikipedia.org/wiki/Mouse_Trap_(1981_video_game)) — 6 котів (2 на старті), IN, яструб, кістки переходять між рівнями, порти.
- [KLOV: Mouse Trap](https://www.arcade-museum.com/Videogame/mouse-trap) — 4 кнопки Red/Yellow/Blue/Dog, 1–2 гравці по черзі.
- [Pixelated Arcade: Mouse Trap](https://pixelatedarcade.com/games/mouse-trap) — двері рухає лише миша, стартова кістка.
- YouTube: пошук «mouse trap exidy 1981 arcade gameplay».

## Непевне
- (?) Яструб: Wikipedia — ігнорує стіни; Pixelated Arcade — «не перелітає стіни». Також: зʼявляється періодично чи лише на пізніх рівнях.
- (?) Тривалість собаки; стартові життя; очки за сир на аркаді.
- (?) Як саме виглядає перемикання: двері відкриваються/закриваються чи переставляються з одного проходу в інший.
- (?) Чи миша стартує з однією кісткою (Pixelated Arcade) — інші джерела не кажуть.
- (?) Чи яструб покидає лабіринт одразу після IN чи після блукання.
