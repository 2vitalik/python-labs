---
title: BroomSweeper
slug: broomsweeper
aka: [Broom Sweeper]
family: hidden-deduction
also: [roguelike]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: both
  goal: state
year: 2026
platforms: [PC (Windows), Steam Deck]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3473250/BroomSweeper/", best: true, note: "опис: сапер-роглайк, 16 поверхів, візок і торгові автомати, боси → ключі, 7 хазматів, персонажі, 16 ascension; демо"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3473250&count=30&maxlength=6000", note: "патчноути 1.1–2.0 (JSON): хазмати, ключі, персонажі, брехливі числа, Daily/Holiday Shifts, Infinity Mode, сіди"}
  - {kind: other, url: "https://www.pcgamer.com/games/roguelike/this-minesweeper-roguelike-is-a-chaotic-corporate-nightmare-and-i-love-it", note: "огляд PC Gamer (текст у фетчі не відкрився)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=BroomSweeper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [cell-click, neighbor-count-clue, chord-click, dot-mark, hp-damage, inventory, inventory-items, round-currency, shop-catalog, run-relics, blob-growth, multi-cell-size, stairs-levels, permadeath, daily-puzzle, seed-share, difficulty-levels, character-select, codex-window, achievements-window, game-settings, game-screen, end-screen, main-menu, +liar-clue, +boss-fight, +ascension-levels, +run-meta-carry, +key-abilities, +event-choice, +first-sweep-opening, +office-end-payout]
proposes: ["+trigger:office_end", "+effect:sweep", "+effect:cement", "+cond:lying", "+role:hazmat", "+ui:keyring", "+ui:number-style", "+window:vending-machine", "+window:event-choice", "+feature:holiday-shifts", "+card:key-abilities", "+card:event-choice", "+card:first-sweep-opening", "+card:office-end-payout", "+card:offset-lie-numbers"]
author: opus
date: 2026-11-09
---

# BroomSweeper — нічна зміна прибиральниці в офісній вежі: сапер-роглайк, де числа брешуть, цвіль їсть HP, а ключі босів міняють правила

## Суть
Роглайк на ядрі сапера: кожен офіс — поле плиток підлоги, під частиною яких сидять пилові кролики (міни). Клік «підмітає» плитку й відкриває число сусідів-кроликів; знак «обережно» — прапорець; кролик під мітлою — втрата HP, 0 HP — кінець зміни. Між офісами — торгові автомати з предметами для візка (сотні предметів із синергіями), події MOP з вибором, боси, за яких дають ключі-здібності. Чим далі в ніч, тим більше **хазматів** — цвіль, слимаки, мегакролики, щупальця, — і тим менше можна довіряти числам.

## Поле і час
- Офіс — квадратна сітка плиток; розмір росте з поверхом (є предмети, що розширюють офіс); «перше підмітання» (First Sweep) відкриває стартову ділянку.
- Шари: плитка (закрита / відкрита / зі знаком) + прихований вміст (кролик, хазмат) + число; деякі числа «брешуть».
- Хід = одна дія курсором; таймера нема (Steam: Playable without Timed Input).
- Забіг = зміна: поверхи від підвалу вгору, згруповані в A.C.T.-и; ACT 3 закінчується офісом боса. Infinity Mode додає A.C.T.-и.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Прибиральниця (персонаж) | player | HP, Max HP, $, предмети, ключі | 6 персонажів зі стартовими предметами/талантами |
| Плитка підлоги | tile | закрита / підметена / «обережно» | підмітання відкриває число сусідів-кроликів |
| Пиловий кролик (Dust Bunny) | hazard | — | міна: підмітання → втрата HP; можна «розтурбувати» (dusturb) |
| Мегакролик | hazard | радіус | займає область; «обережно» на відкритому мегакролику зараховує весь радіус для акорду |
| Нескінченний кролик (Infinity Bunny) | hazard | може бути зацементований | підмести зацементованого → звільнення (кінець забігу) |
| Кролик-привид | hazard | — | хазмат; ефект (?) |
| Цвіль | hazard | росте | розростається офісом і зʼїдає HP (і Max HP) |
| Слимак | hazard | слизькі плитки | плитки під слизом показують «свої» числа |
| Щупальце | enemy | — | зʼявляється (Tentacle Tantrum); його можна проткнути |
| Мішок сміття | hazard | — | хазмат; ефект (?) |
| Брехливе число | mark | зсув ∈ {−2, −1, +1, +2} | в офісі всі брехні зсунуті на однакову величину |
| Торговий автомат | neutral | товари, кнопка restock | продає предмети за $; можна «копнути» — перемішує товари |
| Предмет | pickup | тригер і ефект | пасивний / за умовою (напр., на 12-й акорд, на фінальний не-акорд) |
| Ключ боса | pickup | Duster / Pirate / Query… | нова здібність до кінця забігу |
| Смітник (dust dump) | switch | — | закриває офіс: виплата й ефекти «кінця офісу» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` (офіс) → ТО `custom: «перше підмітання: відкрити стартову ділянку»` (предмети можуть змінити її форму).
- КОЛИ `input(sweep, tile)` → ЯКЩО не `occupied(tile, dust_bunny)` → ТО `reveal(tile)`; число = `adjacent_count(tile, bunny, ==, n)`.
- КОЛИ `input(sweep, tile)` → ЯКЩО `occupied(tile, dust_bunny)` → ТО `damage(player, n)`.
- КОЛИ `input(caution, tile)` → ТО `mark(tile, caution)` (ПКМ).
- КОЛИ `input(chord, number)` → ЯКЩО `adjacent_count(number, caution, ==, n)` → ТО `reveal(neighbors)`; мегакролик зі знаком рахується всім радіусом.
- КОЛИ `level_start` → ЯКЩО `custom: «в офісі є брехливі числа (Dustin / хазмат)»` → ТО `custom: «частина чисел зсунута на однакове k ∈ {−2, −1, +1, +2}, k своє в кожному офісі»`.
- КОЛИ `custom: «прибрано пилового кролика»` → ТО `custom: «сусідні брехливі числа можуть змінитися»`.
- КОЛИ `turn_end` → ЯКЩО `count(mold, >, 0)` → ТО `custom: «цвіль розростається»`, `damage(player, n)` (?).
- КОЛИ `input(sweep, tile)` → ЯКЩО `state(infinity_bunny, cemented)` → ТО `lose` (звільнили).
- КОЛИ `hp_zero(player)` → ТО `lose`, `game_over` (permadeath).
- КОЛИ `input(dust_dump)` → ТО `currency(+base_pay)`; ЯКЩО `custom: «чисте прибирання»` → ТО `currency(+clean_sweep_bonus)`; `custom: «спрацьовують предмети кінця офісу»`, `next_level`.
- КОЛИ `input(buy, item)` → ЯКЩО `counter($, >=, price)` → ТО `currency(-price)`, `give(player, item)`.
- КОЛИ `input(kick, vending_machine)` → ТО `custom: «товари й кнопка restock переміщуються»`.
- КОЛИ `custom: «подія MOP»` → ТО `choose(options)` (напр., Confiscation Station забирає частину ресурсів).
- КОЛИ `destroyed(boss)` → ТО `give(player, key)`; Duster Key — `custom: «відкрити плитку, якщо на ній нема кролика»` (?), Pirate Key — `custom: «відкриває кроликів замість розтурбовування»`.
- КОЛИ `input(chord)` → ЯКЩО `occupied(tile, query_mark)` → ТО `unmark(tile)` («?» від Query Key).
- КОЛИ `input(shift_survived)` → ТО `win` (зміну пройдено).
- Перемога: пройти всі поверхи до ранку · Поразка: 0 HP або звільнення · Рахунок: $ за офіси, статистика Handbook.

## Керування і ввід
- Миша: ЛКМ — підмести, ПКМ — знак «обережно», клік по числу — акорд (зелена підсвітка сусідів).
- ПКМ по відкритому числу — статистика й історія плитки.
- Повна підтримка контролера (DualShock / DualSense), режими лише миша / лише тач; Steam Deck — ПКМ правим трекпадом.

## Вікна, меню, HUD
- `main-menu`: нова зміна → `character-select` (6 персонажів, резюме); `mode-select`: звичайна зміна / Daily Shift / Holiday Shift / Infinity Mode / сід.
- `difficulty-select`: 16 рівнів ascension.
- `game-screen`: офіс, `hp-bar` (HP / Max HP), `coins` ($), `inventory-bar` (візок), `keyring`, `remaining-counter` (?), номер поверху, кнопка смітника «Shift Survived».
- `vending-machine` (`shop-window`): товари, ціна, restock, удар ногою.
- `event-choice`: подія MOP з варіантами та наслідками.
- `codex-window` — Employee Handbook: предмети, MOP-и, хазмати, ключі, лор, досягнення, персонажі з відсотком перемог.
- `achievements-window` (Steam), `settings-window`: стиль чисел (OG / Light / Colored / Retro / Full Color, Full Color Blind), масштаб анімацій, гучність, камера.
- `end-screen`: зміну пройдено / звільнено, виплати.

## Фічі поза полем
- `meta-progression`: очки між забігами на стартові бонуси; персонажі й ключі відкриваються.
- `difficulty-presets` — 16 ascension; Golden Bunny — позначка «чесного» забігу (знімається, якщо вимкнути хазмати чи продовжити зміну).
- `mode-daily` — Daily Shift: 3 модифікатори (добрий / нейтральний / поганий), поверх залежить від дня тижня; Holiday Shifts — святкові виклики.
- `mode-endless` — Infinity Mode (після першої успішної зміни); `seed-input` — сідовані забіги.
- `codex`, `achievements`, `cloud-save`, `colorblind-palette`, `gamepad-support`, `touch-controls`.

## Варіації й родичі
- [Minesweeper](minesweeper.md) — ядро; [DemonCrawl](demoncrawl.md), [Dragonsweeper](dragonsweeper.md), [Necrosweeper](necrosweeper.md) — сапер-роглайки з HP і предметами.
- [14 Minesweeper Variants](14-minesweeper-variants.md) — правило Liar (±1); тут брехня — однаковий зсув на офіс з набору ±1/±2, плюс персонаж-брехун.
- **Осі варіацій**: міна «миттєва смерть / шкода HP / ворог»; числа «правдиві / зсунуті на k / слизькі»; поле «статичне / цвіль росте / щупальця зʼявляються»; прогрес «один пазл / поверхи з босами й магазинами».

## Цікавинки для курсу
- Сапер з HP замість миттєвої смерті + акорд + знаки — 📎.
- Брехливі числа зі спільним зсувом k на офіс: гравець має вивести k разом із мінами — 🥈 (дедукція з невідомим параметром).
- Цвіль як клітинний автомат, що росте і шкодить, — 🥉.
- Мегакролик-міна радіусом r і зарахування всієї області до акорду — 📎.
- Предмети з тригерами («на 12-й акорд», «фінальний хід — не акорд») як шина подій забігу — 🥈.
- Торговий автомат із restock і «удар ногою» — 📎.
- Сідовані Daily Shifts з модифікаторами — 📎.

## Мапа на каталог
- Є: `cell-click` ↔ підмітання; `neighbor-count-clue` ↔ числа; `chord-click` ↔ акорд; `dot-mark` ↔ знак «обережно»; `hp-damage` ↔ кролик і цвіль; `inventory` + `inventory-items` ↔ візок; `round-currency` + `shop-catalog` ↔ $ і автомат; `run-relics` ↔ предмети забігу; `blob-growth` ↔ цвіль; `multi-cell-size` ↔ мегакролик; `stairs-levels` ↔ поверхи; `permadeath`; `daily-puzzle` ↔ Daily Shift; `seed-share` ↔ сіди; `difficulty-levels` ↔ ascension; `character-select`; `codex-window` ↔ Handbook; `achievements-window`; `game-settings` ↔ стилі чисел; `game-screen` / `end-screen` / `main-menu`.
- **Нема** → пропозиції карток:
  - `+liar-clue` (14 Minesweeper Variants) — тут слот {offset: ±1|±2, scope: office}.
  - `+boss-fight`, `+ascension-levels`, `+run-meta-carry` — уже пропоновані в корпусі.
  - `+key-abilities` «Нагорода боса — здібність, що змінює правила розвʼязання» · game-logic/progression · 📎.
  - `+event-choice` «Подія з вибором варіантів і наслідками» · game-logic/progression · 🌱.
  - `+first-sweep-opening` «Стартове відкриття ділянки, форма залежить від предметів» · levels/generation · 🌱.
  - `+office-end-payout` «Виплата за завершене поле + бонус за чистоту» · game-logic/score · 🌱.
  - `+offset-lie-numbers` «Брехливі числа зі спільним невідомим зсувом» · game-logic/constraints · 🥈.

## Пропозиції до словників
- `+trigger:office_end` — гравець закрив поле (смітник): виплати й предмети «кінця офісу».
- `+effect:sweep(tile)` — відкрити плитку з ризиком (зараз `reveal` + умова); `+effect:cement(a)` — зацементувати сутність, змінивши правило взаємодії.
- `+cond:lying(tile)` — число на плитці зсунуте.
- `+role:hazmat` — модифікатор поля з власною поведінкою (росте, змінює числа, спавнить).
- `+ui:keyring` — набір ключів-здібностей; `+ui:number-style` — перемикач стилю чисел (і для дальтоніків).
- `+window:vending-machine` — магазин як обʼєкт на мапі з restock; `+window:event-choice` — подія з варіантами.
- `+feature:holiday-shifts` — сезонні забіги з власними викликами.

## Джерела
- ⭐ [Steam: BroomSweeper](https://store.steampowered.com/app/3473250/BroomSweeper/) — premise, кролики й знаки «обережно», 16 поверхів, візок і автомати (100+ / 150+ предметів), боси → ключі, 7 хазматів і «числа не те, чим здаються», персонажі, 16 ascension, BandsWithLegends / Bandwidth Games, 19.01.2026, фічі доступності.
- [Steam News API, патчноути](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3473250&count=30&maxlength=6000) — хазмати (цвіль, слимаки, мегакролики, щупальця, нескінченні й привиди), брехливі числа ±1/±2, ключі Duster/Pirate/Query, автомат і удар ногою, MOP-и, A.C.T.-и, Handbook, Daily/Holiday Shifts, Infinity Mode, сіди, поверхи 0–13.
- [PC Gamer: огляд](https://www.pcgamer.com/games/roguelike/this-minesweeper-roguelike-is-a-chaotic-corporate-nightmare-and-i-love-it) — у фетчі лише заголовок.
- YouTube: пошук «BroomSweeper gameplay».

## Непевне
- (?) Скільки HP знімає кролик і чи це взагалі HP, а не «помилка» (як у DemonCrawl) — джерела кажуть лише «0 HP — кінець».
- (?) Поверхів: Steam — 16, патчноути 2.0 — «поверхи 0–13» (11–13 додано у 2.0); можливо, 16 рахує офіси босів чи A.C.T.-и.
- (?) Що саме робить «dusturb» (розтурбувати кролика) і як воно відрізняється від підмітання; ефекти привидів і мішків сміття.
- (?) Слимаки: патчноути то «числа сталі в межах офісу», то «відрізняються» — суперечність.
- (?) Цвіль росте за хід чи за подію — у правилі вище `turn_end` умовно.
- (?) 7 хазматів — ймовірно цвіль, слимаки, мегакролики, щупальця, мішки, нескінченні кролики, привиди — список зібрано з патчноутів, офіційного переліку не бачив.
- (?) Персонажі: Janae, Mae (числа-пікрос), Dustin (дискалькулія — брехливі числа), Cousteau, Han (Morphallaxis), Holly Day (святкові зміни); «Broom» — персонаж чи ні — неясно; Steam називає то 5, то 6.
