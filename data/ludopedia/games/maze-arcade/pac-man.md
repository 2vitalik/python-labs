---
title: Pac-Man (Пекмен) і Ms. Pac-Man
slug: pac-man
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: collect
year: 1980
platforms: [arcade, Atari 2600, NES, PC, mobile, web]
links:
  - {kind: other, url: "https://pacman.holenet.info/", best: true, note: "The Pac-Man Dossier (Jamey Pittman) — цілі привидів, таймери, таблиця рівнів"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pac-Man", note: "історія, привиди, kill screen, ідеальний рахунок"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ms._Pac-Man", note: "відмінності Ms. Pac-Man"}
  - {kind: other, url: "https://www.gamedeveloper.com/design/the-pac-man-dossier", note: "Dossier у Gamasutra/Game Developer"}
  - {kind: other, url: "https://arcade-museum.com/dipswitch-settings/pac-man", note: "DIP-налаштування: життя 1/2/3/5, бонус 10k/15k/20k/нема"}
  - {kind: official, url: "https://pacman.com/en/history/", note: "офіційна історія від Bandai Namco"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pac-man+arcade+ghost+ai+explained", note: "пошук; пояснення AI привидів"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=pac-man", note: "пошук; сучасні перевидання"}
stage: v2
coverage: 75
mechanics: [move-4dir, move-auto, collect-all, touch-death, chase-greedy, random-walk, temporary-modes, speed-per-type, spawn-points, respawn, event-points, progress-acceleration, mode-indicator, +target-tile-ai, +scatter-chase-schedule, +ghost-house-release, +escalating-kill-points, +eyes-return-home, +center-bonus-item, +wrap-edges, +speed-zones, +no-turn-zone, +enrage-on-low-remaining, +cornering-assist, +extra-life-threshold]
proposes: ["+trigger:counter", "+trigger:state_off", "+trigger:enter", "+cond:mode", "+cond:in_range", "+effect:set_state", "+effect:set_target", "+effect:speed", "+effect:wrap", "+effect:respawn", "+effect:face", "+role:spawner", "+role:terrain", "+ui:level-icons", "+window:intermission", "+window:attract-demo", "+feature:operator-settings"]
author: opus
date: 2026-11-02
---

# Pac-Man — зʼїж усі точки в лабіринті, тікаючи від чотирьох привидів з різними характерами

## Суть
Пекмен бігає лабіринтом і їсть 244 точки; рівень пройдено, коли зʼїдено все. Чотири привиди переслідують його, але кожен цілиться в **свою клітину-ціль**: червоний — у Пекмена, рожевий — на 4 клітини попереду, блакитний — за вектором від червоного, помаранчевий — то женеться, то тікає в кут. Енерджайзер на кілька секунд перевертає ролі: привиди синіють, тікають, їх можна зʼїсти за зростаючі очки. Уся «хитрість» AI — три прості правила (ціль, жадібний вибір на перехресті, заборона розвороту) плюс розклад режимів scatter/chase.

