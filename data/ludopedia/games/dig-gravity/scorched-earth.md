---
title: Scorched Earth
slug: scorched-earth
aka: ["Scorched Earth: The Mother of All Games", Scorch]
family: dig-gravity
also: [tactics]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: score
year: 1991
platforms: [MS-DOS]
links:
  - {kind: other, url: "https://trwglibsccninuamefls.supabase.co/storage/v1/object/public/assets/scorched-earth/scorched-earth.txt", best: true, note: "текст мануалу 1.5 (сторонній хостинг): усі зброї за групами, захист, фізика, економіка, клавіші, типи AI"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Scorched_Earth_(video_game)", note: "огляд: руйнований рельєф, земляна зброя, засипаний танк, стіни, вітер, до 10 гравців, версії"}
  - {kind: official, url: "https://www.whicken.com/scorch/", note: "сайт автора: завантаження 1.2 і 1.5, збірка Totally Scorched з HTML-мануалом"}
  - {kind: other, url: "https://www.whicken.com/scorch/faq.html", note: "FAQ і історія версій: Liquid Dirt, Simultaneous/Synchronous, ринок, порядок ходу"}
  - {kind: other, url: "https://tcrf.net/Scorched_Earth", note: "вирізане: Dirt Tower, Popcorn Bomb, Jump Jets, щити-телепорти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Scorched+Earth+1991+DOS+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [projectile-shot, explode-area, gravity-fall, hp-damage, wrap-edges, shop-between-levels, shop-catalog, shop-buyback, shop-window, inventory, inventory-items, inventory-limit, hot-seat, ai-opponent, ai-random, turn-enforcement, score-records, save-game, game-settings, settings-elements, keyboard-controls, status-panel, end-screen, +destructible-terrain, +falling-dirt, +dirt-weapons, +liquid-dirt-flow, +roll-downhill, +bury-tank, +angle-power-aim, +wind, +wall-types, +homing-guidance, +parachute-fall-damage, +interest-on-cash, +free-market-prices, +ai-personality-types]
proposes: ["+trigger:landed", "+trigger:round_end", "+effect:flow", "+effect:reload", "+effect:deflect", "+cond:buried", "+ui:wind-indicator", "+ui:angle-power-readout", "+window:match-setup", "+window:round-summary", "+feature:turn-order-options", "+card:falling-dirt", "+card:dirt-weapons", "+card:liquid-dirt-flow", "+card:angle-power-aim", "+card:wall-types", "+card:ai-personality-types"]
author: opus
date: 2026-11-09
---

# Scorched Earth — артилерійська дуель танків, де рельєф і зброя, і пастка, і ресурс

## Суть
До 10 танків стоять на горбистому піксельному рельєфі й по черзі стріляють, задаючи кут і потужність; снаряд летить з гравітацією і вітром. Ядро для корпусу — **рельєф як матеріал**: вибухи вигризають землю, земля без опори осідає, танки падають, а окрема група зброї **насипає** землю (засипати суперника) чи **виймає** її (відкопатись, підкопати). Між раундами — магазин зброї й захисту за гроші, зароблені влучаннями. Описую рельєфний шар детально, балістику й економіку — коротше: за чергою це «межовий випадок, контраст до клітинної фізики».

## Поле і час
- Поле — один екран бічного виду; рельєф — двовимірна маска пікселів «земля / повітря» (по суті квадратна сітка 320×200 або 640×480 залежно від режиму — розміри екранних режимів з FAQ; масштаб світу — опція Scale).
- Генерація ландшафту: опції Bumpiness, Slope, Flatten Peaks, Random Land і частка «сканованих» гірських хребтів (1.5); небо — Plain, Stormy, Stars, Shaded, Sunset, Cavern, Black, Random.
- Межі: ліва/права стіна і стеля одного з типів (Concrete, Padded, Rubber, Spring, Wraparound) або Random/Erratic; снаряд за межею екрана відстежується ще Borders Extend пікселів (типово 75).
- Хід: гравець цілиться й стріляє; фізика польоту і вибухів дограється в реальному часі, потім земля осідає. Режими: звичайний покроковий, Simultaneous (усі стріляють будь-коли, до 99 снарядів у повітрі), Synchronous (усі цілять, потім залп разом).
- Партія — N раундів (1–1000, типово 10); раунд — до останнього живого танка.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Танк | player | енергія, гроші, інвентар, кут, потужність | стоїть на землі; падає, якщо під ним зникла опора (Tanks Fall); з паливом їде, вгору дорожче |
| Танк комп'ютера | enemy | тип AI | 8 типів від Moron до Cyborg; дражнить перед пострілом і смертю |
| Земля (піксель) | terrain | — | руйнується вибухом; без опори падає (ймовірність — опція Suspend Dirt) |
| Повітря | static | — | порожнеча; земля в повітрі може «зависнути» при Suspend Dirt > 0 % |
| Стіни й стеля | static | тип | Concrete — зупиняє; Padded — відбиває з втратою; Rubber — відбиває; Spring — відбиває з прискоренням; Wraparound — тор |
| Снаряди (Missile, Nuke, Leapfrog, MIRV, Death's Head, Funky Bomb) | projectile | радіус, шкода, боєголовки | летять балістично; вибух кругом; MIRV розділяється в апогеї на 5, Death's Head — на 9 |
| Napalm / Hot Napalm | projectile | — | розтікається по рельєфу й горить; глибша калюжа — більша шкода |
| Roller (Baby / звичайний / Heavy) | projectile | — | після приземлення котиться вниз до западини чи танка, тоді вибухає; щит змушує скотитись |
| Earth Destroying: Riot Charge / Riot Blast | projectile | — | прибирає клин землі біля дула — відкопатись |
| Riot Bomb / Heavy Riot Bomb | projectile | — | вибух прибирає кулю землі, танкам шкоди нема |
| Digger / Sandhog (Baby / звичайний / Heavy) | projectile | — | тунелюють у землі; Digger гасне об танк, Sandhog має заряд, що бʼє танк знизу |
| Earth Producing: Dirt Clod / Dirt Ball / Ton of Dirt | projectile | розмір | вибух — куля землі; Ton of Dirt здатна поховати танк |
| Liquid Dirt | projectile | — | рідка земля тече, заповнює ями й вирівнює схил (шлях для Roller) |
| Dirt Charge | projectile | — | клин землі в повітря |
| Earth Disrupter | projectile | — | осаджує завислу землю (корисний при Suspend Dirt > 0) |
| Plasma Blast / Laser | projectile | батареї | плазма бʼє довкола танка; лазер — промінь крізь гори й щити |
| Tracer / Smoke Tracer | projectile | — | без шкоди, лише показує траєкторію (Smoke лишає слід) |
| Щити (Shield, Force, Heavy, Super Mag) | ally | міцність | поглинають шкоду вибуху; Force відбиває снаряди; Super Mag — ще й імунітет до лазера |
| Mag Deflector | ally | кілька ударів | штовхає снаряд угору над танком |
| Парашут | pickup | поріг (типово 5) | гасить шкоду падіння понад поріг, крім приземлення на ворожий танк |
| Батарея / паливо / Contact Trigger / системи наведення | pickup | 10 енергії / 10 палива | лікування й плазма / рух / вибух при контакті / Heat, Ballistic, Horizontal, Vertical, Lazy Boy |
| Блискавка, метеорити | hazard | опція Hostile Environment | випадково бʼють танки з неба |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(aim, angle|power)` → ТО `custom: «змінити кут / потужність дула (Shift — повільніше, Alt — по 1)»`.
- КОЛИ `input(fire)` → ЯКЩО `turn_of(tank)` → ТО `spawn(projectile)` і `custom: «політ за кутом, потужністю, гравітацією (0.05–10), вітром і вʼязкістю повітря»`.
- КОЛИ `edge(projectile)` → ТО за типом стін: Concrete — `block`, Rubber/Padded/Spring — `bounce`, Wraparound — `wrap`, без стін — `disappear`.
- КОЛИ `contact(projectile, ground|tank)` → ТО `explode(circle, r)`: `set_cell(dirt → empty)` у радіусі і `damage(n)` танкам у радіусі.
- КОЛИ `after(explode)` → ЯКЩО `not supported(dirt)` and `prob(1 − suspend_dirt)` → ТО `fall(dirt)` — земля осідає вниз до опори.
- КОЛИ `after(explode)` → ЯКЩО `not supported(tank)` and `mode(tanks_fall)` → ТО `fall(tank)`.
- КОЛИ `custom: «танк приземлився»` → ЯКЩО `custom: «шкода падіння > поріг»` and `has(tank, parachute)` and not `occupied(below, enemy_tank)` → ТО `custom: «шкоди нема»`; інакше `damage(n)` (з великої висоти — знищення).
- КОЛИ `contact(dirt_clod|dirt_ball|ton_of_dirt, any)` → ТО `explode(circle, r, into: dirt)` — куля землі; танк усередині засипаний.
- КОЛИ `input(fire)` → ЯКЩО `custom: «танк засипаний»` → ТО `custom: «постріл вибухає поруч і може поранити свій танк»`; рятує Riot Charge.
- КОЛИ `input(fire, riot_charge|riot_blast)` → ТО `set_cell(wedge біля дула, empty)` без шкоди танкам.
- КОЛИ `contact(liquid_dirt, ground)` → ТО `custom: «земля тече вниз і заповнює ями»`.
- КОЛИ `contact(digger|sandhog, ground)` → ТО `custom: «тунелює, вирізаючи землю»`; ЯКЩО `occupied(cell, tank)` → Digger `disappear`, Sandhog `explode`.
- КОЛИ `contact(roller, ground)` → ТО `roll(roller)` вниз схилом; КОЛИ `custom: «западина»` or `contact(roller, tank)` → ТО `explode`; ЯКЩО `state(tank, shield)` → ТО `roll` повз танк.
- КОЛИ `contact(napalm, ground)` → ТО `custom: «вогонь розтікається вниз рельєфом»`, `damage(n)` за глибиною калюжі.
- КОЛИ `custom: «MIRV / Death's Head досяг апогею»` → ТО `split(5 | 9 warheads)`; ЯКЩО влучив до апогею → `custom: «не вибухає»`.
- КОЛИ `contact(explosion, tank)` → ЯКЩО `state(tank, shield)` → ТО `custom: «щит поглинає шкоду, слабшає»`; Force Shield → `bounce(projectile)`.
- КОЛИ `in_range(projectile, tank)` → ЯКЩО `has(tank, mag_deflector)` → ТО `custom: «відштовхнути снаряд угору»`.
- КОЛИ `input(guidance)` → ЯКЩО `has(tank, guidance)` → ТО `custom: «наступний снаряд наводиться (Heat — на найближчий танк у радіусі; Ballistic — підбирає потужність з поправкою на вітер)»`; після пострілу наведення скидається.
- КОЛИ `input(move, dir)` → ЯКЩО `has(tank, fuel)` → ТО `move(tank, dir)` і `take(fuel, n)` (вгору більше).
- КОЛИ `input(use, battery)` → ТО `heal(tank, 10)`.
- КОЛИ `hp_zero(tank)` → ТО `disappear(tank)` з вибухом.
- КОЛИ `turn_start` → ЯКЩО `mode(changing_wind)` → ТО `custom: «вітер змінюється»` (Max Wind 0–500).
- КОЛИ `rng(p)` → ЯКЩО `mode(hostile_environment)` → ТО `damage(tank)` блискавкою/метеором.
- КОЛИ `count(tank, =, 1)` → ТО `custom: «кінець раунду»`, `currency(+interest × cash)` (типово 5 %), магазин.
- КОЛИ `input(buy, item)` → ЯКЩО `has(player, price)` → ТО `give(player, item)`, `currency(−price)`; понад 99 штук — націнка ≈20 %; Free Market — ціни від попиту.
- КОЛИ `input(retreat)` → ТО `disappear(tank)` без очок (самогубство коштує грошей).
- Перемога: найбільше очок після останнього раунду. Поразка в раунді: танк знищено. Рахунок: Basic (вбивства й виживання), Standard (за шкоду танкам і щитам), Greedy (у фіналі — чиста вартість майна).

## Керування і ввід
- Стрілки ←/→ — кут, ↑/↓ — потужність, PgUp/PgDn — потужність швидко; Shift — повільніше, Alt — по одиниці; Tab / Shift-Tab — перебір зброї; Space/Enter — постріл.
- Гарячі клавіші статус-бару: b батарея, p парашути, s/e щити, g наведення, f паливо (далі стрілки рухають танк, Esc — кінець), `-` тригери; t — панель танка, i — інвентар, u — оновити статус, 0–9 — інфо про танк, r — відступ, F1/Alt-S — системне меню.
- Миша: правий клік — точна ціль для наведення; джойстик і Gravis Gamepad (1.1, 1.5).
- Hotseat до 10 гравців на одному ПК; черга ходу — random, losers-first, winners-first, round-robin.

## Вікна, меню, HUD
- `main-menu` / `match-setup`: кількість гравців і раундів, Sound, Hardware, Economics (відсотки, стартові гроші, Computers Buy, Free Market, Scoring), Physics (вітер, гравітація, вʼязкість, стіни, Suspend Dirt, Tanks Fall), Landscape, Play Options (режим ходу, порядок, Talk) (?) — назви підменю з мануалу/памʼяті.
- `game-screen`: рельєф, танки, рядок статусу — гравець, кут, потужність, вітер, поточна зброя (`wind-indicator`, `angle-power-readout`, `status-panel`).
- `shop-window` (buying screen): сторінки зброї і «misc», ціни, кількість; Space — купити пачку, Esc — завершити; `confirm-dialog` продажу (сума пропозиції, a — прийняти, r — відмовитись).
- `inventory-window` (i), панель танка (t), `custom-window` «No kibitzing» (k — ховає екран від сусідів у hotseat).
- `round-summary` / `end-screen`: місця, очки, типи комп'ютерних гравців; системне меню (`pause-menu`): Save/Restore/Restart, Mass Kill, Quit, очистити дим трасерів.
- Переходи: setup → бій → кінець раунду → магазин → бій …; сейв — лише з магазину.

## Фічі поза полем
- `custom-rules`: майже кожен параметр фізики, економіки й ландшафту — опція (CGW 1993: «найконфігурованіша артилерійська гра»).
- `ai-opponent-levels`: Moron (випадково), Shooter (пряма лінія), Poolshark (рикошет від стін), Tosser (пристрілюється), Chooser, Spoiler (майже точно, плутає вʼязкість), Cyborg (бʼє слабких/лідера/кривдників), Unknown.
- Команди (1.5, три види), режими Simultaneous і Synchronous; «гра без людей» — AI доборюються самі, можна прискорити.
- `save-slots` (з магазину), Talk-файли з репліками танків, `remap-controls` — нема (?).

## Варіації й родичі
- Предки: Tanx (ZX Spectrum, 1983); Artillery-ігри 70–80-х. Нащадки: Scorched 3D, Scorched Earth 2000, Atomic Tanks (atanks), Pocket Tanks, Worms (загони + руйнований рельєф), Liero (real-time з копанням).
- У корпусі: [noita.md](noita.md), [the-powder-toy.md](the-powder-toy.md), [sandspiel.md](sandspiel.md) — пікселі з фізикою; [dig-dug.md](dig-dug.md), [boulder-dash.md](boulder-dash.md) — клітинна гравітація; [terraria-liquids.md](../build-sim/terraria-liquids.md) — рідина в тайлах.
- **Осі варіацій**: рельєф після вибуху — «дірка висить / осідає стовпцями / сиплеться піском»; земля як зброя — «лише руйнує / ще й насипає / тече рідиною»; межі — «стіна / відбиття / тор / безодня»; хід — «по черзі / одночасно (wego) / real-time».

## Цікавинки для курсу
- Осідання землі стовпцями після вибуху: «кожен піксель падає, доки під ним порожньо» — 📎 (heightmap) або 🥉 (довільна маска з печерами).
- Земляна зброя: вибух з продуктом `into: dirt` + перевірка «танк засипаний» → самопошкодження — 🥉.
- Liquid Dirt: рідина, що стікає й заповнює ями — 🥈 (клітинний автомат рідини на рельєфі).
- Roller: снаряд котиться вниз схилом до западини — 📎.
- Типи стін (блок / відбиття з втратою / пружина / тор) як одна функція `edge` — 📎.
- AI-«характери»: Moron → Tosser (пристрілювання бінпошуком) → Spoiler (точна балістика з вітром) — 🥉/🥈.
- Магазин між раундами з відсотками на залишок і ринковими цінами — 🥉.

## Мапа на каталог
- Є: `projectile-shot` ↔ снаряд · `explode-area` ↔ кругові вибухи · `gravity-fall` ↔ падіння танків і землі · `hp-damage` ↔ енергія танка · `wrap-edges` ↔ Wraparound · `shop-between-levels` / `shop-catalog` / `shop-buyback` / `shop-window` · `inventory` / `inventory-items` / `inventory-limit` (99) · `hot-seat` · `ai-opponent` / `ai-random` (Moron) · `turn-enforcement` · `score-records` · `save-game` · `game-settings` / `settings-elements` · `keyboard-controls` · `status-panel` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+falling-dirt` «Земля без опори осідає (з імовірністю)» · entities/move · 📎 · слоти {suspend_pct}.
  - `+dirt-weapons` «Снаряд насипає/виймає землю» · entities/combat · 🥉 · слоти {shape: circle|wedge|tunnel, into: dirt|empty}.
  - `+liquid-dirt-flow` «Рідка земля заповнює ями» · entities/move · 🥈.
  - `+angle-power-aim` «Постріл за кутом і силою з балістикою й вітром» · entities/combat · 🥉 · слоти {gravity, wind, viscosity}.
  - `+wall-types` «Поведінка снаряда на межі поля» · entities/move · 📎 · слоти {concrete, padded, rubber, spring, wrap}.
  - `+ai-personality-types` «Набір AI-характерів різної точності» · game-logic/opponent · 🥈.
  - Також: `+destructible-terrain`, `+roll-downhill`, `+bury-tank`, `+wind`, `+homing-guidance`, `+parachute-fall-damage`, `+interest-on-cash`, `+free-market-prices`.

## Пропозиції до словників
- `+trigger:landed` — повтор: танк/снаряд торкнувся землі після падіння (шкода падіння, парашут).
- `+trigger:round_end` — повтор: лишився один танк → гроші, магазин.
- `+effect:flow` — повтор: рідина (Liquid Dirt, Napalm) стікає й заповнює ями.
- `+effect:reload` — повтор (тут: батарея/паливо як витратні, слабко).
- `+effect:deflect` — змінити напрям снаряда силовим полем, не зіткненням (Mag Deflector, Force Shield).
- `+cond:buried` — сутність повністю засипана (вибух власного пострілу).
- `+ui:wind-indicator` — сила й напрям вітру; `+ui:angle-power-readout` — кут і потужність дула.
- `+window:match-setup` / `+window:round-summary` — повтори.
- `+feature:turn-order-options` — порядок ходу: випадково / першими ті, хто програє / переможці / по колу.

## Джерела
- ⭐ [Мануал 1.5 (текст)](https://trwglibsccninuamefls.supabase.co/storage/v1/object/public/assets/scorched-earth/scorched-earth.txt) — Standard / Energy / Earth Destroying / Earth Producing, захист, наведення, фізичні опції з діапазонами, економіка, Scoring, клавіші, типи AI.
- [Wikipedia](https://en.wikipedia.org/wiki/Scorched_Earth_(video_game)) — засипаний танк відстрілюється, падіння танка, типи стін, вітер, до 10 гравців, версії 1.0–1.5.
- [whicken.com/scorch](https://www.whicken.com/scorch/) і [FAQ](https://www.whicken.com/scorch/faq.html) — завантаження, історія версій, режими ходу, ринок.
- [TCRF](https://tcrf.net/Scorched_Earth) — вирізані предмети (лише з результатів пошуку).

## Непевне
- (?) Енергія танка 100 і звʼязок «енергія обмежує максимальну потужність пострілу» — з памʼяті, не з відкритого тексту.
- (?) Точні назви підменю головного екрана; розміри поля залежать від графічного режиму (320×200 / 640×480 — з FAQ, як режими екрана).
- (?) Як саме осідає земля (стовпцями чи пікселями) — мануал каже лише «airborne dirt falls».
- (?) Хостинг мануалу — сторонній bucket; первинне джерело — HTML-мануал у збірці Totally Scorched.
- (?) Перепризначення клавіш — не бачив.
