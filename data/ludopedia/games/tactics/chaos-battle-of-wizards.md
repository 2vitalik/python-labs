---
title: "Chaos: The Battle of Wizards (+ Chaos Reborn)"
slug: chaos-battle-of-wizards
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: both
  goal: state
year: 1985
platforms: [ZX Spectrum, "PC/Mac/Linux (Chaos Reborn, 2015)", "mobile (Chaos Reborn: Adventures, 2018)"]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Chaos:_The_Battle_of_Wizards", best: true, note: "2–8 магів, таємний вибір заклять, баланс закону/хаосу, шанс успіху, бій, Magic Wood, «останній живий маг»"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Chaos_Reborn", note: "Chaos Reborn: смерть мага = кінець армії, Realm Quest, спорядження, Duel Mode"}
  - {kind: official, url: "https://www.chaos-reborn.com/", note: "сайт Chaos Reborn: «тактика шахів + блеф і шанси покеру»"}
  - {kind: other, url: "https://www.kickstarter.com/projects/1206403106/chaos-reborn-from-the-creator-of-the-original-x-co", note: "Kickstarter Chaos Reborn — дизайн-нотатки Голлопа"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=chaos+reborn", note: "пошук"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=chaos+the+battle+of+wizards+zx+spectrum+gameplay", note: "пошук; геймплей Spectrum"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, move-8dir, melee-vs-ranged, projectile-shot, piece-capture, hot-seat, ai-opponent, difficulty-levels, impassable-cells, spawn-points, temporary-modes, inventory-items, game-screen, end-screen, +summon-creature, +cast-chance, +world-alignment, +illusion-disbelieve, +secret-spell-select, +engagement, +spreading-terrain, +corpse-raise, +mount-ride, +leader-death-lose, +subversion, +hit-chance, +line-of-sight-attack, +spell-once, +undead-immunity, +flying-move]
proposes: ["+cond:prob", "+cond:state", "+cond:line_of_sight", "+cond:alignment", "+effect:set_side", "+effect:spawn_at", "+effect:spread", "+effect:counter", "+effect:choose", "+trigger:phase_start", "+trigger:input", "+role:piece", "+role:hazard", "+role:container", "+window:spell-select", "+ui:cast-chance", "+axis:turn-structure"]
author: opus
date: 2026-11-02
---

# Chaos: The Battle of Wizards — маги кидають закляття з шансом успіху, кличуть істот і блефують ілюзіями

## Суть
До восьми чарівників на одному полі: кожен хід маг обирає одне закляття з випадкового набору — найчастіше виклик істоти поруч із собою — і воно спрацьовує з певним шансом. Шанс залежить від **світового балансу закону й хаосу**: що більше кидали законних заклять, то легше наступні законні. Будь-яку істоту можна викликати як **ілюзію** — вона приходить гарантовано, але суперник може витратити хід на «Disbelieve» і розвіяти її. Далі маги й армії ходять і бʼються; загибель мага прибирає всю його армію; переможець — останній живий маг.

