---
title: Bomberman
slug: bomberman
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: setup
  goal: state
year: 1985
platforms: [NES/Famicom, SNES (Super Bomberman 1993), PC Engine, arcade, сучасні консолі]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bomberman_(1985_video_game)", best: true, note: "NES-версія: бомби, приховані виходи й підсилення, таймер, життя, паролі"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Super_Bomberman", note: "battle mode: 4 гравці, 2 хв, Hurry Up і падаючі стіни, трофеї"}
  - {kind: fandom, url: "https://takeontheneslibrary.com/tag/fire", note: "огляд NES: усі 8 підсилень з ефектами, таймер 200, паролі, бонус-етапи"}
  - {kind: fandom, url: "https://bomberpedia.shoutwiki.com/wiki/Bomberman_(NES)", note: "очки за ворогів, бонус-предмети, бонус-етапи"}
  - {kind: wiki, url: "https://strategywiki.org/wiki/Bomberman/Gameplay", note: "StrategyWiki: керування, детонатор, втрата підсилень"}
  - {kind: wiki, url: "https://strategywiki.org/wiki/Super_Bomberman_2/Power-ups", note: "підсилення SB2: kick, power glove, remote, bomb/block passer"}
  - {kind: fandom, url: "https://randomhoohaas.flyingomelette.com/bomb/nes-1/game.html", note: "фан-довідник: вороги NES з поведінкою й очками"}
  - {kind: wiki, url: "https://www.tcrf.net/Bomberman_(NES)", note: "TCRF: невикористаний контент"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=bomberman+nes+gameplay", note: "пошук; геймплей NES"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=super+bomberman+battle+mode+4+players", note: "пошук; battle mode"}
stage: v1
coverage: 70
mechanics: [move-4dir, impassable-cells, blast-wave, chain-detonation, in-round-upgrades, item-pickup, destroy-all-enemies, reach-exit, time-out, touch-death, environment-death, random-walk, chase-greedy, temporary-modes, +destructible-blocks, +hidden-under-block, +bomb-fuse, +remote-detonation, +bomb-kick, +bomb-throw, +shrinking-arena, +curse-item, +timeout-punisher, +permit-item, +match-trophies]
proposes: ["+effect:explode", "+effect:throw", "+trigger:blast", "+cond:owner_count", "+card:destructible-blocks", "+card:hidden-under-block", "+card:shrinking-arena", "+card:timeout-punisher", "+window:match-setup", "+window:level-password", "+ui:player-portraits", "+feature:match-trophies"]
author: opus
date: 2026-11-02
---

# Bomberman — став бомбу, тікай від хреста вогню, підірви стіну й знайди вихід

## Суть
Бомбермен ходить лабіринтом із нерухомих колон і руйнованих блоків і ставить бомби, що за кілька секунд вибухають хрестом. Вибух руйнує блоки, вбиває ворогів — і самого гравця, тож ядро гри в тому, щоб поставити бомбу й устигнути сховатися з лінії вогню. Під блоками сховані вихід і одне підсилення на рівень; у Super Bomberman battle mode той самий двіжок перетворюється на арену «останній вижилий» на 4 гравців.

