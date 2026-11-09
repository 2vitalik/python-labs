---
title: Armagetron Advanced
slug: armagetron-advanced
aka: [Armagetron, AA, Armagetron - Multiplayer Lightcycle Game]
family: maze-arcade
also: []
klass: avatar
axes:
  field: free
  time: realtime
  opponent: online
  info: partial
  random: none
  goal: survive
year: 2001
platforms: [Windows, macOS, Linux, AmigaOS 4, OpenBSD]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Armagetron_Advanced", best: true, note: "правила, прискорення біля стін, rubber, гальмо, вибух пробиває сліди, усі режими серверів"}
  - {kind: official, url: "https://www.armagetronad.org/", note: "завантаження; боти gLATIS, що вчаться на своїх смертях; фізика налаштовується"}
  - {kind: other, url: "http://wiki.armagetronad.org/index.php?title=Glossary", note: "глосарій: rubber, grind, dig/seal, cut, wrap, holing, zone, sumo, fortress"}
  - {kind: other, url: "http://wiki.armagetronad.org/index.php?title=Playing_the_Game", note: "керування: ліворуч / праворуч / гальмо, скінченні й нескінченні стіни"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=armagetron+advanced+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-auto, no-reverse-turn, touch-death, player-death, realtime-ai, ai-opponent, online-multiplayer, simultaneous-versus, lobby-window, keyboard-controls, controls-remap, rule-variants, game-settings, player-camera, reach-exit, respawn, spawn-points, leaderboard, +trail-wall, +grinding-boost, +rubber-lag-buffer, +explosion-breach, +zone-capture-hold, +shrinking-zone, +team-modes, +flag-capture, +finite-trail, +bot-self-learning, +ball-zone-push]
proposes: ["+effect:leave_trail", "+trigger:zone_stay", "+effect:shrink_zone", "+card:rubber-lag-buffer", "+card:explosion-breach", "+card:zone-capture-hold", "+card:shrinking-zone", "+card:team-modes", "+card:finite-trail", "+card:bot-self-learning", "+card:ball-zone-push", "+ui:rubber-meter", "+ui:brake-meter", "+feature:server-physics-config"]
author: opus
date: 2026-11-09
---

# Armagetron Advanced — Tron-мотоцикли онлайн: тертися об стіни для швидкості, витрачати «гуму», брати зони командою

## Суть
Вільна 3D-реалізація Tron Light Cycles (див. `tron-light-cycles`): мотоцикли безперервно їдуть, повертають на 90°, лишають слід-стіну, зіткнення — смерть. Нове порівняно з аркадою — три фізичні ресурси (швидкість від близькості до стін, «гума» rubber, гальмо з запасом) і **зони** на арені: фортеці, які захоплюють, перебуваючи всередині; сумо-кола, що стискаються; фініш-зони для гонок і лабіринтів. Сервер задає фізику й режим, тож одна гра — це десятки варіантів правил.

