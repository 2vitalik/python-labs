---
title: Othercide
slug: othercide
aka: []
family: tactics
also: [roguelike]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: state
year: 2020
platforms: [PC, PS4, Xbox One, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Othercide", best: true, note: "динамічний таймлайн, AP і виснаження, три класи, лікування лише жертвою, Remembrances після поразки"}
  - {kind: steam, url: "https://store.steampowered.com/app/798490/", note: "Dynamic Timeline System, ланцюги дій і контр, «sacrifice one to heal another», Perma Death, боси"}
  - {kind: other, url: "https://blog.playstation.com/?p=333710", note: "PlayStation Blog: поріг 50 AP, Burst, реакції, затримки ворогів, пастки на таймлайні, Remembrances і Memories"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Othercide+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, permadeath, unit-xp-skills, status-effects, telegraphed-intents, reachable-highlight, path-preview, threat-range, destroy-all-enemies, ai-opponent, mode-indicator, save-autosave, codex-window, character-select, +initiative-timeline, +ap-overspend-delay, +delayed-action, +interrupt-reaction, +turn-order-manipulation, +sacrifice-heal, +run-meta-unlocks]
proposes: ["+trigger:timeline_turn", "+trigger:interrupt", "+effect:delay_turn", "+effect:advance_turn", "+effect:queue_action", "+effect:sacrifice", "+cond:ap", "+ui:timeline-bar", "+ui:action-points-preview", "+window:inner-dream", "+window:remembrance-select", "+feature:run-carryover", "+axis:turn-structure=time-track"]
author: opus
date: 2026-11-09
---

# Othercide — тактика на таймлайні: кожна дія зсуває твій наступний хід, а ворожі атаки можна перебити

## Суть
Гравець веде загін «Доньок» проти чудовиськ на невеликих картах-сітках. Звичайних «ходів сторін» нема: усі юніти стоять на **динамічному таймлайні ініціативи**, і хто ближче до початку — той ходить. Очки дії (AP) — це і бюджет дії, і ціна в часі: витратив до половини — походиш знову скоро; перевитратив (Burst) — отримав більше руху й шкоди зараз, але падаєш у кінець черги. Здоровʼя не відновлюється само: вилікувати Доньку можна лише **принісши в жертву іншу**. Поразка загону не скидає все — гра роглайкова: між спробами лишаються відкриття (Remembrances).

## Поле і час
- Квадратна сітка невеликих тактичних карт; камера згори під кутом, перешкоди й укриття — тло (?).
- Час — **таймлайн**: шкала ініціативи, на якій стоять піктограми всіх юнітів, а також відкладені дії (атаки, що спрацюють пізніше) і пастки/зони, що «вибухнуть» у заданий момент.
- Хід юніта = одна активація: витратив AP → юніт зсувається вперед по шкалі на відстань, що залежить від витрати; поріг — 50 AP.
- Між боями — «стратегічний» шар: вибір місій, найм і жертва Доньок, прогрес до боса ери (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Blademaster | piece | HP, AP, ближній бій | сильна базова атака — старт комбо; клинкові вміння |
| Shieldbearer | piece | високе HP | захищає себе й сусідів; затримує ворогів на таймлайні і переставляє їх |
| Soulslinger | piece | дальня зброя | підтримка: реакції, що зупиняють ворожу атаку або спрацьовують, коли ворогу завдано шкоди |
| Ворог (Suffering) | enemy | HP, своя позиція на таймлайні | ходить за чергою; частина атак — відкладені, видно на таймлайні наперед |
| Бос | boss | фази (?) | битва з «джерелом Страждання» наприкінці етапу |
| Пастка / небезпечна зона | hazard | момент спрацювання на таймлайні | спрацьовує, коли таймлайн доходить до її позначки |
| Відкладена дія | mark | позиція на таймлайні, область | атака/вміння, що виконається пізніше; можна встигнути перебити або вийти з зони |
| Таймлайн | zone | шкала ініціативи | впорядковує всі юніти й події |
| Memory | pickup | слот вміння | модифікує вміння Доньки (з Remembrances) |
| Remembrance | resource | умова відкриття | постійний бонус між забігами |

## Правила (КОЛИ → ЯКЩО → ТО)
- Черга: КОЛИ `custom: «таймлайн дійшов до юніта»` → ТО `custom: «юніт діє»`; КОЛИ `turn_end(unit)` → ТО `custom: «юніт зсувається по таймлайну залежно від витрачених AP»`.
- КОЛИ `input(move|skill, daughter)` → ЯКЩО `counter(ap, ≥, cost)` → ТО `counter(ap, −cost)` і дія.
- КОЛИ `turn_end(daughter)` → ЯКЩО `counter(ap_spent, ≤, 50)` → ТО `custom: «наступний хід скоро»`.
- Burst: КОЛИ `input(skill, daughter)` → ЯКЩО `counter(ap, <, 50)` після дії → ТО `set_state(daughter, burst)`, `custom: «юніт падає в кінець таймлайну»`; Burst-дія дає більше шкоди/руху (?).
- КОЛИ `input(delayed_skill, a, area)` → ТО `custom: «дія ставиться на таймлайн на +N і виконається, коли черга дійде до неї»`.
- КОЛИ `custom: «ворог ставить відкладену атаку»` → ТО `custom: «її позначка й зона видно на полі і таймлайні»`; ЯКЩО `custom: «Донька встигла вбити або затримати ворога раніше»` → ТО `custom: «атака скасована / зсунута»`.
- Переривання: КОЛИ `custom: «на таймлайні є interrupt-дія Доньки раніше за ворожий постріл»` → ТО `custom: «вона спрацьовує першою»` — бий того, хто цілиться.
- Затримка: КОЛИ `input(delay_skill, shieldbearer, enemy)` → ТО `custom: «ворог зсувається далі по таймлайну»`.
- Реакція: КОЛИ `custom: «ворог атакує / ворогу завдано шкоди поруч»` → ЯКЩО `state(daughter, reaction_ready)` → ТО `custom: «реакція Доньки спрацьовує без AP»`, `damage(daughter, cost_hp)`.
- КОЛИ `input(chain, a, b)` → ТО `custom: «вміння, що підсилюють одне одне (позначка → удар), дають ланцюгову реакцію»`.
- КОЛИ `custom: «таймлайн дійшов до пастки / зони виключення»` → ТО `damage(units_in_area, n)`.
- Лікування: КОЛИ `input(sacrifice, a, b)` → ЯКЩО `custom: «b того ж або вищого рівня»` (?) → ТО `disappear_b`, `heal(a, full)`, `give(a, trait)`.
- КОЛИ `hp_zero(daughter)` → ТО `disappear_a` — permadeath; відродити можна лише особливим ресурсом (?).
- КОЛИ `all_gone(enemy)` або `custom: «мета місії виконана»` → ТО `win` (місія); виживші набирають досвід і риси.
- КОЛИ `all_gone(daughter)` (загін знищено) → ТО `custom: «кінець спроби; повернення з частиною сил»`, `custom: «відкриваються Remembrances за виконані умови»`.
- Перемога: перемогти фінального боса · Поразка: втрата загону (не остаточна — новий забіг) · Рахунок: —.

## Керування і ввід
- Мишею/геймпадом: вибрати Доньку на її ході → клітина руху (з показом витрати AP) → вміння зі смуги → ціль.
- Перед підтвердженням — превʼю: скільки AP лишиться і куди юніт стане на таймлайні після дії.
- Наведення на ворога або на позначку таймлайну — коли й куди він ударить.
- Між місіями — вибір місії, найм/жертва, екіпірування Memories.

## Вікна, меню, HUD
- `main-menu`: Нова гра · Продовжити · Налаштування · Вихід.
- `custom-window` «Inner Dream» — хаб між боями: загін, найм нових Доньок, жертва для лікування, Memories (?).
- `map-window` — вибір місії/дня (?).
- `custom-window` «Remembrances» — вибір відкритих бонусів перед новою спробою.
- `codex-window` — кодекс з умовами відкриття Remembrances і описами ворогів.
- `game-screen`: поле; `turn-indicator` у вигляді **таймлайну** (портрети юнітів, позначки відкладених дій і пасток); `action-points`; `hp-bar`; `skill-bar`; `threat-range` і `telegraph-marker` для відкладених атак; `path-preview`.
- `end-screen` — підсумок місії; `settings-window`; `pause-menu`.
- Переходи: main-menu → Inner Dream → місія → end-screen → Inner Dream / (поразка) Remembrances → нова спроба.

## Фічі поза полем
- `meta-progression`: Remembrances між спробами; частина прогресу й Доньок переноситься «за ціну».
- `xp-level` і риси Доньок: стиль бою формує характер і вміння; жертва дає риси вцілілій.
- `mode-hardcore`-подібна природа: смерть остаточна, але кампанія не обнуляється.
- `autosave` (?); `difficulty-presets` (?).

## Варіації й родичі
- Таймлайн ініціативи: [xcom-chimera-squad](xcom-chimera-squad.md) (interleaved timeline, вміння зсуву), [final-fantasy-tactics](final-fantasy-tactics.md) (CT-шкала, швидкість), [triangle-strategy](triangle-strategy.md), [disgaea](disgaea.md); Grandia (ATB з перериванням).
- Ціна дії в часі: [into-the-breach](into-the-breach.md) — наміри ворогів наперед, але фіксовані фази; [banner-saga](banner-saga.md) — чергування.
- **Осі варіацій**: черга — фази сторін / чергування юнітів / таймлайн зі швидкістю / таймлайн з ціною дії · відкладені дії — нема / лише вороги / обидві сторони · лікування — вільне / ресурс / лише жертвою.

## Цікавинки для курсу
- Таймлайн як пріоритетна черга: позиція = ініціатива, вставка/зсув подій — 🥉 (heap і стабільні рівності).
- Поріг 50 AP: «дешевий хід — скоро знову», «дорогий — у кінець» — 📎.
- Відкладені дії на таймлайні + переривання (хто раніше, той скасовує) — 🥈.
- Затримка ворога вміннями як окремий ресурс бою — 📎.
- Лікування лише жертвою з передачею риси — 🌱.
- Мета-прогрес «Remembrances за виконані умови» між спробами — 📎.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` (Blademaster / Soulslinger) · `permadeath` · `unit-xp-skills` · `status-effects` · `telegraphed-intents` (відкладені атаки на таймлайні) · `reachable-highlight` · `path-preview` · `threat-range` · `destroy-all-enemies` · `ai-opponent` · `mode-indicator` · `codex-window` · `character-select`.
- **Нема** → пропозиції карток:
  - `+initiative-timeline` «Таймлайн ініціативи» · game-logic/turns · 🥉 · слоти {шкала, швидкість}.
  - `+ap-overspend-delay` «Ціна дії відсуває наступний хід» · game-logic/turns · 📎 · слот {поріг: 50}.
  - `+delayed-action` «Відкладена дія на таймлайні» · entities/combat · 🥈.
  - `+interrupt-reaction` «Реакція/переривання поза своїм ходом» · entities/combat · 🥉 — спільна з D&D opportunity attack.
  - `+turn-order-manipulation` — спільна з Chimera Squad.
  - `+sacrifice-heal` «Лікування жертвою союзника» · entities/state · 🌱.
  - `+run-meta-unlocks` «Відкриття між спробами за умовами» · progression · 📎.

## Пропозиції до словників
- `+trigger:timeline_turn` — таймлайн дійшов до юніта/події (вже пропонував Chimera Squad).
- `+trigger:interrupt` — подія поза ходом, що спрацьовує перед чужою дією.
- `+effect:delay_turn` / `+effect:advance_turn` — зсунути позицію на таймлайні.
- `+effect:queue_action` — поставити дію на таймлайн на пізніше.
- `+effect:sacrifice` — прибрати свого юніта ціною ефекту для іншого.
- `+cond:ap` — лишок очок дії порівняно з порогом (частковий `counter`).
- `+ui:timeline-bar` — шкала черги з портретами й позначками подій.
- `+ui:action-points-preview` — скільки AP лишиться і куди стане юніт після дії.
- `+window:inner-dream` — хаб між боями; `+window:remembrance-select` — вибір мета-бонусів.
- `+feature:run-carryover` — частина загону переноситься в нову спробу.
- `+axis:turn-structure=time-track` — значення осі з корпусу (FFT, Chimera Squad).

## Джерела
- ⭐ [Wikipedia: Othercide](https://en.wikipedia.org/wiki/Othercide) — таймлайн, AP і виснаження, класи, лікування жертвою, Remembrances, дати виходу.
- [Steam](https://store.steampowered.com/app/798490/) — опис Dynamic Timeline System, контр-дій, жертви, permadeath, босів.
- [PlayStation Blog: поради](https://blog.playstation.com/?p=333710) — поріг 50 AP, Burst, реакції Soulslinger, затримки Shieldbearer, пастки й зони на таймлайні, Memories.
- YouTube: пошук «Othercide gameplay».

## Непевне
- (?) Burst: точна ціна (за пошуковим зведенням — «на 1 AP нижче 50» кидає в кінець таймлайну) і чи дає бонус шкоди/руху — описано лише в гайдах.
- (?) Реакції коштують HP замість AP — з пошукового зведення гайдів Prima/PC Invasion, сторінки не відкрились (403).
- (?) Максимум AP = 100 на Доньку, швидкість/ініціатива як стат — з памʼяті.
- (?) Умова жертви (рівень жертви ≥ рівня лікованої), ресурс для воскресіння — з памʼяті.
- (?) Структура кампанії: ери, дні, бос наприкінці ери, хаб Inner Dream, валюта Vitae — з памʼяті.
- (?) Пізніші класи (Scythemaster тощо) — з памʼяті; у джерелах лише три.
- (?) Чи є шанс влучання (за відчуттям — атаки детерміновані), тому `random: setup`.
