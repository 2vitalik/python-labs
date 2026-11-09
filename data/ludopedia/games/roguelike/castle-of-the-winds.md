---
title: Castle of the Winds
slug: castle-of-the-winds
aka: [CotW, "Castle of the Winds: A Question of Vengeance", "Castle of the Winds: Lifthransir's Bane"]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 1989
platforms: [Windows 3.x]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Castle_of_the_Winds", best: true, note: "мишачий Windows-інтерфейс, вага + обʼєм, контейнери, 30 заклять за рівнями, міста й служби, рейтинг за часом, дві частини"}
  - {kind: other, url: "https://www.roguebasin.com/index.php/Castle_of_the_Winds", note: "RogueBasin: команди лише мишею, атрибути смугами, види контейнерів і пояс, кульові закляття 3×3, мана в мінус, 3 міста й 40 рівнів"}
  - {kind: other, url: "https://en.wikipedia.org/wiki/List_of_roguelikes", note: "WP-список: 1989"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Castle+of+the+Winds+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-by-input, move-8dir, cell-click, gui-render, dungeon-generation, stairs-levels, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, item-identification, status-effects, unit-xp-skills, explode-area, round-currency, shop-catalog, shop-buyback, save-game, player-death, leaderboard, fog-of-war, message-log, status-panel, keyboard-controls, map-window, +drag-drop-inventory, +weight-and-bulk, +nested-containers, +belt-slots, +spell-per-level, +negative-mana, +town-level, +hand-crafted-levels, +word-of-recall, +rotating-stock, +time-scaled-boss, +character-import]
proposes: ["+trigger:drop_on_slot", "+effect:move_item(from, to)", "+effect:learn_spell", "+cond:fits(container, item)", "+cond:on_belt(item)", "+cond:mana(op, n)", "+window:paperdoll", "+window:spellbook-window", "+window:sage-window", "+ui:attribute-bars", "+ui:weight-bulk-meter", "+ui:map-scale-toggle", "+feature:save-anywhere", "+feature:character-import", "+card:drag-drop-inventory", "+card:weight-and-bulk", "+card:belt-slots"]
author: opus
date: 2026-11-09
---

# Castle of the Winds — роглайк у вікнах Windows 3.x: інвентар перетягуванням мишею, вага й обʼєм замість слотів, закляття замість стрільби

## Суть
Від класичних роглайків ([rogue](rogue.md), [nethack](nethack.md)) CotW відрізняє **GUI**: гра на іконках Windows 3.1, багато команд доступні **лише мишею**, атрибути — смугами, а не числами. Інвентар — фізичний: межа задана **вагою (г) і обʼємом (см³)**, предмети лежать у вкладених контейнерах (рюкзаки, мішки, скрині, пояс з фіксованими слотами), і зілля/сувої/жезли працюють лише з поясу або з руки. Класів нема: одне закляття за кожен рівень досвіду (максимум 30), луків нема — дальній бій лише магією. Дві частини, сюжет за скандинавськими мітами.

