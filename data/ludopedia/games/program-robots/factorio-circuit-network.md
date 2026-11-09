---
title: Factorio — circuit network
slug: factorio-circuit-network
aka: [Circuit network, Factorio combinators, Комбінатори Factorio]
family: program-robots
also: [build-sim]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: none
year: 2016
platforms: [PC, Mac, Linux, Switch]
links:
  - {kind: wiki, url: "https://wiki.factorio.com/Circuit_network", best: true, note: "сигнали-канали, int32 з переповненням, червоні/зелені дроти, сумування, комбінатори, Each/Everything/Anything, режими читання всіх будівель, зміни 2.0"}
  - {kind: other, url: "https://wiki.factorio.com/Tutorial:Circuit_network_cookbook", note: "книга рецептів: тригери, лічильники, памʼять, ламп-дисплеї (не відкрито)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=factorio+circuit+network+tutorial", note: "пошук; туторіали"}
stage: v1
coverage: 55
mechanics: [cell-click, drag-drop-piece, sensor-predicates, fsm-program, button-toggle, game-pause, in-game-editor, gui-render, +signal-channels, +signal-vector-bus, +two-color-wires, +signal-sum-on-wire, +combinator-ops, +quantifier-signals, +read-mode-entity, +enable-condition, +feedback-loop-memory, +pulse-vs-hold, +int-overflow-wrap, +logic-gates]
proposes: ["+trigger:signal(net)", "+cond:signal(net, ch, op, n)", "+effect:emit(net, ch, n)", "+effect:enable(entity)", "+role:wire", "+role:combinator", "+window:entity-circuit-panel", "+ui:signal-picker", "+ui:wire-overlay", "+card:signal-vector-bus", "+card:quantifier-signals"]
author: opus
date: 2026-11-09
---

# Factorio, мережа сигналів — дроти двох кольорів несуть вектор цілих по всіх каналах, комбінатори рахують над ним, будівлі вмикаються за умовою

## Суть
Логічний шар поверх заводу ([factorio-belts](../build-sim/factorio-belts.md) описує сам завод): гравець тягне червоні й зелені дроти між будівлями й комбінаторами. Кожна мережа — вектор цілих: по одному каналу на кожен предмет, рідину й віртуальний сигнал; кілька відправників на одному каналі сумуються. Комбінатори роблять арифметику й порівняння над вектором, а скрині, конвеєри, маніпулятори, потяги, лампи читають мережу або вмикаються за умовою. З цього будують лічильники, памʼять, таймери, керування потягами й навіть дисплеї та процесори.

