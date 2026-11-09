---
title: Dungeon Hack
slug: dungeon-hack
aka: ["AD&D Dungeon Hack", "Forgotten Realms: Dungeon Hack"]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 1993
platforms: [MS-DOS, PC-98]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dungeon_Hack", best: true, note: "один герой у рушії Eye of the Beholder, випадкове підземелля, seed для обміну, налаштування складності, сейви стираються після смерті"}
  - {kind: other, url: "https://crpgaddict.blogspot.com/2024/04/game-510-dungeon-hack-1993.html", note: "CRPG Addict: створення героя, вікно опцій підземелля, seed, рівні 28×27, ключі, торгові автомати, ідентифікація"}
  - {kind: other, url: "https://crpgaddict.blogspot.com/2024/05/dungeon-hack-summary-and-rating.html", note: "CRPG Addict: підсумок — особливі зони, рівні-брамники, бос-лич, книги-пастки, автомапа"}
  - {kind: other, url: "https://www.roguebasin.com/index.php/Dungeon_Hack", note: "RogueBasin: випадкові підземелля, real-time, клавіатура + миша"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dungeon+Hack+1993+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, orientation-state, impassable-cells, key-and-door, button-toggle, teleport, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, item-identification, hunger-clock, status-effects, unit-xp-skills, melee-vs-ranged, projectile-shot, chase-player, respawn, stairs-levels, dungeon-generation, seed-share, difficulty-levels, permadeath, save-game, score-records, map-window, gui-render, player-camera, drag-drop-piece, +first-person-grid, +birth-options, +rule-system-import, +spell-memorize-rest, +illusory-wall, +spinner-tile, +dark-zone, +class-race-matrix, +level-drain, +healing-vending-machine, +key-before-lock, +multi-level-puzzle, +gatekeeper-level, +slow-zone, +water-level, +curse-item, +auto-map-notes]
proposes: ["+trigger:rest(party)", "+cond:race_size(a, small)", "+effect:memorize(a, spell)", "+effect:identify", "+effect:level_drain(a)", "+effect:erase_saves", "+window:dungeon-options", "+window:automap", "+window:spell-book", "+window:character-create", "+feature:dungeon-options", "+feature:seed-input", "+card:healing-vending-machine", "+card:multi-level-puzzle"]
author: opus
date: 2026-11-09
---

# Dungeon Hack — Eye of the Beholder для одного героя: підземелля з seed-а, налаштоване тобою, і справжня смерть

## Суть
Один персонаж за правилами AD&D 2-ї редакції спускається у **випадково згенероване** клітинне підземелля від першої особи (рушій Eye of the Beholder), щоб убити фінального боса й забрати магічну сферу. Перед стартом гравець збирає підземелля сам: глибина (від 10 рівнів), кількість і сила монстрів, отрута, нежить, їжа, рівень води, ілюзорні стіни, головоломки на кілька рівнів, «справжня смерть». Seed підземелля можна ввести вручну й передати іншим. Увімкнена справжня смерть — і при загибелі гра **стирає всі сейви**.

