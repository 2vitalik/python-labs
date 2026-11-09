---
title: Dots and Boxes (Крапки й квадрати)
slug: dots-and-boxes
aka: [La Pipopipette, Boxes, Dots and Dashes, Game of Dots, Pigs in a Pen, Крапки й квадрати, Квадратики]
family: chess-abstract
also: [pencil-logic]
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: score
year: 1889
platforms: [paper, web, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dots_and_boxes", best: true, note: "правила, додатковий хід, ланцюги й double-cross, американська/шведська/ісландська дошки, Strings-and-Coins, PSPACE-повнота"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=dots+and+boxes", note: "пошук цифрових версій"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=dots+and+boxes", note: "пошук BGG (не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dots+and+boxes+strategy+double+cross", note: "пошук; стратегія ланцюгів"}
stage: v1
coverage: 70
mechanics: [edge-marking, cell-click, hover-highlight, last-move-highlight, hot-seat, turn-enforcement, ai-opponent, ai-random, ai-greedy, ai-minimax, event-points, completion-detection, no-moves-left, field-size-picker, difficulty-levels, game-screen, main-menu, end-screen, help-window, settings-window, score-records, state-as-data, unit-tests, +edge-claim-box, +extra-turn-on-score, +board-start-preset, +strings-and-coins-dual]
proposes: ["+axis:move-site", "+cond:sides_drawn", "+ui:edge-hover", "+ui:box-owner-mark", "+feature:board-start-preset", "+card:edge-claim-box", "+card:extra-turn-on-score", "+card:strings-and-coins-dual"]
author: opus
date: 2026-11-09
---

# Dots and Boxes — ходиш по ребрах, а не по клітинах: закрив квадрат — забрав очко і ходиш ще

## Суть
Паперова гра двох (інколи більше): на сітці крапок гравці по черзі проводять по одному відрізку між сусідніми крапками. Хто провів **четверту сторону** квадрата 1×1, забирає його (ставить ініціал) і **ходить ще раз**. Коли всі ребра проведено, перемагає той, у кого більше квадратів. Незвичне для корпусу: хід ставиться на **ребро**, а не в клітину, і сама «премія» (додатковий хід) створює глибоку стратегію ланцюгів.

## Поле і час
- Сітка крапок (m+1)×(n+1) → m×n квадратів; ребра — горизонтальні й вертикальні відрізки між сусідніми крапками. Розмір довільний: 2×2 квадрати — для навчання, 5×5 — для досвідчених.
- Логічно три шари: крапки (статичні), ребра (порожнє / проведене), квадрати (нічий / власника).
- Старт: американська дошка — порожня; шведська — з проведеним зовнішнім контуром; ісландська — з проведеними лише лівим і нижнім краями.
- Покроково; хід = одне ребро; ланцюг додаткових ходів може тривати довго (забрати цілий ланцюг квадратів).
- Варіанти полів: трикутна й гексагональна сітки; дуальна форма Strings-and-Coins — на довільному графі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Крапка | static | вузол сітки | лише кінці ребер |
| Ребро | mark | порожнє / проведене; хто провів — не важливо | проводиться раз і назавжди; належить 1 або 2 квадратам |
| Квадрат | zone | 4 сторони; власник: нічий / гравець | дістається тому, хто провів його 4-ту сторону |
| Ланцюг | zone | послідовність квадратів, де вже по 2 сторони | будь-який хід у ньому віддає супернику весь ланцюг (стратегічне поняття, не правило) |
| Гравець | player | рахунок квадратів | ходить ребром; після захоплення — ще раз |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, edge)` → ЯКЩО `turn_of(side)` і `custom: «ребро ще не проведене»` → ТО `mark(edge, drawn)`; інакше `block`.
- КОЛИ `after(mark)` → ЯКЩО `pattern(region_closed)` — `custom: «у сусіднього квадрата тепер 4 сторони»` → ТО `set_side(box, side)`, `score(1)`, `extra_move`.
- КОЛИ `after(mark)` → ЯКЩО ребро закрило одразу два квадрати → ТО обидва `set_side(box, side)`, `score(2)`, `extra_move` (лише один додатковий хід).
- КОЛИ `after(mark)` → ЯКЩО `not pattern(region_closed)` → ТО `end_turn`.
- Додатковий хід — обовʼязковий: гравець мусить провести ще одне ребро (пасу нема).
- КОЛИ `no_moves(all)` — усі ребра проведено → ТО `game_over`; ЯКЩО `counter(boxes, >, opponent)` → `win`; рівні рахунки — `draw` (можливо лише при парній кількості квадратів).
- КОЛИ `input(click, edge)` → ЯКЩО `custom: «ребро стає 3-ю стороною квадрата»` (`+cond:sides_drawn(box, ==, 3)`) → ТО гра дозволяє, але це «подарунок» супернику (стратегія, не заборона).
- Strings-and-Coins (дуал): КОЛИ `input(cut, string)` → ЯКЩО `custom: «у монети не лишилось ниток»` → ТО `pickup(coin)`, `extra_move`.
- Перемога: більше квадратів · Поразка: менше · Рахунок: кількість квадратів.

## Керування і ввід
- Папір: проводиш олівцем відрізок; у закритому квадраті ставиш свій ініціал.
- (цифрова версія) Наведення на проміжок між двома крапками підсвічує ребро-кандидат (`edge-hover`); клік — провести. Ребро забарвлюється в колір гравця (для читабельності), квадрат зафарбовується кольором власника.
- Після захоплення курсор лишається в того самого гравця; індикатор ходу не перемикається.
- На тачі — тап по ребру або свайп від крапки до сусідньої.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Проти AI · Двоє на одному пристрої · Онлайн (?) · Правила → `help-window` · Налаштування → `settings-window`.
- `settings-window` / `match-setup`: розмір поля (рядки × стовпці квадратів), стартова дошка (американська / шведська / ісландська), кількість гравців, рівень AI.
- `game-screen`: сітка крапок; проведені ребра; зафарбовані квадрати з ініціалом/кольором (`box-owner-mark`); `score` кожного; `turn-indicator`; `last-move-highlight` (останнє ребро, або вся серія ребер поточного ходу); кнопка `undo-button` проти AI.
- `end-screen`: рахунок, переможець, «Ще раз».
- Переходи: main-menu → settings-window → game-screen → end-screen → game-screen / main-menu.

## Фічі поза полем
- `custom-difficulty` — довільний розмір поля; `board-start-preset` — американська/шведська/ісландська.
- `ai-opponent-levels`: випадковий → жадібний («бери все, не давай 3-ю сторону») → AI, що знає правило ланцюгів і double-cross → пошук по дереву.
- `hotseat`, `local-multiplayer` на 3+ гравців, `undo` проти AI.
- `stats` — перемоги/поразки за розміром поля.

## Варіації й родичі
- **Шведська / ісландська дошки** — частина ребер проведено на старті; змінює парність і хто контролює ланцюги.
- **Strings-and-Coins** — дуальна форма: монети з нитками, різання останньої нитки монети забирає монету і дає хід; грається на будь-якому графі.
- Трикутні й гексагональні сітки (квадрат → трикутник / шестикутник).
- Не плутати з «Dots» (окрема гра, де оточують крапки суперника, ближче до го).
- Родичі за ідеєю «закрив область — твоя»: go (територія), Xonix/Qix (заливка), `dots-two-dots` у корпусі — інша гра.
- **Осі варіацій**: де хід (клітина / ребро / вершина) · премія за захоплення (додатковий хід / нема) · стартова розмітка (порожня / контур / частково) · топологія (квадрат / трикутник / гекс / довільний граф) · мета (більше / менше квадратів — misère (?)).

## Цікавинки для курсу
- Модель «хід на ребрі»: зберігати горизонтальні й вертикальні ребра окремими масивами, мапити ребро ↔ 1–2 квадрати — 🌱.
- Додатковий хід за захоплення як зміна черговості (не `end_turn`) — 🌱; правильно для «два квадрати одним ребром» — 📎.
- Клік по ребру: hit-test «найближчий проміжок між крапками», hover-підсвітка — 📎.
- Жадібний AI: бери будь-який 4-й бік, інакше не давай 3-го — 📎; AI з правилом ланцюгів і double-cross (віддати 2 квадрати, щоб суперник відкрив наступний ланцюг) — 🥈.
- Повний розвʼязувач на малих полях (мемоізація станів ребер як бітової маски) — 🥇; загальний випадок PSPACE-повний — 👑.
- Дуальність Dots-and-Boxes ↔ Strings-and-Coins як вправа на графи — 🥉.

## Мапа на каталог
- Є: `edge-marking` ↔ хід = провести ребро · `cell-click`, `hover-highlight` ↔ вибір ребра · `last-move-highlight` · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-random`, `ai-greedy`, `ai-minimax` · `event-points` ↔ очко за квадрат · `completion-detection`, `no-moves-left` ↔ кінець, коли ребер не лишилось · `field-size-picker`, `difficulty-levels` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `score-records`, `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+edge-claim-box` «Закрив останню сторону — клітина твоя» · game-logic/scoring · 🌱 · слоти {sides: 4|3|6}.
  - `+extra-turn-on-score` «Додатковий хід за захоплення» · game-logic/turns · 🌱 — також Kalah, Strings-and-Coins.
  - `+board-start-preset` «Передрозмічена стартова дошка» · settings · 🌱 · слоти {american, swedish, icelandic}.
  - `+strings-and-coins-dual` «Гра на довільному графі (дуал)» · field/topology · 🥉.

## Пропозиції до словників
- `+axis:move-site` — де ставиться хід: `cell` · `edge` · `vertex` (Dots and Boxes — edge; го — vertex/перетин; більшість — cell).
- `+cond:sides_drawn(box, op, n)` — скільки сторін клітини вже розмічено (3 = «подарунок»).
- `+ui:edge-hover` — підсвітка ребра-кандидата між двома крапками.
- `+ui:box-owner-mark` — ініціал/колір власника в захопленій клітині.
- `+feature:board-start-preset` — стартова дошка з частково проведеними ребрами.
- `+card:edge-claim-box`, `+card:extra-turn-on-score`, `+card:strings-and-coins-dual` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Dots and boxes](https://en.wikipedia.org/wiki/Dots_and_boxes) — правила, розміри для новачка/експерта, ланцюги, double-cross, жертви, американська/шведська/ісландська дошки, Strings-and-Coins, трикутні й гекс-сітки, PSPACE-повнота (Buchin et al., 2021), історія (Lucas, «La Pipopipette»).
- [Steam: пошук](https://store.steampowered.com/search/?term=dots+and+boxes) — цифрові версії (не відкривав).
- YouTube: пошук «dots and boxes strategy double cross».

## Непевне
- (?) Рік: Wikipedia відносить гру до «1889 introductions», але цитує публікацію Lucas 1895 року («L'arithmétique amusante»).
- (?) Чи додатковий хід обовʼязковий — стаття каже «takes another turn»; у звичних правилах так, у деяких наборах правил можна відмовитись (не перевірено).
- (?) Нічия при рівному рахунку — у статті не описана; очевидна лише для парної кількості квадратів.
- (?) Які розміри полів розвʼязано компʼютером і з яким результатом — стаття згадує аналіз David Wilson без чисел.
- (?) Misère-варіант (виграє той, хто має менше) — не бачив у джерелі.
