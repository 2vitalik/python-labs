---
title: IVAN (Iter Vehemens ad Necem)
slug: ivan
aka: [Iter Vehemens ad Necem, Violent Road to Death, IVAN3D]
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
year: 2001
platforms: [Windows, Linux, macOS, DOS, Steam (2026)]
links:
  - {kind: other, url: "https://www.roguebasin.com/index.php/IVAN", best: true, note: "RogueBasin: частини тіла, відрубування й приєднання кінцівок, матеріали й Scroll of Change Material, 15 богів, найманці, історія версій"}
  - {kind: steam, url: "https://store.steampowered.com/app/4890840/IVAN_Iter_Vehemens_ad_Necem/", note: "безкоштовне Steam-видання 2026 (Zeno Rogue), з IVAN3D"}
  - {kind: other, url: "https://github.com/Attnam/ivan", note: "репозиторій GPL v2; MANUAL з FAQ (стати, рахунок, permadeath, магазини)"}
  - {kind: other, url: "https://attnam.com/wiki/Commands", note: "IvanWiki: усі клавіші"}
  - {kind: other, url: "https://attnam.com/wiki/Attributes", note: "IvanWiki: тренування атрибутів, атрибути кінцівок, життєво важливі частини"}
  - {kind: other, url: "https://attnam.com/wiki/Eating", note: "IvanWiki: харчування, гниття, ефекти мʼяса"}
  - {kind: other, url: "https://attnam.com/wiki/Polymorph", note: "IvanWiki: поліморф, контроль, блок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=IVAN+Iter+Vehemens+ad+Necem+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-8dir, move-by-input, impassable-cells, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, hunger-clock, status-effects, multi-cell-size, chase-player, melee-vs-ranged, projectile-shot, explode-area, dungeon-generation, stairs-levels, world-map, shop-catalog, shop-buyback, round-currency, permadeath, player-death, save-single-slot, score-records, message-log, keyboard-controls, gui-render, fog-of-war, +body-part-targeting, +limb-disable, +limb-sever-reattach, +item-material, +transmute-material, +per-limb-attributes, +attribute-by-use, +armor-absorb, +polymorph, +god-mood, +sacrifice-altar, +recruit-ally, +food-spoilage, +monster-breeding]
proposes: ["+trigger:limb_hp_zero(a, part)", "+cond:material(a, m)", "+cond:vital(part)", "+effect:transmute(a, material)", "+effect:polymorph(a, into)", "+effect:pray(god)", "+effect:offer(item, altar)", "+effect:train(attr, n)", "+role:body-part", "+role:altar", "+role:material", "+ui:body-silhouette", "+ui:attribute-delta", "+window:pray-menu", "+window:equipment-window", "+window:polymorph-select", "+feature:wizard-mode", "+axis:actors=body-parts"]
author: opus
date: 2026-11-09
---

# IVAN (Iter Vehemens ad Necem) — роглайк, де кожна частина тіла має свої HP і броню, а матеріал будь-чого — змінний

## Суть
Класичний покроковий роглайк у дусі NetHack, де «HP героя» розкладено **по частинах тіла**: голова, тулуб, пах, руки, ноги мають власні HP і власну броню, кінцівку можна втратити (і монстрові теж — аж до «безпорадного тулуба»), а потім приєднати назад або отримати нову від бога чи жерця. Друга ідея — **матеріал як окрема вісь предмета**: довгий меч — це тип, а залізо, міфрил чи хліб — матеріал, від якого залежать шкода, вага, міцність і ціна; сувій зміни матеріалу перетворює і предмети, і власні кінцівки. Шлях до смерті неминучий («Violent Road to Death»), сейв стирається.

## Поле і час
- Квадратна сітка рівнів підземель і міст + мапа світу між локаціями (New Attnam, Underwater Tunnel, Attnam, Gloomy Caves, Tomb of Xinroch…).
- Покроково: швидкість дій залежить від Agility (рух) і Dexterity (атака); вантаж знижує легкість руху (Unburdened 100 · Burdened 75 · Stressed/Overloaded 50).
- Видимість обмежена (Perception — дальність зору), кольорове світло, вогонь, дим, погода, кровʼяні сліди поранених монстрів.
- Деякі монстри займають 2×2 клітини.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (гуманоїд) | player | AStr, LStr, Dex, Agi, End, Per, Int, Wis, Will, Cha, Mana, Ht, Wt; HP = сума HP частин | рух 8 напрямків, атака рухом у ворога, усе інше — командами |
| Голова · тулуб · пах | player (частина) | HP, AV | життєво важливі: HP 0 → смерть у людській формі |
| Права/ліва рука | player (частина) | HP, AV, AStr, Dex | тримає зброю/щит, блокує; може бути відрубана |
| Права/ліва нога | player (частина) | HP, AV, LStr, Agi | вантаж, удар ногою, рух; може бути відрубана |
| Відрубана кінцівка | object | матеріал, свіжість | лежить на підлозі; можна приєднати назад |
| Шматки плоті | object | — | лишаються замість кінцівки, знищеної кислотою, струмом, енергією, вогнем чи звуком |
| Предмет-зброя/броня | pickup | тип × матеріал, зачарування +N, вага, шкода/AV, точність, міцність, вимога сили | ефективність від матеріалу й навички категорії + знайомства з цим предметом |
| Матеріал (параметр, не клітина) | — | Strength, Flexibility, Density, бог-покровитель, «твердне в», вимога Int | задає міцність, вагу, ціну, шкоду предмета |
| Сувій зміни / зміцнення матеріалу | pickup | вимога Int | перетворює матеріал предмета чи власної кінцівки |
| Їжа, трупи, рідини | pickup | поживність, рівень гниття 0–8 | дає NP; гниле — отрута, сплутаність, паразити |
| Монстри | enemy | частини тіла, AV, тип шкоди | теж втрачають кінцівки; деякі 2×2; деякі розмножуються; хамелеони поліморфуються |
| Найманці · раби | ally | ціна | вербуються або купуються; команди загону (`I`) |
| Торговець | neutral | товари | підняти = купити, кинути = продати |
| Коваль · кравець | neutral | — | лагодять зламане спорядження |
| Жрець | neutral | — | лікує, повертає кінцівки (?) |
| Бог (15, поза полем) | neutral | закон ↔ хаос, ставлення | молитва, жертва; може дати нову кінцівку зі «священного» матеріалу |
| Вівтар | static | бог | молитва й жертва цьому богові; навчитись ритуалу |
| Фонтан | static | — | випадкові ефекти, серед них поліморф / контроль поліморфу |
| Жезл поліморфу | pickup | — | zap — усе в радіусі 5; застосувати чи зламати — 3×3 навколо |
| Кільце контролю поліморфу · кільце незмінності | pickup | — | вибір форми · заборона поліморфу |
| Міни й пастки | hazard | — | вибух міни: половина вогонь, половина фізична шкода |
| Сходи | static | вгору/вниз | `<` / `>` — інший рівень |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`; ЯКЩО `occupied(cell, monster)` → ТО атака.
- КОЛИ `custom: «удар влучив»` → ТО `custom: «обрати частину тіла за ToHit і Dodge»`, `damage(part, n − AV(part))`.
- КОЛИ `custom: «влучання»` → ЯКЩО `prob(dodge)` → ТО промах; критичний удар не ухиляється й дає ×1.5 + 1.
- КОЛИ `custom: «блок рукою з предметом»` → ТО `custom: «шкода − сила блоку»`, `counter(stamina, −n)`, предмет може зламатись.
- КОЛИ `custom: «HP кінцівки = 0»` → ТО `detach(limb)`, `spawn_at(severed_limb, cell)`; ЯКЩО `custom: «тип шкоди: кислота, струм, енергія, вогонь, звук»` → ТО `spawn_at(flesh_lumps, cell)` замість кінцівки.
- КОЛИ `custom: «HP голови, тулуба чи паху = 0»` → ТО `lose` (у людській формі).
- КОЛИ `custom: «втрачено руку зі зброєю»` → ТО `custom: «зброя падає»` (?); ноги — `speed(hero, −)` (?).
- КОЛИ `use(hero, severed_limb)` → ЯКЩО `custom: «кінцівка свіжа й місце вільне»` → ТО `attach(limb, hero)` (?).
- КОЛИ `custom: «молитва, коли бог прихильний, а кінцівки бракує»` → ТО `spawn(limb)`, `custom: «зі священного матеріалу бога»`.
- КОЛИ `use(hero, healing_liquid)` → ТО `heal(hero, n)`; ЯКЩО `prob(p)` → ТО `custom: «відростає втрачена кінцівка»`.
- КОЛИ `tick` → ЯКЩО `state(hero, regeneration)` → ТО `heal(hero, n)`, `custom: «повільно відростають кінцівки»`.
- КОЛИ `use(hero, scroll_change_material)` → ЯКЩО `custom: «Int ≥ вимога цільового матеріалу»` → ТО `custom: «матеріал предмета чи власної частини тіла → обраний»` (залізний меч → міфриловий чи хлібний).
- КОЛИ `use(hero, scroll_harden_material)` → ЯКЩО `custom: «Int ≥ вимога»` → ТО `custom: «матеріал → твердіший»` (Arcanite → Mithril: Int 25).
- КОЛИ `custom: «змінився матеріал»` → ТО `custom: «шкода, вага, міцність, ціна перераховуються»`.
- КОЛИ `input(offer)` на вівтарі → ЯКЩО `custom: «предмет зі священного матеріалу бога»` → ТО `custom: «ставлення бога +»`.
- КОЛИ `input(pray)` → ЯКЩО `custom: «ритуал вивчено (книга або вівтар)»` → ТО `custom: «відповідь за ставленням бога і вчинками»`; молитися можна будь-якому богові незалежно від світогляду.
- КОЛИ `custom: «вчинки гравця»` → ТО `custom: «світогляд зсувається до закону чи хаосу»`.
- КОЛИ `input(eat)` → ТО `counter(NP, +n)` за обʼємом і поживністю матеріалу (лише органіка й рідини); ЯКЩО `counter(NP, ==, max)` → ТО `custom: «блювота і «зловживання» статами»`.
- КОЛИ `timer(every)` → ТО `counter(NP, −1)`; ЯКЩО `state(hero, starving)` → ТО `custom: «випадково непритомніє»`; ЯКЩО `counter(NP, ==, 0)` → ТО `lose`.
- КОЛИ `custom: «зʼїдено гниле (рівень > 0)»` → ТО `set_state(hero, confused)`; рівень > 4 → `set_state(hero, poisoned)`; мʼясо → тасемниця.
- КОЛИ `custom: «зʼїдено мʼясо зомбі / вовкулаки / хамелеона чи мутанта»` → ТО `set_state(hero, leprosy | lycanthropy | polymorphitis)`.
- КОЛИ `timer(every)` → ЯКЩО `state(hero, leprosy)` → ТО `custom: «атрибути падають, часом відпадає кінцівка»`.
- КОЛИ `rng(p)` → ЯКЩО `state(hero, polymorphitis)` → ТО `transform(hero, random_creature)`; ЯКЩО `state(hero, polycontrol)` → ТО `choose(seen creatures)` з урахуванням Int.
- КОЛИ `input(zap wand_polymorph)` → ТО `transform(all in range 5, random)`; кільце незмінності блокує.
- КОЛИ `custom: «дія тренує атрибут»` → ЯКЩО `custom: «атрибут < (100 + досвід дії)% стартового»` → ТО `custom: «досвід атрибута +»`; рівня персонажа нема.
- КОЛИ `custom: «стан голоду»` → ТО голод тренує вниз AStr і LStr, переїдання — Agi.
- КОЛИ `custom: «тип шкоди drain»` → ТО `heal(attacker, n)`; вогонь → `set_state(limb|item, burning)`.
- КОЛИ `picked(hero, shop_item)` → ТО `currency(−price)` (Cha впливає); `place` у магазині → `currency(+price)`.
- КОЛИ `input(chat)` з найманцем/работорговцем → ТО `choose(hire | buy)` → `custom: «союзник»`.
- КОЛИ `rng(p)` → ЯКЩО `custom: «монстр, що розмножується»` → ТО `spawn(copy)`.
- КОЛИ `died(hero)` → ТО `custom: «сейв видаляється»`, `score(Σ √kills_type × (сума атрибутів типу)²)`; перемога множить рахунок ×2…5 за типом перемоги.
- Перемога: квести (перший — у соборі Attnam; далі — кілька кінцівок). Поразка: смерть = кінець забігу. Рахунок: за вбитих монстрів, з множником за перемогу.

## Керування і ввід
- Рух і атака — стрілки, цифри 1–9 або vi/NetHack-клавіші (y k u h l b j n); `g` — швидкий рух, `U` — біг, `.` — чекати, `h` — відпочинок.
- Дії: `a` застосувати (`A` — повторити) · `C` говорити · `O`/`c` відчинити/зачинити · `,` підняти · `d` кинути · `e` їсти · `D` пити · `T` скуштувати · `!` вмочити · `r` читати · `z` жезл · `t` метнути · `K` ногою · `w`/`x` зброя / обмін · `p` молитися · `f` пожертвувати · `F` ремесло · `G` гравіювати/нотатка на мапі · `I` командувати загоном · `L` дивитись · `s` шукати · `_` сісти · `V` блювати · `<` `>` сходи.
- Екрани: `i` інвентар · `E` спорядження · `m` мапа · `M` історія повідомлень · `@` навички · `\` налаштування · `?` довідка (F1 — підказка до пункту меню) · `S` зберегти · `Q` здатися.
- Wizard mode (збірка з `-DWIZARD`): `0` відірвати кінцівку, `]` підпалити кінцівку, `[` поліморф, `{` вселитися, `3` уся мапа та ін.

## Вікна, меню, HUD
- `game-screen`: мапа з туманом і світлом; бічна панель — атрибути з двома числами (поточне/базове; жовте — щойно виросло, червоне — впало) (`attribute-delta`), Ht, Wt, золото, день і час, номер ходу, стани; `message-log` знизу; `body-silhouette` HP частин тіла (?).
- `inventory-window` (`i`), `equipment-window` (`E`) — слоти за частинами тіла (?), характеристики предмета: матеріал, +N, вага, шкода/AV, точність, міцність, навичка, знайомство.
- `map-window` (`m`) з нотатками; `log-window` (`M`); `stats-window` навичок (`@`); `settings-window` (`\`); `help-window` (`?`).
- `pray-menu`: список богів з позначками L+ / C-- (сила нахилу до закону чи хаосу).
- `polymorph-select`: вибір форми з бачених істот (за контролю поліморфу).
- `end-screen`: опис смерті; `leaderboard` високих рахунків.
- `main-menu` → новий персонаж (імʼя) / продовжити збережену гру.

## Фічі поза полем
- `mode-hardcore` як єдиний: «You have only one chance»; розробники принципово без easy-режиму й без перезавантаження.
- `save-slots`: один сейв на персонажа (`S` — зберегти й вийти), видаляється при смерті.
- `leaderboard-local`; `stats` атрибутів.
- `mod-support` / варіанти: LIVAN, CLIVAN, IVANT; IVAN3D — перша особа (мод Zeno Rogue, у Steam-видання).
- Wizard mode для налагодження (окрема збірка).

## Варіації й родичі
- [nethack](nethack.md) — головний вплив (поліморф, молитва, трупи як їжа); [adom](adom.md), [omega](omega.md) — сучасники з мапою світу.
- [caves-of-qud](caves-of-qud.md) — теж частини тіла й мутації; [dungeon-crawl-stone-soup](dungeon-crawl-stone-soup.md) — без кінцівок, лише HP.
- Осі варіацій: **здоровʼя** (одне HP / HP по частинах / частини з окремою бронею й атрибутами) · **предмет** (тип / тип × матеріал) · **втрата кінцівки** (нема / тимчасово / назавжди, але можна приєднати) · **прогресія** (рівні / атрибути від вжитку).

## Цікавинки для курсу
- Тіло як список частин з HP і AV, вибір частини при влучанні, смерть лише від втрати життєво важливих — 🥉.
- Відрубана кінцівка як предмет на підлозі, який можна підібрати й приєднати — 📎.
- Предмет = тип × матеріал (міцність, щільність, гнучкість) з перерахунком шкоди й ваги — 🥉 (композиція замість спадкування).
- Сувій зміни матеріалу, що діє і на предмети, і на власне тіло — 📎.
- Атрибути від вжитку з «стелею» для кожної дії (ходьба тренує Agi лише до певної межі) — 🌱.
- Їжа з гниттям 0–8 і ефектами за видом мʼяса (проказа, лікантропія, поліморф) — 📎.
- Рахунок Σ √(вбивств) × (сила виду)² — 🌱, гарна задача на зважування.

## Мапа на каталог
- Є: `move-8dir` · `move-by-input` · `impassable-cells` · `hp-damage` · `inventory` / `inventory-items` / `inventory-limit` (вантаж) · `item-pickup` · `hunger-clock` · `status-effects` · `multi-cell-size` (2×2) · `chase-player` · `melee-vs-ranged` · `projectile-shot` (метання, жезли) · `explode-area` (міни) · `dungeon-generation` · `stairs-levels` · `world-map` · `shop-catalog` / `shop-buyback` · `round-currency` · `permadeath` · `player-death` · `save-single-slot` · `score-records` · `message-log` · `keyboard-controls` · `gui-render` · `fog-of-war`.
- **Нема** → пропозиції карток:
  - `+body-part-targeting`, `+limb-disable`, `+armor-absorb` — уже в корпусі; тут — по броні на кожну частину.
  - `+limb-sever-reattach` «Відрубана кінцівка — предмет; приєднати назад» · entities/state · 📎.
  - `+item-material` «Предмет = тип × матеріал» · entities/state · 🥉 · слоти {strength, density, flexibility}.
  - `+transmute-material` «Змінити матеріал предмета або частини тіла» · entities/interact · 📎.
  - `+per-limb-attributes` «Атрибути належать кінцівкам» · entities/state · 📎.
  - `+attribute-by-use` «Атрибути ростуть від дій, зі стелею на дію» · entities/state · 🌱.
  - `+polymorph` «Перетворення на іншу істоту (випадково / з вибором)» · entities/state · 🥉.
  - `+god-mood` (як у корпусі) + `+sacrifice-altar` «Жертва на вівтар за матеріалом» · game-logic/economy · 📎.
  - `+recruit-ally` (як у корпусі) — найманці й раби.
  - `+food-spoilage` «Їжа гниє за рівнями з ефектами» · entities/state · 🌱.
  - `+monster-breeding` «Монстри розмножуються» · entities/spawn · 🌱.

## Пропозиції до словників
- `+trigger:limb_hp_zero(a, part)` — HP окремої частини тіла вичерпано (відрізняється від ✅ `hp_zero(a)` усієї сутності).
- `+cond:material(a, m)` — предмет/частина з матеріалу (уже пропонували в корпусі); `+cond:vital(part)` — частина життєво важлива.
- `+effect:transmute(a, material)` (як у корпусі), `+effect:polymorph(a, into)`, `+effect:pray(god)`, `+effect:offer(item, altar)`, `+effect:train(attr, n)`.
- `+role:body-part` (як у корпусі), `+role:altar`, `+role:material` — матеріал як сутність-параметр.
- `+ui:body-silhouette` — фігурка тіла з кольором HP частин; `+ui:attribute-delta` — жовтий/червоний колір нещодавньої зміни стату.
- `+window:pray-menu`, `+window:equipment-window`, `+window:polymorph-select`.
- `+feature:wizard-mode` — налагоджувальні команди в окремій збірці.
- `+axis:actors=body-parts` — актор складається з частин, кожна з власним станом.

## Джерела
- ⭐ [RogueBasin: IVAN](https://www.roguebasin.com/index.php/IVAN) — частини тіла, відрубування й приєднання, смерть від голови/тулуба/паху, матеріали з 1–2 складників, Scroll of Change Material і вимога Int, 15 богів, молитва без огляду на світогляд, найманці, ковалі, 2×2-монстри, версії 0.301 (2001) → 0.60.
- [Steam](https://store.steampowered.com/app/4890840/IVAN_Iter_Vehemens_ad_Necem/) — броня й HP кожної частини, «безпорадний тулуб», меч із хліба, вовкулацтво, IVAN3D, реліз 6.11.2026.
- [GitHub Attnam/ivan](https://github.com/Attnam/ivan) і [MANUAL](https://raw.githubusercontent.com/Attnam/ivan/master/MANUAL) — FAQ: стати й скорочення, формула рахунку, магазини, permadeath, молитовні позначки.
- [IvanWiki: Commands](https://attnam.com/wiki/Commands) — клавіші; [Attributes](https://attnam.com/wiki/Attributes) — тренування й атрибути кінцівок; [Combat](https://attnam.com/wiki/Combat) — ToHit, блок, крит; [Damage](https://attnam.com/wiki/Damage) — 10 типів шкоди, знищення кінцівок; [Eating](https://attnam.com/wiki/Eating) — NP, гниття; [Status_Effects](https://attnam.com/wiki/Status_Effects) — проказа, регенерація; [Polymorph](https://attnam.com/wiki/Polymorph); [Materials](https://attnam.com/wiki/Materials) — властивості й бог-покровитель; [Worlds](https://attnam.com/wiki/Worlds) — локації.
- YouTube: [пошук](https://www.youtube.com/results?search_query=IVAN+Iter+Vehemens+ad+Necem+gameplay).

## Непевне
- (?) Як саме приєднують відрубану кінцівку (команда й умови: свіжість, той самий вид) — RogueBasin каже лише «reattaching them».
- (?) Наслідки втрати руки (чи падає зброя) і ноги (повільніше, повзання) — не знайшов явного опису.
- (?) Слоти спорядження за частинами тіла (шолом, плащ, рукавиці, чоботи, кільця) і «фігурка тіла» з HP у HUD — з памʼяті.
- (?) Жерці відновлюють кінцівки — FAQ: «Priests, gods, certain potions and magical items may help».
- (?) Кількість кінцівок гри (кілька фіналів, «тип перемоги» множить рахунок ×2…5) — деталей немає.
- (?) Ідентифікація невідомих сувоїв/зілль — за жанром імовірна, джерелами не підтверджена, тому без тегу.