## Поле і час
- Арена-площина з сіткою-розміткою і стінами по периметру; координати неперервні (не клітини), рендер 3D з камерою ззаду/зверху (?).
- Форма й розмір арени, спавни, зони — з файла мапи сервера.
- Real-time з мережевою синхронізацією; «гума» компенсує лаг.
- Стіни: нескінченні (до кінця раунду) або скінченні — хвіст зникає з довжиною (налаштування сервера).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мотоцикл гравця | player | швидкість, rubber, запас гальма, команда | безперервний рух уперед; поворот 90° (45° / без поворотів — сервер) |
| Мотоцикл суперника (людина / бот) | enemy | — | та сама фізика; боти gLATIS запамʼятовують, де загинули |
| Слід (стіна) | hazard | власник, довжина | непрохідний; дотик — смерть; близькість — прискорення |
| Стіна арени | static | — | дотик — смерть; близькість теж прискорює |
| Вибух мотоцикла | projectile | радіус | пробиває сусідні сліди — відкриває прохід |
| Зона-фортеця | zone | команда | стоїш усередині ворожої — вона «колапсує», захоплено |
| Сумо-зона | zone | радіус | повільно стискається; вигнаний назовні/колапс — вибух |
| Фініш-зона (win zone) | zone | — | доїхав першим — перемога (Race, Maze) |
| Зона смерті (death zone) | hazard | — | дотик — смерть; у режимі Shooting — снаряд-зона (?) |
| Мʼяч-зона | object | — | штовхається в зону воріт (StyBall) |
| Прапор | pickup | команда | привезти ворожий у свою зону (CTF) |
| Точка спавну | spawner | — | місце появи; у деяких режимах — відродження товаришів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(cycle, facing)`, `custom: «слід за мотоциклом стає стіною»` (`+effect:leave_trail`).
- КОЛИ `input(left|right)` → ТО `face(cycle, ±90°)` (сервер: ±45° або повороти заборонені); розворот на 180° — лише окремою привʼязкою з двох поворотів.
- КОЛИ `input(brake)` → ЯКЩО `counter(brake_reserve, >, 0)` → ТО `speed(cycle, -k)`; на серверах зі speed brake — `speed(cycle, +k)`.
- КОЛИ `in_range(cycle, wall|trail, d)` → ТО `speed(cycle, +f(d))` — що ближче, то швидше (grind).
- КОЛИ `blocked(cycle)` → ЯКЩО `counter(rubber, >, 0)` → ТО `custom: «час сповільнюється, rubber витрачається»`; інакше `disappear_a`.
- КОЛИ `tick` → ТО `counter(rubber, +regen)` — гума відновлюється рівномірно.
- КОЛИ `contact(cycle, wall|trail)` → ЯКЩО `counter(rubber, ==, 0)` → ТО `disappear_a`, `explode(radius)`.
- КОЛИ `after(explode)` → ТО `custom: «сліди поруч пробиваються — дірка»` (holing: камікадзе відкриває шлях товаришу).
- КОЛИ `custom: «скінченні стіни: слід довший за L»` → ТО `custom: «кінець сліду зникає»`.
- КОЛИ `custom: «ворог у моїй зоні-фортеці довше N»` → ТО `custom: «зона колапсує»`, команда суперника захоплює базу.
- КОЛИ `tick` (Sumo) → ТО `custom: «зона стискається»` (`+effect:shrink_zone`); КОЛИ `leave(cycle, sumo_zone)` → ЯКЩО `custom: «зона колапсувала»` → ТО `explode`.
- КОЛИ `enter(cycle, win_zone)` → ТО `win` (Race, Maze).
- КОЛИ `contact(cycle, death_zone)` → ТО `disappear_a`.
- КОЛИ `contact(cycle, ball_zone)` → ТО `push(ball_zone)`; КОЛИ `enter(ball_zone, goal_zone)` → ТО `score(team, +1)` (StyBall).
- КОЛИ `contact(cycle, enemy_flag)` → ТО `pickup`; КОЛИ `enter(carrier, own_zone)` → ТО `score(team, +1)` (CTF).
- КОЛИ `enter(dead_teammate, base)` (?) → ТО `respawn(teammate, spawn)` — відродження товаришів у деяких режимах.
- КОЛИ `counter(alive, ==, 1)` → ТО `win` для останнього (Death Match); командні — остання жива команда / захоплена база.
- Перемога: останній живий / захоплена база / фініш / прапори · Поразка: зіткнення, колапс, death zone · Рахунок: очки за вбивства й раунди на сервері (?).

## Керування і ввід
- Дві клавіші повороту відносно напрямку руху (ліворуч / праворуч) + гальмо; можна привʼязати розворот на 180°.
- Камери перемикаються (?); `~` — консоль команд.
- Split-screen для кількох гравців на одному компʼютері.

## Вікна, меню, HUD
- `main-menu`: Game (локальна гра з ботами), Network → `lobby-window` (список серверів через master server), Player setup (колір, імʼя), System setup → `settings-window` (графіка, камери, керування).
- `game-screen`: 3D-арена; HUD — `score`-таблиця гравців, `+ui:rubber-meter`, `+ui:brake-meter`, швидкість (?); сповіщення про загибелі (`message-log`).
- `custom-window`: консоль (`~`).
- Переходи: main-menu → lobby-window → game-screen (раунд за раундом); смерть → спостереження до кінця раунду (?).

## Фічі поза полем
- `online-multiplayer` через master server; `local-multiplayer` split-screen.
- `ai-opponent-levels`: боти gLATIS (з 2011) вчаться на ситуаціях, де загинули; вступний матч проти легшого бота.
- `custom-rules` / `+feature:server-physics-config`: сервер налаштовує кут поворотів, rubber, силу гальма, довжину стін, швидкість, режим і мапу.
- `mod-support`: мувіпаки (текстури, моделі), мапи XML (?); серверні скрипти читають ladderlog і шлють команди в консоль.
- Режими серверів: Fast Track, Death Match (NR/LR/MR/HR за rubber, Dog Fight), Team DM, Team Gauntlet / Wild Fortress, Rotation, Fortress, Sumo, Race, Maze, Sty Patch (Shooting, StyBall, CTF, CTFS, Flag Fortress).

## Варіації й родичі
- Tron Light Cycles (аркада 1982, див. `tron-light-cycles`) — без rubber, без зон, повільне гальмо; GLtron — інша вільна 3D-реалізація.
- Achtung, die Kurve! (див. `achtung-die-kurve`) — довільний кут і дірки в сліді.
- Snake (див. `snake`), Blockade — предки; Splix.io, Paper.io (див. `splix-io`, `paper-io`) — слід як межа території.
- **Осі варіацій:**
  - поворот: 90° / 45° / без поворотів;
  - стіни: нескінченні / скінченні;
  - швидкість: стала / grind біля стін / гальмо-прискорювач;
  - похибка: смерть миттєва / запас rubber;
  - мета: вижити / зона-фортеця / сумо / фініш / прапор / мʼяч.

## Цікавинки для курсу
- Прискорення від близькості до стіни (відстань до найближчого сегмента сліду) — 🥉: геометрія «точка — відрізок».
- Rubber як запас «помилки» з регенерацією — 📎: два лічильники (витрата при упорі, відновлення).
- Скінченні стіни: слід як черга сегментів з довжиною — 📎 (як `body-queue`).
- Захоплення зони перебуванням усередині з таймером — 🥉.
- Сумо-зона, що стискається, і вибух за межами — 📎.
- Бот, що вчиться на власних смертях (запис оточення в момент загибелі) — 👑.

## Мапа на каталог
- Є: `move-auto` · `no-reverse-turn` · `touch-death` · `player-death` · `realtime-ai` + `ai-opponent` · `online-multiplayer` + `lobby-window` · `simultaneous-versus` · `keyboard-controls` + `controls-remap` · `rule-variants` + `game-settings` (фізика сервера) · `player-camera` · `reach-exit` (win zone) · `respawn` + `spawn-points` · `leaderboard`.
- **Нема** → пропозиції карток:
  - `+trail-wall`, `+grinding-boost` (запропоновано в `tron-light-cycles`).
  - `+rubber-lag-buffer` «Запас похибки перед смертю» · entities/state · 📎 · слот {max, regen}.
  - `+explosion-breach` «Вибух пробиває сусідні стіни» · entities/combat · 📎 · слот {radius}.
  - `+zone-capture-hold` «Захоплення зони перебуванням» · game-logic/win · 🥉 · слот {time}.
  - `+shrinking-zone` «Безпечна зона стискається» · game-logic/lose · 📎 (споріднене `shrinking-arena` з Bomberman).
  - `+team-modes` «Командні режими» · game-logic/opponent · 🥈.
  - `+flag-capture` «Привези ворожий прапор» · game-logic/win · 🥉.
  - `+finite-trail` «Слід скінченної довжини» · entities/move · 📎 · слот {length}.
  - `+bot-self-learning` «Бот вчиться на своїх смертях» · game-logic/opponent · 👑.
  - `+ball-zone-push` «Штовхни мʼяч-зону у ворота» · entities/interact · 🥉.

## Пропозиції до словників
- `+effect:leave_trail` — підтверджую (Tron, Paper.io, Blockade).
- `+trigger:zone_stay` — перебування в зоні N тіків (фортеця колапсує); див. також Snake Rattle 'n' Roll.
- `+effect:shrink_zone` — зменшити зону на крок (сумо, battle royale).
- `+ui:rubber-meter`, `+ui:brake-meter` — шкали запасу гуми й гальма.
- `+feature:server-physics-config` — фізика й правила задає хост сервера, клієнт підлаштовується.
- `+card:rubber-lag-buffer`, `+card:explosion-breach`, `+card:zone-capture-hold`, `+card:shrinking-zone`, `+card:team-modes`, `+card:finite-trail`, `+card:bot-self-learning`, `+card:ball-zone-push`.

## Джерела
- ⭐ [Wikipedia: Armagetron Advanced](https://en.wikipedia.org/wiki/Armagetron_Advanced) — 2001, GPLv2+, повороти 90°/45°, прискорення біля сліду, гальмо / speed brake, rubber, вибух пробиває сліди, повний список режимів.
- [Armagetron Advanced (офіційний)](https://www.armagetronad.org/) — боти gLATIS, налаштування фізики, master server, split-screen, ladderlog-скрипти.
- [Wiki: Glossary](http://wiki.armagetronad.org/index.php?title=Glossary) — rubber (сповільнення часу біля стіни, регенерація), grind, dig/seal, cut, wrap, holing, зони (fortress, win, death), sumo, respawn.
- [Wiki: Playing the Game](http://wiki.armagetronad.org/index.php?title=Playing_the_Game) — ліворуч/праворуч/гальмо, привʼязка розвороту, консоль `~`, скінченні/нескінченні стіни.
- YouTube: пошук «armagetron advanced gameplay».

## Непевне
- (?) Шкали rubber/гальма/швидкості на HUD і перелік камер — з памʼяті, не перевірено.
- (?) Скільки часу треба бути у фортеці для колапсу, правила respawn товаришів — не знайдено.
- (?) Shooting: death zones як снаряди — з назви режиму «team death match using death zones».
- (?) Рахунок очок на сервері (за вбивство, за раунд) — не знайдено.
- (?) `info: partial` — бо 3D-камера не показує всю арену; чи є мінікарта — не перевірено.
