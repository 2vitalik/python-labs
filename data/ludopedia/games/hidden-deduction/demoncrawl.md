---
title: DemonCrawl
slug: demoncrawl
aka: [Demon Crawl]
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
year: 2019
platforms: [PC (Windows, macOS, Linux)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1141220/", best: true, note: "огляд фіч: 1000+ предметів, 60+ етапів, 100+ модів, 5 квестів, режими, Arena, майстерності"}
  - {kind: wiki, url: "https://demoncrawl.com/wiki/", note: "офіційна вікі: квести, складності, помилка, монстри, предмети, етапи, моди"}
  - {kind: wiki, url: "https://demoncrawl.com/wiki/index.php/Mistake", note: "помилка = клік по клітині з монстром; ефекти «до наступної помилки», серії без помилок"}
  - {kind: wiki, url: "https://demoncrawl.com/wiki/index.php/Stage_Mods", note: "моди етапу зі складністю: Nightmare, Dry, Withering, Trusty, Lofty…"}
  - {kind: wiki, url: "https://demoncrawl.com/wiki/index.php/Stages", note: "5 квестів × 10 етапів, сила етапу, ліміт монстрів, секретні етапи"}
  - {kind: wiki, url: "https://demoncrawl.com/wiki/index.php/Objects", note: "лут на полі: монети, діаманти, скрині, серця, душі, темні серця"}
  - {kind: wiki, url: "https://demoncrawl.com/wiki/index.php/Items", note: "типи предметів, броня зі слотами, мана, приклади"}
  - {kind: wiki, url: "https://demoncrawl.com/wiki/index.php/Strangers", note: "незнайомці: торговці, коваль, священник, гравець-ризикун"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=DemonCrawl+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, neighbor-count-clue, chord-click, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, round-currency, shop-catalog, shop-buyback, run-relics, status-effects, difficulty-levels, daily-puzzle, sequential-levels, world-map, no-guess-generation, mines-after-first-click, codex-window, achievements-window, leaderboard, online-multiplayer, mode-select, tutorial-window, save-progress, game-screen, end-screen, +mistake-damage, +stage-mods, +mistake-free-streak, +mana-charged-items, +armor-slots, +stranger-npcs, +omens, +meta-talents, +autosweeper-mode]
proposes: ["+trigger:mistake", "+trigger:streak", "+effect:omen", "+effect:fortify", "+cond:no_mistake_since", "+ui:mana-bar", "+ui:stage-mod-icons", "+feature:auto-sweep", "+feature:profiles", "+card:mistake-damage", "+card:stage-mods", "+card:mistake-free-streak", "+card:mana-charged-items", "+card:armor-slots", "+card:stranger-npcs", "+card:omens", "+card:meta-talents", "+card:autosweeper-mode"]
author: opus
date: 2026-11-09
---

# DemonCrawl — роглайт-сапер: помилка — не смерть, а удар монстра; квест із 10 етапів-полів із модами, сотні предметів і мана

## Суть
Кожен етап — поле сапера, де під клітинами монстри. Відкрити клітину з монстром — **помилка**: монстр бʼє, гравець втрачає життя, але не програє одразу. Між етапами й на самому полі — лут (монети, скрині, серця), незнайомці-торговці, предмети пасивні, разові й магічні (за ману), омени-прокляття. Квест — послідовність із 10 етапів, кожен з **модами**, що міняють правила поля (без прапорців, удвічі ширше, втрата життя щохвилини…). Між забігами — постійна прогресія: токени, таланти, майстерності. Класичний режим — чистий сапер.

## Поле і час
- Квадратна сітка сапера; розмір і кількість монстрів — за етапом і модами; максимум звичайного поля 2025 клітин, монстрів ≥ 1 і ≤ 95 % клітин.
- Шари: приховані монстри + відкриті числа + обʼєкти (лут, незнайомці, орієнтири) поверх клітин + аури (?) на клітинах.
- Хід = дія гравця (відкрити клітину); багато ефектів рахують «ходи» («на N ходів», «щоходу»). Є й таймерні моди (Withering — щохвилини).
- Обʼєкт на клітині ховає її число (без Magnifying Glass).
- Квест — 10 етапів у фіксованому порядку (5 основних квестів), між ними мапа (?); Endless Multiverse змішує й рандомізує етапи.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | життя, макс. життя, захист, мана, монети, інвентар | не на полі; діє кліком; 0 життів — смерть (є відродження предметами) |
| Закрита клітина | static | прихована: монстр / порожньо | відкривається кліком |
| Відкрита клітина з числом | mark | n монстрів серед 8 сусідів | підказка; дає ману (?) |
| Монстр | enemy | тематичний для етапу, шкода в межах сили етапу | відкритий кліком → атакує (помилка); відкритий — зазвичай вже не шкодить; дропає лут |
| Бос | boss | — | на окремих етапах; посилюється Темним серцем |
| Прапорець | mark | — | позначає монстра; мод Nightmare забороняє |
| Монета / Діамант / Фіолетовий діамант | pickup | +1 / +5 / +25–50 монет | клік — у гаманець |
| Токен / Мега-токен | pickup | +1 / +10–30 | валюта мета-прогресії |
| Скриня | container | вміст росте з силою етапу | предмет або монети |
| Спеціальна скриня | container | тема | бонус-ефект + предмет з тематичного пулу |
| Серце | pickup | +1 життя | лікує |
| Душа | pickup | +1 життя і +1 макс. | сіре серце |
| Темне серце | pickup | — | посилює боса(ів) етапу |
| Артефакт | pickup | тема етапу | для крафту Heirloom і входу в Beyond |
| Кістки | object | — | предмет, що лишився на полі замість інвентаря |
| Незнайомець | neutral | ціна | торгує або дає послугу (Nomad, Blacksmith, Priest, Gambler…) |
| Орієнтир (landmark) | static | — | обʼєкт етапу з ефектом (?) |
| Предмет пасивний / разовий / магічний / омен / легендарний | — | слот, ціна, мана | діє постійно / за застосуванням / за ману з перезарядкою / шкодить / рідкісний |
| Броня (голова / тіло / ноги) | — | значення | «Fortify» за подій (?) |
| Мод етапу | zone | складність −4…4 | змінює правила поля на цей етап |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(open, c)` → ЯКЩО `not occupied(c, monster)` → ТО `reveal(c)` з числом `adjacent_count(c, monster, ==, n)`; `custom: «+мана за клітину»` (?).
- КОЛИ `input(open, c)` → ЯКЩО `occupied(c, monster)` → ТО `reveal(c)`, `custom: «помилка»`, `lives(-k)`, k у межах сили етапу (мін…макс), мінус захист (?).
- КОЛИ `hp_zero(hero)` → ЯКЩО `not has(hero, revive)` → ТО `lose`; інакше `custom: «відродження»` (Wishbone — шанс 25 %).
- КОЛИ `died(monster)` → ТО `custom: «дроп: ~60 % лут, 10 % кістки, 30 % предмет з таблиці монстра»`.
- КОЛИ `input(open, loot)` → ТО `pickup` → `currency(+n)` / `lives(+1)` / `give(item)`.
- КОЛИ `input(open, chest)` → ТО `give(item | coins)`.
- КОЛИ `input(use, item)` → ЯКЩО `has(hero, mana ≥ cost)` → ТО `custom: «ефект предмета на клітину або героя»`, `take(mana)`; магічні предмети — до перезарядки.
- КОЛИ `custom: «N клітин відкрито без помилки»` → ТО `custom: «нагорода серії»` (Badge of Honor кожні 15, квести — 100); помилка обнуляє серію.
- Ефекти «до наступної помилки» (Divine Coffee, First Aid, Horseshoe, Garlic): ЯКЩО `custom: «не було помилки»` → ТО ефект діє.
- КОЛИ `level_start` → ТО `custom: «застосувати моди етапу»`; приклади:
  - Nightmare: `input(flag)` → `block`.
  - Dry: нема випадкового луту, незнайомців, орієнтирів; після завершення — 3 скрині.
  - Withering: `timer(60s)` → `lives(-1)`, але не до смерті.
  - Lofty: КОЛИ `custom: «відкрито половину порожніх»` → ТО числа (крім 0) `+1`.
  - Haunted: КОЛИ `custom: «монстра відкрито»` → ТО `custom: «отримати омен»`; Ominous — омен на старті.
  - Trusty: етап розвʼязний без вгадувань; Hidden — 1 монстр; Horizontal / Vertical — удвічі ширше/вище і вдвічі більше монстрів.
  - Communist: відкрити інвентар — `currency(-5)`; Active — пасивні предмети вимкнено; Blinding — статистику й шкоду приховано.
- КОЛИ `input(buy, stranger)` → ЯКЩО `has(hero, coins ≥ price)` → ТО `currency(-price)`, `give(item)`; ціна Nomad росте з кожною покупкою.
- Gambler: за плату `reveal(random hidden)`; порожньо — переходить туди; монстр — гине, гравець бере його гроші.
- КОЛИ `custom: «етап розвʼязано»` → ТО `next_level`; КОЛИ 10-й етап квесту → ТО `win` (?).
- Перемога: пройти всі етапи квесту. · Поразка: життя вичерпано без відродження. · Рахунок: онлайн-лідерборди Hard+ і Hero Trial (?).
- Мета: перемога чи поразка — квест дає рівні, токени, майстерності, артефакти для наступних забігів.

## Керування і ввід
- Миша: ЛКМ — відкрити клітину / підібрати обʼєкт / взаємодіяти з незнайомцем; ПКМ — прапорець (?); «powerchord» — акорд-клік (відкрити сусідів числа) (?).
- Предмети: клік по іконці в інвентарі, далі — ціль-клітина для цільових (Stick, Bomb 3×3).
- Майстерність: пасив + заряджувана здібність (кнопка) (?).

## Вікна, меню, HUD
- `game-screen`: поле, життя, захист, мана (`mana-bar`), монети, `inventory-bar` предметів, `stage-mod-icons` під статистикою етапу, сила етапу (мін–макс шкода), кількість монстрів.
- `mode-select`: Квести (5) · Classic · Endless Multiverse · Hero Trial (daily) · Beyond · Autosweeper Division · Arena · Tutorial.
- `difficulty-select`: Casual · Normal · Hard · Beyond (?).
- `map-window` / мапа квесту: етапи, спецетапи, підетапи сезонних подій (?).
- `shop-window`: торгівля з незнайомцем (купити/продати/обмін).
- `codex-window`: Codex — знайдені предмети.
- `character-select` / профілі: таланти за токени, майстерність, аватар, вигляд інвентаря.
- `achievements-window` (100+), `leaderboard` (онлайн), `lobby-window` (Arena на 8) (?).
- `end-screen`: результат квесту + нагороди мета-прогресії.

## Фічі поза полем
- `meta-progression`: токени → таланти; 40 майстерностей; рівні; артефакти й heirlooms.
- `difficulty-presets`: Casual / Normal / Hard / Beyond; крафт креслень — у Hard.
- `mode-daily` Hero Trial; `mode-endless` Endless Multiverse; `mode-classic` — звичайний сапер.
- `auto-sweep` — Autosweeper Division: гра сама розміновує, гравець керує предметами й економікою.
- `online-multiplayer`: PvP Arena проти 7 гравців; онлайн-лідерборди кросплатформні.
- `profiles` — кілька профілів для різних білдів; `codex`; косметика (аватари, інвентарі, фарби).

## Варіації й родичі
- [minesweeper](minesweeper.md) (Classic-режим), [dragonsweeper](dragonsweeper.md) і Mamono Sweeper — монстри з HP-бюджетом замість мін; [14-minesweeper-variants](14-minesweeper-variants.md) — моди-правила на рівень; [kaboom](kaboom.md).
- Роглайк-сусіди: Desktop Dungeons, Slay the Spire (предмети-реліквії, мапа шляху) (?).
- Осі варіацій: **ціна помилки** смерть / втрата життя / лічильник · **модифікатори** нема / одне правило на рівень / стек модів зі складністю · **прогрес** нема / в забігу (предмети) / мета (таланти) · **хто розміновує** гравець / автомат (Autosweeper).

## Цікавинки для курсу
- Помилка = втрата життя в межах сили етапу, а не кінець — 🌱.
- Моди етапу як композиція правил (стек модифікаторів поверх сапера: Nightmare, Lofty, Withering, Horizontal) — 🥈.
- Ефекти «до наступної помилки» й серії «N без помилок» як підписка на подію — 📎.
- Інвентар предметів з типами (пасив / разовий / магія за ману / омен) — 🥉; 1000 предметів як дані + рушій ефектів — 🥇.
- Незнайомці-NPC на полі з власною логікою (Gambler відкриває випадкову клітину) — 📎 кожен.
- Autosweeper: солвер сапера як «гравець», а людина — лише економіка — 🥉.
- Мета-прогресія (токени, таланти, профілі) — 🥉.

## Мапа на каталог
- Є: `cell-click` · `neighbor-count-clue` · `chord-click` ↔ powerchord · `hp-damage` ↔ життя і шкода помилки · `inventory` + `inventory-items` + `inventory-limit` + `item-pickup` · `round-currency` ↔ монети · `shop-catalog` + `shop-buyback` ↔ Nomad купує й продає · `run-relics` ↔ пасивні предмети забігу · `status-effects` ↔ омени, burning · `difficulty-levels` · `daily-puzzle` ↔ Hero Trial · `sequential-levels` + `world-map` ↔ квест з 10 етапів · `no-guess-generation` ↔ мод Trusty · `mines-after-first-click` (?) · `codex-window` · `achievements-window` · `leaderboard` · `online-multiplayer` ↔ Arena · `mode-select` · `tutorial-window` · `save-progress` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+mistake-damage` «Помилка коштує життя (сила етапу), а не гру» · game-logic/lose · 🌱.
  - `+stage-mods` «Стек модифікаторів правил рівня зі складністю» · levels/generation · 🥈 · слоти {mods: list, difficulty: int}.
  - `+mistake-free-streak` «Серія дій без помилки з нагородою» · game-logic/score · 📎.
  - `+mana-charged-items` «Магічні предмети за ману з перезарядкою» · entities/state · 🥉.
  - `+armor-slots` «Броня за слотами тіла з ефектом на подію» · entities/state · 📎.
  - `+stranger-npcs` «Незнайомці на полі: торгівля й послуги» · game-logic/economy · 🥉.
  - `+omens` «Прокляття-предмети з негативним ефектом» · entities/state · 📎.
  - `+meta-talents` «Таланти за токени між забігами» · levels/progression · 🥉.
  - `+autosweeper-mode` «Режим, де солвер грає замість гравця» · game-logic/opponent · 🥉.

## Пропозиції до словників
- `+trigger:mistake` — гравець відкрив небезпечну клітину (подія для предметів, модів, серій).
- `+trigger:streak` — N дій поспіль без помилки; `+cond:no_mistake_since` — від моменту X помилок не було.
- `+effect:omen` — накласти прокляття-предмет; `+effect:fortify` — посилити захист броні за подією.
- `+ui:mana-bar` — мана для магічних предметів; `+ui:stage-mod-icons` — іконки модів поточного рівня.
- `+feature:auto-sweep` — гра сама відкриває безпечне; `+feature:profiles` — кілька профілів-білдів.

## Джерела
- ⭐ [Steam: DemonCrawl](https://store.steampowered.com/app/1141220/) — Therefore Games, 05.11.2019; 1000+ предметів, 60+ етапів, 100+ модів, 5 квестів, режими (Endless Multiverse, Hero Trial, Beyond, Autosweeper, Classic, Tutorial), Arena на 8, токени й таланти, 40 майстерностей, крафт у Hard, Codex, 100+ досягнень.
- [DemonCrawl Wiki](https://demoncrawl.com/wiki/) — структура: квести, складності, монстри, лут, моди, аури, боси, незнайомці, орієнтири, мета-системи.
- [Wiki: Mistake](https://demoncrawl.com/wiki/index.php/Mistake) — визначення помилки, ефекти «до наступної помилки», серії без помилок.
- [Wiki: Stage Mods](https://demoncrawl.com/wiki/index.php/Stage_Mods) — моди зі складністю, предмети, що знімають/перекидають моди, Evolving.
- [Wiki: Stages](https://demoncrawl.com/wiki/index.php/Stages) — 5 × 10 етапів, сила етапу = діапазон шкоди помилки, ≤ 95 % монстрів, 2025 клітин, секретні етапи 5 % у Hard.
- [Wiki: Objects](https://demoncrawl.com/wiki/index.php/Objects) — монети, діаманти, токени, скрині, серця, душі, темні серця, кістки.
- [Wiki: Items](https://demoncrawl.com/wiki/index.php/Items) — 949 предметів (83 Divine), типи, броня зі слотами, мана, приклади.
- [Wiki: Strangers](https://demoncrawl.com/wiki/index.php/Strangers) — Nomad, Blacksmith, Priest, Gambler, Hungry Plant, Mercenary…

## Непевне
- (?) Базова механіка шкоди: чи захист віднімається від шкоди, скільки життів на старті — сторінки не пояснюють.
- (?) Мана з відкритих клітин — лише непрямо (Divine Drugs «подвоює ману з клітин»).
- (?) Умова завершення етапу (відкрити всі безпечні? знайти вихід?) і чи є мапа між етапами — не знайшов.
- (?) ПКМ = прапорець і механіка powerchord — з памʼяті / з назв предметів.
- (?) Перший клік безпечний (`mines-after-first-click`) — з памʼяті.
- (?) Що роблять аури й орієнтири — сторінки не відкривав.
- Кількість предметів: Steam «1000+», вікі «949».
