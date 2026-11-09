---
title: Path of Achra
slug: path-of-achra
aka: [Achra]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: state
year: 2024
platforms: [PC]
links:
  - {kind: fandom, url: "https://pathofachra.wiki.gg/wiki/Events", best: true, note: "wiki.gg: повний список подій-тригерів, порядок розвʼязання атаки, умови «if»"}
  - {kind: steam, url: "https://store.steampowered.com/app/2128270/Path_of_Achra/", note: "Steam: culture × class × religion, 50+ сил, ланцюги тригерів, automove; EA 2023, реліз 7.05.2024"}
  - {kind: fandom, url: "https://pathofachra.wiki.gg/wiki/Stats", note: "Str/Dex/Will, Life, Dodge → Block → Armor, Encumbrance, Inflexibility"}
  - {kind: fandom, url: "https://pathofachra.wiki.gg/wiki/Walking_the_Path", note: "21 день-область, вибір наступної з 2–3, вежі, Обеліск, Void, Astrolith"}
  - {kind: fandom, url: "https://pathofachra.wiki.gg/wiki/Controls", note: "керування: bump-атака, auto play, молитви 1–3"}
  - {kind: fandom, url: "https://pathofachra.wiki.gg/wiki/Religion", note: "24 релігії, 3 молитви з зарядами, Divine Intervention"}
  - {kind: fandom, url: "https://pathofachra.wiki.gg/wiki/Glory", note: "Glory: +1 стат і +1 сила за рівень, розблокування стартових опцій"}
  - {kind: other, url: "https://en.wikipedia.org/wiki/List_of_roguelikes", note: "рядок у списку роглайків (Ulfsire, 2024)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Path+of+Achra+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-8dir, keyboard-controls, hp-damage, status-effects, inventory-items, item-pickup, run-relics, in-round-upgrades, unit-xp-skills, permadeath, dungeon-generation, sequential-levels, reach-exit, world-map, chain-reaction, melee-vs-ranged, speed-per-type, message-log, character-select, leaderboard, +event-trigger-build, +attack-resolution-pipeline, +auto-play-step, +prayer-charges, +death-save-charge, +route-choice-no-return, +summon-limit, +encumbrance-speed]
proposes: ["+trigger:on_event(name)", "+cond:encumbered", "+effect:summon(a)", "+window:route-choice", "+ui:glory-bar", "+ui:speed-bar", "+feature:auto-play", "+card:event-trigger-build", "+card:attack-resolution-pipeline"]
author: opus
date: 2026-11-09
---

# Path of Achra — роглайк без активних умінь: усе, крім ходу, спрацьовує на подіях

## Суть
Гравець збирає героя з трьох частин — культура, клас, релігія — і йде крізь 21 «день» паломництва до Обеліска, а потім у Порожнечу. Окрім чотирьох дій ходу (атакувати, ступити, помолитись, стояти) **активних умінь нема**: кожна сила, предмет і бог дають ефекти «на подію» (on hit, on kill, on prayer, on step…), а ефекти породжують нові події — ланцюги реакцій. Ядро — складати збірку, де одна атака запускає каскад; керування мінімальне, є навіть «авто-хід».

## Поле і час
- Квадратна сітка, вид згори, рівень — одна арена з ворогами, предметами й виходом; рух на 8 напрямків (numpad 7/8/9…).
- Хід = одна з дій: Attack · Step · Pray · Stand Still. Кожна дія триває час, що залежить від Speed; «game turn» — одиниця часу, що тече за Speed (база 5, вище 80 — спадна віддача).
- Після кожного game turn спрацьовують усі «on game turn» ефекти всіх юнітів рівня.
- Структура забігу: 21 день, день = область з кількох рівнів; після області — вибір наступної з 2–3; назад не можна — пройдене поглинає World-Ending Sea.
- Дні 1–13 — землі Ахри (звичайні області по 3 рівні, вежі 5–8 поверхів з вартовим, Forbidden Places з 1 поверху; день 12 — Обеліск з богом нагорі); дні 14–21 — The Void; день 20 — Astrolith, на останньому поверсі King of Many Colors.
- Видимість: поле арени видно (?) — туману в джерелах не згадано.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Паломник (герой) | player | Life, Str, Dex, Will, Speed, Dodge, Block, Armor, резисти, Glory | 4 дії ходу; усе інше — тригери сил/предметів/бога |
| Ворог | enemy | Life, зброя, резисти (до 90 %) | ходить і атакує; має власні тригери |
| Вартовий вежі / області (Guardian) | boss | — | на останньому поверсі вежі; перемога дає нагороди |
| Бог Обеліска · King of Many Colors | boss | — | фінальні боси Ахри і Void; останній — перемога в грі |
| Nemesis | enemy | — | окремий тип супротивника (сторінка вікі; деталі не читав) |
| Призване створіння (summon) | ally | ліміт = Willpower | зʼявляється від тригерів; б'ється на боці героя |
| Зброя (main / offhand) | pickup | Hit, Accuracy, Size, Encumbrance, Inflexibility | дає initial attack; дві зброї — дві атаки, якщо ціль у дальності |
| Броня | pickup | Armor, Block, Encumbrance | надягається вільно; перевантаження ріже Speed і Dodge |
| Void-предмет | pickup | — | у Void по одному на область; незвичні ефекти |
| Вихід | static | — | `Enter` — піти, навіть не вбивши всіх |
| Статус (Bleed, Poise, Grace, Bloodrage…) | — | стеки | накладається подією; Willpower Recovery щогейм-тік шансом знімає шкідливий цілком |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(step dir)` → ЯКЩО `occupied(cell, enemy)` → ТО `custom: «initial attack замість кроку»`; інакше `move(player, dir)`.
- КОЛИ `input(attack)` → ЯКЩО `in_range(player, enemy, weapon_range)` → ТО `custom: «initial attack обома зброями»`.
- КОЛИ `custom: «атака»` → ТО `custom: «on attack / on being attacked»` → перевірка Dodge: ЯКЩО `prob(dodge)` → ТО `custom: «on dodge»`, атака закінчилась.
- → далі Block: ЯКЩО `prob(block_chance)` і шкода ≤ Block value → ТО `custom: «on block»`, кінець; → Armor: ЯКЩО шкода ≤ Armor → ТО `custom: «on shrug off»`, кінець.
- → інакше `custom: «hit: on hit / on being hit»`, `damage(target, n)`, `custom: «on dealing damage / on being dealt damage»`.
- КОЛИ `after(effect)` → ТО `custom: «ефект породжує нову подію — ланцюг; триває, доки є вороги»` (`+trigger:on_event(name)`).
- КОЛИ `custom: «on hit, if bare fist / if two-handing / if encumbered»` → ТО ефект сили (умова `custom`; `+cond:encumbered`).
- КОЛИ `custom: «прямий хіт від уміння»` → ТО `damage(target, n)` без Dodge/Block/Armor.
- КОЛИ `hp_zero(enemy)` → ТО `custom: «on kill / on enemy death»`, `counter(glory, +n)`.
- КОЛИ `enter(player, level)` → ЯКЩО `first_time` → ТО `custom: «on entrance»`, `counter(glory, +n)`.
- КОЛИ `counter(glory, >=, next)` → ТО `custom: «+1 stat point, +1 power point; on Glory rising»`.
- КОЛИ `counter(glory, >=, 10)` → ТО `unlock(prayer_2)`; КОЛИ `counter(glory, >=, 20)` → ТО `unlock(prayer_3)`.
- КОЛИ `input(pray k)` → ЯКЩО `has(player, charges_k)` → ТО ефект молитви, `counter(charges_k, −n)`, `custom: «on prayer»`.
- КОЛИ `custom: «умова перезаряду молитви, напр. вхід в нову область»` → ТО `counter(charges_k, +1)`.
- КОЛИ `hp_zero(player)` → ЯКЩО `custom: «хоч одна молитва повністю заряджена»` → ТО `heal(player, 25%)`, `custom: «випадкова повна молитва втрачає всі заряди»` (Divine Intervention); інакше `lose`.
- КОЛИ `custom: «тригер призову»` → ЯКЩО `count(ally, <, willpower)` → ТО `custom: «summon»` (`+effect:summon(a)`), `custom: «on summon»`.
- КОЛИ `turn_end(game)` → ТО `custom: «on game turn у всіх юнітів»`; для кожного шкідливого статусу ЯКЩО `prob(willpower_recovery)` → ТО `clear_state(a, status)`.
- КОЛИ `picked(player, item)` → ТО `custom: «on picking up an item»`; спорядження — вільна заміна.
- КОЛИ `custom: «Encumbrance > Strength»` → ТО `speed(player, −2 за зайве)`, `custom: «−20 Dodge за зайве»`.
- КОЛИ `reach(player, exit)` → ТО `next_level`; КОЛИ `custom: «область пройдено»` → ТО `choose(2–3 areas)`.
- КОЛИ `died(king_of_many_colors)` → ТО `win`.
- Рахунок: Glory за забіг записується як результат; кожні 20 Glory відкривають нову стартову опцію.

## Керування і ввід
- Рух — numpad / QWE-ASD-ZXC / YKU-HJL-BNM (8 напрямків); крок у ворога = атака (bump).
- `Tab` / ПКМ / numpad 0 — **auto play**: атакує ціль, крокує до найближчого ворога в дальності, підбирає найближчий предмет, іде до виходу і проходить крізь нього.
- `Alt` — перемкнути ціль серед ворогів у дальності атаки.
- `Space` / `S` / numpad 5 / СКМ — стояти (не пропуск, а дія тривалістю за Speed).
- `1` `2` `3` — молитви; `Enter` — старт, вхід в нову землю, вихід через вихід, підтвердження смерті.

## Вікна, меню, HUD
- `character-select`: культура × клас × релігія (1000+ комбінацій, частина — за розблокуванням).
- `game-screen`: арена; HP-смуга; під нею `glory-bar` (жовта), далі `speed-bar`; лічильник Divine Interventions і рівень Glory «*N»; `message-log` (?).
- Вибір наступної області з 2–3 — `route-choice` (`+window:route-choice`).
- Бічна панель сил/статів для розподілу очок при підвищенні (?).
- `end-screen`: результат Glory після смерті / перемоги; `leaderboard` — (?).

## Фічі поза полем
- `permadeath`: смерть — новий забіг; `unlockables` — кожні 20 Glory нова стартова опція (культура / клас / релігія).
- Cycles: повторні проходження з вищим циклом — більше Life ворогам і героєві, більше Glory (формули на сторінці Stats).
- Prestige Classes — відкриваються з Glory (деталі не читав).
- `auto-play` (`+feature:auto-play`): одна клавіша грає сама до виходу.
- Демо з перенесенням розблокувань у повну гру; Early Access з 1.05.2023.

## Варіації й родичі
- Збірка через тригери: 868-HACK і Rift Wizard (`roguelike/rift-wizard`, вибір заклинань за очки), Brogue — у корпусі; поза корпусом — Backpack Hero / Balatro-подібні «якщо X — то Y».
- Мінімум активних дій: One Way Heroics (лише рух уперед), Desktop Dungeons (бій — формула).
- **Осі варіацій**: дії гравця — 1 (рух) / 4 (як тут) / десятки (класичний роглайк); ефекти — активні / пасивні на подію; ланцюги — обмежені глибиною / до вичерпання ворогів; маршрут — лінійний / граф з вибором без повернення.

## Цікавинки для курсу
- Шина подій: сили підписуються на «on hit», «on kill», «on step»…, ефект публікує нову подію — 🥉 (observer + захист від нескінченних циклів).
- Конвеєр розвʼязання атаки Dodge → Block → Armor → Hit → Damage, на кожному кроці свій тригер — 📎.
- Auto play: «атакуй ціль / іди до ворога / підбери / до виходу» — пріоритетна поведінка-ланцюжок — 📎.
- Молитви з зарядами + Divine Intervention (повний заряд рятує від смерті) — 🌱.
- Encumbrance > Strength ріже Speed і Dodge: одна нерівність дає два штрафи — 🌱.
- Генератор героя з трьох незалежних частин, кожна додає стати й тригери — 🌱.

## Мапа на каталог
- Є: `move-8dir` · `keyboard-controls` · `hp-damage` · `status-effects` (стеки, тік) · `inventory-items` · `item-pickup` · `run-relics` (сили й void-предмети до кінця забігу) · `in-round-upgrades` (очки сил) · `unit-xp-skills` (Glory → стати й сили) · `permadeath` · `dungeon-generation` · `sequential-levels` · `reach-exit` · `world-map` (дні-області) · `chain-reaction` (каскад подій) · `melee-vs-ranged` (дальність зброї) · `speed-per-type` · `message-log` · `character-select` · `leaderboard`.
- **Нема** → пропозиції карток:
  - `+event-trigger-build` «Ефекти на подію і ланцюги подій» · game-logic/events · 🥉 · слоти {events, max_depth}.
  - `+attack-resolution-pipeline` «Етапи атаки: ухил → блок → броня → шкода» · entities/combat · 📎.
  - `+auto-play-step` «Одна клавіша — розумний наступний крок» · interface/input · 📎.
  - `+prayer-charges` «Активки з зарядами й умовою перезаряду» · entities/state · 🌱.
  - `+death-save-charge` «Повний заряд рятує від смерті» · game-logic/lose · 🌱.
  - `+route-choice-no-return` «Вибір наступної області без повернення» · levels/progression · 🌱.
  - `+summon-limit` «Ліміт призваних за статом» · entities/spawn · 🌱.
  - `+encumbrance-speed` «Вага понад силу ріже швидкість» · entities/state · 🌱.

## Пропозиції до словників
- `+trigger:on_event(name)` — спрацювати на іменовану подію бою (on hit, on dodge, on kill, on prayer) — ширше за `after(effect)`.
- `+cond:encumbered` — вага спорядження понад силу (і загалом «стан збірки»: two-handing, bare fist).
- `+effect:summon(a)` — призвати союзника з перевіркою ліміту (зараз `spawn`).
- `+window:route-choice` — вибір наступної області/вузла маршруту.
- `+ui:glory-bar` · `+ui:speed-bar` — смуги досвіду й швидкості під HP.
- `+feature:auto-play` — авто-хід до виходу однією клавішею.
- `+card:event-trigger-build` · `+card:attack-resolution-pipeline`.

## Джерела
- ⭐ [wiki.gg: Events](https://pathofachra.wiki.gg/wiki/Events) — 4 дії ходу, усі події, порядок атаки, умови «if», game turn.
- [Steam](https://store.steampowered.com/app/2128270/Path_of_Achra/) — опис, 50+ сил, 1000+ комбінацій, automove, дати.
- [wiki.gg: Stats](https://pathofachra.wiki.gg/wiki/Stats) — формули статів, Dodge/Block/Armor, Encumbrance, Inflexibility.
- [wiki.gg: Walking the Path](https://pathofachra.wiki.gg/wiki/Walking_the_Path) — 21 день, області, вежі, Обеліск, Void, Astrolith.
- [wiki.gg: Controls](https://pathofachra.wiki.gg/wiki/Controls) · [Religion](https://pathofachra.wiki.gg/wiki/Religion) · [Glory](https://pathofachra.wiki.gg/wiki/Glory).
- [Wikipedia: List of roguelikes](https://en.wikipedia.org/wiki/List_of_roguelikes) — рядок гри.
- YouTube: [пошук «Path of Achra gameplay»](https://www.youtube.com/results?search_query=Path+of+Achra+gameplay).

## Непевне
- (?) Точна модель часу («speed is weird» — вікі сама не пояснює): чи це енергетична черга, як у DCSS.
- (?) Скільки Glory треба на рівень; чи Glory дає й за вбивство кожного ворога однаково.
- (?) Чи є туман війни; чи видно весь рівень одразу.
- (?) Як розподіляються очки сил (вікно, дерево) і що таке Prestige Class механічно.
- (?) Чи є в грі онлайн-таблиця рекордів, чи лише локальний запис Glory.
- (?) Хто такі Nemeses — окремі вороги-переслідувачі чи модифікатори.
