---
title: From Dust
slug: from-dust
aka: [Project Dust]
family: dig-gravity
also: [build-sim]
klass: cursor
axes:
  field: layers
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2011
platforms: [Xbox 360, PC, PS3, web (Chrome)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/From_Dust", best: true, note: "суть: сферичний курсор, лава → камінь, вода розмиває ґрунт, рослини йдуть ґрунтом, тотеми й села, портал, Challenge 30 рівнів"}
  - {kind: other, url: "https://www.destructoid.com/?p=68309", note: "GDC Europe 2010 (Project Dust): шари камінь → ґрунт → вода/лава; ґрунт осідає, вода розмиває, лава холоне від води; кнопки демо"}
  - {kind: other, url: "https://www.engadget.com/2010-08-17-how-project-dusts-world-building-world-was-built.html", note: "техніка: камінь, пісок, рослини, вода, лава; увесь світ симулюється постійно, 30 fps; грязь замість згладжування"}
  - {kind: other, url: "https://kotaku.com/controlling-the-breath-of-a-god-with-from-dust-5806141", note: "Дихання: вдих RT кулі ґрунту/води/лави, видих LT, обмежений обʼєм; желе з води"}
  - {kind: other, url: "https://www.engadget.com/2011/07/26/from-dust-review/", note: "огляд: тверднення води, гасіння пожеж по всій мапі, тотеми від води/вогню, звʼязок сіл суходолом, вибухові рослини"}
  - {kind: other, url: "https://gamedeveloper.com/design/the-core-of-i-from-dust-i-", note: "інтервʼю Chahi: вогнестійкість рослин росте з часом, припливи, цикл вивержень"}
  - {kind: steam, url: "https://store.steampowered.com/app/33460/From_Dust/", note: "13 територій Story, 30 карт Challenge на час, онлайн-лідерборди"}
  - {kind: wiki, url: "https://fr.wikipedia.org/wiki/From_Dust", note: "пісок перекриває русло, лава холоне в гори, дельта за 10 хв"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=From+Dust+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [cursor-place, gravity-fall, cell-transform, interaction-table, height-levels, inventory-limit, temporary-modes, environment-death, sequential-levels, mode-select, leaderboard, time-bonus, +water-level-cell, +phase-transition, +erosion-flow, +terraform, +fire-spread, +growth-stages, +absorb-release-cursor, +telegraphed-disaster, +tide-cycle, +follower-goal-path]
proposes: ["+effect:inhale", "+effect:exhale", "+effect:flow", "+effect:erode", "+cond:height_diff", "+role:material", "+ui:breath-gauge", "+card:absorb-release-cursor", "+card:erosion-flow", "+card:telegraphed-disaster", "+card:tide-cycle", "+card:follower-goal-path"]
author: opus
date: 2026-11-09
---

# From Dust — божий курсор переносить ґрунт, воду й лаву по карті висот, а світ сам тече, твердне й заростає

## Суть
God-game Еріка Шаї: гравець — Дихання (Breath), сферичний курсор над архіпелагом, що вдихає кулю матерії — ґрунт, воду чи лаву — і видихає її деінде. Мета рівня — провести плем'я до тотемів і захистити села від цунамі, вивержень і пожеж. Описую лише **сітковий шар** — карту висот із шарами матеріалів, що постійно симулюється: ґрунт осипається, вода тече вниз і розмиває береги, лава холоне на камінь, рослини розростаються ґрунтом. Плем'я, сюжет і місії — лише абзацом тут: люди самі йдуть до тотема, коли є шлях суходолом, і ставлять село, яке дає Диханню нову силу.

## Поле і час
- Поле — карта висот (heightfield) над морем; у кожній точці — стовпчик шарів: **камінь** (основа) → **ґрунт/пісок** (на ньому ростуть рослини) → поверх течуть **вода** або **лава** (`field: layers`). Роздільність сітки — (?).
- Симулюється **увесь світ щокадру**, навіть поза камерою; 30 fps на Xbox 360 / PS3 / PC (Engadget, GDC Europe 2010).
- Час — real-time; зміни швидкі: за кілька хвилин перебудовуються острови, дельта може сформуватись за 10 хв (FR-вікі).
- Камера — вид згори/збоку на мапу, вільна; уся мапа видима (`info: full`).
- Події світу: припливи й відпливи, цикл вивержень вулкана, цунамі з попередженням шамана (`random: runtime` — з огляду «random disasters», ?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дихання (Breath) | player | обʼєм «легень», поточна матерія | курсор-сфера: вдихає кулю матерії з поверхні, видихає в іншому місці; активує сили |
| Камінь | terrain | висота | основа рельєфу; не тече; з'являється з охололої лави |
| Ґрунт / пісок | terrain | товщина шару | під гравітацією осипається й вирівнюється; розмивається водою; на ньому ростуть рослини |
| Вода | terrain | глибина | тече вниз по рельєфу; потік прорізає русла, перекритий — стає озером або меандром |
| Грязь (mud) | terrain | — | ґрунт із водою: «твердість ґрунту, в'язкість води»; згладжує русла |
| Лава | hazard | глибина | тече як вода, спалює все, чого торкнеться; холоне в камінь (від води — одразу) |
| Рослинність | terrain | стадія: молода → квітуча → доросла → мертва | розростається ґрунтом; тимчасово тримає воду; горить |
| Вогняне дерево | hazard | — | «дерева, що вибухають вогнем» — підпалює довкілля (?) |
| Вибухова рослина | hazard | — | вибухає (умова — ?) |
| Вогонь | hazard | — | ширить рослинністю; повільніше там, де рослини давно не турбовані |
| Вулкан | spawner | цикл вивержень | періодично виливає лаву |
| Цунамі | hazard | — | хвиля води на берег після попередження шамана |
| Плем'я (люди) | ally | — | самі йдуть до тотема шляхом суходолом; гинуть у воді/лаві/вогні |
| Тотем | zone | сила, яку дає | поруч плем'я ставить село; село відкриває силу Дихання |
| Село | ally | захисна «пісня» (вода / вогонь) | розростає рослинність довкола; з піснею вода чи вогонь його не беруть |
| Камінь знань / реліквія | pickup | — | вчить пісню відштовхувати воду або вогонь; ділиться між селами, якщо є шлях суходолом |
| Портал | gate | — | відкривається, коли біля кожного тотема стоїть село |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(inhale)` → ЯКЩО `custom: «під курсором ґрунт, вода або лава»` and `counter(breath, <, capacity)` → ТО `custom: «зняти кулю матерії з верхнього шару під курсором»`, `counter(breath, +n)`.
- КОЛИ `input(exhale)` → ЯКЩО `counter(breath, >, 0)` → ТО `custom: «висипати матерію під курсор — вона лягає зверху на стовпчик і далі симулюється»`, `counter(breath, −n)`; лаву можна «капати» тонким струменем.
- КОЛИ `tick` → ЯКЩО `custom: «стовпчик ґрунту вищий за сусіда більше за кут укосу»` → ТО `custom: «ґрунт осипається до нижчого сусіда»` (вирівнювання під гравітацією).
- КОЛИ `tick` → ЯКЩО `custom: «рівень води в клітині вищий, ніж у сусіда»` → ТО `custom: «вода перетікає вниз по карті висот»`; лава — так само, але в'язкіше (?).
- КОЛИ `tick` → ЯКЩО `custom: «вода тече по ґрунту»` → ТО `custom: «ерозія: ґрунт зноситься з русла й осідає нижче за течією»` — так виникають річки, дельти, обвали берегів.
- КОЛИ `contact(water, soil)` → ЯКЩО `custom: «багато осаду у воді»` → ТО `transform(water, mud)`.
- КОЛИ `contact(lava, water)` → ТО `transform(lava, rock)`; КОЛИ `tick` → ЯКЩО `custom: «лава зупинилась»` → ТО `transform(lava, rock)` згодом (?).
- КОЛИ `contact(lava, vegetation|village|villager)` → ТО `custom: «спалити»`: `transform(vegetation, fire)`, `disappear(villager)`.
- КОЛИ `tick` → ЯКЩО `cell(target, soil)` and `custom: «умови життя рослини виконано»` → ТО `custom: «рослинність розростається на сусідню клітину»`; стадії старіють за часом.
- КОЛИ `contact(fire, vegetation)` → ТО `transform(vegetation, fire)`; ЯКЩО `custom: «місце давно не турбоване»` → ТО вогонь повільніший.
- КОЛИ `custom: «вогняне дерево спалахнуло»` → ТО `spawn(fire)` довкола (?); вибухова рослина → `explode(circle, r)` (?).
- КОЛИ `timer(tide)` → ТО `custom: «рівень моря піднімається / опускається»`; на відпливі рослини відростають, люди можуть пройти.
- КОЛИ `timer(eruption)` → ТО `spawn_at(lava, volcano)`.
- КОЛИ `schedule(disaster)` → ТО `message(шаман попереджає)`, далі `spawn_at(water, edge)` — цунамі.
- КОЛИ `input(power: jellify)` → ТО `set_state(water, jelly, dur)` — вода не тече, її можна вирізати «траншеями» Диханням.
- КОЛИ `input(power: extinguish)` → ТО `custom: «загасити всі пожежі на мапі»`.
- КОЛИ `input(power)` → ТО `custom: «осушити озеро / виростити ліс / підняти гору»` — сили з опису Steam, назви — (?).
- КОЛИ `custom: «плем'я отримало команду йти до тотема»` → ЯКЩО `path_exists(villager, totem)` → ТО `custom: «люди йдуть самі»`; інакше стоять (гравець має проклати суходіл).
- КОЛИ `reach(villager, totem)` → ТО `spawn_at(village, totem)`, `custom: «Дихання отримує силу тотема»`.
- КОЛИ `picked(villager, knowledge_stone)` → ТО `set_state(village, repel_water|repel_fire)`; ЯКЩО `path_exists(village_a, village_b)` → ТО знання поширюється на інше село.
- КОЛИ `contact(water|fire, village)` → ЯКЩО `state(village, repel_water|repel_fire)` → ТО `block` (обходить село); інакше `disappear(village)`.
- КОЛИ `custom: «біля кожного тотема стоїть село»` → ТО `spawn(portal)`, `next_level`.
- Перемога: села біля всіх тотемів → портал · Поразка: формальної нема, загибель племені фактично зупиняє проходження (?) · Рахунок: лише Challenge — час на онлайн-лідерборді.

## Керування і ввід
- Геймпад: RT — вдих матерії під курсором, LT — видих (Kotaku); курсор — стік.
- Демо 2010: A — додати, B — прибрати, X — згладити, LB/RB — менше/більше ефекту (Destructoid); у фіналі розкладка інша (?).
- Сили (тотемів) — окремою дією, тимчасові; люди — непрямо: вказати тотем/ціль, далі йдуть самі (`control: indirect`).

## Вікна, меню, HUD
- `main-menu`: Story · Challenge → `mode-select`.
- `level-select` (`world-map`-подібно) — 13 територій Story (?) щодо мапи.
- `game-screen`: мапа, курсор-Дихання з кулею матерії, кнопки сил; `breath-gauge` (?) обʼєму матерії.
- `puzzle-select` — 30 карт Challenge з часом; `leaderboard` онлайн.
- `dialogue-window` — попередження шамана й сюжетні вставки.
- `codex-window` (?) — пам'ять племені / знання.
- Переходи: main-menu → рівень → (портал) наступна територія.

## Фічі поза полем
- `levels-sequential` — 13 територій Story; `mode-time-attack` — 30 карт Challenge, `leaderboard-online`.
- Сили відкриваються тотемами по ходу (`ability-gating`-подібно).
- Нема мультиплеєра й редактора (у 2010 «залежить від продажів»).

## Варіації й родичі
- У сімʼї: [sandspiel.md](sandspiel.md), [the-powder-toy.md](the-powder-toy.md), [noita.md](noita.md) — клітинні матеріали без карти висот; [wheres-my-water.md](wheres-my-water.md) — копання ґрунту під воду; [scorched-earth.md](scorched-earth.md) — земля, що осідає.
- Поза сімʼєю: Timberborn (`build-sim`, вода як рівень у клітині), Populous (підняти/опустити землю), Black & White (рука бога).
- **Осі варіацій**: поле «пікселі падають (falling sand) / карта висот із шарами (From Dust) / вокселі»; вода «частинки / рівень у клітині / heightfield»; бог «рука-курсор переносить матерію / кнопки підняти-опустити / непряма віра»; лава «твердне від води / з часом / ніколи».

## Цікавинки для курсу
- Карта висот із шарами (камінь + ґрунт + вода) і перетікання до нижчого сусіда — 🥈 (стійкість, порядок оновлення).
- Осипання ґрунту за кутом укосу — 📎.
- Ерозія: вода зносить ґрунт і відкладає нижче — 🥇 (рівновага осаду, не «дірки»).
- Лава → камінь при контакті з водою — 🌱 поверх рідини.
- Курсор-«пилосос»: вдих/видих матерії з обмеженим обʼємом — 📎.
- Поширення рослин і вогню з «вогнестійкістю», що росте з часом — 📎.
- Плем'я йде лише суходолом: `path_exists` по клітинах без води/лави щокадру — 🥉.

## Мапа на каталог
- Є: `cursor-place` ↔ видих матерії під курсор · `gravity-fall` ↔ осипання ґрунту · `cell-transform` ↔ лава → камінь, вода → грязь · `interaction-table` ↔ матеріали × матеріали · `height-levels` ↔ карта висот · `inventory-limit` ↔ обʼєм Дихання · `temporary-modes` ↔ сили (желе з води) · `environment-death` ↔ люди в лаві/воді · `sequential-levels` · `mode-select` · `leaderboard` + `time-bonus` ↔ Challenge.
- **Нема** → пропозиції карток:
  - `+absorb-release-cursor` «Курсор вбирає матерію й висипає деінде» · entities/interact · 📎 · слот {capacity}.
  - `+erosion-flow` «Вода зносить ґрунт і відкладає нижче» · entities/interact · 🥇.
  - `+telegraphed-disaster` «Катастрофа з попередженням і відліком» · game-logic/waves · 🌱.
  - `+tide-cycle` «Рівень води циклічно росте й спадає» · game-logic/time · 🌱.
  - `+follower-goal-path` «Підопічні йдуть до цілі самі, якщо є шлях» · entities/move · 🥉.
  - Повтори: `+water-level-cell` (Timberborn), `+phase-transition` (Noita, Powder Toy), `+terraform` (Timberborn), `+fire-spread` (Noita), `+growth-stages`.

## Пропозиції до словників
- `+effect:inhale` / `+effect:exhale` — курсор знімає матерію з поля в «запас» і висипає назад (не `pickup`/`place`: матерія — шар висоти, не сутність).
- `+effect:flow` — повтор: рідина перетікає до нижчого сусіда (Timberborn, Scorched Earth).
- `+effect:erode` — повтор (Where's My Water?): потік зносить шар ґрунту.
- `+cond:height_diff` — повтор: різниця висот із сусідом більша за поріг (кут укосу).
- `+role:material` — повтор: шар матерії в клітині (камінь, ґрунт, вода, лава).
- `+ui:breath-gauge` — скільки матерії несе курсор.

## Джерела
- ⭐ [Wikipedia: From Dust](https://en.wikipedia.org/wiki/From_Dust) — сферичний курсор, лава твердне, вода розмиває, рослини йдуть ґрунтом, шамани й катастрофи, тотеми → села → портал, Challenge 30 рівнів, платформи й дати.
- [Destructoid: Project Dust на GDC Europe](https://www.destructoid.com/?p=68309) — шари рельєфу, осідання ґрунту, течія й ерозія, лава холоне від води, грязь, стадії рослин, кнопки A/B/X/LB/RB.
- [Engadget/Joystiq: як будували світ](https://www.engadget.com/2010-08-17-how-project-dusts-world-building-world-was-built.html) — увесь світ симулюється, 30 fps, грязь, русла.
- [Kotaku: Breath of a God](https://kotaku.com/controlling-the-breath-of-a-god-with-from-dust-5806141) — вдих/видих тригерами геймпада, обмежений обʼєм, желе з води.
- [Engadget: огляд](https://www.engadget.com/2011/07/26/from-dust-review/) — сили (тверда вода, гасіння пожеж), тотеми від води/вогню, знання між селами суходолом, вибухові рослини, погана навігація людей.
- [Game Developer: The Core of From Dust](https://gamedeveloper.com/design/the-core-of-i-from-dust-i-) — вогнестійкість, припливи, вулканічний цикл, «прості правила, що сходяться».
- [Steam: From Dust](https://store.steampowered.com/app/33460/From_Dust/) — 13 територій, 30 карт Challenge, лідерборди, перелік катастроф.
- [Wikipedia FR](https://fr.wikipedia.org/wiki/From_Dust) — пісок перекриває річку, лава → гори, дельта за 10 хв.

## Непевне
- (?) Роздільність сітки й точна модель (віртуальні труби, порядок шарів у стовпчику) — джерела кажуть лише «камінь, ґрунт, вода/лава» і «прості правила».
- (?) Чи лава холоне сама з часом, чи лише від води: Wikipedia — «cools into rock», Destructoid — «when water is dropped on it».
- (?) Назви сил (Infinite Earth, Evaporation, Amplify тощо) — у відкритих джерелах лише описи: желе з води, гасіння пожеж, осушити озеро, виростити ліс, підняти гору.
- (?) Вогняне дерево й вибухові рослини — тригер і радіус невідомі.
- (?) Формальна поразка: огляди кажуть, що гра не попереджає про загибель племені; чи є рестарт рівня — не перевірено.
- (?) Випадковість: цунамі й виверження можуть бути скриптовані рівнем, а не випадкові.
