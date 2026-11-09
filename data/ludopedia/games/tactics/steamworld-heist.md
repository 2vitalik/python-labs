---
title: SteamWorld Heist
slug: steamworld-heist
aka: [SWH]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: setup
  goal: state
year: 2015
platforms: [3DS, PC (Steam), macOS, Linux, PS4, Vita, Wii U, Xbox One, Switch, iOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/SteamWorld_Heist", best: true, note: "бічний вид, ручне прицілювання без відсотків, рикошети, 4 класи, процедурні кораблі, swag, капелюхи, NG+"}
  - {kind: steam, url: "https://store.steampowered.com/app/322190/", note: "«skill over chance», bullet-bouncing, процедурні рівні, DLC The Outsider"}
  - {kind: fandom, url: "https://steamworld.wiki.gg/wiki/SteamWorld_Heist", note: "wiki.gg: цілі місій (усіх знищити / обʼєкт / вижити хвилі), swag → галони, Space Bars, капелюхи"}
  - {kind: fandom, url: "https://steamworld.wiki.gg/wiki/Weapons_(SWH)", note: "класи зброї й теги: laser sight, Can't shoot after moving, No ricochets, Pierces covers, Friendly fire"}
  - {kind: fandom, url: "https://steamworld.wiki.gg/wiki/Utilities", note: "2 слоти утиліт: броня, ремонт, гранати, бічна зброя як вільна дія, чоботи на +хід"}
  - {kind: fandom, url: "https://steamworld.wiki.gg/wiki/Captain_Piper", note: "дерево навичок за рівнями: Power Shot, Inspire у радіусі клітин, Area Repair"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=SteamWorld+Heist+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, projectile-shot, mirror-reflect, explode-area, shoot-burst, shoot-spread, shoot-cooldown, status-effects, unit-xp-skills, inventory-items, inventory-limit, shop-between-levels, round-currency, dungeon-generation, destroy-all-enemies, reach-exit, enemy-waves, difficulty-levels, world-map, character-select, ai-opponent, +manual-aim, +ricochet-ballistics, +laser-sight, +move-or-sprint, +no-shoot-after-move, +cover-system, +destructible-cover, +flanking, +hat-shot-collectible, +loot-swag-bags, +free-action-items, +once-per-mission-items, +pierce-flags, +friendly-fire, +adjacency-aura, +new-game-plus]
proposes: ["+trigger:aimed(shot, angle)", "+effect:ricochet(shot, surface)", "+effect:knock_hat", "+cond:moved_this_turn", "+ui:aim-line", "+ui:move-sprint-zones", "+window:space-bar", "+feature:new-game-plus", "+axis:aim=manual", "+card:manual-aim", "+card:move-or-sprint"]
author: opus
date: 2026-11-09
---

# SteamWorld Heist — XCOM збоку без кубика: сам ведеш приціл, а куля відскакує від стін за укриття

## Суть
Покрокова тактика загону роботів-піратів на борту ворожих кораблів, показаних **збоку**. Гравець по черзі рухає своїх бійців, а постріл **цілить руками**: кут задає гравець, куля летить по прямій і рикошетить від стін — відсотків влучання, як у [xcom](xcom.md), нема. Головний прийом — «трюковий» постріл від стелі чи стіни у ворога за укриттям або щитом; близько до [hard-west](hard-west.md), де рикошет — лише окрема здібність з ціною в удачу. Між місіями — бар-хаб: найм, крамниця, капелюхи, які збиваєш з ворожих голів.

## Поле і час
- Бічний розріз корабля: кімнати з підлогами, драбинами/люками (?) і стінами; рівні збираються процедурно з модулів, щоразу інакше.
- Позиції — клітини (рух рахується в клітинах: «Movement 8», Inspire «на дві клітини»); **приціл вільний**: кут пострілу неперервний, балістика — променем з відбиттями. Тому `field: square` з вільною траєкторією.
- Хід: усі бійці гравця, потім вороги (`turn`). Кожен боєць за хід: **рух + дія**, або **спринт** (далі, але без дії).
- Видимість: вороги за межами огляду не показані, кімнати відкриваються при вході (?) — `info: partial`.
- Тривога/хвилі: деякі місії — «вижити хвилі»; підкріплення, якщо затягнути (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Член екіпажу (Piper, Seabrass, Sally, Wonky…) | piece | HP, рух, клас зброї, 2 слоти утиліт, рівень | рух або спринт, постріл, утиліта, здібність |
| Ворог (Scrappers, Royalists, Vectron, Cowbots) | enemy | HP, зброя | ходить і стріляє за AI; щити в деяких |
| Бос | boss | великий HP | місії-кульмінації (?) |
| Укриття (ящик, бочка, стійка) | object | HP | поглинає постріли, поки не зруйноване |
| Вибухова бочка | hazard | — | вибухає від влучання, шкодить по площі (?) |
| Стіна / підлога / стеля | static | — | відбиває кулі (рикошет), непрохідна |
| Swag-мішок | pickup | вміст: вода/галони, зброя, утиліта | збирається на рівні, видається в кінці місії |
| Капелюх | pickup | косметичний | злітає від влучання в голову, підбирається на полі |
| Вихід / шлюз | static | — | евакуація після виконання цілі |
| Ціль місії (обʼєкт) | object | HP | знищити |

### Класи (Wikipedia + wiki.gg)
| Клас | Зброя | Роль |
|---|---|---|
| Vanguard | — | танк-бравлер, тримає удар |
| Sharpshooter | снайперські пістолі з лазерним прицілом; часто «не стріляє після руху» | дальній |
| Assault | дробовики, SMG | ближній, висока шкода |
| Heavy | пускові, мортири | шкода по площі, friendly fire |
| Handgun | пістолі/револьвери | універсал, деякі — кілька пострілів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «кожен боєць має рух і дію»`.
- КОЛИ `input(move, a, cell)` → ЯКЩО `custom: «cell у зоні руху»` → ТО `move(a, cell)`, дія лишається; ЯКЩО `custom: «cell у зоні спринту»` → ТО `move(a, cell)`, `end_turn(a)` — дії нема (`+cond:moved_this_turn`).
- Run 'N' Gun (Payroll): `custom: «після спринту можна атакувати; cooldown 5 ходів»`.
- КОЛИ `input(aim, angle)` → ТО `custom: «траєкторія = промінь під кутом»`; ЯКЩО `custom: «зброя з laser sight»` → ТО `custom: «показано лінію з відбиттями»` (`+ui:aim-line`).
- КОЛИ `input(shoot)` → ЯКЩО `custom: «зброя "Can't shoot after moving"»` and `custom: «боєць рухався цього ходу»` → ТО `block`.
- КОЛИ `contact(bullet, wall)` → ЯКЩО `custom: «зброя без тегу No ricochets»` → ТО `bounce(bullet)` (`+effect:ricochet`).
- КОЛИ `contact(bullet, cover)` → ЯКЩО `custom: «зброя без тегу Pierces covers»` → ТО `damage(cover, n)`, `disappear_a`; ЯКЩО `hp_zero(cover)` → ТО `disappear_b`.
- КОЛИ `contact(bullet, unit)` → ТО `damage(n)`; ЯКЩО `custom: «Pierces characters»` → ТО `custom: «куля летить далі крізь ціль»`.
- КОЛИ `contact(bullet, head)` → ТО `custom: «капелюх злітає»` (`+effect:knock_hat`); КОЛИ `contact(crew, hat)` → ТО `pickup`.
- КОЛИ `custom: «критичний шанс»` → ТО `damage(n + crit)` — Brass Goggles дає +50 % шансу (єдиний кубик гри).
- Flanker (Payroll): КОЛИ `custom: «влучання в спину ворога»` → ТО `damage(+2…+4)`.
- КОЛИ `input(explosive)` → ТО `explode(area)`; ЯКЩО `custom: «Friendly fire»` → ТО шкодить і своїм.
- Inspire (Piper): ЯКЩО `in_range(ally, piper, 1|2)` → ТО `custom: «союзник +1/+2 шкоди»`; Area Repair — `heal(piper + inspired, full)`.
- Утиліти: КОЛИ `input(use, item)` → ТО `heal(a, n)` / `explode(area)` / `stun(target, 1)` / `custom: «бічна зброя — вільна дія»`; обмеження `custom: «раз або двічі за місію»`.
- КОЛИ `contact(crew, swag)` → ТО `pickup` — видача після місії.
- КОЛИ `hp_zero(enemy)` → ТО `disappear_a`; КОЛИ `hp_zero(crew)` → ТО `custom: «вибуває до кінця місії»` (?).
- Перемога місії: `destroy-all-enemies` / знищити обʼєкт / вижити хвилі; далі — до виходу (?). Поразка: увесь загін вибув.
- Рейтинг місії: `custom: «оцінка за результатом (зірки (?))»` → більше нагород/доступ далі.

## Керування і ввід
- Вибір бійця → підсвітка зон руху і спринту (`+ui:move-sprint-zones`) → клік клітини → прицілювання стиком/мишею: лінія повертається, відпускання — постріл.
- Здібності й утиліти — окремі кнопки дій у панелі бійця; кінець ходу — кнопка.

## Вікна, меню, HUD
- `main-menu` → `difficulty-select` → `world-map` (зоряна мапа з місіями) → `+window:space-bar` (найм, крамниця, NPC) → `character-select` (загін на місію, спорядження) → `game-screen` → `end-screen` (рейтинг, swag, XP).
- `game-screen`: бічний розріз корабля; `hp-bar` над кожним; лінія прицілу; зони руху/спринту; панель дій з `skill-bar` (cooldown); `turn-indicator`.
- `shop-window` — зброя й утиліти за галони; `inventory-window` — спорядження загону; `+ui:hat-collection` — шафа капелюхів (?).

## Фічі поза полем
- `unit-xp-skills` — рівні 0–10, на кожному — пасивка, здібність або +HP/+рух (дерево фіксоване для кожного бійця).
- `shop-between-levels` — зброя, утиліти; 2 слоти утиліт на бійця.
- `difficulty-presets` — можна міняти між місіями; `+feature:new-game-plus` — після проходження, зберігає капелюхи й досвід.
- Процедурні рівні — кораблі генеруються щоразу; DLC The Outsider (боєць Fen), набори капелюхів.

## Варіації й родичі
- У корпусі: [xcom](xcom.md) (укриття і 2 дії, але шанс у відсотках), [hard-west](hard-west.md) (рикошет як здібність з ціною), [frozen-synapse](frozen-synapse.md) (бічна-верхня балістика без кубика, WEGO), [steamworld-dig](../dig-gravity/steamworld-dig.md) (той самий світ).
- SteamWorld Heist II (2024) — підводний човен на «Великому морі»; ігролад у Wikipedia не описано.
- Межа сімʼї: вид збоку з гравітацією й вільним прицілом — на межі з артилерійськими (Worms) і shooter-ами; у `tactics` через покрокові загони й клітинний рух.
- **Осі варіацій «влучання»:** відсоток (XCOM) / удача-пул (Hard West) / ручний приціл + рикошети (Heist) / одночасне виконання (Frozen Synapse); **рух:** 2 дії / рух+дія або спринт / очки дій.

## Цікавинки для курсу
- Ручний приціл з трасуванням променя і відбиттями від стін сітки — 🥉 (DDA/відрізки + відбиття за нормаллю).
- Рух+дія або спринт без дії — два радіуси BFS на одній сітці — 📎.
- Теги зброї як дані (`no_ricochet`, `pierces_cover`, `no_shoot_after_move`, `friendly_fire`) — 🌱 (`state-as-data`).
- Руйноване укриття з HP, яке поглинає кулю — 📎.
- Аура «натхнення» в радіусі клітин — 🌱.
- Капелюх як колекційний предмет за влучання в зону голови (хітбокс частини тіла) — 📎.
- Процедурний корабель з кімнат-модулів — 🥈.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `projectile-shot` · `mirror-reflect` (рикошет) · `explode-area` · `shoot-burst` / `shoot-spread` · `shoot-cooldown` (здібності) · `status-effects` (stun, cripple) · `unit-xp-skills` · `inventory-items` + `inventory-limit` (2 слоти) · `shop-between-levels` · `round-currency` · `dungeon-generation` (кораблі) · `destroy-all-enemies` · `enemy-waves` · `difficulty-levels` · `world-map` · `character-select`.
- **Нема** → пропозиції карток:
  - `+manual-aim` «Ручне прицілювання під кутом» · entities/combat · 🥉.
  - `+ricochet-ballistics` (повтор з Hard West) — тут базова, не здібність.
  - `+laser-sight` «Лінія прицілу з відбиттями» · interface/hud · 📎.
  - `+move-or-sprint` «Рух+дія або далекий рух без дії» · entities/legality · 📎.
  - `+no-shoot-after-move` «Зброя, що не стріляє після руху» · entities/legality · 🌱.
  - `+cover-system` / `+flanking` (повтор з XCOM) — тут flanking = бонус у спину.
  - `+destructible-cover` «Укриття з HP» · entities/combat · 📎.
  - `+hat-shot-collectible` «Збитий з ворога предмет-колекція» · entities/interact · 🌱.
  - `+loot-swag-bags` «Здобич на рівні видається після місії» · game-logic/economy · 🌱.
  - `+free-action-items` «Предмет як вільна дія» · entities/state · 🌱.
  - `+once-per-mission-items` «Заряди предмета на місію» · entities/state · 🌱.
  - `+pierce-flags` «Куля пробиває укриття / бійців» · entities/combat · 🌱.
  - `+friendly-fire` «Вибух шкодить своїм» · entities/combat · 🌱.
  - `+adjacency-aura` «Аура бонусу в радіусі клітин» · entities/state · 🌱.
  - `+new-game-plus` «Нова гра зі збереженим прогресом» · levels/progression · 🌱.

## Пропозиції до словників
- `+trigger:aimed(shot, angle)` — гравець задав кут пострілу (відрізняти від `input(target_cell)`).
- `+effect:ricochet(shot, surface)` — повтор з Hard West; тут для будь-якої зброї без тегу.
- `+effect:knock_hat` — збити предмет із сутності (капелюх падає на поле).
- `+cond:moved_this_turn` — сутність уже рухалась цього ходу.
- `+ui:aim-line` — лінія траєкторії з відбиттями; `+ui:move-sprint-zones` — дві зони досяжності різним кольором.
- `+window:space-bar` — хаб між місіями (найм, крамниця, NPC).
- `+feature:new-game-plus` — повторне проходження зі збереженням прогресу.
- `+axis:aim=manual` — влучання задає гравець, не кубик (значення: chance · manual · deterministic).
- `+card:manual-aim`, `+card:move-or-sprint` — див. вище.

## Джерела
- ⭐ [Wikipedia: SteamWorld Heist](https://en.wikipedia.org/wiki/SteamWorld_Heist) — бічний вид, «skill over chance», ручне прицілювання, трюкові рикошети, класи, swag, капелюхи, NG+, процедурні кораблі.
- [Steam: SteamWorld Heist](https://store.steampowered.com/app/322190/) — опис, DLC The Outsider і капелюхи.
- [wiki.gg: SteamWorld Heist](https://steamworld.wiki.gg/wiki/SteamWorld_Heist) — цілі місій, swag → галони, Space Bars.
- [wiki.gg: Weapons (SWH)](https://steamworld.wiki.gg/wiki/Weapons_(SWH)) — класи зброї й теги поведінки.
- [wiki.gg: Utilities](https://steamworld.wiki.gg/wiki/Utilities) — 2 слоти, ремонт, гранати, бічна зброя як вільна дія, рух.
- [wiki.gg: Captain Piper](https://steamworld.wiki.gg/wiki/Captain_Piper) — дерево навичок 0–10; також сторінка Grahame Phroggi (Run 'N' Gun, Flanker).
- YouTube: пошук «SteamWorld Heist gameplay».

## Непевне
- (?) Дає влучання в голову додаткову шкоду, чи лише збиває капелюх; крити — лише шанс (за утилітами), не за зоною влучання.
- (?) Що стається з бійцем при HP = 0 (вибуває до кінця місії, без перманентної смерті — з памʼяті).
- (?) Рейтинг місії (зірки), тривога й підкріплення при затягуванні, обовʼязкова евакуація до виходу.
- (?) Укриття: як саме боєць «займає» укриття і чи вибухають бочки — сторінки «Cover» на wiki.gg нема.
- (?) Назви рівнів складності; чи «Handgun» — окремий клас бійців чи лише клас зброї.
- (?) Валюта: Wikipedia — вода, wiki.gg — галони (ймовірно, вода в галонах).
