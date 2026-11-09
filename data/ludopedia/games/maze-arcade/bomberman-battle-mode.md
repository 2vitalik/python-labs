---
title: Bomberman — battle mode (Super Bomberman, Super Bomberman R / R Online / R 2)
slug: bomberman-battle-mode
aka: [Super Bomberman, Super Bomberman R, Super Bomberman R Online, Super Bomberman R 2, Battle 64, Бомбермен батл]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: online
  info: hidden
  random: setup
  goal: survive
year: 1993
platforms: [SNES (1993), Switch / PS4 / Xbox One / PC (R, 2017), Stadia / Switch / PS4 / Xbox / PC (R Online, 2020–2022), Switch / PS / Xbox / PC (R 2, 2023)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Super_Bomberman", best: true, note: "battle mode SNES: 1–4 гравці, мультитап, 12 арен, 2 хв, Hurry Up з 1:30, трофеї 1–5, нічия"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bomberman_(1990_video_game)", note: "PC Engine Bomberman (1990): battle до 5 гравців через мультитап, лише Bomb/Fire, Skull Mode; вважається першою «last man standing»"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Super_Bomberman_R", note: "R: 8 гравців, 19 арен, 27 персонажів зі здібностями, ліга Baby → God, Grand Prix 3×3 з самоцвітами"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Super_Bomberman_R_Online", note: "R Online: battle royale, характеристики персонажа обмежують прокачку, закрито 1.12.2022"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Super_Bomberman_R_2", note: "R 2: Castle (1 захисник проти 15), Grand Prix Crystal, Battle 64, редактор"}
  - {kind: other, url: "https://www.thesixthaxis.com/2020/09/07/super-bomberman-r-online-review/", note: "огляд R Online: 16 арен по 4, раунд 2 хв, мінус 4 арени за раунд, ліміти прокачки персонажа"}
  - {kind: other, url: "https://www.gamespark.jp/article/2021/05/30/109076.html", note: "плей-репорт R Online: 2 життя-удари, kick/punch/throw з предметів, блоки падають згори, мисобон у кімнатах"}
  - {kind: official, url: "https://www.konami.com/games/eu/en/products/bomberman_r_online/", note: "офіційна сторінка R Online (Konami EU)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=super+bomberman+r+2+castle+mode+gameplay", note: "пошук; Castle mode"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=super+bomberman+r+online+battle+64+gameplay", note: "пошук; Battle 64"}
stage: v1
coverage: 65
mechanics: [move-4dir, impassable-cells, bomb-fuse, blast-wave, chain-detonation, destructible-blocks, hidden-under-block, in-round-upgrades, item-pickup, touch-death, environment-death, hp-damage, timeout-punisher, ai-opponent, realtime-ai, online-multiplayer, rating-system, character-select, avatar-picker, match-setup, mode-select, in-game-editor, level-exchange, floor-types, spawn-points, +shrinking-arena, +match-trophies, +bomb-kick, +bomb-throw, +bomb-punch, +arena-merge-royale, +eliminated-revenge-cart, +character-stat-caps, +team-gem-collect, +asymmetric-castle-siege, +key-opens-chest-exit]
proposes: ["+effect:eliminate", "+trigger:round_end", "+cond:team", "+role:defender", "+window:bracket-view", "+ui:alive-counter", "+feature:league-tiers", "+feature:battle-pass", "+card:arena-merge-royale", "+card:eliminated-revenge-cart", "+card:asymmetric-castle-siege", "+card:character-stat-caps"]
author: opus
date: 2026-11-09
---

# Bomberman battle mode — арена «останній вижилий»: бомби, копняк, стіни Hurry Up, а з R Online — 64 гравці й облога замку

## Суть
Versus-режим серії Bomberman: кілька бомберменів на одній арені, кожен ставить бомби, вибух-хрест убиває будь-кого, переможець раунду — останній живий. Базові правила бомби, вибуху й підсилень описані в `bomberman`; тут — те, що додає versus: таймер раунду з «сутінковою смертю» (стіни падають спіраллю), матч до N трофеїв, CPU-суперники. Сучасні частини розширюють формат: R Online/R 2 — battle royale на 64 гравці, що зливаються з 16 арен у одну, а R 2 — асиметрична облога замку (1 захисник проти 15 атакувальників із ключами).

## Поле і час
- Арена = один екран сітки: непробивні колони через клітину, руйновані блоки з прихованими підсиленнями; гравці стартують у кутах.
- Super Bomberman (1993): 12 тематичних арен (12-та — Speed Round); R (2017): 19 арен, частина багаторівневі, зі спринг-платформами, льодом, рухомими блоками.
- Real-time; раунд SNES — 2 хв, з 1:30 «Hurry Up!» — незнищенні стіни падають від лівого нижнього кута за годинниковою стрілкою.
- Battle 64 (R Online, R 2): старт — 16 арен по 4 гравці, раунд 2 хв; після раунду 4 арени зникають, гравці переходять на решту, доки не лишиться одна (`field` — набір пов'язаних арен).
- Castle (R 2): одна велика арена-замок зі скринями, гарматами й конвеєрами; таймер матчу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бомбермен-гравець | player | bombs, fire, speed; R Online — 2 удари до вибування | як у `bomberman`; у R/R Online — персонаж зі здібністю й лімітами прокачки |
| CPU-бомбермен | enemy | рівень (?) | заповнює вільні слоти, ухиляється від хрестів |
| Бомба | object | запал, range = fire | вибух-хрест; R Online: щойно поставлену можна зсунути у вільний бік |
| Вибух | hazard | range | SNES: миттєва смерть; R Online: −1 життя-удар |
| Колона | static | — | гасить вибух |
| Цегла | object | ховає підсилення | руйнується вибухом |
| Падаюча стіна (Hurry Up) | hazard → static | з 1:30 | спіраль від краю, убиває при падінні |
| Падаючий блок (Battle 64) | hazard | — | після таймера блоки знову падають згори, частина зон закривається; удар = −1 життя |
| Підсилення Bomb / Fire / Speed | pickup | до межі персонажа | як у `bomberman` |
| Kick / Punch / Throw | pickup | — | штовхнути бомбу ногою, вдарити кулаком, підняти й кинути |
| Бонус-предмети SNES (морозиво, млинці, яблука) | pickup | очки | лише очки |
| Годинник (SNES) | pickup | — | додає час раунду |
| Самоцвіт / кристал (Grand Prix) | pickup | — | очки команди |
| Візок мисобона (revenge) | player | — | вибулий гравець їздить краєм арени й кидає бомби всередину (?) |
| Захисник замку (R 2) | player (`+role:defender`) | 1 з 3 спецздібностей | ставить пастки, кличе Еллонів |
| Атакувальник замку (R 2) | player | до 15 | збирає ключі, відкриває скрині |
| Ключ | pickup | — | потрібен, щоб відкрити скриню |
| Скриня | container | — | відкрита ключем → атакувальник виходить з матчу; усі відкриті → кінець |
| Гармата / конвеєр | hazard / terrain | — | охороняють скрині; конвеєр везе |
| Еллон | enemy | — | монстри захисника (?) |
| Пастка | hazard | — | ставить захисник |
| Пружина / лід / рухомий блок (R) | terrain / object | — | підкидає / ковзання / зсувний блок |

## Правила (КОЛИ → ЯКЩО → ТО)
- Бомба, вибух, руйнування, підсилення — як у `bomberman` (див. його правила).
- КОЛИ `contact(blast, player)` → ЯКЩО `mode(classic)` → ТО `custom: «гравець вибуває з раунду»` (`+effect:eliminate`).
- КОЛИ `contact(player, skull)` → ЯКЩО `mode(skull)` → ТО `set_state(player, curse)` (PC Engine 1990; ефекти черепа (?)).
- КОЛИ `contact(blast, player)` → ЯКЩО `mode(battle64)` → ТО `damage(player, 1)`; КОЛИ `hp_zero(player)` → ТО `custom: «вибування з арени»`.
- КОЛИ `contact(player, bomb)` → ЯКЩО `has(player, kick)` → ТО `slide(bomb, dir)`.
- КОЛИ `input(punch)` → ЯКЩО `has(player, punch) and facing(player, bomb)` → ТО `custom: «бомба летить на кілька клітин через перешкоди»`.
- КОЛИ `input(grab)` → ЯКЩО `has(player, throw)` → ТО `pickup(player, bomb)`; повторний `input` → `custom: «кинути бомбу вперед»`.
- КОЛИ `timer(1:30)` → ЯКЩО `mode(classic)` → ТО `message("Hurry Up!")`, `custom: «щотік стіна падає на наступну клітину спіралі від краю»`.
- КОЛИ `contact(falling_wall, player)` → ТО `custom: «миттєве вибування»`.
- КОЛИ `count(alive_players, ==, 1)` → ТО `score(trophy)` переможцю; КОЛИ `count(alive_players, ==, 0)` → ТО `draw`.
- КОЛИ `timer(2:00)` → ЯКЩО `count(alive_players, >, 1)` → ТО `draw` (SNES).
- КОЛИ `counter(trophies, ==, n)` → ТО `win` матчу (n = 1–5 у `match-setup`).
- КОЛИ `contact(player, clock)` → ТО `timer(+n)` (SNES).
- КОЛИ `died(player)` → ЯКЩО `mode(revenge)` → ТО `spawn_at(revenge_cart, edge)` (?); КОЛИ `contact(cart_bomb, player)` → ТО `custom: «вибулий повертається на місце жертви»` (?).
- Battle 64: КОЛИ `custom: «кінець 2-хв раунду»` (`+trigger:round_end`) → ТО `custom: «4 арени зникають, їхні вцілілі переходять на сусідні»`.
- Battle 64: КОЛИ `timer(close)` → ТО `custom: «блоки падають згори, частина зон стає забороненою»`.
- Battle 64: КОЛИ `count(alive_players, ==, 1)` → ТО `win` (останній зі 64).
- R Online: КОЛИ `picked(player, power_up)` → ЯКЩО `custom: «характеристика нижче межі персонажа»` → ТО `counter(stat, 1)`; інакше нічого.
- Grand Prix (R): КОЛИ `contact(player, gem)` → ТО `pickup`, `counter(team_gems, 1)`; КОЛИ `timer(match)` → ТО `win` команді з більшою кількістю (`+cond:team`).
- Castle (R 2): КОЛИ `contact(attacker, key)` → ТО `pickup`; КОЛИ `contact(attacker, chest)` → ЯКЩО `has(attacker, key)` → ТО `custom: «скриня відкрита, атакувальника знято з матчу»`.
- Castle (R 2): КОЛИ `all_gone(closed_chest)` → ТО `win` атакувальникам; КОЛИ `timer(match)` → ТО `custom: «підсумок за відкритими скринями»` (?).
- Castle (R 2): КОЛИ `input(trap)` → ЯКЩО `state(player, defender)` → ТО `place(player, trap)`.
- Перемога: останній вижилий / N трофеїв · команда з більшою кількістю самоцвітів · атака відкрила всі скрині або захист дотримав до таймера · Поразка: вибування · Рахунок: трофеї, ліга (R online), ранги сезону.

## Керування і ввід
- D-pad / стік — рух; кнопка — бомба; окремі кнопки для детонатора, удару кулаком, підйому/кидка (коли є відповідне підсилення) і спецздібності персонажа (R).
- SNES: 1–4 гравці, понад 2 людей — через мультитап; порожні слоти — CPU.
- R: локально й онлайн до 8; R Online / R 2 Battle 64 — онлайн до 64, quick match.

## Вікна, меню, HUD
- `main-menu` → `mode-select` (Normal / Battle; R: Story / Battle / Grand Prix / Online; R 2: Castle, Battle 64…).
- `match-setup`: гравці людина/CPU, трофеї 1–5, арена, правила (SNES; R — також підсилення й мисобон (?)).
- `character-select` — 27 персонажів R (Bomberman Bros., Five Dastardly Bombers, Konami-кросовери); R Online — персонаж з характеристиками.
- `game-screen`: арена; HUD — `timer-countdown` 2:00, `player-portraits` (живі/вибулі), у Battle 64 — `+ui:alive-counter` (скільки з 64 лишилось) (?).
- `end-screen` раунду з трофеями; підсумок матчу.
- `lobby-window` і ліга (R online: Baby B → God A); R Online — `+window:bracket-view` переходу між аренами (?), Bomber Pass.
- `editor-window` — редактор арен Castle, поширення онлайн (R 2, без підтвердження).
- `pause-menu` (лише офлайн).

## Фічі поза полем
- `mode-versus`, `local-multiplayer`, `online-multiplayer`, `ai-opponent-levels` (CPU), `match-trophies`.
- R: ліга з поділами Baby B … God A (`+feature:league-tiers`), Grand Prix 3×3 (оновлення листопада 2017).
- R Online: free-to-play, Bomber Pass з сезонними рангами (`+feature:battle-pass`), Premium Edition з приватними кімнатами; сервери закрито 1.12.2022, Battle 64 перейшов у R 2.
- R 2: редактор арен Castle (`level-editor`, `level-sharing`), Solo-Bomb story.
- Точних збережень матчу нема; прогрес — профіль онлайн.

## Варіації й родичі
- `bomberman` — база: бомба, вибух-хрест, цегла з підсиленнями, двері, вороги.
- Bomberman (PC Engine, 1990) — battle до 5 гравців (TurboGrafx Multitap), підсилення лише Bomb і Fire; Skull Mode — під блоками інколи ховаються шкідливі черепи; вважається першою грою «last man standing». Saturn Bomberman (1996) — 10 гравців; Bomberman Blast — 8; Super Bomberman R Online — 64.
- Battle royale-родичі: `paper-io` (територія онлайн), `pac-man-battle-royale` (останній вижилий в одному лабіринті), Tetris 99.
- **Осі варіацій:** кількість гравців 4 / 8 / 10 / 64 · удар вибуху: миттєва смерть / 2 життя · кара за час: нічия / стіни спіраллю / падаючі блоки й закриті зони · вибулий: глядач / візок-мисобон із поверненням · формат: кожен за себе / команди 3×3 / асиметрія 1×15 · прокачка: без меж / ліміти персонажа.

## Цікавинки для курсу
- Арена «останній вижилий» з трофеями до N — 🌱 поверх готового Bomberman.
- Hurry Up: розклад `set_cell` по спіралі як годинник раунду — 📎.
- Мисобон: вибулий гравець лишається в грі на краю поля й може повернутися — 📎: другий шанс без нового життя.
- Злиття арен Battle 64: 16 полів → 12 → … → 1, перенесення гравців між полями — 🥈: кілька незалежних симуляцій і міграція.
- Ліміти прокачки персонажа (стелі bombs/fire/speed) — 🌱: дані персонажа керують правилом підбору.
- Асиметрична облога Castle: 1 захисник з пастками проти 15 з ключами — 🥈: різні ролі, умови перемоги для сторін.
- CPU-бомбермен на мульти-арені: карта загроз у часі від усіх бомб — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` · `bomb-fuse` · `blast-wave` · `chain-detonation` · `destructible-blocks` · `hidden-under-block` · `in-round-upgrades` · `item-pickup` · `touch-death` · `environment-death` · `hp-damage` (2 удари R Online) · `timeout-punisher` (Hurry Up) · `ai-opponent` · `realtime-ai` · `online-multiplayer` · `rating-system` (ліга) · `character-select` · `avatar-picker` · `match-setup` · `mode-select` · `in-game-editor`, `level-exchange` (R 2) · `floor-types` (лід, пружини) · `spawn-points` (кути).
- **Нема** → пропозиції карток:
  - `+shrinking-arena`, `+match-trophies`, `+bomb-kick`, `+bomb-throw` — уже запропоновані в `bomberman`; підтверджую.
  - `+bomb-punch` «Удар бомби кулаком» · entities/combat · 📎.
  - `+arena-merge-royale` «Злиття арен battle royale» · game-logic/opponent · 🥈 · слот {arenas: 16, drop: 4} .
  - `+eliminated-revenge-cart` «Вибулий атакує з краю» · game-logic/opponent · 📎.
  - `+character-stat-caps` «Стелі прокачки персонажа» · entities/state · 🌱.
  - `+team-gem-collect` «Командний збір самоцвітів на час» · game-logic/score · 📎.
  - `+asymmetric-castle-siege` «Асиметрична облога 1 проти N» · game-logic/opponent · 🥈.
  - `+key-opens-chest-exit` «Ключ відкриває скриню й виводить з матчу» · entities/interact · 🌱.

## Пропозиції до словників
- `+effect:eliminate` — гравець вибуває з раунду, гра триває для інших (є в інших іграх корпусу; підтверджую).
- `+trigger:round_end` — кінець раунду всередині матчу (Battle 64: злиття арен).
- `+cond:team` — сутність належить команді X (Grand Prix, Castle).
- `+role:defender` — гравець асиметричної сторони з окремим набором дій.
- `+window:bracket-view` — схема арен/сітки турніру і переходів між ними.
- `+ui:alive-counter` — скільки гравців лишилось у матчі.
- `+feature:league-tiers` — ліга з поділами, очки за перемоги.
- `+feature:battle-pass` — сезонний трек нагород.
- `+card:arena-merge-royale`, `+card:eliminated-revenge-cart`, `+card:asymmetric-castle-siege`, `+card:character-stat-caps` — див. «Мапу на каталог».

## Джерела
- ⭐ [Wikipedia: Super Bomberman](https://en.wikipedia.org/wiki/Super_Bomberman) — battle mode 1993: 1–4, мультитап, 12 арен, 2 хв, Hurry Up на 1:30, стіни від лівого нижнього кута за годинниковою, трофеї 1–5, нічия, бонус-предмети.
- [Wikipedia: Super Bomberman R](https://en.wikipedia.org/wiki/Super_Bomberman_R) — 8 гравців, 19 арен (пружини, лід, рухомі блоки), 27 персонажів, ліга Baby → God, Grand Prix 3×3.
- [Wikipedia: Super Bomberman R Online](https://en.wikipedia.org/wiki/Super_Bomberman_R_Online) — battle royale, характеристики персонажа, Premium, закриття 1.12.2022.
- [Wikipedia: Super Bomberman R 2](https://en.wikipedia.org/wiki/Super_Bomberman_R_2) — Castle 1 × 15, ключі й скрині, гармати, конвеєри, Еллони, Grand Prix Crystal, Battle 64, редактор.
- [TheSixthAxis: огляд R Online](https://www.thesixthaxis.com/2020/09/07/super-bomberman-r-online-review/) — 16 арен по 4, раунд 2 хв, мінус 4 арени, ліміти прокачки, Bomber Pass.
- [Game*Spark: плей-репорт R Online](https://www.gamespark.jp/article/2021/05/30/109076.html) — 2 удари, kick/punch/throw, падаючі блоки й закриті зони, мисобон у кімнатному режимі.
- [Wikipedia: Bomberman (1990)](https://en.wikipedia.org/wiki/Bomberman_(1990_video_game)) — battle до 5, лише Bomb/Fire, Skull Mode.
- [Konami: Super Bomberman R Online](https://www.konami.com/games/eu/en/products/bomberman_r_online/) — офіційна сторінка (бачив у пошуку).
- YouTube: пошук «super bomberman r 2 castle mode gameplay», «super bomberman r online battle 64 gameplay».

## Непевне
- (?) Чи є в Super Bomberman (1993) копняк бомб (Kick) і череп — Wikipedia перелічує лише бонус-предмети й годинник; копняк точно є з R Online.
- (?) Правила мисобона: з якої частини серії, чи повертає вибулого на арену; у R Online — лише в кімнатному режимі.
- (?) Як саме гравці переходять між аренами Battle 64 і як виглядає фінальна арена.
- (?) Чим закінчується Castle за таймером (перемога захисника чи підрахунок скринь); роль Еллонів; тривалість таймера.
- (?) Наявність `alive-counter` і схеми арен у HUD R Online — з опису механіки, не зі скриншотів.
- (?) Чи PC Engine Bomberman (1990) — справді перший battle-режим серії (Wikipedia: «вважається першою last man standing»).
- (?) R 2: редактор і поширення арен Castle — на Wikipedia без джерела.
