---
title: Ring of Pain
slug: ring-of-pain
aka: []
family: roguelike
also: [board-digital]
klass: avatar
axes:
  field: 1d
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: survive
year: 2020
platforms: [PC (Windows), macOS]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/998740/", best: true, note: "Simon Boxer / Twice Different, Balor Games, 15.10.2020: опис, 16 основних данжів + 2 фінали, 15 слотів, 300+ предметів"}
  - {kind: other, url: "https://www.thesixthaxis.com/?p=366398", note: "огляд: сусіди ліворуч/праворуч, атака або підкрадання, прогноз відповіді ворога, кілька виходів, Dungeon of the Day"}
  - {kind: other, url: "https://steamah.com/ring-of-pain-strategy-for-hard-difficulty/", note: "гайд: роль Speed/Attack/Defense/Clarity/Stealth, крамниці на 3 і 6 рівні, проклятий буст"}
  - {kind: other, url: "https://gamepretty.com/ring-of-pain-tips-tricks-for-winning/", note: "поради: кристали перетасування, бічні кімнати, мімік-крамниці, ріроли за душі"}
  - {kind: other, url: "https://www.gamegrin.com/reviews/ring-of-pain-review", note: "огляд: Speed — черговість, залякування, сети спорядження, фінал-гаунтлет"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ring+of+Pain+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, item-pickup, inventory-items, inventory-limit, status-effects, player-death, permadeath, dungeon-generation, sequential-levels, round-currency, shop-between-levels, shop-catalog, run-relics, chase-player, explode-area, projectile-shot, daily-puzzle, leaderboard, cell-click, wrap-edges, +ring-field, +stealth-sneak, +speed-initiative, +combat-preview, +item-set-bonus, +reroll-for-currency, +branching-exits]
proposes: ["+axis:field=ring", "+trigger:bump", "+cond:faster(a, b)", "+cond:stealth_roll(a)", "+effect:fight(a, b)", "+effect:stat(a, name, ±n)", "+effect:shuffle(field)", "+effect:reroll(options)", "+role:card", "+ui:combat-preview", "+window:exit-choice", "+card:stealth-sneak", "+card:speed-initiative"]
author: opus
date: 2026-11-09
---

# Ring of Pain — данж як кільце карт: бачиш лише двох сусідів, ліворуч і праворуч, і щокроку обираєш — бити чи прослизнути

## Суть
Кімната підземелля — **кільце карт**: монстри, скарби, зілля, буст-стати, крамниці-міміки й вихід. Гравець стоїть у кільці й має справу лише з **двома сусідніми картами** — ліворуч і праворуч; рух кільцем — по одній карті в бік. З монстром можна битись (першим бʼє швидший, видно, скільки HP забере відповідь) або **підкрастися повз** (шанс Stealth; не вдалось — монстр бʼє). Мета — дійти через 16 основних данжів до одного з двох фіналів (світло/темрява), збираючи спорядження з наборами-бонусами. Охоплення «карткової» межі — див. також [card-dungeons](card-dungeons.md), [donsol](donsol.md).

