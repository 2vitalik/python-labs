---
title: Tower of the Sorcerer / Magic Tower (魔塔)
slug: magic-tower
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: none
  goal: state
year: 1996
platforms: [PC-9801, MS-DOS, Windows, Java, Flash, web (H5), mobile]
links:
  - {kind: other, url: "https://raw.githubusercontent.com/ckcz123/mota-js/master/project/functions.js", best: true, note: "рушій H5mota: getDamageInfo — точна формула бою (раунди, першим бʼє герой, спец-здібності); 10 хв на розуміння ядра"}
  - {kind: wiki, url: "https://zh.wikipedia.org/wiki/%E9%AD%94%E5%A1%94", note: "Tower of the Sorcerer: автор, 1996, порти й англ. версія"}
  - {kind: docs, url: "https://raw.githubusercontent.com/ckcz123/mota-js/master/_docs/element.md", note: "документація рушія: ключі, двері, зілля/самоцвіти, предмети, спец-здібності монстрів"}
  - {kind: official, url: "https://github.com/ckcz123/mota-js", note: "відкритий HTML5-рушій веж (BSD-3)"}
  - {kind: play, url: "https://h5mota.com/", note: "H5魔塔广场: 2000+ веж онлайн, рейтинги, редактор"}
  - {kind: steam, url: "https://store.steampowered.com/app/1141290/Tactical_Nexus/", note: "Tactical Nexus — сучасна Magic Tower без рандому, undo/redo"}
  - {kind: steam, url: "https://store.steampowered.com/app/388620/DungeonUp/", note: "DungeonUp — нащадок із процедурними рівнями"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=magic+tower+%E9%AD%94%E5%A1%94+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, key-and-door, hp-damage, item-pickup, inventory-items, impassable-cells, round-currency, shop-catalog, sequential-levels, player-death, event-points, save-multi-slot, save-autosave, replay, level-solver, in-game-editor, cell-click, cell-transform, +deterministic-combat, +damage-preview, +stat-gems, +rising-price-shop, +floor-fly, +monster-manual, +critical-value]
proposes: ["+trigger:bump", "+cond:can_damage", "+effect:fight", "+effect:stat(a, ±n)", "+role:npc-merchant", "+ui:damage-preview", "+ui:critical-value", "+window:codex-window", "+window:floor-select", "+window:save-slots", "+feature:replay", "+feature:level-editor", "+axis:random=none-rpg"]
author: opus
date: 2026-11-02
---

# Magic Tower (魔塔) — RPG без рандому: бій — формула, ключі — бюджет, вежа — головоломка маршруту

## Суть
Герой підіймається вежею поверх за поверхом; кожен поверх — повністю видима мапа з дверима трьох кольорів, ключами, монстрами, самоцвітами атаки/захисту й зіллями HP. Бій не має випадковості: втрата HP = функція (HP, ATK, DEF героя й монстра), і її видно ще до бою. Ресурси скінченні (ключі, зілля, золото), тож гра — оптимізація маршруту: кого вбити зараз, яку двері відчинити, коли купити +ATK, щоб наступний бій коштував менше. Предок жанру — Tower of the Sorcerer (Caravan Software, 1996); у Китаї — тисячі фанатських «веж».

