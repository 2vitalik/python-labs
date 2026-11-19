---
title: Dragon Crystal (ドラゴンクリスタル ツラニの迷宮)
slug: dragon-crystal
aka: ["Dragon Crystal: Tsurani no Meikyū", ドラゴンクリスタル ツラニの迷宮, ドラゴンクリスタル]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 1990
platforms: [Game Gear (JP 1990; NA/EU 1991), Master System (EU 1991), 3DS Virtual Console (2012)]
links:
  - {kind: other, url: "https://shrines.rpgclassics.com/sms/dragoncrystal/manual.shtml", best: true, note: "RPGClassics «How to play»: кнопки, тіки (що коштує тік, а що ні), їжа раз на 10 тіків, лікування раз на 8, ідентифікація вжитком і кидком, прокльони, продовження за гроші (до 3), вихід у вертикальній стіні"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dragon_Crystal", note: "огляд: туман, покроковість, оточення, їжа (1 очко — 6 клітин, максимум 99), кольорові предмети, яйце-дракон, жаби, запаморочення, ніндзя, слизи-клони, Кубок на 30-му поверсі"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ドラゴンクリスタル_ツラニの迷宮", note: "JA: 30 поверхів, нова мапа щогри, 8 категорій предметів по 8 штук, Почі-яйце блокує ворогів, сімʼї монстрів (іржа, −макс. HP, −рівень, крадіжка їжі), керування"}
  - {kind: other, url: "https://shrines.rpgclassics.com/sms/dragoncrystal/items.shtml", note: "усі сувої / книги, жезли, зілля, кільця з ефектами"}
  - {kind: other, url: "https://shrines.rpgclassics.com/sms/dragoncrystal/monsters_nopix.shtml", note: "32 монстри: HP, досвід, поверхи, особливі атаки й темп"}
  - {kind: other, url: "https://shrines.rpgclassics.com/sms/dragoncrystal/levels.shtml", note: "16 рівнів-звань, досвід, формули HP, стадії дракона"}
  - {kind: other, url: "https://shrines.rpgclassics.com/sms/dragoncrystal/floors.shtml", note: "монстри по поверхах, ціна продовження"}
  - {kind: other, url: "https://magnvsrpgjourney.substack.com/p/dragon-crystal-segas-own-early-roguelite", note: "огляд: туман і монстри, що його повертають, яйце-барʼєр, варп у гущу ворогів, гроші лише на продовження, відмінності від Fatal Labyrinth"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dragon+Crystal+Game+Gear+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-by-input, move-4dir, hp-damage, hunger-clock, item-identification, item-pickup, inventory-items, inventory-limit, dungeon-generation, stairs-levels, fog-of-war, status-effects, speed-per-type, teleport, thief, melee-vs-ranged, chase-player, player-death, game-over-continue, status-panel, game-screen, +throw-item, +curse-item, +search-hidden, +wait-turn, +xp-level-up, +level-up-titles, +pet-ally, +follower-chain, +growth-stages, +mimic, +sleeping-enemy, +split-instead-of-attack, +companion-blocker, +food-regen-fuel, +equipment-rust, +stat-drain, +fog-reset, +slayer-weapon, +paid-continue]
proposes: ["+trigger:hunger", "+effect:eat", "+effect:identify", "+effect:level_up", "+effect:forget_map", "+effect:drain", "+effect:rust", "+effect:wait", "+cond:cursed", "+role:pet", "+feature:paid-continue", "+card:companion-blocker", "+card:food-regen-fuel", "+card:equipment-rust", "+card:stat-drain"]
author: opus
date: 2026-11-19
---

# Dragon Crystal — портативний Rogue від Sega: їжа живить лікування, яйце-дракон іде слідом і лише закриває спину

## Суть
Покроковий роглайк для Game Gear (1990) і Master System: учень магічної школи Оші впав у кристал і має пройти 30 згенерованих поверхів лабіринту-лісу, щоб на останньому взяти кристал (у WP — Святий Кубок). Крок героя = тік, після якого діють монстри; поверх відкривається з туману, предмети — кольорові невідомі, доки не вжиєш чи не кинеш. Незвичне для корпусу: **їжа — паливо регенерації** (є їжа — HP росте, нема — тане), а **супутник** — яйце, що з рівнем героя виростає в дракона, — нікого не бʼє, а лише стоїть позаду й не дає ворогам оточити. Гроші не купують нічого, крім продовження після смерті.

