---
title: Rodent's Revenge
slug: rodents-revenge
aka: [Помста гризуна, Microsoft Entertainment Pack 2 — Rodent's Revenge]
family: push-slide
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 1991
platforms: [Windows, iOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rodent%27s_Revenge", best: true, note: "правила: замкнути котів блоками → сир; нерухомі блоки, ями, мишоловки, клубки; 3 життя, рівні 1–50 і далі, годинник із синьою міткою, рекорди за весь час і за 24 год"}
  - {kind: other, url: "https://en.wikipedia.org/wiki/Microsoft_Entertainment_Pack", note: "входить у Microsoft Entertainment Pack 2 і Best of MEP (1994)"}
  - {kind: play, url: "https://www.classicreload.com/rodents-revenge.html", note: "грати в браузері; 50 рівнів у будь-якому порядку, стрілки"}
  - {kind: other, url: "https://github.com/pierreyoda/o2r", note: "Open Rodent's Revenge (C++ ремейк): коти ходять і по діагоналі, шукають шлях A*, інакше блукають"}
  - {kind: other, url: "https://gamebrew.org/wiki/Rodent%27s_Revenge_DS", note: "DS-клон: ті самі 50 рівнів, 5 швидкостей гри, рекорди, вибір рівня"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Rodent%27s+Revenge+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-by-input, keyboard-controls, push-object, impassable-cells, chase-player, touch-death, environment-death, player-death, item-pickup, cell-transform, spawn-schedule, event-points, time-bonus, score-records, level-select, sequential-levels, progress-acceleration, +push-chain, +enclosure-capture, +stun-hole, +flying-hazard, +clock-reinforcement]
proposes: ["+effect:push_line", "+trigger:all_trapped", "+cond:enclosed", "+ui:spawn-clock", "+feature:recent-highscores", "+card:clock-reinforcement", "+card:stun-hole"]
author: opus
date: 2026-11-09
---

# Rodent's Revenge — миша в реальному часі штовхає ряди блоків і замикає котів, а замкнені коти стають сиром

## Суть
Аркадна головоломка з Microsoft Entertainment Pack 2 (автор Christopher Lee Fraley): миша на клітинному полі, повному рухомих і нерухомих блоків, штовхає блоки так, щоб **замкнути кожного кота** — тоді коти перетворюються на сир, який миша зʼїдає за очки. Коти тим часом женуться за мишею; поле ускладнюють ями, мишоловки й літаючі клубки ниток. Годинник рівня — це розклад підкріплень: щоразу, як стрілка доходить до синьої мітки, на поле приходять нові коти.

## Поле і час
- Квадратна сітка, щільно заставлена рухомими блоками, з вкрапленнями нерухомих; розмір поля — (?).
- Real-time: коти ходять своїм тіком незалежно від гравця; темп задає налаштування швидкості (кількість швидкостей — (?)).
- Годинник на панелі: доходить до синьої мітки → зʼявляються нові коти → мітка зсувається далі по циферблату → годинник іде знову.
- Рівні 1–50; після 50-го — 51-й і далі без верхньої межі; складність росте через кількість рухомих/нерухомих блоків і небезпек.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Миша | player | 3 життя | рух клітинами; штовхає ряд рухомих блоків |
| Кіт | enemy | — | женеться за мишею; дотик — миша втрачає життя |
| Замкнений кіт | enemy | стан trapped | не може зробити жодного кроку; разом з іншими перетворюється на сир |
| Сир | pickup | очки | лишається на місці кота; миша зʼїдає за очки |
| Рухомий блок | object | — | зсувається поштовхом; ряд блоків зсувається разом |
| Нерухомий блок | static | — | не штовхається; зупиняє ряд; заважає ходити |
| Яма (sink hole) | hazard | кілька секунд | миша, що стала, застрягає на кілька секунд |
| Мишоловка | hazard | — | миша, що стала, гине |
| Клубок ниток | hazard | летить | рухається полем; дотик — миша гине |
| Годинник | static | синя мітка | розклад приходу нових котів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(mouse, dir)`.
- КОЛИ `contact(mouse, block)` → ЯКЩО `custom: «за суцільним рядом рухомих блоків у напрямку руху є вільна клітина»` → ТО `push` (увесь ряд на 1), `move(mouse, dir)`; ЯКЩО ряд упирається в нерухомий блок або край → ТО `block`.
- КОЛИ `tick` → ТО `custom: «кожен вільний кіт робить крок у бік миші»` (обхід перешкод і діагоналі — (?)).
- КОЛИ `no_moves(cat)` → ТО `set_state(cat, trapped)`.
- КОЛИ `custom: «усі коти на полі замкнені»` → ТО `transform(cat, cheese)` для кожного.
- КОЛИ `contact(mouse, cheese)` → ТО `pickup`, `score(n)`.
- КОЛИ `contact(cat, mouse)` → ЯКЩО `not state(cat, trapped)` → ТО `lives(-1)`.
- КОЛИ `enter(mouse, sink_hole)` → ТО `stun(mouse, n)` — кілька секунд не рухається.
- КОЛИ `enter(mouse, mouse_trap)` → ТО `lives(-1)`.
- КОЛИ `contact(yarn, mouse)` → ТО `lives(-1)`.
- КОЛИ `counter(clock, ==, blue_mark)` → ТО `spawn(cat)` (кілька), `custom: «синя мітка зсувається далі по циферблату»`, `timer(start)`.
- КОЛИ `all_gone(cat)` (нема вільних котів, усі стали сиром) → ТО `score(level_bonus + time_bonus)`, `next_level`.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`, `window(leaderboard)`.
- Перемога: рівень — живим замкнути всіх котів. · Поразка: втрачено 3 життя. · Рахунок: за пройдений рівень + зʼїдений сир + бонус за швидкість проходження і складність рівня.

## Керування і ввід
- Клавіатура: стрілки — рух миші (поштовх = крок у блок); чи є діагоналі на цифровому блоці — (?).
- Деякі версії дозволяють керувати мишею-маніпулятором (?).
- Пауза, новий рівень, вибір стартового рівня — з меню вікна Windows.

## Вікна, меню, HUD
- `game-screen` — поле; панель: годинник із синьою міткою (`spawn-clock`), `score`, `lives` (?), `level-number` (?).
- `level-select` — вибір стартового рівня 1–50.
- `settings-window` (?) — швидкість гри.
- `leaderboard` — дві таблиці: найкращі ігри за весь час і за останні 24 години.
- `help-window` (?) — довідка Windows Help, як у всіх іграх пакета.
- `end-screen` (?) — кінець гри, перехід до рекордів.
- Переходи: запуск → `game-screen` (рівень 1 або обраний) → (усі коти замкнені) наступний рівень → (0 життів) `leaderboard`.

## Фічі поза полем
- `levels-sequential` без `level-unlock`: стартовий рівень обирається вільно (1–50), після 50-го рівні йдуть без кінця (`mode-endless`-подібно).
- `speed-control` — налаштування швидкості гри (у клонах 4–5 швидкостей) (?).
- `leaderboard-local` з окремою таблицею «за 24 години» — `recent-highscores`.
- `pause` (?).
- Перевидання для iOS (09.01.2013).

## Варіації й родичі
- Клони й ремейки: Open Rodent's Revenge (C++), DS-homebrew з тими самими 50 рівнями, Vermin's Vengeance (itch, 4 швидкості, сир дає життя), численні JS/Java/Unity-ремейки.
- Осі варіацій:
  - **як ворога нейтралізують**: розчавити ковзним блоком (`pengo`) / заморозити в блок (Kickle Cubicle) / **замкнути без виходу** (Rodent's Revenge, Libble Rabble);
  - **поштовх**: один ящик (`sokoban`) / ряд до вільної клітини (Rodent's Revenge, `mazezam`) / ковзання до упору (`pengo`);
  - **підкріплення**: нема / за кожного знищеного (Pengo) / за годинником (Rodent's Revenge).
- Родичі в сімʼї: `pengo`, `chew-man-fu` (Sokoban у real-time), `mazezam`, `sokoban`; поза сімʼєю — `libble-rabble` (замикання петлею), `kickle-cubicle`.

## Цікавинки для курсу
- Поштовх ряду: скан у напрямку руху до першої не-блок клітини; вільна → зсув усіх, стіна → нічого — 📎.
- «Кіт замкнений» = у кота нема жодного легального кроку; перевірка для всіх котів після кожного тіку — 🥉.
- Перетворення всіх замкнених котів на сир і поїдання сиру — 🌱 (`transform` + `pickup`).
- Погоня кота з діагоналями: жадібний крок або A* — 🥉 / 🥇.
- Годинник із міткою, що зсувається, як розклад хвиль — 📎.
- Яма-пастка, що заморожує гравця на кілька секунд, і мишоловка — 🌱.
- Таблиця рекордів з двома зрізами (усе / 24 год) — 📎 (фільтр за датою).

## Мапа на каталог
- Є: `move-by-input` + `keyboard-controls` ↔ рух миші; `push-object` ↔ поштовх блока; `impassable-cells` ↔ нерухомі блоки; `chase-player` ↔ коти; `touch-death` ↔ кіт, клубок; `environment-death` ↔ мишоловка; `player-death` ↔ 3 життя; `item-pickup` + `event-points` ↔ сир; `cell-transform` ↔ кіт → сир; `spawn-schedule` ↔ коти за годинником; `time-bonus` ↔ бонус за швидкість; `score-records` ↔ рекорди; `level-select` + `sequential-levels` ↔ рівні 1–50 і далі; `progress-acceleration` ↔ складність росте з рівнем.
- **Нема** → пропозиції карток:
  - `+push-chain` (вже пропонована Spacekoban, Fish Fillets) — ряд блоків до першої вільної клітини.
  - `+enclosure-capture` (вже пропонована Libble Rabble, Cathedral) — замкнений ворог перетворюється.
  - `+clock-reinforcement` «Годинник-розклад підкріплень» · game-logic/waves · 📎 · слот {mark_step}.
  - `+stun-hole` «Яма, що тримає гравця N секунд» · entities/interact · 🌱 · слот {duration}.
  - `+flying-hazard` «Літаюча небезпека, що вбиває дотиком» · entities/move · 🌱 (клубки).

## Пропозиції до словників
- `+effect:push_line` — зсунути весь ряд обʼєктів на 1 (до першої вільної клітини).
- `+trigger:all_trapped` — усі вороги виду замкнені (жоден не має ходу).
- `+cond:enclosed` — сутність не має шляху назовні / жодного вільного сусіда.
- `+ui:spawn-clock` — циферблат із міткою наступного підкріплення.
- `+feature:recent-highscores` — таблиця рекордів за останні 24 години поруч із загальною.
- `+card:clock-reinforcement`, `+card:stun-hole` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Rodent's Revenge](https://en.wikipedia.org/wiki/Rodent%27s_Revenge) — мета, кіт → сир, рухомі/нерухомі блоки, ями, мишоловки, клубки, 3 життя, рівні 1–50 і далі, годинник із синьою міткою, очки і бонус, дві таблиці рекордів, iOS 2013.
- [Wikipedia: Microsoft Entertainment Pack](https://en.wikipedia.org/wiki/Microsoft_Entertainment_Pack) — MEP 2 (1991), Best of MEP.
- [ClassicReload](https://www.classicreload.com/rodents-revenge.html) — гра в браузері, 50 рівнів у будь-якому порядку, стрілки.
- [Open Rodent's Revenge](https://github.com/pierreyoda/o2r) — ремейк: коти з діагоналями й A*, інакше випадкові кроки.
- [Rodent's Revenge DS (GameBrew)](https://gamebrew.org/wiki/Rodent%27s_Revenge_DS) — ті самі 50 рівнів, 5 швидкостей, рекорди, вибір рівня.
- [tassaron/rodents-revenge](https://github.com/tassaron/rodents-revenge) — JS-ремейк: код поштовху ряду (зсув до першої вільної клітини, стіна зупиняє).
- YouTube: пошук «Rodent's Revenge gameplay».

## Непевне
- (?) Поштовх **цілого ряду** блоків — з коду ремейків і черги куратора; у Wikipedia лише «штовхати блоки».
- (?) Коти перетворюються на сир, коли замкнені **всі** (читання фрази Wikipedia «Doing so…»), чи кожен окремо через якийсь час (так у ремейках).
- (?) Чи коти ходять по діагоналі в оригіналі (так у ремейках) і чи миша має 8 напрямків.
- (?) Кількість налаштувань швидкості (клони: 4–5), розмір поля, звідки приходять нові коти, як рухаються клубки.
- (?) Скільки очок дає сир, рівень і бонус; чи сир дає додаткові життя (так лише в одному клоні).
- (?) Склад меню (Game/Options/Help), панель життів і номер рівня на екрані — не перевірено.
