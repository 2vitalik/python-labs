---
title: Mine Bombers
slug: mine-bombers
aka: [MineBombers, Mine Bombers 3.11, MB]
family: dig-gravity
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: both
  goal: score
year: 1996
platforms: [DOS]
links:
  - {kind: other, url: "https://www.dosgames.com/game/mine-bombers", best: true, note: "DOSGames: опис, 1996, Skitso Productions, freeware; архів з мануалами MINEENG.TXT / MINEFIN.TXT"}
  - {kind: other, url: "https://www.homeoftheunderdogs.net/game.php?id=3462", note: "Home of the Underdogs: скарби → гроші → зброя, гроші за фраги, динаміт/вогнемети/ядерки, 15 рівнів сингла, редактор"}
  - {kind: other, url: "https://www.dosgames.com/files/minebomb.zip", note: "архів v3.11: MINEENG.TXT, MINEFIN.TXT (скарби з цінами, предмети на рівні, поради), HISTORIA.TXT (зміни версій)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mine+Bombers+DOS+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, move-auto, keyboard-controls, dig-terrain, destructible-blocks, impassable-cells, push-object, bomb-fuse, blast-wave, explode-area, chain-detonation, hp-damage, player-death, item-pickup, inventory-items, teleport-pair, round-currency, shop-between-levels, shop-catalog, shop-buyback, shop-window, in-round-upgrades, hot-seat, time-out, collect-all, reach-exit, sequential-levels, score-records, in-game-editor, editor-palette, editor-draw-tools, game-settings, controls-remap, profile-stats, +bounty, +interest-on-cash, +free-market-prices, +dig-power-stat, +explosive-fluid-flow, +bomb-kick]
proposes: ["+effect:sell", "+effect:flow", "+effect:interest", "+ui:dig-power", "+card:dig-power-stat", "+card:explosive-fluid-flow", "+card:urethane-trap", "+card:random-weapon-crate"]
author: opus
date: 2026-11-09
---

# Mine Bombers — Bomberman у шахті: прогризай скелю, збирай скарби, купуй напалм і підривай друга

## Суть
Фінська DOS-гра Skitso Productions (Antti Haapakoski, Teppo Lähtinen; 1995–1996, v3.11 — freeware з 31.12.2001). До чотирьох гравців за однією клавіатурою стартують у кутах мапи-шахти, прогризають кам'яні ходи силою копання, збирають скарби й підривають одне одного зброєю, купленою в крамниці між раундами. Гроші — і бюджет, і рахунок: за фраг дають велику винагороду, а переможець турніру — той, хто має найбільше грошей (або найбільше виграних раундів). Від Bomberman відрізняє копання з характеристикою «сила копання», рідинні вибухівки (напалм, пластид, уретан) і економіка з відсотками та плаваючими цінами. Одиночний режим — 15 рівнів з монстрами до дверей-виходу.

## Поле і час
- Квадратна тайлова мапа 64 × 45 клітин: рівень — текстовий файл `.MNE`/`.MNL` (45 рядків по 64 символи), видно всю мапу одразу, гравці дрібні.
- Шари: скеля/прохід + предмети (скарби, ящики, бочки, телепорти) + гравці, монстри, бомби.
- Real-time; рух неперервний за напрямком — клавіша задає напрям, гравець іде, доки не натиснуто «стоп» (щоб на одній клавіатурі не тримати клавіші).
- Опція Darkness — темна мапа (видно лише околиці гравців, ?); з v2.2 і в мультиплеєрі.
- Випадковість: випадкові рівні й випадкове розкидання скарбів (кількість — опція Treasures), вміст ящиків, рідкісні випадкові події (v3.1).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець 1–4 | player | здоровʼя (смуга), сила копання, гроші, обрана зброя | іде за напрямком, довбає скелю, кладе бомбу, перемикає зброю |
| Скеля | terrain | міцність | довбається силою копання; заокруглені краї кришаться швидше |
| Прохід | terrain | — | вільна клітина |
| Металева плита | static | купується | зупиняє напалм і промені хрестової бомби (?) щодо руйнування |
| Камінь, що котиться | object | — | штовхається (з v2.1) |
| Скарби ×9 | pickup | браслет $10 · щит $15 · купа грошей $15 · золоте яйце $25 · злиток $30 · хрест $35 · скіпетр $50 · коштовність $65 · корона $100 | узяти → гроші; вибух знищує |
| Мала кирка / велика кирка / камʼяний бур | pickup | +1 / +3 / +5 до сили копання | до кінця рівня |
| Деревʼяний ящик | container | — | випадкова кількість випадкової зброї |
| Аптечка | pickup | — | повне здоровʼя |
| Додаткове життя | pickup | лише сингл | +1 життя |
| Телепорт | static | парний | переносить до іншого телепорта |
| Бочка | hazard | — | вибухає від вибуху |
| Монстр | enemy | — | керований компʼютером (з v2.1), у сингл-рівнях |
| Двері-вихід | static | чорний квадрат із сірою рамкою | сингл: перехід на наступний рівень |
| Бомби й заряди | object | тип, запал | мала бомба, динаміт, ядерка, напалм, пластид, уретан, хрестова, міна, радіокерована, «коник» (v3.1), біо-слиз (v3.1) |
| Інструменти й захист | pickup | — | вогнемет, піногасник, переносний телепорт, супербур, клон, бронежилет (усі — v3.1) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `face(player, dir)`, `custom: «іти в напрямку, доки не натиснуто стоп чи інший напрям»`.
- КОЛИ `blocked(player)` → ЯКЩО `cell(next, rock)` → ТО `custom: «довбати скелю зі швидкістю за силою копання»`; КОЛИ `custom: «міцність клітини вичерпано»` → ТО `set_cell(next, empty)`.
- КОЛИ `contact(player, treasure)` → ТО `pickup(player, treasure)`, `currency(+value)`.
- КОЛИ `contact(player, pick|drill)` → ТО `counter(dig_power, +1|+3|+5)` до кінця рівня; куплені в крамниці — назавжди.
- КОЛИ `contact(player, crate)` → ТО `give(player, «випадкова зброя × випадкова кількість»)`, `disappear(crate)`.
- КОЛИ `contact(player, medikit)` → ТО `heal(player, full)`.
- КОЛИ `contact(player, extra_life)` → ЯКЩО `mode(single)` → ТО `lives(+1)`.
- КОЛИ `enter(player, teleport)` → ТО `teleport(player, «інший телепорт»)`.
- КОЛИ `contact(player, rolling_rock|bomb)` → ЯКЩО `free(behind)` → ТО `push(rolling_rock|bomb)` (бомби — з v3.1).
- КОЛИ `input(bomb)` → ЯКЩО `has(player, selected_weapon)` → ТО `place(player, selected_weapon)`, `take(player, selected_weapon)`; `input(select)` — наступна зброя.
- КОЛИ `timer(fuse)` → ТО `explode(shape_by_type, n)`: руйнує скелю й скарби, `damage(player, n × Damage%)` у зоні.
- КОЛИ `custom: «вибух зачепив бомбу чи бочку»` → ТО `explode(...)` і для неї.
- Хрестова бомба: `explode(cross, n)`; ЯКЩО `cell(ray, metal_plate)` → ТО `custom: «промінь зупиняється»`.
- Напалм: КОЛИ `custom: «напалм спрацював»` → ТО `custom: «вогонь розтікається коридорами на обмежений обʼєм»`; ЯКЩО `custom: «прохід перекрито каменем або плитою»` → ТО `block`; у великій кімнаті чи розширеному коридорі не дістає.
- Пластид: КОЛИ `custom: «пластид спрацював»` → ТО `custom: «вибухова маса розтікається й зупиняється на бомбах»`; від сусіднього вибуху — `explode(...)` усієї маси.
- Уретан: КОЛИ `custom: «уретанова бомба спрацювала»` → ТО `custom: «піна заповнює простір, гравець застрягає»`; напалм крізь уретан проходить.
- КОЛИ `contact(player, mine)` → ТО `explode(...)`.
- КОЛИ `input(remote)` (?) → ТО `custom: «підірвати свої радіокеровані бомби»`.
- КОЛИ `hp_zero(opponent)` → ЯКЩО `custom: «від зброї гравця»` → ТО `currency(+bounty)` (велика «премія за вбивство»).
- КОЛИ `custom: «час раунду вийшов»` або `all_gone(treasure)` або `count(players_alive, <, 2)` → ТО `level_end`, `window(shop-window)`.
- КОЛИ `level_end` → ТО `currency(+7 % від заощаджених грошей)` (з v3.1).
- Крамниця: КОЛИ `input(bomb)` на товарі → ЯКЩО `counter(cash, >=, price)` → ТО `currency(-price)`, `give(player, item)`; `input(select)` → ЯКЩО `mode(selling)` → ТО `custom: «продати назад»`; з Free Market — ціни змінюються.
- КОЛИ `custom: «зіграно Rounds раундів»` → ТО `win` гравцю з найбільшими грошима (або з найбільшою кількістю виграних раундів — опція Winner).
- Сингл: КОЛИ `enter(player, exit_door)` → ТО `next_level`; КОЛИ `hp_zero(player)` → ТО `lives(-1)`, `restart` рівня; КОЛИ `counter(lives, ==, 0)` → ТО `game_over`, `window(leaderboard)` (Hall of Fame за досягнутим рівнем).
- Перемога: найбільше грошей (чи виграних раундів) після всіх раундів; сингл — пройти 15 рівнів. · Поразка: сингл — три життя вичерпано. · Рахунок: гроші.

## Керування і ввід
- На кожного гравця — свій набір клавіш (перепризначається): 4 напрямки, стоп, «бомба/купити», «вибір/продати»; джойстик (CALIBRA.EXE, з v2.2) і геймпад.
- Клавіші не треба тримати: рух іде до «стоп», щоб не було блокування клавіатури при 4 гравцях.
- F10 — вихід з будь-якого меню чи гри; D в опціях — скидання до стандартних.

## Вікна, меню, HUD
- `splash-screen` — стартова картинка.
- `main-menu`: START GAME · OPTIONS · INFO · QUIT.
- `profile-window` / `stats-window` — екран імен: список гравців (створити, видалити, активувати), статистика вибраного (скарби, смерті) і графік середнього успіху з гри в гру (v3.1).
- `settings-window` (OPTIONS): Treasures, Rounds, Time, Starting Cash, Speed, Damage %, Players 1–4, Redefine Keys, Darkness, Free Market, Selling, Winner by, Load Levels.
- `level-select` — завантаження готових або власних рівнів (Space — обрати, F1 — випадково).
- `help-window` / `codex-window` — INFO: 4 сторінки про зброю, інструменти й авторів.
- `shop-window` — крамниця зброї; при 3–4 гравцях показ двічі; запаси видно смугами; вихід — READY або ESC.
- `game-screen`: мапа; HUD угорі — для кожного гравця ім'я, велика іконка обраної бомби, сила копання (`+ui:dig-power`), гроші (`coins`), вертикальна смуга здоровʼя (`hp-bar`); унизу — жовта смуга часу (`timer-countdown`).
- `end-screen` — переможець турніру / GAME OVER / привітання (сингл).
- `leaderboard` — Hall of Fame (сингл).
- `editor-window` — MINEDIT.
- Переходи: титул → меню → імена → крамниця → рівень → крамниця → … → підсумок.

## Фічі поза полем
- `custom-rules` через OPTIONS (усе вище), `remap-controls`, `gamepad-support`.
- `stats` на гравця й `history`-графік (v3.1), збереження імен.
- `level-editor` MINEDIT: палітра об'єктів на дві кнопки миші, пензель (розмір F7/F8), квадратний пензель, заливка; F2 — віддзеркалити ліву половину на праву, F3 / Z — випадковий скарб; без миші — клавіші A…*; попередження «не ставте забагато монстрів і бочок».
- `cheat-codes` («повністю оновлені чит-коди», v3.1).
- Режими: мультиплеєр 2–4 (турнір з раундів) і сингл 15 рівнів з трьома життями.

## Варіації й родичі
- Версії: 1.1 (лише двоє, кілька зброй) → 2.1 (1–4 гравці, монстри, телепорти, ящики, камені, що штовхаються) → 2.2 (темрява в мультиплеєрі, продаж, плаваючі ціни, турнір за перемогами, аптечка, рвані краї коридорів) → 3.1 (8 нових предметів, випадкові рівні, статистика, відсотки 7 %, штовхання бомб) → 3.11.
- Родичі: [bomberman.md](../maze-arcade/bomberman.md) і [bomberman-battle-mode.md](../maze-arcade/bomberman-battle-mode.md) (бомби з запалом без копання), [dig-dug.md](dig-dug.md) і [tunneler.md](tunneler.md) (дуель у ґрунті), [liero.md](liero.md) (копання + зброя real-time), [scorched-earth.md](scorched-earth.md) (магазин зброї між раундами, відсотки, вільний ринок).
- **Осі варіацій**: копання — миттєве / за силою копання і міцністю / заборонене; вибух — хрест / площа / рідина, що розтікається; рахунок — останній живий / гроші / виграні раунди; економіка — фіксовані ціни / вільний ринок / відсотки на заощадження.

## Цікавинки для курсу
- Сила копання як характеристика (базова + куплена назавжди + знайдена на рівень) і міцність клітини — 📎.
- Напалм і пластид: вибухова «рідина» з обмеженим обʼємом, що тече коридорами й зупиняється на перешкодах (BFS-заливка на N клітин) — 🥉.
- Хрестова бомба, промені якої зупиняє металева плита — 🌱.
- Турнір з крамницею між раундами: купівля/продаж, плаваючі ціни, 7 % на заощадження, вибір критерію переможця — 🥉.
- Рух «до стоп» для кількох гравців за однією клавіатурою — 🌱.
- Рівень як текстовий файл 64 × 45 і редактор з дзеркаленням половини мапи — 📎.

## Мапа на каталог
- Є: `move-4dir` · `move-auto` ↔ рух до «стоп» · `keyboard-controls` · `dig-terrain` + `destructible-blocks` ↔ скеля · `impassable-cells` ↔ плити · `push-object` ↔ камені й бомби · `bomb-fuse` · `blast-wave` ↔ хрестова бомба · `explode-area` · `chain-detonation` ↔ бочки, пластид · `hp-damage` · `player-death` · `item-pickup` ↔ скарби, кирки · `inventory-items` ↔ зброя · `teleport-pair` · `round-currency` · `shop-between-levels` + `shop-catalog` + `shop-buyback` + `shop-window` · `in-round-upgrades` ↔ кирки/бур на рівень · `hot-seat` ↔ одна клавіатура · `time-out` · `collect-all` ↔ кінець рівня, коли скарби зібрано · `reach-exit` ↔ сингл · `sequential-levels` ↔ 15 рівнів · `score-records` ↔ Hall of Fame · `in-game-editor` + `editor-palette` + `editor-draw-tools` ↔ MINEDIT · `game-settings` · `controls-remap` · `profile-stats` ↔ статистика й графік.
- **Нема** → пропозиції карток:
  - `+dig-power-stat` «Сила копання проти міцності клітини» · entities/interact · 📎 · слоти {base, bonus, per_level}.
  - `+explosive-fluid-flow` «Вибухівка, що розтікається коридорами на обмежений обʼєм» · entities/combat · 🥉 · слоти {volume, stops_at}.
  - `+urethane-trap` «Заряд заповнює простір піною, гравець застрягає» · entities/combat · 📎.
  - `+random-weapon-crate` «Ящик з випадковою зброєю» · entities/interact · 🌱.
  - `+bounty`, `+interest-on-cash`, `+free-market-prices`, `+bomb-kick` — повтори з інших файлів.

## Пропозиції до словників
- `+effect:sell` — продати зброю назад у крамниці (повтор).
- `+effect:flow` — розтікання напалму/пластиду по вільних клітинах (повтор).
- `+effect:interest` — нарахування відсотка на заощаджені гроші (повтор).
- `+ui:dig-power` — показник сили копання гравця в HUD.

## Джерела
- ⭐ [DOSGames: Mine Bombers](https://www.dosgames.com/game/mine-bombers) — опис, рік, розробник, freeware, архів гри.
- [Home of the Underdogs: Mine Bombers](https://www.homeoftheunderdogs.net/game.php?id=3462) — огляд: скарби → гроші → зброя, гроші за фраги, динаміт/вогнемети/ядерки, 15 рівнів сингла, редактор, автори.
- [Архів minebomb.zip](https://www.dosgames.com/files/minebomb.zip) — `MINEENG.TXT` (меню, опції, крамниця, умови кінця рівня, сингл, поради, MINEDIT), `MINEFIN.TXT` (ціни 9 скарбів, предмети на рівні, ще поради), `HISTORIA.TXT` (зміни 1.1 → 3.11, нові предмети), формат мап `.MNE` (64 × 45).
- YouTube: пошук «Mine Bombers DOS gameplay».

## Непевне
- (?) Повний список зброї з цінами й формами вибуху — лише в графічних INFO-екранах; у тексті є лише назви з порад, історії версій та огляду (динаміт, ядерка, вогнемет).
- (?) Чи металеві плити й межі мапи взагалі незруйновні, чи лише стійкі до хрестової бомби.
- (?) Як працює радіокерована бомба (окрема клавіша чи повторне «бомба»), «коник», біо-слиз, клон, піногасник — тільки назви.
- (?) Що бачить гравець при Darkness — радіус навколо себе чи навколо всіх.
- (?) Поведінка монстрів (переслідують чи блукають) і чи бʼють вибухи монстрів премією.
- (?) Розмір премії за вбивство й стартові гроші за замовчуванням.
- (?) Кількість гравців: DOSGames пише «до 2», HotU — «двоє і більше», мануал v3.11 — 1–4 (з v2.1); у файлі — за мануалом.
