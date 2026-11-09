---
title: Rompers
slug: rompers
aka: [ロンパーズ]
family: maze-arcade
also: [push-slide]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: collect
year: 1989
platforms: [arcade (Namco System 1), PlayStation (Namco Museum Encore), Switch, PS4 (Arcade Archives 2022)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rompers_(video_game)", best: true, note: "ключі в 61 саду, стіни на ворогів, яйця, Tsukaima після таймера, повний список ворогів"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ロンパーズ", note: "найдетальніше: типи плит (1 / 2–3 / ланцюгова), повернення плит, предмети, 6+ ворогів = життя, поведінка кожного ворога"}
  - {kind: other, url: "https://www.arcade-history.com/game/2262/", note: "залізо, 4-way джойстик + 1 кнопка, 1–2 гравці"}
  - {kind: official, url: "https://nintendo.com/games/detail/arcade-archives-rompers-switch", note: "Arcade Archives: опис, налаштування складності, онлайн-рекорди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Rompers+Namco+arcade", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, collect-all, touch-death, player-death, timeout-punisher, chain-reaction, respawn, spawn-points, temporary-modes, item-pickup, event-points, escalating-kill-points, sequential-levels, player-camera, difficulty-levels, game-screen, +topple-wall-crush, +self-restoring-wall, +egg-hatch, +multi-kill-extra-life, +enemy-topples-walls, +wall-ignoring-enemy, +reverse-pad, +multi-hit-enemy]
proposes: ["+effect:topple(a, dir, len)", "+trigger:crushed_by(a, b)", "+card:topple-wall-crush", "+card:self-restoring-wall", "+card:multi-kill-extra-life", "+card:enemy-topples-walls", "+card:reverse-pad", "+card:multi-hit-enemy"]
author: opus
date: 2026-11-09
---

# Rompers — збери ключі в саду-лабіринті, валячи камʼяні плити на ворогів; вони вертаються з яєць

## Суть
Садівник Чап у садовому лабіринті збирає всі ключі, щоб пройти сад (усього 61). Єдина зброя — **плити**: кнопкою Чап валить плиту перед собою, вона падає плазом і чавить ворогів на 1 або 2–3 клітини; за якийсь час плита встає на місце. Розчавлені вороги повертаються яйцями у фіксованих місцях і вилуплюються за кілька секунд. Коли час раунду вийшов, зʼявляється невбивна Tsukaima, що летить крізь стіни, а музика й вороги пришвидшуються.

