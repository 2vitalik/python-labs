---
title: "Yu-Gi-Oh! Dungeon Dice Monsters"
slug: dungeon-dice-monsters
aka: [Dungeon Dice Monsters, DDM, Dungeondice Monsters, "遊☆戯☆王ダンジョンダイスモンスターズ"]
family: tactics
also: [board-digital]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: runtime
  goal: state
year: 2001
platforms: [GBA, board]
links:
  - {kind: other, url: "https://rulespal.com/yu-gi-oh-dungeon-dice-monsters/rulebook", best: true, note: "настільні правила: 6 гербів, ліміт 10, рівні кубиків, призов за 2+ гербами, будування підземелля, рух і бій за герби, Monster Lord 3 LP, Flying/Tunnel, предмети, базова й розширена гра"}
  - {kind: other, url: "https://obj.vassalengine.org/images/1/19/Dungeon_Dice_Monsters_Rules.pdf", note: "фанатський конспект (PDF): пул 15 кубиків, макс. 3 кубики 4-го рівня, «Dimension Dice» — розгортка кубика в підземелля, кольори класів, chain rule, тайбрейки"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dungeon_Dice_Monsters", note: "GBA-гра Konami: дати релізів 2001 / 2003, настільна адаптація 2002, перевидання 2025"}
  - {kind: other, url: "https://www.playin.gg/games/yu-gi-oh-dungeon-dice-monsters", note: "поле 13 × 19 клітин, 3 LP у Monster Lord"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Yu-Gi-Oh+Dungeon+Dice+Monsters+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [polyomino-placement, cursor-place, move-4dir, hp-damage, round-currency, inventory, hot-seat, ai-opponent, turn-enforcement, legal-move-highlight, reachable-highlight, +dice-unfold-path, +connected-placement, +walk-on-built-only, +dice-crest-economy, +crest-cap, +dice-pool-select, +match-summon-roll, +triple-summon-upgrade, +summon-creature, +move-then-attack, +defend-cost-reaction, +flying-only-vs-flying, +tunnel-pass-through, +fixed-lord-target, +leader-death-lose, +hidden-trap-item, +ability-timing-windows, +chain-lifo-stack, +tiebreak-chain, +basic-advanced-rules]
proposes: ["+effect:roll_dice", "+trigger:dice_face", "+trigger:attacked", "+effect:unfold(die, net, cell)", "+effect:defend(b)", "+cond:connected_to(piece, own_area)", "+cond:can_build(net)", "+role:crest", "+role:lord", "+ui:crest-counter", "+ui:dice-pool", "+window:dice-pool-editor", "+feature:chain-stack", "+axis:field:built-by-players", "+card:dice-unfold-path"]
author: opus
date: 2026-11-09
---

# Yu-Gi-Oh! Dungeon Dice Monsters — кубик призову розгортається на полі в шматок підземелля, і монстри ходять лише тим, що ви збудували

## Суть
Гра з манги/аніме Yu-Gi-Oh!: кожен гравець має пул кубиків-монстрів і нерухомого Повелителя (Monster Lord / Dungeon Master) з 3 життями. Щоходу кидаєш 3 кубики: грані-герби дають **ресурси** (рух, атака, захист, магія, пастка), а два однакові герби призову дозволяють **розгорнути один із кубиків на полі** — розгортка куба стає шматком шляху, на якому зʼявляється монстр. Поле спершу порожнє: обидва гравці **будують підземелля** назустріч одне одному, а ціль — дістатися до ворожого Повелителя й тричі його вдарити.

## Поле і час
- Поле — квадратна сітка; у GBA-версії **13 × 19 клітин**. Настільна версія: базова гра — менша частина поля, розширена — усе поле до найбільшої рамки.
- Повелитель стоїть у своєму слоті-домені (Domain) і **ніколи не рухається**.
- Клітини поля без підземелля непрохідні для монстрів: ходити можна лише по клітинах розгорнутих кубиків (своїх і чужих). Через «невдалу» форму підземелля монстри можуть узагалі не дістатися одне одного — на це є тайбрейк.
- Хід = кидок 3 кубиків → призов/будування → рух і бій за накопичені герби. Ходять по черзі.
- Інформація: монстри відкриті, предмети лежать лицем донизу до спрацювання. Випадковість — кидки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Повелитель (Monster Lord) | piece | 3 LP, ATK 10, DEF 0 | нерухомий; кожна вдала атака по ньому — −1 LP незалежно від сили; бʼє сусіднього монстра за 1 герб атаки; здібності на нього не діють |
| Монстр | piece | рівень 1–4, клас (колір кубика), ATK, DEF, HP, здібність і її ціна в гербах | 1 рух і 1 атака за хід; після атаки не рухається |
| Кубик монстра | object | рівень, колір: білий — Demon, синій — Warrior, жовтий — Undead, зелений — Beast, червоний — Dragon | 6 граней-гербів; після розгортання з пулу зникає |
| Кубик предмета | object | чорний | призивається як монстр, кладе предмет |
| Шматок підземелля | terrain | 6 клітин розгортки, позначка призову | шлях для руху; першим торкається домену, далі — свого підземелля |
| Порожня клітина поля | static | — | не підземелля: ходити не можна, сюди розгортають нові шматки |
| Домен | zone | слот Повелителя | точка старту будування |
| Предмет | hazard | лицем донизу | спрацьовує, коли будь-який монстр проходить або стає; лишається, якщо не сказано скинути |
| Герб Progress | resource | ≤10 | 1 = крок ортогонально (Flying — 2); лише свій хід |
| Герб Attack | resource | ≤10 | 1 = звичайна атака |
| Герб Defense | resource | ≤10 | 1 = захист від атаки; лише в хід суперника |
| Герб Magic | resource | ≤10 | магічні здібності, свій хід; ефект до кінця гри / смерті монстра |
| Герб Trap | resource | ≤10 | пастки в будь-який хід; ефект до кінця того ходу |
| Герб Summon | mark | рівень 1–4 | не накопичується; 2 однакові → призов |
| Маркер шкоди | mark | 1 = 10 шкоди | кладеться на картку монстра |
| Монстр Flying | piece | — | бʼють лише Flying або Повелитель; крок за 2 герби |
| Монстр Tunnel | piece | — | проходить крізь будь-яких монстрів (не зупиняючись на них); предмети при проході не діють |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `choose(3 кубики з пулу)`, `custom: «кинути їх — обовʼязково»`; розширена гра — `custom: «кинути всі три двічі, кубики між кидками не міняти»`.
- КОЛИ `custom: «випав герб Progress / Attack / Defense / Magic / Trap»` → ТО `counter(crest, +n)`; ЯКЩО `counter(crest, >, 10)` → ТО `custom: «надлишок не зберігається»`.
- КОЛИ `custom: «≥2 гербів призову одного рівня»` → ТО `choose(монстр або предмет цього рівня з пулу)` — призов обовʼязковий, якщо його можна збудувати; за хід — один призов.
- КОЛИ `custom: «3 однакові герби призову (розширена гра)»` → ТО `custom: «можна призвати монстра на рівень вище»`.
- КОЛИ `custom: «призов»` → ЯКЩО `custom: «розгортка влазить у межі поля, не накладається на інші шматки»` and `custom: «перша — торкається ребром домену, наступні — свого підземелля»` → ТО `place(player, dungeon_piece)`, `spawn_at(monster, summon_mark)`, `take(player, die)` — кубик із пулу назавжди; інакше `block` — призов не вдався.
- КОЛИ `input(move, m, cell)` → ЯКЩО `cell(cell, dungeon)` and `custom: «сусідня ортогонально»` and `counter(progress, >=, cost)` → ТО `move(m, dir)`, `counter(progress, -1)` (Flying — −2); діагоналі — `block`.
- КОЛИ `input(move, m, cell)` → ЯКЩО `occupied(cell, enemy_monster)` and `not state(m, tunnel)` → ТО `block`; крізь своїх — можна.
- КОЛИ `input(move, m)` → ЯКЩО `state(m, attacked_this_turn)` → ТО `block` — спершу рух, потім атака.
- КОЛИ `input(attack, a, b)` → ЯКЩО `adjacent(a, b)` (ортогонально) and `counter(attack, >=, 1)` and `not state(a, attacked_this_turn)` → ТО `counter(attack, -1)`, `set_state(a, attacked_this_turn)`.
- КОЛИ `input(attack, a, b)` → ЯКЩО `state(b, flying)` and `not state(a, flying)` → ТО `block`.
- КОЛИ `custom: «b атаковано»` → ЯКЩО `counter(defense, >=, 1)` and `custom: «власник обрав захист»` → ТО `counter(defense, -1)`, `damage(b, ATK(a) − DEF(b))` — відʼємна різниця атакувальника не ранить; інакше `damage(b, ATK(a))`.
- КОЛИ `hp_zero(b)` → ТО `disappear(b)`, `custom: «картку перевернуто»`.
- КОЛИ `input(attack, m, enemy_lord)` → ЯКЩО `adjacent(m, enemy_lord)` and `counter(attack, >=, 1)` → ТО `lives(-1)` супернику — завжди рівно одне LP.
- КОЛИ `input(attack, lord, m)` → ЯКЩО `adjacent(lord, m)` and `counter(attack, >=, 1)` → ТО `damage(m, 10)`; від атаки Повелителя монстр не захищається.
- КОЛИ `enter(m, item)` або `custom: «m проходить через предмет»` → ЯКЩО `custom: «не Tunnel-монстр, що лише проходить»` → ТО `reveal(item)`, `custom: «ефект предмета»`; ЯКЩО `custom: «одноразовий»` → ТО `disappear(item)`.
- КОЛИ `input(ability, m)` → ЯКЩО `custom: «вікно часу: Progress/Magic — свій хід; Attack/Defense — у бою; Trap — будь-який хід»` and `has(player, crests)` → ТО `custom: «ефект здібності»`, `counter(crest, -cost)`; на Повелителя здібності не діють.
- КОЛИ `custom: «на дію відповіли іншою здібністю (chain)»` → ТО `custom: «ланцюг розвʼязується з кінця — останній першим»`.
- КОЛИ `counter(lp(enemy_lord), ==, 0)` → ТО `win`; КОЛИ `custom: «обидва Повелителі втратили останнє LP одночасно»` → ТО `draw`.
- КОЛИ `custom: «монстри сторін не можуть дістатися одне одного»` → ТО `custom: «тайбрейк: більше LP → більше призвано монстрів (живі + знищені) → більше високорівневих»`; інакше `draw`.
- Перемога: Повелитель суперника 0 LP · Поразка: твій 0 LP · Рахунок: нема, лише тайбрейк.

## Керування і ввід
- Настільна: вибрати 3 кубики, кинути, перекласти герби на лічильник гербів, вибрати шматок-розгортку й прикласти до свого підземелля, поставити фігурку монстра на позначку, рухати фігурки, платити гербами.
- (GBA, цифрова версія) вибір 3 кубиків з пулу на екрані кидка; при призові — `cursor-place` розгортки на полі з поворотом форми (?) і підсвіткою легальних місць; курсор по монстру → `reachable-highlight` за наявними гербами Progress → атака сусіда; вікно відповіді суперника гербом захисту.

## Вікна, меню, HUD
- (GBA / цифрова версія) `main-menu` → `mode-select` (турнір проти AI, вільна дуель, гра по кабелю на двох (?)) → `+window:dice-pool-editor` (вибір кубиків у пул, макс. 3 кубики 4-го рівня) → `game-screen`.
- `game-screen`: поле з порожніми клітинами й шматками підземелля обох кольорів; `+ui:crest-counter` (5 гербів обох гравців, кожен ≤10); `lives` Повелителів (3 LP); `+ui:dice-pool` з позначкою розгорнутих; `+ui:dice-tray` з трьома гербами кидка; `stat-panel` монстра під курсором (рівень, ATK, DEF, HP, здібність).
- `custom-window` вибору розгортки й місця призову; `confirm-dialog` захисту; `end-screen` з переможцем.

## Фічі поза полем
- Пул кубиків: настільний стартовий набір — 12 кубиків і 6 монстрів (базова гра); фан-правила й розширена гра — пул 15, 10 монстрів/предметів, макс. 3 кубики 4-го рівня.
- Два рівні правил: базова гра (менше поле, 6 монстрів, без предметів) і розширена (усе поле, подвійний кидок, triple summoning, предмети, без дублікатів).
- GBA: одиночна гра проти AI й мультиплеєр; перевидання 2025 у *Yu-Gi-Oh! Early Days Collection*.

## Варіації й родичі
- Родичі в корпусі: [Faeria](faeria.md) (гравці будують саме поле землями), [Summoner Wars](summoner-wars.md) і [Duelyst](duelyst.md) (призов на сітці), [Blokus](../board-digital/blokus.md) і [Carcassonne](../board-digital/carcassonne.md) (викладання фігури, що торкається свого), [Dreamblade](dreamblade.md) (кубики дають очки призову).
- **Осі варіацій**:
  - **поле**: задане / **будується гравцями під час партії** (DDM, [Faeria](faeria.md), [Carcassonne](../board-digital/carcassonne.md));
  - **ресурс ходу**: мана / очки дій / **герби з граней кубиків з лімітом накопичення**;
  - **призов**: за ціну / **за збіг рівнів на кидку**;
  - **ціль**: знищити армію / утримати клітини / **нерухомий Повелитель з фіксованими 3 LP**;
  - **рух**: по будь-яких клітинах / **лише по збудованому шляху**.

## Цікавинки для курсу
- Розгортка куба як гексаміно: перевірка «влазить, не накладається, торкається свого» — 🥉 (polyomino + поворот + звʼязність).
- Монстри ходять лише по побудованих клітинах — поле як граф, що росте щоходу (BFS по підземеллю) — 📎.
- Економіка гербів: 5 накопичуваних ресурсів з лімітом 10 і грані призову, що не накопичуються — 🌱.
- Кубики різних рівнів з різною кількістю граней призову (4/3/2/1 з 6) — ризик vs користь — 🌱.
- Повелитель з LP, які знімаються по одному незалежно від сили атаки — 🌱.
- Вікна часу здібностей (свій хід / бій / будь-коли) і ланцюг відповідей LIFO — 🥈.
- Тайбрейк, коли підземелля не зʼєдналось (LP → призвано → рівні) — 🌱.

## Мапа на каталог
- Є: `polyomino-placement` ↔ розгортка кубика · `cursor-place` ↔ місце призову · `move-4dir` ↔ лише ортогонально · `hp-damage` ↔ HP монстрів · `round-currency` ↔ герби · `inventory` ↔ пул кубиків · `hot-seat`, `ai-opponent`, `turn-enforcement`, `legal-move-highlight`, `reachable-highlight`.
- **Нема** → пропозиції карток:
  - `+dice-unfold-path` «Кубик розгортається в шматок поля» · entities/legality · 🥉 · слот {nets, rotate}.
  - `+connected-placement` «Нова частина торкається своєї» · entities/legality · 🌱.
  - `+walk-on-built-only` «Ходити лише по збудованих клітинах» · entities/move · 🌱.
  - `+dice-crest-economy` «Грані кубиків як ресурси» · game-logic/economy · 📎 · слот {crests}; `+crest-cap` «ліміт 10 на тип» · 🌱.
  - `+dice-pool-select` «Вибір N кубиків з пулу на кидок» · game-logic/random · 🌱.
  - `+match-summon-roll` / `+triple-summon-upgrade` «Призов за збігом граней, 3 збіги — рівень +1» · entities/spawn · 🌱.
  - `+move-then-attack` · `+defend-cost-reaction` «захист коштує ресурс у чужий хід» · `+flying-only-vs-flying` · `+tunnel-pass-through` · `+fixed-lord-target` · `+leader-death-lose` · `+hidden-trap-item` · `+ability-timing-windows` · `+chain-lifo-stack` · `+tiebreak-chain` · `+basic-advanced-rules` · `+summon-creature`.

## Пропозиції до словників
- `+effect:roll_dice` — кинути вибрані кубики; `+trigger:dice_face` — випала грань-герб.
- `+trigger:attacked` — монстра атакують (вікно захисту).
- `+effect:unfold(die, net, cell)` — розгорнути кубик у шматок поля заданої форми в клітині.
- `+effect:defend(b)` — витратити ресурс на захист: шкода = ATK − DEF.
- `+cond:connected_to(piece, own_area)` — нова частина торкається ребром свого домену/підземелля; `connected` перевіряє звʼязність множини, а не дотик нової частини.
- `+cond:can_build(net)` — є легальне місце для розгортки (інакше призов не відбувається).
- `+role:crest` — ресурс-грань із власним лімітом; `+role:lord` — нерухома фігура-«король» з LP.
- `+ui:crest-counter` — лічильник гербів обох гравців; `+ui:dice-pool` — пул кубиків із позначкою використаних.
- `+window:dice-pool-editor` — складання пулу кубиків перед грою.
- `+feature:chain-stack` — ланцюг відповідей зі зворотним розвʼязанням.
- `+axis:field:built-by-players` — поле росте під час партії.
- `+card:dice-unfold-path` — розгортка куба як вхід у тему «поліоміно».

## Джерела
- ⭐ [RulesPal: Yu-Gi-Oh! Dungeon Dice Monsters rulebook](https://rulespal.com/yu-gi-oh-dungeon-dice-monsters/rulebook) — настільні правила: компоненти, 6 гербів і ліміт 10, грані кубиків за рівнем, призов і triple summoning, будування підземелля, рух/Flying/Tunnel, атака й захист, Monster Lord 3 LP, предмети, вікна часу здібностей, базова vs розширена гра.
- [Dungeon Dice Monsters Rules (PDF, VASSAL)](https://obj.vassalengine.org/images/1/19/Dungeon_Dice_Monsters_Rules.pdf) — «Dimension Dice», пул 15, кольори класів, chain rule, тайбрейки, «після атаки не рухається».
- [Wikipedia: Dungeon Dice Monsters](https://en.wikipedia.org/wiki/Dungeon_Dice_Monsters) — GBA-гра (Konami, Японія 21.03.2001, США 2003), настільна адаптація 2002, перевидання 2025.
- [playin.gg](https://www.playin.gg/games/yu-gi-oh-dungeon-dice-monsters) — поле 13 × 19.
- YouTube: пошук «Yu-Gi-Oh Dungeon Dice Monsters gameplay».

## Непевне
- (?) Форми розгорток: скільки з 11 сіток куба дозволено і чи можна повертати/віддзеркалювати — у джерелах не сказано; у настільній — фіксовані пластикові шматки (10 у стартовому наборі).
- (?) Режими й вікна GBA (турнір, вільна дуель, link) — не перевірено; GBA-правила можуть відрізнятися від настільних.
- (?) Дублікати: фан-PDF каже «без ліміту», RulesPal для розширеної гри — «без дублікатів».
- (?) Поріг знищення: RulesPal — «0 HP», фан-PDF — «шкода більша за HP».
- (?) Чи може Tunnel-монстр зупинитися на чужому — RulesPal: «проходить, але не ділить клітину».
