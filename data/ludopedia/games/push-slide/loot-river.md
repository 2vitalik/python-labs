---
title: Loot River
slug: loot-river
aka: []
family: push-slide
also: [roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2022
platforms: [PC, Xbox One, Xbox Series X|S, PS4, PS5]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1494260/", best: true, note: "«Souls meets Tetris»: зсуваєш руїни під собою; трейлери, редактор рівнів; новини: щоденні забіги, таблиці, «corpse runs»"}
  - {kind: official, url: "https://lootriver.com/", note: "сайт гри: «A Dungeon shifting roguelike», straka.studio, SUPERHOT PRESENTS"}
  - {kind: other, url: "https://lootriver.com/press/sheet.php?p=loot_river", note: "прес-кіт: «shift the ground beneath them, sliding floating ruins together», PS4/PS5 — 19.12.2023"}
  - {kind: other, url: "https://www.gameinformer.com/review/loot-river/pieces-sailing-into-place", note: "огляд 8.5/10: платформи правим стіком, монстри замикають платформу, яруси, вогняні пастки, знання"}
  - {kind: other, url: "https://littlebitsofgaming.com/2022/05/03/game-review-loot-river", note: "огляд: правий стік зсуває плитку під тобою, пастка для ворога, сходи між висотами, Святилище"}
  - {kind: other, url: "https://www.commonsensemedia.org/game-reviews/loot-river", note: "огляд: рух — ковзанням платформ, повний контроль героя, easy mode"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Loot+River+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [carrier-platform, multi-cell-size, height-levels, dungeon-generation, hp-damage, realtime-ai, shop-between-levels, daily-puzzle, leaderboard, in-game-editor, level-exchange, map-window, difficulty-levels, +ride-and-steer-platform, +platform-lock-enemy, +meta-progression, +corpse-run, +boss-fight, +parry-counter]
proposes: ["+card:ride-and-steer-platform", "+card:platform-lock-enemy", "+card:corpse-run", "+card:parry-counter"]
author: opus
date: 2026-11-19
---

# Loot River — action-роглайк, де ти зсуваєш плавучі руїни-тетроміно під собою посеред бою

## Суть
Action-роглайк словацької straka.studio (видавець SUPERHOT PRESENTS, 2022): процедурні затоплені лабіринти, бій у дусі Dark Souls (заряджені удари, парирування, ухилення, заклинання), смерть — новий забіг, а частина «знань» іде на постійні відкриття. Тут описано лише сітковий шар (позначка черги «витягти»): сама гра називає себе «Souls meets Tetris».

Підземелля затоплене, і руїни різної форми плавають по воді, як фігури тетроміно. Правим стіком гравець зсуває ту платформу, на якій стоїть, разом із собою, а лівим водночас керує героєм. Так прокладають шлях до виходу, підпливають до ворожого плоту, щоб ударити й відплисти, заганяють ворогів у пастку й ухиляються від сильних атак.

## Поле і час
- Вода — квадратна сітка; платформи — поліоміно з квадратних плиток (прямі, Г-подібні, більші прямокутники), рухаються вздовж осей сітки; береги й стіни нерухомі.
- Real-time: герой ходить вільно, не по клітинах, у межах своєї платформи; платформа ковзає водою під керуванням правого стіка.
- Яруси: платформи різної висоти; щоб піднятися, підганяєш платформу зі сходами; у Sunken Village є ліфт.
- Рівні процедурні; між ними — Святилище (хаб із крамницями, час там стоїть); арени босів змінюються від забігу до забігу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мандрівник | player | HP, мана, 5 характеристик | вільний рух, удари, заряджений удар, парирування, ухилення, ривок, заклинання |
| Платформа-руїна | platform | форма-поліоміно | везе того, хто на ній стоїть; її зсуває гравець, що стоїть на ній |
| Платформа зі сходами | platform | ярус | зʼєднує платформи різної висоти |
| Вода | terrain | — | поле, яким ковзають платформи |
| Берег, стіни, колони | static | — | межі поля |
| Вогняна пастка | hazard | — | підпалює пліт |
| Маг-замикач | enemy | — | замикає платформу на місці, доки живий |
| Маг-захисник | enemy | — | щит на сусідніх ворогів, доки живий |
| Інші вороги (маги-лицарі, маги з бомбами, «електричні ведмеді») | enemy | — | стоять на своїх плотах і б'ються |
| Бос (First One, Usurper та інші) | boss | арена | арена міняється з кожним забігом |
| Скриня | container | — | предмет і / або знання |
| Власний труп | container | — | остання зброя й третина знань, утрачених у минулому забігу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(right_stick, dir)` → ЯКЩО `custom: «герой стоїть на платформі»` і `not state(platform, locked)` → ТО `move(platform, dir)`, `carry(platform, player)`.
- КОЛИ `input(left_stick, dir)` → ТО `custom: «герой іде вільно в межах платформи»` — обидва стіки працюють одночасно.
- КОЛИ `blocked(platform)` → ТО `block` — платформа впирається в берег чи іншу платформу (?).
- КОЛИ `custom: «маг-замикач живий»` → ТО `set_state(platform, locked)`.
- КОЛИ `died(lock_mage)` → ТО `clear_state(platform, locked)`.
- КОЛИ `custom: «спрацювала вогняна пастка»` → ТО `set_state(raft, burning)`, `damage(player, n)`.
- КОЛИ `adjacent(platform, other_platform)` → ЯКЩО `custom: «той самий ярус або сходи»` → ТО `custom: «можна перейти пішки чи ривком»`.
- КОЛИ `input(leap)` → ЯКЩО `counter(mana, >=, cost)` → ТО `move(player, target_platform)` — заклинання Leap; з ним мана відновлюється сама, щоб не застрягнути (патч 1.0.65).
- КОЛИ `input(parry)` → ЯКЩО `custom: «точний момент»` → ТО `stun(enemy, n)`, `set_state(player, invulnerable, short)` — після парирування — контрудар.
- КОЛИ `died(enemy)` → ТО `counter(xp, +n)` — рівень героя росте від кількості вбитих за забіг.
- КОЛИ `reach(player, exit)` → ТО `next_level` — через Святилище.
- КОЛИ `hp_zero(player)` → ТО `lose`, `respawn(player, sanctuary)` — новий забіг з першого рівня, характеристики скинуто, частина знань лишається.
- КОЛИ `contact(player, own_corpse)` → ТО `give(player, last_weapon)`, `currency(+third_of_lost_knowledge)`.
- Перемога: фінал «Victory» або «Escape» (обидва з таблицями часу). · Поразка: смерть → новий забіг. · Рахунок: найкращий час Victory / Escape (NG+ позначено «+»).

## Керування і ввід
- Лівий стік — герой; правий стік — платформа під героєм; обидва водночас.
- Атака, заряджена атака, парирування, ухилення / ривок, заклинання; повна підтримка геймпада.

## Вікна, меню, HUD
- `game-screen`: піксельне поле згори з динамічним світлом і симуляцією води.
- `inventory-window` (вкладка Character): характеристики Strength, Vitality, Dexterity, Endurance, Intelligence, вільні очки, монети й знання; слоти зброї, обладунку, шолома, рун, амулетів, витратних; опис зброї; Health, Mana, Experience, Armor, Crit. Damage, Speed, опір вогню, шоку, морозу, отруті.
- `map-window` — вкладка Map поруч із Character (перемикання A / D); меню модифікаторів (патч 1.0.67).
- `shop-window` у Святилищі: дерево відкриттів за знання (Freya: вузли зброї з замками, «Current Knowledge»), часткові внески.
- `leaderboard` — найкращі часи Victory / Escape; `mode-select` — Daily Run після першої перемоги.
- `editor-window` — редактор рівнів (грудень 2023), обмін через mod.io між Steam, PlayStation і Xbox.
- `settings-window`: тривалість вікна розмови, easy mode (попередження про складність на старті).
- `dialogue-window` — розмови з мандрівниками й Іфіс.

## Фічі поза полем
- `meta-progression`: знання (Knowledge) на постійні відкриття зброї, заклинань, модифікаторів; вкладати можна частинами між забігами.
- Daily Run: те саме підземелля для всіх, випадкова, але однакова видача; нагорода — ще 10 амулетів у пулі й Shapeshift Charm.
- `leaderboard-online`, New Game+, два фінали.
- `level-editor` + `level-sharing` через mod.io, крос-платформно.
- Easy mode.
- Вміст: 26 видів зброї × 4 стихійні руни × 10 рівнів, 40+ амулетів, 9 обладунків, 18 шоломів (Steam).

## Варіації й родичі
- Сітковий шар — родич ковзних пазлів: [rush-hour](rush-hour.md) (блоки вздовж осей), [klotski](klotski.md) (блоки різних розмірів), [slider](slider.md) (зсуваєш шматки мапи); різниця — ти стоїш на тому, що рухаєш.
- Картка `carrier-platform` (колоди Frogger, плоти A Monster's Expedition) — платформа везе; тут гравець ще й веде її.
- Осі варіацій:
  - **хто рухає платформу**: сама за розкладом (Frogger) / гравець, стоячи на ній (Loot River) / гравець ззовні, як курсор (Rush Hour);
  - **чи стоїть поле, поки думаєш**: так — покрокові пазли сімʼї / ні — real-time бій (Loot River);
  - **що замикає платформу**: нічого / живий ворог-замикач (Loot River).
- Роглайк-частина — `also: [roguelike]`: процедурні рівні, хаб, метапрогресія, щоденні забіги.

## Цікавинки для курсу
- Платформа-поліоміно, що везе гравця: зсув усієї фігури з перевіркою колізій із берегом та іншими платформами — 📎.
- Два вводи одночасно: рух героя всередині фігури (локальні координати) + рух фігури по сітці — 🥉.
- Платформа, замкнена, доки живий маг — 🌱.
- Яруси й платформа-сходи як «міст висот» — 📎.
- Процедурне затоплене підземелля з гарантією, що вихід досяжний ковзанням (BFS по станах платформ) — 🥇.
- Метапрогресія знаннями з частковими внесками й «corpse run» — 📎.

## Мапа на каталог
- Є: `carrier-platform` ↔ платформа везе героя; `multi-cell-size` ↔ платформи-поліоміно; `height-levels` ↔ яруси й сходи; `dungeon-generation` ↔ процедурні лабіринти; `hp-damage` ↔ бій; `realtime-ai` ↔ вороги; `shop-between-levels` ↔ Святилище; `daily-puzzle` ↔ Daily Run; `leaderboard` ↔ часи; `in-game-editor` + `level-exchange` ↔ редактор і mod.io; `map-window` ↔ мапа; `difficulty-levels` ↔ easy mode.
- **Нема** → пропозиції карток:
  - `+ride-and-steer-platform` «Аватар веде платформу, на якій стоїть» · entities/move · 🥉 · слоти {shape: polyomino, input: second_stick}.
  - `+platform-lock-enemy` «Ворог замикає платформу, доки живий» · entities/state · 🌱.
  - `+meta-progression` (є в корпусі) — знання між забігами.
  - `+corpse-run` «Труп минулого забігу повертає частину втраченого» · game-logic/economy · 🌱 · слот {share: 1/3}.
  - `+boss-fight` (є в корпусі) — арени змінюються.
  - `+parry-counter` «Парирування в точний момент відкриває контрудар» · entities/combat · 📎.

## Пропозиції до словників
- `+card:ride-and-steer-platform`, `+card:platform-lock-enemy`, `+card:corpse-run`, `+card:parry-counter` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Loot River](https://store.steampowered.com/app/1494260/) — «Souls meets Tetris», «Slide blocks of ancient ruins», редактор рівнів, вміст; новини: «platform locking mages», Leap, сходи, Daily Runs, leaderboards Victory / Escape, corpse runs, Protector Mage, змінні арени босів.
- [Офіційний сайт](https://lootriver.com/) — «A Dungeon shifting roguelike», straka.studio, Slovak Arts Council.
- [Прес-кіт](https://lootriver.com/press/sheet.php?p=loot_river) — «players can shift the ground beneath them, sliding floating ruins together in a series of tile puzzles»; PS4/PS5.
- [Game Informer](https://www.gameinformer.com/review/loot-river/pieces-sailing-into-place) — правий стік для платформ, «monsters that lock a platform in place until killed», яруси, вогняні пастки, Святилище, знання, 8.5/10.
- [Little Bits of Gaming](https://littlebitsofgaming.com/2022/05/03/game-review-loot-river) — «move the right stick… shift the tile that you are currently standing on», пастка для ворогів, сходи між висотами, боси.
- [Common Sense Media](https://www.commonsensemedia.org/game-reviews/loot-river) — рух ковзанням платформ, повний контроль героя, easy mode, Xbox і Windows.
- YouTube: пошук «Loot River gameplay».

## Непевне
- (?) Як саме зупиняється платформа: ковзає, поки тримаєш стік, чи до упору; чи може вона штовхати інші платформи або ворожі плоти — з оглядів не зрозуміло.
- (?) Керування платформою на клавіатурі й миші не перевірено (огляди описують геймпад).
- (?) Що відбувається з героєм на платформі, яка горить, і з ворогом, якого «затиснули» платформами.
- (?) Чи є Вікіпедія-стаття (пошук Вікіпедії нічого не дав) і фан-вікі (fandom віддає 402).
