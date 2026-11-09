---
title: Do! Run Run
slug: do-run-run
aka: [Super Pierrot, スーパーピエロ, Do!ランラン, Mr. Do! Run Run]
family: maze-arcade
also: []
klass: avatar
axes:
  field: layers
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 1984
platforms: [arcade, MSX (Super Pierrot, 1987), Amiga, Atari ST]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Do!_Run_Run", best: true, note: "мотузка й вписування фруктів, колоди, монстри й мутації, альфа-монстри, мʼяч з бонусом за відскоки, очки"}
  - {kind: other, url: "https://www.arcade-history.com/game/649/", note: "вид згори зі схилами, контур як у Qix, таблиця очок, кіт-конверсія"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/Mr.Do!", note: "JA: розділ про Do!ランラン і Super Pierrot"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Do+Run+Run+arcade+1984", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, visited-trail, projectile-shot, chase-player, touch-death, environment-death, player-death, item-pickup, collect-all, destroy-all-enemies, event-points, spawn-schedule, temporary-modes, speed-per-type, sequential-levels, status-panel, +enclose-upgrade, +rolling-log-trap, +slope-speed, +charge-by-pickup, +bounce-bonus, +line-charge-enemy, +letter-spot-summon, +letter-collection, +enemy-mutation, +multi-kill-bonus, +alt-win-conditions]
proposes: ["+card:enclose-upgrade", "+card:rolling-log-trap", "+card:slope-speed", "+card:charge-by-pickup", "+card:bounce-bonus", "+card:line-charge-enemy", "+card:letter-spot-summon", "+ui:letter-progress"]
author: opus
date: 2026-11-09
---

# Do! Run Run — Mr. Do! без копання: мотузка замикає контури, точки в них дозрівають у фрукти, колоди котяться схилом

## Суть
Четверта й остання гра серії Mr. Do! (Universal). Копання й тунелів нема: Mr. Do бігає готовими доріжками з точками по ярусному полю зі схилами, і **за ним тягнеться мотузка**. Замкнув контур — точки всередині «вписуються» й піднімаються на ступінь: точка → вишня → яблуко → лимон → ананас (як у Qix, але замість захоплення території — апгрейд предметів). Яблука, що падали в тунелі, замінили **колоди**, які зіштовхують з опори й котять схилом; мʼяч сили тепер заряджається їжею і дає бонус за відскоки. Тут — лише відмінності від [`dig-gravity/mr-do`](../dig-gravity/mr-do.md).

