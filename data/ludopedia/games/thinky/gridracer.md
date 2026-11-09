---
title: GridRacer
slug: gridracer
aka: [Grid Racer]
family: thinky
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: race
year: 2024
platforms: [web]
links:
  - {kind: itch, url: "https://jackkutilek.itch.io/gridracer", best: true, note: "грати в браузері; керування, правила, редактор з картинки, коментарі гравців про порядок перевірок"}
  - {kind: other, url: "https://jackkutilek.itch.io/gridracer/devlog/763467/checkpoints-leaderboards", note: "devlog 11.07.2024: чекпойнти, спліти, онлайн-таблиці"}
  - {kind: other, url: "https://itch.io/jam/thinky-puzzle-game-jam-4/rate/2813510", note: "сторінка джему: «turn-based momentum racing», 72 учасники"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Racetrack_(game)", note: "паперовий прабатько: векторний рух, 9 варіантів ходу, аварії"}
  - {kind: steam, url: "https://store.steampowered.com/app/1924180/Phantom_Spark/", note: "друге натхнення автора"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=GridRacer+jack+kutilek+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-by-input, inertia-slide, impassable-cells, reach-exit, checkpoint, move-counter, undo-unlimited, restart-level, level-select, score-records, leaderboard, level-exchange, keyboard-controls, path-preview, +vector-momentum, +segment-collision, +checkpoint-groups, +level-from-image, +split-times]
proposes: ["+effect:accelerate", "+trigger:cross", "+ui:split-times", "+ui:velocity-vector", "+feature:level-from-image", "+feature:personal-best", "+card:vector-momentum", "+card:segment-collision", "+card:level-from-image"]
author: opus
date: 2026-11-09
---

# GridRacer — Racetrack на клітинці: щоходу підправляєш вектор швидкості й летиш до фінішу за найменше ходів

## Суть
Покрокова гонка з імпульсом, зроблена на Thinky Puzzle Game Jam 4 (тема «Extreme Sports»). Болід має вектор швидкості; щоходу гравець трохи змінює його й «відпускає» хід — машина стрибає на весь вектор. Мета — пройти всі чекпойнти й дістатися фінішу за найменшу кількість ходів; удар об стіну додає штраф. Це паперовий Racetrack 1960-х, перетворений на пазл-оптимізацію з онлайн-таблицями.

## Поле і час
- Квадратна сітка зверху; трек — стіни, чекпойнти, фініш, старт. Камера йде за болідом (гравці просили зум на весь трек — його не було на старті (?)).
- Покроково: тік = натиснути «рух» після налаштування імпульсу; часу на роздуми не обмежено.
- Хід — відрізок від поточної позиції на величину вектора; перевірки йдуть уздовж відрізка, а не лише в кінцевій клітині.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Болід | player | позиція, вектор швидкості (vx, vy) | щоходу зсувається на вектор; вектор змінюється вводом |
| Стіна (чорна) | static | — | удар об неї — штраф до лічильника ходів і втрата імпульсу (?) |
| Чекпойнт (синій) | zone | звʼязна група клітин = 1 чекпойнт | треба торкнутися всіх до фінішу |
| Фініш (червоний) | zone | — | досягти після всіх чекпойнтів |
| Старт (зелений) | static | кілька → верхній лівий | точка появи з нульовою швидкістю (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `custom: «змінити запланований вектор швидкості на крок у напрямку стрілки»`; дві стрілки разом — діагональна зміна (?).
- КОЛИ `input(move)` → ТО `move(car, car + velocity)`, `counter(moves, +1)`.
- КОЛИ `enter(car, checkpoint)` (будь-яка клітина відрізка ходу) → ТО `counter(checkpoints, +1)`, `custom: «записати спліт-час і порівняти з особистим рекордом»`.
- КОЛИ `enter(car, goal)` → ЯКЩО `count(checkpoints_left, =, 0)` → ТО `win`.
- КОЛИ `enter(car, wall)` → ТО `custom: «штраф імпульсу до лічильника ходів»`, `block`.
- КОЛИ `custom: «один відрізок ходу торкається кількох типів клітин»` → ТО `custom: «порядок перевірки: чекпойнти, потім фініш, потім стіни»` — тому останнім ходом можна врізатися в стіну, якщо відрізок уже зачепив усі чекпойнти й фініш.
- КОЛИ `input(undo)` → ТО `custom: «відкотити один хід»`; КОЛИ `input(restart)` → ТО `restart`.
- КОЛИ `level_end` → ТО `score(moves)`, `custom: «надіслати результат у таблицю, якщо введено імʼя»`.
- Перемога: фініш після всіх чекпойнтів · Поразки нема · Рахунок: кількість ходів + штрафи, менше — краще.

## Керування і ввід
- Стрілки / WASD / IJKL — налаштувати імпульс; `Space` / `X` — виконати хід; `Z` — undo; `R` — рестарт.
- Деякі клавіатури не реєструють кілька клавіш одночасно — автор радить перемкнутися на WASD чи IJKL.

## Вікна, меню, HUD
- `level-select`: список треків, поле для імені гравця, кнопка завантаження власного треку-картинки.
- `game-screen`: трек, болід, `move-counter`, спліти чекпойнтів проти особистого рекорду (`split-times`).
- `leaderboard`: топ результатів треку (у кожного власного треку — своя таблиця).
- `end-screen` (?): результат проїзду і місце в таблиці.
- Переходи: level-select → game-screen → фініш → таблиця → level-select.

## Фічі поза полем
- `leaderboard-online` з іменем; порожнє імʼя — офлайн, лишається `personal-best` локально.
- `level-from-image`: трек = картинка, де чорні пікселі — стіни, сині — чекпойнти, червоні — фініш, зелені — старт; ім'я файла має бути унікальним.
- `undo` ∞, `restart-level`.
- Безкоштовна HTML5-гра на itch.io, лише клавіатура.

## Варіації й родичі
- Racetrack (паперова гра, Martin Gardner 1973): 9 варіантів ходу — кожна координата вектора змінюється ≤ 1; аварія при виїзді з треку; варіанти — масло (не можна міняти швидкість), турбо, 4-сусідство.
- Triplanetary (гекс-поле, космос), Phantom Spark (реал-тайм гонка на найкращий час).
- Осі варіацій: **зміна вектора** — ±1 по осі / 8-сусідство / лише 4 напрямки; **стіна** — аварія / штраф / відскок (просили гравці); **ціль** — перший на фініші (мультиплеєр) / найменше ходів (соло) / найкращий час.

## Цікавинки для курсу
- Векторний рух: позиція + швидкість, ввід змінює прискорення — 🌱.
- Перетин відрізка ходу з клітинами (Брезенхем / DDA) і порядок перевірок — 🥉.
- Звʼязні групи клітин як один чекпойнт (flood fill) — 📎.
- Трек із PNG за кольорами пікселів — 📎.
- Розвʼязувач: BFS у просторі (x, y, vx, vy) з бітмаскою чекпойнтів — 🥈 (класична задача оптимального Racetrack).
- Онлайн-таблиця на трек і спліти проти особистого рекорду — 🥉.

## Мапа на каталог
- Є: `move-by-input` · `inertia-slide` (імпульс зберігається між ходами) · `impassable-cells` · `reach-exit` · `checkpoint` · `move-counter` · `undo-unlimited` · `restart-level` · `level-select` · `score-records` · `leaderboard` · `level-exchange` (власні треки) · `keyboard-controls` · `path-preview` (?).
- **Нема** → пропозиції карток:
  - `+vector-momentum` «Векторний рух з обмеженим прискоренням» · entities/move · 🥉 · слоти {accel: 1|n, neighbourhood: 4|8}.
  - `+segment-collision` «Перевірка відрізка ходу, а не кінцевої клітини» · entities/legality · 🥉.
  - `+checkpoint-groups` «Чекпойнт = звʼязна група клітин» · game-logic/win · 📎.
  - `+level-from-image` «Рівень з картинки за кольорами» · levels/format · 📎.
  - `+split-times` «Спліти проти особистого рекорду» · interface/hud · 📎.

## Пропозиції до словників
- `+effect:accelerate` — змінити вектор швидкості сутності на крок (Racetrack).
- `+trigger:cross` — відрізок руху перетнув клітину / зону (не лише кінцева клітина).
- `+ui:split-times` — час/ходи на чекпойнтах проти найкращого; `+ui:velocity-vector` — стрілка поточного вектора (?).
- `+feature:level-from-image` — завантажити рівень як картинку; `+feature:personal-best` — локальний особистий рекорд на рівень.
- `+card:vector-momentum`, `+card:segment-collision`, `+card:level-from-image` — див. вище.
- ⏳-слова, вжиті тут: `input`, `enter`, `level_end`, `count`, `move`, `counter`, `restart`, `zone`.

## Джерела
- ⭐ [GridRacer на itch.io](https://jackkutilek.itch.io/gridracer) — правила, керування, кольори редактора, таблиці; коментар yergicol про порядок перевірок «checkpoints, then goals, then walls».
- [Devlog «Checkpoints & Leaderboards»](https://jackkutilek.itch.io/gridracer/devlog/763467/checkpoints-leaderboards) — спліти проти PB, онлайн-таблиці (11.07.2024).
- [Сторінка Thinky Puzzle Game Jam 4](https://itch.io/jam/thinky-puzzle-game-jam-4/rate/2813510) — опис-гасло, відгуки.
- [Racetrack (game) — Wikipedia](https://en.wikipedia.org/wiki/Racetrack_(game)) — правила оригіналу й варіанти.
- [Phantom Spark](https://store.steampowered.com/app/1924180/Phantom_Spark/) — названий автором родич.

## Непевне
- (?) Точна модель прискорення: ±1 по кожній осі за хід, як у Racetrack, чи інша; чи дозволено дві стрілки разом (коментар гравця про утримання ←+↑ це натякає).
- (?) Розмір штрафу за стіну і що стається з вектором після удару (обнуляється?).
- (?) Чому результати в таблицях дробові («author time: 93.16») — можливо, частка останнього ходу до фінішу або справжній час.
- (?) Рік: джем 4 і devlog — 2024; черга давала 2025.
- (?) Чи є прев'ю траєкторії наступного ходу і стрілка вектора на екрані.
- (?) Кількість вбудованих треків не вказана.
