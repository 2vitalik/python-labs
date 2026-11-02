---
title: Bookworm
slug: bookworm
family: word-number
also: [falling-match, tactics]
klass: cursor
axes:
  field: hex
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: survive
year: 2003
platforms: [Windows, Mac, iOS, GBA, Xbox Live Arcade, Nintendo DS, Java ME, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bookworm_(video_game)", best: true, note: "правила: сусідні літери, падіння, червоні палаючі плитки Classic/Action, бонусні плитки, Lex-перемішування, bonus words, книги"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bookworm_Adventures", note: "Adventures: слово = атака, самоцвіти, зілля, скарби, глави й боси, Arena"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=bookworm+deluxe+popcap+gameplay", note: "пошук; геймплей Classic"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=bookworm+adventures+gameplay", note: "пошук; геймплей Adventures"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=bookworm", note: "пошук; Bookworm Adventures з 2016 знято з продажу"}
stage: v1
coverage: 65
mechanics: [cell-click, gravity-fall, spawn-random-cell, event-points, combo-multiplier, score-records, profile-stats, difficulty-levels, progress-acceleration, player-death, time-out, sequential-levels, level-unlock, save-progress, hp-damage, inventory-items, temporary-modes, end-screen, game-screen, main-menu, help-window, settings-window, leaderboard, event-effects, +word-validation, +path-trace-word, +word-length-scoring, +burning-tile, +bonus-tile-tier, +board-shuffle-penalty, +bonus-word, +word-as-attack, +status-tile, +word-category-book]
proposes: ["+trigger:input", "+trigger:turn_end", "+trigger:after", "+trigger:reach", "+cond:in_dictionary", "+cond:path_adjacent6", "+cond:length", "+effect:clear", "+effect:fall", "+effect:spawn_at", "+effect:transform", "+effect:damage", "+effect:heal", "+effect:set_state", "+role:tile", "+role:hazard", "+role:boss", "+ui:word-preview", "+ui:level-progress", "+ui:bonus-word", "+ui:hp-bar", "+window:mode-select", "+window:codex-window", "+window:inventory-window", "+feature:hall-of-fame", "+feature:mode-time-attack", "+axis:control"]
author: opus
date: 2026-11-02
---

# Bookworm — слова з сусідніх літер на «гекс»-полі, плитки падають, а вогняні плитки прогорають до низу

## Суть
Поле — колонки літерних плиток, зміщені через одну на пів клітини, тож кожна плитка має до 6 сусідів. Гравець вибирає ланцюжок сусідніх плиток, що складає англійське слово; плитки зникають, зверху падають нові. Довгі слова й рідкісні літери дають більше очок і народжують бонусні плитки, а червоні палаючі плитки щоходу спускаються й спалюють літеру під собою — дійшла до низу, і бібліотека згоріла. Bookworm Adventures (2006) перетворює це на бій: слово = удар по ворогу.

## Поле і час
- Сітка ≈7 колонок × 8 рядів (?), парні колонки зміщені вниз на пів плитки — топологія гекса на квадратних плитках.
- Шари: плитки-літери з типом (звичайна / бонус / палаюча) + рядок «bonus word» + шкала рівня збоку.
- Classic: покроково, хід = одне слово (або перемішування). Action: real-time — палаючі плитки зʼявляються й спускаються кожні кілька секунд.
- Adventures: окреме поле ≈4×4 літер (?), де сусідство не потрібне — слово з будь-яких плиток.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера | tile | літера, вартість за рідкістю | у слові → зникає; колонка осідає, зверху нова |
| Qu | tile | дві літери (?) | одна плитка = «QU» |
| Зелена плитка | tile | бонус ×?; горить 2 ходи | множить очки слова; падає зверху як звичайна |
| Золота плитка | tile | бонус більший; горить 3 ходи | замінює випадкову плитку на полі |
| Сапфірова плитка | tile | бонус ще більший | замінює випадкову плитку; за дуже довгі слова (?) |
| Діамантова плитка | tile | найбільший бонус | за найдовші слова (?) |
| Червона палаюча плитка | hazard | рівень спуску | щоходу (Classic) / кожні N с (Action) опускається на 1, знищуючи плитку під собою; її саму можна вжити в слові й так погасити |
| Lex (книжковий черв'як) | static | — | клік → перемішати всі плитки, але викликає хвилю червоних плиток |
| Bonus word | static | слово з категорії | скласти його → додаткові очки; кожне наступне дорожче |
| Шкала рівня | static | очки до наступного рівня | заповнилась → новий рівень, частіші червоні плитки |
| Adventures: ворог | enemy | HP, атака, особливості | хід ворога після слова: шкодить, накладає статус, лікується, псує плитки |
| Adventures: бос глави | boss | HP | наприкінці глави; дає скарб |
| Adventures: самоцвіт-плитка | tile | тип каменю | у слові → додатковий ефект (лікування, посилення, ослаблення ворога) |
| Adventures: зіпсована плитка | tile (стан) | locked / smashed / poisoned … (?) | заблокована, знецінена або шкодить при використанні (?) |
| Adventures: зілля | pickup | тип, ліміт 10 на тип (Vol. 2) | хід: лікує / посилює наступну атаку / знімає статус з поля |
| Adventures: скарб | pickup | ≤3 на главу (≤2 у Vol. 2) | пасивно: менше шкоди, бонус окремим літерам, імунітет до статусів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click tile)` → ЯКЩО `path_adjacent6(prev, tile)` → ТО `custom: «плитка додається до слова; повторний клік по останній — прибрати»`.
- КОЛИ `input(submit)` → ЯКЩО `length(word) >= 3` і `in_dictionary(word)` → ТО `score(word_value)`, `clear(path)`, `after → fall(column)`, `spawn_at(tile, top)`; інакше `block`.
- Рахунок слова: Σ вартостей літер (рідкісні — дорожчі) × множник довжини × множники бонусних плиток (?).
- КОЛИ `after(clear)` → ЯКЩО `length(word)` великий → ТО `spawn_at(bonus_tile, top|random)` — зелена падає зверху, золота/сапфір/діамант замінюють випадкову плитку; довше слово → кращий камінь.
- КОЛИ `turn_end` → ТО для кожної червоної: `move(down)`, `destroy(tile below)` — «пропалює» колонку.
- КОЛИ `turn_end` → ЯКЩО `rng(p(level))` → ТО `spawn_at(burning_tile, top)`; з рівнем частота росте; короткі слова теж провокують вогонь (?).
- Бонусні плитки витриваліші: вогонь пропалює зелену за 2 ходи, золоту — за 3.
- КОЛИ `reach(burning_tile, bottom)` → ТО Classic: її треба вжити в слові цього ж ходу, інакше `lose`; Action: 10 с на гасіння, інакше `lose`.
- КОЛИ `input(click Lex)` → ТО `custom: «перемішати всі плитки»`, `spawn_at(burning_tiles)` — штраф за перемішування.
- КОЛИ `custom: «складено bonus word»` → ТО `score(bonus)`, наступне bonus word дорожче.
- КОЛИ `counter(level_points, >=, goal)` → ТО `next_level`, складність (частота вогню) росте.
- Перемога: нема (рекорд) · Поразка: палаюча плитка внизу не погашена · Рахунок: очки + рівень.
- **Adventures:** КОЛИ `input(attack word)` → ТО `damage(enemy, f(letters, length))` (довші слова й рідкісні літери — більше шкоди); ЯКЩО в слові самоцвіт → ТО його ефект (`heal`, `set_state(enemy, weakened)` тощо).
- **Adventures:** КОЛИ `turn_end(player)` → ТО ворог: `damage(lex)` / `set_state(lex, debuff)` / `heal(self)` / `set_state(tile, locked|smashed …)`.
- **Adventures:** КОЛИ `input(scramble)` → ТО нові літери, але хід втрачено — ворог б'є безкарно.
- **Adventures:** КОЛИ `hp_zero(enemy)` → ТО наступний ворог; бос → `give(treasure)`; Survival Battles — без лікування між ворогами. КОЛИ `hp_zero(lex)` → ТО `lose` (переграти бій).

## Керування і ввід
- Мишка/тап по плитках по черзі, кнопка Submit (або клік по останній плитці двічі (?)); правий клік / кнопка — скинути слово (?).
- Classic: без часу; Action: тиск таймера на спуск вогню.
- Adventures: плитки з 4×4 у будь-якому порядку; кнопки Attack, Scramble, зілля, вибір скарбів перед главою.

## Вікна, меню, HUD
- `main-menu` / `mode-select`: Classic · Action · (Deluxe) Hall of Fame · Options · Help.
- `game-screen`: поле, поточне слово й вартість (`word-preview`), очки, шкала рівня (`level-progress`), рядок `bonus-word`, Lex.
- `end-screen`: рахунок, найкраще/найдовше слово (?), запис у Hall of Fame.
- `leaderboard`: Hall of Fame (Deluxe).
- `codex-window`: «книги» слів за категоріями — перше слово категорії відкриває книгу й показує повний список (деякі версії).
- Adventures: мапа глав (`world-map`), бойовий екран з HP Лекса й ворога (`hp-bar`), `inventory-window` (скарби/зілля), Tome of Knowledge (`codex-window` ворогів, після Книги 1), міні-ігри (після Книги 2), Arena з таймером (після Книги 3), Clips and Giggles.

## Фічі поза полем
- Режими: `mode-classic` (без часу), `mode-time-attack` (Action), Hall of Fame.
- Прогресія: рівні з наростанням вогню; у Adventures — 3 книги × 10 глав, боси, скарби, зілля, `level-unlock` режимів.
- Міні-ігри Adventures: вгадати таємне слово / скласти якомога більше слів із заданих літер; нагорода — зілля.
- `save-progress`; DS/TAG-версії — мультиплеєр.

## Варіації й родичі
- Boggle (шлях по сусідах), SpellTower (гравітація + тиск), Wordtris, Letterpress, Bejeweled-логіка «зникло → упало зверху» (PopCap).
- Bookworm Adventures Vol. 2 (2009): книги 4–6, компаньйони (ефект кожні 4 ходи), Adventure Replay з бейджами.
- Bookworm Deluxe — оновлена графіка, Action, Hall of Fame.
- **Осі варіацій:** сусідство (6 гекс / 8 / будь-які літери — Adventures) · загроза (вогонь знизу / таймер / ворог з ходом) · винагорода довжини (бонус-плитки / шкода / очки) · результат слова (очки / удар / лікування).

## Цікавинки для курсу
- Сусідство в зміщених колонках (offset-координати гекса): хто сусід плитки (c, r) — 🌱.
- Падіння в колонці й поповнення зверху з ваговим розподілом літер — 📎.
- Палаючі плитки: спуск щоходу з руйнуванням, різна «міцність» бонусних плиток, програш на дні — 📎.
- Бонусні плитки за довжину слова (рівні: зелена → золота → сапфір → діамант) — 🌱.
- Перемішування зі штрафом як рятувальний клапан — 🌱.
- Adventures: бій «слово = удар» з таблицею шкоди по літерах, статусами ворога на плитках і зіллями — 🥈.

## Мапа на каталог
- Є: `cell-click` · `gravity-fall` ↔ осідання колонок · `spawn-random-cell` ↔ нові літери зверху й вогонь · `event-points` ↔ вартість літер · `combo-multiplier` ↔ множники бонус-плиток · `score-records` / `leaderboard` ↔ Hall of Fame · `difficulty-levels` / `progress-acceleration` ↔ частішає вогонь · `player-death` ↔ бібліотека згоріла · `time-out` ↔ 10 с в Action · `sequential-levels` / `level-unlock` ↔ рівні, глави, режими · `save-progress` · `hp-damage` ↔ бій Adventures · `inventory-items` ↔ зілля/скарби · `temporary-modes` ↔ статуси · `profile-stats` · `event-effects` · `end-screen` · `game-screen` · `main-menu` · `help-window` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+word-validation` — див. wordle.md; `+path-trace-word` — див. nyt-connections.md (тут 6-сусіди).
  - `+word-length-scoring` — див. spelltower.md.
  - `+burning-tile` «Плитка-загроза, що спускається й руйнує» · entities/move · 📎 · слоти {step: turn|seconds, durability}.
  - `+bonus-tile-tier` «Бонусна плитка за довжину слова» · entities/spawn · 🌱 · слоти {tiers: table}.
  - `+board-shuffle-penalty` «Перемішати поле зі штрафом» · game-logic/difficulty · 🌱 · слоти {penalty}.
  - `+bonus-word` «Задане слово з бонусом, що дорожчає» · game-logic/score · 🌱.
  - `+word-as-attack` «Слово як удар: шкода з літер» · entities/combat · 🥉 · слоти {damage_table}.
  - `+status-tile` «Ворог псує плитки (замок, знецінення, отрута)» · entities/state · 📎 (?).
  - `+word-category-book` «Колекції слів за категоріями» · levels/progression · 📎.

## Пропозиції до словників
- `+trigger:input`, `+trigger:turn_end` (⏳), `+trigger:after` (⏳), `+trigger:reach` (⏳) — вогонь на дні.
- `+cond:in_dictionary`; `+cond:path_adjacent6` — сусідство в зміщених колонках; `+cond:length`.
- `+effect:clear`, `+effect:fall`, `+effect:spawn_at`, `+effect:transform` (камінь замінює літеру), `+effect:damage`, `+effect:heal`, `+effect:set_state` (статуси плиток).
- `+role:tile`, `+role:hazard` (⏳) — палаюча плитка, `+role:boss` (⏳).
- `+ui:word-preview` (див. spelltower.md), `+ui:level-progress` — шкала очок до рівня; `+ui:bonus-word` — рядок зі словом-бонусом; `+ui:hp-bar` (⏳).
- `+window:mode-select`, `+window:codex-window` (книги слів, Tome of Knowledge), `+window:inventory-window` (⏳).
- `+feature:hall-of-fame` — локальна таблиця рекордів з іменами; `+feature:mode-time-attack` (⏳).
- `+axis:control` — у Classic вибір плиток по одній, а не «шлях-свайп».

## Джерела
- ⭐ [Wikipedia: Bookworm](https://en.wikipedia.org/wiki/Bookworm_(video_game)) — Classic/Action, правила вогню, бонус-плитки і їхня «міцність», Lex, bonus words, книги, платформи.
- [Wikipedia: Bookworm Adventures](https://en.wikipedia.org/wiki/Bookworm_Adventures) — бій словами, самоцвіти, зілля, скарби, режими, Vol. 2.
- [Steam: пошук Bookworm](https://store.steampowered.com/search/?term=bookworm) — Adventures знято з продажу 2016.
- YouTube: пошуки «bookworm deluxe popcap gameplay», «bookworm adventures gameplay».

## Непевне
- Fandom (402) і StrategyWiki (403) недоступні, WebSearch вичерпано — деталі понад Wikipedia з памʼяті.
- (?) Розмір поля 7×8 і 6-сусідство — з памʼяті; вікі каже лише «adjacent letters».
- (?) Пороги довжини для каменів, множники, точна формула очок; чи короткі слова провокують вогонь.
- (?) Повний список самоцвітів Adventures (Amethyst, Emerald, Sapphire, Garnet, Ruby, Crystal, Diamond) і статусів плиток (locked, smashed, poisoned, plagued) — вікі називає лише лікування/ослаблення й Diamond.
- (?) Розмір поля Adventures 4×4.
