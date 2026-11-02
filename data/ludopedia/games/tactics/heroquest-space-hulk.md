---
title: "HeroQuest + Space Hulk (настільні данжен-кроулери на сітці)"
slug: heroquest-space-hulk
family: tactics
also: [roguelike, board-digital]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: state
year: 1989
platforms: [board, "Amiga/ST/PC (HeroQuest 1991)", "PC/Amiga (Space Hulk 1993)", "PC/Mac/iOS/консолі (Space Hulk 2013)", "HeroQuest Companion App (2021)"]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/HeroQuest", best: true, note: "HeroQuest: майстер Zargon/Morcar, 4 героя, рух 2d6, кубики черепів і щитів, пошук скарбів/пасток/таємних дверей, заклинання, цифрові версії"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Space_Hulk", note: "Space Hulk: модульні коридори, асиметрія, очки дій, командні очки, блипи, таймер, overwatch і заклинювання, редакції"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Space_Hulk_(1993_video_game)", note: "real-time з Freeze Time, overwatch, туман, блипи"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Space_Hulk_(2013_video_game)", note: "покрокова цифрова версія за 4-ю редакцією, undo, hotseat"}
  - {kind: other, url: "https://www.boardgamegeek.com/boardgame/2163", note: "BGG: Space Hulk"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=HeroQuest", note: "пошук BGG: HeroQuest і доповнення"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=space+hulk", note: "пошук; Space Hulk 2013, Tactics"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=heroquest+how+to+play", note: "пошук; правила HeroQuest"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=space+hulk+board+game+how+to+play", note: "пошук; правила Space Hulk"}
stage: v1
coverage: 70
mechanics: [move-4dir, impassable-cells, hp-damage, melee-vs-ranged, projectile-shot, blast-wave, key-and-door, item-pickup, inventory-items, spawn-points, reinforcements, move-timer, hot-seat, ai-opponent, destroy-all-enemies, reach-exit, sequential-levels, save-progress, game-screen, end-screen, +room-reveal, +search-action, +game-master, +dice-movement, +combat-dice-symbols, +action-points, +command-points, +overwatch, +weapon-jam, +blips, +facing-hit-bonus, +fog-of-war, +line-of-sight-attack, +treasure-deck, +wandering-monster, +sustained-fire, +spell-once, +permadeath, +asymmetric-sides]
proposes: ["+trigger:input", "+trigger:sighted", "+trigger:enemy_moved", "+trigger:turn_start", "+cond:line_of_sight", "+cond:prob", "+cond:facing", "+cond:state", "+effect:reveal", "+effect:set_cell", "+effect:set_status", "+effect:give", "+effect:face", "+effect:spawn_at", "+role:piece", "+role:gate", "+role:hazard", "+role:supply", "+ui:action-pips", "+ui:dice-result", "+window:quest-briefing", "+window:character-select", "+feature:mode-coop", "+axis:actors"]
author: opus
date: 2026-11-02
---

# HeroQuest + Space Hulk — дошка-підземелля з кімнатами, що відкриваються дверима, і прихований противник за ширмою

## Суть
Два настільні хіти 1989 року задають набір правил «данжен-кроулера на сітці». У **HeroQuest** 4 героя (кооператив) проходять квест на дошці-замку: кидають 2d6 на рух, відкривають двері — майстер (Zargon/Morcar) за ширмою виставляє вміст кімнати, — бʼються кубиками з черепами й щитами, шукають скарби, пастки й таємні двері. У **Space Hulk** Термінатори (мало очок дій, потужні постріли) пробиваються коридорами покинутого корабля проти Генокрадів (швидкі, смертельні впритул), що входять прихованими **блипами**; Термінатор має **таймер** на хід і приховані командні очки, а `overwatch` стріляє в ході суперника. Спільне ядро: сітка-підземелля, туман кімнат, видимість по лінії, асиметрична прихована сторона.