## Поле і час
- Квадратна сітка з іконками 32×32 (?); 8 напрямків (?); повна мапа масштабується, щоб рівень вліз на один екран; спрощений вигляд — для повільних ПК.
- Три міста, біля кожного — підземелля; разом 40 рівнів: покинута шахта (4, без босів), фортеця Bjarnhaven (11, бос Hrungnir), підземелля частини II (25).
- Рівні — суміш випадкових і заготовлених; Rune of Return веде на найглибший відвіданий рівень (відвідані, ймовірно, зберігаються (?)).
- Покроково; гра рахує **ігровий час**: від нього залежать асортимент крамниць і сила фінального боса; рейтинг переможців — за часом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | STR (шкода, макс. вага), DEX (влучання, блок, пастки), INT (макс. мана), CON (макс. HP), рівень ≤30, мана | рух/атака мишею або клавішами; зброя бʼє лише сусідню клітину |
| Монстр | enemy | HP, атаки | переслідує; приспаний — спить ≈10 хв або доки не вдарять |
| Hrungnir | boss | — | вбивство завершує частину I |
| Фінальний бос | boss | сила від ігрового часу | — |
| Рюкзак / мішок (S, M, L) | container | макс. вага, макс. обʼєм | вміщує предмети за вагою й обʼємом |
| Скриня | container | — | займає свій **максимальний** обʼєм незалежно від заповнення |
| Pack of Holding (S, M, L) | container | зачарований | паки відштовхуються — не вкладаються один в одного |
| Пояс | container | фіксовані слоти | лише звідси (або з руки) діють зілля, сувої, книги, жезли |
| Гаманець | container | — | монети (мідь, срібло, золото…) мають вагу (?) |
| Зброя, броня, одяг, прикраси | pickup | normal / cursed / enchanted; зламана або іржава при знахідці | не ламаються від використання |
| Жезл / посох | pickup | заряди | обмежені заряди |
| Зілля / сувій / книга заклять | pickup | вид | ефекти; книга вчить закляття |
| Сувої Map Quadrant / Map Level | pickup | — | відкривають частину / весь рівень |
| Храм Одіна | static | — | лікування, відновлення атрибутів, Remove Curse, Rune of Return |
| Junk store (Olaf) | static | — | купує все, але не більше 25 CP за предмет |
| Мудрець (sage) | static | ціна | ідентифікує за плату |
| Банк (з 2-го міста) | static | — | зберігає монети — менше ваги |
| Крамниці (зброяр, бронник, магічна, загальна, outfitter) | static | асортимент | асортимент змінюється з часом |
| Сходи | static | — | перехід між рівнями |
| Пастка | hazard | — | шкода; DEX допомагає уникнути |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag item → container)` → ЯКЩО `custom: «вага й обʼєм влазять»` → ТО `custom: «предмет у контейнер»`; інакше `block` (?).
- КОЛИ `input(drag item → equipment slot)` → ЯКЩО `custom: «тип предмета підходить слоту»` → ТО `custom: «вдягнути»`; ЯКЩО `custom: «прокляте»` → ТО `custom: «не зняти без Remove Curse»` (?).
- КОЛИ `input(drag Pack of Holding → Pack of Holding)` → ТО `block`.
- КОЛИ `custom: «рахується обʼєм скрині»` → ТО `custom: «завжди максимальний, хоч і порожня»`.
- КОЛИ `input(use potion|scroll|wand)` → ЯКЩО `custom: «предмет на поясі, у руці або вдягнутий замість»` → ТО `custom: «ефект»`; інакше `block`.
- КОЛИ `custom: «сумарна вага > межа від STR»` → ТО `custom: «перевантаження: повільніше»` (?); обʼєм обмежено 1000000 см³.
- КОЛИ `input(click adjacent monster)` → ТО `custom: «атака впритул»`; дальній бій — лише закляттям.
- КОЛИ `custom: «рівень героя +1»` → ТО `choose(spell)` з доступних; КОЛИ `input(read spellbook)` → ТО `custom: «вивчити закляття»`; ЯКЩО `custom: «закляття вже знане»` → ТО `custom: «книга розпізнається автоматично»`.
- КОЛИ `input(cast ball spell, cell)` → ТО `damage(full)` у центрі, `damage(½)` на 8 сусідніх.
- КОЛИ `input(cast)` → ЯКЩО `custom: «мана < ціни»` → ТО `custom: «мана в мінус; ризик падіння CON»`.
- КОЛИ `custom: «CON нижче бази на поріг»` → ТО `lose`.
- КОЛИ `input(cast Clairvoyance)` → ТО `reveal(10×10)`; `Detect Traps` → `reveal(traps, r 10)`; `Light` → `reveal(room | 3×3)`.
- КОЛИ `input(read Rune of Return)` → ТО `custom: «з підземелля — у місто; з міста — на найглибший відвіданий рівень»`.
- КОЛИ `input(sell, junk store)` → ТО `currency(+min(value, 25 CP))`.
- КОЛИ `input(identify, sage)` → ТО `currency(−price)`, `custom: «відкрити зачарування, прокляття, заряди»`.
- КОЛИ `input(deposit, bank)` → ТО `custom: «монети з гаманця на рахунок — вага падає»`.
- КОЛИ `timer(every)` (ігровий час) → ТО `custom: «оновити асортимент крамниць»`.
- КОЛИ `died(Hrungnir)` → ТО `custom: «кінець частини I»`; частина II може імпортувати героя.
- КОЛИ `died(final boss)` → ТО `win`; `custom: «запис у Valhalla's Champions за часом»`.
- КОЛИ `hp_zero(hero)` → ТО `custom: «запис "Dead" з досвідом»`, `custom: «можна відновити збереження»`.
- Перемога: вбити фінального боса частини II. Поразка: смерть (але сейв відновлюється). Рахунок: переможці — за часом, мертві — за досвідом.

