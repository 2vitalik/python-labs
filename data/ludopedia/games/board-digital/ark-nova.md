---
title: Ark Nova
slug: ark-nova
aka: [Arche Nova]
family: board-digital
also: []
klass: cursor
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: score
year: 2021
platforms: [board, PC]
links:
  - {kind: other, url: "https://rulespal.com/ark-nova/rulebook", best: true, note: "повні правила: мапа зоопарку, Build I/II, кіоски, вольєри, перерва, підрахунок"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ark_Nova_(board_game)", note: "огляд: 5 карт дій зі слотами сили, Appeal/Conservation, кінець, видання, Ark Nova Digital"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=ark+nova", note: "пошук BGG (403 для фетчу)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=ark+nova", note: "пошук; Ark Nova Digital (Dire Wolf, 2025)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ark+Nova+how+to+play", note: "пошук; правила"}
stage: v1
coverage: 55
mechanics: [polyomino-placement, impassable-cells, drag-drop-piece, hover-highlight, legal-move-highlight, event-points, round-currency, hot-seat, turn-enforcement, ai-opponent, game-screen, end-screen, help-window, +polyhex-placement, +placement-bonus-cells, +adjacent-terrain-requirement, +min-distance-rule, +adjacency-income, +cover-all-bonus, +action-strength-slots, +two-track-end-trigger, +map-choice-setup]
proposes: ["+trigger:covered", "+cond:touches", "+cond:distance", "+ui:action-card-row", "+ui:appeal-conservation-track", "+card:polyhex-placement", "+card:placement-bonus-cells", "+card:adjacent-terrain-requirement", "+card:min-distance-rule", "+card:adjacency-income", "+card:action-strength-slots"]
author: opus
date: 2026-11-09
---

# Ark Nova — будуй зоопарк на гексовій мапі: вольєри 1–5 клітин, вода й скелі поруч, кіоски на відстані

## Суть
Карткова гра-рушій (engine builder) про сучасний зоопарк, де **сітковий шар** — особиста мапа зоопарку. Гравець ставить на неї будівлі-поліформи (стандартні вольєри розміром 1–5, спецвольєри, кіоски, павільйони, унікальні будівлі спонсорів), а потім заселяє вольєри тваринами з карт, які вимагають мінімального розміру й сусідства з водою/скелями. Тут описано лише мапу; карти, асоціація й збереження видів — коротко.

