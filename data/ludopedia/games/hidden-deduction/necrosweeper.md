---
title: Necrosweeper
slug: necrosweeper
aka: []
family: hidden-deduction
also: [roguelike]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: both
  goal: survive
year: 2026
platforms: [web (itch.io, HTML5, Unity), Windows, macOS (Steam — coming soon), touch / iPad]
links:
  - {kind: itch, url: "https://studio-ahn.itch.io/necrosweeper", best: true, note: "грати в браузері; опис, фічі, відповіді розробника про числа, кольори, stamina, відмову від прапорців"}
  - {kind: steam, url: "https://store.steampowered.com/app/2839860/Necrosweeper/", note: "опис: плитки-обʼєкти, крамниця, еволюція копіями, зброя-карти руки, реліквії, зачарування, здібності монстрів"}
  - {kind: other, url: "https://studio-ahn.itch.io/necrosweeper/devlog/1610152/boss-attack-sequence-ui-effects-udpate", note: "девлог 31.07.2026: атака боса без ходів, Whetstone, Echo Crystal, Eternal Staff, Bandage, переповнена рука"}
  - {kind: other, url: "https://studio-ahn.itch.io/necrosweeper/devlog/1595480/few-bug-fixed", note: "девлог 20.07.2026: Augments, max HP, слоти руки, сувої, Legendary, лічильники руки й колоди"}
  - {kind: other, url: "https://itch.io/post/16576676", note: "тред: розробник про stamina, відмову від прапорців заради тачу, мету гри"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Necrosweeper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [cell-click, neighbor-count-clue, hp-damage, inventory-limit, run-relics, round-currency, shop-between-levels, shop-catalog, explode-area, sequential-levels, difficulty-levels, save-autosave, language-picker, settings-window, shop-window, game-screen, +deck-builder, +stamina-energy, +hand-limit, +star-up-merge, +recipe-combine, +boss-fight, +typed-count-color, +deck-seeded-field, +weapon-instead-of-flag, +item-augments]
proposes: ["+effect:attack", "+cond:hand_full", "+ui:stamina-bar", "+ui:hand-slots", "+ui:deck-counter", "+window:scroll-select", "+feature:ascension", "+card:typed-count-color", "+card:deck-seeded-field", "+card:weapon-instead-of-flag", "+card:item-augments"]
author: opus
date: 2026-11-09
---

# Necrosweeper — сапер-роглайк: число рахує всі обʼєкти поруч, колір натякає на їхній тип, а вміст поля — твоя власна колода плиток

## Суть
Поверхи підземелля некроманта — сітки закритих плиток, як у сапері: відкрита плитка показує число «скільки обʼєктних плиток (монстри, зброя, їжа…) поруч», а **колір числа** залежить від того, які обʼєкти знайдено поруч, і саме число від цього не змінюється. Прапорців нема: розробник прибрав їх заради тач-керування й замінив **зброєю** — знайдена зброя йде картою в руку, нею атакують підозрілі плитки й монстрів. Кожне відкриття коштує **stamina**, тож обережне повне розмінування карається. Між поверхами — крамниця: куплені плитки стають частиною **колоди**, з якої генеруються наступні підземелля; копії зливаються в сильніші форми, частина комбінацій — за прихованими рецептами. Гра в розробці (itch-білд, Steam — coming soon).

## Поле і час
- Квадратна сітка «відносно невелика» (відгук гравця); точний розмір — (?). Сусідство для чисел — (?), імовірно 8.
- Шари клітини: закрита / відкрита + вміст (порожньо з числом або обʼєктна плитка) + «тріщини»-позначки (гравці так назвали маркування) (?).
- Хід = одна дія гравця (відкрити плитку, застосувати карту); ворожі здібності спрацьовують подіями (?). Real-time нема.
- Вміст поля береться з **колоди гравця**: що більша колода, то більше плиток на поверсі й то дорожче за stamina його обшукати.
- 30 етапів, бос кожні 5 поверхів; кілька підземель зі своїми макетами, правилами й стартовими умовами; Endless після 30-го.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | серця (max HP), stamina, рука, колода, золото | діє курсором; не стоїть на полі |
| Закрита плитка | static | — | відкривається кліком/тапом за stamina |
| Число | mark | значення, колір | кількість обʼєктних плиток поруч; колір — від типів знайдених поруч обʼєктів; знайдений монстр може «зняти» колір |
| Монстр | enemy | здібність | ховається під плиткою; здібності: забирає stamina, псує плитки, знищує карти в руці |
| Бос | boss | патерн атак | кожні 5 поверхів; атакує, коли в гравця нема ходів |
| Плитка зброї | pickup | тип: меч, молот, кинджал, посох, паличка, бомба | при відкритті — карта в руку; рука повна → зброя зникає |
| Меч | pickup | — | сильний удар по одній цілі |
| Бомба | pickup | — | нищить групи ворогів і перешкод |
| Магічна паличка / посох | pickup | — | кілька атак |
| Eternal Staff | pickup | зброя | повторно активує обрану плитку (крім себе) |
| Їжа | pickup | — | відновлення (stamina чи HP — (?)) |
| Золото | resource | — | валюта крамниці |
| Пастка | hazard | — | шкодить при відкритті (?) |
| Перешкода | static | — | її кількість змінюють ефекти; бомба руйнує |
| Whetstone | pickup | — | при відкритті створює 2 магічні кулі, що шукають зброю й підсилюють її |
| Echo Crystal | pickup | — | при відкритті дублює одну карту в руці |
| Temple | pickup | — | (?) ефект не описано; баланс у роботі |
| Скриня зброї | container | — | містить зброю |
| Рука | supply | слоти | карти зброї; заповнюється по порядку слотів |
| Реліквія | pickup | — | пасивка забігу: Bag (зникає лише частина карт), Bandage (stamina 0 → −серце → stamina повна) |
| Сувій | pickup | — | застосовується до предмета (напр. Increase Spawn Count) |
| Augment / зачарування | mark | напр. Does Not Disappear | властивість предмета, додає здібність плитці |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(reveal, c)` → ТО `reveal(c)`, `counter(stamina, -вартість)`.
- КОЛИ `input(reveal, c)` → ЯКЩО `cell(c, empty)` → ТО `custom: «показати число = кількість обʼєктних плиток серед сусідів»`, `custom: «колір числа — за типами знайдених поруч обʼєктів; значення не змінюється»`.
- КОЛИ `input(reveal, c)` → ЯКЩО `cell(c, weapon)` and `custom: «рука повна»` → ТО `disappear` (зброя втрачена); інакше `give(player, weapon_card)`.
- КОЛИ `input(use, weapon, c)` → ЯКЩО `occupied(c, monster)` → ТО `damage(monster, n)`; меч — одна ціль; бомба — `explode(group)` ворогів і перешкод; паличка — `custom: «кілька атак»`.
- КОЛИ `input(reveal, c)` → ЯКЩО `cell(c, monster)` → ТО `custom: «монстр діє своєю здібністю»` — `counter(stamina, -n)` / `custom: «псує плитки»` / `take(player, hand_cards)` (?).
- КОЛИ `custom: «ефект знищення карт руки»` → ЯКЩО `has(player, bag)` → ТО `take(player, part_of_hand)`; інакше `take(player, hand_cards)`.
- КОЛИ `input(reveal, c)` → ЯКЩО `cell(c, echo_crystal)` → ТО `clone(hand_card)`.
- КОЛИ `input(reveal, c)` → ЯКЩО `cell(c, whetstone)` → ТО `spawn(magic_orb)` ×2, `custom: «кулі летять до зброї й підсилюють її»`.
- КОЛИ `input(use, eternal_staff, c)` → ЯКЩО `not cell(c, eternal_staff)` → ТО `custom: «плитка c спрацьовує ще раз»`.
- КОЛИ `counter(stamina, ==, 0)` → ТО `lives(-1)` (мінус серце); ЯКЩО `has(player, bandage)` → ТО `custom: «stamina відновлюється повністю»`.
- КОЛИ `hp_zero(player)` → ТО `game_over` (кінець забігу).
- КОЛИ `no_moves(player)` → ЯКЩО `custom: «етап боса»` → ТО `custom: «бос виконує атаку»`.
- КОЛИ `level_end` → ТО `window(shop-window)`.
- КОЛИ `input(buy, tile)` → ЯКЩО `custom: «вистачає золота»` → ТО `currency(-ціна)`, `custom: «плитка додається в колоду й зʼявлятиметься в наступних підземеллях»`.
- КОЛИ `custom: «у колоді кілька копій однієї плитки»` → ТО `merge(copies → evolved_tile)`.
- КОЛИ `custom: «зібрано пару плиток прихованого рецепта»` → ТО `custom: «нова плитка/зброя за рецептом»`.
- КОЛИ `input(remove, tile)` (крамниця) → ТО `custom: «плитка прибирається з колоди»`.
- КОЛИ `input(use, scroll, item)` → ТО `custom: «змінити властивість предмета (Augment, кількість появ)»`.
- Перемога: пройти 30 етапів (бос кожні 5), далі Endless. · Поразка: серця = 0 (найчастіше через stamina). · Рахунок: нема; прогрес — глибина й рівень Ascension.

## Керування і ввід
- Лише клік/тап: відкрити плитку; обрати карту зброї в руці → тапнути ціль. Прапорця правою кнопкою нема (прибрано: «попереміння лівої й правої кнопок втомлює», гра має йти на iPad).
- У крамниці предмети перетягуються drag-ом (перестановка); сувій — вибір предмета у вікні вибору.
- Клавіатурних привʼязок на сторінці не описано.

## Вікна, меню, HUD
- `main-menu` (?): Continue (забіг відновлюється, зокрема з крамниці), новий забіг.
- `mode-select` (?): вибір підземелля й рівня Ascension; Endless.
- `game-screen`: поле; HUD — серця (`hp-bar`), `stamina-bar`, `hand-slots` (карти зброї), лічильник зброї в руці й `deck-counter` (ховаються в крамниці).
- `shop-window`: товари з Augment-ами, рівень крамниці й кнопка Level Up, прибирання плиток, перестановка drag-ом.
- `custom-window` — вибір цілі для сувою (`scroll-select`); вікно опису предмета (`tooltip`).
- `settings-window`: мова EN / KO.
- Переходи: main-menu → game-screen → (кінець поверху) shop-window → game-screen наступного поверху → … → (серця 0) end-screen (?).

## Фічі поза полем
- Колода як мета-прогрес забігу: купівля, видалення, злиття копій, приховані рецепти; Legendary-предмети з окремим правилом появи.
- `continue` / `autosave`: збереження забігу з Augment-ами й max HP.
- Кілька підземель + рівні Ascension (`difficulty-presets`), `mode-endless`.
- `localization` (EN, KO), `touch-controls`; Steam: досягнення, Cloud.
- Ліміт руки й «що більша колода, то дорожче поле» — свідомий тиск проти роздування колоди.

## Варіації й родичі
- Родичі в корпусі: [demoncrawl](demoncrawl.md) (роглайк-сапер з предметами й HP), [dragonsweeper](dragonsweeper.md) (числа монстрів, бій замість мін), [tacticsweeper](tacticsweeper.md), [rock-paper-sweeper](rock-paper-sweeper.md), [minesweeper](minesweeper.md) як база.
- Натхнення за словами розробника — Balatro і Luck be a Landlord (колода/синергії як мета).
- Осі варіацій: **що рахує число** — лише міни / усі обʼєкти з кольором за типом (тут) / сума рівнів монстрів (Dragonsweeper); **позначка небезпеки** — прапорець / атака зброєю (тут); **бюджет дій** — без ліміту / stamina на кожне відкриття; **вміст поля** — випадковий / з колоди гравця.

## Цікавинки для курсу
- Число + колір: одна клітина несе дві підказки (скільки і яких типів) — 🥉 (рахунок по типах і правило, як колір реагує на знайдені обʼєкти).
- Поле, згенероване з колоди гравця (плитки з колоди розкладаються під закриті клітини) — 🥈.
- Stamina як бюджет відкриттів + серце за обнулення + реліквія Bandage — 📎.
- Рука з N слотами: переповнення знищує нову зброю — 📎.
- Злиття копій у сильнішу форму (star-up) + приховані рецепти пар — 🥉.
- Ефекти-ланцюги плиток (Whetstone → кулі шукають зброю, Eternal Staff повторює плитку) — 🥈 (черга подій).

## Мапа на каталог
- Є: `cell-click` ↔ відкриття; `neighbor-count-clue` ↔ число обʼєктів; `hp-damage` ↔ серця; `inventory-limit` ↔ рука; `run-relics` ↔ реліквії; `round-currency` ↔ золото; `shop-between-levels` + `shop-catalog` + `shop-window` ↔ крамниця; `explode-area` ↔ бомба; `sequential-levels` ↔ 30 етапів; `difficulty-levels` ↔ Ascension; `save-autosave` ↔ Continue; `language-picker` + `settings-window`; `game-screen`.
- Корпус уже пропонує: `+deck-builder`, `+stamina-energy`, `+hand-limit`, `+star-up-merge`, `+recipe-combine`, `+boss-fight`.
- **Нема** → пропозиції карток:
  - `+typed-count-color` «Число рахує всі обʼєкти, колір — їхні типи» · game-logic/constraints · 🥉 · слот {types: list}.
  - `+deck-seeded-field` «Вміст прихованого поля — з колоди гравця» · levels/generation · 🥈.
  - `+weapon-instead-of-flag` «Атака картою замість прапорця» · interface/input · 📎.
  - `+item-augments` «Модифікатори-властивості на предметах (Augment)» · entities/state · 📎.

## Пропозиції до словників
- `+effect:attack` — застосувати карту зброї до клітини/монстра (не `damage` гравцеві, а дія гравця з витратою карти).
- `+cond:hand_full` — рука заповнена (нова зброя зникає).
- `+ui:stamina-bar` · `+ui:hand-slots` · `+ui:deck-counter` — уже пропоновані корпусом; тут усі три є в HUD.
- `+window:scroll-select` — вибір предмета, до якого застосувати сувій.
- `+feature:ascension` — нумеровані рівні складності поверх пройденої гри (Slay the Spire-лінія).
- `+card:typed-count-color`, `+card:deck-seeded-field`, `+card:weapon-instead-of-flag`, `+card:item-augments` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch.io: Necrosweeper](https://studio-ahn.itch.io/necrosweeper) — опис, список фіч, 30 етапів і бос кожні 5, Ascension, Endless; відповіді розробника: число = обʼєктні плитки поруч, колір від знайдених обʼєктів, прапорці прибрано заради тачу.
- [Steam: Necrosweeper](https://store.steampowered.com/app/2839860/Necrosweeper/) — плитки під полем (зброя, їжа, золото, пастки, магія), крамниця, плитки переходять у наступні підземелля, еволюція копіями, карти зброї, реліквії й зачарування, здібності монстрів.
- [Девлог: Boss Attack Sequence…](https://studio-ahn.itch.io/necrosweeper/devlog/1610152/boss-attack-sequence-ui-effects-udpate) — бос атакує без ходів, Whetstone, Echo Crystal, Eternal Staff, Bandage, Bag, переповнена рука.
- [Девлог: Few(?) Bug Fixed](https://studio-ahn.itch.io/necrosweeper/devlog/1595480/few-bug-fixed) — Augments, max HP і лікування, слоти руки, сувої, Legendary, лічильники руки й колоди.
- [Тред Warjoy Heir](https://itch.io/post/16576676) — розробник про stamina і раптові смерті, відмову від прапорців, мету «зібрати колоду й синергії».

## Непевне
- (?) Точне правило кольору числа: «колір залежить від знайдених поруч обʼєктів, знайдений монстр може зняти колір» — чи колір кодує ще не знайдені типи, не пояснено; гравці скаржаться, що «числа брешуть» і на blue/yellow-перемикання.
- (?) Умова завершення поверху (знайти вихід? усіх монстрів?) не описана.
- (?) Скільки stamina коштує відкриття, розміри поля й руки, що дає їжа, що робить пастка й Temple — не знайдено.
- (?) Що стається при відкритті монстра без атаки — розробник лише згадує «випадковий контакт з монстром».
- (?) Скільки копій треба для злиття: гравець пише про «правило 3 предметів», розробник не підтверджує.
- (?) Рік: 2026 — за чергою й поточними девлогами; номер сторінки Steam (2839860) натякає, що анонс був раніше.
