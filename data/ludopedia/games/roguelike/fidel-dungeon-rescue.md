---
title: Fidel Dungeon Rescue
slug: fidel-dungeon-rescue
aka: [Fidel, Fidel Dungeon Rescue Anniversary Edition]
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: setup
  goal: state
year: 2017
platforms: [PC (Windows), macOS, iOS]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/573170/Fidel_Dungeon_Rescue/", best: true, note: "трейлер і суть: «roguelite, де можна перемотати й знайти оптимальний шлях»; 1.08.2017, Daniel Benmergui"}
  - {kind: itch, url: "https://danielben.itch.io/fidel-dungeon-rescue", note: "Anniversary Edition: три нові світи, щоденний світ, «більше терпимості до помилок»"}
  - {kind: other, url: "https://kotaku.com/a-puzzle-game-about-a-dungeon-delving-dog-1797274347", note: "Kotaku: слід не дає повернутися, слабкі місця ворогів (охоронець ззаду, рослина й пагінці), перемотка"}
  - {kind: other, url: "https://kotaku.com/my-new-healthier-mobile-game-obsession-is-fidel-dunge-1829866199", note: "Kotaku (iOS): серця, павуки, червоні павуки «трійкою», XP → рівень → серця, сходи з порогом XP, привид"}
  - {kind: other, url: "https://saveorquit.com/?p=68276", note: "огляд: монети → бомба або лікування, привид після смертей, режими й кількість рівнів"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2990054957", note: "гайд досягнень: клавіші (Ctrl — гавкіт, Delete — undo), міміки, Robot/Zombie Dog і їхні здібності за монети, режими"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=573170&count=30&maxlength=0&format=json", note: "новини Steam (API): зміни привида, XP-воріт, змій, аптечки по версіях"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Fidel+Dungeon+Rescue+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, keyboard-controls, visited-trail, self-collision, path-cut, undo-redo, hp-damage, item-pickup, inventory-items, round-currency, button-toggle, reach-exit, stairs-levels, sequential-levels, dungeon-generation, player-death, timeout-punisher, status-effects, daily-puzzle, streak-stats, achievements-window, +leash-no-cross, +xp-level-up, +xp-gate, +bark-action, +backstab-facing, +sleeping-enemy, +kill-streak-heal, +mimic-copy, +variable-player-powers, +boss-fight, +escort-npc, +multiple-endings, +ghost-chaser-after-death, +swap-entrance-exit, +menu-as-level]
proposes: ["+trigger:bark", "+effect:face(a, toward)", "+cond:from_side(a, b, side)", "+cond:on_trail(cell)", "+ui:xp-gate-counter", "+window:hub-level", "+feature:swap-start-exit", "+card:leash-no-cross", "+card:xp-gate", "+card:bark-action", "+card:ghost-chaser-after-death"]
author: opus
date: 2026-11-09
---

# Fidel Dungeon Rescue — пес на повідку: шлях не перетинає себе, кожен укус коштує серце, а помилку можна відмотати

## Суть
Пес Фідель проходить процедурні кімнати-підземелля від сходів-входу до сходів-виходу, щоб урятувати бабусю. Повідець тягнеться за ним: пройдена клітина стає непрохідною, тож маршрут — це шлях без самоперетинів через ворогів, скарби й пастки. Бій — просто вхід у клітину ворога, ціна — 1–2 серця, нагорода — XP, а рівні дають нові серця; у кожного ворога є «слабке місце» (зі спини, після гавкоту, трійкою підряд), яке робить укус безкоштовним. Головний інструмент — перемотка кроків: гра заохочує пробувати й відкочувати, як у пазлі.

