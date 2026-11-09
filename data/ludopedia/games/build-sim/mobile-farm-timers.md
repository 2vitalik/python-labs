---
title: FarmVille і Hay Day — ферма на годиннику
slug: mobile-farm-timers
aka: [FarmVille, Hay Day, ФармВіль, Хей Дей]
family: build-sim
also: []
klass: cursor
axes:
  field: iso
  time: realtime
  opponent: coop
  info: full
  random: runtime
  goal: none
year: 2009
platforms: [web, Facebook, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/FarmVille", best: true, note: "оранка за монети, ріст за час, вʼянення після 2.5× часу росту, Farm Cash, сусіди, кооперативи"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hay_Day", note: "виробничі будівлі, вантажівка/корабель, придорожній магазин, силос і амбар з лімітом, діаманти"}
  - {kind: official, url: "https://supercell.com/en/games/hayday/", note: "Supercell: «урожай ніколи не гине»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hay+Day+gameplay", note: "пошук; геймплей Hay Day"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=FarmVille+2009+gameplay", note: "пошук; геймплей FarmVille"}
stage: v1
coverage: 55
mechanics: [cell-click, multi-select, swipe-gestures, multi-cell-size, cell-transform, timed-despawn, round-currency, shop-catalog, shop-window, inventory, inventory-limit, async-multiplayer, online-multiplayer, save-autosave, level-unlock, popup-text, status-panel, +growth-stages, +wallclock-timer, +wither-window, +premium-speedup, +production-queue, +storage-cap, +order-board, +player-market, +xp-level-unlock, +neighbor-help, +offline-progress]
proposes: ["+trigger:wallclock(t)", "+cond:capacity(store, op, n)", "+effect:enqueue(building, recipe)", "+window:order-board", "+window:roadside-shop", "+ui:ready-icon", "+ui:queue-slots", "+feature:premium-speedup", "+feature:offline-progress", "+card:wither-window", "+card:production-queue"]
author: opus
date: 2026-11-09
---

# FarmVille і Hay Day — ферма на справжньому годиннику: клітина-грядка з таймером, вʼянення (FarmVille) проти вічного врожаю і виробничих черг (Hay Day)

## Суть
Гравець клікає по клітинах ферми: оре, сіє, повертається через реальні хвилини чи години й збирає. Час іде, коли гру закрито, — ядро вимірюється годинником світу, а не тіками. FarmVille карає за запізнення: посів **вʼяне**, якщо не зібрати за 2.5× часу росту. Hay Day знімає покарання («урожай ніколи не гине»), натомість додає **виробничі будівлі з чергами** і ліміти складів — ферма стає ланцюжком «зерно → корм → яйця → торт». Відмінність від `stardew-farm` і `harvest-moon`: нема аватара, денного циклу й витривалості; є лише годинник і гаманець.

## Поле і час
- Ферма — ізометрична сітка; грядка — клітина (FarmVille: ділянка 1 клітина (?), Hay Day: поле 1 клітина (?)); будівлі, тварини, дерева займають кілька клітин.
- Поле розширюється: FarmVille — розширення за монети (?); Hay Day — земля за спецпредмети (?).
- Час — **реальний годинник** (wall-clock): кожна грядка/будівля зберігає момент старту й тривалість; стан рахується при відкритті гри.
- Нема поразки й кінця; темп задає тривалість культур (від хвилин до днів (?)).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Порожня земля | terrain | — | FarmVille: оранка (за монети) → зорана ділянка |
| Зорана ділянка | terrain | — | можна посіяти насіння з магазину |
| Посів | object | культура, час росту, ціна, дохід, XP | росте за таймером → готовий; FarmVille: після 2.5× часу росту вʼяне |
| Зівʼялий посів (FarmVille) | object | — | нічого не дає; «оживити» за Farm Cash або прибрати |
| Поле Hay Day | terrain | — | посів росте за таймером і чекає збору без обмеження |
| Тварина | neutral | продукт, інтервал | FarmVille: збір за інтервалом, не гине; Hay Day: потрібен корм (?) |
| Дерево / кущ | object | продукт, інтервал | FarmVille: не вʼяне, збір періодично |
| Виробнича будівля (Hay Day) | object | рецепти, черга, час | бере інгредієнти (культури, продукти тварин, вироби інших будівель) → виріб |
| Силос (Hay Day) | container | місткість | зберігає культури; повний — більше не взяти |
| Амбар (Hay Day) | container | місткість | зберігає вироби й продукти; апгрейд — рідкісні предмети |
| Вантажівка / корабель замовлень (Hay Day) | sink | список товарів, нагорода | замовлення за монети й XP |
| Відвідувачі містечка (Hay Day) | neutral | запит | купують товари |
| Придорожній магазин (Hay Day) | container | слоти, ціна | гравець виставляє товари; інші гравці купують за монети |
| Сусід | ally | — | FarmVille: відвідини до 5 разів на день, допомога, подарунки, кооператив |
| Декор | static | — | вигляд ферми; без поведінки (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(plow, land)` → ЯКЩО `counter(coins, >=, plow_cost)` → ТО `set_cell(land, plowed)`, `currency(-plow_cost)`, `counter(xp, +n)` (FarmVille).
- КОЛИ `input(seed, plot)` → ЯКЩО `cell(plot, plowed)` and `custom: «культура відкрита рівнем (або дозволом за Farm Cash)»` → ТО `place(player, crop)`, `currency(-seed_cost)`, `set_state(crop, growing)`.
- КОЛИ `custom: «минув час росту за годинником світу»` → ЯКЩО `state(crop, growing)` → ТО `set_state(crop, ready)`, `custom: «іконка готовності»`.
- КОЛИ `custom: «минуло 2.5 × час росту»` → ЯКЩО `state(crop, ready)` and `mode(FarmVille)` → ТО `transform(crop, withered)`.
- КОЛИ `input(unwither, crop)` → ЯКЩО `has(player, farm_cash)` → ТО `transform(withered, ready)`, `take(player, farm_cash)`.
- КОЛИ `input(instant_grow)` → ЯКЩО `has(player, farm_cash)` → ТО `custom: «біплан: усі посіви готові одразу»`.
- КОЛИ `input(harvest, crop)` → ЯКЩО `state(crop, ready)` → ТО `currency(+income)`, `counter(xp, +n)`, `set_cell(plot, plowed)` (FarmVille) / `give(silo, crop)` (Hay Day).
- КОЛИ `input(harvest, crop)` → ЯКЩО `mode(HayDay)` and `custom: «силос повний»` → ТО `block`, `message(«силос повний»)`.
- КОЛИ `custom: «минув інтервал тварини / дерева»` → ТО `set_state(animal, ready)`; не вʼяне й не гине.
- КОЛИ `input(enqueue, building, recipe)` → ЯКЩО `has(barn_or_silo, ingredients)` and `custom: «є вільний слот черги»` → ТО `take(store, ingredients)`, `custom: «виріб стає в чергу»` (Hay Day).
- КОЛИ `custom: «виріб у голові черги готовий»` → ТО `custom: «наступний у черзі стартує»`; готовий виріб чекає на будівлі до збору.
- КОЛИ `input(collect, product)` → ЯКЩО `custom: «в амбарі є місце»` → ТО `give(barn, product)`, `counter(xp, +n)`; інакше `block`.
- КОЛИ `input(speed_up, timer)` → ЯКЩО `has(player, diamonds)` → ТО `custom: «таймер завершується одразу»`, `take(player, diamonds)` (Hay Day).
- КОЛИ `input(fulfil, order)` → ЯКЩО `has(barn, order_items)` → ТО `take(barn, order_items)`, `currency(+reward)`, `counter(xp, +n)` (вантажівка, корабель, відвідувач).
- КОЛИ `input(buy, roadside_offer)` → ЯКЩО `counter(coins, >=, price)` → ТО `currency(-price)`, `give(barn, item)`, `custom: «гроші — продавцю»`.
- КОЛИ `counter(xp, >=, threshold)` → ТО `counter(level, +1)`, `unlock(crops_items_buildings)`.
- КОЛИ `input(visit, neighbor_farm)` → ЯКЩО `counter(visits_today, <, 5)` → ТО `custom: «допомога на чужій фермі»`, `currency(+n)` (FarmVille).
- КОЛИ `input(gift, neighbor)` → ТО `give(neighbor, gift)` — безкоштовно; варіант «таємний подарунок» `rng`.
- КОЛИ `counter(coop_crop, >=, target)` → ТО `custom: «кооператив виконано, нагорода всім»` (FarmVille).
- КОЛИ `input(upgrade, barn)` → ЯКЩО `has(player, rare_items)` → ТО `custom: «місткість зростає»`, `take(player, rare_items)`.
- Перемога: нема · Поразка: нема (лише втрачений урожай у FarmVille) · Рахунок: XP-рівень, монети.

## Керування і ввід
- Клік/тап по клітині — дія поточного інструмента (оранка, посів, збір); FarmVille мав «мультиінструмент» для серії клітин (?).
- Hay Day: протягнути насіння чи серп пальцем по ряду полів — посів/збір одним свайпом (?).
- Тап по будівлі → панель рецептів і черги; перетягнути рецепт у слот (?).
- Перетягування будівель і декору для перестановки.

## Вікна, меню, HUD
- `game-screen`: ферма, монети й преміум-валюта (`coins`), рівень і смуга XP (`progress-bar`), іконки готовності над клітинами (`+ui:ready-icon`), `popup-text` (+монети, +XP).
- `shop-window`: насіння, тварини, будівлі, декор; FarmVille — розділ за Farm Cash.
- Панель будівлі: рецепти, слоти черги з таймерами (`+ui:queue-slots`, `timer-countdown`).
- `+window:order-board`: дошка замовлень вантажівки й корабель (Hay Day).
- `+window:roadside-shop`: свій прилавок і чужі (Hay Day); газета з оголошеннями (?).
- `inventory-window`: силос і амбар із заповненістю (Hay Day).
- `custom-window` сусіди/сусідство, подарунки; `settings-window`.

## Фічі поза полем
- `+feature:offline-progress`: таймери йдуть, коли гру закрито; повернення в гру — ядро петлі.
- `+feature:premium-speedup`: Farm Cash / діаманти миттєво завершують таймер, оживляють посів.
- `xp-level` і `level-unlock`: рівень відкриває культури, будівлі, тварин.
- Соціальне: сусіди (FarmVille — до 5 відвідин на день, фермхенди, кооперативи; Hay Day — сусідства і дербі з 2014), подарунки.
- FarmVille: нові ферми-локації кожні ~6 тижнів (Англія, Гаваї, Японія…); бренд-партнерства.
- `cloud-save` — стан на сервері; FarmVille на Facebook закрито 31.12.2020.

## Варіації й родичі
- У корпусі: `stardew-farm`, `harvest-moon` (аватар, день-тік, полив), `acnh-flowers` (селекція на клітинах), `big-pharma` / `factorio-belts` (виробничі ланцюги, тут — без конвеєрів).
- Наступники: FarmVille 2 (2012), FarmVille 2: Country Escape (2014, офлайн), FarmVille 3 (2021); Hay Day Pop (2020–2021).
- Осі «запізнення»: посів вʼяне (FarmVille) / чекає вічно (Hay Day) / гине з сезоном (`stardew-farm`).
- Осі «виробництво»: грядка → гроші одразу / склад + черга будівель + замовлення.
- Осі «часу»: wall-clock (тут) / день-тік (`harvest-moon`) / покроковий.

## Цікавинки для курсу
- Таймер на клітині за справжнім годинником: зберегти момент старту, стан рахувати при завантаженні — 🌱.
- Вікно вʼянення: готовий → зівʼялий після 2.5× часу росту — 🌱.
- Виробнича черга будівлі зі слотами: стартує лише голова, решта чекає — 📎.
- Склади з лімітом місткості й блок збору при переповненні — 🌱.
- Дошка замовлень: виконати набір товарів зі складу — 📎.
- Прискорення за преміум-валюту як «пропуск таймера» — 🌱.
- Ринок між гравцями (придорожній магазин) — 🥈 (асинхронна торгівля, сервер).

## Мапа на каталог
- Є: `cell-click` · `multi-select` / `swipe-gestures` (серії клітин) (?) · `multi-cell-size` (будівлі) · `cell-transform` (оранка, вʼянення) · `timed-despawn` (вʼянення як «втрата за часом») · `round-currency` · `shop-catalog` / `shop-window` · `inventory` / `inventory-limit` (силос, амбар) · `async-multiplayer` / `online-multiplayer` (сусіди) · `save-autosave` · `level-unlock` · `popup-text` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+wallclock-timer` «Таймер за реальним годинником» · entities/state · 🌱.
  - `+wither-window` «Готове псується, якщо не зібрати вчасно» · entities/state · 🌱.
  - `+production-queue` «Черга виробництва будівлі зі слотами» · game-logic/economy · 📎 · слоти {slots, recipes}.
  - `+storage-cap` «Склад з лімітом, блок при переповненні» · game-logic/economy · 🌱.
  - `+order-board` «Дошка замовлень на набір товарів» · game-logic/win · 📎.
  - `+premium-speedup` «Миттєве завершення таймера за валюту» · game-logic/economy · 🌱.
  - `+player-market` «Прилавок для інших гравців» · game-logic/opponent · 🥈.
  - `+xp-level-unlock`, `+neighbor-help`, `+offline-progress`, `+growth-stages` (як у `stardew-farm`).

## Пропозиції до словників
- `+trigger:wallclock(t)` — настав момент реального часу (відмінно від `timer` у тіках).
- `+cond:capacity(store, op, n)` — вільне місце на складі.
- `+effect:enqueue(building, recipe)` — поставити виріб у чергу будівлі.
- `+window:order-board`, `+window:roadside-shop` — замовлення й прилавок.
- `+ui:ready-icon` — значок «готово» над клітиною; `+ui:queue-slots` — слоти черги з таймерами.
- `+feature:premium-speedup`, `+feature:offline-progress` — див. вище.
- `+card:wither-window`, `+card:production-queue` — див. вище.

## Джерела
- ⭐ [Wikipedia: FarmVille](https://en.wikipedia.org/wiki/FarmVille) — оранка за монети, ріст за час, вʼянення після 2.5× часу росту, Farm Cash (оживити, біплан), тварини й дерева не вʼянуть, сусіди 5 разів на день, подарунки, кооперативи, локації, закриття 31.12.2020.
- [Wikipedia: Hay Day](https://en.wikipedia.org/wiki/Hay_Day) — виробничі будівлі з інгредієнтів, вантажівка/корабель/відвідувачі, придорожні магазини, силос і амбар з апгрейдом рідкісними предметами, діаманти, сусідства й дербі.
- [Supercell: Hay Day](https://supercell.com/en/games/hayday/) — «урожай ніколи не гине».
- YouTube: пошуки «Hay Day gameplay», «FarmVille 2009 gameplay».

## Непевне
- (?) Розміри ділянок і полів у клітинах; механіка розширення ферми в обох іграх.
- (?) Hay Day: збір дає 2 одиниці, посів витрачає 1 зі силосу — з памʼяті.
- (?) Hay Day: тварини їдять корм із кормового млина; кількість слотів черги й купівля нових за діаманти — з памʼяті.
- (?) Свайп серпом/насінням по ряду полів (Hay Day) і мультиінструмент (FarmVille) — з памʼяті.
- (?) Газета з оголошеннями придорожніх магазинів, спецпредмети розширення земель — з памʼяті.
- (?) Тривалості культур (хвилини–дні) не перевірені.
- Hay Day fandom і FarmVille fandom віддали 402 — у шапку не взято.
