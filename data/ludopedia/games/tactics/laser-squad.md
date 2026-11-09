---
title: Rebelstar / Laser Squad
slug: laser-squad
aka: [Rebelstar, Rebelstar Raiders, Rebelstar II, "Laser Squad (1988)", LS]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: state
year: 1988
platforms: [ZX Spectrum, Commodore 64, Amstrad CPC, MSX, Amiga, Atari ST, DOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Laser_Squad", best: true, note: "AP за дію, aimed/snap/auto, тривога при виявленні ворога, паніка, 100 victory points, 7 сценаріїв, закупівля спорядження"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rebelstar", note: "Rebelstar Raiders (1984, лише на двох), Rebelstar (1986): opportunity fire, мораль, стаміна, вантаж; складність 1–8"}
  - {kind: other, url: "https://sunsite2.icm.edu.pl/packages/sinclair/docs/game-database/L/LASERSQD.TXT", note: "інструкція з касети: ціни AP (поворот 1, крок 4/6, +2 по діагоналі), відсоткові дії, огляд 90°, умова opportunity fire, броня 0–4, сценарії"}
  - {kind: other, url: "https://crashonline.org.uk/59/lasersquad.htm", note: "огляд CRASH 59: руйнування стін і дверей, вибух каністри, броня з боків і ззаду, стратегічна мапа, без undo"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Laser+Squad+ZX+Spectrum+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, projectile-shot, shoot-modes, shoot-burst, line-of-sight-attack, fog-of-war, orientation-state, destructible-blocks, explode-area, bomb-fuse, key-and-door, inventory, inventory-items, inventory-limit, item-pickup, ai-opponent, hot-seat, difficulty-levels, destroy-all-enemies, event-points, reinforcements, placement-screen, shop-between-levels, map-window, time-out, +action-points, +ap-percent-cost, +opportunity-fire, +vision-cone, +hit-chance, +armor-by-facing, +morale-states, +stamina-energy, +weight-speed, +throw-catch, +friendly-fire, +victory-points-race, +deployment-phase]
proposes: ["+trigger:enemy_moved", "+trigger:spotted", "+effect:interrupt", "+effect:spend_ap", "+cond:ap_left", "+ui:ap-counter", "+ui:unit-under-cursor", "+window:loadout-shop", "+window:deployment", "+feature:hidden-ai-moves", "+axis:turn-structure=sequential-interruptible"]
author: opus
date: 2026-11-09
---

# Rebelstar / Laser Squad — прабатько X-COM: очки дії на кожен поворот і крок, три режими пострілу, перехоплення ходу з половиною AP

## Суть
Загін із кількох бійців на квадратній сітці виконує сценарій: вбити ціль, підірвати апаратуру, вивести полонених, утримати базу. **Кожна дія коштує очки дії (AP)**: поворот на 45°, крок, відчинити двері, підняти чи кинути предмет, вистрілити. Три режими пострілу (прицільний / навскидку / черга) — обмін AP на точність. Хто закінчив хід з **половиною AP**, стріляє в чужий хід, щойно ворог зʼявиться в полі зору (opportunity fire). Механіки Голлоп переніс у UFO: Enemy Unknown (X-COM), демо Laser Squad 2 стало його зародком.

