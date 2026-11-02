---
title: Frozen Synapse
slug: frozen-synapse
family: tactics
also: [program-robots]
klass: figure
axes:
  field: free
  time: wego
  opponent: online
  info: hidden
  random: setup
  goal: state
year: 2011
platforms: [Windows, Mac, Linux, iPad, Android, iOS, "PS Vita/PS3 (Frozen Synapse Prime)"]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Frozen_Synapse", best: true, note: "одночасні ходи, ~5 с симуляції, вейпоінти/стійка/напрям, детермінований бій, light/dark режими, процедурні карти, режими"}
  - {kind: steam, url: "https://store.steampowered.com/app/98200/Frozen_Synapse/", note: "кнопка Prime, 5 мультиплеєрних режимів (Secure з торгами, Hostage), 55 місій, генератор сутичок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=frozen+synapse+gameplay+tutorial", note: "пошук; розбір планування"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=frozen+synapse", note: "пошук; Frozen Synapse 2, Prime"}
stage: v1
coverage: 55
mechanics: [+line-of-sight-attack, melee-vs-ranged, projectile-shot, blast-wave, impassable-cells, +destructible-blocks, +path-preview, replay, ai-opponent, destroy-all-enemies, reach-exit, game-screen, main-menu, end-screen, level-select, +wego-turns, +action-queue, +cover-system, +fog-of-war, +enemy-plan-sandbox, +last-seen-ghost, +aim-advantage, +async-multiplayer, +zone-bidding, +procedural-arena, +deterministic-combat, +stance-duck, +rescue-carry]
proposes: ["+axis:time", "+axis:turn-structure", "+axis:control", "+trigger:sighted", "+trigger:program_end", "+cond:line_of_sight", "+cond:state", "+cond:facing", "+effect:execute_queue", "+effect:set_state", "+effect:face", "+role:piece", "+role:zone", "+ui:waypoint-path", "+ui:last-seen-marker", "+ui:timeline-scrubber", "+window:replay-window", "+window:lobby-window", "+window:code-editor"]
author: opus
date: 2026-11-02
---

# Frozen Synapse — WEGO-тактика: обидва гравці таємно програмують 5 секунд бою, потім дивляться, чий план кращий

## Суть
Два загони по кілька бійців на процедурно згенерованій карті зі стінами й укриттями. Хід — це **план на ~5 секунд**: кожному бійцю ставиш маршрут з точок, напрям прицілу, присідання, очікування й реакцію на ворога. Коли обидва натиснули **Prime**, плани виконуються **одночасно** й детерміновано: хто дивився в правильний бік, стояв і бачив ворога першим — той і стріляє першим. Ядро — **передбачення**: у режимі планування можна віддати накази й ворожим бійцям і прогнати симуляцію «а що, як він піде сюди».

## Поле і час
- Поле — вільні координати на 2D-карті «згори» (вектор, неон); стіни й низькі стінки згенеровані на кшталт кімнат і коридорів, тому карта виглядає як сітка блоків, але рух і приціл — неперервні (вейпоінти в будь-яку точку). Тому `field: free`, хоча стіни стоять по прихованій сітці (?).
- Час: **WEGO** — фаза планування без ліміту часу (в онлайні — асинхронно, хоч на добу), фаза виконання — ~5 секунд симуляції обох планів разом.
- Інформація: у режимі **light** видно всі рухи; у **dark** — лише ворогів у лінії видимості своїх бійців, а для зниклих — остання відома позиція й скільки часу минуло.
- Випадковість лише в генерації карт і стартових позицій; сам бій детермінований (зброя, стійка, «poise» — готовність стріляти).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Автоматник (Assault / Machine Gun) | piece | середня дистанція | черга; швидко наводиться, базовий боєць |
| Дробовик (Shotgun) | piece | коротка дистанція | вбиває впритул майже гарантовано (?), безсилий здалеку |
| Снайпер (Sniper) | piece | довга дистанція, повільне наведення | один постріл на великій дальності; програє в ближньому бою |
| Ракетник (Rocket) | piece | область вибуху | руйнує стіни, вбиває всіх у радіусі; не стріляє впритул (?) |
| Гранатометник (Grenade) | piece | дуга, таймер | закидає гранату через стіни; вибух через час (?) |
| Riot Shield (Red DLC) | piece | щит | блокує постріли спереду (?) |
| Стіна | static | — | блокує рух і видимість; руйнується ракетою |
| Низька стінка (укриття) | static | — | блокує рух; присівши за нею — боєць прихований і невразливий (?), стоячи — стріляє з перевагою |
| Заручник / VIP | neutral | — | треба довести до зони евакуації (Hostage, місії ескорту) |
| Зона (захоплення / евакуації) | zone | власник | Secure / Disputed / Hostage — мета режиму |
| Ящик (Disputed) | object | — | забрати й донести у свою зону (?) |
| Ворожий «примарний» план | mark | — | накази, які гравець віддає ворогу для симуляції; на бій не впливають |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(plan)` → ТО кожен гравець таємно будує для своїх бійців чергу наказів: `custom: «waypoint(x, y)»` з атрибутами на точці: напрям/ціль прицілу, стійка (стоячи / присівши), швидкість, `wait(t)`, «ignore enemies» (не зупинятись, побачивши ворога).
- КОЛИ `input(simulate)` → ТО `custom: «прогнати 5 с на копії стану»` з власним планом і припущеними планами ворога (вони — лише гіпотеза).
- КОЛИ обидва `input(prime)` → ТО `phase_start(execute)`: `execute_queue` для всіх бійців одночасно, ~5 с.
- КОЛИ `sighted(unit, enemy)` → ЯКЩО `cond:line_of_sight` → ТО `custom: «шанс-тайм: стріляє той, хто раніше прицілився»`; переваги: стоїть > рухається, приціл уже в той бік > треба повернутись, за укриттям > відкрито (?).
- КОЛИ влучання → ТО `disappear_b` (боєць гине з одного попадання (?)).
- КОЛИ `state(unit, ducked)` за низькою стінкою → ТО невидимий/невразливий для стрільби, але сам не стріляє (?).
- КОЛИ боєць побачив ворога і `not ignore_enemies` → ТО `custom: «зупиняється і стріляє»` (дефолтна реакція), решта наказів зсувається (?).
- КОЛИ ракета влучає в стіну або поруч з ціллю → ТО `custom: «explode(area)»`, `set_cell(floor)` для стіни.
- КОЛИ граната → ТО `custom: «летить дугою, вибухає через t»`, `explode(area)`.
- КОЛИ ворог зник з поля зору (dark) → ТО `custom: «примара на останній відомій позиції + час відтоді»`.
- КОЛИ кінець виконання → ТО повтор доступний, нова фаза планування.
- Перемога за режимом: **Extermination** — знищити всіх · **Hostage** — евакуювати заручника / не дати · **Charge** — прорватись у зону (?) · **Disputed** — донести ящики в свою зону (?) · **Secure** — торги: гравці «ставлять» площу зони, яку зобовʼязуються утримати, менша ставка обороняє (?) · Поразка — дзеркально; ліміт ходів у деяких режимах.

## Керування і ввід
- Миша: клік по бійцю → клік по карті ставить вейпоінт (шлях будується автоматично навколо стін); права кнопка на вейпоінті — контекстне меню дій (aim, duck, wait, ignore enemies) (?).
- Таймлайн-повзунок: прокрутити час планування, щоб побачити, де буде кожен боєць (свій і «примарний» ворожий) у момент t.
- Кнопки: Simulate / Play (прогнати план), Reset orders, Prime (віддати хід).
- Асинхронно: можна вести кілька партій онлайн одночасно, повертаючись коли зручно.

## Вікна, меню, HUD
- `main-menu`: Campaign · Multiplayer · Skirmish / Skirmish Generator · Options · Exit.
- `level-select` (кампанія, 55 місій) з брифінгами (`dialogue-window`).
- `lobby-window` мультиплеєра: список активних партій, «твій хід / хід суперника», виклики, режими (?).
- `game-screen` «Planning» — карта, бійці з лініями маршрутів (`ui:waypoint-path`), конуси огляду/прицілу, контекстні дії на вейпоінтах, таймлайн-повзунок (`ui:timeline-scrubber`), привиди ворогів (`ui:last-seen-marker`), кнопки Simulate / Prime.
- `replay-window` — перегляд виконаного ходу й усіх попередніх (на сервері зберігаються повтори партії, ними діляться).
- `end-screen` — підсумок місії/партії, рейтинг.
- `settings-window` — графіка, звук, музика (саундтрек — окремий продукт (?)).
- Переходи: main-menu → lobby/level-select → Planning ↔ execute (анімація) ↔ Planning … → end-screen; будь-коли → replay.

## Фічі поза полем
- `online-multiplayer` асинхронний (сервер зберігає хід), `leaderboard-online`/рейтинг, `replay` і поділ повторів.
- Кампанія 55 місій (+ додаткові цілі: ескорт, захист), `mode-coop` і режим «Upload» у Red DLC.
- Skirmish Generator — `custom-rules`: розмір загону, склад, режим, light/dark.
- `procedural-arena`: кожна партія — нова карта.

## Варіації й родичі
- Frozen Synapse Prime (2014, ремастер), Frozen Synapse 2 (2018, + місто-стратегія (?)), Frozen Cortex (американський футбол за тією ж WEGO-схемою).
- Інші WEGO: Combat Mission, Laser Squad Nemesis (Голлоп), Diplomacy (одночасні накази), RoboRally (програма на 5 регістрів — родич `program-robots`), Door Kickers (пауза-план, але не PvP).
- **Осі варіацій**: структура ходу — по черзі / **одночасно (WEGO)** / real-time з паузою · план — один наказ / **черга на N секунд** / програма з умовами · бій — кубики / **детермінований з перевагою «хто раніше прицілився»** · видимість — повна (light) / туман з останньою позицією (dark).

## Цікавинки для курсу
- WEGO: дві черги наказів виконуються одночасно в одному детермінованому симуляторі — 🥈 (сутності з таймлайном, конфлікти в один момент часу).
- Пісочниця прогнозу: накази ворогу «на пробу» + симуляція на копії стану — 🥇 (`state-as-data` + повтор симуляції).
- Лінія видимості в неперервному просторі з укриттями й стійкою — 🥈 (геометрія відрізків, конус огляду).
- Остання відома позиція ворога в тумані з часом «відтоді» — 📎.
- Повтор ходу/партії з детермінованого стану й наказів — 🥉 (детермінізм = безкоштовний replay).
- Торги в Secure: ставка площею зони, що зобовʼязуєшся втримати, — 📎.

## Мапа на каталог
- Є: `line-of-sight-attack` (пропозиція корпусу) · `melee-vs-ranged` (дробовик / снайпер) · `projectile-shot` · `blast-wave` (ракета, граната) · `impassable-cells` (стіни) · `destructible-blocks` (ракета руйнує) · `path-preview` (маршрут вейпоінтів) · `replay` · `ai-opponent` · `destroy-all-enemies` · `reach-exit` (евакуація) · `game-screen` · `main-menu` · `end-screen` · `level-select`.
- **Нема** → пропозиції карток:
  - `+wego-turns` «Одночасне виконання планів обох сторін» · game-logic/opponent · 🥈 · слот {window_s: 5}.
  - `+action-queue` «Черга наказів на хід» · game-logic/opponent · 🥉 (є в tactics).
  - `+cover-system` «Укриття» · entities/combat · 🥉 (є в xcom).
  - `+fog-of-war` «Туман війни» · interface/render · 🥉 (є в корпусі).
  - `+enemy-plan-sandbox` «Пісочниця прогнозу ходу суперника» · game-logic/opponent · 🥇.
  - `+last-seen-ghost` «Остання відома позиція» · interface/hud · 📎.
  - `+aim-advantage` «Перевага того, хто прицілився раніше» · entities/combat · 🥉.
  - `+async-multiplayer` «Асинхронна партія через сервер» · game-logic/opponent · 🥈.
  - `+zone-bidding` «Торги за розмір зони» · game-logic/win · 📎.
  - `+procedural-arena` «Процедурна арена з укриттями» · levels/generation · 🥇.
  - `+deterministic-combat` «Бій без випадковості» · entities/combat · 🌱 (протиставлення `+hit-chance`).
  - `+stance-duck` «Стійка: присісти за укриттям» · entities/state · 📎.
  - `+rescue-carry` «Евакуація заручника» · game-logic/win · 📎 (є в tactics).

## Пропозиції до словників
- `+axis:time` — значення **`wego`**: план без часу + одночасне виконання фіксованого відрізка; ні `turn`, ні `realtime`, ні `programmed` не описують чесно (найближче — `programmed`, але програма тут на 5 с і пишеться щоходу).
- `+axis:turn-structure` — `wego` (є в корпусі ×4); `+axis:control` — `programmed` (черга вейпоінтів).
- `+trigger:sighted` — боєць побачив ворога (реакція в плані); `+trigger:program_end` — кінець 5-секундного виконання.
- `+cond:line_of_sight` · `+cond:state` (ducked, aiming) · `+cond:facing` (приціл у бік ворога).
- `+effect:execute_queue` — виконати чергу наказів (є в tactics); `+effect:set_state` (duck) · `+effect:face` (приціл).
- `+role:piece` · `+role:zone` (зони режимів).
- `+ui:waypoint-path` — маршрут з вузлами-діями; `+ui:last-seen-marker` — примара ворога з часом; `+ui:timeline-scrubber` — повзунок часу плану.
- `+window:replay-window` · `+window:lobby-window` — список асинхронних партій; `+window:code-editor` — аналог: екран планування як редактор програми бійця.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Frozen_Synapse) — структура ходу, накази, детермінований бій, light/dark, процедурні карти, режими, версії.
- [Steam: Frozen Synapse](https://store.steampowered.com/app/98200/Frozen_Synapse/) — кнопка Prime, Secure з торгами, Hostage Rescue, 55 місій, генератор сутичок.
- YouTube: пошук «frozen synapse gameplay tutorial»; Steam: пошук «frozen synapse» (Prime, FS2).

## Непевне
- (?) Список класів (Assault, Shotgun, Sniper, Rocket, Grenade) і їхня поведінка — з памʼяті; Wikipedia згадує лише «різну зброю» і Riot Shield.
- (?) Точні правила переваги в перестрілці (стійка, наведення, укриття, «poise») — Wikipedia лише називає фактори.
- (?) Присівши за стінкою — невидимий і не стріляє; один постріл = смерть — з памʼяті.
- (?) Правила режимів Charge, Disputed, Secure — з памʼяті, Steam підтверджує лише назви Secure (торги) і Hostage Rescue.
- (?) Чи стіни лежать на прихованій сітці (виглядають блоками) — враження, не перевірено.
- (?) WebSearch вичерпано; frozensynapse.com, mode7games.com, icebrain.free.fr не відповіли.