## Поле і час
- Поверх — квадратна сітка-лабіринт з кімнат; перші 10 поверхів — ліс із дерев, кактусів, соняшників і статуй Моаї; на Master System є ще кришталеві й грибні поверхи (огляд).
- 30 поверхів; мапа кожного генерується наново щогри (JA, RPGClassics); предмети й вороги розкладені випадково.
- Туман: поверх стартує прихованим і відкривається, коли герой ходить; сувій Map показує весь поверх, а стан «туман» знову ховає досліджене (огляд).
- Час — **тіки**: крок, удар, підняти предмет, вжити предмет — 1 тік; вдягнути / зняти й покласти на підлогу — 0 тіків. Без вводу світ стоїть — думати можна скільки завгодно.
- За тік: монстри ходять (швидкі — двічі, повільні — раз на 2 тіки, деякі нерухомі), їжа витрачається, HP відновлюється, стани спадають (крім сповільнення).
- Оточення небезпечне: кожен сусідній ворог бʼє раз на кожну дію героя.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Оші (герой) | player | HP, PW (сила), AC (захист), рівень-звання 1–16, F — їжа 0–99, гроші, досвід | крок або удар у сусіднього монстра; щотік — їжа й лікування |
| Почі: яйце → малий → великий → сірий дракон | ally | стадія за рівнем героя | іде слідом на клітину позаду; не атакує й не допомагає; ворог не пройде крізь нього |
| Стіна, дерево, кактус, статуя | static | — | непрохідні; статуя Моаї «всміхається», коли туман знято (?) |
| Прихований прохід | static | у певних стінах | зникає, якщо кілька разів чекати перед стіною |
| Вихід (варп-клітина) | static | іншого кольору; у вертикальній стіні кімнати, не на краю мапи | перехід на наступний поверх (часто в гущу ворогів) |
| Кристал / Святий Кубок | pickup | лише 30-й поверх, виходу там нема | підняв — кінець гри |
| Хліб (торт) / мʼясо | pickup | F +≈20 / +≈40 (WP: 11–27 / 42–46) | відновлює їжу до 99 |
| Гроші | pickup | сума | лише на продовження після смерті |
| Меч | pickup | +PW, тип не прихований | може бути проклятий; «вбивці» (Magi Masher, Hardbreaker, Ninjakiller, Dragonblade) сильні проти свого типу ворогів |
| Броня | pickup | +AC | може бути проклята; іржавіє від атак «очей» |
| Сувій / книга (14 видів) | pickup | колір-назва невідома | Blade, Shield, Norust, Bless, Map, Shift, Daze, Magi, Cyber, Ninja, Dragon, Summon, Blank, Potion |
| Жезл (12) | pickup | колір-назва невідома | Flame / Flash / Thunder (4 / 6 / 8 × рівень), Travel, Wind, Berserk, Reshape, Silent, Drain, Spirit, Wood, Wither |
| Зілля (13) | pickup | колір-назва невідома | Minheal ¼, Midheal ½, Maxheal, Slow, Slowfix, Fog, Daze, Cure, Freeze, Power, Reflex, Water, Wither |
| Кільце (10) | pickup | колір-назва невідома | Heal, Magic, Food, Sight, Shield +4 AC, Ogre +4 PW, Cursed, Hunger, Toy, Shift |
| Жаби (3 види) | enemy | HP 6–52 | отруюють |
| Полумʼяна / крижана планка | enemy | 2 ходи за тік | запаморочення (рух у випадковий бік), дальня атака |
| Ніндзя (3 види), Magician, Sorcerer | enemy | — | телепортуються; дальня атака; Magician — запаморочення, Sorcerer — туман |
| Акула піщана / Sand jaws | enemy | — | крадуть їжу |
| Очі Medama / Medaoyaji | enemy | раз на 2 тіки | іржа броні / зброї |
| Дріади (Drayad, Hamadryad, Treant) | enemy | нерухомі | дальня атака; дві старші — мінус макс. HP |
| Равлики (3 види) | enemy | — | −1 / −2 PW; King snail — мінус рівень |
| Слизи (Blue slime, Red jelly) | enemy | раз на 2 тіки | інколи діляться замість атаки |
| Metal orb, Death orb | enemy | — | діють, лише коли їх атакують |
| Мімік | enemy | вигляд меча чи жезла | оживає, коли підійти |
| Killer bat, Blob | enemy | 2 ходи за тік | швидкі |
| Дракон | enemy | поверхи 29–30 | найсильніший ворог (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух і бій:
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`, `custom: «минає 1 тік»`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(cell, enemy)` → ТО `damage(enemy, n)` — удар = крок у монстра, теж 1 тік.
- КОЛИ `tick` → ТО `custom: «кожен монстр робить хід: швидкі двічі, повільні раз на 2 тіки, нерухомі лише бʼють»`.
- КОЛИ `adjacent(enemy, hero)` → ТО `damage(hero, n)` — кожен сусід раз на дію героя.
- КОЛИ `input(wait)` → ТО `custom: «тік без дії: підманити монстрів під жезл чи кидок, перечекати стан, шукати прохід»`.
- КОЛИ `turn_end(hero)` → ТО `custom: «Почі стає на клітину, з якої герой пішов»`.
- КОЛИ `custom: «ворог іде в клітину Почі»` → ТО `block`.

Їжа й лікування:
- КОЛИ `timer(10)` → ЯКЩО `counter(food, >, 0)` → ТО `counter(food, -1)` (RPGClassics; WP: 1 очко їжі — 6 клітин ходу).
- КОЛИ `timer(8)` → ЯКЩО `counter(food, >, 0)` → ТО `heal(hero, level)`.
- КОЛИ `tick` → ЯКЩО `counter(food, ==, 0)` → ТО `damage(hero, n)` — лікування стоїть, HP тане до смерті від голоду.
- КОЛИ `input(use, food)` → ТО `counter(food, +20|+40)` до максимуму 99.
- КОЛИ `input(equip, ring)` → ТО `custom: «кільце міняє періоди їжі / лікування: Heal 6 / 2, Food 18 / 4, Hunger 4 / 4, Cursed 6 / ніколи»`.

Предмети:
- КОЛИ `input(pickup)` → ЯКЩО `custom: «у категорії менше 8 предметів»` → ТО `pickup`; гроші й їжа — лічильники без ліміту.
- КОЛИ `input(use, item)` → ТО `use(hero, item)`, `custom: «колір-назву розпізнано для всіх таких предметів до кінця гри»`; назви кольорів перемішуються щогри.
- КОЛИ `input(throw, item)` → ТО `throw(item)`, `custom: «тип розпізнано навіть при промаху; предмет утрачено»`.
- КОЛИ `contact(item, monster)` → ТО `damage(monster, n)` або ефект предмета (зілля Freeze паралізує ціль).
- КОЛИ `input(equip, item)` → ЯКЩО `custom: «предмет проклятий»` → ТО `custom: «не знімається до сувою Bless; меч / броня без бонусу, кільце — шкідливий ефект»`.
- КОЛИ `input(use, rod)` → ТО Flame / Flash / Thunder: `damage(target, 4|6|8 × level)`; Travel: `next_level`; Wind: `disappear_b` (без досвіду); Reshape: `transform(target, random_monster)`; Drain: `swap(hp_hero, hp_target)`; Summon / Spirit: `spawn(monster)`; Wither: `custom: «рівень −1»`.
- КОЛИ `input(use, rod_berserk)` → ТО `damage(target, 2 × HP)`, `hp(hero, -½)`.
- КОЛИ `input(use, scroll)` → ТО Map: `reveal(floor)`; Shift: `teleport(hero, random_room)`; Bless: `custom: «зняти прокляття; прокляте кільце зникає»`; Magi / Cyber / Ninja / Dragon: `transform(sword, slayer)`; Norust: `set_state(armor, norust)` до кінця поверху; Daze: `set_state(monsters, dizzy)` доки герой не підійде.
- КОЛИ `input(use, potion)` → ТО Minheal / Midheal / Maxheal: `heal(hero, ¼|½|all)`; Slow / Freeze / Daze / Fog: `set_state(hero, slow|paralysis|dizzy|fog)`; Cure: `clear_state(hero, poison|dizzy|blind)`; Power / Reflex: `custom: «PW / AC +1 назавжди»`; Wither: `custom: «базова PW = 0»`.

Монстри:
- КОЛИ `contact(toad, hero)` → ТО `set_state(hero, poison)`.
- КОЛИ `contact(flame_bar|ice_bar|magician, hero)` → ТО `set_state(hero, dizzy)` — рух у випадковий бік.
- КОЛИ `contact(sorcerer, hero)` → ТО `set_state(hero, fog)`, `custom: «досліджену мапу знову сховано»` (?).
- КОЛИ `contact(medama, hero)` → ЯКЩО `not state(armor, norust)` → ТО `custom: «іржа броні»`; Medaoyaji — `custom: «іржа зброї»`, захисту нема.
- КОЛИ `contact(shark, hero)` → ТО `take(hero, food)`.
- КОЛИ `contact(hamadryad|treant, hero)` → ТО `custom: «макс. HP −n»`.
- КОЛИ `contact(snail, hero)` → ТО `custom: «PW −1 / −2»`; King snail — `custom: «рівень −1»`.
- КОЛИ `turn_start(slime)` → ЯКЩО `prob(p)` → ТО `split(slime)` замість атаки.
- КОЛИ `turn_start(ninja|sorcerer)` → ТО `teleport(enemy, cell)`.
- КОЛИ `custom: «Metal / Death orb ще не атакували»` → ТО `custom: «стоїть»`.
- КОЛИ `adjacent(hero, mimic)` → ТО `set_state(mimic, awake)`.

Досвід і поверхи:
- КОЛИ `died(monster)` → ТО `counter(exp, +n)` (2–300 залежно від виду).
- КОЛИ `counter(exp, >=, threshold)` → ТО `custom: «рівень +1, нове звання (Apprentice … Masterlord), PW +1…5, макс. HP +(рівень + поверх) × 2»`.
- КОЛИ `counter(level, >=, 5|9|13)` → ТО `transform(pochi, baby_dragon|big_dragon|gray_dragon)` (?).
- КОЛИ `enter(hero, exit)` → ТО `next_level`, `custom: «новий згенерований поверх у тумані»`.
- КОЛИ `input(wait)` → ЯКЩО `cell(front, hidden_passage)` → ТО `set_cell(front, floor)` після кількох очікувань (кільце Sight — з першого).
- КОЛИ `picked(hero, crystal)` → ТО `win`.
- КОЛИ `hp_zero(hero)` → ЯКЩО `counter(gold, >=, cost)` and `counter(continues, <, 3)` → ТО `currency(-cost)`, `respawn(hero, same_floor)`, `custom: «лишаються лише вдягнені меч і броня; рівень і розпізнані кольори — теж»`; інакше `game_over`.
- Перемога: підняти кристал на 30-му поверсі · Поразка: HP = 0 без грошей на продовження або після трьох продовжень · Рахунку нема; гроші — лише ціна продовження (росте з поверхом і на +100 за кожне наступне).

## Керування і ввід
- Хрестовина — крок; крок у монстра — удар (дії «атакувати» окремо нема).
- Кнопка 1 (GG) / A (SMS) — сабскрін предметів і дій; кнопка 2 / B — підняти предмет під ногами або чекати тік (так само шукати прохід перед стіною).
- Start: GG — утримання пришвидшує анімацію (JA: Start + хрестовина — швидкий рух); SMS — перемикач швидкої / повільної анімації.
- Сабскрін: вибір категорії → предмета → команди Equip / Use / Drop / Throw кнопкою 2.

## Вікна, меню, HUD
- `game-screen`: поверх у тумані, герой і Почі; у вікні — F (їжа) і стан героя (?).
- `inventory-window` (сабскрін): поверх, звання, HP, PW, AC, гроші; підменю Swords · Armor · Books (GG) / Scrolls (SMS) · Rods · Potions · Rings; команди Equip / Use / Drop / Throw.
- `message-log`-подібні повідомлення: що сталося від предмета («нічого не сталося» теж розпізнає колір); тексти GG і SMS різні.
- `end-screen` смерті з підсумком → `game-over-continue`: продовжити за гроші (ціна) або кінець.
- `end-screen` фіналу — кінцівка після кристала.
- Переходи: титул (?) → `game-screen` → (вихід) наступний поверх → … ; `game-screen` → кнопка 1 → `inventory-window` → назад; смерть → підсумок → продовження / кінець.

## Фічі поза полем
- Нема збережень: забіг — одна сесія (менш як 2 години, якщо пощастить); на 3DS Virtual Console — призупинення.
- `continue` за гроші до 3 разів (4 життя), ціна 100–800 залежно від поверху + 100 за кожне наступне продовження.
- Музика змінюється на 11-му і 21-му поверхах.
- Дві версії: GG і SMS відрізняються назвами монстрів і предметів (Books / Scrolls, Cyber / Gas), повідомленнями і кількома поверхами.

## Варіації й родичі
- [Fatal Labyrinth](fatal-labyrinth.md) — та сама Sega, той самий рік, спільні ассети; інший код мапи, там приховані двері й пастки, а гроші — на похорон, тут — на продовження.
- Dragon Crystal II для мобільних — анонсовано, не вийшла.
- [Rogue](rogue.md) — предок (невідомі предмети, голод); [Hack](hack.md) / [NetHack](nethack.md) — бойовий улюбленець; [Mystery Dungeon](mystery-dungeon.md), [Torneko](torneko-great-adventure.md) — японська консольна гілка «крок за крок».
- **Осі варіацій**: їжа «лише голод (Rogue) / голод і переїдання (Fatal Labyrinth) / паливо регенерації (Dragon Crystal)» · супутник «нема / бойовий (NetHack) / барʼєр без атаки, що росте з рівнем героя» · гроші «крамниця / похорон / продовження» · ідентифікація «сувій identify / лише вжитком чи кидком» · постійна шкода «нема / іржа спорядження / мінус макс. HP, сила, рівень».

## Цікавинки для курсу
- Їжа як паливо регенерації: два періодичні таймери (їжа −1 раз на 10 тіків, лікування раз на 8 тіків на величину рівня), кільця переписують обидва періоди — 🌱.
- Супутник-барʼєр: іде слідом на клітину позаду, не бʼється, змінює вигляд за рівнем героя — 📎.
- Кольорова ідентифікація з перемішуванням назв щогри; кидок як безпечне розпізнавання — 📎.
- Монстри з «вічними» наслідками (іржа, −макс. HP, −PW, −рівень) і стан «туман», що знову ховає мапу, — 📎 за сімʼю.
- Темп монстрів: 2 ходи за тік / раз на 2 тіки / нерухомі / діють лише після удару / мімік — 📎 (`speed-per-type`).
- Генерація 30 поверхів, де вихід лише у вертикальній стіні кімнати й не на краю мапи, — 🥇 (`dungeon-generation`).
- Продовження за гроші з ціною від поверху й номера спроби, втрата неекіпірованого — 🌱.

## Мапа на каталог
- Є: `move-by-input` + `move-4dir` · `hp-damage` · `hunger-clock` ↔ F і голод · `item-identification` ↔ кольори · `item-pickup` · `inventory-items` · `inventory-limit` ↔ 8 у категорії · `dungeon-generation` · `stairs-levels` ↔ варп-вихід · `fog-of-war` · `status-effects` ↔ отрута, запаморочення, параліч, сповільнення · `speed-per-type` · `teleport` ↔ сувій Shift, ніндзя · `thief` ↔ акули крадуть їжу · `melee-vs-ranged` · `chase-player` · `player-death` · `game-over-continue` · `status-panel` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+companion-blocker` «Супутник-барʼєр без атаки: займає клітину позаду» · entities/move · 📎 — родич `+follower-chain` і `+pet-ally`.
  - `+food-regen-fuel` «Їжа живить регенерацію; без їжі HP тане» · entities/state · 🌱 (дитина `hunger-clock`) · слоти {eat_every, heal_every}.
  - `+equipment-rust` «Монстр псує спорядження» · entities/combat · 🌱 · слот {target: armor | weapon}.
  - `+stat-drain` «Постійна втрата характеристики (макс. HP, сила, рівень)» · entities/combat · 📎.
  - `+fog-reset` «Стан, що знову ховає досліджену мапу» · interface/render · 🌱 (дитина `fog-of-war`).
  - `+slayer-weapon` «Зброя проти типу ворогів» · entities/combat · 🌱.
  - `+split-instead-of-attack` «Ворог інколи ділиться замість удару» · entities/spawn · 📎 (родич `+split-on-hit`).
  - `+paid-continue` «Продовження за ігрову валюту з ростом ціни» · game-logic/lose · 🌱.
  - Повтори з корпусу: `+throw-item`, `+curse-item`, `+search-hidden`, `+wait-turn`, `+xp-level-up`, `+level-up-titles` (Fatal Labyrinth), `+pet-ally`, `+follower-chain`, `+growth-stages` (тут стадії за рівнем героя), `+mimic`, `+sleeping-enemy` (сфери діють лише після удару).

## Пропозиції до словників
- `+trigger:hunger` — їжа скінчилась (F = 0): лікування стоїть, HP тане.
- `+effect:eat` — зʼїсти: F +n до 99.
- `+effect:identify` — розпізнати колір-тип предмета вжитком або кидком.
- `+effect:level_up` — рівень +1 зі званням, PW і макс. HP.
- `+effect:forget_map` — знову сховати досліджену мапу (туман від Sorcerer і зілля Fog; Beneath Apple Manor).
- `+effect:drain` — постійно зменшити характеристику (макс. HP, PW, рівень).
- `+effect:rust` — зіпсувати вдягнене спорядження.
- `+effect:wait` — пропустити тік (і шукати прохід перед стіною).
- `+cond:cursed` — предмет проклятий.
- `+role:pet` — супутник, що йде за героєм без команд (Почі).
- `+feature:paid-continue` — продовження після смерті за гроші, до 3 разів.
- `+card:companion-blocker` · `+card:food-regen-fuel` · `+card:equipment-rust` · `+card:stat-drain`.

## Джерела
- ⭐ [RPGClassics: How to play](https://shrines.rpgclassics.com/sms/dragoncrystal/manual.shtml) — кнопки GG / SMS, сабскрін, тіки й безкоштовні дії, ідентифікація, кидок, прокльони, їжа (хліб ≈20, мʼясо ≈40, −1 раз на 10 тіків), лікування раз на 8 тіків, продовження до 3 разів, вихід у вертикальній стіні, кристал на 30-му.
- [Wikipedia: Dragon Crystal](https://en.wikipedia.org/wiki/Dragon_Crystal) — дати й платформи, туман, ліс із Моаї, варп-клітина, покроковість і оточення, їжа (торт 11–27, мʼясо 42–46, максимум 99, 1 очко — 6 клітин), кольорові предмети, ефекти ворогів, яйце-дракон, Кубок на 30-му, продовження за гроші, Fatal Labyrinth.
- [Wikipedia JA](https://ja.wikipedia.org/wiki/ドラゴンクリスタル_ツラニの迷宮) — 30 поверхів, нова мапа щогри, керування, 8 категорій по 8 штук, Почі блокує ворогів, сімʼї монстрів, продовження лише з вдягненим.
- [RPGClassics: Items](https://shrines.rpgclassics.com/sms/dragoncrystal/items.shtml) · [Monsters](https://shrines.rpgclassics.com/sms/dragoncrystal/monsters_nopix.shtml) · [Levels](https://shrines.rpgclassics.com/sms/dragoncrystal/levels.shtml) · [Floors](https://shrines.rpgclassics.com/sms/dragoncrystal/floors.shtml) — повні таблиці предметів, 32 монстрів, 16 звань і формул HP, ціни продовження.
- [Magnvs RPG Journey](https://magnvsrpgjourney.substack.com/p/dragon-crystal-segas-own-early-roguelite) — туман і його скидання, яйце-барʼєр, варп у гущу ворогів, відмінності GG / SMS і від Fatal Labyrinth.
- YouTube: пошук «Dragon Crystal Game Gear gameplay».

## Непевне
- (?) Темп їжі: RPGClassics — 1 одиниця на 10 тіків; WP — 1 очко на 6 клітин ходу; чи удари теж їдять їжу — не перевірено.
- (?) Пороги стадій Почі (рівні 5 / 9 / 13) — з розкладки таблиці RPGClassics, прямо не підписані.
- (?) Що саме робить стан «туман»: огляд каже «скидає туман війни»; чи це ще й обмеження огляду — не перевірено.
- (?) «Дракон» на 29–30 поверхах — у таблиці монстрів поверхів, але без опису; чи це бос — невідомо.
- (?) Головний предмет: WP / JA — Святий Кубок (聖杯), RPGClassics — кришталева куля.
- (?) Що на основному екрані HUD (F, HP?) — JA згадує «F у вікні»; точний склад не перевірено.
- (?) Формула шкоди удару (PW, AC) і ймовірність поділу слизів — не знайдено.
- (?) Порада RPGClassics «зачищений поверх полегшує останній» — механізм не пояснено.