## Поле і час
- Екран 28×36 клітин по 8 px; ігровий лабіринт 28×31, згори 3 рядки рахунку, знизу 2 — життя і фрукти рівня.
- Рух — по центральних лініях коридорів, логіка рахує **клітину**, у якій центр сутності. Привид приймає рішення на клітину наперед.
- Бічний тунель — тор по горизонталі: вихід праворуч → поява ліворуч. У тунелі привиди повільніші.
- Real-time 60 кадрів/с; швидкості — у відсотках від 100% = 75.76 px/с ≈ 9.5 клітини/с. Пекмен стоїть 1 кадр на кожній точці і 3 кадри на енерджайзері — привиди його наздоганяють, коли він їсть.
- Будиночок привидів у центрі (спавн); під ним — точка появи фрукта. Два «червоні» фрагменти коридору (над будиночком і над стартом Пекмена) — привиди там не повертають угору.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пекмен | player | 3 життя (DIP 1/2/3/5) | безперервний рух 4 напрямки; ввід змінює напрям; їсть точки |
| Точка | pickup | 240 шт., 10 очок | зникає при контакті |
| Енерджайзер | pickup | 4 шт. у кутах, 50 очок | вмикає frightened усіх привидів |
| Стіна | static | — | непрохідна для всіх |
| Двері будиночка | gate | — | прохідні лише привидам (вихід і повернення очей) |
| Тунель | terrain | 2 входи | `wrap` на протилежний край; привиди сповільнюються |
| Червона зона | terrain | 2 смуги | привид не повертає вгору (крім frightened) |
| Будиночок привидів | spawner | лічильники точок, таймер | випускає привидів за правилами; очі тут відроджуються |
| Blinky (червоний, Shadow) | enemy | стартує поза будиночком | chase: ціль = клітина Пекмена; Cruise Elroy — прискорюється |
| Pinky (рожевий, Speedy) | enemy | виходить одразу | chase: ціль = 4 клітини перед Пекменом (вгору — ще 4 ліворуч, баг) |
| Inky (блакитний, Bashful) | enemy | виходить після 30 точок (рівень 1) | chase: ціль = Blinky + 2·(точка 2 клітини перед Пекменом − Blinky) |
| Clyde (помаранчевий, Pokey) | enemy | виходить після 60 точок (рівень 1) | chase: якщо до Пекмена > 8 клітин — ціль Пекмен, інакше — свій кут |
| Синій привид | enemy (стан) | тривалість 6…0 с за рівнем; швидкість 50–60% | псевдовипадковий поворот; повільніший; зʼїдається |
| Очі привида | enemy (стан) | швидкі | ціль = двері будиночка; невразливі, нешкідливі |
| Фрукт / бонус-символ | pickup | 100…5000 очок, 9–10 с | зʼявляється після 70-ї і 170-ї точки під будиночком |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `contact(pacman, dot)` → ТО `pickup`, `score(10)`, `freeze(pacman, 1 frame)`.
- КОЛИ `contact(pacman, energizer)` → ТО `pickup`, `score(50)`, `set_state(ghosts, frightened, T(level))`, `face(ghosts, reverse)`, `custom: «лічильник зʼїдених привидів = 0»`.
- КОЛИ `contact(pacman, ghost)` → ЯКЩО `state(ghost, frightened)` → ТО `score(200·2^k)` (200→400→800→1600), `transform(eyes)`; інакше `lose` (мінус життя).
- КОЛИ `contact(eyes, house_door)` → ТО `respawn(ghost, house)` і вихід за звичайним правилом.
- КОЛИ `state_off(ghost, frightened)` → ТО повернення в поточний режим **без** розвороту; за ~2 с до кінця привид блимає білим.
- КОЛИ `schedule(scatter 7, chase 20, scatter 7, chase 20, scatter 5, chase 20, scatter 5, chase ∞)` (рівень 1; рівні 2–4: 7/20/7/20/5/1033/¹⁄₆₀/∞; з 5-го: 5/20/5/20/5/1037/¹⁄₆₀/∞) → ТО `set_state(ghosts, scatter|chase)`, `face(ghosts, reverse)`; таймер стоїть, поки триває frightened.
- КОЛИ `tick` і привид у центрі клітини перед перехрестям → ТО `custom: «з дозволених напрямків (не назад, не в стіну, не вгору в червоній зоні) обрати той, що дає найменшу евклідову відстань до цілі; нічия: вгору > ліворуч > вниз > праворуч»`.
- Цілі: scatter — `set_target(ghost, corner)` (клітина за межею поля, тому привид кружляє біля кута); chase — правила з таблиці сутностей; frightened — `custom: «випадковий дозволений напрям (PRNG з фіксованим seed, скидається на рівні і життя)»`.
- КОЛИ `enter(ghost, tunnel)` → ТО `speed(ghost, 40–50%)`; КОЛИ `edge(a)` → ТО `wrap(a)`.
- Вихід з дому: КОЛИ `counter(ghost_dots, >=, limit)` (Pinky 0; Inky 30/0; Clyde 60/50/0) → ТО привид виходить; КОЛИ `idle(4 с)` (Пекмен нічого не їв; з рівня 5 — 3 с) → ТО виходить наступний примусово.
- Після втрати життя: загальний лічильник замість особистих — КОЛИ `counter(global_dots, ==, 7|17)` → ТО випускає Pinky / Inky; КОЛИ `counter(global_dots, ==, 32)` → ЯКЩО `occupied(house, clyde)` → ТО загальний лічильник вимикається, знову діють особисті.
- КОЛИ `counter(dots_left, <=, elroy1)` (рівень 1: 20, далі до 120) → ТО `speed(blinky, +5%)`; `<= elroy2` (10…60) → ще +5%; Elroy в scatter теж цілиться в Пекмена.
- КОЛИ `counter(dots_eaten, ==, 70|170)` → ТО `spawn_at(fruit, below_house)`, `timer(9–10 с)` → `disappear_a`; КОЛИ `contact(pacman, fruit)` → ТО `score(fruit_value(level))`.
- КОЛИ `counter(score, >=, 10000)` → ТО `lives(+1)` (DIP: 10k/15k/20k/нема; «один раз» — (?)).
- КОЛИ `all_gone(dot+energizer)` → ТО `custom: «лабіринт блимає»`, `next_level`; після рівнів 2, 5, 9, 13, 17 (?) — `window(intermission)`.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Рівень 256: переповнення байта номера рівня псує праву половину екрана — 114+9 точок, рівень пройти неможливо (kill screen).
- Перемога: рекорд (нескінченні рівні, формально — до 256). Поразка: втрачено всі життя. Рахунок: 10 / 50 / 200–1600 / 100–5000; ідеальна гра — 3 333 360.

