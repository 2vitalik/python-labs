---
title: Liero
slug: liero
aka: [Liero 1.33, Liero 1.36, OpenLiero, WebLiero, lierolibre, Liero Xtreme, LieroX]
family: dig-gravity
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: both
  goal: score
year: 1998
platforms: [MS-DOS, Windows, Linux, macOS, web]
links:
  - {kind: other, url: "https://www.liero.be/THE_OFFICIAL_LIERO_FAQ.txt", best: true, note: "офіційний гайд Durandal: клавіші, копання, мотузка, усі 40 зброй з поведінкою, режими, опції, AI"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Liero", note: "огляд: real-time Worms, копаний рельєф і незламний камінь, 5 з 40 зброй, нескінченні патрони, режими, версії й клони"}
  - {kind: official, url: "https://www.liero.be/", note: "сайт: версії 1.33 / 1.36 / WebLiero / lierolibre, завантаження, ресурси"}
  - {kind: other, url: "https://github.com/gliptic/liero", note: "код Liero 1.36 (OpenLiero)"}
  - {kind: play, url: "https://www.webliero.com/", note: "WebLiero: онлайн-мультиплеєр у браузері"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Liero+1.33+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [projectile-shot, shoot-modes, shoot-burst, shoot-spread, shoot-cooldown, explode-area, bomb-fuse, gravity-fall, hp-damage, respawn, item-pickup, inventory, inventory-items, dig-terrain, destructible-blocks, impassable-cells, spawn-random-cell, particles, hot-seat, ai-opponent, ai-random, realtime-ai, player-camera, minimap-radar, status-panel, game-settings, settings-elements, controls-remap, keyboard-controls, replay, main-menu, game-screen, end-screen, +ninja-rope, +weapon-loadout-select, +reload-time, +dig-by-input-gesture, +dirt-producing-weapons, +steerable-missile, +split-screen-duel, +tag-timer-mode, +capture-the-flag, +booby-crate, +weapon-availability-settings]
proposes: ["+effect:hook", "+effect:reload", "+trigger:landed", "+ui:reload-bar", "+ui:split-screen", "+window:loadout-select", "+feature:weapon-availability", "+card:ninja-rope", "+card:weapon-loadout-select", "+card:reload-time", "+card:dig-by-input-gesture", "+card:dirt-producing-weapons", "+card:split-screen-duel", "+card:tag-timer-mode", "+card:booby-crate"]
author: opus
date: 2026-11-09
---

# Liero — real-time дуель двох черв'яків у піксельному рельєфі, який копають, підривають і насипають

## Суть
Два черв'яки на одному бічному полі б'ються наживо: бігають, стрибають, копають тунелі в землі й стріляють з п'яти обраних перед боєм зброй (з 40). Ядро для корпусу — **рельєф як матеріал і укриття**: земля прогризається руками, вибухами, лазером і вогнем, а частина зброї навпаки **насипає** землю, щоб замурувати тунель; незламний камінь — єдина постійна стіна. Головний рух — ninja rope, гак на мотузці, що чіпляється за рельєф і тягне. Описую рельєфний шар і взаємодії; балістику окремих зброй — коротко (за чергою: «піксельний рельєф, не клітини»).

## Поле і час
- Поле — одна мапа бічного виду, піксельна маска: земля (копана), камінь (незламний), тло (порожнеча). Рівень — з файла або [Random] (генерована печера); опція Regenerate level — нова випадкова мапа щогри.
- Гравітація на черв'яків, гранати, кров і частину снарядів; частина зброї (Bazooka, Zimm) летить без гравітації.
- Камера: розділений екран — у кожного гравця своя половина, що стежить за його черв'яком; опційна мінімапа (Map).
- Час — real-time: обидва діють одночасно; кадри обмежує Screen sync.
- Партія — до цілі режиму (кількість життів, фрагів, часу «it», прапорів).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Черв'як | player | здоров'я, 5 зброй, приціл | ходить, стрибає, копає, цілиться вгору/вниз; після смерті — респавн |
| Черв'як суперника / CPU | enemy | Controller: людина або CPU | CPU здебільшого йде до гравця, ігнорує бонуси, часто бʼє сам себе |
| Земля | terrain | колір | руйнується копанням, вибухами й «копальною» зброєю |
| Камінь | static | — | незламний: не копається, не вибухає |
| Тло | terrain | — | порожнеча, по ній літають і висять на мотузці |
| Ninja rope | object | довжина | гак летить, чіпляється за рельєф або черв'яка; тягне до точки, гойдається, укорочується |
| Ящик зброї | pickup | назва над ящиком (опція) | підібрати = замінити одну з 5 зброй |
| Ящик здоров'я | pickup | — | лікує черв'яка |
| Booby trap (ящик-пастка) | hazard | 5 шкоди | виглядає як ящик; вибухає при дотику |
| Mine / Float mine / Bouncy mine | hazard | 12 / низька / 18 шкоди | Mine зливається з рельєфом; Float — пливе; Bouncy — стрибає й повертається |
| Кулі й ракети (Handgun, Uzi, Rifle, Bazooka, Mini rockets, Gauss gun) | projectile | патрони в обоймі | летять, вибухають/ранять при контакті |
| Chaingun / Minigun / Laser / Flamer / Doomsday | projectile | 50 / 70 / 80 / 100 / 8 | прогризають землю — зброя-лопата; Minigun ще й як джетпак |
| Missile | projectile | — | керується стрілками, поки летить; черв'як тим часом беззахисний |
| Гранати (Grenade, Cluster, Chiquita, Big nuke, Crackler, Grasshopper) | projectile | таймер | вибух + осколки; Crackler копає вниз; Grasshopper розмножується до 7 разів; Big nuke робить велику діру |
| Dirtball | projectile | — | створює грудки землі — закупорити тунель |
| Greenball | projectile | 40 | створює зелені копані кульки, без шкоди |
| Fan | object | — | здуває все, що торкнеться (крім дуже швидких снарядів) |
| Larpa / Bouncy larpa / Zimm / RB Rampage | projectile | — | сиплють осколками або відбиваються від стін і повертаються |
| Прапор / база | zone | режим CTF | прапор несуть на свою базу; падає при смерті |
| Кров | object | Blood % (до 500) | частинки, що падають — лише вигляд |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(worm, dir)`; ЯКЩО `cell(cell_ahead, rock)` → ТО `block`.
- КОЛИ `input(dig)` (утримати напрям і швидко тицьнути протилежний) → ЯКЩО `cell(cell_ahead, dirt)` → ТО `set_cell(cell_ahead, background)` — прогризти тунель.
- КОЛИ `input(jump)` → ЯКЩО `custom: «черв'як стоїть на рельєфі»` → ТО `custom: «стрибок»`; КОЛИ `tick` → ЯКЩО `not supported(worm)` → ТО `fall(worm)`.
- КОЛИ `input(change_weapon + jump)` → ТО `spawn(rope_hook)`; КОЛИ `contact(rope_hook, dirt|rock)` → ТО `attach(worm, hook)` і `pull(worm)` до точки; КОЛИ `contact(rope_hook, enemy_worm)` → ТО `attach(hook, enemy_worm)` — тягне суперника.
- КОЛИ `input(change_weapon + up|down)` → ЯКЩО `state(worm, on_rope)` → ТО `custom: «укоротити / подовжити мотузку»`; `+ left|right` → `custom: «розгойдуватись»`.
- КОЛИ `input(fire)` → ЯКЩО `custom: «зброя заряджена»` → ТО `spawn(projectile)`, `counter(clip, −1)`; ЯКЩО `counter(clip, =, 0)` → ТО `custom: «перезарядка, лише поки зброя обрана»`.
- КОЛИ `input(change_weapon)` → ЯКЩО `mode(load_change)` or `custom: «зброя не перезаряджається»` → ТО `custom: «наступна з 5 зброй»`; інакше гравець беззбройний до кінця перезарядки.
- КОЛИ `contact(projectile, dirt)` → ЯКЩО `custom: «вибухова зброя»` → ТО `explode(circle, r)`: `set_cell(dirt → background)` у радіусі; камінь лишається.
- КОЛИ `contact(laser|chaingun|flamer|doomsday, dirt)` → ТО `set_cell(dirt → background)` — промінь/черга копає.
- КОЛИ `contact(dirtball, any)` → ТО `explode(circle, r, into: dirt)` — грудка землі закупорює тунель; Greenball → `spawn(green_blob)` копаний.
- КОЛИ `contact(projectile|explosion, worm)` → ТО `damage(worm, n)`; КОЛИ `hp_zero(worm)` → ТО `lives(−1)`, `respawn(worm, random)`.
- КОЛИ `timer(fuse)` → ТО `explode` гранати; Cluster / Chiquita / Larpa → `spawn(shrapnel)`; Grasshopper → `clone(grasshopper)` до 7 разів.
- КОЛИ `input(aim)` → ЯКЩО `custom: «Missile у польоті»` → ТО `custom: «стрілки повертають ракету»`, черв'як не керується.
- КОЛИ `contact(any, fan)` → ТО `custom: «здути від вентилятора»`.
- КОЛИ `custom: «ящик зʼявився»` (`rng`) → ТО `spawn_at(crate, random)`; ЯКЩО `mode(names_of_bonuses)` → назва зброї над ящиком (booby теж «підписаний»).
- КОЛИ `contact(worm, weapon_crate)` → ТО `pickup` і `custom: «замінити одну з 5 зброй»`; health crate → `heal(worm, n)`; booby trap → `explode`, `damage(5)`.
- КОЛИ `contact(worm, mine)` → ТО `explode`, `damage(12)`.
- Kill'em all: КОЛИ `counter(lives, =, 0)` → ТО `lose`; КОЛИ `counter(frags, =, target)` → ТО `win`.
- Game of tag: КОЛИ `died(worm)` → ТО `set_state(worm, it)`; КОЛИ `tick` → ЯКЩО `state(worm, it)` → ТО `counter(it_time, +1)`; КОЛИ `counter(it_time, ≥, limit)` → ТО `lose`.
- Capture the flag: КОЛИ `custom: «перше вбивство»` → ТО `set_state(killer, collector)`; КОЛИ `reach(collector, home_base)` → ЯКЩО `has(collector, flag)` → ТО `counter(flags, +1)`; КОЛИ `died(collector)` → ТО `custom: «прапор падає, роль колектора — супернику»`.
- Simple CTF: обидва несуть прапори одночасно, без ролі колектора.
- Перемога: ціль режиму (фраги / життя / прапори) · Поразка: життя скінчились або найбільше часу «it» · Рахунок: фраги; програвший не здається — «winner takes all».

## Керування і ввід
- Гравець 1: R/F — приціл вгору/вниз, D/G — вліво/вправо, Left Alt — стрибок, Left Ctrl — постріл, Left Shift — зміна зброї.
- Гравець 2: стрілки, Right Shift — стрибок, Right Ctrl — постріл, Right Alt — зміна зброї.
- Мотузка: зміна зброї + стрибок — постріл гаком; зміна + ↑/↓ — довжина; ←/→ — гойдання.
- Копання — жест: утримати напрям і швидко тицьнути протилежний.
- Перепризначення клавіш — Player Options; гравець може бути CPU (Controller).

## Вікна, меню, HUD
- `main-menu` / `match-setup`: режим (Kill'em all, Game of tag, CTF, Simple CTF), Lives / ціль, Loading times %, Level ([Random]), Regenerate level, Shadows, Map, Screen sync, Blood %, Max bonuses, Names of Bonuses, Load+Change.
- `custom-window` Player Options (на кожного): ім'я, колір, Controller (людина/CPU), клавіші; Weapon Options — кожна зброя: Menu / Bonus / Banned (≥1 доступна).
- `loadout-select` перед боєм: кожен гравець обирає 5 зброй з дозволених.
- `game-screen`: розділений екран (`split-screen`) — дві камери, у кожної `hp-bar`, `reload-bar`, поточна зброя, лічильник життів/фрагів; опційна `minimap`.
- `end-screen`: переможець; 1.36 — `replay-window` (запис повтору), профілі гравців.
- Переходи: меню → вибір зброї → бій → кінець → меню.

## Фічі поза полем
- `custom-rules`: відсоток перезарядки (≤20 % — дуже швидко, 0 % — «complete mayhem»), доступність кожної зброї, кількість бонусів, кров.
- `ai-opponent-levels` (1.36 — новий AI) (?) щодо рівнів складності.
- `replay`, профілі гравців, режими вікна F5/F6 (1.36).
- `mod-support`: заміна 40 зброй, графіки черв'яка, звуків; мапи з іншим незламним матеріалом і кольоровою землею; редактори мап (Liero Hell Hole).
- WebLiero — `online-multiplayer` з необмеженою кількістю гравців і пулами мап; без splitscreen.

## Варіації й родичі
- Версії: 1.33 (1999, класика; сорс втрачено), 1.34–1.36 (OpenLiero, Gliptic), lierolibre (вільний форк 1.35b), WebLiero (2019), Liero Xtreme / OpenLieroX (онлайн, команди, свої зброї), NiL (GPL, TCP, >2 гравців).
- Родичі: Worms (покроковий предок-ідея), [scorched-earth.md](scorched-earth.md) — покрокова артилерія з земляною зброєю; [noita.md](noita.md) — кожен піксель симулюється; Gusanos, Soldat (?).
- **Осі варіацій**: рух у рельєфі «лише копати / мотузка / джетпак»; зброя «фіксований набір / 5 обраних з N / бонуси»; обмеження стрільби «патрони / перезарядка (Liero) / енергія»; рельєф «руйнується / ще й насипається»; камера «спільна / розділений екран / мережа».

## Цікавинки для курсу
- Піксельний рельєф з трьома матеріалами (земля / камінь / тло) і копання-жест — 📎.
- Вибух як `set_cell` у колі з незламним винятком; зброя-лопата (Laser, Flamer) — 🌱 кожна.
- Ninja rope: гак летить, чіпляється, далі пружинна/маятникова фізика з довжиною — 🥉.
- Перезарядка замість патронів і правило «лише поки обрана» — 🌱.
- Розділений екран: дві камери на одному полі — 📎.
- Game of tag з лічильником часу «it» — 🌱; CTF з роллю колектора — 📎.
- Grasshopper (самокопіювання до 7) і Missile (керований снаряд) — 📎 кожна.

## Мапа на каталог
- Є: `projectile-shot` · `shoot-modes` / `shoot-burst` / `shoot-spread` / `shoot-cooldown` ↔ 40 зброй · `explode-area` · `bomb-fuse` ↔ гранати · `gravity-fall` · `hp-damage` · `respawn` · `item-pickup` / `inventory` / `inventory-items` ↔ 5 слотів і ящики · `dig-terrain` · `destructible-blocks` · `impassable-cells` ↔ камінь · `spawn-random-cell` ↔ ящики · `particles` ↔ кров · `hot-seat` · `ai-opponent` / `ai-random` / `realtime-ai` · `player-camera` · `minimap-radar` · `status-panel` · `game-settings` / `settings-elements` · `controls-remap` · `keyboard-controls` · `replay` · `main-menu` / `game-screen` / `end-screen`.
- **Нема** → пропозиції карток:
  - `+ninja-rope` «Гак на мотузці: чіпляється, тягне, гойдає» · entities/move · 🥉 · слоти {length, swing}.
  - `+weapon-loadout-select` «Вибір N зброй з пулу перед боєм» · game-logic/setup · 🌱 · слот {n}.
  - `+reload-time` «Перезарядка обойми замість скінченних патронів» · entities/combat · 🌱 · слот {loading_pct}.
  - `+dig-by-input-gesture` «Копання жестом вводу» · entities/move · 🌱.
  - `+dirt-producing-weapons` «Снаряд насипає землю» · entities/combat · 📎 (див. `+dirt-weapons` Scorched Earth).
  - `+split-screen-duel` «Дві камери на одному полі» · interface/render · 📎.
  - `+tag-timer-mode` «Режим "квач" з лічильником часу» · game-logic/goals · 🌱.
  - `+booby-crate` «Бонус-пастка, схожа на справжній» · entities/pickup · 🌱.
  - Також: `+steerable-missile`, `+capture-the-flag`, `+weapon-availability-settings`.

## Пропозиції до словників
- `+effect:hook` — сутність чіпляється до точки рельєфу/іншої сутності й підтягується (ninja rope).
- `+effect:reload` — повтор: обойма перезаряджається за час.
- `+trigger:landed` — повтор: сутність торкнулась рельєфу після польоту (гак, граната).
- `+ui:reload-bar` — смуга перезарядки поточної зброї.
- `+ui:split-screen` — поле показано кількома камерами одночасно.
- `+window:loadout-select` — повтор: вибір набору зброї перед боєм.
- `+feature:weapon-availability` — кожна зброя: у меню / лише бонусом / заборонена.

## Джерела
- ⭐ [THE OFFICIAL LIERO FAQ (Durandal)](https://www.liero.be/THE_OFFICIAL_LIERO_FAQ.txt) — клавіші, копання, мотузка, 40 зброй за групами з патронами/шкодою, режими, опції, поведінка CPU.
- [Wikipedia: Liero](https://en.wikipedia.org/wiki/Liero) — 1998, Joosa Riekkinen; 5 з 40 зброй, нескінченні патрони, незламний камінь, режими, версії й клони, модифікації.
- [liero.be](https://www.liero.be/) — версії 1.33 / 1.36 / WebLiero / lierolibre, F5/F6, реплеї.
- [GitHub gliptic/liero](https://github.com/gliptic/liero) — код 1.36 (лише з лінків сайту, не відкривав).
- [WebLiero](https://www.webliero.com/) — браузерна онлайн-версія (лінк із сайту).

## Непевне
- (?) Точні розміри мапи, радіуси вибухів, здоров'я черв'яка — у джерелах нема.
- (?) Чи земля без опори осідає (як у Scorched Earth) — у FAQ не сказано; правило падіння записане лише для черв'яка.
- (?) Рік: Wikipedia — 1998 (перша версія), 1.33 — 1999 (WP) / 2000 (liero.be).
- (?) Склад HUD (смуги здоров'я й перезарядки, лічильники) — з памʼяті про 1.33, не з тексту.
- (?) Режим «Holdazone» — є в 1.36 / WebLiero (?), у FAQ 1.33 нема.
