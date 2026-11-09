---
title: Cave Noire
slug: cave-noire
aka: [ケイヴノワール]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: collect
year: 1991
platforms: [Game Boy]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cave_Noire", best: true, note: "4 типи квестів × 10 рівнів складності, 4 фази ходу, туманні кімнати, пастки"}
  - {kind: other, url: "https://nintendoeverything.com/famicompendium-cave-noire/", note: "огляд: предмети з дерева на старті, без досвіду, вороги ходять маршрутами, квест < 10 хв"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/List_of_roguelikes", note: "у списку роглайків"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cave+Noire+Game+Boy+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, hp-damage, dungeon-generation, collect-quota, difficulty-levels, level-unlock, permadeath, inventory, inventory-items, inventory-limit, item-pickup, enemy-patrol, fog-of-war, teleport, destructible-blocks, environment-death, stairs-levels, save-progress, +quest-goal-select, +rescue-captive, +kill-toggles-room-fog, +random-start-loadout, +no-carryover-items]
proposes: ["+effect:rescue(b)", "+window:quest-board", "+feature:rank-title", "+card:quest-goal-select", "+card:kill-toggles-room-fog"]
author: opus
date: 2026-11-09
---

# Cave Noire — роглайк-«міні-квест»: один спуск — одна мета, і нічого не забираєш із собою

## Суть
Konami-роглайк для Game Boy (лише Японія). Гільдія шукачів пригод у селі Карузу видає **квест одного з чотирьох типів**: убити N монстрів, визволити фей із кліток, зібрати золото або зібрати сфери. Під кожен квест генерується нове підземелля; герой стартує з жменькою випадкових предметів, **без досвіду** — уся сила з того, що знайдеш, і після квесту все зникає. Кожен тип має 10 рівнів складності: вищий — більша квота, інші стартові стати, сильніші вороги. Квест короткий (≈10 хв), спроба одна.

## Поле і час
- Вигляд згори, клітинне підземелля з кімнатами; поверхи вниз (через ями — «провалитись на наступний рівень»).
- Покроково: хід поділено на 4 фази — рух гравця → атака гравця → атака монстрів → рух монстрів.
- Туманні кімнати: підлогу не видно, доки на неї не ступиш, але очі монстрів світяться в темряві.
- Генерація на кожен квест; бій має випадковий складник (удача + кидок).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP, атака, захист, удача | крок, удар по сусідній клітині, предмети |
| Монстр | enemy | атака, захист, HP | ходить заданим маршрутом; бʼє сусіда у фазі атаки |
| Монстр-«ліхтар» | enemy | — | убитий — туман у кімнаті зникає |
| Монстр-«морок» | enemy | — | убитий — кімната стає туманною (протилежний ефект) |
| Фея в клітці | container | — | визволити — +1 до квоти (квест фей) |
| Золото | pickup | — | +квота (квест золота) |
| Сфера (схожа на чашу) | pickup | — | +квота (квест сфер) |
| Скриня | container | рідкісна | дає предмет |
| Зброя / броня | pickup | бонус до статів | одягнути — стати ↑ |
| Зілля, закляття, кільця | pickup | лікування, отрута, шкода ↑, невидимість | одноразово або на час |
| Смолоскип | pickup | — | світло (?) |
| Яма | hazard | — | провал на рівень нижче + шкода |
| Нестійка підлога | hazard | — | (?) обвалюється |
| Лава | hazard | — | смертельна |
| Телепорт | terrain | — | переносить |
| Руйнована стіна | static | — | можна розбити |
| Таємний прохід | static | — | прихований |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)` (фаза 1).
- КОЛИ `input(attack)` → ЯКЩО `adjacent(hero, enemy)` → ТО `custom: «шкода з атаки, захисту, удачі й випадкового кидка»` (фаза 2).
- КОЛИ `turn_end(hero)` → ЯКЩО `adjacent(enemy, hero)` → ТО `damage(n)` (фаза 3); далі `custom: «монстри крокують своїм маршрутом»` (фаза 4).
- КОЛИ `hp_zero(hero)` → ТО `lose`; `custom: «квест провалено, наступна спроба — нове підземелля»`.
- КОЛИ `died(enemy)` → ЯКЩО `mode(kill)` → ТО `counter(quota, +1)`.
- КОЛИ `contact(hero, cage)` → ЯКЩО `mode(fairies)` → ТО `counter(quota, +1)`, `disappear_b`.
- КОЛИ `contact(hero, gold|orb)` → ТО `pickup`, `counter(quota, +1)`.
- КОЛИ `counter(quota, ==, target)` → ТО `custom: «квест виконано»`, `win` (як саме завершити — див. «Непевне»).
- КОЛИ `died(light_monster)` → ТО `reveal(room)`; КОЛИ `died(dark_monster)` → ТО `hide(room)`.
- КОЛИ `enter(hero, fog_cell)` → ТО `reveal(cell)`.
- КОЛИ `enter(hero, pit)` → ТО `damage(n)`, `next_level`.
- КОЛИ `enter(hero, lava)` → ТО `lose`.
- КОЛИ `enter(hero, teleporter)` → ТО `teleport`.
- КОЛИ `died(enemy)` → ЯКЩО `prob(p)` → ТО `spawn(item)` (дроп).
- КОЛИ `input(use item)` → ЯКЩО `has(hero, item)` → ТО `heal(hero, n)` / `set_state(hero, invisible, t)` / `custom: «шкода ↑»`; отрута — `damage(n)`.
- КОЛИ `level_start` → ТО `give(hero, random items)` (з дерева); КОЛИ `level_end` → ТО `custom: «інвентар і спорядження зникають»`.
- КОЛИ `custom: «пройдено рівень складності k квесту»` → ТО `unlock(k+1)`; рівень 6 усіх чотирьох → `custom: «звання Adventurer»`, відкриті рівні 7–10.

## Керування і ввід
- Хрестовина Game Boy — крок; кнопка — удар (?) і меню предметів (?).
- Фазовий хід: спершу рухаєшся, потім бʼєш — монстри відповідають після обох фаз.

## Вікна, меню, HUD
- `main-menu` → `quest-board` у гільдії: вибір одного з 4 квестів і його рівня складності.
- `game-screen`: мапа поверху, HP, лічильник квоти (`progress-bar` / `remaining-counter`) (?).
- `inventory-window`: предмети квесту (у джерелах — 8 слотів (?)).
- `end-screen`: квест виконано / провалено.
- Село Карузу як хаб (4 підземелля + гільдія) — `world-map` у мініатюрі.

## Фічі поза полем
- `level-unlock`: 4 × 10 рівнів складності; рівень 6 усіх — звання (`rank-title`), далі 4 пост-гейм рівні.
- Збереження — лише прогрес рівнів (не стан квесту).
- Фан-переклад англійською (2012).

## Варіації й родичі
- Близько до «одноразових» роглайків-квестів: `mystery-dungeon` (Шірен) — данж за данжем без перенесення; `desktop-dungeons` — короткий забіг і мета-прогрес.
- `rogue` — класичний кістяк; Cave Noire прибирає досвід і накопичення.
- **Осі варіацій**: мета забігу (амулет на дні / вбити квоту / визволити / зібрати); що переноситься між забігами (нічого / відкриті рівні / предмети); туман (глобальний / покімнатний з перемикачами-монстрами).

## Цікавинки для курсу
- Вибір мети як параметр генератора: та сама гра, 4 умови перемоги — 🌱.
- Фазовий хід (рух → атака → атака ворогів → рух ворогів) — 🌱.
- Монстри-перемикачі туману кімнати — 📎.
- Таблиця «рівень складності → квота, стартові стати, вороги» — 🌱 (дані замість коду).
- Випадковий стартовий набір і втрата всього наприкінці — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `hp-damage` · `dungeon-generation` · `collect-quota` (квота вбивств/фей/золота/сфер) · `difficulty-levels` · `level-unlock` · `permadeath` (одна спроба на квест) · `inventory`, `inventory-items`, `inventory-limit` · `item-pickup` · `enemy-patrol` (маршрути) · `fog-of-war` (туманні кімнати) · `teleport` · `destructible-blocks` · `environment-death` (лава) · `stairs-levels` (ями вниз) · `save-progress`.
- **Нема** → пропозиції карток:
  - `+quest-goal-select` «Мета забігу обирається перед стартом» · game-logic/win · 🌱 · слоти {goal, quota}.
  - `+rescue-captive` «Визволити полонених (клітки)» · game-logic/win · 🌱.
  - `+kill-toggles-room-fog` «Убитий монстр відкриває/закриває кімнату» · entities/state · 📎.
  - `+random-start-loadout` «Випадковий стартовий набір предметів» · levels/generation · 🌱.
  - `+no-carryover-items` «Предмети не переносяться між забігами» · game-logic/progression · 🌱.

## Пропозиції до словників
- `+effect:rescue(b)` — визволити полоненого (зараз `disappear_b` + `counter`).
- `+window:quest-board` — дошка квестів гільдії з вибором мети й складності.
- `+feature:rank-title` — звання за пройдені рівні складності.
- `+card:quest-goal-select` · `+card:kill-toggles-room-fog`.

## Джерела
- ⭐ [Wikipedia: Cave Noire](https://en.wikipedia.org/wiki/Cave_Noire) — 4 квести × 10 рівнів, 4 фази ходу, туман, ями/лава/телепорти, монстри-перемикачі, звання Adventurer.
- [Famicompendium: Cave Noire](https://nintendoeverything.com/famicompendium-cave-noire/) — стартові предмети з дерева, без досвіду, маршрути ворогів, рідкісні скрині.
- [Wikipedia: List of roguelikes](https://en.wikipedia.org/wiki/List_of_roguelikes).
- YouTube: [пошук «Cave Noire Game Boy gameplay»](https://www.youtube.com/results?search_query=Cave+Noire+Game+Boy+gameplay).

## Непевне
- (?) Як завершується квест після виконання квоти (вихід, повернення на поверхню, автоматично) — у джерелах нема.
- (?) Чи кожен із 4 підземель привʼязаний до свого типу квесту (так каже один пошуковий підсумок) — Wikipedia цього прямо не каже.
- (?) 8 слотів інвентаря — лише з пошукового підсумку, сторінки не бачив.
- (?) Яка саме роль смолоскипа і що робить «нестійка підлога»; хто з монстрів «ліхтар», а хто «морок».
- (?) Wikipedia згадує «піднімати рівень», Famicompendium — «досвіду нема»; ймовірно, «рівень» = рівень складності квесту.
- (?) 4 напрямки руху і розкладка кнопок — з природи Game Boy, не перевірено.