## Поле і час
- Поле — клітинна мапа Factorio; комбінатори й стовпи займають клітини, дроти — лінії між точками підключення (не клітини), обмежені досяжністю стовпа (?).
- Два незалежні шари мереж: червоний і зелений; на одному стовпі вони не змішуються.
- Час — реальний, 60 тіків/с; значення в мережі — на кожен тік (?); затримка комбінатора на 1 тік у вікі прямо не названа (?).
- Значення — знакові 32-бітні; переповнення загортається (2147483647 + 10 → −2147483639).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Червоний / зелений дріт | conduit | колір | зʼєднує точки; дроти одного кольору, що торкаються, — одна мережа |
| Мережа | zone | вектор каналів | кожен канал = сума всіх відправників; невжиті канали = 0 |
| Сигнал-канал | mark | предмет / рідина / віртуальний (цифри, літери, кольори) | ціле int32 |
| Constant combinator | source | слоти канал → значення | постійно видає задані значення; два слоти одного каналу сумуються |
| Arithmetic combinator | conduit | вхід (червоний, зелений або обидва) → вихід | + − × ÷ mod ^ << >> AND OR XOR; вихід — окрема мережа від входу |
| Decider combinator | conduit | умови (з 2.0 — кілька), виходи | видає сигнал (значення входу або 1), якщо умова істинна |
| Selector combinator (2.0) | conduit | режим | max/min сигнал, розмір стека, кількість входів, випадковий вхід раз на N тіків |
| Each / Everything / Anything | mark | віртуальні | «для кожного» / «для всіх» (істинно на порожньому) / «існує» (хибно на порожньому) |
| Скриня | source | Read contents | видає вміст; empty slots — на сигнал E |
| Конвеєр | source / sink | pulse / hold / hold all belts; enable | читає предмети; вимикається умовою |
| Маніпулятор | source / sink | pulse / hold; enable; filter; stack size | читає взяте, вмикається за умовою, фільтр із сигналу |
| Збиральна машина | source / sink | вміст, інгредієнти, імпульс завершення, working | рецепт задається сигналом |
| Залізнична зупинка / семафор | source / sink | train ID T, en-route C, limit L, priority P; стан семафора | керування потягами з мережі |
| Лампа | sink | колір з сигналу (кольоровий, RGB, packed) | світить, якщо умова істинна |
| Programmable speaker | sink | нота / звук / алерт | грає за сигналом |
| Display panel (2.0) | sink | текст | показує мітку за умовою |
| Power switch | switch | умова | зʼєднує дві електромережі |
| Radar (2.0) | conduit | surface / universe | передає сигнали на інші радари |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `custom: «кожен канал мережі = сума значень усіх відправників цього кольору»`.
- КОЛИ `tick` → ЯКЩО `custom: «приймач підключений до обох кольорів»` → ТО `custom: «бачить суму червоної й зеленої мереж»`.
- КОЛИ `tick` → ТО `custom: «arithmetic: out[ch] = in[a] op in[b]»`; ЯКЩО `custom: «вхід — Each»` → ТО `custom: «операція над кожним ненульовим каналом окремо; вихід — Each або сума»`.
- КОЛИ `tick` → ЯКЩО `custom: «умова decider істинна»` → ТО `custom: «видати канал зі значенням входу або 1»`.
- КОЛИ `tick` → ЯКЩО `custom: «Everything op N»` → ТО `custom: «істинно, якщо всі канали задовольняють; порожня мережа — істинно»`.
- КОЛИ `tick` → ЯКЩО `custom: «Anything op N»` → ТО `custom: «істинно, якщо хоч один канал; порожня — хибно»`.
- КОЛИ `custom: «значення > 2^31−1»` → ТО `custom: «загортається в мінімум (int32)»`.
- КОЛИ `tick` → ЯКЩО `custom: «вихід комбінатора заведено на його вхід»` → ТО `custom: «значення наростає щотік — лічильник/памʼять»`.
- КОЛИ `tick` → ЯКЩО `custom: «умова будівлі (enable) хибна»` → ТО `set_state(entity, disabled)`; circuit- і logistic-умови — через AND.
- КОЛИ `picked(inserter, item)` → ЯКЩО `mode(pulse)` → ТО `custom: «імпульс на 1 тік у мережу»`; `mode(hold)` — поки несе.
- КОЛИ `custom: «машина завершила крафт»` → ТО `custom: «імпульс 1 тік = кількість крафтів»`.
- КОЛИ `custom: «сигнал рецепту в мережі»` → ТО `custom: «збиральна машина перемикає рецепт; без сигналу — рецепт за замовчуванням»`.
- КОЛИ `input(wire a → b)` → ЯКЩО `custom: «такий самий дріт уже є»` → ТО `custom: «дріт знімається»`; дроти не витрачаються.
- Перемога / поразка: нема в шарі — інструмент; Рахунок: —.

## Керування і ввід
- Дріт у руці → клік по одній будівлі, потім по іншій чи основі стовпа; повторний клік тим самим кольором знімає; Shift-клік по стовпу знімає спершу електродроти, потім сигнальні.
- Клік по будівлі → її вікно: режими читання, умова enable, слоти constant combinator, вибір операції.
- Вибір каналу — сітка іконок предметів і віртуальних сигналів.
- Комбінатори можна копіювати blueprint-ами разом із налаштуваннями (?); з 2.0 — редагований опис комбінатора.

## Вікна, меню, HUD
- `game-screen`: мапа з дротами (червоні/зелені лінії) і стовпами.
- `entity-circuit-panel` (custom): вікно будівлі — поточні сигнали на вході/виході, режим, умова `ліве op праве`, кольори входу.
- `signal-picker` (custom-ui): сітка каналів-іконок із вкладками.
- `wire-overlay` (custom-ui): при наведенні — значення сигналів у точці підключення (?).
- Переходи: мапа → клік по будівлі → вікно налаштувань.

## Фічі поза полем
- Blueprint-и й бібліотека креслень зі схемами логіки (?); `mod-support` (моди-комбінатори).
- Зміни 2.0: selector combinator, display panel, кілька умов у decider, радари передають сигнали між планетами, турелі й печі в мережі.

