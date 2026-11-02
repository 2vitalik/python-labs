---
title: RoboZZle
slug: robozzle
family: program-robots
also: [thinky]
klass: avatar
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: collect
year: 2009
platforms: [web (Silverlight, потім JS), iOS, Windows Phone 7, Android, Kindle Fire]
links:
  - {kind: play, url: "https://www.robozzle.com/beta/", best: true, note: "грати в браузері: Tutorial, F1–F5, Go!/Step, редактор пазлів"}
  - {kind: official, url: "https://www.robozzle.com/", note: "сайт гри, платформи, контриб'ютори"}
  - {kind: other, url: "https://www.robozzle.com/js/index.aspx", note: "банк пазлів: складність, лайки/дизлайки, автор, сортування"}
  - {kind: other, url: "https://igoro.com/archive/my-hobby-project-a-social-puzzle-game-developed-in-silverlight/", note: "автор про гру (2009): зірки, пазли гравців, голосування складності"}
  - {kind: other, url: "https://igoro.com/archive/the-first-month-of-my-online-game/", note: "перший місяць: степ-дебагер, скорборд найкоротших розвʼязків, приховування непопулярних"}
  - {kind: other, url: "https://github.com/lostmsu/RoboZZle-Droid", note: "відкритий код Android-порту (MIT)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=robozzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [collect-all, environment-death, level-bank, level-rating, in-game-editor, editor-playtest, score-records, leaderboard, game-screen, end-screen, +command-program, +user-procedures, +recursion-loop, +conditional-color, +command-slots-limit, +paint-cell-command, +call-stack, +step-execution, +code-editor-window, +solvable-proof-on-submit, +difficulty-vote, +shortest-solution-board]
proposes: ["+trigger:exec(cmd)", "+trigger:program_end", "+cond:color(a, c)", "+effect:call(fn)", "+effect:paint", "+effect:crash", "+window:code-editor", "+window:puzzle-submit", "+ui:program-slots", "+ui:command-palette", "+ui:instruction-highlight", "+ui:call-stack-view", "+feature:difficulty-vote", "+feature:solution-required", "+axis:control"]
author: opus
date: 2026-11-02
---

# RoboZZle — до пʼяти коротких функцій і колір під роботом: рекурсія замість циклів

## Суть
Робот-стрілка стоїть на полі з кольорових плиток (червоні, зелені, сині) і має зібрати всі зірки. Гравець не керує ним напряму: заповнює до пʼяти функцій F1–F5 з дуже малою кількістю слотів командами «вперед / ліворуч / праворуч / виклик Fn / зафарбувати плитку». Кожна команда може бути **умовною за кольором** — виконується лише коли робот стоїть на плитці цього кольору. Циклів нема: повтор — це рекурсивний виклик функції, тому гра — практикум із рекурсії й стеку викликів; тисячі пазлів створили самі гравці.

## Поле і час
- Квадратна сітка (у вебверсії 16×12 (?)); клітина — або плитка одного з трьох кольорів, або порожнеча. Зірка лежить на плитці.
- Робот займає клітину й має напрямок (4 сторони).
- Час `programmed`: тік = виконання однієї команди; виконання починається з F1, команди йдуть зліва направо, виклик Fn переходить у Fn, після її кінця — повернення до місця виклику.
- Видимість повна, випадковості нема: один і той самий розвʼязок завжди дає однаковий результат.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робот | player | позиція, напрямок | виконує програму F1…F5; падає, якщо зійде з плиток |
| Плитка | terrain | колір: red / green / blue | по ній ходять; колір — умова для команд; можна перефарбувати |
| Порожнеча | hazard | — | крок сюди — робот падає, спроба провалена |
| Зірка | pickup | — | знімається, коли робот стає на клітину |
| Функція F1–F5 | mark | кількість слотів (задає автор пазла) | контейнер команд; F1 — точка входу |
| Команда | mark | тип + колір-умова (або без) | forward · left · right · call Fn · paint red/green/blue |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(forward)` → ЯКЩО `cell(ahead, tile)` → ТО `move(robot, dir)`; ЯКЩО `cell(ahead, void)` → ТО `lose` (робот падає).
- КОЛИ `exec(left|right)` → ТО `face(robot, turn90)`.
- КОЛИ `exec(paint c)` → ТО `paint(cell_under_robot, c)` — лише якщо автор пазла дозволив «special commands».
- КОЛИ `exec(call Fn)` → ТО `call(Fn)`: поточне місце кладеться на стек, виконання йде з початку Fn.
- КОЛИ `custom: «кінець функції»` → ТО повернення на наступну команду після виклику (зі стеку); стек порожній → `program_end`.
- КОЛИ `exec(cmd)` → ЯКЩО команда має колір c і `not color(cell_under_robot, c)` → ТО команда пропускається (без дії).
- КОЛИ `enter(robot, star)` → ТО `pickup`, `counter(stars_left, -1)`.
- КОЛИ `counter(stars_left, ==, 0)` → ТО `win` — одразу, навіть посеред програми.
- КОЛИ `program_end` → ЯКЩО `counter(stars_left, >, 0)` → ТО `lose` («не всі зірки»).
- КОЛИ `custom: «перевищено ліміт кроків / глибину стеку»` → ТО `crash` (?) — захист від нескінченної рекурсії.
- Хвостовий виклик `F1: forward, F1` = нескінченний цикл; виклик посеред функції будує стек і дає «зворотний хід» (повернення відкладених команд).
- Перемога: усі зірки зібрані · Поразка: падіння в порожнечу або кінець програми зі зірками на полі · Рахунок: нема очок за рівень; скорборд — кількість розвʼязаних пазлів і довжина найкоротших розвʼязків.

## Керування і ввід
- Програмування: перетягнути команду з палітри в слот функції; клік по команді/слоту — вибір кольору-умови (сірий = без умови).
- Кількість функцій і слотів у кожній задає пазл; зайві слоти не можна додати — головна складність.
- Виконання: **Go!** (запуск), **Step** (одна команда), повзунок швидкості Slow/Fast, **Back** — повернутися до редагування.
- Під час виконання підсвічується поточна команда; у пізніших версіях — показ стеку викликів (?).

## Вікна, меню, HUD
- `level-select` (`puzzle-select`): таблиця пазлів — Id, назва, «розвʼязано?», автор, складність (число 1–5), лайки/дизлайки, коментарі; сортування за датою, автором, складністю, популярністю.
- `game-screen`: поле з роботом; праворуч/знизу `program-slots` F1–F5; `command-palette` (дозволені в пазлі команди й кольори); кнопки Go!/Step/Back; `speed-slider`.
- `end-screen` «Congratulations! You've completed the puzzle» → оцінка складності (Very easy … Very hard) і «сподобалось / ні» → інший пазл або повтор.
- `editor-window` «Make a Puzzle»: розстановка плиток, зірок, робота; кількість слотів F1–F5; чекбокс «Allow special commands»; назва й опис; **Provide Solution** — автор мусить розвʼязати свій пазл.
- `help-window` / `tutorial-window`: Tutorial; посилання на Wiki (Puzzle Design Guidelines), форум, чат.
- `leaderboard`: Full scoreboard; `profile-window` гравця (`user.aspx`).
- Переходи: список → пазл → (Go!) виконання → Congratulations → оцінка → список; Make a Puzzle → розвʼязати → submit.

## Фічі поза полем
- `puzzle-bank` + `user-levels-browser` + `level-rating`: пазли гравців, голос складності 1–5 і лайк/дизлайк; пазл з популярністю ≤ −5 ховається.
- `level-editor` + `level-sharing`: публікація лише з власним розвʼязком (доказ розвʼязності).
- `leaderboard-online`: розвʼязані пазли; окремий скорборд найкоротших розвʼязків.
- `step-mode`, `speed-control`; форум-тред на кожен пазл.
- Акаунти (реєстрація), офіційні «кампанії»/туторіал; мобільні порти з офлайн-набором 1024+ пазлів.

## Варіації й родичі
- Lightbot (2008) — та сама ідея «головна + процедури», але без кольорових умов; RoboZZle жорсткіший через крихітні функції.
- Порти: Robot Trainer / RoboZZle Droid (Android, відкритий код), iPhone, WP7.
- Осі варіацій: **умови** (нема / колір під роботом / сенсори); **повтор** (рекурсія / цикли / jump); **змінюваність поля** (нема / paint — гравець пише «памʼять» фарбою); **ліміт** (слоти на функцію / загальний / розмір як метрика).

## Цікавинки для курсу
- Інтерпретатор зі стеком викликів, умовними командами й хвостовою рекурсією — 🥈 (стек явно, захист від нескінченності).
- Колір-умова на кожній команді — «if» без синтаксису — 📎.
- Paint як памʼять програми на полі (робот залишає мітки для себе) — 🥉.
- Редактор з обовʼязковим розвʼязком автора перед публікацією — 🥉.
- Банк пазлів з голосуванням складності й лайками — 📎.
- Скорборд найкоротших розвʼязків (метрика «кількість команд») — 🌱.

## Мапа на каталог
- Є: `collect-all` (зірки) · `environment-death` (падіння в порожнечу) · `level-bank` · `level-rating` · `in-game-editor` + `editor-playtest` · `score-records` / `leaderboard` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+command-program`, `+user-procedures`, `+recursion-loop`, `+conditional-color`, `+command-slots-limit`, `+step-execution`, `+code-editor-window` — спільні з Lightbot/Karel.
  - `+paint-cell-command` «Команда фарбує клітину» · entities/interact · 📎.
  - `+call-stack` «Стек викликів з поверненням» · game-logic · 🥈 · слот {max_depth}.
  - `+solvable-proof-on-submit` «Публікація лише з розвʼязком автора» · levels/editor · 🥉.
  - `+difficulty-vote` «Голос гравців за складність» · levels/bank · 📎.
  - `+shortest-solution-board` «Рекорд найкоротшої програми» · game-logic/score · 🌱.

## Пропозиції до словників
- `+trigger:exec(cmd)`, `+trigger:program_end` — спільні для сімʼї.
- `+cond:color(a, c)` — колір клітини під актором (як у Lightbot).
- `+effect:call(fn)` — виклик функції зі стеком; `+effect:paint` (є ⏳ `paint(cell, color)` — вживати його); `+effect:crash`.
- `+window:code-editor`; `+window:puzzle-submit` — форма публікації з назвою, описом і розвʼязком.
- `+ui:program-slots`, `+ui:command-palette`, `+ui:instruction-highlight`, `+ui:call-stack-view`.
- `+feature:difficulty-vote`, `+feature:solution-required`.
- `+axis:control` — `programmed`.

## Джерела
- ⭐ [RoboZZle (beta, браузер)](https://www.robozzle.com/beta/) — Tutorial, F1–F5, Paint red/green/blue, Go!/Step/Slow-Fast, Make a Puzzle з Provide Solution, рейтинги Very easy…Very hard.
- [robozzle.com](https://www.robozzle.com/) — платформи, автор Igor Ostrovsky.
- [Банк пазлів (JS)](https://www.robozzle.com/js/index.aspx) — колонки Difficulty, Liked/Disliked, сортування.
- [Igor Ostrovsky: hobby project (2009)](https://igoro.com/archive/my-hobby-project-a-social-puzzle-game-developed-in-silverlight/) — ціль «зібрати всі зірки», пазли гравців, голосування.
- [Igor Ostrovsky: перший місяць](https://igoro.com/archive/the-first-month-of-my-online-game/) — степ-дебагер, скорборд найкоротших, приховування при популярності ≤ −5.
- [RoboZZle-Droid на GitHub](https://github.com/lostmsu/RoboZZle-Droid) — Android-порт; опис F-Droid: «move, turn, repaint cells and call very short functions», 1024+ рівнів.
- YouTube: пошук «robozzle gameplay».

## Непевне
- (?) Розмір поля 16×12, максимум 10 слотів на функцію — з памʼяті.
- (?) Ліміт кроків/глибини стеку і що бачить гравець при переповненні — не перевірено.
- (?) Чи падіння зараховується одразу як поразка з повідомленням, чи просто зупинка — з памʼяті (автор згадує баг «мав загинути, впавши з плитки»).
- (?) Візуалізація стеку — у 2009 була лише в планах; чи зʼявилась пізніше — не перевірено.
- Wiki robozzle.com (Puzzle Design Guidelines) не відкрилась (таймаут).
