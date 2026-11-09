---
title: Sprouts (Паростки)
slug: sprouts
aka: [Паростки]
family: connect-rotate
also: [chess-abstract]
klass: cursor
axes:
  field: free
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: survive
year: 1967
platforms: [paper, iOS, macOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Sprouts_(game)", best: true, note: "правила, життя точок, межі 2n…3n−1 ходів, normal/misère, таблиця розвʼязаних n, Brussels Sprouts і комбінований варіант"}
  - {kind: other, url: "https://www.cs.cmu.edu/~sleator/papers/Sprouts.htm", note: "Applegate, Jacobson, Sleator 1991: алгоритм з рядковим представленням позицій, усі ігри до 11 точок, гіпотеза Sprouts (лише абстракт)"}
  - {kind: play, url: "https://apps.apple.com/us/app/sprouts/id6749350046", note: "Sprouts+ (2025): 2–7 точок, кольорові стани точок, гра на одному чи двох пристроях, Game Center"}
  - {kind: other, url: "http://sprouts.tuxfamily.org", note: "SproutsWiki Lemoine і Viennot — код і бінарники розвʼязувача (посилання з Wikipedia, сторінка не відкрилась)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sprouts+game+Conway", note: "пошук; пояснення й партії"}
stage: v1
coverage: 50
mechanics: [hot-seat, turn-enforcement, no-moves-left, ai-opponent, ai-minimax, level-solver, state-string, online-multiplayer, rule-variants, reachable-highlight, game-screen, end-screen, match-setup, help-window, +no-crossing-edges, +misere-win, +spawn-on-edge, +vertex-degree-cap, +freehand-edge-draw, +planar-face-check]
proposes: ["+effect:draw_edge", "+cond:same_face", "+cond:degree", "+role:node", "+role:edge", "+ui:liveness-dots", "+card:no-crossing-edges", "+card:spawn-on-edge", "+card:planar-face-check"]
author: opus
date: 2026-11-09
---

# Sprouts — двоє по черзі зʼєднують точки кривою й ставлять на ній нову; не перетинати, не більше трьох ліній на точку; хто не може ходити — програв

## Суть
Паперова гра John Conway і Michael Paterson (Кембридж). Починають з n точок; хід — провести криву між двома точками (або петлю з точки в неї саму) і поставити на кривій нову точку. Крива не може торкатись чи перетинати жодну лінію, а до точки може сходитись не більше трьох ліній. Normal play — хто зробив останній хід, виграв; misère — програв. Межа сімʼї: «поле» не сітка, а планарний малюнок, що росте; найближчі родичі в корпусі — [Hackenbush](hackenbush.md) і [Sim](sim-pencil-game.md) (ігри на графі).

## Поле і час
- Аркуш паперу; стан — плоский граф (точки + криві), де важать не координати, а **області**, на які криві ділять площину: дві точки можна зʼєднати, лише якщо вони на межі однієї області (`field: free`, логічно — топологія).
- Хід = одна крива + одна точка; покроково, без часу й випадковості.
- Скінченність: кожна точка має 3 «життя», гра з n точок стартує з 3n життів, кожен хід знімає рівно одне (−2 на кінцях, +1 у нової точки). Партія триває не більше 3n−1 і не менше 2n ходів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Жива точка | node (custom) | ліній 0–2, життів 3 − ліній | може бути кінцем нової кривої |
| Нова точка | node (custom) | одразу 2 лінії, 1 життя | ставиться всередині щойно проведеної кривої, не на її кінцях |
| Мертва точка | node (custom) | 3 лінії | більше не бере участі |
| Survivor | node (custom) | 1 життя наприкінці | жива, але недосяжна; щонайменше одна є завжди (точка останнього ходу) |
| Pharisee | node (custom) | мертва | мертва точка, що не є сусідом жодного survivor-а; подовжує гру |
| Крива | edge (custom) | кінці; петля рахується за 2 лінії | не торкається й не перетинає інших ліній і себе |
| Область | zone | межа з кривих | точки з різних областей зʼєднати не можна |
| Гравець | player | перший / другий | ходять по черзі |
| Хрест (Brussels Sprouts) | node (custom) | 4 вільні кінці | варіант: зʼєднують вільні кінці, а не точки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `spawn(spot, n)` — n точок, кожна з 3 життями (`counter(lives, 3n)`).
- КОЛИ `input(draw, spot_a, spot_b)` → ЯКЩО `turn_of(side)` and `custom: «у кожного кінця < 3 ліній; петля a = a — лише в точки з ≤ 1 лінією»` (+cond:degree) and `custom: «a і b на межі однієї області»` (+cond:same_face) and `custom: «крива не торкається й не перетинає жодної лінії, зокрема себе»` → ТО `custom: «провести криву a–b»` (+effect:draw_edge).
- КОЛИ `after(draw_edge)` → ТО `spawn(spot, on_new_curve)` — не на кінці кривої; `set_value(new_spot, 2)` (вважається, що в неї вже 2 лінії), `counter(lives, -1)`, `end_turn`.
- КОЛИ `input(draw, a, b)` → ЯКЩО `custom: «будь-яка умова вище порушена»` → ТО `block`.
- КОЛИ `custom: «до точки сходяться 3 лінії»` → ТО `set_state(spot, dead)`.
- КОЛИ `turn_start(side)` → ЯКЩО `custom: «нема двох живих точок на межі однієї області і нема точки з ≤ 1 лінією для петлі»` → ТО `no_moves(side)`.
- КОЛИ `no_moves(side)` → ЯКЩО `mode(normal)` → ТО `lose(side)`, `window(end-screen)`.
- КОЛИ `no_moves(side)` → ЯКЩО `mode(misere)` → ТО `win(side)` (хто зробив останній хід, програв).
- Межі тривалості: життів після m ходів = 3n − m; наприкінці кожен survivor має рівно 1 життя, тож m ≤ 3n − 1; кожна область містить survivor-а з двома мертвими сусідами, тож m ≥ 2n.
- Стратегія: один гравець ділить площину на замкнені області (гра коротшає), другий тримає її відкритою й плодить pharisee (гра довшає) — боротьба за парність числа ходів.
- Brussels Sprouts: КОЛИ `input(draw, end_a, end_b)` → ЯКЩО `custom: «два вільні кінці, крива без перетинів»` → ТО `custom: «провести криву й перекреслити її коротким штрихом — два нові вільні кінці»`; з n хрестів партія завжди триває рівно 5n − 2 ходів, тож переможець відомий наперед.
- Комбінований варіант: на новій кривій гравець обирає `choose(dot | cross)`; тривалість від 2n до 5n − 2.
- Перемога: normal — суперник не має ходу · misère — ти не маєш ходу · Рахунку нема.

## Керування і ввід
- Папір: олівець; криву ведуть довільно, нову точку ставлять будь-де на ній.
- Цифрова версія (Sprouts+): гра на одному пристрої на двох або на двох пристроях через локальний Wi-Fi чи Game Center; точки підсвічені кольором за станом — уже має 3 лінії / досяжна іншою точкою / заблокована. Спосіб малювання (drag пальцем) — (?).

## Вікна, меню, HUD
- (цифрова версія) `main-menu` → `match-setup`: кількість точок (2–7), один пристрій / два / випадковий суперник за рівнем (Beginner / Intermediate / Advanced) → `game-screen` → `end-screen`.
- `game-screen`: аркуш з точками й кривими; `turn-indicator`; кольорові стани точок (`+ui:liveness-dots`) — живою лишається видима підказка, де ще є хід.
- `end-screen`: хто зробив останній хід, скільки ходів тривала партія.
- `help-window` — правила (цифрова версія, ?).
- Переходи: match-setup → game-screen → (нема ходу) end-screen → match-setup.

## Фічі поза полем
- `hotseat` і `online-multiplayer` (Game Center, SharePlay, Wi-Fi) у Sprouts+.
- `custom-rules`: кількість точок, normal / misère, Brussels Sprouts, комбінований варіант.
- `ai-opponent-levels` — розвʼязувачі є (Applegate et al., Lemoine і Viennot, SPOTS 2025), але готового AI в цифровій версії не бачив (?).
- Sprouts+ — 2-точкові партії безлімітні, більші — за внутрішні токени.

## Варіації й родичі
- Brussels Sprouts (хрести з 4 вільними кінцями, рівно 5n − 2 ходів) і комбінований варіант «точка або хрест».
- Misère Sprouts — грають організовано (World Game of Sprouts Association); гіпотеза — період 6 із винятками n = 1 і n = 4.
- Корпус: [Hackenbush](hackenbush.md) — ребра стирають, хто не має ходу, програв (та сама normal play); [Sim](sim-pencil-game.md) — ребра фарбують на фіксованому K6; [Shannon switching](shannon-switching.md) — захоплення ребер для звʼязку; [Black Path Game](black-path-game.md) — спільний шлях на сітці.
- Осі варіацій: **що додає хід** — точку / хрест / вибір · **ліміт ліній на точку** — 3 (точка) / 4 вільні кінці (хрест) · **мета** — останній хід виграє / програє · **поле** — площина / інші поверхні (?).

## Цікавинки для курсу
- Лічильник життів 3n − m і межі 2n … 3n − 1 ходів — 🌱: інваріант, що доводить скінченність гри.
- Цифрове малювання: крива як ламана з пальця, перевірка самоперетину й перетину з усіма іншими (відрізок × відрізок), вставка нової точки в середину — 🥉.
- Перевірка «a і b на межі однієї області»: обхід граней планарного графа або flood fill по растру аркуша — 🥈.
- Брюссельська «гра для одного»: 5n − 2 через формулу Ейлера (v − e + f = 1 + k) — 📎 як задача на доведення й тест.
- Позиція рядком: області як цикли точок, склеювання ізоморфних (ідея Applegate, Jacobson, Sleator) — 🥇.
- Розвʼязувач: alpha-beta з хешем позицій → nimber-розклад на незалежні області (Lemoine і Viennot), proof-number search (SPOTS) — 👑.

## Мапа на каталог
- Є: `hot-seat` + `turn-enforcement` ↔ двоє по черзі; `no-moves-left` ↔ кінець гри; `ai-opponent` + `ai-minimax` + `level-solver` ↔ розвʼязувачі; `state-string` ↔ рядкове представлення позицій; `online-multiplayer` ↔ Game Center; `rule-variants` ↔ normal / misère / Brussels; `reachable-highlight` ↔ кольори досяжних точок; `game-screen`, `end-screen`, `match-setup`, `help-window`.
- **Нема** → пропозиції карток:
  - `+no-crossing-edges` (Next Station: London, TwixT) — нова лінія не перетинає старих; підтвердження.
  - `+misere-win` (Шашки) — перемикач «останній хід програє»; підтвердження.
  - `+spawn-on-edge` «Хід створює нову вершину на новому ребрі» · entities/state · 🌱.
  - `+vertex-degree-cap` «Ліміт ребер на вершину, петля = 2» · entities/legality · 🌱 · слот {cap: 3}.
  - `+freehand-edge-draw` «Ребро — довільна крива пальцем/мишею» · interface/input · 🥉.
  - `+planar-face-check` «Дві вершини на межі однієї грані» · game-logic/constraints · 🥈.

## Пропозиції до словників
- `+effect:draw_edge` — провести ребро між двома вершинами (підтвердження: Next Station: London, Tentai Show).
- `+cond:same_face` — дві вершини лежать на межі однієї області плоского малюнка.
- `+cond:degree` — кількість ребер у вершини порівняно з N (петля = 2).
- `+role:node` / `+role:edge` — вершина й ребро як сутності поля без сітки (підтвердження: Sim, Shannon, Hackenbush).
- `+ui:liveness-dots` — колір точки показує її стан: мертва / досяжна / заблокована (Sprouts+).
- `+card:no-crossing-edges`, `+card:spawn-on-edge`, `+card:planar-face-check`.

## Джерела
- ⭐ [Wikipedia: Sprouts (game)](https://en.wikipedia.org/wiki/Sprouts_(game)) — правила, life-аналіз і межі 2n … 3n − 1, survivors і pharisees, таблиця результатів normal play (Conway, Mollison, Applegate et al., Purinton, Lemoine і Viennot, SPOTS 2025), misère, Brussels Sprouts і комбінований варіант.
- [Applegate, Jacobson, Sleator: Computer Analysis of Sprouts](https://www.cs.cmu.edu/~sleator/papers/Sprouts.htm) — абстракт: рядкове представлення, що склеює різні планарні графи, хеш позицій, усі ігри до 11 точок, гіпотеза «перший програє при n ≡ 0, 1, 2 (mod 6)».
- [App Store: Sprouts+](https://apps.apple.com/us/app/sprouts/id6749350046) — цифрова версія 2025: 2–7 точок, кольорові стани точок, один / два пристрої, Game Center, рівні суперників.
- [SproutsWiki](http://sprouts.tuxfamily.org) — код розвʼязувача Lemoine і Viennot (посилання з Wikipedia; сторінка не відповіла).
- YouTube: пошук «Sprouts game Conway».

## Непевне
- (?) Рік: Wikipedia — «на початку 1960-х», Sprouts+ — 1967; у шапці 1967.
- (?) Як саме в Sprouts+ малюють криву і чи є AI-суперник та undo — опис застосунку цього не каже.
- (?) Варіанти на інших поверхнях (тор тощо) — не перевірено, у Wikipedia не бачив.
- (?) Деталі рядкової нотації позицій — бачив лише абстракт Applegate et al.; повний текст (PDF) не відкривав.
