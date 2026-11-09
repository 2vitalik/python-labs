---
title: Minami Lane
slug: minami-lane
aka: []
family: build-sim
also: []
klass: cursor
axes:
  field: 1d
  time: turn
  opponent: none
  info: partial
  random: runtime
  goal: state
year: 2024
platforms: [Windows, macOS, Linux, Switch, PS4, PS5, Xbox One, Xbox Series X/S]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Minami_Lane", best: true, note: "одна вулиця, місії з цілями за день, меню й ціни крамниць, дві фази дня, звіт, sandbox Planner/Creative"}
  - {kind: steam, url: "https://store.steampowered.com/app/2678990/Minami_Lane/", note: "будинки → мешканці, рецепти й ціни, сміття, випадкові події, коти й танукі, 2–4 год"}
  - {kind: other, url: "https://www.siliconera.com/review-minami-lane-feels-neighborly/", note: "рецензія: стартові $280, ціни й умови будівель, складники боби, танукі"}
  - {kind: other, url: "https://www.gamereactor.eu/minami-lane-1578993/", note: "рецензія: одна будівля на день, ряд із незмінною правою стороною, цикл дня, 5 місій"}
  - {kind: other, url: "https://hardcoregamer.com/review-minami-lane/", note: "рецензія: швидкість дня, щоденний звіт, йокаї, танукі-гід"}
  - {kind: official, url: "https://minamilane.carrd.co/", note: "офіційна сторінка, магазини платформ"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=PqaRsw4DNX8", note: "трейлер (з офіційної сторінки)"}
stage: v1
coverage: 50
mechanics: [cell-click, cursor-place, round-currency, in-round-upgrades, shop-catalog, sequential-levels, level-unlock, mode-select, achievements-window, +one-row-street, +build-then-simulate-day, +recipe-editor, +price-setting, +preference-satisfaction, +beauty-score, +daily-report, +click-litter, +hidden-bonus-npc, +mission-goals]
proposes: ["+effect:set_price", "+trigger:day_end", "+window:day-report", "+window:recipe-window", "+ui:satisfaction-meter", "+card:recipe-preference"]
author: opus
date: 2026-11-09
---

# Minami Lane — місто з однієї вулиці: щодня одна нова будівля, рецепти й ціни крамниць під смаки мешканців, потім дивишся, як минає день

## Суть
Затишний менеджмент на одному ряду ділянок: гравець ставить будинки (більше мешканців), крамниці (рамен, боба, книжки, квіти, караоке) і парки (краса), налаштовує в крамницях рецепти й ціни. Потім запускає день і дивиться, як мешканці ходять вулицею й залишають відгуки («хочу більше чаю»), а ввечері читає звіт про задоволення й гроші. Ядро — підбір рецепта й ціни під вподобання різних груп (молодь, старші) і умови відкриття будівель (населення, краса, задоволення). Місії мають цілі на кшталт «збудуй бобу, 15 мешканців, 75 % задоволення»; поразки нема.

## Поле і час
- Поле — **одна вулиця**: ряд ділянок (`field: 1d`); права сторона вулиці — незмінний шаблон, будуєш лише по один бік.
- Хід = день з двох фаз: (1) будівництво й налаштування — одна будівля на день, рецепти, ціни; (2) симуляція після «Start Day» — змінювати нічого не можна, лише збирати сміття, гладити котів і шукати танукі; швидкість дня регулюється.
- Кінець дня — щоденний звіт.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ділянка вулиці | terrain | порожня / зайнята | місце для однієї будівлі |
| Будинок (Modern House) | static | $100 | додає мешканців; апгрейд — ще мешканці або краса |
| Раменна | static | $100, потребує +5 людей | рецепт (кількість складників) і ціна |
| Боба-кафе | static | $200, потребує краси +2, 10 людей, 60 % задоволення | рецепт: чай, цукор, вершки, тапіока; ціна |
| Книгарня · квіткова крамниця · караоке | static | — | асортимент: типи книжок, вигляд букета; ціна |
| Парк | static | $150, потребує 5 людей | +5 краси |
| Мешканець | neutral | група (молодь / старші), вподобання | ходить вулицею, купує, ставить оцінку, лишає відгук |
| Йокай | neutral | — | особливий цінний клієнт (?) |
| Кіт | neutral | — | зʼявляється, коли вулиця гарна; можна гладити |
| Танукі | pickup | щодня переодягнений | знайти й клікнути → трохи грошей; також гід-оповідач |
| Сміття | hazard | — | зʼявляється на вулиці; клік прибирає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(build, building, slot)` → ЯКЩО `free(slot)` and `has(player, money)` and `custom: «умови будівлі: населення, краса, задоволення»` and `custom: «сьогодні ще не будували»` → ТО `place(player, building)`, `currency(-cost)`.
- КОЛИ `input(upgrade, building)` → ЯКЩО `has(player, money)` → ТО `custom: «+мешканці або +краса без парку»`, `currency(-cost)`.
- КОЛИ `input(set_recipe, shop)` → ТО `set_value(shop, recipe)`; КОЛИ `input(set_price, shop)` → ТО `set_value(shop, price)`.
- КОЛИ `input(start_day)` → ТО `custom: «фаза симуляції; налаштування заблоковано до вечора»`.
- КОЛИ `custom: «мешканець купив у крамниці»` → ТО `currency(+price)`, `custom: «задоволення = відповідність рецепта вподобанням його групи та ціна»`.
- КОЛИ `custom: «мешканець купив у крамниці»` → ЯКЩО `prob(p)` → ТО `message(feedback)` — відгук про рецепт; відгук можна зберегти.
- КОЛИ `counter(beauty, >=, n)` → ТО `spawn(cat)`, `custom: «мешканці щасливіші»`.
- КОЛИ `input(pet, cat)` → ТО `counter(cats_petted, +1)`.
- КОЛИ `rng(p)` → ТО `spawn_at(trash, street)`; КОЛИ `input(click, trash)` → ТО `disappear(trash)`.
- КОЛИ `custom: «початок дня»` → ТО `spawn_at(tanuki, random)` у вигляді предмета; КОЛИ `input(click, tanuki)` → ТО `currency(+small)`, `disappear(tanuki)`.
- КОЛИ `rng(p)` → ТО `custom: «випадкова подія, яку можна обернути на користь»`.
- КОЛИ `custom: «кінець дня»` → ТО `window(day_report)` — задоволення, фінанси, прогрес додаткових цілей.
- КОЛИ `all_constraints_met` → ТО `next_level`, `custom: «нові будівлі, типи мешканців»`; перша місія: боба-кафе + 15 мешканців + 75 % задоволення.
- КОЛИ `custom: «додаткова ціль виконана»` → ТО `counter(side_goals, +1)` — напр. погладити 20 котів, перша місія за 10 днів, лише 8 будівель (через апгрейди).
- КОЛИ `input(speed, day)` → ТО `custom: «день іде швидше»`.
- Перемога: цілі місії · Поразка: нема («без штрафу за повільність») · Рахунок: — .

## Керування і ввід
- Миша/геймпад: обрати будівлю → клік по вільній ділянці; кнопки апгрейду й вигляду (колір, дах) на будівлі.
- Клік по мешканцю — що він хоче; клік по сміттю, коту, підозрілому предмету (танукі).
- Кнопка «Start Day» і перемикач швидкості.

## Вікна, меню, HUD
- `game-screen`: вулиця збоку; HUD — гроші (`coins`), задоволення у % (`+ui:satisfaction-meter`), кількість мешканців, краса, цілі місії (`objective-text`).
- `+window:recipe-window` — налаштування крамниці: складники, асортимент, ціна.
- Список будівель з ціною й умовами відкриття (`shop-catalog`).
- `+window:day-report` — вечірній звіт.
- `main-menu` → `mode-select` (місії / sandbox: Planner, Creative) → `level-select` місій (?); `achievements-window` (Steam).

## Фічі поза полем
- `levels-sequential` + `level-unlock`: 5 місій (~3–4 год); нових рівнів після релізу не буде.
- `mode-sandbox`: Planner — обмежені ресурси; Creative — безлімітні.
- `speed-control`, досягнення Steam, хмарні збереження; 8 мов інтерфейсу.

## Варіації й родичі
- Родичі в корпусі: `islanders` (вільне поле, очки за сусідів), `tiny-tower-simtower` (крамниці й мешканці поверхами), `townscaper` (затишна іграшка), `plateup` (налаштування закладу під клієнтів), `luck-be-a-landlord` (ряд, що приносить гроші).
- Осі варіацій:
  - **поле:** сітка / один ряд (Minami Lane) / вежа поверхів;
  - **ритм:** real-time / день = хід із фазою планування й фазою спостереження;
  - **задоволення:** за наявність крамниці / за відповідність рецепта й ціни смаку групи.

## Цікавинки для курсу
- Вулиця як одномірний масив слотів з фіксованою іншою стороною — 🌱.
- Цикл «план → запуск дня → звіт»: дві фази з блокуванням вводу — 🌱.
- Рецепт як вектор складників і оцінка «відстань до вподобань групи» + чутливість до ціни — 📎.
- Будівлі з умовами відкриття (населення, краса, задоволення) — 🌱.
- Відгуки клієнтів як підказки (частково прихована інформація) — 📎.
- Прихований щоденний бонус (танукі серед предметів) і клік по сміттю — 🌱.

## Мапа на каталог
- Є: `cell-click` · `cursor-place` (будівля на ділянку) · `round-currency` (гроші вулиці) · `in-round-upgrades` (апгрейд будівлі) · `shop-catalog` (будівлі з цінами) · `sequential-levels` + `level-unlock` (місії) · `mode-select` (місії / sandbox) · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+one-row-street` «Поле — один ряд слотів» · field · 🌱.
  - `+build-then-simulate-day` «Фаза планування + фаза симуляції» · game-logic · 🌱.
  - `+recipe-editor` «Рецепт як набір кількостей» · interface/input · 📎.
  - `+price-setting` «Гравець ставить ціну» · game-logic/economy · 🌱.
  - `+preference-satisfaction` «Задоволення = збіг із вподобанням групи» · game-logic · 📎.
  - `+beauty-score` «Краса вулиці як лічильник з порогами» · game-logic · 🌱.
  - `+daily-report` «Вечірній звіт» · interface/menus · 🌱.
  - `+click-litter` «Клік прибирає сміття» · interface/input · 🌱.
  - `+hidden-bonus-npc` «Знайди переодягненого» · entities/spawn · 🌱.
  - `+mission-goals` «Набір цілей місії» · game-logic/win · 🌱.

## Пропозиції до словників
- `+effect:set_price` — встановити ціну товару (уже просили інші ігри).
- `+trigger:day_end` — кінець ігрового дня (звіт, підрахунок).
- `+window:day-report` — щоденний звіт; `+window:recipe-window` — налаштування рецепта й ціни.
- `+ui:satisfaction-meter` — % задоволення мешканців.
- `+card:recipe-preference` — підбір рецепта під смак груп.

## Джерела
- ⭐ [Wikipedia: Minami Lane](https://en.wikipedia.org/wiki/Minami_Lane) — місії й sandbox, приклад цілей, меню й ціни, апгрейди, дві фази дня, звіт, швидкість, розробники, дати й платформи.
- [Steam: Minami Lane](https://store.steampowered.com/app/2678990/Minami_Lane/) — будинки → мешканці, крамниці (рамен, боба, книжки, караоке), рецепти й ціни, сміття, випадкові події, коти й танукі, 2–4 год, мови.
- [Siliconera](https://www.siliconera.com/review-minami-lane-feels-neighborly/) — $280 і 5 мешканців на старті, ціни й умови раменної, будинку, парку, боби; складники боби; додаткові цілі; танукі.
- [Gamereactor](https://www.gamereactor.eu/minami-lane-1578993/) — одна будівля на день, незмінна права сторона, книгарня й квіткова, цикл дня, 5 місій.
- [Hardcore Gamer](https://hardcoregamer.com/review-minami-lane/) — швидкість дня, звіт, йокаї, коти, танукі-гід.
- [Офіційна сторінка](https://minamilane.carrd.co/) · [трейлер](https://www.youtube.com/watch?v=PqaRsw4DNX8).

## Непевне
- (?) Довжина вулиці в ділянках і чи бувають будівлі на кілька ділянок.
- (?) Роль йокаїв (лише «цінні клієнти» в одній рецензії) і повний перелік груп мешканців.
- (?) Формула задоволення (рецепт vs ціна) — лише з опису рецензій.
- (?) Чи «одна будівля на день» стосується всіх режимів (Planner/Creative).
- (?) Вибір місії зі списку чи лише послідовно.