## Поле і час
- Квадратна сітка сценарію, псевдо-3D вид згори («сплющена» перспектива), прокрутка екрана; окремо — стратегічна мапа всієї місцевості.
- Хід стороною: бійці ходять по одному в будь-якому порядку, кожен витрачає власні AP; «end turn» передає хід. Ходи не скасовуються.
- Огляд бійця — **сектор 90°** (по 45° від напрямку погляду); стіни й двері закривають огляд. Ворог поза оглядом не показаний; у грі проти компʼютера його рухи приховані.
- Обмежена кількість ходів на сценарій; у Rebelstar повстанці програють, якщо не встигли.
- Сцена руйнівна: стіни, двері, меблі можна прострелити; вибух накриває радіус.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Боєць загону | piece | AP за хід, напрямок погляду, броня 0–4 (окремо спереду/з боків/ззаду), мораль, стаміна, навичка зброї, вантаж | ходить, повертається, стріляє, бере/кидає предмети, відкриває двері |
| Ворожий боєць / дроїд | enemy | ті самі параметри | у грі на одного — за компʼютером; рухи приховані |
| Ціль сценарію (Sterner Regnix) | boss | HP | вбити — перемога асасинів |
| Полонений | ally | — | вивести до шахти ліфта (сценарій 3) |
| Апаратура: Databank, Analyser, стабілізаційне ядро, комп'ютери | switch | очки перемоги (Databank 5, Analyser 2) | знищення дає VP |
| Стіна | static | міцність | блокує рух і огляд; руйнується вибухом |
| Двері | gate | відчинено / зачинено / замкнено | відкрити 20 %, замкнути/відімкнути 25 % AP ключем, лицем до дверей; або підірвати |
| Ключ | pickup | до своїх дверей | потрібен для lock/unlock |
| Зброя (пістолети, автомати, лазери, дробовик, снайперка, ракетниця, кинджал, світловий меч) | pickup | вага, ціна AP за режими, точність близько/далеко, обойма | постріл, удар упритул, кидок як снаряд |
| Обойма / ракета | pickup | тип під зброю | перезарядка 50 % AP |
| Граната | object | таймер 0 / 1 / 2 | після зведення вибухає в кінці вказаної фази |
| Вибухівка | object | — | підрив стін, звільнення полоненого |
| Газова каністра | hazard | — | постріл → вибух, шкодить сусідам (і стрільцеві) |
| Тіла й уламки дроїдів | terrain | — | частково заважають руху (Rebelstar) |
| Клітина висадки | zone | — | стартові клітини розстановки |
| Шлюз / край мапи | zone | — | вхід на базу; вихід для доставки предмета |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ТО `custom: «кожен боєць отримує AP; навантажений і втомлений — менше»`.
- КОЛИ `input(turn, u)` → ЯКЩО `counter(ap, ≥, 1)` → ТО `face(u, dir)` на 45°, `counter(ap, −1)`.
- КОЛИ `input(forward, u)` → ЯКЩО `free(cell)` and `counter(ap, ≥, 4)` → ТО `move(u, dir)`, `counter(ap, −4)`; по діагоналі — ще −2; КОЛИ `input(back, u)` → ТО `move`, `counter(ap, −6)`.
- Відсоткові дії (від AP на початок ходу): змінити предмет 25 % · підняти 25 % (50 %, якщо руки зайняті) · кинути на землю 10 % · перезарядити 50 % · звести гранату 20 % · відкрити/зачинити 20 % · відімкнути/замкнути 25 % · кинути 20 % — `custom: «ціна = частка стартових AP»`.
- КОЛИ `input(unlock, u, door)` → ЯКЩО `has(u, key)` and `facing(u, door)` → ТО `clear_state(door, locked)`; інакше двері відкриває лише вибух чи ракета.
- КОЛИ `input(aimed, u, target)` → ЯКЩО `line_of_sight(u, target)` and `has(u, ammo)` and `prob(hit)` (найвищий) → ТО `damage(target, n)`; найбільша ціна AP.
- КОЛИ `input(snap, u, target)` → ТО те саме з меншою ціною AP і меншим шансом.
- КОЛИ `input(auto, u, a, b)` → ЯКЩО `custom: «зброя має автоогонь»` → ТО `custom: «черга по лінії між двома точками, ≥3 пострілів, найменша точність»`; кулі влучають у будь-кого на лінії.
- Шанс влучання: `custom: «навичка бійця × точність зброї на дистанції (окремо далеко / упритул) × режим пострілу»`; броня гасить шкоду за стороною, з якої прийшов удар.
- КОЛИ `turn_end(side)` → ЯКЩО `counter(ap, ≥, half)` → ТО `set_state(u, opportunity)`.
- КОЛИ `line_of_sight(u, e)` у хід суперника → ЯКЩО `state(u, opportunity)` → ТО `custom: «хід перехоплено: власник u стріляє залишком AP, END FIRE повертає хід»`.
- КОЛИ `input(prime, g, n)` → ТО `set_state(g, armed, n)`: 0 — вибух у кінці свого ходу, 1 — у кінці ходу суперника, 2 — у кінці наступного свого.
- КОЛИ `state_off(g, armed)` → ТО `explode(radius)`, `damage(n)` усім у радіусі, `set_cell(wall, rubble)` для стін, що не витримали.
- КОЛИ `input(throw, u, item, cell)` → ТО `custom: «предмет летить; ловить той, у кого вільні руки і хто дивиться на кидача»`.
- КОЛИ `hp_zero(u)` → ТО `disappear(u)`, лишається тіло-перешкода; Rebelstar Raiders: КОЛИ `counter(endurance, <, 1/5 старту)` → ТО `set_state(u, seriously_wounded)`.
- КОЛИ `died(ally)` у полі зору → ЯКЩО `custom: «перевірка моралі провалена»` → ТО `set_state(u, panic)` — боєць виходить з-під контролю.
- КОЛИ `custom: «вантаж важкий»` → ТО `counter(stamina, −n)`; стаміна падає з часом, відпочинок її повертає.
- КОЛИ `destroyed(objective)` або `died(enemy)` → ТО `counter(vp, +n)`; КОЛИ `counter(vp, ≥, 100)` → ТО `win`.
- КОЛИ `reach(carrier, map_edge)` → ЯКЩО `has(carrier, device)` → ТО `win` (Paradise Valley, Stardrive).
- Laser Platoon: КОЛИ `timer(5)` ходів → ЯКЩО `counter(reinforcements, <, 27)` → ТО `spawn_at(trooper, entry)`; КОЛИ `count(own_units, ==, 0)` → ТО `lose` навіть з підкріпленням у черзі.
- КОЛИ `counter(turn, >, limit)` → ТО `lose` сторони, що атакує (Rebelstar).
- Перемога: 100 VP / знищено всіх ворогів / ціль сценарію · Поразка: загін знищено, ліміт ходів · Рахунок: VP.