## Поле і час
- Кожен поверх — один екран-кімната на квадратній сітці (розмір (?)), видимий цілком; вміст скринь прихований до гавкоту (`info: partial`), «правила» ворогів гравець відкриває сам.
- Хід = крок Фіделя (або гавкіт / предмет); вороги реагують покроково (робопес дзеркалить ходи).
- Генерація: більшість рівнів процедурні (`random: setup`), частина — ручні (сюжетні, шахи, «Індіана Джонс»); щоденний виклик — фіксований рівень дня.
- Реальний час лише як тиск: привид-таймер (у різних версіях — після першої смерті або завжди) і ліміти міні-режимів (Puzzle: 6 екранів за 6 хв; Centipede: 5 за 4 хв).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фідель | player | серця (3 на старті з 2022), XP, рівень, монети, бомби, самоцвіти | крок 4 напрямки; вхід у ворога = укус |
| Повідець (слід) | static | — | пройдена клітина; непрохідна для Фіделя; крок назад по ньому = undo |
| Сходи-вхід / сходи-вихід | static | поріг XP (у воротах) | Enter на виході — далі; Enter на вході — поміняти вхід і вихід місцями |
| XP-ворота | gate | число й ланцюги | вихід закритий, доки XP < порога (після 2022 — лише в навчанні) |
| Павук | enemy | −1 серце | укус коштує серце, дає XP |
| Маленький павук | enemy | 0 сердець | укус безкоштовний; гавкіт підриває |
| Червоний павук | enemy | — | третій підряд у серії перевертається й гине без втрати серця |
| Вартовий зі списом (tribal warrior) | enemy | спить / пильнує | безпечний укус ззаду; XP лише поки спить |
| Рослина-песоїд | enemy | пагінці | в'яне, коли потоптано всі малі пагінці; має явний патерн атаки |
| Гном | enemy | — | заганяти на шипи (за оглядом (?)) |
| Змія / зміїне яйце | enemy | отрута | лише змії отруюють Фіделя (з 2022) |
| Вампір | enemy | — | особлива умова вбивства (?), 5 XP |
| Черепаха | enemy | орієнтація | гавкіт розвертає |
| Мімік | enemy | 5 XP | скриня, що кусає; безпечно — з боку завіс (згори) |
| Скриня | container | золото або «зуби» | гавкіт поруч показує вміст |
| Монета | resource | — | валюта здібностей/крамниці |
| Аптечка (medkit) | pickup | +серця | у крамниці Фіделя за монети |
| Бомба | pickup | — | знищує клітину/ворога, кнопку, відкриває таємні двері |
| Кнопка | switch | — | наступити або підірвати |
| Шипи | hazard | — | шкодять; пастка для гномів |
| Свічка | switch | горить / згасла | гавкіт гасить; згаслі свічки відкривають портал |
| Робопес (бос) | boss | — | дзеркалить ходи Фіделя, викрадає бабусю |
| Зомбі / Кігть дракона / Кошмар (боси) | boss | серця | Кошмар (Underworld) імунний до бомб і хробаків |
| Привид | enemy | таймер | приходить по Фіделя; спіймав — кінець забігу (у старих версіях — назад на 1-й поверх) |
| Бабуся | neutral | — | ціль порятунку; викрадена — врятувати = кінцівка «Good Dog!» |
| Тенісний м'яч | object | — | штовхається, переноситься між рівнями (режим Fetch) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` and `not custom: «клітина — повідець»` → ТО `move(fidel, dir)`, `custom: «клітина стає повідцем»`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «клітина — повідець, але не попередня»` → ТО `block`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «клітина — попередня на повідці»` → ТО `undo(1)` (крок назад згортає повідець).
- КОЛИ `input(undo)` → ТО `undo(1)`: відмотати крок без штрафу (redo нема).
- КОЛИ `contact(fidel, enemy)` → ТО `damage(1|2)`, `disappear(enemy)`, `counter(xp, +n)`; ЯКЩО `hp_zero(fidel)` → смерть.
- КОЛИ `contact(fidel, enemy)` → ЯКЩО `custom: «зі спини»` → ТО `disappear(enemy)` без втрати серця.
- КОЛИ `input(bark)` → ТО `face(enemies, fidel)` (вороги розвертаються до пса — спина відкрита іншим), `reveal(chest)`, `rotate(turtle)`, `custom: «маленькі павуки вибухають»`, `custom: «свічка гасне»`.
- КОЛИ `contact(fidel, guard)` → ЯКЩО `state(guard, asleep)` → ТО `counter(xp, +n)`; інакше `custom: «без XP»`.
- КОЛИ `died(red_spider)` → ЯКЩО `chain(3)` → ТО `custom: «без втрати серця»`.
- КОЛИ `all_gone(bud)` → ТО `disappear(plant)` (рослина в'яне).
- КОЛИ `contact(fidel, mimic)` → ЯКЩО `custom: «з боку завіс (згори)»` → ТО `disappear(mimic)`, `counter(xp, +5)`; інакше `damage(n)`.
- КОЛИ `contact(fidel, snake)` → ТО `set_state(fidel, poisoned)`.
- КОЛИ `counter(xp, >=, поріг)` → ТО `custom: «рівень +1, більше сердець»`.
- КОЛИ `contact(fidel, coin)` → ТО `currency(+1)`; КОЛИ `input(shop)` → ЯКЩО `counter(coins, >=, ціна)` → ТО `custom: «бомба або аптечка (Фідель)»`.
- КОЛИ `use(fidel, bomb)` → ТО `custom: «знищити ворога / кнопку / таємну стіну»`; XP за підірваного ворога зараховується.
- КОЛИ `enter(fidel, exit)` → ЯКЩО `counter(xp, >=, gate)` → ТО `next_level`; інакше `block`.
- КОЛИ `input(enter)` → ЯКЩО `custom: «Фідель на сходах-вході»` → ТО `custom: «вхід і вихід міняються місцями»`.
- КОЛИ `died(fidel)` → ЯКЩО `first_time` → ТО `custom: «попередження, хвилина на рівень (v2.7)»`; інакше `spawn(ghost)`; КОЛИ `contact(ghost, fidel)` → ТО `restart` (з першого поверху — у ранніх версіях).
- Zombie Dog: КОЛИ `chain(3)` або `died(large_enemy)` → ТО `heal(dog, 1)`; аптечок не бере; 3 монети — хробаки в сусідні клітини, 9 — хробаки по екрану.
- Robot Dog: XP не отримує; 3 монети — `custom: «знищити всіх ворогів у ряду й стовпці»`; 9 — купити серця.
- КОЛИ `custom: «бабусю повернуто»` and `level_end` → ТО `win` (кінцівка «Good Dog!»); проходження Underworld за Robot/Zombie Dog — їхні кінцівки.
- Перемога: дійти до виходу останнього поверху (Level 15, далі Underworld 10). Поразка: привид/смерть. Рахунок: XP; щоденний виклик — XP-ціль, кістка за розвʼязок.

## Керування і ввід
- Стрілки — крок; Ctrl — гавкіт; Delete — undo кроку (на геймпаді — L-плече); Enter — перейти сходами далі / на вході поміняти вхід і вихід; Esc — меню (версія, текстовий показ XP).
- Клавіатура й Xbox-контролер (itch, Steam: повна підтримка контролера); iOS — тач (?).
- Здібності за монети — зі слотів інвентарю (?).

## Вікна, меню, HUD
- `game-screen`: кімната, серця, XP-смуга (опційно числом), монети, бомби/самоцвіти, слід-повідець.
- `+window:hub-level`: меню — це сам ігровий рівень: міст до бонусних режимів, тенісний м'яч, хот-доги вибору пса (з'їсти = обрати Zombie/Robot Dog).
- `pause-menu` (Esc): налаштування, версія; `settings-window` (текстовий XP, мови — 9).
- `achievements-window` (Steam, 25), `end-screen` / кінцівки (Good Dog!, Fidel, Zombie, Robot), титри.
- Переходи: хаб → Level 1…15 → червоний портал → Underworld 1…10 → Afterlife; хаб → міст → Puzzle / Centipede / Cemetery / щоденний.