### Таблиця рівнів (Dossier, Table A.1, стисло)
| Рівні | Фрукт, очки | Пекмен | Привид | У тунелі | Frightened, с | Elroy1/2, точок |
|---|---|---|---|---|---|---|
| 1 | вишні 100 | 80% | 75% | 40% | 6 | 20/10 |
| 2 | полуниця 300 | 90% | 85% | 45% | 5 | 30/15 |
| 3–4 | персик 500 | 90% | 85% | 45% | 4, 3 | 40/20 |
| 5–6 | яблуко 700 | 100% | 95% | 50% | 2, 5 | 40/20, 50/25 |
| 7–8 | виноград 1000 | 100% | 95% | 50% | 2, 2 | 50/25 |
| 9–10 | Galaxian 2000 | 100% | 95% | 50% | 1, 5 | 60/30 |
| 11–12 | дзвоник 3000 | 100% | 95% | 50% | 2, 1 | 60/30, 80/40 |
| 13+ | ключ 5000 | 100% (21+: 90%) | 95% | 50% | 1,3,1,1,–,1,–… | 80/40 → 120/60 |
Frightened на 17-му і з 19-го — 0 с: енерджайзер лише розвертає привидів. Під час поїдання точок Пекмен повільніший (≈71/79/87/79% за стовпчиком «Пекмен»); у frightened Пекмен 90/95/100%, привиди 50/55/60% (рівні 1 / 2–4 / 5–20).

## Керування і ввід
- 4-позиційний джойстик: напрям задається наперед і виконується, щойно поворот стане можливим; без вводу Пекмен біжить, доки не впреться.
- **Cornering**: Пекмен може «зрізати» поворот за кілька пікселів до/після центру клітини (рух по діагоналі з подвійною швидкістю) — тому досвідчений гравець на поворотах відривається від привидів; привиди так не вміють.
- Кнопки 1P / 2P Start; два гравці — по черзі (hotseat), у кожного свій лабіринт зі станом точок.

