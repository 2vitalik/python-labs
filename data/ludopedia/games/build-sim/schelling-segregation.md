---
title: Schelling's model of segregation (модель сегрегації Шеллінга)
slug: schelling-segregation
aka: ["Schelling model", "модель Шеллінга", "Dynamic Models of Segregation", "Parable of the Polygons", "Притча про багатокутники", "NetLogo Segregation"]
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
year: 1971
platforms: [web, PC]
links:
  - {kind: play, url: "https://ncase.me/polygons/", best: true, note: "Parable of the Polygons (Vi Hart, Nicky Case, 2014): правило 1/3, перетягування, авто-режим, повзунки упередження й різноманіття, графік сегрегації"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Schelling%27s_model_of_segregation", note: "N×N, сусідство Мура, поріг Ba, поріг сегрегації ≈ 1/3, аналогія з Ізінгом, розширення"}
  - {kind: other, url: "https://ccl.northwestern.edu/netlogo/models/Segregation", note: "NetLogo Segregation: %-SIMILAR-WANTED, DENSITY, монітори й графіки, SQUARE-X"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Schelling+segregation+model", note: "пошук; симуляції"}
stage: v1
coverage: 70
mechanics: [drag-drop-piece, game-loop, game-pause, state-as-data, game-settings, wrap-edges, spawn-random-cell, gui-render, logic-render-split, unit-tests, tutorial-window, +threshold-relocation, +random-soup, +step-run-speed, +parameter-sweep, +mood-marker]
proposes: ["+cond:neighbor_share", "+card:threshold-relocation", "+card:mood-marker", "+ui:mood-marker", "+ui:stats-plot", "+ui:param-slider"]
author: opus
date: 2026-11-09
---

# Модель Шеллінга — агент переїжджає, коли схожих сусідів менше за поріг; м'які вподобання дають жорстку сегрегацію

## Суть
Агентна модель Томаса Шеллінга («Dynamic Models of Segregation», 1971): на сітці живуть агенти двох груп і є порожні клітини. Агент задоволений, якщо частка «своїх» серед зайнятих сусідів не нижча за поріг; незадоволений переїжджає у вільну клітину. Навіть за слабкого упередження (~1/3) місто саме розділяється на однорідні квартали. Найвідоміша інтерактивна форма — «Parable of the Polygons» Ві Гарт і Ніккі Кейса (2014), де гравець перетягує незадоволені фігури руками.

## Поле і час
- Сітка N×N (Wikipedia); у NetLogo світ загортається на краях (тор); у Polygons — обмежене поле.
- Клітина: порожня або один агент; густину задає параметр DENSITY (NetLogo).
- Сусідство Мура — 8 сусідніх агентів; порожні клітини в частку не входять.
- Тік = раунд, у якому агенти перевіряють сусідство й незадоволені переїжджають; порядок у раунді Wikipedia не уточнює.
- Polygons: покрокові розділи-сцени, у кожному своє маленьке поле.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Агент групи A (трикутник / помаранчевий) | neutral | поріг Ba | задоволений, якщо частка своїх ≥ Ba; інакше переїжджає |
| Агент групи B (квадрат / синій) | neutral | поріг Ba | так само |
| Порожня клітина | terrain | — | місце для переїзду; не рахується в частці |
| Окіл | zone | 8 клітин (Мур) | база для частки своїх |
| Квартал (кластер) | zone | емерджентний | однорідна область, що виростає з переїздів |
| Незадоволений агент | neutral | стан unhappy | показаний іншою позначкою (X у NetLogo SQUARE-X, «сумна» фігура в Polygons) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `custom: «частка своїх серед зайнятих сусідів-8 < Ba»` → ТО `set_state(agent, unhappy)`; інакше `clear_state(agent, unhappy)`.
- Переїзд (Wikipedia): КОЛИ `tick` → ЯКЩО `state(agent, unhappy)` → ТО `custom: «переїзд у вільну клітину, де частка своїх ≥ Ba»`.
- Переїзд (Polygons, авто-режим): КОЛИ `tick` → ЯКЩО `state(shape, unhappy)` → ТО `teleport(shape, random_free)`.
- Переїзд (NetLogo): КОЛИ `tick` → ЯКЩО `state(agent, unhappy)` → ТО `custom: «переїзд у найближчу вільну клітину (nearby patch)»`.
- КОЛИ `edge(agent)` → ЯКЩО `mode(torus)` → ТО `wrap(agent)` (NetLogo).
- КОЛИ `counter(unhappy, ==, 0)` → ТО `custom: «симуляція зупиняється»`; Wikipedia: стан «усі задоволені» не гарантований.
- Ручний хід (Polygons): КОЛИ `input(drag, shape)` → ЯКЩО `state(shape, unhappy)` and `free(target)` → ТО `move(shape, target)`; задоволену фігуру взяти не можна — `block`.
- Попит на різноманіття (Polygons): КОЛИ `tick` → ЯКЩО `custom: «частка своїх вища за верхній поріг»` → ТО `set_state(shape, unhappy)` — фігури приймають до 90 % своїх, але хочуть трохи інших.
- КОЛИ `level_start` → ТО `spawn_at(agent, random_free)`: групи приблизно порівну (NetLogo), 50/50 (Polygons).
- Метрика: КОЛИ `tick` → ТО `counter(percent_similar, …)` — `custom: «середня частка своїх серед сусідів»`; на старті ~50 % (NetLogo).
- Поріг сегрегації: `custom: «для рівних груп при Ba ≥ Bseg ≈ 1/3 конфігурації сегрегуються, нижче — лишаються випадковими»`.
- Перемоги/поразки нема; у Polygons є сценарій-виклик «Box of Friendship» (підказка — тримати пари поруч).

## Керування і ввід
- Polygons: перетягування мишею лише незадоволених фігур; кнопка авто-руху (незадоволені переїжджають у випадкові порожні місця); повзунок індивідуального упередження; повзунок «попиту на різноманіття»; кнопки скидання сцен; вільна пісочниця наприкінці.
- NetLogo: SETUP (розставити), GO (запуск), повзунки %-SIMILAR-WANTED і DENSITY (DENSITY діє після SETUP), вибір VISUALIZATION (OLD або SQUARE-X).

## Вікна, меню, HUD
- Polygons — одна довга сторінка-`tutorial-window` з розділами: правило → перетягування → авто-рух → повзунок упередження → старт із сегрегованого світу (зниження упередження не змішує) → попит на різноманіття (змішує) → Box of Friendship → пісочниця → висновки.
- `game-screen` Polygons: поле фігур з «настроєм», `stats-plot` (пропозиція) «сегрегація в часі», `param-slider` (пропозиція) упередження / різноманіття.
- `game-screen` NetLogo: світ, кнопки SETUP / GO, повзунки, монітори % SIMILAR, NUM-UNHAPPY, % UNHAPPY, графіки % SIMILAR і NUM-UNHAPPY.
- HUD: `mood-marker` (пропозиція) — позначка незадоволеного агента; `remaining-counter` — кількість незадоволених.
- Переходи: Polygons — прокручування від розділу до розділу; NetLogo — один екран.

## Фічі поза полем
- `tutorial` — вся Polygons є покроковим поясненням зі зростанням складності.
- `mode-sandbox` — фінальна пісочниця Polygons.
- Сканування параметра: NetLogo пропонує порівняти %-SIMILAR-WANTED (30 → в середньому ~70 % своїх) і 40, вплив DENSITY на час до зупинки, налаштування, за яких модель «ніколи не закінчує».
- Збережень і рекордів нема.

## Варіації й родичі
- **Осі варіацій:** правило переїзду (випадкова вільна клітина / найближча / та, де буде задоволений / стратегічно найкраща — «Schelling games») · поріг знизу і зверху (попит на різноманіття) · кількість груп і їхні частки · густина порожніх клітин · межа (тор / обмежене поле) · витрати на переїзд (Hatna & Benenson; Mantzaris — грошова змінна).
- Фізична аналогія: динаміка схожа на модель Ізінга; міра задоволеності R і ентропія S = k_B ln Ω(R), оцінена Монте-Карло.
- Rogers & McKane — єдиний підхід до варіантів моделі.
- Нащадок за ідеєю — [sugarscape](sugarscape.md) (Wikipedia Sugarscape називає статтю Шеллінга 1969 року попередником; там є племена й культурні мітки).
- Родичі в корпусі: [game-of-life](game-of-life.md) (стан від сусідів, але без переїздів), [simant](simant.md) (агенти на сітці), [cities-skylines-zoning](cities-skylines-zoning.md) (місто з попиту).

## Цікавинки для курсу
- Модель Шеллінга з порогом і переїздом у випадкову вільну клітину — 🌱 (частка сусідів + список порожніх).
- Три правила переїзду (випадкова / найближча / та, де задоволений) і порівняння фінальної сегрегації — 📎.
- Метрика «% схожих» і графік у часі + сканування порогу з пошуком ~1/3 — 🥉.
- Ручний режим як у Polygons: drag лише незадоволених, підсвітка настрою — 📎.
- Попит на різноманіття (верхній поріг) і сценарій «почати з сегрегованого світу» — 📎.
- Детектор «ніколи не зупиниться» (цикл переїздів) — 🥈.

## Мапа на каталог
- Є: `drag-drop-piece` (Polygons) · `game-loop` + `game-pause` · `state-as-data` · `game-settings` (повзунки) · `wrap-edges` (NetLogo) · `spawn-random-cell` · `gui-render` · `logic-render-split` · `unit-tests` (частка сусідів, ігнор порожніх) · `tutorial-window` (Polygons).
- **Нема** → пропозиції карток:
  - `+threshold-relocation` «Агент переїжджає, коли частка схожих сусідів нижча за поріг» · entities/move · 📎 · слоти {threshold, upper, move_rule}.
  - `+mood-marker` «Позначка настрою агента (задоволений / незадоволений)» · interface/hud · 🌱.
  - Перевикористано: `+random-soup`, `+step-run-speed`, `+parameter-sweep` (BML).

## Пропозиції до словників
- `+cond:neighbor_share(a, kind, op, x)` — частка сусідів виду серед зайнятих сусідніх клітин (Schelling, Polygons); `adjacent_count` дає кількість, а не частку.
- `+card:threshold-relocation`, `+card:mood-marker` — див. «Мапа на каталог».
- `+ui:mood-marker` — позначка незадоволених на полі (X / сумна фігура).
- `+ui:stats-plot`, `+ui:param-slider` — графік метрики й повзунок параметра (повтор Lenia / BML).

## Джерела
- ⭐ [Parable of the Polygons](https://ncase.me/polygons/) — правило «переїду, якщо менше 1/3 сусідів схожі», перетягування лише незадоволених, авто-рух у випадкові порожні місця, графік сегрегації, повзунки упередження й різноманіття (до 90 %), Box of Friendship, пісочниця; Vi Hart і Nicky Case, 2014.
- [Wikipedia: Schelling's model of segregation](https://en.wikipedia.org/wiki/Schelling%27s_model_of_segregation) — N×N, 8 сусідів, Ba, B ≥ Ba, порожні не рахуються, Bseg ≈ 1/3, Ізінг, Hatna & Benenson, Mantzaris, Rogers & McKane, Schelling games, стаття 1971.
- [NetLogo: Segregation](https://ccl.northwestern.edu/netlogo/models/Segregation) — помаранчеві й сині, %-SIMILAR-WANTED, DENSITY, переїзд у nearby patch, тор, монітори й графіки, OLD / SQUARE-X, «30 % → ~70 %».
- YouTube: пошук «Schelling segregation model».

## Непевне
- (?) Оригінальна паперова версія Шеллінга (рядок і шахівниця з монетами) і рік 1969 vs 1971 — відкриті джерела згадують лише статті 1969 (Models of Segregation) і 1971 (Dynamic Models of Segregation).
- (?) Чи є в Polygons стан «meh» (усі сусіди такі самі) — у переказі сторінки не видно.
- (?) Як саме NetLogo обирає «nearby patch» (напрям і відстань) — на сторінці моделі не описано.
- (?) У тексті Wikipedia «Bseg approximately 13» — очевидно, 1/3 (так у підписі до рисунка).
