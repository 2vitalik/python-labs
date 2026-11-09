---
title: Bagh-chal (Баґ-чал, «Тигри й кози»)
slug: bagh-chal
aka: [Bāgh cāl, Baghchal, Dhun kasa, Tigers and Goats, Тигри й кози, Баг-чал]
family: chess-abstract
also: []
klass: figure
axes:
  field: graph
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1900
platforms: [board, web, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bagh-chal", best: true, note: "5×5 точок як алькерк, 4 тигри в кутах, 20 кіз, фаза розставляння, стрибок по одній козі, 5 зʼїдених / тигри заблоковані, заборона повтору"}
  - {kind: play, url: "https://merokalam.com/baghchal/", note: "грати в браузері: 1P проти рушія (4 рівні) / 2P, Undo, Hint, Moves, огляд партії, лічильники 20 і 5"}
  - {kind: play, url: "https://www.baghchal.net/", note: "онлайн: гра з компʼютером, лобі, рейтинг, повтори, чат"}
  - {kind: other, url: "https://ludii.games/details.php?keyword=Baghchal", note: "Ludii: правила, походження (Непал, XX ст.), рулсети Hora/Parlett і Averbakh 1986"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Fox_games", note: "родина ігор полювання: Fox and geese, Halatafl, Fox and hounds, Koti keliya"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Aadu_puli_attam", note: "індійський родич: 3 тигри, 15 кіз"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Bagh+chal+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [piece-move-patterns, piece-capture, cursor-place, legal-move-highlight, selection-highlight, cell-click, hot-seat, turn-enforcement, ai-opponent, ai-minimax, difficulty-levels, undo-step, no-moves-left, remaining-counter, goal-counter, mode-indicator, replay-window, online-multiplayer, lobby-window, leaderboard, match-setup, game-screen, main-menu, end-screen, settings-window, help-window, language-picker, movement-animation, level-solver, +asymmetric-sides, +place-stone, +phase-transition, +hand-supply, +single-jump-capture, +capture-count-win, +immobilize-win, +repetition-ban, +line-graph-board, +side-swap-match]
proposes: ["+cond:phase(x)", "+cond:on_line(a, b)", "+effect:jump_capture", "+ui:phase-indicator", "+window:side-select", "+feature:side-swap-match", "+card:single-jump-capture", "+card:immobilize-win", "+card:repetition-ban", "+card:line-graph-board"]
author: opus
date: 2026-11-09
---

# Bagh-chal — четверо тигрів полюють стрибками, двадцять кіз розставляються й мусять їх замурувати

## Суть
Непальська асиметрична гра полювання на сітці 5×5 точок: в одного гравця 4 тигри, в іншого — до 20 кіз. Кози спершу по одній **ставляться** на поле (тигри тим часом ходять), лише потім рухаються. Тигр бʼє стрибком через сусідню козу, як у шашках, але по одній за хід; тигри виграють, зʼївши 5 кіз, кози — заблокувавши всіх тигрів. Без заборони повтору кози могли б вічно тупцяти — тому повторювати позицію заборонено.

## Поле і час
- 25 точок-перехресть сітки 5×5, як в алькерку; фігури стоять на точках, ходять уздовж намальованих ліній (`field: graph`).
- Ортогональні лінії — між усіма сусідніми точками; діагоналі — лише через частину точок (кути й центр зʼєднані; за алькерк-схемою — через кожну другу точку (?)).
- Старт: 4 тигри в кутах, «дивляться» до центру; кіз на полі нема, усі 20 — у запасі.
- Хід = одна дія: поставити козу / посунути козу / посунути тигра / тигр стрибає. Першими ходять кози.
- Дві фази кіз: **розставляння** (поки в запасі є кози) → **рух**.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тигр | piece | ×4; старт — кути | крок на сусідню вільну точку по лінії **або** стрибок через сусідню козу по прямій на вільну точку за нею; не перестрибує тигрів |
| Коза | piece | ×20; запас → поле | фаза 1: ставиться на вільну точку, не ходить; фаза 2: крок на сусідню вільну точку по лінії; не стрибає, не бʼє |
| Запас кіз | supply | 20 → 0 | звідки кози йдуть на поле по одній за хід |
| Точка з діагоналями | terrain | 8 сусідів | сюди й звідси можна ходити й стрибати по діагоналі |
| Точка без діагоналей | terrain | ≤4 сусіди | лише ортогональні ходи й стрибки |
| Лічильник зʼїдених | zone | 0…5 | 5 — перемога тигрів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(goats)` → ЯКЩО `counter(supply, >, 0)` → ТО `custom: «хід кіз — лише поставити козу»`.
- КОЛИ `input(place(goat, point))` → ЯКЩО `free(point)` → ТО `place(goat, point)`, `counter(supply, -1)`.
- КОЛИ `input(move(goat, to))` → ЯКЩО `counter(supply, >, 0)` → ТО `block` (кози не ходять, доки всі не поставлені).
- КОЛИ `counter(supply, ==, 0)` → ТО `custom: «починається фаза руху кіз»`.
- КОЛИ `input(move(goat, to))` → ЯКЩО `counter(supply, ==, 0)` and `custom: «to — сусідня точка по намальованій лінії»` and `free(to)` → ТО `move(goat, to)`.
- КОЛИ `input(move(tiger, to))` → ЯКЩО `custom: «to — сусідня точка по лінії»` and `free(to)` → ТО `move(tiger, to)`.
- КОЛИ `input(jump(tiger, over))` → ЯКЩО `in_range(tiger, goat, 1)` and `custom: «тигр, коза й точка за нею — на одній намальованій прямій»` and `free(landing)` → ТО `move(tiger, landing)`, `disappear(goat)`, `counter(captured, +1)`.
- Стрибок — **один** за хід (ланцюгів нема), **необовʼязковий**, можливий і під час розставляння; КОЛИ `input(jump(tiger, over tiger))` → ТО `block`.
- КОЛИ `counter(captured, >=, 5)` → ТО `win(tigers)`.
- КОЛИ `no_moves(tigers)` (жоден тигр не може ні ступити, ні стрибнути) → ТО `win(goats)`.
- КОЛИ `input(move)` → ЯКЩО `counter(supply, ==, 0)` and `custom: «після ходу позиція повторить уже бувалу в цій партії»` → ТО `block` — заборона повтору, щоб кози не тягнули час.
- Деякі реалізації замість заборони — нічия триразовим повтором і нічия, коли козам нема ходу (?).
- Перемога: тигри — 5 зʼїдених кіз; кози — усі тигри заблоковані одночасно. · Поразка — дзеркально. · Рахунок: лише лічильник зʼїдених.

## Керування і ввід
- Настільна: кози з запасу кладуть на точку, фігури посувають уздовж ліній.
- Цифрова (merokalam): клік по вільній точці — поставити козу; клік фігури → підсвітка легальних ходів (перемикається в налаштуваннях) → клік цілі; стрибок — клік точки за козою.
- Кнопки під час гри: Undo, Hint (той самий рушій), Moves (список ходів), Settings, New Game.

## Вікна, меню, HUD
- (цифрова версія — merokalam.com/baghchal, baghchal.net)
- `match-setup` / `mode-select`: 1 гравець (проти рушія) / 2 гравці на одному пристрої; `side-select` — кози чи тигри; `difficulty-select` — Easy / Medium / Hard / Expert; імена; «Продовжити попередню» або «Нова».
- `game-screen`: дошка-граф з лініями; `remaining-counter` «Goats placed x/20»; `progress-bar` «Captured x/5»; `phase-indicator` «Placement / Movement»; `turn-indicator` («Your turn» / «engine is thinking…»); `cell-coordinates` (опційно); `legal-move-highlight`.
- `end-screen`: Play Again · Switch Sides · Review Game.
- `replay-window` (Review): Prev / Next / Return to game.
- `settings-window`: мова (англ. / непальська), звук, анімація (повна / зменшена), показ легальних ходів, координати, складність.
- baghchal.net: `lobby-window` (очікують / грають / завершені), `leaderboard`, повтори партій, чат (з акаунтом).
- Переходи: main-menu → match-setup → game-screen → end-screen → replay-window / нова партія.

## Фічі поза полем
- `ai-opponent-levels` — рушій з ітеративним поглибленням alpha-beta у браузері; складність міняє глибину й оцінку ризику, не правила.
- `hint` тим самим рушієм · `undo` · `replay` · `autosave`-подібне «Continue Previous Game».
- `side-swap-match` — «Switch Sides» після партії (асиметрія).
- `localization` (EN / NE), `animation-toggle`, `sound-toggle`.
- Онлайн: `online-multiplayer`, `leaderboard-online`, `chat`, нотація OBX (?).
- Розвʼязана: Лім Ю Цзінь і Ю. Нівергельт, «Tigers and Goats is a draw» (Games of No Chance 3, 2009) — при ідеальній грі нічия.

## Варіації й родичі
- Рулсети Ludii: Hora/Parlett і Averbakh (1986, «5 кіз — перемога тигрів»); на півдні Індії — ті самі правила на іншій дошці.
- **Aadu puli attam** (Індія): 3 тигри, до 15 кіз, інша дошка.
- **Fox games**: Fox and geese (1 лис проти 13 гусей на хрестоподібній дошці, взяття необовʼязкове), Halatafl (взяття обовʼязкове, вівці мають зайти в загін), Fox and hounds (8×8, без взяття, розвʼязана на користь гончаків), Koti keliya (без взяття).
- Сусіди корпусу: [hnefatafl.md](hnefatafl.md) (асиметричні сторони, мета «замурувати»), [checkers.md](checkers.md) (взяття стрибком, але з ланцюгами й обовʼязкове), [nine-mens-morris.md](nine-mens-morris.md) (фаза розставляння → фаза руху), [konane.md](konane.md), [fanorona.md](fanorona.md) (алькерк-дошка).
- **Осі варіацій**:
  - співвідношення сил: 1 лис : 13 гусей / 3 : 15 / 4 : 20;
  - взяття: обовʼязкове / необовʼязкове; одне / ланцюг;
  - мета слабшої сторони: замурувати / дійти до загону;
  - розставляння: з запасу по одній (Bagh-chal) / усі на полі зі старту (Fox and geese);
  - проти тупцяння: заборона повтору / нічия повтором.

## Цікавинки для курсу
- Дошка-граф з частковими діагоналями (суміжність зі списку ребер, а не з координат) — 📎.
- Дві фази кіз (запас → рух) і хід, зміст якого залежить від фази — 🌱.
- Стрибок тигра: перевірка «сусідня коза + вільна точка на тій самій прямій» — 📎.
- Перемога кіз = жоден тигр не має ходу (генерація ходів усіх тигрів) — 🌱.
- Заборона повтору будь-якої бувалої позиції: множина хешів позицій партії — 📎.
- Рушій alpha-beta з рівнями складності й підказкою тим самим рушієм — 🥈; повна ретроградна розвʼязка (нічия) — 👑.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ крок/стрибок тигра, крок кози · `piece-capture` ↔ стрибок · `cursor-place` ↔ поставити козу · `legal-move-highlight` + `selection-highlight` + `cell-click` · `hot-seat` + `turn-enforcement` · `ai-opponent` + `ai-minimax` ↔ alpha-beta · `difficulty-levels` ↔ 4 рівні · `undo-step` · `no-moves-left` ↔ тигри заблоковані · `remaining-counter` / `goal-counter` ↔ 20 і 5 · `mode-indicator` ↔ фаза · `replay-window` ↔ Review · `online-multiplayer` + `lobby-window` + `leaderboard` (baghchal.net) · `match-setup` · `game-screen` / `main-menu` / `end-screen` / `settings-window` / `help-window` · `language-picker` ↔ EN/NE · `movement-animation` ↔ анімація (повна / зменшена) · `level-solver` ↔ розвʼязана гра.
- **Нема** → пропозиції карток:
  - `+asymmetric-sides` (див. hnefatafl) — тут ще й різні фази.
  - `+place-stone`, `+phase-transition`, `+hand-supply` (див. nine-mens-morris).
  - `+single-jump-capture` «Взяття одним стрибком, без ланцюга, необовʼязкове» · entities/combat · 📎 · слоти {mandatory, chain}.
  - `+capture-count-win` (див. abalone) — тут поріг 5.
  - `+immobilize-win` «Перемога, коли всі фігури суперника без ходу» · game-logic/win · 🌱.
  - `+repetition-ban` «Заборона повторити бувалу позицію» · game-logic/constraints · 📎 (родич `repetition-draw`).
  - `+line-graph-board` «Дошка-граф з намальованими лініями (алькерк)» · field · 📎.
  - `+side-swap-match` (див. hnefatafl) — «Switch Sides».

## Пропозиції до словників
- `+cond:phase(x)` — поточна фаза гри (розставляння / рух; див. nine-mens-morris).
- `+cond:on_line(a, b)` — A і B зʼєднані намальованою лінією (суміжність графа, а не координат).
- `+effect:jump_capture` — стрибок через сусіда з його зняттям (див. checkers, konane).
- `+ui:phase-indicator` (див. nine-mens-morris) — «Placement / Movement».
- `+window:side-select` (див. hnefatafl) — вибір сторони в асиметричній грі.
- `+feature:side-swap-match` (див. hnefatafl) — «Switch Sides» після партії.
- `+card:single-jump-capture`, `+card:immobilize-win`, `+card:repetition-ban`, `+card:line-graph-board`.

## Джерела
- ⭐ [Wikipedia: Bagh-chal](https://en.wikipedia.org/wiki/Bagh-chal) — дошка як алькерк, старт у кутах, кози першими й лише ставляться, «only one goat at a time», тигри не перестрибують тигрів, 5 кіз / блок, заборона повтору після розставляння, назви, Південна Індія.
- [Merokalam: Bagh Chal](https://merokalam.com/baghchal/) — цифрова версія: режими, рівні, рушій alpha-beta, кнопки, лічильники, екран перемоги й огляду, налаштування; правила (діагоналі лише з частини точок, взяття необовʼязкове).
- [baghchal.net](https://www.baghchal.net/) — онлайн-гра, лобі, рейтинг, повтори, чат; «діагоналі зʼєднують кути й центр».
- [Ludii: Baghchal](https://ludii.games/details.php?keyword=Baghchal) — правила, Непал XX ст., рулсети (Hora/Parlett, Averbakh 1986).
- [Wikipedia: Fox games](https://en.wikipedia.org/wiki/Fox_games) — родина ігор полювання.
- [Wikipedia: Aadu puli attam](https://en.wikipedia.org/wiki/Aadu_puli_attam) — 3 тигри, 15 кіз.
- Lim Yew Jin, J. Nievergelt «Tigers and Goats is a draw» (Games of No Chance 3, MSRI) — бачив у пошуку; PDF не відкрився.
- YouTube: [пошук «Bagh chal gameplay»](https://www.youtube.com/results?search_query=Bagh+chal+gameplay).

## Непевне
- (?) Точна схема діагоналей: «як алькерк» і «кути й центр» — за алькерк-схемою діагоналі йдуть через кожну другу точку, але жодне відкрите джерело не описало це текстом.
- (?) Чи бʼють тигри під час розставляння: Wikipedia і merokalam — так; baghchal.net — «тигри лише переставляються».
- (?) Що буде, коли козам у фазі руху нема ходу; нічия повтором — у частині реалізацій (сніпет пошуку), не перевірено.
- (?) `year: 1900` умовно: Ludii — «зафіксовано в XX ст.», сама гра традиційна, старша.
- (?) Нотація OBX на baghchal.net — лише згадка.
