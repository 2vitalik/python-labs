---
title: Sunken Stones
slug: sunken-stones
aka: []
family: tactics
also: [roguelike]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: survive
year: 2025
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2601810/Sunken_Stones/", best: true, note: "капітан + екіпаж на полі 5×5, вороги цілять лише в капітана, стихії Steel/Smoke/Salt, лічильник прокляття, walk the plank"}
  - {kind: itch, url: "https://spritewrench.itch.io/sunken-stones-demo", note: "демо: Smoking = 50 % шанс промаху, Submerge, Steel «домінує в рядах»; список девлогів"}
  - {kind: other, url: "https://spritewrench.itch.io/sunken-stones-demo/devlog/735550/public-demo-is-back-version-005s", note: "девлог 0.0.5S (2024): фази раунду Loot → Deploy → Enemy, скелі-перешкоди"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2601810&count=15&maxlength=0", note: "новини Steam (JSON): 3 зони, бос Kraken, рулетка прокляття (1.1.0), Raffle Bag, історія змін статів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sunken+Stones+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [cursor-place, hp-damage, status-effects, impassable-cells, round-currency, character-select, message-log, game-screen, end-screen, tutorial-window, +protect-vip, +leader-death-lose, +deployment-phase, +knockback, +curse-meter, +elemental-synergy, +dismiss-for-recruit, +treasure-select, +penalty-roulette, +unlock-raffle, +boss-fight, +zone-progression]
proposes: ["+role:leader", "+trigger:round_end", "+cond:element", "+effect:knockback", "+ui:curse-meter", "+window:treasure-select", "+window:penalty-roulette", "+feature:unlock-raffle"]
author: opus
date: 2026-11-09
---

# Sunken Stones — піратський екіпаж на полі 5×5: монстри бʼють лише капітана, а проклятий скарб підсилює їх

## Суть
Покрокова пазл-стратегія-роглайт про піратів і проклятий скарб. Гравець обирає капітана, рятує й наймає членів екіпажу і розставляє їх на полі 5×5 проти морських монстрів (Creeps). Головна незвичність: **вороги цілять лише в капітана**, тож уся тактика — захист однієї фігури руками решти. Друга вісь — **лічильник прокляття**: скарби дають силу, але «уражений» екіпаж наповнює шкалу, і повна шкала в кінці раунду підсилює всіх крипів.

## Поле і час
- Квадратна сітка **5×5** (Steam); скелі — перешкоди, що впливають на розстановку (девлог 0.0.5S).
- Раунд — фази: **Loot** (відкрити скрині, прийняти врятованих) → **Deploy** (розставити екіпаж) → **Enemy** (діють монстри й зʼявляються небезпеки) — за девлогом демо 2024; у релізі могло змінитися (?).
- Забіг — 3 зони (від Cerulean Tides до WraithSea); кожна зона — своя сімʼя монстрів і бос (бос зони 1 — Kraken).
- Між зонами — вибір: зняти ураження (affliction) з екіпажу або вилікуватися, без повернення в порт.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Капітан (6 на вибір) | player | HP, savvy, здібність, ультимейт | ядро загону: **єдина ціль ворогів**; здібність (у деяких — за ammo) і ультимейт |
| Член екіпажу, Steel | ally | ціна в savvy, уміння | агресивний: бонус атаки, контроль позицій, «домінує в рядах», витрачає додатковий savvy |
| Член екіпажу, Smoke | ally | ammo, уміння | комбо й хитрощі: витрачає ammo, накладає Smoking, контроль натовпу, відкидання |
| Член екіпажу, Salt | ally | HP як ціна | контроль поля: платить власним HP, накладає Submerge |
| Уражений член екіпажу | ally | стан afflicted | після проклятого скарбу; у бою додає поділки до лічильника прокляття |
| Крипер (морський монстр) | enemy | HP, атака | атакує лише капітана; сімʼя крипів своя в кожній зоні |
| TENTACLE[LEFT] | enemy | HP 4 (з 0.0.6f) | щупальце зі стороною в назві — напрямлена атака (?) |
| Бос зони (Kraken тощо) | boss | HP | фінал зони; після перемоги — вікно між зонами |
| Небезпека | hazard | — | зʼявляється у фазі ворогів разом із монстрами (девлог) |
| Скеля | static | — | займає клітину, обмежує розстановку |
| Скриня | container | — | відкривається у фазі Loot: предмети / екіпаж |
| Проклятий скарб | pickup | — | зʼявляється на полі → вибір скарбу → ураження члена екіпажу |
| George the Lucky Manatee | neutral | — | «особливий корисний спавн» під час забігу (?) |
| Гарпуни, бомби | pickup | — | предмети Supply Boon (гарпуни) і стартові (прибрані в 0.0.6j) |

Стани ворогів: **Smoking** — 50 % шанс промаху атакою (демо-сторінка); **Submerge** — лише на ворогів, ні атакує, ні може бути атакований.

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «старт забігу»` → ТО `window(character-select)` → `choose(captain)`: HP, savvy і здібність капітана.
- КОЛИ `phase_start(loot)` → ТО `custom: «відкрити скрині»`, `give(crew, crewmate)` за врятованих.
- КОЛИ `input(deploy, crewmate, cell)` → ЯКЩО `free(cell)` і `counter(savvy, >=, cost)` → ТО `place(captain, crewmate)`, `counter(savvy, -cost)`.
- КОЛИ `input(deploy, crewmate, cell)` → ЯКЩО `occupied(cell, rock)` → ТО `block`.
- КОЛИ `input(deploy, crewmate, cell)` → ЯКЩО `state(crewmate, afflicted)` → ТО `counter(curse, +1)`.
- КОЛИ `phase_start(enemy)` → ТО `spawn_at(creep, custom: «поле»)` і `spawn_at(hazard, custom: «поле»)` (девлог: «monster and hazard spawns»).
- КОЛИ `custom: «атака крипера»` → ТО `damage(captain, n)` — ціль завжди капітан, екіпаж не атакують.
- КОЛИ `custom: «атака крипера»` → ЯКЩО `state(creep, smoking)` і `prob(50)` → ТО `custom: «промах»`.
- КОЛИ `custom: «атака крипера або удар по ньому»` → ЯКЩО `state(creep, submerged)` → ТО `block`.
- КОЛИ `input(ability, smoke_crew)` → ЯКЩО `counter(ammo, >=, n)` → ТО `set_state(creep, smoking)` або `custom: «knockback»`, `counter(ammo, -n)`.
- КОЛИ `input(ability, salt_crew)` → ТО `hp(caster, -n)`, `set_state(creep, submerged)`.
- КОЛИ `input(ability, steel_crew)` → ТО `custom: «бонус атаки / удар по ряду / зсув позицій»`, `counter(savvy, -n)`.
- КОЛИ `custom: «уміння члена екіпажу»` → ЯКЩО `custom: «наступний у ланцюгу має синергію»` → ТО `trigger(rule)` — комбо-ланцюг (?).
- КОЛИ `hp_zero(creep)` → ТО `disappear`.
- КОЛИ `custom: «на полі зʼявився скарб»` → ТО `window(treasure-select)` → `choose(treasure)`; проклятий → `set_state(crewmate, afflicted)`.
- КОЛИ `custom: «кінець раунду»` → ЯКЩО `counter(curse, >=, max)` → ТО до 1.1.0 — `set_state(all_creeps, buffed)`; з 1.1.0 — `custom: «рулетка: випадковий наслідок»`.
- КОЛИ `input(walk_the_plank, crewmate)` → ТО `take(crew, crewmate)`, `custom: «новий рекрут із сильнішим потенціалом»`.
- КОЛИ `input(ability, captain)` → ТО здібність капітана; `input(ultimate)` → ультимейт (?) з окремою умовою готовності.
- КОЛИ `hp_zero(boss)` → ТО `custom: «вікно перемоги зони»` → `choose(«зняти affliction» | «вилікуватися»)` → `next_level`.
- КОЛИ `hp_zero(captain)` → ТО `lose` (?).
- Перемога: пройти 3 зони з босами · Поразка: загибель капітана (?) · Рахунок: —.

## Керування і ввід
- Миша: вибір члена екіпажу з ростеру → клік по клітині поля 5×5 (Deploy); кнопки здібності й ультимейту капітана.
- Наведення на клітину показує її деталі (з травня 2025).
- Вибір скарбу — окремий крок; баг 1.0.3 «наведення на поле пропускає вибір скарбу» підтверджує, що це модальне вікно.

## Вікна, меню, HUD
- `character-select` — Captain Select Screen: 6 капітанів; Raffle Bag — відкриття додаткового екіпажу.
- `game-screen`: поле 5×5; HP капітана (`hp-bar`); savvy (`coins`-подібний лічильник); ammo; шкала прокляття (`progress-bar`, пропозиція `curse-meter`); ростер екіпажу (`pocket`); `tooltip` клітини; історія змін статів у бою (`message-log`).
- `custom-window` → `treasure-select` — вибір скарбу; рулетка прокляття (з 1.1.0).
- `end-screen` — вікно перемоги між зонами з вибором «зняти ураження / вилікуватися».
- `tutorial-window` — навчання з діалоговими бульбашками й ультимейтом.

## Фічі поза полем
- Роглайт-забіги; 6 капітанів зі своїми здібностями; пул екіпажу (у демо — до 60) з відкриттям через Raffle Bag — мета-прогресія (?).
- Перебудова складу: walk the plank замість нескінченного ростеру.
- Навчання; досягнення Steam; DLC-саундтрек.
- Undo, налаштування складності, щоденні забіги — у джерелах не згадані.

## Варіації й родичі
- Родичі в корпусі: [into-the-breach](into-the-breach.md) (захист цілі на малому полі), [shogun-showdown](../roguelike/shogun-showdown.md) (мале поле, роглайт), [plants-vs-zombies](../tower-lanes/plants-vs-zombies.md) (розстановка з ресурсу проти хвиль), [super-auto-pets](../tower-lanes/super-auto-pets.md) (синергії складу).
- **Осі варіацій**: ціль ворогів — будь-хто / найближчий / **лише лідер** · ціна розстановки — один ресурс / різні ресурси за стихією (savvy, ammo, HP) · ризик-нагорода — проклятий скарб → шкала → бафф ворогам / рулетка.

## Цікавинки для курсу
- Вороги атакують лише капітана — 🌱: тривіальний таргетинг, тактика переходить у блокування й контроль.
- Шкала прокляття з перевіркою в кінці раунду → бафф усім ворогам — 📎.
- Три стихії з різними ресурсами (savvy / ammo / HP) — 📎: один інтерфейс уміння, три гаманці.
- Фази раунду Loot → Deploy → Enemy як скінченний автомат — 📎.
- Submerge і Smoking (стан «поза боєм», 50 % промаху) — 🌱 поверх `status-effects`.
- Walk the plank: звільнити слот заради кращого рекрута — 🌱.

## Мапа на каталог
- Є: `cursor-place` ↔ розстановка екіпажу · `hp-damage` · `status-effects` ↔ Smoking/Submerge/affliction · `impassable-cells` ↔ скелі · `round-currency` ↔ savvy · `character-select` · `message-log` ↔ історія змін статів · `game-screen` · `end-screen` · `tutorial-window`.
- **Нема** → пропозиції карток:
  - `+protect-vip` «Вороги цілять лише в лідера» · game-logic/opponent · 🌱.
  - `+leader-death-lose` «Смерть лідера = поразка» · game-logic/lose · 🌱.
  - `+deployment-phase` «Фаза розстановки в кожному раунді» · game-logic/opponent · 📎.
  - `+knockback` «Відкидання цілі» · entities/legality · 📎.
  - `+curse-meter` «Шкала ризику → бафф ворогам у кінці раунду» · game-logic/difficulty · 📎.
  - `+elemental-synergy` «Стихії з різними ресурсами й синергіями» · entities/state · 🥉.
  - `+dismiss-for-recruit` «Звільнити члена загону за кращого рекрута» · game-logic/economy · 🌱.
  - `+treasure-select` «Вибір нагороди з ризиком» · game-logic/economy · 🌱.
  - `+penalty-roulette` «Випадковий штраф замість фіксованого» · game-logic/difficulty · 🌱.
  - `+unlock-raffle` «Відкриття контенту лотереєю» · levels/progression · 🌱.
  - `+boss-fight` «Бос наприкінці зони» · game-logic/waves · 🥉.
  - `+zone-progression` «Зони забігу з вибором між ними» · levels/progression · 📎.

## Пропозиції до словників
- `+role:leader` — фігура-лідер: її смерть = поразка, на неї цілять вороги.
- `+trigger:round_end` — кінець повного раунду (усі фази), не ходу однієї сторони.
- `+cond:element` — сутність належить стихії (Steel/Smoke/Salt).
- `+effect:knockback` — відкинути ціль від джерела удару.
- `+ui:curse-meter` — шкала прокляття з порогом, що спрацьовує в кінці раунду.
- `+window:treasure-select` — вибір скарбу; `+window:penalty-roulette` — рулетка покарання.
- `+feature:unlock-raffle` — відкриття нових членів загону лотереєю (Raffle Bag).

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/2601810/Sunken_Stones/) — 5×5, капітан і savvy, вороги лише на капітана, три стихії, Submerge, лічильник прокляття, walk the plank; реліз 18.07.2025, Spritewrench.
- [itch.io — демо](https://spritewrench.itch.io/sunken-stones-demo) — Smoking = 50 % промаху, Steel «домінує в рядах».
- [Девлог 0.0.5S](https://spritewrench.itch.io/sunken-stones-demo/devlog/735550/public-demo-is-back-version-005s) — фази Loot/Deploy/Enemy, скелі.
- [Новини Steam (API)](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2601810&count=15&maxlength=0) — 3 зони, Kraken, рулетка прокляття, Raffle Bag, George the Lucky Manatee, підказки на клітинах, історія статів.
- YouTube: пошук «Sunken Stones gameplay».

## Непевне
- (?) Чи стоїть капітан на полі як фігура, чи він поза полем (портрет) — джерела кажуть лише «вороги цілять у капітана».
- (?) Як рухаються й атакують крипери (лінії, ряди, сторони — `TENTACLE[LEFT]` натякає на атаку збоку) і чи показують намір наперед.
- (?) Чи рухається екіпаж після розстановки, як саме спрацьовують комбо-ланцюги.
- (?) Фази раунду — з девлогу демо 2024; розмір шкали прокляття, наслідки рулетки, умова поразки — не знайдено.
- (?) Boons (Supply Boon) — реліквії забігу чи разові предмети; мета-прогресія між забігами.