## Вікна, меню, HUD
- `splash-screen` / атракт: «CHARACTER / NICKNAME» — привиди по одному з іменами, таблиця очок, потім демо-гра (`+window:attract-demo`).
- `game-screen` — лабіринт; згори `score` 1UP / 2UP і `hi-score`; знизу `lives` (іконки Пекмена) і `+ui:level-icons` (фрукти останніх 7 рівнів = номер рівня); текст «READY!» на старті і «GAME OVER» у кінці.
- `+window:intermission` — короткі комічні мультфільми з Пекменом і Blinky між рівнями (після 2, 5, 9, повтор після 13, 17 — (?)).
- `end-screen` фактично лише «GAME OVER» у лабіринті → атракт; таблиці ініціалів немає (лише один hi-score).
- Переходи: атракт → (монета, Start) → READY! → гра → (рівень) блимання → [intermission] → новий лабіринт → … → (0 життів) GAME OVER → атракт.

## Фічі поза полем
- `levels-sequential` без вибору; `progress-acceleration` — швидкості, Elroy-пороги й коротший frightened за таблицею.
- `hotseat` — 2 гравці по черзі; `+feature:operator-settings` (DIP): кількість життів, поріг extra life, ціна гри; перемичка на платі «hard» вилучає рівні 1, 3, 6, 19, 20 зі списку.
- Збереження нема; `score-records` — лише один hi-score до вимкнення автомата.

## Варіації й родичі
- **Ms. Pac-Man (1982):** 4 лабіринти, що змінюються за рівнями (1–2, 3–5, 6–9, 10–13, далі чергування); у трьох з них — **дві** пари тунелів; сповільнення привидів у тунелі лише перші 3 раунди; Blinky і Pinky перші секунди рівня рухаються випадково (scatter стає непередбачуваним); фрукт **в'їжджає** через тунель, підстрибує лабіринтом і виїжджає, з 8-го раунду — випадковий; Clyde → Sue; нові інтермісії.
- Pac-Man Plus, Super Pac-Man (ключі й двері), Pac-Man Championship Edition (поле поділено навпіл, точки поповнюються), Pac-Man 99 (battle royale), Lady Bug (турнікети), Mr. Do!, Jr. Pac-Man (лабіринт ширший за екран).
- **Осі варіацій:** ціль ворога (сама позиція / попереду / вектор / відстань-перемикач / кут / випадково); розклад режимів (фіксований / з випадковістю); лабіринт (один / ротація / генерований); фрукт (статичний / рухомий); тунелі (0 / 1 / 2 пари).

## Цікавинки для курсу
- Цільова клітина + жадібний вибір без розвороту: 4 різних «характери» з однієї функції `target(ghost)` — 🥈 (просто код, але треба зрозуміти поведінку і баг Pinky).
- Розклад scatter/chase з примусовим розворотом при зміні режиму і паузою під frightened — 🥉 (машина станів з таймером).
- Будиночок привидів: особисті лічильники точок + глобальний після смерті + таймер бездіяльності — 🥉.
- Frightened з подвоєнням очок 200→1600 і очима, що повертаються додому, — 🥉 (стан, зміна цілі, респавн).
- Cornering — буфер напрямку і зрізання повороту — 🥉 (відчуття керування, input buffering).
- Cruise Elroy: ворог прискорюється, коли лишається мало точок, — 📎.
- Таблиця рівнів як дані (швидкості, тривалості, фрукти) — 🌱 але дуже повчально для `state-as-data`.

