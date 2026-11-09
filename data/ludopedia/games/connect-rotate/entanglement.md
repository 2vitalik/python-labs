---
title: Entanglement
slug: entanglement
aka: []
family: connect-rotate
also: [board-digital]
klass: cursor
axes:
  field: hex
  time: turn
  opponent: none
  info: partial
  random: runtime
  goal: score
year: 2010
platforms: [web, PC (Steam), Mac, Linux, board]
links:
  - {kind: other, url: "https://njohnston.ca/2011/01/the-maximum-score-in-the-game-entanglement-is-9080/", best: true, note: "точні правила: 12 кінців на плитці, поле з 36 гексів, стіни, рахунок трикутними числами, максимум 9080"}
  - {kind: steam, url: "https://store.steampowered.com/app/719140", note: "Steam 2017: соло з таблицями рекордів, hot-seat до 6, щоденна задача"}
  - {kind: other, url: "https://blog.gopherwoodstudios.com/2017/10/", note: "блог розробника: 12 мап, Sakura-плитки, настільна версія 72 плитки"}
  - {kind: other, url: "https://divisbyzero.com/2010/08/24/a-game-for-budding-knot-theorists/", note: "2010: правила, рахунок у сегментах (максимум 169), вузлові питання"}
  - {kind: play, url: "https://entanglement.gopherwoodstudios.com/", note: "веб-версія"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Entanglement+Gopherwood+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [tile-rotate, pipe-connectors, movement-animation, event-points, score-records, leaderboard, daily-puzzle, hot-seat, turn-enforcement, next-queue, pocket, game-screen, main-menu, end-screen, mode-select, map-window, +path-follow, +auto-extend-path, +triangular-move-score, +wall-ends-game, +bonus-tile-cells, +hex-12-port-tile, +tile-catalog-enumeration]
proposes: ["+effect:follow_path", "+effect:swap_reserve", "+trigger:path_end", "+card:auto-extend-path", "+card:triangular-move-score", "+card:hex-12-port-tile", "+card:bonus-tile-cells"]
author: opus
date: 2026-11-09
---

# Entanglement — поверни гекс-плитку біля кінця свого шляху, і шлях сам протече через усі вже покладені плитки

## Суть
Є одна лінія, що виходить із центрального гекса. Гравцеві дають плитку з шістьма відрізками-мотузками; він лише обертає її, а кладеться вона завжди в клітину, куди впирається кінець шляху. Шлях одразу йде новою плиткою і далі всіма плитками, які вже зʼєднуються, тож один хід може подовжити лінію на десятки відрізків. Гра закінчується, коли шлях упирається в стіну (край поля або центр); рахунок нагороджує саме довгі стрибки за один хід.

## Поле і час
- Класична мапа: гекс-поле радіуса 3 — кільця з 6, 12, 18 клітин навколо центру = 36 клітин; центр — стартова плитка-стіна.
- На кожному боці гекса 2 кінці → 12 кінців на плитку, 6 відрізків; на повному полі 216 відрізків.
- До центра виходить 12 кінців, до зовнішнього краю — 84; обидва — стіни.
- Покроково: хід = обертання → підтвердження → проходження шляху. Таймера нема.
- Інші мапи (Steam: 12 штук — Classic, Sakura Grove, Honeycomb, Raceway…): інші форми поля, Sakura-клітини дають додаткові плитки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Поточна плитка | tile | 6 відрізків між 12 кінцями; 6 поворотів | стоїть у клітині біля кінця шляху; обертається до підтвердження |
| Запасна плитка | supply | 1 шт. | можна обміняти з поточною (?) |
| Покладена плитка | conduit | фіксований поворот | шлях іде нею, якщо дійшов до її кінця |
| Шлях гравця | player | довжина в сегментах | подовжується сам, доки наступна клітина зайнята плиткою |
| Центральний гекс | static | 12 кінців | старт шляху; повернення в нього = кінець гри |
| Край поля | hazard | 84 кінці (класична мапа) | вихід шляху сюди = кінець гри |
| Sakura-клітина | pickup | — | провести шлях через неї — дати гравцеві додаткові плитки |
| Колода | supply | випадкові плитки; 1799 різних типів за поворотом | рідше трапляються симетричні плитки |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт: шлях виходить з одного кінця центрального гекса в першу клітину кільця 1; туди ставиться перша плитка.
- КОЛИ `input(rotate)` → ТО `rotate(tile, 60)`.
- КОЛИ `input(swap)` → ТО `custom: «поточна плитка ↔ запасна»` (+effect:swap_reserve, ?).
- КОЛИ `input(place)` → ТО `place(tile, cell_at_path_end)` — місце не обирається, лише поворот.
- КОЛИ `after(place)` → ТО `custom: «шлях іде відрізком плитки до іншого кінця, далі в сусідню клітину, доки там є плитка»` (+effect:follow_path).
- КОЛИ `custom: «шлях дійшов до порожньої клітини»` (+trigger:path_end) → ТО `custom: «наступна плитка зʼявляється в цій клітині»`, хід закінчено.
- КОЛИ `after(follow_path)` → ЯКЩО `counter(step_len, ==, n)` → ТО `score(1+2+…+n)` — трикутне число за довжину ходу.
- КОЛИ `edge(path)` або `contact(path, center)` → ТО `game_over`; бали за останній хід нараховуються.
- КОЛИ `enter(path, sakura)` → ТО `give(player, tiles)` (мапи Sakura).
- КОЛИ `custom: «плитки скінчились»` (Sakura-мапи) → ТО `game_over`.
- Hot-seat: КОЛИ `turn_end(p)` → ТО `pass_turn`; кожен веде свій шлях; КОЛИ `contact(path_p, wall | path_q)` → ТО `custom: «гравець вибуває»`.
- Перемога: рекорд / найдовший шлях у hot-seat · Поразка: шлях у стіну · Рахунок: Σ трикутних чисел ходів (до листопада 2010 — довжина в сегментах).

## Керування і ввід
- Веб/ПК: клік або стрілки — повернути плитку на 60°; клік/пробіл — покласти (?); клік по запасній — обмін (?).
- Перед підтвердженням видно, куди піде шлях у межах поточної плитки (підсвітка відрізка, ?).
- Hot-seat: гравці ходять по черзі за одним компʼютером.

## Вікна, меню, HUD
- `main-menu`: Solitaire, Multiplayer (hot-seat до 6), Daily Challenge, вибір мапи.
- `map-window` / `mode-select`: 12 мап у Steam-версії.
- `game-screen`: гекс-поле, поточна плитка біля кінця шляху, `pocket` — запасна плитка (?), `score`, очки останнього ходу, `popup-text`.
- `leaderboard`: денні, тижневі й загальні рекорди.
- `end-screen`: підсумок, довжина шляху, місце в таблиці.
- Переходи: main-menu → вибір мапи → game-screen → end-screen → main-menu.

## Фічі поза полем
- `mode-daily`: однаковий набір плиток для всіх у день.
- `leaderboard-online`: денні, тижневі, усі часи.
- `hotseat` до 6 гравців.
- 12 мап; Sakura-мапи з добором плиток.
- `localization` — 25 мов у Steam.
- Настільна версія 2017 (The Game Crafter): 72 плитки (1 старт, 6 Sakura, 65 шляхових), 6 жетонів; Sakura-плитки роздаються в руку; рахунок — сумарна довжина завершених ліній.

## Варіації й родичі
- Родичі: [tsuro](tsuro.md) (шлях везе фішку, виліт = смерть), [trax](trax.md), [tantrix](tantrix.md), Kaliko / Psyche-Paths, KnoTiles.
- Відміна від Tsuro: одна лінія замість фішки, а клітина ходу задана — вибір лише в повороті (і обміні).
- Осі варіацій: **плитка: 8 кінців (квадрат) / 12 кінців (гекс)** · **місце ходу: задане кінцем шляху / будь-де** · **рахунок: довжина / трикутне число за хід** · **поле: обмежене стінами / з бонус-клітинами**.

## Цікавинки для курсу
- Модель плитки: 12 кінців, перестановка-парування; поворот = зсув на 2 за mod 12 — 🌱.
- Проходження шляху через ланцюг плиток із виходом у сусідню клітину (координати гекса + відповідний кінець сусіда) — 🥉.
- Рахунок трикутними числами: стратегічна напруга «довгий ход зараз чи потім» — 🌱.
- Підрахунок різних плиток (Burnside: 10395 парувань / 6 поворотів → 1799) — 🥈.
- Доведення максимуму 9080 (парність кінців біля стін) — 👑 як дослідницьке завдання.
- AI: жадібний вибір повороту за найдовшим ходом без стіни — 📎.

## Мапа на каталог
- Є: `tile-rotate` · `pipe-connectors` (12 портів) · `movement-animation` (проходження шляху) · `event-points` · `score-records` · `leaderboard` · `daily-puzzle` · `hot-seat` · `turn-enforcement` · `next-queue` / `pocket` (запасна плитка) · `game-screen` · `main-menu` · `end-screen` · `mode-select` · `map-window`.
- **Нема** → пропозиції карток:
  - `+path-follow` «Рух по шляхах плиток до обриву» (є як пропозиція з Tsuro) · entities/move · 🥉.
  - `+auto-extend-path` «Шлях подовжується сам через уже покладені плитки» · entities/move · 🥉.
  - `+triangular-move-score` «Очки 1+2+…+n за довжину ходу» · game-logic/score · 🌱.
  - `+wall-ends-game` «Шлях у стіну = кінець гри» · game-logic/lose · 🌱.
  - `+bonus-tile-cells` «Клітини, що дають додаткові плитки» · game-logic/economy · 🌱.
  - `+hex-12-port-tile` «Гекс-плитка з 12 портами» · entities/state · 🌱.
  - `+tile-catalog-enumeration` «Генерація всіх унікальних плиток» · levels/generation · 🥈.

## Пропозиції до словників
- `+effect:follow_path(a)` — сутність/лінія йде шляхами плиток до обриву (друга гра після Tsuro).
- `+effect:swap_reserve` — обміняти поточну плитку із запасною.
- `+trigger:path_end` — шлях зупинився в порожній клітині (кінець ходу).

## Джерела
- ⭐ [N. Johnston: The Maximum Score in Entanglement is 9080](https://njohnston.ca/2011/01/the-maximum-score-in-the-game-entanglement-is-9080/) — правила, будова поля, кінці біля стін, трикутний рахунок із листопада 2010, кількість типів плиток.
- [Steam: Entanglement](https://store.steampowered.com/app/719140) — режими, hot-seat до 6, daily, таблиці рекордів, 2017.
- [Gopherwood blog, жовтень 2017](https://blog.gopherwoodstudios.com/2017/10/) — 12 мап, Sakura, настільна версія.
- [Division by Zero, 2010](https://divisbyzero.com/2010/08/24/a-game-for-budding-knot-theorists/) — правила, ранній рахунок у сегментах (максимум 169).

## Непевне
- (?) Запасна плитка й обмін (swap) — за памʼяттю; жодне відкрите джерело не підтвердило.
- (?) Точне керування (клавіші, кліки) і підсвітка шляху перед підтвердженням — не бачив.
- (?) Рік 2010 — за датою статті Division by Zero; точна дата запуску веб-версії не звірена.
- (?) Hot-seat: як саме вибувають гравці при зіткненні шляхів — Steam каже лише «не врізатися одне в одного чи в стіну».
- (?) Коли закінчується гра на Sakura-мапах — за логікою обмеженого запасу плиток.