## Керування і ввід
- Миша — основний ввід: клік по клітині (рух, атака), перетягування предметів між полем, контейнерами й слотами тіла (?); частину команд клавіатурою не ввести взагалі.
- Клавіатурні скорочення: `g` — підняти; стрілки / цифри для руху (?).
- Меню Windows (File, Spells, Character…) і діалоги (?).

## Вікна, меню, HUD
- `game-screen`: вікно Windows з меню, мапою з іконок, смугами атрибутів (`attribute-bars`), рядком повідомлень.
- `inventory-window`: паперова лялька з слотами тіла + відкриті контейнери поряд, перетягування між ними (?); `weight-bulk-meter` (?).
- `spellbook-window` — список вивчених заклять, вибір закляття на рівні (?).
- `map-window`: повна мапа рівня, масштабована на один екран; перемикач на спрощену (`map-scale-toggle`).
- Вікна міст (`shop-window`, `sage-window`, храм, банк).
- `save-slots`: збереження будь-коли; `leaderboard` — Valhalla's Champions.
- `character-create`: імʼя, стать, розподіл атрибутів (?); імпорт героя з частини I.

## Фічі поза полем
- `save-anywhere`: збереження в будь-який момент і відновлення після смерті — свідомо без permadeath.
- Дві частини: I — shareware, II — комерційна; `character-import` героя-переможця.
- Рейтинг переможців за ігровим часом (мотив грати швидко без жорсткого дедлайну).
- Монохромна версія; 16 кольорів Windows + прозорість.
- З 1998 — безкоштовна (public domain).

## Варіації й родичі
- Механіки — «NetHack з GUI»: прокляття й зачарування як у [nethack](nethack.md); міста з храмом/мудрецем — як у [angband](angband.md), [larn](larn.md).
- Інвентар-контейнери — предок Diablo / [dungeon-master](dungeon-master.md) (ручне розміщення) (?); Rune of Return ↔ Word of Recall [angband](angband.md).
- Осі варіацій: **ліміт інвентаря** (кількість слотів / вага / вага + обʼєм + вкладені контейнери / сітка Diablo) · **ввід** (клавіатура / миша-клік / drag-and-drop) · **смерть** (permadeath / відновлення сейва) · **рейтинг** (очки / глибина / час).

## Цікавинки для курсу
- Drag-and-drop інвентар з вкладеними контейнерами — 🥈 (дерево контейнерів + перевірки + GUI).
- Подвійна межа: вага (від STR) і обʼєм, скриня займає максимум — 📎.
- Пояс як єдине місце, звідки працюють витратні предмети — 🌱.
- Pack of Holding, що не вкладається в інший, — 🌱 (заборона циклу в дереві).
- Кульове закляття: центр 100 %, сусіди 50 % — 🌱.
- Мана в мінус з ризиком втратити CON — 🌱.
- Асортимент і фінальний бос від ігрового часу + рейтинг за часом — 📎.

