---
title: Kitten Kaboodle (Nyan Nyan Panic)
slug: kitten-kaboodle
aka: [Nyan Nyan Panic, にゃんにゃんぱにっく, Arcade Archives KITTEN KABOODLE, Котяча паніка]
family: push-slide
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: runtime
  goal: collect
year: 1988
platforms: [arcade (Konami GX400), Xbox 360, Windows (Game Room, 2010), PS4, Switch (Arcade Archives, 2025)]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/%E3%81%AB%E3%82%83%E3%82%93%E3%81%AB%E3%82%83%E3%82%93%E3%83%91%E3%83%8B%E3%83%83%E3%82%AF", best: true, note: "правила: удар блоком, блок розбивається об перешкоду, 4 ключі → двері, спецблоки 3 в ряд, секретні етапи (казино, крамниця, кроти), боси з бомбами, 50 етапів"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kitten_Kaboodle", note: "огляд: вид згори, два кошенята, гроші на підсилення, бос кожні 5 рівнів, GX400, Game Room, Arcade Archives"}
  - {kind: official, url: "https://www.arcadearchives.com/en/title/aca-347/", note: "Arcade Archives: 1–2 гравці, налаштування складності, онлайн-рейтинг, 13.02.2025"}
  - {kind: other, url: "https://www.hamster.co.jp/en/release/3281/", note: "реліз Hamster: секретні етапи, крамниця, казино"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Kitten+Kaboodle+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, push-object, inertia-slide, crush-by-slide, destructible-blocks, drop-on-death, key-and-door, collect-quota, reach-exit, temporary-modes, hidden-under-block, shop-between-levels, shop-catalog, shop-window, touch-death, player-death, event-points, score-records, leaderboard, difficulty-levels, sequential-levels, +clear-all-goal, +line-up-bonus, +freeze-all-enemies, +smart-bomb, +multi-kill-bonus, +bonus-stage, +slot-machine-gamble, +whack-a-mole-bonus, +boss-fight, +bomb-exchange-boss, +jump-break-block, +friendly-fire]
proposes: ["+card:slot-machine-gamble", "+card:whack-a-mole-bonus", "+card:bomb-exchange-boss", "+card:jump-break-block", "+card:friendly-fire", "+feature:secret-stage-entrance"]
author: opus
date: 2026-11-09
---

# Kitten Kaboodle — кіт копає блоки у ворогів, збирає 4 ключі з переможених і відчиняє двері; три однакові картинки в ряд — суперсила

## Суть
Аркада Konami 1988 року: один екран, вид згори, поле з блоків і ворогів. Кіт **копає** блок — той летить і збиває ворога, а якщо одразу за блоком перешкода, блок розбивається на місці. Переможені вороги іноді лишають ключ; чотири ключі відчиняють двері, і вхід у них (або руйнування всіх блоків) завершує етап. Поверх цього — блоки з картинками (три однакові в ряд дають суперсилу), секретні етапи під блоками (казино, крамниця, кроти) і бос кожні 5 етапів — перекидання бомбами.