## Поле і час
- Вид згори на ярусний ландшафт: плато різної висоти, зʼєднані схилами й сходинками (arcade-history). Доріжки з точками — по плато й схилах; розмір поля і кількість ярусів — (?).
- Шари: рельєф (ярус, схил) + доріжки з точками/фруктами + мотузка-слід + рухомі сутності (Mr. Do, монстри, мʼяч, колоди).
- Real-time. Висота впливає на темп: униз схилом Mr. Do трохи швидший, монстри «втрачають багато часу» на зміні ярусу.
- Фазовий цикл монстрів: через певний час музика змінюється, монстри мутують, згодом повертаються — і так по колу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Mr. Do | player | життя; заряд мʼяча | рух 4 напрямки доріжками; за собою тягне мотузку; кидає мʼяч; зіштовхує колоди з опори |
| Мотузка (слід) | mark | — | лягає на пройдений шлях; кінці зійшлись → контур замкнено |
| Точка | pickup | 10 очок · 1/16 заряду мʼяча | зʼїдається на ходу; усередині замкненого контуру стає вишнею |
| Вишня → яблуко → лимон → ананас | pickup | 20 / 40 / 80 / 160 очок (arcade-history); ананас — 1/4 заряду | кожне нове вписування піднімає ступінь; кращий фрукт — більше очок і заряду |
| Мигаюча буква | switch | одна з E-X-T-R-A | інколи вписаний фрукт стає буквою; наступив — випускає альфа-монстра цієї букви |
| Діамант | pickup | 10 000 (Wiki) · кредит | зʼявляється як буква; збір завершує етап; оператор може вимкнути |
| Мʼяч сили | projectile | заряд; лічильник відскоків | летить і відскакує; пряме влучання вбиває монстра, мʼяч витрачається |
| Колода | object | лежить на опорі над схилом | зіштовхнута — котиться вниз схилом, давить усіх на шляху, Mr. Do теж |
| Схил / сходинка | terrain | ярус | униз — Mr. Do швидшає; монстри гальмують, міняючи ярус |
| Мушля (зелена) | enemy | — | простий переслідувач; часом раптово входить у траєкторію мʼяча чи виходить з неї |
| Змія (синя) | enemy | — | Mr. Do затримався на прямій з нею → стає вогняною кулею, мчить по прямій, імунна до мʼяча |
| Мутанти | enemy | фаза | після зміни музики: мушлі сині й колючі, змії інакші; інша швидкість і охота гнатися |
| Альфа-монстр | enemy | буква | виходить згори екрана; знищено → буква зарахована, поплічники зникають |
| Сині поплічники ×3 | enemy | — | виходять з альфа-монстром, наводяться на Mr. Do, зазвичай приходять першими |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(do, dir)`, `mark(cell_behind, rope)`.
- КОЛИ `pattern(region_closed)` → ТО `transform(item_inside, next_tier)` — точка → вишня → яблуко → лимон → ананас, по одному ступеню за вписування.
- КОЛИ `pattern(region_closed)` → ЯКЩО `prob(p)` → ТО `transform(fruit, letter_spot)`; рідше — `transform(fruit, diamond)` (?).
- КОЛИ `contact(do, dot)` → ТО `pickup`, `score(10)`, `counter(ball_charge, +1/16)`.
- КОЛИ `contact(do, fruit)` → ТО `pickup`, `score(20|40|80|160)`, `counter(ball_charge, +k)` — ананас дає 1/4, вишня заряджає швидше за точку.
- КОЛИ `counter(ball_charge, >=, 1)` → ТО `set_state(do, ball_ready)`.
- КОЛИ `input(fire)` → ЯКЩО `state(do, ball_ready)` → ТО `spawn(ball)`, `clear_state(do, ball_ready)`, `counter(ball_charge, -1)`.
- КОЛИ `blocked(ball)` → ТО `bounce(ball)`, `counter(bounces, +1)`.
- КОЛИ `contact(ball, monster)` → ЯКЩО `not state(monster, fireball)` → ТО `disappear_both`, `score(500 + 500 × bounces)` — стеля 3000.
- КОЛИ `contact(do, log)` → ЯКЩО `custom: «Mr. Do збоку від опори колоди»` → ТО `slide(log, downslope)` — колода котиться до низу схилу.
- КОЛИ `contact(log, monster)` → ЯКЩО `state(log, rolling)` → ТО `disappear_b`, `score(1000 + 500 × (n − 1))` — кожен наступний розчавлений дорожчий на 500.
- КОЛИ `contact(log, do)` → ЯКЩО `state(log, rolling)` → ТО `lives(-1)`.
- КОЛИ `line_of_sight(snake, do)` → ЯКЩО `custom: «Mr. Do затримався на прямій»` → ТО `transform(snake, fireball)`, `slide(fireball, dir)`, `set_state(fireball, ball_immune)`.
- КОЛИ `timer(phase)` → ТО `sound(music_change)`, `transform(monsters, mutated)`, `speed(monsters, ±n)`.
- КОЛИ `timer(phase_end)` → ТО `sound(music_back)`, `transform(mutated, normal)` — цикл повторюється.
- КОЛИ `enter(do, slope_down)` → ТО `speed(do, +n)`.
- КОЛИ `enter(monster, slope)` → ТО `speed(monster, -n)`.
- КОЛИ `contact(do, letter_spot)` → ТО `spawn_at(alpha_monster, top_edge)`, `spawn_at(henchman ×3, top_edge)`.
- КОЛИ `counter(score, %, 5000)` → ЯКЩО `count(alpha_monster, ==, 0)` → ТО `spawn_at(alpha_monster, top_edge)`.
- КОЛИ `destroyed(alpha_monster)` → ТО `custom: «букву EXTRA зараховано»`, `disappear(henchmen)`.
- КОЛИ `counter(extra_letters, ==, 5)` → ТО `lives(+1)`, `score(5000)`, `next_level`.
- КОЛИ `contact(do, diamond)` → ТО `score(10000)`, `custom: «безкоштовний кредит»`, `next_level`.
- КОЛИ `contact(monster, do)` → ТО `lives(-1)`.
- КОЛИ `all_gone(dot)` → ЯКЩО `count(fruit, ==, 0)` → ТО `next_level`.
- КОЛИ `all_gone(regular_monster)` → ТО `next_level` — альфа-монстр і поплічники не рахуються.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Перемога етапу: зʼїдено всі точки й фрукти · знищено всіх звичайних монстрів · EXTRA · діамант. Поразка: 0 життів. Рахунок: таблиця подій + бонуси за відскоки й серію під колодою.

## Керування і ввід
- 4-позиційна рукоятка + одна кнопка (мʼяч), як у Mr. Do!. Доріжки задані, тож ввід — вибір маршруту: куди вести мотузку, щоб замкнути контур навколо найбільшої купи точок.
- Тактика ухилення — змінити ярус (монстри відстають), а не тікати схилом.

## Вікна, меню, HUD
- `game-screen`: ярусне поле + `score`, `lives`, рядок EXTRA (`+ui:letter-progress`) (?) щодо точного складу HUD.
- `attract-demo` і `leaderboard` з ініціалами — типові для аркад Universal (?).
- `end-screen` — GAME OVER (?).
- Переходи: монета → етап → (будь-яка умова перемоги) → наступний етап; смерть → той самий етап.

## Фічі поза полем
- `operator-settings` — ROM можна налаштувати так, щоб діамант не зʼявлявся (Wiki); DIP-перемикачі (arcade-history: 10 налаштувань).
- 2 гравці (Wiki: multiplayer; arcade-history: players 2), найпевніше по черзі — `hotseat` (?).
- Випускалась лише кітом-конверсією для будь-якої шафи (після краху 1983); Super Pierrot (1987, Японія) — трохи інші лабіринти й персонажі.

## Варіації й родичі
- **Відмінності від Mr. Do!**: нема копання (доріжки готові) · вид згори з ярусами замість плаского саду · вишні не лежать групами по 8, а дозрівають із точок у замкненому контурі · яблука → колоди, що котяться схилом · мʼяч не відновлюється таймером, а заряджається їжею, і має бонус за відскоки · букви EXTRA ще й з мигаючих клітин після вписування · діамант 10 000 (у Mr. Do! 8000).
- Серія: Mr. Do! (1982), Mr. Do's Castle (1983), Mr. Do's Wild Ride (1984), Do! Run Run (1984); Neo Mr. Do! (1996) — римейк першої.
- Родичі за механікою: [`amidar`](amidar.md) (замкнений прямокутник фарбується), [`xonix`](xonix.md) і [`gals-panic`](gals-panic.md) (контур захоплює територію), [`lady-bug`](lady-bug.md) (букви EXTRA/SPECIAL), [`pac-man`](pac-man.md) (точки в лабіринті).
- **Осі варіацій** замикання контуру: «захопити територію (Qix/Xonix) / зафарбувати клітини (Amidar) / підвищити ступінь предметів усередині (Do! Run Run)»; снаряд: «таймер відновлення (Mr. Do!) / заряд від їжі (Do! Run Run)».

## Цікавинки для курсу
- Мотузка-слід + виявлення замкненого контуру + апгрейд предметів усередині (flood fill → `transform` на ступінь) — 🥉.
- Мʼяч, що заряджається з їжі дробами (1/16, 1/4), плюс бонус за кількість відскоків — 📎.
- Колода на опорі: зіштовхнути → котиться схилом, лічильник жертв з наростаючими очками — 📎.
- Яруси й схили: швидкість залежить від напрямку схилу, вороги гальмують на зміні ярусу — 🥉.
- Змія → вогняна куля, якщо гравець довго на одній прямій з нею (LOS + імунітет) — 📎.
- Фазовий цикл монстрів за таймером із музикою як сигналом — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `visited-trail` (мотузка) · `projectile-shot` (мʼяч) · `chase-player` · `touch-death` · `environment-death` (колода) · `player-death` · `item-pickup` · `collect-all` · `destroy-all-enemies` · `event-points` · `spawn-schedule` (альфа кожні 5000) · `temporary-modes` (мутації) · `speed-per-type` (схили) · `sequential-levels` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+enclose-upgrade` «Замкнений контур підвищує ступінь предметів усередині» · entities/interact · 🥉 · слот {tiers}.
  - `+rolling-log-trap` «Обʼєкт на опорі котиться схилом і давить усіх» · entities/move · 📎.
  - `+slope-speed` «Швидкість залежить від схилу і зміни ярусу» · entities/state · 🥉.
  - `+charge-by-pickup` «Снаряд заряджається зібраним» · entities/combat · 📎 · слот {charge per item}.
  - `+bounce-bonus` «Очки снаряда ростуть з кожним відскоком» · game-logic/score · 🌱.
  - `+line-charge-enemy` «Ворог мчить по прямій, побачивши гравця» · entities/move · 📎 (сімʼя з `line-of-sight-attack`).
  - `+letter-spot-summon` «Клітина-буква викликає носія букви» · entities/spawn · 🌱.
  - Повтори з `mr-do`: `+letter-collection`, `+enemy-mutation`, `+multi-kill-bonus`, `+alt-win-conditions`.