## Варіації й родичі
- [minecraft-redstone](../build-sim/minecraft-redstone.md) — один біт / сила 0–15 замість вектора; [mindustry-logic](mindustry-logic.md) — асемблер замість схем; [turing-complete](turing-complete.md) — вентилі як гра; [kohctpyktop](kohctpyktop.md).
- Сусіди: Oxygen Not Included (автоматика 1 біт), Shapez (сигнали в 2-й частині) (?).
- **Осі варіацій:** ширина сигналу (біт / ціле / вектор каналів) · обчислення (вентилі / комбінатори-операції / процесор з кодом) · звʼязок (дріт / бездротово через радар) · такт (подія / тік).

## Цікавинки для курсу
- Вектор-сигнал: словник `канал → int`, сумування відправників, два кольори — 📎.
- Arithmetic/decider як чисті функції над словником з Each/Everything/Anything — 🥉 (семантика порожньої мережі — пастка).
- Симуляція графа комбінаторів по тіках із затримкою і зворотним звʼязком (памʼять, лічильник) — 🥈.
- int32 з загортанням у Python (`(x + 2**31) % 2**32 − 2**31`) — 🌱.
- Будівля з режимами pulse/hold і enable-умовою — 📎.
- Візуалізація мережі: дроти двох кольорів над клітинною мапою — 🥉.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` (дроти) · `sensor-predicates` (умови enable) · `fsm-program` (памʼять з фідбеку) · `button-toggle` (power switch) · `game-pause` · `in-game-editor` · `gui-render`.
- **Нема** → пропозиції карток:
  - `+signal-vector-bus` «Сигнал — вектор цілих по каналах, відправники сумуються» · game-logic/program · 🥉.
  - `+two-color-wires` «Два незалежні шари мереж на тих самих вузлах» · entities · 📎.
  - `+signal-sum-on-wire` · 🌱; `+combinator-ops` «Комбінатор: операція вхід→вихід» · 📎; `+quantifier-signals` «Each/Everything/Anything» · 🥉.
  - `+read-mode-entity` «Будівля читає свій вміст у мережу (pulse/hold)» · 📎; `+enable-condition` «Будівля працює, поки умова істинна» · 🌱.
  - `+feedback-loop-memory` · 🥈; `+pulse-vs-hold` · 🌱; `+int-overflow-wrap` · 🌱.
  - `+signal-channels` (як у Levelhead) і `+logic-gates` (як у редстоуні) — підтвердження.

## Пропозиції до словників
- `+trigger:signal(net)` — у мережі змінився сигнал (уже просили в Kohctpyktop — підтвердження).
- `+cond:signal(net, ch, op, n)` — умова над каналом мережі (`iron > 100`).
- `+effect:emit(net, ch, n)` — видати значення в канал.
- `+effect:enable(entity)` — увімкнути/вимкнути будівлю за умовою (ширше за `set_state`).
- `+role:wire` (підтвердження), `+role:combinator`.
- `+window:entity-circuit-panel`, `+ui:signal-picker`, `+ui:wire-overlay`.
- `+card:signal-vector-bus`, `+card:quantifier-signals`.

## Джерела
- ⭐ [Factorio Wiki: Circuit network](https://wiki.factorio.com/Circuit_network) — сигнали, int32 з переповненням, сумування, червоні/зелені мережі, повний список будівель із режимами, комбінатори й операції, Each/Everything/Anything, зміни 2.0.
- [Factorio Wiki: Circuit network cookbook](https://wiki.factorio.com/Tutorial:Circuit_network_cookbook) — з черги, не відкрито.
- YouTube: пошук «factorio circuit network tutorial».

## Непевне
- (?) Затримка 1 тік на комбінатор — загальновідомо, але на відкритій сторінці не сказано.
- (?) Кількість віртуальних сигналів: сторінка суперечить сама собі (48 / 177 / 241 зі Space Age).
- (?) Довжина дроту / досяжність стовпа, підказка зі значеннями при наведенні, blueprint-и з логікою — з памʼяті.
- (?) Рік: мережа сигналів зʼявилась у ранньому доступі (0.10–0.13, 2014–2016) — рік 2016 умовний (вихід раннього доступу в Steam).
