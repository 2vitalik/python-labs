---
title: "Flash Point: Fire Rescue"
slug: flash-point-fire-rescue
aka: [Flash Point]
family: board-digital
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: coop
  info: hidden
  random: both
  goal: collect
year: 2011
platforms: [board, PC]
links:
  - {kind: other, url: "https://world-of-board-games.com.sg/docs/Flash-Point-Fire-Rescue.pdf", best: true, note: "повні правила Indie Boards & Cards (PDF, 12 с.): родинна й досвідчена гра, вибух, ударна хвиля, спалах, спеціалісти, FAQ, варіанти"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Flash_Point:_Fire_Rescue", note: "автор, видавці, Kickstarter 2011, доповнення"}
  - {kind: steam, url: "https://store.steampowered.com/app/654220/Flash_Point_Fire_Rescue/", note: "цифрова версія RetroEpic (2018): родинні й досвідчені правила, соло й спільний екран"}
  - {kind: official, url: "https://www.indieboardsandcards.com/our-games/flash-point-fire-rescue/", note: "сторінка видавця, доповнення"}
  - {kind: other, url: "https://rulespal.com/flash-point-fire-rescue/rulebook", note: "правила й доповнення (бачив у пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Flash+Point+Fire+Rescue+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 75
mechanics: [move-4dir, impassable-cells, destructible-blocks, blast-wave, explode-area, chain-reaction, spawn-random-cell, hidden-under-block, respawn, carrier-platform, collect-quota, keep-playing-after-win, difficulty-levels, character-select, rule-variants, game-screen, end-screen, help-window, +shared-field-coop, +action-points, +saved-action-points, +variable-player-powers, +fire-spread, +smoke-fire-escalation, +shockwave-through-fire, +edge-walls, +wall-damage-collapse, +door-toggle, +dice-coordinate-target, +flare-up-reroll, +redirect-arrows, +carry-victim-cost, +knockdown-to-respawn, +deck-gun-scatter, +supply-out-lose]
proposes: ["+effect:roll_dice", "+cond:wall_between", "+ui:doom-track", "+card:smoke-fire-escalation", "+card:shockwave-through-fire", "+card:dice-coordinate-target", "+card:flare-up-reroll", "+card:saved-action-points", "+card:wall-damage-collapse"]
author: opus
date: 2026-11-09
---

# Flash Point: Fire Rescue — кооп-пожежники в будинку-сітці: дим густішає у вогонь, вогонь вибухає, хвиля ламає стіни

## Суть
1–6 гравців — пожежна команда в палаючому будинку: треба винести 7 жертв, поки не загинуло 4 і поки будинок не обвалився (24 маркери пошкоджень). Кожен хід — 4 очки дій (рух, гасіння, рубання стін, двері, несення), потім кидок двох кубиків додає дим у випадкову клітину, і клітинні правила ескалації роблять із диму вогонь, з вогню — вибух з ударною хвилею, що ламає стіни й двері. Kevin Lanzing (2011, Indie Boards & Cards); самі автори кажуть, що гра «багато чим завдячує Pandemic».

## Поле і час
- Будинок — сітка 6 рядків × 8 стовпців: координата клітини = червоний d6 (рядок) × чорний d8 (стовпець). Навколо — кільце зовнішніх клітин (з цифрами й гранями кубиків, 4 кутові); зовні теж можна ходити, туди ж вибух може закинути вогонь.
- **Стіни лежать на ребрах** клітин, не в клітинах: сегмент стіни має 0 / 1 (пошкоджена) / 2 (зруйнована, прохідна) маркери. Дверні прорізи (8 на лицьовій стороні) — двері зачинені / відчинені / знищені.
- Сусідство — лише ортогональне, і **зачинені двері чи ціла стіна розривають сусідство** (для руху, гасіння, поширення вогню).
- Поле двобічне (дві будівлі); у досвідченій грі поле ділиться на 4 квадранти (для гармати), є місця паркування машин (по 4 для кожної, машина займає 2 клітини).
- Хід гравця: дії → просування вогню → поповнення POI; далі гравець ліворуч. Темп задає не таймер, а невідворотний кидок кубиків щоходу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пожежник | piece | 4 AP/хід, зберігає до 4 AP | ходить, гасить, рубає, відчиняє двері, несе жертву/небезпечне |
| Дим | hazard | бік маркера загрози (33 маркери «дим/вогонь») | дим + дим = вогонь; дим поруч із вогнем = вогонь |
| Вогонь | hazard | — | вхід 2 AP; хід у вогні закінчувати не можна; кидок у вогонь = вибух |
| POI «?» | container | 18: 12 жертв + 6 хибних, у грі 10 + 5 | лицем донизу; відкривається, коли пожежник входить |
| Жертва | object | — | несуть за 2 AP за клітину; у вогонь не можна; вогонь на ній — втрачена |
| Хибна тривога | object | — | відкрилась — знімається з поля |
| Сегмент стіни | static | 0 / 1 / 2 пошкодження | блокує; 2 пошкодження — зруйнована, прохідна для всіх |
| Двері | gate | зачинені / відчинені / знищені | 1 AP перемкнути; вибух чи ударна хвиля знищує |
| Маркер пошкодження | supply | 24 | вичерпано — будинок обвалюється |
| Маркер дії | supply | 21 | збережений AP |
| Зовнішня клітина | terrain | — | рятування (родинна гра); вогонь тут гасне наприкінці ходу |
| Кубики d6 + d8 | — | червоний / чорний | координата цілі вогню й нових POI |
| Небезпечна речовина (hazmat) | hazard | 3–5 залежно від складності | у вогні → вибух; носиться як жертва; винесена — утилізована |
| Гаряча точка (hot spot) | terrain | 24 маркери, запас на полі | кидок у неї → додатковий кидок (flare up); не гаситься |
| Пожежна машина (Engine) | platform | 2 клітини на місці паркування | Drive 2 AP; Deck Gun 4 AP; на ній — Crew Change |
| Швидка (Ambulance) | platform | 2 клітини | Drive 2 AP «по радіо»; сюди треба донести жертву; сюди потрапляє збитий пожежник |
| Маркер лікування | mark | 3 | жертва вилікувана — йде сама, без штрафу |
| Парамедик | piece | 4 AP | Treat 1 AP; гасіння за подвійну ціну |
| Капітан | piece | 4 AP + 2 командні | командує рухом/дверима інших за їхню ціну |
| CAFS-пожежник | piece | 3 AP + 3 на гасіння | — |
| Універсал (Generalist) | piece | 5 AP | без умінь |
| Рятувальник | piece | 4 AP + 3 на рух | рубає за 1 AP; гасіння за подвійну ціну |
| Водій/оператор | piece | 4 AP | Deck Gun за 2 AP, по одному перекиду кожного кубика |
| Тепловізорник | piece | 4 AP | Identify: відкрити будь-який POI за 1 AP |
| Hazmat-технік | piece | 4 AP | Dispose: прибрати hazmat зі своєї клітини за 2 AP |

## Правила (КОЛИ → ЯКЩО → ТО)
Родинна гра:
- КОЛИ `input(move(ff, dir))` → ЯКЩО `not custom: «стіна чи зачинені двері між клітинами»` (`+cond:wall_between`) і `not occupied(target, fire)` → ТО `move(ff, dir)`, `counter(ap, -1)`; ЯКЩО `occupied(target, fire)` → ТО `move`, `counter(ap, -2)`.
- КОЛИ `input(move(ff, dir))` → ЯКЩО `state(ff, carrying)` і `not occupied(target, fire)` → ТО `move(ff, dir)`, `carry(victim)`, `counter(ap, -2)`; у вогонь — `block`.
- КОЛИ `enter(ff, poi)` → ТО `reveal(poi)` (0 AP); ЯКЩО `state(poi, false_alarm)` → ТО `disappear(poi)`.
- КОЛИ `input(toggle_door)` → ЯКЩО `custom: «двері на ребрі клітини пожежника»` → ТО `set_state(door, open|closed)`, `counter(ap, -1)`.
- КОЛИ `input(extinguish(cell))` → ЯКЩО `in_range(ff, cell, 1)` і `not custom: «стіна між»` → ТО дим: `disappear(smoke)` −1 AP · вогонь у дим: `transform(fire, smoke)` −1 AP · вогонь геть: `disappear(fire)` −2 AP.
- КОЛИ `input(chop(wall))` → ТО `counter(wall_damage, +1)`, `counter(damage_pool, -1)`, `counter(ap, -2)`; КОЛИ `counter(wall_damage, ==, 2)` → ТО `set_state(wall, destroyed)` — сусідство відновлюється.
- КОЛИ `reach(victim, outside)` → ТО `counter(rescued, +1)`, `disappear(victim)`.
- КОЛИ `turn_end(player)` → ЯКЩО `occupied(ff_cell, fire)` → ТО `block` (хід у вогні не закінчують); `counter(saved_ap, +unspent)` до максимуму 4.
- КОЛИ `phase_start(advance_fire)` → ТО `custom: «кинути d6 і d8 — ціль»` (`+effect:roll_dice`), `spawn_at(smoke, target)`.
- КОЛИ `spawned(smoke)` → ЯКЩО `occupied(target, smoke)` → ТО `transform(smoke, fire)` (дим + дим = вогонь).
- КОЛИ `spawned(smoke)` → ЯКЩО `adjacent_count(target, fire, >=, 1)` (без стіни між) → ТО `transform(smoke, fire)`.
- КОЛИ `spawned(smoke)` → ЯКЩО `occupied(target, fire)` → ТО `explode(cross, 1, fire)`: у кожному з 4 напрямків рівно одне — вільна клітина `spawn_at(fire)` / дим `transform(smoke, fire)` / стіна `counter(wall_damage, +1)` / двері `disappear(door)`.
- КОЛИ `custom: «у напрямку вибуху сусідня клітина вже у вогні»` → ТО `custom: «ударна хвиля йде далі крізь вогонь, зруйновані стіни й відчинені двері (знищуючи їх) до першої клітини без вогню / диму / стіни / зачинених дверей і діє на неї, як вибух»`.
- КОЛИ `phase_start(secondary_effects)` → ТО `custom: «повторювати, доки є: дим поруч із вогнем → вогонь»` (flashover) — `adjacent(smoke, fire)` → `transform(smoke, fire)`.
- КОЛИ `contact(fire, ff)` → ТО `respawn(ff, ambulance_spot)` (збитий; найближче місце паркування швидкої); ЯКЩО `state(ff, carrying)` → ТО `counter(lost, +1)`.
- КОЛИ `contact(fire, poi|victim)` → ТО `reveal(poi)`; ЯКЩО жертва → `counter(lost, +1)`; `disappear`.
- КОЛИ `phase_start(cleanup)` → ТО `disappear(fire@outside)`.
- КОЛИ `phase_start(replenish_poi)` → ЯКЩО `count(poi_and_victims, <, 3)` → ТО `custom: «кидок кубиків»`, `spawn_at(poi, target)`; ЯКЩО `occupied(target, fire|smoke)` → спершу `disappear(threat)`; ЯКЩО `occupied(target, ff)` → `reveal(poi)`; ЯКЩО `occupied(target, poi)` → перекинути.
- КОЛИ `counter(rescued, >=, 7)` → ТО `win` (можна грати далі до всіх 10 — «ідеальна гра»).
- КОЛИ `counter(lost, >=, 4)` → ТО `lose`.
- КОЛИ `counter(damage_pool, ==, 0)` → ТО `lose` (обвал; усі, хто всередині, і решта POI — втрачені).
- КОЛИ `custom: «маркери вогню скінчились»` → ТО `custom: «вогонь і дим не додаються, а пошкодження від вибухів — далі»`.

Досвідчена гра (додатково):
- КОЛИ `game_start` → ТО `explode` 3–4 рази у випадкових клітинах + `spawn_at(hot_spot)`, `spawn_at(hazmat)` за кидками; кількість — за складністю.
- КОЛИ `after(flashover)` → ЯКЩО `occupied(hazmat_cell, fire)` → ТО `explode(cross, 1, fire)`, `disappear(hazmat)`, `spawn_at(hot_spot, cell)`.
- КОЛИ `spawned(smoke)` → ЯКЩО `occupied(target, hot_spot)` → ТО `trigger(advance_fire)` ще раз (flare up, без ліміту); після останнього кидка `spawn_at(hot_spot, last_target)` — один за хід, із запасу на полі.
- КОЛИ `reach(victim, ambulance)` → ТО `counter(rescued, +1)`; винести назовні вже не досить.
- КОЛИ `input(drive(vehicle))` → ТО `teleport(vehicle, next_parking)`, `counter(ap, -2)`; пожежники на місці паркування — `carry` за 0 AP; швидка до клітини з жертвою — жертва врятована.
- КОЛИ `input(deck_gun)` → ЯКЩО `occupied(ff_cell, engine)` і `custom: «у сусідньому квадранті нема пожежників»` → ТО `custom: «кидок; кубик поза квадрантом — перевернути на протилежну грань»`, `clear(target + 4 сусіди, без стін між)`, `counter(ap, -4)`.
- КОЛИ `input(treat(victim))` → ЯКЩО `state(ff, paramedic)` → ТО `set_state(victim, treated)` — веде будь-хто без доплати, по одній.
- КОЛИ `input(crew_change)` → ЯКЩО `occupied(ff_cell, engine)` і `first_time` (першою дією ходу) → ТО `choose(вільний спеціаліст)`, `counter(ap, -2)`.
- КОЛИ `contact(fire, ff)` → ТО `respawn(ff, ambulance_current_spot)`.
- КОЛИ `phase_start(replenish_poi)` → ЯКЩО `occupied(target, threat|ff|poi)` → ТО `custom: «йти за стрілками на полі до першої вільної клітини; нема — перекинути»`.
- Перемога: 7 врятованих · Поразка: 4 втрачені або 24 пошкодження (обвал) · Рахунок: нема, лише журнал «Fire Station Log».

## Керування і ввід
- Настільна: активний гравець витрачає AP у довільному порядку, дію можна повторювати; пас дозволений; решту AP — у маркери на майбутнє.
- Кидки кубиків — у фазі вогню й для POI, усе інше — вибір команди, рішення за активним гравцем.
- (цифрова версія) Клік по клітині/дії з вартістю в AP, кидок і каскад вогню — анімацією; соло можна вести кількох пожежників.

## Вікна, меню, HUD
(цифрова версія; інтерфейс RetroEpic не бачив)
- `main-menu`: Нова гра · Правила · Налаштування.
- `match-setup`: кількість пожежників, родинні / досвідчені правила, будівля (сторона поля), складність Recruit / Veteran / Heroic.
- `character-select`: 8 спеціалістів з AP і вміннями.
- `game-screen`: сітка 6×8 зі стінами на ребрах, двері, дим/вогонь, POI, пожежники; лічильники «врятовано / втрачено» (`+ui:doom-track` для пошкоджень і втрат), `action-points` (+збережені), `turn-indicator`, кубики кидка вогню, `popup-text` вибуху.
- `end-screen`: перемога / обвал / 4 втрати.
- `help-window`: памʼятки гравця (порядок фази вогню, вартість дій).
- `stats-window` — аналог паперового «Fire Station Log» (гравці, рівень, будівля, врятовано, втрачено).

## Фічі поза полем
- `difficulty-presets`: Recruit (3 вибухи, 3 hazmat) · Veteran (3, 4 + 3 гарячі точки) · Heroic (4, 5 + 3 гарячі точки, 12 точок у запасі).
- `custom-rules`: родинна ↔ досвідчена гра; досвідчені правила вмикаються частинами (спершу спеціалісти й hazmat, потім машини, потім гарячі точки); варіанти з правил: Lone Engine Company (без Crew Change), Unmarked Hazards (hazmat під хибними тривогами), Murphy Strikes (без гармати).
- `mode-coop`; соло-гра одним або кількома пожежниками.
- `history` — журнал партій на останній сторінці правил.
- Цифрова версія (Steam, 2018): обидва набори правил, одиночна гра й спільний/розділений екран, досягнення, хмарні збереження.

## Варіації й родичі
- Доповнення: Urban Structures (Brownstone, High Rise, інженер) · 2nd Story (два поверхи, драбини, сходи, вікна) · Extreme Danger (лабораторія, гараж, підвал/горище, d12, пошкоджені підлоги, протипожежні двері) · Veteran and Rescue Dog · Dangerous Waters (корабель і підводний човен, незламні перегородки) · Honor & Duty (метро, аеродром, піна) · Tragic Events (картки подій замість гарячих точок).
- Pandemic (`pandemic.md`) — та сама схема «дії → невідворотне поширення → ескалація»; Forbidden Desert (`forbidden-desert.md`) — кооп з поширенням загрози полем; Forest-fire model (`build-sim/forest-fire-model.md`) — поширення вогню як клітинний автомат.
- **Осі варіацій**: стадії загрози (дим → вогонь → вибух / один стан) · де стіни (у клітинах / на ребрах з HP) · ціль поширення (кубик-координата / картка / сусіди) · ескалація (гарячі точки множать кидки / шкала / нема) · ресурс програшу (втрати / пошкодження будівлі / обидва).

## Цікавинки для курсу
- Ескалація загрози як три правила одного кидка (дим+дим=вогонь, дим біля вогню=вогонь, кидок у вогонь=вибух) — 📎.
- Вибух хрестом + ударна хвиля, що летить крізь клітини вогню й зупиняється на першій «не-вогняній» / стіні / дверях — 🥉 (картка `blast-wave` з розповсюдженням).
- Flashover: ітерація до нерухомої точки (BFS від вогню через дим, стіни на ребрах — розриви графа) — 📎.
- Стіни на ребрах з HP 0/1/2 і двері з трьома станами: граф сусідства змінюється під час гри — 🥉.
- Кубики як координати (d6 × d8) + стрілки перенаправлення / перекид для зайнятої цілі — 🌱.
- Гарячі точки: каскад додаткових кидків + накопичення точок — 🌱; ролі-модифікатори AP (безкоштовні AP на рух/гасіння, подвійна ціна, командування чужим рухом) — 🥉.
- AI-порадник команди: пошук послідовності дій на 4 AP, що мінімізує очікувані вибухи й втрати — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` (стіни, зачинені двері) · `destructible-blocks` (рубання й вибухи) · `blast-wave` + `explode-area` (вибух хрестом, ударна хвиля) · `chain-reaction` (flashover, hazmat, flare up) · `spawn-random-cell` (дим і POI за кубиками) · `hidden-under-block` (жертва під «?») · `respawn` (збитий пожежник у швидкій) · `carrier-platform` (їзда на машинах) · `collect-quota` (7 жертв) · `keep-playing-after-win` (до 10) · `difficulty-levels` · `character-select` (спеціалісти) · `rule-variants` · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+smoke-fire-escalation` «Загроза має стадії: дим → вогонь → вибух за правилами накладання й сусідства» · entities/state · 📎.
  - `+shockwave-through-fire` «Ударна хвиля летить крізь клітини свого типу до першої іншої» · entities/combat · 🥉.
  - `+dice-coordinate-target` «Два кубики — координати клітини» · levels/generation · 🌱.
  - `+flare-up-reroll` «Ціль-гаряча точка дає додатковий кидок» · game-logic/waves · 🌱.
  - `+saved-action-points` «Невитрачені очки дій переходять на наступний хід (до ліміту)» · game-logic/opponent · 🌱.
  - `+wall-damage-collapse` «Стіни на ребрах з HP; спільний запас пошкоджень — програш» · entities/legality · 🥉.
  - `+fire-spread` · `+edge-walls` · `+supply-out-lose` · `+shared-field-coop` · `+action-points` · `+variable-player-powers` — уже пропонувались у корпусі; `+door-toggle` · `+redirect-arrows` · `+carry-victim-cost` · `+knockdown-to-respawn` · `+deck-gun-scatter` — дрібні.

## Пропозиції до словників
- `+effect:roll_dice` — кинути кубик(и) й використати результат як координату / відстань (Flash Point: d6 × d8 — клітина вогню).
- `+cond:wall_between` — між двома сусідніми клітинами стоїть ціла стіна чи зачинені двері (сусідство розірване).
- `+ui:doom-track` — шкала наближення поразки (пошкодження будинку 0–24, втрачені 0–4).
- `+card:smoke-fire-escalation` · `+card:shockwave-through-fire` · `+card:dice-coordinate-target` · `+card:flare-up-reroll` · `+card:saved-action-points` · `+card:wall-damage-collapse` — див. «Мапа на каталог».

## Джерела
- ⭐ [Правила Flash Point: Fire Rescue (PDF)](https://world-of-board-games.com.sg/docs/Flash-Point-Fire-Rescue.pdf) — склад, підготовка, 4 AP і ціни дій, просування вогню, вибух, ударна хвиля, спалах, збиття, POI, кінець гри; досвідчена гра: складність, машини, гармата, 8 спеціалістів, hazmat, гарячі точки, порядок фази; FAQ і варіанти.
- [Wikipedia](https://en.wikipedia.org/wiki/Flash_Point:_Fire_Rescue) — автор, видавці, Kickstarter, перелік доповнень.
- [Steam: Flash Point: Fire Rescue](https://store.steampowered.com/app/654220/Flash_Point_Fire_Rescue/) — цифрова версія RetroEpic (29.03.2018): родинні й досвідчені правила, соло, спільний екран.
- [Indie Boards & Cards](https://www.indieboardsandcards.com/our-games/flash-point-fire-rescue/) — сторінка гри й доповнень.
- YouTube: пошук «Flash Point Fire Rescue how to play».

## Непевне
- (?) Інтерфейс цифрової версії не бачив — вікна вище реконструйовані «(цифрова версія)»; Steam також позначає «Shared/Split Screen PvP», що дивно для коопу.
- (?) Точні стартові клітини 10 вогнів і 3 POI родинної гри — у PDF символи кубиків не витягнулись як текст.
- (?) Складність і кількість гарячих точок: «3 додаткові на Veteran/Heroic» і «2 для 3 пожежників / 3 для 4+» — у PDF два пункти поруч, чи вони сумуються, не певен.
- (?) Скільки дверних прорізів на звороті поля (8 — для лицьової сторони).
- (?) Обмеження «одна жертва за раз» для звичайного пожежника явно сказано лише для hazmat («only carry one item at a time»).
- (?) Мобільні версії цифрової гри — не перевіряв.
