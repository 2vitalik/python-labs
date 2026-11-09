---
title: Sugarscape (Цукрова земля)
slug: sugarscape
aka: ["Sugarscape model", "Growing Artificial Societies", "Цукрова земля", "Цукроландшафт", "Epstein–Axtell model"]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: both
  goal: none
year: 1996
platforms: [web, PC]
links:
  - {kind: other, url: "https://ccl.northwestern.edu/netlogo/models/Sugarscape3WealthDistribution", best: true, note: "NetLogo: правила M, G, R з віком, інтерфейс, крива Лоренца й Джині"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Sugarscape", note: "огляд, 51×51 в оригіналі, список дій агентів, реалізації (Ascape, NetLogo, MASON, GPU)"}
  - {kind: other, url: "https://jasss.soc.surrey.ac.uk/12/1/6/appendixB/EpsteinAxtell1996.html", note: "JASSS: модель розділу 2 — тор 50×50, два піки, таблиця параметрів, порядок G → M → R"}
  - {kind: other, url: "https://arxiv.org/pdf/1505.06012", note: "Kehoe, The Specification of Sugarscape: усі правила книги дослівно + Z-специфікація, SU vs AU"}
  - {kind: other, url: "https://ccl.northwestern.edu/netlogo/models/Sugarscape1ImmediateGrowback", note: "NetLogo: миттєве відростання, графіки зору й метаболізму"}
  - {kind: other, url: "https://juliadynamics.github.io/AgentsExampleZoo.jl/dev/examples/sugarscape", note: "Agents.jl: код моделі розділу 2, теплокарта й гістограма багатства"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sugarscape+simulation", note: "пошук; симуляції"}
stage: v1
coverage: 60
mechanics: [game-loop, game-pause, state-as-data, game-settings, rule-variants, wrap-edges, spawn-random-cell, respawn, hunger-clock, level-from-txt, gui-render, logic-render-split, unit-tests, property-tests, +agent-needs, +agent-vision-harvest, +resource-regrowth, +random-agent-order, +agent-reproduction, +culture-tags, +bit-string-immunity, +bilateral-trade, +pollution-diffusion, +gini-lorenz, +metric-histograms, +color-by-attribute, +step-run-speed]
proposes: ["+cond:attr", "+effect:add_value", "+effect:move_to_best", "+effect:breed", "+effect:diffuse", "+effect:barter", "+ui:color-by", "+ui:stats-plot", "+ui:param-slider", "+card:agent-vision-harvest", "+card:resource-regrowth", "+card:gini-lorenz", "+card:culture-tags"]
author: opus
date: 2026-11-09
---

# Sugarscape — агенти із зором і метаболізмом збирають цукор, що відростає; з кількох правил виростає нерівність, племена, торгівля

## Суть
Агентна соціальна симуляція Джошуа Епштейна й Роберта Екстелла (книга «Growing Artificial Societies», Brookings, 1996): тор із «цукровим» рельєфом — два піки й пустеля — і кілька сотень агентів. Кожен бачить на v клітин у 4 напрямках, іде в найближчу вільну клітину з найбільшим цукром, збирає його й спалює m одиниць щотіку; без цукру гине. Правила підключаються модулями: відростання, сезони, забруднення, розмноження, спадок, культура, бій, кредит, хвороби, другий ресурс (спеція) і торгівля. Гравець обирає набір правил і параметри, запускає й дивиться, як з'являються розподіл багатства, міграції й «суспільство».

## Поле і час
- Тор 50×50 (JASSS, NetLogo, Agents.jl; Wikipedia каже про 51×51 в оригіналі); одна клітина — один агент.
- Шар клітини: рівень цукру ≤ місткість c ∈ 0..4; у NetLogo рельєф читається з `sugar-map.txt` (50×50 значень, два піки c = 4 по 112 клітин — північний схід і південний захід).
- Додаткові шари: забруднення, спеція (другий ресурс), сезон (верхня / нижня половина).
- Зір — лише 4 напрямки (не по діагоналі): NetLogo будує список точок `(0,n) (n,0) (0,−n) (−n,0)` для n = 1..v.
- Тік: спершу правило середовища G, потім агенти виконують M у випадковому порядку, потім R (JASSS).
- Оновлення синхронне (SU, як у книзі) або асинхронне (AU, як у більшості тулкітів); Kehoe показує, що результати можуть різнитись.
- Агент бачить лише в межах свого зору; людина бачить усе поле.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Агент | neutral | зір v U[1,6], метаболізм m U[1,4], багатство w0 U[5,25], вік, макс. вік U[60,100] | шукає найкращу видиму клітину, збирає, спалює m; гине без цукру або від старості |
| Клітина цукру | resource | рівень, місткість c 0..4 | відростає на α за тік до c; після збору — 0 |
| Пік | zone | c = 4 | два піки, розділені долиною |
| Пустеля | terrain | c = 0 | цукру нема ніколи |
| Спеція | resource | рівень, місткість; у агента — запас і метаболізм спеції | другий ресурс для торгівлі; добробут залежить від обох |
| Забруднення | terrain | рівень на клітині | росте від збору й споживання; дифундує; знижує привабливість |
| Сезонна половина | zone | summer / winter | у зимі відростання повільніше; половини міняються кожні γ тіків |
| Агент (модулі S, K, E, T) | neutral | стать; фертильність: жінки 12–15 → 40–50, чоловіки 12–15 → 50–60; культурні мітки — рядок бітів непарної довжини; імунний рядок; запас і метаболізм спеції | у віці фертильності може мати дітей; плем'я Blue, якщо в мітках більше нулів, інакше Red |
| Хвороба | object | рядок бітів | передається сусідам; лікується підгонкою імунного рядка |
| Позика | object | сума, строк d, ставка r | від кредитора до позичальника; повернення в строк |

## Правила (КОЛИ → ЯКЩО → ТО)
Базова модель (розділ 2: G, M, R):
- G_α: КОЛИ `phase_start(growback)` → ТО `custom: «цукор клітини += α, не більше місткості»` (α = 1; NetLogo Sugarscape 1 — миттєве відростання до максимуму).
- M: КОЛИ `phase_start(move)` → ЯКЩО `free(cell_in_vision)` → ТО `custom: «перейти в найближчу з видимих вільних клітин (і своєї) з максимумом цукру; при рівності — випадкову»`, `pickup(agent, sugar)`.
- Якщо своя клітина не гірша за всі видимі вільні — агент лишається (NetLogo).
- Метаболізм: КОЛИ `phase_start(move)` → ТО `take(agent, sugar)` на m одиниць (після збору).
- Смерть: КОЛИ `tick` → ЯКЩО `not has(agent, sugar)` → ТО `disappear(agent)`.
- Старість: КОЛИ `tick` → ЯКЩО `custom: «вік > макс. вік»` → ТО `disappear(agent)`.
- R: КОЛИ `died(agent)` → ЯКЩО `mode(replacement)` → ТО `spawn_at(agent, random_free)` з віком 0 і випадковими v, m, макс. віком, w0 — популяція стала.
- Порядок: G → M (агенти у випадковому порядку) → R (JASSS); NetLogo: усі клітини G, далі кожен агент послідовно рух → їжа → вік → смерть/заміна.

Середовище:
- Сезони S_αβγ: КОЛИ `level_start` → ТО `custom: «вгорі літо, внизу зима»`; КОЛИ `timer(γ)` → ТО `custom: «сезони половин міняються»`; ЯКЩО `state(half, winter)` → ТО `custom: «відростання α одиниць за β тіків»`.
- Забруднення P_αβ: КОЛИ `picked(agent, sugar)` → ТО `custom: «забруднення клітини += α·s (збір) + β·m (споживання)»`; рух тоді оцінює клітину як цукор / (1 + забруднення).
- Дифузія D_α: КОЛИ `timer(α)` → ТО `custom: «нове забруднення клітини = середнє по 4 сусідах фон Неймана (з тором)»`.

Агентні модулі:
- Розмноження S: КОЛИ `phase_start(mating)` → ЯКЩО `custom: «випадковий сусід-4 протилежної статі, обидва фертильні, хтось має вільну сусідню клітину, у кожного цукру ≥ початкового»` → ТО `custom: «народжується нащадок зі схрещеною генетикою й культурою; кожен з батьків віддає половину цукру»`; повторити для всіх сусідів.
- Спадок I: КОЛИ `died(agent)` → ЯКЩО `mode(inheritance)` → ТО `custom: «багатство порівну живим дітям»`.
- Культура K: КОЛИ `phase_start(culture)` → ТО `custom: «для кожного сусіда: випадкова позиція мітки; якщо в сусіда інший біт — він перевертає біт до мого»`.
- Плем'я: КОЛИ `after(culture)` → ЯКЩО `custom: «нулів у мітках більше, ніж одиниць»` → ТО `set_side(agent, blue)`; інакше `set_side(agent, red)`.
- Бій C_α: КОЛИ `phase_start(move)` → ЯКЩО `mode(combat)` → ТО `custom: «з видимих клітин відкинути своїх, багатших чужих і вразливі до помсти; нагорода = цукор + min(α, багатство жертви)»`, `move(agent, best_reward_cell)`, `disappear(occupant)`, `pickup(agent, reward)`.
- Кредит L_dr: КОЛИ `adjacent(lender, borrower)` → ЯКЩО `custom: «кредитор старий або має надлишок; позичальник фертильний, без грошей на дитину, з доходом»` → ТО `custom: «позика на d років під r %»`; КОЛИ `timer(d)` → ТО `custom: «повернути або віддати половину багатства й переоформити решту»`.
- Хвороби E: КОЛИ `phase_start(disease)` → ЯКЩО `custom: «хвороба не є підрядком імунного рядка»` → ТО `custom: «у найближчому за Геммінгом підрядку перший відмінний біт стає як у хвороби»`.
- Передача: КОЛИ `adjacent(agent, neighbor)` → ЯКЩО `state(agent, sick)` → ТО `custom: «сусід отримує випадкову хворобу агента»`.
- Торгівля T: КОЛИ `adjacent(agent, neighbor)` → ЯКЩО `custom: «MRS агентів різні»` → ТО `custom: «ціна p = середнє геометричне MRS; спеція тече від більшого MRS до меншого, цукор навпаки; угода — якщо обом краще й MRS не перехрещуються; повторити»`.
- MRS = (спеція · метаболізм цукру) / (метаболізм спеції · цукор).

Метрики:
- КОЛИ `tick` → ТО `custom: «перерахувати криву Лоренца й індекс Джині за багатством»` (0 — усі рівні, 1 — усе в одного).
- Перемоги, поразки, рахунку нема.

## Керування і ввід
- NetLogo: кнопки SETUP (розставити агентів, прочитати мапу цукру), GO (безперервно), GO ONCE (один тік); повзунки INITIAL-POPULATION (10–1000, типово 400), MINIMUM-SUGAR-ENDOWMENT і MAXIMUM-SUGAR-ENDOWMENT (0–200, типово 5 і 25); вибір VISUALIZATION, який можна міняти під час GO.
- Помилка вводу: SETUP при max ≤ min показує повідомлення «Oops: the maximum-sugar-endowment must be larger than the minimum-sugar-endowment» і не стартує.
- Модульність: набір правил (G або S; M, M з забрудненням або C; R або S; I, K, L, E, T) обирається перед запуском (Kehoe перелічує допустимі послідовності).

## Вікна, меню, HUD
- `game-screen` (NetLogo): світ — клітини жовті (темніше = більше цукру), агенти — червоні кружки; кнопки SETUP / GO / GO ONCE; повзунки; лічильник `ticks`.
- `color-by` (пропозиція): NO-VISUALIZATION (усі червоні), COLOR-AGENTS-BY-VISION (найдальший зір — найтемніший), COLOR-AGENTS-BY-METABOLISM (найменший метаболізм — найтемніший).
- Графіки (`stats-plot`, пропозиція): Sugarscape 1 — популяція, розподіл цукру, середній зір і середній метаболізм живих; Sugarscape 3 — гістограма багатства, крива Лоренца, Джині в часі.
- HUD: `turn-counter` (ticks), `remaining-counter` (популяція).
- Ascape: жовтий — багато цукру, білий — нема; лінії соціальних зв'язків між агентами.
- `custom-window` (NetLogo): повідомлення про хибні межі початкового багатства.

## Фічі поза полем
- `custom-rules` / перемикачі правил — суть моделі: кожен експеримент книги = свій набір модулів і констант.
- `step-mode` (GO ONCE), `pause`, `speed-control` (?).
- `export-import`: мапа цукру з текстового файла.
- Реалізації: Ascape (оригінальна Java), NetLogo (3 моделі бібліотеки + спільнотна модель Іена Вівера з усіма правилами, крім бою), MASON, Mathematica (Wolfram Demonstrations), GPU-версія (понад 2 млн агентів, понад 50 оновлень/с).

## Варіації й родичі
- **Осі варіацій:** відростання (миттєве / α за тік / сезонне) · правило руху (цукор / цукор з забрудненням / бій) · заміна чи розмноження · кількість ресурсів (цукор / цукор + спеція) · SU vs AU оновлення · оцінка клітини (цукор / добробут від двох ресурсів).
- NetLogo-моделі: Sugarscape 1 (миттєве відростання: через ~20 тіків більшість не рухається, агенти шаром уздовж меж зон), Sugarscape 2 (стале відростання), Sugarscape 3 (вік, заміна, нерівність).
- Предок: [schelling-segregation](schelling-segregation.md) (Wikipedia: стаття Шеллінга 1969 — попередник); вплив Life — [game-of-life](game-of-life.md).
- Родичі в корпусі: [simant](simant.md) (колонія агентів з потребами), [rimworld-rooms](rimworld-rooms.md), [dwarf-fortress-tiles](dwarf-fortress-tiles.md) (агенти-колоністи), `wa-tor` (хижак/жертва на торі, пачка D002).

## Цікавинки для курсу
- Базова модель G + M + R на торі 50×50 з мапою з файла — 📎 (зір по 4 напрямках, вибір найкращої клітини, випадковий порядок агентів).
- Гістограма багатства, крива Лоренца і Джині — 📎 (сортування, накопичені суми).
- Сезони й забруднення з дифузією — 🥉 (окремі шари поля, дифузія з подвійним буфером).
- Розмноження з фертильністю і спадком + культурні мітки й племена — 🥈 (родовід, кросовер, перевертання бітів).
- Бій з перевіркою помсти — 🥈 (фільтр клітин за силою сусідів цілі).
- Спеція і торгівля через MRS — 🥇 (двосторонній торг до рівноваги без перехрещення MRS).
- Синхронне оновлення з розв'язанням конфліктів (двоє в одну клітину) vs асинхронне — 🥇.

## Мапа на каталог
- Є: `game-loop` + `game-pause` · `state-as-data` · `game-settings` (повзунки) · `rule-variants` (модулі правил) · `wrap-edges` (тор) · `spawn-random-cell` (стартова розстановка) · `respawn` (заміна R) · `hunger-clock` (метаболізм) · `level-from-txt` (`sugar-map.txt`) · `gui-render` · `logic-render-split` · `unit-tests` + `property-tests` (популяція стала з R; цукор клітини ≤ місткості).
- **Нема** → пропозиції карток:
  - `+agent-vision-harvest` «Агент дивиться на v клітин, іде в найкращу вільну, збирає» · entities/move · 📎 · слоти {vision, directions, score}.
  - `+resource-regrowth` «Ресурс клітини відростає до місткості» · entities/state · 🌱 · слоти {rate, capacity, season}.
  - `+gini-lorenz` «Нерівність: крива Лоренца й індекс Джині» · interface/results · 📎.
  - `+culture-tags` «Бітові мітки культури: сусіди перевертають біт, плем'я за більшістю» · entities/state · 📎.
  - `+random-agent-order` «Агенти ходять у випадковому порядку щотіку» · code/architecture · 🌱.
  - `+agent-reproduction`, `+bit-string-immunity`, `+bilateral-trade`, `+pollution-diffusion`, `+color-by-attribute` — назви говорять самі.
  - Перевикористано: `+agent-needs` (RCT), `+metric-histograms`, `+step-run-speed`.

## Пропозиції до словників
- `+cond:attr(a, name, op, n)` — характеристика сутності (вік > макс. вік, v < vmax) — повтор з NaSch.
- `+effect:add_value(cell, prop, n, cap?)` — додати до значення з обмеженням (відростання) — повтор пропозиції корпусу.
- `+effect:move_to_best(a, cells, score)` — перейти в найкращу за оцінкою клітину з видимих (найближча при рівності).
- `+effect:breed(a, b)` — пара дає нащадка — повтор пропозиції корпусу.
- `+effect:diffuse(layer)` — значення клітини стає середнім по сусідах (забруднення).
- `+effect:barter(a, b, x, y)` — обмін ресурсами між двома сутностями за ціною.
- `+ui:color-by` — вибір атрибута для кольору агентів (NetLogo VISUALIZATION).
- `+ui:stats-plot`, `+ui:param-slider` — повтор (Lenia, BML).
- `+card:agent-vision-harvest`, `+card:resource-regrowth`, `+card:gini-lorenz`, `+card:culture-tags` — див. «Мапа на каталог».

## Джерела
- ⭐ [NetLogo: Sugarscape 3 Wealth Distribution](https://ccl.northwestern.edu/netlogo/models/Sugarscape3WealthDistribution) — правила руху, метаболізму, віку 60–100, заміни, відростання +1, повзунки, графіки Лоренца й Джині; код моделі (GitHub NetLogo/models) — зір U[1,6], метаболізм U[1,4], світ 50×50 з загортанням, повзунки 10–1000 / 0–200.
- [NetLogo: Sugarscape 1 Immediate Growback](https://ccl.northwestern.edu/netlogo/models/Sugarscape1ImmediateGrowback) — миттєве відростання, VISUALIZATION, чотири графіки, «~20 тіків — і більшість стоїть».
- [JASSS: Epstein & Axtell's Sugarscape](https://jasss.soc.surrey.ac.uk/12/1/6/appendixB/EpsteinAxtell1996.html) — модель розділу 2: тор 50×50, два піки c = 4, таблиця параметрів, N = 250, порядок G → M → R.
- [Kehoe: The Specification of Sugarscape (arXiv)](https://arxiv.org/pdf/1505.06012) — дослівні формулювання всіх правил (G, S, M, P, D, R, S, I, K, C, L, E, T), межі фертильності, MRS, допустимі послідовності правил, SU vs AU.
- [Agents.jl: Sugarscape](https://juliadynamics.github.io/AgentsExampleZoo.jl/dev/examples/sugarscape) — код розділу 2, піки (10, 40) і (40, 10), теплокарта й гістограма.
- [Wikipedia: Sugarscape](https://en.wikipedia.org/wiki/Sugarscape) — огляд, 51×51, перелік дій, реалізації, історія.
- YouTube: пошук «Sugarscape simulation».

## Непевне
- (?) Розмір поля: 50×50 (JASSS, NetLogo, Agents.jl) vs 51×51 (Wikipedia).
- (?) Точна формула добробуту для двох ресурсів (у книзі — функція типу Кобба–Дугласа з показниками m₁/m_T і m₂/m_T); у витягнутому тексті Kehoe показники не прочиталися.
- (?) Довжина культурного рядка й імунного рядка, константи α/β забруднення, CHILDAMT, ставка й строк кредиту — у Kehoe названі як константи без значень.
- (?) Як саме перевіряти «вразливість до помсти» в бою — Kehoe прямо пише, що визначення неоднозначне (від поточної чи нової позиції).
- (?) Чи є в NetLogo-інтерфейсі повзунок швидкості — стандартний для NetLogo, на сторінках моделей не згаданий.
- (?) N = 250 (JASSS) vs 400 (повзунок NetLogo, і в нотатках Isaac — суперечливо).