## Поле і час
- Квадратна сітка (Spectrum: ~15×10 (?)), без місцевості на старті; місцевість зʼявляється закляттями (ліси, замки, стіни, вогонь, слиз).
- Хід раунду у три фази: **(1) таємний вибір** — кожен гравець по черзі обирає закляття (інші відвертаються); **(2) каст** — закляття розігруються в порядку гравців; **(3) рух** — кожен маг рухає себе й усіх своїх істот.
- Інформація прихована: невідомо, які закляття в руці в суперника і яка істота — ілюзія.
- Випадковість: набір заклять на старті, шанс касту, результат бою, поширення вогню/слизу.
- **Chaos Reborn** (2015): гексагональне поле з висотами (?), колода заклять замість фіксованого набору (?), той самий скелет правил.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Маг | piece (лідер) | combat, defence, move 1, manoeuvre, magic resistance, набір заклять | кастує одне закляття на раунд; загинув → уся його армія зникає |
| Наземна істота (Goblin, Orc, Lion, Ogre, Giant…) | piece | combat, defence, move, manoeuvre, MR | ходить по клітинах (8 напрямків), бʼє ворога рухом на нього |
| Літаюча істота (Eagle, Bat, Harpy, Gryphon, Dragon…) | piece | move = дальність польоту | перелітає через фігури в межах дальності |
| Стрілець (Centaur, Manticore, драконячий подих…) | piece | ranged combat, range | дальня атака при чистій лінії видимості |
| Нежить (Skeleton, Zombie, Ghost, Spectre, Wraith, Vampire) | piece | undead | бʼють її лише нежить або маг зі зброєю-закляттям |
| Скакун (Horse, Unicorn, Pegasus, Gryphon…) | piece / container | можна осідлати | маг сідає й рухається з дальністю скакуна |
| Ілюзія | piece | як справжня істота | ходить і бʼється як справжня; Disbelieve → зникає |
| Труп | object | — | лишається після смерті живої істоти; Raise Dead → нежить |
| Magic Wood | terrain | дерева | маг усередині захищений (?) і може отримати нове закляття |
| Shadow Wood | hazard | — | дерева атакують сусідні клітини |
| Magic Castle / Dark Citadel | container | — | ховає мага; щораунду може зникнути з шансом |
| Стіна | static | — | непрохідна перешкода, ставиться закляттям |
| Gooey Blob | hazard | шириться | розростається на сусідні клітини, поглинає істот (?) |
| Magic Fire | hazard | шириться | розповсюджується й спалює все, що накриває |
| Закляття-зброя (Magic Sword/Knife/Bow, Armour, Shield, Wings, Shadow Form) | pickup | постійне | бафи мага: атака, захист, політ, дальній постріл |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(select)` → ТО кожен гравець по черзі `choose(spell)` таємно; людина бачить шанс кожного закляття, AI обирає пізніше (?).
- КОЛИ `phase_start(cast)` → ТО для кожного мага: ЯКЩО `cond:prob(cast_chance(spell, world_alignment))` → ТО ефект; інакше `custom: «закляття не вдалось»`; закляття (крім Disbelieve) згоряє в будь-якому разі.
- КОЛИ закляття-виклик → ТО `custom: «Illusion? Y/N»`; ЯКЩО ілюзія → ТО `spawn_at(creature, cell_next_to_wizard)` без кидка (100 %); інакше кидок шансу.
- КОЛИ кинуто Disbelieve на істоту → ЯКЩО `state(target, illusion)` → ТО `disappear_b`; інакше нічого (хід втрачено).
- КОЛИ успішно кинуто законне/хаотичне закляття → ТО `counter(world_alignment, ±n)`; КОЛИ рахується шанс → ТО закляття того самого вирівнювання, що й світ, — легші; протилежного — не важчі; нейтральні — без змін.
- КОЛИ `phase_start(move)` → ТО маг гравця і всі його істоти ходять по черзі (кожна раз); людина може пропустити будь-яку дію; AI-істоти завжди рухаються, крім тих, хто в Magic Wood / Castle / Citadel.
- КОЛИ `input(move, creature, cell)` → ЯКЩО наземна → крок на сусідню (8 напрямків) до `move`; ЯКЩО літаюча → `custom: «переліт у межах дальності»`.
- КОЛИ `adjacent(creature, enemy)` → ТО `custom: «engaged»`: ЯКЩО `not cond:prob(manoeuvre)` → ТО істота мусить атакувати сусіда, а не відходити (?).
- КОЛИ `contact(attacker, defender)` (рух на клітину ворога) → ЯКЩО `cond:prob(combat(attacker) vs defence(defender))` → ТО `disappear_b`, атакувальник `move` на клітину; ЯКЩО `state(defender, undead)` і атакувальник не нежить без чарівної зброї → `block`.
- КОЛИ `input(ranged, creature, target)` → ЯКЩО `line_of_sight` and `in_range` → ТО кидок `ranged_combat vs defence` → `disappear_b`.
- КОЛИ жива істота загинула → ТО `transform(corpse)`; КОЛИ Raise Dead на труп → ТО `spawn(undead_copy)` під контролем мага.
- КОЛИ Subversion на ворожу істоту → ЯКЩО `cond:prob(1 - magic_resistance)` → ТО `set_side(target, caster)`.
- КОЛИ Lightning / Magic Bolt → ЯКЩО `line_of_sight` → ТО кидок проти magic resistance → `disappear_b`.
- КОЛИ `turn_end` → ТО Gooey Blob і Magic Fire `custom: «spread»` на випадкові сусідні клітини; замки й цитаделі зникають з шансом.
- КОЛИ маг стоїть у Magic Wood → ЯКЩО `cond:prob(p)` → ТО `give(wizard, random_spell)` — єдиний спосіб отримати нові закляття.
- КОЛИ `hp_zero(wizard)` (переможений у бою чи закляттям) → ТО `disappear_a` + всі його істоти й закляття на полі зникають.
- Перемога: останній живий маг · Нічия (?): ліміт раундів вичерпано — у Spectrum-версії гра може закінчитись без переможця.

## Керування і ввід
- Spectrum: клавіші-курсор (QAOP / 8 напрямків) рухають рамку по полі; клавіша вибору — обрати / підтвердити; цифри — пункти меню.
- Меню мага на фазі вибору: «Examine spells» (список з шансами), «Select spell», «Examine board», «Continue»; на будь-якій клітині можна «оглянути» істоту — її характеристики.
- Chaos Reborn: миша, підсвітка досяжних гексів, відсоток шансу при наведенні (?).

## Вікна, меню, HUD
- `main-menu` (Spectrum): кількість магів 2–8, для кожного — імʼя, людина/комп'ютер, рівень AI 1–8.
- `custom-window` «Spell list» — список заклять мага з вирівнюванням (^ закон / * хаос) і відсотком шансу; `ui:cast-chance`.
- `game-screen` — поле, рамка-курсор, рядок стану знизу (імʼя мага, фаза, результат «SPELL SUCCEEDS / FAILS»), позначка балансу світу (?).
- `custom-window` «Examine creature» — характеристики: combat, ranged combat/range, defence, movement, manoeuvre, magic resistance, вирівнювання, позначки undead / mount / flying.
- `end-screen` — «X is the winner».
- Chaos Reborn: `map-window` Realm Quest, `character-select`/спорядження, лобі онлайн (?).
- Переходи: main-menu → (раунд: вибір → каст → рух) game-screen ↔ Spell list / Examine → end-screen.

## Фічі поза полем
- `hotseat` до 8 людей (інші відвертаються, поки гравець обирає закляття) + `ai-opponent-levels` 1–8 (рівень змінює характеристики AI-мага, а не поведінку).
- Chaos Reborn: `online-multiplayer`, `meta-progression` (броня, посохи, талісмани → додаткові закляття), Realm Quest — `world-map` з захопленням інфраструктури й найманцями, Duel Mode з серіями перемог, щоденні талісмани.

## Варіації й родичі
- Lords of Chaos (1990) — сиквел з запасами мани й рюкзаками; Chaos Funk та інші фан-ремейки; Cyber Wars (Jagex) — SF-клон.
- Предок: настільна Warlock (Games Workshop) і картковий прототип Голлопа (1982); нащадки — Laser Squad / X-COM (той самий автор, інша лінія).
- **Осі варіацій**: шанс касту — фіксований / **залежить від стану світу** / прокачується маною · виклик — завжди справжній / **з опцією ілюзії** · джерело заклять — фіксований набір / колода / знахідки (Magic Wood) · армія після смерті лідера — лишається / **зникає**.

## Цікавинки для курсу
- Ілюзія vs Disbelieve: гарантований виклик, що може бути викритий, — 🥈 (прихований прапорець + ціна перевірки, блеф з AI).
- Глобальний баланс закону/хаосу, що змінює шанси всіх наступних заклять, — 🥉.
- Таємний вибір → каст по черзі → рух: трифазний раунд на N гравців — 🥉.
- Поширення вогню/слизу по сусідніх клітинах з шансом — 📎 (клітинний автомат).
- Смерть лідера знищує всю його армію — 🌱.
- Трупи → Raise Dead → нежить, імунна до звичайних атак, — 📎.
- Скакуни, на яких сідає маг (контейнер-фігура), — 📎.

## Мапа на каталог
- Є: `piece-move-patterns` (наземні / літаючі) · `move-8dir` · `melee-vs-ranged` · `projectile-shot` (дальні атаки, блискавка) · `piece-capture` (переможець займає клітину) · `hot-seat` · `ai-opponent` · `difficulty-levels` (рівень AI) · `impassable-cells` (стіни) · `spawn-points` (виклик біля мага) · `temporary-modes` (замки, що зникають) · `inventory-items` (закляття-зброя) · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+summon-creature` «Виклик істоти поруч із лідером» · entities/spawn · 📎.
  - `+cast-chance` «Шанс успіху дії» · entities/state · 📎 · слот {chance%} — родич `+hit-chance`.
  - `+world-alignment` «Глобальний баланс, що змінює шанси» · game-logic/economy · 🥉.
  - `+illusion-disbelieve` «Ілюзія і викриття» · entities/state · 🥈.
  - `+secret-spell-select` «Таємний вибір дії до розкриття» · game-logic/opponent · 📎.
  - `+engagement` «Зачеплення в ближньому бою» · entities/combat · 📎 · слот {escape: manoeuvre}.
  - `+spreading-terrain` «Місцевість, що шириться» · entities/interact · 📎 · слот {chance}.
  - `+corpse-raise` «Труп → нежить» · entities/spawn · 📎.
  - `+mount-ride` «Осідлати фігуру» · entities/interact · 🥉.
  - `+leader-death-lose` «Смерть лідера прибирає армію» · game-logic/lose · 🌱 (є в tactics).
  - `+subversion` «Переманити фігуру» · entities/state · 📎 (родич `set_side`).
  - `+hit-chance` · `+line-of-sight-attack` · `+spell-once` — наявні пропозиції корпусу.
  - `+undead-immunity` «Імунітет до звичайних атак» · entities/combat · 🌱.
  - `+flying-move` «Політ через фігури в межах дальності» · entities/legality · 🌱.

