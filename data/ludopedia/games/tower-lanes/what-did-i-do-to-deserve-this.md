---
title: "What Did I Do to Deserve This, My Lord?"
slug: what-did-i-do-to-deserve-this
aka: ["Holy Invasion of Privacy, Badman! What Did I Do to Deserve This?", "Holy Invasion of Privacy, Badman!", Yuusha no Kuse ni Namaiki da, "勇者のくせになまいきだ。"]
family: tower-lanes
also: [build-sim, dig-gravity]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 2007
platforms: [PSP]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/What_Did_I_Do_to_Deserve_This,_My_Lord%3F", best: true, note: "Dig Power, пожива й мана в блоках, слизовий мох розносить поживу, герой хапає Badman і несе до виходу, сиквели"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/勇者のくせになまいきだ。", note: "JA: повна екосистема (мох → бутон → квітка, личинка → лялечка → муха, ящір і яйця, елемент, Ліліт, дракон), скелети, магічне коло, класи героїв, or2 і 3D"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Holy+Invasion+of+Privacy+Badman+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [dig-terrain, hp-damage, enemy-waves, round-currency, hunger-clock, turn-when-blocked, line-of-sight-attack, status-effects, spawner-entity, cell-transform, drop-on-death, difficulty-levels, mode-select, +nutrient-diffusion, +nutrient-conservation, +food-chain, +life-cycle-stages, +predator-prey, +egg-hatch-delay, +pupate-in-corridor, +mana-from-spells, +corpse-reanimate, +carry-off-loss, +relocate-core, +hero-avoids-new-tunnels, +torch-heal, +mutation-by-stress, +dungeon-quake]
proposes: ["+cond:nutrient", "+effect:absorb", "+effect:release_nutrients", "+effect:eat", "+card:nutrient-diffusion", "+card:food-chain"]
author: opus
date: 2026-11-09
---

# What Did I Do to Deserve This, My Lord? — копаєш підземелля, і з поживи в землі виростає екосистема, що зʼїсть героя

## Суть
Гравець — невидимий «Бог руйнування» з кайлом; він копає тунелі в розрізі землі, щоб захистити безпорадного демона-лорда Badman від героїв. Монстрів не купують: вони **народжуються з блоків**, у яких є пожива (養分) або мана (魔分), і далі живуть самі — їдять одне одного, розмножуються, перетворюються, помирають і повертають поживу в землю. Гравець не керує монстрами, а **садить екосистему** й підводить героїв до хижаків; герой, що схопив Badman і виніс його назовні, закінчує гру.

