---
title: Fort Triumph
slug: fort-triumph
aka: []
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: state
year: 2020
platforms: [Windows, macOS, Linux, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/612570", best: true, note: "офіційний опис: дерева й валуни як зброя, 4 фракції × 4 класи, процедурні тайлові карти, permadeath; реліз 16.04.2020"}
  - {kind: other, url: "https://gideonsgaming.com/fort-triumph-review-physically-fine", note: "найдокладніша рецензія: 3 ОД, атака 2 ОД, оглушення −2 ОД, копняк урни, гак, вихор, атаки з нагоди, валюти"}
  - {kind: other, url: "https://www.geekyhobbies.com/fort-triumph-indie-video-game-review/", note: "ланцюгова реакція від одного копняка, укриття, вибір 1 з 3 навичок, захоплення міста, permadeath"}
  - {kind: other, url: "https://turnbasedlovers.com/review/fort-triumph-tbl/", note: "кулдауни, overwatch однією кнопкою, автоперемога, 9 будівель форту, герої кожні 7 днів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Fort+Triumph+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, push-object, pull-object, destructible-blocks, chain-reaction, melee-vs-ranged, unit-xp-skills, inventory-items, inventory-limit, round-currency, ai-opponent, difficulty-levels, map-window, game-screen, main-menu, end-screen, settings-window, mode-select, +action-points, +knockback, +collision-damage, +collision-stun-ap-drain, +felling-tree, +collapse-structure, +cover-system, +overwatch, +attack-of-opportunity, +skill-cooldown, +level-up-choice, +unit-permadeath, +auto-resolve-battle, +procedural-battle-maps, +base-building, +hero-recruit-timer, +multi-currency, +enemy-party-spawner, +battle-grade-reward]
proposes: ["+effect:knockback", "+effect:spend_ap", "+trigger:enemy_moved", "+cond:cooldown_ready", "+role:hero", "+role:base", "+ui:action-pips", "+ui:skill-cooldown-icons", "+window:town-hub", "+window:perk-select", "+feature:permadeath", "+card:collision-stun-ap-drain", "+card:felling-tree"]
author: opus
date: 2026-11-09
---

# Fort Triumph — фентезійна тактика, де головна зброя — копняк: ворог летить у дерево, дерево падає на іншого

## Суть
Загін героїв (паладин, варвар, рейнджер, маг) бʼється покроково на процедурних тайлових картах у дусі XCOM, але ядро — фізика оточення: копнути ворога в камінь, звалити дерево на групу, вибити колону з-під арки. Удар об обʼєкт або іншого юніта оглушує, а оглушення знімає 2 з 3 очок дії — тобто ворог не встигне атакувати наступного ходу. Рецензенти пишуть, що рівень можна зачистити, жодного разу не вдаривши напряму. Над боями — стратегічний шар у дусі Heroes: мапа світу, загони героїв, форт із будівлями, три валюти.

## Поле і час
- Бойове поле — тайлова карта (2.5D), що генерується процедурно для кожної місії; на ній дерева, валуни, колони й арки, урни, укриття (Steam: «tiled procedural maps», рецензія TBL: «tiled 2.5D battlescape»).
- Хід — по черзі сторін: гравець витрачає ОД усіх своїх героїв, потім ходить ШІ. Фази розстановки нема — герої стоять автоматично (TBL).
- Стратегічний шар: процедурна мапа світу 2.5D; загони ходять по ній у межах денного запасу руху; дні рахуються (нові герої у форті кожні 7 днів).
- Зберігатися посеред бою не можна (TBL).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой гравця | player | клас; 3 ОД; HP; навички з cooldown; інвентар; рівень | рух і навички за ОД; більшість атак коштують 2 ОД |
| Паладин | player | ближній бій | має копняк (усі ближні класи) |
| Варвар | player | ближній бій | копняк сусіднього обʼєкта або ворога: відкидання по лінії |
| Рейнджер | player | дальній бій | overwatch; гак підтягує ціль до себе |
| Маг | player | дальній бій | вихор відкидає ціль на відстані |
| Ворожий юніт | enemy | ті самі 4 класи; фракція | ходить і бʼє за ШІ; гобліни краще користуються укриттям |
| Дерево | object | — | від удару падає в напрямку удару: шкода й оглушення тим, хто під ним; відкриває лінію огляду |
| Валун | object | — | зсувається поштовхом; в нього вбивають ворогів копняком |
| Колона під аркою | static | руйнується | знищена — арка обвалюється на тих, хто під нею |
| Вогняна урна | object | — | варвар копає її у ворогів |
| Укриття | terrain | — | юніт за ним захищений; зайти в укриття коштує ОД |
| Ворожий загін | enemy | на мапі світу | фракції ШІ безперервно породжують нові загони |
| Лігво, виробництво, святилище, скарб | neutral | на мапі світу | бій або нагорода: ресурси чи предмети |
| Форт / місто | base | до 9 будівель | будівлі дають дохід чи захист; наймання героїв |
| Захисники форту | ally | жерці, чемпіони, баліста | під керуванням гравця, коли форт атаковано |
| Буряки · магія · слава | resource | 3 валюти | плата за будівлі й дисципліни гільдії |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `counter(ap, =3)` кожному герою (базово; оглушений — менше).
- КОЛИ `input(move, hero, cell)` → ЯКЩО `counter(ap, >=, 1)` і `path_exists(hero, cell)` → ТО `move(hero, cell)`, `counter(ap, -1)`.
- КОЛИ `input(skill, hero, target)` → ЯКЩО `counter(ap, >=, cost)` і `custom: «навичка не на cooldown»` → ТО ефект навички, `counter(ap, -cost)` (здебільшого 2, бувають 1 і 0), `set_state(skill, cooldown, n)`.
- КОЛИ `input(kick, hero, target)` → ЯКЩО `in_range(hero, target, 1)` і `custom: «ближній клас»` → ТО `custom: «knockback: ціль летить по лінії удару до перешкоди»`.
- КОЛИ `contact(knocked, object|unit)` → ТО `damage(knocked, n)`, `damage(b, n)`, `set_state(knocked, stunned)`, `set_state(b, stunned)`.
- КОЛИ `after(push)` → ЯКЩО `custom: «збитий юніт сам летить далі в наступного»` → ТО `push(b)` — ланцюг: один копняк зачіпає кілька юнітів.
- КОЛИ `turn_start(side)` → ЯКЩО `state(unit, stunned)` → ТО `counter(ap, -2)`, `clear_state(unit, stunned)` — з 1 ОД атака (2 ОД) неможлива.
- КОЛИ `input(kick, hero, tree)` → ТО `custom: «дерево падає в напрямку удару»`, `damage(units_in_line, n)`, `set_state(units_in_line, stunned)`, `set_cell(line, open)` (огляд відкрито).
- КОЛИ `destroyed(pillar)` → ТО `custom: «арка обвалюється»`, `damage(units_under_arch, n)`.
- КОЛИ `input(kick, barbarian, fire_urn)` → ТО `throw(fire_urn, dir)`, `damage(target, n)`.
- КОЛИ `input(whirlwind, mage, target)` → ЯКЩО `in_range(mage, target, n)` → ТО `custom: «knockback на відстані»`.
- КОЛИ `input(hook, ranger, target)` → ЯКЩО `line_of_sight(ranger, target)` → ТО `pull(target)`.
- КОЛИ `input(lift, unit, object)` → ЯКЩО `in_range(unit, object, n)` → ТО `carry(unit, object)` → `move(object, cell)` (?).
- КОЛИ `custom: «ворог рушив у полі зору»` → ЯКЩО `state(ranger, overwatch)` → ТО `damage(enemy, n)`, `clear_state(ranger, overwatch)`.
- КОЛИ `adjacent(enemy, melee_hero)` → ЯКЩО `custom: «ворог підійшов своїм рухом»` → ТО `damage(enemy, n)` (атака з нагоди).
- КОЛИ `input(attack, a, b)` → ЯКЩО `custom: «b за укриттям від a»` → ТО `custom: «шкода/влучання зменшені»` (?).
- КОЛИ `hp_zero(hero)` → ЯКЩО `mode(permadeath)` → ТО `disappear(hero)`, `custom: «досвід утрачено назавжди»`; інакше (скірміш) `custom: «воскресити за ресурси»`.
- КОЛИ `counter(xp, >=, n)` → ТО `choose(1 з 3 напіввипадкових навичок: класових і крос-класових)`.
- КОЛИ `all_gone(enemy)` → ТО `win` (бій), `custom: «оцінка бою»` → `currency(+n)` для дисциплін гільдії.
- КОЛИ `contact(party, enemy_party)` на мапі світу → ТО `window(battle)`; ЯКЩО `custom: «ворог значно слабший»` → ТО `custom: «автоперемога без бою»`.
- КОЛИ `timer(7_days)` → ТО `spawn_at(hero_for_hire, fort)`.
- КОЛИ `input(build, structure)` → ЯКЩО `counter(resources, >=, cost)` і `count(structure, <, 9)` → ТО `place(fort, structure)`, `currency(-cost)`.
- КОЛИ `timer(day)` → ТО `custom: «ШІ-фракції породжують нові ворожі загони»`.
- КОЛИ `custom: «ворожий загін атакує форт»` → ТО `window(battle)` з захисниками: жерці, чемпіони, баліста.
- Перемога: бій — знищити ворогів або виконати ціль місії; скірміш — захопити місто суперника · Поразка: загинув увесь загін; у скірміші — втрата міста (?) · Рахунок: оцінка бою → ресурси.

## Керування і ввід
- Миша або геймпад (Steam: Full controller support): клік по герою → клік по клітині (рух) або вибір навички → ціль.
- Окрема кнопка «overwatch для всіх» — призначає чатування всім героям одним натиском (TBL).
- На мапі світу: клік по загону → клік по точці; рух обмежений денним запасом.
- Кооператив на одному екрані й локальний мультиплеєр (категорії Steam: Shared/Split Screen Co-op, Local Multiplayer).

## Вікна, меню, HUD
- `main-menu` → `mode-select`: кампанія (3 глави, лише людська фракція) · скірміш (4 фракції, одиночний і мультиплеєр); налаштування гри: permadeath вкл/викл, 4 рівні складності.
- `map-window` — мапа світу: загони, лігва, святилища, скарби, ворожі загони, форт.
- `+window:town-hub` — форт/місто: будівлі (до 9), наймання героїв, глобальний інвентар.
- `inventory-window` — предмети з глобального інвентаря в особистий (мало слотів); зілля, спорядження.
- `+window:perk-select` — підвищення рівня: вибір 1 з 3 навичок.
- `game-screen` (бій): тайлове поле; `action-points` героя; `hp-bar`; `skill-bar` з іконками cooldown; `end-turn-button`; кнопка «overwatch усім»; `tooltip` (?).
- `end-screen` бою: оцінка й нагорода ресурсами.
- Переходи: main-menu → map-window → (контакт загонів) → game-screen → end-screen → map-window; map-window → town-hub.

## Фічі поза полем
- `permadeath` героїв — перемикач на старті (у кампанії, за GeekyHobbies, обовʼязковий); у скірміші загиблих можна відродити за ресурси.
- `difficulty-presets` (4); `achievements`; `cloud-save`; `gamepad-support`; `mode-coop` локальний.
- Прогресія: досвід героїв → навички; дисципліни гільдії за славу; будівлі форту; предмети з даними навичками.
- Автоперемога над набагато слабшим загоном — бій можна пропустити.

## Варіації й родичі
- Фізика як зброя: [Into the Breach](into-the-breach.md) (поштовх, шкода від зіткнення, детермінізм), [Auro](auro.md) (лише поштовхи на гексах), [Tactical Breach Wizards](tactical-breach-wizards.md) (вікна й відкидання), [Fights in Tight Spaces](fights-in-tight-spaces.md).
- Каркас XCOM: [XCOM](xcom.md) — 2 дії, укриття, overwatch; тут 3 ОД і атака 2 ОД.
- Стратегічний шар: [Heroes of Might and Magic III](heroes-of-might-and-magic-3.md) (загони героїв на мапі, місто, тижневий приплив найму).
- **Осі варіацій**: що робить удар об перешкоду — шкода (ItB) / шкода + оглушення = −ОД (Fort Triumph) / нічого · хто відкидає — лише навички (ItB) / базова дія «копняк» усім ближнім класам · обʼєкти поля — пасивні перешкоди / активні снаряди (дерево падає, урна летить, арка обвалюється).

## Цікавинки для курсу
- Копняк із ланцюговим відкиданням: юніт летить по лінії, влучає в іншого, той летить далі — 🥈 (рекурсія руху, порядок обробки, шкода обом).
- Оглушення = −2 ОД при атаці за 2 ОД: одне число робить «пропустити атаку» без окремого стану — 📎.
- Дерево падає лінією й відкриває огляд: обʼєкт поля стає снарядом і змінює видимість — 🥉.
- Арка на колонах: знищення опори валить залежну частину — 🥉 (граф опор).
- Overwatch однією кнопкою для всіх + атаки з нагоди: реакції поза своїм ходом — 🥉.
- Стратегічний шар «загони на мапі + форт + приплив героїв кожні 7 днів» — 🥈.

## Мапа на каталог
- Є: `hp-damage` · `push-object` (копняк, вихор) · `pull-object` (гак) · `destructible-blocks` (дерева, колони) · `chain-reaction` (ланцюг від копняка) · `melee-vs-ranged` · `unit-xp-skills` · `inventory-items` + `inventory-limit` · `round-currency` · `ai-opponent` · `difficulty-levels` · `map-window` · вікна.
- **Нема** → пропозиції карток:
  - `+knockback` «Відкидання до перешкоди» · entities/combat · 🥉 · слот {distance: 1|to_obstacle}.
  - `+collision-stun-ap-drain` «Зіткнення оглушує: −ОД наступного ходу» · entities/combat · 📎 · слот {ap_loss}.
  - `+felling-tree` «Повалене дерево — лінійна атака» · entities/interact · 🥉.
  - `+collapse-structure` «Обвал без опори» · entities/interact · 🥉.
  - `+attack-of-opportunity` «Атака з нагоди при підході» · entities/combat · 📎.
  - `+auto-resolve-battle` «Автоперемога над слабшим» · game-logic/opponent · 🌱.
  - `+hero-recruit-timer` «Нові герої для найму кожні N днів» · game-logic/economy · 🌱.
  - `+battle-grade-reward` «Оцінка бою → ресурси» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:knockback` — ціль відлітає по лінії удару до перешкоди (копняк, вихор); відрізняється від `push` тим, що ініціатор не рухається, а відстань — до упору.
- `+effect:spend_ap` — списати очки дії за дію (рух, навичка).
- `+trigger:enemy_moved` — ворог зробив крок у полі зору (overwatch).
- `+cond:cooldown_ready` — навичка не на перезарядці.
- `+role:hero` — іменований юніт з класом, рівнем і інвентарем, що переходить між боями.
- `+role:base` — форт/місто гравця з будівлями (захоплення = поразка в скірміші).
- `+ui:action-pips` — точки ОД над героєм; `+ui:skill-cooldown-icons` — іконки навичок з лічильником ходів до готовності.
- `+window:town-hub` — екран форту: будівлі, наймання, склад; `+window:perk-select` — вибір 1 з 3 навичок на підвищенні.
- `+feature:permadeath` — загибель героя остаточна (перемикач на старті).
- `+card:collision-stun-ap-drain`, `+card:felling-tree` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Fort Triumph](https://store.steampowered.com/app/612570) — офіційний опис, фракції й класи, дата релізу, категорії (кооператив, контролер).
- [Gideon's Gaming: рецензія](https://gideonsgaming.com/fort-triumph-review-physically-fine) — 3 ОД, атака 2 ОД, оглушення −2 ОД, урна, гак, вихор, атаки з нагоди, валюти, захисники форту.
- [Geeky Hobbies: рецензія](https://www.geekyhobbies.com/fort-triumph-indie-video-game-review/) — ланцюгова реакція, укриття, вибір 1 з 3, захоплення міста, permadeath, 3 глави.
- [Turn Based Lovers: рецензія](https://turnbasedlovers.com/review/fort-triumph-tbl/) — кулдауни, overwatch однією кнопкою, автоперемога, 9 будівель, найм кожні 7 днів, без фази розстановки.
- YouTube: пошук «Fort Triumph gameplay».

## Непевне
- (?) Рік: у черзі 2019; Steam дає повний реліз 16.04.2020; дата раннього доступу не перевірена.
- (?) Сітка квадратна — висновок з «tiled» карт і порівняння з XCOM, прямого підтвердження нема.
- (?) Чи є туман війни в бою і випадковий шанс влучання — джерела мовчать.
- (?) «Lift» будь-яким юнітом — лише в одній рецензії (Gideon's Gaming); можливо, це навичка мага.
- (?) Як саме укриття зменшує шкоду (половинне/повне?) — не описано.
- (?) Чи котиться валун після поштовху — джерела кажуть лише «можна штовхати».
- (?) Консолі: Switch — за списком Wikipedia (TouchArcade, 2021); Xbox згадано лише рецензією xboxtavern.