## Поле і час
- Квадратна сітка блоків на одному екрані з видом згори; вся гра — 50 етапів.
- Real-time: вороги рухаються самі, блок після удару летить до перешкоди.
- Частина інформації схована: який ворог лишить ключ, де під блоком вхід у секретний етап або їжа (`info: partial`, `random: runtime`).
- Двоє гравців грають одночасно на одному полі (кооп).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кіт (кошеня 1P / 2P) | player | життя, підсилення | рух 4 напрямки; стрибок; удар (копнути блок) |
| Блок | object | — | після удару летить; влучив у ворога — ворог гине; за ним одразу перешкода — розбивається; приземлення кота зверху теж розбиває |
| Блок з картинкою (вогонь / динаміт / корона / годинник) | object | символ | три однакові в ряд або стовпець → ефект символу |
| Секретний блок | container | — | розбитий ударом відкриває вхід у секретний етап |
| Блок з кулькою-зіркою | container | — | веде в етап «кроти» |
| Ворог | enemy | типи — (?) | ходить полем; дотик = втрата життя; збитий іноді лишає ключ або монету |
| Ключ | pickup | — | 4 ключі відчиняють двері |
| Двері | gate | закрито / відкрито | після 4 ключів — вихід з етапу |
| Монета | pickup | 500 | випадає з ворога |
| Самоцвіт | pickup | 1000 | за 2+ ворогів одним блоком |
| Їжа | pickup | 5000 | дуже рідко з розбитого блока |
| Бос | boss | запас бомб | кожні 5 етапів: перекидаються бомбами з котом |
| Бомба | projectile | — | у бою з босом; купується в крамниці |
| Кріт | enemy | — | у бонус-етапі: збивати блоками |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(cat, dir)`.
- КОЛИ `input(kick)` → ЯКЩО `adjacent(cat, block)` і `free(cell_behind_block)` → ТО `slide(block, dir)` (летить до перешкоди (?)).
- КОЛИ `input(kick)` → ЯКЩО `adjacent(cat, block)` і `not free(cell_behind_block)` → ТО `disappear_b` — блок розбивається на місці.
- КОЛИ `contact(flying_block, enemy)` → ТО `disappear_b`, `spawn_at(coin, enemy_cell)` (?) або ключ.
- КОЛИ `died(enemy)` → ЯКЩО `prob(p)` → ТО `spawn_at(key, enemy_cell)`.
- КОЛИ `contact(flying_block, enemy)` → ЯКЩО `count(enemies_hit_by_block, >=, 2)` → ТО `spawn(gem)` (1000).
- КОЛИ `input(jump)` → ТО `custom: «перестрибнути ворога»`; приземлився на блок → `disappear(block)`.
- КОЛИ `destroyed(block)` → ЯКЩО `prob(very_rare)` → ТО `spawn_at(food, block_cell)` (5000).
- КОЛИ `picked(cat, coin|gem|food)` → ТО `currency(+500|+1000|+5000)`.
- КОЛИ `picked(cat, key)` → ТО `counter(keys, +1)`; КОЛИ `counter(keys, ==, 4)` → ТО `set_state(door, open)`.
- КОЛИ `enter(cat, door)` → ЯКЩО `state(door, open)` → ТО `win`, `next_level` (екран з котом на весь екран).
- КОЛИ `all_gone(block)` → ТО `win`, `next_level`.
- КОЛИ `pattern(line(3))` → ЯКЩО `same(picture_blocks, symbol)` → ТО за символом: вогонь — `custom: «горизонтальна лінія вогню знищує ворогів»`; динаміт — `disappear(all_enemies)`; корона — `set_state(cat, invincible, n)`; годинник — `freeze(all_enemies, n)`.
- КОЛИ `contact(cat, enemy)` → ЯКЩО `state(cat, invincible)` → ТО `disappear_b`; інакше `lives(-1)`.
- КОЛИ `contact(flying_block, cat)` → ТО `lives(-1)` (удар копнутим блоком).
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- КОЛИ `destroyed(secret_block)` → ТО `custom: «вхід у секретний етап»`: казино або крамниця (лише одне за етап); `contact(cat, star_ball)` → етап «кроти».
- Казино: КОЛИ `input(bet)` → ТО `choose(stake)`, `custom: «слот-машина: до ×30 ставки»`.
- Крамниця: КОЛИ `input(buy)` → ЯКЩО `counter(money, >=, price)` → ТО `currency(-price)`, `give(cat, item)` — швидкісні черевики 4000, бомби 15000, 1UP 20000, швидкість блока 5000.
- Кроти: КОЛИ `contact(flying_block, mole)` → ТО `disappear_b`; пройдено → `next_level` (етап зараховано).
- Бос (кожні 5 етапів): КОЛИ `level_end` → ЯКЩО `custom: «у кота бомб менше, ніж у боса»` → ТО `win`; інакше `lives(-1)`, `take(cat, power_ups)`, `custom: «назад на попередній етап»`.
- Перемога: 4 ключі → двері, або всі блоки знищено. · Поразка: життя вичерпано. · Рахунок: гроші за монети, самоцвіти, їжу; рекорд — у таблиці.

## Керування і ввід
- Чотиринапрямний важіль — рух; кнопка 1 — стрибок; кнопка 2 — удар (копнути блок).
- Двоє гравців одночасно, кожен своїм котом (кооп).

## Вікна, меню, HUD
- `attract-demo` (?) — аркадний демо-екран.
- `game-screen`: етап на весь екран; HUD — `score`/гроші, `lives` (?), зібрані ключі (?), `level-number`.
- `end-screen` етапу: картинка кота на весь екран.
- Секретні етапи — окремі екрани: `custom-window` казино (слот-машина), `shop-window` (товари з цінами), етап «кроти».
- Етап боса — окремий екран з бомбами.
- `leaderboard` — таблиця рекордів (?) ; Arcade Archives — онлайн-рейтинг.
- `settings-window` Arcade Archives: складність, вигляд дисплея, показ номера етапу.
- Переходи: game-screen → (етап пройдено) end-screen → game-screen; розбитий секретний блок → секретний етап → наступний етап; кожен 5-й → бос.

## Фічі поза полем
- `levels-sequential`: 50 етапів, бос кожні 5.
- `operator-settings`: складність та інші DIP-налаштування (Arcade Archives дає їх у меню).
- `mode-coop`: 2 гравці одночасно.
- `leaderboard-online` (Arcade Archives); рахунок до 9 цифр замість 7.
- Arcade Archives містить японську й закордонну версії; у закордонній трохи інші правила секретних етапів.

## Варіації й родичі
- Nyan Nyan Panic (JP) і Kitten Kaboodle (світ) — тексти й логотип англійською, інші правила секретних етапів.
- Порти: Game Room (Xbox 360 / Windows, 15.09.2010, Krome Studios) і Arcade Archives (PS4 / Switch, 13.02.2025, Hamster).
- Родичі: `pengo` (блок ковзає й чавить ворогів, розбивається, якщо нема куди їхати; три діаманти в лінію), `kickle-cubicle` (удар блоком), `bomberman` (бонуси з блоків).
- Осі варіацій:
  - **що робить ударений блок**: ковзає до упору (Pengo) / летить і розбивається об перешкоду одразу (Kitten Kaboodle);
  - **як закрити етап**: усі вороги (Pengo) / 4 ключі → двері або всі блоки (Kitten Kaboodle);
  - **бонус «три в ряд»**: очки (діаманти Pengo) / суперсила за символом (тут).

## Цікавинки для курсу
- Удар блоком: ковзання з перевіркою «одразу за блоком перешкода — розбити» — 📎.
- Ключі як випадковий дроп з ворогів + квота 4 → двері — 🌱.
- Блоки з символами: перевірка «три в ряд або стовпець» і чотири різні ефекти — 🥉.
- Дві умови перемоги (двері або всі блоки) — 🌱.
- Секретні етапи: крамниця з цінами, слот-машина зі ставкою, «кроти» — по 📎 за кожну.
- Бос з обміном бомбами й правилом «у кого менше на кінець» — 🥉.

## Мапа на каталог
- Є: `move-4dir` ↔ важіль; `push-object` + `inertia-slide` ↔ удар блока; `crush-by-slide` ↔ блок збиває ворога; `destructible-blocks` ↔ блок розбивається; `drop-on-death` ↔ ключі й монети з ворогів; `key-and-door` + `collect-quota` + `reach-exit` ↔ 4 ключі → двері; `temporary-modes` ↔ корона, годинник; `hidden-under-block` ↔ секретні входи й їжа; `shop-between-levels` + `shop-catalog` + `shop-window` ↔ крамниця; `touch-death` + `player-death`; `event-points` ↔ таблиця грошей; `score-records` + `leaderboard`; `difficulty-levels`; `sequential-levels`.
- **Нема** → пропозиції карток:
  - `+clear-all-goal` (вже пропонована) — знищити всі блоки.
  - `+line-up-bonus` (Pengo) — три однакові в ряд.
  - `+freeze-all-enemies`, `+smart-bomb` (вже пропоновані) — годинник, динаміт.
  - `+multi-kill-bonus` (вже пропонована) — самоцвіт за 2+ ворогів одним блоком.
  - `+bonus-stage`, `+boss-fight` (вже пропоновані).
  - `+slot-machine-gamble` «Слот-машина: ставка грошей» · game-logic/economy · 📎.
  - `+whack-a-mole-bonus` «Бонус-етап: збивати кротів» · levels/progression · 📎.
  - `+bomb-exchange-boss` «Бос: перекидання бомб, у кого менше» · entities/combat · 🥉.
  - `+jump-break-block` «Стрибок на блок розбиває його» · entities/interact · 🌱.
  - `+friendly-fire` «Свій ударений блок шкодить гравцю» · entities/death · 🌱.

## Пропозиції до словників
- `+feature:secret-stage-entrance` — вхід у прихований етап з поля (тут — під блоком), окремо від `collectibles`.
- `+card:slot-machine-gamble`, `+card:whack-a-mole-bonus`, `+card:bomb-exchange-boss`, `+card:jump-break-block`, `+card:friendly-fire` — див. «Мапа на каталог».

## Джерела
- ⭐ [ja.wikipedia: にゃんにゃんぱにっく](https://ja.wikipedia.org/wiki/%E3%81%AB%E3%82%83%E3%82%93%E3%81%AB%E3%82%83%E3%82%93%E3%83%91%E3%83%8B%E3%83%83%E3%82%AF) — повні правила: удар, розбиття, стрибок, ключі й двері, гроші, спецблоки, секретні етапи й ціни крамниці, боси, життя, кооп, порти.
- [Wikipedia: Kitten Kaboodle](https://en.wikipedia.org/wiki/Kitten_Kaboodle) — вид згори, два кошенята, підсилення за гроші, бос кожні 5 рівнів, GX400.
- [Arcade Archives: KITTEN KABOODLE](https://www.arcadearchives.com/en/title/aca-347/) — 1–2 гравці, налаштування, онлайн-рейтинг.
- [Hamster: реліз](https://www.hamster.co.jp/en/release/3281/) — секретні етапи, крамниця, казино, дата.
- YouTube: пошук «Kitten Kaboodle arcade gameplay».

## Непевне
- (?) Чи блок після удару ковзає до упору, як у Pengo, чи летить фіксовану відстань; що з ним стається після влучання.
- (?) Типи ворогів і їхня поведінка, стартова кількість життів, таймер етапу — у джерелах нема.
- (?) Гроші = очки рахунку чи окремий лічильник (JA-вікі пише «гроші»).
- (?) Як саме працює бій з босом (бомби лежать на половинах поля й перекидаються?) — описано лише «у кого менше бомб на кінець».
- (?) Ефект вогню: JA-вікі — горизонтальна лінія, EN-вікі — «у вибраному радіусі».
- Сімʼя: у черзі гра стоїть у `grid-platformer`, але гравітації нема (вид згори, ядро — удар блоком як у Pengo), тому файл у `push-slide`.
