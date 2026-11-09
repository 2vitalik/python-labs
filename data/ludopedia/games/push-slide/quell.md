---
title: Quell
slug: quell
aka: [Quell Reflect, Quell Memento, Quell Zen]
family: push-slide
also: []
klass: avatar
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: collect
year: 2010
platforms: [iOS, Android, PC, 3DS, PS Vita, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Quell_(video_game)", best: true, note: "серія Fallen Tree Games: крапля ковзає до стіни, всі золоті кулі, шипи; що додали Memento і Zen"}
  - {kind: other, url: "https://www.appspy.com/quell/review/", note: "огляд 2010: усі перли, perfect runs, вихід за край екрана, токени підказок"}
  - {kind: other, url: "https://www.pocketgamer.com/quell/review/", note: "огляд: свайп = зобовʼязання, шипи вбивають, шипи ззаду — опора"}
  - {kind: other, url: "https://images.jayisgames.com/review/quell-memento.php", note: "огляд Memento: лід, телепорти, рухомі шипи, руйнівні стіни, лампи й кристали"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Quell", note: "пошук; Steam-версії серії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Quell+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [inertia-slide, swipe-gestures, wrap-edges, item-pickup, collect-all, touch-death, impassable-cells, teleport-pair, button-toggle, beam-tracing, move-counter, remaining-counter, sequential-levels, level-unlock, level-select, achievements-window, restart-level, reachability-check, level-solver, unsolvable-states, movement-animation, +perfect-move-rating, +hint-tokens, +directional-spikes, +breakable-wall-hits, +color-cycle-goal, +poison-pickup, +bonus-collectible]
proposes: ["+effect:illuminate", "+feature:hint-tokens", "+card:perfect-move-rating", "+card:directional-spikes", "+card:hint-tokens"]
author: opus
date: 2026-11-09
---

# Quell — крапля ковзає до упору й крізь край екрана; збери всі перли за мінімум ходів

## Суть
Гравець свайпом штовхає краплю дощу в одному з 4 напрямків, і вона летить, доки не вдариться в стіну чи перешкоду, — зупинитись посередині не можна. Мета рівня — торкнутися всіх перлів (золотих куль), не напоровшись на шипи й не застрягши. Від Inertia/льодових пазлів Quell відрізняють **вихід за край екрана на протилежний бік** (поле-тор), **рейтинг «ідеально» за мінімальною кількістю ходів** і **підказки-токени**, що їх заробляють проходженням. Сиквели додають нові цілі: лампи, що міняють колір, і кристали, які засвічує світло краплі.

## Поле і час
- Квадратна сітка-кімната на один екран; межі, де нема стіни, — прохідні: крапля виходить за край і зʼявляється з протилежного боку (тор частково, лише де відкрито).
- Шари: підлога + стіни/блоки + обʼєкти (перли, шипи, перемикачі, телепорти); усе поле видно.
- Хід = одне ковзання будь-якої довжини; без вводу світ не змінюється (`static`), часу на рівень нема.
- Серія: Quell (2010), Quell Reflect (2011), Quell Memento (2013), Quell Zen (2016).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Крапля | player | — | свайп → ковзає до упору; збирає перли на льоту |
| Стіна | static | — | зупиняє краплю в клітині перед собою |
| Перл (золота куля) | pickup | — | торкнувся (навіть пролітаючи) → зібрано; усі зібрані → рівень пройдено |
| Шипи | hazard | бік вістря | наліт на вістря → смерть; ззаду поводяться як стіна-опора (?) |
| Блок | object | — | у базовій грі згаданий; поведінка (штовхається ковзанням?) — (?) |
| Ворота (gate) | gate | відкрито/закрито | змінюються перемикачем або після проходу (?) |
| Перемикач | switch | — | крапля торкнулась → перемикає стан воріт/блоків (?) |
| Відкритий край | terrain | — | вихід за межу → поява з протилежного боку (`wrap`) |
| Льодовий блок (Memento) | object | — | перешкода нового типу; точна поведінка — (?) |
| Телепорт (Memento) | static | пара | влетів → вилітаєш з парного в тому ж напрямку (?) |
| Рухомі шипи (Memento) | hazard | — | шипи, які можна зсунути (?) |
| Руйнівна стіна (Memento) | static | кілька ударів | треба вдарити кілька разів; за нею бонусні самоцвіти |
| Лампа (Memento) | switch | колір | удар/дотик змінює колір; ціль — потрібний колір (?) |
| Кристал (Memento) | mark | засвічено / ні | засвічується світлом, що йде від краплі у 4 боки до перешкоди |
| Бонусний самоцвіт (Memento) | pickup | — | необовʼязковий, часто у важкодоступних місцях |
| Плитка-символ (Zen) | switch | символ | парні символи мають збігтися (?) |
| Отруйний перл (Zen) | hazard | — | торкатися не можна (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(swipe_dir)` → ЯКЩО `custom: «крапля стоїть»` → ТО `slide(drop, dir)`, `counter(moves, +1)`.
- КОЛИ `blocked(drop)` → ТО `custom: «зупинка в клітині перед перешкодою — нова точка вибору»`.
- КОЛИ `edge(drop)` → ЯКЩО `not cell(edge, wall)` → ТО `wrap(drop)`, ковзання триває.
- КОЛИ `contact(drop, pearl)` → ТО `pickup`, `counter(pearls_left, -1)`.
- КОЛИ `contact(drop, spikes)` → ЯКЩО `custom: «крапля летить на вістря»` → ТО `lose`, `restart`; інакше `block`.
- КОЛИ `contact(drop, switch)` → ТО `set_state(gates, toggle)` (?).
- КОЛИ `enter(drop, teleport)` → ТО `teleport`, `custom: «ковзання продовжується з парного телепорта»` (?).
- КОЛИ `contact(drop, breakable_wall)` → ТО `hp(wall, -1)`, `block`; КОЛИ `hp_zero(wall)` → ТО `disappear_b`, `reveal(bonus_gems)`.
- КОЛИ `contact(drop, lamp)` → ТО `custom: «наступний колір лампи»` (?).
- КОЛИ `blocked(drop)` → ЯКЩО `line_of_sight(drop, crystal)` → ТО `set_state(crystal, lit)` — світло від краплі в 4 боки до перешкоди (Memento; кандидат `+effect:illuminate`).
- КОЛИ `contact(drop, poison_pearl)` → ТО `lose` (Zen) (?).
- КОЛИ `all_gone(pearl)` (і виконані інші цілі рівня) → ТО `win`, `next_level`.
- КОЛИ `level_end` → ЯКЩО `custom: «ходів ≤ мінімуму рівня»` → ТО `custom: «рівень позначено як perfect»`.
- КОЛИ `input(hint)` → ЯКЩО `has(player, hint_token)` → ТО `take(player, hint_token)`, `custom: «показати один можливий розвʼязок»`.
- КОЛИ `level_end` → ЯКЩО `first_time` → ТО `give(player, hint_token)` (поповнення токенів проходженням) (?).
- Перемога: зібрано всі перли (у Memento — ще й лампи/кристали, за рівнем). · Поразка: шипи; «застряг» — фактично глухий кут → рестарт. · Рахунок: кількість ходів проти мінімуму (perfect), самоцвіти й досягнення.

## Керування і ввід
- Свайп у 4 напрямки (тач); у Memento — також тап/флік по краплі. ПК/консолі — стрілки або стік (?).
- Ввід під час ковзання ігнорується (?); перервати ковзання не можна.
- Кнопки: рестарт рівня, підказка (витрачає токен); undo — (?).

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Грати → `level-select` (розділи-кімнати; Memento — покинутий будинок), досягнення → `achievements-window`, `settings-window` (звук/музика (?)).
- `game-screen`: поле; HUD — `move-counter` і `par-moves` (?), `remaining-counter` перлів (?), `hint-button`, `restart-button`.
- `hints-window`: показ розвʼязку за токен.
- `end-screen`: рівень пройдено / perfect, перехід далі.
- Переходи: main-menu → level-select → game-screen → (усі перли) end-screen → наступний рівень.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: послідовність розділів; у Memento 150+ пазлів і приховані рівні (timekeeper), у Zen — приховані Zen і Black Hole рівні.
- `par-target`: «perfect» лише за мінімальну кількість ходів — головна причина перегравати.
- `hint` за токени, які заробляються проходженням рівнів.
- `achievements` за perfect-проходження й колекційні самоцвіти (`collectibles`).
- `restart-level`; збереження прогресу (`autosave`).

## Варіації й родичі
- Сиквели: Reflect (2011; нові механіки в джерелах не названі), Memento (2013: лід, телепорти, рухомі шипи, перемикачі, руйнівні стіни, лампи, кристали, троянди), Zen (2016: плитки-символи, отруйні перли).
- Родичі в корпусі: [ice-sliding-puzzles](ice-sliding-puzzles.md) (Inertia — та сама «ковзай до упору» + збери все, але 8 напрямків і без тору), [tomb-of-the-mask](tomb-of-the-mask.md) (те саме ковзання в real-time), [pengo](pengo.md) (ковзні блоки), [ricochet-robots](ricochet-robots.md) (ковзання фігур до упору, мінімум ходів), [atomix](atomix.md).
- Осі варіацій:
  - **край поля**: стіна (Inertia) / тор (Quell) / смерть;
  - **ціль**: зібрати все / дійти до виходу / засвітити (кристали, лампи) / кілька цілей разом;
  - **що зупиняє**: лише стіни / ще й обʼєкти (лід, блоки) / шипи-з-боку як опора;
  - **оцінка**: пройдено / пройдено за par (perfect) / зірки.

## Цікавинки для курсу
- Ковзання до упору з тором: цикл, що завершується на стіні, і захист від нескінченного кола, коли в ряду нема жодної стіни — 📎.
- Шипи з напрямком: смерть лише при нальоті на вістря, ззаду — опора — 🌱.
- Perfect-рейтинг: BFS по станах (позиція краплі + множина зібраних перлів) дає мінімум ходів для par — 🥈 (стан = бітова маска перлів).
- Підказка-розвʼязок за токен, токени заробляються проходженням — 📎.
- Кристали Memento: після кожної зупинки трасувати 4 промені від краплі до перешкоди й засвітити кристали — 📎.
- Руйнівна стіна з кількома ударами (HP у статики) — 🌱.

## Мапа на каталог
- Є: `inertia-slide` ↔ ковзання до упору; `swipe-gestures` ↔ ввід; `wrap-edges` ↔ вихід за край; `item-pickup` + `collect-all` ↔ перли; `touch-death` ↔ шипи; `impassable-cells` ↔ стіни; `teleport-pair` ↔ телепорти Memento; `button-toggle` ↔ перемикачі; `beam-tracing` ↔ світло на кристали; `move-counter`, `remaining-counter` ↔ HUD; `sequential-levels`, `level-unlock`, `level-select`, `achievements-window`, `restart-level`; `reachability-check`, `level-solver`, `unsolvable-states` ↔ «застряг» і пошук par.
- **Нема** → пропозиції карток:
  - `+perfect-move-rating` «Позначка perfect за мінімум ходів» · game-logic/score · 📎 · слот {par}.
  - `+hint-tokens` «Підказки за токени, токени за проходження» · game-logic/difficulty · 📎 · слот {start, per_level}.
  - `+directional-spikes` «Шипи, що вбивають лише з боку вістря» · entities/death · 🌱.
  - `+breakable-wall-hits` «Стіна, що руйнується після N ударів» · entities/interact · 🌱 · слот {hits}.
  - `+color-cycle-goal` «Лампа міняє колір від дотику; ціль — колір» · game-logic/win · 📎.
  - `+poison-pickup` «Предмет, якого не можна торкатись серед потрібних» · entities/death · 🌱.
  - `+bonus-collectible` «Необовʼязковий колекційний предмет» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:illuminate` — після зупинки світло від сутності в 4 боки до перешкоди засвічує цілі (кристали Quell Memento); відмінне від `reveal` (туману тут нема).
- `+feature:hint-tokens` — підказки обмежені токенами, що поповнюються проходженням (у словнику є лише `hint`).
- `+card:perfect-move-rating`, `+card:directional-spikes`, `+card:hint-tokens` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Quell](https://en.wikipedia.org/wiki/Quell_(video_game)) — розробник, дати й платформи серії; свайп, «рухається до стіни», торкнутися всіх золотих куль без шипів і застрягання; перемикачі/блоки/ворота; що додали Memento і Zen.
- [AppSpy: огляд Quell](https://www.appspy.com/quell/review/) — усі перли, неможливо зупинитись посередині, perfect runs, прохід з краю на край, токени підказок за проходження.
- [Pocket Gamer: огляд Quell](https://www.pocketgamer.com/quell/review/) — свайп як зобовʼязання, шипи вбивають, підхід до шипів ззаду, досягнення.
- [Jay is Games: Quell Memento](https://images.jayisgames.com/review/quell-memento.php) — тор, лід, телепорти, рухомі шипи, перемикачі, руйнівні стіни з самоцвітами, лампи, кристали від світла краплі, 150+ пазлів, мінімум ходів.
- YouTube / Steam — пошукові URL.

## Непевне
- (?) Поведінка блоків і воріт базової гри: чи блок штовхається краплею, чи ворота однопрохідні або керуються перемикачем — у відкритих джерелах лише назви.
- (?) Шипи ззаду як безпечна опора — виведено з фрази Pocket Gamer «approaching them from behind»; чи шипи взагалі мають бік — не підтверджено.
- (?) Точна механіка телепортів, льоду, рухомих шипів, ламп і троянд Memento; плиток-символів і отруйних перлів Zen.
- (?) Що нового в Quell Reflect.
- (?) Наявність undo, показ par у HUD, кількість стартових токенів підказок і скільки дають за рівень.
- (?) Чи світ справді тор на всіх краях, чи лише в отворах стін (огляди кажуть просто «з одного боку екрана на інший»).
