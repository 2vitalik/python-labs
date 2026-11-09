---
title: Captive
slug: captive
aka: [Captive (1990), Каптив]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: setup
  goal: state
year: 1990
platforms: [Amiga, Atari ST, MS-DOS (1992)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Captive_(video_game)", best: true, note: "4 дроїди з брифкейса, 6 змінних частин тіла, 10 баз + станція, генератори й втеча, 65 535 рівнів з одного seed"}
  - {kind: other, url: "https://captive.atari.org/", note: "Ultimate Captive Guide: інтерфейс, частини, навички, стіни, двері, крамниці, вороги, генератор мап"}
  - {kind: other, url: "https://captive.atari.org/Technical/MapGen/Introduction.php", note: "seed = (місія−1)·11 + база, мапа 64×32 по байту, поверхи — області однієї мапи, 30 кроків"}
  - {kind: other, url: "https://captive.atari.org/Environment/Walls/Walls.php", note: "усі типи стін: піднімні, штовхані, фальшиві, панелі, головоломки, ґрати, розетки"}
  - {kind: other, url: "https://captive.atari.org/Environment/Encounters/Encounters.php", note: "34 типи ворогів у базах, групи до 9, переслідування по сліду з 7 клітин"}
  - {kind: other, url: "https://crpgaddict.blogspot.com/2014/08/game-156-captive-1990.html", note: "CRPG Addict: перші враження, розетки, двері-пастки, динаміт і вибух бази"}
  - {kind: other, url: "https://crpgaddict.blogspot.com/2014/09/captive-final-rating.html", note: "CRPG Addict: підсумок — зброя, оптика, тактики середовища, 256 місій на PC"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Captive+Amiga+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, orientation-state, impassable-cells, push-object, button-toggle, key-and-door, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, unit-xp-skills, melee-vs-ranged, projectile-shot, chase-player, round-currency, shop-catalog, shop-buyback, shop-window, ladder-climb, floor-types, player-death, save-game, seed-share, dungeon-generation, map-window, gui-render, player-camera, +first-person-grid, +party-formation, +drone-control, +body-parts-composition, +armor-per-part, +limb-disable, +breakdown-repair, +skill-unlock-chain, +electric-socket-charge, +raiser-wall-crush, +grate-trap, +combination-door, +password-terminal, +remote-camera, +mine-drop-on-death, +water-flood-stun, +escape-countdown, +probe-reveals-next, +mission-loop, +seeded-generator, +encumbrance-slowdown]
proposes: ["+trigger:generators_destroyed", "+cond:skill(a, s, op, n)", "+cond:part_health(a, part, op, n)", "+effect:repair(a, part)", "+effect:charge(hand)", "+effect:collapse_base", "+role:party-member", "+role:remote-camera", "+window:holamap", "+window:shop-dialog", "+window:skills-screen", "+ui:monitor-bank", "+ui:hand-slots", "+ui:droid-power-bars", "+feature:base-seed", "+card:remote-camera", "+card:electric-socket-charge"]
author: opus
date: 2026-11-09
---

# Captive — керуй чотирма дроїдами з брифкейса: розбирай бази на планетах, підривай генератори й тікай

## Суть
Вʼязень Трилл, що прокинувся в камері з брифкейс-компʼютером, дистанційно веде загін із **чотирьох дроїдів** клітинними базами в стилі Dungeon Master: real-time, від першої особи, крок/поворот. Дроїд — не герой, а **збірка з шести частин** (голова, груди, руки, кисті, ноги, ступні), кожна з власним здоровʼям, захистом і споживанням струму; частини купують, ремонтують і міняють у крамницях. У кожній базі треба знайти космічний зонд (вказує наступну базу), підірвати генератори силового поля й **встигнути вибратися**, поки база руйнується. Усі бази — з одного числа-seed, тож їх 65 535 без збереження на диску.

## Поле і час
- База = плоска мапа **64×32 клітини** (2048 байт, байт на клітину); поверхи — окремі області цієї мапи, розділені стінами; ліфт чи драбина переносять в іншу область, а не «вниз» тієї самої.
- Вигляд — від першої особи, рух по клітинах з орієнтацією; у клітині до 9 позицій для групи ворогів; влучання — ліворуч/центр/праворуч і на двох висотах.
- Поза базою — планета: суходіл, вода, евергріни, вхід у базу 3×3 з ірис-дверима, динозаври; над усім — векторна космічна мапа (Holamap): 49 планет, 150 місяців, 1 станція.
- Real-time: вороги мають власну швидкість, задану при генерації; кнопка сну пришвидшує час.
- Seed бази = (місія − 1) · 11 + номер бази; генератор детермінований і однаковий на Atari, Amiga й PC.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Загін дроїдів | player | 4 дроїди: 2 спереду, 2 ззаду; орієнтація | рухається як одна фігура |
| Дроїд | ally | DEX, VIT, WIS (від імені), навички, струм, 6 частин | передні бʼють флангами ліворуч/праворуч, задні — лише стріляють по центру |
| Частина тіла | object | тип (Human … Titaniux, 10 типів, 71 частина), Armature, Agility, Health, Drainage | захищає; на 0 — непридатна; потрібен рівень навички Robotics |
| Голова лідера | object | здоровʼя | < 1/3 — видно лише кожен другий рядок, 0 — нема огляду |
| Стіна | static | — | непрохідна |
| Стіна з кульками | object | — | штовхається вперед; можна заблокувати прохід назавжди |
| Піднімна стіна (raiser) | gate | до 4 відкритих | закривається сама; чавить ×4, нищить предмети під собою; кнопка або постріл |
| Фальшива стіна | static | — | прохідна; оптика Vision Correction її ховає |
| Стіна з панеллю | container | — | ховає предмет або випускає засідку |
| Стіна з отвором | gate | — | відкриває віконце для пострілів |
| Стіна з важелем (1 або 3) | switch | інколи одноразовий | відчиняє стіну, двері, гасить вогонь; 3 важелі — комбінація |
| Стіна-головоломка (смуги / кнопки) | gate | код із clipboard | відчиняється, коли відтворено комбінацію |
| Ґрати-пастка | hazard | — | ступив — за спиною закривається стіна; прихована цеглина відчиняє |
| Розетка | terrain | — | заряджає руку (постріли струмом), груди дроїда, батарею; інше вибухає |
| Невидимий барʼєр | static | — | зникає від будь-якого влучання |
| Двері з кнопкою · ліфтові · пробивні · сині | gate | — | кнопка; виклик ліфта; пробити удар/постріл; сині відбивають снаряди й зачиняються самі |
| Ірис-двері | gate | 4 кнопки по кутах, 24 послідовності | код з послання або кубика-підказки |
| Лазерні двері | gate | пароль | пароль від «двірника» або термінала |
| Двері Трилла | gate | одні на місію | як ірис, без підказки кубиком |
| Драбина · ліфт | static | ≤ 25 ліфтів (5 шахт по 5) | вгору/вниз; драбина чавить ворога, якщо сусідня клітина зайнята |
| Вода | hazard | — | у базі 8 шкоди на дроїда, зовні — 7 × 20; стікає в отвори на нижні поверхи; паралізує роботів |
| Вогонь | hazard | — | шкода; літаючі пролітають; батарея у вогні → 23 % заряду |
| Міна | hazard | — | лишається після деяких ворогів; детонують снаряди |
| Генератор | object | у кімнаті ≥ 3×3 | підірвати динамітом → розетки гаснуть, база руйнується |
| Крамниця | neutral | 5 дій | купити, продати, полагодити предмет, полагодити дроїда; мішок грошей — у праву руку продавця |
| Термінал | static | пароль | відкриває карти рівня («Map Basic») або закриває лазерні двері |
| Космічний зонд | pickup | ≤ 2 на базу | показує на Holamap наступну базу |
| Clipboard · послання від Ratt | pickup | — | паролі й коди; продаються за гроші |
| Камера | object | ≤ 4 | кидається вперед, керується дистанційно, показ на 5-му моніторі, може вибухнути |
| Ворог бази | enemy | 34 типи; група до 9; швидкість; Floating | блукає, з 7 клітин на одній осі йде слідом; частина стріляє, частина лишає міну |
| Динозавр | enemy | 5 типів, поза базою | респавниться |
| Трилл | neutral | на космічній станції | звільнити → кінець, або знову в полон → нова місія |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(forward|back|strafe)` → ЯКЩО `free(cell)` → ТО `move(party, dir)`; інакше `block`.
- КОЛИ `input(turn)` → ТО `face(party, ±90°)`; `input(climb)` → ЯКЩО `cell(here, ladder)` → ТО `custom: «на інший поверх»`.
- КОЛИ `input(push)` → ЯКЩО `cell(ahead, ball_wall)` → ТО `push`; інакше `block`.
- КОЛИ `input(hand)` → ЯКЩО `custom: «дроїд спереду або зброя дистанційна»` and `not custom: «рука на перезарядці»` → ТО `custom: «атака предметом у руці; порожня рука — удар кулаком»`, `damage(n)`.
- КОЛИ `custom: «ворог на лівому фланзі»` → ЯКЩО `custom: «атакує правий дроїд»` → ТО `block`.
- КОЛИ `died(enemy)` → ТО `counter(xp, +n)` усім чотирьом, `score(+1)`, інколи `spawn(mine)`, `spawn(gold)`.
- КОЛИ `custom: «зброя вжита / завдано / отримано шкоду / крок»` → ТО `counter(xp, +n)`.
- КОЛИ `input(click skill)` → ЯКЩО `counter(xp, >=, cost)` → ТО `custom: «XP → +1 до навички»`, `custom: «+1 до випадкового з DEX/VIT/WIS»`.
- КОЛИ `counter(skill_k, >=, 9)` → ТО `unlock(skill_k+1)` (Robotics, Brawling → Swords → Handguns → Rifles → Automatics → Lasers → Cannons → Sprayguns).
- КОЛИ `contact(enemy_hit, part)` → ЯКЩО `custom: «частина вимагає більше Robotics, ніж у дроїда»` → ТО `damage(×2)`, `custom: «наче VIT = 2»`.
- КОЛИ `counter(part_health, ==, 0)` → ТО `set_state(part, useless)`; ліва рука лідера → `custom: «кидати не можна»`.
- КОЛИ `custom: «вага понад межу»` → ТО `speed(party, ÷2 | ÷3 | ÷4)` за перевищенням 50 / 100 / більше кг.
- КОЛИ `contact(hand, socket)` → ТО `set_state(hand, charged)`; ЯКЩО `input(throw charge)` → ТО `custom: «постріл струмом»`; ЯКЩО `contact(charged hand, other item)` → ТО `disappear(item)`.
- КОЛИ `input(put droid|battery on socket)` → ТО `custom: «перезарядка»`; КОЛИ `contact(other item, socket)` → ТО `explode`.
- КОЛИ `input(button|shot)` → ЯКЩО `cell(target, raiser_wall)` → ТО `custom: «стіна піднялась»`; КОЛИ `timer(close)` → ТО `custom: «стіна опустилась»`, `damage(×4)` тому, хто під нею, `disappear(items under)`.
- КОЛИ `enter(party, grate_trap)` → ТО `set_cell(behind, wall)`; КОЛИ `input(hidden brick)` → ТО `set_cell(behind, floor)`.
- КОЛИ `input(panel)` → ТО `reveal(item)` або `spawn_at(enemies, nearby wall)`.
- КОЛИ `input(iris buttons)` → ЯКЩО `custom: «послідовність збігається з однією з 24»` → ТО `custom: «двері відчинено»`; натиснути знову → зачиняються.
- КОЛИ `input(password)` → ЯКЩО `has(party, clipboard_code)` → ТО `custom: «лазерні двері / термінал відчинено»`.
- КОЛИ `enter(party, water)` → ТО `damage(droids, 8)` у базі, `damage(droids, 7 × 20)` поза базою.
- КОЛИ `custom: «вода в клітині з отвором»` → ТО `custom: «вода стікає на нижній поверх»`; ЯКЩО `occupied(cell, robot enemy)` → ТО `stun(enemy, n)`.
- КОЛИ `in_range(enemy, party, 7)` → ЯКЩО `custom: «на одній осі»` → ТО `custom: «ворог іде слідом по сліду загону»`; інакше `custom: «блукає»`.
- КОЛИ `input(drop camera)` → ТО `place(party, camera)` у клітину попереду; `input(camera move)` → `move(camera, dir)`; `input(red X)` → ЯКЩО `custom: «DEX лідера ≥ 15»` → ТО `explode`.
- КОЛИ `custom: «двері зачиняються на камеру»` → ТО `disappear(camera)`.
- КОЛИ `custom: «динаміт біля генератора»` → ТО `disappear(generator)`, `custom: «розетки бази більше не працюють»`.
- КОЛИ `custom: «усі генератори бази знищено»` → ТО `timer(start)`, `custom: «база руйнується»` (`+trigger:generators_destroyed`).
- КОЛИ `counter(collapse_timer, ==, 0)` → ЯКЩО `not reach(party, lander)` → ТО `lose` (загін гине з базою).
- КОЛИ `picked(party, probe)` → ТО `custom: «на Holamap зʼявляється наступна база»`.
- КОЛИ `input(Orbit|Land)` → ЯКЩО `custom: «ціль на точці планети»` → ТО `teleport(party, planet)`; влучив у воду → `damage`.
- КОЛИ `custom: «знищено всі 10 баз місії»` → ТО `custom: «силове поле станції знято»`.
- КОЛИ `contact(party, Trill)` → ТО `choose(звільнити → win | лишити → нова місія)`.
- КОЛИ `input(shop)` → ЯКЩО `has(shopkeeper right hand, money_bag)` → ТО `choose(buy | sell | fix item | fix droid | leave)`; продаж нетипового — 50 %, ремонт нетипового — ×2.
- КОЛИ `input(sleep)` → ТО `custom: «час іде швидше; струм не витрачається, якщо пристрої вимкнено»`.
- КОЛИ `custom: «усі дроїди розбиті»` → ТО `lose` → завантаження збереження.
- Перемога: звільнити Трилла (або грати далі — до 65 535 баз). Поразка: загін знищено / не встиг з бази. Рахунок: 1 очко за кожного вбитого ворога.

## Керування і ввід
- Права панель: 8 кнопок руху (вперед, назад, крок убік, повороти, драбина вгору/вниз); на клавіатурі — Keypad 8/2/4/6/7/9/1/3; штовхнути — правий клік на «вперед» або Shift-8.
- Атака — клік по іконці руки дроїда (лише мишею); лівий клік — зняти предмет у «повітря», правий — вжити.
- Розетка, панелі, кнопки, крамниця — клік рукою-курсором у головному виді.
- Космос: ціль на векторній мапі, зум, Orbit, Land.

## Вікна, меню, HUD
- `game-screen`: вид від першої особи; праворуч — кнопки руху, стан і струм кожного дроїда (`+ui:droid-power-bars`), руки (`+ui:hand-slots`, як у DM); угорі — **5 моніторів** (`+ui:monitor-bank`): 1–4 — оптика й девайс кожного дроїда, 5 — камери.
- Клік по смузі дроїда → `skills-screen` (`+window:skills-screen`): навички й перенесення XP; правий клік → `inventory-window` і стан частин.
- `holamap` (`+window:holamap`): векторна мапа космосу з кораблем, зондами, планетами, станцією; лічильник знищених баз.
- `shop-dialog` (`+window:shop-dialog`): продавець з двома руками, 5 пунктів меню.
- Пульт (remote): кнопки девайсів і камери; Disk — `save-slots`; Sleep & Pause; Preferences — `settings-window`.
- Переходи: камера Трилла → Holamap → посадка → планета → база → (генератори) → втеча до посадкового модуля → Holamap.

## Фічі поза полем
- `save-game` на диск (Disk у пульті); активна завжди лише одна база.
- `+feature:base-seed`: номер бази однозначно задає мапу — відтворюється на всіх платформах.
- Нескінченні місії: на Atari/Amiga застрягає на базі 1 місії 2316, на PC після 256 місій — знову перша.
- `pause` і сон-пришвидшення; налаштування.

## Варіації й родичі
- Сиквел: Liberation: Captive 2 (1993, CD32) — не досліджено.
- Родичі: [dungeon-master](dungeon-master.md) (той самий real-time клітинний вид, руки-слоти), [eye-of-the-beholder](eye-of-the-beholder.md), [legend-of-grimrock](legend-of-grimrock.md), [bloodwych](bloodwych.md), [cogmind](cogmind.md) (робот зі змінних частин, але покроково).
- Осі варіацій: **герої** (люди / дроїди-збірки з частин) · **підземелля** (ручне / генероване з seed) · **кінець бази** (вийти сходами / таймер після підриву) · **огляд** (свої очі / дистанційна камера).

## Цікавинки для курсу
- Генератор баз з одного seed: `(місія − 1)·11 + база` → детермінований ГВЧ → мапа 64×32 за 30 кроків — 🥇.
- Дроїд як набір частин зі здоровʼям кожної; поломка голови псує рендер — 🥉.
- Розетка-заряд: рука стає зброєю, торкнешся предмета — знищиш — 🌱.
- Дистанційна камера: окремий вʼюпорт, що рухається поза загоном і може вибухнути — 🥉.
- Ланцюг навичок: наступна відкривається на 9 рівні попередньої; XP витрачаєш сам — 📎.
- Таймер втечі після підриву генераторів + вимкнені розетки — 🌱.
- Вода як рідина: стікає в отвори на нижні поверхи й паралізує роботів — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `orientation-state` · `impassable-cells` · `push-object` (стіни з кульками) · `button-toggle` (кнопки, важелі) · `key-and-door` (паролі й коди як ключі) · `hp-damage` · `inventory` / `inventory-items` / `inventory-limit` (вага) · `item-pickup` · `unit-xp-skills` · `melee-vs-ranged` (фронт / тил) · `projectile-shot` · `chase-player` · `round-currency` · `shop-catalog` / `shop-buyback` / `shop-window` · `ladder-climb` · `floor-types` (вода, вогонь, ґрати) · `player-death` · `save-game` · `seed-share` · `dungeon-generation` · `map-window` (Holamap) · `gui-render` · `player-camera`.
- Вже пропоновані: `+first-person-grid` · `+party-formation` (як у DM) · `+drone-control` · `+body-parts-composition` · `+armor-per-part` · `+limb-disable` · `+breakdown-repair` · `+seeded-generator`.
- **Нема** → пропозиції карток:
  - `+skill-unlock-chain` «Навичка відкривається на N рівні попередньої» · entities/state · 📎.
  - `+electric-socket-charge` «Розетка заряджає руку для пострілу; дотик заряду нищить предмет» · entities/interact · 🌱.
  - `+raiser-wall-crush` «Стіна, що опускається сама, чавить і нищить предмети» · entities/interact · 📎.
  - `+grate-trap` «Ступив — за спиною виросла стіна» · entities/interact · 🌱.
  - `+combination-door` «Двері з кнопок: одна з 24 послідовностей» · entities/interact · 🌱.
  - `+password-terminal` «Термінал з паролем із знайденої записки» · entities/interact · 🌱.
  - `+remote-camera` «Дистанційна камера з окремим вʼюпортом» · interface/render · 🥉.
  - `+mine-drop-on-death` «Ворог лишає міну» · entities/spawn · 🌱.
  - `+water-flood-stun` «Вода стікає вниз і паралізує роботів» · entities/interact · 🥈.
  - `+escape-countdown` (як у Sword of Fargoal) · `+probe-reveals-next` «Знахідка відкриває наступну ціль на мапі» · levels/progression · 🌱.
  - `+mission-loop` «Після фіналу — нова місія з наступних seed-ів» · levels/progression · 🌱.
  - `+encumbrance-slowdown` «Перевага ваги ділить швидкість загону» · entities/state · 🌱.

## Пропозиції до словників
- `+trigger:generators_destroyed` — знищено всі генератори бази.
- `+cond:skill(a, s, op, n)` — рівень навички дроїда (доступ до частин і зброї).
- `+cond:part_health(a, part, op, n)` — здоровʼя частини тіла.
- `+effect:repair(a, part)` — ремонт у крамниці · `+effect:charge(hand)` — зарядити руку · `+effect:collapse_base` — база руйнується.
- `+role:party-member` (як у DM) · `+role:remote-camera` — сутність-«око» гравця поза аватаром.
- `+window:holamap` — векторна мапа космосу · `+window:shop-dialog` · `+window:skills-screen`.
- `+ui:monitor-bank` — ряд моніторів пристроїв · `+ui:hand-slots` (як у DM) · `+ui:droid-power-bars`.
- `+feature:base-seed` — номер рівня = seed.
- `+card:remote-camera` · `+card:electric-socket-charge`.

## Джерела
- ⭐ [Wikipedia: Captive (video game)](https://en.wikipedia.org/wiki/Captive_(video_game)) — Трилл і брифкейс, 4 дроїди, корабель і посадка, 10 баз + станція, зонди, генератори, втеча до обвалу, 6 змінних частин, оптика й девайси, фронт/тил у бою, вода паралізує роботів, seed і 65 535 рівнів.
- [Ultimate Captive Guide](https://captive.atari.org/) — фан-довідник: [генератор мап](https://captive.atari.org/Technical/MapGen/Introduction.php) (seed, 64×32, поверхи-області), [частини дроїда](https://captive.atari.org/Droids/DroidParts/DroidParts.php) (10 типів, 71 частина, вага), [навички](https://captive.atari.org/Droids/Skills.php) (ланцюг, ціни XP), [монітори](https://captive.atari.org/Interface/Monitors.php), [рух](https://captive.atari.org/Interface/Movements.php), [стіни](https://captive.atari.org/Environment/Walls/Walls.php), [двері](https://captive.atari.org/Environment/Doors/Doors.php), [крамниці](https://captive.atari.org/Environment/Shops/Shops.php), [вороги](https://captive.atari.org/Environment/Encounters/Encounters.php), [камера](https://captive.atari.org/Tools/Camera/Camera.php), [FAQ](https://captive.atari.org/Miscellaneous/FAQ/FAQ.php), [поради](https://captive.atari.org/Miscellaneous/TipsTricks.php), [чи знали ви](https://captive.atari.org/Miscellaneous/DidYouKnow/DidYouKnow.php).
- [CRPG Addict: Game 156: Captive](https://crpgaddict.blogspot.com/2014/08/game-156-captive-1990.html) — імена → атрибути, панелі, розетки, крамниці, кодові двері, динаміт → вибух бази.
- [CRPG Addict: Captive: Final Rating](https://crpgaddict.blogspot.com/2014/09/captive-final-rating.html) — класи зброї, оптика «AG Scan», тактики середовища (двері, міни, потоп), закрита економіка, 256 місій на PC.

## Непевне
- (?) Тривалість таймера обвалу бази після підриву генераторів — жодне джерело не дає числа.
- (?) Кількість генераторів на базу (комент CRPG Addict: «10 генераторів, щоб звільнити Трилла» — ймовірно, по одному на базу).
- (?) Чи смерть одного дроїда остаточна і як його відновити (крім «Fix Player» у крамниці) — не знайшов.
- (?) Як саме імʼя дроїда задає DEX/VIT/WIS — лише «імʼя визначає атрибути».
- (?) Анти-грав «ходити по стелі» і задні дроїди стріляють крізь отвір — з CRPG Addict і сторінки стін, механіку висоти не перевірив.
- (?) Liberation: Captive 2 — відмінностей не досліджував.