## Фічі поза полем
- `undo` (покроковий, без штрафу) — ядро; `mode-daily` / `daily-puzzle` («Bones»: розв'язок дня = кістка; 319 кісток — досягнення); `streaks`-подібний лічильник кісток.
- Режими: основна пригода (15 рівнів), Underworld (друге проходження, 10), Cemetery (привид), Puzzle (6 екранів / 6 хв), Centipede (5 екранів / 4 хв), Fetch (м'яч), таємні рівні (шахи, НЛО-вечірка, Flashback, кімната з хот-догами).
- `unlockables`: Robot Dog (пройти Puzzle), Zombie Dog (пройти Centipede); «гра в грі» — повна інша гра як великодня пасхалка (оновлення 2.5).
- `autosave` посеред забігу; Steam Cloud; `localization`; `achievements`.

## Варіації й родичі
- Сімейні сусіди: [desktop-dungeons](desktop-dungeons.md) і [magic-tower](magic-tower.md) (бій як ціна маршруту), [crypt-of-the-necrodancer](crypt-of-the-necrodancer.md) (патерни ворогів), [card-dungeons](card-dungeons.md).
- Заборона самоперетину — як у змійці (сімʼя `maze-arcade`) і в шляхових пазлах типу Flow/LYNE; тут слід — повідець, а undo — «змотати повідець».
- Версії (новини Steam): 2.0 (2017-12) — нові світи й режими, м'якший привид; 2.5 — щоденні виклики; 2.7 — попередження й хвилина після першої смерті; Anniversary (2018-11) — без таймера привида; Cerebral Puzzles (2022-05) — привид лише за таймером, смерть без штрафу, 3 серця на старті, XP-ворота лише в навчанні, аптечка в крамниці.
- Осі варіацій: **слід** (нема / блокує / стирається undo) · **ціна бою** (фіксоване серце / безкоштовно за умови: ззаду, сплячий, трійка) · **тиск** (привид після смерті / таймер / нема) · **пес** (Фідель — XP і аптечки; Robot — без XP, удар по ряду й стовпцю; Zombie — лікування комбо).

## Цікавинки для курсу
- Повідець: пройдені клітини блокують, крок назад по ньому = undo — 🌱 (стек позицій = і слід, і історія).
- Слабкі місця ворогів (ззаду, після гавкоту, сплячий, трійка підряд) як таблиця умов «укус безкоштовний» — 📎.
- Гавкіт як глобальна дія з різними реакціями (розвернути, підірвати, розкрити скриню, загасити свічку) — 📎 (interaction-table).
- XP-ворота: вихід відкривається лише після набору XP — маршрут мусить «зібрати» достатньо — 🌱.
- Генератор кімнат, що гарантує прохідність без самоперетину з потрібним XP — 🥇 (пошук гамільтоново-подібного шляху з обмеженнями).
- Робопес-дзеркало: ворог, що повторює ходи гравця — 🌱.
- Привид-таймер після першої смерті — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` · `visited-trail` + `self-collision` (повідець) · `path-cut` (крок назад згортає хвіст) · `undo-redo` · `hp-damage` · `item-pickup` + `inventory-items` (бомби, аптечки) · `round-currency` (монети) · `button-toggle` · `reach-exit` + `stairs-levels` + `sequential-levels` · `dungeon-generation` · `player-death` · `timeout-punisher` (привид) · `status-effects` (отрута) · `daily-puzzle` + `streak-stats` (кістки) · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+leash-no-cross` «Шлях не перетинає себе; згортання = undo» · entities/move · 🌱 (дитина `visited-trail`).
  - `+xp-gate` «Вихід відчиняється за порогом XP» · game-logic/win · 🌱.
  - `+bark-action` «Глобальна дія-звук: кожен тип реагує по-своєму» · entities/interact · 📎.
  - `+ghost-chaser-after-death` «Після смерті приходить переслідувач з таймером» · game-logic/lose · 🌱.
  - `+kill-streak-heal` «Серія вбивств лікує / робить укус безкоштовним» · entities/combat · 🌱.
  - `+swap-entrance-exit` «Поміняти старт і фініш місцями» · levels/progression · 🌱.
  - `+menu-as-level` «Меню — ігровий рівень» · interface/menus · 📎.
  - Повтори з корпусу: `+xp-level-up`, `+backstab-facing`, `+sleeping-enemy`, `+mimic-copy` (робопес), `+variable-player-powers`, `+boss-fight`, `+escort-npc` (бабуся), `+multiple-endings`.

## Пропозиції до словників
- `+trigger:bark` — гравець подав «звук» (гавкіт), на який реагують усі в радіусі; поки — `input(bark)`.
- `+effect:face(a, toward)` — розвернути сутність до цілі (у словнику `face(a, dir)` — лише до напрямку).
- `+cond:from_side(a, b, side)` — A входить у B з певного боку (ззаду, з боку завіс).
- `+cond:on_trail(cell)` — клітина належить сліду / повідцю.
- `+ui:xp-gate-counter` — число й ланцюги на виході: скільки XP бракує.
- `+window:hub-level` — меню як прохідний ігровий рівень.
- `+feature:swap-start-exit` — поміняти вхід і вихід рівня для оптимізації маршруту.
- `+card:leash-no-cross`, `+card:xp-gate`, `+card:bark-action`, `+card:ghost-chaser-after-death` — див. «Мапу на каталог».

## Джерела
- ⭐ [Steam: Fidel Dungeon Rescue](https://store.steampowered.com/app/573170/Fidel_Dungeon_Rescue/) — трейлер, «roguelite з перемоткою», дата, розробники (Daniel Benmergui, Jeremías Babini, Hernán Rozenwasser), теги Grid-Based Movement / Procedural Generation.
- [itch.io: Fidel Dungeon Rescue](https://danielben.itch.io/fidel-dungeon-rescue) — Anniversary Edition: світи, щоденний світ, клавіатура й Xbox-контролер.
- [Kotaku (2017)](https://kotaku.com/a-puzzle-game-about-a-dungeon-delving-dog-1797274347) — слід без повернення, самозамикання, слабкі місця (охоронець ззаду, рослина й пагінці), перемотка.
- [Kotaku (2018, iOS)](https://kotaku.com/my-new-healthier-mobile-game-obsession-is-fidel-dunge-1829866199) — серця, павуки й червоні павуки, вампіри, робопес-дзеркало, XP і рівні, сходи з порогом XP, привид.
- [Save or Quit: огляд](https://saveorquit.com/?p=68276) — монети → бомба / повне лікування, вартовий дає XP лише сплячим, привид після смертей, режими.
- [Steam-гайд досягнень](https://steamcommunity.com/sharedfiles/filedetails/?id=2990054957) — клавіші, гавкіт розвертає ворогів, міміки (5 XP, атакувати згори), Robot/Zombie Dog і їхні здібності, Puzzle 6/6 і Centipede 5/4, кістки.
- [Steam News API: новини гри](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=573170&count=30&maxlength=0&format=json) — історія змін привида, XP-воріт, змій, аптечки, щоденних.

## Непевне
- (?) Розмір кімнати в клітинах і чи бувають кімнати більші за екран.
- (?) Правило вампіра: «треба не мати здоров'я» (Save or Quit) чи «засинає, коли його здоров'я вичерпане, тоді 5 XP» (Kotaku) — джерела розходяться.
- (?) Що саме дає гавкіт для XP (досягнення «XP Overdrive»: «гавкіт може перевищити потрібний XP»), і чи будить він сплячих.
- (?) Привид: між версіями мінялось усе (після 2 смертей → хвилина після першої → без таймера → «лише за таймером»); поточна поведінка не перевірена.
- (?) Скільки серць коштує кожен тип ворога (огляди: «здебільшого 1–2»), ліміт перемотки, керування на iOS.
