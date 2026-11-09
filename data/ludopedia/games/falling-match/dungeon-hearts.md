---
title: Dungeon Hearts
slug: dungeon-hearts
aka: [Dungeon Hearts DX]
family: falling-match
also: [tower-lanes, roguelike]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 2013
platforms: [PC, macOS, iOS, Wii U (DX, 2016)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dungeon_Hearts", best: true, note: "4 смуги-лінії героїв, Chargers → Striker, комбо в рядку/стовпці, сірі Striker-и ворога, рівні між боями, скидання прогресу"}
  - {kind: steam, url: "https://store.steampowered.com/app/229520/Dungeon_Hearts/", note: "Fatestream, 4 героя, ~дюжина умінь, 10 середовищ, 40+ істот і 7 босів, бонусні саундтреки"}
  - {kind: other, url: "https://ztgd.com/reviews/dungeon-hearts-pc/", note: "огляд PC: клік зливає трійку в діамант, діамант бʼє свій рядок і стовпець, статус-камені, новий забіг з 1 рівня"}
  - {kind: other, url: "https://www.gamerstemple.com/game-reviews/pc/2367/dungeon-hearts-review", note: "огляд PC: drag мишею, подвійний клік — постріл, мертвий герой сірить свої камені, бонус-етап зірок"}
  - {kind: other, url: "https://www.destructoid.com/reviews/review-dungeon-hearts/", note: "огляд PC: real-time, 4 ряди, Striker чистить шкідливе у своєму ряду, HP і мана"}
  - {kind: other, url: "https://www.pocketgamer.com/dungeon-hearts/review/", note: "огляд iOS: тап по руні кольору героя — атака, сіра руна гине від руни в тій самій смузі"}
  - {kind: other, url: "https://www.gamingnexus.com/Article/Dungeon-Hearts/Item3927.aspx", note: "огляд: підібрати й покласти фігуру на стрічку, нерухомі квадратні блоки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dungeon+hearts+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [row-conveyor, drag-drop-piece, cell-click, blast-wave, chain-detonation, combo-multiplier, hp-damage, enemy-reached-base, telegraphed-intents, status-effects, unit-xp-skills, player-death, permadeath, progress-acceleration, score-records, game-screen, end-screen, +lane-grid, +edge-spawn, +match-forms-striker, +lane-per-hero, +dead-ally-greys-tiles, +bonus-stage-levelup, +immovable-blocker]
proposes: ["+card:match-forms-striker", "+card:lane-per-hero", "+card:dead-ally-greys-tiles", "+card:bonus-stage-levelup", "+card:immovable-blocker", "+feature:bonus-stage"]
author: opus
date: 2026-11-09
---

# Dungeon Hearts — чотири смуги-конвеєри рун їдуть до героїв: склади трійку в Striker і вистрели, поки сірі атаки ворога не доїхали

## Суть
Ліворуч стоять чотири герої (воїн, маг, цілитель, лучник), праворуч — монстр; між ними «Fatestream» — чотири горизонтальні смуги, кожна належить одному героєві й безперервно зсувається ліворуч. Гравець переносить кольорові руни-«Chargers», щоб три одного кольору стали в лінію: трійка зливається в діамант-«Striker», а його активація — удар героя цього кольору; Striker-и в одному рядку чи стовпці детонують разом (комбо). Атаки монстра — сірі символи на тих самих смугах: доїхавши до лівого краю, вони бʼють героя смуги. Між боями — короткий бонус-етап рівнів; загибель усієї партії скидає забіг до нуля (роглайт).

## Поле і час
- Поле — 4 рядки (смуга = герой) × кілька видимих стовпців (?); уся сітка — конвеєр: вміст рядків їде ліворуч і зникає за лівим краєм, нові символи входять справа.
- Real-time: тиск задає швидкість стрічки й темп появи ворожих символів; рецензенти порівнюють з «highway» Guitar Hero і з Theatrhythm Final Fantasy.
- Шари: смуги з символами · ліворуч герої з HP · праворуч поточний монстр.
- Бій = один монстр; забіг = випадкова послідовність боїв у 10 середовищах (Steam), кожен наступний важчий.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Charger (кольорова руна) | tile | колір ∈ {червоний, жовтий, синій, зелений} = герой | їде ліворуч зі стрічкою; гравець переносить; 3 в лінію одного кольору → Striker |
| Striker (діамант) | tile | колір героя | активація → удар героя по монстру; вибух по своєму рядку й стовпцю знищує ворожі символи й підриває інші Striker-и |
| Готовий Striker від гри | pickup | колір | інколи приходить на стрічці одразу, без збирання трійки |
| Ворожа атака (сірий Striker, череп) | projectile | шкода | їде ліворуч; доїхала до краю → шкода герою цієї смуги; знищується Striker-ом у тому ж рядку/стовпці |
| Статус-символ ворога | hazard | кровотеча, ослаблення… | доїхав до краю → дебаф герою; знищується Striker-ом; дебаф минає після бою |
| Міцна ворожа атака | projectile | кілька ударів або певний колір | пізні вороги: звичайний Striker не знімає її з першого разу |
| Нерухомий квадратний блок | static | — | займає клітину стрічки, не переноситься |
| Сірий камінь загиблого героя | tile | — | кольорові руни загиблого стають сірими й не утворюють Striker-ів до кінця бою |
| Герой ×4 | ally | HP, мана (?), рівень, уміння | стоїть на лівому кінці своєї смуги; атакує, коли активовано Striker його кольору |
| Монстр | enemy | HP; 47 видів (Wikipedia) | праворуч; шле атаки й дебафи у смуги, кожен вид — свій стиль атак |
| Бос | boss | 7 (Steam) | особливі атаки (?) |
| Зірка бонус-етапу | pickup | колір героя | трійка зірок кольору → +1 рівень героя |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `shift(rows, left)`; КОЛИ `edge(charger)` → ТО `disappear`.
- КОЛИ `timer(every)` → ТО `spawn_at(random_symbol, right_edge)` — руни героїв, атаки й дебафи монстра.
- КОЛИ `input(drag_drop)` → ЯКЩО `free(target_cell)` → ТО `custom: «руну перенесено на вибрану клітину стрічки»`; на блок чи зайняту клітину — `block` (?).
- КОЛИ `pattern(line(3))` → ЯКЩО `same(chargers, colour)` → ТО `merge(chargers, striker)` (сама чи кліком по трійці — див. «Непевне»).
- КОЛИ `input(click_striker)` → ТО `damage(monster, n)` від героя кольору Striker-а, `explode(row+col)`.
- КОЛИ `after(explode)` → ЯКЩО `occupied(row|col, enemy_symbol)` → ТО `disappear` ворожих атак і статус-символів у рядку й стовпці.
- КОЛИ `after(explode)` → ЯКЩО `occupied(row|col, striker)` → ТО `trigger(explode)` того Striker-а, `combo(+1)`; шкода росте з числом Striker-ів, змішані кольори — бонус, атакують кілька героїв разом.
- КОЛИ `custom: «вибух зачепив міцну атаку»` → ЯКЩО `custom: «не той колір або ще не всі удари»` → ТО `custom: «атака лишається на стрічці»`.
- КОЛИ `reach(enemy_attack, left_edge)` → ТО `damage(hero_of_lane, n)`, `disappear`.
- КОЛИ `reach(status_symbol, left_edge)` → ТО `set_state(hero_of_lane, debuff)` (кровотеча, ослаблення).
- КОЛИ `hp_zero(hero)` → ТО `set_state(hero, dead)`, `transform(chargers_of_colour, grey_stone)`.
- КОЛИ `hp_zero(monster)` → ТО `clear_state(heroes, debuff)`, `respawn(dead_heroes)`, `window(custom-window)` — бонус-етап.
- КОЛИ `level_start` → ЯКЩО `mode(bonus_stage)` → ТО `custom: «густий швидкий потік зірок, ворога нема, кілька секунд»`.
- КОЛИ `pattern(line(3))` → ЯКЩО `mode(bonus_stage)` and `same(stars, colour)` → ТО `counter(hero_level, +1)`; на певних рівнях — `unlock(skill)`.
- КОЛИ `input(skill)` → ЯКЩО `custom: «уміння відкрите (і мана є?)»` → ТО `damage(monster, n)` / `heal(party, n)` / `set_state(hero, shield)` / `speed(stream, -k)` — за героєм.
- КОЛИ `level_end` → ТО `next_level`, `custom: «наступний монстр сильніший»`.
- КОЛИ `count(alive_heroes, ==, 0)` → ТО `lose`, `game_over`; рівні й уміння скидаються, новий забіг з 1 рівня.
- Перемога: фінальний бій з The Dark One (сюжет Steam) (?). Рахунок: показується в кінці гри; мета — пройти якомога далі.

## Керування і ввід
- PC: лише миша — затиснути руну, перенести, відпустити; клік (ZTGD) або подвійний клік (Gamer's Temple) по Striker-у — постріл. Скарга рецензій: миша «губить» камінь на кутах, хапається не та фігура.
- iOS: тап по руні кольору героя — атака (PocketGamer); перенесення — пальцем.
- Уміння героїв — окремі кнопки біля героїв (?).

## Вікна, меню, HUD
- `game-screen`: 4 смуги-стрічки; ліворуч `player-portraits` з `hp-bar` (і мана — ?), праворуч монстр з `hp-bar`; `ability-buttons` відкритих умінь (?).
- `custom-window` «бонус-етап»: ті самі 4 смуги, лише зірки, без ворога; відлік секунд (?).
- `end-screen` — загибель партії, `score`.
- `main-menu` — Нова гра · Продовжити (Gamer's Temple: можна вийти й продовжити) (?).
- `codex-window` (?) — Steam: перемоги відкривають шматки лору світу й героїв.
- DX (Wii U): хаб — керування партією, прослуховування музики.
- Переходи: main-menu → game-screen (бій) → бонус-етап → game-screen (наступний бій) … → end-screen → main-menu.

## Фічі поза полем
- Забіг без `meta-progression`: рівні не переносяться між партіями.
- `unlockables` — 4 бонусні саундтреки різних жанрів (Steam).
- `continue` — збереження забігу при виході (PC); iOS-версія на старті губила забіг при виході з застосунку (PocketGamer, 2013).
- `pause` — на iOS 2013 не було надійної паузи.

## Варіації й родичі
- Dungeon Hearts DX (Wii U, 2016, Wolfgame): нові персонажі, хаб, ребаланс бою, змінений інтерфейс.
- Родичі в корпусі: `10000000` (стрічка з плитками, збіг рухає героя), `puzzle-quest` / `gems-of-war` / `clash-of-heroes` (match-3 бій), `dungeon-raid` (монстри як плитки), `lumines` (потік у ритмі). Theatrhythm Final Fantasy — порівняння PocketGamer (смуги до героїв).
- **Осі варіацій**: рух поля (статичне / гравітація / **конвеєр убік**) · що дає збіг (зникнення / **заряд, який гравець вистрілює окремо**) · атака ворога (поза полем / **символ на полі, який треба перехопити**) · привʼязка смуги (нема / **смуга = персонаж**).

## Цікавинки для курсу
- Сітка-конвеєр 4×N: зсув рядків щотік, вхід справа, вихід зліва — 📎.
- Двоетапний збіг: трійка → Striker, постріл — окремою дією — 🌱.
- Вибух хрестом, що підриває інші Striker-и, + множник комбо — 🥉 (каскад по рядках і стовпцях).
- Ворожі символи на тих самих смугах, які гравець має перехопити, — 📎.
- Загибель героя сірить його колір — поле погіршується динамічно — 🌱.
- Бонус-етап між боями з іншими правилами (лише зірки, трійка = рівень) — 🌱.

## Мапа на каталог
- Є: `row-conveyor` ↔ смуги-стрічки · `drag-drop-piece` ↔ перенесення руни · `cell-click` ↔ постріл Striker-ом · `blast-wave` ↔ вибух по рядку й стовпцю · `chain-detonation` ↔ Striker підриває Striker · `combo-multiplier` · `hp-damage` · `enemy-reached-base` ↔ атака доїхала до героя · `telegraphed-intents` ↔ атаку видно на смузі заздалегідь · `status-effects` ↔ кровотеча/ослаблення · `unit-xp-skills` ↔ рівні й уміння · `player-death` · `permadeath` · `progress-acceleration` · `score-records` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+lane-grid` (з tower-lanes) — підтверджую: поле зі смуг, тут смуги — рядки сітки.
  - `+edge-spawn` (з 2048/Threes) — підтверджую: символи входять з правого краю.
  - `+match-forms-striker` «Збіг створює заряд, який активують окремо» · entities/interact · 🌱 · слоти {min: 3, fire: click|double-click}.
  - `+lane-per-hero` «Смуга = персонаж: шкода й колір привʼязані до рядка» · entities/combat · 🌱.
  - `+dead-ally-greys-tiles` «Загибель союзника вимикає його колір на полі» · entities/state · 🌱.
  - `+bonus-stage-levelup` «Бонус-етап між боями дає рівні» · game-logic/progress · 🌱.
  - `+immovable-blocker` «Нерухомий блок посеред рухомих плиток» · entities/legality · 🌱.

## Пропозиції до словників
- `+card:match-forms-striker` — збіг не зникає, а дає заряд, який гравець вистрілює окремою дією (Dungeon Hearts).
- `+card:lane-per-hero` — рядок поля привʼязаний до персонажа: колір його рун і ціль ворожих атак.
- `+card:dead-ally-greys-tiles` — плитки загиблого союзника стають мертвим баластом до кінця бою.
- `+card:bonus-stage-levelup` — короткий етап без ворога між боями, де збіги дають рівні.
- `+card:immovable-blocker` — блок на рухомій стрічці, який не можна перенести.
- `+feature:bonus-stage` — окремий короткий етап між рівнями з іншими правилами (Dungeon Hearts; аркадні бонус-раунди).

## Джерела
- ⭐ [Wikipedia: Dungeon Hearts](https://en.wikipedia.org/wiki/Dungeon_Hearts) — Chargers/Striker, комбо в рядку чи стовпці, сірі Striker-и, дебафи, бонус-етап, 4 героя з кольорами, 47 монстрів, скидання прогресу, DX для Wii U.
- [Steam](https://store.steampowered.com/app/229520/Dungeon_Hearts/) — Fatestream, уміння (атаки, лікування, «time-altering»), 10 середовищ, 40+ істот і 7 босів, Cube Roots / Devolver Digital, 28.03.2013.
- [ZTGD (PC)](https://ztgd.com/reviews/dungeon-hearts-pc/) — клік зливає трійку в діамант, діамант знищує ворожі кристали в рядку й стовпці, кровотеча/ослаблення, новий забіг з 1 рівня.
- [Gamer's Temple (PC)](https://www.gamerstemple.com/game-reviews/pc/2367/dungeon-hearts-review) — drag мишею, подвійний клік, ланцюг діамантів, мертвий герой сірить камені, бонус-етап зірок, рахунок у кінці, збереження.
- [Destructoid](https://www.destructoid.com/reviews/review-dungeon-hearts/) — real-time, 4 ряди, Striker чистить шкідливе у своєму ряду, HP і мана, до 3 заклять на героя.
- [PocketGamer (iOS)](https://www.pocketgamer.com/dungeon-hearts/review/) — тап по руні, сіра руна гине від руни в тій самій смузі, бонус-етап без ворога, проблеми з паузою.
- [Gaming Nexus](https://www.gamingnexus.com/Article/Dungeon-Hearts/Item3927.aspx) — «підібрати й покласти» на стрічку, нерухомі квадратні блоки, «непотрібні» сірі блоки, що треба розбивати після загибелі героя.

## Непевне
- (?) Як утворюється й активується Striker: Wikipedia — трійка перетворюється сама, ZTGD — клік по одній з трьох зливає їх, Gamer's Temple — трійка зливається сама, постріл подвійним кліком; PocketGamer (iOS) — один тап.
- (?) Куди можна перенести руну: на будь-яку вільну клітину чи лише поруч; що буде при опусканні на зайняту клітину.
- (?) Кількість стовпців, швидкість стрічки, формула шкоди комбо й бонусу за змішані кольори.
- (?) Мана й вартість умінь — лише в Destructoid; перелік умінь за героями не знайдено (є щит, отруйні стріли, лікування, сповільнення стрічки).
- (?) Класи розходяться між джерелами: Wikipedia — Brand (червоний мечник), Jin (жовтий маг), August (синій клірик), Telina (зелена лучниця); Destructoid — «warrior, white mage, dark mage, archer».
- (?) Кількість монстрів: Wikipedia — 47, Steam — 40+ і 7 босів; особливі механіки босів не описані.
- (?) Умова поразки: Wikipedia — «програний бій» скидає рівні; Gamer's Temple — гра закінчується, коли загинули всі четверо (так і записано).