## Поле і час
- Рівень — сітка 28×27 клітин (CRPG Addict), однакового розміру, звивисті коридори; кількість рівнів — з налаштувань (мінімум 10; на «moderate» — 18).
- Вид від першої особи, крок на клітину з орієнтацією, як у EoB; автомапа показує відкрите, монстрів і предмети.
- Real-time: монстри рухаються й бʼють, поки гравець думає; відпочинок — пропуск часу.
- Особливі рівні/зони: темні (навпомацки за автомапою), «повільні», «голодні», водний рівень (бульбашки), рівні-брамники (5-й і 10-й у забігу автора).
- Генерація займає кілька хвилин; seed + опції однозначно задають підземелля.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | раса, клас (мульти-клас лише для нелюдей), 6 атрибутів, світогляд, HP, рівень, їжа/вода, 2 руки | рух клітинами; атака предметом у руці; кастер — заучені заклинання |
| Стіна | static | текстура випадкова | непрохідна |
| Ілюзорна стіна | static | вмикається опцією | виглядає стіною, проходиться |
| Таємні двері | gate | можна вимкнути опцією | знайти й відчинити |
| Двері | gate | кнопка / ланцюг / перемикач / важіль / ключ | відчиняються механізмом або ключем |
| «Ключ» | pickup | ключ, молот, монета, самоцвіт | молот — по гонгу, монета — у щілину, самоцвіт — у мурал; завжди зʼявляється раніше за свій замок |
| Статуя-стіна | static | — | блокує прохід |
| Лаз | gate | — | пройти можуть лише малі раси |
| Телепорт · спінер | terrain | — | переносить / розвертає героя |
| Пастка в підлозі / люк | hazard | — | шкода або падіння (?) |
| Сходи | static | вгору / вниз | перехід між рівнями |
| Темна зона | terrain | — | вид темний, орієнтація за автомапою |
| Повільна зона · голодна зона | terrain | — | сповільнює рух · прискорює голод |
| Водний рівень | terrain | — | штраф без Water Breathing; книга заклинань і їжа не страждають |
| Лікувальний автомат | static | 1 монета | повне здоровʼя, лікує отруту |
| Ігровий автомат | static | монета | випадковий виграш (?) |
| Ніша зі скарбом | container | — | предмет у стіні |
| Раціон | pickup | — | відновлює їжу |
| Зілля · амулет · жезл · кільце | pickup | вигляд (колір/матеріал) випадковий за гру | невідомі до ідентифікації; впізнав одне — впізнав усі такі самі |
| Сувій · книга | pickup | — | сувої підписані; книги можуть бути пасткою (втрата рівня, смерть) |
| Пергамент-мапа | pickup | — | мапить рівень |
| Монстр | enemy | ~2 типи на рівень, HP | real-time; респавниться; частина паралізує (ghoul), тримає (carrion crawler), краде зброю (living muck), невидима |
| Нежить | enemy | — | висмоктує рівні досвіду (wight) |
| Бос рівня | boss | — | на кожному рівні; можна оминути, якщо знайти сходи раніше |
| Фінальний бос | boss | сфера | у забігу автора — лич на 18-му рівні; перемога = кінець гри |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(step|strafe)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`; стіна, двері, монстр → `block`.
- КОЛИ `input(turn)` → ТО `face(hero, ±90°)`.
- КОЛИ `contact(hero, illusory_wall)` → ТО `move(hero, dir)` — стіна прохідна.
- КОЛИ `input(click_hand)` → ЯКЩО `not custom: «рука на перезарядці»` → ТО `custom: «атака предметом у руці за правилами AD&D»`, `damage(n)`.
- КОЛИ `input(throw item)` → ТО `custom: «будь-який предмет летить уперед»`, `damage(n)` при влучанні.
- КОЛИ `died(monster)` → ТО `counter(xp, +n)`; КОЛИ `counter(xp, >=, threshold)` → ТО `custom: «рівень класу +1»` (у межах лімітів раси).
- КОЛИ `timer(food_period)` → ТО `counter(food, −1)`; ЯКЩО `cell(here, hunger_zone)` → ТО швидше; КОЛИ `counter(food, ==, 0)` → ТО `damage(n)` (?).
- КОЛИ `enter(hero, slow_zone)` → ТО `speed(hero, −n)`.
- КОЛИ `enter(hero, water_level)` → ЯКЩО `not state(hero, water_breathing)` → ТО `custom: «штраф водного рівня»`.
- КОЛИ `enter(hero, dark_zone)` → ТО `custom: «вид темний»`.
- КОЛИ `enter(hero, teleporter)` → ТО `teleport(hero, cell)`; `enter(hero, spinner)` → ТО `face(hero, random)`.
- КОЛИ `input(use key, lock)` → ЯКЩО `has(hero, matching key)` → ТО `custom: «двері / прохід відчинено»`, `take(hero, key)`.
- КОЛИ `input(button|lever|chain)` → ТО `custom: «перемикає повʼязані двері»`.
- КОЛИ `input(enter hole)` → ЯКЩО `custom: «раса мала (гном, гобіт…)»` → ТО `move(hero, dir)`; інакше `block` (`+cond:race_size`).
- КОЛИ `input(coin, healing machine)` → ЯКЩО `has(hero, coin)` → ТО `take(hero, coin)`, `heal(hero, full)`, `clear_state(hero, poison)`.
- КОЛИ `input(use unknown potion|wand)` → ТО `custom: «ефект»`, `custom: «тип стає відомим для всіх таких предметів»`.
- КОЛИ `input(read unknown book)` → ЯКЩО `custom: «книга-пастка»` → ТО `custom: «мінус рівень»` або `lose`.
- КОЛИ `input(cast Improved Identify)` → ТО `custom: «назва одного предмета»` (`+effect:identify`).
- КОЛИ `input(rest)` → ТО `heal(hero, n)`, `custom: «кастер заучує заклинання»` (`+effect:memorize`, як у EoB), час іде.
- КОЛИ `input(cast)` → ЯКЩО `custom: «заклинання заучене»` and `not custom: «маг в обладунку»` → ТО `custom: «ефект»`, `custom: «заклинання витрачене»`; маг в обладунку — `custom: «каст не вдається без попередження»`.
- КОЛИ `contact(ghoul, hero)` → ТО `stun(hero, n)` — рухатись можна, діяти ні; `contact(wight, hero)` → ТО `custom: «мінус рівень досвіду»`.
- КОЛИ `contact(living_muck, hero)` → ТО `take(hero, weapon)`.
- КОЛИ `timer(respawn)` → ТО `spawn(monster)` на рівні.
- КОЛИ `input(stairs)` → ТО `custom: «наступний / попередній рівень»`.
- КОЛИ `hp_zero(hero)` → ЯКЩО `mode(real death)` → ТО `custom: «усі сейви стерто»`, `game_over`; інакше `lose` → завантаження.
- КОЛИ `died(final_boss)` → ТО `win`, `custom: «сфера в героя — гра завершена»`.
- КОЛИ `game_over` → ТО `window(leaderboard)` — досвід.
- Перемога: вбити фінального боса, здобути сферу. Поразка: смерть героя (з опцією — стирання сейвів). Рахунок: досвід у таблиці рекордів.

## Керування і ввід
- Рух — цифровий блок (крок, крок убік, поворот); взаємодія — миша (руки, інвентар, кнопки на стінах, предмети, автомати), як у EoB.
- Атака — клік по руці портрета; кидок — перетягнути предмет у вид.
- Заклинання — книга заклинань: вибір заученого; відпочинок — кнопка табору (?).
- Автомапа — окремий екран (з’являється ~10 с).

## Вікна, меню, HUD
- `main-menu` — нова гра, завантажити (?).
- `character-create` (як у Wizardry): раса, клас, атрибути (кидки скільки завгодно або вручну), 9 світоглядів, портрет; або ~20 готових героїв.
- `dungeon-options` (`+window:dungeon-options`): глибина, монстри (кількість і сила), отрута, нежить, їжа, рівень води, ілюзорні стіни, ключі й таємні двері, головоломки на кілька рівнів, «Character Death Real», seed; пресети Easy / Moderate / Hard.
- `game-screen`: вид від першої особи, портрет із руками, `hp-bar`, `hunger-bar`, інвентар на головному екрані.
- `automap` (`+window:automap`, `map-window`): відкриті клітини, монстри, предмети.
- `spell-book` (як у EoB) · `inventory-window` · `save-slots` · `leaderboard` · `end-screen`.
- Переходи: меню → створення героя → опції підземелля → генерація → гра → (смерть / бос) → рекорди.

## Фічі поза полем
- `+feature:dungeon-options` — конструктор забігу (`custom-difficulty`, `difficulty-presets`, `+birth-options` як в Angband).
- `+feature:seed-input` / `seed-share` — ручний seed: те саме підземелля в друга.
- `permadeath`-перемикач: смерть стирає всі сейви (`mode-hardcore`).
- `save-slots`, `leaderboard-local` (досвід), автомапа; без музики — лише звуки EoB.
- Нагорода Computer Game Review «Most Replay Value of 1994».

## Варіації й родичі
- Рушій і правила — [eye-of-the-beholder](eye-of-the-beholder.md) (загін 4 → один герой); сусіди — [dungeon-master](dungeon-master.md), [legend-of-grimrock](legend-of-grimrock.md), [captive](captive.md) (теж генерація з seed у real-time блобері).
- Роглайк-спадок: [rogue](rogue.md) (нове підземелля щогри, невідомі зілля), [angband](angband.md) (опції народження), [nethack](nethack.md).
- Осі варіацій: **підземелля** (ручне / генероване / генероване з налаштувань і seed-а) · **смерть** (перезавантаження / стирання сейвів за опцією) · **загін** (4–6 / один) · **ключі** (на рівні / на попередніх рівнях / вимкнено).

## Цікавинки для курсу
- Вікно опцій генератора: глибина, щільність монстрів, їжа, вода, пастки → параметри генерації + пресети — 📎.
- Seed як «код підземелля» для обміну: вхід генератора = seed + опції — 🌱.
- «Ключ завжди раніше замка» (зокрема на попередніх рівнях): генерація головоломки з гарантією розвʼязності — 🥇.
- Ідентифікація за виглядом: вигляд перемішано щогри, впізнав одне — впізнав клас — 🌱.
- Особливі зони рівня (темна, повільна, голодна, водна) як модифікатори правил на ділянці — 📎.
- Лаз лише для малих рас: прохідність клітини залежить від атрибута героя — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `orientation-state` · `impassable-cells` · `key-and-door` · `button-toggle` (кнопки, важелі, ланцюги) · `teleport` · `hp-damage` · `inventory` / `inventory-items` / `inventory-limit` · `item-pickup` · `item-identification` · `hunger-clock` · `status-effects` (параліч, отрута) · `unit-xp-skills` · `melee-vs-ranged` · `projectile-shot` (кидок, луки, жезли) · `chase-player` · `respawn` (монстри) · `stairs-levels` · `dungeon-generation` · `seed-share` · `difficulty-levels` · `permadeath` · `save-game` · `score-records` · `map-window` (автомапа) · `gui-render` · `player-camera` · `drag-drop-piece` (предмети).
- Вже пропоновані: `+first-person-grid` · `+birth-options` (Angband) · `+rule-system-import` · `+spell-memorize-rest` · `+illusory-wall` · `+class-race-matrix` (EoB) · `+spinner-tile` · `+dark-zone` · `+level-drain` · `+curse-item` · `+auto-map-notes`.
- **Нема** → пропозиції карток:
  - `+healing-vending-machine` «Автомат: монета → повне здоровʼя» · game-logic/economy · 🌱.
  - `+key-before-lock` «Генератор кладе ключ раніше за його замок» · levels/generation · 🥇.
  - `+multi-level-puzzle` «Ключ на одному рівні, замок на іншому» · levels/generation · 🥈.
  - `+gatekeeper-level` «Рівень із сильнішим брамником» · levels/progression · 🌱.
  - `+slow-zone` «Ділянка, що сповільнює рух» · entities/interact · 🌱.
  - `+water-level` «Рівень під водою зі штрафом без закляття» · entities/interact · 🌱.

## Пропозиції до словників
- `+trigger:rest(party)` (як у EoB) — відпочинок героя.
- `+cond:race_size(a, small)` — розмір раси для лазів.
- `+effect:memorize(a, spell)` (як у EoB) · `+effect:identify` (як у Rogue) · `+effect:level_drain(a)` (як у Wizardry) · `+effect:erase_saves` — стерти сейви після смерті.
- `+window:dungeon-options` — налаштування генератора забігу · `+window:automap` · `+window:spell-book` (як у EoB) · `+window:character-create` (як у Wizardry).
- `+feature:dungeon-options` — конструктор підземелля · `+feature:seed-input` — ввести seed вручну.
- `+card:healing-vending-machine` · `+card:multi-level-puzzle`.

## Джерела
- ⭐ [Wikipedia: Dungeon Hack](https://en.wikipedia.org/wiki/Dungeon_Hack) — 1993, DOS і PC-98; роглайк + EoB, один герой, AD&D 2e, «понад 4 млрд» підземель, seed для обміну, опції складності (пастки, головоломки, сильні вороги), справжня смерть стирає сейви; таємні двері, невидимі стіни, люки, телепорти, прокляті предмети; мета — сфера й фінальний монстр.
- [CRPG Addict: Game 510: Dungeon Hack](https://crpgaddict.blogspot.com/2024/04/game-510-dungeon-hack-1993.html) — обмеження рас/класів, стартові рівні класів, ~20 готових героїв, опції підземелля (глибина ≥ 10, монстри, отрута, нежить, їжа, вода, ілюзорні стіни, multi-level puzzles, seed, Character Death Real), рівні 28×27, ключі-молоти/монети/самоцвіти, автомати лікування, ідентифікація за кольором.
- [CRPG Addict: Dungeon Hack: Summary and Rating](https://crpgaddict.blogspot.com/2024/05/dungeon-hack-summary-and-rating.html) — 18 рівнів на moderate, темні/повільні/голодні зони, водний рівень, спінери, рівні-брамники, книги-пастки, незвичні вороги (muck, ghoul, carrion crawler), лич-бос, автомапа.
- [RogueBasin: Dungeon Hack](https://www.roguebasin.com/index.php/Dungeon_Hack) — випадкові підземелля, real-time, клавіатура + миша.

## Непевне
- (?) Механіка голоду на нулі (шкода чи смерть) і окрема шкала води — бачив лише «food meter» і «food and water meters».
- (?) Що дають ігрові автомати (автор «лікувався» ними) — не перевірив.
- (?) Пастки в підлозі: шкода чи падіння на рівень нижче.
- (?) Повний список повзунків вікна опцій («близько дюжини») — бачив лише частину.
- (?) Фінальний бос завжди лич чи залежить від глибини — бачив лише забіг автора.
- (?) Кнопка табору / відпочинку й вікно автомапи — за аналогією з EoB.
