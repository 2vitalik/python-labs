---
title: Dig Dug
slug: dig-dug
family: dig-gravity
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 1982
platforms: [arcade, Atari 2600, Atari 5200, C64, NES, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dig_Dug", best: true, note: "правила, насос, привиди, камені, втеча останнього, kill screen 256"}
  - {kind: wiki, url: "https://discmaster.textfiles.com/view/1886/1000gamemanuals.iso/Atari%202600/Dig%20Dug.txt", note: "інструкція Atari 2600: повні таблиці очок, овочі за раундами, життя"}
  - {kind: wiki, url: "https://www.c64-wiki.com/wiki/Dig_Dug", note: "C64: 5 життів, складність 1–10, овоч 10 с"}
  - {kind: wiki, url: "https://strategywiki.org/wiki/Dig_Dug/Gameplay", note: "StrategyWiki: геймплей і таблиці очок (аркада)"}
  - {kind: wiki, url: "https://www.exotica.org.uk/wiki/Lost_In_Translation/Dig_Dug", note: "відмінності портів"}
  - {kind: play, url: "https://c64.krissz.hu/dig-dug/play-online/", note: "C64-версія в браузері"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dig+dug+arcade+1982+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 70
mechanics: [move-4dir, gravity-fall, touch-death, environment-death, player-death, destroy-all-enemies, chase-player, event-points, combo-multiplier, progress-acceleration, sequential-levels, score-records, status-panel, +dig-terrain, +pump-inflate, +ghost-phase, +delayed-fall, +bonus-item-spawn, +layer-score, +flee-last-enemy, +fire-breath]
proposes: ["+trigger:input", "+trigger:counter", "+trigger:idle", "+cond:state", "+cond:facing", "+cond:count", "+effect:fall", "+effect:set_state", "+effect:stun", "+effect:speed", "+effect:spawn_at", "+effect:lives", "+role:terrain", "+role:projectile", "+ui:lives", "+ui:level-number", "+card:fire-breath", "+window:game-over-continue"]
author: opus
date: 2026-11-02
---

# Dig Dug — прокопай тунелі, надуй ворогів насосом або розчави каменем

## Суть
Діг Даг риє тунелі в розрізі ґрунту й знищує всіх ворогів раунду: Пука й дракони Фігари. Зброя — **насос**, що чіпляється на ворога, і повторні натискання надувають його до вибуху, або **камінь**, під яким треба підкопати. Вороги ходять тунелями, але можуть перетворитися на «очі» й пройти крізь землю; Фігар дихає вогнем. Цікаве — гравець сам будує лабіринт, по якому за ним женуться.

## Поле і час
- Вертикальний розріз ґрунту: зверху поверхня з небом, далі **4 шари різного кольору** (глибше — дорожче); на старті кожного раунду — кілька порожніх кишень з ворогами, центральний тунель гравця і кілька каменів.
- Земля «зʼїдається» плавно, але рух і повороти привʼязані до сітки.
- Real-time; з часом раунду вороги прискорюються й частіше стають привидами; останній ворог тікає.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Діг Даг | player | життя (аркада ~3; C64 5) | 4 напрямки; риє тунель у напрямку руху; стріляє насосом |
| Земля (4 шари) | terrain | шар → множник очок | стає тунелем, коли через неї пройти; +10 очок за копання |
| Тунель | terrain | — | вороги ходять лише ним (у звичайному стані) |
| Насос (гарпун) | projectile | коротка дальність | летить уперед по тунелю; не крізь землю; влучив → ворог прикутий |
| Пука | enemy | стадії надування 0→вибух | ходить тунелями до Діг Дага; дотик — смерть |
| Фігар | enemy | вогонь по горизонталі | як Пука + видих вогню на кілька клітин, крізь землю; збоку — подвійні очки |
| Привид («очі») | enemy | стан ворога | проходить крізь землю повільно; невразливий, не атакує; у тунелі → знову тіло |
| Камінь | object | затримка перед падінням | підкопали знизу → хитається → падає; розчавлює всіх; розбивається при приземленні |
| Овоч (бонус) | pickup | ціна за раундом 400…8000 | після 2 впалих каменів зʼявляється в центрі на ~10 с |
| Квіти на поверхні | static | лічильник раундів | показують номер раунду (великий = 10) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(digdug, dir)`; ЯКЩО `cell(target, dirt)` → ТО `set_cell(tunnel)`, `score(10)` (2600: за кожні 2 клітини).
- КОЛИ `input(fire)` → ЯКЩО `free(tunnel ahead)` → ТО `spawn(pump)` уперед; КОЛИ `contact(pump, enemy)` → ТО `set_state(enemy, inflating)`, `freeze`.
- КОЛИ `input(fire)` → ЯКЩО `state(enemy, inflating)` → ТО `custom: «стадія надування +1»`; стадія 4 → `disappear_b`, `score(layer_value)`.
- КОЛИ `idle(n)` або `input(move)` → ЯКЩО `state(enemy, inflating)` → ТО `custom: «насос відчіплюється, ворог здувається»`, `stun(enemy, до повного здування)`.
- КОЛИ `custom: «ворога надуто до вибуху»` → ТО `score(200|300|400|500 за шаром)`; ЯКЩО Фігар і `facing(digdug, horizontal)` → ТО `score(×2)`.
- КОЛИ `custom: «під каменем вирито»` → ЯКЩО `not occupied(below, digdug)` → ТО `timer(wobble)` → `fall(rock)`; поки Діг Даг стоїть під ним — тримається.
- КОЛИ `contact(falling rock, enemy|digdug)` → ТО розчавлює: ворог `disappear_b`; Діг Даг → `lose`.
- КОЛИ `after(fall(rock))` → ТО `disappear_a` (камінь розбивається); `score` за кількістю розчавлених: 1 = 1000, 2 = 2500, 3 = 4000 … 7 = 12000.
- КОЛИ `counter(rocks_dropped, ==, 2)` → ЯКЩО `count(enemy, <, 7)` → ТО `spawn_at(vegetable, center)`, `timer(10 s)` → `disappear`.
- КОЛИ `contact(digdug, vegetable)` → ТО `pickup`, `score(round_value)`.
- КОЛИ `rng(p)` (з часом частіше) → ТО `set_state(enemy, ghost)`: `move(enemy, toward(digdug))` крізь землю, `speed(×slow)`; КОЛИ `enter(enemy, tunnel)` → ТО `clear_state(ghost)`.
- КОЛИ `in_range(fygar, digdug, n)` and `line_of_sight` по горизонталі → ТО `custom: «видих вогню на кілька клітин, крізь землю»`; КОЛИ `contact(fire, digdug)` → ТО `lose`.
- КОЛИ `contact(enemy, digdug)` → ЯКЩО `not state(enemy, inflating|ghost)` → ТО `lose`, `lives(-1)`, `respawn(digdug, start)`.
- КОЛИ `died(enemy)` → ТО `speed(other enemies, +)`; КОЛИ `count(enemy, ==, 1)` → ТО `custom: «останній тікає вгору до лівого краю поверхні»`; дійшов → `disappear` без очок.
- КОЛИ `all_gone(enemy)` → ТО `next_level`.
- КОЛИ `counter(score, >=, threshold)` → ТО `lives(+1)` (2600: 20 000, далі кожні 50 000).
- Перемога раунду: усі вороги знищені або втекли. Поразка: дотик ворога, вогонь, камінь → −1 життя; 0 → `game_over`. Раунд 256 — «kill screen» (переповнення байта).

## Керування і ввід
- Джойстик 4 напрямки (без діагоналей): рух і копання в напрямку.
- Кнопка: постріл насосом; повторні натискання — надування; відпустити/рушити — ворог зривається.
- Тактика каменів — тайминг: вирити під каменем і відійти, щоб камінь упав на ворогів.

## Вікна, меню, HUD
- `splash-screen` / атракт-режим: демо-гра, таблиця очок.
- `game-screen`: розріз ґрунту; HUD — `score`, `hi-score`, `lives` (фігурки), `level-number` (квіти на поверхні + номер раунду).
- `custom-window` «Round N»: заставка перед раундом.
- `end-screen` «Game Over» → `leaderboard` з ініціалами (аркада).
- `game-over-continue` (2600): кнопка на титулі за ~10 с після смерті — продовжити з останнього раунду.
- `difficulty-select`: 2600 — Normal/Easy (ведмедик); C64 — 1–10.

## Фічі поза полем
- `levels-sequential`: 255 раундів; розкладка ґрунту й кількість/швидкість ворогів ростуть.
- `difficulty-presets` (порти), `continue` (2600), `leaderboard-local` (аркада), бонусні життя за очки.
- Easy-режим 2600: та сама мапа, 2 вороги, без привидів і прискорення.

## Варіації й родичі
- Dig Dug II (вид згори, свердлиш розломи, щоб топити шматки острова), Dig Dug Arrangement (кооп, боси), Dig Dug Deeper (3D), Digging Strike (DS, гібрид 1 і 2).
- Родичі: Mr. Do! (тунелі, яблука падають), Digger (1983), Boulder Dash (копання + падіння, але покрокова фізика), Mr. Driller.
- **Осі варіацій**: убивство — «надування з кількох натискань / одразу»; ворог і земля — «лише тунелями / привидом крізь землю»; камінь — «падає одразу (BD) / з затримкою й розбивається (Dig Dug)»; очки — «фіксовані / залежать від глибини й боку».

## Цікавинки для курсу
- Копання тунелів, що стають лабіринтом для AI-ворогів — 🥉 (поле змінюється, погоня по ньому).
- Насос: багатостадійна атака з відкатом (не дотиснув — ворог здувається й оглушений) — 🥉.
- Ворог-привид: зміна правил проходу (крізь землю, невразливий) за таймером — 📎.
- Камінь з затримкою + множник за кількість розчавлених — 📎.
- Бонус-предмет після події (2 камені) з таймером зникнення — 🌱.
- Очки за глибиною шару й боком удару — 🌱.
- Останній ворог тікає до краю — 📎 (зміна цілі AI).

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` ↔ камені · `touch-death` · `environment-death` ↔ камінь, вогонь · `player-death` · `destroy-all-enemies` · `chase-player` · `event-points` · `combo-multiplier` ↔ кілька ворогів одним каменем · `progress-acceleration` ↔ прискорення ворогів · `sequential-levels` · `score-records` · `status-panel`; вікно `game-over-continue` ⏳ — у «Вікнах».
- **Нема** → пропозиції карток:
  - `+pump-inflate` «Атака в кілька натискань з відкатом» · entities/combat · 🥉 · слоти {stages, decay}.
  - `+ghost-phase` «Ворог проходить крізь стіни в стані» · entities/move · 📎 · слот {chance, speed}.
  - `+delayed-fall` «Падіння з затримкою й руйнуванням» · entities/move · 📎 — дитина `gravity-fall`.
  - `+bonus-item-spawn` «Бонус після події з таймером» · entities/spawn · 🌱 · слоти {after, lifetime}.
  - `+layer-score` «Очки за зоною поля» · game-logic/score · 🌱.
  - `+flee-last-enemy` «Останній ворог тікає» · entities/move · 📎.
  - `+fire-breath` «Атака по лінії на N клітин крізь перешкоди» · entities/combat · 📎.
  - Повтор: `+dig-terrain` (з Boulder Dash/Repton — тут копання ще й дає очки).

## Пропозиції до словників
- `+trigger:input` ⏳ (насос), `+trigger:counter` ⏳ (2 камені → овоч), `+trigger:idle` ⏳ (не тиснеш → ворог здувається).
- `+cond:state` ⏳ (надувається/привид), `+cond:facing` ⏳ (удар збоку по Фігару), `+cond:count` ⏳ (ворогів < 7).
- `+effect:fall` ⏳, `+effect:set_state` ⏳, `+effect:stun` ⏳, `+effect:speed` ⏳, `+effect:spawn_at` ⏳, `+effect:lives` ⏳.
- `+role:terrain` ⏳ (шари землі), `+role:projectile` ⏳ (насос, вогонь).
- `+ui:lives`, `+ui:level-number` — ⏳, тут номер раунду ще й «квітами» на полі.

## Джерела
- ⭐ [Wikipedia: Dig Dug](https://en.wikipedia.org/wiki/Dig_Dug) — повний опис механік, привиди, камені, втеча, kill screen, сиквели.
- [Інструкція Atari 2600](https://discmaster.textfiles.com/view/1886/1000gamemanuals.iso/Atari%202600/Dig%20Dug.txt) — таблиці очок (шари, бік, камені, овочі), бонусні життя, Easy-режим.
- [C64-Wiki](https://www.c64-wiki.com/wiki/Dig_Dug) — 5 життів, складність 1–10, овоч у центрі на 10 с, вогонь крізь землю.
- [StrategyWiki: Gameplay](https://strategywiki.org/wiki/Dig_Dug/Gameplay) — аркадні таблиці (сторінка не відкрилась для перевірки).
- [Lost In Translation](https://www.exotica.org.uk/wiki/Lost_In_Translation/Dig_Dug) — відмінності версій.

## Непевне
- (?) Значення очок узяті з інструкції 2600; аркадні таблиці близькі, але не звірені (StrategyWiki не відкрилась).
- (?) Квіти на поверхні як лічильник раундів і «великий квіт = 10» — з памʼяті, у прочитаних джерелах нема.
- (?) Кількість стадій надування (4) і кількість життів аркади — з памʼяті.
- (?) Наскільки поведінка ворогів випадкова (`random: runtime`) — джерела кажуть «час від часу стають привидами».
- (?) Овоч: 2600 — на стартовій позиції гравця, C64 — у центрі; в аркаді — центр (?).
