---
title: Shogun Showdown
slug: shogun-showdown
aka: [Shogun Showdown Prologue]
family: roguelike
also: [tactics]
klass: avatar
axes:
  field: 1d
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2023
platforms: [Windows, macOS, Linux, Switch, PS4, PS5, Xbox One, Xbox Series]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shogun_Showdown", best: true, note: "лінія 5–9 клітин, дії ходу, черга до 3 атак, наміри ворогів, тайли й апгрейди"}
  - {kind: steam, url: "https://store.steampowered.com/app/2084000/Shogun_Showdown/", note: "Steam: ранній доступ 27.06.2023, реліз 5.09.2024"}
  - {kind: fandom, url: "https://shogunshowdown.wiki.gg/wiki/Tiles", note: "wiki.gg: усі тайли (шкода/кулдаун/патерн), черга, кулдаун, апгрейди, зачарування"}
  - {kind: fandom, url: "https://shogunshowdown.wiki.gg/wiki/Enemies", note: "вороги, риси (Aggro, Quick, Explosive, Dash), елітні риси"}
  - {kind: fandom, url: "https://shogunshowdown.wiki.gg/wiki/Characters", note: "5 героїв: тайли, спецздібність, умова відкриття"}
  - {kind: fandom, url: "https://shogunshowdown.wiki.gg/wiki/Shop_%26_Skills", note: "5 типів крамниць, пасивні навички, ціни, «кров» замість грошей"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Shogun+Showdown+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-by-input, orientation-state, telegraphed-intents, telegraph-marker, hp-damage, projectile-shot, melee-vs-ranged, status-effects, explode-area, swap-on-contact, pull-object, enemy-waves, destroy-all-enemies, round-currency, shop-between-levels, shop-catalog, shop-sales, in-round-upgrades, run-relics, world-map, map-window, character-select, difficulty-levels, level-unlock, permadeath, keyboard-controls, +one-lane-battlefield, +attack-queue, +tile-cooldown, +facing-attacks, +collision-damage, +friendly-fire, +elite-traits, +hp-as-currency, +combo-kill-rewards, +meta-unlocks]
proposes: ["+effect:enqueue(tile)", "+cond:charged(tile)", "+ui:attack-queue", "+feature:difficulty-days", "+card:attack-queue", "+card:tile-cooldown", "+card:one-lane-battlefield"]
author: opus
date: 2026-11-09
---

# Shogun Showdown — бій на одній лінії: склади з тайлів чергу з трьох ударів і розряди її в потрібний момент

## Суть
Самурай іде островами до Шоґуна; кожен бій — **одновимірна смуга з 5–9 клітин**, де герой і вороги стоять обличчям ліворуч або праворуч. За хід — одна дія: крок, розворот, спецздібність, **покласти тайл-атаку в чергу** (до 3) або **розрядити чергу**. Вороги показують, що зроблять наступного ходу, тож гра — пазл таймінгу: що поставити в чергу зараз, щоб ударити саме тоді, коли ворог стане перед тобою. Між боями — апгрейди тайлів, крамниці, нові тайли; смерть завершує забіг, відкриття лишаються.

