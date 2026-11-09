---
title: elephant-in-a-bottle
slug: elephant-in-a-bottle
aka: [Elephant-in-a-Bottle, Elephant in a Bottle]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [web, mobile]
links:
  - {kind: itch, url: "https://pancelor.itch.io/elephant-in-a-bottle", best: true, note: "грати в браузері; керування, 12 рівнів, вибір рівня в меню, devlog-и"}
  - {kind: other, url: "https://www.puzzlescript.net/editor.html?hack=77efccad03902fa962a10cadae1334ce", note: "сирці PuzzleScript (посилання зі сторінки гри)"}
  - {kind: other, url: "https://pancelor.itch.io/elephant-in-a-bottle/devlog/270056/v12-de-cheesing", note: "devlog v1.2 de-cheesing (03.07.2021)"}
  - {kind: other, url: "https://pancelor.itch.io/elephant-in-a-bottle/devlog/390605/v14-tweaks-new-levels", note: "devlog v1.4: правки й нові рівні (08.06.2022)"}
  - {kind: other, url: "https://itch.io/jam/thinky-puzzle-game-jam/rate/1110199", note: "сторінка на Thinky Puzzle Game Jam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=elephant-in-a-bottle+pancelor+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, keyboard-controls, swipe-gestures, push-object, stick-together, impassable-cells, all-on-targets, undo-unlimited, restart-level, level-select, sequential-levels, sound-effects, tutorial-window, +axis-locked-movers, +rigid-stick-pusher, +assemble-shape-in-template]
proposes: ["+cond:axis(a, h|v)", "+effect:move_group", "+axis:control=axis-split", "+card:axis-locked-movers", "+card:rigid-stick-pusher", "+card:assemble-shape-in-template"]
author: opus
date: 2026-11-09
---

# elephant-in-a-bottle — збери липкого слона в «пляшці», штовхаючи його палицями, які ходять лише вздовж своєї осі

## Суть
PuzzleScript-головоломка без аватара: гравець керує набором **палиць-штовхачів** (prodders). Стрілка вліво/вправо рушає одразу всі горизонтальні палиці, вгору/вниз — усі вертикальні. Палиці штовхають чотири шматки слона, а шматки **липкі**: щойно два торкнулися, далі рухаються разом. Мета — скласти слона 2×2 у правильному порядку чвертей точно на місці в «пляшці» — вузькому стінному контурі з шийкою. Ядро — непрямий контроль через осі й незворотне злипання.

## Поле і час
- Квадратна сітка, рівень на один екран; стіни з фаскою (beveled) і рамка поля.
- Шари: фон → шаблон-ціль (малюнок пляшки 4×3, генерується від позначеної клітини) → стіни → палиці → шматки слона → рамка-виділення навколо слона.
- Хід = натискання; усі палиці потрібної осі рухаються одночасно, заблоковані стоять, решта йдуть.
- Повна інформація, без випадковості.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Горизонтальна палиця | player | наконечник + сегменти держака в ряд | рухається лише вліво/вправо цілою; штовхає все, що попереду |
| Вертикальна палиця | player | наконечник + сегменти в стовпчик | рухається лише вгору/вниз цілою |
| Шматок слона (4 види: чверті 2×2) | object | вид 0–3 | штовхається; злипається з будь-яким сусіднім шматком і далі рухається групою |
| Стіна | static | — | непрохідна; зупиняє палицю чи групу слона, що в неї впирається |
| Рамка поля | static | — | як стіна |
| Пляшка-ціль | zone | шаблон 4×3 | чотири клітини, куди мають стати чверті слона |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `custom: «палиця горизонтальна»` → ТО `move(stick, dir)` усією палицею; вертикальні не рухаються.
- КОЛИ `input(up|down)` → ЯКЩО `custom: «палиця вертикальна»` → ТО `move(stick, dir)`; горизонтальні не рухаються.
- КОЛИ `input(dir)` → ЯКЩО `custom: «попереду рухомого (палиці чи шматка) у напрямку руху — стіна або рамка»` → ТО `block` для нього; блокування поширюється на всю групу слона й усі сегменти тієї палиці.
- КОЛИ `contact(mover, mover)` → ЯКЩО `not state(target, blocked)` → ТО `push` — палиця штовхає шматок слона, шматок — іншу палицю чи шматок, ланцюгом; поштовх може зрушити й палицю «чужої» осі.
- КОЛИ `custom: «шматок слона рушив»` → ТО `custom: «рушають усі шматки, що з ним стикаються (flood)»` — злипання без окремої дії, назавжди.
- КОЛИ `adjacent(elephant_piece, elephant_piece)` → ТО `attach` (неявно — шматки злиплися).
- КОЛИ `all_on(elephant_piece, matching_target)` → ТО `win`, `message(text)`, `next_level`.
- КОЛИ `level_start` → ТО `custom: «намалювати пляшку 4×3 від клітини-мітки, виставити checkpoint»`.
- КОЛИ `input(z)` → ТО `custom: «undo»`; `input(r)` → `restart`; `input(esc)` → `window(level-select)`.
- Перемога: чверть 0 на клітині 1, чверть 1 — на 2, чверть 2 — на 5, чверть 3 — на 6 шаблону (верхня середина пляшки). · Поразка: нема; злиплі невдало шматки — глухий кут, лише undo/restart. · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — рух усіх палиць відповідної осі; Z — undo; R — рестарт; Esc — до вибору рівня.
- Мобільні: свайп = напрямок.
- Аватара нема: одне натискання рухає кілька сутностей водночас.

## Вікна, меню, HUD
- `main-menu` з вибором рівня (за сторінкою itch: «Jump around if you like» через level selector).
- `level-select` — стрибок на будь-який із 12 рівнів.
- `game-screen`: поле без HUD; рамка-виділення обводить шматки слона.
- `custom-window` — текстові перебивки-оповідь між рівнями («I am constructing an elephant in a bottle», «the elephant is very sticky» …).
- `tutorial-window` — інтерактивне навчання (тег сторінки itch).
- Переходи: меню → game-screen → (слон у пляшці) текст → наступний рівень; Esc → level-select.

## Фічі поза полем
- `undo` ∞, `restart-level`, вибір рівня (додано в пізнішій версії: у сирцях v1.2 опція ще закоментована).
- `colorblind-palette`, `high-contrast`, `tutorial` — заявлено тегами доступності itch.
- `touch-controls` — свайпи.
- v1.2 «de-cheesing» — закриття обхідних розвʼязків; v1.4 — правки й нові рівні.

## Варіації й родичі
- Сімʼя: [sokobond](sokobond.md) і [jelly-no-puzzle](jelly-no-puzzle.md) — злипання при дотику; [puddle-knights](puddle-knights.md), [mirror-isles](mirror-isles.md) — непрямий контроль кількох сутностей; [increpare-micro-puzzles](increpare-micro-puzzles.md) — PuzzleScript-мініатюри однієї ідеї; [bean-and-nothingness](bean-and-nothingness.md) — того ж кола тестувальників (incnone).
- Поза thinky: «корабель у пляшці» як образ — складання через вузьку шийку.
- **Осі варіацій**: чим керуєш — одним аватаром / усіма сутностями однієї осі (тут) / усіма одразу (2048-подібний swipe-all); злипання — нема / при дотику назавжди (тут, Sokobond) / за кольором (Jelly); ціль — будь-де / точне положення й орієнтація частин у шаблоні.

## Цікавинки для курсу
- Ввід, що вибирає підмножину акторів за віссю (горизонтальні / вертикальні палиці), — 🌱.
- Тверда палиця з кількох сегментів, яка рухається й блокується цілою, — 📎.
- Поширення блокування: упор будь-якої частини зупиняє групу, решта акторів ходить — 🥉 (порядок розвʼязання поштовхів).
- Липкі шматки: flood-fill групи перед кожним поштовхом — 📎.
- Перемога «кожна чверть на своїй клітині шаблону» (порядок частин важливий) — 🌱.
- Розвʼязувач BFS з незворотним злипанням (рання відсічка тупиків) — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` + `swipe-gestures` ↔ ввід; `push-object` ↔ палиці штовхають; `stick-together` ↔ липкий слон; `impassable-cells` ↔ стіни; `all-on-targets` ↔ чверті на шаблоні; `undo-unlimited` + `restart-level`; `level-select` + `sequential-levels`; `sound-effects` ↔ звуки поштовху й упору; `tutorial-window`.
- **Нема** → пропозиції карток:
  - `+axis-locked-movers` «Ввід рухає всіх акторів своєї осі одночасно» · entities/move · 📎 · слот {axes: h|v}.
  - `+rigid-stick-pusher` «Багатосегментна тверда палиця-штовхач» · entities/legality · 📎.
  - `+assemble-shape-in-template` «Скласти фігуру з частин у точному положенні шаблону» · game-logic/win · 🌱.

## Пропозиції до словників
- `+cond:axis(a, h|v)` — сутність належить до горизонтальної/вертикальної осі (вибір акторів вводом).
- `+effect:move_group` — рух звʼязної групи цілком (вже пропонувалося іншими іграми).
- `+axis:control=axis-split` — новий режим осі `control`: напрям вводу вибирає підмножину акторів.
- Карткові — див. «Мапа на каталог».

## Джерела
- ⭐ [itch.io: elephant-in-a-bottle](https://pancelor.itch.io/elephant-in-a-bottle) — «I am building an elephant in a bottle», 12 рівнів, вибір рівня, керування (WASD/стрілки, Z, R, Esc, свайп), теги доступності, коментарі про «elephant prodders».
- [Сирці PuzzleScript](https://www.puzzlescript.net/editor.html?hack=77efccad03902fa962a10cadae1334ce) — обʼєкти (el0–el3, poke*0/poke*1, targ0–targ11), правила осей, поширення nomove, злипання flood, WINCONDITIONS, тексти-перебивки; gist створено 02.07.2021.
- [Devlog v1.2](https://pancelor.itch.io/elephant-in-a-bottle/devlog/270056/v12-de-cheesing) і [devlog v1.4](https://pancelor.itch.io/elephant-in-a-bottle/devlog/390605/v14-tweaks-new-levels) — історія версій.
- [Thinky Puzzle Game Jam](https://itch.io/jam/thinky-puzzle-game-jam/rate/1110199) — джемова сторінка.

## Непевне
- (?) Сирці, які я читав, — gist від 02.07.2021 (≈v1.2); актуальна v1.4 могла змінити рівні та меню; механіка, найімовірніше, та сама.
- (?) У сирцях є рівні «level 3/4/5, hell version» — чи вони входять у 12 рівнів v1.4, не перевірено.
- (?) Чи може поштовх зрушити палицю «чужої» осі — так за правилом `[> mover | stationary mover]`, у грі не перевірено.
- (?) Наконечник і держак палиці мають різні спрайти (l/r/u/d); чи наконечник щось робить, крім вигляду, — з коду не видно, імовірно ні.
