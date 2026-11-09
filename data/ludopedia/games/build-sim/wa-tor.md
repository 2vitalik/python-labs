---
title: Wa-Tor (Ва-Тор)
slug: wa-tor
aka: [Wator, WATOR, «Water Torus», «акули й риби», Sharks and Fish]
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
year: 1984
platforms: [web, PC]
links:
  - {kind: play, url: "http://www.leinweb.com/snackbar/wator/", best: true, note: "JS-симулятор Leinweber: правила, 7 повзунків з дефолтами, Stop/Go/Remix, графік популяцій"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wa-Tor", note: "Dewdney, Scientific American, грудень 1984; тор, правила риб і акул, енергія, три результати"}
  - {kind: other, url: "https://seed7.net/scrshots/wator.htm", note: "Seed7: параметри nfish, nsharks, fbreed, sbreed, starve"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Wa-Tor+simulation", note: "пошук; симуляції"}
stage: v1
coverage: 70
mechanics: [random-walk, wrap-edges, hunger-clock, chase-greedy, spawn-random-cell, game-loop, game-pause, state-as-data, game-settings, settings-elements, field-size-picker, logic-render-split, unit-tests, +breed-timer, +predator-prey, +population-graph, +update-order, +step-run-speed]
proposes: ["+ui:population-graph", "+ui:param-slider", "+feature:remix", "+card:breed-timer", "+card:predator-prey", "+card:population-graph"]
author: opus
date: 2026-11-09
---

# Wa-Tor — планета-тор під водою: риби блукають і розмножуються, акули їдять риб і гинуть з голоду

## Суть
Модель «хижак — жертва» А. К. Дьюдні з колонки Computer Recreations (Scientific American, грудень 1984). На сітці-торі живуть риби й акули: щохронону риба робить випадковий крок, акула — крок на рибу (зʼїдає її) або випадковий крок; дожившись до віку розмноження, тварина лишає на старому місці нащадка; акула без їжі гине. Гравець лише задає параметри й стартові популяції та дивиться, як популяції коливаються (як у рівняннях Лотки — Вольтерри) або вимирають. На відміну від Life, це не синхронний автомат клітин, а **агенти з таймерами** на сітці.

## Поле і час
- Прямокутна сітка, склеєна в **тор**: хто виходить за край, зʼявляється з протилежного боку (`wrap-edges`). Уся планета — вода.
- Клітина: порожня / риба / акула (одна істота на клітину).
- Сусідство — 4 клітини (вгору, вниз, ліворуч, праворуч; Leinweb).
- Тік = **хронон**: кожна істота діє один раз. Порядок обходу (усі риби, потім акули; випадковий) у джерелах не описано — див. «Непевне».
- Leinweb: поле Size від 1 до 217 856 клітин; Delay 0–100 сповільнює цикл.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вода (порожня клітина) | terrain | — | прохідна; сюди ходять і тут народжуються |
| Риба | neutral | вік, fbreed | крок у випадкову вільну сусідню клітину; немає вільних — стоїть; у віці fbreed лишає нову рибу на старому місці |
| Акула | enemy | вік, sbreed; енергія або лічильник голоду (starve) | крок на сусідню рибу (зʼїдає) або у вільну клітину; розмножується як риба; без їжі гине |
| Край поля | static | тор | склеєний із протилежним краєм |
| Популяції | object | кількість риб і акул | емерджентні коливання: багато риб → вибух акул → риб мало → акули голодують → риби відновлюються |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(go)` → ТО `custom: «розкидати nfish риб і nsharks акул у випадкові вільні клітини»` (Leinweb: Remix; зміна Size/Sharks/Fish теж робить remix).
- Риба: КОЛИ `tick` → ЯКЩО `free(nbr4)` → ТО `move(fish, random_free_nbr4)`; інакше `block` (лишається).
- КОЛИ `edge(a)` → ТО `wrap(a)` — для риб і акул.
- Риба: КОЛИ `after(move)` → ЯКЩО `counter(age, ≥, fbreed)` → ТО `spawn(fish, old_cell)`, `counter(age, 0)`.
- Акула: КОЛИ `tick` → ЯКЩО `occupied(nbr4, fish)` → ТО `move(shark, random_fish_nbr4)`, `disappear(fish)`, `counter(energy, +E)`.
- Акула: КОЛИ `tick` → ЯКЩО `not occupied(nbr4, fish)` and `free(nbr4)` → ТО `move(shark, random_free_nbr4)`; немає вільних → `block`.
- Акула (Вікіпедія): КОЛИ `tick` → ТО `counter(energy, −1)`.
- Акула (Вікіпедія): КОЛИ `counter(energy, ≤, 0)` → ТО `disappear(shark)`.
- Акула (Seed7/Leinweb): КОЛИ `counter(since_meal, ≥, starve)` → ТО `disappear(shark)`; їжа обнуляє лічильник (картка hunger-clock).
- Акула: КОЛИ `after(move)` → ЯКЩО `counter(age, ≥, sbreed)` → ТО `spawn(shark, old_cell)`, `counter(age, 0)`.
- Leinweb: КОЛИ `spawned(animal)` → ТО `custom: «breed і starve новонародженого трохи випадково відхиляються від значень повзунків»`.
- Leinweb: КОЛИ `input(slider)` → ТО `custom: «нове breed/starve діє на тварину лише після її наступного розмноження чи їжі»`.
- Наслідок (Вікіпедія): КОЛИ `all_gone(shark)` → ТО `custom: «риби без ворогів заповнюють океан»`.
- Наслідок (Вікіпедія): КОЛИ `all_gone(fish)` → ТО `custom: «акули гинуть від голоду, океан порожніє»`. Мала стартова кількість риб або короткий starve — вимирають акули.
- Перемоги/поразки нема; неформальна мета з Leinweb — підібрати параметри, щоб обидві популяції жили стабільно.

## Керування і ввід
- Leinweb: повзунки Size, Sharks, Fish, Shark Breed, Fish Breed, Shark Starve, Delay (праворуч — більше); кнопки Stop / Go / Remix.
- Seed7: стартовий екран → будь-яка клавіша запускає; будь-яка клавіша під час роботи зупиняє.
- Оригінал 1984 — програма-«рецепт» для читачів журналу; параметри задавались на старті (nfish, nsharks, fbreed, sbreed, starve).

## Вікна, меню, HUD
- `game-screen` (Leinweb): угорі світ Wa-Tor (риби зелені, акули червоні, тло світло-блакитне), унизу `population-graph`.
- `population-graph`: криві риб і акул, 0 знизу, загальна кількість клітин угорі; чорна вертикаль біжить зліва направо на піксель за цикл і загортається; біла вертикаль позначає розрив (зміна параметра, Remix).
- Панель `param-slider` ×7 + Stop/Go/Remix на тому самому екрані; окремих вікон нема.
- Seed7: `splash-screen` → `game-screen` (риби зелені, акули сині).

## Фічі поза полем
- `custom-difficulty` ~ параметри breed/starve/кількості; `speed-control` (Delay); `pause` (Stop/Go).
- `remix` — випадково перерозкласти тварин без зміни параметрів.
- Leinweb: 2025 JS/HTML-версії й оригінальний Java-аплет 1995 року.
- Нема рахунку, збережень, рівнів.

## Варіації й родичі
- **Осі варіацій:** голод (енергія з поповненням за рибу / лічильник ходів без їжі) · сусідство (4 / 8) · порядок оновлення (послідовний / випадковий / синхронний з конфліктами) · розкид параметрів у нащадків (так у Leinweb / ні) · кількість видів (2 / харчовий ланцюг).
- Відкриті реалізації: Planet Wator (NYU), Java-аплет panmental, Seed7, HTML5 wa-tor.saidone.org, версія для домашнього компʼютера Sinclair ZX (Syncware, 1985) (?) — усе з External links Вікіпедії.
- Родичі: рівняння Лотки — Вольтерри (неперервний аналог); у корпусі — [simant](simant.md) (агенти-мурахи з потребами), [game-of-life](game-of-life.md) (синхронний автомат замість агентів), [langtons-ant](langtons-ant.md) (агент на сітці).

## Цікавинки для курсу
- Базовий Wa-Tor на торі з fbreed/sbreed/starve — 🌱 (класична лаба на 2D-масив і `random.choice`).
- Прапорець «вже ходив цього хронону» (риба, що переїхала вперед, не має ходити двічі) — 📎 (пастка порядку оновлення).
- Графік популяцій у реальному часі з бігунком і позначками розривів — 🥉.
- Порівняти порядки оновлення (риби → акули / перемішаний список / випадковий обхід клітин) і їхній вплив на коливання — 🥈.
- Пошук параметрів, за яких обидва види живуть N хрононів (перебір / оптимізація) — 🥈.
- Третій вид або «планктон» як ресурс, що відростає — 📎 поверх двіжка.

## Мапа на каталог
- Є: `random-walk` (риба) · `chase-greedy` (крок акули на сусідню рибу) · `wrap-edges` (тор) · `hunger-clock` (starve) · `spawn-random-cell` (стартовий розклад, Remix) · `game-loop` + `game-pause` · `state-as-data` · `game-settings` + `settings-elements` + `field-size-picker` (Size) · `logic-render-split` · `unit-tests`.
- **Нема** → пропозиції карток:
  - `+breed-timer` «Розмноження за віком: нащадок на старому місці» · entities/spawn · 🌱 · слоти {period, jitter}.
  - `+predator-prey` «Хижак і жертва на сітці» · entities/interact · 📎 · слоти {energy_gain, starve}.
  - `+population-graph` «Графік популяцій у часі» · interface/hud · 🥉 · слоти {series, sweep}.
  - Перевикористано: `+update-order`, `+step-run-speed`.

## Пропозиції до словників
- `+ui:population-graph` — криві кількостей видів у часі (Wa-Tor, Lenia «stats»).
- `+ui:param-slider` — повзунок параметра моделі, що діє «на льоту» (вже просила Lenia).
- `+feature:remix` — випадково перерозкласти сутності з тими самими параметрами.
- `+card:breed-timer`, `+card:predator-prey`, `+card:population-graph` — див. «Мапа на каталог».

## Джерела
- ⭐ [Leinweb: WATOR Predator-Prey Simulation](http://www.leinweb.com/snackbar/wator/) — правила, повзунки й дефолти (Size 1000, Sharks 1, Fish 999, Shark Breed 10, Fish Breed 3, Shark Starve 3, Delay 10), розкид breed/starve у нащадків, Stop/Go/Remix, графік.
- [Wikipedia: Wa-Tor](https://en.wikipedia.org/wiki/Wa-Tor) — автор і стаття 1984, тор, рух риб і акул, енергія, розмноження, три довгострокові результати, лінки на реалізації.
- [Seed7: Wator](https://seed7.net/scrshots/wator.htm) — параметри nfish, nsharks, fbreed, sbreed, starve; керування клавішами.
- YouTube: пошук «Wa-Tor simulation».

## Непевне
- (?) Порядок обходу істот у хрононі (спершу всі риби, потім акули; один прохід по клітинах з прапорцем «ходив») — джерела не описують; Вікіпедія каже лише, що вибір робить генератор випадкових чисел.
- (?) Енергія (Вікіпедія) проти лічильника «хрононів без їжі» (Seed7, Leinweb) — який варіант був у Дьюдні, не перевірено; стартових значень у статті Вікіпедії нема.
- (?) Чи розмножується риба, якщо їй нікуди ходити (Leinweb: «якщо є вільна клітина»), — деталь різниться між версіями.
- (?) Версія для Sinclair ZX — лише за підписом лінку у Вікіпедії, сторінка archive.org не відкрилась (таймаут).
