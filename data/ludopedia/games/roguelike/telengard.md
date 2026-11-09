---
title: Telengard
slug: telengard
aka: [DND (1976), "Telengard (Avalon Hill)", PC Telengard]
family: roguelike
also: []
klass: avatar
axes:
  field: 3d
  time: realtime
  opponent: ai
  info: hidden
  random: runtime
  goal: score
year: 1982
platforms: [PET, Apple II, TRS-80, Atari 8-bit, VIC-20, C64, CP/M, IBM PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Telengard", best: true, note: "50 рівнів і 2 млн кімнат з координат, real-time без паузи, сейв у корчмі, 6 атрибутів, fight/magic/evade"}
  - {kind: other, url: "https://www.c64-wiki.de/wiki/Telengard", note: "C64-Wiki (DE): 5 с на хід, корчми, вівтарі, трони, фонтани, куби, скриньки, заклинання, клавіші, пороги досвіду"}
  - {kind: other, url: "https://atarihq.com/danb/Telengard.shtml", note: "розбір BASIC-лістингу Atari: формула кімнати, біти стін, коди особливостей"}
  - {kind: other, url: "https://elm-telengard.blogspot.com/2014/03/the-dungeon.html", note: "реімплементація: формула, 200×200×50, старт (25,13,1), виправлення сходів"}
  - {kind: other, url: "https://elm-telengard.blogspot.com/2014/03/line-of-sight-and-movement.html", note: "видимість, ями, ліфти, телепорти за формулою, куби, заклинання Teleport"}
  - {kind: other, url: "https://elm-telengard.blogspot.com/2014/04/encounters.html", note: "фази ходу, 30 % зустрічей, рівень і HP монстра, ельфи/гобіти/дракони"}
  - {kind: other, url: "https://www.roguebasin.com/index.php/Telengard", note: "RogueBasin: 5 с без команди → Stay, один клас, відкрита гра"}
  - {kind: official, url: "http://www.aquest.com/telen.htm", note: "сторінка автора (Daniel Lawrence): історія від DND, двійники PC-версії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Telengard+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, impassable-cells, fog-of-war, stairs-levels, teleport, teleport-one-way, hp-damage, unit-xp-skills, inventory-items, item-pickup, round-currency, thief, status-effects, temporary-modes, player-death, permadeath, save-game, cheat-codes, keyboard-controls, state-as-data, +hash-room-generation, +idle-auto-turn, +encounter-roll, +town-hub, +random-encounter, +altar-sacrifice, +gold-to-xp, +pit-fall-check, +forced-elevator, +level-choice-portal, +random-feature-effect, +level-drain, +exp-doubling-by-level, +charisma-reactions, +save-at-inn, +coordinate-teleport]
proposes: ["+trigger:room_feature(kind)", "+cond:stat_roll(stat, die)", "+effect:stay", "+effect:sacrifice(gold)", "+effect:level_drain(a)", "+effect:return_to_town", "+role:room-feature", "+window:inn-window", "+ui:spell-units", "+feature:save-at-inn", "+axis:time=turn-with-timeout", "+card:hash-room-generation", "+card:idle-auto-turn"]
author: opus
date: 2026-11-09
---

# Telengard — 50 поверхів по 200×200 кімнат, які ніде не зберігаються: кожну обчислює формула з (x, y, z)

## Суть
Один герой без класу (воїн і маг водночас) блукає незмінним підземеллям, бʼється з монстрами, що сильнішають з глибиною, і міняє золото на досвід у корчмах і на вівтарях. Кінця нема: мета — дожити до наступного рівня досвіду. Дві незвичні речі: **підземелля в 2 млн кімнат обчислюється на льоту** хеш-формулою з координат героя (влізло у 8–32 КБ памʼяті), і **гра не чекає** — не дав команду за ~5 секунд, герой автоматично «стоїть», а в бою пропускає удар.

## Поле і час
- Решітка 200×200 кімнат на рівень × 50 рівнів (≈2 млн кімнат, 40 000 на рівень); координати (x, y, z), старт — (25, 13, 1) біля корчми Worthy Meade Inn.
- Кімната = клітина. Формула з трьома константами (1.6915, 1.4278, 1.2462) дає число; молодші біти — північна й західна межі кімнати (порожньо / двері / стіна), старші — особливість кімнати. Південна й східна межі — це північна й західна сусідів. Нічого не зберігається, тому підземелля **однакове в кожній грі** і його можна мапити.
- Вертикаль: сходи, ями, ліфти, телепорти й сірі куби переносять між рівнями, зберігаючи або перераховуючи (x, y) — поле поводиться як тривимірна решітка.
- Видимість: видно найближчі кімнати навколо героя; стіни й двері затуляють чверті огляду; особливості видно лише в своїй кімнаті (Light показує, що вони є поруч).
- Час: хід = команда або тайм-аут ~5 с; хід має фази «зустріч → здобич → особливість кімнати → команда». Паузи нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | STR, INT, WIS, DEX, CON, CHR (кидки), HP, SU (очки заклинань), досвід, рівень, золото | ходить по кімнатах; бій, магія, предмети |
| Межа кімнати | static | порожньо / двері / стіна (2 біти) | стіна блокує рух; двері пропускають, але затуляють огляд |
| Корчма (Inn) | zone | на 1-му рівні; усі сходи вгору з рівня 1 ведуть у корчму | лікування, золото → досвід, збереження |
| Сходи | static | вниз / вгору / в обидва боки | перехід на сусідній рівень у тій самій (x, y) |
| Яма (pit) | hazard | — | перевірка DEX: падіння на рівень нижче з шкодою 3d6 або добровільний спуск |
| Ліфт (elevator) | static | — | неминуче піднімає на рівень вище в ту саму (x, y), без шкоди |
| Телепорт | terrain | — | переносить за формулою від (x, y, z); 20 % шанс ще одного стрибка |
| Сірий туманний куб | static | односторонній | гравець вводить номер рівня; 20 % — випадковий рівень 1–50 |
| Вівтар | static | — | пожертва золота → досвід або добрий ефект заклинання; більше золота — більша нагорода |
| Фонтан | static | — | ковток дає ефект, що змінюється з кожним ковтком |
| Трон | static | — | різні ефекти, добрі й погані |
| Скринька з кнопками (blinking box) | container | — | багато золота, але бʼє струмом |
| Скарб `$` | pickup | золото / зброя / броня / зілля / сувій / кільце | здобич фази «looting» |
| Монстр | enemy | клас 1–20 (кидок 1d20), рівень і HP за формулами від глибини | бій; сильніші глибше |
| Нежить (skeleton, zombie, mummy, ghoul, ghost, spectre, vampire) | enemy | — | привиди/спектри/вампіри висмоктують рівні; ghoul паралізує |
| Ельф | enemy | — | може вилікувати героя замість бою (шанс від CHR) |
| Гобіт | enemy | — | може вкрасти предмет (шанс тим вищий, що нижча CHR) |
| Дракон | enemy | дихає вогнем | може подарувати спорядження (кидок 1d30 ≤ CHR) |
| Меч / броня / щит +X | pickup | бонус | шкода / захист; щит — і від вогню дракона |
| Ельфійський плащ / чоботи +X | pickup | бонус | підкрастися повз монстра / DEX і скритність, перевірка ями |
| Кільця регенерації / захисту +X | pickup | бонус | HP щораунду / менша шкода |
| Свиток порятунку · зілля зцілення · зілля сили велетня | pickup | — | на старт рівня 1 без золота · +HP · тимчасова сила |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(W|A|D|X)` → ЯКЩО `custom: «межа в напрямку руху — не стіна»` → ТО `move(hero, dir)`; інакше `block`.
- КОЛИ `enter(hero, room(x,y,z))` → ТО `custom: «межі й особливість кімнати обчислено формулою з x, y, z»`, `reveal(rooms in sight)`.
- КОЛИ `idle(5 s)` → ТО `custom: «автоматичний Stay»` (`+effect:stay`); поза боєм Stay може дати зустріч або знахідку.
- КОЛИ `phase_start(encounter)` → ЯКЩО `prob(30%)` → ТО `spawn(monster)` класу 1d20, `custom: «рівень = ⌊rnd^1.5 · (2·глибина + 2) + 1⌋»`.
- КОЛИ `spawned(monster)` → ЯКЩО `state(hero, invisible)` and `prob(80%)` → ТО `disappear(monster)`.
- КОЛИ `spawned(monster)` → ЯКЩО `state(hero, fear)` → ТО `custom: «класи 1–4 перекидаються»`.
- КОЛИ `spawned(monster)` → ЯКЩО `custom: «1d20 ≤ бонус ельфійського плаща»` → ТО `choose(підкрастися мимо | бій)` — мимо означає без досвіду й без здобичі.
- КОЛИ `spawned(elf)` → ЯКЩО `prob(4·CHR %)` → ТО `heal(hero, full)`.
- КОЛИ `spawned(hobbit)` → ЯКЩО `prob(100 − 5·CHR %)` → ТО `take(hero, item)`.
- КОЛИ `spawned(dragon)` → ЯКЩО `custom: «1d30 ≤ CHR і подарунок кращий за наявний»` → ТО `give(hero, equipment)`; інакше бій.
- КОЛИ `spawned(monster)` → ЯКЩО `prob(50 + 2·DEX %)` → ТО `custom: «герой бʼє першим»`.
- КОЛИ `input(fight)` → ТО `damage(monster, n)` (STR, меч +X); КОЛИ `turn_end(monster)` → ТО `damage(hero, n)` мінус броня/щит/кільце.
- КОЛИ `input(evade)` → ЯКЩО `prob(by DEX)` → ТО `custom: «втеча з бою»`.
- КОЛИ `idle(5 s)` у бою → ТО `skip_turn(hero)`, монстр атакує.
- КОЛИ `died(monster)` → ТО `counter(xp, +n)`, `custom: «фаза здобичі»`.
- КОЛИ `counter(xp, >=, 2000 · 2^(L−1))` → ТО `custom: «рівень героя +1»`; у v5.2 `custom: «+1 до випадкового атрибута, макс. 18»`.
- КОЛИ `contact(ghost|spectre|vampire, hero)` → ЯКЩО `not state(hero, protection_from_evil)` → ТО `custom: «мінус рівень досвіду»`; ghoul → `stun(hero, n)`.
- КОЛИ `enter(hero, inn)` → ТО `heal(hero, full)`, `custom: «золото → досвід»`; `input(F1)` → `custom: «збереження»` (у v5.2 — лише в корчмі).
- КОЛИ `enter(hero, pit)` → ЯКЩО `not state(hero, levitation)` and `custom: «1d20 > DEX + бонус чобіт»` → ТО `fall(hero)`, `damage(3d6)` на (x, y, z+1); інакше `choose(спуститись | лишитись)`.
- КОЛИ `enter(hero, elevator)` → ТО `move(hero, z−1)` у тій самій (x, y), без шкоди.
- КОЛИ `input(stairs)` → ЯКЩО `cell(here, stairs_up|stairs_down|both)` → ТО `move(hero, z∓1)`.
- КОЛИ `enter(hero, teleporter)` → ТО `teleport(hero, x' = (x + 8z + 13y) mod 200 + 1, y' = (y + 6z + 17x) mod 200 + 1, z ± за бітами x + y)`; ЯКЩО `prob(20%)` → ТО `custom: «ще один стрибок»` (повторно 20 %).
- КОЛИ `input(enter cube)` → ЯКЩО `prob(80%)` → ТО `teleport(hero, level of choice)` — у v5.2 не глибше за рівень героя + 3; інакше `teleport(hero, level 1d50)`.
- КОЛИ `input(pray at altar)` → ТО `currency(−n)`, `custom: «досвід або добрий ефект, пропорційно пожертві»`.
- КОЛИ `input(drink fountain)` → ТО `custom: «випадковий ефект, інший з кожним ковтком»`.
- КОЛИ `input(sit on throne)` → ТО `custom: «випадковий добрий або поганий ефект»`.
- КОЛИ `input(open box)` → ТО `currency(+n)`, `damage(hero, shock)`.
- КОЛИ `input(cast Light)` → ТО `custom: «кімнати з особливостями й пастки поруч позначено картатими клітинами»`.
- КОЛИ `input(cast Sleep|Charm)` → ТО `set_state(monster, asleep|charmed)`; сплячий може прокинутись; Charm не діє на нежить.
- КОЛИ `input(cast Turn Undead)` → ЯКЩО `custom: «монстр — нежить»` → ТО `custom: «нежить тікає»` (WIS).
- КОЛИ `input(cast Time Stop)` → ЯКЩО `not custom: «монстр стійкий (dwarf, giant, spectre, vampire, demon, dragon)»` → ТО `custom: «бій перервано»`.
- КОЛИ `input(cast Astral Walk|Pass Wall)` → ТО `move(hero, dir)` крізь стіну, у межах 1–200.
- КОЛИ `input(cast Teleport, dx, dy, dz)` → ЯКЩО `custom: «√(dx² + dy² + 5dz²) − 0.1 ≤ 5 · рівень героя і ціль у межах»` → ТО `teleport(hero, offset)`; інакше `custom: «закляття не вдалося»`.
- КОЛИ `input(F3 Scroll of Rescue)` → ТО `teleport(hero, start of level 1)`, `currency(−all)`.
- КОЛИ `input(F5|F7)` → ТО `heal(hero, n)` | `set_state(hero, giant_strength, кілька раундів)`.
- КОЛИ `hp_zero(hero)` → ТО `lose`, `custom: «дзвін по разу за кожен рівень досвіду»`, `custom: «персонажа стерто, якщо не чіт-імʼя SV… (v4.18)»`.
- Перемога: нема (гра відкрита). Поразка: смерть = втрата персонажа. Рахунок: рівень досвіду героя.

## Керування і ввід
- Рух: W — північ, A — захід, D — схід, X — південь; S — стояти (Stay). Діагоналей нема (?).
- Бій: атакувати, заклинання, предмет, втеча. Заклинання — за номером/назвою зі списку (?).
- F1 — зберегти, F3 — свиток порятунку, F5 — зілля зцілення, F7 — зілля сили велетня (C64).
- Сірий куб — ввід номера рівня цифрами.
- Таймер ходу ~5 с — головна незвичність вводу: бездіяльність теж є командою.

## Вікна, меню, HUD
- `character-create` (`+window:character-create`, як у Wizardry): кидки шести атрибутів, перекидання скільки завгодно (у v5.2 — ні, але HP ≥ 15), імʼя.
- `game-screen`: тайлова мапа кімнат навколо героя (у ранніх ASCII-версіях `/` — сходи, `$` — скарб), `status-panel` — HP, SU (`+ui:spell-units`), EXP і атрибути; `message-log` — опис кімнати, монстра, результату удару.
- Бій — у тому ж екрані: монстр, рівень, меню дій.
- `inn-window` (`+window:inn-window`): лікування, обмін золота на досвід, збереження (?).
- `end-screen` — смерть із дзвоном.
- Переходи: створення героя / завантаження `.PLR` → корчма → підземелля → (смерть) кінець; підземелля → корчма (сходи з рівня 1).

## Фічі поза полем
- `save-at-inn` (`+feature:save-at-inn`): до v5.2 — F1 будь-де, крім бою; у v5.2 — лише в корчмі.
- `permadeath`: смерть стирає персонажа; у v4.18 імʼя з префіксом «SV» дозволяло оживити (`cheat-codes`).
- `state-as-data`: мапа — функція від координат, а не дані; збереження — лише стан героя.
- Нема фіналу, нема рекордів; немає вибору складності.

## Варіації й родичі
- Попередник — DND (1976–77, DECsystem-10) того ж автора; Telengard переписано під 8 КБ BASIC, підземелля перепроєктовано під більші тайли (C64 і PC мають різну мапу).
- PC Telengard (C, джерело втрачено), ремейк Travis Baldree для Windows; спадкоємці ідеї «особливостей кімнати» — Tunnels of Doom (вівтарі, фонтани, телепорт-куби, трони).
- Родичі в корпусі: [rogue](rogue.md) (покроково, рівні генеруються), [wizardry](wizardry.md) (фіксований лабіринт, телепорт за координатами), [dungeons-of-daggorath](dungeons-of-daggorath.md) (real-time того ж часу), [beneath-apple-manor](beneath-apple-manor.md), [sword-of-fargoal](sword-of-fargoal.md) (жертва золота за досвід).
- Осі варіацій: **мапа** (генерується й зберігається / обчислюється з координат на льоту / ручна) · **хід** (чекає гравця / тайм-аут → авто-дія / real-time) · **сейв** (будь-де / лише в безпечному місці / нема) · **кінець** (бос / нема).

## Цікавинки для курсу
- Хеш-генерація кімнати з (x, y, z): поле, яке не зберігається, але однакове щоразу; сусіди ділять межі — 🥉.
- Тайм-аут ходу: `idle(5 s)` → Stay, а в бою — пропуск удару — 🌱.
- Фази ходу «зустріч → здобич → особливість → команда» з імовірностями й формулами рівня/HP монстра — 📎.
- Вертикальні «особливості» з різною логікою: яма (кидок DEX), ліфт (неминуче вгору), телепорт (формула + ланцюг 20 %), куб (вибір рівня + 20 % випадку) — 📎 за всі.
- CHR як «соціальний» стат: ельф лікує, гобіт краде, дракон дарує — шанс від одного числа — 🌱.
- Закляття Teleport з перевіркою дальності `√(dx² + dy² + 5dz²) ≤ 5·рівень` — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` (межі-стіни) · `fog-of-war` (огляд найближчих кімнат) · `stairs-levels` · `teleport` (пасток-телепортів) / `teleport-one-way` (куби) · `hp-damage` · `unit-xp-skills` · `inventory-items` / `item-pickup` · `round-currency` (золото) · `thief` (гобіт) · `status-effects` (сон, параліч, висмоктування) · `temporary-modes` (Invisibility, Fear, Levitation, Time Stop) · `player-death` · `permadeath` · `save-game` · `cheat-codes` (SV) · `keyboard-controls` · `state-as-data` (мапа як функція).
- Вже пропоновані: `+town-hub` (корчма) · `+random-encounter` · `+altar-sacrifice` · `+exp-doubling-by-level` · `+coordinate-teleport` (як у Wizardry).
- **Нема** → пропозиції карток:
  - `+hash-room-generation` «Кімната обчислюється з координат: хеш → біти стін і особливість» · levels/generation · 🥉.
  - `+idle-auto-turn` «Нема вводу N секунд → гра робить хід за гравця» · game-logic/opponent · 🌱.
  - `+encounter-roll` «Шанс зустрічі на хід + кидок класу монстра» · entities/spawn · 🌱.
  - `+gold-to-xp` «Золото міняється на досвід у безпечному місці» · game-logic/economy · 🌱.
  - `+pit-fall-check` «Яма: кидок спритності — впав чи спустився сам» · entities/interact · 🌱.
  - `+forced-elevator` «Клітина неминуче переносить на рівень вище» · entities/interact · 🌱.
  - `+level-choice-portal` «Портал, де гравець вводить номер рівня» · entities/interact · 🌱.
  - `+random-feature-effect` «Особливість кімнати з випадковим ефектом (фонтан, трон)» · entities/interact · 📎.
  - `+level-drain` «Ворог забирає рівень досвіду» · entities/state · 📎.
  - `+charisma-reactions` «Стат героя змінює реакцію монстрів» · entities/state · 🌱.
  - `+save-at-inn` «Збереження лише в безпечному місці» · game-logic/save · 🌱.

## Пропозиції до словників
- `+trigger:room_feature(kind)` — герой у кімнаті з особливістю (фаза «особливість»).
- `+cond:stat_roll(stat, die)` — кидок кубика проти атрибута (1d20 ≤ DEX, 1d30 ≤ CHR).
- `+effect:stay` — хід «стояти», зокрема автоматичний по тайм-ауту.
- `+effect:sacrifice(gold)` (як у Sword of Fargoal) · `+effect:level_drain(a)` (як у Wizardry) · `+effect:return_to_town` (як у Wizardry; Scroll of Rescue).
- `+role:room-feature` — особливість кімнати з дією «увійти/вжити» (фонтан, трон, вівтар, куб).
- `+window:inn-window` — корчма: лікування, золото → досвід, сейв.
- `+ui:spell-units` — очки заклинань (SU).
- `+feature:save-at-inn` — сейв лише в корчмі.
- `+axis:time=turn-with-timeout` — хід, що настає сам після тайм-ауту.
- `+card:hash-room-generation` · `+card:idle-auto-turn`.

## Джерела
- ⭐ [Wikipedia: Telengard](https://en.wikipedia.org/wiki/Telengard) — 50 рівнів, 2 млн кімнат з позиції героя без збереження, real-time без паузи, сейв у корчмі, шість атрибутів і їхній зміст, старт без грошей, fight/magic/evade, нежить і дракони, S — стояти, X — південь, платформи.
- [C64-Wiki (DE): Telengard](https://www.c64-wiki.de/wiki/Telengard) — 40 000 кімнат на рівень, незмінне підземелля, корчми, вівтарі, трони, фонтани, куби (у v5.2 ≤ рівень + 3), скриньки зі струмом, заклинання, 5 с на хід, F1/F3/F5/F7, HP/SU/EXP, 2000 досвіду й подвоєння, предмети +X, SV-чіт.
- [AtariHQ: Telengard](https://atarihq.com/danb/Telengard.shtml) — формула з константами 1.6915 / 1.4278 / 1.2462, біти верхньої й лівої стін, коди особливостей 1–9 (Inn, Pit, Teleporter, Stairway, Altar, Fountain, Cube, Throne, Box).
- [Telengard in Elm: The Dungeon](https://elm-telengard.blogspot.com/2014/03/the-dungeon.html) — 200×200×50, старт (25, 13, 1), коди 1–15 з ліфтом, виправлення сходів на рівнях 1 і 50.
- [Telengard in Elm: Line of Sight and Movement](https://elm-telengard.blogspot.com/2014/03/line-of-sight-and-movement.html) — огляд чвертями, ями (1d20 проти DEX, 3d6), ліфти, формула телепорту, 20 % ланцюг, куби, Astral Walk, Pass Wall, формула Teleport.
- [Telengard in Elm: Encounters](https://elm-telengard.blogspot.com/2014/04/encounters.html) — 4 фази ходу, 30 % зустрічі, Invisibility 80 %, Fear, плащ, формули рівня й HP, ельф/гобіт/дракон від CHR, ініціатива 50 + 2·DEX.
- [RogueBasin: Telengard](https://www.roguebasin.com/index.php/Telengard) — 5 с без команди → Stay; Stay у бою дає ворогу вдарити; один клас-гібрид; відкрита гра.
- [aquest.com: Telengard](http://www.aquest.com/telen.htm) — автор про DND (1976–77), 8 КБ → 32 КБ, платформи Avalon Hill, PC-версія на C.

## Непевне
- (?) Код особливості 1: «Inn» у лістингу Atari, «Elevator» у реімплементації (за C64); версії, мабуть, різняться — на рівні 1 ліфти стають сходами вгору до корчми.
- (?) Два різні записи формули (AtariHQ і Elm) — суть однакова (хеш від x, y, z з трьома константами), деталі бітів різняться між версіями.
- (?) «Real-time» у Wikipedia проти «покроково з 5 с на хід» у C64-Wiki — описано як хід із тайм-аутом; точний таймінг різних портів не перевірив.
- (?) Ефекти фонтанів, тронів і скриньок по пунктах — джерела дають лише загальний опис.
- (?) Повний список заклинань за рівнями та їхня вартість у SU — бачив лише окремі назви.
- (?) Рекорд 2021 р. з Wikipedia («level 9,949» проти «level 27940 Ogre») — неясно, рівень героя чи підземелля; гра дозволяє рівні нижче 50 лише в деяких версіях.
- (?) Діагональний рух і розкладка клавіш поза C64 — не перевірив.