## Керування і ввід
- Курсор по клітинах (клавіші або джойстик) обирає бійця; дії — з меню: Move (стрілки: вперед, назад, поворот), Fire (вибір режиму і цілі курсором), Pick up, Drop, Change, Load, Prime, Throw, Open/Close, Lock/Unlock, End turn.
- Черга — дві точки на мапі; постріл — ціль-клітина в секторі огляду.
- Opportunity fire: керування переходить до гравця, що чекав, у «fire mode» до END FIRE.
- Два гравці — за одним компʼютером по черзі.

## Вікна, меню, HUD
- `main-menu`: вибір сценарію (1–7; у 8-бітній версії 3 + доповнення), 1 або 2 гравці, рівень складності.
- `+window:loadout-shop` (`shop-window`): кредити за складністю, на кожного бійця — зброя, гранати, броня 0–4; «FIRE двічі — закінчити озброєння».
- `+window:deployment` (`placement-screen`): розставити бійців на клітинах висадки.
- `game-screen`: поле; бічна панель `+ui:unit-under-cursor` — хто/що під курсором; `+ui:ap-counter`; `stat-panel` бійця (броня, мораль, стаміна, навичка); `message-log` повідомлень («ворог помічений»).
- `map-window` — стратегічна мапа: уся місцевість, свої і видимі вороги.
- `end-screen` — переможець і VP.

## Фічі поза полем
- `difficulty-presets` — кредити на спорядження і сила AI в кожному сценарії; Rebelstar — складність 1–8 (кількість і сила дроїдів).
- `hotseat` (на двох) і гра проти AI з прихованими ходами `+feature:hidden-ai-moves`; у сценарії на одного сторони не обрати.
- Доповнення (Expansion Kit) додають сценарії й зброю.

## Варіації й родичі
- Rebelstar Raiders (1984, BASIC, лише на двох) → Rebelstar (1986, AP, opportunity fire, мораль) → Laser Squad (1988) → Lords of Chaos (фентезі) → UFO: Enemy Unknown / [X-COM](xcom.md) (1994) → Laser Squad Nemesis (2002, PBEM, без AP — одночасні накази).
- Rebelstar II (1989): шатл прилітає на 15-му ході, відлітає на 26-му, потім порівнюють VP; Rebelstar: Tactical Command (2005, GBA).
- Родичі в корпусі: [Jagged Alliance 2](jagged-alliance-2.md) (AP, перехоплення), [Silent Storm](silent-storm.md), [XCOM](xcom.md) — дві дії замість AP.
- **Осі варіацій**: ціна дії — фіксована (поворот, крок) / частка стартових AP (LS) / 2 дії (XCOM) · реакція — залишок ≥½ AP (LS) / overwatch-стан (XCOM) / порівняння реакцій (X-COM 1994) · огляд — сектор 90° / коло.

