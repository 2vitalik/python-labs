---
title: Kroz
slug: kroz
aka: [Kingdom of Kroz, Caverns of Kroz, Dungeons of Kroz, The Lost Adventures of Kroz, Super Kroz Trilogy]
family: maze-arcade
also: [roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 1987
platforms: [DOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kroz", best: true, note: "серія, епізоди й кількість рівнів, самоцвіти як здоровʼя, батоги, shareware-модель"}
  - {kind: other, url: "https://github.com/tangentforks/kroz", note: "усі епізоди + вихідний код Turbo Pascal (GPL, 2009)"}
  - {kind: other, url: "https://raw.githubusercontent.com/tangentforks/kroz/master/source/LOSTKROZ/MASTER/LOST5.MOV", note: "код: процедура Move — що робить кожна клітина, тексти повідомлень"}
  - {kind: other, url: "https://raw.githubusercontent.com/tangentforks/kroz/master/source/LOSTKROZ/MASTER/LOST1.LEV", note: "код: таблиця 83 типів обʼєктів і символів, очки"}
  - {kind: other, url: "https://sfprod.shikadi.net/games/kroz.htm", note: "чіти, стартові самоцвіти 10/3/0 за складністю"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kingdom+of+kroz+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-8dir, move-by-input, chase-greedy, hp-damage, item-pickup, inventory, inventory-items, key-and-door, destructible-blocks, impassable-cells, teleport-random-exit, teleport, spawner-entity, temporary-modes, explode-area, push-object, gravity-fall, ladder-climb, environment-death, sequential-levels, dungeon-generation, save-multi-slot, difficulty-levels, cheat-codes, event-points, score-records, leaderboard, console-render, status-panel, message-log, +gems-as-health, +whip-adjacent-attack, +monster-steals-item, +lure-into-breakable, +spreading-terrain, +trigger-reveals-hidden, +spell-opens-walls, +bonus-letter-sequence, +first-touch-message, +sideways-gravity-level]
proposes: ["+effect:spread", "+role:spell", "+ui:message-line", "+feature:message-toggle", "+card:gems-as-health", "+card:whip-adjacent-attack"]
author: opus
date: 2026-11-09
---

# Kroz — ASCII-підземелля в реальному часі: самоцвіти — і здоровʼя, і щит; батіг — і зброя, і кайло

## Суть
Археолог спускається рівнями Kroz до сходів униз, а з усіх боків до нього повзуть монстри трьох швидкостей. Самоцвіти — це здоровʼя: монстр, що торкнувся, зникає й забирає 1–3 самоцвіти, а без самоцвітів гравець гине. Батіг бʼє все довкола, але кожен удар витрачає батіг — тим самим батогом треба й розбивати стіни на шляху до виходу. Рівень — це «енциклопедія» з ~80 типів клітин: заклинання, пастки, невидимі стіни, лава, що розтікається, тунелі, мотузки й гравітація.

## Поле і час
- Текстовий режим 80×25, 16 кольорів CGA; ігрове поле 64×23 клітини символами CP437, праворуч — панель стану.
- Рівні — заздалегідь намальовані або **випадково згенеровані** (купа монстрів і предметів, «хаотичні»); частина епізодів має прапорець перемішування рівнів.
- Real-time: монстри ходять за власними таймерами (повільні, середні, швидкі), гравець — по натисканню; гра має сповільнення, щоб працювати на будь-якому PC.
- Особливі рівні: **гравітаційні** (тягне вниз лише гравця, угору — мотузкою, тунелем чи телепортом) і **«збоку»** (угору рухатись не можна взагалі; про це пише повідомлення внизу).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (смайлик) | player | самоцвіти, батоги, телепорти, ключі, сила батога | рух у 8 напрямках, удар батогом, телепорт |
| Червоний монстр | enemy | повільний, −1 самоцвіт | крок до гравця по обох осях |
| Зелений монстр | enemy | середній, −2 | те саме, швидше |
| Синій монстр | enemy | швидкий, −3 | те саме, найшвидше |
| Рухома стіна (MBlock) | enemy | свій таймер | повзе до гравця, як монстр |
| Генератор | spawner | — | породжує повільних монстрів на порожніх клітинах; непрохідний |
| Статуя | hazard | — | непрохідна; поки є на рівні, тягне самоцвіти |
| Самоцвіт | pickup | — | +1 самоцвіт |
| Батіг | pickup | — | +1 батіг |
| Сувій телепорту | pickup | — | +1 телепорт у запас |
| Ключ | pickup | — | +1 ключ |
| Скриня | pickup | — | випадкова кількість самоцвітів і батогів |
| Мішечок (Chance) | pickup | — | 13+ самоцвітів |
| Кільце сили | pickup | — | +1 сила батога |
| Золотий самородок | pickup | — | очки |
| Скрижаль | pickup | текст рівня | очки + підказка/попередження, іноді ефект |
| Літери K, R, O, Z | pickup | порядок | зібрані по порядку → великий бонус |
| Амулет Kroz / Tome | pickup | — | фінальна ціль епізоду; великий бонус |
| Двері | gate | — | пропускає з ключем, ключ витрачається; зазвичай закриває сходи |
| Сходи | static | — | наступний рівень |
| Стіна | static | — | непрохідна |
| Ламка стіна (Block) | static | — | розбивається батогом; монстр, що врізався, гине разом із нею |
| Невидима стіна / ламка / двері | static | прихована | при дотику проявляється й блокує |
| Електрична стіна | hazard | — | дотик −1 самоцвіт; може мерехтіти (зʼявлятись/зникати) |
| Ліс, дерево | static | ріст | непрохідні; дерево проростає в сусідні порожні клітини |
| Вода (річка) | terrain | випаровування | непрохідна; на деяких рівнях висихає |
| Лава | hazard | розтікання | крок −10 самоцвітів; на деяких рівнях розтікається |
| Бездонна яма | hazard | — | смерть |
| Валун | object | — | штовхається на клітину |
| Мотузка | terrain | — | на гравітаційних рівнях можна лізти вгору |
| Тунель | terrain | — | переносить до іншого тунелю |
| Пастка-телепорт | hazard | прихована | переносить у випадкову клітину |
| Пастка «Землетрус» | hazard | — | розкидає валуни по рівню |
| Пастка «Творення» | hazard | — | спавн повільних монстрів |
| Заклинання сповільнення / прискорення / заморозки | pickup | тривалість | змінюють швидкість монстрів на час |
| Зілля сліпоти (Invisible) | pickup | тривалість | гравець стає невидимим на екрані |
| Магічна бомба | pickup | радіус | вибух довкола гравця: зносить клітини і монстрів |
| Заклинання «Zap» | pickup | до 40 | знищує випадкових монстрів |
| Сувій «Reveal Gems» | pickup | — | розкидає самоцвіти по порожніх клітинах |
| Заклинання стін (OSpell / CSpell) | switch | колір-група 1–3 | прибирає стіни своєї групи / ставить нові стіни на мітки |
| «Вибухові стіни» (BlockSpell) | switch | — | знищує всі ламкі стіни певного типу |
| «Зникнення стін» (WallVanish) | hazard | — | робить багато стін невидимими |
| Тригер-пастки (TBlock…TTree) | switch | тип | перетворюють приховані мітки на блоки, валуни, самоцвіти, батоги, золото, дерева |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir8)` → ЯКЩО `free(cell_ahead)` → ТО `move(player, dir)`; на рівні «збоку» вгору — `block`.
- КОЛИ `tick` → ЯКЩО `state(level, gravity) and not occupied(cell_under, rope)` → ТО `fall(player)`.
- КОЛИ `timer(monster_speed)` → ТО `custom: «монстр робить крок до гравця по обох осях»` (жадібна погоня, діагоналі можливі).
- КОЛИ `contact(monster, player)` → ТО `disappear(monster)`, `counter(gems, −1|−2|−3)` за кольором монстра.
- КОЛИ `counter(gems, <, 0)` → ТО `lose` («YOU HAVE DIED!!»).
- КОЛИ `input(whip)` → ЯКЩО `has(player, whip)` → ТО `take(player, whip)`, `custom: «удар по 8 сусідніх клітинах: монстри гинуть, ламкі стіни/ліс розбиваються»`; кільце сили посилює удар.
- КОЛИ `input(teleport)` → ЯКЩО `has(player, teleport_scroll)` → ТО `take(player, teleport_scroll)`, `teleport(player, random_empty)`.
- КОЛИ `contact(monster, block)` → ТО `disappear_both` — монстра заманюють у ламкі стіни.
- КОЛИ `contact(monster, pickup)` → ТО `disappear_b` — монстр зʼїдає предмет.
- КОЛИ `contact(player, gem|whip|key|teleport_scroll)` → ТО `pickup`, `score(n)`.
- КОЛИ `contact(player, chest)` → ТО `give(player, rnd gems + rnd whips)`, `message(«You found X gems and Y whips…»)`.
- КОЛИ `contact(player, door)` → ЯКЩО `has(player, key)` → ТО `take(player, key)`, `disappear_b`; інакше `block`, `message(«To pass the Door you need a Key»)`.
- КОЛИ `contact(player, stairs)` → ТО `next_level` (останній рівень → фінал).
- КОЛИ `contact(player, block|wall|forest|tree|river|generator|statue)` → ТО `block`, `message(...)`.
- КОЛИ `contact(player, invisible_wall)` → ТО `reveal(cell)`, `block`.
- КОЛИ `contact(player, electric_wall)` → ТО `counter(gems, −1)`, `block`.
- КОЛИ `enter(player, lava)` → ТО `counter(gems, −10)`; КОЛИ `enter(player, pit)` → ТО `lose`.
- КОЛИ `enter(player, tunnel)` → ТО `teleport(player, other_tunnel)`; КОЛИ `enter(player, teleport_trap)` → ТО `teleport(player, random_empty)`.
- КОЛИ `contact(player, rock)` → ЯКЩО `free(cell_behind)` → ТО `push`.
- КОЛИ `picked(player, slow_spell|speed_spell|freeze_spell)` → ТО `set_state(monsters, slow|fast|frozen, t)`.
- КОЛИ `picked(player, blind_potion)` → ТО `set_state(player, invisible, t)` — гравця не видно на екрані.
- КОЛИ `picked(player, bomb)` → ТО `explode(area, empty)` довкола гравця, `score(за монстрів)`.
- КОЛИ `picked(player, zap)` → ТО `custom: «знищити до 40 випадкових монстрів»`.
- КОЛИ `enter(player, quake)` → ТО `spawn_at(rock, random)`; КОЛИ `enter(player, create)` → ТО `spawn_at(slow_monster, random)`.
- КОЛИ `enter(player, open_spell[c])` → ТО `custom: «зникають усі стіни групи c»`; `close_spell[c]` → `set_cell(marks[c], wall)`.
- КОЛИ `enter(player, trigger[t])` → ТО `custom: «усі приховані мітки типу t стають предметом/блоком»`.
- КОЛИ `timer(generator)` → ТО `spawn_at(slow_monster, random_empty)`.
- КОЛИ `timer(lava_rate|tree_rate)` → ТО `custom: «лава/дерево займає сусідню порожню клітину»` (`+effect:spread`).
- КОЛИ `rng(1/18)` → ЯКЩО `count(statue, >, 0)` → ТО `counter(gems, −1)` (статуї тягнуть самоцвіти).
- КОЛИ `contact(player, letter)` → ЯКЩО `custom: «попередні літери K-R-O зібрані по порядку»` → ТО `score(bonus)` на Z.
- КОЛИ `contact(player, X)` → ЯКЩО `first_time` → ТО `message(опис X)` — підказка з'являється лише при першій зустрічі типу.
- Перемога: знайти амулет/скарб на останньому рівні епізоду. Поразка: самоцвіти нижче нуля, бездонна яма. Рахунок: очки за предмети і монстрів, наприкінці — бонус за кожен самоцвіт, батіг, телепорт і ключ.

## Керування і ввід
- Курсорні стрілки + Home/End/PgUp/PgDn — 8 напрямків (PCjr — U I O / J K / N M ,).
- W — удар батогом; клавіша телепорту (T (?)) — використати сувій.
- Збереження/відновлення в слоти A/B/C, пауза, вихід з підтвердженням; «−» / «+» — вимкнути/увімкнути повідомлення про предмети.
- На старті — вибір складності: Novice / Experienced / Advanced (+ прихований X — Secret Mode).

## Вікна, меню, HUD
- `splash-screen` — титул «An Apogee Software Production»; інструкції й історія — `help-window` (кілька сторінок тексту про предмети й правила).
- `difficulty-select` — Novice / Experienced / Advanced.
- `game-screen` — поле 64×23 + права панель: `score`, `level-number`, лічильники Gems / Whips (+сила) / Teleports / Keys (`status-panel`), рядок повідомлень унизу (`+ui:message-line`).
- `pause-menu` — «Press any key to resume game»; `confirm-dialog` — вихід, відновлення; `save-slots` — A/B/C.
- `end-screen` — «You have died» / фінальний підрахунок: самоцвіти, батоги, телепорти, ключі в очки.
- `leaderboard` — таблиця рекордів з рівнем, якого досяг.
- Shareware-екран — адреса автора для замовлення решти епізодів (`custom-window`).
- Переходи: splash → інструкції → difficulty-select → game-screen → (сходи) наступний рівень / (смерть) end-screen → leaderboard → «play another game?».

## Фічі поза полем
- `save-slots` (3 слоти, рекомендовано зберігатися на кожному рівні — смерть = відновитись).
- `difficulty-presets` — стартова кількість самоцвітів (у Dungeons: 10 / 3 / 0).
- `cheat-codes` — прихований режим X (Dungeons: старт із 50 самоцвітами).
- `leaderboard-local`, `levels-sequential` (25–75 рівнів на епізод), випадкові рівні між намальованими.
- `+feature:message-toggle` — вимкнути пояснення предметів.
- Shareware-модель Apogee: перший епізод безкоштовний, решта — за оплату.

## Варіації й родичі
- Епізоди: Kingdom (25 рівнів), Caverns (40), Dungeons (30), Return (20), Temple (20), Final Crusade (25), Lost Adventures (75); Kingdom of Kroz II (21). Розширення словника від епізоду до епізоду: гравітація, «збоку», мотузки, лава, що тече.
- Задум автора — «Rogue, який можна пройти»: аркадний темп замість RPG-статистики.
- Родичі в корпусі: `zzt` (той самий ASCII-світ, але з редактором і мовою обʼєктів), `chips-challenge` (енциклопедія клітин), `gauntlet` (орди, генератори), `lady-bug` / `pac-man` (жадібна погоня).
- **Осі варіацій:** здоровʼя (HP / самоцвіти-ресурс / життя); батіг (вічна зброя / витратний предмет на два призначення); гравітація рівня (нема / лише гравцю / «збоку»); вороги (за кольором-швидкістю / за поведінкою).

## Цікавинки для курсу
- Самоцвіти як здоровʼя й валюта одночасно; монстр, що вдарив, гине — 🌱.
- Витратний батіг «зброя або кайло» — дилема ресурсу — 📎.
- Монстри, що зʼїдають предмети і гинуть у ламких стінах (заманювання) — 📎.
- Розтікання лави / ріст дерев за таймером — 📎 (клітинний автомат на одному правилі).
- Групи стін, які відкриває/закриває заклинання групи — 🥉 (звʼязок «switch → множина клітин»).
- Невидимі стіни, тригери прихованих міток, «зникнення стін» — 🥉 (шар прихованого типу клітини).
- Пояснення предмета лише при першій зустрічі — 🌱 (просто, але хороший UX-прийом).

## Мапа на каталог
- Є: `move-8dir` · `chase-greedy` · `hp-damage` (самоцвіти як HP) · `item-pickup` · `inventory` + `inventory-items` (батоги, телепорти, ключі) · `key-and-door` · `destructible-blocks` · `impassable-cells` · `teleport-random-exit` · `teleport` (тунелі) · `spawner-entity` (генератор) · `temporary-modes` (сповільнення/заморозка) · `explode-area` (бомба) · `push-object` (валун) · `gravity-fall` + `ladder-climb` (мотузки) · `environment-death` (яма, лава) · `sequential-levels` · `dungeon-generation` (випадкові рівні) · `save-multi-slot` · `difficulty-levels` · `cheat-codes` · `event-points` · `score-records` + `leaderboard` · `console-render` · `status-panel` · `message-log`.
- **Нема** → пропозиції карток:
  - `+gems-as-health` «Ресурс = здоровʼя» · entities/state · 🌱 · слот {loss_per_enemy}.
  - `+whip-adjacent-attack` «Витратна атака по всіх сусідах» · entities/combat · 📎 · слот {radius}.
  - `+monster-steals-item` «Ворог зʼїдає предмет на полі» · entities/interact · 🌱.
  - `+lure-into-breakable` «Ворог гине разом з ламкою стіною» · entities/interact · 🌱.
  - `+spreading-terrain` «Клітина розростається в сусідні» · entities/state · 📎 · слот {rate}.
  - `+trigger-reveals-hidden` «Тригер перетворює приховані мітки» · entities/interact · 🥉.
  - `+spell-opens-walls` «Заклинання відкриває групу стін» · entities/interact · 📎 (дитина `button-toggle`).
  - `+bonus-letter-sequence` «Літери по порядку → бонус» · game-logic/score · 🌱.
  - `+first-touch-message` «Пояснення при першій зустрічі» · interface/hud · 🌱.
  - `+sideways-gravity-level` «Рівень з гравітацією лише для гравця» · levels/progression · 📎.

## Пропозиції до словників
- `+effect:spread` — клітина займає сусідні порожні (лава, дерева, слиз у ZZT).
- `+role:spell` — одноразовий предмет-заклинання, що діє на весь рівень (сповільнення, zap, reveal).
- `+ui:message-line` — рядок повідомлень унизу екрана.
- `+feature:message-toggle` — вимкнути пояснювальні повідомлення.
- `+card:gems-as-health`, `+card:whip-adjacent-attack` — див. вище.

## Джерела
- ⭐ [Wikipedia: Kroz](https://en.wikipedia.org/wiki/Kroz) — епізоди, рівні, самоцвіти/батоги, випадкові рівні, CGA-текст, shareware.
- [GitHub: tangentforks/kroz](https://github.com/tangentforks/kroz) — ігри і код; коментарі фанів (заманювання в стіни).
- [LOST5.MOV](https://raw.githubusercontent.com/tangentforks/kroz/master/source/LOSTKROZ/MASTER/LOST5.MOV) — процедура Move: ефект і текст кожної клітини.
- [LOST1.LEV](https://raw.githubusercontent.com/tangentforks/kroz/master/source/LOSTKROZ/MASTER/LOST1.LEV) — таблиця 83 обʼєктів, поле 64×23, очки, панель, рекорди.
- [Shikadi: Kroz](https://sfprod.shikadi.net/games/kroz.htm) — чіти, стартові самоцвіти.
- YouTube: пошук «kingdom of kroz gameplay».

## Непевне
- (?) Клавіша телепорту (T) і точна дія батога (радіус, що саме розбиває сила кільця) — у вивченому коді не знайдено.
- (?) Заклинання прискорення: повідомлення «Speed Creature spell», але опис коду неоднозначний — пришвидшує монстрів чи гравця.
- (?) Таблиця обʼєктів — з Lost Adventures (останній епізод); у Kingdom of Kroz набір менший.
- (?) Очки: тексти повідомлень (25 000, 500, 10 000) розходяться з кодом (2 500, 27, 1 000) — числа не наводжу.
- (?) Як саме статуя тягне самоцвіти: у Move — лише блок і попередження, у головному циклі — шанс 1/18 на тік.
