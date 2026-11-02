---
title: Desktop Dungeons
slug: desktop-dungeons
family: roguelike
also: [hidden-deduction, thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: setup
  goal: state
year: 2013
platforms: [PC, Mac, Linux, iOS, Android]
links:
  - {kind: wiki, url: "https://www.qcfdesign.com/wiki/DesktopDungeons/index.php?title=Strategy", best: true, note: "DDwiki (видавця): «чорне поле — це мана і здоровʼя», бос-фази, level-up-лікування"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Desktop_Dungeons", note: "історія: альфа 2010, реліз 2013, Rewind 2023, IGF 2011"}
  - {kind: wiki, url: "https://www.qcfdesign.com/wiki/DesktopDungeons/index.php?title=Monsters", note: "формули атаки/HP монстрів 1–10, 38 монстрів на данж"}
  - {kind: wiki, url: "https://www.qcfdesign.com/wiki/DesktopDungeons/index.php?title=Glyphs", note: "усі гліфи з вартістю мани"}
  - {kind: wiki, url: "https://www.qcfdesign.com/wiki/DesktopDungeons/index.php?title=Gods", note: "боги, побожність, навернення, осквернення"}
  - {kind: play, url: "https://qcf-design.itch.io/desktop-dungeons", note: "itch.io: завантаження (безкоштовно)"}
  - {kind: steam, url: "https://store.steampowered.com/app/226620", note: "Enhanced Edition; Daily Dungeon"}
  - {kind: official, url: "http://www.desktopdungeons.net/"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=desktop+dungeons+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cell-click, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, dungeon-generation, shop-catalog, round-currency, destroy-all-enemies, player-death, level-unlock, daily-puzzle, temporary-modes, cell-transform, teleport-random-exit, +exploration-regen, +level-up-heal, +deterministic-combat, +strike-order, +xp-level-bonus, +god-piety, +item-conversion, +kingdom-meta, +static-enemies]
proposes: ["+trigger:revealed", "+trigger:level_up", "+cond:level_cmp", "+cond:piety", "+effect:heal_full", "+effect:convert", "+effect:piety", "+role:boss", "+role:altar", "+ui:combat-preview", "+ui:monster-level-badge", "+window:inventory-window", "+window:god-window", "+window:kingdom-map", "+window:character-select", "+feature:meta-progression", "+feature:puzzle-bank", "+axis:control=indirect"]
author: opus
date: 2026-11-02
---

# Desktop Dungeons — роглайк на один екран: нерозкриті клітини — це твоє здоровʼя

## Суть
Герой обраної раси й класу стоїть у випадковому данжі на одному екрані, вкритому чорним «туманом»; треба вбити боса (монстра 10-го рівня). Ключова механіка — **розкриття клітин відновлює HP і ману** (і ворогам теж), тож нерозкрите поле — скінченний ресурс, який витрачаєш між боями; підвищення рівня повністю лікує. Монстри стоять на місці й не нападають самі, бій детермінований — гра стає логістичною головоломкою «кого вбити в якому порядку». Забіг ≈ 10 хвилин.

## Поле і час
- Одне поле на весь екран, квадратна сітка (класично 20×20 (?)): стіни, підлога, монстри, предмети, вівтарі, крамниці; камера статична.
- Невідкриті клітини чорні; розкриваються в радіусі навколо героя при ході (`info: hidden`), монстри з'являються з рівнем на іконці.
- **Час рухається лише розкриттям і боєм**: ходити по відкритому — безкоштовно, і ні гравцю, ні монстрам нічого не відновлюється. Одне розкриття клітини = «тік» регенерації для всіх поранених.
- 38 звичайних монстрів рівнів 1–9 + бос(и) рівня 10; поле генерується на старті (`random: setup`), далі все детерміновано (крім Dodge-шансів).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | раса, клас, рівень 1–10, HP/maxHP (+10 за рівень), MP, атака (5×рівень), XP, золото, 5–6 слотів інвентаря (?) | клік по клітині — іде найкоротшим шляхом; клік по монстру — обмін ударами |
| Монстр рівня n | enemy | атака n(n+5)/2, HP n(n+6)−1, тип + риси | стоїть на місці; відповідає ударом, якщо вижив; регенерує при розкритті клітин |
| Риси монстрів | — | First Strike, Poisonous, Mana Burn, Cursed, Magical attack, Undead, Retaliate, Blinks, Fast regen | змінюють порядок ударів і наслідки бою |
| Бос | boss | рівень 10+, сильніші риси | ціль данжу |
| Рослина | enemy | не дає XP (?) | блокує прохід; Earthmother забороняє вбивати |
| Стіна | static | руйнівна | ENDISWAL/PISORF руйнують; IMAWAL створює |
| Чорна клітина | terrain | нерозкрита | при розкритті: +HP і +MP герою, +HP пораненим монстрам |
| Гліф | pickup | займає слот, вартість мани | закляття (таблиця нижче) |
| Зілля HP / MP | pickup | — | лікує/відновлює ману (запас на боса) |
| Бустери (атака/HP/мана) | pickup | — | постійні +10 % атаки / +HP за рівень / +max MP |
| Золото | pickup / resource | — | для крамниць і мета-королівства |
| Крамниця | static | товар і ціна | купити предмет за золото |
| Вівтар бога | static | бог | крок — почати поклоніння / просити дари / навернутися / осквернити |
| Блискітки біля вівтаря | pickup | колір бога | +1 побожність |
| Калюжа крові | terrain | — | випити — бонус для Dracul |

Гліфи (мана): BURNDAYRAZ 6 — вогняна куля 4×рівень · PISORF 4 — відкинути монстра (у стіну — шкода й руйнування) · ENDISWAL 6 — зруйнувати стіну · IMAWAL 5 — перетворити монстра на стіну (3 — стіна на порожній) · GETINDARE 3 — First Strike на наступний удар · HALPMEH 5 — лікування 4×рівень, знімає отруту · BYSSEPS 2 — +30 % наступного удару · LEMMISI 2 — розкрити 3 випадкові клітини · WEYTWUT 8 — обмін місцями з монстром + сповільнення · WONAFYT 5 — притягнути монстра рівня ≤ твого · APHEELSIK 5 — отрута (блокує регенерацію) · CYDSTEPP 10 — захист від смерті (лишається 1 HP) · BLUDTUPOWA 0 — 3 HP×рівень за розкриття 3 клітин з маною.

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click cell)` → ЯКЩО `reachable(cell)` → ТО `move(hero, path)` (без витрати часу).
- КОЛИ `revealed(cell)` → ТО `heal(hero, hp_per_tile)`, `custom: «+1 MP»`, `heal(each injured monster, regen)` (ЯКЩО `not state(hero, poisoned)` — для героя HP).
- КОЛИ `input(click monster)` → ТО бій: порядок ударів — `custom: «First Strike > вищий рівень > рівні рівні — монстр першим»`; кожен бʼє один раз: `damage(atk − reduction)`; той, хто вижив, отримує удар у відповідь.
- КОЛИ `hp_zero(monster)` → ТО `disappear_b`, `counter(xp, +monster_level + bonus)`, де `bonus = n(n−1)+2` для n = рівень монстра − рівень героя > 0.
- КОЛИ `counter(xp, >=, 5×level)` → ТО `custom: «level +1»`, `heal_full(hero)` (HP і MP), `custom: «atk +5, maxHP +10»`; максимум 10-й рівень.
- КОЛИ `hp_zero(hero)` → ЯКЩО `state(hero, death_protection)` → ТО `hp(hero, =1)`; інакше `lose`.
- КОЛИ `input(cast glyph)` → ЯКЩО `count(mp, >=, cost)` → ТО ефект гліфа, `counter(mp, −cost)`.
- КОЛИ `input(drop on convert)` (предмет/гліф) → ТО `convert(item)`: предмет зникає, `counter(conversion_points, +n)` (гліф = 100) → бонус за расою, деяким богам — `piety(+)`.
- КОЛИ `contact(hero, altar)` → ЯКЩО `no god` → ТО `custom: «поклоніння»`, стартовий бонус бога; ЯКЩО інший бог і `piety(>=50)` → ТО навернення: `piety(÷2)`.
- КОЛИ дія, що подобається богу (вбивство, каст, перетворення…) → ТО `piety(+n)` (0…100); КОЛИ заборонена дія → ТО `piety(−fine)`; ЯКЩО не вистачає → ТО `custom: «кара бога»`.
- КОЛИ `input(request boon)` біля свого вівтаря → ЯКЩО `piety(>= cost)` → ТО `give(hero, boon)`, `piety(−cost)` (багаторазові дорожчають).
- КОЛИ `input(desecrate altar)` → ТО `piety(+30)`, 3 індульгенції, кара власника вівтаря, вівтар зламано.
- КОЛИ `contact(hero, shop)` → ЯКЩО `count(gold, >=, price)` і є слот → ТО `give(hero, item)`.
- КОЛИ `died(boss)` → ТО `win`, `currency(gold → kingdom)`.
- Перемога: убити боса (бос-фаза: лікуватись level-up-ами на дрібних монстрах, потім витрачати зілля). Поразка: HP героя = 0. Рахунок: перемога/поразка + золото й прогрес у королівстві; окремі виклики класів.

## Керування і ввід
- Лише миша/тач: клік по клітині — іти туди (автошлях, `control: indirect`); клік по монстру — атака; наведення — прогноз бою.
- Клік по гліфу/зіллю в інвентарі — застосувати; гліфи з ціллю — потім клік по монстру/клітині.
- Перетягти предмет на «конвертер» — перетворити; кнопки дарів бога у вікні релігії.

## Вікна, меню, HUD
- `game-screen` — поле + бічна панель: портрет, `level-number`, `hp-bar`, `energy-bar` (MP), `xp`-смужка, атака, золото, побожність, `inventory-bar` (слоти гліфів і предметів), `combat-preview` (наведення на монстра: хто виживе, скільки шкоди), `monster-level-badge` на кожному монстрі.
- `god-window` — бог, побожність, список дарів з цінами, що бог любить/ненавидить.
- `kingdom-map` — місто королівства: будівлі (гільдії класів і рас), входи в данжі, крамниці підготовок.
- `character-select` — вибір раси й класу (розблоковані будівлями).
- `end-screen` — перемога/смерть, золото до королівства.
- `level-select` — набір данжів/квестів і `puzzle-select` (пазл-данжі з фіксованою розстановкою).
- `settings-window`, `main-menu`.
- Переходи: `main-menu` → `kingdom-map` → данж → `character-select` → `game-screen` → `end-screen` → `kingdom-map`.

## Фічі поза полем
- `meta-progression` — королівство: золото з данжів → будівлі → нові класи, раси, данжі, «підготовки» (переваги на наступний забіг), сховище предметів між забігами.
- `level-unlock`, `achievements` (badges, класові виклики), `puzzle-bank` (Puzzles — фіксовані данжі з одним розвʼязком), `mode-daily` (Daily Dungeon / D.E.R.P. з однаковим seed для друзів).
- Desktop Dungeons: Rewind (2023) — 3D-ремейк з **undo/rewind** (`undo`).
- `custom-skins` — тайлсети від спільноти (Derek Yu став стандартним).

## Варіації й родичі
- Rewind — та сама гра з відкатом ходів; вільна альфа 2010 (GameMaker) — коротша версія без королівства.
- Родичі: 868-HACK, Hoplite (детермінований мікророглайк), Magic Tower (детермінований бій, порядок вбивств — ядро), Dungelot (відкривати клітини), Minesweeper (розкриття як ресурс/ризик).
- Осі варіацій: **регенерація** (за хід / за розкриту клітину / за рівень) · **вороги** (стоять / ходять) · **бій** (кидок / формула) · **порядок удару** (завжди гравець / за рівнем / за рисою).

## Цікавинки для курсу
- Регенерація за розкриту клітину (і ворогам теж) — туман як витратний ресурс — 📎 (одна подія `revealed` → кілька ефектів).
- Детермінований бій з порядком ударів за рівнем/рисою + прогноз результату при наведенні — 🥉 (симуляція бою без побічних ефектів).
- Level-up = повне лікування: «steamroll» — вбивати дрібних посеред бою з босом — 🌱 (правило), але гарна задача на баланс.
- Формули монстрів n(n+5)/2 і n(n+6)−1, XP з бонусом n(n−1)+2 — 🌱 (табличні дані, тест на функції).
- Боги з «любить/ненавидить», побожність, дари, навернення, осквернення — 🥈 (система реакцій на події гри — шина подій).
- Гліфи як інвентарні закляття, що займають слот, і конверсія предметів у бонуси раси — 📎.
- Розвʼязувач: «чи можна пройти данж» перебором порядку вбивств — 🥇 (пошук у просторі станів з ресурсами).

## Мапа на каталог
- Є: `cell-click` · `hp-damage` · `inventory` + `inventory-items` + `inventory-limit` · `item-pickup` · `dungeon-generation` · `shop-catalog` · `round-currency` · `destroy-all-enemies` (≈ убити боса) · `player-death` · `level-unlock` · `daily-puzzle` · `temporary-modes` (бафи на наступний удар) · `cell-transform` (IMAWAL, ENDISWAL) · `teleport-random-exit` (WONAFYT, WEYTWUT — близько).
- **Нема** → пропозиції карток:
  - `+exploration-regen` «Розкриття клітини лікує (гравця і ворогів)» · entities/state · 📎 · слоти {hp_per_tile, mp_per_tile}.
  - `+level-up-heal` «Підвищення рівня — повне лікування» · entities/state · 🌱.
  - `+deterministic-combat` «Бій за формулою без кидків» · entities/combat · 📎 · слоти {formula}.
  - `+strike-order` «Хто бʼє першим: рівень/риса» · entities/combat · 🌱.
  - `+xp-level-bonus` «XP за рівнем ворога з бонусом за сильнішого» · entities/state · 🌱.
  - `+god-piety` «Бог: побожність, дари, заборони» · rules/meta · 🥈.
  - `+item-conversion` «Перетворити предмет на бонус» · entities/interact · 📎.
  - `+kingdom-meta` «Місто між забігами, будівлі відкривають контент» · interface/menus · 🥉.
  - `+static-enemies` «Вороги стоять, бій лише з ініціативи гравця» · entities/move · 🌱.

## Пропозиції до словників
- `+trigger:revealed` — клітину розкрито вперше (тут — головний тік регенерації); `+trigger:level_up` — рівень підвищено.
- `+cond:level_cmp` — порівняння рівнів сутностей (порядок удару, бонус XP); `+cond:piety` — побожність ≥ N.
- `+effect:heal_full` — повне відновлення HP/MP; `+effect:convert` — знищити предмет за бонус; `+effect:piety` — ±побожність.
- `+role:boss` — ⏳, вжито; `+role:altar` — клітина, що відкриває систему (бог), а не просто `static`.
- `+ui:combat-preview` — прогноз бою при наведенні; `+ui:monster-level-badge` — рівень на іконці ворога.
- `+window:inventory-window` (⏳), `+window:god-window` — сторінка бога; `+window:kingdom-map` — мета-місто; `+window:character-select` (⏳).
- `+feature:meta-progression` (⏳), `+feature:puzzle-bank` (⏳) — вжито.
- `+axis:control=indirect` — клік → автошлях як єдиний режим руху.

## Джерела
- ⭐ [DDwiki: Strategy](https://www.qcfdesign.com/wiki/DesktopDungeons/index.php?title=Strategy) — «чорний простір — це мана й здоровʼя», регенерація монстрів, level-up-лікування, бос-фази.
- [DDwiki: Health and Attack](https://www.qcfdesign.com/wiki/DesktopDungeons/index.php?title=Health_and_Attack) — регенерація за клітину, level-up, атака 5×рівень.
- [DDwiki: Strike Order](https://www.qcfdesign.com/wiki/DesktopDungeons/index.php?title=Strike_Order) · [Level](https://www.qcfdesign.com/wiki/DesktopDungeons/index.php?title=Level) · [Monsters](https://www.qcfdesign.com/wiki/DesktopDungeons/index.php?title=Monsters) · [Glyphs](https://www.qcfdesign.com/wiki/DesktopDungeons/index.php?title=Glyphs) · [Gods](https://www.qcfdesign.com/wiki/DesktopDungeons/index.php?title=Gods) — формули й таблиці.
- [Wikipedia](https://en.wikipedia.org/wiki/Desktop_Dungeons) — історія, Rewind, IGF.
- [itch.io](https://qcf-design.itch.io/desktop-dungeons) · [Steam](https://store.steampowered.com/app/226620) — грати.

## Непевне
- (?) Розмір поля 20×20 — з памʼяті, у знайдених джерелах не названо.
- (?) Скільки HP дає клітина: DDwiki — «1 unit health і 1 mana за клітину»; у класиці, наскільки памʼятаю, HP = рівень героя за клітину — «unit», можливо, саме це.
- (?) Кількість слотів інвентаря, прогноз бою при наведенні, «рослини без XP», бонуси конверсії за расами — з памʼяті.
- (?) Деталі королівства (які будівлі що відкривають) — DDwiki-сторінки Buildings/Settlements не читав.