## Цікавинки для курсу
- AP-економіка з поворотом як окремою дією і діагоналлю дорожчою — 📎 (Dijkstra з орієнтацією в стані).
- Opportunity fire: подія «ворог увійшов у сектор огляду» перериває хід суперника — 🥉.
- Сектор огляду 90° від напрямку погляду + туман — 🥉 (кут + raycast).
- Граната з таймером у фазах (0/1/2) — 🌱.
- Черга між двома точками, що влучає в усіх на лінії (дружній вогонь) — 📎 (Bresenham).
- Броня за стороною удару — 🌱.
- Відсоткові ціни дій від стартових AP — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `projectile-shot` · `shoot-modes` ↔ aimed/snap/auto · `shoot-burst` ↔ черга · `line-of-sight-attack` · `fog-of-war` · `orientation-state` ↔ напрямок погляду · `destructible-blocks` · `explode-area` · `bomb-fuse` ↔ граната · `key-and-door` · `inventory` / `inventory-items` / `inventory-limit` ↔ вантаж · `item-pickup` · `ai-opponent` · `hot-seat` · `difficulty-levels` · `destroy-all-enemies` · `event-points` ↔ VP · `reinforcements` · `placement-screen` · `shop-between-levels` ↔ закупівля · `map-window` · `time-out`.
- **Нема** → пропозиції карток:
  - `+action-points` — уже в корпусі.
  - `+ap-percent-cost` «Ціна дії — частка стартових AP» · game-logic/opponent · 🌱.
  - `+opportunity-fire` «Постріл у чужий хід, якщо лишилось ≥½ AP» · entities/combat · 🥉 · слот {threshold: 0.5}.
  - `+vision-cone` «Сектор огляду від напрямку погляду» · interface/render · 🥉 · слот {angle: 90}.
  - `+armor-by-facing` «Броня залежить від сторони удару» · entities/combat · 🌱.
  - `+throw-catch` «Кинути предмет союзнику» · entities/interact · 📎.
  - `+victory-points-race` «Перший до 100 VP» · game-logic/win · 🌱.
  - `+hit-chance`, `+morale-states`, `+stamina-energy`, `+weight-speed`, `+friendly-fire`, `+deployment-phase` — уже в корпусі.

## Пропозиції до словників
- `+trigger:enemy_moved` — ворог зробив крок у чужий хід (тригер opportunity fire).
- `+trigger:spotted` — ворог уперше потрапив у поле зору (тривога).
- `+effect:interrupt` — перехопити хід суперника; `+effect:spend_ap` — списати AP (фіксовано або %).
- `+cond:ap_left` — лишилось AP (≥ частки).
- `+ui:ap-counter` — AP бійця; `+ui:unit-under-cursor` — панель «що під курсором».
- `+window:loadout-shop` — закупівля спорядження на кредити; `+window:deployment` — розстановка на клітинах висадки.
- `+feature:hidden-ai-moves` — рухи AI не показуються.
- `+axis:turn-structure=sequential-interruptible` — послідовні ходи з перериванням.

## Джерела
- ⭐ [Wikipedia: Laser Squad](https://en.wikipedia.org/wiki/Laser_Squad) — AP, режими пострілу, тривога при виявленні, паніка, втома від вантажу, 100 VP, 7 сценаріїв, закупівля на кредити, родовід до X-COM.
- [Wikipedia: Rebelstar](https://en.wikipedia.org/wiki/Rebelstar) — Raiders (на двох, endurance, поранення нижче 1/5), Rebelstar (opportunity fire, мораль, стаміна, вантаж, тіла заважають, складність 1–8, ліміт часу), Rebelstar II.
- [Інструкція Laser Squad (txt)](https://sunsite2.icm.edu.pl/packages/sinclair/docs/game-database/L/LASERSQD.TXT) — таблиця AP, відсоткові дії, граната 0/1/2, огляд 90°, умова opportunity fire, броня 0–4, сценарії й VP.
- [CRASH 59: Laser Squad](https://crashonline.org.uk/59/lasersquad.htm) — руйнування стін/дверей/меблів, вибух каністри, броня спереду/ззаду/з боків, стратегічна мапа, без скасування ходів.
- YouTube: пошук «Laser Squad ZX Spectrum gameplay».

## Непевне
- (?) Скільки AP дає хід (залежить від бійця і стану) і формула зменшення від вантажу/втоми.
- (?) Точна ціна AP пострілів — таблиця в інструкції без підписаних колонок.
- (?) Як саме броня «за стороною» множить шкоду; формула шансу влучання.
- (?) Ліміт ходів у сценаріях Laser Squad (Wikipedia згадує ліміт без чисел).
- (?) Чи панікує боєць лише від смерті союзника в полі зору, чи й від поранень.
