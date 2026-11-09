---
title: Robots (BSD) / Chase / Daleks
slug: robots
aka: [Chase, Chase!, Escape!, Daleks, Zombies, HiVolts, GNOME Robots, robots(6)]
family: roguelike
also: [maze-arcade, thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: state
year: 1976
platforms: [mainframe (DTSS, Honeywell), Unix/BSD, Mac, PC, Linux (GNOME)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Robots_(1984_video_game)", best: true, note: "Wikipedia (стаття Chase): правила, телепорт, купи брухту, «танк», історія 1976 → 4.3BSD"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Chase_(video_game)", note: "та сама стаття; варіанти Escape!, Robot Minefield, Daleks, HiVolts"}
  - {kind: other, url: "https://man.openbsd.org/robots.6", note: "man robots(6): клавіші hjklyubn, t, w, >, очки 10 за робота, бонус за очікування, -r real-time"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=bsd+robots+game+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [move-8dir, chase-player, chase-greedy, touch-death, teleport-random-exit, spawn-random-cell, destroy-all-enemies, sequential-levels, progress-acceleration, event-points, score-records, keyboard-controls, console-render, gui-render, realtime-ai, player-death, cell-transform, +collision-junk, +wait-until-end, +run-direction, +safe-teleport, +auto-teleport]
proposes: ["+trigger:collide(a, b)", "+effect:wait_until(cond)", "+effect:run(dir)", "+feature:auto-teleport", "+feature:start-level", "+card:collision-junk", "+card:wait-until-end", "+card:safe-teleport"]
author: opus
date: 2026-11-09
---

# Robots (BSD) / Chase / Daleks — роботи щоходу крокують до тебе; зіштовхни їх між собою

## Суть
Гравець `@` на прямокутному полі серед натовпу роботів `+`. Після кожного ходу гравця **кожен робот робить один крок до нього найкоротшим шляхом** (8 напрямків). Роботи, що зіткнулися між собою, гинуть і лишають купу брухту `*`, яка вбиває кожного наступного робота, що на неї ступить. Гравець не має зброї (в оригіналі): єдині інструменти — позиціювання і **телепорт у випадкову клітину**, який може врятувати або покласти просто під робота. Знищив усіх — наступне поле, роботів більше.

## Поле і час
- Квадратна сітка, суміжність 8 (ортогональ + діагоналі); рамка поля — межа.
- Покроково: хід гравця = один тік, після нього одночасно ходять усі роботи. Режим `-r` у BSD — real-time: роботи ходять щонайменше раз на 3 секунди після першого ходу.
- Усе видно (`info: full`); випадковість — лише в розстановці на старті рівня і в точці телепорту (`random: setup` + runtime-телепорт, див. «Непевне»).
- Консоль: роботи `+`, брухт `*`, гравець `@` (BSD robots); у Daleks/GNOME — спрайти.
- Ранні Chase!-версії: на полі одразу нерухомі смертельні обʼєкти (електропаркан/стовпи); robots-версії — поле чисте, перешкоди народжуються з зіткнень.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець `@` | player | 1 життя | крок у 8 напрямків, стоїть, телепорт, «чекати до кінця» |
| Робот `+` | enemy | — | щохід — 1 крок до гравця найкоротшим шляхом |
| Купа брухту `*` | hazard | нерухома | робот, що ступив на неї, гине; гравцю — стіна |
| Танк (окремі версії) | enemy | не руйнується | поводиться як робот, але переживає зіткнення |
| Смертельна перешкода (Chase!) | hazard | нерухома | вбиває і гравця, і робота при вході |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move dir)` → ЯКЩО `free(target)` і `not occupied(target, junk)` → ТО `move(player, dir)`; інакше `block`.
- КОЛИ `input(wait)` → ТО `custom: «пропустити хід — роботи ходять»`.
- КОЛИ `turn_end(player)` → ТО для кожного робота `move(robot, step toward player)` (`chase-greedy`, 8 напрямків).
- КОЛИ `contact(robot, robot)` → ТО `disappear_both`, `spawn_at(junk, cell)`, `score(+10)` за кожного загиблого.
- КОЛИ `contact(robot, junk)` → ТО `disappear_a`, `score(+10)`.
- КОЛИ `contact(robot, player)` → ТО `lose`.
- КОЛИ `contact(robot, hazard)` (Chase!) → ТО `disappear_a`; КОЛИ `contact(player, hazard)` → ТО `lose`.
- КОЛИ `contact(tank, junk|robot)` (варіант) → ТО `custom: «танк переживає, жертва гине»`.
- КОЛИ `input(teleport)` → ТО `teleport(player, random cell)`, далі звичайний хід роботів (може впасти поруч з роботом).
- КОЛИ `input(safe teleport)` (GNOME тощо) → ЯКЩО `count(safe_teleports, >, 0)` → ТО `custom: «телепорт у клітину, куди жоден робот не дістане цього ходу»`, `counter(safe_teleports, −1)`.
- КОЛИ `input(screwdriver)` (Daleks) → ЯКЩО `count(charges, >, 0)` → ТО `custom: «знищити роботів у сусідніх клітинах»`, `counter(charges, −1)`.
- КОЛИ `input(w)` → ТО `custom: «чекати, доки не загинуть усі роботи або гравець»`; ЯКЩО гравець вижив → ТО `score(+10 % за кожного робота, що загинув під час очікування)`; ЯКЩО загинув → бонусу нема.
- КОЛИ `no_moves(player)` → ЯКЩО `mode(auto-teleport)` (`-t`) → ТО `teleport(player, random cell)`.
- КОЛИ `all_gone(robot)` → ТО `next_level`, `spawn(more robots)` (традиційно +10 за рівень).
- Перемога (рівень): усі роботи знищені. Поразка: робот (або перешкода) у клітині гравця. Рахунок: 10 очок за робота + бонус очікування; таблиця 5 найкращих на користувача (`$HOME/.robots.scores`).

## Керування і ввід
- BSD: `h j k l` — ліворуч/вниз/вгору/праворуч, `y u b n` — діагоналі; `.`/пробіл — стояти; **великі** `H J K L Y U B N` — бігти в напрямку, скільки можна; `>` — стояти, скільки безпечно; `t` — телепорт; `w` — чекати до кінця; `q` — вийти; `^L` — перемалювати.
- Більшість команд беруть числовий префікс-повтор (крім real-time).
- Гра «зупиняє тебе на межі»: біг і `>` не заведуть під робота — ризикує лише `w`.
- Daleks/GNOME — клавіатура або клік мишею по сусідній клітині (?).

## Вікна, меню, HUD
- `game-screen`: поле символами, `score`, `level-number`, `remaining-counter` (роботів) (?).
- `leaderboard`: показ таблиці після гри, якщо потрапив; `-s` — лише показати рекорди.
- `settings-window` — у GNOME Robots (тип гри, графіка, клавіші) (?); BSD — опції командного рядка `-a` (старт з вищого рівня), `-j` (показувати лише кінцеву позицію бігу), `-r`, `-t`.
- Переходи: старт → `game-screen` → (смерть) → `leaderboard` → вихід.

## Фічі поза полем
- `leaderboard-local` — файл рекордів, 5 на користувача, імʼя з `LOGNAME`.
- `start-level` (`-a`) — почати з вищого рівня; `auto-teleport` (`-t`); `speed-control`-подібне `-j` для повільних терміналів.
- Real-time-режим `-r` (і в Escape! від Sublogic) — та сама гра з годинником.

## Варіації й родичі
- Chase (DTSS, Dartmouth BASIC, поч. 1970-х; *Creative Computing* 1976) → Escape! (TRS-80: + танк, 2 телепорти) → HiVolts (PLATO) → Logan (real-time) → Robot Minefield 1983 (4 вороги, гравець лише ортогонально, вороги діагонально, real-time) → Daleks, Zombies, robots (1984; Allan R. Black, 4.3BSD 1986) → GNOME Robots.
- Robotron: 2084 — real-time нащадок ідеї.
- Родичі в корпусі: [theseus-and-the-minotaur](theseus-and-the-minotaur.md) (детермінований переслідувач, яким маніпулюєш), [rogue](rogue.md) (ті самі клавіші hjklyubn), [868-hack](868-hack.md).
- Осі варіацій: **перешкоди** (з самого початку / лише брухт з зіткнень) · **зброя** (нема / обмежена «викрутка» поруч / безпечний телепорт) · **швидкість роботів** (1 крок / 2 кроки / незнищенний танк) · **суміжність** (8 / гравець 4 проти 8 ворогів) · **час** (покроково / real-time).

## Цікавинки для курсу
- Уся гра — консольна, ≈150 рядків: поле, жадібна погоня 8-сусідами, зіткнення → брухт — 🌱 (ідеальне перше роглайк-завдання).
- Одночасний хід роботів і розвʼязання зіткнень (два у клітині, робот на брухті) — 📎 (порядок оновлення, «спершу всі ходять, потім колізії»).
- «Безпечний» біг і `>`: перевірка, чи не зайде гравець під удар, моделюванням наступного ходу — 📎.
- Безпечний телепорт: знайти клітину, куди жоден робот не дістане за хід — 🌱/📎 (маска досяжності 8-сусідів).
- `w` з бонусом: симуляція до кінця з ризиком — 📎.
- Розвʼязувач «чи можна вижити без телепорту» — пошук у дереві станів — 🥈.

## Мапа на каталог
- Є: `move-8dir` · `chase-player`/`chase-greedy` ↔ крок до гравця · `touch-death` · `teleport-random-exit` ↔ телепорт у випадкову клітину · `spawn-random-cell` ↔ розстановка · `destroy-all-enemies` · `sequential-levels` + `progress-acceleration` (+роботи за рівень) · `event-points` · `score-records` · `keyboard-controls` · `console-render`/`gui-render` · `realtime-ai` (`-r`) · `cell-transform` (брухт на місці зіткнення).
- **Нема** → пропозиції карток:
  - `+collision-junk` «Вороги гинуть від зіткнення між собою, лишають перешкоду» · entities/death · 🌱 · слоти {що лишається}.
  - `+wait-until-end` «Чекати до розвʼязки з бонусом/ризиком» · game-logic/score · 📎.
  - `+run-direction` «Біг у напрямку до упору/небезпеки» · entities/move · 🌱.
  - `+safe-teleport` «Телепорт у недосяжну ворогами клітину, обмежено» · entities/interact · 📎 · слоти {uses}.
  - `+auto-teleport` «Автотелепорт, коли нема безпечного ходу» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+trigger:collide(a, b)` — дві рухомі сутності одночасно опинились в одній клітині (симетрично, на відміну від `contact`, де A входить у B).
- `+effect:wait_until(cond)` — пропускати ходи, доки не виконається умова (BSD `w`, `>`).
- `+effect:run(dir)` — повторювати крок, поки безпечно/можливо.
- `+feature:auto-teleport` — автоматичний рятувальний хід; `+feature:start-level` — почати з вищого рівня.
- `+card:collision-junk` · `+card:wait-until-end` · `+card:safe-teleport` — див. вище.

## Джерела
- ⭐ [Wikipedia: Robots / Chase](https://en.wikipedia.org/wiki/Robots_(1984_video_game)) — правила, телепорт, брухт, танк, усі гілки варіантів і дати.
- [Wikipedia: Chase (video game)](https://en.wikipedia.org/wiki/Chase_(video_game)) — та сама стаття (редирект), історія Dartmouth → BSD.
- [man robots(6), OpenBSD](https://man.openbsd.org/robots.6) — клавіші, очки, бонус `w`, опції `-a -j -r -s -t`, файл рекордів.

## Непевне
- (?) Розмір поля BSD robots (в памʼяті 60×22 (?)) і стартова кількість роботів (10 (?)) — у man-сторінці не названо; Wikipedia: «+10 роботів за рівень» лише як традиція.
- (?) Daleks (Mac, 1984): «звукова викрутка» знищує сусідніх, кількість зарядів і телепортів на рівень — з памʼяті; Wikipedia каже загально про «close-range weapon, limited».
- (?) GNOME Robots: «швидкі» роботи на 2 кроки, налаштування типу гри, керування мишею — з памʼяті.
- (?) `random` — фактично `both` (телепорт випадковий під час гри); залишив `setup`, бо поле після розстановки детерміноване, а випадковість — лише інструмент гравця.
- (?) HUD BSD-версії (рядок рахунку/рівня) — не бачив скріншота.
