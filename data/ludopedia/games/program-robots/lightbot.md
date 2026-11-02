---
title: Lightbot (Light-Bot)
slug: lightbot
family: program-robots
also: [thinky]
klass: avatar
axes:
  field: layers
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2008
platforms: [web (Flash), iOS, Android, PC]
links:
  - {kind: play, url: "https://armorgames.com/play/2205/light-bot", best: true, note: "оригінальна Flash-версія 2008 (CoolioNiato), drag команд у слоти"}
  - {kind: official, url: "https://lightbot.com/", note: "сучасна версія: sequencing, procedures, overloading, recursive loops, conditionals"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lightbot", note: "коротка стаття: розробник, платформи"}
  - {kind: official, url: "https://techcrunch.com/2013/06/26/light-bot-teaches-computer-science-with-a-cute-little-robot-and-some-symbol-based-programming/", note: "огляд TechCrunch 2013"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=lightbot+gameplay+walkthrough", note: "пошук; проходження"}
stage: v1
coverage: 75
mechanics: [impassable-cells, level-select, level-unlock, sequential-levels, game-screen, main-menu, +command-program, +command-slots-limit, +user-procedures, +recursion-loop, +conditional-color, +height-levels, +toggle-light-goal, +step-execution, +code-editor-window]
proposes: ["+trigger:exec(cmd)", "+trigger:program_end", "+effect:toggle(cell)", "+cond:height_diff(a, cell, op, n)", "+cond:color(a, c)", "+window:code-editor", "+ui:program-slots", "+ui:command-palette", "+ui:instruction-highlight", "+feature:slot-limit", "+axis:control"]
author: opus
date: 2026-11-02
---

# Lightbot — склади з іконок програму, щоб робот запалив усі сині плитки

## Суть
Робот стоїть на ізометричній сітці плиток різної висоти; частина плиток сині — їх треба «запалити». Гравець перетягує іконки-команди (крок, поворот, стрибок, світло, виклик процедури) у **обмежену кількість слотів** головної програми й процедур P1/P2, потім натискає Run. Ліміт слотів змушує виносити повтори в процедури, а далі — робити процедуру, що викликає сама себе (рекурсія як цикл). Пізні розділи додають умовне виконання через колір робота.

## Поле і час
- Квадратна сітка в ізометричній проєкції; кожна клітина — стовпчик **висоти** 0…N (звідси `field: layers`). Порожні клітини — «безодня»: туди не можна ступити.
- Плитки двох видів за метою: звичайні й сині (лампи), лампа має стан off/on.
- Час `programmed`: програма виконується покроково з анімацією, одна команда — один тік. Перемога перевіряється після кожної дії «світло» (?) або в кінці програми.
- Камера фіксована (у мобільній версії — можна повертати вид (?)); поле невелике (до ~8×8), видно цілком.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Lightbot | player | позиція, висота, напрям, колір (у розділі «Conditionals») | виконує команди зі слотів по черзі |
| Плитка | terrain | висота h | на неї ходять; перехід між сусідніми залежить від різниці висот |
| Порожня клітина | static | — | непрохідна (робот не ступає за край) |
| Синя плитка (лампа) | switch | стан off/on | команда «світло» на ній перемикає стан; мета — усі on |
| Плитка-перефарбовувач (?) | terrain | колір | змінює колір робота, коли він на ній (?) |
| Головна програма (main) | — (програма) | N слотів (≈12) | точка входу |
| Процедури P1, P2 | — (програма) | по ≈8 слотів | викликаються іконкою з будь-якої програми, у т. ч. самої себе |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(walk)` → ЯКЩО `free(front)` і `height_diff(bot, front, ==, 0)` → ТО `move(bot, facing)`; інакше `block` (робот «тупцює», програма йде далі).
- КОЛИ `exec(jump)` → ЯКЩО `height_diff(bot, front, ==, +1)` або `height_diff(bot, front, <, 0)` → ТО `move(bot, facing)` (на 1 вгору або на будь-скільки вниз); інакше `block`.
- КОЛИ `exec(turn_left|turn_right)` → ТО `face(bot, left|right)`.
- КОЛИ `exec(light)` → ЯКЩО `cell(here, blue)` → ТО `toggle(here)` (off ↔ on; повторне світло гасить); інакше нічого.
- КОЛИ `exec(P1|P2)` → ТО `custom: «покласти адресу повернення, виконати процедуру, повернутись»`; процедура може викликати себе й іншу — рекурсія без бази стає нескінченним циклом.
- КОЛИ `exec(cmd)` → ЯКЩО команда пофарбована в колір c → ТО виконати лише при `color(bot, c)`; інакше пропустити (розділ «Conditionals») (?).
- КОЛИ `custom: «усі сині плитки on»` → ТО `win` (одразу, навіть посеред нескінченної рекурсії) (?), `next_level`.
- КОЛИ `program_end` → ЯКЩО є лампи off → ТО `custom: «рівень не пройдено, програма лишається в слотах»` — гравець редагує і запускає знову.
- Обмеження: команду можна покласти лише у вільний слот; кількість слотів main/P1/P2 фіксована на рівень — це головне «обмеження ресурсу» гри.
- Перемога: усі лампи горять. Поразки як такої нема — лише невдала спроба. Рахунок: нема; деякі версії рахують кількість використаних команд (?).

## Керування і ввід
- Drag & drop іконок з палітри у слоти main/P1/P2 (Flash: «Mouse to drag light-Bot controls into the slots»); клік по слоту — видалити команду; вибір активної програми — клік по її рамці.
- Палітра: ↑ walk · ↰ turn left · ↱ turn right · ⤴ jump · 💡 light · P1 · P2 (+ у пізніх розділах — перемикачі кольору команди) (?).
- Кнопки: Run (▶), Stop/Reset, швидкість (?), Clear (очистити слоти).
- Жодного прямого керування: аватар рухається лише через програму.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Play, (у сучасній версії) вибір розділу.
- `level-select` — розділи Basics · Procedures · Overloading · Loops (recursion) · Conditionals, у кожному сітка рівнів з позначкою «пройдено».
- `game-screen`: ізометричне поле зліва; справа `command-palette`, блоки `program-slots` Main/P1/P2; `instruction-highlight` під час виконання; кнопки Run/Reset/Clear; назва рівня й номер.
- `tutorial-window`/оверлеї-підказки на перших рівнях кожного розділу: що робить нова іконка.
- `end-screen` — «Level complete», перехід до наступного.
- `settings-window` (мобільна версія): звук, музика, мова (?).
- Переходи: main-menu → level-select → game-screen → (усі лампи) end-screen → наступний рівень; Back → level-select.

## Фічі поза полем
- `levels-sequential` + `level-unlock` всередині розділу; розділи як уроки (одна нова концепція на розділ).
- `onboarding-hints` — підказки на початку розділу.
- `slot-limit` — обмеження розміру програми як головний «твіст» складності.
- Code Hour — коротка демо-версія для Hour of Code (Basics, Procedures, Loops) (?).
- Нема редактора рівнів (у Flash-версії 2.0 (?)), збереження — прогрес по рівнях.

## Варіації й родичі
- Light-Bot (2008, Flash, Armor Games) → Light-Bot 2.0 (2010, Kongregate: рекурсія, кольорові умови) (?) → Lightbot (2013, iOS/Android/PC) → Lightbot Jr (для 4–8 років, простіші рівні) → Lightbot: Code Hour. Наступник автора — SpriteBox Coding (від іконок до текстової мови).
- Родичі: Robozzle (умови за кольором клітини, а не робота), Karel (текстова мова), Cargo-Bot (кран і ящики, стек), Human Resource Machine.
- Осі варіацій: **місце умови** (колір робота / колір клітини / сенсор), **цикл** (лише рекурсія / окрема іконка repeat), **ліміт** (слоти / кількість кроків / без ліміту), **рельєф** (плаский / висоти зі стрибком).

## Цікавинки для курсу
- Слоти main/P1/P2 зі стеком викликів і рекурсією як єдиним циклом — 🥈 (стек повернень + захист від нескінченності).
- Стрибок з правилом висот «+1 вгору, будь-скільки вниз» — 📎.
- Лампа-перемикач (toggle, а не «увімкнути») — 🌱, але пастка для гравця: подвійне світло гасить.
- Ліміт слотів як обмеження ресурсу, що змушує абстрагувати — 📎.
- Умовні команди за кольором робота — 🥉.
- Ізометричний рендер стовпчиків висоти з порядком малювання — 🥈.

## Мапа на каталог
- Є: `impassable-cells` (порожні клітини, різниця висот) · `level-select` · `level-unlock` · `sequential-levels` · `game-screen` · `main-menu`.
- **Нема** → пропозиції карток:
  - `+command-program` «Програма команд для аватара» · entities/move · 🥉 (спільна з Karel).
  - `+command-slots-limit` «Обмежена кількість слотів програми» · game-logic/constraints · 📎.
  - `+user-procedures` «Процедури P1/P2» · game-logic · 🥈.
  - `+recursion-loop` «Цикл через самовиклик процедури» · game-logic · 🥈.
  - `+conditional-color` «Команда виконується лише за кольору актора» · game-logic · 🥉.
  - `+height-levels` «Клітини з висотою, стрибок вгору/вниз» · entities/legality · 🥉 · слоти {up: 1, down: any}.
  - `+toggle-light-goal` «Плитки-лампи, усі on = перемога» · game-logic/win · 🌱.
  - `+step-execution` · interface/input · 🥉; `+code-editor-window` (тут — палітра й слоти) · interface/menus · 🥉.

## Пропозиції до словників
- `+trigger:exec(cmd)` / `+trigger:program_end` — як у Karel.
- `+effect:toggle(cell)` — перемкнути стан клітини (лампа, перемикач) без явного `set_state`.
- `+cond:height_diff(a, cell, op, n)` — різниця висот між сутністю й клітиною (стрибок, падіння).
- `+cond:color(a, c)` — поточний колір сутності (умовне виконання).
- `+window:code-editor` — тут у формі слотів.
- `+ui:program-slots` — ряди слотів фіксованої довжини; `+ui:command-palette` — палітра іконок-команд; `+ui:instruction-highlight`.
- `+feature:slot-limit` — обмеження довжини програми.
- `+axis:control` — `programmed`.

## Джерела
- ⭐ [Light-Bot на Armor Games](https://armorgames.com/play/2205/light-bot) — оригінал 2008, грається за 10 хвилин.
- [lightbot.com](https://lightbot.com/) — сучасна версія: перелік концепцій (sequencing, overloading, procedures, recursive loops, conditionals), платформи.
- [Wikipedia: Lightbot](https://en.wikipedia.org/wiki/Lightbot) — Danny Yaroslavski, 2008, walk/turn/jump/light, процедури й цикли.
- [TechCrunch 2013](https://techcrunch.com/2013/06/26/light-bot-teaches-computer-science-with-a-cute-little-robot-and-some-symbol-based-programming/) — огляд перевидання.
- YouTube: пошук «lightbot gameplay walkthrough».

## Непевне
- (?) Пошук був недоступний (вичерпаний ліміт): іконки, кількість слотів (≈12/8/8), правило стрибка й механіка кольору — з памʼяті, не звірено з грою.
- (?) Що означає розділ «Overloading» (на сайті є, механіку не перевірив).
- (?) Чи перемога настає миттєво посеред програми, чи лише в кінці; чи світло повторно гасить лампу в усіх версіях.
- (?) Light-Bot 2.0 на Kongregate і його фічі — з памʼяті; сторінку не знайдено без пошуку.
- (?) Рахунок/медалі за кількість команд — не підтверджено.
