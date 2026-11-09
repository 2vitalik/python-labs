---
title: Phoenix Point
slug: phoenix-point
aka: []
family: tactics
also: [build-sim]
klass: figure
axes:
  field: layers
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2019
platforms: [PC, Mac, PS4, Xbox One, Stadia]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Phoenix_Point", best: true, note: "дві дії, зупинка при виявленні, прицілювання по частинах тіла, балістика промахів, Will, мутації ворогів, геоскейп, фракції"}
  - {kind: other, url: "https://phoenixpoint.wiki.fextralife.com/Combat", note: "Fextralife: частки AP за зброю, синя/жовта зона руху, два кола розкиду, броня частин тіла, вибухи, Will, overwatch, туман, слиз, вогонь"}
  - {kind: other, url: "https://phoenixpoint.wiki.fextralife.com/Stats", note: "Fextralife: Strength/Willpower/Speed/Perception/Stealth/Accuracy; кровотеча, отрута, параліч, вірус, паніка"}
  - {kind: steam, url: "https://store.steampowered.com/app/839770/Phoenix_Point/", note: "вільне прицілювання, адаптивний ворог, фракції, DLC"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Phoenix+Point+gameplay+free+aim", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, projectile-shot, shoot-burst, line-of-sight-attack, explode-area, destructible-blocks, status-effects, fog-of-war, reachable-highlight, inventory-items, inventory-limit, unit-xp-skills, ai-opponent, world-map, difficulty-levels, save-autosave, player-camera, +action-points, +cover-system, +overwatch, +free-aim-spread, +body-part-targeting, +limb-disable, +armor-per-part, +armor-shred, +stray-bullet-hits, +will-points-panic, +return-fire, +spot-interrupt, +enemy-evolution, +hazard-tiles]
proposes: ["+trigger:sighted", "+trigger:attacked", "+trigger:enemy_moved", "+cond:ap", "+cond:part_disabled", "+effect:disable_part", "+effect:shred", "+effect:interrupt_move", "+effect:panic", "+effect:mutate", "+role:body-part", "+ui:spread-circles", "+ui:part-info-box", "+ui:ap-bar-quarters", "+ui:will-points", "+ui:overwatch-cone", "+window:first-person-aim", "+window:geoscape", "+window:mutation-lab"]
author: opus
date: 2026-11-09
---

# Phoenix Point — XCOM від автора X-COM, але куля летить фізично: цілишся в руку, а не в «78 %»

## Суть
Покрокова тактика загону проти мутантів на мапі з поверхами, з геоскейпом зверху — як [xcom](xcom.md). Відмінності: **вільне прицілювання** — кожна куля летить за конусом розкиду з реальною балістикою, промах може влучити в іншого (і свого) або зруйнувати укриття; ворог складається з **частин тіла** з окремими HP і бронею — відстрілена рука прибирає зброю, нога — рух; **AP дробові** (дії коштують ¼–¾ запасу) замість «двох дій»; **Will Points** — витратна воля для навичок, яка падає від втрат і веде до паніки; ворог **еволюціонує** — успішні мутації розмножуються. Тут описано різницю, спільне з XCOM — у її файлі.

## Поле і час
- Сітка з поверхами в 3D (руйнівні будівлі, висота); процедурні мапи.
- Хід гравця: кожен солдат витрачає свій запас AP у будь-якому порядку; AP відновлюються на початку ходу. Потім хід інопланетян.
- Рух: **синя** зона — після руху ще вистачить AP на обрану дію; **жовта** — дійти можна, діяти вже ні.
- Видимість: ворог прихований, доки його не помітили (Perception проти Stealth), але діє і в тумані; помічений ворог **зупиняє** рух солдата.
- Середовище: Mist (сліпить солдатів, але не прибульців), слиз Goo, вогонь — клітини з тривалістю 3 ходи.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Солдат | piece | HP (від Strength), Will Points (від Willpower), Speed, Perception, Stealth, Accuracy, AP, клас | рух/постріл/навички за AP; навички — ще й за WP |
| Частина тіла (голова, торс, руки, ноги) | object | власні HP і броня | HP=0 → вимкнена: прибрано її стати/зброю/навичку, кровотеча |
| Спорядження на тілі (зброя, щит) | object | HP | HP=0 → знищене |
| Прибулець (Arthron, Triton, Siren, Chiron…) | enemy | зібраний з пулу частин | мутує між місіями; Arthron відповідає вогнем |
| Crab Queen / Scylla | boss | — | огортає туманом, народжує нових прибульців |
| Людські фракції (New Jericho, Synedrion, Disciples of Anu, бандити) | enemy | — | можуть бути союзниками, ворогами |
| Укриття повне / половинне | terrain | щит | знижує ймовірність влучання; руйнується |
| Mist | zone | — | солдат у ньому видимий ворогові і −1 WP на початку ходу; прибульці +1 WP |
| Goo (слиз) | hazard | 3 ходи | не дає рухатись; гасить вогонь |
| Вогонь | hazard | до 6 шкоди, 3 ходи | блокує рух (крім тих, хто у шаленстві); шкода при вході і на початку ходу |
| Ящик | pickup | — | відкриття дає лут і WP |
| Стратегічна ціль (сяйво) | zone | — | досягнення дає WP |
| Транспорт, дрони | ally | — | у загоні замість солдата (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
Спільне з XCOM (укриття, туман, переповнення ходу, overwatch як ідея) — у [xcom](xcom.md). Відмінні правила:
- КОЛИ `turn_start(player)` → ТО `custom: «AP солдатів = максимум (мінус штрафи Tired −1, Exhausted −2, Dazed → 1)»`.
- КОЛИ `input(action)` → ЯКЩО `custom: «AP ≥ частка дії: ¼ — пістолет, перезарядка, інвентар; ½ — гвинтівка, граната, ракета; ¾ — снайперка, кулемет»` → ТО дія, `counter(AP, −частка)`.
- КОЛИ `input(move, path)` → ТО `move`; КОЛИ `line_of_sight(soldier, hidden_enemy)` під час руху → ТО `custom: «рух зупиняється, решта AP лишається»`, `reveal(enemy)`.
- КОЛИ `input(aim, point)` → ТО `custom: «показати два кола: синє — межа розкиду (розподіл дзвоном), червоне — куди ляже половина куль»`.
- КОЛИ `input(fire)` → ТО `custom: «кожна куля — окремий промінь з випадковим відхиленням у конусі»`; КОЛИ куля `contact(bullet, x)` → ТО шкода тому, у що влучила (ворог, союзник, укриття, обʼєкт).
- КОЛИ `contact(bullet, body_part)` → ТО `damage(шкода − броня частини)`; залишок знімає HP частини **і** загальні HP.
- КОЛИ `hp_zero(body_part)` → ТО `custom: «частину вимкнено: прибрати її стати, навички, зброю»`, `set_state(unit, bleeding)`.
- КОЛИ `hp_zero(equipment)` → ТО `disappear_b` (зброю/щит знищено).
- КОЛИ `custom: «влучання зброєю з shred»` → ТО `custom: «броня частини зменшується назавжди»`.
- КОЛИ `explode(area)` → ТО `custom: «шкода кожній частині тіла, відкритій до центру вибуху; загальні HP — один раз за найслабшою бронею»`, шкода і своїм.
- КОЛИ `explode(area)` → ЯКЩО `custom: «у зоні — укриття/стіна»` → ТО `set_cell(cell, rubble)` (руйнування, новий прохід).
- КОЛИ `input(overwatch, cone)` → ЯКЩО `has(soldier, AP)` → ТО `set_state(soldier, overwatch)`; КОЛИ `enter(enemy, cone)` → ТО постріл по першому, хто увійшов; конус можна звузити/розширити.
- КОЛИ `custom: «по юніту з Return Fire вистрелили в межах ~½ його Perception»` → ТО `custom: «відповідний постріл»`.
- КОЛИ `custom: «вимкнено частину тіла / загинув товариш / ефект Terror Sentinel»` → ТО `counter(WP, −n)`.
- КОЛИ `custom: «досягнуто стратегічної цілі / відкрито ящик»` → ТО `counter(WP, +n)`; `input(recover)` → `counter(WP, +½ max)`.
- КОЛИ `counter(WP, <, 0)` → ТО `set_state(soldier, panic)` — `custom: «тікає в безпечне місце, пропускає хід, частково відновлює WP»`.
- КОЛИ `turn_start(side)` → ЯКЩО `state(unit, bleeding)` → ТО `damage(bleed)`; ЯКЩО `state(unit, poison)` → ТО `damage(poison)`, `counter(poison, −10)`; ЯКЩО `state(unit, virus)` → ТО `counter(WP, −virus)`.
- КОЛИ `enter(unit, fire)` або `turn_start(side)` у вогні → ТО `damage(≤6)`; `enter(unit, goo)` → `freeze(unit, n)`.
- КОЛИ `custom: «між місіями: ворожий тип часто програє»` → ТО `custom: «AI відкидає невдалі мутації, успішні частіше зʼявляються»`.
- КОЛИ `all_gone(enemy)` або `custom: «виконано ціль місії»` → ТО `win`; КОЛИ `all_gone(soldiers)` → ТО `lose`.
- Перемога: ціль місії · Поразка: загін знищено / провал цілі · Рахунок: —.

## Керування і ввід
- Миша: клік солдата → кольорові зони руху (синя/жовта) → клік клітини; вибір зброї → режим пострілу.
- **Вільне прицілювання** — перемикання у вигляд від першої особи: курсор на частину тіла або спорядження → інфо-бокс (назва, HP- і броня-піпси, «вимкнено»); колесо миші показує кола розкиду.
- Overwatch: розмір конуса — Ctrl + колесо.
- Кінець ходу — кнопка; AP-панель з четвертинами.

## Вікна, меню, HUD
- `main-menu` → нова гра: `difficulty-select`, `custom-window` налаштувань кампанії.
- `game-screen` (бій): 3D-мапа, `reachable-highlight` синім/жовтим, AP-панель з четвертинами, Will Points, `hp-bar` з піпсами броні, іконки укриття, `fog-overlay`.
- `custom-window` «Free aim» — вигляд від першої особи з колами розкиду і інфо-боксом частини тіла.
- `custom-window` «Geoscape» — глобус: туман поширюється, сховища фракцій, місії, переліт літаків (`map-window`).
- `custom-window` бази: дослідження, виробництво, лікування; `inventory-window` (спорядження й вага за Strength), `upgrade-window` (навички класу, подвійний клас) (?).
- `custom-window` «Diplomacy» — стосунки з фракціями.
- `end-screen` місії — підсумок втрат і луту.

## Фічі поза полем
- Геоскейп: туман поширюється по глобусу; бази, сховища, рейди, дипломатія; союз з однією фракцією веде до своєї кінцівки — технології інших недоступні.
- Ворожа еволюція: склад прибульців залежить від того, що гравець вбиває.
- `autosave` / Ironman (?); `difficulty-presets`.
- DLC: Blood and Titanium, Legacy of the Ancients, Corrupted Horizons, Festering Skies, Kaos Engines, Living Weapons.

## Варіації й родичі
- Батько: [xcom](xcom.md) і оригінальний X-COM (1994) того ж автора (Julian Gollop); брат [jagged-alliance-2](jagged-alliance-2.md) (AP і прицілювання по частинах тіла), [silent-storm](silent-storm.md) (руйнування й балістика), Fallout V.A.T.S. (вибір частини тіла).
- **Осі варіацій**: влучання — відсоток з кубиком (XCOM) / фізичний розкид куль (Phoenix Point) · ціль — юніт цілком / частини тіла з власними HP · дії — 2 дії / AP-бюджет з частками · мораль — нема / воля як ресурс навичок · вороги — фіксований ростер / еволюціонує під гравця.

## Цікавинки для курсу
- Постріл як N променів з випадковим відхиленням у конусі (розподіл дзвоном) і влучання в перший обʼєкт на шляху — 🥈 (геометрія, raycast).
- Ворог з частин тіла: окремі HP/броня, вимкнення частини забирає здібність — 📎 (композиція сутностей).
- Броня на частину + shred + вибух «за найслабшою бронею» — 📎.
- AP з частками дій + синя/жовта зони досяжності (BFS з бюджетом) — 📎.
- Will Points як ресурс навичок і тригер паніки — 🌱.
- Еволюція ворожого складу: успішні варіанти множаться — 🥇 (генетичний відбір на рівні кампанії).
- Клітини-стихії з тривалістю 3 ходи (вогонь, слиз) і їхня взаємодія — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `projectile-shot` (куля як промінь) · `shoot-burst` (черга — кожна куля окремо) · `line-of-sight-attack` · `explode-area` · `destructible-blocks` · `status-effects` (кровотеча, отрута, параліч, вірус, паніка) · `fog-of-war` · `reachable-highlight` · `inventory-items` + `inventory-limit` (вага за Strength) · `unit-xp-skills` · `ai-opponent` · `world-map` (геоскейп) · `difficulty-levels` · `save-autosave` · `player-camera`.
- **Нема** → пропозиції карток:
  - `+free-aim-spread` «Вільне прицілювання з конусом розкиду» · entities/combat · 🥈.
  - `+body-part-targeting` / `+limb-disable` «Ціль — частина тіла; вимкнення забирає здібність» · entities/combat · 📎.
  - `+armor-per-part` / `+armor-shred` «Броня по частинах і її зношування» · entities/state · 📎.
  - `+stray-bullet-hits` «Промах влучає в те, що на шляху» · entities/combat · 🥉.
  - `+will-points-panic` «Воля як ресурс і поріг паніки» · entities/state · 🌱.
  - `+return-fire` «Відповідний вогонь на постріл» · entities/combat · 🌱.
  - `+spot-interrupt` «Виявлення ворога зупиняє рух» · entities/move · 🌱.
  - `+enemy-evolution` «Ворожий склад адаптується до гравця» · game-logic/opponent · 🥇.
  - `+hazard-tiles` «Клітини-стихії з тривалістю» · entities/state · 🌱.
  - `+action-points` / `+cover-system` / `+overwatch` — спільні з XCOM.

## Пропозиції до словників
- `+trigger:sighted` — ворога виявлено (уже просить XCOM); `+trigger:attacked` — по юніту стріляли (Return Fire); `+trigger:enemy_moved` — рух у зоні overwatch.
- `+cond:ap` — вистачає очок дії (частка); `+cond:part_disabled` — частина тіла вимкнена.
- `+effect:disable_part` — вимкнути частину тіла з її здібностями; `+effect:shred` — назавжди зменшити броню; `+effect:interrupt_move` — обірвати рух; `+effect:panic` — перехід у паніку з вимушеною дією; `+effect:mutate` — замінити частину тіла ворожого типу.
- `+role:body-part` — підсутність юніта з власними HP/бронею.
- `+ui:spread-circles` — два кола розкиду; `+ui:part-info-box` — HP/броня обраної частини; `+ui:ap-bar-quarters` — AP четвертинами; `+ui:will-points`; `+ui:overwatch-cone` — регульований конус.
- `+window:first-person-aim` — вигляд прицілювання; `+window:geoscape` — глобальна стратегія; `+window:mutation-lab` — дослідження/мутації (?).

## Джерела
- ⭐ [Wikipedia: Phoenix Point](https://en.wikipedia.org/wiki/Phoenix_Point) — дві дії, зупинка при виявленні, overwatch і return fire, частини тіла, балістика промахів, руйнування, Will, мутації й еволюція, геоскейп, фракції, дати.
- [Fextralife: Combat](https://phoenixpoint.wiki.fextralife.com/Combat) — частки AP, зони руху, кола розкиду, броня по кулях, вимкнення частин, вибухи, Will, overwatch, туман, слиз, вогонь.
- [Fextralife: Stats](https://phoenixpoint.wiki.fextralife.com/Stats) — Strength/Willpower/Speed/Perception/Stealth/Accuracy, статуси (кровотеча, отрута −10, параліч, вірус, паніка), модифікатори AP.
- [Steam](https://store.steampowered.com/app/839770/Phoenix_Point/) — вільне прицілювання, адаптивний ворог, фракції, перелік DLC.
- YouTube: пошук «Phoenix Point gameplay free aim».

## Непевне
- (?) Базовий запас AP (4 у релізі?) — у джерелах лише частки й модифікатори.
- (?) Конус overwatch, що регулюється Ctrl+колесом, і поріг Return Fire «½ Perception» — з фанатських сторінок, бачених у пошуку.
- (?) Розмір загону (вікі: 4–16) — дані до релізу; у релізі менше (?).
- (?) Імена прибульців (Triton, Siren, Chiron, Scylla), класи солдатів і подвійний клас — з памʼяті.
- (?) Wiki Fextralife редагувалась у грудні 2019 — цифри (вогонь до 6, тривалість 3 ходи) могли змінитись патчами.
- (?) Fandom-вікі гри віддає 402 — у шапку не покладено.