## Поле і час
- **HeroQuest**: одна дошка 26×19 клітин (?) з фіксованими стінами кімнат і коридорів; квест (мапа в книзі майстра) визначає, які двері, монстри, пастки й меблі є; на дошці спочатку порожньо — усе зʼявляється в міру видимості.
- **Space Hulk**: модульні секції (коридори шириною 1 клітину, кімнати, двері, вентиляція у 2-й ред.), склеювані «як пазл» за схемою місії; входи-точки появи генокрадів по краях.
- Хід покроковий: HQ — герої по черзі за годинниковою стрілкою, потім майстер усіма монстрами; SH — фаза Термінаторів (з таймером), фаза Генокрадів.
- Туман: HQ — невідкриті кімнати/коридори порожні на дошці; SH — блипи (кількість генокрадів у сигналі невідома), у 1-й ред. ще й командні очки приховані.
- Випадковість: кубики руху (HQ), бою (обидві), колода скарбів (HQ), жетони блипів і командних очок (SH).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Варвар (HQ) | piece | атака 3, захист 2, тіло 8, розум 2 (?) | найсильніший у бою, без магії |
| Гном (HQ) | piece | 2/2/7/3 (?) | роззброює пастки без набору |
| Ельф (HQ) | piece | 2/2/6/4 (?) | одна стихія заклять (3 закляття) |
| Чарівник (HQ) | piece | 1/2/4/6 (?) | три стихії (9 заклять), найслабший у бою |
| Монстри HQ (гоблін, орк, фімір, скелет, зомбі, мумія, воїн хаосу, гаргулья) | enemy | фіксований рух, атака/захист, тіло 1 (?) | ходять під керуванням майстра; бʼють сусідню клітину |
| Майстер (Zargon / Morcar) | — | книга квесту, колода «хаосу» (US) | прихована сторона: виставляє вміст за видимістю, керує монстрами |
| Двері | gate | закриті/відкриті | HQ: відчиняються рухом, відкривають кімнату; SH: відкрити/зачинити — 1 ОД, ламаються атакою |
| Таємні двері (HQ) | gate | приховані | зʼявляються лише після пошуку в кімнаті |
| Пастки HQ (яма, спис, скриня, обвал) | hazard | — | непомічена яма — −1 тіла; обвал лишає блок; знешкоджуються пошуком/набором |
| Меблі HQ (скрині, столи, трон…) | static | — | непрохідні, часто з квестовими предметами |
| Скарб (картка) | pickup | колода 24–25, з них 8–10 «погані» | золото, зілля або блукаючий монстр / пастка |
| Сходи HQ | static | — | старт і вихід з квесту |
| Термінатор (SH) | piece | 4 ОД, напрям погляду | штормболтер (дальній), силовий кулак; рух уперед 1 ОД, назад 2, поворот 1 (?) |
| Термінатор з важким вогнеметом / штурмовою гарматою (SH) | piece | обмежені заряди | вогнемет палить секцію; гармата — швидка стрільба, вибух при перегріві (?) |
| Сержант (SH) | piece | — | лідер загону; у деяких місіях його смерть — поразка (?) |
| Генокрад (SH) | enemy | 6 ОД | лише ближній бій (3 кубики проти 1), швидкий, повертається дешево |
| Блип (SH) | enemy | 6 ОД, жетон 0–3 генокради (за редакцією) | рухається прихованим; у полі зору → перетворюється на фігури |
| Командні очки (SH) | supply | 1–6 щоходу (жетон) | бонусні ОД для будь-якого Термінатора |
| Таймер (SH) | — | пісочний годинник (~2–3 хв) (?) | хід Термінаторів обривається, коли пісок вийшов |
| Точка входу (SH) | spawner | край карти | тут блипи заходять підкріпленням щоходу |