## Мапа на каталог
- Є: `cell-click` · `gui-render` · `move-8dir` · `stairs-levels` · `dungeon-generation` · `inventory` + `inventory-items` + `inventory-limit` · `item-identification` · `status-effects` (сон) · `unit-xp-skills` (закляття за рівнем) · `explode-area` (куля 3×3) · `shop-catalog` + `shop-buyback` · `save-game` · `leaderboard` · `map-window`.
- **Нема** → пропозиції карток:
  - `+drag-drop-inventory` «Перетягнути предмет між полем, контейнерами й слотами тіла» · interface/input · 🥈.
  - `+weight-and-bulk` «Ліміт інвентаря двома величинами: вага й обʼєм» · entities/inventory · 📎 · слоти {max_weight, max_bulk}.
  - `+nested-containers` «Контейнери в контейнерах із власними лімітами й забороною циклів» · entities/inventory · 🥉.
  - `+belt-slots` «Швидкі слоти, з яких лише й можна використати витратне» · entities/inventory · 🌱.
  - `+spell-per-level` «Одне нове закляття за рівень, без класів» · entities/state · 🌱.
  - `+negative-mana` «Каст у борг з ризиком для стату» · entities/state · 🌱.
  - `+hand-crafted-levels` «Заготовлені рівні серед процедурних» · levels/generation · 📎.
  - `+rotating-stock` «Асортимент крамниці змінюється з часом» · game-logic/economy · 🌱.
  - `+time-scaled-boss` «Сила фінального боса від витраченого часу» · game-logic/difficulty · 🌱.
  - `+character-import` «Перенос героя в наступну частину» · game-logic/save · 🌱. Перевикористано: `+town-level`, `+word-of-recall`.

## Пропозиції до словників
- `+trigger:drop_on_slot` — гравець відпустив перетягнутий предмет над слотом/контейнером.
- `+effect:move_item(from, to)` — перемістити предмет між контейнерами; `+effect:learn_spell`.
- `+cond:fits(container, item)` — предмет влазить за вагою й обʼємом (у словнику `fits` лише для форми фігури на полі); `+cond:on_belt(item)`; `+cond:mana(op, n)`.
- `+window:paperdoll`, `+window:spellbook-window`, `+window:sage-window`.
- `+ui:attribute-bars`, `+ui:weight-bulk-meter`, `+ui:map-scale-toggle`.
- `+feature:save-anywhere`, `+feature:character-import`.
- `+card:drag-drop-inventory`, `+card:weight-and-bulk`, `+card:belt-slots`.

## Джерела
- ⭐ [Wikipedia: Castle of the Winds](https://en.wikipedia.org/wiki/Castle_of_the_Winds) — мишачий інтерфейс, вага й обʼєм, контейнери, 30 заклять і 6 категорій, міста й служби, ігровий час і рейтинг, дві частини, графіка й мапа.
- [RogueBasin: Castle of the Winds](https://www.roguebasin.com/index.php/Castle_of_the_Winds) — команди лише мишею, смуги атрибутів, види контейнерів, пояс, Packs of Holding, обʼєм 1000000 см³, кульові закляття, мана в мінус, 3 міста й 40 рівнів, Junk store ≤25 CP, сейв будь-коли.
- [WP: List of roguelikes](https://en.wikipedia.org/wiki/List_of_roguelikes) — рік.

## Непевне
- (?) Сам **drag-and-drop** (перетягування між лялькою й контейнерами) — у прочитаних джерелах прямо не описано; є лише «команди лише мишею»; з памʼяті.
- (?) Наслідок перевантаження, вага монет, вигляд вікна інвентаря — не перевірено.
- (?) Чи зберігаються відвідані рівні (лише непрямо через Rune of Return) — не перевірено.
- (?) Рух у 8 напрямків, розмір іконок, меню Windows і створення героя — з памʼяті.
- (?) Рік: v1.0 1989 (RogueBasin), Wikipedia подає й 1993 (дистрибуція Epic MegaGames).
- (?) Wikipedia — 6 категорій заклять, RogueBasin — 7 (+ «лише з предметів»).
