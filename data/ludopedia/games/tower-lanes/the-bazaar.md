---
title: The Bazaar
slug: the-bazaar
aka: []
family: tower-lanes
also: []
klass: cursor
axes:
  field: 1d
  time: realtime
  opponent: online
  info: partial
  random: runtime
  goal: collect
year: 2025
platforms: [Windows, macOS]
links:
  - {kind: other, url: "https://loadlastsave.substack.com/p/the-bazaar-review", best: true, note: "огляд із механікою: дні по 6 годин, 10 слотів, розміри 1/2/3, сусідство, leftmost, кулдауни, NPC на 3-й годині, привиди PvP"}
  - {kind: steam, url: "https://store.steampowered.com/app/1617400/The_Bazaar/", note: "Steam: реліз 13.08.2025, Tempo; теги Auto Battler, Asynchronous Multiplayer"}
  - {kind: other, url: "https://game8.co/articles/reviews/the-bazaar-gameplay-and-story-info", note: "Rug 4→10 слотів, сховок, тири, дублікати, Slow/Haste/Freeze/Charge/Multicast, Burn/Poison/Shield/Regen, золото й дохід, досвід"}
  - {kind: other, url: "https://rkblog.pages.dev/posts/games/the-bazaar-card-game", note: "структура дня (2 + PvE + 2 + PvP), кінець забігу, привиди того ж дня, набої, знищення предмета"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tempo_Storm", note: "історія The Bazaar: анонс 2018, бета 2024, Season One 2025, Steam 2025, асинхронний мультиплеєр"}
  - {kind: other, url: "https://mobalytics.gg/the-bazaar/guides/keywords-and-terms", note: "глосарій ключових слів (агентам 403)"}
  - {kind: official, url: "https://www.playthebazaar.com/", note: "офіційний сайт (JS-застосунок)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Bazaar+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [round-currency, shop-catalog, shop-buyback, shop-window, inventory-limit, multi-cell-size, drag-drop-piece, hp-damage, status-effects, chain-reaction, tile-merge, in-round-upgrades, run-relics, async-multiplayer, online-multiplayer, rating-system, character-select, mode-select, end-screen, +auto-battle, +adjacency-buff, +cooldown-ability, +cooldown-manipulation, +multicast, +ammo-limit, +positional-targeting, +card-keywords, +item-enchant, +shop-reroll, +choose-upgrade, +encounter-choice, +stash-storage, +lives-and-trophies, +ghost-opponent]
proposes: ["+effect:charge", "+effect:shield", "+effect:upgrade", "+effect:sell", "+effect:reroll", "+trigger:fight_start", "+trigger:fight_end", "+cond:position", "+ui:cooldown-overlay", "+ui:prestige-counter", "+ui:day-hour-track", "+window:choice-window", "+card:cooldown-manipulation", "+card:positional-targeting", "+axis:time"]
author: opus
date: 2026-11-09
---

# The Bazaar — автобатлер на лінійці з 10 слотів: предмети з кулдаунами, розмір 1–3 і сусідство

## Суть
Роглайт-автобатлер від Tempo: обираєш героя, і за «дні» по шість «годин» купуєш у торговців предмети, проходиш події й бʼєшся з монстрами, а наприкінці дня — з привидом іншого гравця. Предмети лежать **в один ряд** на дошці до 10 слотів, займають 1, 2 або 3 слоти, і в бою самі спрацьовують, коли заповнюється їхній кулдаун. Глибина — у порядку на лінійці: сусідні бафи, «найлівіший/найправіший», прискорення й заморожування чужих кулдаунів. Мета забігу — 10 перемог у PvP, доки не скінчився престиж.

## Поле і час
- Дошка (у game8 — «Rug») — **1D-ряд слотів**, максимум 10; предмет займає суцільний відрізок з 1/2/3 слотів. Сусіди — лише ліворуч і праворуч; частина ефектів адресує «найлівіший» або «праворуч від себе».
- Сховок (stash) — окремий ряд для неактивних предметів: їхні кулдауни в бою не біжать, деякі пасивки діють.
- Два масштаби часу: **забіг** — дискретні кроки (день → 6 годин; година = один вибір), **бій** — неперервний час у секундах, кулдауни заповнюються паралельно на обох дошках, гравець не втручається.
- Таймерів на підготовку нема: забіг можна покинути й продовжити пізніше (асинхронний PvP).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | Health, Max Health, Shield, Regen, рівень, досвід | приймає всю шкоду напряму (істот-захисників нема); визначає пул предметів |
| Дошка (Rug) | zone | до 10 слотів | лише предмети на дошці діють у бою; порядок важливий |
| Сховок (Stash) | zone | слоти | зберігання; кулдауни стоять, частина пасивок працює |
| Предмет малий / середній / великий | object | розмір 1/2/3, тир, кулдаун, теги (Weapon, Aquatic, Vehicle, Property…) | активний — спрацьовує щоразу, як заповнився кулдаун; пасивний — постійний баф |
| Предмет з набоями | object | ammo | спрацьовує, доки є набої; інші предмети перезаряджають |
| Тир | — | Bronze → Silver → Gold → Diamond | дублікат піднімає тир на 1; ранні дні дають лише Bronze |
| Зачарування (enchantment) | — | Fiery, Toxic…, freeze — найрідкісніше | дописує предмету ефект (вогонь, отрута, multicast) |
| Навичка (Skill) | — | тир Bronze–Diamond | пасивний баф героя чи предметів певного типу, поза дошкою |
| Торговець | neutral | спеціалізація (середні, водні…) | продає предмети (не свого героя); один реролл за плату |
| Подія | neutral | — | дає золото, бонус або предмет |
| Монстр | enemy | своя дошка предметів | PvE-бій на 3-й годині; перемога — золото, досвід, випадковий предмет з його дошки |
| Привид гравця | enemy | збережена дошка того ж дня | PvP-бій у кінці дня |
| Золото | resource | Income | нараховується на початку дня за доходом; продаж — половина ціни |
| Престиж | resource | — | втрачається за поразки в PvP; 0 — кінець забігу |
| Перемоги | resource | 0–10 | +1 за PvP-перемогу; 10 — максимальний результат |
| Burn / Poison | hazard | стеки | шкода з часом: Burn згасає, Poison — ні |
| Shield | resource | значення | понад HP; поглинає шкоду першим |
| Haste / Slow / Freeze / Charge | — | тривалість у с | кулдаун біжить швидше / повільніше / стоїть / миттєво доповнюється |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(day)` → ТО `currency(+income)`.
- КОЛИ `custom: «завершено подію години»` → ТО `counter(xp, +1)`.
- КОЛИ `phase_start(hour)` → ЯКЩО `custom: «година не бойова»` → ТО `choose(3: merchant | event)`.
- КОЛИ `phase_start(hour)` → ЯКЩО `custom: «3-тя година дня»` → ТО `custom: «бій з монстром (PvE)»`.
- КОЛИ `phase_start(hour)` → ЯКЩО `custom: «кінець дня»` → ТО `custom: «бій з привидом гравця того самого дня (PvP)»`.
- КОЛИ `input(buy, item)` → ЯКЩО `counter(gold, >=, price)` and `fits(item, slots)` → ТО `currency(-price)`, `place(hero, item)`; інакше `block`.
- КОЛИ `input(buy, item)` → ЯКЩО `same(item, owned, name)` → ТО `merge(owned, item → tier+1)`.
- КОЛИ `input(sell, item)` → ТО `currency(+price/2)`, `disappear(item)`.
- КОЛИ `input(drag, item, slot)` → ЯКЩО `fits(item, slot)` → ТО `move(item, slot)`; інакше `block`.
- КОЛИ `input(reroll)` → ЯКЩО `first_time` → ТО `currency(-fee)`, `custom: «нова вітрина торговця»`.
- КОЛИ `counter(xp, >=, need)` → ТО `counter(level, +1)`, `choose(level_up_bonus)`, `custom: «дошка й сховок розширюються»`.
- КОЛИ `timer(cooldown)` → ЯКЩО `custom: «предмет на дошці»` and `not state(item, frozen)` → ТО `custom: «активація: ефект предмета»` (шкода, лікування, щит, отрута…).
- КОЛИ `timer(cooldown)` → ЯКЩО `counter(ammo, ==, 0)` → ТО `block`.
- КОЛИ `custom: «активація з Multicast k»` → ТО `custom: «ефект k разів за одну активацію»`.
- КОЛИ `custom: «активація»` → ЯКЩО `prob(crit)` → ТО `custom: «ефект ×2»`.
- КОЛИ `custom: «активація предмета з Haste»` → ТО `speed(target_item, +, t)`; Slow — `speed(target_item, -, t)`; Freeze — `freeze(target_item, t)`; Charge — `custom: «кулдаун цілі +t секунд одразу»`.
- КОЛИ `custom: «Slow або Freeze по чужій дошці»` → ТО `custom: «ціль обирається випадково»`.
- КОЛИ `custom: «активація з Damage»` → ЯКЩО `counter(shield, >, 0)` → ТО `custom: «шкода спершу знімає Shield»`; інакше `damage(enemy_hero, n)`.
- КОЛИ `tick` → ЯКЩО `state(hero, burn)` → ТО `damage(hero, burn)`, `custom: «Burn зменшується»`.
- КОЛИ `tick` → ЯКЩО `state(hero, poison)` → ТО `damage(hero, poison)`.
- КОЛИ `tick` → ЯКЩО `counter(regen, >, 0)` → ТО `heal(hero, regen)`.
- КОЛИ `custom: «ефект Destroy»` → ТО `disappear(target_item)` до кінця бою.
- КОЛИ `custom: «пасивка: сусід зліва/справа або предмет із тегом»` → ТО `custom: «баф сусіда (шкода, кулдаун, крит)»`.
- КОЛИ `input(sell, loot)` → ТО `custom: «назавжди баф найлівішому відповідному предмету»`.
- КОЛИ `custom: «предмет перетворюється»` → ТО `transform(item, same_total_size)`.
- КОЛИ `hp_zero(hero)` → ТО `custom: «бій програно»`.
- КОЛИ `custom: «PvP програно»` → ТО `counter(prestige, -n)`.
- КОЛИ `custom: «PvE виграно»` → ТО `currency(+gold)`, `counter(xp, +n)`, `give(hero, random_item_of_monster)`.
- КОЛИ `custom: «PvP виграно»` → ТО `counter(wins, +1)`.
- КОЛИ `counter(wins, ==, 10)` → ТО `win`.
- КОЛИ `counter(prestige, <=, 0)` → ТО `lose`.
- Перемога: 10 PvP-перемог · Поразка: престиж = 0 (або вичерпано дні забігу) · Рахунок: кількість перемог забігу → нагороди; у Ranked — рейтинг.

## Керування і ввід
- Миша/тач: клік по одній із карт години (торговець/подія), клік-купівля, drag предмета між слотами дошки, дошкою й сховком, продаж — перетягнути до торговця або кнопкою.
- Кнопка рероллу вітрини; вибір бонусу за рівень; кнопка старту бою не потрібна — бій запускається годиною.
- Бій — лише перегляд: жодного вводу, поки кулдауни відпрацьовують.

## Вікна, меню, HUD
- `main-menu`: Play → `mode-select` (Normal, Ranked за квиток, турнірна черга на 8 гравців); колекція/косметика; налаштування.
- `character-select` — герой (Vanessa, Pygmalien, Dooley, Mak, Stelle, Jules, Karnok, The Dragons) і стартовий предмет/бонус.
- `game-screen` забігу: дошка з 10 слотів і сховок, портрет героя з `hp-bar` і щитом, `coins` + дохід, `level-number` + досвід, `+ui:prestige-counter` (перемикається в налаштуваннях), лічильник перемог, `+ui:day-hour-track`.
- `+window:choice-window` — три карти години (торговці/події); `shop-window` торговця з `tooltip` предметів і кнопкою рероллу.
- `game-screen` бою: дві дошки-ряди одна навпроти одної, `+ui:cooldown-overlay` (заповнення кулдауну на кожному предметі), `popup-text` шкоди/лікування/щита, статуси на героях.
- `upgrade-window` — вибір бонусу за рівень; `end-screen` — підсумок забігу (кількість перемог, нагорода).
- `settings-window` — зокрема індикатор престижу.

## Фічі поза полем
- `online-multiplayer` асинхронно: сервер зберігає дошку кожного гравця на кожен день; ти бʼєшся з копією того самого дня.
- Ranked: квитки, рейтинг (Legendary), нагороди-скрині за кількість перемог; Normal без ставок; турніри на 8 гравців.
- `meta-progression` через колекцію (Prize Pass, сезони), DLC-герої; `pause` у сенсі «вийти й продовжити забіг».
- Експедиції — особливі події в певні дні (напр., Crash Site — 6-й день, потрібен квиток).

## Варіації й родичі
- Родичі в сімʼї: [super-auto-pets](super-auto-pets.md) (ряд 5 слотів, бій передніх, асинхронні привиди), [hearthstone-battlegrounds](hearthstone-battlegrounds.md) (ряд юнітів і тригери), [teamfight-tactics](teamfight-tactics.md) і [dota-auto-chess](dota-auto-chess.md) (2D-дошка, злиття копій), [mechabellum](mechabellum.md) (той самий видавець, поле 2D). Поза корпусом — Backpack Battles (2D-рюкзак із кулдаунами; межа з `build-sim`).
- **Осі варіацій** автобатлерів: поле — ряд слотів (Bazaar, SAP) / 2D-дошка (TFT) / рюкзак-поліоміно (Backpack Battles) · бій — черга передніх (SAP) / кулдауни всіх предметів одночасно (Bazaar) · хто отримує шкоду — юніт попереду / герой напряму · апгрейд — дублікат +1 тир / 3 копії → зірка.

## Цікавинки для курсу
- Рядок слотів із предметами розміру 1–3: вставка, перевірка «влізе», переставляння без накладань — 📎.
- Бій як симуляція кулдаунів у неперервному часі (подієва черга «хто спрацює наступним») — 🥈.
- Модифікатори кулдауну Haste/Slow/Freeze/Charge з тривалістю і випадковою ціллю — 🥉.
- Позиційні адресати: сусід, «праворуч від себе», найлівіший предмет — 📎 за набір.
- Асинхронний PvP: зберегти білд на день N і віддати іншому гравцеві на тому ж дні — 🥈.
- Структура дня «вибір 1 з 3 → бій» як кінцевий автомат забігу — 🌱.

## Мапа на каталог
- Є: `round-currency` ↔ золото й дохід · `shop-catalog`/`shop-window` ↔ торговці · `shop-buyback` ↔ продаж за половину · `inventory-limit` ↔ 10 слотів · `multi-cell-size` ↔ предмети на 2–3 слоти · `drag-drop-piece` · `hp-damage` · `status-effects` ↔ Burn/Poison/Freeze · `chain-reaction` ↔ предмет заряджає/прискорює інші · `tile-merge` ↔ дублікат → тир · `in-round-upgrades` ↔ тири й зачарування · `run-relics` ↔ навички · `async-multiplayer` ↔ привиди · `online-multiplayer`/`rating-system` ↔ Ranked · `character-select` · `mode-select` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+cooldown-manipulation` «Прискорити/сповільнити/заморозити/дозарядити чужий кулдаун» · entities/state · 🥉 · слот {kind: haste|slow|freeze|charge, dur}.
  - `+positional-targeting` «Ефект адресує позицію в ряду (сусід, найлівіший)» · entities/interact · 📎.
  - `+encounter-choice` «Година = вибір 1 з 3 карт подій» · game-logic/economy · 🌱.
  - `+stash-storage` «Неактивний сховок поза полем бою» · entities/state · 🌱.
  - `+ghost-opponent` «Суперник — збережений білд гравця з того ж етапу» · game-logic/opponent · 🥈.
  - `+multicast` «Кілька спрацювань за одну активацію» · entities/combat · 🌱.

## Пропозиції до словників
- `+effect:charge` — миттєво доповнити кулдаун цілі на t; `+effect:shield` — додати щит понад HP; `+effect:upgrade` — підняти тир; `+effect:sell` — продати за частку ціни; `+effect:reroll` — оновити вітрину.
- `+trigger:fight_start` / `+trigger:fight_end` — межі бою (на них висять «на початку бою» / «наприкінці бою»).
- `+cond:position` — місце в ряду (найлівіший, сусід праворуч).
- `+ui:cooldown-overlay` — заповнення кулдауну поверх предмета; `+ui:prestige-counter` — престиж поточний/повний; `+ui:day-hour-track` — день і година забігу.
- `+window:choice-window` — вибір 1 з N карт.
- `+card:cooldown-manipulation`, `+card:positional-targeting` — див. «Мапу на каталог».
- `+axis:time` — значення `phased`: підготовка покроково, бій у неперервному часі.

## Джерела
- ⭐ [Load Last Save: огляд The Bazaar](https://loadlastsave.substack.com/p/the-bazaar-review) — дні по 6 годин, вибір 3 торговців/подій, NPC на 3-й годині, PvP-привиди в кінці дня, 10 слотів, розміри 1/2/3, сховок, сусідство, leftmost-Loot, Dooley Core, крит ×2, автобій без ходів, тири навичок, зачарування.
- [Steam](https://store.steampowered.com/app/1617400/The_Bazaar/) — Tempo, реліз 13.08.2025, Windows/macOS, теги автобатлера, асинхронний PvP без таймерів.
- [game8: Gameplay Info](https://game8.co/articles/reviews/the-bazaar-gameplay-and-story-info) — Rug 4 + 2 за рівень до 10, Stash, розміри, тири й дублікати, Slow/Haste/Freeze/Charge/Multicast, Health/Shield/Regen/Burn/Poison/Crit, золото й дохід, продаж за половину, 1 досвід за подію.
- [rkblog: The Bazaar](https://rkblog.pages.dev/posts/games/the-bazaar-card-game) — день: 2 слоти + PvE + 2 слоти + PvP; кінець забігу (10 перемог / 15 днів / престиж); копії дошок за днями; набої; знищення предмета.
- [Wikipedia: Tempo Storm](https://en.wikipedia.org/wiki/Tempo_Storm) — історія, бета 2024, Season One 2025, перехід на Steam, асинхронний мультиплеєр.
- Steam News (API `ISteamNews/GetNewsForApp`, appid 1617400) — патчі: індикатор престижу, сховок, «перетворення зберігають розмір», дохід 5, Legendary-рейтинг, турнірна черга на 8, герої.

## Непевне
- (?) Розмір дошки: game8 (стаття до релізу) — 4 слоти на старті, +2 за рівень, макс. 10; огляд після релізу — просто 10 слотів. Що діє зараз — не перевірено.
- (?) Скільки престижу на старті й скільки знімає поразка (залежність від дня) — не знайдено; так само ліміт днів (15 — з бети).
- (?) Пісчана буря (Sandstorm), що наростальною шкодою завершує затяжний бій, — з памʼяті, у відкритих джерелах не побачив.
- (?) Взаємодія Shield з Poison: game8 пише, що щит зменшує й Burn, і Poison; за памʼяттю Poison щит ігнорує.
- (?) Haste/Slow — множник швидкості кулдауну (×2 / ×½?) — точних коефіцієнтів не бачив.
- (?) Фраза огляду «перемога над привидом замінює твій білд його» — незрозуміла, не включено.
- (?) Мобільна версія: у новинах Steam є «Mobile announcement», дату й платформи не перевіряв.
