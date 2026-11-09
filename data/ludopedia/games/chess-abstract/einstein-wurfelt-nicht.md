---
title: "EinStein würfelt nicht!"
slug: einstein-wurfelt-nicht
aka: [EWN, "Einstein does not play dice", Ейнштейн не грає в кості, "EinStein Würfelt Nicht"]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: race
year: 2004
platforms: [board, iOS, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/EinStein_w%C3%BCrfelt_nicht!", best: true, note: "правила: 5×5, кубики 1–6, кидок обирає куб, найближчий вищий/нижчий, бʼє будь-кого, два способи перемоги; варіант 6×6 з двома кубиками"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/EinStein_w%C3%BCrfelt_nicht", note: "DE: уточнення вибору вищий/нижчий, без пасу, 3 і 4 гравці на 6×6 (Quattro), застосунок iOS"}
  - {kind: play, url: "https://ludii.games/details.php?keyword=EinStein%20W%C3%BCrfelt%20Nicht", note: "Ludii: правила, вільна розстановка в трикутнику, 3-Hirn-Verlag"}
  - {kind: official, url: "http://www.althofer.de/ewn-ursprung.html", note: "Ingo Althöfer про походження: BallaBalla → Würfel-Fussball → EWN (2004), видання, Best of Five на Little Golem"}
  - {kind: play, url: "https://www.littlegolem.net/jsp/games/gamedetail.jsp?gtid=einstein", note: "Little Golem: гра поштою, випадкова стартова позиція"}
  - {kind: other, url: "https://itunes.apple.com/app/einstein-wurfelt-nicht!/id981066027", note: "застосунок iOS (з DE-Wikipedia; не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=einstein+w%C3%BCrfelt+nicht+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [piece-capture, reach-exit, legal-move-highlight, selection-highlight, last-move-highlight, hot-seat, turn-enforcement, ai-opponent, ai-random, ai-greedy, ai-minimax, cell-click, drag-drop-piece, placement-screen, async-multiplayer, match-setup, game-screen, main-menu, end-screen, help-window, state-as-data, unit-tests, +die-selects-piece, +nearest-value-fallback, +friendly-fire-capture, +capture-all-win, +random-setup, +multi-round-match, +doubling-cube, +ai-expectimax]
proposes: ["+effect:roll_dice", "+cond:die_value", "+ui:dice-result", "+ui:required-piece-highlight", "+ui:match-score", "+card:nearest-value-fallback", "+card:doubling-cube", "+card:ai-expectimax"]
author: opus
date: 2026-11-09
---

# EinStein würfelt nicht! — кубик каже, яким номерним кубом ходити; гонка в протилежний кут, де бити можна й своїх

## Суть
Гра Ingo Althöfer (професор математики в Єні, 2004) на дошці 5×5: у кожного 6 кубів з номерами 1–6, що стартують у своєму куті. Кидок кубика обирає, яким кубом ходити; куб іде на 1 клітину в бік протилежного кута і знімає будь-який куб на цій клітині — і чужий, і свій. Виграє той, хто першим доведе куб у кут суперника або зніме всі його куби. Назва — гра слів: Einstein «Бог не грає в кості» та «один камінь» (*ein Stein*) — коли лишився один куб, кидати вже не треба.

## Поле і час
- Дошка 5×5, один шар; у клітині ≤1 куб.
- Старт: свої 6 кубів — у трикутнику свого кольору в куті (червоні — лівий верхній, сині — правий нижній); розстановка вільна (Ludii, DE) або випадкова (онлайн: inetplay, Little Golem).
- Покроково: кидок d6 → обовʼязковий хід; пасу нема. Кожен куб іде лише «вперед» до кута суперника: 3 напрямки.
- Матч: Best of Five на Little Golem (до 3 перемог; той, хто програв попередню, ходить першим); варіант з кубом подвоєння, як у нардах.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Куб гравця | piece | номер 1–6; сторона червона / синя | на 1 клітину: червоний — вправо, вниз, по діагоналі вниз-вправо; синій — вліво, вгору, по діагоналі вгору-вліво |
| Ігровий кубик (d6) | object | 1–6 | обирає, яким кубом ходити |
| Стартовий трикутник | zone | у куті кожного | тут розставляються куби |
| Цільовий кут | zone | кутова клітина суперника | куб, що дійшов сюди, виграє партію |
| Гравець | player | куби на полі | кидає й ходить; один куб — без кидка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «кожен розставляє куби 1–6 у трикутнику свого кута»` (онлайн — `custom: «випадкова розстановка»`).
- КОЛИ `turn_start(side)` → ЯКЩО `count(own_cubes, >, 1)` → ТО `custom: «кинути d6»` (`+effect:roll_dice`).
- КОЛИ `turn_start(side)` → ЯКЩО `count(own_cubes, ==, 1)` → ТО `custom: «кидок не потрібен: ходить єдиний куб»`.
- КОЛИ `input(move, cube, dir)` → ЯКЩО `turn_of(side)` і `custom: «номер cube = випадіння»` (`+cond:die_value`) і `custom: «dir — один із 3 напрямків до кута суперника, клітина в межах дошки»` → ТО `move(cube, dir)`, `end_turn`.
- КОЛИ `input(move, cube, dir)` → ЯКЩО `custom: «куба з випаденням N уже нема; cube — найближчий існуючий вищий або найближчий нижчий за N»` → ТО `move(cube, dir)`; якщо є лише вищі — обовʼязково найближчий вищий, лише нижчі — найближчий нижчий.
- КОЛИ `input(move, cube, dir)` → ЯКЩО `occupied(target, any_cube)` → ТО `disappear(target_cube)`, `move(cube, target)` — бʼє будь-кого, і свій куб теж.
- КОЛИ `input(move, cube, dir)` → ЯКЩО `custom: «target поза дошкою»` → ТО `block`.
- КОЛИ `reach(cube, enemy_corner)` → ТО `win`.
- КОЛИ `all_gone(enemy_cubes)` → ТО `win`.
- Матч: КОЛИ `counter(wins, ==, 3)` → ТО `win` матчу (Best of Five); КОЛИ `level_start` → ТО першим ходить той, хто програв попередню партію.
- Перемога: куб у куті суперника або всі його куби зняті · Поразка: навпаки · Нічиєї нема.

## Керування і ввід
- Настільна: кинути кубик, пересунути куб на 1 клітину.
- (цифрова версія) Кнопка/жест «кинути» → підсвічуються дозволені куби (один або два при відсутньому номері) і по 3 цільові клітини; клік — хід.
- Розстановка перед партією — drag кубів у трикутнику або «випадково».

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Грати · Проти AI (рівні за Elo, застосунок iOS) · Онлайн · Правила → `help-window`.
- `match-setup`: суперник, довжина матчу (1 / Best of Five), розстановка вільна / випадкова, варіант 6×6.
- Екран розстановки (картка `placement-screen`): трикутник, куби 1–6, «випадково», «готово».
- `game-screen`: дошка 5×5 з цільовими кутами; `dice-result` (випало N); `required-piece-highlight` (який куб або який із двох); `legal-move-highlight`; `last-move-highlight`; `turn-indicator`; `match-score`.
- `end-screen`: хто переміг і як (кут / усі зняті), рахунок матчу; Наступна партія.
- Переходи: main-menu → match-setup → розстановка → game-screen → end-screen → розстановка (наступна партія) / main-menu.

## Фічі поза полем
- `ai-opponent-levels` (iOS: програми Christian Donninger за Elo; ранні програми — McRandom Jörg Sameith для тестів попередника).
- `online-multiplayer` / гра поштою (Little Golem, MasterMoves, inetplay 2005–2008); `random-setup` онлайн.
- `custom-rules`: варіант 6×6, команди на 3–4 гравці, куб подвоєння.

## Варіації й родичі
- 6×6, по 10 кубів з номерами 2–6, 8–12, кидок двох кубиків (сума) — EN-Wikipedia.
- На 3 гравці (один проти пари) і на 4 «Quattro» (команди по двоє: діагональна або «longline» посадка) на 6×6 — DE-Wikipedia.
- Попередники Althöfer: BallaBalla (Zillions of Games, 2002) → Würfel-Fussball (2003, поле 7×5+2, 11 фішок, без взяття).
- Видання: Edition Perlhuhn (Reinhold Wittig, до виставки «Gott würfelt nicht»), камʼяне видання 3-Hirn-Verlag; офіційна гра виставки до Року Ейнштейна (2005).
- Родичі: [breakthrough-loa](breakthrough-loa.md) (гонка до краю з взяттям) · [halma-chinese-checkers](halma-chinese-checkers.md) (з кута в кут) · [kamisado](kamisado.md) (не ти обираєш, чим ходити) · [hexapawn](hexapawn.md) (мала дошка, повний перебір).
- **Осі варіацій**: хто обирає фігуру (гравець / кубик / колір клітини — Kamisado) · кого можна бити (лише ворога / будь-кого) · мета (кут / усіх зняти / обидва) · розстановка (фіксована / вільна / випадкова).

## Цікавинки для курсу
- Вибір куба за кидком з правилом «найближчий вищий/нижчий» — 🌱 (гарна вправа на крайні випадки).
- Генерація ходів: 1–2 куби × 3 напрямки, взяття своїх — 🌱.
- AI expectimax: вузли випадковості (6 результатів кидка) між ходами — 🥇; «Schwarz score» (очікувана кількість ходів до кута) як оцінка позиції — 🥉.
- Повний перебір/ендшпільні таблиці на малій дошці — 🥇.
- Матч Best of Five з правилом «хто програв, той ходить першим» і кубом подвоєння — 📎.
- Екран розстановки з «випадково» — 🌱.

## Мапа на каталог
- Є: `piece-capture` · `reach-exit` ↔ куб у куті суперника · `legal-move-highlight`, `selection-highlight`, `last-move-highlight` · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-random`, `ai-greedy`, `ai-minimax` · `cell-click`, `drag-drop-piece` · `placement-screen` ↔ розстановка в трикутнику · `async-multiplayer` ↔ Little Golem · `match-setup` · `game-screen`, `main-menu`, `end-screen`, `help-window` · `state-as-data`, `unit-tests`.
- Наявні пропозиції корпусу: `+die-selects-piece` (див. tetris-link: кубик визначає фігуру) · `+friendly-fire-capture` (бити своїх) · `+capture-all-win` · `+random-setup` (онлайн-розстановка) · `+multi-round-match` (Best of Five, див. [kamisado](kamisado.md)).
- **Нема** → пропозиції карток:
  - `+nearest-value-fallback` «Нема фігури з випалим числом — найближча вища чи нижча» · game-logic/opponent · 🌱.
  - `+doubling-cube` «Куб подвоєння ставки в матчі» · game-logic/score · 📎 · слоти {max: 64}.
  - `+ai-expectimax` «AI з вузлами випадковості (кидки)» · game-logic/opponent · 🥇 · слоти {depth, chance_nodes: d6} — дитина `ai-opponent`.

## Пропозиції до словників
- `+effect:roll_dice` — підтверджую (card-hunter): кинути кубик, результат визначає хід.
- `+cond:die_value` — підтверджую (castles-of-burgundy): номер фігури = випадіння.
- `+ui:dice-result` — підтверджую (heroquest, das-magische-labyrinth): показ випадіння.
- `+ui:required-piece-highlight`, `+ui:match-score` — підтверджую (kamisado): яким кубом ходити; рахунок матчу.
- `+card:nearest-value-fallback`, `+card:doubling-cube`, `+card:ai-expectimax` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: EinStein würfelt nicht!](https://en.wikipedia.org/wiki/EinStein_w%C3%BCrfelt_nicht!) — дошка, куби 1–6, трикутник, кидок, найближчий вищий/нижчий, напрямки, «бʼє будь-який куб», перемога; Schwarz score; варіант 6×6 з двома кубиками; раунди з кубом подвоєння; Little Golem, MasterMoves.
- [Wikipedia DE](https://de.wikipedia.org/wiki/EinStein_w%C3%BCrfelt_nicht) — вибір вищий/нижчий і обовʼязковість, без пасу, один камінь без кидка, стратегія «бити свої 3/4, не 1/6», 3 і 4 гравці (Quattro), застосунок iOS з AI Donninger.
- [Ludii: EinStein Würfelt Nicht](https://ludii.games/details.php?keyword=EinStein%20W%C3%BCrfelt%20Nicht) — формалізовані правила, вільна розстановка, 3-Hirn-Verlag, 2004.
- [Althöfer: Ursprung](http://www.althofer.de/ewn-ursprung.html) — літо 2004, Games Convention Leipzig, попередники, видання, випадковий старт і Best of Five онлайн.
- [Little Golem](https://www.littlegolem.net/jsp/games/gamedetail.jsp?gtid=einstein) — гра онлайн поштою.
- YouTube: пошук «einstein würfelt nicht gameplay».

## Непевне
- (?) Трикутник старту — 6 клітин (3+2+1) у куті; джерела кажуть лише «трикутна зона», розмір виведено з 6 кубів.
- (?) EN-Wikipedia: «15 625 різних передобчислюваних ситуацій» — що саме рахується, не пояснено; не переносив у правила.
- (?) Рік: Ludii й EN — 2004 (Games Convention, серпень 2004); DE підкреслює виставку 2005 (Рік Ейнштейна).
- (?) Правила 6×6 з двома кубиками (як рахувати суму, номери 2–12 без 7) — лише перелік номерів, деталей не бачив.
- (?) Computer Olympiad: EN лише посилається на «16th Computer Olympiad» у «See also»; участь EWN у турнірах — не перевірено.
