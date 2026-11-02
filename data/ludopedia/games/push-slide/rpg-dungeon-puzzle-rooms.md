---
title: RPG dungeon puzzle rooms (Pokémon, Zelda, Golden Sun, Lufia II)
slug: rpg-dungeon-puzzle-rooms
family: push-slide
also: [roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 1986
platforms: [NES, SNES, GB, GBC, GBA, DS, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lufia_II:_Rise_of_the_Sinistrals", best: true, note: "покрокові підземелля-пазли: монстри ходять лише коли ходиш ти; стріли/бомби/гак як інструменти"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Legend_of_Zelda:_Link%27s_Awakening", note: "предмети відкривають області; кольорове підземелля DX"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Golden_Sun", note: "Psynergy поза боєм: штовхати стовпи, заморожувати калюжі в стовпи"}
  - {kind: fandom, url: "https://zeldawiki.wiki/wiki/Block", note: "Zelda Wiki: блоки (з черги; сторінка закрита для бота, не прочитано)"}
  - {kind: other, url: "https://www.serebii.net/pokearth/johto/icepath.shtml", note: "Serebii: Ice Path — багаторівнева печера з льодовими пазлами"}
  - {kind: other, url: "https://www.serebii.net/attackdex-dp/strength.shtml", note: "Serebii: Strength — рухати валуни поза боєм"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pokemon+ice+path+puzzle", note: "пошук; льодові пазли Pokémon"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pokemon+strength+boulder+puzzle", note: "пошук; валуни Strength"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lufia+2+puzzle+room", note: "пошук; кімнати-пазли Lufia II"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Game+Maker%27s+Toolkit+Boss+Keys+Link%27s+Awakening", note: "пошук; GMTK Boss Keys — структура данжів Zelda"}
stage: v1
coverage: 65
mechanics: [move-4dir, keyboard-controls, push-object, inertia-slide, floor-types, impassable-cells, key-and-door, inventory-items, item-pickup, cell-transform, reach-exit, destroy-all-enemies, dungeon-generation, player-camera, checkpoint, save-game, +room-memory, +reset-zone, +fill-hole, +button-toggle, +hold-all-switches, +crumbling-floor, +one-way-cell, +ability-gating, +toggle-light-goal, +push-once-block, +remote-push, +strength-gate, +crystal-switch, +shutter-door, +turn-based-dungeon, +freeze-into-pillar]
proposes: ["+trigger:input", "+trigger:enter", "+trigger:leave_room", "+trigger:all_on", "+trigger:all_gone", "+cond:has", "+cond:free", "+cond:state", "+effect:slide", "+effect:move", "+effect:set_cell", "+effect:set_state", "+effect:fall", "+effect:unlock", "+effect:restart", "+role:terrain", "+role:switch", "+role:gate", "+role:hazard", "+window:inventory-window", "+window:map-window", "+window:dialogue-window", "+ui:inventory-bar", "+feature:room-reset", "+axis:session"]
author: opus
date: 2026-11-02
---

# RPG dungeon puzzle rooms — кімнати-головоломки всередині пригодницької RPG

## Суть
Парасолька над «кімнатами-пазлами», вбудованими в RPG/action-adventure з аватаром: гравець іде світом, а прохід далі закриває кімната з одним клітинним правилом — **лід**, **валун**, **плита-перемикач**, **кристал**, **смолоскипи**. Ядро — ті самі механіки, що в Sokoban чи Inertia, але дозовані по одній-дві на кімнату, підвʼязані до прогресії (здібність/предмет відкриває правило) і з **м'якою поразкою**: вийшов з кімнати — вона скинулась. Для курсу це «набір клітинних правил як модулі»: кожна кімната — маленький рівень з власною `interaction-table`.

## Поле і час
- Світ — сітка тайлів 16×16 px; кімната = екран (Zelda GB, Pokémon) або прокручувана карта (Golden Sun, Lufia II). Камера за гравцем, у Zelda — перемикання екранами.
- Pokémon: аватар ходить строго по клітинах (покроково, але в реальному часі); Zelda: рух вільний по пікселях, але блоки зсуваються рівно на клітину; Lufia II: **покроково** — монстри ходять лише коли ходить гравець.
- Шари: підлога (лід, тріснутий лід, стрілки-обертачі, плита, дірка) + обʼєкти (блок, валун, смолоскип, кристал) + межі кімнати.
- Кілька поверхів: дірка/тріснутий лід скидає на нижній поверх (Pokémon), валун у дірці — з'являється знизу (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Аватар (Червоний/Голд, Лінк, Isaac, Maxim) | player | інвентар, бейджі/HM | рух 4 напрямки; штовхає впираючись; використовує предмет/здібність |
| Лід (Pokémon) | terrain | — | ступив → ковзає в напрямку руху до перешкоди; на льоду не повернути |
| Тріснутий лід (Pokémon, гімнастика Sootopolis (?)) | terrain | цілий → тріснутий → дірка | 1-й крок тріскає, 2-й — падіння поверхом нижче; усі тріснуті — прохід (?) |
| Стрілка-обертач (Pokémon, Rocket Hideout / Viridian Gym (?)) | terrain | напрям | тягне аватара в напрямку до стоп-клітини |
| Валун Strength (Pokémon) | object | — | лише після Strength (HM + бейдж); штовхається на 1; не тягнеться; не в інший валун/стіну |
| Дірка в підлозі (Pokémon, Seafoam (?)) | terrain | — | валун провалюється → поверх нижче, отвір закрито / течія змінюється (?) |
| Кнопка під валун (Pokémon Victory Road (?)) | switch | постійна | валун на ній → барʼєр зникає назавжди |
| Блок (Zelda) | object | раз / завжди; напрям (?) | штовхається на 1, якщо за ним вільно; часто — лише один раз за візит |
| Плита-перемикач (Zelda) | switch | тримати / одноразово | наступити або поставити блок → двері/міст/скриня |
| Кристал-перемикач (Zelda) | switch | 2 стани кольору | удар мечем/снарядом → перемкнути піднятий колір барʼєрних блоків |
| Барʼєрні блоки двох кольорів | gate | колір, піднятий / опущений | непрохідні, доки свого кольору підняті |
| Смолоскип (Zelda) | switch | горить / ні | запалити (порошок, вогняний жезл, Ember Seed) → усі запалені = двері (?) |
| Двері-затвор (shutter) | gate | умова | закрито, доки не: убиті всі вороги / розвʼязано пазл / натиснута плита |
| Двері з замком + малий ключ | gate / pickup | — | ключ витрачається на двері |
| Тріснута стіна | static | — | бомба → прохід |
| Кольорові плитки (Oracle of Ages (?)) | terrain | цикл кольорів | наступив → колір змінюється; ціль — узор/один колір (?) |
| Стовп (Golden Sun) | object | — | Move-Psynergy штовхає здалеку; стовпи будують шлях між висотами |
| Калюжа (Golden Sun) | terrain | — | Frost → крижаний стовп (новий обʼєкт-сходинка) |
| Монстр на карті (Lufia II) | enemy | — | ходить лише коли гравець ходить; стріла/бомба/гак — оглушають його і діють на перешкоди |
| Межа кімнати | static | — | вихід → кімната скидається до початку (Zelda, Pokémon валуни (?)) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `enter(player, ice)` → ТО `slide(player, dir)` до `blocked(player)`; ввід під час ковзання ігнорується.
- КОЛИ `enter(player, cracked_ice)` → ЯКЩО `state(tile, cracked)` → ТО `fall(player)` → поверх нижче; інакше `set_state(tile, cracked)`.
- КОЛИ `enter(player, spinner(d))` → ТО `custom: «рух у напрямку d до стоп-клітини»` (`slide` з примусовим напрямком).
- КОЛИ `contact(player, boulder)` → ЯКЩО `has(player, strength_active)` and `free(cell_behind)` → ТО `push`; інакше `block` (+ `message`: «Тут великий валун…» без Strength).
- КОЛИ `enter(boulder, hole)` → ТО `disappear_a`, `set_cell(floor)` (засипано) або `spawn(boulder)` на нижньому поверсі (?).
- КОЛИ `enter(boulder, boulder_switch)` → ТО `set_state(barrier, open)` назавжди.
- КОЛИ `contact(player, block)` (Zelda, утримання ~пів секунди (?)) → ЯКЩО `free(cell_behind)` and `not state(block, used)` → ТО `push`, `set_state(block, used)` (для блоків «раз»).
- КОЛИ `enter(player|block, floor_switch)` → ТО `set_state(target, open)`; для «тримати»-плит — `leave` → `set_state(target, closed)`.
- КОЛИ `all_on(block, floor_switch)` → ТО `unlock(door)` (кімнати з кількома плитами).
- КОЛИ `contact(attack, crystal_switch)` → ТО `set_state(barriers[colorA], lowered)`, `set_state(barriers[colorB], raised)`.
- КОЛИ `contact(fire, torch)` → ТО `set_state(torch, lit)`; КОЛИ `all_on(torch, lit)` → ТО `unlock(shutter)`; деякі гаснуть через N с (`timer`) (?).
- КОЛИ `all_gone(enemy)` → ТО `unlock(shutter)` (кімнати-арени).
- КОЛИ `contact(player, locked_door)` → ЯКЩО `has(player, small_key)` → ТО `disappear_b`, `take(small_key)`.
- КОЛИ `contact(bomb_blast, cracked_wall)` → ТО `set_cell(passage)`.
- КОЛИ `input(psynergy_move, pillar)` (Golden Sun) → ЯКЩО `free(cell_behind)` → ТО `push` здалеку; КОЛИ `input(frost, puddle)` → ТО `transform(puddle → ice_pillar)`.
- Lufia II: КОЛИ `input(dir)` → ТО `move(player)`, потім `custom: «кожен монстр робить свій крок»`; КОЛИ `contact(arrow|bomb|hook, monster)` → ТО `stun(monster, n)`.
- КОЛИ `custom: «гравець вийшов з кімнати»` → ТО `restart` кімнати: блоки на старт, плити віджато (Zelda); валуни Strength — на старт при виході з локації (?).
- Перемога: прохід/скриня/двері відкрито. · Поразка: формально нема — глухий кут лікується виходом з кімнати; падіння крізь лід — переміщення поверхом нижче. · Рахунок: нема (ресурси RPG — окремо).

## Керування і ввід
- D-pad — рух; впиратися в блок/валун — поштовх (Pokémon — вибрати Strength з меню покемона один раз, далі штовхати; Zelda — тиснути в блок деякий час).
- Кнопка дії / предмета: меч (кристал), порошок/жезл/насіння (смолоскипи), бомба, гак, стріли; Golden Sun — меню Psynergy з вибором цілі напрямком погляду.
- Zelda GB: два слоти предметів на A/B, що дозволяє комбінувати інструменти в пазлах.
- Lufia II: кожен крок — тік світу, тож можна «думати» без тиску часу.

## Вікна, меню, HUD
- `game-screen`: кімната; HUD Zelda — серця, рупії, ключі, слоти A/B (`inventory-bar`); Pokémon — без HUD, повідомлення внизу (`dialogue-window`).
- `inventory-window` (Zelda subscreen, Pokémon Bag/Party) — вибір предмета/HM.
- `map-window` — карта підземелля з позначкою кімнат (Zelda: після знаходження мапи; компас — скрині/бос).
- `dialogue-window` — «Великий валун. Можна посунути, якщо…» / «Він не зрушує».
- `pause-menu` + `save-slots` / `save-game` (Pokémon «Save», Zelda save & quit).
- Переходи: світ → (вхід) підземелля → кімната; кімната → (вихід за межу) сусідня кімната + скидання попередньої.

## Фічі поза полем
- `ability-gating` — нова здібність (Strength, Surf, Psynergy, предмет данжу) відкриває старі кімнати; Metroid-подібна прогресія.
- `room-reset` — скидання кімнати при виході замість undo; деякі пазли «запамʼятовують» розвʼязання (відкриті двері лишаються).
- `save-game`, `checkpoint` (вхід у данж).
- Lufia II: **Ancient Cave** — 99 поверхів, згенерованих заново при кожному вході, персонажі з нуля (`dungeon-generation`).
- `tutorial`/`onboarding-hints` — NPC або табличка перед першою кімнатою з новим правилом.

## Варіації й родичі
- Правила-модулі, що повторюються: **лід** (Pokémon G/S Ice Path і Mahogany Gym, пізніші ігри) · **валун без тягнення** (Strength з Gen I) · **блок на плиту** (Zelda з NES) · **кристал/два кольори барʼєрів** (Zelda) · **смолоскипи** · **стовпи й калюжі** (Golden Sun) · **покрокові монстри як рухомі перешкоди** (Lufia II).
- Окремі ігри корпусу на ці правила: [ice-sliding-puzzles](ice-sliding-puzzles.md) (лід як ціла гра), [sokoban](sokoban.md) (валуни як ціла гра), [adventures-of-lolo](adventures-of-lolo.md) (кімната-пазл як рівень), [chips-challenge](../maze-arcade/chips-challenge.md) (кнопки → цілі, лід, вода).
- Осі варіацій:
  - **поразка в кімнаті**: нема (вихід скидає) / падіння поверхом нижче / шкода від монстрів;
  - **хто штовхає**: аватар впритул / здалеку здібністю (Golden Sun Move) / снаряд;
  - **памʼять кімнати**: скидається при виході / розвʼязок постійний / пазл «раз і назавжди» (кнопка Victory Road);
  - **час**: real-time (Zelda) / покроково-real-time сітка (Pokémon) / покроково з монстрами (Lufia II).

## Цікавинки для курсу
- Кімната як окремий міні-рівень з власним набором правил + скидання при виході — 🥉 (`+room-memory`).
- Лід «ковзай до упору» + тріснутий лід з падінням на поверх нижче (два рівні карти) — 📎 / 🥉 з поверхами.
- Strength-валун: штовхання, дозволене предметом/здібністю + засипання дірки — 📎.
- Кристал-перемикач і два кольори барʼєрів (глобальний стан на кімнату) — 📎.
- Затвор «відкрити, коли всі вороги / усі плити / усі смолоскипи» — одна механіка з трьома умовами — 🥉.
- Покрокові монстри, що ходять тільки з гравцем (Lufia II) — 🥉; генерація 99-поверхового данжу — 🥇 (`dungeon-generation`).
- Стовп із калюжі (Frost) — ситуативна сутність, створена здібністю — 📎.

## Мапа на каталог
- Є: `move-4dir` ↔ рух; `push-object` ↔ блоки/валуни; `inertia-slide` + `floor-types` ↔ лід, обертачі; `impassable-cells` ↔ стіни, барʼєри; `key-and-door` ↔ малі ключі; `inventory-items` + `item-pickup` ↔ предмети/HM; `cell-transform` ↔ калюжа → стовп, валун → засипана дірка; `reach-exit` ↔ прохід; `destroy-all-enemies` ↔ кімнати-арени; `dungeon-generation` ↔ Ancient Cave; `player-camera` ↔ екран/прокрутка; `checkpoint` + `save-game`.
- **Нема** → пропозиції карток:
  - `+push-once-block` «Блок, що зсувається лише раз» · entities/legality · 🌱 · слот {times, dirs}.
  - `+remote-push` «Штовхання здалеку здібністю» · entities/interact · 📎 — Golden Sun Move.
  - `+strength-gate` «Штовхання лише з дозволом» · entities/legality · 🌱 — валун + HM (родич `+permit-item`).
  - `+crystal-switch` «Кристал перемикає два кольори барʼєрів» · entities/interact · 📎 (дитина `+button-toggle`).
  - `+shutter-door` «Двері відкриваються умовою кімнати» · game-logic/win · 🥉 · слот {cond: enemies|switches|torches}.
  - `+turn-based-dungeon` «Монстри ходять лише разом з гравцем» · entities/move · 🥉.
  - `+freeze-into-pillar` «Здібність робить з клітини обʼєкт» · entities/interact · 📎 — Frost: калюжа → стовп.
  - Повтор корпусу: `+room-memory`, `+reset-zone`, `+fill-hole`, `+button-toggle`, `+hold-all-switches`, `+crumbling-floor` (тріснутий лід), `+one-way-cell` (обертачі), `+ability-gating`, `+toggle-light-goal` (смолоскипи).

## Пропозиції до словників
- `+trigger:leave_room` — вихід з кімнати (скидання стану); `+trigger:all_on` (плити/смолоскипи), `+trigger:all_gone` (вороги).
- `+cond:has` (HM/бейдж/предмет), `+cond:state` (тріснуто, використано, колір піднятий).
- `+effect:slide`, `+effect:fall` (на нижній поверх), `+effect:set_cell`, `+effect:set_state`, `+effect:unlock`, `+effect:restart` (кімнати).
- `+role:switch` (плита, кристал, смолоскип), `+role:gate` (затвор, барʼєр), `+role:terrain` (лід, обертач), `+role:hazard` (тріснутий лід).
- `+window:inventory-window`, `+window:map-window`, `+window:dialogue-window`; `+ui:inventory-bar` (слоти A/B).
- `+feature:room-reset` — скидання кімнати як заміна undo.
- `+axis:session` — тут `room` усередині відкритого світу, не `level`.

## Джерела
- ⭐ [Wikipedia: Lufia II](https://en.wikipedia.org/wiki/Lufia_II:_Rise_of_the_Sinistrals) — «підземелля наголошують на пазлах», покроковий рух з монстрами, інструменти, Ancient Cave з 99 поверхів.
- [Wikipedia: Link's Awakening](https://en.wikipedia.org/wiki/The_Legend_of_Zelda:_Link%27s_Awakening) — предмети відкривають області, A/B-слоти для комбінацій, Color Dungeon у DX.
- [Wikipedia: Golden Sun](https://en.wikipedia.org/wiki/Golden_Sun) — Psynergy для пазлів, штовхання стовпів, крижані стовпи з калюж.
- [Serebii: Ice Path](https://www.serebii.net/pokearth/johto/icepath.shtml) — багатоповерхова печера з льодовими пазлами.
- [Serebii: Strength](https://www.serebii.net/attackdex-dp/strength.shtml) — «також рухає валуни».
- [Zelda Wiki: Block](https://zeldawiki.wiki/wiki/Block) — з черги куратора; не прочитано (403).
- YouTube: пошуки «Pokemon ice path puzzle», «Pokemon strength boulder puzzle», «Lufia 2 puzzle room», GMTK Boss Keys.

## Непевне
- (?) Bulbapedia, Zelda Wiki, Pokémon Fandom закриті для бота; WebSearch вичерпано — деталі Pokémon/Zelda описано з памʼяті.
- (?) Тріснутий лід Sootopolis Gym (крок → тріщина → падіння; усі тріснуті відкривають сходи), обертачі Rocket Hideout/Viridian Gym, валуни в дірки Seafoam, кнопки Victory Road — з памʼяті.
- (?) Скидання валунів Strength при виході з локації і точна поведінка «блок штовхається лише раз» у LA/Oracle.
- (?) Кольорові плитки Oracle of Ages і правило смолоскипів з таймером — у яких саме іграх.
- (?) Рік 1986 — перші блоки-на-двері в The Legend of Zelda (NES); для Link's Awakening — 1993, Pokémon R/G — 1996.
