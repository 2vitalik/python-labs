---
title: Tron Light Cycles (Світлові мотоцикли) і нащадки
slug: tron-light-cycles
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
year: 1982
platforms: [arcade (Tron, Bally Midway), PC (Armagetron Advanced, GLtron), web (Paper.io, Splix.io), mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tron_(video_game)", best: true, note: "аркада 1982: Light Cycles серед 4 підігор, керування, AI-мотоцикли"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Light_cycle", note: "мотоцикл і слід-стіна, повороти під прямим кутом, нащадки"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Blockade_(video_game)", note: "предок 1976: слід блоками на двох"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Armagetron_Advanced", note: "grinding, brake, rubber, командні режими"}
  - {kind: official, url: "https://www.armagetronad.org/", note: "Armagetron Advanced: завантаження, боти, сервери"}
  - {kind: play, url: "https://splix.io/", note: "клітинний «territory» нащадок у браузері"}
  - {kind: official, url: "https://voodoo.io/paper2", note: "Paper.io 2 (Voodoo)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tron+arcade+1982+light+cycles+gameplay", note: "пошук; аркада"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=paper.io+gameplay", note: "пошук; Paper.io"}
stage: v1
coverage: 70
mechanics: [move-auto, realtime-ai, touch-death, impassable-cells, ai-opponent, ai-greedy, player-death, progress-acceleration, keyboard-controls, leaderboard, event-points, +trail-wall, +no-reverse-turn, +grinding-boost, +territory-capture, +region-fill, +trail-vulnerable, +simultaneous-versus]
proposes: ["+effect:leave_trail", "+effect:clear_trail", "+trigger:return_home", "+card:trail-wall", "+card:territory-capture", "+card:grinding-boost", "+role:zone", "+axis:control", "+ui:territory-percent"]
author: opus
date: 2026-11-02
---

# Tron Light Cycles — мотоцикл не зупиняється, слід стає стіною, переживи суперника

## Суть
Кожен мотоцикл безупинно їде вперед і лишає за собою слід, який до кінця раунду працює як стіна; гравець лише повертає на 90°. Мета — змусити суперника врізатися в стіну арени, свій чи чужий слід, і не врізатися самому, тому поле поступово заповнюється лабіринтом, який гравці будують одне одному. Сучасні .io-нащадки (Paper.io, Splix.io) перевернули ідею: слід — це межа нової території, а вразливий він лише поки не замкнений.

## Поле і час
- Аркада: прямокутна арена-сітка, стіни по периметру; гравець (синій) проти кількох жовтих AI-мотоциклів.
- Real-time: кожен тік усі мотоцикли роблять крок; слід займає пройдені клітини назавжди (до смерті власника).
- Armagetron: 3D-рендер того самого поля, швидкість безперервна, може зростати (grinding), сервери можуть дозволяти повороти на 45°.
- Splix.io: клітинна мапа 500×500 або 600×600 блоків, 60–90 гравців у лобі; Paper.io — вільний рух (Paper.io 2) (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мотоцикл гравця | player | напрям, швидкість | щотік крок уперед; поворот ліворуч/праворуч на 90°; гальмо (аркада: курок сповільнює) |
| AI-мотоцикл | enemy | напрям, швидкість | та сама фізика; намагається відрізати й вижити |
| Слід (jetwall) | static | власник | клітина, яку пройшов мотоцикл; дотик — смерть; зникає разом із власником |
| Стіна арени | static | — | дотик — смерть |
| Територія (Paper.io/Splix) | zone | власник, площа | безпечна зона власника; на ній слід не лишається |
| Слід поза територією (Paper.io/Splix) | hazard | власник | вразливий: хто перетне — вбиває власника |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(cycle, dir)`, `custom: «попередня клітина стає слідом власника»`.
- КОЛИ `input(turn_left|turn_right)` → ТО `face(cycle, ±90°)`; розворот на 180° неможливий (тільки два повороти).
- КОЛИ `contact(cycle, wall|trail)` → ТО `disappear_a`, `custom: «слід загиблого зникає»`; (Armagetron: вибух ще й пробиває сусідні сліди).
- КОЛИ `contact(cycle_a, cycle_b)` (лоб у лоб) → ТО обидва гинуть.
- КОЛИ `count(enemy_cycles, ==, 0)` → ТО `win` раунду (аркада: перехід до вибору наступної підгри); КОЛИ гине гравець → `lives(-1)`.
- КОЛИ `input(brake)` → ТО `speed(cycle, -k)` (аркада — курок сповільнює; Armagetron — гальмо з обмеженим запасом, на деяких серверах — прискорювач).
- КОЛИ `in_range(cycle, trail, d)` (Armagetron) → ТО `speed(cycle, +f(d))` — grinding: що ближче до чужого/свого сліду, то швидше.
- Armagetron rubber: КОЛИ `blocked(cycle)` → ЯКЩО `counter(rubber, >, 0)` → ТО `custom: «мить затримки замість смерті, витрачає rubber»` — компенсація лагу.
- Blockade: КОЛИ `contact(arrow, wall|trail)` → ТО `score(+1)` суперникові; гра до 3–6 зіткнень (налаштування оператора).
- Paper.io/Splix (?): КОЛИ `leave(player, own_territory)` → ТО починає лишати вразливий слід.
- КОЛИ `enter(player, own_territory)` зі слідом → ТО `fill(region)` — `custom: «замкнена слідом і територією область (разом із чужою землею) стає своєю»`, слід → територія.
- КОЛИ `contact(other, trail_of(player))` → ТО гине `player` (власник сліду), вбивця `score(+500)` (Splix).
- КОЛИ `contact(player, own_trail)` → ТО `lose` (?).
- КОЛИ `died(player)` → ТО `custom: «уся територія власника стає нічиєю»` (?).
- Splix: КОЛИ `input(pause)` → ТО `freeze(player)`; замороженого можна вбити навіть на його землі.
- Перемога: останній живий (аркада, Armagetron DM) / найбільший % території (Paper.io) / рейтинг серверу (Splix). Поразка: зіткнення. Рахунок: Splix — блоки, вбивства, ранг.

## Керування і ввід
- Аркада Tron: 8-напрямний джойстик (у Light Cycles — лише повороти) + курок, що сповільнює мотоцикл; єдина підгра без крутилки-прицілу.
- Armagetron: дві клавіші «ліворуч/праворуч» відносно напрямку руху + гальмо; камера ззаду/зверху.
- Splix.io: стрілки/WASD — абсолютний напрям; утримання однієї й натискання другої запамʼятовує напрям; P — пауза-заморозка.
- Paper.io: свайп/палець задає напрям (?).

## Вікна, меню, HUD
- Аркада: `custom-window` «вибір підгри» (4 сектори: Light Cycles, I/O Tower, MCP Cone, Battle Tanks) → `game-screen` (арена, `score`, `lives`) → назад до вибору.
- `leaderboard` (аркада — ініціали рекордсменів).
- Armagetron: `main-menu` (Game, Network → `lobby-window` зі списком серверів, Player setup, System setup → `settings-window` фізики й камер), `game-screen` з `minimap`, `score`-таблицею гравців.
- Splix.io / Paper.io: `main-menu` з полем імені, `skin-select`, `game-screen` з `minimap`, `leaderboard` серверу, `territory-percent` (Paper.io) (?); `end-screen` з Kills / Blocks captured / Score / Rank (Splix).
- Переходи: main-menu → game-screen → (смерть) end-screen → main-menu.

## Фічі поза полем
- `ai-opponent-levels` (кількість/сила AI у Armagetron; боти gLATIS вчаться на власних смертях), `online-multiplayer` (сервери Armagetron, лобі .io), `local-multiplayer` split-screen (Armagetron (?)).
- `custom-rules` — сервери Armagetron задають фізику: повороти 45°, сила гальма, rubber, швидкість стін, режими (Team DM, Fortress, Sumo, Race, Maze, CTF).
- `custom-skins` (.io), `leaderboard-online`.

## Варіації й родичі
- Blockade (1976) → Surround (Atari 2600) → Tron Light Cycles (1982) → GLtron, Armagetron Advanced (вільні 3D-реалізації) → Paper.io (2016), Paper.io 2 (2018), Splix.io (territory).
- Snake — той самий рух, але хвіст рухається (див. `snake`); Xonix/Qix — відрізання території сітким слідом проти ворогів (див. `xonix`).
- **Осі варіацій:**
  - слід: вічний (Tron) / зникає з часом або з довжиною (деякі клони) (?) / стає територією після повернення (Paper.io);
  - повороти: 90° / 45° / вільні (Tron: Legacy, Paper.io 2);
  - швидкість: стала / гальмо / grinding біля стін;
  - зіткнення: миттєва смерть / rubber-допуск;
  - мета: останній живий / площа / очки за вбивства.

## Цікавинки для курсу
- Слід = стіна, що росте щотік (масив власників клітин) — 🌱: найпростіша real-time гра на двох.
- AI, що виживає: «рахувати вільну площу після кожного з 3 ходів» (flood fill) і йти туди, де її більше — 🥇: картка `realtime-ai` прямо про це.
- Розділення поля голосуванням Вороного (хто ближче до клітини) як евристика AI — 👑: класика змагань з ботів для Tron.
- Grinding — швидкість як функція відстані до стін — 🥉: оцінка відстані щотік.
- Захоплення території: замкнути контур і залити область, яка не містить ворогів/яка відрізана від «зовні» — 🥈 (flood fill з кількома власниками).
- Вразливий слід: перетин чужого сліду вбиває власника, а не того, хто перетнув — 📎: інверсія `touch-death`.

## Мапа на каталог
- Є: `move-auto` · `realtime-ai` («Виживання проти Tron-змійки» — дослівно ця гра) · `touch-death` · `impassable-cells` · `ai-opponent` / `ai-greedy` · `player-death` · `progress-acceleration` · `keyboard-controls` · `leaderboard` · `event-points`.
- **Нема** → пропозиції карток:
  - `+trail-wall` «Слід стає стіною» · entities/move · 🌱 · слот {lifetime: forever|n_ticks}.
  - `+no-reverse-turn` (запропоновано в `snake`).
  - `+grinding-boost` «Прискорення біля стін» · entities/state · 🥉.
  - `+territory-capture` «Захоплення території контуром» · game-logic/win · 🥈 · слот {owners: 1|n}.
  - `+region-fill` «Заливка замкненої області» · entities/interact · 🥉 — спільна з Xonix.
  - `+trail-vulnerable` «Вразливий незамкнений слід» · entities/death · 📎.
  - `+simultaneous-versus` (запропоновано в `snake`).

## Пропозиції до словників
- `+effect:leave_trail` — клітина, з якої пішла сутність, стає її слідом (Tron, Xonix, Paper.io).
- `+effect:clear_trail` — прибрати всі клітини сліду сутності (смерть у Tron, замикання в Paper.io).
- `+trigger:return_home` — сутність повернулась на свою територію/сушу зі слідом (запуск заливки); можна `enter(a, own_zone)`, але умова «є слід» важлива.
- `+card:trail-wall`, `+card:territory-capture`, `+card:grinding-boost`.
- `+role:zone` — уже кандидат; підтверджую: територія з власником.
- `+ui:territory-percent` — частка поля у власника (Paper.io, Qix, Xonix).
- `+axis:control` — Armagetron: `direct-relative` (ліво/право від напрямку), Splix: `direct-absolute`.

## Джерела
- ⭐ [Wikipedia: Tron (video game)](https://en.wikipedia.org/wiki/Tron_(video_game)) — Light Cycles: синій гравець проти жовтих AI, змусити врізатися у стіни/сліди/одне одного; курок сповільнює; підгра без крутилки.
- [Wikipedia: Light cycle](https://en.wikipedia.org/wiki/Light_cycle) — слід як стіна, лише прямі кути, нащадки (Armagetron, GLtron).
- [Wikipedia: Blockade](https://en.wikipedia.org/wiki/Blockade_(video_game)) — двоє гравців, слід блоками, 3–6 зіткнень.
- [Wikipedia: Armagetron Advanced](https://en.wikipedia.org/wiki/Armagetron_Advanced) — grinding, brake, rubber, 45°-повороти на серверах, режими.
- [armagetronad.org](https://www.armagetronad.org/) — офіційний сайт, боти gLATIS, платформи (Steam як Retrocycles).
- [Splix.io](https://splix.io/) — грати; changelog: заморозка, +500 за вбивство, мапи 600×600.
- [Voodoo: Paper.io 2](https://voodoo.io/paper2) — офіційна сторінка (правил не містить).
- YouTube: пошук «tron arcade 1982 light cycles gameplay», «paper.io gameplay».

## Непевне
- (?) Правила Paper.io (слід поза своєю землею, замикання заливає область разом із чужою землею, смерть від власного сліду, вся земля загиблого стає нічиєю) — з памʼяті; офіційні сторінки правил не мають, пошуковий ліміт вичерпано.
- (?) Кількість AI-мотоциклів у аркаді по рівнях і чи прискорюються вони — Wikipedia не вказує.
- (?) Split-screen у Armagetron — не підтверджено на сторінках.
- (?) Клони, де слід зникає з часом, — як вісь варіацій, без конкретного підтвердженого прикладу.
