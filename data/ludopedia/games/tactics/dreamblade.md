---
title: Dreamblade
slug: dreamblade
aka: [Дрімблейд]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: territory
year: 2006
platforms: [board]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dreamblade", best: true, note: "поле 5×5, портали, ряд призову, ключові клітини 3×3 з очками 5/4/3 і 1/2/1, спільна клітина — нікому, 6 перемог у ходах, стати Power/Defense/Life, кубик з blade"}
  - {kind: other, url: "https://rulespal.com/dreamblade/rulebook", note: "правила: фази ходу, ініціатива = очки призову, ряд призову за стовпчиком, ліміт стеку, shift/strike, розподіл шкоди, disrupt/destroy, deathblow, conquest, warband 16"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dreamblade+miniatures+game", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, spawn-points, hp-damage, event-points, hot-seat, turn-enforcement, match-setup, codex-window, +key-cell-scoring, +contested-cell-null, +territory-capture, +spawn-row-column-rule, +initiative-spawn-points, +catch-up-spawn-bonus, +cell-stacking-limit, +mass-shift-or-strike, +cell-melee-pool, +combat-dice-symbols, +damage-allocation, +disrupt-vs-destroy, +deathblow, +blade-face-abilities, +round-win-track, +aspect-cost, +graveyard-resource, +warband-limit, +initiative-roll, +summon-creature]
proposes: ["+effect:roll_dice", "+trigger:round_end", "+trigger:round_start", "+cond:engaged(a)", "+cond:controls_column(side, col)", "+effect:allocate_damage", "+effect:summon", "+role:location", "+role:portal", "+ui:victory-track", "+ui:cell-score-overlay", "+ui:spawn-points", "+window:warband-builder", "+axis:turn-structure:phase-alternation", "+card:contested-cell-null"]
author: opus
date: 2026-11-09
---

# Dreamblade — дуель мініатюр на полі 5×5: тримай ключові клітини сам, бо спільна клітина не дає очок нікому

## Суть
Двоє гравців призивають істот-кошмарів на крихітне поле 5×5 і змагаються не за знищення, а за **присутність**: у кінці кожного ходу той, хто набрав більше очок за ключові клітини (де лише його істоти) і за знищених ворогів, виграє хід. Перший, хто виграє **6 ходів**, перемагає. Призов можливий у свій портал або в клітину ряду призову, лише якщо в тому самому **стовпчику** вже є твоя мініатюра — тож просування вперед відкриває нові точки входу. Усі твої істоти разом або рухаються, або бʼються: у кожній із двох фаз дії ти обираєш shift або strike для всієї армії.

## Поле і час
- Поле **5×5 = 25 клітин** (dreamscape). Портали — у протилежних кутах (правий нижній і лівий верхній). Задній ряд на своєму боці — **ряд призову** (spawn row).
- **Ключові клітини** — центральні 3×3. Кожен гравець має 6 клітин, що дають йому очки: три в ряду ключових клітин біля ряду призову суперника і три середні.
  - Ряд ключових клітин біля ряду призову гравця дає **супернику** 5, 4, 3 очки (5 — у кутку біля порталу цього гравця).
  - Середня клітина центрального ряду — 2 очки обом; дві інші клітини середнього ряду — по 1.
  - Якщо в клітині є істоти обох гравців — її не рахує ніхто.
- Стек: у клітині до 8 істот (по 4 на гравця) і одна локація; у портал призивати можна понад ліміт.
- Хід (turn): ініціатива → фаза призову першого, потім другого → дві фази дії першого → дві фази дії другого → фаза conquest (підрахунок). Рух — на 1 ортогональну клітину.
- Інформація повна: обидва бачать склад warband суперника. Випадковість — кубики ініціативи й атаки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Істота | piece | Power (кубики атаки), Defense (поріг disrupt), Life (поріг destroy), spawn cost, aspect cost, аспект (Valor · Fear · Madness · Passion; Anvilborn — без), здібності | рухається на 1 ортогонально, якщо не engaged; бʼється лише в своїй клітині |
| Локація | static | одна на клітину | мініатюра-місце з власним ефектом (?) |
| Портал | spawner | кут поля | призов завжди дозволений, ліміт стеку не діє |
| Клітина ряду призову | zone | задній ряд | призов, якщо в стовпчику є твоя мініатюра й у клітині не було твоїх істот на початку фази |
| Ключова клітина | zone | 5 / 4 / 3 або 1 / 2 / 1 очок | дає очки, якщо там лише твої істоти |
| Кубик атаки | object | 6 граней: 1, 2, 3 шкоди · 2 промахи · blade | сума — шкода; blade обовʼязково витрачається на blade-здібність, якщо можна |
| Кубик ініціативи | object | d6 | більший ходить першим; сума обох — очки призову |
| Цвинтар (graveyard) | supply | знищені й пожертвувані | рахується в aspect cost; ресурс для Raise / Reincarnate / Respawn |
| Резерв (warband) | supply | ≤16 мініатюр, ≤3 копії | звідси призивають |
| Трек перемог | resource | 1 крок за виграний хід | 6 кроків — перемога |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «початок ходу»` → ТО кожен `custom: «кидає d6 ініціативи»`; більший — перший; нічия — той, хто виграв більше ходів, далі перекид.
- КОЛИ `custom: «хтось викинув 1»` → ТО `custom: «обидва пропускають фазу призову»`.
- КОЛИ `phase_start(spawn)` → ТО `set_value(spawn_points, сума обох кубиків + 2 × свої мініатюри, знищені з минулої фази призову)`; невитрачені очки згорають.
- КОЛИ `input(spawn, m, cell)` → ЯКЩО `custom: «spawn cost + бракуючий aspect cost ≤ spawn_points»` and (`cell(cell, portal)` or (`cell(cell, spawn_row)` and `custom: «у стовпчику є твоя мініатюра»` and `custom: «на початку фази в клітині не було твоїх істот»`)) → ТО `place(player, m)`, `counter(spawn_points, -cost)`.
- КОЛИ `input(spawn, m, cell)` → ЯКЩО `count(own_creatures_in_cell, >=, 4)` and `not cell(cell, portal)` → ТО `block`.
- КОЛИ `custom: «aspect cost»` → ТО `custom: «кожен символ аспекту покривається мініатюрою того ж аспекту на полі або на цвинтарі; бракує — +1 очко призову за символ»`.
- КОЛИ `phase_start(action)` → ТО `choose(shift | strike)` — для **всіх** своїх істот разом; фаз дії дві на гравця.
- КОЛИ `custom: «обрано shift»` → ЯКЩО `not occupied(cell_of_a, enemy)` → ТО `move(a, orthogonal)` на 1 (необовʼязково); engaged — `block`.
- КОЛИ `custom: «обрано strike»` → ТО `custom: «по клітинах у довільному порядку: у кожній, де є вороги, твої істоти атакують разом (частину можна притримати)»`.
- КОЛИ `custom: «атака в клітині»` → ТО `custom: «кинути кубиків = сума Power атакувальників»`, `custom: «шкоду розподіляє атакувальник між місцевими ворогами»`.
- КОЛИ `custom: «на кубику blade»` → ЯКЩО `custom: «є blade-здібність»` → ТО `custom: «обовʼязково активувати (Crit 5 — +5 шкоди цього бою, Fumble, Payback, Advance…)»`.
- КОЛИ `custom: «кінець бою»` → ЯКЩО `counter(damage(b), >=, Life(b))` → ТО `disappear(b)` на цвинтар; ЯКЩО `counter(damage(b), >=, Defense(b))` → ТО `custom: «disrupt: атакувальник переставляє b у порожню клітину»`, нема порожньої — `disappear(b)`; обидва пороги — вибір атакувальника.
- КОЛИ `custom: «Defense або Life зменшено ефектом»` → ТО `custom: «не нижче 1»`.
- КОЛИ `destroyed(enemy)` → ЯКЩО `custom: «зараз фаза дії першого гравця»` → ТО `custom: «deathblow: знищена істота атакує раз перед цвинтарем»`.
- КОЛИ `input(ability, Warpstrike, b)` → ЯКЩО `custom: «b не місцевий»` → ТО `custom: «атака X-power по іншій клітині»`.
- КОЛИ `phase_start(conquest)` → ТО для кожної своєї ключової клітини: ЯКЩО `occupied(cell, own)` and `not occupied(cell, enemy)` → ТО `score(+cell_value)`; плюс `score(+1)` за кожну ворожу мініатюру, знищену цього ходу.
- КОЛИ `custom: «очки conquest порахувано»` → ЯКЩО `custom: «у тебе більше»` → ТО `counter(turns_won, +1)`; рівно — ніхто.
- КОЛИ `counter(turns_won, ==, 6)` → ТО `win`.
- Перемога: першим виграти 6 ходів · Поразка: суперник виграв 6 · Рахунок: у межах ходу — очки клітин + 1 за знищену ворожу мініатюру.

## Керування і ввід
- Настільна: гравець рахує очки призову, ставить мініатюри з резерву в портал або ряд призову, оголошує shift / strike, рухає фігури на 1 клітину, кидає кубики атаки й розподіляє шкоду.
- (цифрова версія) кнопки `shift` / `strike` на кожну з двох фаз; drag мініатюри з резерву на підсвічені клітини призову (`legal-move-highlight` з урахуванням стовпчика й стеку); у strike — вибір клітини бою, притримання окремих істот, розподіл шкоди слайдерами; вибір клітини для disrupt-нутої істоти.

## Вікна, меню, HUD
- (цифрова версія) `main-menu` → `+window:warband-builder` (16 мініатюр, ≤3 копії, аспекти) → `match-setup` → `game-screen`.
- `game-screen`: поле 5×5 з `+ui:cell-score-overlay` (очки ключових клітин для кожного гравця, сірі — спірні), стопки мініатюр у клітинах; `+ui:spawn-points` цієї фази; `+ui:victory-track` 0–6 обох; `turn-indicator` з поточною фазою; панель резерву й цвинтаря (`pocket`); `+ui:dice-tray` з blade-гранями.
- `codex-window` — карта мініатюри: стати, вартість, аспект, здібності; `end-screen` — переможець.

## Фічі поза полем
- Колекційна гра: мініатюри у бустерах, наборах; warband до 16 мініатюр з ≤3 копіями, видно супернику.
- Аспекти як «кольори» колоди: змішувати можна, але aspect cost зростає.
- Набори-розширення до *Night Fusion*; виробництво зупинено у 2007, пʼятий сет *Serrated Dawn* скасовано.

## Варіації й родичі
- Родичі в корпусі: [Summoner Wars](summoner-wars.md) (призов біля своєї споруди), [Duelyst](duelyst.md) (призов біля будь-якого свого юніта), [Faeria](faeria.md) (поле будують землями), [Neuroshima Hex](neuroshima-hex.md) (маленьке поле, бій фазами), [Memoir '44](memoir-44.md) (кубики з символами).
- Межа з `board-digital`: ціль — **контроль клітин**, як у territory-іграх; але дієслово «призвати й бити» — тактика.
- **Осі варіацій**:
  - **де призивати**: портал / ряд призову за контрольованим стовпчиком (Dreamblade) / поруч зі своєю спорудою ([Summoner Wars](summoner-wars.md)) / поруч із будь-яким своїм юнітом ([Duelyst](duelyst.md));
  - **спірна клітина**: ділиться / **не дає нікому** / дає більшості;
  - **хто діє за фазу**: одна фігура / **уся армія одним наказом shift або strike**;
  - **бій**: поодинці / **пул усіх у клітині з розподілом шкоди**;
  - **наслідок шкоди**: HP / **два пороги: відкинути (disrupt) або знищити**.

## Цікавинки для курсу
- Скоринг клітин з правилом «спільна клітина = 0» і переможцем ходу за більшістю — 🌱.
- Правило ряду призову «лише в стовпчику, де вже є твоя мініатюра» — 🌱 (перевірка стовпчика + стеку).
- Масовий наказ shift/strike на всю армію двічі за хід — 📎 (розвʼязання по клітинах у порядку гравця).
- Пул кубиків = сума Power у клітині + ручний розподіл шкоди між ворогами — 📎.
- Два пороги шкоди: Defense → disrupt з переставлянням у порожню клітину, Life → знищення — 📎.
- Очки призову = сума кубиків ініціативи + 2 за кожну свою втрату (catch-up) — 🌱.
- Best-of-turns: гра — серія міні-раундів до 6 перемог — 🌱.

## Мапа на каталог
- Є: `move-4dir` ↔ shift на 1 ортогонально · `spawn-points` ↔ портал і ряд призову · `hp-damage` ↔ Defense/Life · `event-points` ↔ +1 за знищену мініатюру · `hot-seat`, `turn-enforcement`, `match-setup`, `codex-window`.
- **Нема** → пропозиції карток:
  - `+key-cell-scoring` «Очки за утримання клітин» · game-logic/score · 🌱 · слот {cell_values}.
  - `+contested-cell-null` «Спірна клітина не рахується» · game-logic/score · 🌱.
  - `+territory-capture` (спільна з territory-іграми) · `+round-win-track` «Перемога за кількістю виграних раундів» · game-logic/win · 🌱 · слот {target: 6}.
  - `+spawn-row-column-rule` «Призов лише в стовпчик зі своєю фігурою» · entities/spawn · 🌱.
  - `+initiative-spawn-points` / `+catch-up-spawn-bonus` «Очки призову з кубиків + бонус за втрати» · game-logic/economy · 🌱.
  - `+cell-stacking-limit` «Ліміт фігур у клітині» · entities/legality · 🌱 · слот {per_side: 4, total: 8}.
  - `+mass-shift-or-strike` «Один наказ для всієї армії» · game-logic/opponent · 📎.
  - `+cell-melee-pool` + `+damage-allocation` «Пул клітини і розподіл шкоди» · entities/combat · 📎.
  - `+disrupt-vs-destroy` «Два пороги шкоди» · entities/combat · 📎.
  - `+deathblow` «Знищений бʼє у відповідь (лише у фазах першого)» · entities/combat · 🌱.
  - `+combat-dice-symbols` · `+blade-face-abilities` «грань-тригер здібності» · `+aspect-cost` · `+graveyard-resource` · `+warband-limit` · `+initiative-roll` · `+summon-creature`.

## Пропозиції до словників
- `+effect:roll_dice` — кинути кубики (ініціатива, атака).
- `+trigger:round_start` / `+trigger:round_end` — межі ходу з підрахунком (фаза conquest).
- `+cond:engaged(a)` — у клітині A є ворожа істота (блокує shift).
- `+cond:controls_column(side, col)` — у стовпчику є мініатюра сторони (умова призову).
- `+effect:allocate_damage` — гравець розподіляє суму шкоди між кількома цілями.
- `+effect:summon` — призов з резерву за вартість (відмінність від `place`: ціна й умови клітини).
- `+role:location` — мініатюра-місце в клітині; `+role:portal` — клітина-спавнер гравця з винятком зі стеку.
- `+ui:victory-track` — трек виграних ходів; `+ui:cell-score-overlay` — очки клітин для кожного гравця; `+ui:spawn-points` — бюджет призову фази.
- `+window:warband-builder` — складання армії з лімітами копій.
- `+axis:turn-structure:phase-alternation` — хід як фіксована послідовність фаз обох гравців.
- `+card:contested-cell-null` — «спільне не рахується» як окрема механіка скорингу.

## Джерела
- ⭐ [Wikipedia: Dreamblade](https://en.wikipedia.org/wiki/Dreamblade) — 5×5, портали в кутах, ряд призову за стовпчиком, ключові клітини 3×3 з цінами 5/4/3 і 1/2/1, спільна клітина — нікому, 6 victory points, Power/Defense/Life, кубик (1/2/3, 2 промахи, blade), аспекти, історія WotC 2006–2007.
- [RulesPal: Dreamblade rulebook](https://rulespal.com/dreamblade/rulebook) — фази ходу, ініціатива й очки призову, ліміт стеку 4/8, shift/strike, engaged і local, розподіл шкоди, disrupt/destroy, deathblow, conquest, warband 16 / 3 копії, цвинтар, перелік здібностей.
- YouTube: пошук «Dreamblade miniatures game».

## Непевне
- (?) Чи шкода накопичується між боями, чи скидається після кожного (правило «наприкінці бою» натякає на скидання) — не перевірено.
- (?) Ефекти локацій і як вони потрапляють у клітину — у прочитаних уривках не описано.
- (?) Max очок клітин за хід 16 (5+4+3+1+2+1) — моє обчислення з цін, у джерелах не сказано.
- (?) Межі «очки призову 4–12»: RulesPal наводить як діапазон суми, бо з одиницею призов пропускається.
- (?) Цифрової версії не знайшов; вікна — як «цифрова версія». Дизайнер (Jonathan Tweet) — лише з категорії Wikipedia.