## Пропозиції до словників
- `+ui:letter-progress` — рядок EXTRA із зарахованими буквами (повтор із `mr-do`).

## Джерела
- ⭐ [Wikipedia: Do! Run Run](https://en.wikipedia.org/wiki/Do!_Run_Run) — мотузка й вписування, ступені фруктів, колоди, мушлі/змії й фазові мутації, альфа-монстри з поплічниками, мʼяч, очки, умови етапу.
- [Arcade History: Do! Run Run](https://www.arcade-history.com/game/649/) — вид згори зі схилами, «прямокутник як у Qix», очки 10/20/40/80/160, колоди, кіт-конверсія, Super Pierrot.
- [Wikipedia JA: Mr.Do!](https://ja.wikipedia.org/wiki/Mr.Do!) — лінія за Mr. Do, замикання цілей підвищує їхні очки й викликає EXTRA-монстрів; MSX-порт Super Pierrot (Nidecom, 1987).
- YouTube: пошук «Do Run Run arcade 1984».

## Непевне
- (?) Діамант: Wikipedia — 10 000, arcade-history — 8000; бонус за вбивство 5 монстрів колодою 10 000 — лише arcade-history.
- (?) Третій ступінь: Wikipedia — яблуко, arcade-history — «cake» (40 очок).
- (?) Чи мотузка зникає після замикання, чи її рвуть монстри, чи є обмеження довжини — у джерелах нема.
- (?) Що буде з мʼячем, який не влучив (лежить, як у Mr. Do!, чи зникає); звідки виходять звичайні монстри.
- (?) Склад HUD, attract-режим і таблиця рекордів — не бачив; розмір поля й кількість ярусів — не бачив.
- (?) Чим саме відрізняються Amiga/ST-порти (1990) від аркади.
