---
title: Space Invaders (Космічні загарбники)
slug: space-invaders
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: survive
year: 1978
platforms: [arcade, Atari 2600, PC, mobile, web]
links:
  - {kind: official, url: "https://www.computerarcheology.com/Arcade/SpaceInvaders/", best: true, note: "розбір коду: рух строю, типи бомб, таблиця НЛО, висоти хвиль"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Space_Invaders", note: "правила, прискорення як апаратний ефект, історія"}
  - {kind: official, url: "https://www.computerarcheology.com/Arcade/SpaceInvaders/Code.html", note: "дизасемблер з коментарями"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=space+invaders+1978+arcade+gameplay", note: "пошук; геймплей оригіналу"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=space+invaders", note: "пошук; перевидання"}
stage: v1
coverage: 70
mechanics: [move-by-input, projectile-shot, shoot-forward, projectile-collision, enemy-waves, destroy-all-enemies, enemy-reached-base, player-death, event-points, progress-acceleration, score-records, status-panel, hot-seat, game-screen, splash-screen, game-loop, +swarm-formation, +descend-and-reverse, +speed-by-remaining, +erodible-shield, +bottom-shooter-only, +mystery-bonus-ship, +one-shot-on-screen, +wave-start-lower, +extra-life-threshold]
proposes: ["+trigger:edge", "+trigger:all_gone", "+trigger:reach", "+trigger:counter", "+effect:shift", "+effect:speed", "+effect:erode", "+effect:spawn_at", "+effect:lives", "+cond:count", "+role:projectile", "+window:attract-demo", "+feature:operator-settings", "+axis:actors"]
author: opus
date: 2026-11-02
---

# Space Invaders — збий строй прибульців, що крокує вниз, поки він не дійшов до землі

## Суть
Гравець водить гармату по нижньому краю екрана і стріляє вгору одним пострілом за раз. Згори — строй 5×11 прибульців, що рухається як одне ціле: крок убік, біля краю — крок униз і розворот. Чим менше прибульців лишилось, тим швидше крокує строй (апаратний ефект, залишений як фіча). Чотири укриття поступово руйнуються від пострілів з обох боків; прибульці кидають бомби трьох типів; угорі іноді пролітає НЛО за таємні очки.

## Поле і час
- Екран 224×256 px (монітор повернуто вертикально); строй — **сітка 5×11**, кожен прибулець у своїй комірці, але весь строй зсувається піксельно.
- Рух строю: опорний прибулець (лівий нижній) зсувається на 2 px; за один кадр-переривання перемальовується **один** прибулець — строй «перебирає» хвилею, повний цикл при 55 прибульцях ≈ 1 с. Біля краю — розворот і −8 px униз.
- Час — кадри 60 Гц; бомби падають на 4 px кожні 3 кадри (5 px, коли прибульців ≤ 8).
- Шари: зелена лінія землі, гармата, 4 укриття (піксельні бітмапи), строй, смуга НЛО згори.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гармата (laser base) | player | 3 життя (DIP 3–6) | рух ліворуч/праворуч, 1 постріл на екрані |
| Постріл гравця | projectile | — | летить угору; знищує прибульця, НЛО, бомбу або шматок укриття |
| Кальмар (верхній ряд) | enemy | 30 очок | у строю |
| Краб (2 ряди) | enemy | 20 очок | у строю |
| Восьминіг (2 нижні ряди) | enemy | 10 очок | у строю |
| Строй | enemy (група) | 55 → 1 | крок 2 px, край → вниз 8 px і розворот; швидшає з втратами |
| Бомба «rolling» | projectile | 1 на екрані | падає над колоною гравця (прицільна) |
| Бомба «plunger» | projectile | 1 на екрані | колона з фіксованої таблиці; вимкнена, коли лишився 1 прибулець |
| Бомба «squiggly» | projectile | 1 на екрані | колона з таблиці; ділить слот з НЛО |
| НЛО (mystery ship) | enemy | 50–300 очок | пролітає верхом, якщо прибульців ≥ 8; напрям — від парності пострілів |
| Укриття (shield) | object | 4 шт. | руйнується піксельно від пострілів, бомб і дотику строю |
| Земля | static | — | лінія під гарматою; бомба вибухає на ній |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(fire)` → ЯКЩО `count(player_shot, ==, 0)` → ТО `spawn(player_shot)`; інакше нічого.
- КОЛИ `contact(player_shot, invader)` → ТО `disappear_both`, `score(10|20|30)`, `speed(formation, ↑)` (менше прибульців — швидший цикл).
- КОЛИ `tick` → ТО `shift(formation, dir, 2px)`; КОЛИ `edge(formation)` → ТО `shift(formation, down, 8px)`, `face(formation, reverse)`.
- КОЛИ `count(invaders, ==, 1)` → ТО `custom: «останній іде 2 px ліворуч і 3 px праворуч»`, plunger вимкнено.
- КОЛИ `timer(reload(score))` → ТО `spawn_at(bomb, нижній прибулець колони)`: rolling — над гравцем, plunger/squiggly — колона з таблиці; кожного типу не більше 1. Перезарядка коротшає з ростом рахунку (0x30 → 7 кадрів).
- КОЛИ `contact(bomb, player)` → ТО `lose` (мінус життя), строй стоїть на час вибуху.
- КОЛИ `contact(player_shot, bomb)` → ТО `disappear_both` (?) — постріли можуть збивати бомби.
- КОЛИ `contact(shot|bomb, shield)` → ТО `custom: «вирізати шматок бітмапи укриття у формі вибуху»` (`+effect:erode`), `disappear_a`.
- КОЛИ `contact(formation, shield)` → ТО `erode(shield)` — низький строй «зʼїдає» укриття.
- КОЛИ `timer(600 циклів)` → ЯКЩО `count(invaders, >=, 8)` → ТО `spawn_at(ufo, top_edge)` з боку, що залежить від парності кількості пострілів.
- КОЛИ `contact(player_shot, ufo)` → ТО `score(table[shots mod 15])` (100, 50, 50, 100, 150, 100, 100, 50, 300, …): 23-й постріл, далі кожен 15-й — 300.
- КОЛИ `reach(formation, ground_row)` → ТО `game_over` незалежно від кількості життів (вторгнення).
- КОЛИ `all_gone(invaders)` → ТО `spawn(formation)` на висоті з таблиці хвиль (кожна нижча, цикл після 9-ї).
- КОЛИ `counter(score, >=, 1500)` → ТО `lives(+1)` один раз (DIP: 1000) (?).
- Перемога: нема (нескінченні хвилі, рекорд). Поразка: 0 життів або строй дійшов донизу. Рахунок: 10/20/30 за прибульця, 50–300 за НЛО.

## Керування і ввід
- Ліворуч / праворуч (кнопки або 2-позиційний джойстик) і кнопка Fire; кнопки 1P/2P Start.
- Одночасно лише один постріл гравця: промах = довга пауза. Звідси тактика «стріляти з-під укриття» (руйнує його знизу) і рахувати постріли для НЛО на 300.
- Два гравці — по черзі, у кожного свій стан строю і укриттів.

## Вікна, меню, HUD
- `splash-screen` / атракт: «PLAY SPACE INVADERS», таблиця «SCORE ADVANCE TABLE» (НЛО = ?, кальмар 30, краб 20, восьминіг 10), демо-гра (`+window:attract-demo`).
- `game-screen` — згори `score` <1>, `hi-score`, `score` <2>; знизу `lives` числом і іконками гармат, «CREDIT nn».
- «GAME OVER» поверх поля → атракт. Таблиці ініціалів нема.
- Переходи: атракт → (монета, Start) → «PLAY PLAYER<1>» → гра → (хвиля зачищена) нова хвиля → … → (0 життів / вторгнення) GAME OVER → атракт.

## Фічі поза полем
- `+feature:operator-settings` (DIP): життя 3–6, поріг extra life 1000/1500, показ монет.
- `hotseat` — 2 гравці по черзі; `score-records` — один hi-score.
- Нема паузи, рівнів складності, збережень; складність = висота старту хвилі і темп бомб від рахунку.

## Варіації й родичі
- Space Invaders Part II / Deluxe (1979): прибульці, що діляться при влучанні, інтермісії; Galaxian/Galaga — прибульці вилітають зі строю в атаку; Space Invaders Extreme / Infinity Gene — комбо й апгрейди.
- Родичі за «строєм, що спускається»: Centipede (ланцюг замість сітки), Breakout (стіна згори, але без загрози).
- **Осі варіацій:** строй (сітка, що крокує / прибульці виходять з нього / діляться); укриття (нема / руйнуються піксельно / відновлюються між хвилями); бомби (прицільні / з таблиці / випадкові); прискорення (від кількості живих / від часу / від хвилі).

## Цікавинки для курсу
- Строй як одна сутність із сіткою учасників: рух, межі за крайніми живими, крок униз — 🥉.
- Прискорення від кількості живих (апаратний ефект як геймдизайн) — 📎.
- Укриття, що руйнується по шматочку (маска клітин/пікселів) — 🥉 у консолі (клітина з HP), 🥈 у GUI з піксельною маскою.
- Три типи бомб: прицільна vs за таблицею колон, стріляє лише нижній у колоні — 📎.
- НЛО з таблицею очок і лічильником пострілів (детерміновано, «23-й постріл») — 🌱, але гарний урок, що «випадкове» буває таблицею.
- Нова хвиля стартує нижче за таблицею — 🌱.

## Мапа на каталог
- Є: `move-by-input` (ліворуч/праворуч) · `projectile-shot` · `shoot-forward` · `projectile-collision` · `enemy-waves` · `destroy-all-enemies` (хвиля) · `enemy-reached-base` · `player-death` · `event-points` · `progress-acceleration` · `score-records` · `status-panel` · `hot-seat` (по черзі) · `game-screen` · `splash-screen` · `game-loop`.
- **Нема** → пропозиції карток:
  - `+swarm-formation` «Строй рухається як одне ціле» · entities/move · 🥉 · слоти {rows, cols, step}.
  - `+descend-and-reverse` «Біля краю/перешкоди — крок униз і розворот» · entities/move · 📎 (також Centipede).
  - `+speed-by-remaining` «Темп росте, коли ворогів меншає» · game-logic/waves · 📎.
  - `+erodible-shield` «Укриття руйнується по шматочку» · entities/combat · 🥉 · слот {hp|mask}.
  - `+bottom-shooter-only` «Стріляє лише нижній у колоні» · entities/combat · 📎.
  - `+mystery-bonus-ship` «Бонусний ворог-перелітник» · entities/spawn · 📎 · слот {score_table}.
  - `+one-shot-on-screen` «Новий постріл лише після зникнення попереднього» · entities/combat · 🌱 (дитина `shoot-modes`).
  - `+wave-start-lower` «Кожна хвиля стартує ближче» · game-logic/waves · 🌱.
  - `+extra-life-threshold` «Додаткове життя за очки» · game-logic/score · 🌱.

## Пропозиції до словників
- `+trigger:edge` — крайній живий прибулець торкнувся межі (строй розвертається).
- `+trigger:all_gone` — хвиля знищена; `+trigger:reach` — строй дійшов до рядка землі; `+trigger:counter` — рахунок для extra life.
- `+effect:shift` — зсув усього строю; `+effect:speed` — прискорення; `+effect:erode` — нове: вирізати частину сутності/клітини (укриття); `+effect:spawn_at` — бомба від нижнього в колоні; `+effect:lives`.
- `+cond:count` — кількість прибульців (≥ 8 для НЛО, = 1 для останнього).
- `+role:projectile` — постріл і бомби.
- `+window:attract-demo` — атракт з таблицею очок (Q*bert, Pac-Man).
- `+feature:operator-settings` — DIP-налаштування.
- `+axis:actors` — `swarm`: ворог як 55 однакових учасників однієї групи.

## Джерела
- ⭐ [Computer Archeology: Space Invaders](https://www.computerarcheology.com/Arcade/SpaceInvaders/) — як рухається строй, три типи бомб, таблиця НЛО і баг 15 записів, висоти хвиль.
- [Computer Archeology: код](https://www.computerarcheology.com/Arcade/SpaceInvaders/Code.html) — дизасемблер з коментарями.
- [Wikipedia](https://en.wikipedia.org/wiki/Space_Invaders) — правила, вторгнення = кінець гри, прискорення як апаратний ефект.
- YouTube: пошук «space invaders 1978 arcade gameplay».

## Непевне
- (?) Extra life 1500 (DIP 1000) і життя 3–6 — з памʼяті; у переглянутих сторінках не знайдено.
- (?) Чи постріл гравця завжди збиває бомбу, чи лише деякі типи — не перевірено.
- (?) `random: none` — вибір колон бомб і очки НЛО табличні; чи є десь справжній RNG — не перевірено.
- (?) Кількість укриттів (4) і очки 10/20/30 за ряди — з памʼяті (широко відомо, але в переглянутих текстах не наведено).
