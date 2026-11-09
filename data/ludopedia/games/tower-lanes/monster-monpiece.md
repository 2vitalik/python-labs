---
title: Monster Monpiece
slug: monster-monpiece
aka: [限界凸騎 モンスターモンピース, Genkai Tokki Monster Monpiece]
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 2013
platforms: [PS Vita, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Monster_Monpiece", best: true, note: "сітка 7×3, чотири класи карт (melee, ranged, healer, booster), First Crush Rub, платформи й дати"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/限界凸騎_モンスターモンピース", note: "JA: поле 横7×縦3, синя половина — своя, червона — ворожа; призвані юніти рухаються самі; очки «こすりP» за перемоги"}
  - {kind: other, url: "https://www.cubed3.com/games/reviews/ps-vita/monster-monpiece", note: "рецензія з механікою: свої 3×3 + нейтральний стовпець, рука 5, колода 30–40, мана щохід, юніт чекає хід, 1 шкоди базі за прохід, злиття одного племені"}
  - {kind: other, url: "https://rpgsite.net/review/3621-monster-monpiece-review", note: "рецензія: три смуги, замок з кількома HP, мана, ATK/HP/INT, навички за рівні, паки 3–5 карт"}
  - {kind: steam, url: "https://store.steampowered.com/app/415300/Monster_Monpiece/", note: "PC-порт 2017: Skills, Potentials, Fusions, Aura Bonuses, 100+ карт"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Monster+Monpiece+battle+gameplay", note: "пошук; бої"}
stage: v1
coverage: 45
mechanics: [cursor-place, hp-damage, melee-vs-ranged, round-currency, enemy-reached-base, ai-opponent, pocket, end-screen, shop-window, +lane-grid, +deck-draw, +deck-builder, +card-collection, +auto-march-units, +summoning-sickness, +base-hp-duel, +front-ally-support, +same-tribe-fusion, +touch-upgrade-minigame, +card-packs, +lane-skill-effects]
proposes: ["+role:card", "+role:base", "+effect:draw_card", "+trigger:card_played", "+cond:own_half", "+window:deck-builder", "+window:upgrade-minigame", "+ui:mana-counter", "+card:front-ally-support", "+card:same-tribe-fusion"]
author: opus
date: 2026-11-09
---

# Monster Monpiece — картярка на полі 7×3: призвані карти самі крокують до ворожого замку, бʼються з тими, хто в досяжності, а прохід крізь усе поле знімає замку HP

## Суть
Карткова RPG від Compile Heart (PS Vita, 2013; PC, 2017). Гравець призиває з руки карти-«монстрів» на свою половину поля 7×3; юніт наступного ходу починає сам рухатися вперед по своєму ряду, атакує ворогів у досяжності, а дійшовши до протилежного краю, знімає 1 HP ворожого штабу. Чотири класи — ближній бій, дальній бій, лікар і підсилювач (бафер); підтримка діє на союзника прямо попереду. Між боями карти колекціонують, складають колоди й прокачують у міні-грі «First Crush Rub» (сенсорне «натирання» карт; фан-сервіс, через який гру критикували).

## Поле і час
- Поле 7 стовпців × 3 ряди (JA-вікі: 横7×縦3): у кожної сторони своя ділянка 3×3, між ними — один нейтральний стовпець (Cubed3). Ряд — смуга руху юнітів.
- Свої клітини — синя половина, ворожі — червона; за краєм поля — штаб (Headquarters, «замок»).
- Покроково: хід гравця → хід суперника; у свій хід відновлюється мана й призиваються карти, юніти рухаються й атакують без прямого керування.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Карта-юніт (monster girl) | ally (`+role:card`) | вартість мани, HP, ATK, INT, плем'я, клас, навички | призивається на свою ділянку; з наступного ходу крокує вперед по ряду |
| Melee | ally | високі HP й ATK | атакує ворога впритул попереду |
| Ranged | ally | менша ATK | атакує ворога на відстані (дальність — див. «Непевне») |
| Healer | ally | INT | лікує союзника прямо попереду |
| Booster | ally | INT | підсилює атаку союзника попереду або силу лікаря |
| Ворожий юніт | enemy | ті самі класи | дзеркальна поведінка з протилежного боку |
| Штаб гравця / суперника | static (`+role:base`) | кілька HP | −1 HP за кожного ворога, що пройшов поле; 0 → кінець бою |
| Мана | resource | — | відновлюється щохід, витрачається на призов; деякі навички додають |
| Рука | supply | 5 карт | добір з колоди |
| Колода | supply | 30–40 карт | збирається з колекції |
| Свіжопризваний юніт | ally | стан «чекає» | не рухається в хід призову (крім особливих навичок) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «колода перемішана, у руці 5 карт»`.
- КОЛИ `turn_start(player)` → ТО `currency(+n)` — мана відновлюється; `custom: «draw_card до 5 у руці»` (?).
- КОЛИ `input(summon, card, cell)` → ЯКЩО `turn_of(player)` and `custom: «own_half: клітина на своїй ділянці 3×3»` and `free(cell)` and `counter(mana, >=, cost)` → ТО `place(player, card)`, `currency(-cost)`; інакше `block`.
- КОЛИ `spawned(unit)` → ТО `set_state(unit, summoned, 1)` — цього ходу не рухається.
- КОЛИ `turn_start(side)` → ЯКЩО `not state(unit, summoned)` and `free(cell_ahead)` → ТО `move(unit, forward)`.
- КОЛИ `in_range(melee, enemy, 1)` → ТО `damage(enemy, atk)`.
- КОЛИ `in_range(ranged, enemy, n)` → ТО `damage(enemy, atk)` — `n` залежить від карти (?).
- КОЛИ `turn_start(side)` → ЯКЩО `occupied(cell_ahead, ally)` and `custom: «клас — healer»` → ТО `heal(ally, int)`.
- КОЛИ `turn_start(side)` → ЯКЩО `occupied(cell_ahead, ally)` and `custom: «клас — booster»` → ТО `counter(atk[ally], +int)`.
- КОЛИ `hp_zero(unit)` → ТО `disappear(unit)`.
- КОЛИ `reach(unit, enemy_edge)` → ТО `damage(enemy_base, 1)` (?) — що далі з юнітом, див. «Непевне».
- КОЛИ `custom: «два юніти одного племені обʼєднуються»` → ТО `merge(a, b → fused)` — характеристики сумуються (Cubed3; приклади племен — птахи, звірі, дракони).
- КОЛИ `custom: «навичка карти, напр. шкода ворогу в тому самому ряду»` → ТО `damage(enemy_in_lane, n)`; інша — `counter(atk[ally_in_column], +n)` (RPGSite).
- КОЛИ `hp_zero(enemy_base)` → ТО `win`; КОЛИ `hp_zero(own_base)` → ТО `lose`.
- КОЛИ `level_end` → ЯКЩО `custom: «бій виграно»` → ТО `counter(rub_points, +n)`, `give(player, card_pack)` — пак 3–5 карт (RPGSite).
- КОЛИ `input(rub, card)` (поза боєм) → ЯКЩО `counter(rub_points, >=, cost)` → ТО `custom: «рівень карти +1: або ріст характеристик, або жертва характеристик заради нової навички»`; високий рівень → `transform(card, evolved_form)`.
- Перемога: HP ворожого штабу = 0 · Поразка: HP свого штабу = 0 · Рахунок: — (прогрес — колекція й рівні карт).

## Керування і ввід
- Vita: тач — перетягнути карту з руки на клітину своєї ділянки (EN-вікі: «drags … onto the grid»); кнопки — вибір карти й клітини.
- PC: миша/клавіатура; рецензенти пишуть, що міні-гра «натирання» з мишею незручна.
- Юнітами напряму не керують: лише вибір, кого й куди призвати.

## Вікна, меню, HUD
- `main-menu`: Story → мапа/сцени візуальної новели (`dialogue-window`); вільний бій; колекція; налаштування (`settings-window`).
- `game-screen`: поле 7×3 з 3D-chibi юнітами, `pocket` (рука 5 карт), лічильник мани (`+ui:mana-counter`), HP обох штабів (`hp-bar`), `tooltip` з характеристиками карти.
- `+window:deck-builder` — колода з колекції 100+ карт.
- `+window:upgrade-minigame` — «First Crush ❤ Rub»: витрата очок на рівень карти, нові арти.
- `shop-window` — паки карт і очки «натирання».
- `end-screen` — перемога/поразка, нагорода (очки, пак).

## Фічі поза полем
- `unlockables`: еволюції карт з новими артами; `+card-packs` — паки за перемоги й у крамниці.
- Сюжетна кампанія (VN-сцени між боями); Vita — онлайн-бої на двох (`online-multiplayer`), у PC-порті мультиплеєра нема.
- Бонус за попереднє замовлення — камео Нептунії (Hyperdimension Neptunia).

## Варіації й родичі
- Сиквел: Monster Monpiece Naked (iOS/Android, 2016) — правила не перевірені.
- Родичі в корпусі: [ironclad-tactics](ironclad-tactics.md) і [the-battle-cats](the-battle-cats.md) (юніти самі марширують смугою, база з HP), [mega-man-battle-network](mega-man-battle-network.md) (поле, поділене на половини), [plants-vs-zombies-heroes](plants-vs-zombies-heroes.md), [inscryption](inscryption.md), [queens-blood](queens-blood.md) (поле 3×5 з картами в клітинках).
- **Осі варіацій**: рух юніта — стоїть / крокує сам / рухається за наказом · підтримка — на сусіда попереду / на ряд / на стовпець · прохід до бази — знімає 1 HP / знімає ATK · злиття — немає / одного племені / однакових карт.

## Цікавинки для курсу
- Автомарш юнітів по рядах з «хворобою призову» (хід очікування) і зупинкою перед зайнятою клітиною — 📎.
- Чотири класи з різними цілями: впритул, на відстань, лікування й бафер союзника попереду — 🥉 (порядок застосування в межах ходу).
- Поле з нейтральним стовпцем: своя ділянка 3×3 як зона призову — 🌱.
- Злиття юнітів одного племені з сумою характеристик — 📎.
- Колекція → колода → бій → нагорода-пак: замкнений цикл метапрогресу — 🥉.

## Мапа на каталог
- Є: `cursor-place` ↔ призов на клітину · `hp-damage` · `melee-vs-ranged` ↔ класи · `round-currency` ↔ мана · `enemy-reached-base` ↔ прохід до штабу · `ai-opponent` · `pocket` ↔ рука · `end-screen`, `shop-window`.
- **Нема** → пропозиції карток:
  - `+lane-grid`, `+deck-draw`, `+deck-builder`, `+card-collection`, `+auto-march-units`, `+summoning-sickness`, `+base-hp-duel` — уже в корпусі.
  - `+front-ally-support` «Лікар/бафер діє на союзника прямо попереду» · entities/combat · 🌱.
  - `+same-tribe-fusion` «Два юніти одного племені зливаються, характеристики сумуються» · entities/state · 📎.
  - `+touch-upgrade-minigame` «Прокачка карти міні-грою дотиків» · game-logic/economy · 🥉.
  - `+card-packs` «Пак з випадковими 3–5 картами» · game-logic/economy · 🌱.
  - `+lane-skill-effects` «Навички по ряду/стовпцю від позиції карти» · entities/combat · 📎.

## Пропозиції до словників
- `+role:card`, `+role:base` — повтори з корпусу.
- `+effect:draw_card` — повтор.
- `+trigger:card_played` — повтор (призов карти як подія).
- `+cond:own_half` — клітина на своїй ділянці поля (зона призову).
- `+window:deck-builder` — повтор; `+window:upgrade-minigame` — міні-гра прокачки карти.
- `+ui:mana-counter` — повтор (поточна мана).
- `+card:front-ally-support`, `+card:same-tribe-fusion`.

## Джерела
- ⭐ [Wikipedia: Monster Monpiece](https://en.wikipedia.org/wiki/Monster_Monpiece) — сітка 7×3, перетягування карт, чотири класи, First Crush Rub, платформи, 100+ карт.
- [JA Wikipedia](https://ja.wikipedia.org/wiki/限界凸騎_モンスターモンピース) — 横7×縦3, синя й червона половини, юніти рухаються самі, очки «натирання» за перемоги.
- [Cubed3: рецензія Vita](https://www.cubed3.com/games/reviews/ps-vita/monster-monpiece) — 3×3 + нейтральний стовпець, рука 5, колода 30–40, мана щохід, хід очікування, крок на клітину, 1 шкоди базі, злиття одного племені.
- [RPGSite: рецензія](https://rpgsite.net/review/3621-monster-monpiece-review) — три смуги, замок з кількома HP, мана від ходу й навичок, ATK/HP/INT, навички, паки 3–5 карт.
- [Steam](https://store.steampowered.com/app/415300/Monster_Monpiece/) — PC-порт 2017, Skills/Potentials/Fusions/Aura Bonuses.
- YouTube: пошук «Monster Monpiece battle gameplay».

## Непевне
- (?) Скільки мани відновлюється за хід і чи є стеля; скільки карт можна призвати за хід (Cubed3: «одну з пʼяти» — можливо, спрощення).
- (?) Стартове HP штабу («кілька»), добір карт щохід.
- (?) Дальність ranged-юнітів; що буває, коли попереду ворог: стоїть і бʼється чи проходить; хто бʼє першим.
- (?) Чи зникає юніт після удару по штабу.
- (?) Як саме ініціюється злиття (призов поверх союзника?) і що таке Aura Bonuses та Potentials (Steam називає без пояснень).
- (?) Режими поза сюжетом (вільний бій, онлайн-лобі Vita) — з рецензій уривками.
