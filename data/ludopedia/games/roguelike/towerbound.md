---
title: TowerBound
slug: towerbound
aka: [Towerbound]
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: none
  goal: state
year: 2027
platforms: [PC (Windows), Steam Deck]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4860450", best: true, note: "сторінка гри: 50 ручних поверхів у традиції Tower of the Sorcerer, «no luck», кольорові ключі, предмети, вівтарі, бестіарій; безкоштовне демо; реліз Q1 2027"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=TowerBound+steam+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, key-and-door, hp-damage, item-pickup, inventory-items, impassable-cells, round-currency, shop-catalog, stairs-levels, sequential-levels, player-death, cell-transform, achievements-window, +deterministic-combat, +damage-preview, +stat-gems, +monster-manual, +floor-fly]
proposes: ["+effect:fight(a, b)", "+effect:stat(a, name, ±n)", "+cond:can_damage(a, b)", "+window:codex-window", "+feature:bestiary-unlock"]
author: opus
date: 2026-11-09
---

# TowerBound — свіжа Magic Tower: 50 ручних поверхів, «у цій вежі нема удачі»

## Суть
Пряма спадкоємиця [magic-tower](magic-tower.md) (Tower of the Sorcerer): герой підіймається на 50 поверхів, де бій повністю передбачуваний, а HP, атака, захист, золото й кольорові ключі — валюти, які легко витратити не в тому порядку й заблокувати собі шлях. Поверхи — ручні головоломки без процедурної генерації. Нове відносно класики — сучасна подача (контролер, Steam Deck), бестіарій, що заповнюється перемогами, і набір предметів руху (посохи, крила, кирки, бомби). Станом на 2026-11 вийшло лише демо.

## Поле і час
- Квадратна сітка поверху (тег «Grid-Based Movement»); 50 поверхів, зʼєднаних сходами (?).
- Покроково; монстри стоять, бій ініціює гравець (за традицією жанру; сторінка прямо цього не каже).
- `random: none`: «no misses, no crits» — результат бою наперед відомий зі статів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP, Attack, Defense, Gold, ключі | рух сіткою; вхід у монстра = бій, у двері = ключ |
| Монстр | enemy | HP, ATK, DEF (?) | бій за статами без випадковості; ціну бою видно до рішення |
| Бос | boss | — | «boss encounters» між етапами |
| Кольорові двері (напр., червоні) | gate | колір | фіксовані; відкриваються ключем кольору |
| Кольоровий ключ | pickup | колір | ресурс, порядок витрати вирішує прохідність |
| Посох · крила · кирка · бомба | pickup | — | «змінюють, як ти рухаєшся вежею» (кирка/бомба — руйнування, крила — між поверхами (?)) |
| Вівтар | neutral | ціна | продає силу за ресурси |
| Купець · NPC | neutral | — | торгівля, сюжет |
| Сходи | static | — | на сусідній поверх |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`.
- КОЛИ `contact(hero, monster)` → ТО `custom: «детермінований бій за статами (формула не опублікована)»`; ЯКЩО `hp_zero(hero)` → ТО `lose`; інакше `disappear(monster)`, `currency(+gold)`, `custom: «запис у бестіарій»`.
- КОЛИ `contact(hero, door[c])` → ЯКЩО `has(hero, key[c])` → ТО `disappear(door)`, `take(hero, key[c])`; інакше `block`.
- КОЛИ `picked(hero, key|stat_item)` → ТО `pickup` (?).
- КОЛИ `use(hero, pickaxe|bomb)` → ТО `custom: «руйнує перешкоду»` (?).
- КОЛИ `use(hero, wings)` → ТО `custom: «переміщення між поверхами»` (?).
- КОЛИ `contact(hero, altar|merchant)` → ТО `window(shop-window)`; купівля → `currency(−price)`, `custom: «+стат / предмет»`.
- КОЛИ `custom: «ресурси витрачено так, що далі не пройти»` → ТО `custom: «софтлок — гра цього не каже»` (опис: «spend them in the wrong order and the tower closes»).
- КОЛИ `died(final_boss)` → ТО `win` (?).

## Керування і ввід
- Повна підтримка контролера, «designed with Steam Deck in mind»; клавіатура (?).

## Вікна, меню, HUD
- `game-screen`: поверх, `stat-panel` (HP, ATK, DEF, Gold, ключі) (?), прогноз втрат (?).
- `codex-window`: бестіарій, що заповнюється з перемогами.
- `shop-window`: вівтарі й купці; `dialogue-window`: NPC, «story beats».
- `achievements-window` (Steam Achievements), `main-menu`, `settings-window` (мови: EN, 简体, 繁體, 日本語).

## Фічі поза полем
- `achievements`, `gamepad-support`, `localization` (4 мови); Steam Family Sharing.
- Безкоштовне демо до релізу.
- Undo / сейви — сторінка не згадує.

## Варіації й родичі
- [magic-tower](magic-tower.md) — батько; [tactical-nexus](tactical-nexus.md) (undo/redo, рахунок за HP), [h5mota](h5mota.md) (тисячі фанатських веж), [dungeonup](dungeonup.md) (процедурні поверхи).
- Відмінності від `magic-tower`: формально ті самі сутності; акценти — **бестіарій як прогресія**, предмети саме **руху** (посохи, крила), західна подача й контролер. Число поверхів — 50 (як у великих китайських вежах).
- Осі варіацій: як у `magic-tower` (генерація, прокачка, відкат, спец-здібності, ціни).

## Цікавинки для курсу
- Детермінований бій із прогнозом — 🌱 (див. `magic-tower`).
- Бестіарій, що відкривається перемогами (`codex-window` з прогресом) — 🌱.
- Детектор софтлоку: «чи можна ще дійти до сходів з поточними ключами/HP» — 🥇 (пошук у просторі станів).

## Мапа на каталог
- Є: `move-4dir` · `key-and-door` · `hp-damage` · `item-pickup` · `inventory-items` · `impassable-cells` · `round-currency` · `shop-catalog` · `stairs-levels` · `sequential-levels` · `player-death` · `cell-transform` (кирка/бомба) · `achievements-window`.
- **Нема** → `+deterministic-combat`, `+damage-preview`, `+stat-gems`, `+monster-manual`, `+floor-fly` — як у `magic-tower`.

## Пропозиції до словників
- `+effect:fight(a, b)`, `+effect:stat(a, name, ±n)`, `+cond:can_damage(a, b)` — повтор пропозицій сімʼї Magic Tower (ще не в словнику).
- `+window:codex-window` — бестіарій (⏳ кандидат, тут вжито).
- `+feature:bestiary-unlock` — запис у довідник відкривається першою перемогою над видом.

## Джерела
- ⭐ [Steam: TowerBound](https://store.steampowered.com/app/4860450) — опис, теги (Puzzle, RPG, Turn-Based Combat, Grid-Based Movement, Resource Management), демо, мови, реліз Q1 2027, розробник Jelte.
- YouTube: [пошук](https://www.youtube.com/results?search_query=TowerBound+steam+gameplay).

## Непевне
- (?) Формула бою, наявність прогнозу втрат на монстрі, хто бʼє першим — сторінка каже лише «бачиш ціну до рішення».
- (?) Що саме роблять посохи й крила; чи є телепорт між поверхами.
- (?) Розмір поверху, наявність undo/сейвів, рахунку чи рейтингу.
- (?) Реліз Q1 2027 і `year: 2027` — за сторінкою на 2026-11; демо агент не запускав.
