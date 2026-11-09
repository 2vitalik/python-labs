---
title: "Magic Tower: Legion (军团魔塔)"
slug: magic-tower-legion
aka: [军团魔塔, Legion Magic Tower]
family: roguelike
also: [tactics]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: state
year: 2026
platforms: [PC (Steam)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4012830/Magic_Tower_Legion/", best: true, note: "опис: Magic Tower загоном, порядок виходу в бій, тяжко поранений вибуває — наступний продовжує, фіксовані числа, невідновні ресурси"}
  - {kind: steam, url: "https://store.steampowered.com/app/4012830/Magic_Tower_Legion/?l=schinese", note: "китайський опис: 固定数值战斗, 破炸飞, ролі 进攻/防御/辅助/成长, 合成装备"}
  - {kind: steam, url: "https://store.steampowered.com/app/4253360/Magic_Tower_Legion_Demo/", note: "демо 2.01.2026: ~20 персонажів, дві вежі, ~40 видів спорядження"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Magic+Tower+Legion+%E5%86%9B%E5%9B%A2%E9%AD%94%E5%A1%94+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [hp-damage, item-pickup, inventory-items, key-and-door, round-currency, unit-xp-skills, stairs-levels, character-select, level-select, +deterministic-combat, +party-relay-order, +retreat-on-injury, +recruit-party, +stat-gems, +crafting-recipes, +random-floor-layout, +non-renewable-resources, +enemy-scaling]
proposes: ["+trigger:bump", "+effect:fight", "+effect:retreat(a)", "+effect:next_in_queue", "+cond:queue_empty", "+window:battle-order", "+window:recruit-window", "+window:crafting-window", "+axis:actors=party-queue"]
author: opus
date: 2026-11-09
---

# Magic Tower: Legion — Magic Tower загоном: бій за фіксованими числами веде черга героїв, поранений вибуває, наступний продовжує

## Суть
Роглайк у жанрі «магічної вежі» ([magic-tower](magic-tower.md)): підйом поверхами з ключами, зіллями, самоцвітами й монстрами, у яких **фіксовані числа** бою, а ресурси **не відновлюються**. Головна відмінність — замість одного героя **загін**: гравець наймає персонажів з активними/пасивними вміннями (атакуючі, захисні, підтримка, «ростучі») і задає **порядок виходу в бій** під тип і розташування ворогів. Тяжко поранений герой виходить з бою, і наступний у черзі продовжує. Поверхи, ресурси, предмети й персонажі частково випадкові — «єдиної найкращої стратегії нема».

## Поле і час
- Поверхи вежі, вид згори, 2D-піксельна графіка; поверх — поле класичної Magic Tower (клітинна карта з дверима, предметами й монстрами, див. «Непевне»).
- Покроково: бій — розрахунок за фіксованими числами, без кидків.
- `random: setup` — випадкове збирання поверхів, ресурсів, предметів і персонажів на початку забігу/поверху.
- Дилема темпу: витратити ресурси — поверх легший, але «вороги теж ростуть»; притримати — більше золота й досвіду з монстрів на потім.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Стартовий герой | player | середні характеристики | веде загін вежею |
| Найнятий персонаж | ally | роль (атака / захист / підтримка / ріст), активні й пасивні вміння, спорядження | стоїть у черзі бою; тяжко поранений — вибуває, далі бʼється наступний |
| Монстр | enemy | фіксовані числа, золото, досвід | бій ініціює гравець; перемога дає золото й досвід |
| Фінальний бос | boss | — | мета забігу; під нього бережуть витратні предмети |
| Ключ | pickup | — | базовий витратний ресурс для дверей |
| Двері | gate | — | відчиняються ключем (жанрова конвенція) |
| Зілля, самоцвіти | pickup | — | лікування / посилення характеристик |
| 破炸飞 (кирка, бомба, політ) | pickup | одноразові | базові інструменти жанру: пробити стіну, підірвати, перелетіти на поверх |
| Матеріали | resource | — | збираються у вежі, з них крафтять зброю й броню |
| Спорядження (Tier 1–2) | pickup | ~40 видів у демо | одягається на героя під його риси |
| Витратні предмети | pickup | тимчасовий ефект | тимчасове посилення зараз або запас на боса |
| Сходи | static | — | на наступний поверх |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(party, dir)`.
- КОЛИ `input(order, list)` → ТО `custom: «задати порядок виходу героїв у бій»` (під тип і позиції ворогів).
- КОЛИ `contact(party, monster)` → ТО `custom: «бій за фіксованими числами; бʼється перший герой черги»`.
- КОЛИ `state_on(hero, seriously_injured)` → ТО `custom: «герой виходить з бою»`, `custom: «наступний у черзі продовжує цей самий бій»`.
- КОЛИ `custom: «у черзі не лишилось героїв»` → ТО `lose`.
- КОЛИ `died(monster)` → ТО `currency(+gold)`, `counter(xp, +n)`.
- КОЛИ `contact(party, door)` → ЯКЩО `has(party, key)` → ТО `disappear(door)`, `take(party, key)`; інакше `block`.
- КОЛИ `contact(party, potion | gem)` → ТО `pickup`, `custom: «+HP / +характеристика»`.
- КОЛИ `input(use, consumable)` → ТО `set_state(hero, boost, dur)`.
- КОЛИ `input(use, pickaxe | bomb | fly)` → ТО `custom: «пробити стіну / прибрати перешкоду / перелетіти»` (одноразово).
- КОЛИ `input(craft, recipe)` → ЯКЩО `has(party, materials)` → ТО `take(party, materials)`, `give(hero, equipment)`.
- КОЛИ `input(recruit, character)` → ТО `custom: «персонаж додається в загін і чергу»`.
- КОЛИ `enter(party, stairs)` → ТО `custom: «наступний поверх»`, `custom: «вороги сильнішають»`.
- КОЛИ `died(final_boss)` → ТО `win`.
- Перемога: здолати боса вежі. Поразка: загін вичерпано (або ресурсів не вистачає далі — «софтлок» жанру). Рахунок: невідомо.

## Керування і ввід
- Рух загону вежею (клавіші/миша — див. «Непевне»); вікно порядку бою — перестановка героїв у черзі; екіпірування й крафт — у меню.

## Вікна, меню, HUD
- `main-menu` → `level-select` (у демо — дві вежі: Tower of Training і Tower of Slimes) → `game-screen`.
- `game-screen`: поверх, ресурси (ключі, золото, досвід), загін.
- `+window:battle-order` — черга героїв на бій; `+window:recruit-window` — найм (≈20 персонажів у демо); `inventory-window` + `+window:crafting-window` — спорядження й крафт.
- `end-screen` — перемога над босом або поразка загону.

## Фічі поза полем
- Демо (2.01.2026): один стартовий герой, ~20 персонажів для найму, 2 вежі, ~40 видів спорядження Tier 1–2 і витратні предмети. Мови — англійська, спрощена китайська.
- Повна гра — 2026 (на момент запису ще не вийшла).

## Варіації й родичі
- База: [magic-tower](magic-tower.md) — формула бою, ключі трьох кольорів, самоцвіти, 破炸飞; [h5mota](h5mota.md), [tactical-nexus](tactical-nexus.md), [dungeonup](dungeonup.md) (процедурні поверхи), [towerbound](towerbound.md).
- Родич за загоном-чергою: [mystery-dungeon](mystery-dungeon.md) (напарники), тактики з ротацією бійців.
- Осі варіацій: **хто бʼється** (один герой / черга загону з виходом пораненого) · **генерація** (ручна вежа / випадкові поверхи) · **ресурси** (відновні / невідновні) · **вороги** (статичні / ростуть з часом).

## Цікавинки для курсу
- Бій «естафетою»: черга героїв проти одного монстра, поранений вибуває, бій продовжує наступний — 📎 (черга + детермінований бій).
- Порядок черги як головоломка: перебір перестановок під тип ворога — 🥉 (n! варіантів, відсікання).
- Дилема «витратити зараз / притримати», бо вороги ростуть — 🌱 (одна змінна масштабу).
- Випадкові поверхи у жанрі без рандому в бою — 🥈 (генерація має лишати вежу розвʼязною).

## Мапа на каталог
- Є: `hp-damage` · `item-pickup` · `inventory-items` · `key-and-door` · `round-currency` (золото) · `unit-xp-skills` (досвід, вміння героїв) · `stairs-levels` · `character-select` (найм) · `level-select` (вежі).
- **Нема** → пропозиції карток:
  - `+deterministic-combat` «Бій за формулою без кидків» · entities/combat · 📎.
  - `+party-relay-order` «Загін бʼється чергою, порядок задає гравець» · entities/combat · 📎 · слот {order}.
  - `+retreat-on-injury` «Тяжко поранений вибуває з бою» · entities/combat · 🌱 · слот {threshold}.
  - `+recruit-party` «Найм персонажів у загін» · game-logic/economy · 🌱.
  - `+stat-gems` · 🌱; `+crafting-recipes` · 🥉; `+random-floor-layout` «Випадкові поверхи у вежі» · levels/generation · 🥈; `+non-renewable-resources` · 🌱; `+enemy-scaling` «Вороги ростуть з поступом» · game-logic/waves · 🌱.

## Пропозиції до словників
- `+trigger:bump` — загін «входить» у клітину монстра/дверей (бій як наслідок руху).
- `+effect:fight` — атомарний розрахунок бою за формулою; `+effect:retreat(a)` — сутність виходить з бою, лишаючись у загоні; `+effect:next_in_queue` — у бій стає наступний з черги.
- `+cond:queue_empty` — у черзі бою нікого не лишилось.
- `+window:battle-order`, `+window:recruit-window`, `+window:crafting-window` — див. «Вікна».
- `+axis:actors=party-queue` — загін як черга бійців, а не набір фігур на полі.

## Джерела
- ⭐ [Steam: Magic Tower: Legion](https://store.steampowered.com/app/4012830/Magic_Tower_Legion/) — опис механіки загону, черги й виходу пораненого, рандом поверхів, крафт, витратні предмети.
- [Steam (китайський опис)](https://store.steampowered.com/app/4012830/Magic_Tower_Legion/?l=schinese) — 固定数值战斗与不可再生资源, 破炸飞, ролі 进攻型/防御型/辅助型/成长型, «敌人也会不断成长».
- [Steam: Magic Tower: Legion Demo](https://store.steampowered.com/app/4253360/Magic_Tower_Legion_Demo/) — склад демо, дата 2.01.2026, теги (Turn-Based Tactics, Top-Down, Logic, Puzzle).

## Непевне
- (?) Сітка поверху, рух у 4 напрямки й двері кольорів — жанрова конвенція Magic Tower; опис Steam прямо не каже ні про клітини, ні про двері.
- (?) Формула бою і що саме означає «тяжко поранений» (поріг HP) — не описано; чи наступний герой бʼє того самого монстра з його залишком HP — з логіки «продовжує бій».
- (?) Розшифровка 破炸飞 як «кирка / бомба / політ» — за жанровою традицією (破墙镐, 炸弹, 飞行器); у грі можуть бути інші ефекти.
- (?) `info: full` — у класичній вежі поверх видно цілком; для Legion не перевірено.
- (?) Керування, збереження/undo, складності, рахунок — не описані.
