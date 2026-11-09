---
title: Backpack Battles
slug: backpack-battles
aka: [BB, Backpack Battles PvP]
family: build-sim
also: [tower-lanes]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: online
  info: partial
  random: both
  goal: score
year: 2024
platforms: [Windows, Linux]
links:
  - {kind: fandom, url: "https://backpackbattles.wiki.gg/wiki/Game_Mechanics", best: true, note: "офіційна вікі: рюкзак, крамниця, рідкість за раундами, HP/золото за раундами, статуси, ★/♦-синергії, ранги"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Backpack_Battles", note: "структура раунду, рецепти, 10 перемог до 5 поразок, режими"}
  - {kind: steam, url: "https://store.steampowered.com/app/2427700", note: "500+ предметів, класи й підкласи, асинхронний PvP, custom rules"}
  - {kind: fandom, url: "https://backpackbattles.wiki.gg/wiki/Backpack_Battles_Wiki", note: "головна вікі: Items, Characters, Version History"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=backpack+battles+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [inventory, inventory-limit, multi-cell-size, orientation-state, drag-drop-piece, hover-highlight, hp-damage, status-effects, round-currency, shop-between-levels, shop-catalog, shop-sales, shop-buyback, in-round-upgrades, async-multiplayer, online-multiplayer, rating-system, rule-variants, character-select, lobby-window, match-setup, polyomino-placement, +shaped-items, +adjacency-buff, +bag-expansion, +recipe-combine, +shop-reroll, +shop-lock, +rarity-by-round, +item-cooldown, +stamina-cost, +fatigue-timer, +ghost-opponent, +storage-zone, +auto-battle]
proposes: ["+trigger:cooldown_ready", "+trigger:battle_end", "+cond:in_mark", "+effect:reroll", "+effect:combine", "+ui:synergy-marks", "+ui:storage-area", "+card:recipe-combine", "+card:ghost-opponent", "+feature:async-pvp"]
author: opus
date: 2026-11-09
---

# Backpack Battles — розкладаєш фігурні предмети в рюкзаку так, щоб сусіди підсилювали одне одного, а бій іде сам проти рюкзака іншого гравця

## Суть
Гібрид `cursor` (крамниця й розкладка) + автобій: гравець купує предмети різної форми, кладе й обертає їх у сітці рюкзака, розширює її сумками, а потім рюкзак бʼється сам проти збереженого рюкзака іншого гравця. Предмети спрацьовують за кулдауном і залежать від **сусідів** — позначки ★ і ♦ у підказці кажуть, яка сусідня клітина має містити якого роду предмет (сковорідка сильніша біля їжі, лялька швидша біля темних предметів). Після бою суміжні інгредієнти зливаються в сильніші предмети за рецептами.

## Поле і час
- Сітка інвентаря 63 клітини; клас стартує з 12–14 доступних, решту відкривають сумки (Leather Bag, Fanny Pack, Stamina Sack, Potion Belt, Protective Purse). Поза рюкзаком — **сховище**: предмети там неактивні.
- Предмети — поліоміно різних форм; обертаються.
- Раунд = фаза крамниці (без часу в unranked, з таймером у лобі) + фаза бою (real-time, зазвичай 10–20 с). До 18 раундів.
- Бій: два рюкзаки поруч, предмети тікають кулдаунами; з «ночі» обом іде наростаюча втома.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж (клас) | player | HP за раундом · витривалість · клас/підклас | бʼється автоматично; HP росте з раундом (25 → 350) |
| Клас (Berserker, Pyromancer, Reaper, Ranger…) | — | 2 стартові сумки | визначає пул предметів; підклас — з 8-го раунду |
| Сумка | container | форма, бонус | додає клітини рюкзака; деякі мають ефект на вміст |
| Предмет (500+) | object | форма · ціна · рідкість · тип/теги · кулдаун · витрата витривалості | у рюкзаку спрацьовує за кулдауном; у сховищі неактивний |
| Зброя (ближня / дистанційна) | object | шкода · точність · кулдаун | б'є суперника; крит — подвійна шкода |
| Їжа · темні предмети · зілля · магічні | object | тег | цілі ★/♦-синергій інших предметів |
| Позначка ★ / ♦ | zone | клітини відносно предмета | предмет потрібного тегу в позначці вмикає ефект; ♦ — для другого ефекту |
| Крамниця | supply | 5 слотів | пропонує предмети за рідкістю раунду |
| Суперник («привид») | enemy | збережений рюкзак іншого гравця | бʼється тим самим рушієм, без живого керування |
| Статуси-бафи: Empower · Heat · Luck · Mana · Regeneration · Spikes · Vampirism | — | стеки | +1 шкоди зброї / +2% швидкості / +5% точності / ресурс магії / +1 HP за 2 с / відбиття / вампіризм |
| Статуси-дебафи: Blind · Cold · Poison | — | стеки | −5% точності / −2% швидкості / −1 HP за 2 с |
| Блок (броня) | — | стеки | поглинає 1 шкоди за стек |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(round)` → ТО `currency(+gold_of_round)`, `custom: «макс. HP = таблиця раунду»` (старт 13 золота, 25 HP).
- КОЛИ `turn_start(round)` → ТО `custom: «5 предметів за таблицею рідкості раунду»` (R1 90/10/0/0/0 … R12–18 по 20%), `custom: «кожен з шансом 10% — знижка 50%»`.
- КОЛИ `input(buy, item)` → ЯКЩО `has(player, gold >= price)` → ТО `currency(-price)`, `give(player, item)` (у сховище).
- КОЛИ `input(sell, item)` → ТО `currency(+sell_price)`, `disappear_b`.
- КОЛИ `input(reroll)` → ЯКЩО `has(player, gold >= cost)` → ТО `currency(-cost)`, `custom: «нові 5 предметів, крім зарезервованих»`; ціна 1 за перші 4 рероли, далі 2.
- КОЛИ `input(lock, item)` → ТО `set_state(item, reserved)` — не зникає при реролі й на початку наступного раунду.
- КОЛИ `input(drag, item, cells)` → ЯКЩО `fits(item_shape, free_bag_cells)` → ТО `place(item)`; інакше `move(item, storage)`.
- КОЛИ `input(rotate, item)` → ТО `rotate(item, 90)`.
- КОЛИ `counter(round, ==, 8)` → ТО `choose(subclass)`.
- КОЛИ `timer(item_cooldown)` → ЯКЩО `cell(item, bag)` and `has(player, stamina >= item_cost)` → ТО `custom: «предмет спрацьовує»`, `counter(stamina, -item_cost)`.
- КОЛИ `timer(weapon_cooldown)` → ЯКЩО `prob(accuracy)` → ТО `damage(n)`.
- КОЛИ `timer(weapon_cooldown)` → ЯКЩО `prob(accuracy)` and `prob(crit)` → ТО `damage(2n)` (крит).
- КОЛИ `timer(item_cooldown)` → ЯКЩО `custom: «у клітині ★ лежить предмет потрібного тегу»` → ТО `custom: «ефект синергії предмета»`; один предмет зазвичай заповнює лише одну ★ і одну ♦ іншого.
- КОЛИ `timer(2s)` → ЯКЩО `state(a, poison)` → ТО `hp(a, -stacks)`.
- КОЛИ `timer(2s)` → ЯКЩО `state(a, regeneration)` → ТО `heal(a, stacks)`.
- КОЛИ `custom: «зміна стеків Heat/Cold»` → ТО `speed(items, ±2% × stacks)`.
- КОЛИ `contact(melee_hit, a)` → ЯКЩО `state(a, spikes)` → ТО `damage(stacks)` атакувальнику (до 100% шкоди).
- КОЛИ `contact(melee_hit, a)` → ЯКЩО `state(attacker, vampirism)` → ТО `heal(attacker, stacks)` (до 100% шкоди).
- КОЛИ `contact(hit, a)` → ЯКЩО `state(a, block)` → ТО `custom: «стек поглинає 1 шкоди»` (частина шкоди ігнорує броню).
- КОЛИ `custom: «настала ніч у бою»` → ТО `damage(both, rising)` (втома).
- КОЛИ `hp_zero(a)` → ТО `custom: «a програв бій»`, `counter(losses_of_a, +1)`, `counter(wins_of_b, +1)`.
- КОЛИ `custom: «бій скінчився»` → ЯКЩО `custom: «інгредієнти рецепта суміжні в рюкзаку»` → ТО `merge(a, b → c)` (Hero Sword + 2 Whetstone → Hero Longsword).
- КОЛИ `counter(wins, >=, 10)` → ТО `win`, `choose(stop | survival_mode)`; survival триває до 18-го раунду.
- КОЛИ `counter(losses, >=, 5)` → ТО `lose`.
- Рахунок: ранг персонажа (Bronze → … → Grandmaster → Grandma), очки рангу за результат забігу.

## Керування і ввід
- Миша: drag-n-drop предмета з крамниці/сховища в рюкзак, обертання під час перетягування (колесо/клавіша (?)), ПКМ по товару — резерв, кнопка реролу, перетягнути на крамницю — продати (?).
- Наведення — `tooltip` з характеристиками й підсвіткою клітин ★/♦ відносно предмета.
- Під час бою гравець не керує — лише дивиться (швидкість/пропуск бою (?)).

## Вікна, меню, HUD
- `main-menu`: Ranked · Unranked · Custom (`match-setup`: золото, макс. HP та ін.) · Lobby (`lobby-window`, синхронна гра з друзями) · Settings.
- `character-select`: клас + одна з двох стартових сумок, або випадково.
- `game-screen` (крамниця): рюкзак-сітка, сховище, 5 слотів крамниці, кнопка реролу, лічильники `coins`, `hp-bar`, раунд, перемоги/поразки (`progress-bar` трофеїв (?)).
- `custom-window` бою: два рюкзаки, `hp-bar` і `energy-bar` (витривалість), іконки статусів зі стеками, `popup-text` шкоди.
- `upgrade-window`: вибір підкласу на 8-му раунді.
- `end-screen` забігу: перемоги, зміна рангу; `leaderboard` рангів (?).
- Переходи: main-menu → character-select → (крамниця ↔ бій) × раунди → end-screen.

## Фічі поза полем
- `online-multiplayer` асинхронно: суперник — збережений рюкзак іншого гравця близького рангу; лобі — синхронно.
- `rank-tiers` (8 рангів, окремо для кожного персонажа); забіги з модифікаторами виключено з пулу суперників.
- `custom-rules` — свої правила (золото, HP); `mode-endless`-подібний survival після 10 перемог.
- Рідкість за раундами (Common → Godly) — `meta-progression` нема, кожен забіг з нуля.

## Варіації й родичі
- `backpack-hero` у корпусі — те саме ядро «форма + сусідство в рюкзаку», але PvE покроково з енергією на хід; Backpack Battles — PvP-автобій із кулдаунами.
- Автобатлери (Super Auto Pets, TFT) — крамниця-реролл + бій без керування; `luck-be-a-landlord` — сусідство символів дає ефект.
- Осі варіацій:
  - **синергія:** будь-який сусід / позначені клітини ★/♦ / за тегом;
  - **бій:** покроковий з вибором (Backpack Hero) / real-time автоматичний (BB);
  - **суперник:** AI / живий синхронно / «привид» збереженого білду;
  - **крафт:** вибором у меню / суміжністю після бою.

## Цікавинки для курсу
- Розкладка поліоміно в сітці рюкзака з обертанням і сховищем — 📎.
- Позначки ★/♦: ефект предмета залежить від тегу предмета в конкретних відносних клітинах — 🥉 (синергії як шаблони навколо форми, що обертаються разом із предметом).
- Рецепти суміжністю після бою (злиття A + B → C) — 📎.
- Автобій на кулдаунах + витривалість + стеки статусів (Heat/Cold як множник швидкості) — 🥈 (подієва симуляція з таймерами).
- Крамниця: 5 слотів, рерол 1→2 золота, резерв, 10% знижка, рідкість за раундом — 🥉.
- Асинхронний PvP проти «привидів»-білдів — 🥈 (серіалізація стану рюкзака й підбір за рангом).

## Мапа на каталог
- Є: `inventory` + `inventory-limit` + `multi-cell-size` + `polyomino-placement` + `orientation-state` (предмети-форми, обертання) · `drag-drop-piece` · `hover-highlight` · `hp-damage` · `status-effects` · `round-currency` · `shop-between-levels` + `shop-catalog` + `shop-sales` + `shop-buyback` · `in-round-upgrades` (підклас) · `async-multiplayer` + `online-multiplayer` · `rating-system` · `rule-variants` (custom rules) · `character-select` · `lobby-window` · `match-setup`.
- **Нема** → пропозиції карток:
  - `+shaped-items` · `+adjacency-buff` · `+bag-expansion` — як у `backpack-hero`.
  - `+recipe-combine` «Рецепт суміжністю» · entities/interact · 📎 · слоти {inputs, output, when: after_battle}.
  - `+shop-reroll` «Рерол вітрини» · game-logic/economy · 🌱 · слоти {cost, step}.
  - `+shop-lock` «Резерв товару» · game-logic/economy · 🌱.
  - `+rarity-by-round` «Таблиця рідкості за раундом» · game-logic/economy · 🌱.
  - `+item-cooldown` «Предмет спрацьовує за кулдауном» · entities/combat · 📎.
  - `+stamina-cost` «Витривалість на спрацювання» · entities/state · 🌱.
  - `+fatigue-timer` «Наростаюча шкода обом після межі часу» · game-logic · 🌱.
  - `+ghost-opponent` «Суперник — збережений білд іншого гравця» · players · 🥈.
  - `+storage-zone` «Сховище неактивних предметів» · entities/state · 🌱.
  - `+auto-battle` «Бій без керування» · game-logic · 🥉.

## Пропозиції до словників
- `+trigger:cooldown_ready` — предмет/вміння готове до спрацювання (зараз `timer(item_cooldown)`).
- `+trigger:battle_end` — кінець фази бою (рецепти, нагороди).
- `+cond:in_mark` — у позначеній відносній клітині ★/♦ є сутність з тегом.
- `+effect:reroll` — оновити вітрину/вибір за ціну; `+effect:combine` — злиття кількох суміжних за рецептом (≥2 інгредієнти, на відміну від `merge` пари однакових).
- `+ui:synergy-marks` — підсвітка ★/♦-клітин навколо предмета; `+ui:storage-area` — зона неактивних предметів поза полем.
- `+card:recipe-combine`, `+card:ghost-opponent` — див. вище.
- `+feature:async-pvp` — гра проти збережених знімків інших гравців.

## Джерела
- ⭐ [Backpack Battles Wiki: Game Mechanics](https://backpackbattles.wiki.gg/wiki/Game_Mechanics) — 63 клітини, сумки, крамниця (5 предметів, рерол 1/2, резерв, 10% знижки), таблиця рідкості й HP/золота за раундами, статуси зі стеками, ★/♦, ранги.
- [Wikipedia](https://en.wikipedia.org/wiki/Backpack_Battles) — до 18 раундів, бій 10–20 с, рецепти (Hero Longsword), 10 перемог до 5 поразок, survival, режими.
- [Steam](https://store.steampowered.com/app/2427700) — 500+ предметів, 7 класів × 5 підкласів, асинхронний PvP, custom rules, лобі.
- [Wiki: головна](https://backpackbattles.wiki.gg/wiki/Backpack_Battles_Wiki) — розділи Items, Characters.
- YouTube: пошук «backpack battles gameplay».

## Непевне
- (?) Кількість класів: Wikipedia називає 4, Steam — 7 класів × 5 підкласів (пізніші оновлення).
- (?) Числа витривалості, кулдаунів, точності за замовчуванням і темп наростання втоми — вікі їх не дає.
- (?) Як саме продається предмет (перетягнути на крамницю) і клавіша обертання; швидкість/пропуск бою; екрани рангів.
- (?) Підбір суперника — «напіввипадково з забігів інших гравців» (Wikipedia); чи того самого раунду — не перевірив.