## Поле і час
- Поле — цикл карт (`field: 1d` з замиканням; для корпусу — кандидат `+axis:field=ring`). Більша кімната — більше кільце.
- Видно лише сусідні карти повністю; решта кільця — за туманом/віддалена (`info: partial`) (?).
- Покроково: дія гравця (крок, атака, вжити предмет) → реакція монстрів (атака сусідніх, рух рухомих) (?).
- Випадковість: генерація кімнат і вмісту (`setup`) + шанс підкрадання, парирування, рівність Speed 50/50 (`runtime`). Dungeon of the Day — фіксований порядок карт для всіх.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | Health, Attack, Defense, Speed, Stealth (старт 23%), Clarity; душі; 15 слотів | крок кільцем ліворуч/праворуч; діє на сусідню карту |
| Монстр | enemy | HP, ATK, DEF, Speed, душі | бʼє, коли герой поруч/проходить повз (?) |
| Рухомий монстр (переслідувач) | enemy | — | рухається кільцем до героя |
| Вибуховий монстр | enemy | — | вибухає, шкодить сусідам; можна підірвати здалеку |
| Стрілець | enemy | дальність | бʼє здалеку, не лише як сусід |
| Злодій-втікач | enemy | — | тікає до скарбу/предмета (?) |
| «Залякувач» | enemy | Speed | не можна атакувати, якщо твій Speed не більший |
| Бос | boss | 500 HP (фінальний), спавн | спавнить монстрів, що полюють на героя |
| Предмет / спорядження | pickup | слот, сет | стати, пасивки; комбінації сету дають пасив |
| Буст статів | pickup | базовий / компроміс / спеціалізований / проклятий | постійна зміна статів (проклятий — з мінусом) |
| Зілля | pickup | лікування / прокляте | лікує (Clarity підсилює); прокляте — з побічною дією |
| Скриня | container | ранг (золота, епічна) | відкрити за душі (?) → предмет |
| Мімік-крамниця | neutral | ціна в душах | продає спорядження; ріроли за душі |
| Сова (Owl) | neutral | — | дарує предмети/вибір, говорить загадками; в одній кімнаті — ворог |
| Тінь (The Dark) | neutral | — | зʼявляється при виході, теж дарує |
| Кристал перетасування | pickup | — | перетасовує кільце (вихід з блоку) |
| Сувій / книга заклять | pickup | cooldown (книга) | одноразова / перезаряджувана дія |
| Вихід | static | вид: основний / бічна кімната / роздоріжжя | перехід у наступну кімнату; кілька виходів — різні гілки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(hero, dir)` кільцем на одну карту; `wrap` по колу.
- КОЛИ `input(dir)` → ЯКЩО `adjacent(hero, monster)` → ТО `custom: «спроба підкрастися повз»`: ЯКЩО `prob(stealth)` → прохід без шкоди; інакше `damage(hero, n)` один удар монстра.
- КОЛИ `input(monster)` → ЯКЩО `custom: «монстр-залякувач і Speed героя ≤ його Speed»` → ТО `block` (атакувати не можна).
- КОЛИ `input(monster)` → ТО бій: ЯКЩО `custom: «Speed героя > Speed монстра»` → герой бʼє першим; рівні — `prob(50)`; інакше першим монстр.
- КОЛИ `custom: «удар»` → ТО `damage(target, max(1, ATK − DEF))` — навіть коли DEF ≥ ATK, проходить 1.
- КОЛИ `custom: «монстр бʼє героя»` → ЯКЩО `custom: «DEF героя > ATK монстра»` and `prob(p)` → ТО `custom: «парирування»`: шкоди нема, `stun(monster, 1)`.
- КОЛИ `hp_zero(monster)` → ТО `disappear(monster)`, `currency(+souls)`; карти за ним зсуваються ближче.
- КОЛИ `input(item)` → ЯКЩО `custom: «є вільний слот з 15»` → ТО `pickup(hero, item)`; інакше `choose(replace)`.
- КОЛИ `picked(hero, item)` → ЯКЩО `custom: «зібрано кілька частин сету»` → ТО `set_state(hero, set_bonus)`.
- КОЛИ `input(potion)` → ТО `heal(hero, n + clarity_bonus)`; прокляте — ще й `custom: «мінус до стату»`.
- КОЛИ `input(stat_boost)` → ТО `choose(options)` → `custom: «стати ±n»`.
- КОЛИ `input(mimic)` → ЯКЩО `count(souls, >=, price)` → ТО `currency(-price)`, `give(hero, item)`; `custom: «ріроль за душі»`.
- КОЛИ `input(shuffle_crystal)` → ТО `custom: «перетасувати кільце»`.
- КОЛИ `died(exploder)` → ТО `explode(adjacent, 1)`.
- КОЛИ `tick` → ЯКЩО `custom: «монстр-переслідувач»` → ТО `move(monster, toward_hero)`.
- КОЛИ `input(exit)` → ТО `next_level` (основний вихід — глибше; бічний — додаткова кімната; роздоріжжя — вибір гілки).
- КОЛИ `hp_zero(hero)` → ТО `lose` (permadeath, новий забіг).
- Перемога: пройти 16 данжів і фінал (бос світла або гаунтлет із пʼяти темряви — чи навпаки (?)). Поразка: HP = 0. Рахунок: глибина/перемога; у Dungeon of the Day — глобальна таблиця.

## Керування і ввід
- Миша/геймпад: стрілки з боків екрана — крок ліворуч/праворуч кільцем; клік по сусідній карті — атака/взяти/відкрити.
- Наведення на монстра — прогноз: скільки HP втратиш на відповіді.
- Інвентар — клік по предмету для використання (сувій, книга з cooldown).

## Вікна, меню, HUD
- `game-screen` — кільце карт, дві сусідні збоку від героя, `stat-panel` (HP, ATK, DEF, Speed, Stealth, Clarity), душі, `inventory-bar` на 15 слотів, `combat-preview` на монстрі.
- `shop-window` — мімік-крамниця й крамниця кожні 3 рівні (ріроль за душі).
- `upgrade-window` — вибір буста статів / дару сови.
- `dialogue-window` — сова й тінь (загадки, вірші).
- `exit-choice` (?) — коли в кімнаті кілька виходів.
- `daily-window` — Dungeon of the Day; `leaderboard` — глобальна таблиця дня.
- `main-menu` → `character-select`/вибір стартового предмета (свічка тощо) (?) → `game-screen`; смерть → `end-screen`.

## Фічі поза полем
- `mode-daily` + `leaderboard-online` — однаковий данж для всіх, одна оптимальна траса.
- `unlockables` — предмети відкриваються з прогресом (180 / 300+ — джерела розходяться); стартові предмети (подвійна свічка, темний камінь) відкриває перемога на шляху світла/темряви.
- `difficulty-presets` — є hard-рівень (?).
- `codex` — колекція предметів і монстрів (?).

## Варіації й родичі
- Родичі: [donsol](donsol.md) і [card-dungeons](card-dungeons.md) (данж з карт: Scoundrel, Card Crawl), [one-way-heroics](one-way-heroics.md) (обмежений рух одним напрямком), [desktop-dungeons](desktop-dungeons.md) (детермінований прогноз бою).
- Черга сімʼї вважала межовим (`board-digital`); тут — `roguelike` з `also: board-digital`, бо ядро — рух героя кільцем і бій.
- Осі варіацій: **поле** (рядок кімнати — Donsol / кільце — Ring of Pain / сітка — Card Crawl (?)) · **видимість** (уся кімната / лише сусіди) · **черговість бою** (герой завжди першим / за Speed) · **ухилення** (втеча з кімнати / підкрадання повз кожного).

## Цікавинки для курсу
- Кільцеве поле: індекс по модулю, дві «активні» клітини — сусіди героя — 🌱.
- Бій з ініціативою за Speed і мінімальною шкодою 1 — 🌱; парирування з шансом і оглушенням — 📎.
- Підкрадання повз монстра як ризикований хід (шанс Stealth, провал = удар) — 🌱.
- Прогноз відповіді ворога перед атакою (симуляція бою без застосування) — 📎.
- Сети спорядження: бонус за N частин одного набору — 📎.
- Граф данжів з основними, бічними й роздоріжними виходами та двома фіналами — 🥉.
- Daily-сід + глобальний лідерборд — 🥉.

## Мапа на каталог
- Є: `hp-damage` · `item-pickup` · `inventory-items` · `inventory-limit` (15) · `status-effects` · `player-death` · `permadeath` · `dungeon-generation` · `sequential-levels` · `round-currency` (душі) · `shop-between-levels` · `shop-catalog` · `run-relics` · `chase-player` · `explode-area` · `projectile-shot` (стрільці) · `daily-puzzle` · `leaderboard` · `cell-click` · `wrap-edges` (кільце).
- **Нема** → пропозиції карток:
  - `+ring-field` «Поле-кільце, видно лише сусідів» · field/topology · 🌱.
  - `+stealth-sneak` «Прослизнути повз ворога з шансом» · entities/combat · 🌱 · слот {stealth}.
  - `+speed-initiative` «Першим бʼє швидший» · entities/combat · 🌱.
  - `+combat-preview` «Прогноз втрат до бою» · interface/hud · 📎 (родич `+damage-preview` з [magic-tower](magic-tower.md)).
  - `+item-set-bonus` «Бонус за набір предметів» · progression/items · 📎.
  - `+reroll-for-currency` «Переграти пропозицію крамниці за валюту» · economy/shop · 🌱.
  - `+branching-exits` «Кілька виходів у різні гілки» · levels/progress · 🌱.

## Пропозиції до словників
- `+axis:field=ring` — поле-цикл (Ring of Pain); зараз лише `1d` + `wrap`.
- `+trigger:bump` — рух/дія в клітину, зайняту сутністю.
- `+cond:faster(a, b)` — Speed A > Speed B (ініціатива, залякування).
- `+cond:stealth_roll(a)` — успіх перевірки скритності (окремо від загального `prob`, бо шанс — стат).
- `+effect:fight(a, b)` — атомарний бій з черговістю й відповіддю.
- `+effect:stat(a, name, ±n)` — змінити стат (ATK/DEF/Speed/Stealth).
- `+effect:shuffle(field)` — перетасувати поле (кристал).
- `+effect:reroll(options)` — замінити пропозиції вибору новими.
- `+role:card` — карта-сутність на картковому полі.
- `+ui:combat-preview` — скільки HP забере бій, на ворогові.
- `+window:exit-choice` — вибір гілки на роздоріжжі.
- `+card:stealth-sneak`, `+card:speed-initiative` — див. картки.

## Джерела
- ⭐ [Steam: Ring of Pain](https://store.steampowered.com/app/998740/) — офіційний опис: «encounters come to you», бій/підкрадання, 15 слотів, 300+ предметів, 16 данжів + 2 фінали, 25+ спецданжів, міміки.
- [TheSixthAxis: огляд](https://www.thesixthaxis.com/?p=366398) — сусіди ліворуч/праворуч, провал підкрадання, прогноз відповіді, кілька виходів, сова й тінь, бос 500 HP, Dungeon of the Day.
- [SteamAH: стратегія hard](https://steamah.com/ring-of-pain-strategy-for-hard-difficulty/) — пороги статів, Clarity → лікування, крамниці 3/6 рівня, свічка/темний камінь.
- [GamePretty: поради](https://gamepretty.com/ring-of-pain-tips-tricks-for-winning/) — кристали перетасування, бічні кімнати, роздоріжжя, сувої й книга з cooldown.
- [GameGrin: огляд](https://www.gamegrin.com/reviews/ring-of-pain-review) — Speed і черговість, залякування, сети, фінал.

## Непевне
- (?) Стаття Wikipedia з черги (`W:Ring_of_Pain`) не існує (404) — у шапку не покладено.
- (?) Чи видно далекі карти кільця, чи лише сусідні; як саме кільце «підсувається» після зникнення карти.
- (?) Черговість ходу монстрів (бʼють усі сусіди після кожної дії героя чи лише при проході повз).
- (?) Формула `max(1, ATK − DEF)` — з гайду (приклад 4 ATK проти 2 DEF = 2, DEF > ATK = 1); шанс парирування — невідомий.
- (?) Залякування: в одному джерелі — риса монстра (не атакуєш швидшого), в іншому — стат героя «для виживання».
- (?) Кількість предметів: 300+ (Steam) проти 180 (огляд TheSixthAxis, ймовірно на старті).
- (?) Який фінал — бос, а який — гаунтлет із пʼяти; консольні порти (Steam-сторінка їх не згадує).
- (?) Чи скрині відкриваються за душі; заморожування ворогів предметами — лише згадка в огляді.