## Мапа на каталог
- Є: `move-4dir` · `move-auto` (Пекмен біжить сам) · `impassable-cells` · `collect-all` (точки) · `item-pickup` · `touch-death` · `player-death` · `chase-player`/`chase-greedy` (вибір напрямку на перехресті) · `random-walk` (frightened без розвороту) · `temporary-modes` (енерджайзер) · `speed-per-type` · `spawn-points` (будиночок) · `respawn` (очі → дім) · `event-points` · `progress-acceleration` · `sequential-levels` · `status-panel` · `mode-indicator` (сині/блимають) · `score-records` · `game-screen` · `splash-screen` · `game-loop`.
- **Нема** → пропозиції карток:
  - `+target-tile-ai` «Ворог цілиться у клітину-ціль» · entities/move · 🥈 · слоти {target: player|ahead(n)|vector|distance-switch|corner} — 4 привиди.
  - `+scatter-chase-schedule` «Розклад режимів ворогів» · entities/state · 🥉 · слот {schedule: list} — з розворотом при зміні.
  - `+ghost-house-release` «Випуск з дому за лічильником» · entities/spawn · 🥉 · слоти {dot_limit, idle_timer}.
  - `+escalating-kill-points` «Очки за серію подвоюються» · game-logic/score · 📎 · слот {base, factor}.
  - `+eyes-return-home` «Зʼїдений ворог повертається на базу» · entities/death · 📎.
  - `+center-bonus-item` «Бонус у точці спавну після події» · entities/spawn · 🌱 (Lady Bug) — фрукт після 70/170 точок.
  - `+wrap-edges` «Тор по краях» · entities/move · 🌱 (Snake) — тунель.
  - `+speed-zones` «Зона змінює швидкість» · entities/state · 📎 — тунель.
  - `+no-turn-zone` «Зона заборони повороту» · entities/legality · 🌱 — червоні зони.
  - `+enrage-on-low-remaining` «Ворог лютішає під кінець рівня» · game-logic/waves · 📎 — Cruise Elroy.
  - `+cornering-assist` «Буфер напрямку і зрізання повороту» · entities/move · 🥉.
  - `+extra-life-threshold` «Додаткове життя за очки» · game-logic/score · 🌱 · слот {at, every?}.

## Пропозиції до словників
- `+trigger:counter` — кількість зʼїдених точок (вихід привидів, фрукт, Elroy).
- `+trigger:state_off` — кінець frightened (без розвороту, на відміну від зміни режиму).
- `+trigger:enter` — привид у тунелі / червоній зоні.
- `+cond:mode` — поточний глобальний режим scatter/chase; `+cond:in_range` — Clyde: відстань > 8.
- `+effect:set_state` (frightened, scatter/chase), `+effect:set_target` (нове: призначити ворогові клітину-ціль), `+effect:speed` (Elroy, тунель), `+effect:wrap` (тунель), `+effect:respawn` (очі вдома), `+effect:face` (примусовий розворот).
- `+role:spawner` — будиночок привидів; `+role:terrain` — тунель і червоні зони.
- `+ui:level-icons` — номер рівня показано іконками фруктів.
- `+window:intermission` — мультфільм між рівнями (Pengo); `+window:attract-demo` — атракт з представленням персонажів (Q*bert).
- `+feature:operator-settings` — DIP-налаштування автомата (Q*bert).

## Джерела
- ⭐ [The Pac-Man Dossier](https://pacman.holenet.info/) — усе про цілі, режими, будиночок, cornering, Table A.1 по рівнях, kill screen.
- [Dossier на Game Developer](https://www.gamedeveloper.com/design/the-pac-man-dossier) — та сама стаття з ілюстраціями цілей.
- [Wikipedia: Pac-Man](https://en.wikipedia.org/wiki/Pac-Man) — привиди і прізвиська, інтермісії, kill screen, 3 333 360.
- [Wikipedia: Ms. Pac-Man](https://en.wikipedia.org/wiki/Ms._Pac-Man) — розділ відмінностей: лабіринти, тунелі, фрукти, AI.
- [pacman.com — історія](https://pacman.com/en/history/) — офіційна сторінка Bandai Namco.
- [Museum of the Game: DIP Pac-Man](https://arcade-museum.com/dipswitch-settings/pac-man) — життя 1/2/3/5, бонус 10k/15k/20k/нема (дані спільноти, неверифіковані).
- YouTube: пошук «pac-man arcade ghost ai explained».

## Непевне
- (?) DIP-дані (життя 1/2/3/5, бонус 10k/15k/20k) — зі спільнотної таблиці; типове значення (3 життя, 10k) і «бонус лише один раз» — не перевірено.
- (?) Нумерація рівнів інтермісій (2, 5, 9, 13, 17) — ні Dossier, ні Wikipedia її не дають.