## Поле і час
- Поверх — фіксована сітка (класично 11×11 клітин (?)), вся видима одразу (`info: full`); поверхи зʼєднані сходами вгору/вниз (24, 50 або більше поверхів).
- Покроково, але час не має значення: монстри стоять на місці й не ходять; хід = один крок героя або один «удар об» обʼєкт.
- `random: none` — рівні ручні, бій детермінований (саме тому вежі мають рейтинги «скільки HP лишилося»).
- Шари: підлога/стіна + обʼєкт (монстр, двері, предмет, NPC) + події-тригери на клітинах (діалог, засідка, відкрити залізні двері).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP, ATK, DEF, MDEF (щит), золото, XP/рівень (у частині веж), ключі | рух 4 напрямки; «наступити» на монстра = бій |
| Монстр | enemy | HP, ATK, DEF, золото, XP, спец-здібності | стоїть; бій ініціює лише гравець |
| Бос | boss | великі параметри, події | охороняє вихід/сюжет |
| Жовті/сині/червоні двері | gate | колір | відкриває ключ того ж кольору, ключ витрачається |
| Залізні двері / ворота | gate | подія | відкриваються перемогою над охоронцями або важелем |
| Ключ (жовтий/синій/червоний) | pickup | колір | +1 до лічильника ключів |
| Червоний / синій самоцвіт | pickup | +ATK / +DEF (множник області вежі) | постійне посилення |
| Червоне / синє зілля | pickup | +HP мале / велике | лікування одразу при підборі |
| Сходи ↑ / ↓ | static | — | на поверх вище/нижче |
| Вівтар-крамниця | static / neutral | ціна росте з кожною покупкою | золото → +HP / +ATK / +DEF |
| Старий / купець | neutral | — | дає предмет, підказку або продає ключі |
| Злодій (NPC) | neutral | — | сюжетний: відкриває прохід |
| Кирка (破墙镐) | pickup | — | зруйнувати сусідню стіну |
| Бомба (炸弹) | pickup | — | знищити сусідніх монстрів (без нагороди) |
| Транспортер поверхів (楼传) | pickup | постійний | телепорт на будь-який відвіданий поверх |
| Книга монстрів (怪物手册) | pickup | постійний | показує всіх монстрів поверху й очікувані втрати |
| Хрест (十字架) / Щасливу монету | pickup | постійні | хрест — посилює проти певних ворогів (?); монета — ×2 золота |
| Свята вода / чарівні черевики / заморожування / сувій землетрусу | pickup | одноразові | лікування; стрибок через клітину; заморозити; зруйнувати всі стіни поверху, що піддаються |
| Лава / зона монстра | hazard | — | шкода при вході/поряд (у пізніх вежах) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`.
- КОЛИ `contact(hero, monster)` → ЯКЩО `hero.atk − mon.def <= 0` → ТО `block` («не можна атакувати»); інакше бій:
  - `turn = ceil(mon.hp / (hero.atk − mon.def))`; `per = max(0, mon.atk − hero.def)`;
  - `damage = (turn − 1) × per` (герой бʼє першим, останній удар — його) `− hero.mdef`, не менше 0;
  - ТО `hp(hero, −damage)`; ЯКЩО `hp_zero(hero)` → `lose`; інакше `disappear_b`, `currency(+mon.gold)`, `counter(xp, +mon.xp)`.
- Спец-здібності змінюють формулу: `先攻` перший удар монстра (+1×per) · `魔攻` per = mon.atk (ігнорує DEF) · `坚固` DEF = hero.atk − 1 (лише 1 шкоди за удар) · `N连击` per×N · `破甲`/`反击` — додаткова шкода від DEF/ATK героя · `吸血` — відсоток HP героя · `固伤` фіксована шкода · `中毒`/`衰弱`/`诅咒` — стан після бою (отрута щокроку, −ATK/DEF, без золота/XP) · `自爆` HP героя → 1 · `领域`/`夹击`/`阻击` — шкода, коли проходиш поряд / між двома, відштовхування.
- КОЛИ `contact(hero, door[c])` → ЯКЩО `has(hero, key[c])` → ТО `disappear_b`, `take(hero, key[c])`; інакше `block`.
- КОЛИ `contact(hero, gem|potion)` → ТО `pickup`, `custom: «stat +value × ratio_області»`.
- КОЛИ `contact(hero, altar)` → ТО `window(shop)`; купівля → ЯКЩО `count(gold, >=, price)` → ТО `currency(−price)`, `stat(+n)`, `custom: «price зростає»`.
- КОЛИ `contact(hero, npc)` → ТО `window(dialogue)`, `give(hero, item)` (один раз).
- КОЛИ `enter(hero, event_cell)` → ТО `trigger(rule)` (засідка: `spawn` монстрів, двері за спиною зачиняються; відкрити залізні двері).
- КОЛИ `input(pickaxe, dir)` → ЯКЩО `cell(wall, breakable)` → ТО `set_cell(floor)`, `take(pickaxe)`.
- КОЛИ `input(floor_fly)` → ЯКЩО `visited(floor)` → ТО `teleport(hero, stairs_of_floor)`.
- КОЛИ `died(guardians)` → ТО `unlock(iron_door)`; КОЛИ `died(final_boss)` → ТО `win`.
- Перемога: здолати фінального боса / дійти на верх. Поразка: HP = 0 (часто — «софтлок»: ключів/HP не вистачає далі, гра не скаже). Рахунок (H5): HP, що лишилось у фіналі, — рейтинг вежі.

## Керування і ввід
- Стрілки (або WASD) — крок; клік/тап по клітині — автошлях (H5), з показом шляху.
- Гарячі клавіші H5: книга монстрів, транспортер поверхів, збереження/завантаження, `A` — відкат до автосейву (фактично undo), `Q` — спорядження, `V` — швидка крамниця, `R` — відтворення запису (1–6 — швидкість).
- Предмети — з панелі інструментів (клік або клавіша), з вибором напрямку для кирки/бомби.

## Вікна, меню, HUD
- `game-screen` — поверх + `stat-panel` (поверх, рівень, HP, ATK, DEF, MDEF, золото, XP), лічильники ключів трьох кольорів, `inventory-bar` предметів; `damage-preview` — **очікувана втрата HP прямо на іконці монстра** (显伤; червоне — смертельно), опційно `critical-value` (скільки ATK треба для меншої кількості раундів).
- `codex-window` (книга монстрів) — усі монстри поверху: HP/ATK/DEF, золото, XP, спец-здібності, втрата HP, критичне значення.
- `floor-select` (транспортер) — список відвіданих поверхів.
- `shop-window` (вівтар) — три кнопки «+HP / +ATK / +DEF» з поточною ціною; купці ключів — те саме.
- `dialogue-window` — розмова з NPC.
- `save-slots` — збереження/завантаження, автосейв.
- `replay-window` (H5) — перегляд запису проходження; `leaderboard` — рейтинги веж.
- `main-menu`, `end-screen` (фінал/смерть), `help-window` (H5: курс-навчальна вежа).
- Переходи: `main-menu` → `game-screen` ⇄ `codex-window` / `floor-select` / `shop-window` / `save-slots`; смерть → `end-screen` → завантажити сейв.

## Фічі поза полем
- `save-slots` + `autosave` — головний «undo» жанру (класична порада: зберігайся перед кожним рішенням); Tactical Nexus — повний `undo`/`redo`.
- `difficulty-presets` (H5: кілька складностей однієї вежі — множники параметрів).
- `replay` + `leaderboard-online` (H5 перевіряє рекорд відтворенням запису), `level-editor` + `level-sharing` (H5mota: редактор веж без програмування), `user-levels-browser` (2000+ веж).
- Tactical Nexus: `meta-progression` (медалі між вежами), «чистий» рахунок без медалей.

## Варіації й родичі
- Tower of the Sorcerer (1996) → Magic Tower Jr. (1997) → Windows-порт з англ. перекладом (1998) → Java (2001) → китайські Flash-вежі (新新魔塔 та ін.) → H5mota (сотні фанатських веж) → Tactical Nexus (2019), DungeonUp (2014, процедурні рівні), DROD RPG (Caravel), Towerbound.
- Осі варіацій: **генерація** (ручна вежа / процедурна — DungeonUp) · **прокачка** (лише самоцвіти / ще рівні за XP) · **відкат** (сейви / undo-redo) · **спец-здібності** (жодних / десятки модифікаторів формули) · **ціни** (фіксовані / зростають з кожною покупкою).
- Родичі: Desktop Dungeons (детермінований порядок убивств, стоячі вороги), Chip's Challenge (ключі-двері як бюджет), DROD.

## Цікавинки для курсу
- Формула бою `ceil(HP/(ATK−DEF))` раундів × `(mATK−DEF)` — детермінований бій з прогнозом — 🌱 (одна чиста функція, ідеальна для unit-тестів).
- Прогноз втрат на іконці кожного монстра + «критичне значення» ATK (бінарний пошук мінімального ATK, що зменшує раунди) — 📎.
- Спец-здібності як модифікатори формули (перший удар, магічна атака, міцний, N ударів, отрута, слабкість) — 🥉 (стратегія/декоратор над функцією бою).
- Ключі трьох кольорів як скінченний бюджет: кожні двері — рішення — 🌱 (картка `key-and-door` є).
- Вівтар з ціною, що росте з кожною покупкою — 🌱.
- Розвʼязувач вежі: пошук оптимального маршруту (максимум HP наприкінці) у просторі станів «зібрано/відчинено/вбито» — 👑 (комбінаторний вибух, евристики, DP по підмножинах).
- Запис-відтворення проходження як перевірка рекорду — 🥉 (детермінізм → реплей = список кроків).

## Мапа на каталог
- Є: `move-4dir` · `key-and-door` · `hp-damage` · `item-pickup` · `inventory-items` · `impassable-cells` · `round-currency` · `shop-catalog` · `sequential-levels` (поверхи) · `player-death` · `event-points` (HP як рахунок) · `save-multi-slot` + `save-autosave` · `replay` · `level-solver` · `in-game-editor` (H5) · `cell-click` · `cell-transform` (кирка).
- **Нема** → пропозиції карток:
  - `+deterministic-combat` «Бій за формулою без кидків» · entities/combat · 📎 · слоти {formula, first_strike}.
  - `+damage-preview` «Прогноз втрат на ворогові» · interface/hud · 📎.
  - `+stat-gems` «Постійні +ATK/+DEF/+HP предмети» · entities/state · 🌱.
  - `+rising-price-shop` «Ціна росте з кожною покупкою» · economy/shop · 🌱 · слот {price_fn} (дитина `shop-catalog`).
  - `+floor-fly` «Телепорт на відвіданий поверх» · rules/progress · 🌱.
  - `+monster-manual` «Книга ворогів поточного рівня з прогнозом» · interface/menus (#window) · 📎.
  - `+critical-value` «Скільки атаки до меншої кількості раундів» · interface/hud · 📎.
  - `+monster-specials` «Модифікатори формули бою (перший удар, магія, N ударів, отрута)» · entities/combat · 🥉.

## Пропозиції до словників
- `+trigger:bump` — гравець «входить» у клітину зайнятої сутності (бій, двері, NPC) — у роглайках це основний тригер, ширший за `contact`.
- `+cond:can_damage` — ATK героя > DEF монстра (інакше бій неможливий).
- `+effect:fight` — розрахувати бій формулою й застосувати результат (атомарний ефект); `+effect:stat(a, ±n)` — змінити характеристику (ATK/DEF), бо `hp(±n)` не покриває.
- `+role:npc-merchant` — NPC, що торгує/дарує (або вжити ⏳ `neutral`).
- `+ui:damage-preview`, `+ui:critical-value` — див. картки.
- `+window:codex-window` (⏳, тут еталон: книга монстрів), `+window:floor-select` — вибір поверху для телепорту, `+window:save-slots` (⏳).
- `+feature:replay`, `+feature:level-editor` (⏳) — вжито.
- `+axis:random=none-rpg` — нагадування: RPG-бій без рандому — значення `none` тут ключове для жанру.

## Джерела
- ⭐ [mota-js: functions.js (getDamageInfo)](https://raw.githubusercontent.com/ckcz123/mota-js/master/project/functions.js) — точна формула бою: раунди, хто бʼє першим, спец-здібності, щит, монета ×2.
- [mota-js: element.md](https://raw.githubusercontent.com/ckcz123/mota-js/master/_docs/element.md) — ключі/двері, зілля/самоцвіти з множником області, кирка/бомба/транспортер/книга монстрів, список спец-здібностей.
- [mota-js на GitHub](https://github.com/ckcz123/mota-js) — рушій, гарячі клавіші, реплеї.
- [H5魔塔广场](https://h5mota.com/) — 2000+ веж, рейтинги, редактор, навчальна вежа.
- [zh.wikipedia: 魔塔](https://zh.wikipedia.org/wiki/%E9%AD%94%E5%A1%94) — Tower of the Sorcerer (1996), порти.
- [Steam: Tactical Nexus](https://store.steampowered.com/app/1141290/Tactical_Nexus/) · [Steam: DungeonUp](https://store.steampowered.com/app/388620/DungeonUp/) — сучасні нащадки.

## Непевне
- (?) Механіка оригіналу 1996 (розмір поверху 11×11, кількість поверхів, точний набір предметів і цін вівтаря) — описано за китайською традицією та рушієм H5; оригінальні сторінки (wwajp.com) агенту недоступні.
- (?) «Ціна вівтаря росте з кожною покупкою» — з памʼяті (新新魔塔); рушій лише згадує глобальні крамниці.
- (?) Ефект хреста (十字架) у документації не описано; «посилення проти нежиті/вампірів» — з памʼяті.
- (?) DungeonUp: Steam-пошук показує 4 Sep 2015, сторінка гри — 18 Nov 2014.
- (?) Числа спец-здібностей (`坚固` — 1 шкоди за удар, `自爆` — HP → 1, `夹击` тощо) — з памʼяті; у рушії підтверджено лише формули `先攻`, `魔攻`, `2连击` і щит MDEF.