## Правила (КОЛИ → ЯКЩО → ТО)
- **HeroQuest**
- КОЛИ `turn_start(hero)` → ТО герой робить рух і одну дію в будь-якому порядку, але не розриваючи рух дією посередині: рух = `custom: «2d6 клітин»`, дія = атака / закляття / пошук скарбу / пошук пасток і таємних дверей / знешкодження пастки.
- КОЛИ `input(move, hero, cell)` → ЯКЩО `free(cell)` → ТО `move`; крізь іншого героя — лише з дозволу, ділити клітину не можна; діагоналлю не ходять (?).
- КОЛИ `contact(hero, door)` (відчинив) або `line_of_sight(hero, area)` → ТО `reveal(room|corridor)`: майстер ставить монстрів, меблі, двері за мапою квесту; поставлене лишається до знищення.
- КОЛИ `input(attack, hero, adjacent_monster)` → ТО атакувальник кидає N бойових кубиків (черепи), захисник — свої (білі щити — герой, чорні — монстр); `damage(skulls − shields)` тілу.
- КОЛИ `hp_zero(hero)` → ТО герой гине; його речі бере герой у тій самій кімнаті, інакше — монстр (EU) / повертаються новому герою (US).
- КОЛИ `input(cast, spell, target)` → ЯКЩО `line_of_sight` and `not used(spell)` → ТО ефект; захист розумом (mind points) від магії (?); кожне закляття — раз за квест.
- КОЛИ `input(search_treasure)` → ЯКЩО `count(monster, in_room) == 0` → ТО квестовий предмет або `custom: «тягни картку скарбу»`: золото/зілля або блукаючий монстр (`spawn_at` поруч) / пастка (`damage`).
- КОЛИ `input(search_traps)` → ЯКЩО в кімнаті нема монстрів → ТО `reveal(traps, secret_doors)` у поточній кімнаті/коридорі.
- КОЛИ `enter(hero, pit)` → ЯКЩО пастка не знайдена → ТО `damage(1)`, `custom: «хід закінчено»`; обвал → `set_cell(rubble)`.
- КОЛИ всі герої повернулись на сходи / вийшли / загинули → ТО кінець квесту: ЯКЩО мету виконано → `win` героїв (золото → спорядження між квестами); інакше перемога майстра.
- **Space Hulk**
- КОЛИ `turn_start(terminators)` → ТО `custom: «перевернути пісочний годинник»`, тягнути жетон командних очок (1–6); КОЛИ пісок вийшов → `end_turn`.
- КОЛИ `input(action, marine)` → ЯКЩО `ap ≥ cost` (або CP) → ТО крок уперед / назад / поворот на 90° / відкрити двері / постріл / атака, `counter(ap, −cost)`.
- КОЛИ `input(shoot, marine, target)` → ЯКЩО `line_of_sight` і ціль у секторі спереду → ТО 2 кубики, влучання на 6; повторний постріл у ту саму ціль — легше (5+, потім 4+) — `custom: «sustained fire»`.
- КОЛИ `input(overwatch, marine)` → ТО `set_status(marine, overwatch)` (2 ОД); КОЛИ `enemy_moved(g)` в полі зору → ТО безкоштовний постріл на кожну дію генокрада; ЯКЩО на кубиках дубль → `set_status(jammed)`, до розклинення.
- КОЛИ `contact(genestealer, marine)` (атака впритул) → ТО генокрад кидає 3 кубики, Термінатор 1 (+бонуси зброї): вищий результат перемагає, програвший гине; ЯКЩО атака з флангу/тилу і Термінатор переміг → ТО він лише повертається обличчям (?).
- КОЛИ `turn_start(genestealers)` → ТО `spawn_at(blips, entry_points)` (підкріплення за місією); кожен блип/генокрад має 6 ОД.
- КОЛИ `sighted(marine, blip)` → ТО `reveal`: блип перетворюється на 0–3 генокради (за жетоном), ставляться в його клітину й поруч.
- КОЛИ `input(flame, section)` → ТО `custom: «секція горить»`: кидок за кожну фігуру в ній, вогонь блокує прохід до кінця ходу (?).
- Перемога SH — за місією: дійти до точки, спалити секцію, вивести N Термінаторів / для генокрадів — знищити всіх або не дати виконати; HQ — мета квесту (порятунок, вбивство, артефакт).