## Пропозиції до словників
- `+cond:prob` — шанс касту, бою, переманювання; `+cond:alignment` — вирівнювання закляття відносно світу.
- `+cond:state` (illusion, undead, engaged) · `+cond:line_of_sight`.
- `+effect:set_side` (Subversion) · `+effect:spawn_at` (виклик біля мага) · `+effect:counter` (баланс світу) · `+effect:choose` (таємний вибір).
- `+effect:spread` — сутність-місцевість поширюється на сусідню клітину (вогонь, слиз).
- `+trigger:phase_start` — фази вибору/касту/руху; `+trigger:input`.
- `+role:piece` · `+role:hazard` (вогонь, слиз, тіньовий ліс) · `+role:container` (замок, скакун).
- `+window:spell-select` — список заклять з шансами; `+ui:cast-chance` — відсоток успіху біля дії.
- `+axis:turn-structure` — `sequential` з таємним вибором (кроки «обрати таємно → розкрити по черзі»).

## Джерела
- ⭐ [Wikipedia: Chaos](https://en.wikipedia.org/wiki/Chaos:_The_Battle_of_Wizards) — 2–8 магів, фази раунду, шанси й вирівнювання, характеристики, Magic Wood, нащадки.
- [Wikipedia: Chaos Reborn](https://en.wikipedia.org/wiki/Chaos_Reborn) — правила ремейку, Realm Quest, спорядження, Duel Mode.
- [chaos-reborn.com](https://www.chaos-reborn.com/) — офіційний сайт ремейку.
- [Kickstarter Chaos Reborn](https://www.kickstarter.com/projects/1206403106/chaos-reborn-from-the-creator-of-the-original-x-co) — задум Голлопа.
- Steam: пошук «chaos reborn»; YouTube: пошук «chaos the battle of wizards zx spectrum gameplay».

## Непевне
- (?) Розмір поля Spectrum (15×10) і ліміт раундів — з памʼяті.
- (?) Механіка «engaged» (утримання поруч за manoeuvre) — з памʼяті; Wikipedia лише каже, що manoeuvre визначає вихід з бою.
- (?) Деталі Gooey Blob (поглинутий маг гине чи ні), захист у Magic Wood, імовірності зникнення замків — з памʼяті.
- (?) Перелік істот і заклять — з памʼяті, не з мануала.
- (?) Chaos Reborn: гекси з висотами, колода заклять, мана для підсилення шансу — у перевірених джерелах нема, з памʼяті.
- (?) WebSearch вичерпано; сторінка Spectrum Computing не завантажилась.
