---
title: "Fell Seal: Arbiter's Mark"
slug: fell-seal
aka: [Fell Seal]
family: tactics
also: []
klass: figure
axes:
  field: layers
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2019
platforms: [PC, macOS, Linux, PS4, Xbox One, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Fell_Seal:_Arbiter%27s_Mark", best: true, note: "«грається як FFT», творення героїв, класи, складність: травми й permadeath, розробник, релізи"}
  - {kind: other, url: "https://www.rpgsite.net/review/8479-fell-seal-arbiters-mark-review", note: "RPG Site: радіальне меню класів, слоти 2 набори + 2 пасиви + контратака, 10 навичок на клас, Lich платить HP, налаштування складності"}
  - {kind: steam, url: "https://store.steampowered.com/app/699170/Fell_Seal_Arbiters_Mark/", note: "30+ класів, ~300 навичок, підклас і пасиви, 240+ спорядження, крафт, висоти, кастом вигляду"}
  - {kind: steam, url: "https://store.steampowered.com/app/1155320/Fell_Seal_Arbiters_Mark_Missions_and_Monsters/", note: "DLC: найм монстрів з 2 підкласами, місії-відправки, 3 нові класи, Arbiter's Guild"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Fell+Seal+Arbiter%27s+Mark+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, melee-vs-ranged, height-levels, status-effects, unit-xp-skills, inventory-items, shop-between-levels, shop-catalog, ai-opponent, destroy-all-enemies, legal-move-highlight, reachable-highlight, world-map, map-window, difficulty-levels, save-multi-slot, character-select, permadeath, +job-system, +subclass-slots, +retaliation, +injury-penalty, +custom-difficulty, +hp-as-mana, +item-crafting, +mission-dispatch, +monster-recruit, +appearance-editor, +deployment-phase, +turn-order-bar, +facing-hit-bonus]
proposes: ["+trigger:attacked", "+effect:counterattack", "+cond:charges", "+ui:turn-order-bar", "+window:job-window", "+window:formation", "+window:crafting-window", "+window:mission-board", "+window:appearance-editor", "+window:difficulty-custom", "+feature:custom-difficulty", "+feature:permadeath", "+axis:session"]
author: opus
date: 2026-11-09
---

# Fell Seal: Arbiter's Mark — інді-наступник Final Fantasy Tactics: та сама сітка з висотою й класами, але з налаштовуваною жорсткістю

## Суть
Загін «арбітрів» бʼється на ізометричних мапах-сітках з перепадами висоти; основа — як у [Final Fantasy Tactics](final-fantasy-tactics.md): професії, навички вчаться в одному класі й ставляться в інший. Гравець сам створює більшість бійців (клас, портрет, одяг, кольори). Нове відносно FFT — **жорсткість як налаштування**: окремі перемикачі статів ворога, permadeath, дозволу ворогам лікуватись і воскрешати; замість «кристалу» — травми, якщо боєць іде в бій одразу після нокауту. Ця картка описує **відмінності від FFT**; спільне (висоти, досяжність, вибір цілі) — див. її файл.

## Поле і час
- Ізометрична квадратна сітка з висотами і «нерівним рельєфом» — як у FFT (`field: layers`).
- Черга ходів — індивідуальна, за швидкістю юніта, видна як список (?); на відміну від FFT, **нема заряджання заклинань** — дії миттєві (?).
- MP на старті бою частковий і накопичується щоходу (?) — сильні навички стають доступні ближче до середини бою.
- Інформація повна, випадковість — шанси влучань і статусів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Арбітр (створений боєць) | piece | HP, MP, стати, основний клас, підклас, 2 пасиви, 1 контратака, спорядження | хід за швидкістю; вчить навички свого класу |
| Сюжетний персонаж | piece | може мати унікальний клас | частина недоступних класів закрита для інших |
| Lich | piece | — | кастує заклинання **за HP**, а не MP |
| Fellblade | piece | — | накладає стани на ворогів атаками |
| Vessel | piece | — | подвійне закляття (аналог Summoner) |
| Монстр загону (DLC) | ally | до 2 підкласів з 20+ | наймається й приручається, бʼється поруч |
| Ворог-людина, монстр, іменний монстр | enemy | — | AI; на «Veteran» лікується, воскрешає союзників, юзає предмети |
| Бос (опційні бої) | boss | — | окремі бої поза сюжетом |
| Перепад висоти | terrain | висота | обмежує рух і впливає на дальність (?) |
| Предмет-витратник | pickup | заряди на бій (?) | використовується з слота; відновлюється після бою (?) |
| Матеріал крафту | resource | — | випадає з ворогів; відкриває секретні класи і зброю |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(u)` (за швидкістю) → ТО `custom: «меню: рух, дія, кінець ходу з вибором напрямку»` (?).
- КОЛИ `turn_start(u)` → ТО `custom: «+MP за хід»` (?).
- КОЛИ `input(act, u, skill)` → ЯКЩО `custom: «skill з основного класу або підкласу»` and `custom: «вистачає MP»` → ТО ефект одразу (без заряджання, ≠ FFT) (?).
- КОЛИ `input(act, lich, spell)` → ТО `damage(lich, cost)` замість витрати MP.
- КОЛИ `custom: «u атакований»` → ЯКЩО `custom: «у слоті контратаки є навичка-реакція»` → ТО `custom: «контратака / реакція»`.
- КОЛИ `input(item, u)` → ЯКЩО `custom: «у слота лишились заряди»` → ТО `use(u, item)`; КОЛИ `level_end` → ТО `custom: «заряди відновлюються»` (?).
- КОЛИ `hp_zero(u)` → ЯКЩО `mode(permadeath)` → ТО `disappear(u)` назавжди; інакше `set_state(u, ko)` до кінця бою.
- КОЛИ `level_start` → ЯКЩО `custom: «боєць був у нокауті в попередньому бою»` and `not mode(easiest)` → ТО `set_state(u, injured)` (тимчасовий штраф статів).
- КОЛИ `custom: «бій завершено з юнітом у класі»` → ТО `custom: «очки класу; відкривається наступна з 10 навичок»`.
- КОЛИ `custom: «класи-передумови вивчено»` → ТО `unlock(class)`; секретні класи — за матеріалами крафту.
- КОЛИ `input(mission, recruits)` (DLC) → ТО `custom: «загін іде на місію поза боєм і повертає ресурси, нові локації, класи»`.
- Перемога: знищити всіх ворогів (або сюжетну ціль). Поразка: усі бійці загону вибули (?).
- Складність (`custom-difficulty`): стати ворогів · permadeath · чи може ворог юзати предмети · чи може ворог воскрешати; пресет «Veteran» — усе дозволено.

## Керування і ввід
- Курсор по клітинах, поворот камери; меню дії активного юніта; підсвітка досяжних клітин і області навички — як у FFT.
- Радіальне меню вибору класу (запозичене в FFT); у меню загону — слоти основного класу, підкласу, двох пасивів, контратаки, спорядження.
- Редактор вигляду: портрет, одяг, кольори; вигляд фіксований або міняється з класом.

## Вікна, меню, HUD
- `main-menu`: New / Continue / Load / Options.
- `map-window` — карта світу з вузлами-локаціями (бої, міста).
- `formation` — розстановка загону перед боєм (?).
- `game-screen`: ізометрична мапа, `turn-order-bar` (?), панель юніта (HP/MP), прогноз влучання й шкоди.
- `job-window` — радіальне меню класів з деревом відкриття і списком навичок.
- `shop-window`, `crafting-window`, `inventory-window` (240+ предметів спорядження).
- `appearance-editor` — створення й вигляд бійця.
- `difficulty-custom` — перемикачі складності.
- `mission-board` (DLC) — відправка бійців на місії; Arbiter's Guild (апгрейди гільдії).
- `dialogue-window`, `end-screen` бою, `save-slots`.

## Фічі поза полем
- Створення бійців і повний редактор вигляду; турнір і завдання відкривають нові образи.
- Класи 30+ (+3 у DLC: Beastmaster, Samurai, Wrangler), ~300 навичок; секретні класи і зброя за матеріалами.
- Турніри, опційні боси, пост-гейм підземелля (~40 год на все).
- `custom-difficulty` + `permadeath` як опція; травми замість кристалізації.
- DLC Missions and Monsters: найм монстрів, місії-відправки, 5 локацій із великими боями.

## Варіації й родичі
- [Final Fantasy Tactics](final-fantasy-tactics.md) — прямий прообраз; [Tactics Ogre](tactics-ogre.md), [Triangle Strategy](triangle-strategy.md), [Disgaea](disgaea.md).
- **Відмінності від FFT** (головне для корпусу):
  - нема Brave/Faith і зодіаку; нема CT-заряджання заклинань (?);
  - смерть: не лічильник 3 → кристал, а нокаут → травма-штраф наступного бою; permadeath — лише опція;
  - слоти: 2 набори навичок + 2 пасиви + 1 контратака (у FFT: Action, Secondary, Reaction, Support, Movement);
  - предмети з зарядами на бій, що відновлюються (у FFT — купуються поштучно) (?);
  - складність — набір незалежних перемикачів, а не одна шкала;
  - Lich (HP як мана) і Vessel (подвійне закляття) — класи з нестандартною ціною.
- Осі варіацій: **ціна навички** (MP / HP / заряди / накопичувальний MP); **наслідок нокауту** (нічого / травма / лічильник / смерть).

## Цікавинки для курсу
- Складність як набір незалежних прапорців (`enemy_items`, `enemy_revive`, `permadeath`, `stat_mult`) — 🌱, гарна вправа на конфіг.
- Травма як стан між боями (`injured`, якщо нокаут у попередньому) — 🌱.
- Lich: навичка, що платить HP замість MP — 🌱 (параметризувати ціну ресурсом).
- Слоти «основний клас + підклас + пасиви + контратака» — 📎.
- Відкриття класів за передумовами (граф класів) — 🥉.
- Накопичувальний MP (старт із частини, +N щоходу) — 🌱 (?).

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `height-levels` · `status-effects` · `unit-xp-skills` · `inventory-items` · `shop-between-levels`/`shop-catalog` · `world-map`/`map-window` · `difficulty-levels` · `permadeath` (опція) · `character-select` ↔ створення бійця · `save-multi-slot`.
- **Нема** → пропозиції карток:
  - `+subclass-slots` «Основний клас + підклас + пасиви» · entities/state · 📎 · слоти {sets: 2, passives: 2, counter: 1}.
  - `+injury-penalty` «Травма після нокауту» · entities/death · 🌱.
  - `+custom-difficulty` «Перемикачі складності» · settings · 🌱.
  - `+hp-as-mana` «Навичка за HP» · entities/combat · 🌱.
  - `+item-crafting` · `+mission-dispatch` «Відправка юнітів на місії поза боєм» · levels/progression · 📎.
  - `+monster-recruit` «Найм монстрів» · `+appearance-editor` «Редактор вигляду героя» · interface · 📎.
  - `+job-system`, `+deployment-phase`, `+facing-hit-bonus` — як у FFT.

## Пропозиції до словників
- `+trigger:attacked`, `+effect:counterattack` — слот контратаки.
- `+cond:charges` — у предмета/слота лишились заряди.
- `+ui:turn-order-bar` — список черги ходів.
- `+window:job-window`, `+window:formation` (вже з FFT), `+window:crafting-window`, `+window:mission-board`, `+window:appearance-editor`, `+window:difficulty-custom`.
- `+feature:custom-difficulty`, `+feature:permadeath`; `+axis:session` = `campaign`.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Fell_Seal:_Arbiter%27s_Mark) — «грається як FFT», творення героїв, рівні складності: без штрафу / тимчасовий штраф після бою / permadeath; 6 Eyes Studio, Unity, релізи 2019.
- [RPG Site: review](https://www.rpgsite.net/review/8479-fell-seal-arbiters-mark-review) — радіальне меню, слоти 2+2+1, 10 навичок на клас, Lich (HP), Fellblade, Vessel, налаштування складності, турніри, пост-гейм.
- [Steam](https://store.steampowered.com/app/699170/Fell_Seal_Arbiters_Mark/) — 30+ класів, ~300 навичок, підклас і пасиви, 240+ предметів, крафт, висоти, кастом вигляду.
- [Steam: Missions and Monsters](https://store.steampowered.com/app/1155320/Fell_Seal_Arbiters_Mark_Missions_and_Monsters/) — монстри з 2 підкласами, місії-відправки, Beastmaster/Samurai/Wrangler, Arbiter's Guild.

## Непевне
- (?) Фан-вікі (fandom 402, wiki.gg 401) і офіційний сайт недоступні: черга ходів за швидкістю, відсутність заряджання, накопичувальний MP, заряди предметів, бонус за удар у спину — з памʼяті.
- (?) Чи є окреме вікно розстановки перед боєм і список черги ходів.
- (?) Точні механіки травм (скільки боїв триває штраф, чи складається).
