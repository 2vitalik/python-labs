---
title: Lock's Quest
slug: locks-quest
aka: [Lock's Quest Remastered, Construction Kingdom]
family: tower-lanes
also: []
klass: hybrid
axes:
  field: iso
  time: realtime
  opponent: none
  info: full
  random: none
  goal: survive
year: 2008
platforms: [Nintendo DS, PC, PS4, Xbox One, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lock%27s_Quest", best: true, note: "фази Build → Battle, Source, ворота, ремонт ratcheting, ціль-обʼєкт, таймер бою, Siege mode, versus"}
  - {kind: other, url: "https://www.cubed3.com/games/reviews/nintendo-ds/locks-quest-2", note: "рецензія: сітка, переставити/переробити в Build, хелпери-ремонтники, Source Wells, відлік до фінального штурму"}
  - {kind: steam, url: "https://store.steampowered.com/app/490080/Locks_Quest/", note: "ремастер 2017: 75 днів, турелі/пастки/хелпери, Special і Super атаки, Antonia Defense"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=lock%27s+quest+ds+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [tower-placement, tower-range, cursor-place, piece-rotate-flip, impassable-cells, destructible-blocks, enemy-waves, spawn-points, enemy-reached-base, round-currency, shop-buyback, hp-damage, melee-vs-ranged, move-by-input, restart-level, sequential-levels, level-unlock, mode-select, minimap-radar, +phase-cycle, +repair-structure, +wall-adjacency-bonus, +qte-action, +survive-timer, +gate-own-side, +send-units-versus]
proposes: ["+trigger:phase_end", "+trigger:attacked", "+effect:sell", "+effect:repair", "+role:base", "+ui:phase-timer", "+ui:source-counter", "+feature:local-versus", "+card:repair-structure", "+card:survive-timer"]
author: opus
date: 2026-11-09
---

# Lock's Quest — день за днем: за таймер збудуй стіни й турелі на ізометричній сітці, потім бийся і лагодь їх героєм

## Суть
Кожен «день» кампанії — дві фази. **Build**: за обмежений час і запас Source гравець ставить на ізометричну сітку стіни, ворота, турелі, гармати, машини, пастки й хелперів. **Battle**: годинникові вороги (Clockworks) виходять із країв мапи до цілі, а гравець керує героєм Lock — бʼється сам і **ремонтує** пошкоджені споруди міні-грою. Гібрид: курсорне будування (Rampart/TD) + аватарний бій (action RPG).

## Поле і час
- Ізометрична сітка мапи; споруди займають клітини; стіни — сегменти, що мають зʼєднуватися й «дивитися» правильно (поворот кнопкою L).
- DS: два екрани — нижній з ізометричним полем (дотик), верхній — загальна мапа з позиціями споруд і ворогів та час до кінця бою.
- Фаза Build — таймер; фаза Battle — відлік, наприкінці якого йде фінальний штурм; пережити відлік (або вбити боса) = перемога дня.
- Кампанія — 75 днів на дюжині мап (ремастер), між днями — сюжет.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Lock | player | HP, атаки | ходить полем (індиректно — тап по клітині), бʼє ворогів, ремонтує споруди |
| Ціль захисту (персонаж/обʼєкт) | static (`+role:base`) | HP | вороги йдуть до неї; знищено — програш дня (?) |
| Стіна | static | HP, напрямок сегмента | непрохідна для ворогів і Lock; вороги ламають на шляху |
| Ворота | gate | HP | свої проходять, вороги — ні |
| Турель / гармата | tower | дальність, шкода, HP | сама стріляє в ворогів у радіусі; стіни обабіч дають бонус захисту (?) |
| Пастка | hazard | одноразова на бій | спрацьовує при контакті; після бою зникає |
| Хелпер (машина) | ally | — | сам ремонтує/підсилює сусідні споруди |
| Source | resource | лічильник | платіж за будівництво; +за вбитих ворогів; бонус із Siege mode |
| Source Well | resource | — | джерело Source, яке часто треба втримати (?) |
| Clockwork-піхотинець | enemy | HP | іде від зони спавну до цілі, атакує споруди на шляху |
| Clockwork дальній / літаючий | enemy | — | різні типи (?) |
| Бос | boss | фази | на деяких мапах бій триває до його знищення |
| Зона спавну | spawner | край мапи | звідки виходять хвилі |
| Союзні Clockworks (versus) | ally | — | будуються в мультиплеєрі й відправляються на суперника |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(build)` → ТО `timer(start, t_build)`; нові турелі доступні з сюжетних точок (`unlock`).
- КОЛИ `input(place, structure, cell)` → ЯКЩО `free(cells)` and `counter(source, >=, cost)` → ТО `currency(-cost)`, `place(player, structure)`; інакше `block`.
- КОЛИ `input(rotate)` → ТО `rotate(wall_piece, 90)` (зʼєднання сегментів стіни).
- КОЛИ `input(recycle, structure)` у фазі Build → ТО `disappear(structure)`, `custom: «sell: повернення Source»` (?).
- КОЛИ `input(move, structure, cell)` у фазі Build → ЯКЩО `free(cell)` → ТО `move(structure, cell)`.
- КОЛИ `custom: «phase_end(build)»` або `timer(build_end)` → ТО `custom: «phase_start(battle)»`, `timer(start, t_battle)`.
- КОЛИ `schedule(waves)` → ТО `spawn_at(clockwork, spawn_zone)`; рух — `custom: «шлях до цілі; стіна на шляху — атакувати її»`.
- КОЛИ `adjacent(clockwork, structure)` → ТО `damage(structure, n)`; `hp_zero(structure)` → `disappear(structure)`.
- КОЛИ `in_range(turret, clockwork, n)` → ТО `spawn(projectile)` → `damage(n)`.
- КОЛИ `custom: «турель має стіни з обох боків»` → ТО `set_state(turret, reinforced)` (?).
- КОЛИ `contact(clockwork, trap)` → ТО `damage(n)`; `custom: «пастка живе лише один бій»`.
- КОЛИ `input(attack, clockwork)` → ЯКЩО `adjacent(player, clockwork)` → ТО `damage(n)`; `custom: «QTE-атака: успіх → додаткова шкода»`.
- КОЛИ `input(repair, structure)` → ЯКЩО `adjacent(player, structure)` and not `custom: «повністю знищена»` → ТО `custom: «ratcheting QTE: крутити стилусом → heal(structure)»`.
- КОЛИ `timer(every)` біля хелпера → ТО `heal(сусідня споруда, n)`.
- КОЛИ `died(clockwork)` → ТО `currency(+source)`.
- КОЛИ `reach(clockwork, target)` → ТО `damage(target, n)`; `hp_zero(target)` → `lose` (?).
- КОЛИ `timer(battle_end)` → ЯКЩО not `custom: «на мапі живий бос»` → ТО `win`, `next_level` (наступний день).
- КОЛИ `input(restart)` → ТО `restart` (без штрафу, будь-коли).
- Versus: КОЛИ `input(send, unit)` → ТО `spawn_at(clockwork, мапа суперника)` — кожен будує на своїй мапі й обирає, кого відправити супернику.
- Перемога: протриматися до кінця відліку бою / знищити боса · Поразка: ціль захисту знищена (?) · Рахунок: —.

## Керування і ввід
- DS: стилус на нижньому екрані — вибір споруди з меню і тап по клітині (Build), тап по клітині/ворогу/споруді (Battle: рух, атака, ремонт); кнопка L — поворот сегмента.
- Ремонт і спецатаки — QTE на дотику («ratcheting» — обертання стилусом).
- Ремастер: миша/клавіатура або геймпад; Special Attacks контекстні, Super Attacks — по площі.

## Вікна, меню, HUD
- `main-menu`: кампанія · Siege mode · мультиплеєр · Antonia Defense (ремастер) → `mode-select`.
- `game-screen` (нижній екран): ізометричне поле, `+ui:source-counter`, `+ui:phase-timer`, `tool-palette` з типами споруд і цінами, `hp-bar` Lock і споруд, `ghost-piece` сегмента під курсором.
- Верхній екран: `minimap` (уся мапа: споруди, вороги) + час до кінця бою.
- `dialogue-window` — сюжетні сцени між днями; `map-window` (?) — дні на мапі королівства.
- `end-screen` — день виграно / програно → рестарт.
- `pause-menu`: продовжити, рестарт бою.
- Переходи: dialogue → Build → Battle → end-screen → dialogue (наступний день).

## Фічі поза полем
- `levels-sequential`: 75 днів; `level-unlock` турелей за сюжетом.
- `restart-level` будь-коли без штрафу.
- Siege mode — окрема 2D side-scroll TD міні-гра, що дає бонус Source у кампанії.
- Antonia Defense (ремастер) — `mode-endless`: ставиш юніти Kingdom Force на новій мапі.
- `+feature:local-versus` (DS): кожен на своїй мапі, обирає хвилі для суперника.
- `achievements` (Steam-ремастер).

## Варіації й родичі
- Ремастер 2017 (PC/PS4/Xbox One), мобільний порт 2019.
- Родичі: [rampart](rampart.md) (фази будування й бою, стіни), [plants-vs-zombies](plants-vs-zombies.md) і [fieldrunners](fieldrunners.md) (TD-економіка), [pixeljunk-monsters](pixeljunk-monsters.md) і [orcs-must-die](orcs-must-die.md) (герой бʼється поруч із вежами), Dungeon Defenders, [they-are-billions](they-are-billions.md) (стіни-периметр), [legion-td](legion-td.md) (відправка ворогів супернику).
- **Осі варіацій**: фази — розділені Build/Battle / будування завжди · хто лагодить — ніхто / герой міні-грою / хелпер-споруди · сітка — квадрат / ізометрія · мета дня — пережити таймер / вбити боса / зберегти обʼєкт.

## Цікавинки для курсу
- Машина фаз Build → Battle з таймером кожної і своїм набором дозволених дій (переставити можна лише в Build) — 🥉.
- Ремонт: HP споруди, «повністю знищена не лагодиться», хелпер, що лікує сусідів за таймером — 📎.
- Бонус турелі від сусідніх стін (перевірка сусідства за напрямками) — 🌱.
- Вороги з ціллю: якщо стіна на шляху — атакувати стіну, інакше йти; без повного мейзингу — 🥈.
- Перемога за таймер виживання + бос як альтернативна умова — 📎.
- Versus «відправ ворогів супернику» з двома мапами — 🥈.

## Мапа на каталог
- Є: `tower-placement`, `tower-range`, `cursor-place` ↔ Build · `piece-rotate-flip` ↔ поворот сегмента стіни · `impassable-cells`, `destructible-blocks` ↔ стіни · `enemy-waves`, `spawn-points`, `enemy-reached-base` · `round-currency` ↔ Source · `shop-buyback` ↔ recycle · `hp-damage`, `melee-vs-ranged` · `move-by-input` ↔ Lock · `restart-level`, `sequential-levels`, `level-unlock`, `mode-select`, `minimap-radar` ↔ верхній екран.
- **Нема** → пропозиції карток:
  - `+phase-cycle` (з Rampart) — Build/Battle з таймерами.
  - `+repair-structure` «Ремонт споруди героєм або хелпером» · entities/state · 📎 · слоти {who, rate, destroyed_irreparable}.
  - `+wall-adjacency-bonus` «Бонус споруди від сусідніх стін» · entities/state · 🌱.
  - `+qte-action` «Дія через швидку міні-гру (QTE)» · interface/input · 📎.
  - `+survive-timer` «Перемога — протриматися до кінця відліку» · game-logic/win · 🌱.
  - `+gate-own-side` «Ворота: свої проходять, вороги — ні» · entities/legality · 🌱.
  - `+send-units-versus` «Відправити хвилю супернику» (з Legion TD) · game-logic/opponent · 🥉.

## Пропозиції до словників
- `+trigger:phase_end` — кінець фази (Build → Battle).
- `+trigger:attacked` — сутність отримала удар (тригер ремонту/хелпера).
- `+effect:sell` — рециклінг споруди з поверненням валюти.
- `+effect:repair` — відновити HP споруди (≠ `heal` живої сутності; повністю знищена — не можна).
- `+role:base` — ціль захисту з HP (роль `tower` уже є в 🔥-списку `roles.md`).
- `+ui:phase-timer` — таймер фази; `+ui:source-counter` — запас валюти будування.
- `+feature:local-versus` — локальний бій двох DS, кожен на своїй мапі.
- `+card:repair-structure`, `+card:survive-timer` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Lock's Quest](https://en.wikipedia.org/wiki/Lock%27s_Quest) — Build (обмежений час і ресурси; стіни, турелі, гармати, машини, пастки; ворота), Source за ворогів, Battle з QTE-атаками й ремонтом «ratcheting», ціль-обʼєкт, вороги з країв мапи атакують споруди на шляху, боси, два екрани, Siege mode, versus.
- [Cubed3: рецензія](https://www.cubed3.com/games/reviews/nintendo-ds/locks-quest-2) — сітка, переставити/рециклити в Build, рестарт без штрафу, пастки біля спавну, лишати прохід для Lock, хелпери ремонтують, Source Wells, відлік і фінальний штурм, versus із союзними Clockworks.
- [Steam: Lock's Quest](https://store.steampowered.com/app/490080/Locks_Quest/) — 75 днів, дюжина мап, турелі за сюжетом, Special/Super Attacks, Antonia Defense.
- YouTube: пошук «lock's quest ds gameplay».

## Непевне
- (?) Поворот сегментів кнопкою L, бонус турелі від стін і «пастки лише на один бій» — з підсумку пошуку, першоджерело не відкрито.
- (?) Точна умова поразки: знищення цілі захисту — так у більшості рівнів, але для «Source Well»-мап може бути інакше.
- (?) Типи Clockworks (дальні, літаючі, підривники) і їхні правила.
- (?) Тривалість фаз, ціни споруд, частка повернення при рециклі.
- (?) Чи мусить Lock стояти поруч, щоб будувати, чи ставить будь-де (тап по клітині).
