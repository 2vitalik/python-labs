---
title: Tinkle Pit (ティンクルピット)
slug: tinkle-pit
aka: [ティンクルピット, Тінкл Піт]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 1994
platforms: [arcade (Namco NA-1), Switch / PS4 (Arcade Archives, 2024)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tinkle_Pit", best: true, note: "Tinker Ball і лінія, popcorn, останній ворог тікає з «Bye-bye!», 8 світів, камео Namco"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ティンクルピット", note: "повний довідник: 4 типи погоні, вороги, Hurry Up, Dark Prince, бонус-мішені, предмети, приховані персонажі, 48 GAME"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tinkle+Pit+Namco", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, touch-death, player-death, destroy-all-enemies, sequential-levels, chase-player, chase-greedy, temporary-modes, in-round-upgrades, item-pickup, hp-damage, projectile-shot, event-points, escalating-kill-points, extra-life-threshold, timeout-punisher, score-records, leaderboard, hot-seat, +tether-line-sweep, +line-cutter-enemy, +flee-player, +flee-last-enemy, +enrage-on-low-remaining, +ghost-phase, +ricochet-shot, +smart-bomb, +multi-kill-bonus, +target-chain-bonus, +hidden-bonus-character, +item-unlock-meter, +boss-fight]
proposes: ["+card:tether-line-sweep", "+card:line-cutter-enemy", "+card:target-chain-bonus", "+card:hidden-bonus-character", "+card:item-unlock-meter", "+effect:recall", "+effect:throw"]
author: opus
date: 2026-11-09
---

# Tinkle Pit — поклади кульку-дзвіночок, протягни від неї лінію лабіринтом і відпусти: кулька летить назад і змітає ворогів

## Суть
Лабіринтна аркада Namco (1994): Пітт/Патті бігає коридорами, вороги переслідують. Головна зброя — **Tinker Ball**: кнопка кладе кульку на місце героя, утримання кнопки під час руху тягне за героєм лінію від кульки, а відпускання змушує кульку пролетіти назад уздовж усієї лінії й убити кожного ворога на ній. Тобто атака — це **шлях, який ти щойно пробіг**: заманити ворогів на свій слід і «закрити пастку». Раунд — знищити всіх ворогів; довкола ядра — бонус-мішені, що змінюють вартість, предмети-камео з інших ігор Namco і анти-кемпінговий невразливий Dark Prince.

## Поле і час
- Один екран-лабіринт з коридорами й перехрестями (вороги ухвалюють рішення на перехрестях); лінія міряється «символами» — тайлами (Spark відкладається, якщо лінія ≤ 4 символів).
- Real-time; таймінги в джерелі — у кадрах (оглушення 38/60 і 46/60 с).
- 48 GAME (етапів), згрупованих у 8 світів по 4–6; GAME 23 — середній бос, GAME 48 — фінальний бос Mao.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пітт / Патті | player | життя, швидкість | 4 напрямки; кладе кульку, тягне лінію, кидає popcorn |
| Tinker Ball (дзвіночок) | object | швидкість (апгрейд ×2) | лежить, де поклали; невразлива для ворогів; летить назад по лінії й убиває |
| Лінія | zone | довжина в тайлах | слід героя від кульки; шлях польоту кульки |
| Popcorn | projectile | 15 с | кидок; відбивається від стін до влучання; промах — зникає |
| Soldier | enemy | тип A, повільний | без атак |
| Puka | enemy | тип A | періодично прискорюється, потім стає формою, що проходить крізь стіни |
| Вогнедишний | enemy | тип B | зупиняється й дихає вогнем — випадково або в гравця |
| Tinbot | enemy | тип C | лазер крізь стіни; відскакує, якщо кулька стартує, коли гравець на його лінії |
| Popper / Parchik | enemy | тип A | кидає бомби: 3 відскоки й вибух; вибух смертельний |
| Poppy Knight | enemy | тип B, броня | 2 влучання (спецпредметом — 1) |
| Clipper | enemy | тип A | пройшовши певну відстань, перерізає лінію; герой оглушений 38/60 с і мусить знову підібрати кульку |
| Stinger | enemy | тип D | промінь-стріли у 4 напрямки; влучання — оглушення 46/60 с без втрати життя |
| Pot | spawner | тип A | випускає паразитів (?) |
| Паразит | enemy | — | чіпляється до покладеної кульки й сповільнює її; пробіг кульки зменшує їх; до прилипання — розчавити за 10 очок |
| Spark | hazard | кожні 45 с часу з лінією | зʼявляється на місці кульки; виклик кульки знищує |
| Dark Prince | enemy | невразливий | анти-кемпінг: на 45-й с етапу (GAME 47 — 60-й), крізь стіни, прискорюється; нема в бос-етапах; скидається після смерті героя |
| Бонус-мішень велика / мала | pickup | 1500 / 500 | до 8 на етап; див. правила ланцюга |
| Предмети (Speed Up, Ball Speed Up, Line Power-Up…) | pickup | — | див. правила |
| Прихований персонаж | pickup | 16 с | зʼявляється, якщо перетнути певну зону у вікні 4–24 с |
| Бос (NAKA-G1, Mao) | boss | — | GAME 23 і 48 |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`.
- КОЛИ `input(A)` → ЯКЩО `has(player, ball)` → ТО `place(player, ball)` (на клітину героя).
- КОЛИ `input(hold_A + dir)` → ТО `move(player, dir)`, `custom: «лінія від кульки подовжується за героєм»`.
- КОЛИ `input(release_A)` → ТО `custom: «кулька летить уздовж лінії назад до героя»` (`+effect:recall`).
- КОЛИ `contact(ball, enemy)` → ЯКЩО `custom: «кулька летить»` → ТО `disappear_b`, `counter(kill_points, +k)` (за одним пробігом k = 1, 2, 3…).
- КОЛИ `contact(enemy, ball)` → ЯКЩО `custom: «кулька лежить»` → ТО `block` — кулька невразлива.
- КОЛИ `contact(enemy, player)` → ТО `lives(-1)`; Dark Prince скидається.
- КОЛИ `input(B)` → ЯКЩО `has(player, popcorn)` → ТО `throw(popcorn)`; КОЛИ `blocked(popcorn)` → ТО `bounce(popcorn)`; КОЛИ `contact(popcorn, enemy)` → ТО `disappear_both`.
- Clipper: КОЛИ `counter(clipper_walk, >=, d)` → ТО `custom: «лінію перерізано»`, `stun(player, 38/60 s)`.
- Stinger: КОЛИ `contact(arrow, player)` → ТО `stun(player, 46/60 s)` (без втрати життя).
- Popper: КОЛИ `counter(bomb_bounces, ==, 3)` → ТО `explode(area)`; КОЛИ `contact(blast, player)` → ТО `lives(-1)`.
- Poppy Knight: КОЛИ `contact(ball, knight)` → ТО `damage(1)`; КОЛИ `hp_zero(knight)` → ТО `disappear_a`.
- Tinbot: КОЛИ `line_of_sight(tinbot, player)` → ТО `custom: «лазер крізь стіни»`; ЯКЩО `custom: «кулька стартує»` → ТО `custom: «Tinbot відскакує»`.
- Паразит: КОЛИ `contact(parasite, ball)` → ЯКЩО `custom: «кулька лежить»` → ТО `attach(parasite, ball)`, `speed(ball, -1)`; КОЛИ `contact(player, parasite)` → ЯКЩО `custom: «ще не прилип»` → ТО `disappear_b`, `score(+10)`.
- Spark: КОЛИ `counter(line_time, >=, 45 s)` → ТО `spawn_at(spark, ball)`; ЯКЩО лінія ≤ 4 тайлів — відкласти; КОЛИ `custom: «кульку викликано»` → ТО `disappear(spark)`.
- Dark Prince: КОЛИ `timer(45 s)` → ЯКЩО `custom: «не бос-етап»` → ТО `spawn(dark_prince)`; рухається крізь стіни, `speed(dark_prince, +n)`.
- Hurry Up: КОЛИ `counter(enemies_left, <=, threshold)` (поріг 1–5 за етапом) → ТО `sound(fast_music)`, `speed(enemies, +n)`; тип D → тип A.
- КОЛИ `counter(enemies_left, ==, 1)` → ТО `custom: «через 4 с останній ворог тікає на першому перехресті з "Bye-bye!"»`, `custom: «зменшує Pursuit Bonus»`.
- КОЛИ `all_gone(enemy)` → ТО `next_level`.
- Мішені: КОЛИ `level_start` → ТО `spawn(large ×2, small ×1)`; КОЛИ `picked(player, large)` → ТО `score(+1500)`, `transform(all_small, large)`, `spawn(small)`; КОЛИ `picked(player, small)` → ТО `score(+500)`, `spawn(small)`; КОЛИ `counter(large_picked, ==, 8)` → ТО `custom: «Perfect Bonus 20 000 після етапу»`. Порядок мішеней залежить від напрямку першого підбору.
- Предмети: КОЛИ `counter(sp_points, >=, 150)` → ТО `custom: «у наступному раунді зʼявиться спецпредмет»` (через 3 с, якщо попередній раунд пройдено за 25 с, інакше — через 8 с). Очки: вбивство 1 (мультикіл 1, 2, 3…), мала мішень 1, велика 2.
- КОЛИ `picked(player, speed_up|ball_speed_up|line_power)` → ТО `speed(player|ball, +1)` / `custom: «лінія дає ударну хвилю: stun(enemy, ~3 s)»`.
- КОЛИ `picked(player, pac_attack)` → ТО `set_state(player, pac_man, dur)`; КОЛИ `contact(player, enemy)` → ЯКЩО `state(player, pac_man)` → ТО `disappear_b`, `score(+escalating)`.
- КОЛИ `picked(player, holy_halation|penguin_blizzard)` → ТО `clear(all_enemies)`, `custom: «поки діє — нових ворогів нема»`.
- КОЛИ `picked(player, dig_dug_rock)` → ТО `custom: «падають камені, чавлять ворогів»`, `set_state(player, invulnerable)`.
- КОЛИ `custom: «усіх стартових ворогів убито одночасно»` → ТО `spawn(bonus_flag)` (10 000, зростає до 100 000 за серію раундів).
- КОЛИ `counter(score, >=, 500 000|1 000 000)` → ТО `spawn(special_flag)`; КОЛИ `picked(player, special_flag)` → ТО `lives(+1)` (у грі вдвох рахується сума).
- Прихований персонаж: КОЛИ `reach(player, zone_from_score_digits)` → ЯКЩО `timer(>=, 4 s)` і `timer(<=, 24 s)` → ТО `spawn(hidden_char, 16 s)`.
- Перемога: пройти 48 GAME і перемогти Mao · Поразка: втрачено всі життя · Рахунок: вбивства, мішені, Perfect 20 000, Bonus Flag, Pursuit Bonus, предмети; топ-10 з фруктовою позначкою за «перфекти» світу.

## Керування і ввід
- 4-напрямний важіль — рух.
- A — покласти кульку; утримувати A під час руху — тягнути лінію; відпустити A — кулька летить назад.
- B — кинути popcorn (коли підібрано).
- Прихований ввід: двічі Start з утриманням «вгору», поки показано предмет, — прибрати предмет за 20 000 очок.
- 1–2 гравці по черзі.

## Вікна, меню, HUD
- `attract-demo` (?) — аркадний демо-цикл.
- `game-screen` — лабіринт; HUD — `score`, `hi-score`, `lives` (іконка життя підскакує, коли відкрито вікно прихованого персонажа), `level-number` (GAME) (?).
- `end-screen` етапу — бонуси (Perfect, Pursuit Bonus) (?).
- `leaderboard` — топ-10 з введенням імені; фрукт-позначка за перфекти світу; на екрані вводу зʼявляється Ms. Pac-Man (вигляд — від суми цифр рахунку; у порті Arcade Archives замінено на Pac-Man).
- Переходи: attract → (монета) GAME 1 → … → бос → кінцівка / game over → введення імені.

## Фічі поза полем
- `levels-sequential` — 48 GAME у 8 світах із босами.
- `hotseat` — двоє по черзі; Special Flag рахує спільний рахунок.
- `collectibles` — приховані персонажі (по одному на етап, переносяться, якщо пропущені); камео: флагман Galaxian, Pac-Man, Special Flag з Rally-X, Solvalou з Xevious, Mappy.
- `leaderboard-local` — топ-10 з позначками.
- Порт Arcade Archives (Hamster, 2024) — Switch і PS4.

## Варіації й родичі
- Лабіринтні аркади Namco: `pac-man`, `rally-x`, Mappy (камео; див. `hopping-mappy`); пастка-слідом — родич `xonix` / `gals-panic` (замкнути область), але тут убиває не площа, а шлях кульки.
- `heiankyo-alien`, `lady-bug` — інші способи «зброї з лабіринту» (ями, двері).
- **Осі варіацій:** зброя — постріл / яма / **слід, по якому повертається снаряд** · хто перериває — ніхто / ворог-ножиці (Clipper) · анти-кемпінг — прискорення / невразливий переслідувач (Dark Prince) / кінець часу.

## Цікавинки для курсу
- Лінія-повідець: слід героя від кульки як список клітин; відпускання — кулька проходить список назад і вбиває всіх на ньому — 🥉.
- Чотири типи переслідування: вирівнювати бульшу відстань по осі / меншу / жадібно наближатись / тікати (стає A при Hurry Up) — 📎 (чудова вправа на AI в лабіринті).
- Clipper перерізає лінію й оглушує — 📎.
- Ланцюг бонус-мішеней: велика перетворює всі малі на великі, порядок залежить від напрямку першого підбору — 🥉.
- Hurry Up + останній ворог тікає + Dark Prince — три механізми проти затягування — 📎.
- Лічильник 150 «спецочок» за вбивства й мішені відкриває предмет наступного раунду — 🌱.
- Прихований персонаж: зона виводиться з цифр рахунку на старті, вікно 4–24 с — 📎.

## Мапа на каталог
- Є: `move-4dir` · `touch-death`, `player-death` · `destroy-all-enemies` ↔ раунд · `sequential-levels` ↔ 48 GAME · `chase-player`, `chase-greedy` ↔ типи A–C · `temporary-modes` ↔ Pac Attack · `in-round-upgrades` ↔ Speed / Ball Speed / Line Power · `item-pickup` · `hp-damage` ↔ Poppy Knight · `projectile-shot` ↔ popcorn, лазер, стріли · `event-points` · `escalating-kill-points` ↔ Pac Attack · `extra-life-threshold` ↔ Special Flag · `timeout-punisher` ↔ Dark Prince · `score-records`, `leaderboard` · `hot-seat` ↔ двоє по черзі.
- **Нема** → пропозиції карток:
  - `+tether-line-sweep` «Слід від покладеного снаряда; відпустив — снаряд повертається слідом і бʼє все на ньому» · entities/combat · 🥉.
  - `+line-cutter-enemy` «Ворог перерізає слід/лінію гравця» · entities/interact · 📎.
  - `+target-chain-bonus` «Бонус-мішені змінюють вартість і множаться від підбору» · game-logic/score · 🥉.
  - `+hidden-bonus-character` «Секретний бонус: зона й часове вікно» · game-logic/score · 📎.
  - `+item-unlock-meter` «Лічильник спецочок відкриває предмет у наступному раунді» · game-logic/economy · 🌱.
  - З корпусу: `+flee-player`, `+flee-last-enemy` (`dig-dug`), `+enrage-on-low-remaining` (`pac-man`), `+ghost-phase` (Puka), `+ricochet-shot` (popcorn), `+smart-bomb` (очищення екрана), `+multi-kill-bonus`, `+boss-fight`.

## Пропозиції до словників
- `+card:tether-line-sweep`, `+card:line-cutter-enemy`, `+card:target-chain-bonus`, `+card:hidden-bonus-character`, `+card:item-unlock-meter` — див. вище.
- `+effect:recall` — повернути покладений обʼєкт до власника його шляхом (кулька, бумеранг).
- `+effect:throw` — підтримую наявну пропозицію (`bomberman`): кинути popcorn.

## Джерела
- ⭐ [Wikipedia: Tinkle Pit](https://en.wikipedia.org/wiki/Tinkle_Pit) — Tinker Ball невразлива, кнопки Line і Popcorn, останній ворог «Bye-bye!» і Pursuit Bonus, 8 світів (4 + 7×6), Mao, камео, Arcade Archives.
- [Wikipedia JA: ティンクルピット](https://ja.wikipedia.org/wiki/ティンクルピット) — керування (важіль, A/B), типи погоні A–D, вороги з таймінгами, Spark, Dark Prince, Hurry Up, бонус-мішені й Perfect, предмети й умова їх появи, приховані персонажі, 48 GAME, плата NA-1.

## Непевне
- (?) Скільки кульок у героя (EN-вікі — «Tinker Balls», множина; JA — одна кулька) і чи кулька зникає з поля після повернення.
- (?) Розмір лабіринту в тайлах; чи рух строго клітинний (опис «символів» лінії і перехресть каже «так»).
- (?) Кількість життів, пороги додаткових життів крім Special Flag, чи є continue.
- (?) Що робить Pot (спавнер паразитів — з назви «Pot & Parasite»).
- (?) Popcorn: JA — зникає через 15 с, EN — «до кінця етапу».
- (?) Вміст екрана бонусів між етапами і величина Pursuit Bonus.