## Поле і час
- Сітка блоків з косим видом згори (псевдо-ізометрія); лабіринт більший за екран і прокручується за Чапом.
- Чап ходить по 1 блоку; real-time з лімітом часу на раунд.
- Шари: підлога · нерухомі стіни (ґрати тощо) · плити (стоять / лежать) · вороги, яйця, предмети.
- Плита стоїть на клітині й падає в бік поштовху, займаючи 1 або 2–3 клітини підлоги; не впаде, якщо заважає стіна чи інша плита, і падає лише в дозволені боки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чап | player | життя; швидкість | 4 напрямки по 1 блоку; кнопка — повалити плиту перед собою |
| Нерухома стіна | static | — | не рухається, зупиняє падіння плит |
| Плита жовта / блакитна | object | довжина 1 | падає на 1 клітину, чавить |
| Плита салатова | object | довжина 2–3 | падає на 2–3 клітини |
| Плита червона ланцюгова | object | довжина 1 | падаючи, валить інші плити в ряд |
| Повалена плита | hazard | час до відновлення | лежить, потім встає; що стоїть на місці підйому — відкидає |
| Ключ | pickup | — | зібрати всі → раунд пройдено |
| Самоцвіт, перстень, намисто, корона | pickup | — | бонусні очки |
| Землетрус | pickup | тривалість | заморожує ворогів на екрані, Чап невразливий |
| Прискорення | pickup | — | Чап швидшає |
| U-turn | pickup | — | ворог, що торкнувся, розвертається на 180° |
| Яйце | container | фіксоване місце; кілька секунд | у ньому відроджується розчавлений ворог; дотик безпечний |
| Pyokorin | enemy | біла крапля | стрибає на 1–2 блоки |
| Fumajime Pyokorin | enemy | бірюзова | як Pyokorin, але періодично зупиняється покурити |
| Kerara | enemy | — | дихає вогнем; вогонь убиває |
| Todorin | enemy | — | дихає хуртовиною — Чап сповільнюється |
| Gororin | enemy | — | котиться прямо на Чапа, валить плити, в які вріжеться, міняє вісь руху |
| Bekabeka | enemy | пласка «стіна» | валить плити на Чапа |
| Nachibo | enemy | у шоломі | треба розчавити двічі |
| Taggus | enemy | — | кидає бомбу; вибух валить плити поруч |
| Oogumo | boss | кожні 10 раундів | павук-напівбос, плете павутину-пастку |
| Tsukaima | enemy | після таймера | летить крізь стіни, плитами не чавиться, поступово швидшає; дотик — «поцілунок», смерть |
| Gurerin + 4 клони | boss | фінальний раунд | плити лише затримують; ключі відкривають спосіб перемогти; 2 клони вогняні, 2 крижані |
| Вогонь, хуртовина, бомба, павутина | projectile | — | атаки ворогів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_in_dir)` → ТО `move(chap, dir)`, `face(chap, dir)`; інакше `face(chap, dir)`, `block`.
- КОЛИ `input(push)` → ЯКЩО `occupied(cell_ahead, slab)` and `custom: «плита може впасти в цей бік, місце для неї вільне від стін і плит»` → ТО `custom: «плита падає плазом у напрямку погляду на свою довжину (1 або 2–3)»`; інакше `block`.
- КОЛИ `custom: «плита впала на клітини»` → ЯКЩО `occupied(cell, enemy)` → ТО `disappear(enemy)`, `score(n)` — більше ворогів за раз = більше очок; Nachibo — `counter(hits, +1)`, гине з 2-го.
- КОЛИ `custom: «одна 1-клітинна неланцюгова плита розчавила ≥ 6 ворогів»` → ТО `lives(+1)`.
- КОЛИ `custom: «червона плита впала на сусідню плиту»` → ТО `custom: «та теж падає»` (ланцюг, як доміно).
- КОЛИ `custom: «плита впала на Чапа»` (Bekabeka, Gororin, бомба Taggus) → ТО `lose`.
- КОЛИ `timer(slab_restore)` → ТО `custom: «плита встає на початкове місце»`; ЯКЩО `occupied(cell, character)` → ТО `custom: «відкинути того, хто там рухався»`.
- КОЛИ `died(enemy)` → ТО `spawn_at(egg, enemy_spawn_point)`; КОЛИ `timer(hatch)` → ТО `transform(egg, enemy)`.
- КОЛИ `contact(chap, egg)` → ТО `custom: «нічого — яйце безпечне»`.
- КОЛИ `custom: «повалено певну плиту»` → ТО `spawn_at(item, slab_cell)` (предмети ховаються під конкретними плитами).
- КОЛИ `contact(chap, key)` → ТО `pickup`, `counter(keys_left, -1)`.
- КОЛИ `counter(keys_left, ==, 0)` → ТО `win`, `next_level`; кожен 10-й раунд — `window(dialogue-window)` «The Rompers Show».
- КОЛИ `contact(chap, treasure)` → ТО `pickup`, `score(n)`.
- КОЛИ `contact(chap, earthquake)` → ТО `freeze(enemies_on_screen, n)`, `set_state(chap, invincible, n)`.
- КОЛИ `contact(chap, speed_up)` → ТО `speed(chap, +n)`.
- КОЛИ `contact(enemy, u_turn)` → ТО `face(enemy, reverse)`.
- КОЛИ `contact(chap, enemy|fire|bomb_blast)` → ТО `lose` (−1 життя), `restart` раунду з початку, а не з місця смерті.
- КОЛИ `contact(blizzard, chap)` → ТО `speed(chap, -n)`; КОЛИ `contact(chap, web)` → ТО `custom: «Чап застрягає»`.
- КОЛИ `blocked(gororin)` → ТО `custom: «валить плиту, в яку вріжеться, і міняє вертикаль ↔ горизонталь»`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `spawn(tsukaima)`, `speed(enemies, ×k)`, `sound(music_fast)`.
- Tsukaima щотік: `custom: «летить до Чапа крізь стіни»`, `speed(tsukaima, +n)`; плита її не чавить.
- Перемога: пройти 61 раунд, у фінальному розчавити Gurerin і 4 клони. · Поразка: життя вичерпано → `game_over`. · Рахунок: розчавлені вороги (серія за одну плиту дорожча), скарби.

## Керування і ввід
- 4-позиційний джойстик — крок на 1 блок; одна кнопка — повалити плиту перед Чапом.
- 1–2 гравці (по черзі — (?)).

## Вікна, меню, HUD
- `attract-demo` — аркадне демо (?), `splash-screen` — титул.
- `game-screen` — косий вид на прокручуваний лабіринт; HUD: `score`, `hi-score`, `lives`, `timer-countdown`, ключів лишилось (`remaining-counter`) (?).
- `dialogue-window` — катсцена «The Rompers Show» після кожного 10-го раунду.
- `end-screen` — game over; ввід імені → `leaderboard` (?).
- Arcade Archives: `settings-window` (складність, параметри екрана), онлайн-`leaderboard`.
- Переходи: атракт → (монета) раунд → (усі ключі) наступний раунд → кожен 10-й — шоу → … → (життя 0) game over.

## Фічі поза полем
- `levels-sequential` (61 раунд), фінальний бос.
- `operator-settings` (DIP аркади; конкретні опції — (?)); у перевиданні — `difficulty-presets`, `leaderboard-online`.
- Нема збережень і паузи в оригіналі.

## Варіації й родичі
- Офіційні перевидання: Namco Museum Encore (PS1), Arcade Archives (Switch/PS4, 2022). Дизайнер — Akira Usukura (Splatterhouse).
- Родичі: Pengo (ворогів чавлять ковзним блоком), Boulder Dash (обвал на ворога), Heiankyo Alien (вбивство через поле, а не зброю), Lock 'n' Chase і Mouse Trap (стіни-двері зі станом), Devil World (поле чавить гравця).
- Осі варіацій:
  - **як поле вбиває ворога**: блок ковзає до упору (Pengo) / плита падає на довжину 1–3 (Rompers) / камінь падає згори (Boulder Dash);
  - **чи повертається зброя**: блок зникає / плита сама встає за таймером (Rompers);
  - **що робить ворог-«інженер»**: нічого / валить плити на гравця (Bekabeka, Gororin, бомба Taggus);
  - **кара за час**: програш / невбивний переслідувач крізь стіни (Rompers, Heiankyo Alien, Berzerk).

## Цікавинки для курсу
- Плита, що падає плазом на довжину L у напрямку поштовху, з перевіркою «чи вільне місце падіння» — 📎.
- Самовідновлення плити за таймером + відкидання того, хто на місці підйому — 📎.
- Ланцюгова червона плита (доміно) — 🥉: каскад падінь з перевіркою кожного кроку.
- Яйця: смерть ворога → контейнер у точці спавну → таймер вилуплення — 📎.
- Вороги, що самі валять плити на гравця, — поле як зброя обох сторін — 🥉.
- Невбивний переслідувач після таймера з наростанням швидкості — 🌱.
- Бонус-життя за 6+ ворогів однією плитою — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `collect-all` ↔ ключі; `touch-death` · `player-death`; `timeout-punisher` ↔ Tsukaima; `chain-reaction` ↔ червона плита; `respawn` + `spawn-points` ↔ яйця у фіксованих місцях; `temporary-modes` ↔ землетрус; `item-pickup` ↔ скарби й бонуси; `event-points` · `escalating-kill-points` ↔ серія за одну плиту; `sequential-levels` ↔ 61 раунд; `player-camera` ↔ прокручуваний лабіринт; `difficulty-levels` (перевидання); `game-screen`.
- **Нема** → пропозиції карток:
  - `+topple-wall-crush` «Повалити плиту на ворогів» · entities/combat · 📎 · слот {length: 1..3}.
  - `+self-restoring-wall` «Повалена стіна встає за таймером» · entities/state · 📎 · слот {delay}.
  - `+egg-hatch` (Dot Valley, Repton) — ворог повертається яйцем і вилуплюється.
  - `+multi-kill-extra-life` «Життя за N ворогів одним ударом» · game-logic/score · 🌱 · слот {n: 6}.
  - `+enemy-topples-walls` «Ворог використовує ту саму зброю поля» · entities/move · 📎.
  - `+wall-ignoring-enemy` (Mouse Trap) — Tsukaima крізь стіни.
  - `+reverse-pad` «Предмет розвертає ворога» · entities/interact · 🌱.
  - `+multi-hit-enemy` «Ворог гине з N-го удару» · entities/combat · 🌱 · слот {hits: 2}.

## Пропозиції до словників
- `+effect:topple(a, dir, len)` — плита падає плазом у напрямку на довжину L (уже пропонувалось у корпусі — підтверджую).
- `+trigger:crushed_by(a, b)` — A опинився під плитою/стіною, що впала або зсунулась (Rompers, Devil World).
- `+card:topple-wall-crush`, `+card:self-restoring-wall`, `+card:multi-kill-extra-life`, `+card:enemy-topples-walls`, `+card:reverse-pad`, `+card:multi-hit-enemy` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Rompers](https://en.wikipedia.org/wiki/Rompers_(video_game)) — 61 сад, ключі, стіни на ворогів, яйця за кілька секунд, Tsukaima після таймера з пришвидшенням, 9 ворогів і фінальний бос із 4 клонами, шоу кожні 10 раундів.
- [Wikipedia JA: ロンパーズ](https://ja.wikipedia.org/wiki/ロンパーズ) — типи плит і їхні довжини, обмеження напрямку падіння, повернення плит і відкидання, 6+ ворогів = життя, предмети з плит, рестарт раунду з початку, поведінка кожного ворога.
- [arcade-history: Rompers](https://www.arcade-history.com/game/2262/) — Namco System 1, вертикальний екран, 4-way джойстик + 1 кнопка, 1–2 гравці.
- [Nintendo: Arcade Archives ROMPERS](https://nintendo.com/games/detail/arcade-archives-rompers-switch) — перевидання 2022, налаштування складності, онлайн-рекорди.
- YouTube: пошук «Rompers Namco arcade».

## Непевне
- (?) Тривалість таймера раунду, час повернення плит і вилуплення яєць; очки за ворогів і скарби — не знайдено.
- (?) Скільки життів на старті: JA-вікі пише «残り人数3人分» — трактування неоднозначне.
- (?) Чи зібрані ключі зберігаються після смерті, коли раунд рестартує з початку.
- (?) Як саме павутина Oogumo тримає Чапа (час, чи можна вибратись) і чи є в ній випадковість поведінки ворогів.
- (?) 2P — по черзі чи одночасно; DIP-налаштування (життя, бонус) — сторінка їх не показує.