## Поле і час
- NES: поле — сітка з непробивних колон (кожна друга клітина в кожному другому рядку) і коридорів між ними; рівень завширшки у два екрани, камера скролиться горизонтально. Гравець стартує в лівому верхньому куті, блоки розставлені випадково.
- Battle mode (Super Bomberman): одна арена на екран, 12 тематичних арен (Speed Round — найконкурентніша), до 4 гравців.
- Real-time: усі сутності рухаються одночасно, у кожного ворога своя швидкість; бомба — локальний таймер (запал) на кілька секунд.
- Шари: підлога → блок (під ним може бути вихід/підсилення) → бомба/вогонь → персонажі. Вихід і підсилення невидимі, доки блок не зруйновано — звідси `info: hidden`.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бомбермен | player | 3 життя (NES), швидкість, bombs, fire | рух 4 напрямки; кнопка A — бомба на свою клітину |
| Бомба | object | fuse ≈ кілька секунд, range = fire | непрохідна (без Bomb Pass); за запалом → вибух |
| Вибух (вогонь) | hazard | range клітин у 4 боки, коротке життя | хрест, зупиняється на колоні; на блоці руйнує його й зупиняється |
| Колона (hard block) | static | — | непробивна, гасить вибух |
| Цегла (soft block) | object | може ховати вихід/підсилення | руйнується вибухом |
| Вихід (двері) | gate | прихований під цеглою | відкритий лише коли ворогів 0; вибух по ньому → спавн ворогів |
| Bomb Up | pickup | +1 | +1 одночасна бомба (постійне) |
| Fire Up | pickup | +1 | +1 клітина дальності (постійне) |
| Speed (ковзани) | pickup | — | швидший рух |
| Wall Pass | pickup | до смерті | прохід крізь цеглу (не крізь колони) |
| Bomb Pass | pickup | до смерті | прохід крізь власні бомби |
| Flame Pass | pickup | до смерті | імунітет до вибухів |
| Detonator (Remote) | pickup | до смерті | бомби не вибухають самі; B підриває найстарішу |
| Mystery (?) | pickup | тимчасове | невразливість до ворогів і вибухів на час |
| Ballom | enemy | 100 очок, повільний | блукає |
| Onil | enemy | 200, середній | блукає, повертає до гравця на одній осі (?) |
| Dahl | enemy | 400 | змінює напрям за таймером 0.8–3.2 с (?) |
| Minvo | enemy | 800, швидкий | змінює напрям 0.5–2 с, повертає до гравця (?) |
| Kondoria (Doria) | enemy | 1000, дуже повільний | проходить крізь цеглу |
| Ovape | enemy | 2000, повільний | проходить крізь цеглу, то наближається, то тікає |
| Pass | enemy | 4000, швидкий | переслідує гравця |
| Pontan | enemy | 8000, найшвидший | переслідує, проходить крізь цеглу; карає за таймер і вибух виходу |
| Бонус-предмети | pickup | 10 000…20 000 000 очок | зʼявляються за прихованими умовами, один на рівень |
| Падаюча стіна (battle) | hazard → static | з 1:30 раунду | заповнює арену спіраллю від лівого нижнього кута за годинниковою стрілкою, убиває |
| Kick / Power Glove / Skull (Super-серія) | pickup | — | штовхнути бомбу ногою / підняти й кинути / прокляття |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(bomb)` → ЯКЩО `count(own_bombs, <, bombs) and free(cell_under)` → ТО `spawn(bomb)` на клітині гравця.
- КОЛИ `timer(fuse)` бомби → ЯКЩО `not has(owner, detonator)` → ТО `custom: «вибух: хрест на range клітин у 4 боки, промінь зупиняється на колоні; на цеглі — руйнує й зупиняється»` (`disappear_a`, `spawn(blast)`).
- КОЛИ `input(detonate)` → ЯКЩО `has(player, detonator)` → ТО вибухає найстаріша власна бомба.
- КОЛИ `contact(blast, bomb)` → ТО `trigger(explode)` — ланцюгова детонація; так влаштовуються «мости» вогню.
- КОЛИ `contact(blast, soft_block)` → ТО `disappear_b`, `reveal(cell)` (вихід/підсилення, якщо було).
- КОЛИ `contact(blast, enemy)` → ТО `disappear_b`, `score(enemy_value)`.
- КОЛИ `contact(blast, player)` → ЯКЩО `not has(player, flame_pass) and not state(player, invincible)` → ТО `lives(-1)`, `restart` рівня.
- КОЛИ `contact(enemy, player)` → ЯКЩО `not state(player, invincible)` → ТО `lives(-1)`.
- КОЛИ `contact(player, power_up)` → ТО `pickup`, `custom: «бомби/вогонь +1, решта — дозвіл»`.
- КОЛИ `contact(blast, power_up)` → ТО `disappear_b` (підсилення втрачено), `spawn(enemy×N)` сильніших ворогів.
- КОЛИ `contact(blast, exit)` → ТО `spawn(enemy×N)` з дверей (двері лишаються).
- КОЛИ `all_gone(enemy)` → ТО `sound(chime)`; КОЛИ `contact(player, exit)` → ЯКЩО `count(enemy, ==, 0)` → ТО `next_level`, `lives(+1)`.
- КОЛИ `counter(time, ==, 0)` (старт 200) → ТО `spawn_at(pontan×N, field)` — життя не забирається, але виживати стає майже неможливо.
- КОЛИ `contact(player, soft_block)` → ЯКЩО `has(player, wall_pass)` → ТО прохід; інакше `block`. Аналогічно бомба + `bomb_pass`.
- КОЛИ `died(player)` → ТО `take(player, wall_pass|bomb_pass|flame_pass|detonator)`; bombs/fire (і, за одним джерелом, speed) лишаються.
- Вороги: Ballom/Onil/Dahl/Minvo — `random-walk` зі зміною напрямку за таймером; Kondoria/Ovape/Pontan — `custom: «ігнорують цеглу»`; Pass/Pontan — `chase-greedy` (?); швидкість — `speed-per-type`.
- Battle mode: КОЛИ `contact(blast, player)` → ТО `disappear_b` (без HP, без щита за замовчуванням); КОЛИ `count(alive, ==, 1)` → ТО `score(trophy)` переможцю; КОЛИ `count(alive, ==, 0)` або `timer(2:00)` → ТО `draw`.
- Battle mode: КОЛИ `timer(1:30)` → ТО `message("Hurry Up!")`, `set_cell(wall)` по спіралі від краю щотік; `contact(falling_wall, player)` → `lose` для гравця.
- Super-серія: КОЛИ `contact(player, bomb)` → ЯКЩО `has(player, kick)` → ТО `slide(bomb, dir)` до упору; Power Glove — `custom: «підняти бомбу й кинути на кілька клітин через перешкоди»`; Skull — `set_state(player, curse, 6s)` (реверс керування, понос бомбами, повільно…), передається дотиком іншому гравцю (SB3).
- Перемога (кампанія): усі вороги знищені + вхід у двері, 50 рівнів. Поразка: 0 життів → пароль. Рахунок: очки за ворога за типом (100…8000), бонус-предмети, бонус-етапи.

## Керування і ввід
- D-pad — рух 4 напрямки (клітинний, але плавний: персонаж «доводиться» до коридору); A — поставити бомбу; B — детонатор (лише з підсиленням).
- Battle mode: кожен гравець — свій контролер (SNES — мультитап для 3–4 людей); CPU-гравці заповнюють решту слотів.
- Super-серія: окрема кнопка для kick-стопу / підняття бомби з Power Glove (?).

## Вікна, меню, HUD
- `splash-screen` / `main-menu` (NES): START · CONTINUE → `level-password`.
- `game-screen`: поле + верхня смуга `timer-countdown` (200), `score`, `lives`.
- `custom-window` «STAGE N» — заставка перед рівнем; «BONUS STAGE» — після кожного 5-го.
- `end-screen` «GAME OVER» → показ пароля (20 літер A–P: рівень, бомби, вогонь, очки).
- `level-password` — введення пароля для продовження.
- Super Bomberman: `mode-select` (Normal / Battle), `match-setup` (кількість гравців людина/CPU, кількість трофеїв 1–5, вибір арени), `end-screen` раунду з трофеями, `pause-menu`.
- HUD battle: `player-portraits` з живими/мертвими, `timer-countdown` 2:00.
- Переходи: main-menu → STAGE N → game-screen → (двері) STAGE N+1; (смерть) → STAGE N; (0 життів) → GAME OVER + пароль.

## Фічі поза полем
- `levels-sequential` (50 рівнів) + `level-password` замість збереження; пароль кодує і стан апгрейдів.
- Бонус-етапи — `mode`-вставка: без цегли, нескінченні вороги одного типу, гравець невразливий, лише очки.
- Приховані бонус-предмети з умовами (секрети) — `collectibles`.
- Super Bomberman: `mode-versus` (battle, до 4), `mode-coop` (кампанія вдвох, свої бомби вбивають напарника), `ai-opponent-levels` (CPU-гравці), чотиризначний пароль етапу.
- Нема undo, редактора; `pause` є.

## Варіації й родичі
- Bomber Man (1983, PC-8801/MSX) — оригінал, натхненний Pengo; Eric and the Floaters — європейська назва.
- Bomberman II (NES), Super Bomberman 1–5, Saturn Bomberman (10 гравців), Bomberman 64 (3D), Super Bomberman R / R Online (battle royale), безліч клонів (Dyna Blaster, BombSquad).
- **Осі варіацій:**
  - вибух: хрест до першої цегли / наскрізний (Pierce, SB4) / на весь ряд (Full Fire);
  - детонація: запал / дистанційна / ланцюгова;
  - бомба після постановки: нерухома / штовхається (Kick) / кидається (Glove) / б'ється кулаком (Punch);
  - кара за час: смерть / спавн сильних ворогів (Pontan) / звуження арени (падаючі стіни);
  - втрата підсилень зі смертю: усе / крім bombs+fire / розкидаються по арені (сучасний battle) (?).
  - ворог ↔ цегла: блокує / проходить крізь (Kondoria, Ovape, Pontan).

## Цікавинки для курсу
- Вибух-хрест з дальністю й зупинкою на перешкоді — 🥉: промінь з трьома типами реакції (колона гасить, цегла руйнується й гасить, бомба детонує).
- Ланцюгова детонація з чергою подій в одному тіку — 🥉: черга/BFS по бомбах, щоб уникнути рекурсії й подвійного вибуху.
- Приховане під блоком (вихід, підсилення) і кара за підрив виходу — 📎: другий шар клітини + реакція спавном.
- Таймер, що не вбиває, а «спускає собак» (Pontan) — 📎: м'яка кара замість `time-out`.
- Battle mode зі звуженням арени спіраллю — 🥈: розклад `set_cell` по спіралі + кілька гравців + CPU, що тікає з ліній вогню.
- CPU-бомбермен: оцінка небезпечних клітин (усі майбутні хрести з таймерами) і пошук безпечної — 🥇: карта загроз у часі + BFS.
- Прокляття-черепа, що передаються дотиком — 📎 за кожне, 🥉 за систему.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` (колони) · `blast-wave` (хрест на range) · `chain-detonation` · `in-round-upgrades` (bombs, fire — картка прямо про це) · `item-pickup` · `destroy-all-enemies` + `reach-exit` (двері відкриваються після зачистки) · `time-out` (у варіанті «кара») · `touch-death` · `environment-death` (власний вибух) · `random-walk` · `chase-greedy` (Pass/Pontan) · `speed-per-type` · `event-points` · `player-death` · `sequential-levels` · `temporary-modes` (Mystery) · `inventory-duration` · `spawn-points`.
- **Нема** → пропозиції карток:
  - `+destructible-blocks` «Руйновані блоки» · entities/interact · 🌱 · слот {drops: none|item|exit} — цегла, що зникає від вибуху.
  - `+hidden-under-block` «Сховане під блоком» · entities/interact · 📎 — вихід/підсилення видно лише після руйнування.
  - `+bomb-fuse` «Бомба із запалом» · entities/combat · 📎 · слоти {fuse, max_bombs} — постановка й відкладений вибух.
  - `+remote-detonation` «Дистанційний підрив» · entities/combat · 🌱 — найстаріша бомба за кнопкою.
  - `+bomb-kick` «Штовхнути бомбу ногою» · entities/legality · 📎 — бомба ковзає до упору (дитина `inertia-slide`).
  - `+bomb-throw` «Кинути бомбу» · entities/combat · 🥉 · слот {distance} — політ через перешкоди, приземлення з обгортанням (?).
  - `+shrinking-arena` «Звуження арени» · game-logic/waves · 🥉 · слот {start_at, pattern: spiral|rows} — Hurry Up.
  - `+curse-item` «Предмет-прокляття» · entities/state · 🥉 · слот {curses} — череп, передача дотиком.
  - `+timeout-punisher` «Кара за час без смерті» · game-logic/lose · 🌱 — Pontan.
  - `+permit-item` (вже запропонована в Chip's Challenge) — Wall/Bomb/Flame Pass.
  - `+level-password` (вже запропонована) — пароль з закодованим станом.
  - `+match-trophies` «Матч до N перемог у раундах» · game-logic/opponent · 🌱 · слот {wins: 1..5}.

## Пропозиції до словників
- `+effect:explode` — підрив із формою (хрест, радіус) як один ефект; зараз доводиться писати `custom` + `spawn(blast)`.
- `+effect:throw` — кинути сутність на N клітин через перешкоди (Power Glove; також snowball-ігри).
- `+trigger:blast` — клітина/сутність потрапила у вогонь вибуху; відрізняється від `contact`, бо вогонь живе кілька тіків і накриває одразу багато клітин.
- `+cond:owner_count` — кількість сутностей виду, що належать A (ліміт бомб на гравця); `count` рахує глобально.
- `+card:destructible-blocks`, `+card:hidden-under-block`, `+card:shrinking-arena`, `+card:timeout-punisher` — див. «Мапу на каталог».
- `+window:match-setup` — налаштування партії перед боєм (гравці людина/CPU, кількість перемог, арена).
- `+window:level-password` — уже в кандидатах; підтверджую другу гру.
- `+ui:player-portraits` — смуга облич гравців зі станом живий/мертвий/трофеї.
- `+feature:match-trophies` — матч із раундів до N перемог.

## Джерела
- ⭐ [Wikipedia: Bomberman (1985)](https://en.wikipedia.org/wiki/Bomberman_(1985_video_game)) — правила NES коротко: 50 рівнів, вихід під блоком, вибух по виходу кличе ворогів, таймер, 3 життя, паролі.
- [Wikipedia: Super Bomberman](https://en.wikipedia.org/wiki/Super_Bomberman) — battle mode: 1–4 гравці, 12 арен, 2 хв, Hurry Up на 1:30 зі стінами спіраллю, трофеї 1–5, нічия.
- [Take On the NES Library](https://takeontheneslibrary.com/tag/fire) — усі 8 підсилень з ефектами, таймер 200, пароль 20 літер A–P, бонус-етапи.
- [Bomberpedia: Bomberman (NES)](https://bomberpedia.shoutwiki.com/wiki/Bomberman_(NES)) — очки ворогів 100…8000, бонус-предмети, двоекранні рівні.
- [StrategyWiki: Bomberman/Gameplay](https://strategywiki.org/wiki/Bomberman/Gameplay) — детонатор на B, що втрачається зі смертю.
- [StrategyWiki: Super Bomberman 2 Power-ups](https://strategywiki.org/wiki/Super_Bomberman_2/Power-ups) — Kick, Power Glove, Remote, Bomb/Block Passer, Heart.
- [Flying Omelette: Bomberman NES](https://randomhoohaas.flyingomelette.com/bomb/nes-1/game.html) — вороги з поведінкою (бачив у пошуку, сторінка не відкрилась).
- [TCRF: Bomberman (NES)](https://www.tcrf.net/Bomberman_(NES)) — невикористаний контент.
- YouTube: пошук «bomberman nes gameplay», «super bomberman battle mode 4 players».

## Непевне
- (?) Поведінка ворогів (Onil/Dahl/Minvo повертають до гравця на спільній осі, таймери зміни напрямку 0.8–3.2 с / 0.5–2 с) — з фан-сайту через пошуковий конспект; першоджерело не відкрилось.
- (?) Скільки ворогів зʼявляється при вибуху виходу/підсилення: 8 (necretro), 4 Pontan раз на рівень (фан-ремейк) чи «до 10 на полі» — джерела розходяться.
- (?) Скільки Pontan зʼявляється після таймера: ~20 або 12.
- (?) Speed зберігається після смерті: Take On the NES — так, StrategyWiki — ні (лише Bombs і Flames).
- (?) Точна дія Power Glove у SB2 (підняти й кинути) vs SB3 (Power Bomb) vs Bomberman World (прохід крізь бомби) — назва одна, ефекти різні.
- (?) Прокляття черепа (6 с, передача дотиком) і їх список — з описів SB3, не SB1.
- (?) Розсипання підсилень по арені після смерті в battle — з памʼяті про пізні частини.