## Поле і час
- Поле: лінія з 5–9 клітин (`field: 1d`); у кожної істоти є напрямок погляду — більшість атак бʼє «вперед».
- Хід: гравець діє першим, потім усі вороги виконують показані наміри.
- Вороги приходять хвилями; рівень закінчується, коли всіх переможено (?).
- Карта забігу — вузли регіонів (Bamboo Grove, Whispering Caves, Moonlit Port…) з боями, крамницями, подіями й босами.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP, щит, напрямок, набір тайлів, спецздібність з кулдауном | крок, розворот, черга атак |
| Тайл-атака | supply | шкода, кулдаун 0–8, патерн, слоти апгрейдів (≤8), 1 зачарування | у чергу, лише коли повністю заряджений; після спрацювання заряд скидається |
| Черга атак | zone | 3 слоти | спрацьовує знизу вгору, потім минає хід |
| Ashigaru | enemy | 3 HP | простий мечник |
| Twin Tachi | enemy | 2 HP | бʼє навсібіч — і своїх теж |
| Spike Charger | enemy | 1 HP | таранить |
| Yari Master | enemy | 4 HP | спис на 2 клітини; бʼє, навіть якщо зачепить союзника |
| Yumi Sniper / Ashigaru Archer | enemy | 3 / 2 HP | стрільба з тилу / засідка за лінією |
| Guardian | enemy | 5 HP, Aggro | після атаки йде на гравця |
| Grappler | enemy | 5 HP | гак (тягне) і меч |
| Shinobi | enemy | 4 HP, Quick | сюрікен або димова бомба |
| Shielder | enemy | 4 HP | ставить щит собі або союзнику |
| Warden | enemy | 1 HP, Explosive | призиває або позначає цілі |
| Strider | enemy | 4 HP, Dash | іде якнайдалі за крок |
| Kabukai | enemy | 5 HP | копіює ходи гравця (дзеркало) |
| Елітний ворог | enemy | +HP; Heavy / Double-Striker / Reactive Shield / Corrupted | з Дня 2 |
| Бос (Twins, Nobunaga, Шоґун…) | boss | власні тайли | фінал регіону |
| Barricade | static | 5 HP | перешкода |
| Summoner (статуя) | spawner | — | на старті деяких бос-боїв |
| Пастка (від тайла Trap) | hazard | 3 шкоди | спрацьовує, коли хтось ступає |
| Thorns | hazard | 1 HP | барʼєр, що бʼє у відповідь |
| Монети / черепи | resource | — | монети — крамниця; черепи — відкриття навичок, Astronomer |
| Витратні (Edamame Brew, Kami Brew, Lucky Die, Fenghuang's Feather…) | pickup | — | лікування / реролл / воскресіння з ½ HP |

## Правила (КОЛИ → ЯКЩО → ТО)
Дії героя:
- КОЛИ `input(step dir)` → ЯКЩО `free(cell)` → ТО `move(hero, 1)`, `end_turn`.
- КОЛИ `input(step)` → ЯКЩО `occupied(cell, enemy)` → ТО `custom: «спецздібність героя: Wanderer — swap; Ronin — push; Shadow — пройти крізь; Chain Master — підкинути»`.
- КОЛИ `input(turn)` → ТО `face(hero, opposite)`, `end_turn`.
- КОЛИ `input(queue tile)` → ЯКЩО `custom: «тайл заряджений»` і `count(queue, <, 3)` → ТО `custom: «тайл у чергу»`; ЯКЩО `not state(tile, free_play)` → ТО `end_turn`.
- КОЛИ `input(unleash)` → ТО `custom: «тайли черги спрацьовують знизу вгору»`, `end_turn`.
- КОЛИ `turn_end(hero)` → ТО `custom: «заряд кожного тайла +1»`; КОЛИ `level_start` → ТО `custom: «усі тайли заряджені»`.

Тайли (приклади):
- КОЛИ `exec(katana)` → ЯКЩО `occupied(cell_ahead, unit)` → ТО `damage(2)`; після спрацювання `custom: «кулдаун з нуля»` — навіть якщо промах.
- КОЛИ `exec(spear)` → ТО `damage(2)` на 2 клітини вперед наскрізно; `exec(arrow)` → `damage(2)` першій цілі на лінії.
- КОЛИ `exec(dragon_punch)` → ТО `damage(1)`, `push(target)`; КОЛИ `blocked(target)` → ЯКЩО `occupied(cell, unit)` → ТО `custom: «шкода від зіткнення»`.
- КОЛИ `exec(bo)` → ТО `damage(1)`, `face(target, opposite)` (ворог тепер бʼє не туди).
- КОЛИ `exec(smoke_bomb)` → ТО `swap(hero, first_target)`; `exec(grappling_hook)` → `pull(b)` на клітину перед героєм.
- КОЛИ `exec(sai)` → ЯКЩО `custom: «ціль атакує цього ходу»` → ТО `damage(4)` (подвійна).
- КОЛИ `turn_end(hero)` → ЯКЩО `custom: «Blade of Patience лежить у черзі»` → ТО `custom: «шкода тайла +1»`.
- КОЛИ `exec(trap)` → ТО `place(trap, ahead)`; КОЛИ `enter(unit, trap)` → ТО `damage(3)`.
- Зачарування: Ice → `freeze(target, 3)`; Poison → `set_state(target, poison, 3)` з `damage(1)` щоходу; Curse → `custom: «наступний удар ×2»`; Shockwave → `damage(adjacent)`; Double-Strike → удар двічі.

Вороги:
- КОЛИ `turn_end(hero)` → ТО `custom: «кожен ворог виконує показаний намір (крок, розворот, атака своїм тайлом)»`; нові наміри показуються одразу.
- КОЛИ `input(queue tile)` → ЯКЩО `state(enemy, quick)` → ТО `custom: «ворог атакує одразу»`.
- КОЛИ `custom: «ворог атакував»` → ЯКЩО `state(enemy, aggro)` → ТО `move(enemy, toward hero)`.
- КОЛИ `died(enemy)` → ЯКЩО `state(enemy, explosive)` → ТО `explode(adjacent, 2)`; ЯКЩО `state(enemy, corrupted)` → ТО `spawn_at(progeny, cell)`.
- КОЛИ `custom: «атака ворога зачіпає союзника»` → ТО `damage(ally, n)` (Twin Tachi, Yari Master — дружній вогонь).
- КОЛИ `custom: «спроба зсунути / розвернути»` → ЯКЩО `state(enemy, heavy)` → ТО `block`.
- КОЛИ `custom: «ворог отримав шкоду»` → ЯКЩО `state(enemy, reactive_shield)` → ТО `set_state(enemy, shield)`.

Забіг:
- КОЛИ `died(enemy)` → ТО `currency(+coins)`; кілька вбивств однією чергою — комбо (бонуси навичок: Combo Coin, Triple-Combo Heal).
- КОЛИ `all_gone(enemy)` → ТО `level_end`, `choose(upgrade|tile)` (реролл за монети).
- КОЛИ `hp_zero(hero)` → ЯКЩО `has(hero, Fenghuang's Feather)` → ТО `heal(hero, ½max)`; інакше `lose`; відкриття лишаються.
- КОЛИ `input(blood service)` → ТО `hp(hero, −1)` → реролл крамниці; `hp(hero, −2)` → `currency(+5)`.
- КОЛИ `died(shogun)` → ТО `win`, `unlock(next Day)`; особливі боси → `unlock(hero)`.

## Керування і ввід
- Клавіатура/геймпад: крок вліво/вправо, розворот, тайли з руки (клавіша на тайл), розрядка черги, спецздібність; перестановка й очищення черги.
- Деякі дії (Free-Play тайли) не витрачають хід — комбо в межах одного ходу.

## Вікна, меню, HUD
- `main-menu` → `character-select` (5 героїв) → `difficulty-select` (День 1…7) → `map-window` (вузли регіонів).
- `game-screen`: смуга клітин; над кожним ворогом — `telegraph-marker` (іконка наміру); HP і щит одиниць; стрілка погляду; `attack-queue` (3 слоти); тайли з `skill-bar` (кулдаун-заряд); кнопка спецздібності; монети; витратні.
- `shop-window`: Warring / Combo / Guarding / Dancer / Astronomer (за черепи); послуги «кров'ю».
- `upgrade-window`: апгрейд тайла (+шкода, −кулдаун, +слот, жертва тайла за 40 монет) і вибір нового тайла з рероллом.
- `end-screen`: смерть або перемога над Шоґуном; що відкрито.

## Фічі поза полем
- `meta-progression`: герої, тайли, навички відкриваються незалежно від результату забігу.
- `difficulty-days`: перемога відкриває наступний День (до 7): елітні вороги з Дня 2, Corrupted — на Дні 7.
- Навички в крамницях стакаються до рівня 3; іноді розпродаж за половину ціни.
- Безкоштовний Prologue (демо, 2023); консольні порти.
- Квести (сторінка у вікі) — (?) зміст не перевірено.

## Варіації й родичі
- `tactics/into-the-breach` — показані наміри; `tactics/hoplite` — маленьке поле, кожен крок вирішальний; `rift-wizard`, `pixel-dungeon` — роглайк-забіг з апгрейдами.
- Інші «лінійні» бої: Dicey Dungeons (без поля), Slay the Spire (наміри без позиції), Darkest Dungeon (позиції в шерензі).
- **Осі варіацій**: поле (лінія / сітка); коли бʼють атаки (одразу / з черги за командою / за таймером); що обмежує атаки (кулдаун / мана / колода); видимість намірів (усі / частина / нема).

## Цікавинки для курсу
- Черга з 3 тайлів, що спрацьовує знизу вгору, з «безкоштовними» тайлами — 📎.
- Кулдаун як заряд, що скидається після спрацювання (навіть на промах) — 🌱.
- Одновимірне поле з напрямком погляду: розворот як дія, перевертання ворога як атака — 🌱 (найпростіше поле в корпусі з повноцінною тактикою).
- Наміри ворогів + реакції (Quick атакує, щойно ти поклав тайл) — 🥉.
- Зіткнення від поштовху, дружній вогонь, вибух на смерть — 📎.
- Тайли як дані (шкода, кулдаун, патерн, ефект) + конструктор апгрейдів — 🥉.

## Мапа на каталог
- Є: `move-by-input` · `orientation-state` (погляд ліворуч/праворуч) · `telegraphed-intents`, `telegraph-marker` · `hp-damage` · `projectile-shot` (стріли, сюрікени) · `melee-vs-ranged` · `status-effects` (отрута, лід, прокляття, щит) · `explode-area` (Explosive, Blazing Suisei) · `swap-on-contact` (Wanderer) · `pull-object` (гак) · `enemy-waves` · `destroy-all-enemies` · `round-currency` · `shop-between-levels`, `shop-catalog`, `shop-sales` · `in-round-upgrades` · `run-relics` (навички) · `world-map`, `map-window` · `character-select` · `difficulty-levels` (Дні), `level-unlock` · `permadeath` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+one-lane-battlefield` «Поле — одна лінія з напрямком погляду» · entities/movement · 🌱.
  - `+attack-queue` «Черга до N дій, розрядка за командою» · game-logic/turns · 📎 · слоти {size, order}.
  - `+tile-cooldown` «Атака доступна, коли заряд повний; скидається після вжитку» · entities/state · 🌱.
  - `+facing-attacks` «Атака бʼє за напрямком погляду; розворот — дія» · entities/combat · 🌱.
  - `+collision-damage` «Поштовх у зайняту клітину — шкода обом» · entities/combat · 🌱.
  - `+friendly-fire` «Атака ворога зачіпає союзників» · entities/combat · 🌱.
  - `+elite-traits` «Випадкові елітні риси ворогів» · entities/ai · 📎.
  - `+hp-as-currency` «Платити здоровʼям у крамниці» · game-logic/economy · 🌱.
  - `+combo-kill-rewards` «Бонус за кілька вбивств однією дією» · game-logic/score · 🌱.
  - `+meta-unlocks` «Відкриття між забігами незалежно від результату» · game-logic/progression · 🌱.

## Пропозиції до словників
- `+effect:enqueue(tile)` — покласти дію в чергу без виконання.
- `+cond:charged(tile)` — тайл/здібність заряджені.
- `+ui:attack-queue` — слоти черги дій з порядком.
- `+feature:difficulty-days` — «Дні»: наступна складність відкривається перемогою.
- `+card:attack-queue` · `+card:tile-cooldown` · `+card:one-lane-battlefield`.

## Джерела
- ⭐ [Wikipedia: Shogun Showdown](https://en.wikipedia.org/wiki/Shogun_Showdown) — лінія 5–9 клітин, дії ходу, черга до 3, наміри, тайли, апгрейди, карта, відкриття, релізи й порти.
- [wiki.gg: Tiles](https://shogunshowdown.wiki.gg/wiki/Tiles) — ~40 тайлів із шкодою/кулдауном/патерном, правила черги й кулдауну, апгрейди, зачарування.
- [wiki.gg: Enemies](https://shogunshowdown.wiki.gg/wiki/Enemies) — вороги з HP, риси, елітні риси.
- [wiki.gg: Characters](https://shogunshowdown.wiki.gg/wiki/Characters) — 5 героїв, спецздібності, умови відкриття.
- [wiki.gg: Shop & Skills](https://shogunshowdown.wiki.gg/wiki/Shop_%26_Skills) — крамниці, навички, ціни, HP-послуги.
- [Steam](https://store.steampowered.com/app/2084000/Shogun_Showdown/) — дати, видавці, теги.
- YouTube: [пошук «Shogun Showdown gameplay»](https://www.youtube.com/results?search_query=Shogun+Showdown+gameplay).

## Непевне
- (?) Як саме приходять хвилі ворогів (з країв лінії, за розкладом) і умова кінця бою — не бачив опису.
- (?) Що таке «комбо» формально (кілька вбивств однією розрядкою черги?) — сторінка навичок згадує «combo kill», визначення нема.
- (?) Стартове HP героя, джерела монет крім дропу з ворогів.
- (?) Розкладка клавіш і геймпада — не перевірено.
- (?) Сторінка Quests у вікі — зміст не відкривав.
- (?) Рік: Prologue і ранній доступ — 2023, повний реліз — 4 чи 5.09.2024 (Wikipedia розходиться сама з собою).