## Поле і час
- Особиста мапа зоопарку з клітин-«spaces»; на мапі — клітини скель (R) і води (W), клітини з бонусом розміщення, клітини з іконкою BUILD II (будувати лише після апгрейду карти Build). Форма клітин — гекси (?).
- Варіанти мап: Map A (однакова для всіх, стартовий вольєр розміру 3 на позначених клітинах), Map 0 (для новачків), Maps 1–8 (просунуті, кожна з власною здібністю).
- Покроково за годинниковою стрілкою; хід = одна дія (одна з 5 карт дій або X-токен). Періодично — **Перерва** (Break): ліміт руки, дохід від привабливості й кіосків, оновлення ринку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Будівельна клітина | terrain | може мати бонус / BUILD II | на неї можна ставити будівлі |
| Скеля (R) | static | — | не забудовується; сусідство потрібне деяким тваринам |
| Вода (W) | static | — | не забудовується; сусідство потрібне деяким тваринам |
| Клітина бонусу | terrain | жовтий пʼятикутник з іконкою | накрив → одразу береш бонус |
| Стандартний вольєр | tile | розмір 1–5 (28/24/15/13/10 шт.) | порожній бік угору; тварина → перевертається на «зайнятий» |
| Дитячий зоопарк | tile | розмір 3, один на зоопарк | лише тварини дитячого зоопарку |
| Дім рептилій / Великий вольєр птахів | tile | розмір 5, по одному; лише Build II | рептилії / птахи; можна раз перенести наявних |
| Кіоск | tile | розмір 1 | ≥ 3 клітини до іншого кіоску; дохід за сусідні будівлі |
| Павільйон | tile | розмір 1 | +1 привабливість при будівництві |
| Унікальна будівля | tile | з карти спонсора (15 шт.) | деякі — лише біля води/скель |
| Карта тварини | supply | мін. розмір вольєра (у гексагоні), вимоги води/скель | заселяє порожній вольєр |
| Карти дій ×5 | supply | слот 1–5 = сила X | використана → у слот 1, інші зсуваються |
| X-токен | resource | ≤ 5 | +1 до сили дії |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(build, building, cells)` → ЯКЩО `fits(building, cells)` and `custom: «клітини порожні, не вода/скеля, не за краєм мапи»` → ТО `place(player, building)`, `currency(-2 × розмір)`.
- Сусідство: ЯКЩО це не перша будівля → вимога `custom: «хоча б одне ребро спільне з наявною будівлею»` (`+cond:touches`); перша — `custom: «хоча б одна клітина на межі мапи»`.
- КОЛИ `custom: «будівля накрила клітину з бонусом»` (`+trigger:covered`) → ТО `custom: «одразу взяти бонус»` (до наступної будівлі тієї ж дії).
- ЯКЩО `cell(cells, build_ii)` and `not state(build_card, upgraded)` → ТО `block`.
- Кіоск: ЯКЩО `custom: «інший кіоск ближче ніж за 3 клітини»` (`+cond:distance`) → ТО `block`.
- Build I: одна будівля розміру ≤ X. Build II: кілька **різних** будівель сумарного розміру ≤ X; відкриває Дім рептилій і Великий вольєр птахів.
- КОЛИ `after(place)` → ЯКЩО `cover_all(building)` (крім води й скель) → ТО `counter(appeal, +7)`.
- КОЛИ `input(animals, card)` → ЯКЩО `state(enclosure, empty)` and `custom: «розмір ≥ вимоги карти»` and `adjacent_count(enclosure, water|rock, >=, n)` → ТО `set_state(enclosure, occupied)` (перевернути); бонуси тварини.
- КОЛИ `custom: «збудовано Дім рептилій / Великий вольєр птахів»` → ТО `custom: «можна раз перенести придатних тварин»`, їхні вольєри → `set_state(enclosure, empty)`.
- КОЛИ `phase_start(break)` → ТО `currency(+дохід за привабливістю)`; для кожного кіоску `currency(+1)` за кожну сусідню (спільне ребро) унікальну будівлю, спецвольєр, **зайнятий** стандартний вольєр, павільйон; порожній стандартний — 0.
- КОЛИ `input(action_card)` → ТО `custom: «сила = номер слота; карта → слот 1, лівіші зсуваються вправо»`.
- КОЛИ `custom: «маркери Appeal і Conservation в одній зоні або розминулись»` → ТО `custom: «останній хід іншим (або всім, якщо в Перерву)»`, `game_over`.
- Рахунок: Appeal − цільове число зони Conservation; більше → `win`; нічия — за кількістю підтриманих природоохоронних проєктів.

## Керування і ввід
- (цифрова версія) Обрати карту дії → обрати будівлю з запасу → перетягнути на мапу з поворотом (?), `legal-move-highlight` допустимих клітин; заселення — обрати карту тварини і вольєр.

## Вікна, меню, HUD
- (цифрова версія)
- `game-screen`: мапа зоопарку, ряд 5 карт дій (`action-card-row`), рука, ринок карт, треки Appeal/Conservation/Reputation (`appeal-conservation-track`), гроші, X-токени, трек Перерви.
- `match-setup`: кількість гравців, вибір мапи (Map A / 0 / 1–8: дві випадкові, обрати одну).
- `end-screen`: фінальні карти підрахунку, очки, переможець. `help-window` — довідка іконок.

## Фічі поза полем
- Мапи 1–8 зі здібностями (`+map-choice-setup`), соло-режим (окремий розділ правил), доповнення Marine Worlds, Zoo Map Pack 1/2.
- Ark Nova Digital (Dire Wolf, 2025, кросплатформна): `online-multiplayer`, `ai-opponent-levels` (?).

## Варіації й родичі
- Поліоміно на особистій мапі з бонусами клітин: [Bärenpark](barenpark.md), [A Feast for Odin](a-feast-for-odin-polyomino.md), [The Isle of Cats](the-isle-of-cats.md), [Cartographers](cartographers.md).
- Сусідство з місцевістю як умова: [Kingdom Builder](kingdom-builder.md), [Cascadia](cascadia-calico.md).
- **Осі варіацій**: форма клітин (квадрат / гекс) · обмеження розміщення (сусідство з будівлею / з місцевістю / відстань між однаковими) · бонус за накриту клітину (одноразовий / дохід) · вміст будівлі (порожня / зайнята змінює дохід сусідів).

## Цікавинки для курсу
- Розміщення поліформи на гекс-сітці з перевіркою «не вода/скеля, не за краєм, спільне ребро» — 🥉.
- Мінімальна відстань між кіосками (BFS-відстань на гексах) — 📎.
- Вимога тварини «≥ N сусідніх клітин води/скель» — 📎.
- Дохід кіоску = сусідні будівлі за типом і станом (порожній/зайнятий) — 📎.
- Карти дій як черга сили: використана → у слот 1 — 🌱 (проста, але елегантна механіка).
- Повна перевірка «чи вміщується вольєр десь на мапі» для підсвітки — 🥉.

## Мапа на каталог
- Є: `polyomino-placement` (тут поліформи на гексах) · `impassable-cells` ↔ вода/скелі · `drag-drop-piece`, `hover-highlight`, `legal-move-highlight` · `event-points`, `round-currency` · `hot-seat`, `turn-enforcement`, `ai-opponent` · `game-screen`, `end-screen`, `help-window`.
- **Нема** → пропозиції карток:
  - `+polyhex-placement` «Поліформа на гекс-сітці» · entities/legality · 🥉 — дитина `polyomino-placement`.
  - `+placement-bonus-cells` «Бонус за накриту клітину» · entities/interact · 🌱 (також Bärenpark, Feast for Odin).
  - `+adjacent-terrain-requirement` «Розміщення лише біля місцевості виду» · entities/legality · 📎 · слоти {terrain, n}.
  - `+min-distance-rule` «Мінімальна відстань між однаковими» · entities/legality · 📎 · слоти {kind, n}.
  - `+adjacency-income` «Дохід за сусідів за типом/станом» · game-logic/economy · 📎.
  - `+cover-all-bonus` «Бонус за повне заповнення мапи» · game-logic/score · 🌱.
  - `+action-strength-slots` «Карти дій зі слотами сили» · game-logic/opponent · 🥉.
  - `+two-track-end-trigger` «Кінець, коли зустрілися два треки» · game-logic/win · 🌱.
  - `+map-choice-setup` «Вибір особистої мапи з кількох» · levels/bank · 🌱.

## Пропозиції до словників
- `+trigger:covered` — будівля накрила клітину з іконкою (також Bärenpark).
- `+cond:touches(a, b|border)` — фігура має спільне ребро з іншою / з межею поля.
- `+cond:distance(a, kind, op, n)` — відстань до найближчої сутності виду.
- `+ui:action-card-row` — ряд карт дій зі слотами сили; `+ui:appeal-conservation-track` — два зустрічні треки.
- `+card:…` — 6 карток вище.

## Джерела
- ⭐ [RulesPal: Ark Nova rulebook](https://rulespal.com/ark-nova/rulebook) — розміри й кількості вольєрів, спецвольєри, кіоски (≥ 3 клітини), павільйон +1, 2 гроші за клітину, сусідство ребром, межа для першої будівлі, бонуси розміщення, +7 за повне покриття, Build I/II, дохід кіосків, мапи A/0/1–8, кінець і підрахунок.
- [Wikipedia: Ark Nova](https://en.wikipedia.org/wiki/Ark_Nova_(board_game)) — 5 карт дій і слоти, Перерва, кінець, Wigge / Feuerland 2021 / Capstone 2022, Ark Nova Digital 2025.
- BGG, Steam, YouTube — лише пошукові URL.

## Непевне
- (?) Форма клітин: правила кажуть «spaces», слово «hexagon» — лише про розмір на карті тварини; гекси — з черги й памʼяті.
- (?) Чи можна повертати / віддзеркалювати будівлі (у правилах не знайдено).
- (?) Повний список іконок бонусів розміщення (у RulesPal — посилання на окремий огляд іконок).
- (?) Вікна й функції Ark Nova Digital (онлайн, AI, платформи) — не відкривав.
- Веб-пошук сесії вичерпано; UltraBoardGames за прямим URL віддав головну.