## Поле і час
- Поле — **вертикальний розріз** підземелля: квадратна сітка блоків ґрунту; прокопаний блок стає тунелем, яким ходять монстри й герої. Вхід для героїв — з поверхні (?).
- Кожен блок має рівень поживи й мани; текстура блоку показує, скільки там поживи. Пожива **збережена**: загальна кількість стала, вона лише переходить між блоками й тілами.
- Real-time: фаза підготовки до приходу героя → герой входить і йде підземеллям → бій. Монстри живуть власним циклом увесь час.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Badman (демон-лорд) | object | — | не бʼється, лише радить; гравець переносить його в схованку перед входом героя |
| Блок ґрунту | terrain | пожива, мана | копається кайлом; прокопаний із поживою/маною народжує монстра |
| Тунель | terrain | — | прохід для всіх; новий тунель герой, що вже увійшов, оминає |
| Мох (Nijirigoke, slimemoss) | ally | життєвість | з бідного ґрунту; повзе, бере й віддає поживу сусіднім блокам; повертає лише біля стіни |
| Бутон (Tsubomi) | ally | — | мох зі спадом життєвості; тягне поживу з ширшої зони |
| Квітка (Nijiribana) | ally | запас поживи | дозріває з бутона; липкий секрет сповільнює героїв; помирає й сіє нові мохи |
| Личинка (Gajigajimushi) | ally | пожива | з помірного ґрунту; їсть мох (не квіти); наситившись — заляльковується у вузькому коридорі |
| Муха (Gajifly) | ally | — | з лялечки; відкладає нові личинки |
| Ящір (Tokageotoko) | ally | сила | з багатого ґрунту; їсть личинок; помітивши героя — швидко атакує; несе яйця в гнізда |
| Яйце ящера | container | затримка вилуплення | вилуплюється з часом; герой може розбити |
| Елемент (Element) | ally | мана | мана-версія моху; ділиться, коли накопичив життєвість, і породжує нову ману |
| Ліліт (Lilith) | ally | мала міцність | з ґрунту з маною; їсть личинок, вбирає елементи; сильна дальня магія; швидко голодує; феромон знерухомлює героїв |
| Дракон | ally | найсильніший | з ґрунту, багатого на ману; ходить лише горизонтально; вогонь по лінії; їсть усіх поруч; помирає, лишивши яйце; послід приголомшує героя |
| Яйце дракона → Dofugon | container → ally | — | вилуплюється в Dofugon: швидший і слабший за дракона |
| Труп героя | object | мана | дотик кайлом → скелет; насичений маною (червоний) → слуга демон-лорда |
| Скелет | ally | сила від мани | без життєвості знову стає трупом; убитий героєм або кайлом — зникає назавжди |
| Слуга демон-лорда | ally | — | сильніший скелет, що не їсть |
| Магічне коло | spawner | запас мани | будується з багатого ґрунту; вбирає сусідні елементи; викликає Dee-mon; висмоктує MP героя на ньому |
| Dee-mon | ally | аура захисту | +захист усім монстрам; їсть скелетів і елементи, голодний — личинок і Ліліт |
| Скриня-монстри (золоті личинка й лялечка, Gajiseint, Sanpou Hone) | ally | міцні | зі скринь; ростуть повільно, не розмножуються |
| Герой: мечник / воїн / маг | enemy | HP, MP | йде підземеллям, бʼє монстрів на шляху, лікується й чаклує; групи можуть розділятись |
| Смолоскип | terrain | — | відновлює HP героя поруч |
| Dig Power | resource | — | обмежений запас на копання й апгрейд монстрів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dig, block)` → ЯКЩО `counter(dig_power, >=, 1)` → ТО `set_cell(block, tunnel)`, `counter(dig_power, -1)`.
- КОЛИ `input(dig, block)` → ЯКЩО `custom: «у блоці мало / середньо / багато поживи»` → ТО `spawn(moss)` / `spawn(larva)` / `spawn(lizardman)`.
- КОЛИ `input(dig, block)` → ЯКЩО `custom: «у блоці трохи / помірно / багато мани»` → ТО `spawn(element)` / `spawn(lilith)` / `spawn(dragon)`.
- КОЛИ `tick` → ТО `move(moss, dir)`, `custom: «absorb поживу з сусідніх блоків і release у них»`; КОЛИ `blocked(moss)` → ТО `face(moss, new_dir)`.
- КОЛИ `counter(moss_vitality, <=, n)` → ТО `transform(moss, bud)`; бутон дозрів → `transform(bud, flower)`.
- КОЛИ `died(flower)` → ТО `spawn(moss)` × `custom: «кількість — за накопиченою поживою»`.
- КОЛИ `in_range(flower, hero, n)` → ТО `set_state(hero, slowed)`.
- КОЛИ `contact(larva, moss)` → ТО `custom: «eat: здобич зникає, її пожива — хижаку»`; на квітку — `block`.
- КОЛИ `counter(larva_nutrients, >=, n)` → ЯКЩО `custom: «вузький коридор»` → ТО `transform(larva, pupa)`; згодом `transform(pupa, gajifly)`; КОЛИ `timer(every)` → ТО `spawn(larva)` біля мухи.
- КОЛИ `contact(lizardman, larva)` → ТО `custom: «eat»`.
- КОЛИ `line_of_sight(lizardman, hero)` → ТО `move(lizardman, toward_hero)`, `damage(hero, n)`.
- КОЛИ `enter(lizardman, nest)` → ЯКЩО `custom: «досить поживи»` → ТО `spawn(lizard_egg)`; КОЛИ `timer(hatch)` → ТО `transform(lizard_egg, lizardman)`; КОЛИ `contact(hero, lizard_egg)` → ТО `disappear_b`.
- КОЛИ `counter(element_vitality, >=, n)` → ТО `split(element)`, `custom: «нова мана в блоки поруч»`.
- КОЛИ `contact(lilith, larva|element)` → ТО `custom: «eat / absorb»`; КОЛИ `in_range(lilith, hero, n)` → ТО `spawn(magic_shot)`.
- КОЛИ `custom: «пожива Ліліт досягла порогу»` → ТО `stun(hero, n)` (феромон).
- КОЛИ `tick` → ТО `move(dragon, left|right)` — `custom: «лише горизонтально»`; КОЛИ `line_of_sight(dragon, hero)` → ТО `custom: «вогонь по лінії»`, `damage(hero, n)`.
- КОЛИ `adjacent(dragon, monster)` → ТО `custom: «eat будь-кого, і своїх»`.
- КОЛИ `rng(p)` → ТО `spawn(dung)` під драконом; КОЛИ `enter(hero, dung)` → ТО `stun(hero, n)`.
- КОЛИ `custom: «життєвість дракона вичерпано»` → ТО `transform(dragon, dragon_egg)`; згодом `transform(dragon_egg, dofugon)`.
- КОЛИ `tick` → ТО `counter(vitality, -1)` кожному монстру; голодний (нема їжі) — помирає швидше.
- КОЛИ `died(any)` → ТО `custom: «release: пожива тіла → у сусідні блоки; нема блоків поруч — пожива втрачена»`.
- КОЛИ `custom: «герой чаклує / застосовує навичку»` → ТО `custom: «мана → у блоки поруч»`; КОЛИ `died(hero)` → ТО `custom: «залишок мани героя → у блоки поруч»`.
- КОЛИ `input(tap, hero_corpse)` → ЯКЩО `state(corpse, mana_saturated)` → ТО `transform(corpse, demon_servant)`; інакше `transform(corpse, skeleton)`.
- КОЛИ `custom: «життєвість скелета вичерпано»` → ТО `transform(skeleton, corpse)`; КОЛИ `destroyed(skeleton)` → ТО `disappear(skeleton)` назавжди.
- КОЛИ `adjacent(magic_circle, element)` → ТО `custom: «коло вбирає елемент і запасає ману»`; запас досягнуто → `spawn(dee_mon)`.
- КОЛИ `enter(hero, magic_circle)` → ТО `custom: «коло втрачає ману, герой втрачає MP»`.
- КОЛИ `tick` → ЯКЩО `count(dee_mon, >=, 1)` → ТО `set_state(all_monsters, defense_up)`.
- КОЛИ `wave_start` → ТО `spawn_at(hero, entrance)`, `custom: «герой вносить поживу/ману»`.
- КОЛИ `contact(hero, monster)` → ТО `damage(monster, n)`, `damage(hero, n)`; КОЛИ `in_range(hero, torch, n)` → ТО `heal(hero, n)`.
- КОЛИ `custom: «тунель прокопано після входу героя»` → ТО `custom: «герой оминає новий тунель»`.
- КОЛИ `input(move_badman, cell)` → ЯКЩО `custom: «до входу героя»` → ТО `move(badman, cell)`.
- КОЛИ `contact(hero, badman)` → ТО `carry(hero, badman)`, `custom: «герой іде назад своїм шляхом»`.
- КОЛИ `reach(hero, entrance)` → ЯКЩО `custom: «герой несе Badman»` → ТО `lose`, `game_over` (підземелля з нуля).
- КОЛИ `all_gone(hero)` → ТО `custom: «етап пройдено»`, `counter(dig_power, +n)` за результатом.
- Перемога: відбити всіх героїв етапу · Поразка: Badman винесено з підземелля · Рахунок: нема; нагорода — Dig Power на наступний етап.

## Керування і ввід
- Курсор-кайло ходить по клітинах розрізу; дія — копати блок (і народити монстра) або торкнутись трупа (скелет).
- Окремо — перенести Badman у схованку перед приходом героя.
- Монстрів напряму не керують; Dig Power витрачається й на їхні апгрейди.

## Вікна, меню, HUD
- `game-screen`: розріз підземелля, `energy-bar`/лічильник Dig Power, Badman, монстри, герої з HP.
- `dialogue-window`: поради Badman і сюжетні сцени між етапами.
- `end-screen`: кінець етапу (Dig Power за результат) або game over.
- `main-menu`: сюжет (8 етапів в оригіналі), продовження.
- 3D: `mode-select` (Main · Daily · Family на двох через ad hoc), `difficulty-select` (3 рівні); Daily Dungeon і «Destruction God Test» — вікторина з оцінкою (`custom-window`).
- Переходи: `main-menu` → `dialogue-window` → `game-screen` (підготовка → вторгнення) → `end-screen` → наступний етап.

## Фічі поза полем
- `levels-sequential`: 8 сюжетних етапів; Dig Power переходить з етапу на етап за результатом.
- Завантажувані історії з лімітом часу (за JA-вікі).
- or2: `mode-sandbox`, режим «hero rush», коментарі в грі, прапорці збереження.
- 3D: `difficulty-presets`, `mode-daily`, `local-multiplayer` (Family), EX-етапи з додатковим Dig Power.

## Варіації й родичі
- **or2 (2008)**: Dungeon Quake (20 Dig Power, мутації, інколи заморожує героїв), пастки-приманки; нові монстри Golem (зелене коло) і Lady (синє коло, дальня атака); **мутації**: звичайна / аномальна (отрута, сон, швидке розмноження) / гігантська (канібалізм від голоду) / чиста / рідкісна; нові класи героїв Hunter (пастки) і Alchemist (викликає монстрів кола).
- **3D (2010; на Заході — No Heroes Allowed!)**: магічна вода з водяними монстрами, «інтелектуальна еволюція» через насіння лотоса, навички кайла за драконячі сфери (Hydroride, Navi Timer, Sleep, Dungeon Quake), мутація від «стресу» (смерті сусідів), класи Iron Warrior, Priest, Martial Artist, Shaman; 30 с на порятунок схопленого лорда.
- No Heroes Allowed: No Puzzles Either! (2014, Vita) — інший жанр; No Heroes Allowed! VR (2017).
- Родичі в корпусі: [dungeon-keeper](dungeon-keeper.md) (копаєш підземелля проти героїв), [creeper-world](creeper-world.md) (поле як рідина/поширення), [dungeon-warfare](dungeon-warfare.md); з build-sim — клітинні автомати й екосистеми.
- **Осі варіацій**: звідки беруться захисники — купуються / **виростають із ресурсу в клітині**; чи захисники керовані — так / **живуть власним циклом (голод, розмноження, хижацтво)**; ресурс — валюта / **збережена пожива, що циркулює полем**.

## Цікавинки для курсу
- Пожива в клітинах + повзун, що бере й віддає її сусідам (дифузія) — 🥈 (клітинне поле з потоком ресурсу).
- Харчовий ланцюг мох → личинка → ящір, де хижак забирає поживу здобичі — 🥈.
- Закон збереження поживи: смерть повертає її в сусідні блоки, без блоків — втрачено — 🥉.
- Життєві цикли (мох → бутон → квітка → нові мохи; личинка → лялечка → муха → личинки) як автомат станів — 🥉.
- Програш «ядро винесли»: герой несе Badman назад своїм шляхом, а гравець ще може відбити — 📎.
- Герой оминає тунелі, прокопані після входу (памʼять карти на момент входу) — 📎.

## Мапа на каталог
- Є: `dig-terrain` · `hp-damage` · `enemy-waves` · `round-currency` (Dig Power) · `hunger-clock` (життєвість) · `turn-when-blocked` (мох) · `line-of-sight-attack` (ящір, дракон) · `status-effects` (липкість, феромон, послід) · `spawner-entity` (магічне коло) · `cell-transform` (блок → тунель, труп → скелет) · `drop-on-death` (яйце дракона) · `difficulty-levels` · `mode-select` (3D).
- **Нема** → пропозиції карток:
  - `+nutrient-diffusion` «Ресурс у клітинах і його перенесення сутностями» · entities/state · 🥈 · слоти {field: nutrient|mana}.
  - `+food-chain` «Харчовий ланцюг: хто кого їсть» · entities/interact · 🥈 · слот {table: predator→prey}.
  - `+nutrient-conservation` «Ресурс не зникає, а переходить» · game-logic/economy · 🥉.
  - `+life-cycle-stages` «Стадії життя сутності» · entities/state · 🥉 (мох/личинка/дракон).
  - `+carry-off-loss` «Ворог виносить ядро — ще можна відбити» · game-logic/win · 📎.
  - `+corpse-reanimate`, `+egg-hatch-delay`, `+pupate-in-corridor`, `+mana-from-spells`, `+relocate-core`, `+hero-avoids-new-tunnels`, `+torch-heal`, `+mutation-by-stress`, `+dungeon-quake`, `+predator-prey` — 🌱–📎.

## Пропозиції до словників
- `+cond:nutrient(cell, op, n)` — рівень поживи/мани в клітині порівняно з N (який монстр народиться).
- `+effect:absorb(a, cell, n)` — сутність забирає ресурс із клітини.
- `+effect:release_nutrients(cells, n)` — ресурс розподіляється по сусідніх клітинах (смерть, віддача мохом).
- `+effect:eat(a, b)` — A поїдає B і забирає її ресурс (харчовий ланцюг; відрізняється від `disappear_b` передачею поживи).
- `+card:nutrient-diffusion` · `+card:food-chain` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia (EN)](https://en.wikipedia.org/wiki/What_Did_I_Do_to_Deserve_This,_My_Lord%3F) — Dig Power, підготовка й переховування Badman, захоплення й повернення героя, мох і пожива, мана від заклять, сиквели, релізи.
- [Wikipedia (JA): 勇者のくせになまいきだ。](https://ja.wikipedia.org/wiki/勇者のくせになまいきだ。) — уся екосистема й особливі монстри, класи героїв, умови програшу, відмінності or2 і 3D.
- YouTube: пошук «Holy Invasion of Privacy Badman gameplay».

## Непевне
- (?) Керування PSP (які кнопки копають / переносять Badman) — у джерелах нема.
- (?) Чи можна копати лише блок, суміжний із тунелем; ціни апгрейдів монстрів; пороги поживи для кожного монстра.
- (?) Англійські назви монстрів локалізації (Slimemoss, Omnom тощо) — тут JA-назви з вікі; «slimemoss» — з EN-вікі.
- (?) Вхід героїв згори — з памʼяті про вигляд гри; як саме «рік»/етап складається з кількох героїв — не уточнено.