## Керування і ввід
- Настільно: фігурки рукою; майстер HQ — за ширмою з книгою квестів; SH — пісочний годинник, жетони ОД/CP.
- HeroQuest (1991, комп'ютерна): курсор/миша — обрати героя, «кинути кубики», клікнути клітину, піктограми дій (атака, пошук, закляття, двері); майстер — комп'ютер.
- Space Hulk (1993): real-time з **Freeze Time** — кнопка зупиняє гру на обмежений запас часу, що відновлюється; екран планування (карта згори, накази піктограмами) + вид від першої особи обраного Термінатора й 4 малих вікна загону.
- Space Hulk (2013): покроково за 4-ю ред., undo останньої дії, hotseat.

## Вікна, меню, HUD
- `main-menu` (цифрові версії): кампанія / окремий квест-місія / мультиплеєр / налаштування.
- `custom-window` «Брифінг квесту» (`quest-briefing`) — легенда й мета місії, мапа (у HQ герої мапи не бачать).
- `character-select` — вибір героїв (HQ) / загону й зброї (SH 1993).
- `game-screen`: поле з туманом невідкритого, фігури, `action-pips` ОД обраного Термінатора, `ui:dice-result` (кубики з черепами/щитами), `hp-bar` тіла/розуму героїв (HQ), лічильник командних очок і `timer-countdown` таймера (SH), позначки overwatch/jam.
- `inventory-window` (HQ) — зброя, броня, зілля, золото героя; `shop-window` «Оружейна» між квестами.
- `end-screen` — результат квесту/місії, хто вижив, золото.
- `confirm-dialog` (кінець ходу з невитраченими ОД); `pause-menu`.

## Фічі поза полем
- **Кампанія**: HQ — 14 квестів книги поспіль, герої зберігають спорядження й золото (`save-progress`, `permadeath` загиблого героя з новим замість нього); SH — кампанії-доповнення (Deathwing, Genestealer, Mission Files).
- **Гра за обидві сторони**: правила SH радять грати кожну місію двічі, мінявшись сторонами (`custom-rules` балансу асиметрії).
- `mode-coop` (HQ: усі герої проти майстра; Companion App бере роль майстра — соло/кооп); `hotseat` (SH 2013).
- `turn-timer` (пісочний годинник SH) — фіча складності, в цифрових версіях опційна (?).
- Space Hulk 1993: досвід Термінаторів між місіями кампанії.

## Варіації й родичі
- Нащадки HQ: Warhammer Quest, Descent, Gloomhaven, Mice and Mystics, HeroQuest 2021 (Avalon Hill) з застосунком-майстром; Advanced HeroQuest (тайли генерують підземелля).
- Нащадки SH: Space Hulk: Tactics (2018) і Deathwing (FPS), Space Crusade (1990) — «HeroQuest у космосі»; XCOM (overwatch).
- **Осі варіацій**: противник — людина-майстер за ширмою / комп'ютер / застосунок · рух — кубики (HQ) / очки дій (SH) / фіксований · туман — кімнати відкриваються дверима / блипи невідомого розміру · тиск — нема / **пісочний годинник** / лічильник ходів · реакція поза ходом — нема / overwatch.

## Цікавинки для курсу
- Відкриття кімнати дверима: невидимий вміст зʼявляється за мапою квесту при видимості — 🥉 (два шари: повна мапа і видима гравцю).
- Блипи: жетон невідомого розміру, що розкривається в полі зору, — 🥉.
- Overwatch з заклинюванням на дублі: реакція в ході суперника на кожну його дію — 🥈 (переривання черги дій).
- Очки дій з різною ціною дій (вперед 1, назад 2, поворот 1) + орієнтація фігури — 🥉.
- Кубики з символами (3 черепи / 2 білих щити / 1 чорний) як «шкода − захист» — 📎.
- Пошук у кімнаті без монстрів → картка скарбу з «поганими» картами (блукаючий монстр) — 📎.
- Таймер на хід і приховані командні очки — 📎; майстер як AI, що відкриває кімнати, — 🥈.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` (стіни, меблі, обвал) · `hp-damage` (тіло, розум) · `melee-vs-ranged` (генокрад лише впритул, Термінатор стріляє) · `projectile-shot` · `blast-wave` (вогнемет секцією) · `key-and-door` (двері) · `item-pickup` / `inventory-items` (скарби, зілля, спорядження) · `spawn-points` + `reinforcements` (блипи на входах, блукаючий монстр) · `move-timer` (пісочний годинник) · `hot-seat` · `ai-opponent` (цифрові версії) · `destroy-all-enemies` · `reach-exit` (повернутись на сходи / вивести загін) · `sequential-levels` (квести поспіль) · `save-progress` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+room-reveal` «Кімната відкривається дверима/видимістю» · interface/render · 🥉.
  - `+search-action` «Пошук у кімнаті: скарб, пастки, таємні двері» · entities/interact · 📎.
  - `+game-master` «Сторона-майстер з прихованою мапою» · game-logic/opponent · 🥈.
  - `+dice-movement` «Рух на кидок кубиків» · entities/move · 🌱.
  - `+combat-dice-symbols` «Кубики з символами: удар проти захисту» · entities/combat · 📎.
  - `+action-points` «Очки дій з ціною дій» · entities/state · 🥉 (є в tactics).
  - `+command-points` «Спільний (прихований) запас бонус-дій» · game-logic/economy · 📎.
  - `+overwatch` · `+facing-hit-bonus` · `+fog-of-war` · `+line-of-sight-attack` · `+spell-once` · `+permadeath` — наявні пропозиції корпусу.
  - `+weapon-jam` «Заклинювання при дублі» · entities/combat · 🌱.
  - `+blips` «Сигнал невідомого розміру» · entities/spawn · 🥉.
  - `+treasure-deck` «Колода знахідок з поганими картами» · game-logic/economy · 📎.
  - `+wandering-monster` «Блукаючий монстр за подією» · entities/spawn · 🌱.
  - `+sustained-fire` «Повторний постріл у ту саму ціль легший» · entities/combat · 🌱.
  - `+asymmetric-sides` «Асиметричні сторони з різними правилами» · game-logic/opponent · 🥉.

## Пропозиції до словників
- `+trigger:sighted` (блип у полі зору → розкриття) · `+trigger:enemy_moved` (overwatch) · `+trigger:turn_start` (таймер, жетон CP, підкріплення) · `+trigger:input`.
- `+cond:line_of_sight` · `+cond:prob` (кубики) · `+cond:facing` (сектор стрільби, атака з тилу) · `+cond:state` (overwatch, jammed).
- `+effect:reveal` (кімнати, пастки, блипи) · `+effect:set_cell` (обвал) · `+effect:set_status` (overwatch, jammed) · `+effect:give` (скарб) · `+effect:face` (поворот) · `+effect:spawn_at` (блипи на входах, блукаючий монстр).
- `+role:piece` · `+role:gate` (двері, таємні двері) · `+role:hazard` (пастки) · `+role:supply` (командні очки, колода скарбів).
- `+ui:action-pips` — ОД обраної фігури; `+ui:dice-result` — показ кинутих кубиків із символами.
- `+window:quest-briefing` — брифінг місії; `+window:character-select` — вибір героїв.
- `+feature:mode-coop` — герої разом проти майстра; `+axis:actors` — `party`.

## Джерела
- ⭐ [Wikipedia: HeroQuest](https://en.wikipedia.org/wiki/HeroQuest) — майстер, герої, рух 2d6, бойові кубики, пошук, пастки, колода скарбів, цифрові версії.
- [Wikipedia: Space Hulk](https://en.wikipedia.org/wiki/Space_Hulk) — асиметрія, ОД, командні очки, блипи за редакціями, таймер, overwatch і заклинювання, вентиляція.
- [Wikipedia: Space Hulk (1993)](https://en.wikipedia.org/wiki/Space_Hulk_(1993_video_game)) — Freeze Time, overwatch, туман, блипи, досвід.
- [Wikipedia: Space Hulk (2013)](https://en.wikipedia.org/wiki/Space_Hulk_(2013_video_game)) — покрокова версія за 4-ю ред., undo, hotseat.
- [BGG: Space Hulk](https://www.boardgamegeek.com/boardgame/2163) — сторінка настільної гри.
- BGG: пошук «HeroQuest»; Steam: пошук «space hulk»; YouTube: пошук «heroquest how to play», «space hulk board game how to play».

## Непевне
- (?) Числа героїв HQ (атака/захист/тіло/розум), розмір дошки 26×19, ходи монстрів — з памʼяті; Wikipedia їх не дає.
- (?) Ціни дій SH (назад 2, поворот 1), влучання на 6 з sustained fire 5+/4+, 3 кубики проти 1 у ближньому бою, тривалість таймера — з памʼяті (1-ша/3-тя ред.), Wikipedia лише підтверджує ОД, CP, таймер, overwatch і заклинювання.
- (?) Поведінка вогнемета й штурмової гармати, сержант як умова поразки — з памʼяті.
- (?) Чи можна в HQ ходити по діагоналі — за базовими правилами ні, з памʼяті.
- (?) WebSearch вичерпано; BGG і StrategyWiki віддають 403 на пряму вибірку.
